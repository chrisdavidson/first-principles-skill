#!/usr/bin/env python3
"""Re-derives the pre-mortem/adversarial-pass shape reading over a set of
Markdown captures, and separately feeds the same text through the frozen
`_battery_core` classifier. Rebuilds two corrections that previously existed
only as prose in `PLAN-premortem-wiring.md`: it anchors on every occurrence
of the case-insensitive `pre-mortem`/`adversarial pass` marker rather than
only the first, and it anchors on both spellings rather than only the older
one. A window drawn forward from each anchor line is scored for a
past-tense failure premise, an enumerated cause list, named clusters, and a
per-cluster disposition (a plan change or a named accepted risk); present
and shape-complete are reported per file and in aggregate, alongside the
fired-technique set, composer-structure hit count, and verdict
`_battery_core.classify()` returns for the same text.

This is a developer tool, never registered in the battery or in CI --
`--self-test` is its own offline control battery, exercised by a human or
by the pre-commit hooks that regenerate the claim surface after a new file
lands under `scripts/`.

Usage:
    python3 scripts/measure-adversarial-pass.py --score FILE.md [FILE.md ...]
    python3 scripts/measure-adversarial-pass.py --classify FILE.md [FILE.md ...]
    python3 scripts/measure-adversarial-pass.py --self-test

Exit codes:
    0  success -- score/classify printed, or every self-test control passed
    1  a path argument failed validation, an empty file set was given, or a
       self-test control failed
"""

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from pathlib import Path

REPO_ROOT: Path = Path(__file__).resolve().parents[1]

# Anchor widened to both spellings -- the second documented instrument
# correction (Phase 5's own capture emits the record under a heading that
# never contains the literal "pre-mortem").
_ANCHOR_RE = re.compile(r"pre-mortem|adversarial pass", re.IGNORECASE)

WINDOW_LINES = 30  # retained only as the fallback bound; see _window_lines().

# A record's window ends at the next top-level heading, not at a fixed line
# count -- the THIRD documented instrument correction, found by the Phase 48
# live reading (MEAS-03) rather than by inspection.
#
# The fixed 30-line span was wrong in both directions, and the same constant
# caused both failures:
#
#   too long  -- `Q-P1.md`'s baseline pre-mortem is a single sentence, and the
#                30 lines after it hold 12 list items belonging to output
#                section 6. Those were counted as causes, giving a spurious
#                baseline reading of 6 where the correct answer is 0.
#   too short -- the fresh `Q-P3` capture emits 15 causes and 6 clusters before
#                its `**Dispositions:**` block, which therefore begins ~40
#                lines past the anchor. The window never reached it and the
#                record scored `disposition: no` -- a false negative on a
#                record that satisfies the contract in full, verified by
#                reading it.
#
# Scoping to the section the contract itself defines removes both. Confirmed
# invariant: the ten frozen baseline files still return present 6/10 and
# shape-complete 3/10 under this window, the same aggregates the two earlier
# and differently-windowed instruments produced.
_SECTION_BREAK_RE = re.compile(r"^#{1,2}\s+\S")

# Bare "cluster"/"clusters" as a noun, or the "structural weakness(es)"
# phrase -- deliberately excludes the adjective "clustered" standing alone,
# which describes raw causes without naming a grouping (the DEMO ticket
# triage capture uses "clustered causes" this way with no named clusters).
_CLUSTER_RE = re.compile(r"\bclusters?\b|\bstructural weakness\w*\b", re.IGNORECASE)

_DISPOSITION_RE = re.compile(r"\bplan change\b|\baccepted risk\b", re.IGNORECASE)

_PREMISE_RE = re.compile(r"\bfailed\b|\bwent up\b", re.IGNORECASE)

_CAUSE_KEYWORD_RE = re.compile(r"\bcause(?:s|d)?\b", re.IGNORECASE)
_LIST_ITEM_RE = re.compile(r"^\s*(?:\d+\.|-|\*)\s+\S")


@dataclass
class Shape:
    present: bool
    premise: bool | None
    causes: int | None
    clusters: bool | None
    disposition: bool | None
    shape_complete: bool


def _anchor_line_numbers(lines: list[str]) -> list[int]:
    """1-indexed line numbers of every anchor match -- every occurrence,
    not the first (the first documented instrument correction)."""
    return [i + 1 for i, line in enumerate(lines) if _ANCHOR_RE.search(line)]


def _window_lines(lines: list[str], anchor_line: int, span: int = WINDOW_LINES) -> list[str]:
    """The record's own section: anchor line to the next top-level heading.

    `span` bounds the scan so a document with no subsequent heading cannot
    make the window the whole file; it is a backstop, not the boundary.
    A heading that itself mentions the record is not a break, so the
    `## Adversarial pass (process output)` anchor does not terminate its
    own section.
    """
    start = anchor_line - 1
    hard_end = min(len(lines), start + max(span, 200))
    out: list[str] = []
    for i in range(start, hard_end):
        stripped = lines[i].strip()
        if i > start and _SECTION_BREAK_RE.match(stripped):
            if "adversarial" not in stripped.lower() and "pre-mortem" not in stripped.lower():
                break
        out.append(lines[i])
    return out


