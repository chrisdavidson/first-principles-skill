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
    """GAP-01 emission guard: build_matrix_rows() must include 7 active-tail rows.

    The 7 active-tail rows (D-05 path b) are:
      bare IDs: GEN-01, GEN-02, RR-80-01, RR-79-01, RR-95-01, RR-95-02, RR-77-08
      (RR-80-01 = the former S-N04 residual, assigned its tracked ID in Phase 83)
      (RR-95-01 supersedes RR-92-01 supersedes RR-79-02, Phase 95 v6.4 carry-forward,
       S-P02 inversion CARRIED 1/5; full chain: RR-79-02 -> RR-92-01 -> RR-95-01)
      (RR-95-02 supersedes RR-92-02 supersedes RR-79-03, Phase 95 v6.4 carry-forward,
       S-P05 trade-off CARRIED 2/5; full chain: RR-79-03 -> RR-92-02 -> RR-95-02)
      Each must be tagged:
        capability == "Test-Network"
        deliverable_path == "active-tail"

    All active-tail rows are now reproducible (GEN-01 flipped scheduled->reproducible
    in Phase 93, D-08; GEN-01 artifact_link bumped v6.3->v6.4 baseline in Phase 96,
    D-03; RR-95-01/02 renamed from RR-92-01/02 in Phase 96, Plan 03).
    The coverage_tier check was removed because tiers are now mixed non-gap values
    (reproducible for all 7 rows after the Phase 93 GEN-01 flip).
    """
    mod = _load_check_traceability()
    rows = mod.build_matrix_rows()

    required_bare_ids = {
        "GEN-01", "GEN-02", "RR-80-01",
        "RR-79-01", "RR-95-01", "RR-95-02", "RR-77-08",
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


if __name__ == "__main__":
    import pytest
    sys.exit(pytest.main([__file__, "-v"]))
