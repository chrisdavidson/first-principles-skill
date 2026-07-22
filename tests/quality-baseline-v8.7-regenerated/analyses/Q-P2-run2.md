# First-Principles Analysis: Loyalty Program Funding Decision

## 1. Problem Essence

**Core question:** Is $310,000/year the cheapest way to buy back 1.8 points of monthly churn — and is churn even the thing that program can move?

Note what this is *not*. It is not "should we have a loyalty program" and not "should we respond to the rival." The triggering event (rival launch, board deadline) is not the question. The question is a purchase: we are being asked to buy a churn reduction at a stated price, on the basis of an effect size nobody has yet evidenced.

**Success criteria** — a correct answer must:

1. Compare the program's all-in cost against the margin value of averted churn, not the gross revenue value.
2. Establish whether the churn the program can address is the churn we actually have.
3. Identify the cheapest alternative that buys the same outcome (funding decisions are comparative, not absolute).
4. Fit the three-week window, or explicitly state what the window forces us to give up.

---

## 2. Assumptions Table

| # | Assumption | Type | Treatment | Verdict |
|---|---|---|---|---|
| A1 | $19 × 48,000 members is the revenue base | current constraint | Accept; expires on any pricing/tier change | **Accepted** — given |
| A2 | The $310k "to run" figure is the total cost | untested belief | Challenge before use | **REJECTED as stated.** "Run" cost conventionally means ops/tooling/staff. Points redeemed for account credit are a *separate* contra-revenue cost that scales with the member base. Scope must be confirmed. |
| A3 | The program will pull churn to ~5% | untested belief | Verify or flag | **Unverified — flagged.** No cited evidence. Presented as a "bet." Load-bearing for the entire case. → GT-9? |
| A4 | The churn that rose is churn a loyalty program can address | untested belief | Verify | **Unverified — flagged.** Involuntary churn (card failures, dunning) is typically 20–40% of SaaS churn and is completely unresponsive to points. → GT-10? |
| A5 | The rival's program is relevant to our decision | convention | Challenge explicitly | **REJECTED as a reason.** Timeline disproves causation (GT-7). Competitive symmetry is not evidence of value. |
| A6 | Gross margin on subscription revenue | untested belief | Verify | **Unverified — flagged.** Not supplied. Swings the answer materially. → GT-11? |
| A7 | The base is roughly at steady state (gross adds ≈ gross churn) | untested belief | Verify | **Unverified — flagged**, used with a bracket. → GT-6? |
| A8 | Retention spend must be a standing entitlement rather than a targeted intervention | convention | Challenge explicitly | **REJECTED.** Program-wide entitlements pay the majority of their cost to members who were never going to leave. |
| A9 | The three-week window forces a fund/don't-fund binary | convention | Challenge explicitly | **REJECTED.** Three weeks is ample to *diagnose*; it is not enough to *validate an effect size*. The window constrains the decision's form, not its existence. |
| A10 | A launched loyalty program can be withdrawn if it underperforms | untested belief | Challenge | **REJECTED as safe.** Removing an earned benefit reads to members as a takeaway; practical reversibility is near zero. |

**Fishbone pass on the churn rise** (default six-category set), to keep the assumption space from being set by whoever spoke first. Every branch below is an `untested belief` and none has been excluded by evidence supplied:

- **People:** support quality/staffing change; sales channel mix shift bringing lower-fit members
- **Process:** dunning/payment-retry regression; a renewal or cancellation flow change; an onboarding change
- **Technology:** product reliability regression; a feature removal or redesign
- **Environment:** macro/discretionary-spend pressure; category-wide substitution
- **Information:** the metric definition or measurement window changed; the denominator changed
- **Resources:** a promo/discount cohort from ~2–3 quarters ago hitting first full-price renewal — a cohort artifact, not a trend

That last branch deserves emphasis: a 4.2% → 6.8% move is a **62% relative jump in two quarters**. Trends of that shape are usually a *specific event* — a cohort, a regression, a billing change — not a diffuse decline in loyalty. Diffuse loyalty decay is the one cause a points program addresses, and it is the least likely explanation for this curve shape.

---

## 3. Ground Truths

