#!/usr/bin/env python3
# /// script
# requires-python = ">=3.12"
# ///
"""CONF-SURFACE: generate the CI-gate claim surface from --describe emissions.

Hand-transcribed gate documentation was the direct cause of a substantial
share of review findings across Phases 13-15 (see
`scripts/_gate_registry.py`'s own module docstring for the measured figure)
— every branch count, surface list and disclosed bound was copied by hand
into up to five places with nothing checking they agreed. This script is
the fix's compute+render layer (D-21-B): it subprocess-invokes every
script-backed `scripts/_gate_registry.py` entry's `--describe` leg, applies
the registry's own D-01/D-04 floors plus a frozen-path disjointness floor
over its own write set, and regenerates `CLAUDE.md`'s and
`docs/ARCHITECTURE.md`'s gate tables, `docs/TESTING.md`'s per-gate index,
and every `docs/gates/<GATE-ID>.md` detail page from harvested facts. It
also carries CONF-13's standing scanner (`run_literal_scan()`) — the
`--check` leg that drives this file's own registration, CONF-SURFACE, as a
battery gate, CI job and pre-commit hook (plan 21-11, D-21-C).

This module does not import any of the scripts it describes as gates (D-21-A
— it shells out to their `--describe` leg exactly as
`scripts/check-firewall-battery.sh` already does), and it perturbs none of
the three CONTRACT-06 sha256 pins (`_chain_block_well_formed`,
`_conclusion_claims`, `_slice_sections`) — it neither imports nor edits the
file that carries them.

Usage:
    python3 scripts/gen-gate-docs.py --write
    python3 scripts/gen-gate-docs.py --check
    python3 scripts/gen-gate-docs.py --self-test
    python3 scripts/gen-gate-docs.py --describe

Exit codes:
    0  write succeeded / check found no drift / self-test PASS
    1  check found drift, or a harvest/floor problem, or self-test FAIL
    2  check found a non-deterministic generate_all() (pass-1 != pass-2)
"""

from __future__ import annotations

import argparse
import ast
import contextlib
import difflib
import fnmatch
import hashlib
import importlib.util
import inspect
import io
import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import NamedTuple

REPO_ROOT: Path = Path(__file__).resolve().parents[1]
BATTERY_PATH: Path = REPO_ROOT / "scripts" / "check-firewall-battery.sh"

# ---------------------------------------------------------------------------
# Load _gate_registry.py via importlib (same MUST-pre-register-in-sys.modules
# discipline as scripts/check-step0-live.py's _battery_core load — Python
# 3.13+ @dataclass(frozen=True) compatibility, "Pitfall 3").
# ---------------------------------------------------------------------------

_REGISTRY_PATH: Path = Path(__file__).resolve().parent / "_gate_registry.py"
_registry_spec = importlib.util.spec_from_file_location("_gate_registry", _REGISTRY_PATH)
_gate_registry = importlib.util.module_from_spec(_registry_spec)  # type: ignore[arg-type]
sys.modules["_gate_registry"] = _gate_registry  # MUST precede exec_module
_registry_spec.loader.exec_module(_gate_registry)  # type: ignore[union-attr]

# `_this_module` is used by self-test controls that need to monkeypatch a
# module-level function (`generate_all`) and restore it afterwards — the
# exact idiom `scripts/sync-content.py`'s own `--self-test` control (l) uses
# for `GENERATED_TARGET_COUNT`.
_this_module = sys.modules[__name__]


# ---------------------------------------------------------------------------
# Stamping vocabulary (adapts scripts/sync-content.py:174-175's existing
# phrasing rather than inventing a second one).
# ---------------------------------------------------------------------------

GENERATED_MARKER = (
    "<!-- GENERATED — DO NOT EDIT. Source: {source}. "
    "Regenerate via: scripts/gen-gate-docs.py --write. -->"
)
GENERATED_END_MARKER = "<!-- END GENERATED -->"


# ---------------------------------------------------------------------------
# harvest(): subprocess-invoke every script-backed entry's --describe leg
# ---------------------------------------------------------------------------


class _HarvestEntry(NamedTuple):
    """The minimal shape harvest() needs from a registry entry — a `script`
    relpath (or, for self-test fixtures, an absolute temp-file path;
    `REPO_ROOT / script` returns `script` unchanged when it is already
    absolute, so both forms work through the same join). Duck-typed rather
    than `_gate_registry.GateEntry` itself so self-test fixtures do not have
    to construct every one of that frozen dataclass's unrelated fields."""

    script: str


def harvest(entries) -> tuple[dict[str, dict], list[str]]:
    """Subprocess-invoke `--describe` for every distinct script-backed entry.

    Returns `(by_script_relpath, problems)`. Never raises on a script that
    crashes, cannot be invoked, or emits malformed JSON (T-21-06-03): the
    script is named in `problems` and harvesting continues to the next one.
    `entries` may be `_gate_registry.GateEntry` instances or any object
    exposing a `.script` attribute (see `_HarvestEntry`); entries with a
    `None`/falsy `script` are skipped (nothing to invoke).
    """
    by_script: dict[str, dict] = {}
    problems: list[str] = []
    scripts = sorted({e.script for e in entries if e.script})
    for script in scripts:
        script_path = REPO_ROOT / script
        try:
            proc = subprocess.run(
                [sys.executable, str(script_path), "--describe"],
                capture_output=True,
                text=True,
                timeout=120,
            )
        except OSError as exc:
            problems.append(f"harvest: {script} could not be invoked: {exc!r}")
            continue
        if proc.returncode != 0:
            first_stderr_line = next(iter(proc.stderr.splitlines()), "")
            problems.append(
                f"harvest: {script} --describe exited {proc.returncode}: "
                f"{first_stderr_line}"
            )
            continue
        try:
            blob = json.loads(proc.stdout)
        except json.JSONDecodeError as exc:
            problems.append(
                f"harvest: {script} --describe emitted malformed JSON: {exc}"
            )
            continue
        by_script[script] = blob
    return by_script, problems


def _expected_harvest_scripts() -> frozenset[str]:
    """Script relpaths harvest() is expected to reach on a live run: every
    script-backed `ENTRIES` member, excluding the anticipatory ones
    (`CONF-SURFACE`, D-21-C) that are not wired into the battery yet —
    mirrors `_gate_registry._registry_entry_ids()`'s own exclusion so this
    vacuity floor and the D-01 id floor agree about what "documented"
    means."""
    return frozenset(
        e.script
        for e in _gate_registry.ENTRIES
        if e.script and e.key not in _gate_registry._ANTICIPATORY_KEYS
    )


# ---------------------------------------------------------------------------
# GAP A item 3 (plan 21-19): a standing, registry-derived census of the
# defective roster-arm shape that wave 15 introduced and plans 21-17/21-18
# removed from the six scripts they touched — a synthetic id tested against
# the WHOLE joined roster-mismatch message rather than against its extracted
# `missing=`/`extra=` clause. Nothing before this plan stopped a seventh
# script, or a later edit to any of the six, from reintroducing it; this
# census makes that unreintroducible across every script-backed registry
# entry, not just the six this phase touched (21-18-SUMMARY.md
# falsification 7's own reopening demonstration).
# ---------------------------------------------------------------------------

# Wave-15 shape: a synthetic fixture id (always literally the word
# "synthetic" plus a hyphen and a single lowercase letter, across every
# fixture in this repo) tested with `not in` against a plain identifier that
# does NOT end in `_clause`. The FIXED shape splits the id into its own
# clause first, so the fixed identifier always ends in `_clause` and must
# not match. (Deliberately not spelled out here as a literal quoted example
# — this file is itself one of the 22 population members the live control
# below scans, and a literal example in this comment would self-match.)
_ROSTER_ARM_SYNTHETIC_MEMBERSHIP_RE = re.compile(
    r'"synthetic-[a-z]"\s+not in\s+([A-Za-z_][A-Za-z0-9_]*)\b'
)

# check-version-stamps.py's pre-21-17 shape: testing whether the clause
# marker text itself (the word missing followed by an equals sign, or the
# word extra followed by an equals sign) appears anywhere in the joined
# message, via `in` rather than `not in` — true of every roster-mismatch
# message regardless of which clause anything landed in. Always defective;
# there is no fixed form of this exact shape (the fix is the clause split,
# not a renamed identifier). Same self-match note as above applies.
_ROSTER_ARM_CLAUSE_MARKER_RE = re.compile(
    r'"(?:missing=|extra=)"\s+in\s+([A-Za-z_][A-Za-z0-9_]*)\b'
)


def _roster_arm_census_sources() -> dict[str, str]:
    """Build the live population for `roster_arm_shape_census_problems()`'s
    default `sources=None` path: reads every `_expected_harvest_scripts()`
    relpath from `REPO_ROOT`. Exposed separately (not inlined into the scan
    function) so the anti-vacuity floor can assert the read count
    independently of the scan logic itself."""
    return {
        relpath: (REPO_ROOT / relpath).read_text(encoding="utf-8")
        for relpath in sorted(_expected_harvest_scripts())
    }


def roster_arm_shape_census_problems(
    sources: dict[str, str] | None = None,
) -> list[str]:
    """Scan every population member's source text for the two defective
    roster-arm shapes above. `sources` lets the vacuity control drive this
    function against synthetic text without touching disk (mirrors
    `literal_ledger_ratchet_problems(ledger=...)`'s parameter shape); the
    default `None` reads the real population via
    `_roster_arm_census_sources()`. An empty population is itself a
    finding — a census that silently scans nothing must fail, not pass.

    Scoped to `--self-test` only: this is a property of source SHAPE, not
    of generated-output drift, and `--self-test` already runs in the
    battery, in CI, and in both pre-commit hooks. Not wired into
    `cmd_check()`.
    """
    if sources is None:
        sources = _roster_arm_census_sources()

    if not sources:
        return [
            "roster-arm-shape-census: population is empty — the census "
            "cannot scan nothing"
        ]

    problems: list[str] = []
    for relpath in sorted(sources):
        lines = sources[relpath].splitlines()
        for lineno, line in enumerate(lines, start=1):
            for match in _ROSTER_ARM_SYNTHETIC_MEMBERSHIP_RE.finditer(line):
                ident = match.group(1)
                if not ident.endswith("_clause"):
                    problems.append(
                        f"{relpath}:{lineno}: whole-message synthetic-id "
                        f"membership test (wave-15 shape): {match.group(0)!r}"
                    )
            for match in _ROSTER_ARM_CLAUSE_MARKER_RE.finditer(line):
                problems.append(
                    f"{relpath}:{lineno}: bare clause-marker membership "
                    f"test against a whole message: {match.group(0)!r}"
                )
    return problems


# ---------------------------------------------------------------------------
# Frozen-path disjointness floor (T-21-06-02 / 19-D-08)
#
# `_FROZEN_PATHS_ARRAY_RE` / `_FROZEN_PATHS_ENTRY_RE` copy the identical
# grammar `scripts/check-quality-harness.py`'s `read_frozen_pathspecs` /
# `_frozen_spec_matches` already use over the same file — copied text, not a
# code dependency, the same boundary `_gate_registry.py`'s own
# `_BATTERY_GATE_RE` documents for its analogous D-01 extraction.
# ---------------------------------------------------------------------------

_FROZEN_PATHS_ARRAY_RE = re.compile(r"^_FROZEN_PATHS=\(\n(.*?)^\)$", re.MULTILINE | re.DOTALL)
_FROZEN_PATHS_ENTRY_RE = re.compile(r"^[ \t]*'([^']+)'[ \t]*$", re.MULTILINE)


def frozen_pathspecs(battery_text: str) -> tuple[str, ...]:
    """Pure regex extraction of `_FROZEN_PATHS` from the battery script's own
    source text — derived, never re-typed a second time (19-D-08). Returns
    `()` when the array cannot be located (a self-test fixture may
    deliberately pass array-free text); the live control asserts the real
    array parses to a non-empty tuple."""
    match = _FROZEN_PATHS_ARRAY_RE.search(battery_text)
    if match is None:
        return ()
    return tuple(_FROZEN_PATHS_ENTRY_RE.findall(match.group(1)))


def _frozen_pathspec_matches(rel_posix: str, spec: str) -> bool:
    """Mirrors git's default pathspec matching (fnmatch without
    FNM_PATHNAME, plus directory-prefix coverage) — the same semantics
    `check-quality-harness.py`'s `_frozen_spec_matches` documents for the
    battery's own `git diff`/`git status` legs."""
    return fnmatch.fnmatchcase(rel_posix, spec) or fnmatch.fnmatchcase(
        rel_posix, f"{spec}/*"
    )


def frozen_path_write_problems(write_paths, pathspecs) -> list[str]:
    """T-21-06-02: every path `generate_all()` would write must lie outside
    every `_FROZEN_PATHS` entry. A write inside a frozen path turns
    FROZEN-EVIDENCE red and blocks every commit in the repo (19-D-08)."""
    problems: list[str] = []
    for path in write_paths:
        try:
            rel = path.relative_to(REPO_ROOT).as_posix()
        except ValueError:
            rel = Path(path).as_posix()
        for spec in pathspecs:
            if _frozen_pathspec_matches(rel, spec):
                problems.append(
                    f"frozen-path-write: write target {rel!r} lies inside "
                    f"frozen pathspec {spec!r} (19-D-08)"
                )
                break
    return problems


# ---------------------------------------------------------------------------
# All floors, run together (D-01, D-04, vocabulary, frozen-path) — never
# short-circuited, so no floor can mask another (T-21-06-05's own lesson
# applied to the floor-runner itself).
# ---------------------------------------------------------------------------


def all_floor_problems(
    registry_ids: frozenset[str],
    battery_ids: frozenset[str],
    precommit_ids: frozenset[str],
    requested: dict[str, frozenset[str]],
    emitted: dict[str, frozenset[str]],
    write_paths,
    frozen_specs,
) -> list[str]:
    problems: list[str] = []
    problems += _gate_registry.registry_id_problems(registry_ids, battery_ids, precommit_ids)
    problems += _gate_registry.field_resolution_problems(requested, emitted)
    problems += _gate_registry.vocabulary_problems(emitted)
    problems += frozen_path_write_problems(write_paths, frozen_specs)
    return problems


# ---------------------------------------------------------------------------
# Render layer (plan 21-07, D-21-B): render_gate_table()/render_table_region()
# turn ENTRIES + a harvested blob into the unified 27x4 table both surfaces
# emit (D-02); render_detail_page() emits docs/gates/<GATE-ID>.md pages in
# D-05's fenced-split / D-08's thin-page shapes. Nothing here is written to
# disk by this plan — generate_all() below returns strings, and --check
# reports drift against every target, which is the expected, proving state
# this plan hands to 21-08.
# ---------------------------------------------------------------------------

CLAUDE_MD: Path = REPO_ROOT / "CLAUDE.md"
ARCHITECTURE_MD: Path = REPO_ROOT / "docs" / "ARCHITECTURE.md"
TESTING_MD: Path = REPO_ROOT / "docs" / "TESTING.md"
DETAIL_PAGE_DIR: Path = REPO_ROOT / "docs" / "gates"

# The gate ids whose docs/gates/<ID>.md page carries a hand-written narrative
# region — the four measured-fat cells (D-08) plus the 11 gates whose
# docs/TESTING.md `###` section carried operational prose beyond its bare run
# command (D-21-F, plan 21-10 Task 1). QUAL-01 and TRACE-03 already carried
# real narrative before this migration; the other 11 gained one.
NARRATIVE_ENTRIES: frozenset[str] = frozenset(
    {
        "QUAL-01", "SCAN-GUARD", "TRACE-03", "CONF-GATE", "CONF-SURFACE",
        "VAL-01", "VAL-02", "VAL-03", "VAL-04", "VAL-05", "VERSION-01",
        "DUAL-04", "GATE-01", "BATT-06", "STEP0-08", "STEP0-06",
    }
)

# The two region-marker pairs bounding CLAUDE.md's and docs/ARCHITECTURE.md's
# generated CI-gate-table regions. Both surfaces reuse the identical literal
# marker text — _replace_region operates per-file, so reusing the same
# HTML-comment text across two files is not a collision.
CLAUDE_REGION_MARKERS: tuple[str, str] = (
    GENERATED_MARKER.format(source="scripts/_gate_registry.py"),
    GENERATED_END_MARKER,
)
ARCHITECTURE_REGION_MARKERS: tuple[str, str] = (
    GENERATED_MARKER.format(source="scripts/_gate_registry.py"),
    GENERATED_END_MARKER,
)
TESTING_REGION_MARKERS: tuple[str, str] = (
    GENERATED_MARKER.format(source="scripts/_gate_registry.py"),
    GENERATED_END_MARKER,
)

# Bootstrap anchors (first-migration only — see _replace_or_bootstrap_region):
# stable, pre-existing, whole-line prose that brackets the span being
# converted from hand-maintained to generated. Both lines are hand-written
# narrative that survives OUTSIDE the generated region on every subsequent
# regeneration, so re-using them as anchors on every call (not just the
# first) is safe: they never move.
_CLAUDE_BOOTSTRAP_AFTER = "### CI gates"
_CLAUDE_BOOTSTRAP_BEFORE = (
    "HARN-01, HARN-02 and HARN-03 were registered under HARN-04 at v8.18.0 — each is a CI job plus a"
)
_ARCHITECTURE_BOOTSTRAP_AFTER = "## CI and pre-commit gate inventory"
_ARCHITECTURE_BOOTSTRAP_BEFORE = (
    "HARN-01, HARN-02 and HARN-03 were registered under HARN-04 at v8.18.0 — each has a CI job plus a"
)
# docs/TESTING.md (D-21-F): the generated index replaces the 13 `###`-level
# per-gate sections between "## CI gates — operational run-detail" and the
# next H2 heading, "## Routing battery (developer tools — not in CI)" — both
# anchor lines are hand-written prose that stays outside the generated
# region on every subsequent regeneration.
_TESTING_BOOTSTRAP_AFTER = "## CI gates — operational run-detail"
_TESTING_BOOTSTRAP_BEFORE = "## Routing battery (developer tools — not in CI)"

# The shared post-unification statement (D-02): replaces both surfaces'
# superseded framing sentences ("keeps its own operational copy by design" /
# "Every other document links here rather than restating it"), which
# described the pre-unification state and are false the moment this lands.
_POST_UNIFICATION_STATEMENT = (
    "Both surfaces render the same population and the same columns from "
    "`scripts/_gate_registry.py`, emitted by `scripts/gen-gate-docs.py --write`, "
    "so the two cannot diverge"
)


def _page_slug(entry) -> str:
    """The docs/gates/<slug>.md filename stem for a registry entry. Derived
    from `entry.key` (equal to `gate_id` for every normal entry) rather than
    hand-typed per row; `:` is not a safe filename character, so the two
    PRECOMMIT: synthetic keys are the only ones actually rewritten."""
    return entry.key.replace(":", "-")


class SlugCollisionError(ValueError):
    """Raised by `generate_all()` when two registry entries resolve to the
    same `docs/gates/<slug>.md` page slug (T-21-14-02). `_control_page_per_entry`
    compares SETS of expected-vs-emitted paths and therefore cannot see a
    collision — the `targets` dict `generate_all()` builds would silently
    overwrite one entry's detail page with another's, and the set comparison
    would still read as clean because both sets have the same cardinality
    drop. This raises at generation time, before any page is written, naming
    every colliding key."""


def _assert_no_slug_collisions(entries) -> None:
    """Pure floor, called by `generate_all()` and driven directly by its own
    negative-arm control (`slug-collision-raises`) against a synthetic
    entry list, so the control exercises the SAME code the live floor uses.

    Raises `SlugCollisionError` naming every key sharing a slug when
    `len({_page_slug(e) for e in entries}) != len(entries)`.
    """
    by_slug: dict[str, list[str]] = {}
    for e in entries:
        by_slug.setdefault(_page_slug(e), []).append(e.key)
    collisions = {slug: keys for slug, keys in by_slug.items() if len(keys) > 1}
    if collisions:
        detail = "; ".join(
            f"{slug!r} shared by {keys!r}" for slug, keys in sorted(collisions.items())
        )
        raise SlugCollisionError(
            f"duplicate docs/gates/<slug>.md page slug(s): {detail}"
        )


def _glob_prose(globs) -> str:
    """`", ".join(f"`{g}`" for g in globs)` — the exact formula
    `check-traceability.py`'s block (n) requires for its TRACE-03 row lock.
    Applied generically to whatever `scan_globs` a harvested blob carries,
    never re-typed against a specific gate's list (T-21-07-01)."""
    return ", ".join(f"`{g}`" for g in globs)


def _script_cell(entry) -> str:
    """The Script column's rendered text, derived from the registry entry
    rather than a fifth hand-typed column. A script-backed entry renders its
    own script relpath, extended with the first invocation's flag when its
    `run_command` addresses that same script (so two entries sharing one
    script, e.g. DUAL-04 / GATE-02-v8.5, still render distinctly); an
    orphan entry (no script) renders its `static_facts['tool']` when present,
    else an em dash."""
    if entry.script is not None:
        first_cmd = entry.run_command.split(" && ")[0].strip()
        prefixed = f"python3 {entry.script}"
        if first_cmd.startswith(prefixed):
            return f"`{first_cmd[len('python3 '):]}`"
        return f"`{entry.script}`"
    tool = entry.static_facts.get("tool")
    if tool:
        return f"`{tool}`"
    return "—"


def _checks_cell(entry, blob) -> str:
    """The 'What it checks' cell: the registry entry's `summary` plus
    whichever derived counts its `consumes` tuple names, rendered from the
    harvested blob (never re-typed), plus a link to the gate's detail page
    (D-07: no character cap, short because the detail lives elsewhere)."""
    derived_bits: list[str] = []
    if blob is not None:
        for field_name in entry.consumes:
            value = blob.get(field_name)
            if value is None:
                continue
            if field_name == "scan_globs" and isinstance(value, list):
                derived_bits.append(_glob_prose(value))
            elif isinstance(value, list):
                derived_bits.append(f"{field_name}={len(value)}")
            elif isinstance(value, dict):
                derived_bits.append(f"{field_name}={len(value)} entries")
            else:
                derived_bits.append(f"{field_name}={value}")
    slug = _page_slug(entry)
    parts = [entry.summary]
    if derived_bits:
        parts.append("(" + "; ".join(derived_bits) + ")")
    # Canonical link target is repo-root-relative (docs/gates/<slug>.md) — the
    # form that resolves correctly from CLAUDE.md, which sits at the repo
    # root. render_gate_table(rows) is called identically for BOTH surfaces
    # (D-02), so this same string reaches docs/ARCHITECTURE.md's table too,
    # where it would NOT resolve (docs/ARCHITECTURE.md sits one directory
    # level inside docs/, so its correct relative target is gates/<slug>.md,
    # not docs/gates/<slug>.md). render_table_region() rewrites this target
    # for the ARCHITECTURE_MD surface only, after this shared row text is
    # computed — the same directory-depth fix sync-content.py's
    # _rewrite_detail_link() applies to the agent-body/skill-stub split.
    parts.append(f"See [`docs/gates/{slug}.md`](docs/gates/{slug}.md).")
    text = " ".join(parts)
    return text.replace("\n", " ").replace("|", "\\|")


def _gate_table_rows(
    entries, harvested: dict[str, dict]
) -> list[tuple[str, str, str, str]]:
    """Build the documented (non-anticipatory) x 4-column row set from
    `entries` + a harvest blob map -- one row per non-anticipatory
    registry entry, a live count this function derives from `entries`
    rather than a hand-typed one (a prior row-count docstring literal
    went stale as the registry grew; plan 21-20 Task 2 removed it). Pure
    -- used identically to build the SAME `rows` value `generate_all()`
    hands to both surfaces (D-02)."""
    rows: list[tuple[str, str, str, str]] = []
    for entry in entries:
        if entry.key in _gate_registry._ANTICIPATORY_KEYS:
            continue
        if entry.gate_id is None and not entry.extra_ids:
            gate_col = "—"
        else:
            ids = ((entry.gate_id,) if entry.gate_id else ()) + entry.extra_ids
            gate_col = " / ".join(ids)
        blob = harvested.get(entry.script) if entry.script else None
        rows.append((gate_col, entry.mechanism, _script_cell(entry), _checks_cell(entry, blob)))
    return rows


def render_gate_table(rows) -> str:
    """The single 4-column row renderer (`Gate | Job / Mechanism | Script |
    What it checks`). Called twice by `generate_all()` — once per surface —
    on the SAME `rows` value, which is what makes 'one renderer, two
    surfaces' true by construction rather than by comparison (D-02)."""
    header = "| Gate | Job / Mechanism | Script | What it checks |"
    sep = "|------|-----------------|--------|-----------------|"
    lines = [header, sep]
    for gate_col, mechanism_col, script_col, checks_col in rows:
        lines.append(f"| {gate_col} | {mechanism_col} | {script_col} | {checks_col} |")
    return "\n".join(lines)


def _population_counts(entries) -> dict[str, int]:
    """Every count the population-arithmetic sentence states, derived from
    `entries` — never a hand-typed literal. `entries` is a parameter (not a
    read of the module global) specifically so a self-test control can add a
    synthetic entry and observe which counts move.

    `precommit_count` and `hook_mechanism_count` are two SEPARATELY derived
    figures naming two different nouns (CR-04): `precommit_count` counts
    pre-commit GATES (registry `PRECOMMIT:` rows, one per hook gate);
    `hook_mechanism_count` counts hook MECHANISMS (distinct hook script
    relpaths in `_gate_registry._HOOK_PATHS` that exist on disk — never the
    same value reused under a second name). A reader could not previously
    tell whether "2 pre-commit" meant hooks or gates, which is what made the
    stale figure unfalsifiable in the first place.
    """
    documented = [e for e in entries if e.key not in _gate_registry._ANTICIPATORY_KEYS]
    ci_count = sum(1 for e in documented if e.ci_job is not None)
    precommit_count = sum(1 for e in documented if e.key.startswith("PRECOMMIT:"))
    inline_count = sum(
        1
        for e in documented
        if e.script is None and e.gate_id is not None and e.ci_job is None
        and not e.key.startswith("PRECOMMIT:")
    )
    tallied_count = sum(1 for e in documented if e.gate_id is not None)
    battery_only_count = tallied_count - ci_count - inline_count
    hook_mechanism_count = sum(
        1 for relpath in _gate_registry._HOOK_PATHS if (REPO_ROOT / relpath).exists()
    )
    return {
        "ci_count": ci_count,
        "precommit_count": precommit_count,
        "inline_count": inline_count,
        "tallied_count": tallied_count,
        "battery_only_count": battery_only_count,
        "hook_mechanism_count": hook_mechanism_count,
    }


def _pluralize_count(count: int, singular: str, plural: str | None = None) -> str:
    """`"{count} {word}"` with the WORD correctly singular or plural — never
    the literal-parenthetical `gate(s)`/`check(s)` shape, which reads as a
    template artifact on a surface whose entire purpose is readability.
    `plural` defaults to `singular + "s"`; pass it explicitly for irregular
    forms (none needed today, but the parameter exists so a future noun
    doesn't have to relearn this)."""
    word = singular if count == 1 else (plural if plural is not None else f"{singular}s")
    return f"{count} {word}"


def _population_arithmetic_sentence(entries) -> str:
    c = _population_counts(entries)
    battery_only_phrase = _pluralize_count(c["battery_only_count"], "battery-only gate")
    inline_phrase = _pluralize_count(c["inline_count"], "inline check")
    precommit_gates_phrase = _pluralize_count(c["precommit_count"], "pre-commit gate")
    hook_mechanism_phrase = _pluralize_count(c["hook_mechanism_count"], "hook mechanism")
    return (
        f"Gates run on three surfaces: **{c['ci_count']} in CI** "
        "(`.github/workflows/validation.yml`, on push/PR to master), "
        f"**{c['tallied_count']} tallied in the offline battery** "
        "(`bash scripts/check-firewall-battery.sh`), and "
        f"**{precommit_gates_phrase}** ({hook_mechanism_phrase} run the "
        "identical set in the identical order). The battery is a strict "
        f"superset of CI: all {c['ci_count']} CI gates plus "
        f"{battery_only_phrase} plus "
        f"{inline_phrase}. That is {c['ci_count']} + "
        f"{c['battery_only_count']} + {c['inline_count']} = {c['tallied_count']}."
    )


