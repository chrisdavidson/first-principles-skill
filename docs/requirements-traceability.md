# Requirements and Traceability

This file is the active canonical source of truth for requirements and traceability in this project; it supersedes the 26 scattered `milestones/vX.Y-REQUIREMENTS.md` files for all forward use (CANON-01).

## Status

**Coverage headline:** 121 reproducible / 85 audit-only / 0 gap / 206 total

The full 206-row capability-to-requirement-to-test mapping is in the generated matrix:
[`requirements-matrix.md`](requirements-matrix.md)

> **Honesty note (D-07):** A non-zero audit-only count is the expected honest success state.
> 85 requirements are validated by milestone audit without a re-runnable gate (audit-only);
> No current open gaps — GEN-01 → reproducible (Phase 93, committed v6.3 baseline; artifact `tests/step0-baseline-v6.3.md`) and GEN-02 → reproducible (runbook + wrapper; artifact `docs/live-monitoring-runbook.md`);
> 5 further requirements are confirmed by offline gates but remain honest live carry-forwards (RR-80-01, RR-79-01, RR-92-01 (supersedes RR-79-02), RR-92-02 (supersedes RR-79-03), RR-77-08).

## Active Surface

Exactly 7 live items. Nothing shipped or superseded belongs here.

1. **RR-79-01** [HIGH] — S-P01 pre-mortem carry-forward (Phase 79): no false-positive-safe marker cleared the D-08 evidence bar; "Bottom line" framing has zero technique markers. Confirmed by BATT-06 (RR-79-01 sentinel in `_battery_core.self_test_boundary()`); honest live carry-forward (not resolved).

2. **RR-92-01** [HIGH] — S-P02 inversion carry-forward (Phase 92, supersedes RR-79-02). Zero canonical inversion vocabulary in v6.3 (0/5 FAIL at Phase 92 re-baseline). Confirmed by BATT-06 (RR-92-01 sentinel in `_battery_core.self_test_boundary()`); honest live carry-forward (not resolved).

3. **RR-92-02** [HIGH] — S-P05 trade-off carry-forward (Phase 92, supersedes RR-79-03). 1/5 FAIL at Phase 92 re-baseline; the two-distinct-marker barrier is cleared by runs 2 and 3 in v6.3 evidence, but live MODE was 4/5 full-composer. Confirmed by BATT-06 (RR-92-02 sentinel in `_battery_core.self_test_boundary()`); honest live carry-forward (not resolved).

4. **RR-77-08** [MEDIUM] — CEILING=4 vs expected=3 warning: incidental `\bVerdict\b` IGNORECASE match in `composer_hits`; not a blocking defect but unresolved. Locked by BATT-06 anti-masking sentinel (CEILING=4) in `_battery_core.self_test_boundary()`.

5. **GEN-01** [reproducible] — Full Step 0 classifier rearchitecture (GEN-01-REARCH, Phases 91-93). GEN-01 is now reproducible: the Step 0 classifier capability is reproducibly measured by the committed v6.3 live re-baseline (Phase 92). Earned by the committed baseline, not a passing score (BATTERY: FAIL, 2/4 residuals carried — legitimate v6.3 success state). Artifact: `tests/step0-baseline-v6.3.md`. No longer an open gap.

6. **GEN-02** [reproducible] — Periodic live monitoring cadence; runbook + wrapper script established (Phase 89). Confirmed by git-tracked runbook and wrapper; artifact: `docs/live-monitoring-runbook.md`. No longer an open gap.

7. **RR-80-01** [CRITICAL] — Negative-control over-routing dip. CLOSED 4/5 at Phase 92 re-baseline (v6.3).
   **Lineage:** Formerly tracked as S-N04 (placeholder `RR-75-NN`). The dip was first recorded in Phase 80's live re-baseline run. Assigned the ID RR-80-01 in Phase 83 (D-05). See `tests/step0-baseline-v6.3.md` for the v6.3 re-baseline capture (CLOSED 4/5).
   Confirmed by STEP0-08 (S-N04 emulator assertion in `check-step0-emulator.py --self-test`) and BATT-06 (marker-counting assertion in `_battery_core.self_test_boundary()`); CLOSED at Phase 92 re-baseline (4/5 pass rate).

## Gap Findings

Summary of Phase 82 gap analysis. Full details in [`requirements-matrix.md`](requirements-matrix.md) (sections "Gap Findings (GAP-01)" and "Future-Milestone Candidate Work List (GAP-02)").

### GAP-01: Current gap picture

**No current open gaps.** Both previously-open gap rows are resolved:

- **GEN-01** → **reproducible** (Phase 93, GEN-01-REARCH Phases 91-93). Artifact: `tests/step0-baseline-v6.3.md`. The Step 0 classifier capability is now reproducibly measured by the committed v6.3 live re-baseline; earned by the committed baseline, not a passing score (BATTERY: FAIL, 2/4 residuals carried — legitimate v6.3 success state). Removed from the open-gap set.
- **GEN-02** → **reproducible** (runbook + wrapper script; Phase 89). Artifact: `docs/live-monitoring-runbook.md`. The periodic live monitoring cadence is now confirmed by a git-tracked runbook with re-runnable harness invocations; it is removed from the open-gap set.

**5 reproducible rows with confirming offline gates** (live behavior documented at Phase 92 re-baseline):

- **RR-80-01** [CRITICAL] — Negative-control over-routing; CLOSED 4/5 at Phase 92 re-baseline. Confirmed by STEP0-08 + BATT-06. Artifact: `scripts/_battery_core.py#self_test_boundary`.
- **RR-79-01** [HIGH] — S-P01 honest carry-forward; CLOSED 3/5 at Phase 92 re-baseline. Confirmed by BATT-06. Artifact: `scripts/_battery_core.py#self_test_boundary`.
- **RR-92-01** [HIGH] — S-P02 honest carry-forward (supersedes RR-79-02); CARRIED 0/5 at Phase 92 re-baseline. Confirmed by BATT-06. Artifact: `scripts/_battery_core.py#self_test_boundary`.
- **RR-92-02** [HIGH] — S-P05 honest carry-forward (supersedes RR-79-03); CARRIED 1/5 at Phase 92 re-baseline. Confirmed by BATT-06. Artifact: `scripts/_battery_core.py#self_test_boundary`.
- **RR-77-08** [MEDIUM] — CEILING=4 warning; locked by BATT-06 anti-masking sentinel (CEILING=4). Artifact: `scripts/_battery_core.py#self_test_boundary`.

**85 audit-only rows** — validated by milestone audit; no re-runnable gate exists. These represent genuine coverage but cannot be re-verified programmatically without new confirming tests.

### GAP-02: Candidate work list

Future-milestone candidates: add a confirming Test-Network or Methodology gate for each remaining audit-only row. Priority: MEDIUM audit-only items (85 rows). The 5 rows promoted in Phase 86 (RR-80-01, RR-79-01, RR-79-02/now-RR-92-01, RR-79-03/now-RR-92-02, RR-77-08) now have confirming offline gates and are no longer open candidates; closing the remaining live routing dips (RR-92-01, RR-92-02) is a future live-routing milestone. GEN-01 and GEN-02 are resolved (see GAP-01 above) and no longer appear in this work list.

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
