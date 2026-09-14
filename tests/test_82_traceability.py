#!/usr/bin/env python3
"""Tests for Phase 82: traceability matrix gate (TRACE-01..TRACE-03, GAP-01, GAP-02).

Pins the ``--self-test`` exit code to 0 so a breakage in the gate logic or its
inline fixtures is caught immediately by pytest without reading any .planning/
files. Also guards the script structure, emit output, path confinement, and
the GAP-01 active-tail emission.

Requirements covered:
  TRACE-01 — capability assignment + script structure
  TRACE-02 — emit writes both MATRIX.md and matrix.json
  TRACE-03 — consistency gate fixtures (dangling file/catalog/rubric/schema)
  GAP-01   — active-tail rows (RR-80-01/GEN-01/GEN-02 + RR residuals) emitted
  GAP-02   — path confinement rejects /tmp paths (T-81-01 reuse)

Run from repo root:
    python3 -m pytest tests/test_82_traceability.py -v
"""

from __future__ import annotations

import importlib.util
import subprocess
import sys
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[1]
SCRIPT = REPO / "scripts" / "check-traceability.py"


def _load_check_traceability():
    """Load check-traceability.py as a module (hyphenated name needs importlib)."""
    spec = importlib.util.spec_from_file_location("check_traceability", SCRIPT)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


# ---------------------------------------------------------------------------
# Structural guards
# ---------------------------------------------------------------------------


def test_script_exists() -> None:
    """scripts/check-traceability.py must exist (TRACE-01 structural)."""
    assert SCRIPT.exists(), f"check-traceability.py not found at {SCRIPT}"


def test_script_has_inline_script_header() -> None:
    """check-traceability.py must contain the inline script metadata header."""
    text = SCRIPT.read_text(encoding="utf-8")
    assert '# requires-python = ">=3.12"' in text, (
        "check-traceability.py does not contain "
        "'# requires-python = \">=3.12\"' in the inline script header"
    )


def test_script_has_no_external_imports() -> None:
    """check-traceability.py must be stdlib-only — no yaml, requests, or similar."""
    import re
    text = SCRIPT.read_text(encoding="utf-8")
    # Filter comment lines first (grep-gate hygiene)
    non_comment_lines = [
        line for line in text.splitlines()
        if line.strip() and not line.strip().startswith("#")
    ]
    non_comment_text = "\n".join(non_comment_lines)
    pattern = re.compile(r"\b(import|from)\s+(yaml|requests|pyyaml|toml|tomllib)\b")
    match = pattern.search(non_comment_text)
    assert match is None, (
        f"check-traceability.py imports a non-stdlib module: {match.group()!r}"
    )


# ---------------------------------------------------------------------------
# Behavioural invariant: --self-test exits 0 (TRACE-03 primary CI gate guard)
# ---------------------------------------------------------------------------


