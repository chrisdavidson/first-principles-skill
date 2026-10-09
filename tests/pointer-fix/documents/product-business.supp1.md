## Answer

**Recommendation:** Run a small, private, sales-assisted pilot — free or heavily discounted access for roughly 15-25 ICP-matched prospects sourced through the existing outbound/referral motion, tracked for 90-180 days — before committing any engineering resources to a public self-serve or freemium build (chain C4).

**Band (from §6):** LOW

**Would change it:** Running the pilot itself — it replaces the assumed per-free-user cost and value estimates with measured ones (chain C1) and directly tests whether the free/pilot activator reaches the budget holder (chain C4), the single biggest open question behind the LOW band.

## 1. Problem Essence

**Core problem:** Given zero internal data on free-to-paid conversion, a confirmed real marginal cost per free active user, and an unvalidated "competitors have it" argument, should this company commit engineering and support resources to build a permanent free tier as its mechanism for creating a self-serve/inbound acquisition channel it currently lacks?

**Success criteria:**
- The answer identifies whether a $0 price point is actually the binding constraint on building a self-serve/inbound channel, or whether the absence of any self-serve activation path (which a free tier is only one way to fix) is the real constraint.
- The answer states whether the marginal infra+support cost of free users (confirmed real by Finance) is, by itself, economically prohibitive at plausible conversion rates, with the reasoning shown.
- The answer evaluates a free tier against at least one concrete alternative mechanism for the same goal (not just "free tier: yes or no"), including a composite/staged option.
- The answer names a minimal, low-cost validation step — if any — that should happen before a full freemium build-out is funded, and what result from that step would change the recommendation.
- The answer is usable by a founder/exec for a go/no-go decision this quarter: a clear recommendation, the strongest reasoning, the single biggest risk, and the trigger for revisiting the decision.

## 2. Assumptions Table

| Assumption | Type | Treatment | Verdict | Verification |
|------------|------|-----------|---------|--------------|
| A1. Competitors having a free tier means we need one too | convention | Explicitly challenge before use | Challenge — competitive parity is unvalidated as causal (GT-5?); the company already generates $2.4M ARR without a free tier (GT-1?, GT-2?); demoted to a secondary, non-load-bearing motivation (chain C3) | unverified — flagged |
| A2. A free tier will fix our lack of an inbound/self-serve channel | untested belief | Verify or flag unverified | Challenge — the 5-whys reduction (chain C2) shows the root cause is "no self-serve activation path exists at all," of which a permanent free tier is only one of several candidate fixes; conflating the fix with the goal is the error this assumption encodes | unverified — flagged |
| A3. Free users will convert to paid at a workable rate | untested belief | Verify or flag unverified | Challenge — no internal data exists (GT-4?); external benchmarks (GT-6, GT-7) range 2-20% depending heavily on segment and ACV, and this company's ACV sits above the typical benchmarked ARPC, so applicability is uncertain | unverified — flagged; verification path = the recommended pilot |
| A4. A permanent $0 free tier is the only/best way to build a self-serve channel | convention | Explicitly challenge before use | Challenge — the trade-off analysis (chain C4) shows a sales-assisted limited pilot dominates a full freemium build on cost, speed, risk, and reversibility; a time-boxed free trial or low-priced self-serve starter plan are also live, untested alternatives | unverified — flagged |
| A5. Infra + support costs scale with active (not paying) users — free users carry a real marginal cost | current constraint | Record expiry conditions | Accept — stated as confirmed by Finance; treated as a cost-structure constraint of today's architecture and billing model. Expires if the product is re-architected so free-tier resource consumption is decoupled from active-user count (e.g., aggressive per-tenant cost capping or near-zero marginal-cost infra at scale) | unverified — flagged (no Finance cost-model document was opened by this analysis) |
| A6. No internal freemium pilot has been run; no internal conversion data exists | current constraint | Record expiry conditions | Accept — stated as current fact. Expires the moment a pilot (recommended in §6) produces real conversion data; this is the specific gap the recommendation closes | unverified — flagged |
| A7. The company has spare engineering capacity/budget to build full self-serve signup, billing, metering, and upgrade infrastructure without displacing other roadmap commitments | untested belief | Verify or flag unverified | Challenge — not evidenced either way; a full freemium build-out is a nontrivial multi-quarter engineering investment (chain C4) the prompt does not confirm is funded or staffed | unverified — flagged |
| A8. The person who self-activates on free/low-commitment access is the same person, or has a credible path to the person, who holds budget authority for a ~$10k/year team purchase | untested belief | Verify or flag unverified; stakes-escalation applies | Challenge — the single highest-stakes assumption in this analysis: if false, no volume of free-tier signups converts to revenue, because the activator cannot authorize the spend. Surfaced independently by inversion (precondition P3) and by the pre-mortem's Cluster A | unverified — flagged; verification path = the recommended pilot, explicitly tracking signup-role vs. buyer-role |
| A9. All competitors' free tiers are causally linked to their market success (not merely correlated or cargo-culted) | convention | Explicitly challenge before use | Discard — the user explicitly states this causal link is unvalidated (GT-5?), and chain C3 shows the company's own growth is not evidently blocked by its absence; retained only as a cheap secondary diagnostic (win-loss interviews), never as a load-bearing reason to build | unverified — flagged |
| A10. The company's ICP buyers currently fail to find/evaluate the product because of channel-type (no self-serve path), not because of other factors (brand awareness, SEO/content presence, sales capacity) | untested belief | Verify or flag unverified | Challenge — plausible but unexamined; reaching $2.4M ARR via outbound+referral alone (GT-1?, GT-2?) is equally consistent with an ICP that is inherently low-volume/high-touch, in which case no channel-type fix would meaningfully grow inbound volume | unverified — flagged |
| A11. GT-6's benchmark sample's ARPC ($50-249/mo) transfers to this company's ~$10k/yr ACV *(surfaced in chain C1, step 2)* | untested belief | Verify or flag unverified | Challenge — unexamined; this company's considered, team-based purchase is structurally unlike the benchmark sample's typical low-ACV self-serve buyer | unverified — flagged; verification path = the pilot's own measured conversion rate for this company's actual ICP |
| A12. A $0 price point specifically removes a trust/budget-risk barrier that a time-boxed trial does not *(surfaced in chain C2, step 1)* | untested belief | Verify or flag unverified | Challenge — unexamined rival to A2/A4; no evidence distinguishes "must be free" from "must be low-friction and self-serve" | unverified — flagged; verification path = compare pilot engagement against any future trial/freemium test |
| A13. GT-1?'s 240-paying-team count is not subject to survivorship bias from prospects who self-selected out before ever entering the outbound pipeline *(surfaced in chain C3, step 1)* | untested belief | Verify or flag unverified | Challenge — unexamined and plausible; current ARR could already understate lost demand attributable to lacking a free tier | unverified — flagged; verification path = win-loss / lost-deal interviews asking specifically about free-tier absence |
| A14. The locked trade-off criteria weights (cost-to-validate, time-to-signal, risk-to-existing-motion, optionality, brand risk, goal-achievement) reflect this company's actual risk tolerance and strategic priorities *(surfaced in chain C4, step 1)* | convention | Explicitly challenge before use | Challenge — a judgment convention adopted for this analysis; the flip-test shows the ranking is robust to any single-weight change within the locked 1-5 scale, but the weights themselves were set by this analysis, not ratified by the founder/exec team | unverified — flagged; verification path = founder/exec team reviews and ratifies or adjusts the weights |
| A15. A small, sales-assisted pilot stays genuinely invisible to competitors and the broader market *(surfaced in chain C5, step 1)* | current constraint | Record expiry conditions | Accept — true only while the pilot stays small and private. Expires if pilot slots are publicized, referenced in marketing, or scaled beyond a handful of design partners, at which point the competitive-reaction risk modeled for a full public tier reapplies | unverified — flagged |

