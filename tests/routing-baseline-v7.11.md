# Routing Baseline — v7.11

**Recorded:** 2026-06-29 — initial run 16:32:48Z (165 invocations; monthly spend-cap truncated at N13), **resumed to completion** ending 22:36:24Z after budget reset (the 9 contaminated negatives N3/N13/N14–N20 re-measured; final captures **165/165 genuine, 0 spend-limit**)
**Script version:** `scripts/check-routing.py` (commit `e92fc7e`)
**Fixture version:** `tests/routing-catalog.md` (commit `c05f568`)
**Agent version:** `first-principles/agents/first-principles.md` at commit `9a795e2`
**Catalog:** `tests/routing-catalog.md`
**Run flags:** `--repeat 5 --min-pass 3` (thresholds P≥11/13, N≥18/20)
**Run cwd:** `/tmp` (out-of-repo — orchestrator-owned background run, Phase-78 pattern)
**Verdict:** BATTERY: FAIL — P 1/13, N 20/20
**Summary:** P **1/13** DELEGATE · N **20/20** NO-DELEGATE — a genuine DELEGATE-routing regression vs the v3.13 anchor (P 11/13); negatives unchanged. honesty-not-score (D-01): recorded as observed, never forced; any fix forward-committed.
**Milestone:** v7.11 Live Re-Measure — first live re-baseline of the main DELEGATE-boundary since v3.13 (2026-06-03), at the heavier `--repeat 5 --min-pass 3` gate (v3.13 used `--repeat 3`).

---

## Per-prompt results

| # | Expected | Runs | Matches | K/N | Verdict |
|---|----------|------|---------|-----|---------|
| P1 | DELEGATE | 5 | 0 | 0/5 | FAIL |
| P2 | DELEGATE | 5 | 0 | 0/5 | FAIL |
| P3 | DELEGATE | 5 | 0 | 0/5 | FAIL |
| P4 | DELEGATE | 5 | 5 | 5/5 | PASS |
| P5 | DELEGATE | 5 | 0 | 0/5 | FAIL |
| P6 | DELEGATE | 5 | 0 | 0/5 | FAIL |
| P7 | DELEGATE | 5 | 0 | 0/5 | FAIL |
| P8 | DELEGATE | 5 | 0 | 0/5 | FAIL |
| P9 | DELEGATE | 5 | 0 | 0/5 | FAIL |
| P10 | DELEGATE | 5 | 0 | 0/5 | FAIL |
| P11 | DELEGATE | 5 | 0 | 0/5 | FAIL |
| P12 | DELEGATE | 5 | 1 | 1/5 | FAIL |
| P13 | DELEGATE | 5 | 0 | 0/5 | FAIL |
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
BATTERY: FAIL
P: 1/13  N: 20/20

Per-prompt K/N (best-of-5, K=3):
  P1: 0/5 FAIL
  P2: 0/5 FAIL
  P3: 0/5 FAIL
  P4: 5/5 PASS
  P5: 0/5 FAIL
  P6: 0/5 FAIL
  P7: 0/5 FAIL
  P8: 0/5 FAIL
  P9: 0/5 FAIL
  P10: 0/5 FAIL
  P11: 0/5 FAIL
  P12: 1/5 FAIL
  P13: 0/5 FAIL
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

Orchestrator-owned background run from `/tmp` (Phase-78 live-run pattern, D-01 — not a worktree
subagent):

```
OUT=/tmp/check-routing-v7.11-20260629T163248Z
python3 scripts/check-routing.py \
  --catalog tests/routing-catalog.md \
  --plugin-dir first-principles \
  --repeat 5 --min-pass 3 \
  --out "$OUT"
```

