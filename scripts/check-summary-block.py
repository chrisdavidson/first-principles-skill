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

# Closed set of finding codes. Plan 01 emits the first eight; Plan 02 of
# v9.16 emitted fifteen cross-check codes (against the report's own prose);
# Phase 80 adds one more (SB-CONCLUSION-RESTS-ON); Phase 93 adds the eight
# SB-PRECHECK-* codes of the pre-check field comparator.
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
    "SB-CONCLUSION-RESTS-ON",
    "SB-PRECHECK-SHAPE",
    "SB-PRECHECK-HEAD",
    "SB-PRECHECK-CITED-BAND",
    "SB-PRECHECK-QMARK",
    "SB-PRECHECK-LOWEST",
    "SB-PRECHECK-CEILING",
    "SB-PRECHECK-BAND",
    "SB-PRECHECK-MISSING",
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
_KNOWN_FIELD_KEYS = (
    frozenset(
        {
            "type",
            "nullable",
            "const",
            "enum",
            "pattern",
            "items",
            "fields",
            "length",
            "minimum",
            "maximum",
        }
    )
    | _DOC_KEYS
)

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


def _fence_state(
    lines: list[str],
) -> tuple[list[bool], list[tuple[int, int, str, str]]]:
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
            blocks.append(
                _Block(start=start, end=end, info=info, body=body, under_heading=under)
            )
    return blocks


def _placement_findings(text: str, block: _Block) -> list[Finding]:
    """SB-PLACEMENT: heading absent, repeated, not after APPENDIX_HEADING,
    the block not under it, or anything other than whitespace following the
    block's closing fence."""
    lines = text.split("\n")
    inside, _fences = _fence_state(lines)
    heading_idxs = [
        i for i, l in enumerate(lines) if not inside[i] and l.strip() == BLOCK_HEADING
    ]
    appendix_idxs = [
        i
        for i, l in enumerate(lines)
        if not inside[i] and l.strip() == APPENDIX_HEADING
    ]
    findings: list[Finding] = []
    if not heading_idxs:
        findings.append(Finding("SB-PLACEMENT", f"{BLOCK_HEADING!r} heading not found"))
        return findings
    if len(heading_idxs) > 1:
        findings.append(
            Finding(
                "SB-PLACEMENT",
                f"{BLOCK_HEADING!r} heading appears {len(heading_idxs)} times",
            )
        )
    heading_idx = heading_idxs[0]
    if not any(a < heading_idx for a in appendix_idxs):
        findings.append(
            Finding(
                "SB-PLACEMENT",
                f"{BLOCK_HEADING!r} heading is not after {APPENDIX_HEADING!r}",
            )
        )
    if block.start <= heading_idx:
        findings.append(
            Finding("SB-PLACEMENT", "the summary block is not under its heading")
        )
    trailing = lines[block.end + 1 :]
    if any(l.strip() for l in trailing):
        findings.append(
            Finding(
                "SB-PLACEMENT",
                "non-whitespace content follows the block's closing fence",
            )
        )
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
        findings.append(
            Finding(
                "SB-SCHEMA", f"{path}: expected type {t}, got {type(value).__name__}"
            )
        )
        return findings
    if "const" in spec and value != spec["const"]:
        findings.append(
            Finding("SB-SCHEMA", f"{path}: expected {spec['const']!r}, got {value!r}")
        )
    if "enum" in spec and value not in spec["enum"]:
        findings.append(
            Finding("SB-SCHEMA", f"{path}: {value!r} is not one of {spec['enum']}")
        )
    if (
        "pattern" in spec
        and isinstance(value, str)
        and re.fullmatch(spec["pattern"], value) is None
    ):
        findings.append(
            Finding(
                "SB-SCHEMA",
                f"{path}: {value!r} does not match pattern {spec['pattern']!r}",
            )
        )
    if "length" in spec and hasattr(value, "__len__") and len(value) != spec["length"]:
        findings.append(
            Finding(
                "SB-SCHEMA",
                f"{path}: expected length {spec['length']}, got {len(value)}",
            )
        )
    if (
        "minimum" in spec
        and isinstance(value, (int, float))
        and not isinstance(value, bool)
        and value < spec["minimum"]
    ):
        findings.append(
            Finding("SB-SCHEMA", f"{path}: {value} is below minimum {spec['minimum']}")
        )
    if (
        "maximum" in spec
        and isinstance(value, (int, float))
        and not isinstance(value, bool)
        and value > spec["maximum"]
    ):
        findings.append(
            Finding("SB-SCHEMA", f"{path}: {value} is above maximum {spec['maximum']}")
        )
    if t == "array" and "items" in spec and isinstance(value, list):
        item_spec = spec["items"]
        for idx, item in enumerate(value):
            findings.extend(
                validate(item, item_spec, f"{path}[{idx}]", exemplar=exemplar)
            )
    if t == "object" and "fields" in spec and isinstance(value, dict):
        subfields = spec["fields"]
        for key in value:
            if key not in subfields:
                findings.append(Finding("SB-SCHEMA", f"{path}.{key}: unknown key"))
        for key, subspec in subfields.items():
            if key not in value:
                findings.append(
                    Finding("SB-SCHEMA", f"{path}.{key}: missing required key")
                )
                continue
            findings.extend(
                validate(value[key], subspec, f"{path}.{key}", exemplar=exemplar)
            )
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
        if (
            not isinstance(bands, list)
            or len(bands) != 6
            or not all(isinstance(b, str) for b in bands)
        ):
            continue
        actual_cleared = "Absent" not in bands
        actual_cap = bands.count("Hand-wavy") <= 1
        if p.get("gate_cleared") is not actual_cleared:
            findings.append(
                Finding(
                    "SB-INVARIANT",
                    f"gate.passes[{idx}].gate_cleared disagrees with its own bands",
                )
            )
        if p.get("hand_wavy_cap_cleared") is not actual_cap:
            findings.append(
                Finding(
                    "SB-INVARIANT",
                    f"gate.passes[{idx}].hand_wavy_cap_cleared disagrees with its own bands",
                )
            )
    if passes:
        last = passes[-1]
        if isinstance(last, dict):
            expected_cleared = (
                last.get("gate_cleared") is True
                and last.get("hand_wavy_cap_cleared") is True
            )
            if gate.get("cleared") is not expected_cleared:
                findings.append(
                    Finding(
                        "SB-GATE-CLEARED",
                        "gate.cleared disagrees with the last pass's gate_cleared/"
                        "hand_wavy_cap_cleared",
                    )
                )
    else:
        if gate.get("cleared") is not False:
            findings.append(
                Finding(
                    "SB-GATE-CLEARED", "gate.cleared must be false when passes is empty"
                )
            )
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
        return [
            Finding(
                "SB-INVARIANT",
                "re_entry.fired disagrees with whether re_entry.edges is empty",
            )
        ]
    return []


@functools.lru_cache(maxsize=1)
def _load_qh():
    """Load `check-quality-harness.py` as a module, cached. The cross-checks
    below reuse its prose extractors through this loader, following the
    pattern `check-emission-stage-a.py` established."""
    import importlib.util as _ilu
    import sys as _sys

    spec = _ilu.spec_from_file_location(
        "_qh_for_summary_block", REPO_ROOT / "scripts" / "check-quality-harness.py"
    )
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
# The taxonomy's locked subtype form, `<parent> — <discriminator>`
# (shared/spine/references/assumption-taxonomy.md, "Naming pattern (locked)").
# The discriminator may not contain "/", so a compound cell whose first
# type carries the subtype (`a — x / b`) is left whole and fails closed (D-16).
_EM_DASH_SUBTYPE_RE = re.compile(r"^(.*?) \u2014 [^/]+$")


def _strip_trailing_paren_group(s: str) -> str:
    """Drop one trailing parenthesised group, balanced, so a subtype whose
    own discriminator nests a paren (`convention (design-practice
    (codified))`, sanctioned by assumption-taxonomy.md's Table presentation
    list) is stripped whole. Only the group the final `)` closes is removed,
    so `a (x) / b (y)` leaves `a (x) / b` and still fails closed (D-16)."""
    s = s.rstrip()
    if not s.endswith(")"):
        return s
    depth = 0
    for i in range(len(s) - 1, -1, -1):
        if s[i] == ")":
            depth += 1
        elif s[i] == "(":
            depth -= 1
            if depth == 0:
                return s[:i].rstrip()
    return s


def _parent_type(cell: str) -> str:
    """Strip bold markers around the whole cell, then a trailing
    parenthesised subtype or the taxonomy's locked em-dash subtype
    (`<parent> — <discriminator>`), leaving the cell's parent type. The
    em-dash form is stripped only when what precedes it is exactly one
    taxonomy type, so a compound cell (e.g. "a / b") or any other
    annotation is deliberately left unchanged -- it will not equal any
    single taxonomy value (D-16)."""
    s = cell.strip()
    m = _BOLD_WHOLE_CELL_RE.match(s)
    if m:
        s = m.group(1).strip()
    s = _strip_trailing_paren_group(s)
    m = _EM_DASH_SUBTYPE_RE.match(s)
    if m and m.group(1).strip() in _TAXONOMY_TYPES:
        return m.group(1).strip()
    return s


_LEADING_VERDICT_RE = re.compile(r"(Accept|Challenge|Discard)\b")


def _leading_verdict_token(cell: str) -> str | None:
    """The token that leads the row's Verdict cell, before its em-dash,
    bold markers stripped."""
    s = cell.strip().lstrip("*").strip()
    m = _LEADING_VERDICT_RE.match(s)
    return m.group(1) if m else None


def _table_columns(
    section_text: str, colnames: tuple[str, ...]
) -> list[dict[str, str]]:
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
        rows.append(
            {name: (cells[j] if j < len(cells) else "") for name, j in col_idx.items()}
        )
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
        findings.append(
            Finding(
                "SB-ASSUMPTION",
                f"block has {len(items)} assumptions but section 2's table has "
                f"{len(rows)} data row(s)",
            )
        )
    for i in range(min(len(rows), len(items))):
        item = items[i]
        if not isinstance(item, dict):
            continue
        expected_id = f"A-{i + 1}"
        if item.get("id") != expected_id:
            findings.append(
                Finding(
                    "SB-ASSUMPTION",
                    f"assumption {i + 1}: block id {item.get('id')!r} does not "
                    f"match its row position {expected_id!r}",
                )
            )
        parent_type = _parent_type(rows[i]["type"])
        block_type = item.get("type")
        if exemplar:
            if block_type is None:
                if parent_type in _TAXONOMY_TYPES:
                    findings.append(
                        Finding(
                            "SB-ASSUMPTION",
                            f"{expected_id}: block type is null but section 2's "
                            f"cell {rows[i]['type']!r} is a single taxonomy type "
                            f"({parent_type!r})",
                        )
                    )
            elif block_type != parent_type:
                findings.append(
                    Finding(
                        "SB-ASSUMPTION",
                        f"{expected_id}: block type {block_type!r} disagrees "
                        f"with section 2's cell {rows[i]['type']!r} (parent type "
                        f"{parent_type!r})",
                    )
                )
        elif block_type is not None and block_type != parent_type:
            findings.append(
                Finding(
                    "SB-ASSUMPTION",
                    f"{expected_id}: block type {block_type!r} disagrees with "
                    f"section 2's cell {rows[i]['type']!r} (parent type "
                    f"{parent_type!r})",
                )
            )
        expected_verdict = _leading_verdict_token(rows[i]["verdict"])
        block_verdict = item.get("verdict")
        if block_verdict != expected_verdict:
            findings.append(
                Finding(
                    "SB-ASSUMPTION",
                    f"{expected_id}: block verdict {block_verdict!r} disagrees "
                    f"with section 2's Verdict cell {rows[i]['verdict']!r} "
                    f"(expected {expected_verdict!r})",
                )
            )
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
        findings.append(
            Finding(
                "SB-GROUND-TRUTH",
                f"block has {len(items)} ground truths but section 3 declares "
                f"{len(declared)}",
            )
        )
    for i in range(min(len(declared), len(items))):
        gid, read_at_source = declared[i]
        item = items[i]
        if not isinstance(item, dict):
            continue
        if item.get("id") != gid:
            findings.append(
                Finding(
                    "SB-GROUND-TRUTH",
                    f"ground truth {i + 1}: block id {item.get('id')!r} disagrees "
                    f"with section 3's declared id {gid!r}",
                )
            )
        if item.get("read_at_source") != read_at_source:
            findings.append(
                Finding(
                    "SB-GROUND-TRUTH",
                    f"{gid}: block read_at_source {item.get('read_at_source')!r} "
                    f"disagrees with section 3's declaration (expected "
                    f"{read_at_source!r})",
                )
            )
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
        return [
            Finding(
                "SB-CHAIN-ID",
                f"block chain ids {block_ids!r} disagree with section 4's chain "
                f"ids {doc_ids!r}",
            )
        ]
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
            findings.append(
                Finding(
                    "SB-CHAIN-CONFIDENCE",
                    f"{cid}: no readable **Confidence:** line in section 4",
                )
            )
            continue
        if item.get("confidence") != label:
            findings.append(
                Finding(
                    "SB-CHAIN-CONFIDENCE",
                    f"{cid}: block confidence {item.get('confidence')!r} "
                    f"disagrees with section 4's Confidence line ({label!r})",
                )
            )
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
            findings.append(
                Finding(
                    "SB-CHAIN-RESTS-ON",
                    f"{cid}: block rests_on {sorted(actual)!r} disagrees with "
                    f"section 4's head refs {sorted(expected)!r}",
                )
            )
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
        return [
            Finding(
                "SB-DEAD-END",
                f"block dead_ends {names!r} disagree with section 5's Dead End "
                f"headings {doc_names!r}",
            )
        ]
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
    m = _TECH_NOT_APPLIED_HEADING_RE.search(text) or _TECH_NOT_APPLIED_LABEL_RE.search(
        text
    )
    if m is None:
        return None
    out: list[str] = []
    for line in text[m.end() :].splitlines():
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
            findings.append(
                Finding(
                    "SB-NULL",
                    "techniques is null but a Techniques not applied block is "
                    "present in the document",
                )
            )
        return findings
    if not isinstance(techniques, dict):
        return findings
    not_applied = techniques.get("not_applied")
    if not isinstance(not_applied, list):
        return findings
    parsed: list[re.Match] = []
    for raw in raw_lines or []:
        pm = _TECH_NOT_APPLIED_LINE_RE.match(raw.strip())
        if pm is None:
            findings.append(
                Finding("SB-TECHNIQUES", f"could not parse not-applied line: {raw!r}")
            )
            continue
        parsed.append(pm)
    if len(parsed) != len(not_applied):
        findings.append(
            Finding(
                "SB-TECHNIQUES",
                f"block has {len(not_applied)} not-applied entries but the "
                f"document's not-applied block lists {len(parsed)} parseable "
                f"line(s)",
            )
        )
    for i in range(min(len(parsed), len(not_applied))):
        pm = parsed[i]
        item = not_applied[i]
        if not isinstance(item, dict):
            continue
        if item.get("technique") != pm.group("tech"):
            findings.append(
                Finding(
                    "SB-TECHNIQUES",
                    f"not_applied[{i}]: block technique {item.get('technique')!r} "
                    f"disagrees with the document's {pm.group('tech')!r}",
                )
            )
        phase_str = pm.group("phase")
        # disclosed bound: not-applied-phase-only-where-stated
        if phase_str is not None and item.get("phase") != int(phase_str):
            findings.append(
                Finding(
                    "SB-TECHNIQUES",
                    f"not_applied[{i}]: block phase {item.get('phase')!r} "
                    f"disagrees with the document's Phase {phase_str}",
                )
            )
        expected_reason = re.sub(r"\s+", " ", pm.group("reason")).strip()
        actual_reason = re.sub(r"\s+", " ", str(item.get("reason") or "")).strip()
        if actual_reason != expected_reason:
            findings.append(
                Finding(
                    "SB-TECHNIQUES",
                    f"not_applied[{i}]: block reason {item.get('reason')!r} "
                    f"disagrees with the document's reason {expected_reason!r}",
                )
            )
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
            findings.append(
                Finding(
                    "SB-NULL",
                    f"run_mode is null but the document states MODE = {stated}",
                )
            )
        return findings
    if stated is not None and run_mode != stated:
        findings.append(
            Finding(
                "SB-RUN-MODE",
                f"block run_mode {run_mode!r} disagrees with the document's "
                f"MODE = {stated!r} statement",
            )
        )
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
    rest = section6[m.end() :]
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
        missing = prose[len(block_norm) :].strip()[:60]
        return [
            Finding(
                "SB-CONCLUSION-CUT",
                f"conclusion.recommendation is cut short — missing: {missing!r}",
            )
        ]
    return [
        Finding(
            "SB-CONCLUSION-TEXT",
            "conclusion.recommendation disagrees with section 6's Recommended "
            "approach text",
        )
    ]


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
        return [
            Finding(
                "SB-CONCLUSION-CONFIDENCE",
                "no readable **Confidence:** line in section 6",
            )
        ]
    if block_conf != band:
        return [
            Finding(
                "SB-CONCLUSION-CONFIDENCE",
                f"conclusion.confidence {block_conf!r} disagrees with section "
                f"6's Confidence line ({band!r})",
            )
        ]
    return []


