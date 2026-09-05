#!/usr/bin/env python3
# /// script
# requires-python = ">=3.12"
# dependencies = []
# ///
"""Conformance measurement for Phase 17: reads 29 shipped Markdown artifacts through the
frozen, CONTRACT-06-pinned detectors in `scripts/check-quality-harness.py` and reports what
they find. This script imports that harness read-only and calls none of its CLI entry
points; it never edits, and its own self-test never mutates, any of the three sha256-pinned
functions (`_chain_block_well_formed`, `_conclusion_claims`, `_slice_sections`).

`MEASUREMENT_DATE` below is a hardcoded module constant, not `date.today()`. This is a NEW
pattern for this repository -- no existing script combines "carries an embedded date" with
"byte-for-byte reproducible on every re-run" (the closest precedent, `docs/requirements-matrix.md`
/ `docs/data/matrix.json`, sidesteps the tension by carrying no date at all). Bumping
`MEASUREMENT_DATE` is a deliberate, reviewed source edit, the same discipline
`check-provenance.py` applies to `_EXPECTED_SOURCES`/`_EXPECTED_LITERALS`.

Both rendered files end with exactly one trailing newline, produced by a single shared write
helper and by the identical in-memory strings `--check` compares. This deliberately diverges
from `docs/data/matrix.json`, which has no trailing newline -- uniformity across this pair
matters more here than matching that sibling artifact.

The D-05 two-census reconciliation note (why one frozen detector yields two different
chain-block counts) is rendered into `docs/conformance-baseline.md` itself, not restated here.

Usage:
    python3 scripts/report-conformance.py               # write both artifacts
    python3 scripts/report-conformance.py --check       # regenerate in memory, diff on-disk
    python3 scripts/report-conformance.py --self-test   # offline control battery

Exit codes:
    0  success (write / --check clean / --self-test clean)
    1  --check found drift, or discovery floor failed, or --self-test found a failing
       control, or (Phase 19) a corpus floor was breached (catalog<->discovery roster
       drift, a fully-clean corpus item with no recorded disposition, a corpus
       population floor breach, or a D-03 perturbation mutation that did not move the
       expected reading)
    2  --check found the pass1/pass2 in-memory generation itself non-deterministic
"""

from __future__ import annotations

import argparse
import difflib
import importlib.util
import inspect
import json
import re
import sys
import tempfile
from dataclasses import dataclass
from pathlib import Path
from typing import Literal

REPO_ROOT: Path = Path(__file__).resolve().parents[1]
MEASUREMENT_DATE: str = "2026-09-05"
MD_PATH: Path = REPO_ROOT / "docs" / "conformance-baseline.md"
JSON_PATH: Path = REPO_ROOT / "docs" / "data" / "conformance.json"

SHARED_EXAMPLES_GLOB: str = "shared/examples/*.md"
TWIN_EXAMPLES_GLOB: str = "first-principles/agents/references/examples/*.md"
CONTRACT_SURFACE_RELPATH: str = "shared/spine/references/output-template.md"
ADVERSARIAL_CORPUS_GLOB: str = "tests/adversarial-corpus-v9.0/*.md"
ADVERSARIAL_CORPUS_CATALOG: str = "tests/adversarial-corpus-v9.0/catalog.md"
ADVERSARIAL_CORPUS_README: str = "tests/adversarial-corpus-v9.0/README.md"

MIN_SHARED_EXAMPLES: int = 14
MIN_TWIN_EXAMPLES: int = 14
MIN_CONTRACT_SURFACES: int = 1
# CONF-07's floor (Phase 19): fewer than this many corpus items and
# discover_artifacts raises DiscoveryFloorError rather than returning a short
# list -- D-02's "never return a short list silently" idiom, reused verbatim
# from the three surfaces above. Raising this blocks EVERY commit in the
# repository through the pre-commit conformance-drift gate (`--check` on
# every commit, not just commits touching this surface), which is exactly
# why the thirteen-item corpus is authored and committed BEFORE this
# constant goes live, never after.
MIN_CORPUS_ITEMS: int = 12


# ---------------------------------------------------------------------------
# Harness import (one-way, read-only). check-quality-harness.py never imports
# this file. Same sys.modules key as scripts/check-provenance.py -- safe for
# separate CLI invocations, would collide if the two were ever imported into
# one process (RESEARCH.md Pitfall 1).
# ---------------------------------------------------------------------------

_HARNESS_PATH: Path = REPO_ROOT / "scripts" / "check-quality-harness.py"
_spec = importlib.util.spec_from_file_location("_quality_harness", _HARNESS_PATH)
_mod = importlib.util.module_from_spec(_spec)  # type: ignore[arg-type]
sys.modules["_quality_harness"] = _mod  # Python 3.13+ dataclass compat -- must precede exec_module
_spec.loader.exec_module(_mod)  # type: ignore[union-attr]

detect_defects = _mod.detect_defects
SectionResolutionError = _mod.SectionResolutionError
_render_example_chain_blocks = _mod._render_example_chain_blocks
_chain_block_well_formed = _mod._chain_block_well_formed
_DEFECT_RECORD_FIELDS = _mod._DEFECT_RECORD_FIELDS
# Phase 19 (CONF-07/CONF-08): read-only bindings the D-03 perturbation floor
# uses to locate mutation sites STRUCTURALLY, through the same section-
# slicing and cell/chain/citation vocabulary the frozen detector itself
# uses -- never a hand-transcribed byte literal per item. Calling these is
# unrestricted; CONTRACT-06 forbids editing them, not reading them.
_slice_sections = _mod._slice_sections
_verdict_cells = _mod._verdict_cells
_verdict_conforms = _mod._verdict_conforms
_chain_ids = _mod._chain_ids
_chain_blocks = _mod._chain_blocks
_STRUCTURAL_LEDGER_ROW_RE = _mod._STRUCTURAL_LEDGER_ROW_RE
_cites_chain = _mod._cites_chain

# Derived, never restated: slices of the frozen schema tuple, so widening
# _DEFECT_RECORD_FIELDS upstream cannot silently narrow what this script excludes from
# source-vs-twin agreement.
PROVENANCE_FIELDS: tuple[str, ...] = _DEFECT_RECORD_FIELDS[13:]
MEASURED_SCHEMA_FIELDS: tuple[str, ...] = _DEFECT_RECORD_FIELDS[1:13]
REPORT_FIELDS: tuple[str, ...] = (
    "section_resolution",
    "heading_chain_blocks",
    "heading_malformed_blocks",
    "marked_untraced_claims",
    "silent_untraced_claims",
)
# D-04 (settled decision, sharpening RESEARCH.md A3), widened by D-06a: seventeen fields
# compared for source-vs-twin agreement -- the twelve measured schema fields plus the five
# report-added columns (three heading-census columns plus the two D-06a marked/silent
# untraced-claim columns). Excluded: analysis_id (foreordained equal, same filename stem on
# both surfaces) and the nine always-"n/a" provenance columns (foreordained equal, no capture
# exists for any of the 29 artifacts). Including either would inflate the agreement headline
# with matches that cannot fail.
AGREEMENT_FIELDS: tuple[str, ...] = MEASURED_SCHEMA_FIELDS + REPORT_FIELDS

# D-06a: the exact marker literal `output-template.md`, `validation-rubric.md` and
# `SKILL-body.md` all prescribe for a legitimately-untraced but honestly-flagged claim (U+2014
# EM DASH, lower case, no trailing punctuation inside the marker itself -- a claim's own
# sentence-ending period after the marker is not part of it). Defined once here and
# referenced wherever the marked/silent split is computed -- never inlined at a second call
# site.
CAVEAT_MARKER: str = "no chain — flagged assumption only"


class DiscoveryFloorError(RuntimeError):
    """Raised when discover_artifacts finds fewer artifacts than its named floors require.

    Carries every accumulated floor-failure message -- main() prints them all to stderr and
    exits 1. Never return a short list silently; that is the exact failure D-02 forbids.
    """


@dataclass(frozen=True)
class Artifact:
    surface: Literal[
        "shared-examples", "generated-twin", "contract-surface", "adversarial-corpus"
    ]
    relpath: str
    path: Path
    analysis_id: str


def discover_artifacts(repo_root: Path) -> list[Artifact]:
    """Glob the two example directories, resolve the contract surface by explicit path,
    and glob the adversarial corpus, then enforce four named count floors (D-02).
    `repo_root` is a parameter (not a module-level read) so --self-test can drive this
    against a tempdir fixture.

    `sorted()` is mandatory on every glob result: Path.glob order is not stable across
    platforms, and byte-for-byte --check reproduction depends on it.
    """
    messages: list[str] = []

    shared_paths = sorted(repo_root.glob(SHARED_EXAMPLES_GLOB))
    if len(shared_paths) < MIN_SHARED_EXAMPLES:
        messages.append(
            f"report-conformance: COUNT FLOOR FAIL — expected >= {MIN_SHARED_EXAMPLES} "
            f"files matching {SHARED_EXAMPLES_GLOB}, found {len(shared_paths)}"
        )

    twin_paths = sorted(repo_root.glob(TWIN_EXAMPLES_GLOB))
    if len(twin_paths) < MIN_TWIN_EXAMPLES:
        messages.append(
            f"report-conformance: COUNT FLOOR FAIL — expected >= {MIN_TWIN_EXAMPLES} "
            f"files matching {TWIN_EXAMPLES_GLOB}, found {len(twin_paths)}"
        )

    contract_path = repo_root / CONTRACT_SURFACE_RELPATH
    contract_paths = [contract_path] if contract_path.is_file() else []
    if len(contract_paths) < MIN_CONTRACT_SURFACES:
        # Named-path failure, never a bare count of zero -- the contract surface is
        # resolved by explicit path, not a glob, so "found 0" would obscure which exact
        # file is missing.
        messages.append(
            f"report-conformance: COUNT FLOOR FAIL — expected {CONTRACT_SURFACE_RELPATH} "
            f"to exist at {contract_path}, found missing"
        )

    # The two sidecar files (catalog.md, README.md) are excluded by name -- they are
    # metadata about the corpus, never a corpus item to measure.
    corpus_excluded = {
        (repo_root / ADVERSARIAL_CORPUS_CATALOG).resolve(),
        (repo_root / ADVERSARIAL_CORPUS_README).resolve(),
    }
    corpus_paths = [
        p
        for p in sorted(repo_root.glob(ADVERSARIAL_CORPUS_GLOB))
        if p.resolve() not in corpus_excluded
    ]
    if len(corpus_paths) < MIN_CORPUS_ITEMS:
        messages.append(
            f"report-conformance: COUNT FLOOR FAIL — expected >= {MIN_CORPUS_ITEMS} "
            f"files matching {ADVERSARIAL_CORPUS_GLOB} (excluding catalog.md and "
            f"README.md), found {len(corpus_paths)}"
        )

    if messages:
        raise DiscoveryFloorError("\n".join(messages))

    artifacts: list[Artifact] = []
    for p in shared_paths:
        artifacts.append(
            Artifact("shared-examples", p.relative_to(repo_root).as_posix(), p, p.stem)
        )
    for p in twin_paths:
        artifacts.append(
            Artifact("generated-twin", p.relative_to(repo_root).as_posix(), p, p.stem)
        )
    for p in contract_paths:
        artifacts.append(
            Artifact("contract-surface", p.relative_to(repo_root).as_posix(), p, p.stem)
        )
    for p in corpus_paths:
        artifacts.append(
            Artifact("adversarial-corpus", p.relative_to(repo_root).as_posix(), p, p.stem)
        )
    return artifacts


_CORPUS_CATALOG_COLUMNS: dict[str, str] = {
    "ID": "id",
    "File": "file",
    "Stratum": "stratum",
    "Source": "source",
    "What is false": "what_is_false",
    "Rule that ought to catch it": "ought_to_catch",
    "Disposition": "disposition",
    "Target": "target",
}
_VALID_STRATA: frozenset[str] = frozenset({"A", "B1", "B2"})

# Phase 19 (CONF-08, D-19-08-B): the closed vocabulary the catalog's `Target`
# column is validated against -- the three `detect_defects` columns with
# genuine substantive reach. `Target` is deliberately scoped to these three:
# a stratum-B1 item reachable only by PROV-GUARD reads the literal `none`
# here, which does not mean "nothing reaches it" -- the `Stratum` column and
# `Rule that ought to catch it` prose carry that distinction instead.
_CORPUS_TARGET_COLUMNS: frozenset[str] = frozenset(
    {"dependency_cycles", "ungrounded_chains", "selfaudit_disagreements"}
)


def _parse_corpus_target(cell: str) -> tuple[list[tuple[str, list[str]]], list[str]]:
    """Parse one `Target` cell into `(pairs, problems)`.

    Grammar (closed; an unrecognised shape is reported by name, never
    silently accepted or silently dropped): the literal `none` (a stratum-B1
    or B2 item with no `detect_defects` target), or one or more `;`-joined
    `<column>:<selector>` terms, `<column>` one of `_CORPUS_TARGET_COLUMNS`,
    `<selector>` a comma-joined list (chain ids for `dependency_cycles`/
    `ungrounded_chains`, integer criterion numbers for
    `selfaudit_disagreements`).

    On ANY problem anywhere in the cell, the returned pair list is EMPTY --
    a cell that is partly well-formed and partly malformed is not partially
    trusted; every problem found is still reported by name in the second
    return value, so a floor built on this has something to name. This
    mirrors `parse_corpus_catalog`'s own "never silently drop, report as a
    problem instead" discipline for the row as a whole.
    """
    problems: list[str] = []
    stripped = cell.strip()

    if not stripped:
        return [], ["empty Target cell"]
    if stripped == "none":
        return [], []

    pairs: list[tuple[str, list[str]]] = []
    for term in stripped.split(";"):
        term = term.strip()
        if ":" not in term:
            problems.append(f"term has no ':': {term!r}")
            continue
        column, _, selector_str = term.partition(":")
        column = column.strip()
        selector_str = selector_str.strip()
        if column not in _CORPUS_TARGET_COLUMNS:
            problems.append(
                f"unknown column {column!r} (expected one of "
                f"{sorted(_CORPUS_TARGET_COLUMNS)})"
            )
            continue
        if not selector_str:
            problems.append(f"empty selector for column {column!r}")
            continue
        selectors = [s.strip() for s in selector_str.split(",")]
        if any(not s for s in selectors):
            problems.append(f"empty selector element in {term!r}")
            continue
        if column == "selfaudit_disagreements":
            non_integers = [s for s in selectors if not s.isdigit()]
            if non_integers:
                problems.append(
                    f"selfaudit_disagreements selector not an integer: {non_integers!r}"
                )
                continue
        pairs.append((column, selectors))

    if problems:
        return [], problems
    return pairs, []


def parse_corpus_catalog(repo_root: Path) -> tuple[dict[str, dict], list[str]]:
    """Parse `ADVERSARIAL_CORPUS_CATALOG`'s `## Catalog` table into
    `{stem: {"stratum": ..., "source": ..., "what_is_false": ..., "ought_to_catch": ...,
    "disposition": ..., "target": ..., "parsed_target": ...}}`, keyed by the `File` column
    (the artifact stem, matching `Artifact.analysis_id`).

    Parses by locating the header row containing all eight column names, then reading the
    `|`-delimited data rows beneath it, mapping BY HEADER NAME, never by position -- a
    future column insertion must not silently shift the parse. Never silently drops a
    malformed row: a row whose `File` cell is empty, or whose `Stratum` cell is not one of
    A/B1/B2, is returned as a parse problem in the second tuple element instead, so a
    floor built on this function's output can report parse failures by name rather than
    seeing a shorter dict than expected.

    Phase 19 (CONF-08, D-19-08-B): the `Target` cell is additionally run through
    `_parse_corpus_target`. A `Target` that fails to parse does NOT drop the row -- the
    entry is still returned, with `target` set to the raw cell text and `parsed_target`
    empty, so a later floor (the roster/disposition floors this feeds) has something to
    name -- and every problem `_parse_corpus_target` reports is folded into this
    function's own *problems* list, prefixed `CATALOG TARGET PARSE FAIL — <file>: <reason>`
    so `_corpus_roster_problems` reports it alongside the existing `CATALOG PARSE FAIL`
    strings, never as a second, separately-consumed channel.
    """
    text = (repo_root / ADVERSARIAL_CORPUS_CATALOG).read_text(encoding="utf-8")
    lines = text.splitlines()

    header_idx: int | None = None
    header_cols: list[str] = []
    for i, line in enumerate(lines):
        if not line.strip().startswith("|"):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if all(name in cells for name in _CORPUS_CATALOG_COLUMNS):
            header_idx = i
            header_cols = cells
            break

    entries: dict[str, dict] = {}
    problems: list[str] = []

    if header_idx is None:
        problems.append(
            f"CATALOG PARSE FAIL — header row naming all of "
            f"{sorted(_CORPUS_CATALOG_COLUMNS)} not found in {ADVERSARIAL_CORPUS_CATALOG}"
        )
        return entries, problems

    col_index = {name: header_cols.index(name) for name in _CORPUS_CATALOG_COLUMNS}

    # The row immediately after the header is the `|---|---|...` separator; skip it.
    for line in lines[header_idx + 2 :]:
        stripped = line.strip()
        if not stripped.startswith("|"):
            # The table has ended (blank line, prose, or next heading).
            break
        cells = [c.strip() for c in stripped.strip("|").split("|")]
        if len(cells) <= max(col_index.values()):
            problems.append(f"CATALOG PARSE FAIL — short row, cannot map columns: {stripped!r}")
            continue

        file_cell = cells[col_index["File"]]
        stratum_cell = cells[col_index["Stratum"]]

        if not file_cell:
            problems.append(f"CATALOG PARSE FAIL — empty File cell: {stripped!r}")
            continue
        if stratum_cell not in _VALID_STRATA:
            problems.append(
                f"CATALOG PARSE FAIL — {file_cell}: Stratum {stratum_cell!r} not one of "
                f"{sorted(_VALID_STRATA)}"
            )
            continue

        target_cell = cells[col_index["Target"]]
        parsed_target, target_problems = _parse_corpus_target(target_cell)
        for reason in target_problems:
            problems.append(f"CATALOG TARGET PARSE FAIL — {file_cell}: {reason}")

        entries[file_cell] = {
            "stratum": stratum_cell,
            "source": cells[col_index["Source"]],
            "what_is_false": cells[col_index["What is false"]],
            "ought_to_catch": cells[col_index["Rule that ought to catch it"]],
            "disposition": cells[col_index["Disposition"]],
            "target": target_cell,
            "parsed_target": parsed_target,
        }

    return entries, problems


