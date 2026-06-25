# Requirements and Traceability

This file is the active canonical source of truth for requirements and traceability in this project; it supersedes the 26 scattered `milestones/vX.Y-REQUIREMENTS.md` files for all forward use (CANON-01).

## Status

**Coverage headline:** 121 reproducible / 85 audit-only / 0 gap / 206 total

The full 206-row capability-to-requirement-to-test mapping is in the generated matrix:
[`requirements-matrix.md`](requirements-matrix.md)

> **Honesty note (D-07):** A non-zero audit-only count is the expected honest success state.
> 85 requirements are validated by milestone audit without a re-runnable gate (audit-only);
> No current open gaps — GEN-01 → reproducible (Phase 93, committed v7.6 baseline Phase 114 + v7.7 CONF-01 baseline Phase 117; latest artifact `tests/step0-baseline-v7.7.md`; "live re-baseline deferred" carry-forward carried since v7.1 is now RESOLVED) and GEN-02 → reproducible (runbook + wrapper; artifact `docs/live-monitoring-runbook.md`);
> 3 further requirements are confirmed by offline gates but remain honest live carry-forwards (RR-80-01, RR-114-01 (supersedes RR-108-01, supersedes RR-95-01, supersedes RR-92-01, supersedes RR-79-02), RR-77-08); RR-108-02 is CLOSED at 4/5 ≥ min-pass (Phase 114 v7.6 re-baseline — ID retained, sentinel present as regression guard); RR-79-01 is CLOSED at 3/5 ≥ min-pass (Phase 117 v7.7 CONF-01 — ID retained, sentinel present as regression guard); RR-117-01 (S-P03 fishbone) CLOSED 5/5 at Phase 117 CONF-01; RR-117-02 (S-N03 precision) minted Phase 117 CONF-02.

## Active Surface

Exactly 9 live items (FIX-01/FIX-02/CONF-01/CONF-02 done: RR-79-01 and new fishbone sentinel CLOSED; new precision sentinel minted). Nothing shipped or superseded belongs here.

1. **RR-79-01** [HIGH] — S-P01 pre-mortem. **CLOSED at Phase 117 v7.7 CONF-01** (S-P01 3/5 ≥ min-pass; FIX-01 detector recalibration confirmed out-of-sample). ID retained; sentinel re-pointed to v7.7 live captures, vector [0,2,3,1,4], retained as regression guard. Confirmed by BATT-06 (RR-79-01 sentinel in `_battery_core.self_test_boundary()`).

2. **RR-114-01** [HIGH] — S-P02 inversion carry-forward (Phase 114, supersedes RR-108-01, supersedes RR-95-01, supersedes RR-92-01, supersedes RR-79-02; full chain: RR-79-02 -> RR-92-01 -> RR-95-01 -> RR-108-01 -> RR-114-01). 1/5 FAIL at Phase 114 v7.6 re-baseline (no change vs v7.4 1/5; below min-pass 3/5). Confirmed by BATT-06 (RR-114-01 sentinel in `_battery_core.self_test_boundary()`); honest live carry-forward (not resolved; out of scope at Phase 117).

3. **RR-108-02** [HIGH] — S-P05 trade-off (Phase 108, supersedes RR-95-02, supersedes RR-92-02, supersedes RR-79-03; full chain: RR-79-03 -> RR-92-02 -> RR-95-02 -> RR-108-02 CLOSED). **CLOSED at 4/5 ≥ min-pass at Phase 114 v7.6 re-baseline** (the lone canonical improver; S-P05 trade-off cleared min-pass). ID retained; sentinel in `_battery_core.self_test_boundary()` re-pointed to the v7.6 count vector [2,2,2,2,1] and remains present as a regression guard.

4. **RR-77-08** [MEDIUM] — CEILING=4 vs expected=3 warning: incidental `\bVerdict\b` IGNORECASE match in `composer_hits`; not a blocking defect but unresolved. Locked by BATT-06 anti-masking sentinel (CEILING=4) in `_battery_core.self_test_boundary()`.

