#!/usr/bin/env python3
# /// script
# requires-python = ">=3.12"
# dependencies = []
# ///
"""Sub-skill routing battery harness for the first-principles agent.

Why this exists:
    Phase 45 measures whether the first-principles agent, once routed via the
    parent routing battery (`scripts/check-routing.py`), then loads the
    *correct sub-skill reference* (`agents/references/pre-mortem.md` vs
    `agents/references/inversion.md`) for the prompt class. The parent battery
    proves the binary DELEGATE vs NO-DELEGATE routing; this sibling proves the
    finer-grained sub-skill selection layer beneath it.

    Sibling, not extension (locked decision D-01 — see 45-CONTEXT.md):
        `scripts/check-routing.py` is v3.4-locked and may NOT be modified.
        This script lives next to it as a sibling verifier. The two share
        nothing at the import layer.

    Inline-copy, no shared module (locked decision D-02):
        Eleven named code regions are copy-pasted verbatim from
        `scripts/check-routing.py` (shebang block, imports, Prompt dataclass,
        catalog parser + helpers, _walk, _run_prompt_to, _run_prompt_n_times,
        _ensure_claude_available, _print, _default_out_dir, build_parser +
        main with the K>N guard, self-test scaffolding). Only the detection
        layer (_signal_a / _signal_b / detect_routing) is replaced with a
        sub-skill classifier (Task 2). When a third routing-measurement
        consumer arrives, the deferred `scripts/_routing_common.py`
        factoring is triggered — not before.

    Classification is 4-way:
        {"pre-mortem", "inversion", "both", "none-or-other"}
        - pre-mortem: pre-mortem.md loaded OR procedure markers fired
        - inversion: inversion.md loaded OR procedure markers fired
        - both: both fired (used as match when expected is pre-mortem or inversion)
        - none-or-other: neither fired (Phase 45 baseline expects this for
          the FU-21-1/FU-21-2 regression cases)

Usage:
    scripts/check-sub-skill-routing.py --catalog <path> [--plugin-dir <path>]
                                       [--out <dir>] [--p-threshold N]
                                       [--n-threshold N] [--quiet] [--dry-run]
                                       [--repeat N] [--min-pass K]
    scripts/check-sub-skill-routing.py --self-test

Defaults:
    --plugin-dir   $(pwd)/first-principles
    --out          /tmp/check-sub-skill-routing-<UTC-timestamp>/
    --p-threshold  0   (Phase 45 baseline is non-gating on P-failures —
                        FU-21-1/FU-21-2 are EXPECTED to FAIL pre-Phase 46)
    --n-threshold  2   (both N-controls must classify none-or-other)
    --repeat       5
    --min-pass     3   (3-of-5 K-of-N for noise tolerance)

Exit codes:
    0  thresholds met (battery PASS), --self-test all fixtures correct,
       or --dry-run successful parse
    1  thresholds not met (battery FAIL) or --self-test fixture mismatch
    2  environment error (claude missing, catalog parse error, IO error,
       invalid CLI args)
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


REPO_ROOT: Path = Path(__file__).resolve().parents[1]
DEFAULT_PLUGIN_DIR: Path = REPO_ROOT / "first-principles"

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

SUBSKILL_INVOCATION_RE: dict[str, re.Pattern[str]] = {
    "pre-mortem": re.compile(r"first-principles:pre-mortem\b", re.IGNORECASE),
    "inversion": re.compile(r"first-principles:inversion\b", re.IGNORECASE),
}


# ---------------------------------------------------------------------------
# Data types
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class Prompt:
    """One row from the sub-skill routing catalog."""

    id: str
    text: str
    expected: SubSkill


# ---------------------------------------------------------------------------
# Catalog parsing
# (Inline-copied from scripts/check-routing.py:_strip_quotes, _split_row,
# _is_separator_row, parse_catalog. Only the verdict-validation set differs.)
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


def parse_catalog(path: Path) -> tuple[list[Prompt], list[Prompt]]:
    """Parse a sub-skill-routing-catalog.md-shaped Markdown catalog.

    Returns (positives, negatives). Rows are classified by the prefix of
    the id cell: `P*` -> positive, `N*` -> negative. Other ids are ignored.

    Raises FileNotFoundError if path missing, ValueError on parse error
    or empty result.
    """
    if not path.exists():
        raise FileNotFoundError(f"catalog not found: {path}")

    positives: list[Prompt] = []
    negatives: list[Prompt] = []

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

        prompt = Prompt(id=rid, text=prompt_text, expected=expected_lc)  # type: ignore[arg-type]
        if rid.startswith("P"):
            positives.append(prompt)
        else:
            negatives.append(prompt)

    if not positives and not negatives:
        raise ValueError(f"catalog {path} contained no P* or N* rows")
    return positives, negatives


# ---------------------------------------------------------------------------
# Detection (Signal A / Signal B) — sub-skill 4-way classifier
# (Replaces scripts/check-routing.py:_signal_a / _signal_b / detect_routing.)
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


_SUBSKILL_TOOL_NAMES: set[str] = {"Skill", "Agent", "Task"}


# Routing-field keys: the input-dict keys that name the invocation target.
# Other input keys (`prompt`, `args`, `description`) carry user-facing text
# that can mention sub-skill names without invoking them — must NOT count.
_ROUTING_FIELDS: tuple[str, ...] = ("skill", "subagent_type")


def _signal_a(parsed_lines: list[object], raw_text: str) -> set[str]:
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


def detect_subskill(jsonl_path: Path) -> SubSkill:
    """Score a captured stream-json event log into one of the 4 SubSkill values.

    v2 design: single-signal detection (see SUBSKILL_INVOCATION_RE block above
    for the v1→v2 rationale). Signal B was removed because the composer
    `first-principles:first-principles` Agent emits all six companion
    techniques' procedure text verbatim, causing text-marker-based detection
    to spuriously fire `pre-mortem` AND `inversion` on every composer-only run.

    Resolution:
        fired = _signal_a(parsed_lines, raw_text)
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

    fired = _signal_a(parsed_lines, raw_text)
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
# Transport: invoke claude -p per prompt
# (Inline-copied verbatim from scripts/check-routing.py:_run_prompt_to —
# DO NOT EDIT the flag list. RESEARCH §Pitfall 6: omitting any flag breaks
# detection.)
# ---------------------------------------------------------------------------


