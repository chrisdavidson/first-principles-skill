#!/usr/bin/env python3
# /// script
# requires-python = ">=3.12"
# dependencies = []
# ///
"""PROV-GUARD gate: verify `*Provenance: read-at-source.*` ground truths against a
stored generation capture.

Parses an analysis's section 3 (Ground Truths), joins every read-at-source GT to the
real `WebFetch`/`Read` call in the run's `.jsonl` capture that fetched its cited
source, and requires every numeric/currency literal the GT states to appear verbatim
in that source's retrieved text (PROV-01, PROV-02, PROV-03). Findings land as named
`_DEFECT_RECORD_FIELDS` columns (PROV-05) via `provenance_defect_record`.

Usage:
    python3 scripts/check-provenance.py [--self-test]

Exit codes:
    0  all checks passed
    1  validation/content failure (a source is unmatched or unreadable, a literal is
       unlocated or misattributed, or a self-test control behaves wrongly)
    2  environment error (Python <3.12, the fixture files are missing)

--self-test: runs an offline control battery of positive, negative and anti-masking
             controls (D-16), fully in-memory or tempdir-scoped -- no network access
             and no live Claude session.

## What this gate does not assert

1. It verifies that a stated number appears in the retrieved text of the source the
   analysis names. It does not verify the number means what the analysis says it
   means, nor that the chain citing it is valid inference -- that is backlog 999.4.
2. The literal regex (D-01, locked) also matches digit runs that are the tail of an
   alphanumeric identifier: `x86` yields `86`, `EC2` yields `2`. These still verify,
   because the identifier appears verbatim in the retrieved text, but carry no
   independent evidentiary weight. This is expected behaviour, not a parser bug.
3. Whole-span (bold or quoted) matching was measured and rejected -- 4/11 bold spans
   and 4/8 quoted spans located, because bold spans are paraphrase envelopes and
   quotes carry the analyst's own elisions. Do not resurrect it as a "cleaner" rule.
4. PROV-04's no-network control blocks `socket`; it does not cover a `subprocess`
   shell-out. Stated residual (D-14).

Phase 6 note: `scripts/check-firewall-battery.sh:346-349` already registers a battery
gate literally named `GATE-01` (bound to `check-agent.py`), so this gate must be
registered under a distinct id such as `PROV-GUARD` when Phase 6 wires it in.
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import re
import socket
import sys
import tempfile
from dataclasses import dataclass
from pathlib import Path
from unittest import mock
from urllib.parse import urlsplit


# Repo-anchored, not caller-supplied: check-agent.py's rationale reproduced here --
# a constant derived from __file__ keeps the gate cwd-independent and its target
# cannot be silently re-pointed by an argv/env override.
REPO_ROOT: Path = Path(__file__).resolve().parents[1]
_FIXTURE_CAPTURE: Path = REPO_ROOT / "tests" / "quality-provenance-v8.24" / "PR-P1.jsonl"
_FIXTURE_ANALYSIS: Path = REPO_ROOT / "tests" / "quality-provenance-v8.24" / "PR-P1.md"
_FIXTURE_SUBAGENT_TYPE: str = "first-principles:first-principles"

# D-02: hardcoded pins, not merely reflected from whatever the run computes -- the
# STEP0-08 pin-as-literal pattern. A silent drop in extraction must fail the live
# leg, not pass with a smaller number.
_EXPECTED_SOURCES: int = 7
_EXPECTED_LITERALS: int = 35

# Deliberately NOT derived from the fixture's own 532-char minimum retrieved-text
# length, which would make the floor fixture-shaped. 50 is clearly below any real
# fetched page and clearly above an empty or near-empty fetch.
_MIN_RETRIEVED_TEXT_CHARS: int = 50


# ---------------------------------------------------------------------------
# Harness import (one-way). check-quality-harness.py never imports this file.
# ---------------------------------------------------------------------------

_HARNESS_PATH: Path = REPO_ROOT / "scripts" / "check-quality-harness.py"
_spec = importlib.util.spec_from_file_location("_quality_harness", _HARNESS_PATH)
_mod = importlib.util.module_from_spec(_spec)  # type: ignore[arg-type]
sys.modules["_quality_harness"] = _mod  # Python 3.13+ dataclass compat -- must precede exec_module
_spec.loader.exec_module(_mod)  # type: ignore[union-attr]

_slice_sections = _mod._slice_sections
_capture_subagent_tool_calls = _mod._capture_subagent_tool_calls
detect_defects = _mod.detect_defects
read_defect_incidence = _mod.read_defect_incidence
_DEFECT_RECORD_FIELDS = _mod._DEFECT_RECORD_FIELDS


def _require_python_version() -> None:
    if sys.version_info < (3, 12):
        sys.stderr.write(
            f"scripts/check-provenance.py requires Python >=3.12 "
            f"(running {sys.version_info.major}.{sys.version_info.minor}).\n"
        )
        sys.exit(2)


# ---------------------------------------------------------------------------
# PROV-01: section-3 parsing
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class GroundTruth:
    """One `- **GT-n**` list item parsed from an analysis's section 3."""

    gt_id: str
    label: str
    claim_body: str
    source: str
    literals: tuple[str, ...]


# A section-3 list item: "- **GT-1** <rest of line>". `re.M` so `$` anchors each
# GT to its own line -- every GT in the fixture is single-line.
_GT_LINE_RE = re.compile(r"^\-\s+\*\*(GT-\d+\??)\*\*\s+(.*)$", re.M)

# The literal label FORM, never the bare "read-at-source" substring: the fixture's
# section 3 contains "read-at-source" 26 times total (7 in this label, 19 more
# inside each GT's own "read-at-source: <location>" clause), but the label form
# itself only 7 times.
_READ_AT_SOURCE_LABEL = "*Provenance: read-at-source.*"

_PROVENANCE_LABEL_RE = re.compile(r"\*Provenance:\s*([a-zA-Z][a-zA-Z\-]*)\.\*")

# D-01, locked verbatim. No word-boundary anchor: it deliberately also matches a
# digit run that is the tail of an alphanumeric identifier (see limit 2 above).
_LITERAL_RE = re.compile(r"\$?\d[\d,]*(?:\.\d+)?")


def _claim_body(line_body: str) -> str:
    """Return the claim substring preceding the '— source: ...' clause.

    Without this split, digits inside the 'read-at-source: <location>'
    description are scanned too and the literal count lands on 37, not 35.
    """
    return re.split(r"\s+—\s+source:", line_body)[0]


def _source_string(line_body: str) -> str:
    """Return the text between '— source:' and the following ';', or the
    '*Provenance:' label if the source clause carries no semicolon, stripped.
    """
    m = re.search(r"—\s+source:\s*(.*)", line_body)
    if not m:
        return ""
    rest = m.group(1)
    if ";" in rest:
        return rest.split(";", 1)[0].strip()
    return rest.split("*Provenance:", 1)[0].strip()


def _label(line_body: str) -> str:
    """Return the GT's provenance label word ("read-at-source", "unverified", ...).

    Checks the exact `_READ_AT_SOURCE_LABEL` form as a substring first -- see
    that constant's own comment for why the bare substring is rejected.
    """
    if _READ_AT_SOURCE_LABEL in line_body:
        return "read-at-source"
    m = _PROVENANCE_LABEL_RE.search(line_body)
    return m.group(1) if m else ""


def _parse_ground_truths(section3: str) -> list[GroundTruth]:
    """Parse every '- **GT-n**' list item in `section3` into a `GroundTruth`.

    Includes every GT regardless of its provenance label; callers filter on
    `label == "read-at-source"`.
    """
    out: list[GroundTruth] = []
    for m in _GT_LINE_RE.finditer(section3):
        gt_id = m.group(1)
        line_body = m.group(2)
        claim = _claim_body(line_body)
        out.append(
            GroundTruth(
                gt_id=gt_id,
                label=_label(line_body),
                claim_body=claim,
                source=_source_string(line_body),
                literals=tuple(_LITERAL_RE.findall(claim)),
            )
        )
    return out


