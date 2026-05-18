---
phase: 05-domain-spread-worked-examples
fixed_at: 2026-05-18T00:00:00Z
review_path: .planning/phases/05-domain-spread-worked-examples/05-REVIEW.md
iteration: 1
findings_in_scope: 5
fixed: 5
skipped: 0
status: all_fixed
---

# Phase 5: Code Review Fix Report

**Fixed at:** 2026-05-18
**Source review:** .planning/phases/05-domain-spread-worked-examples/05-REVIEW.md
**Iteration:** 1

**Summary:**
- Findings in scope: 5 (WR-01 through WR-05; critical_warning scope, no critical findings, Info findings IN-01..IN-05 out of scope)
- Fixed: 5
- Skipped: 0

## Fixed Issues

### WR-01: GT-3 misstates the California marginal tax rate for the income band in question

**Files modified:** `first-principles-thinking/examples/personal-general.md`
**Commit:** 6a012f5 (committed jointly with WR-02 — the two findings are coupled)
**Applied fix:** Rewrote GT-3 to state the marginal rate that actually applies to the
$125K–$250K income band the engineer's raise falls in: ~9.3% California vs ~9.9% Oregon,
a differential of roughly 0 to −0.6 percentage points (effectively negligible, possibly a
slight Oregon disadvantage). Added an explicit note that California's frequently-cited
13.3% figure is the *top* marginal rate applying only above ~$1M of taxable income and is
not the marginal rate on this raise. The corrected differential was then propagated
through every dependent figure (see WR-02).

### WR-02: Chain 1 reports a "$50,000-$52,000" range but the arithmetic produces a single point

**Files modified:** `first-principles-thinking/examples/personal-general.md`
**Commit:** 6a012f5 (committed jointly with WR-01 — the two findings are coupled)
**Applied fix:** Replaced the asserted "$50,000-$52,000" range with the single point the
corrected arithmetic now yields. With the WR-01 tax correction the tax term becomes ~$0,
so Chain 1's combined deduction is the ~$15,600/year rent premium alone, giving an
effective gain of $70,000 − $15,600 ≈ $54,000. Updated the Chain 1 heading, the chain
steps, and the Chain 1 confidence line; updated Chain 2's "$50K gain" reference to
"~$54K"; updated the Abandoned Reasoning section ("$50,000-$52,000" → "$54,000",
"25-30%" → "roughly 23%"); and updated Section 6 recommendation point 3, the trade-offs
paragraph, and the cost-differential figure ("~$18,000" rent-and-tax → "~$15,600" rent
only). The chain now states $54,000 is an upper bound, since unquantified additional SF
costs would push the figure lower — replacing the post-hoc range justification with an
honest single derived point plus a directional caveat.

**Note:** WR-01 and WR-02 are factual/arithmetic corrections that propagate through a
derivation chain. The numeric propagation was done by hand; the developer should confirm
the corrected effective-gain figure (~$54,000) and the negligible tax differential before
the phase proceeds — requires human verification of the corrected figures.

### WR-03: "More than four times" overstates an exact 4.0x ratio

**Files modified:** `first-principles-thinking/examples/science-engineering.md`
**Commit:** b20c011
**Applied fix:** Changed "more than four times the actual 1.5 kWh/day load" to "exactly
four times the actual 1.5 kWh/day load (6 ÷ 1.5 = 4.0)" in the Abandoned Reasoning
section, and "a specification more than four times too large" to "a specification four
times too large" in the Key insight. The multiplier is now stated precisely with the
arithmetic shown inline.

### WR-04: product-business Chain 3 and Conclusion claim a break-even rate is computable from GTs that do not supply the needed input

**Files modified:** `first-principles-thinking/examples/product-business.md`
**Commit:** db1ec3a
**Applied fix:** Softened the Chain 3 wording and the matching Section 6 Conclusion text.
The break-even formula is retained, but the documents now state explicitly that GT-1
supplies the average contract value while no named ground truth supplies the blended
monthly cost per free user — GT-3 establishes only that this cost is real, not its
magnitude. The threshold is reframed as not-yet-calculable from the named ground truths,
requiring one additional measured input (the per-free-user cost) that the pilot itself
must produce. Chain 3's conclusion (pre-specify the threshold before the pilot) is
unchanged and remains HIGH confidence, since it is a methodological claim and no longer
overstates what the GTs enable.

### WR-05: Section 1 shape is inconsistent across the four examples and departs from the strict template

**Files modified:** `first-principles-thinking/examples/personal-general.md`,
`first-principles-thinking/examples/software-systems.md`
**Commit:** ec89e8f
**Applied fix:** Applied review option (a) — brought all four examples into uniform
Section 1 shape (Core problem + Success criteria only). In `software-systems.md` the
`**Scenario:**` block was moved out of Section 1 into the italic preamble above it. In
`personal-general.md` the `**Background:**` and `**The re-framing operation:**` blocks
were moved into the preamble (relabelled `**Scenario.**` and `**The re-framing
operation.**` as preamble paragraphs). Section 1 in both files now opens directly with
`**Core problem:**`, matching `product-business.md` and `science-engineering.md` and the
strict-shape output template.

---

_Fixed: 2026-05-18_
_Fixer: Claude (gsd-code-fixer)_
_Iteration: 1_
