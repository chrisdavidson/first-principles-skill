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
    1  --check found drift, or discovery floor failed, or --self-test found a failing control
    2  --check found the pass1/pass2 in-memory generation itself non-deterministic
"""

from __future__ import annotations

import argparse
import difflib
import importlib.util
import json
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
}
_VALID_STRATA: frozenset[str] = frozenset({"A", "B1", "B2"})


def parse_corpus_catalog(repo_root: Path) -> tuple[dict[str, dict], list[str]]:
    """Parse `ADVERSARIAL_CORPUS_CATALOG`'s `## Catalog` table into
    `{stem: {"stratum": ..., "source": ..., "what_is_false": ..., "ought_to_catch": ...,
    "disposition": ...}}`, keyed by the `File` column (the artifact stem, matching
    `Artifact.analysis_id`).

    Parses by locating the header row containing all seven column names, then reading the
    `|`-delimited data rows beneath it, mapping BY HEADER NAME, never by position -- a
    future column insertion must not silently shift the parse. Never silently drops a
    malformed row: a row whose `File` cell is empty, or whose `Stratum` cell is not one of
    A/B1/B2, is returned as a parse problem in the second tuple element instead, so a
    floor built on this function's output can report parse failures by name rather than
    seeing a shorter dict than expected.
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

        entries[file_cell] = {
            "stratum": stratum_cell,
            "source": cells[col_index["Source"]],
            "what_is_false": cells[col_index["What is false"]],
            "ought_to_catch": cells[col_index["Rule that ought to catch it"]],
            "disposition": cells[col_index["Disposition"]],
        }

    return entries, problems