_PRECHECK_CHAIN_ID_RE = re.compile(r"^[Cc][1-9][0-9]*$")


def _section6_precheck_head_ids(section6: str) -> list[str] | str | None:
    """The §6 Conclusion's own **Pre-check:** head field as a plain ordered
    id list: each Cn with its (BAND) dropped and upper-cased (mirroring
    `_xc_chain_rests_on`'s chain-ref upper-casing), each bare GT-N/GT-N? kept
    as written. None when section6 carries no unfenced **Pre-check:** line at
    all. The sentinel string "UNREADABLE" when the first matching line's body
    has no readable `head ` field."""
    qh = _load_qh()
    lines = section6.splitlines()
    fenced = qh._fenced_code_flags(lines)
    for raw_line, in_fence in zip(lines, fenced):
        if in_fence:
            continue
        m = qh._PRECHECK_LINE_RE.match(raw_line)
        if m is None:
            continue
        parts = m.group("body").split(qh._PRECHECK_SEP)
        if len(parts) != 4 or not parts[0].startswith("head "):
            return "UNREADABLE"
        head_str = parts[0][len("head ") :].strip()
        ids: list[str] = []
        for item in (h.strip() for h in head_str.split(",") if h.strip()):
            im = qh._PRECHECK_HEAD_ITEM_RE.fullmatch(item) if "(" in item else None
            rid = im.group("id") if im else item
            if _PRECHECK_CHAIN_ID_RE.match(rid):
                rid = rid.upper()
            ids.append(rid)
        return ids
    return None


def _xc_conclusion_rests_on(text, sections, block, exemplar) -> list[Finding]:
    """SB-CONCLUSION-RESTS-ON: block conclusion.rests_on vs section 6's own
    **Pre-check:** head field, compared as a SET here. Order is compared
    separately, by `_xc_prechecks` as SB-PRECHECK-HEAD, and only when the two
    sets agree, so one defect never reports under both codes; the
    rests_on-order-not-compared bound still holds for `chains[].rests_on`.
    SB-NULL (exemplar mode only -- live mode's SB-NULL already comes from
    validate()) fires when rests_on is null but section 6 carries a
    Pre-check line."""
    conclusion = block.get("conclusion")
    if not isinstance(conclusion, dict):
        return []
    rests_on = conclusion.get("rests_on")
    section6 = (sections or {}).get(6, "")
    head = _section6_precheck_head_ids(section6)
    if rests_on is None:
        if exemplar and head is not None:
            return [
                Finding(
                    "SB-NULL",
                    "conclusion.rests_on is null but section 6 carries a "
                    "**Pre-check:** line",
                )
            ]
        return []
    if head is None:
        return [
            Finding(
                "SB-CONCLUSION-RESTS-ON",
                "conclusion.rests_on is non-null but section 6 carries no "
                "**Pre-check:** line",
            )
        ]
    if head == "UNREADABLE":
        return [
            Finding(
                "SB-CONCLUSION-RESTS-ON",
                "section 6's Pre-check line has no readable head field",
            )
        ]
    expected = set(head)
    actual = set(rests_on)
    if actual != expected:
        return [
            Finding(
                "SB-CONCLUSION-RESTS-ON",
                f"conclusion.rests_on {sorted(actual)!r} disagrees with section "
                f"6's Pre-check head {sorted(expected)!r}",
            )
        ]
    return []


# ---------------------------------------------------------------------------
# Pre-check field comparator (SB-PRECHECK-*)
# ---------------------------------------------------------------------------
#
# Grammar (output-template.md, "Confidence pre-check (Inputs axis)"): four
# fields separated by ` · `. `head ` (no colon) lists every identifier on the
# chain's head line in order, each Cn carrying its own band `Cn (BAND)`;
# `?-marked: ` the `?`-suffixed head ids or `none`; `lowest cited: ` the
# lowest band among the head's Cn or `none`; `Inputs ceiling: ` LOW if lowest
# cited is LOW, else MEDIUM if anything is ?-marked or lowest cited is MEDIUM,
# else HIGH. The paired Confidence label may sit at or below the ceiling,
# never above. The line regex, separator and head-item regex are the quality
# harness's own, reached through `_load_qh()`: one grammar, not two.

_PRECHECK_BAND_RANK = {"LOW": 0, "MEDIUM": 1, "HIGH": 2}
_PRECHECK_GT_ID_RE = re.compile(r"^GT-[1-9][0-9]*\??$")
_PRECHECK_CN_ID_RE = re.compile(r"^[Cc][1-9][0-9]*$")
# A head term's leading identifier: GT-N, GT-N? or Cn, then whitespace, `(`,
# `*` or end of term -- so `C1a` and `C2's` are not identifiers. Single
# level, anchored, matched with `.match()` (T-52-07 discipline).
_HEAD_LEAD_ID_RE = re.compile(r"^(GT-[1-9][0-9]*\??|[Cc][1-9][0-9]*)(?=[\s(*]|$)")


def _split_top_level_plus(s: str) -> list[str]:
    """Split `s` on `+` at parenthesis depth 0 only."""
    out: list[str] = []
    depth = 0
    cur: list[str] = []
    for ch in s:
        if ch == "(":
            depth += 1
        elif ch == ")" and depth > 0:
            depth -= 1
        if ch == "+" and depth == 0:
            out.append("".join(cur))
            cur = []
        else:
            cur.append(ch)
    out.append("".join(cur))
    return out


def _lead_id(term: str) -> str | None:
    """A head term's leading identifier (Cn upper-cased, GT-N? kept as
    written), after optional whitespace and `**`; None when it has none."""
    t = term.strip()
    if t.startswith("**"):
        t = t[2:].lstrip()
    m = _HEAD_LEAD_ID_RE.match(t)
    if m is None:
        return None
    rid = m.group(1)
    return rid.upper() if _PRECHECK_CN_ID_RE.match(rid) else rid


def _chain_head_ids(block: str) -> list[str] | None:
    """The chain's head-line identifiers, IN ORDER (D-06).

    Deliberately not `qh._chain_head_refs`, which returns sets (order lost)
    and takes the first line merely CONTAINING an identifier as the head --
    999.183's intro-sentence false positive. Here the head line is the first
    unfenced line after the block's own heading or bold label (line 0) whose
    first token, after optional whitespace and `**`, IS an identifier. The
    text before its first arrow (`→` or `->`) is split on `+` at parenthesis
    depth 0, and each term contributes its own leading identifier, so a
    parenthetical mention (`GT-1 (see GT-9)`) is never read as an input.
    Returns None -- reported unlocated, never guessed -- when no line
    qualifies or any term has no leading identifier."""
    qh = _load_qh()
    lines = block.splitlines()
    fenced = qh._fenced_code_flags(lines)
    for idx, raw in enumerate(lines):
        if idx == 0 or fenced[idx]:
            continue
        if _lead_id(raw) is None:
            continue
        head = raw
        for arrow in ("→", "->"):
            pos = head.find(arrow)
            if pos != -1:
                head = head[:pos]
        ids: list[str] = []
        for term in _split_top_level_plus(head):
            rid = _lead_id(term)
            if rid is None:
                return None
            ids.append(rid)
        return ids
    return None


def _parse_precheck(body: str) -> dict | str:
    """Parse a **Pre-check:** body into `{head: [(id, band|None)], qmark:
    list|'none', lowest: band|'none', ceiling: band}`, or return an error
    string naming the first violation. Splitting is `str.split` throughout,
    never a nested regex (T-52-07)."""
    qh = _load_qh()
    parts = body.strip().split(qh._PRECHECK_SEP)
    if len(parts) != 4:
        return f"expected 4 ` · `-separated fields, found {len(parts)}"
    prefixes = ("head ", "?-marked: ", "lowest cited: ", "Inputs ceiling: ")
    values: list[str] = []
    for part, prefix in zip(parts, prefixes):
        if not part.startswith(prefix):
            return f"field {part!r} does not start with {prefix!r}"
        values.append(part[len(prefix) :].strip())
    head_s, qmark_s, lowest_s, ceiling_s = values

    head: list[tuple[str, str | None]] = []
    if not head_s:
        return "empty head field"
    for item in head_s.split(", "):
        item = item.strip()
        if _PRECHECK_GT_ID_RE.match(item):
            head.append((item, None))
            continue
        im = qh._PRECHECK_HEAD_ITEM_RE.fullmatch(item)
        if im is None or not _PRECHECK_CN_ID_RE.match(im.group("id")):
            return f"head item {item!r} is neither a bare GT-N[?] nor `Cn (BAND)`"
        band = im.group("band")
        if band not in _PRECHECK_BAND_RANK:
            return f"head item {item!r} carries band {band!r}, not HIGH/MEDIUM/LOW"
        head.append((im.group("id").upper(), band))

    if qmark_s == "none":
        qmark: list[str] | str = "none"
    else:
        qmark = qmark_s.split(", ")
        for q in qmark:
            if not (_PRECHECK_GT_ID_RE.match(q) and q.endswith("?")):
                return f"?-marked item {q!r} is not a GT-N? id"
    if lowest_s != "none" and lowest_s not in _PRECHECK_BAND_RANK:
        return f"lowest cited {lowest_s!r} is neither `none` nor a band"
    if ceiling_s not in _PRECHECK_BAND_RANK:
        return f"Inputs ceiling {ceiling_s!r} is not a band"
    return {"head": head, "qmark": qmark, "lowest": lowest_s, "ceiling": ceiling_s}


def _precheck_field_findings(
    where: str,
    parsed: dict,
    truth_head: list[str] | None,
    chain_bands: dict[str, str | None],
    label: str,
    *,
    section6: bool,
) -> list[Finding]:
    """Compare one parsed pre-check with the truth it summarises.

    Fields 2-4 are derived from the STATED head ids combined with each cited
    Cn's TRUE section 4 band, so each defect fires its own code alone: a
    wrong head fires HEAD, not also QMARK/LOWEST/CEILING; a wrong cited band
    fires CITED-BAND, not also LOWEST. `truth_head` is the chain's head-line
    ids for section 4, or `conclusion.rests_on` (or None) for section 6."""
    findings: list[Finding] = []
    stated_ids = [rid for rid, _band in parsed["head"]]

    if not section6:
        if truth_head is None:
            findings.append(Finding("SB-PRECHECK-HEAD", f"{where}: head line not located"))
        elif stated_ids != truth_head:
            findings.append(
                Finding(
                    "SB-PRECHECK-HEAD",
                    f"{where}: Pre-check head {stated_ids!r} disagrees with the "
                    f"chain's head line {truth_head!r} (ids in head-line order)",
                )
            )
    elif (
        isinstance(truth_head, list)
        and set(stated_ids) == set(truth_head)
        and stated_ids != truth_head
    ):
        findings.append(
            Finding(
                "SB-PRECHECK-HEAD",
                f"{where}: Pre-check head order {stated_ids!r} disagrees with "
                f"conclusion.rests_on order {truth_head!r}",
            )
        )

    true_cited: list[str] = []
    for rid, band in parsed["head"]:
        if band is None:
            continue
        if rid not in chain_bands:
            findings.append(
                Finding(
                    "SB-PRECHECK-CITED-BAND",
                    f"{where}: head cites {rid} ({band}), but {rid} is not a "
                    f"section 4 chain",
                )
            )
            continue
        true_band = chain_bands[rid]
        if true_band is None:
            findings.append(
                Finding(
                    "SB-PRECHECK-CITED-BAND",
                    f"{where}: head cites {rid} ({band}), but chain {rid} has no "
                    f"readable section 4 band",
                )
            )
            continue
        true_cited.append(true_band)
        if band != true_band:
            findings.append(
                Finding(
                    "SB-PRECHECK-CITED-BAND",
                    f"{where}: head cites {rid} ({band}), but chain {rid}'s "
                    f"section 4 band is {true_band}",
                )
            )

    expected_q = [rid for rid in stated_ids if rid.endswith("?")]
    stated_q = [] if parsed["qmark"] == "none" else list(parsed["qmark"])
    if stated_q != expected_q:
        findings.append(
            Finding(
                "SB-PRECHECK-QMARK",
                f"{where}: ?-marked {', '.join(stated_q) or 'none'!r} disagrees "
                f"with the head's ?-suffixed ids {', '.join(expected_q) or 'none'!r}",
            )
        )

    expected_lowest = (
        min(true_cited, key=_PRECHECK_BAND_RANK.__getitem__) if true_cited else "none"
    )
    if parsed["lowest"] != expected_lowest:
        findings.append(
            Finding(
                "SB-PRECHECK-LOWEST",
                f"{where}: lowest cited {parsed['lowest']!r} disagrees with the "
                f"lowest section 4 band among the head's chains ({expected_lowest!r})",
            )
        )

    if expected_lowest == "LOW":
        expected_ceiling = "LOW"
    elif expected_q or expected_lowest == "MEDIUM":
        expected_ceiling = "MEDIUM"
    else:
        expected_ceiling = "HIGH"
    if parsed["ceiling"] != expected_ceiling:
        findings.append(
            Finding(
                "SB-PRECHECK-CEILING",
                f"{where}: Inputs ceiling {parsed['ceiling']!r} disagrees with the "
                f"derived ceiling {expected_ceiling!r}",
            )
        )

    if _PRECHECK_BAND_RANK[label] > _PRECHECK_BAND_RANK[expected_ceiling]:
        findings.append(
            Finding(
                "SB-PRECHECK-BAND",
                f"{where}: Confidence {label} ranks above the derived Inputs "
                f"ceiling {expected_ceiling}",
            )
        )
    return findings


