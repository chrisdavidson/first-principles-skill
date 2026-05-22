#!/usr/bin/env python3
# /// script
# requires-python = ">=3.12"
# dependencies = ["pyyaml>=6.0"]
# ///
"""VAL-04 / GATE-02 gate: cross-sibling 4-token n-gram collision scanner.

Usage:
    python3 scripts/check-trigger-collisions.py [--self-test]

Exit codes: 0 clean, 1 collision (or self-test fixture wrongly produced no
collision), 2 environment error.

--self-test: runs an inline fixture pair (synthetic agent + synthetic skill
descriptions that share at least one 4-gram) and asserts the scanner detects
the collision. Negative proof per D-07: it must demonstrate the scanner FAILs
on a known-colliding input — a silent no-op extension cannot pass.

Algorithm matches D-19-7 verbatim: lowercase -> re.split(r'\\W+', s) -> drop
empties -> contiguous 4-grams -> pairwise set intersection across all 28 pairs
(8 nodes: the 7 plugin skills + the first-principles agent description folded
in as an 8th node per Phase 26 D-06).
No stop-word filtering; no normalization beyond lower() + \\W+ split.

Em-dash (U+2014, research P6): "first—principles" -> ["first", "principles"] via
\\W+, identical to "first-principles" — no special casing needed.

Trigger surface: description + " " + when_to_use (unified with VAL-05, research Q1).
The agent's trigger surface is just its frontmatter description (the agent file
has no when_to_use field).

The monolith skill at first-principles-thinking/ is deliberately excluded
(D-09 — agent and monolith never co-install on the same surface).
"""

from __future__ import annotations

import argparse
import itertools
import re
import sys
from pathlib import Path

# Adjust sys.path so _skill_io is importable when invoked from any cwd.
sys.path.insert(0, str(Path(__file__).resolve().parent))

from _skill_io import iter_plugin_skills  # noqa: E402


# Agent surface location (D-06: fold the agent description in as an 8th scan node).
# Mirrors scripts/check-agent.py REPO_ROOT/AGENT_FILE/_FENCE_RE constants.
REPO_ROOT: Path = Path(__file__).resolve().parents[1]
AGENT_FILE: Path = REPO_ROOT / "first-principles" / "agents" / "first-principles.md"
_FENCE_RE = re.compile(r"^---\s*$", re.MULTILINE)

# Slug used for the agent node in the pairwise scan — chosen so it cannot
# collide with any plugin skill directory name.
_AGENT_SLUG = "first-principles-agent"


def _require_python_version() -> None:
    if sys.version_info < (3, 12):
        sys.stderr.write(
            f"scripts/check-trigger-collisions.py requires Python >=3.12 "
            f"(running {sys.version_info.major}.{sys.version_info.minor}).\n"
        )
        sys.exit(2)


def _require_pyyaml() -> None:
    """Catch missing PyYAML at startup with a clear remediation message."""
    try:
        import yaml  # noqa: F401
    except ImportError:
        sys.stderr.write(
            "check-trigger-collisions.py needs PyYAML.\n"
            "  uv run scripts/check-trigger-collisions.py\n"
            "  pip install --user 'pyyaml>=6.0'\n"
        )
        sys.exit(2)


def tokens(s: str) -> list[str]:
    """Tokenize per D-19-7: lowercase + \\W+ split, drop empties."""
    return [t for t in re.split(r"\W+", s.lower()) if t]


def ngrams(toks: list[str], n: int = 4) -> set[tuple[str, ...]]:
    """Return all contiguous n-grams from a token list."""
    return {tuple(toks[i : i + n]) for i in range(len(toks) - n + 1)}


def _load_agent_description() -> str:
    """Read the generated agent file's frontmatter `description` (D-06).

    Returns the description string. Exits 2 (environment error) if the agent
    file is missing, malformed, has no frontmatter, or the description field
    is missing/non-string — same handling shape build_skill_ngrams uses for a
    missing skill description so a broken agent surface FAILs the gate loudly
    instead of silently shrinking the scan back to 21 pairs.
    """
    # Lazy import — _require_pyyaml() is what surfaces the missing-yaml case.
    import yaml

    if not AGENT_FILE.exists():
        sys.stderr.write(
            f"check-trigger-collisions: ERROR agent file not found: {AGENT_FILE}\n"
            f"  Run the sync pipeline to generate it before running this gate.\n"
        )
        sys.exit(2)

    text = AGENT_FILE.read_text(encoding="utf-8")
    if not text.startswith("---"):
        sys.stderr.write(
            "check-trigger-collisions: ERROR agent file does not begin with a "
            "frontmatter fence\n"
        )
        sys.exit(2)
    parts = _FENCE_RE.split(text, maxsplit=2)
    if len(parts) < 3:
        sys.stderr.write(
            "check-trigger-collisions: ERROR agent file is missing/has malformed "
            "frontmatter fences\n"
        )
        sys.exit(2)

    try:
        frontmatter = yaml.safe_load(parts[1])
    except yaml.YAMLError as exc:
        sys.stderr.write(
            f"check-trigger-collisions: ERROR malformed YAML in agent frontmatter: {exc}\n"
        )
        sys.exit(2)

    if not isinstance(frontmatter, dict):
        sys.stderr.write(
            "check-trigger-collisions: ERROR agent frontmatter is not a mapping\n"
        )
        sys.exit(2)

    desc = frontmatter.get("description", "")
    if not isinstance(desc, str) or not desc:
        sys.stderr.write(
            "check-trigger-collisions: ERROR agent frontmatter missing or "
            "non-string 'description' field\n"
        )
        sys.exit(2)
    return desc


