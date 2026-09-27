# First-Principles Analysis: Fund the $310K/Year Loyalty Program?

*(Full-composer mode — no single technique phrase triggered the Step 0 detector, so all five phases run in full; the estimate technique is applied inline in Phase 4 for the unit-economics rebuild, and second-order thinking is applied for the extension pass.)*

## 1. Problem Essence

**Core problem:** Should the company commit ≈$310,000/year to a loyalty/points program on the bet that it will pull monthly churn from 6.8% back toward ≈5%, given that the churn rise from a 4.2% baseline has no established cause, a rival just launched a similar program, and a funding decision is due in 3 weeks?

**Success criteria** (each checkable directly against section 6 below):

1. Section 6 states a fund / don't-fund / fund-conditionally decision that cites a derivation chain quantifying the $310,000 cost against retained revenue at 4.2%, 6.8%, and 5% churn.
2. Section 6 states whether the loyalty-program lever is verified or unverified against the churn increase's actual cause, citing the relevant chain.
3. Section 6 states whether the 5% target clears or fails a computed breakeven threshold, citing the relevant chain.
4. Section 6 separates the competitor-launch signal's evidentiary weight from any independent market-positioning rationale, citing the relevant chain.
5. Section 6 names the specific unknowns (root cause, margin, CAC, cost-estimate completeness, rival efficacy) and a data-gathering action for each that fits inside the 3-week window.

## 2. Assumptions Table

| # | Assumption | Type | Treatment | Verdict | Verification |
|---|---|---|---|---|---|
| A1 | The churn increase is driven by something a loyalty/points program can fix (value perception, switching cost) rather than product, support, pricing, cohort, or payment-failure issues | untested belief | Verify via root-cause diagnostics before/alongside funding; mark GT-N? if used unresolved | Challenge — this is the single most load-bearing gap in the proposal (used in chain C5) | unverified — flagged |
| A2 | 5% churn is the correct/sufficient target | convention (round intermediate figure between 6.8% and 4.2%) | Explicitly challenge against a derived breakeven/LTV target | Challenge — found quantitatively insufficient (chains C3, C8) | Computed directly from GT-1/GT-2/GT-3 |
| A3 | The $310,000/year cost estimate is complete (includes projected redemption/credit liability, not just admin/build cost) | untested belief | Verify with CS/Finance before approval; mark GT-N? if unresolved | Challenge — completeness unverified (used in chain C9) | unverified — flagged |
| A4 | The rival's loyalty-program launch is evidence a loyalty program is an effective retention lever and justifies matching it | convention (reflexive competitive-matching instinct) | Explicitly challenge; no analogy as direct evidence | Challenge — rejected as a churn-fix justification; timing (chain C6) and missing efficacy data (chain C7) both undercut it | unverified — flagged |
| A5 | The 6.8% aggregate churn figure is not concentrated in one cohort/channel/vintage | untested belief | Verify via cohort/vintage churn breakdown | Challenge — not established either way | unverified — flagged |
| A6 | A loyalty program's retention effect, if any, is additive to/independent of other levers (e.g., a dunning fix) | untested belief | Treat cautiously; do not assume additivity when sizing combined impact | Challenge — not testable from the data given | unverified — flagged |
| A7 | The 3-week deadline forecloses gathering any new diagnostic data before the decision | current constraint | Record expiry conditions | Accept — expires once the recommendation is reframed as staged/conditional (chain C10); the deadline binds the announcement date, not the diagnostic start date | Reasoned in chain C10 |
| A8 | Monthly churn is measured the same way (same definition/denominator) across the two compared quarters | untested belief | Verify with analytics/finance before trusting the 4.2%→6.8% delta at face value | Challenge — not stated; a definitional change could itself explain part of the rise | unverified — flagged |
| A9 | Gross revenue is the right comparison unit for the cost-vs-benefit calculation in chain C3 | untested belief, surfaced via challenge in chain C3 | Use as a deliberately conservative (benefit-favoring) floor pending real margin data | Accept — conservative simplification; refined by A12 in chain C4 | Reasoned in chain C4 |
| A10 | Retaining a member has no CAC-avoidance value beyond the $19/month counted in the naive calc | untested belief | Flag as an omitted, direction-uncertain benefit; verify with CAC data | Challenge — likely understates true benefit, magnitude unverified | unverified — flagged |
| A11 *(surfaced at chain C3, step 6)* | Gross, not margin-adjusted, revenue is a valid unit for the C3 breakeven comparison | untested belief | Accept as a conservative simplification pending GT-7? | Accept — a margin-adjusted comparison would only widen the shortfall, never close it | Reasoned in chain C4 |
| A12 *(surfaced at chain C4, step 1)* | Any real subscription business carries gross margin materially below 100%, so a revenue-only comparison understates true cost impact | convention (near-universal subscription-economics default) | Accept as a reasonable default; still verify actual margin | Accept, low risk — domain convention | Verify GT-7? with Finance |
| A13 *(surfaced at chain C5, step 1)* | A loyalty/points program can plausibly influence only voluntary cancellations, not payment-failure-driven involuntary churn | convention (standard subscription-ops distinction) | Accept as a reasonable default | Accept, low risk — domain convention | Verify GT-9? with billing/support data |

