#!/usr/bin/env python3
"""Behavioral test for docs/ anchor + bad-link detection in check-links.py.

Tests:
    A - docs/-prefixed link is flagged BROKEN (CF-04 bare-filename rule)
    B - dangling/mis-slugged anchor is caught as BROKEN
    C - real em-dash anchor passes (github-slugger double-hyphen rule)
    D - live clean run: `python3 scripts/check-links.py` exits 0

Run with:
    python3 -m pytest scripts/check-links_anchors_test.py -q
"""

from __future__ import annotations

import subprocess
import sys
import tempfile
from pathlib import Path

import pytest

# Ensure scripts/ is importable.
SCRIPTS_DIR = Path(__file__).resolve().parent
REPO_ROOT = SCRIPTS_DIR.parent
sys.path.insert(0, str(SCRIPTS_DIR))


# ---------------------------------------------------------------------------
# Import the helpers we need from check-links.py.
# We import lazily so the module is only loaded once.
# ---------------------------------------------------------------------------

def _import_check_links():
    import importlib.util
    spec = importlib.util.spec_from_file_location(
        "check_links", SCRIPTS_DIR / "check-links.py"
    )
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


@pytest.fixture(scope="module")
def check_links_mod():
    return _import_check_links()


# ---------------------------------------------------------------------------
# Test A: docs/-prefixed link is flagged BROKEN
# ---------------------------------------------------------------------------

def test_a_docs_prefixed_link_flagged(check_links_mod, tmp_path):
    """A link written as docs/TESTING.md from inside a docs/ file is BROKEN.

    It would resolve to docs/docs/TESTING.md (CF-04 bare-filename rule).
    """
    mod = check_links_mod

    # Create a synthetic docs/ directory with a target file + source file.
    docs_dir = tmp_path / "docs"
    docs_dir.mkdir()
    target = docs_dir / "TESTING.md"
    target.write_text("# Testing\n\n## A heading\n", encoding="utf-8")

    source = docs_dir / "SOURCE.md"
    # Link uses docs/-prefixed form: [x](docs/TESTING.md)
    source.write_text("# Source\n\n[x](docs/TESTING.md)\n", encoding="utf-8")

    broken: list = []
    total_links: list[int] = [0]
    total_refs: list[int] = [0]

    mod._check_docs_file(
        source_file=source,
        docs_dir=docs_dir,
        broken=broken,
        total_links=total_links,
        total_refs=total_refs,
    )

    assert total_links[0] == 1, "Should have counted the link"
    assert len(broken) == 1, f"Expected 1 broken, got {broken}"
    _, _, ref, reason = broken[0]
    assert "docs/" in ref or "docs/" in reason, (
        f"BROKEN reason should reference docs/-prefix rule; got ref={ref!r} reason={reason!r}"
    )


# ---------------------------------------------------------------------------
# Test B: dangling/mis-slugged anchor is caught as BROKEN
# ---------------------------------------------------------------------------

def test_b_dangling_anchor_caught(check_links_mod, tmp_path):
    """A link to a real file but with a non-existent anchor is BROKEN."""
    mod = check_links_mod

    docs_dir = tmp_path / "docs"
    docs_dir.mkdir()

    # Target: TESTING.md with known heading (no em-dash for simplicity here)
    target = docs_dir / "TESTING.md"
    target.write_text(
        "# Testing\n\n## CI gates — operational run-detail\n\nsome text\n",
        encoding="utf-8",
    )

    source = docs_dir / "SOURCE.md"
    # Link uses a mis-slugged single-hyphen anchor (the collapsed form that's wrong)
    source.write_text(
        "# Source\n\n[x](TESTING.md#ci-gates-operational-run-detail)\n",
        encoding="utf-8",
    )

    broken: list = []
    total_links: list[int] = [0]
    total_refs: list[int] = [0]

    mod._check_docs_file(
        source_file=source,
        docs_dir=docs_dir,
        broken=broken,
        total_links=total_links,
        total_refs=total_refs,
    )

    assert total_links[0] == 1
    assert len(broken) == 1, f"Expected 1 broken anchor, got {broken}"
    _, _, ref, reason = broken[0]
    assert "anchor" in reason.lower() or "heading" in reason.lower(), (
        f"Reason should mention anchor/heading; got reason={reason!r}"
    )


# ---------------------------------------------------------------------------
# Test C: real em-dash anchor passes (github-slugger double-hyphen rule)
# ---------------------------------------------------------------------------