def _rewrite_gates_link_for_architecture(text: str) -> str:
    """Rewrite a `](docs/gates/...)` link target to `](gates/...)`.

    `_checks_cell()` computes ONE canonical link target — `docs/gates/<slug>.md`,
    the form that resolves from `CLAUDE.md` (repo root) — and `render_gate_table
    (rows)` renders it identically for both surfaces (D-02: same `rows` value,
    same renderer, no per-surface branch in the row computation itself).
    `docs/ARCHITECTURE.md` sits one directory level INSIDE `docs/`, so that same
    target does not resolve there; its correct relative form is `gates/<slug>.md`.

    This mirrors `sync-content.py`'s `_rewrite_detail_link()` — the identical
    directory-depth problem (a shared source rendered onto two assembly
    surfaces sitting at different depths), fixed the same way: adapt the
    ASSEMBLED TEXT for the surface that needs a shorter path, rather than
    branching the shared row/cell computation. The row DATA (`rows`, and
    `render_gate_table(rows)`'s output) stays surface-agnostic and byte-
    identical between the two calls; only this post-processing step, applied
    to `docs/ARCHITECTURE.md`'s rendering alone, differs.
    """
    return text.replace("](docs/gates/", "](gates/")


def render_table_region(rows, surface: str) -> str:
    """Wrap `render_gate_table(rows)` with the population-arithmetic
    paragraph and the surface-appropriate lead-in prose (D-02). The lead-in
    replaces both surfaces' superseded framing sentences with the shared
    post-unification statement."""
    if surface == "CLAUDE_MD":
        lead_in = (
            f"{_POST_UNIFICATION_STATEMENT}; a working session still sees the full "
            "gate list here without opening `docs/`, and per-gate detail lives in "
            "`docs/gates/<GATE-ID>.md`. Every gate below except QUAL-01 runs in "
            "`.github/workflows/validation.yml` on push/PR to master; QUAL-01 is "
            "battery-only — it has no CI job, and "
            "`bash scripts/check-firewall-battery.sh` is the only thing that runs it."
        )
    elif surface == "ARCHITECTURE_MD":
        lead_in = (
            f"{_POST_UNIFICATION_STATEMENT}; `CLAUDE.md` keeps the full gate list "
            "visible without opening `docs/`, and per-gate detail lives in "
            "`docs/gates/<GATE-ID>.md`."
        )
    else:
        raise ValueError(f"render_table_region: unknown surface {surface!r}")
    table = render_gate_table(rows)
    if surface == "ARCHITECTURE_MD":
        table = _rewrite_gates_link_for_architecture(table)
    arithmetic = _population_arithmetic_sentence(_gate_registry.ENTRIES)
    return f"{lead_in}\n\n{table}\n\n{arithmetic}"


# The lead-in sentence for docs/TESTING.md's generated index (D-21-F): states
# the split between "how to run" (this file) and "what a gate asserts and
# does not" (docs/gates/<ID>.md) — the same "point at the generated fact,
# don't restate it" fork this module already uses for the two CI-gate
# tables' lead-ins.
_TESTING_INDEX_LEAD_IN = (
    "`docs/TESTING.md` is how to run every gate locally; `docs/gates/<GATE-ID>.md` "
    "is what each gate asserts and what it does not. One row below per "
    "registry entry — the id (or `—` for an entry with no standalone gate "
    "id), the detail page, and the exact local run command."
)


def _testing_index_rows(entries) -> list[tuple[str, str, str]]:
    """Build docs/TESTING.md's generated index rows: id, a link to
    `docs/gates/<GATE-ID>.md`, and the local run command — one row per
    registry entry (`len(ENTRIES)`, D-21-F), covering every gate the old 13
    `###` sections only partially enumerated (13 of 25/28)."""
    rows: list[tuple[str, str, str]] = []
    for entry in entries:
        if entry.gate_id is None and not entry.extra_ids:
            id_col = "—"
        else:
            ids = ((entry.gate_id,) if entry.gate_id else ()) + entry.extra_ids
            id_col = " / ".join(ids)
        slug = _page_slug(entry)
        # Canonical target is repo-root-relative (docs/gates/<slug>.md), the
        # same string `_checks_cell()` computes for the two CI-gate tables;
        # rewritten to `gates/<slug>.md` below since docs/TESTING.md sits at
        # the same directory depth as docs/ARCHITECTURE.md.
        page_col = f"[`docs/gates/{slug}.md`](docs/gates/{slug}.md)"
        run_col = f"`{entry.run_command}`".replace("\n", " ")
        rows.append((id_col, page_col, run_col))
    return rows


def render_testing_index_region(entries) -> str:
    """Wrap the docs/TESTING.md index table with its lead-in sentence.
    Reuses `_rewrite_gates_link_for_architecture` for the same directory-
    depth rewrite `docs/ARCHITECTURE.md` needs — both files sit one level
    inside `docs/`, so the fix is identical, not architecture-specific."""
    rows = _testing_index_rows(entries)
    header = "| Gate | Page | Run command |"
    sep = "|------|------|-------------|"
    lines = [header, sep]
    for id_col, page_col, run_col in rows:
        lines.append(f"| {id_col} | {page_col} | {run_col} |")
    table = _rewrite_gates_link_for_architecture("\n".join(lines))
    return f"{_TESTING_INDEX_LEAD_IN}\n\n{table}"


def _replace_or_bootstrap_region(
    text: str,
    start_marker: str,
    end_marker: str,
    new_content: str,
    bootstrap_anchor_after: str,
    bootstrap_anchor_before: str,
) -> str:
    """Like `_replace_region`, but bootstraps the region on the FIRST
    migration, when `start_marker`/`end_marker` do not yet exist in `text`
    at all (CLAUDE.md and docs/ARCHITECTURE.md carry no GENERATED markers
    today). `bootstrap_anchor_after`/`bootstrap_anchor_before` are stable,
    pre-existing whole lines that bracket the span being converted — each
    must appear exactly once, non-fenced. Once the real markers exist (any
    `--write` after the first), this delegates straight to `_replace_region`
    and the bootstrap anchors are not consulted."""
    lines = text.splitlines(keepends=True)
    bare_lines = [ln.splitlines()[0] if ln.splitlines() else ln for ln in lines]
    fenced = _fenced_line_flags(bare_lines)
    start_count = sum(
        1 for bare, is_fenced in zip(bare_lines, fenced) if not is_fenced and bare == start_marker
    )
    if start_count >= 1:
        return _replace_region(text, start_marker, end_marker, new_content)

    def _find(marker: str) -> list[int]:
        return [
            i
            for i, (bare, is_fenced) in enumerate(zip(bare_lines, fenced))
            if not is_fenced and bare == marker
        ]

    after_idxs = _find(bootstrap_anchor_after)
    if len(after_idxs) != 1:
        raise RegionMarkerError(
            f"bootstrap anchor (after) {bootstrap_anchor_after!r}: found "
            f"{len(after_idxs)} occurrence(s) outside fenced code blocks (expected exactly 1)"
        )
    before_idxs = _find(bootstrap_anchor_before)
    if len(before_idxs) != 1:
        raise RegionMarkerError(
            f"bootstrap anchor (before) {bootstrap_anchor_before!r}: found "
            f"{len(before_idxs)} occurrence(s) outside fenced code blocks (expected exactly 1)"
        )
    after_idx, before_idx = after_idxs[0], before_idxs[0]
    if before_idx <= after_idx:
        raise RegionMarkerError(
            f"bootstrap anchor (before) {bootstrap_anchor_before!r} (line {before_idx}) "
            f"does not follow anchor (after) {bootstrap_anchor_after!r} (line {after_idx})"
        )
    prefix = "".join(lines[: after_idx + 1])
    suffix = "".join(lines[before_idx:])
    body = new_content
    if body and not body.endswith("\n"):
        body += "\n"
    block = f"\n{start_marker}\n{body}{end_marker}\n\n"
    return prefix + block + suffix


# ---------------------------------------------------------------------------
# docs/gates/<GATE-ID>.md detail-page renderer (D-05 fenced split, D-08 thin
# pages)
# ---------------------------------------------------------------------------

DETAIL_FACTS_MARKERS: tuple[str, str] = (
    "<!-- GENERATED:FACTS -->",
    "<!-- END GENERATED:FACTS -->",
)
DETAIL_HOWTORUN_MARKERS: tuple[str, str] = (
    "<!-- GENERATED:HOW-TO-RUN -->",
    "<!-- END GENERATED:HOW-TO-RUN -->",
)
_ALL_DETAIL_MARKER_PAIRS: tuple[tuple[str, str], ...] = (
    DETAIL_FACTS_MARKERS,
    DETAIL_HOWTORUN_MARKERS,
)

_DISCLOSED_BOUNDS_HAND_WRITTEN_COMMENT = (
    "<!-- HAND-WRITTEN: preserved verbatim across regeneration. Fill in this "
    "gate's disclosed bounds / limitations narrative below. -->"
)


def _facts_block(entry, blob: dict | None) -> str:
    lines = ["## Facts", ""]
    if not entry.consumes or blob is None:
        reason = "no script backs it" if entry.script is None else "nothing consumed yet"
        lines.append(f"This gate carries no `--describe`-derived facts ({reason}).")
    else:
        for field_name in entry.consumes:
            value = blob.get(field_name)
            if value is None:
                lines.append(f"- `{field_name}`: (not emitted by the live harvest)")
            elif field_name == "scan_globs" and isinstance(value, list):
                lines.append(f"- `{field_name}` ({len(value)}): {_glob_prose(value)}")
            elif isinstance(value, list):
                rendered = ", ".join(f"`{v}`" for v in value)
                lines.append(f"- `{field_name}` ({len(value)}): {rendered}")
            elif isinstance(value, dict) and all(isinstance(v, dict) for v in value.values()):
                # Nested dict-of-dicts (e.g. `contract_pins`, each keyed by
                # function name with its own {digest, line_count}): render
                # the sub-fields too, not just the outer keys, so a narrative
                # citing a pin's line_count (D-06's containment rule) has a
                # corroborating literal to point at on the same page.
                parts = []
                for k in sorted(value):
                    sub = value[k]
                    sub_bits = ", ".join(f"{sk}={sv}" for sk, sv in sorted(sub.items()))
                    parts.append(f"`{k}` ({sub_bits})")
                lines.append(f"- `{field_name}` ({len(value)} entries): {'; '.join(parts)}")
            elif isinstance(value, dict) and all(
                isinstance(v, (str, int, float, bool)) for v in value.values()
            ):
                # Scalar-valued dict (e.g. `locked_constants`): render the
                # value alongside each key, not just the key — a narrative
                # citing a locked constant's actual value (e.g. the
                # marked-claim ratchet's pinned `4`) needs that digit
                # present inside the fence for D-06's containment rule.
                rendered = ", ".join(f"`{k}`={v!r}" for k, v in sorted(value.items()))
                lines.append(f"- `{field_name}` ({len(value)} entries): {rendered}")
            elif isinstance(value, dict):
                rendered = ", ".join(f"`{k}`" for k in sorted(value))
                lines.append(f"- `{field_name}` ({len(value)} entries): {rendered}")
            else:
                lines.append(f"- `{field_name}`: `{value}`")
    return "\n".join(lines)


def _how_to_run_block(entry) -> str:
    ci_job_text = f"`{entry.ci_job}`" if entry.ci_job else "— (not a CI job)"
    return "\n".join(
        [
            "## How to run",
            "",
            "```sh",
            entry.run_command,
            "```",
            "",
            f"CI job: {ci_job_text}",
        ]
    )


def render_detail_page(entry, blob: dict | None, existing_text: str | None) -> str:
    """Emit `docs/gates/<GATE-ID>.md`. A thin (non-`NARRATIVE_ENTRIES`) entry
    is fully generated end to end (D-08). A `NARRATIVE_ENTRIES` member's page
    preserves every byte of its hand-written narrative across regeneration
    (D-05): when `existing_text` is not None, only the two fenced regions
    (Facts, How to run) are rewritten via `_replace_region`; everything else
    — including the disclosed-bounds narrative — is untouched."""
    facts_content = _facts_block(entry, blob)
    howtorun_content = _how_to_run_block(entry)

    if existing_text is not None and entry.key in NARRATIVE_ENTRIES:
        text = existing_text
        text = _replace_region(
            text, DETAIL_FACTS_MARKERS[0], DETAIL_FACTS_MARKERS[1], facts_content
        )
        text = _replace_region(
            text, DETAIL_HOWTORUN_MARKERS[0], DETAIL_HOWTORUN_MARKERS[1], howtorun_content
        )
        return text

    title_sentence = entry.summary.split(". ")[0].rstrip(".") + "."
    parts = [
        f"# {entry.key}: {title_sentence}",
        "",
        DETAIL_FACTS_MARKERS[0],
        facts_content,
        DETAIL_FACTS_MARKERS[1],
        "",
        DETAIL_HOWTORUN_MARKERS[0],
        howtorun_content,
        DETAIL_HOWTORUN_MARKERS[1],
    ]
    if entry.key in NARRATIVE_ENTRIES:
        parts += [
            "",
            "## Disclosed bounds",
            "",
            _DISCLOSED_BOUNDS_HAND_WRITTEN_COMMENT,
            "",
            "(TODO: fill in this gate's disclosed bounds narrative.)",
        ]
    return "\n".join(parts) + "\n"


# ---------------------------------------------------------------------------
# D-06: containment rule — a number stated in a detail page's hand-written
# prose (outside a generated fence) must also appear, as that exact literal,
# inside a generated fence on the same page. Proves the number is CURRENT,
# never that it describes the right thing — a count that is correct but
# attached to the wrong noun still passes (published on each page's own
# text by render_detail_page's narrative section, in the voice R7/R9/R10
# use).
# ---------------------------------------------------------------------------

_NUMBER_RE = re.compile(r"\b\d[\d,]*\b")

# Identifier/citation shapes stripped BEFORE `_NUMBER_RE` runs, so a digit
# that is part of an identifier or a measured-transition reading is never
# treated as a "count claim" in the D-06 sense. Each pattern mirrors an
# EXISTING exemption idiom already shipped elsewhere in this repo for the
# identical underlying problem (a digit that names something rather than
# counting something) — this is not new checking philosophy, it is the
# same idiom applied to a new surface:
#   - `check-quality-harness.py`'s own gate-id H1-exclusion (21-07): an
#     identifier like `GATE-02-v8.5` trips a bare digit regex on its own
#     suffix despite naming a gate, not a count.
#   - `check-traceability.py`'s HEADLINE-LOCK arrow-adjacency exemption: a
#     digit run immediately adjacent to a transition arrow (`→`, `->`,
#     `-->`) is a DELTA, not a current-fact count.
# Disclosed bound, in the same voice as D-06's own: stripping an
# identifier shape proves that shape is NOT a count claim; it does not
# prove the identifier itself is correct (a stale plan number would still
# pass). Order matters — longer/more specific patterns (ISO dates, version
# stamps) are tried before the generic two-segment hyphen pattern so a
# three-segment date is consumed whole rather than leaving a residual
# single-segment match.
_CITATION_SHAPE_RES: tuple[re.Pattern[str], ...] = (
    # ISO date: 2026-09-02
    re.compile(r"\b\d{4}-\d{2}-\d{2}\b"),
    # Version stamp: v8.7, v8.26, v9.0.0
    re.compile(r"\bv\d+(?:\.\d+){1,2}\b"),
    # Backlog reference: 999.12, 999.13 (this repo's one numeric backlog
    # namespace prefix, per CLAUDE.md's own "999.NN" citations)
    re.compile(r"\b999\.\d{1,3}\b"),
    # Bare two/three-segment numeric citation: plan numbers (13-10, 15-08),
    # ordinal ranges of named items (arms 4-9, hop 1-6) — never a count.
    # Tried BEFORE the letter-prefixed identifier pattern below: a compound
    # like "pre-13-12" would otherwise have its "pre-13" segment consumed
    # first (matching the identifier shape), leaving a residual "-12" that
    # no longer has a leading digit to pair with.
    re.compile(r"\b\d{1,4}-\d{1,4}(?:-\d{1,4})?\b"),
    # Plan-number-prefixed filename/id citation: 13-VERIFICATION-round3.md,
    # 15-04-SUMMARY.md (the digit-digit prefix of the second already
    # matched above; this catches the digit-letter form).
    re.compile(r"\b\d{1,4}-[A-Za-z][A-Za-z0-9_.\-]*\b"),
    # Letter-prefixed identifier double-dot range: LEDGER-01..04. Tried
    # BEFORE the plain letter-prefixed pattern below for the same reason as
    # the plan-number-before-identifier ordering above — otherwise
    # "LEDGER-01" is consumed first, leaving an orphaned "..04".
    re.compile(r"\b[A-Za-z][A-Za-z0-9]*-\d{1,4}\.\.\d{1,4}\b"),
    # Letter-prefixed identifier hyphen-then-slash compound: "Criteria-4/6"
    # (an elliptical re-mention of "Criteria 4 and 6" elsewhere in the same
    # narrative). Tried before the plain letter-prefixed pattern below for
    # the same reason as the other two-part orderings above.
    re.compile(r"\b[A-Za-z][A-Za-z0-9]*-\d{1,4}/\d{1,4}\b"),
    # Letter-prefixed identifier-digit citation: CONTRACT-06, WR-04, D-02,
    # SCAN-04, CHAINHEAD-07, HARNESS-01, LEDGER-01, CR-01, HC-04, etc.
    re.compile(r"\b[A-Za-z][A-Za-z0-9]*-\d{1,4}\b"),
    # Measured-transition vector, mirroring HEADLINE-LOCK's own
    # arrow-adjacency rule: a digit immediately next to a transition arrow
    # is a delta, not a current-fact count.
    re.compile(r"\d[\d,]*\s*(?:→|-->|->)\s*\d[\d,]*"),
    # Slash-separated reading vector: 0/0/0, 7/0/1 (a measured (claims/
    # fragments/untraced)-shaped triple, not a single count claim).
    re.compile(r"\b\d+(?:/\d+){1,3}\b"),
    # Named-thing ordinal reference: Phase 11, section 6, arm 11, leg 5, hop
    # position 1, Criterion 4 (and its plural, "Criteria 4 and 6") — the
    # digit names WHICH numbered thing is being discussed, it does not
    # count anything. The optional "(and|or|/) N" tail catches the
    # "Criteria 4 and 6"/"4 or 6"/"4/6" shape without a second, separately
    # unanchored bare-digit match escaping.
    re.compile(
        r"\b(?:Phase|section|arm|arms|leg|hop|position|criteria|criterion|gap|plan)\s+\d{1,3}"
        r"(?:\s*(?:and|or|/)\s*\d{1,3})?\b",
        re.IGNORECASE,
    ),
    # Parenthetical leg/item enumeration: "(1) worked-example extraction",
    # "(2) cross-surface literal reconciliation" — an ordinal marker, not a
    # count of anything.
    re.compile(r"\(\d{1,2}\)"),
    # Double-dot fixture-id range: LEDGER-01..04 — an id range, not a count.
    re.compile(r"\b\d{1,3}\.\.\d{1,3}\b"),
    # English-prose transition: "58 to 72", "72 to 86" — the same DELTA
    # shape the arrow-vector rule above covers, spelled with "to" instead
    # of an arrow.
    re.compile(r"\b\d{1,4}\s+to\s+\d{1,4}\b"),
    # Exit-code / return-code reference: "rc 0", "exit code 1" — an
    # identifier for a specific outcome, not a count.
    re.compile(r"\b(?:rc|exit code|exit)\s+\d{1,2}\b", re.IGNORECASE),
    # Quoted historical figure being corrected/disputed in the same
    # sentence ('not the "20" an earlier version ... stated') — the quotes
    # mark it as a citation of what was WRITTEN, not a restated current
    # count.
    re.compile(r'"\d{1,4}"'),
    # Named-fixture measured-reading phrases specific to one frozen capture
    # (a fixture's own reading is not a `--describe`-derived current fact;
    # it is a historical measurement pinned to that one fixture, reported
    # the same way a version number is): "N call sites", "N real", "N
    # claims", "N (ledger) fragments", "N untraced", "N malformed", "N
    # targeted neutralizations", and the disclosed-as-unfalsifiable
    # emission-cost character-count comparison ("2,288 vs. an independent
    # 1,381 reconstruction").
    re.compile(r"\b\d{1,3}\s+call\s+sites?\b", re.IGNORECASE),
    re.compile(r":\s*\d{1,3}\s+real\b", re.IGNORECASE),
    re.compile(r"\b\d{1,3}\s+claims?\b", re.IGNORECASE),
    re.compile(r"\b\d{1,3}\s+(?:ledger\s+)?fragments?\b", re.IGNORECASE),
    re.compile(r"\b\d{1,3}\s+untraced\b", re.IGNORECASE),
    re.compile(r"\b\d{1,3}\s+malformed\b", re.IGNORECASE),
    re.compile(r"\b\d{1,3}\s+targeted\s+neutralizations?\b", re.IGNORECASE),
    re.compile(r"\b\d{1,3}\s+of\s+them\b", re.IGNORECASE),
    # Code-literal comparison / precise-increment phrasing: "== 0",
    # "by exactly 1" — describes a specific test assertion's shape, not a
    # current-fact count this page's Facts fence is expected to carry.
    re.compile(r"==\s*\d{1,3}\b"),
    re.compile(r"\bexactly\s+\d{1,3}\b", re.IGNORECASE),
    re.compile(
        r"\b\d{1,3}(?:,\d{3})*\s+vs\.\s+an?\s+independent\s+\d{1,3}(?:,\d{3})*\s+reconstruction\b",
        re.IGNORECASE,
    ),
)


def _strip_citation_shaped_numbers(text: str) -> str:
    """Remove every recognised identifier/citation/transition-vector shape
    from `text` before `_normalise_numbers` extracts count claims from it.
    See `_CITATION_SHAPE_RES` for the shapes and their precedent."""
    for pattern in _CITATION_SHAPE_RES:
        text = pattern.sub(" ", text)
    return text


_SPELLED_OUT_ONES: dict[str, int] = {
    "one": 1, "two": 2, "three": 3, "four": 4, "five": 5, "six": 6, "seven": 7,
    "eight": 8, "nine": 9, "ten": 10, "eleven": 11, "twelve": 12, "thirteen": 13,
    "fourteen": 14, "fifteen": 15, "sixteen": 16, "seventeen": 17, "eighteen": 18,
    "nineteen": 19,
}
_SPELLED_OUT_TENS: dict[str, int] = {
    "twenty": 20, "thirty": 30, "forty": 40, "fifty": 50, "sixty": 60,
    "seventy": 70, "eighty": 80, "ninety": 90,
}
_WORD_RE = re.compile(r"[A-Za-z][A-Za-z-]*")


def _spelled_number_value(word: str) -> int | None:
    """One spelled-out number word or hyphenated tens-ones compound
    ('twenty' .. 'ninety-nine') to its int value, else None. Bound to the
    vocabulary D-06 names: one..twenty, the tens, and hyphenated compounds;
    'hundred' is combined by `_normalise_numbers` itself, one level up."""
    word = word.lower()
    if word in _SPELLED_OUT_ONES:
        return _SPELLED_OUT_ONES[word]
    if word in _SPELLED_OUT_TENS:
        return _SPELLED_OUT_TENS[word]
    if "-" in word:
        left, _, right = word.partition("-")
        if left in _SPELLED_OUT_TENS and right in _SPELLED_OUT_ONES:
            return _SPELLED_OUT_TENS[left] + _SPELLED_OUT_ONES[right]
    return None


def _normalise_numbers(text: str, include_spelled_out: bool = True) -> set[str]:
    """Every digit-form number literal in `text`, plus — when
    `include_spelled_out` — every spelled-out number word/compound
    normalised to its digit string (D-06's stated position on spelled-out
    forms). Disclosed bound, published on every detail page: a spelled-out
    form outside this vocabulary (one..twenty, the tens, hundred,
    hyphenated compounds) is not normalised and is therefore not checked.

    Second, measured disclosed bound (found migrating the four
    `NARRATIVE_ENTRIES` pages, plan 21-08): dense technical prose uses
    small number words constantly as ordinary language ("the two contract
    surfaces", "one of the three entries", "seven of the nine") that are
    not current-fact count claims at all. `include_spelled_out=False`
    (used for `NARRATIVE_ENTRIES` hand-written narrative text only, never
    for the thin fully-generated pages, a live-counted population that
    moves as gates are added) turns off SPELLED-OUT matching
    for that text while leaving bare-digit containment fully active — a
    stale bare-digit count (`27` diverging from a Facts-fence `27`) is
    still caught; an ordinary-language spelled-out number in flowing prose
    is not force-corroborated or force-reworded."""
    found: set[str] = {m.group(0).replace(",", "") for m in _NUMBER_RE.finditer(text)}
    if not include_spelled_out:
        return found
    words = _WORD_RE.findall(text)
    i = 0
    while i < len(words):
        value = _spelled_number_value(words[i])
        if value is not None:
            if i + 1 < len(words) and words[i + 1].lower() == "hundred":
                value *= 100
                i += 1
            found.add(str(value))
        i += 1
    return found


def _generated_line_flags(bare_lines: list[str], marker_pairs) -> list[bool]:
    """Per bare line: is it inside — or itself — one of `marker_pairs`'
    GENERATED regions? Independent of `_fenced_line_flags` (CommonMark code
    fences) — these are the HTML-comment GENERATED markers instead."""
    inside = [False] * len(bare_lines)
    open_end: str | None = None
    for i, bare in enumerate(bare_lines):
        if open_end is None:
            for start, end in marker_pairs:
                if bare == start:
                    open_end = end
                    inside[i] = True
                    break
            continue
        inside[i] = True
        if bare == open_end:
            open_end = None
    return inside


def detail_page_containment_problems(
    display_name: str,
    text: str,
    marker_pairs=_ALL_DETAIL_MARKER_PAIRS,
    check_spelled_out: bool = True,
) -> list[str]:
    """D-06's containment floor for one `docs/gates/*.md` page's text. The
    page's own H1 title (line 0) is excluded from the 'outside' scan — it
    names the gate id, an identifier, not a count claim, and gate ids like
    `VAL-01` or `GATE-02-v8.5` otherwise trip the digit regex on their own
    suffix. Citation/identifier/transition-vector shapes (plan numbers,
    phase-adjacent identifiers, version stamps, backlog refs, measured
    transitions) are stripped before counting — see `_CITATION_SHAPE_RES`.

    `check_spelled_out=False` (used by `cmd_check()` for `NARRATIVE_ENTRIES`
    pages only) additionally turns off spelled-out-number matching — see
    `_normalise_numbers`'s second disclosed bound for why."""
    lines = text.splitlines()
    inside = _generated_line_flags(lines, marker_pairs)
    outside_lines = [line for idx, (line, is_in) in enumerate(zip(lines, inside)) if not is_in and idx != 0]
    inside_lines = [line for line, is_in in zip(lines, inside) if is_in]
    outside_numbers = _normalise_numbers(
        _strip_citation_shaped_numbers("\n".join(outside_lines)), include_spelled_out=check_spelled_out
    )
    inside_numbers = _normalise_numbers(
        _strip_citation_shaped_numbers("\n".join(inside_lines)), include_spelled_out=check_spelled_out
    )
    missing = sorted(outside_numbers - inside_numbers, key=lambda s: (len(s), s))
    return [
        f"containment: {display_name} states {number!r} outside a generated fence "
        "with no matching literal inside one (D-06)"
        for number in missing
    ]