## 3. Ground Truths

- **GT-1?** ARR = $2.4M from 240 paying teams, averaging ~$10,000/team/year — unverified: user-supplied internal figure; no external source was opened by this analysis; verification path: the company's own billing/CRM system
- **GT-2?** Current acquisition channels are outbound sales and referrals only; no self-serve/inbound channel exists today — unverified: user-supplied
- **GT-3?** Finance has confirmed free-tier infra and support costs scale with active (not paying) users, i.e., every free user carries a real, nonzero marginal cost — unverified: user-supplied; no Finance cost-model document was opened by this analysis; verification path: that cost model directly
- **GT-4?** No internal freemium pilot has ever been run; no internal free-to-paid conversion data exists — unverified: user-supplied; this absence is the specific gap the recommended pilot (chain C4) closes
- **GT-5?** All current competitors have a free tier; the causal link between that free tier and their market success is explicitly not established — unverified: user-supplied, and the causal gap is acknowledged by the user's own framing
- **GT-6** ChartMogul SaaS Conversion Report (survey of 200 B2B software products, fielded January 2026; respondent profile: ARR $1-10M, average revenue per customer $50-$249/month, 25-50% YoY growth): general freemium conversion = 3-5% at the 50th percentile ("good"), 8-12% at the 75th percentile ("great"); B2B-focused subset = 6-10% ("good"), 15-20% ("great"); conversion window defined as free signup to paying customer within 6 months — source: chartmogul.com/reports/saas-conversion-report/; read-at-source: "Freemium Conversion Rate Benchmarks" and "Methodology Notes" sections, fetched directly 2026-10-09
- **GT-7** First Page Sage analysis of 80+ SaaS clients using a freemium model, 2022-2026, across 15 industries: freemium-to-paid conversion rate median ≈3.9% across industries (range 2.1%-5.6%); by model subtype: Traditional Freemium 3.4%, Land & Expand 3.7%, Freeware 2.0 3.5% — source: firstpagesage.com/seo-blog/saas-freemium-conversion-rates/; read-at-source: "Methodology" and "Average Freemium-to-Paid Conversion Rate" sections, fetched directly 2026-10-09
- **GT-8** Break-even identity (derived definition, not sourced): for a free tier whose marginal serving cost scales with active users (per GT-3?), the free-to-paid conversion rate r required to break even on that marginal cost alone satisfies r_breakeven = c / V, where c = marginal infra+support cost per free active user over a measurement window and V = gross-margin value captured from one converted customer over the same window — a tautological accounting identity, not an empirical claim, so it carries no `?` and no source to read
- **GT-9?** Estimated marginal infra+support cost per free active user, per year: bracket $15 (low) to $275 (high), central ≈$70 — assumed/estimated: a Fermi bracket built from general SaaS per-user hosting/compute cost ranges (≈$10-$200/yr) plus free-tier support-ticket-handling cost ranges (≈$5-$75/yr); not a measured company-specific figure; no document from the company's own Finance cost model was opened by this analysis
- **GT-10?** Estimated gross-margin value captured per converted paying customer in year 1: $10,000 ACV (GT-1?) × 65-85% gross margin ≈ $6,500-$8,500, central ≈$7,500 — assumed/estimated: derived from GT-1? and a typical SaaS gross-margin range; the company's actual gross margin was not confirmed by this analysis

**Provenance summary:** `?`-marked: GT-1, GT-2, GT-3, GT-4, GT-5, GT-9, GT-10 (7 of 10). Read-at-source: GT-6 — chartmogul.com/reports/saas-conversion-report/, "Freemium Conversion Rate Benchmarks" + "Methodology Notes" sections. GT-7 — firstpagesage.com/seo-blog/saas-freemium-conversion-rates/, "Methodology" + "Average Freemium-to-Paid Conversion Rate" sections. GT-8 is a derived definitional identity and carries no source to read. GT-6 and GT-7 each feed a HIGH-confidence chain (chain C6), and both are named above with their read-at-source location, satisfying the HIGH-chain read-at-source obligation for every unsuffixed ground truth in this analysis.

## 4. Derivation Chains

### Conclusion C1: The marginal infra+support cost of serving free users is, by itself, unlikely to be the deciding factor against a free tier — but this is not fully settled

