#!/usr/bin/env python3
# /// script
# requires-python = ">=3.12"
# dependencies = ["pyyaml>=6.0"]
# ///
# NOTE: D-02 (Phase 2) deliberately overrides 02-RESEARCH.md's Pitfall 3
# stdlib-only recommendation — PyYAML robustness on frontmatter edge cases
# (multiline block scalars, complex quoting) is worth the added dependency.
# Do not "restore" the dependency-free `[]` form.
"""REG-GUARD (Phase 1/2) discovery + verification layer: enumerate plugin
skills/agent, parse the plugin manifest, and verify frontmatter `name:`
fields match their conventional directory/file basenames.

Usage:
    python3 scripts/check-registration.py [--self-test] [--json]

Exit codes: 0 pass, 1 validation/content failure, 2 environment error.

--self-test: runs 21 named, decision-traceable controls against tempdir and
in-memory fixtures — fully offline and deterministic, no network access and
no live Claude session, independent of the live first-principles/ tree.
"""

from __future__ import annotations

import argparse
import glob
import json
import os
import re
import sys
import tempfile
from pathlib import Path

try:
    import yaml
except ImportError:
    sys.stderr.write(
        "check-registration: PyYAML is required (pip install 'pyyaml>=6.0')\n"
    )
    sys.exit(2)


REPO_ROOT: Path = Path(__file__).resolve().parents[1]
PLUGIN_DIR: Path = REPO_ROOT / "first-principles"
SKILLS_DIR: Path = PLUGIN_DIR / "skills"
AGENT_NAME: str = "first-principles"
AGENT_PATH: Path = PLUGIN_DIR / "agents" / "first-principles.md"
MANIFEST_PATH: Path = PLUGIN_DIR / ".claude-plugin" / "plugin.json"

# Matches scripts/_skill_io.py's constant of the same name — splits frontmatter
# text on the `---` fence lines.
_FENCE_RE = re.compile(r"^---\s*$", re.MULTILINE)


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


def extract_frontmatter_name(text: str) -> str | None:
    """Return the frontmatter `name:` value from already-read SKILL.md/agent
    text, or None for any malformed or absent shape.

    Implements REG-04/REG-05 (Phase 2) and D-02/D-04. Pure function — takes
    text, never a Path, so self-test controls can drive it with in-memory
    literals (D-04). Nothing in this function raises: malformed frontmatter
    is a finding, not a crash (ASVS V5, threat T-02-01).
    """
    parts = _FENCE_RE.split(text, maxsplit=2)
    if len(parts) < 3:
        return None
    if parts[0].strip():
        # Content before the opening fence — not valid frontmatter.
        return None

    try:
        frontmatter = yaml.safe_load(parts[1])
    except yaml.YAMLError:
        return None

    if not isinstance(frontmatter, dict):
        return None

    name = frontmatter.get("name")
    if not isinstance(name, str):
        return None
    name = name.strip()
    if not name:
        return None
    return name


def _read_frontmatter_name(path: Path) -> str | None:
    """Thin I/O wrapper around extract_frontmatter_name for a file on disk.

    Implements D-04's tempdir-driven wrapper tier. Keeps the read and the
    parse split exactly this way so the pure branch stays file-I/O-free.
    """
    try:
        text = path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return None
    return extract_frontmatter_name(text)


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


def verify_skill_names(skills: set[str], skills_dir: Path) -> list[dict]:
    """Verify each discovered skill's SKILL.md frontmatter `name:` matches its
    directory basename.

    Implements REG-04/REG-05 per D-01: "registered with correct name/type" is
    reinterpreted as present-at-conventional-path AND frontmatter name equals
    the basename. Returns one record per skill, iterating `sorted(skills)`
    for deterministic output. Never calls sys.exit — gating is Plan 02's job.
    """
    records: list[dict] = []
    for name in sorted(skills):
        skill_md = skills_dir / name / "SKILL.md"
        frontmatter_name = (
            _read_frontmatter_name(skill_md) if skill_md.is_file() else None
        )
        records.append(
            {
                "directory_name": name,
                "frontmatter_name": frontmatter_name,
                "type": "skill",
                "matches": frontmatter_name == name,
            }
        )
    return records


