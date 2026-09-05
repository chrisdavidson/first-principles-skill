#!/usr/bin/env python3
# /// script
# requires-python = ">=3.12"
# dependencies = []
# ///
"""CONF-GATE: the standing conformance gate over the fourteen shipped worked examples.

Plans 18-01 through 18-06 drove four counts (unreadable, `heading_malformed_blocks`,
`nonconforming_verdict_cells`, `silent_untraced_claims`) to zero across the corpus. This
gate makes the zeros stick: it measures the shipped tree LIVE, through the frozen,
CONTRACT-06-pinned detectors in `scripts/check-quality-harness.py`, and compares those live
readings against targets written as literals in ITS OWN SOURCE — never against
`docs/data/conformance.json`. That artifact is regenerated from the same tree this gate
measures, so a gate reading both its targets and its readings from it would regenerate the
target alongside any regression and could never fire. That is the 999.30/999.31 defect
class this milestone exists to stop repeating.

Import discipline (D-06): this file imports `scripts/report-conformance.py` exactly once,
under the `sys.modules` key `_report_conformance`, and reads every detector function off
that already-imported module (`_rc.detect_defects`, `_rc.build_rows`,
`_rc.discover_artifacts`, `_rc._synthetic_row`, ...). It never re-registers the harness
under `_quality_harness` — `report-conformance.py` already performs that one-way import at
its own module scope, and re-running `exec_module` against the same `sys.modules` key would
re-execute the harness module body inside a process that already has it loaded.

Accepted cost, stated rather than hidden: `report-conformance.py` is the ONE aggregation
this gate and the published baseline both depend on. A bug in `build_rows` or
`detect_defects` makes the baseline and this gate wrong together, and neither can catch the
other. The alternative — an independent re-implementation of the same discovery and
measurement logic — was considered and declined in favour of a thin gate: two
implementations of the same aggregation is twice the surface for the two to silently
diverge, which is a worse failure mode than a shared bug.

`scripts/check-quality-harness.py` is FROZEN (CONTRACT-06). This gate calls its detectors
through `report-conformance.py`; it never modifies them and never re-implements them.

Usage:
    python3 scripts/check-conf-gate.py               # live leg against the shipped tree
    python3 scripts/check-conf-gate.py --self-test    # offline control battery

Exit codes:
    0  live leg clean / --self-test clean
    1  a target was exceeded, a claim floor or population floor was breached, the D-07 roster
       drifted, the D-03 rule fired, the ratchet rose, a D-08 mutation did not produce its
       expected defect, or a discovery floor failed
    2  environment error (module import failure)

`--self-test` additionally floors the seven enforcement symbols named by `_LIVE_CALL_SITES` /
`_LIVE_CALL_FORMS` by a set-equality lock (`_LIVE_CALL_SITES_LOCK`, BL-02) over both tables,
and each is counted and form-matched in `run_live()`'s comment-stripped source (CR-01, BL-01)
via `_strip_line_comments(inspect.getsource(run_live))`: this counts and matches SOURCE TEXT
only, so it catches a call site that was deleted, rewritten, or commented out — never one
whose returned problems are computed correctly and then silently discarded before reaching
the failure report.
"""

from __future__ import annotations

import argparse
import importlib.util
import inspect
import sys
from pathlib import Path

REPO_ROOT: Path = Path(__file__).resolve().parents[1]

# ---------------------------------------------------------------------------
# Import (D-06): scripts/report-conformance.py, exactly once, under its own
# sys.modules key. That module performs the one-way harness import under
# "_quality_harness" at ITS OWN module scope — by the time this module's body
# runs, that key is already populated. Every detector function this gate uses
# is read off the already-imported `_rc` module below; `_quality_harness` is
# never named as a sys.modules key anywhere in this file.
# ---------------------------------------------------------------------------

_RC_PATH: Path = REPO_ROOT / "scripts" / "report-conformance.py"
_rc_spec = importlib.util.spec_from_file_location("_report_conformance", _RC_PATH)
if _rc_spec is None or _rc_spec.loader is None:
    sys.stderr.write(f"check-conf-gate: ENV FAIL — could not build a module spec for {_RC_PATH}\n")
    sys.exit(2)
_rc = importlib.util.module_from_spec(_rc_spec)
sys.modules["_report_conformance"] = _rc  # assignment must precede exec_module (3.13/3.14 dataclasses._is_type)
_rc_spec.loader.exec_module(_rc)

detect_defects = _rc.detect_defects
build_rows = _rc.build_rows
discover_artifacts = _rc.discover_artifacts
DiscoveryFloorError = _rc.DiscoveryFloorError
CAVEAT_MARKER = _rc.CAVEAT_MARKER

# ---------------------------------------------------------------------------
# DEC-D: gated surfaces. contract-surface (shared/spine/references/
# output-template.md) is measured by report-conformance.py but never gated
# here — it is the specification document whose §4 worked examples
# deliberately include non-conforming forms as labelled teaching contrasts.
# Gating it would require either mislabelling a deliberately-broken example
# or restructuring the document's own pedagogy. This is a named constant
# carrying its own written reason, not a filter that happens to exclude it —
# a disclosed decision, never a silent omission.
# ---------------------------------------------------------------------------

_GATED_SURFACES: tuple[str, ...] = ("shared-examples", "generated-twin")

# D-05: targets are source literals, never read back from a regenerated
# artifact. Readings are re-derived live from `build_rows(REPO_ROOT)` every
# run. Moving a target is a reviewable source diff, the same discipline the
# sha256 pins and `_RENDER_RULE_LITERALS` already apply.
_TARGETS: dict[str, int] = {
    "unreadable": 0,
    "heading_malformed_blocks": 0,
    "nonconforming_verdict_cells": 0,
    "silent_untraced_claims": 0,
}

# D-04: one entry per shipped shared-examples analysis, transcribed from this
# phase's own summaries (18-02 through 18-06), each independently confirmed
# live against docs/data/conformance.json before being pinned here. No entry
# is below its 2026-09-04 baseline reading — plans 18-01 through 18-06 cut
# zero claims across the corpus — so no entry below carries a CUT-marker
# inline comment naming a removed claim and the plan that removed it (the
# convention any future reduction below baseline must follow).
# Floored by EQUALITY against the live-discovered shared-examples ids (D-07),
# never by subset: a dropped entry or an added-but-unfloored example both
# fail by name.
_CLAIM_FLOORS: dict[str, int] = {
    "composed-inversion-second-order": 2,
    "decompose-irreducibility": 7,
    "estimate-fermi": 5,
    "ishikawa-fishbone": 4,
    "personal-general": 7,
    "personal-general-2": 7,
    "product-business": 3,
    "product-business-2": 4,
    "science-engineering": 3,
    "science-engineering-2": 3,
    "self-application": 9,
    "software-systems": 8,
    "software-systems-2": 10,
    "theoretical-limit-carnot": 5,
}

