# Trade-Off Analysis

> Structures a choice between two or more genuinely viable options by weighting
> criteria before scoring — preventing the reverse-engineering of weights to
> justify a decision already made intuitively.

---

## When to reach for this

Use this tool when: two or more options are viable (none obviously dominant), the
choice spans multiple criteria that pull in different directions, and a single
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
   (1–5). Lock the weights before scoring any option. If you find you cannot
   assign weights without first looking at how the options score, stop — you are
   not ready to use this tool. Locking weights before scoring is the core
   discipline: it prevents reverse-engineering weights to favor a choice you have
   already made intuitively.

4. **Score each option** on each criterion independently (1–5).

5. **Compute:** multiply weight × score per criterion; sum across criteria per
   option.

6. **Read the result.** The highest weighted total is the analysis's
   recommendation. If the result surprises you, re-examine the weights — but
   only if you can state why a specific weight was wrong *before* you saw the
   result. Adjusting weights after seeing scores to change the outcome is the
   failure mode this procedure is designed to prevent.

**Sensitivity check:** If two options score within roughly 10% of each other, do
not refine scores further. Instead, identify the single criterion whose weight,
if changed, would flip the result. Ask whether that weight is genuinely wrong —
if not, the near-tie is a real finding: either option is defensible.

---

## Example

**Decision:** Which laptop to buy for a parent who mainly browses, video-calls,
and writes documents — a refurbished mid-range machine or a new entry-level
machine.

**Options:** A = Refurbished mid-range, B = New entry-level

**Step 2 — criteria locked:**

| Criterion          | Weight |
|--------------------|--------|
| Performance        | 4      |
| Reliability risk   | 5      |
| Cost               | 3      |
| Warranty / support | 4      |

**Steps 3 → 4 — weights locked, then scored independently:**

| Option     | Performance (×4) | Reliability risk (×5) | Cost (×3) | Warranty (×4) | Total  |
|------------|------------------|-----------------------|-----------|----------------|--------|
| A (refurb) | 4 × 4 = 16       | 2 × 5 = 10            | 5 × 3 = 15 | 2 × 4 = 8    | **49** |
| B (new)    | 2 × 4 = 8        | 5 × 5 = 25            | 3 × 3 = 9  | 5 × 4 = 20   | **62** |

**Result:** B (new entry-level) scores 62 vs. 49. The gap is driven by
reliability risk and warranty — criteria weighted high because device failure
would leave the parent without support. Recommendation: buy new.

---

## Failure modes

- **Weights set after scoring.** If you scored options before assigning weights,
  the weights will unconsciously reflect the scores. Discard and restart from
  step 3.

- **Too many criteria.** More than 8 criteria dilute the signal — each
  criterion's influence shrinks toward noise. Prune to the criteria that
  genuinely differentiate the options.

- **Criteria added mid-analysis.** Adding a criterion after seeing partial
  scores is almost always rationalizing. Lock the list at step 2 — restart if
  an omitted criterion is material.

- **Treating a near-tie as a precision problem.** Refining scores to break a
  near-tie manufactures false precision. Run the sensitivity check: find the
  swing criterion and decide whether that weight is genuinely wrong.

- **Criteria that are not independent.** If two criteria measure the same
  factor (e.g., "cost" and "budget impact"), they double-count its influence.
  Merge them or keep only the more precise one.

---

## Handoff

The output of this tool is the recommended option with its weighted justification
and the reasoning behind the weight assignments. Return to Phase 4 (Reason
Upward) and use this output as the Derivation Chain that selects between viable
options — citing the weighted scores as the intermediate step between the ground
truths and the final conclusion.
