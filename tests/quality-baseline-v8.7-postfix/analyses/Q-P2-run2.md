# First-Principles Analysis: Funding the Loyalty Program

**Step 0 — technique selection:** No focused-technique trigger phrase fires ("should we fund… at that price" is a decision question, not a literal "trade-off analysis" / "pre-mortem" / etc. request). `MODE = full-composer`. All phases run; Phase 4 uses the inlined trade-off and second-order procedures where the structure calls for them.

---

## 1. Problem Essence

**Core question:** Is a points-for-credit loyalty program the *right lever*, at an *acceptable ROI and risk*, to arrest a churn increase whose *cause is currently undiagnosed* — and can that be committed within a 3-week board deadline?

The triggering framing ("fund at $310K betting on 5% churn") is **not** the essence. It smuggles in an unverified causal claim (that this program moves churn) and a specific target (5.0%) as if they were the decision. The real decision is: *given an undiagnosed 4.2% → 6.8% churn rise, is spending $310K/yr on this particular intervention justified?*

**Success criteria for a correct answer:**
- States whether expected benefit exceeds $310K/yr and under what condition.
- Names the load-bearing assumption and its confidence.
- Separates "is the ROI good if it works" from "will it work."
- Fits a decision that can be made in 3 weeks.

---

## 2. Assumptions Table

| Assumption | Type | Treatment | Verdict | Verification |
|---|---|---|---|---|
| Program *causes* churn to fall toward 5% | untested belief | Challenge — this is the whole thesis | **UNVERIFIED — flagged** (GT-8?) | No cited pilot/test; loyalty points address price/engagement, not diagnosed cause |
| The 4.2→6.8 rise has a cause loyalty points can touch | untested belief | Challenge | **UNVERIFIED** | Root cause never stated; could be product, service, pricing, or the rival |
| $310K "to run" includes redemption liability (credit given back) | untested belief | Challenge before use | **UNVERIFIED — ambiguous** | "Costing ~$310K to run" does not clarify if redeemed credit is in or out |
| Member base stays ~48,000 during the year | current constraint | Record expiry | Accept for year-1 model | Holds only if gross adds ≈ churn; base is already eroding |
| Rival's launch is driving our churn | untested belief | Challenge | **UNVERIFIED** | Timing is suggestive, not causal; could be coincident |
| Gross margin on $19 revenue is high (SaaS-typical 70%+) | untested belief | Verify or bound | **ASSUMED — bounded** (GT-7?) | Not given; used only as a range 50–90% |
| 3-week deadline is a hard commit-or-lose gate | convention | Challenge | **Partly false** | Deadline is for a *board update*, not an irreversible spend; a pilot decision fits it |
| Arithmetic on base/price/churn | physical-law-equivalent (definitional) | Accept | VERIFIED | See Ground Truths |

**Assumption Audit (Phase 4 scan — every chain step checked for undeclared assumptions):**

| Chain | Step | Step text (brief) | Assumption surfaced? | Added to table? |
|---|---|---|---|---|
| C1 | 1 | Member-months delta from churn drop | Base stable ~48k | Already row 4 |
| C1 | 2 | Delta × $19 = gross benefit | Price constant $19 | New → added below |
| C1 | 3 | Apply margin → net | Margin 70% | Already row 6 |
| C2 | 1 | Points don't address undiagnosed cause | Cause is not price/engagement | Already rows 1–2 |
| C3 | 1 | Break-even churn movement ≈0.7–1.0pp | Year-1, existing-base-only (conservative) | New → added below |
| C3 | 2 | Low bar → wide safety margin | Benefit scales ~linearly near 6.8% | New → added below |

Added rows: **[Assumes: price held at $19 for retained members]** (undercut if redeemed credit lowers effective price); **[Assumes: benefit computed on existing base only — real benefit higher because new adds also retained]** (this makes break-even *conservative*, i.e. safe); **[Assumes: churn-value roughly linear in the 5–7% band]** (true for small moves).

---

## 3. Ground Truths

- **GT-1:** 48,000 × $19 = **$912,000/month** gross revenue (~$10.94M/yr). *(arithmetic)*
- **GT-2:** Monthly churn = 6.8%, up from 4.2% over two quarters. *(given)*
- **GT-3:** At 6.8% → ~3,264 members lost/month; at 5.0% → ~2,400/month; **~864 members/month retained** by a 1.8pp reduction. *(GT-1, GT-2, arithmetic)*
- **GT-4:** Mean tenure = 1/churn: **14.7 months at 6.8% vs 20.0 months at 5.0%** → LTV $279 vs $380 per member. *(definition of geometric mean lifetime)*
- **GT-5:** Program cost = **$310,000/yr**; annual revenue ~$10.94M → cost is **~2.8% of revenue**. *(given, GT-1)*
- **GT-6:** Rival launched a similar program last month. *(given)*
- **GT-7?:** Gross margin unverified; bounded **50–90%**. *(flagged)*
- **GT-8?:** Program's causal effect on churn is **unverified**. *(flagged — load-bearing)*
- **GT-9:** Cohort retention over 12 months (existing base, equal gross adds in both scenarios): summed survivor-months = **7.82 × 48k = 375,300** at 6.8% vs **8.73 × 48k = 419,200** at 5.0% → **Δ ≈ 43,900 member-months**. *(geometric-decay sum, arithmetic — see Chain 1)*

---

## 4. Derivation Chains

**Chain C1 — ROI *if the program works* (moves churn 6.8%→5.0%):**
GT-9 + GT-1 → Δ43,900 member-months × $19 = **~$834K incremental gross revenue in year 1** (existing base only; new adds would add more) → at 70% margin ≈ **$584K net** → **[Assumes: price held $19; margin 70%; existing-base-only ⇒ conservative]** → **$584K net benefit ≫ $310K cost.** ROI positive with room to spare. **Confidence: HIGH** *for the arithmetic*, but the whole chain is gated by GT-8?.

