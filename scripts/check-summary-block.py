#!/usr/bin/env python3
# /// script
# requires-python = ">=3.12"
# dependencies = []
# ///
"""Checker and self-test for the structured-summary process-output block.

Finds the report's one fenced JSON summary block, checks its placement,
parses it, and validates it against the shipped schema file with a
hand-written stdlib validator -- no schema-validation package dependency
anywhere in this repo's tooling. Every structural defect is reported under
its own finding code. This plan implements block detection, placement, JSON
parsing, schema validation and the two block-only internal invariants;
cross-checks against the report's own prose are a later plan's addition,
registered through the cross-check roster below.

Usage:
    python3 scripts/check-summary-block.py [--exemplar] [--json] [--schema PATH] REPORT [REPORT ...]
    python3 scripts/check-summary-block.py --self-test
    python3 scripts/check-summary-block.py --describe
"""
from __future__ import annotations

import argparse
import copy
import functools
import json
import re
import sys
import tempfile
from collections.abc import Callable
from pathlib import Path
from typing import NamedTuple

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_SCHEMA = REPO_ROOT / "shared" / "spine" / "references" / "summary-schema.json"
APPENDIX_HEADING = "## Appendix — process output"

# Closed set of finding codes. Plan 01 emits the first eight; Plan 02 emits
# the remaining fifteen (cross-checks against the report's own prose).
FINDING_CODES: tuple[str, ...] = (
    "SB-MISSING",
    "SB-MULTIPLE",
    "SB-JSON",
    "SB-PLACEMENT",
    "SB-SCHEMA",
    "SB-NULL",
    "SB-INVARIANT",
    "SB-GATE-CLEARED",
    "SB-ASSUMPTION",
    "SB-GROUND-TRUTH",
    "SB-CHAIN-ID",
    "SB-CHAIN-CONFIDENCE",
    "SB-CHAIN-RESTS-ON",
    "SB-DEAD-END",
    "SB-TECHNIQUES",
    "SB-RUN-MODE",
    "SB-GATE-RESULT",
    "SB-GATE-PASSES",
    "SB-GATE-BANDS",
    "SB-REENTRY",
    "SB-CONCLUSION-CUT",
    "SB-CONCLUSION-TEXT",
    "SB-CONCLUSION-CONFIDENCE",
)


class Finding(NamedTuple):
    code: str
    message: str


class SchemaError(Exception):
    """The schema file is malformed or uses a validator keyword this checker
    does not implement. Never raised for a malformed REPORT."""


# ---------------------------------------------------------------------------
# Schema loading and the stdlib field-table validator
# ---------------------------------------------------------------------------

_DOC_KEYS = frozenset({"source", "null_when", "$comment"})
_KNOWN_FIELD_KEYS = frozenset({
    "type", "nullable", "const", "enum", "pattern", "items", "fields",
    "length", "minimum", "maximum",
}) | _DOC_KEYS

_TYPE_MAP: dict[str, type] = {
    "integer": int,
    "string": str,
    "boolean": bool,
    "array": list,
    "object": dict,
}


def _validate_schema_keys(spec, path: str) -> None:
    """Raise SchemaError if `spec` (or anything nested under it) uses a
    field-spec keyword this validator does not implement. This is the guard
    that keeps a future schema feature from being silently ignored."""
    if not isinstance(spec, dict):
        raise SchemaError(f"{path}: field spec must be a JSON object")
    unknown = set(spec) - _KNOWN_FIELD_KEYS
    if unknown:
        raise SchemaError(f"{path}: unknown schema keyword(s) {sorted(unknown)!r}")
    if "items" in spec:
        _validate_schema_keys(spec["items"], f"{path}[]")
    if "fields" in spec:
        fields = spec["fields"]
        if not isinstance(fields, dict):
            raise SchemaError(f"{path}.fields must be a JSON object")
        for key, sub in fields.items():
            _validate_schema_keys(sub, f"{path}.{key}")


def load_schema(path: Path) -> dict:
    """Load and structurally validate a summary-schema.json file.

    Raises SchemaError for anything wrong with the SCHEMA -- unreadable, not
    JSON, not an object, or carrying a field-spec keyword this validator does
    not implement. Never raised for a report.
    """
    try:
        raw = path.read_text()
    except OSError as exc:
        raise SchemaError(f"cannot read schema file {path}: {exc}") from exc
    try:
        schema = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise SchemaError(f"schema file {path} is not valid JSON: {exc}") from exc
    if not isinstance(schema, dict):
        raise SchemaError(f"schema file {path}: top level must be a JSON object")
    fields = schema.get("fields", {})
    if not isinstance(fields, dict):
        raise SchemaError(f"schema file {path}: 'fields' must be a JSON object")
    for key, spec in fields.items():
        _validate_schema_keys(spec, key)
    return schema


# Block heading/fence are read once from the shipped schema, never retyped.
_SCHEMA_FOR_CONSTANTS = load_schema(DEFAULT_SCHEMA)
BLOCK_HEADING: str = _SCHEMA_FOR_CONSTANTS["block"]["heading"]
BLOCK_FENCE: str = _SCHEMA_FOR_CONSTANTS["block"]["fence"]


# ---------------------------------------------------------------------------
# Fence scan and block detection
# ---------------------------------------------------------------------------

_FENCE_OPEN_RE = re.compile(r"^ {0,3}(?P<ticks>`{3,})(?P<info>.*)$")
_FENCE_CLOSE_RE = re.compile(r"^ {0,3}(?P<ticks>`{3,})\s*$")


class _Block(NamedTuple):
    start: int
    end: int
    info: str
    body: str
    under_heading: bool


def _fence_state(lines: list[str]) -> tuple[list[bool], list[tuple[int, int, str, str]]]:
    """Per line: is it inside a fenced code block? Also return every fence
    found as (start_line, end_line, info_string, body_text). An opening fence
    of three or more backticks closes on a line of at least the same number
    of backticks and nothing else; an unterminated fence runs to end of
    input."""
    inside = [False] * len(lines)
    fences: list[tuple[int, int, str, str]] = []
    n = len(lines)
    i = 0
    open_len: int | None = None
    start: int | None = None
    while i < n:
        line = lines[i]
        if open_len is None:
            m = _FENCE_OPEN_RE.match(line)
            if m:
                open_len = len(m.group("ticks"))
                start = i
                inside[i] = True
            i += 1
            continue
        inside[i] = True
        cm = _FENCE_CLOSE_RE.match(line)
        if cm and len(cm.group("ticks")) >= open_len:
            info = _FENCE_OPEN_RE.match(lines[start]).group("info").strip()
            body = "\n".join(lines[start + 1 : i])
            fences.append((start, i, info, body))
            open_len = None
            start = None
        i += 1
    if open_len is not None:
        info = _FENCE_OPEN_RE.match(lines[start]).group("info").strip()
        body = "\n".join(lines[start + 1 : n])
        fences.append((start, n - 1, info, body))
    return inside, fences


def find_blocks(text: str) -> list[_Block]:
    """A summary block is any fenced code block whose opening fence info
    string is BLOCK_FENCE ("json") AND that is either under BLOCK_HEADING or
    whose body contains the key "schema_version". Headings inside any fence
    are ignored."""
    lines = text.split("\n")
    inside, fences = _fence_state(lines)
    heading_idx: int | None = None
    for i, line in enumerate(lines):
        if inside[i]:
            continue
        if line.strip() == BLOCK_HEADING:
            heading_idx = i
            break
    blocks: list[_Block] = []
    for start, end, info, body in fences:
        if info != BLOCK_FENCE:
            continue
        under = heading_idx is not None and start > heading_idx
        if under or '"schema_version"' in body:
            blocks.append(_Block(start=start, end=end, info=info, body=body, under_heading=under))
    return blocks


def _placement_findings(text: str, block: _Block) -> list[Finding]:
    """SB-PLACEMENT: heading absent, repeated, not after APPENDIX_HEADING,
    the block not under it, or anything other than whitespace following the
    block's closing fence."""
    lines = text.split("\n")
    inside, _fences = _fence_state(lines)
    heading_idxs = [i for i, l in enumerate(lines) if not inside[i] and l.strip() == BLOCK_HEADING]
    appendix_idxs = [i for i, l in enumerate(lines) if not inside[i] and l.strip() == APPENDIX_HEADING]
    findings: list[Finding] = []
    if not heading_idxs:
        findings.append(Finding("SB-PLACEMENT", f"{BLOCK_HEADING!r} heading not found"))
        return findings
    if len(heading_idxs) > 1:
        findings.append(Finding(
            "SB-PLACEMENT", f"{BLOCK_HEADING!r} heading appears {len(heading_idxs)} times"))
    heading_idx = heading_idxs[0]
    if not any(a < heading_idx for a in appendix_idxs):
        findings.append(Finding(
            "SB-PLACEMENT", f"{BLOCK_HEADING!r} heading is not after {APPENDIX_HEADING!r}"))
    if block.start <= heading_idx:
        findings.append(Finding("SB-PLACEMENT", "the summary block is not under its heading"))
    trailing = lines[block.end + 1 :]
    if any(l.strip() for l in trailing):
        findings.append(Finding(
            "SB-PLACEMENT", "non-whitespace content follows the block's closing fence"))
    return findings


