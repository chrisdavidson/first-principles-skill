<!-- GENERATED — DO NOT EDIT. Source: shared/examples/product-business.md. Regenerate via: scripts/sync-content.py --write. -->

# Worked Example: Product and Business

A complete first-principles analysis of a product and business pricing question, following the standardized output format. The Phase 2 Classified Assumptions Table is the deepest section of analysis — seven assumptions examined, two discarded outright — and the abandoned reasoning path demonstrates the Phase 4 no-analogies guidance applied to a competitor-parity argument. Authored in Phase 5.

---

## 1. Problem Essence

**Core problem:** Does this B2B SaaS product's own economics support adding a free tier, or is the case for one resting entirely on unverified beliefs and competitor analogy?

**Success criteria:**
- A verifiable data gap (the product's free-to-paid conversion rate) is either measured or a concrete plan to measure it is recommended.
- The competitor-parity argument ("all our competitors have a free tier") is tested against the Phase 4 no-analogies guidance (SKILL.md, Phase 4 Operation), with a clear verdict on whether it can anchor a decision.
- The recommendation is grounded in what is actually known about this product's acquisition model, cost structure, and ICP behavior — not in industry convention.
- A skeptic can evaluate whether a free tier is the right move for this specific product at this specific ARR stage, using only the reasoning and ground truths in this document.

---

## 2. Assumptions Table

| Assumption | Type | Treatment | Verdict | Verification |
|------------|------|-----------|---------|--------------|
| A free tier drives top-of-funnel growth | untested belief | Verify, or flag as unverified. Free-tier growth depends on whether the ICP self-serves — not a universal law. | Challenge | unverified — flagged; true for some products (consumer tools, developer utilities), not for B2B outbound-led SaaS |
| Free users convert to paid at a meaningful rate | untested belief | Verify, or flag as unverified. Conversion rate is the economic hinge of the entire decision. | Challenge | unverified — flagged; no conversion data exists for this product in this ICP segment (confirmed absent in GT-4) |
| Competitors' free-tier economics are profitable | untested belief | Verify against published data, or flag. Competitor ARR, cost structure, and conversion rates are not observable without disclosure. | Challenge | unverified; no public data on competitors' free-tier unit economics is available |
| All our competitors have a free tier, so we need one | convention | Explicitly challenge before use. Ask whether the convention holds in this context or merely carries industry inertia. Without a named GT about competitor conversion economics, competitor behavior cannot anchor a derivation chain. | Discard | Analogy-as-evidence move. Competitor adoption of a pricing model is not evidence that the same model is economically viable for this product in this ICP segment at this ARR stage. Discard as a stand-alone justification. |
| Adding a free tier has no opportunity cost | untested belief | Verify. Free tiers require engineering capacity (feature gating, infrastructure separation), support resources, and pricing-page complexity. | Discard | False. Engineering bandwidth to build and maintain feature gating, incremental support load for non-paying users, and deal-desk overhead from a more complex pricing surface are documented operational costs. |
| The current ICP (B2B teams, ~$10K/year contracts) responds to free-tier self-service | untested belief | Verify. B2B enterprise buyers are often procurement-driven, not self-serve. The assumption that free tiers attract ICP-aligned users (rather than non-ICP individual users) has not been tested. | Challenge | unverified; the product's $10K/year average contract suggests a buying process driven by champions and procurement, not individual self-sign-up |
| Free-tier acquisition cost is lower than current outbound acquisition cost | untested belief | Verify against actual cost data. Free tiers carry infrastructure, support, and conversion costs that may exceed the CAC savings from reduced outbound. | Challenge | unverified; no blended cost-per-acquisition comparison has been calculated |

---

## 3. Ground Truths

- **GT-1** Current ARR is $2.4M from 240 paying teams at approximately $10,000 per team per year. — source: internal financial report (company's own ARR dashboard)
- **GT-2** The product's current acquisition model is primarily outbound sales and referrals; no self-serve inbound channel exists. — source: known channel mix (sales team records)
- **GT-3** Free-tier infrastructure and support must be budgeted separately from the paid-tier cost structure; they cannot be absorbed as zero marginal cost into the current operating model. — source: accounting principle; confirmed by finance team (infrastructure and support costs scale with active users, not paying users)
- **GT-4** The free-to-paid conversion rate for this product in this ICP segment is unknown and has not been measured; no historical pilot or freemium experiment has been run. — source: verified gap (product and sales teams confirm no conversion data exists)

---

## 4. Derivation Chains

### Conclusion: The competitor-parity argument cannot justify adding a free tier

GT-3 (free-tier costs are real and must be separately budgeted) + GT-4 (conversion rate unknown and unverified)
→ Any projection of free-tier profitability or payback period requires a conversion rate assumption, and that assumption cannot be filled from competitor behavior without knowing competitors' cost structure and ICP overlap
→ The competitor-parity argument ("they have a free tier, so we need one") is an analogy-as-evidence move that collapses without a named GT about competitor conversion economics — it cannot anchor a derivation chain

**Confidence:** HIGH

---

### Conclusion: The free-tier decision is empirical, not a convention to follow; a time-boxed pilot is the minimum required action before any adoption decision

GT-1 (240 teams at $10K/year average contract; outbound acquisition model) + GT-4 (conversion rate unknown and unverified)
→ At $10K/year average contract, even a modest conversion rate (1–2%) on a free-tier cohort could justify the investment; but at near-zero conversion the free tier generates support and infrastructure cost with no revenue offset — the outcome is highly sensitive to a variable that has never been measured for this product
→ Deciding to add or reject a free tier without conversion data is a decision under ignorance, not a decision under uncertainty; the minimum responsible action is to run a time-boxed pilot designed to generate the missing data before committing to a permanent pricing change

**Confidence:** HIGH

---

### Conclusion: The pilot threshold for adoption must be pre-specified before the pilot begins, not inferred from results afterward

GT-2 (outbound-led acquisition; no existing self-serve channel) + GT-3 (free-tier costs are real and separately budgeted)
→ The break-even conversion rate has the form (blended monthly cost per free user) / (average contract value): GT-1 supplies the average contract value (~$10K/year), but no named ground truth supplies the blended monthly cost per free user — GT-3 establishes only that this cost is real and must be separately budgeted, not its magnitude. The threshold is therefore not yet calculable from the named ground truths; it requires one additional measured input — the per-free-user cost — that the pilot itself must produce
→ Pre-specifying the threshold formula before the pilot — and committing to compute the actual break-even number as soon as the pilot yields the per-free-user cost — gives the pilot a falsifiable success criterion and prevents post-hoc rationalization of a result that falls below the economic break-even

**Confidence:** HIGH

---

## 5. Abandoned Reasoning

### Dead End: Competitors have free tiers, therefore we need one

**What was tried:** Use the observation that all major competitors offer a free tier as direct evidence that this product must add one to remain competitive. The reasoning chain was: "industry-wide adoption of free tiers indicates it is a necessary competitive feature; we lack it; therefore we are at a competitive disadvantage."

**Why abandoned:** This is an analogy-as-evidence move. The Phase 4 instruction not to use analogies as direct evidence (SKILL.md, Phase 4 Operation) requires any reference to how others solved a similar problem to be grounded in a verified ground truth about their situation. The competitors' free-tier economics — their conversion rates, their ICP fit, their cost structure, and whether their free tiers are net-positive for growth — are not observable without published data. Without a named GT anchoring those facts, competitor behavior is an untested belief elevated to the role of direct evidence, which the methodology does not permit. The assumption "all our competitors have a free tier, so we need one" was classified in Phase 2 as a convention with Verdict: Discard precisely because it commits this error. A derivation chain built on it collapses the moment the analogy is probed: competitors may be at a different ARR stage, serve a different ICP sub-segment, or run a free tier that is loss-leading with a known payback horizon — none of which is established as a GT for this analysis.

**What it ruled out:** Competitor parity as a sufficient justification for restructuring the pricing model. This dead end establishes that the free-tier question must be evaluated on this product's own economics — GT-1, GT-2, GT-3, and the gap in GT-4 — not by reference to what others have chosen to do.

---

## 6. Conclusion

**Recommended approach:** Run a time-boxed 90-day pilot with a limited cohort of free-tier users (up to 5 users, limited projects, as proposed) to generate the conversion data currently absent in GT-4. Before the pilot launches, pre-specify the break-even threshold *formula* — blended monthly cost per free user divided by average contract value gives the minimum conversion needed to cover costs. GT-1 supplies the average contract value, but the blended cost per free user is not supplied by any named ground truth (GT-3 establishes only that this cost is real); it is a required input the pilot must measure. Commit in advance to compute the actual threshold number as soon as that per-free-user cost is known. If the pilot clears the threshold, adopt the free tier with full cost budgeting per GT-3. If it does not, reject the free tier and document the result so the question does not re-open without new evidence.

**Key insight:** "Competitors do it" is not a valid reason to restructure a B2B pricing model at $2.4M ARR. The free-tier question is an empirical question about this product's conversion economics, not a convention the product team is obligated to follow. An outbound-led SaaS product with $10K/year average contracts and no existing self-serve channel is structurally different from the consumer tools and developer utilities where free-tier models consistently generate positive unit economics. The methodology forced this distinction by requiring competitor behavior to be grounded in a named GT about competitor economics — and no such GT exists or can be constructed from available data.

**Trade-offs acknowledged:** The pilot has real costs that must be budgeted before approval: engineering time to build feature gating and usage limits, infrastructure for non-paying users, and support overhead during the 90-day window. The pilot produces conversion data only for the cohort it runs on; if that cohort is not representative of the broader ICP, the data may not generalize to a full launch. There is also a pricing-page complexity cost during and after the pilot regardless of outcome.

**Confidence:** HIGH
