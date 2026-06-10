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

Why this exists:
    Phase 46 ships an internal dispatcher in the composer agent body
    (`Step 0 — Technique selection`) that branches between MODE=focused-X
    and MODE=full-composer. Plan 46-04 needs a measurement instrument that
    can classify a captured composer response stream into one of:

        focused-pre-mortem | focused-inversion | focused-fishbone |
        focused-five-whys | focused-trade-off | focused-second-order |
        ambiguous | full-composer | none

    This script provides that instrument as a SIBLING to
    `scripts/check-routing.py` and `scripts/check-sub-skill-routing.py`
    rather than an in-place edit to either. DEC-46-C locks the sibling
    decision; D-01 (no-edit) and D-02 (inline-copy reuse) are inherited
    from Phase 45.

Inline-copy regions (verbatim from scripts/check-routing.py — D-01/D-02):
    - Shebang + script-header block + imports + module constants
    - `Prompt` dataclass shape
    - Catalog parsing helpers (`_strip_quotes`, `_split_row`,
      `_is_separator_row`, `parse_catalog`)
    - `_walk` structured-walk helper
    - Transport: `_run_prompt_to`, `_run_prompt_n_times`
    - CLI surface: argparse builder, K>N pre-flight rejection guard,
      battery driver, scores.tsv / verdict.txt writers
    - `_ensure_claude_available`, `_print`, `_default_out_dir`
    - `--self-test` scaffolding