# CR-02(a) (18-VERIFICATION.md blocking gap): a SECOND, independently
# transcribed copy of _CLAIM_FLOORS' fourteen entries — deliberately NOT
# derived from _CLAIM_FLOORS in any way. Before this lock, every fixture
# consuming _CLAIM_FLOORS built its expected value FROM the constant under
# test (e.g. `conclusion_claims=_CLAIM_FLOORS["personal-general"] - 1`),
# which is invariant to the constant's own value — CONTRACT-06's ENTRY-
# SOURCE LOCK names this shape explicitly as "a required side rebound to
# its own actual side". Setting every _CLAIM_FLOORS value to 0 (CR-02(a)'s
# measured defect) left both self-test and the live leg green. Moving a
# floor is therefore a two-place reviewable edit by design, the same
# discipline the sha256 pins already apply.
_CLAIM_FLOORS_LOCK: dict[str, int] = {
    "composed-inversion-second-order": 2,
    "decompose-irreducibility": 7,
    "estimate-fermi": 5,
    "ishikawa-fishbone": 4,
    "personal-general": 7,
    "personal-general-2": 7,
    "product-business": 3,
    "product-business-2": 4,
    "science-engineering": 3,
    "science-engineering-2": 3,
    "self-application": 9,
    "software-systems": 8,
    "software-systems-2": 10,
    "theoretical-limit-carnot": 5,
}

# BL-03 (18-VERIFICATION.md blocking gap): two of _TARGETS' four zero counts
# — nonconforming_verdict_cells and heading_malformed_blocks — are
# NUMERATOR-only. Neither had a denominator floor, so zero-by-conformance and
# zero-by-deletion were indistinguishable: deleting all six §2 Assumptions-
# Table data rows from shared/examples/software-systems.md and its
# byte-identical generated twin left `--self-test` at 34 controls and the
# live leg at PASS, rc 0 (measured 2026-09-05). These are DENOMINATOR
# floors, not targets — a zero numerator is meaningful only against a
# population that has not itself been deleted. Values are source literals
# under D-05, re-derived live from `docs/data/conformance.json`'s
# `headline.verdict_cells` / `headline.heading_swept_blocks` blocks at
# authoring time and never read back from that regenerated artifact. Each
# floor applies PER GATED SURFACE, not as a corpus-wide sum, matching
# _targets_problems' own per-surface shape.
#
# DISCLOSED BOUND: a floor detects population SHRINKAGE below the pinned
# figure, not substitution — deleting one artifact's rows while another
# grows by the same count would not fire it. Legitimate corpus growth never
# fires this floor; a legitimate reduction is a deliberate two-place edit —
# this constant and `population-floor-values-locked`'s inline literal both
# move together, the same discipline `_CLAIM_FLOORS_LOCK` already applies.
_POPULATION_FLOORS: dict[str, int] = {
    "verdict_cells": 77,
    "heading_chain_blocks": 31,
}

# The marked_untraced_claims sum over BOTH gated surfaces (_GATED_SURFACES):
# shared-examples 2 + generated-twin 2 = 4, measured by plan 18-06 and
# unchanged since — the two shared-examples instances live in
# decompose-irreducibility.md, and DUAL-04's byte-identity with the
# generated tree carries the same two instances onto generated-twin. This is
# exactly the figure docs/conformance-baseline.md's "Disclosed bounds" §2
# already publishes and names as pinned by this constant, so the code and
# the published sentence now state the same quantity over the same row set.
# Pinned as a RATCHET — the live reading may fall, never rise. A rising
# marked count means claims are being marked instead of cited, which is the
# drift this ratchet exists to catch. Closes 18-VERIFICATION.md minor gap 3
# / 18-REVIEW.md WR-02, which found this constant scoped to shared-examples
# only (2) while its own comment called that sum "corpus-wide" and the
# published baseline already stated 4.
#
# CR-02(b): the `ratchet-value-locked` control below asserts this value
# against an INLINE integer literal written at the control site, never read
# from this constant — setting _MARKED_RATCHET to 99 previously left both
# self-test and the live leg green. Plan 18-10 is the first exercise of that
# two-place discipline: it moves both this constant and that lock from 2 to
# 4 together, in the same commit.
_MARKED_RATCHET: int = 4

# The three prescribed section-6 lead-ins output-template.md names. A claim
# that opens with one of these AND carries the caveat marker is illegal
# (D-03): a prescribed lead-in commits the analysis to a specific, checkable
# claim, and the marker is reserved for a genuinely-uncitable flagged
# assumption, not a substitute for doing the citation work a prescribed
# lead-in already promises.
_PRESCRIBED_LEAD_INS: tuple[str, ...] = (
    "**Recommended approach:**",
    "**Key insight:**",
    "**Trade-offs acknowledged:**",
)

# CR-02(c) (18-VERIFICATION.md blocking gap): a SECOND, independently
# transcribed copy of _PRESCRIBED_LEAD_INS — narrowing the tuple to one
# literal previously left both self-test and the live leg green, because
# only "**Recommended approach:**" was ever exercised by a control. Control
# `d03-leadin-set-locked` asserts equality against this tuple, and the
# `d03-fires-on-leadin-<slug>` controls generated below (one per member of
# _PRESCRIBED_LEAD_INS) are additionally floored by the existing
# `coverage-floor` in self_test(), since narrowing the source tuple
# generates fewer entries while _CONTROL_IDS' hand-transcribed roster stays
# whole — the SCAN-GUARD plan-15-12 property, not a new mechanism.
_PRESCRIBED_LEAD_INS_LOCK: tuple[str, ...] = (
    "**Recommended approach:**",
    "**Key insight:**",
    "**Trade-offs acknowledged:**",
)

# One control-id slug per _PRESCRIBED_LEAD_INS member. The generated
# `d03-fires-on-leadin-<slug>` control ids are hand-transcribed into
# _CONTROL_IDS as plain literals below.
_D03_LEADIN_SLUGS: dict[str, str] = {
    "**Recommended approach:**": "recommended-approach",
    "**Key insight:**": "key-insight",
    "**Trade-offs acknowledged:**": "trade-offs-acknowledged",
}

# The one repaired example the D-08 live arm mutates in memory. personal-
# general.md is the tree's exemplar of conforming chain form — two chains,
# no drill-preamble scaffolding, straightforward verdict cells and citations
# — so a mutation site is easy to locate and reason about by inspection.
_D08_TARGET_SURFACE = "shared-examples"
_D08_TARGET_ID = "personal-general"

# The three literal mutation sites, transcribed from the live text of
# shared/examples/personal-general.md and each confirmed unique (str.count
# == 1) before being pinned here. A future edit to this file that removes
# one of these needles is exactly the "mutation site cannot be located"
# failure the D-08 arm is required to report rather than silently skip.
_D08_HOP_NEEDLE = "→ The effective annual compensation gain"
_D08_HOP_REPLACEMENT = "  The effective annual compensation gain"
_D08_CELL_NEEDLE = (
    "Discard — proxies the real question; GT-5 states the actual goal is not "
    "compensation maximization"
)
_D08_CELL_REPLACEMENT = "Discard"
_D08_CITE_NEEDLE = "3. (chain C1) Use the effective compensation figure"
_D08_CITE_REPLACEMENT = "3. Use the effective compensation figure"

# CR-01 (18-VERIFICATION.md blocking gap): `run_live()`'s seven `problems +=`
# enforcement call sites (widened from six by plan 18-12's BL-03 floor) are
# floored by a source-text census, in the same shape
# `check-selfaudit-scan.py`'s `(validate-census)` and `(roster-entry-source)`
# blocks already use for themselves. Every entry maps to expected count 1 —
# one call site, called exactly once.
_LIVE_CALL_SITES: dict[str, int] = {
    "_targets_problems": 1,
    "_claim_floor_roster_problems": 1,
    "_claim_floor_problems": 1,
    "_population_floor_problems": 1,
    "_d03_rule_problems_from_text": 1,
    "_ratchet_problems": 1,
    "_run_d08_arm": 1,
}