| ID | Fact | Source |
|---|---|---|
| GT-1 | Base = 48,000 × $19 = **$912,000 MRR**, ≈ **$10.94M/yr** gross | Given + arithmetic |
| GT-2 | Monthly churn 6.8%, previously 4.2%; delta = 2.6 pp (+62% relative) | Given |
| GT-3 | At 6.8%: **3,264 members/month** lost = $62,016 MRR/month | GT-1 × GT-2 |
| GT-4 | Target 5.0% implies **1.8 pp** reduction = **864 members/month** retained | GT-2, GT-3 |
| GT-5 | Steady-state base = gross adds ÷ churn rate | Definitional identity |
| GT-6? | Gross adds ≈ 3,264/month (steady-state inference) | *Unverified* |
| GT-7 | The rival's program launched **after** the churn rise began → it cannot be the cause | Given timeline |
| GT-8 | Points redeemed for account credit are contra-revenue — economically a **discount with a delay and an administrative layer** | Definitional |
| GT-9? | Effect size = 1.8 pp | *Unverified — stated as a bet* |
| GT-10? | Voluntary/involuntary churn split | *Unverified — not supplied* |
| GT-11? | Gross margin | *Unverified — not supplied* |
| GT-12 | Decision window: 3 weeks, board update | Given |

---

## 4. Derivation Chains

### Chain A — The upside, sized honestly

Year-one value is *not* the steady-state value; the base migrates toward the new equilibrium gradually. Modeling the base at 5% churn with adds held at GT-6?:

- New equilibrium: 3,264 ÷ 0.05 = **65,280** members (vs. 48,000 today)
- Cumulative incremental **member-months in year 1** ≈ 17,280 × (12 − Σ0.95ᵗ) ≈ 17,280 × 3.27 ≈ **56,500**
- At $19: **≈ $1.07M incremental gross revenue in year 1** (bracket: **$0.85M – $1.20M**)

> GT-3 + GT-4 + GT-5 + GT-6? → year-1 incremental member-months ≈ 56,500 → **≈$1.07M incremental gross revenue**, *conditional on GT-9? holding in full*. **Confidence: MEDIUM** (arithmetic is sound; both inputs GT-6? and GT-9? are unverified).

### Chain B — The cost, rebuilt from unit-factors

The stated $310k does not include the credit itself. Rebuilding it (units: % of revenue earned × redemption rate × revenue base):

| Factor | Conservative | Central | Aggressive |
|---|---|---|---|
| Earn rate (% of spend) | 2% | 5% | 10% |
| Redemption rate (net of breakage) | 50% | 70% | 80% |
| Credit cost on $10.94M | $109k | $383k | $875k |
| **+ stated run cost** | **$419k** | **$693k** | **$1,185k** |

> GT-1 + GT-8 + A2-rejected → redemption credit is a second, larger, revenue-scaling cost line → **all-in cost is $419k–$1,185k, not $310k**. **Confidence: MEDIUM-HIGH** on the structure, LOW on the point value until the program's earn/redemption design is specified.

### Chain C — Breakeven, and where it bites

Solving Chain A backwards: the program breaks even on **gross revenue** at roughly a **0.55 pp** churn reduction if $310k were truly all-in. But against the Chain B cost range and a plausible 75% gross margin:

- Year-1 contribution from Chain A: $1.07M × 0.75 ≈ **$805k**
- Cost, central: **$693k** → net **+$112k** (a 10% surplus on a seven-figure program)
- Cost, aggressive: **$1,185k** → net **−$380k**
- If the effect is **half** of what's claimed (0.9 pp): contribution ≈ **$400k** → **negative in every cost scenario except the most conservative**

> Chain A + Chain B + GT-11? → the bracket **straddles zero** → per the decision-resolution stop criterion, **this estimate does not resolve the decision**. **Confidence: HIGH** that it does not resolve; the straddle is robust to reasonable re-parameterization.

The dominant uncertain factor is not cost — it is **GT-9?, the effect size**, which is currently a hope with a number attached.

### Chain D — Mechanism check

> GT-2 + GT-10? + fishbone → the observed curve is a sharp two-quarter step, whose likeliest causes (cohort renewal cliff, dunning regression, product/pricing event, measurement change) are **all unresponsive to points** → a loyalty program is a **generic treatment applied to an undiagnosed specific cause**. **Confidence: MEDIUM-HIGH.**

Concretely: if even 30% of the 6.8% is involuntary (failed payments), a points program addresses at most 4.8 points of churn, and dunning improvements — typically a five-figure project — would recover more churn per dollar than the entire $310k.

### Chain E — Second-order effects

Extending Chain C forward:

**2nd order:**
- The rival matches or has already matched → the program becomes table stakes, conferring **no differentiation**, only a permanent cost line (GT-7, A5)
- Redemption liability accrues on the balance sheet and grows with the base
- Roughly **93% of monthly credit** flows to the ~93% of members who were not going to churn this month — structural deadweight (A8)

**3rd order:**
- Competition migrates from product to discount depth; both parties' unit economics compress
- The program becomes **practically irreversible** (A10), so a wrong call is not a one-year $310k mistake but a standing annuity
- Point-based credit trains price sensitivity into a base that currently accepts $19 without one

