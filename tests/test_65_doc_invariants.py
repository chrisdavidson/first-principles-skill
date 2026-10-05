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

import json
import re
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
        [
            sys.executable,
            str(CHECK_BATTERY),
            "--catalog",
            str(BATTERY_CATALOG),
            "--dry-run",
        ],
        capture_output=True,
        text=True,
        timeout=30,
        check=False,
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
        assert not hits, f"{py_file.name} has active '--p-threshold 0' lines: {hits}"


def test_no_active_p_threshold_0_in_test_catalogs() -> None:
    """No *catalog*.md in tests/ must carry an active '--p-threshold 0'."""
    for md in sorted(TESTS.glob("*catalog*.md")):
        hits = _active_p_threshold_0_lines(md)
        assert not hits, f"{md.name} has active '--p-threshold 0' lines: {hits}"


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
# Script defaults: check-routing-battery.py threshold defaults
# (successor to the retired check-sub-skill-routing.py and
# check-focused-output.py guards)
# ---------------------------------------------------------------------------

# Loads the script from a fresh compile of its source in a child process, so
# a stale scripts/__pycache__ entry can never stand in for the current source
# and the test process's sys.path / sys.modules stay untouched.
_PARSER_DEFAULTS_PROBE = """
import json, sys, types
path = sys.argv[1]
module = types.ModuleType("check_routing_battery")
module.__file__ = path
sys.modules[module.__name__] = module
with open(path, encoding="utf-8") as fh:
    exec(compile(fh.read(), path, "exec"), module.__dict__)
print(json.dumps({a.dest: a.default for a in module.build_parser()._actions}, default=str))
"""


def _battery_help_defaults() -> dict[str, int]:
    """Map each documented option of check-routing-battery.py --help to its default.

    The help strings type their defaults by hand, so this reads what a user is
    told, which _battery_parser_defaults() checks against what argparse applies.
    The lookahead stops a flag whose own '(default: N' is missing from borrowing
    the next option's.
    """
    result = subprocess.run(
        [sys.executable, "-B", str(CHECK_BATTERY), "--help"],
        capture_output=True,
        text=True,
        timeout=15,
        check=False,
    )
    assert result.returncode == 0, (
        f"--help exited {result.returncode}:\n{result.stdout}{result.stderr}"
    )
    output = " ".join(result.stdout.split())
    return {
        m.group(1): int(m.group(2))
        for m in re.finditer(
            r"(--[a-z-]+) [A-Z_]+ (?:(?! --[a-z]).)*?\(default: (\d+)", output
        )
    }


def _battery_parser_defaults() -> dict[str, object]:
    """Map each argparse dest of check-routing-battery.py to its real default."""
    result = subprocess.run(
        [sys.executable, "-B", "-c", _PARSER_DEFAULTS_PROBE, str(CHECK_BATTERY)],
        capture_output=True,
        text=True,
        timeout=15,
        check=False,
    )
    assert result.returncode == 0, f"parser probe failed:\n{result.stderr}"
    return json.loads(result.stdout)


def test_battery_boundary_p_threshold_default_is_2() -> None:
    """check-routing-battery.py must default --boundary-p-threshold to 2.

    The retired check-sub-skill-routing.py shim owned this default; the merged
    battery carries it forward under a namespaced flag. Pinning it here keeps
    the pre-merge verdicts reproducible. Read per flag: --boundary-n-threshold
    also documents 'default: 2', so a bare substring match could not see this
    one change.
    """
    help_defaults = _battery_help_defaults()
    assert help_defaults.get("--boundary-p-threshold") == 2, (
        f"--help documents --boundary-p-threshold default "
        f"{help_defaults.get('--boundary-p-threshold')}, expected 2"
    )
    actual = _battery_parser_defaults().get("boundary_p_threshold")
    assert actual == 2, f"parser default boundary_p_threshold is {actual}, expected 2"


def test_battery_focused_thresholds_default_4_1() -> None:
    """check-routing-battery.py must default the focused thresholds to P>=4, N>=1.

    The retired check-focused-output.py shim owned these as --p-threshold 4
    --n-threshold 1; the merged battery carries them forward under namespaced
    flags. Both the --help text and the parser's real defaults are read: the
    help string types its default by hand, so it alone could disagree with
    the value argparse actually applies.
    """
    help_defaults = _battery_help_defaults()
    parser_defaults = _battery_parser_defaults()
    for flag, dest, value in (
        ("--focused-p-threshold", "focused_p_threshold", 4),
        ("--focused-n-threshold", "focused_n_threshold", 1),
    ):
        assert help_defaults.get(flag) == value, (
            f"--help documents {flag} default {help_defaults.get(flag)}, "
            f"expected {value}"
        )
        actual = parser_defaults.get(dest)
        assert actual == value, f"parser default {dest} is {actual}, expected {value}"


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
        check=False,
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
