## Answer

**Recommendation:** Run a 2-4 week, near-zero-cost diagnostic sprint — pulling raw renewal-cohort counts, signup-vintage tags, and churned-account reason codes — before committing budget to any fix, and fund only the driver(s) the diagnostics confirm (chain C1, C8).

**Band (from §6):** MEDIUM

**Would change it:** A same-day confirmation that Northbrook can actually retrieve cohort, reason-code, and ticket-normalization data within 2-4 weeks; if that data is unavailable or slower than assumed, the diagnose-first recommendation weakens and the trade-off in chain C8 would need to be re-run with a longer diagnostic-cost estimate.
## 1. Problem Essence

**Essence Statement:** Northbrook's quarterly renewal non-renewal rate has risen sharply between two observed quarters (4.1% → 9.2%), and leadership wants the true upstream driver(s) isolated and fixed — but no data yet distinguishes genuine broad-based deterioration from a cohort-specific artifact, a measurement/seasonality artifact, or a combination of several partial causes, so the real question is not "which of the six named hypotheses is correct" but "what is the cheapest, fastest way to determine which of them — alone or in combination — is actually operating, before resources are committed to a fix."

**Success criteria — a correct answer must:**
1. Distinguish what can be concluded from the given facts alone versus what requires further diagnostic data, with no step skipped silently.
2. State an explicit confidence level for every causal claim, naming the cheapest diagnostic that would confirm or disconfirm it.
3. Not treat rising ticket volume and falling adoption scores as self-evidently *causes* of churn without testing whether they are symptoms of a shared upstream driver.
4. Test whether the Q1→Q3 "doubling" reflects genuine broad-based deterioration versus a cohort-specific shock, a seasonal/fiscal-cycle effect, or small-sample statistical noise, before accepting that something is systemically wrong across the whole customer base.
5. Produce a prioritized, cost/speed-ranked diagnostic action plan, plus the shape of candidate fixes conditional on diagnostic outcomes.
6. Explicitly flag and disposition the risk that leadership commits to a symptom-level fix (discounting, CS headcount) before a driver is confirmed.
7. Not require the answer to be exactly one of the six named hypotheses — a combination, "insufficient evidence yet, run diagnostics first," or a reframing of the measurement itself are all admissible answers.

No success criterion above requires selecting exactly one of the six named candidate hypotheses; each has been checked against that floor.

## 2. Assumptions Table