def _confidence_and_precheck(
    lines: list[str], fenced: list[bool], start: int = 0
) -> tuple[int | None, str | None, str | None]:
    """(confidence line index, band, paired pre-check body) for the first
    unfenced `**Confidence:**` line at or after `start`. The band is None
    (the line counts as unlocated) when its word is not HIGH/MEDIUM/LOW. The
    pre-check is paired only when it is the line DIRECTLY above (D-02 strict
    adjacency): a blank line in between means unpaired."""
    qh = _load_qh()
    for i in range(start, len(lines)):
        if fenced[i]:
            continue
        m = qh._CONFIDENCE_LINE_RE.match(lines[i])
        if m is None:
            continue
        word = m.group("word").upper()
        if word not in _PRECHECK_BAND_RANK:
            return None, None, None
        body = None
        if i > 0 and not fenced[i - 1]:
            pm = qh._PRECHECK_LINE_RE.match(lines[i - 1])
            if pm is not None:
                body = pm.group("body")
        return i, word, body
    return None, None, None


def _orphan_lines(
    lines: list[str], fenced: list[bool], paired_idx: int | None, start: int = 0
) -> int:
    """Unfenced pre-check lines at or after `start` other than the one at
    `paired_idx` (the line directly above the paired Confidence line)."""
    qh = _load_qh()
    n = 0
    for i in range(start, len(lines)):
        if fenced[i] or i == paired_idx:
            continue
        if qh._PRECHECK_LINE_RE.match(lines[i]):
            n += 1
    return n


def _precheck_sites(sections: dict) -> dict:
    """Every pre-check site in sections 4 and 6.

    Returns `{sites, orphans, chains, confidence_lines, chain_bands}`. Each
    site is `{where, label, body, head}`: `label` None when the section's
    Confidence line is not located, `body` the paired pre-check body or
    None, `head` the chain's head-line ids (section 4 only). `orphans` lists
    the where-string of each unfenced pre-check line that is not directly
    above its section's paired Confidence line."""
    qh = _load_qh()
    section4 = sections.get(4, "") or ""
    section6 = sections.get(6, "") or ""
    doc_ids, doc_blocks = _doc_chain_index(section4)
    sites: list[dict] = []
    orphans: list[str] = []
    chain_bands: dict[str, str | None] = {}

    # Section 4 text before the first chain block (or all of it, when no
    # chain label is found) holds no site; any pre-check there is an orphan.
    if doc_ids and doc_blocks:
        preamble = section4[: section4.find(doc_blocks[0])]
    else:
        preamble = section4
    pre_lines = preamble.splitlines()
    for _ in range(_orphan_lines(pre_lines, qh._fenced_code_flags(pre_lines), None)):
        orphans.append("section 4 (before the first chain)")

    for cid, blk in zip(doc_ids, doc_blocks):
        chain_bands[cid] = qh._chain_confidence_label(blk)
        lines = blk.splitlines()
        fenced = qh._fenced_code_flags(lines)
        idx, band, body = _confidence_and_precheck(lines, fenced, start=1)
        paired_idx = idx - 1 if (idx is not None and body is not None) else None
        sites.append(
            {"where": cid, "label": band, "body": body, "head": _chain_head_ids(blk)}
        )
        for _ in range(_orphan_lines(lines, fenced, paired_idx)):
            orphans.append(cid)

    lines6 = section6.splitlines()
    fenced6 = qh._fenced_code_flags(lines6)
    idx6, band6, body6 = _confidence_and_precheck(lines6, fenced6)
    paired6 = idx6 - 1 if (idx6 is not None and body6 is not None) else None
    sites.append({"where": "section 6", "label": band6, "body": body6, "head": None})
    for _ in range(_orphan_lines(lines6, fenced6, paired6)):
        orphans.append("section 6")

    return {
        "sites": sites,
        "orphans": orphans,
        "chains": len(doc_ids),
        "confidence_lines": sum(1 for s in sites if s["label"] is not None),
        "chain_bands": chain_bands,
    }


def _precheck_site_findings(site: dict, chain_bands: dict, rests_on) -> list[Finding]:
    """SHAPE or field findings for one paired site (none for an unpaired
    one)."""
    if site["label"] is None or site["body"] is None:
        return []
    parsed = _parse_precheck(site["body"])
    if isinstance(parsed, str):
        return [Finding("SB-PRECHECK-SHAPE", f"{site['where']}: {parsed}")]
    section6 = site["where"] == "section 6"
    truth = (rests_on if isinstance(rests_on, list) else None) if section6 else site["head"]
    return _precheck_field_findings(
        site["where"], parsed, truth, chain_bands, site["label"], section6=section6
    )


def _xc_prechecks(text, sections, block, exemplar) -> list[Finding]:
    """SB-PRECHECK-*: each **Pre-check:** line directly above a section 4
    chain's or section 6's **Confidence:** line, compared field by field
    with its own chain (head-line ids in order, each cited Cn's section 4
    band, the derived ?-marked / lowest cited / Inputs ceiling) and its
    paired label against that ceiling.

    Disclosed bounds:
    precheck-missing-fails-in-exemplar-mode-only -- a Confidence line with
    no pre-check directly above it is SB-PRECHECK-MISSING in exemplar mode
    only; live mode never emits it, because a live presence reading is
    K-of-N and barred from gating, and `--precheck-reading` reports it.
    precheck-band-raised-to-ceiling-undetectable -- a label at or below its
    derived ceiling is legal, so a band raised up to its ceiling passes this
    checker; only a diff of the Confidence lines guards against that.
    precheck-section6-head-completeness-not-checked -- section 6's head is
    compared with conclusion.rests_on for order and with section 4 for
    bands; nothing checks that it names every chain the Conclusion rests
    on, which is a reading of section 6's prose.
    precheck-overlaps-qual01-precheck-defects -- QUAL-01's
    `_precheck_defects` stays and checks a pre-check's internal consistency,
    blank-line tolerant; this comparator checks it against the chain and is
    strict about adjacency."""
    if sections is None:
        return []
    conclusion = block.get("conclusion") if isinstance(block, dict) else None
    rests_on = conclusion.get("rests_on") if isinstance(conclusion, dict) else None
    read = _precheck_sites(sections)
    findings: list[Finding] = []
    for site in read["sites"]:
        findings.extend(_precheck_site_findings(site, read["chain_bands"], rests_on))
    if exemplar:
        for site in read["sites"]:
            if site["label"] is not None and site["body"] is None:
                findings.append(
                    Finding(
                        "SB-PRECHECK-MISSING",
                        f"{site['where']}: no **Pre-check:** line directly above "
                        f"its **Confidence:** line",
                    )
                )
        for where in read["orphans"]:
            findings.append(
                Finding(
                    "SB-PRECHECK-MISSING",
                    f"{where}: a **Pre-check:** line is not directly above its "
                    f"**Confidence:** line",
                )
            )
        if read["confidence_lines"] != read["chains"] + 1:
            findings.append(
                Finding(
                    "SB-PRECHECK-MISSING",
                    f"{read['confidence_lines']} Confidence line(s) located for "
                    f"{read['chains']} chain(s) plus section 6",
                )
            )
    return findings


def precheck_reading(text: str) -> dict:
    """Report-only reading of a document's pre-checks, sharing
    `_xc_prechecks`'s site reader and comparator. Integer keys: chains,
    confidence_lines, compared, missing, orphans, field_findings. A document
    whose sections cannot be resolved reads all zeros."""
    qh = _load_qh()
    zero = dict.fromkeys(
        ("chains", "confidence_lines", "compared", "missing", "orphans", "field_findings"),
        0,
    )
    try:
        sections = qh._slice_sections(text)
    except qh.SectionResolutionError:
        return zero
    rests_on = None
    blocks = find_blocks(text)
    if len(blocks) == 1:
        try:
            value = json.loads(blocks[0].body)
        except json.JSONDecodeError:
            value = None
        if isinstance(value, dict) and isinstance(value.get("conclusion"), dict):
            rests_on = value["conclusion"].get("rests_on")
    read = _precheck_sites(sections)
    located = [s for s in read["sites"] if s["label"] is not None]
    field = 0
    for site in located:
        field += len(_precheck_site_findings(site, read["chain_bands"], rests_on))
    return {
        "chains": read["chains"],
        "confidence_lines": read["confidence_lines"],
        "compared": sum(1 for s in located if s["body"] is not None),
        "missing": sum(1 for s in located if s["body"] is None),
        "orphans": len(read["orphans"]),
        "field_findings": field,
    }


# ---------------------------------------------------------------------------
# Gate span / disclosure region locators and their fixed-form readers
# ---------------------------------------------------------------------------
#
# The PRD's personal-general failure came from reading a whole-document
# sentence ("There was therefore no Phase 2 re-entry.") as a Gate verdict.
# Every reader below is therefore scoped to exactly two spans: the
# Self-Audit Gate section's own fixed lines, and the pre-first-heading
# disclosure region where a `**Disclosed:**` paragraph lives -- never the
# whole document.

_GATE_HEADING_TEXT = "## Self-Audit Gate (process output)"
_H2_LINE_RE = re.compile(r"^##[ \t]")


def _gate_span(text: str) -> str | None:
    """From the Gate heading line to the next '## ' heading outside a fence,
    or end of text. None when the heading is not present outside a fence."""
    qh = _load_qh()
    lines = text.split("\n")
    fenced = qh._fenced_code_flags(lines)
    start_idx = None
    for i, line in enumerate(lines):
        if fenced[i]:
            continue
        if line.strip() == _GATE_HEADING_TEXT:
            start_idx = i
            break
    if start_idx is None:
        return None
    end_idx = len(lines)
    for i in range(start_idx + 1, len(lines)):
        if fenced[i]:
            continue
        if _H2_LINE_RE.match(lines[i]):
            end_idx = i
            break
    return "\n".join(lines[start_idx:end_idx])


def _disclosure_region(text: str) -> str:
    """Text before the first '## ' heading outside a fence -- the top of the
    delivered file, where a top-of-response `**Disclosed:**` paragraph is
    written (never as a heading)."""
    qh = _load_qh()
    lines = text.split("\n")
    fenced = qh._fenced_code_flags(lines)
    for i, line in enumerate(lines):
        if fenced[i]:
            continue
        if _H2_LINE_RE.match(line):
            return "\n".join(lines[:i])
    return text


_DISCLOSED_PARA_RE = re.compile(r"^\*\*Disclosed:\*\*.*$", re.MULTILINE)


def _disclosed_paragraphs(region: str) -> list[str]:
    return [m.group(0) for m in _DISCLOSED_PARA_RE.finditer(region)]


_ANY_EDGE_NAME_RE = re.compile(
    r"re-entry edge|Fix/Repeat|return(?:ed)? to Phase [12]|re-open", re.IGNORECASE
)


def _names_second_order(p: str) -> bool:
    return bool(re.search(r"Phase\s*2", p)) and bool(
        re.search(r"re-entry|return|re-challeng", p, re.IGNORECASE)
    )


def _names_input_reopen(p: str) -> bool:
    return bool(re.search(r"re-open|reopen", p, re.IGNORECASE))


_PASS_LEAD_RE = re.compile(
    r"^\*\*Pass[ \t]+(?P<num>\d+)[ \t]*\(before re-score\):\*\*[ \t]*(?P<rest>.*)$"
)
_CRITERION_PIECE_RE = re.compile(
    r"^Criterion[ \t]+(?P<n>[1-6])[ \t]+(?P<band>Absent|Hand-wavy|Sound|Rigorous)$"
)
_GATE_CLEARED_PIECE_RE = re.compile(r"^Gate cleared:[ \t]*(?P<v>yes|no)$")
_CAP_CLEARED_PIECE_RE = re.compile(r"^Hand-wavy cap cleared:[ \t]*(?P<v>yes|no)$")


def _parse_pass_line(line: str) -> tuple[int, list[str], bool, bool] | None:
    """Parse a fixed-form '**Pass N (before re-score):** ...' line into
    (num, bands[6], gate_cleared, cap_cleared), or None when it does not
    parse to the fixed form (74-prose-inserts.md B6) exactly."""
    m = _PASS_LEAD_RE.match(line.strip())
    if m is None:
        return None
    pieces = [p.strip() for p in m.group("rest").split("·")]
    if len(pieces) != 8:
        return None
    bands: list[str] = []
    for i in range(6):
        cm = _CRITERION_PIECE_RE.match(pieces[i])
        if cm is None or int(cm.group("n")) != i + 1:
            return None
        bands.append(cm.group("band"))
    gm = _GATE_CLEARED_PIECE_RE.match(pieces[6])
    cm2 = _CAP_CLEARED_PIECE_RE.match(pieces[7])
    if gm is None or cm2 is None:
        return None
    return int(m.group("num")), bands, gm.group("v") == "yes", cm2.group("v") == "yes"


def _gate_pass_lines(gate_span: str) -> list[str]:
    """Raw '**Pass N (before re-score):** ...' lines in the Gate span,
    before the first criterion verdict heading."""
    qh = _load_qh()
    m = qh._SELFAUDIT_CRITERION_WIDE_RE.search(gate_span)
    head = gate_span[: m.start()] if m else gate_span
    return [
        ln
        for ln in head.splitlines()
        if ln.strip().startswith("**Pass") and "(before re-score):" in ln
    ]