# ---------------------------------------------------------------------------
# T-21-19-01: joins docs/gates/VERSION-01.md's narrative citations to live
# `expect(` control names in scripts/check-version-stamps.py, so a renamed
# or removed control id fails THIS page's own claim rather than leaving a
# narrative sentence that merely HAPPENS to be true today (the falsified
# "floored ... in both directions" sentence this plan replaces). Scoped to
# this one page and this one script only — it does not generalise to any
# other NARRATIVE_ENTRIES detail page.
# ---------------------------------------------------------------------------

# A control-id-shaped backticked token: lowercase alphanumerics joined by at
# least one hyphen. Deliberately excludes underscores, dots, slashes and
# parens so file paths, function calls and dotted field names never match.
_BACKTICK_CONTROL_ID_SHAPE_RE = re.compile(r"`([a-z0-9]+(?:-[a-z0-9]+)+)`")


def _extract_control_id_shaped_tokens(text: str) -> set[str]:
    """Every backticked token in `text` shaped like a control id, excluding
    any token that resolves to a real repo path — `scripts/<token>.py` or
    `<token>` existing directly under `REPO_ROOT` — which is what keeps
    script-name and directory-name mentions like `check-version-stamps` and
    `first-principles` out of the set."""
    tokens = set(_BACKTICK_CONTROL_ID_SHAPE_RE.findall(text))
    return {
        token
        for token in tokens
        if not (REPO_ROOT / "scripts" / f"{token}.py").exists()
        and not (REPO_ROOT / token).exists()
    }


def _expect_call_present(token: str, script_text: str) -> bool:
    """True if `script_text` contains an `expect("<token>"` call, tolerating
    the multi-line `expect(\\n    "<token>",` call form this repo's
    self-tests commonly use (a literal substring check would miss every
    multi-line call site)."""
    pattern = re.compile(r'expect\(\s*"' + re.escape(token) + r'"')
    return bool(pattern.search(script_text))


def version01_narrative_problems(
    page_text: str | None = None,
    script_text: str | None = None,
) -> list[str]:
    """Every backticked control-id-shaped token `docs/gates/VERSION-01.md`'s
    hand-written narrative cites must exist as a live `expect(` name in
    `scripts/check-version-stamps.py` — otherwise the page's coverage claim
    can drift from the code silently, exactly as the falsified "floored ...
    in both directions" sentence did. An empty citation set is itself a
    finding: the join must have something to join, not pass vacuously.
    `page_text`/`script_text` default to the real files; a synthetic pair
    drives the vacuity and fabricated-id control arms without touching disk.
    """
    if page_text is None:
        page_text = (REPO_ROOT / "docs/gates/VERSION-01.md").read_text(encoding="utf-8")
    if script_text is None:
        script_text = (REPO_ROOT / "scripts/check-version-stamps.py").read_text(encoding="utf-8")

    lines = page_text.splitlines()
    inside = _generated_line_flags(lines, _ALL_DETAIL_MARKER_PAIRS)
    outside_text = "\n".join(line for line, is_in in zip(lines, inside) if not is_in)
    tokens = _extract_control_id_shaped_tokens(outside_text)

    if not tokens:
        return [
            "version01-narrative-control-ids-live: no backticked control-id-shaped "
            "token found in docs/gates/VERSION-01.md's narrative"
        ]

    return [
        f"version01-narrative-control-ids-live: cited control id {token!r} not "
        "found as a live expect(...) name in scripts/check-version-stamps.py"
        for token in sorted(tokens)
        if not _expect_call_present(token, script_text)
    ]


# ---------------------------------------------------------------------------
# CONF-13: the standing hand-maintained count-literal scanner.
#
# 21-CONF13-BASELINE.md measured the real target (79 scanner-target hits, 15
# legitimate exempt hits) and wrote the exemption taxonomy this section
# implements. Its own job is not to re-measure the baseline — plan 21-08's
# generation already collapsed most of the 250-hit raw surface structurally
# — it is to make the remaining zero (or the residual plan 21-10 inherits)
# STAND: a literal reappearing anywhere in the D-21-E surface set, outside a
# generated fence and outside a named exemption class, must fail `--check`.
# ---------------------------------------------------------------------------


class LiteralHit(NamedTuple):
    """One count-noun-adjacent number literal the scanner detected, before
    exemption attribution. `relpath` is the surface's display name — a
    plain repo-relative path for Markdown, `<script>#__doc__` for a module
    docstring, matching `conf13_sweep.py`'s own labelling."""

    relpath: str
    line: int
    text: str


class LiteralExemptionClass(NamedTuple):
    """One exemption class from 21-CONF13-BASELINE.md's taxonomy: a name, a
    written reason (so a later reviewer can re-derive or dispute the call
    from the artifact, not from memory — the baseline's own discipline), and
    a matcher over one hit's own text. A hit matching no class is a finding,
    never a silently-permitted pass (T-21-09-02)."""

    name: str
    reason: str
    matches: object  # Callable[[str], bool]


# --- vocabulary (verbatim from 21-CONF13-BASELINE.md's conf13_sweep.py) ----

_LITERAL_ONES_1_20 = [
    "one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten",
    "eleven", "twelve", "thirteen", "fourteen", "fifteen", "sixteen", "seventeen",
    "eighteen", "nineteen", "twenty",
]
_LITERAL_ONES_1_9 = _LITERAL_ONES_1_20[:9]
_LITERAL_TENS = ["thirty", "forty", "fifty", "sixty", "seventy", "eighty", "ninety"]

# Count nouns (singular/plural) — the D-21-E vocabulary harvested from
# CLAUDE.md's own QUAL-01/SCAN-GUARD/TRACE-03/CONF-GATE rows, not guessed.
# "call site"/"call sites" is handled as a bigram, separately from this set.
_LITERAL_NOUNS: frozenset[str] = frozenset({
    "branch", "branches", "control", "controls", "arm", "arms", "gate", "gates",
    "row", "rows", "entry", "entries", "fixture", "fixtures", "surface", "surfaces",
    "assertion", "assertions", "check", "checks", "id", "ids", "literal", "literals",
    "stamp", "stamps", "pin", "pins", "job", "jobs", "plan", "plans", "mutation",
    "mutations", "leg", "legs", "criterion", "criteria", "column", "columns",
    "case", "cases", "probe", "probes", "item", "items",
})
_LITERAL_BIGRAM_NOUN_HEAD = "call"
_LITERAL_BIGRAM_NOUN_TAILS = frozenset({"site", "sites"})

_LITERAL_NUM_ATOM_RE = re.compile(
    r"(?:\d{1,4}"
    r"|(?:" + "|".join(sorted([re.escape(w) for w in _LITERAL_TENS], key=len, reverse=True)) + r")"
    r"(?:-(?:" + "|".join(sorted([re.escape(w) for w in _LITERAL_ONES_1_9], key=len, reverse=True)) + r"))?"
    r"|" + "|".join(
        sorted([re.escape(w) for w in (_LITERAL_TENS + _LITERAL_ONES_1_20)], key=len, reverse=True)
    ) + r"|(?:one\s+)?hundred)",
    re.IGNORECASE,
)
_LITERAL_RANGE_SEP = {"to", "→", "->"}

# Ordinal/label nouns: a number immediately AFTER one of these identifies
# WHICH instance, not HOW MANY ("Criterion 4", "Phase 3", "Plan 01") —
# direction-based, so "27 rows" (number-before-noun) is unaffected. Ported
# from the baseline's own second tightening pass, plus "stage" (plan 21-10,
# Task 3): docs/DATA-FLOW.md's five `## Stage N — ...` headings identify
# which stage, not how many, the identical shape "phase"/"step" already
# cover in this same set — measured as a false positive on docs/DATA-FLOW.md
# rather than routed through the deferred-remediation class, since it is a
# genuine detection-time gap, not a budget-driven deferral.
_LITERAL_ORDINAL_ADJACENT_NOUNS = frozenset({
    "criterion", "criteria", "phase", "check", "item", "arm", "row",
    "plan", "leg", "id", "gate", "step", "stage",
})
_LITERAL_EXIT_CODE_PROSE_WORDS = frozenset({"exits", "exit"})
# "Exit codes:" docstring blocks render as "    0  description" — a lone
# leading digit 0/1/2 followed by 2+ spaces then prose; never a count.
_LITERAL_EXIT_CODE_LINE_RE = re.compile(r"^\s*[012]\s{2,}\S")


def _literal_tokenize(line: str) -> list[tuple[int, int, str]]:
    return [(m.start(), m.end(), m.group()) for m in re.finditer(r"\S+", line)]


def _literal_clean(raw: str) -> str:
    return re.sub(r"^[^\w]+|[^\w]+$", "", raw)


def _literal_is_num_atom(clean: str) -> bool:
    if not clean:
        return False
    return bool(re.fullmatch(_LITERAL_NUM_ATOM_RE, clean))


def _literal_is_noun(clean: str) -> bool:
    return clean.lower() in _LITERAL_NOUNS


def _scan_text_for_literal_hits(relpath: str, text: str) -> list[LiteralHit]:
    """Detect count-noun-adjacent number literals (digit form, spelled-out
    form, `up from N`, and two-token range forms), line-scoped — **disclosed
    bound (1)**, inherited from `HEADLINE-LOCK`: a literal hard-wrapped
    across two physical lines is invisible. Ports
    `21-CONF13-BASELINE.md`'s `conf13_sweep.py::scan_text` verbatim,
    including its two measurement-time tightening passes (the exit-code-line
    exclusion, the ordinal/label-adjacency exclusion, and `§`-token
    blanking) — these are DETECTION-time exclusions, not exemption classes:
    they identify text that never made a count claim in the first place, so
    they belong in the scanner (what counts as a candidate hit) rather than
    in `LITERAL_EXEMPTION_CLASSES` (which permits a genuine count claim for a
    named reason)."""
    hits: list[LiteralHit] = []
    lines = text.splitlines()
    for lineno, line in enumerate(lines, start=1):
        if _LITERAL_EXIT_CODE_LINE_RE.match(line):
            continue
        toks = _literal_tokenize(line)
        cleaned = [_literal_clean(t[2]) for t in toks]
        n = len(toks)
        for _si in range(n):
            if toks[_si][2].startswith("§"):
                cleaned[_si] = ""

        for i in range(n - 1):
            if cleaned[i].lower() == "up" and i + 1 < n and cleaned[i + 1].lower() == "from":
                if i + 2 < n and _literal_is_num_atom(cleaned[i + 2]):
                    start = toks[i][0]
                    end = toks[i + 2][1]
                    hits.append(LiteralHit(relpath, lineno, line[start:end]))

        i = 0
        while i < n:
            if not _literal_is_num_atom(cleaned[i]):
                i += 1
                continue
            span_start_idx = i
            span_end_idx = i
            slash_m = re.fullmatch(r"(\d{1,4})/(\d{1,4})", cleaned[i])
            if slash_m:
                span_end_idx = i
            elif i + 2 < n and cleaned[i + 1] in _LITERAL_RANGE_SEP and _literal_is_num_atom(cleaned[i + 2]):
                span_end_idx = i + 2
            elif cleaned[i].lower() == "one" and i + 1 < n and cleaned[i + 1].lower() == "hundred":
                span_end_idx = i + 1

            window_lo = max(0, span_start_idx - 3)
            window_hi = min(n - 1, span_end_idx + 3)

            if (
                span_start_idx - 1 >= 0
                and (
                    cleaned[span_start_idx - 1].lower() in _LITERAL_ORDINAL_ADJACENT_NOUNS
                    or cleaned[span_start_idx - 1].lower() in _LITERAL_EXIT_CODE_PROSE_WORDS
                )
            ):
                i = span_end_idx + 1
                continue

            noun_idx = None
            for j in range(window_lo, window_hi + 1):
                if span_start_idx <= j <= span_end_idx:
                    continue
                if _literal_is_noun(cleaned[j]):
                    noun_idx = j
                    break
                if (
                    cleaned[j].lower() in _LITERAL_BIGRAM_NOUN_TAILS
                    and j - 1 >= 0
                    and cleaned[j - 1].lower() == _LITERAL_BIGRAM_NOUN_HEAD
                ):
                    noun_idx = j
                    break

            if noun_idx is not None:
                lo_idx = min(span_start_idx, noun_idx)
                hi_idx = max(span_end_idx, noun_idx)
                start = toks[lo_idx][0]
                end = toks[hi_idx][1]
                hits.append(LiteralHit(relpath, lineno, line[start:end]))

            i = span_end_idx + 1

    return hits


def _generated_marker_pairs_for(relpath: str) -> tuple[tuple[str, str], ...]:
    """Which GENERATED-fence marker pairs apply to `relpath`, so the
    generated-region discriminator (D-21-D: this scanner lives beside
    `_replace_region`/D-06 precisely so it can reuse this) can tell a
    hand-maintained literal from one inside a fence this same module already
    regenerates. Reuses the existing marker constants — one implementation,
    not a second (the action's own instruction)."""
    if relpath == "CLAUDE.md":
        return (CLAUDE_REGION_MARKERS,)
    if relpath == "docs/ARCHITECTURE.md":
        return (ARCHITECTURE_REGION_MARKERS,)
    if relpath == "docs/TESTING.md":
        return (TESTING_REGION_MARKERS,)
    if relpath.startswith("docs/gates/") and relpath.endswith(".md"):
        return _ALL_DETAIL_MARKER_PAIRS
    return ()


def _literal_hits_outside_generated(relpath: str, text: str) -> list[LiteralHit]:
    """`_scan_text_for_literal_hits`, minus any hit whose line sits inside a
    generated fence for this surface — a literal inside a generated fence is
    not hand-maintained by definition (D-21-D)."""
    all_hits = _scan_text_for_literal_hits(relpath, text)
    marker_pairs = _generated_marker_pairs_for(relpath)
    if not marker_pairs:
        return all_hits
    lines = text.splitlines()
    inside = _generated_line_flags(lines, marker_pairs)
    return [h for h in all_hits if not (1 <= h.line <= len(inside) and inside[h.line - 1])]


# --- exemption taxonomy (21-CONF13-BASELINE.md § Exemption taxonomy) -------


def _match_version_stamp_count(hit: LiteralHit) -> bool:
    return "version stamp" in hit.text.lower()


def _match_retired_body_budget(hit: LiteralHit) -> bool:
    return "644" in hit.text


def _match_plan_number_identifier(hit: LiteralHit) -> bool:
    if not re.search(r"\bplan \d{2}(-\d{2})?\b", hit.text, re.IGNORECASE):
        return False
    return not re.search(r"\b(more|added|split)\b", hit.text, re.IGNORECASE)


_HEADLINE_ROW_DELTA_NUMBERS = ("192", "94", "286", "229", "214", "237", "252", "266")
_HEADLINE_ROW_DELTA_RE = re.compile(
    r"\b(?:" + "|".join(_HEADLINE_ROW_DELTA_NUMBERS) + r")\b.*\brows?\b"
    r"|\brows?\b.*\b(?:" + "|".join(_HEADLINE_ROW_DELTA_NUMBERS) + r")\b",
    re.IGNORECASE,
)


def _match_headline_provenance_delta(hit: LiteralHit) -> bool:
    return bool(_HEADLINE_ROW_DELTA_RE.search(hit.text))


def _match_maxturns_60(hit: LiteralHit) -> bool:
    return bool(re.search(r"maxturns", hit.text, re.IGNORECASE)) and "60" in hit.text


def _match_sha256_digest(hit: LiteralHit) -> bool:
    return bool(re.search(r"sha256", hit.text, re.IGNORECASE))


def _match_commonmark_heading_depth(hit: LiteralHit) -> bool:
    return bool(re.search(r"hash", hit.text, re.IGNORECASE)) and bool(
        re.search(r"\b1\b", hit.text) and re.search(r"\b6\b", hit.text)
    )