def build_skill_ngrams() -> dict[str, set[tuple[str, ...]]]:
    """Return {slug: 4-gram set} for every plugin skill's unified trigger surface."""
    skill_ngrams: dict[str, set[tuple[str, ...]]] = {}
    for slug, fm, _body in iter_plugin_skills():
        desc = fm.get("description", "")
        if not isinstance(desc, str) or not desc:
            sys.stderr.write(
                f"check-trigger-collisions: ERROR {slug}/SKILL.md missing or "
                f"non-string 'description' field\n"
            )
            sys.exit(2)
        wtu = fm.get("when_to_use", "")
        if not isinstance(wtu, str):
            wtu = ""
        surface = desc if not wtu else f"{desc} {wtu}"
        skill_ngrams[slug] = ngrams(tokens(surface))
    return skill_ngrams


def _run_self_test() -> None:
    """Negative proof (D-07): feed a deliberately colliding agent/skill pair
    into the same tokens()/ngrams() functions and assert a 4-gram collision is
    detected. If the fixture produces NO collision the algorithm or fixture is
    broken — FAIL with exit 1. If the collision IS detected, PASS with exit 0.

    Fixture is inline (no external files), matching the
    scripts/check-agent.py --self-test precedent.
    """
    # Synthetic colliding pair — share the 4-gram
    # ("analyze", "from", "first", "principles"), which is one of the locked
    # agent description's trigger phrases. A real skill description that
    # accidentally re-introduced this 4-token sequence is exactly the failure
    # mode the gate must catch.
    fixture_agent_desc = (
        "Synthetic fixture: analyze from first principles for self-test."
    )
    fixture_skill_desc = (
        "Synthetic skill that helps users analyze from first principles too."
    )

    agent_grams = ngrams(tokens(fixture_agent_desc))
    skill_grams = ngrams(tokens(fixture_skill_desc))
    collision = agent_grams & skill_grams

    if not collision:
        sys.stderr.write(
            "check-trigger-collisions --self-test: FAIL — fixture produced no "
            "collision (algorithm or fixture broken; the 4-gram intersection "
            "of the inline agent/skill descriptions was empty)\n"
        )
        sys.exit(1)

    sample = sorted(collision)[0]
    print(
        f"check-trigger-collisions --self-test: PASS "
        f"(fixture collision detected: {' '.join(sample)})"
    )
    sys.exit(0)


def main() -> None:
    parser = argparse.ArgumentParser(
        description=(
            "VAL-04 / GATE-02: cross-sibling 4-token n-gram collision scanner "
            "(7 plugin skills + first-principles agent, 28 pairs)."
        )
    )
    parser.add_argument(
        "--self-test",
        action="store_true",
        help=(
            "run an inline colliding fixture pair and verify the scanner "
            "detects the collision (negative proof, D-07)"
        ),
    )
    args = parser.parse_args()

    _require_python_version()
    _require_pyyaml()

    if args.self_test:
        _run_self_test()
        return

    try:
        skills = build_skill_ngrams()
    except (ValueError, FileNotFoundError) as exc:
        sys.stderr.write(f"check-trigger-collisions: ERROR {exc}\n")
        sys.exit(2)

    # D-06: fold the agent description in as an 8th node. The pairwise scan
    # then naturally grows from 21 to 28 pairs (8 nodes choose 2). The collision
    # loop and exit-code semantics are unchanged.
    agent_desc = _load_agent_description()
    skills[_AGENT_SLUG] = ngrams(tokens(agent_desc))

    slugs = sorted(skills.keys())
    pairs = list(itertools.combinations(slugs, 2))
    collision_count = 0
    colliding_pairs: set[tuple[str, str]] = set()

    for slug_a, slug_b in pairs:
        for gram in sorted(skills[slug_a] & skills[slug_b]):
            sys.stderr.write(f"COLLISION: {slug_a} <-> {slug_b}: {' '.join(gram)}\n")
            colliding_pairs.add((slug_a, slug_b))
            collision_count += 1

    if collision_count > 0:
        sys.stderr.write(
            f"check-trigger-collisions: FAIL "
            f"({collision_count} collisions across {len(colliding_pairs)} sibling pairs)\n"
        )
        sys.exit(1)

    print(
        f"check-trigger-collisions: PASS "
        f"({len(pairs)} sibling pairs, no 4-token collisions)"
    )
    sys.exit(0)


if __name__ == "__main__":
    main()
