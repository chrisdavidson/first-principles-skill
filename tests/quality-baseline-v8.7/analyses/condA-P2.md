## Missing inputs (flagged, proceeding best-effort)

Four inputs would materially sharpen this and I don't have them: (1) whether the 5% is **logo** or **revenue** churn and whether it's gross or net; (2) the **churn curve by tenure cohort** (flat vs. front-loaded); (3) the **involuntary/voluntary split** (failed payments vs. deliberate cancels); (4) B2C vs. B2B and ARPU. Where I've had to assume, the ground truth carries a `?` and the dependent conclusion carries a confidence caveat.

---

## 1. Problem Essence

**Core question:** Not "should we build a loyalty program?" but — *what mechanism is causing 5% of paying customers to leave each month, and is a rewards program the highest-return intervention against that mechanism?*

The team has proposed a solution before naming a cause. "Loyalty program" is an answer to "our customers lack an incentive to stay." That is one hypothesis among at least seven, and it has not been tested.

**Success criteria for a correct answer:**
- Names the churn *mechanism(s)*, not just the rate.
- Compares the proposed intervention against the cheapest alternative that attacks the same mechanism.
- States what would have to be true for the loyalty program to be right.
- Resolves to a decision, or explicitly states the decision cannot yet be resolved and names the information that would resolve it.

---

## 2. Assumptions Table

| Assumption | Type | Treatment | Verdict | Verification |
|---|---|---|---|---|
| 5% monthly churn is abnormally high | convention | Challenge before use | **Contested.** For B2C subscription, 3–8%/mo is an ordinary band; for B2B SaaS it is 3–5× the norm | Unverified — depends on segment, which I wasn't given |
| Churn is a single phenomenon with a single fix | untested belief | Verify or flag | **Rejected.** Churn is definitionally an aggregate of involuntary + voluntary, and voluntary decomposes further | Fishbone below |
| Customers leave because they lack loyalty incentives | untested belief | Verify or flag | **Unverified — flagged.** No cancel-reason or cohort data cited | This is the load-bearing assumption of the entire proposal |
| Rewards can influence a failed credit card | physical/mechanistic | Accept as ground-truth candidate | **False.** No reward mechanism touches an expired card | Mechanistic — GT-4 |
| Reward payouts convert 1:1 into retention | untested belief | Challenge | **Rejected.** Payout goes to all redeemers; benefit comes only from the marginal switcher | GT-7 |
| Churn is spread evenly across tenure | untested belief | Verify or flag | **Unverified — flagged.** Subscription churn is usually front-loaded | GT-6? |
| The team has capacity to build this without displacing other work | untested belief | Challenge | **Rejected by default.** Engineering capacity is rivalrous; this displaces something | Structural |
| A loyalty program's cost is the build cost | untested belief | Challenge | **Rejected.** Reward liability is a permanent margin line, not a one-time cost | GT-8 |

**Fishbone (default six-category set), to widen the cause space before narrowing:**

- **Information/Payments:** expired cards, dunning gaps, failed retries, involuntary churn
- **Process/Onboarding:** users never reach first value; activation failure in week 1
- **Product:** value decays after the job is done ("goal completion" churn); missing feature; reliability
- **People/Acquisition:** a channel or promo delivers mis-expecting, low-intent cohorts
- **Environment:** competitor launch, price sensitivity, seasonality, budget cycles
- **Resources/Support:** unresolved tickets preceding cancels

A loyalty program addresses at most a slice of one branch (Product/perceived ongoing value). Every other branch is untouched by it.

---

## 3. Ground Truths

