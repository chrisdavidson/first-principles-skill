---
phase: 04-companion-tool-references
reviewed: 2026-05-17T00:00:00Z
depth: standard
files_reviewed: 3
files_reviewed_list:
  - first-principles-thinking/references/five-whys.md
  - first-principles-thinking/references/pre-mortem.md
  - first-principles-thinking/references/trade-off-analysis.md
findings:
  critical: 0
  warning: 3
  info: 4
  total: 7
status: issues_found
---

# Phase 4: Code Review Report

**Reviewed:** 2026-05-17T00:00:00Z
**Depth:** standard
**Files Reviewed:** 3
**Status:** issues_found

## Summary

Reviewed three companion-tool reference files for the first-principles-thinking
skill: `five-whys.md`, `pre-mortem.md`, and `trade-off-analysis.md`. Each follows
a consistent structure (intro callout, "When to reach for this", "Procedure",
"Example", "Failure modes", "Handoff") and is internally coherent prose. The
worked-example arithmetic in `trade-off-analysis.md` is correct (A = 49, B = 62).
Cross-references to `SKILL.md` phase names were verified against the parent
`SKILL.md` and are accurate.

No critical defects. However, there is one clear contradiction between a stated
procedure and its own worked example, plus two procedural omissions where the
example does not exercise a rule the procedure mandates. These are real
consistency defects in a skill whose entire value proposition (per `CLAUDE.md`)
is that "every conclusion traces back to a verified ground truth" — an example
that violates its own procedure undermines the methodology it teaches.

## Warnings

### WR-01: Trade-off example uses 4 criteria, violating the procedure's "5–8 criteria" rule

**File:** `first-principles-thinking/references/trade-off-analysis.md:24-26, 61-69`

**Issue:** Step 2 of the procedure explicitly mandates "Identify 5–8 criteria that
matter to this decision." The "Too many criteria" failure mode reinforces the
upper bound ("More than 8 criteria dilute the signal"). But the worked example
locks only **4** criteria (Performance, Reliability risk, Cost, Warranty/support).
The example directly violates the rule the same file teaches. A reader
calibrating their own analysis against this example will reasonably conclude 4
criteria is acceptable, contradicting the procedure. This is the most damaging
defect type for a methodology skill: the canonical example demonstrates
non-compliance with the canonical rule.

**Fix:** Either (a) add one or two more criteria to the example so it falls
within 5–8 (e.g., "Portability" and "Ease of setup for a non-technical user"),
recomputing the totals; or (b) soften the procedure's lower bound to "roughly
4–8 criteria" and remove the implication that 5 is a hard floor. Option (a) is
preferred — keep the rule strict and make the example obey it.

### WR-02: Trade-off example never demonstrates the mandatory "Reliability risk" scoring direction, creating an ambiguous scale

**File:** `first-principles-thinking/references/trade-off-analysis.md:64, 74-75`

**Issue:** The criterion is named "Reliability risk." Higher *risk* is worse, yet
the example scores Option B (new) a **5** and Option A (refurb) a **2** on this
criterion, and the result narrative says the gap "is driven by reliability risk
... because device failure would leave the parent without support" — i.e., the
score of 5 represents *low* risk / *high* reliability. The score scale (1–5,
higher = better) is therefore being applied to a criterion whose *name* implies
higher = worse. Nothing in the file states the convention that all criteria must
be phrased so that higher score = more desirable. A reader could plausibly score
"Reliability risk" with 5 = highest risk and silently invert the result.