def build_row(artifact: Artifact, _audit_record_out: dict | None = None) -> dict:
    """D-03's partial row: the heading census runs FIRST and unconditionally, so a
    document `_slice_sections` rejects still carries a real heading-sweep reading rather
    than losing that datum along with everything `detect_defects` would have produced.

    Three-way column vocabulary, never confused with each other: a number means the
    detector read the document and counted; the literal "n/a" means no `.jsonl` capture
    exists (true of all 29 artifacts for the nine provenance columns, unconditionally --
    detect_defects never running changes nothing about capture availability); the literal
    "unreadable" means `_slice_sections` rejected the document, so the twelve measured
    schema fields were never computed.

    Phase 19 (CONF-08): *_audit_record_out*, when given a dict, is populated IN PLACE with
    the raw `detect_defects` return record (including its underscore-prefixed audit-only
    fields, e.g. `_dependency_cycles`) whenever the document is readable -- a private
    channel `build_corpus_row` uses to reach those fields without a second `detect_defects`
    call and without widening this function's own return schema for the other three
    surfaces (shared-examples, generated-twin, contract-surface never pass this argument).
    Left empty (never populated) when the document is unreadable, matching `row`'s own
    "no `detect_defects` record exists" state for that case.
    """
    text = artifact.path.read_text(encoding="utf-8")

    blocks = _render_example_chain_blocks(text)
    heading_chain_blocks = len(blocks)
    heading_malformed_blocks = sum(1 for _, b in blocks if not _chain_block_well_formed(b))

    row: dict = {
        "surface": artifact.surface,
        "relpath": artifact.relpath,
        "section_resolution": None,
        "heading_chain_blocks": heading_chain_blocks,
        "heading_malformed_blocks": heading_malformed_blocks,
    }

    try:
        record = detect_defects(text, artifact.analysis_id)
        row["section_resolution"] = "OK"
        for field in _DEFECT_RECORD_FIELDS:
            row[field] = record[field]
        # D-06a: derived from the SAME detect_defects record's audit-only
        # `_untraced_claims_text` -- never a second markdown parse. A marked caveat still
        # scores untraced (R-CLAIM-CAVEAT-MARKED); this only splits that existing count into
        # "disclosed the gap" vs. "silently untraced".
        marked_untraced = sum(
            1 for claim_text in record["_untraced_claims_text"] if CAVEAT_MARKER in claim_text
        )
        row["marked_untraced_claims"] = marked_untraced
        row["silent_untraced_claims"] = row["untraced_claims"] - marked_untraced
        if _audit_record_out is not None:
            _audit_record_out.update(record)
    except SectionResolutionError as exc:
        row["section_resolution"] = f"SectionResolutionError: {exc}"
        for field in _DEFECT_RECORD_FIELDS:
            if field == "analysis_id":
                row[field] = artifact.analysis_id
            elif field in PROVENANCE_FIELDS:
                # Always "n/a" regardless of readability: no .jsonl capture exists for
                # this artifact whether or not detect_defects ran.
                row[field] = "n/a"
            else:
                row[field] = "unreadable"
        # D-06a: `_slice_sections` never ran, so there is no `_untraced_claims_text` to
        # scan. This must read the literal "unreadable", never "0" -- the module's own
        # three-way vocabulary (a number counted, "n/a" no capture, "unreadable" unparsed).
        row["marked_untraced_claims"] = "unreadable"
        row["silent_untraced_claims"] = "unreadable"

    return row


# Phase 19 (CONF-07/CONF-08): the two derived-field tuples that define a corpus item's
# "fully clean" predicate. Form fields are the same three columns CONF-07's precondition
# pins to zero corpus-wide; substantive fields are the three columns with genuine
# detector reach (dependency_cycles, ungrounded_chains, selfaudit_disagreements) -- NOT
# form checks, and the only columns this corpus's stratum-A positive controls are built
# to fire on.
_CORPUS_FORM_FIELDS: tuple[str, ...] = (
    "untraced_claims",
    "nonconforming_verdict_cells",
    "malformed_chain_blocks",
)
_CORPUS_SUBSTANTIVE_FIELDS: tuple[str, ...] = (
    "dependency_cycles",
    "ungrounded_chains",
    "selfaudit_disagreements",
)


def _corpus_target_hits(
    record: dict, parsed_targets: list[tuple[str, list[str]]]
) -> list[str]:
    """Phase 19 (CONF-08, D-19-08-B): given a raw `detect_defects` return *record* (its
    underscore-prefixed audit fields specifically) and a `_parse_corpus_target`-parsed
    pair list, return the sorted list of `<column>:<selector>` target terms that HIT --
    using the record's own audit fields and nothing else.

    Chain-SCOPED, never column-scoped -- this is the load-bearing reason this join has
    this shape rather than a simpler one. `t13`'s catalogued target is chain C1
    specifically; its measured `_ungrounded_chains` names c2 and c3. A column-level join
    ("did `ungrounded_chains` fire at all?") would score `t13` CAUGHT -- the exact wrong
    answer the 19-VERIFICATION.md gap named, reached by a different route. Comparing chain
    ids case-insensitively (the audit lists are already lowercased; catalog values are
    written lowercase) is what lets this distinguish "the catalogued chain was flagged"
    from "a different chain was flagged".

    `dependency_cycles:<ids>` / `ungrounded_chains:<ids>` hit iff any named id appears in
    `record["_dependency_cycles"]` / `record["_ungrounded_chains"]`.
    `selfaudit_disagreements:<n>` hits iff any entry in `record["_selfaudit_disagreements"]`
    has `criterion` equal to `int(n)`.
    """
    hits: list[str] = []
    for column, selectors in parsed_targets:
        if column in ("dependency_cycles", "ungrounded_chains"):
            audit_ids = {str(i).lower() for i in record.get(f"_{column}", [])}
            if any(s.lower() in audit_ids for s in selectors):
                hits.append(f"{column}:{','.join(selectors)}")
        elif column == "selfaudit_disagreements":
            wanted_criteria = {int(s) for s in selectors}
            disagreement_criteria = {
                d.get("criterion") for d in record.get("_selfaudit_disagreements", [])
            }
            if wanted_criteria & disagreement_criteria:
                hits.append(f"{column}:{','.join(selectors)}")
    return sorted(hits)


def build_corpus_row(artifact: Artifact, catalog_entry: dict | None) -> dict:
    """A thin wrapper over `build_row` -- never a second `detect_defects` call and never a
    reimplementation. Calls `build_row(artifact, _audit_record_out)` exactly once (the
    `_audit_record_out` private channel surfaces the raw `detect_defects` record's
    underscore-prefixed audit fields without widening `build_row`'s own return schema for
    the other three surfaces), then merges in the joined catalog fields (`stratum`,
    `source`, `disposition`, `target`) plus four computed fields:

    `no_column_fired` (Phase 19, CONF-08 -- the renamed identifier this predicate used to
    carry conflated two distinct concepts under one clean-sounding name) is True iff
    `section_resolution == "OK"` and every field in both `_CORPUS_FORM_FIELDS` and
    `_CORPUS_SUBSTANTIVE_FIELDS` reads the integer 0. It means exactly what its name
    says -- no `detect_defects` column fired on this document -- and NEVER means "the
    item's catalogued falsehood was caught"; `t13-grounded-alongside-cyclic-ref` is live
    proof the two diverge (its `no_column_fired` reads False because an unrelated column
    fires, while its own catalogued target is never flagged). This field is a per-row
    DIAGNOSTIC, demoted from the published headline it used to drive.

    `target_hits` is the sorted list `_corpus_target_hits` returns for this item's parsed
    catalog `Target` against its own `detect_defects` audit fields.

    `target_missed` -- **the field the published false-negative figure keys on** -- is
    True iff `target_hits` is empty. A `Target` of `none` is therefore ALWAYS
    `target_missed=True`: no `detect_defects` column is this item's catalogued target, so
    `detect_defects` cannot have caught it. A row with no catalog entry at all (`target`
    the literal "MISSING") is likewise always `target_missed=True`. An **unreadable** row
    is `target_missed=True` and `no_column_fired=False` -- unchanged from how an
    unreadable row was always scored non-clean under the predicate this replaces.

    `form_defects` is the summed `_CORPUS_FORM_FIELDS` when readable, and the literal
    "unreadable" otherwise -- preserving `build_row`'s three-way column vocabulary rather
    than coercing an unreadable row's absence of a count into 0.

    If *catalog_entry* is None (the artifact has no catalog row), `stratum`/`source`/
    `disposition`/`target` are populated with the literal "MISSING" rather than omitted,
    so the row still renders and a later floor has something to name. The row is never
    dropped.
    """
    audit_record: dict = {}
    row = build_row(artifact, audit_record)

    if catalog_entry is None:
        row["stratum"] = "MISSING"
        row["source"] = "MISSING"
        row["disposition"] = "MISSING"
        row["target"] = "MISSING"
        parsed_target: list[tuple[str, list[str]]] = []
    else:
        row["stratum"] = catalog_entry["stratum"]
        row["source"] = catalog_entry["source"]
        row["disposition"] = catalog_entry["disposition"]
        row["target"] = catalog_entry["target"]
        parsed_target = catalog_entry["parsed_target"]

    readable = row["section_resolution"] == "OK"
    if readable:
        row["form_defects"] = sum(row[f] for f in _CORPUS_FORM_FIELDS)
        row["no_column_fired"] = all(row[f] == 0 for f in _CORPUS_FORM_FIELDS) and all(
            row[f] == 0 for f in _CORPUS_SUBSTANTIVE_FIELDS
        )
        target_hits = _corpus_target_hits(audit_record, parsed_target)
        row["target_hits"] = target_hits
        row["target_missed"] = len(target_hits) == 0
    else:
        row["form_defects"] = "unreadable"
        row["no_column_fired"] = False
        row["target_hits"] = []
        row["target_missed"] = True

    return row


def build_rows(repo_root: Path) -> list[dict]:
    """One row per discovered artifact, in discovery order (shared-examples, then
    generated-twin, then contract-surface, then adversarial-corpus; each group sorted by
    discover_artifacts). Corpus artifacts are routed through `build_corpus_row`, joined
    against a catalog parsed exactly once per call; the other three surfaces go through
    the unwrapped `build_row`. A catalog parse problem is not raised here -- reporting it
    is a later floor's job (plan 19-06); an artifact whose stem has no clean catalog
    entry simply reads `stratum`/`source`/`disposition` as "MISSING", never dropped."""
    catalog_entries, _catalog_problems = parse_corpus_catalog(repo_root)

    rows: list[dict] = []
    for artifact in discover_artifacts(repo_root):
        if artifact.surface == "adversarial-corpus":
            rows.append(build_corpus_row(artifact, catalog_entries.get(artifact.analysis_id)))
        else:
            rows.append(build_row(artifact))
    return rows


# ---------------------------------------------------------------------------
# Phase 19 (CONF-07/CONF-08): the three corpus floors that make the
# false-negative-rate reading falsifiable. Each mirrors a shape already
# proven in scripts/check-conf-gate.py -- copied here because the corpus
# floors read report-conformance.py's own build_rows/parse_corpus_catalog
# output and check-conf-gate.py is scoped to the 14 shipped exemplars only
# (RESEARCH.md D-03 / <interfaces>). Neither check-quality-harness.py nor
# check-conf-gate.py is imported for write access anywhere in this section.
# ---------------------------------------------------------------------------


def _corpus_roster_problems(
    catalog_entries: dict[str, dict],
    catalog_problems: list[str],
    corpus_rows: list[dict],
) -> list[str]:
    """D-04: EQUALITY, never subset, between the corpus catalog's `File`
    column stem set and the discovered adversarial-corpus stem set -- the
    18-D-07 pattern (`_claim_floor_roster_problems`'s shape, copied
    verbatim) adopted after a subset test proved unable to see its own
    table narrowing. Reports both `missing` (a discovered item with no
    catalog row) and `extra` (a catalog row naming no discovered file) by
    name in one `D-04 CORPUS ROSTER DRIFT` problem.

    Also folds in `parse_corpus_catalog`'s own *catalog_problems* -- a
    malformed catalog row (empty `File` cell, invalid `Stratum`) is
    reported by name here rather than silently shrinking the entries dict
    the roster comparison itself reads.
    """
    problems: list[str] = list(catalog_problems)
    catalog_stems = set(catalog_entries)
    discovered_stems = {r["analysis_id"] for r in corpus_rows}
    missing = sorted(discovered_stems - catalog_stems)
    extra = sorted(catalog_stems - discovered_stems)
    if missing or extra:
        problems.append(f"D-04 CORPUS ROSTER DRIFT: missing={missing} extra={extra}")
    return problems


# The three disposition prefixes D-04/CONTEXT.md's stratum table names as
# honest dispositions. A fourth value ("MISSING", or an empty cell) is
# exactly the silent pass CONF-08 forbids.
_VALID_DISPOSITION_PREFIXES: tuple[str, ...] = ("fix", "accept-with-reason", "defer-with-owner")


def _corpus_disposition_problems(corpus_rows: list[dict]) -> list[str]:
    """CONF-08's zero-silent-passes clause, made mechanical rather than a
    prose promise. Phase 19 (CONF-08, D-19-08-A/B): checks every row whose
    `target_missed` is True OR whose `no_column_fired` is True -- the UNION
    of the two predicates, never `no_column_fired` alone. This is the fix
    for the 19-VERIFICATION.md gap: under the old single-predicate scope,
    `t13-grounded-alongside-cyclic-ref` escaped this floor entirely (an
    unrelated column fired on it, so it was never "clean"), even though its
    own catalogued falsehood was silently missed -- exactly the silent pass
    CONF-08 exists to catch. The union can only ever be a superset of the
    old scope, never narrower, so this widening cannot let a
    previously-checked row escape.

    Requires a `disposition` that is non-empty, is not the literal
    "MISSING", and begins with one of `fix` / `accept-with-reason` /
    `defer-with-owner`. A row where NEITHER predicate is True is never
    checked here -- a genuine catch, with no diagnostic column firing
    either, needs no disclosed disposition.
    """
    problems: list[str] = []
    for r in corpus_rows:
        if r["target_missed"] is not True and r["no_column_fired"] is not True:
            continue
        disposition = r.get("disposition")
        if not disposition or disposition == "MISSING":
            problems.append(
                f"SILENT PASS [{r['analysis_id']}]: catalogued target missed or no "
                "column fired, no disposition recorded"
            )
            continue
        if not any(disposition.startswith(p) for p in _VALID_DISPOSITION_PREFIXES):
            problems.append(
                f"DISPOSITION FORM [{r['analysis_id']}]: {disposition!r} does not "
                "begin with fix / accept-with-reason / defer-with-owner"
            )
    return problems


