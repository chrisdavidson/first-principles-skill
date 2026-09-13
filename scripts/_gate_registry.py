#!/usr/bin/env python3
# /// script
# requires-python = ">=3.12"
# ///
"""Gate registry (Phase 21, D-01): a single entry per documented gate row.

Hand-transcribed gate documentation produced the measured share of all review
findings across Phases 13-15 (see `HAND_TRANSCRIPTION_FINDING_SHARE` below for
the figure) — every branch count, surface list and disclosed bound was copied
by hand into up to five places with nothing checking they agreed. This module
is the fix: it holds `len(ENTRIES)` entries -- a single entry per row
`CLAUDE.md`'s and `docs/ARCHITECTURE.md`'s gate tables currently document, and
floors its own id set by EQUALITY against the ids
`scripts/check-firewall-battery.sh` actually registers — derived by regex from
that file's own source text, never hand-retyped a second time (D-21-K: this
registry does NOT get a second, independently-typed transcription in this
phase; that question is explicitly Phase 22's call, 999.30/999.31).

Later plans in this phase (21-03/04/05) implement `--describe` limbs against
this module's `DESCRIBE_FIELD_VOCABULARY`; the generator (21-06/07) renders
`CLAUDE.md` and `docs/ARCHITECTURE.md` from `ENTRIES`; the drift gate (21-11)
is registered as an `ENTRIES` member in its own right.

This module does not import any of the scripts it describes (D-21-A): it
declares field names and static facts, it never executes another gate's
checking logic, and it perturbs none of the three CONTRACT-06 sha256 pins
(`_chain_block_well_formed`, `_conclusion_claims`, `_slice_sections`).

Usage:
    python3 scripts/_gate_registry.py --self-test
    python3 scripts/_gate_registry.py --describe

Exit codes: 0 pass, 1 self-test/validation failure.
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import NamedTuple

REPO_ROOT: Path = Path(__file__).resolve().parents[1]
BATTERY_PATH: Path = REPO_ROOT / "scripts" / "check-firewall-battery.sh"
ARCHITECTURE_PATH: Path = REPO_ROOT / "docs" / "ARCHITECTURE.md"

# Measured across Phases 13-15 (this phase's own milestone justification):
# the share of all review findings in those phases directly caused by
# hand-transcribed gate documentation drifting out of sync with the scripts
# it described. A frozen historical measurement, not a derived count -- it
# does not move as the code in this file changes, and re-measuring it is out
# of scope for this module. Kept here, in a named constant rather than
# inline prose, so CONF-13's standing literal scanner (which reads this
# module's own docstring) sees no hand-maintained count claim while the
# figure itself stays in the tracked tree.
HAND_TRANSCRIPTION_FINDING_SHARE: str = "41%"


# ---------------------------------------------------------------------------
# GateEntry
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class GateEntry:
    """One documented gate/mechanism row.

    `key` is a stable identifier used internally by this module (equal to
    `gate_id` for every battery-registered entry; a synthetic `PRECOMMIT:...`
    string for the five pre-commit mechanism rows, which carry no gate id).

    `gate_id` is the id `scripts/check-firewall-battery.sh` registers via
    `gate "<ID>"` / `gate_prereq "<ID>"` — `None` for the five pre-commit rows,
    which have no battery registration at all.

    `extra_ids` carries additional ids the SAME row states but the battery
    does not itself register under (`VAL-04` row also states `GATE-02` — the
    pre-existing v3.0 trigger-collision-scanner id; the battery only ever
    calls `gate "VAL-04"`). `extra_ids` is deliberately excluded from the
    D-01 battery-id equality floor — see `registry_id_problems()`.

    `consumes` is the set of `--describe` field names this entry's table row
    and `docs/gates/<ID>.md` detail page are expected to read. It starts
    empty for every entry in this plan (no script yet emits `--describe` —
    that is plans 21-03/04/05's job) and is filled in as those limbs land.

    `static_facts` is populated ONLY for entries with no backing Python
    script (`script is None`) — there is nothing for a `--describe` limb to
    emit, so the registry itself carries the static description.
    """

    key: str
    gate_id: str | None
    extra_ids: tuple[str, ...]
    mechanism: str
    ci_job: str | None
    script: str | None
    run_command: str
    summary: str
    consumes: tuple[str, ...] = ()
    static_facts: dict[str, object] = field(default_factory=dict)


# ---------------------------------------------------------------------------
# ENTRIES
#
# One per row in docs/ARCHITECTURE.md's "CI and pre-commit gate inventory"
# table (31 rows as of plan 21-13: 24 battery-registered gate ids — VAL-04's
# row carries a second, extra id, GATE-02, so 24 rows still means 24 primary
# ids — plus the 2 inline checks INVARIANT-CHECK/FROZEN-EVIDENCE, giving 26
# battery-tallied rows; plus the 5 pre-commit mechanism rows with no gate id
# at all, one per hook gate (plan 21-13, CR-04) = 31 total documented rows).
#
# `_ANTICIPATORY_KEYS` is now empty (D-21-C, plan 21-11): CONF-SURFACE was
# the single anticipatory entry — added ahead of its own documentation while
# `scripts/gen-gate-docs.py` did not yet exist, was not yet in the battery,
# had no CI job, and did not yet appear in docs/ARCHITECTURE.md's table.
# Plan 21-11 wired all three (battery registration, CI job, and both
# pre-commit hooks) and regenerated docs/ARCHITECTURE.md's table to include
# its row, so CONF-SURFACE is now a fully-documented entry like every other
# row and no longer needs the exclusion. The mechanism stays named
# (`_ANTICIPATORY_KEYS`, not deleted) so a future anticipatory entry has a
# working precedent to extend, rather than needing to be re-invented.
# ---------------------------------------------------------------------------

_ANTICIPATORY_KEYS: frozenset[str] = frozenset()


def _ci(job_key: str) -> str:
    """Render the `Job / Mechanism` column's CI-job form, matching the
    exact string shape docs/ARCHITECTURE.md's table already uses
    (`` `plugin-validate` (CI) ``)."""
    return f"`{job_key}` (CI)"


ENTRIES: tuple[GateEntry, ...] = (
    GateEntry(
        key="VAL-01",
        gate_id="VAL-01",
        extra_ids=(),
        mechanism=_ci("plugin-validate"),
        ci_job="plugin-validate",
        script=None,
        run_command="claude plugin validate ./first-principles",
        summary=(
            "Plugin manifest schema validity via the `claude` CLI. Spends zero model "
            "tokens. Does NOT validate the agent frontmatter — the CLI walks "
            "subdirectories of `agents/` and never inspects a flat `agents/*.md`, so "
            "GATE-01 is the sole validator of agent frontmatter."
        ),
        static_facts={"tool": "claude plugin validate", "spends_model_tokens": 0},
    ),
    GateEntry(
        key="VAL-02",
        gate_id="VAL-02",
        extra_ids=(),
        mechanism=_ci("markdownlint"),
        ci_job="markdownlint",
        script=None,
        run_command=(
            "markdownlint-cli2 --config .markdownlint.jsonc 'first-principles/**/*.md'"
        ),
        summary="MD style across `first-principles/**/*.md` via `markdownlint-cli2`.",
        static_facts={
            "tool": "markdownlint-cli2",
            "scan_glob": "first-principles/**/*.md",
        },
    ),
    GateEntry(
        key="VAL-03",
        gate_id="VAL-03",
        extra_ids=(),
        mechanism=_ci("check-links"),
        ci_job="check-links",
        script="scripts/check-links.py",
        run_command=(
            "python3 scripts/check-links.py --self-test && "
            "python3 scripts/check-links.py && "
            ".venv/bin/python3 -m pytest scripts/check-links_anchors_test.py -q  "
            "# or any pytest-capable interpreter"
        ),
        summary=(
            "Relative Markdown link validity across the plugin, `shared/`, and `docs/` "
            "trees; `docs/` anchors validated with a github-slugger rule. Three legs: "
            "self-test, a live scan, and a pytest run of "
            "`check-links_anchors_test.py`. The third leg needs a pytest-capable "
            "interpreter — when none is found the battery still runs legs 1-2 through "
            "`gate_prereq` and reports [PREREQ]/BLOCKED rather than [PASS]/GREEN."
        ),
        consumes=("scan_globs", "locked_constants"),
        static_facts={
            "pytest_leg_script": "scripts/check-links_anchors_test.py",
            "pytest_leg_note": (
                "runs under EITHER gate() (interpreter resolved) OR gate_prereq() "
                "(no interpreter found); either way VAL-03 occupies exactly one "
                "battery tally slot — this is a leg of THIS entry, never a second one"
            ),
        },
    ),
    GateEntry(
        key="VAL-04",
        gate_id="VAL-04",
        extra_ids=("GATE-02",),
        mechanism=_ci("check-trigger-collisions"),
        ci_job="check-trigger-collisions",
        script="scripts/check-trigger-collisions.py",
        run_command=(
            "python3 scripts/check-trigger-collisions.py --self-test && "
            "python3 scripts/check-trigger-collisions.py"
        ),
        summary=(
            "No 4-gram collision across skill descriptions. Carries the pre-existing "
            "v3.0 GATE-02 id alongside VAL-04 — the battery registers this row under "
            "`VAL-04` only; `GATE-02` is a name the row also carries, not a second "
            "battery registration (see `extra_ids` on this entry, excluded from the "
            "D-01 battery-id equality floor by construction)."
        ),
        consumes=("derived_counts",),
    ),
    GateEntry(
        key="VAL-05",
        gate_id="VAL-05",
        extra_ids=(),
        mechanism=_ci("check-description-budget"),
        ci_job="check-description-budget",
        script="scripts/check-description-budget.py",
        run_command="python3 scripts/check-description-budget.py",
        summary="All skill listings stay under the 2000-character budget cap.",
        consumes=("locked_constants",),
    ),
    GateEntry(
        key="VERSION-01",
        gate_id="VERSION-01",
        extra_ids=(),
        mechanism=_ci("check-version-stamps"),
        ci_job="check-version-stamps",
        script="scripts/check-version-stamps.py",
        run_command=(
            "python3 scripts/check-version-stamps.py --self-test && "
            "python3 scripts/check-version-stamps.py"
        ),
        summary=(
            "Every hand-maintained version stamp carries the same value. Runs the "
            "live scan as well as the self-test — the invariant is a property of "
            "the working tree, not of the script's own fixtures."
        ),
        consumes=("derived_counts", "registered_surfaces"),
    ),
    GateEntry(
        key="REG-GUARD",
        gate_id="REG-GUARD",
        extra_ids=(),
        mechanism=_ci("check-registration"),
        ci_job="check-registration",
        script="scripts/check-registration.py",
        run_command=(
            "python3 scripts/check-registration.py --self-test && "
            "python3 scripts/check-registration.py"
        ),
        summary=(
            "Registration completeness over two surfaces: (a) every skill directory "
            "and the main agent carry a frontmatter `name:` matching their own "
            "basename; (b) every gate this file's own battery registers has a "
            "matching `name: <job> (<GATE-ID>)` job in "
            "`.github/workflows/validation.yml`, QUAL-01 the one named battery-only "
            "exemption. This module's D-01 floor deliberately reuses "
            "`check-registration.py`'s `_BATTERY_GATE_RE` parsing semantics rather "
            "than inventing a second grammar over the same file."
        ),
        consumes=(
            "control_ids",
            "control_count",
            "registered_surfaces",
            "checked_files",
            "locked_constants",
        ),
    ),
    GateEntry(
        key="COLLIDE-01",
        gate_id="COLLIDE-01",
        extra_ids=(),
        mechanism=_ci("check-install-collisions"),
        ci_job="check-install-collisions",
        script="scripts/check-install-collisions.py",
        run_command=(
            "python3 scripts/check-install-collisions.py --self-test && "
            "python3 scripts/check-install-collisions.py"
        ),
        summary=(
            "Dual-install name-collision scan: no skill/agent name collisions "
            "between the plugin and monolith install surfaces."
        ),
        consumes=("registered_surfaces", "disclosed_bounds_anchors"),
    ),
    GateEntry(
        key="DUAL-04",
        gate_id="DUAL-04",
        extra_ids=(),
        mechanism=_ci("sync-check"),
        ci_job="sync-check",
        script="scripts/sync-content.py",
        run_command="python3 scripts/sync-content.py --check",
        summary="`shared/` and the generated `first-principles/` tree are in sync.",
        consumes=(
            "derived_counts",
            "registered_surfaces",
            "locked_constants",
            "control_ids",
            "control_count",
        ),
    ),
    GateEntry(
        key="GATE-02-v8.5",
        gate_id="GATE-02-v8.5",
        extra_ids=(),
        mechanism="`GATE-02-v8.5`",  # bare CI job name form — see parse_ci_job_name()
        ci_job="pointer-drift-guard",
        script="scripts/sync-content.py",
        run_command="python3 scripts/sync-content.py --self-test",
        summary=(
            "Pointer drift-guard: each of the four split core reference files' "
            "extracted Procedure slice carries exactly one well-formed link to its "
            "own `-detail.md` sibling. Proves the pointer exists and is well-formed, "
            "NOT that it is followed. Same script as DUAL-04, a different flag — the "
            "D-03 case for a flat `--describe` namespace rather than a per-gate id "
            "argument."
        ),
    ),
    GateEntry(
        key="GATE-01",
        gate_id="GATE-01",
        extra_ids=(),
        mechanism=_ci("check-agent"),
        ci_job="check-agent",
        script="scripts/check-agent.py",
        run_command=(
            "python3 scripts/check-agent.py --self-test && "
            "python3 scripts/check-agent.py"
        ),
        summary=(
            "Agent structural checks — 8 frontmatter/body assertions on the shipped "
            "agent, including the exact `maxTurns` value (60), not merely its "
            "presence. The live leg targets the repo-anchored `AGENT_FILE` constant, "
            "so the gate is cwd-independent and cannot be silently re-pointed."
        ),
        consumes=(
            "branch_roster",
            "branch_count",
            "scoped_branches",
            "locked_constants",
            "checked_files",
            "disclosed_bounds_anchors",
        ),
    ),
    GateEntry(
        key="BATT-06",
        gate_id="BATT-06",
        extra_ids=(),
        mechanism=_ci("check-routing-battery"),
        ci_job="check-routing-battery",
        script="scripts/check-routing-battery.py",
        run_command="python3 scripts/check-routing-battery.py --self-test",
        summary=(
            "Offline merged dual-signal routing-battery self-test (boundary + "
            "focused-output); owns the honest-state and anti-masking sentinels."
        ),
        consumes=("locked_constants", "disclosed_bounds_anchors", "derived_counts", "checked_files"),
    ),
    GateEntry(
        key="STEP0-08",
        gate_id="STEP0-08",
        extra_ids=(),
        mechanism=_ci("check-step0-emulator"),
        ci_job="check-step0-emulator",
        script="scripts/check-step0-emulator.py",
        run_command="python3 scripts/check-step0-emulator.py --self-test",
        summary="Offline Step 0 phrase-detection classifier self-test.",
        consumes=("locked_constants", "derived_counts", "disclosed_bounds_anchors", "checked_files"),
    ),
    GateEntry(
        key="STEP0-06",
        gate_id="STEP0-06",
        extra_ids=(),
        mechanism=_ci("check-step0-live"),
        ci_job="check-step0-live",
        script="scripts/check-step0-live.py",
        run_command="python3 scripts/check-step0-live.py --self-test",
        summary="Offline Step 0 live-harness scoring/parsing logic self-test.",
        consumes=("locked_constants", "checked_files", "control_ids", "control_count"),
    ),
    GateEntry(
        key="TRACE-03",
        gate_id="TRACE-03",
        extra_ids=(),
        mechanism=_ci("check-traceability"),
        ci_job="check-traceability",
        script="scripts/check-traceability.py",
        run_command="python3 scripts/check-traceability.py --self-test",
        summary=(
            "Offline traceability gate self-test — capability/tier schema, artifact "
            "resolution, a live row-field leg checking every matrix row's surfaces "
            "value against the shipped-skill vocabulary, plus the HEADLINE-LOCK "
            "sentinel asserting the published coverage headline against five named "
            "current-fact surfaces and both tracked matrix artifacts."
        ),
        consumes=(
            "scan_globs",
            "registered_surfaces",
            "branch_roster",
            "branch_count",
            "locked_constants",
            "coverage_headline",
        ),
    ),
    GateEntry(
        key="QUAL-01",
        gate_id="QUAL-01",
        extra_ids=(),
        mechanism="battery only — not a CI job",
        ci_job=None,
        script="scripts/check-quality-harness.py",
        run_command="python3 scripts/check-quality-harness.py --self-test",
        summary=(
            "Offline blind A/B quality-measurement harness self-test — extraction "
            "guardrails, scoreline parsing, blinding, tabulation, baseline-fixture "
            "integrity, the mechanical defect detector, and the emission rendering "
            "contract's six legs. The single named battery-only CI exemption in "
            "REG-GUARD's `BATTERY_ONLY_GATE_IDS`."
        ),
        consumes=(
            "control_ids",
            "control_count",
            "registered_surfaces",
            "disclosed_bounds_anchors",
            "derived_counts",
            "locked_constants",
            "contract_pins",
        ),
    ),
    GateEntry(
        key="PROV-GUARD",
        gate_id="PROV-GUARD",
        extra_ids=(),
        mechanism=_ci("check-provenance"),
        ci_job="check-provenance",
        script="scripts/check-provenance.py",
        run_command=(
            "python3 scripts/check-provenance.py --self-test && "
            "python3 scripts/check-provenance.py"
        ),
        summary=(
            "Every `read-at-source` ground truth in an analysis's section 3 joins to "
            "a real WebFetch/Read of that source in the run's stored capture, and "
            "every literal it states appears verbatim in that source's retrieved "
            "text. Live leg reads `tests/quality-provenance-v8.24/` and reports "
            "7/7 sources matched, 35/35 literals located."
        ),
        consumes=("control_ids", "control_count", "registered_surfaces", "locked_constants"),
    ),
    GateEntry(
        key="HARN-01",
        gate_id="HARN-01",
        extra_ids=(),
        mechanism=_ci("check-act-limb"),
        ci_job="check-act-limb",
        script="scripts/check-act-limb.py",
        run_command="python3 scripts/check-act-limb.py --self-test",
        summary=(
            "Offline Act-limb gate: the Phase 3 verification step and the "
            "Criterion 3 Fix note are present, correctly placed, and internally "
            "coherent in the emitted tree."
        ),
        consumes=("branch_roster", "branch_count", "control_ids", "control_count", "checked_files", "disclosed_bounds_anchors"),
    ),
    GateEntry(
        key="HARN-02",
        gate_id="HARN-02",
        extra_ids=(),
        mechanism=_ci("check-loop-closure"),
        ci_job="check-loop-closure",
        script="scripts/check-loop-closure.py",
        run_command="python3 scripts/check-loop-closure.py --self-test",
        summary=(
            "Observe->Perceive re-entry edges: a Criterion 1 Absent verdict routes "
            "back to Phase 1, every re-entry edge is bounded to one re-perception "
            "pass, and a fired edge is recorded."
        ),
        consumes=("checked_files", "control_ids", "control_count"),
    ),
    GateEntry(
        key="HARN-03",
        gate_id="HARN-03",
        extra_ids=(),
        mechanism=_ci("check-focused-parity"),
        ci_job="check-focused-parity",
        script="scripts/check-focused-parity.py",
        run_command="python3 scripts/check-focused-parity.py --self-test",
        summary=(
            "Focused-mode parity: stub surface, agent surface and cross-surface "
            "parity-token set equality, with the D-12 anchor-control ratchet."
        ),
        consumes=("locked_constants", "registered_surfaces", "disclosed_bounds_anchors"),
    ),
    GateEntry(
        key="SCAN-GUARD",
        gate_id="SCAN-GUARD",
        extra_ids=(),
        mechanism=_ci("check-selfaudit-scan"),
        ci_job="check-selfaudit-scan",
        script="scripts/check-selfaudit-scan.py",
        run_command=(
            "python3 scripts/check-selfaudit-scan.py --self-test && "
            "python3 scripts/check-selfaudit-scan.py"
        ),
        summary=(
            "Self-audit scan structural gate: the Phase 15 self-audit scan "
            "prescription, its rubric verify block, and the Criterion-2-widened "
            "Verdict Block Format admission are present, correctly placed and "
            "internally coherent in the emitted tree, with one hundred clause-level "
            "named branches floored by an independent transcription "
            "(`_BRANCH_ROSTER_LOCK`)."
        ),
        consumes=(
            "branch_roster",
            "branch_count",
            "registered_surfaces",
            "call_site_census",
            "control_ids",
            "control_count",
            "locked_constants",
        ),
    ),
    GateEntry(
        key="HC-BOUND",
        gate_id="HC-BOUND",
        extra_ids=(),
        mechanism=_ci("check-high-confidence-bound"),
        ci_job="check-high-confidence-bound",
        script="scripts/check-high-confidence-bound.py",
        run_command="python3 scripts/check-high-confidence-bound.py --self-test",
        summary=(
            "Structural validation gate: Phase 5 tightening of Criterion 3 "
            "(Evidence) and Criterion 5 (Conclusion) HIGH-confidence bound is "
            "present and well-formed on both rubric surfaces, and all three "
            "documented EXCEPT exceptions are present."
        ),
        consumes=("registered_surfaces", "derived_counts", "disclosed_bounds_anchors"),
    ),
    GateEntry(
        key="CONF-GATE",
        gate_id="CONF-GATE",
        extra_ids=(),
        mechanism=_ci("check-conf-gate"),
        ci_job="check-conf-gate",
        script="scripts/check-conf-gate.py",
        run_command=(
            "python3 scripts/check-conf-gate.py --self-test && "
            "python3 scripts/check-conf-gate.py"
        ),
        summary=(
            "Standing exemplar-conformance comparator: the four conformance counts "
            "on both gated example surfaces against source-literal targets, a "
            "14-entry claim floor locked by equality to the live-discovered "
            "`shared-examples` ids, the D-03 prescribed-lead-in rule, and the "
            "marked-claim ratchet (may fall, never rise)."
        ),
        consumes=(
            "registered_surfaces",
            "population_floors",
            "call_site_census",
            "control_ids",
            "control_count",
            "locked_constants",
        ),
    ),
    GateEntry(
        key="INVARIANT-CHECK",
        gate_id="INVARIANT-CHECK",
        extra_ids=(),
        mechanism="battery only (inline)",
        ci_job=None,
        script=None,
        run_command=(
            "bash scripts/check-firewall-battery.sh  "
            "# INVARIANT-CHECK runs inline; no standalone command"
        ),
        summary=(
            "Anti-masking constants still hold in `scripts/_battery_core.py`: "
            "pre-mortem=9 fishbone=7 inversion=13 trade-off=10 MIN_HEADER_HITS=2. "
            "A direct value-grep double-check of what BATT-06 and STEP0-08 already "
            "assert internally."
        ),
        static_facts={
            "checked_constants": (
                "_TECHNIQUE_CATEGORIES['pre-mortem']",
                "_TECHNIQUE_CATEGORIES['fishbone']",
                "_TECHNIQUE_CATEGORIES['inversion']",
                "_TECHNIQUE_CATEGORIES['trade-off']",
                "MIN_HEADER_HITS",
            ),
            "source": "scripts/_battery_core.py",
        },
    ),
    GateEntry(
        key="FROZEN-EVIDENCE",
        gate_id="FROZEN-EVIDENCE",
        extra_ids=(),
        mechanism="battery only (inline)",
        ci_job=None,
        script=None,
        run_command=(
            "bash scripts/check-firewall-battery.sh  "
            "# FROZEN-EVIDENCE runs inline; no standalone command"
        ),
        summary=(
            "Frozen baselines and captures are unmodified relative to HEAD, plus an "
            "untracked-files sweep over the same paths. `_FROZEN_PATHS` grows over "
            "time; this inline check increments the battery tally once regardless "
            "of array length."
        ),
        static_facts={"source": "scripts/check-firewall-battery.sh:_FROZEN_PATHS"},
    ),
    GateEntry(
        key="PRECOMMIT:sync-drift-gate",
        gate_id=None,
        extra_ids=(),
        mechanism="sync-drift gate (pre-commit)",
        ci_job=None,
        script="scripts/sync-content.py",
        run_command="python3 scripts/sync-content.py --check",
        summary=(
            "`shared/` and the generated tree are in sync — the same check as "
            "DUAL-04, fired before commit rather than in CI/battery."
        ),
    ),
    GateEntry(
        key="PRECOMMIT:conformance-generator-self-test",
        gate_id=None,
        extra_ids=(),
        mechanism="conformance generator self-test (pre-commit)",
        ci_job=None,
        script="scripts/report-conformance.py",
        run_command="python3 scripts/report-conformance.py --self-test",
        summary=(
            "Blocks if `scripts/report-conformance.py --self-test` fails. Runs "
            "the generator's own falsifiability controls before its output is "
            "compared to anything (WR-05) — ordered before `--check` because a "
            "generator whose own controls are failing makes that comparison "
            "meaningless."
        ),
    ),
    GateEntry(
        key="PRECOMMIT:conformance-baseline-drift-gate",
        gate_id=None,
        extra_ids=(),
        mechanism="conformance-baseline drift gate (pre-commit)",
        ci_job=None,
        script="scripts/report-conformance.py",
        run_command="python3 scripts/report-conformance.py --check",
        summary=(
            "`docs/conformance-baseline.md` and `docs/data/conformance.json` "
            "reproduce byte-for-byte a fresh `report-conformance.py` run (D-06); "
            "fires before commit. Deliberately not registered in the battery or "
            "in CI."
        ),
        consumes=("registered_surfaces", "checked_files", "control_ids", "control_count", "locked_constants"),
    ),
    GateEntry(
        key="PRECOMMIT:claim-surface-generator-self-test",
        gate_id=None,
        extra_ids=(),
        mechanism="claim-surface generator self-test (pre-commit)",
        ci_job=None,
        script="scripts/gen-gate-docs.py",
        run_command="python3 scripts/gen-gate-docs.py --self-test",
        summary=(
            "Blocks if `scripts/gen-gate-docs.py --self-test` fails. Same WR-05 "
            "ordering discipline as the conformance generator self-test — a "
            "broken generator's own controls must be caught before its "
            "comparison against committed output (the claim-surface drift "
            "gate) is even attempted."
        ),
    ),
    GateEntry(
        key="PRECOMMIT:claim-surface-drift-gate",
        gate_id=None,
        extra_ids=(),
        mechanism="claim-surface drift gate (pre-commit)",
        ci_job=None,
        script="scripts/gen-gate-docs.py",
        run_command="python3 scripts/gen-gate-docs.py --check",
        summary=(
            "Blocks if `CLAUDE.md`'s/`docs/ARCHITECTURE.md`'s generated gate "
            "tables, `docs/TESTING.md`'s generated index, or any "
            "`docs/gates/<ID>.md` page no longer match a fresh "
            "`scripts/gen-gate-docs.py --write` run, or if CONF-13's standing "
            "literal scanner finds a non-exempt hand-maintained count literal "
            "— the same check as CONF-SURFACE, fired before commit rather "
            "than in CI/battery."
        ),
    ),
    # --- CONF-SURFACE (D-21-C) ---------------------------------------------
    # The claim-surface drift gate. Landed by plan 21-11 into
    # scripts/check-firewall-battery.sh, .github/workflows/validation.yml,
    # and both pre-commit hooks in the same commit that removed it from
    # `_ANTICIPATORY_KEYS` above -- matching D-08's "a generator that cannot
    # describe itself would be the first exception to its own uniformity in
    # the same phase that establishes it."
    GateEntry(
        key="CONF-SURFACE",
        gate_id="CONF-SURFACE",
        extra_ids=(),
        mechanism=_ci("gen-gate-docs"),
        ci_job="gen-gate-docs",
        script="scripts/gen-gate-docs.py",
        run_command=(
            "python3 scripts/gen-gate-docs.py --self-test && "
            "python3 scripts/gen-gate-docs.py --check"
        ),
        summary=(
            "The claim-surface drift gate itself: regenerates `CLAUDE.md`'s and "
            "docs/ARCHITECTURE.md's gate tables and docs/gates/<ID>.md pages from "
            "this registry's ENTRIES and every gate's --describe emission, and "
            "fails on drift. Registered in the battery, with a matching "
            "`gen-gate-docs (CONF-SURFACE)` CI job and both pre-commit hooks "
            "(plan 21-11, D-21-C)."
        ),
        consumes=(
            "registered_surfaces",
            "checked_files",
            "derived_counts",
            "disclosed_bounds_anchors",
            "control_ids",
            "control_count",
            "locked_constants",
        ),
    ),
)


# ---------------------------------------------------------------------------
# D-01: battery-id equality floor
# ---------------------------------------------------------------------------

# Same regex semantics as scripts/check-registration.py's `_BATTERY_GATE_RE`
# (reused deliberately, per this plan's own read_first instruction, rather
# than inventing a second grammar over the same file). Not imported: this
# module must not execute or import another gate script (D-21-A / T-21-02-05
# forbids it) — a bare regex with the identical pattern is copied text, not a
# code dependency, and check-registration.py's own self-test already proves
# this exact pattern's behavior against the real file.
_BATTERY_GATE_RE = re.compile(r'^[ \t]*gate(?:_prereq)?[ \t]+"([^"]+)"', re.MULTILINE)


def battery_gate_ids(battery_src: str) -> tuple[str, ...]:
    """Pure regex extraction over the battery script's own source text.

    Matches both `gate "<ID>"` and `gate_prereq "<ID>"` registration lines,
    de-duplicated with order preserved — VAL-03 registers under EITHER helper
    depending on pytest-interpreter resolution (never both in the same run,
    but the source text contains both call sites), and that is one gate, not
    two.

    Takes the source text, not a path, so --self-test can drive it against
    synthetic fixtures without touching disk.
    """
    seen: list[str] = []
    for gate_id in _BATTERY_GATE_RE.findall(battery_src):
        if gate_id not in seen:
            seen.append(gate_id)
    return tuple(seen)


def registry_id_problems(
    entry_ids: frozenset[str],
    derived_ids: frozenset[str],
    precommit_ids: frozenset[str],
) -> list[str]:
    """D-01's two-directional equality floor, both directions reported in one run.

    `entry_ids` is the set of PRIMARY `gate_id`s the registry declares
    (never `extra_ids` — those are additional names the same row carries,
    not a second battery registration; see `GateEntry.extra_ids`'s
    docstring). `derived_ids` is `battery_gate_ids()`'s output. `precommit_ids`
    names the pre-commit mechanism rows' synthetic keys explicitly so they
    are excluded from the comparison BY CONSTRUCTION — a pre-commit row has
    no battery registration to agree or disagree with, and folding it into
    `entry_ids` unfiltered would make it look like a battery id the battery
    never registers.

    `precommit_ids` also carries the two truly-inline battery checks
    (`INVARIANT-CHECK`, `FROZEN-EVIDENCE`) alongside the five pre-commit
    mechanism rows — all seven increment a battery/pre-commit tally directly
    rather than through a `gate "<ID>"` / `gate_prereq "<ID>"` call
    `battery_gate_ids()` can see, so all seven must be excluded from this
    comparison by construction, not merely by convention.

    Pure: does no I/O. Reports `missing=` (battery has it, registry lacks
    it) and `extra=` (registry has it, battery lacks it) in the SAME run, so
    a fix for one direction cannot mask the other (D-04's own bidirectional
    lesson, applied here to the id axis first).
    """
    problems: list[str] = []
    comparable = entry_ids - precommit_ids
    missing = derived_ids - comparable
    extra = comparable - derived_ids
    if missing:
        problems.append(
            "D-01: battery registers gate id(s) with no registry entry: "
            f"{sorted(missing)}"
        )
    if extra:
        problems.append(
            "D-01: registry names gate id(s) the battery does not register: "
            f"{sorted(extra)}"
        )
    return problems


def _registry_entry_ids() -> frozenset[str]:
    """Primary gate ids ENTRIES declares, excluding anticipatory entries.

    CONF-SURFACE (D-21-C) is not yet battery-registered — including it here
    would make the D-01 floor report a phantom `extra=`. `_ANTICIPATORY_KEYS`
    is the single named exclusion list; nothing else is filtered.
    """
    return frozenset(
        e.gate_id
        for e in ENTRIES
        if e.gate_id is not None and e.key not in _ANTICIPATORY_KEYS
    )


def _registry_precommit_ids() -> frozenset[str]:
    """Ids excluded from the D-01 battery-gate-id equality floor: the five
    pre-commit mechanism rows' synthetic keys (no gate id, no battery
    registration to compare against at all) AND the two truly-inline
    battery checks, `INVARIANT-CHECK` and `FROZEN-EVIDENCE`, which increment
    the battery's PASS/FAIL/TOTAL tally directly rather than through a
    `gate "<ID>"` / `gate_prereq "<ID>"` call — `battery_gate_ids()`
    structurally cannot see either, so leaving them in the comparison set
    would report both as a phantom `extra=` forever."""
    precommit_keys = frozenset(
        e.key
        for e in ENTRIES
        if e.gate_id is None and e.key.startswith("PRECOMMIT:")
    )
    return precommit_keys | frozenset({"INVARIANT-CHECK", "FROZEN-EVIDENCE"})


# ---------------------------------------------------------------------------
# CR-04: pre-commit hook-roster floor — derives the five `PRECOMMIT:` rows'
# `run_command` set from both hook scripts' own source text, rather than
# trusting the registry to have transcribed them correctly.
# ---------------------------------------------------------------------------

# The two hook relpaths that must run the identical five-gate sequence in
# the identical order (both files' own header comments assert this; nothing
# checked it before this plan). Named here, not re-typed at each call site.
_HOOK_PATHS: tuple[str, str] = (".githooks/pre-commit", "scripts/git-hooks/pre-commit")

# The three literal message prefixes `hook_roster_problems()` emits, shared
# by the producer (below) and `_hook_roster_arm_clauses`' parser so the two
# cannot drift apart. A message-format change on the producer side must fail
# loudly at the parser rather than degrade into whole-message blindness —
# that is the boundary the pre-plan-21-21 shape crossed silently.
_HOOK_DIVERGENCE_PREFIX = "hook-divergence: "
_HOOK_ROSTER_MISSING_PREFIX = "hook-roster missing=: "
_HOOK_ROSTER_EXTRA_PREFIX = "hook-roster extra=: "

# Matches a `(?:exec )?$PY <script> <flag>` invocation line — the shape both
# hook scripts use for every one of their five gates (the terminal line uses
# `exec`, the other four use `|| exit $?`, which this pattern ignores since
# it only needs the script and the leading flag).
_HOOK_GATE_INVOCATION_RE = re.compile(
    r'^[ \t]*(?:exec[ \t]+)?\$PY[ \t]+(scripts/\S+)[ \t]+(--\S+)',
    re.MULTILINE,
)


def hook_gate_invocations(hook_src: str) -> tuple[str, ...]:
    """Derive the ordered sequence of hook-gate invocations from a hook
    script's own source TEXT (not a path) — the same signature discipline
    `battery_gate_ids()` uses, so a control can drive it against synthetic
    fixtures with no disk I/O.

    Normalises `$PY` to `python3` at the comparison boundary, not by
    re-typing the commands: the hooks resolve `$PY` to `uv run python3` or
    `python3` at runtime, but every registry `run_command` is always written
    in the `python3 <script> <flag>` form, so this is where the two
    vocabularies are reconciled.
    """
    return tuple(
        f"python3 {script} {flag}"
        for script, flag in _HOOK_GATE_INVOCATION_RE.findall(hook_src)
    )


def hook_roster_problems(
    hook_a_invocations: tuple[str, ...] | None = None,
    hook_b_invocations: tuple[str, ...] | None = None,
    registry_run_commands: frozenset[str] | None = None,
) -> list[str]:
    """CR-04's derived pre-commit hook floor, reported in ONE run and never
    short-circuited (the same bidirectional-report discipline
    `registry_id_problems()` and `field_resolution_problems()` already use):

      (a) `hook_a_invocations == hook_b_invocations` — a hook gate edited in
          one file only is a finding, the lockstep property both hooks'
          header comments assert but nothing previously checked;
      (b) the union of both hooks' invocations equals `registry_run_commands`
          — reported as `missing=` (a hook gate with no `PRECOMMIT:` registry
          row) and `extra=` (a registry row naming an invocation neither
          hook makes).

    Every argument defaults to a LIVE read (both real hook files via
    `_HOOK_PATHS`, and the real `PRECOMMIT:` `run_command` set from
    `ENTRIES`) so this function can be called with no arguments for the live
    check. Passing explicit tuples/sets — as the missing=/extra=/divergence
    self-test arms do — makes the call pure with no disk I/O, exercising the
    same comparison logic against synthetic fixtures.
    """
    if hook_a_invocations is None:
        hook_a_invocations = hook_gate_invocations(
            (REPO_ROOT / _HOOK_PATHS[0]).read_text(encoding="utf-8")
        )
    if hook_b_invocations is None:
        hook_b_invocations = hook_gate_invocations(
            (REPO_ROOT / _HOOK_PATHS[1]).read_text(encoding="utf-8")
        )
    if registry_run_commands is None:
        registry_run_commands = frozenset(
            e.run_command for e in ENTRIES if e.key.startswith("PRECOMMIT:")
        )
    problems: list[str] = []
    if hook_a_invocations != hook_b_invocations:
        problems.append(
            _HOOK_DIVERGENCE_PREFIX
            + "the two hook scripts' derived invocation "
            f"sequences differ: {list(hook_a_invocations)} != "
            f"{list(hook_b_invocations)}"
        )
    derived = frozenset(hook_a_invocations) | frozenset(hook_b_invocations)
    missing = derived - registry_run_commands
    extra = registry_run_commands - derived
    if missing:
        problems.append(
            _HOOK_ROSTER_MISSING_PREFIX
            + "hook gate(s) with no PRECOMMIT: registry "
            f"row: {sorted(missing)}"
        )
    if extra:
        problems.append(
            _HOOK_ROSTER_EXTRA_PREFIX
            + "PRECOMMIT: registry row(s) naming an "
            f"invocation neither hook makes: {sorted(extra)}"
        )
    return problems


class HookRosterClauses(NamedTuple):
    """The payload clauses `_hook_roster_arm_clauses` extracts from a
    `hook_roster_problems()` findings list — named fields rather than a
    widened positional tuple, so every call site reads as what it asserts
    and a future field cannot be silently mis-positioned."""

    missing: str
    extra: str
    divergence: str


def _hook_roster_arm_clauses(problems: list[str]) -> HookRosterClauses:
    """Split a `hook_roster_problems()` findings list into its `missing=`,
    `extra=` and hook-divergence payload clauses, porting
    `check-version-stamps.py`'s `_roster_arm_clauses` idiom to this
    producer's SEPARATE-list-entry message grammar rather than a single
    joined string.

    Four legs, each raising `ValueError` naming the offending text rather
    than silently degrading to whole-message blindness:

      1. every entry must start with exactly one of the three declared
         prefixes (`_HOOK_DIVERGENCE_PREFIX`, `_HOOK_ROSTER_MISSING_PREFIX`,
         `_HOOK_ROSTER_EXTRA_PREFIX`); an unrecognised entry raises.
      2. no single entry may carry BOTH the missing= and extra= clause
         markers — the combined-message shape a message-construction
         refactor could reintroduce, and the one this helper exists to
         catch, checked via a `not in` precondition rather than the bare
         `in`-membership-against-a-whole-message shape the census below
         forbids.
      3. no prefix may appear on more than one entry.
      4. otherwise return a `HookRosterClauses(missing, extra, divergence)`
         — the payload following each roster/divergence prefix, and the
         empty string when that finding is absent.
    """
    missing_clause = ""
    extra_clause = ""
    divergence_clause = ""
    seen_missing = False
    seen_extra = False
    seen_divergence = False
    for entry in problems:
        if entry.startswith(_HOOK_ROSTER_MISSING_PREFIX):
            if "extra=" not in entry:
                if seen_missing:
                    raise ValueError(
                        "_hook_roster_arm_clauses: missing= prefix appears "
                        f"on more than one entry: {entry!r}"
                    )
                seen_missing = True
                missing_clause = entry.removeprefix(_HOOK_ROSTER_MISSING_PREFIX)
            else:
                raise ValueError(
                    "_hook_roster_arm_clauses: entry carries both roster "
                    f"clause markers: {entry!r}"
                )
        elif entry.startswith(_HOOK_ROSTER_EXTRA_PREFIX):
            if "missing=" not in entry:
                if seen_extra:
                    raise ValueError(
                        "_hook_roster_arm_clauses: extra= prefix appears "
                        f"on more than one entry: {entry!r}"
                    )
                seen_extra = True
                extra_clause = entry.removeprefix(_HOOK_ROSTER_EXTRA_PREFIX)
            else:
                raise ValueError(
                    "_hook_roster_arm_clauses: entry carries both roster "
                    f"clause markers: {entry!r}"
                )
        elif entry.startswith(_HOOK_DIVERGENCE_PREFIX):
            if seen_divergence:
                raise ValueError(
                    "_hook_roster_arm_clauses: hook-divergence prefix "
                    f"appears on more than one entry: {entry!r}"
                )
            seen_divergence = True
            divergence_clause = entry.removeprefix(_HOOK_DIVERGENCE_PREFIX)
        else:
            raise ValueError(
                "_hook_roster_arm_clauses: entry does not start with a "
                f"recognised prefix: {entry!r}"
            )
    return HookRosterClauses(missing_clause, extra_clause, divergence_clause)


# ---------------------------------------------------------------------------
# D-04: bidirectional field-resolution floor + the closed field vocabulary
# ---------------------------------------------------------------------------

# The closed set of field names any --describe limb may emit, and what each
# name must mean. A script must not know its own gate ids (D-03), so field
# names name KINDS OF FACT, never gate identities. Batch plans 21-03/04/05
# extend this dict in the SAME commit as the limb that emits the new name —
# an undocumented member is treated as a defect by this module's own
# self-test (see `_control_vocabulary_members_documented`).
_FIELD_DESCRIPTIONS: dict[str, str] = {
    "control_ids": (
        "the second, independently-typed roster of self-test control ids "
        "(the `_CONTROL_IDS` shape) — a sorted list of strings"
    ),
    "control_count": (
        "len() of the emitting script's own executed-control roster; a derived "
        "int, never hand-typed"
    ),
    "branch_roster": (
        "a sorted list of named branch/check ids a gate's structural assertions "
        "are organized around (the `_BRANCH_ROSTER_LOCK` / `REQUIRED_BRANCHES` "
        "shape)"
    ),
    "branch_count": "len() of branch_roster; a derived int, never hand-typed",
    "registered_surfaces": (
        "a sorted list of file relpaths a gate declares it reads/asserts "
        "against (the `COVERED_HEADLINE_SURFACES` / `_GATED_SURFACES` shape)"
    ),
    "population_floors": (
        "a mapping of population-name -> minimum count a gate's zero-target "
        "assertions are floored against, so a zero achieved by shrinking the "
        "measured population is distinguishable from a zero achieved by fixing "
        "the defect"
    ),
    "call_site_census": (
        "a mapping of symbol-name -> observed call-site count from a gate's own "
        "source-text census (the `_LIVE_CALL_SITES` / `_CORPUS_CALL_SITES` shape)"
    ),
    "scan_globs": (
        "a sorted list of glob patterns a tree-wide scanner reads (the "
        "`HEADLINE_SCAN_GLOBS` / `FULL_CHECK_GLOBS` shape)"
    ),
    "frozen_paths": (
        "a sorted list of pathspecs a gate asserts are byte-frozen relative to "
        "HEAD (the `_FROZEN_PATHS` shape)"
    ),
    "disclosed_bounds_anchors": (
        "a sorted list of short identifiers naming a gate's own disclosed "
        "bounds/limitations, so a detail page can enumerate them without "
        "restating their prose"
    ),
    "checked_files": (
        "a sorted list of file relpaths a gate's live leg actually opened this "
        "run (the `read_relpaths` shape) — distinct from `registered_surfaces`, "
        "which is a DECLARED set, not an observed one"
    ),
    "self_test_dispatch_anchors": (
        "a sorted list of `_selftest_*`/`_self_test_*` symbol names a gate "
        "asserts are CALLED from a top-level dispatcher, not merely defined"
    ),
    "run_commands": (
        "a mapping of leg-name -> the exact command a reader would run for that "
        "leg (self-test, live, etc.) — for gates with more than one leg where a "
        "single `run_command` on the registry entry is not granular enough"
    ),
    "derived_counts": (
        "a mapping of count-name -> len()-derived integer a gate publishes; "
        "every value must trace to a live len() (or an inspect.signature "
        "default, for a width/threshold baked into a function signature "
        "rather than a container), never a hand-typed literal"
    ),
    "locked_constants": (
        "a mapping of constant-name -> the literal value (str/int/bool) a "
        "gate asserts against, read directly from the emitting script's own "
        "module constant — the schema-lock shape (_EXPECTED_NAME, CAP, "
        "GENERATED_MARKER, PLUGIN_ROOT_TOKEN)"
    ),
    "scoped_branches": (
        "a sorted list of branch_roster entries (by description text) that "
        "are skipped under a named alternate invocation mode (e.g. "
        "--skip-name-check), so the scoping itself is derivable rather than "
        "restated in prose"
    ),
    "coverage_headline": (
        "a mapping with 'slash' and 'prose' keys holding the two live "
        "renderings of the traceability coverage headline, re-derived from "
        "build_matrix_rows() on every call (the check-traceability.py "
        "_headline_literals() shape) — deliberately NOT locked, since the "
        "headline must keep moving the instant a matrix row is registered "
        "or re-tiered"
    ),
    "contract_pins": (
        "a mapping of frozen-function-name -> {'digest': the pinned "
        "sha256:<hex> literal, 'line_count': int} for every CONTRACT-06 "
        "sha256-pinned function this gate carries — both values are READ "
        "from the pin's own module constant and a pre-existing single-"
        "call-site source wrapper, never recomputed inside describe()"
    ),
}

DESCRIBE_FIELD_VOCABULARY: frozenset[str] = frozenset(_FIELD_DESCRIPTIONS)


def vocabulary_problems(emitted: dict[str, frozenset[str]]) -> list[str]:
    """A --describe limb emitting a field name outside the closed vocabulary
    is a named failure — this is what keeps the vocabulary closed rather
    than aspirational. `emitted` is keyed by script relpath, matching
    `field_resolution_problems()`'s shape."""
    problems: list[str] = []
    for script, fields in sorted(emitted.items()):
        bogus = sorted(f for f in fields if f not in DESCRIBE_FIELD_VOCABULARY)
        for name in bogus:
            problems.append(
                f"vocabulary_problems: {script} emits undeclared field "
                f"'{name}' (not in DESCRIBE_FIELD_VOCABULARY)"
            )
    return problems


