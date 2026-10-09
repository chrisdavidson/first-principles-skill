## Answer

**Recommendation:** Do not launch an unlimited, company-wide free tier now, and don't add one merely because competitors have one (chain C1, chain C2). Instead, run a capped, time-boxed, single-segment freemium-lite pilot — it beats the status quo and a sales-assisted trial in the trade-off (chain C3) — gated by a named owner, an enforced signup cap and end date, PQL lead-routing, and committed Finance cost-tracking (chain C4).

**Band (from §6):** MEDIUM

**Would change it:** The real $/active-free-user cost from Finance would tighten chain C5's breakeven bracket, and the pilot's own measured conversion rate would resolve the uncertainty behind chains C1 and C5.

## 1. Problem Essence

**Core problem:** Given a profitable, enterprise-leaning B2B SaaS business ($2.4M ARR, 240 paying teams, ~$10K ACV) built entirely on outbound sales and referrals — with no self-serve motion, no freemium experience, and a Finance-confirmed real, scaling (not near-zero) cost attached to every active free user — should the company add a free tier as a lever for more scalable, lower-CAC acquisition, and if so, in what form and on what timeline?

**Success criteria:**
1. The Conclusion names a specific recommended form of action (not a bare yes/no to "add a free tier") and states whether it is launched now, piloted first, or deferred.
2. The Conclusion explicitly tests, rather than assumes, "competitors have a free tier" and "a free tier drives growth," and cites the chains that tested them.
3. The Conclusion states a confidence band and names the single most decision-moving piece of missing evidence.
4. The Conclusion names a concrete, low-cost next step that would de-risk a fuller commitment, with a stated go/no-go signal.
5. The Conclusion addresses second-order consequences on sales motion, support load, and brand/competitive optics, not only the headline acquisition question.

## 2. Assumptions Table

### 5-Whys (causal mode) on the real motivation

**Symptom:** Leadership is asking whether to add a free tier.
Why? → Acquisition today is 100% outbound + referral, and leadership wants a cheaper, faster, more scalable top-of-funnel motion (outbound cost and rep time scale roughly linearly with each new logo).
Why does that scaling feel urgent now specifically? → All named competitors already offer a free tier (GT-5?), creating competitive-optics pressure and fear of losing self-serve comparison-shopping visibility.
**Counterfactual test:** had competitors not offered a free tier, would the question still be live, given the outbound-scaling concern? Plausibly yes, with less urgency — so competitive-optics pressure is a **contributing condition**, not the counterfactually necessary cause.
Why is "add a free tier" specifically the proposed fix, rather than more outbound capacity, channel/partner motion, paid marketing, or a lower-friction sales-assisted trial? → No evidence any of those levers were compared; "ship a free tier" reads as the default SaaS-growth-playbook answer to "we want scalable growth," not a conclusion reached by comparing levers.
**Root cause — within control:** leadership wants lower-CAC, more scalable acquisition than a 100%-outbound motion provides, and reached for the free-tier playbook by default/competitive mimicry rather than after comparing it against other acquisition-scaling levers. **Corrective action:** widen the evaluation to include non-freemium levers aimed at the same goal — done below by including a sales-assisted trial as a scored alternative in the trade-off (section 4).

