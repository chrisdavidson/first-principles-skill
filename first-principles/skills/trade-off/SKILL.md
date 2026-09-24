---
name: trade-off
description: Runs a focused trade-off only — weighted-criteria scoring. Invoke via /trade-off only.
disable-model-invocation: true
metadata:
  version: "9.11.0"
license: MIT
---
<!-- DO NOT EDIT — generated from shared/skills/trade-off/SKILL.md by sync-content.py -->

# Focused Trade-off Mode

You are running in focused-trade-off mode. Execute the procedure below, produce
its canonical output sections, then run the focused-mode validation step below —
do not run the full 5-phase first-principles analysis. Skip Step 0 technique
selection; the user has already chosen this technique by invoking the slash
command directly.

## When to reach for this

Use this tool when two or more options are viable (none obviously dominant), the
choice spans multiple criteria that pull in different directions, and an
intuitive pick would be hard to justify to others.

Do not use it when one option dominates on every relevant criterion — that is a
direct decision, not a trade-off.

---

## Procedure

1. **Name the options — including the status quo.** List each option being
   compared, and **always include doing nothing** as one of them, named as what
   it concretely is ("keep the current 70/30 split", "stay on REST/JSON"). A
   comparison whose option set is all-change silently assumes change is
   warranted and reports that assumption back as a finding. If the status quo is
   genuinely unavailable — a contract expires, the hardware is failing — say so
   in one line and list it as ruled out; do not omit it silently.

2. **State the must-haves and apply them as knock-outs.** Before any scoring,
   name the conditions an option must satisfy to be viable at all. An option
   that fails a must-have is **eliminated, not scored low** — report it under
   `## Options` as knocked out, with the must-have it failed. Scoring a
   non-viable option lets a high weighted total out-vote a hard constraint,
   which is how an option that cannot actually be chosen wins a trade-off.
   If nothing is a must-have, write "no must-haves" rather than skipping the
   step — the two are different claims.

3. **List criteria.** Identify 5–8 criteria that matter to this decision. Lock
   this list — add no new criteria after this step. If a criterion matters, it
   must appear now.

4. **Assign weights. Lock them now.** Give each criterion a relative weight
   (1–5) before scoring any option. If you cannot assign weights without first
   seeing how options score, stop — locking weights before scoring is the core
   discipline that prevents reverse-engineering them to favor an intuitive pick.

5. **Anchor the scale, then score.** Before scoring, state for each criterion
   what a **1** and a **5** concretely mean — the anchors. "Cost: 1 = over
   $20k, 5 = under $2k" is an anchor; "Cost: 1 = bad, 5 = good" is not. Then
   score each option on each criterion independently (1–5) against those
   anchors. Phrase every criterion so higher is always better (e.g.,
   "Reliability" not "Reliability risk") — a mixed scale silently inverts the
   result. Without anchors a score means only "how I felt about this option",
   and the arithmetic that follows inherits that and dresses it as a number.

6. **Cite the ground truth each score rests on.** Every score names the
   `GT-ID`s that justify it. A score resting on a `GT-N?` input carries that
   `?` forward: per D-07, the chain this trade-off collapses into is capped at
   **MEDIUM** and its confidence line names the unverified input and the
   verification that would remove it. A score with no ground truth behind it is
   a preference — mark it as one rather than citing nothing.

7. **Compute:** multiply weight × score per criterion; sum per option.

8. **Read the result.** The highest weighted total among the surviving options
   is the recommendation. If it surprises you, only re-examine a weight when you
   can state why it was wrong *before* seeing the result — adjusting weights
   afterward is the failure mode this procedure prevents.

**Flip test — run it every time, not only on a near-tie.** Report the
**smallest weight change that changes the winner**: name the criterion, the
weight it would have to move to, and how far that is from the weight you
locked. Then ask whether that weight is genuinely wrong. A winner that survives
only a ±1 move on one criterion is a near-tie whatever the totals look like,
and a winner that survives every single-criterion move is a robust result —
both are findings, and neither is visible from the totals alone. Report the
flip distance under `## Recommendation`. Do not refine scores to break a
near-tie; refining manufactures false precision. If no single-criterion change
flips the result, say that explicitly — "no single weight change flips this"
is the strongest result this procedure can return, and it is worth stating.

---

## Example

**Decision:** Laptop for a parent who browses, video-calls, and writes
documents.

**Ground truths this rests on:**

- **GT-1** — the current machine drops video calls roughly weekly (observed over
  two months).
