# First-Principles Analysis: Fund the loyalty program at $310k/year?

**Step 0 — Technique selection:** No focused-technique trigger phrase fires (no "pre-mortem," "invert," "trade-off analysis," etc. — the competitor mention and deadline are context, not technique requests). `MODE = full-composer`. All five phases run; Phase 4 enumerates the companion techniques that earn their place (estimate, second-order, trade-off, inversion for assumption-surfacing).

---

## 1. Problem Essence

**Essence Statement:** Is spending $310k/year on a points-for-credit loyalty program a positive-expected-value way to reduce monthly churn, given that the decision rests on an unverified bet that the program moves churn and on an ambiguous cost figure?

Note the reframe: the triggering question is "fund the program yes/no," but the *real* decision has two nested sub-questions the framing hides — (a) do the economics survive if the program delivers only *part* of its promised effect, and (b) is a credit incentive even the right instrument for *why* churn rose? A yes/no on the program that skips (b) risks buying a treatment for the wrong disease.

**Success criteria** (checkable against the conclusion):
- S1: Establishes the break-even churn reduction, not just the promised one.
- S2: Separates the *facts* (member count, price, current churn) from the *bet* (churn falls to 5%).
- S3: Resolves or explicitly flags the "$310k all-in?" ambiguity, since it is load-bearing.
- S4: Does not treat the rival's launch as evidence the program works.
- S5: Fits an actionable answer inside the 3-week window.

---

## 2. Assumptions Table

| # | Assumption | Type | Treatment | Verdict | Verification |
|---|---|---|---|---|---|
| A1 | The program actually pulls churn toward ~5% (a 1.8pp drop) | untested belief | Verify or flag; it is the central bet | **Unverified — load-bearing** | No causal evidence supplied; it is a projection |
| A2 | $310k is all-in, *including the account-credit liability members redeem* | untested belief | Verify before decision | **Unverified — must clarify** | "Cost to run" is ambiguous; credits are a revenue give-back, not opex |
| A3 | Gross margin on subscription revenue is high (~70–100%) | convention | Challenge in context | **Plausible, confirm** | Typical for digital subscriptions; unstated here |
| A4 | Churn rose for a reason a credit incentive can address (price/value perception), not a structural product/market failure | untested belief | Verify — root-cause the churn spike | **Unverified — high leverage** | 4.2%→6.8% cause not diagnosed |
| A5 | Some redeemers would have stayed anyway (incentive dilution / discount-seekers) | untested belief | Flag; sizes the true net cost | Unverified | Inherent to broad loyalty programs |
| A6 | Rival's launch is evidence the program works | convention / analogy | **Challenge and reject as evidence** | **Rejected as evidence** (D: no-analogy rule) | Their situation ≠ ours; competitive *pressure* is a real 2nd-order factor, their *result* is not our data |
| A7 | Acquisition rate stays roughly stable, so churn savings compound on an ongoing base | current constraint | Record expiry | Accepted for base case | Holds unless acquisition collapses |
| A8 | The decision is time-boxable / reversible | current constraint | Record | Accepted | A pilot can be killed; reputational cost of withdrawal is modest |

**Inversion pass (to surface hidden preconditions of "fund it"):** What would *guarantee* the program is a bad call? (1) $310k excludes redeemed credits → true cost is 2–3× higher; (2) churn is driven by a product/competitor problem credits can't touch → churn keeps climbing and you've added cost; (3) credits are redeemed overwhelmingly by loyal members → pure margin give-away with no retention lift. Each is now a row above (A2, A4, A5). None is currently ruled out — hence the conditions in the conclusion.

---

## 3. Ground Truths

