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

A BATTERY:FAIL is **not a blocker** if the failing rows are already documented as carry-forward
residuals in the prior baseline. The following residuals are known carry-forwards from
`tests/step0-baseline-v5.3.md` — **do not chase them**:

| Prompt ID | Expected MODE | v5.3 K/N | Status |
|-----------|--------------|----------|--------|
| S-P01 | focused-pre-mortem | 1/5 | Carry-forward — expected FAIL |
| S-P02 | focused-inversion | 0/5 | Carry-forward — expected FAIL |
| S-P05 | focused-trade-off | 0/5 | Carry-forward — expected FAIL |
| S-N04 | full-composer | 2/5 | Carry-forward — expected FAIL |

These residuals reflect genuine detection limits documented at the time of the v5.3 baseline.
A BATTERY:FAIL that matches this exact set of rows is **honesty-not-score** — the mechanism is
working correctly and honestly reporting its limits.

### BATTERY:FAIL — new regression (blocking)

A new failure is a row that was **PASS** in the prior baseline and is now **FAIL**. This indicates
a regression introduced since the last baseline run. Investigate before closing the milestone.

To detect a new regression: compare the current per-prompt K/N table against the prior baseline
file (`tests/step0-baseline-v5.3.md` or the most recent versioned file in `tests/`).

---

## Where to record results

Each cadence run records its honest K/N outcome **two ways** (D-05 dual-record procedure):

### (a) New versioned baseline file

Create a new `tests/step0-baseline-vN.md` file, where `N` = the active milestone label at the
time of the run (e.g., `v6.2` for milestone v6.2). Follow the existing header convention from
`tests/step0-baseline-v5.3.md` (Recorded, Script version, Core version, Fixture version, Agent
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
| (initial — no live run yet) | v6.2 | — | — | — | S-P01, S-P02, S-P05, S-N04 | [step0-baseline-v5.3.md](../tests/step0-baseline-v5.3.md) |

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