GT-8 (break-even identity) + GT-9? (free-user cost estimate, $15-$275/yr) + GT-10? (converted-customer value estimate, $6,500-$8,500/yr)
→ the break-even conversion rate on marginal cost alone brackets to about 0.18% at the low-cost/high-value end and 4.23% at the high-cost/low-value end, central roughly 0.93%
→ observed freemium conversion rates across segments in GT-6 and GT-7 (3.4%-20%) sit at or above the high end of that break-even bracket in every reported segment *[Assumes: A11 — GT-6's benchmark sample's ARPC transfers to this company's higher ACV]*
→ the marginal cost of serving free users is therefore not, by itself, a sufficient reason to reject a free tier

**Pre-check:** head GT-8, GT-9?, GT-10?, GT-6, GT-7 · ?-marked: GT-9?, GT-10? · lowest cited: none · Inputs ceiling: MEDIUM
**Confidence:** LOW — two axes are short. Inputs: GT-9? (free-user cost estimate) and GT-10? (converted-customer value estimate) are both assumed Fermi brackets, not measured figures; verification = replace both with Finance's actual per-user cost model and the company's actual gross margin. Rivals: a live rival is not settled — if this company's real free-to-paid conversion rate (untested, GT-4?) comes in below the pessimistic break-even bound (4.23%) because its higher ACV (GT-1?, ~$10k/yr vs. GT-6's benchmark sample at $600-$3,000/yr ARPC) makes self-serve conversion structurally harder than the benchmarked population (A11), the cost argument flips and infra+support cost could become a real deciding factor; nothing in this analysis settles which reading is correct. What would close both gaps: the pilot recommended in §6, which measures this company's actual r, c, and V directly rather than relying on benchmark transfer.

### Conclusion C2: "Add a free tier" conflates a specific tactic with the actual root cause of the missing inbound channel

GT-2? (no self-serve/inbound channel exists today)
→ applying the counterfactual test, had the company instead offered a self-serve free trial or a low-priced starter plan, the "no inbound channel" symptom would very likely not have persisted
→ the absence of any self-serve activation path, not the absence of a $0 price point, is therefore the more necessary condition *[Assumes: A12 — a $0 price point specifically removes a trust/budget-risk barrier that a time-boxed trial does not]*
→ treating "add a permanent free tier" as the fix conflates one candidate tactic with the actual root cause, which admits several candidate fixes of different cost and risk

**Pre-check:** head GT-2? · ?-marked: GT-2? · lowest cited: none · Inputs ceiling: MEDIUM
**Confidence:** LOW — two axes are short. Inputs: GT-2? is an unverified, user-supplied fact; verification = confirm directly against the company's own marketing/sales-ops records that no self-serve signup path of any kind (trial, low-price, or free) has ever existed. Rivals: a live rival (A12) is not settled — it is possible this company's specific buyers treat "free" as categorically different from "cheap and self-serve" for reasons a trial does not address (e.g., risk-averse procurement treating any paid trial as a commitment); nothing in this analysis distinguishes the two readings. What would close it: compare engagement/conversion on the recommended pilot (which is sales-assisted, not $0) against any future trial or freemium test, once run.

### Conclusion C3: Competitive parity ("they have one, so must we") is the weakest of the four motivations and should not, alone, justify a full build

GT-1? (ARR $2.4M / 240 teams via outbound+referral) + GT-2? (no self-serve channel exists) + GT-5? (all competitors have a free tier; causal link unvalidated)
→ the company's current growth to $2.4M ARR was achieved with no free tier at all, so lack of a free tier is not evidently blocking the growth already realized *[Assumes: A13 — GT-1?'s 240-team count is not subject to survivorship bias from prospects who self-selected out before entering the pipeline]*
→ competitive parity is therefore a weak, non-load-bearing justification on its own for a multi-quarter engineering investment

**Pre-check:** head GT-1?, GT-2?, GT-5? · ?-marked: GT-1?, GT-2?, GT-5? · lowest cited: none · Inputs ceiling: MEDIUM
**Confidence:** LOW — two axes are short. Inputs: all three head ground truths are unverified, user-supplied figures with no external source opened by this analysis; verification = GT-1?/GT-2? against the company's own CRM/billing records, GT-5? against an actual competitor audit. Rivals: a live rival (A13, survivorship bias) is not settled — the 240-team figure could already understate demand lost to competitors specifically because this company lacks a free tier, if prospects who wanted free access never entered the outbound pipeline at all and so never show up in any internal count; nothing in this analysis observes that silent population. What would close it: win-loss or lost-deal interviews that specifically ask lost prospects whether free-tier absence factored into their choice — a cheap diagnostic that can be folded into the recommended pilot's scope.

### Conclusion C4: A limited, sales-assisted pilot is the correct next action — not a full freemium build, and not staying the course

C1 (LOW — cost is not clearly prohibitive, but unsettled) + C3 (LOW — competitive parity is weak, but unsettled)
→ scoring four options (status quo, full freemium, free trial, limited pilot) against six locked, weighted criteria (cost to validate, time to signal, risk to existing motion, optionality, brand risk, goal-achievement) produces a weighted total for each option
→ the weighted totals are 88 (status quo), 55 (full freemium), 74 (free trial), and 112 (limited pilot)
→ the limited pilot weakly dominates the status quo, beats the full-freemium and free-trial options on five of six criteria, and loses only on direct goal-achievement
→ a flip-test confirms this is robust: reversing the pilot's win over full-freemium would require raising the goal-achievement weight to roughly 32 on a locked 1-5 scale *[Assumes: A14 — the locked criteria weights reflect this company's actual risk tolerance and priorities]*
→ the correct next action is therefore the limited, sales-assisted pilot, with the full-build decision deferred until the pilot produces real data

**Pre-check:** head C1 (LOW), C3 (LOW) · ?-marked: none directly · lowest cited: LOW · Inputs ceiling: LOW
**Confidence:** LOW — capped by the lowest-rated chain this chain's head cites (C1 and C3 are both LOW), per the unverified-input ceiling rule. The dominance argument itself (weak dominance over the status quo; a flip-test requiring an implausible weight change to reverse the win over full-freemium and free-trial) is robust independent of C1/C3's underlying uncertainty, and would independently support at least MEDIUM — but the citation ceiling governs. What would lift the cap: resolving C1's and C3's underlying input uncertainty (GT-9?, GT-10?, the ARPC-transfer rival A11, and the survivorship-bias rival A13) — which is exactly what the recommended pilot produces as a byproduct of running it.

