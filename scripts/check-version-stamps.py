#!/usr/bin/env python3
# /// script
# requires-python = ">=3.12"
# dependencies = ["pyyaml>=6.0"]
# ///
"""VERSION-01 gate: every hand-maintained version stamp carries the same value.

Why this gate exists
--------------------
Plugin installs are version-gated, not content-gated: a body edit that ships
without a version bump never reaches an installed session, because the install
cache keys on the version string. CHANGELOG.md's preamble therefore states that
every release bumps all stamps *in lockstep*.

Nothing enforced that. `sync-content.py` copies `metadata.version` through
per-file (it re-quotes the value, it does not propagate one source of truth to
the rest), and the documented "version string invariant" is a *format* rule
(double-quoted YAML scalar), not an equality rule. A single missed stamp was
enough to leave the v8.14 update path inert while every other gate stayed green.

This gate closes that hole: it discovers every hand-maintained stamp and asserts
they are all equal.

Discovery is by glob, never by a hardcoded count. A newly added skill is picked
up automatically; a new skill that forgets its stamp fails on presence, not on a
magic number. The count is reported, not asserted -- asserting it would recreate
the very drift this gate exists to catch.

Scope
-----
Hand-maintained stamps only:

  * shared/skills/<slug>/SKILL.md      -- YAML frontmatter, metadata.version
  * shared/spine/SKILL.meta.yml        -- YAML, metadata.version
  * .claude-plugin/marketplace.json    -- plugins[*].version
  * first-principles/.claude-plugin/plugin.json  -- version

The generated tree (first-principles/agents/**, first-principles/skills/**) is
NOT scanned: those stamps are produced by `sync-content.py` from the `shared/`
sources above, and DUAL-04 (`sync-content.py --check`) already fails on any
divergence between them. Scanning them here would double-gate one invariant and
report a misleading stamp count.

Usage:
    python3 scripts/check-version-stamps.py
    python3 scripts/check-version-stamps.py --self-test

Exit codes:
    0  all discovered stamps agree (or --self-test fixtures all behaved)
    1  stamps diverge, a stamp is missing/malformed, or a self-test fixture failed
    2  environment error (Python <3.12, PyYAML missing, no stamp sources found)
"""

from __future__ import annotations

import json
import re
import sys
import tempfile
from dataclasses import dataclass
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]

# The documented invariant: a YAML version stamp is a DOUBLE-QUOTED scalar.
# Bare `version: 8.17` parses as a float and silently stops matching the string
# the install cache compares against; bare `version: 8.17.1` happens to parse as
# a string, which makes the failure mode intermittent and therefore worse.
_YAML_STAMP_RE = re.compile(r'^\s*version:\s*(?P<raw>\S.*?)\s*$', re.MULTILINE)
_FENCE_RE = re.compile(r"^---\s*$", re.MULTILINE)


@dataclass(frozen=True)
class Stamp:
    """One discovered version stamp."""

    source: str  # repo-relative path, plus a locator for multi-stamp files
    value: str


def _require_python_version() -> None:
    if sys.version_info < (3, 12):
        sys.stderr.write(
            f"scripts/check-version-stamps.py requires Python >=3.12 "
            f"(running {sys.version_info.major}.{sys.version_info.minor}).\n"
        )
        sys.exit(2)


def _require_pyyaml() -> None:
    try:
        import yaml  # noqa: F401
    except ImportError:
        sys.stderr.write(
            "scripts/check-version-stamps.py needs PyYAML.\n"
            "  Easiest:  uv run scripts/check-version-stamps.py\n"
            "  Or:       pip install --user 'pyyaml>=6.0'  &&  "
            "python3 scripts/check-version-stamps.py\n"
        )
        sys.exit(2)


def _yaml_stamp(text: str, label: str, problems: list[str]) -> str | None:
    """Extract and format-check a `version:` stamp from YAML text.

    Returns the stamp value, or None (recording a problem) when the stamp is
    absent or not a double-quoted scalar.
    """
    matches = _YAML_STAMP_RE.findall(text)
    if not matches:
        problems.append(f"{label}: no `version:` stamp found")
        return None
    if len(matches) > 1:
        problems.append(
            f"{label}: {len(matches)} `version:` stamps in one file "
            f"(expected exactly 1): {matches}"
        )
        return None
    raw = matches[0]
    if not (len(raw) >= 2 and raw.startswith('"') and raw.endswith('"')):
        problems.append(
            f"{label}: version stamp {raw!r} is not a double-quoted string "
            f'(write version: "x.y.z" -- an unquoted stamp can parse as a float)'
        )
        return None
    return raw[1:-1]


def _md_frontmatter(text: str, label: str, problems: list[str]) -> str | None:
    """Extract the YAML frontmatter block of a Markdown file, then stamp it."""
    parts = _FENCE_RE.split(text, maxsplit=2)
    if len(parts) < 3:
        problems.append(f"{label}: missing closing frontmatter fence")
        return None
    return _yaml_stamp(parts[1], label, problems)


