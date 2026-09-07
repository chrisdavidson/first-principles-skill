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
    """Build the 27-row (documented, non-anticipatory) x 4-column row set
    from `entries` + a harvest blob map. Pure — used identically to build
    the SAME `rows` value `generate_all()` hands to both surfaces (D-02)."""
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
    for the 24 thin fully-generated pages) turns off SPELLED-OUT matching
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


# --- deferred-remediation (plan 21-10, Task 3): whole-surface deferral -----
#
# A budget-driven deferral, not a content-based exemption — every hit on a
# REGISTERED surface in this map is permitted, regardless of what its text
# says, because plan 21-10 measured the surface's remediation as out of this
# task's ~15-item/6-file budget and deferred the whole surface under a named
# 999.x backlog id with a written reason (21-CONF13-BASELINE.md,
# docs/gates/CONF-SURFACE.md). Matches on `hit.relpath`, never `hit.text` —
# the one exemption class in this tuple that needs the whole hit rather than
# just its text, which is why `LiteralExemptionClass.matches` takes the full
# `LiteralHit` rather than a bare string.
_DEFERRED_REMEDIATION_SURFACES: dict[str, str] = {
    # 999.40: docs/gates/*.md narrative pages migrated/hand-written under
    # plans 21-08/21-10 — dense technical prose using ordinary-language small
    # numbers ("two contract surfaces", "(1) worked-example extraction") that
    # D-06's containment check already learned a citation-exemption
    # vocabulary for (plan 21-08) but the standing CONF-13 scanner does not
    # share (21-09-SUMMARY.md's own Assumption Drift note).
    "docs/gates/QUAL-01.md": "999.40",
    "docs/gates/SCAN-GUARD.md": "999.40",
    "docs/gates/TRACE-03.md": "999.40",
    "docs/gates/CONF-GATE.md": "999.40",
    "docs/gates/GATE-01.md": "999.40",
    "docs/gates/HC-BOUND.md": "999.40",
    "docs/gates/REG-GUARD.md": "999.40",
    "docs/gates/VAL-02.md": "999.40",
    "docs/gates/VERSION-01.md": "999.40",
    "docs/gates/STEP0-08.md": "999.40",
    # 999.41: .py module docstrings — the same ordinary-language-number shape,
    # in dense narrative docstrings this scanner reads verbatim
    # (21-CONF13-BASELINE.md's own false-positive layer — ordinal-label-
    # reference, adjacency-mistrack, enumerated-list-marker — was deliberately
    # not ported into the standing scanner; plan 21-09's key-decision).
    "scripts/check-selfaudit-scan.py#__doc__": "999.41",
    "scripts/check-step0-emulator.py#__doc__": "999.41",
    "scripts/check-quality-harness.py#__doc__": "999.41",
    "scripts/check-conf-gate.py#__doc__": "999.41",
    "scripts/check-step0-live.py#__doc__": "999.41",
    "scripts/check-provenance.py#__doc__": "999.41",
    "scripts/check-focused-parity.py#__doc__": "999.41",
    "scripts/check-registration.py#__doc__": "999.41",
    "scripts/check-loop-closure.py#__doc__": "999.41",
    "scripts/check-links.py#__doc__": "999.41",
    "scripts/check-agent.py#__doc__": "999.41",
    "scripts/check-act-limb.py#__doc__": "999.41",
    # 999.42: the peripheral CI-gate-table host surfaces' own remaining
    # non-structural prose — CLAUDE.md and docs/ARCHITECTURE.md carry
    # operational/provenance narrative outside the generated table region
    # (D-02's fold), and docs/TESTING.md carries the "Pre-commit gates" and
    # "Anti-masking measurement invariants" sections plan 21-10 Task 1
    # deliberately left outside the per-gate-section fold (D-21-F's own
    # scope: the 13 CI-gate ### sections, not the whole file).
    "CLAUDE.md": "999.42",
    "docs/ARCHITECTURE.md": "999.42",
    "docs/TESTING.md": "999.42",
}


def _match_deferred_remediation(hit: LiteralHit) -> bool:
    return hit.relpath in _DEFERRED_REMEDIATION_SURFACES


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
        "deferred-remediation",
        "Plan 21-10 measured this surface's remediation as beyond its own "
        "~15-item/6-file task budget and deferred it under a named 999.x "
        "backlog id (999.40 docs/gates/*.md narrative, 999.41 .py module "
        "docstrings, 999.42 the peripheral CI-gate-table host surfaces' own "
        "remaining prose) — see 21-CONF13-BASELINE.md and "
        "docs/gates/CONF-SURFACE.md for the full item list and reason. Not a "
        "content-based exemption: every hit on a deferred surface is "
        "permitted regardless of what its text says.",
        _match_deferred_remediation,
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
    making the whole scanner vacuous)."""
    problems: list[str] = []
    for hit in read.hits:
        if _literal_hit_exemption(hit) is not None:
            continue
        problems.append(
            f"{hit.relpath}:{hit.line}: hand-maintained count literal '{hit.text}' "
            "(no exemption class matches)"
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


# ---------------------------------------------------------------------------
# generate_all() — the single compute+render entry point (D-21-B interface).
# Called ONCE per --write, TWICE per --check (idempotency), following
# report-conformance.py:2636-2646's "cannot disagree with each other"
# discipline. Nothing is written to disk by THIS plan — 21-08 lands --write.
# ---------------------------------------------------------------------------


def generate_all() -> dict[Path, str]:
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
    "deferred-remediation-is-budget-driven",
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
    derived_counts = {
        "literal_scan_surfaces": len(LITERAL_SCAN_SURFACES),
        "literal_scan_read_files": len(literal_read.read_relpaths),
        "literal_scan_hits": len(literal_read.hits),
        "literal_scan_non_exempt": non_exempt_count,
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
    args = p.parse_args(argv)
    if args.write:
        return cmd_write()
    if args.check:
        return cmd_check()
    if args.self_test:
        return self_test()
    print(json.dumps(describe(), indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main())