# ---------------------------------------------------------------------------
# Schema-driven value validator
# ---------------------------------------------------------------------------

def _type_ok(value, type_name: str) -> bool:
    if type_name == "integer":
        return isinstance(value, int) and not isinstance(value, bool)
    if type_name == "boolean":
        return isinstance(value, bool)
    py_type = _TYPE_MAP.get(type_name)
    if py_type is None:
        raise SchemaError(f"unknown type {type_name!r}")
    return isinstance(value, py_type)


def validate(value, spec: dict, path: str, *, exemplar: bool) -> list[Finding]:
    """Recursively validate `value` against a field spec. Never raises on a
    malformed value; a schema problem (unknown type name) still raises."""
    findings: list[Finding] = []
    nullable = bool(spec.get("nullable", False))
    if value is None:
        if not nullable:
            findings.append(Finding("SB-SCHEMA", f"{path}: null is not allowed"))
        elif not exemplar:
            findings.append(Finding("SB-NULL", f"{path}: is null"))
        return findings
    t = spec.get("type")
    if t is not None and not _type_ok(value, t):
        findings.append(Finding(
            "SB-SCHEMA", f"{path}: expected type {t}, got {type(value).__name__}"))
        return findings
    if "const" in spec and value != spec["const"]:
        findings.append(Finding(
            "SB-SCHEMA", f"{path}: expected {spec['const']!r}, got {value!r}"))
    if "enum" in spec and value not in spec["enum"]:
        findings.append(Finding(
            "SB-SCHEMA", f"{path}: {value!r} is not one of {spec['enum']}"))
    if "pattern" in spec and isinstance(value, str):
        if re.fullmatch(spec["pattern"], value) is None:
            findings.append(Finding(
                "SB-SCHEMA", f"{path}: {value!r} does not match pattern {spec['pattern']!r}"))
    if "length" in spec and hasattr(value, "__len__") and len(value) != spec["length"]:
        findings.append(Finding(
            "SB-SCHEMA", f"{path}: expected length {spec['length']}, got {len(value)}"))
    if "minimum" in spec and isinstance(value, (int, float)) and not isinstance(value, bool):
        if value < spec["minimum"]:
            findings.append(Finding(
                "SB-SCHEMA", f"{path}: {value} is below minimum {spec['minimum']}"))
    if "maximum" in spec and isinstance(value, (int, float)) and not isinstance(value, bool):
        if value > spec["maximum"]:
            findings.append(Finding(
                "SB-SCHEMA", f"{path}: {value} is above maximum {spec['maximum']}"))
    if t == "array" and "items" in spec and isinstance(value, list):
        item_spec = spec["items"]
        for idx, item in enumerate(value):
            findings.extend(validate(item, item_spec, f"{path}[{idx}]", exemplar=exemplar))
    if t == "object" and "fields" in spec and isinstance(value, dict):
        subfields = spec["fields"]
        for key in value:
            if key not in subfields:
                findings.append(Finding("SB-SCHEMA", f"{path}.{key}: unknown key"))
        for key, subspec in subfields.items():
            if key not in value:
                findings.append(Finding("SB-SCHEMA", f"{path}.{key}: missing required key"))
                continue
            findings.extend(validate(value[key], subspec, f"{path}.{key}", exemplar=exemplar))
    return findings


def validate_report(value: dict, schema: dict, *, exemplar: bool) -> list[Finding]:
    """Top-level validation: required keys, unknown keys, then each known
    field recursively."""
    findings: list[Finding] = []
    required = schema.get("required", [])
    fields = schema.get("fields", {})
    for key in required:
        if key not in value:
            findings.append(Finding("SB-SCHEMA", f"{key}: missing required key"))
    for key in value:
        if key not in fields:
            findings.append(Finding("SB-SCHEMA", f"{key}: unknown key"))
    for key, spec in fields.items():
        if key in value:
            findings.extend(validate(value[key], spec, key, exemplar=exemplar))
    return findings


# ---------------------------------------------------------------------------
# Internal (block-only) invariants: INV-04, INV-05, INV-09
# ---------------------------------------------------------------------------

def _gate_invariant_findings(gate) -> list[Finding]:
    """INV-04: each pass's gate_cleared/hand_wavy_cap_cleared agree with its
    own bands (SB-INVARIANT). INV-05: gate.cleared follows the LAST pass's
    gate_cleared/hand_wavy_cap_cleared (SB-GATE-CLEARED)."""
    findings: list[Finding] = []
    if not isinstance(gate, dict):
        return findings
    passes = gate.get("passes")
    if not isinstance(passes, list):
        return findings
    for idx, p in enumerate(passes):
        if not isinstance(p, dict):
            continue
        bands = p.get("bands")
        if not isinstance(bands, list) or len(bands) != 6 or not all(isinstance(b, str) for b in bands):
            continue
        actual_cleared = "Absent" not in bands
        actual_cap = bands.count("Hand-wavy") <= 1
        if p.get("gate_cleared") is not actual_cleared:
            findings.append(Finding(
                "SB-INVARIANT", f"gate.passes[{idx}].gate_cleared disagrees with its own bands"))
        if p.get("hand_wavy_cap_cleared") is not actual_cap:
            findings.append(Finding(
                "SB-INVARIANT",
                f"gate.passes[{idx}].hand_wavy_cap_cleared disagrees with its own bands"))
    if passes:
        last = passes[-1]
        if isinstance(last, dict):
            expected_cleared = last.get("gate_cleared") is True and last.get("hand_wavy_cap_cleared") is True
            if gate.get("cleared") is not expected_cleared:
                findings.append(Finding(
                    "SB-GATE-CLEARED",
                    "gate.cleared disagrees with the last pass's gate_cleared/"
                    "hand_wavy_cap_cleared"))
    else:
        if gate.get("cleared") is not False:
            findings.append(Finding(
                "SB-GATE-CLEARED", "gate.cleared must be false when passes is empty"))
    return findings


def _re_entry_invariant_findings(re_entry) -> list[Finding]:
    """INV-09: re_entry.fired is false exactly when re_entry.edges is
    empty (SB-INVARIANT)."""
    if not isinstance(re_entry, dict):
        return []
    edges = re_entry.get("edges")
    if not isinstance(edges, list):
        return []
    fired = re_entry.get("fired")
    expected_fired = len(edges) > 0
    if fired is not expected_fired:
        return [Finding(
            "SB-INVARIANT", "re_entry.fired disagrees with whether re_entry.edges is empty")]
    return []


@functools.lru_cache(maxsize=1)
def _load_qh():
    """Load `check-quality-harness.py` as a module, cached. The cross-checks
    below reuse its prose extractors through this loader, following the
    pattern `check-emission-stage-a.py` established."""
    import importlib.util as _ilu
    import sys as _sys

    spec = _ilu.spec_from_file_location(
        "_qh_for_summary_block", REPO_ROOT / "scripts" / "check-quality-harness.py")
    qh = _ilu.module_from_spec(spec)
    _sys.modules["_qh_for_summary_block"] = qh
    spec.loader.exec_module(qh)
    return qh


# ---------------------------------------------------------------------------
# Prose readers shared by the cross-checks (CHECK-02)
# ---------------------------------------------------------------------------

_TAXONOMY_TYPES = frozenset(
    _SCHEMA_FOR_CONSTANTS["fields"]["assumptions"]["items"]["fields"]["type"]["enum"]
)

_BOLD_WHOLE_CELL_RE = re.compile(r"^\*\*(.*)\*\*$")
_TRAILING_PAREN_RE = re.compile(r"\s*\([^)]*\)\s*$")


def _parent_type(cell: str) -> str:
    """Strip bold markers around the whole cell, then a trailing
    parenthesised subtype, leaving the cell's parent type. A compound cell
    (e.g. "a / b") or any other annotation is deliberately left unchanged --
    it will not equal any single taxonomy value (D-16)."""
    s = cell.strip()
    m = _BOLD_WHOLE_CELL_RE.match(s)
    if m:
        s = m.group(1).strip()
    return _TRAILING_PAREN_RE.sub("", s).strip()


_LEADING_VERDICT_RE = re.compile(r"(Accept|Challenge|Discard)\b")


def _leading_verdict_token(cell: str) -> str | None:
    """The token that leads the row's Verdict cell, before its em-dash,
    bold markers stripped."""
    s = cell.strip().lstrip("*").strip()
    m = _LEADING_VERDICT_RE.match(s)
    return m.group(1) if m else None


