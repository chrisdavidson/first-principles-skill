#!/usr/bin/env python3
# /// script
# requires-python = ">=3.12"
# dependencies = []
# ///
"""Focused-output structure detector for the first-principles composer.

Sibling per DEC-46-C. Measures whether the composer agent produced a
focused single-technique output or the full six-technique walkthrough.
Transport inline-copied from check-routing.py (D-01/D-02). Detection
layer is novel — cardinality-classified marker firing per 46-RESEARCH §Q4.

Task 1 scaffold (this commit):
    Transport regions inline-copied verbatim from `scripts/check-routing.py`
    per the Phase 45 PATTERNS §Inline-copy reuse discipline:
      - shebang block + imports + module constants
      - `Prompt` dataclass shape
      - catalog parser + helpers
      - `_walk` structured-walk helper
      - `_run_prompt_to` + `_run_prompt_n_times` (claude -p invocation,
        K-of-N loop, file naming)
      - `_ensure_claude_available`, `_print`, `_default_out_dir`
      - `build_parser` / `main` (CLI surface + K>N pre-flight guard)
      - scores.tsv / verdict.txt writers
    `_TECHNIQUE_CATEGORIES` is present as a placeholder with the six
    technique keys mapped to empty tuples; `classify()` and
    `detect_output_structure()` return "none". Task 2 fills the detection
    layer. Task 3 adds the --self-test fixture battery.

DO NOT inline-copy `_HEADER_CATEGORIES` / `_HEADER_LINE_RE` / `_signal_a`
/ `_signal_b` from check-routing.py — those are routing-signal detectors;
Phase 46's detector is output-structure-shaped and is authored fresh.

Usage:
    scripts/check-focused-output.py --catalog <path> [--plugin-dir <path>]
                                    [--out <dir>] [--p-threshold N]
                                    [--n-threshold N] [--quiet] [--dry-run]
                                    [--repeat N] [--min-pass K]
    scripts/check-focused-output.py --self-test

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

# Six canonical companion technique keys.
_TECHNIQUE_KEYS: tuple[str, ...] = (
    "pre-mortem",
    "inversion",
    "fishbone",
    "five-whys",
    "trade-off",
    "second-order",
)

# Noise-tolerance floor — a marker "fires" only if its regex matches
# >= MIN_HEADER_HITS distinct times in the assistant text. Mirrors the
# Phase 45 `MIN_TEXT_HITS = 2` precedent (see check-sub-skill-routing.py
# v2.1 history). A single incidental mention of e.g. "trade-off" inside
# an unrelated discussion should NOT fire the trade-off technique.
MIN_HEADER_HITS: int = 2


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
# capture.
#
# Pitfall 4 mitigation (MIN_HEADER_HITS=2 floor): each technique requires
# >= 2 distinct phrase hits to count, mirroring Phase 45 MIN_TEXT_HITS=2.
#
# Trade-off bare-token tiebreaker: the bare token `trade-off` (without
# the procedural-marker phrases) is too lexically common to count toward
# MIN_HEADER_HITS. It is detected separately as a tiebreaker signal only
# (currently unused beyond documentation — preserved for future tuning).
#
# Cardinality calibration choice (LOAD-BEARING — read before editing):
# 46-RESEARCH Q4 base rule says n>=4 distinct techniques = full-composer.
# BUT 46-01-SUMMARY Probe 3 showed real composer output fires only 1-2
# distinct technique-name markers (Inversion + Second-Order + brief
# Trade-off mention), while emitting the canonical 5-phase structure
# headers ("Phase 1 — Ground Truths", "Phase 2 — Assumption Audit",
# "Phase 5 — Second-Order Effects", "Verdict", etc.) repeatedly.
#
# Calibration path chosen here = OPTION B from 46-01-SUMMARY findings:
#   Add a structural `composer-structure` signal counting the canonical
#   5-phase markers ("Phase 1", "Ground Truths", "Assumption Audit",
#   "Derivation Chains", "Verdict"). If composer-structure fires at
#   >= MIN_HEADER_HITS, classify as full-composer regardless of the
#   per-technique cardinality. This matches the Probe 3 empirical
#   signal (5 Phase headers + Ground Truths + Assumption Audit + Verdict
#   all fire ≥2x in the real capture) while preserving the original
#   n>=4 rule as a fallback for outputs that omit the canonical headers
#   but emit all six techniques' verbatim markers.
#
# Rationale: the LOAD-BEARING distinction between focused-X and
# full-composer is structural — the composer walks the 5-phase scaffold;
# focused-X output does not. A single technique fired in passing inside
# a 5-phase walkthrough is still full-composer, not focused-X.
#
# Citation: 46-01-SUMMARY "Findings to surface to 46-03" §1, captured
# in `.planning/phases/46-.../wave0-evidence/probe3-full-composer.jsonl`.
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
        re.compile(r"the plan has (already )?failed", re.IGNORECASE),
        # pre-mortem.md procedure step — "working backward: what caused..."
        re.compile(r"working backward(s)?:?\s+what caused", re.IGNORECASE),
        # Note: `failure-guaranteeing` is intentionally NOT included here —
        # Q4.1 collision note flags it as overlapping with inversion. The
        # disambiguation lives in inversion's marker set, not pre-mortem's.
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
    ),
}

# Tiebreaker — bare `trade-off` token. Counted separately, NOT toward
# MIN_HEADER_HITS for the trade-off technique. Reserved for future
# tuning of the focused-trade-off vs ambiguous boundary; currently
# present as documentation of the Q4.5 collision-avoidance choice.
_TRADEOFF_BARE_TOKEN_RE: re.Pattern[str] = re.compile(
    r"\btrade[- ]?off\b", re.IGNORECASE
)

# Composer-structure markers — the canonical 5-phase scaffold headers
# the composer emits in its output. Per the calibration block above
# (OPTION B from 46-01-SUMMARY), if >= MIN_HEADER_HITS of these fire,
# classify as `full-composer` regardless of per-technique cardinality.
# Empirically verified against
# .planning/phases/46-.../wave0-evidence/probe3-full-composer.jsonl
# (5 Phase headers + 2 "Ground Truths" + 1 "Assumption Audit" + 1
# "Verdict" all fired in that real capture).
_COMPOSER_STRUCTURE_PATTERNS: tuple[re.Pattern[str], ...] = (
    re.compile(r"\bPhase\s+[0-9]+\b", re.IGNORECASE),
    re.compile(r"\bGround\s+Truths?\b", re.IGNORECASE),
    re.compile(r"\bAssumption\s+Audit\b", re.IGNORECASE),
    re.compile(r"\bDerivation\s+Chains?\b", re.IGNORECASE),
    re.compile(r"\bVerdict\b", re.IGNORECASE),
)


# ---------------------------------------------------------------------------
# Data types (inline-copied from scripts/check-routing.py — `Prompt`)
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class Prompt:
    """One row from a routing/output-structure catalog."""

    id: str
    text: str
    expected: str


# ---------------------------------------------------------------------------
# Catalog parsing
# (Inline-copied verbatim from scripts/check-routing.py:_strip_quotes,
# _split_row, _is_separator_row, parse_catalog. Only the verdict-validation
# rule differs — this script's parser accepts any non-empty expected
# string because the output-structure verdict vocabulary is open-ended
# until 46-04 calibrates the per-prompt expectations.)
# ---------------------------------------------------------------------------


def _strip_quotes(s: str) -> str:
    s = s.strip()
    if len(s) >= 2 and s[0] in ('"', "'") and s[-1] == s[0]:
        return s[1:-1]
    return s


def _split_row(line: str) -> list[str]:
    """Split a Markdown table row on `|`, returning trimmed cells."""
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
    """Parse a Markdown routing/output-structure catalog."""
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

        if not expected_raw:
            raise ValueError(
                f"row {rid!r}: expected verdict cell must be non-empty"
            )

        prompt = Prompt(id=rid, text=prompt_text, expected=expected_raw)
        if rid.startswith("P"):
            positives.append(prompt)
        else:
            negatives.append(prompt)

    if not positives and not negatives:
        raise ValueError(f"catalog {path} contained no P* or N* rows")
    return positives, negatives


# ---------------------------------------------------------------------------
# Structured walker (inline-copied from scripts/check-routing.py:_walk)
# ---------------------------------------------------------------------------


def _walk(obj: object) -> Iterable[object]:
    """Yield every node in a nested JSON-like structure."""
    yield obj
    if isinstance(obj, dict):
        for v in obj.values():
            yield from _walk(v)
    elif isinstance(obj, list):
        for v in obj:
            yield from _walk(v)


# ---------------------------------------------------------------------------
# Detection — per-technique marker firing + cardinality classifier
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
    text_blobs: list[str] = []
    for parsed in parsed_lines:
        for node in _walk(parsed):
            if not isinstance(node, dict):
                continue
            if node.get("type") == "assistant":
                direct_text = node.get("text")
                if isinstance(direct_text, str):
                    text_blobs.append(direct_text)
                msg = node.get("message")
                if isinstance(msg, dict):
                    content = msg.get("content")
                    if isinstance(content, list):
                        for c in content:
                            if isinstance(c, dict) and c.get("type") == "text":
                                t = c.get("text")
                                if isinstance(t, str):
                                    text_blobs.append(t)
            elif node.get("type") == "text" and isinstance(node.get("text"), str):
                text_blobs.append(node["text"])
    return "\n".join(text_blobs)


def _technique_hits(text: str) -> dict[str, int]:
    """Per-technique total marker-hit count across `text`."""
    hits: dict[str, int] = {}
    for tech, patterns in _TECHNIQUE_CATEGORIES.items():
        total = 0
        for rx in patterns:
            total += len(rx.findall(text))
        hits[tech] = total
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
    Probe 3 finding (OPTION B — composer-structure signal):

        composer_structure_hits >= MIN_HEADER_HITS
                                      → "full-composer"  (structural override)
        n == 0                        → "none"
        n == 1                        → "focused-<technique>"
        n in {2, 3}                   → "ambiguous"
        n >= 4                        → "full-composer"

    The structural override is the LOAD-BEARING calibration — real
    composer outputs may fire only 1-2 technique-name markers but always
    emit the canonical 5-phase scaffold. The override prevents Pitfall 1
    (misclassifying a full-composer walkthrough as `focused-<technique>`
    just because one technique's markers happen to fire).
    """
    if composer_structure_hits >= MIN_HEADER_HITS:
        return "full-composer"
    n = len(fired)
    if n == 0:
        return "none"
    if n == 1:
        tech = next(iter(fired))
        return f"focused-{tech}"  # type: ignore[return-value]
    if n in (2, 3):
        return "ambiguous"
    return "full-composer"


