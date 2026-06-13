#!/usr/bin/env python3
# /// script
# requires-python = ">=3.12"
# dependencies = []
# ///
"""Shared verbatim-extraction core for the merged routing battery.

This module holds BOTH detectors (boundary Signal A + focused-output
classifier), the single Plan-36-locked transport, the shared
parsing/utility helpers, the merged-catalog parser, and the both-match
verdict function.

Every detector/transport/utility region is a VERBATIM MOVE from:
  - scripts/check-sub-skill-routing.py  (boundary / Signal A discipline)
  - scripts/check-focused-output.py     (focused-output classifier)

No logic is re-derived (honors BATT-02/03 and D-05). Renames:
  - Prompt (boundary)        → BoundaryPrompt        (CR-3)
  - Prompt (focused)         → FocusedPrompt         (CR-3)
  - parse_catalog (boundary) → parse_boundary_catalog (CR-2)
  - parse_catalog (focused)  → parse_focused_catalog  (CR-2)
  - _signal_a                → _boundary_signal_a     (CR-5/Pitfall 3)
  - _signal_a_invocations    → _focused_signal_a_invocations (CR-5/Pitfall 3)
  - self_test (boundary)     → self_test_boundary()
  - self_test (focused)      → self_test_focused()

New symbols (no source analog, added for merged battery):
  - MergedPrompt
  - parse_merged_catalog
  - _run_prompt_n_times_to_paths   (CR-1: path-returning transport)
  - _validate_kn
  - _both_match
"""

from __future__ import annotations

import argparse
import datetime as _dt
import json
import re
import shutil
import subprocess
import sys
import tempfile
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Literal

# Python 3.13 compat: when loaded via importlib spec loader without
# pre-registering in sys.modules, dataclasses._process_class raises
# AttributeError because sys.modules[cls.__module__] is None.
# Register a stub so @dataclass(frozen=True) resolves correctly.
if __name__ not in sys.modules:
    import types as _types
    _mod_stub = _types.ModuleType(__name__)
    sys.modules[__name__] = _mod_stub


# ---------------------------------------------------------------------------
# Module-level constants
# verbatim-move-from: scripts/check-sub-skill-routing.py lines 83-84
# ---------------------------------------------------------------------------

REPO_ROOT: Path = Path(__file__).resolve().parents[1]
DEFAULT_PLUGIN_DIR: Path = REPO_ROOT / "first-principles"


# ===========================================================================
# SECTION 1: Shared catalog-parsing utilities
# (Bit-for-bit identical in both source scripts — consolidated to one copy)
# ===========================================================================

# ---------------------------------------------------------------------------
# Catalog helpers
# verbatim-move-from: scripts/check-sub-skill-routing.py lines 145-169
# ---------------------------------------------------------------------------


def _strip_quotes(s: str) -> str:
    s = s.strip()
    if len(s) >= 2 and s[0] in ('"', "'") and s[-1] == s[0]:
        return s[1:-1]
    return s


def _split_row(line: str) -> list[str]:
    """Split a Markdown table row on `|`, returning trimmed cells.

    Leading/trailing `|` produce empty cells which we drop.
    """
    parts = [c.strip() for c in line.split("|")]
    if parts and parts[0] == "":
        parts = parts[1:]
    if parts and parts[-1] == "":
        parts = parts[:-1]
    return parts


def _is_separator_row(cells: list[str]) -> bool:
    """A separator row in a Markdown table is all dashes (with optional colons)."""
    if not cells:
        return False
    return all(re.fullmatch(r":?-{3,}:?", c) is not None for c in cells)


# ---------------------------------------------------------------------------
# Structured walker
# verbatim-move-from: scripts/check-sub-skill-routing.py lines 247-255
# ---------------------------------------------------------------------------


def _walk(obj: object) -> Iterable[object]:
    """Yield every node in a nested JSON-like structure (dicts/lists/scalars)."""
    yield obj
    if isinstance(obj, dict):
        for v in obj.values():
            yield from _walk(v)
    elif isinstance(obj, list):
        for v in obj:
            yield from _walk(v)


# ---------------------------------------------------------------------------
# Runtime utilities
# verbatim-move-from: scripts/check-sub-skill-routing.py lines 424-435
# ---------------------------------------------------------------------------


def _ensure_claude_available() -> None:
    if shutil.which("claude") is None:
        print(
            "error: `claude` CLI not found on PATH; cannot run the sub-skill routing battery",
            file=sys.stderr,
        )
        sys.exit(2)


def _print(msg: str, quiet: bool) -> None:
    if not quiet:
        print(msg, flush=True)


# ---------------------------------------------------------------------------
# Plan-36-locked transport
# verbatim-move-from: scripts/check-sub-skill-routing.py lines 367-397
# ---------------------------------------------------------------------------


def _run_prompt_to(prompt: "BoundaryPrompt | FocusedPrompt | MergedPrompt", plugin_dir: Path, out_path: Path) -> Path:
    """Issue one prompt via `claude -p` and capture the stream-json log to out_path.

    Transport per D-10 (verbatim, copied from check-routing.py lines 329-341):
        claude -p --plugin-dir <path> --no-session-persistence \
          --output-format stream-json --verbose \
          --permission-mode bypassPermissions <prompt>

    Returns out_path (combined stdout + stderr written there).
    """
    # Plan-36-locked — do not modify this argv list
    argv = [
        "claude",
        "-p",
        "--plugin-dir",
        str(plugin_dir),
        "--no-session-persistence",
        "--output-format",
        "stream-json",
        "--verbose",
        "--permission-mode",
        "bypassPermissions",
        prompt.text,
    ]
    proc = subprocess.run(
        argv,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
    )
    out_path.write_bytes(proc.stdout or b"")
    return out_path


# new in Phase 67 (CR-1): path-returning transport so both detectors score the same .jsonl
def _run_prompt_n_times_to_paths(
    prompt: "MergedPrompt", plugin_dir: Path, out_dir: Path, repeat: int
) -> list[Path]:
    """Run a single prompt N times and return the list of written JSONL paths.

    When repeat == 1, writes to <id>.jsonl.
    When repeat > 1, writes to <id>-run<n>.jsonl (1-indexed).

    This is the only intentional behavioral delta from verbatim-move: the
    original _run_prompt_n_times functions returned list[SubSkill] or
    list[OutputStructure]. This variant returns list[Path] so both detectors
    can independently score the same captured .jsonl files.
    """
    paths: list[Path] = []
    for run_idx in range(repeat):
        if repeat == 1:
            out_path = out_dir / f"{prompt.id}.jsonl"
        else:
            out_path = out_dir / f"{prompt.id}-run{run_idx + 1}.jsonl"
        paths.append(_run_prompt_to(prompt, plugin_dir, out_path))
    return paths


# verbatim-move-from: scripts/check-sub-skill-routing.py lines 970-987 (extracted to helper)
def _validate_kn(args: argparse.Namespace) -> int | None:
    """Validate --repeat / --min-pass K>N constraint. Returns exit code or None."""
    if args.repeat < 1:
        print("error: --repeat must be >= 1", file=sys.stderr)
        return 2
    if args.repeat == 1:
        if args.min_pass != 1:
            print(
                f"warning: --repeat 1 forces --min-pass to 1 "
                f"(supplied {args.min_pass} ignored)",
                file=sys.stderr,
            )
        args.min_pass = 1
    elif args.min_pass < 1 or args.min_pass > args.repeat:
        print(
            f"error: --min-pass ({args.min_pass}) must be >= 1 and "
            f"<= --repeat ({args.repeat})",
            file=sys.stderr,
        )
        return 2
    return None


# ===========================================================================
# SECTION 2: Boundary detector — Signal A v2.1
# verbatim-move-from: scripts/check-sub-skill-routing.py (multiple regions)
# ===========================================================================

# ---------------------------------------------------------------------------
# Boundary-detector constants
# verbatim-move-from: scripts/check-sub-skill-routing.py lines 86-88
# ---------------------------------------------------------------------------

SubSkill = Literal["pre-mortem", "inversion", "both", "none-or-other"]

_VALID_SUBSKILLS: set[str] = {"pre-mortem", "inversion", "both", "none-or-other"}


# ---------------------------------------------------------------------------
# Detection regex — Signal A v2 (sub-skill invocation at orchestrator boundary).
#
# What this measures and why it changed (v1 → v2, see Plan 45-04):
#
# v1 design (Plan 45-01) assumed Signal A could detect Reads of
# `agents/references/<name>.md` from the outer `claude -p` stream-json. Wave 0
# calibration on 2026-05-28 (artefacts in
# /tmp/check-sub-skill-routing-calib-20260528T133944Z/) proved this assumption
# wrong: when the orchestrator invokes the `first-principles:first-principles`
# composer Agent, that subagent's Reads of `pre-mortem.md` / `inversion.md`
# happen inside the subagent's nested stream and never appear in the outer
# capture. Signal A always returned empty; the v1 Signal B text-marker fallback
# then misclassified composer-only runs as `inversion` because the composer
# emits all six techniques' procedure text verbatim.
#
# v2 design (Plan 45-04): measure the OBSERVABLE signal at the orchestrator
# boundary — a `Skill` or `Agent` (or `Task`) tool_use that explicitly names a
# specific sub-skill (`first-principles:pre-mortem` or `first-principles:inversion`).
# This mirrors the parent verifier (`check-routing.py:_signal_a`) which also
# inspects tool_use envelopes rather than nested subagent behaviour. The
# absence of a sub-skill invocation IS the FU-21 regression: the current
# shipped descriptions route to the composer, never naming a sub-skill;
# Phase 46's description fixes will make `Skill: first-principles:pre-mortem`
# appear in the stream for prompts like P12.
# ---------------------------------------------------------------------------

# verbatim-move-from: scripts/check-sub-skill-routing.py lines 118-121
SUBSKILL_INVOCATION_RE: dict[str, re.Pattern[str]] = {
    "pre-mortem": re.compile(r"first-principles:pre-mortem\b", re.IGNORECASE),
    "inversion": re.compile(r"first-principles:inversion\b", re.IGNORECASE),
}


# ---------------------------------------------------------------------------
# BoundaryPrompt dataclass (renamed from Prompt — CR-3)
# verbatim-move-from: scripts/check-sub-skill-routing.py lines 129-135
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class BoundaryPrompt:
    """One row from the sub-skill routing catalog."""

    id: str
    text: str
    expected: SubSkill


# ---------------------------------------------------------------------------
# Boundary catalog parser (renamed from parse_catalog — CR-2)
# verbatim-move-from: scripts/check-sub-skill-routing.py lines 172-238
# ---------------------------------------------------------------------------


def parse_boundary_catalog(path: Path) -> tuple[list[BoundaryPrompt], list[BoundaryPrompt]]:
    """Parse a sub-skill-routing-catalog.md-shaped Markdown catalog.

    Returns (positives, negatives). Rows are classified by the prefix of
    the id cell: `P*` -> positive, `N*` -> negative. Other ids are ignored.

    Raises FileNotFoundError if path missing, ValueError on parse error
    or empty result.
    """
    if not path.exists():
        raise FileNotFoundError(f"catalog not found: {path}")

    positives: list[BoundaryPrompt] = []
    negatives: list[BoundaryPrompt] = []

    in_table = False
    expecting_separator = False

    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.rstrip()
        if not line.startswith("|"):
            in_table = False
            expecting_separator = False
            continue

        cells = _split_row(line)
        if not cells:
            in_table = False
            continue

        if not in_table:
            if len(cells) >= 3 and cells[1].strip().lower() == "prompt":
                in_table = True
                expecting_separator = True
                continue
            continue

        if expecting_separator:
            expecting_separator = False
            if _is_separator_row(cells):
                continue

        if len(cells) < 3:
            continue
        rid = cells[0].strip()
        prompt_text = _strip_quotes(cells[1])
        expected_raw = cells[2].strip()

        if not rid or rid[0] not in ("P", "N"):
            continue

        expected_lc = expected_raw.lower()
        if expected_lc not in _VALID_SUBSKILLS:
            raise ValueError(
                f"row {rid!r}: expected sub-skill must be one of "
                f"{sorted(_VALID_SUBSKILLS)}, got {expected_raw!r}"
            )

        prompt = BoundaryPrompt(id=rid, text=prompt_text, expected=expected_lc)  # type: ignore[arg-type]
        if rid.startswith("P"):
            positives.append(prompt)
        else:
            negatives.append(prompt)

    if not positives and not negatives:
        raise ValueError(f"catalog {path} contained no P* or N* rows")
    return positives, negatives


