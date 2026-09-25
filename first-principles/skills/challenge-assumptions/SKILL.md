---
name: challenge-assumptions
description: Slash-only Phase 2 stub — classify and test every assumption before reasoning.
disable-model-invocation: true
metadata:
  version: "9.12.0"
license: MIT
---
<!-- DO NOT EDIT — generated from shared/skills/challenge-assumptions/SKILL.md by sync-content.py -->

# Focused Challenge Assumptions Mode

You are running in focused-challenge-assumptions mode. Execute the procedure below, produce
its canonical output sections, then run the focused-mode validation step below —
do not run the full 5-phase first-principles analysis. Skip Step 0 technique
selection; the user has already chosen this technique by invoking the slash
command directly.

## When to reach for this

Use this phase once the Essence Statement from Phase 1 is complete. An unchallenged
assumption that is false propagates invisibly through every later reasoning step. By
explicitly classifying and testing each assumption before establishing ground truths,
the analysis prevents false premises from masquerading as verified facts.

---

## Procedure

Identify every assumption — explicit and implicit — that bears on the problem. For each
one, classify it by type using the four-type scheme below, apply the prescribed treatment,
and record the verdict. Surface hidden assumptions: things that are treated as given but
have never been verified. When the assumption space feels too broad to enumerate by
intuition, use the fishbone procedure to brainstorm causes by category, then bring each
branch into this table as an `untested belief`. When a conclusion feels too clean or a
goal feels too obvious, use the inversion procedure to enumerate what would guarantee
failure — each unverified precondition becomes an `untested belief` row in this table.
When the stakes of a conclusion rest heavily on a particular assumption, push that
assumption down toward physical law or verified ground truth status rather than accepting
a weaker classification. Classification drives the method — it is not merely labelling.

**The four assumption types and their prescribed treatments:**

| Type | Prescribed Treatment |
|------|---------------------|
| **physical law** | Accept as a ground-truth candidate. Physical laws do not expire and cannot be negotiated away. |
| **current constraint** | Record the expiry conditions — what would have to change for this constraint to lift. |
| **convention** | Explicitly challenge before use. Ask whether the convention holds in this specific context or merely carries historical inertia. |
| **untested belief** | Verify, or flag as unverified. An unverified belief may be used in a derivation chain but must be visibly flagged (e.g., `GT-N?: unverified`) and any conclusion depending on it inherits an explicit confidence caveat. |

**Stakes-escalation rule:** The higher the stakes of the conclusion resting on an
assumption, the more that assumption must be pushed toward physical law or verified ground
truth. A critical conclusion resting on a convention or untested belief is a fragile
conclusion — either verify the assumption or flag the conclusion's confidence accordingly.

For a refined within-type subtype catalog with prescribed treatments and cited evidence,
see the Assumption Taxonomy reference. Subtypes are recommended-but-not-required; the
parent type's treatment remains a valid fallback.

**Named artifact:** Classified Assumptions Table — a table with columns: Assumption,
Type, Treatment, Verdict, Verification.

**Exit criterion:** Every assumption in scope has a classification from the four-type
scheme (physical law / current constraint / convention / untested belief) AND has a
recorded verdict and verification note, or an explicit "unverified — flagged" note per
D-07.

## Focused-mode validation

**Check the output against its own completion condition before presenting it.** The
procedure above states one, in whichever form this technique uses — an exit criterion, a
stop test, or an output contract. Read that condition again and confirm the output actually
produced meets every requirement it names, not just the ones that were easiest to satisfy.

**This is a scope-proportionate check, not the six-criterion Self-Audit Gate.** That gate
scores a six-section analysis document; this run produced one technique's output sections,
not six, so walking all six criteria against it would score structure that was never
produced. The larger of the two components: a focused run does not acquire evidence — it
opens no cited source — so a claim resting on a source this run did not open stays marked
rather than being resolved as confirmed.

**Carry the mark forward.** Anything this run could not verify is carried into the output
marked with a `?` rather than dropped or silently asserted as fact.

**Run the technique's own semantic check before declaring the output satisfied.** The
completion condition above is structural — it asks whether the required parts are present.
This asks whether the content holds up. One question, per technique:

- **five-whys** — is each cause counterfactually necessary: would the symptom still have
  happened without it?
- **fishbone** — does each prioritised cause carry an observation that distinguishes it
  from its siblings?
- **inversion** — is each precondition stated as a claim that can be false, and tagged for
  whether the conclusion survives it being false?
- **estimate** — does the bracket's whole width drive the same decision? If the low and
  high ends point different ways, the bracket has not yet answered the question.
- **trade-off** — does the winner survive the smallest weight flip, and is the status quo
  among the options?
- **pre-mortem** — does every fatal or costly cluster carry a tripwire that someone is
  positioned to see?
- **second-order** — has any effect been checked against what the decision is *for*, not
  only against what is true?
- **theoretical-limit** — is the bound the tightest applicable one, and is the demonstrated
  tier an observed figure rather than a calculated one?

A failed semantic check is a `not satisfied` result, not a caveat to attach to a satisfied
one.

**Escalate to the full composer when a `?` becomes load-bearing.** If a claim this run could
not verify turns out to be one the answer does not survive being false — load-bearing in the
validation rubric's sense — stop and say so, in this form:

- `Focused-mode escalation: <the ?-marked claim> is load-bearing - recommend a full analysis`

A focused run acquires no evidence, so it cannot resolve that claim; continuing produces a
confident-looking answer resting on exactly the thing nobody checked. Escalation is the
honest exit, and it is the only case where a focused run should decline to answer in its own
terms. Recommend the escalation; do not silently perform a full analysis instead — the run
was asked for one technique.

**Revise once, then stop.** If the check fails, revise the output and check it again.
Revise at most one time. If it still fails after that pass, present the output with the
gap named rather than revising again.

**End every run with a validation line, without exception.** State exactly one of the
following, verbatim, never silently:

- `Focused-mode validation: satisfied`
- `Focused-mode validation: revised once, now satisfied`
- `Focused-mode validation: not satisfied - <reason>`

Close with the reason this line is unconditional: a silent run is indistinguishable from a
run that skipped the check.

**Then state the residual, on its own line, every time — including after `satisfied`.**
Verbatim:

- `Focused-mode residual: this run opened no cited source, so any ?-marked claim is unverified, not merely uncited.`

This is the one thing the reader of a focused run cannot infer from the output. The
completion-condition check above is a rule *this document* gives the model; the residual is a
fact about the run that its reader needs, and until it is emitted the reader has no way to
tell a focused analysis from a full one that happened to be short. `satisfied` means the
output met its completion condition — never that its claims were verified against a source.

---

If a fuller analysis is needed afterward, invoke the main `first-principles`
agent with this output as candidate inputs for Phase 2. Carry the `?` marks
with it — this run opened no cited source.