def detect_output_structure(
    parsed_lines: list[object], raw_text: str
) -> OutputStructure:
    """Score a parsed stream-json event log into one of the 9 OutputStructure values.

    Structured-walk-first: extract assistant text via `_walk` (Pitfall 3 —
    don't count Read tool_result echoes). If the structured walk yields
    no text (parser drift or unanticipated capture shape), fall back to
    `raw_text` for marker counting — the trade-off here is that raw-text
    fallback may over-count markers that appear in tool inputs, but
    that risk is preferable to silently returning "none" on a capture
    shape we did not anticipate.
    """
    text = _extract_assistant_text(parsed_lines)
    if not text.strip():
        text = raw_text

    hits = _technique_hits(text)
    fired = {tech for tech, n in hits.items() if n >= MIN_HEADER_HITS}
    structure_hits = _composer_structure_hits(text)
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
# Transport: invoke claude -p per prompt
# (Inline-copied verbatim from scripts/check-routing.py:_run_prompt_to and
# _run_prompt_n_times — DO NOT EDIT the flag list.)
# ---------------------------------------------------------------------------


def _run_prompt_to(prompt: Prompt, plugin_dir: Path, out_path: Path) -> Path:
    """Issue one prompt via `claude -p` and capture the stream-json log."""
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
) -> list[OutputStructure]:
    """Run a single prompt N times and return a list of N OutputStructure values."""
    results: list[OutputStructure] = []
    for run_idx in range(repeat):
        if repeat == 1:
            out_path = out_dir / f"{prompt.id}.jsonl"
        else:
            out_path = out_dir / f"{prompt.id}-run{run_idx + 1}.jsonl"
        jsonl_path = _run_prompt_to(prompt, plugin_dir, out_path)
        results.append(detect_output_structure_from_file(jsonl_path))
    return results


