#!/usr/bin/env python3
"""Tests for Phase 69: migrated merged-baseline invariant guards (BATT-08).

Supersedes test_66's two-file v4.2 guards by asserting over the single merged v4.3
baseline. The anti-masking guarantees (no --p-threshold 0 mask, no silent fixture drift,
falsifiable verdict cells) carry forward onto the merged battery surface.

Requirements covered:
  BATT-08 — Nyquist invariant tests migrated to target the merged battery / v4.3 baseline

This module defines 20 test functions: 8 file-level guards, 4 boundary-row checks,
5 focused-row checks, and 3 self-check / anti-falsifiability tests.

Note: The live battery run (BATT-07) is recorded in the baseline file itself. These tests
guard the committed baseline content so structural drift is caught immediately.

Run from repo root:
    python3 -m pytest tests/test_69_merged_baseline_invariants.py -v
"""

from __future__ import annotations

import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
TESTS = REPO / "tests"
BASELINE_V43 = TESTS / "routing-battery-baseline-v4.3.md"


# ---------------------------------------------------------------------------
# File-level guards
# ---------------------------------------------------------------------------

def test_baseline_v43_exists() -> None:
    """tests/routing-battery-baseline-v4.3.md must exist."""
    assert BASELINE_V43.exists(), (
        f"routing-battery-baseline-v4.3.md not found at {BASELINE_V43}"
    )


def test_baseline_v43_minimum_length() -> None:
    """routing-battery-baseline-v4.3.md must be at least 60 lines (merged file is longer than either v4.2 file)."""
    lines = BASELINE_V43.read_text(encoding="utf-8").splitlines()
    assert len(lines) >= 60, (
        f"routing-battery-baseline-v4.3.md is only {len(lines)} lines (need >= 60)"
    )


# ---------------------------------------------------------------------------
# Anti-masking guards — BATTERY: PASS, masked-threshold audit, lineage
# ---------------------------------------------------------------------------

def test_baseline_v43_battery_pass_verdict() -> None:
    """routing-battery-baseline-v4.3.md must contain 'BATTERY: PASS'."""
    text = BASELINE_V43.read_text(encoding="utf-8")
    assert "BATTERY: PASS" in text, (
        "routing-battery-baseline-v4.3.md does not contain 'BATTERY: PASS'"
    )


def test_baseline_v43_has_masked_threshold_audit_attestation() -> None:
    """Header must contain the pre-run masked-threshold audit attestation line (D-04)."""
    text = BASELINE_V43.read_text(encoding="utf-8")
    assert "masked-threshold audit" in text, (
        "routing-battery-baseline-v4.3.md missing 'masked-threshold audit' attestation"
    )


def test_baseline_v43_run_flags_contain_namespaced_focused_thresholds() -> None:
    """Run flags line must contain the namespaced '--focused-p-threshold 4 --focused-n-threshold 1' (Landmine 5)."""
    text = BASELINE_V43.read_text(encoding="utf-8")
    assert "--focused-p-threshold 4 --focused-n-threshold 1" in text, (
        "routing-battery-baseline-v4.3.md does not record the namespaced run flag "
        "'--focused-p-threshold 4 --focused-n-threshold 1'"
    )


def test_baseline_v43_lineage_mentions_supersedes() -> None:
    """Lineage section must mention 'supersedes'."""
    text = BASELINE_V43.read_text(encoding="utf-8")
    assert "supersedes" in text, (
        "routing-battery-baseline-v4.3.md lineage does not mention 'supersedes'"
    )


def test_baseline_v43_lineage_mentions_fu21_diagnosis() -> None:
    """Lineage section must mention the fu21-fixture-contradiction-diagnosis document."""
    text = BASELINE_V43.read_text(encoding="utf-8")
    assert "fu21-fixture-contradiction-diagnosis" in text, (
        "routing-battery-baseline-v4.3.md lineage does not reference "
        "'fu21-fixture-contradiction-diagnosis'"
    )