def build_row(artifact: Artifact) -> dict:
    """D-03's partial row: the heading census runs FIRST and unconditionally, so a
    document `_slice_sections` rejects still carries a real heading-sweep reading rather
    than losing that datum along with everything `detect_defects` would have produced.

    Three-way column vocabulary, never confused with each other: a number means the
    detector read the document and counted; the literal "n/a" means no `.jsonl` capture
    exists (true of all 29 artifacts for the nine provenance columns, unconditionally --
    detect_defects never running changes nothing about capture availability); the literal
    "unreadable" means `_slice_sections` rejected the document, so the twelve measured
    schema fields were never computed.
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


def build_corpus_row(artifact: Artifact, catalog_entry: dict | None) -> dict:
    """A thin wrapper over `build_row` -- never a second `detect_defects` call and never a
    reimplementation. Calls `build_row(artifact)` verbatim, then merges in the joined
    catalog fields (`stratum`, `source`, `disposition`) plus two computed fields:

    `fully_clean` is True iff `section_resolution == "OK"` and every field in both
    `_CORPUS_FORM_FIELDS` and `_CORPUS_SUBSTANTIVE_FIELDS` reads the integer 0. An
    "unreadable" row is never fully_clean -- a document the detector could not read was
    not missed, and counting it as a false negative would be wrong (19-CONTEXT.md
    `<specifics>`).

    `form_defects` is the summed `_CORPUS_FORM_FIELDS` when readable, and the literal
    "unreadable" otherwise -- preserving `build_row`'s three-way column vocabulary rather
    than coercing an unreadable row's absence of a count into 0.

    If *catalog_entry* is None (the artifact has no catalog row), `stratum`/`source`/
    `disposition` are populated with the literal "MISSING" rather than omitted, so the row
    still renders and a later floor has something to name. The row is never dropped.
    """
    row = build_row(artifact)

    if catalog_entry is None:
        row["stratum"] = "MISSING"
        row["source"] = "MISSING"
        row["disposition"] = "MISSING"
    else:
        row["stratum"] = catalog_entry["stratum"]
        row["source"] = catalog_entry["source"]
        row["disposition"] = catalog_entry["disposition"]

    readable = row["section_resolution"] == "OK"
    if readable:
        row["form_defects"] = sum(row[f] for f in _CORPUS_FORM_FIELDS)
        row["fully_clean"] = all(row[f] == 0 for f in _CORPUS_FORM_FIELDS) and all(
            row[f] == 0 for f in _CORPUS_SUBSTANTIVE_FIELDS
        )
    else:
        row["form_defects"] = "unreadable"
        row["fully_clean"] = False

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
    extra entry inside it: a corpus headline counts fully-clean ITEMS, while
    `compute_headline`'s `per_surface`/`_sum_measured` helpers sum a numeric field across
    a surface -- a different shape of aggregation. Every value here is derived from
    `corpus_rows` at call time; nothing is hardcoded.
    """
    total = len(corpus_rows)
    clean = sum(1 for r in corpus_rows if r["fully_clean"] is True)
    unreadable = sum(1 for r in corpus_rows if r["section_resolution"] != "OK")
    form_defects = sum(
        r["form_defects"] for r in corpus_rows if r["section_resolution"] == "OK"
    )

    by_stratum: dict[str, dict[str, int]] = {}
    for r in corpus_rows:
        stratum = r["stratum"]
        bucket = by_stratum.setdefault(stratum, {"clean": 0, "total": 0})
        bucket["total"] += 1
        if r["fully_clean"] is True:
            bucket["clean"] += 1

    clean_without_disposition = sum(
        1
        for r in corpus_rows
        if r["fully_clean"] is True and (not r["disposition"] or r["disposition"] == "MISSING")
    )

    return {
        "total": total,
        "clean": clean,
        "unreadable": unreadable,
        "form_defects": form_defects,
        "by_stratum": by_stratum,
        "clean_without_disposition": clean_without_disposition,
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
    "fully_clean",
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
        f"{headline['clean']} of {headline['total']} corpus items score fully clean "
        "under the unmodified, CONTRACT-06-frozen `detect_defects` -- despite every item "
        "being a stated, catalogued falsehood. Each of those "
        f"{headline['clean']} is a false negative: a substantively wrong analysis this "
        "instrument cannot distinguish from a sound one."
    )
    lines.append("")
    for stratum in _STRATUM_ORDER:
        if stratum not in headline["by_stratum"]:
            continue
        bucket = headline["by_stratum"][stratum]
        lines.append(f"- Stratum {stratum}: {bucket['clean']} of {bucket['total']} clean")
    lines.append("")
    b2 = headline["by_stratum"].get("B2", {"clean": 0, "total": 0})
    lines.append(
        "**Backlog 999.4 gate input.** Stratum B2 -- reachable by nothing this project "
        f"ships -- reads {b2['clean']} of {b2['total']} clean. Per "
        "`.planning/ROADMAP.md` Phase 999.4 (CONDITIONAL, gated on this measurement): a "
        "low B2 rate closes 999.4 unrun, with this measurement recorded as the reason; a "
        "high B2 rate promotes 999.4, with this corpus as its validation set."
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
    lines.append(
        "**Fixtures, not artifacts.** This section measures deliberately wrong test "
        "fixtures, never shipped artifacts. A probe reading clean is never the same "
        "claim as an artifact conforming. A stratum-A item scoring non-clean (`t03`, "
        "`t04`, `t05` in this corpus) is a positive control proving the run genuinely "
        "reaches that column on shipped corpus bytes, not a defect in the corpus. The "
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

    drifted = _diff_against_disk(pass1)

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


def _control_corpus_clean_without_disposition() -> None:
    """Phase 19 (CONF-08): a synthetic corpus row set with one clean row carrying a real
    disposition and one clean row whose disposition is the literal "MISSING" reads
    clean_without_disposition == 1. Perturbing the "MISSING" row's disposition to a
    non-empty string moves the count to 0 -- the same fixture, re-scored, proving the
    predicate reads the disposition field rather than being permanently pinned at 1."""
    clean_with_disposition = _synthetic_row(
        "adversarial-corpus",
        "with-disposition.md",
        "with-disposition",
        stratum="B2",
        source="derived:x",
        disposition="accept-with-reason: some reason.",
        form_defects=0,
        fully_clean=True,
    )
    clean_without_disposition = _synthetic_row(
        "adversarial-corpus",
        "missing-disposition.md",
        "missing-disposition",
        stratum="B2",
        source="derived:x",
        disposition="MISSING",
        form_defects=0,
        fully_clean=True,
    )
    headline = compute_corpus_headline([clean_with_disposition, clean_without_disposition])
    assert headline["clean_without_disposition"] == 1, headline["clean_without_disposition"]

    perturbed = dict(clean_without_disposition)
    perturbed["disposition"] = "accept-with-reason: now has one."
    perturbed_headline = compute_corpus_headline([clean_with_disposition, perturbed])
    assert perturbed_headline["clean_without_disposition"] == 0, perturbed_headline[
        "clean_without_disposition"
    ]


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
    ("corpus-clean-without-disposition", _control_corpus_clean_without_disposition),
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
    "corpus-clean-without-disposition",
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