Detection layer — what differs from check-routing.py:
    - `_HEADER_CATEGORIES` / `_HEADER_LINE_RE` from check-routing.py are
      ROUTING-shaped (six section headers of the FP agent's output).
      Phase 46 needs OUTPUT-STRUCTURE-shaped detection: per-technique
      marker tables `_TECHNIQUE_CATEGORIES` keyed by the six companion
      techniques (pre-mortem, inversion, fishbone, five-whys, trade-off,
      second-order). Markers are verbatim phrases drawn from
      46-RESEARCH §Q4.1-Q4.6 tables (cited at each entry).
    - Cardinality classifier `classify()` resolves to focused-<technique>
      (n=1), ambiguous (n=2, n=3), or full-composer (n>=4 OR composer-
      structure signal fires). MIN_HEADER_HITS=2 mirrors the Phase 45
      `MIN_TEXT_HITS=2` precedent (noise-tolerance floor — a single
      incidental mention should NOT fire a marker).

Cardinality calibration choice (LOAD-BEARING — read before editing):
    46-RESEARCH Q4 base rule says n>=4 distinct techniques = full-composer.
    BUT 46-01-SUMMARY Probe 3 showed real composer output fires only 1-2
    distinct technique-name markers (Inversion + Second-Order + brief
    Trade-off mention), while emitting the canonical 5-phase structure
    headers ("Phase 1 — Ground Truths", "Phase 2 — Assumption Audit",
    "Phase 5 — Second-Order Effects", "Verdict", etc.) repeatedly.

    Calibration path chosen here = OPTION B from 46-01-SUMMARY findings:
      Add a structural `composer-structure` signal counting the canonical
      5-phase scaffold markers ("Ground Truths", "Assumption Audit",
      "Derivation Chains", "Verdict"). If
      composer-structure fires at >= MIN_HEADER_HITS, classify as
      full-composer regardless of the per-technique cardinality. This
      matches the Probe 3 empirical signal (Phase-titled section headers +
      Ground Truths + Assumption Audit + Derivation Chains + Verdict all
      fire ≥2x in the real capture) while preserving the original n>=4
      rule as a fallback for outputs that omit the canonical headers but
      emit all six techniques' verbatim markers.

    Bug 1 fix (66-03 Signal B probe, 2026-06-10): the original "Phase N"
      entry was r"\\bPhase\\s+[0-9]+\\b" — too broad. It fired on plan-content
      prose in focused pre-mortem output ("Phase 1 migrates staging"; "Phase
      1/2/3" in a multi-phase migration plan 19-29 times), causing false
      full-composer classifications on P24 and P25. First tightened to a
      multi-word composer-header form, then removed entirely (66 review
      WR-02): the tightened form double-counted against the standalone
      header patterns, so a single header line defeated the
      MIN_HEADER_HITS=2 noise floor. The standalone scaffold tokens
      ("Ground Truths", "Assumption Audit", "Derivation Chains",
      "Verdict") now carry the structural signal alone.

    Bug 2 fix (66-03 Signal B probe, 2026-06-10): pre-mortem technique
      markers were too strict — required exact procedure-text phrases
      ("working backward: what caused", "the plan has already failed").
      Real focused pre-mortem output uses natural variation ("Working
      backward from the wreckage", "treat it as already failed"). Both
      patterns were loosened; see _TECHNIQUE_CATEGORIES['pre-mortem'].

    Rationale: the LOAD-BEARING distinction between focused-X and
    full-composer is structural — the composer walks the 5-phase scaffold;
    focused-X output does not. A single technique fired in passing inside
    a 5-phase walkthrough is still full-composer, not focused-X. The
    structural signal is the load-bearing observable.

    Citation: 46-01-SUMMARY "Findings to surface to 46-03" §1, captured
    in `.planning/phases/46-.../wave0-evidence/probe3-full-composer.jsonl`.

Usage:
    scripts/check-focused-output.py --catalog <path> [--plugin-dir <path>]
                                    [--out <dir>] [--p-threshold N]
                                    [--n-threshold N] [--quiet] [--dry-run]
                                    [--repeat N] [--min-pass K]
    scripts/check-focused-output.py --self-test

Defaults:
    --plugin-dir   $(pwd)/first-principles
    --out          /tmp/check-focused-output-<UTC-timestamp>/
    --p-threshold  4   (all four calibrated P rows must pass)
    --n-threshold  1   (sole over-trigger control N1 must pass)
    --repeat       5
    --min-pass     3   (3-of-5 K-of-N noise tolerance)

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
# the composer emits in its output. Per the calibration block at the top
# of this file (OPTION B from 46-01-SUMMARY), if >= MIN_HEADER_HITS of
# these fire, classify as `full-composer` regardless of per-technique
# cardinality. Empirically verified against
# .planning/phases/46-.../wave0-evidence/probe3-full-composer.jsonl
# (5 Phase headers + 2 "Ground Truths" + 1 "Assumption Audit" + 1
# "Verdict" all fired in that real capture).
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
# Data types
# (Inline-copied from scripts/check-routing.py — Prompt dataclass shape.)
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
    """Parse a Markdown routing/output-structure catalog.

    Returns (positives, negatives). Rows are classified by the prefix of
    the id cell: `P*` -> positive, `N*` -> negative. Other ids are ignored.

    Raises FileNotFoundError if path missing, ValueError on empty result.
    Verdict strings are NOT validated against an enum here — 46-04 will
    define the calibrated expectations.
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
# Structured walker
# (Inline-copied verbatim from scripts/check-routing.py:_walk.)
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


def _signal_a_invocations(parsed_lines: list[object]) -> set[str]:
    """Return the set of sub-skill techniques explicitly invoked at the
    orchestrator boundary via Skill/Agent/Task tool_use envelopes whose
    routing fields (skill / subagent_type) name `first-principles:<technique>`.

    Mirrors Phase 45 v2.1 Signal A discipline: inspect only routing fields
    (not the entire input dict — would catch sub-skill names appearing in
    prompt/args text).
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
    invoked = _signal_a_invocations(parsed_lines)
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
# Transport: invoke claude -p per prompt
# (Inline-copied verbatim from scripts/check-routing.py:_run_prompt_to and
# _run_prompt_n_times — DO NOT EDIT the flag list. The K-of-N loop and
# the per-prompt file naming convention (<id>.jsonl vs <id>-run<n>.jsonl)
# are also inline-copied.)
# ---------------------------------------------------------------------------


def _run_prompt_to(prompt: Prompt, plugin_dir: Path, out_path: Path) -> Path:
    """Issue one prompt via `claude -p` and capture the stream-json log.

    Transport per D-10 (verbatim, copied from check-routing.py):
        claude -p --plugin-dir <path> --no-session-persistence \
          --output-format stream-json --verbose \
          --permission-mode bypassPermissions <prompt>
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
) -> list[OutputStructure]:
    """Run a single prompt N times and return a list of N OutputStructure values.

    When repeat == 1, writes to <id>.jsonl (legacy parity).
    When repeat > 1, writes to <id>-run<n>.jsonl (1-indexed, n in 1..repeat).
    """
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
# Battery driver
# (Inline-copied verbatim from scripts/check-routing.py.)
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
        match_count = sum(1 for v in verdicts if _verdict_matches(v, prompt.expected))
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
                    match_flag = 1 if _verdict_matches(actual, prompt.expected) else 0
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
_FIXTURE_NONE = "\n".join(
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


def _run_one_fixture(
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


def self_test() -> int:
    """Validate detection logic against in-script fixtures, plus the
    Probe 3 sanity feed when its local-only capture is present
    (soft-skipped otherwise — 66 review WR-05). No claude invocation.
    """
    fixtures: list[tuple[str, str, OutputStructure]] = [
        ("focused_pre_mortem", _FIXTURE_FOCUSED_PREMORTEM, "focused-pre-mortem"),
        ("focused_inversion", _FIXTURE_FOCUSED_INVERSION, "focused-inversion"),
        # LOAD-BEARING: prevents Pitfall 1 (v1-style false-positive).
        ("full_composer_LOAD_BEARING", _FIXTURE_FULL_COMPOSER, "full-composer"),
        ("ambiguous", _FIXTURE_AMBIGUOUS, "ambiguous"),
        ("none", _FIXTURE_NONE, "none"),
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
    ]
    all_passed = True
    for name, body, expected in fixtures:
        if not _run_one_fixture(name, body, expected):
            all_passed = False

    # Fixture 8 — Probe 3 sanity feed (soft-skip when the local-only
    # capture is absent — 66 review WR-05; None means skipped).
    probe3_result = _run_probe3_sanity_feed()
    if probe3_result is False:
        all_passed = False

    # K>N rejection self-test (parallel to check-routing.py and
    # check-sub-skill-routing.py): --repeat 2 --min-pass 3 must exit 2
    # before any I/O.
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

    # Fixture 9 — NOT-any-focused semantic comparator assertions
    _not_any_cases: list[tuple[OutputStructure, str, bool]] = [
        ("none", "NOT-any-focused", True),
        ("full-composer", "NOT-any-focused", True),
        ("ambiguous", "NOT-any-focused", True),
        ("focused-pre-mortem", "NOT-any-focused", False),
        ("focused-inversion", "focused-inversion", True),
        ("none", "focused-pre-mortem", False),
    ]
    for actual_v, expected_v, want in _not_any_cases:
        got = _verdict_matches(actual_v, expected_v)
        if got is not want:
            print(
                f"self-test FAIL: _verdict_matches({actual_v!r}, {expected_v!r}) "
                f"expected {want}, got {got}",
                file=sys.stderr,
            )
            all_passed = False

    probe3_counted = 1 if probe3_result is not None else 0
    fixture_total = (
        len(fixtures) + probe3_counted + 1 + len(_not_any_cases)
    )  # +probe3 when present, +1 K>N guard, +NOT-any-focused assertions
    skip_note = (
        "" if probe3_result is not None
        else " (Fixture 8 probe3 sanity feed skipped — local capture absent)"
    )
    if all_passed:
        print(f"self-test PASS ({fixture_total} fixtures){skip_note}")
        return 0
    return 1


# ---------------------------------------------------------------------------
# Main / CLI
# (Inline-copied verbatim from scripts/check-routing.py:_default_out_dir,
# build_parser, main — K>N pre-flight guard preserved at lines 753-772 of
# the parent. Default thresholds set to calibrated gating values 4/1 per
# Phase 65 gap-closure: all four P rows and the sole N1 control must pass.)
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
            "Output directory for per-prompt .jsonl + scores.tsv + verdict.txt "
            "(default: /tmp/check-focused-output-<UTC-timestamp>/)."
        ),
    )
    p.add_argument(
        "--p-threshold",
        type=int,
        default=4,
        help=(
            "Min P-cases matching expected structure for battery PASS "
            "(default: 4 — all four P rows in the calibrated FU-21 catalog "
            "must pass)."
        ),
    )
    p.add_argument(
        "--n-threshold",
        type=int,
        default=1,
        help=(
            "Min N-cases matching expected for battery PASS "
            "(default: 1 — the sole over-trigger negative control N1 must pass)."
        ),
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

    # K>N pre-flight guard — validated BEFORE any I/O (verbatim parallel
    # to check-routing.py:T-36-01 lines 753-772).
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