This reframes the question: "should we add a free tier" and "how do we get scalable, lower-CAC acquisition" are not the same question, and the second is the one actually worth answering (feeds the Conclusion's Key Insight).

### Fishbone: what would actually drive free→paid conversion

Effect framed positively: *a free tier converts free users to paying teams at a commercially viable rate.* Custom categories (the standard 6M/8P/4S sets do not fit a PLG-funnel question; the default six-category set is a poor fit too, since "People/Process/Technology" cuts across every funnel stage at once).

| Category | Candidate driver | Discriminating observation | Status |
|---|---|---|---|
| Product Fit & Time-to-Value | Free users reach a meaningful outcome unassisted | Does current (sales-assisted) onboarding require a CS call to reach first value? Not stated — if yes, self-serve activation is unproven. | Unverified → A-14 |
| Product Fit & Time-to-Value | Value is realizable by one user alone, not only a coordinated team | Does the product's core value require >1 active seat? Not stated. | Unverified → A-14 |
| Packaging & Caps | Free tier gates exactly the capability that makes paying teams pay | Can we name the feature/usage threshold where paying customers say the product became indispensable? Not given. | Unverified → A-10 |
| Distribution & Discovery | A pre-existing discovery surface (SEO/content/community) lets free signups find the product without paid spend | GT-2? states 100% outbound + referral today — **no inbound motion exists yet**, which is evidence *against* this driver being present, not for it. | Contradicted-for-now → A-13 |
| Sales & CS Handoff | A defined PQL signal and routing rule connects free usage to a human seller before churn | Does any lead-scoring/routing exist today? Not stated. | Unverified → feeds pre-mortem Cluster 2 |
| Buyer Structure & Pricing Psychology | Free signups include the actual budget-holder, not only individual evaluators with no purchase authority | Who initiates contact for the 240 current paying teams — an individual user or an existing buying-committee member? Not given. | Unverified → A-15 |

The one driver this analysis can check against a given fact (Distribution & Discovery) comes back **negative in the near term**: GT-2? directly contradicts "a free tier will create its own top-of-funnel," because there is no discovery surface for it to ride on yet. This is the fishbone's most decision-relevant finding and is carried into A-2 and A-13.

### Inversion: what would guarantee the recommended pilot is the wrong move

The emerging conclusion — "a bounded pilot is a safe, low-risk way to explore scalable acquisition" — feels clean enough to invert before trusting it. Inverted claim: *the pilot fails to produce a decision-useful answer, or actively harms the business.* Failure-guaranteeing conditions (at least five, unfiltered):

1. Free users never reach the product's core "aha" value unassisted.
2. No PQL/lead-routing mechanism exists, so even successful free usage never reaches a human seller.
3. The pilot's signup cap is not enforced and signups run unbounded in practice.
4. Free-tier support demand exceeds capacity and degrades paying-customer support.
5. Free signups come overwhelmingly from people without purchase authority, so "successful" usage never reaches a buyer.
6. Finance never actually measures $/free-user cost during the pilot, so it produces a conversion rate but not the other half of the breakeven question.
7. The existing sales team deprioritizes free-tier-sourced leads because they are not compensated on them.

**Necessary preconditions derived** (each a checkable assertion, not a topic): free users can reach core value unassisted (= A-14); a PQL/routing mechanism connects free usage to a seller (**new — A-18**); the cap/sunset is enforced in product, not policy (= A-12); free-tier support demand stays within capacity (= A-7); free signups include people with real purchase authority (= A-15); Finance measures and reports $/free-user cost during the pilot (**new — A-19**).

**Load-bearing tags:** A-18 and A-19 are both **load-bearing** — without A-18, the pilot cannot distinguish "free usage that never reached a seller" from "free usage that reached a seller and was rejected," defeating its purpose as a learning vehicle; without A-19, chain C5's breakeven question cannot actually be answered by the pilot, which is exactly what C4's "learning value" score of 5/5 assumed would happen. A-14, A-12, A-7 and A-15 were already tabled from the fishbone and second-order passes above; A-18 and A-19 are new and are the sharpest findings of this pass — reported first, per the inversion procedure, ahead of the rest of the list.

### Classified Assumptions Table

| Assumption | Type | Treatment | Verdict | Verification |
|---|---|---|---|---|
| A-1: Competitors having a free tier means we need one too | convention | Explicitly challenge before use | Challenge — disanalogous GTM motion/buyer type (GT-1?, GT-2? vs GT-5?); downweighted to a minor factor, not a decisive one (chain C2) | unverified — flagged |
| A-2: A free tier will meaningfully drive growth/acquisition | untested belief | Verify or flag | Challenge — no internal data (GT-4?) and the fishbone's Distribution/Discovery branch is currently absent, not present (GT-2?) | unverified — flagged |
| A-3: Free-tier costs are a near-zero-marginal-cost loss leader | convention | Explicitly challenge before use | Discard — directly contradicted by GT-3? (Finance's confirmed fact that costs scale with active users) | Finance-confirmed per prompt; not independently re-opened by this analysis, so GT-3? itself still carries a `?` |
| A-4: Our product/ICP is suited to self-serve evaluation without a sales touch | untested belief | Verify or flag | Challenge — the 100%-outbound history (GT-2?) is silent on this at best, and the buyer-structure fishbone branch raises real doubt | unverified — flagged |
| A-5: A free tier won't cannibalize or complicate existing paid relationships/renewals | untested belief | Verify or flag | Challenge — surfaced explicitly by the pre-mortem (Cluster 3, Appendix) | unverified — flagged |
| A-6: The real need is best solved specifically by a free tier, versus other acquisition levers | untested belief | Verify or flag | Challenge — the 5-whys root cause above shows "free tier" is a default answer, not a compared one | unverified — flagged |
| A-7: Spare eng/support capacity exists to build and operate a free tier without diverting from the paid roadmap/queue | current constraint | Record expiry conditions | Challenge — expires once capacity is explicitly allocated or hired; until then it is a real resourcing constraint (pre-mortem Cluster 2) | unverified — flagged |
| A-8: A free tier materially improves brand/competitive perception for this buyer, even though enterprise-ish buyers don't comparison-shop like self-serve PLG buyers | convention | Explicitly challenge before use | Challenge — down-weighted in the trade-off (lowest weight of six criteria) given GT-1?/GT-2? | unverified — flagged |
| A-9: Free users who never convert still provide latent value (feedback/brand/referral) that offsets their cost | untested belief | Verify or flag | Challenge — plausible but unquantified; not used as load-bearing support anywhere in this analysis | unverified — flagged; non-load-bearing |
| A-10: A free tier can be packaged so it doesn't satisfy the whole need for free forever | untested belief | Verify or flag | Challenge — exactly the fishbone's Packaging & Caps gap; unresolved without pilot data | unverified — flagged |
| A-11: The freemium decision is cheaply reversible if it doesn't work | convention | Explicitly challenge before use | Discard-as-stated — the pre-mortem and second-order analysis (chain C4) show reversibility is not automatic; a guarded version ("reversible *if enforced*") survives as A-12 | unverified — flagged |
| A-12: Leadership will enforce the pilot's hard signup cap and sunset date even if early signups look promising *[surfaced in End-of-phase Assumption Audit, chain C4]* | untested belief | Verify or flag | Challenge — the single largest execution risk named by the pre-mortem (Cluster 1) | unverified — flagged; requires a named owner and a product-enforced (not policy-only) cap |
| A-13: A self-serve discovery/distribution surface exists or will emerge for free signups *[from fishbone]* | untested belief | Verify or flag | Challenge — contradicted in the near term by GT-2? (no inbound motion exists today) | unverified — flagged |
| A-14: The product's core value is realizable by a single unassisted user, not only a coordinated team *[from fishbone]* | untested belief | Verify or flag | Challenge — unknown from given facts; determines whether self-serve activation is even possible | unverified — flagged |
| A-16: The 1–5 trade-off scores assigned to each option validly proxy the underlying criteria, even where not grounded in measured data *[surfaced in End-of-phase Assumption Audit, chain C3]* | untested belief | Verify or flag | Challenge — mitigated, not resolved, by the flip test showing the ranking is robust to single-criterion weight changes (chain C3) | unverified — flagged; robustness check substitutes for direct verification |
| A-17: Program cost and incremental revenue scale linearly with free-signup volume — no economies/diseconomies of scale in support cost, no network/referral effects from free users *[surfaced in End-of-phase Assumption Audit, chain C5]* | untested belief | Verify or flag | Challenge — a simplifying first-order model; untested in either direction | unverified — flagged |
| A-18: A PQL/lead-routing mechanism connects free usage to a human seller before a free user churns out *[from inversion; load-bearing]* | untested belief | Verify or flag | Challenge — not stated to exist today; without it the pilot cannot tell successful-but-unrouted usage from rejected usage | unverified — flagged; load-bearing for the pilot's learning-value score (chain C3/C4) |
| A-19: Finance actually measures and reports $/active-free-user cost during the pilot window *[from inversion; load-bearing]* | untested belief | Verify or flag | Challenge — GT-3? confirms the cost scales but no monitoring commitment is given; without it C5's breakeven question stays unanswered even after the pilot runs | unverified — flagged; load-bearing for chain C5 and for GT-7?'s verification path |
| A-15: Free signups will reach the actual budget-holder, not only individual evaluators with no purchase authority *[from fishbone]* | untested belief | Verify or flag | Challenge — unknown; bears on whether any free-tier motion can close $10K/yr deals unassisted | unverified — flagged |

## 3. Ground Truths

- **GT-1?** Current state: $2.4M ARR from 240 paying teams, average ACV ≈ $10,000/team/year — unverified: stated by the requester as a known internal fact; no independent source document (e.g., a billing-system export) was available to this analysis to open and check against.
- **GT-2?** Customer acquisition today is 100% outbound sales + referrals; no self-serve inbound channel exists today — unverified: stated by the requester; no CRM/attribution data was opened by this analysis.
- **GT-3?** Finance has confirmed free-tier infrastructure and support costs scale with active (free) users, not with paying users — a real, scaling cost center, not a near-zero-marginal-cost loss leader — unverified: stated by the requester as Finance's conclusion; this analysis did not independently open Finance's cost model. **This is the single most load-bearing unverified input in the analysis — see the Sensitivity finding in the Appendix.**
- **GT-4?** The company has never run a freemium pilot and has no internal data on free-to-paid conversion rate — unverified (self-report by the requester about their own data state; a negative-existence claim about the requester's own knowledge, lower-risk to be wrong than most `?` entries, but still carries the suffix per the Input Contract's rule that a supplied fact naming no source enters as unverified).
- **GT-5?** All competitors in this product space currently offer a free tier — unverified: stated by the requester; this analysis did not independently audit named competitors (none were named) or their buyer segments.
- **GT-6?** Commonly cited industry benchmarks (frequently attributed to OpenView Partners' SaaS Benchmarks research) put median B2B SaaS freemium free-to-paid conversion around 2–5%, with wide variance by category (roughly 1–2% for productivity tools, 5–10%+ for enterprise-grade/dev-tool products), and freemium-to-paid conversion structurally well below trial-to-paid conversion — reported-by-delegate / unverified: this analysis ran two web searches and could not locate or open the original OpenView report; every citing page found was a secondary aggregator, several evidently low-quality SEO content (e.g., pages dated 2026/2027 suggesting auto-generated content). Treated only as a **directional, low-confidence industry anchor**, not as a number this company's own funnel should be assumed to match — the buyer type implied by GT-1? (high ACV, multi-stakeholder) and the total absence of self-serve motion in GT-2? are both disanalogies from the PLG companies this benchmark is usually drawn from.
- **GT-7?** Assumed fully-loaded cost per active free user: $20–$150/year — unverified: no company-specific unit-cost figure was supplied; this is a defensible generic-SaaS-infra-plus-support magnitude bracket (per the Estimate procedure's "assumed, flagged" allowance), not a measured figure. Finance has confirmed costs scale with active users (GT-3?) but no $/user figure was given in the inputs to this analysis — **this is the single cheapest, highest-value number to obtain before any further decision** (see Conclusion).
- **GT-8?** Assumed revenue per newly-converted free→paid customer: $3,000–$10,000/year, i.e. 30–100% of the current ACV in GT-1? — unverified: assumed bracket reflecting the likelihood that free-tier converts skew toward smaller teams than the current outbound-sourced book; no company-specific data exists.

**Provenance summary.** `?`-marked: GT-1, GT-2, GT-3, GT-4, GT-5, GT-6, GT-7, GT-8 (8 of 8). No ground truth in this analysis is read-at-source: every input is either a fact stipulated directly by the requester about their own company with no external document named (per the Input Contract, such facts enter as unverified, not as ground truth by default), a claim this analysis attempted to verify externally and could not fully source (GT-6?), or an explicitly assumed bracket (GT-7?, GT-8?). This is a materially data-thin analysis, and that thinness is the central finding, not an incidental caveat — see the Conclusion and the de-risking experiment it names.


## 4. Derivation Chains

### Conclusion C1: An unlimited, company-wide freemium launch now is a high-stakes bet on an unmeasured number, not a low-risk growth experiment

GT-3? (Finance: free-tier cost scales with active users) + GT-4? (no freemium pilot ever run; conversion rate unknown) + GT-1? (ACV ≈ $10,000/team/year, enterprise-leaning buyer)
→ an uncapped free tier commits the company to an open-ended, scaling cost line item whose size depends entirely on a conversion rate nobody has measured
→ at this ACV, that is a single, highly-levered bet rather than a cheap-to-run loss leader
→ launching an unlimited, company-wide freemium tier now is a high-stakes bet on an unmeasured number, not a low-risk growth experiment

**Pre-check:** head GT-3?, GT-4?, GT-1? · ?-marked: GT-3?, GT-4?, GT-1? · lowest cited: none · Inputs ceiling: MEDIUM
**Confidence:** MEDIUM — GT-3?, GT-4? and GT-1? are each unverified by this analysis (section 3); the verification that would remove each as a cause of the downgrade is opening Finance's cost model (GT-3?), running the pilot recommended in C3/C4 below (GT-4?), and pulling the actual billing-system ARR/ACV figures (GT-1?). The rival reading — "the real cost is trivial, so this is low-risk after all" — is exactly what GT-3? asserts is false; see the Sensitivity finding in the Appendix, which names GT-3? as the single fact whose falsity would flip this conclusion.

### Conclusion C2: "Competitors have a free tier" is weak evidence on its own for this company

GT-5? (all named competitors offer a free tier) + GT-1? (ACV ≈ $10,000/year, outbound/referral-driven buyer) + GT-2? (no self-serve channel exists today)
→ competitors offering a free tier is evidence about their GTM motion and buyer type, not about this company's, unless the two are shown comparable
→ with zero self-serve motion and a sales-cycle buyer, this company's funnel looks less like the self-serve PLG companies the "everyone has one" claim is usually drawn from
→ competitive-parity alone is weak justification and does not by itself warrant adding a freemium tier

**Pre-check:** head GT-5?, GT-1?, GT-2? · ?-marked: GT-5?, GT-1?, GT-2? · lowest cited: none · Inputs ceiling: MEDIUM
**Confidence:** MEDIUM — all three head inputs are unverified (section 3); the verification that would remove each as a cause of the downgrade is naming and auditing the actual competitors and their buyer segments (GT-5?), and pulling internal GTM/billing data (GT-1?, GT-2?). The only genuine rival to this chain's actual claim — that an unshown competitor-parity analogy is, by itself, sufficient justification — is ruled out by the ban on using analogy as direct evidence without a grounding fact about comparability (Abandoned Reasoning, the dead end on treating competitor parity as sufficient justification); a rival claiming parity matters *at all* would not contradict this chain, which only disputes the sufficiency of this one unshown analogy, not the general relevance of parity.

### Conclusion C3: A capped, time-boxed, single-segment pilot beats both the status quo and a sales-assisted trial

**Trade-off analysis — options compared.** Options always include the status quo and a composite: **A — status quo** (no free tier); **B — full open-ended freemium**, company-wide, unbounded signups; **C — sales-assisted structured free trial** (14–30 days, full-featured, routed to existing SDR/AE capacity); **D — freemium-lite rolled out company-wide**, uncapped signup volume; **E — composite:** a volume-capped, time-boxed, single-segment pilot of a capped "freemium-lite" tier, run as an explicit instrumented experiment with a hard signup ceiling and a kill-switch, purpose-built to generate the missing conversion data (GT-4?).

**Must-haves (knockouts, applied before scoring):** must not create an open-ended, unbounded cost commitment before conversion data exists, since GT-3? confirms real per-user scaling cost and GT-4? confirms zero internal conversion data. Options B and D both fail this — both make total cost a direct function of an uncapped signup volume nobody has bounded in advance — and neither is scored (see Abandoned Reasoning, Dead End 1).

**Criteria and locked weights** (locked before any option was scored): Cost exposure/downside bound (5), Learning value / de-risking (5), Fit with current GTM motion (4), Reversibility (4), Expected acquisition-channel value (3), Brand/competitive-parity signal (2 — reflecting A-1/A-8's weak evidentiary standing from C2).

**Anchors (1/5):** Cost exposure: 1 = spend uncapped and scales with uncontrolled signup volume, 5 = a pre-set hard ceiling approved in advance. Learning value: 1 = produces no new conversion data, 5 = produces a directly measurable free→paid rate for this ICP within 6 months. Fit with GTM motion: 1 = requires an all-new self-serve support function from scratch, 5 = routes entirely through existing sales/CS capacity. Reversibility: 1 = cannot be shut down without brand/press consequences, 5 = ends at a stated date with no user ever promised permanence. Acquisition-channel value: 1 = no plausible new top-of-funnel signal, 5 = a durable new self-serve channel at full scale. Brand/parity signal: 1 = no change to "do they have a free tier" comparisons, 5 = fully closes the gap.

| Criterion (weight) | A: Status quo | C: Sales-assisted trial | E: Capped single-segment pilot |
|---|---|---|---|
| Cost exposure (5) | 5 | 4 | 5 |
| Learning value (5) | 1 | 3 | 5 |
| Fit with GTM motion (4) | 5 | 5 | 3 |
| Reversibility (4) | 5 | 4 | 5 |
| Acquisition-channel value (3) | 1 | 3 | 2 |
| Brand/parity signal (2) | 1 | 2 | 2 |
| **Weighted total** | **75** | **84** | **92** |

**Flip test:** the E–C margin is 8 points. Checking every single-criterion weight move within the locked 1–5 scale, the largest lever is Learning value (weight 5, E−C score diff +2) — dropping its weight to 1 only **ties** E and C (margin → 0) and does not hand the win to C. Every other single-criterion move shifts the margin by less and does not reach zero. **No single-criterion weight change flips the winner** — a robust result, not a near-tie.

GT-3? (Finance: free-tier cost scales with active users) + GT-4? (no conversion pilot ever run) + GT-2? (100% outbound/referral GTM, no self-serve channel)
→ scoring cost exposure, learning value, GTM fit, reversibility, acquisition value and brand signal across the status quo (A), a sales-assisted trial (C), and a capped single-segment pilot (E) yields weighted totals A=75, C=84, E=92, a margin the flip test shows is not reversed by any single-criterion weight change
→ the capped, time-boxed, single-segment pilot (Option E) is the preferred near-term move, ahead of both the status quo and a sales-assisted trial

**Pre-check:** head GT-3?, GT-4?, GT-2? · ?-marked: GT-3?, GT-4?, GT-2? · lowest cited: none · Inputs ceiling: MEDIUM
**Confidence:** MEDIUM — all three head inputs are `?`-marked (section 3); the verification that would remove each as a cause of the downgrade is: for GT-3?, opening Finance's actual cost model (also tightens GT-7?); for GT-4?, running the pilot this chain itself recommends; for GT-2?, no action is strictly needed since it is a negative-existence claim the requester is positioned to know firsthand and is low-risk to be wrong. The live rival — Option B (full freemium now) — is ruled out structurally before scoring, not out-scored; see Abandoned Reasoning, Dead End 1.

### Conclusion C4: The pilot is net favorable only if paired with binding operational guardrails

**Second-order extension — can the pilot actually stay bounded?** Actor lens: support/CS must triage a new, lower-SLA ticket queue; the existing outbound sales team starts seeing "I'm already using the free version" inbound leads that don't fit their outbound playbook or comp plan; a competitor who notices a small, capped pilot may market against it as "a late, half-hearted free tier." Time lens: immediately, nothing changes operationally; after a few cycles, "raise the cap, we're leaving growth on the table" becomes a normal internal argument; once the pilot has run long enough to be assumed rather than questioned, nobody revokes access already granted, because revoking active users is itself an unpleasant, deferrable decision.

C3 (capped, time-boxed, single-segment pilot wins the trade-off, MEDIUM)
→ a bounded pilot's scored advantages (cost exposure 5/5, reversibility 5/5) hold only if the cap and sunset date are actually enforced in product and process rather than declared in a memo
→ organizational inertia can turn an uncapped-in-practice pilot back into the same unbounded cost exposure that knocked Options B and D out of scoring entirely *[Assumes: A-12 — leadership enforces the cap/sunset date; if this fails, the pilot's bounded/reversible properties do not hold and it converges toward Option B/D's already-rejected risk profile]*
→ the pilot is net favorable only when paired with a named owner, a product-enforced signup cap and end date, a PQL/lead-routing mechanism, committed Finance cost-tracking, and a scheduled go/no-go decision point *[Assumes: A-18, A-19 — a lead-routing mechanism and committed cost-tracking exist; without them the pilot cannot produce the learning it was scored 5/5 on in C3]*

**Pre-check:** head C3 (MEDIUM) · ?-marked: none · lowest cited: MEDIUM · Inputs ceiling: MEDIUM
**Confidence:** MEDIUM — capped by C3's own MEDIUM rating (lowest-rated chain its head cites). The `[Assumes: A-12, A-18, A-19]` premises on the third hop are priced, not merely flagged: the hop states what happens to the conclusion if any fails (it converges toward the already-rejected Option B/D risk profile, or produces a pilot that cannot answer the question it was run for), which is why this stays at C3's ceiling rather than dropping to LOW. Each assumption's own verification path is a named accountable owner plus a product-level enforcement mechanism for A-12, a built PQL/routing rule for A-18, and a monthly Finance report for A-19 (see Conclusion, section 6, and the pre-mortem's Cluster 1/2 dispositions in the Appendix). The Rivals axis is clean here: the pre-mortem's "inertia concern is overstated" consideration is not a rival conclusion from the same ground truths — this chain's conclusion is explicitly conditional ("favorable only when paired with..."), and a claim that the condition usually holds in practice disputes a probability, not the conditional logic itself; that probability question is exactly what the pre-mortem's Cluster 1 disposition exists to manage.

### Conclusion C5: The free-tier economics are genuinely conversion-rate-sensitive, not clearly favorable or unfavorable

GT-7? (assumed cost-per-active-free-user, $20–150/yr) + GT-8? (assumed ACV of a free→paid convert, $3,000–10,000/yr) + GT-6? (industry freemium conversion benchmark ≈2–5%, low-confidence)
→ modeling program cost as signups × cost-per-user and incremental revenue as signups × conversion rate × converted-ACV reduces the decision to whether the breakeven conversion rate — cost-per-user divided by converted-ACV — sits below or above plausible real-world conversion rates
→ bracketing the breakeven rate across GT-7?'s and GT-8?'s ranges gives roughly 0.2% at the favorable end and 5% at the unfavorable end, with an illustrative central value near 1.3%, a range whose two ends do not agree against the ≈2–5% benchmark in GT-6?
→ the program's economics are genuinely conversion-rate-sensitive rather than clearly favorable or unfavorable, which is itself the strongest argument for measuring the real rate cheaply before committing capital to either a full launch or a permanent rejection

**Pre-check:** head GT-7?, GT-8?, GT-6? · ?-marked: GT-7?, GT-8?, GT-6? · lowest cited: none · Inputs ceiling: MEDIUM
**Confidence:** MEDIUM — all three head inputs are unverified assumed brackets or an unopened secondary benchmark (section 3); the verification that would remove each as a cause of the downgrade is: for GT-7?, Finance supplying the real $/active-free-user figure it already has the data to compute (GT-3? confirms the cost scales, so the number exists internally); for GT-8?, measuring realized ACV from the pilot's actual conversions; for GT-6?, locating and opening the primary OpenView report rather than secondary citations. The rival — "the bracket is too wide to be decision-useful" — is addressed directly: the bracket straddling the threshold is itself the finding (the decision is genuinely data-sensitive), not a defect of the estimate; see the Recompute step in the Appendix for the independent arithmetic check.


## 5. Abandoned Reasoning

### Dead End: Full company-wide freemium (Option B), scored like the other options

**What was tried:** initially considered scoring Option B (an unlimited, company-wide freemium tier) in the same weighted trade-off matrix as the status quo, the sales-assisted trial, and the capped pilot.

**Why abandoned:** Option B fails a knockout must-have before any weighted score is meaningful — it creates an open-ended, unbounded cost commitment (per GT-3?) with zero conversion data to size the bet (per GT-4?). Scoring it anyway would let a high weighted total out-vote a hard constraint, which is exactly the failure mode the must-have step of the trade-off procedure exists to prevent.

**What it ruled out:** this rules out jumping straight to full, company-wide freemium as this analysis's headline recommendation, and is why no comparative 1–5 scores were collected for Option B at all — scoring a non-viable option would have manufactured false precision about an option that was never really on the table.

### Dead End: Freemium-lite rolled out company-wide with uncapped signups (Option D)

**What was tried:** considered a "lighter" freemium tier (hard per-user feature/usage caps) but still offered broadly with no limit on total signup volume.

**Why abandoned:** fails the identical must-have as Option B through the identical mechanism — total program cost is signup volume × cost-per-user (GT-3?, GT-7?), and signup volume is uncapped, so per-seat caps bound nothing about total exposure.

**What it ruled out:** this rules out treating "make the free tier less generous per user" as a substitute for bounding total program cost — the two are independent levers, and only the composite pilot (Option E / Conclusion C3) bounds the one that actually matters for downside risk.

### Dead End: Treating "competitors have a free tier" as sufficient justification on its own

**What was tried:** initially considered simply recommending "ship a free tier because that is now standard practice in this market," using competitor behavior as direct evidence.

**Why abandoned:** this is reasoning by analogy without grounding in a named fact about whether competitors' buyers and GTM motion resemble this company's — the methodology explicitly bans using "others do it this way" as standalone justification, and GT-5? names only that competitors have a free tier, not that their buyer type or funnel resembles GT-1?/GT-2?.

**What it ruled out:** this rules out "ship a free tier purely for competitive optics" as a decisive, standalone argument; the underlying concern is folded into C3's trade-off as the lowest-weighted of six criteria rather than treated as decisive.

### Dead End: Calling an uncapped rollout a "pilot" and relying on intent alone to keep it reversible

**What was tried:** considered recommending Option B/D but simply labeling it "a pilot we can shut down if it doesn't work," without a product-enforced cap or calendar sunset.

**Why abandoned:** the second-order analysis in C4 shows organizational inertia — nobody revokes access already granted — turns an unenforced "pilot" into a permanent commitment regardless of what it is called; the label does no work on its own.

**What it ruled out:** this rules out treating "we'll call it a pilot" as sufficient; the recommendation instead requires an enforced cap, a named owner, and a calendar sunset as explicit preconditions (C4, section 6), not a label.


## 6. Conclusion

**Recommended approach:** Do not launch an unlimited, company-wide free tier now (chain C1), and do not treat competitor parity as sufficient reason to add one either (chain C2). Instead, run a capped, time-boxed, single-segment freemium-lite pilot — the option that outscores both the status quo and a sales-assisted trial in the trade-off (chain C3) — gated by five named preconditions: an accountable owner, a product-enforced signup cap and end date, a PQL/lead-routing rule into the existing sales motion, committed Finance cost-tracking per active free user, and a scheduled go/no-go decision at the end of the window (chain C4).

**Key insight:** "Should we add a free tier" and "how do we get scalable, lower-CAC acquisition" are different questions that competitive analogy collapses into one; the free-tier economics turn out to be genuinely conversion-rate-sensitive rather than obviously good or bad (chain C5), and the single highest-leverage missing fact — a $/active-free-user cost number Finance can already compute from data it confirmed it has — is cheap to obtain without betting the acquisition strategy on an unmeasured conversion rate (chain C1, chain C5).

**Trade-offs acknowledged:** running the pilot instead of either extreme means accepting slower validated learning than a full launch would have produced if it happened to work, accepting a real (if bounded) new support and engineering surface the roadmap must absorb, and accepting that a small, single-segment pilot will not deliver whatever competitive-optics benefit a full, publicly-visible freemium rollout might (chain C4; chain C2). It also means accepting a residual cannibalization/renegotiation risk among existing paying teams who notice the pilot exists, mitigated by restricting the pilot to a segment distinct from the current paid ICP rather than eliminated outright — no chain — flagged assumption only.

**Pre-check:** head C1 (MEDIUM), C2 (MEDIUM), C3 (MEDIUM), C4 (MEDIUM), C5 (MEDIUM) · ?-marked: none directly · lowest cited: MEDIUM · Inputs ceiling: MEDIUM
**Confidence:** MEDIUM — every contributing chain (C1–C5) is itself MEDIUM, each capped by `?`-marked ground truths this analysis could not read at source (section 3) rather than by any weak inference step; none is LOW, and none carries an unsettled rival that would push it lower, so MEDIUM is the matching, not the fallback, rating. The single piece of evidence most likely to move this band is the actual Finance cost-per-active-free-user figure (which would tighten GT-3?/GT-7? and directly narrow chain C5's breakeven bracket), followed by the pilot's own measured conversion rate (which would resolve GT-4? entirely and let a follow-on analysis replace C1 and C5's caution with a direct answer).

## Appendix — process output

## Assumption Audit scan (process output)

| Chain | Step | Step Text (brief) | Assumption surfaced? | Added to Table? |
|---|---|---|---|---|
| C1 | 1 | uncapped free tier → open-ended scaling cost tied to unmeasured conversion | none | n/a |
| C1 | 2 | at this ACV, that is a highly-levered bet | none | n/a |
| C1 | 3 (conclusion) | launching unlimited freemium now is a high-stakes bet | none | n/a |
| C2 | 1 | competitor behavior is evidence about their GTM, not ours, absent shown comparability | A-1 (already in table) | n/a — reference |
| C2 | 2 | zero self-serve motion + sales-cycle buyer looks unlike PLG comparators | none new | n/a |
| C2 | 3 (conclusion) | competitive parity alone is weak justification | none | n/a |
| C3 | 1 | weighted scoring across A/C/E yields totals 75/84/92, flip-test robust | A-16 | yes |
| C3 | 2 (conclusion) | capped single-segment pilot (E) preferred | none new | n/a |
| C4 | 1 | pilot's scored advantages hold only if cap/sunset enforced | A-12 | yes |
| C4 | 2 | organizational inertia risk `[Assumes: A-12]` | A-12 (reference) | n/a — reference |
| C4 | 3 (conclusion) | pilot favorable only with named owner + enforced cap + PQL routing + cost-tracking + go/no-go date | A-18, A-19 | yes |
| C5 | 1 | cost/revenue modeled as linear in signup volume, reducing to a breakeven-rate question | A-17 | yes |
| C5 | 2 | breakeven bracket ≈0.2%–5%, straddles ≈2–5% benchmark | none new | n/a |
| C5 | 3 (conclusion) | economics are genuinely conversion-rate-sensitive | none | n/a |

Scan complete: 14 steps across 5 chains, in order, no step skipped. Five assumptions newly surfaced across this audit and the Phase 2 inversion pass (A-12, A-16, A-17, A-18, A-19), each added to the Classified Assumptions Table (section 2) and marked inline on its originating or load-bearing step with `[Assumes: X]` (C4's steps 2 and 3); A-12's first mention (C3→C4 boundary, step 1) and A-1's reference (C2, step 1) are citations to an already-tabled row, not duplicate additions.

## Techniques not applied (process output)

- theoretical-limit (Phase 1 essence-reframe invocation) — not applicable — the essence question is a resource-allocation/GTM decision, not one where a current figure is plausibly a mere convention masking a hard physical ceiling; no reframe toward a law-permitted limit was available.
- theoretical-limit (Phase 4 ceiling-derivation invocation) — not applicable — no governing hard constraint (physical, mathematical, or protocol-level) bounds a freemium conversion rate the way thermodynamics bounds an engine; the relevant ceiling is the empirical industry benchmark (GT-6?), which the Estimate technique already incorporates as a bracket input to chain C5, not a theoretical-limit derivation.
- inversion (Phase 5 adversarial-technique invocation) — not applicable — the conclusion is a plan/recommendation (run a bounded pilot under named guardrails), and the decision rule assigns plans to pre-mortem rather than inversion; inversion was instead applied at Phase 2 (section 2) on the assumption space, which is its other invocation point and did fire.

## Adversarial pass (process output)

**Recompute.** C5's arithmetic, redone independently of the chain text: breakeven rate = cost-per-free-user ÷ converted-ACV. Favorable end: $20 ÷ $10,000 = 0.20%. Unfavorable end: $150 ÷ $3,000 = 5.00%. Illustrative central point, using the arithmetic midpoint of each bracket ($85/yr; $6,500/yr): $85 ÷ $6,500 ≈ 1.31%. All three recompute consistently with chain C5's stated figures (0.2%, ~1.3%, 5%). C3's weighted totals, redone independently: A = 5(5)+1(5)+5(4)+5(4)+1(3)+1(2) = 25+5+20+20+3+2 = 75; C = 4(5)+3(5)+5(4)+4(4)+3(3)+2(2) = 20+15+20+16+9+4 = 84; E = 5(5)+5(5)+3(4)+5(4)+2(3)+2(2) = 25+25+12+20+6+4 = 92. All three recompute to the values stated in chain C3. No arithmetic error found.

**Sensitivity.** The single ground truth whose falsity would flip the headline conclusion is **GT-3?** (Finance's claim that free-tier cost scales with active users, not revenue — i.e., is a real, scaling cost center). It is `?`-marked. If GT-3? were false — if free-tier cost were in fact near-zero and marginal, as the naive loss-leader convention (A-3, discarded) assumes — then C1's and C5's entire cost-side premise collapses, and a far more aggressive rollout (closer to Option B) would likely be justified without a bounded pilot. Verification path: open Finance's actual cost model and the specific $/active-free-user figure (which also tightens GT-7?). This is the single highest-leverage fact named anywhere in this analysis (see Conclusion, section 6).

**Rival.** Headline conclusion (run the bounded pilot rather than full freemium or outright rejection): the rival "just launch full freemium now" (Option B) is ruled out structurally — see Abandoned Reasoning, Dead End 1. The rival "reject freemium outright, keep doing exactly what works" (Option A) is ruled out by C3's trade-off (A=75 loses to E=92, and the margin is not a near-tie requiring a flip test to trust). Chain C1: rival "the real cost is trivial" is exactly GT-3?'s negation; not ruled out independently, carried as the Sensitivity finding above. Chain C2: the only rival that would actually contradict this chain's narrow claim — that an unshown parity analogy is sufficient justification on its own — is ruled out by the ban on analogy-as-direct-evidence (Abandoned Reasoning); a rival asserting parity matters generally does not contradict this chain, which disputes only this one unshown analogy's sufficiency. Chain C3: rivals A and B are the two alternatives explicitly scored/knocked out above. Chain C4: the "organizational-inertia concern is overstated" consideration is not a rival conclusion — C4's claim is explicitly conditional ("favorable only when paired with..."), and disputing how often the condition holds in practice does not dispute the conditional itself; that likelihood question is a probability concern the pre-mortem's Cluster 1 disposition manages, not a competing conclusion from the same ground truths. Chain C5: rival "the bracket is too wide to be decision-useful" is reframed, not ruled out — the straddle is the finding itself (see C5's own confidence line).

**Premise.** The freemium-lite pilot described in chain C3/C4 has already failed within its 6–12 month window.

**Causes** (unfiltered, generated from five stakeholder viewpoints):

*Implementer/Product-Eng:* self-serve signup/billing-tier gating took far longer than estimated because no self-serve infrastructure existed before (GT-2?), eating into other roadmap commitments. The free tier's usage/feature caps were set either too generous (free users never needed to pay) or too stingy (free users bounced before reaching value), with no principled way to choose correctly without data.

*Sales/CS (who live with the result):* existing outbound reps treat free-tier leads as low-priority because their entire motion and comp plan is built around outbound-sourced deals (GT-2?), so "free user asking about upgrading" leads get routed nowhere. Support gets a new ticket queue from users with no paid-support SLA; either paying customers' tickets get neglected to keep up, or free users get a visibly bad experience that damages brand anyway.

*Finance/budget owner (who pays for it):* the signup cap gets raised "just this once" repeatedly because marketing wants more top-of-funnel volume, quietly turning a capped pilot into an uncapped cost center. Nobody actually tracks cost-per-free-user against the $20–150 bracket, so twelve months in, Finance still can't say whether the real number is $20 or $300 — the pilot produced a conversion number without producing the other half of the breakeven equation.

*Competitor/market (adversary who benefits):* a competitor notices the small, capped pilot and markets aggressively against "a late, half-hearted free tier," turning the intended optics move negative. Free-tier users who never convert become unpaid evaluators *for a rival's* paid product instead, using the free tier to benchmark against competitors rather than to build this company's funnel.

*Existing paying customer:* a paying team discovers the free tier exists and asks for a discount or downgrade at renewal ("why am I paying $10K when there's a free version"), creating an unmodeled renegotiation risk.

**Clusters:**

- **Cluster 1 — No operational enforcement of pilot boundaries** (cap creep, "just this once" raises, no cost tracking) — bears on chain C4's `[Assumes: A-12, A-19]` and Abandoned Reasoning's dead end on labeling an uncapped rollout "a pilot."
- **Cluster 2 — No GTM-motion integration for free-tier leads** (sales ignores them, support unprepared, no PQL routing) — bears on chain C3's "Fit with GTM motion" criterion, chain C4's `[Assumes: A-18]`, and GT-2?.
- **Cluster 3 — Existing-customer cannibalization/renegotiation risk** — bears on assumption A-5 and chain C1.
- **Cluster 4 — Negative-sum competitive/optics outcome** (a half-hearted free tier becomes an attack vector; free tier subsidizes rivals' competitive intelligence) — bears on A-1/A-8 and chain C2.

**Disposition:**

- Cluster 1 → **Plan change:** name a single accountable owner for the pilot (not "marketing" generically); require the signup cap and end date to be enforced in the product/billing system as a hard gate, not a policy memo; require a monthly Finance report of cost-per-active-free-user against the $20–150 bracket (GT-7?) as a standing go/no-go input starting month one.
- Cluster 2 → **Plan change:** before launch, define and build a minimal PQL scoring rule and an explicit lead-routing path (which queue/rep owns a free-tier signal); give CS a stated, even if minimal, support-tier policy for free users so it is not "whatever capacity is left over."
- Cluster 3 → **Accepted risk, named mitigation:** accept that some existing customers may ask about the free tier; mitigate by restricting the pilot to a segment/persona distinct from the current paid ICP, and brief CS/AMs with a scripted response before launch rather than after the first renewal conversation goes sideways.
- Cluster 4 → **Accepted risk, named mitigation:** accept that a small, capped pilot will not win a public "we have a free tier too" argument; mitigate by not messaging the pilot as a competitive-parity move at all (low-key, invite-only framing) until real conversion data supports a larger, confident claim — directly applying chain C2's finding that the parity argument was weak evidence on its own.

**Falsification.** This analysis's conclusion is false if, once Finance supplies the real cost-per-active-free-user figure and the pilot is run under the five named guardrails, the measured free→paid conversion rate and real cost-per-user combination clears chain C5's breakeven bracket with a comfortable margin, and none of Clusters 1–4 materializes — in that case, a larger-scale freemium rollout (not merely a continued capped pilot) would be the better next recommendation, which is a different conclusion than "pilot, then decide."

## §6→§4 closure ledger (process output)

- "Do not launch an unlimited, company-wide free tier now... run a capped, time-boxed, single-segment freemium-lite pilot... gated by a named owner, a product-enforced signup cap, and a scheduled go/no-go decision" → chains C1, C2, C3, C4 ✓ (inline)
- "'Should we add a free tier' and 'how do we get scalable, lower-CAC acquisition' are different questions... the single highest-leverage missing fact... is cheap to obtain" → chains C1, C5 ✓ (inline)
- "running the pilot instead of either extreme means accepting slower validated learning... a real... new support and engineering surface... a small, single-segment pilot will not deliver whatever competitive-optics benefit a full... rollout might" → chains C4, C2 ✓ (inline)
- "accepting a residual cannibalization/renegotiation risk among existing paying teams..." → no chain — flagged assumption only (caveat marker; sourced from the pre-mortem's Cluster 3, process output, not a formal §4 chain; discloses rather than discharges)
- "**Confidence:** MEDIUM — every contributing chain (C1–C5) is itself MEDIUM..." → chains C1, C2, C3, C4, C5 ✓ (inline)

Scan result: 5 claims identified in §6 (4 bold lead-ins + 1 embedded caveat); 4 cited inline and traced, 1 caveat carries the flagged-assumption marker (honest-disclosure, not discharge); 0 cut.

## Self-audit scan (process output)

| Chain | Chain Head (brief) | Form conforming? | Rule applied | Dependency clean? | Band | Act attempted? | Edges fired |
|---|---|---|---|---|---|---|---|
| C1 | GT-3?, GT-4?, GT-1? | yes | n/a | yes | MEDIUM | no | none |
| C2 | GT-5?, GT-1?, GT-2? | yes | n/a | yes | MEDIUM | no | none |
| C3 | GT-3?, GT-4?, GT-2? | yes | n/a | yes | MEDIUM | no | none |
| C4 | C3 (MEDIUM) | yes | n/a | yes | MEDIUM | no | none |
| C5 | GT-7?, GT-8?, GT-6? | yes | n/a | yes | MEDIUM | yes | none |

| §6 Span (brief) | Construct | Claim under R11? | R11 clause applied | Chain cited |
|---|---|---|---|---|
| "Do not launch an unlimited... run a capped... pilot... gated by five named preconditions..." | bold lead-in | yes | lead-in whose colon closes the bold span | C1, C2, C3, C4 |
| "'Should we add a free tier'... is cheap to obtain" | bold lead-in | yes | lead-in whose colon closes the bold span | C5, C1 |
| "running the pilot instead of either extreme means accepting..." | bold lead-in | yes | lead-in whose colon closes the bold span | C4, C2 |
| "It also means accepting a residual cannibalization/renegotiation risk... no chain — flagged assumption only" | prose | no | prose carrying neither a bold colon lead-in nor a list marker is not a claim at all (voluntarily marked anyway, as a caveat on the preceding claim) | n/a |
| "**Pre-check:** head C1 (MEDIUM), C2 (MEDIUM)..." | bold lead-in | yes | pre-check line is itself a claim, cited by the chains its own head names | C1, C2, C3, C4, C5 |
| "**Confidence:** MEDIUM — every contributing chain..." | bold lead-in | yes | lead-in whose colon closes the bold span | C1, C2, C3, C4, C5 |

Scan complete: 5 chain rows, one per section-4 chain block in order; 6 section-6 rows, one per construct in order — 5 claims under R11, 1 excluded. 0 chains malformed, 0 claims untraced.

## Self-Audit Gate (process output)

**Criterion 1: Identify Essence**
Quoted span: "Given a profitable, enterprise-leaning B2B SaaS business ($2.4M ARR, 240 paying teams, ~$10K ACV) built entirely on outbound sales and referrals — with no self-serve motion, no freemium experience, and a Finance-confirmed real, scaling (not near-zero) cost attached to every active free user — should the company add a free tier as a lever for more scalable, lower-CAC acquisition, and if so, in what form and on what timeline?"
Band: **Rigorous**
Justification: the statement names the real decision (not the triggering event "leadership is asking," not a generic restatement), is specific to this company's numbers and GTM shape, and the five success criteria each state a checkable property of section 6 (names a specific form, tests the two named assumptions, states a confidence band and the top missing evidence, names a concrete next step, addresses second-order effects) rather than a vague standard.

**Criterion 2: Challenge Assumptions**
Quoted span (Assumption Audit scan): "Scan complete: 14 steps across 5 chains, in order, no step skipped. ... Five assumptions newly surfaced across this audit and the Phase 2 inversion pass (A-12, A-16, A-17, A-18, A-19), each added to the Classified Assumptions Table (section 2)..."
Band: **Rigorous**
Justification: all 19 rows use the four-type scheme with no freeform labels, every Verdict cell leads with Accept/Challenge/Discard followed by an em-dash and a specific justification, every Verification cell reads "unverified — flagged" (or names why that phrase does not apply, as for the discarded A-3/A-11), multiple assumptions are genuinely challenged or discarded (not merely Accepted), and the Assumption Audit scan confirms the Phase 4 audit ran exhaustively over every chain step with no step skipped.

**Criterion 3: Establish Ground Truths**
Quoted span: "`?`-marked: GT-1, GT-2, GT-3, GT-4, GT-5, GT-6, GT-7, GT-8 (8 of 8). No ground truth in this analysis is read-at-source..."
Band: **Rigorous**
Justification: checking the enumeration against the Ground Truths list (section 3) confirms it matches exactly — all 8 entries carry `?` and the enumeration names all 8; every entry carries a provenance label and an analysis-specific (not generic "common knowledge") reason; no `?` entries are discarded-assumption leakage (A-3/A-11 were discarded in section 2 and do not appear here); since no ground truth is unsuffixed, the "unsuffixed GT feeding a HIGH chain must name a read-at-source location" requirement has no instance to fail.

**Criterion 4: Reason Upward**
Quoted span (self-audit scan, chain-form table): "C1 | GT-3?, GT-4?, GT-1? | yes | n/a | yes | MEDIUM | no | none" ... "C5 | GT-7?, GT-8?, GT-6? | yes | n/a | yes | MEDIUM | yes | none" — reconciliation: "0 chains malformed."
Band: **Rigorous**
Justification: the scan shows all five chains form-conforming with clean dependencies; each conclusion in section 6 has exactly one named chain (C1–C5, no redundant restatement, no orphan); Abandoned Reasoning (section 5) documents four dead ends each with a specific, non-generic abandonment reason; no analogy is used as direct evidence (C2 explicitly interrogates rather than relies on the competitor analogy, and Abandoned Reasoning records exactly that dead end); newly-introduced assumptions are declared inline with `[Assumes: A-12, A-18, A-19]` on their load-bearing step (C4); the Recompute step in the adversarial pass (Appendix) independently re-derives every computed figure in C3 and C5 with no arithmetic error found.

**Criterion 5: Validate**
Quoted span (adversarial pass record, Appendix): "Cluster 1 → Plan change: name a single accountable owner... Cluster 4 → Accepted risk, named mitigation: accept that a small, capped pilot will not win a public... argument..." — every cluster carries a disposition.
Band: **Rigorous**
Justification: every chain's confidence line names its weakest link, each `GT-N?` input with the specific verification that would remove it as a cause of the downgrade, and each cited `Cn` rated below HIGH without re-explaining it; no chain is rated HIGH while consuming a `?` input; every chain is rated no higher than the lowest-rated chain its head cites (C4 ≤ C3); each band matches what its three axes license on inspection — Inputs short on all five (bounding each to MEDIUM), Inference priced where an `[Assumes:]` premise appears (C4), and Rivals clean on each (ruled out via Abandoned Reasoning for C2/C3, reframed as non-rival for C4/C5, or carried as the named Sensitivity finding for C1) — so no chain is mis-rated in either direction; the adversarial pass record carries all required parts (Recompute, Sensitivity, Rival, Premise, Causes from five stakeholder viewpoints, Clusters tied to chain/GT ids, Disposition, Falsification) with every cluster disposed as a plan change or an accepted risk with a named mitigation.

**Criterion 6: Conclusion-to-Ground-Truth Traceability**
Quoted span (self-audit scan, claim-inventory table): "Scan complete: 5 chain rows... 6 section-6 rows, one per construct in order — 5 claims under R11, 1 excluded. 0 chains malformed, 0 claims untraced."
Band: **Rigorous**
Justification: every claim under R11 in section 6 cites a specific named chain inline (C1–C5), none untraced; the one excluded construct is a caveat correctly carrying the "no chain — flagged assumption only" marker rather than masquerading as a traced claim; the Key Insight ("add a free tier" and "get scalable lower-CAC acquisition" are different questions, and the economics are conversion-rate-sensitive rather than obviously good or bad) is a non-obvious finding distinct from the Recommended approach's action, not a restatement of it.

**Gate result:** cleared · passes: 1 · Fix/Repeat fired: no

## Structured summary (process output)

```json
{
  "schema_version": 1,
  "run_mode": "full-composer",
  "assumptions": [
    {"id": "A-1", "type": "convention", "verdict": "Challenge"},
    {"id": "A-2", "type": "untested belief", "verdict": "Challenge"},
    {"id": "A-3", "type": "convention", "verdict": "Discard"},
    {"id": "A-4", "type": "untested belief", "verdict": "Challenge"},
    {"id": "A-5", "type": "untested belief", "verdict": "Challenge"},
    {"id": "A-6", "type": "untested belief", "verdict": "Challenge"},
    {"id": "A-7", "type": "current constraint", "verdict": "Challenge"},
    {"id": "A-8", "type": "convention", "verdict": "Challenge"},
    {"id": "A-9", "type": "untested belief", "verdict": "Challenge"},
    {"id": "A-10", "type": "untested belief", "verdict": "Challenge"},
    {"id": "A-11", "type": "convention", "verdict": "Discard"},
    {"id": "A-12", "type": "untested belief", "verdict": "Challenge"},
    {"id": "A-13", "type": "untested belief", "verdict": "Challenge"},
    {"id": "A-14", "type": "untested belief", "verdict": "Challenge"},
    {"id": "A-15", "type": "untested belief", "verdict": "Challenge"},
    {"id": "A-16", "type": "untested belief", "verdict": "Challenge"},
    {"id": "A-17", "type": "untested belief", "verdict": "Challenge"},
    {"id": "A-18", "type": "untested belief", "verdict": "Challenge"},
    {"id": "A-19", "type": "untested belief", "verdict": "Challenge"}
  ],
  "ground_truths": [
    {"id": "GT-1", "read_at_source": false},
    {"id": "GT-2", "read_at_source": false},
    {"id": "GT-3", "read_at_source": false},
    {"id": "GT-4", "read_at_source": false},
    {"id": "GT-5", "read_at_source": false},
    {"id": "GT-6", "read_at_source": false},
    {"id": "GT-7", "read_at_source": false},
    {"id": "GT-8", "read_at_source": false}
  ],
  "chains": [
    {"id": "C1", "confidence": "MEDIUM", "rests_on": ["GT-3?", "GT-4?", "GT-1?"]},
    {"id": "C2", "confidence": "MEDIUM", "rests_on": ["GT-5?", "GT-1?", "GT-2?"]},
    {"id": "C3", "confidence": "MEDIUM", "rests_on": ["GT-3?", "GT-4?", "GT-2?"]},
    {"id": "C4", "confidence": "MEDIUM", "rests_on": ["C3"]},
    {"id": "C5", "confidence": "MEDIUM", "rests_on": ["GT-7?", "GT-8?", "GT-6?"]}
  ],
  "dead_ends": [
    "Full company-wide freemium (Option B), scored like the other options",
    "Freemium-lite rolled out company-wide with uncapped signups (Option D)",
    "Treating \"competitors have a free tier\" as sufficient justification on its own",
    "Calling an uncapped rollout a \"pilot\" and relying on intent alone to keep it reversible"
  ],
  "techniques": {
    "applied": ["five-whys", "fishbone", "inversion", "trade-off", "second-order", "estimate", "pre-mortem"],
    "not_applied": [
      {"technique": "theoretical-limit", "phase": 1, "reason": "the essence question is a resource-allocation/GTM decision, not one where a current figure is plausibly a mere convention masking a hard physical ceiling; no reframe toward a law-permitted limit was available."},
      {"technique": "theoretical-limit", "phase": 4, "reason": "no governing hard constraint (physical, mathematical, or protocol-level) bounds a freemium conversion rate the way thermodynamics bounds an engine; the relevant ceiling is the empirical industry benchmark (GT-6?), which the Estimate technique already incorporates as a bracket input to chain C5, not a theoretical-limit derivation."},
      {"technique": "inversion", "phase": 5, "reason": "the conclusion is a plan/recommendation (run a bounded pilot under named guardrails), and the decision rule assigns plans to pre-mortem rather than inversion; inversion was instead applied at Phase 2 on the assumption space, which is its other invocation point and did fire."}
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
    "recommendation": "Do not launch an unlimited, company-wide free tier now (chain C1), and do not treat competitor parity as sufficient reason to add one either (chain C2). Instead, run a capped, time-boxed, single-segment freemium-lite pilot — the option that outscores both the status quo and a sales-assisted trial in the trade-off (chain C3) — gated by five named preconditions: an accountable owner, a product-enforced signup cap and end date, a PQL/lead-routing rule into the existing sales motion, committed Finance cost-tracking per active free user, and a scheduled go/no-go decision at the end of the window (chain C4).",
    "confidence": "MEDIUM",
    "rests_on": ["C1", "C2", "C3", "C4", "C5"]
  }
}
```

