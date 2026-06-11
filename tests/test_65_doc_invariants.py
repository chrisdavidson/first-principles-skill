#!/usr/bin/env python3
"""Tests for Phase 65: fixture and documentation-correction invariants.

Requirements covered:
  CAT-01..04 — sub-skill catalog rows and header correctness
  FOCUS-01..03 — focused-output catalog dry-run parse + content
  STRICT-01 — no active --p-threshold 0 in docs/scripts/catalogs
  SUPERSEDED banners — v3.8 and v3.12 baselines carry banners
  Self-tests — both verifier --self-test exits pass
  Script defaults — check-sub-skill-routing.py p-threshold default=2, no --p-threshold 0

Run from repo root:
    python3 -m pytest tests/test_65_doc_invariants.py -v
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
TESTS = REPO / "tests"
SCRIPTS = REPO / "scripts"
CLAUDE_MD = REPO / "CLAUDE.md"
SUB_SKILL_CATALOG = TESTS / "sub-skill-routing-catalog.md"
FOCUSED_CATALOG = TESTS / "focused-output-catalog.md"
SUB_SKILL_BASELINE_V38 = TESTS / "sub-skill-routing-baseline-v3.8.md"
FOCUSED_BASELINE_V38 = TESTS / "focused-output-baseline-v3.8.md"
ROUTING_BASELINE_V312 = TESTS / "routing-baseline-v3.12.md"
CHECK_SUB_SKILL = SCRIPTS / "check-sub-skill-routing.py"
CHECK_FOCUSED = SCRIPTS / "check-focused-output.py"


# ---------------------------------------------------------------------------
# CAT-01: sub-skill catalog rows P12/P24/N2 all expect none-or-other
# ---------------------------------------------------------------------------

def test_sub_skill_catalog_p12_expects_none_or_other() -> None:
    """P12 row in sub-skill catalog must expect none-or-other (not direct sub-skill)."""
    text = SUB_SKILL_CATALOG.read_text(encoding="utf-8")
    # The row starts with "| P12 |" — find it and check expectation cell
    for line in text.splitlines():
        if line.strip().startswith("| P12 |"):
            assert "none-or-other" in line, (
                f"P12 row does not contain 'none-or-other': {line!r}"
            )
            return
    raise AssertionError("Row P12 not found in sub-skill-routing-catalog.md")


def test_sub_skill_catalog_p24_expects_none_or_other() -> None:
    """P24 row in sub-skill catalog must expect none-or-other."""
    text = SUB_SKILL_CATALOG.read_text(encoding="utf-8")
    for line in text.splitlines():
        if line.strip().startswith("| P24 |"):
            assert "none-or-other" in line, (
                f"P24 row does not contain 'none-or-other': {line!r}"
            )
            return
    raise AssertionError("Row P24 not found in sub-skill-routing-catalog.md")


def test_sub_skill_catalog_n2_expects_none_or_other() -> None:
    """N2 row in sub-skill catalog must expect none-or-other (not pre-mortem)."""
    text = SUB_SKILL_CATALOG.read_text(encoding="utf-8")
    for line in text.splitlines():
        if line.strip().startswith("| N2 |"):
            assert "none-or-other" in line, (
                f"N2 row does not contain 'none-or-other': {line!r}"
            )
            return
    raise AssertionError("Row N2 not found in sub-skill-routing-catalog.md")


# ---------------------------------------------------------------------------
# CAT-02: sub-skill catalog header references check-focused-output and disable-model-invocation
# ---------------------------------------------------------------------------

def test_sub_skill_catalog_header_references_focused_output_script() -> None:
    """Catalog header must mention check-focused-output (FU-21 gate lives there)."""
    text = SUB_SKILL_CATALOG.read_text(encoding="utf-8")
    assert "check-focused-output" in text, (
        "sub-skill-routing-catalog.md does not reference check-focused-output"
    )


def test_sub_skill_catalog_header_references_disable_model_invocation() -> None:
    """Catalog must mention disable-model-invocation to document Path 2 architecture."""
    text = SUB_SKILL_CATALOG.read_text(encoding="utf-8")
    assert "disable-model-invocation" in text, (
        "sub-skill-routing-catalog.md does not mention disable-model-invocation"
    )


def test_sub_skill_catalog_header_has_no_must_start_passing() -> None:
    """Catalog header must NOT contain 'must start PASSing' (v3.8 bad instruction removed)."""
    text = SUB_SKILL_CATALOG.read_text(encoding="utf-8")
    assert "must start PASSing" not in text, (
        "sub-skill-routing-catalog.md still contains old 'must start PASSing' instruction"
    )


# ---------------------------------------------------------------------------
# FOCUS-01: focused-output catalog dry-run parses as 4 P-prompts, 1 N-prompt
# ---------------------------------------------------------------------------

def test_focused_output_catalog_dry_run_parses_4p_1n() -> None:
    """check-focused-output.py --dry-run must report '4 P-prompts, 1 N-prompts'."""
    result = subprocess.run(
        [sys.executable, str(CHECK_FOCUSED),
         "--catalog", str(FOCUSED_CATALOG),
         "--dry-run"],
        capture_output=True,
        text=True,
        timeout=30,
    )
    output = result.stdout + result.stderr
    assert result.returncode == 0, (
        f"--dry-run exited {result.returncode}; output:\n{output}"
    )
    assert "4 P-prompts" in output, (
        f"--dry-run output does not say '4 P-prompts'; got:\n{output}"
    )
    assert "1 N-prompts" in output, (
        f"--dry-run output does not say '1 N-prompts'; got:\n{output}"
    )


# ---------------------------------------------------------------------------
# FOCUS-02: focused-output catalog contains NOT-any-focused
# ---------------------------------------------------------------------------

def test_focused_output_catalog_contains_not_any_focused() -> None:
    """focused-output-catalog.md must contain NOT-any-focused (N1 negative control)."""
    text = FOCUSED_CATALOG.read_text(encoding="utf-8")
    assert "NOT-any-focused" in text, (
        "focused-output-catalog.md does not contain 'NOT-any-focused'"
    )


# ---------------------------------------------------------------------------
# FOCUS-03: focused-output catalog exists (file guard)
# ---------------------------------------------------------------------------

def test_focused_output_catalog_exists() -> None:
    """tests/focused-output-catalog.md must exist as a committed file."""
    assert FOCUSED_CATALOG.exists(), (
        f"focused-output-catalog.md not found at {FOCUSED_CATALOG}"
    )


# ---------------------------------------------------------------------------
# STRICT-01: CLAUDE.md battery commands and threshold invariants
# ---------------------------------------------------------------------------

def test_claude_md_names_both_battery_commands() -> None:
    """CLAUDE.md must name both check-sub-skill-routing.py and check-focused-output.py."""
    text = CLAUDE_MD.read_text(encoding="utf-8")
    assert "check-sub-skill-routing.py" in text, (
        "CLAUDE.md does not mention check-sub-skill-routing.py"
    )
    assert "check-focused-output.py" in text, (
        "CLAUDE.md does not mention check-focused-output.py"
    )


def test_claude_md_mentions_fu21() -> None:
    """CLAUDE.md must mention FU-21 (requirement anchor)."""
    text = CLAUDE_MD.read_text(encoding="utf-8")
    assert "FU-21" in text, "CLAUDE.md does not mention FU-21"


def test_claude_md_contains_exactly_two_p_threshold_4_n_threshold_1() -> None:
    """CLAUDE.md must contain '--p-threshold 4 --n-threshold 1' exactly 2 times."""
    text = CLAUDE_MD.read_text(encoding="utf-8")
    count = text.count("--p-threshold 4 --n-threshold 1")
    assert count == 2, (
        f"CLAUDE.md contains '--p-threshold 4 --n-threshold 1' {count} times, expected 2"
    )


def test_claude_md_has_zero_p_threshold_0() -> None:
    """CLAUDE.md must contain zero occurrences of '--p-threshold 0'."""
    text = CLAUDE_MD.read_text(encoding="utf-8")
    count = text.count("--p-threshold 0")
    assert count == 0, (
        f"CLAUDE.md contains '--p-threshold 0' {count} times (should be 0)"
    )


def test_claude_md_has_zero_p_threshold_2_n_threshold_1() -> None:
    """CLAUDE.md must contain zero occurrences of '--p-threshold 2 --n-threshold 1'."""
    text = CLAUDE_MD.read_text(encoding="utf-8")
    count = text.count("--p-threshold 2 --n-threshold 1")
    assert count == 0, (
        f"CLAUDE.md contains '--p-threshold 2 --n-threshold 1' {count} times (should be 0)"
    )


# ---------------------------------------------------------------------------
# STRICT-01 sweep: no active --p-threshold 0 in scripts or test catalogs
# ---------------------------------------------------------------------------

def _active_p_threshold_0_lines(path: Path) -> list[str]:
    """Return lines containing '--p-threshold 0' that are not in SUPERSEDED blocks."""
    lines = path.read_text(encoding="utf-8").splitlines()
    in_superseded = False
    hits: list[str] = []
    for line in lines:
        if "SUPERSEDED" in line:
            in_superseded = True
        if "--p-threshold 0" in line and not in_superseded:
            hits.append(line)
    return hits


def test_no_active_p_threshold_0_in_scripts() -> None:
    """No script in scripts/ must carry an active '--p-threshold 0'."""
    for py_file in sorted(SCRIPTS.glob("*.py")):
        hits = _active_p_threshold_0_lines(py_file)
        assert not hits, (
            f"{py_file.name} has active '--p-threshold 0' lines: {hits}"
        )


def test_no_active_p_threshold_0_in_test_catalogs() -> None:
    """No *catalog*.md in tests/ must carry an active '--p-threshold 0'."""
    for md in sorted(TESTS.glob("*catalog*.md")):
        hits = _active_p_threshold_0_lines(md)
        assert not hits, (
            f"{md.name} has active '--p-threshold 0' lines: {hits}"
        )


# ---------------------------------------------------------------------------
# SUPERSEDED banners on the three archived baselines
# ---------------------------------------------------------------------------

def test_sub_skill_baseline_v38_has_superseded_banner() -> None:
    """sub-skill-routing-baseline-v3.8.md must have SUPERSEDED banner at head."""
    text = SUB_SKILL_BASELINE_V38.read_text(encoding="utf-8")
    head = text[:500]
    assert "SUPERSEDED" in head, (
        "sub-skill-routing-baseline-v3.8.md missing SUPERSEDED banner in first 500 chars"
    )


def test_routing_baseline_v312_has_superseded_banner() -> None:
    """routing-baseline-v3.12.md must have SUPERSEDED banner at head."""
    text = ROUTING_BASELINE_V312.read_text(encoding="utf-8")
    head = text[:500]
    assert "SUPERSEDED" in head, (
        "routing-baseline-v3.12.md missing SUPERSEDED banner in first 500 chars"
    )


def test_focused_output_baseline_v38_has_superseded_banner() -> None:
    """focused-output-baseline-v3.8.md must have SUPERSEDED banner at head."""
    text = FOCUSED_BASELINE_V38.read_text(encoding="utf-8")
    head = text[:500]
    assert "SUPERSEDED" in head, (
        "focused-output-baseline-v3.8.md missing SUPERSEDED banner in first 500 chars"
    )


# ---------------------------------------------------------------------------
# Script defaults: check-sub-skill-routing.py p-threshold default=2, no --p-threshold 0
# ---------------------------------------------------------------------------

def test_check_sub_skill_routing_p_threshold_default_is_2() -> None:
    """check-sub-skill-routing.py --help must report p-threshold default of 2."""
    result = subprocess.run(
        [sys.executable, str(CHECK_SUB_SKILL), "--help"],
        capture_output=True,
        text=True,
        timeout=15,
    )
    output = result.stdout + result.stderr
    # default=2 appears in argparse help text
    assert "default: 2" in output or "default=2" in output, (
        f"--help does not show p-threshold default=2; got:\n{output}"
    )


def test_check_sub_skill_routing_source_has_no_p_threshold_0() -> None:
    """check-sub-skill-routing.py source must not contain '--p-threshold 0' as an active default."""
    text = CHECK_SUB_SKILL.read_text(encoding="utf-8")
    # The only occurrence would be in a comment or self-test fixture string;
    # there must be no call-site default of 0
    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith("#"):
            continue
        # Reject any non-comment line that sets p-threshold to 0 as a literal default
        if "p_threshold" in stripped and "= 0" in stripped and "default" in stripped:
            raise AssertionError(
                f"check-sub-skill-routing.py has p_threshold default=0 at: {line!r}"
            )


# ---------------------------------------------------------------------------
# Self-tests: both verifiers must pass their own --self-test
# ---------------------------------------------------------------------------

def test_check_sub_skill_routing_self_test_passes() -> None:
    """check-sub-skill-routing.py --self-test must exit 0."""
    result = subprocess.run(
        [sys.executable, str(CHECK_SUB_SKILL), "--self-test"],
        capture_output=True,
        text=True,
        timeout=60,
    )
    output = result.stdout + result.stderr
    assert result.returncode == 0, (
        f"check-sub-skill-routing.py --self-test exited {result.returncode};\n{output}"
    )


def test_check_focused_output_self_test_passes() -> None:
    """check-focused-output.py --self-test must exit 0."""
    result = subprocess.run(
        [sys.executable, str(CHECK_FOCUSED), "--self-test"],
        capture_output=True,
        text=True,
        timeout=60,
    )
    output = result.stdout + result.stderr
    assert result.returncode == 0, (
        f"check-focused-output.py --self-test exited {result.returncode};\n{output}"
    )


if __name__ == "__main__":
    import pytest
    sys.exit(pytest.main([__file__, "-v"]))
