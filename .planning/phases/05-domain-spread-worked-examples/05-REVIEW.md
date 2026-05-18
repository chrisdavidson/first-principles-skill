---
phase: 05-domain-spread-worked-examples
reviewed: 2026-05-18T00:00:00Z
depth: standard
files_reviewed: 4
files_reviewed_list:
  - first-principles-thinking/examples/personal-general.md
  - first-principles-thinking/examples/product-business.md
  - first-principles-thinking/examples/science-engineering.md
  - first-principles-thinking/examples/software-systems.md
findings:
  critical: 0
  warning: 5
  info: 5
  total: 10
status: issues_found
---

# Phase 5: Code Review Report

**Reviewed:** 2026-05-18
**Depth:** standard
**Files Reviewed:** 4
**Status:** issues_found

## Summary

This is a re-review of the four domain worked-example documents after the GAP-01/02/03
gap-closure edits. The prior `05-REVIEW.md` has been replaced because most of its
findings are now stale: the `Conclusion A/B/C` heading scheme is gone (all examples now
use the template's `### Conclusion: [text]` form), the invented "Phase 4
no-analogies-as-direct-evidence rule" wording is gone (`product-business.md` now cites
"the Phase 4 instruction not to use analogies as direct evidence (SKILL.md, Phase 4
Operation)"), GT-2 in `science-engineering.md` now explicitly enumerates battery
round-trip loss, and `product-business.md` now carries a preamble. Those prior warnings
are confirmed closed and are not re-reported.

The remaining review focused on what the gap closure did not catch: arithmetic and
factual correctness of the derivation inputs, internal numeric consistency, and residual
template-conformance gaps. These are pure-Markdown documentation artifacts — there is no
security surface and no runtime behavior, so there are no BLOCKER findings. But the
skill's stated core value is that "every conclusion traces back to a verified ground
truth" and the examples are explicitly calibration material the model reads to learn
what rigor looks like. A wrong number presented as a verified ground truth, or a result
range the chain never actually computes, teaches the wrong habit and is reported as
WARNING.

No `<structural_findings>` block was provided; this report contains narrative findings
only.

## Narrative Findings (AI reviewer)

## Warnings

### WR-01: GT-3 misstates the California marginal tax rate for the income band in question

**File:** `first-principles-thinking/examples/personal-general.md:47` (consumed at line 60)
**Issue:** GT-3 states "California marginal state income tax rate on income above
approximately $125,000 is approximately 13.3%" and cites "California Franchise Tax Board
... published rate schedules" as the source. This is factually wrong as a *marginal*
rate for income just above $125K. California's 13.3% figure is the top marginal rate and
applies only to taxable income above roughly $1M. In the ~$125K–$250K band a software
engineer's incremental income actually falls in, the California marginal rate is about
9.3%. Oregon's top rate is ~9.9%. So the realistic California-vs-Oregon marginal
differential on the $70K increment is roughly **zero, or even slightly in Oregon's
favor** — not the +3.4 percentage points GT-3 claims. Chain 1 (line 60) then derives
"additional state tax burden ... approximately $2,400/year" directly from this wrong
3.4-point figure. For a skill whose entire premise is that ground truths are *verified*
facts traceable to a cited source, presenting an incorrect tax rate as GT-3 with an
authoritative-sounding citation is the most serious defect in the set: it is exactly the
"well-packaged conjecture" the methodology exists to expose, embedded in the example
meant to model the methodology.
**Fix:** Correct GT-3 to the marginal rate that actually applies to the stated income
band (~9.3% CA vs ~9.9% OR; differential approximately 0 to −0.6 points), and propagate
the corrected — much smaller, possibly negative — tax term through Chain 1 (line 60),
the Abandoned Reasoning section (line 83), and the Conclusion (lines 97, 103). If the
intent is genuinely to exercise the 13.3% bracket, the scenario must be rewritten so the
persona's total taxable income exceeds ~$1M, which is implausible for the stated
software engineer. Correcting GT-3 is the right choice; note it also changes the Chain 1
effective-gain figure (see WR-02).

### WR-02: Chain 1 reports a "$50,000–$52,000" range but the arithmetic produces a single point

