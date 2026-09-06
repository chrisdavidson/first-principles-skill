#!/usr/bin/env python3
# /// script
# requires-python = ">=3.12"
# ///
"""CONF-SURFACE: generate the CI-gate claim surface from --describe emissions.

Hand-transcribed gate documentation produced 41% of all review findings
across Phases 13-15 — every branch count, surface list and disclosed bound
was copied by hand into up to five places with nothing checking they
agreed. This script is the fix's compute layer (D-21-B): it subprocess-
invokes every script-backed `scripts/_gate_registry.py` entry's `--describe`
leg, applies the registry's own D-01/D-04 floors plus a frozen-path
disjointness floor over its own write set, and exposes the region-
replacement primitive `docs/gates/<GATE-ID>.md` pages and the two hand-
written table regions will be regenerated through. The render layer that
turns harvested facts into `CLAUDE.md`/`docs/ARCHITECTURE.md`/`docs/gates/`
text is a later plan's job (`generate_all()` is a stub here, returning no
targets) — this plan proves the harvest, the floors and the region-rewrite
primitive work before any rendered text exists to drift against.

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
import difflib
import fnmatch
import importlib.util
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
DETAIL_PAGE_DIR: Path = REPO_ROOT / "docs" / "gates"

# The gate ids whose docs/gates/<ID>.md page carries a hand-written narrative
# region — the four measured-fat cells (D-08). Membership is a property of
# content, not a threshold rule someone applies.
NARRATIVE_ENTRIES: frozenset[str] = frozenset({"QUAL-01", "SCAN-GUARD", "TRACE-03", "CONF-GATE"})

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
    parts.append(f"See [`docs/gates/{slug}.md`](gates/{slug}.md).")
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
    synthetic entry and observe which counts move."""
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
    return {
        "ci_count": ci_count,
        "precommit_count": precommit_count,
        "inline_count": inline_count,
        "tallied_count": tallied_count,
        "battery_only_count": battery_only_count,
    }


def _population_arithmetic_sentence(entries) -> str:
    c = _population_counts(entries)
    return (
        f"Gates run on three surfaces: **{c['ci_count']} in CI** "
        "(`.github/workflows/validation.yml`, on push/PR to master), "
        f"**{c['tallied_count']} tallied in the offline battery** "
        "(`bash scripts/check-firewall-battery.sh`), and "
        f"**{c['precommit_count']} pre-commit** hooks. The battery is a strict "
        f"superset of CI: all {c['ci_count']} CI gates plus "
        f"{c['battery_only_count']} battery-only gate(s) plus "
        f"{c['inline_count']} inline check(s). That is {c['ci_count']} + "
        f"{c['battery_only_count']} + {c['inline_count']} = {c['tallied_count']}."
    )


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
    arithmetic = _population_arithmetic_sentence(_gate_registry.ENTRIES)
    return f"{lead_in}\n\n{table}\n\n{arithmetic}"


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


def _normalise_numbers(text: str) -> set[str]:
    """Every digit-form number literal in `text`, plus every spelled-out
    number word/compound normalised to its digit string (D-06's stated
    position on spelled-out forms). Disclosed bound, published on every
    detail page: a spelled-out form outside this vocabulary (one..twenty,
    the tens, hundred, hyphenated compounds) is not normalised and is
    therefore not checked."""
    found: set[str] = {m.group(0).replace(",", "") for m in _NUMBER_RE.finditer(text)}
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
    display_name: str, text: str, marker_pairs=_ALL_DETAIL_MARKER_PAIRS
) -> list[str]:
    """D-06's containment floor for one `docs/gates/*.md` page's text. The
    page's own H1 title (line 0) is excluded from the 'outside' scan — it
    names the gate id, an identifier, not a count claim, and gate ids like
    `VAL-01` or `GATE-02-v8.5` otherwise trip the digit regex on their own
    suffix."""
    lines = text.splitlines()
    inside = _generated_line_flags(lines, marker_pairs)
    outside_lines = [line for idx, (line, is_in) in enumerate(zip(lines, inside)) if not is_in and idx != 0]
    inside_lines = [line for line, is_in in zip(lines, inside) if is_in]
    outside_numbers = _normalise_numbers("\n".join(outside_lines))
    inside_numbers = _normalise_numbers("\n".join(inside_lines))
    missing = sorted(outside_numbers - inside_numbers, key=lambda s: (len(s), s))
    return [
        f"containment: {display_name} states {number!r} outside a generated fence "
        "with no matching literal inside one (D-06)"
        for number in missing
    ]


