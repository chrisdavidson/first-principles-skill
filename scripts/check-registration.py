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


def parse_manifest(manifest_path: Path) -> dict:
    """Parse the plugin manifest JSON file and return its root object.

    Implements REG-03 and D-05/D-09. This is the one helper permitted to
    call sys.exit(), because D-09 locks fail-fast semantics on a malformed
    manifest — matching check-agent.py's malformed-input treatment. Exit
    code 2 (environment error), never 1: a malformed manifest is a broken
    environment, not a content-validation failure.
    """
    if not manifest_path.is_file():
        sys.stderr.write(
            f"check-registration: manifest not found: {manifest_path}\n"
        )
        sys.exit(2)

    try:
        text = manifest_path.read_text(encoding="utf-8")
    except OSError as exc:
        sys.stderr.write(
            f"check-registration: cannot read manifest: {exc}\n"
        )
        sys.exit(2)

    try:
        manifest = json.loads(text)
    except json.JSONDecodeError as exc:
        sys.stderr.write(
            f"check-registration: malformed JSON in manifest: {exc}\n"
        )
        sys.exit(2)

    # V5 input validation: do not assume shape. The schema requires the root
    # to be a JSON object; a list or scalar root would fail later and less
    # clearly on .get() calls in extract_registered_paths().
    if not isinstance(manifest, dict):
        sys.stderr.write(
            "check-registration: manifest root is not a JSON object\n"
        )
        sys.exit(2)

    return manifest


def extract_registered_paths(manifest: dict) -> tuple[list[str], list[str]]:
    """Return (skill_paths, agent_paths) normalized from manifest fields.

    Implements D-07/D-08. Per the official plugin manifest schema, `skills`
    and `agents` are optional *additional path* fields (string or array of
    strings) — not a name/type roster. An absent key is the normal,
    schema-valid default-auto-discovery state, never an error. Phase 2 still
    has to decide what "registered" means for REG-04/REG-05 comparison work
    (RESEARCH.md Open Question #1); this function only normalizes the raw
    field values and does not attempt any name/type comparison.
    """

    def _normalize(value: object) -> list[str]:
        if value is None:
            return []
        if isinstance(value, str):
            return [value]
        if isinstance(value, list):
            return value
        return []

    skill_paths = _normalize(manifest.get("skills"))
    agent_paths = _normalize(manifest.get("agents"))
    return (skill_paths, agent_paths)


def build_discovery_report(
    skills: set[str],
    agent_present: bool,
    agent_path: Path,
    manifest: dict,
    manifest_path: Path,
) -> dict:
    """Return a pure, JSON-serializable discovery report dict.

    Implements D-13/D-14. No I/O — Phase 2 can call this with in-memory
    fixtures. Every value is JSON-serializable: no Path objects, no sets.
    """
    registered_skill_paths, registered_agent_paths = extract_registered_paths(
        manifest
    )
    registration_source = (
        "manifest-paths"
        if (registered_skill_paths or registered_agent_paths)
        else "default-directory-auto-discovery"
    )
    return {
        "discovered_skills": sorted(skills),
        "discovered_skill_count": len(skills),
        "discovered_agent": {
            "name": AGENT_NAME,
            "present": agent_present,
            "path": str(agent_path),
        },
        "manifest_path": str(manifest_path),
        "manifest_skills_field": manifest.get("skills"),
        "manifest_agents_field": manifest.get("agents"),
        "registered_skill_paths": registered_skill_paths,
        "registered_agent_paths": registered_agent_paths,
        "registration_source": registration_source,
    }


def format_report_text(report: dict) -> str:
    """Render a discovery report dict as human-readable multi-line text."""
    lines: list[str] = []

    skills = report["discovered_skills"]
    lines.append(f"Discovered skills ({report['discovered_skill_count']}):")
    for name in skills:
        lines.append(f"  {name}")

    agent = report["discovered_agent"]
    presence = "present" if agent["present"] else "absent"
    lines.append(
        f"Discovered agent: {agent['name']} ({presence}) at {agent['path']}"
    )

    lines.append(f"Manifest: {report['manifest_path']}")

    skills_field = report["manifest_skills_field"]
    lines.append(
        f"Manifest skills field: {skills_field if skills_field is not None else 'absent'}"
    )
    agents_field = report["manifest_agents_field"]
    lines.append(
        f"Manifest agents field: {agents_field if agents_field is not None else 'absent'}"
    )

    lines.append(f"Registration source: {report['registration_source']}")

    return "\n".join(lines)


def _run_self_test() -> None:
    raise NotImplementedError("Task 3 adds the offline self-test")


def main() -> None:
    parser = argparse.ArgumentParser(
        description=(
            "REG-GUARD (Phase 1 discovery): enumerate plugin skills/agent "
            "and parse the plugin manifest."
        )
    )
    parser.add_argument(
        "--self-test",
        action="store_true",
        help="run the offline deterministic fixture mode (no live session)",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="emit the discovery report as JSON instead of human-readable text",
    )
    args = parser.parse_args()

    _require_python_version()

    if args.self_test:
        _run_self_test()
        return

    skills = discover_skills(SKILLS_DIR)
    agent_present, agent_path = discover_agent(AGENT_PATH)
    manifest = parse_manifest(MANIFEST_PATH)
    report = build_discovery_report(
        skills, agent_present, agent_path, manifest, MANIFEST_PATH
    )

    # Non-vacuity guards, mirroring COLLIDE-01's `if not plugin_names` guard.
    # These are the only two live failure conditions in Phase 1 — manifest
    # registration comparison is Phase 2's job and must not gate here.
    if not skills:
        sys.stderr.write(
            "check-registration: FAIL — discovered 0 skill directories under "
            f"{SKILLS_DIR} (collector regression? expected a populated set)\n"
        )
        sys.exit(1)

    if not agent_present:
        sys.stderr.write(
            f"check-registration: FAIL — main agent not found at {agent_path}\n"
        )
        sys.exit(1)

    pass_line = (
        f"check-registration: PASS (discovered {len(skills)} skills, "
        "agent present, manifest parsed)"
    )

    if args.json:
        # PASS line goes to stderr in --json mode so stdout stays pure JSON,
        # parseable with no stripping.
        print(json.dumps(report, indent=2))
        sys.stderr.write(pass_line + "\n")
    else:
        print(format_report_text(report))
        print(pass_line)

    sys.exit(0)


if __name__ == "__main__":
    main()
