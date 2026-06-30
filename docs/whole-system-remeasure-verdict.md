# Whole-System Live Re-Measure — v7.11 Verdict

**Milestone:** v7.11 Live Re-Measure of the Whole System (Phases 128–131)
**Recorded:** 2026-06-29
**Status:** Durable git-tracked verdict (RECON-01). Offline-only reconcile — no live `claude`
invocation, no detector change, no agent-body change.

> **No `git tag` is cut in this phase.** The annotated `v7.11` tag is the milestone-close
> deliverable, produced by `/gsd-complete-milestone` after Phase 131 verifies (D-01) — not a
> keystroke inside this phase. This phase stops at "surface reconciled + offline battery green."

---

## 1. Whole-system verdict: **SPLIT**

The v7.11 live re-measure ran three independent measurable layers. The honest whole-system
outcome is a **SPLIT — two layers FAIL, one layer PASS**. Per honesty-not-score (milestone D-01)
the SPLIT is the durable recorded outcome; **no layer was chased to green** and every fix surfaced
is forward-committed, not applied here.

| Layer | Verdict |
|-------|---------|
| Step 0 technique selection | **FAIL** (carried residuals — no new regression) |
| Main routing DELEGATE boundary | **FAIL** (genuine NEW regression — RR-130-01) |
| Merged dual-signal battery (boundary + focused output) | **PASS** (clean reproduction of v4.3) |

The two FAILs are different in kind: Step 0 fails on **previously-carried** residuals (nothing
new broke), while main routing fails on a **new** inline-answering regression first observed at
this re-baseline (RR-130-01, §4).

---

## 2. Per-layer results

| Layer | Baseline file | Verdict | Key metric |
|-------|---------------|---------|------------|
| Step 0 | `tests/step0-baseline-v7.11.md` | **BATTERY: FAIL** | P **4/8** canonical bar (S-P01/03/05/06 PASS; S-P02/04/10/14 FAIL); S-N 8/14 |
| Main routing | `tests/routing-baseline-v7.11.md` | **BATTERY: FAIL** | P **1/13** DELEGATE · N **20/20** NO-DELEGATE |
| Merged battery | `tests/routing-battery-baseline-v7.11.md` | **BATTERY: PASS** | boundary P 2/2 · N 2/2; focused P 4/4 · N 1/1 |

### Step 0 — canonical-bar per-row scores (8-technique bar)

| Row | Technique | v7.11 K/N | Verdict | RR ID |
|-----|-----------|-----------|---------|-------|
| S-P01 | pre-mortem | 5/5 | PASS | RR-79-01 (CLOSED, sustained) |
| S-P02 | inversion | 2/5 | **FAIL** | RR-114-01 (CARRIED) |
| S-P03 | fishbone | 4/5 | PASS | RR-117-01 (CLOSED, sustained) |
| S-P04 | five-whys | 2/5 | **FAIL** | RR-75-04 |
| S-P05 | trade-off | 5/5 | PASS | RR-108-02 (CLOSED, sustained) |
| S-P06 | second-order | 4/5 | PASS | — |
| S-P10 | estimate | 0/5 | **FAIL** | RR-108-04 (CARRIED) |
| S-P14 | theoretical-limit | 0/5 | **FAIL** | RR-108-05 (CARRIED) |

Bar = 4/8 PASS. S-N negatives scored 8/14 (not part of the pass bar; S-P16 merge-validation
signal 0/5 sits outside the /8 bar). S-P07/08/11/12/13/15 are context-free parser-robustness
falsifiers, excluded from the bar by design.

### Main routing — per-prompt collapse

Only **P4** delegated to the `first-principles:first-principles` agent (5/5). **P12** landed 1/5.
The other **eleven** P-prompts scored **0/5**. The N (NO-DELEGATE) side is unchanged at **20/20**.

### Merged battery — all rows clean

All 9 rows passed both gates: the two boundary P-prompts (B-P12, B-P24) and two boundary
negatives (B-N1, B-N2) routed to `none-or-other` 5/5; the four focused P-prompts (F-P12, F-P24,
F-P25, F-P26) produced their expected focused-technique output 5/5; the focused negative (F-N1)
produced no focused output 5/5.

---

## 3. Comparison vs prior anchor (per layer)

### Step 0 — vs `tests/step0-baseline-v7.8.md` (Phase 119 CONF-03)