def parse_analysis(analysis_text: str) -> list[GroundTruth]:
    """Slice section 3 (Ground Truths) out of an analysis and parse its GT list.

    Lets `SectionResolutionError` from `_slice_sections` propagate -- a document
    the parser cannot read must fail loudly, never report zero findings.
    """
    section3 = _slice_sections(analysis_text)[3]
    return _parse_ground_truths(section3)


# ---------------------------------------------------------------------------
# PROV-02: source <-> fetch join
# ---------------------------------------------------------------------------

_BACKTICK_RE = re.compile(r"`([^`]+)`")


def _join_key(source: str) -> str:
    """Return the join key used to bind a GT's source string to a capture triple.

    If `source` contains backticked tokens, return the LAST one -- the verbatim
    filename join for the two doc-name-plus-backticked-filename sources. Otherwise
    return the bare source string stripped of a leading http(s) scheme and of any
    trailing '/' or '.'.

    Exact-URL canonicalization is rejected: it fails outright on the two
    backticked-filename GTs, whose source strings are not URLs at all -- "AWS
    Lambda Developer Guide" is not a resolvable scheme+host.
    """
    tokens = _BACKTICK_RE.findall(source)
    if tokens:
        return tokens[-1]
    key = source.strip()
    key = re.sub(r"^https?://", "", key)
    return key.rstrip("/.")


def _anchored_match(key: str, target: str) -> bool:
    """CR-01: anchor the source<->fetch join instead of raw substring
    containment, so a key can never bind by mere prefix/substring collision
    (e.g. 'example.com' must not match '...ref=example.com-mirror', and
    'lambda' must not match inside 'lambda-old'). Both sides are parsed with
    `urllib.parse.urlsplit` -- never a raw substring test.

    `key` is either a host+path string (scheme-stripped, from a bare GT
    source with a path) or a bare token (a backticked filename, or a bare
    hostname with no path):

    - If `key` contains '/', treat it as host+path: require exact host
      (netloc) equality (case-insensitive) AND exact path equality (mod a
      trailing '/'). A trailing scheme is added back (`https://`) purely so
      `urlsplit` parses the netloc/path split correctly; the scheme itself is
      never compared.
    - Otherwise, treat `key` as a single bare token: it binds either as an
      exact netloc match (a bare-hostname source) or as an exact
      `/`-delimited path segment of the target's path (a backticked filename
      cited without its containing directory) -- never as a substring
      landing mid-segment.
    """
    target_parts = urlsplit(target)
    if "/" in key:
        key_parts = urlsplit("https://" + key)
        return (
            key_parts.netloc.lower() == target_parts.netloc.lower()
            and key_parts.path.rstrip("/") == target_parts.path.rstrip("/")
        )
    if key == target_parts.netloc:
        return True
    return key in target_parts.path.split("/")


def _bind(
    gt: GroundTruth, tool_calls: list[tuple[str, str, str]]
) -> tuple[int, tuple[str, str, str], tuple[int, ...]] | None:
    """Bind `gt` to the capture triple(s) whose target anchors on gt's join
    key (see `_anchored_match` -- never a raw substring test).

    Zero matches is unmatched (returns None). Two or more matches with
    DIFFERING `target` strings is a genuine ambiguous join -- an ambiguous
    join must never be silently resolved by taking the first (measured: no
    such collision on the fixture) -- and also returns None (CR-01/CR-02).

    Two or more matches that all share the SAME `target` string (e.g. a
    WebFetch retried after a transient failure, or fetched twice for two
    different literals) are NOT ambiguous: they bind to the first occurrence,
    and every matching index is returned alongside it so the caller can mark
    all of them bound rather than reporting the retry as unmatched (CR-02).

    Returns `(index, triple, all_matched_indices)` on a successful bind, so
    `verify()` never needs to re-derive the index via a value-equality
    `tool_calls.index(triple)` lookup.
    """
    key = _join_key(gt.source)
    if not key:
        return None
    matches = [(i, t) for i, t in enumerate(tool_calls) if _anchored_match(key, t[1])]
    if not matches:
        return None
    distinct_targets = {t[1] for _, t in matches}
    if len(distinct_targets) > 1:
        return None
    first_index, first_triple = matches[0]
    return first_index, first_triple, tuple(i for i, _ in matches)


# ---------------------------------------------------------------------------
# PROV-03 location, D-03/D-04/D-06/D-08 finding families, PROV-05 record
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class ProvenanceResult:
    """The nine D-11 counters plus underscore-prefixed audit lists.

    The audit lists let a caller (the D-15 mutation control, the self-test) assert
    on a SPECIFIC gt_id/literal rather than merely on a count.
    """

    provenance_labels: int
    unmatched_sources: int
    unreadable_sources: int
    literals_checked: int
    unlocated_literals: int
    misattributed_literals: int
    zero_literal_gts: int
    orphan_fetches: int
    provenance_flag: int
    _unmatched_gt_ids: tuple[str, ...]
    _unreadable_gt_ids: tuple[str, ...]
    _zero_literal_gt_ids: tuple[str, ...]
    _unlocated_pairs: tuple[tuple[str, str], ...]
    _misattributed_pairs: tuple[tuple[str, str], ...]
    _orphan_targets: tuple[str, ...]


def verify(
    analysis_text: str, capture_path: Path, subagent_type: str, analysis_id: str
) -> ProvenanceResult:
    """PROV-02/PROV-03 engine: join, locate, and roll every read-at-source GT into
    a `ProvenanceResult`.

    Calls `_capture_subagent_tool_calls` WITHOUT a try/except wrapper -- a
    `ValueError` from a never-dispatched subagent must propagate (constraint 5).

    Comparison is comma-normalized on both sides (the literal and the retrieved
    text each have ',' stripped before the substring test); '$' is never stripped.
    """
    ground_truths = parse_analysis(analysis_text)
    read_gts = [gt for gt in ground_truths if gt.label == "read-at-source"]

    tool_calls = _capture_subagent_tool_calls(capture_path, subagent_type)

    # Per-source normalized corpus, built once -- the D-04 cross-source lookup is
    # then near-free.
    corpus: dict[int, str] = {i: t[2].replace(",", "") for i, t in enumerate(tool_calls)}

    bound_indices: set[int] = set()
    unmatched_ids: list[str] = []
    unreadable_ids: list[str] = []
    zero_literal_ids: list[str] = []
    unlocated_pairs: list[tuple[str, str]] = []
    misattributed_pairs: list[tuple[str, str]] = []
    literals_checked = 0

    for gt in read_gts:
        bound = _bind(gt, tool_calls)
        if bound is None:
            unmatched_ids.append(gt.gt_id)
            continue
        idx, triple, all_indices = bound
        bound_indices.update(all_indices)
        retrieved = triple[2]

        # D-08: an unreadable bound source is counted INSTEAD OF running literal
        # location for that GT, so an infrastructure failure is never mislabelled
        # as fabrication.
        if len(retrieved) < _MIN_RETRIEVED_TEXT_CHARS:
            unreadable_ids.append(gt.gt_id)
            continue

        # D-03: zero checkable literals is reported, never failed.
        if not gt.literals:
            zero_literal_ids.append(gt.gt_id)
            continue

        own_corpus = retrieved.replace(",", "")
        for literal in gt.literals:
            literals_checked += 1
            norm = literal.replace(",", "")
            if norm in own_corpus:
                continue
            # D-04: absent from the bound source but present in a DIFFERENT
            # fetched source is a distinct finding from absent-everywhere.
            found_elsewhere = any(
                j != idx and norm in other for j, other in corpus.items()
            )
            if found_elsewhere:
                misattributed_pairs.append((gt.gt_id, literal))
            else:
                unlocated_pairs.append((gt.gt_id, literal))

    # D-06: a tool call bound to no read-at-source GT is an orphan fetch --
    # counted and reported, never failed.
    orphan_targets = [t[1] for i, t in enumerate(tool_calls) if i not in bound_indices]

    unmatched_sources = len(unmatched_ids)
    unreadable_sources = len(unreadable_ids)
    unlocated_literals = len(unlocated_pairs)
    misattributed_literals = len(misattributed_pairs)
    zero_literal_gts = len(zero_literal_ids)
    orphan_fetches = len(orphan_targets)
    provenance_flag = (
        1
        if (unmatched_sources or unreadable_sources or unlocated_literals or misattributed_literals)
        else 0
    )

    return ProvenanceResult(
        provenance_labels=len(read_gts),
        unmatched_sources=unmatched_sources,
        unreadable_sources=unreadable_sources,
        literals_checked=literals_checked,
        unlocated_literals=unlocated_literals,
        misattributed_literals=misattributed_literals,
        zero_literal_gts=zero_literal_gts,
        orphan_fetches=orphan_fetches,
        provenance_flag=provenance_flag,
        _unmatched_gt_ids=tuple(unmatched_ids),
        _unreadable_gt_ids=tuple(unreadable_ids),
        _zero_literal_gt_ids=tuple(zero_literal_ids),
        _unlocated_pairs=tuple(unlocated_pairs),
        _misattributed_pairs=tuple(misattributed_pairs),
        _orphan_targets=tuple(orphan_targets),
    )