5. **GEN-01** [reproducible] — Full Step 0 classifier rearchitecture (GEN-01-REARCH, Phases 91-93). GEN-01 is now reproducible: the Step 0 classifier capability is reproducibly measured by the committed baselines — v7.6 (Phase 114) and v7.7 CONF-01 (Phase 117). Latest artifact: `tests/step0-baseline-v7.7.md`. Earned by the committed baselines, not passing scores. Key Phase 117 outcomes: S-P01 3/5 PASS + S-P03 5/5 PASS (fix confirmed out-of-sample); SHORT OF BAR overall (S-N01 0/5 / S-N02 2/5 over-route; transcript-confirmed genuine pre-mortem routing on semantically-pre-mortem prompts, not a fix defect); RR-114-01 S-P02 inversion carried untouched; RR-108-03 decompose 0/5 RESOLVED-BY-MERGE (see [`decompose-five-whys-merge.md`](decompose-five-whys-merge.md)); RR-108-04 estimate 0/5 CARRIED-INDETERMINATE; RR-108-05 theoretical-limit 0/5 CARRIED-INDETERMINATE. Fix outcome recorded in [`merge-validation-verdict.md`](merge-validation-verdict.md) (Phase 117 section). No longer an open gap.

6. **GEN-02** [reproducible] — Periodic live monitoring cadence; runbook + wrapper script established (Phase 89). Confirmed by git-tracked runbook and wrapper; artifact: `docs/live-monitoring-runbook.md`. No longer an open gap.

7. **RR-80-01** [CRITICAL] — S-N04 semantically-pre-mortem over-routing. CLOSED 4/5 at Phase 95 re-baseline (v6.4). At v7.4: S-N04 2/5 (regression). At v7.6: S-N04 3/5 PASS. At Phase 117 v7.7 CONF-01: S-N04 2/5, NON_BLOCKING (D-16 — the live agent genuinely routes to focused pre-mortem on this semantically-pre-mortem prompt; sentinel re-pointed to v7.7 vector [1,2,2,1,3]).
   **Lineage:** Formerly tracked as S-N04 (placeholder `RR-75-NN`). Assigned RR-80-01 in Phase 83 (D-05).
   Confirmed by STEP0-08 (S-N04 emulator assertion in `check-step0-emulator.py --self-test`) and BATT-06 (marker-counting assertion in `_battery_core.self_test_boundary()`).

8. **RR-117-01** [HIGH] — S-P03 fishbone. **CLOSED at Phase 117 v7.7 CONF-01** (S-P03 5/5; FIX-01 detector recalibration confirmed out-of-sample). First fishbone vector sentinel; RR-75-03 lineage. Sentinel asserts v7.7 vector [3,3,2,2,2] + fishbone drift guard == 7. ID retained; retained as regression guard. Confirmed by BATT-06 (RR-117-01 sentinel in `_battery_core.self_test_boundary()`).

9. **RR-117-02** [MEDIUM] — S-N03 precision (Phase 117 CONF-02). The one truly-oblique negative in the v7.7 CONF-01 run. Proves FIX-01 did NOT hurt routing on genuinely-unrelated prompts (debugging request, 0 pre-mortem markers on all 5 runs). Sentinel asserts v7.7 vector [0,0,0,0,0]. Confirmed by BATT-06 (RR-117-02 sentinel in `_battery_core.self_test_boundary()`). D-17 precision finding locked.

## Gap Findings

Summary of Phase 82 gap analysis. Full details in [`requirements-matrix.md`](requirements-matrix.md) (sections "Gap Findings (GAP-01)" and "Future-Milestone Candidate Work List (GAP-02)").

### GAP-01: Current gap picture

**No current open gaps.** Both previously-open gap rows are resolved:

- **GEN-01** → **reproducible** (Phase 93, GEN-01-REARCH Phases 91-93; artifact pointer updated to v7.6 baseline in Phase 114 Plan 02). Artifact: `tests/step0-baseline-v7.6.md`. The Step 0 classifier capability is now reproducibly measured by the committed v7.6 live re-baseline (Phase 114); earned by the committed baseline, not a passing score (BATTERY: FAIL, P 3/8 REGRESSION — RR-114-01 S-P02 1/5 CARRIED, RR-108-02 S-P05 4/5 CLOSED, new S-P01/S-P03 regressions — legitimate v7.6 honest state; verdict recorded in [`merge-validation-verdict.md`](merge-validation-verdict.md)). The "live re-baseline deferred" carry-forward (carried since v7.1) is RESOLVED by the committed v7.6 re-baseline. Removed from the open-gap set.
- **GEN-02** → **reproducible** (runbook + wrapper script; Phase 89). Artifact: `docs/live-monitoring-runbook.md`. The periodic live monitoring cadence is now confirmed by a git-tracked runbook with re-runnable harness invocations; it is removed from the open-gap set.

**7 reproducible rows with confirming offline gates** (live behavior documented at Phase 114 v7.6 re-baseline + Phase 117 v7.7 CONF-01):