_GATE_RESULT_LINE_RE = re.compile(
    r"^\*\*Gate result:\*\*[ \t]*(?P<cleared>cleared|not cleared)[ \t]*"
    r"·[ \t]*passes:[ \t]*(?P<passes>\d+)[ \t]*"
    r"·[ \t]*Fix/Repeat fired:[ \t]*(?P<fired>yes|no)[ \t]*$",
    re.MULTILINE,
)


def _gate_result_matches(span: str) -> list[re.Match]:
    return list(_GATE_RESULT_LINE_RE.finditer(span))


_RE_ENTRY_EDGE_ENUM = _SCHEMA_FOR_CONSTANTS["fields"]["re_entry"]["fields"]["edges"][
    "items"
]["fields"]["edge"]["enum"]
_EDGE_SECOND_ORDER, _EDGE_FIX_REPEAT, _EDGE_CRITERION1, _EDGE_MIDRUN = (
    _RE_ENTRY_EDGE_ENUM
)


def _xc_gate_bands(text, sections, block, exemplar) -> list[Finding]:
    """SB-GATE-BANDS: block gate.passes[-1].bands vs the Gate's own final
    verdict blocks, read via `qh._selfaudit_band_census` scoped to the Gate
    span only."""
    gate = block.get("gate")
    if not isinstance(gate, dict):
        return []
    passes = gate.get("passes")
    if not isinstance(passes, list) or not passes:
        return []
    last = passes[-1]
    if not isinstance(last, dict):
        return []
    bands = last.get("bands")
    if not isinstance(bands, list) or len(bands) != 6:
        return []
    span = _gate_span(text)
    if span is None:
        return []
    qh = _load_qh()
    prose_bands, _off = qh._selfaudit_band_census(span)
    findings: list[Finding] = []
    for i in range(6):
        n = i + 1
        prose_band = prose_bands.get(n)
        if prose_band is None:
            findings.append(
                Finding(
                    "SB-GATE-BANDS",
                    f"Criterion {n}: no readable band in the Self-Audit Gate section",
                )
            )
            continue
        if bands[i] != prose_band:
            findings.append(
                Finding(
                    "SB-GATE-BANDS",
                    f"Criterion {n}: block band {bands[i]!r} disagrees with the "
                    f"Gate's own {prose_band!r}",
                )
            )
    return findings


def _xc_gate_passes(text, sections, block, exemplar) -> list[Finding]:
    """SB-GATE-PASSES / SB-NULL: block gate.passes vs the Gate span's own
    Pass lines, in order, plus the exemplar/live null-iff-absent rule for
    `gate` (D-15)."""
    findings: list[Finding] = []
    gate = block.get("gate")
    span = _gate_span(text)
    if exemplar:
        if gate is None:
            if span is not None:
                findings.append(
                    Finding(
                        "SB-NULL",
                        "gate is null but the document carries a Self-Audit Gate section",
                    )
                )
            return findings
        if span is None:
            findings.append(
                Finding(
                    "SB-NULL",
                    "gate is non-null but the document carries no Self-Audit Gate section",
                )
            )
            return findings
    if not isinstance(gate, dict):
        return findings
    if span is None:
        if gate != {"passes": [], "fix_repeat_fired": False, "cleared": False}:
            findings.append(
                Finding(
                    "SB-GATE-PASSES",
                    "the document carries no Self-Audit Gate section but gate is "
                    "not {passes: [], fix_repeat_fired: false, cleared: false}",
                )
            )
        return findings
    passes = gate.get("passes")
    if not isinstance(passes, list):
        return findings
    raw_lines = _gate_pass_lines(span)
    parsed: list[tuple[int, list[str], bool, bool]] = []
    for raw in raw_lines:
        p = _parse_pass_line(raw)
        if p is None:
            findings.append(
                Finding("SB-GATE-PASSES", f"could not parse Pass line: {raw!r}")
            )
            continue
        parsed.append(p)
    nums = [p[0] for p in parsed]
    if nums != list(range(1, len(nums) + 1)):
        findings.append(
            Finding(
                "SB-GATE-PASSES",
                f"Pass line numbers {nums!r} are not consecutive starting at 1",
            )
        )
    for num, bands, gate_cleared, cap_cleared in parsed:
        expected_cleared = "Absent" not in bands
        expected_cap = bands.count("Hand-wavy") <= 1
        if gate_cleared != expected_cleared:
            findings.append(
                Finding(
                    "SB-GATE-PASSES",
                    f"Pass {num}: Gate cleared: {'yes' if gate_cleared else 'no'} "
                    f"disagrees with its own bands",
                )
            )
        if cap_cleared != expected_cap:
            findings.append(
                Finding(
                    "SB-GATE-PASSES",
                    f"Pass {num}: Hand-wavy cap cleared: "
                    f"{'yes' if cap_cleared else 'no'} disagrees with its own bands",
                )
            )
    k = len(parsed)
    if len(passes) != k + 1:
        findings.append(
            Finding(
                "SB-GATE-PASSES",
                f"block has {len(passes)} pass(es) but the Gate section shows "
                f"{k} Pass line(s) plus the final verdict blocks (expected {k + 1})",
            )
        )
    result_matches = _gate_result_matches(span)
    if len(result_matches) == 1:
        stated_n = int(result_matches[0].group("passes"))
        if len(passes) != stated_n:
            findings.append(
                Finding(
                    "SB-GATE-PASSES",
                    f"block has {len(passes)} pass(es) but the Gate result line "
                    f"states passes: {stated_n}",
                )
            )
    for i in range(min(k, max(len(passes) - 1, 0))):
        num, bands, gate_cleared, cap_cleared = parsed[i]
        bp = passes[i]
        if not isinstance(bp, dict):
            continue
        if bp.get("bands") != bands:
            findings.append(
                Finding(
                    "SB-GATE-PASSES",
                    f"block passes[{i}].bands {bp.get('bands')!r} disagree with "
                    f"Pass {num}'s own bands {bands!r}",
                )
            )
        if bp.get("gate_cleared") != gate_cleared:
            findings.append(
                Finding(
                    "SB-GATE-PASSES",
                    f"block passes[{i}].gate_cleared disagrees with Pass {num}'s own line",
                )
            )
        if bp.get("hand_wavy_cap_cleared") != cap_cleared:
            findings.append(
                Finding(
                    "SB-GATE-PASSES",
                    f"block passes[{i}].hand_wavy_cap_cleared disagrees with "
                    f"Pass {num}'s own line",
                )
            )
    return findings


def _xc_gate_result(text, sections, block, exemplar) -> list[Finding]:
    """SB-GATE-RESULT: exactly one well-formed '**Gate result:**' line;
    block cleared/fix_repeat_fired vs its own values; the prose-internal
    inconsistency `Fix/Repeat fired: yes` with `passes: 1`."""
    gate = block.get("gate")
    if not isinstance(gate, dict):
        return []
    span = _gate_span(text)
    if span is None:
        return []
    candidate_lines = [
        ln for ln in span.splitlines() if ln.strip().startswith("**Gate result:**")
    ]
    matches = _gate_result_matches(span)
    if len(candidate_lines) != 1 or len(matches) != 1:
        quote = candidate_lines[0] if candidate_lines else "(none found)"
        return [
            Finding(
                "SB-GATE-RESULT",
                f"expected exactly one well-formed Gate result line, found "
                f"{len(candidate_lines)} candidate line(s) (e.g. {quote!r})",
            )
        ]
    gm = matches[0]
    findings: list[Finding] = []
    expected_cleared = gm.group("cleared") == "cleared"
    if gate.get("cleared") != expected_cleared:
        findings.append(
            Finding(
                "SB-GATE-RESULT",
                f"block gate.cleared {gate.get('cleared')!r} disagrees with the "
                f"Gate result line ({gm.group('cleared')!r})",
            )
        )
    expected_fired = gm.group("fired") == "yes"
    if gate.get("fix_repeat_fired") != expected_fired:
        findings.append(
            Finding(
                "SB-GATE-RESULT",
                f"block gate.fix_repeat_fired {gate.get('fix_repeat_fired')!r} "
                f"disagrees with the Gate result line (Fix/Repeat fired: "
                f"{gm.group('fired')!r})",
            )
        )
    if expected_fired and gm.group("passes") == "1":
        findings.append(
            Finding(
                "SB-GATE-RESULT",
                "the Gate result line states Fix/Repeat fired: yes with "
                "passes: 1, which is internally inconsistent",
            )
        )
    return findings


def _xc_gate_cleared(text, sections, block, exemplar) -> list[Finding]:
    """SB-GATE-CLEARED (prose-side): the Gate result line says cleared while
    the Gate's own final bands fail the rubric rule (an Absent band, or two
    or more Hand-wavy bands) -- alongside Plan 01's block-internal INV-05
    rule."""
    span = _gate_span(text)
    if span is None:
        return []
    matches = _gate_result_matches(span)
    if len(matches) != 1:
        return []
    qh = _load_qh()
    bands, _off = qh._selfaudit_band_census(span)
    if len(bands) != 6:
        return []
    band_values = [bands[n] for n in range(1, 7)]
    fails_rubric = ("Absent" in band_values) or (band_values.count("Hand-wavy") >= 2)
    if matches[0].group("cleared") == "cleared" and fails_rubric:
        return [
            Finding(
                "SB-GATE-CLEARED",
                "the Gate result line says cleared but the Gate's own final "
                "bands fail the rubric rule (an Absent band, or two or more "
                "Hand-wavy bands)",
            )
        ]
    return []


def _xc_reentry(text, sections, block, exemplar) -> list[Finding]:
    """SB-REENTRY / SB-NULL: re_entry vs the Gate span's fixed lines and the
    disclosure region only (R1-R6); nothing outside those two spans is read
    (disclosed bound: reentry-read-from-gate-span-and-disclosure-only)."""
    re_entry = block.get("re_entry")
    gate = block.get("gate")
    span = _gate_span(text)
    disclosure = _disclosure_region(text)
    disclosed_paragraphs = _disclosed_paragraphs(disclosure)
    has_reentry_disclosure = any(
        _ANY_EDGE_NAME_RE.search(p) for p in disclosed_paragraphs
    )
    if exemplar and re_entry is None:
        if span is not None or has_reentry_disclosure:
            return [
                Finding(
                    "SB-NULL",
                    "re_entry is null but the document carries a Self-Audit "
                    "Gate section or a re-entry disclosure",
                )
            ]
        return []
    if not isinstance(re_entry, dict) or not isinstance(gate, dict):
        return []

    fired = re_entry.get("fired")
    edges = re_entry.get("edges")
    edge_names = {e.get("edge") for e in (edges or []) if isinstance(e, dict)}
    passes = gate.get("passes") if isinstance(gate.get("passes"), list) else []
    fix_repeat_fired = gate.get("fix_repeat_fired")
    findings: list[Finding] = []

    # R1 / INV-07
    if fix_repeat_fired is True and not (
        fired is True and _EDGE_FIX_REPEAT in edge_names
    ):
        findings.append(
            Finding(
                "SB-REENTRY",
                "gate.fix_repeat_fired is true but re_entry.fired is not true "
                "with the Fix/Repeat edge listed",
            )
        )

    # R2 / INV-08
    if len(passes) >= 2 and fired is not True:
        findings.append(
            Finding(
                "SB-REENTRY",
                "gate.passes has two or more entries but re_entry.fired is not true",
            )
        )

    # R3
    if span is not None:
        result_matches = _gate_result_matches(span)
        if len(result_matches) == 1:
            result_fired = result_matches[0].group("fired") == "yes"
            has_fix_repeat_edge = _EDGE_FIX_REPEAT in edge_names
            if has_fix_repeat_edge != result_fired:
                findings.append(
                    Finding(
                        "SB-REENTRY",
                        "the Fix/Repeat edge's presence in re_entry.edges "
                        "disagrees with the Gate result line's Fix/Repeat fired value",
                    )
                )

    # R4
    criterion1_absent_in_pass = False
    if span is not None:
        for raw in _gate_pass_lines(span):
            parsed = _parse_pass_line(raw)
            if parsed is not None and parsed[1][0] == "Absent":
                criterion1_absent_in_pass = True
                break
    has_criterion1_edge = _EDGE_CRITERION1 in edge_names
    if has_criterion1_edge != criterion1_absent_in_pass:
        findings.append(
            Finding(
                "SB-REENTRY",
                "the Criterion 1 Absent edge's presence in re_entry.edges "
                "disagrees with whether a Pass line shows Criterion 1 Absent",
            )
        )

    # R5
    if _EDGE_SECOND_ORDER in edge_names and not any(
        _names_second_order(p) for p in disclosed_paragraphs
    ):
        findings.append(
            Finding(
                "SB-REENTRY",
                "re_entry.edges names the second-order return edge but no "
                "**Disclosed:** paragraph at the top of the document names it",
            )
        )
    if _EDGE_MIDRUN in edge_names and not any(
        _names_input_reopen(p) for p in disclosed_paragraphs
    ):
        findings.append(
            Finding(
                "SB-REENTRY",
                "re_entry.edges names the mid-run input re-open edge but no "
                "**Disclosed:** paragraph at the top of the document names it",
            )
        )

    # R6
    if fired is False and has_reentry_disclosure:
        findings.append(
            Finding(
                "SB-REENTRY",
                "re_entry.fired is false but a **Disclosed:** paragraph at the "
                "top of the document names a re-entry edge",
            )
        )

    return findings


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
    ("SB-CONCLUSION-RESTS-ON", _xc_conclusion_rests_on),
    ("SB-GATE-BANDS", _xc_gate_bands),
    ("SB-GATE-PASSES", _xc_gate_passes),
    ("SB-GATE-RESULT", _xc_gate_result),
    ("SB-GATE-CLEARED", _xc_gate_cleared),
    ("SB-REENTRY", _xc_reentry),
    ("SB-PRECHECK-HEAD", _xc_prechecks),
)


# ---------------------------------------------------------------------------
# Top-level entry point
# ---------------------------------------------------------------------------


def check_report(
    text: str, *, exemplar: bool = False, schema: dict | None = None
) -> list[Finding]:
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
        findings.append(
            Finding("SB-JSON", f"summary block body does not parse as JSON: {exc}")
        )
        return findings
    if not isinstance(value, dict):
        findings.append(
            Finding(
                "SB-JSON",
                f"summary block body is not a JSON object (got {type(value).__name__})",
            )
        )
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