# ---------------------------------------------------------------------------
# Battery driver (inline-copied from scripts/check-routing.py)
# ---------------------------------------------------------------------------


def _ensure_claude_available() -> None:
    if shutil.which("claude") is None:
        print(
            "error: `claude` CLI not found on PATH; cannot run the focused-output battery",
            file=sys.stderr,
        )
        sys.exit(2)


def _print(msg: str, quiet: bool) -> None:
    if not quiet:
        print(msg, flush=True)


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
    """Run the full battery, write outputs, return 0 (PASS) or 1 (FAIL)."""
    _ensure_claude_available()
    out_dir.mkdir(parents=True, exist_ok=True)

    total = len(positives) + len(negatives)
    _print(
        f"check-focused-output: catalog has {len(positives)} P + "
        f"{len(negatives)} N (total {total})",
        quiet,
    )
    _print(f"  plugin-dir: {plugin_dir}", quiet)
    _print(f"  out:        {out_dir}", quiet)
    _print(f"  thresholds: P >= {p_threshold}, N >= {n_threshold}", quiet)
    if repeat > 1:
        _print(f"  repeat:     {repeat} (K-of-N, min-pass={min_pass})", quiet)

    prompt_results: list[tuple[Prompt, list[OutputStructure], int, bool]] = []
    ordered = list(positives) + list(negatives)
    for idx, prompt in enumerate(ordered, start=1):
        _print(
            f"[{idx}/{total}] {prompt.id}: expected={prompt.expected} ...",
            quiet,
        )
        verdicts = _run_prompt_n_times(prompt, plugin_dir, out_dir, repeat)
        match_count = sum(1 for v in verdicts if v == prompt.expected)
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
            _print(
                f"    -> {ratio_str} {'PASS' if prompt_passed else 'FAIL'}",
                quiet,
            )

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
                    match_flag = 1 if actual == prompt.expected else 0
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
# Self-test (Task 3 adds fixtures)
# ---------------------------------------------------------------------------