def field_resolution_problems(
    requested: dict[str, frozenset[str]],
    emitted: dict[str, frozenset[str]],
) -> list[str]:
    """D-04's bidirectional equality floor, keyed by script relpath.

    `requested[script]` is the union of `consumes` fields every registry
    entry backed by that script declares it reads. `emitted[script]` is what
    that script's live `--describe` actually produced.

    Both directions are reported in the SAME run:
      - `requested - emitted`: a registry entry asks for a field its script
        never emits -> one problem per missing field, naming both.
      - `emitted - requested`: a script computes a field no registry entry or
        detail page reads -> one problem per unconsumed field, naming both.
    This is what catches "a row that quietly stops rendering a count while
    the script still computes it" — a missing-only check cannot see that
    direction, in exactly the way a subset test could not see its own table
    narrowing (19-D-04, CR-03).

    No exemption list (D-04 explicitly holds that in reserve, not adopted
    pre-emptively): a genuine unconsumed constant is fixed by adding a
    consumer, not by suppressing the finding.
    """
    problems: list[str] = []
    scripts = sorted(set(requested) | set(emitted))
    for script in scripts:
        req = requested.get(script, frozenset())
        emit = emitted.get(script, frozenset())
        for field_name in sorted(req - emit):
            problems.append(
                f"D-04: {script} — registry entry requests field '{field_name}' "
                "but the script's --describe does not emit it"
            )
        for field_name in sorted(emit - req):
            problems.append(
                f"D-04: {script} — --describe emits field '{field_name}' but no "
                "registry entry or detail page consumes it"
            )
    return problems