def test_c_github_slug_em_dash_double_hyphen(check_links_mod):
    """_github_slug must produce double-hyphen for em-dash headings."""
    mod = check_links_mod

    # Primary fixture: em-dash heading from docs/TESTING.md line 8
    result = mod._github_slug("## CI gates — operational run-detail")
    assert result == "ci-gates--operational-run-detail", (
        f"Expected 'ci-gates--operational-run-detail' but got {result!r}. "
        "The github-slugger rule: strip leading '#', lowercase, remove punctuation "
        "(including em-dash '—'), replace EACH remaining space with one hyphen (no collapsing). "
        "em-dash removed → 'CI gates  operational run-detail' (two spaces) → double hyphen."
    )


def test_c_github_slug_val03(check_links_mod):
    """_github_slug must handle '### VAL-03 — check-links'."""
    mod = check_links_mod
    result = mod._github_slug("### VAL-03 — check-links")
    assert result == "val-03--check-links", (
        f"Expected 'val-03--check-links' but got {result!r}"
    )


def test_c_github_slug_preserves_underscore(check_links_mod):
    """_github_slug must KEEP underscores (github-slugger preserves word chars).

    Locks WR-01: a code-span heading like '`scripts/_battery_core.py`' slugs to
    'scripts_battery_corepy' — the underscore survives, the slash/period/backticks
    are stripped. A naive keep-list that drops '_' would yield 'scriptsbatterycorepy'.
    """
    mod = check_links_mod
    assert mod._github_slug("## foo_bar") == "foo_bar", (
        f"Underscore must be preserved; got {mod._github_slug('## foo_bar')!r}"
    )
    result = mod._github_slug("### Anti-masking constants (`scripts/_battery_core.py`)")
    assert result == "anti-masking-constants-scripts_battery_corepy", (
        f"Expected 'anti-masking-constants-scripts_battery_corepy' but got {result!r}. "
        "github-slugger preserves the underscore as a word character."
    )


def test_c_doc_anchors_dedup_duplicate_headings(check_links_mod, tmp_path):
    """_doc_anchors must dedup duplicate headings: slug, slug-1, slug-2 (WR-02)."""
    mod = check_links_mod
    doc = tmp_path / "DUP.md"
    doc.write_text(
        "# Title\n\n## Overview\n\ntext\n\n## Overview\n\ntext\n\n## Overview\n",
        encoding="utf-8",
    )
    anchors = mod._doc_anchors(doc)
    assert "overview" in anchors, f"first occurrence base slug missing; got {anchors}"
    assert "overview-1" in anchors, f"second occurrence '-1' suffix missing; got {anchors}"
    assert "overview-2" in anchors, f"third occurrence '-2' suffix missing; got {anchors}"


def test_c_real_em_dash_anchor_passes(check_links_mod, tmp_path):
    """A link to the real docs/TESTING.md#ci-gates--operational-run-detail resolves."""
    mod = check_links_mod

    docs_dir = tmp_path / "docs"
    docs_dir.mkdir()

    # Reproduce the real TESTING.md heading as a synthetic target.
    target = docs_dir / "TESTING.md"
    target.write_text(
        "# Testing\n\n## CI gates — operational run-detail\n\nsome text\n",
        encoding="utf-8",
    )

    source = docs_dir / "SOURCE.md"
    # Correct double-hyphen anchor form
    source.write_text(
        "# Source\n\n[x](TESTING.md#ci-gates--operational-run-detail)\n",
        encoding="utf-8",
    )

    broken: list = []
    total_links: list[int] = [0]
    total_refs: list[int] = [0]

    mod._check_docs_file(
        source_file=source,
        docs_dir=docs_dir,
        broken=broken,
        total_links=total_links,
        total_refs=total_refs,
    )

    assert total_links[0] == 1
    assert len(broken) == 0, (
        f"Expected 0 broken (real em-dash anchor should pass), got {broken}"
    )


# ---------------------------------------------------------------------------
# Test D: live clean run exits 0 on real repo
# ---------------------------------------------------------------------------

def test_d_live_clean_run():
    """python3 scripts/check-links.py exits 0 on the real repo."""
    result = subprocess.run(
        [sys.executable, str(SCRIPTS_DIR / "check-links.py")],
        capture_output=True,
        text=True,
        cwd=str(REPO_ROOT),
    )
    assert result.returncode == 0, (
        f"check-links.py exited {result.returncode}.\n"
        f"stdout: {result.stdout}\n"
        f"stderr: {result.stderr}"
    )
    # Must still emit the PASS line
    assert "PASS" in result.stdout, f"Expected PASS in output; got: {result.stdout!r}"