**Contradiction check:** No 3rd-order effect contradicts a ground truth, so no return to Phase 2 is triggered. But the irreversibility effect materially raises the evidentiary bar — an irreversible commitment justified by an unverified effect size (GT-9?) is the specific pattern this methodology exists to catch.

### Chain F — The comparative test

> GT-8 + A8-rejected → points-for-credit is a delayed, administered discount → **any outcome it buys can be bought more cheaply and more measurably by a direct, targeted retention offer to the at-risk cohort**, at a fraction of the deadweight. **Confidence: MEDIUM-HIGH.**

---

## 5. Abandoned Reasoning

- **Per-member LTV framing.** Initially valued each retained member at 1/0.05 × $19 = $380 lifetime and multiplied by 864/month → ~$3.9M. Discarded: it books multi-year lifetime value against a one-year cost, which flatters the program. Year-one member-months is the honest comparison for an annually-funded program.
- **Steady-state framing as the headline number.** The +17,280 steady-state member figure (+$3.9M annualized) is real but arrives asymptotically; leading with it would overstate the year-one case by ~4×. Retained as context only.
- **"The rival did it" as evidence.** Discarded per the no-analogy rule — we have no ground truth about the rival's churn, margin, or program economics, so their launch carries zero evidential weight about *our* return. GT-7 further removes it as a causal explanation.
- **Treating the 3-week window as forcing a yes/no.** Discarded (A9): the window's real constraint is that it precludes *validating* an effect size, which is an argument for changing the shape of the commitment, not for guessing.

---

## 6. Conclusion

**Do not fund the program at $310,000 as specified. Confidence: MEDIUM-HIGH.**

Three findings drive it, in order of weight:

1. **The price is not $310k.** Points redeemed for account credit are a separate, revenue-scaling contra-revenue line worth an estimated $110k–$875k/yr. All-in cost is **$419k–$1,185k**. The proposal as presented understates its own cost by roughly 2×. *(Chain B)*
2. **The central case is a coin flip, not an investment.** Against a 75% margin, the central case nets ~+$112k on a ~$693k spend — and turns sharply negative if the effect size is half of what's claimed. The 1.8 pp figure has no evidence behind it. *(Chain C)*
3. **The mechanism may not touch the problem.** A 62% relative churn jump in two quarters has an event shape, not a loyalty-decay shape. Until the churn is decomposed, this is a generic treatment for an undiagnosed cause. *(Chain D)*

Combined with irreversibility (A10) and near-total deadweight to non-churners (Chain E), this is a permanent, undifferentiated cost committed on unverified grounds.

### What to bring to the board in three weeks instead

Three weeks is not enough to validate an effect size, but it is more than enough to do the following — and each item directly resolves a flagged `GT-N?`:

| Days | Action | Resolves |
|---|---|---|
| 1–5 | Decompose churn: voluntary vs. involuntary; by cohort, tenure, acquisition channel, plan | GT-10?, Chain D |
| 1–5 | Confirm the $310k's scope and the intended earn/redemption design; get gross margin | A2, GT-11? |
| 5–10 | Exit-survey / cancellation-reason pull on the last two quarters of churners | GT-9?, Chain D |
| 10–21 | Design a **bounded pilot**: targeted retention offer to the identified at-risk cohort only, with a holdout control, budgeted at ~10–15% of $310k | Chain F, A8 |

**The board ask becomes:** approve a ~$40k instrumented pilot with a holdout, and a decision gate at 90 days on measured lift — rather than a $310k–$1.2M standing entitlement on an unmeasured bet.

### Weakest links in this analysis

- **GT-9? (effect size)** is load-bearing for Chain A and remains unverified in both directions. If customer success holds evidence for the 1.8 pp figure — a prior program, a competitor benchmark, a survey — that evidence would raise Chain A to HIGH confidence and could flip the recommendation. Ask for it before the board meeting; its absence is itself informative.
- **GT-11? (gross margin)** shifts Chain C's central case by roughly ±$150k. Verifiable in an afternoon.
- **GT-6? (steady-state adds)** biases Chain A's magnitude but not its sign; if the base is growing, the program's value is larger in absolute terms, though the deadweight critique (Chain E) intensifies with base size.
- **Pre-mortem residual:** the most likely way this recommendation is *wrong* is that the churn decomposition comes back showing genuine broad-based value erosion with no cohort or billing signature — the one world where a standing loyalty benefit is the right instrument. The 5-day diagnostic is designed to detect exactly that, cheaply, before the window closes.