def _run_prompt_to(prompt: Prompt, plugin_dir: Path, out_path: Path) -> Path:
    """Issue one prompt via `claude -p` and capture the stream-json log to out_path.

    Transport per D-10 (verbatim, copied from check-routing.py lines 329-341):
        claude -p --plugin-dir <path> --no-session-persistence \
          --output-format stream-json --verbose \
          --permission-mode bypassPermissions <prompt>

    Returns out_path (combined stdout + stderr written there).
    """
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


def _run_prompt_n_times(
    prompt: Prompt, plugin_dir: Path, out_dir: Path, repeat: int
) -> list[SubSkill]:
    """Run a single prompt N times and return a list of N SubSkill values.

    When repeat == 1, writes to <id>.jsonl (Phase 36-locked legacy parity).
    When repeat > 1, writes to <id>-run<n>.jsonl (1-indexed, n in 1..repeat).
    """
    results: list[SubSkill] = []
    for run_idx in range(repeat):
        if repeat == 1:
            out_path = out_dir / f"{prompt.id}.jsonl"
        else:
            out_path = out_dir / f"{prompt.id}-run{run_idx + 1}.jsonl"
        jsonl_path = _run_prompt_to(prompt, plugin_dir, out_path)
        results.append(detect_subskill(jsonl_path))
    return results


# ---------------------------------------------------------------------------
# Battery driver
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


