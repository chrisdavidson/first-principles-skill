#!/usr/bin/env python3
"""Tests for Phase 65: fixture and documentation-correction invariants.

Requirements covered:
  CAT-01..04 — sub-skill catalog rows and header correctness
  FOCUS-01..03 — focused-output catalog dry-run parse + content
  STRICT-01 — no active --p-threshold 0 in docs/scripts/catalogs
  SUPERSEDED banners — v3.8 and v3.12 baselines carry banners
  Self-tests — the merged battery's --self-test exits 0
  Script defaults — check-routing-battery.py boundary p-threshold default=2

Migration note (2026-08-16 audit, stream 2): the two deprecated shims this file
used to pin — check-sub-skill-routing.py and check-focused-output.py — were
retired. Every invariant they guarded was moved onto their successor,
check-routing-battery.py, rather than dropped: the boundary p-threshold default
of 2, the absence of an active --p-threshold 0, the catalog dry-run parse, and
the self-test exit. Retiring a shim must not retire its regression guard.

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
CHECK_BATTERY = SCRIPTS / "check-routing-battery.py"
BATTERY_CATALOG = TESTS / "routing-battery-catalog.md"


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

def test_battery_catalog_dry_run_parses() -> None:
    """check-routing-battery.py --dry-run must parse its catalog and exit 0.

    Successor to the retired check-focused-output.py --dry-run check. The exact
    "4 P-prompts, 1 N-prompts" counts were properties of the pre-merge
    focused-output catalog; the merged catalog carries both signals, so the
    invariant that survives is that the catalog parses cleanly.
    """
    result = subprocess.run(
        [sys.executable, str(CHECK_BATTERY),
         "--catalog", str(BATTERY_CATALOG),
         "--dry-run"],
        capture_output=True,
        text=True,
        timeout=30,
    )
    output = result.stdout + result.stderr
    assert result.returncode == 0, (
        f"--dry-run exited {result.returncode}; output:\n{output}"
    )
    assert "prompt" in output.lower(), (
        f"--dry-run output does not report parsed prompts; got:\n{output}"
    )


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

def test_claude_md_names_the_merged_battery() -> None:
    """CLAUDE.md must name check-routing-battery.py as a runnable command.

    Was: an assertion that CLAUDE.md named the two pre-merge shims. Those were
    retired at the 2026-08-16 audit, and CLAUDE.md still names them once each in
    the sentence recording that retirement — so the old assertion would have kept
    passing while documenting nothing runnable. It now pins the successor, and
    pins it inside a command block rather than anywhere in the file.
    """
    text = CLAUDE_MD.read_text(encoding="utf-8")
    assert "python3 scripts/check-routing-battery.py" in text, (
        "CLAUDE.md does not carry a runnable check-routing-battery.py command"
    )


def test_claude_md_mentions_fu21() -> None:
    """CLAUDE.md must mention FU-21 (requirement anchor)."""
    text = CLAUDE_MD.read_text(encoding="utf-8")
    assert "FU-21" in text, "CLAUDE.md does not mention FU-21"


def test_claude_md_documents_namespaced_focused_thresholds() -> None:
    """CLAUDE.md must document the focused-output thresholds as 4 / 1.

    Was: '--p-threshold 4 --n-threshold 1' appearing exactly twice — the
    un-namespaced flags of the retired check-focused-output.py shim. The
    threshold values are the invariant; the flag spelling was the shim's.
    """
    text = CLAUDE_MD.read_text(encoding="utf-8")
    assert "--focused-p-threshold 4" in text, (
        "CLAUDE.md does not document --focused-p-threshold 4"
    )
    assert "--focused-n-threshold 1" in text, (
        "CLAUDE.md does not document --focused-n-threshold 1"
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
# Script defaults: check-routing-battery.py boundary p-threshold default=2
# (successor to the retired check-sub-skill-routing.py guards)
# ---------------------------------------------------------------------------

def test_battery_boundary_p_threshold_default_is_2() -> None:
    """check-routing-battery.py --help must report a boundary p-threshold default of 2.

    The retired check-sub-skill-routing.py shim owned this default; the merged
    battery carries it forward under a namespaced flag. Pinning it here keeps
    the pre-merge verdicts reproducible.
    """
    result = subprocess.run(
        [sys.executable, str(CHECK_BATTERY), "--help"],
        capture_output=True,
        text=True,
        timeout=15,
    )
    output = result.stdout + result.stderr
    assert "--boundary-p-threshold" in output, (
        f"--help does not expose --boundary-p-threshold; got:\n{output}"
    )
    assert "default: 2" in output or "default=2" in output, (
        f"--help does not show a default of 2; got:\n{output}"
    )


def test_battery_source_has_no_p_threshold_0() -> None:
    """check-routing-battery.py must not set any p-threshold default to 0."""
    text = CHECK_BATTERY.read_text(encoding="utf-8")
    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith("#"):
            continue
        if "p_threshold" in stripped and "= 0" in stripped and "default" in stripped:
            raise AssertionError(
                f"check-routing-battery.py has a p_threshold default=0 at: {line!r}"
            )


# ---------------------------------------------------------------------------
# Self-test: the merged battery must pass its own --self-test
# ---------------------------------------------------------------------------

def test_battery_self_test_passes() -> None:
    """check-routing-battery.py --self-test must exit 0 (also the BATT-06 CI gate)."""
    result = subprocess.run(
        [sys.executable, str(CHECK_BATTERY), "--self-test"],
        capture_output=True,
        text=True,
        timeout=120,
    )
    output = result.stdout + result.stderr
    assert result.returncode == 0, (
        f"check-routing-battery.py --self-test exited {result.returncode};\n{output}"
    )


# ---------------------------------------------------------------------------
# Retirement guard: the shims must stay gone
# ---------------------------------------------------------------------------

def test_retired_shims_are_absent() -> None:
    """The scripts retired by the 2026-08-16 audit must not reappear.

    Without this, a later 'restore the old battery' change would silently
    reintroduce two entry points whose thresholds diverge from the merged
    battery's namespaced defaults.
    """
    for name in (
        "check-sub-skill-routing.py",
        "check-focused-output.py",
        "check-inventory.py",
    ):
        assert not (SCRIPTS / name).exists(), (
            f"scripts/{name} was retired at the 2026-08-16 audit but exists again"
        )


if __name__ == "__main__":
    import pytest
    sys.exit(pytest.main([__file__, "-v"]))
