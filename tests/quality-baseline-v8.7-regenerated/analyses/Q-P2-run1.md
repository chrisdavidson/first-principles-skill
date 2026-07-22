## 1. Problem Essence

**Core problem:** Is $310,000/year of recurring spend on a points-for-credit loyalty program the highest-return way to reverse a 2.6-percentage-point monthly churn increase whose cause has not been diagnosed — and is a three-week deadline a reason to commit rather than a reason to buy information?

**Success criteria** (each checkable against section 6):

1. The Conclusion states a break-even churn improvement in percentage points, derived from the $310,000 figure and the revenue base — not an assertion that the program "pays for itself."
2. The Conclusion names the specific unknown that flips the recommendation, and states what measurement resolves it.
3. The Conclusion delivers a decision that can be made inside three weeks, without that decision being a yes/no on the full $310,000.
4. The Conclusion does not use the rival's launch as evidence for funding.

---

## 2. Assumptions Table

| Assumption | Type | Treatment | Verdict | Verification |
|---|---|---|---|---|
| 48,000 members × $19/mo = $10.944M annual gross billings | current constraint | Expiry: changes with base size, price, or mix | Accept | User-stated + arithmetic |
| Monthly churn is 6.8%, up from 4.2% over two quarters | current constraint | Expiry: this is the variable under intervention | Accept | User-stated |
| $310,000/yr is the true full cost of the program | untested belief | Verify or flag | **Challenge** | unverified — flagged (GT-10?): "cost to run" typically means operations/tooling; redeemed credit is a separate contra-revenue line |
| Contribution margin per subscription dollar | untested belief | Verify — this is load-bearing | **Challenge** | unverified — flagged (GT-9?): not supplied; retained revenue ≠ retained profit |
| The loyalty program will move churn to ~5.0% | untested belief | Verify or flag | **Challenge** | unverified — flagged (GT-13?): a forecast by the team proposing the spend |
| Gross adds are stable at ≈3,264/mo (base roughly flat) | untested belief | Verify or flag | **Challenge** | unverified — flagged (GT-11?): if the base is shrinking, absolute benefit is smaller |
| Churn is a single behaviour addressable by one lever | convention | Explicitly challenge before use | **Discard** | Churn is a mixture (involuntary/payment-failure, onboarding-cohort, tenure, channel, plan). A blended rate is not an actionable object |
| "The rival launched one; we need parity" | convention | Explicitly challenge before use | **Discard** | Reasoning by analogy. No verified ground truth about the rival's cost base, churn, or results exists |
| A 3-week deadline requires a yes/no on the full spend | convention | Explicitly challenge before use | **Discard** | The deadline constrains *when a decision is made*, not *what is decided*. Conditional commitment is a decision |
| Retention economics compound: base equilibrium = adds ÷ churn; LTV = ARPU ÷ churn | physical law (mathematical) | Accept as ground-truth candidate | Accept | Geometric series identity |
| Statistical power for a two-proportion churn test | physical law (mathematical) | Accept as ground-truth candidate | Accept | Standard two-proportion sample-size formula |
| Retention response to a small price concession is highly elastic | untested belief | Verify or flag | **Challenge** | unverified — flagged (GT-14?): no elasticity measurement supplied; typical demand elasticities are 1–3 |
| Credit redemption reduces effective ARPU on retained members | current constraint | Expiry: only if the program is redesigned to non-monetary rewards | Accept | Definitional — account credit is a revenue offset |
| The program is reversible after one year | untested belief | Verify or flag | **Challenge** | unverified — flagged (GT-15?): withdrawing an accrued-points benefit is itself a churn event |

---

## 3. Ground Truths