# --- deferred-literal-ledger (plan 21-16): enumerated per-hit permit -------
#
# Plan 21-10's whole-surface permit dict (matching on `hit.relpath` alone)
# made every hit on a registered surface permitted regardless of what its
# text said -- including CLAUDE.md,
# docs/ARCHITECTURE.md and docs/TESTING.md, the three surfaces CONF-13
# exists to protect. That structural zero survived a genuinely wrong claim
# this same phase shipped (docs/TESTING.md's "Two gates fire on every
# `git commit`" while both hooks ran five) -- the scanner saw it and
# permitted it (21-VERIFICATION.md GAP 1).
#
# `_DEFERRED_LITERAL_HITS` replaces the whole-surface permit with an
# enumerated per-hit ledger: keyed by `(relpath, normalised_text)` -- the
# EXACT text the scanner captured, whitespace-normalised -- and valued by
# `(backlog_id, occurrences, written_reason)`. A hit whose key is not in
# this dict is a finding regardless of which surface it sits on; a
# ledgered key whose LIVE occurrence count exceeds its pinned `occurrences`
# is also a finding (see literal_scan_problems's occurrence-surplus pass,
# below) -- the same exact sentence copied to a second place is a NEW
# finding, not a free ride on an existing entry.
#
# The 21 primary-surface entries (CLAUDE.md, docs/ARCHITECTURE.md,
# docs/TESTING.md -- 999.42) were adjudicated BY HAND, one at a time: each
# is either a currently-correct hand-maintained fact nothing derives
# (disposition CORRECT-BUT-HAND-MAINTAINED) or a false positive of the
# adjacency heuristic (disposition NOT-A-COUNT -- an enumerated-list
# marker, a per-item ratio statement, or a correct number attached to the
# wrong noun). No STALE literal survived the adjudication; every one that
# was stale was already fixed by plan 21-13 or earlier in this phase. The
# remaining 114 entries (10 docs/gates/*.md narrative pages, 999.40; 12
# `.py#__doc__` module docstrings, 999.41) are pinned MECHANICALLY from the
# live scan, without per-entry adjudication -- a real reduction in what
# this ledger certifies, published as a disclosed bound on
# docs/gates/CONF-SURFACE.md rather than left implicit.
#
# Populated via `--emit-deferred-ledger` (below), never hand-typed -- hand
# transcription of exactly this shape is the defect this plan exists to
# end.
_DEFERRED_LITERAL_HITS: dict[tuple[str, str], tuple[str, int, str]] = {
    ('CLAUDE.md', '(33 controls)'): ('999.42', 1, 'Correct: check-provenance.py --describe reports control_count 33 (live-verified).'),
    ('CLAUDE.md', '(43 controls)'): ('999.42', 1, 'Correct: check-conf-gate.py --describe reports control_count 43 (live-verified).'),
    ('CLAUDE.md', '1. The **sync-drift gate**'): ('999.42', 1, "NOT-A-COUNT: an enumerated-list marker ('1.') the adjacency heuristic mistakes for a count -- it identifies which list item, not how many pre-commit gates exist."),
    ('CLAUDE.md', 'Five gates'): ('999.42', 1, 'Correct: 5 pre-commit gates fire on git commit (sync-drift, conformance generator self-test, conformance-baseline drift, claim-surface generator self-test, claim-surface drift) -- verified against both hook scripts in plan 21-13.'),
    ('CLAUDE.md', 'rows; the 14'): ('999.42', 1, "Correct: 14 v8.25 milestone requirements were registered as matrix rows at Phase 12 / 12-01 -- same headline-provenance narrative as the '23' entry above."),
    ('CLAUDE.md', 'rows; the 15'): ('999.42', 1, "Correct: 15 v8.24 milestone requirements were registered as matrix rows at Phase 6 / D-06 -- same headline-provenance narrative as the '23' entry above."),
    ('CLAUDE.md', 'rows; the 23'): ('999.42', 1, "Correct: 23 v8.18 milestone requirements were registered as matrix rows at Phase 4 / D-05 -- historical provenance narrative for the coverage headline, matching docs/requirements-traceability.md; not caught by the headline-provenance-delta class because 23 is not one of that class's row-delta numbers."),
    ('CLAUDE.md', 'surface now contributes 16'): ('999.42', 1, 'Correct: the skill-stub cross-technique-link surface contributes 16 real links (12 cross-technique + 4 detail.md pointers) as of v8.17.5 -- a structural fact, not derived by any script.'),
    ('CLAUDE.md', 'three surfaces,'): ('999.42', 1, 'Correct: gates run on three surfaces -- CI, the offline battery, and pre-commit -- a structural fact restated at CLAUDE.md:181, not derived by any script.'),
    ('CLAUDE.md', 'two assembly surfaces,'): ('999.42', 1, 'Correct: the assembled agent body and the skill stub are the two assembly surfaces _rewrite_detail_link() adapts a detail-sibling pointer for -- a structural fact, not derived by any script.'),
    ('CLAUDE.md', 'two inline checks'): ('999.42', 1, 'Correct: INVARIANT-CHECK and FROZEN-EVIDENCE are the two inline (non-gate/gate_prereq) battery checks -- a structural fact, not derived by any script.'),
    ('docs/ARCHITECTURE.md', '(five gates'): ('999.42', 1, "Correct: both pre-commit hooks now run 5 gates each -- same fact as 'up from three)' above, second number on the same line."),
    ('docs/ARCHITECTURE.md', '**Two gates'): ('999.42', 1, "NOT-A-COUNT: 'Two gates are called GATE-02' identifies two DIFFERENT gates that share a display name (VAL-04/GATE-02 vs GATE-02-v8.5) -- the number is correct but attached to a disambiguation, not a population count."),
    ('docs/ARCHITECTURE.md', 'five surfaces.'): ('999.42', 1, "Correct: the battery total is restated on five surfaces (CLAUDE.md, docs/ARCHITECTURE.md, docs/TESTING.md, docs/gates/CONF-SURFACE.md, and check-firewall-battery.sh's own tally comment) rather than swept by hand across all of them -- verified by grep across the five files."),
    ('docs/ARCHITECTURE.md', 'one entry'): ('999.42', 1, "NOT-A-COUNT: 'holds one entry per companion-tool slug' states a per-slug cardinality invariant (a ratio), not a population total -- the adjacency heuristic attaches it to the 'entry' noun as though it counted the whole file."),
    ('docs/ARCHITECTURE.md', 'stamps rather than 13.'): ('999.42', 1, "Correct: shared/skills/*/SKILL.md held 13 version stamps before the first-principles-analysis launcher was added (now 14) -- a correct historical count, adjacent to the version-stamp narrative but not caught by the version-stamp-count exemption's literal 'version stamp' substring match."),
    ('docs/ARCHITECTURE.md', 'two unrelated checks.'): ('999.42', 1, "NOT-A-COUNT: same paragraph and same false-positive class as '**Two gates' above -- 'conflates two unrelated checks' names which two, not how many checks exist in total."),
    ('docs/ARCHITECTURE.md', 'up from three)'): ('999.42', 1, 'Correct: both pre-commit hooks moved from 3 to 5 gates each when CONF-SURFACE landed -- verified against both hook scripts in plan 21-13.'),
    ('docs/TESTING.md', 'Five gates'): ('999.42', 1, "Correct: 5 pre-commit gates fire on every git commit -- same verified fact as CLAUDE.md's 'Five gates' entry above."),
    ('docs/TESTING.md', 'five labelled surfaces:'): ('999.42', 1, "Correct: docs/conformance-baseline.md publishes five labelled surfaces (shared-examples, generated-twin, contract-surface, adversarial-corpus, live-conformance) -- verified by reading that file's own ## headers."),
    ('docs/TESTING.md', 'literal `== 4`'): ('999.42', 1, "NOT-A-COUNT: 'literal' here means the constant's literal value as written in code (_COMPOSER_FOCUS_CEILING == 4), not a count of literals -- an adjacency-mistrack false positive on the noun 'literal'."),
    ('docs/gates/CONF-GATE.md', 'four internal predicates (plan'): ('999.40', 1, 'Pinned mechanically from the live literal scan under 999.40 (docs/gates/*.md narrative pages) -- not adjudicated entry-by-entry; see docs/gates/CONF-SURFACE.md for what this group certifies.'),
    ('docs/gates/CONF-GATE.md', 'seven enforcement call sites'): ('999.40', 1, 'Pinned mechanically from the live literal scan under 999.40 (docs/gates/*.md narrative pages) -- not adjudicated entry-by-entry; see docs/gates/CONF-SURFACE.md for what this group certifies.'),
    ('docs/gates/CONF-GATE.md', 'three mutations'): ('999.40', 1, 'Pinned mechanically from the live literal scan under 999.40 (docs/gates/*.md narrative pages) -- not adjudicated entry-by-entry; see docs/gates/CONF-SURFACE.md for what this group certifies.'),
    ('docs/gates/GATE-01.md', 'checks — 8'): ('999.40', 1, 'Pinned mechanically from the live literal scan under 999.40 (docs/gates/*.md narrative pages) -- not adjudicated entry-by-entry; see docs/gates/CONF-SURFACE.md for what this group certifies.'),
    ('docs/gates/HC-BOUND.md', 'surfaces, and all three'): ('999.40', 1, 'Pinned mechanically from the live literal scan under 999.40 (docs/gates/*.md narrative pages) -- not adjudicated entry-by-entry; see docs/gates/CONF-SURFACE.md for what this group certifies.'),
    ('docs/gates/QUAL-01.md', '(2) cross-surface literal'): ('999.40', 1, 'Pinned mechanically from the live literal scan under 999.40 (docs/gates/*.md narrative pages) -- not adjudicated entry-by-entry; see docs/gates/CONF-SURFACE.md for what this group certifies.'),
    ('docs/gates/QUAL-01.md', '(5 call sites:'): ('999.40', 1, 'Pinned mechanically from the live literal scan under 999.40 (docs/gates/*.md narrative pages) -- not adjudicated entry-by-entry; see docs/gates/CONF-SURFACE.md for what this group certifies.'),
    ('docs/gates/QUAL-01.md', '(5) **worked-example conformance** (plan'): ('999.40', 1, 'Pinned mechanically from the live literal scan under 999.40 (docs/gates/*.md narrative pages) -- not adjudicated entry-by-entry; see docs/gates/CONF-SURFACE.md for what this group certifies.'),
    ('docs/gates/QUAL-01.md', '(6 call sites:'): ('999.40', 1, 'Pinned mechanically from the live literal scan under 999.40 (docs/gates/*.md narrative pages) -- not adjudicated entry-by-entry; see docs/gates/CONF-SURFACE.md for what this group certifies.'),
    ('docs/gates/QUAL-01.md', '6 absorbed the Gate'): ('999.40', 1, 'Pinned mechanically from the live literal scan under 999.40 (docs/gates/*.md narrative pages) -- not adjudicated entry-by-entry; see docs/gates/CONF-SURFACE.md for what this group certifies.'),
    ('docs/gates/QUAL-01.md', 'Eleven mutations'): ('999.40', 1, 'Pinned mechanically from the live literal scan under 999.40 (docs/gates/*.md narrative pages) -- not adjudicated entry-by-entry; see docs/gates/CONF-SURFACE.md for what this group certifies.'),
    ('docs/gates/QUAL-01.md', 'arms, plus two'): ('999.40', 1, 'Pinned mechanically from the live literal scan under 999.40 (docs/gates/*.md narrative pages) -- not adjudicated entry-by-entry; see docs/gates/CONF-SURFACE.md for what this group certifies.'),
    ('docs/gates/QUAL-01.md', 'check requires only two'): ('999.40', 1, 'Pinned mechanically from the live literal scan under 999.40 (docs/gates/*.md narrative pages) -- not adjudicated entry-by-entry; see docs/gates/CONF-SURFACE.md for what this group certifies.'),
    ('docs/gates/QUAL-01.md', 'four canonical surfaces'): ('999.40', 1, 'Pinned mechanically from the live literal scan under 999.40 (docs/gates/*.md narrative pages) -- not adjudicated entry-by-entry; see docs/gates/CONF-SURFACE.md for what this group certifies.'),
    ('docs/gates/QUAL-01.md', 'four lettered controls'): ('999.40', 1, 'Pinned mechanically from the live literal scan under 999.40 (docs/gates/*.md narrative pages) -- not adjudicated entry-by-entry; see docs/gates/CONF-SURFACE.md for what this group certifies.'),
    ('docs/gates/QUAL-01.md', 'gate count from 15'): ('999.40', 1, 'Pinned mechanically from the live literal scan under 999.40 (docs/gates/*.md narrative pages) -- not adjudicated entry-by-entry; see docs/gates/CONF-SURFACE.md for what this group certifies.'),
    ('docs/gates/QUAL-01.md', 'legs: (1)'): ('999.40', 1, 'Pinned mechanically from the live literal scan under 999.40 (docs/gates/*.md narrative pages) -- not adjudicated entry-by-entry; see docs/gates/CONF-SURFACE.md for what this group certifies.'),
    ('docs/gates/QUAL-01.md', 'literal reconciliation — twelve'): ('999.40', 1, 'Pinned mechanically from the live literal scan under 999.40 (docs/gates/*.md narrative pages) -- not adjudicated entry-by-entry; see docs/gates/CONF-SURFACE.md for what this group certifies.'),
    ('docs/gates/QUAL-01.md', 'literals on all three'): ('999.40', 1, 'Pinned mechanically from the live literal scan under 999.40 (docs/gates/*.md narrative pages) -- not adjudicated entry-by-entry; see docs/gates/CONF-SURFACE.md for what this group certifies.'),
    ('docs/gates/QUAL-01.md', 'nine `R-CLAIM-*` fixtures'): ('999.40', 1, 'Pinned mechanically from the live literal scan under 999.40 (docs/gates/*.md narrative pages) -- not adjudicated entry-by-entry; see docs/gates/CONF-SURFACE.md for what this group certifies.'),
    ('docs/gates/QUAL-01.md', 'one arm.'): ('999.40', 1, 'Pinned mechanically from the live literal scan under 999.40 (docs/gates/*.md narrative pages) -- not adjudicated entry-by-entry; see docs/gates/CONF-SURFACE.md for what this group certifies.'),
    ('docs/gates/QUAL-01.md', 'one row'): ('999.40', 1, 'Pinned mechanically from the live literal scan under 999.40 (docs/gates/*.md narrative pages) -- not adjudicated entry-by-entry; see docs/gates/CONF-SURFACE.md for what this group certifies.'),
    ('docs/gates/QUAL-01.md', 'pins — three,'): ('999.40', 1, 'Pinned mechanically from the live literal scan under 999.40 (docs/gates/*.md narrative pages) -- not adjudicated entry-by-entry; see docs/gates/CONF-SURFACE.md for what this group certifies.'),
    ('docs/gates/QUAL-01.md', 'sites: 1'): ('999.40', 3, 'Pinned mechanically from the live literal scan under 999.40 (docs/gates/*.md narrative pages) -- not adjudicated entry-by-entry; see docs/gates/CONF-SURFACE.md for what this group certifies.'),
    ('docs/gates/QUAL-01.md', 'six legs.'): ('999.40', 1, 'Pinned mechanically from the live literal scan under 999.40 (docs/gates/*.md narrative pages) -- not adjudicated entry-by-entry; see docs/gates/CONF-SURFACE.md for what this group certifies.'),
    ('docs/gates/QUAL-01.md', 'six separate legs:'): ('999.40', 1, 'Pinned mechanically from the live literal scan under 999.40 (docs/gates/*.md narrative pages) -- not adjudicated entry-by-entry; see docs/gates/CONF-SURFACE.md for what this group certifies.'),
    ('docs/gates/QUAL-01.md', 'surface (three'): ('999.40', 1, 'Pinned mechanically from the live literal scan under 999.40 (docs/gates/*.md narrative pages) -- not adjudicated entry-by-entry; see docs/gates/CONF-SURFACE.md for what this group certifies.'),
    ('docs/gates/QUAL-01.md', 'surface among all four'): ('999.40', 1, 'Pinned mechanically from the live literal scan under 999.40 (docs/gates/*.md narrative pages) -- not adjudicated entry-by-entry; see docs/gates/CONF-SURFACE.md for what this group certifies.'),
    ('docs/gates/QUAL-01.md', 'surfaces declare all twelve);'): ('999.40', 1, 'Pinned mechanically from the live literal scan under 999.40 (docs/gates/*.md narrative pages) -- not adjudicated entry-by-entry; see docs/gates/CONF-SURFACE.md for what this group certifies.'),
    ('docs/gates/QUAL-01.md', 'three independently-neutralization-tested anti-vacuity arms,'): ('999.40', 1, 'Pinned mechanically from the live literal scan under 999.40 (docs/gates/*.md narrative pages) -- not adjudicated entry-by-entry; see docs/gates/CONF-SURFACE.md for what this group certifies.'),
    ('docs/gates/QUAL-01.md', 'two contract surfaces'): ('999.40', 1, 'Pinned mechanically from the live literal scan under 999.40 (docs/gates/*.md narrative pages) -- not adjudicated entry-by-entry; see docs/gates/CONF-SURFACE.md for what this group certifies.'),
    ('docs/gates/QUAL-01.md', 'two new pins'): ('999.40', 1, 'Pinned mechanically from the live literal scan under 999.40 (docs/gates/*.md narrative pages) -- not adjudicated entry-by-entry; see docs/gates/CONF-SURFACE.md for what this group certifies.'),
    ('docs/gates/REG-GUARD.md', 'two surfaces:'): ('999.40', 1, 'Pinned mechanically from the live literal scan under 999.40 (docs/gates/*.md narrative pages) -- not adjudicated entry-by-entry; see docs/gates/CONF-SURFACE.md for what this group certifies.'),
    ('docs/gates/SCAN-GUARD.md', '"Criteria 4 and 6'): ('999.40', 1, 'Pinned mechanically from the live literal scan under 999.40 (docs/gates/*.md narrative pages) -- not adjudicated entry-by-entry; see docs/gates/CONF-SURFACE.md for what this group certifies.'),
    ('docs/gates/SCAN-GUARD.md', '(plan 15-06 split thirty-one'): ('999.40', 1, 'Pinned mechanically from the live literal scan under 999.40 (docs/gates/*.md narrative pages) -- not adjudicated entry-by-entry; see docs/gates/CONF-SURFACE.md for what this group certifies.'),
    ('docs/gates/SCAN-GUARD.md', 'Criteria 4 and 6'): ('999.40', 1, 'Pinned mechanically from the live literal scan under 999.40 (docs/gates/*.md narrative pages) -- not adjudicated entry-by-entry; see docs/gates/CONF-SURFACE.md for what this group certifies.'),
    ('docs/gates/SCAN-GUARD.md', 'Criterion 4 or 6'): ('999.40', 1, 'Pinned mechanically from the live literal scan under 999.40 (docs/gates/*.md narrative pages) -- not adjudicated entry-by-entry; see docs/gates/CONF-SURFACE.md for what this group certifies.'),
    ('docs/gates/SCAN-GUARD.md', "arms, omitting Rubric-2's two."): ('999.40', 1, 'Pinned mechanically from the live literal scan under 999.40 (docs/gates/*.md narrative pages) -- not adjudicated entry-by-entry; see docs/gates/CONF-SURFACE.md for what this group certifies.'),
    ('docs/gates/SCAN-GUARD.md', 'branches to fifty-eight'): ('999.40', 1, 'Pinned mechanically from the live literal scan under 999.40 (docs/gates/*.md narrative pages) -- not adjudicated entry-by-entry; see docs/gates/CONF-SURFACE.md for what this group certifies.'),
    ('docs/gates/SCAN-GUARD.md', 'four branches),'): ('999.40', 1, 'Pinned mechanically from the live literal scan under 999.40 (docs/gates/*.md narrative pages) -- not adjudicated entry-by-entry; see docs/gates/CONF-SURFACE.md for what this group certifies.'),
    ('docs/gates/SCAN-GUARD.md', 'four legs'): ('999.40', 1, 'Pinned mechanically from the live literal scan under 999.40 (docs/gates/*.md narrative pages) -- not adjudicated entry-by-entry; see docs/gates/CONF-SURFACE.md for what this group certifies.'),
    ('docs/gates/SCAN-GUARD.md', 'ids with eight'): ('999.40', 1, 'Pinned mechanically from the live literal scan under 999.40 (docs/gates/*.md narrative pages) -- not adjudicated entry-by-entry; see docs/gates/CONF-SURFACE.md for what this group certifies.'),
    ('docs/gates/SCAN-GUARD.md', 'one arm'): ('999.40', 1, 'Pinned mechanically from the live literal scan under 999.40 (docs/gates/*.md narrative pages) -- not adjudicated entry-by-entry; see docs/gates/CONF-SURFACE.md for what this group certifies.'),
    ('docs/gates/SCAN-GUARD.md', 'one hundred clause-level named branches'): ('999.40', 2, 'Pinned mechanically from the live literal scan under 999.40 (docs/gates/*.md narrative pages) -- not adjudicated entry-by-entry; see docs/gates/CONF-SURFACE.md for what this group certifies.'),
    ('docs/gates/SCAN-GUARD.md', 'one literal'): ('999.40', 1, 'Pinned mechanically from the live literal scan under 999.40 (docs/gates/*.md narrative pages) -- not adjudicated entry-by-entry; see docs/gates/CONF-SURFACE.md for what this group certifies.'),
    ('docs/gates/SCAN-GUARD.md', 'plan 15-07 added fourteen'): ('999.40', 1, 'Pinned mechanically from the live literal scan under 999.40 (docs/gates/*.md narrative pages) -- not adjudicated entry-by-entry; see docs/gates/CONF-SURFACE.md for what this group certifies.'),
    ('docs/gates/SCAN-GUARD.md', 'plan 15-08 added fourteen'): ('999.40', 1, 'Pinned mechanically from the live literal scan under 999.40 (docs/gates/*.md narrative pages) -- not adjudicated entry-by-entry; see docs/gates/CONF-SURFACE.md for what this group certifies.'),
    ('docs/gates/SCAN-GUARD.md', 'plan 15-09 added one'): ('999.40', 1, 'Pinned mechanically from the live literal scan under 999.40 (docs/gates/*.md narrative pages) -- not adjudicated entry-by-entry; see docs/gates/CONF-SURFACE.md for what this group certifies.'),
    ('docs/gates/SCAN-GUARD.md', 'plan 15-12 added six'): ('999.40', 1, 'Pinned mechanically from the live literal scan under 999.40 (docs/gates/*.md narrative pages) -- not adjudicated entry-by-entry; see docs/gates/CONF-SURFACE.md for what this group certifies.'),
    ('docs/gates/SCAN-GUARD.md', 'row claimed, "one'): ('999.40', 1, 'Pinned mechanically from the live literal scan under 999.40 (docs/gates/*.md narrative pages) -- not adjudicated entry-by-entry; see docs/gates/CONF-SURFACE.md for what this group certifies.'),
    ('docs/gates/SCAN-GUARD.md', 'row named only five'): ('999.40', 1, 'Pinned mechanically from the live literal scan under 999.40 (docs/gates/*.md narrative pages) -- not adjudicated entry-by-entry; see docs/gates/CONF-SURFACE.md for what this group certifies.'),
    ('docs/gates/SCAN-GUARD.md', 'surface in one'): ('999.40', 1, 'Pinned mechanically from the live literal scan under 999.40 (docs/gates/*.md narrative pages) -- not adjudicated entry-by-entry; see docs/gates/CONF-SURFACE.md for what this group certifies.'),
    ('docs/gates/SCAN-GUARD.md', 'two branches),'): ('999.40', 1, 'Pinned mechanically from the live literal scan under 999.40 (docs/gates/*.md narrative pages) -- not adjudicated entry-by-entry; see docs/gates/CONF-SURFACE.md for what this group certifies.'),
    ('docs/gates/SCAN-GUARD.md', 'two branches);'): ('999.40', 1, 'Pinned mechanically from the live literal scan under 999.40 (docs/gates/*.md narrative pages) -- not adjudicated entry-by-entry; see docs/gates/CONF-SURFACE.md for what this group certifies.'),
    ('docs/gates/STEP0-08.md', 'two fixture'): ('999.40', 1, 'Pinned mechanically from the live literal scan under 999.40 (docs/gates/*.md narrative pages) -- not adjudicated entry-by-entry; see docs/gates/CONF-SURFACE.md for what this group certifies.'),
    ('docs/gates/TRACE-03.md', 'arms, one'): ('999.40', 1, 'Pinned mechanically from the live literal scan under 999.40 (docs/gates/*.md narrative pages) -- not adjudicated entry-by-entry; see docs/gates/CONF-SURFACE.md for what this group certifies.'),
    ('docs/gates/TRACE-03.md', 'eight named arms,'): ('999.40', 1, 'Pinned mechanically from the live literal scan under 999.40 (docs/gates/*.md narrative pages) -- not adjudicated entry-by-entry; see docs/gates/CONF-SURFACE.md for what this group certifies.'),
    ('docs/gates/TRACE-03.md', 'five named current-fact surfaces'): ('999.40', 1, 'Pinned mechanically from the live literal scan under 999.40 (docs/gates/*.md narrative pages) -- not adjudicated entry-by-entry; see docs/gates/CONF-SURFACE.md for what this group certifies.'),
    ('docs/gates/TRACE-03.md', 'four cases'): ('999.40', 1, 'Pinned mechanically from the live literal scan under 999.40 (docs/gates/*.md narrative pages) -- not adjudicated entry-by-entry; see docs/gates/CONF-SURFACE.md for what this group certifies.'),
    ('docs/gates/TRACE-03.md', 'literal itself: one'): ('999.40', 1, 'Pinned mechanically from the live literal scan under 999.40 (docs/gates/*.md narrative pages) -- not adjudicated entry-by-entry; see docs/gates/CONF-SURFACE.md for what this group certifies.'),
    ('docs/gates/TRACE-03.md', "site (`(m)`'s three"): ('999.40', 1, 'Pinned mechanically from the live literal scan under 999.40 (docs/gates/*.md narrative pages) -- not adjudicated entry-by-entry; see docs/gates/CONF-SURFACE.md for what this group certifies.'),
    ('docs/gates/TRACE-03.md', 'two ARROW arms,'): ('999.40', 1, 'Pinned mechanically from the live literal scan under 999.40 (docs/gates/*.md narrative pages) -- not adjudicated entry-by-entry; see docs/gates/CONF-SURFACE.md for what this group certifies.'),
    ('docs/gates/TRACE-03.md', 'two whole-file cases'): ('999.40', 1, 'Pinned mechanically from the live literal scan under 999.40 (docs/gates/*.md narrative pages) -- not adjudicated entry-by-entry; see docs/gates/CONF-SURFACE.md for what this group certifies.'),
    ('docs/gates/VAL-02.md', 'two gates'): ('999.40', 1, 'Pinned mechanically from the live literal scan under 999.40 (docs/gates/*.md narrative pages) -- not adjudicated entry-by-entry; see docs/gates/CONF-SURFACE.md for what this group certifies.'),
    ('docs/gates/VERSION-01.md', '4 hand-maintained stamp'): ('999.40', 1, 'Pinned mechanically from the live literal scan under 999.40 (docs/gates/*.md narrative pages) -- not adjudicated entry-by-entry; see docs/gates/CONF-SURFACE.md for what this group certifies.'),
    ('docs/gates/VERSION-01.md', "surfaces `collect_stamps()`'s own four"): ('999.40', 1, 'Pinned mechanically from the live literal scan under 999.40 (docs/gates/*.md narrative pages) -- not adjudicated entry-by-entry; see docs/gates/CONF-SURFACE.md for what this group certifies.'),
    ('scripts/check-act-limb.py#__doc__', '2 item'): ('999.41', 1, 'Pinned mechanically from the live literal scan under 999.41 (.py module docstrings) -- not adjudicated entry-by-entry; see docs/gates/CONF-SURFACE.md for what this group certifies.'),
    ('scripts/check-agent.py#__doc__', 'three inline malformed fixtures'): ('999.41', 1, 'Pinned mechanically from the live literal scan under 999.41 (.py module docstrings) -- not adjudicated entry-by-entry; see docs/gates/CONF-SURFACE.md for what this group certifies.'),
    ('scripts/check-conf-gate.py#__doc__', 'gate over the fourteen'): ('999.41', 1, 'Pinned mechanically from the live literal scan under 999.41 (.py module docstrings) -- not adjudicated entry-by-entry; see docs/gates/CONF-SURFACE.md for what this group certifies.'),
    ('scripts/check-conf-gate.py#__doc__', 'surface for the two'): ('999.41', 1, 'Pinned mechanically from the live literal scan under 999.41 (.py module docstrings) -- not adjudicated entry-by-entry; see docs/gates/CONF-SURFACE.md for what this group certifies.'),
    ('scripts/check-conf-gate.py#__doc__', 'two arms'): ('999.41', 1, 'Pinned mechanically from the live literal scan under 999.41 (.py module docstrings) -- not adjudicated entry-by-entry; see docs/gates/CONF-SURFACE.md for what this group certifies.'),
    ('scripts/check-focused-parity.py#__doc__', '2 item'): ('999.41', 1, 'Pinned mechanically from the live literal scan under 999.41 (.py module docstrings) -- not adjudicated entry-by-entry; see docs/gates/CONF-SURFACE.md for what this group certifies.'),
    ('scripts/check-focused-parity.py#__doc__', 'check between the two'): ('999.41', 1, 'Pinned mechanically from the live literal scan under 999.41 (.py module docstrings) -- not adjudicated entry-by-entry; see docs/gates/CONF-SURFACE.md for what this group certifies.'),
    ('scripts/check-links.py#__doc__', 'two newly-extended scan surfaces'): ('999.41', 1, 'Pinned mechanically from the live literal scan under 999.41 (.py module docstrings) -- not adjudicated entry-by-entry; see docs/gates/CONF-SURFACE.md for what this group certifies.'),
    ('scripts/check-loop-closure.py#__doc__', 'gate reads four'): ('999.41', 1, 'Pinned mechanically from the live literal scan under 999.41 (.py module docstrings) -- not adjudicated entry-by-entry; see docs/gates/CONF-SURFACE.md for what this group certifies.'),
    ('scripts/check-provenance.py#__doc__', '2. The literal'): ('999.41', 1, 'Pinned mechanically from the live literal scan under 999.41 (.py module docstrings) -- not adjudicated entry-by-entry; see docs/gates/CONF-SURFACE.md for what this group certifies.'),
    ('scripts/check-provenance.py#__doc__', "4. PROV-04's no-network control"): ('999.41', 1, 'Pinned mechanically from the live literal scan under 999.41 (.py module docstrings) -- not adjudicated entry-by-entry; see docs/gates/CONF-SURFACE.md for what this group certifies.'),
    ('scripts/check-quality-harness.py#__doc__', '[ID] Dispatch exactly one'): ('999.41', 1, 'Pinned mechanically from the live literal scan under 999.41 (.py module docstrings) -- not adjudicated entry-by-entry; see docs/gates/CONF-SURFACE.md for what this group certifies.'),
    ('scripts/check-quality-harness.py#__doc__', 'one tabulated row.'): ('999.41', 1, 'Pinned mechanically from the live literal scan under 999.41 (.py module docstrings) -- not adjudicated entry-by-entry; see docs/gates/CONF-SURFACE.md for what this group certifies.'),
    ('scripts/check-quality-harness.py#__doc__', 'row. Dispatches exactly one'): ('999.41', 1, 'Pinned mechanically from the live literal scan under 999.41 (.py module docstrings) -- not adjudicated entry-by-entry; see docs/gates/CONF-SURFACE.md for what this group certifies.'),
    ('scripts/check-registration.py#__doc__', '29 named, decision-traceable controls'): ('999.41', 1, 'Pinned mechanically from the live literal scan under 999.41 (.py module docstrings) -- not adjudicated entry-by-entry; see docs/gates/CONF-SURFACE.md for what this group certifies.'),
    ('scripts/check-selfaudit-scan.py#__doc__', '(11) **What plan'): ('999.41', 1, 'Pinned mechanically from the live literal scan under 999.41 (.py module docstrings) -- not adjudicated entry-by-entry; see docs/gates/CONF-SURFACE.md for what this group certifies.'),
    ('scripts/check-selfaudit-scan.py#__doc__', '(12) **What plan'): ('999.41', 1, 'Pinned mechanically from the live literal scan under 999.41 (.py module docstrings) -- not adjudicated entry-by-entry; see docs/gates/CONF-SURFACE.md for what this group certifies.'),
    ('scripts/check-selfaudit-scan.py#__doc__', '(9) **What plan'): ('999.41', 1, 'Pinned mechanically from the live literal scan under 999.41 (.py module docstrings) -- not adjudicated entry-by-entry; see docs/gates/CONF-SURFACE.md for what this group certifies.'),
    ('scripts/check-selfaudit-scan.py#__doc__', '(eight ids'): ('999.41', 1, 'Pinned mechanically from the live literal scan under 999.41 (.py module docstrings) -- not adjudicated entry-by-entry; see docs/gates/CONF-SURFACE.md for what this group certifies.'),
    ('scripts/check-selfaudit-scan.py#__doc__', '0 ("All 94 branches'): ('999.41', 1, 'Pinned mechanically from the live literal scan under 999.41 (.py module docstrings) -- not adjudicated entry-by-entry; see docs/gates/CONF-SURFACE.md for what this group certifies.'),
    ('scripts/check-selfaudit-scan.py#__doc__', '17 stamps'): ('999.41', 1, 'Pinned mechanically from the live literal scan under 999.41 (.py module docstrings) -- not adjudicated entry-by-entry; see docs/gates/CONF-SURFACE.md for what this group certifies.'),
    ('scripts/check-selfaudit-scan.py#__doc__', '17 table data rows**'): ('999.41', 1, 'Pinned mechanically from the live literal scan under 999.41 (.py module docstrings) -- not adjudicated entry-by-entry; see docs/gates/CONF-SURFACE.md for what this group certifies.'),
    ('scripts/check-selfaudit-scan.py#__doc__', '2 item'): ('999.41', 1, 'Pinned mechanically from the live literal scan under 999.41 (.py module docstrings) -- not adjudicated entry-by-entry; see docs/gates/CONF-SURFACE.md for what this group certifies.'),
    ('scripts/check-selfaudit-scan.py#__doc__', '94 branches'): ('999.41', 1, 'Pinned mechanically from the live literal scan under 999.41 (.py module docstrings) -- not adjudicated entry-by-entry; see docs/gates/CONF-SURFACE.md for what this group certifies.'),
    ('scripts/check-selfaudit-scan.py#__doc__', 'Criteria 4 and 6'): ('999.41', 1, 'Pinned mechanically from the live literal scan under 999.41 (.py module docstrings) -- not adjudicated entry-by-entry; see docs/gates/CONF-SURFACE.md for what this group certifies.'),
    ('scripts/check-selfaudit-scan.py#__doc__', 'Criteria 4 and 6,'): ('999.41', 1, 'Pinned mechanically from the live literal scan under 999.41 (.py module docstrings) -- not adjudicated entry-by-entry; see docs/gates/CONF-SURFACE.md for what this group certifies.'),
    ('scripts/check-selfaudit-scan.py#__doc__', 'Criterion 4 or 6'): ('999.41', 1, 'Pinned mechanically from the live literal scan under 999.41 (.py module docstrings) -- not adjudicated entry-by-entry; see docs/gates/CONF-SURFACE.md for what this group certifies.'),
    ('scripts/check-selfaudit-scan.py#__doc__', 'eight arms'): ('999.41', 1, 'Pinned mechanically from the live literal scan under 999.41 (.py module docstrings) -- not adjudicated entry-by-entry; see docs/gates/CONF-SURFACE.md for what this group certifies.'),
    ('scripts/check-selfaudit-scan.py#__doc__', 'fixture actually contains, 7'): ('999.41', 1, 'Pinned mechanically from the live literal scan under 999.41 (.py module docstrings) -- not adjudicated entry-by-entry; see docs/gates/CONF-SURFACE.md for what this group certifies.'),
    ('scripts/check-selfaudit-scan.py#__doc__', 'four assertions'): ('999.41', 1, 'Pinned mechanically from the live literal scan under 999.41 (.py module docstrings) -- not adjudicated entry-by-entry; see docs/gates/CONF-SURFACE.md for what this group certifies.'),
    ('scripts/check-selfaudit-scan.py#__doc__', 'literal (nine'): ('999.41', 1, 'Pinned mechanically from the live literal scan under 999.41 (.py module docstrings) -- not adjudicated entry-by-entry; see docs/gates/CONF-SURFACE.md for what this group certifies.'),
    ('scripts/check-selfaudit-scan.py#__doc__', 'literal via the `-1`'): ('999.41', 1, 'Pinned mechanically from the live literal scan under 999.41 (.py module docstrings) -- not adjudicated entry-by-entry; see docs/gates/CONF-SURFACE.md for what this group certifies.'),
    ('scripts/check-selfaudit-scan.py#__doc__', 'literals themselves — two'): ('999.41', 1, 'Pinned mechanically from the live literal scan under 999.41 (.py module docstrings) -- not adjudicated entry-by-entry; see docs/gates/CONF-SURFACE.md for what this group certifies.'),
    ('scripts/check-selfaudit-scan.py#__doc__', 'one arm'): ('999.41', 1, 'Pinned mechanically from the live literal scan under 999.41 (.py module docstrings) -- not adjudicated entry-by-entry; see docs/gates/CONF-SURFACE.md for what this group certifies.'),
    ('scripts/check-selfaudit-scan.py#__doc__', 'one hand-written arm'): ('999.41', 1, 'Pinned mechanically from the live literal scan under 999.41 (.py module docstrings) -- not adjudicated entry-by-entry; see docs/gates/CONF-SURFACE.md for what this group certifies.'),
    ('scripts/check-selfaudit-scan.py#__doc__', 'one row'): ('999.41', 2, 'Pinned mechanically from the live literal scan under 999.41 (.py module docstrings) -- not adjudicated entry-by-entry; see docs/gates/CONF-SURFACE.md for what this group certifies.'),
    ('scripts/check-selfaudit-scan.py#__doc__', 'rows (17'): ('999.41', 1, 'Pinned mechanically from the live literal scan under 999.41 (.py module docstrings) -- not adjudicated entry-by-entry; see docs/gates/CONF-SURFACE.md for what this group certifies.'),
    ('scripts/check-selfaudit-scan.py#__doc__', 'rows (17 / 44)'): ('999.41', 1, 'Pinned mechanically from the live literal scan under 999.41 (.py module docstrings) -- not adjudicated entry-by-entry; see docs/gates/CONF-SURFACE.md for what this group certifies.'),
    ('scripts/check-selfaudit-scan.py#__doc__', 'six now-uncovered ids.'): ('999.41', 1, 'Pinned mechanically from the live literal scan under 999.41 (.py module docstrings) -- not adjudicated entry-by-entry; see docs/gates/CONF-SURFACE.md for what this group certifies.'),
    ('scripts/check-selfaudit-scan.py#__doc__', 'surfaces run TWO'): ('999.41', 1, 'Pinned mechanically from the live literal scan under 999.41 (.py module docstrings) -- not adjudicated entry-by-entry; see docs/gates/CONF-SURFACE.md for what this group certifies.'),
    ('scripts/check-selfaudit-scan.py#__doc__', 'two surfaces'): ('999.41', 1, 'Pinned mechanically from the live literal scan under 999.41 (.py module docstrings) -- not adjudicated entry-by-entry; see docs/gates/CONF-SURFACE.md for what this group certifies.'),
    ('scripts/check-selfaudit-scan.py#__doc__', 'two tables. This gate'): ('999.41', 1, 'Pinned mechanically from the live literal scan under 999.41 (.py module docstrings) -- not adjudicated entry-by-entry; see docs/gates/CONF-SURFACE.md for what this group certifies.'),
    ('scripts/check-step0-emulator.py#__doc__', '1. Fault-injection fixtures'): ('999.41', 1, 'Pinned mechanically from the live literal scan under 999.41 (.py module docstrings) -- not adjudicated entry-by-entry; see docs/gates/CONF-SURFACE.md for what this group certifies.'),
    ('scripts/check-step0-emulator.py#__doc__', '2. Classification fixtures'): ('999.41', 1, 'Pinned mechanically from the live literal scan under 999.41 (.py module docstrings) -- not adjudicated entry-by-entry; see docs/gates/CONF-SURFACE.md for what this group certifies.'),
    ('scripts/check-step0-emulator.py#__doc__', 'TWO fixture'): ('999.41', 1, 'Pinned mechanically from the live literal scan under 999.41 (.py module docstrings) -- not adjudicated entry-by-entry; see docs/gates/CONF-SURFACE.md for what this group certifies.'),
    ('scripts/check-step0-emulator.py#__doc__', 'fixtures (D-05) — four'): ('999.41', 1, 'Pinned mechanically from the live literal scan under 999.41 (.py module docstrings) -- not adjudicated entry-by-entry; see docs/gates/CONF-SURFACE.md for what this group certifies.'),
    ('scripts/check-step0-live.py#__doc__', 'fixture (default: 5)'): ('999.41', 1, 'Pinned mechanically from the live literal scan under 999.41 (.py module docstrings) -- not adjudicated entry-by-entry; see docs/gates/CONF-SURFACE.md for what this group certifies.'),
    ('scripts/check-step0-live.py#__doc__', 'row PASS (default: 3)'): ('999.41', 1, 'Pinned mechanically from the live literal scan under 999.41 (.py module docstrings) -- not adjudicated entry-by-entry; see docs/gates/CONF-SURFACE.md for what this group certifies.'),
}