### Conclusion C5: The pilot bounds near-term risk, but a later public launch creates a lock-in risk that must be planned for deliberately, not by default momentum

C4 (limited pilot is the correct next action)
→[2nd] actor lens: sales reps may informally offer pilot slots as backdoor discounts to close hesitant deals
→[2nd] actor lens: existing paying customers may perceive unfairness if they learn new prospects get free pilot access
→[2nd] actor lens: competitors are unlikely to react at all, given the pilot's small and private scope *[Assumes: A15 — a small, sales-assisted pilot stays genuinely invisible to competitors and the broader market]*
→[2nd] time lens: in the near term (0-3 months) the business is largely unchanged
→[2nd] time lens: in the medium term (3-9 months) real conversion, support-load, and deal-cycle data accumulate, resolving A8 and replacing GT-9?/GT-10? with measured figures
→[3rd] time lens: if the pilot succeeds and a public tier is later built, reversing it is reputationally costly, so pressure to keep lowering friction tends to persist long after the original ROI case is tested
→ the go/no-go decision after the pilot should therefore be made deliberately, with an explicit reversibility plan and kill criteria set in advance

**Pre-check:** head C4 (LOW) · ?-marked: none directly · lowest cited: LOW · Inputs ceiling: LOW
**Confidence:** LOW — capped by citing C4 (LOW) on its head, per the unverified-input ceiling rule; C4's own confidence line carries the explanation and is not repeated here. No GT-N? input is rested on directly by this chain. The second- and third-order effects named do not contradict any ground truth in section 3, so no return to Phase 2 is triggered.


### Conclusion C6: Published external benchmarks place B2B freemium free-to-paid conversion rates in a wide band, roughly 2%-20% depending on segment and model

GT-6 (ChartMogul: B2B-focused 6-10% good / 15-20% great; general 3-5% good / 8-12% great) + GT-7 (First Page Sage: traditional-freemium median ~3.9%, range 2.1%-5.6%)
→ the two independently-sourced reports overlap, with B2B-specific products in GT-6 clustering higher (6%-20%) than the cross-industry traditional-freemium figures in GT-7 (2.1%-5.6%)
→ published external benchmarks place realistic freemium conversion somewhere between roughly 2% and 20%, with the exact figure highly dependent on segment, model, and ACV — the external reference point chain C1 uses, not a prediction of this company's own rate