def _requested_fields_by_script() -> dict[str, frozenset[str]]:
    """Derive `requested` (D-04's first argument) from ENTRIES' own `consumes`
    tuples — never hand-typed a second time."""
    out: dict[str, set[str]] = {}
    for entry in ENTRIES:
        if entry.script is None or not entry.consumes:
            continue
        out.setdefault(entry.script, set()).update(entry.consumes)
    return {script: frozenset(fields) for script, fields in out.items()}


# ---------------------------------------------------------------------------
# --self-test
# ---------------------------------------------------------------------------


def _control_d01_id_missing_from_registry() -> None:
    battery_src = 'gate "REAL-ONE" "x" "true"\ngate "MISSING-ONE" "x" "true"\n'
    derived = frozenset(battery_gate_ids(battery_src))
    registry = frozenset({"REAL-ONE"})
    problems = registry_id_problems(registry, derived, frozenset())
    assert len(problems) == 1, problems
    assert "MISSING-ONE" in problems[0], problems
    assert "battery registers" in problems[0], problems


def _control_d01_id_extra_in_registry() -> None:
    battery_src = 'gate "REAL-ONE" "x" "true"\n'
    derived = frozenset(battery_gate_ids(battery_src))
    registry = frozenset({"REAL-ONE", "EXTRA-ONE"})
    problems = registry_id_problems(registry, derived, frozenset())
    assert len(problems) == 1, problems
    assert "EXTRA-ONE" in problems[0], problems
    assert "registry names" in problems[0], problems