| Metric | v7.11 | v7.8 anchor | Delta |
|--------|-------|-------------|-------|
| Verdict | **BATTERY: FAIL** | BATTERY: PASS | regression at verdict level |
| Scope | full 8-technique canonical bar (P 4/8) | targeted 6-row confirmation (S-P01 3/5, S-P03 4/5 PASS; S-N01/02/03/04 controls) | broader bar |
| S-P01 pre-mortem | 5/5 PASS | 3/5 PASS | +2 (sustained over floor) |
| S-P03 fishbone | 4/5 PASS | 4/5 PASS | none |
| Run flags | `--repeat 5 --min-pass 3` | `--repeat 5 --min-pass 3` | same |

The v7.8 anchor was a **targeted** 6-row confirmation of the Phase-118 over-routing prose fix; it
did not run S-P02/04/05/06/10/14. The v7.11 FAIL is driven by the broader-bar carried residuals
(S-P02/10/14) plus S-P04, not by a regression of the rows v7.8 did measure — S-P01 and S-P03 both
held at or above their v7.8 values.

### Main routing — vs `tests/routing-baseline-v3.13.md` (2026-06-03)

| Side | v7.11 | v3.13 anchor | Delta |
|------|-------|--------------|-------|
| P (DELEGATE) | **1/13** | 11/13 | **−10 (regression)** |
| N (NO-DELEGATE) | **20/20** | 20/20 | none |
| Overall | **BATTERY: FAIL** | BATTERY: PASS | regression |
| Run flags | `--repeat 5 --min-pass 3` | `--repeat 3 --min-pass 2` | heavier gate in v7.11 |

This is the first live re-baseline of the main DELEGATE boundary since v3.13, at a heavier gate.
The negatives are unchanged and genuine; the positives collapsed (see §4).

### Merged battery — vs `tests/routing-battery-baseline-v4.3.md` (2026-06-11)

| Signal | v7.11 | v4.3 anchor | Delta |
|--------|-------|-------------|-------|
| Boundary | P 2/2 · N 2/2 PASS | P 2/2 · N 2/2 PASS | none |
| Focused output | P 4/4 · N 1/1 PASS | P 4/4 · N 1/1 PASS | none |
| Overall (both-match) | **BATTERY: PASS** | BATTERY: PASS | none |
| Row strength | all 9 rows 5/5 on active signal | F-P12 was 4/5 | slightly stronger |

Despite substantial routing-surface change since v4.x (8-technique Step 0, expanded negative
catalog, output-contract headers, the v7.8 guard column + stay-in-composer tiebreaker), the merged
battery reproduces the v4.3 anchor at verdict level and is marginally stronger per-row.

---

## 4. RR-130-01 — main-routing inline-answering regression (NEW, D-02)

The main-routing FAIL (P 1/13) is a **genuine new regression**, not a detector false-negative and
not a truncation artifact (the P-prompts all ran genuinely before any cap pressure and were
inspected directly). It is minted as **`RR-130-01`** (the `RR-<phase>-NN` convention; the Phase-130
slot was free — Phase 129 minted no RR-129-NN).

**Root cause (quoted verbatim from `tests/routing-baseline-v7.11.md`):**

> On the failing P-prompts the orchestrator **answers the first-principles-style prompt inline
> itself** — a single-turn response (`num_turns:1`, `stop_reason:end_turn`, no `Task` tool_use)
> that performs the ground-truths / decomposition analysis directly — instead of auto-delegating
> to the registered agent. The most likely cause is the substantially newer/more-capable
> orchestrator model running these `claude -p` invocations (vs the 2026-06-03 v3.13 era): it is
> capable enough to satisfy the prompt directly and so does not route to the sub-agent.

**Disposition:** fix **applied at Phase 133** (imperative `description:` rewrite of
`shared/spine/SKILL.meta.yml`, regenerated at zero drift, full offline battery green — STRENGTHEN
verdict per `docs/rr-130-01-diagnosis.md`). Residual **OPEN** — no resolution tier claimed; the
authoritative live P re-measure is forward-committed (§7). ID kept (RR-130-01; D-02 / D-04
precedent). Per the v7.9 D-02 "documented residual with no matrix row" precedent it is recorded as
prose in `docs/requirements-traceability.md` (active surface) and `.planning/REQUIREMENTS.md`
Future Requirements, without a `gap`-tier matrix row.

---

## 5. Step-0 carried-residual dispositions

The three long-deferred Step-0 residuals were measured against the v7.11 run and **carried** at
their honest observed K/N (each below the 3/5 min-pass bar). Per D-09 (CLOSE/CARRY keeps the
existing RR ID) **no RR-129-NN successor is minted** — the existing IDs are kept. These are
honest failing vectors, recorded as-measured.