# ---------------------------------------------------------------------------
# Boundary detector constants
# verbatim-move-from: scripts/check-sub-skill-routing.py lines 258-264
# ---------------------------------------------------------------------------

_SUBSKILL_TOOL_NAMES: set[str] = {"Skill", "Agent", "Task"}


# Routing-field keys: the input-dict keys that name the invocation target.
# Other input keys (`prompt`, `args`, `description`) carry user-facing text
# that can mention sub-skill names without invoking them — must NOT count.
_ROUTING_FIELDS: tuple[str, ...] = ("skill", "subagent_type")


# ---------------------------------------------------------------------------
# _boundary_signal_a (renamed from _signal_a — CR-5/Pitfall 3)
# verbatim-move-from: scripts/check-sub-skill-routing.py lines 267-315
# ---------------------------------------------------------------------------


def _boundary_signal_a(parsed_lines: list[object], raw_text: str) -> set[str]:
    """Signal A v2.1: which sub-skills were invoked at the orchestrator boundary.

    Structured walk, routing-field scoped: for every dict whose `name` is
    in _SUBSKILL_TOOL_NAMES (Skill, Agent, Task), inspect ONLY the routing
    fields of its `input` dict (`skill`, `subagent_type`) against each
    SUBSKILL_INVOCATION_RE entry.

    Why scoped:
    - Raw-text regex fallback over the whole stream catches sub-skill names
      that appear inside Read tool_result content when the agent Reads
      in-repo files (this script's source, plan files). Removed in v2.1.
    - Stringifying the full `input` dict catches sub-skill names that
      appear inside the user-facing `prompt` / `args` / `description`
      fields when the orchestrator enriches a vague prompt with project
      context that quotes the verifier's own design. Plan 45-03 baseline
      run on 2026-05-28 P12-run4 showed this: the orchestrator sent the
      composer subagent a prompt that quoted `first-principles:pre-mortem`
      and `first-principles:inversion` verbatim as background context, and
      Signal A v2.0 matched both in the stringified input dict despite the
      actual `subagent_type` being `first-principles:first-principles`
      (the composer). v2.1 inspects only routing fields to avoid this.

    Trade-off: we lose the parser-drift recovery the fallback provided. If
    a stream-json line ever fails to parse but contains a real sub-skill
    invocation, we will miss it. Currently judged an acceptable loss: the
    Plan 36-locked transport produces well-formed stream-json reliably, and
    a false-negative on a true invocation is preferable to a false-positive
    on quoted prompt-text. `raw_text` is retained as a parameter for
    signature stability and future tightening (e.g. scoped to lines that
    failed JSON parse).
    """
    del raw_text  # see docstring — fallback intentionally removed in v2.1
    fired: set[str] = set()
    for parsed in parsed_lines:
        for node in _walk(parsed):
            if isinstance(node, dict) and node.get("name") in _SUBSKILL_TOOL_NAMES:
                inp = node.get("input", {})
                if not isinstance(inp, dict):
                    continue
                # Extract only the routing fields. Concat their string values
                # so a single regex search covers both fields.
                routing_text = " ".join(
                    str(inp.get(field, "")) for field in _ROUTING_FIELDS
                )
                for name, rx in SUBSKILL_INVOCATION_RE.items():
                    if rx.search(routing_text):
                        fired.add(name)
    return fired


# ---------------------------------------------------------------------------
# detect_subskill
# verbatim-move-from: scripts/check-sub-skill-routing.py lines 318-357
# ---------------------------------------------------------------------------


def detect_subskill(jsonl_path: Path) -> SubSkill:
    """Score a captured stream-json event log into one of the 4 SubSkill values.

    v2 design: single-signal detection (see SUBSKILL_INVOCATION_RE block above
    for the v1→v2 rationale). Signal B was removed because the composer
    `first-principles:first-principles` Agent emits all six companion
    techniques' procedure text verbatim, causing text-marker-based detection
    to spuriously fire `pre-mortem` AND `inversion` on every composer-only run.

    Resolution:
        fired = _boundary_signal_a(parsed_lines, raw_text)
        |fired| == 0  → "none-or-other"   (no specific sub-skill named —
                                           composer-only routing or no
                                           first-principles invocation at all;
                                           this IS the FU-21 regression signal)
        |fired| == 1  → the single name
        |fired| == 2  → "both"
    """
    raw_text = jsonl_path.read_text(encoding="utf-8", errors="replace")
    parsed_lines: list[object] = []
    for line in raw_text.splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            parsed_lines.append(json.loads(line))
        except json.JSONDecodeError:
            continue

    fired = _boundary_signal_a(parsed_lines, raw_text)
    if not fired:
        return "none-or-other"
    if len(fired) == 1:
        name = next(iter(fired))
        # Defensive: only accept the two known sub-skill names.
        if name in ("pre-mortem", "inversion"):
            return name  # type: ignore[return-value]
        return "none-or-other"
    return "both"


# ---------------------------------------------------------------------------
# _is_match lenient rule
# verbatim-move-from: scripts/check-sub-skill-routing.py lines 438-450
# ---------------------------------------------------------------------------


def _is_match(actual: SubSkill, expected: SubSkill) -> bool:
    """Lenient match rule (RESEARCH §Open Question 2):

    actual == expected always matches. Additionally, when the agent loads
    BOTH reference files and the prompt expected exactly one of the two
    sub-skills, count it as a match — the correct sub-skill *was* loaded;
    the extra sibling load is over-eager but not a regression.
    """
    if actual == expected:
        return True
    if actual == "both" and expected in ("pre-mortem", "inversion"):
        return True
    return False


# ---------------------------------------------------------------------------
# Boundary self-test fixtures
# verbatim-move-from: scripts/check-sub-skill-routing.py lines 578-798
# ---------------------------------------------------------------------------

# v2 fixtures (Plan 45-04): exercise Signal A invocation detection at the
# orchestrator boundary. See SUBSKILL_INVOCATION_RE block for the v1→v2
# rationale (subagent-side Reads are invisible to the outer stream-json).

# Fixture (a): pre-mortem via Skill tool_use naming the sub-skill
_FIXTURE_PREMORTEM_VIA_SKILL = "\n".join(
    [
        json.dumps(
            {
                "type": "tool_use",
                "name": "Skill",
                "input": {"skill": "first-principles:pre-mortem", "args": "stress-test the plan"},
            }
        ),
        json.dumps({"type": "assistant", "text": "Loaded the pre-mortem sub-skill."}),
    ]
)

# Fixture (b): inversion via Agent tool_use naming the sub-skill
_FIXTURE_INVERSION_VIA_AGENT = "\n".join(
    [
        json.dumps(
            {
                "type": "tool_use",
                "name": "Agent",
                "input": {
                    "subagent_type": "first-principles:inversion",
                    "description": "Inversion analysis",
                    "prompt": "Invert the claim and enumerate failure-guaranteeing conditions.",
                },
            }
        ),
        json.dumps({"type": "assistant", "text": "Delegating to the inversion sub-skill."}),
    ]
)

# Fixture (c): pre-mortem via Task tool_use whose stringified input mentions
# the sub-skill (parser-drift / nested-wrap case).
_FIXTURE_PREMORTEM_VIA_TASK = "\n".join(
    [
        json.dumps(
            {
                "type": "tool_use",
                "name": "Task",
                "input": {
                    "subagent_type": "first-principles:pre-mortem",
                    "prompt": "Run a structured pre-mortem on this plan.",
                },
            }
        ),
        json.dumps({"type": "assistant", "text": "Task dispatched."}),
    ]
)

# Fixture (d): both — Skill invocation for pre-mortem AND Agent invocation
# for inversion in the same stream.
_FIXTURE_BOTH = "\n".join(
    [
        json.dumps(
            {
                "type": "tool_use",
                "name": "Skill",
                "input": {"skill": "first-principles:pre-mortem", "args": "..."},
            }
        ),
        json.dumps({"type": "assistant", "text": "Pre-mortem first."}),
        json.dumps(
            {
                "type": "tool_use",
                "name": "Agent",
                "input": {"subagent_type": "first-principles:inversion", "prompt": "..."},
            }
        ),
        json.dumps({"type": "assistant", "text": "Then inversion."}),
    ]
)

# Fixture (e): none-or-other — empty / generic stream with no
# first-principles invocation at all.
_FIXTURE_NONE = "\n".join(
    [
        json.dumps({"type": "assistant", "text": "Hello world. Here is a generic answer."}),
        json.dumps({"type": "assistant", "text": "Nothing distinctive in this text at all."}),
    ]
)

# Fixture (f) — LOAD-BEARING: composer-only stream. The orchestrator invokes
# the `first-principles:first-principles` composer Skill+Agent, NOT a specific
# sub-skill. The composer's response text will mention pre-mortem AND
# inversion (it runs all six techniques), but Signal A v2 only counts explicit
# sub-skill names. Expected: none-or-other.
#
# This fixture encodes exactly what /tmp/check-sub-skill-routing-calib-20260528T133944Z/
# P-CAL1-run3.jsonl showed against current shipped descriptions. The v1
# verifier misclassified that run as `inversion` via Signal B text markers;
# v2 must correctly classify it as `none-or-other`.
_FIXTURE_COMPOSER_ONLY = "\n".join(
    [
        json.dumps(
            {
                "type": "tool_use",
                "name": "Skill",
                "input": {"skill": "first-principles:first-principles", "args": "..."},
            }
        ),
        json.dumps(
            {
                "type": "tool_use",
                "name": "Agent",
                "input": {
                    "subagent_type": "first-principles:first-principles",
                    "description": "Composer agent",
                    "prompt": "Apply all six techniques.",
                },
            }
        ),
        json.dumps(
            {
                "type": "user",
                "message": {
                    "role": "user",
                    "content": [
                        {
                            "type": "tool_result",
                            "content": (
                                "Pre-mortem analysis: working backward from failure. "
                                "Invert, always invert. Failure-guaranteeing conditions. "
                                "Prospective-hindsight framing. Inversion of the claim."
                            ),
                        }
                    ],
                },
            }
        ),
    ]
)

# Fixture (g) — LOAD-BEARING NEGATIVE: Read tool_result contains a verbatim
# `first-principles:pre-mortem` / `:inversion` mention (e.g. when the agent
# Reads this script's own source, a plan file, or any of the agent reference
# markdown). The verifier must NOT classify this as `both` or any specific
# sub-skill. The Plan 45-03 baseline (2026-05-28) showed this false-positive
# pattern on N1 and P12; the raw-text fallback was removed in response. This
# fixture encodes the regression test.
# Fixture (h) — LOAD-BEARING NEGATIVE: composer invocation whose prompt/args
# text quotes the sub-skill names verbatim (e.g. orchestrator enriches a vague
# user prompt with project context that mentions `first-principles:pre-mortem`
# and `first-principles:inversion` as background). The verifier must NOT
# classify this as `both` — only the routing fields (`skill`,
# `subagent_type`) count. Plan 45-03 P12-run4 (2026-05-28) showed this on
# the live baseline; Signal A v2.1 (routing-field scoped) fixes it.
_FIXTURE_COMPOSER_WITH_QUOTED_SUBSKILLS = "\n".join(
    [
        json.dumps(
            {
                "type": "tool_use",
                "name": "Skill",
                "input": {
                    "skill": "first-principles:first-principles",
                    "args": (
                        "Run a pre-mortem. Background: Plan 45-04 distinguishes "
                        "first-principles:pre-mortem from first-principles:inversion "
                        "and the verifier must catch composer routing."
                    ),
                },
            }
        ),
        json.dumps(
            {
                "type": "tool_use",
                "name": "Agent",
                "input": {
                    "subagent_type": "first-principles:first-principles",
                    "description": "Composer for pre-mortem analysis",
                    "prompt": (
                        "Apply first-principles methodology. Phase 45 fixture "
                        "covers P12 (expected first-principles:pre-mortem) and "
                        "P24 (expected first-principles:inversion)."
                    ),
                },
            }
        ),
    ]
)

_FIXTURE_READ_RESULT_CONTAMINATION = "\n".join(
    [
        json.dumps(
            {
                "type": "assistant",
                "message": {
                    "content": [
                        {
                            "type": "tool_use",
                            "name": "Read",
                            "input": {"file_path": "scripts/check-sub-skill-routing.py"},
                        }
                    ],
                },
            }
        ),
        json.dumps(
            {
                "type": "user",
                "message": {
                    "role": "user",
                    "content": [
                        {
                            "type": "tool_result",
                            "content": (
                                "SUBSKILL_INVOCATION_RE pre-mortem matches "
                                "first-principles:pre-mortem and inversion matches "
                                "first-principles:inversion (script source)"
                            ),
                        }
                    ],
                },
            }
        ),
    ]
)