**File:** `first-principles-thinking/examples/personal-general.md:57, 61, 97, 99, 103`
**Issue:** The effective compensation gain is stated repeatedly as "approximately
$50,000–$52,000". The Chain 1 derivation at line 60 produces exactly one combined
deduction: ~$15,600 rent premium + ~$2,400 tax ≈ $18,000, giving $70,000 − $18,000 =
$52,000. Nothing in the chain computes the $50,000 lower bound — the chain arrives at a
single point. Line 61 attributes the range to "the illustrative precision of GT-2 and
GT-3", but that is a post-hoc justification: the stated arithmetic does not generate a
$2,000-wide interval. Worse, the chain explicitly says the $18,000 is "before accounting
for other SF cost differences (transportation, food, services)" — those unquantified
extra costs would push the effective gain *below* $50,000, so $50,000 cannot be a floor.
The range is asserted, not derived, which conflicts with rubric Criterion 6 (every
Conclusion claim traces to a chain) and the template rule that Section 6 introduces no
new claims (`output-template.md:140`).
**Fix:** Make the chain produce whatever it reports. Either show an explicit low/high
computation (state a band for the rent and tax terms and carry both ends through the
arithmetic), or replace the range with the single point the current arithmetic yields
("approximately $52,000") and update lines 57, 61, 97, 99, 103 to match. The figure in
Section 6 must equal the figure Chain 1 computes. Note WR-01's correction changes this
number regardless, so WR-01 and WR-02 should be fixed together.

### WR-03: "More than four times" overstates an exact 4.0x ratio