def provenance_defect_record(analysis_text: str, analysis_id: str, result: ProvenanceResult) -> dict:
    """PROV-05: `detect_defects`'s 22-column record with the nine provenance keys
    overwritten from a real `ProvenanceResult` -- replacing the harness's "n/a"
    sentinel only when a capture was actually read. Does not modify
    `run_detect_defects`; this script owns its own single-row emission (D-09
    discretion, RESEARCH assumption A2).
    """
    record = detect_defects(analysis_text, analysis_id)
    record.update(
        {
            "provenance_labels": result.provenance_labels,
            "unmatched_sources": result.unmatched_sources,
            "unreadable_sources": result.unreadable_sources,
            "literals_checked": result.literals_checked,
            "unlocated_literals": result.unlocated_literals,
            "misattributed_literals": result.misattributed_literals,
            "zero_literal_gts": result.zero_literal_gts,
            "orphan_fetches": result.orphan_fetches,
            "provenance_flag": result.provenance_flag,
        }
    )
    return record


def record_to_tsv(record: dict) -> str:
    """Render `record` as a two-line TSV string (header + one data row) over
    `_DEFECT_RECORD_FIELDS`, so the round-trip through `read_defect_incidence` is
    exercisable.
    """
    header = "\t".join(_DEFECT_RECORD_FIELDS)
    row = "\t".join(str(record[f]) for f in _DEFECT_RECORD_FIELDS)
    return f"{header}\n{row}\n"


# ---------------------------------------------------------------------------
# --self-test (D-16): named control inventory, fully in-memory or
# tempdir-scoped -- no network access and no live Claude session. Every
# control adds its id to _covered_controls only after its OWN assertion
# passed for its OWN stated reason -- never merely "did not raise".
# ---------------------------------------------------------------------------

_covered_controls: set[str] = set()
_self_test_failures: list[str] = []


def _fail(control_id: str, msg: str) -> None:
    sys.stderr.write(f"check-provenance --self-test: FAIL — {control_id}: {msg}\n")
    _self_test_failures.append(control_id)


def _run_control(control_id: str, fn) -> None:
    """Run one control, recording pass/fail. A control signals failure by
    raising AssertionError (a plain `assert`) -- any other exception is a
    genuine bug in the control itself and is left to propagate.
    """
    try:
        fn()
    except AssertionError as exc:
        _fail(control_id, str(exc))
    else:
        _covered_controls.add(control_id)
        print(f"check-provenance --self-test: {control_id} PASS")


_SYNTH_DISPATCH_ID = "toolu_dispatch1"
_SYNTH_TARGET_KEY = {"WebFetch": "url", "Read": "file_path"}


def _synth_capture(
    tmpdir: Path, calls: list[tuple[str, str, str]], *, dispatch: bool = True
) -> Path:
    """Write a synthesized JSONL capture into `tmpdir`: one `Agent` dispatch
    event (unless `dispatch=False`) followed by one child `tool_use` +
    matching `tool_result` per `(tool_name, target, retrieved_text)` triple in
    `calls`. Mirrors the verified minimal event shape from 05-RESEARCH.md's
    "D-07 minimal synthetic Read-arm fixture" section exactly -- copy that
    shape, do not improvise a new one.
    """
    events: list[dict] = []
    if dispatch:
        events.append(
            {
                "type": "assistant",
                "message": {
                    "content": [
                        {
                            "type": "tool_use",
                            "id": _SYNTH_DISPATCH_ID,
                            "name": "Agent",
                            "input": {"subagent_type": _FIXTURE_SUBAGENT_TYPE},
                        }
                    ]
                },
            }
        )
    for i, (tool_name, target, retrieved_text) in enumerate(calls):
        call_id = f"toolu_call{i}"
        events.append(
            {
                "type": "assistant",
                "parent_tool_use_id": _SYNTH_DISPATCH_ID,
                "message": {
                    "content": [
                        {
                            "type": "tool_use",
                            "id": call_id,
                            "name": tool_name,
                            "input": {_SYNTH_TARGET_KEY[tool_name]: target},
                        }
                    ]
                },
            }
        )
        events.append(
            {
                "type": "user",
                "message": {
                    "content": [
                        {
                            "type": "tool_result",
                            "tool_use_id": call_id,
                            "content": retrieved_text,
                        }
                    ]
                },
            }
        )
    path = tmpdir / "synthetic.jsonl"
    path.write_text(
        "\n".join(json.dumps(e) for e in events) + "\n", encoding="utf-8"
    )
    return path


def _gt_line(
    gt_id: str,
    claim: str,
    source: str,
    *,
    label: str = "read-at-source",
    location: str = "synthesized location",
) -> str:
    """Build one section-3 GT list item in the exact form `_GT_LINE_RE` /
    `_source_string` / `_label` parse. The trailing 'read-at-source: <location>'
    clause is present regardless of `label` -- this is deliberate: it is what
    makes PROV01-labelform-negative's bare-substring trap realistic (every
    real GT in the fixture carries this clause whether or not it is actually
    read-at-source labelled).
    """
    return (
        f"- **{gt_id}** {claim} — source: {source}; read-at-source: {location}. "
        f"*Provenance: {label}.*"
    )


def _synth_analysis(gt_lines: list[str]) -> str:
    """Wrap `gt_lines` (already-built section-3 list items) in the smallest
    six-section skeleton `_slice_sections` resolves -- copied from
    check-quality-harness.py's `_selftest_gap5_conclusion_heading` in-line
    document (harness:6901-6949), trimmed to section 3's content only. Only
    section 3 is exercised by `parse_analysis`; sections 1/2/4/5/6 exist
    purely so `_slice_sections` resolves all six numbers in order.
    """
    gts = "\n".join(gt_lines)
    return f"""# 1. Problem Essence

**Core problem:** synthesized self-test fixture.

# 2. Assumptions Table

| Assumption | Type | Treatment | Verdict | Verification |
|---|---|---|---|---|
| placeholder | convention | Challenge before use | Accept — synthesized | n/a |

# 3. Ground Truths

{gts}

# 4. Derivation Chains

### Conclusion C1: synthesized

GT-1 (a)
-> synthesized conclusion

# 5. Abandoned Reasoning

None.

# 6. Conclusion

**Recommended approach:** synthesized.
"""