- **GT-1:** 48,000 active members. *(given)*
- **GT-2:** Price $19/member/month. *(given)*
- **GT-3:** Current monthly churn 6.8% (up from 4.2% over two quarters). *(given)*
- **GT-4?:** Program cost ~$310k/year — **`?` because scope ("to run") is unverified** re: whether it includes the redeemed-credit liability. *(given, flagged)*
- **GT-5:** Monthly revenue = members × $19. *(definitional)*
- **GT-6:** A retained member generates recurring $19/month until they churn; reducing the monthly churn rate raises the survival curve of the whole base. *(definitional of a subscription)*
- **GT-7:** Rival launched a similar program last month. *(given — a fact about the market, NOT evidence of program efficacy)*
- **GT-8:** Decision window is 3 weeks. *(given)*

The "target 5% churn" figure is deliberately **not** a ground truth — it is A1, the bet. Promoting it to a fact would be the single most common failure mode here.

---

## 4. Derivation Chains

**Estimate procedure — value of a 1.8pp churn reduction in year 1.** Target unit: incremental subscription revenue ($). Model: hold acquisition flat (conservative — isolates the churn effect), compare cumulative member-months over 12 months at survival factor 0.932 (6.8%) vs 0.950 (5.0%).

- Member-months, base (r=0.932): 48,000 × Σr^t(t=0..11) = 48,000 × 8.39 ≈ 402,500
- Member-months, program (r=0.95): 48,000 × 9.19 ≈ 441,200
- Δ ≈ 38,700 member-months × $19 ≈ **$735k incremental revenue, year 1**

Bracket: **[lower ≈ $500k** (apply ~70% gross margin, haircut for dilution A5) **, central ≈ $550–735k, upper > $1M** (multi-year LTV + compounding on a growing base)]. Both ends of the bracket exceed the $310k cost — the estimate resolves the decision.