def _table_columns(section_text: str, colnames: tuple[str, ...]) -> list[dict[str, str]]:
    """Locate a Markdown table's header row by column NAME (never index) and
    return each data row's cells for the requested columns, in row order.
    Empty when no header row carries every requested name."""
    qh = _load_qh()
    lines = section_text.splitlines()
    header_idx: int | None = None
    col_idx: dict[str, int] = {}
    for i, line in enumerate(lines):
        stripped = line.strip()
        if not stripped.startswith("|"):
            continue
        cells = qh._split_row(stripped)
        if qh._is_separator_row(cells):
            continue
        idx_map = {c.strip().lower(): j for j, c in enumerate(cells)}
        if all(name.lower() in idx_map for name in colnames):
            header_idx = i
            col_idx = {name: idx_map[name.lower()] for name in colnames}
            break
    if header_idx is None:
        return []
    rows: list[dict[str, str]] = []
    i = header_idx + 1
    if i < len(lines):
        sep_cells = qh._split_row(lines[i].strip())
        if qh._is_separator_row(sep_cells):
            i += 1
    while i < len(lines):
        stripped = lines[i].strip()
        if not stripped.startswith("|"):
            break
        cells = qh._split_row(stripped)
        rows.append({name: (cells[j] if j < len(cells) else "") for name, j in col_idx.items()})
        i += 1
    return rows


def _xc_assumptions(text, sections, block, exemplar) -> list[Finding]:
    """SB-ASSUMPTION: block assumptions vs section 2's table, by row order.
    An extractor returning no rows while the block carries items is itself a
    finding (length mismatch) rather than a vacuous pass."""
    findings: list[Finding] = []
    items = block.get("assumptions")
    if not isinstance(items, list):
        return findings
    section2 = (sections or {}).get(2, "")
    rows = _table_columns(section2, ("type", "verdict"))
    if len(rows) != len(items):
        findings.append(Finding(
            "SB-ASSUMPTION",
            f"block has {len(items)} assumptions but section 2's table has "
            f"{len(rows)} data row(s)",
        ))
    for i in range(min(len(rows), len(items))):
        item = items[i]
        if not isinstance(item, dict):
            continue
        expected_id = f"A-{i + 1}"
        if item.get("id") != expected_id:
            findings.append(Finding(
                "SB-ASSUMPTION",
                f"assumption {i + 1}: block id {item.get('id')!r} does not "
                f"match its row position {expected_id!r}",
            ))
        parent_type = _parent_type(rows[i]["type"])
        block_type = item.get("type")
        if exemplar:
            if block_type is None:
                if parent_type in _TAXONOMY_TYPES:
                    findings.append(Finding(
                        "SB-ASSUMPTION",
                        f"{expected_id}: block type is null but section 2's "
                        f"cell {rows[i]['type']!r} is a single taxonomy type "
                        f"({parent_type!r})",
                    ))
            elif block_type != parent_type:
                findings.append(Finding(
                    "SB-ASSUMPTION",
                    f"{expected_id}: block type {block_type!r} disagrees "
                    f"with section 2's cell {rows[i]['type']!r} (parent type "
                    f"{parent_type!r})",
                ))
        elif block_type is not None and block_type != parent_type:
            findings.append(Finding(
                "SB-ASSUMPTION",
                f"{expected_id}: block type {block_type!r} disagrees with "
                f"section 2's cell {rows[i]['type']!r} (parent type "
                f"{parent_type!r})",
            ))
        expected_verdict = _leading_verdict_token(rows[i]["verdict"])
        block_verdict = item.get("verdict")
        if block_verdict != expected_verdict:
            findings.append(Finding(
                "SB-ASSUMPTION",
                f"{expected_id}: block verdict {block_verdict!r} disagrees "
                f"with section 2's Verdict cell {rows[i]['verdict']!r} "
                f"(expected {expected_verdict!r})",
            ))
    return findings


_GT_DECL_LEAD_RE = re.compile(r"^\s*(?:[-*]|\d+[.)])\s+(?P<rest>.*)$")
_GT_DECL_TOKEN_RE = re.compile(r"^\*{0,2}GT-(?P<n>\d+)(?P<q>\??)")


def _gt_declarations(section3: str) -> list[tuple[str, bool]]:
    """Section 3's own canonical ground-truth declarations, in order,
    deduplicated: (id, read_at_source). The FIRST GT-<digits> token of each
    list-item line, optionally ?-suffixed, optionally bold."""
    declared: list[tuple[str, bool]] = []
    seen: set[str] = set()
    for line in section3.splitlines():
        lm = _GT_DECL_LEAD_RE.match(line)
        if not lm:
            continue
        tm = _GT_DECL_TOKEN_RE.match(lm.group("rest"))
        if not tm:
            continue
        gid = f"GT-{tm.group('n')}"
        if gid in seen:
            continue
        seen.add(gid)
        declared.append((gid, tm.group("q") != "?"))
    return declared


def _xc_ground_truths(text, sections, block, exemplar) -> list[Finding]:
    """SB-GROUND-TRUTH: block ground_truths vs section 3's own canonical
    declarations -- never against every later citation (A3)."""
    findings: list[Finding] = []
    items = block.get("ground_truths")
    if not isinstance(items, list):
        return findings
    section3 = (sections or {}).get(3, "")
    declared = _gt_declarations(section3)
    if len(declared) != len(items):
        findings.append(Finding(
            "SB-GROUND-TRUTH",
            f"block has {len(items)} ground truths but section 3 declares "
            f"{len(declared)}",
        ))
    for i in range(min(len(declared), len(items))):
        gid, read_at_source = declared[i]
        item = items[i]
        if not isinstance(item, dict):
            continue
        if item.get("id") != gid:
            findings.append(Finding(
                "SB-GROUND-TRUTH",
                f"ground truth {i + 1}: block id {item.get('id')!r} disagrees "
                f"with section 3's declared id {gid!r}",
            ))
        if item.get("read_at_source") != read_at_source:
            findings.append(Finding(
                "SB-GROUND-TRUTH",
                f"{gid}: block read_at_source {item.get('read_at_source')!r} "
                f"disagrees with section 3's declaration (expected "
                f"{read_at_source!r})",
            ))
    return findings


def _doc_chain_index(section4: str) -> tuple[list[str], list[str]]:
    """(doc_ids, doc_blocks) for section 4: ids normalized and upper-cased,
    aligned with `qh._chain_blocks`."""
    qh = _load_qh()
    ids = [qh._normalize_chain_id(cid).upper() for cid in qh._chain_ids(section4)]
    blocks = qh._chain_blocks(section4)
    return ids, blocks


def _xc_chain_ids(text, sections, block, exemplar) -> list[Finding]:
    """SB-CHAIN-ID: block chain ids vs section 4's chain ids, in order."""
    items = block.get("chains")
    if not isinstance(items, list):
        return []
    section4 = (sections or {}).get(4, "")
    doc_ids, _blocks = _doc_chain_index(section4)
    block_ids = [c.get("id") for c in items if isinstance(c, dict)]
    if block_ids != doc_ids:
        return [Finding(
            "SB-CHAIN-ID",
            f"block chain ids {block_ids!r} disagree with section 4's chain "
            f"ids {doc_ids!r}",
        )]
    return []


def _xc_chain_confidence(text, sections, block, exemplar) -> list[Finding]:
    """SB-CHAIN-CONFIDENCE: each chain's block confidence vs its own
    **Confidence:** line, read from section 4 only -- a decoy confidence
    line elsewhere in the document is invisible to this check."""
    qh = _load_qh()
    findings: list[Finding] = []
    items = block.get("chains")
    if not isinstance(items, list):
        return findings
    section4 = (sections or {}).get(4, "")
    doc_ids, doc_blocks = _doc_chain_index(section4)
    by_id = dict(zip(doc_ids, doc_blocks))
    for item in items:
        if not isinstance(item, dict):
            continue
        cid = item.get("id")
        doc_block = by_id.get(cid)
        if doc_block is None:
            continue
        label = qh._chain_confidence_label(doc_block)
        if label is None:
            findings.append(Finding(
                "SB-CHAIN-CONFIDENCE",
                f"{cid}: no readable **Confidence:** line in section 4",
            ))
            continue
        if item.get("confidence") != label:
            findings.append(Finding(
                "SB-CHAIN-CONFIDENCE",
                f"{cid}: block confidence {item.get('confidence')!r} "
                f"disagrees with section 4's Confidence line ({label!r})",
            ))
    return findings


def _xc_chain_rests_on(text, sections, block, exemplar) -> list[Finding]:
    """SB-CHAIN-RESTS-ON: block rests_on vs the chain head's own refs (GT
    tokens union upper-cased chain refs), compared as a SET (disclosed
    bound: rests_on-order-not-compared)."""
    qh = _load_qh()
    findings: list[Finding] = []
    items = block.get("chains")
    if not isinstance(items, list):
        return findings
    section4 = (sections or {}).get(4, "")
    doc_ids, doc_blocks = _doc_chain_index(section4)
    by_id = dict(zip(doc_ids, doc_blocks))
    for item in items:
        if not isinstance(item, dict):
            continue
        cid = item.get("id")
        doc_block = by_id.get(cid)
        if doc_block is None:
            continue
        gt_refs, chain_refs = qh._chain_head_refs(doc_block)
        expected = set(gt_refs) | {c.upper() for c in chain_refs}
        actual = set(item.get("rests_on") or [])
        if actual != expected:
            findings.append(Finding(
                "SB-CHAIN-RESTS-ON",
                f"{cid}: block rests_on {sorted(actual)!r} disagrees with "
                f"section 4's head refs {sorted(expected)!r}",
            ))
    return findings