- **RR-80-01** [CRITICAL] — S-N04 semantically-pre-mortem over-routing; NON_BLOCKING per D-16. Observed 2/5 at Phase 117 v7.7 CONF-01 (genuine pre-mortem routing, not a fix defect). Sentinel re-pointed to v7.7 vector [1,2,2,1,3]. Confirmed by STEP0-08 + BATT-06. Artifact: `scripts/_battery_core.py#self_test_boundary`.
- **RR-79-01** [HIGH] — S-P01 **CLOSED** at 3/5 ≥ min-pass at Phase 117 v7.7 CONF-01 (FIX-01 confirmed out-of-sample; v7.7 vector [0,2,3,1,4]; ID retained, sentinel retained as regression guard). Confirmed by BATT-06. Artifact: `scripts/_battery_core.py#self_test_boundary`.
- **RR-114-01** [HIGH] — S-P02 honest carry-forward (supersedes RR-108-01, supersedes RR-95-01, supersedes RR-92-01, supersedes RR-79-02; chain: RR-79-02 -> RR-92-01 -> RR-95-01 -> RR-108-01 -> RR-114-01); CARRIED 1/5 at Phase 114 v7.6 re-baseline; out of scope at Phase 117. Confirmed by BATT-06. Artifact: `scripts/_battery_core.py#self_test_boundary`.
- **RR-108-02** [HIGH] — S-P05 CLOSED at 4/5 ≥ min-pass at Phase 114 v7.6 re-baseline (chain: RR-79-03 -> RR-92-02 -> RR-95-02 -> RR-108-02 CLOSED). ID retained, sentinel re-pointed to v7.6 vector [2,2,2,2,1]. Confirmed by BATT-06. Artifact: `scripts/_battery_core.py#self_test_boundary`.
- **RR-77-08** [MEDIUM] — CEILING=4 warning; locked by BATT-06 anti-masking sentinel (CEILING=4). Artifact: `scripts/_battery_core.py#self_test_boundary`.
- **RR-117-01** [HIGH] — S-P03 fishbone **CLOSED** at 5/5 ≥ min-pass at Phase 117 v7.7 CONF-01 (FIX-01 confirmed out-of-sample; first fishbone vector sentinel; v7.7 vector [3,3,2,2,2]; RR-75-03 lineage; retained as regression guard). Confirmed by BATT-06. Artifact: `scripts/_battery_core.py#self_test_boundary`.
- **RR-117-02** [MEDIUM] — S-N03 precision sentinel; [0,0,0,0,0] at v7.7 CONF-01. Proves FIX-01 did not hurt routing on genuinely-oblique prompts. Confirmed by BATT-06. Artifact: `scripts/_battery_core.py#self_test_boundary`.

**85 audit-only rows** — validated by milestone audit; no re-runnable gate exists. These represent genuine coverage but cannot be re-verified programmatically without new confirming tests.

### GAP-02: Candidate work list

Future-milestone candidates: add a confirming Test-Network or Methodology gate for each remaining audit-only row. Priority: MEDIUM audit-only items (85 rows). The rows promoted in Phase 86 (RR-80-01, RR-79-01, RR-79-02→RR-92-01→RR-95-01→RR-108-01→RR-114-01, RR-79-03→RR-92-02→RR-95-02→RR-108-02-CLOSED, RR-77-08) now have confirming offline gates; Phase 117 CONF-02 adds RR-117-01 (S-P03 fishbone CLOSED) and RR-117-02 (S-N03 precision). Closing the remaining live routing dip (RR-114-01 S-P02 1/5, chain: RR-79-02->RR-92-01->RR-95-01->RR-108-01->RR-114-01) is a future live-routing milestone. RR-108-02 S-P05 is CLOSED at 4/5 at the v7.6 re-baseline (lone canonical improver); RR-79-01 S-P01 and RR-117-01 S-P03 are CLOSED at Phase 117 v7.7 CONF-01. v7.4 introduced three first-time residuals: RR-108-03 (decompose, 0/5) RESOLVED-BY-MERGE (v7.5 decompose→five-whys merge, see [`decompose-five-whys-merge.md`](decompose-five-whys-merge.md)), RR-108-04 (estimate, 0/5) CARRIED-INDETERMINATE (spend-limit-truncated), RR-108-05 (theoretical-limit, 0/5) CARRIED-INDETERMINATE (spend-limit-truncated). v7.6 Phase 114 measurement: S-P16 0/5 (merge did NOT improve five-whys routing — REGRESSION; fix forward-committed and APPLIED at Phase 117 — see [`merge-validation-verdict.md`](merge-validation-verdict.md) Phase 117 section); S-P01/S-P03 regressions RESOLVED at Phase 117 v7.7 CONF-01. Still-deferred merge pairs: theoretical-limit↔inversion (SECOND recommendation, own future milestone) and estimate↔? (FLAG, partner unscoped). GEN-01 and GEN-02 are resolved (see GAP-01 above) and no longer appear in this work list. Phase 117 FIX-01/FIX-02/CONF-01/CONF-02 complete: the v7.7 fix-and-confirm chain is closed (honesty-not-score: SHORT OF BAR overall per D-17, but the positive conjuncts S-P01 3/5 + S-P03 5/5 confirmed; S-N01/S-N02 failures are transcript-confirmed genuine pre-mortem routing on semantically-pre-mortem prompts, not fix defects).

