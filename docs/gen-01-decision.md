# GEN-01 Resolution Decision

**Artifact type:** ADR-style decision record (D-06)
**Date:** 2026-06-15
**Phase:** 87-gen-01-decision (Plan 01)
**Requirement:** GR-01 [CRITICAL]
**Status:** DECIDED

---

## Decision

GEN-01 (full Step 0 classifier rearchitecture) takes the
**convert-to-committed-future-milestone** path.

A new committed milestone, **GEN-01-REARCH**, is activated (D-01, D-02). GEN-01 leaves
the open-gap set as *scheduled forward work*, not a perpetual deferral. What distinguishes
this from prior deferrals is the concrete commitment structure mandated for Phase 88 (see
Forward Pointer section below).

---

## Rejected Alternatives

Three alternative resolution paths were considered and rejected:

**1. rearchitect-now**

Ruled out by the v6.2 documentation-scope boundary. A full classifier rearchitecture is
a distinct, large body of *live-routing* work — it requires iterative live `claude`
invocations, detector-marker broadening grounded in new captures, and K-of-N validation
across the focused-routing rows. None of that is a documentation task. Attempting to land
it within v6.2 would over-scope this milestone beyond its established boundary.

**2. bounded-fix**

Ruled out because it under-delivers for a gap of this scope. A partial code change to
`scripts/_battery_core.py` (e.g., adding one or two new detector markers without the
full evidence-grounded rearchitecture) cannot honestly close a full-classifier
rearchitecture gap. It would produce exactly the kind of score-chasing that
honesty-not-score discipline (D-01) prohibits — apparent improvement in the K/N metric
without the structural work that justifies calling the gap closed.

**3. formal-retire**

Ruled out because GEN-01 represents *real, still-measured, still-failing* live-routing
work. Retiring GEN-01 would abandon work the Step 0 harness continues to measure and
that the live baseline honestly records as failing (S-P01, S-P02, S-P05 all FAIL in
`tests/step0-baseline-v5.3.md`). Formal retirement without resolution is only appropriate
when the work is genuinely no longer relevant — that is not the case here.

---

## Evidence (falsifiable)

All figures below are checkable against their named source files.

### Live K/N from `tests/step0-baseline-v5.3.md`

The v5.3 live re-baseline (Phase 80, 60 live `claude` invocations, `--repeat 5
--min-pass 3`) records the following per-row results:

| Row | Expected MODE | K/N | Verdict |
|-----|---------------|-----|---------|
| S-P01 | focused-pre-mortem | 1/5 | FAIL |
| S-P02 | focused-inversion | 0/5 | FAIL |
| S-P05 | focused-trade-off | 0/5 | FAIL |
| S-N04 | full-composer | 2/5 | FAIL |

- **S-P01 1/5** — pre-mortem focused-routing dip; residual-risk **RR-79-01**
- **S-P02 0/5** — inversion focused-routing dip; residual-risk **RR-79-02**
- **S-P05 0/5** — trade-off focused-routing dip; residual-risk **RR-79-03**
- **S-N04 2/5** — negative-control over-routing dip; residual-risk **RR-80-01**

These four K/N figures are verified directly in `tests/step0-baseline-v5.3.md` (the
"Per-prompt results" table and the "Residual risk notes" section). No figure is rounded
or transposed.

### Step 0 harness state

Two scripts constitute the Step 0 measurement harness:

- **`scripts/check-step0-emulator.py`** (STEP0-08 CI gate) — offline phrase-detection
  classifier. Parses the `**Phrase detection rules**` table from
  `shared/spine/SKILL-body.md` into a deterministic regex classifier. `--self-test`
  runs the fault-injection fixtures plus a hardcoded named S-N04 assertion (RR-80-01
  layer 1: proving the S-N04 oblique prompt classifies `full-composer` at the
  phrase-detection layer). Runs in CI on every push/PR.

- **`scripts/check-step0-live.py`** (STEP0-06 CI gate) — live Step 0 MODE harness.
  Forces agent invocation over the approach-② `_wrap_for_bypass` bypass channel,
  classifies each run's MODE from the captured `.jsonl` stream, and scores K-of-N
  against `tests/step0-fixture-catalog.md`. The `--self-test` (offline) is the STEP0-06
  CI gate; the full manual run (`--repeat 5 --min-pass 3`, 60 invocations) produces the
  canonical live baseline. It continuously measures the focused-routing gaps and the
  S-N04 over-routing dip.

### Containment sentinels (measured-not-masked)

The four residual-risk IDs are locked against silent regression by offline sentinels
in `scripts/_battery_core.py`, function `self_test_boundary()` (BATT-06 CI gate):

- **RR-79-01** — S-P01 pre-mortem count vector `[0,1,2,1,3]` asserted across 5 vendored
  v5.2 excerpts in `tests/step0-captures-v5.2/S-P01-run{1..5}.txt`.
- **RR-79-02** — S-P02 zero inversion vocabulary asserted across 5 vendored v5.2 excerpts
  in `tests/step0-captures-v5.2/S-P02-run{1..5}.txt`.
- **RR-79-03** — S-P05 trade-off single-marker barrier: distinct canonical trade-off marker
  count always `< MIN_HEADER_HITS (2)` across 5 vendored v5.2 excerpts in
  `tests/step0-captures-v5.2/S-P05-run{1..5}.txt`.