def verify_agent_name(
    agent_present: bool, agent_path: Path, expected_name: str
) -> dict:
    """Verify the main agent's frontmatter `name:` matches expected_name.

    Implements REG-04/REG-05 per D-01, singular equivalent of
    verify_skill_names(). Callers pass the existing AGENT_NAME constant as
    expected_name rather than a second literal. Never calls sys.exit.
    """
    frontmatter_name = _read_frontmatter_name(agent_path) if agent_present else None
    return {
        "expected_name": expected_name,
        "frontmatter_name": frontmatter_name,
        "type": "agent",
        "present": agent_present,
        "matches": agent_present and frontmatter_name == expected_name,
    }


def verify_manifest_paths(
    registered_skill_paths: list[str],
    registered_agent_paths: list[str],
    plugin_dir: Path,
) -> list[dict]:
    """Verify each manifest-declared path resolves to an existing file inside
    plugin_dir.

    Implements D-03. Takes the already-normalized path lists that
    extract_registered_paths() produces, plus a base directory, so a
    self-test can drive it with fabricated data — it must not read
    MANIFEST_PATH or any module constant. Emits skill records first, then
    agent records, preserving input order. Returns [] when both input lists
    are empty (the live tree's normal state today).

    Resolution rule (threat T-02-03): the joined target must BOTH exist on
    disk AND stay inside plugin_dir after resolution (Path.is_relative_to()
    against plugin_dir.resolve()) — an absolute path or a `..` escape reports
    resolved: False rather than silently resolving outside the plugin.
    """
    plugin_dir_resolved = plugin_dir.resolve()

    def _resolve(declared_path: str) -> bool:
        stripped = declared_path[2:] if declared_path.startswith("./") else declared_path
        candidate = plugin_dir / stripped
        if not candidate.exists():
            return False
        return candidate.resolve().is_relative_to(plugin_dir_resolved)

    records: list[dict] = []
    for declared_path in registered_skill_paths:
        records.append(
            {
                "declared_path": declared_path,
                "component_kind": "skill",
                "resolved": _resolve(declared_path),
            }
        )
    for declared_path in registered_agent_paths:
        records.append(
            {
                "declared_path": declared_path,
                "component_kind": "agent",
                "resolved": _resolve(declared_path),
            }
        )
    return records


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


def _write_skills_fixture(base: Path) -> None:
    """Build a synthetic skills-directory fixture under base for --self-test.

    Creates real directories alpha and beta, a hidden directory .hidden, a
    symlink gamma pointing at alpha, and a plain file notes.txt — exercising
    all three discover_skills() exclusions (D-10, D-11, D-12) in one fixture.
    """
    (base / "alpha").mkdir(parents=True, exist_ok=True)
    (base / "beta").mkdir(parents=True, exist_ok=True)
    (base / ".hidden").mkdir(parents=True, exist_ok=True)
    (base / "gamma").symlink_to(base / "alpha")
    (base / "notes.txt").write_text("", encoding="utf-8")