**Fix:** Add an explicit instruction to Step 4: "Phrase every criterion so that a
higher score is always more desirable (e.g., use 'Reliability' not 'Reliability
risk')." Then rename the example criterion to "Reliability" so the name matches
the scoring direction. This removes a genuine source of incorrect results.

### WR-03: 5-Whys example branches do not perform the mandated lateral scan at every level

**File:** `first-principles-thinking/references/five-whys.md:31-33, 52-61`

**Issue:** The procedure mandates: "At each level, ask 'What else caused this?'
before going deeper into any one branch. Complete the lateral scan at a level
before descending." The "Single-thread drilling" failure mode reinforces this as
a primary error. But in the example, the lateral scan ("Why else...") appears
**only at level 1** (line 57). Every deeper level (levels 2, 3 in both branches)
is a single-thread descent with no "What else caused this?" shown. The example
demonstrates exactly the "Single-thread drilling" anti-pattern below the first
level. As with WR-01, the canonical example contradicts the canonical procedure.

**Fix:** Either (a) extend the example so at least one deeper level shows a
considered-and-rejected alternate cause (e.g., under "No one sealed the bag",
note "Why else? — considered: bag is defective; rejected, bag seals fine"); or
(b) add a one-line note after the example acknowledging it shows a simplified
single alternative per level for brevity and that real analyses scan laterally
at every level. Option (a) better models the discipline the file teaches.

## Info

### IN-01: 5-Whys "Stop" test wording differs between procedure and example

**File:** `first-principles-thinking/references/five-whys.md:35-37, 55-56`

**Issue:** The procedure's stop test has two named conditions: (1) "you can state
a specific corrective action that would prevent recurrence" and (2) "that action
is within your practical control." The example's stop annotations use the
shorthand "In control, specific, prevents recurrence" (line 56) and "In control,
specific" (line 61) — the second branch's annotation omits the "prevents
recurrence" clause entirely. Minor inconsistency; both stop conditions should be
visibly confirmed in every stop annotation for the example to model the test
faithfully.

**Fix:** Make both stop annotations cite all three elements consistently, e.g.,
"Specific, in control, prevents recurrence" in both branches.

### IN-02: Pre-mortem "six months" framing vs. example "two weeks" horizon

**File:** `first-principles-thinking/references/pre-mortem.md:21-22, 63`

**Issue:** The Framing block states the premise as "It is approximately six
months from now." The example then applies the framing with "It is two weeks
from now" — appropriate, since the example plan is two weeks out. This is
defensible (the horizon should match the plan), but the file never says the
six-month figure is an adjustable placeholder. A literal reader could think the
framing must always say "six months."

**Fix:** Add a short clause to the Framing block, e.g., "(adjust the horizon to
sit just past the plan's completion date)" so the example's deviation is
explicitly sanctioned.

### IN-03: Trade-off "Steps 3 → 4" heading does not match the example's actual content

**File:** `first-principles-thinking/references/trade-off-analysis.md:70-75`

**Issue:** The heading "Steps 3 → 4 — weights locked, then scored independently"
implies the table shows step 3 (weight assignment) and step 4 (scoring). But
weights were already presented in the Step 2 table (lines 63-68), and this table
shows scoring plus the step 5 computation (weight × score and the summed Total).
The heading omits step 5 even though the Total column is step 5 output. Minor
labeling imprecision.

**Fix:** Retitle to "Steps 4 → 5 — scored independently, then computed" (weights
were shown under Step 2), or "Steps 3–5" if the intent is to span weight lock
through computation.

### IN-04: 5-Whys symptom example states a cause-flavored phrase, mildly at odds with "state the observable effect"

**File:** `first-principles-thinking/references/five-whys.md:25-26, 50`

**Issue:** The procedure says "Do not state a suspected cause — state the
observable effect." The example symptom is "The bread keeps going stale before it
is finished" — this is a clean observable effect and is fine. No defect in the
example itself. Flagging only that the procedure could strengthen the
example's instructional value by briefly contrasting a bad symptom ("the bread is
bought in too-large loaves" — a cause) against the good one, so readers see the
distinction the rule is guarding against.

**Fix:** Optional. Add a one-line counter-example in the Procedure's "State the
symptom" paragraph, e.g., "(Bad: 'loaves are bought too large' — that is a
suspected cause, not the observed effect.)"

---

## Narrative Findings (AI reviewer)

All findings above are narrative findings from direct review. No
`<structural_findings>` block was provided for this phase, so there is no
separate structural substrate section.

The three files are well-written and structurally consistent with each other and
with the parent `SKILL.md` (phase names "Phase 2 (Challenge Assumptions)",
"Phase 4 (Reason Upward)", "Phase 5 (Validate)" all match `SKILL.md` exactly;
the artifact names "Classified Assumptions Table", "Derivation Chain",
"adversarial validation pass" are consistent with `SKILL.md`). The dominant theme
across the three warnings is the same: **the worked examples do not fully obey
the procedures they sit beside.** For a skill whose stated core value is rigor a
skeptic cannot dismiss, the examples are the highest-leverage place to be exact.
WR-01 and WR-03 should be fixed before this phase ships.

---

_Reviewed: 2026-05-17T00:00:00Z_
_Reviewer: Claude (gsd-code-reviewer)_
_Depth: standard_