def test_baseline_v43_lineage_mentions_commit_151b197() -> None:
    """Lineage must attribute the focused-output detector fix to commit 151b197."""
    text = BASELINE_V43.read_text(encoding="utf-8")
    assert "151b197" in text, (
        "routing-battery-baseline-v4.3.md lineage does not mention commit 151b197"
    )


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _check_baseline_row(text: str, row_id: str, kn_value: str, verdict: str) -> None:
    """Assert that a boundary table row has the expected Boundary K/N and Verdict cells.

    Cell-anchored (CR-01): splits the matched line on '|' and checks EXACT equality on
    cell index 4 (Boundary K/N) and cell index 6 (Both-Match Verdict). This prevents two
    proven leak vectors on the merged table:
      - '5/5 FAIL' passing a substring '5/5' check on the K/N cell
      - 'FAIL' verdict passing because 'PASS' leaks from the Focused K/N cell (index 5)

    Column layout after split on '|' and strip (indices):
      [0]="" [1]=row_id [2]=Expected Boundary [3]=Expected Output
      [4]=Boundary K/N [5]=Focused K/N [6]=Both-Match Verdict [7]=""
    """
    MIN_CELLS = 7  # need at least index 6 to be present
    for line in text.splitlines():
        if f"| {row_id} " in line or f"| {row_id}  " in line:
            cells = [c.strip() for c in line.split("|")]
            if len(cells) < MIN_CELLS + 1:
                raise AssertionError(
                    f"Row {row_id}: malformed line — expected at least {MIN_CELLS + 1} "
                    f"pipe-delimited cells, got {len(cells)}: {line!r}"
                )
            actual_kn = cells[4]
            actual_verdict = cells[6]
            assert actual_kn == kn_value, (
                f"Row {row_id}: Boundary K/N cell (index 4) is {actual_kn!r}, "
                f"expected {kn_value!r}. Full line: {line!r}"
            )
            assert actual_verdict == verdict, (
                f"Row {row_id}: Verdict cell (index 6) is {actual_verdict!r}, "
                f"expected {verdict!r}. Full line: {line!r}"
            )
            return
    raise AssertionError(
        f"Row '{row_id}' not found in baseline"
    )


def _check_focused_row(text: str, row_id: str) -> None:
    """Assert that a row contains a falsifiable '<n>/5 PASS' cell.

    Tightened (Landmine 4): the loose 'PASS in line' fallback is NOT inherited.
    A row reading '2/5 FAIL' MUST fail this assertion.
    """
    for line in text.splitlines():
        if f"| {row_id} " in line or f"| {row_id}  " in line:
            has_kn = any(f"{k}/5 PASS" in line for k in range(1, 6))
            assert has_kn, (
                f"Row {row_id}: no falsifiable '<n>/5 PASS' cell found in: {line!r}"
            )
            return
    raise AssertionError(f"Row '{row_id}' not found in routing-battery-baseline-v4.3.md")


# ---------------------------------------------------------------------------
# Boundary rows (B-P12, B-P24, B-N1, B-N2) — must be 5/5 PASS
# ---------------------------------------------------------------------------

def test_baseline_v43_row_b_p12_5of5_pass() -> None:
    """B-P12 boundary row must have K/N '5/5' and Verdict 'PASS'."""
    text = BASELINE_V43.read_text(encoding="utf-8")
    _check_baseline_row(text, "B-P12", "5/5", "PASS")


def test_baseline_v43_row_b_p24_5of5_pass() -> None:
    """B-P24 boundary row must have K/N '5/5' and Verdict 'PASS'."""
    text = BASELINE_V43.read_text(encoding="utf-8")
    _check_baseline_row(text, "B-P24", "5/5", "PASS")


def test_baseline_v43_row_b_n1_5of5_pass() -> None:
    """B-N1 boundary row must have K/N '5/5' and Verdict 'PASS'."""
    text = BASELINE_V43.read_text(encoding="utf-8")
    _check_baseline_row(text, "B-N1", "5/5", "PASS")


def test_baseline_v43_row_b_n2_5of5_pass() -> None:
    """B-N2 boundary row must have K/N '5/5' and Verdict 'PASS'."""
    text = BASELINE_V43.read_text(encoding="utf-8")
    _check_baseline_row(text, "B-N2", "5/5", "PASS")


# ---------------------------------------------------------------------------
# Focused rows (F-P12, F-P24, F-P25, F-P26, F-N1) — must have <n>/5 PASS cell
# ---------------------------------------------------------------------------

def test_baseline_v43_row_f_p12_has_pass_cell() -> None:
    """F-P12 focused row must have a falsifiable '<n>/5 PASS' cell."""
    text = BASELINE_V43.read_text(encoding="utf-8")
    _check_focused_row(text, "F-P12")


def test_baseline_v43_row_f_p24_has_pass_cell() -> None:
    """F-P24 focused row must have a falsifiable '<n>/5 PASS' cell."""
    text = BASELINE_V43.read_text(encoding="utf-8")
    _check_focused_row(text, "F-P24")