def run_battery(
    positives: list[Prompt],
    negatives: list[Prompt],
    plugin_dir: Path,
    out_dir: Path,
    p_threshold: int,
    n_threshold: int,
    quiet: bool,
    repeat: int = 1,
    min_pass: int = 1,
) -> int:
    """Run the full battery, write outputs, return 0 (PASS) or 1 (FAIL).

    When repeat == 1, output is legacy-shape (no `run` column in scores.tsv).
    When repeat > 1, scores.tsv carries a `run` column and the v3.4 per-run
    schema. Per-prompt PASS requires match_count >= min_pass under the
    lenient match rule.
    """
    _ensure_claude_available()
    out_dir.mkdir(parents=True, exist_ok=True)

    total = len(positives) + len(negatives)
    _print(
        f"check-sub-skill-routing: catalog has {len(positives)} P + "
        f"{len(negatives)} N (total {total})",
        quiet,
    )
    _print(f"  plugin-dir: {plugin_dir}", quiet)
    _print(f"  out:        {out_dir}", quiet)
    _print(f"  thresholds: P >= {p_threshold}, N >= {n_threshold}", quiet)
    if repeat > 1:
        _print(f"  repeat:     {repeat} (K-of-N, min-pass={min_pass})", quiet)

    prompt_results: list[tuple[Prompt, list[SubSkill], int, bool]] = []
    ordered = list(positives) + list(negatives)
    for idx, prompt in enumerate(ordered, start=1):
        _print(f"[{idx}/{total}] {prompt.id}: expected={prompt.expected} ...", quiet)
        verdicts = _run_prompt_n_times(prompt, plugin_dir, out_dir, repeat)
        match_count = sum(1 for v in verdicts if _is_match(v, prompt.expected))
        prompt_passed = match_count >= min_pass
        prompt_results.append((prompt, verdicts, match_count, prompt_passed))
        if repeat == 1:
            actual = verdicts[0]
            _print(
                f"    -> actual={actual} {'PASS' if prompt_passed else 'FAIL'}",
                quiet,
            )
        else:
            ratio_str = f"{match_count}/{repeat}"
            _print(f"    -> {ratio_str} {'PASS' if prompt_passed else 'FAIL'}", quiet)

    scores_path = out_dir / "scores.tsv"
    with scores_path.open("w", encoding="utf-8") as fh:
        if repeat == 1:
            fh.write("id\texpected\tactual\tpass\n")
            for prompt, verdicts, match_count, prompt_passed in prompt_results:
                actual = verdicts[0]
                fh.write(
                    f"{prompt.id}\t{prompt.expected}\t{actual}\t"
                    f"{'pass' if prompt_passed else 'fail'}\n"
                )
        else:
            fh.write("id\trun\texpected\tactual\tmatch\n")
            for prompt, verdicts, match_count, prompt_passed in prompt_results:
                for run_idx, actual in enumerate(verdicts, start=1):
                    match_flag = 1 if _is_match(actual, prompt.expected) else 0
                    fh.write(
                        f"{prompt.id}\t{run_idx}\t{prompt.expected}\t"
                        f"{actual}\t{match_flag}\n"
                    )

    p_pass = sum(
        1
        for prompt, verdicts, match_count, prompt_passed in prompt_results
        if prompt.id.startswith("P") and prompt_passed
    )
    n_pass = sum(
        1
        for prompt, verdicts, match_count, prompt_passed in prompt_results
        if prompt.id.startswith("N") and prompt_passed
    )
    battery_pass = p_pass >= p_threshold and n_pass >= n_threshold

    verdict_lines: list[str] = []
    verdict_lines.append(f"BATTERY: {'PASS' if battery_pass else 'FAIL'}")
    verdict_lines.append(
        f"P: {p_pass}/{len(positives)}  N: {n_pass}/{len(negatives)}"
    )
    if not battery_pass:
        verdict_lines.append("")
        verdict_lines.append("Failed prompts:")
        for prompt, verdicts, match_count, prompt_passed in prompt_results:
            if not prompt_passed:
                if repeat == 1:
                    actual = verdicts[0]
                    verdict_lines.append(
                        f"  {prompt.id}: expected={prompt.expected} actual={actual}"
                    )
                else:
                    verdict_lines.append(
                        f"  {prompt.id}: expected={prompt.expected} "
                        f"{match_count}/{repeat} match"
                    )
    if repeat > 1:
        verdict_lines.append("")
        verdict_lines.append(
            f"Per-prompt K/N (best-of-{repeat}, K={min_pass}):"
        )
        for prompt, verdicts, match_count, prompt_passed in prompt_results:
            verdict_lines.append(
                f"  {prompt.id}: {match_count}/{repeat} "
                f"{'PASS' if prompt_passed else 'FAIL'}"
            )
    verdict_text = "\n".join(verdict_lines) + "\n"
    (out_dir / "verdict.txt").write_text(verdict_text, encoding="utf-8")

    print(verdict_text, end="")
    return 0 if battery_pass else 1


# ---------------------------------------------------------------------------
# Self-test
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


def _run_one_fixture(name: str, body: str, expected: SubSkill) -> bool:
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