# The whitespace-normalized call-form fragment each symbol above must appear
# in, transcribed from run_live()'s current source. Five carry the
# `problems += <symbol>(...)` form; `_run_d08_arm` carries
# `mutation_lines = _run_d08_arm(rows)`. Every fragment is built BY
# CONCATENATION of short string pieces, never as one contiguous literal —
# the `(roster-entry-source)` convention `check-selfaudit-scan.py` uses for
# the same reason it exists there: a contiguous literal is a self-match
# hazard the moment anyone widens the census's search scope from run_live to
# the module (this table's own source text would then contain the exact
# string it is searching for).
_LIVE_CALL_FORMS: dict[str, str] = {
    "_targets_problems": "problems += " + "_targets_problems(rows)",
    "_claim_floor_roster_problems": (
        "problems += "
        + "_claim_floor_roster_problems(set(_CLAIM_FLOORS), discovered_ids)"
    ),
    "_claim_floor_problems": "problems += " + "_claim_floor_problems(rows)",
    "_population_floor_problems": "problems += " + "_population_floor_problems(rows)",
    "_d03_rule_problems_from_text": (
        "problems += "
        + '_d03_rule_problems_from_text(text, r["analysis_id"], r["relpath"])'
    ),
    "_ratchet_problems": "problems += " + "_ratchet_problems(rows)",
    "_run_d08_arm": "mutation_lines = " + "_run_d08_arm(rows)",
}

# BL-02 (18-VERIFICATION.md blocking gap): a SECOND, independently
# transcribed roster of the same seven enforcement symbol names (widened from
# six by plan 18-12's BL-03 floor) — deliberately NOT derived from
# _LIVE_CALL_SITES or _LIVE_CALL_FORMS by any expression, the same discipline
# _CLAIM_FLOORS_LOCK already applies to _CLAIM_FLOORS. Before this lock, four
# of the original six symbols (_run_d08_arm, _claim_floor_problems,
# _d03_rule_problems_from_text, _claim_floor_roster_problems) could be
# deleted from both census tables plus their call site in run_live(), and
# `--self-test` still reported `SELF-TEST PASS — 32 controls run` at rc 0.
# Adding or removing an enforcement call is therefore a two-place reviewable
# edit by design.
_LIVE_CALL_SITES_LOCK: tuple[str, ...] = (
    "_targets_problems",
    "_claim_floor_roster_problems",
    "_claim_floor_problems",
    "_population_floor_problems",
    "_d03_rule_problems_from_text",
    "_ratchet_problems",
    "_run_d08_arm",
)


def _strip_line_comments(source: str) -> str:
    """BL-01 (18-VERIFICATION.md): strip everything from the first `#` on each
    line before the census counts or the form lock matches, the same idiom
    `scripts/check-traceability.py` uses at its own comment-stripping site
    (`line.split("#", 1)[0]`, ~line 2152, backed by control `(h1)`,
    "comment stripping is load-bearing"). Without this, a `# ` prefix on an
    enforcement call line leaves the text present and unchanged in raw source,
    so `_call_site_census_problems` still counts it and the form lock still
    finds it — a commented-out call satisfies both checks.

    DISCLOSED BOUND, same conservative direction as the sibling site: this
    over-strips a `#` that appears inside a string literal, which can only
    make the census see LESS text, never more. It cannot manufacture a false
    PASS by hiding a real call site behind an in-string `#` — the worst case
    is an unrelated false positive from a call site that never existed.
    """
    return "\n".join(line.split("#", 1)[0] for line in source.splitlines())


def _call_site_census_problems(
    source: str,
    expected_counts: dict[str, int],
    expected_forms: dict[str, str] | None = None,
) -> list[str]:
    """CR-01: a PURE source-text census over `run_live()`'s enforcement call
    sites. Takes source text as a parameter — never `inspect.getsource
    (run_live)` directly — so the `census-x*`/`form-lock-x*` isolation arms
    below can drive it with synthetic strings and never with the real
    function's source. That discipline is what keeps the arms falsifiable
    when the real source changes.

    For each symbol in *expected_counts* this counts occurrences of
    ``symbol + "("`` in *source* and reports
    ``CALL-SITE CENSUS: <symbol> occurs <n> time(s) in run_live's source,
    expected <k>`` when the count differs. When *expected_forms* is supplied,
    *source* is additionally whitespace-normalized (every run of whitespace
    collapsed to a single space) and each symbol's expected call-form
    fragment is checked for containment, reporting
    ``CALL-FORM LOCK: <symbol>'s expected call form not found in run_live's
    source: <fragment>`` when absent. Problems are returned in the tables'
    own declaration order, so failure output is stable across runs.

    DISCLOSED LIMITATION, in the same voice as `check-selfaudit-scan.py`'s
    ENTRY-SOURCE LOCK: this counts and matches SOURCE TEXT and observes no
    behaviour. (i) It catches a call site that was DELETED, REWRITTEN, or
    COMMENTED OUT — closing BL-01 (18-VERIFICATION.md) via the
    `_strip_line_comments` call below and the `census-x4-commented` control.
    (ii) It still does NOT catch a call whose returned problems are computed
    correctly and then discarded before reaching the failure report — the
    same residual `check-quality-harness.py` control `(t)` and
    `check-selfaudit-scan.py`'s `validate-census` state for themselves.
    (iii) A call form rebound to an expression of EQUAL VALUE remains
    invisible to it by construction. Closes CR-01 and the blocking gap
    18-VERIFICATION.md records against `run_live()`'s six enforcement call
    sites.
    """
    source = _strip_line_comments(source)
    problems: list[str] = []
    for symbol, expected in expected_counts.items():
        pattern = symbol + "("
        actual = source.count(pattern)
        if actual != expected:
            problems.append(
                f"CALL-SITE CENSUS: {symbol} occurs {actual} time(s) in "
                f"run_live's source, expected {expected}"
            )
    if expected_forms is not None:
        normalized = " ".join(source.split())
        for symbol, fragment in expected_forms.items():
            normalized_fragment = " ".join(fragment.split())
            if normalized_fragment not in normalized:
                problems.append(
                    f"CALL-FORM LOCK: {symbol}'s expected call form not "
                    f"found in run_live's source: {fragment!r}"
                )
    return problems


# ---------------------------------------------------------------------------
# Pure comparators. Each takes a list of row-shaped dicts (real, from
# build_rows(REPO_ROOT), or synthetic, from _rc._synthetic_row) and returns a
# list of named problem strings. Never called with anything but real rows at
# the live call site; --self-test drives every one of these with synthetic
# rows so the comparison logic itself is proven correct independently of
# whether the real corpus happens to be clean today.
# ---------------------------------------------------------------------------


def _targets_problems(rows: list[dict]) -> list[str]:
    """CONF-06: fail if any of the four _TARGETS counts rises above its
    target on EITHER gated surface. `heading_malformed_blocks` is summed over
    every row regardless of readability (the heading census runs
    unconditionally, per report-conformance.py's build_row); the other three
    are summed only over rows that resolved ("OK"), since an unreadable row
    carries the literal "unreadable" for those fields, never a number.
    """
    problems: list[str] = []
    for surface in _GATED_SURFACES:
        surf_rows = [r for r in rows if r["surface"] == surface]
        readable = [r for r in surf_rows if r["section_resolution"] == "OK"]
        readings = {
            "unreadable": sum(
                1
                for r in surf_rows
                if str(r["section_resolution"]).startswith("SectionResolutionError:")
            ),
            "heading_malformed_blocks": sum(r["heading_malformed_blocks"] for r in surf_rows),
            "nonconforming_verdict_cells": sum(
                r["nonconforming_verdict_cells"] for r in readable
            ),
            "silent_untraced_claims": sum(r["silent_untraced_claims"] for r in readable),
        }
        for key, target in _TARGETS.items():
            actual = readings[key]
            if actual > target:
                problems.append(
                    f"TARGET EXCEEDED [{surface}] {key}: {actual} > target {target}"
                )
    return problems


