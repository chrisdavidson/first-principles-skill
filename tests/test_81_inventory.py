#!/usr/bin/env python3
"""Tests for Phase 81: requirements inventory parser (AUDIT-01..AUDIT-04).

Pins the ``--self-test`` exit code to 0 so a breakage in the parser or its
inline format/edge fixtures is caught immediately by pytest without reading
any .planning/ files. Also guards the milestone-REQUIREMENTS corpus floor and script
structure.

Requirements covered:
  AUDIT-01 — every ID extracted from all milestone REQUIREMENTS files
  AUDIT-03 — collision report lists all cross-milestone ID reuses
  AUDIT-04 — unresolved [~] and deferred items flagged as orphan candidates

Run from repo root:
    python3 -m pytest tests/test_81_inventory.py -v
"""

from __future__ import annotations

import importlib.util
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
SCRIPT = REPO / "scripts" / "check-inventory.py"

# ---------------------------------------------------------------------------
# Drift-proof corpus floor constant (DEBT-04 / D-01)
# ---------------------------------------------------------------------------

# The on-disk count of .planning/milestones/v*-REQUIREMENTS.md files as of
# milestone v7.10 initialization (verified 2026-06-28). This is a MONOTONIC
# FLOOR: each /gsd-complete-milestone call archives one more file so the corpus
# only grows. Asserting >= (not ==) means the test tolerates growth without
# re-staling while still failing on net corpus loss.
#
# Deliberately NOT derived from the same glob it guards — a self-derived count
# would be tautological (would never catch accidental file deletion).
#
# Note: the count does NOT equal the number of shipped milestones because
# /gsd-complete-milestone at v7.5 plain-rm'd v7.5-REQUIREMENTS.md (no archive),
# so the on-disk count and the milestone count diverge by one. The floor is
# set from the verified on-disk count, not from a milestone-set derivation.
MIN_MILESTONE_REQUIREMENTS_FILES = 40


def _load_check_inventory():
    """Load check-inventory.py as a module (hyphenated name, so importlib needed)."""
    spec = importlib.util.spec_from_file_location("check_inventory", SCRIPT)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


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


def test_milestone_requirements_corpus_present() -> None:
    """The milestone-REQUIREMENTS corpus must meet the monotonic floor with a structural anchor.

    Two assertions over ``found = list(milestones.glob("v*-REQUIREMENTS.md"))``:

    (1) Monotonic floor: ``len(found) >= MIN_MILESTONE_REQUIREMENTS_FILES``.
        Each ``/gsd-complete-milestone`` run archives one more file, so the corpus
        only grows.  The floor catches net corpus loss (accidental deletion) while
        tolerating growth without re-staling.  The constant is a documented literal,
        NOT derived from the same glob (a self-derived count would be tautological).

    (2) Structural non-vacuity anchor: ``v1.0-REQUIREMENTS.md`` is present in the
        glob result, proving the glob resolved the real corpus and not an empty or
        wrong directory.  Without this anchor the floor could pass vacuously if the
        glob silently matched nothing on a future refactor.
    """
    milestones = REPO / ".planning" / "milestones"
    found = list(milestones.glob("v*-REQUIREMENTS.md"))
    found_names = sorted(f.name for f in found)
    assert len(found) >= MIN_MILESTONE_REQUIREMENTS_FILES, (
        f"Expected at least {MIN_MILESTONE_REQUIREMENTS_FILES} vX.Y-REQUIREMENTS.md files "
        f"(monotonic floor), found {len(found)}: {found_names}"
    )
    assert "v1.0-REQUIREMENTS.md" in {f.name for f in found}, (
        f"Structural anchor v1.0-REQUIREMENTS.md not found in corpus glob result. "
        f"Found files: {found_names}"
    )


