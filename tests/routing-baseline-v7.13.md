# Routing Baseline — v7.13

**Recorded:** 2026-07-01 — orchestrator-owned background run from `/tmp` (Phase-78 pattern). The run hit the monthly spend cap twice; each time the OUTDIR was preserved, only the `api_error_status:429` spend-limit error-stub captures were deleted (identified and confirmed by their error signature — **not** by a naive `grep 'spend'`, which would have destroyed genuine transcripts that merely mention the word), and the same `--out` was resumed. `--priority positives` front-loaded the 13 P-cases so the recovery signal was measured first, before either truncation. Final captures **165/165 genuine, 0 spend-limit** (independently cross-checked).
**Script version:** `scripts/check-routing.py` (commit `b32bc33`)
**Fixture version:** `tests/routing-catalog.md` (commit `c05f568`)
**Agent version:** `first-principles/agents/first-principles.md` at commit `ef22988`
**Catalog:** `tests/routing-catalog.md`
**Run flags:** `--repeat 5 --min-pass 3 --priority positives` (thresholds P≥11/13, N≥18/20)
**Run cwd:** `/tmp` (out-of-repo — orchestrator-owned background run, Phase-78 pattern)
**Verdict:** BATTERY: PASS — P 11/13, N 20/20
**Summary:** P **11/13** DELEGATE · N **20/20** NO-DELEGATE — a full recovery from the v7.11 floor (P 1/13), matching the v3.13 anchor (P 11/13). The P133 imperative-hardening fix (agent `ef22988`) is confirmed live. honesty-not-score (D-01): recorded as observed, never forced.
**Milestone:** v7.13 Live Re-Measure — first LIVE measurement of the P133 imperative-hardening fix for RR-130-01, at the `--repeat 5 --min-pass 3` gate, vs the v3.13 anchor (P 11/13) and the v7.11 floor (P 1/13).

---

## Per-prompt results

| # | Expected | Runs | Matches | K/N | Verdict |
|---|----------|------|---------|-----|---------|
| P1 | DELEGATE | 5 | 5 | 5/5 | PASS |
| P2 | DELEGATE | 5 | 4 | 4/5 | PASS |
| P3 | DELEGATE | 5 | 4 | 4/5 | PASS |
| P4 | DELEGATE | 5 | 5 | 5/5 | PASS |
| P5 | DELEGATE | 5 | 5 | 5/5 | PASS |
| P6 | DELEGATE | 5 | 5 | 5/5 | PASS |
| P7 | DELEGATE | 5 | 5 | 5/5 | PASS |
| P8 | DELEGATE | 5 | 4 | 4/5 | PASS |
| P9 | DELEGATE | 5 | 2 | 2/5 | FAIL |
| P10 | DELEGATE | 5 | 3 | 3/5 | PASS |
| P11 | DELEGATE | 5 | 5 | 5/5 | PASS |
| P12 | DELEGATE | 5 | 5 | 5/5 | PASS |
| P13 | DELEGATE | 5 | 2 | 2/5 | FAIL |
| N1 | NO-DELEGATE | 5 | 5 | 5/5 | PASS |
| N2 | NO-DELEGATE | 5 | 5 | 5/5 | PASS |
| N3 | NO-DELEGATE | 5 | 5 | 5/5 | PASS |
| N4 | NO-DELEGATE | 5 | 5 | 5/5 | PASS |
| N5 | NO-DELEGATE | 5 | 5 | 5/5 | PASS |
| N6 | NO-DELEGATE | 5 | 5 | 5/5 | PASS |
| N7 | NO-DELEGATE | 5 | 5 | 5/5 | PASS |
| N8 | NO-DELEGATE | 5 | 5 | 5/5 | PASS |
| N9 | NO-DELEGATE | 5 | 5 | 5/5 | PASS |
| N10 | NO-DELEGATE | 5 | 5 | 5/5 | PASS |
| N11 | NO-DELEGATE | 5 | 5 | 5/5 | PASS |
| N12 | NO-DELEGATE | 5 | 5 | 5/5 | PASS |
| N13 | NO-DELEGATE | 5 | 5 | 5/5 | PASS |
| N14 | NO-DELEGATE | 5 | 5 | 5/5 | PASS |
| N15 | NO-DELEGATE | 5 | 5 | 5/5 | PASS |
| N16 | NO-DELEGATE | 5 | 5 | 5/5 | PASS |
| N17 | NO-DELEGATE | 5 | 5 | 5/5 | PASS |
| N18 | NO-DELEGATE | 5 | 5 | 5/5 | PASS |
| N19 | NO-DELEGATE | 5 | 5 | 5/5 | PASS |
| N20 | NO-DELEGATE | 5 | 5 | 5/5 | PASS |

