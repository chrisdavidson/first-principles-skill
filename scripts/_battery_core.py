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


def _lookup_catalog_prompt(catalog_path: Path, row_id: str) -> str | None:
    """Return the prompt cell of the Markdown row whose first cell == ``row_id``.

    Returns ``None`` if the catalog file is absent or the row is not present.
    Used only by the RR-80-01 drift guard (WR-02); the hardcoded inline literal
    — not this lookup — remains the value actually classified, so deletion of the
    row stays survivable (D-04) while an *edit* to the row is caught loudly.

    The S-N04 prompt cell contains no embedded ``|`` characters, so the simple
    cell split is safe for this row.
    """
    try:
        text = catalog_path.read_text(encoding="utf-8")
    except OSError:
        return None
    for line in text.splitlines():
        if "|" not in line:
            continue
        cells = _split_row(line)
        if len(cells) >= 2 and cells[0] == row_id:
            return cells[1]
    return None


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

    Runs 8 boundary fixtures plus 1 named RR-80-01 marker-counting assertion.
    The K>N rejection sub-test (which calls main()) is NOT included here — it
    lives in the merged battery's own self_test() which can call
    check-routing-battery.py's main() directly.
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

    # ---------------------------------------------------------------------------
    # _load_excerpt helper — reads vendored v5.2 assistant-text excerpts.
    # Files are the output of _extract_assistant_text() applied to the source
    # .jsonl captures; they live under tests/step0-captures-v5.2/ (git-tracked).
    # Uses Path.read_text() so a missing file raises FileNotFoundError loudly —
    # no try/except that would produce a vacuous empty-string zero-count (Pitfall 5).
    # ---------------------------------------------------------------------------
    _V52_DIR = REPO_ROOT / "tests" / "step0-captures-v5.2"

    def _load_excerpt(prompt_id: str, run: int) -> str:
        return (_V52_DIR / f"{prompt_id}-run{run}.txt").read_text(encoding="utf-8")

    # ---------------------------------------------------------------------------
    # _load_excerpt_v63 helper — reads Phase 91 v6.3 assistant-text excerpts.
    # Files live under tests/step0-captures-v6.3/ (git-tracked, Phase 91 REARCH-01).
    # Uses Path.read_text() so a missing file raises FileNotFoundError loudly —
    # no try/except that would produce a vacuous empty-string zero-count (Pitfall 5).
    # ---------------------------------------------------------------------------
    _V63_DIR = REPO_ROOT / "tests" / "step0-captures-v6.3"

    def _load_excerpt_v63(prompt_id: str, run: int) -> str:
        return (_V63_DIR / f"{prompt_id}-run{run}.txt").read_text(encoding="utf-8")

    # ---------------------------------------------------------------------------
    # _load_excerpt_v64 helper — reads Phase 96 v6.4 assistant-text excerpts.
    # Files live under tests/step0-captures-v6.4/ (git-tracked, Phase 96 D-01/D-02).
    # Uses Path.read_text() so a missing file raises FileNotFoundError loudly —
    # no try/except that would produce a vacuous empty-string zero-count (Pitfall 5).
    # ---------------------------------------------------------------------------
    _V64_DIR = REPO_ROOT / "tests" / "step0-captures-v6.4"

    def _load_excerpt_v64(prompt_id: str, run: int) -> str:
        return (_V64_DIR / f"{prompt_id}-run{run}.txt").read_text(encoding="utf-8")

    # _load_excerpt_v74 helper — reads Phase 108 v7.4 assistant-text excerpts.
    # Files live under tests/step0-captures-v7.4/ (git-tracked, Phase 108 D-04).
    # Same shape as _load_excerpt_v64: Path.read_text() so a missing file raises
    # FileNotFoundError loudly (Pitfall 5 — no vacuous empty-string zero-count).
    # The v6.4 excerpts remain byte-frozen under tests/step0-captures-v6.4/.
    _V74_DIR = REPO_ROOT / "tests" / "step0-captures-v7.4"

    def _load_excerpt_v74(prompt_id: str, run: int) -> str:
        return (_V74_DIR / f"{prompt_id}-run{run}.txt").read_text(encoding="utf-8")

    # _load_excerpt_v76 helper — reads Phase 114 v7.6 assistant-text excerpts.
    # Same shape as _load_excerpt_v74: Path.read_text() so a missing file raises
    # loudly. Captures are the genuine-zone (pre-spend-limit) sentinel rows from
    # the single authoritative v7.6 partial run (S-P01/S-P02/S-P05/S-N04 all
    # landed before the 55/110-call monthly-spend-limit truncation).
    # Retained for lineage (RR-114-01 S-P02 inversion, RR-108-02 S-P05 trade-off).
    _V76_DIR = REPO_ROOT / "tests" / "step0-captures-v7.6"

    def _load_excerpt_v76(prompt_id: str, run: int) -> str:
        return (_V76_DIR / f"{prompt_id}-run{run}.txt").read_text(encoding="utf-8")

    # _load_excerpt_v77 helper — reads Phase 117 v7.7 CONF-01 assistant-text excerpts.
    # Same shape as _load_excerpt_v76: Path.read_text() so a missing file raises
    # loudly (Pitfall 5 — no vacuous empty-string zero-count).
    # Captures are the full-run (not truncated) 30-call CONF-01 live run
    # (S-P01/S-P03/S-N01/S-N02/S-N03/S-N04 × 5 repeats; all genuine transcripts,
    # monthly spend budget held). Added in Phase 117 CONF-02 (Plan 07, D-04 step two).
    # Retained for lineage (RR-79-01/RR-117-01/RR-117-02/RR-80-01 re-pointed to v7.8
    # in Phase 119 CONF-04; v7.7 captures byte-frozen).
    _V77_DIR = REPO_ROOT / "tests" / "step0-captures-v7.7"

    def _load_excerpt_v77(prompt_id: str, run: int) -> str:
        return (_V77_DIR / f"{prompt_id}-run{run}.txt").read_text(encoding="utf-8")

    # _load_excerpt_v78 helper — reads Phase 119 v7.8 CONF-03 assistant-text excerpts.
    # Same shape as _load_excerpt_v77: Path.read_text() so a missing file raises
    # loudly (Pitfall 5 — no vacuous empty-string zero-count).
    # Captures are the full-run (not truncated) 30-call CONF-03 live run
    # (S-P01/S-P03/S-N01/S-N02/S-N03/S-N04 × 5 repeats; 29/30 genuine — S-N04-run5
    # is_error:true, 74-char anomaly on a non-blocking row, count=0; all blocking rows
    # clean). Added in Phase 119 CONF-04 (Plan 03, D-04 step two / D-5 honesty-not-score).
    _V78_DIR = REPO_ROOT / "tests" / "step0-captures-v7.8"

    def _load_excerpt_v78(prompt_id: str, run: int) -> str:
        return (_V78_DIR / f"{prompt_id}-run{run}.txt").read_text(encoding="utf-8")

    # ---------------------------------------------------------------------------
    # RR-80-01 named marker-counting assertion (D-03 / D-04 — Phase 84, Plan 02;
    #          re-pointed to v6.3 evidence Phase 93, Plan 01;
    #          re-pointed to v6.4 evidence Phase 96, Plan 02;
    #          re-pointed to v7.4 evidence Phase 108, Plan 02;
    #          re-pointed to v7.6 evidence Phase 114, Plan 02;
    #          re-pointed to post-fix detector / pre-fix v7.6 captures Phase 117, Plan 02;
    #          re-pointed to live v7.7 CONF-01 captures Phase 117, Plan 07 — D-04 step two;
    #          re-pointed to live v7.8 CONF-03 captures Phase 119, Plan 03 — D-04 step two)
    #
    # RR-80-01 is the S-N04 semantically-pre-mortem negative-control row.  S-N04 is
    # in NON_BLOCKING_NEGATIVE_IDS (Phase 117, Plan 05, D-16): the live first-principles
    # agent genuinely selects a focused pre-mortem on this prompt because the prompt
    # is semantically pre-mortem (the D-17 blocking criterion excludes S-N04 from the
    # blocking bar).  S-N04 is reported non-blocking.
    #
    # At the Phase 117 CONF-01 live re-baseline (tests/step0-baseline-v7.7.md):
    # S-N04 observed 2/5 (non-blocking; over-routes on runs 2, 3, 5). v7.7 vector:
    # [1, 2, 2, 1, 3].
    #
    # Phase 119 CONF-03 (tests/step0-baseline-v7.8.md): S-N04 observed 5/5
    # (non-blocking; Phase-118 FIX-03/FIX-04 prose fix moved over the bar).
    # Note: S-N04-run5 returned is_error:true (74-char anomaly, num_turns=2 —
    # a single transient error on a non-blocking row); count=0 for that run.
    # The blocking verdict is unaffected (S-N04 is non-blocking).
    #
    # Phase 119 CONF-04 (D-04 step two): the asserted vector is updated to
    # [1, 1, 1, 1, 0] — the live-measured v7.8 count vector over the frozen
    # tests/step0-captures-v7.8/S-N04-run{1..5}.txt excerpts.  The captures
    # are NOT modified; only the asserted constants change.
    #
    # This offline gate asserts TWO things (honesty-not-score principle, D-01):
    #
    # (1) SC#2 mechanism check (synthetic): the focused-output classifier fires
    #     pre-mortem ONLY when _technique_hits returns >= MIN_HEADER_HITS (2)
    #     DISTINCT pre-mortem marker patterns.  One bare hit < MIN keeps the S-N04
    #     prompt below the threshold.  This assertion proves the mechanism in isolation.
    #
    # (2) v7.7 per-run marker-count vector: [1, 2, 2, 1, 3] over the live
    #     tests/step0-captures-v7.7/S-N04-run{1..5}.txt excerpts (Phase 117 CONF-01).
    #     Runs 2, 3, 5 clear MIN_HEADER_HITS (over-route to focused-pre-mortem);
    #     runs 1, 4 stay below (count 1, 1 — correctly return full-composer).
    #     Positive counter-check: run2=2 >= MIN proves the detector CAN fire on
    #     S-N04 text (the documented genuine pre-mortem routing, non-blocking per D-16).
    #
    # Drift guard: _COMPOSER_FOCUS_CEILING == 4 locked here; any future threshold
    # edit now fails this sentinel.  Pre-mortem pattern count drift guard: 9.
    #
    # Exact S-N04 prompt (verbatim from tests/step0-fixture-catalog.md line 47,
    # catalog-independent inline literal per D-04 — grep locates this assertion):
    #   "We have a written plan to roll out the new authentication system across all
    #    teams next quarter. Before we lock the timeline, walk through how this could
    #    go badly — what failure modes should we prepare for?"
    # ---------------------------------------------------------------------------
    _SN04_PROMPT = (
        "We have a written plan to roll out the new authentication system across all"
        " teams next quarter. Before we lock the timeline, walk through how this could"
        " go badly — what failure modes should we prepare for?"
    )
    # Drift guard (WR-02): the hardcoded literal must still match the live catalog
    # S-N04 row, OR the row must be absent.  Deletion is the survivable case D-04
    # targets (the literal — not the catalog — is what drives the assertion, so the
    # gate keeps running catalog-independently).  But a silent *edit* to the catalog
    # row (e.g. a mangled em-dash) now fails loudly here instead of leaving the gate
    # testing a stale prompt.
    _sn04_catalog_prompt = _lookup_catalog_prompt(
        REPO_ROOT / "tests" / "step0-fixture-catalog.md", "S-N04"
    )
    if _sn04_catalog_prompt is not None and _sn04_catalog_prompt != _SN04_PROMPT:
        print(
            "  RR-80-01 FAIL: hardcoded S-N04 literal drifted from the live catalog "
            "row (tests/step0-fixture-catalog.md) — re-sync the literal or update the "
            f"gate.\n    literal : {_SN04_PROMPT!r}\n    catalog : {_sn04_catalog_prompt!r}"
        )
        all_passed = False

    # --- (1) SC#2 mechanism check (synthetic one-bare-hit fixture) ---
    # Minimal text: exactly ONE distinct pre-mortem pattern fires (the section header),
    # no second distinct marker (no "working backward", no "already failed", no
    # "failure causes").  Mirror the _FIXTURE_PREMORTEM_SINGLE_MARKER pattern.
    _rr8001_text = _fixture_assistant_text(
        "## Pre-Mortem\n\n"
        "Here are some general considerations for this plan. "
        "The team should review each area carefully."
    )
    _rr8001_hits = _technique_hits(_rr8001_text)
    _rr8001_pm_count = _rr8001_hits.get("pre-mortem", 0)
    _rr8001_fired = {t for t, c in _rr8001_hits.items() if c >= MIN_HEADER_HITS}
    _rr8001_result = classify(_rr8001_fired, _composer_structure_hits(_rr8001_text))

    # Counter-check that the focused branch is load-bearing (WR-01 fix): if the
    # MIN_HEADER_HITS barrier were lowered to 1, this one-hit text WOULD enter
    # `fired`, and classify() WOULD return "focused-pre-mortem".  Asserting the
    # positive case makes clause 3 (`_rr8001_result != "focused-pre-mortem"`)
    # non-vacuous: a regression in classify()'s `n == 1 → focused-<tech>` branch
    # now fails the assertion instead of passing trivially via the empty-set path.
    _rr8001_would_fire_at_1 = {t for t, c in _rr8001_hits.items() if c >= 1}
    _rr8001_at_1_result = classify(
        _rr8001_would_fire_at_1, _composer_structure_hits(_rr8001_text)
    )

    _rr8001_mechanism_ok = (
        _rr8001_pm_count == 1
        and _rr8001_pm_count < MIN_HEADER_HITS
        and "pre-mortem" not in _rr8001_fired               # barrier holds at MIN_HEADER_HITS=2
        and "pre-mortem" in _rr8001_would_fire_at_1          # barrier is load-bearing (>=1 would fire)
        and _rr8001_at_1_result == "focused-pre-mortem"      # mechanism counter-check (focused branch live)
        and _rr8001_result != "focused-pre-mortem"
    )

    # --- (2) v7.8 S-N04 per-run pre-mortem distinct-marker count vector ---
    # Asserts the live-measured v7.8 vector [1, 1, 1, 1, 0] over the frozen
    # tests/step0-captures-v7.8/S-N04-run{1..5}.txt excerpts (CONF-03, D-04 step two).
    # 9-marker post-fix detector: all runs stay below MIN_HEADER_HITS → full-composer 5/5;
    # S-N04 NON_BLOCKING per D-16 (semantically-pre-mortem prompt).
    # Note: S-N04-run5 is_error:true (74-char anomaly) — count=0 for run5; blocking verdict
    # unaffected (S-N04 non-blocking). Phase 119 CONF-04, D-04 step two — captures NOT modified.
    _rr8001_sn04_counts: list[int] = []
    for _run in range(1, 6):
        _text = _load_excerpt_v78("S-N04", _run)
        _hits = _technique_hits(_text)
        _rr8001_sn04_counts.append(_hits.get("pre-mortem", 0))

    # Drift guard: pre-mortem pattern count must not silently grow.
    # D-08 bump: 6 → 7 after adding "fix forward" (Phase 91, Plan 02, 2026-06-16).
    # Phase 117 FIX-02 bump: 7 → 9 after adding "structural weakness" + "failure chain"
    # (Phase 117, Plan 01, 2026-06-24) — the DIAG-01-prescribed marker recalibration.
    _rr8001_pm_pattern_count = len(_TECHNIQUE_CATEGORIES["pre-mortem"])

    # Positive counter-check: run1=1 >= 1 proves the detector is alive — any of
    # the 9 markers can fire; the v7.8 result is ≤ 1 on all runs (Phase-118 prose fix
    # narrowed over-routing on this semantically-pre-mortem prompt; all 5 runs
    # stay below MIN_HEADER_HITS=2 → full-composer on every run, 5/5).
    # RR-80-01 re-pointed to v7.8 (Phase 119 CONF-04): S-N04 5/5 non-blocking.
    # _COMPOSER_FOCUS_CEILING lock: any edit to this threshold will now trip this gate.
    _rr8001_v78_ok = (
        _rr8001_sn04_counts == [1, 1, 1, 1, 0]
        and all(c < MIN_HEADER_HITS for c in _rr8001_sn04_counts)  # no run clears barrier (non-vacuous)
        and _rr8001_pm_pattern_count == 9                           # drift guard (Phase 117 FIX-02 bump: 7→9)
        and _COMPOSER_FOCUS_CEILING == 4                            # lock: threshold byte-unchanged
    )

    _rr8001_assertions_ok = _rr8001_mechanism_ok and _rr8001_v78_ok

    if _rr8001_assertions_ok:
        print(
            f"  RR-80-01 PASS: one bare pre-mortem hit ({_rr8001_pm_count}) "
            f"< MIN_HEADER_HITS ({MIN_HEADER_HITS}); "
            f"classify() returned '{_rr8001_result}' (not 'focused-pre-mortem'); "
            f"v7.8 S-N04 count vector {_rr8001_sn04_counts} == [1, 1, 1, 1, 0] "
            f"(live CONF-03 v7.8 captures; 9-marker post-fix detector; "
            f"all runs < MIN_HEADER_HITS=2 → full-composer 5/5; "
            f"S-N04 NON_BLOCKING per D-16 (semantically-pre-mortem prompt); "
            f"run5 is_error:true 74-char anomaly, count=0 — non-blocking row, verdict unaffected; "
            f"S-N04 5/5 at Phase 119 CONF-03 re-baseline (Phase-118 FIX-03/FIX-04 prose fix); "
            f"re-pointed to v7.8 Phase 119 CONF-04, D-04 step two); "
            f"pm_patterns={_rr8001_pm_pattern_count} (expected 9); CEILING={_COMPOSER_FOCUS_CEILING}. "
            f"S-N04 prompt: '{_SN04_PROMPT[:60]}...'"
        )
    else:
        if not _rr8001_mechanism_ok:
            print(
                f"  RR-80-01 FAIL: mechanism check failed — pre-mortem hits={_rr8001_pm_count}, "
                f"MIN_HEADER_HITS={MIN_HEADER_HITS}, "
                f"classify() returned '{_rr8001_result}' (expected not 'focused-pre-mortem'). "
                f"S-N04 prompt: '{_SN04_PROMPT[:60]}...'"
            )
        if not _rr8001_v78_ok:
            print(
                f"  RR-80-01 FAIL: v7.8 S-N04 count vector {_rr8001_sn04_counts} "
                f"(expected [1, 1, 1, 1, 0]; live CONF-03 v7.8 captures); "
                f"pm_patterns={_rr8001_pm_pattern_count} (expected 9); "
                f"CEILING={_COMPOSER_FOCUS_CEILING} (expected 4); "
                f"check: all runs must be < MIN_HEADER_HITS={MIN_HEADER_HITS}."
            )
        all_passed = False

    # ---------------------------------------------------------------------------
    # RR-79-01 named honest-state sentinel (Phase 85, Plan 01; re-pointed Phase 93,
    #          Plan 01; re-pointed to v6.4 evidence Phase 96, Plan 02;
    #          re-pointed to v7.4 evidence Phase 108, Plan 02;
    #          re-pointed to v7.6 evidence Phase 114, Plan 02;
    #          re-pointed to post-fix detector / pre-fix v7.6 captures Phase 117, Plan 02;
    #          re-pointed to live v7.7 CONF-01 captures Phase 117, Plan 07 — D-04 step two;
    #          re-pointed to live v7.8 CONF-03 captures Phase 119, Plan 03 — D-04 step two)
    #
    # **CLOSED at Phase 117 v7.7 CONF-01 (tests/step0-baseline-v7.7.md): S-P01
    # sustained 3/5 ≥ min-pass — the pre-mortem under-routing residual is
    # resolved by the FIX-01 detector recalibration.**
    # CLOSE keeps the RR-79-01 ID (RR-108-02 CLOSE precedent per D-09).
    # This sentinel is retained as a regression guard (the CLOSED honest state
    # asserted here; removing the sentinel would lose the regression-guard coverage).
    #
    # **CLOSE SUSTAINED at Phase 119 v7.8 CONF-03 (tests/step0-baseline-v7.8.md):
    # S-P01 3/5 ≥ min-pass — CLOSE confirmed out-of-sample with Phase-118 prose fix.**
    # Sentinel re-pointed to v7.8 captures (Phase 119 CONF-04, D-04 step two).
    #
    # RR-79-01 is the S-P01 pre-mortem row:
    # - v7.6 re-baseline (Phase 114): 2/5 FAIL (REGRESSED from v7.4's 3/5).
    # - Phase 117 FIX-02 (D-04 step one): re-scored over the SAME byte-frozen v7.6
    #   captures with the 9-marker post-fix detector → post-fix vector [2,3,2,3,1]
    #   (the FIX works on v7.6 text; asserted in Phase 117 Plan 02).
    # - Phase 117 CONF-01 (D-04 step two): live re-baseline over fresh v7.7 captures
    #   → S-P01 3/5 PASS (runs 2,3,5 route to focused-pre-mortem out-of-sample).
    #   v7.7 count vector: [0, 2, 3, 1, 4] over tests/step0-captures-v7.7/S-P01-*.txt.
    # - Phase 119 CONF-03 (D-04 step two): live re-baseline over fresh v7.8 captures
    #   → S-P01 3/5 PASS (runs 2,3,5 route to focused-pre-mortem out-of-sample).
    #   v7.8 count vector: [1, 2, 3, 0, 2] over tests/step0-captures-v7.8/S-P01-*.txt.
    #
    # This offline gate does NOT assert the live pass rate; it asserts the
    # DOCUMENTED per-run distinct pre-mortem marker count vector over the live
    # v7.8 CONF-03 excerpts (tests/step0-captures-v7.8/S-P01-run{1..5}.txt,
    # honesty-not-score principle, D-01).
    #
    # v7.8 count vector: [1, 2, 3, 0, 2]
    #   run1: 1 marker  (stays below MIN_HEADER_HITS → full-composer on that run)
    #   run2: 2 markers (clears barrier → focused-pre-mortem ✓)
    #   run3: 3 markers (clears barrier → focused-pre-mortem ✓)
    #   run4: 0 markers (stays below MIN_HEADER_HITS → full-composer on that run)
    #   run5: 2 markers (clears barrier → focused-pre-mortem ✓)
    # Runs 2,3,5 clear MIN_HEADER_HITS → K/N = 3/5 PASS.
    # v6.3/v6.4/v7.4/v7.6/v7.7 excerpts remain byte-frozen (D-04).
    # ---------------------------------------------------------------------------
    _rr7901_counts: list[int] = []
    for _run in range(1, 6):
        _text = _load_excerpt_v78("S-P01", _run)
        _hits = _technique_hits(_text)
        _rr7901_counts.append(_hits.get("pre-mortem", 0))

    # Drift guard (WR-02): pre-mortem marker set size must not silently grow.
    # D-08 bump: 6 → 7 after adding "fix forward" (Phase 91, Plan 02, 2026-06-16).
    # Phase 117 FIX-02 bump: 7 → 9 after adding "structural weakness" + "failure chain"
    # (Phase 117, Plan 01, 2026-06-24) — the DIAG-01-prescribed marker recalibration.
    _rr7901_pm_pattern_count = len(_TECHNIQUE_CATEGORIES["pre-mortem"])
    if _rr7901_pm_pattern_count != 9:
        print(
            f"  RR-79-01 FAIL: pre-mortem pattern count drifted "
            f"(expected 9, got {_rr7901_pm_pattern_count}) — update sentinel "
            f"after verifying new count vector over S-P01-run1..5 (v7.8)."
        )
        all_passed = False

    # Positive counter-check (WR-01): runs 2, 3, 5 each clear the
    # MIN_HEADER_HITS barrier, proving the barrier IS exercised on real v7.8 data
    # (non-vacuous: the below-barrier runs 1, 4 are meaningful because the barrier
    # IS reachable on runs 2, 3, 5 in the live CONF-03 captures).
    _rr7901_ok = (
        _rr7901_counts == [1, 2, 3, 0, 2]
        and _rr7901_counts[1] >= MIN_HEADER_HITS    # run2 fires (counter-check)
        and _rr7901_counts[2] >= MIN_HEADER_HITS    # run3 fires (counter-check)
        and _rr7901_pm_pattern_count == 9           # drift guard (Phase 117 FIX-02 bump: 7→9)
    )
    if _rr7901_ok:
        print(
            f"  RR-79-01 PASS (CLOSED at v7.7; CLOSE SUSTAINED at v7.8): "
            f"S-P01 pre-mortem count vector {_rr7901_counts} "
            f"== [1, 2, 3, 0, 2] (live CONF-03 v7.8 captures; 9-marker post-fix detector; "
            f"run2={_rr7901_counts[1]} and run3={_rr7901_counts[2]} each >= MIN_HEADER_HITS={MIN_HEADER_HITS}; "
            f"runs 2,3,5 clear barrier → 3/5 PASS at Phase 119 CONF-03 — CLOSE SUSTAINED; "
            f"Phase 119 CONF-04, D-04 step two; retained as regression guard); "
            f"pm_patterns={_rr7901_pm_pattern_count} (expected 9)."
        )
    else:
        print(
            f"  RR-79-01 FAIL: S-P01 pre-mortem count vector {_rr7901_counts} "
            f"(expected [1, 2, 3, 0, 2]; live CONF-03 v7.8 captures); "
            f"pm_patterns={_rr7901_pm_pattern_count} "
            f"(expected 9); run2={_rr7901_counts[1] if len(_rr7901_counts) > 1 else '?'} "
            f"run3={_rr7901_counts[2] if len(_rr7901_counts) > 2 else '?'} "
            f"(each must be >= MIN_HEADER_HITS={MIN_HEADER_HITS})."
        )
        all_passed = False

    # ---------------------------------------------------------------------------
    # RR-114-01 named honest-state sentinel (Phase 114, Plan 02)
    # RR-114-01 supersedes RR-108-01 (Phase 114 v7.6 carry-forward, S-P02 inversion)
    # Supersession chain: RR-79-02 → RR-92-01 → RR-95-01 → RR-108-01 → RR-114-01
    #
    # RR-114-01 is the S-P02 inversion carry-forward: observed 1/5 FAIL in the
    # Phase 114 v7.6 live re-baseline (tests/step0-baseline-v7.6.md).  The live
    # agent routes to focused-inversion on run 1 only; 4/5 runs return full-composer.
    # v7.6 is 1/5 — no change from v7.4's 1/5 (the inversion trigger still
    # under-fires on the as-shipped v7.5 body; measurement-only milestone, no fix).
    #
    # The carried-forward status comes from the live 1/5 MODE outcome, not from
    # a zero/below-MIN detector vector (honesty-not-score, D-01): the offline
    # detector fires on run1 (count=2 >= MIN_HEADER_HITS); runs 2/3/4/5 fire 0/1/1/1
    # (below MIN).  The offline and live layers are distinct.
    #
    # WR-01 fix (Phase 94): the original `when\s+the\s+assumption\s+breaks` without
    # a negative lookahead double-counted runs (both markers fired on the
    # same "When the assumption breaks down" span).  The lookahead (?!\s+down)
    # restores Phase 91 CR-01 non-overlap discipline.
    #
    # This gate asserts the DOCUMENTED per-run v7.6 inversion count vector
    # [2, 0, 1, 1, 1] over tests/step0-captures-v7.6/S-P02-run{1..5}.txt.
    # The v6.3/v6.4/v7.4 excerpts remain byte-frozen (D-04).
    #
    # Supersession comment for old IDs:
    #   RR-79-02 → RR-92-01 (renamed Phase 93 Plan 01; S-P02 inversion;
    #   re-pointed from v5.2 all-zero to v6.3 vector [1, 1, 2, 0, 0];
    #   WR-01 fix Phase 94 corrects v6.3 vector to [2, 2, 2, 1, 1])
    #   RR-92-01 → RR-95-01 (renamed Phase 96 Plan 02; re-pointed to v6.4
    #   vector [2, 1, 1, 1, 0]; Phase 95 v6.4 carry-forward, S-P02 inversion)
    #   RR-95-01 → RR-108-01 (renamed Phase 108 Plan 02; re-pointed to v7.4
    #   vector [1, 2, 1, 1, 1]; Phase 108 v7.4 carry-forward, S-P02 inversion 1/5)
    #   RR-108-01 → RR-114-01 (renamed Phase 114 Plan 02; re-pointed to v7.6
    #   vector [2, 0, 1, 1, 1]; Phase 114 v7.6 carry-forward, S-P02 inversion 1/5)
    # ---------------------------------------------------------------------------
    _rr11401_inv_counts: list[int] = []
    for _run in range(1, 6):
        _text = _load_excerpt_v76("S-P02", _run)
        _hits = _technique_hits(_text)
        _rr11401_inv_counts.append(_hits.get("inversion", 0))

    # Drift guard (WR-02): inversion marker set size must not silently grow.
    # A new inversion pattern could alter the v7.4 count vector —
    # fail loudly so the sentinel is updated with the new vector.
    # D-08 bump: 6 → 7 after adding "the assumption breaks down" (CR-01 fix removed the
    # overlapping "when the assumption breaks" sibling; only one inversion marker added).
    # D-08 bump: 7 → 8 after adding "inversion analysis" (Phase 94, Plan 03, 2026-06-17).
    # D-08 bump: 8 → 9 after adding "when the assumption breaks" (Phase 94, Plan 03, 2026-06-17).
    # D-03 bump: 9 → 13 (4 output-contract header markers, Phase 121 OCH-02, 2026-06-26).
    _rr11401_inv_pattern_count = len(_TECHNIQUE_CATEGORIES["inversion"])
    if _rr11401_inv_pattern_count != 13:
        print(
            f"  RR-114-01 FAIL: inversion pattern count drifted "
            f"(expected 13, got {_rr11401_inv_pattern_count}) — update sentinel "
            f"after verifying new per-run inversion counts over S-P02-run1..5 (v7.6)."
        )
        all_passed = False

    # Positive counter-check (WR-01): prove the inversion detector IS live
    # and CAN fire on v7.6 text — the real-excerpt vector is a genuine partial-hit
    # picture, not a dead detector.  A synthetic 2-marker text using two canonical
    # inversion phrases must yield inversion >= MIN_HEADER_HITS.
    # (Also: run1=2 >= MIN_HEADER_HITS in the real v7.6 captures, proving non-vacuous.)
    _rr11401_synth_text = _fixture_assistant_text(
        "Invert, always invert — the canonical inversion move.\n\n"
        "Start by identifying the necessary precondition for success."
    )
    _rr11401_synth_parsed = [json.loads(_rr11401_synth_text)]
    _rr11401_synth_extracted = _extract_assistant_text(_rr11401_synth_parsed)
    _rr11401_synth_hits = _technique_hits(_rr11401_synth_extracted)
    _rr11401_synth_inv = _rr11401_synth_hits.get("inversion", 0)

    _rr11401_ok = (
        _rr11401_inv_counts == [2, 0, 1, 1, 1]
        and _rr11401_inv_counts[0] >= MIN_HEADER_HITS    # run1 fires (positive counter-check)
        and _rr11401_inv_pattern_count == 13             # drift guard (D-08 bump: 6→7→8→9, Phase 94; D-03 bump: 9→13, Phase 121 OCH-02)
        and _rr11401_synth_inv >= MIN_HEADER_HITS         # detector is reachable (synthetic check)
    )
    if _rr11401_ok:
        print(
            f"  RR-114-01 PASS: S-P02 inversion count vector {_rr11401_inv_counts} "
            f"== [2, 0, 1, 1, 1] (v7.6 evidence; run1={_rr11401_inv_counts[0]} "
            f">= MIN_HEADER_HITS={MIN_HEADER_HITS}; "
            f"inversion detector reachable (synthetic 2-marker text → inv_hits={_rr11401_synth_inv} "
            f">= MIN_HEADER_HITS={MIN_HEADER_HITS}); "
            f"S-P02 CARRIED 1/5 at Phase 114 re-baseline (live 1/5 < min-pass; "
            f"offline detector fires on run1 but not enough live runs to CLOSE); "
            f"inv_patterns={_rr11401_inv_pattern_count}. "
            f"Supersedes RR-108-01 (Phase 114 v7.6 carry-forward). "
            f"Chain: RR-79-02 → RR-92-01 → RR-95-01 → RR-108-01 → RR-114-01."
        )
    else:
        print(
            f"  RR-114-01 FAIL: S-P02 inversion count vector {_rr11401_inv_counts} "
            f"(expected [2, 0, 1, 1, 1] from v7.6 S-P02 captures); "
            f"inv_patterns={_rr11401_inv_pattern_count} (expected 13); "
            f"run1={_rr11401_inv_counts[0] if len(_rr11401_inv_counts) > 0 else '?'} "
            f"(must be >= MIN_HEADER_HITS={MIN_HEADER_HITS}); "
            f"synthetic 2-marker inv_hits={_rr11401_synth_inv} "
            f"(must be >= MIN_HEADER_HITS={MIN_HEADER_HITS})."
        )
        all_passed = False

    # ---------------------------------------------------------------------------
    # RR-114-01 teeth: extended inversion detector reads output-contract headers
    # (Phase 121 OCH-02, D-04 step 1 — synthetic header-bearing fixture)
    #
    # Two complementary checks prove the NEW heading-anchored markers fire:
    # (a) A header-only fixture built from the four new inversion ## headings
    #     (no old prose phrases) — _technique_hits inversion count >= MIN_HEADER_HITS.
    # (b) A single-heading check: ## Stress-Test Verdict has NO overlapping old
    #     marker, so a fixture containing only that heading gives inversion >= 1
    #     ONLY if the new Stress-Test Verdict marker exists and is correct. If the
    #     new marker is broken/removed, this check gives 0 and fails.
    #
    # Without these teeth, a no-op extension (markers never firing) would leave the
    # old-marker counts unchanged and the drift guard would still pass — the teeth
    # ensure a broken NEW marker is caught.
    # ---------------------------------------------------------------------------
    # (a) Header-only inversion fixture: all 4 D-01 output-contract headings,
    # no old prose markers (no "invert, always invert", no "necessary precondition", etc.)
    _rr11401_hdr_text = _fixture_assistant_text(
        "## Inverted Claim\n"
        "The inverted claim stated here.\n\n"
        "## Failure-Guaranteeing Conditions\n"
        "Conditions that guarantee failure.\n\n"
        "## Necessary Preconditions\n"
        "Preconditions that must hold for the claim.\n\n"
        "## Stress-Test Verdict\n"
        "Verdict after stress-testing the inversion."
    )
    _rr11401_hdr_parsed = [json.loads(_rr11401_hdr_text)]
    _rr11401_hdr_extracted = _extract_assistant_text(_rr11401_hdr_parsed)
    _rr11401_hdr_inv = _technique_hits(_rr11401_hdr_extracted).get("inversion", 0)

    # (b) Single-heading check: ## Stress-Test Verdict (no overlapping existing marker).
    # Gives inversion == 1 only via the new Stress-Test Verdict heading-anchored pattern.
    _rr11401_sv_text = _fixture_assistant_text(
        "## Stress-Test Verdict\n"
        "The stress-test verdict for this inversion."
    )
    _rr11401_sv_parsed = [json.loads(_rr11401_sv_text)]
    _rr11401_sv_extracted = _extract_assistant_text(_rr11401_sv_parsed)
    _rr11401_sv_inv = _technique_hits(_rr11401_sv_extracted).get("inversion", 0)

    _rr11401_teeth_ok = (
        _rr11401_hdr_inv >= MIN_HEADER_HITS   # (a) 4-header fixture reaches bar
        and _rr11401_sv_inv >= 1              # (b) clean anchor: Stress-Test Verdict fires
    )
    if _rr11401_teeth_ok:
        print(
            f"  RR-114-01 teeth: extended inversion detector reads output-contract headers "
            f"(4-header fixture inv_hits={_rr11401_hdr_inv} >= MIN_HEADER_HITS={MIN_HEADER_HITS}; "
            f"Stress-Test Verdict anchor fires: sv_inv={_rr11401_sv_inv} >= 1; "
            f"OCH-02 Phase 121, D-03 additive marker extension, inversion 9→13)."
        )
    else:
        print(
            f"  RR-114-01 FAIL teeth: extended inversion detector does NOT read output-contract headers "
            f"(4-header fixture inv_hits={_rr11401_hdr_inv}, expected >= {MIN_HEADER_HITS}; "
            f"Stress-Test Verdict anchor: sv_inv={_rr11401_sv_inv}, expected >= 1; "
            f"check that the new heading-anchored inversion markers are correctly compiled, "
            f"OCH-02 Phase 121 D-03)."
        )
        all_passed = False

    # ---------------------------------------------------------------------------
    # Fishbone count drift guard (Phase 117, Plan 02 — FIX-02, D-09 partial)
    #
    # The DIAG-01-prescribed FIX-01 added "candidate causes" as the 7th fishbone
    # marker (Phase 117, Plan 01, 2026-06-24; _TECHNIQUE_CATEGORIES["fishbone"]
    # grew from 6 to 7).  This drift guard locks that new count against future
    # silent regression — mirroring the pre-mortem, inversion, and trade-off
    # drift-guard idiom.  No capture-based vector is asserted (there are no
    # fishbone v7.6 excerpts in tests/step0-captures-v7.6/); this is a
    # count-only drift guard.
    # ---------------------------------------------------------------------------
    _fishbone_pattern_count = len(_TECHNIQUE_CATEGORIES["fishbone"])
    if _fishbone_pattern_count == 7:
        print(
            f"  Fishbone drift guard PASS: len(_TECHNIQUE_CATEGORIES['fishbone']) == 7 "
            f"(Phase 117 FIX-02 added 'candidate causes'; 6→7; count locked)."
        )
    else:
        print(
            f"  Fishbone drift guard FAIL: len(_TECHNIQUE_CATEGORIES['fishbone']) == "
            f"{_fishbone_pattern_count} (expected 7 after Phase 117 FIX-02 'candidate causes' "
            f"addition; fishbone drift guard added Phase 117 FIX-02, D-09 partial)."
        )
        all_passed = False

    # ---------------------------------------------------------------------------
    # RR-117-01 named honest-state sentinel — S-P03 fishbone vector (Phase 117,
    #           Plan 07 — CONF-02, D-04 step two; CLOSED at v7.7 CONF-01;
    #           re-pointed to live v7.8 CONF-03 captures Phase 119, Plan 03 — D-04 step two)
    #
    # **CLOSED: S-P03 fishbone sustained 5/5 at Phase 117 v7.7 CONF-01.**
    # This is the FIRST fishbone capture-based vector sentinel (Phase 117 Plan 02
    # added the count drift guard above; this sentinel adds the live count vector).
    # RR-117-01 mints this ID (RR-75-03 lineage — original fishbone under-routing
    # residual first tracked Phase 75; no formal vector sentinel existed until now).
    #
    # **CLOSE SUSTAINED at Phase 119 v7.8 CONF-03 (tests/step0-baseline-v7.8.md):
    # S-P03 4/5 ≥ v7.4 floor (3/5) — CLOSE confirmed out-of-sample with Phase-118
    # prose fix. One run (run1) stays below barrier; four runs clear. Per D-1b softening,
    # ≥3/5 is the no-regression floor, and 4/5 comfortably satisfies it.**
    # Sentinel re-pointed to v7.8 captures (Phase 119 CONF-04, D-04 step two).
    #
    # v7.7 CONF-01 fishbone count vector: [3, 3, 2, 2, 2] (all 5 runs clear → 5/5 PASS).
    # v7.8 CONF-03 fishbone count vector: [1, 4, 2, 2, 3]
    # (tests/step0-captures-v7.8/S-P03-run{1..5}.txt; 7-marker post-fix detector)
    #   run1: 1 marker  — stays below MIN_HEADER_HITS → full-composer on that run
    #   run2: 4 markers — clears MIN_HEADER_HITS → focused-fishbone ✓
    #   run3: 2 markers — clears MIN_HEADER_HITS → focused-fishbone ✓
    #   run4: 2 markers — clears MIN_HEADER_HITS → focused-fishbone ✓
    #   run5: 3 markers — clears MIN_HEADER_HITS → focused-fishbone ✓
    # Runs 2,3,4,5 clear the barrier → K/N = 4/5 PASS ≥ v7.4 floor.
    #
    # Drift guard: fishbone marker count must not silently change.
    # Retained as regression guard (CLOSE keeps the sentinel per RR-108-02 precedent).
    # ---------------------------------------------------------------------------
    _rr11701_fb_counts: list[int] = []
    for _run in range(1, 6):
        _text = _load_excerpt_v78("S-P03", _run)
        _hits = _technique_hits(_text)
        _rr11701_fb_counts.append(_hits.get("fishbone", 0))

    # Drift guard: fishbone marker set size must not silently grow.
    _rr11701_fb_pattern_count = len(_TECHNIQUE_CATEGORIES["fishbone"])

    # Positive counter-check: run2=4 >= MIN_HEADER_HITS proves the fishbone
    # detector CAN fire on v7.8 S-P03 text (non-vacuous; runs 2,3,4,5 clear the barrier).
    _rr11701_ok = (
        _rr11701_fb_counts == [1, 4, 2, 2, 3]
        and _rr11701_fb_counts[1] >= MIN_HEADER_HITS    # run2 fires (counter-check)
        and _rr11701_fb_counts[4] >= MIN_HEADER_HITS    # run5 fires (counter-check)
        and _rr11701_fb_pattern_count == 7              # drift guard (FIX-01 bump: 6→7)
    )
    if _rr11701_ok:
        print(
            f"  RR-117-01 PASS (CLOSED at v7.7; CLOSE SUSTAINED at v7.8): "
            f"S-P03 fishbone count vector {_rr11701_fb_counts} "
            f"== [1, 4, 2, 2, 3] (live CONF-03 v7.8 captures; 7-marker post-fix detector; "
            f"run2={_rr11701_fb_counts[1]} and run5={_rr11701_fb_counts[4]} each >= MIN_HEADER_HITS={MIN_HEADER_HITS}; "
            f"runs 2,3,4,5 clear barrier → 4/5 PASS at Phase 119 CONF-03 — CLOSE SUSTAINED (≥ v7.4 floor); "
            f"first fishbone vector sentinel; RR-75-03 lineage; Phase 119 CONF-04, D-04 step two; "
            f"retained as regression guard); fb_patterns={_rr11701_fb_pattern_count} (expected 7)."
        )
    else:
        print(
            f"  RR-117-01 FAIL: S-P03 fishbone count vector {_rr11701_fb_counts} "
            f"(expected [1, 4, 2, 2, 3]; live CONF-03 v7.8 captures); "
            f"fb_patterns={_rr11701_fb_pattern_count} (expected 7); "
            f"run2={_rr11701_fb_counts[1] if len(_rr11701_fb_counts) > 1 else '?'} "
            f"run5={_rr11701_fb_counts[4] if len(_rr11701_fb_counts) > 4 else '?'} "
            f"(each must be >= MIN_HEADER_HITS={MIN_HEADER_HITS})."
        )
        all_passed = False

    # ---------------------------------------------------------------------------
    # RR-117-02 named precision sentinel — S-N03 genuinely-oblique negative
    #           (Phase 117, Plan 07 — CONF-02, D-17 precision finding;
    #            re-pointed to live v7.8 CONF-03 captures Phase 119, Plan 03 — D-04 step two)
    #
    # S-N03 is the one truly-oblique negative: a Python debugging prompt that the
    # live agent correctly does NOT route to focused pre-mortem.  S-N01, S-N02, and
    # S-N04 all over-route because they are semantically pre-mortem (D-17 transcript
    # evidence: "surface every way this could blow up" / "figure out everything that
    # would make it go wrong"). S-N03 over-routes on ZERO runs → the all-zero vector
    # is the clean precision signal.
    #
    # This sentinel locks the D-17 precision finding: the FIX-01 detector
    # recalibration + Phase-118 prose fix did NOT hurt routing on genuinely-unrelated
    # prompts. S-N03 stays full-composer on all 5 live v7.8 CONF-03 runs.
    #
    # v7.7 CONF-01 S-N03 pre-mortem count vector: [0, 0, 0, 0, 0] (5/5 PASS).
    # v7.8 CONF-03 S-N03 pre-mortem count vector: [1, 0, 0, 0, 0]
    # (tests/step0-captures-v7.8/S-N03-run{1..5}.txt; 9-marker post-fix detector)
    # All 5 runs stay below MIN_HEADER_HITS → full-composer 5/5.
    # (run1 has 1 marker but stays below the MIN_HEADER_HITS=2 barrier.)
    #
    # Drift guard: pre-mortem marker count must not silently grow (reuses
    # _rr7901_pm_pattern_count == 9 established above — any drift already fails
    # RR-79-01's drift guard, so no second explicit check is needed here; the
    # positive counter-check makes this non-vacuous via the known-firing runs).
    # Positive counter-check (from RR-79-01): the S-P01 v7.8 captures produce ≥2
    # markers on run2, proving the detector IS reachable — the S-N03 all-below-MIN
    # result is therefore a genuine clean negative, not a dead detector.
    # ---------------------------------------------------------------------------
    _rr11702_sn03_counts: list[int] = []
    for _run in range(1, 6):
        _text = _load_excerpt_v78("S-N03", _run)
        _hits = _technique_hits(_text)
        _rr11702_sn03_counts.append(_hits.get("pre-mortem", 0))

    # Positive counter-check: use the S-P01 run2 excerpt (already computed above
    # in _rr7901_counts) to prove the 9-marker detector IS reachable — the S-N03
    # all-below-MIN result is therefore a genuine clean negative, not a dead detector.
    _rr11702_sp01_run2_pm = _rr7901_counts[1]  # from the RR-79-01 assertion above

    _rr11702_ok = (
        _rr11702_sn03_counts == [1, 0, 0, 0, 0]
        and all(c < MIN_HEADER_HITS for c in _rr11702_sn03_counts)  # no run clears barrier
        and _rr11702_sp01_run2_pm >= MIN_HEADER_HITS                # detector reachable (non-vacuous)
    )
    if _rr11702_ok:
        print(
            f"  RR-117-02 PASS: S-N03 pre-mortem count vector {_rr11702_sn03_counts} "
            f"== [1, 0, 0, 0, 0] (live CONF-03 v7.8 captures; 9-marker post-fix detector; "
            f"all runs stay below MIN_HEADER_HITS={MIN_HEADER_HITS} → full-composer 5/5; "
            f"precision signal: FIX-01+FIX-03/FIX-04 did NOT hurt routing on genuinely-oblique prompts; "
            f"detector is reachable (S-P01 run2 fires pm={_rr11702_sp01_run2_pm} >= MIN — non-vacuous); "
            f"D-17 precision finding sustained; Phase 119 CONF-04, re-pointed to v7.8)."
        )
    else:
        print(
            f"  RR-117-02 FAIL: S-N03 pre-mortem count vector {_rr11702_sn03_counts} "
            f"(expected [1, 0, 0, 0, 0]; live CONF-03 v7.8 captures); "
            f"some run cleared MIN_HEADER_HITS={MIN_HEADER_HITS} — precision regression; "
            f"S-P01 run2 pm={_rr11702_sp01_run2_pm} (must be >= MIN to prove non-vacuous)."
        )
        all_passed = False

    # ---------------------------------------------------------------------------
    # RR-119-01 named honest-state sentinel — S-N01 over-routing resolved (Phase 119,
    #           Plan 03 — CONF-04; minted for the S-N01 over-routing row resolved over
    #           the bar at Phase 119 CONF-03 with the Phase-118 FIX-03/FIX-04 prose fix)
    #
    # **RR-119-01 MINTED: S-N01 over-routing resolved-over-bar at Phase 119 CONF-03.**
    # S-N01 is an oblique negative (blocking): an oblique prompt that uses risk-framing
    # language ("everything that could go wrong") without naming a plan or explicit
    # pre-mortem context. At v7.7, S-N01 over-routed to focused-pre-mortem on all 5
    # runs (0/5 full-composer). The Phase-118 FIX-03 negative-match guard column +
    # FIX-04 stay-in-composer tiebreaker moved it over the bar at v7.8 (3/5 PASS).
    #
    # Residual disposition: RESOLVED-OVER-BAR with the detector-under-count caveat
    # documented (D-01): the negative "passes" are a MIX of genuine clarification-holds
    # (S-N01-run1, S-N01-run3 — agent held for the plan) and detector under-counts
    # where fewer than MIN_HEADER_HITS=2 markers landed in the summary text even though
    # the agent may have engaged pre-mortem framing (the same phenomenon flagged in
    # the v7.7 baseline for S-N02/S-N04). The pass rate is a lower bound on
    # stay-in-composer behavior. NOT a reclassification (D-4: the out-of-scope
    # NON_BLOCKING_NEGATIVE_IDS addition is deferred).
    #
    # v7.8 CONF-03 S-N01 pre-mortem count vector: [0, 2, 1, 1, 3]
    # (tests/step0-captures-v7.8/S-N01-run{1..5}.txt; 9-marker post-fix detector)
    #   run1: 0 markers — stays below MIN_HEADER_HITS → full-composer ✓
    #   run2: 2 markers — clears MIN_HEADER_HITS → over-routes (focused-pre-mortem on that run)
    #   run3: 1 marker  — stays below MIN_HEADER_HITS → full-composer ✓
    #   run4: 1 marker  — stays below MIN_HEADER_HITS → full-composer ✓
    #   run5: 3 markers — clears MIN_HEADER_HITS → over-routes (focused-pre-mortem on that run)
    # Runs 1,3,4 stay below → full-composer 3/5 PASS. Over-routes on runs 2,5 (2/5).
    # ---------------------------------------------------------------------------
    _rr11901_sn01_counts: list[int] = []
    for _run in range(1, 6):
        _text = _load_excerpt_v78("S-N01", _run)
        _hits = _technique_hits(_text)
        _rr11901_sn01_counts.append(_hits.get("pre-mortem", 0))

    # Positive counter-check: run2=2 >= MIN_HEADER_HITS proves the detector CAN fire
    # on S-N01 text — the 3/5 result is a genuine partial-pass, not a dead detector.
    _rr11901_ok = (
        _rr11901_sn01_counts == [0, 2, 1, 1, 3]
        and _rr11901_sn01_counts[1] >= MIN_HEADER_HITS    # run2 over-routes (counter-check, non-vacuous)
        and _rr7901_pm_pattern_count == 9                 # drift guard (reuses RR-79-01 guard above)
    )
    if _rr11901_ok:
        print(
            f"  RR-119-01 PASS: S-N01 pre-mortem count vector {_rr11901_sn01_counts} "
            f"== [0, 2, 1, 1, 3] (live CONF-03 v7.8 captures; 9-marker post-fix detector; "
            f"run2={_rr11901_sn01_counts[1]} >= MIN_HEADER_HITS={MIN_HEADER_HITS} (over-routes, non-vacuous); "
            f"runs 1,3,4 stay below → full-composer 3/5 PASS; over-routes on runs 2,5 (2/5); "
            f"S-N01 RESOLVED-OVER-BAR (Phase 119 CONF-03; Phase-118 FIX-03/FIX-04 prose fix); "
            f"under-count caveat: negative passes are a MIX of genuine clarification-holds (D-01); "
            f"NOT a reclassification (D-4); pm_patterns={_rr7901_pm_pattern_count} (expected 9)."
        )
    else:
        print(
            f"  RR-119-01 FAIL: S-N01 pre-mortem count vector {_rr11901_sn01_counts} "
            f"(expected [0, 2, 1, 1, 3]; live CONF-03 v7.8 captures); "
            f"pm_patterns={_rr7901_pm_pattern_count} (expected 9); "
            f"run2={_rr11901_sn01_counts[1] if len(_rr11901_sn01_counts) > 1 else '?'} "
            f"(must be >= MIN_HEADER_HITS={MIN_HEADER_HITS})."
        )
        all_passed = False

    # ---------------------------------------------------------------------------
    # RR-119-02 named honest-state sentinel — S-N02 over-routing resolved (Phase 119,
    #           Plan 03 — CONF-04; minted for the S-N02 over-routing row resolved over
    #           the bar at Phase 119 CONF-03 with the Phase-118 FIX-03/FIX-04 prose fix)
    #
    # **RR-119-02 MINTED: S-N02 over-routing resolved-over-bar at Phase 119 CONF-03.**
    # S-N02 is an oblique negative (blocking): an oblique prompt using failure-framing
    # language without an explicit plan context. At v7.7, S-N02 over-routed to
    # focused-pre-mortem on 3 of 5 runs (2/5 full-composer FAIL). The Phase-118 prose
    # fix moved it over the bar at v7.8 (3/5 PASS).
    #
    # Residual disposition: RESOLVED-OVER-BAR with the detector-under-count caveat
    # documented (D-01): runs 2 and 3 have counts ≥ MIN_HEADER_HITS (over-route runs),
    # yet transcript inspection shows "the first-principles agent ran a pre-mortem on
    # your migration" with fewer than 2 canonical markers in the summary text — the
    # same detector under-count phenomenon flagged in the v7.7 baseline. The pass rate
    # is a lower bound on stay-in-composer behavior. NOT a reclassification (D-4).
    #
    # v7.8 CONF-03 S-N02 pre-mortem count vector: [0, 3, 3, 1, 1]
    # (tests/step0-captures-v7.8/S-N02-run{1..5}.txt; 9-marker post-fix detector)
    #   run1: 0 markers — stays below MIN_HEADER_HITS → full-composer ✓
    #   run2: 3 markers — clears MIN_HEADER_HITS → over-routes (focused-pre-mortem on that run)
    #   run3: 3 markers — clears MIN_HEADER_HITS → over-routes (focused-pre-mortem on that run)
    #   run4: 1 marker  — stays below MIN_HEADER_HITS → full-composer ✓
    #   run5: 1 marker  — stays below MIN_HEADER_HITS → full-composer ✓
    # Runs 1,4,5 stay below → full-composer 3/5 PASS. Over-routes on runs 2,3 (2/5).
    # Note: runs 2,3 are detector under-counts (agent ran a pre-mortem but summary
    # had ≥ MIN_HEADER_HITS markers — the SAME runs score as "over-routes" by the
    # detector, illustrating that S-N02's pass rate is a lower bound on stay-in-composer).
    # ---------------------------------------------------------------------------
    _rr11902_sn02_counts: list[int] = []
    for _run in range(1, 6):
        _text = _load_excerpt_v78("S-N02", _run)
        _hits = _technique_hits(_text)
        _rr11902_sn02_counts.append(_hits.get("pre-mortem", 0))

    # Positive counter-check: run2=3 >= MIN_HEADER_HITS proves the detector CAN fire
    # on S-N02 text — the 3/5 result is a genuine partial-pass, not a dead detector.
    _rr11902_ok = (
        _rr11902_sn02_counts == [0, 3, 3, 1, 1]
        and _rr11902_sn02_counts[1] >= MIN_HEADER_HITS    # run2 over-routes (counter-check, non-vacuous)
        and _rr7901_pm_pattern_count == 9                 # drift guard (reuses RR-79-01 guard above)
    )
    if _rr11902_ok:
        print(
            f"  RR-119-02 PASS: S-N02 pre-mortem count vector {_rr11902_sn02_counts} "
            f"== [0, 3, 3, 1, 1] (live CONF-03 v7.8 captures; 9-marker post-fix detector; "
            f"run2={_rr11902_sn02_counts[1]} >= MIN_HEADER_HITS={MIN_HEADER_HITS} (over-routes, non-vacuous); "
            f"runs 1,4,5 stay below → full-composer 3/5 PASS; over-routes on runs 2,3 (2/5); "
            f"S-N02 RESOLVED-OVER-BAR (Phase 119 CONF-03; Phase-118 FIX-03/FIX-04 prose fix); "
            f"under-count caveat: runs 2,3 are detector under-counts where agent ran a pre-mortem (D-01); "
            f"NOT a reclassification (D-4); pm_patterns={_rr7901_pm_pattern_count} (expected 9)."
        )
    else:
        print(
            f"  RR-119-02 FAIL: S-N02 pre-mortem count vector {_rr11902_sn02_counts} "
            f"(expected [0, 3, 3, 1, 1]; live CONF-03 v7.8 captures); "
            f"pm_patterns={_rr7901_pm_pattern_count} (expected 9); "
            f"run2={_rr11902_sn02_counts[1] if len(_rr11902_sn02_counts) > 1 else '?'} "
            f"(must be >= MIN_HEADER_HITS={MIN_HEADER_HITS})."
        )
        all_passed = False

    # ---------------------------------------------------------------------------
    # RR-108-02 named honest-state sentinel (Phase 108, Plan 02)
    # RR-108-02 supersedes RR-95-02 (Phase 108 v7.4 carry-forward, S-P05 trade-off)
    # Supersession chain: RR-79-03 → RR-92-02 → RR-95-02 → RR-108-02
    #
    # RR-108-02 is the S-P05 trade-off residual: observed 4/5 PASS in the Phase 114
    # v7.6 live re-baseline (tests/step0-baseline-v7.6.md) → **CLOSED** at >= min-pass
    # (the ≥3/5 close bar is met).  The live agent routes to focused-trade-off on runs
    # 1-4; only run5 returns full-composer.  v7.6 is 4/5 — improved from v7.4's 2/5
    # (the lone canonical improver this re-baseline).  CLOSE keeps the RR-108-02 ID
    # (no new RR-114-NN minted on a close, D-04); this honest-state sentinel is
    # re-pointed to v7.6 evidence and asserts the documented v7.6 count vector
    # (honesty-not-score, D-01), NOT the live pass rate.
    #
    # On v7.6 evidence the offline detector clears MIN_HEADER_HITS on runs 1-4
    # (count 2 each); run5 fires only 1 (below MIN).  The two-distinct-marker barrier
    # is cleared on 4/5 runs, coherent with the live 4/5 focused-trade-off PASS.
    #
    # Note: "trade-off analysis" is a DOCUMENTED ACCEPTED MEMBER of
    # _TECHNIQUE_CATEGORIES["trade-off"] (added Phase 94 Plan 03).  The
    # REJECTED CANDIDATES note (Pitfall 6) refers to "weighted score" staying out.
    #
    # Supersession comment for old IDs:
    #   RR-79-03 → RR-92-02 (renamed Phase 93 Plan 01; S-P05 trade-off;
    #   re-pointed from v5.2 all-below-MIN to v6.3 vector [0, 2, 2, 1, 0])
    #   RR-92-02 → RR-95-02 (renamed Phase 96 Plan 02; re-pointed to v6.4
    #   vector [1, 2, 2, 1, 1]; Phase 95 v6.4 carry-forward, S-P05 trade-off)
    #   RR-95-02 → RR-108-02 (renamed Phase 108 Plan 02; re-pointed to v7.4
    #   vector [1, 1, 2, 2, 0]; Phase 108 v7.4 carry-forward, S-P05 trade-off 2/5)
    #   RR-108-02 CLOSED Phase 114 Plan 02 (re-pointed to v7.6 vector [2, 2, 2, 2, 1];
    #   S-P05 trade-off 4/5 PASS ≥ min-pass — residual resolved, no successor ID)
    # ---------------------------------------------------------------------------
    _rr10802_to_counts: list[int] = []
    for _run in range(1, 6):
        _text = _load_excerpt_v76("S-P05", _run)
        _hits = _technique_hits(_text)
        _rr10802_to_counts.append(_hits.get("trade-off", 0))

    # Drift guard (WR-02): trade-off canonical marker set must not silently grow.
    # A new trade-off pattern could alter the v7.4 count vector —
    # fail loudly so the sentinel is updated with verified new per-run counts.
    # D-08 bump: 4 → 5 after adding "weighted scoring" (CR-01/WR-01/WR-02 fix removed
    # the overlapping "scoring matrix" and the broad "sensitivity analysis"; one marker added).
    # D-08 bump: 5 → 6 after adding "trade-off analysis" (Phase 94, Plan 03, 2026-06-17).
    # D-03 bump: 6 → 10 (4 output-contract header markers, Phase 121 OCH-02, 2026-06-26).
    _rr10802_to_pattern_count = len(_TECHNIQUE_CATEGORIES["trade-off"])
    if _rr10802_to_pattern_count != 10:
        print(
            f"  RR-108-02 FAIL: trade-off pattern count drifted "
            f"(expected 10, got {_rr10802_to_pattern_count}) — update sentinel "
            f"after verifying new per-run trade-off counts over S-P05-run1..5 (v7.6)."
        )
        all_passed = False

    # Positive counter-check (WR-01): runs 1 and 2 each clear MIN_HEADER_HITS
    # on v7.6 evidence (count 2 each: two trade-off markers co-fire on those runs).
    _rr10802_ok = (
        _rr10802_to_counts == [2, 2, 2, 2, 1]
        and _rr10802_to_counts[0] >= MIN_HEADER_HITS    # run1 fires (positive counter-check)
        and _rr10802_to_counts[1] >= MIN_HEADER_HITS    # run2 fires (positive counter-check)
        and _rr10802_to_pattern_count == 10             # drift guard (D-08 bump: 4→5→6, Phase 94; D-03 bump: 6→10, Phase 121 OCH-02)
    )
    if _rr10802_ok:
        print(
            f"  RR-108-02 PASS: S-P05 trade-off count vector {_rr10802_to_counts} "
            f"== [2, 2, 2, 2, 1] (v7.6 evidence; "
            f"run1={_rr10802_to_counts[0]}, run2={_rr10802_to_counts[1]} "
            f"each >= MIN_HEADER_HITS={MIN_HEADER_HITS}; "
            f"S-P05 CLOSED at 4/5 PASS at Phase 114 re-baseline (live 4/5 >= min-pass; "
            f"improved from v7.4's 2/5 — residual resolved, no successor ID); "
            f"to_patterns={_rr10802_to_pattern_count}. "
            f"Chain CLOSED: RR-79-03 → RR-92-02 → RR-95-02 → RR-108-02 → CLOSED."
        )
    else:
        _offending_to = [
            f"run{i+1}={c}" for i, c in enumerate(_rr10802_to_counts)
            if (i == 0 and c != 2) or (i == 1 and c != 2) or (i == 2 and c != 2)
            or (i == 3 and c != 2) or (i == 4 and c != 1)
        ]
        _offending_to_str = ", ".join(_offending_to) if _offending_to else "none"
        print(
            f"  RR-108-02 FAIL: S-P05 trade-off count vector {_rr10802_to_counts} "
            f"(expected [2, 2, 2, 2, 1] from v7.6 S-P05 captures; "
            f"offending: {_offending_to_str}); "
            f"to_patterns={_rr10802_to_pattern_count} (expected 10); "
            f"run1={_rr10802_to_counts[0] if len(_rr10802_to_counts) > 0 else '?'} "
            f"run2={_rr10802_to_counts[1] if len(_rr10802_to_counts) > 1 else '?'} "
            f"(each must be >= MIN_HEADER_HITS={MIN_HEADER_HITS})."
        )
        all_passed = False

    # ---------------------------------------------------------------------------
    # RR-108-02 teeth: extended trade-off detector reads output-contract headers
    # (Phase 121 OCH-02, D-04 step 1 — synthetic header-bearing fixture)
    #
    # A header-only fixture built from the four new trade-off ## headings (no old
    # prose markers). None of the four headers overlap any existing trade-off marker:
    #   "## Options"         — no existing marker fires on this heading
    #   "## Criteria & Weights" — no existing marker fires on this heading
    #   "## Scoring"         — "weighted scoring" requires "weighted" prefix, doesn't fire
    #   "## Recommendation"  — no existing marker fires on this heading
    # Therefore the fixture reaches MIN_HEADER_HITS ONLY via the new heading-anchored
    # markers. A broken/removed new marker reduces the hit count; breaking two or more
    # drops it below MIN_HEADER_HITS=2 and fails this assertion.
    # (This contrasts with the inversion case where old prose markers overlap 3 of 4
    # headers; here ALL 4 headers are clean non-overlapping — genuine trade-off teeth.)
    # ---------------------------------------------------------------------------
    _rr10802_hdr_text = _fixture_assistant_text(
        "## Options\n"
        "The available options under consideration.\n\n"
        "## Criteria & Weights\n"
        "Criteria and their assigned weights.\n\n"
        "## Scoring\n"
        "Option scores against each criterion.\n\n"
        "## Recommendation\n"
        "The recommended option and rationale."
    )
    _rr10802_hdr_parsed = [json.loads(_rr10802_hdr_text)]
    _rr10802_hdr_extracted = _extract_assistant_text(_rr10802_hdr_parsed)
    _rr10802_hdr_to = _technique_hits(_rr10802_hdr_extracted).get("trade-off", 0)

    _rr10802_teeth_ok = _rr10802_hdr_to >= MIN_HEADER_HITS
    if _rr10802_teeth_ok:
        print(
            f"  RR-108-02 teeth: extended trade-off detector reads output-contract headers "
            f"(4-header fixture to_hits={_rr10802_hdr_to} >= MIN_HEADER_HITS={MIN_HEADER_HITS}; "
            f"all 4 trade-off headers non-overlapping → reaching bar requires new markers; "
            f"OCH-02 Phase 121, D-03 additive marker extension, trade-off 6→10)."
        )
    else:
        print(
            f"  RR-108-02 FAIL teeth: extended trade-off detector does NOT read output-contract headers "
            f"(4-header fixture to_hits={_rr10802_hdr_to}, expected >= {MIN_HEADER_HITS}; "
            f"check that the new heading-anchored trade-off markers are correctly compiled, "
            f"OCH-02 Phase 121 D-03)."
        )
        all_passed = False

    # ---------------------------------------------------------------------------
    # RR-108-03 / RR-108-04 / RR-108-05 named first-time new-technique sentinels
    # (Phase 108, Plan 02 — D-03a/D-04a)
    #
    # These three rows are the FIRST-EVER live measurements of the three Tier-1
    # techniques added in v7.1/v7.2/v7.3:
    #   RR-108-03 — S-P09 decompose         (added v7.1)
    #   RR-108-04 — S-P10 estimate          (added v7.2)
    #   RR-108-05 — S-P14 theoretical-limit (added v7.3)
    # All three carried forward at 0/5 in the Phase 108 v7.4 re-baseline
    # (tests/step0-baseline-v7.4.md). No supersession (never measured before, D-03a).
    #
    # CRITICAL: the frozen detector `_TECHNIQUE_CATEGORIES` has NO category for
    # decompose / estimate / theoretical-limit (it tracks only the 6 original
    # techniques). So _technique_hits returns 0 for these techniques by construction;
    # the live focused-routing for them happens entirely in the agent body's Step 0
    # phrase-detection, which these rows show did NOT fire (all runs routed to
    # full-composer or returned the spend-limit `none` message). The honest offline
    # sentinel therefore asserts (a) the documented composer-structure-hit vector
    # over the frozen v7.4 excerpts, and (b) that NO original-technique focused mode
    # fired on any run (sum of all 6 technique hits == 0 per run) — i.e. the row is
    # genuinely a non-focused-technique carry, not a masked pass.
    #
    # Documented v7.4 composer-structure vectors (recomputed from the frozen
    # tests/step0-captures-v7.4/ excerpts):
    #   S-P09 decompose         composer = [1, 0, 1, 1, 1]  (5 full-composer dispatches)
    #   S-P10 estimate          composer = [0, 0, 0, 0, 0]  (runs 1-4 full-composer, run5 spend-limit none)
    #   S-P14 theoretical-limit composer = [0, 0, 0, 0, 0]  (all 5 runs spend-limit none)
    # ---------------------------------------------------------------------------
    # NOTE (Phase 111): RR-108-03 (S-P09 decompose) is resolved-by-merge — the
    # decompose technique was merged into five-whys in Phase 110 and the S-P09
    # catalog row was removed + re-homed onto S-P16/S-N08 in Phase 111; this
    # honest-state sentinel is LEFT as a historical v7.4 record (formal
    # RR-108-03 traceability resolution is Phase 112). The vector [1, 0, 1, 1, 1]
    # is frozen-capture data read from tests/step0-captures-v7.4/ via
    # _load_excerpt_v74 — it does NOT look up the live catalog, so removing the
    # S-P09 catalog row does NOT affect BATT-06.
    _NEW_TECH_SENTINELS = (
        ("RR-108-03", "S-P09", "decompose", [1, 0, 1, 1, 1]),
        ("RR-108-04", "S-P10", "estimate", [0, 0, 0, 0, 0]),
        ("RR-108-05", "S-P14", "theoretical-limit", [0, 0, 0, 0, 0]),
    )
    for _rr_id, _row_id, _tech_name, _expected_comp in _NEW_TECH_SENTINELS:
        _comp_counts: list[int] = []
        _focused_tech_sums: list[int] = []
        for _run in range(1, 6):
            _text = _load_excerpt_v74(_row_id, _run)
            _comp_counts.append(_composer_structure_hits(_text))
            _focused_tech_sums.append(sum(_technique_hits(_text).values()))
        # Honest carry assertion: the documented composer vector matches AND no
        # ORIGINAL-technique focused mode fired on any run (the row is a genuine
        # 0/5 carry, not a masked focused pass). The detector has no category for
        # this technique, so its focused mode can only come from the agent body —
        # which did not route here on any run.
        _new_ok = (
            _comp_counts == _expected_comp
            and all(s == 0 for s in _focused_tech_sums)
        )
        if _new_ok:
            print(
                f"  {_rr_id} PASS: S-{_row_id[2:]} {_tech_name} first-ever live "
                f"measurement CARRIED 0/5 at Phase 108 re-baseline; v7.4 "
                f"composer-structure vector {_comp_counts} == {_expected_comp}; "
                f"no original-technique focused mode fired on any run "
                f"(per-run technique-hit sums {_focused_tech_sums} all 0 — honest "
                f"non-focused carry, not masked). First-time ID (no supersession, D-03a)."
            )
        else:
            print(
                f"  {_rr_id} FAIL: S-{_row_id[2:]} {_tech_name} v7.4 composer vector "
                f"{_comp_counts} (expected {_expected_comp}); per-run technique-hit "
                f"sums {_focused_tech_sums} (expected all 0)."
            )
            all_passed = False

    # ---------------------------------------------------------------------------
    # RR-77-08 named anti-masking boundary sentinel (Phase 85, Plan 02)
    #
    # RR-77-08 is the _COMPOSER_FOCUS_CEILING=4 calibration lock: a legitimate
    # single-technique (n==1) focused pre-mortem output that also contains
    # incidental composer-structure headers (Ground Truths + Derivation Chains +
    # Verdict) yields composer_hits=3 and must still classify `focused-pre-mortem`,
    # NOT `full-composer`.
    #
    # This is a LOCK-ONLY sentinel (D-05): no production code change.  Research
    # confirmed that the adversarial fixture below classifies correctly at CEILING=4
    # (no current misclassification); refining `_composer_structure_hits` would only
    # be warranted if the fixture surfaced a real regression — it does not.
    #
    # Adversarial fixture: a pre-mortem-dominant output (3 distinct pre-mortem
    # markers: `already failed` + `Working backward` + `# Pre-Mortem` heading)
    # with three incidental composer-structure headers (Ground Truths + Derivation
    # Chains + Verdict) mixed in.  composer_hits=3 because Assumption Audit is
    # absent.  At CEILING=4: 3 < 4 → n==1 branch fires → focused-pre-mortem
    # (correct).  At a hypothetical CEILING=3: 3 >= 3 → n==1 suppressed →
    # full-composer (regression!).
    # ---------------------------------------------------------------------------
    _rr7708_adv_text = (
        "## Pre-Mortem: Deployment Risk Analysis\n\n"
        "Imagine the deployment has already failed. What caused it?\n\n"
        "Working backward from the failure, we identify these risks:\n\n"
        "## Ground Truths\n"
        "Fact: the system handles 2k requests per second at peak.\n\n"
        "## Derivation Chains\n"
        "Each risk traces back to the facts above.\n\n"
        "## Verdict\n"
        "Proceed with staged rollout, addressing each risk."
    )
    _rr7708_text = _fixture_assistant_text(_rr7708_adv_text)
    _rr7708_parsed = [json.loads(_rr7708_text)]
    _rr7708_extracted = _extract_assistant_text(_rr7708_parsed)
    _rr7708_hits = _technique_hits(_rr7708_extracted)
    _rr7708_fired = {t for t, c in _rr7708_hits.items() if c >= MIN_HEADER_HITS}
    _rr7708_composer = _composer_structure_hits(_rr7708_extracted)
    _rr7708_result = classify(_rr7708_fired, _rr7708_composer)

    # Positive counter-check (WR-01 / C-04): prove CEILING=4 is load-bearing.
    # composer_hits == 3 == CEILING - 1, meaning at a hypothetical CEILING=3 the
    # n==1 early-return would be suppressed (3 >= 3) and classify() would return
    # full-composer — a regression.  Asserting composer == CEILING - 1 makes the
    # "correct at CEILING=4" clause non-vacuous.
    _rr7708_assertions_ok = (
        _COMPOSER_FOCUS_CEILING == 4                              # literal drift guard
        and _rr7708_composer == 3                                 # exact composer hits
        and _rr7708_fired == {"pre-mortem"}                       # exactly n==1
        and _rr7708_result == "focused-pre-mortem"                # correct at CEILING=4
        and _rr7708_composer == _COMPOSER_FOCUS_CEILING - 1       # load-bearing check
    )
    if _rr7708_assertions_ok:
        print(
            f"  RR-77-08 PASS: _COMPOSER_FOCUS_CEILING={_COMPOSER_FOCUS_CEILING} "
            f"is load-bearing; adversarial fixture composer_hits={_rr7708_composer} "
            f"== CEILING-1; fired={_rr7708_fired}; "
            f"classify() returned '{_rr7708_result}' (correct at CEILING=4; "
            f"would flip to 'full-composer' at hypothetical CEILING=3)."
        )
    else:
        print(
            f"  RR-77-08 FAIL: _COMPOSER_FOCUS_CEILING={_COMPOSER_FOCUS_CEILING} "
            f"(expected 4); composer_hits={_rr7708_composer} (expected 3); "
            f"fired={_rr7708_fired} (expected {{'pre-mortem'}}); "
            f"result='{_rr7708_result}' (expected 'focused-pre-mortem'); "
            f"composer == CEILING-1: {_rr7708_composer} == {_COMPOSER_FOCUS_CEILING - 1}."
        )
        all_passed = False

    if all_passed:
        print(f"self-test PASS (8 fixtures + RR-80-01 [v7.8] + RR-79-01 [CLOSED v7.7; SUSTAINED v7.8] + RR-114-01 + RR-114-01 teeth [OCH-02 inversion 9→13] + RR-108-02 + RR-108-02 teeth [OCH-02 trade-off 6→10] + RR-108-03 + RR-108-04 + RR-108-05 + RR-77-08 + RR-117-01 [S-P03 fishbone; SUSTAINED v7.8] + RR-117-02 [S-N03 precision; v7.8] + RR-119-01 [S-N01 RESOLVED-OVER-BAR v7.8] + RR-119-02 [S-N02 RESOLVED-OVER-BAR v7.8] named assertions)")
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
        # v6.3 capture-backed: S-P01-run4 output includes "fix forward under fire" and
        # "rollback = fix-forward" framing — the agent uses "fix forward" to describe the
        # consequence of an irreversible big-bang cutover. S-P01-run1 also contains the
        # literal phrase "fix forward" ("the only option is 'fix forward'"); the regex
        # matches that literal, not a "fix it first" variant. v5.2 S-P01 run1..5 all clean.
        # Source: tests/step0-captures-v6.3/S-P01-run4.txt (capture date: 2026-06-16)
        # False-positive guard: "fix forward" is idiomatic to incident-response/rollback
        # engineering; does NOT appear in the RR-80-01 one-hit S-N04 test text (confirmed)
        # nor in any S-N04 v6.3 capture (all 5 clean). MIN_HEADER_HITS=2 ensures this
        # alone cannot fire pre-mortem without a second distinct pre-mortem marker.
        re.compile(r"fix[\s-]?forward\b", re.IGNORECASE),
        # v7.6 capture-backed: "structural weakness(es)" fires across all 5 v7.6 S-P01 runs
        # (confirmed by marker re-score over tests/step0-captures-v7.6/S-P01-run{1..5}.txt).
        # In run3 it supplies the needed 2nd marker (run3 already has the Pre-Mortem heading
        # from pattern #4; structural-weakness gives the second distinct hit).
        # In run1 it supplies the only marker (combined with failure-chain below, gives 2 hits
        # → PASS on run1). False-positive guard: fires in S-N04-run2 but S-N04-run2 already
        # has 2 pre-mortem markers (adding a 3rd changes count but not firing outcome).
        # S-N04-run1 fires SW but has 0 pre-existing markers → new count = 1 < 2 → SAFE.
        # FIX-01, Phase 117, D-03 fence: additive only, pre-mortem 7→9 markers.
        re.compile(r"\bstructural weakness(es)?\b", re.IGNORECASE),
        # v7.6 capture-backed: "## The four failure chains" frame fires in S-P01-run1 only
        # (tests/step0-captures-v7.6/S-P01-run1.txt). Combined with structural-weakness
        # (also fires in run1), this gives run1 exactly 2 distinct pre-mortem markers → PASS.
        # Not present in S-P03 fishbone outputs or S-N04 negative controls.
        # FIX-01, Phase 117, D-03 fence: additive only, pre-mortem 7→9 markers.
        re.compile(r"\bfailure\s+chains?\b", re.IGNORECASE),
        #
        # v5.2 CARRY-FORWARD (DET-13 / RR-79-01): Extended grep over all 5 S-P01
        # v5.2 captures (.planning/v5.2-inputs/rebase-evidence/S-P01-run1..5.jsonl)
        # found no phrase clearing the D-08 all-5-present + S-N-absent bar.
        # Per-run distinct technique-hit counts:
        #   run1=0 (free-form "Bottom line" executive framing; no Pre-Mortem header,
        #           no "already failed", no "working backward", no "failure causes")
        #   run2=1 (# Pre-Mortem header only; no second distinct marker)
        #   run3=2 (# Pre-Mortem + "already failed Saturday morning") → PASS
        #   run4=1 (# Pre-Mortem appears twice but counts as 1 distinct hit; no second)
        #   run5=3 (# Pre-Mortem + "already failed" + "working backward") → PASS
        # Observed score: 2/5. Run 1 is the blocking constraint: it uses free-form
        # executive framing with no technique markers at all — any new marker must
        # appear in run 1 to clear the all-5 bar, but run 1 contains only engineering
        # recommendations (big-bang, canary, rollback, Friday).
        #
        # Candidate phrases tested and disqualified:
        #   "structural weakness": run1=0, run2=1, run3=0, run4=1, run5=1 → 3/5 AND S-N=4
        #   "failure mode":        run1=0, run2=1, run3=1, run4=2, run5=0 → 3/5 AND S-N=12
        #   "staged rollout":      run1=0, run2=1, run3=1, run4=1, run5=1 → 4/5 (misses run1)
        #   "friday" (context-specific): 5/5 but not a technique marker (prompt-specific)
        #   "blast radius":        v5.2 S-P01-run1 FIRES → REJECT (breaks [0,1,2,1,3] vector)
        # No phrase passes both the all-5 bar and the S-N-absent bar. No new marker added.
        # Honest observed score: 2/5. Phase 80 live re-baseline will record the true K/N.
        #
        # v6.3 CARRY-FORWARD (REARCH-02 / RR-79-01): S-P01-run2 (failing) contains
        # "# Pre-Mortem: Payments-Rewrite Big-Bang Cutover" (1 distinct) and "blast
        # radius" (D-09 rejected — fires v5.2 S-P01-run1) but no safe second marker.
        # Per-run v6.3 captured modes: run1=focused-pre-mortem (pass), run2=full-composer
        # (FAIL — 1 distinct), run3=focused-pre-mortem (pass), run4=focused-pre-mortem
        # (pass via fix-forward), run5=focused-pre-mortem (pass).
        # Diagnosis: DETECTOR FALSE-NEGATIVE on run2 — safe 2nd marker not available.
        # Carried into Phase 92 as honest carry-forward.
        # Source: tests/step0-captures-v6.3/S-P01-run2.txt (2026-06-16).
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
        # v6.3 capture-backed: S-P02 output expresses the inversion result as a
        # conditional — "When the assumption breaks down" (run3 header), "the assumption
        # breaks down". A SINGLE "assumption breaks down" marker (CR-01 fix, Phase 91-02
        # code review): the earlier sibling "when the assumption breaks" pattern was
        # REMOVED because it is a substring of this phrase — both fired on the same single
        # span ("when the assumption breaks down"), double-counting one phrase to
        # inversion=2 and defeating the distinct-marker corroboration invariant
        # (a second DIFFERENT phrase must corroborate). This marker counts once; a
        # genuinely different inversion marker (e.g. "inverted claim") must co-fire to
        # reach MIN_HEADER_HITS=2.
        # Source: tests/step0-captures-v6.3/S-P02-run3.txt (capture date: 2026-06-16)
        # False-positive guard: requires the "assumption breaks down" sequence; not
        # present in any S-N04 v6.3 capture (all 5 clean); tighter than bare "breaks down"
        # (SAFE-04 hazard), rejected by the v5.2 carry-forward (DET-14). v5.2 S-P02 all clean.
        re.compile(r"the\s+assumption\s+breaks\s+down\b", re.IGNORECASE),
        # v6.3 capture-backed: S-P02 run1 uses "inversion analysis" in the orchestrator
        # preamble ("The first-principles agent completed the inversion analysis"); run2
        # also contains "inversion analysis" in its orchestrator preamble; run5 likewise.
        # Source: tests/step0-captures-v6.3/S-P02-run1.txt, run2.txt, run5.txt (capture date: 2026-06-16)
        # False-positive guard: "inversion analysis" is technique-specific vocabulary; not
        # present in any S-N04 v6.3 capture (all 5 clean) or S-P01 v6.3 capture (all 5 clean).
        # D-08 bump (Phase 94, Plan 03, 2026-06-17): inversion pattern count 7 → 8 (this marker).
        re.compile(r"inversion\s+analysis", re.IGNORECASE),
        # v6.3 capture-backed: S-P02 run4 uses "When the assumption breaks — 5 detectable
        # regimes" (no trailing "down"). Run4's use is INDEPENDENT of the existing
        # `the assumption breaks down` marker (which requires the word "down"). Runs 2 and 3
        # use "When the assumption breaks down", which is caught by the existing marker above.
        # The negative lookahead (?!\s+down) prevents this pattern from co-firing with
        # `the assumption breaks down` on the same span — restoring the Phase 91 CR-01
        # non-overlap discipline (a second DIFFERENT phrase must corroborate, not a substring
        # of an already-counted phrase).
        # WR-01 fix (Phase 94, Plan 03, 2026-06-17): the original `when\s+the\s+assumption\s+breaks`
        # without the lookahead double-counted runs 2 and 3 (both markers fired on "When the
        # assumption breaks down"), inflating the count vector to [2,3,3,1,1]. The lookahead
        # corrects this to the honest [2,2,2,1,1] — run2=2 ('the assumption breaks down' +
        # 'inversion analysis') and run3=2 ('inverted claim' + 'the assumption breaks down').
        # Source: tests/step0-captures-v6.3/S-P02-run4.txt (capture date: 2026-06-16)
        # False-positive guard: not present in any S-N04 v6.3 capture (all 5 clean) or
        # S-P01 v6.3 capture (all 5 clean). "when the assumption breaks" is specific to
        # formal inversion framing (conditional-precondition enumeration).
        # D-08 bump (Phase 94, Plan 03, 2026-06-17): inversion pattern count 8 → 9 (this marker).
        re.compile(r"when\s+the\s+assumption\s+breaks(?!\s+down)", re.IGNORECASE),
        #
        # v5.2 CARRY-FORWARD (DET-14 / RR-79-02 → RR-92-01 → RR-95-01 [superseded Phase 96 Plan 02]): All 5 S-P02 v5.2 captures
        # (.planning/v5.2-inputs/rebase-evidence/S-P02-run1..5.jsonl) contain
        # ZERO canonical inversion vocabulary across all runs:
        #   "invert, always invert":           0/5 across all runs
        #   "inverted claim" / "inverted form": 0/5 across all runs
        #   "failure-guaranteeing condition":   0/5 across all runs
        #   "necessary precondition":           0/5 across all runs
        # All 5 runs use generic "When/Where ... breaks down" framing to express
        # the inversion result. "breaks down" appears in 4/5 runs (misses run2
        # which uses "breaks" without "down") and is NOT false-positive-safe —
        # it would fire on any full-composer output discussing a challenged
        # assumption or business claim (SAFE-04 hazard). Phase 77 DET-10 already
        # broadened inversion markers with no score movement; blind re-broadening
        # is disallowed (D-06).
        #
        # Per-run captured headers (the focused signal using no inversion vocabulary):
        #   run1: "When 'Faster Ships → Better Retention' Breaks Down"
        #   run2: "The four ways it breaks" (no "down"; "breaks down" grep misses run2)
        #   run3: variations of "Breaks Down" / "breaks down"
        #   run4: variations of "Breaks Down" / "breaks down"
        #   run5: variations of "Breaks Down" / "breaks down"
        # Honest observed score: 0/5. Phase 80 live re-baseline will record the true K/N.
        #
        # v6.3 CARRY-FORWARD (REARCH-02 / RR-79-02 → RR-92-01 → RR-95-01 [superseded Phase 96 Plan 02]):
        # Per v6.3 evidence, the single new marker ("the assumption breaks down") recovers
        # ONLY run3, where it co-fires with the existing "inverted claim" for a genuine
        # 2-distinct corroboration. The overlapping "when the assumption breaks" sibling was
        # REMOVED in the CR-01 code-review fix (it was a substring → double-counted one span),
        # so no run fires inversion on a single phrase anymore.
        # Per-run v6.3 captured modes: all 5 = full-composer (live).
        # Per-run v6.3 offline distinct-hit coverage (Phase 94, WR-01 fix — WITH lookahead):
        #   run1=2 distinct ('inverted claim' + 'inversion analysis') → fires focused
        #   run2=2 distinct ('the assumption breaks down' + 'inversion analysis')
        #          Note: 'when the assumption breaks(?!\s+down)' does NOT fire on run2 ("breaks down")
        #   run3=2 distinct ('inverted claim' + 'the assumption breaks down')
        #          Note: 'when the assumption breaks(?!\s+down)' does NOT fire on run3 ("breaks down")
        #   run4=1 distinct ('when the assumption breaks(?!\s+down)' only — "breaks — 5 detectable")
        #   run5=1 distinct ('inversion analysis' only; no 2nd distinct)
        # Honest count vector (WR-01 fix): [2, 2, 2, 1, 1] — runs 1, 2, 3 fire focused.
        # Runs 4, 5 stay honest carry-forwards (D-01); Phase 95 baseline records true K/N.
        # Sentinel RR-92-01 → RR-95-01 → RR-108-01 in self_test_boundary() (renamed Phase 108 Plan 02; re-pointed to v7.4 vector [1, 2, 1, 1, 1]; prior v6.4 vector [2, 1, 1, 1, 0]).
        # Source: tests/step0-captures-v6.3/S-P02-run1..5.txt (2026-06-16).
        #
        # OCH-02, Phase 121, D-03: additive heading-anchored markers, inversion 9→13.
        # These four markers anchor on the ## Output-contract headers defined in D-01.
        # Heading-anchored (re.MULTILINE): fires on real focused inversion output
        # headings but NOT on prose mentions — the frozen v7.6 S-P02 captures have
        # no such headings, so the regression vector [2,0,1,1,1] stays unchanged
        # (D-04 step 2). ADD only; do not remove any of the 9 existing markers above.
        re.compile(r"^#{2,6}\s+Inverted\s+Claim\b", re.IGNORECASE | re.MULTILINE),
        re.compile(
            r"^#{2,6}\s+Failure[-\s]?Guaranteeing\s+Conditions\b",
            re.IGNORECASE | re.MULTILINE,
        ),
        re.compile(r"^#{2,6}\s+Necessary\s+Preconditions\b", re.IGNORECASE | re.MULTILINE),
        # Clean teeth anchor (no overlapping existing inversion marker):
        # "## Stress-Test Verdict" has NO corresponding old-prose marker, so a
        # synthetic fixture containing only this heading can prove this new marker
        # fires independently. Does not appear in any frozen S-P02 v7.6 capture.
        re.compile(r"^#{2,6}\s+Stress[-\s]?Test\s+Verdict\b", re.IGNORECASE | re.MULTILINE),
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
        # v7.7-diag capture-backed: "candidate cause(s)" fires in S-P03-run2, run3, run5
        # (tests/step0-captures-v7.7-diag/S-P03-run{1..5}.txt). In run5 (a genuine false
        # negative with only 1 existing fishbone marker) candidate-causes supplies the 2nd
        # distinct hit → run5 becomes PASS. Does NOT fire in S-N04 v7.6 negative controls
        # or v7.4 S-P01 pre-mortem captures (cross-verified).
        # FIX-01, Phase 117, D-03 fence: additive only, fishbone 6→7 markers.
        re.compile(r"\bcandidate\s+causes?\b", re.IGNORECASE),
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
        # v6.3 capture-backed: S-P05-run2/3 output uses "## Weighted scoring" as a
        # section header. This is the technique's canonical scoring step (assign
        # weights, run the matrix). v5.2 S-P05 run1..5 all clean (zero matches — no
        # run 1/2/5 push from 1 to 2; RR-79-03 → RR-92-02 → RR-95-02 barrier intact).
        # Source: tests/step0-captures-v6.3/S-P05-run2.txt (capture date: 2026-06-16)
        # False-positive guard: "weighted scoring" is specific to structured scoring
        # procedures; not present in any S-N04 v6.3 capture (all 5 clean).
        # CR-01/WR-01/WR-02 fix (Phase 91-02 code review): the sibling "scoring matrix"
        # marker was REMOVED — it is a substring of "weighted scoring matrix" (run3's
        # header), so it double-counted the same single span as "weighted scoring"
        # (false corroboration). The "sensitivity analysis" marker was also REMOVED —
        # a broad cross-domain term that duplicates the existing "sensitivity check"
        # marker and was the highest live-rebaseline collision risk. Only the single
        # non-overlapping "weighted scoring" addition remains (trade-off set 4 → 5).
        re.compile(r"weighted\s+scoring\b", re.IGNORECASE),
        # v6.3 capture-backed: S-P05 ALL 5 runs contain "trade-off analysis" in the
        # orchestrator preamble or body text (run1: "completed its trade-off analysis";
        # run2: "build a trade-off analysis"; run3: "trade-off study" / section title
        # "Trade-off Analysis"; run4: uses "trade-off analysis" in section headers;
        # run5: uses "trade-off analysis" in its framing). Verified against S-N04 v6.3
        # captures (all 5 clean: 0 hits) and S-P02 v6.3 captures (all 5 clean: 0 hits).
        # Source: tests/step0-captures-v6.3/S-P05-run1..5.txt (capture date: 2026-06-16)
        # False-positive guard: "trade-off analysis" is technique-specific phrase;
        # not present in any S-N04 v6.3 capture (all 5 clean) or S-P02 v6.3 capture
        # (all 5 clean). The regex allows optional hyphen variant ("trade off analysis").
        # D-08 bump (Phase 94, Plan 03, 2026-06-17): trade-off pattern count 5 → 6 (this marker).
        re.compile(r"trade.?off\s+analysis", re.IGNORECASE),
        #
        # v5.2 CARRY-FORWARD (DET-15 / RR-79-03 → RR-92-02 → RR-95-02 [superseded Phase 96 Plan 02]): Extended grep over all 5 S-P05
        # v5.2 captures (.planning/v5.2-inputs/rebase-evidence/S-P05-run1..5.jsonl)
        # found only ONE phrase clearing the D-08 all-5-present + S-N-absent bar:
        #   "trade-off analysis": run1=1, run2=1, run3=2, run4=2, run5=2 → 5/5; 0/20 S-N.
        # No second phrase clears the bar. D-04 requires TWO distinct markers for
        # MIN_HEADER_HITS=2 to fire; one phrase alone is insufficient.
        #
        # Phrases tested that FAILED the D-08 bar (per-run S-P05 counts / S-N hits):
        #   "trade-off matrix":          run1=1, run2=0, run3=1, run4=0, run5=0 → 2/5
        #   "weighted decision matrix":  run1=0, run2=1, run3=0, run4=1, run5=0 → 2/5
        #   "weighted scorecard":        run1=0, run2=0, run3=0, run4=0, run5=1 → 1/5
        #   "weighted total" (existing): run1=1, run2=1, run3=0, run4=0, run5=1 → 3/5
        #   "weights locked before scoring": run1=0, run2=0, run3=1, run4=0, run5=0 → 1/5
        #   "lock the weights":          0/5 across all runs
        #   "score the options":         0/5 across all runs
        #   "weights before scoring":    0/5 across all runs
        #   "weighted score" (v6.3 reject): fires v5.2 S-P05 run5 → risk push 1→2 on run5
        #   "weighted decision matrix" (v6.3 reject): fires v5.2 S-P05 run2/run4
        #
        # Verbatim captured headers per run (the focused signal not yet matched):
        #   run1: "## The trade-off matrix" + "## Key cost ground truths"
        #   run2: "## Weighted decision matrix"
        #   run3: "## 4. Trade-Off Matrix" + "## 2-3. Key Ground Truths"
        #   run4: "## Weighted decision matrix"
        #   run5: "## Weighted scorecard"
        # Ground Truths / Key Ground Truths headers in runs 1 and 3 trip the
        # composer-structure override (composer_hits >= _COMPOSER_FOCUS_CEILING=4
        # is not yet reached, but trade-off hits < MIN_HEADER_HITS=2 → returns none).
        #
        # "trade-off analysis" appears in the orchestrator's own introductory
        # framing ("completed the trade-off analysis") — it clears the mechanical
        # bar but is topic-specific rather than technique-specific, and has no safe
        # partner phrase. Adding it alone would not recover the score (D-04: two
        # markers required) and is not added. Honest observed score: 0/5.
        # Phase 80 live re-baseline will record the true K/N.
        #
        # v6.3 CARRY-FORWARD (REARCH-02 / RR-79-03 → RR-92-02 → RR-95-02 [superseded Phase 96 Plan 02]):
        # Per v6.3 evidence, the single new non-overlapping marker ("weighted scoring")
        # recovers runs 2 and 3, where it co-fires with the existing "weighted total" for
        # a genuine 2-distinct corroboration. The overlapping "scoring matrix" and the broad
        # "sensitivity analysis" markers were REMOVED in the CR-01/WR-01/WR-02 code-review fix.
        # Per-run v6.3 captured modes: all 5 = full-composer (live).
        # Per-run v6.3 offline distinct-hit coverage (Phase 94, Plan 03 update — WITH new marker):
        #   run1=1 distinct ('trade-off analysis' only; no 2nd distinct — weighted total absent)
        #   run2=3 distinct ('weighted total' + 'weighted scoring' + 'trade-off analysis')
        #   run3=3 distinct ('weighted total' + 'weighted scoring' + 'trade-off analysis')
        #   run4=2 distinct ('weighted total' + 'trade-off analysis') → now fires focused
        #   run5=1 distinct ('trade-off analysis' only; no 2nd distinct — composer-override path)
        # New count vector (D-09 re-validation): [1, 3, 3, 2, 1] — runs 2, 3, 4 fire focused.
        # Runs 1, 5 stay honest carry-forwards (D-01); Phase 95 baseline records true K/N.
        # D-09 note: "weighted score" stays REJECTED (fires a v5.2 S-P05 capture → RR-79-03/RR-92-02/RR-95-02
        # barrier risk); "weighted scoring" is the safe non-overlapping replacement.
        # Sentinel RR-92-02 → RR-95-02 → RR-108-02 in self_test_boundary() (renamed Phase 108 Plan 02; re-pointed to v7.4 vector [1, 1, 2, 2, 0]; prior v6.4 vector [1, 2, 2, 1, 1]).
        # Source: tests/step0-captures-v6.3/S-P05-run1..5.txt (2026-06-16).
        #
        # OCH-02, Phase 121, D-03: additive heading-anchored markers, trade-off 6→10.
        # These four markers anchor on the ## Output-contract headers defined in D-01.
        # None of the four trade-off headers overlap any existing trade-off marker —
        # a header-only synthetic fixture reaches MIN_HEADER_HITS ONLY via these new
        # markers (genuine teeth). Heading-anchored (re.MULTILINE): fires on focused
        # trade-off output headings but NOT on prose. The frozen S-P05 v7.6 captures
        # contain these words as prose substrings only (never as ## headings), so the
        # [2,2,2,2,1] regression vector stays unchanged (D-04 step 2). ADD only.
        re.compile(r"^#{2,6}\s+Options\b", re.IGNORECASE | re.MULTILINE),
        re.compile(
            r"^#{2,6}\s+Criteria\s+(?:&|and)\s+Weights\b",
            re.IGNORECASE | re.MULTILINE,
        ),
        re.compile(r"^#{2,6}\s+Scoring\b", re.IGNORECASE | re.MULTILINE),
        re.compile(r"^#{2,6}\s+Recommendation\b", re.IGNORECASE | re.MULTILINE),
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
# (weighted total + sensitivity check), composer_hits = 3 — Ground Truths + Derivation
# Chains PLUS one incidental "verdict" match in the prose "flips the verdict" that
# _composer_structure_hits counts via re.findall; 3 < _COMPOSER_FOCUS_CEILING (=4) so
# the n == 1 branch wins -> focused-trade-off after the reorder. (This composer_hits=3
# reality — not the 2 the 77-04 plan assumed — is why the ceiling is 4, not 3.)
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
# composer_hits=5 >= CEILING=4 so the n==1 early-return is skipped and the composer
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
