"""RED test — Task 1 (72-01): catalog loader + _classify_mode inference.

These assertions will FAIL until check-step0-live.py is renamed and
hardened with:
  - _read_step0_catalog (returns 28 Step0Prompt objects, S-P01 first)
  - _agent_was_dispatched (dispatch detection)
  - _classify_mode (none->full-composer inference)
  - KNOWN_MODES allowlist validation
"""
from __future__ import annotations

import importlib.util
import json
import sys
import tempfile
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]
HARNESS = REPO_ROOT / "scripts" / "check-step0-live.py"
CATALOG = REPO_ROOT / "tests" / "step0-fixture-catalog.md"


def _load_harness():
    """Load check-step0-live.py as a module."""
    spec = importlib.util.spec_from_file_location("check_step0_live", HARNESS)
    mod = importlib.util.module_from_spec(spec)
    sys.modules["check_step0_live"] = mod
    spec.loader.exec_module(mod)
    return mod


@pytest.fixture(scope="module")
def harness():
    return _load_harness()


# --- Task 1 RED assertions ---

def test_harness_file_exists():
    """check-step0-live.py must exist (renamed from spike — D-04)."""
    assert HARNESS.exists(), (
        f"check-step0-live.py not found at {HARNESS}. "
        "Run: git mv scripts/check-step0-live-spike.py scripts/check-step0-live.py"
    )


def test_read_step0_catalog_returns_35_rows(harness):
    """_read_step0_catalog must return exactly 35 Step0Prompt objects.

    v7.9 NEGCAT fixtures (S-N09..S-N15, Phase 120) added 7 negative-category
    boundary cases, bringing the catalog from 28 to 35 rows.  This exact count
    is a deliberate regression guard: the catalog changes only on intentional
    fixture edits, so a frozen literal is correct — deriving the expected value
    from the same _read_step0_catalog parse would be tautological.
    """
    rows = harness._read_step0_catalog(CATALOG)
    assert len(rows) == 35, f"Expected 35 rows, got {len(rows)}"


def test_read_step0_catalog_sp01_first(harness):
    """S-P01 must be the first row (S-P01-first execution order)."""
    rows = harness._read_step0_catalog(CATALOG)
    assert rows[0].id == "S-P01", f"First row should be S-P01, got {rows[0].id}"


def test_classify_mode_none_with_dispatch_returns_full_composer(harness, tmp_path):
    """_classify_mode on none-capture WITH dispatch returns 'full-composer' (LOAD-BEARING)."""
    dispatch_line = json.dumps({
        "type": "assistant",
        "message": {
            "content": [{
                "type": "tool_use",
                "name": "Agent",
                "input": {"subagent_type": "first-principles:first-principles", "prompt": "test"}
            }]
        }
    })
    clarification_line = json.dumps({
        "type": "assistant",
        "text": "I need more information to run the analysis. Please share the plan.",
    })
    p = tmp_path / "none_with_dispatch.jsonl"
    p.write_text(dispatch_line + "\n" + clarification_line + "\n", encoding="utf-8")
    result = harness._classify_mode(p)
    assert result == "full-composer", (
        f"Expected 'full-composer' (inference fix), got {result!r}. "
        "The _classify_mode inference must fire when none + dispatch."
    )


def test_classify_mode_none_without_dispatch_stays_none(harness, tmp_path):
    """_classify_mode on none-capture WITHOUT dispatch returns 'none'."""
    text_line = json.dumps({"type": "assistant", "text": "Hello world. Nothing special."})
    p = tmp_path / "none_no_dispatch.jsonl"
    p.write_text(text_line + "\n", encoding="utf-8")
    result = harness._classify_mode(p)
    assert result == "none", (
        f"Expected 'none' (no inference), got {result!r}. "
        "Inference must NOT fire when no dispatch is present."
    )


def test_read_step0_catalog_rejects_unknown_mode(harness, tmp_path):
    """_read_step0_catalog must exit non-zero on unknown Expected MODE."""
    bad_catalog = tmp_path / "bad_catalog.md"
    bad_catalog.write_text(
        "| ID | Prompt | Expected MODE | Notes |\n"
        "|---|--------|--------------|-------|\n"
        "| S-P01 | some prompt | unknown-mode | bad |\n",
        encoding="utf-8",
    )
    with pytest.raises(SystemExit) as exc_info:
        harness._read_step0_catalog(bad_catalog)
    assert exc_info.value.code != 0, "Should exit non-zero on unknown mode"


def test_agent_was_dispatched_true(harness, tmp_path):
    """_agent_was_dispatched returns True when first-principles dispatch present."""
    line = json.dumps({
        "type": "assistant",
        "message": {
            "content": [{
                "type": "tool_use",
                "name": "Agent",
                "input": {"subagent_type": "FIRST-PRINCIPLES:FIRST-PRINCIPLES", "prompt": "x"}
            }]
        }
    })
    p = tmp_path / "dispatch.jsonl"
    p.write_text(line + "\n", encoding="utf-8")
    assert harness._agent_was_dispatched(p) is True


def test_agent_was_dispatched_false(harness, tmp_path):
    """_agent_was_dispatched returns False when no dispatch line present."""
    p = tmp_path / "no_dispatch.jsonl"
    p.write_text(json.dumps({"type": "assistant", "text": "Hello"}) + "\n", encoding="utf-8")
    assert harness._agent_was_dispatched(p) is False
