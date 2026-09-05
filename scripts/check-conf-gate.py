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

Exit codes:
    0  live leg clean
    1  a target was exceeded, a floor was breached, the D-07 roster drifted, the D-03 rule
       fired, the ratchet rose, or a discovery floor failed
    2  environment error (module import failure)
"""

from __future__ import annotations

import importlib.util
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

# The corpus-wide marked_untraced_claims sum over shared-examples, measured
# by plan 18-06 and unchanged since: both instances live in
# decompose-irreducibility.md. Pinned as a RATCHET — the live reading may
# fall, never rise. A rising marked count means claims are being marked
# instead of cited, which is the drift this ratchet exists to catch. Task 3
# reconciles this literal against the derived reading published in
# docs/conformance-baseline.md.
_MARKED_RATCHET: int = 2

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


# ---------------------------------------------------------------------------
# Pure comparators. Each takes a list of row-shaped dicts (real, from
# build_rows(REPO_ROOT), or synthetic, from _rc._synthetic_row) and returns a
# list of named problem strings. Never called with anything but real rows at
# the live call site; task 2's --self-test drives every one of these with
# synthetic rows so the comparison logic itself is proven correct
# independently of whether the real corpus happens to be clean today.
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
    """The marked-claim ratchet: the shared-examples sum of
    `marked_untraced_claims` may fall, never rise, above `_MARKED_RATCHET`.
    """
    marked_sum = sum(
        r["marked_untraced_claims"]
        for r in rows
        if r["surface"] == "shared-examples" and r["section_resolution"] == "OK"
    )
    if marked_sum > _MARKED_RATCHET:
        return [f"MARKED-CLAIM RATCHET VIOLATION: {marked_sum} > pinned {_MARKED_RATCHET}"]
    return []


# ---------------------------------------------------------------------------
# Live leg. Task 2 adds the D-08 live anti-vacuity arm between the target/
# floor/rule checks above and the final COVERAGE/PASS report below.
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

    gated_count = sum(1 for r in rows if r["surface"] in _GATED_SURFACES)
    print(
        f"check-conf-gate: COVERAGE — measured {gated_count} artifacts across "
        f"{', '.join(_GATED_SURFACES)}"
    )
    print("check-conf-gate: PASS")
    return 0


def main(argv: list[str] | None = None) -> int:
    return run_live()


if __name__ == "__main__":
    sys.exit(main())