def test_corpus_floor_logic_fails_below_floor(tmp_path: Path) -> None:
    """The floor predicate (>= MIN_MILESTONE_REQUIREMENTS_FILES) is non-vacuous.

    Builds a temp corpus with exactly MIN - 1 files (below floor) and asserts the
    predicate is False, then adds one more file (reaching the floor) and asserts it
    is True.  This proves the guard still catches net corpus loss without reading the
    real corpus.
    """
    # Create MIN - 1 empty placeholder files (below floor — predicate must be False)
    for i in range(MIN_MILESTONE_REQUIREMENTS_FILES - 1):
        (tmp_path / f"v{i}.0-REQUIREMENTS.md").touch()

    below_floor = list(tmp_path.glob("v*-REQUIREMENTS.md"))
    assert not (len(below_floor) >= MIN_MILESTONE_REQUIREMENTS_FILES), (
        f"Floor predicate must be False with {len(below_floor)} files "
        f"(floor={MIN_MILESTONE_REQUIREMENTS_FILES})"
    )

    # Add one more to reach exactly the floor — predicate must now be True
    (tmp_path / f"v{MIN_MILESTONE_REQUIREMENTS_FILES - 1}.0-REQUIREMENTS.md").touch()
    at_floor = list(tmp_path.glob("v*-REQUIREMENTS.md"))
    assert len(at_floor) >= MIN_MILESTONE_REQUIREMENTS_FILES, (
        f"Floor predicate must be True with {len(at_floor)} files "
        f"(floor={MIN_MILESTONE_REQUIREMENTS_FILES})"
    )


# ---------------------------------------------------------------------------
# Task 1 (Plan 02): Structural guards — collision and orphan functions
# ---------------------------------------------------------------------------


def test_script_has_collision_and_orphan_functions() -> None:
    """check-inventory.py must define detect_collisions and find_orphan_candidates."""
    text = SCRIPT.read_text(encoding="utf-8")
    assert "def detect_collisions(" in text, (
        "check-inventory.py does not define detect_collisions"
    )
    assert "def find_orphan_candidates(" in text, (
        "check-inventory.py does not define find_orphan_candidates"
    )
    assert "def _enumerate_corpus(" in text, (
        "check-inventory.py does not define _enumerate_corpus"
    )


