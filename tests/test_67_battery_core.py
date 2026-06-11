#!/usr/bin/env python3
"""Tests for Phase 67: unified battery core invariant guards.

Requirements covered:
  BATT-01 — merged catalog parses correctly (9 rows, two-column values, unique IDs,
             n-a placement)
  BATT-02 — transport argv is Plan-36-locked (verbatim `claude -p --output-format
             stream-json --verbose --permission-mode bypassPermissions`; no shell=True)
  BATT-03 — both detectors pass all source fixtures (8 boundary + 9 focused);
             _both_match n-a auto-pass logic
  BATT-04 — threshold defaults (boundary_p=2, boundary_n=2, focused_p=4, focused_n=1)
             and K>N guard (repeat=2, min_pass=3 → exit 2 before any I/O)

Run from repo root:
    python3 -m pytest tests/test_67_battery_core.py -v
"""

from __future__ import annotations

import importlib.util
import json
import sys
import tempfile
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[1]
TESTS = REPO / "tests"
SCRIPTS = REPO / "scripts"
CATALOG_PATH = TESTS / "routing-battery-catalog.md"

# ---------------------------------------------------------------------------
# Module loader — importlib convention (scripts/ has no __init__.py; the
# modules use hyphenated filenames; `from scripts._battery_core import ...`
# fails — use spec_from_file_location for check-routing-battery.py;
# _battery_core uses a regular import since the scripts dir is on sys.path).
# Mirror idiom from:
#   tests/test_64_01_install.py lines 62-69
#   tests/test_60_01_check_agent_candidate.py lines 84-92
#
# Loading order matters:
#   1. Add SCRIPTS to sys.path first.
#   2. Load _battery_core via spec_from_file_location and register it as
#      sys.modules["_battery_core"] so that check-routing-battery.py's
#      internal `import _battery_core` resolves to the SAME object.
#   3. Load check-routing-battery.py via spec_from_file_location.
# ---------------------------------------------------------------------------

_scripts_dir = str(SCRIPTS)
if _scripts_dir not in sys.path:
    sys.path.insert(0, _scripts_dir)


def _load_battery_core():
    """Load scripts/_battery_core.py as module `bc` and register in sys.modules."""
    spec = importlib.util.spec_from_file_location(
        "_battery_core", SCRIPTS / "_battery_core.py"
    )
    mod = importlib.util.module_from_spec(spec)
    # Register BEFORE exec_module so that @dataclass resolves sys.modules[__name__]
    # correctly AND so that check-routing-battery.py's `import _battery_core` gets
    # this same object (not a fresh re-import or an empty stub).
    sys.modules["_battery_core"] = mod
    spec.loader.exec_module(mod)
    return mod


def _load_check_routing_battery():
    """Load scripts/check-routing-battery.py as module `crb`.

    _battery_core must already be registered in sys.modules (done by
    _load_battery_core above) so that this module's internal
    `import _battery_core as _bc` resolves correctly.
    """
    spec = importlib.util.spec_from_file_location(
        "check_routing_battery", SCRIPTS / "check-routing-battery.py"
    )
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


# Load once at module level so all tests share the same objects.
bc = _load_battery_core()
crb = _load_check_routing_battery()


# ===========================================================================
# TASK 1 TESTS: Catalog + transport + threshold/guard  (BATT-01, BATT-02, BATT-04)
# ===========================================================================


# ---------------------------------------------------------------------------
# BATT-01: Merged catalog parsing
# ---------------------------------------------------------------------------

# Expected two-column values for all 9 rows (from PATTERNS.md de-collision table
# and RESEARCH.md §3.2).  Ordering matches the catalog rows.
_EXPECTED_CATALOG_ROWS: list[tuple[str, str, str]] = [
    # (id, expected_boundary, expected_output)
    ("B-P12", "none-or-other", "n-a"),
    ("B-P24", "none-or-other", "n-a"),
    ("B-N1",  "none-or-other", "n-a"),
    ("B-N2",  "none-or-other", "n-a"),
    ("F-P12", "n-a", "focused-pre-mortem"),
    ("F-P24", "n-a", "focused-inversion"),
    ("F-P25", "n-a", "focused-pre-mortem"),
    ("F-P26", "n-a", "focused-pre-mortem"),
    ("F-N1",  "n-a", "NOT-any-focused"),
]

_EXPECTED_P_IDS = {"B-P12", "B-P24", "F-P12", "F-P24", "F-P25", "F-P26"}
_EXPECTED_N_IDS = {"B-N1", "B-N2", "F-N1"}


