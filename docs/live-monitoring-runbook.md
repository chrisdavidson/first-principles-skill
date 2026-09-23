# Live Monitoring Runbook

**Artifact type:** Operator runbook (GR-03 / GR-04)
**Date:** 2026-06-15
**Phase:** 89-gen-02-cadence-and-runbook
**Requirements:** GR-03, GR-04
**Status:** ACTIVE

---

## Purpose

This runbook covers periodic **live** monitoring of the Step 0 technique-selection harness
(`check-step0-live.py`) and the merged routing battery (`check-routing-battery.py`),
supplementing the offline CI gates that run automatically on every PR. It documents the
hybrid cadence, the exact re-runnable invocations, how to interpret PASS / FAIL /
honest-carry-forward verdicts, and where to record run results.

---

## When to run

Re-run the live harness on either of the following triggers (hybrid cadence, D-01):

**(a) At each milestone boundary** — both when opening a new milestone and when closing it.
A milestone boundary is the natural synchronization point for establishing a fresh honest
baseline before and after a batch of changes lands.

**(b) Whenever a change touches the Step-0 detector surface.** The three detector surfaces
that warrant a re-run are:

1. `scripts/check-step0-*.py` logic — any change to the phrase-detection or mode-classification
   code inside the live-harness scripts.
2. The `_battery_core.py` `_TECHNIQUE_CATEGORIES` markers — any addition, removal, or rename of
   canonical technique-category phrases.
3. The `**Phrase detection rules**` table in `shared/spine/SKILL-body.md` — any edit to the
   trigger-phrase rows the agent body uses for Step-0 branching.

**Rationale:** The live signal only moves meaningfully when detector logic or the phrase table
changes. A pure calendar cadence (e.g., weekly) would consume live `claude` invocations with no
signal change between runs, wasting budget and producing uninformative results.

---

## How to run

### Option A — wrapper (recommended)

```bash
bash scripts/run-live-monitoring.sh
```

This chains both canonical invocations in sequence (Step-0 live harness first, then routing battery).
See `scripts/run-live-monitoring.sh` for the full script.

### Option B — individual invocations

```bash
# Step-0 live harness (STEP0-06 domain) — 60 live claude invocations
python3 scripts/check-step0-live.py \
  --catalog tests/step0-fixture-catalog.md \
  --repeat 5 \
  --min-pass 3

# Routing battery (BATT-06 domain) — live
python3 scripts/check-routing-battery.py \
  --catalog tests/routing-battery-catalog.md \
  --repeat 5 \
  --min-pass 3
```

**Gate owners:**
- `check-step0-live.py` — STEP0-06 (offline `--self-test` is the CI gate; this manual run is the
  live supplemental measurement)
- `check-routing-battery.py` — BATT-06 (offline `--self-test` is the CI gate; this manual run is
  the live supplemental measurement)

**Cross-references:** See `CLAUDE.md` §"Step 0 measurement harness" and §"Routing battery" for
the full measurement comparison table and gate ownership details.

---

## What each invocation measures

| Script | Measured layer | Run mode |
|--------|---------------|----------|
| `check-step0-live.py` | Live Step 0 MODE classification — classifies each fixture prompt via the approach-② bypass channel (`--output-format stream-json --verbose`) and scores K-of-N results across the 12-row fixture catalog | Manual: `--repeat 5 --min-pass 3` (60 live `claude` invocations) |
| `check-routing-battery.py` | Merged dual-signal battery — boundary discipline (DELEGATE / NO-DELEGATE) AND focused-output signal (FU-21 gate, FOCUS-01) scored from the same stream; both-match per-prompt verdict | Manual: `--repeat 5 --min-pass 3` |

**Note:** The `--self-test` forms of both scripts (e.g., `check-step0-live.py --self-test`) are
different commands — they are offline, deterministic CI gates (STEP0-06, BATT-06) and do NOT
invoke `claude`. This runbook covers the supplemental live runs only.

---

## How to interpret results

### BATTERY:PASS

All K/N thresholds are met. No action required. Record the result per §"Where to record results".

### BATTERY:FAIL — carry-forward (expected, non-blocking)

A BATTERY:FAIL is **not a blocker** if the failing row is a documented live carry-forward. There
is exactly **one** such row. Residual ids supersede over time; the id below is current as of
2026-09-23 (chains per `docs/requirements-traceability.md` and `scripts/_battery_core.py`).

| Prompt ID | Expected MODE | Current residual | Last live K/N | Status |
|-----------|--------------|------------------|---------------|--------|
| S-P02 | focused-inversion | **RR-114-01** (chain: RR-79-02 → RR-92-01 → RR-95-01 → RR-108-01 → RR-114-01) | 0/5 at v8.5 (`tests/step0-baseline-v8.5.md`); 2/5 at v7.11; 1/5 at v7.13 | Carry-forward — expected FAIL, **[v8.0 ACCEPTED-FINAL]**. Do not chase. |

**S-P05 `focused-trade-off` is NOT a carry-forward, and a FAIL there IS blocking.** Its chain
(RR-79-03 → RR-92-02 → RR-95-02 → **RR-108-02**) **CLOSED** at 4/5 at the Phase 114 v7.6
re-baseline, and the close was **sustained at 5/5** at the Phase 129 v7.11 re-baseline. `RR-108-02`
is retained only as a regression guard, and no successor id was minted on the close. An S-P05 FAIL
is a regression from a clean sweep — investigate it.

