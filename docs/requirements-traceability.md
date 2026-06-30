# Requirements and Traceability

This file is the active canonical source of truth for requirements and traceability in this project; it supersedes the 26 scattered `milestones/vX.Y-REQUIREMENTS.md` files for all forward use (CANON-01).

## Status

**Coverage headline:** 133 reproducible / 96 audit-only / 0 gap / 229 total

The full 218-row capability-to-requirement-to-test mapping is in the generated matrix:
[`requirements-matrix.md`](requirements-matrix.md)

> **Honesty note (D-07):** A non-zero audit-only count is the expected honest success state.
> 96 requirements are validated by milestone audit without a re-runnable gate (audit-only);
> No current open gaps — GEN-01 → reproducible (Phase 93; artifact bumped to the committed v7.11 live re-baseline Phase 129; latest artifact `tests/step0-baseline-v7.11.md`; reproducible = measured, not passing — v7.11 BATTERY: FAIL P 4/8) and GEN-02 → reproducible (runbook + wrapper; artifact `docs/live-monitoring-runbook.md`);
> Headline change vs prior 121/85/0/206: +4 reproducible rows added to the active tail in Phase 119 CONF-04 — RR-117-01 (S-P03 fishbone, minted Phase 117 CONF-02), RR-117-02 (S-N03 precision, minted Phase 117 CONF-02), RR-119-01 (S-N01 resolved, minted Phase 119 CONF-04), RR-119-02 (S-N02 resolved, minted Phase 119 CONF-04). These rows existed as sentinels in _battery_core.py but were not previously registered in the matrix.
> Headline change vs prior 125/85/0/210: +8 reproducible rows added in Phase 123 RECON-01 — the v7.9 milestone requirements NEGCAT-01, NEGCAT-02, OCH-01, OCH-02, OCH-03, COLLIDE-01, COLLIDE-02, RECON-01, each backed by a deterministic offline gate (STEP0-08 for NEGCAT-01/02; DUAL-04 + BATT-06 for OCH-01/02/03; COLLIDE-01 gate for COLLIDE-01/02; TRACE-03 for RECON-01).
> Headline change vs prior 133/85/0/218: +11 audit-only rows added in Phase 131 RECON-03 — the v7.11 milestone requirements READY-01/02/03, STEP0L-01/02/03, ROUTEL-01/02, RECON-01/02/03 (audit-only; validated by one-shot manual live runs, not deterministic offline CI gates, D-04). GEN-01's artifact_link bumped v7.8 → v7.11 (paired data + gate-code edit, D-05). RR-130-01 (main-routing inline-answering regression) recorded as a documented residual with NO matrix row (v7.9 D-02 precedent).
> Headline change vs prior 133/96/0/229: **zero** — RR-130-01 remains a documented residual with no matrix row (v7.9 D-02 precedent); Phase 133 fix is a prose edit in `shared/` with no new matrix row. Reconcile = prove zero drift, not re-count (D-03).
> 3 further requirements are confirmed by offline gates but remain honest live carry-forwards (RR-80-01, RR-114-01 (supersedes RR-108-01, supersedes RR-95-01, supersedes RR-92-01, supersedes RR-79-02), RR-77-08); RR-108-02 is CLOSED at 4/5 ≥ min-pass (Phase 114 v7.6 re-baseline — ID retained, sentinel present as regression guard); RR-79-01 is CLOSED at 3/5 ≥ min-pass (Phase 117 v7.7 CONF-01; CLOSE SUSTAINED 3/5 at Phase 119 v7.8 CONF-03 — ID retained, sentinel present as regression guard); RR-117-01 (S-P03 fishbone) CLOSED 5/5 at Phase 117 CONF-01; CLOSE SUSTAINED 4/5 at Phase 119 CONF-03; RR-117-02 (S-N03 precision) minted Phase 117 CONF-02, re-pointed to v7.8 Phase 119 CONF-04; RR-119-01/RR-119-02 (S-N01/S-N02 resolved-over-bar) minted Phase 119 CONF-04.

## Active Surface

Exactly 12 live items (v7.12: RR-130-01 offline fix applied Phase 133 — FIX-APPLIED, still OPEN, ID kept). Nothing shipped or superseded belongs here.

1. **RR-79-01** [HIGH] — S-P01 pre-mortem. **CLOSED at Phase 117 v7.7 CONF-01** (S-P01 3/5 ≥ min-pass; FIX-01 detector recalibration confirmed out-of-sample). **CLOSE SUSTAINED at Phase 119 v7.8 CONF-03** (S-P01 3/5 = v7.4 floor). ID retained; sentinel re-pointed to v7.8 live captures, vector [1,2,3,0,2], retained as regression guard. Confirmed by BATT-06 (RR-79-01 sentinel in `_battery_core.self_test_boundary()`).

