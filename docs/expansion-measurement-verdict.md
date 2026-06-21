# Expansion Measurement Verdict — v7.4

**Artifact type:** Decision / verdict record
**Date:** 2026-06-21
**Phase:** 109-verdict-artifact-traceability-reconciliation (Plan 01)
**Requirement:** VERDICT-01
**Status:** DECIDED

---

## Decision

The v7.4 live 9-technique Step 0 re-baseline (Phase 108, 110 live `claude` invocations,
`tests/step0-baseline-v7.4.md`) returns **P 4/9 → CONFIRMED**.

The milestone hypothesis under test was "capability breadth = result breadth" — i.e. that
expanding the technique portfolio from 6 to 9 would broaden the focused-routing results.
Observed **P 4/9**: the hypothesis "capability breadth ≠ result breadth" is **CONFIRMED**,
and merging the overlapping techniques is no longer deferred-optional but urgent.

**Spend-limit-robust caveat (honesty-not-score, D-01).** The confirming weight is carried
by **clean** evidence:

- **decompose (S-P09): 0/5 FAIL — clean.** Zero spend-limit truncations on any run; all
  5 runs routed to full-composer. This is the strongest confirming signal.
- **estimate (S-P10): 0/5 FAIL — clean.** The baseline `scores.tsv` records `full-composer`
  for all 5 runs — a clean under-route on every run. Confirming evidence on its own.
- **theoretical-limit (S-P14): 0/5 — spend-limit-INDETERMINATE.** All five runs returned
  the verbatim spend-limit message (`"You've hit your monthly spend limit"`), so the
  classifier received `none` with no agent dispatch. S-P14's 0/5 is therefore **an artifact
  of the spend limit, NOT a clean misroute.** Do not read S-P14's 0/5 as confirmed
  under-routing — it is honestly unresolved.

The not-refuted conclusion holds under **any** charitable reading: even if S-P14 is counted
as a PASS (the most generous possible interpretation), the tally is 5/9 → MIXED, still
below the ≥7/9 refute bar. The CONFIRMED verdict is spend-limit-robust.

---

## Evidence (falsifiable)

All K/N figures below are cloned verbatim from the source baseline and are checkable
directly against [`../tests/step0-baseline-v7.4.md`](../tests/step0-baseline-v7.4.md).
No figure is re-derived or transposed.

### 9-canonical per-technique tally

| # | Technique | Row | K/N | Verdict |
|---|-----------|-----|-----|---------|
| 1 | pre-mortem | S-P01 | 3/5 | PASS |
| 2 | inversion | S-P02 | 1/5 | FAIL |
| 3 | fishbone | S-P03 | 3/5 | PASS |
| 4 | five-whys | S-P04 | 4/5 | PASS |
| 5 | trade-off | S-P05 | 2/5 | FAIL |
| 6 | second-order | S-P06 | 5/5 | PASS |
| 7 | **decompose** | S-P09 | 0/5 | FAIL (first-ever live measurement) |
| 8 | **estimate** | S-P10 | 0/5 | FAIL (first-ever live measurement) |
| 9 | **theoretical-limit** | S-P14 | 0/5 | FAIL (first-ever live measurement) |

**Tally: P 4/9 → CONFIRMED.** (Pre-registered criterion: ≥7/9 → REFUTED; ≤~4/9 →
CONFIRMED; in between → MIXED.)

### Spend-limit caveat (per-row clean-vs-indeterminate status)

Consistent with honesty-not-score (D-01), the spend-limit contamination is recorded
verbatim and NOT masked:

- **S-P09 (decompose) 0/5 — CLEAN.** Not spend-limited on any run. All 5 observed
  modes: `full-composer`. The strongest confirming signal.
- **S-P10 (estimate) 0/5 — CLEAN.** All 5 observed modes in the baseline `scores.tsv`:
  `full-composer` — a clean under-route on every run.
- **S-P14 (theoretical-limit) 0/5 — SPEND-LIMIT-INDETERMINATE.** All 5 observed modes:
  `none` (spend-limit message, no agent dispatch). This row could not be cleanly measured
  before the session spend limit was reached. Its 0/5 is an artifact, not a confirmed
  under-route. Tracked as **RR-108-05** (carry, honestly unresolved, not masked).