def _json_stamps(text: str, label: str, problems: list[str]) -> list[Stamp]:
    """Extract version stamps from a plugin or marketplace manifest."""
    try:
        data = json.loads(text)
    except json.JSONDecodeError as exc:
        problems.append(f"{label}: malformed JSON: {exc}")
        return []
    if not isinstance(data, dict):
        problems.append(f"{label}: top level is not a JSON object")
        return []

    found: list[Stamp] = []
    if isinstance(data.get("version"), str):
        found.append(Stamp(label, data["version"]))
    for i, plugin in enumerate(data.get("plugins", []) or []):
        if isinstance(plugin, dict) and isinstance(plugin.get("version"), str):
            found.append(Stamp(f"{label}#plugins[{i}]", plugin["version"]))

    if not found:
        problems.append(f"{label}: no string `version` field found")
    return found


def collect_stamps(root: Path) -> tuple[list[Stamp], list[str]]:
    """Discover every hand-maintained version stamp under `root`.

    Returns (stamps, problems). A problem is a per-file defect (missing stamp,
    unquoted stamp, unreadable file); divergence between files is judged by the
    caller, which needs the whole set to report it usefully.
    """
    stamps: list[Stamp] = []
    problems: list[str] = []

    def read(path: Path) -> str | None:
        try:
            return path.read_text(encoding="utf-8")
        except OSError as exc:
            problems.append(f"{path}: unreadable: {exc}")
            return None

    # Skill sources -- globbed, never counted against a constant.
    for skill in sorted((root / "shared" / "skills").glob("*/SKILL.md")):
        label = str(skill.relative_to(root))
        text = read(skill)
        if text is None:
            continue
        value = _md_frontmatter(text, label, problems)
        if value is not None:
            stamps.append(Stamp(label, value))

    # Spine metadata -- plain YAML, no frontmatter fences.
    spine = root / "shared" / "spine" / "SKILL.meta.yml"
    if spine.exists():
        text = read(spine)
        if text is not None:
            label = str(spine.relative_to(root))
            value = _yaml_stamp(text, label, problems)
            if value is not None:
                stamps.append(Stamp(label, value))

    # Manifests. Both are hand-maintained: sync-content.py explicitly does NOT
    # generate first-principles/.claude-plugin/plugin.json.
    for manifest in (
        root / ".claude-plugin" / "marketplace.json",
        root / "first-principles" / ".claude-plugin" / "plugin.json",
    ):
        if not manifest.exists():
            continue
        text = read(manifest)
        if text is not None:
            stamps.extend(_json_stamps(text, str(manifest.relative_to(root)), problems))

    return stamps, problems


def check(root: Path) -> tuple[bool, list[str], list[Stamp]]:
    """Run the gate against `root`. Returns (ok, messages, stamps)."""
    stamps, problems = collect_stamps(root)

    if not stamps and not problems:
        return False, [f"no version stamps found under {root} (vacuous run)"], stamps

    values = {s.value for s in stamps}
    if len(values) > 1:
        by_value: dict[str, list[str]] = {}
        for s in stamps:
            by_value.setdefault(s.value, []).append(s.source)
        detail = [f"version stamps diverge across {len(stamps)} source(s):"]
        for value in sorted(by_value):
            detail.append(f"  {value!r}  <- {len(by_value[value])} file(s)")
            detail.extend(f"      {src}" for src in sorted(by_value[value]))
        problems.extend(detail)

    return (not problems), problems, stamps


# ---------------------------------------------------------------------------
# Self-test
# ---------------------------------------------------------------------------

_SKILL_TEMPLATE = """---
name: {slug}
description: Fixture skill for the VERSION-01 self-test.
metadata:
  version: {stamp}
---

# {slug}
"""

_SPINE_TEMPLATE = """name: first-principles
description: Fixture spine.
metadata:
  version: {stamp}
"""


def _build_fixture(
    root: Path,
    *,
    skill_stamps: list[str],
    spine_stamp: str | None = '"1.0.0"',
    marketplace_stamp: str | None = "1.0.0",
    plugin_stamp: str | None = "1.0.0",
) -> None:
    """Materialise a synthetic repo whose stamp layout mirrors the real one."""
    for i, stamp in enumerate(skill_stamps):
        slug = f"fixture-skill-{i}"
        d = root / "shared" / "skills" / slug
        d.mkdir(parents=True, exist_ok=True)
        (d / "SKILL.md").write_text(
            _SKILL_TEMPLATE.format(slug=slug, stamp=stamp), encoding="utf-8"
        )

    if spine_stamp is not None:
        d = root / "shared" / "spine"
        d.mkdir(parents=True, exist_ok=True)
        (d / "SKILL.meta.yml").write_text(
            _SPINE_TEMPLATE.format(stamp=spine_stamp), encoding="utf-8"
        )

    if marketplace_stamp is not None:
        d = root / ".claude-plugin"
        d.mkdir(parents=True, exist_ok=True)
        (d / "marketplace.json").write_text(
            json.dumps({"name": "fx", "plugins": [{"name": "fx", "version": marketplace_stamp}]}),
            encoding="utf-8",
        )

    if plugin_stamp is not None:
        d = root / "first-principles" / ".claude-plugin"
        d.mkdir(parents=True, exist_ok=True)
        (d / "plugin.json").write_text(
            json.dumps({"name": "fx", "version": plugin_stamp}), encoding="utf-8"
        )