**Chain C3 — break-even efficacy (the reframe — the decision-relevant chain):**
C1 shows 1.8pp of churn reduction ≈ $834K gross / ~$463K per 1.0pp gross. Setting benefit = $310K:
- Gross break-even ≈ **0.67pp** (churn only needs to fall 6.8% → ~6.1%).
- At 70% margin, break-even ≈ **0.96pp** (churn → ~5.85%).
→ **[Assumes: near-linearity in the 5–7% band; existing-base-only ⇒ true bar is lower]** → **The program does not need to hit 5%. It needs to move churn ~0.7–1.0pp to pay for itself.** **Confidence: HIGH.** This is the strongest result in the analysis: the downside is bounded and the break-even bar is low.

**Chain C2 — efficacy is unproven and possibly mis-targeted:**
GT-2 (undiagnosed rise) + GT-8? → points redeemable for credit reward *engagement and price-sensitivity*, not *product/service defects or competitive gaps* → if the 2.6pp rise is driven by a product/service problem, the program moves churn ≈ 0pp and $310K is spent with no return → **the causal link is the single point of failure.** **Confidence that the link holds: LOW/MEDIUM** (no test cited).

**Second-order extension (applied to C1/C2 before Phase 5):**
1. *Redemption liability:* if $310K excludes redeemed credit, true cost rises and effective price per retained member falls below $19 — erodes C1's benefit. (Does not contradict a GT; flags a cost-understatement.)
2. *Expectation lock-in:* rewards are hard to withdraw once launched; a failed program isn't cleanly reversible. (Adverse.)
3. *Masking effect:* funding the program may substitute for diagnosing the 4.2→6.8 root cause, letting a deteriorating product keep bleeding. (Adverse — the highest-signal second-order risk.)
4. *Competitive parity:* rival's launch (GT-6) may make a loyalty program **table stakes** — absence becomes a churn driver even if presence isn't a strong retainer. (Favourable to funding.)

No extension contradicts a Ground Truth → no return to Phase 2.

---

## 5. Abandoned Reasoning

- **LTV-multiple framing** (GT-4, $279→$380) was set aside as the headline metric: it overstates year-1 cash because it credits full future lifetime immediately. The 12-month member-months model (GT-9) is the honest year-1 figure.
- **"Trust the 5% target and compute ROI at 5%"** was abandoned as the decision frame — it embeds the unverified GT-8? as if verified. Chain C3 (break-even) replaces it because it survives even if 5% is never reached.
- **Treating the 3-week deadline as commit-or-lose** was dropped: the deadline gates a *board update*, and a time-boxed pilot decision fits it, so the deadline does not force an all-or-nothing annual commit.

---

## 6. Conclusion

**§6 → §4 closure ledger:**
- "ROI is strongly positive *if* it works" → chain **C1** ✓
- "It only needs to move churn ~0.7–1.0pp to break even" → chain **C3** ✓
- "Efficacy is unproven and may be mis-targeted at an undiagnosed cause" → chain **C2** ✓
- "Downside is bounded (~2.8% of revenue) and parity may be table stakes" → **C3 + second-order 4 / GT-5** ✓

**Recommendation: Qualified YES — fund it, but not on the terms as framed.**

The economics are asymmetric in your favour. The break-even bar (Chain C3) is a churn movement of only **~0.7–1.0 percentage points**, not the full 1.8pp to 5.0%. Because the true bar is even lower than that (C3 is computed on the existing base only), and the maximum downside is bounded at ~$310K (~2.8% of annual revenue), this is a bet with a wide margin of safety on the *cost* side. Competitive parity (rival already launched) makes the program closer to table stakes than to a differentiator. **Confidence: MEDIUM**, gated entirely by GT-8? (the causal link).

**But do not fund it as an open-ended annual commit betting on 5%.** Three conditions, all cheap and all fit the 3-week window:

1. **Reframe the bet from "hits 5%" to "moves churn ≥ ~1pp."** Present it to the board on the break-even math (C3), not the aspirational 5% (which the analysis cannot support).
2. **Structure as a time-boxed pilot with a kill criterion.** Roll out to a segment (or for one quarter) with a pre-registered kill metric: if churn in the treated group doesn't move ≥ ~0.7–1.0pp vs control, stop. This converts an unverified belief (GT-8?) into a measured one and caps the downside.
3. **Run root-cause diagnosis in parallel — this is non-negotiable.** The weakest link (Chain C2, second-order effect 3) is that points may be aimed at the wrong problem. A 4.2→6.8 rise has a cause; if it's product/service/pricing, the loyalty program will move churn ≈0. Fund a fast diagnostic (exit surveys, cohort analysis, rival-switch tracking) *before or alongside* launch.
4. **Before signing, get one number:** does the $310K include the redemption liability (credit actually paid out), or only operating cost? If it excludes redemptions, re-run C1 with the true cost — the ROI cushion narrows.

**Weakest link, explicitly flagged:** the entire positive case rests on GT-8? (unverified causal efficacy). The pilot-with-kill-criterion is precisely what verifies it while keeping the loss bounded. Do that, and a MEDIUM-confidence recommendation becomes a HIGH-confidence one within a quarter.

---

*Validation pass: every §6 claim traces to a named chain (ledger clean); the load-bearing unverified assumption (GT-8?) is flagged and its resolution is built into the recommendation; the second-order masking risk is surfaced rather than buried; no analogy (the rival's program) is used as evidence — it enters only as GT-6 with a stated, unverified causal status.*