---

## Aggregate verdict

```
BATTERY: PASS
P: 11/13  N: 20/20

Per-prompt K/N (best-of-5, K=3):
  P1: 5/5 PASS
  P2: 4/5 PASS
  P3: 4/5 PASS
  P4: 5/5 PASS
  P5: 5/5 PASS
  P6: 5/5 PASS
  P7: 5/5 PASS
  P8: 4/5 PASS
  P9: 2/5 FAIL
  P10: 3/5 PASS
  P11: 5/5 PASS
  P12: 5/5 PASS
  P13: 2/5 FAIL
  N1: 5/5 PASS
  N2: 5/5 PASS
  N3: 5/5 PASS
  N4: 5/5 PASS
  N5: 5/5 PASS
  N6: 5/5 PASS
  N7: 5/5 PASS
  N8: 5/5 PASS
  N9: 5/5 PASS
  N10: 5/5 PASS
  N11: 5/5 PASS
  N12: 5/5 PASS
  N13: 5/5 PASS
  N14: 5/5 PASS
  N15: 5/5 PASS
  N16: 5/5 PASS
  N17: 5/5 PASS
  N18: 5/5 PASS
  N19: 5/5 PASS
  N20: 5/5 PASS
```

---

## How this baseline was produced

Orchestrator-owned background run from `/tmp` (Phase-78 live-run pattern, D-05 — not a worktree
subagent):

```
MAIN_OUT=/tmp/check-routing-v7.13-20260701T115444Z
cd /tmp && python3 scripts/check-routing.py \
  --catalog tests/routing-catalog.md \
  --plugin-dir first-principles \
  --repeat 5 --min-pass 3 \
  --priority positives \
  --out "$MAIN_OUT"
```

**Cap-defensive truncation recovery (D-05).** The monthly spend cap truncated the run **twice**. Each
time the recovery discipline was: (1) PRESERVE `$MAIN_OUT` — never delete the directory; (2) identify
the spend-limit error-stub captures and **confirm their `api_error_status:429` error signature by
inspection** before deleting anything (a naive `grep 'spend'` would have matched — and destroyed —
genuine transcripts that merely contain the word); (3) DELETE only the confirmed error-stub captures;
(4) RESUME the same `--out`, whereupon `check-routing.py` re-scored the already-genuine prompts from
disk and re-ran only the deleted ones. `--priority positives` front-loaded all 13 P-cases ahead of the
20 N-cases, so both truncations sacrificed only already-stable / not-yet-critical negatives — never the
P recovery signal, which was measured first. Final state: **165/165 captures genuine, 0 spend-limit** —
a complete honest measurement, not a PARTIAL. The per-prompt table + aggregate block were assembled
from `$MAIN_OUT/scores.tsv` + `$MAIN_OUT/verdict.txt` by the throwaway helper
`scratchpad/emit_routing_baselines.py` (D-06 — no baseline emitter exists in the harness; the
routing-emitter-absence guard is intentional). Raw `.jsonl` are not committed (T-136-05).

---

## Methodology notes