**Chain C1 — Margin of safety (the load-bearing result):**
> GT-1 + GT-2 + GT-3 + GT-6 → a 1.8pp churn drop is worth ≈ $735k/yr revenue (~$550k at margin) → **break-even needs only ≈ 1.0pp of churn reduction** (churn to ~5.8%), i.e. the program pays back if it delivers just over *half* its promised effect → **the bet has a wide margin of safety.** *(Confidence: HIGH on the arithmetic; MEDIUM overall because it inherits A1's uncertainty about whether* any *effect materializes.)*

**Chain C2 — Cost-scope sensitivity:**
> GT-4? + A2 + A5 → IF $310k excludes redeemed credits, true cost could be $500k–$900k (credit give-away scales with membership) → break-even churn reduction rises to ~1.7–3.0pp → **the margin of safety in C1 collapses.** *(Confidence: MEDIUM — this is why A2 must be clarified before signing. This single ambiguity swings the answer more than any other input.)*

**Chain C3 — Root-cause fit (trade-off framing):**
> GT-3 (churn rose 62% relative) + A4 → the program is only high-ROI if the churn driver is incentive-addressable → if the spike is a product regression, a pricing-perception break, or the rival poaching on *features* rather than price, credits treat a symptom → **a 3-week parallel churn diagnosis is a near-zero-cost hedge that de-risks C1.** *(Confidence: MEDIUM.)*

**Chain C4 — Competitive second-order (2nd/3rd-order pass):**
> GT-7 → points-for-credit may be becoming table-stakes in this category → 2nd-order: *not* funding while the rival offers it could itself accelerate churn (a cost of inaction, not just forgone benefit) → 3rd-order: BUT credits also train members to expect discounts and attract price-sensitive redeemers (A5), which can depress long-run ARPU. → Net: competitive pressure raises the value of *acting*, but favors a **differentiated / capped** design over an open-ended one. *(No step contradicts a Ground Truth — no return to Phase 2 required.)*

**Assumption Audit (end-of-Phase-4 scan):**

| Chain | Step | Step text (brief) | Assumption surfaced? | Added to table? |
|---|---|---|---|---|
| C1 | 1 | 1.8pp worth ~$735k | A3 (margin), A1 (effect real) | Already A1/A3 → `[Assumes: A1, A3]` |
| C1 | 2 | break-even ~1.0pp | none new | clean |
| C2 | 1 | true cost if credits excluded | A2, A5 | Already present |
| C3 | 1 | driver is incentive-addressable | A4 | Already present |
| C4 | 1 | table-stakes / inaction cost | A6 (reframed as pressure, not evidence) | Already present |
| C4 | 2 | discount-training depresses ARPU | A5 | Already present |

No new assumptions surfaced beyond the Phase 2 table. Clean pass.

---

## 5. Abandoned Reasoning

- **"The rival launched it, so it must work — copy them."** Abandoned per the no-analogy rule (A6). Their result is not our evidence; only the *competitive-pressure* fact (GT-7) survives, and it argues for acting, not for this specific design.
- **Full multi-year LTV/DCF model.** Considered and set aside: the year-1 estimate already clears the decision threshold at both bracket ends, so a heavier model adds precision the decision doesn't need (estimate stop-criterion: both bounds drive the same call — *conditional* on A2).
- **"Just decide yes/no in 3 weeks as asked."** Abandoned as under-scoped: the 3 weeks are better spent resolving A2 (finance can answer in days) and running a churn diagnosis in parallel, converting a blind bet into an informed one within the same window.

---

## Process gates

**§6→§4 closure ledger:**
- "Fund it, conditionally" → chains C1 + C2 ✓
- "Structure as a capped, time-boxed pilot with a kill criterion" → chains C1 + C4 ✓
- "Clarify $310k scope before signing" → chain C2 ✓
- "Run a parallel churn root-cause diagnosis" → chain C3 ✓
- "Don't treat the rival as proof" → GT-7 / A6 ✓

Ledger clean — every §6 claim carries a chain. **Rubric pass:** essence reframed (S1–S5 met); every assumption classified with a verdict; ground truths carry the `?` flag where unverified (GT-4?); each chain has an intermediate step and a confidence level; the load-bearing weak link (A1 effect real, A2 cost scope) is explicitly flagged, not buried. Gate cleared.

---

## 6. Conclusion

**Conditional YES — fund it, but as a capped, time-boxed pilot with a hard kill criterion, and only after resolving one cost question.** All three actions fit inside the 3-week window.

**Why the economics favor funding (C1):** A 1.8pp churn reduction is worth roughly $735k/year in revenue (~$550k at margin) against a $310k cost. The break-even is only ~1.0pp — the program pays for itself if it delivers *just over half* its promised effect. That is a genuinely wide margin of safety, which is what makes this an attractive bet even though the effect is unproven.

**The one thing that can flip the answer (C2):** Whether $310k is *all-in including redeemed account credits*. Account credit is a direct revenue give-back that scales with membership; if it sits outside the $310k, true cost could be $500k–$900k and the margin of safety collapses. **Confirm this with finance before signing — it is a days-long question and the highest-leverage unknown in the whole decision.**

**De-risk the bet, don't just place it (C3, C4):**
- Run a **parallel churn root-cause diagnosis** in the same 3 weeks (exit-survey/cohort/cancel-reason data). If churn rose because of a product regression or the rival's *features*, credits treat a symptom and you should redirect the spend.
- Structure as a **6-month pilot with a pre-registered kill criterion** (e.g., "churn must fall below ~5.8% — the break-even line — by month 4, or we stop"). Cap redemption value and design for differentiation, since open-ended credits train discount-seeking and depress long-run ARPU.
- Note the **cost of inaction** (C4): with the rival live, doing nothing is not neutral — it may itself accelerate churn. That strengthens the case for acting, but not for an uncapped design.

**Explicit confidence caveat:** The recommendation is MEDIUM confidence, gated on two unverified inputs — A1 (that the program moves churn at all) and A2 (cost scope). Verifying A2 and committing to a kill criterion is what converts this from a hope into a bounded, positive-expected-value bet. Do **not** let the rival's launch (GT-7/A6) substitute for evidence that the mechanism works for *your* churn.

---

No files were created or modified — this analysis is returned inline as requested.