#!/usr/bin/env python3
"""Tests for Phase 66: committed baseline invariant guards.

Requirements covered:
  STRICT-02 / BASE-01 — sub-skill-routing-baseline-v4.2.md structural invariants
  STRICT-02 / BASE-02 — focused-output-baseline-v4.2.md structural invariants

Note: The live battery runs (STRICT-02/BASE-01/BASE-02 live PASS evidence) are
recorded in the baseline files themselves. Re-running costs ~25 claude sessions
and is documented as manual-only. These tests guard the committed baseline
content so structural drift is caught immediately.

Run from repo root:
    python3 -m pytest tests/test_66_baseline_invariants.py -v
"""

from __future__ import annotations

import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
TESTS = REPO / "tests"
SUB_SKILL_BASELINE_V42 = TESTS / "sub-skill-routing-baseline-v4.2.md"
FOCUSED_BASELINE_V42 = TESTS / "focused-output-baseline-v4.2.md"


# ---------------------------------------------------------------------------
# BASE-01: sub-skill-routing-baseline-v4.2.md
# ---------------------------------------------------------------------------

def test_sub_skill_baseline_v42_exists() -> None:
    """tests/sub-skill-routing-baseline-v4.2.md must exist."""
    assert SUB_SKILL_BASELINE_V42.exists(), (
        f"sub-skill-routing-baseline-v4.2.md not found at {SUB_SKILL_BASELINE_V42}"
    )


def test_sub_skill_baseline_v42_minimum_length() -> None:
    """sub-skill-routing-baseline-v4.2.md must be at least 40 lines."""
    lines = SUB_SKILL_BASELINE_V42.read_text(encoding="utf-8").splitlines()
    assert len(lines) >= 40, (
        f"sub-skill-routing-baseline-v4.2.md is only {len(lines)} lines (need >= 40)"
    )


def test_sub_skill_baseline_v42_battery_pass_verdict() -> None:
    """sub-skill-routing-baseline-v4.2.md must contain 'BATTERY: PASS'."""
    text = SUB_SKILL_BASELINE_V42.read_text(encoding="utf-8")
    assert "BATTERY: PASS" in text, (
        "sub-skill-routing-baseline-v4.2.md does not contain 'BATTERY: PASS'"
    )


def _check_baseline_row(text: str, row_id: str, kn_value: str, verdict: str) -> None:
    """Assert that a table row contains the expected K/N and verdict cells."""
    for line in text.splitlines():
        if f"| {row_id} " in line or f"| {row_id}  " in line:
            assert kn_value in line, (
                f"Row {row_id}: expected K/N cell '{kn_value}' not found in: {line!r}"
            )
            assert verdict in line, (
                f"Row {row_id}: expected Verdict '{verdict}' not found in: {line!r}"
            )
            return
    raise AssertionError(
        f"Row '{row_id}' not found in baseline"
    )


def test_sub_skill_baseline_v42_row_p12_5of5_pass() -> None:
    """P12 row must have K/N '5/5' and Verdict 'PASS'."""
    text = SUB_SKILL_BASELINE_V42.read_text(encoding="utf-8")
    _check_baseline_row(text, "P12", "5/5", "PASS")


def test_sub_skill_baseline_v42_row_p24_5of5_pass() -> None:
    """P24 row must have K/N '5/5' and Verdict 'PASS'."""
    text = SUB_SKILL_BASELINE_V42.read_text(encoding="utf-8")
    _check_baseline_row(text, "P24", "5/5", "PASS")


def test_sub_skill_baseline_v42_row_n1_5of5_pass() -> None:
    """N1 row must have K/N '5/5' and Verdict 'PASS'."""
    text = SUB_SKILL_BASELINE_V42.read_text(encoding="utf-8")
    _check_baseline_row(text, "N1", "5/5", "PASS")


def test_sub_skill_baseline_v42_row_n2_5of5_pass() -> None:
    """N2 row must have K/N '5/5' and Verdict 'PASS'."""
    text = SUB_SKILL_BASELINE_V42.read_text(encoding="utf-8")
    _check_baseline_row(text, "N2", "5/5", "PASS")


def test_sub_skill_baseline_v42_has_masked_threshold_audit_attestation() -> None:
    """Header must contain the pre-run masked-threshold audit attestation line."""
    text = SUB_SKILL_BASELINE_V42.read_text(encoding="utf-8")
    assert "masked-threshold audit" in text, (
        "sub-skill-routing-baseline-v4.2.md missing 'masked-threshold audit' attestation"
    )


def test_sub_skill_baseline_v42_lineage_mentions_supersedes() -> None:
    """Lineage section must mention 'supersedes'."""
    text = SUB_SKILL_BASELINE_V42.read_text(encoding="utf-8")
    assert "supersedes" in text, (
        "sub-skill-routing-baseline-v4.2.md lineage does not mention 'supersedes'"
    )


def test_sub_skill_baseline_v42_lineage_mentions_fu21_diagnosis() -> None:
    """Lineage section must mention the fu21-fixture-contradiction-diagnosis document."""
    text = SUB_SKILL_BASELINE_V42.read_text(encoding="utf-8")
    assert "fu21-fixture-contradiction-diagnosis" in text, (
        "sub-skill-routing-baseline-v4.2.md lineage does not reference "
        "fu21-fixture-contradiction-diagnosis"
    )