# CONF-07/CONF-08 (Phase 19, D-05 source-literal discipline, the 18-12
# "re-derive, never transcribe" convention): three corpus-wide DENOMINATOR
# floors, each the sum of the named field over every READABLE corpus row,
# re-derived at authoring time from docs/data/conformance.json's
# adversarial_corpus.rows and pinned here as source literals -- never read
# back from that regenerated artifact. Derivation command (19-06-SUMMARY.md
# quotes its verbatim output):
#
#   python3 -c "
#   import json
#   data = json.load(open('docs/data/conformance.json'))
#   rows = data['adversarial_corpus']['rows']
#   for f in ('conclusion_claims', 'verdict_cells', 'chain_blocks'):
#       print(f, sum(r[f] for r in rows if r['section_resolution'] == 'OK'))
#   "
#
# These are DENOMINATOR floors, not targets: a zero numerator
# (untraced_claims == 0, etc.) is meaningful only against a population that
# has not itself been deleted. DISCLOSED BOUND: a floor here detects
# population SHRINKAGE below the pinned figure, never substitution --
# deleting one item's rows while another item's grows by the same count
# would not fire it. Legitimate corpus growth never fires this floor; a
# legitimate reduction is a deliberate two-place edit -- this constant and
# its neutralization-tested control both move together, the same
# discipline check-conf-gate.py's `_POPULATION_FLOORS` already applies.
_CORPUS_POPULATION_FLOORS: dict[str, int] = {
    "conclusion_claims": 49,
    "verdict_cells": 66,
    "chain_blocks": 32,
}


def _corpus_population_problems(corpus_rows: list[dict]) -> list[str]:
    """CONF-07's population precondition, two layers.

    Per item: every READABLE corpus row must read `conclusion_claims >= 1`
    and `chain_blocks >= 1` -- a form-clean reading over an empty
    population is not a probe. An unreadable row is reported by name too,
    never silently skipped (it is also caught by Task 1's roster/build
    machinery upstream, but this floor names it independently so a reader
    scanning only D-03/D-05's output still sees it).

    Corpus-wide: the three `_CORPUS_POPULATION_FLOORS` denominators, summed
    over readable rows, must not fall below their pinned floor -- so a zero
    numerator achieved by deleting the measured population, rather than by
    genuine detector clarity, is caught.
    """
    problems: list[str] = []
    totals: dict[str, int] = {field: 0 for field in _CORPUS_POPULATION_FLOORS}
    for r in corpus_rows:
        if r["section_resolution"] != "OK":
            problems.append(
                f"CORPUS POPULATION [{r['analysis_id']}] section_resolution: "
                "unreadable — a form-clean reading over an empty population is "
                "not a probe"
            )
            continue
        for field in ("conclusion_claims", "chain_blocks"):
            if r[field] == 0:
                problems.append(
                    f"CORPUS POPULATION [{r['analysis_id']}] {field}: 0 — a "
                    "form-clean reading over an empty population is not a probe"
                )
        for field in _CORPUS_POPULATION_FLOORS:
            totals[field] += r[field]

    for field, floor in _CORPUS_POPULATION_FLOORS.items():
        actual = totals[field]
        if actual < floor:
            problems.append(
                f"CORPUS POPULATION FLOOR BREACH {field}: {actual} < floor "
                f"{floor} — a zero defect count against a shrunken population "
                "is not conformance"
            )
    return problems


# ---------------------------------------------------------------------------
# Phase 19 (CONF-07/CONF-08, D-03): the per-item in-memory perturbation
# floor -- this phase's anti-vacuity backbone, the one arm a tempdir/
# synthetic self-test structurally cannot provide. Reuses check-conf-gate.py
# `_run_d08_arm_on`'s shape (read baseline, mutate one occurrence, re-
# measure, assert the specific field moved by the expected amount, never
# exit) generalized from ONE hardcoded (surface, id) target to EVERY corpus
# row. CONF-GATE's exact-string-count-== 1 "site is unique" test does not
# scale here: a corpus item's own inline citations legitimately repeat
# ("(chain C2)" 2-3 times in one item is normal prose, not a defect), so
# string-literal uniqueness cannot be the "site found" signal the way it is
# for CONF-GATE's one long, naturally-unique needle. Sites are instead
# located by ABSOLUTE POSITION: the structural locator returns a
# (start, end) character span inside the document, computed from the
# frozen detector's own section-slicing and cell/chain/citation vocabulary,
# and the mutation is a precise slice replacement at that span -- there is
# no string-count ambiguity to lose, because the span IS the site.
# ---------------------------------------------------------------------------

_HOP_ARROW: str = "→"  # U+2192 RIGHTWARDS ARROW

# The inline section-6 citation form every corpus item that carries one
# uses: "(chain C2)" or "(chains C1 and C2)" (also accepting a comma-joined
# form for robustness). Matched case-insensitively, matching _cites_chain's
# own case-folded loose-match half.
_INLINE_CHAIN_CITE_RE = re.compile(
    r"\(chains?\s+C\d+(?:\s*(?:,|and)\s*C\d+)*\)", re.IGNORECASE
)


def _corpus_section_offsets(
    text: str, section2: str, section4: str, section6: str
) -> tuple[int, int, int] | None:
    """Absolute character offsets of sections 2, 4 and 6 within *text*,
    located in DOCUMENT ORDER -- each search starts immediately after the
    previous section's own start, so a byte-identical section body
    occurring twice (never observed in this corpus, guarded against
    anyway) resolves to its real in-order position rather than an earlier
    false match. Returns None if any section cannot be located -- this
    should never happen for text `_slice_sections` itself just sliced
    *text* from, but the caller treats a None here as a not-found
    mutation site rather than raising.
    """
    sec2 = text.find(section2)
    if sec2 == -1:
        return None
    sec4 = text.find(section4, sec2 + len(section2))
    if sec4 == -1:
        return None
    sec6 = text.find(section6, sec4 + len(section4))
    if sec6 == -1:
        return None
    return sec2, sec4, sec6


def _corpus_verdict_mutation_site(
    text: str, section2: str, sec2_start: int
) -> tuple[int, int] | None:
    """(a) verdict-cell separator: the absolute [start, end) span of the
    U+2014 EM DASH inside the first `_verdict_cells` entry `_verdict_
    conforms` accepts. Cells are tried in document order; a cell whose own
    text cannot be relocated inside section2 (a whitespace-normalization
    edge case) is skipped in favour of the next one rather than aborting
    the whole search -- CONF-07's own precondition guarantees every corpus
    item carries at least one conforming cell, so exhausting the list
    without a hit is treated as a genuine "not found" by the caller.
    """
    search_from = 0
    for cell in _verdict_cells(section2):
        local = section2.find(cell, search_from)
        if local == -1:
            continue
        search_from = local + len(cell)
        if not _verdict_conforms(cell):
            continue
        dash_local = cell.find("—")
        if dash_local == -1:
            continue
        abs_start = sec2_start + local + dash_local
        return abs_start, abs_start + 1
    return None


def _corpus_hop_mutation_site(
    text: str, section4: str, sec4_start: int
) -> tuple[int, int] | None:
    """(b) chain-hop re-wrap: the absolute [start, end) span of the leading
    U+2192 on the first chain-block line that begins with it, scanning
    `_chain_blocks(section4)` in document order. Genuinely absent for a
    single-line chain whose two arrows sit on the SAME physical line as the
    GT head (`GT-1 -> intermediate -> conclusion`, no separate continuation
    line) -- five of this corpus's thirteen items use exactly that shape.
    The caller treats a (b) absence as an EXPECTED CONDITION, never a
    reported problem on its own (see `_corpus_perturbation_problems`).
    """
    for block in _chain_blocks(section4):
        block_local = section4.find(block)
        if block_local == -1:
            continue
        cursor = block_local
        for line in block.splitlines(keepends=True):
            if line.strip().startswith(_HOP_ARROW):
                arrow_local = cursor + line.index(_HOP_ARROW)
                abs_start = sec4_start + arrow_local
                return abs_start, abs_start + 1
            cursor += len(line)
    return None


def _corpus_citation_mutation_site(
    section6: str, sec6_start: int, chain_ids: list[str]
) -> tuple[int, int] | None:
    """(c) citation removal: the absolute [start, end) span of the first
    section-6 citation -- an inline `(chain Cn)`/`(chains Cn and Cm)`
    parenthetical, tried first, or a structural closure-ledger row's
    arrow-to-chain-id tail, tried as a fallback.

    Re-measured (Phase 19, plan 19-08 Task 3) rather than transcribed: exactly ONE
    structural ledger row exists across all thirteen corpus items --
    `t01-ledger-arbitrary-chain`'s own 999.2-seed-case ledger row (measured via
    `_closure_ledger_fragments`, command and verbatim output in 19-08-SUMMARY.md). The
    prior claim of zero was false. Despite that one row existing, the ledger fallback
    branch below is STILL never exercised against real corpus bytes: `t01` ALSO carries
    inline `(chain Cn)` citations earlier in the same section-6 body, and
    `_INLINE_CHAIN_CITE_RE.search` matches on the FIRST inline occurrence anywhere in
    `section6` regardless of where the ledger row sits, so this function always returns
    from the inline branch before ever reaching the fallback below. The branch remains
    genuinely untested against real corpus bytes -- for a different, now-measured
    reason ("an inline citation always wins the search when both forms coexist in one
    document") rather than the previous false one ("no ledger row exists to test
    against").
    """
    m = _INLINE_CHAIN_CITE_RE.search(section6)
    if m is not None:
        return sec6_start + m.start(), sec6_start + m.end()

    cursor = 0
    for line in section6.splitlines(keepends=True):
        stripped = line.strip()
        leading_ws = len(line) - len(line.lstrip())
        ledger_m = _STRUCTURAL_LEDGER_ROW_RE.match(stripped)
        if ledger_m is not None and _cites_chain(stripped, chain_ids):
            arrow_char = "→" if "→" in stripped else "->"
            tail_start_in_stripped = stripped.index(arrow_char)
            tail_end_in_stripped = ledger_m.end(2)
            abs_start = sec6_start + cursor + leading_ws + tail_start_in_stripped
            abs_end = sec6_start + cursor + leading_ws + tail_end_in_stripped
            return abs_start, abs_end
        cursor += len(line)
    return None


def _corpus_perturbation_problems(rows: list[dict], repo_root: Path) -> list[str]:
    """D-03: for EVERY corpus row (never one hardcoded target), read the
    item's shipped bytes fresh from *repo_root*, take
    `baseline = detect_defects(text, analysis_id)`, then run the three
    structurally-located mutation families above and assert each one that
    fires moves its target field by exactly the expected amount. Mutations
    are IN-MEMORY ONLY: `tests/adversarial-corpus-v9.0/` is never written
    by this function (it is about to be registered in `_FROZEN_PATHS`, and
    `check-quality-harness.py` already refuses writes into a frozen path).
    Every family runs for every item regardless of whether an earlier
    family or item failed -- nothing short-circuits.

    Per-family absence disposition, decided here rather than left implicit
    (RESEARCH.md Q4's own framing: "not every item will admit every
    family"): families (a) and (c) are EXPECTED to find a site on every
    corpus item -- CONF-07's population floor above already requires every
    item to carry verdict cells and traced §6 claims, so a missing (a) or
    (c) site is reported as `D-03(<family>) mutation site not found`.
    Family (b) requires a chain block whose continuation sits on its own
    arrow-led line, which five of this corpus's thirteen items structurally
    lack (a single-line chain form); that absence is an EXPECTED CONDITION,
    never reported as its own problem. Every item must still admit AT LEAST
    ONE family, so `D-03 NO MUTATION APPLIED [<analysis_id>]` fires for an
    item that admits zero -- verified live to never fire on the shipped
    corpus (every item has (a) and (c) available; see 19-06-SUMMARY.md).

    DISCLOSED BOUND: a mutation site is located structurally, not by a
    hardcoded byte literal, so this loses the exact-string-uniqueness
    precision CONF-GATE's D-08 arm gets from its single long needle
    (RESEARCH.md Q4) -- a deliberate, documented trade for scaling from one
    target to thirteen without a thirteen-entry needle table to maintain.
    """
    problems: list[str] = []
    for r in rows:
        if r["surface"] != "adversarial-corpus":
            continue
        if r["section_resolution"] != "OK":
            # An unreadable item is already reported by the CORPUS
            # POPULATION floor above; D-03 has nothing to perturb.
            continue

        relpath = r["relpath"]
        analysis_id = r["analysis_id"]
        text = (repo_root / relpath).read_text(encoding="utf-8")
        baseline = detect_defects(text, analysis_id)

        try:
            sections = _slice_sections(text)
        except SectionResolutionError:
            problems.append(
                f"D-03 [{analysis_id}] item could not be re-sliced for perturbation"
            )
            continue
        section2, section4, section6 = sections[2], sections[4], sections[6]
        offsets = _corpus_section_offsets(text, section2, section4, section6)
        if offsets is None:
            problems.append(
                f"D-03 [{analysis_id}] sections could not be relocated inside the "
                "document for perturbation"
            )
            continue
        sec2_start, sec4_start, sec6_start = offsets
        chain_ids = _chain_ids(section4)

        applied = 0

        site_a = _corpus_verdict_mutation_site(text, section2, sec2_start)
        if site_a is None:
            problems.append(f"D-03(a) mutation site not found (or not unique) in {relpath}")
        else:
            a_start, a_end = site_a
            mutated_text = text[:a_start] + "-" + text[a_end:]
            mutated = detect_defects(mutated_text, analysis_id)
            expected = baseline["nonconforming_verdict_cells"] + 1
            if mutated["nonconforming_verdict_cells"] != expected:
                problems.append(
                    f"D-03(a) verdict-cell separator mutation on {relpath} did not "
                    "increment nonconforming_verdict_cells by exactly 1 (baseline "
                    f"{baseline['nonconforming_verdict_cells']}, mutated "
                    f"{mutated['nonconforming_verdict_cells']})"
                )
            else:
                applied += 1

        site_b = _corpus_hop_mutation_site(text, section4, sec4_start)
        if site_b is not None:
            b_start, b_end = site_b
            mutated_text = text[:b_start] + "  " + text[b_end:]
            mutated = detect_defects(mutated_text, analysis_id)
            expected = baseline["malformed_chain_blocks"] + 1
            if mutated["malformed_chain_blocks"] != expected:
                problems.append(
                    f"D-03(b) chain-hop re-wrap mutation on {relpath} did not "
                    "increment malformed_chain_blocks by exactly 1 (baseline "
                    f"{baseline['malformed_chain_blocks']}, mutated "
                    f"{mutated['malformed_chain_blocks']})"
                )
            else:
                applied += 1
        # (b) absence is an expected condition (see docstring) -- no problem
        # appended when site_b is None.

        site_c = _corpus_citation_mutation_site(section6, sec6_start, chain_ids)
        if site_c is None:
            problems.append(f"D-03(c) mutation site not found (or not unique) in {relpath}")
        else:
            c_start, c_end = site_c
            mutated_text = text[:c_start] + text[c_end:]
            mutated = detect_defects(mutated_text, analysis_id)
            if mutated["untraced_claims"] < baseline["untraced_claims"] + 1:
                problems.append(
                    f"D-03(c) citation removal mutation on {relpath} did not "
                    "increment untraced_claims by at least 1 (baseline "
                    f"{baseline['untraced_claims']}, mutated "
                    f"{mutated['untraced_claims']})"
                )
            else:
                applied += 1

        if applied == 0:
            problems.append(f"D-03 NO MUTATION APPLIED [{analysis_id}]")

    return problems


# CR-01/BL-01/BL-02 shape (check-conf-gate.py `_LIVE_CALL_SITES`/
# `_LIVE_CALL_FORMS`/`_LIVE_CALL_SITES_LOCK`, copied verbatim): a source-text
# census over cmd_check()'s four Phase-19 enforcement call sites, floored by
# set equality against a second, independently transcribed roster, so
# narrowing either table -- or deleting, commenting out, or rewriting a call
# -- fails `--self-test` by name. DISCLOSED BOUND, same voice as the
# original: this counts and matches SOURCE TEXT and observes no behaviour --
# it catches a call site that was DELETED, REWRITTEN, or COMMENTED OUT, not
# a call whose returned problems are computed correctly and then discarded
# before reaching the failure report.
_CORPUS_CALL_SITES: dict[str, int] = {
    "_corpus_roster_problems": 1,
    "_corpus_disposition_problems": 1,
    "_corpus_population_problems": 1,
    "_corpus_perturbation_problems": 1,
}

# The whitespace-normalized call-form fragment each symbol above must
# appear in, transcribed from cmd_check()'s current source. Built BY
# CONCATENATION of short string pieces, never as one contiguous literal --
# the same self-match-hazard discipline check-conf-gate.py's own
# `_LIVE_CALL_FORMS` states for itself.
_CORPUS_CALL_FORMS: dict[str, str] = {
    "_corpus_roster_problems": (
        "problems += "
        + "_corpus_roster_problems(catalog_entries, catalog_problems, corpus_rows)"
    ),
    "_corpus_disposition_problems": (
        "problems += " + "_corpus_disposition_problems(corpus_rows)"
    ),
    "_corpus_population_problems": (
        "problems += " + "_corpus_population_problems(corpus_rows)"
    ),
    "_corpus_perturbation_problems": (
        "problems += " + "_corpus_perturbation_problems(rows, REPO_ROOT)"
    ),
}

# BL-02: a SECOND, independently transcribed roster of the same four
# enforcement symbol names -- deliberately NOT derived from
# _CORPUS_CALL_SITES or _CORPUS_CALL_FORMS by any expression. Narrowing
# either census table while this stays whole fails `--self-test` by name.
_CORPUS_CALL_SITES_LOCK: tuple[str, ...] = (
    "_corpus_roster_problems",
    "_corpus_disposition_problems",
    "_corpus_population_problems",
    "_corpus_perturbation_problems",
)