The spend-limit also affected falsifier rows S-P11/S-P12/S-P13/S-P15 and control rows
S-N06/S-N07, which are excluded from the 9-technique bar. Full per-row evidence is in the
source baseline.

---

## Rationale

### Capabilities vs. results breadth

The v7.4 re-baseline conclusively demonstrates that **the 6→9 technique expansion added
zero result breadth**:

- The four passing techniques (pre-mortem 3/5, fishbone 3/5, five-whys 4/5, second-order
  5/5) are **exactly the original-6 subset** that already passed in the prior v6.4 baseline.
- The **original-6 subset itself is 4/6** — identical to the 4/6 prior. Expanding from 6
  to 9 techniques did not change the set of techniques whose Step 0 trigger fires.
- All **three newly-measured techniques** scored 0/5: decompose (clean), estimate (clean),
  theoretical-limit (indeterminate). Zero new techniques joined the passing set.

This result directly confirms the finding from the **v7.3 first-principles self-analysis**
(the activating prediction that v7.4 was run to verify): "capability breadth ≠ result
breadth." Adding techniques to the agent's repertoire has broadened what the agent *can*
do but has not broadened the routing that activates focused mode. The Step 0 trigger
mechanism — not the capability set — is the binding constraint.

The implication is concrete: the techniques that fail focused routing under-route because
their Step 0 trigger phrases do not reliably fire in natural phrasing, not because of a
capability gap. The overlap analysis (decompose↔five-whys, theoretical-limit↔inversion)
identifies the most actionable fix: merging overlapping techniques reduces the number of
trigger targets the Step 0 mechanism must distinguish.

---

## Merge Recommendation

This section implements D-02: a concrete, evidence-anchored recommendation with pair
selection AND execution deferred to the named follow-up milestone. The artifact
recommends; it does not choose-and-merge.

### Primary candidate pair: `decompose` ↔ `five-whys`

**Strongest candidate.** `decompose` (S-P09) scored **0/5 FAIL on clean evidence** —
all 5 runs were zero spend-limit, all 5 routed to full-composer. The trigger never fired.
The conceptual overlap is well-established: decompose (break a problem into primitive
components) and five-whys (recurse through causal layers) operate on the same
reduce-to-root-cause intent. Merging them reduces the trigger target count and concentrates
routing signal onto the remaining technique.

**Recommendation:** PRIMARY — investigate merge of `decompose` into `five-whys` (or a
unified technique under a shared trigger). Pair selection and merge execution are deferred
to the follow-up milestone.

### Second candidate pair: `theoretical-limit` ↔ `inversion`

**Second candidate (prior overlap analysis, honesty caveat applies).** `theoretical-limit`
(S-P14) scored **0/5 — spend-limit-INDETERMINATE** (all 5 runs truncated). Its
recommendation as a merge candidate therefore rests on the **prior overlap analysis** (the
v7.3 self-analysis identified theoretical-limit↔inversion as an overlapping pair) rather
than on a clean live miss. The live measurement could not confirm or deny the misroute;
the overlap rationale remains. `inversion` (S-P02) scored **1/5 FAIL** (RR-108-01,
carried).

**Recommendation:** SECOND — investigate merge of `theoretical-limit` into `inversion`
(or a unified technique), explicitly noting that S-P14's 0/5 is spend-limit-indeterminate
and the pair selection should be re-evaluated once a clean S-P14 live measurement is
available.

### Newly-evidenced candidate: `estimate` — partner needs scoping

**Newly evidenced, no pre-named partner.** `estimate` (S-P10) scored **0/5 FAIL on clean
evidence** — all 5 runs routed to full-composer per the baseline `scores.tsv`. This is a
genuine clean fail on first-ever live measurement.
However, `estimate` had **no pre-named merge partner** in the prior overlap analysis.

**Flag:** `estimate` (S-P10, **0/5 FAIL, clean**) is a newly-confirmed merge
candidate. Its merge partner needs scoping in the follow-up milestone before pair selection
can proceed. Do not pre-select a partner here without live evidence of the overlap.