- **`--repeat 5 --min-pass 3`** (best-of-5, K=3) — same heavier gate as the v7.11 floor; K/N
  denominators are `/5` (not the v3.13 anchor's `/3`, which used `--repeat 3`). A prompt PASSes iff
  ≥ 3 of 5 runs match the expected verdict.
- **`--priority positives`** (RMEASURE-01, added Plan 01) — front-loads all 13 P-cases before the 20
  N-cases so a spend-cap truncation sacrifices only stable negatives, never the P recovery signal. The
  flag is measurement-order only; it does not change any per-prompt verdict.
- **DELEGATE classification (Signal A):** a `Task` tool_use whose `subagent_type` is
  `first-principles:first-principles`. NO-DELEGATE otherwise. Verified genuine.
- **Blocking human checkpoint (D-04):** the honest verdict was confirmed by a human before commit; the
  RR-130-01 tier was read straight off the disposition block below.
- **Priors byte-frozen:** the v3.13 anchor, the v7.11 floor, and all prior routing baselines are
  read-only; the firewall FROZEN-EVIDENCE gate (`bash scripts/check-firewall-battery.sh` →
  `FIREWALL: GREEN (15/15)`) was confirmed before and after this commit.

---

## Classification — vs the v3.13 anchor

**PASS — a full recovery of the DELEGATE-routing boundary, matching the v3.13 anchor.**

| Side | v7.13 (this run) | v3.13 anchor | v7.11 floor | Delta vs anchor | Delta vs floor |
|------|------------------|--------------|-------------|-----------------|----------------|
| P (DELEGATE) | **11/13** | 11/13 | 1/13 | **matched (±0)** | **+10 (recovery)** |
| N (NO-DELEGATE) | **20/20** | 20/20 | 20/20 | none | none |
| Overall | **BATTERY: PASS** | PASS | FAIL | matched | recovered |

At v7.11 the positives had collapsed to **1/13** — the orchestrator answered the first-principles-style
prompts inline instead of auto-delegating to the registered sub-agent. The Phase-133 imperative
rewrite of the agent's routing surface (FIX-01, agent commit `ef22988`) was the fix, forward-committed
from v7.11 and **not tuned in this milestone**. This run is the first LIVE measurement of that fix: P
recovers to **11/13**, exactly matching the v3.13 anchor and **+10** over the v7.11 floor. Eleven of
thirteen P-prompts now delegate at ≥ 3/5; the two below-threshold prompts are **P9 (2/5)** and **P13
(2/5)** — the same boundary-noise band the v3.13 anchor tolerated (it also carried two P-prompts at the
2/3 minimum). The negatives are unchanged and genuine at **20/20 NO-DELEGATE**.

This is the "recovered" outcome the live re-measure exists to surface. Per honesty-not-score (D-01),
the observed P 11/13 is recorded verbatim; no run was re-rolled or extended to nudge P across a tier
boundary.

---

## Coexistence note

`tests/routing-baseline-v3.13.md`, `tests/routing-baseline-v7.11.md`, and all prior routing baselines
remain byte-identical — verified by
`git diff --quiet -- tests/routing-baseline-v3.13.md tests/routing-baseline-v7.11.md` and the firewall
FROZEN-EVIDENCE gate.

---

## RR-130-01 Disposition

Measured: P 11/13, N 20/20 | Anchor (v3.13): 11/13 | Floor (v7.11): 1/13 | Partial band: >= 7/13 | -> Tier: RESOLVE

Tier ladder (D-04): P >= 11/13 -> RESOLVE (CLOSE, ID kept as sentinel); 7/13 <= P < 11/13 -> PARTIAL (OPEN, partial-recovery, no re-diagnosis); P < 7/13 -> OPEN+re-diagnosis (forward-commit named re-diagnosis milestone).

**Disposition rationale:** Measured P 11/13 lands on the RESOLVE rung (P ≥ 11/13), matching the v3.13
anchor exactly and recovering +10 over the v7.11 floor. **RR-130-01 → RESOLVED / CLOSE**; the ID is
kept as a regression sentinel so any future drift back toward the inline-answering floor is caught. The
Phase-133 imperative-hardening fix (agent `ef22988`) is confirmed live — this is the "recovered" path,
so **no re-diagnosis milestone is forward-committed** (that is only the P < 7/13 rung). honesty-not-score
(D-01/D-04b): the observed P 11/13 is recorded verbatim, never forced. **D-04a deviation:** D-04 inserts
a PARTIAL middle rung (7/13 ≤ P < 11/13 → OPEN, partial-recovery) that deliberately refines RMEASURE-02's
original binary recovered/not-recovered wording into a three-tier ladder; here the refinement does not
change the outcome (P = 11 is the RESOLVE rung, not the PARTIAL band), but the ladder itself is the
recorded deviation and is auditable in this committed block and in the phase VERIFICATION.md.