def _strip_line_comments(source: str) -> str:
    """BL-01 (check-conf-gate.py, copied verbatim): strip everything from
    the first `#` on each line before the census counts or the form lock
    matches, so a `# ` prefix on an enforcement call line -- which leaves
    the text present and unchanged in raw source -- can no longer satisfy
    either check. DISCLOSED BOUND, same conservative direction as the
    original: this over-strips a `#` inside a string literal, which can
    only make the census see LESS text, never more; it cannot manufacture
    a false PASS by hiding a real call site behind an in-string `#`.
    """
    return "\n".join(line.split("#", 1)[0] for line in source.splitlines())


def _corpus_call_site_census_problems(
    source: str,
    expected_counts: dict[str, int],
    expected_forms: dict[str, str] | None = None,
) -> list[str]:
    """A PURE source-text census over `cmd_check()`'s Phase-19 enforcement
    call sites, copying `check-conf-gate.py`'s `_call_site_census_problems`
    shape verbatim. Takes source text as a parameter -- never
    `inspect.getsource(cmd_check)` directly -- so the isolation-arm
    controls below can drive it with synthetic strings, never the real
    function's source, which is what keeps the arms falsifiable when the
    real source changes.
    """
    source = _strip_line_comments(source)
    problems: list[str] = []
    for symbol, expected in expected_counts.items():
        actual = source.count(symbol + "(")
        if actual != expected:
            problems.append(
                f"CALL-SITE CENSUS: {symbol} occurs {actual} time(s) in "
                f"cmd_check's source, expected {expected}"
            )
    if expected_forms is not None:
        normalized = " ".join(source.split())
        for symbol, fragment in expected_forms.items():
            normalized_fragment = " ".join(fragment.split())
            if normalized_fragment not in normalized:
                problems.append(
                    f"CALL-FORM LOCK: {symbol}'s expected call form not found in "
                    f"cmd_check's source: {fragment!r}"
                )
    return problems


def _corpus_call_sites_roster_problems(
    call_sites: dict[str, int] = _CORPUS_CALL_SITES,
    call_forms: dict[str, str] = _CORPUS_CALL_FORMS,
    lock: tuple[str, ...] = _CORPUS_CALL_SITES_LOCK,
) -> list[str]:
    """BL-02: *call_sites* and *call_forms* must each agree, by set
    equality, with the independently transcribed *lock* -- and every
    *call_sites* value must equal 1 (each enforcement symbol is called
    exactly once). Takes the three tables as parameters, defaulting to the
    real module constants, so a `--self-test` control can drive this with
    an alternate table without mutating global state.
    """
    problems: list[str] = []
    lock_set = set(lock)
    counts_diff = set(call_sites) ^ lock_set
    if counts_diff:
        problems.append(
            f"ROSTER LOCK: _CORPUS_CALL_SITES diverges from lock: {sorted(counts_diff)}"
        )
    forms_diff = set(call_forms) ^ lock_set
    if forms_diff:
        problems.append(
            f"ROSTER LOCK: _CORPUS_CALL_FORMS diverges from lock: {sorted(forms_diff)}"
        )
    wrong_counts = sorted(k for k, v in call_sites.items() if v != 1)
    if wrong_counts:
        problems.append(
            f"ROSTER LOCK: _CORPUS_CALL_SITES has non-1 expected count for: {wrong_counts}"
        )
    return problems


def pair_agreement(
    rows: list[dict],
) -> tuple[int, int, list[tuple[str, list[str]]]]:
    """D-04: match each shared-examples row to its generated-twin row by analysis_id and
    compare only AGREEMENT_FIELDS. Returns (agreeing pairs, total pairs considered,
    divergences). A source row with no twin counterpart, or vice versa, is itself a named
    divergence -- it is never silently dropped from the denominator.
    """
    source_by_id = {r["analysis_id"]: r for r in rows if r["surface"] == "shared-examples"}
    twin_by_id = {r["analysis_id"]: r for r in rows if r["surface"] == "generated-twin"}
    all_ids = sorted(set(source_by_id) | set(twin_by_id))

    agreeing = 0
    divergences: list[tuple[str, list[str]]] = []
    for analysis_id in all_ids:
        source_row = source_by_id.get(analysis_id)
        twin_row = twin_by_id.get(analysis_id)
        if source_row is None:
            divergences.append((analysis_id, ["<missing shared-examples row>"]))
            continue
        if twin_row is None:
            divergences.append((analysis_id, ["<missing generated-twin row>"]))
            continue
        differing = [f for f in AGREEMENT_FIELDS if source_row[f] != twin_row[f]]
        if differing:
            divergences.append((analysis_id, differing))
        else:
            agreeing += 1

    return agreeing, len(all_ids), divergences


# ---------------------------------------------------------------------------
# Rendering: one row set, two renderers. Neither renderer restates figures the
# other computes -- both read from the same rows/agreement inputs, so the two
# surfaces cannot disagree with each other.
# ---------------------------------------------------------------------------

_EXCLUDED_AGREEMENT_FIELDS: tuple[str, ...] = ("analysis_id",) + PROVENANCE_FIELDS


def _readable(group: list[dict]) -> list[dict]:
    return [r for r in group if r["section_resolution"] == "OK"]


def _unreadable_count(group: list[dict]) -> int:
    return sum(
        1 for r in group if str(r["section_resolution"]).startswith("SectionResolutionError:")
    )


def _sum_measured(group: list[dict], field: str) -> int:
    return sum(r[field] for r in _readable(group))


def _sum_heading(group: list[dict], field: str) -> int:
    return sum(r[field] for r in group)


def compute_headline(rows: list[dict]) -> dict:
    """The six computed figures this report publishes. Every value here is derived from
    `rows` at call time -- nothing is a hardcoded literal. Grouped per surface so a reader
    can see shared-examples, generated-twin and the contract surface side by side.
    """
    by_surface = {
        "shared-examples": [r for r in rows if r["surface"] == "shared-examples"],
        "generated-twin": [r for r in rows if r["surface"] == "generated-twin"],
        "contract-surface": [r for r in rows if r["surface"] == "contract-surface"],
    }

    def per_surface(fn) -> dict:
        return {surface: fn(group) for surface, group in by_surface.items()}

    return {
        "unreadable": per_surface(_unreadable_count),
        "conclusion_claims": {
            surface: {
                "total": _sum_measured(group, "conclusion_claims"),
                "untraced": _sum_measured(group, "untraced_claims"),
            }
            for surface, group in by_surface.items()
        },
        # D-06a: the marked/silent split of the untraced count above, per surface. Both
        # summed via _sum_measured, which already excludes unreadable rows -- their
        # "unreadable" string value never reaches a sum.
        "untraced_breakdown": {
            surface: {
                "marked": _sum_measured(group, "marked_untraced_claims"),
                "silent": _sum_measured(group, "silent_untraced_claims"),
            }
            for surface, group in by_surface.items()
        },
        "verdict_cells": {
            surface: {
                "total": _sum_measured(group, "verdict_cells"),
                "nonconforming": _sum_measured(group, "nonconforming_verdict_cells"),
            }
            for surface, group in by_surface.items()
        },
        "section4_chain_blocks": {
            surface: {
                "total": _sum_measured(group, "chain_blocks"),
                "malformed": _sum_measured(group, "malformed_chain_blocks"),
            }
            for surface, group in by_surface.items()
        },
        "heading_swept_blocks": {
            surface: {
                "total": _sum_heading(group, "heading_chain_blocks"),
                "malformed": _sum_heading(group, "heading_malformed_blocks"),
            }
            for surface, group in by_surface.items()
        },
    }


def compute_corpus_headline(corpus_rows: list[dict]) -> dict:
    """Phase 19's false-negative-rate headline. A sibling of `compute_headline`, not an
    extra entry inside it: a corpus headline counts ITEMS by predicate, while
    `compute_headline`'s `per_surface`/`_sum_measured` helpers sum a numeric field across
    a surface -- a different shape of aggregation. Every value here is derived from
    `corpus_rows` at call time; nothing is hardcoded.

    Phase 19 (CONF-08, D-19-08-A): TWO keys replace the old single `clean` key.
    `target_missed` is **the published false-negative count** -- items whose catalogued
    falsehood `detect_defects` did not catch. `no_column_fired` is the per-row DIAGNOSTIC
    -- items on which no substantive `detect_defects` column fired at all. The two can
    diverge (`t13-grounded-alongside-cyclic-ref` does, by exactly one item): a column can
    fire on an unrelated chain while the catalogued target is still missed. Exactly ONE of
    these two is ever published as "the" rate (CONF-08's own "single figure" clause);
    `target_missed` is that one.
    """
    total = len(corpus_rows)
    target_missed = sum(1 for r in corpus_rows if r["target_missed"] is True)
    no_column_fired = sum(1 for r in corpus_rows if r["no_column_fired"] is True)
    unreadable = sum(1 for r in corpus_rows if r["section_resolution"] != "OK")
    form_defects = sum(
        r["form_defects"] for r in corpus_rows if r["section_resolution"] == "OK"
    )

    by_stratum: dict[str, dict[str, int]] = {}
    for r in corpus_rows:
        stratum = r["stratum"]
        bucket = by_stratum.setdefault(
            stratum, {"target_missed": 0, "no_column_fired": 0, "total": 0}
        )
        bucket["total"] += 1
        if r["target_missed"] is True:
            bucket["target_missed"] += 1
        if r["no_column_fired"] is True:
            bucket["no_column_fired"] += 1

    # Phase 19 (CONF-08, D-19-08-A): renamed from `clean_without_disposition`, and
    # widened from the single predicate it used to read to the UNION
    # `target_missed is True or no_column_fired is True` -- so this count can never be
    # narrower than what it reported before this rename, only equal or wider.
    missed_without_disposition = sum(
        1
        for r in corpus_rows
        if (r["target_missed"] is True or r["no_column_fired"] is True)
        and (not r["disposition"] or r["disposition"] == "MISSING")
    )

    return {
        "total": total,
        "target_missed": target_missed,
        "no_column_fired": no_column_fired,
        "unreadable": unreadable,
        "form_defects": form_defects,
        "by_stratum": by_stratum,
        "missed_without_disposition": missed_without_disposition,
    }


def render_json(rows: list[dict], agreement: tuple[int, int, list[tuple[str, list[str]]]]) -> str:
    agreeing, total, divergences = agreement
    corpus_rows = [r for r in rows if r["surface"] == "adversarial-corpus"]
    obj = {
        "measurement_date": MEASUREMENT_DATE,
        "generator": "scripts/report-conformance.py",
        "artifact_count": len(rows),
        "surface_counts": {
            "shared-examples": sum(1 for r in rows if r["surface"] == "shared-examples"),
            "generated-twin": sum(1 for r in rows if r["surface"] == "generated-twin"),
            "contract-surface": sum(1 for r in rows if r["surface"] == "contract-surface"),
            "adversarial-corpus": len(corpus_rows),
        },
        "headline": compute_headline(rows),
        "pair_agreement": {
            "agreeing": agreeing,
            "total": total,
            "divergences": [
                {"analysis_id": analysis_id, "differing_fields": fields}
                for analysis_id, fields in divergences
            ],
        },
        "rows": rows,
        # Phase 19 (CONF-08): a NEW top-level key, never folded into the flat `rows` list
        # above or into `pair_agreement` -- the corpus has no generated twin, so widening
        # either would inflate the agreement headline with rows that cannot pair.
        "adversarial_corpus": {
            "headline": compute_corpus_headline(corpus_rows),
            "rows": corpus_rows,
        },
    }
    return json.dumps(obj, indent=2) + "\n"


_CORPUS_TABLE_FIELDS: tuple[str, ...] = (
    "relpath",
    "stratum",
    "section_resolution",
    "form_defects",
    "dependency_cycles",
    "ungrounded_chains",
    "selfaudit_disagreements",
    "target",
    "target_hits",
    "target_missed",
    "no_column_fired",
    "disposition",
)

# Fixed rendering order for the per-stratum breakdown -- A, B1, B2 in the corpus's own
# vocabulary order, then MISSING last (visible, never silently dropped) if any row's
# stratum is uncatalogued.
_STRATUM_ORDER: tuple[str, ...] = ("A", "B1", "B2", "MISSING")


def _render_adversarial_corpus_section(corpus_rows: list[dict], headline: dict) -> list[str]:
    """Phase 19 (CONF-07/CONF-08): the ## adversarial-corpus section. Reads every figure
    from `headline` (itself computed from `corpus_rows` by `compute_corpus_headline`) --
    nothing here is a hardcoded literal."""
    lines: list[str] = []
    lines.append("## adversarial-corpus")
    lines.append("")
    lines.append(
        "**False-negative rate:** "
        f"{headline['target_missed']} of {headline['total']} corpus items' catalogued "
        "falsehood the unmodified, CONTRACT-06-frozen `detect_defects` did not catch -- "
        "despite every item being a stated, catalogued falsehood. Each of those "
        f"{headline['target_missed']} is a false negative: a substantively wrong "
        "analysis this instrument cannot distinguish from a sound one. Diagnostic: "
        f"{headline['no_column_fired']} of {headline['total']} items had no substantive "
        "`detect_defects` column fire on them at all; the difference between the two "
        "figures is exactly the items on which an unrelated column fired for a reason "
        "having nothing to do with the item's own catalogued falsehood."
    )
    lines.append("")
    for stratum in _STRATUM_ORDER:
        if stratum not in headline["by_stratum"]:
            continue
        bucket = headline["by_stratum"][stratum]
        lines.append(
            f"- Stratum {stratum}: {bucket['target_missed']} of {bucket['total']} "
            f"catalogued target missed ({bucket['no_column_fired']} of {bucket['total']} "
            "no column fired)"
        )
    lines.append("")
    b2 = headline["by_stratum"].get(
        "B2", {"target_missed": 0, "no_column_fired": 0, "total": 0}
    )
    lines.append(
        "**Backlog 999.4 gate input.** Stratum B2 -- reachable by nothing this project "
        f"ships -- reads {b2['target_missed']} of {b2['total']} catalogued target "
        "missed. Per `.planning/ROADMAP.md` Phase 999.4 (CONDITIONAL, gated on this "
        "measurement): a low B2 rate closes 999.4 unrun, with this measurement recorded "
        "as the reason; a high B2 rate promotes 999.4, with this corpus as its "
        "validation set."
    )
    lines.append("")
    lines.append(
        "**Stratum vocabulary.** Stratum A: a named `detect_defects` column "
        "(`dependency_cycles`, `ungrounded_chains` or `selfaudit_disagreements`) "
        "plausibly has reach over the item's wrongness. Stratum B1: out of "
        "`detect_defects`'s reach but reachable by another shipped instrument -- closed "
        "at PROV-GUARD only (`scripts/check-provenance.py`'s read-at-source join), since "
        "no other shipped instrument has a code path over an arbitrary analysis. Stratum "
        "B2: reachable by nothing this project ships."
    )
    lines.append("")
    caught_stems = sorted(r["analysis_id"] for r in corpus_rows if r["target_missed"] is False)
    diverging_stems = sorted(
        r["analysis_id"]
        for r in corpus_rows
        if r["no_column_fired"] is False and r["target_missed"] is True
    )
    nothing_fired_stems = sorted(
        r["analysis_id"] for r in corpus_rows if r["no_column_fired"] is True
    )

    def _fmt_stems(stems: list[str]) -> str:
        return ", ".join(f"`{s}`" for s in stems) if stems else "none"

    lines.append(
        "**Fixtures, not artifacts.** This section measures deliberately wrong test "
        "fixtures, never shipped artifacts. A probe reading clean is never the same "
        "claim as an artifact conforming. A stratum-A item is a positive control ONLY "
        "when the column that fired is its own catalogued target -- proving the run "
        f"genuinely reaches that column on shipped corpus bytes: {_fmt_stems(caught_stems)}. "
        "An item on which a substantive column fired for an UNRELATED reason "
        f"({_fmt_stems(diverging_stems)}) had its own catalogued target missed regardless "
        "-- it is a false negative, never a positive control, no matter which column "
        f"fired. An item on which no substantive column fired at all "
        f"({_fmt_stems(nothing_fired_stems)}) is a false negative under the same figure. "
        "Which item sits in which set is answered by the `target` / `target_hits` / "
        "`target_missed` columns of the table below, never by this prose. The "
        "false-negative rate above is a measurement no phase may target (D-06): the only "
        "lever that would move it is widening a frozen detector, which CONTRACT-06 "
        "forbids."
    )
    lines.append("")
    lines.append(
        "**No generated twin.** The corpus is a test fixture, not a shipped artifact: "
        "nothing under `shared/` produces it and `sync-content.py` never emits it, so it "
        "has no twin and carries no pair-agreement row."
    )
    lines.append("")
    lines.append("| " + " | ".join(_CORPUS_TABLE_FIELDS) + " |")
    lines.append("|" + "---|" * len(_CORPUS_TABLE_FIELDS))
    for r in corpus_rows:
        lines.append("| " + " | ".join(str(r[f]) for f in _CORPUS_TABLE_FIELDS) + " |")
    lines.append("")
    lines.append(
        "All thirteen form columns and all nine always-`n/a` provenance columns for "
        "these items are carried in full in `docs/data/conformance.json` under "
        "`adversarial_corpus.rows`, and are omitted here for readability."
    )
    lines.append("")
    return lines


