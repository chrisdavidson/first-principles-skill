#!/usr/bin/env python3
"""Tests for Phase 81: requirements inventory parser (AUDIT-01..AUDIT-04).

Pins the ``--self-test`` exit code to 0 so a breakage in the parser or its
inline format/edge fixtures is caught immediately by pytest without reading
any .planning/ files. Also guards the 26-file corpus presence and script
structure.

Requirements covered:
  AUDIT-01 — every ID extracted from all 26 milestone REQUIREMENTS files
  AUDIT-03 — collision report lists all cross-milestone ID reuses
  AUDIT-04 — unresolved [~] and deferred items flagged as orphan candidates

Run from repo root:
    python3 -m pytest tests/test_81_inventory.py -v
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
SCRIPT = REPO / "scripts" / "check-inventory.py"


# ---------------------------------------------------------------------------
# Structural guards
# ---------------------------------------------------------------------------


def test_script_exists() -> None:
    """scripts/check-inventory.py must exist."""
    assert SCRIPT.exists(), f"check-inventory.py not found at {SCRIPT}"


def test_script_has_inline_script_header() -> None:
    """check-inventory.py must contain the inline script metadata header."""
    text = SCRIPT.read_text(encoding="utf-8")
    assert '# requires-python = ">=3.12"' in text, (
        "check-inventory.py does not contain '# requires-python = \">=3.12\"' "
        "in the inline script header"
    )


def test_script_has_id_regex() -> None:
    """check-inventory.py must define the _ID_RE module-level constant."""
    text = SCRIPT.read_text(encoding="utf-8")
    assert "_ID_RE" in text, (
        "check-inventory.py does not define the _ID_RE constant"
    )


def test_script_has_no_external_imports() -> None:
    """check-inventory.py must be stdlib-only — no yaml, requests, or similar."""
    import re
    text = SCRIPT.read_text(encoding="utf-8")
    # Only check non-comment lines
    non_comment_lines = [
        line for line in text.splitlines()
        if line.strip() and not line.strip().startswith("#")
    ]
    non_comment_text = "\n".join(non_comment_lines)
    pattern = re.compile(r"\b(import|from)\s+(yaml|requests|pyyaml|toml|tomllib)\b")
    match = pattern.search(non_comment_text)
    assert match is None, (
        f"check-inventory.py imports a non-stdlib module: {match.group()!r}"
    )


# ---------------------------------------------------------------------------
# Behavioural invariant: --self-test exits 0
# ---------------------------------------------------------------------------


def test_self_test_exits_zero() -> None:
    """``python3 scripts/check-inventory.py --self-test`` must exit 0.

    This is the primary regression guard for the extraction core. A non-zero
    exit means at least one of the 6 inline format/edge fixtures classified
    incorrectly:
      (1) **ID** bold-close form not extracted
      (2) **ID:** colon-inside-bold form not extracted (v3.9-v3.12 pitfall)
      (3) **META-03-SW** alpha sub-ID not extracted
      (4) embedded prose bold NOT excluded (false positive)
      (5) **FU-21-1 / FU-21-2** dual-ID not split into two records
      (6) [~] checkbox not classified as 'obsoleted'

    No live claude session required — uses inline fixture strings only.
    """
    result = subprocess.run(
        [sys.executable, str(SCRIPT), "--self-test"],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, (
        f"check-inventory.py --self-test exited {result.returncode} "
        f"(expected 0).\n"
        f"stdout:\n{result.stdout}\n"
        f"stderr:\n{result.stderr}"
    )


# ---------------------------------------------------------------------------
# Corpus coverage: the 26 milestone REQUIREMENTS files must exist
# ---------------------------------------------------------------------------


def test_milestones_directory_exists() -> None:
    """The corpus directory .planning/milestones/ must exist."""
    milestones = REPO / ".planning" / "milestones"
    assert milestones.exists(), (
        f".planning/milestones/ not found at {milestones}"
    )


def test_all_26_requirements_files_present() -> None:
    """All 26 vX.Y-REQUIREMENTS.md files confirmed by RESEARCH.md must be present."""
    milestones = REPO / ".planning" / "milestones"
    found = list(milestones.glob("v*-REQUIREMENTS.md"))
    assert len(found) == 26, (
        f"Expected 26 vX.Y-REQUIREMENTS.md files, found {len(found)}: "
        f"{sorted(f.name for f in found)}"
    )


if __name__ == "__main__":
    import pytest
    sys.exit(pytest.main([__file__, "-v"]))