## 3. Ground Truths

- **GT-1** 48,000 active members at $19/month → MRR = $912,000; ARR = $10,944,000 — source: user-stated Context, bullet 1 ("48,000 active members, $19/month each"); read-at-source: direct arithmetic on the stated figures, this conversation.
- **GT-2** Monthly churn was 4.2% two quarters ago and is now 6.8% — source: Context, bullet 2; read-at-source: as stated.
- **GT-3** Proposed loyalty program costs ≈$310,000/year and targets ≈5% churn — source: Context, bullet 3; read-at-source: as stated.
- **GT-4** A rival launched a similar loyalty program ≈1 month before this analysis (2026-09-27) — source: Context, bullet 4; read-at-source: as stated.
- **GT-5** A funding decision is needed within 3 weeks, ahead of the next board update — source: Context, bullet 5 / Task framing; read-at-source: as stated.
- **GT-6** For a constant monthly churn rate *c*, steady-state annual retention ≈ (1−*c*)¹². This is a mathematical identity — source: direct calculation in this analysis (0.932¹² ≈ 0.4296; 0.958¹² ≈ 0.5971; 0.95¹² ≈ 0.5404); read-at-source: computed directly, verified by repeated squaring, not an external citation.
- **GT-7?** Contribution/gross margin per subscriber — unverified: not stated anywhere in the given materials.
- **GT-8?** Customer acquisition cost (CAC) — unverified: not stated.
- **GT-9?** Voluntary vs. involuntary (payment-failure) split of the churn increase — unverified: not stated.
- **GT-10?** Whether the $310,000/year cost estimate already includes projected redemption/credit liability or only program admin/build cost — unverified: not stated.
- **GT-11?** Whether the rival's own loyalty program is achieving its retention goal — unverified: no data available, and one month is too soon for even the rival to know with confidence.

**Provenance summary.**
`?`-marked: GT-7, GT-8, GT-9, GT-10, GT-11 (5 of 11).
Read-at-source (unsuffixed, feeding HIGH-confidence chains): GT-1 — Context bullet 1, direct arithmetic; GT-2 — Context bullet 2, as stated; GT-3 — Context bullet 3, as stated; GT-4 — Context bullet 4, as stated; GT-5 — Context bullet 5, as stated; GT-6 — computed directly in this analysis via repeated squaring of (1−*c*).

## 4. Derivation Chains

### Conclusion C1: The churn rise is high-stakes on its own, independent of which lever fixes it

GT-2 (churn 4.2% → 6.8%) + GT-6 (steady-state annual-retention identity)
→ holding 6.8% monthly churn steady for a year implies annual retention of only ≈43% of the current base
→ holding the prior 4.2% monthly rate steady implies annual retention of ≈60%
→ the gap between those two steady-state figures is roughly 17 points of annual retention
→ a swing of that size establishes the churn rise as high-stakes, independent of which lever eventually addresses it