def _control_d01_id_equal_passes() -> None:
    battery_src = 'gate "A" "x" "true"\ngate "B" "x" "true"\n'
    derived = frozenset(battery_gate_ids(battery_src))
    registry = frozenset({"A", "B"})
    problems = registry_id_problems(registry, derived, frozenset())
    assert problems == [], problems


def _control_d01_gate_prereq_recognised() -> None:
    battery_src = 'gate_prereq "SOLO" "x" "reason" "true"\n'
    derived = battery_gate_ids(battery_src)
    assert derived == ("SOLO",), derived


def _control_d01_precommit_excluded() -> None:
    battery_src = 'gate "A" "x" "true"\n'
    derived = frozenset(battery_gate_ids(battery_src))
    registry = frozenset({"A", "PRECOMMIT:thing"})
    problems = registry_id_problems(
        registry, derived, frozenset({"PRECOMMIT:thing"})
    )
    assert problems == [], problems
    # And WITHOUT the exclusion, the same registry set would report the
    # precommit key as a phantom "extra" battery id — proving the exclusion
    # is load-bearing, not decorative.
    unfiltered_problems = registry_id_problems(registry, derived, frozenset())
    assert len(unfiltered_problems) == 1, unfiltered_problems
    assert "PRECOMMIT:thing" in unfiltered_problems[0], unfiltered_problems