_DEAD_END_HEADING_RE = re.compile(
    r"^#{2,4}\s*Dead End(?:\s+\d+)?\s*:\s*(?P<name>.+?)\s*$", re.MULTILINE
)


def _xc_dead_ends(text, sections, block, exemplar) -> list[Finding]:
    """SB-DEAD-END: block dead_ends vs section 5's own '### Dead End: ...'
    headings, in order."""
    names = block.get("dead_ends")
    if not isinstance(names, list):
        return []
    section5 = (sections or {}).get(5, "")
    doc_names = [
        re.sub(r"\s+", " ", m.group("name")).strip()
        for m in _DEAD_END_HEADING_RE.finditer(section5)
    ]
    if names != doc_names:
        return [Finding(
            "SB-DEAD-END",
            f"block dead_ends {names!r} disagree with section 5's Dead End "
            f"headings {doc_names!r}",
        )]
    return []


_TECH_NOT_APPLIED_HEADING_RE = re.compile(
    r"^##\s*Techniques not applied \(process output\)\s*$", re.MULTILINE
)
_TECH_NOT_APPLIED_LABEL_RE = re.compile(r"^Techniques not applied:\s*$", re.MULTILINE)
_TECH_LIST_ITEM_RE = re.compile(r"^\s*[-*]\s+(?P<body>.+)$")
_TECH_NOT_APPLIED_LINE_RE = re.compile(
    r"^(?P<tech>[a-z-]+)(?:\s+\(Phase\s+(?P<phase>[1-5])\))?\s+—\s+"
    r"not applicable\s+—\s+(?P<reason>.+)$"
)


def _techniques_not_applied_lines(text: str) -> list[str] | None:
    """Raw list-item bodies under the '## Techniques not applied (process
    output)' heading, or after a 'Techniques not applied:' label line, up to
    the next heading. None when neither marker is present anywhere (the
    exemplar null_when condition for `techniques`)."""
    m = _TECH_NOT_APPLIED_HEADING_RE.search(text) or _TECH_NOT_APPLIED_LABEL_RE.search(text)
    if m is None:
        return None
    out: list[str] = []
    for line in text[m.end():].splitlines():
        if not line.strip():
            continue
        if line.lstrip().startswith("#"):
            break
        lm = _TECH_LIST_ITEM_RE.match(line)
        if lm is not None:
            out.append(lm.group("body"))
    return out


def _xc_techniques(text, sections, block, exemplar) -> list[Finding]:
    """SB-TECHNIQUES / SB-NULL: block techniques.not_applied vs the
    document's own not-applied lines, in order. `techniques.applied` is
    schema-validated only (disclosed bound:
    techniques-applied-vocabulary-only); the prose carries no fixed marker
    for an applied technique."""
    findings: list[Finding] = []
    techniques = block.get("techniques")
    raw_lines = _techniques_not_applied_lines(text)
    if techniques is None:
        if exemplar and raw_lines is not None:
            findings.append(Finding(
                "SB-NULL",
                "techniques is null but a Techniques not applied block is "
                "present in the document",
            ))
        return findings
    if not isinstance(techniques, dict):
        return findings
    not_applied = techniques.get("not_applied")
    if not isinstance(not_applied, list):
        return findings
    parsed: list[re.Match] = []
    for raw in (raw_lines or []):
        pm = _TECH_NOT_APPLIED_LINE_RE.match(raw.strip())
        if pm is None:
            findings.append(Finding(
                "SB-TECHNIQUES", f"could not parse not-applied line: {raw!r}"
            ))
            continue
        parsed.append(pm)
    if len(parsed) != len(not_applied):
        findings.append(Finding(
            "SB-TECHNIQUES",
            f"block has {len(not_applied)} not-applied entries but the "
            f"document's not-applied block lists {len(parsed)} parseable "
            f"line(s)",
        ))
    for i in range(min(len(parsed), len(not_applied))):
        pm = parsed[i]
        item = not_applied[i]
        if not isinstance(item, dict):
            continue
        if item.get("technique") != pm.group("tech"):
            findings.append(Finding(
                "SB-TECHNIQUES",
                f"not_applied[{i}]: block technique {item.get('technique')!r} "
                f"disagrees with the document's {pm.group('tech')!r}",
            ))
        phase_str = pm.group("phase")
        # disclosed bound: not-applied-phase-only-where-stated
        if phase_str is not None and item.get("phase") != int(phase_str):
            findings.append(Finding(
                "SB-TECHNIQUES",
                f"not_applied[{i}]: block phase {item.get('phase')!r} "
                f"disagrees with the document's Phase {phase_str}",
            ))
        expected_reason = re.sub(r"\s+", " ", pm.group("reason")).strip()
        actual_reason = re.sub(r"\s+", " ", str(item.get("reason") or "")).strip()
        if actual_reason != expected_reason:
            findings.append(Finding(
                "SB-TECHNIQUES",
                f"not_applied[{i}]: block reason {item.get('reason')!r} "
                f"disagrees with the document's reason {expected_reason!r}",
            ))
    return findings


_MODE_STATEMENT_RE = re.compile(r"`?MODE\s*=\s*(?P<mode>[A-Za-z0-9-]+)`?")


def _text_outside_block(text: str) -> str:
    """`text` with the one summary block's own fence removed, so a MODE
    statement can never be misread from inside the JSON payload."""
    blocks = find_blocks(text)
    if len(blocks) != 1:
        return text
    lines = text.split("\n")
    b = blocks[0]
    return "\n".join(lines[: b.start] + lines[b.end + 1 :])


def _xc_run_mode(text, sections, block, exemplar) -> list[Finding]:
    """SB-RUN-MODE / SB-NULL: block run_mode vs a stated `MODE = ...`
    statement outside the block (disclosed bound:
    run-mode-only-where-stated -- not compared when the document states
    none)."""
    findings: list[Finding] = []
    m = _MODE_STATEMENT_RE.search(_text_outside_block(text))
    stated = m.group("mode") if m else None
    run_mode = block.get("run_mode")
    if run_mode is None:
        if exemplar and stated is not None:
            findings.append(Finding(
                "SB-NULL", f"run_mode is null but the document states MODE = {stated}"
            ))
        return findings
    if stated is not None and run_mode != stated:
        findings.append(Finding(
            "SB-RUN-MODE",
            f"block run_mode {run_mode!r} disagrees with the document's "
            f"MODE = {stated!r} statement",
        ))
    return findings


_RECOMMENDED_LEADIN_RE = re.compile(
    r"^\*\*Recommended approach(?P<tail>[^*\n]*):\*\*", re.MULTILINE
)
_BOLD_COLON_LEADIN_RE = re.compile(r"^\*\*[^*\n]+:\*\*", re.MULTILINE)
_ANY_HEADING_RE = re.compile(r"^#{1,6}[ \t]", re.MULTILINE)


def _normalize_for_compare(s: str) -> str:
    """Strip bold markers (disclosed bound:
    recommendation-bold-markers-ignored) and collapse whitespace runs."""
    return re.sub(r"\s+", " ", s.replace("**", "")).strip()


def _section6_recommendation(section6: str) -> str | None:
    """Section 6's own Recommended approach text, normalized, through every
    following line until the next bold-colon lead-in, a heading, or the end
    of section 6. None when the lead-in is not present at all."""
    m = _RECOMMENDED_LEADIN_RE.search(section6)
    if m is None:
        return None
    tail = m.group("tail").strip().lstrip("—–").strip().rstrip(":").strip()
    rest = section6[m.end():]
    end = len(rest)
    for pat in (_BOLD_COLON_LEADIN_RE, _ANY_HEADING_RE):
        pm = pat.search(rest)
        if pm is not None:
            end = min(end, pm.start())
    return _normalize_for_compare(tail + rest[:end])


def _xc_conclusion_text(text, sections, block, exemplar) -> list[Finding]:
    """SB-CONCLUSION-CUT / SB-CONCLUSION-TEXT: conclusion.recommendation vs
    section 6's own Recommended approach text, in full. Truncation is what
    is compared; a shorter block that is a strict prefix of the prose is
    SB-CONCLUSION-CUT, anything else disagreeing is SB-CONCLUSION-TEXT."""
    conclusion = block.get("conclusion")
    if not isinstance(conclusion, dict):
        return []
    block_rec = conclusion.get("recommendation")
    if not isinstance(block_rec, str):
        return []
    section6 = (sections or {}).get(6, "")
    prose = _section6_recommendation(section6)
    if prose is None:
        return []
    block_norm = _normalize_for_compare(block_rec)
    if block_norm == prose:
        return []
    if prose.startswith(block_norm) and len(prose) > len(block_norm):
        missing = prose[len(block_norm):].strip()[:60]
        return [Finding(
            "SB-CONCLUSION-CUT",
            f"conclusion.recommendation is cut short — missing: {missing!r}",
        )]
    return [Finding(
        "SB-CONCLUSION-TEXT",
        "conclusion.recommendation disagrees with section 6's Recommended "
        "approach text",
    )]