**Confidence:** HIGH (GT-2 and GT-6 are both unsuffixed and read-at-source; pure arithmetic)

### Conclusion C2: Hitting the proposed 5% target retains ≈$196,992/year in gross revenue

GT-1 (MRR $912,000 = 48,000 × $19) + GT-2 (churn 4.2% → 6.8%) + GT-3 (proposed target ≈5%)
→ monthly members lost at 6.8% churn is 0.068 × 48,000 ≈ 3,264
→ monthly members lost at the proposed 5% target is 0.05 × 48,000 = 2,400
→ the difference is ≈864 fewer members lost per month if the 5% target is hit
→ 864 members/month at $19/month is ≈$16,416/month in retained gross revenue
→ annualized, that is ≈$196,992/year in retained gross revenue, on a flow-rate basis that holds the 48,000-member base constant

**Confidence:** HIGH (GT-1, GT-2, GT-3 all unsuffixed and read-at-source)

### Conclusion C3: The proposed 5% target does not clear its own breakeven bar

C2 (≈$196,992/yr retained revenue at the 5% target) + GT-3 (program costs $310,000/year)
→ the $310,000 annual cost exceeds the ≈$196,992/year retained-revenue benefit
→ the shortfall is roughly $113,000/year even if the 5% target is fully achieved
→ the churn-point reduction needed to make retained revenue equal $310,000/year is ≈1,360 members/month, from $310,000 divided by $19×12
→ 1,360 members/month is ≈2.83 points of monthly churn on the 48,000-member base
→ subtracting that from the current 6.8% rate gives a breakeven target of ≈3.97% monthly churn
→ 3.97% sits below the pre-crisis 4.2% baseline, so the proposed 5% target does not clear the pure gross-revenue breakeven bar *[Assumes: A11]*

**Confidence:** HIGH (the arithmetic rests only on GT-1/GT-2/GT-3; A11 affects interpretation, not the computation, and is stress-tested directly in C4)

### Conclusion C4: Margin and CAC data could move the case in either direction

C3 (≈$113,000/yr shortfall at target) + GT-7? (contribution margin unverified) + GT-8? (CAC unverified)
→ if gross margin is materially below 100%, as is normal for a subscription business, the true profit-basis shortfall is larger than the revenue-basis shortfall in C3 *[Assumes: A12]*
→ retaining a member also avoids a re-acquisition cost that C2/C3 do not credit, which is an omitted benefit pointing the other way
→ because GT-7? and GT-8? are both unverified, the net direction and size of the fully-loaded economic case cannot be pinned down from the numbers given
→ the C3 comparison stands as a conservative floor on the cost-side shortfall, not a complete picture, until GT-7?/GT-8? are resolved

**Confidence:** MEDIUM — this chain's conclusion depends on GT-7? and GT-8?; pulling actual contribution margin and CAC from Finance would raise this to HIGH in whichever direction the resolved figures point

### Conclusion C5: The lever's fit to the actual problem is unverified

GT-2 (churn rose 2.6 points, a ≈62% relative increase) + GT-9? (voluntary/involuntary split unverified)
→ a loyalty program can plausibly influence only voluntary, value-perception-driven cancellations *[Assumes: A13]*
→ it cannot plausibly influence involuntary churn caused by failed payments or expired cards
→ because the voluntary/involuntary split is unverified, it is not established that the proposed lever addresses the mechanism behind the rise, or even a majority share of it
→ this is the most load-bearing unverified input in the proposal, and a diagnostic on the same timeline as the funding decision would resolve it

**Confidence:** LOW — this chain's conclusion depends directly on GT-9?; a cohort/exit-survey/payment-failure audit resolving GT-9? would raise this to HIGH

### Conclusion C6: The rival's program cannot be the primary cause of most of the churn rise