def _claim_floor_roster_problems(floor_keys: set[str], discovered_ids: set[str]) -> list[str]:
    """D-07: EQUALITY, never subset, between _CLAIM_FLOORS' keys and the live-
    discovered shared-examples ids. Reports both `missing` (discovered but
    unfloored) and `extra` (floored but no longer discovered) by name.
    """
    missing = sorted(discovered_ids - floor_keys)
    extra = sorted(floor_keys - discovered_ids)
    if missing or extra:
        return [f"D-07 ROSTER DRIFT: missing={missing} extra={extra}"]
    return []


def _claim_floor_problems(rows: list[dict]) -> list[str]:
    """D-04: fail if any floored file's live `conclusion_claims` falls below
    its pinned floor. A row absent from `rows` is already reported by
    `_claim_floor_roster_problems` and is silently skipped here rather than
    double-reported.
    """
    problems: list[str] = []
    by_id = {r["analysis_id"]: r for r in rows if r["surface"] == "shared-examples"}
    for analysis_id, floor in _CLAIM_FLOORS.items():
        row = by_id.get(analysis_id)
        if row is None:
            continue
        actual = row.get("conclusion_claims")
        if isinstance(actual, int) and actual < floor:
            problems.append(
                f"D-04 CLAIM FLOOR BREACH [{analysis_id}]: conclusion_claims "
                f"{actual} < floor {floor}"
            )
    return problems


def _population_floor_problems(rows: list[dict]) -> list[str]:
    """BL-03: per-surface denominator floors over `verdict_cells` (summed
    over READABLE rows, mirroring `_targets_problems`' `nonconforming_
    verdict_cells` scope) and `heading_chain_blocks` (summed over EVERY row
    of the surface, mirroring `_targets_problems`' `heading_malformed_blocks`
    scope — the heading sweep runs unconditionally in `build_row`, so an
    unreadable artifact still contributes a real reading, and scoping it to
    readable rows would let an artifact become unreadable and drop out of
    the denominator undetected). Iterates `_GATED_SURFACES` then
    `_POPULATION_FLOORS` in declaration order so failure output is
    deterministic.
    """
    problems: list[str] = []
    for surface in _GATED_SURFACES:
        surf_rows = [r for r in rows if r["surface"] == surface]
        readable = [r for r in surf_rows if r["section_resolution"] == "OK"]
        readings = {
            "verdict_cells": sum(r["verdict_cells"] for r in readable),
            "heading_chain_blocks": sum(r["heading_chain_blocks"] for r in surf_rows),
        }
        for key, floor in _POPULATION_FLOORS.items():
            actual = readings[key]
            if actual < floor:
                problems.append(
                    f"POPULATION FLOOR BREACH [{surface}] {key}: {actual} < floor "
                    f"{floor} — a zero defect count against a shrunken population "
                    "is not conformance"
                )
    return problems


def _d03_rule_problems_from_text(text: str, analysis_id: str, relpath: str) -> list[str]:
    """D-03: a claim carrying CAVEAT_MARKER may not open with one of the three
    prescribed lead-ins. Calls the frozen `detect_defects` directly (never a
    second markdown parse) and reads the audit-only `_untraced_claims_text`
    field — a marked caveat always scores untraced (R-CLAIM-CAVEAT-MARKED),
    so every marked claim is guaranteed to appear there.
    """
    problems: list[str] = []
    record = detect_defects(text, analysis_id)
    for claim_text in record["_untraced_claims_text"]:
        if CAVEAT_MARKER in claim_text and claim_text.startswith(_PRESCRIBED_LEAD_INS):
            problems.append(
                f"D-03 RULE VIOLATION [{relpath}]: marked claim opens with a "
                f"prescribed lead-in: {claim_text[:80]!r}"
            )
    return problems


def _ratchet_problems(rows: list[dict]) -> list[str]:
    """The marked-claim ratchet: the sum of `marked_untraced_claims` over
    BOTH gated surfaces (_GATED_SURFACES) may fall, never rise, above
    `_MARKED_RATCHET` — matching `_targets_problems`' existing both-surfaces
    shape and docs/conformance-baseline.md's published corpus-wide figure.
    """
    marked_sum = sum(
        r["marked_untraced_claims"]
        for r in rows
        if r["surface"] in _GATED_SURFACES and r["section_resolution"] == "OK"
    )
    if marked_sum > _MARKED_RATCHET:
        return [f"MARKED-CLAIM RATCHET VIOLATION: {marked_sum} > pinned {_MARKED_RATCHET}"]
    return []


# ---------------------------------------------------------------------------
# D-08: the live anti-vacuity arm. Three in-memory mutations of a real
# repaired example the live leg has just measured, each required to produce
# its specific defect. Mutations are string-only; shared/ and
# first-principles/ are never written. This is the one thing a tempdir
# fixture structurally cannot prove: that the live leg is wired to the
# shipped artifacts, not to nothing.
# ---------------------------------------------------------------------------