- **RR-80-01** — S-N04 marker-counting assertion: one bare pre-mortem header hit `< MIN_HEADER_HITS`
  so `classify()` returns `"none"` not `"focused-pre-mortem"` (BATT-06 layer 2).

These sentinels assert the documented honest state, not a live pass-rate. The containment
proof is: the dips are continuously measured (harness), the honest documented states are
locked against drift (sentinels in `self_test_boundary()`), and any regression would
cause BATT-06 to fail CI.

---

## Rationale (D-07 falsifiable core)

**Scope-vs-risk:** The three focused-routing dips (S-P01 1/5, S-P02 0/5, S-P05 0/5) are
a genuine classifier rearchitecture problem — they require iterative capture-backed marker
work and live K-of-N validation to resolve. This is a distinct, large body of live-routing
work. v6.2's documentation-scoped milestone cannot safely contain that work without
exceeding its established scope boundary and risking quality on a fast timeline.

**Measured-not-masked:** The dips are real (confirmed by live baseline) and *contained*
(locked by offline sentinels in `self_test_boundary()`). The Step 0 harness
(`check-step0-live.py`) continuously measures the gap. Because the dips are measured and
not masked, they can be carried forward honestly — this is the honesty-not-score
discipline in action, not an evasion.

**Commit (schedule) rather than retire (abandon) or rush:** Formal retirement would abandon
work the harness keeps measuring. A bounded-fix would under-deliver (partial markers ≠
full rearchitecture). Rearchitecting now would over-scope v6.2. Therefore the correct
disposition is to commit to a fully-scoped future milestone — scheduled, not floating —
so the work receives the scope and live-session budget it requires.

---

## Honesty-not-score Acknowledgement (D-01 / D-08)

Converting GEN-01 to a committed future milestone is recorded here as a **legitimate
resolution**, not a failure and not a score-mask.

The live K/N figures (S-P01 1/5, S-P02 0/5, S-P05 0/5, S-N04 2/5) are honest
carry-forwards. They are NOT chased to a forced PASS, because:
- Forcing a PASS without the structural classifier work that justifies it would be a
  score-mask — precisely what honesty-not-score discipline (D-01) prohibits.
- The resolution criterion for GEN-01 is removing it from the open-gap set via a
  *legitimate* mechanism. Converting it to a committed scheduled milestone satisfies
  that criterion.
- The gap status changes from "perpetually deferred" (no committed resolution path) to
  "scheduled forward work" (committed milestone with a concrete scope and ordering).

The live scores will remain as honest carry-forwards until GEN-01-REARCH executes and
delivers the rearchitecture work.

---

## Forward Pointer: Mandate for Phase 88

This artifact activates the conditional **GEN-01-REARCH** entry in
`.planning/REQUIREMENTS.md` → "Future Requirements (deferred)". Phase 88 must satisfy
the following mandate (recorded here; not authored here):

### D-04: Full roadmap stub (not a named goal or one-line pointer)

The committed GEN-01-REARCH entry must be a **full roadmap stub** — it specifies its own
phases, requirement IDs, and dependencies. This is what distinguishes a *committed*
milestone from a renamed deferral. A stub that says only "implement GEN-01-REARCH
later" does not satisfy this requirement.

### D-05: Designated next live-routing milestone

GEN-01-REARCH must be explicitly tagged as the **designated next live-routing / Step-0
milestone** to run after v6.2 closes. This is a concrete ordering constraint, not a
hard calendar date. The ordering is load-bearing: it prevents GEN-01-REARCH from floating
indefinitely in a candidate list.

### D-03: Dual-placement requirement (authoritative + mirror)

Phase 88 must place the committed GEN-01-REARCH entry in **both** locations and keep them
consistent:

1. **Authoritative copy** — in the git-tracked `docs/` tree (e.g., a dedicated
   `docs/gen-01-rearch-milestone.md` or a `docs/future-milestones.md`). The exact
   filename is Phase 88's choice; D-03 fixes only that it is git-tracked under `docs/`.
   (`.planning/` is gitignored and cannot serve as the authoritative committed entry for
   milestone-tracking purposes.)

2. **Mirror pointer entry** — in `.planning/ROADMAP.md`, so the milestone surfaces in GSD
   workflow tooling. The mirror must point to the authoritative `docs/` copy and must be
   kept consistent with it.

**This artifact does NOT author that stub.** Phase 88 authors it.
**This artifact does NOT write the ROADMAP.md mirror.** Phase 88 writes it.
**This artifact does NOT add any cross-link from `docs/requirements-traceability.md`.**
That belongs to Phase 90 (Canonical Surface Reconciliation).

---

## Out of Scope for This Phase

The following actions are explicitly deferred and must NOT happen in Phase 87:

- Authoring the GEN-01-REARCH full roadmap stub (Phase 88)
- Writing the `.planning/ROADMAP.md` mirror pointer (Phase 88)
- Flipping GEN-01 out of `gap` in `scripts/check-traceability.py` (Phase 88)
- Regenerating `docs/requirements-matrix.md` (Phase 90)
- Adding the cross-link from `docs/requirements-traceability.md` to this file (Phase 90)
- Any changes to `scripts/check-step0-emulator.py`, `scripts/check-step0-live.py`,
  or `scripts/_battery_core.py`

---

*Decision recorded: 2026-06-15*
*Authored in: Phase 87-gen-01-decision, Plan 01*
*Supersedes: nothing (first GEN-01 decision artifact)*
