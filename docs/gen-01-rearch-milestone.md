# GEN-01-REARCH: Full Step 0 Classifier Rearchitecture

**Artifact type:** Committed future-milestone stub
**Date:** 2026-06-15
**Phase:** 88-gen-01-execution (Plan 01)
**Requirement:** GR-02 [CRITICAL]
**Status:** Committed / Scheduled

---

## Ordering Constraint

GEN-01-REARCH is the **designated next live-routing / Step-0 milestone** to run after v6.2 closes. This is a concrete ordering constraint, not a calendar date.

**Depends on:** v6.2 milestone closed (see `.planning/ROADMAP.md` milestone sequence).

GEN-01-REARCH must not begin until v6.2 completes its Canonical Surface Reconciliation
(Phase 90), because Phase 90 regenerates `docs/requirements-matrix.md` with the final
0-open-gap headline. GEN-01-REARCH's REARCH-06 completion will then update the GEN-01 row
from `scheduled` to `reproducible`, and that update should land on a stable matrix baseline.

---

## ADR Lineage

This milestone is activated by the Phase 87 decision recorded in
`docs/gen-01-decision.md`. That artifact chose path (c): convert GEN-01 from an open
gap into a committed scheduled future milestone (GEN-01-REARCH), rather than
rearchitecting-now (out of v6.2 scope), applying a bounded-fix (under-delivers for this
scope), or formally retiring (inappropriate — the work remains real and measured).

The decision artifact is the authoritative source for the rationale; this file records the
resulting committed scope and phase breakdown.

**Activating decision:** `docs/gen-01-decision.md` (Phase 87, Plan 01, GR-01).

---

## Milestone Scope

GEN-01-REARCH resolves the full Step 0 classifier rearchitecture gap that remains after
v6.2. The gap is defined by four live-routing rows in `tests/step0-baseline-v5.3.md` that
fail at the K-of-N threshold under the current `scripts/_battery_core.py` detector:

| Row | Expected MODE | Honest K/N (v5.3 baseline) | Residual |
|-----|---------------|----------------------------|----------|
| S-P01 | focused-pre-mortem | 1/5 | RR-79-01 |
| S-P02 | focused-inversion | 0/5 | RR-79-02 |
| S-P05 | focused-trade-off | 0/5 | RR-79-03 |
| S-N04 | full-composer | 2/5 | RR-80-01 |

These figures are honest carry-forwards from the v5.3 live re-baseline (Phase 80,
60 live `claude` invocations, `--repeat 5 --min-pass 3`). They are NOT chased to a
forced PASS in v6.2 because doing so without the structural classifier work would be a
score-mask under honesty-not-score discipline (D-01).

This milestone is **live-routing work** — it requires iterative live `claude` invocations,
evidence-backed marker broadening, and K-of-N validation. It is explicitly NOT a
documentation task. A full rearchitecture requires the scope and live-session budget of
its own milestone, which is why it is committed here rather than included in v6.2.

---

## Phase Breakdown

### Phase REARCH-01: Capture-Grounded Detector Rearchitecture + Offline Gates

**Goal:** The `_battery_core.py` classifier is rearchitectured based on new live captures.
Run new live `claude` sessions for the four failing rows (S-P01, S-P02, S-P05, S-N04),
apply the Phase 76 Diagnosis Gate pattern to classify each output as detector
false-negative vs. genuine routing gap, then broaden `_TECHNIQUE_CATEGORIES` markers
capture-backed (provenance comments per marker, per the D-08/D-09 evidence standard from
v5.2). All offline gates must be green before any live spend in REARCH-02.

**Requirements:** REARCH-01, REARCH-02, REARCH-03

**Depends on:** v6.2 milestone closed (see Ordering Constraint above).

---

### Phase REARCH-02: Live Re-Baseline

**Goal:** Run the single authoritative 60-invocation live harness
(`python3 scripts/check-step0-live.py --repeat 5 --min-pass 3`) against the rearchitectured
detector. Record an honest `tests/step0-baseline-vX.Y.md` with true K/N for every row —
never a forced or masked PASS. Each of RR-79-01, RR-79-02, RR-79-03, and RR-80-01 is
either closed (row reaches min-pass) or honestly carried forward with an updated residual ID
and the true observed K/N. Prior baselines (v5.0 through v5.3) are preserved byte-for-byte.

**Requirements:** REARCH-04, REARCH-05