def _run_d08_arm(rows: list[dict]) -> list[str]:
    target_row = next(
        (
            r
            for r in rows
            if r["surface"] == _D08_TARGET_SURFACE and r["analysis_id"] == _D08_TARGET_ID
        ),
        None,
    )
    if target_row is None:
        sys.stderr.write(
            f"check-conf-gate: COVERAGE FAIL — D-08 target {_D08_TARGET_ID!r} not found "
            f"on surface {_D08_TARGET_SURFACE!r}; the anti-vacuity arm cannot run\n"
        )
        sys.exit(1)

    relpath = target_row["relpath"]
    path = REPO_ROOT / relpath
    text = path.read_text(encoding="utf-8")
    baseline = detect_defects(text, target_row["analysis_id"])
    baseline_blocks = _rc._render_example_chain_blocks(text)
    baseline_malformed = sum(
        1 for _, b in baseline_blocks if not _rc._chain_block_well_formed(b)
    )
    baseline_marked = sum(1 for t in baseline["_untraced_claims_text"] if CAVEAT_MARKER in t)
    baseline_silent = baseline["untraced_claims"] - baseline_marked

    lines: list[str] = []

    # (a) re-wrap one hop across two physical lines: remove the leading arrow
    # from a continuation line and indent it instead, so the line no longer
    # starts with an arrow and is not absorbed as a chain continuation.
    if _D08_HOP_NEEDLE not in text or text.count(_D08_HOP_NEEDLE) != 1:
        sys.stderr.write(
            f"check-conf-gate: COVERAGE FAIL — D-08(a) mutation site not found "
            f"(or not unique) in {relpath}\n"
        )
        sys.exit(1)
    mutated_a = text.replace(_D08_HOP_NEEDLE, _D08_HOP_REPLACEMENT, 1)
    blocks_a = _rc._render_example_chain_blocks(mutated_a)
    malformed_a = sum(1 for _, b in blocks_a if not _rc._chain_block_well_formed(b))
    if malformed_a != baseline_malformed + 1:
        sys.stderr.write(
            f"check-conf-gate: COVERAGE FAIL — D-08(a) hop re-wrap mutation on {relpath} "
            f"did not increment heading_malformed_blocks by exactly 1 "
            f"(baseline {baseline_malformed}, mutated {malformed_a})\n"
        )
        sys.exit(1)
    lines.append(
        f"check-conf-gate: D-08(a) hop re-wrap on {relpath} — "
        f"heading_malformed_blocks {baseline_malformed} -> {malformed_a}"
    )

    # (b) strip the em dash and its justification from a repaired Verdict
    # cell, leaving the bare vocabulary token.
    if _D08_CELL_NEEDLE not in text or text.count(_D08_CELL_NEEDLE) != 1:
        sys.stderr.write(
            f"check-conf-gate: COVERAGE FAIL — D-08(b) mutation site not found "
            f"(or not unique) in {relpath}\n"
        )
        sys.exit(1)
    mutated_b = text.replace(_D08_CELL_NEEDLE, _D08_CELL_REPLACEMENT, 1)
    record_b = detect_defects(mutated_b, target_row["analysis_id"])
    if record_b["nonconforming_verdict_cells"] != baseline["nonconforming_verdict_cells"] + 1:
        sys.stderr.write(
            f"check-conf-gate: COVERAGE FAIL — D-08(b) verdict-cell strip on {relpath} "
            f"did not increment nonconforming_verdict_cells by exactly 1 "
            f"(baseline {baseline['nonconforming_verdict_cells']}, "
            f"mutated {record_b['nonconforming_verdict_cells']})\n"
        )
        sys.exit(1)
    lines.append(
        f"check-conf-gate: D-08(b) verdict-cell strip on {relpath} — "
        f"nonconforming_verdict_cells {baseline['nonconforming_verdict_cells']} -> "
        f"{record_b['nonconforming_verdict_cells']}"
    )

    # (c) remove one (chain Cn) citation from an otherwise-traced claim.
    if _D08_CITE_NEEDLE not in text or text.count(_D08_CITE_NEEDLE) != 1:
        sys.stderr.write(
            f"check-conf-gate: COVERAGE FAIL — D-08(c) mutation site not found "
            f"(or not unique) in {relpath}\n"
        )
        sys.exit(1)
    mutated_c = text.replace(_D08_CITE_NEEDLE, _D08_CITE_REPLACEMENT, 1)
    record_c = detect_defects(mutated_c, target_row["analysis_id"])
    marked_c = sum(1 for t in record_c["_untraced_claims_text"] if CAVEAT_MARKER in t)
    silent_c = record_c["untraced_claims"] - marked_c
    if silent_c != baseline_silent + 1:
        sys.stderr.write(
            f"check-conf-gate: COVERAGE FAIL — D-08(c) citation removal on {relpath} "
            f"did not increment silent_untraced_claims by exactly 1 "
            f"(baseline {baseline_silent}, mutated {silent_c})\n"
        )
        sys.exit(1)
    lines.append(
        f"check-conf-gate: D-08(c) citation removal on {relpath} — "
        f"silent_untraced_claims {baseline_silent} -> {silent_c}"
    )

    return lines


# ---------------------------------------------------------------------------
# Live leg
# ---------------------------------------------------------------------------


def run_live() -> int:
    try:
        rows = build_rows(REPO_ROOT)
    except DiscoveryFloorError as exc:
        for line in str(exc).splitlines():
            sys.stderr.write(line + "\n")
        return 1

    problems: list[str] = []
    problems += _targets_problems(rows)

    discovered_ids = {r["analysis_id"] for r in rows if r["surface"] == "shared-examples"}
    problems += _claim_floor_roster_problems(set(_CLAIM_FLOORS), discovered_ids)
    problems += _claim_floor_problems(rows)
    problems += _population_floor_problems(rows)

    for r in rows:
        if r["surface"] not in _GATED_SURFACES or r["section_resolution"] != "OK":
            continue
        text = (REPO_ROOT / r["relpath"]).read_text(encoding="utf-8")
        problems += _d03_rule_problems_from_text(text, r["analysis_id"], r["relpath"])

    problems += _ratchet_problems(rows)

    if problems:
        for p in problems:
            sys.stderr.write(f"check-conf-gate: FAIL — {p}\n")
        return 1

    mutation_lines = _run_d08_arm(rows)

    gated_count = sum(1 for r in rows if r["surface"] in _GATED_SURFACES)
    print(
        f"check-conf-gate: COVERAGE — measured {gated_count} artifacts across "
        f"{', '.join(_GATED_SURFACES)}"
    )
    for line in mutation_lines:
        print(line)
    print("check-conf-gate: PASS")
    return 0


# ---------------------------------------------------------------------------
# --self-test: offline control battery, entirely synthetic rows and
# in-memory documents. Never touches the real tree. Roster floored by
# EQUALITY against a second, independently transcribed lock (the
# SCAN-GUARD/_BRANCH_ROSTER_LOCK shape) so a control added to one and not the
# other fails self_test() by name. No control here is given a control of its
# own — the depth rule stops at one level.
# ---------------------------------------------------------------------------

_D03_FIRE_TEXT = (
    "## 1. Problem Essence\nSome essence text that is long enough.\n\n"
    "## 2. Assumptions Table\n| Assumption | Confidence |\n|---|---|\n\n"
    "## 3. Ground Truths\n- GT-1: some ground truth here.\n\n"
    "## 4. Derivation Chains\nGT-1 -> some conclusion, with no numbered chain heading.\n\n"
    "## 5. Abandoned Reasoning\nNone.\n\n"
    "## 6. Conclusion\n**Recommended approach:** " + CAVEAT_MARKER + ", this claim is long "
    "enough to clear the assertiveness floor on its own merits.\n"
)

_D03_PASS_TEXT = (
    "## 1. Problem Essence\nSome essence text that is long enough.\n\n"
    "## 2. Assumptions Table\n| Assumption | Confidence |\n|---|---|\n\n"
    "## 3. Ground Truths\n- GT-1: some ground truth here.\n\n"
    "## 4. Derivation Chains\nGT-1 -> some conclusion, with no numbered chain heading.\n\n"
    "## 5. Abandoned Reasoning\nNone.\n\n"
    "## 6. Conclusion\n**Non-prescribed label:** " + CAVEAT_MARKER + ", this claim is long "
    "enough to clear the assertiveness floor on its own merits.\n"
)

# CR-02(d): a claim that DOES open with a prescribed lead-in and does NOT
# carry the caveat marker — derived from _D03_FIRE_TEXT by removing the
# marker, never hand-duplicated, so the two fixtures cannot silently drift
# apart. Dropping the `CAVEAT_MARKER in claim_text` conjunct from
# _d03_rule_problems_from_text previously left this shape entirely
# unguarded: with no marker, the predicate's remaining half ("any untraced
# claim with a prescribed lead-in is a violation") would flag every such
# example, and no control noticed.
_D03_UNMARKED_TEXT = _D03_FIRE_TEXT.replace(CAVEAT_MARKER + ", ", "", 1)


def _control_target_unreadable_fires() -> None:
    bad = _rc._synthetic_row(
        "shared-examples", "u.md", "u", section_resolution="SectionResolutionError: boom"
    )
    problems = _targets_problems([bad])
    assert any("unreadable" in p for p in problems), problems


def _control_target_unreadable_passes_at_zero() -> None:
    good = _rc._synthetic_row("shared-examples", "g.md", "g")
    assert _targets_problems([good]) == []