def test_merged_catalog_parses() -> None:
    """parse_merged_catalog returns 6 P + 3 N MergedPrompts with correct two-column values."""
    positives, negatives = bc.parse_merged_catalog(CATALOG_PATH)

    assert len(positives) == 6, (
        f"expected 6 P-rows, got {len(positives)}: {[p.id for p in positives]}"
    )
    assert len(negatives) == 3, (
        f"expected 3 N-rows, got {len(negatives)}: {[n.id for n in negatives]}"
    )

    # Build a lookup by id and verify both expectation columns.
    all_prompts = {p.id: p for p in positives + negatives}
    for rid, exp_boundary, exp_output in _EXPECTED_CATALOG_ROWS:
        assert rid in all_prompts, f"row {rid!r} missing from parsed catalog"
        prompt = all_prompts[rid]
        assert prompt.expected_boundary == exp_boundary, (
            f"row {rid}: expected_boundary {exp_boundary!r}, got {prompt.expected_boundary!r}"
        )
        assert prompt.expected_output == exp_output, (
            f"row {rid}: expected_output {exp_output!r}, got {prompt.expected_output!r}"
        )


def test_merged_catalog_ids_unique() -> None:
    """All 9 parsed IDs are unique and match the de-collided ID set."""
    positives, negatives = bc.parse_merged_catalog(CATALOG_PATH)
    all_ids = [p.id for p in positives + negatives]

    assert len(all_ids) == 9, f"expected 9 total rows, got {len(all_ids)}: {all_ids}"
    assert len(set(all_ids)) == len(all_ids), (
        f"duplicate IDs found in catalog: {all_ids}"
    )

    expected_ids = {rid for rid, _, _ in _EXPECTED_CATALOG_ROWS}
    assert set(all_ids) == expected_ids, (
        f"ID mismatch — expected {sorted(expected_ids)}, got {sorted(all_ids)}"
    )


def test_merged_catalog_na_placement() -> None:
    """Every B-* row has expected_output=='n-a'; every F-* row has expected_boundary=='n-a'."""
    positives, negatives = bc.parse_merged_catalog(CATALOG_PATH)
    for prompt in positives + negatives:
        if prompt.id.startswith("B-"):
            assert prompt.expected_output == "n-a", (
                f"B-* row {prompt.id}: expected expected_output='n-a', "
                f"got {prompt.expected_output!r}"
            )
        elif prompt.id.startswith("F-"):
            assert prompt.expected_boundary == "n-a", (
                f"F-* row {prompt.id}: expected expected_boundary='n-a', "
                f"got {prompt.expected_boundary!r}"
            )


# ---------------------------------------------------------------------------
# BATT-02: Transport argv lock
# ---------------------------------------------------------------------------


def test_transport_argv_locked() -> None:
    """_run_prompt_to builds the Plan-36-locked argv and does not use shell=True.

    Uses a monkeypatched subprocess.run that captures the argv list so we assert
    the LIVE argv (not just source text).
    """
    import subprocess as _subprocess_mod
    import types

    captured_argv: list | None = None
    captured_kwargs: dict = {}

    def fake_run(argv, **kwargs):
        nonlocal captured_argv, captured_kwargs
        captured_argv = argv
        captured_kwargs = kwargs
        # Return a minimal proc-like object so _run_prompt_to doesn't crash.
        return types.SimpleNamespace(stdout=b"")

    # Patch subprocess.run on the bc module.
    original_run = bc.subprocess.run
    bc.subprocess.run = fake_run
    try:
        dummy_prompt = bc.MergedPrompt(
            id="test", text="hello world", expected_boundary="n-a", expected_output="n-a"
        )
        plugin_dir = Path("/tmp/fake-plugin-dir")
        out_path = Path("/tmp/fake-out.jsonl")
        bc._run_prompt_to(dummy_prompt, plugin_dir, out_path)
    finally:
        bc.subprocess.run = original_run

    assert captured_argv is not None, "_run_prompt_to did not call subprocess.run"

    # Assert the Plan-36-locked argv tokens are present in order.
    argv_str = " ".join(str(a) for a in captured_argv)

    ordered_tokens = [
        "claude",
        "-p",
        "--plugin-dir",
        "--output-format",
        "stream-json",
        "--verbose",
        "--permission-mode",
        "bypassPermissions",
    ]
    last_idx = -1
    for token in ordered_tokens:
        found_idx = argv_str.find(token, last_idx + 1)
        assert found_idx != -1, (
            f"Plan-36-locked token {token!r} not found in argv after position {last_idx}: "
            f"{captured_argv!r}"
        )
        last_idx = found_idx

    # shell=True must NOT be present (Plan-36 transport uses a list argv).
    assert captured_kwargs.get("shell", False) is False, (
        f"transport must not use shell=True, got kwargs={captured_kwargs!r}"
    )
    assert "shell" not in captured_kwargs or captured_kwargs["shell"] is False, (
        f"shell=True found in subprocess.run kwargs: {captured_kwargs!r}"
    )


