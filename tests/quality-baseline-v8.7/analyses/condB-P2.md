## 1. Problem Essence

**Essence Statement:** Is a loyalty rewards program the highest-return intervention available for reducing 5% monthly churn — or is the team proposing a solution before the churn has been decomposed into its causes?

Note the reframe. "Should we build loyalty rewards?" is a *solution* question. The real decision is an allocation one: given finite engineering capacity, which intervention buys the most retained revenue per unit of cost and risk.

**Success criteria** a correct answer must satisfy:
1. Identifies what the 5% is actually *made of* (churn is not one phenomenon).
2. States the fraction of that 5% a loyalty program can physically address.
3. Establishes the breakeven bar the program must clear, derived rather than asserted.
4. Compares against at least one alternative on the same yardstick.

---

## 2. Assumptions Table

| # | Assumption | Type | Treatment | Verdict |
|---|---|---|---|---|
| A1 | 5%/month is a problem worth spending on | current constraint | Test against unit economics, not benchmarks | **Likely true** — 5%/mo ⇒ 0.95¹² = 54% annual retention, ~20-month average lifetime. Genuinely constraining for most subscription models. |
| A2 | The 5% is one homogeneous population | untested belief | Challenge — decompose | **False.** Churn splits at minimum into involuntary (payment failure), never-activated, need-ended, and value-disappointed. These have disjoint remedies. |
| A3 | Churn is caused by insufficient loyalty/incentive | untested belief | Challenge before use | **Unverified and load-bearing.** No stated evidence. The proposal encodes a diagnosis nobody has confirmed. |
| A4 | Rewards can be targeted at at-risk customers only | convention | Challenge | **False in practice.** A loyalty program is a published, standing offer; its cost lands on the ~95% who would have stayed anyway. This is the dominant cost term. |
| A5 | "Loyalty members churn 18–24% less" implies rewards cause retention | untested belief | Challenge | **Selection bias.** Enrolment is voluntary; already-engaged customers enrol. The cited figures ([Blustream](https://blustream.ai/blog/subscription-loyalty-program-do-they-work-for-churn), [LoyaltyLion](https://loyaltylion.com/blog/five-benefits-of-a-loyalty-program)) are correlational, not causal. Do **not** use as evidence. |
| A6 | Rewards are removable if they don't work | convention | Challenge | **False.** Withdrawing an active loyalty program is itself a churn event; accrued points are a balance-sheet liability. The decision is closer to irreversible than it looks. |
| A7 | Team capacity is the binding constraint | current constraint | Record expiry | Holds while one team owns retention work. |

*(Inversion pass, Phase 2: "What would guarantee this program fails to pay back?" → (i) churn is mostly involuntary; (ii) churners are low-engagement and never encounter the reward loop; (iii) reward cost exceeds retained margin; (iv) it attracts discount-seekers with worse cohort economics. Each became a row or a chain input above.)*

---

## 3. Ground Truths

- **GT-1** — Monthly churn c and mean customer lifetime are reciprocals: L = 1/c. At c = 0.05, L = 20 months. *(Definition, geometric survival.)*
- **GT-2** — 0.95¹² = 0.5404. Annual retention ≈ 54%. *(Arithmetic.)*
- **GT-3** — Involuntary churn (failed cards, expiry, retry exhaustion) averages ~26% of total subscription churn, range 20–40% for e-commerce subscriptions, up to 68% for subscription boxes. *(Recurly benchmarks via [Finsi](https://www.finsi.ai/blog/involuntary-churn-hidden-revenue-leak/), [Loopwork](https://www.loopwork.co/blog/voluntary-vs-involuntary-churn-shopify-subscription-revenue).)*
- **GT-4** — Involuntary churn is mechanically insensitive to loyalty incentives: a customer whose card declines does not decide to leave. *(Definition.)*
- **GT-5** — A loyalty reward is a cost paid to the entire enrolled base, not only to retained-at-margin customers. *(Follows from A4.)*
- **GT-6** — Annual billing reduces cancellation decision points from 12/year to 1/year. *(Definition. The often-quoted "51% churn reduction" is correlational, but the mechanism is structural.)*
- **GT-7?** — *Unverified:* your churn's composition, tenure curve, and engagement profile. **This is the single most load-bearing unknown in the analysis.**

---

## 4. Derivation Chains

**Chain A — the breakeven bar (quantitative).**

GT-5 + GT-1 → contribution LTV = (m·A)/c, where A = ARPU, m = gross margin, c = churn. With a program costing r (as a fraction of revenue) and reducing churn by Δ: LTV′ = (m−r)·A/(c−Δ). Setting LTV′ = LTV:

> **Δ/c = r/m** → *required **relative** churn reduction = reward cost as % of revenue ÷ gross margin.*

This is independent of ARPU and of the churn level. At 80% gross margin, a program giving back 5% of revenue must cut churn **6.3% relative** (5.00% → 4.69%) just to break even *before* build cost; a 10% giveaway needs **12.5% relative**.

**Chain B — the physical ceiling on what rewards can move.**

GT-3 + GT-4 → ~26% of your churn is untouchable by rewards → addressable pool ≤ 74%. Of that voluntary remainder, rewards cannot reach never-activated users (never see the loop), need-ended users (life change, project finished), or hard product-gap churners. Bracketing the genuinely reward-responsive segment — engaged, tenured, price/value-marginal — at **15–30%** of total churn, and assuming an optimistic 15–25% lift *within* that segment:

> Expected total churn reduction = **2–7.5% relative** [lower 2%, central ~4%, upper 7.5%].

**Chain C — the comparison.**

Chain A (need 6–13% relative) + Chain B (expect 2–7.5% relative) → **the expected effect sits at or below the breakeven bar**, before counting build cost. Fermi on build: ~6–10 person-months for ledger, earn/redeem rules, tiers, comms, admin, and revenue-recognition handling ⇒ **$60k–$300k, central ~$130k**, plus ongoing ops. That cost pushes the true bar above the top of the expected-effect bracket.

Contrast — dunning/retry logic + network card-updater: recovers roughly 30–50% of involuntary churn (GT-3) ⇒ 0.26 × 0.4 ≈ **10% relative total churn reduction** (5.0% → 4.5%), at ~1–3 engineer-weeks and near-zero recurring margin cost. **Strictly dominant** on both axes.

**Chain D — second-order effects.**
1. Rewards raise the salience of price → 2nd-order: more customers evaluate the subscription as a price decision → 3rd-order: increased discount elasticity and a worse-quality acquisition mix. *(Contradicts the intent of the program.)*
2. Accrued points become a liability → 2nd-order: the program cannot be cheaply withdrawn (A6) → 3rd-order: a failed experiment becomes permanent cost.
3. A program that "works" masks the diagnostic signal → 2nd-order: the real churn cause stays unfixed and resurfaces at higher scale.

No second-order effect contradicts a Ground Truth; effect 1 contradicts the *proposal's* premise (A3), which is already flagged unverified.

---

## 5. Abandoned Reasoning

- **Benchmarking 5% against industry averages.** Abandoned: comparing to peers is reasoning by analogy. Whether 5% is acceptable depends on your CAC payback, not on a median.
- **LTV/CAC framing as the primary lens.** Abandoned: CAC was not supplied, and the decision resolves without it.
- **Treating published "loyalty members churn less" statistics as evidence.** Abandoned per A5 — correlational, selection-biased. Using them would have inverted the recommendation on unsound grounds.

---

## 6. Conclusion

**No — not now. Confidence: HIGH on "don't build it yet," MEDIUM on "don't build it ever."**

The loyalty program is an answer to a diagnosis nobody has made (A3). Its breakeven bar (Chain A: 6–13% relative churn reduction) sits at or above its physical ceiling (Chain B: 2–7.5%), and that comparison ignores $60k–$300k of build cost and a set of adverse second-order effects that are hard to reverse (Chain D).

**Do this instead, in order:**

1. **Decompose the 5% (1–2 weeks, resolves GT-7?).** Split into involuntary vs. voluntary; then voluntary by tenure (month-1 vs. month-6+) and by engagement decile before cancel. This is the cheapest, highest-information action available and it determines everything downstream.
2. **Fix involuntary churn first.** Smart retries, dunning emails, network card-updater. ~10% relative churn reduction for a fraction of the loyalty program's cost (Chain C).
3. **Then match remedy to the largest voluntary segment.** Month-1 churn ⇒ onboarding/activation, not rewards. Month-6+ tenured churn ⇒ deepening value or annual-plan conversion (GT-6), which attacks the decision-frequency structurally rather than paying a standing bribe against it.

**What would change this answer:** if step 1 shows a large cohort of *tenured, highly engaged* churners citing price or a competitor's incentive — the one segment Chain B says rewards can reach — revisit. Verifying GT-7? is what would move the confidence on any of this from MEDIUM to HIGH.

**Weakest link:** the 15–30% reward-addressable bracket in Chain B is estimated, not measured. Even at its optimistic end, though, it does not clear the Chain A bar once build cost is included — so the conclusion holds across the full bracket.

**Sources:** [Finsi — Involuntary Churn](https://www.finsi.ai/blog/involuntary-churn-hidden-revenue-leak/) · [Loopwork — Voluntary vs Involuntary Churn](https://www.loopwork.co/blog/voluntary-vs-involuntary-churn-shopify-subscription-revenue) · [Blustream — Subscription Loyalty & Churn](https://blustream.ai/blog/subscription-loyalty-program-do-they-work-for-churn) · [Loyalty & Reward Co — Scientific Evidence Review](https://loyaltyrewardco.com/do-loyalty-programs-work-a-review-of-scientific-evidence/)

*(Note: the claude.ai Gmail, Calendar, and Drive connectors are unauthorized in this session — if you have churn data in Drive, authorize them via your claude.ai connector settings and I can run step 1 against the real numbers.)*agentId: aae32af1fa346ecd1 (use SendMessage with to: 'aae32af1fa346ecd1', summary: '<5-10 word recap>' to continue this agent)
<usage>subagent_tokens: 38663
tool_uses: 3
duration_ms: 110823</usage>