def test_baseline_v43_row_f_p25_has_pass_cell() -> None:
    """F-P25 focused row must have a falsifiable '<n>/5 PASS' cell."""
    text = BASELINE_V43.read_text(encoding="utf-8")
    _check_focused_row(text, "F-P25")


def test_baseline_v43_row_f_p26_has_pass_cell() -> None:
    """F-P26 focused row must have a falsifiable '<n>/5 PASS' cell."""
    text = BASELINE_V43.read_text(encoding="utf-8")
    _check_focused_row(text, "F-P26")


def test_baseline_v43_row_f_n1_has_pass_cell() -> None:
    """F-N1 focused row must have a falsifiable '<n>/5 PASS' cell."""
    text = BASELINE_V43.read_text(encoding="utf-8")
    _check_focused_row(text, "F-N1")


# ---------------------------------------------------------------------------
# Anti-falsifiability self-check — confirm _check_focused_row rejects 2/5 FAIL
# ---------------------------------------------------------------------------

def test_check_focused_row_is_falsifiable() -> None:
    """_check_focused_row must raise AssertionError when a focused cell reads '2/5 FAIL'.

    This self-check confirms the tightened helper is falsifiable: a malformed baseline
    row with a FAIL verdict must fail the gate (not pass silently).
    """
    malformed_table = (
        "| #     | Expected Boundary | Expected Output    | Boundary K/N | Focused K/N | Both-Match Verdict |\n"
        "|-------|-------------------|--------------------|--------------|-------------|--------------------|\n"
        "| F-P12 | n-a               | focused-pre-mortem | n-a          | 2/5 FAIL    | FAIL               |\n"
    )
    try:
        _check_focused_row(malformed_table, "F-P12")
    except AssertionError:
        pass  # Expected — the helper correctly rejects a 2/5 FAIL cell
    else:
        raise AssertionError(
            "_check_focused_row did not raise for a '2/5 FAIL' cell — "
            "the tightened falsifiability check is broken"
        )


# ---------------------------------------------------------------------------
# Anti-falsifiability self-check — confirm _check_baseline_row rejects leak vectors
# ---------------------------------------------------------------------------

def test_check_baseline_row_is_falsifiable_kn_leak() -> None:
    """_check_baseline_row must raise when Boundary K/N cell reads '5/5 FAIL' (leak vector 1).

    A row with '5/5 FAIL' in the Boundary K/N cell must NOT satisfy the gate, even though
    '5/5' is a substring of '5/5 FAIL'. The cell-anchored check must reject this row.
    """
    malformed_table = (
        "| #     | Expected Boundary | Expected Output | Boundary K/N | Focused K/N | Both-Match Verdict |\n"
        "|-------|-------------------|-----------------|--------------|-------------|--------------------|\n"
        "| B-P12 | none-or-other     | n-a             | 5/5 FAIL     | n-a         | PASS               |\n"
    )
    try:
        _check_baseline_row(malformed_table, "B-P12", "5/5", "PASS")
    except AssertionError:
        pass  # Expected — the cell-anchored check correctly rejects '5/5 FAIL' != '5/5'
    else:
        raise AssertionError(
            "_check_baseline_row did not raise for a '5/5 FAIL' Boundary K/N cell — "
            "the cell-anchored K/N check is broken (CR-01 leak vector 1)"
        )


def test_check_baseline_row_is_falsifiable_verdict_leak() -> None:
    """_check_baseline_row must raise when Verdict cell reads 'FAIL' (leak vector 2).

    A row with a 'FAIL' Verdict cell must NOT pass, even though 'PASS' is present as a
    substring in the Focused K/N cell (index 5). The cell-anchored check must isolate
    the Verdict at index 6 and reject it.
    """
    malformed_table = (
        "| #     | Expected Boundary | Expected Output | Boundary K/N | Focused K/N | Both-Match Verdict |\n"
        "|-------|-------------------|-----------------|--------------|-------------|--------------------|\n"
        "| B-P12 | none-or-other     | n-a             | 5/5          | 3/5 PASS    | FAIL               |\n"
    )
    try:
        _check_baseline_row(malformed_table, "B-P12", "5/5", "PASS")
    except AssertionError:
        pass  # Expected — the cell-anchored check correctly rejects 'FAIL' != 'PASS' at index 6
    else:
        raise AssertionError(
            "_check_baseline_row did not raise for a 'FAIL' Verdict cell with 'PASS' leaking "
            "from the Focused K/N cell — the cell-anchored verdict check is broken (CR-01 leak vector 2)"
        )


if __name__ == "__main__":
    import pytest
    sys.exit(pytest.main([__file__, "-v"]))