# ---------------------------------------------------------------------------
# Boundary self-test runner (renamed from self_test — CR-4/Pitfall 5)
# verbatim-move-from: scripts/check-sub-skill-routing.py lines 801-868
# (K>N rejection sub-test removed — main() not in this module; see merged
# battery's own self_test() for that sub-test)
# ---------------------------------------------------------------------------


def _run_one_fixture_boundary(name: str, body: str, expected: SubSkill) -> bool:
    with tempfile.NamedTemporaryFile(
        mode="w", suffix=".jsonl", delete=False, encoding="utf-8"
    ) as tmp:
        tmp.write(body)
        tmp_path = Path(tmp.name)
    try:
        actual = detect_subskill(tmp_path)
        if actual != expected:
            print(
                f"self-test FAIL: fixture {name!r} expected {expected}, got {actual}",
                file=sys.stderr,
            )
            return False
        return True
    finally:
        try:
            tmp_path.unlink()
        except OSError:
            pass


def self_test_boundary() -> int:
    """Validate boundary detection logic against in-module fixtures. No claude invocation.

    Runs 8 fixtures. The K>N rejection sub-test (which calls main()) is NOT
    included here — it lives in the merged battery's own self_test() which
    can call check-routing-battery.py's main() directly.
    """
    fixtures: list[tuple[str, str, SubSkill]] = [
        ("pre-mortem_via_skill", _FIXTURE_PREMORTEM_VIA_SKILL, "pre-mortem"),
        ("inversion_via_agent", _FIXTURE_INVERSION_VIA_AGENT, "inversion"),
        ("pre-mortem_via_task", _FIXTURE_PREMORTEM_VIA_TASK, "pre-mortem"),
        ("both", _FIXTURE_BOTH, "both"),
        ("none-or-other", _FIXTURE_NONE, "none-or-other"),
        ("composer_only_LOAD_BEARING", _FIXTURE_COMPOSER_ONLY, "none-or-other"),
        ("read_result_contamination_LOAD_BEARING", _FIXTURE_READ_RESULT_CONTAMINATION, "none-or-other"),
        ("composer_with_quoted_subskills_LOAD_BEARING", _FIXTURE_COMPOSER_WITH_QUOTED_SUBSKILLS, "none-or-other"),
    ]
    all_passed = True
    for name, body, expected in fixtures:
        if not _run_one_fixture_boundary(name, body, expected):
            all_passed = False

    if all_passed:
        print(f"self-test PASS (8 fixtures)")
        return 0
    return 1


# ===========================================================================
# SECTION 3: Focused-output classifier
# verbatim-move-from: scripts/check-focused-output.py (multiple regions)
# ===========================================================================

# ---------------------------------------------------------------------------
# Output-structure type + constants
# verbatim-move-from: scripts/check-focused-output.py lines 144-196
# ---------------------------------------------------------------------------

# Valid output-structure classifications.
OutputStructure = Literal[
    "focused-pre-mortem",
    "focused-inversion",
    "focused-fishbone",
    "focused-five-whys",
    "focused-trade-off",
    "focused-second-order",
    "ambiguous",
    "full-composer",
    "none",
]

# Six canonical companion technique keys (must match the file basenames
# under first-principles/agents/references/<key>.md).
_TECHNIQUE_KEYS: tuple[str, ...] = (
    "pre-mortem",
    "inversion",
    "fishbone",
    "five-whys",
    "trade-off",
    "second-order",
)

# Frozenset of the six focused-technique verdict strings, built from
# _TECHNIQUE_KEYS. Used by the semantic comparator below.
_FOCUSED_PREFIXES: frozenset[str] = frozenset(
    f"focused-{tech}" for tech in _TECHNIQUE_KEYS
)


def _verdict_matches(actual: OutputStructure, expected: str) -> bool:
    """Semantic comparator: handles NOT-any-focused as 'not in focused set'.

    When expected == "NOT-any-focused", returns True if actual is NOT one of
    the six focused-<technique> verdicts (i.e. none/ambiguous/full-composer
    all match). Otherwise falls back to exact string equality.
    """
    if expected == "NOT-any-focused":
        return actual not in _FOCUSED_PREFIXES
    return actual == expected


# Noise-tolerance floor. A technique "fires" only if >= MIN_HEADER_HITS
# DISTINCT marker patterns each match the assistant text (distinct-pattern
# counting in `_technique_hits` — 66 review WR-01); the composer-structure
# signal fires at >= MIN_HEADER_HITS total scaffold-marker hits. Mirrors
# the Phase 45 `MIN_TEXT_HITS = 2` precedent (see
# check-sub-skill-routing.py v2.1 history). A single incidental mention
# of e.g. "trade-off" inside an unrelated discussion — or one generic
# phrase repeated — should NOT fire the trade-off technique.
MIN_HEADER_HITS: int = 2

# Composer-structure hit ceiling for the classify() n==1 early-return (CR-02 / DET-11).
# When exactly one technique fires (n==1) AND composer_structure_hits reaches this
# ceiling, the n==1 early-return is suppressed and the composer-structure override
# fires instead — returning `full-composer`.
#
# Justification: there are exactly four _COMPOSER_STRUCTURE_PATTERNS (Ground Truths,
# Assumption Audit, Derivation Chains, Verdict). A focused-with-methodology output
# (e.g. focused trade-off with ## Ground Truths + ## Derivation Chains) fires <= 3
# composer hits because _composer_structure_hits uses findall (total occurrences),
# and the generic word "verdict" may appear in technique prose (e.g. "flips the
# verdict"). A genuine full-composer synthesis that includes all four canonical
# scaffold sections (each appearing as a heading) fires 4-5 composer hits.
# CEILING=4 is the correct value that:
#   - PRESERVES _FIXTURE_FOCUSED_TRADEOFF_WITH_METHODOLOGY (composer_hits=3 < 4):
#     n==1 early-return still fires → focused-trade-off (correct). The fixture
#     has 3 hits because "verdict" appears in the prose ("flips the verdict"),
#     not from a ## Verdict heading; the ceiling must be above 3 to be safe.
#   - CLOSES CR-02 for _FIXTURE_FULLCOMPOSER_SINGLE_TECHNIQUE (composer_hits=5 >= 4):
#     n==1 early-return suppressed → composer override fires → full-composer (correct).
#   - classify({'pre-mortem'}, 4) → 4 >= CEILING=4 → suppressed → full-composer (correct).
_COMPOSER_FOCUS_CEILING: int = 4


# ---------------------------------------------------------------------------
# Technique marker tables
# verbatim-move-from: scripts/check-focused-output.py lines 228-322
# ---------------------------------------------------------------------------

# ---------------------------------------------------------------------------
# Detection layer — what this measures and why
#
# Markers verbatim from 46-RESEARCH §1 Q4.1-Q4.6 (each subsection lists
# the per-technique phrase set with provenance citations into the agent
# reference files at first-principles/agents/references/<technique>.md).
#
# Pitfall 1 mitigation (cardinality classifier prevents v1-style false
# positives): a single technique's markers firing does NOT classify the
# output as `focused-<technique>` unless ZERO other techniques fire and
# ZERO composer-structure markers fire. The structural-signal path is
# the load-bearing observable empirically demonstrated by 46-01 Probe 3
# capture (see top-of-file calibration block).
#
# Pitfall 4 mitigation (MIN_HEADER_HITS=2 floor): each technique requires
# >= 2 DISTINCT marker patterns to match, mirroring Phase 45
# MIN_TEXT_HITS=2. Distinct-pattern counting (66 review WR-01) means two
# repeats of a single generic phrase cannot fire a technique on their own.
#
# Trade-off bare-token tiebreaker: the bare token `trade-off` (without
# the procedural-marker phrases) is too lexically common to count toward
# MIN_HEADER_HITS. It is detected separately as a tiebreaker signal only
# (currently unused beyond documentation — preserved for future tuning).
# ---------------------------------------------------------------------------


