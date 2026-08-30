---
name: trade-off
description: Runs a focused trade-off only — weighted-criteria scoring. Invoke via /trade-off only.
disable-model-invocation: true
metadata:
  version: "8.20.0"
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

1. **Name the options.** List each option being compared.

2. **List criteria.** Identify 5–8 criteria that matter to this decision. Lock
   this list — add no new criteria after this step. If a criterion matters, it
   must appear now.

3. **Assign weights. Lock them now.** Give each criterion a relative weight
   (1–5) before scoring any option. If you cannot assign weights without first
   seeing how options score, stop — locking weights before scoring is the core
   discipline that prevents reverse-engineering them to favor an intuitive pick.

4. **Score each option** on each criterion independently (1–5). Phrase every
   criterion so higher is always better (e.g., "Reliability" not "Reliability
   risk") — a mixed scale silently inverts the result.

5. **Compute:** multiply weight × score per criterion; sum per option.

6. **Read the result.** The highest weighted total is the recommendation. If
   it surprises you, only re-examine a weight when you can state why it was
   wrong *before* seeing the result — adjusting weights afterward is the
   failure mode this procedure prevents.

**Sensitivity check:** If two options score within roughly 10% of each other,
do not refine scores. Identify the criterion whose weight, if changed, would
flip the result, and ask whether that weight is genuinely wrong — if not, the
near-tie is a real finding and either option is defensible.

---

## Example

**Decision:** Laptop for a parent who browses, video-calls, and writes
documents — refurbished mid-range (A) vs. new entry-level (B).

**Step 2 — criteria locked:**

| Criterion                       | Weight |
|----------------------------------|--------|
| Performance                      | 4      |
| Reliability                      | 5      |
| Cost                             | 3      |
| Warranty / support               | 4      |
| Portability                      | 2      |
| Ease of setup (non-technical)    | 3      |

**Steps 3 → 4 — weights locked, then scored independently:**

| Option     | Performance (×4) | Reliability (×5) | Cost (×3)  | Warranty (×4) | Portability (×2) | Ease of setup (×3) | Total  |
|------------|------------------|------------------|------------|---------------|------------------|--------------------|--------|
| A (refurb) | 4 × 4 = 16       | 2 × 5 = 10       | 5 × 3 = 15 | 2 × 4 = 8     | 3 × 2 = 6        | 3 × 3 = 9          | **64** |
| B (new)    | 2 × 4 = 8        | 5 × 5 = 25       | 3 × 3 = 9  | 5 × 4 = 20    | 4 × 2 = 8        | 4 × 3 = 12         | **82** |

**Result:** B (new entry-level) scores 82 vs. 64 — driven by reliability and
warranty, weighted high because device failure would leave the parent without
support. Recommendation: buy new.

---

## Failure modes

- **Weights set after scoring.** If you scored options before assigning
  weights, the weights will unconsciously reflect the scores — discard and
  restart from step 3.

- **Too many criteria.** More than 8 criteria dilute the signal toward noise —
  prune to those that genuinely differentiate the options.

- **Criteria added mid-analysis.** Adding a criterion after seeing partial
  scores is almost always rationalizing — lock the list at step 2 and restart.

- **Treating a near-tie as a precision problem.** Refining scores to break a
  near-tie manufactures false precision; run the sensitivity check instead.

- **Criteria that are not independent.** Two criteria measuring the same factor
  (e.g., "cost" and "budget impact") double-count it — merge or drop one.

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

---

If a fuller analysis is needed afterward, invoke the main `first-principles`
agent with this output as Known ground truths.