# ---------------------------------------------------------------------------
# generate_all() — the single compute+render entry point (D-21-B interface).
# Called ONCE per --write, TWICE per --check (idempotency), following
# report-conformance.py:2636-2646's "cannot disagree with each other"
# discipline. Nothing is written to disk by THIS plan — 21-08 lands --write.
# ---------------------------------------------------------------------------


def generate_all() -> dict[Path, str]:
    non_anticipatory = [
        e for e in _gate_registry.ENTRIES if e.key not in _gate_registry._ANTICIPATORY_KEYS
    ]
    by_script, _harvest_problems = harvest(non_anticipatory)

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

    # D-08: every registry entry — including the anticipatory CONF-SURFACE
    # member — gets a docs/gates/<GATE-ID>.md page.
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

    non_anticipatory = [
        e for e in _gate_registry.ENTRIES if e.key not in _gate_registry._ANTICIPATORY_KEYS
    ]
    by_script, harvest_problems = harvest(non_anticipatory)
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
    print(f"harvested {len(by_script)}/{len(expected_scripts)} script-backed entries")
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
            problems += detail_page_containment_problems(str(rel), generated)

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


def describe() -> dict:
    """CONF-SURFACE's own self-description (D-21-C: "a generator that cannot
    describe itself would be the first exception to D-08's uniformity in
    the same phase that establishes it"). Pure — reads only this module's
    own constants."""
    return {
        "control_ids": sorted(_CONTROL_IDS),
        "control_count": len(_CONTROL_IDS),
        "locked_constants": {
            "generated_marker": GENERATED_MARKER,
            "generated_end_marker": GENERATED_END_MARKER,
        },
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

    As of plan 21-07's render layer, this must return 1 (drift), never 0:
    `generate_all()` now returns real content for CLAUDE.md,
    docs/ARCHITECTURE.md and every docs/gates/*.md page, none of which
    exist yet in their generated form on disk — a 0 here would mean the
    renderer reproduced the pre-existing text, which D-02 makes
    impossible, so this control now treats a 0 as a defect (matching the
    plan's own acceptance criterion)."""
    rc = main(["--check"])
    assert rc == 1, f"main(['--check']) returned {rc}, expected 1 (drift) against the live tree"


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
    assert CLAUDE_MD in targets and ARCHITECTURE_MD in targets, targets.keys()
    assert len(targets) == len(expected) + 2, (len(targets), len(expected))


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
    entry = next(e for e in _gate_registry.ENTRIES if e.key == "VAL-01")
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
    """Live leg: main(["--check"]) against the real tree names every
    docs/gates/*.md page as missing (they do not exist on disk yet) plus
    both surface files — len(ENTRIES) + 2 drifted targets, exit 1."""
    targets = generate_all()
    assert len(targets) == len(_gate_registry.ENTRIES) + 2, len(targets)
    for path in targets:
        if DETAIL_PAGE_DIR in path.parents:
            assert not path.exists(), f"{path} unexpectedly exists on disk"
    rc = main(["--check"])
    assert rc == 1, f"main(['--check']) returned {rc}, expected 1 (drift: pages do not exist yet)"


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
    ("row-count-equals-entries", _control_row_count_equals_entries),
    ("no-row-wrapped", _control_no_row_wrapped),
    ("trace03-glob-substring-derived", _control_trace03_glob_substring_derived),
    ("population-arithmetic-derived", _control_population_arithmetic_derived),
    ("framing-sentences-replaced", _control_framing_sentences_replaced),
    ("region-preserves-surrounding-prose", _control_region_preserves_surrounding_prose),
    ("page-per-entry", _control_page_per_entry),
    ("narrative-preserved-across-regeneration", _control_narrative_preserved_across_regeneration),
    ("thin-page-fully-generated", _control_thin_page_fully_generated),
    ("containment-violation-fires", _control_containment_violation_fires),
    ("containment-satisfied-passes", _control_containment_satisfied_passes),
    ("containment-spelled-out-normalised", _control_containment_spelled_out_normalised),
    ("check-reports-full-drift-count", _control_page_check_dispatch_wired),
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
    "row-count-equals-entries",
    "no-row-wrapped",
    "trace03-glob-substring-derived",
    "population-arithmetic-derived",
    "framing-sentences-replaced",
    "region-preserves-surrounding-prose",
    "page-per-entry",
    "narrative-preserved-across-regeneration",
    "thin-page-fully-generated",
    "containment-violation-fires",
    "containment-satisfied-passes",
    "containment-spelled-out-normalised",
    "check-reports-full-drift-count",
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