def _control_d01_live_battery_equality() -> None:
    """Live equality against the real check-firewall-battery.sh."""
    battery_src = BATTERY_PATH.read_text(encoding="utf-8")
    derived = frozenset(battery_gate_ids(battery_src))
    problems = registry_id_problems(
        _registry_entry_ids(), derived, _registry_precommit_ids()
    )
    assert problems == [], problems


def _control_cr04_hook_roster_live_positive() -> None:
    """CR-04's positive arm, over the REAL hook text: both hook scripts
    derive exactly five invocations each, the two sequences agree, and they
    equal the five `PRECOMMIT:` registry rows' `run_command` set. Called
    with zero arguments — the same live-default call shape a developer or
    the pre-commit hook itself would use. Its three sibling negative arms
    below now parse `hook_roster_problems()`'s findings through
    `_hook_roster_arm_clauses` rather than testing a bare clause-marker
    substring against the whole message."""
    problems = hook_roster_problems()
    assert problems == [], problems
    hook_a = hook_gate_invocations(
        (REPO_ROOT / _HOOK_PATHS[0]).read_text(encoding="utf-8")
    )
    hook_b = hook_gate_invocations(
        (REPO_ROOT / _HOOK_PATHS[1]).read_text(encoding="utf-8")
    )
    assert len(hook_a) == 5, hook_a
    assert len(hook_b) == 5, hook_b
    assert hook_a == hook_b, (hook_a, hook_b)