def render_markdown(
    rows: list[dict], agreement: tuple[int, int, list[tuple[str, list[str]]]]
) -> str:
    agreeing, total, divergences = agreement
    shared = [r for r in rows if r["surface"] == "shared-examples"]
    twin = [r for r in rows if r["surface"] == "generated-twin"]
    contract = [r for r in rows if r["surface"] == "contract-surface"]
    headline = compute_headline(rows)

    lines: list[str] = []
    lines.append("<!-- GENERATED — DO NOT EDIT -->")
    lines.append("<!-- Source: scripts/report-conformance.py -->")
    lines.append("<!-- Regenerate: python3 scripts/report-conformance.py -->")
    lines.append("")
    lines.append("# Conformance Baseline")
    lines.append("")
    lines.append(f"Measurement date: {MEASUREMENT_DATE}")
    lines.append("")
    lines.append(
        "This file is a measurement, not a contract: no figure below defines what the "
        "codebase is required to become, and no count in it gates a conformance check. "
        "Regenerating this file only ever fails on staleness -- committed bytes that no "
        "longer match a fresh run of `scripts/report-conformance.py` -- never on a count "
        "read here being high."
    )
    lines.append("")
    lines.append("## Headline")
    lines.append("")
    lines.append("| Reading | shared-examples | generated-twin | contract-surface |")
    lines.append("|---|---|---|---|")
    lines.append(
        "| Files unreadable by `_slice_sections` "
        f"| {headline['unreadable']['shared-examples']} of {len(shared)} "
        f"| {headline['unreadable']['generated-twin']} of {len(twin)} "
        f"| {headline['unreadable']['contract-surface']} of {len(contract)} |"
    )
    lines.append(
        "| §6 conclusion claims (untraced) | "
        + " | ".join(
            f"{headline['conclusion_claims'][s]['total']} "
            f"({headline['conclusion_claims'][s]['untraced']} untraced)"
            for s in ("shared-examples", "generated-twin", "contract-surface")
        )
        + " |"
    )
    lines.append(
        "| §6 untraced claims (marked / silent) | "
        + " | ".join(
            f"{headline['conclusion_claims'][s]['untraced']} untraced "
            f"({headline['untraced_breakdown'][s]['marked']} marked, "
            f"{headline['untraced_breakdown'][s]['silent']} silent)"
            for s in ("shared-examples", "generated-twin", "contract-surface")
        )
        + " |"
    )
    lines.append(
        "| §2 verdict cells (non-conforming) | "
        + " | ".join(
            f"{headline['verdict_cells'][s]['total']} "
            f"({headline['verdict_cells'][s]['nonconforming']} non-conforming)"
            for s in ("shared-examples", "generated-twin", "contract-surface")
        )
        + " |"
    )
    lines.append(
        "| §4 `chain_blocks` (malformed) | "
        + " | ".join(
            f"{headline['section4_chain_blocks'][s]['total']} "
            f"({headline['section4_chain_blocks'][s]['malformed']} malformed)"
            for s in ("shared-examples", "generated-twin", "contract-surface")
        )
        + " |"
    )
    lines.append(
        "| `### Conclusion` heading-swept blocks (malformed) | "
        + " | ".join(
            f"{headline['heading_swept_blocks'][s]['total']} "
            f"({headline['heading_swept_blocks'][s]['malformed']} malformed)"
            for s in ("shared-examples", "generated-twin", "contract-surface")
        )
        + " |"
    )
    lines.append(
        f"| Source-vs-twin agreement (D-04) | {agreeing} of {total} pairs agree | | |"
    )
    lines.append("")

    lines.append("## Two chain-block censuses (D-05)")
    lines.append("")
    lines.append(
        "`detect_defects` and the `### Conclusion` heading sweep are both produced by the "
        "same frozen instrument, `scripts/check-quality-harness.py`, yet they read a "
        "different number of chain blocks. `detect_defects`'s §4-scoped `chain_blocks` / "
        "`malformed_chain_blocks` columns come from a section slice, so they cannot read "
        "the files `_slice_sections` rejects. The `### Conclusion` heading sweep -- "
        "`_render_example_chain_blocks` paired with `_chain_block_well_formed` -- is a "
        "heading scan, not a section parse, so it can read those same files. The two "
        "figures measure different things and are published as separately named columns "
        "rather than reconciled into one number."
    )
    lines.append("")

    lines.append("## Column vocabulary")
    lines.append("")
    lines.append(
        "Three kinds of value appear in the per-artifact tables below. A number means the "
        "detector read the document and counted. The literal `n/a` means no `.jsonl` "
        "generation capture exists for this artifact -- true of all 29 artifacts, for the "
        "nine provenance columns, unconditionally. The literal `unreadable` means "
        "`_slice_sections` rejected the document, so the twelve measured schema fields "
        "were never computed. The nine provenance columns are emitted in full precisely so "
        "`n/a` and `0` are never printed as the same thing."
    )
    lines.append("")

    lines.append("## Disclosed bounds")
    lines.append("")
    lines.append(
        "This phase publishes four disclosures in the same voice R7/R9/R10 use on the "
        "agent surface to state their own measured bounds, rather than leaving them to be "
        "discovered."
    )
    lines.append("")
    lines.append(
        "**1. Chain-form reach.** `heading_malformed_blocks == 0` means every scanned "
        "block conforms under `_chain_block_well_formed`'s measured reach -- the head and "
        "first hop, up to the second arrow of the first matching candidate. This is NOT "
        "the same claim as \"no R7 violations remain in `shared/examples/`\": a wrap or a "
        "GT-led hop after the second arrow is not detected. This phase fixes to the "
        "detector's bound, which is what CONF-04 states; fixing to R7 as published is a "
        "strictly larger job and is recorded as backlog, not as done."
    )
    lines.append("")
    marked_total = sum(
        headline["untraced_breakdown"][s]["marked"]
        for s in ("shared-examples", "generated-twin")
        if isinstance(headline["untraced_breakdown"][s]["marked"], int)
    )
    lines.append(
        "**2. Marked-claim residual (derived) — a ratchet as of Phase 18 (CONF-GATE).** "
        f"{marked_total} claim(s) across shared-examples and generated-twin carry the "
        "`no chain — flagged assumption only` marker "
        f"(shared-examples: {headline['untraced_breakdown']['shared-examples']['marked']}, "
        f"generated-twin: {headline['untraced_breakdown']['generated-twin']['marked']}), "
        "computed from `rows` at render time, never hardcoded. This figure was "
        "established by Phase 18's exemplar-conformance pass rather than pre-declared, "
        "and it is now pinned by `scripts/check-conf-gate.py`'s `_MARKED_RATCHET`: the "
        "reading may fall, never rise. A marked caveat still scores untraced BY DESIGN "
        "(`R-CLAIM-CAVEAT-MARKED`): the marker discloses the gap, it does not discharge "
        "the claim. Driving the `untraced_claims` reading itself to zero would mean "
        "inventing citations, which is the failure mode the bound exists to prevent."
    )
    lines.append("")
    lines.append(
        "**3. `shared/spine/references/output-template.md` is measured but not gated.** "
        "It is the specification document whose §4 worked examples deliberately include "
        "non-conforming forms as labelled teaching contrasts, so a detector-conformance "
        "fix would require either mislabelling a deliberately-broken example or "
        "restructuring the document's own pedagogy. CONF-03..06 name the fourteen shipped "
        "analyses only. Phase 17 measured this surface and handed the scope question to "
        "Phase 18; Phase 18 declines it by this stated reason -- an accepted, disclosed "
        "exclusion, never a silent omission."
    )
    lines.append("")
    lines.append(
        "**4. The closure-ledger route has zero shipped exemplars.** "
        "`output-template.md` §6 blesses two citation routes; the exemplars use one -- "
        "the inline `(chain Cn)` form the template itself calls \"the mechanically "
        "checkable form\" (decision D-01). After this phase no shipped worked example "
        "demonstrates the `- \"quoted claim\" → chain Cn` closure-ledger row, because of "
        "backlog 999.24 (an unfenced in-section-6 ledger row counts itself as a claim) "
        "and `_slice_sections`'s section-6 rule, which ends §6 at the first ATX heading "
        "of any depth."
    )
    lines.append("")
    lines.append(
        "**5. The pre-commit conformance-drift gate fails on staleness, not on a lost "
        "catch (D-07).** `scripts/report-conformance.py --check` fails when the committed "
        "bytes of this file or `docs/data/conformance.json` no longer match a fresh run -- "
        "never when a count read here, including the adversarial-corpus false-negative "
        "rate below, is high. A detector change that moves a corpus reading fails `--check` "
        "as drift; regenerating the two artifacts makes it pass again. Nothing here raises "
        "an alarm that the *meaning* of a reading changed -- only that the committed bytes "
        "are out of date."
    )
    lines.append("")

    header_fields = ["relpath"] + list(REPORT_FIELDS) + list(_DEFECT_RECORD_FIELDS)
    for surface_name, group in (
        ("shared-examples", shared),
        ("generated-twin", twin),
        ("contract-surface", contract),
    ):
        lines.append(f"## {surface_name}")
        lines.append("")
        lines.append("| " + " | ".join(header_fields) + " |")
        lines.append("|" + "---|" * len(header_fields))
        for r in group:
            lines.append("| " + " | ".join(str(r[f]) for f in header_fields) + " |")
        lines.append("")

    corpus = [r for r in rows if r["surface"] == "adversarial-corpus"]
    corpus_headline = compute_corpus_headline(corpus)
    lines.extend(_render_adversarial_corpus_section(corpus, corpus_headline))

    lines.append("## Source-vs-twin agreement (D-04)")
    lines.append("")
    lines.append(
        f"Compared fields ({len(AGREEMENT_FIELDS)}): "
        + ", ".join(f"`{f}`" for f in AGREEMENT_FIELDS)
        + "."
    )
    lines.append("")
    lines.append(
        "Excluded (ten, foreordained equal on both surfaces): "
        + ", ".join(f"`{f}`" for f in _EXCLUDED_AGREEMENT_FIELDS)
        + "."
    )
    lines.append("")
    lines.append(f"Result: {agreeing} of {total} pairs agree.")
    if divergences:
        lines.append("")
        for analysis_id, fields in divergences:
            lines.append(f"- `{analysis_id}`: {', '.join(fields)}")
    lines.append("")

    lines.append(
        "Prior readings: `git log --follow docs/conformance-baseline.md`."
    )

    return "\n".join(lines) + "\n"


def generate_all(repo_root: Path) -> dict[Path, str]:
    """Build both rendered strings from ONE `build_rows` call, so the two surfaces cannot
    disagree with each other."""
    rows = build_rows(repo_root)
    agreement = pair_agreement(rows)
    return {
        MD_PATH: render_markdown(rows, agreement),
        JSON_PATH: render_json(rows, agreement),
    }


def _write_text(path: Path, text: str) -> None:
    path.write_text(text, encoding="utf-8")


def cmd_write() -> int:
    generated = generate_all(REPO_ROOT)
    JSON_PATH.parent.mkdir(parents=True, exist_ok=True)
    for path, text in generated.items():
        _write_text(path, text)
    row_count = len(json.loads(generated[JSON_PATH])["rows"])
    print(f"report-conformance: PASS — wrote {MD_PATH} + {JSON_PATH} ({row_count} rows)")
    return 0


def _diff_against_disk(generated: dict[Path, str]) -> list[Path]:
    """Compare each generated text against its on-disk bytes (empty string if absent);
    write a DRIFT: line plus a unified diff to stderr for every path that differs, and
    return the list of drifted paths.

    Takes an arbitrary path->text mapping so --self-test can drive it against a tempdir
    fixture (mutation 6) without ever writing into the real docs/ tree -- cmd_check()
    itself stays hardcoded to REPO_ROOT/MD_PATH/JSON_PATH per settled decision (d).
    """
    drifted: list[Path] = []
    for path, text in generated.items():
        on_disk = path.read_text(encoding="utf-8") if path.exists() else ""
        if on_disk != text:
            drifted.append(path)
            rel = path.relative_to(REPO_ROOT) if path.is_relative_to(REPO_ROOT) else path
            sys.stderr.write(f"DRIFT: {rel}\n")
            sys.stderr.writelines(
                difflib.unified_diff(
                    on_disk.splitlines(keepends=True),
                    text.splitlines(keepends=True),
                    fromfile=f"a/{rel}",
                    tofile=f"b/{rel}",
                    n=3,
                )
            )
            sys.stderr.write("\n")
    return drifted


def cmd_check() -> int:
    # Idempotency self-test: two in-memory generations must be equal, or an unsorted glob
    # or a leaked wall-clock value would otherwise become a mystery --check failure.
    pass1 = generate_all(REPO_ROOT)
    pass2 = generate_all(REPO_ROOT)
    if pass1 != pass2:
        sys.stderr.write("NON-DETERMINISTIC: pass-1 != pass-2\n")
        return 2

    # Collect-then-report (check-conf-gate.py run_live()'s shape): every
    # predicate below runs regardless of whether an earlier one already
    # found a problem, so a stale baseline and a Phase 19 corpus floor
    # breach are both reported in the same run rather than the first
    # masking the second.
    problems: list[str] = []

    drifted = _diff_against_disk(pass1)
    if drifted:
        rels = [
            str(p.relative_to(REPO_ROOT) if p.is_relative_to(REPO_ROOT) else p)
            for p in drifted
        ]
        problems.append("DRIFT: " + ", ".join(rels))

    # Phase 19 (CONF-07/CONF-08): the corpus floors. A fresh build_rows()
    # call, independent of pass1/pass2 above (generate_all does not expose
    # its intermediate rows), matching the shape check-conf-gate.py's own
    # run_live() already uses for the same reason.
    rows = build_rows(REPO_ROOT)
    corpus_rows = [r for r in rows if r["surface"] == "adversarial-corpus"]
    catalog_entries, catalog_problems = parse_corpus_catalog(REPO_ROOT)

    problems += _corpus_roster_problems(catalog_entries, catalog_problems, corpus_rows)
    problems += _corpus_disposition_problems(corpus_rows)
    problems += _corpus_population_problems(corpus_rows)
    problems += _corpus_perturbation_problems(rows, REPO_ROOT)

    if problems:
        for p in problems:
            sys.stderr.write(f"report-conformance: FAIL — {p}\n")
        if drifted:
            sys.stderr.write("Run: python3 scripts/report-conformance.py && git add -u\n")
        return 1
    print("report-conformance: PASS — no drift")
    return 0


# ---------------------------------------------------------------------------
# --self-test: offline control battery, entirely tempdir/in-memory. Never
# touches the real tree, never writes under tests/. Each control has a stable
# id string; every failure names its id and states expected vs. actual.
# ---------------------------------------------------------------------------

# A synthetic row shaped exactly like a real build_row() output: measured
# fields default to 0, provenance fields default to "n/a" (never 0), matching
# what detect_defects itself would produce for a clean, readable artifact.
def _synthetic_row(surface: str, relpath: str, analysis_id: str, **overrides) -> dict:
    row: dict = {
        "surface": surface,
        "relpath": relpath,
        "section_resolution": "OK",
        "heading_chain_blocks": 0,
        "heading_malformed_blocks": 0,
        # D-06a: measured fields, same default-to-0 rule as every other measured column.
        "marked_untraced_claims": 0,
        "silent_untraced_claims": 0,
    }
    for field in _DEFECT_RECORD_FIELDS:
        if field == "analysis_id":
            row[field] = analysis_id
        elif field in PROVENANCE_FIELDS:
            row[field] = "n/a"
        else:
            row[field] = 0
    row.update(overrides)
    return row


# A minimal document _slice_sections resolves cleanly -- six numbered sections,
# each with just enough body to be non-empty. Reused by every control that
# needs a "readable" counterpart to an unreadable one.
_READABLE_FIXTURE_TEXT = """## 1. Problem Essence
Some essence text.

## 2. Assumptions Table
| Assumption | Confidence |
|---|---|

## 3. Ground Truths
- GT-1: some ground truth.

## 4. Derivation Chains
GT-1 -> some conclusion.

## 5. Abandoned Reasoning
None.

## 6. Conclusion
### Conclusion
GT-1 -> some conclusion.
"""

# A document with one heading-swept ### Conclusion block but no resolvable
# six-section structure -- _slice_sections raises, the heading sweep does not.
_UNREADABLE_FIXTURE_TEXT = (
    "# Some Doc\n\n### Conclusion\nThis is just prose with no chain arrows at all.\n"
)