# Per-technique marker regex sets — verbatim from 46-RESEARCH §Q4.1-Q4.6.
# Case-insensitive matching is applied uniformly. Each entry cites its
# source file + approximate line (pre-Phase-43 lines may have shifted by
# +/-1 after the Phase 43 edits; the phrases themselves are stable).
_TECHNIQUE_CATEGORIES: dict[str, tuple[re.Pattern[str], ...]] = {
    "pre-mortem": (
        # pre-mortem.md line 3 (frontmatter blurb) + line 36 (Phase 2 framing)
        re.compile(r"prospective[- ]?hindsight", re.IGNORECASE),
        # pre-mortem.md "the plan has (already) failed. What caused it?"
        # Covers natural variation: "has already failed", "already failed",
        # and the bounded "treat <up to 4 words> as (already) failed" form
        # ("treat it as already failed"). The treat branch is bounded to at
        # most 4 intervening words so it cannot greedily match across
        # unrelated clauses on the same line ("we treat retries gracefully
        # and mark the job as failed" must NOT fire) — 66 review WR-01.
        re.compile(
            r"(already|has already)\s+failed"
            r"|treat(?:ing)?\s+(?:\w+\s+){0,4}as\s+(?:already\s+)?failed",
            re.IGNORECASE,
        ),
        # Additional variant: bare "has failed" without "already" qualifier.
        # Real focused pre-mortem output ("the migration has failed",
        # "the rollout has failed") consistently uses this form. The phrase
        # is generic on its own — `_technique_hits` counts DISTINCT patterns
        # matched (66 review WR-01), so this pattern can never fire
        # pre-mortem by itself: a second, different marker (e.g. "working
        # backward") must also match. Observed in 100% of P25/P26 runs in
        # the 66-03 probe capture (2026-06-10).
        re.compile(r"\bhas\s+failed\b", re.IGNORECASE),
        # pre-mortem.md procedure step — loosened from "working backward: what
        # caused" to bare "working backward" to match natural output variation
        # ("Working backward from the wreckage", "Working backward from this
        # failure", etc.) observed in 66-03 Signal B probe (2026-06-10).
        re.compile(r"working backward(s)?\b", re.IGNORECASE),
        # Note: `failure-guaranteeing` is intentionally NOT included here —
        # Q4.1 collision note flags it as overlapping with inversion. The
        # disambiguation lives in inversion's marker set, not pre-mortem's.
        # v5.1 capture-backed: S-P01-run1/2/3/4/5 orchestrator assistant text all
        # include a section header of the form "## Pre-Mortem:", "# First-Principles
        # Pre-Mortem:", or "## Focused Pre-mortem Mode" — the technique name in a
        # Markdown heading is the most reliable cross-run observable in the
        # orchestrator synthesis layer (the detector reads _extract_assistant_text,
        # which captures only type=assistant events). Verified to FIRE in extracted
        # assistant text for S-P01-run1,2,3,4,5.
        # Source: .planning/v5.2-inputs/rr75-evidence/S-P01-run1.jsonl through
        # S-P01-run5.jsonl (Q1/Q2 verify-first, 2026-06-13).
        # False-positive guard (WR-01 corrected): `#\s*` matches one or more `#`
        # then optional whitespace, so the pattern matches ANY Markdown heading level
        # including `### Pre-mortem` subsections that a full-composer synthesis can
        # legitimately emit. The actual false-positive guard is:
        #   (a) _COMPOSER_FOCUS_CEILING bound in classify(): when a full-composer
        #       synthesis fires both this header pattern and a second pre-mortem
        #       marker (n==1) but also reaches composer_structure_hits >= 4,
        #       the n==1 early-return is suppressed and the composer override wins
        #       → full-composer (CR-02 closed).
        #   (b) MIN_HEADER_HITS=2: a second distinct pre-mortem marker must also fire;
        #       the header pattern alone cannot fire the technique.
        re.compile(r"#\s*(focused\s+)?pre[-\s]?mortem\b", re.IGNORECASE),
        # v5.1 capture-backed: S-P01-run1 orchestrator assistant text includes
        # "### Failure Causes" (echoed section header from the sub-agent's output);
        # run4 uses "Failure Causes" framing in the synthesis summary. Combined with
        # the section-header pattern above, this provides the second distinct hit for
        # runs 1, 3, and 4. SW-N structural-weakness enumeration (run5) is also
        # present but covered by the header pattern alone on run5.
        # Source: .planning/v5.2-inputs/rr75-evidence/S-P01-run1.jsonl,
        # S-P01-run3.jsonl, S-P01-run4.jsonl (Q1/Q2 verify-first, 2026-06-13).
        # False-positive guard: "failure causes" is engineering prose but rarely
        # co-occurs with a "## Pre-Mortem" section header in the same output.
        # MIN_HEADER_HITS=2 ensures one alone cannot fire pre-mortem.
        re.compile(r"\bfailure\s+causes?\b", re.IGNORECASE),
    ),
    "inversion": (
        # inversion.md frontmatter / opening — "Invert, always invert"
        re.compile(r"invert,?\s+always invert", re.IGNORECASE),
        # inversion.md lines 52-53 — "failure-guaranteeing conditions"
        re.compile(r"failure[- ]?guaranteeing condition", re.IGNORECASE),
        # inversion.md lines 25, 56, 60 — "necessary precondition"
        re.compile(r"necessary precondition", re.IGNORECASE),
        # inversion.md lines 46, 49, 96 — "inverted form"
        re.compile(r"inverted form", re.IGNORECASE),
        # v5.0 capture-backed: S-P02-run1 emitted "## Claim, inverted" header;
        # S-P02-run2/3/4 emitted "## Inverted claim" header. Neither phrase
        # appears in any S-N capture tested. Source: /tmp/step0-baseline-20260612T133945Z/
        # S-P02-run1..5.jsonl (evidence copy: .planning/phases/74-fixture-context-detector-markers-and-offline-gates/evidence/).
        # False-positive guard: "claim, inverted" is idiomatic to formal inversion
        # analysis; it does not appear in general analytical prose (verified against
        # S-N01/N02/N03/N04 run1 captures, all clean). MIN_HEADER_HITS=2 means a
        # second distinct marker must also fire — one alone cannot fire inversion.
        re.compile(r"\bclaim[,.]?\s+inverted\b", re.IGNORECASE),
        # v5.0 capture-backed: S-P02-run2 "## Inverted claim", run3 "## Inverted claim",
        # run4 "**Inverted claim:**". Clean in S-N captures. Same provenance as above.
        re.compile(r"\binverted\s+claim\b", re.IGNORECASE),
    ),
    "fishbone": (
        # fishbone.md procedure section — "cause categories"
        re.compile(r"cause categor(y|ies)", re.IGNORECASE),
        # fishbone.md — "breadth-first" enumeration phrasing
        re.compile(r"breadth[- ]?first", re.IGNORECASE),
        # fishbone.md presets — 6M / 8P / 4S categorization presets
        re.compile(r"\b(6M|8P|4S)\s+(preset|categor)", re.IGNORECASE),
        # fishbone.md — "sub-causes" enumeration
        re.compile(r"sub[- ]?causes?", re.IGNORECASE),
        # fishbone.md name itself — "fishbone" or "Ishikawa"
        re.compile(r"fishbone|ishikawa", re.IGNORECASE),
        # v5.0 capture-backed: S-P03-run2 produced a real fishbone diagram with
        # category table "People, Process, Technology & Tools, Environment,
        # Information, Resources". The existing `fishbone|ishikawa` fires once
        # (=1 distinct); this marker supplies the second distinct hit.
        # Source: /tmp/step0-baseline-20260612T133945Z/S-P03-run2.jsonl
        # (evidence copy: .planning/phases/74-fixture-context-detector-markers-and-offline-gates/evidence/).
        # False-positive guard: the 3-word "People, Process, Technology" sequence
        # identifies the 6M software fishbone category preset; not present in
        # general prose. If it appears in full-composer output, the composer-
        # structure override fires first (>=2 scaffold tokens from Ground Truths /
        # Assumption Audit / Verdict), correctly labeling the run full-composer.
        re.compile(r"\bPeople[,;]?\s+(and\s+)?Process[,;]?\s+(Technology|Tools)\b", re.IGNORECASE),
    ),
    "five-whys": (
        # five-whys.md — the canonical drill question
        re.compile(r"why did this happen", re.IGNORECASE),
        # five-whys.md — siblings-check phrasing
        re.compile(r"what else caused this", re.IGNORECASE),
        # five-whys.md procedure step — symptom statement
        re.compile(r"state the symptom", re.IGNORECASE),
        # five-whys.md framing — "depth-first root-cause"
        re.compile(r"depth[- ]?first\s+root[- ]?cause", re.IGNORECASE),
        # five-whys.md name itself — "five-whys" or "5 whys"
        re.compile(r"\b(five[- ]?whys?|5[- ]?whys?)\b", re.IGNORECASE),
        # v5.1 capture-backed: S-P04 orchestrator assistant text on ALL 5 runs
        # contains "causal link", "causal chain", or "causal step" — the orchestrator
        # summarises the Five Whys result using "causal chain" (run2: "causal chain",
        # run4: "causal chain from symptom to root") or "causal link" (run1: "causal
        # link", run3: "causal links"). Combined with the existing `five[- ]?whys?`
        # marker (which fires on all 5 runs' assistant text), this achieves 2 distinct
        # hits on every run, lifting five-whys hits from 1→2.
        # Source: .planning/v5.2-inputs/rr75-evidence/S-P04-run1.jsonl through
        # S-P04-run5.jsonl (Q1/Q2 verify-first, 2026-06-13).
        # False-positive guard: "causal chain/link" is more specific than bare
        # "cause". In the routing battery the Five Whys technique name is required
        # as the SECOND distinct marker; "causal chain" alone cannot fire five-whys.
        # MIN_HEADER_HITS=2 ensures a second distinct pattern (e.g. five[- ]?whys?)
        # must also match before the technique fires.
        re.compile(r"\bcausal\s+(link|step|chain)\b", re.IGNORECASE),
    ),
    "trade-off": (
        # trade-off.md procedure step — "Assign weights. Lock them now."
        re.compile(r"assign weights\.?\s+lock them now", re.IGNORECASE),
        # trade-off.md — "weighted total"
        re.compile(r"weighted total", re.IGNORECASE),
        # trade-off.md — "sensitivity check"
        re.compile(r"sensitivity check", re.IGNORECASE),
        # trade-off.md — "weight × score" or "weight x score"
        re.compile(r"weight\s*[×x]\s*score", re.IGNORECASE),
        # Note: bare `trade-off` token is NOT included — Q4.5 collision
        # note flags it as too lexically common (RFC-style "trade-off"
        # mentions everywhere). Detected separately as a tiebreaker (see
        # `_TRADEOFF_BARE_TOKEN_RE` below) but not counted toward
        # MIN_HEADER_HITS for the trade-off technique.
    ),
    "second-order": (
        # second-order.md — "2nd-order consequence" / "3rd-order consequence"
        re.compile(r"2nd[- ]?order consequence", re.IGNORECASE),
        re.compile(r"3rd[- ]?order consequence", re.IGNORECASE),
        # second-order.md — "undermining contradiction"
        re.compile(r"undermining contradiction", re.IGNORECASE),
        # second-order.md — "stopping rule"
        re.compile(r"stopping rule", re.IGNORECASE),
        # second-order.md framing — "second-level thinking"
        re.compile(r"second[- ]?level thinking", re.IGNORECASE),
        # v5.1 capture-backed: S-P06 orchestrator assistant text on ALL 5 runs
        # contains "second-order" as an adjective ("second-order analysis",
        # "second-order effects", "second-order mode"). The existing markers
        # (2nd-order consequence, 3rd-order consequence, etc.) are specific to
        # procedure-text language that appears only in the sub-agent tool_result,
        # not in the orchestrator synthesis. This broader pattern matches the
        # orchestrator summary form.
        # Source: .planning/v5.2-inputs/rr75-evidence/S-P06-run1.jsonl through
        # S-P06-run5.jsonl (Q1/Q2 verify-first, 2026-06-13).
        # False-positive guard: "second-order" is a recognisable technical term
        # but requires pairing with a second distinct marker (see next entry).
        # MIN_HEADER_HITS=2 ensures a single "second-order" mention alone does
        # not fire the technique.
        re.compile(r"\bsecond[- ]?order\b", re.IGNORECASE),
        # v5.1 capture-backed (CR-01 de-nested replacement): S-P06 orchestrator assistant
        # text on ALL 5 runs includes a Markdown section heading of the form
        # "## Second-Order Effects", "## Second-order effects", "# Second-Order Effects",
        # or "## Focused Second-Order Mode" (heading-anchored), plus run5 includes
        # "effect chains" in the prose summary. The heading-anchored disjunction here
        # is NOT a lexical subset/superset of pattern A (`\bsecond[- ]?order\b`):
        #   - disjunct-1 (`^#{1,3}\s*(focused\s+)?second[- ]?order\b.*\b(effects?|mode|analysis)\b`)
        #     requires a leading Markdown heading anchor `^#{1,3}`, so it does NOT fire
        #     on bare-prose "second-order effects" (no heading) — closes CR-01.
        #   - disjunct-2 (`\beffect\s+chains?\b`) does not contain the substring
        #     "second-order" at all — completely non-overlapping with pattern A.
        # Together the two patterns supply >= 2 distinct hits on every S-P06 run:
        #   run1/2/3/4/5: disjunct-1 fires on the "## Second-Order Effects:" heading;
        #   run5: both disjuncts fire (heading + "effect chains" in prose).
        # Verify-first firing matrix (2026-06-13): run1=2, run2=2, run3=2, run4=2, run5=2
        #   (all via A + heading-disjunct-1; run5 additionally via disjunct-2).
        # Source: .planning/v5.2-inputs/rr75-evidence/S-P06-run1.jsonl through
        # S-P06-run5.jsonl (Q1/Q2 verify-first, 2026-06-13).
        # False-positive guard: the heading anchor `^#{1,3}` requires a real Markdown
        # heading prefix; bare "second-order effects" in incidental prose matches only
        # pattern A (1 distinct hit), staying below MIN_HEADER_HITS=2 (CR-01 closed).
        # The `_FIXTURE_SECONDORDER_EFFECTS_NEGATIVE` fixture guards this invariant.
        re.compile(
            r"(^#{1,3}\s*(focused\s+)?second[- ]?order\b.*\b(effects?|mode|analysis)\b)"
            r"|(\beffect\s+chains?\b)",
            re.IGNORECASE | re.MULTILINE,
        ),
    ),
}

# Tiebreaker — bare `trade-off` token. Counted separately, NOT toward
# MIN_HEADER_HITS for the trade-off technique. Reserved for future
# tuning of the focused-trade-off vs ambiguous boundary; currently
# present as documentation of the Q4.5 collision-avoidance choice.
# verbatim-move-from: scripts/check-focused-output.py lines 324-330
_TRADEOFF_BARE_TOKEN_RE: re.Pattern[str] = re.compile(
    r"\btrade[- ]?off\b", re.IGNORECASE
)

# Composer-structure markers — the canonical 5-phase scaffold headers
# the composer emits in its output. Per the calibration block at the top
# of this file (OPTION B from 46-01-SUMMARY), if >= MIN_HEADER_HITS of
# these fire, classify as `full-composer` regardless of per-technique
# cardinality. Empirically verified against
# .planning/phases/46-.../wave0-evidence/probe3-full-composer.jsonl
# (5 Phase headers + 2 "Ground Truths" + 1 "Assumption Audit" + 1
# "Verdict" all fired in that real capture).
# verbatim-move-from: scripts/check-focused-output.py lines 332-358
_COMPOSER_STRUCTURE_PATTERNS: tuple[re.Pattern[str], ...] = (
    # History (Bug 1, 66-03 Signal B probe, 2026-06-10): the original first
    # entry here was bare `\bPhase\s+[0-9]+\b`, which fired on plan-content
    # prose ("Phase 1 migrates staging"; "Phase 1/2/3" appearing 19-29
    # times in a multi-phase migration plan), false-classifying P24/P25 as
    # full-composer. It was first tightened to the multi-word header form
    # ("Phase N — Ground Truths" etc.), but that form structurally
    # OVERLAPPED the standalone patterns below — every header match
    # double-counted, so a single header line defeated the
    # MIN_HEADER_HITS=2 noise floor (66 review WR-02). The Phase-header
    # entry is now REMOVED entirely: the distinctive suffix tokens
    # (Ground Truths / Assumption Audit / Derivation Chains / Verdict)
    # are fully counted by the standalone patterns, each occurrence
    # exactly once. Bare "Phase N" prose never fires.
    re.compile(r"\bGround\s+Truths?\b", re.IGNORECASE),
    re.compile(r"\bAssumption\s+Audit\b", re.IGNORECASE),
    re.compile(r"\bDerivation\s+Chains?\b", re.IGNORECASE),
    re.compile(r"\bVerdict\b", re.IGNORECASE),
)