def _synthetic_precheck_line(
    ids: list[str], chain_bands: dict[str, str], fallback_band: str
) -> str:
    """A **Pre-check:** line for head `ids`: each Cn with its band from
    `chain_bands` (`fallback_band` when the id is not a chain), every other
    id bare, and the remaining three fields derived by the template's
    formula."""
    rank = {"LOW": 0, "MEDIUM": 1, "HIGH": 2}
    rendered: list[str] = []
    q_marked: list[str] = []
    cited: list[str] = []
    for rid in ids:
        if rid.startswith("C"):
            band = chain_bands.get(rid, fallback_band)
            rendered.append(f"{rid} ({band})")
            cited.append(band)
        else:
            rendered.append(rid)
            if rid.endswith("?"):
                q_marked.append(rid)
    lowest = min(cited, key=lambda b: rank.get(b, 0)) if cited else "none"
    if lowest == "LOW":
        ceiling = "LOW"
    elif q_marked or lowest == "MEDIUM":
        ceiling = "MEDIUM"
    else:
        ceiling = "HIGH"
    q_str = ", ".join(q_marked) if q_marked else "none"
    return (
        f"**Pre-check:** head {', '.join(rendered)} · ?-marked: {q_str} · "
        f"lowest cited: {lowest} · Inputs ceiling: {ceiling}"
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
      disclosed                     -- if given, write a top-of-document
                                       **Disclosed:** paragraph with this text
      omit_gate_section              -- drop the Self-Audit Gate section
                                         regardless of `block['gate']`
      omit_chain_prechecks            -- drop the section 4 **Pre-check:**
                                          line rendered directly above each
                                          chain's **Confidence:** line

    Every rendered pre-check (each section 4 chain's, and section 6's when
    `conclusion.rests_on` is non-null) is built from the ids actually
    rendered on its head, with each Cn's band taken from the block's chains
    and the remaining fields derived by the template's formula.
    """
    omit_block = overrides.get("omit_block", False)
    duplicate_block = overrides.get("duplicate_block", False)
    raw_block_body = overrides.get("raw_block_body")
    trailing_after_block = overrides.get("trailing_after_block", "")
    omit_heading = overrides.get("omit_heading", False)
    heading_before_appendix = overrides.get("heading_before_appendix", False)
    type_cells: dict = overrides.get("type_cells") or {}
    mode_statement = overrides.get("mode_statement")
    disclosed = overrides.get("disclosed")
    omit_gate_section = overrides.get("omit_gate_section", False)
    omit_chain_prechecks = overrides.get("omit_chain_prechecks", False)

    body_json = (
        raw_block_body if raw_block_body is not None else json.dumps(block, indent=2)
    )
    block_fence = f"```{BLOCK_FENCE}\n{body_json}\n```"

    assumptions = block.get("assumptions") or []
    ground_truths = block.get("ground_truths") or []
    chains = block.get("chains") or []
    dead_ends = block.get("dead_ends") or []
    techniques = block.get("techniques") or {"applied": [], "not_applied": []}
    gate = block.get("gate") or {
        "passes": [],
        "cleared": False,
        "fix_repeat_fired": False,
    }
    conclusion = block.get("conclusion") or {}

    lines: list[str] = []
    if mode_statement is not None:
        lines.append(f"Step 0 set `MODE = {mode_statement}`.")
        lines.append("")
    if disclosed is not None:
        lines.append(f"**Disclosed:** {disclosed}")
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
    chain_bands = {c["id"]: c["confidence"] for c in chains}
    for c in chains:
        lines.append(f"### Conclusion {c['id']}: synthetic conclusion")
        head_ids = list(c.get("rests_on") or []) or ["GT-1"]
        head = " + ".join(head_ids)
        lines.append(
            f"{head} → synthetic intermediate reasoning → synthetic conclusion."
        )
        if not omit_chain_prechecks:
            lines.append(_synthetic_precheck_line(head_ids, chain_bands, "MEDIUM"))
        lines.append(
            f"**Confidence:** {c['confidence']} — synthetic confidence rationale."
        )
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
    rests_on = conclusion.get("rests_on")
    if rests_on is not None:
        lines.append(
            _synthetic_precheck_line(
                rests_on, chain_bands, conclusion.get("confidence", "MEDIUM")
            )
        )
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
    # The Gate section's presence tracks the RAW block['gate'] value, not the
    # nullable-safe fallback above: a null gate must render no Gate section
    # at all (the schema's null_when condition), never a section built from
    # the empty-gate default.
    if block.get("gate") is not None and not omit_gate_section:
        passes = gate.get("passes") or []
        gate_lines.append("## Self-Audit Gate (process output)")
        for i, p in enumerate(passes[:-1], start=1):
            bands = p.get("bands") or []
            pieces = " · ".join(
                f"Criterion {n} {b}" for n, b in enumerate(bands, start=1)
            )
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
            gate_lines.append(
                "Justification: synthetic justification tying the span to the band."
            )
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
            summary_heading_lines
            + block_lines
            + [""]
            + appendix_heading_lines
            + techniques_lines
            + gate_lines
        )
    else:
        appendix_section = (
            appendix_heading_lines
            + techniques_lines
            + gate_lines
            + summary_heading_lines
            + block_lines
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
        schema["example"],
        raw_block_body='{"schema_version": 1, "run_mode": "full-composer",}',
    )
    findings = check_report(trailing_comma, schema=schema)
    codes = {f.code for f in findings}
    if codes != {"SB-JSON"}:
        return f"trailing comma: expected {{'SB-JSON'}}, got {codes!r} ({findings!r})"
    array_body = _synthetic_report(
        schema["example"], raw_block_body='["schema_version", 1]'
    )
    findings2 = check_report(array_body, schema=schema)
    codes2 = {f.code for f in findings2}
    if codes2 != {"SB-JSON"}:
        return f"array body: expected {{'SB-JSON'}}, got {codes2!r} ({findings2!r})"
    return None


def _c05_placement_defects_are_rejected() -> str | None:
    schema = load_schema(DEFAULT_SCHEMA)
    example = schema["example"]

    trailing = _synthetic_report(
        example, trailing_after_block="Some trailing prose after the block."
    )
    findings = check_report(trailing, schema=schema)
    codes = {f.code for f in findings}
    if codes != {"SB-PLACEMENT"}:
        return (
            f"trailing prose: expected {{'SB-PLACEMENT'}}, got {codes!r} ({findings!r})"
        )

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
            return (
                f"expected a message naming {expected_path_substr!r}, got {findings!r}"
            )
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
    """Plan 01's block-internal invariants (INV-04/INV-09) stay enforced
    once Plan 02's prose cross-checks are active. Both fixtures below build
    the report's prose FROM the same mutated block (no decoupling), so the
    mutation is visible to the Gate-span/re-entry readers too -- Plan 02's
    SB-GATE-PASSES and SB-REENTRY legitimately co-fire alongside Plan 01's
    SB-INVARIANT on these same fixtures; this is added detection, not a
    weakened one."""
    schema = load_schema(DEFAULT_SCHEMA)

    m = copy.deepcopy(schema["example"])
    m["gate"]["passes"][0]["bands"] = [
        "Sound",
        "Hand-wavy",
        "Sound",
        "Hand-wavy",
        "Sound",
        "Sound",
    ]
    m["gate"]["passes"][0]["hand_wavy_cap_cleared"] = True
    text = _synthetic_report(m)
    findings = check_report(text, schema=schema)
    codes = {f.code for f in findings}
    if codes != {"SB-INVARIANT", "SB-GATE-PASSES"}:
        return (
            "two hand-wavy, cap true: expected {'SB-INVARIANT', "
            f"'SB-GATE-PASSES'}}, got {codes!r} ({findings!r})"
        )

    m2 = copy.deepcopy(schema["example"])
    m2["re_entry"]["fired"] = False
    text2 = _synthetic_report(m2)
    findings2 = check_report(text2, schema=schema)
    codes2 = {f.code for f in findings2}
    if codes2 != {"SB-INVARIANT", "SB-REENTRY"}:
        return (
            "fired false, edges non-empty: expected {'SB-INVARIANT', "
            f"'SB-REENTRY'}}, got {codes2!r} ({findings2!r})"
        )
    return None


def _c09_gate_cleared_follows_last_pass() -> str | None:
    schema = load_schema(DEFAULT_SCHEMA)

    m = copy.deepcopy(schema["example"])
    m["gate"]["passes"][-1]["bands"] = [
        "Sound",
        "Hand-wavy",
        "Sound",
        "Hand-wavy",
        "Sound",
        "Sound",
    ]
    m["gate"]["passes"][-1]["hand_wavy_cap_cleared"] = False
    m["gate"]["passes"][-1]["gate_cleared"] = True
    m["gate"]["cleared"] = True
    text = _synthetic_report(m)
    findings = check_report(text, schema=schema)
    codes = {f.code for f in findings}
    if codes != {"SB-GATE-CLEARED"}:
        return f"two hand-wavy, cleared true: expected {{'SB-GATE-CLEARED'}}, got {codes!r} ({findings!r})"

    m2 = copy.deepcopy(schema["example"])
    m2["gate"]["passes"][-1]["bands"] = [
        "Sound",
        "Hand-wavy",
        "Sound",
        "Sound",
        "Sound",
        "Sound",
    ]
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

    mutants = {case[0]: case[1] for case in _c27_mutants()}
    for case in ("a wrong head id", "i wrong separator"):
        for f in check_report(mutants[case], schema=schema):
            observed.add(f.code)

    unknown = observed - set(FINDING_CODES)
    if unknown:
        return f"observed codes outside FINDING_CODES: {sorted(unknown)!r}"
    if not any(code.startswith("SB-PRECHECK-") for code in observed):
        return "no SB-PRECHECK- code observed across fixtures"
    if not observed:
        return (
            "no codes observed across fixtures -- controls are not exercising findings"
        )
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
    cases.append(
        ("recommendation with one word changed", m, {"SB-CONCLUSION-TEXT"}, True)
    )

    m = copy.deepcopy(example)
    m["conclusion"]["rests_on"] = m["conclusion"]["rests_on"][1:]
    cases.append(
        ("conclusion rests_on drops an id", m, {"SB-CONCLUSION-RESTS-ON"}, True)
    )

    m = copy.deepcopy(example)
    m["conclusion"]["rests_on"] = m["conclusion"]["rests_on"] + ["C99"]
    cases.append(
        ("conclusion rests_on adds an uncited id", m, {"SB-CONCLUSION-RESTS-ON"}, True)
    )

    m = copy.deepcopy(example)
    m["conclusion"]["rests_on"] = ["GT-x"]
    cases.append(("conclusion rests_on malformed item", m, {"SB-SCHEMA"}, True))

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
        ("physical law", "physical law \u2014 derived"),
        ("untested belief", "**untested belief \u2014 economic-hinge**"),
        ("convention", "convention (design-practice (codified))"),
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

    m = copy.deepcopy(example)
    m["assumptions"][0]["type"] = "convention"
    text = _synthetic_report(
        m, type_cells={"A-1": "convention / untested belief \u2014 economic-hinge"}
    )
    codes = {f.code for f in check_report(text, schema=schema)}
    if codes != {"SB-ASSUMPTION"}:
        return f"compound cell with an em-dash subtype: expected {{'SB-ASSUMPTION'}}, got {codes!r}"

    m = copy.deepcopy(example)
    m["assumptions"][0]["type"] = "convention"
    text = _synthetic_report(
        m,
        type_cells={
            "A-1": "convention \u2014 context-dependent technical / untested belief"
        },
    )
    codes = {f.code for f in check_report(text, schema=schema)}
    if codes != {"SB-ASSUMPTION"}:
        return f"compound cell, em-dash subtype first: expected {{'SB-ASSUMPTION'}}, got {codes!r}"

    m = copy.deepcopy(example)
    m["assumptions"][0]["type"] = "untested belief"
    text = _synthetic_report(
        m, type_cells={"A-1": "untested belief (x) / convention (y (z))"}
    )
    codes = {f.code for f in check_report(text, schema=schema)}
    if codes != {"SB-ASSUMPTION"}:
        return f"compound cell with a nested trailing paren: expected {{'SB-ASSUMPTION'}}, got {codes!r}"
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
        return (
            f"techniques null, block present: expected {{'SB-NULL'}}, got {findings2!r}"
        )

    m3 = copy.deepcopy(example)
    m3["run_mode"] = None
    text3 = _synthetic_report(m3)
    findings3 = check_report(text3, exemplar=True, schema=schema)
    if any(f.code == "SB-NULL" for f in findings3):
        return f"run_mode null, no MODE line: unexpected SB-NULL, got {findings3!r}"
    return None


def _c17_two_pass_synthetic_is_clean_with_gate_checks() -> str | None:
    schema = load_schema(DEFAULT_SCHEMA)
    text = _synthetic_report(schema["example"])
    findings = check_report(text, schema=schema)
    if findings:
        return f"expected [], got {findings!r}"
    return None


def _c18_gate_bands_mismatch_or_unreadable() -> str | None:
    schema = load_schema(DEFAULT_SCHEMA)
    example = schema["example"]

    m = copy.deepcopy(example)
    m["gate"]["passes"][-1]["bands"][2] = "Rigorous"
    text = _synthetic_report(example, raw_block_body=json.dumps(m))
    codes = {f.code for f in check_report(text, schema=schema)}
    if codes != {"SB-GATE-BANDS"}:
        return f"Criterion 3 band changed: expected {{'SB-GATE-BANDS'}}, got {codes!r}"

    text2 = _synthetic_report(example)
    text2 = text2.replace(
        "**Criterion 3: Establish Ground Truths**",
        "Criterion 3: Establish Ground Truths",
        1,
    )
    findings2 = check_report(text2, schema=schema)
    if not any(
        f.code == "SB-GATE-BANDS" and "Criterion 3" in f.message for f in findings2
    ):
        return (
            "unreadable Criterion 3 verdict block: expected an SB-GATE-BANDS "
            f"finding naming Criterion 3, got {findings2!r}"
        )
    return None


def _c19_gate_passes_mismatches() -> str | None:
    schema = load_schema(DEFAULT_SCHEMA)
    example = schema["example"]

    m = copy.deepcopy(example)
    m["gate"]["passes"] = [copy.deepcopy(m["gate"]["passes"][-1])]
    text = _synthetic_report(example, raw_block_body=json.dumps(m))
    codes = {f.code for f in check_report(text, schema=schema)}
    if codes != {"SB-GATE-PASSES"}:
        return f"passes shortened to final only: expected {{'SB-GATE-PASSES'}}, got {codes!r}"

    m2 = copy.deepcopy(example)
    m2["gate"]["passes"][0]["bands"][0] = "Rigorous"
    text2 = _synthetic_report(example, raw_block_body=json.dumps(m2))
    codes2 = {f.code for f in check_report(text2, schema=schema)}
    if codes2 != {"SB-GATE-PASSES"}:
        return f"pass 1 band changed: expected {{'SB-GATE-PASSES'}}, got {codes2!r}"

    text3 = _synthetic_report(example)
    text3 = text3.replace("Criterion 6 Sound · ", "", 1)
    codes3 = {f.code for f in check_report(text3, schema=schema)}
    if codes3 != {"SB-GATE-PASSES"}:
        return (
            "malformed Pass line (missing Criterion 6): expected "
            f"{{'SB-GATE-PASSES'}}, got {codes3!r}"
        )
    return None


def _c20_gate_result_mismatches() -> str | None:
    schema = load_schema(DEFAULT_SCHEMA)
    example = schema["example"]

    text = _synthetic_report(example)
    text = re.sub(r"\n\*\*Gate result:\*\*[^\n]*\n", "\n", text, count=1)
    codes = {f.code for f in check_report(text, schema=schema)}
    if codes != {"SB-GATE-RESULT"}:
        return f"Gate result line removed: expected {{'SB-GATE-RESULT'}}, got {codes!r}"

    m = copy.deepcopy(example)
    m["gate"]["fix_repeat_fired"] = False
    text2 = _synthetic_report(example, raw_block_body=json.dumps(m))
    codes2 = {f.code for f in check_report(text2, schema=schema)}
    if "SB-GATE-RESULT" not in codes2:
        return (
            "fix_repeat_fired false vs prose yes: expected SB-GATE-RESULT in "
            f"codes, got {codes2!r}"
        )

    m2 = copy.deepcopy(example)
    m2["gate"]["cleared"] = False
    text3 = _synthetic_report(example, raw_block_body=json.dumps(m2))
    codes3 = {f.code for f in check_report(text3, schema=schema)}
    if not {"SB-GATE-RESULT", "SB-GATE-CLEARED"} <= codes3:
        return (
            "cleared false with prose cleared and passing bands: expected "
            f"SB-GATE-RESULT and SB-GATE-CLEARED in codes, got {codes3!r}"
        )

    prose_block = copy.deepcopy(example)
    two_hand_wavy = ["Sound", "Hand-wavy", "Sound", "Hand-wavy", "Sound", "Sound"]
    prose_block["gate"]["passes"][-1]["bands"] = two_hand_wavy
    prose_block["gate"]["passes"][-1]["gate_cleared"] = True
    prose_block["gate"]["passes"][-1]["hand_wavy_cap_cleared"] = False
    prose_block["gate"]["cleared"] = True

    embedded_block = copy.deepcopy(prose_block)
    embedded_block["gate"]["cleared"] = False

    text4 = _synthetic_report(prose_block, raw_block_body=json.dumps(embedded_block))
    codes4 = {f.code for f in check_report(text4, schema=schema)}
    if codes4 != {"SB-GATE-RESULT", "SB-GATE-CLEARED"}:
        return (
            "prose-internal contradiction (prose says cleared over two "
            "Hand-wavy bands, block correctly says not cleared): expected "
            f"{{'SB-GATE-RESULT', 'SB-GATE-CLEARED'}}, got {codes4!r}"
        )
    return None


def _c21_reentry_fix_repeat_mismatches() -> str | None:
    schema = load_schema(DEFAULT_SCHEMA)
    example = schema["example"]

    m = copy.deepcopy(example)
    m["re_entry"] = {"fired": False, "edges": []}
    text = _synthetic_report(example, raw_block_body=json.dumps(m))
    codes = {f.code for f in check_report(text, schema=schema)}
    if codes != {"SB-REENTRY"}:
        return f"fix_repeat_fired true, re_entry false/[]: expected {{'SB-REENTRY'}}, got {codes!r}"

    m2 = copy.deepcopy(example)
    m2["re_entry"] = {
        "fired": True,
        "edges": [{"edge": _EDGE_SECOND_ORDER, "trigger": "synthetic trigger"}],
    }
    text2 = _synthetic_report(example, raw_block_body=json.dumps(m2))
    codes2 = {f.code for f in check_report(text2, schema=schema)}
    if codes2 != {"SB-REENTRY"}:
        return (
            "edges = [second-order] only while prose says Fix/Repeat fired: "
            f"yes: expected {{'SB-REENTRY'}}, got {codes2!r}"
        )
    return None


def _one_pass_block(example: dict) -> dict:
    m = copy.deepcopy(example)
    m["gate"] = {
        "passes": [
            {
                "bands": ["Sound", "Sound", "Sound", "Sound", "Sound", "Sound"],
                "gate_cleared": True,
                "hand_wavy_cap_cleared": True,
            }
        ],
        "fix_repeat_fired": False,
        "cleared": True,
    }
    m["re_entry"] = {"fired": False, "edges": []}
    return m


def _c22_single_pass_reentry() -> str | None:
    schema = load_schema(DEFAULT_SCHEMA)
    example = schema["example"]
    base = _one_pass_block(example)

    text = _synthetic_report(base)
    findings = check_report(text, schema=schema)
    if findings:
        return f"clean single-pass variant: expected [], got {findings!r}"

    m = copy.deepcopy(base)
    m["re_entry"] = {
        "fired": True,
        "edges": [{"edge": _EDGE_SECOND_ORDER, "trigger": "synthetic trigger"}],
    }
    text2 = _synthetic_report(m)
    codes2 = {f.code for f in check_report(text2, schema=schema)}
    if codes2 != {"SB-REENTRY"}:
        return f"second-order edge, no disclosure: expected {{'SB-REENTRY'}}, got {codes2!r}"

    text3 = _synthetic_report(
        m,
        disclosed=(
            "The second-order pass's return to Phase 2 fired once, "
            "re-challenging Ground Truth GT-2."
        ),
    )
    findings3 = check_report(text3, schema=schema)
    if findings3:
        return f"second-order edge with a matching disclosure: expected [], got {findings3!r}"
    return None


def _c23_reentry_decoys_outside_scope_are_invisible() -> str | None:
    schema = load_schema(DEFAULT_SCHEMA)
    example = schema["example"]
    base = _one_pass_block(example)
    text = _synthetic_report(base)
    text = text.replace(
        "## 4. Derivation Chains\n",
        "## 4. Derivation Chains\n\nThere was therefore no Phase 2 re-entry.\n",
        1,
    )
    text = text.replace(
        "## 5. Abandoned Reasoning\n",
        "## 5. Abandoned Reasoning\n\n**Disclosed:** The Fix/Repeat loop fired.\n",
        1,
    )
    findings = check_report(text, schema=schema)
    if findings:
        return (
            "decoys outside the Gate span/disclosure region: expected [], "
            f"got {findings!r}"
        )
    return None


def _c24_exemplar_gate_reentry_null_iff_absent() -> str | None:
    schema = load_schema(DEFAULT_SCHEMA)
    example = schema["example"]

    m = copy.deepcopy(example)
    m["gate"] = None
    m["re_entry"] = None
    text = _synthetic_report(m, omit_gate_section=True)
    findings = check_report(text, exemplar=True, schema=schema)
    if findings:
        return f"gate/re_entry null, Gate section absent: expected [], got {findings!r}"

    null_gate = copy.deepcopy(example)
    null_gate["gate"] = None
    text2 = _synthetic_report(example, raw_block_body=json.dumps(null_gate))
    findings2 = check_report(text2, exemplar=True, schema=schema)
    if {f.code for f in findings2} != {"SB-NULL"}:
        return f"gate null, Gate section present: expected {{'SB-NULL'}}, got {findings2!r}"
    return None


def _c25_conclusion_rests_on_null_and_absence() -> str | None:
    schema = load_schema(DEFAULT_SCHEMA)
    example = schema["example"]

    # restored leg: the unmutated example is clean in both modes.
    text = _synthetic_report(example)
    findings_live = check_report(text, exemplar=False, schema=schema)
    if findings_live:
        return f"unmutated example, live mode: expected [], got {findings_live!r}"
    findings_exemplar = check_report(text, exemplar=True, schema=schema)
    if findings_exemplar:
        return (
            f"unmutated example, exemplar mode: expected [], got {findings_exemplar!r}"
        )

    # reversed order: section 6's order is now compared, by SB-PRECHECK-HEAD
    # alone (SB-CONCLUSION-RESTS-ON still compares sets, so it stays silent).
    # The rests_on-order-not-compared bound still holds for chains[].rests_on.
    reversed_rests_on = copy.deepcopy(example)
    reversed_rests_on["conclusion"]["rests_on"] = list(
        reversed(reversed_rests_on["conclusion"]["rests_on"])
    )
    text_rev = _synthetic_report(example, raw_block_body=json.dumps(reversed_rests_on))
    codes_rev = {f.code for f in check_report(text_rev, schema=schema)}
    if codes_rev != {"SB-PRECHECK-HEAD"}:
        return (
            f"reversed rests_on order: expected {{'SB-PRECHECK-HEAD'}}, "
            f"got {codes_rev!r}"
        )

    # null-iff-absent, case 1: rests_on null, no Pre-check line rendered --
    # clean in exemplar mode.
    null_version = copy.deepcopy(example)
    null_version["conclusion"]["rests_on"] = None
    text_null = _synthetic_report(null_version)
    findings_null = check_report(text_null, exemplar=True, schema=schema)
    if any(f.code == "SB-NULL" for f in findings_null):
        return (
            f"rests_on null, no Pre-check line: unexpected SB-NULL, "
            f"got {findings_null!r}"
        )

    # null-iff-absent, case 2: rests_on null, but section 6 DOES carry a
    # Pre-check line (built from the DIFFERENT, non-null block) -- SB-NULL fires.
    text_null_present = _synthetic_report(
        example, raw_block_body=json.dumps(null_version)
    )
    findings_null_present = check_report(
        text_null_present, exemplar=True, schema=schema
    )
    if {f.code for f in findings_null_present} != {"SB-NULL"}:
        return (
            f"rests_on null, Pre-check line present: expected {{'SB-NULL'}}, "
            f"got {findings_null_present!r}"
        )

    # non-null without a Pre-check line (both modes) -- the reverse pairing:
    # text built from the null copy (no Pre-check line rendered), block body
    # carrying the example's non-null rests_on.
    text_nonnull_absent = _synthetic_report(
        null_version, raw_block_body=json.dumps(example)
    )
    codes_live = {
        f.code for f in check_report(text_nonnull_absent, exemplar=False, schema=schema)
    }
    if codes_live != {"SB-CONCLUSION-RESTS-ON"}:
        return (
            f"rests_on non-null, no Pre-check line, live mode: expected "
            f"{{'SB-CONCLUSION-RESTS-ON'}}, got {codes_live!r}"
        )
    codes_exemplar = {
        f.code for f in check_report(text_nonnull_absent, exemplar=True, schema=schema)
    }
    if codes_exemplar != {"SB-CONCLUSION-RESTS-ON", "SB-PRECHECK-MISSING"}:
        return (
            f"rests_on non-null, no Pre-check line, exemplar mode: expected "
            f"{{'SB-CONCLUSION-RESTS-ON', 'SB-PRECHECK-MISSING'}}, "
            f"got {codes_exemplar!r}"
        )

    # Section 6's Pre-check line present but with no readable `head ` field.
    # Section 6's is the LAST pre-check in the text (each section 4 chain
    # carries its own above it), so the replacement targets the last one.
    marker = "**Pre-check:** head "
    cut = text.rfind(marker)
    text_unreadable = text[:cut] + "**Pre-check:** " + text[cut + len(marker) :]
    codes_unreadable = {f.code for f in check_report(text_unreadable, schema=schema)}
    if codes_unreadable != {"SB-CONCLUSION-RESTS-ON", "SB-PRECHECK-SHAPE"}:
        return (
            f"unreadable Pre-check head field: expected "
            f"{{'SB-CONCLUSION-RESTS-ON', 'SB-PRECHECK-SHAPE'}}, "
            f"got {codes_unreadable!r}"
        )

    # fenced decoy (80-REVIEW AP-01): a Pre-check line inside a fenced block
    # is illustration, not the Conclusion's own line -- the real one wins.
    decoy = (
        "```\n**Pre-check:** head C9 (LOW) · ?-marked: none · lowest cited: LOW"
        " · Inputs ceiling: LOW\n```\n\n"
        "**Pre-check:** head C1 (HIGH), GT-2? · ?-marked: GT-2? · lowest cited: HIGH"
        " · Inputs ceiling: MEDIUM\n"
    )
    got = _section6_precheck_head_ids(decoy)
    if got != ["C1", "GT-2?"]:
        return f"fenced decoy Pre-check line: expected ['C1', 'GT-2?'], got {got!r}"
    fenced_only = "```\n**Pre-check:** head C9 (LOW) · ?-marked: none · lowest cited: LOW · Inputs ceiling: LOW\n```\n"
    if _section6_precheck_head_ids(fenced_only) is not None:
        return (
            "a section 6 whose only Pre-check line is fenced must read as absent (None)"
        )
    return None


# ---------------------------------------------------------------------------
# Real-report fixtures (CHECK-03 P1-P4, X1)
# ---------------------------------------------------------------------------

FIXTURE_DIR = REPO_ROOT / "tests" / "summary-block-v9.16"
FIXTURES: tuple[str, ...] = (
    "personal-general.md",
    "software-systems.md",
    "science-engineering.md",
    "tb-01.md",
)


def _fixture(name: str) -> str:
    return (FIXTURE_DIR / name).read_text()


# Pasted from falsifier f5's output (`75-falsifiers.sh f5`, an independent
# awk/grep inventory over each fixture's own section headings and Pass
# lines -- shares no code with this checker or with the transcription
# scripts that built the fixtures' blocks): per fixture, (assumption rows,
# ground-truth declarations, chains, dead ends, earlier Gate passes).
_FIXTURE_INVENTORY: dict[str, tuple[int, int, int, int, int]] = {
    "personal-general.md": (18, 20, 8, 4, 0),
    "software-systems.md": (22, 10, 8, 6, 1),
    "science-engineering.md": (13, 10, 5, 4, 0),
    "tb-01.md": (21, 6, 8, 4, 0),
}


def _fixture_reader_inventory(name: str) -> tuple[int, int, int, int, int]:
    """The same five counts as `_FIXTURE_INVENTORY`, computed by this
    checker's own readers over the fixture's PROSE (never its block)."""
    qh = _load_qh()
    text = _fixture(name)
    sections = qh._slice_sections(text)
    a = len(_table_columns(sections.get(2, ""), ("type", "verdict")))
    g = len(_gt_declarations(sections.get(3, "")))
    doc_ids, _blocks = _doc_chain_index(sections.get(4, ""))
    c = len(doc_ids)
    d = len(_DEAD_END_HEADING_RE.findall(sections.get(5, "")))
    span = _gate_span(text)
    p = len(_gate_pass_lines(span)) if span is not None else 0
    return (a, g, c, d, p)


def _p_positive_fixture(name: str) -> str | None:
    text = _fixture(name)
    findings = check_report(text, exemplar=False)
    if findings:
        return f"{name} live mode: expected [], got {findings!r}"
    findings2 = check_report(text, exemplar=True)
    if findings2:
        return f"{name} exemplar mode: expected [], got {findings2!r}"
    return None


def _p1_personal_general() -> str | None:
    return _p_positive_fixture("personal-general.md")


def _p2_software_systems() -> str | None:
    return _p_positive_fixture("software-systems.md")


def _p3_science_engineering() -> str | None:
    return _p_positive_fixture("science-engineering.md")


def _p4_tb_01() -> str | None:
    return _p_positive_fixture("tb-01.md")


def _block_of(text: str) -> dict:
    """The one summary block's parsed JSON body. Requires exactly one
    block."""
    blocks = find_blocks(text)
    assert len(blocks) == 1, f"expected exactly one block, found {len(blocks)}"
    return json.loads(blocks[0].body)


def _splice_block(text: str, new_block: dict) -> str:
    """Replace the summary block's JSON body with `new_block`, re-serialised
    (`json.dumps(indent=2, ensure_ascii=False)`), leaving everything else in
    `text` -- including the fence lines themselves -- untouched. Requires
    exactly one block."""
    blocks = find_blocks(text)
    assert len(blocks) == 1, f"expected exactly one block, found {len(blocks)}"
    b = blocks[0]
    lines = text.split("\n")
    new_body = json.dumps(new_block, indent=2, ensure_ascii=False)
    return "\n".join(lines[: b.start + 1] + new_body.split("\n") + lines[b.end :])


def _x1_extraction_floor() -> str | None:
    """The checker's readers, run over each fixture's prose, must equal an
    independent hand-transcribed inventory (`_FIXTURE_INVENTORY`, sourced
    from falsifier f5); assumptions/ground_truths/chains must be non-zero
    for every fixture (a floor that cannot pass vacuously on an empty
    report)."""
    for name in FIXTURES:
        actual = _fixture_reader_inventory(name)
        expected = _FIXTURE_INVENTORY[name]
        if actual != expected:
            return (
                f"{name}: reader counts {actual!r} disagree with "
                f"_FIXTURE_INVENTORY {expected!r}"
            )
        a, g, c, _d, _p = actual
        if a == 0 or g == 0 or c == 0:
            return (
                f"{name}: assumptions/ground_truths/chains must be non-zero, "
                f"got {actual!r}"
            )
    return None


# ---------------------------------------------------------------------------
# CHECK-03 must-fail controls (M1-M9), built by mutating a real fixture's
# text or its parsed block in memory -- never writing to the fixture file.
# Each asserts the EXACT finding-code set and a message substring, per
# 75-04-PLAN.md's interfaces table.
# ---------------------------------------------------------------------------


def _assert_codes_and_substring(
    findings: list[Finding], expected_codes: set[str], substring: str, label: str
) -> str | None:
    codes = {f.code for f in findings}
    if codes != expected_codes:
        return f"{label}: expected codes == {expected_codes!r}, got {codes!r} ({findings!r})"
    if not any(substring in f.message for f in findings):
        return f"{label}: expected a message containing {substring!r}, got {findings!r}"
    return None


def _m1_missing_block() -> str | None:
    text = _fixture("personal-general.md")
    blocks = find_blocks(text)
    assert len(blocks) == 1
    b = blocks[0]
    lines = text.split("\n")
    mutated = "\n".join(lines[: b.start] + lines[b.end + 1 :])
    findings = check_report(mutated)
    return _assert_codes_and_substring(
        findings, {"SB-MISSING"}, "no summary block", "M1-missing-block"
    )


def _m2_two_blocks() -> str | None:
    text = _fixture("personal-general.md")
    blocks = find_blocks(text)
    assert len(blocks) == 1
    b = blocks[0]
    lines = text.split("\n")
    block_text = "\n".join(lines[b.start : b.end + 1])
    mutated = "\n".join(lines[: b.end + 1] + ["", block_text] + lines[b.end + 1 :])
    findings = check_report(mutated)
    return _assert_codes_and_substring(findings, {"SB-MULTIPLE"}, "2", "M2-two-blocks")


def _m3_malformed_json() -> str | None:
    text = _fixture("personal-general.md")
    blocks = find_blocks(text)
    assert len(blocks) == 1
    b = blocks[0]
    body = b.body
    stripped = body.rstrip()
    assert stripped.endswith("}")
    new_body = stripped[:-1] + body[len(stripped) :]
    lines = text.split("\n")
    mutated = "\n".join(lines[: b.start + 1] + new_body.split("\n") + lines[b.end :])
    findings = check_report(mutated)
    return _assert_codes_and_substring(
        findings, {"SB-JSON"}, "JSON", "M3-malformed-json"
    )


def _m4_chain_confidence() -> str | None:
    text = _fixture("personal-general.md")
    block = _block_of(text)
    block["chains"][0]["confidence"] = "HIGH"
    mutated = _splice_block(text, block)
    findings = check_report(mutated)
    return _assert_codes_and_substring(
        findings, {"SB-CHAIN-CONFIDENCE"}, "C1", "M4-chain-confidence"
    )


def _m5_reentry_fired_personal_general() -> str | None:
    text = _fixture("personal-general.md")
    if "There was therefore no Phase 2 re-entry." not in text:
        return "decoy line missing from personal-general.md (the control would no longer exercise the PRD's trap)"

    block = _block_of(text)

    case1 = copy.deepcopy(block)
    case1["re_entry"] = {
        "fired": True,
        "edges": [
            {
                "edge": _EDGE_SECOND_ORDER,
                "trigger": "The second-order pass considered a Phase 2 re-entry.",
            }
        ],
    }
    msg1 = _assert_codes_and_substring(
        check_report(_splice_block(text, case1)),
        {"SB-REENTRY"},
        "re_entry",
        "M5-reentry-fired-personal-general (second-order edge)",
    )
    if msg1:
        return msg1

    case2 = copy.deepcopy(block)
    case2["re_entry"] = {
        "fired": True,
        "edges": [
            {
                "edge": _EDGE_FIX_REPEAT,
                "trigger": "The Fix/Repeat loop was considered.",
            }
        ],
    }
    msg2 = _assert_codes_and_substring(
        check_report(_splice_block(text, case2)),
        {"SB-REENTRY"},
        "re_entry",
        "M5-reentry-fired-personal-general (Fix/Repeat edge)",
    )
    if msg2:
        return msg2
    return None


def _m6_reentry_not_fired_software_systems() -> str | None:
    text = _fixture("software-systems.md")
    block = _block_of(text)
    block["re_entry"] = {"fired": False, "edges": []}
    mutated = _splice_block(text, block)
    findings = check_report(mutated)
    return _assert_codes_and_substring(
        findings, {"SB-REENTRY"}, "Fix/Repeat", "M6-reentry-not-fired-software-systems"
    )


def _m7_single_pass_before_fix() -> str | None:
    text = _fixture("software-systems.md")
    block = _block_of(text)
    block["gate"]["passes"] = [block["gate"]["passes"][-1]]
    mutated = _splice_block(text, block)
    findings = check_report(mutated)
    return _assert_codes_and_substring(
        findings, {"SB-GATE-PASSES"}, "passes", "M7-single-pass-before-fix"
    )


def _m8_conclusion_cut() -> str | None:
    text = _fixture("science-engineering.md")
    block = _block_of(text)
    marker = "(chains C3, C4):"
    full = block["conclusion"]["recommendation"]
    idx = full.find(marker)
    assert idx != -1, (
        f"marker {marker!r} not found in science-engineering.md's recommendation"
    )
    block["conclusion"]["recommendation"] = full[: idx + len(marker)]
    mutated = _splice_block(text, block)
    findings = check_report(mutated)
    return _assert_codes_and_substring(
        findings, {"SB-CONCLUSION-CUT"}, "cut short", "M8-conclusion-cut"
    )


_BAND_TOKEN_RE = re.compile(r"Band: \*\*[^*]+\*\*")


def _m9_two_hand_wavy_cleared() -> str | None:
    text = _fixture("personal-general.md")
    block = _block_of(text)
    bands = block["gate"]["passes"][-1]["bands"]
    block["gate"]["passes"][-1]["bands"] = ["Hand-wavy", "Hand-wavy"] + bands[2:]
    block["gate"]["passes"][-1]["hand_wavy_cap_cleared"] = False
    # gate.cleared (top level) is left untouched -- still true, per the plan's
    # instruction -- creating the prose/block Gate-cleared disagreement.
    mutated_block_text = _splice_block(text, block)

    span = _gate_span(mutated_block_text)
    assert span is not None
    count = 0

    def _repl(m: re.Match) -> str:
        nonlocal count
        count += 1
        return "Band: **Hand-wavy**" if count <= 2 else m.group(0)

    new_span = _BAND_TOKEN_RE.sub(_repl, span)
    assert count >= 2, (
        f"expected at least two 'Band: **...**' tokens in the Gate span, found {count}"
    )
    mutated = mutated_block_text.replace(span, new_span, 1)

    findings = check_report(mutated)
    return _assert_codes_and_substring(
        findings, {"SB-GATE-CLEARED"}, "Hand-wavy", "M9-two-hand-wavy-cleared"
    )


# ---------------------------------------------------------------------------
# Pre-check comparator controls (C26-C29, P5, M10, X3)
# ---------------------------------------------------------------------------


def _precheck_codes(findings: list[Finding]) -> set[str]:
    return {f.code for f in findings if f.code.startswith("SB-PRECHECK-")}


def _mutate_precheck_line(text: str, index: int, old: str, new: str) -> str:
    """Replace `old` with `new` inside the `index`-th **Pre-check:** line of
    `text` (Python indexing, so -1 is the last one,
    section 6's), never by a first-match replace over the whole text.
    Raises when `old` is not in that line."""
    lines = text.split("\n")
    positions = [i for i, ln in enumerate(lines) if ln.startswith("**Pre-check:**")]
    pos = positions[index]
    if old not in lines[pos]:
        raise ValueError(f"{old!r} not in pre-check line {lines[pos]!r}")
    lines[pos] = lines[pos].replace(old, new, 1)
    return "\n".join(lines)


_C2_PRECHECK_LITERAL = (
    "**Pre-check:** head GT-2?, C1 (HIGH) · ?-marked: GT-2? · "
    "lowest cited: HIGH · Inputs ceiling: MEDIUM"
)


def _c26_precheck_clean() -> str | None:
    schema = load_schema(DEFAULT_SCHEMA)
    text = _synthetic_report(schema["example"])
    for exemplar in (False, True):
        findings = check_report(text, exemplar=exemplar, schema=schema)
        if findings:
            return f"unmutated synthetic report (exemplar={exemplar}): expected [], got {findings!r}"
    if _C2_PRECHECK_LITERAL not in text.split("\n"):
        return f"C2's pre-check line (a Cn on a section 4 head) is not {_C2_PRECHECK_LITERAL!r}"
    r = precheck_reading(text)
    if (r["compared"], r["confidence_lines"], r["chains"]) != (3, 3, 2):
        return f"precheck_reading: expected compared 3, confidence_lines 3, chains 2, got {r!r}"
    return None


def _c27_mutants() -> list[tuple[str, str, str]]:
    """(case, mutant text, the one SB-PRECHECK code it must fire)."""
    schema = load_schema(DEFAULT_SCHEMA)
    text = _synthetic_report(schema["example"])
    m = _mutate_precheck_line
    conf_marker = "**Confidence:** MEDIUM"
    cut = text.rfind(conf_marker)
    band_text = text[:cut] + "**Confidence:** HIGH" + text[cut + len(conf_marker) :]
    return [
        ("a wrong head id", m(text, 0, "head GT-1 ·", "head GT-9 ·"), "SB-PRECHECK-HEAD"),
        (
            "b wrong head order",
            m(text, 1, "head GT-2?, C1 (HIGH)", "head C1 (HIGH), GT-2?"),
            "SB-PRECHECK-HEAD",
        ),
        ("c wrong ?-marked", m(text, 1, "?-marked: GT-2?", "?-marked: none"), "SB-PRECHECK-QMARK"),
        (
            "d wrong lowest cited",
            m(text, 1, "lowest cited: HIGH", "lowest cited: none"),
            "SB-PRECHECK-LOWEST",
        ),
        (
            "e wrong ceiling",
            m(text, 1, "Inputs ceiling: MEDIUM", "Inputs ceiling: HIGH"),
            "SB-PRECHECK-CEILING",
        ),
        ("f label above ceiling", band_text, "SB-PRECHECK-BAND"),
        (
            "g cited band disagrees with section 4",
            m(text, -1, "C2 (MEDIUM)", "C2 (HIGH)"),
            "SB-PRECHECK-CITED-BAND",
        ),
        (
            "h cited Cn is not a section 4 chain",
            m(text, -1, "C1 (HIGH)", "C7 (HIGH)"),
            "SB-PRECHECK-CITED-BAND",
        ),
        ("i wrong separator", m(text, 0, " · ", " ; "), "SB-PRECHECK-SHAPE"),
    ]


def _c27_precheck_field_mutations() -> str | None:
    schema = load_schema(DEFAULT_SCHEMA)
    mutants = _c27_mutants()
    if mutants[5][1] == _synthetic_report(schema["example"]):
        return "case f did not mutate the section 6 label"
    for case, mutant, code in mutants:
        got = _precheck_codes(check_report(mutant, schema=schema))
        if got != {code}:
            return f"C27 ({case}): expected exactly {{{code!r}}}, got {got!r}"
    return None


def _c28_precheck_decoys() -> str | None:
    got = _chain_head_ids("### Conclusion C1: x\nGT-1 (see GT-9 for the list) + GT-2 → x → y\n")
    if got != ["GT-1", "GT-2"]:
        return f"(a) parenthetical decoy: expected ['GT-1', 'GT-2'], got {got!r}"
    got = _chain_head_ids(
        "### Conclusion C2: x\n"
        "This chain combines GT-3 with the prior result.\n"
        "C1 (MEDIUM) + GT-4 → x → y\n"
    )
    if got != ["C1", "GT-4"]:
        return f"(b) intro-sentence head: expected ['C1', 'GT-4'], got {got!r}"
    got = _chain_head_ids("### Conclusion C1: x\nGT-1 + C2's threshold → x → y\n")
    if got is not None:
        return f"(c) a term with no leading identifier: expected None, got {got!r}"
    schema = load_schema(DEFAULT_SCHEMA)
    text = _synthetic_report(schema["example"])
    old_head = "GT-1 → synthetic intermediate reasoning"
    if text.count(old_head) != 1:
        return f"(c) expected C1's head {old_head!r} exactly once"
    unlocated = text.replace(old_head, "GT-1 + C2's threshold → synthetic intermediate reasoning")
    findings = [
        f for f in check_report(unlocated, schema=schema) if f.code.startswith("SB-PRECHECK-")
    ]
    if {f.code for f in findings} != {"SB-PRECHECK-HEAD"} or not any(
        "head line not located" in f.message for f in findings
    ):
        return f"(c) unlocated head: expected SB-PRECHECK-HEAD 'head line not located', got {findings!r}"
    # The decoy's Confidence word matches C1's real band on purpose: the
    # chain band source, `qh._chain_confidence_label`, searches the whole
    # block without fence awareness (as SB-CHAIN-CONFIDENCE does), so a
    # different word would test that reader, not this one. A fenced C9
    # pre-check that was read would still fire CITED-BAND or count as an
    # orphan.
    decoy = (
        "```\n"
        "**Pre-check:** head C9 (LOW) · ?-marked: none · lowest cited: LOW · Inputs ceiling: LOW\n"
        "**Confidence:** HIGH — fenced illustration.\n"
        "```\n"
    )
    first = "**Pre-check:** head GT-1 ·"
    if text.count(first) != 1:
        return f"(d) expected C1's pre-check {first!r} exactly once"
    fenced = text.replace(first, decoy + first, 1)
    for exemplar in (False, True):
        got_codes = _precheck_codes(check_report(fenced, exemplar=exemplar, schema=schema))
        if got_codes:
            return f"(d) fenced decoy (exemplar={exemplar}): expected no SB-PRECHECK code, got {got_codes!r}"
    r = precheck_reading(fenced)
    if (r["compared"], r["orphans"], r["confidence_lines"]) != (3, 0, 3):
        return f"(d) fenced decoy: expected compared 3, orphans 0, confidence_lines 3, got {r!r}"
    return None


def _c29_precheck_missing() -> str | None:
    schema = load_schema(DEFAULT_SCHEMA)
    example = schema["example"]
    omitted = _synthetic_report(example, omit_chain_prechecks=True)
    full = _synthetic_report(example)
    first = "**Pre-check:** head GT-1 ·"
    pos = full.find(first)
    eol = full.find("\n", pos)
    blank = full[:eol] + "\n" + full[eol:]
    got = [f for f in check_report(omitted, exemplar=True, schema=schema)]
    missing = [f for f in got if f.code == "SB-PRECHECK-MISSING"]
    if not missing or not all(
        any(f.message.startswith(f"{cid}:") for f in missing) for cid in ("C1", "C2")
    ):
        return f"(a) omitted chain pre-checks, exemplar mode: expected SB-PRECHECK-MISSING naming C1 and C2, got {got!r}"
    codes = _precheck_codes(check_report(blank, exemplar=True, schema=schema))
    if codes != {"SB-PRECHECK-MISSING"}:
        return f"(b) blank line between pre-check and Confidence: expected {{'SB-PRECHECK-MISSING'}}, got {codes!r}"
    for label, t in (("omitted", omitted), ("blank-line", blank)):
        codes = {f.code for f in check_report(t, exemplar=False, schema=schema)}
        if "SB-PRECHECK-MISSING" in codes:
            return f"(c) {label}, live mode: SB-PRECHECK-MISSING must never fire live"
    r = precheck_reading(omitted)
    if r["missing"] != 2:
        return f"report-only reading: expected missing 2, got {r!r}"
    return None


def _p5_precheck_real_fixtures() -> str | None:
    for name in FIXTURES:
        text = _fixture(name)
        r = precheck_reading(text)
        if not (r["compared"] == r["confidence_lines"] > 0):
            return f"{name}: expected compared == confidence_lines > 0, got {r!r}"
        if r["field_findings"]:
            return f"{name}: expected 0 field findings, got {r!r}"
        codes = _precheck_codes(check_report(text, exemplar=False))
        if codes:
            return f"{name} live mode: unexpected {codes!r}"
    return None


_M10_BEFORE = "head C1 (MEDIUM), C2 (MEDIUM), C3 (MEDIUM), C4 (MEDIUM), C5 (MEDIUM), GT-9 ·"
_M10_AFTER = "head C2 (MEDIUM), C1 (MEDIUM), C3 (MEDIUM), C4 (MEDIUM), C5 (MEDIUM), GT-9 ·"


def _m10_precheck_real_fixture_mutation() -> str | None:
    """software-systems C6: a Cn-led head after an intro paragraph (the
    999.183 shape). Swapping its first two pre-check head items must fire
    SB-PRECHECK-HEAD alone."""
    text = _fixture("software-systems.md")
    if text.count(_M10_BEFORE) != 1:
        return f"expected C6's pre-check head {_M10_BEFORE!r} exactly once in the fixture"
    mutant = text.replace(_M10_BEFORE, _M10_AFTER)
    got = _precheck_codes(check_report(mutant, exemplar=False))
    if got != {"SB-PRECHECK-HEAD"}:
        return f"expected exactly {{'SB-PRECHECK-HEAD'}}, got {got!r}"
    return None


def _x3_precheck_comparator_stub() -> str | None:
    """Anti-masking: with `_precheck_field_findings` stubbed to return [],
    C27 and M10 must both fail. A stub that leaves either green means the
    controls are not reaching the comparator."""
    global _precheck_field_findings
    original = _precheck_field_findings
    try:
        _precheck_field_findings = lambda *a, **k: []  # noqa: E731
        c27 = _c27_precheck_field_mutations()
        m10 = _m10_precheck_real_fixture_mutation()
    finally:
        _precheck_field_findings = original
    if not c27 or not m10:
        return f"stubbed comparator left a control green (C27 -> {c27!r}, M10 -> {m10!r})"
    return None


# ---------------------------------------------------------------------------
# X4: the shipped worked examples carry a pre-check above every Confidence line
# ---------------------------------------------------------------------------

EXEMPLAR_SURFACES: tuple[Path, ...] = (
    REPO_ROOT / "shared" / "examples",
    REPO_ROOT / "first-principles" / "references" / "examples",
)


def _x4_exemplar_precheck_floor() -> str | None:
    """Every worked example on both surfaces, discovered live: each section 4
    chain and section 6 has a Confidence line with a field-correct pre-check
    directly above it, and the two surfaces agree on the total. The chain
    count is read by `qh._chain_ids`, independently of the Confidence-line
    locator, so a locator that finds nothing cannot pass vacuously."""
    qh = _load_qh()
    totals: list[int] = []
    for surface in EXEMPLAR_SURFACES:
        files = sorted(surface.glob("*.md"))
        if not files:
            return f"{_relpath(surface)}: no worked example discovered"
        total = 0
        for path in files:
            rel = _relpath(path)
            text = path.read_text()
            try:
                sections = qh._slice_sections(text)
            except qh.SectionResolutionError as exc:
                return f"{rel}: sections not resolvable ({exc})"
            chains = len(qh._chain_ids(sections.get(4, "") or ""))
            r = precheck_reading(text)
            if not (r["compared"] == r["confidence_lines"] == chains + 1):
                return (
                    f"{rel}: expected compared == confidence_lines == chains + 1 "
                    f"({chains + 1}), got {r!r}"
                )
            if r["missing"] or r["orphans"] or r["field_findings"]:
                return f"{rel}: expected no missing, orphan or field finding, got {r!r}"
            total += r["compared"]
        totals.append(total)
    if len(set(totals)) != 1:
        return f"surfaces disagree on the pre-check total: {totals!r}"
    return None


# ---------------------------------------------------------------------------
# X2: every registered cross-check must be load-bearing (an ablation)
# ---------------------------------------------------------------------------


def _x2_cross_check_ablation() -> str | None:
    """For each ENTRY (code, fn) in `_CROSS_CHECKS` -- by position, not by
    code -- rebind `_CROSS_CHECKS` to the tuple without that one entry, run
    every C/M/P control (never X1/X2), restore in a `finally`, and require
    at least one control to fail. Any entry whose removal leaves every other
    control green is reported by code as a dead check.

    Ablating by POSITION (not by filtering every entry that shares a code)
    is deliberate: two entries can share a code (e.g. a no-op planted next
    to a real reader under the same code), and removing "by code" would
    silently remove both together, hiding a dead entry behind its
    load-bearing twin. See 75-04-PLAN.md's X2 falsifier."""
    global _CROSS_CHECKS
    original = _CROSS_CHECKS
    exercised = [
        (cid, fn)
        for cid, fn in _CONTROLS
        if cid
        not in (
            "X1-extraction-floor",
            "X2-cross-check-ablation",
            "X3-precheck-comparator-stub",
            "X4-exemplar-precheck-floor",
        )
    ]
    dead: list[str] = []
    try:
        for i, (code, _fn) in enumerate(original):
            _CROSS_CHECKS = original[:i] + original[i + 1 :]
            any_failed = False
            for _cid, fn in exercised:
                try:
                    msg = fn()
                except Exception as exc:  # noqa: BLE001
                    msg = f"{type(exc).__name__}: {exc}"
                if msg:
                    any_failed = True
                    break
            if not any_failed:
                dead.append(code)
    finally:
        _CROSS_CHECKS = original
    if dead:
        return f"removing cross-check(s) {dead!r} left every other control green (dead check)"
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
    ("C17", _c17_two_pass_synthetic_is_clean_with_gate_checks),
    ("C18", _c18_gate_bands_mismatch_or_unreadable),
    ("C19", _c19_gate_passes_mismatches),
    ("C20", _c20_gate_result_mismatches),
    ("C21", _c21_reentry_fix_repeat_mismatches),
    ("C22", _c22_single_pass_reentry),
    ("C23", _c23_reentry_decoys_outside_scope_are_invisible),
    ("C24", _c24_exemplar_gate_reentry_null_iff_absent),
    ("C25", _c25_conclusion_rests_on_null_and_absence),
    ("C26-precheck-clean", _c26_precheck_clean),
    ("C27-precheck-field-mutations", _c27_precheck_field_mutations),
    ("C28-precheck-decoys", _c28_precheck_decoys),
    ("C29-precheck-missing", _c29_precheck_missing),
    ("P1-personal-general", _p1_personal_general),
    ("P2-software-systems", _p2_software_systems),
    ("P3-science-engineering", _p3_science_engineering),
    ("P4-tb-01", _p4_tb_01),
    ("P5-precheck-real-fixtures", _p5_precheck_real_fixtures),
    ("M1-missing-block", _m1_missing_block),
    ("M2-two-blocks", _m2_two_blocks),
    ("M3-malformed-json", _m3_malformed_json),
    ("M4-chain-confidence", _m4_chain_confidence),
    ("M5-reentry-fired-personal-general", _m5_reentry_fired_personal_general),
    ("M6-reentry-not-fired-software-systems", _m6_reentry_not_fired_software_systems),
    ("M7-single-pass-before-fix", _m7_single_pass_before_fix),
    ("M8-conclusion-cut", _m8_conclusion_cut),
    ("M9-two-hand-wavy-cleared", _m9_two_hand_wavy_cleared),
    ("M10-precheck-real-fixture-mutation", _m10_precheck_real_fixture_mutation),
    ("X1-extraction-floor", _x1_extraction_floor),
    ("X2-cross-check-ablation", _x2_cross_check_ablation),
    ("X3-precheck-comparator-stub", _x3_precheck_comparator_stub),
    ("X4-exemplar-precheck-floor", _x4_exemplar_precheck_floor),
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
        "registered_surfaces": [
            _relpath(DEFAULT_SCHEMA),
            _relpath(FIXTURE_DIR),
            *(_relpath(surface) for surface in EXEMPLAR_SURFACES),
        ],
        "checked_files": [_relpath(FIXTURE_DIR / name) for name in FIXTURES],
        "locked_constants": {
            "DEFAULT_SCHEMA": _relpath(DEFAULT_SCHEMA),
            "BLOCK_HEADING": BLOCK_HEADING,
            "SCHEMA_VERSION": schema.get("schema_version"),
        },
        "derived_counts": {
            "finding_codes": len(FINDING_CODES),
            "cross_checks": len(_CROSS_CHECKS),
        },
        "disclosed_bounds_anchors": sorted(
            [
                "rests_on-order-not-compared",
                "not-applied-phase-only-where-stated",
                "techniques-applied-vocabulary-only",
                "run-mode-only-where-stated",
                "recommendation-bold-markers-ignored",
                "reentry-read-from-gate-span-and-disclosure-only",
                "second-order-and-input-reopen-edges-need-a-disclosed-paragraph",
                "precheck-missing-fails-in-exemplar-mode-only",
                "precheck-band-raised-to-ceiling-undetectable",
                "precheck-section6-head-completeness-not-checked",
                "precheck-overlaps-qual01-precheck-defects",
            ]
        ),
    }


_PRECHECK_READING_KEYS = (
    ("chains", "chains"),
    ("confidence-lines", "confidence_lines"),
    ("compared", "compared"),
    ("missing", "missing"),
    ("orphans", "orphans"),
    ("field-findings", "field_findings"),
)


def _print_precheck_reading(reports: list[str]) -> int:
    """`--precheck-reading`: one fixed-format line per REPORT, then a total.
    Report-only: exits 0 whatever it reads, 2 on an unreadable path."""
    totals = dict.fromkeys((k for _label, k in _PRECHECK_READING_KEYS), 0)
    out: list[str] = []
    for report_arg in reports:
        try:
            text = Path(report_arg).read_text()
        except OSError as exc:
            print(f"ERROR: cannot read {report_arg}: {exc}", file=sys.stderr)
            return 2
        r = precheck_reading(text)
        for _label, k in _PRECHECK_READING_KEYS:
            totals[k] += r[k]
        fields = " ".join(f"{label}={r[k]}" for label, k in _PRECHECK_READING_KEYS)
        out.append(f"PRECHECK-READING {report_arg}: {fields}")
    fields = " ".join(f"{label}={totals[k]}" for label, k in _PRECHECK_READING_KEYS)
    out.append(f"PRECHECK-READING total: files={len(reports)} {fields}")
    print("\n".join(out))
    return 0


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("reports", nargs="*", metavar="REPORT")
    ap.add_argument("--exemplar", action="store_true")
    ap.add_argument("--json", action="store_true", dest="as_json")
    ap.add_argument("--schema", type=Path, default=None)
    ap.add_argument("--self-test", action="store_true")
    ap.add_argument("--describe", action="store_true")
    ap.add_argument("--precheck-reading", action="store_true", dest="precheck_reading")
    args = ap.parse_args(argv)

    if args.describe:
        print(json.dumps(describe(), indent=2, sort_keys=True))
        return 0
    if args.self_test:
        return self_test()

    if not args.reports:
        print("ERROR: no REPORT given", file=sys.stderr)
        return 2

    if args.precheck_reading:
        return _print_precheck_reading(args.reports)

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
                    "findings": [
                        {"code": f.code, "message": f.message} for f in findings
                    ],
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