- **GT-1** *(arithmetic, verified)*: 5%/mo → 0.95¹² = 0.54, i.e. ~46% of paying customers lost per year; mean customer lifetime = 1/0.05 = **20 months**.
- **GT-2** *(definitional, verified)*: Gross churn ≡ involuntary churn (payment failure) + voluntary churn (deliberate cancel). These have disjoint causal mechanisms.
- **GT-3?** *(untested belief — industry pattern, unverified for this app)*: Involuntary churn is commonly 20–40% of gross subscription churn.
- **GT-4** *(mechanistic, verified)*: A rewards program operates by changing a customer's *decision* to cancel. It has no mechanism that acts on a declined transaction. Therefore its addressable share of churn is bounded above by the voluntary share.
- **GT-5** *(definitional, verified)*: Loyalty rewards accrue with tenure. Payout is therefore weighted toward long-tenured customers.
- **GT-6?** *(untested belief — unverified for this app)*: Subscription churn is typically front-loaded, concentrated in months 0–3.
- **GT-7** *(economic, verified)*: Reward cost is incurred against **all** redeemers; retention benefit is generated only by the **marginal** customer whose decision the reward changed. Incrementality is therefore strictly less than redemption, usually by a large factor.
- **GT-8?** *(estimate, bracketed below)*: Build cost ≈ 2–4 engineers × 3–6 months ≈ **$90k–$360k**, central ~$200k, plus ongoing reward liability and ~0.5 FTE ops.
- **GT-9** *(verified from the prompt)*: No diagnosed cause has been stated. The proposal is solution-first.

---

## 4. Derivation Chains

**Chain A — the proposal is untethered from a diagnosis.** *(HIGH)*
GT-9 + GT-2 → the "5%" is an aggregate of mechanistically disjoint components, none of which has been sized → committing engineering capacity to one mechanism-specific intervention before decomposition is a bet placed before the cards are dealt → **the decision as posed cannot be answered "yes" on available evidence.**

**Chain B — a structural ceiling on what the program can do.** *(MEDIUM — rests on GT-3?)*
GT-2 + GT-3? + GT-4 → if 20–40% of the 5 points is involuntary, that's **1.0–2.0 points/mo the loyalty program cannot touch at any budget** → the program's addressable ceiling is 3.0–4.0 points → meanwhile the untouchable 1.0–2.0 points is attackable by card-updater services, smart dunning, and retry-timing at roughly **$10k–30k and a few engineer-weeks**, typically recovering 20–40% of failed payments (≈0.3–0.7 churn points) → **there is a cheaper intervention with a larger evidenced effect sitting unbuilt.** *Raise to HIGH by pulling one number: the share of cancels that are payment-failure driven.*

**Chain C — Fermi: the cost/benefit bracket straddles zero.** *(MEDIUM)*
Target quantity: **net change in LTV**. Units: (Δ lifetime months) × (contribution margin/month), with margin itself moved by reward cost.
- GT-1 → baseline lifetime 20 months.
- Optimistic: 20% relative churn reduction (5.0 → 4.0) → lifetime 25 mo → **+25% lifetime**.
- Central: 10% relative reduction (5.0 → 4.5) → lifetime 22.2 mo → **+11% lifetime**.
- Pessimistic: rewards land almost entirely on customers who would have stayed (GT-7) → **+0% lifetime**.
- Reward liability: ~5% of revenue given back to ~50% of the base → **~2.5% of revenue**, i.e. ~3.6% of contribution margin at a 70% margin, **permanent**.

Net LTV: **[−3.6%, +7%, +20%]**, plus a one-time $90k–360k (GT-8?).

→ The bracket **straddles zero**. Per the decision-resolution stop criterion, an estimate whose lower and upper ends drive *opposite* decisions is not good enough to act on → **the correct move is to buy information, not to fund the build.** The dominant uncertain factor is the incrementality of the reward, and it is measurable in weeks via a holdout test on an existing discount/save offer.

**Chain D — probable mistiming.** *(LOW–MEDIUM — rests on GT-6?)*
GT-5 + GT-6? → rewards pay out to long-tenured customers while churn concentrates in months 0–3 → the program spends most of its budget on the cohort *least* at risk, and offers the at-risk cohort a benefit that hasn't vested yet → **if the churn curve is front-loaded, the program is structurally aimed at the wrong cohort, and the right intervention is activation/onboarding, not rewards.** One cohort chart falsifies or confirms this.

**Chain E — second-order effects** (applied to the first-order conclusion "we ship a loyalty rewards program"):

*2nd order:*
1. Reward value becomes an expectation, not a delight → margin reduction is permanent and non-reversible without a perceived takeaway.
2. Discount-shaped rewards skew acquisition and retention toward price-sensitive users.
3. Engineering attention moves off the product-value branch of the fishbone for 3–6 months.
4. Accrued unredeemed rewards become a balance-sheet liability requiring ongoing accounting treatment.