def _control_prov02_readarm_positive() -> None:
    """D-07 positive: a synthesized Read capture supplies the exact path a GT
    cites, carrying the GT's one literal. This is the only exercise the
    `Read` arm gets -- the committed capture's 2 `Read` calls are cited by no
    GT.
    """
    with tempfile.TemporaryDirectory() as d:
        tmp = Path(d)
        capture = _synth_capture(
            tmp,
            [("Read", "/tmp/fixture-source.txt", "the retrieved literal value is 42 " + "z" * _MIN_RETRIEVED_TEXT_CHARS)],
        )
        analysis = _synth_analysis(
            [_gt_line("GT-1", "a fact citing 42", "`/tmp/fixture-source.txt`")]
        )
        result = verify(analysis, capture, _FIXTURE_SUBAGENT_TYPE, "synthetic")
        got = (
            result.provenance_labels,
            result.unmatched_sources,
            result.unreadable_sources,
            result.literals_checked,
            result.unlocated_literals,
            result.misattributed_literals,
            result.zero_literal_gts,
            result.orphan_fetches,
            result.provenance_flag,
        )
        want = (1, 0, 0, 1, 0, 0, 0, 0, 0)
        assert got == want, f"D-11 counter tuple: got {got!r}, want {want!r}"


def _control_prov02_readarm_negative() -> None:
    """D-07 negative: the same GT, but the capture's Read supplies a
    DIFFERENT path -- the cited source was never actually read.
    """
    with tempfile.TemporaryDirectory() as d:
        tmp = Path(d)
        capture = _synth_capture(
            tmp,
            [("Read", "/tmp/other-file.txt", "the retrieved literal value is 42 " + "z" * _MIN_RETRIEVED_TEXT_CHARS)],
        )
        analysis = _synth_analysis(
            [_gt_line("GT-1", "a fact citing 42", "`/tmp/fixture-source.txt`")]
        )
        result = verify(analysis, capture, _FIXTURE_SUBAGENT_TYPE, "synthetic")
        assert result.unmatched_sources == 1, (
            f"expected 1 unmatched source, got {result.unmatched_sources}"
        )
        assert result._unmatched_gt_ids == ("GT-1",), (
            f"expected GT-1 named, got {result._unmatched_gt_ids!r}"
        )
        assert result.provenance_flag == 1, (
            f"expected provenance_flag=1, got {result.provenance_flag}"
        )


def _control_d08_unreadable_positive() -> None:
    """D-08 positive: the bound source's retrieved text is one character
    SHORTER than `_MIN_RETRIEVED_TEXT_CHARS`. Must count as unreadable, never
    as unmatched or as a fabrication, and its literal must not be counted
    into `literals_checked`.
    """
    with tempfile.TemporaryDirectory() as d:
        tmp = Path(d)
        short_text = "42 " + "z" * (_MIN_RETRIEVED_TEXT_CHARS - 4)
        assert len(short_text) == _MIN_RETRIEVED_TEXT_CHARS - 1
        capture = _synth_capture(tmp, [("Read", "/tmp/thin.txt", short_text)])
        analysis = _synth_analysis(
            [_gt_line("GT-1", "a fact citing 42", "`/tmp/thin.txt`")]
        )
        result = verify(analysis, capture, _FIXTURE_SUBAGENT_TYPE, "synthetic")
        assert result.unreadable_sources == 1, (
            f"expected 1 unreadable source, got {result.unreadable_sources}"
        )
        assert result.unmatched_sources == 0, (
            f"an unreadable source must not also count as unmatched, got {result.unmatched_sources}"
        )
        assert result.unlocated_literals == 0, (
            f"an unreadable source must not count as fabrication, got {result.unlocated_literals}"
        )
        assert result.literals_checked == 0, (
            f"an unreadable source's literal must not be counted, got {result.literals_checked}"
        )


def _control_d08_unreadable_negative() -> None:
    """D-08 negative: retrieved text one character ABOVE the floor and
    containing the literal -- pins the floor itself, not just the branch.
    """
    with tempfile.TemporaryDirectory() as d:
        tmp = Path(d)
        text = "42 " + "z" * (_MIN_RETRIEVED_TEXT_CHARS - 2)
        assert len(text) == _MIN_RETRIEVED_TEXT_CHARS + 1
        capture = _synth_capture(tmp, [("Read", "/tmp/thin.txt", text)])
        analysis = _synth_analysis(
            [_gt_line("GT-1", "a fact citing 42", "`/tmp/thin.txt`")]
        )
        result = verify(analysis, capture, _FIXTURE_SUBAGENT_TYPE, "synthetic")
        assert result.unreadable_sources == 0, (
            f"expected 0 unreadable sources, got {result.unreadable_sources}"
        )
        assert result.provenance_flag == 0, (
            f"expected provenance_flag=0, got {result.provenance_flag}"
        )


def _control_prov02_dispatch_raises() -> None:
    """Constraint 5 guard: a synthesized capture built WITHOUT the `Agent`
    dispatch event must make `_capture_subagent_tool_calls` raise `ValueError`,
    and `verify()` must let it propagate rather than converting it to a
    zero-finding result. This is the guard against reintroducing the
    conflation constraint 5 exists to close.
    """
    with tempfile.TemporaryDirectory() as d:
        tmp = Path(d)
        capture = _synth_capture(
            tmp,
            [("Read", "/tmp/fixture-source.txt", "the retrieved literal value is 42 " + "z" * _MIN_RETRIEVED_TEXT_CHARS)],
            dispatch=False,
        )
        analysis = _synth_analysis(
            [_gt_line("GT-1", "a fact citing 42", "`/tmp/fixture-source.txt`")]
        )
        try:
            verify(analysis, capture, _FIXTURE_SUBAGENT_TYPE, "synthetic")
        except ValueError:
            pass
        else:
            raise AssertionError(
                "verify() did not propagate ValueError for a never-dispatched subagent"
            )


def _labelform_analysis() -> str:
    """One read-at-source GT plus one GT that mentions the bare substring
    'read-at-source' in its own 'read-at-source: <location>' clause but
    carries the *unverified* label -- the shared fixture for the
    PROV01-labelform pair.
    """
    return _synth_analysis(
        [
            _gt_line("GT-1", "a fact citing 42", "`/tmp/a.txt`", label="read-at-source"),
            _gt_line("GT-2", "a fact citing 7", "`/tmp/b.txt`", label="unverified"),
        ]
    )


def _control_prov01_labelform_positive() -> None:
    """PROV-01 positive: the label-FORM GT is counted."""
    with tempfile.TemporaryDirectory() as d:
        tmp = Path(d)
        capture = _synth_capture(
            tmp,
            [
                ("Read", "/tmp/a.txt", "42 " + "z" * _MIN_RETRIEVED_TEXT_CHARS),
                ("Read", "/tmp/b.txt", "7 " + "z" * _MIN_RETRIEVED_TEXT_CHARS),
            ],
        )
        result = verify(_labelform_analysis(), capture, _FIXTURE_SUBAGENT_TYPE, "synthetic")
        assert result.provenance_labels == 1, (
            f"expected 1 read-at-source label, got {result.provenance_labels}"
        )


