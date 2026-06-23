# Merge Validation Verdict — v7.6

**Artifact type:** Decision / verdict record
**Date:** 2026-06-23
**Phase:** 115-verdict-artifact-traceability-reconciliation (Plan 01)
**Requirement:** VERDICT-01
**Status:** DECIDED

---

## Decision

The v7.6 live 8-technique Step 0 re-baseline (Phase 114, 55/110 live `claude` invocations
measured before spend-limit cutoff, `tests/step0-baseline-v7.6.md`) returns **REGRESSION
(human-confirmed at the blocking checkpoint)**.

**The question this milestone answered:** The v7.5 milestone shipped the
decompose→five-whys merge on offline-only evidence and left UNVERIFIED whether it improved
five-whys routing. The Phase 114 live re-baseline measured it. The measured answer is
REGRESSION.

**Two combining signals:**

(1) **Merge-validation: S-P16 routed 0/5 to the full composer.** All five runs dispatched
`first-principles:first-principles` (the full-composer path). The v7.4 decompose anchor
(S-P09) was 0/5. **S-P16 = 0/5 is NOT > 0/5** — the v7.5 merge did **not** improve
five-whys routing on the merge-validation prompt. The "decompose this claim…" phrasing
still routes to the full composer exactly as the standalone decompose technique did
pre-merge. Five-whys *itself* still fires (S-P04 3/5) — it is the "decompose" phrasing
that does not trigger focused mode.

(2) **Genuine canonical rows fell below their v7.4 floors.** S-P01 pre-mortem 3/5→2/5 and
S-P03 fishbone 3/5→1/5 are now both below min-pass (genuine REGRESSIONS from v7.4 PASS).
S-P04 five-whys 4/5→3/5 and S-P06 second-order 5/5→4/5 dipped but still pass. S-P05
trade-off is the lone improver (2/5→4/5, ▲ +2, closing RR-108-02). Per the pre-registered
D-02 rule ("any canonical row below its v7.4 K/N → regression"), the human recorded this
as a REGRESSION finding with a forward-committed fix.

**Spend-limit caveat (D-01 honesty — read immediately):** The run was a **PARTIAL**,
truncated at the monthly spend limit after **55/110 calls (the first 11 prompts × 5
repeats)**. The `--priority` front-load landed the S-P04/S-P16 core in the genuine
measurement zone before the cutoff, so the milestone's core question is answered on
**genuine evidence**. However: **S-P10 (estimate) and S-P14 (theoretical-limit) were
spend-limit-truncated this run** (all 5 runs returned `none` / API-429). Their 0/5 cells
are **INDETERMINATE artifacts — NOT clean misroutes and NOT "held steady."** Never read
S-P10 or S-P14's 0/5 in this run as a confirmed routing failure.

---

## Evidence (falsifiable)

All K/N figures below are cloned verbatim from the source baseline and are checkable
directly against [`../tests/step0-baseline-v7.6.md`](../tests/step0-baseline-v7.6.md).
No figure is re-derived or transposed.

### 8-canonical per-technique vs-floor table

| # | Technique | Row | v7.4 floor | **v7.6** | vs floor |
|---|-----------|-----|:---:|:---:|:---:|
| 1 | pre-mortem | S-P01 | 3/5 | **2/5 FAIL** | ▼ −1 (regression) |
| 2 | inversion | S-P02 | 1/5 | **1/5 FAIL** | = holds |
| 3 | fishbone | S-P03 | 3/5 | **1/5 FAIL** | ▼ −2 (regression) |
| 4 | five-whys | S-P04 | 4/5 | **3/5 PASS** | ▼ −1 (still passes) |
| 5 | trade-off | S-P05 | 2/5 | **4/5 PASS** | ▲ +2 (improved) |
| 6 | second-order | S-P06 | 5/5 | **4/5 PASS** | ▼ −1 (still passes) |
| 7 | estimate | S-P10 | 0/5 *(contaminated)* | **— truncated** | indeterminate |
| 8 | theoretical-limit | S-P14 | 0/5 *(contaminated)* | **— truncated** | indeterminate |

**Tally: P 3/8** (6 genuinely measured, 2 spend-limit-truncated/indeterminate).

**Merge-validation (S-P16, outside the /8 bar): 0/5 — genuinely measured.** All five
runs routed to the full composer. The v7.4 decompose anchor (S-P09) was 0/5. S-P16 = 0/5
is NOT > 0/5, confirming the merge did not improve five-whys routing on the
"decompose this claim…" phrasing.

### Spend-limit caveat (per-row clean-vs-indeterminate status)

Consistent with honesty-not-score (D-01), the spend-limit contamination is recorded
verbatim and NOT masked:

- **Genuinely measured (11 prompts, 55 calls):** S-P04, S-P16, S-P01, S-P02, S-P03,
  S-P05, S-P06, S-N01, S-N02, S-N03, S-N04 — real agent transcripts; their K/N cells
  above are true measurements.
- **Spend-limit-truncated / INDETERMINATE:** S-P07, S-P08, S-P10, S-P11, S-P12, S-P13,
  S-N06, S-P14, S-P15, S-N07, S-N08 — uniform API-429 captures classified `none`.
  Their 0/5 cells are truncation artifacts, not genuine routing measurements.
- Of the canonical rows, **S-P10 (estimate) and S-P14 (theoretical-limit)** are
  carried-indeterminate (RR-108-04 / RR-108-05 kept; no fresh RR-114 mint — there is no
  clean K/N to supersede with). Do NOT read their 0/5 as confirmed under-routing.

**Negative-control discipline (measured zone):** S-N01 4/5, S-N02 4/5, S-N03 5/5,
S-N04 3/5 → **4/4 measured N-rows PASS** (the honest measured result). S-N06/07/08
were truncated (indeterminate, not genuine 0/5). The raw emitter header "S-N 4/7"
counts truncated rows as failing; the honest measured result is 4/4.

All figures are checkable against `../tests/step0-baseline-v7.6.md`.

---

## Rationale

**The merge's central routing claim is refuted.** The v7.5 merge's structural rationale
— stated in `docs/decompose-five-whys-merge.md`: "merging overlapping techniques reduces
the trigger target count and concentrates routing signal onto the remaining technique" —
is refuted for the routing-improvement question. The "decompose this claim…" prompt
still routes to the full composer post-merge (S-P16 0/5) exactly as it did pre-merge
(decompose S-P09 0/5). The merge consolidated the surface without improving the routing
that activates focused mode.

This finding is consistent with the v7.4 "capability breadth ≠ result breadth" finding
one milestone earlier: expanding (or consolidating) the technique surface changes what
the agent *can* do, but does not by itself change the routing that activates focused
mode. The Step 0 trigger mechanism — not the capability structure — remains the binding
constraint.

**Two original techniques regressed below their v7.4 floors** — S-P01 pre-mortem
(3/5→2/5) and S-P03 fishbone (3/5→1/5) are new regressions from v7.4 PASS, both now
below min-pass. These regressions are a genuine finding and motivate the
forward-committed fix in the next section. Five-whys itself (S-P04 3/5) holds above
min-pass, as does trade-off (S-P05 4/5, the lone improver) and second-order (S-P06 4/5).
Inversion (S-P02 1/5) carries forward unchanged from its v7.4 floor.

---

## Forward-Committed Fix

The two genuine regressions found at the v7.6 re-baseline are the **forward-committed
fix** this verdict names. The FIX is **DEFERRED** to a follow-up milestone per the
milestone's measure+decide+defer shape. Phase 115 RECORDS the regression and COMMITS the
fix forward; it does NOT fix routing (no `shared/` edit, no agent-body change, no
detector change in Phase 115).

**Regressed techniques (the forward-committed fix target):**

- **S-P01 pre-mortem — 2/5 (down from v7.4 floor 3/5, ▼ −1, below min-pass):** Tracked
  in the v7.6 baseline against the prior/legacy anchor RR-79-01. The v7.6 run records
  five modes: `['full-composer', 'focused-pre-mortem', 'full-composer',
  'focused-pre-mortem', 'full-composer']`. This is a genuinely measured regression on
  real transcripts.

- **S-P03 fishbone — 1/5 (down from v7.4 floor 3/5, ▼ −2, below min-pass):** Tracked in
  the v7.6 baseline against the prior/legacy anchor RR-75-03. The v7.6 run records five
  modes: `['full-composer', 'full-composer', 'focused-fishbone', 'full-composer',
  'full-composer']`. Also a genuinely measured regression on real transcripts.

Do NOT mint new RR IDs for S-P01 or S-P03 in this artifact — the traceability-ledger
reconciliation (including full RR-ID chain updates) is Plan 02 scope.

**Residual carry-forward summary for this milestone:**

| Residual | Technique | K/N | Status |
|----------|-----------|-----|--------|
| RR-114-01 | S-P02 inversion (supersedes RR-108-01) | 1/5 | CARRIED — genuinely measured, < min-pass; chain RR-79-02 → RR-92-01 → RR-95-01 → RR-108-01 → RR-114-01 |
| RR-108-02 | S-P05 trade-off | 4/5 | **CLOSED** at 4/5 ≥ min-pass (▲ +2 improvement) |
| RR-108-04 | S-P10 estimate | 0/5 | CARRIED-INDETERMINATE — spend-limit-truncated, NOT a clean measurement; no fresh K/N |
| RR-108-05 | S-P14 theoretical-limit | 0/5 | CARRIED-INDETERMINATE — spend-limit-truncated, NOT a clean measurement; no fresh K/N |