def self_test() -> int:
    """Validate detection logic against in-script fixtures. No claude invocation."""
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
        if not _run_one_fixture(name, body, expected):
            all_passed = False

    # K>N rejection self-test (parallel to check-routing.py lines 650-660):
    # invoke main(["--catalog", "/nonexistent", "--repeat", "2", "--min-pass", "3"])
    # and assert exit code 2 (the K>N guard fires before any I/O).
    try:
        rc = main(
            [
                "--catalog",
                "/nonexistent/path/that/does/not/exist",
                "--repeat",
                "2",
                "--min-pass",
                "3",
            ]
        )
    except SystemExit as exc:
        rc = exc.code if isinstance(exc.code, int) else 2
    if rc != 2:
        print(
            f"self-test FAIL: 'kofn_invalid_kn_rejection' expected exit 2 "
            f"(K>N guard), got {rc}",
            file=sys.stderr,
        )
        all_passed = False

    fixture_total = len(fixtures) + 1  # +1 for the K>N rejection test
    if all_passed:
        print(f"self-test PASS ({fixture_total} fixtures)")
        return 0
    return 1


# ---------------------------------------------------------------------------
# Main / CLI
# ---------------------------------------------------------------------------


def _default_out_dir() -> Path:
    ts = _dt.datetime.now(_dt.timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    return Path("/tmp") / f"check-sub-skill-routing-{ts}"


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="check-sub-skill-routing.py",
        description=(
            "Sub-skill routing battery harness — classifies stream-json logs "
            "into {pre-mortem, inversion, both, none-or-other}."
        ),
    )
    mode = p.add_mutually_exclusive_group(required=True)
    mode.add_argument(
        "--catalog",
        type=Path,
        help="Path to a Markdown sub-skill routing catalog.",
    )
    mode.add_argument(
        "--self-test",
        dest="self_test",
        action="store_true",
        help="Validate detection logic against in-script fixtures and exit.",
    )
    p.add_argument(
        "--plugin-dir",
        type=Path,
        default=DEFAULT_PLUGIN_DIR,
        help=(
            f"Plugin directory passed to `claude --plugin-dir` "
            f"(default: {DEFAULT_PLUGIN_DIR})."
        ),
    )
    p.add_argument(
        "--out",
        type=Path,
        default=None,
        help=(
            "Output directory for per-prompt .jsonl + scores.tsv + verdict.txt "
            "(default: /tmp/check-sub-skill-routing-<UTC-timestamp>/)."
        ),
    )
    p.add_argument(
        "--p-threshold",
        type=int,
        default=0,
        help=(
            "Min P-cases matching expected sub-skill for battery PASS "
            "(default: 0 — Phase 45 baseline is non-gating on P-failures)."
        ),
    )
    p.add_argument(
        "--n-threshold",
        type=int,
        default=2,
        help="Min N-cases classified none-or-other for battery PASS (default: 2).",
    )
    p.add_argument(
        "--quiet",
        action="store_true",
        help="Suppress per-prompt progress lines (final verdict still printed).",
    )
    p.add_argument(
        "--dry-run",
        action="store_true",
        help="Parse the catalog and print counts; do not invoke claude.",
    )
    p.add_argument(
        "--repeat",
        type=int,
        default=5,
        metavar="N",
        help="Run each catalog prompt N times (default: 5).",
    )
    p.add_argument(
        "--min-pass",
        type=int,
        default=3,
        metavar="K",
        help="K-of-N runs must match expected for prompt to PASS (default: 3).",
    )
    return p


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.self_test:
        return self_test()

    # K>N pre-flight guard — validated BEFORE any I/O (parallel to
    # check-routing.py:T-36-01 line 753-772, verbatim).
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

    catalog_path: Path = args.catalog
    try:
        positives, negatives = parse_catalog(catalog_path)
    except FileNotFoundError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    except ValueError as exc:
        print(f"error: failed to parse catalog: {exc}", file=sys.stderr)
        return 2

    if args.dry_run:
        print(
            f"Catalog: {len(positives)} P-prompts, {len(negatives)} N-prompts"
        )
        return 0

    out_dir: Path = args.out if args.out is not None else _default_out_dir()
    try:
        return run_battery(
            positives,
            negatives,
            plugin_dir=args.plugin_dir,
            out_dir=out_dir,
            p_threshold=args.p_threshold,
            n_threshold=args.n_threshold,
            quiet=args.quiet,
            repeat=args.repeat,
            min_pass=args.min_pass,
        )
    except OSError as exc:
        print(f"error: IO failure during battery run: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