def _control_cr04_hook_roster_missing_fires() -> None:
    """FALSIFICATION, `missing=` direction: a synthetic sixth invocation line
    appended to a COPY of the real hook source text must produce a finding
    naming the offending command by name."""
    real_hook_src = (REPO_ROOT / _HOOK_PATHS[0]).read_text(encoding="utf-8")
    synthetic_hook_src = (
        real_hook_src + "\n$PY scripts/check-agent.py --self-test || exit $?\n"
    )
    synthetic_invocations = hook_gate_invocations(synthetic_hook_src)
    assert "python3 scripts/check-agent.py --self-test" in synthetic_invocations, (
        synthetic_invocations
    )
    registry_commands = frozenset(
        e.run_command for e in ENTRIES if e.key.startswith("PRECOMMIT:")
    )
    problems = hook_roster_problems(
        synthetic_invocations, synthetic_invocations, registry_commands
    )
    assert len(problems) == 1, problems
    clauses = _hook_roster_arm_clauses(problems)
    assert "python3 scripts/check-agent.py --self-test" in clauses.missing, problems
    assert clauses.extra == "", problems


def _control_cr04_hook_roster_extra_fires() -> None:
    """FALSIFICATION, `extra=` direction: a registry roster naming a
    fabricated invocation the real hook text does not make must produce a
    finding naming that offending command by name."""
    real_hook_src = (REPO_ROOT / _HOOK_PATHS[0]).read_text(encoding="utf-8")
    real_invocations = hook_gate_invocations(real_hook_src)
    fabricated_commands = frozenset(real_invocations) | frozenset(
        {"python3 scripts/check-links.py --check"}
    )
    problems = hook_roster_problems(
        real_invocations, real_invocations, fabricated_commands
    )
    assert len(problems) == 1, problems
    clauses = _hook_roster_arm_clauses(problems)
    assert "python3 scripts/check-links.py --check" in clauses.extra, problems
    assert clauses.missing == "", problems