- **GT-2** — refurbished units from this vendor carry a 90-day warranty; new
  units carry 12 months (vendor's published terms, read at source).
- **GT-3?** — refurbished failure rates are "around twice" new in the first
  year. *Unverified — recalled from a review article, source not located.*

**Step 1 — options named, status quo included:**

- **A** — refurbished mid-range
- **B** — new entry-level
- **C** — keep the current laptop (status quo)

**Step 2 — must-haves applied as knock-outs:**

| Must-have | A | B | C |
|---|---|---|---|
| Holds a video call without dropping | ✓ | ✓ | **✗ (GT-1)** |

**C is knocked out, not scored.** Had it been scored instead, its perfect cost
score (5 × 3 = 15, nothing to spend) would have carried it close to A on a
total — while still failing the one thing the machine is being replaced *for*.
This is the failure mode step 2 exists to prevent.

**Steps 3-4 — criteria and weights locked before any scoring:**

| Criterion                       | Weight | 1 means…                    | 5 means…                     |
|----------------------------------|--------|-----------------------------|------------------------------|
| Performance                      | 4      | stutters on a video call    | headroom for years           |
| Reliability                      | 5      | failure expected in year 1  | failure unlikely in 5 years  |
| Cost                             | 3      | over $900                   | under $300                   |
| Warranty / support               | 4      | none                        | 12 months or more            |
| Portability                      | 2      | desk-bound                  | carried daily without thought|
| Ease of setup (non-technical)    | 3      | needs a technical helper    | works out of the box         |

**Step 5-7 — scored against those anchors, with the ground truth behind each:**

| Option     | Performance (×4) | Reliability (×5) | Cost (×3)  | Warranty (×4) | Portability (×2) | Ease of setup (×3) | Total  |
|------------|------------------|------------------|------------|---------------|------------------|--------------------|--------|
| A (refurb) | 4 × 4 = 16       | 2 × 5 = 10       | 5 × 3 = 15 | 2 × 4 = 8     | 3 × 2 = 6        | 3 × 3 = 9          | **64** |
| B (new)    | 2 × 4 = 8        | 5 × 5 = 25       | 3 × 3 = 9  | 5 × 4 = 20    | 4 × 2 = 8        | 4 × 3 = 12         | **82** |

Reliability scores rest on **GT-3?**; warranty scores on **GT-2**.

**Step 8 — result:** B scores 82 vs. A's 64, a gap of 18, driven by reliability
and warranty.

**Flip test:** no single weight change within the 1–5 scale flips this result.
The closest is Reliability 5 → 1, which closes the gap from 18 to 6 — and that
move means asserting reliability barely matters for a machine bought *because*
the current one fails. Every other single-criterion move leaves a wider gap
(Warranty 4 → 1 leaves 9; Cost 3 → 5 leaves 14). The recommendation is robust
in the sense this test can establish.

**Confidence:** MEDIUM, not HIGH. Reliability carries the heaviest weight (5)
and its scores rest on **GT-3?**, which is unverified — so per D-07 the chain
this collapses into is capped at MEDIUM. Locating a failure-rate figure in the
vendor's own return data, or a cited reliability study, would remove that cause.
Note what the flip test does *not* do here: it varies weights, not scores, so a
robust flip result does not repair an unverified input.

---

## Failure modes

- **Weights set after scoring.** If you scored options before assigning
  weights, the weights will unconsciously reflect the scores — discard and
  restart from step 4.

- **Too many criteria.** More than 8 criteria dilute the signal toward noise —
  prune to those that genuinely differentiate the options.

- **Criteria added mid-analysis.** Adding a criterion after seeing partial
  scores is almost always rationalizing — lock the list at step 3 and restart.

- **Treating a near-tie as a precision problem.** Refining scores to break a
  near-tie manufactures false precision; run the flip test instead.

- **Criteria that are not independent.** Two criteria measuring the same factor
  (e.g., "cost" and "budget impact") double-count it — merge or drop one.

- **The status quo left off the option list.** An all-change option set assumes
  change is warranted and then reports that assumption as a finding. Doing
  nothing is an option until a stated must-have rules it out (step 1).

- **A must-have scored instead of applied.** Scoring a non-viable option lets a
  high weighted total out-vote a hard constraint, so an option that cannot
  actually be chosen can win. Knock it out at step 2 and say which must-have it
  failed.

- **Unanchored scores.** Without stated 1-and-5 anchors a score records how the
  option felt, and the arithmetic launders that into a number. Anchors are what
  make two options comparable — and the same analysis reproducible.

- **The flip test skipped because the totals look decisive.** A wide gap can
  still rest on one weight. Run the test every time; "no single weight change
  flips this" is a real and reportable result, not a null one.

- **A robust flip result read as confidence in the inputs.** The flip test
  varies *weights*, not scores. It says nothing about whether a `GT-N?` behind a
  score is true, and never lifts D-07's cap.

---

## Output contract

The focused trade-off output MUST include these four level-2 section headers, verbatim,
as real `##` headings in the response. Strict on the header strings; soft on content.
This structure enables reliable downstream detection.

Required headers:

- `## Options`
- `## Criteria & Weights`
- `## Scoring`
- `## Recommendation`

---

## Handoff

The output is the recommended option with its weighted justification and the
reasoning behind the weights. Return to Phase 4 (Reason Upward) and convert it
into the Derivation Chain using the trade-off collapse form defined in
output-template.md §4 ("Converting structured-technique outputs into chains") —
citing the weighted scores as the step between ground truths and conclusion.

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
