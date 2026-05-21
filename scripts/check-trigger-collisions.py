#!/usr/bin/env python3
# /// script
# requires-python = ">=3.12"
# dependencies = ["pyyaml>=6.0"]
# ///
"""VAL-04 gate: cross-sibling 4-token n-gram collision scanner.

Usage: python3 scripts/check-trigger-collisions.py
Exit codes: 0 clean, 1 collision, 2 environment error.

Algorithm matches D-19-7 verbatim: lowercase -> re.split(r'\\W+', s) -> drop
empties -> contiguous 4-grams -> pairwise set intersection across all 21 pairs.
No stop-word filtering; no normalization beyond lower() + \\W+ split.

Em-dash (U+2014, research P6): "first—principles" -> ["first", "principles"] via
\\W+, identical to "first-principles" — no special casing needed.

Trigger surface: description + " " + when_to_use (unified with VAL-05, research Q1).
"""

from __future__ import annotations

import itertools
import re
import sys
from pathlib import Path

# Adjust sys.path so _skill_io is importable when invoked from any cwd.
sys.path.insert(0, str(Path(__file__).resolve().parent))

from _skill_io import iter_plugin_skills  # noqa: E402


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


def main() -> None:
    _require_python_version()
    _require_pyyaml()

    try:
        skills = build_skill_ngrams()
    except (ValueError, FileNotFoundError) as exc:
        sys.stderr.write(f"check-trigger-collisions: ERROR {exc}\n")
        sys.exit(2)

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