def _xc_conclusion_confidence(text, sections, block, exemplar) -> list[Finding]:
    """SB-CONCLUSION-CONFIDENCE: conclusion.confidence vs section 6's own
    **Confidence:** line, read with the quality harness's
    `_CONFIDENCE_LINE_RE` (accepts both the trailing-marker and bold-wrapped
    forms)."""
    qh = _load_qh()
    conclusion = block.get("conclusion")
    if not isinstance(conclusion, dict):
        return []
    block_conf = conclusion.get("confidence")
    if not isinstance(block_conf, str):
        return []
    section6 = (sections or {}).get(6, "")
    m = qh._CONFIDENCE_LINE_RE.search(section6)
    band = None
    if m is not None:
        word = m.group("word").upper()
        if word in ("HIGH", "MEDIUM", "LOW"):
            band = word
    if band is None:
        return [Finding(
            "SB-CONCLUSION-CONFIDENCE", "no readable **Confidence:** line in section 6"
        )]
    if block_conf != band:
        return [Finding(
            "SB-CONCLUSION-CONFIDENCE",
            f"conclusion.confidence {block_conf!r} disagrees with section "
            f"6's Confidence line ({band!r})",
        )]
    return []


# Cross-checks against the report's own prose (CHECK-02). Plan 01 left this
# an explicit empty tuple; each line below is `("<CODE>", _xc_<name>)`.
_CROSS_CHECKS: tuple[tuple[str, Callable[..., list[Finding]]], ...] = (
    ("SB-ASSUMPTION", _xc_assumptions),
    ("SB-GROUND-TRUTH", _xc_ground_truths),
    ("SB-CHAIN-ID", _xc_chain_ids),
    ("SB-CHAIN-CONFIDENCE", _xc_chain_confidence),
    ("SB-CHAIN-RESTS-ON", _xc_chain_rests_on),
    ("SB-DEAD-END", _xc_dead_ends),
    ("SB-TECHNIQUES", _xc_techniques),
    ("SB-RUN-MODE", _xc_run_mode),
    ("SB-CONCLUSION-CUT", _xc_conclusion_text),
    ("SB-CONCLUSION-CONFIDENCE", _xc_conclusion_confidence),
)


# ---------------------------------------------------------------------------
# Top-level entry point
# ---------------------------------------------------------------------------

def check_report(text: str, *, exemplar: bool = False, schema: dict | None = None) -> list[Finding]:
    """Detection -> placement -> parse -> schema -> null-mode -> internal
    invariants -> cross-checks. Never raises on a malformed report; raises
    SchemaError only for a schema problem."""
    if schema is None:
        schema = load_schema(DEFAULT_SCHEMA)
    blocks = find_blocks(text)
    if not blocks:
        return [Finding("SB-MISSING", "no summary block found in the report")]
    if len(blocks) > 1:
        return [Finding("SB-MULTIPLE", f"{len(blocks)} summary blocks found")]
    block = blocks[0]
    findings: list[Finding] = list(_placement_findings(text, block))
    try:
        value = json.loads(block.body)
    except json.JSONDecodeError as exc:
        findings.append(Finding(
            "SB-JSON", f"summary block body does not parse as JSON: {exc}"))
        return findings
    if not isinstance(value, dict):
        findings.append(Finding(
            "SB-JSON",
            f"summary block body is not a JSON object (got {type(value).__name__})"))
        return findings
    schema_findings = validate_report(value, schema, exemplar=exemplar)
    findings.extend(schema_findings)
    if not any(f.code == "SB-SCHEMA" for f in schema_findings):
        findings.extend(_gate_invariant_findings(value.get("gate")))
        findings.extend(_re_entry_invariant_findings(value.get("re_entry")))
        if _CROSS_CHECKS:
            qh = _load_qh()
            try:
                sections = qh._slice_sections(text)
            except qh.SectionResolutionError:
                sections = None
            for _code, fn in _CROSS_CHECKS:
                findings.extend(fn(text, sections, value, exemplar))
    return findings


# ---------------------------------------------------------------------------
# Synthetic self-test fixture
# ---------------------------------------------------------------------------

_CRITERION_TITLES = (
    "Identify Essence",
    "Challenge Assumptions",
    "Establish Ground Truths",
    "Reason Upward",
    "Validate",
    "Conclusion-to-Ground-Truth Traceability",
)


def _synthetic_report(block: dict, **overrides) -> str:
    """Build a minimal, complete report whose prose agrees with `block`.

    Override flags (all optional, default off):
      omit_block              -- drop the summary block
      duplicate_block          -- emit the block twice
      raw_block_body            -- use this literal string as the JSON body
      trailing_after_block      -- non-empty text placed after the closing fence
      omit_heading               -- drop the block's own heading line
      heading_before_appendix     -- place the heading (and block) before the
                                     Appendix heading
      type_cells                  -- dict of assumption id -> literal section 2
                                      Type cell text, overriding the plain
                                      `a['type']` rendering for that row only
      mode_statement               -- if given, write a top-of-document
                                       Step 0 set `MODE = <value>`. line
    """
    omit_block = overrides.get("omit_block", False)
    duplicate_block = overrides.get("duplicate_block", False)
    raw_block_body = overrides.get("raw_block_body")
    trailing_after_block = overrides.get("trailing_after_block", "")
    omit_heading = overrides.get("omit_heading", False)
    heading_before_appendix = overrides.get("heading_before_appendix", False)
    type_cells: dict = overrides.get("type_cells") or {}
    mode_statement = overrides.get("mode_statement")

    body_json = raw_block_body if raw_block_body is not None else json.dumps(block, indent=2)
    block_fence = f"```{BLOCK_FENCE}\n{body_json}\n```"

    assumptions = block.get("assumptions") or []
    ground_truths = block.get("ground_truths") or []
    chains = block.get("chains") or []
    dead_ends = block.get("dead_ends") or []
    techniques = block.get("techniques") or {"applied": [], "not_applied": []}
    gate = block.get("gate") or {"passes": [], "cleared": False, "fix_repeat_fired": False}
    conclusion = block.get("conclusion") or {}

    lines: list[str] = []
    if mode_statement is not None:
        lines.append(f"Step 0 set `MODE = {mode_statement}`.")
        lines.append("")
    lines += [
        "## Answer",
        "Synthetic answer for self-test fixtures.",
        "",
        "## 1. Problem Essence",
        "A synthetic problem essence statement for self-test purposes.",
        "",
        "## 2. Assumptions Table",
        "| Assumption | Type | Treatment | Verdict | Verification |",
        "|---|---|---|---|---|",
    ]
    for a in assumptions:
        atype = type_cells.get(a["id"], a.get("type") or "untested belief")
        lines.append(
            f"| Assumption {a['id']} | {atype} | Treated as stated | "
            f"{a['verdict']} — synthetic justification | Not applicable |"
        )
    lines += ["", "## 3. Ground Truths"]
    for gt in ground_truths:
        suffix = "" if gt["read_at_source"] else "?"
        lines.append(f"- **{gt['id']}{suffix}** synthetic ground truth statement.")
    lines += ["", "## 4. Derivation Chains"]
    for c in chains:
        lines.append(f"### Conclusion {c['id']}: synthetic conclusion")
        head = " + ".join(c.get("rests_on") or []) or "GT-1"
        lines.append(f"{head} → synthetic intermediate reasoning → synthetic conclusion.")
        lines.append(f"**Confidence:** {c['confidence']} — synthetic confidence rationale.")
        lines.append("")
    lines.append("## 5. Abandoned Reasoning")
    if dead_ends:
        for d in dead_ends:
            lines.append(f"### Dead End: {d}")
            lines.append("Synthetic reason this path was abandoned.")
            lines.append("")
    else:
        lines.append("Nothing material here.")
        lines.append("")
    lines.append("## 6. Conclusion")
    lines.append(f"**Recommended approach:** {conclusion.get('recommendation', '')}")
    lines.append("**Key insight:** synthetic key insight.")
    lines.append(
        f"**Confidence:** {conclusion.get('confidence', 'MEDIUM')} — synthetic confidence rationale."
    )
    lines.append("")

    appendix_heading_lines = [APPENDIX_HEADING, ""]

    techniques_lines: list[str] = []
    if techniques.get("not_applied"):
        techniques_lines.append("## Techniques not applied (process output)")
        for t in techniques["not_applied"]:
            techniques_lines.append(
                f"- {t['technique']} (Phase {t['phase']}) — not applicable — {t['reason']}"
            )
        techniques_lines.append("")

    gate_lines: list[str] = []
    if gate:
        passes = gate.get("passes") or []
        gate_lines.append("## Self-Audit Gate (process output)")
        for i, p in enumerate(passes[:-1], start=1):
            bands = p.get("bands") or []
            pieces = " · ".join(f"Criterion {n} {b}" for n, b in enumerate(bands, start=1))
            gate_lines.append(
                f"**Pass {i} (before re-score):** {pieces} · "
                f"Gate cleared: {'yes' if p.get('gate_cleared') else 'no'} · "
                f"Hand-wavy cap cleared: {'yes' if p.get('hand_wavy_cap_cleared') else 'no'}"
            )
        final_bands = passes[-1].get("bands") if passes else ["Absent"] * 6
        for n, (title, band) in enumerate(zip(_CRITERION_TITLES, final_bands), start=1):
            gate_lines.append(f"**Criterion {n}: {title}**")
            gate_lines.append('Quoted span: "synthetic evidence span."')
            gate_lines.append(f"Band: **{band}**")
            gate_lines.append("Justification: synthetic justification tying the span to the band.")
            gate_lines.append("")
        cleared_word = "cleared" if gate.get("cleared") else "not cleared"
        fired_word = "yes" if gate.get("fix_repeat_fired") else "no"
        gate_lines.append(
            f"**Gate result:** {cleared_word} · passes: {len(passes)} · "
            f"Fix/Repeat fired: {fired_word}"
        )
        gate_lines.append("")

    summary_heading_lines = [] if omit_heading else [BLOCK_HEADING, ""]
    if omit_block:
        block_lines: list[str] = []
    elif duplicate_block:
        block_lines = [block_fence, "", block_fence]
    else:
        block_lines = [block_fence]

    if heading_before_appendix:
        appendix_section = (
            summary_heading_lines + block_lines + [""] + appendix_heading_lines
            + techniques_lines + gate_lines
        )
    else:
        appendix_section = (
            appendix_heading_lines + techniques_lines + gate_lines
            + summary_heading_lines + block_lines
        )

    lines.extend(appendix_section)
    if trailing_after_block:
        lines.append(trailing_after_block)

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Self-test controls
# ---------------------------------------------------------------------------