> **Correction note, 2026-09-23 (backlog 999.158).** Through v9.8.0 this section listed S-P02 under
> the retired id `RR-95-01` and S-P05 under the retired id `RR-95-02`, presenting each row's v6.4
> K/N figure (1/5 and 2/5 respectively) as the current expectation. Both ids had been superseded —
> S-P02's chain ran on three more supersessions to RR-114-01, and S-P05's chain had *closed*. An
> operator following the old table would have excused an S-P05 regression from a clean 5/5 sweep as
> expected, which masks a regression instead of reporting one. The v6.4 figures remain correct as a
> record of v6.4; see `tests/step0-baseline-v6.4.md:177-180` for the original mints.

A carry-forward FAIL matching the single row above is **honesty-not-score** — the mechanism is
working correctly and honestly reporting its limits.

### BATTERY:FAIL — new regression (blocking)

A new failure is a row that was **PASS** in the prior baseline and is now **FAIL**. This indicates
a regression introduced since the last baseline run. Investigate before closing the milestone.

To detect a new regression: compare the current per-prompt K/N table against the prior baseline
file. As of 2026-09-23 that is **`tests/step0-baseline-v8.5.md`** — the version
`_BASELINE_VERSION` in `scripts/check-step0-live.py` pins. `tests/step0-baseline-v7.8.md` is the
last full-run baseline (6 prompts x 5) and is the better comparison when the current run covers
prompts v8.5 did not measure — except for S-P02 or S-P05: v7.8's run covered only
`S-P01 S-P03 S-N01 S-N02 S-N03 S-N04`, so it is not a usable comparison for either of those two
prompts.

---

## Where to record results

Each cadence run records its honest K/N outcome **two ways** (D-05 dual-record procedure):

### (a) New versioned baseline file

Create a new `tests/step0-baseline-vN.md` file, where `N` = the active milestone label at the
time of the run (e.g., `v6.2` for milestone v6.2). Follow the existing header convention from
`tests/step0-baseline-v6.4.md` (Recorded, Script version, Core version, Fixture version, Agent
version, Run flags, Run cwd, Baseline verdict, Summary — then the per-prompt results table).

Labeling rule: `tests/step0-baseline-v<milestone>.md` (e.g., `tests/step0-baseline-v6.2.md` for
the first cadence run under milestone v6.2).

**Note:** Phase 89 does NOT itself create a fresh baseline file. The next baseline
(`tests/step0-baseline-v6.2.md`) is created by the operator on the first cadence run.

### (b) Append one row to the rolling results table

Append a single row to the "Rolling results table" section (§"Rolling results table") in
`docs/live-monitoring-runbook.md` with the date, milestone, BATTERY verdict, S-P PASS count,
S-N PASS count, known carry-forward residuals, and a link to the new baseline file.

---

## Rolling results table

| Date | Milestone | BATTERY verdict | Step-0 S-P PASS | S-N PASS | Carry-forward residuals | Baseline file |
|------|-----------|----------------|-----------------|----------|------------------------|---------------|
| (initial — no live run yet) | v7.0 | — | — | — | S-P02, S-P05 | [step0-baseline-v6.4.md](../tests/step0-baseline-v6.4.md) |

> **Status note, 2026-09-23 (drift audit).** This table has never been filled in. The row above is
> the v7.0 placeholder it shipped with, and the cadence this runbook prescribes ("re-run at each
> milestone boundary") has **not** been executed through it since — the repository is at v9.8.0.
> The live Step-0 readings that *were* taken live elsewhere: `tests/step0-baseline-v7.8.md`
> (the last full run), `tests/step0-baseline-v8.5.md` (current pinned baseline), and the v9.6.0
> readings in `docs/v9.6-baseline-reading.md` / `docs/v9.6-rebaseline-reading.md`. Treat this
> table as aspirational, not as a record of runs that happened. The placeholder row's `S-P05`
> entry is NOT a current carry-forward: its chain closed at the Phase 114 v7.6 re-baseline (see
> § BATTERY:FAIL above).

---

## Offline gates

The following offline gates run automatically on every PR via `.github/workflows/validation.yml`
and do NOT require this runbook's manual procedure:

| Gate | Script | What it checks |
|------|--------|----------------|
| STEP0-06 | `python3 scripts/check-step0-live.py --self-test` | Offline Step 0 live-harness self-test — scoring/parsing logic (deterministic, no live session) |
| STEP0-08 | `python3 scripts/check-step0-emulator.py --self-test` | Offline phrase-detection classifier self-test (deterministic, no live session) |
| BATT-06 | `python3 scripts/check-routing-battery.py --self-test` | Offline battery core self-test — marker counting + sentinel assertions (deterministic) |
| TRACE-03 | `python3 scripts/check-traceability.py --self-test` | Traceability gate — owns the GEN-02-RUNBOOK sentinel (checks that this runbook and the wrapper script exist) |

This runbook covers the **supplemental live monitoring** that CI cannot perform — actual
`claude` invocations against the 12-row Step-0 fixture catalog and the routing battery catalog.
The offline gates confirm the harness logic is correct; the live runs confirm the agent body
behaves as expected in live sessions.
