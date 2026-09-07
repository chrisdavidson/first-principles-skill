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

import argparse
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

# Phase 21 (D-03/D-21-A): the static roster of stamp-source KINDS
# collect_stamps() walks — one glob pattern plus three fixed files. This is
# deliberately NOT a live count of discovered stamps (that would require the
# disk I/O collect_stamps() itself performs, which describe() must not do —
# D-03's "pure, no disk I/O" contract). len(_STAMP_SOURCE_KINDS) is what
# describe() publishes instead of a hand-typed "17" so a fifth source kind
# added to collect_stamps() without updating this roster is visible as a
# stale describe() rather than a silent drift.
#
# Phase 21-14 (CR-03): each value is a bare relpath or glob with no prose
# suffix — a "(glob)" annotation on the first entry made the value fail the
# vocabulary's own "file relpath" definition. That an entry is a glob is
# evident from the `*` in it. `registered_surfaces` in describe() publishes
# `sorted(_STAMP_SOURCE_KINDS)` directly (the surfaces the gate DECLARES IT
# READS), never `_EXCLUDED_GENERATED_GLOBS` (surfaces it deliberately does
# NOT read) — publishing the latter under that name stated the inverse of
# what the closed vocabulary defines (CR-03).
#
# Phase 21-17: `_stamp_roster_problems` below computes
# `missing = registered - walked` (a kind this roster DECLARES that the live
# walk never reaches — the roster over-claims) and
# `extra = walked - registered` (a kind the live walk REACHES that this
# roster does not declare — the roster under-claims). This is the same
# missing/extra vocabulary used by `check-agent.py`, `check-act-limb.py`,
# `check-selfaudit-scan.py`, `check-step0-live.py`, `check-step0-emulator.py`
# and `sync-content.py` — this file previously computed the reverse, which no
# sibling floor does.
_STAMP_SOURCE_KINDS: tuple[str, ...] = (
    "shared/skills/*/SKILL.md",
    "shared/spine/SKILL.meta.yml",
    ".claude-plugin/marketplace.json",
    "first-principles/.claude-plugin/plugin.json",
)

# The generated tree the docstring's "Scope" section explicitly excludes from
# scanning (DUAL-04 already gates its divergence from these shared/ sources).
# Not part of `registered_surfaces` (the vocabulary is closed by name; this is
# an exclusion, not a surface the gate reads) — stated in
# docs/gates/VERSION-01.md's hand-written narrative instead, and used below
# only by a self-test sanity control asserting these kinds are never walked.
_EXCLUDED_GENERATED_GLOBS: tuple[str, ...] = (
    "first-principles/agents/**",
    "first-principles/skills/**",
)

# Phase 21-14 (CR-03/CR-05): the kinds `collect_stamps()` actually walked on
# its most recent call, reset at entry and assigned at exit. Lets
# `self_test()` floor the published `_STAMP_SOURCE_KINDS` roster against
# reality without collect_stamps() changing its two-value return signature.
_LAST_WALKED_SOURCE_KINDS: list[str] = []


def _stamp_roster_problems(
    walked: list[str], registered: tuple[str, ...]
) -> list[str]:
    """Pure set-equality floor between what `collect_stamps()` actually
    walked and the published `_STAMP_SOURCE_KINDS` roster.

    `missing=` names a kind the roster declares that the live walk never
    reaches (the roster over-claims). `extra=` names a kind the live walk
    reaches that the roster does not declare (the roster under-claims — the
    CR-05 direction). Phase 21-17: this is the same missing/extra polarity
    used by `check-agent.py`, `check-act-limb.py`, `check-selfaudit-scan.py`,
    `check-step0-live.py`, `check-step0-emulator.py` and `sync-content.py`;
    this file previously computed the reverse of every sibling floor.
    """
    walked_set = set(walked)
    registered_set = set(registered)
    missing = registered_set - walked_set
    extra = walked_set - registered_set
    if missing or extra:
        return [
            f"stamp-source-kind roster/walked mismatch: "
            f"missing={sorted(missing)} extra={sorted(extra)}"
        ]
    return []