# ---------------------------------------------------------------------------
# BATT-04: Threshold defaults and K>N guard
# ---------------------------------------------------------------------------


def test_default_thresholds() -> None:
    """Merged battery argparse defaults are boundary_p=2, boundary_n=2, focused_p=4, focused_n=1."""
    args = crb.build_parser().parse_args(["--catalog", "x"])
    assert args.boundary_p_threshold == 2, (
        f"expected boundary_p_threshold=2, got {args.boundary_p_threshold}"
    )
    assert args.boundary_n_threshold == 2, (
        f"expected boundary_n_threshold=2, got {args.boundary_n_threshold}"
    )
    assert args.focused_p_threshold == 4, (
        f"expected focused_p_threshold=4, got {args.focused_p_threshold}"
    )
    assert args.focused_n_threshold == 1, (
        f"expected focused_n_threshold=1, got {args.focused_n_threshold}"
    )


def test_kn_guard_fires() -> None:
    """main(['--catalog','/nonexistent','--repeat','2','--min-pass','3']) returns 2 before any I/O."""
    try:
        rc = crb.main(
            [
                "--catalog",
                "/nonexistent/path/that/does/not/exist",
                "--repeat",
                "2",
                "--min-pass",
                "3",
            ]
        )
    except SystemExit as exc:
        rc = exc.code if isinstance(exc.code, int) else 2

    assert rc == 2, (
        f"K>N guard (repeat=2, min-pass=3) expected exit code 2, got {rc}"
    )


# ===========================================================================
# TASK 2 TESTS: Detector fixtures + both-match + output format  (BATT-03, BATT-04)
# ===========================================================================


# ---------------------------------------------------------------------------
# BATT-03: Boundary detector fixtures (mirror self_test_boundary pairings exactly)
# ---------------------------------------------------------------------------

_BOUNDARY_FIXTURE_CASES: list[tuple[str, str]] = [
    (bc._FIXTURE_PREMORTEM_VIA_SKILL, "pre-mortem"),
    (bc._FIXTURE_INVERSION_VIA_AGENT, "inversion"),
    (bc._FIXTURE_PREMORTEM_VIA_TASK, "pre-mortem"),
    (bc._FIXTURE_BOTH, "both"),
    (bc._FIXTURE_NONE, "none-or-other"),
    (bc._FIXTURE_COMPOSER_ONLY, "none-or-other"),
    (bc._FIXTURE_READ_RESULT_CONTAMINATION, "none-or-other"),
    (bc._FIXTURE_COMPOSER_WITH_QUOTED_SUBSKILLS, "none-or-other"),
]

_BOUNDARY_FIXTURE_IDS = [
    "pre-mortem_via_skill",
    "inversion_via_agent",
    "pre-mortem_via_task",
    "both",
    "none-or-other",
    "composer_only_LOAD_BEARING",
    "read_result_contamination_LOAD_BEARING",
    "composer_with_quoted_subskills_LOAD_BEARING",
]


@pytest.mark.parametrize(
    "fixture_text,expected",
    _BOUNDARY_FIXTURE_CASES,
    ids=_BOUNDARY_FIXTURE_IDS,
)
def test_boundary_signal_a_fixtures(fixture_text: str, expected: str) -> None:
    """All 8 boundary _FIXTURE_* constants classify correctly through detect_subskill."""
    with tempfile.NamedTemporaryFile(
        mode="w", suffix=".jsonl", delete=False, encoding="utf-8"
    ) as f:
        f.write(fixture_text)
        f.flush()
        tmp_path = Path(f.name)
    try:
        result = bc.detect_subskill(tmp_path)
        assert result == expected, (
            f"detect_subskill: expected {expected!r}, got {result!r}"
        )
    finally:
        try:
            tmp_path.unlink()
        except OSError:
            pass


# ---------------------------------------------------------------------------
# BATT-03: Focused classifier fixtures (mirror self_test_focused pairings exactly;
# Fixture 8 / probe3 sanity feed is environment-dependent — skipped here, covered by
# self_test_focused()'s in-module soft-skip)
# ---------------------------------------------------------------------------