def self_test() -> int:
    """Placeholder — Task 3 wires in the in-script fixture battery and the
    Probe 3 sanity feed. For Task 1 scaffold we still exercise the K>N
    rejection path so the guard ships green from day one.
    """
    all_passed = True
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

    if all_passed:
        print("self-test PASS (1 fixture — Task 3 will expand)")
        return 0
    return 1


# ---------------------------------------------------------------------------
# Main / CLI (inline-copied from scripts/check-routing.py)
# ---------------------------------------------------------------------------


def _default_out_dir() -> Path:
    ts = _dt.datetime.now(_dt.timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    return Path("/tmp") / f"check-focused-output-{ts}"


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="check-focused-output.py",
        description=(
            "Focused-output structure detector for the first-principles "
            "composer agent. Classifies stream-json logs into "
            "{focused-<technique>, ambiguous, full-composer, none}."
        ),
    )
    mode = p.add_mutually_exclusive_group(required=True)
    mode.add_argument(
        "--catalog",
        type=Path,
        help="Path to a Markdown output-structure catalog.",
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
            "Output directory (default: /tmp/check-focused-output-<UTC-ts>/)."
        ),
    )
    p.add_argument("--p-threshold", type=int, default=0)
    p.add_argument("--n-threshold", type=int, default=0)
    p.add_argument("--quiet", action="store_true")
    p.add_argument("--dry-run", action="store_true")
    p.add_argument("--repeat", type=int, default=5, metavar="N")
    p.add_argument("--min-pass", type=int, default=3, metavar="K")
    return p


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.self_test:
        return self_test()

    # K>N pre-flight guard — validated BEFORE any I/O.
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