# ---------------------------------------------------------------------------
# FocusedPrompt dataclass (renamed from Prompt — CR-3)
# verbatim-move-from: scripts/check-focused-output.py lines 367-374
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class FocusedPrompt:
    """One row from a routing/output-structure catalog."""

    id: str
    text: str
    expected: str


# ---------------------------------------------------------------------------
# Focused catalog parser (renamed from parse_catalog — CR-2)
# verbatim-move-from: scripts/check-focused-output.py lines 413-478
# ---------------------------------------------------------------------------


def parse_focused_catalog(path: Path) -> tuple[list[FocusedPrompt], list[FocusedPrompt]]:
    """Parse a Markdown routing/output-structure catalog.

    Returns (positives, negatives). Rows are classified by the prefix of
    the id cell: `P*` -> positive, `N*` -> negative. Other ids are ignored.

    Raises FileNotFoundError if path missing, ValueError on empty result.
    Verdict strings are NOT validated against an enum here — 46-04 will
    define the calibrated expectations.
    """
    if not path.exists():
        raise FileNotFoundError(f"catalog not found: {path}")

    positives: list[FocusedPrompt] = []
    negatives: list[FocusedPrompt] = []

    in_table = False
    expecting_separator = False

    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.rstrip()
        if not line.startswith("|"):
            in_table = False
            expecting_separator = False
            continue

        cells = _split_row(line)
        if not cells:
            in_table = False
            continue

        if not in_table:
            if len(cells) >= 3 and cells[1].strip().lower() == "prompt":
                in_table = True
                expecting_separator = True
                continue
            continue

        if expecting_separator:
            expecting_separator = False
            if _is_separator_row(cells):
                continue

        if len(cells) < 3:
            continue
        rid = cells[0].strip()
        prompt_text = _strip_quotes(cells[1])
        expected_raw = cells[2].strip()

        if not rid or rid[0] not in ("P", "N"):
            continue

        if not expected_raw:
            raise ValueError(
                f"row {rid!r}: expected verdict cell must be non-empty"
            )

        prompt = FocusedPrompt(id=rid, text=prompt_text, expected=expected_raw)
        if rid.startswith("P"):
            positives.append(prompt)
        else:
            negatives.append(prompt)

    if not positives and not negatives:
        raise ValueError(f"catalog {path} contained no P* or N* rows")
    return positives, negatives


# ---------------------------------------------------------------------------
# Focused detection layer
# verbatim-move-from: scripts/check-focused-output.py lines 503-604
# ---------------------------------------------------------------------------


def _extract_assistant_text(parsed_lines: list[object]) -> str:
    """Concatenate every assistant-text blob from a parsed stream-json log.

    Pitfall 3 mitigation: walk the parsed structure rather than regexing
    the raw bytes, so we only count markers that appear inside actual
    assistant output — not Read tool_result contents echoing this script's
    own source.

    Recognises both shapes observed in real `claude -p` captures:
      1. `{"type": "assistant", "text": "..."}`            (direct text field)
      2. `{"type": "assistant", "message": {"content": [   (nested message
            {"type": "text", "text": "..."}                  envelope)
         ]}}`
    """
    # IMPORTANT: only inspect TOP-LEVEL parsed entries with type=assistant.
    # Do NOT recurse via _walk(): nested text nodes inside user messages
    # (e.g. when the Skill tool loads a stub body into the conversation as a
    # user-role context block) would otherwise be incorrectly counted as
    # assistant output. Phase 46-04 mini-battery (2026-05-28) surfaced this:
    # _walk yielded the stub body content from inside parsed[8] (a user
    # message with the SKILL.md body) and the defensive fallback for
    # standalone {"type":"text"} blocks then included it, polluting the
    # marker counts with the stub's references to all six techniques.
    text_blobs: list[str] = []
    for parsed in parsed_lines:
        if not isinstance(parsed, dict):
            continue
        if parsed.get("type") != "assistant":
            continue
        # Direct text field (legacy shape).
        direct_text = parsed.get("text")
        if isinstance(direct_text, str):
            text_blobs.append(direct_text)
        # Nested message envelope.
        msg = parsed.get("message")
        if isinstance(msg, dict):
            content = msg.get("content")
            if isinstance(content, list):
                for c in content:
                    if isinstance(c, dict) and c.get("type") == "text":
                        t = c.get("text")
                        if isinstance(t, str):
                            text_blobs.append(t)
    return "\n".join(text_blobs)


def _technique_hits(text: str) -> dict[str, int]:
    """Per-technique count of DISTINCT marker patterns matching `text`.

    A technique "fires" iff at least MIN_HEADER_HITS of its patterns each
    match at least once. Counting distinct patterns rather than total
    occurrences (66 review WR-01) prevents one generic phrase repeated
    twice (e.g. two bare "has failed" mentions in ordinary debugging
    prose) from firing a technique on its own — a second, different
    marker must corroborate.
    """
    hits: dict[str, int] = {}
    for tech, patterns in _TECHNIQUE_CATEGORIES.items():
        hits[tech] = sum(1 for rx in patterns if rx.search(text))
    return hits


def _composer_structure_hits(text: str) -> int:
    """Total composer-structure marker hits across `text` (5-phase scaffold)."""
    total = 0
    for rx in _COMPOSER_STRUCTURE_PATTERNS:
        total += len(rx.findall(text))
    return total


def classify(
    fired: set[str], composer_structure_hits: int = 0
) -> OutputStructure:
    """Cardinality-based output-structure classifier.

    Per 46-RESEARCH §Q4 cardinality table, calibrated by 46-01-SUMMARY
    Probe 3 finding (OPTION B — composer-structure signal).

    Precedence order (DET-11 reorder + CR-02 ceiling bound, Phase 77-04):

        n == 1 AND composer < _COMPOSER_FOCUS_CEILING
                                      → "focused-<technique>"
        composer_structure_hits >= MIN_HEADER_HITS
                                      → "full-composer"  (structural override)
        n == 0                        → "none"
        n in {2, 3}                   → "ambiguous"
        n >= 4                        → "full-composer"

    DET-11 rationale: a genuine full-composer run fires MULTIPLE techniques
    (n >= 2); when exactly one technique has fired (n == 1), the output is
    a focused-technique run even if it includes canonical procedure section
    headers (e.g. `## Ground Truths` and `## Derivation Chains`). The
    focused trade-off procedure legitimately emits these headers as part of
    its standard methodology — classifying such output as `full-composer`
    was a false negative for S-P05-run2/3/5.

    CR-02 / DET-11 ceiling bound: the n==1 early-return is suppressed when
    composer_structure_hits >= _COMPOSER_FOCUS_CEILING (==4). A full-composer
    synthesis that legitimately includes a single-technique section heading
    (e.g. "## Pre-Mortem: Risk Assessment" + "failure causes" → 2 pre-mortem
    markers, n==1) alongside all four canonical scaffold headers (Ground Truths,
    Assumption Audit, Derivation Chains, Verdict → composer_hits >= 4) must
    classify `full-composer`, not `focused-pre-mortem`. The ceiling is chosen
    so that focused-with-methodology output (composer_hits <= 3, e.g.
    _FIXTURE_FOCUSED_TRADEOFF_WITH_METHODOLOGY with composer_hits=3 because
    "verdict" appears in prose as "flips the verdict") is unaffected.

    The structural override is preserved for the n == 0 case: when NO
    technique markers fire but >=2 composer scaffold tokens appear, the
    output is a full-composer run (the override prevents Pitfall 1 —
    misclassifying a lightly-fired full-composer run as `none`). The
    `_FIXTURE_STRUCTURAL_OVERRIDE` regression test (n=0, composer_hits=3)
    must still return `full-composer` after this reorder.
    """
    n = len(fired)
    # DET-11 + CR-02: check single-technique focus BEFORE the composer override,
    # but ONLY when composer hits are below the ceiling. When composer_structure_hits
    # reaches _COMPOSER_FOCUS_CEILING, the output is a full-composer synthesis that
    # happens to include a technique-specific section — the composer override must win.
    if n == 1 and composer_structure_hits < _COMPOSER_FOCUS_CEILING:
        tech = next(iter(fired))
        return f"focused-{tech}"  # type: ignore[return-value]
    # Composer-structure override: n == 0 with scaffold headers → full-composer.
    # Also applies for n == 1 when composer hits reach the ceiling (CR-02), and
    # for n >= 2 paths below when composer hits are high.
    if composer_structure_hits >= MIN_HEADER_HITS:
        return "full-composer"
    if n == 0:
        return "none"
    if n in (2, 3):
        return "ambiguous"
    return "full-composer"


# ---------------------------------------------------------------------------
# Signal A routing envelope (focused variant)
# verbatim-move-from: scripts/check-focused-output.py lines 607-667
# Note: renamed from _signal_a_invocations to _focused_signal_a_invocations
#       (CR-5/Pitfall 3 — different implementation from boundary _signal_a)
# ---------------------------------------------------------------------------

# Routing-envelope detection (Phase 46-04 calibration addition, 2026-05-28).
#
# Why this exists: the per-technique TEXT_CATEGORIES patterns were derived
# verbatim from each reference file's procedure text. Real focused-mode
# agent output uses the procedure framing but with natural variation
# ("Working backward from the wreckage" rather than the procedure's exact
# "Working backward: what caused it?"). Under strict MIN_HEADER_HITS=2 the
# focused outputs underfire and classify as `none`.
#
# The principled fix mirrors Phase 45 v2.1 Signal A: when the orchestrator's
# stream-json shows an explicit `Skill`/`Agent`/`Task` invocation targeting
# `first-principles:<technique>`, that envelope IS the routing signal.
# Combined with even a SINGLE technique-marker hit in the assistant output
# (loosened from MIN_HEADER_HITS=2), it is sufficient to classify as focused.
# The routing envelope cannot fire on its own — Signal A still requires the
# agent's output to show at least minimal procedure language, guarding
# against false-positives from invocation that immediately fails (e.g.
# clarification request returning no procedure text).
_SUBSKILL_INVOCATION_TOOL_NAMES: tuple[str, ...] = ("Skill", "Agent", "Task")


def _focused_signal_a_invocations(parsed_lines: list[object]) -> set[str]:
    """Return the set of sub-skill techniques explicitly invoked at the
    orchestrator boundary via Skill/Agent/Task tool_use envelopes whose
    routing fields (skill / subagent_type) name `first-principles:<technique>`.

    Mirrors Phase 45 v2.1 Signal A discipline: inspect only routing fields
    (not the entire input dict — would catch sub-skill names appearing in
    prompt/args text).

    NOTE: This is a DIFFERENT implementation from _boundary_signal_a. It walks
    only `type=assistant` content lists (not all parsed lines), matching the
    focused-output capture structure. Renamed from _signal_a_invocations to
    avoid confusion with the boundary detector (CR-5/Pitfall 3).
    """
    invoked: set[str] = set()
    for parsed in parsed_lines:
        if not isinstance(parsed, dict):
            continue
        if parsed.get("type") != "assistant":
            continue
        msg = parsed.get("message")
        if not isinstance(msg, dict):
            continue
        content = msg.get("content")
        if not isinstance(content, list):
            continue
        for c in content:
            if not isinstance(c, dict):
                continue
            if c.get("type") != "tool_use":
                continue
            if c.get("name") not in _SUBSKILL_INVOCATION_TOOL_NAMES:
                continue
            inp = c.get("input", {})
            if not isinstance(inp, dict):
                continue
            for field in ("skill", "subagent_type"):
                val = inp.get(field, "")
                if not isinstance(val, str):
                    continue
                val_lc = val.lower()
                for tech in _TECHNIQUE_KEYS:
                    if f"first-principles:{tech}" in val_lc:
                        invoked.add(tech)
    return invoked


# ---------------------------------------------------------------------------
# detect_output_structure + detect_output_structure_from_file
# verbatim-move-from: scripts/check-focused-output.py lines 670-743
# (internal call updated to _focused_signal_a_invocations)
# ---------------------------------------------------------------------------


