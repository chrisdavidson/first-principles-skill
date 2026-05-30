# Routing Baseline — v3.11 (P8 forward-monitoring closure; mini-catalog scope)

**Recorded:** 2026-05-30
**Script version:** `scripts/check-routing.py` (unchanged)
**Agent version:** `first-principles/agents/first-principles.md` including the v3.9 P8 trigger-phrase fix at commit `0d9c9f8` ("reason from the ground up" + "what do we actually know is true") — this is the fix being confirmed
**Catalog:** `tests/routing-mini-catalog-p8.md`
**Run flags:** `--repeat 5 --min-pass 3`
**Verdict:** P8 HELD at 3/5 PASS

---

> **SCOPE NOTE — P8-SCOPED MINI-CATALOG RUN (4 prompts: P8, N8, N9, N10)**
> This is NOT a full 27-prompt battery snapshot. This baseline covers only the P8 mini-catalog
> subset used to measure the v3.9 fix under the heavy `--repeat 5 --min-pass 3` gate.
> Do not compare per-prompt counts to full-battery baselines (v3.7, v3.8).
>
> **MON-03** (apply fix) and **MON-04** (verify fix) are **N/A — not triggered** because P8
> HELD at 3/5 means no fix was applied and no fix-verification is needed.

---

## Per-prompt results

| # | Expected | Runs | Matches | K/N | Verdict |
|---|----------|------|---------|-----|---------|
| P8 | DELEGATE | 5 | 3 | 3/5 | PASS |
| N8 | NO-DELEGATE | 5 | 5 | 5/5 | PASS |
| N9 | NO-DELEGATE | 5 | 5 | 5/5 | PASS |
| N10 | NO-DELEGATE | 5 | 5 | 5/5 | PASS |

---

## Per-run P8 actuals

| Run | Expected | Actual | Match |
|-----|----------|--------|-------|
| 1 | DELEGATE | DELEGATE | 1 |
| 2 | DELEGATE | DELEGATE | 1 |
| 3 | DELEGATE | NO-DELEGATE | 0 |
| 4 | DELEGATE | NO-DELEGATE | 0 |
| 5 | DELEGATE | DELEGATE | 1 |

Matches came from runs 1, 2, and 5.

---

## How this baseline was produced

```
python3 scripts/check-routing.py --catalog tests/routing-mini-catalog-p8.md --repeat 5 --min-pass 3 --out /tmp/p50-p8-battery
```

Output directory: `/tmp/p50-p8-battery` (transient).

---

## Interpretation note

The global `BATTERY: FAIL` line in `verdict.txt` reflects the script's default full-battery
thresholds (P >= 8/10, N >= 15/17). A 1P + 3N mini-catalog cannot satisfy those thresholds —
this is expected behavior for a scoped run and does NOT affect the per-prompt K/N verdict.
The relevant classification is the per-prompt block: **P8: 3/5 PASS**.

Raw verdict.txt (verbatim):

```
BATTERY: FAIL
P: 1/1  N: 3/3

Failed prompts:

Per-prompt K/N (best-of-5, K=3):
  P8: 3/5 PASS
  N8: 5/5 PASS
  N9: 5/5 PASS
  N10: 5/5 PASS
```

---

## Classification

**HELD** — P8 match_count 3/5 satisfies the >= 3 threshold. The v3.9 trigger-phrase fix
("reason from the ground up" + "what do we actually know is true") survives the heavy 5-run
gate at the minimum passing threshold.

N-side confirmation: N8, N9, N10 all scored 5/5 NO-DELEGATE — no N-side regression from
the v3.9 prompt rewrite.

---

## Forward-monitoring disposition

P8 monitoring obligation closed. The v3.9 trigger-phrase fix ("reason from the ground up" + "what do we actually know is true") survived the heavy 5-run gate at 3/5. The v3.11 baseline closes the P8 watch obligation inherited from v3.8. Future milestones resume standard battery cadence; no dedicated P8 mini-battery runs are required unless a new regression is detected in the full battery.