# ---------------------------------------------------------------------------
# BASE-02: focused-output-baseline-v4.2.md
# ---------------------------------------------------------------------------

def test_focused_baseline_v42_exists() -> None:
    """tests/focused-output-baseline-v4.2.md must exist."""
    assert FOCUSED_BASELINE_V42.exists(), (
        f"focused-output-baseline-v4.2.md not found at {FOCUSED_BASELINE_V42}"
    )


def test_focused_baseline_v42_minimum_length() -> None:
    """focused-output-baseline-v4.2.md must be at least 45 lines."""
    lines = FOCUSED_BASELINE_V42.read_text(encoding="utf-8").splitlines()
    assert len(lines) >= 45, (
        f"focused-output-baseline-v4.2.md is only {len(lines)} lines (need >= 45)"
    )


def test_focused_baseline_v42_battery_pass_verdict() -> None:
    """focused-output-baseline-v4.2.md must contain 'BATTERY: PASS'."""
    text = FOCUSED_BASELINE_V42.read_text(encoding="utf-8")
    assert "BATTERY: PASS" in text, (
        "focused-output-baseline-v4.2.md does not contain 'BATTERY: PASS'"
    )


def _check_focused_row(text: str, row_id: str) -> None:
    """Assert that a row contains a falsifiable '<n>/5 PASS' cell."""
    for line in text.splitlines():
        # Match table rows with the given ID (allow trailing spaces)
        if f"| {row_id} " in line or f"| {row_id}  " in line:
            # Must contain some variant of '<n>/5 PASS'
            has_kn = any(f"{k}/5 PASS" in line for k in range(1, 6))
            # Also accept plain 5/5 PASS (as Verdict cell alone)
            if not has_kn:
                has_kn = "5/5 PASS" in line or "PASS" in line
            assert has_kn, (
                f"Row {row_id}: no falsifiable '<n>/5 PASS' cell found in: {line!r}"
            )
            return
    raise AssertionError(f"Row '{row_id}' not found in focused-output-baseline-v4.2.md")


def test_focused_baseline_v42_row_p12_has_pass_cell() -> None:
    """P12 row must have a falsifiable PASS cell."""
    text = FOCUSED_BASELINE_V42.read_text(encoding="utf-8")
    _check_focused_row(text, "P12")


def test_focused_baseline_v42_row_p24_has_pass_cell() -> None:
    """P24 row must have a falsifiable PASS cell."""
    text = FOCUSED_BASELINE_V42.read_text(encoding="utf-8")
    _check_focused_row(text, "P24")


def test_focused_baseline_v42_row_p25_has_pass_cell() -> None:
    """P25 row must have a falsifiable PASS cell."""
    text = FOCUSED_BASELINE_V42.read_text(encoding="utf-8")
    _check_focused_row(text, "P25")


def test_focused_baseline_v42_row_p26_has_pass_cell() -> None:
    """P26 row must have a falsifiable PASS cell."""
    text = FOCUSED_BASELINE_V42.read_text(encoding="utf-8")
    _check_focused_row(text, "P26")


def test_focused_baseline_v42_row_n1_has_pass_cell() -> None:
    """N1 row must have a falsifiable PASS cell."""
    text = FOCUSED_BASELINE_V42.read_text(encoding="utf-8")
    _check_focused_row(text, "N1")


def test_focused_baseline_v42_has_masked_threshold_audit_attestation() -> None:
    """Header must contain the pre-run masked-threshold audit attestation line."""
    text = FOCUSED_BASELINE_V42.read_text(encoding="utf-8")
    assert "masked-threshold audit" in text, (
        "focused-output-baseline-v4.2.md missing 'masked-threshold audit' attestation"
    )


def test_focused_baseline_v42_run_flags_contain_p_threshold_4_n_threshold_1() -> None:
    """Run flags line must contain '--p-threshold 4 --n-threshold 1'."""
    text = FOCUSED_BASELINE_V42.read_text(encoding="utf-8")
    assert "--p-threshold 4 --n-threshold 1" in text, (
        "focused-output-baseline-v4.2.md does not record run flag '--p-threshold 4 --n-threshold 1'"
    )


def test_focused_baseline_v42_lineage_mentions_supersession() -> None:
    """Lineage section must mention supersession of v3.8."""
    text = FOCUSED_BASELINE_V42.read_text(encoding="utf-8")
    assert "supersedes" in text, (
        "focused-output-baseline-v4.2.md lineage does not mention 'supersedes'"
    )


def test_focused_baseline_v42_lineage_mentions_commit_151b197() -> None:
    """Lineage must attribute Phase 66-03 fix to commit 151b197."""
    text = FOCUSED_BASELINE_V42.read_text(encoding="utf-8")
    assert "151b197" in text, (
        "focused-output-baseline-v4.2.md lineage does not mention commit 151b197"
    )


if __name__ == "__main__":
    import pytest
    sys.exit(pytest.main([__file__, "-v"]))