def _roster_arm_clauses(text: str) -> tuple[str, str]:
    """Split a `_stamp_roster_problems` mismatch message into its
    `missing=` and `extra=` clauses, mirroring the idiom in
    `check-agent.py`'s `_index_roster_problems` negative arm.

    Raises `ValueError` naming the offending text if either the `missing=`
    or the ` extra=` marker is absent, rather than silently returning the
    whole string as both clauses — a message-format change must surface as
    a loud failure here, not as both clauses collapsing to the same
    whole-message blindness this helper exists to remove.
    """
    if "missing=" not in text or " extra=" not in text:
        raise ValueError(
            f"_roster_arm_clauses: message lacks 'missing=' or ' extra=' "
            f"marker: {text!r}"
        )
    missing_clause = text.split("missing=", 1)[-1].split(" extra=", 1)[0]
    extra_clause = text.split("extra=", 1)[-1]
    return missing_clause, extra_clause


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

    Phase 21-14 (CR-03/CR-05): also records, into the module-level
    `_LAST_WALKED_SOURCE_KINDS`, which of the four walk sites below actually
    ran — reset to empty at entry, assigned to the final list at exit — so
    `self_test()` can floor `_STAMP_SOURCE_KINDS` against reality without
    changing this function's two-value return signature.
    """
    stamps: list[Stamp] = []
    problems: list[str] = []
    walked: list[str] = []

    module = sys.modules[__name__]
    module._LAST_WALKED_SOURCE_KINDS = []  # reset at entry

    def read(path: Path) -> str | None:
        try:
            return path.read_text(encoding="utf-8")
        except OSError as exc:
            problems.append(f"{path}: unreadable: {exc}")
            return None

    # Skill sources -- globbed, never counted against a constant. The site
    # itself always runs (the glob call and loop are unconditional), so the
    # kind is recorded regardless of match count.
    skill_kind = "shared/skills/*/SKILL.md"
    walked.append(skill_kind)
    for skill in sorted((root / "shared" / "skills").glob("*/SKILL.md")):
        label = str(skill.relative_to(root))
        text = read(skill)
        if text is None:
            continue
        value = _md_frontmatter(text, label, problems)
        if value is not None:
            stamps.append(Stamp(label, value))

    # Spine metadata -- plain YAML, no frontmatter fences.
    spine_kind = "shared/spine/SKILL.meta.yml"
    spine = root / "shared" / "spine" / "SKILL.meta.yml"
    if spine.exists():
        walked.append(spine_kind)
        text = read(spine)
        if text is not None:
            label = str(spine.relative_to(root))
            value = _yaml_stamp(text, label, problems)
            if value is not None:
                stamps.append(Stamp(label, value))

    # Manifests. Both are hand-maintained: sync-content.py explicitly does NOT
    # generate first-principles/.claude-plugin/plugin.json.
    for manifest, manifest_kind in (
        (root / ".claude-plugin" / "marketplace.json", ".claude-plugin/marketplace.json"),
        (
            root / "first-principles" / ".claude-plugin" / "plugin.json",
            "first-principles/.claude-plugin/plugin.json",
        ),
    ):
        if not manifest.exists():
            continue
        walked.append(manifest_kind)
        text = read(manifest)
        if text is not None:
            stamps.extend(_json_stamps(text, str(manifest.relative_to(root)), problems))

    module._LAST_WALKED_SOURCE_KINDS = walked  # assigned at exit
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


def describe() -> dict:
    """Phase 21 (D-03): pure, gate-agnostic self-description backing
    VERSION-01.

    Reads module-level constants only — no disk I/O, no argv, no subprocess.
    The stamp COUNT this gate discovers at runtime is inherently a property
    of the live tree (collect_stamps() globs it), not a describe()-safe
    constant; what IS describable without I/O is the fixed roster of source
    KINDS it is configured to walk (_STAMP_SOURCE_KINDS).

    Phase 21-14 (CR-03): `registered_surfaces` publishes the surfaces this
    gate DECLARES IT READS — `_STAMP_SOURCE_KINDS`, floored against
    `collect_stamps()`'s own walk sites by `self_test()`. It previously
    published `_EXCLUDED_GENERATED_GLOBS` (the surfaces the gate explicitly
    does NOT read) under this name, stating the closed vocabulary's inverse.
    The exclusion is real and still true; it belongs in
    docs/gates/VERSION-01.md's hand-written narrative, not in this field.
    """
    return {
        "derived_counts": {"stamp_source_kind_count": len(_STAMP_SOURCE_KINDS)},
        "registered_surfaces": sorted(_STAMP_SOURCE_KINDS),
    }


def self_test() -> int:
    """Fixture-driven fault injection.

    Every check accumulates into `failures` and the function returns an exit
    code -- deliberately no bare `assert`, which `python -O` strips, turning a
    self-test into a vacuous pass.
    """
    failures: list[str] = []
    module = sys.modules[__name__]

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

        # (h) Kind roster/walked floor, positive (Phase 21-14, CR-03/CR-05):
        # published _STAMP_SOURCE_KINDS must equal what collect_stamps()
        # actually walks on the live tree, in both directions.
        collect_stamps(REPO_ROOT)
        kind_problems = _stamp_roster_problems(
            module._LAST_WALKED_SOURCE_KINDS, module._STAMP_SOURCE_KINDS
        )
        expect("kind-roster-matches-walked", not kind_problems, f"({kind_problems})")

        # (i) Negative arm, over-claim direction via fabricated roster entry
        # (CR-05/21-17): a roster entry that nothing walks is DECLARED but
        # never REACHED, so it must land in the MISSING clause and NOT in
        # the EXTRA clause.
        original_kinds = module._STAMP_SOURCE_KINDS
        try:
            module._STAMP_SOURCE_KINDS = original_kinds + ("fixture-fabricated-kind",)
            collect_stamps(REPO_ROOT)
            kind_problems = _stamp_roster_problems(
                module._LAST_WALKED_SOURCE_KINDS, module._STAMP_SOURCE_KINDS
            )
            joined = " ".join(kind_problems)
            missing_clause, extra_clause = (
                _roster_arm_clauses(joined) if kind_problems else ("", "")
            )
            expect(
                "kind-roster-overclaim-fabricated",
                bool(kind_problems)
                and "fixture-fabricated-kind" in missing_clause
                and "fixture-fabricated-kind" not in extra_clause,
                f"({kind_problems})",
            )
        finally:
            module._STAMP_SOURCE_KINDS = original_kinds

        # (j) Negative arm, over-claim direction via fixture tree (CR-05/
        # 21-17): a tree that lacks shared/spine/SKILL.meta.yml means the
        # walk never REACHES it while the roster still DECLARES it — an
        # over-claim, not an under-claim (this arm was misnamed before this
        # plan). Must land in the MISSING clause and NOT in the EXTRA
        # clause.
        missing_spine = base / "missing-spine"
        _build_fixture(missing_spine, skill_stamps=['"1.0.0"'], spine_stamp=None)
        collect_stamps(missing_spine)
        kind_problems = _stamp_roster_problems(
            module._LAST_WALKED_SOURCE_KINDS, module._STAMP_SOURCE_KINDS
        )
        joined = " ".join(kind_problems)
        missing_clause, extra_clause = (
            _roster_arm_clauses(joined) if kind_problems else ("", "")
        )
        expect(
            "kind-roster-overclaim-fixture",
            bool(kind_problems)
            and "shared/spine/SKILL.meta.yml" in missing_clause
            and "shared/spine/SKILL.meta.yml" not in extra_clause,
            f"({kind_problems})",
        )

        # (j') Negative arm, GENUINE under-claim direction (21-17): shrink
        # the roster while walking the REAL repo tree, so the walk still
        # REACHES a kind the roster no longer DECLARES. Must land in the
        # EXTRA clause and NOT in the MISSING clause. This is the permanent
        # form of the one-off scratch-copy demonstration recorded in
        # 21-14-SUMMARY.md — the direction that had no registered control
        # before this plan.
        original_kinds = module._STAMP_SOURCE_KINDS
        try:
            module._STAMP_SOURCE_KINDS = tuple(
                k for k in original_kinds if k != "shared/spine/SKILL.meta.yml"
            )
            collect_stamps(REPO_ROOT)
            kind_problems = _stamp_roster_problems(
                module._LAST_WALKED_SOURCE_KINDS, module._STAMP_SOURCE_KINDS
            )
            joined = " ".join(kind_problems)
            missing_clause, extra_clause = (
                _roster_arm_clauses(joined) if kind_problems else ("", "")
            )
            expect(
                "kind-roster-underclaim-detected",
                bool(kind_problems)
                and "shared/spine/SKILL.meta.yml" in extra_clause
                and "shared/spine/SKILL.meta.yml" not in missing_clause,
                f"({kind_problems})",
            )
        finally:
            module._STAMP_SOURCE_KINDS = original_kinds

        # Message-shape guard control (21-17): _roster_arm_clauses must
        # raise ValueError on a message missing the ' extra=' marker,
        # proving the guard is live rather than decorative.
        try:
            _roster_arm_clauses(
                "stamp-source-kind roster/walked mismatch: missing=[]"
            )
            expect(
                "kind-roster-arm-shape-guard",
                False,
                "(_roster_arm_clauses accepted a message lacking ' extra=')",
            )
        except ValueError:
            expect("kind-roster-arm-shape-guard", True)

        # (k) Sanity control: the excluded generated-tree globs must never
        # appear among what collect_stamps() walked — they are declared
        # excluded, not merely absent from the roster by omission.
        excluded_walked = [
            k
            for k in module._LAST_WALKED_SOURCE_KINDS
            if k in module._EXCLUDED_GENERATED_GLOBS
        ]
        expect("excluded-globs-never-walked", not excluded_walked, f"({excluded_walked})")

    # (l) describe() consistency control (Phase 21, D-03): mutate a copy of
    # _STAMP_SOURCE_KINDS and confirm describe()'s emitted count moves with
    # it — proving the field is a real derivation, not a hand-typed literal.
    original_kinds = module._STAMP_SOURCE_KINDS
    try:
        before = describe()["derived_counts"]["stamp_source_kind_count"]
        module._STAMP_SOURCE_KINDS = original_kinds + ("fixture-extra-source",)
        after = describe()["derived_counts"]["stamp_source_kind_count"]
        expect(
            "describe-consistency",
            after == before + 1,
            f"(before={before}, after mutation={after}, expected={before + 1})",
        )
    finally:
        module._STAMP_SOURCE_KINDS = original_kinds

    # (m) argparse dispatch control (Phase 21-14, WR-12): a mistyped flag
    # must not fall through to the live scan and silently exit 0. Before
    # this control, `--decribe` fell through to the argv-substring dispatch
    # and ran the live scan, exiting 0 for a check that was never requested.
    try:
        main(["--decribe"])
        expect(
            "typo-flag-rejected",
            False,
            "(main(['--decribe']) returned normally instead of raising SystemExit)",
        )
    except SystemExit as exc:
        expect(
            "typo-flag-rejected",
            exc.code not in (0, None),
            f"(SystemExit code={exc.code!r}, expected non-zero)",
        )

    if failures:
        sys.stderr.write(
            f"check-version-stamps --self-test: FAIL "
            f"({len(failures)} fixture(s): {', '.join(failures)})\n"
        )
        return 1

    print("check-version-stamps --self-test: PASS (8 fixture trees, 16 named assertions)")
    return 0


def _build_arg_parser() -> argparse.ArgumentParser:
    """Phase 21-14 (WR-12): argparse with a mutually exclusive group, replacing
    the `if "--flag" in sys.argv[1:]` substring dispatch. That dispatch let a
    mistyped flag (e.g. `--decribe`) fall through to the live scan silently —
    a CI step or battery line with a typo reported PASS for a check it never
    ran.
    """
    parser = argparse.ArgumentParser(
        prog="check-version-stamps.py",
        description=(
            "VERSION-01 gate: every hand-maintained version stamp carries "
            "the same value."
        ),
    )
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument(
        "--self-test", action="store_true", help="Run the fixture-driven self-test."
    )
    mode.add_argument(
        "--describe",
        action="store_true",
        help="Emit a JSON self-description and exit.",
    )
    return parser


def main(argv: list[str] | None = None) -> None:
    """Run the check-version-stamps CLI.

    `argv` defaults to None, which makes argparse fall back to `sys.argv[1:]`
    exactly as before this parameter existed. The parameter exists so
    `self_test()`'s typo-dispatch control can drive `main()` itself against a
    fixture argv (mirrors `sync-content.py`'s `main(argv=...)` precedent,
    Phase 152 WR-01).
    """
    args = _build_arg_parser().parse_args(argv)

    if args.describe:
        print(json.dumps(describe(), indent=2, sort_keys=True))
        return

    _require_python_version()
    _require_pyyaml()

    if args.self_test:
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