_FOCUSED_FIXTURE_CASES: list[tuple[str, str]] = [
    (bc._FIXTURE_FOCUSED_PREMORTEM, "focused-pre-mortem"),
    (bc._FIXTURE_FOCUSED_INVERSION, "focused-inversion"),
    (bc._FIXTURE_FULL_COMPOSER, "full-composer"),
    (bc._FIXTURE_AMBIGUOUS, "ambiguous"),
    (bc._FIXTURE_NONE_FOCUSED, "none"),
    (bc._FIXTURE_RAW_TEXT_FALLBACK, "focused-inversion"),
    (bc._FIXTURE_BUG1_PHASE_PROSE, "focused-pre-mortem"),
    (bc._FIXTURE_BUG2_NATURAL_VARIATION, "focused-pre-mortem"),
    (bc._FIXTURE_STRUCTURAL_OVERRIDE, "full-composer"),
]

_FOCUSED_FIXTURE_IDS = [
    "focused_pre_mortem",
    "focused_inversion",
    "full_composer_LOAD_BEARING",
    "ambiguous",
    "none",
    "raw_text_fallback",
    "bug1_phase_prose_regression",
    "bug2_natural_variation_regression",
    "structural_override_LOAD_BEARING",
]


@pytest.mark.parametrize(
    "fixture_text,expected",
    _FOCUSED_FIXTURE_CASES,
    ids=_FOCUSED_FIXTURE_IDS,
)
def test_focused_classifier_fixtures(fixture_text: str, expected: str) -> None:
    """All 9 focused _FIXTURE_* constants classify correctly through detect_output_structure_from_file.

    Fixture 8 (probe3 sanity feed) is NOT included here — it depends on a local-only
    gitignored file and is covered by self_test_focused()'s in-module soft-skip.
    """
    with tempfile.NamedTemporaryFile(
        mode="w", suffix=".jsonl", delete=False, encoding="utf-8"
    ) as f:
        f.write(fixture_text)
        f.flush()
        tmp_path = Path(f.name)
    try:
        result = bc.detect_output_structure_from_file(tmp_path)
        assert result == expected, (
            f"detect_output_structure_from_file: expected {expected!r}, got {result!r}"
        )
    finally:
        try:
            tmp_path.unlink()
        except OSError:
            pass


# ---------------------------------------------------------------------------
# BATT-03: _both_match n-a auto-pass logic
# ---------------------------------------------------------------------------


def test_both_match_na_auto_pass() -> None:
    """_both_match n-a signals auto-pass; real-signal mismatch fails."""
    # Case 1: boundary is n-a → b_count forced to min_pass regardless of boundary verdicts.
    b_count, f_count, passed = bc._both_match(
        ["none-or-other"] * 5,          # boundary verdicts (all non-matching)
        ["focused-pre-mortem"] * 5,      # focused verdicts (all matching)
        "n-a",                           # expected_boundary: auto-pass
        "focused-pre-mortem",            # expected_output: real signal
        3,                               # min_pass
    )
    assert b_count == 3, f"n-a boundary: expected b_count=3 (==min_pass), got {b_count}"
    assert f_count == 5, f"n-a boundary: expected f_count=5, got {f_count}"
    assert passed is True, "n-a boundary + matching focused should PASS"

    # Case 2: output is n-a → f_count forced to min_pass regardless of focused verdicts.
    b_count2, f_count2, passed2 = bc._both_match(
        ["pre-mortem"] * 5,   # boundary verdicts (matching — _is_match passes)
        ["none"] * 5,          # focused verdicts (all non-matching if output expected was real)
        "pre-mortem",          # expected_boundary: real signal
        "n-a",                 # expected_output: auto-pass
        3,
    )
    assert f_count2 == 3, f"n-a output: expected f_count=3 (==min_pass), got {f_count2}"
    assert b_count2 == 5, f"n-a output: expected b_count=5, got {b_count2}"
    assert passed2 is True, "matching boundary + n-a output should PASS"

    # Case 3: real mismatch — boundary expected pre-mortem but all verdicts none-or-other.
    b_count3, f_count3, passed3 = bc._both_match(
        ["none-or-other"] * 5,  # boundary verdicts: all wrong
        ["none"] * 5,
        "pre-mortem",            # expected_boundary: real signal that all verdicts miss
        "n-a",
        3,
    )
    assert b_count3 == 0, f"mismatch: expected b_count=0, got {b_count3}"
    assert passed3 is False, "boundary mismatch with n-a output should FAIL"