*3rd order:*
5. From (2): the surviving base has *higher* price sensitivity → churn re-rises when the reward is matched by a competitor or trimmed → **contradicts GT-1's assumption that the intervention is churn-reducing.** ⚠️
6. From (1)+(4): margin compression narrows future CAC headroom, slowing growth even if churn improves.
7. From (3): if the true cause was activation (GT-6?), the underlying leak widens for two quarters while the program is built.

**Effect (5) is a contradicting effect.** Per the routing rule, this sends the conclusion back to Phase 2 rather than forward — and the assumption it invalidates is "reward-driven retention is durable," which now enters the table as a further untested belief. This is why I do not offer a "yes, but smaller" conclusion.

---

## 5. Abandoned Reasoning

- **"5% is above/below benchmark, therefore act/don't act."** Abandoned: benchmark comparison is reasoning by analogy — it tells you about other companies' situations, not yours, and I lack the B2C/B2B split that would even make the comparison meaningful. It cannot carry a conclusion.
- **"Loyalty programs work for airlines and coffee chains, so they'll work here."** Abandoned as pure analogy. Those are high-frequency, low-switching-cost, commoditized *transactional* choices where the program creates artificial switching cost. A subscription already has a switching cost (the subscription itself); the churn decision is about perceived ongoing value, not about which vendor to transact with today. The analogy is not grounded in any verified ground truth about this app.
- **A weighted trade-off matrix across interventions.** Started, then abandoned: scoring "loyalty program vs. dunning vs. onboarding" requires weighting criteria I cannot set without knowing the churn decomposition. Producing a matrix here would manufacture false precision — the matrix's output would be entirely determined by weights I'd be guessing at.
- **Recommending a cheap "loyalty-lite" pilot as a compromise.** Abandoned after Chain E effect (5): a discount-shaped pilot still risks skewing the cohort and still doesn't discriminate between causes. A holdout test on an *existing* save offer gets the same information with no new build.

---

## 6. Conclusion

**No — not yet.** Not "never," but the decision cannot responsibly be made "yes" on what's currently known, and the analysis says the odds are against it.

The strongest single finding: **the cost/benefit bracket straddles zero** (Chain C, [−3.6%, +20%] net LTV against a $90k–360k build). When an estimate's pessimistic and optimistic ends drive opposite decisions, the correct action is to buy the information that narrows the bracket — not to spend $200k picking one end of it.

Three supporting findings:
- The program has a **hard structural ceiling** — it cannot touch involuntary churn at any budget (Chain B), while the intervention that *can* costs ~10% as much.
- It is **probably mistimed** — rewards vest with tenure, churn probably concentrates early (Chain D).
- It carries a **contradicting second-order effect** — discount-shaped retention selects for price-sensitive customers, which re-raises churn later (Chain E-5).

**What to do instead, in order — roughly 3–4 weeks and ~$10–30k of analyst time:**

1. **Split the 5% into involuntary vs. voluntary.** One query. If involuntary is >1 point, ship dunning + card-updater immediately; it is the cheapest churn point available anywhere in this analysis.
2. **Plot churn by tenure cohort.** If it's front-loaded, the answer is activation/onboarding and the loyalty program is aimed at the wrong people.
3. **Read cancel reasons and interview 20 churned customers.** Cheapest possible test of the proposal's load-bearing assumption ("they leave for lack of incentive"). My expectation is you'll find price, unmet expectation, or job-completed — not absence of rewards.
4. **Run a holdout on any existing save/discount offer** to measure reward incrementality (GT-7) before assuming it.

**What would flip this to "yes":** involuntary churn is small (<0.5 pts), the churn curve is *flat or back-weighted*, cancel reasons cluster on "found a cheaper alternative" or "didn't feel I was getting enough for the price," and a holdout shows measured incrementality above ~15%. Under all four, Chain C's bracket lifts clear of zero and the program becomes defensible. Absent them, the loyalty program is an expensive answer to a question nobody has asked yet.

**One reframe worth naming:** the team's instinct is not wrong that 5%/mo is worth attacking — GT-1 says you're rebuilding nearly half your customer base annually. The error is not the ambition; it's jumping from a *number* to a *solution* without passing through a *mechanism*.agentId: a2fdba4a38ac87374 (use SendMessage with to: 'a2fdba4a38ac87374', summary: '<5-10 word recap>' to continue this agent)
<usage>subagent_tokens: 35830
tool_uses: 0
duration_ms: 110870</usage>