2. **RR-114-01** [HIGH] — S-P02 inversion (Phase 114, supersedes RR-108-01, supersedes RR-95-01, supersedes RR-92-01, supersedes RR-79-02; full chain: RR-79-02 -> RR-92-01 -> RR-95-01 -> RR-108-01 -> RR-114-01). 1/5 FAIL at Phase 114 v7.6 re-baseline (no change vs v7.4 1/5; below min-pass 3/5). **RESOLVED-STRUCTURALLY-OFFLINE Phase 121 OCH-02**: the detector now reads the heading-anchored output-contract headers (inversion extended 9→13 by adding ## Inverted Claim / ## Failure-Guaranteeing Conditions / ## Necessary Preconditions / ## Stress-Test Verdict); the frozen v7.6 vector [2,0,1,1,1] is UNCHANGED (captures predate the headers); the live S-P02 pass-rate re-measure is the forward-committed half (honesty-not-score, D-01). ID kept; no successor minted. Confirmed by BATT-06 (RR-114-01 sentinel in `_battery_core.self_test_boundary()`).

3. **RR-108-02** [HIGH] — S-P05 trade-off (Phase 108, supersedes RR-95-02, supersedes RR-92-02, supersedes RR-79-03; full chain: RR-79-03 -> RR-92-02 -> RR-95-02 -> RR-108-02 CLOSED). **CLOSED at 4/5 ≥ min-pass at Phase 114 v7.6 re-baseline** (the lone canonical improver; S-P05 trade-off cleared min-pass). **Structurally extended Phase 121 OCH-02**: trade-off extended 6→10 by adding 4 heading-anchored output-contract markers (## Options / ## Criteria & Weights / ## Scoring / ## Recommendation); frozen v7.6 vector [2,2,2,2,1] UNCHANGED (captures predate the headers); live trade-off emission re-measure forward-committed (honesty-not-score, D-01). ID retained; sentinel re-pointed to v7.6 count vector [2,2,2,2,1] and remains present as a regression guard.

4. **RR-77-08** [MEDIUM] — CEILING=4 vs expected=3 warning: incidental `\bVerdict\b` IGNORECASE match in `composer_hits`; not a blocking defect but unresolved. Locked by BATT-06 anti-masking sentinel (CEILING=4) in `_battery_core.self_test_boundary()`.

5. **GEN-01** [reproducible] — Full Step 0 classifier rearchitecture (GEN-01-REARCH, Phases 91-93). GEN-01 is now reproducible: the Step 0 classifier capability is reproducibly measured by the committed baselines — v7.6 (Phase 114), v7.7 CONF-01 (Phase 117), v7.8 CONF-03 (Phase 119), and the v7.11 whole-system live re-baseline (Phase 129). Latest artifact: `tests/step0-baseline-v7.11.md` (bumped Phase 131 RECON-03, paired data + gate-code edit D-05). Reproducible = measured, not passing. Phase 129 v7.11 verdict: BATTERY: FAIL, P 4/8 (S-P01 5/5, S-P03 4/5, S-P05 5/5, S-P06 4/5 PASS; S-P02 2/5, S-P04 2/5, S-P10 0/5, S-P14 0/5 FAIL) — honest measured state (honesty-not-score, D-01). No open gap (the tier reflects reproducible measurement, not a passing score).

6. **GEN-02** [reproducible] — Periodic live monitoring cadence; runbook + wrapper script established (Phase 89). Confirmed by git-tracked runbook and wrapper; artifact: `docs/live-monitoring-runbook.md`. No longer an open gap.

7. **RR-80-01** [CRITICAL] — S-N04 semantically-pre-mortem over-routing. CLOSED 4/5 at Phase 95 re-baseline (v6.4). At v7.4: S-N04 2/5 (regression). At v7.6: S-N04 3/5 PASS. At Phase 117 v7.7 CONF-01: S-N04 2/5, NON_BLOCKING (D-16 — genuine pre-mortem routing on semantically-pre-mortem prompt). At Phase 119 v7.8 CONF-03: S-N04 5/5 non-blocking (Phase-118 prose fix moved over bar; run5 is_error anomaly, count=0). Sentinel re-pointed to v7.8 vector [1,1,1,1,0].
   **Lineage:** Formerly tracked as S-N04 (placeholder `RR-75-NN`). Assigned RR-80-01 in Phase 83 (D-05).
   Confirmed by STEP0-08 (S-N04 emulator assertion in `check-step0-emulator.py --self-test`) and BATT-06 (marker-counting assertion in `_battery_core.self_test_boundary()`).

8. **RR-117-01** [HIGH] — S-P03 fishbone. **CLOSED at Phase 117 v7.7 CONF-01** (S-P03 5/5; FIX-01 detector recalibration confirmed out-of-sample). **CLOSE SUSTAINED at Phase 119 v7.8 CONF-03** (S-P03 4/5 ≥ v7.4 floor 3/5; D-1b softening). First fishbone vector sentinel; RR-75-03 lineage. Sentinel re-pointed to v7.8 vector [1,4,2,2,3] + fishbone drift guard == 7. ID retained; retained as regression guard. Confirmed by BATT-06 (RR-117-01 sentinel in `_battery_core.self_test_boundary()`).

9. **RR-117-02** [MEDIUM] — S-N03 precision (Phase 117 CONF-02; re-pointed to v7.8 Phase 119 CONF-04). The one truly-oblique negative: debugging prompt with no pre-mortem framing. Proves FIX-01+FIX-03/FIX-04 did NOT hurt routing on genuinely-oblique prompts (5/5 full-composer at v7.8). Sentinel re-pointed to v7.8 vector [1,0,0,0,0] (all runs stay below MIN_HEADER_HITS). Confirmed by BATT-06 (RR-117-02 sentinel in `_battery_core.self_test_boundary()`). D-17 precision finding sustained.

10. **RR-119-01** [MEDIUM] — S-N01 over-routing, resolved-over-bar (Phase 119 CONF-04, minted). At v7.7: S-N01 0/5 (all-over-route). At v7.8 CONF-03: S-N01 3/5 PASS (Phase-118 FIX-03/FIX-04 prose fix moved over bar). Residual disposition: RESOLVED-OVER-BAR with detector-under-count caveat (negative passes are a MIX of genuine clarification-holds and under-counts; D-01). NOT a reclassification (D-4). Sentinel asserts v7.8 vector [0,2,1,1,3]. Confirmed by BATT-06 (RR-119-01 sentinel in `_battery_core.self_test_boundary()`).

11. **RR-119-02** [MEDIUM] — S-N02 over-routing, resolved-over-bar (Phase 119 CONF-04, minted). At v7.7: S-N02 2/5 (over-routes on 3 of 5 runs). At v7.8 CONF-03: S-N02 3/5 PASS (Phase-118 FIX-03/FIX-04 prose fix moved over bar). Residual disposition: RESOLVED-OVER-BAR with detector-under-count caveat (runs 2,3 are documented detector under-counts where agent still ran a pre-mortem; D-01). NOT a reclassification (D-4). Sentinel asserts v7.8 vector [0,3,3,1,1]. Confirmed by BATT-06 (RR-119-02 sentinel in `_battery_core.self_test_boundary()`)..

12. **RR-130-01** [HIGH] — Main-routing inline-answering regression (Phase 130). P **1/13** DELEGATE FAIL at the v7.11 live re-baseline (`tests/routing-baseline-v7.11.md`) vs the v3.13 anchor (P 11/13); the orchestrator answers the first-principles prompt **inline** (`num_turns:1`, `stop_reason:end_turn`, no `Task` tool_use) instead of auto-delegating — only P4 delegated. Likely a newer/more-capable orchestrator model satisfying the prompt directly. Negatives unchanged (N 20/20). ID kept (RR-`<phase>`-NN convention; Phase-130 slot free). **Documented residual with NO matrix row** (v7.9 D-02 precedent); named the open whole-system gap by `docs/whole-system-remeasure-verdict.md`. honesty-not-score (D-01): recorded as observed, never forced. Offline fix **applied at Phase 133** (imperative `description:` rewrite of `shared/spine/SKILL.meta.yml`, regenerated at zero drift; STRENGTHEN verdict per `docs/rr-130-01-diagnosis.md`). Residual remains **OPEN** — no resolution tier claimed; authoritative live P re-measure forward-committed. ID kept (D-01 / D-02 / D-04).

## Gap Findings

Summary of Phase 82 gap analysis. Full details in [`requirements-matrix.md`](requirements-matrix.md) (sections "Gap Findings (GAP-01)" and "Future-Milestone Candidate Work List (GAP-02)").

### GAP-01: Current gap picture

**No current open gaps.** Both previously-open gap rows are resolved:

- **GEN-01** → **reproducible** (Phase 93, GEN-01-REARCH Phases 91-93; artifact pointer updated to v7.8 baseline in Phase 119 Plan 03). Artifact: `tests/step0-baseline-v7.8.md`. The Step 0 classifier capability is now reproducibly measured by the committed v7.8 live re-baseline (Phase 119 CONF-03); earned by the committed baseline, not a passing score (BATTERY: PASS, D-1c CONFIRMED — Phase-118 FIX-03/FIX-04 prose fix confirmed; all 5 blocking conjuncts hold). The "live re-baseline deferred" carry-forward (carried since v7.1) is RESOLVED. Removed from the open-gap set.
- **GEN-02** → **reproducible** (runbook + wrapper script; Phase 89). Artifact: `docs/live-monitoring-runbook.md`. The periodic live monitoring cadence is now confirmed by a git-tracked runbook with re-runnable harness invocations; it is removed from the open-gap set.

**11 reproducible rows with confirming offline gates** (live behavior documented at Phase 114 v7.6 re-baseline + Phase 117 v7.7 CONF-01 + Phase 119 v7.8 CONF-03):

- **RR-80-01** [CRITICAL] — S-N04 semantically-pre-mortem over-routing; NON_BLOCKING per D-16. Observed 5/5 at Phase 119 v7.8 CONF-03 (Phase-118 prose fix moved over bar; run5 is_error anomaly). Sentinel re-pointed to v7.8 vector [1,1,1,1,0]. Confirmed by STEP0-08 + BATT-06. Artifact: `scripts/_battery_core.py#self_test_boundary`.
- **RR-79-01** [HIGH] — S-P01 **CLOSED** at 3/5 ≥ min-pass at Phase 117 v7.7 CONF-01; **CLOSE SUSTAINED** 3/5 at Phase 119 v7.8 CONF-03 (FIX-01 confirmed; v7.8 vector [1,2,3,0,2]; ID retained, sentinel retained as regression guard). Confirmed by BATT-06. Artifact: `scripts/_battery_core.py#self_test_boundary`.
- **RR-114-01** [HIGH] — S-P02 inversion (supersedes RR-108-01, supersedes RR-95-01, supersedes RR-92-01, supersedes RR-79-02; chain: RR-79-02 -> RR-92-01 -> RR-95-01 -> RR-108-01 -> RR-114-01); CARRIED 1/5 at Phase 114 v7.6 re-baseline; **RESOLVED-STRUCTURALLY-OFFLINE Phase 121 OCH-02** (inversion extended 9→13; detector now reads heading-anchored output-contract headers; frozen v7.6 vector [2,0,1,1,1] UNCHANGED; live S-P02 re-measure forward-committed, honesty-not-score D-01; ID kept, no successor). Confirmed by BATT-06. Artifact: `scripts/_battery_core.py#self_test_boundary`.
- **RR-108-02** [HIGH] — S-P05 CLOSED at 4/5 ≥ min-pass at Phase 114 v7.6 re-baseline (chain: RR-79-03 -> RR-92-02 -> RR-95-02 -> RR-108-02 CLOSED). Structurally extended Phase 121 OCH-02 (trade-off extended 6→10; live emission re-measure forward-committed, honesty-not-score D-01). ID retained, sentinel re-pointed to v7.6 vector [2,2,2,2,1]. Confirmed by BATT-06. Artifact: `scripts/_battery_core.py#self_test_boundary`.
- **RR-77-08** [MEDIUM] — CEILING=4 warning; locked by BATT-06 anti-masking sentinel (CEILING=4). Artifact: `scripts/_battery_core.py#self_test_boundary`.
- **RR-117-01** [HIGH] — S-P03 fishbone **CLOSED** at 5/5 at Phase 117 v7.7 CONF-01; **CLOSE SUSTAINED** 4/5 (≥ v7.4 floor) at Phase 119 v7.8 CONF-03 (first fishbone vector sentinel; v7.8 vector [1,4,2,2,3]; RR-75-03 lineage; retained as regression guard). Confirmed by BATT-06. Artifact: `scripts/_battery_core.py#self_test_boundary`.
- **RR-117-02** [MEDIUM] — S-N03 precision sentinel; re-pointed to v7.8 vector [1,0,0,0,0] at Phase 119 CONF-04. All runs stay below MIN_HEADER_HITS → full-composer 5/5 at v7.8. Proves FIX-01+FIX-03/FIX-04 did not hurt routing on genuinely-oblique prompts. D-17 precision finding sustained. Confirmed by BATT-06. Artifact: `scripts/_battery_core.py#self_test_boundary`.
- **RR-119-01** [MEDIUM] — S-N01 over-routing, **RESOLVED-OVER-BAR** at Phase 119 v7.8 CONF-03 (3/5 PASS; v7.8 vector [0,2,1,1,3]; under-count caveat; NOT a reclassification, D-4). Minted Phase 119 CONF-04. Confirmed by BATT-06. Artifact: `scripts/_battery_core.py#self_test_boundary`.
- **RR-119-02** [MEDIUM] — S-N02 over-routing, **RESOLVED-OVER-BAR** at Phase 119 v7.8 CONF-03 (3/5 PASS; v7.8 vector [0,3,3,1,1]; under-count caveat documented — runs 2,3 are detector under-counts where agent still ran a pre-mortem; NOT a reclassification, D-4). Minted Phase 119 CONF-04. Confirmed by BATT-06. Artifact: `scripts/_battery_core.py#self_test_boundary`.

**85 audit-only rows** — validated by milestone audit; no re-runnable gate exists. These represent genuine coverage but cannot be re-verified programmatically without new confirming tests.

### GAP-02: Candidate work list

Future-milestone candidates: add a confirming Test-Network or Methodology gate for each remaining audit-only row. Priority: MEDIUM audit-only items (85 rows). The rows promoted in Phase 86 (RR-80-01, RR-79-01, RR-79-02→RR-92-01→RR-95-01→RR-108-01→RR-114-01, RR-79-03→RR-92-02→RR-95-02→RR-108-02-CLOSED, RR-77-08) now have confirming offline gates; Phase 117 CONF-02 adds RR-117-01 (S-P03 fishbone CLOSED) and RR-117-02 (S-N03 precision); Phase 119 CONF-04 adds RR-119-01/RR-119-02 (S-N01/S-N02 resolved-over-bar). Closing the remaining live routing dip (RR-114-01 S-P02 1/5, chain: RR-79-02->RR-92-01->RR-95-01->RR-108-01->RR-114-01) is a future live-routing milestone. RR-108-02 S-P05 is CLOSED at 4/5 at the v7.6 re-baseline (lone canonical improver); RR-79-01 S-P01 and RR-117-01 S-P03 are CLOSED at Phase 117 v7.7 CONF-01 and their CLOSE SUSTAINED at Phase 119 v7.8 CONF-03. v7.4 introduced three first-time residuals: RR-108-03 (decompose, 0/5) RESOLVED-BY-MERGE (v7.5 decompose→five-whys merge, see [`decompose-five-whys-merge.md`](decompose-five-whys-merge.md)), RR-108-04 (estimate, 0/5) CARRIED-INDETERMINATE (spend-limit-truncated at v7.4), RR-108-05 (theoretical-limit, 0/5) CARRIED-INDETERMINATE (spend-limit-truncated at v7.4). v7.6 Phase 114 measurement: S-P16 0/5 (merge did NOT improve five-whys routing — REGRESSION; fix forward-committed and APPLIED at Phase 117 — see [`merge-validation-verdict.md`](merge-validation-verdict.md) Phase 117 section); S-P01/S-P03 regressions RESOLVED at Phase 117 v7.7 CONF-01 and SUSTAINED at Phase 119 v7.8 CONF-03. Still-deferred merge pairs: theoretical-limit↔inversion (SECOND recommendation, own future milestone) and estimate↔? (FLAG, partner unscoped). GEN-01 and GEN-02 are resolved (see GAP-01 above) and no longer appear in this work list. Phase 117 FIX-01/FIX-02/CONF-01/CONF-02 + Phase 118 FIX-03/FIX-04 + Phase 119 CONF-03/CONF-04 complete: the v7.8 fix-and-confirm chain is closed (D-1c CONFIRMED; all 5 blocking conjuncts hold; honesty-not-score: positive conjuncts S-P01 3/5 + S-P03 4/5 sustained; S-N01/S-N02 moved over bar — under-count caveat documented, not reclassified D-4). Remaining deferred (out-of-scope Fix-#3): NON_BLOCKING_NEGATIVE_IDS reclassification for S-N01/S-N02 (the prompts remain semantically pre-mortem; their resolved-over-bar state is documented; future milestone).

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

- **Generated matrix (218 rows):** [`requirements-matrix.md`](requirements-matrix.md)
- **Frozen milestone history:** [`history/`](history/)
- **Project overview and active milestone context:** [`../.planning/PROJECT.md`](../.planning/PROJECT.md)
  *(Note: `.planning/` is gitignored. The canonical historical detail is the promoted `docs/history/` copies linked above.)*
- **v7.10 agent-goal alignment audit** (ALIGN-01/02/03 — authoritative prioritized inventory of method-fidelity gaps and technical debt behind the DEBT-*/METHFID-* split): [`agent-goal-alignment-audit.md`](agent-goal-alignment-audit.md)