def _control_prov01_labelform_negative() -> None:
    """PROV-01 negative: the bare 'read-at-source' substring inside the
    *unverified* GT's own location clause is never counted.
    """
    with tempfile.TemporaryDirectory() as d:
        tmp = Path(d)
        capture = _synth_capture(
            tmp,
            [
                ("Read", "/tmp/a.txt", "42 " + "z" * _MIN_RETRIEVED_TEXT_CHARS),
                ("Read", "/tmp/b.txt", "7 " + "z" * _MIN_RETRIEVED_TEXT_CHARS),
            ],
        )
        result = verify(_labelform_analysis(), capture, _FIXTURE_SUBAGENT_TYPE, "synthetic")
        assert result.provenance_labels == 1, (
            f"the bare substring in GT-2's location clause must never be "
            f"counted, got provenance_labels={result.provenance_labels}"
        )


def _control_prov02_bind_positive() -> None:
    """PROV-02 positive: the WebFetch arm, mirroring the Read-arm pair --
    source cited and fetched.
    """
    with tempfile.TemporaryDirectory() as d:
        tmp = Path(d)
        capture = _synth_capture(
            tmp,
            [("WebFetch", "https://example.com/pricing", "42 " + "z" * _MIN_RETRIEVED_TEXT_CHARS)],
        )
        analysis = _synth_analysis(
            [_gt_line("GT-1", "a fact citing 42", "example.com/pricing")]
        )
        result = verify(analysis, capture, _FIXTURE_SUBAGENT_TYPE, "synthetic")
        assert result.unmatched_sources == 0, (
            f"expected the WebFetch arm to bind, got {result.unmatched_sources} unmatched"
        )


def _control_prov02_unmatched_negative() -> None:
    """PROV-02 negative: the WebFetch arm, source cited and never fetched."""
    with tempfile.TemporaryDirectory() as d:
        tmp = Path(d)
        capture = _synth_capture(tmp, [])
        analysis = _synth_analysis(
            [_gt_line("GT-1", "a fact citing 42", "example.com/pricing")]
        )
        result = verify(analysis, capture, _FIXTURE_SUBAGENT_TYPE, "synthetic")
        assert result.unmatched_sources == 1, (
            f"expected 1 unmatched source, got {result.unmatched_sources}"
        )
        assert result.provenance_flag == 1, (
            f"expected provenance_flag=1, got {result.provenance_flag}"
        )


def _control_prov02_ambiguous_positive() -> None:
    """WR-02 positive: two DIFFERENT fetched targets both anchor-match the
    same join key (same host+path, different query string -- so the two
    triples are genuinely distinct capture entries, not a retry) -- a
    genuine ambiguous join, must stay unmatched even after the CR-02 fix for
    duplicate fetches.
    """
    with tempfile.TemporaryDirectory() as d:
        tmp = Path(d)
        capture = _synth_capture(
            tmp,
            [
                ("WebFetch", "https://example.com/pricing", "42 " + "z" * _MIN_RETRIEVED_TEXT_CHARS),
                ("WebFetch", "https://example.com/pricing?ref=other", "42 " + "z" * _MIN_RETRIEVED_TEXT_CHARS),
            ],
        )
        analysis = _synth_analysis(
            [_gt_line("GT-1", "a fact citing 42", "example.com/pricing")]
        )
        result = verify(analysis, capture, _FIXTURE_SUBAGENT_TYPE, "synthetic")
        assert result.unmatched_sources == 1, (
            f"two distinct-target matches must stay ambiguous/unmatched, "
            f"got {result.unmatched_sources}"
        )
        assert result._unmatched_gt_ids == ("GT-1",), (
            f"expected GT-1 named as unmatched, got {result._unmatched_gt_ids!r}"
        )


def _control_prov02_ambiguous_negative() -> None:
    """WR-02 negative / CR-02 regression guard: the SAME target fetched
    twice (a WebFetch retry) must bind cleanly -- not reported as
    unmatched_sources -- and BOTH occurrences must be marked bound (not left
    as an orphan fetch), pinning the 'mark all matching indices bound' half
    of the CR-02 fix.
    """
    with tempfile.TemporaryDirectory() as d:
        tmp = Path(d)
        capture = _synth_capture(
            tmp,
            [
                ("WebFetch", "https://example.com/pricing", "the price is 42 dollars " + "z" * _MIN_RETRIEVED_TEXT_CHARS),
                ("WebFetch", "https://example.com/pricing", "the price is 42 dollars " + "z" * _MIN_RETRIEVED_TEXT_CHARS),
            ],
        )
        analysis = _synth_analysis(
            [_gt_line("GT-1", "a fact citing 42", "example.com/pricing")]
        )
        result = verify(analysis, capture, _FIXTURE_SUBAGENT_TYPE, "synthetic")
        assert result.unmatched_sources == 0, (
            f"a duplicate fetch of the same target must bind cleanly, "
            f"got {result.unmatched_sources} unmatched"
        )
        assert result.provenance_flag == 0, (
            f"expected provenance_flag=0 for a correctly-bound retried fetch, "
            f"got {result.provenance_flag}"
        )
        assert result.orphan_fetches == 0, (
            f"both occurrences of the retried fetch must be marked bound, "
            f"not left as an orphan, got {result.orphan_fetches}"
        )


def _control_prov02_anchor_negative() -> None:
    """CR-01 regression guard: an unrelated URL that merely contains the
    cited join key as a raw substring (not anchored on a host/path
    boundary) must NOT bind. Mirrors the review's exact repro: 'example.com'
    must not bind to '...ref=example.com-mirror', even though the digit
    literal happens to also appear in the unrelated page's retrieved text.
    """
    with tempfile.TemporaryDirectory() as d:
        tmp = Path(d)
        capture = _synth_capture(
            tmp,
            [
                (
                    "WebFetch",
                    "https://spam-aggregator.test/links?ref=example.com-mirror",
                    "the number 42 shows up here too " + "z" * _MIN_RETRIEVED_TEXT_CHARS,
                ),
            ],
        )
        analysis = _synth_analysis(
            [_gt_line("GT-1", "a fact citing 42", "example.com")]
        )
        result = verify(analysis, capture, _FIXTURE_SUBAGENT_TYPE, "synthetic")
        assert result.unmatched_sources == 1, (
            f"a substring collision must not bind; expected 1 unmatched "
            f"source, got {result.unmatched_sources}"
        )
        assert result.provenance_flag == 1, (
            f"expected provenance_flag=1 (the CR-01 false PASS must not "
            f"recur), got {result.provenance_flag}"
        )


def _control_prov03_located_positive() -> None:
    """PROV-03 positive: the GT's one literal is present in the bound
    source's retrieved text.
    """
    with tempfile.TemporaryDirectory() as d:
        tmp = Path(d)
        capture = _synth_capture(
            tmp,
            [("Read", "/tmp/a.txt", "the price is 42 dollars " + "z" * _MIN_RETRIEVED_TEXT_CHARS)],
        )
        analysis = _synth_analysis(
            [_gt_line("GT-1", "a fact citing 42", "`/tmp/a.txt`")]
        )
        result = verify(analysis, capture, _FIXTURE_SUBAGENT_TYPE, "synthetic")
        assert result.unlocated_literals == 0, (
            f"expected 0 unlocated literals, got {result.unlocated_literals}"
        )
        assert result.misattributed_literals == 0, (
            f"expected 0 misattributed literals, got {result.misattributed_literals}"
        )


def _control_prov03_unlocated_negative() -> None:
    """PROV-03 negative: the GT's literal is absent from the bound source's
    retrieved text. Must also assert misattributed_literals == 0, proving
    the two families are not conflated.
    """
    with tempfile.TemporaryDirectory() as d:
        tmp = Path(d)
        capture = _synth_capture(
            tmp,
            [("Read", "/tmp/a.txt", "no matching number here " + "z" * _MIN_RETRIEVED_TEXT_CHARS)],
        )
        analysis = _synth_analysis(
            [_gt_line("GT-1", "a fact citing 42", "`/tmp/a.txt`")]
        )
        result = verify(analysis, capture, _FIXTURE_SUBAGENT_TYPE, "synthetic")
        assert result.unlocated_literals == 1, (
            f"expected 1 unlocated literal, got {result.unlocated_literals}"
        )
        assert result.misattributed_literals == 0, (
            f"expected 0 misattributed literals (families must not conflate), "
            f"got {result.misattributed_literals}"
        )