## Historical Ledger

One row per milestone. Each links into [`history/`](history/) for the frozen snapshots.
Milestones with no audit file did not produce one at the time of shipping.

| Milestone | Status | Requirements | Roadmap | Audit |
|-----------|--------|-------------|---------|-------|
| v1.0 | shipped 2026-05-18 | [v1.0-REQUIREMENTS.md](history/v1.0-REQUIREMENTS.md) | [v1.0-ROADMAP.md](history/v1.0-ROADMAP.md) | [v1.0-MILESTONE-AUDIT.md](history/v1.0-MILESTONE-AUDIT.md) |
| v1.1 | shipped 2026-05-19 | [v1.1-REQUIREMENTS.md](history/v1.1-REQUIREMENTS.md) | [v1.1-ROADMAP.md](history/v1.1-ROADMAP.md) | — |
| v1.2 | shipped 2026-05-20 | [v1.2-REQUIREMENTS.md](history/v1.2-REQUIREMENTS.md) | [v1.2-ROADMAP.md](history/v1.2-ROADMAP.md) | — |
| v2.0 | shipped 2026-05-22 | [v2.0-REQUIREMENTS.md](history/v2.0-REQUIREMENTS.md) | [v2.0-ROADMAP.md](history/v2.0-ROADMAP.md) | [v2.0-MILESTONE-AUDIT.md](history/v2.0-MILESTONE-AUDIT.md) |
| v3.0 | shipped 2026-05-23 | [v3.0-REQUIREMENTS.md](history/v3.0-REQUIREMENTS.md) | [v3.0-ROADMAP.md](history/v3.0-ROADMAP.md) | [v3.0-MILESTONE-AUDIT.md](history/v3.0-MILESTONE-AUDIT.md) |
| v3.1 | shipped 2026-05-23 | [v3.1-REQUIREMENTS.md](history/v3.1-REQUIREMENTS.md) | [v3.1-ROADMAP.md](history/v3.1-ROADMAP.md) | — |
| v3.2 | shipped 2026-05-24 | [v3.2-REQUIREMENTS.md](history/v3.2-REQUIREMENTS.md) | [v3.2-ROADMAP.md](history/v3.2-ROADMAP.md) | [v3.2-MILESTONE-AUDIT.md](history/v3.2-MILESTONE-AUDIT.md) |
| v3.3 | shipped 2026-05-25 | [v3.3-REQUIREMENTS.md](history/v3.3-REQUIREMENTS.md) | [v3.3-ROADMAP.md](history/v3.3-ROADMAP.md) | [v3.3-MILESTONE-AUDIT.md](history/v3.3-MILESTONE-AUDIT.md) |
| v3.4 | shipped 2026-05-25 | [v3.4-REQUIREMENTS.md](history/v3.4-REQUIREMENTS.md) | [v3.4-ROADMAP.md](history/v3.4-ROADMAP.md) | — |
| v3.5 | shipped 2026-05-25 | [v3.5-REQUIREMENTS.md](history/v3.5-REQUIREMENTS.md) | [v3.5-ROADMAP.md](history/v3.5-ROADMAP.md) | — |
| v3.6 | shipped 2026-05-26 | [v3.6-REQUIREMENTS.md](history/v3.6-REQUIREMENTS.md) | [v3.6-ROADMAP.md](history/v3.6-ROADMAP.md) | — |
| v3.7 | shipped 2026-05-27 | [v3.7-REQUIREMENTS.md](history/v3.7-REQUIREMENTS.md) | [v3.7-ROADMAP.md](history/v3.7-ROADMAP.md) | — |
| v3.8 | shipped 2026-05-28 | [v3.8-REQUIREMENTS.md](history/v3.8-REQUIREMENTS.md) | [v3.8-ROADMAP.md](history/v3.8-ROADMAP.md) | [v3.8-MILESTONE-AUDIT.md](history/v3.8-MILESTONE-AUDIT.md) |
| v3.9 | shipped 2026-05-29 | [v3.9-REQUIREMENTS.md](history/v3.9-REQUIREMENTS.md) | [v3.9-ROADMAP.md](history/v3.9-ROADMAP.md) | — |
| v3.10 | shipped 2026-05-29 | [v3.10-REQUIREMENTS.md](history/v3.10-REQUIREMENTS.md) | [v3.10-ROADMAP.md](history/v3.10-ROADMAP.md) | — |
| v3.11 | shipped 2026-05-30 | [v3.11-REQUIREMENTS.md](history/v3.11-REQUIREMENTS.md) | [v3.11-ROADMAP.md](history/v3.11-ROADMAP.md) | — |
| v3.12 | shipped 2026-05-30 | [v3.12-REQUIREMENTS.md](history/v3.12-REQUIREMENTS.md) | [v3.12-ROADMAP.md](history/v3.12-ROADMAP.md) | [v3.12-MILESTONE-AUDIT.md](history/v3.12-MILESTONE-AUDIT.md) |
| v3.13 | shipped 2026-06-03 | [v3.13-REQUIREMENTS.md](history/v3.13-REQUIREMENTS.md) | [v3.13-ROADMAP.md](history/v3.13-ROADMAP.md) | [v3.13-MILESTONE-AUDIT.md](history/v3.13-MILESTONE-AUDIT.md) |
| v4.0 | shipped 2026-06-04 | [v4.0-REQUIREMENTS.md](history/v4.0-REQUIREMENTS.md) | [v4.0-ROADMAP.md](history/v4.0-ROADMAP.md) | [v4.0-MILESTONE-AUDIT.md](history/v4.0-MILESTONE-AUDIT.md) |
| v4.1 | shipped 2026-06-06 | [v4.1-REQUIREMENTS.md](history/v4.1-REQUIREMENTS.md) | [v4.1-ROADMAP.md](history/v4.1-ROADMAP.md) | [v4.1-MILESTONE-AUDIT.md](history/v4.1-MILESTONE-AUDIT.md) |
| v4.2 | shipped 2026-06-11 | [v4.2-REQUIREMENTS.md](history/v4.2-REQUIREMENTS.md) | [v4.2-ROADMAP.md](history/v4.2-ROADMAP.md) | [v4.2-MILESTONE-AUDIT.md](history/v4.2-MILESTONE-AUDIT.md) |
| v4.3 | shipped 2026-06-11 | [v4.3-REQUIREMENTS.md](history/v4.3-REQUIREMENTS.md) | [v4.3-ROADMAP.md](history/v4.3-ROADMAP.md) | [v4.3-MILESTONE-AUDIT.md](history/v4.3-MILESTONE-AUDIT.md) |
| v5.0 | shipped 2026-06-12 | [v5.0-REQUIREMENTS.md](history/v5.0-REQUIREMENTS.md) | [v5.0-ROADMAP.md](history/v5.0-ROADMAP.md) | — |
| v5.1 | shipped 2026-06-13 | [v5.1-REQUIREMENTS.md](history/v5.1-REQUIREMENTS.md) | [v5.1-ROADMAP.md](history/v5.1-ROADMAP.md) | [v5.1-MILESTONE-AUDIT.md](history/v5.1-MILESTONE-AUDIT.md) |
| v5.2 | shipped 2026-06-13 | [v5.2-REQUIREMENTS.md](history/v5.2-REQUIREMENTS.md) | [v5.2-ROADMAP.md](history/v5.2-ROADMAP.md) | [v5.2-MILESTONE-AUDIT.md](history/v5.2-MILESTONE-AUDIT.md) |
| v5.3 | shipped 2026-06-14 | [v5.3-REQUIREMENTS.md](history/v5.3-REQUIREMENTS.md) | [v5.3-ROADMAP.md](history/v5.3-ROADMAP.md) | [v5.3-MILESTONE-AUDIT.md](history/v5.3-MILESTONE-AUDIT.md) |

## Cross-links

- **Generated matrix (206 rows):** [`requirements-matrix.md`](requirements-matrix.md)
- **Frozen milestone history:** [`history/`](history/)
- **Project overview and active milestone context:** [`../.planning/PROJECT.md`](../.planning/PROJECT.md)
  *(Note: `.planning/` is gitignored. The canonical historical detail is the promoted `docs/history/` copies linked above.)*