def _control_target_heading_malformed_fires() -> None:
    bad = _rc._synthetic_row("shared-examples", "h.md", "h", heading_malformed_blocks=1)
    problems = _targets_problems([bad])
    assert any("heading_malformed_blocks" in p for p in problems), problems


def _control_target_nonconforming_verdict_fires() -> None:
    bad = _rc._synthetic_row("shared-examples", "n.md", "n", nonconforming_verdict_cells=1)
    problems = _targets_problems([bad])
    assert any("nonconforming_verdict_cells" in p for p in problems), problems


def _control_target_silent_untraced_fires() -> None:
    bad = _rc._synthetic_row("shared-examples", "sl.md", "sl", silent_untraced_claims=1)
    problems = _targets_problems([bad])
    assert any("silent_untraced_claims" in p for p in problems), problems


def _control_targets_pass_on_generated_twin_too() -> None:
    good_shared = _rc._synthetic_row("shared-examples", "g.md", "g")
    good_twin = _rc._synthetic_row("generated-twin", "g.md", "g")
    assert _targets_problems([good_shared, good_twin]) == []


def _control_target_fires_on_generated_twin() -> None:
    bad_twin = _rc._synthetic_row("generated-twin", "t.md", "t", nonconforming_verdict_cells=1)
    problems = _targets_problems([bad_twin])
    assert any("[generated-twin]" in p for p in problems), problems


def _control_d07_missing_named() -> None:
    problems = _claim_floor_roster_problems({"a", "b"}, {"a", "b", "c"})
    assert problems, problems
    assert "missing=['c']" in problems[0], problems


def _control_d07_extra_named() -> None:
    problems = _claim_floor_roster_problems({"a", "b", "c"}, {"a", "b"})
    assert problems, problems
    assert "extra=['c']" in problems[0], problems


def _control_d07_equal_passes() -> None:
    assert _claim_floor_roster_problems({"a", "b"}, {"a", "b"}) == []


def _control_d04_floor_fires() -> None:
    # CR-02(a): INLINE by design (6 is one below personal-general's pinned
    # floor of 7) — never `_CLAIM_FLOORS["personal-general"] - 1`, which is
    # invariant to the floor's own value and cannot fail when the floor is
    # loosened. See _CLAIM_FLOORS_LOCK's comment.
    row = _rc._synthetic_row(
        "shared-examples", "personal-general.md", "personal-general", conclusion_claims=6
    )
    problems = _claim_floor_problems([row])
    assert any("personal-general" in p for p in problems), problems


def _control_d04_floor_passes_at_floor() -> None:
    # CR-02(a): INLINE by design (7 is exactly personal-general's pinned
    # floor) — see _control_d04_floor_fires' comment.
    row = _rc._synthetic_row(
        "shared-examples", "personal-general.md", "personal-general", conclusion_claims=7
    )
    assert _claim_floor_problems([row]) == []


# CR-02(c)/(d) (18-VERIFICATION.md blocking gap): the D-03 predicate's
# coverage was narrowed on two independent axes. (c) Only one of the three
# _PRESCRIBED_LEAD_INS literals was ever exercised by a control, so
# narrowing the tuple to that one literal left both self-test and the live
# leg green; `d03-leadin-set-locked` plus the per-literal
# `d03-fires-on-leadin-<slug>` controls below close it — the ids are
# GENERATED from _PRESCRIBED_LEAD_INS and hand-transcribed as plain
# literals into _CONTROL_IDS, so narrowing the tuple fails the existing
# `coverage-floor` by naming the missing ids. (d) The
# `CAVEAT_MARKER in claim_text` conjunct at the D-03 predicate had no
# negative control; `d03-passes-on-unmarked-prescribed-leadin` closes it.


def _control_d03_passes_on_nonprescribed_leadin() -> None:
    problems = _d03_rule_problems_from_text(_D03_PASS_TEXT, "pass", "synthetic/pass.md")
    assert problems == [], problems


def _make_d03_fires_on_leadin_control(lead_in: str):
    """Build a control closure for one _PRESCRIBED_LEAD_INS member, used
    only to GENERATE the `d03-fires-on-leadin-<slug>` entries below —
    never called with anything but a member of _PRESCRIBED_LEAD_INS.
    """

    def _control() -> None:
        fixture = _D03_FIRE_TEXT.replace("**Recommended approach:**", lead_in, 1)
        problems = _d03_rule_problems_from_text(fixture, "fire", "synthetic/fire.md")
        assert problems, (lead_in, problems)
        assert any("D-03 RULE VIOLATION" in p for p in problems), (lead_in, problems)

    return _control


# GENERATED: one control entry per member of _PRESCRIBED_LEAD_INS. The
# retired `d03-fires-on-prescribed-leadin` control is this table's
# "**Recommended approach:**" entry — its exact superset.
_D03_LEADIN_FIRES_CONTROLS: tuple[tuple[str, object], ...] = tuple(
    (
        f"d03-fires-on-leadin-{_D03_LEADIN_SLUGS[lead_in]}",
        _make_d03_fires_on_leadin_control(lead_in),
    )
    for lead_in in _PRESCRIBED_LEAD_INS
)


def _control_d03_leadin_set_locked() -> None:
    """CR-02(c): _PRESCRIBED_LEAD_INS and its second, independent
    transcription _PRESCRIBED_LEAD_INS_LOCK must agree, reporting the
    symmetric difference by literal on failure.
    """
    diff = set(_PRESCRIBED_LEAD_INS) ^ set(_PRESCRIBED_LEAD_INS_LOCK)
    assert not diff, f"D-03 LEAD-IN LOCK MISMATCH: {sorted(diff)}"


def _control_d03_passes_on_unmarked_prescribed_leadin() -> None:
    """CR-02(d): a claim opening with a prescribed lead-in and NOT carrying
    the caveat marker must pass — the `CAVEAT_MARKER in claim_text` half of
    the D-03 conjunct is what exempts it. Carries its own inline
    NON-VACUITY assertion before the main assertion (18-REVIEW.md's own
    vacuity probe on the sibling control): a fixture that silently stopped
    yielding any claim would pass this control for the wrong reason.
    """
    record = detect_defects(_D03_UNMARKED_TEXT, "u")
    assert record["untraced_claims"] >= 1, record
    assert any(
        t.startswith("**Recommended approach:**") for t in record["_untraced_claims_text"]
    ), record["_untraced_claims_text"]
    assert (
        _d03_rule_problems_from_text(_D03_UNMARKED_TEXT, "u", "synthetic/u.md") == []
    )


def _control_ratchet_fires_above() -> None:
    # 18-10: INLINE by design (5 is one above the pinned ratchet of 4) —
    # never `_MARKED_RATCHET + 1`, which is invariant to the ratchet's own
    # value and cannot fail when the ratchet is loosened.
    row = _rc._synthetic_row("shared-examples", "r.md", "r", marked_untraced_claims=5)
    assert _ratchet_problems([row]) != []


def _control_ratchet_passes_at_pin() -> None:
    # 18-10: INLINE by design (4 is exactly the pinned ratchet) — see
    # _control_ratchet_fires_above's comment.
    row = _rc._synthetic_row("shared-examples", "r2.md", "r2", marked_untraced_claims=4)
    assert _ratchet_problems([row]) == []


def _control_ratchet_passes_below() -> None:
    # 18-10: INLINE by design (3 is one below the pinned ratchet) — see
    # _control_ratchet_fires_above's comment.
    row = _rc._synthetic_row("shared-examples", "r3.md", "r3", marked_untraced_claims=3)
    assert _ratchet_problems([row]) == []