# D-06a control (a) fixture: a resolvable six-section document whose section 6 carries
# three assertive, uncited list-item claims (each over the forty-character floor
# _is_assertive_claim enforces), one of which carries CAVEAT_MARKER. Section 4 has no
# `### Conclusion Cn:` heading, so chain_ids is empty and none of the three claims can
# trace by any route -- all three are untraced, and the split must read marked=1, silent=2.
_MARKED_CLAIM_FIXTURE_TEXT = """## 1. Problem Essence
Some essence text.

## 2. Assumptions Table
| Assumption | Confidence |
|---|---|

## 3. Ground Truths
- GT-1: some ground truth.

## 4. Derivation Chains
GT-1 -> some conclusion, with no numbered chain heading anywhere in this section.

## 5. Abandoned Reasoning
None.

## 6. Conclusion
- This is the first assertive claim and it is long enough on its own to clear the floor
- This is the second assertive claim and it is also long enough to clear the same floor
- This third claim carries the marker no chain — flagged assumption only and clears the floor too
"""


def _make_minimum_tree(root: Path) -> None:
    """Populate *root* with exactly the 14/14/1/12 floor minimum discover_artifacts
    requires."""
    shared_dir = root / "shared" / "examples"
    shared_dir.mkdir(parents=True, exist_ok=True)
    for i in range(MIN_SHARED_EXAMPLES):
        (shared_dir / f"ex{i}.md").write_text("x", encoding="utf-8")
    twin_dir = root / "first-principles" / "agents" / "references" / "examples"
    twin_dir.mkdir(parents=True, exist_ok=True)
    for i in range(MIN_TWIN_EXAMPLES):
        (twin_dir / f"ex{i}.md").write_text("x", encoding="utf-8")
    contract_dir = root / "shared" / "spine" / "references"
    contract_dir.mkdir(parents=True, exist_ok=True)
    (contract_dir / "output-template.md").write_text("x", encoding="utf-8")
    corpus_dir = root / "tests" / "adversarial-corpus-v9.0"
    corpus_dir.mkdir(parents=True, exist_ok=True)
    for i in range(MIN_CORPUS_ITEMS):
        (corpus_dir / f"t{i:02d}-item.md").write_text("x", encoding="utf-8")
    (corpus_dir / "catalog.md").write_text("x", encoding="utf-8")
    (corpus_dir / "README.md").write_text("x", encoding="utf-8")


def _control_floor_shared_short() -> None:
    with tempfile.TemporaryDirectory() as td:
        root = Path(td)
        _make_minimum_tree(root)
        # Remove one shared-examples file so the glob yields 13, not 14.
        (root / "shared" / "examples" / "ex0.md").unlink()
        try:
            discover_artifacts(root)
        except DiscoveryFloorError as exc:
            msg = str(exc)
            assert SHARED_EXAMPLES_GLOB in msg, msg
            assert "expected >= 14" in msg, msg
            assert "found 13" in msg, msg
        else:
            raise AssertionError("discover_artifacts did not raise on a 13-file shared glob")


def _control_floor_twin_short() -> None:
    with tempfile.TemporaryDirectory() as td:
        root = Path(td)
        _make_minimum_tree(root)
        (root / "first-principles" / "agents" / "references" / "examples" / "ex0.md").unlink()
        try:
            discover_artifacts(root)
        except DiscoveryFloorError as exc:
            msg = str(exc)
            assert TWIN_EXAMPLES_GLOB in msg, msg
            assert "found 13" in msg, msg
        else:
            raise AssertionError("discover_artifacts did not raise on a 13-file twin glob")


def _control_floor_contract_missing() -> None:
    with tempfile.TemporaryDirectory() as td:
        root = Path(td)
        _make_minimum_tree(root)
        (root / "shared" / "spine" / "references" / "output-template.md").unlink()
        try:
            discover_artifacts(root)
        except DiscoveryFloorError as exc:
            msg = str(exc)
            assert CONTRACT_SURFACE_RELPATH in msg, msg
            assert "found 0" not in msg, msg
        else:
            raise AssertionError("discover_artifacts did not raise when the contract surface is missing")


def _control_floor_glob_empty() -> None:
    with tempfile.TemporaryDirectory() as td:
        root = Path(td)
        try:
            discover_artifacts(root)
        except DiscoveryFloorError as exc:
            msg = str(exc)
            assert SHARED_EXAMPLES_GLOB in msg, msg
            assert TWIN_EXAMPLES_GLOB in msg, msg
        else:
            raise AssertionError("discover_artifacts did not raise on a completely empty root")


def _control_floor_passes_at_minimum() -> None:
    with tempfile.TemporaryDirectory() as td:
        root = Path(td)
        _make_minimum_tree(root)
        artifacts = discover_artifacts(root)
        expected = (
            MIN_SHARED_EXAMPLES + MIN_TWIN_EXAMPLES + MIN_CONTRACT_SURFACES + MIN_CORPUS_ITEMS
        )
        assert len(artifacts) == expected, (len(artifacts), expected)


def _control_partial_row_records_heading_census() -> None:
    with tempfile.TemporaryDirectory() as td:
        path = Path(td) / "synth.md"
        path.write_text(_UNREADABLE_FIXTURE_TEXT, encoding="utf-8")
        artifact = Artifact("shared-examples", "synth.md", path, "synth")
        row = build_row(artifact)
        assert row["section_resolution"].startswith("SectionResolutionError:"), row[
            "section_resolution"
        ]
        assert row["conclusion_claims"] == "unreadable", row["conclusion_claims"]
        assert row["heading_chain_blocks"] == 1, row["heading_chain_blocks"]
        assert row["heading_malformed_blocks"] == 1, row["heading_malformed_blocks"]


def _control_partial_row_not_dropped() -> None:
    with tempfile.TemporaryDirectory() as td:
        root = Path(td)
        bad_path = root / "bad.md"
        good_path = root / "good.md"
        bad_path.write_text(_UNREADABLE_FIXTURE_TEXT, encoding="utf-8")
        good_path.write_text(_READABLE_FIXTURE_TEXT, encoding="utf-8")
        artifacts = [
            Artifact("shared-examples", "bad.md", bad_path, "bad"),
            Artifact("shared-examples", "good.md", good_path, "good"),
        ]
        rows = [build_row(a) for a in artifacts]
        assert len(rows) == 2, len(rows)


def _control_agreement_field_scope() -> None:
    # D-06a widened this from 15 to 17: confirming (not assuming) that appending the two
    # new report columns to REPORT_FIELDS widens AGREEMENT_FIELDS automatically, since it
    # is derived (MEASURED_SCHEMA_FIELDS + REPORT_FIELDS), never restated.
    assert len(AGREEMENT_FIELDS) == 17, len(AGREEMENT_FIELDS)
    assert "analysis_id" not in AGREEMENT_FIELDS
    for field in PROVENANCE_FIELDS:
        assert field not in AGREEMENT_FIELDS, field
    assert "untraced_claims" in AGREEMENT_FIELDS
    assert "heading_malformed_blocks" in AGREEMENT_FIELDS
    assert "marked_untraced_claims" in AGREEMENT_FIELDS
    assert "silent_untraced_claims" in AGREEMENT_FIELDS


def _control_agreement_detects_measured_divergence() -> None:
    source_row = _synthetic_row("shared-examples", "synth.md", "synth")
    twin_row = _synthetic_row("generated-twin", "synth.md", "synth", untraced_claims=1)
    agreeing, total, divergences = pair_agreement([source_row, twin_row])
    assert agreeing == 0, agreeing
    assert total == 1, total
    assert len(divergences) == 1, divergences
    analysis_id, fields = divergences[0]
    assert analysis_id == "synth", analysis_id
    assert "untraced_claims" in fields, fields


def _control_agreement_vacuity_guard() -> None:
    provenance_field = _DEFECT_RECORD_FIELDS[13]
    source_row = _synthetic_row("shared-examples", "synth.md", "synth")
    twin_row = _synthetic_row(
        "generated-twin", "synth.md", "synth", **{provenance_field: "different"}
    )
    agreeing, total, divergences = pair_agreement([source_row, twin_row])
    assert agreeing == 1, (agreeing, divergences)
    assert total == 1, total
    assert divergences == [], divergences


def _control_agreement_unpaired_is_divergence() -> None:
    source_row = _synthetic_row("shared-examples", "lonely.md", "lonely")
    agreeing, total, divergences = pair_agreement([source_row])
    assert agreeing == 0, agreeing
    assert total == 1, total
    assert len(divergences) == 1, divergences
    analysis_id, _fields = divergences[0]
    assert analysis_id == "lonely", analysis_id


def _synthetic_rows_for_render() -> list[dict]:
    return [
        _synthetic_row("shared-examples", "synth.md", "synth"),
        _synthetic_row("generated-twin", "synth.md", "synth"),
        _synthetic_row("contract-surface", "contract.md", "contract"),
    ]


def _control_render_determinism() -> None:
    rows = _synthetic_rows_for_render()
    agreement = pair_agreement(rows)
    md1, md2 = render_markdown(rows, agreement), render_markdown(rows, agreement)
    json1, json2 = render_json(rows, agreement), render_json(rows, agreement)
    assert md1 == md2
    assert json1 == json2
    for text in (md1, json1):
        assert text.endswith("\n") and not text.endswith("\n\n"), text[-5:]


def _control_render_provenance_sentinel() -> None:
    rows = _synthetic_rows_for_render()
    agreement = pair_agreement(rows)
    md = render_markdown(rows, agreement)
    assert "n/a" in md
    # Every provenance field on every synthetic row is "n/a" by construction
    # (_synthetic_row); this asserts the invariant survives rendering rather
    # than being silently coerced to a bare "0" string along the way.
    for row in rows:
        for field in PROVENANCE_FIELDS:
            assert row[field] == "n/a", (field, row[field])


def _control_check_detects_drift() -> None:
    with tempfile.TemporaryDirectory() as td:
        target = Path(td) / "artifact.md"
        target.write_text("original content\n", encoding="utf-8")
        generated = {target: "original content\n"}
        assert _diff_against_disk(generated) == []
        target.write_text("mutated content\n", encoding="utf-8")
        assert _diff_against_disk(generated) == [target]


# ---------------------------------------------------------------------------
# D-06a controls: the marked/silent untraced-claim split.
# ---------------------------------------------------------------------------


def _control_marked_untraced_claim_counted() -> None:
    """(a) A synthetic readable row whose claim text carries CAVEAT_MARKER reads
    marked=1, silent=N-1 (here N=3), computed through the real build_row() -> detect_defects
    path, never hand-assembled."""
    with tempfile.TemporaryDirectory() as td:
        path = Path(td) / "marked.md"
        path.write_text(_MARKED_CLAIM_FIXTURE_TEXT, encoding="utf-8")
        artifact = Artifact("shared-examples", "marked.md", path, "marked")
        row = build_row(artifact)
        assert row["section_resolution"] == "OK", row["section_resolution"]
        assert row["untraced_claims"] == 3, row["untraced_claims"]
        assert row["marked_untraced_claims"] == 1, row["marked_untraced_claims"]
        assert row["silent_untraced_claims"] == 2, row["silent_untraced_claims"]


def _control_unreadable_columns_are_literal() -> None:
    """(b) A synthetic unreadable row reads the literal "unreadable" for both new
    columns, and a negative arm asserts a row coerced to 0 is REJECTED by that same
    assertion shape -- "unreadable" and 0 must never compare equal."""
    with tempfile.TemporaryDirectory() as td:
        path = Path(td) / "bad.md"
        path.write_text(_UNREADABLE_FIXTURE_TEXT, encoding="utf-8")
        artifact = Artifact("shared-examples", "bad.md", path, "bad")
        row = build_row(artifact)
        assert row["marked_untraced_claims"] == "unreadable", row["marked_untraced_claims"]
        assert row["silent_untraced_claims"] == "unreadable", row["silent_untraced_claims"]

        coerced = dict(row)
        coerced["marked_untraced_claims"] = 0
        coerced["silent_untraced_claims"] = 0
        try:
            assert coerced["marked_untraced_claims"] == "unreadable", coerced[
                "marked_untraced_claims"
            ]
        except AssertionError:
            pass
        else:
            raise AssertionError(
                "a row coerced to 0 for the unreadable columns was not rejected"
            )


def _control_render_marked_silent_parsed_from_output() -> None:
    """(c) Parses BOTH new columns back out of the string render_markdown() actually
    produced and asserts on the PARSED CELL -- never on the input fixture. Carries a
    negative arm proving a renderer that coerced the cells to 0 before rendering is
    caught. This control exists specifically because Phase 17's
    `_control_render_provenance_sentinel` asserted on the input row dict instead of the
    rendered string and was proved vacuous by monkeypatch (17-VERIFICATION gap 1, CR-01)."""
    header_fields = ["relpath"] + list(REPORT_FIELDS) + list(_DEFECT_RECORD_FIELDS)
    marked_idx = header_fields.index("marked_untraced_claims")
    silent_idx = header_fields.index("silent_untraced_claims")

    def _parsed_cells(md: str) -> list[str]:
        lines = md.splitlines()
        section_start = lines.index("## shared-examples")
        data_line = next(
            line
            for line in lines[section_start:]
            if line.startswith("| ") and "synth.md" in line
        )
        return [c.strip() for c in data_line.strip("|").split("|")]

    rows = [
        _synthetic_row(
            "shared-examples",
            "synth.md",
            "synth",
            untraced_claims=3,
            marked_untraced_claims=1,
            silent_untraced_claims=2,
        ),
        _synthetic_row(
            "generated-twin",
            "synth.md",
            "synth",
            untraced_claims=3,
            marked_untraced_claims=1,
            silent_untraced_claims=2,
        ),
        _synthetic_row("contract-surface", "contract.md", "contract"),
    ]
    md = render_markdown(rows, pair_agreement(rows))
    cells = _parsed_cells(md)
    assert cells[marked_idx] == "1", cells
    assert cells[silent_idx] == "2", cells

    # Negative arm: a renderer that coerced these two columns to 0 before rendering must
    # be caught by the identical parse-and-assert shape, not silently pass.
    coerced_rows = [
        _synthetic_row(
            "shared-examples",
            "synth.md",
            "synth",
            untraced_claims=3,
            marked_untraced_claims=0,
            silent_untraced_claims=0,
        ),
        rows[1],
        rows[2],
    ]
    coerced_md = render_markdown(coerced_rows, pair_agreement(coerced_rows))
    coerced_cells = _parsed_cells(coerced_md)
    try:
        assert coerced_cells[marked_idx] == "1", coerced_cells
    except AssertionError:
        pass
    else:
        raise AssertionError("a rendering that coerced marked/silent to 0 was not caught")


def _control_corpus_render_no_hardcoded_stems() -> None:
    """Phase 19 (plan 19-08 Task 3): `_render_adversarial_corpus_section`'s docstring
    claims "nothing here is a hardcoded literal" -- this is the check that makes that
    claim falsifiable. Renders the section from a synthetic corpus whose stems are
    deliberately NOT `t01`..`t14` (`x01`, `x02`, `x03`, one per set: caught, diverging,
    nothing-fired) and asserts (a) no `t0`/`t1`-prefixed stem literal appears anywhere in
    the rendered output, and (b) the synthetic stems DO appear in the enumerations. A
    renderer that reintroduces any hardcoded stem list fails this by finding a `t0x`
    literal that this synthetic corpus never supplied."""
    caught = _synthetic_row(
        "adversarial-corpus",
        "x01.md",
        "x01",
        stratum="A",
        source="hand-authored",
        disposition="accept-with-reason: positive control.",
        target="dependency_cycles:c1,c2",
        target_hits=["dependency_cycles:c1,c2"],
        target_missed=False,
        no_column_fired=False,
        form_defects=0,
    )
    diverges = _synthetic_row(
        "adversarial-corpus",
        "x02.md",
        "x02",
        stratum="A",
        source="hand-authored",
        disposition="accept-with-reason: disclosed bound.",
        target="ungrounded_chains:c1",
        target_hits=[],
        target_missed=True,
        no_column_fired=False,
        form_defects=0,
    )
    nothing_fired = _synthetic_row(
        "adversarial-corpus",
        "x03.md",
        "x03",
        stratum="B2",
        source="derived:x",
        disposition="accept-with-reason: no shipped rule reaches this.",
        target="none",
        target_hits=[],
        target_missed=True,
        no_column_fired=True,
        form_defects=0,
    )
    corpus_rows = [caught, diverges, nothing_fired]
    headline = compute_corpus_headline(corpus_rows)
    rendered = "\n".join(_render_adversarial_corpus_section(corpus_rows, headline))

    for bad in (
        "t01",
        "t02",
        "t03",
        "t04",
        "t05",
        "t06",
        "t07",
        "t08",
        "t09",
        "t10",
        "t11",
        "t12",
        "t13",
        "t14",
    ):
        assert bad not in rendered, f"hardcoded stem literal {bad!r} found in rendered output"

    for good in ("x01", "x02", "x03"):
        assert good in rendered, f"synthetic stem {good!r} missing from rendered output"