def _run_self_test() -> None:
    """Run 15 named, decision-traceable offline controls against the
    production helpers, using tempdir and in-memory fixtures only.

    Fully deterministic and offline: no network, no live Claude session, no
    dependence on the live first-principles/ tree, so adding or removing a
    skill can never flip this self-test. Every control invokes a production
    helper by name — none reimplements a filter or parser inline — so a
    no-op helper cannot pass.
    """
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        _write_skills_fixture(tmp_path)

        # Control 1 — D-10 dotfile exclusion. Set equality (not a membership
        # check) proves the filter removed .hidden AND kept the real entries.
        result = discover_skills(tmp_path)
        if result != {"alpha", "beta"}:
            sys.stderr.write(
                "check-registration --self-test: FAIL — D-10 dotfile "
                f"exclusion: discover_skills returned {sorted(result)}, "
                "expected ['alpha', 'beta']\n"
            )
            sys.exit(1)

        # Control 2 — D-11 symlink exclusion. Anti-masking: the symlink
        # target (alpha) itself must survive the exclusion.
        if "gamma" in result:
            sys.stderr.write(
                "check-registration --self-test: FAIL — D-11 symlink "
                "exclusion: 'gamma' present in discover_skills result\n"
            )
            sys.exit(1)
        if "alpha" not in result:
            sys.stderr.write(
                "check-registration --self-test: FAIL — D-11 symlink "
                "exclusion: 'alpha' (the symlink target) missing from "
                "discover_skills result — filter is over-broad\n"
            )
            sys.exit(1)

        # Control 3 — D-12 non-directory exclusion.
        if "notes.txt" in result or "notes" in result:
            sys.stderr.write(
                "check-registration --self-test: FAIL — D-12 non-directory "
                f"exclusion: plain file leaked into result {sorted(result)}\n"
            )
            sys.exit(1)

        # Control 4 — absent skills dir returns empty set, never raises.
        absent_result = discover_skills(tmp_path / "does-not-exist")
        if absent_result != set():
            sys.stderr.write(
                "check-registration --self-test: FAIL — absent skills dir: "
                f"discover_skills returned {sorted(absent_result)}, expected []\n"
            )
            sys.exit(1)

        # Control 5 — agent present.
        agent_file = tmp_path / "agent.md"
        agent_file.write_text("agent body\n", encoding="utf-8")
        present, path = discover_agent(agent_file)
        if not (present is True and path == agent_file):
            sys.stderr.write(
                "check-registration --self-test: FAIL — agent present: "
                f"discover_agent returned ({present!r}, {path!r})\n"
            )
            sys.exit(1)

        # Control 6 — agent absent.
        missing_agent = tmp_path / "missing.md"
        present, path = discover_agent(missing_agent)
        if not (present is False and path == missing_agent):
            sys.stderr.write(
                "check-registration --self-test: FAIL — agent absent: "
                f"discover_agent returned ({present!r}, {path!r})\n"
            )
            sys.exit(1)

        # Control 7 — manifest valid.
        good_manifest = tmp_path / "good.json"
        good_manifest.write_text('{"name": "x"}', encoding="utf-8")
        parsed = parse_manifest(good_manifest)
        if parsed != {"name": "x"}:
            sys.stderr.write(
                "check-registration --self-test: FAIL — manifest valid: "
                f"parse_manifest returned {parsed!r}\n"
            )
            sys.exit(1)

        # Control 8 — D-09 malformed JSON fail-fast. Must prove SystemExit
        # actually fires, not merely that no exception escaped.
        bad_manifest = tmp_path / "bad.json"
        bad_manifest.write_text("{not json", encoding="utf-8")
        raised = False
        try:
            parse_manifest(bad_manifest)
        except SystemExit as exc:
            raised = True
            if exc.code != 2:
                sys.stderr.write(
                    "check-registration --self-test: FAIL — D-09 malformed "
                    f"JSON fail-fast: exit code {exc.code}, expected 2\n"
                )
                sys.exit(1)
        if not raised:
            sys.stderr.write(
                "check-registration --self-test: FAIL — D-09 malformed JSON "
                "fail-fast: parse_manifest did not raise SystemExit\n"
            )
            sys.exit(1)

        # Control 9 — non-object manifest root.
        array_manifest = tmp_path / "arr.json"
        array_manifest.write_text("[]", encoding="utf-8")
        raised = False
        try:
            parse_manifest(array_manifest)
        except SystemExit as exc:
            raised = True
            if exc.code != 2:
                sys.stderr.write(
                    "check-registration --self-test: FAIL — non-object "
                    f"manifest root: exit code {exc.code}, expected 2\n"
                )
                sys.exit(1)
        if not raised:
            sys.stderr.write(
                "check-registration --self-test: FAIL — non-object manifest "
                "root: parse_manifest did not raise SystemExit\n"
            )
            sys.exit(1)

        # Control 10 — missing manifest.
        raised = False
        try:
            parse_manifest(tmp_path / "nope.json")
        except SystemExit as exc:
            raised = True
            if exc.code != 2:
                sys.stderr.write(
                    "check-registration --self-test: FAIL — missing "
                    f"manifest: exit code {exc.code}, expected 2\n"
                )
                sys.exit(1)
        if not raised:
            sys.stderr.write(
                "check-registration --self-test: FAIL — missing manifest: "
                "parse_manifest did not raise SystemExit\n"
            )
            sys.exit(1)

    # Control 11 — D-07 absent keys tolerated. Direct negative control
    # against the Pitfall-3 failure mode (treating an absent key as an error).
    absent_keys_result = extract_registered_paths({})
    if absent_keys_result != ([], []):
        sys.stderr.write(
            "check-registration --self-test: FAIL — D-07 absent keys "
            f"tolerated: extract_registered_paths({{}}) returned "
            f"{absent_keys_result!r}\n"
        )
        sys.exit(1)

    # Control 12 — string-valued field normalization.
    string_field_result = extract_registered_paths({"skills": "./x"})
    if string_field_result != (["./x"], []):
        sys.stderr.write(
            "check-registration --self-test: FAIL — string-valued field "
            f"normalization: got {string_field_result!r}\n"
        )
        sys.exit(1)

    # Control 13 — list-valued field passthrough.
    list_field_result = extract_registered_paths(
        {"agents": ["./a.md", "./b.md"]}
    )
    if list_field_result != ([], ["./a.md", "./b.md"]):
        sys.stderr.write(
            "check-registration --self-test: FAIL — list-valued field "
            f"passthrough: got {list_field_result!r}\n"
        )
        sys.exit(1)

    # Control 14 — report shape. Key-set equality, JSON round-trip, and the
    # default-auto-discovery registration_source for an empty manifest.
    fixture_skills = {"alpha", "beta"}
    fixture_agent_path = Path("/synthetic/agents/agent.md")
    report = build_discovery_report(
        fixture_skills, True, fixture_agent_path, {}, Path("/synthetic/manifest.json")
    )
    expected_keys = {
        "discovered_skills",
        "discovered_skill_count",
        "discovered_agent",
        "manifest_path",
        "manifest_skills_field",
        "manifest_agents_field",
        "registered_skill_paths",
        "registered_agent_paths",
        "registration_source",
    }
    if set(report) != expected_keys:
        sys.stderr.write(
            "check-registration --self-test: FAIL — report shape: key set "
            f"{sorted(report)} != expected {sorted(expected_keys)}\n"
        )
        sys.exit(1)
    round_tripped = json.loads(json.dumps(report))
    if round_tripped != report:
        sys.stderr.write(
            "check-registration --self-test: FAIL — report shape: JSON "
            "round-trip did not equal the original report\n"
        )
        sys.exit(1)
    if report["registration_source"] != "default-directory-auto-discovery":
        sys.stderr.write(
            "check-registration --self-test: FAIL — report shape: expected "
            "registration_source 'default-directory-auto-discovery', got "
            f"{report['registration_source']!r}\n"
        )
        sys.exit(1)

    # Control 15 — report registration_source flips. Anti-constant control
    # for control 14: without this, a hardcoded return value would pass.
    flipped_report = build_discovery_report(
        fixture_skills,
        True,
        fixture_agent_path,
        {"skills": "./extra"},
        Path("/synthetic/manifest.json"),
    )
    if flipped_report["registration_source"] != "manifest-paths":
        sys.stderr.write(
            "check-registration --self-test: FAIL — report "
            "registration_source flips: expected 'manifest-paths', got "
            f"{flipped_report['registration_source']!r}\n"
        )
        sys.exit(1)

    print(
        "check-registration --self-test: PASS (15 controls: discovery "
        "exclusions D-10/D-11/D-12, agent presence, manifest fail-fast "
        "D-09, absent-key tolerance D-07, report shape)"
    )
    sys.exit(0)


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