def detect_output_structure(
    parsed_lines: list[object], raw_text: str
) -> OutputStructure:
    """Score a parsed stream-json event log into one of the 9 OutputStructure values.

    Structured-walk-first: extract assistant text via `_walk` (Pitfall 3 —
    don't count Read tool_result echoes). If the structured walk yields
    no text (parser drift or pre-Phase-46 capture shape), fall back to
    `raw_text` for marker counting — the trade-off here is that raw-text
    fallback may over-count markers that appear in tool inputs, but
    that risk is preferable to silently returning "none" on a capture
    shape we did not anticipate.

    Signal A (routing-envelope) override: when exactly one sub-skill was
    explicitly invoked AND its technique has at least one marker hit in
    the output AND composer-structure markers are under the full-composer
    threshold, classify as `focused-<technique>`. This handles the calibration
    gap between strict procedure-text markers and natural agent variation.
    """
    text = _extract_assistant_text(parsed_lines)
    if not text.strip():
        # Parser-drift fallback: regex the raw bytes.
        text = raw_text

    hits = _technique_hits(text)
    fired = {tech for tech, n in hits.items() if n >= MIN_HEADER_HITS}
    structure_hits = _composer_structure_hits(text)

    # Signal A: routing envelope override (Phase 46-04 calibration).
    # Direct routing evidence (Skill/Agent/Task invocation of a specific
    # sub-skill) is stronger than the composer-structure heuristic.
    # Post-151b197 rationale (66 review WR-03): the structural signal now
    # rests on the standalone scaffold tokens ("Ground Truths",
    # "Assumption Audit", "Derivation Chains", "Verdict"), and focused
    # output can mention those incidentally — e.g. the closing handoff
    # suggestion "feed this output to the composer as known ground
    # truths", or ordinary analytic prose using "verdict". Two such
    # incidental mentions reach MIN_HEADER_HITS and would force
    # `full-composer`. Without this priority ordering, P26-style prompts
    # (P26 = the former N2: slash-invoked focused-mode on a multi-phase
    # plan) could false-fail as `full-composer` despite the explicit
    # invocation envelope.
    #
    # Guard: Signal A only fires when (a) exactly one sub-skill was
    # invoked, (b) its technique shows at least one marker in the agent's
    # output, and (c) no OTHER technique fired above MIN_HEADER_HITS.
    # Condition (c) ensures we don't classify as `focused-X` when the agent
    # actually ran the full six-technique walkthrough despite a slash hint.
    invoked = _focused_signal_a_invocations(parsed_lines)
    if len(invoked) == 1:
        tech = next(iter(invoked))
        if hits.get(tech, 0) >= 1:
            other_fired = {
                t for t, c in hits.items() if t != tech and c >= MIN_HEADER_HITS
            }
            if not other_fired:
                return f"focused-{tech}"  # type: ignore[return-value]

    return classify(fired, structure_hits)


def detect_output_structure_from_file(jsonl_path: Path) -> OutputStructure:
    """File-path convenience wrapper around `detect_output_structure`."""
    raw_text = jsonl_path.read_text(encoding="utf-8", errors="replace")
    parsed_lines: list[object] = []
    for line in raw_text.splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            parsed_lines.append(json.loads(line))
        except json.JSONDecodeError:
            continue
    return detect_output_structure(parsed_lines, raw_text)


# ---------------------------------------------------------------------------
# Focused self-test fixtures
# verbatim-move-from: scripts/check-focused-output.py lines 950-1106
# ---------------------------------------------------------------------------


def _fixture_assistant_text(text: str) -> str:
    """Build a one-line stream-json blob whose assistant text == `text`."""
    return json.dumps({"type": "assistant", "text": text})


# Fixture 1 — focused-pre-mortem: ≥2 distinct pre-mortem markers, no others.
_FIXTURE_FOCUSED_PREMORTEM = "\n".join(
    [
        _fixture_assistant_text(
            "Running a prospective-hindsight analysis on the launch plan. "
            "Imagine the plan has already failed. What caused it?\n\n"
            "Working backward: what caused the rollout to stall?\n"
            "We adopt the prospective-hindsight stance throughout."
        ),
    ]
)

# Fixture 2 — focused-inversion: ≥2 distinct inversion markers, no others.
_FIXTURE_FOCUSED_INVERSION = "\n".join(
    [
        _fixture_assistant_text(
            "Invert, always invert. The inverted form of the claim is sharper.\n\n"
            "Enumerate failure-guaranteeing conditions. Each condition has a "
            "necessary precondition we must verify.\n"
            "The inverted form clarifies the assertion."
        ),
    ]
)

# Fixture 3 — LOAD-BEARING: prevents Pitfall 1 (v1-style false-positive).
# Synthetic full-composer text with markers from FOUR techniques firing
# (≥2 distinct patterns each: pre-mortem, inversion, trade-off,
# second-order). Must NOT classify as `focused-pre-mortem` just because
# pre-mortem markers fired — the cardinality classifier must return
# `full-composer`. NOTE (66 review WR-04): this fixture passes via the
# n>=4 cardinality fallback, NOT the structural override — its
# `## Phase N — <technique>` headers are not composer scaffold tokens.
# The structural-override path is covered by _FIXTURE_STRUCTURAL_OVERRIDE.
_FIXTURE_FULL_COMPOSER = "\n".join(
    [
        _fixture_assistant_text(
            "## Phase 2 — Pre-mortem\n"
            "Prospective-hindsight: the plan has already failed. What caused it?\n"
            "Working backward: what caused the rollout to stall? "
            "We adopt prospective-hindsight throughout.\n\n"
            "## Phase 3 — Inversion\n"
            "Invert, always invert. The inverted form of the claim:\n"
            "necessary precondition X is unverified. Failure-guaranteeing "
            "condition Y also holds. necessary precondition Z is fragile.\n\n"
            "## Phase 4 — Trade-off matrix\n"
            "Assign weights. Lock them now. Weighted total: 0.72.\n"
            "Sensitivity check: dropping one criterion flips the verdict.\n"
            "weighted total of the alternative scores higher.\n\n"
            "## Phase 5 — Second-order effects\n"
            "2nd-order consequence: the downstream team's roadmap shifts.\n"
            "3rd-order consequence: the platform team's hiring plan breaks.\n"
            "undermining contradiction: the fix introduces the failure mode "
            "it was supposed to prevent. The stopping rule applies here.\n"
        ),
    ]
)

# Fixture 4 — ambiguous: exactly TWO techniques' markers fire (pre-mortem
# + inversion — the documented Phase 2 + Phase 3 chain). NO composer-
# structure markers. Expected: `ambiguous`.
_FIXTURE_AMBIGUOUS = "\n".join(
    [
        _fixture_assistant_text(
            "Prospective-hindsight framing: the plan has already failed.\n"
            "Working backward: what caused the breakage?\n\n"
            "Now invert, always invert. The inverted form clarifies the claim.\n"
            "Each failure-guaranteeing condition maps to a necessary precondition.\n"
        ),
    ]
)

# Fixture 5 — none: no technique markers above threshold, no structure.
_FIXTURE_NONE_FOCUSED = "\n".join(
    [
        _fixture_assistant_text(
            "Hello world. Here is a generic answer with no methodology markers."
        ),
        _fixture_assistant_text(
            "Just plain text discussing some unrelated topic at length."
        ),
    ]
)

# Fixture 6 — raw-text fallback: malformed stream-json that fails to parse
# at the assistant-text extraction layer. Markers appear only in the raw
# bytes. Exactly ONE technique's markers fire (inversion). Expected:
# `focused-inversion` via the raw-text fallback path.
_FIXTURE_RAW_TEXT_FALLBACK = (
    "not valid json line one with no structure\n"
    "Invert, always invert. The inverted form of the claim is sharper.\n"
    "Enumerate every failure-guaranteeing condition. Each has a "
    "necessary precondition we must check. The inverted form sharpens "
    "the assertion. necessary precondition X is unverified.\n"
    "more non-json garbage\n"
)

# Fixture 10 — Bug-1 regression guard (66-03 fix; 66 review WR-04).
# Focused pre-mortem output whose PLAN CONTENT mentions "Phase 1/2/3"
# repeatedly, with NO composer scaffold tokens. Under the pre-151b197
# broad `\bPhase\s+\d+\b` structure pattern this false-classified as
# `full-composer`; it must classify `focused-pre-mortem`. Reintroducing
# a bare Phase-N structure pattern makes this fixture FAIL.
_FIXTURE_BUG1_PHASE_PROSE = "\n".join(
    [
        _fixture_assistant_text(
            "Pre-mortem on the migration plan. It is six months from now "
            "and the plan has already failed. What caused it?\n"
            "Working backward: what caused the failure?\n"
            "Phase 1 migrated staging. Phase 2 moved production traffic. "
            "Phase 3 cut over DNS. The failure traces back to Phase 2 — "
            "Phase 2 assumed staging parity that Phase 1 never validated.\n"
        ),
    ]
)

# Fixture 11 — Bug-2 regression guard (66-03 fix; 66 review WR-04).
# Natural-variation pre-mortem phrasing (no exact procedure-text quotes):
# "treat the rollout as already failed", "working backward from the
# wreckage". Under the pre-151b197 strict markers this under-fired;
# it must classify `focused-pre-mortem`. Tightening the pre-mortem
# markers back to exact procedure-text phrases makes this fixture FAIL.
_FIXTURE_BUG2_NATURAL_VARIATION = "\n".join(
    [
        _fixture_assistant_text(
            "Treat the rollout as already failed — assume it is dead on "
            "arrival.\n"
            "Working backward from the wreckage, three causes stand out: "
            "the unrehearsed cutover, the silent schema drift, and the "
            "missing rollback rehearsal.\n"
        ),
    ]
)

# Fixture DET-11 — focused trade-off output that contains methodology sections.
# The standard 5-phase procedure places "## Ground Truths" and "## Derivation
# Chains" as canonical sections even in focused-trade-off mode. With the pre-DET-11
# classify() code these 2 composer-structure hits returned "full-composer" before
# trade-off technique cardinality (n==1) was checked. After the DET-11 reorder
# (n==1 wins before composer override), this must classify `focused-trade-off`.
# Modelled on S-P05-run2/run3/run5 output shapes from:
# .planning/v5.2-inputs/rr75-evidence/S-P05-run2.jsonl, run3.jsonl, run5.jsonl
# (Q1/Q2 verify-first, 2026-06-13). The fixture fires: trade-off >= 2 distinct
# (weighted total + sensitivity check), composer_hits = 2 (Ground Truths + Derivation
# Chains), n == 1 -> focused-trade-off after the reorder.
# DET-11 regression: _FIXTURE_STRUCTURAL_OVERRIDE (n=0, composer>=2) must still
# return full-composer — the reorder only changes behaviour for the n==1 branch.
_FIXTURE_FOCUSED_TRADEOFF_WITH_METHODOLOGY = "\n".join(
    [
        _fixture_assistant_text(
            "## Trade-off Analysis: Build vs Buy\n\n"
            "The agent completed a focused trade-off analysis. "
            "Assign weights. Lock them now.\n\n"
            "| Option | weighted total |\n"
            "|--------|---------------|\n"
            "| Build  | 0.72           |\n"
            "| Buy    | 0.65           |\n\n"
            "Sensitivity check: dropping the 'team velocity' criterion flips "
            "the verdict.\n\n"
            "## Ground Truths\n"
            "Fact: the in-house team has capacity for a 6-week build.\n\n"
            "## Derivation Chains\n"
            "The weighted total of 0.72 (Build) vs 0.65 (Buy) is stable unless "
            "the team velocity assumption changes by more than 30 percent.\n"
        ),
    ]
)

# Fixture 12 — structural-override regression guard (LOAD-BEARING;
# 66 review WR-04). Canonical composer scaffold tokens with ZERO
# techniques firing. The OPTION B structural override (see calibration
# block) must classify this `full-composer` even though technique
# cardinality alone would say `none`. This is the in-repo coverage of
# the override path — the Probe 3 sanity feed (Fixture 8) is a
# local-only, gitignored capture and may be absent on fresh clones.
_FIXTURE_STRUCTURAL_OVERRIDE = "\n".join(
    [
        _fixture_assistant_text(
            "## Phase 1 — Ground Truths\n"
            "Fact: the service handles 2k rps today.\n\n"
            "## Phase 2 — Assumption Audit\n"
            "Untested belief: the cache hit rate survives the migration.\n\n"
            "## Phase 6 — Verdict\n"
            "Proceed, with the cache assumption flagged for verification.\n"
        ),
    ]
)