def self_test() -> int:
    """Fixture-driven fault injection.

    Every check accumulates into `failures` and the function returns an exit
    code -- deliberately no bare `assert`, which `python -O` strips, turning a
    self-test into a vacuous pass.
    """
    failures: list[str] = []

    def expect(name: str, condition: bool, detail: str = "") -> None:
        if condition:
            print(f"check-version-stamps --self-test: {name} PASS")
        else:
            msg = f"check-version-stamps --self-test: {name} FAIL {detail}".rstrip()
            print(msg)
            failures.append(name)

    with tempfile.TemporaryDirectory(prefix="version-stamps-selftest-") as tmp:
        base = Path(tmp)

        # (a) Positive control: every stamp agrees.
        clean = base / "clean"
        _build_fixture(clean, skill_stamps=['"1.0.0"'] * 3)
        ok, problems, stamps = check(clean)
        expect("clean-agrees", ok, f"(problems={problems})")
        expect(
            "clean-discovers-all",
            len(stamps) == 6,
            f"(expected 6: 3 skills + spine + marketplace + plugin; got {len(stamps)})",
        )

        # (b) Fault injection: one skill stamp diverges. This is the exact v8.14
        #     failure mode -- everything green except the one file that matters.
        drifted = base / "drifted"
        _build_fixture(drifted, skill_stamps=['"1.0.0"', '"1.0.0"', '"0.9.9"'])
        ok, problems, _ = check(drifted)
        expect("divergent-skill-detected", not ok)
        expect(
            "divergent-skill-names-both-values",
            any("0.9.9" in p for p in problems) and any("1.0.0" in p for p in problems),
            f"(problems={problems})",
        )

        # (c) Fault injection: a manifest lags behind the sources.
        lagging = base / "lagging"
        _build_fixture(lagging, skill_stamps=['"1.0.0"'] * 2, plugin_stamp="0.9.9")
        ok, _, _ = check(lagging)
        expect("divergent-manifest-detected", not ok)

        # (d) Fault injection: a skill ships with no stamp at all. Presence, not
        #     count, is what catches this -- so a 15th skill cannot slip through.
        missing = base / "missing"
        _build_fixture(missing, skill_stamps=['"1.0.0"'])
        d = missing / "shared" / "skills" / "no-stamp"
        d.mkdir(parents=True, exist_ok=True)
        (d / "SKILL.md").write_text(
            "---\nname: no-stamp\ndescription: x\n---\n\n# no-stamp\n", encoding="utf-8"
        )
        ok, problems, _ = check(missing)
        expect("missing-stamp-detected", not ok)
        expect(
            "missing-stamp-names-file",
            any("no-stamp" in p for p in problems),
            f"(problems={problems})",
        )

        # (e) Fault injection: the documented format invariant. An unquoted
        #     stamp is what turns `8.17` into a float and breaks the compare.
        unquoted = base / "unquoted"
        _build_fixture(unquoted, skill_stamps=['"1.0.0"', "1.0"])
        ok, problems, _ = check(unquoted)
        expect("unquoted-stamp-detected", not ok)
        expect(
            "unquoted-stamp-explains",
            any("double-quoted" in p for p in problems),
            f"(problems={problems})",
        )

        # (f) Vacuity guard: an empty tree must FAIL, not trivially pass. Without
        #     this, a mis-rooted invocation would report GREEN forever.
        empty = base / "empty"
        empty.mkdir(parents=True, exist_ok=True)
        ok, problems, stamps = check(empty)
        expect("empty-tree-is-not-vacuously-clean", not ok and not stamps)

        # (g) Counter-check: the detector is not simply always-failing. (a)
        #     already passed, so a FAIL here would mean the fixtures, not the
        #     gate, decide the verdict.
        ok_again, _, _ = check(clean)
        expect("detector-not-always-failing", ok_again)

    if failures:
        sys.stderr.write(
            f"check-version-stamps --self-test: FAIL "
            f"({len(failures)} fixture(s): {', '.join(failures)})\n"
        )
        return 1

    print("check-version-stamps --self-test: PASS (7 fixture trees, 11 named assertions)")
    return 0


def main() -> None:
    _require_python_version()
    _require_pyyaml()

    if "--self-test" in sys.argv[1:]:
        sys.exit(self_test())

    ok, problems, stamps = check(REPO_ROOT)

    if not stamps and not problems:
        sys.stderr.write(
            f"check-version-stamps: no stamp sources found under {REPO_ROOT} "
            f"(is this the repo root?)\n"
        )
        sys.exit(2)

    if not ok:
        for line in problems:
            sys.stderr.write(f"check-version-stamps: {line}\n")
        sys.stderr.write("check-version-stamps: FAIL\n")
        sys.exit(1)

    value = stamps[0].value
    print(f"check-version-stamps: {len(stamps)} stamps, all {value!r}")
    for s in sorted(stamps, key=lambda s: s.source):
        print(f"  {s.source}")
    print("check-version-stamps: PASS")


if __name__ == "__main__":
    main()