def _control_d04_misattributed_positive() -> None:
    """D-04 positive: a two-source capture where the GT's literal is absent
    from its BOUND source but present in the OTHER fetched source --
    misattribution, not fabrication.
    """
    with tempfile.TemporaryDirectory() as d:
        tmp = Path(d)
        capture = _synth_capture(
            tmp,
            [
                ("Read", "/tmp/a.txt", "no matching number here " + "z" * _MIN_RETRIEVED_TEXT_CHARS),
                ("Read", "/tmp/b.txt", "the price is 42 dollars " + "z" * _MIN_RETRIEVED_TEXT_CHARS),
            ],
        )
        analysis = _synth_analysis(
            [_gt_line("GT-1", "a fact citing 42", "`/tmp/a.txt`")]
        )
        result = verify(analysis, capture, _FIXTURE_SUBAGENT_TYPE, "synthetic")
        assert result.misattributed_literals == 1, (
            f"expected 1 misattributed literal, got {result.misattributed_literals}"
        )
        assert result.unlocated_literals == 0, (
            f"expected 0 unlocated literals (families must not conflate), "
            f"got {result.unlocated_literals}"
        )


def _control_d04_misattributed_negative() -> None:
    """D-04 negative: the same literal absent from BOTH fetched sources --
    fabrication, not misattribution.
    """
    with tempfile.TemporaryDirectory() as d:
        tmp = Path(d)
        capture = _synth_capture(
            tmp,
            [
                ("Read", "/tmp/a.txt", "no matching number here " + "z" * _MIN_RETRIEVED_TEXT_CHARS),
                ("Read", "/tmp/b.txt", "still nothing here " + "z" * _MIN_RETRIEVED_TEXT_CHARS),
            ],
        )
        analysis = _synth_analysis(
            [_gt_line("GT-1", "a fact citing 42", "`/tmp/a.txt`")]
        )
        result = verify(analysis, capture, _FIXTURE_SUBAGENT_TYPE, "synthetic")
        assert result.unlocated_literals == 1, (
            f"expected 1 unlocated literal, got {result.unlocated_literals}"
        )
        assert result.misattributed_literals == 0, (
            f"expected 0 misattributed literals, got {result.misattributed_literals}"
        )


def _control_d03_zeroliteral_positive() -> None:
    """D-03 positive: a read-at-source GT whose claim body contains no
    numeric token at all -- reported, never failing.
    """
    with tempfile.TemporaryDirectory() as d:
        tmp = Path(d)
        capture = _synth_capture(
            tmp,
            [("Read", "/tmp/a.txt", "no digits in this retrieved text at all " + "z" * _MIN_RETRIEVED_TEXT_CHARS)],
        )
        analysis = _synth_analysis(
            [_gt_line("GT-1", "a claim with no numeric token", "`/tmp/a.txt`")]
        )
        result = verify(analysis, capture, _FIXTURE_SUBAGENT_TYPE, "synthetic")
        assert result.zero_literal_gts == 1, (
            f"expected 1 zero-literal GT, got {result.zero_literal_gts}"
        )
        assert result.literals_checked == 0, (
            f"expected 0 literals checked, got {result.literals_checked}"
        )
        assert result.provenance_flag == 0, (
            f"zero-literal GTs must never gate the run, got provenance_flag={result.provenance_flag}"
        )


def _control_d03_zeroliteral_negative() -> None:
    """D-03 negative: the same GT shape but with one literal present."""
    with tempfile.TemporaryDirectory() as d:
        tmp = Path(d)
        capture = _synth_capture(
            tmp,
            [("Read", "/tmp/a.txt", "the price is 42 dollars " + "z" * _MIN_RETRIEVED_TEXT_CHARS)],
        )
        analysis = _synth_analysis(
            [_gt_line("GT-1", "a claim citing 42", "`/tmp/a.txt`")]
        )
        result = verify(analysis, capture, _FIXTURE_SUBAGENT_TYPE, "synthetic")
        assert result.zero_literal_gts == 0, (
            f"expected 0 zero-literal GTs, got {result.zero_literal_gts}"
        )


def _control_d06_orphan_positive() -> None:
    """D-06 positive: a capture with one fetched source cited by no GT --
    reported, never failing (the fixture's own 2 reference-file Reads are the
    normal case).
    """
    with tempfile.TemporaryDirectory() as d:
        tmp = Path(d)
        capture = _synth_capture(
            tmp,
            [
                ("Read", "/tmp/a.txt", "the price is 42 dollars " + "z" * _MIN_RETRIEVED_TEXT_CHARS),
                ("Read", "/tmp/uncited.txt", "cited by nothing " + "z" * _MIN_RETRIEVED_TEXT_CHARS),
            ],
        )
        analysis = _synth_analysis(
            [_gt_line("GT-1", "a claim citing 42", "`/tmp/a.txt`")]
        )
        result = verify(analysis, capture, _FIXTURE_SUBAGENT_TYPE, "synthetic")
        assert result.orphan_fetches == 1, (
            f"expected 1 orphan fetch, got {result.orphan_fetches}"
        )
        assert result.provenance_flag == 0, (
            f"orphan fetches must never gate the run, got provenance_flag={result.provenance_flag}"
        )


def _control_d06_orphan_negative() -> None:
    """D-06 negative: every fetched source is cited by a GT."""
    with tempfile.TemporaryDirectory() as d:
        tmp = Path(d)
        capture = _synth_capture(
            tmp,
            [("Read", "/tmp/a.txt", "the price is 42 dollars " + "z" * _MIN_RETRIEVED_TEXT_CHARS)],
        )
        analysis = _synth_analysis(
            [_gt_line("GT-1", "a claim citing 42", "`/tmp/a.txt`")]
        )
        result = verify(analysis, capture, _FIXTURE_SUBAGENT_TYPE, "synthetic")
        assert result.orphan_fetches == 0, (
            f"expected 0 orphan fetches, got {result.orphan_fetches}"
        )


def _control_prov05_record_roundtrip() -> None:
    """PROV-05: build the record via provenance_defect_record, write
    record_to_tsv's output into the tempdir, read it back with
    read_defect_incidence, and assert the flag sums and row shape survive
    the round-trip.
    """
    with tempfile.TemporaryDirectory() as d:
        tmp = Path(d)
        capture = _synth_capture(
            tmp,
            [("WebFetch", "https://example.com/pricing", "42 " + "z" * _MIN_RETRIEVED_TEXT_CHARS)],
        )
        analysis = _synth_analysis(
            [_gt_line("GT-1", "a fact citing 42", "example.com/pricing")]
        )
        result = verify(analysis, capture, _FIXTURE_SUBAGENT_TYPE, "synthetic")
        record = provenance_defect_record(analysis, "synthetic", result)
        tsv_text = record_to_tsv(record)
        tsv_path = tmp / "roundtrip.tsv"
        tsv_path.write_text(tsv_text, encoding="utf-8")

        read_back = read_defect_incidence(tsv_path)
        assert read_back["n"] == 1, f"expected n=1, got {read_back['n']}"
        assert read_back["untraced"] == record["untraced_flag"], (
            f"untraced sum diverged from detect_defects: "
            f"{read_back['untraced']} vs {record['untraced_flag']}"
        )
        assert read_back["verdict"] == record["verdict_flag"], (
            f"verdict sum diverged from detect_defects: "
            f"{read_back['verdict']} vs {record['verdict_flag']}"
        )
        assert read_back["chain"] == record["chain_flag"], (
            f"chain sum diverged from detect_defects: "
            f"{read_back['chain']} vs {record['chain_flag']}"
        )

        row_cells = tsv_text.splitlines()[1].split("\t")
        assert len(row_cells) == len(_DEFECT_RECORD_FIELDS), (
            f"expected {len(_DEFECT_RECORD_FIELDS)} cells, got {len(row_cells)}"
        )
        for field in (
            "provenance_labels",
            "unmatched_sources",
            "unreadable_sources",
            "literals_checked",
            "unlocated_literals",
            "misattributed_literals",
            "zero_literal_gts",
            "orphan_fetches",
            "provenance_flag",
        ):
            assert isinstance(record[field], int), (
                f"{field} is {type(record[field]).__name__}, not int -- "
                f"the 'n/a' sentinel was not overwritten"
            )


