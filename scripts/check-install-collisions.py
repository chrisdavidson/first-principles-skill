#!/usr/bin/env python3
# /// script
# requires-python = ">=3.12"
# dependencies = []
# ///
"""COLLIDE-01 gate: dual-install name-collision scanner.

Usage:
    python3 scripts/check-install-collisions.py [--self-test]

Exit codes: 0 clean, 1 collision (or self-test fixture wrongly produced no
collision), 2 environment error.

--self-test: runs an inline fixture pair (synthetic plugin name colliding with
a synthetic monolith name) and asserts the scanner detects the collision.
Negative proof per D-04/D-07: it must demonstrate the scanner FAILs on a
known-colliding input — a silent no-op extension cannot pass.

The monolith surface (first-principles-thinking/) is intentionally included
here (D-02), relaxing VAL-04's D-09 monolith exclusion for the NAME axis only.
VAL-04 owns the trigger 4-gram axis; this gate owns the name-collision axis —
orthogonal concerns.

first-principles-thinking/ is currently absent from the committed tree (D-03).
A live-tree scan against an absent or empty monolith dir is vacuously clean and
is NOT an error — the gate's teeth come from the inline self-test fixture.
The live scan auto-activates if the monolith form is ever populated.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


REPO_ROOT: Path = Path(__file__).resolve().parents[1]
PLUGIN_DIR: Path = REPO_ROOT / "first-principles"
MONOLITH_DIR: Path = REPO_ROOT / "first-principles-thinking"

_FENCE_RE = re.compile(r"^---\s*$", re.MULTILINE)


def _require_python_version() -> None:
    if sys.version_info < (3, 12):
        sys.stderr.write(
            f"scripts/check-install-collisions.py requires Python >=3.12 "
            f"(running {sys.version_info.major}.{sys.version_info.minor}).\n"
        )
        sys.exit(2)


def _extract_name(md_path: Path) -> str | None:
    """Extract the 'name:' scalar from a SKILL.md or agent .md frontmatter block.

    Isolates the frontmatter block between the first two YAML fences (---), then
    searches for a name: line with a stdlib regex. Returns the stripped name string,
    or None if not found or the file cannot be read.
    """
    try:
        text = md_path.read_text(encoding="utf-8")
    except OSError:
        return None

    parts = _FENCE_RE.split(text, maxsplit=2)
    if len(parts) >= 3:
        block = parts[1]
    else:
        block = text

    m = re.search(r"^name:\s*(.+?)\s*$", block, re.MULTILINE)
    if m is None:
        return None
    name = m.group(1).strip("'\"`")
    return name if name else None


def _collect_names(base_dir: Path) -> set[str]:
    """Return the set of skill+agent names under an install surface.

    Walks base_dir/skills/ (each direct child dir's SKILL.md) and
    base_dir/agents/ (each *.md). Returns an empty set if base_dir does not
    exist — absent surface is vacuously clean, NOT an environment error (D-03).
    """
    if not base_dir.exists():
        return set()

    names: set[str] = set()

    skills_dir = base_dir / "skills"
    if skills_dir.exists() and skills_dir.is_dir():
        for skill_dir in skills_dir.iterdir():
            if not skill_dir.is_dir():
                continue
            skill_md = skill_dir / "SKILL.md"
            if skill_md.is_file():
                name = _extract_name(skill_md)
                if name is not None:
                    names.add(name)

    agents_dir = base_dir / "agents"
    if agents_dir.exists() and agents_dir.is_dir():
        for agent_md in agents_dir.glob("*.md"):
            if agent_md.is_file():
                name = _extract_name(agent_md)
                if name is not None:
                    names.add(name)

    return names


def _find_collisions(plugin_names: set[str], monolith_names: set[str]) -> set[str]:
    """Return the set of names present in both plugin and monolith surfaces.

    Shared by main() (live scan) and _run_self_test() (D-04 negative proof) so
    the self-test exercises the same production code path.
    """
    return plugin_names & monolith_names


def _run_self_test() -> None:
    """Negative proof (D-04): inject a known-colliding name-pair into the
    production _find_collisions() helper and assert the scanner flags it.
    A silent no-op extension must not be able to pass.

    If no collision is detected: FAIL exit 1.
    If collision is detected as expected: PASS exit 0.
    Fixture is inline (no external files).
    """
    # Synthetic colliding pair: same name on both surfaces.
    fixture_plugin_names: set[str] = {"first-principles"}
    fixture_monolith_names: set[str] = {"first-principles"}  # deliberate collision

    # Invoke the PRODUCTION helper — not an inline intersection — so a broken
    # or no-op _find_collisions() implementation cannot silently pass (D-04).
    collisions = _find_collisions(fixture_plugin_names, fixture_monolith_names)

    if not collisions:
        sys.stderr.write(
            "check-install-collisions --self-test: FAIL — fixture produced no "
            "collision (algorithm or fixture broken)\n"
        )
        sys.exit(1)

    print(
        f"check-install-collisions --self-test: PASS "
        f"(fixture collision detected: {sorted(collisions)[0]!r})"
    )
    sys.exit(0)


def main() -> None:
    parser = argparse.ArgumentParser(
        description=(
            "COLLIDE-01: dual-install name-collision scanner "
            "(plugin first-principles/ vs monolith first-principles-thinking/)."
        )
    )
    parser.add_argument(
        "--self-test",
        action="store_true",
        help=(
            "run an inline colliding name-pair fixture and verify the scanner "
            "detects the collision (negative proof, D-04)"
        ),
    )
    args = parser.parse_args()

    _require_python_version()

    if args.self_test:
        _run_self_test()
        return

    plugin_names = _collect_names(PLUGIN_DIR)
    monolith_names = _collect_names(MONOLITH_DIR)
    collisions = _find_collisions(plugin_names, monolith_names)

    if collisions:
        sys.stderr.write(
            f"check-install-collisions: FAIL "
            f"({len(collisions)} name collision(s): {sorted(collisions)})\n"
        )
        sys.exit(1)

    print(
        f"check-install-collisions: PASS "
        f"(plugin names: {len(plugin_names)}, monolith names: {len(monolith_names)}, "
        f"no name collisions)"
    )
    sys.exit(0)


if __name__ == "__main__":
    main()
