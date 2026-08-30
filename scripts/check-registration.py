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
    *,
    skills_dir: Path = SKILLS_DIR,
    plugin_dir: Path = PLUGIN_DIR,
) -> dict:
    """Return a pure, JSON-serializable discovery report dict.

    Implements D-13/D-14. No I/O beyond what verify_skill_names/
    verify_agent_name perform via their own file reads — Phase 2 can call
    this with in-memory fixtures by passing skills_dir/plugin_dir. Every
    value is JSON-serializable: no Path objects, no sets.

    D-05 (Plan 02): three verification keys are appended after
    registration_source, preserving the flat single-level shape and the
    nine Phase 1 keys byte-identical.
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
        "skill_name_verification": verify_skill_names(skills, skills_dir),
        "agent_name_verification": verify_agent_name(
            agent_present, agent_path, AGENT_NAME
        ),
        "manifest_path_verification": verify_manifest_paths(
            registered_skill_paths, registered_agent_paths, plugin_dir
        ),
    }


def collect_verification_failures(report: dict) -> list[str]:
    """Return one human-readable failure line per registration-verification
    finding in report, or [] on a clean report.

    Implements REG-06's accumulate-then-report requirement — every
    discrepancy in one run, not just the first. Reads only the three
    verification keys build_discovery_report() adds; never calls sys.exit.
    """
    failures: list[str] = []

    for record in report["skill_name_verification"]:
        if not record["matches"]:
            frontmatter_name = record["frontmatter_name"] or "(none)"
            failures.append(
                "skill name mismatch: directory "
                f"'{record['directory_name']}' vs frontmatter "
                f"'{frontmatter_name}'"
            )

    agent_record = report["agent_name_verification"]
    if not agent_record["matches"]:
        if not agent_record["present"]:
            failures.append(
                f"agent absent: expected '{agent_record['expected_name']}' "
                "not found at conventional path"
            )
        else:
            frontmatter_name = agent_record["frontmatter_name"] or "(none)"
            failures.append(
                f"agent name mismatch: expected '{agent_record['expected_name']}' "
                f"vs frontmatter '{frontmatter_name}'"
            )

    for record in report["manifest_path_verification"]:
        if not record["resolved"]:
            failures.append(
                f"manifest {record['component_kind']} path does not resolve "
                f"under the plugin directory: '{record['declared_path']}'"
            )

    return failures


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

    skill_verifications = report["skill_name_verification"]
    skill_matched = sum(1 for r in skill_verifications if r["matches"])
    skill_total = len(skill_verifications)
    skill_mismatches = skill_total - skill_matched

    agent_verification = report["agent_name_verification"]
    if agent_verification["matches"]:
        agent_status = f"name-matched ({agent_verification['expected_name']})"
    elif not agent_verification["present"]:
        agent_status = f"MISMATCH — absent (expected '{agent_verification['expected_name']}')"
    else:
        frontmatter_name = agent_verification["frontmatter_name"] or "(none)"
        agent_status = (
            f"MISMATCH — expected '{agent_verification['expected_name']}' vs "
            f"frontmatter '{frontmatter_name}'"
        )

    path_verifications = report["manifest_path_verification"]
    path_skill_count = sum(
        1 for r in path_verifications if r["component_kind"] == "skill"
    )
    path_agent_count = sum(
        1 for r in path_verifications if r["component_kind"] == "agent"
    )
    path_unresolved = sum(1 for r in path_verifications if not r["resolved"])

    lines.append("")
    lines.append("Registration verification (REG-04/REG-05):")
    lines.append(
        f"  Skills verified: {skill_matched}/{skill_total} name-matched, "
        f"{skill_mismatches} mismatch(es)"
    )
    lines.append(f"  Agent verified: {agent_status}")
    lines.append(
        "  Manifest-declared additional paths: "
        f"{path_skill_count} skills, {path_agent_count} agents "
        f"({path_unresolved} unresolved)"
    )

    failures = collect_verification_failures(report)
    if failures:
        lines.append("  Failures:")
        for failure in failures:
            lines.append(f"    {failure}")

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
    # Task 1 (Plan 02): the report now carries 12 keys, including three
    # verification keys. This control drives synthetic skill names/agent
    # path against the DEFAULT live skills_dir/plugin_dir, so the new
    # records legitimately carry frontmatter_name: None / matches: False —
    # shape only. Control 22 owns the values axis against a real fixture.
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
        "skill_name_verification",
        "agent_name_verification",
        "manifest_path_verification",
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

    # Control 16 — extract_frontmatter_name on literal strings (in-memory,
    # D-04): plain scalar, single-quoted, and double-quoted name values all
    # return the bare name.
    for literal, expected in (
        ("---\nname: alpha\n---\nbody", "alpha"),
        ("---\nname: 'alpha'\n---\nbody", "alpha"),
        ('---\nname: "alpha"\n---\nbody', "alpha"),
    ):
        got = extract_frontmatter_name(literal)
        if got != expected:
            sys.stderr.write(
                "check-registration --self-test: FAIL — Control 16 literal "
                f"frontmatter name extraction: {literal!r} -> {got!r}, "
                f"expected {expected!r}\n"
            )
            sys.exit(1)

    # Control 17 — anti-constant control for Control 16: a literal whose
    # frontmatter says `name: beta` must return exactly "beta", not a
    # hardcoded "alpha".
    beta_result = extract_frontmatter_name("---\nname: beta\n---\nbody")
    if beta_result != "beta":
        sys.stderr.write(
            "check-registration --self-test: FAIL — Control 17 anti-constant: "
            f"expected 'beta', got {beta_result!r}\n"
        )
        sys.exit(1)

    # Control 18 — malformed frontmatter shapes all return None without
    # raising (in-memory, D-04; ASVS V5, threat T-02-01).
    malformed_cases = {
        "no name key": "---\ndescription: x\n---\nbody",
        "no fences at all": "just some plain text, no frontmatter",
        "opening fence but no closing fence": "---\nname: alpha\nbody text",
        "content before opening fence": "leading content\n---\nname: alpha\n---\nbody",
        "unparseable YAML": "---\nname: [unterminated\n---\nbody",
    }
    for case_name, text in malformed_cases.items():
        result = extract_frontmatter_name(text)
        if result is not None:
            sys.stderr.write(
                "check-registration --self-test: FAIL — Control 18 malformed "
                f"frontmatter ({case_name}): expected None, got {result!r}\n"
            )
            sys.exit(1)

    # Control 19 — verify_skill_names against a mixed tempdir fixture
    # (D-04 wrapper tier): alpha matches, beta mismatches, delta has no
    # SKILL.md at all.
    with tempfile.TemporaryDirectory() as tmp19:
        tmp19_path = Path(tmp19)
        (tmp19_path / "alpha").mkdir(parents=True)
        (tmp19_path / "alpha" / "SKILL.md").write_text(
            "---\nname: alpha\n---\nbody", encoding="utf-8"
        )
        (tmp19_path / "beta").mkdir(parents=True)
        (tmp19_path / "beta" / "SKILL.md").write_text(
            "---\nname: gamma\n---\nbody", encoding="utf-8"
        )
        (tmp19_path / "delta").mkdir(parents=True)

        skill_records = verify_skill_names({"alpha", "beta", "delta"}, tmp19_path)
        expected_records = [
            {
                "directory_name": "alpha",
                "frontmatter_name": "alpha",
                "type": "skill",
                "matches": True,
            },
            {
                "directory_name": "beta",
                "frontmatter_name": "gamma",
                "type": "skill",
                "matches": False,
            },
            {
                "directory_name": "delta",
                "frontmatter_name": None,
                "type": "skill",
                "matches": False,
            },
        ]
        if skill_records != expected_records:
            sys.stderr.write(
                "check-registration --self-test: FAIL — Control 19 "
                f"verify_skill_names: got {skill_records!r}, expected "
                f"{expected_records!r}\n"
            )
            sys.exit(1)
        # Anti-masking: at least one True and one False, so neither a
        # constant-True nor constant-False implementation can pass.
        matches_seen = {r["matches"] for r in skill_records}
        if matches_seen != {True, False}:
            sys.stderr.write(
                "check-registration --self-test: FAIL — Control 19 "
                "anti-masking: verify_skill_names matches values were "
                f"{matches_seen!r}, expected both True and False present\n"
            )
            sys.exit(1)

    # Control 20 — verify_agent_name against a mixed tempdir fixture:
    # matching name, mismatched name, and an absent agent file.
    with tempfile.TemporaryDirectory() as tmp20:
        tmp20_path = Path(tmp20)

        matching_agent = tmp20_path / "matching-agent.md"
        matching_agent.write_text(
            "---\nname: first-principles\n---\nbody", encoding="utf-8"
        )
        matching_result = verify_agent_name(True, matching_agent, "first-principles")
        if not (
            matching_result["matches"] is True
            and matching_result["frontmatter_name"] == "first-principles"
        ):
            sys.stderr.write(
                "check-registration --self-test: FAIL — Control 20 "
                f"verify_agent_name matching case: {matching_result!r}\n"
            )
            sys.exit(1)

        mismatched_agent = tmp20_path / "mismatched-agent.md"
        mismatched_agent.write_text("---\nname: other\n---\nbody", encoding="utf-8")
        mismatched_result = verify_agent_name(
            True, mismatched_agent, "first-principles"
        )
        if not (
            mismatched_result["matches"] is False
            and mismatched_result["frontmatter_name"] == "other"
        ):
            sys.stderr.write(
                "check-registration --self-test: FAIL — Control 20 "
                f"verify_agent_name mismatched case: {mismatched_result!r}\n"
            )
            sys.exit(1)

        absent_agent = tmp20_path / "does-not-exist.md"
        absent_result = verify_agent_name(False, absent_agent, "first-principles")
        if not (
            absent_result["matches"] is False
            and absent_result["present"] is False
            and absent_result["frontmatter_name"] is None
        ):
            sys.stderr.write(
                "check-registration --self-test: FAIL — Control 20 "
                f"verify_agent_name absent case: {absent_result!r}\n"
            )
            sys.exit(1)

    # Control 21 — verify_manifest_paths against a mixed tempdir fixture:
    # a resolving path, a non-existent path, a `../` escape (containment,
    # threat T-02-03), and the empty-lists case.
    with tempfile.TemporaryDirectory() as tmp21:
        tmp21_path = Path(tmp21)
        plugin_root = tmp21_path / "plugin"
        (plugin_root / "skills" / "alpha").mkdir(parents=True)
        (plugin_root / "skills" / "alpha" / "SKILL.md").write_text(
            "body", encoding="utf-8"
        )
        (plugin_root / "agents").mkdir(parents=True)
        (plugin_root / "agents" / "agent.md").write_text("body", encoding="utf-8")
        # A real file OUTSIDE plugin_root, so the escape control proves
        # containment rather than mere absence.
        (tmp21_path / "escape.md").write_text("body", encoding="utf-8")

        path_records = verify_manifest_paths(
            [
                "./skills/alpha/SKILL.md",
                "./skills/does-not-exist/",
                "../escape.md",
            ],
            ["./agents/agent.md"],
            plugin_root,
        )
        if len(path_records) != 4:
            sys.stderr.write(
                "check-registration --self-test: FAIL — Control 21 "
                f"verify_manifest_paths record count: got {len(path_records)}, "
                "expected 4\n"
            )
            sys.exit(1)
        resolved_flags = [r["resolved"] for r in path_records]
        if resolved_flags != [True, False, False, True]:
            sys.stderr.write(
                "check-registration --self-test: FAIL — Control 21 "
                f"verify_manifest_paths resolved flags: got {resolved_flags!r}, "
                "expected [True, False, False, True]\n"
            )
            sys.exit(1)
        kinds = [r["component_kind"] for r in path_records]
        if kinds != ["skill", "skill", "skill", "agent"]:
            sys.stderr.write(
                "check-registration --self-test: FAIL — Control 21 "
                f"verify_manifest_paths component_kind: got {kinds!r}\n"
            )
            sys.exit(1)

        empty_records = verify_manifest_paths([], [], plugin_root)
        if empty_records != []:
            sys.stderr.write(
                "check-registration --self-test: FAIL — Control 21 "
                f"verify_manifest_paths empty inputs: got {empty_records!r}, "
                "expected []\n"
            )
            sys.exit(1)

    # Control 22 — report shape against a REAL tempdir fixture (Plan 02):
    # two skill directories (one matching, one mismatched) plus an agent
    # file, driven through build_discovery_report() with skills_dir/
    # plugin_dir pointed at the fixture. Unlike Control 14 (shape only,
    # against the default live tree), this control additionally asserts
    # the verification records' VALUES — the axis Control 14 deliberately
    # does not cover.
    with tempfile.TemporaryDirectory() as tmp22:
        tmp22_path = Path(tmp22)
        (tmp22_path / "skills" / "alpha").mkdir(parents=True)
        (tmp22_path / "skills" / "alpha" / "SKILL.md").write_text(
            "---\nname: alpha\n---\nbody", encoding="utf-8"
        )
        (tmp22_path / "skills" / "beta").mkdir(parents=True)
        (tmp22_path / "skills" / "beta" / "SKILL.md").write_text(
            "---\nname: wrong-name\n---\nbody", encoding="utf-8"
        )
        (tmp22_path / "agents").mkdir(parents=True)
        agent_file_22 = tmp22_path / "agents" / "agent.md"
        agent_file_22.write_text(
            "---\nname: first-principles\n---\nbody", encoding="utf-8"
        )

        fixture_manifest = {"skills": ["./skills/does-not-exist/"]}
        report_22 = build_discovery_report(
            {"alpha", "beta"},
            True,
            agent_file_22,
            fixture_manifest,
            tmp22_path / "manifest.json",
            skills_dir=tmp22_path / "skills",
            plugin_dir=tmp22_path,
        )

        expected_keys_22 = {
            "discovered_skills",
            "discovered_skill_count",
            "discovered_agent",
            "manifest_path",
            "manifest_skills_field",
            "manifest_agents_field",
            "registered_skill_paths",
            "registered_agent_paths",
            "registration_source",
            "skill_name_verification",
            "agent_name_verification",
            "manifest_path_verification",
        }
        if set(report_22) != expected_keys_22:
            sys.stderr.write(
                "check-registration --self-test: FAIL — Control 22 report "
                f"shape (tempdir): key set {sorted(report_22)} != expected "
                f"{sorted(expected_keys_22)}\n"
            )
            sys.exit(1)

        round_tripped_22 = json.loads(json.dumps(report_22))
        if round_tripped_22 != report_22:
            sys.stderr.write(
                "check-registration --self-test: FAIL — Control 22 report "
                "shape (tempdir): JSON round-trip did not equal the "
                "original report\n"
            )
            sys.exit(1)

        # Phase 1 keys still carry their Phase 1 values — a regression guard
        # on the backward-compatible extension.
        if report_22["discovered_skills"] != ["alpha", "beta"]:
            sys.stderr.write(
                "check-registration --self-test: FAIL — Control 22 Phase 1 "
                f"regression: discovered_skills = {report_22['discovered_skills']!r}\n"
            )
            sys.exit(1)
        if report_22["discovered_skill_count"] != 2:
            sys.stderr.write(
                "check-registration --self-test: FAIL — Control 22 Phase 1 "
                f"regression: discovered_skill_count = "
                f"{report_22['discovered_skill_count']!r}\n"
            )
            sys.exit(1)
        if report_22["discovered_agent"] != {
            "name": AGENT_NAME,
            "present": True,
            "path": str(agent_file_22),
        }:
            sys.stderr.write(
                "check-registration --self-test: FAIL — Control 22 Phase 1 "
                f"regression: discovered_agent = {report_22['discovered_agent']!r}\n"
            )
            sys.exit(1)
        if report_22["registration_source"] != "manifest-paths":
            sys.stderr.write(
                "check-registration --self-test: FAIL — Control 22 Phase 1 "
                f"regression: registration_source = "
                f"{report_22['registration_source']!r}\n"
            )
            sys.exit(1)

        # Values axis: one skill matches True, one matches False.
        skill_matches_22 = {
            r["directory_name"]: r["matches"]
            for r in report_22["skill_name_verification"]
        }
        if skill_matches_22 != {"alpha": True, "beta": False}:
            sys.stderr.write(
                "check-registration --self-test: FAIL — Control 22 "
                f"skill_name_verification values: {skill_matches_22!r}, "
                "expected {'alpha': True, 'beta': False}\n"
            )
            sys.exit(1)

        # Manifest record resolved False (declared path does not exist).
        manifest_resolved_22 = [
            r["resolved"] for r in report_22["manifest_path_verification"]
        ]
        if manifest_resolved_22 != [False]:
            sys.stderr.write(
                "check-registration --self-test: FAIL — Control 22 "
                f"manifest_path_verification values: {manifest_resolved_22!r}, "
                "expected [False]\n"
            )
            sys.exit(1)

    # Control 23 — collect_verification_failures, in-memory literal reports
    # (D-04): a clean report returns []; a report carrying two mismatched
    # skills, a mismatched agent and one unresolved path returns EXACTLY
    # four lines, each naming its offending identifier. Anti-masking: the
    # count assertion is exact (4), not merely non-zero, so a
    # first-failure-only implementation fails this control.
    clean_report_23 = {
        "skill_name_verification": [
            {
                "directory_name": "alpha",
                "frontmatter_name": "alpha",
                "type": "skill",
                "matches": True,
            }
        ],
        "agent_name_verification": {
            "expected_name": "first-principles",
            "frontmatter_name": "first-principles",
            "type": "agent",
            "present": True,
            "matches": True,
        },
        "manifest_path_verification": [],
    }
    clean_failures_23 = collect_verification_failures(clean_report_23)
    if clean_failures_23 != []:
        sys.stderr.write(
            "check-registration --self-test: FAIL — Control 23 clean report: "
            f"expected [], got {clean_failures_23!r}\n"
        )
        sys.exit(1)

    failing_report_23 = {
        "skill_name_verification": [
            {
                "directory_name": "skill-one",
                "frontmatter_name": "wrong-one",
                "type": "skill",
                "matches": False,
            },
            {
                "directory_name": "skill-two",
                "frontmatter_name": None,
                "type": "skill",
                "matches": False,
            },
        ],
        "agent_name_verification": {
            "expected_name": "first-principles",
            "frontmatter_name": "wrong-agent-name",
            "type": "agent",
            "present": True,
            "matches": False,
        },
        "manifest_path_verification": [
            {
                "declared_path": "./skills/ghost/",
                "component_kind": "skill",
                "resolved": False,
            }
        ],
    }
    failing_failures_23 = collect_verification_failures(failing_report_23)
    if len(failing_failures_23) != 4:
        sys.stderr.write(
            "check-registration --self-test: FAIL — Control 23 anti-masking: "
            f"expected exactly 4 failure lines, got {len(failing_failures_23)}: "
            f"{failing_failures_23!r}\n"
        )
        sys.exit(1)
    joined_failures_23 = "\n".join(failing_failures_23)
    for identifier in (
        "skill-one",
        "wrong-one",
        "skill-two",
        "first-principles",
        "wrong-agent-name",
        "./skills/ghost/",
    ):
        if identifier not in joined_failures_23:
            sys.stderr.write(
                "check-registration --self-test: FAIL — Control 23: "
                f"identifier {identifier!r} missing from failure lines: "
                f"{failing_failures_23!r}\n"
            )
            sys.exit(1)

    # Control 24 — format_report_text rendering, in-memory (same two
    # literal reports as Control 23, extended with the nine Phase 1 keys
    # so format_report_text's earlier lines don't KeyError). The clean
    # report contains the section header and no "Failures:" block; the
    # failing report contains "Failures:" and every one of the four lines.
    # Anti-masking: without the negative half, a formatter that always
    # emits the Failures block would pass.
    base_fields_24 = {
        "discovered_skills": ["alpha"],
        "discovered_skill_count": 1,
        "discovered_agent": {
            "name": "first-principles",
            "present": True,
            "path": "/synthetic/agent.md",
        },
        "manifest_path": "/synthetic/manifest.json",
        "manifest_skills_field": None,
        "manifest_agents_field": None,
        "registered_skill_paths": [],
        "registered_agent_paths": [],
        "registration_source": "default-directory-auto-discovery",
    }
    clean_text_24 = format_report_text({**base_fields_24, **clean_report_23})
    if "Registration verification (REG-04/REG-05):" not in clean_text_24:
        sys.stderr.write(
            "check-registration --self-test: FAIL — Control 24 clean report: "
            "missing 'Registration verification (REG-04/REG-05):' header\n"
        )
        sys.exit(1)
    if "Failures:" in clean_text_24:
        sys.stderr.write(
            "check-registration --self-test: FAIL — Control 24 anti-masking: "
            "clean report text unexpectedly contains 'Failures:'\n"
        )
        sys.exit(1)

    failing_text_24 = format_report_text({**base_fields_24, **failing_report_23})
    if "Failures:" not in failing_text_24:
        sys.stderr.write(
            "check-registration --self-test: FAIL — Control 24 failing "
            "report: missing 'Failures:' block\n"
        )
        sys.exit(1)
    for failure_line in failing_failures_23:
        if failure_line not in failing_text_24:
            sys.stderr.write(
                "check-registration --self-test: FAIL — Control 24 failing "
                f"report: failure line missing from text: {failure_line!r}\n"
            )
            sys.exit(1)

    print(
        "check-registration --self-test: PASS (24 controls: discovery "
        "exclusions D-10/D-11/D-12, agent presence, manifest fail-fast "
        "D-09, absent-key tolerance D-07, report shape, frontmatter name "
        "extraction, skill/agent name verification, manifest-path "
        "resolution and containment, tempdir-fixture report values, "
        "failure collection accumulate-then-report, text rendering)"
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

    # Plan 02 (D-07): registration verification findings — name mismatches
    # and unresolved manifest-declared paths — gate exit 1 here. Environment
    # errors (manifest I/O/parse failures) already exited 2 above, inside
    # parse_manifest(), before we ever reached this point.
    verification_failures = collect_verification_failures(report)
    if verification_failures:
        # Print the full report first so the operator sees the whole summary
        # before the failure lines (REG-06 accumulate-then-report).
        if args.json:
            print(json.dumps(report, indent=2))
        else:
            print(format_report_text(report))
        for failure in verification_failures:
            sys.stderr.write(failure + "\n")
        sys.stderr.write(
            "check-registration: FAIL — "
            f"{len(verification_failures)} registration verification "
            "failure(s)\n"
        )
        sys.exit(1)

    skill_verifications = report["skill_name_verification"]
    skill_matched = sum(1 for r in skill_verifications if r["matches"])
    skill_total = len(skill_verifications)

    pass_line = (
        f"check-registration: PASS (discovered {len(skills)} skills, "
        "agent present, manifest parsed, "
        f"{skill_matched}/{skill_total} names verified)"
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