def _control_prov04_network_blocked() -> None:
    """D-14: patch both `socket.socket` and `socket.create_connection` to
    raise, then run the FULL committed-fixture verification under the patch
    -- the real path never touches the network. New ground for this repo: no
    existing gate monkeypatches a stdlib network call.
    """
    with (
        mock.patch("socket.socket", side_effect=OSError("network disabled by control")),
        mock.patch(
            "socket.create_connection",
            side_effect=OSError("network disabled by control"),
        ),
    ):
        analysis_text = _FIXTURE_ANALYSIS.read_text(encoding="utf-8")
        result = verify(analysis_text, _FIXTURE_CAPTURE, _FIXTURE_SUBAGENT_TYPE, "PR-P1")
        assert result.provenance_labels == _EXPECTED_SOURCES, (
            f"expected {_EXPECTED_SOURCES} sources, got {result.provenance_labels}"
        )
        assert result.literals_checked == _EXPECTED_LITERALS, (
            f"expected {_EXPECTED_LITERALS} literals, got {result.literals_checked}"
        )
        assert not (
            result.unmatched_sources
            or result.unreadable_sources
            or result.unlocated_literals
            or result.misattributed_literals
        ), f"expected zero failing families under the network block, got {result!r}"

    # Restore proof: after the `with` block exits, socket.create_connection
    # must be the real stdlib callable again (the mock context manager's own
    # restore discipline).
    assert socket.create_connection.__module__ == "socket", (
        "socket.create_connection was not restored after the patch context exited"
    )


def _control_prov04_network_armed_proof() -> None:
    """D-14 armed-proof: a deliberate connect attempt under the same patch
    must raise, or PROV04-network-blocked is a control that proves nothing.
    """
    with (
        mock.patch("socket.socket", side_effect=OSError("network disabled by control")),
        mock.patch(
            "socket.create_connection",
            side_effect=OSError("network disabled by control"),
        ),
    ):
        try:
            socket.create_connection(("example.com", 80), timeout=1)
        except OSError:
            pass
        else:
            raise AssertionError(
                "armed-proof: create_connection was NOT blocked -- the patch is inert"
            )


def _control_gate01_antimask_selfproof() -> None:
    """D-16: prove the anti-masking assertion itself is not inert. Compute the
    diff against a deliberately shrunk copy of `_covered_controls` (one id
    removed) and assert the diff is non-empty and names that id.
    """
    shrunk = set(_covered_controls)
    assert shrunk, "cannot self-proof against an empty covered_controls set"
    removed = sorted(shrunk)[0]
    shrunk.discard(removed)
    diff = REQUIRED_CONTROLS - shrunk
    assert diff, "anti-masking diff was empty against a deliberately shrunk set"
    assert removed in diff, (
        f"expected {removed!r} to be named in the diff, got {sorted(diff)!r}"
    )


# D-16 inventory: every self-test control id, mapped to the decision it traces
# to. Deliberately in-code with NO sidecar `.md` -- the HARN-01 pattern is not
# adopted here because these controls are self-describing.
#
#   PROV02-readarm-positive      D-07  synthesized Read-arm, positive
#   PROV02-readarm-negative      D-07  synthesized Read-arm, negative
#   D08-unreadable-positive      D-08  unreadable-source floor, positive
#   D08-unreadable-negative      D-08  unreadable-source floor, negative
#   PROV02-dispatch-raises       constraint 5  never-dispatched ValueError propagates
#   PROV01-labelform-positive    PROV-01  label-form match, positive
#   PROV01-labelform-negative    PROV-01  bare substring rejected, negative
#   PROV02-bind-positive         PROV-02  WebFetch-arm bind, positive
#   PROV02-unmatched-negative    PROV-02  WebFetch-arm bind, negative
#   PROV02-ambiguous-positive    WR-02  two distinct targets both match key -> unmatched
#   PROV02-ambiguous-negative    WR-02/CR-02  duplicate fetch of same target -> binds cleanly
#   PROV02-anchor-negative       CR-01  substring collision (no boundary) must not bind
#   PROV03-located-positive      PROV-03  literal location, positive
#   PROV03-unlocated-negative    PROV-03  literal location, negative
#   D04-misattributed-positive   D-04  attribution error, positive
#   D04-misattributed-negative   D-04  fabrication (absent everywhere), negative
#   D03-zeroliteral-positive     D-03  zero-literal GT, positive (reported, not failing)
#   D03-zeroliteral-negative     D-03  zero-literal GT, negative
#   D06-orphan-positive          D-06  orphan fetch, positive (reported, not failing)
#   D06-orphan-negative          D-06  orphan fetch, negative
#   PROV05-record-roundtrip      PROV-05  22-column TSV round-trip
#   PROV04-network-blocked       D-14  full fixture verification under a socket block
#   PROV04-network-armed-proof   D-14  the block is armed, not silently inert
#   GATE01-antimask-selfproof    D-16  the anti-masking assertion is not itself inert
REQUIRED_CONTROLS: frozenset[str] = frozenset(
    {
        "PROV02-readarm-positive",
        "PROV02-readarm-negative",
        "D08-unreadable-positive",
        "D08-unreadable-negative",
        "PROV02-dispatch-raises",
        "PROV01-labelform-positive",
        "PROV01-labelform-negative",
        "PROV02-bind-positive",
        "PROV02-unmatched-negative",
        "PROV02-ambiguous-positive",
        "PROV02-ambiguous-negative",
        "PROV02-anchor-negative",
        "PROV03-located-positive",
        "PROV03-unlocated-negative",
        "D04-misattributed-positive",
        "D04-misattributed-negative",
        "D03-zeroliteral-positive",
        "D03-zeroliteral-negative",
        "D06-orphan-positive",
        "D06-orphan-negative",
        "PROV05-record-roundtrip",
        "PROV04-network-blocked",
        "PROV04-network-armed-proof",
        "GATE01-antimask-selfproof",
    }
)