def _control_ratchet_fires_across_both_surfaces() -> None:
    """18-10 (WR-02): DISCRIMINATING between the old shared-examples-only
    filter and the widened _GATED_SURFACES filter. shared-examples carries
    marked_untraced_claims=2 and generated-twin alone carries 3: under the
    OLD filter the sum would be 2 (<= the pinned ratchet of 4, no fire);
    under the WIDENED filter the sum is 5 (> pinned 4, fires). A control
    that would pass under both the old and the new filter would be
    decorative — this one only passes under the new one, so narrowing
    `_ratchet_problems` back to shared-examples-only fails this control by
    name.
    """
    shared_row = _rc._synthetic_row("shared-examples", "s.md", "s", marked_untraced_claims=2)
    twin_row = _rc._synthetic_row("generated-twin", "t.md", "t", marked_untraced_claims=3)
    problems = _ratchet_problems([shared_row, twin_row])
    assert problems != [], problems
    assert "5" in problems[0] and "4" in problems[0], problems


def _control_claim_floor_values_locked() -> None:
    """CR-02(a): _CLAIM_FLOORS and its second, independent transcription
    _CLAIM_FLOORS_LOCK must agree by name. Reports the sorted list of keys
    whose values differ, or which are present in only one table — never a
    bare count, so a narrowing shows up by name.
    """
    differing = sorted(
        k
        for k in set(_CLAIM_FLOORS) | set(_CLAIM_FLOORS_LOCK)
        if _CLAIM_FLOORS.get(k) != _CLAIM_FLOORS_LOCK.get(k)
    )
    assert not differing, f"D-04 LOCK MISMATCH: {differing}"


def _control_ratchet_value_locked() -> None:
    """CR-02(b): _MARKED_RATCHET must equal an INLINE integer literal
    written at this control site, never read from the constant itself —
    the shape that makes loosening _MARKED_RATCHET a reviewable, falsifiable
    edit rather than an invisible one. Plan 18-10 is the first exercise of
    this two-place discipline: it moves the constant and this lock from 2
    to 4 together, in the same commit, per WR-02's widening.
    """
    assert _MARKED_RATCHET == 4, _MARKED_RATCHET


def _control_contract_surface_excluded() -> None:
    """DEC-D reachability: a wildly non-conforming contract-surface row must
    not fail any comparator — the exclusion is a deliberate, reachable
    decision, not an accident of a filter nobody exercised.
    """
    bad = _rc._synthetic_row(
        "contract-surface",
        "output-template.md",
        "output-template",
        heading_malformed_blocks=99,
        nonconforming_verdict_cells=99,
        silent_untraced_claims=99,
        marked_untraced_claims=99,
        conclusion_claims=0,
        section_resolution="SectionResolutionError: irrelevant",
    )
    assert bad["surface"] not in _GATED_SURFACES
    assert _targets_problems([bad]) == []
    assert _ratchet_problems([bad]) == []
    assert _claim_floor_problems([bad]) == []


# CR-01 census/form-lock controls (18-VERIFICATION.md blocking gap). Every
# `census-x*`/`form-lock-x*` isolation arm below drives `_call_site_census_
# problems` with one of these SYNTHETIC source strings — never with
# `inspect.getsource(run_live)` — so the arms stay falsifiable independently
# of whatever `run_live`'s real source happens to read today.

_CENSUS_X1_CLEAN_SOURCE = (
    "def run_live():\n"
    "    problems: list[str] = []\n"
    "    problems += _targets_problems(rows)\n"
    "    problems += _claim_floor_roster_problems(set(_CLAIM_FLOORS), discovered_ids)\n"
    "    problems += _claim_floor_problems(rows)\n"
    "    problems += _population_floor_problems(rows)\n"
    '    problems += _d03_rule_problems_from_text(text, r["analysis_id"], r["relpath"])\n'
    "    problems += _ratchet_problems(rows)\n"
    "    mutation_lines = _run_d08_arm(rows)\n"
)

_CENSUS_X2_MISSING_SOURCE = (
    "def run_live():\n"
    "    problems: list[str] = []\n"
    "    problems += _claim_floor_roster_problems(set(_CLAIM_FLOORS), discovered_ids)\n"
    "    problems += _claim_floor_problems(rows)\n"
    "    problems += _population_floor_problems(rows)\n"
    '    problems += _d03_rule_problems_from_text(text, r["analysis_id"], r["relpath"])\n'
    "    problems += _ratchet_problems(rows)\n"
    "    mutation_lines = _run_d08_arm(rows)\n"
)

_CENSUS_X3_DUPLICATED_SOURCE = (
    "def run_live():\n"
    "    problems: list[str] = []\n"
    "    problems += _targets_problems(rows)\n"
    "    problems += _claim_floor_roster_problems(set(_CLAIM_FLOORS), discovered_ids)\n"
    "    problems += _claim_floor_problems(rows)\n"
    "    problems += _population_floor_problems(rows)\n"
    '    problems += _d03_rule_problems_from_text(text, r["analysis_id"], r["relpath"])\n'
    "    problems += _ratchet_problems(rows)\n"
    "    problems += _ratchet_problems(rows)\n"
    "    mutation_lines = _run_d08_arm(rows)\n"
)

_FORM_LOCK_X2_REWRITTEN_SOURCE = (
    "def run_live():\n"
    "    problems: list[str] = []\n"
    "    _targets_problems(rows)\n"
    "    problems += _claim_floor_roster_problems(set(_CLAIM_FLOORS), discovered_ids)\n"
    "    problems += _claim_floor_problems(rows)\n"
    "    problems += _population_floor_problems(rows)\n"
    '    problems += _d03_rule_problems_from_text(text, r["analysis_id"], r["relpath"])\n'
    "    problems += _ratchet_problems(rows)\n"
    "    mutation_lines = _run_d08_arm(rows)\n"
)

# BL-01 (18-VERIFICATION.md): derived from _CENSUS_X1_CLEAN_SOURCE by
# commenting out a single enforcement call line — never hand-duplicated —
# so the two fixtures cannot drift apart (the _D03_UNMARKED_TEXT convention
# already in this file). Proves the census catches a COMMENTED-OUT call,
# not merely a deleted or rewritten one.
_CENSUS_X4_COMMENTED_SOURCE = _CENSUS_X1_CLEAN_SOURCE.replace(
    "    problems += _targets_problems(rows)\n",
    "    # problems += _targets_problems(rows)\n",
)


def _control_live_call_site_census() -> None:
    source = inspect.getsource(run_live)
    problems = _call_site_census_problems(source, _LIVE_CALL_SITES)
    assert problems == [], problems


def _control_live_call_form_lock() -> None:
    source = inspect.getsource(run_live)
    problems = _call_site_census_problems(source, _LIVE_CALL_SITES, _LIVE_CALL_FORMS)
    assert problems == [], problems


def _control_census_x1_clean() -> None:
    problems = _call_site_census_problems(_CENSUS_X1_CLEAN_SOURCE, _LIVE_CALL_SITES)
    assert problems == [], problems


def _control_census_x2_missing() -> None:
    problems = _call_site_census_problems(_CENSUS_X2_MISSING_SOURCE, _LIVE_CALL_SITES)
    assert len(problems) == 1, problems
    assert "_targets_problems" in problems[0], problems
    assert "occurs 0 time" in problems[0], problems