def _control_cr04_hook_roster_divergence_fires() -> None:
    """FALSIFICATION, hook-divergence direction: two synthetic hook texts
    differing by one invocation line must produce a finding naming the
    differing command, even when the registry roster covers the union of
    both (isolating the divergence arm from the missing=/extra= arms)."""
    hook_a_src = (
        "$PY scripts/sync-content.py --check || exit $?\n"
        "$PY scripts/report-conformance.py --self-test || exit $?\n"
    )
    hook_b_src = (
        "$PY scripts/sync-content.py --check || exit $?\n"
        "$PY scripts/report-conformance.py --check || exit $?\n"
    )
    inv_a = hook_gate_invocations(hook_a_src)
    inv_b = hook_gate_invocations(hook_b_src)
    assert inv_a != inv_b, (inv_a, inv_b)
    registry_commands = frozenset(inv_a) | frozenset(inv_b)
    problems = hook_roster_problems(inv_a, inv_b, registry_commands)
    assert len(problems) == 1, problems
    assert problems[0].startswith(_HOOK_DIVERGENCE_PREFIX), problems
    clauses = _hook_roster_arm_clauses(problems)
    assert clauses.missing == "", problems
    assert clauses.extra == "", problems
    assert "python3 scripts/report-conformance.py --self-test" in clauses.divergence, (
        clauses
    )
    assert "python3 scripts/report-conformance.py --check" in clauses.divergence, clauses


def _control_cr04_hook_roster_arm_shape_guard() -> None:
    """Message-shape guard, mirroring `check-version-stamps.py`'s
    `kind-roster-arm-shape-guard` control: `_hook_roster_arm_clauses` must
    raise `ValueError` naming the offending text on every malformed shape,
    return an all-empty `HookRosterClauses` for an empty list, and split a
    well-formed list correctly.

    Every fixture here is assembled from the shared `_HOOK_*_PREFIX`
    constants rather than a quoted marker literal — not a defence against
    the fixture splitting across physical source lines (this file carries
    no `"missing="`/`"extra="` string literal at all), but because building
    every fixture from the same constants the producer emits is what keeps
    producer and parser from drifting apart: a rename of any prefix
    constant breaks both sides identically, at the same edit, rather than
    the fixture continuing to build a message the real producer no longer
    emits (21-24, correcting a prior IN-03 finding that misattributed this
    to a self-match defence against plan 21-22's census)."""
    # (a) a single entry carrying both clause markers, reached through the
    # missing= branch.
    both_markers_entry_missing = (
        _HOOK_ROSTER_MISSING_PREFIX
        + "fixture-command-a "
        + _HOOK_ROSTER_EXTRA_PREFIX
        + "fixture-command-b"
    )
    try:
        _hook_roster_arm_clauses([both_markers_entry_missing])
    except ValueError as exc:
        assert "fixture-command-a" in str(exc), exc
    else:
        assert False, (
            "_hook_roster_arm_clauses accepted an entry carrying both "
            "roster clause markers (missing= branch)"
        )

    # (b) an entry with an unrecognised prefix.
    try:
        _hook_roster_arm_clauses(["unrecognised-prefix: fixture-command-c"])
    except ValueError as exc:
        assert "unrecognised-prefix" in str(exc), exc
    else:
        assert False, "_hook_roster_arm_clauses accepted an unrecognised prefix"

    # (c) two entries sharing the missing= prefix.
    try:
        _hook_roster_arm_clauses(
            [
                _HOOK_ROSTER_MISSING_PREFIX + "fixture-command-d",
                _HOOK_ROSTER_MISSING_PREFIX + "fixture-command-e",
            ]
        )
    except ValueError as exc:
        assert "fixture-command-e" in str(exc), exc
    else:
        assert False, (
            "_hook_roster_arm_clauses accepted two entries sharing the "
            "missing= prefix"
        )

    # (d) two entries sharing the extra= prefix (line 1006's raise site,
    # the mirror of arm (c) on the extra= branch).
    try:
        _hook_roster_arm_clauses(
            [
                _HOOK_ROSTER_EXTRA_PREFIX + "fixture-command-h",
                _HOOK_ROSTER_EXTRA_PREFIX + "fixture-command-i",
            ]
        )
    except ValueError as exc:
        assert "fixture-command-i" in str(exc), exc
    else:
        assert False, (
            "_hook_roster_arm_clauses accepted two entries sharing the "
            "extra= prefix"
        )

    # (e) two hook-divergence entries (line 1019's raise site).
    try:
        _hook_roster_arm_clauses(
            [
                _HOOK_DIVERGENCE_PREFIX + "fixture-command-j",
                _HOOK_DIVERGENCE_PREFIX + "fixture-command-k",
            ]
        )
    except ValueError as exc:
        assert "hook-divergence" in str(exc), exc
    else:
        assert False, (
            "_hook_roster_arm_clauses accepted two hook-divergence entries"
        )

    # (f) a single entry carrying both clause markers, reached through the
    # extra= branch (line 1013's raise site — an entry starting with the
    # extra prefix that also carries the missing marker, the mirror of arm
    # (a); today's only both-markers coverage runs through the missing
    # branch).
    both_markers_entry_extra = (
        _HOOK_ROSTER_EXTRA_PREFIX
        + "fixture-command-l "
        + _HOOK_ROSTER_MISSING_PREFIX
        + "fixture-command-m"
    )
    try:
        _hook_roster_arm_clauses([both_markers_entry_extra])
    except ValueError as exc:
        assert "fixture-command-l" in str(exc), exc
    else:
        assert False, (
            "_hook_roster_arm_clauses accepted an entry carrying both "
            "roster clause markers (extra= branch)"
        )

    # Empty list returns an all-empty HookRosterClauses.
    assert _hook_roster_arm_clauses([]) == ("", "", ""), _hook_roster_arm_clauses([])

    # Well-formed two-entry list returns the correct clause split.
    clauses = _hook_roster_arm_clauses(
        [
            _HOOK_ROSTER_MISSING_PREFIX + "fixture-command-f",
            _HOOK_ROSTER_EXTRA_PREFIX + "fixture-command-g",
        ]
    )
    assert clauses.missing == "fixture-command-f", clauses
    assert clauses.extra == "fixture-command-g", clauses
    assert clauses.divergence == "", clauses


def _parse_architecture_data_row_count() -> int:
    """Parse docs/ARCHITECTURE.md's 'CI and pre-commit gate inventory' table
    live and return its data-row count (excludes the header and separator
    rows). Never hand-typed — a control below asserts len(ENTRIES) (minus
    the anticipatory entries) equals this parsed figure."""
    text = ARCHITECTURE_PATH.read_text(encoding="utf-8")
    lines = text.splitlines()
    header_idx = None
    for i, line in enumerate(lines):
        if line.strip() == "| Gate | Job / Mechanism | Script | What it checks |":
            header_idx = i
            break
    assert header_idx is not None, "gate inventory table header not found"
    # lines[header_idx] = header, lines[header_idx + 1] = separator (|---|...)
    row_count = 0
    i = header_idx + 2
    while i < len(lines) and lines[i].startswith("|"):
        row_count += 1
        i += 1
    return row_count


def _control_entries_count_matches_architecture_table() -> None:
    documented = [e for e in ENTRIES if e.key not in _ANTICIPATORY_KEYS]
    parsed = _parse_architecture_data_row_count()
    assert len(documented) == parsed, (
        f"len(documented ENTRIES)={len(documented)} != "
        f"docs/ARCHITECTURE.md data rows={parsed}"
    )
    assert len(ENTRIES) == parsed + len(_ANTICIPATORY_KEYS), (
        f"len(ENTRIES)={len(ENTRIES)} != parsed({parsed}) + "
        f"anticipatory({len(_ANTICIPATORY_KEYS)})"
    )


def _control_no_gate_id_duplicated() -> None:
    ids = [e.gate_id for e in ENTRIES if e.gate_id is not None]
    assert len(ids) == len(set(ids)), f"duplicate gate_id in ENTRIES: {ids}"
    keys = [e.key for e in ENTRIES]
    assert len(keys) == len(set(keys)), f"duplicate key in ENTRIES: {keys}"


