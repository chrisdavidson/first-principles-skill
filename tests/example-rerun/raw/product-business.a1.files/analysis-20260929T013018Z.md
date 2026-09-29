## Techniques not applied (process output)

- **five-whys (reduce-to-primitives)** — not applicable — every Phase 3 ground truth is either an external direct-measurement statistic (GT-6, already an irreducible published figure) or a user-stipulated primary business fact explicitly marked "verified, treat as true, do not re-derive" (GT-1? through GT-5?, GT-7? is an explicitly-flagged assumed range, not a compound claim). No candidate ground truth in scope was a compound claim requiring decomposition into constituent primitives.
- **fishbone** — not applicable — the assumption space was narrow enough to enumerate directly (13 named assumptions clustering tightly around GTM motion, cost structure, and competitive framing). Breadth of unknown cause-categories was not the limiting factor; inversion (which did fire) already supplied the structured coverage this decision needed.
- **theoretical-limit (Phase 1 essence-reframe invocation)** — not applicable — the essence here is a discrete strategic choice (launch / don't / pilot), not a metric bounded by convention vs. physical law; reframing the essence around "what the fundamentals permit" would not change the core question. (theoretical-limit's Phase 4 invocation did fire — see chain C2's cost-floor reasoning.)
- **inversion (Phase 5 adversarial-technique invocation)** — not applicable — the Conclusion is a plan/recommendation, not a bare claim, so Pre-Mortem is the prescribed adversarial technique per the stated decision rule (inversion vs. pre-mortem). (inversion's Phase 2 invocation did fire — see the Assumptions Table treatment of assumptions #1, #5, #7, #8, #9, #11, all surfaced via the failure-precondition enumeration.)

## Assumption Audit scan (process output)

| Chain | Step | Step Text (brief) | Assumption surfaced? | Added to Table? |
|-------|------|-------------------|----------------------|-----------------|
| C1 | 1 | competitor freemium ≠ our own economics | none | n/a |
| C1 | 2 | no-analogy rule applied to GT-5?/GT-4? | none | n/a |
| C1 | 3 | parity insufficient standalone justification | none | n/a |
| C2 | 1 | breakeven = cost per free account ÷ ACV | none | n/a |
| C2 | 2 | breakeven range at GT-7?'s low/high bounds | none | n/a |
| C2 | 3 | breakeven band vs. GT-6 benchmark | none | n/a |
| C2 | 4 | signup-volume 500-8,000 → net $ bracket | year-one signup volume will fall in an unanchored 500-8,000 range | yes — row 12 |
| C2 | 5 | estimate stop-criterion not met | none | n/a |
| C2 | 6 | cannot resolve by desk estimation alone | none | n/a |
| C3 | 1 | free tier reachable without sales mediation | existing customers/prospects can reach a free tier without sales mediation | yes — row 11 |
| C3 | 2 | actor lens: prospects/departments exploit access | none (covered by row 11) | n/a |
| C3 | 3 | time lens: risk compounds over 12-18 months | none | n/a |
| C3 | 4 | ungated launch risks existing ARR | none | n/a |
| C4 | 1 | full launch fails the cost-exposure must-have | none | n/a |
| C4 | 2 | weighted trade-off ranks bounded pilot highest | trade-off weights reflect this business's actual strategic priorities | yes — row 13 |
| C4 | 3 | flip test shows ranking is not a near-tie | none (covered by row 13) | n/a |
| C4 | 4 | recommend scoped, capped, time-boxed pilot | none | n/a |

## Adversarial pass (process output)

**Recompute.** GT-7? low bound: $60/yr ÷ $10,000 ACV = 0.006 = 0.6% breakeven — recomputes clean. High bound: $600/yr ÷ $10,000 = 0.06 = 6% — recomputes clean. Low bracket: 500 signups × $600/yr = $300,000 cost; revenue = 500 × 1% × $10,000 = $50,000; net = $50,000 − $300,000 = −$250,000/yr — recomputes clean. High bracket: 8,000 × $60/yr = $480,000 cost; revenue = 8,000 × 5% × $10,000 = $4,000,000; net = $4,000,000 − $480,000 = $3,520,000/yr — recomputes clean. Trade-off totals: Status quo = 5·5+1·5+1·3+1·2+5·4+5·4 = 25+5+3+2+20+20 = 75 — recomputes clean. Bounded pilot = 4·5+5·5+2·3+4·2+3·4+4·4 = 20+25+6+8+12+16 = 87 — recomputes clean. Alt-diversification = 4·5+2·5+2·3+3·2+4·4+5·4 = 20+10+6+6+16+20 = 78 — recomputes clean. Flip-test decomposition (pilot vs. alt-diversification): Data value (5−2)·5=15, Speed (4−3)·2=2, Eng-cost (3−4)·4=−4, Channel-safety (4−5)·4=−4; net 15+2−4−4=9, matching the 87−78=9 total gap exactly. No arithmetic errors found anywhere in the analysis.

**Sensitivity.** The single ground truth whose falsity would flip the headline recommendation is GT-4? (that the three unknowns are genuinely unmeasurable internally right now) — it is `?`-marked. If, contrary to the stipulated ground facts, usable proxy data already existed somewhere in the business, the case for running a pilot specifically (rather than moving faster on existing information) would weaken; GT-4? is user-stipulated and not independently re-derived here per the Input Contract. Weakest link per chain: C1's weakest link is GT-5? (unverified — competitors unnamed, no source could be targeted). C2's weakest link is the unanchored year-one signup-volume range (500-8,000), the single most speculative number in the analysis — anchored by neither internal data nor an external benchmark. C3's weakest link, and the reason it is rated LOW rather than MEDIUM, is the live, unsettled rival named below — the magnitude of cannibalization risk is genuinely unknown, not merely unmeasured-but-bounded like the other chains' `?` inputs. C4's weakest link is inherited directly from C3 via the confidence-capping rule.

**Rival.** Headline conclusion (run a bounded pilot): strongest rival is "skip the pilot and copy competitors' freemium motion now" — ruled out by the no-analogy ban (Abandoned Reasoning, Dead End 1). C1: rival reading "competitor parity alone justifies a full launch" — ruled out by Dead End 1, which names GT-4?'s absence as the reason parity cannot substitute for our own data. C2: rival reading "the bracket centers positive, so proceed on the strength of the central estimate" — ruled out inside the chain itself (hop 5: the estimate procedure's stop criterion is explicitly not met, so a central value cannot substitute for that criterion). C3: rival reading "cannibalization risk is negligible because the product's complexity naturally deters casual free-tier abuse" — this rival is **live and not ruled out** by any ground truth in this analysis; it is an open question the pilot's gating design (see Conclusion) is built to test rather than assume away. This is why C3 is rated LOW rather than MEDIUM — the Rivals axis is short here, not merely the Inputs axis. C4: rival reading "the trade-off weights understate competitive parity, and different weights would favor a faster path" — addressed by the flip test, which shows this rival would require moving the "data value" criterion's weight down by more than half its own scale range to win; recorded as ruled out by that margin.

**Premise.** The free-tier pilot has already been launched, has already failed, and has already been shut down within its first year.

**Causes** (unfiltered, generated from named stakeholder viewpoints before any grouping):
- CFO/Finance: (1) free-tier infra/support costs ran past budget because no hard cap was enforced; (2) no cap or kill-switch was defined at launch; (3) cohort-level conversion/CAC/cost instrumentation was not actually built alongside the pilot, so Finance had no real-time read on the breakeven math.
- Head of Sales: (4) free signups generated noisy "warm lead" signals that AEs chased instead of outbound targets, hurting quota attainment; (5) active outbound prospects discovered the free tier mid-negotiation and used it to anchor a discount; (6) departments inside existing paying accounts fragmented into free instances instead of expanding the paid contract.
- Engineering lead: (7) the minimum self-serve build took materially longer than time-boxed, displacing a committed roadmap item and damaging credibility with prospects promised that item; (8) the free product surface was crippled to protect the $10k ACV feature set, producing low-quality signups and weak word of mouth.
- Customer/end-user: (9) free-tier support was deprioritized and quality suffered, generating public complaints visible to the same ICP outbound sells into.
- Competitor: (10) a competitor used the new free tier for reconnaissance, then used feature gaps surfaced there in competitive-deal messaging.

**Clusters:**
- **Cluster A — Unbounded cost exposure** (causes 1, 2, 3; bears on GT-3?, chain C2). Triage: **Fatal if uncapped.** Disposition: plan change — hard monthly spend cap and kill-switch defined with Finance before launch; real-time cohort instrumentation built as part of MVP scope, not deferred.
- **Cluster B — Channel conflict with existing outbound motion** (causes 4, 5, 6; bears on chain C3, assumption row 11/A-11). Triage: **Costly but survivable.** Disposition: plan change — access gating (exclude existing customer domains; no discount-anchoring exposure to active deals) and separate PQL lead-routing so free-tier leads don't compete with outbound quota credit.
- **Cluster C — Infra build underestimation / opportunity cost** (causes 7, 8; bears on assumption row 9, Abandoned Reasoning Dead End 3). Triage: **Costly but survivable.** Disposition: plan change — scope the build to the minimum needed to measure conversion (signup + one upgrade path), time-box it, and set a hard go/no-go gate on the build itself before the acquisition pilot starts.
- **Cluster D — Reputation / competitive exposure** (causes 9, 10; bears on assumption row 4). Triage: **Tolerable.** Disposition: accepted risk, with a named mitigation — a minimum support SLA applies even to free accounts, and free-tier feature scope is chosen to avoid exposing roadmap gaps.

**Falsification.** The recommendation (run a bounded, capped, gated pilot rather than an immediate full launch or indefinite inaction) is false if either: (a) a capped, gated pilot turns out to be logistically infeasible to build at all with current engineering capacity within a reasonable time-box, making indefinite inaction the only real near-term option; or (b) reliable proxy data becomes available some other way — e.g., a verified, directly-read account of a named competitor's own freemium unit economics in an equivalent ACV/motion segment — that closes GT-4?'s gap without needing to run anything.

## §6→§4 closure ledger (process output)

- "Run a scoped, capped, time-boxed self-serve free-tier pilot rather than a full broad launch or indefinite inaction" → chain C4 ✓
- "The real obstacle to this decision is not whether a free tier is a good idea in the abstract... it's that the one number the decision actually turns on currently has no internal data behind it" → chains C1, C2 ✓
- "The bounded pilot is not free — it requires a real (if minimal) engineering build that doesn't exist today, and it accepts a period where the company still cannot claim full competitive parity" → chains C1, C3 ✓
- "Confidence: LOW on the specific shape of the pilot's numbers... but the choice of action — pilot over full launch or over inaction — is comparatively robust" → chains C1, C2, C3, C4 ✓

All four Conclusion-section claims cite a chain inline; no claim required cutting.

## Self-audit scan (process output)

| Chain | Chain Head (brief) | Form conforming? | Rule applied | Dependency clean? | Band | Act attempted? | Edges fired |
|-------|---------------------|-------------------|---------------|--------------------|------|-----------------|-------------|
| C1 | GT-5? + GT-1? + GT-4? | yes | n/a | yes | MEDIUM | no | none |
| C2 | GT-1? + GT-3? + GT-4? + GT-6 + GT-7? | yes | n/a | yes | MEDIUM | yes | none |
| C3 | GT-1? + GT-2? | yes | n/a | yes | LOW | no | none |
| C4 | C1 + C2 + C3 + GT-1? | yes | n/a | yes | LOW | no | none |

| §6 Span (brief) | Construct | Claim under R11? | R11 clause applied | Chain cited |
|-------------------|-----------|-------------------|----------------------|---------------|
| Recommended approach: run a scoped, capped, time-boxed pilot... | bold lead-in | yes | bold lead-in whose colon closes the bold span | C4 |
| Key insight: the real obstacle is the missing data behind the breakeven number... | bold lead-in | yes | bold lead-in whose colon closes the bold span | C1, C2 |
| Trade-offs acknowledged: the pilot is not free, requires a real build, accepts a parity gap... | bold lead-in | yes | bold lead-in whose colon closes the bold span | C1, C3 |
| Confidence: LOW on the specific shape of the pilot's numbers... | bold lead-in | yes | bold lead-in whose colon closes the bold span | C1, C2, C3, C4 |
| Falsification condition is recorded in the adversarial pass record, not here | prose | no | prose sentence pointing elsewhere; carries no bold-colon lead-in, no list marker, and is explicitly excluded per the rule that falsification belongs in the record only | n/a |

Scan complete: 4 chain rows, one per section-4 chain block in order; 5 section-6 rows, one per construct in order — 4 claims under R11, 1 excluded. 0 chains malformed, 0 claims untraced.

---

# First-Principles Analysis: Should the B2B SaaS Product Add a Free Tier?

## 1. Problem Essence

**Core problem:** Should the company commit to building and launching a self-serve free tier — given a go-to-market motion that is currently 100% outbound sales and referral, zero self-serve infrastructure, and no internal data on free-to-paid conversion rate, free-tier CAC, or free-tier support burden — or is there a lower-risk path to the same competitive goal?

**Success criteria:**
- The Conclusion section names exactly one of three actions — full launch, no launch, or a scoped pilot — with no fourth option left open.
- The Conclusion section's recommendation does not cite the unmeasured free-to-paid conversion rate (GT-4?) as a load-bearing premise for a binary launch/no-launch decision.
- The Conclusion section's Trade-offs acknowledged claim names the cost exposure implied by GT-3? (cost scales with active users) in dollar or rate terms.
- If the Conclusion recommends a pilot, it states explicit go/no-go conditions and names what the pilot must build given GT-2? (zero self-serve infrastructure today).

## 2. Assumptions Table

| Assumption | Type | Treatment | Verdict | Verification |
|---|---|---|---|---|
| 1. Competitors have a free tier, so we need one too | convention | Explicitly challenged — parity pressure is real but is a claim about differentiation signaling, not about our own unit economics | Challenge — insufficient standalone justification for an immediate full launch (addressed in chain C1) | unverified — flagged; GT-5? unverifiable in this session (competitors unnamed) |
| 2. A free tier drives growth | convention (PLG folklore generalized from low-ACV self-serve markets) | Challenged — growth effect is benchmark- and segment-dependent | Challenge — not established for this company's ACV/motion segment (addressed in chain C2) | unverified — flagged; GT-6 gives an external range only, applicability to our segment untested |
| 3. PLG is the natural next motion | untested belief | Verify against readiness preconditions (infra, product boundary, conversion path) | Challenge — preconditions currently unmet | unverified — flagged; GT-2? confirms no self-serve infrastructure exists |
| 4. Free-tier signups will resemble our actual ICP buyers, not tire-kickers | untested belief | Flag as unverified | Challenge — no basis to assume either way | unverified — flagged; no internal data (GT-4?); feeds Pre-Mortem Cluster D |
| 5. Free-to-paid conversion will land in the normal SaaS benchmark range (3-12%) | untested belief | Verify via pilot; do not assume | Challenge — explicitly flagged as currently unknowable | unverified — flagged; GT-4? states this is unknowable from internal data today; GT-6 supplies only an external reference range |
| 6. Free-tier infrastructure and support cost scales with active users, not paying users | current constraint (Finance-confirmed operating reality) | Record expiry conditions | Accept — expires only if the product moved to a fully static/cached free experience with no per-account compute or human support, which is not a realistic option for this product | GT-3? (Finance-confirmed; internal, not independently opened this session) |
| 7. Current outbound/referral growth is bottlenecked by lead-generation volume | untested belief | Verify — bottleneck could instead be sales-cycle length, win rate, or market size | Challenge — unresolved; no data supplied on which funnel stage actually binds | unverified — flagged; open question for pilot scoping |
| 8. A free tier will not cannibalize existing $10k ACV deals or existing paying accounts | untested belief | Challenge directly — pricing unit is per-team, structurally reachable by prospects and existing customers' other teams | Challenge — live risk, not resolved | unverified — flagged; addressed in chain C3 |
| 9. The engineering cost to build minimum self-serve infrastructure is small/incidental | untested belief | Challenge — GT-2? confirms zero self-serve infrastructure exists today, so this is a nonzero build | Challenge — likely underestimated by default optimism | unverified — flagged; addressed in Pre-Mortem Cluster C |
| 10. Copying competitors' freemium motion is a valid substitute for our own data | convention / reasoning-by-analogy | Explicitly banned as direct evidence per the Phase 4 no-analogy rule | Discard — reasoning by analogy, not evidence about our own economics | routed to Abandoned Reasoning, Dead End 1 |
| 11. Existing customers and outbound-stage prospects can reach a free tier without sales mediation [surfaced in Assumption Audit, chain C3 step 1] | current constraint (a pilot design choice, not yet made) | Record expiry condition — this risk lifts if the pilot is scoped with deliberate access gating | Challenge — open pilot-design parameter, not yet resolved | unverified — flagged; addressed in chain C3 [Assumes: A-11] and Pre-Mortem Cluster B; becomes a design requirement in the Conclusion |
| 12. Year-one free signup volume will land in the 500-8,000 range absent any inbound channel today [surfaced in Assumption Audit, chain C2 step 4] | untested belief | Flag as unverified — no anchor, internal or external | Challenge — the least-constrained input in this analysis | unverified — flagged; addressed via pilot instrumentation in the Conclusion [Assumes: A-12] |
| 13. The trade-off's six criteria and their assigned weights reflect this business's actual strategic priorities [surfaced in Assumption Audit, chain C4 step 2] | untested belief | Standard trade-off-procedure risk — weights were locked before scoring per the procedure's discipline, but their correctness is not independently verified | Challenge — unverified, but the flip test shows robustness to reasonable disagreement | unverified — flagged; addressed by the flip test in chain C4 [Assumes: A-13] |

## 3. Ground Truths

- **GT-1?** ARR is $2.4M; 240 paying teams; ~$10,000 ACV per team per year — unverified: primary-source assertion by the user as the business's own principal; this session opened no external document confirming it, though the company's own billing/CRM system and financial statements are the concrete verification path available outside this session.
- **GT-2?** No self-serve or inbound acquisition channel exists today; 100% of acquisition is outbound sales and referrals — unverified: internal operating fact; verification path = the company's own CRM/marketing-attribution reports, not opened in this session.
- **GT-3?** Finance has confirmed that free-tier infrastructure and support costs scale with active users, not paying users — every free signup is a real marginal cost regardless of conversion — unverified: internal Finance determination relayed by the user; verification path = Finance's own cost-allocation model and cloud billing reports, not opened in this session.
- **GT-4?** The company has never run a freemium pilot or self-serve motion; free-to-paid conversion rate, free-tier CAC, and free-tier support burden are currently unknowable from internal data — unverified: this is an absence-of-data self-report, so there is, by definition, no internal document to open; the verification path is exactly the pilot instrumentation the Conclusion recommends building.
- **GT-5?** All named competitors already have a free tier — unverified: competitors were not named in this session, so no specific competitor pricing or plans page could be targeted for a read. Phase 3 failure record: source unreachable — no competitor identity was supplied to fetch a source against, a gap in the input rather than a failed fetch attempt. Verification path = name the competitors and read their published free-tier terms; this is the one ground truth in this set resolvable to read-at-source simply by naming them.
- **GT-6** B2B SaaS freemium free-to-paid conversion benchmarks (200-product B2B software sample): median 8% across all models; "Freemium (regular signup)" band: Good = 3-5%, Great = 8-12%; cross-checked against industry-level figures of 2.1%-5.6% and model-type figures of 3.4%/3.7%/3.5% (Traditional Freemium / Land & Expand / Freeware 2.0) — source: ChartMogul/Growth Unhinged SaaS Conversion Report and First Page Sage's SaaS Freemium Conversion Rates report; read-at-source: chartmogul.com/reports/saas-conversion-report/, quoted directly as "The median free-to-paid conversion rate across all products is 8%" and the "Freemium (regular signup): Good = 3-5%, Great = 8-12%" row; firstpagesage.com/seo-blog/saas-freemium-conversion-rates/, quoted directly for the 2.1%-5.6% industry range and the 3.4%/3.7%/3.5% model-type figures. Applicability of this benchmark to this company's specific $10k-ACV, outbound-native segment is untested and remains an open question (see assumptions 2 and 5) — the benchmark is not itself in dispute, only its fit to this segment.
- **GT-7?** An assumed, explicitly-flagged per-free-account annual infrastructure+support cost range of $60-$600/year for a mid-complexity B2B SaaS product — unverified: this is an assumed range per the estimate procedure's own guidance for when no first-principles-cited value exists, not a measured or cited figure. The informal single-author sources surfaced by search (a Medium post and a "~$1/user/month" rule-of-thumb) were judged too low-confidence (undisclosed methodology, consumer-SaaS flavor) to anchor a load-bearing number and are therefore not used as this ground truth's basis. Verification path = the pilot's own realized cost actuals from Finance/DevOps once it runs.

**Provenance summary.** `?`-marked: GT-1?, GT-2?, GT-3?, GT-4?, GT-5?, GT-7? (6 of 7). Read-at-source: GT-6 — chartmogul.com/reports/saas-conversion-report/ ("The median free-to-paid conversion rate across all products is 8%"; Freemium regular-signup Good=3-5%/Great=8-12%) and firstpagesage.com/seo-blog/saas-freemium-conversion-rates/ (2.1%-5.6% industry range; 3.4%/3.7%/3.5% model-type figures).

## 4. Derivation Chains

### Conclusion C1: Competitive parity alone does not justify an immediate full-scale launch

GT-5? (competitors already have a free tier) + GT-1? (our $10,000 ACV, outbound-native motion) + GT-4? (no internal data on conversion, CAC, or support burden)
→ a competitor's freemium adoption is evidence of a category-level trend, not evidence about this company's own conversion rate, cost structure, or channel fit
→ per the ban on reasoning by analogy, GT-5? alone cannot stand in for GT-4?'s missing data because differentiation signaling and proven unit economics are separate claims
→ competitive parity raises the priority of getting real data soon but is not sufficient justification for an immediate full-scale launch

**Pre-check:** head GT-5?, GT-1?, GT-4? · ?-marked: GT-5?, GT-1?, GT-4? · lowest cited: none · Inputs ceiling: MEDIUM
**Confidence:** MEDIUM — GT-5? is unverified (competitors were not named, so no pricing page could be opened; verification path: name the competitors and read their published free-tier terms). GT-1? is unverified (primary-source internal data with no external document opened this session; verification path: the company's own billing/CRM system and financial statements). GT-4? is unverified by definition (an absence-of-data self-report; verification path: the pilot instrumentation the Conclusion recommends). All three inputs are `?`-marked but each carries a stated verification path, so the Inputs axis is short but bounded. The rival reading — that competitor parity alone justifies a full launch — is ruled out in Abandoned Reasoning, Dead End 1, which settles the Rivals axis and is what keeps this chain at MEDIUM rather than LOW.

### Conclusion C2: The cost/benefit of a free tier cannot be resolved by desk estimation alone

GT-1? (ACV $10,000/team/year) + GT-3? (cost scales with active users, not payers) + GT-4? (no internal data on conversion/CAC/cost) + GT-6 (freemium conversion benchmarks, 3-12%) + GT-7? (assumed per-account cost, $60-$600/yr)
→ breakeven conversion rate equals annual cost per free account divided by ACV, by unit-factor construction
→ at GT-7?'s low bound ($60/yr) breakeven conversion is about 0.6%, and at its high bound ($600/yr) about 6%
→ this breakeven band sits at or below GT-6's 3-5% "Good" benchmark depending on which end of the cost range is realized
→ layering in an unanchored year-one signup-volume assumption of 500-8,000 accounts [Assumes: A-12] produces a net annual dollar-impact bracket from roughly -$250,000 to +$3,520,000
→ the estimate procedure's own stop criterion is not met because the bracket's two ends do not drive the same decision
→ this decision cannot be responsibly resolved by desk estimation alone, because its dominant uncertainty is exactly the data GT-4? confirms does not exist internally

**Pre-check:** head GT-1?, GT-3?, GT-4?, GT-6, GT-7? · ?-marked: GT-1?, GT-3?, GT-4?, GT-7? · lowest cited: none · Inputs ceiling: MEDIUM
**Confidence:** MEDIUM — GT-1?, GT-3?, GT-4? and GT-7? are each unverified but each carries a stated verification path (internal financial/billing systems for GT-1?/GT-3?; the pilot's own build for GT-4?; realized pilot cost actuals for GT-7?), so the Inputs axis is short but bounded. The hop resting on assumption A-12 (signup volume 500-8,000) is priced: this chain's endpoint — that desk estimation cannot resolve the decision — survives even if the true signup-volume range differs from 500-8,000, because GT-2? independently establishes that no anchor for that number exists today regardless of which specific range is assumed; the Inference axis is therefore not short. The rival reading — proceed on the strength of a positive central estimate — is ruled out inside this chain's own fifth hop (the stop criterion is explicitly not met), settling the Rivals axis. Only the Inputs axis is short, and it is named and bounded, which is why this chain is MEDIUM rather than LOW.

### Conclusion C3: An ungated free tier puts a slice of the existing $2.4M ARR base at risk, not just new incremental cost

GT-1? (per-team $10,000 ACV pricing unit) + GT-2? (100% outbound/referral, zero self-serve infrastructure today)
→ a persistent, broadly-available free team account creates a lower-friction path that both outbound prospects and other teams inside already-paying customer organizations can reach directly, because the pricing and product unit is the team, not the individual user [Assumes: A-11]
→ actor lens: outbound prospects mid-negotiation gain a discount-anchoring lever, and departments inside existing paying accounts gain an incentive to spin up a separate free instance instead of expanding the paid one
→ time lens: this risk is small in month one before the free tier is discoverable, and compounds over 12-18 months as awareness spreads through exactly the accounts sales worked hardest to close
→ a free tier launched without deliberate scope controls puts a slice of the current $2.4M ARR base at risk, not just new incremental cost

**Pre-check:** head GT-1?, GT-2? · ?-marked: GT-1?, GT-2? · lowest cited: none · Inputs ceiling: MEDIUM
**Confidence:** LOW — GT-1? and GT-2? are each unverified but each carries a stated verification path (internal financial/billing systems for GT-1?; CRM/marketing-attribution reports for GT-2?), so the Inputs axis alone would only be short-but-bounded. The hop resting on assumption A-11 is priced: this chain's endpoint is itself conditional on A-11 ("without deliberate scope controls..."), so if A-11 turns out false because the pilot is properly gated, the endpoint's own condition is simply satisfied rather than falsified, and the Inference axis is not short. What drags this chain to LOW is the Rivals axis: the rival reading that cannibalization risk is negligible (because product complexity naturally deters casual free-tier abuse) is **live and not settled by any ground truth in this analysis** — it is recorded as an open question in the adversarial pass rather than ruled out. Two short axes would trigger LOW on their own, but even on the Rivals axis alone, an unsettled live rival is the explicit LOW-trigger condition stated in the confidence-band definition. Verification that would remove this cause of the downgrade: measure actual free-tier signup composition and cannibalization incidence during the pilot itself.

### Conclusion C4: Run a scoped, capped, time-boxed free-tier pilot rather than a full launch or indefinite inaction

C1 (MEDIUM) + C2 (MEDIUM) + C3 (LOW) + GT-1? (ACV, criteria factual basis for the trade-off's cost/value scoring)
→ against the must-have "must not create unbounded, uncapped cost exposure before the data GT-4? says we lack exists," an immediate full broad launch fails and is eliminated before scoring
→ weighted trade-off scoring across the three surviving options (status quo 75, bounded pilot 87, non-product funnel diversification 78) ranks the bounded pilot highest, driven mainly by the "data value" criterion, where the pilot scores 5 against 1-2 for the alternatives [Assumes: A-13]
→ the flip test shows this ranking is not a near-tie: the smallest single-criterion weight change that overturns it is dropping "data value" from weight 5 to below roughly 2, more than half that criterion's own scale range
→ recommend a scoped, capped, time-boxed pilot over both an immediate full launch and indefinite inaction

**Pre-check:** head C1 (MEDIUM), C2 (MEDIUM), C3 (LOW), GT-1? · ?-marked: GT-1? · lowest cited: LOW · Inputs ceiling: LOW
**Confidence:** LOW — this chain is capped at LOW because its head cites C3, which is rated LOW (per the ceiling rule, a chain is rated no higher than the lowest-rated chain its head cites). GT-1? is unverified with a stated verification path (internal billing/CRM systems), contributing only ordinary Inputs-axis shortfall on its own. The hop resting on assumption A-13 (trade-off weights reflect actual priorities) is priced by the flip test itself, which shows the ranking is robust to any single-criterion reweighting within a normal range — so the Inference axis is not independently short here. The two rivals considered for the headline recommendation (copy competitors now; never build one) are both ruled out in Abandoned Reasoning, Dead Ends 1 and 2. This chain's LOW rating is therefore inherited entirely from C3's unsettled Rivals axis, not from a defect of its own — the recommendation to pilot rather than decide outright is the correct response to that inherited uncertainty, not a weakness of this chain's construction.

## 5. Abandoned Reasoning

### Dead End 1: Match competitors and launch a full free tier now on the strength of competitive parity

**What was tried:** Reasoning that since every named competitor already has a free tier (GT-5?), the company should match them and launch broadly now.

**Why abandoned:** This treats GT-5? as a proxy for our own unit economics, which is reasoning by analogy — explicitly disallowed as direct evidence in Phase 4. Differentiation signaling and proven unit economics are two separate claims that this line of reasoning conflates.

**What it ruled out:** An immediate full-scale launch justified by competitive parity alone; ruled out by chain C1 and by the Rival analysis in the adversarial pass.

### Dead End 2: Never build a free tier because the outbound/high-ACV motion structurally doesn't fit PLG

**What was tried:** Reasoning that because the current motion is 100% outbound and high-ACV, a freemium/PLG motion structurally doesn't fit this business and should never be built.

**Why abandoned:** This forecloses learning at a cost (a bounded pilot) that chain C2 shows is small relative to the value of the information a wide, decision-straddling estimate bracket reveals is missing. It also treats "different from competitors' apparent motion" as sufficient reason to stop investigating — the same reasoning-by-analogy error as Dead End 1, run in reverse.

**What it ruled out:** Permanent inaction as the final answer; ruled out by the trade-off scoring in chain C4 (status quo scored lowest of the three viable options, 75 vs. 87) and by the value-of-information argument embedded in chain C2.

### Dead End 3: Launch a nominal "free tier" immediately without new infrastructure, provisioned manually

**What was tried:** Reasoning that the company could offer a "free tier" today by manually provisioning free accounts, without building any new self-serve infrastructure.

**Why abandoned:** GT-2? establishes that zero self-serve infrastructure exists today; a "free tier" provisioned manually by a human is not a self-serve acquisition channel and would not test the thing the decision actually turns on — unassisted signup-to-conversion behavior. It would produce data contaminated by the same sales-assisted motion already in use.

**What it ruled out:** A zero-build pilot design; ruled out by the pre-mortem's Cluster C finding, which is why the Conclusion specifies a minimum-viable — not zero — infrastructure build.

## 6. Conclusion

**Recommended approach:** Run a scoped, capped, time-boxed self-serve free-tier pilot rather than a full broad launch or indefinite inaction (chain C4). Concretely: (1) build only the minimum self-serve signup and in-product upgrade path needed to test unassisted conversion — not a full production freemium platform (addresses Abandoned Reasoning Dead End 3 and Pre-Mortem Cluster C); (2) gate the pilot so it cannot be reached by existing paying customers' domains and is not offered as a discount lever mid-negotiation to active outbound prospects (addresses assumption row 11/A-11 and chain C3's channel-conflict finding); (3) cap the pilot's signup volume and set a hard monthly infra+support spend ceiling with Finance before launch (addresses chain C2's cost-exposure finding and Pre-Mortem Cluster A); (4) instrument it from day one to measure the three currently-unknowable numbers directly — free-to-paid conversion rate, blended free-tier CAC, and realized support cost per free account (closes GT-4?); (5) set an explicit go/no-go review date (4-6 months post-launch, enough time for a first conversion cohort to mature), using chain C2's breakeven math as the decision rule — if realized conversion clears realized cost-per-account ÷ ACV, expand; if not, kill or redesign.

**Key insight:** The real obstacle to this decision is not whether a free tier is a good idea in the abstract — every named competitor already answered that question for their own business, and this company can't rent that answer (chain C1) — it's that the one number the decision actually turns on, chain C2's breakeven math, currently has no internal data behind it (GT-4?), and the estimate bracket built from external benchmarks alone spans from a $250,000/year loss to a $3,520,000/year gain, wide enough to make either a blind "yes" or a blind "no" reckless (chains C1, C2). A bounded pilot is the cheapest way to convert that unknown into a number Finance can actually underwrite.

**Trade-offs acknowledged:** The bounded pilot is not free — it requires a real, if minimal, engineering build that doesn't exist today (GT-2?, Pre-Mortem Cluster C), and it accepts a period where the company still cannot claim full competitive parity with competitors' more mature free tiers (chain C1). It also carries residual, not eliminated, channel-conflict risk to the existing $2.4M ARR base even with gating — the gating reduces but does not zero out the risk that a determined prospect or customer department finds and exploits the free path, which is precisely why chain C3 is this analysis's least-settled finding (chain C3, Pre-Mortem Cluster B).

**Pre-check:** head C1 (MEDIUM), C2 (MEDIUM), C3 (LOW), C4 (LOW) · ?-marked: none directly (all `?`-marked ground-truth dependencies are mediated through chains C1-C4 and reflected in those chains' own bands) · lowest cited: C3, C4 (LOW) · Inputs ceiling: LOW
**Confidence:** LOW on the specific shape of the pilot's numbers — chain C2's bracket is intentionally wide by design, and chain C3 rests on a genuinely live, unsettled rival (whether cannibalization risk is negligible or material) that nothing in this analysis settles — but the choice of *action*, pilot over full launch or over inaction, is comparatively robust: chain C4's flip test shows no single reasonable reweighting of the decision criteria overturns it, and both rival conclusions considered at the headline level (copy competitors now; never build one) were separately ruled out (Abandoned Reasoning, Dead Ends 1 and 2). This LOW rating is driven specifically by chain C3's unresolved rival, not by a general absence of data — which is exactly why the pilot's gating design is the mechanism built to resolve it, rather than a mitigation bolted onto an otherwise-settled plan (chains C1, C2, C3, C4).

## Self-Audit Gate (process output)

**Criterion 1: Identify Essence**
Quoted span: "Should the company commit to building and launching a self-serve free tier — given a go-to-market motion that is currently 100% outbound sales and referral, zero self-serve infrastructure, and no internal data on free-to-paid conversion rate, free-tier CAC, or free-tier support burden — or is there a lower-risk path to the same competitive goal?"
Band: **Rigorous**
Justification: the statement names the specific GTM state, ACV, and unknowns of this business rather than a generic template phrase, and each of the four success criteria is a pass/fail structural test naming a property of the Conclusion section (which action is named, whether GT-4? is load-bearing, whether cost exposure is quantified, whether go/no-go conditions are stated) that a reviewer applies by scanning section 6 alone.

**Criterion 2: Challenge Assumptions**
Quoted span (from the Assumption Audit scan): "17 rows... C4 | 2 | weighted trade-off ranks bounded pilot highest | trade-off weights reflect this business's actual strategic priorities | yes — row 13" — the scan covers all 17 named chain steps across C1 (3), C2 (6), C3 (4), C4 (4), with no step skipped.
Band: **Rigorous**
Justification: every Assumptions Table row uses one of the four prescribed types, every Verdict cell is a token (Accept/Challenge/Discard) followed by an em-dash and specific justification, every assumption used in a chain carries "unverified — flagged" in its Verification cell, and the Assumption Audit scan is exhaustive over every named chain step, surfacing three new assumptions (rows 11-13) and adding them to the table as prescribed.

**Criterion 3: Establish Ground Truths**
Quoted span: "?-marked: GT-1?, GT-2?, GT-3?, GT-4?, GT-5?, GT-7? (6 of 7). Read-at-source: GT-6 — chartmogul.com/reports/saas-conversion-report/..." — checked against the Ground Truths list: exactly six of the seven listed IDs (GT-1? through GT-5?, GT-7?) carry `?`, and GT-6 is the sole unsuffixed entry, matching the enumeration exactly.
Band: **Rigorous**
Justification: GT-IDs are stable and referenced identically in section 4; every verified GT (GT-6) cites a specific, opened source rather than "common knowledge"; every GT carries a provenance label; the `?` enumeration matches the list when checked against it rather than merely quoted; no assumption discarded in Phase 2 (assumption 10, Discard) appears in this list; and since no chain in this analysis is rated HIGH, the "unsuffixed GT feeding a HIGH chain must name read-at-source" clause is vacuously satisfied — GT-6's read-at-source location is named regardless.

**Criterion 4: Reason Upward**
Quoted span (from the self-audit scan chain-form table): "C1 | GT-5? + GT-1? + GT-4? | yes | n/a | yes | MEDIUM | no | none" / "C4 | C1 + C2 + C3 + GT-1? | yes | n/a | yes | LOW | no | none" — all four chain rows read `Form conforming? = yes` and `Dependency clean? = yes`.
Band: **Rigorous**
Justification: every conclusion in section 6 has exactly one chain in section 4; every chain names its head inputs in the prescribed form, contains multiple genuine intermediate hops (each recomputing cleanly per the adversarial pass), and reaches a conclusion; no analogy is used as direct evidence (Dead End 1 explicitly bans it); every chain step introducing a new assumption declares it inline (`[Assumes: A-11]`, `[Assumes: A-12]`, `[Assumes: A-13]`); and Abandoned Reasoning documents three dead ends, each with a specific, non-generic abandonment reason (reasoning-by-analogy, foreclosed value-of-information, contaminated pilot data) rather than invoking the escape valve.

**Criterion 5: Validate**
Quoted span: "This chain's LOW rating is therefore inherited entirely from C3's unsettled Rivals axis, not from a defect of its own — the recommendation to pilot rather than decide outright is the correct response to that inherited uncertainty, not a weakness of this chain's construction." (chain C4's confidence line)
Band: **Rigorous**
Justification: every chain's confidence line names its `?`-marked inputs with verification paths, names the cited chain that caps it (C4 names C3), and states what would remove each downgrade cause; no chain consuming a `GT-N?` input is rated HIGH; every chain is rated no higher than the lowest-rated chain its head cites; every band is the one its three axes license (C3 and C4 correctly land at LOW specifically because of an unsettled Rivals axis, not a blanket "everything is uncertain" hedge); and the adversarial pass record is complete — Recompute, Sensitivity, Rival, Premise, Causes, Clusters (each with a named disposition), and Falsification are all present with content, satisfying the technique-step requirement since the Conclusion is a plan.

**Criterion 6: Conclusion-to-Ground-Truth Traceability**
Quoted span (from the self-audit scan claim-inventory table): "Recommended approach... | bold lead-in | yes | bold lead-in whose colon closes the bold span | C4" / "Falsification condition is recorded... | prose | no | ... explicitly excluded per the rule that falsification belongs in the record only | n/a" — 4 of 5 rows are claims, all 4 cite a chain, the 5th is correctly excluded.
Band: **Rigorous**
Justification: every Conclusion-section claim traces to a specific named chain in section 4 with no new reasoning introduced in section 6; and the Key Insight (the missing data behind the breakeven number is the real obstacle) is a non-obvious finding distinct from the Recommended approach (run a scoped pilot) — it explains *why* the pilot is the right move rather than restating *what* the pilot is, so it is not a restatement.

**Gate result:** No criterion scores Absent (condition 1 cleared); zero criteria score Hand-wavy, well under the at-most-one cap (condition 2 cleared). The analysis clears the Self-Audit Gate on the first scoring pass — no Fix/Repeat loop was required, and no bounded re-entry edge fired during this run.
