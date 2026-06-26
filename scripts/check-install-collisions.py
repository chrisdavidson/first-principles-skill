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
import tempfile
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

    # Require a *leading* frontmatter block: the file must start with a `---`
    # fence (parts[0] empty) and contain a closing fence (>=3 parts). Anything
    # else (no fence, partial fence, or content before the first fence) has no
    # isolatable frontmatter, so there is no name — do NOT fall back to scanning
    # the whole body, which would let a column-0 `name:` in prose/code masquerade
    # as the surface name (WR-02).
    parts = _FENCE_RE.split(text, maxsplit=2)
    if len(parts) < 3 or parts[0].strip():
        return None
    block = parts[1]

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


def _write_surface(
    base_dir: Path, skill_names: list[str], agent_name: str
) -> None:
    """Write a synthetic install surface on disk for the fixture self-test.

    Builds base_dir/skills/<name>/SKILL.md and base_dir/agents/<agent>.md, each
    carrying a real leading `---\\nname: ...\\n---` frontmatter block, so the
    collector+parser layer (_collect_names / _extract_name) is exercised exactly
    as it would be against a live install tree.
    """
    skills_dir = base_dir / "skills"
    for skill_name in skill_names:
        skill_dir = skills_dir / skill_name
        skill_dir.mkdir(parents=True, exist_ok=True)
        (skill_dir / "SKILL.md").write_text(
            f"---\nname: {skill_name}\ndescription: synthetic fixture skill\n---\n\nBody.\n",
            encoding="utf-8",
        )

    agents_dir = base_dir / "agents"
    agents_dir.mkdir(parents=True, exist_ok=True)
    (agents_dir / f"{agent_name}.md").write_text(
        f"---\nname: {agent_name}\ndescription: synthetic fixture agent\n---\n\nBody.\n",
        encoding="utf-8",
    )


def _run_self_test() -> None:
    """Negative proof (D-04): inject a known-colliding name-pair into the
    production _find_collisions() helper and assert the scanner flags it.
    A silent no-op extension must not be able to pass.

    Three-part test:
    1. Positive fixture: colliding pair → assert collision IS detected (exit 1 if not).
    2. Negative control: disjoint pair → assert NO collision reported (exit 1 if wrong).
    3. Collector+parser fixture (WR-01): build two synthetic on-disk install
       surfaces in a tempdir, assert _collect_names/_extract_name return the
       expected names AND that _find_collisions flags a planted collision — so
       the bug-prone parsing/collection layer has real teeth, decoupled from the
       live plugin's skill count.

    If any assertion fails: FAIL exit 1. If all pass: PASS exit 0.
    """
    # Positive fixture — same name on both surfaces (deliberate collision).
    fixture_plugin_names: set[str] = {"first-principles"}
    fixture_monolith_names: set[str] = {"first-principles"}

    # Invoke the PRODUCTION helper — not an inline intersection — so a broken
    # or no-op _find_collisions() implementation cannot silently pass (D-04).
    collisions = _find_collisions(fixture_plugin_names, fixture_monolith_names)

    if not collisions:
        sys.stderr.write(
            "check-install-collisions --self-test: FAIL — fixture produced no "
            "collision (algorithm or fixture broken)\n"
        )
        sys.exit(1)

    # Negative control — disjoint pair must produce empty set (proves detector
    # is not a constant that always reports a collision).
    disjoint_collisions = _find_collisions({"x"}, {"y"})
    if disjoint_collisions:
        sys.stderr.write(
            "check-install-collisions --self-test: FAIL — disjoint pair "
            f"incorrectly reported a collision: {disjoint_collisions}\n"
        )
        sys.exit(1)

    # Collector+parser fixture (WR-01) — exercise the full _collect_names /
    # _extract_name path against synthetic on-disk surfaces with a planted
    # collision ("shared-tool" present on both surfaces).
    with tempfile.TemporaryDirectory() as tmp:
        tmp_root = Path(tmp)
        plugin_surface = tmp_root / "plugin"
        monolith_surface = tmp_root / "monolith"
        _write_surface(
            plugin_surface,
            skill_names=["shared-tool", "plugin-only"],
            agent_name="plugin-orchestrator",
        )
        _write_surface(
            monolith_surface,
            skill_names=["shared-tool", "monolith-only"],
            agent_name="monolith-agent",
        )

        expected_plugin = {"shared-tool", "plugin-only", "plugin-orchestrator"}
        expected_monolith = {"shared-tool", "monolith-only", "monolith-agent"}

        collected_plugin = _collect_names(plugin_surface)
        if collected_plugin != expected_plugin:
            sys.stderr.write(
                "check-install-collisions --self-test: FAIL — _collect_names "
                f"returned {sorted(collected_plugin)} for the plugin fixture, "
                f"expected {sorted(expected_plugin)} (collector/parser regression?)\n"
            )
            sys.exit(1)

        collected_monolith = _collect_names(monolith_surface)
        if collected_monolith != expected_monolith:
            sys.stderr.write(
                "check-install-collisions --self-test: FAIL — _collect_names "
                f"returned {sorted(collected_monolith)} for the monolith fixture, "
                f"expected {sorted(expected_monolith)} (collector/parser regression?)\n"
            )
            sys.exit(1)

        fixture_collisions = _find_collisions(collected_plugin, collected_monolith)
        if fixture_collisions != {"shared-tool"}:
            sys.stderr.write(
                "check-install-collisions --self-test: FAIL — collector fixture "
                f"collision was {sorted(fixture_collisions)}, expected ['shared-tool']\n"
            )
            sys.exit(1)

    print(
        f"check-install-collisions --self-test: PASS "
        f"(fixture collision detected: {sorted(collisions)[0]!r}; "
        f"disjoint pair clean; collector fixture flagged 'shared-tool')"
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

    # Live collector invariant (WR-01): the committed plugin tree always ships a
    # populated set of skill+agent names. A parser/collector regression that
    # zeroes this out would otherwise make the live gate vacuously "clean"
    # (empty intersection), so an empty result trips the gate. Non-empty (rather
    # than a hardcoded count) keeps the gate stable when skills are added/removed.
    if not plugin_names:
        sys.stderr.write(
            "check-install-collisions: FAIL — collected 0 plugin names from "
            f"{PLUGIN_DIR} (parser/collector regression? expected a populated set)\n"
        )
        sys.exit(1)

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