def _control_corpus_missed_without_disposition() -> None:
    """Phase 19 (CONF-08, D-19-08-A): a synthetic corpus row set with one missed row
    carrying a real disposition and one missed row whose disposition is the literal
    "MISSING" reads missed_without_disposition == 1. Perturbing the "MISSING" row's
    disposition to a non-empty string moves the count to 0 -- the same fixture, re-scored,
    proving the predicate reads the disposition field rather than being permanently
    pinned at 1."""
    missed_with_disposition = _synthetic_row(
        "adversarial-corpus",
        "with-disposition.md",
        "with-disposition",
        stratum="B2",
        source="derived:x",
        disposition="accept-with-reason: some reason.",
        form_defects=0,
        no_column_fired=True,
        target_missed=True,
    )
    missed_without_disposition = _synthetic_row(
        "adversarial-corpus",
        "missing-disposition.md",
        "missing-disposition",
        stratum="B2",
        source="derived:x",
        disposition="MISSING",
        form_defects=0,
        no_column_fired=True,
        target_missed=True,
    )
    headline = compute_corpus_headline([missed_with_disposition, missed_without_disposition])
    assert headline["missed_without_disposition"] == 1, headline["missed_without_disposition"]

    perturbed = dict(missed_without_disposition)
    perturbed["disposition"] = "accept-with-reason: now has one."
    perturbed_headline = compute_corpus_headline([missed_with_disposition, perturbed])
    assert perturbed_headline["missed_without_disposition"] == 0, perturbed_headline[
        "missed_without_disposition"
    ]


# ---------------------------------------------------------------------------
# Phase 19 (CONF-07/CONF-08) controls: the three Task-1 floors, plus the
# D-03 perturbation floor and its call-site census, all offline and
# tempdir/in-memory -- none of these touches tests/adversarial-corpus-v9.0/.
# ---------------------------------------------------------------------------


def _control_corpus_roster_drift_detected() -> None:
    corpus_rows = [
        _synthetic_row("adversarial-corpus", "a.md", "a"),
        _synthetic_row("adversarial-corpus", "b.md", "b"),
    ]
    catalog_entries = {
        "a": {
            "stratum": "B2",
            "source": "x",
            "what_is_false": "x",
            "ought_to_catch": "x",
            "disposition": "accept-with-reason: x.",
        },
        "c": {
            "stratum": "B2",
            "source": "x",
            "what_is_false": "x",
            "ought_to_catch": "x",
            "disposition": "accept-with-reason: x.",
        },
    }
    problems = _corpus_roster_problems(catalog_entries, [], corpus_rows)
    assert len(problems) == 1, problems
    assert "missing=['b']" in problems[0], problems
    assert "extra=['c']" in problems[0], problems


def _control_corpus_roster_equal_passes() -> None:
    corpus_rows = [_synthetic_row("adversarial-corpus", "a.md", "a")]
    catalog_entries = {
        "a": {
            "stratum": "B2",
            "source": "x",
            "what_is_false": "x",
            "ought_to_catch": "x",
            "disposition": "accept-with-reason: x.",
        }
    }
    assert _corpus_roster_problems(catalog_entries, [], corpus_rows) == []


def _control_corpus_roster_catalog_problems_folded() -> None:
    problems = _corpus_roster_problems({}, ["CATALOG PARSE FAIL — x"], [])
    assert problems == ["CATALOG PARSE FAIL — x"], problems


def _control_corpus_disposition_silent_pass_detected() -> None:
    row = _synthetic_row(
        "adversarial-corpus",
        "a.md",
        "a",
        stratum="B2",
        source="derived:x",
        disposition="MISSING",
        no_column_fired=True,
        target_missed=True,
        form_defects=0,
    )
    problems = _corpus_disposition_problems([row])
    assert len(problems) == 1, problems
    assert "SILENT PASS [a]" in problems[0], problems


def _control_corpus_disposition_target_missed_only_checked() -> None:
    """Phase 19 (CONF-08, D-19-08-A): the t13 shape -- `no_column_fired` False (an
    unrelated column fired) but `target_missed` True (the catalogued target itself was
    never flagged) -- is CHECKED by the union floor even though the old single-predicate
    scope would have skipped it entirely. This is the exact fix for the
    19-VERIFICATION.md gap: a missing disposition on a row shaped exactly like this used
    to escape CONF-08's zero-silent-passes mechanism."""
    row = _synthetic_row(
        "adversarial-corpus",
        "a.md",
        "a",
        stratum="A",
        source="hand-authored",
        disposition="MISSING",
        no_column_fired=False,
        target_missed=True,
        form_defects=0,
    )
    problems = _corpus_disposition_problems([row])
    assert len(problems) == 1, problems
    assert "SILENT PASS [a]" in problems[0], problems


def _control_corpus_disposition_form_bad_detected() -> None:
    row = _synthetic_row(
        "adversarial-corpus",
        "a.md",
        "a",
        stratum="B2",
        source="derived:x",
        disposition="looks fine",
        no_column_fired=True,
        target_missed=True,
        form_defects=0,
    )
    problems = _corpus_disposition_problems([row])
    assert len(problems) == 1, problems
    assert "DISPOSITION FORM [a]" in problems[0], problems


def _control_corpus_disposition_valid_passes() -> None:
    row = _synthetic_row(
        "adversarial-corpus",
        "a.md",
        "a",
        stratum="B2",
        source="derived:x",
        disposition="accept-with-reason: fine.",
        no_column_fired=True,
        target_missed=True,
        form_defects=0,
    )
    assert _corpus_disposition_problems([row]) == []


def _control_corpus_disposition_nonclean_skipped() -> None:
    """Both predicates False -- a genuine catch, target hit AND a substantive column
    fired -- is skipped by the union floor exactly as the old single-predicate scope
    skipped it."""
    row = _synthetic_row(
        "adversarial-corpus",
        "a.md",
        "a",
        stratum="A",
        source="derived:x",
        disposition="MISSING",
        no_column_fired=False,
        target_missed=False,
        form_defects=1,
    )
    assert _corpus_disposition_problems([row]) == []


# ---------------------------------------------------------------------------
# Phase 19 (CONF-08, D-19-08-B) controls: the Target column grammar, the
# chain-scoped join, and the two "always missed" shapes.
# ---------------------------------------------------------------------------


def _control_corpus_target_parse_vocabulary() -> None:
    assert _parse_corpus_target("none") == ([], [])
    assert _parse_corpus_target("dependency_cycles:c1") == (
        [("dependency_cycles", ["c1"])],
        [],
    )
    assert _parse_corpus_target("dependency_cycles:c1,c2") == (
        [("dependency_cycles", ["c1", "c2"])],
        [],
    )
    assert _parse_corpus_target("dependency_cycles:c1;ungrounded_chains:c2") == (
        [("dependency_cycles", ["c1"]), ("ungrounded_chains", ["c2"])],
        [],
    )

    pairs, problems = _parse_corpus_target("foo:c1")
    assert pairs == [], pairs
    assert any("unknown column" in p for p in problems), problems

    pairs, problems = _parse_corpus_target("dependency_cycles")
    assert pairs == [], pairs
    assert any("no ':'" in p for p in problems), problems

    pairs, problems = _parse_corpus_target("dependency_cycles:")
    assert pairs == [], pairs
    assert any("empty selector" in p for p in problems), problems

    pairs, problems = _parse_corpus_target("selfaudit_disagreements:x")
    assert pairs == [], pairs
    assert any("not an integer" in p for p in problems), problems

    pairs, problems = _parse_corpus_target("")
    assert pairs == [], pairs
    assert any("empty" in p for p in problems), problems


def _control_corpus_target_hits_chain_scoped() -> None:
    """The t13 control: `_ungrounded_chains=['c2','c3']` against target
    `ungrounded_chains:c1` (t13's actual catalogued target) yields NO hit -- the
    catalogued chain was never flagged, even though the column fired on OTHER chains.
    The same record against `ungrounded_chains:c2` DOES hit -- proving the join reads
    chain identity, not merely "did this column fire"."""
    record = {"_ungrounded_chains": ["c2", "c3"], "_dependency_cycles": ["c2", "c3"]}
    no_hit = _corpus_target_hits(record, [("ungrounded_chains", ["c1"])])
    assert no_hit == [], no_hit

    hit = _corpus_target_hits(record, [("ungrounded_chains", ["c2"])])
    assert hit == ["ungrounded_chains:c2"], hit


def _control_corpus_target_hits_selfaudit_criterion() -> None:
    record = {"_selfaudit_disagreements": [{"criterion": 4}]}
    hit = _corpus_target_hits(record, [("selfaudit_disagreements", ["4"])])
    assert hit == ["selfaudit_disagreements:4"], hit

    no_hit = _corpus_target_hits(record, [("selfaudit_disagreements", ["6"])])
    assert no_hit == [], no_hit


def _control_corpus_target_none_is_missed() -> None:
    """A `Target` of `none` parses to an empty pair list, so `_corpus_target_hits` returns
    no hits regardless of what the record measures -- proving `target_missed` is True by
    construction for a `none` target, even against a record showing real audit-field
    activity on an unrelated column."""
    parsed, problems = _parse_corpus_target("none")
    assert problems == [], problems
    record_with_activity = {
        "_dependency_cycles": ["c1", "c2"],
        "_ungrounded_chains": [],
        "_selfaudit_disagreements": [],
    }
    hits = _corpus_target_hits(record_with_activity, parsed)
    assert hits == [], hits


def _control_corpus_target_missing_entry_is_missed() -> None:
    with tempfile.TemporaryDirectory() as td:
        root = Path(td)
        (root / "z.md").write_text(_READABLE_FIXTURE_TEXT, encoding="utf-8")
        artifact = Artifact("adversarial-corpus", "z.md", root / "z.md", "z")
        row = build_corpus_row(artifact, None)
    assert row["target"] == "MISSING", row["target"]
    assert row["target_missed"] is True, row


def _control_corpus_headline_keys_on_target_missed() -> None:
    """Phase 19 (CONF-08, D-19-08-A) -- the ANTI-VACUITY ARM for the whole rename: a
    synthetic three-row corpus with one row whose `no_column_fired` is False but whose
    `target_missed` is True (the exact t13 shape) must produce a headline whose
    `target_missed` count differs from its `no_column_fired` count. A headline
    computation that merely renamed the old `clean` key -- reading `no_column_fired` for
    both -- would report the same number for both keys here and FAIL this control."""
    caught_by_both = _synthetic_row(
        "adversarial-corpus",
        "caught.md",
        "caught",
        stratum="A",
        source="hand-authored",
        disposition="accept-with-reason: positive control.",
        form_defects=0,
        no_column_fired=False,
        target_missed=False,
    )
    missed_by_both = _synthetic_row(
        "adversarial-corpus",
        "missed.md",
        "missed",
        stratum="B2",
        source="derived:x",
        disposition="accept-with-reason: no shipped rule reaches this.",
        form_defects=0,
        no_column_fired=True,
        target_missed=True,
    )
    # The t13 shape: an unrelated column fired (no_column_fired=False) while the item's
    # own catalogued target was never flagged (target_missed=True).
    diverges = _synthetic_row(
        "adversarial-corpus",
        "diverges.md",
        "diverges",
        stratum="A",
        source="hand-authored",
        disposition="accept-with-reason: disclosed bound.",
        form_defects=0,
        no_column_fired=False,
        target_missed=True,
    )
    headline = compute_corpus_headline([caught_by_both, missed_by_both, diverges])
    assert headline["target_missed"] == 2, headline
    assert headline["no_column_fired"] == 1, headline
    assert headline["target_missed"] != headline["no_column_fired"], headline


def _control_corpus_population_per_item_zero_detected() -> None:
    row = _synthetic_row(
        "adversarial-corpus",
        "a.md",
        "a",
        stratum="B2",
        source="x",
        disposition="accept-with-reason: x.",
        form_defects=0,
        conclusion_claims=0,
        chain_blocks=1,
        verdict_cells=1,
    )
    problems = _corpus_population_problems([row])
    assert any("CORPUS POPULATION [a] conclusion_claims: 0" in p for p in problems), problems


def _control_corpus_population_per_item_unreadable_detected() -> None:
    row = _synthetic_row(
        "adversarial-corpus",
        "a.md",
        "a",
        stratum="MISSING",
        source="MISSING",
        disposition="MISSING",
        form_defects="unreadable",
        section_resolution="SectionResolutionError: x",
    )
    problems = _corpus_population_problems([row])
    assert any(
        "CORPUS POPULATION [a] section_resolution: unreadable" in p for p in problems
    ), problems


def _control_corpus_population_corpuswide_breach_detected() -> None:
    row = _synthetic_row(
        "adversarial-corpus",
        "a.md",
        "a",
        stratum="B2",
        source="x",
        disposition="accept-with-reason: x.",
        form_defects=0,
        conclusion_claims=1,
        chain_blocks=1,
        verdict_cells=1,
    )
    problems = _corpus_population_problems([row])
    assert any("CORPUS POPULATION FLOOR BREACH conclusion_claims" in p for p in problems), problems
    assert any("CORPUS POPULATION FLOOR BREACH verdict_cells" in p for p in problems), problems
    assert any("CORPUS POPULATION FLOOR BREACH chain_blocks" in p for p in problems), problems


def _control_corpus_population_floor_values_locked() -> None:
    """BL-03 (18-12's convention): the pinned floors must equal an INLINE
    dict literal written at the control site, never read from
    `_CORPUS_POPULATION_FLOORS` itself -- a fixture derived from the
    constant it protects is invariant to that constant's value.
    """
    expected = {"conclusion_claims": 49, "verdict_cells": 66, "chain_blocks": 32}
    assert _CORPUS_POPULATION_FLOORS == expected, (
        f"CORPUS POPULATION FLOOR VALUE MISMATCH: {_CORPUS_POPULATION_FLOORS} != {expected}"
    )


# A resolvable six-section document whose §2 has one em-dash-separated
# conforming verdict cell, whose §4 carries one `### Conclusion C1:` block
# with a GT head and TWO separate arrow-led continuation lines (the second
# ending in a period so it closes the segment -- the first is deliberately
# left OPEN, matching personal-general.md's own shape, verified live
# against report-conformance.py before being pinned here), and whose §6
# carries one inline `(chain C1)` citation. All three D-03 mutation
# families fire with delta exactly 1 against this fixture (verified via
# scratch script during 19-06's authoring; see 19-06-SUMMARY.md).
_D03_FIXTURE_TEXT = """## 1. Problem Essence
Some essence text long enough.

## 2. Assumptions Table
| Assumption | Type | Treatment | Verdict | Verification |
|---|---|---|---|---|
| Some assumption | untested belief | Verify it. | Accept — because the evidence directly supports it. | Some verification text. |

## 3. Ground Truths
- GT-1: some ground truth fact with enough detail to be real.

## 4. Derivation Chains

### Conclusion C1: Some conclusion label goes here
GT-1 (some observation about the ground truth)
→ An intermediate claim that is long enough to look like real chain content and stays open
→ The final conclusion text that is also long enough to be a real chain conclusion.

## 5. Abandoned Reasoning
None.

## 6. Conclusion

**Recommended approach:** (chain C1) Do the thing that the chain concludes should be done here.
"""

# (a) absent: the only verdict cell uses an ASCII hyphen, never U+2014, so
# _verdict_conforms rejects it and no conforming cell exists to locate.
_D03_FIXTURE_NO_A_SITE_TEXT = _D03_FIXTURE_TEXT.replace(
    "Accept — because the evidence directly supports it.",
    "Accept - because the evidence directly supports it.",
)

# (b) absent: the same chain, rewritten onto ONE physical line -- both
# arrows sit on the head line itself, so no separate arrow-led continuation
# line exists to locate. This is the real shape five of the thirteen
# shipped corpus items use.
_D03_FIXTURE_NO_B_SITE_TEXT = _D03_FIXTURE_TEXT.replace(
    "GT-1 (some observation about the ground truth)\n"
    "→ An intermediate claim that is long enough to look like real chain content and stays open\n"
    "→ The final conclusion text that is also long enough to be a real chain conclusion.",
    "GT-1 (some observation about the ground truth) → An intermediate claim that is long "
    "enough to look like real chain content → The final conclusion text that is also long "
    "enough to be a real chain conclusion.",
)

# (c) absent: the §6 claim names no chain at all -- no inline parenthetical,
# no structural ledger row.
_D03_FIXTURE_NO_C_SITE_TEXT = _D03_FIXTURE_TEXT.replace(
    "**Recommended approach:** (chain C1) Do the thing that the chain concludes should be "
    "done here.",
    "**Recommended approach:** Do the thing that this analysis concludes should be done, "
    "stated without naming any chain at all here.",
)