def _c01_example_block_is_clean() -> str | None:
    schema = load_schema(DEFAULT_SCHEMA)
    text = _synthetic_report(schema["example"])
    findings = check_report(text, exemplar=False, schema=schema)
    if findings:
        return f"expected [], got {findings!r}"
    return None


def _c02_missing_block_is_rejected() -> str | None:
    schema = load_schema(DEFAULT_SCHEMA)
    text = _synthetic_report(schema["example"], omit_block=True)
    findings = check_report(text, schema=schema)
    if len(findings) != 1 or findings[0].code != "SB-MISSING":
        return f"expected exactly one SB-MISSING finding, got {findings!r}"
    return None


def _c03_duplicated_block_is_rejected() -> str | None:
    schema = load_schema(DEFAULT_SCHEMA)
    text = _synthetic_report(schema["example"], duplicate_block=True)
    findings = check_report(text, schema=schema)
    codes = {f.code for f in findings}
    if codes != {"SB-MULTIPLE"}:
        return f"expected codes == {{'SB-MULTIPLE'}}, got {codes!r} ({findings!r})"
    return None


def _c04_malformed_json_is_rejected() -> str | None:
    schema = load_schema(DEFAULT_SCHEMA)
    trailing_comma = _synthetic_report(
        schema["example"], raw_block_body='{"schema_version": 1, "run_mode": "full-composer",}')
    findings = check_report(trailing_comma, schema=schema)
    codes = {f.code for f in findings}
    if codes != {"SB-JSON"}:
        return f"trailing comma: expected {{'SB-JSON'}}, got {codes!r} ({findings!r})"
    array_body = _synthetic_report(schema["example"], raw_block_body='["schema_version", 1]')
    findings2 = check_report(array_body, schema=schema)
    codes2 = {f.code for f in findings2}
    if codes2 != {"SB-JSON"}:
        return f"array body: expected {{'SB-JSON'}}, got {codes2!r} ({findings2!r})"
    return None


def _c05_placement_defects_are_rejected() -> str | None:
    schema = load_schema(DEFAULT_SCHEMA)
    example = schema["example"]

    trailing = _synthetic_report(example, trailing_after_block="Some trailing prose after the block.")
    findings = check_report(trailing, schema=schema)
    codes = {f.code for f in findings}
    if codes != {"SB-PLACEMENT"}:
        return f"trailing prose: expected {{'SB-PLACEMENT'}}, got {codes!r} ({findings!r})"

    no_heading = _synthetic_report(example, omit_heading=True)
    findings2 = check_report(no_heading, schema=schema)
    codes2 = {f.code for f in findings2}
    if codes2 != {"SB-PLACEMENT"}:
        return f"heading missing: expected {{'SB-PLACEMENT'}}, got {codes2!r} ({findings2!r})"

    before_appendix = _synthetic_report(example, heading_before_appendix=True)
    findings3 = check_report(before_appendix, schema=schema)
    codes3 = {f.code for f in findings3}
    if codes3 != {"SB-PLACEMENT"}:
        return f"heading before Appendix: expected {{'SB-PLACEMENT'}}, got {codes3!r} ({findings3!r})"
    return None


def _c06_schema_violations_are_named() -> str | None:
    schema = load_schema(DEFAULT_SCHEMA)
    base = schema["example"]

    def _run(mutated, expected_path_substr):
        text = _synthetic_report(mutated)
        findings = check_report(text, schema=schema)
        codes = {f.code for f in findings}
        if codes != {"SB-SCHEMA"}:
            return f"expected codes == {{'SB-SCHEMA'}}, got {codes!r} ({findings!r})"
        if not any(expected_path_substr in f.message for f in findings):
            return f"expected a message naming {expected_path_substr!r}, got {findings!r}"
        return None

    cases = []

    m = copy.deepcopy(base)
    m["assumptions"][0]["verdict"] = "Reject"
    cases.append((m, "assumptions[0].verdict"))

    m = copy.deepcopy(base)
    m["chains"][0]["confidence"] = "high"
    cases.append((m, "chains[0].confidence"))

    m = copy.deepcopy(base)
    m["schema_version"] = 2
    cases.append((m, "schema_version"))

    m = copy.deepcopy(base)
    m["ground_truths"][0]["id"] = "GT-1?"
    cases.append((m, "ground_truths[0].id"))

    m = copy.deepcopy(base)
    del m["conclusion"]
    cases.append((m, "conclusion"))

    m = copy.deepcopy(base)
    m["model"] = "synthetic"
    cases.append((m, "model"))

    m = copy.deepcopy(base)
    m["gate"]["passes"][0]["bands"] = m["gate"]["passes"][0]["bands"] + ["Sound"]
    cases.append((m, "gate.passes[0].bands"))

    for mutated, expected in cases:
        msg = _run(mutated, expected)
        if msg:
            return f"({expected}): {msg}"
    return None


def _c07_live_null_gate_is_rejected() -> str | None:
    schema = load_schema(DEFAULT_SCHEMA)
    mutated = copy.deepcopy(schema["example"])
    mutated["gate"] = None
    text = _synthetic_report(mutated)
    findings = check_report(text, exemplar=False, schema=schema)
    codes = {f.code for f in findings}
    if codes != {"SB-NULL"}:
        return f"live mode: expected {{'SB-NULL'}}, got {codes!r} ({findings!r})"
    findings2 = check_report(text, exemplar=True, schema=schema)
    if any(f.code == "SB-NULL" for f in findings2):
        return f"exemplar mode: unexpected SB-NULL, got {findings2!r}"
    return None


def _c08_gate_and_reentry_invariants_are_enforced() -> str | None:
    schema = load_schema(DEFAULT_SCHEMA)

    m = copy.deepcopy(schema["example"])
    m["gate"]["passes"][0]["bands"] = ["Sound", "Hand-wavy", "Sound", "Hand-wavy", "Sound", "Sound"]
    m["gate"]["passes"][0]["hand_wavy_cap_cleared"] = True
    text = _synthetic_report(m)
    findings = check_report(text, schema=schema)
    codes = {f.code for f in findings}
    if codes != {"SB-INVARIANT"}:
        return f"two hand-wavy, cap true: expected {{'SB-INVARIANT'}}, got {codes!r} ({findings!r})"

    m2 = copy.deepcopy(schema["example"])
    m2["re_entry"]["fired"] = False
    text2 = _synthetic_report(m2)
    findings2 = check_report(text2, schema=schema)
    codes2 = {f.code for f in findings2}
    if codes2 != {"SB-INVARIANT"}:
        return f"fired false, edges non-empty: expected {{'SB-INVARIANT'}}, got {codes2!r} ({findings2!r})"
    return None