def _count_causes(window: list[str]) -> int:
    """Count the enumerated causes following the first cause-keyword mention
    in the window. Returns zero when the causes are written inline inside a
    prose paragraph with no enumerated list before the grouping -- a true
    reading, not a miss (the Q-P2 fixture in the frozen baseline is the
    reference case)."""
    keyword_idx = None
    for idx, line in enumerate(window):
        if _CAUSE_KEYWORD_RE.search(line):
            keyword_idx = idx
            break
    if keyword_idx is None:
        return 0
    # Prefer an inline semicolon list on the keyword's own line -- the raw,
    # unfiltered enumeration ("Causes written before filtering: a; b; c")
    # precedes any later clustering and must not be shadowed by a numbered
    # cluster list appearing further down the same window.
    keyword_line = window[keyword_idx]
    keyword_match = _CAUSE_KEYWORD_RE.search(keyword_line)
    after_keyword = keyword_line[keyword_match.end() :]
    colon_idx = after_keyword.find(":")
    if colon_idx != -1:
        segment = after_keyword[colon_idx + 1 :]
        pieces = [p for p in segment.split(";") if p.strip()]
        if len(pieces) > 1:
            return len(pieces)
    tail = window[keyword_idx:]
    items: list[str] = []
    started = False
    for line in tail:
        if _LIST_ITEM_RE.match(line):
            items.append(line)
            started = True
        elif started and not line.strip():
            break
    if items:
        return len(items)
    return 0


def score_text(text: str) -> Shape:
    lines = text.splitlines()
    anchors = _anchor_line_numbers(lines)
    if not anchors:
        return Shape(
            present=False,
            premise=None,
            causes=None,
            clusters=None,
            disposition=None,
            shape_complete=False,
        )
    premise = False
    clusters = False
    disposition = False
    causes = 0
    for anchor_line in anchors:
        window = _window_lines(lines, anchor_line)
        joined = "\n".join(window)
        if _PREMISE_RE.search(joined):
            premise = True
        if _CLUSTER_RE.search(joined):
            clusters = True
        if _DISPOSITION_RE.search(joined):
            disposition = True
        causes = max(causes, _count_causes(window))
    return Shape(
        present=True,
        premise=premise,
        causes=causes,
        clusters=clusters,
        disposition=disposition,
        shape_complete=bool(premise and clusters and disposition),
    )


def score_file(path: Path) -> Shape:
    return score_text(path.read_text(encoding="utf-8"))


def _validate_input_path(raw: str) -> Path:
    """Resolve `raw` and refuse it unless it lands inside the repository and
    ends in `.md` -- the shape `check-quality-harness.py`'s `_CATALOG_ID_RE`
    applies to catalog ids before they become filesystem paths, applied
    here to a path argument directly."""
    candidate = Path(raw)
    try:
        resolved = candidate.resolve()
    except OSError as exc:
        raise SystemExit(f"measure-adversarial-pass: cannot resolve path {raw!r}: {exc}")
    if resolved != REPO_ROOT and REPO_ROOT not in resolved.parents:
        raise SystemExit(
            f"measure-adversarial-pass: refusing {raw!r} -- it resolves outside "
            f"the repository ({REPO_ROOT})"
        )
    if resolved.suffix.lower() == ".jsonl":
        raise SystemExit(
            f"measure-adversarial-pass: refusing {raw!r} -- a '.jsonl' file is "
            "the raw orchestrator transport log (every event), not the "
            "sub-agent's extracted analysis. For a delegated composer "
            "dispatch, the top-level type=assistant events in that log are "
            "the orchestrator's own summary, not the sub-agent's analysis -- "
            "feeding it here reads the wrong channel. Pass the '.md' "
            "extraction instead."
        )
    if resolved.suffix.lower() != ".md":
        raise SystemExit(
            f"measure-adversarial-pass: refusing {raw!r} -- only '.md' paths are accepted"
        )
    if not resolved.is_file():
        raise SystemExit(f"measure-adversarial-pass: {raw!r} does not exist or is not a file")
    return resolved


def _cell(value: object) -> str:
    if value is None:
        return "-"
    if isinstance(value, bool):
        return "yes" if value else "no"
    return str(value)


def cmd_score(paths: list[Path]) -> int:
    if not paths:
        print("ANTI-VACUITY: --score received an empty file set -- this is a finding, not a silent pass")
        return 1
    rows = [(p, score_file(p)) for p in paths]
    print("| file | present | premise | causes | clusters | disposition |")
    print("|---|---|---|---|---|---|")
    for path, shape in rows:
        print(
            f"| {path.name} | {_cell(shape.present)} | {_cell(shape.premise)} | "
            f"{_cell(shape.causes)} | {_cell(shape.clusters)} | {_cell(shape.disposition)} |"
        )
    present_total = sum(1 for _, shape in rows if shape.present)
    complete_total = sum(1 for _, shape in rows if shape.shape_complete)
    print(f"present {present_total}/{len(rows)}")
    print(f"shape-complete {complete_total}/{len(rows)}")
    return 0