def _control_census_x3_duplicated() -> None:
    problems = _call_site_census_problems(_CENSUS_X3_DUPLICATED_SOURCE, _LIVE_CALL_SITES)
    assert len(problems) == 1, problems
    assert "_ratchet_problems" in problems[0], problems
    assert "occurs 2 time" in problems[0], problems


def _control_form_lock_x1_clean() -> None:
    problems = _call_site_census_problems(
        _CENSUS_X1_CLEAN_SOURCE, _LIVE_CALL_SITES, _LIVE_CALL_FORMS
    )
    assert problems == [], problems


def _control_form_lock_x2_rewritten() -> None:
    problems = _call_site_census_problems(
        _FORM_LOCK_X2_REWRITTEN_SOURCE, _LIVE_CALL_SITES, _LIVE_CALL_FORMS
    )
    assert len(problems) == 1, problems
    assert "CALL-FORM LOCK" in problems[0], problems
    assert "_targets_problems" in problems[0], problems


def _control_census_x4_commented() -> None:
    problems = _call_site_census_problems(_CENSUS_X4_COMMENTED_SOURCE, _LIVE_CALL_SITES)
    assert len(problems) == 1, problems
    assert "_targets_problems" in problems[0], problems
    assert "occurs 0 time" in problems[0], problems


def _control_live_call_site_roster_locked() -> None:
    """BL-02: `_LIVE_CALL_SITES` and `_LIVE_CALL_FORMS` must each agree, by
    set equality, with the independently transcribed `_LIVE_CALL_SITES_LOCK`
    — never with each other, since a coordinated deletion from both tables
    (BL-02's measured defect) would satisfy a cross-table comparison. Also
    asserts the tables' own "one call site, called exactly once" contract:
    every `_LIVE_CALL_SITES` value must equal 1.

    DISCLOSED BOUND, in the same voice as `check-selfaudit-scan.py`'s
    ENTRY-SOURCE LOCK: this floors the roster's MEMBERSHIP and per-symbol
    expected count, not the behaviour of the calls themselves. A coordinated
    three-place edit (both tables, the lock, and the call site) remains
    possible and is by design a reviewable source diff, exactly as a sha256
    pin move is.
    """
    counts_diff = set(_LIVE_CALL_SITES) ^ set(_LIVE_CALL_SITES_LOCK)
    assert not counts_diff, f"CALL-SITE ROSTER DRIFT: {sorted(counts_diff)}"

    forms_diff = set(_LIVE_CALL_FORMS) ^ set(_LIVE_CALL_SITES_LOCK)
    assert not forms_diff, f"CALL-SITE ROSTER DRIFT: {sorted(forms_diff)}"

    wrong_counts = sorted(k for k, v in _LIVE_CALL_SITES.items() if v != 1)
    assert not wrong_counts, f"CALL-SITE ROSTER DRIFT: expected-count != 1 for {wrong_counts}"


_CONTROLS: tuple[tuple[str, object], ...] = (
    ("target-unreadable-fires", _control_target_unreadable_fires),
    ("target-unreadable-passes-at-zero", _control_target_unreadable_passes_at_zero),
    ("target-heading-malformed-fires", _control_target_heading_malformed_fires),
    ("target-nonconforming-verdict-fires", _control_target_nonconforming_verdict_fires),
    ("target-silent-untraced-fires", _control_target_silent_untraced_fires),
    ("targets-pass-on-generated-twin-too", _control_targets_pass_on_generated_twin_too),
    ("target-fires-on-generated-twin", _control_target_fires_on_generated_twin),
    ("d07-missing-named", _control_d07_missing_named),
    ("d07-extra-named", _control_d07_extra_named),
    ("d07-equal-passes", _control_d07_equal_passes),
    ("d04-floor-fires", _control_d04_floor_fires),
    ("d04-floor-passes-at-floor", _control_d04_floor_passes_at_floor),
    ("claim-floor-values-locked", _control_claim_floor_values_locked),
    ("d03-leadin-set-locked", _control_d03_leadin_set_locked),
    *_D03_LEADIN_FIRES_CONTROLS,
    ("d03-passes-on-nonprescribed-leadin", _control_d03_passes_on_nonprescribed_leadin),
    (
        "d03-passes-on-unmarked-prescribed-leadin",
        _control_d03_passes_on_unmarked_prescribed_leadin,
    ),
    ("ratchet-fires-above", _control_ratchet_fires_above),
    ("ratchet-passes-at-pin", _control_ratchet_passes_at_pin),
    ("ratchet-passes-below", _control_ratchet_passes_below),
    ("ratchet-value-locked", _control_ratchet_value_locked),
    ("ratchet-fires-across-both-surfaces", _control_ratchet_fires_across_both_surfaces),
    ("contract-surface-excluded", _control_contract_surface_excluded),
    ("live-call-site-census", _control_live_call_site_census),
    ("live-call-form-lock", _control_live_call_form_lock),
    ("census-x1-clean", _control_census_x1_clean),
    ("census-x2-missing", _control_census_x2_missing),
    ("census-x3-duplicated", _control_census_x3_duplicated),
    ("form-lock-x1-clean", _control_form_lock_x1_clean),
    ("form-lock-x2-rewritten", _control_form_lock_x2_rewritten),
    ("census-x4-commented", _control_census_x4_commented),
    ("live-call-site-roster-locked", _control_live_call_site_roster_locked),
)

# Coverage floor (SCAN-GUARD's _BRANCH_ROSTER_LOCK shape): a second,
# independently-typed transcription of every control id this self-test must
# run. A control added to _CONTROLS but missing here, or vice versa, fails
# self_test() by name rather than silently narrowing coverage.
_CONTROL_IDS: tuple[str, ...] = (
    "target-unreadable-fires",
    "target-unreadable-passes-at-zero",
    "target-heading-malformed-fires",
    "target-nonconforming-verdict-fires",
    "target-silent-untraced-fires",
    "targets-pass-on-generated-twin-too",
    "target-fires-on-generated-twin",
    "d07-missing-named",
    "d07-extra-named",
    "d07-equal-passes",
    "d04-floor-fires",
    "d04-floor-passes-at-floor",
    "claim-floor-values-locked",
    "d03-leadin-set-locked",
    "d03-fires-on-leadin-recommended-approach",
    "d03-fires-on-leadin-key-insight",
    "d03-fires-on-leadin-trade-offs-acknowledged",
    "d03-passes-on-nonprescribed-leadin",
    "d03-passes-on-unmarked-prescribed-leadin",
    "ratchet-fires-above",
    "ratchet-passes-at-pin",
    "ratchet-passes-below",
    "ratchet-value-locked",
    "ratchet-fires-across-both-surfaces",
    "contract-surface-excluded",
    "live-call-site-census",
    "live-call-form-lock",
    "census-x1-clean",
    "census-x2-missing",
    "census-x3-duplicated",
    "form-lock-x1-clean",
    "form-lock-x2-rewritten",
    "census-x4-commented",
    "live-call-site-roster-locked",
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
            sys.stderr.write(f"check-conf-gate: SELF-TEST FAIL [{control_id}] — {message}\n")
        return 1

    print(f"check-conf-gate: SELF-TEST PASS — {len(executed)} controls run")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="CONF-GATE: live conformance gate over the fourteen shipped worked "
        "examples, against source-literal targets."
    )
    parser.add_argument(
        "--self-test",
        action="store_true",
        help="run the offline control battery (positive, negative, anti-masking)",
    )
    args = parser.parse_args(argv)

    if args.self_test:
        return self_test()
    return run_live()


if __name__ == "__main__":
    sys.exit(main())