# Fixture CR-02 adversarial — full-composer synthesis with exactly ONE fired technique
# (n==1) AND all four composer scaffold markers (composer_structure_hits >= 4).
# A genuine full-composer output can legitimately include a "## Pre-Mortem: ..." section
# heading AND a "failure causes" mention (2 distinct pre-mortem markers → n==1) alongside
# all four canonical 5-phase scaffold headers (Ground Truths, Assumption Audit,
# Derivation Chains, Verdict → composer_hits >= 4).
# Under the pre-CR-02-fix unconditional n==1 early-return, this returns `focused-pre-mortem`.
# After the CR-02 fix (n==1 bounded by composer_structure_hits < _COMPOSER_FOCUS_CEILING),
# composer_hits=4 >= CEILING=3 so the n==1 early-return is skipped and the composer
# override fires, returning `full-composer`.
# Modelled on the VERIFICATION CR-02 reproduction text (77-VERIFICATION.md §"CR-02
# Reproduction"). The fixture must classify `full-composer`, NOT `focused-pre-mortem`.
_FIXTURE_FULLCOMPOSER_SINGLE_TECHNIQUE = "\n".join(
    [
        _fixture_assistant_text(
            "## Ground Truths\n"
            "The established constraints and facts that bound this analysis.\n\n"
            "## Assumption Audit\n"
            "All load-bearing assumptions have been audited and surfaced.\n\n"
            "## Derivation Chains\n"
            "Each conclusion traces back to a verified ground truth.\n\n"
            "## Pre-Mortem: Risk Assessment\n"
            "The potential failure causes include schema drift and rollback gaps. "
            "This section surfaces every way the plan could fail.\n\n"
            "## Verdict\n"
            "The plan is sound with the flagged risks mitigated before go-live.\n"
        ),
    ]
)

# Fixture D-08 — capture-backed positive: v5.0 inversion natural-phrasing guard.
# S-P02-run1 emitted "## Claim, inverted" / "## Inverted claim" / "## Verdict"
# but scored `none` due to missing markers. S-P02-run2 emitted "## Inverted claim".
# These new markers must fire >= MIN_HEADER_HITS on this output shape.
# Source: /tmp/step0-baseline-20260612T133945Z/S-P02-run1..2.jsonl
# (evidence copy: .planning/phases/74-fixture-context-detector-markers-and-offline-gates/evidence/v5.0-captures/).
# Dropping either new marker (`claim, inverted` or `inverted claim`) makes
# this fixture FAIL loudly on BATT-06.
_FIXTURE_FOCUSED_INVERSION_V50 = "\n".join(
    [
        _fixture_assistant_text(
            "## Claim, inverted\n"
            "- **Original:** 'Faster shipping causes better retention.'\n"
            "- **Inverted:** 'Faster shipping does not improve retention.'\n\n"
            "## Inverted claim\n"
            "Shipping speed and shipping the right thing are independent variables. "
            "Six hidden preconditions silently hold in the original.\n\n"
            "## Verdict\n"
            "False as a general rule; conditionally true at best."
        ),
    ]
)

# Fixture D-09 — explicit negative: single new inversion marker, must NOT fire.
# Proves MIN_HEADER_HITS=2 — one new marker phrase alone cannot fire inversion.
# If this fixture were to classify `focused-inversion`, a new marker was added
# without a required second-pattern guard (DET-02 / D-06 violation).
_FIXTURE_INVERSION_SINGLE_MARKER = "\n".join(
    [
        _fixture_assistant_text(
            "The claim, inverted, is that shipping faster worsens outcomes. "
            "This is a generic analytical restatement. No second marker appears here. "
            "The analysis proceeds without applying the formal inversion procedure."
        ),
    ]
)

# Fixture D-08 (pre-mortem) — capture-backed positive: v5.1 pre-mortem natural-phrasing
# guard. S-P01-run1 assistant text includes "## Pre-Mortem: Payments-Rewrite Launch"
# + "### Failure Causes"; run4 includes "# First-Principles Pre-Mortem:" + "Failure
# Causes" framing; run5 includes "## Focused Pre-mortem Mode" + "SW-1" label.
# The two new markers (section-header + failure_causes) must each fire >= 1 time
# to reach 2 distinct hits.
# Source: .planning/v5.2-inputs/rr75-evidence/S-P01-run1.jsonl, run4.jsonl,
# run5.jsonl (Q1/Q2 verify-first, 2026-06-13).
# Dropping either new marker makes this fixture FAIL loudly on BATT-06.
_FIXTURE_FOCUSED_PREMORTEM_V51 = "\n".join(
    [
        _fixture_assistant_text(
            "## Pre-Mortem: Payments-Rewrite Launch\n\n"
            "The agent reframed this as: it is the Friday after launch and "
            "the payments rewrite has failed. Here are the failure causes "
            "the agent identified:\n\n"
            "### Failure Causes\n"
            "1. Silent schema drift between legacy and new service undetected "
            "until the first real transaction.\n"
            "2. No rollback path validated before go-live.\n"
        ),
    ]
)

# Fixture D-09 (pre-mortem) — explicit negative: single new pre-mortem section-
# header marker, must NOT fire. Proves MIN_HEADER_HITS=2 — the bare section-header
# pattern alone cannot fire pre-mortem; a second distinct marker must also match.
# The fixture contains ONLY the header pattern and neutral engineering prose.
_FIXTURE_PREMORTEM_SINGLE_MARKER = "\n".join(
    [
        _fixture_assistant_text(
            "## Pre-Mortem: Checklist Entry\n\n"
            "This checklist was drawn up before the launch to capture open questions. "
            "The team reviewed each risk item and assigned an owner. "
            "No technique-specific analysis was performed in this session."
        ),
    ]
)

# Fixture D-08 (five-whys) — capture-backed positive: v5.1 five-whys natural-phrasing
# guard. S-P04 orchestrator assistant text on ALL 5 runs contains both the existing
# `five[- ]?whys?` pattern AND "causal chain" or "causal link" — the new marker.
# Together they supply 2 distinct hits.
# Source: .planning/v5.2-inputs/rr75-evidence/S-P04-run1.jsonl through
# S-P04-run5.jsonl (Q1/Q2 verify-first, 2026-06-13).
# Dropping the `causal_link` marker makes this fixture FAIL on BATT-06 (it
# reverts to 1 distinct hit, just below MIN_HEADER_HITS=2).
_FIXTURE_FOCUSED_FIVEWHYS_V51 = "\n".join(
    [
        _fixture_assistant_text(
            "The first-principles agent completed the Five Whys analysis. "
            "The agent traced a single causal chain from symptom to root:\n\n"
            "- Why #1: The payment service returned 500s for 12 minutes.\n"
            "- Why #2: A connection-pool leak hit its ceiling under load.\n"
            "- Why #3: The pool was never sized for the new traffic profile.\n"
            "- Why #4: Capacity planning was skipped during the migration sprint.\n"
            "- Why #5: No checklist item required it before the cutover gate.\n"
        ),
    ]
)

# Fixture D-09 (five-whys) — explicit negative: single new five-whys causal-link
# marker alone, must NOT fire. Proves MIN_HEADER_HITS=2 — "causal chain" alone
# (without `five[- ]?whys?` or another five-whys marker) cannot fire the technique.
# The fixture contains ONLY the causal_link pattern and neutral debugging prose.
_FIXTURE_FIVEWHYS_SINGLE_MARKER = "\n".join(
    [
        _fixture_assistant_text(
            "The agent traced a single causal chain from the observed timeout "
            "to the misconfigured connection-pool ceiling. "
            "The investigation was a standard debugging trace, not a structured "
            "methodology run. The team reviewed the causal chain and assigned a fix."
        ),
    ]
)

# Fixture D-08 (second-order) — capture-backed positive: v5.1 second-order natural-
# phrasing guard. S-P06 orchestrator assistant text on ALL 5 runs contains both
# `second[- ]?order` AND `second[- ]?order\s+(mode|analysis|effects?)` — two distinct
# patterns. Together they supply 2 distinct hits (the second is a subset of the first
# lexically, but they are separate compiled patterns and `_technique_hits` counts
# distinct PATTERNS matched, not distinct phrases).
# Source: .planning/v5.2-inputs/rr75-evidence/S-P06-run1.jsonl through
# S-P06-run5.jsonl (Q1/Q2 verify-first, 2026-06-13).
# Dropping the second-order qualified-form marker makes this fixture FAIL on BATT-06.
_FIXTURE_FOCUSED_SECONDORDER_V51 = "\n".join(
    [
        _fixture_assistant_text(
            "The first-principles agent completed its second-order analysis. "
            "Here is what it found in focused second-order effects mode:\n\n"
            "The dominant second-order effect: shipping the sync inserts a new "
            "external dependency into the revenue-critical checkout path. "
            "Three effect chains matter this week. "
            "Chain A — Temporal risk: the dependency goes live at the same moment "
            "as the highest-blast-radius demo.\n"
        ),
    ]
)

# Fixture D-09 (second-order) — explicit negative: single broad `second[- ]?order`
# marker alone, must NOT fire. Proves MIN_HEADER_HITS=2 — the bare "second-order"
# adjective alone cannot fire the technique; the more specific qualifier form
# (`second[- ]?order\s+(mode|analysis|effects?)`) must also match.
# The fixture uses "second-order" as an adjective in plain risk prose but avoids
# "second-order effects/analysis/mode" and all other second-order technique markers.
_FIXTURE_SECONDORDER_SINGLE_MARKER = "\n".join(
    [
        _fixture_assistant_text(
            "This is a second-order consideration the team raised during planning. "
            "It was noted in the risk register and deferred for the next sprint. "
            "The team did not perform a structured consequence trace in this session."
        ),
    ]
)

# Fixture D-09 (second-order / CR-01) — falsifying fixture: bare-prose "second-order
# effects" (no Markdown heading, no "effect chains", no other second-order marker).
# Under the pre-CR-01-fix nested patterns (B is subset of A), this bare phrase matched
# BOTH `\bsecond[- ]?order\b` (A) AND `\bsecond[- ]?order\s+(mode|analysis|effects?)\b`
# (B) simultaneously, yielding 2 distinct hits and firing `focused-second-order`.
# After the CR-01 fix (de-nested B with heading-anchor), the bare phrase matches only
# A (1 hit) — below MIN_HEADER_HITS=2 — so classify returns `none`.
# If this fixture classifies as anything other than `none`, the nested-pattern
# anti-masking violation has been re-introduced and CR-01 is open again.
_FIXTURE_SECONDORDER_EFFECTS_NEGATIVE = "\n".join(
    [
        _fixture_assistant_text(
            "The team flagged second-order effects as a concern during the planning session. "
            "The risk register captures this as a deferred item for the next sprint. "
            "No structured consequence trace was performed in this session. "
            "The concern is noted but not analyzed further here."
        ),
    ]
)


# ---------------------------------------------------------------------------
# Focused self-test runner (renamed from self_test — CR-4/Pitfall 5)
# verbatim-move-from: scripts/check-focused-output.py lines 1109-1273
# (K>N rejection sub-test removed — main() not in this module; K>N sub-test
# lives in merged battery's own self_test(). Probe 3 soft-skip preserved.)
# ---------------------------------------------------------------------------


def _run_one_fixture_focused(
    name: str, body: str, expected: OutputStructure
) -> bool:
    with tempfile.NamedTemporaryFile(
        mode="w", suffix=".jsonl", delete=False, encoding="utf-8"
    ) as tmp:
        tmp.write(body)
        tmp_path = Path(tmp.name)
    try:
        actual = detect_output_structure_from_file(tmp_path)
        if actual != expected:
            print(
                f"self-test FAIL: fixture {name!r} expected {expected}, got {actual}",
                file=sys.stderr,
            )
            return False
        return True
    finally:
        try:
            tmp_path.unlink()
        except OSError:
            pass