| # | Assumption | Type | Treatment | Verdict | Verification |
|---|---|---|---|---|---|
| 1 | Churn is a single, uniform phenomenon across the customer base | untested belief | Verify via cohort/segment breakdown of churned accounts | Challenge — likely false/oversimplified; CS's two distinct flags (tickets, adoption) and the six non-exclusive hypotheses already suggest at least two mechanisms could be operating at once | unverified — flagged; requires churned-account segmentation data not supplied |
| 2 | A "quarterly churn rate" is a valid apples-to-apples trend measure for an annual-contract business, the way it would be for a monthly-churn business | convention | Explicitly challenged (see GT-8) | Challenge — does not transfer cleanly; each quarter's denominator is a different renewal cohort (different signup vintage), so Q1 vs Q3 compares two different sub-populations, not two measurements of one stable population | Holds only if cohort size/vintage composition is similar quarter to quarter — unverified |
| 3 | Rising ticket volume and falling adoption scores are *causes* of churn | untested belief | Verify direction of causality — leading indicators of a shared upstream driver, or independent causes? | Challenge — treated as correlated leading indicators, not confirmed causes, pending data | unverified — flagged; requires ticket-category tagging + adoption sub-component breakdown (see C2) |
| 4 | The Q1→Q3 increase reflects a general, continuing deterioration rather than a one-off cohort or seasonal artifact | untested belief | Test against cohort vintage, fiscal-calendar seasonality, and sample-size/noise explanations before accepting | Challenge — cannot be confirmed from the two given percentages alone; gates which hypothesis branch is even worth pursuing | unverified — flagged; highest-priority item to resolve first (see C1, C4, C5) |
| 5 | The renewal-cohort size (N) each quarter is large enough that 4.1%→9.2% reflects a real rate shift rather than small-N noise | untested belief (current constraint if N is in fact small) | Obtain raw counts (# up for renewal, # churned, per quarter) | Challenge — unverified; this is the cheapest, fastest diagnostic available | unverified — flagged; expires the moment raw counts are supplied (see C5) |
| 6 | No fiscal-calendar / budget-cycle seasonality affects which customers are up for renewal in Q3 vs Q1 | convention / untested belief | Check whether the Q3 cohort disproportionately includes customers whose budget cycles create elevated non-renewal risk in that period | Challenge — unverified | unverified — flagged; requires renewal-date distribution and customer fiscal-year data (not supplied) |
| 7 | A fix exists entirely within Northbrook's control that can return churn to Q1 levels or better | convention (implicit in the "find it and fix it" mandate) | Challenge via theoretical-limit reasoning — some mid-market B2B SaaS churn (M&A, budget elimination, strategic consolidation) is structurally outside product/CS control | Challenge — partially false; a nonzero "irreducible" fraction almost certainly exists and must be separated from the fixable fraction before setting a target (see C7) | unverified — flagged; requires Northbrook's own historical non-renewal reason codes, segmented by "controllable" vs "structural" cause |
| 8 | Renewal-reason codes, win/loss notes, and pricing-change history are not needed because CS's qualitative flags are enough | untested belief / framing gap (surfaced by omission in the mandate) | Surface these as required, cheap, already-available data sources | Discard — this implicit assumption does not survive challenge; these are the cheapest and most directly diagnostic inputs available and are currently unused | Pull immediately — see Conclusion, diagnostic step 3 |
| A-1 | Rising tickets and falling adoption share one upstream driver rather than being two independent problems | untested belief | Surfaced from chain C2; verify via ticket-category tagging + adoption sub-component trend | Challenge — plausible but not confirmed | unverified — flagged; see C2 |
| A-2 | Customer count/ARR grew during this period without proportional CS headcount growth | untested belief | Surfaced from chain C3; pull headcount-vs-customer-count ratio history | Challenge — unverified, cheap and immediate to check | unverified — flagged; see C3 |
| A-3 | The Q3-renewal cohort experienced a distinct negative event at/near signup (~12 months prior) that the Q1 cohort did not | untested belief | Surfaced from chain C4; tag churned accounts by signup vintage | Challenge — unverified | unverified — flagged; see C4 |
| A-4 | Renewal-cohort N is small enough that a handful of churns swings the rate by several points | untested belief | Surfaced from chain C5; pull raw counts | Challenge — unverified | unverified — flagged; see C5 |
| A-5 | Q3's rate, if sustained across four quarters, approximates a new steady-state annualized churn probability | untested belief (explicitly scenario, not forecast) | Surfaced from chain C6; gated by resolving A-3/A-4 first | Challenge — unverified / scenario-only | unverified — flagged; see C6 |
| A-6 | A nonzero churn floor exists in this category that is structurally outside Northbrook's control | current constraint (industry-structural) | Surfaced from chain C7; check Northbrook's own historical reason-code mix for "structural" vs "dissatisfaction" causes | Challenge — plausible, directionally supported by common B2B SaaS market structure, but not independently verified here; expires once Northbrook's own historical reason-code mix is pulled and a structural-fraction figure is confirmed | unverified — flagged; see C7 |
| A-7 | A diagnose-first composite (pulling cohort/reason-code/ticket-normalization data) is achievable within 2-4 weeks at low cost | untested belief (operational) | Surfaced from chain C8; confirm with a same-day internal check of data availability | Challenge — unverified but low-risk to confirm | unverified — flagged; see C8 |
## 3. Ground Truths

Source note on provenance: GT-1 through GT-7 are facts stipulated directly in the task's problem statement — this analysis has read them at source (the prompt text itself is the source for this hypothetical) and they carry no `?`. GT-8 is a mechanical/definitional truth about annual-contract renewal structure, derived by definition rather than cited externally. GT-9 is an unverified external industry convention with no source opened in this exercise and is flagged accordingly. No customer count, ARR total, ticket-category breakdown, adoption-score magnitude, renewal-reason-code distribution, pricing-change history, or competitor identity was supplied — none of these is fabricated anywhere in this analysis; where such detail would normally appear, it is instead named as an open diagnostic question.

1. **GT-1** — Q1 quarterly churn rate = 4.1%. [Source: task problem statement, "THE SITUATION" section — read at source directly in the prompt text.]
2. **GT-2** — Q3 quarterly churn rate = 9.2% ("more than doubled within two quarters"). [Source: task problem statement — read at source.]
3. **GT-3** — Contracts are annual, ACV range $18,000–$40,000. [Source: task context paragraph — read at source.]
4. **GT-4** — Churn is observed/measured at renewal events (annual cadence); it can be diagnosed continuously via leading indicators but is only *realized* as a churn event once per customer per year. [Source: task context paragraph — read at source.]
5. **GT-5** — Customer Success has qualitatively flagged rising support-ticket volume. No magnitude, baseline, or category breakdown is given. [Source: task "THE SITUATION" section — read at source; qualitative only.]
6. **GT-6** — Customer Success has qualitatively flagged a drop in feature-adoption scores. No magnitude or segment breakdown is given. [Source: task "THE SITUATION" section — read at source; qualitative only.]
7. **GT-7** — No root cause has yet been identified or confirmed; six non-mutually-exclusive candidate hypotheses are explicitly in play (offer/product gaps, pricing pressure, onboarding failure, service/support quality degradation, competitive displacement, or combinations). [Source: task "THE SITUATION" section — read at source.]
8. **GT-8** — For an annual-contract business, a period churn rate (e.g., "Q1 churn," "Q3 churn") is necessarily computed over the subset of customers whose contracts are up for renewal *in that specific period* — not over the full customer base — so a quarter-over-quarter comparison compares two different renewal cohorts (different signup vintages, potentially different sizes and composition), not two repeated samples of one stable population. [Source: definitional/mechanical consequence of GT-3 + GT-4 combined with the standard definition of a period churn rate; derived by definition, not externally cited — no `?` needed for a definitional truth, but its *application* to this specific case (i.e., whether cohort composition actually differs enough to matter) remains unverified, which is why it feeds untested-belief items A-2 through A-5 rather than settling them.]
9. **GT-9?** — Industry-typical "healthy" annual logo churn for mid-market B2B SaaS is commonly cited in the high-single-digit to low-double-digit percent range, with category-level attrition (tool consolidation, M&A, budget elimination) contributing a nonzero floor regardless of vendor execution quality. **Unverified.** [Phase 3 failure record: no source was opened for this figure — it is a general industry convention recalled from training knowledge, not independently verified or cited in this exercise, and used only directionally in C7 to bound expectations, never as a precise benchmark. Flagged `?` by design rather than presented as fact, per the task's explicit instruction not to fabricate data as if real.]

**`?`-marked:** GT-9 (1 of 9).

**Read-at-source locations:** GT-1 through GT-7 — the task's "THE SITUATION" and introductory context paragraphs (the prompt text itself, read directly). GT-8 — derived by definition from GT-3 and GT-4; no external read applies. GT-9 — not read at any source; see its Phase 3 failure record above.

**What is explicitly NOT a ground truth here (and is not fabricated anywhere below):** total customer count, total ARR, raw renewal-cohort counts (N) per quarter, ticket volume magnitude or category mix, adoption-score magnitude or sub-component breakdown, renewal-reason-code distribution, win/loss notes, pricing-change history, competitor identities, CS headcount history, and Q2's churn rate. Every one of these is treated below as an open diagnostic question, never as an assumed fact.

## 4. Derivation Chains

### C1 — The headline comparison is cohort-structural, not a repeated measurement

```text
GT-1 (Q1=4.1%) + GT-2 (Q3=9.2%) + GT-8 (quarterly rate = cohort-specific, not repeated-sample)
→ the headline "churn more than doubled" compares two different renewal-cohort populations (the Q1-anniversary customers and the Q3-anniversary customers), not the same population measured twice
→ the raw percentage jump is therefore consistent with at least three structurally different explanations: broad-based deterioration, a cohort-specific shock, or small-sample noise
→ broad deterioration would affect all cohorts; a cohort-specific shock would concentrate only in the Q3-renewal vintage; noise would require no real change in the underlying per-customer churn probability
→ the trend as stated therefore cannot be used to pick a root cause without first decomposing it by cohort, size, and reason code
→ the first diagnostic priority is accordingly not "which of the six hypotheses" but "is this a broad trend, a cohort artifact, or noise"
```
**Pre-check:** head: GT-1, GT-2, GT-8 (no chains cited) · ?-marked: none · lowest cited: none · Inputs ceiling: HIGH
**Confidence:** HIGH. Inputs are clean (no `?`, no cited chains). Inference follows deductively from the definition of a period churn rate for annual contracts (GT-8) — no unverified premise is required to state that multiple explanations remain possible. Rivals: a competing reading ("the two-quarter comparison is already valid as-is because cohorts are evenly sized and distributed") is not seriously live — nothing in the given facts supports it, and no cohort data exists yet to support it either, so it cannot be asserted with any more confidence than the alternatives this chain opens up.

### C2 — Tickets and adoption likely share one upstream driver, not two independent causes

```text
GT-5 (rising tickets) + GT-6 (falling adoption)
→ [Assumes: A-1] both signals are consistent with being downstream symptoms of one shared upstream shift rather than two independent root causes
→ two plausible shared upstream shifts are a product change that made the platform harder to use, or CS capacity falling behind customer-base growth
→ treating "service/support quality degradation" and "onboarding failure" as two separate boxes on leadership's list likely understates how tightly coupled the two CS-flagged signals are
→ the two signals more plausibly point toward one upstream capacity/quality shift than confirm two distinct, independent causes
```
**Pre-check:** head: GT-5, GT-6 (no chains cited) · ?-marked: none · lowest cited: none · Inputs ceiling: HIGH
**Confidence:** LOW. Inputs are clean, but Inference rests on A-1 (unverified — tickets and adoption could equally be two unrelated problems, e.g., a buggy release causing tickets and a separate sales-motion failure causing low adoption). Rivals: that independent-causes rival is live and not ruled out by the given facts. Two axes short. Would be lifted by ticket-category tagging plus an adoption sub-component breakdown showing whether the same accounts/timeframes drive both signals.

### C3 — CS-capacity-scaling is a specific, falsifiable version of the shared-driver hypothesis

```text
GT-5 + GT-6 + C2 (shared upstream driver likely)
→ [Assumes: A-2] a common structural cause of simultaneous ticket-volume increase and adoption-score decline is CS capacity failing to scale with the customer base
→ capacity failing to scale produces slower response times, visible as a higher ticket backlog, and less proactive onboarding and training time, visible as lower adoption
→ if true, this predicts a falsifiable signature: ticket volume per customer rising and resolution time lengthening, not just absolute ticket counts rising
→ it also predicts adoption scores falling disproportionately among customers served during the capacity-constrained window
→ the Q3-renewal cohort, having lived through that window right before its renewal decision, should then churn more than the Q1 cohort
→ "service/support degradation driven by capacity not scaling with growth" is a plausible, specific, and cheaply testable root-cause candidate
→ it is not yet confirmed — it rests entirely on A-2, which Northbrook can check at near-zero cost from its own headcount and customer-count history
```
**Pre-check:** head: GT-5, GT-6, C2 (LOW) · ?-marked: none · lowest cited: LOW · Inputs ceiling: LOW
**Confidence:** LOW (mechanically capped by citing C2). Weakest link: A-2 (CS headcount-to-customer ratio trend), entirely unverified but resolvable same-day from internal data.

### C4 — A cohort-specific shock (onboarding or pricing) at signup is an equally live, self-limiting alternative

```text
GT-1 + GT-2 + GT-8 (cohort-structure fact) + GT-3 (contract-value range, for segment framing)
→ [Assumes: A-3] the Q3-renewal cohort experienced a distinct negative event at or near signup roughly 12 months prior that the Q1-renewal cohort did not experience
→ candidate signup-time events include a specific onboarding-team change, a product-onboarding-flow defect window, or a pricing/packaging change rolled out starting mid-year
→ this hypothesis is self-limiting and sharply falsifiable: if true, elevated churn should track with that specific vintage and then subside in Q4 and beyond as the vintage ages out of the renewal population
→ if the true cause were ongoing systemic deterioration instead, elevated churn should persist or worsen across newer cohorts too, not just the Q3 vintage
→ distinguishing "cohort-specific one-off" from "ongoing systemic deterioration" is the single highest-value diagnostic fork in this analysis, because the correct action differs completely
→ resolving that fork requires only renewal-reason codes and signup-date tagging of churned accounts — data Northbrook almost certainly already holds
```
**Pre-check:** head: GT-1, GT-2, GT-8 (no chains cited) · ?-marked: none · lowest cited: none · Inputs ceiling: HIGH
**Confidence:** LOW. Inputs are clean, but Inference rests on A-3 (unverified) and Rivals is explicitly and seriously live — the "broad systemic deterioration" reading from C1 is an undecided competing explanation of the same two data points, by design. Two axes short. Resolves via a cohort/signup-date pull on churned accounts (cheap, internal).

### C5 — Statistical noise from a small renewal-cohort denominator is an equally live alternative

```text
GT-1 + GT-2
→ [Assumes: A-4] a jump from 4.1% to 9.2% could be produced by as few as a handful of additional non-renewals
→ this is plausible if the renewal-cohort denominator each quarter is modest, as could be expected for an $18k-$40k ACV mid-market vendor
→ under that assumption the underlying per-customer churn probability would not need to have changed at all
→ this is immediately and cheaply falsifiable: Northbrook already has the raw counts behind both percentages
→ recomputing the two rates' confidence intervals, even informally, shows whether 4.1% and 9.2% are statistically distinguishable at the cohort sizes actually involved
```
**Pre-check:** head: GT-1, GT-2 (no chains cited) · ?-marked: none · lowest cited: none · Inputs ceiling: HIGH
**Confidence:** LOW. Inference rests on A-4 (unverified — the actual N is not given anywhere in this problem). Rivals: "the rates are measured on a large, stable base and the jump is real" is live and not ruled out. Two axes short. This is the single cheapest diagnostic in the entire analysis (see Sensitivity, §5 adversarial pass) — a raw-count pull Northbrook can do today.

### C6 — Illustrative annualized-risk framing (Fermi estimate), explicitly scenario-conditional

```text
GT-1 + GT-2 + C4 (LOW) + C5 (LOW)
→ [Assumes: A-5] treating the Q3 quarterly rate as an illustrative, sustained steady-state non-renewal probability across all four quarters
→ this is explicitly a scenario, not a forecast, since GT-8 shows the four quarters are different cohorts
→ compounding the Q3 rate this way gives an illustrative annualized logo-attrition figure of roughly 1-(1-0.092)^4 ≈ 32%
→ compounding the Q1 rate the same way gives roughly 1-(1-0.041)^4 ≈ 15% — a ratio of roughly 2.1x
→ without a given customer count or total ARR, neither supplied in this problem, this illustrative figure cannot be converted into a dollar amount
→ the given $18k-$40k ACV range only bounds the per-account stakes — each additional churned logo costs $18k-$40k/year of ARR — not the portfolio-wide impact
→ urgency framing should therefore be scenario-based rather than a single number: if Q3 is representative of a new baseline, portfolio annual-attrition risk roughly doubles
→ if Q3 is instead a cohort-specific or noise artifact (C4/C5), portfolio risk is largely unchanged
→ resolving which scenario applies is a precondition for sizing real dollar urgency, which Northbrook can compute immediately once it supplies customer count and ARR
```
**Pre-check:** head: GT-1, GT-2, C4 (LOW), C5 (LOW) · ?-marked: none · lowest cited: LOW · Inputs ceiling: LOW
**Confidence:** LOW (mechanically capped by citing C4 and C5, which is appropriate here: the dollar-urgency scenario literally cannot be resolved until the cohort-vs-noise question is resolved). Recomputed arithmetic: 0.908^4 = 0.6797 → 1−0.6797 = 0.3203 (≈32.0%); 0.959^4 = 0.8458 → 1−0.8458 = 0.1542 (≈15.4%); ratio ≈ 2.08x. Figures check out.

### C7 — A nonzero, structurally irreducible churn floor likely exists for this category

```text
GT-9? (industry convention, unverified) + GT-3 (mid-market ACV / category framing)
→ [Assumes: A-6] some portion of mid-market B2B SaaS churn is driven by factors structurally outside a vendor's product/CS control, such as customer M&A, budget elimination, or strategic tool-consolidation decisions
→ a nonzero floor of "unfixable-by-this-team" churn almost certainly exists for this category regardless of execution quality
→ leadership's "find it and fix it" mandate should therefore implicitly target the gap between the current rate and a realistic best-achievable floor, not zero churn
→ separating the fixable fraction — product, onboarding, and service-quality issues — from the structurally irreducible fraction is necessary before setting a remediation target or declaring success
```
**Pre-check:** head: GT-9? (?-marked), GT-3 · ?-marked: GT-9 · lowest cited: none · Inputs ceiling: MEDIUM
**Confidence:** MEDIUM. Inputs ceiling is MEDIUM because of GT-9's `?`. Inference rests on A-6 (unverified here, though directionally plausible and consistent with common B2B SaaS market structure). Rivals: "all of this churn is theoretically fixable with perfect execution" is not a seriously live rival in this market — so only one axis (Inference) is short. What would raise this to HIGH: pulling Northbrook's own historical non-renewal reason codes (pre-dating the current spike) and checking what fraction were coded as structural/strategic versus dissatisfaction-driven — Northbrook's own data, not an external benchmark.

### C8 — Trade-off across fix options: diagnose-first weakly dominates committing to any single lever now

Options considered: (1) status quo/do nothing; (2) commit to CS-capacity investment now; (3) commit to a broad renewal discount now; (3′) a *targeted* discount restricted to confirmed price-sensitive accounts; (4) onboarding-process overhaul for future cohorts; (5) product/offer-gap roadmap investment; (6) a composite — run the near-zero-cost diagnostics first, then fund whichever of (2)-(5) the diagnostics confirm, in proportion to each driver's demonstrated contribution.

**Must-have knockouts (applied before scoring):** (a) must produce a measurable signal within 1-2 quarters via a leading indicator, not wait for a full annual renewal cycle; (b) must not commit an irreversible, hard-to-unwind action before any driver is confirmed. Option (1) status quo fails (a) — it never produces evidence toward resolving GT-7's open hypothesis set — and is knocked out. Option (3) *broad, blanket* discount fails (b) — a blanket discount is sticky, hard to retract, and is referenced at the next renewal regardless of whether it addressed the real driver — and is knocked out; only the targeted variant (3′) survives to scoring.

**Criteria and weights (locked before scoring):** Confidence in causal link given current evidence (5); Cost to implement (3); Speed to first measurable leading-indicator signal (4); Reversibility / downside if wrong (4); Revenue/margin protection (3).

| Option | Confidence (5) | Cost (3) | Speed (4) | Reversibility (4) | Margin (3) | Weighted total |
|---|---|---|---|---|---|---|
| (6) Diagnose first, then fund confirmed driver(s) | 5 | 5 | 5 | 5 | 5 | **95** |
| (2) CS-capacity investment, committed now | 2 | 2 | 3 | 3 | 4 | 52 |
| (3′) Targeted discount, committed now (pre-diagnosis) | 2 | 4 | 4 | 2 | 2 | 52 |

Scores above are judgment calls under current uncertainty, not measured facts, and are flagged as such — they rest on this analysis's own read of the evidence quality for each option (e.g., option (6) scores a clean 5 on every criterion essentially by construction, since it commits nothing before evidence exists).

**Flip test:** Option (6) leads option (2)/(3′) by 43 of 95 possible points. No single-criterion weight change flips the ranking: option (6) weakly dominates on every criterion (it can only match or improve on the information available to a committed-now option, at near-zero extra cost, within the same short window), so even moving any one weight to its extreme does not change the ordering. "No single weight change flips this" is the result.

```text
GT-7 (non-exclusive, unconfirmed hypotheses) + GT-4 (annual renewal cadence, observation lag)
→ [Assumes: A-7] a diagnose-first composite — pulling cohort data, reason codes, and ticket-per-customer normalization — is achievable within 2-4 weeks at low cost
→ that window is far shorter than the annual renewal cycle in which churn itself is observed (GT-4), so skipping diagnostics does not actually buy faster feedback on a committed-now fix
→ applying the weighted trade-off above, after knocking out options that fail the two must-haves, shows the diagnose-first composite outscores every committed-now alternative
→ it weakly dominates because it can only match or improve on the information a committed-now option has, at near-zero extra cost, within the same short window
→ the flip test finds no single-weight reweighting that changes that ranking
→ the trade-off therefore strongly favors sequencing over commitment
→ run the near-zero-cost diagnostics — C1, C4, and C5's falsification tests — before committing material budget to any single fix lever
→[2nd] if leadership hires CS headcount or discounts broadly without diagnosis, the CS team bears the next round of blame if churn doesn't improve, because the real driver (A-2) was never confirmed
→[2nd] a reactive, ticket-driven response can systematically miss the customers most at risk, since low-adoption accounts that never file a ticket stay invisible to it
→[2nd] if a discount pattern becomes known internally, sales may pre-negotiate renewal discounts proactively, compounding margin erosion beyond the original targeted intent
→[2nd] if competitive displacement is even partially real, a visible churn spike or a publicized discount or support backlog becomes ammunition competitors can use in sales conversations
→[2nd] near-term, diagnostics are low-cost and should run now, while any funded fix will not show up in the churn rate itself until the affected cohort's next annual renewal twelve months out (GT-4)
→[2nd] medium-term, the leading indicators CS already tracks — ticket volume and adoption score — should respond within one to two quarters if the capacity-scaling hypothesis is correct and addressed
→[3rd] long-term, if a cohort-specific shock is the only real driver, the elevated rate should mechanically subside on its own within two to four quarters as that vintage ages out of the renewal population
→[3rd] if leadership credits a concurrent fix for that natural reversion, it will misallocate confidence and future resourcing toward a lever that did not actually cause the improvement
```
**Pre-check:** head: GT-7, GT-4 (no chains cited) · ?-marked: none · lowest cited: none · Inputs ceiling: HIGH
**Confidence:** MEDIUM. Inputs are clean. Inference rests on A-7 (unverified but low-risk — a same-day internal check of whether CS/RevOps can actually pull renewal-reason codes and signup-date tags settles it). Rivals: the obvious rival — "leadership time pressure makes any delay unacceptable, commit now" — is substantially undercut by GT-4 itself: because churn is only *realized* at each cohort's annual renewal regardless, a 2-4 week diagnostic delay does not meaningfully slow the feedback loop on any fix leadership would commit to anyway. One axis (Inference) short → MEDIUM.

**Second-order pass (both lenses walked, both marked above on C8):** *Actor lens* — CS team, sales, quiet low-adoption/no-ticket customers, and competitors each react differently once a diagnose-first or a commit-now path is chosen (hops marked →[2nd] above). *Time lens* — immediate, medium-term (1-2 quarters, leading indicators), and long-term (2-4 quarters, cohort aging-out and the post-hoc-fallacy risk) horizons produce different readings of the same metric (hops marked →[2nd]/→[3rd] above). No extension hop above contradicts a Ground Truth; no return to Phase 2 was triggered by this pass.

**End-of-phase Assumption Audit (scan table):**

| Chain | Step | Step Text (brief) | Assumption surfaced? | Added to Table? |
|---|---|---|---|---|
| C1 | 1 | the headline "churn more than doubled" compares two different renewal-cohort populations (the Q... | none | no (clean pass) |
| C1 | 2 | the raw percentage jump is therefore consistent with at least three structurally different expl... | none | no (clean pass) |
| C1 | 3 | broad deterioration would affect all cohorts; a cohort-specific shock would concentrate only in... | none | no (clean pass) |
| C1 | 4 | the trend as stated therefore cannot be used to pick a root cause without first decomposing it... | none | no (clean pass) |
| C1 | 5 | the first diagnostic priority is accordingly not "which of the six hypotheses" but "is this a b... | none | no (clean pass) |
| C2 | 1 | [Assumes: A-1] both signals are consistent with being downstream symptoms of one shared upstrea... | A-1 | yes |
| C2 | 2 | two plausible shared upstream shifts are a product change that made the platform harder to use,... | none | no (clean pass) |
| C2 | 3 | treating "service/support quality degradation" and "onboarding failure" as two separate boxes o... | none | no (clean pass) |
| C2 | 4 | the two signals more plausibly point toward one upstream capacity/quality shift than confirm tw... | none | no (clean pass) |
| C3 | 1 | [Assumes: A-2] a common structural cause of simultaneous ticket-volume increase and adoption-sc... | A-2 | yes |
| C3 | 2 | capacity failing to scale produces slower response times, visible as a higher ticket backlog, a... | none | no (clean pass) |
| C3 | 3 | if true, this predicts a falsifiable signature: ticket volume per customer rising and resolutio... | none | no (clean pass) |
| C3 | 4 | it also predicts adoption scores falling disproportionately among customers served during the c... | none | no (clean pass) |
| C3 | 5 | the Q3-renewal cohort, having lived through that window right before its renewal decision, shou... | none | no (clean pass) |
| C3 | 6 | "service/support degradation driven by capacity not scaling with growth" is a plausible, specif... | none | no (clean pass) |
| C3 | 7 | it is not yet confirmed — it rests entirely on A-2, which Northbrook can check at near-zero cos... | none | no (clean pass) |
| C4 | 1 | [Assumes: A-3] the Q3-renewal cohort experienced a distinct negative event at or near signup ro... | A-3 | yes |
| C4 | 2 | candidate signup-time events include a specific onboarding-team change, a product-onboarding-fl... | none | no (clean pass) |
| C4 | 3 | this hypothesis is self-limiting and sharply falsifiable: if true, elevated churn should track... | none | no (clean pass) |
| C4 | 4 | if the true cause were ongoing systemic deterioration instead, elevated churn should persist or... | none | no (clean pass) |
| C4 | 5 | distinguishing "cohort-specific one-off" from "ongoing systemic deterioration" is the single hi... | none | no (clean pass) |
| C4 | 6 | resolving that fork requires only renewal-reason codes and signup-date tagging of churned accou... | none | no (clean pass) |
| C5 | 1 | [Assumes: A-4] a jump from 4.1% to 9.2% could be produced by as few as a handful of additional... | A-4 | yes |
| C5 | 2 | this is plausible if the renewal-cohort denominator each quarter is modest, as could be expecte... | none | no (clean pass) |
| C5 | 3 | under that assumption the underlying per-customer churn probability would not need to have chan... | none | no (clean pass) |
| C5 | 4 | this is immediately and cheaply falsifiable: Northbrook already has the raw counts behind both... | none | no (clean pass) |
| C5 | 5 | recomputing the two rates' confidence intervals, even informally, shows whether 4.1% and 9.2% a... | none | no (clean pass) |
| C6 | 1 | [Assumes: A-5] treating the Q3 quarterly rate as an illustrative, sustained steady-state non-re... | A-5 | yes |
| C6 | 2 | this is explicitly a scenario, not a forecast, since GT-8 shows the four quarters are different... | none | no (clean pass) |
| C6 | 3 | compounding the Q3 rate this way gives an illustrative annualized logo-attrition figure of roug... | none | no (clean pass) |
| C6 | 4 | compounding the Q1 rate the same way gives roughly 1-(1-0.041)^4 ≈ 15% — a ratio of roughly 2.1... | none | no (clean pass) |
| C6 | 5 | without a given customer count or total ARR, neither supplied in this problem, this illustrativ... | none | no (clean pass) |
| C6 | 6 | the given $18k-$40k ACV range only bounds the per-account stakes — each additional churned logo... | none | no (clean pass) |
| C6 | 7 | urgency framing should therefore be scenario-based rather than a single number: if Q3 is repres... | none | no (clean pass) |
| C6 | 8 | if Q3 is instead a cohort-specific or noise artifact (C4/C5), portfolio risk is largely unchang... | none | no (clean pass) |
| C6 | 9 | resolving which scenario applies is a precondition for sizing real dollar urgency, which Northb... | none | no (clean pass) |
| C7 | 1 | [Assumes: A-6] some portion of mid-market B2B SaaS churn is driven by factors structurally outs... | A-6 | yes |
| C7 | 2 | a nonzero floor of "unfixable-by-this-team" churn almost certainly exists for this category reg... | none | no (clean pass) |
| C7 | 3 | leadership's "find it and fix it" mandate should therefore implicitly target the gap between th... | none | no (clean pass) |
| C7 | 4 | separating the fixable fraction — product, onboarding, and service-quality issues — from the st... | none | no (clean pass) |
| C8 | 1 | [Assumes: A-7] a diagnose-first composite — pulling cohort data, reason codes, and ticket-per-c... | A-7 | yes |
| C8 | 2 | that window is far shorter than the annual renewal cycle in which churn itself is observed (GT-... | none | no (clean pass) |
| C8 | 3 | applying the weighted trade-off above, after knocking out options that fail the two must-haves,... | none | no (clean pass) |
| C8 | 4 | it weakly dominates because it can only match or improve on the information a committed-now opt... | none | no (clean pass) |
| C8 | 5 | the flip test finds no single-weight reweighting that changes that ranking | none | no (clean pass) |
| C8 | 6 | the trade-off therefore strongly favors sequencing over commitment | none | no (clean pass) |
| C8 | 7 | run the near-zero-cost diagnostics — C1, C4, and C5's falsification tests — before committing m... | none | no (clean pass) |
| C8 | 8 [2nd] | if leadership hires CS headcount or discounts broadly without diagnosis, the CS team bears the... | none | no (clean pass) |
| C8 | 9 [2nd] | a reactive, ticket-driven response can systematically miss the customers most at risk, since lo... | none | no (clean pass) |
| C8 | 10 [2nd] | if a discount pattern becomes known internally, sales may pre-negotiate renewal discounts proac... | none | no (clean pass) |
| C8 | 11 [2nd] | if competitive displacement is even partially real, a visible churn spike or a publicized disco... | none | no (clean pass) |
| C8 | 12 [2nd] | near-term, diagnostics are low-cost and should run now, while any funded fix will not show up i... | none | no (clean pass) |
| C8 | 13 [2nd] | medium-term, the leading indicators CS already tracks — ticket volume and adoption score — shou... | none | no (clean pass) |
| C8 | 14 [3rd] | long-term, if a cohort-specific shock is the only real driver, the elevated rate should mechani... | none | no (clean pass) |
| C8 | 15 [3rd] | if leadership credits a concurrent fix for that natural reversion, it will misallocate confiden... | none | no (clean pass) |

## 5. Abandoned Reasoning

### Dead End: Treating Q1 as the baseline and Q3 as the anomaly

**What was tried:** Treating Q1's 4.1% as the "normal" baseline and Q3's 9.2% as the anomaly requiring explanation.

**Why abandoned:** This silently assumes a direction for the anomaly; it is equally possible Q1 was an unusually *low* quarter (e.g., a renewal cohort with unusually few at-risk accounts) and Q3 is closer to an underlying "true" rate.

**What it ruled out:** Nothing on its own — this reframing doesn't change which diagnostics are needed, so it was folded into C4/C8 (cohort-composition framing) rather than pursued as a separate chain, to avoid double-counting the same cohort-structure argument under a different label.

### Dead End: Inventing specific ticket categories, named competitors, or a specific pricing-change date

**What was tried:** Fabricating plausible-sounding specifics (ticket categories, competitor names, a pricing-change date) to make the analysis feel concrete.

**Why abandoned:** None of this was supplied in the task, and the task explicitly instructs against fabricating specific internal data.

**What it ruled out:** Any appearance in this analysis of invented specifics; every such detail is instead named as an open diagnostic question (see Conclusion).

### Dead End: Computing a precise dollar ARR-at-risk figure

**What was tried:** Computing a single, precise dollar ARR-at-risk figure for the churn increase.

**Why abandoned:** No customer count or total ARR was given; producing a specific dollar figure would require silently assuming a customer-base size and presenting it as if real.

**What it ruled out:** A single-number urgency claim; replaced with the scenario-bracketed, unit-based estimate in C6 plus an explicit call for the missing inputs.

### Dead End: Accepting CS's flags at face value as confirming CS-capacity as the driver

**What was tried:** Accepting CS's qualitative flags (tickets, adoption) at face value as sufficient evidence that "service/support quality degradation" is *the* driver, and recommending an immediate CS-capacity fix.

**Why abandoned:** C1's cohort-structure logic plus C4 and C5 show that the same two given percentages are equally consistent with a cohort-specific shock or statistical noise — face-value acceptance of one hypothesis among several equally-supported ones is underdetermined by the evidence actually in hand.

**What it ruled out:** Committing budget to a CS-capacity fix as the sole or first action before running the diagnostics in C1/C4/C5; this rival remains *live but unconfirmed*, not disproven — it is simply not uniquely supported, which is exactly why C8 recommends diagnosing before funding any one lever.

## 6. Conclusion

**Recommended approach:** Run a 2-4 week, near-zero-cost diagnostic sprint before committing budget to any fix. In priority order (cheapest/fastest first): (1) pull raw renewal-cohort counts (N and non-renewal count) for Q1 and Q3 to test whether the gap is statistically distinguishable from noise at the cohort sizes actually involved (chain C5); (2) tag churned accounts by signup vintage/cohort to test for a concentrated onboarding or pricing shock specific to one renewal vintage (chain C4); (3) pull renewal-reason codes and win/loss notes for churned accounts to directly classify cause (offer gap, price, competitive, service) rather than inferring it (chains C2/C3); (4) normalize ticket volume per customer and check the CS-headcount-to-customer-count ratio trend to test the capacity-scaling hypothesis (chain C3); (5) cross-reference any pricing/packaging change history against churned-account timing to refine the cohort-shock hypothesis (chain C4). Only once one or more drivers are confirmed should Northbrook fund the corresponding fix — and even then, measure early success using leading indicators (ticket-per-customer trend, adoption-score trend) over the next 1-2 quarters, not the annual churn rate itself, since the churn rate for any affected cohort cannot move again until that cohort's next renewal (chain C8, GT-4). Before setting a target, separate the fixable fraction of churn from a likely nonzero structural floor this team cannot eliminate (chain C7). (chain C1, C4, C5, C8)

**Key insight:** The headline "churn more than doubled" is not yet evidence of a single root cause. Because annual-contract churn rates are measured on a different renewal cohort each quarter (chain C1), the same two data points are equally consistent with genuine broad deterioration, a cohort-specific shock, or statistical noise — and the diagnostics that resolve this ambiguity take weeks, while any committed fix cannot even be judged by the churn rate itself for a full year. Diagnosing first therefore costs little of the time leadership is worried about losing. (chain C1, C8)

**Trade-offs acknowledged:** Diagnosing first costs 2-4 weeks of delay against leadership's urgency and declines to hand leadership a simple, single-cause story immediately; it also means CS's qualitative flags (tickets, adoption) are treated as leading-indicator clues rather than as already-confirmed causes, which may read as under-crediting the team closest to the customer. (chain C8)

**Pre-check:** head: C1 (HIGH), C8 (MEDIUM) · ?-marked inputs used directly: none · lowest cited: MEDIUM (C8) · Inputs ceiling: MEDIUM
**Confidence:** MEDIUM that "the root cause is not yet determinable from the facts given, and a short diagnostic sprint is the correct next step before committing to a fix" — capped at MEDIUM by chain C8, whose own Inference axis rests on A-7 (that Northbrook can retrieve cohort/reason-code/ticket data within 2-4 weeks at low cost). That one check — a same-day confirmation that this data is actually retrievable — is what would lift this conclusion to HIGH; if that data turns out to be unavailable or much slower to retrieve than assumed, the diagnose-first recommendation weakens and the trade-off in C8 would need to be re-run with a longer diagnostic-cost estimate. (chain C1, C8)
## Appendix — process output

## §6→§4 closure ledger (process output)

- "Recommended approach: Run a 2-4 week, near-zero-cost diagnostic sprint..." → chains C1, C4, C5, C8 ✓
- "Key insight: The headline 'churn more than doubled' is not yet evidence of a single root cause..." → chains C1, C8 ✓
- "Trade-offs acknowledged: Diagnosing first costs 2-4 weeks of delay..." → chain C8 ✓
- "Confidence: MEDIUM that 'the root cause is not yet determinable...'" → chains C1, C8 ✓ (discharges D-07's naming requirement: names C8 as the capping chain and A-7 as the input to verify)

Scan complete: 4 §6 claims, all four carry inline chain citations; 0 cut.

## Self-audit scan (process output)

**Table 1 — Chain form (section 4)**

| Chain | Chain Head (brief) | Form conforming? | Rule applied | Dependency clean? | Band | Act attempted? | Edges fired |
|---|---|---|---|---|---|---|---|
| C1 | GT-1 + GT-2 + GT-8 | yes | n/a | yes | HIGH | yes | none |
| C2 | GT-5 + GT-6 | yes | n/a | yes | LOW | yes | none |
| C3 | GT-5 + GT-6 + C2 | yes | n/a | yes (depends on C2, no cycle) | LOW | yes | none |
| C4 | GT-1 + GT-2 + GT-8 + GT-3 | yes | n/a | yes | LOW | yes | none |
| C5 | GT-1 + GT-2 | yes | n/a | yes | LOW | yes | none |
| C6 | GT-1 + GT-2 + C4 + C5 | yes | n/a | yes (depends on C4, C5, no cycle) | LOW | yes | none |
| C7 | GT-9? + GT-3 | yes | n/a | yes | MEDIUM | yes | none |
| C8 | GT-7 + GT-4 | yes | n/a | yes | MEDIUM | yes | none |

**Table 2 — Claim inventory (section 6)**

| §6 Span (brief) | Construct | Claim under R11? | R11 clause applied | Chain cited |
|---|---|---|---|---|
| "Recommended approach: Run a 2-4 week..." | bold lead-in | yes | prescribed lead-in — always a claim | C1, C4, C5, C8 |
| "Key insight: The headline...not yet evidence..." | bold lead-in | yes | prescribed lead-in — always a claim | C1, C8 |
| "Trade-offs acknowledged: Diagnosing first costs..." | bold lead-in | yes | prescribed lead-in — always a claim | C8 |
| "Pre-check: head: C1 (HIGH), C8 (MEDIUM)..." | bold lead-in | no | structural scaffold field for the Confidence line, not itself an assertion (treated as a section-intro-label equivalent) | n/a |
| "Confidence: MEDIUM that 'the root cause is not yet determinable...'" | bold lead-in | yes | prescribed lead-in — always a claim | C1, C8 |

Scan complete: 8 chain rows, one per section-4 chain block in order; 5 section-6 rows, one per construct in order — 4 claims under R11, 1 excluded. 0 chains malformed, 0 claims untraced.

## Adversarial pass (process output)

**Recompute:** C6's compounding arithmetic recomputed independently: (1-0.092)^4 = 0.908^4 → 0.908^2 = 0.824464 → 0.824464^2 = 0.679742 → churn ≈ 32.03%. (1-0.041)^4 = 0.959^4 → 0.959^2 = 0.919681 → 0.919681^2 = 0.845814 → churn ≈ 15.42%. Ratio 32.03/15.42 ≈ 2.08x — matches C6's stated figures; no arithmetic error found. C8's weighted-sum trade-off table recomputed: Option 6 = 5·5+5·3+5·4+5·4+5·3 = 95 ✓; Option 2 = 2·5+2·3+3·4+3·4+4·3 = 52 ✓; Option 3′ = 2·5+4·3+4·4+2·4+2·3 = 52 ✓. All recomputed figures match the stated totals.

**Sensitivity:** The single assumption whose falsity would flip the most of the analysis is A-4 (small renewal-cohort N, used in C5) — not GT-marked `?` since it is an assumption rather than a ground truth, but the highest-leverage unresolved input in the whole set: if raw counts show the cohorts are large and the gap is statistically real, the "could be noise" branch (C5) collapses and diagnostic effort concentrates on C2/C3/C4/C7; if the counts show the gap is not statistically distinguishable from noise, most of C6's urgency framing and much of the downstream diagnostic plan becomes unnecessary. Per-chain weakest links: C2→A-1, C3→A-2, C4→A-3, C5→A-4, C6→A-3/A-4 (inherited via C4/C5), C7→GT-9? and A-6, C8→A-7.

**Rival:** Headline conclusion ("root cause not yet determinable from the given facts; diagnose first") — strongest rival: "CS's flags are already sufficient evidence that service/support degradation is the driver; fix CS capacity now." This rival is not ruled out by the given facts (see §5 Abandoned Reasoning entry); it remains live but unconfirmed, at the same epistemic status as the cohort-shock and noise explanations. Intermediate chains: C2's rival ("tickets and adoption are two unrelated problems") is live, named on C2's Confidence line. C4's rival ("broad systemic deterioration," C1's other branch) is live, named on C4's Confidence line. C7's rival ("zero churn is theoretically achievable with perfect execution") is not seriously live, noted on C7's Confidence line. C1 and C8 carry no rival serious enough to unseat them, noted on their own Confidence lines.

**Adversarial technique — pre-mortem** (the conclusion is a plan/recommendation, so pre-mortem applies per the inversion-vs-pre-mortem decision rule; the pre-mortem procedure was opened and read from the skill body before this pass was run, not recalled):

- **Premise:** It is 12 months from now. Leadership rushed into a CS headcount hire and a broad renewal-discount program without completing the diagnostic sprint. Churn is still at or above 9% and gross margin is worse. What caused this?
- **Causes** (generated from three stakeholder viewpoints — CFO, CS manager, competitor — unfiltered):
  1. (CFO) Discounting eroded margin broadly, including on accounts that were never going to churn, without being offset by confirmed retention gains.
  2. (CS manager) New CS hires took 3-6 months to ramp; by the time they were productive, leadership's patience had run out and reorganized CS again, adding internal instability on top of the original customer-facing issue.
  3. (Competitor-exploitation) If competitive displacement was actually a real partial driver, it was never tested (no win/loss notes pulled), so the competitor kept winning deals unchallenged while budget went to CS and pricing instead.
  4. (Measurement-timing) Because churn is only observed annually per cohort (GT-4), no real churn-rate feedback existed for 12 months; leadership either prematurely declared the fix a failure, or prematurely declared success because a cohort-specific shock (C4) naturally aged out and got credited to a fix it had nothing to do with.
  5. (Statistical-noise) If the original jump was substantially small-N noise (C5), any "fix" looks successful or unsuccessful almost at random the next quarter, and leadership draws a false lesson either way.
- **Clusters:**
  - Cluster A, "Symptom-vs-cause misattribution" (bears on C2, C3, C4) — fixing CS capacity or tickets without confirming A-1/A-2, or fixing pricing without confirming A-3's cohort specificity.
  - Cluster B, "Measurement-lag misread" (bears on GT-4, GT-8, C6) — annual renewal cadence means fix efficacy can't be judged for a full cycle; a natural cohort reversion (C4) can be misattributed to a fix.
  - Cluster C, "Untargeted discounting margin erosion" (bears on C7, C8) — a pricing-lever fix applied broadly ignores the structural-churn-floor finding and risks giving away margin to non-price-sensitive accounts.
  - Cluster D, "Diagnosis skipped under urgency pressure" (bears on C1, C5, C8) — leadership mandate pressure short-circuits the near-zero-cost diagnostics that would have redirected the whole effort cheaply.
- **Disposition:**
  - Cluster A — Plan change: require that any funded fix cite which diagnostic (reason codes, cohort tagging, ticket-per-customer normalization) confirmed its target cause before funding it.
  - Cluster B — Plan change: define success/failure measurement windows using leading indicators (ticket volume/resolution time, adoption-score trend), tracked monthly, for the first 2-3 quarters after any fix; reserve churn-rate judgment for after the funded cohort has gone through a full renewal cycle.
  - Cluster C — Accepted risk with named mitigation: if a retention discount is used at all, restrict it to accounts with confirmed price-sensitivity signals (renewal-reason codes / sales notes), never a blanket renewal discount; accept the residual risk that price-sensitive churn outside that confirmed set is not addressed in the first pass.
  - Cluster D — Plan change: run the five diagnostics named in the Conclusion within the first 2-4 weeks, explicitly timeboxed, in parallel with (not instead of) preparing fix options, so urgency is honored without skipping diagnosis.

**Falsification:** The headline conclusion is false if, once Northbrook pulls raw renewal-cohort counts and churned-account reason codes: (a) the Q1 vs Q3 cohort sizes are statistically indistinguishable from noise at standard confidence levels (confirming C5 alone explains the headline), or (b) churned accounts are overwhelmingly concentrated in a single prior onboarding/pricing vintage with no elevated churn in other vintages (confirming C4 alone explains it and the issue is self-limiting), or (c) elevated churn instead persists broadly across all vintages into Q4 and beyond with no cohort concentration and no noise explanation (confirming genuine broad deterioration, which would then require urgently distinguishing among the remaining capacity/offer/pricing/competitive hypotheses rather than the "diagnose calmly first" framing recommended here).

## Techniques not applied (process output)

- theoretical-limit — not applicable at Phase 1 — the essence question here is which upstream driver(s) explain the churn-rate increase, not whether a current figure is a convention versus a hard mathematical/physical bound; that reframe is instead applied at Phase 4 (chain C7), where it does fire.
- inversion — not applicable at Phase 5 — the headline conclusion is a plan/recommendation (a diagnostic-then-fix roadmap), not a bare claim, so per the inversion-vs-pre-mortem decision rule the Phase 5 adversarial technique routes to pre-mortem instead; inversion's Phase 2 invocation (challenging each of the six candidate hypotheses and deriving their necessary preconditions) does fire — see the Assumptions Table items and chains C2-C7.

## Self-Audit Gate (process output)

**Criterion 1: Identify Essence**
Quoted span: "Northbrook's quarterly renewal non-renewal rate has risen sharply between two observed quarters (4.1% → 9.2%)... so the real question is not 'which of the six named hypotheses is correct' but 'what is the cheapest, fastest way to determine which of them — alone or in combination — is actually operating, before resources are committed to a fix.'"
Band: **Rigorous**
Justification: The statement names the core decision (how to isolate the driver before committing resources), not a symptom or a restatement of the prompt, is specific to this problem's exact figures and framing, and each of its seven success criteria is checkable by scanning the Conclusion/Derivation Chains without further clarification.

**Criterion 2: Challenge Assumptions**
Quoted span (from the Assumption Audit scan, section 4): "C2 | 1 | [Assumes: A-1] both signals are consistent with being downstream symptoms of one shared upstream shift... | A-1 | yes" — and the scan's 55 rows cover every named hop across C1-C8 in order, with "none / no (clean pass)" recorded for every hop that introduces no new assumption.
Band: **Rigorous**
Justification: All Type values are drawn from the four-type scheme; Verdict cells are token-led (Challenge/Discard — justification, per the Verdict Vocabulary); every assumption used in a chain despite being unverified carries "unverified — flagged" in its Verification cell; at least one assumption (item 8) is Discarded rather than merely Accepted; and the Assumption Audit scan is exhaustive over every named derivation-chain step, confirming no surfaced assumption (A-1 through A-7) is missing from the Assumptions Table.

**Criterion 3: Establish Ground Truths**
Quoted span: "`?`-marked: GT-9 (1 of 9)." together with "Read-at-source locations: GT-1 through GT-7 — the task's 'THE SITUATION' and introductory context paragraphs... GT-8 — derived by definition..."
Band: **Rigorous**
Justification: Every GT carries a stable ID matching the Derivation Chains section's references; every GT carries a provenance label (read-at-source for GT-1–8, unverified with a Phase 3 failure record for GT-9); the `?`-marked GT is enumerated by ID and the enumeration matches the one suffixed entry in the list (checked: GT-9 is the only `?` in the list); GT-1, GT-2, GT-8 (unsuffixed, feeding HIGH-confidence chain C1) each name a read-at-source location; no Phase-2-Discarded assumption (e.g., item 8) appears in this list.

**Criterion 4: Reason Upward**
Quoted span (from the self-audit scan's chain-form table): "C1 | GT-1 + GT-2 + GT-8 | yes | n/a | yes | HIGH | yes | none" through "C8 | GT-7 + GT-4 | yes | n/a | yes | MEDIUM | yes | none" — all 8 rows score Form conforming = yes, Dependency clean = yes.
Band: **Rigorous**
Justification: Every conclusion in section 6 has exactly one chain in section 4; every chain carries a genuine intermediate (verified by the scan's conforming rows); hops are rendered one-per-line in arrow-led form with no ordered-list rendering; every surfaced assumption carries an inline `[Assumes: A-N]` mark (confirmed by the Criterion-2 Assumption Audit scan); the Abandoned Reasoning section documents four dead ends in the prescribed What-was-tried/Why-abandoned/What-it-ruled-out structure; no analogy is used as direct, ungrounded evidence (GT-9's industry convention is explicitly flagged unverified rather than offered as justification on its own).

**Criterion 5: Validate**
Quoted span: "**Confidence:** MEDIUM. Inference rests on A-4 (unverified — the actual N is not given anywhere in this problem). Rivals: 'the rates are measured on a large, stable base and the jump is real' is live and not ruled out. Two axes short." (chain C5) — and the adversarial pass record's Recompute/Sensitivity/Rival/Premise-Causes-Clusters-Disposition/Falsification parts are all present with content.
Band: **Rigorous**
Justification: Every chain's weakest link is named on its own Confidence line; no chain consuming a `GT-N?` input (C7) is rated HIGH; every chain citing another chain is capped at or below that chain's band (C3≤C2, C6≤min(C4,C5)); the Conclusion's MEDIUM rating matches its weakest contributing chain (C8); every band matches what its own Inputs/Inference/Rivals axes license per the pre-check lines; and the pre-mortem-based adversarial pass record is complete, with every cluster carrying a named plan change or an explicitly accepted risk with a named mitigation.

**Criterion 6: Conclusion-to-Ground-Truth Traceability**
Quoted span (from the self-audit scan's claim-inventory table): "'Recommended approach: Run a 2-4 week...' | bold lead-in | yes | prescribed lead-in — always a claim | C1, C4, C5, C8" through "'Confidence: MEDIUM...' | bold lead-in | yes | prescribed lead-in — always a claim | C1, C8" — all four claim rows cite a chain, zero untraced.
Band: **Rigorous**
Justification: Every Conclusion-section claim traces to a specific named chain (per the scan and the inline citations); no new reasoning is introduced in section 6 that does not already appear in section 4; and the Key Insight (the cohort-structure reframing of the headline statistic) is a non-obvious finding distinct from the Recommended approach (the diagnostic action sequence), not a restatement of it.

**Gate result:** cleared · passes: 1 · Fix/Repeat fired: no

## Structured summary (process output)

```json
{
  "schema_version": 1,
  "run_mode": "full-composer",
  "assumptions": [
    { "id": "A-1", "type": "untested belief", "verdict": "Challenge" },
    { "id": "A-2", "type": "untested belief", "verdict": "Challenge" },
    { "id": "A-3", "type": "untested belief", "verdict": "Challenge" },
    { "id": "A-4", "type": "untested belief", "verdict": "Challenge" },
    { "id": "A-5", "type": "untested belief", "verdict": "Challenge" },
    { "id": "A-6", "type": "current constraint", "verdict": "Challenge" },
    { "id": "A-7", "type": "untested belief", "verdict": "Challenge" }
  ],
  "ground_truths": [
    { "id": "GT-1", "read_at_source": true },
    { "id": "GT-2", "read_at_source": true },
    { "id": "GT-3", "read_at_source": true },
    { "id": "GT-4", "read_at_source": true },
    { "id": "GT-5", "read_at_source": true },
    { "id": "GT-6", "read_at_source": true },
    { "id": "GT-7", "read_at_source": true },
    { "id": "GT-8", "read_at_source": true },
    { "id": "GT-9", "read_at_source": false }
  ],
  "chains": [
    { "id": "C1", "confidence": "HIGH", "rests_on": ["GT-1", "GT-2", "GT-8"] },
    { "id": "C2", "confidence": "LOW", "rests_on": ["GT-5", "GT-6"] },
    { "id": "C3", "confidence": "LOW", "rests_on": ["GT-5", "GT-6", "C2"] },
    { "id": "C4", "confidence": "LOW", "rests_on": ["GT-1", "GT-2", "GT-8", "GT-3"] },
    { "id": "C5", "confidence": "LOW", "rests_on": ["GT-1", "GT-2"] },
    { "id": "C6", "confidence": "LOW", "rests_on": ["GT-1", "GT-2", "C4", "C5"] },
    { "id": "C7", "confidence": "MEDIUM", "rests_on": ["GT-9?", "GT-3"] },
    { "id": "C8", "confidence": "MEDIUM", "rests_on": ["GT-7", "GT-4"] }
  ],
  "dead_ends": [
    "Treating Q1 as the baseline and Q3 as the anomaly",
    "Inventing specific ticket categories, named competitors, or a specific pricing-change date",
    "Computing a precise dollar ARR-at-risk figure",
    "Accepting CS's flags at face value as confirming CS-capacity as the driver"
  ],
  "techniques": {
    "applied": [
      "five-whys",
      "fishbone",
      "inversion",
      "pre-mortem",
      "trade-off",
      "second-order",
      "estimate",
      "theoretical-limit"
    ],
    "not_applied": [
      {
        "technique": "theoretical-limit",
        "phase": 1,
        "reason": "the essence question here is which upstream driver(s) explain the churn-rate increase, not whether a current figure is a convention versus a hard mathematical/physical bound; that reframe is instead applied at Phase 4 (chain C7), where it does fire"
      },
      {
        "technique": "inversion",
        "phase": 5,
        "reason": "the headline conclusion is a plan/recommendation (a diagnostic-then-fix roadmap), not a bare claim, so per the inversion-vs-pre-mortem decision rule the Phase 5 adversarial technique routes to pre-mortem instead"
      }
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
    "recommendation": "Run a 2-4 week, near-zero-cost diagnostic sprint before committing budget to any fix. In priority order (cheapest/fastest first): (1) pull raw renewal-cohort counts (N and non-renewal count) for Q1 and Q3 to test whether the gap is statistically distinguishable from noise at the cohort sizes actually involved (chain C5); (2) tag churned accounts by signup vintage/cohort to test for a concentrated onboarding or pricing shock specific to one renewal vintage (chain C4); (3) pull renewal-reason codes and win/loss notes for churned accounts to directly classify cause (offer gap, price, competitive, service) rather than inferring it (chains C2/C3); (4) normalize ticket volume per customer and check the CS-headcount-to-customer-count ratio trend to test the capacity-scaling hypothesis (chain C3); (5) cross-reference any pricing/packaging change history against churned-account timing to refine the cohort-shock hypothesis (chain C4). Only once one or more drivers are confirmed should Northbrook fund the corresponding fix — and even then, measure early success using leading indicators (ticket-per-customer trend, adoption-score trend) over the next 1-2 quarters, not the annual churn rate itself, since the churn rate for any affected cohort cannot move again until that cohort's next renewal (chain C8, GT-4). Before setting a target, separate the fixable fraction of churn from a likely nonzero structural floor this team cannot eliminate (chain C7).",
    "confidence": "MEDIUM",
    "rests_on": ["C1", "C8"]
  }
}

```