def _ledger_key_for(hit: LiteralHit) -> tuple[str, str]:
    """The `_DEFERRED_LITERAL_HITS` key for one hit: its relpath paired with
    its whitespace-normalised text -- never a bare relpath (that would be
    the whole-surface permit this ledger replaces)."""
    return (hit.relpath, " ".join(hit.text.split()))


def _match_deferred_ledger(hit: LiteralHit) -> bool:
    """Presence check only -- a matcher sees one hit at a time and cannot
    count occurrences across the whole scan. The occurrence-surplus check
    (a ledgered key whose LIVE count exceeds its pinned figure) runs
    separately, over the full `read.hits`, inside `literal_scan_problems`
    below -- the one place the whole scan is visible."""
    return _ledger_key_for(hit) in _DEFERRED_LITERAL_HITS


def _deferred_ledger_keys_digest(
    ledger: dict[tuple[str, str], tuple[str, int, str]],
) -> str:
    """sha256 over *ledger*'s sorted `(relpath, text)` keys, one key per
    line with a stable `\\x1f` separator between the two components, UTF-8
    encoded. Order-independent (the keys are sorted before hashing) and
    sensitive to any key-set change, including a same-size substitution --
    the case `_DEFERRED_LEDGER_MAX` alone cannot see (plan 21-20 Task 1,
    T-21-20-01)."""
    lines = [f"{relpath}\x1f{text}" for relpath, text in sorted(ledger)]
    blob = "\n".join(lines).encode("utf-8")
    return "sha256:" + hashlib.sha256(blob).hexdigest()


# The ledger's pinned maximum size, as committed by plan 21-16 Task 1 (135
# entries) and turned by plan 21-20 Task 1 into a REPIN OBLIGATION rather
# than free headroom: the ledger may still shrink, but a shrink must
# re-pin `_DEFERRED_LEDGER_MAX` to the new live size in the SAME commit
# that shrinks it, or `literal_ledger_ratchet_problems`'s second predicate
# (below) fails, naming both figures. This is the ONE place in the ledger
# machinery where a hand-typed number is correct: deriving the pin from
# `len(_DEFERRED_LITERAL_HITS)` at runtime would compare the ledger
# against itself, which can never fail -- a tautology, not a ratchet.
# Standing rule, in this repo's own words (the CONTRACT-06 pin discipline,
# `scripts/check-quality-harness.py`): never recompute a pin to make a
# failing check pass.
_DEFERRED_LEDGER_MAX: int = 135


# A sha256 pin over the ledger's sorted `(relpath, text)` key set (plan
# 21-20 Task 1), closing the hole the size pin above cannot see on its
# own: a remove-and-add performed in ONE commit -- one real entry removed,
# a fabricated, never-adjudicated permit added in its place -- leaves
# `live_size == max_size`, so neither the growth nor the shrink predicate
# fires. This digest is the one predicate a same-size substitution cannot
# evade. Same pin idiom `scripts/check-quality-harness.py` already uses
# for its three CONTRACT-06 detector digests: hand-committed, because a
# self-derived digest compares the ledger against itself. Standing rule:
# never recompute this digest to make a failing check pass -- a mismatch
# means the key set changed, and silently recomputing it here is what an
# unadjudicated refill would look like from the outside.
#
# DISCLOSED BOUND: this digest proves the key set changed DELIBERATELY --
# someone edited `_DEFERRED_LITERAL_HITS` and re-ran the pin -- never that
# the change was ADJUDICATED. It cannot tell a genuinely-remediated permit
# apart from a rubber-stamped one; it can only prove the set is not
# drifting silently underneath an unchanged pin.
_DEFERRED_LEDGER_KEYS_DIGEST = (
    "sha256:0a249f6de8c4b520d3e76590cfc6d1b8296497c5cbfef05bd7533d64a0f068bc"
)


def literal_ledger_ratchet_problems(
    ledger: dict[tuple[str, str], tuple[str, int, str]] | None = None,
    max_size: int | None = None,
    keys_digest: str | None = None,
) -> list[str]:
    """Three independent predicates, all evaluated (none short-circuits
    another): (1) `live_size > max_size` is growth, always a finding; (2)
    `live_size < max_size` is an un-repinned shrink -- legal, but
    `_DEFERRED_LEDGER_MAX` must be lowered to the live size in the SAME
    commit, or remediation buys permanent headroom for a future,
    never-adjudicated permit; (3) the live key-set digest not matching the
    pin is the ONLY predicate that closes a same-size substitution -- an
    atomic remove-and-add leaves `live_size == max_size`, so predicates 1
    and 2 alone produce no finding for it. Do not delete predicate 3 as
    redundant with the size checks; it is the one they cannot see.

    Takes the ledger, its pin, and its key-set digest as optional
    parameters (defaulting to the real ones) so the permanent negative-arm
    controls can drive it against synthetic ledger/pin/digest triples
    without touching the module-level constants."""
    if ledger is None:
        ledger = _DEFERRED_LITERAL_HITS
    if max_size is None:
        max_size = _DEFERRED_LEDGER_MAX
    if keys_digest is None:
        keys_digest = _DEFERRED_LEDGER_KEYS_DIGEST
    problems: list[str] = []
    live_size = len(ledger)
    if live_size > max_size:
        problems.append(
            "deferred-literal-ledger ratchet: live ledger size "
            f"{live_size} exceeds the pinned maximum {max_size} -- the "
            "ledger may shrink but must never grow"
        )
    if live_size < max_size:
        problems.append(
            "deferred-literal-ledger ratchet: live ledger size "
            f"{live_size} is below the pinned maximum {max_size} -- lower "
            "_DEFERRED_LEDGER_MAX to the live size in this same commit so "
            "the shrink is locked in and cannot silently refill with a "
            "new, never-adjudicated permit"
        )
    live_digest = _deferred_ledger_keys_digest(ledger)
    if live_digest != keys_digest:
        problems.append(
            "deferred-literal-ledger ratchet: live key-set digest "
            f"{live_digest!r} != pinned {keys_digest!r} -- the ledger's "
            "key set changed; if this is a deliberate, adjudicated "
            "remediation, re-pin _DEFERRED_LEDGER_KEYS_DIGEST to the live "
            "value in this same commit (this digest proves the key set "
            "changed deliberately, never that the change was adjudicated)"
        )
    return problems


def literal_ledger_staleness_problems(
    read: LiteralScanRead,
    ledger: dict[tuple[str, str], tuple[str, int, str]] | None = None,
) -> list[str]:
    """Every ledger key must match at least one live hit. A key matching
    nothing is a finding naming the key -- the ledger cannot silently
    outlive its own findings, which is what actually drives the ratchet
    down: a permitted residual whose underlying prose was fixed must be
    removed from the ledger, not left to rot."""
    if ledger is None:
        ledger = _DEFERRED_LITERAL_HITS
    live_keys = {_ledger_key_for(hit) for hit in read.hits}
    problems: list[str] = []
    for relpath, text in sorted(ledger):
        if (relpath, text) not in live_keys:
            problems.append(
                f"{relpath}: deferred-literal-ledger key no longer matches any "
                f"live hit: '{text}' (remove this ledger entry -- its "
                "underlying prose was likely already fixed)"
            )
    return problems


LITERAL_EXEMPTION_CLASSES: tuple[LiteralExemptionClass, ...] = (
    LiteralExemptionClass(
        "version-stamp-count",
        "The 17 hand-maintained version stamps (VERSION-01's own invariant, "
        "CLAUDE.md's Key invariants) are a legitimate, gate-enforced number — "
        "not a CONF-13 branch count.",
        _match_version_stamp_count,
    ),
    LiteralExemptionClass(
        "headline-provenance-delta",
        "HEADLINE-LOCK's own remit (scripts/check-traceability.py) — the "
        "coverage-headline row-count's historical provenance narrative, "
        "asserted live off build_matrix_rows(), not hand-transcribed.",
        _match_headline_provenance_delta,
    ),
    LiteralExemptionClass(
        "plan-number-identifier",
        "A plan number ('Plan 04 Task 1') is an identifier — it names which "
        "plan, not how many plans exist.",
        _match_plan_number_identifier,
    ),
    LiteralExemptionClass(
        "retired-body-budget",
        "The retired 644-line agent-body budget (TEARDOWN-01) — explicitly "
        "named in the exempt list.",
        _match_retired_body_budget,
    ),
    LiteralExemptionClass(
        "maxturns-60-value",
        "GATE-01's pinned maxTurns value (60) is a gate-enforced structural "
        "invariant, not a hand-maintained branch count.",
        _match_maxturns_60,
    ),
    LiteralExemptionClass(
        "sha256-digest",
        "A CONTRACT-06 sha256 digest names a pinned function body's hash, "
        "not a count.",
        _match_sha256_digest,
    ),
    LiteralExemptionClass(
        "commonmark-heading-depth",
        "CommonMark's 1-6 ATX-heading-depth range is a language-spec fact, "
        "not a hand-maintained branch count.",
        _match_commonmark_heading_depth,
    ),
    LiteralExemptionClass(
        "deferred-literal-ledger",
        "Plan 21-16 replaced the whole-surface permit this class used to "
        "grant with an enumerated per-hit ledger (_DEFERRED_LITERAL_HITS): "
        "each permitted hit is named by its exact (relpath, text) key, a "
        "999.x backlog id, and a pinned occurrence count — see "
        "21-CONF13-BASELINE.md and docs/gates/CONF-SURFACE.md. A hit on a "
        "registered surface that is NOT in the ledger is a finding "
        "regardless of which surface it sits on, and a ledgered key's live "
        "occurrence count exceeding its pinned figure is also a finding.",
        _match_deferred_ledger,
    ),
)


def _literal_hit_exemption(hit: LiteralHit) -> str | None:
    for cls in LITERAL_EXEMPTION_CLASSES:
        if cls.matches(hit):
            return cls.name
    return None


# --- surface set (D-21-E) --------------------------------------------------


def _py_docstring_scan_scripts() -> tuple[str, ...]:
    """The `.py` module-docstring surfaces: every script-backed,
    non-anticipatory registry entry's script relpath, derived from
    `_gate_registry.ENTRIES` itself via the already-existing
    `_expected_harvest_scripts()` — never a second hand-typed list. This is
    what closes `21-CONF13-BASELINE.md`'s own disclosed hand-transcription
    bound ("plan 21-09's standing scanner is expected to derive this set
    programmatically... rather than hand-list it a second time")."""
    return tuple(sorted(_expected_harvest_scripts()))


LITERAL_SCAN_MD_GLOBS: tuple[str, ...] = (
    "CLAUDE.md",                  # the densest single hand-maintained surface (D-21-E)
    "docs/ARCHITECTURE.md",       # the CI-gate-table twin surface (D-02)
    "docs/TESTING.md",            # per-gate narrative, largely folded under D-21-F
    "docs/MEASUREMENT-MAP.md",    # layer-map prose citing gate/branch counts
    "docs/COMPONENT-DIAGRAM.md",  # architecture-diagram prose citing gate counts
    "docs/DATA-FLOW.md",          # data-flow prose citing gate counts
    "docs/README.md",             # changelog-style narrative, historically the noisiest doc
    "docs/gates/*.md",            # the 28 generated detail pages (thin + narrative)
)

# The full D-21-E scanned surface set: the Markdown globs above, plus every
# script-backed registry entry's module docstring, derived (not re-typed).
LITERAL_SCAN_SURFACES: tuple[str, ...] = LITERAL_SCAN_MD_GLOBS + _py_docstring_scan_scripts()


class LiteralScanRead(NamedTuple):
    """Everything one `run_literal_scan()` call actually did: the set of
    relpaths it really opened (`read_relpaths` — never a glob-derived
    substitute), the hits it found, and a named INFO line for every
    registered candidate it declined to open. Mirrors
    `check-traceability.py`'s `HEADLINE-LOCK` read-record shape."""

    read_relpaths: frozenset[str]
    hits: tuple[LiteralHit, ...]
    declined: tuple[str, ...]


def run_literal_scan(surfaces: tuple[str, ...] = LITERAL_SCAN_SURFACES) -> LiteralScanRead:
    """The read loop: open every surface in `surfaces`, scan it for
    candidate literal hits (outside any generated fence), and record which
    relpaths were actually opened. Every candidate the loop declines to
    open — a missing script, a glob matching zero files — is a named INFO
    line, never a silent skip (the property `HEADLINE-LOCK` states for its
    own scan)."""
    read_relpaths: set[str] = set()
    hits: list[LiteralHit] = []
    declined: list[str] = []
    for surface in surfaces:
        if surface.endswith(".py"):
            p = REPO_ROOT / surface
            if not p.is_file():
                declined.append(f"INFO: literal-scan declined to open {surface!r} (script not found)")
                continue
            try:
                src = p.read_text(encoding="utf-8")
                doc = ast.get_docstring(ast.parse(src, filename=str(p)))
            except (OSError, SyntaxError) as exc:
                declined.append(f"INFO: literal-scan declined to open {surface!r} ({exc!r})")
                continue
            read_relpaths.add(surface)
            if doc:
                hits.extend(_literal_hits_outside_generated(f"{surface}#__doc__", doc))
            continue
        if "*" in surface:
            matched = sorted(REPO_ROOT.glob(surface))
            if not matched:
                declined.append(f"INFO: literal-scan glob {surface!r} matched zero files")
            for p in matched:
                if not p.is_file():
                    continue
                rel = p.relative_to(REPO_ROOT).as_posix()
                text = p.read_text(encoding="utf-8")
                read_relpaths.add(rel)
                hits.extend(_literal_hits_outside_generated(rel, text))
            continue
        p = REPO_ROOT / surface
        if not p.is_file():
            declined.append(f"INFO: literal-scan declined to open {surface!r} (not found)")
            continue
        text = p.read_text(encoding="utf-8")
        read_relpaths.add(surface)
        hits.extend(_literal_hits_outside_generated(surface, text))
    return LiteralScanRead(
        read_relpaths=frozenset(read_relpaths), hits=tuple(hits), declined=tuple(declined)
    )


def literal_scan_coverage_floor_problems(
    read: LiteralScanRead, surfaces: tuple[str, ...] = LITERAL_SCAN_SURFACES
) -> list[str]:
    """Every non-glob entry in `surfaces` must have really been opened —
    i.e. present in `read.read_relpaths`. Takes the `LiteralScanRead` record
    itself as its first parameter (asserted by `_control_scan_coverage_floor_signature_locked`),
    never a glob-derived `set[str]`, so a glob-derived substitute is
    unexpressible at this call site — the `HEADLINE-LOCK` block (m)
    discipline: the floor cannot be forged by handing it a set built
    independently of what the read loop actually opened."""
    problems: list[str] = []
    for surface in surfaces:
        if "*" in surface:
            continue
        if surface not in read.read_relpaths:
            problems.append(
                f"literal-scan-coverage: registered surface {surface!r} was never opened "
                "(see the matching INFO line for why)"
            )
    return problems


def literal_scan_problems(read: LiteralScanRead) -> list[str]:
    """One named finding per non-exempt hit, in CONF-13's own wording. A hit
    matching an exemption class is permitted and attributed by name
    (`literal_scan_attributions`); a hit matching none is a finding, never a
    silent pass (T-21-09-02: this is what keeps a catch-all exemption from
    making the whole scanner vacuous).

    Also runs the deferred-literal-ledger's occurrence-surplus check: a
    ledgered key's LIVE count across `read.hits` must not exceed its pinned
    `occurrences` figure — the same exact sentence copied to a second place
    on the same surface is a NEW finding, not a free ride on the existing
    entry. This is done here, over the whole scan, rather than inside
    `_match_deferred_ledger` (plan 21-16 Task 1): a per-hit matcher sees one
    hit at a time and cannot count."""
    problems: list[str] = []
    for hit in read.hits:
        if _literal_hit_exemption(hit) is not None:
            continue
        problems.append(
            f"{hit.relpath}:{hit.line}: hand-maintained count literal '{hit.text}' "
            "(no exemption class matches)"
        )

    live_counts: dict[tuple[str, str], int] = {}
    for hit in read.hits:
        key = _ledger_key_for(hit)
        if key in _DEFERRED_LITERAL_HITS:
            live_counts[key] = live_counts.get(key, 0) + 1
    for key, live_count in sorted(live_counts.items()):
        _backlog_id, pinned_occurrences, _reason = _DEFERRED_LITERAL_HITS[key]
        if live_count > pinned_occurrences:
            relpath, text = key
            problems.append(
                f"{relpath}: deferred-literal-ledger occurrence surplus for "
                f"'{text}': pinned {pinned_occurrences}, live {live_count}"
            )
    return problems


def literal_scan_attributions(read: LiteralScanRead) -> list[str]:
    """Diagnostic companion to `literal_scan_problems`: one line per
    EXEMPT hit, naming the class it was attributed to — so a permitted hit
    is never silent about why it was permitted."""
    lines: list[str] = []
    for hit in read.hits:
        cls_name = _literal_hit_exemption(hit)
        if cls_name is not None:
            lines.append(f"{hit.relpath}:{hit.line}: exempt ({cls_name}): '{hit.text}'")
    return lines