def _run_probe3_sanity_feed() -> bool | None:
    """Fixture 8 — Probe 3 sanity feed (soft-skip when the capture is absent).

    Read the LOCAL-ONLY cross-wave Probe 3 capture from
    `.planning/phases/46-.../wave0-evidence/probe3-full-composer.jsonl`
    and assert it classifies as `full-composer`. The file is NOT committed
    — `.planning/` is gitignored (66 review WR-05) — so on a fresh clone
    or CI runner it is absent. In that case this fixture is SKIPPED with
    a warning (returns None) rather than hard-failing the self-test:
    in-repo hard coverage of the structural-override path is provided by
    `_FIXTURE_STRUCTURAL_OVERRIDE` (66 review WR-04). When the capture IS
    present, a classification mismatch still fails the self-test.
    """
    probe3_path = (
        REPO_ROOT
        / ".planning"
        / "phases"
        / "46-composer-internal-dispatcher-and-focused-output"
        / "wave0-evidence"
        / "probe3-full-composer.jsonl"
    )
    if not probe3_path.exists():
        print(
            "self-test WARNING: Fixture 8 SKIPPED — Probe 3 capture absent "
            f"at\n  {probe3_path}\n"
            "  (.planning/ is gitignored; the capture exists only on the "
            "machine that ran 46-01 Task 1 Probe 3. The structural-override "
            "path is still hard-covered by the in-script "
            "structural_override_LOAD_BEARING fixture.)",
            file=sys.stderr,
        )
        return None
    actual = detect_output_structure_from_file(probe3_path)
    expected: OutputStructure = "full-composer"
    if actual != expected:
        print(
            f"self-test FAIL: Fixture 8 (Probe 3 sanity feed) expected "
            f"{expected}, got {actual}. The Q4 marker tables or the "
            f"composer-structure calibration need tuning before 46-04 runs.",
            file=sys.stderr,
        )
        return False
    return True


def self_test_focused() -> int:
    """Validate focused-output detection logic against in-module fixtures.

    Runs 20 deterministic fixtures plus the Probe 3 sanity feed when its
    local-only capture is present (soft-skipped otherwise — 66 review WR-05).
    No claude invocation.

    Fixture count breakdown:
      11 original (Fixtures 1-12 minus skipped) + 2 Phase-74 inversion D-08/D-09
      + 6 Phase-77 DET-10 D-08/D-09 (pre-mortem, five-whys, second-order)
      + 1 Phase-77 DET-11 (focused_tradeoff_with_methodology)
      + 1 Phase-77-04 CR-01 (secondorder_effects_negative)
      + 1 Phase-77-04 CR-02 (fullcomposer_single_technique)
      = 20 inline + 1 soft-skip (Probe 3).

    The K>N rejection sub-test (which calls main()) is NOT included here —
    it lives in the merged battery's own self_test() which can call
    check-routing-battery.py's main() directly.
    """
    fixtures: list[tuple[str, str, OutputStructure]] = [
        ("focused_pre_mortem", _FIXTURE_FOCUSED_PREMORTEM, "focused-pre-mortem"),
        ("focused_inversion", _FIXTURE_FOCUSED_INVERSION, "focused-inversion"),
        # LOAD-BEARING: prevents Pitfall 1 (v1-style false-positive).
        ("full_composer_LOAD_BEARING", _FIXTURE_FULL_COMPOSER, "full-composer"),
        ("ambiguous", _FIXTURE_AMBIGUOUS, "ambiguous"),
        ("none", _FIXTURE_NONE_FOCUSED, "none"),
        ("raw_text_fallback", _FIXTURE_RAW_TEXT_FALLBACK, "focused-inversion"),
        # 66 review WR-04 regression fixtures (Bug 1 / Bug 2 / override):
        (
            "bug1_phase_prose_regression",
            _FIXTURE_BUG1_PHASE_PROSE,
            "focused-pre-mortem",
        ),
        (
            "bug2_natural_variation_regression",
            _FIXTURE_BUG2_NATURAL_VARIATION,
            "focused-pre-mortem",
        ),
        (
            "structural_override_LOAD_BEARING",
            _FIXTURE_STRUCTURAL_OVERRIDE,
            "full-composer",
        ),
        # D-08: capture-backed positive — v5.0 natural inversion phrasing
        ("focused_inversion_v50_natural_phrasing", _FIXTURE_FOCUSED_INVERSION_V50, "focused-inversion"),
        # D-09: single new marker does NOT fire inversion alone
        ("inversion_single_new_marker_negative", _FIXTURE_INVERSION_SINGLE_MARKER, "none"),
        # D-08 (pre-mortem): capture-backed positive — v5.1 pre-mortem natural phrasing
        # (section-header + failure_causes new markers must fire >= 2 distinct)
        ("focused_premortem_v51_natural_phrasing", _FIXTURE_FOCUSED_PREMORTEM_V51, "focused-pre-mortem"),
        # D-09 (pre-mortem): single new section-header marker alone must NOT fire
        ("premortem_single_new_marker_negative", _FIXTURE_PREMORTEM_SINGLE_MARKER, "none"),
        # D-08 (five-whys): capture-backed positive — v5.1 five-whys natural phrasing
        # (existing five-whys + new causal_link marker must reach 2 distinct hits)
        ("focused_fivewhys_v51_natural_phrasing", _FIXTURE_FOCUSED_FIVEWHYS_V51, "focused-five-whys"),
        # D-09 (five-whys): single new causal_link marker alone must NOT fire five-whys
        ("fivewhys_single_new_marker_negative", _FIXTURE_FIVEWHYS_SINGLE_MARKER, "none"),
        # D-08 (second-order): capture-backed positive — v5.1 second-order natural phrasing
        # (two new second-order marker patterns must each fire as distinct hits)
        ("focused_secondorder_v51_natural_phrasing", _FIXTURE_FOCUSED_SECONDORDER_V51, "focused-second-order"),
        # D-09 (second-order): single broad second-order marker alone must NOT fire
        ("secondorder_single_new_marker_negative", _FIXTURE_SECONDORDER_SINGLE_MARKER, "none"),
        # D-09 (second-order / CR-01): bare-prose "second-order effects" only (no heading,
        # no "effect chains") must classify `none` — guards the de-nested pattern B.
        ("secondorder_effects_negative", _FIXTURE_SECONDORDER_EFFECTS_NEGATIVE, "none"),
        # DET-11: focused trade-off output + ## Ground Truths + ## Derivation Chains
        # (n==1 + composer_hits==2) must classify focused-trade-off after the
        # classify() reorder (was full-composer before DET-11 fix)
        (
            "focused_tradeoff_with_methodology",
            _FIXTURE_FOCUSED_TRADEOFF_WITH_METHODOLOGY,
            "focused-trade-off",
        ),
        # CR-02 adversarial: full-composer synthesis with one fired technique (n==1)
        # and composer_structure_hits >= 4 must classify `full-composer`, not `focused-`.
        # Guards the _COMPOSER_FOCUS_CEILING bound in classify() — if this fixture
        # returns `focused-pre-mortem`, CR-02 is open and the ceiling is too high or absent.
        (
            "fullcomposer_single_technique",
            _FIXTURE_FULLCOMPOSER_SINGLE_TECHNIQUE,
            "full-composer",
        ),
    ]
    all_passed = True
    for name, body, expected in fixtures:
        if not _run_one_fixture_focused(name, body, expected):
            all_passed = False

    # Fixture 8 — Probe 3 sanity feed (soft-skip when the local-only
    # capture is absent — 66 review WR-05; None means skipped).
    probe3_result = _run_probe3_sanity_feed()
    if probe3_result is False:
        all_passed = False

    probe3_counted = 1 if probe3_result is not None else 0
    fixture_total = len(fixtures) + probe3_counted
    skip_note = (
        "" if probe3_result is not None
        else " (Fixture 8 probe3 sanity feed skipped — local capture absent)"
    )
    if all_passed:
        print(f"self-test PASS ({fixture_total} fixtures){skip_note}")
        return 0
    return 1


# ===========================================================================
# SECTION 4: New symbols (no source analog — Phase 67 additions)
# ===========================================================================

# new in Phase 67 (no source analog)
@dataclass(frozen=True)
class MergedPrompt:
    """One row from the merged routing-battery-catalog.md."""

    id: str
    text: str
    expected_boundary: str  # "none-or-other" | sub-skill | "n-a"
    expected_output: str    # "focused-<technique>" | "NOT-any-focused" | "n-a"


# new in Phase 67 (no source analog)
def parse_merged_catalog(path: Path) -> tuple[list[MergedPrompt], list[MergedPrompt]]:
    """Parse a merged routing-battery-catalog.md-shaped Markdown catalog.

    Reads 4-column rows:
      cells[0] = id (de-collided, e.g. B-P12, F-P12)
      cells[1] = prompt text
      cells[2] = expected_boundary ("none-or-other" | sub-skill | "n-a")
      cells[3] = expected_output ("focused-<technique>" | "NOT-any-focused" | "n-a")
      cells[4+] = ignored (Signal, Lineage columns)

    P/N classification: strips a single leading [A-Z]- prefix before checking
    rid[0] in ("P", "N"), so B-P12 → P-row, F-N1 → N-row.

    Validates expected_boundary against _VALID_SUBSKILLS unless it equals "n-a".
    Accepts any non-empty string for expected_output.

    Raises FileNotFoundError if path missing, ValueError on malformed/empty rows
    or invalid expected_boundary value.
    """
    if not path.exists():
        raise FileNotFoundError(f"catalog not found: {path}")

    positives: list[MergedPrompt] = []
    negatives: list[MergedPrompt] = []

    in_table = False
    expecting_separator = False

    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.rstrip()
        if not line.startswith("|"):
            in_table = False
            expecting_separator = False
            continue

        cells = _split_row(line)
        if not cells:
            in_table = False
            continue

        if not in_table:
            if len(cells) >= 3 and cells[1].strip().lower() == "prompt":
                in_table = True
                expecting_separator = True
                continue
            continue

        if expecting_separator:
            expecting_separator = False
            if _is_separator_row(cells):
                continue

        if len(cells) < 4:
            continue
        rid = cells[0].strip()
        prompt_text = _strip_quotes(cells[1])
        expected_boundary_raw = cells[2].strip()
        expected_output_raw = cells[3].strip()

        if not rid:
            continue

        # Strip leading [A-Z]- prefix for P/N classification (de-collision scheme)
        # e.g. "B-P12" → rid_stripped = "P12", rid_stripped[0] = "P"
        rid_stripped = re.sub(r"^[A-Z]-", "", rid)
        if not rid_stripped or rid_stripped[0] not in ("P", "N"):
            continue

        # Validate expected_boundary (unless n-a)
        expected_boundary_lc = expected_boundary_raw.lower()
        if expected_boundary_lc != "n-a" and expected_boundary_lc not in _VALID_SUBSKILLS:
            raise ValueError(
                f"row {rid!r}: expected_boundary must be one of "
                f"{sorted(_VALID_SUBSKILLS)} or 'n-a', got {expected_boundary_raw!r}"
            )

        # expected_output: accept any non-empty string
        if not expected_output_raw:
            raise ValueError(
                f"row {rid!r}: expected_output cell must be non-empty"
            )

        prompt = MergedPrompt(
            id=rid,
            text=prompt_text,
            expected_boundary=expected_boundary_lc,
            expected_output=expected_output_raw,
        )
        if rid_stripped.startswith("P"):
            positives.append(prompt)
        else:
            negatives.append(prompt)

    if not positives and not negatives:
        raise ValueError(f"catalog {path} contained no P* or N* rows")
    return positives, negatives


# new in Phase 67 (no source analog)
def _both_match(
    boundary_verdicts: list[SubSkill],
    focused_verdicts: list[OutputStructure],
    expected_boundary: str,
    expected_output: str,
    min_pass: int,
) -> tuple[int, int, bool]:
    """Return (boundary_match_count, focused_match_count, both_passed).

    n-a signals auto-pass (count as min_pass matches). This implements D-02:
    per-prompt verdict reduces to the single non-n-a signal for rows where
    only one signal is relevant.

    Args:
        boundary_verdicts: list of SubSkill verdicts from detect_subskill()
        focused_verdicts: list of OutputStructure verdicts from
                          detect_output_structure_from_file()
        expected_boundary: "none-or-other" | sub-skill | "n-a"
        expected_output: "focused-<technique>" | "NOT-any-focused" | "n-a"
        min_pass: K-of-N threshold

    Returns:
        (b_count, f_count, both_passed) where both_passed = True iff
        b_count >= min_pass and f_count >= min_pass.
    """
    if expected_boundary == "n-a":
        b_count = min_pass  # auto-pass
    else:
        b_count = sum(
            1 for v in boundary_verdicts
            if _is_match(v, expected_boundary)  # type: ignore[arg-type]
        )

    if expected_output == "n-a":
        f_count = min_pass  # auto-pass
    else:
        f_count = sum(
            1 for v in focused_verdicts
            if _verdict_matches(v, expected_output)
        )

    return b_count, f_count, (b_count >= min_pass and f_count >= min_pass)