def _run_self_test() -> None:
    """D-16 control battery: positive and negative controls for every named
    finding family, the synthesized Read-arm fixture (D-07), the PROV-04
    no-network proof, and the anti-masking coverage assertion.
    """
    _covered_controls.clear()
    _self_test_failures.clear()

    _run_control("PROV02-readarm-positive", _control_prov02_readarm_positive)
    _run_control("PROV02-readarm-negative", _control_prov02_readarm_negative)
    _run_control("D08-unreadable-positive", _control_d08_unreadable_positive)
    _run_control("D08-unreadable-negative", _control_d08_unreadable_negative)
    _run_control("PROV02-dispatch-raises", _control_prov02_dispatch_raises)
    _run_control("PROV01-labelform-positive", _control_prov01_labelform_positive)
    _run_control("PROV01-labelform-negative", _control_prov01_labelform_negative)
    _run_control("PROV02-bind-positive", _control_prov02_bind_positive)
    _run_control("PROV02-unmatched-negative", _control_prov02_unmatched_negative)
    _run_control("PROV02-ambiguous-positive", _control_prov02_ambiguous_positive)
    _run_control("PROV02-ambiguous-negative", _control_prov02_ambiguous_negative)
    _run_control("PROV02-anchor-negative", _control_prov02_anchor_negative)
    _run_control("PROV03-located-positive", _control_prov03_located_positive)
    _run_control("PROV03-unlocated-negative", _control_prov03_unlocated_negative)
    _run_control("D04-misattributed-positive", _control_d04_misattributed_positive)
    _run_control("D04-misattributed-negative", _control_d04_misattributed_negative)
    _run_control("D03-zeroliteral-positive", _control_d03_zeroliteral_positive)
    _run_control("D03-zeroliteral-negative", _control_d03_zeroliteral_negative)
    _run_control("D06-orphan-positive", _control_d06_orphan_positive)
    _run_control("D06-orphan-negative", _control_d06_orphan_negative)
    _run_control("PROV05-record-roundtrip", _control_prov05_record_roundtrip)
    _run_control("PROV04-network-blocked", _control_prov04_network_blocked)
    _run_control("PROV04-network-armed-proof", _control_prov04_network_armed_proof)
    _run_control("GATE01-antimask-selfproof", _control_gate01_antimask_selfproof)

    # D-16 anti-masking: the full named inventory must have run, and nothing
    # that ran may be absent from the inventory (a control cannot silently
    # drift behind the code in either direction).
    uncovered = REQUIRED_CONTROLS - _covered_controls
    unregistered = _covered_controls - REQUIRED_CONTROLS
    if uncovered:
        print(
            f"ANTI-MASKING GATE FAILURE: {len(uncovered)} control(s) not "
            f"covered: {sorted(uncovered)}"
        )
        _self_test_failures.append("ANTI-MASKING-uncovered")
    elif unregistered:
        print(
            f"ANTI-MASKING GATE FAILURE: {len(unregistered)} control(s) ran "
            f"but are not registered in REQUIRED_CONTROLS: {sorted(unregistered)}"
        )
        _self_test_failures.append("ANTI-MASKING-unregistered")
    else:
        print(f"ANTI-MASKING GATE: All {len(REQUIRED_CONTROLS)} controls covered ✓")

    if _self_test_failures:
        sys.stderr.write(
            f"check-provenance --self-test: {len(_self_test_failures)} "
            f"control(s) failed: {sorted(set(_self_test_failures))}\n"
        )
        sys.exit(1)

    print("check-provenance --self-test: PASS")


# ---------------------------------------------------------------------------
# Live leg (D-13: no --analysis / --capture flag -- targets the repo-anchored
# fixture constants only) with the D-15 anti-vacuity mutation.
# ---------------------------------------------------------------------------

# GT-1's own literal, mutated to a value absent from the retrieved text of every
# fetched source. D-15: modelled line-for-line on check-agent.py's
# _assert_live_coverage -- the live PASS is backed by an in-memory mutation of the
# bytes the run actually read, so a vacuous verifier (broken regex, empty parse,
# swallowed exception) cannot report green.
_MUTATE_FROM = "$0.0000166667"
_MUTATE_TO = "$0.0000199999"


def _validate_live_fixture() -> None:
    """PROV-GUARD's live leg: verify the committed fixture, then require the D-15
    in-memory mutation to surface as an unlocated finding naming GT-1 before PASS
    prints. Nothing is written to disk: `tests/quality-provenance-v8.24/` is
    frozen evidence, and FROZEN-EVIDENCE sweeps for untracked files too.
    """
    if not _FIXTURE_ANALYSIS.is_file():
        sys.stderr.write(f"check-provenance: fixture analysis not found: {_FIXTURE_ANALYSIS}\n")
        sys.exit(2)
    if not _FIXTURE_CAPTURE.is_file():
        sys.stderr.write(f"check-provenance: fixture capture not found: {_FIXTURE_CAPTURE}\n")
        sys.exit(2)

    analysis_text = _FIXTURE_ANALYSIS.read_text(encoding="utf-8")

    result = verify(analysis_text, _FIXTURE_CAPTURE, _FIXTURE_SUBAGENT_TYPE, "PR-P1")

    # Compare against the module constants, not merely reflected from whatever the
    # run computed, so a silent drop in extraction is caught (D-02).
    failures: list[str] = []
    if result.provenance_labels != _EXPECTED_SOURCES:
        failures.append(
            f"provenance_labels={result.provenance_labels}, expected {_EXPECTED_SOURCES}"
        )
    if result.literals_checked != _EXPECTED_LITERALS:
        failures.append(
            f"literals_checked={result.literals_checked}, expected {_EXPECTED_LITERALS}"
        )
    if result.unmatched_sources:
        failures.append(
            f"unmatched_sources={result.unmatched_sources} {result._unmatched_gt_ids}"
        )
    if result.unreadable_sources:
        failures.append(
            f"unreadable_sources={result.unreadable_sources} {result._unreadable_gt_ids}"
        )
    if result.unlocated_literals:
        failures.append(
            f"unlocated_literals={result.unlocated_literals} {result._unlocated_pairs}"
        )
    if result.misattributed_literals:
        failures.append(
            f"misattributed_literals={result.misattributed_literals} {result._misattributed_pairs}"
        )

    if failures:
        sys.stderr.write("check-provenance: FAIL — " + "; ".join(failures) + "\n")
        sys.exit(1)

    # COVERAGE: a clean PASS cannot be taken on trust -- mutate the bytes this run
    # actually read (one numeric literal, GT-1's) and require the checker to
    # report that specific defect before printing PASS.
    mutated_text, count = re.subn(re.escape(_MUTATE_FROM), _MUTATE_TO, analysis_text, count=1)
    if count != 1:
        sys.stderr.write(
            f"check-provenance: COVERAGE FAIL — could not locate the literal to "
            f"mutate ({_MUTATE_FROM!r}); the anti-vacuity control cannot run\n"
        )
        sys.exit(1)

    mutated_result = verify(mutated_text, _FIXTURE_CAPTURE, _FIXTURE_SUBAGENT_TYPE, "PR-P1")
    if not any(gt_id == "GT-1" for gt_id, _lit in mutated_result._unlocated_pairs):
        sys.stderr.write(
            "check-provenance: COVERAGE FAIL — the mutated literal did NOT produce "
            "the expected unlocated finding; this gate is passing vacuously and is "
            "NOT verifying this fixture\n"
        )
        sys.exit(1)

    sources_matched = result.provenance_labels - result.unmatched_sources
    literals_located = result.literals_checked - result.unlocated_literals - result.misattributed_literals
    print(
        f"check-provenance: COVERAGE — verified {_FIXTURE_ANALYSIS} against "
        f"{_FIXTURE_CAPTURE} ({sources_matched}/{result.provenance_labels} sources "
        f"matched, {literals_located}/{result.literals_checked} literals located)"
    )
    print(
        f"check-provenance: {result.zero_literal_gts} zero-literal GT(s), "
        f"{result.orphan_fetches} orphan fetch(es), provenance_flag={result.provenance_flag}"
    )
    print("check-provenance: PASS")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="PROV-GUARD: verify read-at-source provenance against a stored capture."
    )
    parser.add_argument(
        "--self-test",
        action="store_true",
        help="run the offline control battery (positive, negative, anti-masking)",
    )
    args = parser.parse_args()

    _require_python_version()

    if args.self_test:
        _run_self_test()
        return

    _validate_live_fixture()


if __name__ == "__main__":
    main()