**Depends on:** REARCH-01 (all offline gates green: STEP0-08, BATT-06/FU-21, DUAL-04).

---

### Phase REARCH-03: Sentinel + Surface Reconciliation

**Goal:** Lock the rearchitecture against silent regression and close the milestone. Update
the offline sentinels in `scripts/_battery_core.py#self_test_boundary()` (or equivalent)
to lock the resolved or honestly-carried-forward states of RR-79-01/02/03 and RR-80-01.
Update GEN-01's row in `scripts/check-traceability.py _rows_active_tail()` from `scheduled`
to `reproducible`, with a confirming artifact link pointing to the live re-baseline file.
Regenerate `docs/requirements-matrix.md` to reflect the updated tier. Prove all offline
gates green simultaneously: TRACE-03, BATT-06, STEP0-06, STEP0-08, DUAL-04.

**Requirements:** REARCH-06

**Depends on:** REARCH-02 (honest baseline committed to the main branch).

---

## Requirement Definitions

| ID | Description | Type |
|----|-------------|------|
| REARCH-01 | Capture new live `claude` outputs for S-P01, S-P02, S-P05, and S-N04; classify each run's output as detector false-negative or genuine agent routing gap using the Phase 76 Diagnosis Gate pattern (same `_wrap_for_bypass` approach-② channel + `stream-json` transport) | live capture + classification |
| REARCH-02 | Broaden `scripts/_battery_core.py` `_TECHNIQUE_CATEGORIES` markers based on REARCH-01 captures (capture-backed per marker, provenance comments citing capture file + run date, `MIN_HEADER_HITS=2` preserved, no anti-masking regression — `_COMPOSER_FOCUS_CEILING=4` unchanged) | code change |
| REARCH-03 | All offline gates green simultaneously before any live spend in REARCH-02: STEP0-08 (`check-step0-emulator.py --self-test`), BATT-06/FU-21 (`check-routing-battery.py --self-test`), DUAL-04 (`sync-content.py --check`) | offline gate |
| REARCH-04 | Single authoritative 60-invocation live run (`python3 scripts/check-step0-live.py --repeat 5 --min-pass 3`, from `/tmp`, one run only) records honest baseline `tests/step0-baseline-vX.Y.md` with true K/N for every row; never forced; prior baselines v5.0–v5.3 preserved byte-for-byte | live run |
| REARCH-05 | Each of RR-79-01, RR-79-02, RR-79-03, and RR-80-01 is explicitly resolved in the new baseline: closed if the row reaches min-pass (K/N ≥ 3/5), or carried forward with an updated residual ID and documented honest K/N if still below min-pass | honesty gate |
| REARCH-06 | Offline sentinels updated to lock the resolved or carried-forward states from REARCH-05; GEN-01 row in `check-traceability.py _rows_active_tail()` flipped from `scheduled` to `reproducible` with confirming artifact link to the new baseline file; `docs/requirements-matrix.md` regenerated; all offline gates green simultaneously: TRACE-03, BATT-06, STEP0-06, STEP0-08, DUAL-04 | sentinel + reconciliation |

---

## Honesty-Not-Score Note

The live K/N figures recorded in `tests/step0-baseline-v5.3.md` (S-P01 1/5, S-P02 0/5,
S-P05 0/5, S-N04 2/5) are honest carry-forwards. They are not chased to a forced PASS in
v6.2 because doing so without the full structural classifier work would be a score-mask —
precisely what honesty-not-score discipline (D-01) prohibits.

Converting GEN-01 to this committed future milestone changes the gap *status* (from
"perpetually deferred open gap" to "scheduled forward commitment"), not the live *scores*.
The live scores will remain as honest carry-forwards, measured by the existing Step 0
harness (`scripts/check-step0-live.py`), until GEN-01-REARCH executes REARCH-01 through
REARCH-06 and delivers the rearchitecture work.

This milestone resolves GEN-01 as a **committed scheduled future milestone** (the confirming
artifact is this file + the ROADMAP mirror pointer written in Phase 88 Plan 01). It does NOT
claim the routing quality gap is closed — that claim requires the live re-baseline committed
by REARCH-04 to reach min-pass for the affected rows.

---

*Milestone stub authored: 2026-06-15*
*Authored in: Phase 88-gen-01-execution, Plan 01*
*Activating ADR: docs/gen-01-decision.md (Phase 87)*
*Supersedes: GEN-01 open-gap entry (gap→scheduled via Phase 88 path (c))*