RR-114-01 and RR-108-02 CLOSED were minted / resolved in Phase 114 — they are referenced
here, not re-defined.

---

## Honesty-not-score Acknowledgement

**REGRESSION + BATTERY: FAIL + PARTIAL RUN** is the legitimate committed outcome of Phase
114 and of this verdict. No K/N number was softened, chased to a forced PASS, or masked.

- The BATTERY: FAIL result (P 3/8) was committed verbatim from the single authoritative
  live run. It was not re-run to improve the score (one authoritative baseline per
  milestone, D-01/D-03).
- The partial run (55/110 calls) is the honest deliverable — the `--priority` front-load
  guaranteed the S-P04/S-P16 merge-validation core landed first, so the milestone's core
  question is answered on genuine evidence even though the run was truncated.
- The spend-limit-truncated rows (S-P10 estimate, S-P14 theoretical-limit) are recorded
  `none` verbatim and labelled INDETERMINATE — never masked, never called clean misroutes,
  never described as "held steady."
- The below-min-pass rows are honest carry-forwards, tracked against residual IDs
  referenced without re-definition:
  - **RR-114-01** (S-P02 inversion, 1/5, supersedes RR-108-01) — minted Phase 114
  - **RR-108-02** (S-P05 trade-off, **CLOSED** at 4/5) — resolved Phase 114
  - **RR-108-04** (S-P10 estimate, 0/5, carried-indeterminate, truncated) — kept
  - **RR-108-05** (S-P14 theoretical-limit, 0/5, carried-indeterminate, truncated) — kept
- A documented REGRESSION + the honest carry-forwards are the whole point of a
  measure+decide+defer milestone: honesty-not-score (D-01) governs every cell of the
  baseline and every sentence of this verdict. The measured result is the deliverable, not
  a chased green number.

---

## Out of Scope

### What this artifact does NOT do

The following actions are explicitly OUT OF SCOPE for this artifact, for Phase 115, and
for the entire v7.6 milestone:

- **The REGRESSION FIX** (S-P01 pre-mortem / S-P03 fishbone under-routing) — this is the
  single most important out-of-scope boundary. No `shared/` edit, no agent-body change,
  no trigger/phrase broadening in Phase 115. The fix is deferred to the named follow-up
  milestone (see Forward Pointer below).
- **Merge execution of any further technique pair** — `theoretical-limit`↔`inversion`
  (SECOND recommendation, gated on a clean S-P14 live re-measurement; tracked TLINV-01)
  and `estimate`↔? (FLAG, merge partner unscoped; tracked ESTPART-01) both remain
  deferred per the v7.4 verdict and the v7.5 merge doc. Neither is in scope for v7.6.
- **Any agent-body / `shared/` companion-technique change** — this is a measurement and
  verdict phase, not an authoring phase.
- **Any detector (`_battery_core.py`) change** — the detector is byte-frozen; the v7.6
  baseline was measured against the as-shipped detector.
- **Any new live run** — the v7.6 baseline (`tests/step0-baseline-v7.6.md`) is the one
  authoritative measurement for this milestone. Never re-run to chase a number (D-01/D-03).
- **A clean re-measurement of S-P10 / S-P14** — their 0/5 results are spend-limit-
  truncated, not confirmed misroutes. A clean re-measurement requires fresh live budget;
  it is deferred to a future milestone (RR-108-04/05 carried-indeterminate).

### Forward pointer: the routing-fix follow-up milestone

The REGRESSION FIX — addressing the S-P01 pre-mortem and S-P03 fishbone under-routing
found at the v7.6 re-baseline — is deferred to a **named follow-up milestone**: the
**five-whys / under-routing fix milestone**, gated on this verdict (VERDICT-01 of v7.6).

This is a concrete ordering constraint, not a calendar date or invented version number —
mirroring how `docs/expansion-measurement-verdict.md` named the
technique-merge-execution milestone and `docs/decompose-five-whys-merge.md` recorded its
closure. The routing-fix milestone must not begin until this verdict artifact is committed
and the traceability surface reconciled (VERDICT-02). It will scope: which trigger
phrases to add or broaden, the shared/ edit, regeneration, and re-validation.

See also: `.planning/REQUIREMENTS.md`, "Future Requirements (deferred)" — "A routing fix
for five-whys (or any regressed technique) IF the re-baseline shows it under-target —
forward-committed to a scoped follow-up milestone per the measure+decide+defer shape."

---

*Decision recorded: 2026-06-23*
*Authored in: Phase 115-verdict-artifact-traceability-reconciliation, Plan 01*
*Supersedes: nothing (first v7.6 merge-validation verdict artifact)*
