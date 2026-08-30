#!/usr/bin/env python3
# /// script
# requires-python = ">=3.12"
# dependencies = []
# ///
"""REG-GUARD (Phase 1) discovery layer: enumerate plugin skills/agent and parse
the plugin manifest.

Usage:
    python3 scripts/check-registration.py [--self-test] [--json]

Exit codes: 0 pass, 1 validation/content failure, 2 environment error.
"""

from __future__ import annotations

import argparse
import glob
import json
import os
import sys
import tempfile
from pathlib import Path


REPO_ROOT: Path = Path(__file__).resolve().parents[1]
PLUGIN_DIR: Path = REPO_ROOT / "first-principles"
SKILLS_DIR: Path = PLUGIN_DIR / "skills"
AGENT_NAME: str = "first-principles"
AGENT_PATH: Path = PLUGIN_DIR / "agents" / "first-principles.md"
MANIFEST_PATH: Path = PLUGIN_DIR / ".claude-plugin" / "plugin.json"


def _require_python_version() -> None:
    if sys.version_info < (3, 12):
        sys.stderr.write(
            f"scripts/check-registration.py requires Python >=3.12 "
            f"(running {sys.version_info.major}.{sys.version_info.minor}).\n"
        )
        sys.exit(2)


def discover_skills(skills_dir: Path) -> set[str]:
    """Return the set of skill directory basenames under skills_dir.

    Implements REG-01 and D-01/D-03. Returns an empty set (never raises) if
    skills_dir does not exist or is not a directory — absence is tolerated at
    the helper layer, main() decides whether an empty result is a failure.

    D-10 (dotfile exclusion): uses the module-level `glob.glob()` function
    rather than the pathlib method of the same name — glob.glob excludes
    dotfile entries by default, while the pathlib method does not on Python
    3.13+ (this repo runs 3.14.7). Do not "simplify" this call away.
    """
    if not skills_dir.exists() or not skills_dir.is_dir():
        return set()

    pattern = glob.escape(str(skills_dir)) + "/*/"
    result: set[str] = set()
    for entry in glob.glob(pattern):
        p = Path(entry.rstrip("/"))
        # D-11: check symlink status BEFORE is_dir() — is_dir() follows the
        # link and would return True for a symlink pointing at a directory.
        if p.is_symlink():
            continue
        # D-12: non-directory entries are ignored.
        if not p.is_dir():
            continue
        result.add(p.name)
    return result


def discover_agent(agent_path: Path) -> tuple[bool, Path]:
    """Return (present, agent_path) for the fixed main-agent path.

    Implements REG-02 and D-02/D-04. Fixed path, no glob. A symlink at
    agent_path is reported absent, for consistency with the D-11 symlink
    exclusion applied to skill discovery.
    """
    if agent_path.is_symlink():
        return (False, agent_path)
    return (agent_path.is_file(), agent_path)


if __name__ == "__main__":
    raise SystemExit(
        "scripts/check-registration.py: main() not yet defined (Task 2)"
    )