- **GT-1** 48,000 members × $19/mo = $912,000/mo = $10,944,000/yr gross billings — source: user-stated figures + arithmetic.
- **GT-2** Monthly churn is 6.8%, up from 4.2% over ~6 months — a 2.6pp absolute, 62% relative increase — source: user-stated.
- **GT-3** The proposed program costs $310,000/yr as budgeted — source: user-stated.
- **GT-4** The rival's program launched ~1 month ago; the churn climb spans ~6 months — therefore the rival's launch post-dates roughly five-sixths of the observed deterioration — source: user-stated dates + calendar arithmetic.
- **GT-5** A decision is required within three weeks (board update) — source: user-stated.
- **GT-6** For a subscription with constant gross adds *G* and monthly churn *c*: equilibrium base = *G/c*, and LTV = ARPU/*c* — source: geometric series identity (mathematical, not empirical).
- **GT-7** $310,000 ÷ 48,000 members ÷ 12 months = **$0.538 per member per month = 2.83% of the $19 price** — source: arithmetic on GT-1 and GT-3.
- **GT-8** Detecting a 6.8% → 5.0% monthly churn difference at 80% power / 95% confidence over a 90-day window requires **≈950 members per arm** (cumulative churn 19.0% vs 14.3%) — source: two-proportion sample-size formula.
- **GT-9?** Contribution margin per subscription dollar — **unverified:** not supplied, and the analysis cannot be closed without it.
- **GT-10?** Whether the $310,000 includes redeemed credit liability — **unverified:** "cost to run" was not decomposed.
- **GT-11?** Gross adds ≈3,264/mo, base approximately flat — **unverified:** assumed for modelling; the base may be contracting.
- **GT-12?** The composition of the 2.6pp churn increase (involuntary vs voluntary; which cohorts, channels, plans) — **unverified:** no decomposition has been performed.
- **GT-13?** The program will deliver a 1.8pp churn improvement — **unverified:** a forecast, not a measurement.
- **GT-14?** Retention elasticity with respect to a small effective price concession — **unverified:** no benchmark supplied.
- **GT-15?** The program is withdrawable after year one without a churn penalty — **unverified.**

---

## 4. Derivation Chains

### Conclusion A: The break-even churn improvement is 0.52pp at 100% margin and the full 1.8pp at 30% margin — so the decision is determined by contribution margin, which nobody has stated

GT-1 (48,000 × $19, $10.944M/yr) + GT-3 ($310,000/yr) + GT-6 (base evolves as *Bₙ₊₁ = Bₙ(1−c) + G*)
→ *intermediate:* modelling year 1 with G = 3,264 (GT-11?), a churn drop to 5.0% yields **56,451 incremental member-months** ($1.073M gross); a drop to only 6.28% yields **15,005 incremental member-months** ($285k gross). Break-even therefore requires ~**0.52pp** improvement if every retained dollar were profit, ~**1.05pp** (churn → 5.75%) at 50% contribution margin, and ~**1.75pp** (churn → 5.05%) at 30% contribution margin.
→ *conclusion:* at 30% margin the program must deliver **essentially 100% of its own optimistic forecast just to break even in year one**, with zero room for error; at 50% margin it needs 58% of the forecast; at high margin it needs only 29%. The same $310,000 is an easy yes or a coin-flip depending entirely on a number that was not in the proposal.

**Confidence: MEDIUM.** GT-9? (margin) and GT-11? (gross adds) are unverified. Supplying the contribution margin per subscription dollar and the last six months of gross adds raises this to HIGH — both are one-query finance pulls, not studies.

*Second-order extension (non-contradicting, per §4 extension check):* redeemed credit reduces effective ARPU on **every** retained member, not just the marginal ones, which lowers the $19 numerator in the same break-even. If GT-10? resolves to "excludes redemption," a 3–5% redemption rate adds **$360k–$600k/yr** on the grown base, taking loaded cost to $670k–$910k against $1.073M of gross benefit — negative at any margin below ~65%. This modifies Conclusion A's threshold; it does not contradict GT-1, so no return to Phase 2 is triggered.

### Conclusion B: The mechanism is a 2.83% price concession being asked to produce a 26% relative churn reduction — an implied elasticity of ~9

GT-7 ($0.538/member/month = 2.83% of price) + GT-2 (6.8% → 5.0% is a 26% relative reduction)
→ *intermediate:* stripped of its framing, the program is a **2.83% effective discount distributed across the entire base**, ~93% of which each month goes to members who were never going to leave. For it to hit its target through a price-value mechanism, retention response would have to be roughly **9× the size of the price change**.
→ *conclusion:* the stated bet is not credible as economics. If a loyalty program moves churn, it moves it through habit formation, engagement, and switching cost — none of which a redeem-for-account-credit design is built to maximise, because credit redemption is the one reward structure that converts directly back into "your price is too high."

**Confidence: MEDIUM.** GT-14? (elasticity benchmark) is unverified; the implied-elasticity arithmetic is sound but the "typical elasticity is 1–3" comparator is a general prior, not a measurement on this product. A single past price or promotion test on this base would raise this to HIGH.

### Conclusion C: The rival's launch cannot be evidence for this spend

GT-2 (climb spans ~6 months) + GT-4 (rival launched ~1 month ago)
→ *intermediate:* the deterioration predates the rival's program by roughly five months, so the rival's program is causally excluded as an explanation for at least the first ~2.1pp of the 2.6pp climb.
→ *conclusion:* "they did it, so we should" is analogy, not evidence, and it is analogy to a company whose margin structure, churn baseline, and results are all unknown. Matching a competitor's loyalty spend is also the classic symmetric move: if both run it, both pay and neither gains share.

**Confidence: HIGH.** No unverified inputs — this rests on stated dates and arithmetic only.

### Conclusion D: Expected value is unbounded below until churn is decomposed

GT-2 (2.6pp climb, cause unidentified) + GT-12? (no decomposition performed)
→ *intermediate:* realised benefit = 1.8pp × (share of the churn increase that is *both* price-value-driven *and* reversible by a 2.83% credit). Involuntary churn from failed payments is immune to loyalty points and commonly runs 20–40% of gross churn; a cohort-quality shift from a new acquisition channel is immune; a product or onboarding regression is immune.
→ *conclusion:* the program's expected effect is the forecast multiplied by an unmeasured fraction between 0 and 1. If the climb is largely involuntary, dunning and card-updater fixes recover most of it at a small fraction of $310,000 — and would be the higher-return action by an order of magnitude.

**Confidence: LOW.** GT-12? is entirely unverified. A cohort/tenure/channel/payment-failure decomposition of the last six months — a few days of analyst work — raises this to HIGH and may change the recommended intervention outright.

### Conclusion E: The information needed to make this call costs under 25% of the call itself

GT-1 (48,000-member base) + GT-8 (≈950 members/arm for 90-day detection) + GT-5 (three-week deadline)
→ *intermediate:* a randomised holdout of ~3,000 treated / 3,000 control — 12.5% of the base, comfortably above the 950/arm power floor with margin for segment effects — costs roughly **$50,000–$70,000** (setup dominates; the credit itself is ~$4,000 over 90 days at the same per-member rate) and returns a causal, not correlational, churn delta.
→ *conclusion:* committing $310,000 now buys **no information** that $60,000 would not buy better, and forecloses the option to redesign the reward mechanism after seeing which lever actually moves. The three-week deadline is satisfied by presenting a pre-registered conditional commitment, which is a decision.

**Confidence: HIGH.** Rests on the base size, the power calculation, and the deadline — all verified.

### Conclusion F: This is a recurring, hard-to-reverse commitment, not a one-year experiment

GT-3 ($310k/yr) + GT-6 (LTV = ARPU/churn) + GT-15? (reversibility unverified)
→ *intermediate:* points accrue as a member-held balance and a balance-sheet liability; once members hold balances, withdrawing the program is itself a churn event, and the program permanently lowers the ARPU numerator in every future LTV and pricing calculation. It also trains price sensitivity into a base you may later need to raise prices on.
→ *conclusion:* the true commitment being voted on is not $310,000 — it is $310,000/year in perpetuity plus a constraint on future pricing. It should be underwritten to that standard, which makes the missing margin number and the missing diagnostic more serious, not less.

**Confidence: MEDIUM.** GT-15? unverified. Legal/finance confirmation of the points-liability treatment and a modelled sunset path would raise this to HIGH.

---

## 5. Abandoned Reasoning

### Dead End: LTV-uplift framing as the funding justification

**What was tried:** Per-member LTV rises from $19/0.068 = $279 to $19/0.05 = $380 — a $101 gain — which across ~39,000 annual gross adds implies $3.9M of created value against $310k of cost, a 12× return.

**Why abandoned:** It answers a different question. LTV is a discounted future-value figure applied largely to members not yet acquired; the board question is a one-year funding call. Substituting it for year-one cash inflates apparent ROI roughly fourfold ($3.9M vs the $1.07M gross of Conclusion A) and hides the margin dependency entirely. It also multiplies through GT-13?, treating the forecast as achieved.

**What it ruled out:** Saves the reader from concluding "the LTV math makes this obvious." It does not — the LTV math makes it obvious only if you already grant the churn improvement, which is the thing in question.

### Dead End: Competitive-parity as a decision rule

**What was tried:** Treating the rival's launch as market evidence that loyalty programs work in this category.

**Why abandoned:** Fails on GT-4 timing (the rival post-dates the climb) and rests on zero verified ground truths about the rival's economics or results. The rival launched one month ago and therefore has no results to reason from.

**What it ruled out:** Saves re-litigating "we'll look slow." Speed matters for the decision, not for the spend.

### Dead End: Sizing the program against the rival's spend

**What was tried:** Benchmarking $310,000 as reasonable-or-not by comparison to what a competitor appears to be spending.

**Why abandoned:** No verified ground truth exists about the rival's cost base, and the correct sizing anchor is our own break-even (Conclusion A), which is derivable from facts we hold.

**What it ruled out:** Rules out any "is $310k a normal number?" line of inquiry — normality is irrelevant; break-even is the test.

### Dead End: Treating the 6.8% as a single number to be moved

**What was tried:** Modelling one blended churn rate and one blended intervention.

**Why abandoned:** Churn is a mixture of mechanisms with different reversibility and different costs to fix. A blended rate cannot be acted on, only reported on. This dead end is what produced Conclusion D.

**What it ruled out:** Rules out any single-lever plan — including a cheaper single lever — as a defensible response before decomposition.

---

## 6. Conclusion

**Recommended approach: No — do not fund the loyalty program at $310,000 in three weeks.** Instead, bring the board a three-part conditional decision, all of which fits inside the deadline:

1. **Decompose the churn increase (week 1, ~$0).** Split the 4.2% → 6.8% move by involuntary/payment-failure vs voluntary, by tenure cohort, by acquisition channel, and by plan. If a material share is involuntary, fix dunning and card-updating first — that is a low-thousands intervention against a lever loyalty points cannot touch.
2. **Get the two missing numbers (week 1, ~$0).** Contribution margin per subscription dollar (GT-9?), and whether the $310,000 includes redeemed credit liability (GT-10?). These two figures alone move the break-even from "needs 0.52pp" to "needs the entire forecast," and the second can nearly double the true cost.
3. **Fund a powered pilot, not a launch (weeks 2–14, ~$50–70k).** Randomised holdout, ~3,000 treated / 3,000 control, 90 days, with the success threshold **pre-registered before results** at the margin-adjusted break-even from step 2. Ask the board for conditional approval of the full $310,000, releasable only on hitting that pre-registered threshold.

**Key insight:** Stripped of its framing, the program is a **2.83% price cut sprayed across the entire base** — $0.54 per member per month — being asked to produce a **26% relative churn reduction**, an implied retention elasticity of about 9 against typical demand elasticities of 1–3. Roughly 93% of the spend each month lands on members who were never going to leave. Reasoning by analogy — the rival launched one, so parity is prudent — would have skipped both the elasticity check and the timing check that shows the rival's launch post-dates five-sixths of the churn climb and therefore cannot be its cause.

**Trade-offs acknowledged:** The board gets a decision in three weeks but not an answer; the answer arrives at roughly day 90. If the churn cause is genuinely price-value and genuinely urgent, a quarter of delay costs approximately 2,600 member-months of the benefit — about $49,000 gross at list price, well under the $240,000 of avoided commitment and materially under the downside if the program lands closer to 0.5pp than 1.8pp. Customer success will experience this as being told no; the mitigation is that they get a funded, properly powered test with a threshold they help set, rather than a program they will be held to for a forecast they were never in a position to verify.

**Confidence: MEDIUM.** The downgrade is caused by **GT-9?** (contribution margin — unstated, and it alone moves break-even from 0.52pp to 1.75pp), **GT-10?** (redemption liability inside or outside the $310k — potentially a near-doubling of true cost), and **GT-12?** (undiagnosed churn composition — which determines whether this lever addresses the actual cause at all). Supplying the margin figure and a six-month cohort/involuntary-churn decomposition — days of work, not weeks — raises the funding recommendation to HIGH in either direction. **GT-13?** (the 1.8pp effect itself) can only be raised to HIGH by the randomised holdout in step 3, which is precisely why step 3 exists.

---

## Validation Pass (rubric applied before presenting)

**Assumption audit scan**

| Chain | Step | Step text (brief) | Assumption surfaced? | Added to Table? |
|---|---|---|---|---|
| A (break-even) | 1 | Model *Bₙ₊₁ = Bₙ(1−c) + G* with G = 3,264 | Gross adds constant, base at equilibrium | yes (GT-11?) |
| A | 2 | Convert member-months to profit at margin *m* | Contribution margin exists and is uniform across cohorts | yes (GT-9?) |
| A (2nd-order) | 3 | Redemption adds $360–600k | $310k excludes redeemed credit | yes (GT-10?) |
| B (elasticity) | 1 | $0.538/mo = 2.83% of price | Credit is spread evenly, not concentrated on at-risk members | yes (row: "single behaviour addressable by one lever", Discard) |
| B | 2 | Implied elasticity ≈9 is implausible | Typical elasticity is 1–3 | yes (GT-14?) |
| C (rival timing) | 1 | Climb predates rival launch by ~5 months | none — stated dates | n/a |
| D (decomposition) | 1 | Benefit = 1.8pp × reversible share | Churn is a mixture, not a single mechanism | yes (Discard row) |
| D | 2 | Involuntary churn is commonly 20–40% | Category prior, not measured here | yes (GT-12?) |
| E (pilot) | 1 | 950/arm at 90 days | Test and control populations are exchangeable; no cross-contamination | yes (GT-12? cohort mixture covers segment heterogeneity) |
| E | 2 | Pilot costs $50–70k | Setup cost dominates credit cost at pilot scale | yes (GT-10? scope of program cost) |
| F (irreversibility) | 1 | Points accrue as a member-held liability | Program is not costlessly withdrawable | yes (GT-15?) |

**Criterion 1: Identify Essence** — Quoted span: *"Is $310,000/year of recurring spend … the highest-return way to reverse a 2.6-percentage-point monthly churn increase whose cause has not been diagnosed — and is a three-week deadline a reason to commit rather than a reason to buy information?"* Band: **Rigorous.** Names the underlying allocation-and-diagnosis question rather than the triggering event (the rival's launch) or the prompt's surface form; each of the four success criteria is a scannable pass/fail test against section 6.

**Criterion 2: Challenge Assumptions** — Quoted span: *"'The rival launched one; we need parity' | convention | Explicitly challenge before use | **Discard**"* Band: **Rigorous.** Every row carries one of the four types, treatment vocabulary matches the type, three rows reach Discard and five reach Challenge (challenge is not merely labelled), and every unverified row used downstream reads "unverified — flagged" with its GT-N? handle.

**Criterion 3: Establish Ground Truths** — Quoted span: *"**GT-7** $310,000 ÷ 48,000 members ÷ 12 months = $0.538 per member per month = 2.83% of the $19 price"* Band: **Rigorous.** All 15 entries carry stable IDs and either a source or a specific unverified reason; the seven `?`-suffixed entries are exactly the untested beliefs from section 2; GT-6 and GT-8 bottom out at mathematical identities rather than borrowed benchmarks.

**Criterion 4: Reason Upward** — Quoted span: *"GT-7 … + GT-2 … → the program is a **2.83% effective discount distributed across the entire base** … → the stated bet is not credible as economics."* Band: **Rigorous.** All six chains carry at least one genuine intermediate that neither input yields alone; every `GT-N?`-bearing chain terminates in MEDIUM or LOW with the named input and the specific verification that would lift it; the second-order pass ran and its one material extension (redemption lowering the ARPU numerator) modifies rather than contradicts GT-1, so no Phase 2 return was triggered.

**Criterion 5: Validate** — Quoted span: *"**Confidence: MEDIUM.** The downgrade is caused by **GT-9?** … **GT-10?** … and **GT-12?**"* Band: **Sound.** Each conclusion traces to named ground truths and the load-bearing weak links are flagged with the verification that resolves them; short of Rigorous because GT-14? (the 1–3 elasticity comparator underpinning Conclusion B's force) is a general prior that could not be verified against this product's own price history within the analysis.

**Criterion 6: Whole-document coherence** — Quoted span: *"Instead, bring the board a three-part conditional decision, all of which fits inside the deadline"* Band: **Rigorous.** The Conclusion introduces no claim absent from sections 3–4, satisfies all four success criteria from section 1 (break-even in pp; named flipping unknown with its measurement; a three-week decision that is not a yes/no on $310k; no reliance on the rival), and the four abandoned paths are each named with a specific falsifying reason rather than a time excuse.

**Gate:** no criterion Absent; one criterion at Sound, zero at Hand-wavy. **Rubric cleared.**