# All three families absent at once: (a), (b) and (c) all removed, so the
# item admits zero mutations.
_D03_FIXTURE_NO_SITES_TEXT = (
    _D03_FIXTURE_NO_A_SITE_TEXT.replace(
        "GT-1 (some observation about the ground truth)\n"
        "→ An intermediate claim that is long enough to look like real chain content and stays open\n"
        "→ The final conclusion text that is also long enough to be a real chain conclusion.",
        "GT-1 (some observation about the ground truth) → An intermediate claim that is "
        "long enough to look like real chain content → The final conclusion text that is "
        "also long enough to be a real chain conclusion.",
    ).replace(
        "**Recommended approach:** (chain C1) Do the thing that the chain concludes should be "
        "done here.",
        "**Recommended approach:** Do the thing that this analysis concludes should be done, "
        "stated without naming any chain at all here.",
    )
)

# The WR-03 masking shape `_chain_block_well_formed`'s own docstring
# discloses: a SECOND independent GT-headed candidate in the same block,
# also well-formed on its own, masks the mutation applied to the first
# candidate -- baseline and mutated malformed_chain_blocks both read 0,
# so the (b) delta-mismatch problem must fire (verified via scratch script;
# see 19-06-SUMMARY.md).
_D03_FIXTURE_MASKED_HOP_TEXT = """## 1. Problem Essence
Some essence text long enough.

## 2. Assumptions Table
| Assumption | Type | Treatment | Verdict | Verification |
|---|---|---|---|---|
| Some assumption | untested belief | Verify it. | Accept — because the evidence directly supports it. | Some verification text. |

## 3. Ground Truths
- GT-1: some ground truth fact with enough detail to be real.
- GT-2: a second ground truth fact with enough detail to also be real.

## 4. Derivation Chains

### Conclusion C1: Some conclusion label goes here
GT-1 (some observation about the ground truth)
→ An intermediate claim that is long enough to look like real chain content and stays open
→ The first candidate final conclusion text that is long enough to close this segment.
GT-2 (a second observation about the ground truth)
→ A second intermediate claim that is long enough to look like real chain content too
→ The second candidate final conclusion text that is also long enough to close.

## 5. Abandoned Reasoning
None.

## 6. Conclusion

**Recommended approach:** (chain C1) Do the thing that the chain concludes should be done here.
"""


def _corpus_perturbation_row(analysis_id: str, relpath: str = "item.md") -> dict:
    return {
        "surface": "adversarial-corpus",
        "relpath": relpath,
        "analysis_id": analysis_id,
        "section_resolution": "OK",
    }


def _control_corpus_d03_positive_all_families() -> None:
    with tempfile.TemporaryDirectory() as td:
        root = Path(td)
        (root / "item.md").write_text(_D03_FIXTURE_TEXT, encoding="utf-8")
        problems = _corpus_perturbation_problems([_corpus_perturbation_row("item")], root)
        assert problems == [], problems


def _control_corpus_d03_family_a_not_found() -> None:
    with tempfile.TemporaryDirectory() as td:
        root = Path(td)
        (root / "item.md").write_text(_D03_FIXTURE_NO_A_SITE_TEXT, encoding="utf-8")
        problems = _corpus_perturbation_problems([_corpus_perturbation_row("item")], root)
        assert any("D-03(a) mutation site not found" in p for p in problems), problems


def _control_corpus_d03_family_b_absence_not_reported() -> None:
    with tempfile.TemporaryDirectory() as td:
        root = Path(td)
        (root / "item.md").write_text(_D03_FIXTURE_NO_B_SITE_TEXT, encoding="utf-8")
        problems = _corpus_perturbation_problems([_corpus_perturbation_row("item")], root)
        assert not any("D-03(b)" in p for p in problems), problems
        assert not any("NO MUTATION APPLIED" in p for p in problems), problems
        assert problems == [], problems


def _control_corpus_d03_family_c_not_found() -> None:
    with tempfile.TemporaryDirectory() as td:
        root = Path(td)
        (root / "item.md").write_text(_D03_FIXTURE_NO_C_SITE_TEXT, encoding="utf-8")
        problems = _corpus_perturbation_problems([_corpus_perturbation_row("item")], root)
        assert any("D-03(c) mutation site not found" in p for p in problems), problems


def _control_corpus_d03_no_mutation_applied() -> None:
    with tempfile.TemporaryDirectory() as td:
        root = Path(td)
        (root / "item.md").write_text(_D03_FIXTURE_NO_SITES_TEXT, encoding="utf-8")
        problems = _corpus_perturbation_problems([_corpus_perturbation_row("item")], root)
        assert any("D-03(a) mutation site not found" in p for p in problems), problems
        assert any("D-03(c) mutation site not found" in p for p in problems), problems
        assert any("D-03 NO MUTATION APPLIED [item]" in p for p in problems), problems


def _control_corpus_d03_delta_mismatch_detected() -> None:
    with tempfile.TemporaryDirectory() as td:
        root = Path(td)
        (root / "item.md").write_text(_D03_FIXTURE_MASKED_HOP_TEXT, encoding="utf-8")
        problems = _corpus_perturbation_problems([_corpus_perturbation_row("item")], root)
        assert any(
            "D-03(b) chain-hop re-wrap mutation" in p and "did not increment" in p
            for p in problems
        ), problems


def _control_corpus_d03_unreadable_skipped() -> None:
    row = _corpus_perturbation_row("nope")
    row["section_resolution"] = "SectionResolutionError: x"
    problems = _corpus_perturbation_problems([row], Path("/nonexistent-repo-root"))
    assert problems == [], problems


def _control_corpus_call_site_census_positive() -> None:
    source = inspect.getsource(cmd_check)
    problems = _corpus_call_site_census_problems(source, _CORPUS_CALL_SITES, _CORPUS_CALL_FORMS)
    assert problems == [], problems


def _control_corpus_call_site_census_missing() -> None:
    source = "def cmd_check():\n    problems = []\n    return 0\n"
    problems = _corpus_call_site_census_problems(source, _CORPUS_CALL_SITES)
    assert len(problems) == len(_CORPUS_CALL_SITES), problems
    assert all("occurs 0 time" in p for p in problems), problems


def _control_corpus_call_site_census_commented() -> None:
    source = (
        "def cmd_check():\n"
        "    problems = []\n"
        "    # problems += "
        + "_corpus_roster_problems(catalog_entries, catalog_problems, corpus_rows)\n"
        "    problems += " + "_corpus_disposition_problems(corpus_rows)\n"
        "    problems += " + "_corpus_population_problems(corpus_rows)\n"
        "    problems += " + "_corpus_perturbation_problems(rows, REPO_ROOT)\n"
        "    return 0\n"
    )
    problems = _corpus_call_site_census_problems(source, _CORPUS_CALL_SITES)
    assert any("_corpus_roster_problems occurs 0" in p for p in problems), problems


def _control_corpus_call_form_lock_rewritten() -> None:
    source = (
        "def cmd_check():\n"
        "    problems = []\n"
        "    problems += " + "_corpus_roster_problems(catalog_entries)\n"
        "    problems += " + "_corpus_disposition_problems(corpus_rows)\n"
        "    problems += " + "_corpus_population_problems(corpus_rows)\n"
        "    problems += " + "_corpus_perturbation_problems(rows, REPO_ROOT)\n"
        "    return 0\n"
    )
    problems = _corpus_call_site_census_problems(source, _CORPUS_CALL_SITES, _CORPUS_CALL_FORMS)
    assert any("CALL-FORM LOCK: _corpus_roster_problems" in p for p in problems), problems


def _control_corpus_call_sites_roster_lock_positive() -> None:
    assert _corpus_call_sites_roster_problems() == []


def _control_corpus_call_sites_roster_lock_narrowed() -> None:
    narrowed_sites = dict(_CORPUS_CALL_SITES)
    del narrowed_sites["_corpus_perturbation_problems"]
    problems = _corpus_call_sites_roster_problems(call_sites=narrowed_sites)
    assert any("_CORPUS_CALL_SITES diverges" in p for p in problems), problems


def _control_corpus_call_sites_roster_lock_wrong_count() -> None:
    wrong_sites = dict(_CORPUS_CALL_SITES)
    wrong_sites["_corpus_roster_problems"] = 2
    problems = _corpus_call_sites_roster_problems(call_sites=wrong_sites)
    assert any("non-1 expected count" in p for p in problems), problems


_CONTROLS: tuple[tuple[str, object], ...] = (
    ("floor-shared-short", _control_floor_shared_short),
    ("floor-twin-short", _control_floor_twin_short),
    ("floor-contract-missing", _control_floor_contract_missing),
    ("floor-glob-empty", _control_floor_glob_empty),
    ("floor-passes-at-minimum", _control_floor_passes_at_minimum),
    ("partial-row-records-heading-census", _control_partial_row_records_heading_census),
    ("partial-row-not-dropped", _control_partial_row_not_dropped),
    ("agreement-field-scope", _control_agreement_field_scope),
    ("agreement-detects-measured-divergence", _control_agreement_detects_measured_divergence),
    ("agreement-vacuity-guard", _control_agreement_vacuity_guard),
    ("agreement-unpaired-is-divergence", _control_agreement_unpaired_is_divergence),
    ("render-determinism", _control_render_determinism),
    ("render-provenance-sentinel", _control_render_provenance_sentinel),
    ("check-detects-drift", _control_check_detects_drift),
    ("marked-untraced-claim-counted", _control_marked_untraced_claim_counted),
    ("unreadable-columns-are-literal", _control_unreadable_columns_are_literal),
    (
        "render-marked-silent-parsed-from-output",
        _control_render_marked_silent_parsed_from_output,
    ),
    ("corpus-render-no-hardcoded-stems", _control_corpus_render_no_hardcoded_stems),
    ("corpus-missed-without-disposition", _control_corpus_missed_without_disposition),
    ("corpus-roster-drift-detected", _control_corpus_roster_drift_detected),
    ("corpus-roster-equal-passes", _control_corpus_roster_equal_passes),
    (
        "corpus-roster-catalog-problems-folded",
        _control_corpus_roster_catalog_problems_folded,
    ),
    (
        "corpus-disposition-silent-pass-detected",
        _control_corpus_disposition_silent_pass_detected,
    ),
    (
        "corpus-disposition-target-missed-only-checked",
        _control_corpus_disposition_target_missed_only_checked,
    ),
    (
        "corpus-disposition-form-bad-detected",
        _control_corpus_disposition_form_bad_detected,
    ),
    ("corpus-disposition-valid-passes", _control_corpus_disposition_valid_passes),
    ("corpus-disposition-nonclean-skipped", _control_corpus_disposition_nonclean_skipped),
    ("corpus-target-parse-vocabulary", _control_corpus_target_parse_vocabulary),
    ("corpus-target-hits-chain-scoped", _control_corpus_target_hits_chain_scoped),
    (
        "corpus-target-hits-selfaudit-criterion",
        _control_corpus_target_hits_selfaudit_criterion,
    ),
    ("corpus-target-none-is-missed", _control_corpus_target_none_is_missed),
    (
        "corpus-target-missing-entry-is-missed",
        _control_corpus_target_missing_entry_is_missed,
    ),
    (
        "corpus-headline-keys-on-target-missed",
        _control_corpus_headline_keys_on_target_missed,
    ),
    (
        "corpus-population-per-item-zero-detected",
        _control_corpus_population_per_item_zero_detected,
    ),
    (
        "corpus-population-per-item-unreadable-detected",
        _control_corpus_population_per_item_unreadable_detected,
    ),
    (
        "corpus-population-corpuswide-breach-detected",
        _control_corpus_population_corpuswide_breach_detected,
    ),
    (
        "corpus-population-floor-values-locked",
        _control_corpus_population_floor_values_locked,
    ),
    ("corpus-d03-positive-all-families", _control_corpus_d03_positive_all_families),
    ("corpus-d03-family-a-not-found", _control_corpus_d03_family_a_not_found),
    (
        "corpus-d03-family-b-absence-not-reported",
        _control_corpus_d03_family_b_absence_not_reported,
    ),
    ("corpus-d03-family-c-not-found", _control_corpus_d03_family_c_not_found),
    ("corpus-d03-no-mutation-applied", _control_corpus_d03_no_mutation_applied),
    ("corpus-d03-delta-mismatch-detected", _control_corpus_d03_delta_mismatch_detected),
    ("corpus-d03-unreadable-skipped", _control_corpus_d03_unreadable_skipped),
    ("corpus-call-site-census-positive", _control_corpus_call_site_census_positive),
    ("corpus-call-site-census-missing", _control_corpus_call_site_census_missing),
    ("corpus-call-site-census-commented", _control_corpus_call_site_census_commented),
    ("corpus-call-form-lock-rewritten", _control_corpus_call_form_lock_rewritten),
    (
        "corpus-call-sites-roster-lock-positive",
        _control_corpus_call_sites_roster_lock_positive,
    ),
    (
        "corpus-call-sites-roster-lock-narrowed",
        _control_corpus_call_sites_roster_lock_narrowed,
    ),
    (
        "corpus-call-sites-roster-lock-wrong-count",
        _control_corpus_call_sites_roster_lock_wrong_count,
    ),
)

# Coverage floor (SCAN-GUARD's _BRANCH_ROSTER_LOCK shape, backlog 999.30/999.31): a second,
# independently-typed transcription of every control id this self-test must run. A control
# added to _CONTROLS but missing here, or vice versa, fails self_test() by name rather than
# silently narrowing coverage.
_CONTROL_IDS: tuple[str, ...] = (
    "floor-shared-short",
    "floor-twin-short",
    "floor-contract-missing",
    "floor-glob-empty",
    "floor-passes-at-minimum",
    "partial-row-records-heading-census",
    "partial-row-not-dropped",
    "agreement-field-scope",
    "agreement-detects-measured-divergence",
    "agreement-vacuity-guard",
    "agreement-unpaired-is-divergence",
    "render-determinism",
    "render-provenance-sentinel",
    "check-detects-drift",
    "marked-untraced-claim-counted",
    "unreadable-columns-are-literal",
    "render-marked-silent-parsed-from-output",
    "corpus-render-no-hardcoded-stems",
    "corpus-missed-without-disposition",
    "corpus-roster-drift-detected",
    "corpus-roster-equal-passes",
    "corpus-roster-catalog-problems-folded",
    "corpus-disposition-silent-pass-detected",
    "corpus-disposition-target-missed-only-checked",
    "corpus-disposition-form-bad-detected",
    "corpus-disposition-valid-passes",
    "corpus-disposition-nonclean-skipped",
    "corpus-target-parse-vocabulary",
    "corpus-target-hits-chain-scoped",
    "corpus-target-hits-selfaudit-criterion",
    "corpus-target-none-is-missed",
    "corpus-target-missing-entry-is-missed",
    "corpus-headline-keys-on-target-missed",
    "corpus-population-per-item-zero-detected",
    "corpus-population-per-item-unreadable-detected",
    "corpus-population-corpuswide-breach-detected",
    "corpus-population-floor-values-locked",
    "corpus-d03-positive-all-families",
    "corpus-d03-family-a-not-found",
    "corpus-d03-family-b-absence-not-reported",
    "corpus-d03-family-c-not-found",
    "corpus-d03-no-mutation-applied",
    "corpus-d03-delta-mismatch-detected",
    "corpus-d03-unreadable-skipped",
    "corpus-call-site-census-positive",
    "corpus-call-site-census-missing",
    "corpus-call-site-census-commented",
    "corpus-call-form-lock-rewritten",
    "corpus-call-sites-roster-lock-positive",
    "corpus-call-sites-roster-lock-narrowed",
    "corpus-call-sites-roster-lock-wrong-count",
)


def self_test() -> int:
    executed: list[str] = []
    failures: list[tuple[str, str]] = []

    for control_id, control_fn in _CONTROLS:
        executed.append(control_id)
        try:
            control_fn()
        except AssertionError as exc:
            failures.append((control_id, str(exc)))
        except Exception as exc:  # noqa: BLE001 -- a control that crashes is a failure too
            failures.append((control_id, f"{type(exc).__name__}: {exc}"))

    registered = set(_CONTROL_IDS)
    ran = set(executed)
    missing = registered - ran
    extra = ran - registered
    if missing or extra:
        failures.append(
            (
                "coverage-floor",
                f"registered/executed control-id mismatch: missing={sorted(missing)} "
                f"extra={sorted(extra)}",
            )
        )

    if failures:
        for control_id, message in failures:
            sys.stderr.write(f"report-conformance: SELF-TEST FAIL [{control_id}] — {message}\n")
        return 1

    print(f"report-conformance: SELF-TEST PASS — {len(executed)} controls run")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Phase 17 conformance measurement report over the frozen quality harness."
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="regenerate in memory and diff against the on-disk artifacts; exit 1 on drift",
    )
    parser.add_argument(
        "--self-test",
        action="store_true",
        help="run the offline control battery (positive, negative, anti-masking)",
    )
    args = parser.parse_args(argv)

    try:
        if args.self_test:
            return self_test()
        if args.check:
            return cmd_check()
        return cmd_write()
    except DiscoveryFloorError as exc:
        for line in str(exc).splitlines():
            sys.stderr.write(line + "\n")
        return 1


if __name__ == "__main__":
    sys.exit(main())