**File:** `first-principles-thinking/examples/science-engineering.md:156, 182, 184`
**Issue:** The peak-load dead end computes 250 W × 24 h = 6 kWh/day and describes the
result as "more than four times the actual 1.5 kWh/day load" (line 156) and a
"specification more than four times too large" (line 184). 6 ÷ 1.5 = exactly 4.0, not
more than four. In a worked example whose own Success Criteria (lines 24-25) demand that
"every sizing number traces to a named ground truth or a derivation chain" and that
uncertainty is explicitly propagated, an imprecise multiplier models the wrong habit. (A
defensible alternative reading — that the 6 kWh peak-sizing figure ignores the ~1.5 kWh
of non-pump load, so the true full-system overbuild is *less* than 4x — makes "more
than" wrong in the other direction too.)
**Fix:** Change "more than four times" to "four times" (or "roughly four times") at
lines 156 and 184. Pick whichever is arithmetically defensible and state it precisely.

### WR-04: product-business Chain 3 and Conclusion claim a break-even rate is computable from GTs that do not supply the needed input

**File:** `first-principles-thinking/examples/product-business.md:67, 88`
**Issue:** Chain 3 (line 67) states "The break-even conversion rate can be calculated
from GT-1 and GT-3 ... (blended monthly cost per free user) / (average contract value)",
and the Conclusion (line 88) repeats this as "calculable from GT-1 and GT-3". But GT-3
(line 37) only asserts that free-tier costs *exist and must be separately budgeted* — it
provides no "blended monthly cost per free user" figure and no number from which one
could be derived. The break-even formula therefore cannot actually be evaluated from the
named ground truths; it requires a per-user cost input that no GT supplies. This is the
same defect class the document itself flags elsewhere (GT-4 being a verified gap). Rubric
Criterion 4 requires a chain's intermediate to be genuinely supported by the named
GT-IDs; here the chain overstates what the ground truths enable.
**Fix:** Either add a ground truth for the blended monthly cost-per-free-user estimate
(an unverified `GT-5?` is acceptable if it is only an estimate, and would correctly
force a confidence caveat on Chain 3), or soften the wording to name cost-per-free-user
as a *required input that must be measured*, not as something already derivable from
GT-1 and GT-3. As written, Chain 3 and the Conclusion claim more than the GTs support.

### WR-05: Section 1 shape is inconsistent across the four examples and departs from the strict template

**File:** `first-principles-thinking/examples/software-systems.md:9-26`,
`first-principles-thinking/examples/personal-general.md:7-25`
**Issue:** `output-template.md:10` calls the format a "strict-shape document" and
prescribes Section 1 "Problem Essence" as a `**Core problem:**` sentence plus
`**Success criteria:**`. `product-business.md` and `science-engineering.md` follow this.
`software-systems.md` Section 1 inserts a `**Scenario:**` block before `**Core problem:**`;
`personal-general.md` Section 1 inserts `**Background:**` and `**The re-framing
operation:**` before `**Core problem:**`. The extra subsections are not part of the
prescribed Section 1 shape, and the two deviating examples differ from each other on
which extra subsections appear — so the calibration set sends contradictory signals
about what Section 1 must contain.
**Fix:** Either (a) bring all four examples into uniform Section 1 shape — Core problem
+ Success criteria only — moving scenario/background context into the italic preamble
that already sits above Section 1, matching `product-business.md` and
`science-engineering.md`; or (b) amend `output-template.md` to explicitly define an
optional scenario/background block within Section 1. Option (a) keeps the template
strict and is preferred. Whichever is chosen, all four examples must end up consistent.

## Info

### IN-01: "approximately" applied to an exact computed sum

**File:** `first-principles-thinking/examples/science-engineering.md:90`
**Issue:** The per-appliance table total reads "**~1,495 Wh ≈ 1.5 kWh/day**". The five
component rows (240 + 540 + 390 + 125 + 200) sum to exactly 1,495, and each component is
an exact product of the stated W × h values. The `~` before 1,495 is therefore
misleading — 1,495 is an exact sum; the only approximation is the rounding to 1.5 kWh.
The genuine uncertainty in the *inputs* is already correctly carried by the `GT-5?` flag
and the verification-path note.
**Fix:** Write "1,495 Wh ≈ 1.5 kWh/day" — drop the `~` before 1,495, keep `≈` for the
rounding step.

### IN-02: science-engineering uses a non-template Confidence label format

**File:** `first-principles-thinking/examples/science-engineering.md:118, 135, 197`
**Issue:** `output-template.md:111` prescribes `**Confidence:** [HIGH / MEDIUM / LOW]` —
the label bold, the rating outside the bold span. The other three examples follow this.
`science-engineering.md` writes `**Confidence: MEDIUM**` (rating inside the bold) at all
three occurrences. A validator pattern-matching on the prescribed `**Confidence:** RATING`
form (rubric Criterion 5) could miss these, and the examples are meant to model the exact
output format.
**Fix:** Change `**Confidence: MEDIUM**` to `**Confidence:** MEDIUM` at lines 118, 135,
and 197.

### IN-03: No example demonstrates the honest-depth escape valve

**File:** all four files (Section 5, Abandoned Reasoning)
**Issue:** `output-template.md:130-134` defines the `Nothing material here — [reason]`
escape valve, and the validation rubric scores its correct use (escape-valve scoring
rule). All four examples populate every section with real content, so the calibration
set never shows the model what a correct escape-valve use looks like. This is not a
defect in any single file — but the four examples are the only calibration material, and
a documented part of the format is unmodeled.
**Fix:** Optional but recommended for a calibration set — consider having one example
demonstrate the escape valve in a section where it genuinely applies, or add a short note
in `SKILL.md` pointing to `output-template.md` for the escape-valve form. Not required to
pass the phase.

### IN-04: Section 6 of personal-general drops a caveat that Chain 1 attached to the $18,000 figure

**File:** `first-principles-thinking/examples/personal-general.md:60` vs `97, 103`
**Issue:** Chain 1 (line 60) qualifies the $18,000 differential as "roughly $18,000/year
before accounting for other SF cost differences (transportation, food, services)".
Section 6 line 97 and line 103 both restate the figure *with* the caveat — so this is
actually consistent on close reading. Flagging only because the caveat phrasing is long
and repeated three times nearly verbatim; consider stating it once and referencing it.
Minor stylistic redundancy, not an inconsistency.
**Fix:** Optional — state the "before other SF costs" caveat once and cross-reference it
rather than repeating the full clause at lines 60, 97, and 103.

### IN-05: science-engineering intro line forward-references a GT-ID

**File:** `first-principles-thinking/examples/science-engineering.md:5`
**Issue:** The intro line names "a genuine unverified input (GT-5?)" — a forward
reference to a GT defined later in Section 3. The other three examples do not name
specific GT-IDs in their intro lines. Minor consistency nit; the forward reference is
understandable and arguably useful as a signal of the example's distinguishing feature.
**Fix:** Optional — either keep it (it usefully flags what makes this example distinct)
or rephrase to "a genuine unverified load estimate" without the ID, to match the other
three intros.

---

_Reviewed: 2026-05-18_
_Reviewer: Claude (gsd-code-reviewer)_
_Depth: standard_