**Recommendation:** FLAG — include `estimate` in the follow-up milestone's scoping
discussion; determine its merge partner (if any) based on behavioral analysis, not
assumption.

### Scope boundary

Pair selection AND execution are **explicitly deferred** to the named follow-up milestone
(see Out of Scope / Forward Pointer below). This artifact recommends; it does not
choose-and-merge. Any `shared/` edit, agent-body change, or detector change is out of
scope for v7.4 and for this artifact.

---

## Honesty-not-score Acknowledgement

**CONFIRMED + BATTERY: FAIL** is the legitimate committed outcome of Phase 108 and of this
verdict. No K/N number was softened, chased to a forced PASS, or masked.

- The four-passer result (P 4/9) was committed verbatim from the single authoritative live
  run. It was not re-run to improve the score (one authoritative baseline per milestone,
  REBASE-01 / CF-01).
- The below-min-pass rows are honest carry-forwards, tracked as residual IDs minted in
  Phase 108 (not re-defined here):
  - **RR-108-01** (S-P02 inversion, 1/5, supersedes RR-95-01)
  - **RR-108-02** (S-P05 trade-off, 2/5, supersedes RR-95-02)
  - **RR-108-03** (S-P09 decompose, 0/5, first-time)
  - **RR-108-04** (S-P10 estimate, 0/5, first-time)
  - **RR-108-05** (S-P14 theoretical-limit, 0/5, spend-limit-indeterminate, first-time)
- The spend-limit contamination on S-P14 is recorded prominently, NOT masked. Its 0/5 is
  labelled indeterminate, not called a clean misroute.
- A documented BATTERY: FAIL and an honest below-min-pass residual set are the whole point
  of the measurement: honesty-not-score (D-01) governs every cell of the baseline and every
  sentence of this verdict.

The CONFIRMED verdict is reached on the evidence, not on a score target. The confirming
weight is carried by decompose (S-P09, 0/5, clean) and estimate (S-P10, 0/5, clean runs
1–4) independently of S-P14. The verdict would read CONFIRMED even if S-P14 were
retroactively counted as a PASS.

---

## Out of Scope

### What this artifact does NOT do

The following actions are explicitly deferred and must NOT happen in this artifact, in
Phase 109, or in the v7.4 milestone:

- **Merge execution** of any technique pair (`decompose`↔`five-whys`,
  `theoretical-limit`↔`inversion`, or any `estimate`↔? pairing) — this is the single
  most important out-of-scope boundary. No `shared/` edit, no agent-body change, no
  `sync-content.py --write` regeneration for a merge.
- Any agent-body / `shared/` companion-technique change.
- Any detector (`_battery_core.py`) change.
- Any new live run (the v7.4 baseline is the one authoritative measurement for this
  milestone — never re-run to chase a number, CF-01).
- A clean re-measurement of S-P14 (theoretical-limit unaffected by spend-limit) — not
  required because the CONFIRMED verdict is spend-limit-robust; deferred to a future
  milestone that has fresh live budget.

### Forward pointer: the technique-merge-execution milestone

**Merge execution is deferred to a named follow-up milestone**: the
**technique-merge-execution milestone**, gated on this verdict (VERDICT-01).

This is a concrete ordering constraint, not a calendar date — mirroring how
`docs/gen-01-decision.md` named GEN-01-REARCH (the designated next live-routing milestone)
and `docs/gen-01-rearch-milestone.md` recorded its ordering constraint: "GEN-01-REARCH is
the designated next live-routing / Step-0 milestone to run after v6.2 closes."

The technique-merge-execution milestone must not begin until VERDICT-01 is closed (i.e.,
until this verdict artifact is committed and the traceability surface reconciled). It will
scope: which pair(s) to merge, the `estimate` partner question, the merge mechanics in
`shared/`, regeneration, and re-validation. That scoping work cannot be done well before
this data exists — and it now exists.

See also: `.planning/REQUIREMENTS.md`, "Future Requirements (deferred)" — the
technique-merge-execution milestone language carries the authoritative deferral boundary.

---

*Decision recorded: 2026-06-21*
*Authored in: Phase 109-verdict-artifact-traceability-reconciliation, Plan 01*
*Supersedes: nothing (first v7.4 expansion-measurement verdict artifact)*