| Prompt | Technique | v7.11 K/N | Disposition | RR ID (kept) |
|--------|-----------|-----------|-------------|--------------|
| S-P02 | inversion | 2/5 FAIL | CARRIED (2/5 < 3/5) | RR-114-01 |
| S-P10 | estimate | 0/5 FAIL | CARRIED (0/5 < 3/5) | RR-108-04 |
| S-P14 | theoretical-limit | 0/5 FAIL | CARRIED (0/5 < 3/5) | RR-108-05 |

- **RR-114-01 (S-P02 inversion):** v7.6 live 1/5 → v7.11 live **2/5**. RESOLVED-STRUCTURALLY-OFFLINE
  at Phase 121 OCH-02 (inversion detector extended to 13 markers); the live pass-rate re-measure
  this run still lands below bar. CARRIED.
- **RR-108-04 (S-P10 estimate):** v7.6 was spend-limit-indeterminate → v7.11 live **0/5** (all five
  runs routed `full-composer`). First genuine live measurement; CARRIED.
- **RR-108-05 (S-P14 theoretical-limit):** v7.6 was spend-limit-indeterminate → v7.11 live **0/5**
  (all five runs routed `full-composer`). First genuine live measurement; CARRIED.

S-P04 (RR-75-04, 2/5) and the S-P16 merge-validation signal (0/5, outside the /8 bar) appear in
the full per-prompt table of `tests/step0-baseline-v7.11.md`; they are not the milestone's named
carried residuals and need no dedicated disposition here.

The BATT-06 honest-state sentinels for these three residuals are re-pointed to the frozen v7.11
vectors in Phase 131 Plan 02 (RECON-02) — each asserts its **honest (failing) vector**, never a
forced pass.

---

## 6. Spend / truncation caveats

All three layers were measured under the monthly spend cap (org overage disabled). Two of the
three runs hit the cap mid-run and were recovered to a complete honest measurement; none shipped
as a PARTIAL.

| Layer | Live invocations | Truncation | Recovery |
|-------|------------------|------------|----------|
| Step 0 (Phase 129, STEP0L) | 145 (29 prompts × 5) | monthly-spend-limit truncation in runs 1–2 | 3-run best-genuine merge (run1 + run2 + run3 rerun), per D-02 resume-to-complete |
| Main routing (Phase 130, ROUTEL-01) | 165 (33 prompts × 5) | monthly spend-cap truncated at N13 (9 negatives N3/N13/N14–N20 contaminated) | deleted the 38 spend-limit/error captures, re-ran same `--out` after budget reset; implicit disk-aware resume re-measured only the 9 deleted prompts → final **165/165 genuine, 0 spend-limit** |
| Merged battery (Phase 130, ROUTEL-02) | 45 (9 prompts × 5) | none — clean run | n/a (0 spend-limit, 0 `is_error`) |

The Step 0 and main-routing FAIL verdicts are **not** truncation artifacts: the Step 0 carried
rows and the main-routing P-prompts were all measured on genuine (non-error) captures, and the
final capture sets are fully genuine after recovery.

---

## 7. Forward commitments

Per the v7.11 milestone's standing constraint (measure + record + reconcile; never change the
measured surface), every fix surfaced by this re-measure was forward-committed to a future
milestone; none was applied in Phase 131. One commitment — **RR-130-01** — was subsequently
fulfilled by an offline fix at Phase 133 (see below); the remaining three stay live.

- **RR-130-01** (main-routing inline-answering regression) — offline fix applied at Phase 133
  (imperative `description:` rewrite; STRENGTHEN verdict). Authoritative **live P re-measure**
  forward-committed to a future measurement milestone (gated on fresh `claude` budget; honesty-
  not-score, D-01: no live pass-rate claimed without a live run).
- **RR-114-01** (S-P02 inversion) — inversion live re-measure on its gated future milestone.
- **RR-108-04** (S-P10 estimate) — gated on **ESTPART-01** (estimate merge-partner scoping).
- **RR-108-05** (S-P14 theoretical-limit) — gated on **TLINV-01** (theoretical-limit ↔ inversion
  merge), now informed by the clean v7.11 0/5 measurement.

The annotated **`v7.11` git tag** is itself a forward (milestone-close) deliverable — cut by
`/gsd-complete-milestone`, not in this phase (D-01).

---

## Source baselines

- `tests/step0-baseline-v7.11.md` — Step 0 honest baseline (FAIL, P 4/8); anchor `tests/step0-baseline-v7.8.md` (PASS).
- `tests/routing-baseline-v7.11.md` — main-routing honest baseline (FAIL, P 1/13 / N 20/20); anchor `tests/routing-baseline-v3.13.md` (PASS, P 11/13 / N 20/20).
- `tests/routing-battery-baseline-v7.11.md` — merged-battery honest baseline (PASS); anchor `tests/routing-battery-baseline-v4.3.md` (PASS).
