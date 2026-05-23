#!/usr/bin/env python3
# /// script
# requires-python = ">=3.12"
# dependencies = ["pyyaml>=6.0"]
# ///
"""Internal helper: shared frontmatter+body reader for VAL-03/04/05 scripts.

Not directly invocable (underscore prefix per D-19-5). Exposes:
  - REPO_ROOT       Path to the repository root
  - PLUGIN_SKILLS_DIR  Path to first-principles/skills/
  - iter_plugin_skills() -> Iterator[tuple[str, dict, str]]
"""

from __future__ import annotations

import re
from collections.abc import Iterator
from pathlib import Path

import yaml

# Path resolution: relative to this script's location, not Path.cwd() (mirrors sync-content.py).
REPO_ROOT: Path = Path(__file__).resolve().parents[1]
PLUGIN_SKILLS_DIR: Path = REPO_ROOT / "first-principles" / "skills"

# Regex to split on a frontmatter fence line (^---\s*$).
_FENCE_RE = re.compile(r"^---\s*$", re.MULTILINE)


def iter_plugin_skills() -> Iterator[tuple[str, dict, str]]:
    """Yield (slug, frontmatter_dict, body_str) for each plugin skill.

    Walks PLUGIN_SKILLS_DIR for direct child directories containing SKILL.md.
    Yields tuples sorted by slug for deterministic stderr output across runs.

    Raises:
        ValueError: if a SKILL.md has non-mapping frontmatter or is missing
                    the closing frontmatter fence.
        FileNotFoundError: propagated from Path.read_text if SKILL.md vanishes
                           between directory listing and read.

    Defensive early-return: if PLUGIN_SKILLS_DIR does not exist (e.g., after
    the Phase 26.1 migration deletes first-principles/skills/), yield nothing
    rather than raising FileNotFoundError. Consumers (check-trigger-collisions,
    check-description-budget) treat an empty iterator as "0 plugin skills" —
    the agent surface is checked separately.
    """
    if not PLUGIN_SKILLS_DIR.exists():
        return

    skill_dirs = sorted(
        d for d in PLUGIN_SKILLS_DIR.iterdir()
        if d.is_dir() and (d / "SKILL.md").exists()
    )

    for skill_dir in skill_dirs:
        slug = skill_dir.name
        skill_path = skill_dir / "SKILL.md"
        text = skill_path.read_text(encoding="utf-8")

        # Split on closing frontmatter fence; maxsplit=2 → ["", fm_text, body_text].
        parts = _FENCE_RE.split(text, maxsplit=2)
        if len(parts) < 3:
            raise ValueError(f"{slug}/SKILL.md is missing closing frontmatter fence")

        fm_text = parts[1]
        body = parts[2]  # Preserve leading newlines (byte-level fidelity).

        frontmatter = yaml.safe_load(fm_text)

        # WR-05: reject non-mapping results (None, list, scalar) with a structured error.
        if not isinstance(frontmatter, dict):
            got = "empty/null" if frontmatter is None else type(frontmatter).__name__
            raise ValueError(
                f"{slug}/SKILL.md frontmatter is not a mapping (got {got})"
            )

        yield (slug, frontmatter, body)
