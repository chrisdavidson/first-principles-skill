#!/usr/bin/env python3
"""Tests for Phase 70: offline Step 0 emulator invariants (STEP0-01/02/03).

Pins the ``--self-test`` exit code to 0 so a breakage in the emulator or the
fixture catalog is caught immediately by pytest without needing a live claude
session. Follows the ``tests/test_69_*`` convention: resolve REPO root via
``Path(__file__).resolve().parents[1]``, invoke the target script via
``subprocess.run``, and assert the exit code.

Requirements covered:
  STEP0-01 — classifier maps prompt → MODE (first-row-wins)
  STEP0-02 — loud failure on all four D-05 corruption modes
  STEP0-03 — ``--self-test`` exits 0 offline, no live claude session

Run from repo root:
    python3 -m pytest tests/test_70_step0_emulator_invariants.py -v
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
EMULATOR = REPO / "scripts" / "check-step0-emulator.py"


# ---------------------------------------------------------------------------
# Structural guards
# ---------------------------------------------------------------------------

def test_emulator_script_exists() -> None:
    """scripts/check-step0-emulator.py must exist."""
    assert EMULATOR.exists(), (
        f"check-step0-emulator.py not found at {EMULATOR}"
    )


def test_emulator_contains_known_techniques_constant() -> None:
    """check-step0-emulator.py must contain the KNOWN_TECHNIQUES eight-name tuple.

    Phase 110 merged decompose into five-whys (9→8 techniques).
    Phase 111 removed "decompose" from the tuple.

    This is a cheap structural anti-drift pin: if the constant is accidentally
    removed or renamed, this test surfaces the breakage immediately.
    """
    text = EMULATOR.read_text(encoding="utf-8")
    expected = (
        'KNOWN_TECHNIQUES = ("pre-mortem", "inversion", "fishbone", '
        '"five-whys", "trade-off", "second-order", "estimate", "theoretical-limit")'
    )
    assert expected in text, (
        f"check-step0-emulator.py does not contain the expected KNOWN_TECHNIQUES "
        f"eight-name tuple. Expected to find:\n  {expected!r}"
    )


def test_emulator_does_not_import_battery_core() -> None:
    """check-step0-emulator.py must not import from _battery_core (D-11 standalone)."""
    import re
    text = EMULATOR.read_text(encoding="utf-8")
    pattern = re.compile(r"(import|from)\s+_battery_core")
    assert not pattern.search(text), (
        "check-step0-emulator.py imports from _battery_core — D-11 requires "
        "the emulator to be fully standalone with no _battery_core import"
    )


# ---------------------------------------------------------------------------
# Behavioural invariant: --self-test exits 0
# ---------------------------------------------------------------------------

def test_self_test_exits_zero() -> None:
    """``python3 scripts/check-step0-emulator.py --self-test`` must exit 0.

    This is the primary regression guard. A non-zero exit means at least one
    of the following broke:
      - A D-05 fault-injection fixture no longer produces the expected error
      - The phrase-detection table changed in a way that misclassifies a
        fixture in tests/step0-fixture-catalog.md
      - The fixture catalog itself was edited inconsistently

    No live claude session is required — the test is entirely offline.
    """
    result = subprocess.run(
        [sys.executable, str(EMULATOR), "--self-test"],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, (
        f"check-step0-emulator.py --self-test exited {result.returncode} "
        f"(expected 0).\n"
        f"stdout:\n{result.stdout}\n"
        f"stderr:\n{result.stderr}"
    )


def test_self_test_prints_pass() -> None:
    """``--self-test`` stdout must contain 'check-step0-emulator --self-test: PASS'."""
    result = subprocess.run(
        [sys.executable, str(EMULATOR), "--self-test"],
        capture_output=True,
        text=True,
    )
    assert "check-step0-emulator --self-test: PASS" in result.stdout, (
        f"Expected 'check-step0-emulator --self-test: PASS' in stdout but got:\n"
        f"{result.stdout}"
    )


if __name__ == "__main__":
    import pytest
    sys.exit(pytest.main([__file__, "-v"]))