# ---------------------------------------------------------------------------
# BATT-03/04: Output format contract
# ---------------------------------------------------------------------------


def test_verdict_output_format(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    """run_battery produces verdict.txt with required three section markers, per-section
    BATTERY line, per-signal P/N tally line, and scores-boundary.tsv + scores-focused.tsv.

    Transport and claude-availability are monkeypatched so no claude invocation occurs.
    """
    # Build a canned pre-mortem assistant-text JSONL response.
    # The focused detector needs procedure markers to fire 'focused-pre-mortem'.
    # Use the same text as _FIXTURE_FOCUSED_PREMORTEM so the detector fires correctly.
    canned_jsonl = json.dumps({
        "type": "assistant",
        "text": (
            "Running a prospective-hindsight analysis on the plan. "
            "Imagine the plan has already failed. What caused it?\n\n"
            "Working backward: what caused the rollout to stall?\n"
            "We adopt the prospective-hindsight stance throughout."
        ),
    })

    def fake_run_prompt_n_times_to_paths(prompt, plugin_dir, out_dir, repeat):
        """Write canned JSONL fixture per requested run and return the paths."""
        paths = []
        for run_idx in range(repeat):
            if repeat == 1:
                out_path = out_dir / f"{prompt.id}.jsonl"
            else:
                out_path = out_dir / f"{prompt.id}-run{run_idx + 1}.jsonl"
            out_path.write_text(canned_jsonl, encoding="utf-8")
            paths.append(out_path)
        return paths

    def fake_ensure_claude_available():
        """No-op: skip the 'claude' binary check during the test."""
        return

    monkeypatch.setattr(crb, "_run_prompt_n_times_to_paths", fake_run_prompt_n_times_to_paths)
    monkeypatch.setattr(crb, "_ensure_claude_available", fake_ensure_claude_available)

    # Use one F-* MergedPrompt: expected_boundary=n-a, expected_output=focused-pre-mortem.
    # With repeat=1 and min_pass=1 the result is determinate.
    test_prompt = bc.MergedPrompt(
        id="F-P12",
        text="/first-principles:pre-mortem test prompt",
        expected_boundary="n-a",
        expected_output="focused-pre-mortem",
    )

    # Call run_battery via crb (uses the monkeypatched transport + availability check).
    rc = crb.run_battery(
        prompts_p=[test_prompt],
        prompts_n=[],
        plugin_dir=Path("/tmp/fake-plugin"),
        out_dir=tmp_path,
        boundary_p_threshold=1,
        boundary_n_threshold=0,
        focused_p_threshold=1,
        focused_n_threshold=0,
        quiet=True,
        repeat=1,
        min_pass=1,
    )

    # --- Assert verdict.txt ---
    verdict_path = tmp_path / "verdict.txt"
    assert verdict_path.exists(), "verdict.txt was not written"
    verdict_text = verdict_path.read_text(encoding="utf-8")

    # Three section markers (Phase 69 output contract).
    assert "--- Boundary signal ---" in verdict_text, (
        "verdict.txt missing '--- Boundary signal ---' section marker"
    )
    assert "--- Focused output ---" in verdict_text, (
        "verdict.txt missing '--- Focused output ---' section marker"
    )
    assert "--- Overall ---" in verdict_text, (
        "verdict.txt missing '--- Overall ---' section marker"
    )

    # At least one BATTERY: PASS or BATTERY: FAIL line must appear per section.
    import re as _re
    battery_lines = _re.findall(r"BATTERY: (?:PASS|FAIL)", verdict_text)
    assert len(battery_lines) >= 3, (
        f"expected >= 3 'BATTERY: PASS|FAIL' lines (one per section), "
        f"found {len(battery_lines)}: {verdict_text!r}"
    )

    # At least one P: x/y  N: a/b tally line in each signal section.
    pn_lines = _re.findall(r"P: \d+/\d+  N: \d+/\d+", verdict_text)
    assert len(pn_lines) >= 2, (
        f"expected >= 2 'P: x/y  N: a/b' tally lines (one per signal section), "
        f"found {len(pn_lines)}: {verdict_text!r}"
    )

    # --- Assert TSV files written ---
    b_tsv = tmp_path / "scores-boundary.tsv"
    assert b_tsv.exists(), "scores-boundary.tsv was not written"

    f_tsv = tmp_path / "scores-focused.tsv"
    assert f_tsv.exists(), "scores-focused.tsv was not written"