def _load_battery_core():
    scripts_dir = str(REPO_ROOT / "scripts")
    if scripts_dir not in sys.path:
        sys.path.insert(0, scripts_dir)
    import _battery_core as bc  # noqa: PLC0415 -- deliberate late import, see module docstring

    return bc


def cmd_classify(paths: list[Path]) -> int:
    if not paths:
        print("ANTI-VACUITY: --classify received an empty file set -- this is a finding, not a silent pass")
        return 1
    bc = _load_battery_core()
    for path in paths:
        text = path.read_text(encoding="utf-8")
        hits = bc._technique_hits(text)
        fired = {tech for tech, n in hits.items() if n >= bc.MIN_HEADER_HITS}
        composer_hits = bc._composer_structure_hits(text)
        verdict = bc.classify(fired, composer_hits)
        print(
            f"{path.name}: fired={sorted(fired)} len(fired)={len(fired)} "
            f"composer_structure_hits={composer_hits} verdict={verdict}"
        )
    return 0


def _report(failures: list[str], name: str, ok: bool) -> None:
    print(f"{'PASS' if ok else 'FAIL'}: {name}")
    if not ok:
        failures.append(name)


def run_self_test() -> int:
    failures: list[str] = []

    # Control 1: the first anchor match is meta-discussion; the real
    # section sits far enough below that a first-match-only anchor would
    # miss it entirely. Fixes the failure that scored both root demos "no"
    # on every column.
    padding = "\n".join(f"Filler paragraph {i} of unrelated prose." for i in range(1, 40))
    first_match_text = (
        "This document mentions pre-mortem only as a technique name in passing, "
        "with no analysis attached.\n"
        + padding
        + "\n\n"
        "## Pre-mortem (Phase 5 process output)\n"
        "Premise restated: it is twelve months later and the launch already failed.\n"
        "Causes written before filtering:\n"
        "- alpha risk surfaced late\n"
        "- beta risk surfaced late\n"
        "- gamma risk surfaced late\n"
        "Clustered into two structural weaknesses:\n"
        "1. Alpha weakness -> Plan change: fix alpha first.\n"
        "2. Beta weakness -> Accepted risk: monitor beta on a fixed schedule.\n"
    )
    shape = score_text(first_match_text)
    ok = bool(
        shape.present
        and shape.premise
        and shape.clusters
        and shape.disposition
        and shape.causes
        and shape.causes > 0
    )
    _report(failures, "control-anchor-on-every-match-not-first", ok)

    # Control 2: the anchor is widened to the "Adversarial pass" heading --
    # the literal "pre-mortem" never occurs. Fixes the failure that scored
    # the wired body's own output worse than the baseline it improves on.
    heading_only_text = (
        "## Adversarial pass (process output)\n"
        "The plan has already failed six months on.\n"
        "Cause: the vendor contract lapsed silently.\n"
        "Accepted risk: renew reminders scheduled with a named owner.\n"
    )
    assert "pre-mortem" not in heading_only_text.lower()
    shape = score_text(heading_only_text)
    ok = bool(shape.present and shape.premise and shape.disposition)
    _report(failures, "control-anchor-widened-to-adversarial-pass-heading", ok)

    # Negative control: no anchor at all.
    negative_text = "This document discusses migration cost trade-offs with no risk-review terminology.\n"
    shape = score_text(negative_text)
    ok = (not shape.present) and (not shape.shape_complete)
    _report(failures, "control-negative-no-anchor", ok)

    # Anti-vacuity control: an empty input set is itself a finding, never a
    # silent pass.
    ok = cmd_score([]) != 0
    _report(failures, "control-anti-vacuity-empty-score-input", ok)
    ok = cmd_classify([]) != 0
    _report(failures, "control-anti-vacuity-empty-classify-input", ok)

    # .jsonl refusal control -- offline, against a path that need not exist.
    refused = False
    try:
        _validate_input_path("tests/synthetic-control/example.jsonl")
    except SystemExit as exc:
        refused = ".jsonl" in str(exc)
    _report(failures, "control-jsonl-argument-refused", refused)

    if failures:
        print(f"SELF-TEST: FAILED ({len(failures)} failing control)")
        return 1
    print("SELF-TEST: PASSED")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Re-derive the pre-mortem/adversarial-pass shape reading, "
        "or feed capture text through the frozen output-structure classifier."
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--score", nargs="+", metavar="FILE.md", help="score files for pre-mortem shape")
    group.add_argument("--classify", nargs="+", metavar="FILE.md", help="feed files through _battery_core.classify()")
    group.add_argument("--self-test", action="store_true", help="run the offline control battery")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.self_test:
        return run_self_test()
    if args.score is not None:
        paths = [_validate_input_path(raw) for raw in args.score]
        return cmd_score(paths)
    if args.classify is not None:
        paths = [_validate_input_path(raw) for raw in args.classify]
        return cmd_classify(paths)
    parser.error("one of --score, --classify, --self-test is required")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