def test_check_coverage_visits_all_26_files() -> None:
    """``python3 scripts/check-inventory.py --check-coverage`` exits 0 and reports 26 files.

    This is the AUDIT-01 file-coverage round-trip guard: every one of the 26
    .planning/milestones/vX.Y-REQUIREMENTS.md files must be visited and must
    yield at least one ID. A zero-ID file exits non-zero.
    """
    result = subprocess.run(
        [sys.executable, str(SCRIPT), "--check-coverage"],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, (
        f"check-inventory.py --check-coverage exited {result.returncode} (expected 0).\n"
        f"stdout:\n{result.stdout}\n"
        f"stderr:\n{result.stderr}"
    )
    assert "26" in result.stdout, (
        f"Expected '26' in --check-coverage stdout but got:\n{result.stdout}"
    )


# ---------------------------------------------------------------------------
# Task 2 (Plan 02): --output path-confinement and Markdown path notice
# ---------------------------------------------------------------------------


def test_output_path_confinement() -> None:
    """``--output /tmp/escape-inventory.md`` must exit 2 without creating the file (T-81-01)."""
    import os
    escape_path = "/tmp/escape-inventory-test-81-02.md"
    # Ensure the file does not already exist from a prior failed run
    if os.path.exists(escape_path):
        os.unlink(escape_path)
    result = subprocess.run(
        [sys.executable, str(SCRIPT), "--output", escape_path],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 2, (
        f"Expected exit 2 for escaping --output path, got {result.returncode}.\n"
        f"stdout:\n{result.stdout}\n"
        f"stderr:\n{result.stderr}"
    )
    assert not os.path.exists(escape_path), (
        f"File {escape_path!r} was created despite the confinement check (T-81-01 violated)"
    )


def test_render_has_path_notice() -> None:
    """No-flag stdout must contain the D-09 documented-vs-actual path notice substring."""
    result = subprocess.run(
        [sys.executable, str(SCRIPT)],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, (
        f"check-inventory.py (no flags) exited {result.returncode}.\n"
        f"stdout:\n{result.stdout}\nstderr:\n{result.stderr}"
    )
    assert ".planning/milestones" in result.stdout, (
        f"Expected D-09 path notice substring '.planning/milestones' in stdout but not found.\n"
        f"stdout (first 500 chars):\n{result.stdout[:500]}"
    )
    assert "# Requirements Inventory" in result.stdout, (
        f"Expected '# Requirements Inventory' header in stdout but not found.\n"
        f"stdout (first 500 chars):\n{result.stdout[:500]}"
    )


# ---------------------------------------------------------------------------
# Plan 04 (RED): parenthetical-title ID extraction and MKT-F1 collision
# ---------------------------------------------------------------------------


def test_paren_title_id_extracted(tmp_path: Path) -> None:
    """_extract_ids_from_file must extract IDs from bold list-item titles in (ID) form.

    Three sub-cases encoded in a single temp file:
      (a) Single-ID parenthetical: `- **Title (MKT-F1)** — text` → MKT-F1 extracted
      (b) Dual-ID parenthetical:   `- **Title (FU-21-1 / FU-21-2)** — text`
              → FU-21-1 and FU-21-2 both extracted
      (c) Pipe-table cell (precision guard): `| Title (MKT-F1) | ... |`
              → zero entries (no list-item anchor)

    Currently FAILS (RED) — _ID_RE only matches when bold-terminator follows the ID.
    """
    mod = _load_check_inventory()

    tmp_file = tmp_path / "vTEST-REQUIREMENTS.md"
    tmp_file.write_text(
        "- **Community marketplace submission (MKT-F1)** — description text\n"
        "- **Routing-regression hardening (FU-21-1 / FU-21-2)** — description text\n"
        "| Community marketplace submission (MKT-F1) | Not selected |\n",
        encoding="utf-8",
    )

    entries = mod._extract_ids_from_file(tmp_file, "vTEST")
    extracted_ids = {e["id"] for e in entries}

    # (a) single-ID parenthetical
    assert "MKT-F1" in extracted_ids, (
        f"Expected MKT-F1 from parenthetical-title form; got ids={extracted_ids!r}"
    )
    # (b) dual-ID parenthetical — both IDs must appear
    assert "FU-21-1" in extracted_ids, (
        f"Expected FU-21-1 from dual parenthetical-title form; got ids={extracted_ids!r}"
    )
    assert "FU-21-2" in extracted_ids, (
        f"Expected FU-21-2 from dual parenthetical-title form; got ids={extracted_ids!r}"
    )
    # (c) precision guard — pipe-table cell must NOT be extracted
    assert extracted_ids == {"MKT-F1", "FU-21-1", "FU-21-2"}, (
        f"Unexpected IDs extracted (pipe-table cell must not match): {extracted_ids!r}"
    )


def test_mkt_f1_multi_milestone_detected() -> None:
    """detect_collisions must report MKT-F1 across at least 4 milestones.

    MKT-F1 appears as:
      v2.0  line 100: `- **MKT-F1**: ...`              (standard form — already matched)
      v3.0  line 82:  `- **Community marketplace submission (MKT-F1)** — ...` (paren)
      v3.1  line 52:  `- **Community marketplace submission (MKT-F1):** ...`  (paren+colon)
      v3.2  line 71:  `- **Community marketplace submission (MKT-F1):** ...`  (paren+colon)

    Currently FAILS (RED) — only v2.0/MKT-F1 is captured so MKT-F1 is absent from the
    collision map entirely (len == 1, not in detect_collisions output).
    """
    mod = _load_check_inventory()

    all_entries, _files = mod._enumerate_corpus()
    collisions = mod.detect_collisions(all_entries)

    assert "MKT-F1" in collisions, (
        f"Expected MKT-F1 in collision map (>=4 milestones); "
        f"MKT-F1 milestones found: "
        f"{[e['milestone'] for e in all_entries if e['id'] == 'MKT-F1']!r}"
    )
    mkt_milestones = set(collisions["MKT-F1"])
    required = {"v2.0", "v3.0", "v3.1", "v3.2"}
    assert required <= mkt_milestones, (
        f"MKT-F1 must appear in milestones {required}; got {sorted(mkt_milestones)!r}"
    )


if __name__ == "__main__":
    import pytest
    sys.exit(pytest.main([__file__, "-v"]))