def _c09_gate_cleared_follows_last_pass() -> str | None:
    schema = load_schema(DEFAULT_SCHEMA)

    m = copy.deepcopy(schema["example"])
    m["gate"]["passes"][-1]["bands"] = ["Sound", "Hand-wavy", "Sound", "Hand-wavy", "Sound", "Sound"]
    m["gate"]["passes"][-1]["hand_wavy_cap_cleared"] = False
    m["gate"]["passes"][-1]["gate_cleared"] = True
    m["gate"]["cleared"] = True
    text = _synthetic_report(m)
    findings = check_report(text, schema=schema)
    codes = {f.code for f in findings}
    if codes != {"SB-GATE-CLEARED"}:
        return f"two hand-wavy, cleared true: expected {{'SB-GATE-CLEARED'}}, got {codes!r} ({findings!r})"

    m2 = copy.deepcopy(schema["example"])
    m2["gate"]["passes"][-1]["bands"] = ["Sound", "Hand-wavy", "Sound", "Sound", "Sound", "Sound"]
    m2["gate"]["passes"][-1]["hand_wavy_cap_cleared"] = True
    m2["gate"]["passes"][-1]["gate_cleared"] = True
    m2["gate"]["cleared"] = True
    text2 = _synthetic_report(m2)
    findings2 = check_report(text2, schema=schema)
    if findings2:
        return f"off-by-one guard (one hand-wavy): expected [], got {findings2!r}"
    return None


def _c10_unknown_schema_keyword_raises() -> str | None:
    schema = load_schema(DEFAULT_SCHEMA)
    mutated = copy.deepcopy(schema)
    mutated["fields"]["run_mode"]["oneOf"] = []
    with tempfile.TemporaryDirectory() as td:
        bad_schema_path = Path(td) / "bad-schema.json"
        bad_schema_path.write_text(json.dumps(mutated))
        try:
            load_schema(bad_schema_path)
        except SchemaError:
            pass
        else:
            return "load_schema did not raise SchemaError for an unknown keyword"

        report_path = Path(td) / "report.md"
        report_path.write_text(_synthetic_report(schema["example"]))
        rc = main(["--schema", str(bad_schema_path), str(report_path)])
        if rc != 2:
            return f"CLI with a bad --schema exited {rc}, expected 2"
    return None


def _c11_all_observed_codes_are_registered() -> str | None:
    schema = load_schema(DEFAULT_SCHEMA)
    example = schema["example"]
    observed: set[str] = set()

    fixtures = [
        _synthetic_report(example),
        _synthetic_report(example, omit_block=True),
        _synthetic_report(example, duplicate_block=True),
        _synthetic_report(example, raw_block_body='{"schema_version": 1,}'),
        _synthetic_report(example, trailing_after_block="trailing prose"),
        _synthetic_report(example, omit_heading=True),
        _synthetic_report(example, heading_before_appendix=True),
    ]
    for text in fixtures:
        for f in check_report(text, schema=schema):
            observed.add(f.code)

    bad_key = copy.deepcopy(example)
    bad_key["model"] = "x"
    for f in check_report(_synthetic_report(bad_key), schema=schema):
        observed.add(f.code)

    null_gate = copy.deepcopy(example)
    null_gate["gate"] = None
    for f in check_report(_synthetic_report(null_gate), schema=schema):
        observed.add(f.code)

    inv = copy.deepcopy(example)
    inv["re_entry"]["fired"] = False
    for f in check_report(_synthetic_report(inv), schema=schema):
        observed.add(f.code)

    unknown = observed - set(FINDING_CODES)
    if unknown:
        return f"observed codes outside FINDING_CODES: {sorted(unknown)!r}"
    if not observed:
        return "no codes observed across fixtures -- controls are not exercising findings"
    return None


def _c12_cli_round_trip() -> str | None:
    schema = load_schema(DEFAULT_SCHEMA)
    example = schema["example"]
    with tempfile.TemporaryDirectory() as td:
        good = Path(td) / "good.md"
        good.write_text(_synthetic_report(example))
        rc = main([str(good)])
        if rc != 0:
            return f"expected exit 0 for a clean report, got {rc}"

        bad = Path(td) / "bad.md"
        bad.write_text(_synthetic_report(example, omit_block=True))
        rc2 = main([str(bad)])
        if rc2 != 1:
            return f"expected exit 1 for a report missing its block, got {rc2}"

        missing = Path(td) / "does-not-exist.md"
        rc3 = main([str(missing)])
        if rc3 != 2:
            return f"expected exit 2 for a missing REPORT path, got {rc3}"
    return None


def _c13_synthetic_report_is_clean_with_cross_checks() -> str | None:
    schema = load_schema(DEFAULT_SCHEMA)
    text = _synthetic_report(schema["example"])
    findings = check_report(text, exemplar=False, schema=schema)
    if findings:
        return f"expected [], got {findings!r}"
    return None


def _c14_single_block_mutations_fire_named_codes() -> str | None:
    schema = load_schema(DEFAULT_SCHEMA)
    example = schema["example"]

    def _codes_for(mutated: dict) -> set[str]:
        text = _synthetic_report(example, raw_block_body=json.dumps(mutated))
        return {f.code for f in check_report(text, schema=schema)}

    cases: list[tuple[str, dict, set[str], bool]] = []

    m = copy.deepcopy(example)
    m["assumptions"][0]["verdict"] = "Challenge"
    cases.append(("assumption verdict swap", m, {"SB-ASSUMPTION"}, True))

    m = copy.deepcopy(example)
    m["assumptions"][0]["type"] = "untested belief"
    cases.append(("assumption type swap", m, {"SB-ASSUMPTION"}, True))

    m = copy.deepcopy(example)
    m["assumptions"].append({"id": "A-3", "type": "convention", "verdict": "Accept"})
    cases.append(("third assumption appended", m, {"SB-ASSUMPTION"}, True))

    m = copy.deepcopy(example)
    m["ground_truths"][1]["read_at_source"] = True
    cases.append(("GT-2 read_at_source true", m, {"SB-GROUND-TRUTH"}, True))

    m = copy.deepcopy(example)
    m["ground_truths"].append({"id": "GT-3", "read_at_source": True})
    cases.append(("GT-3 appended", m, {"SB-GROUND-TRUTH"}, True))

    m = copy.deepcopy(example)
    m["chains"][1]["id"] = "C3"
    cases.append(("chain C2 renamed C3", m, {"SB-CHAIN-ID"}, False))

    m = copy.deepcopy(example)
    m["chains"][0]["confidence"] = "MEDIUM"
    cases.append(("C1 confidence MEDIUM", m, {"SB-CHAIN-CONFIDENCE"}, True))

    m = copy.deepcopy(example)
    m["chains"][1]["rests_on"] = ["GT-2?"]
    cases.append(("C2 rests_on drops C1", m, {"SB-CHAIN-RESTS-ON"}, True))

    m = copy.deepcopy(example)
    m["dead_ends"] = ["Renamed dead end"]
    cases.append(("dead end renamed", m, {"SB-DEAD-END"}, True))

    m = copy.deepcopy(example)
    m["techniques"]["not_applied"][0]["reason"] = "a completely different reason"
    cases.append(("not_applied reason altered", m, {"SB-TECHNIQUES"}, True))

    m = copy.deepcopy(example)
    m["conclusion"]["confidence"] = "HIGH"
    cases.append(("conclusion confidence HIGH", m, {"SB-CONCLUSION-CONFIDENCE"}, True))

    full = example["conclusion"]["recommendation"]
    m = copy.deepcopy(example)
    m["conclusion"]["recommendation"] = full[: full.index(":") + 1]
    cases.append(("recommendation cut at its colon", m, {"SB-CONCLUSION-CUT"}, True))

    m = copy.deepcopy(example)
    m["conclusion"]["recommendation"] = full.replace("Adopt", "Reject", 1)
    cases.append(("recommendation with one word changed", m, {"SB-CONCLUSION-TEXT"}, True))

    for label, mutated, expected, exact in cases:
        codes = _codes_for(mutated)
        ok = codes == expected if exact else expected <= codes
        if not ok:
            rel = "==" if exact else ">="
            return f"{label}: expected codes {rel} {expected!r}, got {codes!r}"

    m = copy.deepcopy(example)
    m["run_mode"] = "focused-inversion"
    text = _synthetic_report(
        example, raw_block_body=json.dumps(m), mode_statement="full-composer"
    )
    codes = {f.code for f in check_report(text, schema=schema)}
    if codes != {"SB-RUN-MODE"}:
        return f"run_mode disagreement: expected {{'SB-RUN-MODE'}}, got {codes!r}"

    return None


def _c15_prose_mutations_that_still_pass() -> str | None:
    schema = load_schema(DEFAULT_SCHEMA)
    example = schema["example"]

    m = copy.deepcopy(example)
    m["assumptions"][0]["type"] = "convention"
    text = _synthetic_report(m, type_cells={"A-1": "convention / untested belief"})
    codes = {f.code for f in check_report(text, schema=schema)}
    if codes != {"SB-ASSUMPTION"}:
        return f"compound type cell (D-16): expected {{'SB-ASSUMPTION'}}, got {codes!r}"

    m2 = copy.deepcopy(example)
    m2["chains"][1]["rests_on"] = ["GT-2", "C1"]
    text2 = _synthetic_report(m2)
    findings2 = check_report(text2, schema=schema)
    if findings2:
        return (
            "GT-2 cited without '?' in a chain head must not affect the "
            f"ground-truth cross-check (the declaration governs): {findings2!r}"
        )
    return None