GT-2 (churn began rising two quarters ago) + GT-4 (rival's program launched one month ago)
→ the churn rise predates the rival's program launch by roughly five months
→ the rival's program therefore cannot be the primary driver of most of the observed increase
→ it could still be a marginal contributor to the most recent month, but no month-by-month churn breakdown exists to isolate that

**Confidence:** HIGH (GT-2 and GT-4 are both unsuffixed and read-at-source)

### Conclusion C7: "The rival launched one" is not evidence a loyalty program works

C6 (rival's program postdates most of the churn rise) + GT-11? (rival's program efficacy unverified)
→ no data exists on whether the rival's own program is achieving its own retention goal
→ treating the rival's launch as evidence that a loyalty program works is reasoning by analogy, not evidence, and is inadmissible as direct justification for funding this program
→ a separate market-positioning rationale for a loyalty program may still exist, but it carries a different cost-benefit basis and should not be conflated with a churn-fix justification

**Confidence:** MEDIUM — this chain includes GT-11?; obtaining any performance read on the rival's program (public disclosure, review sentiment, competitive intel) would raise this to HIGH without altering C6's timing finding

### Conclusion C8: The 5% target should be derived from economics, not picked as a round number

GT-3 (proposed target ≈5%) + C3 (breakeven target ≈3.97%)
→ 5% sits between the current 6.8% and the historical 4.2%, with no stated derivation for that specific value
→ 5% is measurably short of the ≈3.97% breakeven target derived in C3
→ even a fully successful program, by the proposal's own stated target, would not recover its cost on a gross-revenue basis
→ the target should instead be derived from breakeven or LTV-optimal economics once margin and CAC are known, not selected as a round intermediate figure

**Confidence:** HIGH (follows directly from C3's arithmetic; the "no stated derivation" finding is a direct read of GT-3 as given)

### Conclusion C9: Funding without fixing the root cause compounds cost and delay

C5 (root cause unverified) + GT-3 (program funded regardless) + GT-10? (redemption-liability completeness unverified)
→[2nd] if the program is funded without addressing the true root cause, the annual cost is spent while the underlying driver of the rise continues unresolved
→[2nd] a growing redeemable-points liability is created on the books, requiring breakage/redemption accounting that the $310,000 admin-cost figure may not capture, because GT-10? is unverified
→[3rd] a second remediation cycle becomes necessary after the first program under-delivers, compounding total spend and delaying the real fix by a quarter or more
→ none of these extension steps contradicts a Ground Truth, so this second-order pass does not trigger a return to Phase 2

**Confidence:** MEDIUM — this chain includes GT-10?; obtaining the cost estimate's line-item breakdown from Finance/CS would raise this to HIGH

### Conclusion C10: A staged decision is deliverable inside the 3-week window

GT-5 (funding decision needed within 3 weeks) + GT-2 (churn already elevated for two quarters)
→ the 3-week deadline binds the date a decision is announced to the board, not the date evidence-gathering can begin
→ voluntary/involuntary split, cohort breakdown, margin, and CAC data can be pulled from existing systems within days, in parallel with board-prep work, since none require new instrumentation
→ a staged recommendation — fund a limited pilot, or defer full funding pending this diagnostic — is deliverable inside the 3-week window without waiting on a full root-cause study
→ this resolves the apparent conflict between "decide in 3 weeks" and "the root cause is unverified" (chain C5): the decision made in 3 weeks can be conditional rather than final

**Confidence:** HIGH (GT-5 and GT-2 are both unsuffixed and read-at-source; the feasibility claim is a direct read of the given deadline structure)

## 5. Abandoned Reasoning

### Dead End: Using undiscounted stock-based LTV uplift as the primary economic case

**What was tried:** Computing customer lifetime value at each churn rate via the standard undiscounted identity LTV ≈ ARPU/churn (drawing on GT-1 and GT-2's rate figures) — at 6.8% churn, implied lifetime ≈14.7 months (LTV ≈$279); at 5%, ≈20 months (LTV ≈$380); a per-customer delta of ≈$100.6, or ≈$4.83M applied across the 48,000-member base.

**Why abandoned:** This treats a one-time stock revaluation (the LTV uplift, assuming the lower churn rate holds for the customer base's entire remaining lifetime) as comparable to a recurring annual cost ($310,000/year, paid every year to sustain the new equilibrium). The two are not the same unit: sustaining the LTV uplift requires paying $310,000/year in perpetuity, so the correct comparison is recurring cost vs. recurring benefit (chain C2/C3's flow-rate framing), not recurring cost vs. one-time stock revaluation. Using the stock figure would have overstated the case for funding by roughly 25x.

**What it ruled out:** Any future comparison should default to a per-year, per-year comparison against this recurring cost, not a lifetime-value stock figure — the mismatch in units is the specific defect, not merely "the number seemed too good."

### Dead End: Treating the rival's launch as sufficient standalone justification

**What was tried:** Reasoning "a competitor just launched something similar, so we should too, and soon" as a direct justification for funding.

**Why abandoned:** This is reasoning by analogy without grounding in a verified fact about the rival's own results — exactly the pattern this methodology treats as inadmissible direct evidence. Chain C6 also shows the timing doesn't support "their program is why our churn rose" as the primary explanation, since our churn rise predates their launch by roughly five months.

**What it ruled out:** "Match the competitor" is not, by itself, evidence the lever fixes the actual problem. It survives only as a separate, explicitly-labeled market-positioning consideration (chain C7), not as part of the churn-fix cost-benefit case.

### Dead End: Accepting the CS-proposed 5% target without independent derivation

**What was tried:** Taking "5%" at face value as a reasonable, already-vetted target, since it sits between the current 6.8% and the historical 4.2%.

**Why abandoned:** Chain C3 shows the pure gross-revenue breakeven point is ≈3.97% — below the pre-crisis baseline — so 5%, even if fully achieved, does not recover the $310,000 annual cost. The target's plausibility as a "reasonable midpoint" does not survive contact with the arithmetic.

**What it ruled out:** Any board-facing target for this initiative should be re-derived from breakeven/LTV economics (chain C8) rather than restated as CS's original 5% figure.

### Dead End: Deferring any recommendation until a full root-cause study is complete

**What was tried:** Concluding that because GT-7? through GT-11? are all unverified, the only responsible answer is "we cannot recommend anything until a full study is done."

**Why abandoned:** This is non-responsive to GT-5 (the 3-week deadline is a real current constraint, A7) and treats the deadline as unconditionally binding evidence-gathering rather than only the announcement date. Chain C10 shows a staged/conditional recommendation is achievable inside the window without waiting on a full study.

**What it ruled out:** "Wait for perfect data" is not a valid answer here; the correct response is a conditional recommendation plus a fast, parallel diagnostic (chain C10), not silence or indefinite delay.

## 6. Conclusion

**Recommended approach:** Do not fund the $310,000/year loyalty program as proposed, in its current form, within the 3-week window. Instead, approve a parallel diagnostic — voluntary/involuntary churn split, cohort/vintage breakdown, contribution margin, and CAC — to run over the same 3 weeks, and bring the board either a conditional deferral or a scaled-down pilot rather than a full commitment (chains C3, C8, C10).

**Key insight:** Even in the CS proposal's own best case — hitting exactly the stated 5% target — the program's gross-revenue-retention benefit (≈$196,992/year) does not cover its ≈$310,000/year cost; the actual breakeven churn rate is ≈3.97%, below the pre-crisis 4.2% baseline. The proposal's own target is quantitatively insufficient before root-cause, margin, or CAC uncertainty is even considered (chains C3, C8).

**Trade-offs acknowledged:** Delaying full funding for a 3-week diagnostic forgoes the fast, visible, competitor-matching response marketing wants for the board update, and leaves whatever near-term competitive pressure the rival's move creates unaddressed for a few more weeks (chains C6, C7). Conversely, funding the full program immediately risks committing $310,000/year to a lever that misses its own breakeven bar and may not touch the true driver of the churn rise, which remains unverified (chains C3, C5, C9). Both paths carry real downside; this recommendation accepts the smaller, bounded downside of a short parallel diagnostic delay over the larger, less-bounded downside of funding an under-sized fix for an unverified cause (chain C10).

**Confidence:** MEDIUM — the "economics don't clear breakeven" and "timing rules out the rival's program as the primary cause" findings are HIGH-confidence (chains C1, C2, C3, C6, C8, C10, resting only on unsuffixed, read-at-source ground truths). The overall rating is held to MEDIUM rather than HIGH because the recommendation's supporting case also leans on GT-7? (margin), GT-8? (CAC), GT-9? (voluntary/involuntary split), GT-10? (redemption-liability completeness), and GT-11? (rival efficacy), all unverified (chains C4, C5, C7, C9). Verifying any of these five — pulling margin and CAC from Finance, a payment-failure/voluntary split from billing and support data, redemption-cost line items from CS/Finance, and any public read on the rival's results — would raise the corresponding chain, and eventually the overall rating, to HIGH.

---

## Process output: End-of-phase Assumption Audit (Phase 4)

| Chain | Step | Step Text (brief) | Assumption surfaced? | Added to Table? |
|---|---|---|---|---|
| C1 | 1 | 6.8% steady → ≈43% annual retention | none | n/a |
| C1 | 2 | 4.2% steady → ≈60% annual retention | none | n/a |
| C1 | 3 | gap ≈17 pts annual retention | none | n/a |
| C1 | 4 | stakes established, doesn't pick lever | none | n/a |
| C2 | 1 | members lost/mo at 6.8% ≈3,264 | none | n/a |
| C2 | 2 | members lost/mo at 5% = 2,400 | none | n/a |
| C2 | 3 | difference ≈864/mo | none | n/a |
| C2 | 4 | 864×$19 ≈$16,416/mo | none | n/a |
| C2 | 5 | annualized ≈$196,992/yr | none | n/a |
| C3 | 1 | $310k > $196,992 benefit | none | n/a |
| C3 | 2 | shortfall ≈$113k/yr | none | n/a |
| C3 | 3 | breakeven needs ≈1,360 members/mo | none | n/a |
| C3 | 4 | 1,360 ≈2.83 churn points | none | n/a |
| C3 | 5 | breakeven target ≈3.97% | none | n/a |
| C3 | 6 | 3.97% < 4.2% baseline, 5% doesn't clear bar | A11 (gross revenue is a valid comparison unit) | yes |
| C4 | 1 | margin <100% → true shortfall larger | A12 (subscription businesses carry margin <100%) | yes |
| C4 | 2 | CAC-avoidance omitted benefit, other direction | none | n/a |
| C4 | 3 | GT-7?/GT-8? unverified → net size unresolved | none | n/a |
| C4 | 4 | C3 is a floor, not complete picture | none | n/a |
| C5 | 1 | loyalty program affects only voluntary churn | A13 (loyalty programs affect only voluntary churn) | yes |
| C5 | 2 | cannot affect involuntary/payment-failure churn | none | n/a |
| C5 | 3 | split (GT-9?) unverified → lever fit unverified | none | n/a |
| C5 | 4 | most load-bearing gap; diagnostic would resolve | none | n/a |
| C6 | 1 | churn rise predates rival launch by ≈5 months | none | n/a |
| C6 | 2 | rival's program can't be primary driver of most of the rise | none | n/a |
| C6 | 3 | could be marginal contributor to latest month only | none | n/a |
| C7 | 1 | no data on rival's own program efficacy (GT-11?) | none | n/a |
| C7 | 2 | treating launch as evidence is analogy, inadmissible | none | n/a |
| C7 | 3 | separate market-positioning rationale possible | none | n/a |
| C8 | 1 | 5% is an underived round intermediate figure | none | n/a |
| C8 | 2 | 5% falls short of ≈3.97% breakeven | none | n/a |
| C8 | 3 | full success still wouldn't recover cost | none | n/a |
| C8 | 4 | target should be re-derived from economics | none | n/a |
| C9 | 1 | [2nd] funding without fix spends while driver persists | none | n/a |
| C9 | 2 | [2nd] points liability needs accounting, GT-10? unverified | none | n/a |
| C9 | 3 | [3rd] second remediation cycle compounds spend/delay | none | n/a |
| C9 | 4 | no contradiction of a Ground Truth, no return to Phase 2 | none | n/a |
| C10 | 1 | 3-week deadline binds announcement date only | none | n/a |
| C10 | 2 | diagnostic data pullable within days, in parallel | none | n/a |
| C10 | 3 | staged recommendation deliverable inside 3 weeks | none | n/a |
| C10 | 4 | resolves conflict between deadline and unverified root cause | none | n/a |

Table confirmed exhaustive: 41 rows, one per chain step across C1–C10, no step skipped. A11–A13 surfaced here are already reflected as rows in section 2's Assumptions Table above.

## Process output: §6→§4 closure ledger

- "Do not fund the $310,000/year loyalty program as proposed... approve a parallel diagnostic... conditional deferral or a scaled-down pilot" → chains C3, C8, C10 ✓ (cited inline)
- "Even in the CS proposal's own best case... the actual breakeven churn rate is ≈3.97%..." → chains C3, C8 ✓ (cited inline)
- "Delaying full funding... risks committing $310,000/year to a lever that misses its own breakeven bar..." → chains C6, C7, C3, C5, C9, C10 ✓ (cited inline)
- "Confidence: MEDIUM — ... chains C1, C2, C3, C6, C8, C10 ... chains C4, C5, C7, C9" → chains C1, C2, C3, C4, C5, C6, C7, C8, C9, C10 ✓ (cited inline)

All four section-6 claims carry inline chain citations; no claim required a ledger-only discharge; nothing was cut.

## Self-audit scan (process output)

**Table 1 — chain form (section 4)**

| Chain | Chain Head (brief) | Form conforming? | Rule applied | Dependency clean? |
|---|---|---|---|---|
| C1 | GT-2 + GT-6 | yes | n/a | yes |
| C2 | GT-1 + GT-2 + GT-3 | yes | n/a | yes |
| C3 | C2 + GT-3 | yes | n/a | yes |
| C4 | C3 + GT-7? + GT-8? | yes | n/a | yes |
| C5 | GT-2 + GT-9? | yes | n/a | yes |
| C6 | GT-2 + GT-4 | yes | n/a | yes |
| C7 | C6 + GT-11? | yes | n/a | yes |
| C8 | GT-3 + C3 | yes | n/a | yes |
| C9 | C5 + GT-3 + GT-10? | yes | n/a | yes |
| C10 | GT-5 + GT-2 | yes | n/a | yes |

**Table 2 — claim inventory (section 6)**

| §6 Span (brief) | Construct | Claim under R11? | R11 clause applied | Chain cited |
|---|---|---|---|---|
| "Recommended approach: Do not fund..." | bold lead-in | yes | colon closes bold span, carries its own assertion | C3, C8, C10 |
| "Key insight: Even in the CS proposal's own best case..." | bold lead-in | yes | colon closes bold span, carries its own assertion | C3, C8 |
| "Trade-offs acknowledged: Delaying full funding..." | bold lead-in | yes | colon closes bold span, carries its own assertion | C6, C7, C3, C5, C9, C10 |
| "Confidence: MEDIUM — the 'economics don't clear breakeven'..." | bold lead-in | yes | colon closes bold span, carries its own assertion | C1, C2, C3, C4, C5, C6, C7, C8, C9, C10 |

Scan complete: 10 chain rows, one per section-4 chain block in order; 4 section-6 rows, one per construct in order — 4 claims under R11, 0 excluded. 0 chains malformed, 0 claims untraced.

## Self-Audit Gate

**Criterion 1: Identify Essence**
Quoted span: "Should the company commit ≈$310,000/year to a loyalty/points program on the bet that it will pull monthly churn from 6.8% back toward ≈5%, given that the churn rise from a 4.2% baseline has no established cause, a rival just launched a similar program, and a funding decision is due in 3 weeks?"
Band: **Rigorous**
Justification: The statement names the core decision (not the triggering event alone) and is followed by five success criteria, each a verb+subject+outcome triplet checkable directly against section 6 without further interpretation.

**Criterion 2: Challenge Assumptions**
Quoted span: from the Assumption Audit scan — "C3 | 6 | ... 3.97% < 4.2% baseline, 5% doesn't clear bar | A11 (gross revenue is a valid comparison unit) | yes" and "C5 | 1 | loyalty program affects only voluntary churn | A13 ... | yes"
Band: **Rigorous**
Justification: All 13 rows use the four-type scheme, Verdict cells lead with Accept/Challenge and an em-dash justification, unverified-and-used assumptions carry "unverified — flagged" verbatim, at least six assumptions are Challenged (not merely Accepted), and the Assumption Audit scan confirms the end-of-phase surfacing (A11–A13) ran exhaustively over all 41 chain steps.

**Criterion 3: Establish Ground Truths**
Quoted span: "?-marked: GT-7, GT-8, GT-9, GT-10, GT-11 (5 of 11)." — checked against the Ground Truths list, which carries `?` on exactly those five IDs and no others.
Band: **Rigorous**
Justification: All 11 GT-IDs are stable and referenced consistently in section 4; every unsuffixed GT (1–6) names a read-at-source location and each feeds at least one HIGH-confidence chain (GT-1→C2, GT-2→C1, GT-3→C2, GT-4→C6, GT-5→C10, GT-6→C1); the `?` enumeration matches the list exactly.

**Criterion 4: Reason Upward**
Quoted span: from the self-audit scan Table 1 — all ten rows read "Form conforming? yes ... Dependency clean? yes"; plus, from the analysis text, chain C7's hop "treating the rival's launch as evidence that a loyalty program works is reasoning by analogy, not evidence, and is inadmissible as direct justification."
Band: **Rigorous**
Justification: Every chain is head-plus-arrow-form with genuine intermediates and clean dependencies per the scan; the Abandoned Reasoning section documents four real dead ends in the prescribed What-was-tried/Why-abandoned/What-it-ruled-out structure (no escape valve needed); the analogy ban is applied explicitly rather than violated; every chain step that introduced a new assumption (C3 step 6, C4 step 1, C5 step 1) carries an inline `[Assumes: X]` tag matching the Assumption Audit scan.

**Criterion 5: Validate**
Quoted span: "The overall rating is held to MEDIUM rather than HIGH because the recommendation's supporting case also leans on GT-7? ... GT-8? ... GT-9? ... GT-10? ... and GT-11? ... all unverified (chains C4, C5, C7, C9)."
Band: **Sound**
Justification: Every GT-N? input is named with its causing chain and a specific verification path to HIGH, and no chain consuming a GT-N? input is rated HIGH — but the overall Conclusion confidence is honestly stated as MEDIUM rather than HIGH, and per this rubric's own text a MEDIUM overall rating is "not... Rigorous on Criterion 5" even when every individual claim traces to at least one HIGH chain, so this bands Sound rather than Rigorous.

**Criterion 6: Conclusion-to-Ground-Truth Traceability**
Quoted span: from the self-audit scan Table 2 — all four rows read "Claim under R11? yes" with a non-empty "Chain cited" column ("C3, C8, C10"; "C3, C8"; "C6, C7, C3, C5, C9, C10"; "C1–C10").
Band: **Rigorous**
Justification: Every section-6 claim traces to specific, named section-4 chains with no new reasoning introduced in section 6, and the Key Insight (the 5% target itself falls short of the ≈3.97% breakeven point, below the pre-crisis baseline) is a non-obvious finding that reasoning by convention would have missed, not a restatement of the recommended approach.

**Gate result:** No criterion scored Absent (condition 1 cleared); zero criteria scored Hand-wavy, well under the one-Hand-wavy cap (condition 2 cleared). **The analysis clears the Self-Audit Gate.** No Fix/Repeat pass was required.