Uncapped, no `--priority` (D-01). The initial run truncated at the monthly spend cap during the
N-prompts (onset at N13; N3/N13/N14–N20 returned spend-limit error captures). **Truncation recovery
(D-03):** the 38 spend-limit/error captures for the 9 affected negatives were deleted and the harness
re-run against the **same `--out`** after budget reset — `check-routing.py`'s implicit disk-aware
resume (`_is_prompt_complete`) re-scored the 24 already-genuine prompts from disk and re-measured only
the 9 deleted ones. Final state: **165/165 captures genuine, 0 spend-limit** — a complete honest
measurement, not a PARTIAL. The per-prompt table + aggregate block were assembled from
`$OUT/scores.tsv` + `$OUT/verdict.txt` by the throwaway helper `scratchpad/emit_routing_baselines.py`
(D-04 — no baseline emitter exists in the harness; the routing-emitter-absence guard is intentional).
Raw `.jsonl` are not committed (D-05).

---

## Methodology notes

- **`--repeat 5 --min-pass 3`** (best-of-5, K=3) — heavier than the v3.13 anchor's `--repeat 3`
  (best-of-3, K=2); K/N denominators are `/5`. A prompt PASSes iff ≥ 3 of 5 runs match the expected
  verdict.
- **DELEGATE classification (Signal A):** a `Task` tool_use whose `subagent_type` is
  `first-principles:first-principles`. NO-DELEGATE otherwise. Verified genuine (P4's captures carry 5
  real such delegations; P1's carry none).
- **Blocking human checkpoint (D-06):** the honest verdict was confirmed by a human before commit. No
  residual dispositions occur in this phase (RR-114-01 / S-P10 / S-P14 are all Step-0, Phase 129).
- **Priors byte-frozen:** the v3.13 anchor and all prior routing baselines are read-only; the firewall
  FROZEN-EVIDENCE gate (`bash scripts/check-firewall-battery.sh` → `FIREWALL: GREEN (15/15)`) was
  confirmed before and after this commit.

---

## Classification — vs the v3.13 anchor

**FAIL — a genuine DELEGATE-routing regression at the main orchestrator boundary.**

| Side | v7.11 (this run) | v3.13 anchor | Delta |
|------|------------------|--------------|-------|
| P (DELEGATE) | **1/13** | 11/13 | **−10 (regression)** |
| N (NO-DELEGATE) | **20/20** | 20/20 | none |
| Overall | **BATTERY: FAIL** | PASS | regression |

**The negatives are unchanged and genuine** — 20/20 NO-DELEGATE (the resume re-measured N14–N20 etc.
to genuine no-delegate behavior, not error captures). **The positives collapsed:** only **P4**
delegates to the `first-principles:first-principles` agent (5/5); P12 lands 1/5; the other eleven
P-prompts score **0/5**.

This is **not** a detector false-negative and **not** a truncation artifact (the P-prompts all ran
genuinely before any cap pressure, and were inspected directly). On the failing P-prompts the
orchestrator **answers the first-principles-style prompt inline itself** — a single-turn response
(`num_turns:1`, `stop_reason:end_turn`, no `Task` tool_use) that performs the ground-truths /
decomposition analysis directly — instead of auto-delegating to the registered agent. The most likely
cause is the substantially newer/more-capable orchestrator model running these `claude -p`
invocations (vs the 2026-06-03 v3.13 era): it is capable enough to satisfy the prompt directly and so
does not route to the sub-agent. The routing surface itself also changed substantially since v4.x
(8-technique Step 0, expanded negatives, output-contract headers, v7.8 guard column + tiebreaker).

**Disposition (honesty-not-score, D-01):** this `BATTERY: FAIL` is the true observed outcome and is
recorded as-is, never forced toward green. Per the v7.11 milestone's standing constraint, any routing
*fix* (e.g. strengthening the agent's auto-delegation triggers, or re-evaluating whether inline
first-principles analysis is acceptable) is **forward-committed to a future milestone** — a re-measure
*measures* the routing, it does not change it here. This is exactly the kind of divergence the live
re-baseline exists to surface.

---

## Coexistence note

`tests/routing-baseline-v3.13.md` (and all prior routing baselines) remain byte-identical — verified
by `git diff --quiet -- tests/routing-baseline-v3.13.md` and the firewall FROZEN-EVIDENCE gate.