**Pre-check:** head GT-6, GT-7 · ?-marked: none · lowest cited: none · Inputs ceiling: HIGH
**Confidence:** HIGH — both inputs are unsuffixed ground truths read directly at their source (GT-6, GT-7); the inference is a direct, deductive restatement of what the two sources report, with no unstated premise; and no rival reading of what these two specific reports say is live — the only open question (whether this range transfers to this company's own ACV, A11) belongs to chain C1, which uses this chain's output as an external reference point, not to this chain's own narrower claim about what the published data itself says.

## 5. Abandoned Reasoning

### Dead End: Full freemium build now, skipping validation

**What was tried:** Scored as Option 2 in the trade-off analysis (chain C4) — committing immediately to building self-serve signup, billing, metering, and upgrade infrastructure for a permanent public free tier.

**Why abandoned:** Dominated on cost-to-validate, time-to-signal, risk-to-existing-support/sales-motion, strategic optionality, and brand/positioning risk by the limited-pilot option, per the locked weighted-criteria scoring (55 vs. 112), with a flip-test showing no plausible single-weight change (within the locked 1-5 scale) reverses the ranking.

**What it ruled out:** Committing 6-12 months of engineering effort and an unbounded support/sales-disruption risk before any internal data exists on the single highest-stakes unverified assumption (A8 — whether the free activator reaches the budget holder).

### Dead End: Doing nothing (status quo indefinitely)

**What was tried:** Scored as Option 1 — continuing outbound-and-referral-only acquisition with no freemium, trial, or pilot of any kind.

**Why abandoned:** Ties the limited pilot on cost, support/sales risk, and optionality, but scores lowest alongside full-freemium on time-to-signal and loses badly on goal-achievement (88 vs. 112), because it generates no data and leaves the stated motivations (missing inbound channel, unresolved competitive-parity question) permanently untested.

**What it ruled out:** Treating "we already grow fine via outbound" (GT-1?, GT-2?) as sufficient reason to never test the free/self-serve question at all — the trade-off shows that testing cheaply dominates not testing.

### Dead End: Competitive parity alone as the deciding rationale

**What was tried:** Treating "all competitors have a free tier" (GT-5?, assumptions A1 and A9) as sufficient justification on its own for a multi-quarter engineering investment.

**Why abandoned:** The causal link between competitors' free tiers and their success is explicitly unvalidated by the user's own framing (GT-5?), and chain C3 shows the company's own $2.4M ARR (GT-1?) was built via outbound+referral alone (GT-2?) — contradicting the idea that lack of a free tier is currently blocking growth.

**What it ruled out:** Using bandwagon/competitive-parity reasoning as a standalone justification for the build decision; retained only as a near-zero-cost secondary diagnostic (asking lost deals why they chose a competitor) folded into the recommended pilot's scope.

## 6. Conclusion

**Recommended approach:** Run a small, private, sales-assisted pilot — offering free or heavily discounted access to roughly 15-25 ICP-matched prospects sourced through the existing outbound/referral motion, manually onboarded and tracked for 90-180 days — before committing any engineering resources to a public self-serve or freemium build (chain C4).

**Key insight:** The actual bottleneck is very likely not whether the price is $0 — it is whether the person who can self-activate on cheap or free access is the same person who holds budget authority for a ~$10,000/year team purchase (assumption A8). The break-even math shows that if that bottleneck is cleared, infra+support cost is not the limiting factor (chain C1); but if it isn't cleared, no conversion-rate benchmark or price point fixes it (chain C4).

**Trade-offs acknowledged:** This recommendation accepts slower progress toward an actual public self-serve/inbound channel — the pilot does not itself build the channel — in exchange for a near-zero-cost, fully reversible test of the riskiest assumption before any public commitment (chain C4). It also leaves the competitive-parity rationale (A1, A9) unresolved beyond a cheap diagnostic add-on (win-loss interviews), since no chain in this analysis settles it either way (chain C3). Published external benchmarks place realistic freemium conversion somewhere between roughly 2% and 20% depending on segment and ACV (chain C6), but this analysis does not claim that range predicts this company's own result without the recommended pilot (chain C1).

**Pre-check:** head C1 (LOW), C2 (LOW), C3 (LOW), C4 (LOW), C5 (LOW), C6 (HIGH) · ?-marked: none directly · lowest cited: LOW · Inputs ceiling: LOW
**Confidence:** LOW — every chain this conclusion rests on is LOW except C6, which is HIGH but only establishes what published benchmarks report (chain C6), not what this company's own buyers will do. The recommendation itself is LOW primarily because the company has zero internal data on its single highest-stakes assumption (A8: whether the free/pilot activator reaches the budget holder) and on its actual per-free-user cost (GT-9?) and gross margin (GT-10?). This is not a defect in the reasoning: chain C4's dominance argument for running the pilot is itself robust under a flip-test independent of these uncertainties (chain C4); the LOW band is a direct, honest reflection of the fact that no freemium pilot has ever been run (GT-4?) and no Finance cost-model document was opened by this analysis (GT-3?, GT-9?). What would raise this to MEDIUM or HIGH: running the recommended pilot, which directly measures the real conversion rate, the real per-user cost, and whether activators reach budget holders — replacing GT-9?, GT-10?, and A8 with measured figures rather than assumed brackets.

## Appendix — process output

## Assumption Audit scan (process output)

| Chain | Step | Step Text (brief) | Assumption surfaced? | Added to Table? |
|-------|------|--------------------|-----------------------|------------------|
| C1 | 1 | break-even conversion rate brackets to ~0.18%-4.23%, central 0.93% | none | n/a |
| C1 | 2 | observed rates in GT-6/GT-7 sit at/above high end of bracket in every segment | GT-6's benchmark ARPC may not transfer to this company's higher ACV (A11) | yes |
| C1 | 3 | marginal cost not, by itself, sufficient reason to reject | none | n/a |
| C2 | 1 | counterfactual test: a trial/low-price plan would likely also have fixed the symptom | none | n/a |
| C2 | 2 | absence of any self-serve path, not specifically $0 price, is the more necessary condition | a $0 price point specifically removes a trust/budget-risk barrier a trial does not (A12) | yes |
| C2 | 3 | "add a free tier" conflates tactic with root cause | none | n/a |
| C3 | 1 | company's growth not evidently blocked by lack of free tier | GT-1?'s 240-team count is not subject to survivorship bias (A13) | yes |
| C3 | 2 | competitive parity is the weakest of the four motivations | none | n/a |
| C4 | 1 | scoring four options against six locked, weighted criteria produces a weighted total each | none | n/a |
| C4 | 2 | weighted totals: 88/55/74/112 | none | n/a |
| C4 | 3 | pilot weakly dominates status quo, beats full-freemium/trial on 5 of 6 criteria | none | n/a |
| C4 | 4 | flip-test confirms robustness | the locked criteria weights reflect this company's actual priorities (A14) | yes |
| C4 | 5 | correct next action is the limited pilot | none | n/a |
| C5 | 1 | actor lens: reps may offer pilot slots as backdoor discounts | none | n/a |
| C5 | 2 | actor lens: paying customers may perceive unfairness | none | n/a |
| C5 | 3 | actor lens: competitors unlikely to react, pilot small/private | a small pilot stays genuinely invisible to competitors/market (A15) | yes |
| C5 | 4 | time lens: near term, business largely unchanged | none | n/a |
| C5 | 5 | time lens: medium term, real data accumulates, resolving A8/GT-9?/GT-10? | none | n/a |
| C5 | 6 | time lens: long horizon, reversal cost creates persistent friction-lowering pressure | none | n/a |
| C5 | 7 | go/no-go decision should be deliberate, with reversibility plan | none | n/a |
| C6 | 1 | GT-6/GT-7 overlap, B2B-specific clusters higher than cross-industry | none | n/a |
| C6 | 2 | published benchmarks span ~2%-20%, the external reference point chain C1 uses | none | n/a |

Scan complete: 6 chains, 22 steps in order; 5 assumptions surfaced (A11-A15), all added to the Assumptions Table in section 2.

## Techniques not applied (process output)

- fishbone — not applicable — the assumption space was narrow and directly enumerable (four assumptions named in the prompt plus structurally necessary extensions); breadth-first category brainstorming was not needed to surface it.
- theoretical-limit — not applicable — this is a business/economic go/no-go decision with no governing hard physical or mathematical constraint whose ceiling needs deriving; the estimate technique (break-even conversion rate) covers the quantitative-magnitude need instead.

## Adversarial pass (process output)

**Recompute.** C1: c_low/V_high = 15/8500 = 0.18%; c_high/V_low = 275/6500 = 4.23%; central 70/7500 = 0.93% — all match chain C1's stated bracket. C4 weighted totals, recomputed independently from the locked weights (cost-to-validate=5, time-to-signal=4, risk=5, optionality=3, brand-risk=3, goal-achievement=4) and each option's 1-5 scores: Option 1 (status quo) = 5·5+1·4+5·5+5·3+5·3+1·4 = 88; Option 2 (full freemium) = 1·5+2·4+2·5+2·3+2·3+5·4 = 55; Option 3 (free trial) = 2·5+3·4+3·5+3·3+4·3+4·4 = 74; Option 4 (pilot) = 5·5+5·4+5·5+5·3+5·3+3·4 = 112. All four totals match chain C4's stated figures exactly — no arithmetic error found. Chain C6 computes nothing — it restates figures already quoted verbatim from GT-6 and GT-7 — so there is no arithmetic to recompute beyond confirming the quoted figures match section 3's Ground Truths list, which they do.

**Sensitivity.** The single ground truth whose falsity would flip the headline recommendation is GT-9? (marginal infra+support cost per free active user). It is `?`-marked. If the true cost were materially higher than this analysis's bracket (e.g., a compute/data-intensive product at $1,000+/free-user/year), the break-even conversion rate would exceed every realistic benchmark (GT-6, GT-7), and the conclusion would shift from "run a pilot, cost is probably not the blocker" to "a public free tier is very likely uneconomic regardless of conversion rate, full stop." GT-9? is not currently verifiable without Finance's actual cost model, which is precisely the kind of measurement the recommended pilot would force even at small scale (a 15-25-prospect pilot still generates real, attributable infra/support cost data).

**Rival.** Headline conclusion (run the pilot before building): the strongest rival — "skip the pilot and build a public self-serve tier (free trial or freemium) now, because speed-to-market and competitive parity matter more than certainty" — is ruled out by chain C4's dominance argument and flip-test (see §5, Dead End "Full freemium build now, skipping validation"). Intermediate chain C1 (cost is not the blocker): a live rival (ARPC-transfer mismatch, A11) is not ruled out and is carried live on C1's confidence line. Intermediate chain C2 (root cause is channel-type, not price): a live rival (A12, "$0 specifically matters") is not ruled out and is carried live on C2's confidence line. Intermediate chain C3 (competitive parity is weak): a live rival (A13, survivorship bias) is not ruled out and is carried live on C3's confidence line. Chain C5 (lock-in risk needs deliberate planning): rival not applicable — no competing plan for handling reversibility risk has been proposed anywhere in this analysis; the point is a risk-management addition, not a contested empirical claim. Chain C6 (published benchmarks span ~2%-20%): rival not applicable — this chain is a faithful restatement of two independently-sourced reports, not a contested empirical claim; the open question (whether this range transfers to this company) is carried on chain C1, not C6.

**Adversarial technique — Pre-Mortem** (the conclusion is a plan/recommendation, so pre-mortem applies rather than inversion).

*Premise:* It is 12 months from now. The free/self-serve initiative has already failed to produce a viable channel, and resources were wasted in the process.

*Causes (unfiltered, by stakeholder, generated before any grouping):*
1. (Head of Sales) Free/pilot signups are low-intent (students, consultants, competitors browsing), not real buyers.
2. (Head of Sales) Existing outbound prospects stalled deals, saying "we'll just use the free/pilot access for now."
3. (Head of Sales) No SQL definition existed for free signups, wasting SDR time working unqualified leads.
4. (Head of Sales) Reps began offering pilot slots as informal discounts to close hesitant deals.
5. (Head of Support/CS) Free-tier/pilot ticket volume saturated support capacity sized for 240 paying teams.
6. (Head of Support/CS) Paying-customer SLA degraded as a result.
7. (Head of Support/CS) No tooling existed to deprioritize free-tier tickets relative to paying ones.
8. (Rival vendor) A competitor matched or undercut the free offering, turning the fight into a race-to-the-bottom rather than differentiation on the paid product.
9. (Rival vendor) A competitor used the freemium launch as a talking point to attack the company's premium pricing in competitive deals.
10. (Churned free/pilot user) Hit a usage/feature wall with no clear upgrade path communicated.
11. (Churned free/pilot user) Never had budget authority to convert, and no path existed from them to the actual budget holder.
12. (Churned free/pilot user) Left negative reviews citing "bait and switch."
13. (Finance/Exec) The self-serve build consumed 6-12 months of engineering roadmap with no stated kill criterion, and nobody revisited the bet once sunk.
14. (Finance/Exec) The initiative's cost (infra plus opportunity cost) was never tracked separately from steady-state costs, so its real ROI was never knowable.

*Clusters:*
- **Cluster A — Lead quality / pipeline cannibalization / budget-authority mismatch** (causes 1, 2, 3, 4, 11; bears on GT-2?, chain C3, chain C4, assumption A8). Triage: **fatal** if true at scale — it kills the entire strategic rationale for a self-serve channel.
- **Cluster B — Support capacity overload** (causes 5, 6, 7; bears on GT-3?, GT-9?, chain C1). Triage: **costly but survivable.**
- **Cluster C — Competitive/positioning erosion** (causes 8, 9; bears on GT-5?, chain C3). Triage: **tolerable** while the pilot stays private (A15); becomes live risk only if scaled publicly.
- **Cluster D — Poor UX/communication causing frustration and brand damage** (causes 10, 12; bears on chain C5, actor lens). Triage: **costly but survivable.**
- **Cluster E — Unbounded, unkillable investment** (causes 13, 14; bears on chain C4, chain C5). Triage: **costly but survivable,** and the easiest to prevent in advance.

*Disposition:*
- Cluster A: **plan change** — the recommended pilot explicitly tracks whether signups are ICP-matched and whether the activator reaches the budget holder (directly testing A8) before any larger investment; require a lead-qualification signal (team size/usage) before scaling beyond the pilot. Tripwire: fewer than a stated minimum of qualified-ICP signups convert among the pilot cohort by day 90 — owner: Head of Growth/Product.
- Cluster B: **plan change** — scope the pilot, and any future free tier, with hard usage caps and self-serve-only/community support by default, no live-support SLA commitment, before any public launch. Tripwire: paying-customer median support response time degrades by more than 50% in any week post-pilot-launch — owner: Head of Support.
- Cluster C: **accepted risk with mitigation** — keep the pilot private/unannounced (per A15); if a public tier is later built, monitor enterprise win-rate and review-site positioning quarterly as the tripwire — owner: Head of Sales/RevOps.
- Cluster D: **plan change** — design explicit upgrade-path messaging and communication before any self-serve launch (pilot or public), not retrofitted afterward.
- Cluster E: **plan change** — set an explicit kill/scale decision gate tied to the pilot's measured conversion rate and lead quality (the data points chain C1/C4 would then carry as measured rather than assumed figures), with pilot cost tracked separately from steady-state spend, before committing to a full build.

**Falsification.** This analysis's recommendation is false if a 90-180 day sales-assisted pilot, run among ICP-matched prospects via the existing outbound/referral motion, shows that free/low-commitment access converts to paid at a rate clearing the measured break-even threshold (chain C1) AND that the activating user reliably reaches or is the budget holder (resolving A8) — in that case, proceeding directly to a public self-serve tier build-out would be justified rather than overcautious.

## §6→§4 closure ledger (process output)

- "Run a small, private, sales-assisted pilot ... before committing any engineering resources to a public self-serve or freemium build" → chain C4 ✓
- "The actual bottleneck is very likely not whether the price is $0 ... infra+support cost is not the limiting factor ... no conversion-rate benchmark or price point fixes it" → chain C1, chain C4 ✓
- "This recommendation accepts slower progress ... in exchange for a near-zero-cost, fully reversible test ... It also leaves the competitive-parity rationale ... unresolved ... Published external benchmarks place realistic freemium conversion somewhere between roughly 2% and 20% ..." → chain C4, chain C3, chain C6 ✓
- "**Pre-check:** head C1 (LOW), C2 (LOW), C3 (LOW), C4 (LOW), C5 (LOW), C6 (HIGH) ..." → chain C1, chain C2, chain C3, chain C4, chain C5, chain C6 ✓
- "every chain this conclusion rests on is LOW except C6 ... What would raise this to MEDIUM or HIGH: running the recommended pilot ..." → chain C1, chain C2, chain C3, chain C4, chain C5, chain C6 ✓

Ledger complete: 5 §6 claims, 5 traced to named section-4 chains (citing C1-C6 in total), 0 cut.

## Self-audit scan (process output)

| Chain | Chain Head (brief) | Form conforming? | Rule applied | Dependency clean? | Band | Act attempted? | Edges fired |
|-------|---------------------|-------------------|---------------|--------------------|------|-----------------|-------------|
| C1 | GT-8 + GT-9? + GT-10? | yes | n/a | yes | LOW | yes | none |
| C2 | GT-2? | yes | n/a | yes | LOW | no | none |
| C3 | GT-1? + GT-2? + GT-5? | yes | n/a | yes | LOW | no | none |
| C4 | C1 + C3 | yes | n/a | yes | LOW | no | none |
| C5 | C4 | yes | n/a | yes | LOW | no | none |
| C6 | GT-6 + GT-7 | yes | n/a | yes | HIGH | yes | none |

| §6 Span (brief) | Construct | Claim under R11? | R11 clause applied | Chain cited |
|-------------------|-----------|-------------------|----------------------|---------------|
| Recommended approach: Run a small, private, sales-assisted pilot... | bold lead-in | yes | bold lead-in whose colon closes the bold span | C4 |
| Key insight: The actual bottleneck is very likely not whether the price is $0... | bold lead-in | yes | bold lead-in whose colon closes the bold span | C1, C4 |
| Trade-offs acknowledged: This recommendation accepts slower progress... | bold lead-in | yes | bold lead-in whose colon closes the bold span | C4, C3, C6 |
| Pre-check: head C1 (LOW), C2 (LOW), C3 (LOW), C4 (LOW), C5 (LOW), C6 (HIGH)... | bold lead-in | yes | bold lead-in whose colon closes the bold span; pre-check line is itself a claim cited by the chains its own head names | C1, C2, C3, C4, C5, C6 |
| Confidence: LOW — every chain this conclusion rests on is LOW except C6... | bold lead-in | yes | bold lead-in whose colon closes the bold span | C1, C2, C3, C4, C5, C6 |

Scan complete: 6 chain rows, one per section-4 chain block in order; 5 section-6 rows, one per construct in order — 5 claims under R11, 0 excluded. 0 chains malformed, 0 claims untraced.

## Self-Audit Gate (process output)

**Criterion 1: Identify Essence**
Quoted span: "Given zero internal data on free-to-paid conversion, a confirmed real marginal cost per free active user, and an unvalidated 'competitors have it' argument, should this company commit engineering and support resources to build a permanent free tier as its mechanism for creating a self-serve/inbound acquisition channel it currently lacks?"
Band: **Rigorous**
Justification: The statement names the actual decision (build vs. not, and via what mechanism) rather than restating the prompt or a symptom, and each of the five success criteria is a verb+subject+outcome test scannable against section 6 (e.g., "names a minimal, low-cost validation step" checks directly against the Recommended approach line) without further interpretation.

**Criterion 2: Challenge Assumptions**
Quoted span (from the Assumption Audit scan): "Scan complete: 6 chains, 22 steps in order; 5 assumptions surfaced (A11-A15), all added to the Assumptions Table in section 2."
Band: **Rigorous**
Justification: All 15 rows use the four-type scheme correctly, every Verdict cell leads with Accept/Challenge/Discard followed by an em-dash and a specific justification, every unverified entry used in a chain reads "unverified — flagged," at least one assumption is Discarded (A9) and several Challenged with evidence, and the Assumption Audit scan confirms the end-of-Phase-4 audit ran exhaustively over every chain step and surfaced five new assumptions into the table.

**Criterion 3: Establish Ground Truths**
Quoted span: "?-marked: GT-1, GT-2, GT-3, GT-4, GT-5, GT-9, GT-10 (7 of 10). Read-at-source: GT-6 — ...; GT-7 — ..." compared against the Ground Truths list, which carries the `?` suffix on exactly those seven IDs and no others.
Band: **Rigorous**
Justification: GT-IDs are stable and match the Derivation Chains section; the enumeration matches the list when checked against it; GT-6 and GT-7 are both reachable, were read at source with named locations, and each now feeds a HIGH-confidence chain (C6), satisfying the unsuffixed-GT-feeds-a-HIGH-chain requirement; no Discard-verdict assumption appears in the list.

**Criterion 4: Reason Upward**
Quoted span (from the Self-audit scan's chain-form table): all six rows read "Form conforming? = yes" with "Dependency clean? = yes," and the Abandoned Reasoning section documents three dead ends, each with a specific structural reason ("dominated ... per the locked weighted-criteria scoring," "contradicting the idea that lack of a free tier is currently blocking growth").
Band: **Rigorous**
Justification: Every conclusion in sections 4 and 6 has exactly one chain in the prescribed arrow-led form with a genuine intermediate step; no analogy is used as direct evidence anywhere in the analysis; each chain step introducing a new assumption (A11-A15) declares it inline with `[Assumes: X]` at the point it was surfaced; and the three dead ends use the specific What-was-tried/Why-abandoned/What-it-ruled-out structure rather than a vague reason.

**Criterion 5: Validate**
Quoted span: "capped by the lowest-rated chain this chain's head cites (C1 and C3 are both LOW), per the unverified-input ceiling rule" (chain C4's confidence line) and "A premise stated in the past tense... It is 12 months from now. The free/self-serve initiative has already failed..." (adversarial pass record).
Band: **Rigorous**
Justification: Every chain's band matches what its own Inputs/Inference/Rivals axes license (verified independently in the self-audit scan's Band column against each chain's stated reasoning), no chain with a `GT-N?` input is rated HIGH, every chain is capped at or below the lowest-rated chain its head cites, the overall Conclusion's LOW rating matches its weakest contributing chain, and the adversarial pass record is complete — Recompute, Sensitivity, Rival, the full pre-mortem (past-tense premise, 14 unfiltered multi-stakeholder causes, 5 named clusters, a named plan-change or accepted-risk-with-mitigation disposition for every cluster), and Falsification are all present.

**Criterion 6: Conclusion-to-Ground-Truth Traceability**
Quoted span (from the Self-audit scan's claim-inventory table): all five section-6 rows read "Claim under R11? = yes" with a named chain in the "Chain cited" column (C4; C1, C4; C4, C3, C6; C1-C6; C1-C6), and zero rows read "none — untraced."
Band: **Rigorous**
Justification: Every claim in section 6 traces to a specific named chain in section 4, no new reasoning is introduced in section 6 that section 4 does not already establish, and the Key Insight ("the actual bottleneck is... whether the activator reaches the budget holder") is a distinct, non-obvious analytical finding rather than a restatement of the Recommended approach ("run a pilot").

**Gate result:** cleared · passes: 1 · Fix/Repeat fired: no

## Structured summary (process output)

```json
{
  "schema_version": 1,
  "run_mode": "full-composer",
  "assumptions": [
    {"id": "A-1", "type": "convention", "verdict": "Challenge"},
    {"id": "A-2", "type": "untested belief", "verdict": "Challenge"},
    {"id": "A-3", "type": "untested belief", "verdict": "Challenge"},
    {"id": "A-4", "type": "convention", "verdict": "Challenge"},
    {"id": "A-5", "type": "current constraint", "verdict": "Accept"},
    {"id": "A-6", "type": "current constraint", "verdict": "Accept"},
    {"id": "A-7", "type": "untested belief", "verdict": "Challenge"},
    {"id": "A-8", "type": "untested belief", "verdict": "Challenge"},
    {"id": "A-9", "type": "convention", "verdict": "Discard"},
    {"id": "A-10", "type": "untested belief", "verdict": "Challenge"},
    {"id": "A-11", "type": "untested belief", "verdict": "Challenge"},
    {"id": "A-12", "type": "untested belief", "verdict": "Challenge"},
    {"id": "A-13", "type": "untested belief", "verdict": "Challenge"},
    {"id": "A-14", "type": "convention", "verdict": "Challenge"},
    {"id": "A-15", "type": "current constraint", "verdict": "Accept"}
  ],
  "ground_truths": [
    {"id": "GT-1", "read_at_source": false},
    {"id": "GT-2", "read_at_source": false},
    {"id": "GT-3", "read_at_source": false},
    {"id": "GT-4", "read_at_source": false},
    {"id": "GT-5", "read_at_source": false},
    {"id": "GT-6", "read_at_source": true},
    {"id": "GT-7", "read_at_source": true},
    {"id": "GT-8", "read_at_source": true},
    {"id": "GT-9", "read_at_source": false},
    {"id": "GT-10", "read_at_source": false}
  ],
  "chains": [
    {"id": "C1", "confidence": "LOW", "rests_on": ["GT-8", "GT-9?", "GT-10?", "GT-6", "GT-7"]},
    {"id": "C2", "confidence": "LOW", "rests_on": ["GT-2?"]},
    {"id": "C3", "confidence": "LOW", "rests_on": ["GT-1?", "GT-2?", "GT-5?"]},
    {"id": "C4", "confidence": "LOW", "rests_on": ["C1", "C3"]},
    {"id": "C5", "confidence": "LOW", "rests_on": ["C4"]},
    {"id": "C6", "confidence": "HIGH", "rests_on": ["GT-6", "GT-7"]}
  ],
  "dead_ends": [
    "Full freemium build now, skipping validation",
    "Doing nothing (status quo indefinitely)",
    "Competitive parity alone as the deciding rationale"
  ],
  "techniques": {
    "applied": ["inversion", "estimate", "five-whys", "trade-off", "second-order", "pre-mortem"],
    "not_applied": [
      {"technique": "fishbone", "phase": 2, "reason": "the assumption space was narrow and directly enumerable (four assumptions named in the prompt plus structurally necessary extensions); breadth-first category brainstorming was not needed to surface it."},
      {"technique": "theoretical-limit", "phase": 4, "reason": "this is a business/economic go/no-go decision with no governing hard physical or mathematical constraint whose ceiling needs deriving; the estimate technique (break-even conversion rate) covers the quantitative-magnitude need instead."}
    ]
  },
  "gate": {
    "passes": [
      {
        "bands": ["Rigorous", "Rigorous", "Rigorous", "Rigorous", "Rigorous", "Rigorous"],
        "gate_cleared": true,
        "hand_wavy_cap_cleared": true
      }
    ],
    "fix_repeat_fired": false,
    "cleared": true
  },
  "re_entry": {
    "fired": false,
    "edges": []
  },
  "conclusion": {
    "recommendation": "Run a small, private, sales-assisted pilot — offering free or heavily discounted access to roughly 15-25 ICP-matched prospects sourced through the existing outbound/referral motion, manually onboarded and tracked for 90-180 days — before committing any engineering resources to a public self-serve or freemium build (chain C4).",
    "confidence": "LOW",
    "rests_on": ["C1", "C2", "C3", "C4", "C5", "C6"]
  }
}
```