def test_self_test_exits_zero() -> None:
    """``python3 scripts/check-traceability.py --self-test`` must exit 0.

    This is the primary CI gate guard (TRACE-03). A non-zero exit means at
    least one of the 8 inline fixtures classified incorrectly:
      (1) valid reproducible row → PASS
      (2) dangling file path → non-zero exit
      (3) dangling catalog row → non-zero exit
      (4) missing rubric anchor → non-zero exit
      (5) audit-only row, no artifact link → PASS
      (6) gap row with rationale, no artifact link → PASS
      (7) row missing capability → non-zero exit
      (8) row missing coverage_tier → non-zero exit

    No live session required — uses inline fixture rows only.
    """
    result = subprocess.run(
        [sys.executable, str(SCRIPT), "--self-test"],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, (
        f"check-traceability.py --self-test exited {result.returncode} "
        f"(expected 0).\n"
        f"stdout:\n{result.stdout}\n"
        f"stderr:\n{result.stderr}"
    )


# ---------------------------------------------------------------------------
# TRACE-03: Dangling-reference detection fixtures
# ---------------------------------------------------------------------------


def test_dangling_file_path_detected() -> None:
    """A reproducible row with scripts/nonexistent-check-99.py must exit non-zero."""
    mod = _load_check_traceability()
    row = mod.MatrixRow(
        key="test/DANGLE-01",
        bare_id="DANGLE-01",
        milestone="test",
        capability="Test-Network",
        deliverable_path="scripts/check-routing-battery.py",
        coverage_tier="reproducible",
        artifact_link="scripts/nonexistent-check-99.py",
        gap_rationale="",
        surfaces=("apparatus",),
        statement=mod._STATEMENT_UNRECOVERABLE,
    )
    issues = mod.check_consistency([row])
    assert issues, (
        f"Expected dangling file path to be flagged; check_consistency returned: {issues!r}"
    )


def test_dangling_catalog_row_detected() -> None:
    """A reproducible row citing B-NONEXISTENT (not in catalog) must be flagged."""
    mod = _load_check_traceability()
    row = mod.MatrixRow(
        key="test/DANGLE-02",
        bare_id="DANGLE-02",
        milestone="test",
        capability="Test-Network",
        deliverable_path="scripts/check-routing-battery.py",
        coverage_tier="reproducible",
        artifact_link="tests/routing-battery-catalog.md#B-NONEXISTENT",
        gap_rationale="",
        surfaces=("apparatus",),
        statement=mod._STATEMENT_UNRECOVERABLE,
    )
    issues = mod.check_consistency([row])
    assert issues, (
        f"Expected dangling catalog row to be flagged; "
        f"check_consistency returned: {issues!r}"
    )


def test_missing_rubric_section_detected() -> None:
    """A reproducible row citing a non-existent rubric anchor must be flagged."""
    mod = _load_check_traceability()
    row = mod.MatrixRow(
        key="test/DANGLE-03",
        bare_id="DANGLE-03",
        milestone="test",
        capability="Methodology",
        deliverable_path="shared/spine/references/validation-rubric.md",
        coverage_tier="reproducible",
        artifact_link=(
            "shared/spine/references/validation-rubric.md"
            "#criterion-99-nonexistent"
        ),
        gap_rationale="",
        surfaces=("apparatus",),
        statement=mod._STATEMENT_UNRECOVERABLE,
    )
    issues = mod.check_consistency([row])
    assert issues, (
        f"Expected missing rubric section to be flagged; "
        f"check_consistency returned: {issues!r}"
    )


def test_missing_capability_detected() -> None:
    """A row with empty/absent capability must be flagged (TRACE-01)."""
    mod = _load_check_traceability()
    row = mod.MatrixRow(
        key="test/SCHEMA-01",
        bare_id="SCHEMA-01",
        milestone="test",
        capability="",
        deliverable_path="scripts/check-routing-battery.py",
        coverage_tier="audit-only",
        artifact_link="",
        gap_rationale="no capability assigned",
        surfaces=("apparatus",),
        statement=mod._STATEMENT_UNRECOVERABLE,
    )
    issues = mod.check_consistency([row])
    assert issues, (
        f"Expected missing capability to be flagged; "
        f"check_consistency returned: {issues!r}"
    )


def test_missing_coverage_tier_detected() -> None:
    """A row with empty/absent coverage_tier must be flagged (TRACE-03)."""
    mod = _load_check_traceability()
    row = mod.MatrixRow(
        key="test/SCHEMA-02",
        bare_id="SCHEMA-02",
        milestone="test",
        capability="Test-Network",
        deliverable_path="scripts/check-routing-battery.py",
        coverage_tier="",
        artifact_link="",
        gap_rationale="no tier assigned",
        surfaces=("apparatus",),
        statement=mod._STATEMENT_UNRECOVERABLE,
    )
    issues = mod.check_consistency([row])
    assert issues, (
        f"Expected missing coverage_tier to be flagged; "
        f"check_consistency returned: {issues!r}"
    )


# ---------------------------------------------------------------------------
# D-06 valid states: audit-only and gap rows with no artifact link
# ---------------------------------------------------------------------------


def test_audit_only_row_is_valid() -> None:
    """An audit-only row with no artifact link is a valid state (D-06)."""
    mod = _load_check_traceability()
    row = mod.MatrixRow(
        key="v3.1/ROUTE-02",
        bare_id="ROUTE-02",
        milestone="v3.1",
        capability="Test-Network",
        deliverable_path="scripts/check-routing.py",
        coverage_tier="audit-only",
        artifact_link="",
        gap_rationale="Validated by v3.1 milestone audit; no re-runnable gate",
        surfaces=("apparatus",),
        statement=mod._STATEMENT_UNRECOVERABLE,
    )
    issues = mod.check_consistency([row])
    assert not issues, (
        f"Unexpected issues for audit-only row (should be valid): {issues!r}"
    )


def test_gap_row_is_valid() -> None:
    """A gap row with rationale and no artifact link is a valid state (D-06)."""
    mod = _load_check_traceability()
    row = mod.MatrixRow(
        key="v5.3/GEN-01",
        bare_id="GEN-01",
        milestone="v5.3",
        capability="Test-Network",
        deliverable_path="active-tail",
        coverage_tier="gap",
        artifact_link="",
        gap_rationale=(
            "Full Step 0 classifier rearchitecture; perpetually deferred; "
            "no confirming phase"
        ),
        surfaces=("apparatus",),
        statement=mod._STATEMENT_UNRECOVERABLE,
    )
    issues = mod.check_consistency([row])
    assert not issues, (
        f"Unexpected issues for gap row (should be valid): {issues!r}"
    )


# ---------------------------------------------------------------------------
# TRACE-02: emit writes both .md and .json outputs
# ---------------------------------------------------------------------------


def test_emit_writes_both_files() -> None:
    """emit subcommand must write both .md and .json outputs under .planning/."""
    # Use a real path under .planning/ so the confinement guard passes.
    # (tmp_path is outside .planning/ and would fail the confinement guard —
    # PATTERNS.md note + T-82-01)
    phase_dir = (
        REPO
        / ".planning"
        / "phases"
        / "82-traceability-matrix-and-gap-findings"
    )
    md_out = phase_dir / "MATRIX.md"
    json_out = phase_dir / "matrix.json"
    result = subprocess.run(
        [
            sys.executable, str(SCRIPT), "emit",
            "--md-output", str(md_out),
            "--json-output", str(json_out),
        ],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, (
        f"emit failed (expected 0): returncode={result.returncode}\n"
        f"stdout:\n{result.stdout}\n"
        f"stderr:\n{result.stderr}"
    )
    assert md_out.exists(), f"MATRIX.md not written to {md_out}"
    assert json_out.exists(), f"matrix.json not written to {json_out}"


# ---------------------------------------------------------------------------
# Phase 32 SCHEMA-01/SCHEMA-02: surfaces field (D-05, D-06)
# ---------------------------------------------------------------------------


def test_matrixrow_requires_surfaces() -> None:
    """Omitting `surfaces` at construction raises TypeError (D-05: no default,
    required at every call site — a future batch cannot ship without it)."""
    mod = _load_check_traceability()
    with pytest.raises(TypeError):
        mod.MatrixRow(
            key="test/SURF-01",
            bare_id="SURF-01",
            milestone="test",
            capability="Methodology",
            deliverable_path="scripts/check-routing.py",
            coverage_tier="audit-only",
            artifact_link="",
            gap_rationale="test fixture",
        )


def test_empty_surfaces_detected() -> None:
    """A row with `surfaces=()` is flagged by check_consistency (D-06)."""
    mod = _load_check_traceability()
    row = mod.MatrixRow(
        key="test/SURF-02",
        bare_id="SURF-02",
        milestone="test",
        capability="Methodology",
        deliverable_path="scripts/check-routing.py",
        coverage_tier="audit-only",
        artifact_link="",
        gap_rationale="test fixture",
        surfaces=(),
        statement=mod._STATEMENT_UNRECOVERABLE,
    )
    issues = mod.check_consistency([row])
    assert issues, (
        f"Expected empty surfaces to be flagged; check_consistency returned: {issues!r}"
    )


def test_load_rows_retuples_surfaces() -> None:
    """load_rows() re-tuples `surfaces` after the JSON round-trip, so loaded rows
    stay hashable (Pitfall 2: a `list`-valued field would break
    @dataclass(frozen=True) hashability the first time anything hashes a row)."""
    mod = _load_check_traceability()
    phase_dir = (
        REPO
        / ".planning"
        / "phases"
        / "82-traceability-matrix-and-gap-findings"
    )
    md_out = phase_dir / "MATRIX.md"
    json_out = phase_dir / "matrix.json"
    result = subprocess.run(
        [
            sys.executable, str(SCRIPT), "emit",
            "--md-output", str(md_out),
            "--json-output", str(json_out),
        ],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, (
        f"emit failed (expected 0): returncode={result.returncode}\n"
        f"stdout:\n{result.stdout}\nstderr:\n{result.stderr}"
    )
    loaded_rows = mod.load_rows(json_out)
    assert all(isinstance(r.surfaces, tuple) for r in loaded_rows), (
        "Expected every loaded row's surfaces to be a tuple after the JSON "
        "round-trip"
    )
    assert len(set(loaded_rows)) == len(loaded_rows), (
        "Expected loaded rows to be hashable and unique (a list-valued surfaces "
        "field would raise TypeError on hash())"
    )


def test_matrixrow_requires_statement() -> None:
    """Omitting `statement` at construction raises TypeError (D-05: no default,
    required at every call site)."""
    mod = _load_check_traceability()
    with pytest.raises(TypeError):
        mod.MatrixRow(
            key="test/STMT-01",
            bare_id="STMT-01",
            milestone="test",
            capability="Methodology",
            deliverable_path="scripts/check-routing.py",
            coverage_tier="audit-only",
            artifact_link="",
            gap_rationale="test fixture",
            surfaces=("apparatus",),
        )


def test_blank_statement_detected() -> None:
    """A row with a blank statement is flagged by check_consistency (STMT-01)."""
    mod = _load_check_traceability()
    row = mod.MatrixRow(
        key="test/STMT-02",
        bare_id="STMT-02",
        milestone="test",
        capability="Methodology",
        deliverable_path="scripts/check-routing.py",
        coverage_tier="audit-only",
        artifact_link="",
        gap_rationale="test fixture",
        surfaces=("apparatus",),
        statement="   ",
    )
    issues = mod.check_consistency([row])
    assert issues, (
        f"Expected blank statement to be flagged; check_consistency returned: {issues!r}"
    )


def test_statement_pipe_escaped_in_markdown() -> None:
    """A literal `|` inside a statement is escaped in the rendered Matrix Table
    (D-07), so it cannot split the row into extra columns."""
    mod = _load_check_traceability()
    row = mod.MatrixRow(
        key="v8.18/STMT-PIPE",
        bare_id="STMT-PIPE",
        milestone="v8.18",
        capability="Methodology",
        deliverable_path="scripts/check-routing.py",
        coverage_tier="audit-only",
        artifact_link="",
        gap_rationale="test fixture",
        surfaces=("apparatus",),
        statement="left|right",
    )
    rendered = mod.render_matrix_markdown([row])
    assert r"left\|right" in rendered, (
        "Expected the literal | inside the statement to be escaped as \\|"
    )
    assert "| left|right |" not in rendered, (
        "Unescaped pipe leaked into the Markdown table"
    )


# ---------------------------------------------------------------------------
# T-81-01 path confinement: out-of-.planning/ outputs must exit 2
# ---------------------------------------------------------------------------


def test_output_path_confinement() -> None:
    """emit with an /tmp/... --md-output exits 2 and writes nothing (T-81-01)."""
    import os
    escape_md = "/tmp/escape-traceability-test-82.md"
    escape_json = "/tmp/escape-traceability-test-82.json"
    # Clean up from any prior failed run
    for p in (escape_md, escape_json):
        if os.path.exists(p):
            os.unlink(p)
    result = subprocess.run(
        [
            sys.executable, str(SCRIPT), "emit",
            "--md-output", escape_md,
            "--json-output", escape_json,
        ],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 2, (
        f"Expected exit 2 for escaping --md-output path, "
        f"got {result.returncode}.\n"
        f"stdout:\n{result.stdout}\n"
        f"stderr:\n{result.stderr}"
    )
    assert not os.path.exists(escape_md), (
        f"{escape_md!r} was created despite the confinement check (T-82-01 violated)"
    )


# ---------------------------------------------------------------------------
# GAP-01: active-tail emission guard
# ---------------------------------------------------------------------------


def test_active_tail_items_present() -> None:
    """GAP-01 emission guard: build_matrix_rows() must include 9 active-tail rows.

    The 9 active-tail rows (D-05 path b) are:
      bare IDs: GEN-01, GEN-02, RR-80-01, RR-79-01, RR-114-01, RR-108-02, RR-77-08,
      RR-108-04, RR-108-05
      (RR-80-01 = the former S-N04 residual, assigned its tracked ID in Phase 83)
      (RR-114-01 supersedes RR-108-01 supersedes RR-95-01 supersedes RR-92-01 supersedes RR-79-02,
       Phase 114 v7.6 carry-forward, S-P02 inversion CARRIED 1/5;
       full chain: RR-79-02 -> RR-92-01 -> RR-95-01 -> RR-108-01 -> RR-114-01)
      (RR-108-02 supersedes RR-95-02 supersedes RR-92-02 supersedes RR-79-03,
       Phase 108 v7.4 carry-forward, S-P05 trade-off; CLOSED at 4/5 ≥ min-pass
       at Phase 114 v7.6 re-baseline — lone canonical improver; ID retained,
       sentinel present in _battery_core.self_test_boundary() as regression guard;
       full chain: RR-79-03 -> RR-92-02 -> RR-95-02 -> RR-108-02 CLOSED)
      (RR-108-04 (S-P10 estimate) and RR-108-05 (S-P14 theoretical-limit): registered at
       Phase 33 RESID-01, ACCEPTED-FINAL at v8.0, re-opened and re-measured at v8.5,
       CARRIED 0/5 both, sentinel re-pointed to _load_excerpt_v85 at Phase 156)
      Each must be tagged:
        capability == "Test-Network"
        deliverable_path == "active-tail"

    All active-tail rows are now reproducible (GEN-01 flipped scheduled->reproducible
    in Phase 93, D-08; GEN-01 artifact_link bumped v6.3->v6.4 baseline in Phase 96,
    D-03; bumped v6.4->v7.4 baseline in Phase 109, D-04; bumped v7.4->v7.6 in Phase 114,
    Plan 02 (this phase); RR-114-01 renamed from RR-108-01 in Phase 114, Plan 02;
    RR-108-02 retained as CLOSED row — sentinel present, not removed; RR-108-04/RR-108-05
    registered reproducible at Phase 33 RESID-01).
    The coverage_tier check was removed for the general loop because tiers are mixed
    non-gap values across the whole active-tail set; RR-108-04/RR-108-05 get an explicit
    coverage_tier + artifact_link check below instead, since RESID-01 names those two
    values specifically.
    """
    mod = _load_check_traceability()
    rows = mod.build_matrix_rows()

    required_bare_ids = {
        "GEN-01", "GEN-02", "RR-80-01",
        "RR-79-01", "RR-114-01", "RR-108-02", "RR-77-08",
        "RR-108-04", "RR-108-05",
    }

    found_ids = {r.bare_id for r in rows}
    missing_ids = required_bare_ids - found_ids
    assert not missing_ids, (
        f"Active-tail rows missing from build_matrix_rows(): {sorted(missing_ids)!r}. "
        f"Found bare_ids: {sorted(found_ids)!r}"
    )

    # Each active-tail row must be tagged Test-Network + active-tail
    # (coverage_tier check removed: all rows are now non-gap; see docstring)
    errors: list[str] = []
    for row in rows:
        if row.bare_id not in required_bare_ids:
            continue
        if row.capability != "Test-Network":
            errors.append(
                f"{row.bare_id}: expected capability='Test-Network', "
                f"got {row.capability!r}"
            )
        if row.deliverable_path != "active-tail":
            errors.append(
                f"{row.bare_id}: expected deliverable_path='active-tail', "
                f"got {row.deliverable_path!r}"
            )
    assert not errors, (
        f"Active-tail row tagging errors:\n" + "\n".join(errors)
    )

    # RESID-01: RR-108-04 and RR-108-05 specifically must be reproducible, tagged
    # residual/ keys, and carry the _battery_core.py#self_test_boundary sentinel link.
    resid_ids = {"RR-108-04", "RR-108-05"}
    resid_rows = {r.bare_id: r for r in rows if r.bare_id in resid_ids}
    missing_resid = resid_ids - resid_rows.keys()
    assert not missing_resid, (
        f"RESID-01 rows missing from build_matrix_rows(): {sorted(missing_resid)!r}"
    )
    resid_errors: list[str] = []
    for bare_id, row in resid_rows.items():
        if row.key != f"residual/{bare_id}":
            resid_errors.append(
                f"{bare_id}: expected key='residual/{bare_id}', got {row.key!r}"
            )
        if row.coverage_tier != "reproducible":
            resid_errors.append(
                f"{bare_id}: expected coverage_tier='reproducible', "
                f"got {row.coverage_tier!r}"
            )
        if row.artifact_link != "scripts/_battery_core.py#self_test_boundary":
            resid_errors.append(
                f"{bare_id}: expected artifact_link="
                f"'scripts/_battery_core.py#self_test_boundary', "
                f"got {row.artifact_link!r}"
            )
    assert not resid_errors, (
        f"RESID-01 row field errors:\n" + "\n".join(resid_errors)
    )


# ---------------------------------------------------------------------------
# Phase 33 ROWS-01: v8.19/v8.20/v8.21 milestone rows registered in build order
# ---------------------------------------------------------------------------


def test_v819_v820_v821_milestone_rows_present() -> None:
    """ROWS-01 gap test: build_matrix_rows() must carry exactly the 24 v8.19/
    v8.20/v8.21 milestone keys, each exactly once, positioned between the last
    v8.18 row and the first v8.24 row in build order, each with a non-empty
    sourced statement (never the _STATEMENT_UNRECOVERABLE sentinel — every row
    in these three batches is either Methodology rubric prose or a quoted
    requirement-archive bullet, per _rows_v819()/_rows_v820()/_rows_v821()'s
    own docstrings).
    """
    mod = _load_check_traceability()
    rows = mod.build_matrix_rows()

    expected_keys = {
        "v8.19/HC-01", "v8.19/HC-02", "v8.19/HC-03", "v8.19/HC-04",
        "v8.20/HARN-01-01", "v8.20/HARN-01-02", "v8.20/HARN-01-03",
        "v8.20/HARN-01-04", "v8.20/HARN-01-05",
        "v8.21/REG-01", "v8.21/REG-02", "v8.21/REG-03",
        "v8.21/REG-04", "v8.21/REG-05", "v8.21/REG-06",
        "v8.21/GATE-01", "v8.21/GATE-02", "v8.21/GATE-03",
        "v8.21/GATE-04", "v8.21/GATE-05", "v8.21/GATE-06",
        "v8.21/VAL-01", "v8.21/VAL-02", "v8.21/VAL-03",
    }
    assert len(expected_keys) == 24, "expected-key roster itself must be 24 entries"

    all_keys = [r.key for r in rows]
    found_keys = set(all_keys)
    missing = expected_keys - found_keys
    assert not missing, (
        f"ROWS-01 milestone rows missing from build_matrix_rows(): {sorted(missing)!r}"
    )

    # Each expected key must appear exactly once (no accidental duplication).
    dup_errors = [
        k for k in expected_keys
        if all_keys.count(k) != 1
    ]
    assert not dup_errors, (
        f"ROWS-01 keys not appearing exactly once: {sorted(dup_errors)!r} "
        f"(counts: {[(k, all_keys.count(k)) for k in dup_errors]!r})"
    )

    # Ordering: every v8.19/v8.20/v8.21 row's index must sit strictly between the
    # last v8.18 row's index and the first v8.24 row's index.
    v818_indices = [i for i, r in enumerate(rows) if r.milestone == "v8.18"]
    v824_indices = [i for i, r in enumerate(rows) if r.milestone == "v8.24"]
    assert v818_indices, "No v8.18 rows found in build_matrix_rows() — cannot bound order"
    assert v824_indices, "No v8.24 rows found in build_matrix_rows() — cannot bound order"
    last_v818 = max(v818_indices)
    first_v824 = min(v824_indices)

    order_errors: list[str] = []
    for i, r in enumerate(rows):
        if r.key in expected_keys:
            if not (last_v818 < i < first_v824):
                order_errors.append(
                    f"{r.key} at index {i} is not strictly between last v8.18 row "
                    f"(index {last_v818}) and first v8.24 row (index {first_v824})"
                )
    assert not order_errors, (
        "ROWS-01 build-order errors:\n" + "\n".join(order_errors)
    )

    # Every row must carry a non-empty, non-sentinel statement.
    stmt_errors: list[str] = []
    for r in rows:
        if r.key in expected_keys:
            stmt = r.statement
            if not stmt or not stmt.strip():
                stmt_errors.append(f"{r.key}: statement is empty/blank")
            elif stmt.strip() == mod._STATEMENT_UNRECOVERABLE:
                stmt_errors.append(
                    f"{r.key}: statement is the _STATEMENT_UNRECOVERABLE sentinel, "
                    f"expected a sourced statement"
                )
    assert not stmt_errors, (
        "ROWS-01 statement errors:\n" + "\n".join(stmt_errors)
    )


# ---------------------------------------------------------------------------
# Phase 33 ROWS-03: reproducible rows cite the three named scripts directly
# ---------------------------------------------------------------------------


def test_rows03_reproducible_rows_cite_new_scripts() -> None:
    """ROWS-03 gap test: at least one `reproducible` row's artifact_link (path
    before any `#`) equals each of scripts/check-high-confidence-bound.py,
    scripts/check-registration.py and scripts/check-act-limb.py.

    Deliberately does not pin exact counts (moving figures; CR-01 moved
    REG-GUARD's) and deliberately does not assert v8.21/REG-06's tier (it is
    audit-only since CR-01, not reproducible).
    """
    mod = _load_check_traceability()
    rows = mod.build_matrix_rows()

    required_scripts = {
        "scripts/check-high-confidence-bound.py",
        "scripts/check-registration.py",
        "scripts/check-act-limb.py",
    }

    reproducible_link_paths = {
        r.artifact_link.split("#", 1)[0]
        for r in rows
        if r.coverage_tier == "reproducible" and r.artifact_link
    }

    missing_scripts = required_scripts - reproducible_link_paths
    assert not missing_scripts, (
        f"No reproducible row cites these scripts directly as artifact_link: "
        f"{sorted(missing_scripts)!r}. "
        f"Reproducible artifact_link paths found: {sorted(reproducible_link_paths)!r}"
    )

    # REG-06 must not be relied on as the reproducible evidence for check-registration.py —
    # it is audit-only since CR-01 (Phase 33 code review).
    reg06_rows = [r for r in rows if r.key == "v8.21/REG-06"]
    assert reg06_rows, "v8.21/REG-06 row not found"
    assert reg06_rows[0].coverage_tier == "audit-only", (
        f"v8.21/REG-06 expected coverage_tier='audit-only' (CR-01), "
        f"got {reg06_rows[0].coverage_tier!r}"
    )


if __name__ == "__main__":
    import pytest
    sys.exit(pytest.main([__file__, "-v"]))