def _c15b_annotated_type_cells_match_parent() -> str | None:
    schema = load_schema(DEFAULT_SCHEMA)
    example = schema["example"]

    for block_type, cell_text in (
        ("untested belief", "untested belief (economic-hinge)"),
        ("convention", "**convention (regulatory)**"),
    ):
        m = copy.deepcopy(example)
        m["assumptions"][0]["type"] = block_type
        text = _synthetic_report(m, type_cells={"A-1": cell_text})
        findings = check_report(text, schema=schema)
        if any(f.code == "SB-ASSUMPTION" for f in findings):
            return f"{cell_text!r} should match parent type {block_type!r}, got {findings!r}"

    m = copy.deepcopy(example)
    m["assumptions"][0]["type"] = "untested belief"
    text = _synthetic_report(m, type_cells={"A-1": "untested belief (x) / convention"})
    codes = {f.code for f in check_report(text, schema=schema)}
    if codes != {"SB-ASSUMPTION"}:
        return f"compound cell with a trailing paren: expected {{'SB-ASSUMPTION'}}, got {codes!r}"
    return None


def _c15c_exemplar_type_nullability() -> str | None:
    schema = load_schema(DEFAULT_SCHEMA)
    example = schema["example"]

    m = copy.deepcopy(example)
    m["assumptions"][0]["type"] = None
    text = _synthetic_report(m, type_cells={"A-1": "factual"})
    findings = check_report(text, exemplar=True, schema=schema)
    if any(f.code == "SB-ASSUMPTION" for f in findings):
        return f"factual cell, null block type: expected no SB-ASSUMPTION, got {findings!r}"

    m2 = copy.deepcopy(example)
    m2["assumptions"][0]["type"] = "untested belief"
    text2 = _synthetic_report(m2, type_cells={"A-1": "factual"})
    findings2 = check_report(text2, exemplar=True, schema=schema)
    if {f.code for f in findings2} != {"SB-ASSUMPTION"}:
        return f"factual cell, non-null block type: expected {{'SB-ASSUMPTION'}}, got {findings2!r}"

    m3 = copy.deepcopy(example)
    m3["assumptions"][0]["type"] = None
    text3 = _synthetic_report(m3, type_cells={"A-1": "convention"})
    findings3 = check_report(text3, exemplar=True, schema=schema)
    if {f.code for f in findings3} != {"SB-ASSUMPTION"}:
        return f"convention cell, null block type: expected {{'SB-ASSUMPTION'}}, got {findings3!r}"

    m4 = copy.deepcopy(example)
    m4["assumptions"][0]["type"] = None
    text4 = _synthetic_report(m4)
    findings4 = check_report(text4, exemplar=False, schema=schema)
    if {f.code for f in findings4} != {"SB-NULL"}:
        return f"live mode null type: expected {{'SB-NULL'}}, got {findings4!r}"
    return None


def _c16_exemplar_null_iff_absent() -> str | None:
    schema = load_schema(DEFAULT_SCHEMA)
    example = schema["example"]

    m = copy.deepcopy(example)
    m["techniques"] = None
    text = _synthetic_report(m)
    findings = check_report(text, exemplar=True, schema=schema)
    if any(f.code == "SB-NULL" for f in findings):
        return f"techniques null, no not-applied block: unexpected SB-NULL, got {findings!r}"

    with_tech = copy.deepcopy(example)
    null_tech = copy.deepcopy(example)
    null_tech["techniques"] = None
    text2 = _synthetic_report(with_tech, raw_block_body=json.dumps(null_tech))
    findings2 = check_report(text2, exemplar=True, schema=schema)
    if {f.code for f in findings2} != {"SB-NULL"}:
        return f"techniques null, block present: expected {{'SB-NULL'}}, got {findings2!r}"

    m3 = copy.deepcopy(example)
    m3["run_mode"] = None
    text3 = _synthetic_report(m3)
    findings3 = check_report(text3, exemplar=True, schema=schema)
    if any(f.code == "SB-NULL" for f in findings3):
        return f"run_mode null, no MODE line: unexpected SB-NULL, got {findings3!r}"
    return None


_CONTROLS: tuple[tuple[str, Callable[[], str | None]], ...] = (
    ("C01", _c01_example_block_is_clean),
    ("C02", _c02_missing_block_is_rejected),
    ("C03", _c03_duplicated_block_is_rejected),
    ("C04", _c04_malformed_json_is_rejected),
    ("C05", _c05_placement_defects_are_rejected),
    ("C06", _c06_schema_violations_are_named),
    ("C07", _c07_live_null_gate_is_rejected),
    ("C08", _c08_gate_and_reentry_invariants_are_enforced),
    ("C09", _c09_gate_cleared_follows_last_pass),
    ("C10", _c10_unknown_schema_keyword_raises),
    ("C11", _c11_all_observed_codes_are_registered),
    ("C12", _c12_cli_round_trip),
    ("C13", _c13_synthetic_report_is_clean_with_cross_checks),
    ("C14", _c14_single_block_mutations_fire_named_codes),
    ("C15", _c15_prose_mutations_that_still_pass),
    ("C15b", _c15b_annotated_type_cells_match_parent),
    ("C15c", _c15c_exemplar_type_nullability),
    ("C16", _c16_exemplar_null_iff_absent),
)


def self_test() -> int:
    failures = []
    for cid, fn in _CONTROLS:
        try:
            msg = fn()
        except Exception as exc:  # noqa: BLE001
            msg = f"{type(exc).__name__}: {exc}"
        print(f"  {'FAIL' if msg else 'PASS'}  [{cid}]")
        if msg:
            failures.append(f"  [{cid}] {msg}")
    if failures:
        print(f"SUMMARY-BLOCK SELF-TEST: FAIL ({len(failures)}/{len(_CONTROLS)})")
        print("\n".join(failures))
        return 1
    print(f"SUMMARY-BLOCK SELF-TEST: PASS ({len(_CONTROLS)}/{len(_CONTROLS)} controls)")
    return 0


def _relpath(path: Path) -> str:
    try:
        return path.resolve().relative_to(REPO_ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def describe() -> dict:
    """Pure self-description. Every value is derived from this module's own
    data, never hand-typed."""
    schema = load_schema(DEFAULT_SCHEMA)
    return {
        "control_ids": [cid for cid, _fn in _CONTROLS],
        "control_count": len(_CONTROLS),
        "registered_surfaces": [_relpath(DEFAULT_SCHEMA)],
        "locked_constants": {
            "DEFAULT_SCHEMA": _relpath(DEFAULT_SCHEMA),
            "BLOCK_HEADING": BLOCK_HEADING,
            "SCHEMA_VERSION": schema.get("schema_version"),
        },
        "derived_counts": {
            "finding_codes": len(FINDING_CODES),
            "cross_checks": len(_CROSS_CHECKS),
        },
        "disclosed_bounds_anchors": sorted([
            "rests_on-order-not-compared",
            "not-applied-phase-only-where-stated",
            "techniques-applied-vocabulary-only",
            "run-mode-only-where-stated",
            "recommendation-bold-markers-ignored",
        ]),
    }


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("reports", nargs="*", metavar="REPORT")
    ap.add_argument("--exemplar", action="store_true")
    ap.add_argument("--json", action="store_true", dest="as_json")
    ap.add_argument("--schema", type=Path, default=None)
    ap.add_argument("--self-test", action="store_true")
    ap.add_argument("--describe", action="store_true")
    args = ap.parse_args(argv)

    if args.describe:
        print(json.dumps(describe(), indent=2, sort_keys=True))
        return 0
    if args.self_test:
        return self_test()

    if not args.reports:
        print("ERROR: no REPORT given", file=sys.stderr)
        return 2

    schema_path = args.schema if args.schema is not None else DEFAULT_SCHEMA
    try:
        schema = load_schema(schema_path)
    except SchemaError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2

    results: list[tuple[str, list[Finding]]] = []
    for report_arg in args.reports:
        report_path = Path(report_arg)
        try:
            text = report_path.read_text()
        except OSError as exc:
            print(f"ERROR: cannot read {report_arg}: {exc}", file=sys.stderr)
            return 2
        findings = check_report(text, exemplar=args.exemplar, schema=schema)
        results.append((report_arg, findings))

    any_failed = any(findings for _path, findings in results)

    if args.as_json:
        doc = {
            "schema": _relpath(schema_path),
            "mode": "exemplar" if args.exemplar else "live",
            "passed": not any_failed,
            "reports": [
                {
                    "path": path,
                    "passed": not findings,
                    "findings": [{"code": f.code, "message": f.message} for f in findings],
                }
                for path, findings in results
            ],
        }
        print(json.dumps(doc))
    else:
        for path, findings in results:
            for f in findings:
                print(f"{path}: {f.code}: {f.message}")
            if findings:
                print(f"SUMMARY-BLOCK: FAIL {path} ({len(findings)} finding(s))")
            else:
                print(f"SUMMARY-BLOCK: PASS {path}")

    return 1 if any_failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