# --- py-docstrings-only blind-spot measurement (plan 21-20 Task 3) --------
#
# The standing scanner's `.py` branch (`run_literal_scan`, above) reads
# exactly the module-level docstring via `ast.get_docstring(ast.parse(src))`
# -- that single call IS the `py-docstrings-only` disclosed bound. A count
# literal sitting in a FUNCTION, async-function, or CLASS docstring is
# structurally invisible to it. `_nonmodule_docstring_hits`, below,
# MEASURES that blind spot's live size without closing it: its hits are
# never fed into `literal_scan_problems`, never added to `--check`'s
# enforced findings, and never change what the standing scanner polices.
#
# Decision of record (not re-derived here on every read): the standing
# scan is NOT widened to cover these docstrings. Widening it would surface
# a very large number of non-module-docstring hits across the registered
# `.py` surfaces -- re-measure live via `describe()`'s
# `literal_scan_nonmodule_docstring_hits` field rather than trusting a
# stale figure in this comment -- and after plan 21-20 Task 1 the
# deferred-literal ledger is BOTH size-pinned and key-digest-locked, so
# absorbing that volume by refilling the ledger is exactly the regression
# Task 1 closes. The bound therefore stays; what changes is that its size
# is now published and derived, not merely asserted in prose.
def _nonmodule_docstring_hits(
    sources: dict[str, str] | None = None,
) -> list[LiteralHit]:
    """Every function-, async-function-, and class-docstring literal hit
    across the registered `.py` surfaces, excluding each module's own
    docstring (already covered by `run_literal_scan`'s `.py` branch).
    Each hit's `relpath` is `<surface>#<qualname>` (a dotted path through
    any enclosing class/function, matching `<script>#__doc__`'s labelling
    shape for the module docstring itself).

    Takes an optional `sources` mapping (relpath -> source text) so a
    control can drive this against synthetic text without touching the
    real tree or the filesystem, mirroring
    `literal_ledger_ratchet_problems`'s parameter-injection shape. Reads
    the real `.py` surfaces in `LITERAL_SCAN_SURFACES` when *sources* is
    omitted."""
    if sources is None:
        sources = {}
        for surface in LITERAL_SCAN_SURFACES:
            if not surface.endswith(".py"):
                continue
            path = REPO_ROOT / surface
            if path.is_file():
                sources[surface] = path.read_text(encoding="utf-8")

    hits: list[LiteralHit] = []

    def _walk(node: ast.AST, surface: str, prefix: str) -> None:
        for child in ast.iter_child_nodes(node):
            if isinstance(child, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                qualname = f"{prefix}{child.name}"
                doc = ast.get_docstring(child)
                if doc:
                    hits.extend(_literal_hits_outside_generated(f"{surface}#{qualname}", doc))
                _walk(child, surface, prefix=f"{qualname}.")
            else:
                _walk(child, surface, prefix)

    for surface, text in sources.items():
        try:
            tree = ast.parse(text, filename=surface)
        except SyntaxError:
            continue
        _walk(tree, surface, prefix="")

    return hits


# This phase's own file's pinned non-module-docstring hit count (plan
# 21-20 Task 3): the file this phase edits, and the file
# `_control_registry_self_test_passes`'s stale "16 controls" docstring
# literal (WR-08, closed by Task 2) actually landed in. Everywhere else
# the blind spot is MEASURED, not enforced (see the comment above); this
# one file additionally carries a two-sided ratchet so a second WR-08
# cannot land here unnoticed -- growth over the pin is a finding, and a
# shrink below it demands the pin be lowered in the same commit, the same
# shape as Task 1's ledger ratchet. Never recompute this pin to make a
# failing check pass; re-pin it only alongside a real docstring edit in
# the same commit.
_SELF_FILE_NONMODULE_DOCSTRING_HITS: int = 30


def nonmodule_docstring_selffile_ratchet_problems(
    live_count: int | None = None,
    pinned_count: int | None = None,
) -> list[str]:
    """Two-sided ratchet over `scripts/gen-gate-docs.py`'s OWN share of the
    py-docstrings-only blind spot: growth over the pin is a finding (a
    second WR-08 landing in the file the first one landed in); a shrink
    below the pin is ALSO a finding, demanding the pin be lowered to the
    live count in the same commit, so a shrink cannot silently buy
    headroom for a later, unnoticed regrowth (the same two-predicate shape
    `literal_ledger_ratchet_problems` uses for the deferred-literal
    ledger's own size pin).

    Takes the live and pinned counts as optional parameters (defaulting
    to the real ones) so the permanent registered controls can drive this
    against synthetic counts without touching the module-level constant."""
    if live_count is None:
        live_count = len(
            [h for h in _nonmodule_docstring_hits() if h.relpath.startswith("scripts/gen-gate-docs.py#")]
        )
    if pinned_count is None:
        pinned_count = _SELF_FILE_NONMODULE_DOCSTRING_HITS
    problems: list[str] = []
    if live_count > pinned_count:
        problems.append(
            "nonmodule-docstring self-file ratchet: scripts/gen-gate-docs.py's live "
            f"non-module-docstring hit count {live_count} exceeds the pinned "
            f"{pinned_count} -- a new hand-maintained count literal landed in a "
            "function/class docstring in this file (the WR-08 shape) and must be "
            "fixed or the pin explicitly raised alongside a written justification"
        )
    if live_count < pinned_count:
        problems.append(
            "nonmodule-docstring self-file ratchet: scripts/gen-gate-docs.py's live "
            f"non-module-docstring hit count {live_count} is below the pinned "
            f"{pinned_count} -- lower _SELF_FILE_NONMODULE_DOCSTRING_HITS to the "
            "live count in this same commit so the shrink is locked in"
        )
    return problems


def _emit_deferred_ledger_backlog_id(relpath: str) -> str:
    """The 999.40/999.41/999.42 classification recorded in
    21-CONF13-BASELINE.md: docs/gates/*.md narrative pages, .py module
    docstrings, or the three peripheral CI-gate-table host surfaces."""
    if relpath.startswith("docs/gates/"):
        return "999.40"
    if relpath in ("CLAUDE.md", "docs/ARCHITECTURE.md", "docs/TESTING.md"):
        return "999.42"
    return "999.41"


def emit_deferred_ledger() -> str:
    """Maintenance-only (`--emit-deferred-ledger`): run the real scanner
    with the deferred-literal-ledger exemption class disabled, so every
    otherwise-non-exempt hit surfaces, then print a `_DEFERRED_LITERAL_HITS`
    literal — sorted deterministically, each entry's backlog id assigned
    from its surface's 999.40/999.41/999.42 classification — to stdout.
    Writes NOTHING to disk; the executor pipes this output into the module
    by hand, rather than hand-typing 135 keys, which is the exact defect
    this plan exists to end. The written reason is left as a TODO for the
    human adjudicator to fill in — this function's job is population, not
    adjudication."""
    classes_without_ledger = tuple(
        c for c in LITERAL_EXEMPTION_CLASSES if c.name != "deferred-literal-ledger"
    )

    def _exemption_without_ledger(hit: LiteralHit) -> str | None:
        for cls in classes_without_ledger:
            if cls.matches(hit):
                return cls.name
        return None

    read = run_literal_scan()
    counts: dict[tuple[str, str], int] = {}
    for hit in read.hits:
        if _exemption_without_ledger(hit) is not None:
            continue
        counts[_ledger_key_for(hit)] = counts.get(_ledger_key_for(hit), 0) + 1

    lines = ["_DEFERRED_LITERAL_HITS: dict[tuple[str, str], tuple[str, int, str]] = {"]
    for (relpath, text), occ in sorted(counts.items()):
        backlog_id = _emit_deferred_ledger_backlog_id(relpath)
        lines.append(
            f"    ({relpath!r}, {text!r}): ({backlog_id!r}, {occ}, "
            '"TODO: written reason"),'
        )
    lines.append("}")
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# generate_all() — the single compute+render entry point (D-21-B interface).
# Called ONCE per --write, TWICE per --check (idempotency), following
# report-conformance.py:2636-2646's "cannot disagree with each other"
# discipline. Nothing is written to disk by THIS plan — 21-08 lands --write.
# ---------------------------------------------------------------------------


def generate_all() -> dict[Path, str]:
    # Phase 21-14 (T-21-14-02): a duplicate page slug must fail here, before
    # any target is written, rather than silently overwriting one entry's
    # detail page via the `targets` dict below.
    _assert_no_slug_collisions(_gate_registry.ENTRIES)

    # Harvest EVERY script-backed entry, including CONF-SURFACE itself
    # (D-21-C/D-21-K): `_ANTICIPATORY_KEYS` — now empty, plan 21-11 landed
    # CONF-SURFACE's battery/CI registration — exists purely as a mechanism
    # for a FUTURE anticipatory entry to exclude itself from the D-01
    # battery-id floor and the live table row count while not yet
    # battery/CI-registered; it never excludes a script from actually
    # running its own `--describe`.
    by_script, _harvest_problems = harvest(_gate_registry.ENTRIES)

    rows = _gate_table_rows(_gate_registry.ENTRIES, by_script)
    targets: dict[Path, str] = {}

    claude_text = CLAUDE_MD.read_text(encoding="utf-8")
    claude_region = render_table_region(rows, "CLAUDE_MD")
    targets[CLAUDE_MD] = _replace_or_bootstrap_region(
        claude_text,
        CLAUDE_REGION_MARKERS[0],
        CLAUDE_REGION_MARKERS[1],
        claude_region,
        _CLAUDE_BOOTSTRAP_AFTER,
        _CLAUDE_BOOTSTRAP_BEFORE,
    )

    architecture_text = ARCHITECTURE_MD.read_text(encoding="utf-8")
    architecture_region = render_table_region(rows, "ARCHITECTURE_MD")
    targets[ARCHITECTURE_MD] = _replace_or_bootstrap_region(
        architecture_text,
        ARCHITECTURE_REGION_MARKERS[0],
        ARCHITECTURE_REGION_MARKERS[1],
        architecture_region,
        _ARCHITECTURE_BOOTSTRAP_AFTER,
        _ARCHITECTURE_BOOTSTRAP_BEFORE,
    )

    # D-21-F: docs/TESTING.md's third generated target — a per-gate index
    # covering every registry entry, replacing the 13 hand-maintained `###`
    # per-gate sections that only covered 13 of 28.
    testing_text = TESTING_MD.read_text(encoding="utf-8")
    testing_region = render_testing_index_region(_gate_registry.ENTRIES)
    targets[TESTING_MD] = _replace_or_bootstrap_region(
        testing_text,
        TESTING_REGION_MARKERS[0],
        TESTING_REGION_MARKERS[1],
        testing_region,
        _TESTING_BOOTSTRAP_AFTER,
        _TESTING_BOOTSTRAP_BEFORE,
    )

    # D-08: every registry entry — including CONF-SURFACE itself — gets a
    # docs/gates/<GATE-ID>.md page.
    for entry in _gate_registry.ENTRIES:
        page_path = DETAIL_PAGE_DIR / f"{_page_slug(entry)}.md"
        existing_text = page_path.read_text(encoding="utf-8") if page_path.exists() else None
        blob = by_script.get(entry.script) if entry.script else None
        targets[page_path] = render_detail_page(entry, blob, existing_text)

    return targets


# ---------------------------------------------------------------------------
# _replace_region: the region-replacement primitive (Task 2)
# ---------------------------------------------------------------------------


class RegionMarkerError(ValueError):
    """Raised by `_replace_region` on any malformed-marker shape (T-21-06-01):
    a marker occurring zero times, two-or-more times, or an end marker
    positioned before the start marker. Named, never a silent skip — the
    failure mode here is silent corruption of a project-instruction file."""


# A CommonMark fenced-code-block delimiter: up to three leading spaces, then
# three-or-more backticks or tildes, then the info string. Copied (not
# imported) from `scripts/check-quality-harness.py`'s `_FENCE_DELIM_RE` —
# that file's `_slice_sections` is CONTRACT-06 pinned and must not be
# imported or edited by this module.
_FENCE_DELIM_RE = re.compile(r"^ {0,3}(?P<fence>`{3,}|~{3,})(?P<info>.*)$")


def _fenced_line_flags(bare_lines: list[str]) -> list[bool]:
    """Per (already-terminator-stripped) line: is it inside — or itself — a
    CommonMark-fenced code block?

    Reimplements (does not import) `check-quality-harness.py`'s
    `_fenced_code_flags` closing-rule discipline: a fence closes only on the
    SAME delimiter character, at least as long as the opener, and carrying
    no info string of its own on the closer; a backtick opener may not have
    a backtick in its own info string. An unterminated fence runs to end of
    input. A naive parity toggle gets this wrong on a legal `~~~` block
    quoting an unclosed ``` example — this repo already shipped that exact
    bug once in `_slice_sections`; this function does not reinvent it.
    """
    inside = [False] * len(bare_lines)
    open_char: str | None = None
    open_len = 0
    for i, bare in enumerate(bare_lines):
        m = _FENCE_DELIM_RE.match(bare)
        if open_char is None:
            if m is not None:
                char = m.group("fence")[0]
                if not (char == "`" and "`" in m.group("info")):
                    open_char, open_len = char, len(m.group("fence"))
                    inside[i] = True
            continue
        inside[i] = True
        if (
            m is not None
            and m.group("fence")[0] == open_char
            and len(m.group("fence")) >= open_len
            and not m.group("info").strip()
        ):
            open_char, open_len = None, 0
    return inside


def _replace_region(
    text: str, start_marker: str, end_marker: str, new_content: str
) -> str:
    """Replace exactly the span from `start_marker`'s line through
    `end_marker`'s line, inclusive, leaving every other byte identical.

    Marker matching is on the WHOLE LINE (the marker string must equal a
    line's content, its own line terminator stripped) and ignores matches
    inside a CommonMark-fenced code block, so a marker string appearing in a
    fenced example (as `docs/gates/*.md` pages documenting this very
    mechanism will contain) is not treated as a real marker.

    Raises `RegionMarkerError`, naming the marker text and the observed
    count, when either marker's real (non-fenced) line-count is not exactly
    1, or when the end marker's line precedes the start marker's line —
    there is no best-effort branch and no silent skip.

    Every byte outside the replaced span — including the file's final
    newline (or lack of one) and any CRLF present — is preserved exactly.
    Inside the span, `new_content` is inserted between fresh copies of both
    markers using this repo's LF convention (CLAUDE.md's `newline='\\n'`
    mandate), except the end marker's own trailing terminator, which is
    reused from the original so a file with no final newline stays that
    way.
    """
    lines = text.splitlines(keepends=True)
    bare_lines = [ln.splitlines()[0] if ln.splitlines() else ln for ln in lines]
    fenced = _fenced_line_flags(bare_lines)

    def _find(marker: str) -> list[int]:
        return [
            i
            for i, (bare, is_fenced) in enumerate(zip(bare_lines, fenced))
            if not is_fenced and bare == marker
        ]

    start_idxs = _find(start_marker)
    if len(start_idxs) != 1:
        raise RegionMarkerError(
            f"start marker {start_marker!r}: found {len(start_idxs)} "
            "occurrence(s) outside fenced code blocks (expected exactly 1)"
        )
    end_idxs = _find(end_marker)
    if len(end_idxs) != 1:
        raise RegionMarkerError(
            f"end marker {end_marker!r}: found {len(end_idxs)} occurrence(s) "
            "outside fenced code blocks (expected exactly 1)"
        )
    start_idx, end_idx = start_idxs[0], end_idxs[0]
    if end_idx < start_idx:
        raise RegionMarkerError(
            f"end marker {end_marker!r} (line {end_idx}) precedes start "
            f"marker {start_marker!r} (line {start_idx})"
        )

    prefix = "".join(lines[:start_idx])
    suffix = "".join(lines[end_idx + 1 :])
    end_terminator = lines[end_idx][len(bare_lines[end_idx]) :]

    body = new_content
    if body and not body.endswith("\n"):
        body += "\n"
    span = f"{start_marker}\n{body}{end_marker}{end_terminator}"
    return prefix + span + suffix


# ---------------------------------------------------------------------------
# CLI: cmd_write / cmd_check / self_test / describe / main
# ---------------------------------------------------------------------------


def cmd_write() -> int:
    targets = generate_all()
    for path, content in targets.items():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8", newline="\n")
    print(f"wrote {len(targets)} file(s)")
    return 0


def cmd_check() -> int:
    """Idempotency self-check (sync-content.py's Pitfall-7 discipline), then
    the harvest + all four floors, then an on-disk drift diff.

    Exit 2 distinguishes a non-deterministic generator from a drifted tree
    (T-21-06-04) — a generator that disagrees with itself must never send a
    developer chasing a `--write` that can't converge.
    """
    pass1 = generate_all()
    pass2 = generate_all()
    if pass1 != pass2:
        sys.stderr.write("NON-DETERMINISTIC: pass-1 != pass-2\n")
        for k in pass1.keys() | pass2.keys():
            if pass1.get(k) != pass2.get(k):
                try:
                    rel = k.relative_to(REPO_ROOT)
                except ValueError:
                    rel = k
                sys.stderr.write(f"  differs: {rel}\n")
        return 2

    # See generate_all()'s matching comment: harvest EVERY script-backed
    # entry, including CONF-SURFACE itself (plan 21-11 landed it — no longer
    # anticipatory), so its own detail page's Facts fence gets real
    # `--describe`-derived counts.
    by_script, harvest_problems = harvest(_gate_registry.ENTRIES)
    battery_text = BATTERY_PATH.read_text(encoding="utf-8")
    registry_ids = _gate_registry._registry_entry_ids()
    battery_ids = frozenset(_gate_registry.battery_gate_ids(battery_text))
    precommit_ids = _gate_registry._registry_precommit_ids()
    requested = _gate_registry._requested_fields_by_script()
    emitted_fields = {script: frozenset(blob.keys()) for script, blob in by_script.items()}
    specs = frozen_pathspecs(battery_text)

    problems: list[str] = list(harvest_problems)
    problems += all_floor_problems(
        registry_ids,
        battery_ids,
        precommit_ids,
        requested,
        emitted_fields,
        list(pass1.keys()),
        specs,
    )

    expected_scripts = _expected_harvest_scripts()
    harvested_expected = len(set(by_script) & expected_scripts)
    print(
        f"harvested {harvested_expected}/{len(expected_scripts)} expected script-backed "
        f"entries ({len(by_script)} total)"
    )
    missing_scripts = expected_scripts - set(by_script)
    if missing_scripts:
        problems.append(
            "cmd_check: harvested "
            f"{len(by_script)} of {len(expected_scripts)} expected script-backed "
            f"entries — missing: {sorted(missing_scripts)} (T-21-06-05)"
        )

    # D-06: containment floor over every generated docs/gates/*.md page —
    # a number stated outside a generated fence must also appear inside one
    # on the same page.
    for path, generated in pass1.items():
        if DETAIL_PAGE_DIR in path.parents:
            try:
                rel = path.relative_to(REPO_ROOT)
            except ValueError:
                rel = path
            # `path.stem` equals `_page_slug(entry)`, which equals
            # `entry.key` for every NARRATIVE_ENTRIES member (none of the
            # four carry a `:` requiring the slug rewrite) — see
            # `_normalise_numbers`'s second disclosed bound for why
            # spelled-out matching is off for these four pages only.
            check_spelled_out = path.stem not in NARRATIVE_ENTRIES
            problems += detail_page_containment_problems(
                str(rel), generated, check_spelled_out=check_spelled_out
            )

    # CONF-13: the standing hand-maintained count-literal scanner, run over
    # the real on-disk D-21-E surface set (not `pass1`'s in-memory content —
    # this scanner protects the actual repo state, the same target
    # HEADLINE-LOCK's own live leg reads).
    literal_read = run_literal_scan()
    for info_line in literal_read.declined:
        print(info_line)
    problems += literal_scan_coverage_floor_problems(literal_read)
    literal_findings = literal_scan_problems(literal_read)
    if literal_findings:
        print(f"literal-scan: {len(literal_findings)} non-exempt hit(s) found")
    problems += literal_findings

    # plan 21-16 Task 2: the ledger's ratchet and staleness floors, evaluated
    # alongside the scan findings above and never short-circuited, so one
    # cannot mask the other.
    problems += literal_ledger_ratchet_problems()
    problems += literal_ledger_staleness_problems(literal_read)

    # plan 21-20 Task 3: this phase's own file's two-sided ratchet over its
    # share of the (deliberately unwidened) py-docstrings-only blind spot.
    problems += nonmodule_docstring_selffile_ratchet_problems()

    if problems:
        for p in problems:
            sys.stderr.write(p + "\n")
        return 1

    drifted: list[Path] = []
    for path, generated in pass1.items():
        on_disk = path.read_text(encoding="utf-8") if path.exists() else ""
        if on_disk != generated:
            drifted.append(path)
            rel = path.relative_to(REPO_ROOT)
            sys.stderr.write(f"DRIFT: {rel}\n")
            sys.stderr.writelines(
                difflib.unified_diff(
                    on_disk.splitlines(keepends=True),
                    generated.splitlines(keepends=True),
                    fromfile=f"a/{rel}",
                    tofile=f"b/{rel}",
                    n=3,
                )
            )
            sys.stderr.write("\n")
    if drifted:
        sys.stderr.write("Run: python3 scripts/gen-gate-docs.py --write && git add -u\n")
        return 1
    return 0


# Short, stable identifiers naming CONF-13's own disclosed bounds (D-21-E's
# `disclosed_bounds_anchors` shape) — so `docs/gates/CONF-SURFACE.md` can
# enumerate them from a derived list rather than restating their prose a
# second time. Order matches the numbered list in the plan's own action and
# in the page's narrative below.
LITERAL_SCAN_DISCLOSED_BOUNDS: tuple[str, ...] = (
    "line-scoped-detection",
    "currency-not-correctness",
    "closed-spelled-out-vocabulary",
    "py-docstrings-only",
    "enumerated-per-hit-ledger",
    "ledger-repin-and-key-digest",
    "non-primary-entries-pinned-mechanically",
)


def describe() -> dict:
    """CONF-SURFACE's own self-description (D-21-C: "a generator that cannot
    describe itself would be the first exception to D-08's uniformity in
    the same phase that establishes it"). Runs the real literal scan (a
    read-only operation over the live tree) so the emitted counts are
    genuinely `--describe`-derived, matching every other gate's own
    `derived_counts`/`checked_files` discipline, rather than pure module
    constants alone."""
    literal_read = run_literal_scan()
    exempt_counts: dict[str, int] = {cls.name: 0 for cls in LITERAL_EXEMPTION_CLASSES}
    for hit in literal_read.hits:
        cls_name = _literal_hit_exemption(hit)
        if cls_name is not None:
            exempt_counts[cls_name] += 1
    non_exempt_count = len(literal_scan_problems(literal_read))
    # 999.42 (the three primary surfaces) is the one backlog id adjudicated
    # BY HAND, entry by entry; 999.40/999.41 are pinned MECHANICALLY,
    # without per-entry adjudication (plan 21-16 Task 1). Computed from the
    # ledger's own backlog ids, never hand-counted, so this figure moves
    # with the ledger rather than going stale beside it.
    ledger_adjudicated = sum(
        1 for (_bid, _occ, _reason) in _DEFERRED_LITERAL_HITS.values() if _bid == "999.42"
    )
    ledger_mechanical = len(_DEFERRED_LITERAL_HITS) - ledger_adjudicated
    # The py-docstrings-only blind spot's own live size (plan 21-20 Task
    # 3): a MEASUREMENT, never fed back into `non_exempt_count` or any
    # `--check` finding -- see `_nonmodule_docstring_hits`'s own comment
    # for why the standing scan is not widened to cover it.
    nonmodule_hits = _nonmodule_docstring_hits()
    nonmodule_surfaces = {h.relpath.split("#", 1)[0] for h in nonmodule_hits}
    derived_counts = {
        "literal_scan_surfaces": len(LITERAL_SCAN_SURFACES),
        "literal_scan_read_files": len(literal_read.read_relpaths),
        "literal_scan_hits": len(literal_read.hits),
        "literal_scan_non_exempt": non_exempt_count,
        "literal_scan_ledger_entries": len(_DEFERRED_LITERAL_HITS),
        "literal_scan_ledger_max": _DEFERRED_LEDGER_MAX,
        "literal_scan_ledger_adjudicated": ledger_adjudicated,
        "literal_scan_ledger_mechanical": ledger_mechanical,
        "literal_scan_nonmodule_docstring_hits": len(nonmodule_hits),
        "literal_scan_nonmodule_docstring_surfaces": len(nonmodule_surfaces),
    }
    for cls_name, count in exempt_counts.items():
        derived_counts[f"literal_scan_exempt_{cls_name}"] = count
    return {
        "control_ids": sorted(_CONTROL_IDS),
        "control_count": len(_CONTROL_IDS),
        "locked_constants": {
            "generated_marker": GENERATED_MARKER,
            "generated_end_marker": GENERATED_END_MARKER,
        },
        "registered_surfaces": sorted(LITERAL_SCAN_SURFACES),
        "checked_files": sorted(literal_read.read_relpaths),
        "derived_counts": derived_counts,
        "disclosed_bounds_anchors": list(LITERAL_SCAN_DISCLOSED_BOUNDS),
    }


# ---------------------------------------------------------------------------
# --self-test: _CONTROLS / _CONTROL_IDS / self_test() house style
# (scripts/report-conformance.py:5226-5361's shape)
# ---------------------------------------------------------------------------


def _control_harvest_nonzero_exit_named() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        bad = Path(tmp) / "bad_exit.py"
        bad.write_text("import sys\nsys.exit(1)\n", encoding="utf-8")
        by_script, problems = harvest([_HarvestEntry(script=str(bad))])
        assert by_script == {}, by_script
        assert len(problems) == 1, problems
        assert "bad_exit.py" in problems[0], problems


def _control_harvest_malformed_json_named() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        bad = Path(tmp) / "bad_json.py"
        bad.write_text("print('not json')\n", encoding="utf-8")
        by_script, problems = harvest([_HarvestEntry(script=str(bad))])
        assert by_script == {}, by_script
        assert len(problems) == 1, problems
        assert "bad_json.py" in problems[0], problems


def _control_harvest_one_bad_does_not_abort() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        good = Path(tmp) / "good_one.py"
        good.write_text(
            "import json\nprint(json.dumps({'control_count': 3}))\n",
            encoding="utf-8",
        )
        bad = Path(tmp) / "bad_one.py"
        bad.write_text("import sys\nsys.exit(1)\n", encoding="utf-8")
        by_script, problems = harvest(
            [_HarvestEntry(script=str(good)), _HarvestEntry(script=str(bad))]
        )
        assert len(problems) == 1, problems
        assert str(good) in by_script, by_script
        assert by_script[str(good)] == {"control_count": 3}, by_script


def _control_floors_run_together() -> None:
    registry_ids = frozenset({"REAL-ONE"})
    battery_ids = frozenset(
        _gate_registry.battery_gate_ids(
            'gate "REAL-ONE" "x" "true"\ngate "MISSING-ONE" "x" "true"\n'
        )
    )
    requested = {"scripts/x.py": frozenset({"branch_count"})}
    emitted: dict[str, frozenset[str]] = {"scripts/x.py": frozenset()}
    problems = all_floor_problems(
        registry_ids, battery_ids, frozenset(), requested, emitted, [], ()
    )
    assert len(problems) == 2, problems
    joined = " ".join(problems)
    assert "MISSING-ONE" in joined, problems
    assert "branch_count" in joined, problems


def _control_frozen_path_write_fires() -> None:
    write_target = REPO_ROOT / "tests" / "adversarial-corpus-v9.0" / "bogus.md"
    problems = frozen_path_write_problems(
        [write_target], ("tests/adversarial-corpus-v9.0",)
    )
    assert len(problems) == 1, problems
    assert "tests/adversarial-corpus-v9.0" in problems[0], problems


def _control_frozen_paths_derived_not_typed() -> None:
    battery_text = BATTERY_PATH.read_text(encoding="utf-8")
    derived = frozen_pathspecs(battery_text)
    match = _FROZEN_PATHS_ARRAY_RE.search(battery_text)
    assert match is not None, "could not locate _FROZEN_PATHS in the live battery script"
    body_lines = [ln.strip() for ln in match.group(1).splitlines() if ln.strip()]
    independent = tuple(
        ln[1:-1] for ln in body_lines if ln.startswith("'") and ln.endswith("'")
    )
    assert derived == independent, (derived, independent)
    assert len(derived) > 0, "frozen_pathspecs derived zero entries from the live battery script"


def _control_check_dispatch_wired() -> None:
    """Phase-152 WR-01 precedent: drive `main(["--check"])` itself
    in-process against the real tree, proving the CLI dispatch is wired —
    not just `cmd_check()` called directly.

    As of plan 21-08's landed `--write` (Task 1), this must return 0 (no
    drift): CLAUDE.md, docs/ARCHITECTURE.md and every docs/gates/*.md page
    now carry the generator's real output on disk, so a byte-reproducible
    `--write` leaves nothing for `--check` to flag. This control previously
    (plan 21-07, before the first real `--write` landed) asserted rc == 1
    for the opposite reason — the generated content necessarily differed
    from the pre-existing hand-maintained text. Both assertions describe
    the SAME invariant (`--check`'s rc reflects genuine drift against
    whatever is actually on disk) at two different, correctly-identified
    points in the migration; this is not a weakening of the control.

    Plan 21-09 (CONF-13) adds a third legitimate reason for rc == 1: a
    residual, named literal-scan finding (never drift). This control
    asserts on the reason (no `DRIFT:` line ever; a `literal-scan:` line iff
    rc == 1), matching `_control_page_check_dispatch_wired`'s own widening
    below, so it stays correct on either side of plan 21-10's remediation."""
    stdout_buf, stderr_buf = io.StringIO(), io.StringIO()
    with contextlib.redirect_stdout(stdout_buf), contextlib.redirect_stderr(stderr_buf):
        rc = main(["--check"])
    stdout_text, stderr_text = stdout_buf.getvalue(), stderr_buf.getvalue()
    assert "DRIFT:" not in stderr_text, stderr_text
    assert rc in (0, 1), f"main(['--check']) returned {rc}, expected 0 or 1 against the live tree"
    if rc == 1:
        assert "literal-scan:" in stdout_text, (
            "expected the exit-1 to be the CONF-13 residual, not drift/floor "
            "problems: " + stdout_text + stderr_text
        )


def _control_nondeterminism_exit_2() -> None:
    original = _this_module.generate_all
    calls = {"n": 0}

    def _flaky() -> dict[Path, str]:
        calls["n"] += 1
        return {Path("/tmp/gen-gate-docs-fixture-target.md"): f"call-{calls['n']}"}

    try:
        _this_module.generate_all = _flaky
        rc = cmd_check()
        assert rc == 2, f"cmd_check() returned {rc}, expected 2 for a non-deterministic generator"
    finally:
        _this_module.generate_all = original


def _control_region_happy_path() -> None:
    text = "before\nSTART\nold body\nEND\nafter\n"
    result = _replace_region(text, "START", "END", "new body\n")
    assert result == "before\nSTART\nnew body\nEND\nafter\n", result


def _control_region_zero_start_raises() -> None:
    text = "before\nEND\nafter\n"
    try:
        _replace_region(text, "START", "END", "x\n")
        raise AssertionError("expected RegionMarkerError")
    except RegionMarkerError as exc:
        assert "START" in str(exc) and " 0 " in str(exc), str(exc)


def _control_region_zero_end_raises() -> None:
    text = "before\nSTART\nafter\n"
    try:
        _replace_region(text, "START", "END", "x\n")
        raise AssertionError("expected RegionMarkerError")
    except RegionMarkerError as exc:
        assert "END" in str(exc) and " 0 " in str(exc), str(exc)


def _control_region_duplicate_start_raises() -> None:
    text = "START\nmid\nSTART\nEND\n"
    try:
        _replace_region(text, "START", "END", "x\n")
        raise AssertionError("expected RegionMarkerError")
    except RegionMarkerError as exc:
        assert " 2 " in str(exc), str(exc)


def _control_region_duplicate_end_raises() -> None:
    text = "START\nEND\nmid\nEND\n"
    try:
        _replace_region(text, "START", "END", "x\n")
        raise AssertionError("expected RegionMarkerError")
    except RegionMarkerError as exc:
        assert " 2 " in str(exc), str(exc)


def _control_region_end_before_start_raises() -> None:
    text = "END\nmid\nSTART\n"
    try:
        _replace_region(text, "START", "END", "x\n")
        raise AssertionError("expected RegionMarkerError")
    except RegionMarkerError as exc:
        assert "precedes" in str(exc), str(exc)


def _control_region_marker_in_fence_ignored() -> None:
    # Two invariants must BOTH hold, or this control cannot discriminate
    # which one broke: whole-line anchoring (line 0 CONTAINS "START" as a
    # substring but does not EQUAL it — a substring search would wrongly
    # count it) and fence exclusion (the fenced "START" line equals the
    # marker exactly but must not count either). Only the real, non-fenced,
    # exact-match "START" line may be the start marker.
    text = (
        "See the START region below for an example.\n"
        "```\n"
        "START\n"
        "```\n"
        "START\n"
        "old\n"
        "END\n"
        "after\n"
    )
    result = _replace_region(text, "START", "END", "new\n")
    assert result.startswith(
        "See the START region below for an example.\n```\nSTART\n```\n"
    ), result
    assert result.endswith("START\nnew\nEND\nafter\n"), result


def _control_region_tilde_fence_quoting_backticks() -> None:
    # ~~~ ... ~~~ quotes an UNCLOSED ``` fence inside it. A parity toggle
    # inverts on the unclosed ``` and treats the real START (outside both
    # fences) as still "inside a fence" — CommonMark closing rules do not.
    text = "~~~\n```\nSTART\n```\n~~~\nSTART\nold\nEND\n"
    result = _replace_region(text, "START", "END", "new\n")
    assert result.startswith("~~~\n```\nSTART\n```\n~~~\n"), result
    assert result.endswith("START\nnew\nEND\n"), result


def _control_region_preserves_final_newline() -> None:
    text = "before\nSTART\nold\nEND"  # no trailing newline
    result = _replace_region(text, "START", "END", "new\n")
    assert result == "before\nSTART\nnew\nEND", result


def _control_region_preserves_crlf() -> None:
    text = "before\r\nSTART\r\nold\r\nEND\r\nafter\r\n"
    result = _replace_region(text, "START", "END", "new\n")
    assert result.startswith("before\r\nSTART\n"), result
    assert result.endswith("END\r\nafter\r\n"), result


def _control_real_file_claude_md_region() -> None:
    """A real-file control (Task 2): wrap the live CLAUDE.md's own
    "### CI gates" subsection with synthetic markers in memory only, call
    `_replace_region`, and assert everything before the heading and
    everything after the subsection is byte-identical to the untouched
    file. Nothing is written to disk."""
    text = (REPO_ROOT / "CLAUDE.md").read_text(encoding="utf-8")
    lines = text.splitlines(keepends=True)
    bare = [ln.splitlines()[0] if ln.splitlines() else ln for ln in lines]
    heading_idx = next(i for i, b in enumerate(bare) if b.strip() == "### CI gates")
    end_idx = next(
        i
        for i in range(heading_idx + 1, len(bare))
        if bare[i].startswith("## ") or bare[i].startswith("### ")
    )
    start_marker = "<!-- TEST-REGION-START -->"
    end_marker = "<!-- TEST-REGION-END -->"
    synthetic_lines = (
        lines[:heading_idx]
        + [start_marker + "\n"]
        + lines[heading_idx:end_idx]
        + [end_marker + "\n"]
        + lines[end_idx:]
    )
    synthetic_text = "".join(synthetic_lines)
    result = _replace_region(synthetic_text, start_marker, end_marker, "NEW CONTENT\n")
    prefix_original = "".join(lines[:heading_idx])
    suffix_original = "".join(lines[end_idx:])
    assert result.startswith(prefix_original), "prefix diverged from live CLAUDE.md bytes"
    assert result.endswith(suffix_original), "suffix diverged from live CLAUDE.md bytes"


def _control_describe_emits_parseable_json() -> None:
    blob = describe()
    encoded = json.dumps(blob, indent=2, sort_keys=True)
    decoded = json.loads(encoded)
    assert decoded == blob, "describe() output did not round-trip through JSON"


# ---------------------------------------------------------------------------
# Task 1 controls: the shared row renderer and the two table regions
# ---------------------------------------------------------------------------


def _control_one_renderer_two_surfaces() -> None:
    entries = [e for e in _gate_registry.ENTRIES if e.key not in _gate_registry._ANTICIPATORY_KEYS][:5]
    rows = _gate_table_rows(entries, {})
    claude_table = render_gate_table(rows)
    architecture_table = render_gate_table(rows)
    assert claude_table == architecture_table, "the same rows must render byte-identically"


def _control_gates_link_resolves_per_surface() -> None:
    """`render_table_region()`'s two calls emit the SAME row data
    (`_control_one_renderer_two_surfaces` proves that), but the two surfaces
    sit at different directory depths (`CLAUDE.md` at the repo root,
    `docs/ARCHITECTURE.md` one level inside `docs/`), so a single link
    target string cannot resolve correctly from both. This asserts the
    surface-specific rewrite (`_rewrite_gates_link_for_architecture`) makes
    both resolve, simulating each surface's own directory as the resolution
    base — exactly the defect a raw byte-identity check on the FULL rendered
    region cannot see, since it would incorrectly demand the same string in
    both places."""
    entries = [e for e in _gate_registry.ENTRIES if e.key not in _gate_registry._ANTICIPATORY_KEYS][:3]
    rows = _gate_table_rows(entries, {})
    claude_region = render_table_region(rows, "CLAUDE_MD")
    architecture_region = render_table_region(rows, "ARCHITECTURE_MD")
    link_re = re.compile(r"\]\(([^)]+\.md)\)")
    claude_targets = link_re.findall(claude_region)
    architecture_targets = link_re.findall(architecture_region)
    assert claude_targets, "no docs/gates links found in the CLAUDE_MD region"
    assert len(claude_targets) == len(architecture_targets)
    for target in claude_targets:
        assert target.startswith("docs/gates/"), target
        # Simulated resolution base: CLAUDE.md sits at the repo root, so a
        # relative target is resolved directly against REPO_ROOT.
        assert (REPO_ROOT / target).exists(), f"CLAUDE_MD target does not resolve: {target}"
    for target in architecture_targets:
        assert target.startswith("gates/"), target
        assert not target.startswith("docs/gates/"), target
        # Simulated resolution base: docs/ARCHITECTURE.md sits one directory
        # level inside docs/, so a relative target is resolved against
        # REPO_ROOT / "docs".
        assert (REPO_ROOT / "docs" / target).exists(), (
            f"ARCHITECTURE_MD target does not resolve: {target}"
        )
    # Anti-vacuity: the un-rewritten form must not survive into the
    # ARCHITECTURE_MD rendering.
    assert "](docs/gates/" not in architecture_region


def _control_row_count_equals_entries() -> None:
    rows = _gate_table_rows(_gate_registry.ENTRIES, {})
    table = render_gate_table(rows)
    lines = table.splitlines()
    data_rows = [ln for ln in lines[2:] if ln.strip()]
    documented = [
        e for e in _gate_registry.ENTRIES if e.key not in _gate_registry._ANTICIPATORY_KEYS
    ]
    assert len(data_rows) == len(documented), (len(data_rows), len(documented))


def _control_no_row_wrapped() -> None:
    rows = _gate_table_rows(_gate_registry.ENTRIES, {})
    table = render_gate_table(rows)
    for line in table.splitlines():
        assert line.startswith("|") and line.endswith("|"), line
    documented = [
        e for e in _gate_registry.ENTRIES if e.key not in _gate_registry._ANTICIPATORY_KEYS
    ]
    assert len(table.splitlines()) == 2 + len(documented)


def _control_testing_index_row_count_equals_entries() -> None:
    """docs/TESTING.md's index (D-21-F) covers EVERY registry entry —
    unlike the two CI-gate tables, it does not exclude the anticipatory
    CONF-SURFACE member, since D-08 already gives every entry a page and the
    plan's own acceptance criterion asserts `len(ENTRIES)` rows verbatim."""
    region = render_testing_index_region(_gate_registry.ENTRIES)
    table_lines = [ln for ln in region.splitlines() if ln.startswith("|")]
    data_rows = table_lines[2:]
    assert len(data_rows) == len(_gate_registry.ENTRIES), (
        len(data_rows), len(_gate_registry.ENTRIES)
    )


def _control_testing_index_links_resolve() -> None:
    """Every `docs/gates/<slug>.md` link the TESTING.md index renders must
    resolve BOTH from the repo root (the canonical target string) and from
    `docs/` (the rewritten, docs-relative target actually written to
    disk) — the same directory-depth property
    `_control_gates_link_resolves_per_surface` proves for the two CI-gate
    tables, applied to the third generated target."""
    region = render_testing_index_region(_gate_registry.ENTRIES)
    link_re = re.compile(r"\]\(([^)]+\.md)\)")
    targets = link_re.findall(region)
    assert len(targets) == len(_gate_registry.ENTRIES), (len(targets), len(_gate_registry.ENTRIES))
    for target in targets:
        assert target.startswith("gates/"), target
        assert not target.startswith("docs/gates/"), target
        assert (REPO_ROOT / "docs" / target).exists(), f"TESTING_MD target does not resolve: {target}"


def _control_testing_real_file_region() -> None:
    """A real-file control (Task 1), mirroring
    `_control_real_file_claude_md_region`: wrap the live docs/TESTING.md's
    own "## CI gates — operational run-detail" span with synthetic markers
    in memory only, call `_replace_region`, and assert everything before and
    after the span is byte-identical to the untouched file. Nothing is
    written to disk."""
    text = TESTING_MD.read_text(encoding="utf-8")
    lines = text.splitlines(keepends=True)
    bare = [ln.splitlines()[0] if ln.splitlines() else ln for ln in lines]
    heading_idx = next(
        i for i, b in enumerate(bare) if b.strip() == "## CI gates — operational run-detail"
    )
    end_idx = next(
        i for i in range(heading_idx + 1, len(bare))
        if bare[i].startswith("## ")
    )
    start_marker = "<!-- TEST-REGION-START -->"
    end_marker = "<!-- TEST-REGION-END -->"
    synthetic_lines = (
        lines[:heading_idx + 1]
        + [start_marker + "\n"]
        + lines[heading_idx + 1:end_idx]
        + [end_marker + "\n"]
        + lines[end_idx:]
    )
    synthetic_text = "".join(synthetic_lines)
    result = _replace_region(synthetic_text, start_marker, end_marker, "NEW CONTENT\n")
    prefix_original = "".join(lines[:heading_idx + 1])
    suffix_original = "".join(lines[end_idx:])
    assert result.startswith(prefix_original), "prefix diverged from live docs/TESTING.md bytes"
    assert result.endswith(suffix_original), "suffix diverged from live docs/TESTING.md bytes"


def _control_trace03_glob_substring_derived() -> None:
    entry = next(e for e in _gate_registry.ENTRIES if e.key == "TRACE-03")
    synthetic_blob = {"scan_globs": ["a/*.md", "B.md"]}
    rows = _gate_table_rows([entry], {entry.script: synthetic_blob})
    table = render_gate_table(rows)
    assert "`a/*.md`, `B.md`" in table, table

    by_script, harvest_problems = harvest([entry])
    assert not harvest_problems, harvest_problems
    live_rows = _gate_table_rows([entry], by_script)
    live_table = render_gate_table(live_rows)
    live_globs = by_script[entry.script]["scan_globs"]
    assert _glob_prose(live_globs) in live_table, live_table
    expected = "`docs/*.md`, `CLAUDE.md`, `CHANGELOG.md`, `README.md`"
    assert expected in live_table, live_table


def _control_population_arithmetic_derived() -> None:
    base = list(_gate_registry.ENTRIES)
    before = _population_counts(base)
    synthetic = _gate_registry.GateEntry(
        key="SYN-TEST",
        gate_id="SYN-TEST",
        extra_ids=(),
        mechanism="`syn-job` (CI)",
        ci_job="syn-job",
        script=None,
        run_command="true",
        summary="Synthetic entry for the population-arithmetic control.",
    )
    after = _population_counts(base + [synthetic])
    assert after["ci_count"] == before["ci_count"] + 1, (before, after)
    assert after["tallied_count"] == before["tallied_count"] + 1, (before, after)
    assert after["precommit_count"] == before["precommit_count"], (before, after)
    assert after["inline_count"] == before["inline_count"], (before, after)
    sentence_before = _population_arithmetic_sentence(base)
    sentence_after = _population_arithmetic_sentence(base + [synthetic])
    assert sentence_before != sentence_after, "adding a synthetic entry did not move the sentence"
    assert str(before["ci_count"]) in sentence_before, sentence_before
    assert str(after["ci_count"]) in sentence_after, sentence_after
    assert str(before["tallied_count"]) in sentence_before, sentence_before
    assert str(after["tallied_count"]) in sentence_after, sentence_after

    # CR-04: a SIXTH synthetic `PRECOMMIT:` row must move precommit_count
    # (and only precommit_count) — proving the figure is derived from the
    # PRECOMMIT: roster and not from anything else, the same isolation
    # discipline the ci_count/tallied_count assertions above already give
    # the pre-existing synthetic entry.
    synthetic_precommit = _gate_registry.GateEntry(
        key="PRECOMMIT:syn-test-gate",
        gate_id=None,
        extra_ids=(),
        mechanism="synthetic pre-commit gate for the population-arithmetic control",
        ci_job=None,
        script=None,
        run_command="true",
        summary="Synthetic PRECOMMIT: entry for the population-arithmetic control.",
    )
    after_precommit = _population_counts(base + [synthetic_precommit])
    assert after_precommit["precommit_count"] == before["precommit_count"] + 1, (
        before,
        after_precommit,
    )
    assert after_precommit["ci_count"] == before["ci_count"], (before, after_precommit)
    assert after_precommit["tallied_count"] == before["tallied_count"], (
        before,
        after_precommit,
    )
    assert after_precommit["inline_count"] == before["inline_count"], (
        before,
        after_precommit,
    )
    sentence_precommit_after = _population_arithmetic_sentence(base + [synthetic_precommit])
    assert str(after_precommit["precommit_count"]) in sentence_precommit_after, (
        sentence_precommit_after
    )


def _control_arithmetic_sentence_names_gates_not_hooks() -> None:
    """CR-04's noun-disambiguation control: the rendered sentence must state
    the pre-commit clause as GATES (`pre-commit gates`), never the ambiguous
    `pre-commit** hooks` shape that made the original figure unfalsifiable —
    a reader could not tell whether "2 pre-commit" meant hooks or gates, so
    neither value could be called wrong."""
    sentence = _population_arithmetic_sentence(_gate_registry.ENTRIES)
    assert "pre-commit gates" in sentence, sentence
    assert "pre-commit** hooks" not in sentence, sentence


def _control_hook_mechanism_count_independent_of_precommit_count() -> None:
    """`hook_mechanism_count` and `precommit_count` must be computed by
    DIFFERENT code paths: mutating the synthetic entries list (adding a
    PRECOMMIT: row) must move precommit_count without moving
    hook_mechanism_count. If they moved together, one derivation would be
    doing both jobs and the CR-04 disambiguation would be cosmetic."""
    base = list(_gate_registry.ENTRIES)
    before = _population_counts(base)
    synthetic_precommit = _gate_registry.GateEntry(
        key="PRECOMMIT:syn-test-gate-2",
        gate_id=None,
        extra_ids=(),
        mechanism="synthetic pre-commit gate for the independence control",
        ci_job=None,
        script=None,
        run_command="true",
        summary="Synthetic PRECOMMIT: entry for the independence control.",
    )
    after = _population_counts(base + [synthetic_precommit])
    assert after["precommit_count"] != before["precommit_count"], (before, after)
    assert after["hook_mechanism_count"] == before["hook_mechanism_count"], (before, after)


def _control_arithmetic_sentence_pluralizes_correctly() -> None:
    """The population-arithmetic sentence must never render the literal
    parenthetical-plural shape `gate(s)`/`check(s)` — a template artifact
    a reader would notice on a surface whose whole purpose is readability
    (found live at v9.0.0: the shipped sentence read "1 battery-only
    gate(s) plus 2 inline check(s)"). Checks both the correct singular and
    plural forms render, and that the wrong form never does, for each of
    the two counted nouns independently."""
    assert _pluralize_count(1, "battery-only gate") == "1 battery-only gate"
    assert _pluralize_count(0, "battery-only gate") == "0 battery-only gates"
    assert _pluralize_count(2, "battery-only gate") == "2 battery-only gates"
    assert _pluralize_count(1, "inline check") == "1 inline check"
    assert _pluralize_count(0, "inline check") == "0 inline checks"
    assert _pluralize_count(2, "inline check") == "2 inline checks"
    sentence = _population_arithmetic_sentence(_gate_registry.ENTRIES)
    assert "gate(s)" not in sentence, sentence
    assert "check(s)" not in sentence, sentence
    c = _population_counts(_gate_registry.ENTRIES)
    assert _pluralize_count(c["battery_only_count"], "battery-only gate") in sentence, sentence
    assert _pluralize_count(c["inline_count"], "inline check") in sentence, sentence


def _control_framing_sentences_replaced() -> None:
    rows = _gate_table_rows(_gate_registry.ENTRIES, {})
    for surface in ("CLAUDE_MD", "ARCHITECTURE_MD"):
        region = render_table_region(rows, surface)
        assert "keeps its own operational copy by design" not in region, (surface, region)
        assert "Every other document links here rather than restating it" not in region, (
            surface,
            region,
        )
        assert _POST_UNIFICATION_STATEMENT in region, (surface, region)


def _control_region_preserves_surrounding_prose() -> None:
    original = CLAUDE_MD.read_text(encoding="utf-8")
    generated = generate_all()[CLAUDE_MD]
    heading_line = "### CI gates\n"
    idx = original.index(heading_line) + len(heading_line)
    prefix_original = original[:idx]
    assert generated.startswith(prefix_original), "CLAUDE.md prefix (through heading) diverged"
    idx2 = original.index(_CLAUDE_BOOTSTRAP_BEFORE)
    suffix_original = original[idx2:]
    assert generated.endswith(suffix_original), "CLAUDE.md suffix (registration history onward) diverged"


# ---------------------------------------------------------------------------
# Task 2 controls: docs/gates/<GATE-ID>.md detail-page renderer
# ---------------------------------------------------------------------------


def _control_page_per_entry() -> None:
    targets = generate_all()
    page_paths = {p for p in targets if DETAIL_PAGE_DIR in p.parents}
    expected = {DETAIL_PAGE_DIR / f"{_page_slug(e)}.md" for e in _gate_registry.ENTRIES}
    assert page_paths == expected, page_paths.symmetric_difference(expected)
    assert CLAUDE_MD in targets and ARCHITECTURE_MD in targets and TESTING_MD in targets, (
        targets.keys()
    )
    assert len(targets) == len(expected) + 3, (len(targets), len(expected))


def _control_narrative_preserved_across_regeneration() -> None:
    entry = _gate_registry.GateEntry(
        key="QUAL-01",
        gate_id="QUAL-01",
        extra_ids=(),
        mechanism="x",
        ci_job=None,
        script="scripts/fake.py",
        run_command="python3 scripts/fake.py --self-test",
        summary="Fake gate for testing.",
        consumes=("control_count",),
    )
    existing = "\n".join(
        [
            f"# {entry.key}: test gate",
            "",
            DETAIL_FACTS_MARKERS[0],
            "## Facts",
            "",
            "- `control_count`: `10`",
            DETAIL_FACTS_MARKERS[1],
            "",
            DETAIL_HOWTORUN_MARKERS[0],
            "## How to run",
            "",
            "```sh",
            "python3 scripts/fake.py --self-test",
            "```",
            "",
            "CI job: — (not a CI job)",
            DETAIL_HOWTORUN_MARKERS[1],
            "",
            "## Disclosed bounds",
            "",
            _DISCLOSED_BOUNDS_HAND_WRITTEN_COMMENT,
            "",
            "HAND-WRITTEN NARRATIVE PARAGRAPH — do not touch.",
        ]
    ) + "\n"
    blob_v2 = {"control_count": 99}
    page_v2 = render_detail_page(entry, blob_v2, existing)
    assert "HAND-WRITTEN NARRATIVE PARAGRAPH" in page_v2, page_v2
    assert "`control_count`: `99`" in page_v2, page_v2
    assert "`control_count`: `10`" not in page_v2, page_v2
    page_v3 = render_detail_page(entry, blob_v2, page_v2)
    assert page_v3 == page_v2, "regeneration is not idempotent"


def _control_thin_page_fully_generated() -> None:
    # REG-GUARD is still thin (D-08) after plan 21-10 moved 11 formerly-thin
    # entries (VAL-01/02/03/04/05, VERSION-01, DUAL-04, GATE-01, BATT-06,
    # STEP0-08, STEP0-06) into NARRATIVE_ENTRIES — this control needs a gate
    # id that stays outside that set.
    entry = next(e for e in _gate_registry.ENTRIES if e.key == "REG-GUARD")
    assert entry.key not in NARRATIVE_ENTRIES, entry.key
    page = render_detail_page(entry, None, None)
    assert "HAND-WRITTEN" not in page, page
    assert "Disclosed bounds" not in page, page


def _control_containment_violation_fires() -> None:
    text = (
        "# Page\n\nthere are 47 controls\n\n"
        f"{DETAIL_FACTS_MARKERS[0]}\nsome fact\n{DETAIL_FACTS_MARKERS[1]}\n"
    )
    problems = detail_page_containment_problems("test.md", text)
    assert len(problems) == 1, problems
    assert "'47'" in problems[0], problems


def _control_containment_satisfied_passes() -> None:
    text = (
        "# Page\n\nthere are 47 controls\n\n"
        f"{DETAIL_FACTS_MARKERS[0]}\ncontrol_count: 47\n{DETAIL_FACTS_MARKERS[1]}\n"
    )
    problems = detail_page_containment_problems("test.md", text)
    assert problems == [], problems


def _control_containment_spelled_out_normalised() -> None:
    text_pass = (
        "# Page\n\nforty-seven controls\n\n"
        f"{DETAIL_FACTS_MARKERS[0]}\ncontrol_count: 47\n{DETAIL_FACTS_MARKERS[1]}\n"
    )
    assert detail_page_containment_problems("t.md", text_pass) == []
    text_fail = (
        "# Page\n\nforty-seven controls\n\n"
        f"{DETAIL_FACTS_MARKERS[0]}\ncontrol_count: 48\n{DETAIL_FACTS_MARKERS[1]}\n"
    )
    problems = detail_page_containment_problems("t.md", text_fail)
    assert len(problems) == 1, problems
    assert "'47'" in problems[0], problems


def _control_version01_narrative_control_ids_live() -> None:
    """T-21-19-01: the real docs/gates/VERSION-01.md narrative's cited
    control ids are all live `expect(` names in check-version-stamps.py,
    plus three synthetic arms proving the join is not vacuous: an empty
    citation set is itself a finding, a fabricated id is named, and a real
    id produces nothing."""
    assert version01_narrative_problems() == [], version01_narrative_problems()

    empty_problems = version01_narrative_problems(
        page_text="# VERSION-01\n\nNo control ids cited here.\n",
        script_text='def x():\n    expect("some-other-id", True)\n',
    )
    assert len(empty_problems) == 1, empty_problems
    assert "no backticked" in empty_problems[0].lower(), empty_problems

    fabricated_problems = version01_narrative_problems(
        page_text="# VERSION-01\n\nSee `kind-roster-nonexistent-arm` for detail.\n",
        script_text='def x():\n    expect("some-other-id", True)\n',
    )
    assert len(fabricated_problems) == 1, fabricated_problems
    assert "kind-roster-nonexistent-arm" in fabricated_problems[0], fabricated_problems

    real_problems = version01_narrative_problems(
        page_text="# VERSION-01\n\nSee `kind-roster-matches-walked` for detail.\n",
        script_text='def x():\n    expect("kind-roster-matches-walked", True)\n',
    )
    assert real_problems == [], real_problems


def _control_page_check_dispatch_wired() -> None:
    """Live leg: `generate_all()` always computes len(ENTRIES) + 3 targets
    (every docs/gates/*.md page plus the three surface files — CLAUDE.md,
    docs/ARCHITECTURE.md, docs/TESTING.md, the last added by plan 21-10's
    D-21-F fold), regardless of whether `--write` has landed. As of plan
    21-08's Task 1 `--write`, every one of those pages now exists on disk
    with byte-reproducible content, so `main(["--check"])` against the real
    tree reports zero drift (rc == 0). Before that `--write` landed (plan
    21-07), the same assertion read the opposite way — rc == 1, because the
    pages did not exist yet. Both readings describe the SAME invariant
    (`--check`'s rc tracks genuine drift against whatever is really on disk)
    at the two different points in the migration where this control was
    exercised.

    Plan 21-09 (CONF-13) wires a THIRD source of `--check` failure: the
    standing literal-count scanner. The live tree still carries the
    baseline's residual scanner-target hits at this plan's own completion
    (plan 21-10's job to close), so `main(["--check"])` may legitimately
    return 1 for that reason alone — never for drift. This control asserts
    the REASON, not just the exit code, so it stays correct on either side
    of plan 21-10's remediation: zero `DRIFT:` lines always, and a
    `literal-scan:` line present if and only if the exit code is 1."""
    targets = generate_all()
    assert len(targets) == len(_gate_registry.ENTRIES) + 3, len(targets)
    for path in targets:
        if DETAIL_PAGE_DIR in path.parents:
            assert path.exists(), f"{path} unexpectedly missing from disk"
    stdout_buf, stderr_buf = io.StringIO(), io.StringIO()
    with contextlib.redirect_stdout(stdout_buf), contextlib.redirect_stderr(stderr_buf):
        rc = main(["--check"])
    stdout_text, stderr_text = stdout_buf.getvalue(), stderr_buf.getvalue()
    assert "DRIFT:" not in stderr_text, stderr_text
    assert rc in (0, 1), f"main(['--check']) returned {rc}, expected 0 or 1"
    if rc == 0:
        assert "literal-scan:" not in stdout_text, stdout_text
    else:
        assert "literal-scan:" in stdout_text, (
            "expected the exit-1 to be the CONF-13 residual, not drift/floor "
            "problems: " + stdout_text + stderr_text
        )


# ---------------------------------------------------------------------------
# Task 1 controls: the CONF-13 standing literal scanner
# ---------------------------------------------------------------------------


def _control_scan_hit_outside_fence_fires() -> None:
    text = "There are 47 controls in this fixture.\n"
    hits = tuple(_literal_hits_outside_generated("fixture.md", text))
    read = LiteralScanRead(read_relpaths=frozenset({"fixture.md"}), hits=hits, declined=())
    problems = literal_scan_problems(read)
    assert len(problems) == 1, problems
    assert "fixture.md:1" in problems[0], problems
    assert "47" in problems[0], problems


def _control_scan_hit_inside_fence_passes() -> None:
    text = (
        f"{CLAUDE_REGION_MARKERS[0]}\n"
        "There are 47 controls in this fixture.\n"
        f"{CLAUDE_REGION_MARKERS[1]}\n"
    )
    hits = _literal_hits_outside_generated("CLAUDE.md", text)
    assert hits == [], hits


def _control_scan_exempt_class_attributed() -> None:
    text = "There are 17 version stamps tracked here.\n"
    hits = _literal_hits_outside_generated("fixture.md", text)
    assert len(hits) == 1, hits
    read = LiteralScanRead(read_relpaths=frozenset({"fixture.md"}), hits=tuple(hits), declined=())
    assert literal_scan_problems(read) == [], literal_scan_problems(read)
    attrs = literal_scan_attributions(read)
    assert len(attrs) == 1, attrs
    assert "version-stamp-count" in attrs[0], attrs


def _control_scan_unattributable_permit_fires() -> None:
    """A hit matching NO exemption class must still fire as a finding — this
    is what prevents a silent catch-all permit (T-21-09-02)."""
    text = "There are 9 branches in this fixture.\n"
    hits = _literal_hits_outside_generated("fixture.md", text)
    assert len(hits) == 1, hits
    for h in hits:
        assert _literal_hit_exemption(h) is None, h
    read = LiteralScanRead(read_relpaths=frozenset({"fixture.md"}), hits=tuple(hits), declined=())
    problems = literal_scan_problems(read)
    assert len(problems) == 1, problems


def _control_scan_spelled_out_detected() -> None:
    text = "forty-seven controls were measured.\n"
    hits = _literal_hits_outside_generated("fixture.md", text)
    assert len(hits) == 1, hits
    assert "forty-seven" in hits[0].text.lower(), hits


def _control_scan_docstring_only() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        p = Path(tmp) / "fixture_mod.py"
        p.write_text(
            '"""There are 9 branches documented here."""\n'
            "# there are 9 branches in this comment, never scanned\n"
            "x = 1  # there are 9 branches in this comment either\n",
            encoding="utf-8",
        )
        # `run_literal_scan` joins `REPO_ROOT / surface`; pathlib discards
        # the left operand when the right one is already absolute, so an
        # absolute scratch path drives the real read loop unmodified.
        read = run_literal_scan(surfaces=(str(p),))
        assert str(p) in read.read_relpaths, read.read_relpaths
        assert len(read.hits) == 1, read.hits
        assert read.hits[0].relpath == f"{p}#__doc__", read.hits


def _control_scan_coverage_floor_fires() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        missing_script = str(Path(tmp) / "does_not_exist.py")
        read = run_literal_scan(surfaces=(missing_script,))
        assert read.declined, "expected a declined INFO line for a missing script"
        assert any(missing_script in line for line in read.declined), read.declined
        problems = literal_scan_coverage_floor_problems(read, surfaces=(missing_script,))
        assert len(problems) == 1, problems
        assert missing_script in problems[0], problems


def _control_scan_glob_narrowing_fires() -> None:
    """The `HEADLINE-LOCK` block (l) property: narrowing the registered
    surface set fails, naming the surface it can no longer reach — driven
    through the REAL read loop and the REAL floor, not a hand-built
    simulation."""
    narrowed = tuple(s for s in LITERAL_SCAN_SURFACES if s != "CLAUDE.md")
    read = run_literal_scan(surfaces=narrowed)
    assert "CLAUDE.md" not in read.read_relpaths, read.read_relpaths
    problems = literal_scan_coverage_floor_problems(read, surfaces=LITERAL_SCAN_SURFACES)
    assert any("CLAUDE.md" in p for p in problems), problems


def _control_scan_coverage_floor_signature_locked() -> None:
    """`HEADLINE-LOCK` block (m)'s own discipline: the floor helper's first
    parameter is the read record itself, never a glob-derived `set[str]` — a
    glob-derived substitute is unexpressible at the call site."""
    sig = inspect.signature(literal_scan_coverage_floor_problems)
    params = list(sig.parameters.values())
    assert params[0].name == "read", params
    annotation = params[0].annotation
    assert annotation in (LiteralScanRead, "LiteralScanRead"), annotation


def _control_scan_neutralization_arms() -> None:
    """Anti-vacuity by neutralization, three arms, each restored to its
    ORIGINAL function after being probed. Each is proven to break exactly
    the isolation arm the acceptance criteria name — not merely "some
    control somewhere fails"."""

    # Arm 1: disable the generated-region discriminator.
    original_fence = _this_module._generated_marker_pairs_for
    _this_module._generated_marker_pairs_for = lambda relpath: ()
    try:
        failed = False
        try:
            _control_scan_hit_inside_fence_passes()
        except AssertionError:
            failed = True
        assert failed, "neutralizing the fence discriminator did not break scan-hit-inside-fence-passes"
    finally:
        _this_module._generated_marker_pairs_for = original_fence

    # Arm 2: disable spelled-out normalisation (digit atoms only).
    original_num_atom = _this_module._literal_is_num_atom
    _digit_only_re = re.compile(r"\d{1,4}")
    _this_module._literal_is_num_atom = (
        lambda clean: bool(clean) and bool(re.fullmatch(_digit_only_re, clean))
    )
    try:
        failed = False
        try:
            _control_scan_spelled_out_detected()
        except AssertionError:
            failed = True
        assert failed, "neutralizing spelled-out matching did not break scan-spelled-out-detected"
    finally:
        _this_module._literal_is_num_atom = original_num_atom

    # Arm 3: unconditional permit — every hit exempt, no class named.
    original_exemption = _this_module._literal_hit_exemption
    _this_module._literal_hit_exemption = lambda hit: "unconditional-permit"
    try:
        failed = False
        try:
            _control_scan_unattributable_permit_fires()
        except AssertionError:
            failed = True
        assert failed, "an unconditional permit did not break scan-unattributable-permit-fires"
    finally:
        _this_module._literal_hit_exemption = original_exemption


def _control_roster_arm_shape_census() -> None:
    """GAP A item 3 (plan 21-19): the live tree carries none of the
    defective roster-arm shapes, and the census actually read every
    population member — an anti-vacuity floor independent of the scan
    logic itself, since a census silently reading nothing would otherwise
    also report zero problems."""
    problems = roster_arm_shape_census_problems()
    assert problems == [], problems
    sources = _roster_arm_census_sources()
    expected = len(_expected_harvest_scripts())
    assert len(sources) == expected, (len(sources), expected)


def _control_roster_arm_shape_census_vacuity() -> None:
    """Anti-vacuity by construction: drives
    `roster_arm_shape_census_problems` against three synthetic sources —
    the wave-15 shape, the check-version-stamps.py pre-21-17 shape, and the
    FIXED shape — and asserts exactly the first two fire, by relpath, and
    the third does not. Stops the census from passing because its patterns
    match nothing.

    The first two fixture strings below are deliberately assembled across
    more than one physical source line: `gen-gate-docs.py` is itself one of
    the 22 population members this census scans (a script-backed registry
    entry, CONF-SURFACE), so if either defective shape appeared contiguously
    on a single ON-DISK line of this file's own source, the live control
    above would self-match its own fixture data. Splitting the literal
    across a line boundary defeats that per-line self-match while the
    JOINED runtime value — what the function under test actually receives
    — is unaffected and still carries the shape whole."""
    sources = {
        "scripts/fixture-wave15.py": (
            '    elif "synthetic-b" not'
            ' in _synthetic_text:\n'
        ),
        "scripts/fixture-version-stamps.py": (
            '            "extra="'
            ' in p\n'
        ),
        "scripts/fixture-fixed.py": (
            '    elif "synthetic-b" not in missing_clause:\n'
        ),
    }
    problems = roster_arm_shape_census_problems(sources=sources)
    assert len(problems) == 2, problems
    assert any("scripts/fixture-wave15.py" in p for p in problems), problems
    assert any("scripts/fixture-version-stamps.py" in p for p in problems), problems
    assert not any("scripts/fixture-fixed.py" in p for p in problems), problems


# ---------------------------------------------------------------------------
# Task 2 controls: the deferred-literal-ledger's ratchet and staleness
# floors, plus the three per-surface injection arms promoting Task 1's
# manual falsifications into permanent registered controls.
# ---------------------------------------------------------------------------


def _control_ledger_ratchet_fires() -> None:
    """A synthetic ledger one entry larger than a synthetic pin must fail,
    naming both the pinned figure and the live figure. Drives the digest
    parameter with this ledger's own live digest so the growth predicate
    is isolated from the (unrelated) key-set-drift predicate."""
    ledger = {("fixture.md", "one"): ("999.99", 1, "fixture"), ("fixture.md", "two"): ("999.99", 1, "fixture")}
    digest = _deferred_ledger_keys_digest(ledger)
    problems = literal_ledger_ratchet_problems(ledger=ledger, max_size=1, keys_digest=digest)
    assert len(problems) == 1, problems
    assert "1" in problems[0] and "2" in problems[0], problems[0]


def _control_ledger_ratchet_requires_repin_on_shrink() -> None:
    """A synthetic ledger one entry SMALLER than its pin must now produce
    exactly one finding, naming both figures -- plan 21-20 Task 1 replaced
    the old free-shrink pass with a same-commit repin obligation: an
    un-repinned shrink buys permanent headroom for a future,
    never-adjudicated permit (T-21-20-02), so it is a finding rather than
    a silent pass. Drives the digest parameter with this ledger's own live
    digest so the shrink predicate is isolated from key-set drift."""
    ledger = {("fixture.md", "one"): ("999.99", 1, "fixture")}
    digest = _deferred_ledger_keys_digest(ledger)
    problems = literal_ledger_ratchet_problems(ledger=ledger, max_size=2, keys_digest=digest)
    assert len(problems) == 1, problems
    assert "1" in problems[0] and "2" in problems[0], problems[0]


def _control_ledger_key_digest_fires() -> None:
    """The verifier's exact reproduction (21-VERIFICATION.md GAP B), made
    permanent: remove one real ledger entry and add a fabricated,
    never-adjudicated permit in its place so the size is UNCHANGED, and
    confirm a finding naming the digest mismatch. Neither the growth nor
    the shrink predicate can see this -- `live_size` never moves -- so
    this is the one arm that proves predicate 3 is load-bearing."""
    ledger = {("fixture.md", "one"): ("999.99", 1, "fixture"), ("fixture.md", "two"): ("999.99", 1, "fixture")}
    pinned_digest = _deferred_ledger_keys_digest(ledger)
    substituted = dict(ledger)
    substituted.pop(("fixture.md", "one"))
    substituted[("fixture.md", "three (a never-adjudicated permit)")] = ("999.99", 1, "fixture")
    assert len(substituted) == len(ledger), "fixture is not a same-size substitution"
    problems = literal_ledger_ratchet_problems(
        ledger=substituted, max_size=len(ledger), keys_digest=pinned_digest
    )
    assert len(problems) == 1, problems
    assert "digest" in problems[0], problems[0]


def _control_ledger_key_digest_derived() -> None:
    """The digest helper is a real derivation, not a constant standing in
    for one: two synthetic ledgers differing in exactly one key produce
    different digests, and the same ledger built in a different insertion
    order produces the SAME digest (the sort-before-hash discipline)."""
    ledger_a = {("fixture.md", "one"): ("999.99", 1, "fixture"), ("fixture.md", "two"): ("999.99", 1, "fixture")}
    ledger_b = {("fixture.md", "one"): ("999.99", 1, "fixture"), ("fixture.md", "three"): ("999.99", 1, "fixture")}
    digest_a = _deferred_ledger_keys_digest(ledger_a)
    digest_b = _deferred_ledger_keys_digest(ledger_b)
    assert digest_a != digest_b, "differing key sets produced the same digest"
    ledger_a_reordered = dict(reversed(list(ledger_a.items())))
    digest_a_reordered = _deferred_ledger_keys_digest(ledger_a_reordered)
    assert digest_a_reordered == digest_a, "insertion-order changed the digest"


def _control_ledger_staleness_fires() -> None:
    """A fabricated ledger key matching no live hit must fail, naming that
    key -- the ledger cannot silently outlive its own findings."""
    ledger = {("fixture.md", "this text never appears anywhere in the tree"): ("999.99", 1, "fixture")}
    read = LiteralScanRead(read_relpaths=frozenset(), hits=(), declined=())
    problems = literal_ledger_staleness_problems(read, ledger=ledger)
    assert len(problems) == 1, problems
    assert "this text never appears anywhere in the tree" in problems[0], problems[0]


def _control_ledger_occurrence_surplus_fires() -> None:
    """A ledgered key's pinned occurrence count exceeded by the live scan
    must fail, naming the key and both counts — promoted from Task 1's
    manual falsification into a permanent registered control."""
    original_ledger = _this_module._DEFERRED_LITERAL_HITS
    fixture_ledger = dict(original_ledger)
    fixture_ledger[("fixture.md", "9 branches")] = ("999.99", 1, "fixture, pinned at 1")
    _this_module._DEFERRED_LITERAL_HITS = fixture_ledger
    try:
        text = "There are 9 branches here.\nThere are 9 branches here too.\n"
        hits = _literal_hits_outside_generated("fixture.md", text)
        assert len(hits) == 2, hits
        read = LiteralScanRead(read_relpaths=frozenset({"fixture.md"}), hits=tuple(hits), declined=())
        problems = literal_scan_problems(read)
        surplus = [p for p in problems if "occurrence surplus" in p]
        assert len(surplus) == 1, problems
        assert "pinned 1" in surplus[0] and "live 2" in surplus[0], surplus[0]
    finally:
        _this_module._DEFERRED_LITERAL_HITS = original_ledger


def _control_ledger_not_an_unconditional_permit() -> None:
    """Anti-masking: (a) the real ledger contains no wildcard-shaped key —
    no bare-relpath key, no empty-string text — so it cannot silently widen
    into the whole-surface permit it replaced (untouched by this task);
    (b) emptying the ledger makes the live scan report AT LEAST AS MANY
    findings as the ledger holds entries, proving the ledger is
    load-bearing rather than decorative (the same spirit as
    `_control_scan_neutralization_arms` arm 3).

    Arm (b) is relative to the ledger's own live size, not the fixed
    absolute floor this control used to assert (WR-05). The absolute form
    turns RED on successful remediation: once enough of today's hits are
    genuinely fixed and removed from the ledger, the fixed floor starts
    failing -- taking `--self-test`, the battery, CI and both pre-commit
    hooks down with it -- with a message that reads like a regression
    while describing progress. The relative form cannot make that
    mistake: it shrinks in lockstep with the ledger it measures.
    """
    for relpath, text in _DEFERRED_LITERAL_HITS:
        assert relpath, "bare-relpath-shaped key found (wildcard permit)"
        assert text, f"empty-text key found for {relpath!r} (wildcard permit)"

    original_ledger = _this_module._DEFERRED_LITERAL_HITS
    ledger_size = len(original_ledger)
    _this_module._DEFERRED_LITERAL_HITS = {}
    try:
        read = run_literal_scan()
        problems = literal_scan_problems(read)
        assert len(problems) >= ledger_size, (
            f"emptying the ledger produced only {len(problems)} findings, "
            f"fewer than the ledger's own {ledger_size} entries -- the "
            "ledger is not load-bearing"
        )
    finally:
        _this_module._DEFERRED_LITERAL_HITS = original_ledger


def _control_ledger_injection_claude_md_fires() -> None:
    """Promotes Task 1's manual CLAUDE.md falsification into a permanent
    control: an injected count literal outside the generated region must be
    a non-exempt finding on the real, on-disk CLAUDE.md."""
    text = (REPO_ROOT / "CLAUDE.md").read_text(encoding="utf-8")
    mutated = text + "\nSCAN-GUARD carries 999 clause-level named branches\n"
    hits = _literal_hits_outside_generated("CLAUDE.md", mutated)
    read = LiteralScanRead(read_relpaths=frozenset({"CLAUDE.md"}), hits=tuple(hits), declined=())
    problems = literal_scan_problems(read)
    injected = [p for p in problems if "999" in p]
    assert len(injected) == 1, problems


def _control_ledger_injection_architecture_fires() -> None:
    """Same as `_control_ledger_injection_claude_md_fires`, for
    docs/ARCHITECTURE.md."""
    text = (REPO_ROOT / "docs/ARCHITECTURE.md").read_text(encoding="utf-8")
    mutated = text + "\nSCAN-GUARD carries 999 clause-level named branches\n"
    hits = _literal_hits_outside_generated("docs/ARCHITECTURE.md", mutated)
    read = LiteralScanRead(
        read_relpaths=frozenset({"docs/ARCHITECTURE.md"}), hits=tuple(hits), declined=()
    )
    problems = literal_scan_problems(read)
    injected = [p for p in problems if "999" in p]
    assert len(injected) == 1, problems


def _control_ledger_injection_testing_fires() -> None:
    """Same as `_control_ledger_injection_claude_md_fires`, for
    docs/TESTING.md -- the exact surface the shipped regression
    ("Two gates fire on every `git commit`" while both hooks ran five) was
    silently permitted on before this plan."""
    text = (REPO_ROOT / "docs/TESTING.md").read_text(encoding="utf-8")
    mutated = text + "\nSCAN-GUARD carries 999 clause-level named branches\n"
    hits = _literal_hits_outside_generated("docs/TESTING.md", mutated)
    read = LiteralScanRead(
        read_relpaths=frozenset({"docs/TESTING.md"}), hits=tuple(hits), declined=()
    )
    problems = literal_scan_problems(read)
    injected = [p for p in problems if "999" in p]
    assert len(injected) == 1, problems


def _control_registry_self_test_passes() -> None:
    """Wires the orphan. `scripts/_gate_registry.py --self-test`'s
    controls — including the ONLY duplicate-`key`/`gate_id` check —
    previously ran nowhere automated: not the battery, not CI, not either
    pre-commit hook. This drives it as a real subprocess
    (`_control_harvest_nonzero_exit_named`'s shape) so a broken registry
    control now fails `gen-gate-docs.py --self-test`, and by extension the
    battery, CI, and both pre-commit hooks at once, naming which registry
    control broke via `proc.stderr`."""
    proc = subprocess.run(
        [sys.executable, str(_REGISTRY_PATH), "--self-test"],
        capture_output=True,
        text=True,
        timeout=60,
    )
    assert proc.returncode == 0, (
        f"scripts/_gate_registry.py --self-test exited {proc.returncode}: "
        f"{proc.stderr}"
    )


def _control_own_registry_docstring_has_no_count() -> None:
    """Deliberately narrow: pins the one function whose docstring shipped
    a stale hand-maintained control-roster count, gone by the time this
    control was added. Asserts `_control_registry_self_test_passes`'s
    docstring carries no digit at all, rather than re-checking any
    particular value -- a value would go stale again the moment the
    registry's own control count changes. This control answers only for
    that one function; the general, quantified answer for the rest of
    this file's function docstrings is a separate derived measurement,
    not a floor here. Carries no digit in its own docstring either, for
    the same reason."""
    doc = _control_registry_self_test_passes.__doc__ or ""
    assert not re.search(r"[0-9]", doc), (
        f"_control_registry_self_test_passes' docstring carries a digit: {doc!r}"
    )


def _control_selffile_docstring_ratchet_fires() -> None:
    """A synthetic live count one above a synthetic pin must fail, naming
    both figures -- the growth direction of this file's own
    py-docstrings-only-blind-spot ratchet (a second WR-08 landing in the
    file the first one landed in)."""
    problems = nonmodule_docstring_selffile_ratchet_problems(live_count=5, pinned_count=4)
    assert len(problems) == 1, problems
    assert "5" in problems[0] and "4" in problems[0], problems[0]


def _control_selffile_docstring_ratchet_requires_repin_on_shrink() -> None:
    """A synthetic live count one below a synthetic pin must also fail,
    naming both figures -- the shrink direction, demanding the pin be
    lowered to the live count in the same commit rather than granting
    free headroom for a later, unnoticed regrowth."""
    problems = nonmodule_docstring_selffile_ratchet_problems(live_count=3, pinned_count=4)
    assert len(problems) == 1, problems
    assert "3" in problems[0] and "4" in problems[0], problems[0]


def _control_slug_collision_raises() -> None:
    """Phase 21-14 (T-21-14-02): a synthetic two-entry list sharing a slug
    must raise `SlugCollisionError` naming both keys.
    `_control_page_per_entry` compares SETS of expected-vs-emitted paths and
    cannot see a collision (both sides shrink by the same count); this
    floor can, and it fires before any page is written."""
    fake = _gate_registry.GateEntry(
        key="FAKE-01",
        gate_id="FAKE-01",
        extra_ids=(),
        mechanism="x",
        ci_job=None,
        script="scripts/fake.py",
        run_command="python3 scripts/fake.py --self-test",
        summary="Fake gate for the slug-collision negative control.",
        consumes=(),
    )
    # `_page_slug` replaces ":" with "-", so a PRECOMMIT:-shaped key and a
    # plain key can collide on the same rendered slug without being
    # textually identical.
    fake_colliding = _gate_registry.GateEntry(
        key="FAKE:01",
        gate_id="FAKE:01",
        extra_ids=(),
        mechanism="x",
        ci_job=None,
        script="scripts/fake2.py",
        run_command="python3 scripts/fake2.py --self-test",
        summary="Second fake gate colliding on the same page slug.",
        consumes=(),
    )
    try:
        _assert_no_slug_collisions([fake, fake_colliding])
        raise AssertionError("expected SlugCollisionError")
    except SlugCollisionError as exc:
        assert "FAKE-01" in str(exc) and "FAKE:01" in str(exc), str(exc)


_CONTROLS: tuple[tuple[str, object], ...] = (
    ("harvest-nonzero-exit-named", _control_harvest_nonzero_exit_named),
    ("harvest-malformed-json-named", _control_harvest_malformed_json_named),
    ("harvest-one-bad-does-not-abort", _control_harvest_one_bad_does_not_abort),
    ("floors-run-together", _control_floors_run_together),
    ("frozen-path-write-fires", _control_frozen_path_write_fires),
    ("frozen-paths-derived-not-typed", _control_frozen_paths_derived_not_typed),
    ("check-dispatch-wired", _control_check_dispatch_wired),
    ("nondeterminism-exit-2", _control_nondeterminism_exit_2),
    ("region-happy-path", _control_region_happy_path),
    ("region-zero-start-raises", _control_region_zero_start_raises),
    ("region-zero-end-raises", _control_region_zero_end_raises),
    ("region-duplicate-start-raises", _control_region_duplicate_start_raises),
    ("region-duplicate-end-raises", _control_region_duplicate_end_raises),
    ("region-end-before-start-raises", _control_region_end_before_start_raises),
    ("region-marker-in-fence-ignored", _control_region_marker_in_fence_ignored),
    (
        "region-tilde-fence-quoting-backticks",
        _control_region_tilde_fence_quoting_backticks,
    ),
    ("region-preserves-final-newline", _control_region_preserves_final_newline),
    ("region-preserves-crlf", _control_region_preserves_crlf),
    ("region-real-file-claude-md", _control_real_file_claude_md_region),
    ("describe-emits-parseable-json", _control_describe_emits_parseable_json),
    ("one-renderer-two-surfaces", _control_one_renderer_two_surfaces),
    ("gates-link-resolves-per-surface", _control_gates_link_resolves_per_surface),
    ("row-count-equals-entries", _control_row_count_equals_entries),
    ("no-row-wrapped", _control_no_row_wrapped),
    ("testing-index-row-count-equals-entries", _control_testing_index_row_count_equals_entries),
    ("testing-index-links-resolve", _control_testing_index_links_resolve),
    ("testing-real-file-region", _control_testing_real_file_region),
    ("trace03-glob-substring-derived", _control_trace03_glob_substring_derived),
    ("population-arithmetic-derived", _control_population_arithmetic_derived),
    ("arithmetic-sentence-pluralizes-correctly", _control_arithmetic_sentence_pluralizes_correctly),
    ("arithmetic-sentence-names-gates-not-hooks", _control_arithmetic_sentence_names_gates_not_hooks),
    (
        "hook-mechanism-count-independent-of-precommit-count",
        _control_hook_mechanism_count_independent_of_precommit_count,
    ),
    ("framing-sentences-replaced", _control_framing_sentences_replaced),
    ("region-preserves-surrounding-prose", _control_region_preserves_surrounding_prose),
    ("page-per-entry", _control_page_per_entry),
    ("narrative-preserved-across-regeneration", _control_narrative_preserved_across_regeneration),
    ("thin-page-fully-generated", _control_thin_page_fully_generated),
    ("containment-violation-fires", _control_containment_violation_fires),
    ("containment-satisfied-passes", _control_containment_satisfied_passes),
    ("containment-spelled-out-normalised", _control_containment_spelled_out_normalised),
    ("version01-narrative-control-ids-live", _control_version01_narrative_control_ids_live),
    ("check-reports-full-drift-count", _control_page_check_dispatch_wired),
    ("scan-hit-outside-fence-fires", _control_scan_hit_outside_fence_fires),
    ("scan-hit-inside-fence-passes", _control_scan_hit_inside_fence_passes),
    ("scan-exempt-class-attributed", _control_scan_exempt_class_attributed),
    ("scan-unattributable-permit-fires", _control_scan_unattributable_permit_fires),
    ("scan-spelled-out-detected", _control_scan_spelled_out_detected),
    ("scan-docstring-only", _control_scan_docstring_only),
    ("scan-coverage-floor-fires", _control_scan_coverage_floor_fires),
    ("scan-glob-narrowing-fires", _control_scan_glob_narrowing_fires),
    ("scan-coverage-floor-signature-locked", _control_scan_coverage_floor_signature_locked),
    ("scan-neutralization-arms", _control_scan_neutralization_arms),
    ("roster-arm-shape-census", _control_roster_arm_shape_census),
    ("roster-arm-shape-census-vacuity", _control_roster_arm_shape_census_vacuity),
    ("ledger-ratchet-fires", _control_ledger_ratchet_fires),
    ("ledger-ratchet-requires-repin-on-shrink", _control_ledger_ratchet_requires_repin_on_shrink),
    ("ledger-key-digest-fires", _control_ledger_key_digest_fires),
    ("ledger-key-digest-derived", _control_ledger_key_digest_derived),
    ("ledger-staleness-fires", _control_ledger_staleness_fires),
    ("ledger-occurrence-surplus-fires", _control_ledger_occurrence_surplus_fires),
    ("ledger-not-an-unconditional-permit", _control_ledger_not_an_unconditional_permit),
    ("ledger-injection-claude-md-fires", _control_ledger_injection_claude_md_fires),
    ("ledger-injection-architecture-fires", _control_ledger_injection_architecture_fires),
    ("ledger-injection-testing-fires", _control_ledger_injection_testing_fires),
    ("registry-self-test", _control_registry_self_test_passes),
    ("own-registry-docstring-has-no-count", _control_own_registry_docstring_has_no_count),
    ("selffile-docstring-ratchet-fires", _control_selffile_docstring_ratchet_fires),
    (
        "selffile-docstring-ratchet-requires-repin-on-shrink",
        _control_selffile_docstring_ratchet_requires_repin_on_shrink,
    ),
    ("slug-collision-raises", _control_slug_collision_raises),
)

# Second, independently-typed transcription of every control id above (the
# SCAN-GUARD/CONF-GATE coverage-floor shape, D-21-K note: this discipline
# applies to self-test control-id coverage only, not to the battery gate-id
# set, which stays derived). A control added to _CONTROLS but missing here,
# or vice versa, fails self_test() by name rather than silently narrowing
# coverage.
_CONTROL_IDS: tuple[str, ...] = (
    "harvest-nonzero-exit-named",
    "harvest-malformed-json-named",
    "harvest-one-bad-does-not-abort",
    "floors-run-together",
    "frozen-path-write-fires",
    "frozen-paths-derived-not-typed",
    "check-dispatch-wired",
    "nondeterminism-exit-2",
    "region-happy-path",
    "region-zero-start-raises",
    "region-zero-end-raises",
    "region-duplicate-start-raises",
    "region-duplicate-end-raises",
    "region-end-before-start-raises",
    "region-marker-in-fence-ignored",
    "region-tilde-fence-quoting-backticks",
    "region-preserves-final-newline",
    "region-preserves-crlf",
    "region-real-file-claude-md",
    "describe-emits-parseable-json",
    "one-renderer-two-surfaces",
    "gates-link-resolves-per-surface",
    "row-count-equals-entries",
    "no-row-wrapped",
    "testing-index-row-count-equals-entries",
    "testing-index-links-resolve",
    "testing-real-file-region",
    "trace03-glob-substring-derived",
    "population-arithmetic-derived",
    "arithmetic-sentence-pluralizes-correctly",
    "arithmetic-sentence-names-gates-not-hooks",
    "hook-mechanism-count-independent-of-precommit-count",
    "framing-sentences-replaced",
    "region-preserves-surrounding-prose",
    "page-per-entry",
    "narrative-preserved-across-regeneration",
    "thin-page-fully-generated",
    "containment-violation-fires",
    "containment-satisfied-passes",
    "containment-spelled-out-normalised",
    "version01-narrative-control-ids-live",
    "check-reports-full-drift-count",
    "scan-hit-outside-fence-fires",
    "scan-hit-inside-fence-passes",
    "scan-exempt-class-attributed",
    "scan-unattributable-permit-fires",
    "scan-spelled-out-detected",
    "scan-docstring-only",
    "scan-coverage-floor-fires",
    "scan-glob-narrowing-fires",
    "scan-coverage-floor-signature-locked",
    "scan-neutralization-arms",
    "roster-arm-shape-census",
    "roster-arm-shape-census-vacuity",
    "ledger-ratchet-fires",
    "ledger-ratchet-requires-repin-on-shrink",
    "ledger-key-digest-fires",
    "ledger-key-digest-derived",
    "ledger-staleness-fires",
    "ledger-occurrence-surplus-fires",
    "ledger-not-an-unconditional-permit",
    "ledger-injection-claude-md-fires",
    "ledger-injection-architecture-fires",
    "ledger-injection-testing-fires",
    "registry-self-test",
    "own-registry-docstring-has-no-count",
    "selffile-docstring-ratchet-fires",
    "selffile-docstring-ratchet-requires-repin-on-shrink",
    "slug-collision-raises",
)


def self_test() -> int:
    executed: list[str] = []
    failures: list[tuple[str, str]] = []

    for control_id, control_fn in _CONTROLS:
        executed.append(control_id)
        try:
            control_fn()
        except AssertionError as exc:
            failures.append((control_id, str(exc)))
        except Exception as exc:  # noqa: BLE001 -- a control that crashes is a failure too
            failures.append((control_id, f"{type(exc).__name__}: {exc}"))

    registered = set(_CONTROL_IDS)
    ran = set(executed)
    missing = registered - ran
    extra = ran - registered
    if missing or extra:
        failures.append(
            (
                "coverage-floor",
                f"registered/executed control-id mismatch: missing={sorted(missing)} "
                f"extra={sorted(extra)}",
            )
        )

    if failures:
        for control_id, message in failures:
            sys.stderr.write(f"gen-gate-docs: SELF-TEST FAIL [{control_id}] — {message}\n")
        return 1
    print(f"gen-gate-docs: SELF-TEST PASS — {len(executed)} controls run")
    return 0


def main(argv: list[str] | None = None) -> int:
    """`argv` defaults to `None` so `--self-test` can drive `main()` itself
    end to end against a fixture argv, proving the CLI dispatch is wired,
    not just the `cmd_*` functions it calls (Phase-152 WR-01 precedent,
    `scripts/sync-content.py`'s own comment)."""
    p = argparse.ArgumentParser(
        prog="gen-gate-docs.py",
        description="Generate the CI-gate claim surface from --describe emissions.",
    )
    g = p.add_mutually_exclusive_group(required=True)
    g.add_argument("--write", action="store_true", help="Regenerate all targets.")
    g.add_argument(
        "--check",
        action="store_true",
        help="Compare; exit 1 on drift or a harvest/floor problem, exit 2 on non-determinism.",
    )
    g.add_argument("--self-test", action="store_true", help="Run the offline control battery.")
    g.add_argument(
        "--describe",
        action="store_true",
        help="Emit this gate's self-description as a flat JSON blob on stdout.",
    )
    g.add_argument(
        "--emit-deferred-ledger",
        action="store_true",
        help=(
            "Maintenance-only: print a mechanically-populated "
            "_DEFERRED_LITERAL_HITS literal to stdout. Writes nothing to disk."
        ),
    )
    args = p.parse_args(argv)
    if args.write:
        return cmd_write()
    if args.check:
        return cmd_check()
    if args.self_test:
        return self_test()
    if args.emit_deferred_ledger:
        print(emit_deferred_ledger())
        return 0
    print(json.dumps(describe(), indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main())