def _control_d04_missing_field_fires() -> None:
    requested = {"scripts/x.py": frozenset({"branch_count"})}
    emitted: dict[str, frozenset[str]] = {"scripts/x.py": frozenset()}
    problems = field_resolution_problems(requested, emitted)
    assert len(problems) == 1, problems
    assert "scripts/x.py" in problems[0] and "branch_count" in problems[0], problems


def _control_d04_unconsumed_field_fires() -> None:
    requested: dict[str, frozenset[str]] = {}
    emitted = {"scripts/x.py": frozenset({"call_site_census"})}
    problems = field_resolution_problems(requested, emitted)
    assert len(problems) == 1, problems
    assert "scripts/x.py" in problems[0] and "call_site_census" in problems[0], problems


def _control_d04_both_directions_in_one_run() -> None:
    requested = {"scripts/x.py": frozenset({"branch_count"})}
    emitted = {"scripts/x.py": frozenset({"call_site_census"})}
    problems = field_resolution_problems(requested, emitted)
    assert len(problems) == 2, problems
    joined = " ".join(problems)
    assert "branch_count" in joined and "call_site_census" in joined, problems


def _control_d04_equal_passes() -> None:
    requested = {"scripts/x.py": frozenset({"branch_count", "control_count"})}
    emitted = {"scripts/x.py": frozenset({"branch_count", "control_count"})}
    problems = field_resolution_problems(requested, emitted)
    assert problems == [], problems


def _control_d04_vocabulary_violation_fires() -> None:
    emitted = {"scripts/x.py": frozenset({"bogus_field"})}
    problems = vocabulary_problems(emitted)
    assert len(problems) == 1, problems
    assert "bogus_field" in problems[0], problems


def _control_vocabulary_members_documented() -> None:
    assert DESCRIBE_FIELD_VOCABULARY, "vocabulary must not be empty"
    for name in DESCRIBE_FIELD_VOCABULARY:
        description = _FIELD_DESCRIPTIONS.get(name, "")
        assert description and description.strip(), (
            f"field '{name}' has no description in _FIELD_DESCRIPTIONS"
        )


def _control_describe_emits_parseable_json() -> None:
    blob = describe()
    encoded = json.dumps(blob, indent=2, sort_keys=True)
    decoded = json.loads(encoded)
    assert decoded == blob, "describe() output did not round-trip through JSON"


def _live_describe(script_relpath: str) -> dict:
    """Shell out to a script's own `--describe` leg and parse its stdout.

    Not a Python import: D-21-A forbids this module from importing another
    gate script's code (it would let this module execute another gate's
    checking logic, which its own docstring disclaims). Subprocess-invoking
    `--describe` only reads that script's stdout, the same "copied grammar,
    not a code dependency" boundary `_BATTERY_GATE_RE` already documents for
    the D-01 floor.
    """
    proc = subprocess.run(
        [sys.executable, str(REPO_ROOT / script_relpath), "--describe"],
        capture_output=True,
        text=True,
        timeout=60,
    )
    if proc.returncode != 0:
        raise RuntimeError(
            f"{script_relpath} --describe exited {proc.returncode}: {proc.stderr}"
        )
    return json.loads(proc.stdout)


def _control_d04_live_field_equality() -> None:
    """Live D-04 floor: for every script ENTRIES declares a non-empty
    `consumes` against, shell out to its real `--describe` leg and assert
    `field_resolution_problems()` (plus `vocabulary_problems()`) report
    nothing in either direction.

    The script set is DERIVED from ENTRIES itself (`{e.script for e in
    ENTRIES if e.consumes}`), never a hand-typed list — so this control
    automatically covers every batch plan (21-03/04/05) lands, with no
    further self-test edits required as later batches add their own
    `consumes` tuples.
    """
    scripts = sorted({e.script for e in ENTRIES if e.consumes and e.script})
    requested = _requested_fields_by_script()
    emitted: dict[str, frozenset[str]] = {}
    for script in scripts:
        blob = _live_describe(script)
        emitted[script] = frozenset(blob.keys())
    problems = field_resolution_problems(requested, emitted)
    problems += vocabulary_problems(emitted)
    assert problems == [], problems


_CONTROLS: tuple[tuple[str, object], ...] = (
    ("d01-id-missing-from-registry", _control_d01_id_missing_from_registry),
    ("d01-id-extra-in-registry", _control_d01_id_extra_in_registry),
    ("d01-id-equal-passes", _control_d01_id_equal_passes),
    ("d01-gate-prereq-recognised", _control_d01_gate_prereq_recognised),
    ("d01-precommit-excluded", _control_d01_precommit_excluded),
    ("d01-live-battery-equality", _control_d01_live_battery_equality),
    ("cr04-hook-roster-live-positive", _control_cr04_hook_roster_live_positive),
    ("cr04-hook-roster-missing-fires", _control_cr04_hook_roster_missing_fires),
    ("cr04-hook-roster-extra-fires", _control_cr04_hook_roster_extra_fires),
    ("cr04-hook-roster-divergence-fires", _control_cr04_hook_roster_divergence_fires),
    ("cr04-hook-roster-arm-shape-guard", _control_cr04_hook_roster_arm_shape_guard),
    (
        "entries-count-matches-architecture-table",
        _control_entries_count_matches_architecture_table,
    ),
    ("no-gate-id-duplicated", _control_no_gate_id_duplicated),
    ("d04-missing-field-fires", _control_d04_missing_field_fires),
    ("d04-unconsumed-field-fires", _control_d04_unconsumed_field_fires),
    ("d04-both-directions-in-one-run", _control_d04_both_directions_in_one_run),
    ("d04-equal-passes", _control_d04_equal_passes),
    ("d04-vocabulary-violation-fires", _control_d04_vocabulary_violation_fires),
    ("vocabulary-members-documented", _control_vocabulary_members_documented),
    ("describe-emits-parseable-json", _control_describe_emits_parseable_json),
    ("d04-live-field-equality", _control_d04_live_field_equality),
)

# Second, independently-typed transcription of every control id above (the
# SCAN-GUARD/CONF-GATE coverage-floor shape) — a control added to _CONTROLS
# but missing here, or vice versa, fails self_test() by name rather than
# silently narrowing coverage. Per D-21-K this discipline applies to
# self-test control-id coverage only; it does NOT extend to a second
# transcription of the battery gate-id set itself, which stays derived.
_CONTROL_IDS: tuple[str, ...] = (
    "d01-id-missing-from-registry",
    "d01-id-extra-in-registry",
    "d01-id-equal-passes",
    "d01-gate-prereq-recognised",
    "d01-precommit-excluded",
    "d01-live-battery-equality",
    "cr04-hook-roster-live-positive",
    "cr04-hook-roster-missing-fires",
    "cr04-hook-roster-extra-fires",
    "cr04-hook-roster-divergence-fires",
    "cr04-hook-roster-arm-shape-guard",
    "entries-count-matches-architecture-table",
    "no-gate-id-duplicated",
    "d04-missing-field-fires",
    "d04-unconsumed-field-fires",
    "d04-both-directions-in-one-run",
    "d04-equal-passes",
    "d04-vocabulary-violation-fires",
    "vocabulary-members-documented",
    "describe-emits-parseable-json",
    "d04-live-field-equality",
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
            sys.stderr.write(f"_gate_registry: SELF-TEST FAIL [{control_id}] — {message}\n")
        return 1
    print(f"_gate_registry: SELF-TEST PASS — {len(executed)} controls run")
    return 0


# ---------------------------------------------------------------------------
# --describe: the registry's own self-description, uniform with everything
# it registers (D-08's own uniformity demand applied reflexively).
# ---------------------------------------------------------------------------


def describe() -> dict:
    return {
        "entry_count": len(ENTRIES),
        "documented_entry_count": len(
            [e for e in ENTRIES if e.key not in _ANTICIPATORY_KEYS]
        ),
        "anticipatory_keys": sorted(_ANTICIPATORY_KEYS),
        "gate_ids": sorted(_registry_entry_ids()),
        "precommit_keys": sorted(_registry_precommit_ids()),
        "control_ids": sorted(_CONTROL_IDS),
        "control_count": len(_CONTROL_IDS),
        "describe_field_vocabulary": sorted(DESCRIBE_FIELD_VOCABULARY),
    }


def main(argv: list[str] | None = None) -> int:
    """Run the registry CLI and return a process exit code.

    `argv` defaults to None so a self-test control can drive `main()` itself
    end-to-end against a fixture argv, proving the `--self-test`/`--describe`
    dispatch is actually wired (mirrors `sync-content.py`'s precedent,
    Phase 152 WR-01).
    """
    p = argparse.ArgumentParser(
        prog="_gate_registry.py",
        description="Gate registry: one entry per documented gate row (D-01).",
    )
    g = p.add_mutually_exclusive_group(required=True)
    g.add_argument("--self-test", action="store_true", help="Run the offline control battery.")
    g.add_argument(
        "--describe",
        action="store_true",
        help="Emit this registry's own self-description as a flat JSON blob on stdout.",
    )
    args = p.parse_args(argv)
    if args.self_test:
        return self_test()
    print(json.dumps(describe(), indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main())
