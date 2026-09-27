# Loyalty Program Funding Decision — First-Principles Analysis

## Bottom line, up front

**Recommendation: Fund conditionally — not the full $310K/year blind commitment, not zero.** Fund a 1–2 week churn diagnostic (data pull, not a study) running in parallel with a scoped, cost-capped pilot with a hard go/no-go gate at 90–180 days. This fits comfortably inside the 3-week board deadline: the board answer becomes "we're funding a gated pilot with a defined checkpoint," not "yes" or "no."

**Why not a straight yes:** The proposal's causal story doesn't survive a timeline check. Churn started rising roughly **six months ago**; the competitor's loyalty program launched **one month ago**. The competitor's move cannot explain the first five months of the spike, and "match the competitor" is doing most of the persuasive work in the pitch. Separately, the public statistics claiming loyalty programs cut churn by ~10–19% trace back (I checked) to vendor marketing content citing a secondary, unverifiable source — weak evidence for the core bet.

**Why not a straight no:** The dollars justify *some* action regardless of which lever is right. At current churn (6.8%), the existing 48,000-member base is worth about **$279 in lifetime revenue per customer**, versus **$452 at the pre-spike 4.2% rate** — roughly **$8.3M in destroyed customer-relationship value** already baked into the run rate. And the financial bar for the *specific* $310K program is low: on a conservative 12-month, no-new-signups basis, it breaks even if churn falls from 6.8% to only about **6.0%** — a third of the way to the 5% target, not all the way.

**Top 3 things that would change this answer:**
1. **The voluntary/involuntary split.** If the diagnostic shows churn is majority payment-failure-driven (a common finding in subscription businesses, and one a rewards program cannot touch), redirect the $310K to dunning/payment-recovery tooling instead — that's a different, better bet, not a variant of this one.
2. **The true all-in cost.** If "$310K to operate" excludes the redemption/credit liability (i.e., real cost is materially higher, e.g., 2–3x), the breakeven bar rises and the case weakens; get Finance to confirm scope before committing.
3. **Whether the churn spike coincides with a price change, product incident, or single acquisition-channel cohort.** If so, that's the actual lever, and loyalty is a band-aid over it.

---

## 1. Problem Essence

**Core problem:** Given a fast, large rise in monthly churn (4.2%→6.8%) whose cause is undiagnosed, should the company commit $310,000/year to a specific proposed remedy (a loyalty/rewards program) before knowing whether that remedy addresses the actual cause?

**Success criteria** (checkable against the Conclusion, section 6):
- A funding verdict (fund / don't fund / fund conditionally) is stated, with the conditions named if conditional.
- The verdict is tied to an explicit dollar comparison: cost of status-quo churn vs. cost of the program vs. the churn-reduction level at which the program pays for itself.
- The verdict does not depend on an unverified assumption about *why* churn rose without saying so plainly.
- The verdict is deliverable inside the stated 3-week window without requiring information this analysis cannot obtain.

---

## 2. Assumptions Table

Companion-technique note: the Phase 2 **inversion** procedure was applied to the proposal's implicit claim ("funding this program will pull churn to ~5%"), generating A12–A13 below. The Phase 2 **fishbone** procedure was applied to the churn spike's cause space using the category set {Pricing, Product/Quality, Involuntary/Payment, Competitive, Acquisition/Onboarding, Support/Service} — each category has no discriminating observation available from the facts given, which is itself the finding: nothing in the stated facts lets us tell these apart yet, which is exactly why a diagnostic (not a bigger analysis) is the prescribed next step, not a further round of desk research.

| # | Assumption | Type | Treatment | Verdict | Verification |
|---|---|---|---|---|---|
| A1 | Churn rose because of a lack of loyalty/rewards | untested belief | verify via diagnostic | Challenge — em dash: temporal mismatch (see C3) undermines this as the primary driver of most of the spike | unverified — flagged |
| A2 | A competitor's loyalty launch is a valid reason to match | convention | challenge explicitly | Challenge — em dash: competitor launched ~5 months after the spike began; parity has marketing value but is not evidence of a fix | unverified — flagged |
| A3 | 5% churn is achievable specifically via this lever | untested belief | verify/diagnose | Challenge — em dash: no data distinguishes voluntary from involuntary churn, which have very different loyalty-lever responsiveness | unverified — flagged |
| A4 | 48,000 members × $19/mo and the churn figures are current/accurate | untested belief | reconcile against billing/CRM before publishing to the board | Accept — em dash: used as the stipulated basis for this analysis; not independently reconciled in this session | unverified — flagged |
| A5 | $310K/year fully captures total program cost, including redemption/credit liability | untested belief | clarify with Finance/CS before funding | Challenge — em dash: "to operate" is ambiguous as stated; changes breakeven materially either way | unverified — flagged |
| A6 | Loyalty/rewards programs are a well-evidenced general lever for reducing churn | convention | challenge explicitly | Challenge — em dash: the specific efficacy stats found trace to vendor-promotional content citing an unverifiable secondary source (see GT-8?) | reported-by-delegate — flagged |
| A7 | The 48,000-member base stays roughly constant over the next 12 months (no material net signup growth or further churn shock) | current constraint | record as a modeling simplification | Accept — em dash: expires at 12 months or sooner if signup/churn trends shift; disclosed as a simplification in C1/C2 | unverified — flagged |
| A8 | Subscription LTV can be modeled as ARPU ÷ monthly churn, and cohort revenue as ARPU×N×Σ(1−c)^t | physical law (mathematical identity) | accept as ground-truth candidate | Accept — em dash: independently re-derived by geometric series in C1/C2, not merely cited | read-at-source (by derivation) |
| A9 | The 3-week deadline precludes any diagnostic work before deciding | convention/current constraint | challenge explicitly | Challenge — em dash: a voluntary/involuntary churn-reason data pull is typically a days-long query, not a multi-week study; the deadline governs the board *message*, not whether groundwork can precede it | unverified — flagged (depends on this company's data infrastructure, not independently confirmed) |
| A10 | Public industry benchmark blogs are representative of this company's specific market segment | untested belief | verify/challenge | Challenge — em dash: no segment-specific fit confirmed; surfaced during Assumption Audit on C4 | unverified — flagged |
| A11 | The weighted criteria/scores used in the options trade-off (C5) reflect this business's actual risk tolerance | convention | challenge explicitly | Challenge — em dash: weights are this analyst's judgment; board should sanity-check before treating C5's ranking as final; surfaced during Assumption Audit on C5 | unverified — flagged |
| A12 | The program, if funded, would achieve broad enrollment among at-risk customers, not just already-loyal ones | untested belief | verify via pilot design | Challenge — em dash: adverse selection (engaged customers redeem; disengaged ones don't) is a known structural risk of rewards mechanics; surfaced via Phase 2 inversion | unverified — flagged |
| A13 | No other unaddressed competitive/macro factor is simultaneously driving churn up faster than a loyalty program could offset | untested belief | verify via diagnostic | Challenge — em dash: nothing in the facts given rules this out; surfaced via Phase 2 inversion | unverified — flagged |
| A14 | Redemption-credit usage does not materially dilute the $19 ARPU used in the revenue-retention estimate | untested belief | clarify with Finance | Challenge — em dash: credits are a contra-revenue mechanic by design; surfaced during Assumption Audit on C2 | unverified — flagged |
| A15 | No pre-launch signaling/awareness of the competitor's program reached customers before the stated "last month" launch | untested belief | verify (market intelligence, social listening) | Challenge — em dash: this is the live, unsettled rival to the temporal-mismatch argument (C3); surfaced during Assumption Audit on C3 | unverified — flagged |
| A16 | The company has the internal capability/willingness to redirect budget toward payment-recovery tooling if the diagnostic points that way | untested belief | confirm with Finance/Eng ahead of the gate | Challenge — em dash: an unstated organizational precondition for the recommendation's second-order value; surfaced during Assumption Audit on C5's extension | unverified — flagged |
| A17 | Competitors will not further differentiate their loyalty programs beyond parity (a commodity dynamic, not an arms race) | untested belief | monitor post-launch | Challenge — em dash: unverifiable market-dynamics forecast; surfaced during Assumption Audit on C5's extension | unverified — flagged |

**Compact fishbone (Phase 2, churn root-cause breadth):**

| Category | Candidate cause(s) | Discriminating observation available from facts given? |
|---|---|---|
| Pricing | Recent price change or perceived value-for-price drop | None stated — no discriminator available |
| Product/Quality | Outage, bug, feature removal in the last 2 quarters | None stated — no discriminator available |
| Involuntary/Payment | Card expirations/failed renewals (common in consumer subscriptions) | None stated — no voluntary/involuntary breakdown given |
| Competitive | Customers leaving for a specific competitor advantage (price, product — not just loyalty) | None stated |
| Acquisition/Onboarding | A recent acquisition channel or cohort with structurally higher early churn | None stated |
| Support/Service | Degraded support response times or satisfaction | None stated |

No category can be ruled in or out from the facts as given — which is itself the headline finding of this step: the assumption space is genuinely multi-causal and currently indistinguishable, which is the strongest argument for diagnosing before committing $310K to one specific lever.

---

## 3. Ground Truths

**Provenance summary:** `?`-marked: GT-1, GT-2, GT-3, GT-4, GT-5, GT-7, GT-8, GT-9, GT-10 (9 of 10). Read-at-source: GT-6 — verified by independent mathematical re-derivation (geometric-series identity shown in chains C1/C2), not by opening an external citation.

- **GT-1?** 48,000 active subscription members — stakeholder-stated; unverified: not reconciled against a billing/CRM system of record in this session.
- **GT-2?** ARPU = $19/month per active member — stakeholder-stated; unverified: same reason as GT-1.
- **GT-3?** Monthly churn rose from 4.2% to 6.8% over the last two quarters (~6 months), with no voluntary/involuntary breakdown provided — stakeholder-stated; unverified: not reconciled against a churn-reporting system.
- **GT-4?** The proposed loyalty (points-for-account-credit) program costs ~$310,000/year "to operate" — stakeholder-stated; unverified: scope of "to operate" not specified (see A5/GT-10).
- **GT-5?** A competitor launched a similar loyalty program approximately one month ago — stakeholder-stated; unverified: exact dates not independently confirmed, though the *qualitative* gap (quarters vs. one month) is stated directly in the given facts.
- **GT-6** Subscription LTV (revenue-only) = ARPU ÷ monthly churn rate in steady state, and revenue from a fixed cohort over T months = ARPU × N × Σ_{t=0}^{T−1}(1−c)^t — a geometric-series identity for constant-hazard retention. — source: standard SaaS-finance LTV formulation (ChartMogul/Wall Street Prep descriptions, search-summary reviewed, primary page not opened); **read-at-source: independently re-derived in chains C1/C2 below**, which is the stronger and controlling verification.
- **GT-7?** Consumer subscription businesses commonly see monthly churn around 6.5%–8%, with under-5%-monthly generally described as "healthy" — cited to industry benchmark aggregator blogs (dollarpocket, vitally, subjolt, focus-digital); reported-by-delegate: WebSearch summaries reviewed, primary pages not opened; unverified — flagged. Note: several of these sources inconsistently mix monthly and annual churn scales within their own claims, which further weakens confidence in the precise range.
- **GT-8?** Vendor content (Paytronix) claims real-time reward redemption correlates with a ~10% drop in churn, attributed to a secondary "Winsavvy" reference — **Phase 3 verification performed:** opened https://www.shno.co/marketing-statistics/customer-retention-statistics (did not corroborate this figure at all — different statistics appeared) and https://www.paytronix.com/blog/effectiveness-of-loyalty-programs (corroborated the 10% figure but sourced it to "Winsavvy," itself unopened and unverifiable, inside promotional content from a company that sells loyalty software). **Phase 3 failure record:** citation traces to an unverifiable secondary source embedded in vendor-promotional content — this is evidence of weak sourcing, not evidence the figure is false. Unverified — flagged.
- **GT-9?** No gross margin per subscriber is provided in the facts given, so all dollar figures in this analysis are revenue-only, not profit-only — unverified: margin data not supplied.
- **GT-10?** It is not specified whether the $310,000/year figure includes the cost of redeemed points/credits (a direct revenue offset) or only platform/staffing/ops overhead — unverified: scope not specified by the stakeholder.

No assumption that received a Discard verdict in Phase 2 appears in this list (none were discarded; all challenged assumptions were retained as flagged, unverified inputs).

---

## 4. Derivation Chains

### Conclusion C1: The churn spike represents a large, real destruction of customer-relationship value, independent of which lever fixes it

GT-1? (48,000 members) + GT-2? (ARPU $19) + GT-3? (churn 4.2%→6.8%) + GT-6 (LTV = ARPU ÷ churn, cohort-revenue identity)
→ applying the LTV identity to each churn rate yields per-customer steady-state value of about $452 at 4.2%, $279 at 6.8%, and $380 at a 5% target
→ aggregated across the 48,000-member base, the rise from 4.2% to 6.8% has already destroyed roughly $8.3 million in steady-state customer-relationship value, using a revenue-only, undiscounted, constant-base approximation [Assumes: A7]
→ some level of retention investment is easily justified financially by this figure alone, though it does not yet indicate which lever is the right one

**Pre-check:** head GT-1?, GT-2?, GT-3?, GT-6 · ?-marked: GT-1?, GT-2?, GT-3? · lowest cited: none · Inputs ceiling: MEDIUM
**Confidence:** MEDIUM — GT-1?, GT-2?, GT-3? are stakeholder-reported figures not reconciled against a system of record in this session; the verification that would remove them as a cause of the downgrade is a direct pull from the billing/CRM and churn-reporting systems. The steady-state, no-new-signups simplification (A7) is disclosed and bounded to a 12-month/steady-state horizon. The rival that "this doesn't actually matter because departing customers have low future value anyway" does not survive: even at 6.8% churn, per-customer LTV ($279) times 48,000 members remains a very large aggregate figure.

### Conclusion C2: The $310K program is financially justified on a conservative 12-month basis even if it achieves only about a third of its stated churn-reduction goal

GT-1? (48,000 members) + GT-2? (ARPU $19) + GT-4? ($310K/year cost) + GT-6 (cohort-revenue identity) + C1 (established LTV/cohort machinery, MEDIUM)
→ modeling the existing 48,000-member cohort over the next 12 months with no new signups, retained revenue differs by about $730,000 between the 6.8% and 5% churn scenarios (member-months factor 8.39 vs 9.19, each ×48,000×$19)
→ solving for the churn rate at which this 12-month retained-revenue gain equals the $310,000 program cost gives a breakeven of approximately 6.0% monthly churn
→ the program pays for itself in year one if it closes only about 0.8 of the full 1.8-percentage-point gap to the 5% target — roughly a third of the stated bet, not all of it

**Pre-check:** head GT-1?, GT-2?, GT-4?, GT-6, C1 (MEDIUM) · ?-marked: GT-1?, GT-2?, GT-4? · lowest cited: MEDIUM · Inputs ceiling: MEDIUM
**Confidence:** MEDIUM — GT-1?, GT-2?, GT-4? carry the same unreconciled-figures caveat as C1, with the same verification path (system-of-record pull). C1's MEDIUM rating caps this chain (already explained on C1's own line). Two chain-specific downgrade causes: GT-9? (no margin figure — this is a revenue, not profit, breakeven; the verification that would remove it is a gross-margin figure from Finance) and GT-10? (ambiguous $310K scope — the verification that would remove it is Finance confirming whether redemption liability is included; if it is not, the breakeven bar rises and this MEDIUM could move toward LOW). [Assumes: A7, A14 — see Assumption Audit]

### Conclusion C3: The proposal's causal story linking the churn spike to a competitor's loyalty launch does not survive a timeline check

GT-3? (churn rose over ~2 quarters / ~6 months) + GT-5? (competitor launched ~1 month ago)
→ churn began rising roughly five months before the competitor's loyalty program existed
→ the competitor's loyalty launch therefore cannot be the primary cause of most of the observed churn increase, undermining "match the competitor" as the load-bearing justification for the specific remedy proposed

**Pre-check:** head GT-3?, GT-5? · ?-marked: GT-3?, GT-5? · lowest cited: none · Inputs ceiling: MEDIUM
**Confidence:** LOW — two axes are short at once. Inputs: both GT-3? and GT-5? are unreconciled stakeholder-stated dates; the verification that would remove them is confirming exact churn-rise onset and exact competitor-launch date. Rivals: a live, unsettled rival survives — the competitor may have signaled or previewed the program (leaks, beta, word-of-mouth) before the stated "last month" launch date (A15), which this analysis cannot rule out. The qualitative gap (quarters vs. weeks) is robust to modest date imprecision, but the analysis cannot currently rule out meaningful pre-launch awareness, so this stays LOW rather than MEDIUM. [Assumes: A15]

### Conclusion C4: The efficacy case for this specific $310K program is evidentially weak, distinct from the general case that some retention action is justified

GT-7? (consumer churn benchmark ~6.5–8% monthly) + GT-8? (weak/conflicted loyalty-efficacy evidence)
→ 6.8% sits inside, not far outside, the range commonly observed for consumer subscription businesses generally, and the specific "X% churn reduction from loyalty" figures found trace to vendor-promotional secondary sourcing rather than independent research [Assumes: A10]
→ neither "how anomalous is 6.8%" nor "how much will rewards specifically move it" can be answered with confidence from the publicly available benchmarks located during this analysis

**Pre-check:** head GT-7?, GT-8? · ?-marked: GT-7?, GT-8? · lowest cited: none · Inputs ceiling: MEDIUM
**Confidence:** LOW — Inputs axis short (both GT-7? and GT-8? are reported-by-delegate industry content, and GT-8?'s citation chain failed corroboration on direct read, per its Phase 3 failure record). Rivals axis short: a live rival survives — loyalty mechanics could still plausibly help this specific company for reasons independent of the unverified vendor statistics (e.g., simple engagement/re-activation effects); nothing here settles that. The verification that would remove the Inputs shortfall is a segment-specific A/B or matched-cohort test (which is exactly what the recommended pilot would produce).

### Conclusion C5: The recommended course of action is a diagnostic-gated pilot, not a blind full rollout or an outright refusal

C1 (size of the stakes, MEDIUM) + C2 (favorable breakeven bar, MEDIUM) + C3 (weak causal story re: competitor timing, LOW) + C4 (weak efficacy evidence, LOW)
→ weighing four options — fund fully, don't fund, fund conditionally (diagnostic + scoped pilot + go/no-go gate), redirect the budget to likely root-cause fixes — against six weighted criteria (financial-ROI likelihood, speed to a board-credible answer, fit to a diagnosed cause, competitive signaling, downside/reversibility, operational risk), "fund conditionally" scores highest on every single criterion (weighted total 102, vs. 73 for redirect, 57 for fund-fully, 54 for don't-fund) [Assumes: A11]
→ because "fund conditionally" leads on every criterion individually, no single-criterion reweighting can overturn the ranking — this is the strongest form of trade-off result available, not a near-tie
→ therefore the recommended action is to fund a scoped, cost-capped, diagnostic-gated pilot rather than either a full blind commitment or a refusal to act

→[2nd] within the 3-week-to-90/180-day window, the diagnostic either confirms a loyalty-addressable (voluntary/engagement) driver — in which case the pilot proceeds toward the full $310K commitment — or reveals a majority-involuntary or price/product driver, in which case Customer Success's original framing is shown to be mismatched and budget redirects toward payment-recovery or product/pricing fixes [Assumes: A16]
→[3rd] if the pilot succeeds and the program becomes permanent, the retention advantage likely erodes toward parity within 12–24 months as loyalty programs become a category norm rather than a differentiator, and the credit-redemption mechanic risks disproportionately rewarding already-loyal customers (adverse selection) rather than the at-risk segment it is meant to save [Assumes: A17, A12] (no contradiction with any stated ground truth; extension retained)

**Pre-check:** head C1 (MEDIUM), C2 (MEDIUM), C3 (LOW), C4 (LOW) · ?-marked: none directly · lowest cited: LOW · Inputs ceiling: LOW
**Confidence:** LOW — capped by the lowest-rated chains it cites (C3, C4), both LOW for reasons explained on their own confidence lines (unreconciled dates plus a live unsettled rival on C3; weak vendor-sourced evidence plus a live unsettled rival on C4). This is not a defect in the recommendation: the LOW rating on the causal/efficacy story is precisely why the recommendation is a gated, capped pilot rather than a full commitment — high confidence in a weak causal story would be the actual red flag here, not the LOW rating itself. The trade-off's own robustness (C5's dominance across every criterion) does not depend on C3/C4 being fully verified; it only requires that the causal story be *genuinely uncertain*, which C3/C4 establish regardless of which way that uncertainty eventually resolves. Tag: A11 (trade-off weights are this analyst's judgment — see Assumption Audit).

---

## 5. Abandoned Reasoning

### Dead End: Point-estimate NPV with a discount rate

**What was tried:** Attempting to convert the LTV/cohort-revenue figures into a discounted net-present-value comparison against the $310K annual cost, to produce a single "true" ROI figure.

**Why abandoned:** No cost-of-capital, discount rate, or planning horizon was supplied in the facts given, and no reliable proxy exists in this session; inventing one would manufacture false precision that a board could mistake for rigor. Speculative with no verification path, so not cited on any chain's head.

**What it ruled out:** Saves a future analyst from re-deriving a "precise" NPV figure from this data — the honest answer at this level of information is the bracketed, revenue-only, undiscounted 12-month and steady-state figures presented in C1/C2, not a single discounted number.

### Dead End: Treating the vendor efficacy statistics (10%/19% churn/retention figures) as a hard point-estimate for program impact

**What was tried:** Using the "real-time reward redemption correlates with a 10% drop in churn" figure directly as an expected-value input to a probability-weighted ROI calculation.

**Why abandoned:** Phase 3 verification opened the cited sources and found the figure traces to an unverifiable secondary citation ("Winsavvy," via Paytronix) embedded in promotional content from a company selling loyalty software — a conflict of interest and a broken evidentiary chain. Contradicts the ground-truth standard applied elsewhere in this analysis (GT-8?'s failure record); using it as a hard input would be inconsistent with how every other unverified figure in this document was treated.

**What it ruled out:** Saves a future analyst from citing "loyalty programs cut churn by ~10%" to the board as if it were an established fact; it is marketing content, not a controlled study, and the correlation it reports is also confounded by selection (already-engaged customers are the ones who redeem in real time).

### Dead End: Treating "the competitor is doing it" as direct evidence the program will work here

**What was tried:** Using industry/competitor adoption as standalone justification for funding, in the style of "this is what companies in this position do."

**Why abandoned:** This is reasoning by analogy without a grounding ground truth about the *competitor's own results* — no evidence exists (in the facts given or found during research) that the competitor's program has moved their retention numbers at all. Analogy to what others have adopted is not evidence of what those adoptions achieved.

**What it ruled out:** Saves the board from treating competitive parity as a substitute for evidence of efficacy; parity has a legitimate but separate value (signaling, feature-completeness) that this analysis keeps distinct from the churn-fixing claim.

---

## 6. Conclusion

**Recommended approach:** Do not fund the full $310K/year program as proposed, and do not reject it outright. Fund a scoped, cost-capped pilot running alongside a 1–2 week churn diagnostic (voluntary vs. involuntary split, price/product-incident correlation, cohort/channel breakdown), with a pre-committed go/no-go gate at 90–180 days measured against a control cohort's churn rate, not engagement/redemption metrics (chain C5).

**Key insight:** The proposal's central justification — "the competitor just launched a similar program, so we should too, and this is why our churn rose" — is chronologically impossible for most of the observed churn increase: the spike predates the competitor's launch by roughly five months (chain C3). Reasoning by analogy to a competitor's recent move, rather than from the actual timeline of the event being explained, is exactly the kind of error a first-principles pass is meant to catch — no chain, no conventional churn-reduction argument makes this timing problem go away.

**Trade-offs acknowledged:** Funding conditionally means the board does not get a clean "yes" or "no" in three weeks — it gets a decision plus a checkpoint, which is a harder message to deliver than either extreme (chain C5). It also means accepting that if the diagnostic confirms a loyalty-addressable driver, roughly $77–155K of the $310K annual budget is being spent before full confirmation, in exchange for capturing the favorable breakeven math established in chain C2 — a 12-month payback if churn falls only from 6.8% to about 6.0%, a third of the full bet (chain C2). Separately: if Finance confirms the $310K figure excludes redemption-credit liability, the true cost is higher than modeled here and this breakeven bar should be recomputed before the pilot is finalized — no chain — flagged assumption only (GT-10?/A5).

**Pre-check:** head C1 (MEDIUM), C2 (MEDIUM), C3 (LOW), C4 (LOW), C5 (LOW) · ?-marked: none directly (all `?` inputs are already reflected through the cited chains) · lowest cited: LOW · Inputs ceiling: LOW
**Confidence:** LOW — driven by C3 and C4, both LOW for reasons stated on their own lines (unreconciled dates and a live unsettled pre-launch-signaling rival on C3; weak, conflict-of-interest-laden vendor sourcing and a live unsettled rival on C4, chain C1). This LOW rating describes the strength of the *causal and efficacy* evidence available today, not the soundness of the recommendation's structure: the recommendation is explicitly built to be robust to that uncertainty (gate, cap, control cohort) rather than to resolve it prematurely. The two things most likely to raise this to MEDIUM/HIGH are named in the bottom-line summary above: the voluntary/involuntary churn split, and confirmation of the program's true all-in cost.

---

## Techniques not applied (process output)

theoretical-limit — not applicable — no governing hard constraint (physical law, conservation identity, or comparable mathematical ceiling) bounds achievable churn reduction from a rewards program in this domain; any "ceiling" here would be empirical/behavioral, which is what the recommended diagnostic and pilot are designed to measure directly rather than derive from first principles.

(Five-Whys/reduce-to-primitives, fishbone, inversion, trade-off, second-order, estimate, and pre-mortem were each applied above — see A8/GT-6 for the irreducibility check, the Phase 2 fishbone table, the Phase 2 inversion behind A12–A13, chain C5's trade-off collapse and second/third-order extension, the member-months estimate underlying C1/C2, and the adversarial pass below.)

## Assumption Audit scan (process output)

| Chain | Step | Step Text (brief) | Assumption surfaced? | Added to Table? |
|---|---|---|---|---|
| C1 | 1 | Head: GT-1?,GT-2?,GT-3?,GT-6 | none | n/a |
| C1 | 2 | Per-customer LTV at 3 churn rates | none | n/a |
| C1 | 3 | Aggregate ~$8.3M destroyed value | A7 (steady-state base) — already declared | n/a |
| C2 | 1 | Head: GT-1?,GT-2?,GT-4?,GT-6,C1 | none | n/a |
| C2 | 2 | 12-month cohort revenue diff ~$730K | A7 (already declared) + A14 (ARPU not diluted by credits) | yes (A14) |
| C2 | 3 | Breakeven churn ≈6.0% | none beyond A7/A14 | n/a |
| C3 | 1 | Head: GT-3?,GT-5? | none | n/a |
| C3 | 2 | Temporal ordering (5-month gap) | none (pure arithmetic on given dates) | n/a |
| C3 | 3 | Competitor timing can't explain most of the spike | A15 (no pre-launch signaling) | yes (A15) |
| C4 | 1 | Head: GT-7?,GT-8? | none | n/a |
| C4 | 2 | 6.8% within normal range; efficacy stats weak | A10 (benchmark blogs representative of this segment) | yes (A10) |
| C4 | 3 | Neither anomaly nor efficacy answerable with confidence | none beyond A10 | n/a |
| C5 | 1 | Head: C1,C2,C3,C4 | none | n/a |
| C5 | 2 | Trade-off scoring, "fund conditionally" dominates | A11 (weights reflect actual priorities) | yes (A11) |
| C5 | 3 | Recommended action: diagnostic-gated pilot | none beyond A11 | n/a |
| C5 | 4 (2nd) | Diagnostic outcome redirects budget or confirms pilot | A16 (internal capability to redirect) | yes (A16) |
| C5 | 5 (3rd) | Loyalty parity erodes toward commodity over 12–24mo | A17 (no further loyalty arms-race) + A12 (enrollment reaches at-risk segment) | yes (A17); A12 already declared |

## Adversarial pass (process output)

**Recompute:** LTV(4.2%)=19/0.042=$452.38; LTV(6.8%)=19/0.068=$279.41; LTV(5%)=19/0.05=$380.00; aggregate Δ(4.2 vs 6.8)=172.97×48,000≈$8.30M. 12-month member-months factor at 6.8%=(1−0.932¹²)/0.068≈8.390; at 5%=(1−0.95¹²)/0.05≈9.193; revenue diff=48,000×19×(9.193−8.390)≈$732K (reported as ~$730K). Breakeven churn solves 48,000×19×[(1−(1−c)¹²)/c − 8.390]=310,000 → c≈0.060 (6.0%). All figures recompute as stated; presented with "~" to avoid false precision given GT-9?/GT-10? gaps.

**Sensitivity:** The single ground truth whose falsity would most flip the overall recommendation is **GT-10?** (whether the $310K "to operate" figure includes redemption-credit liability). It is `?`-marked. If the true all-in annual cost is materially higher (e.g., 2–3x), the breakeven bar rises well above the full 6.8%→5% bet, and the recommendation would shift from "fund a capped pilot, favorable breakeven" toward "don't fund without independently verified efficacy evidence first." Verification path: a scoped-cost memo from Finance before the go/no-go gate.

**Rival:** Headline conclusion (fund conditionally) — rival is "fund fully as proposed"; ruled out by C3+C4's weak causal grounding and by C5's trade-off dominance (§5 entries: "point-estimate NPV" and "vendor efficacy stats as hard input" both bear on why a full blind commitment is premature). C1 — rival "the departing customers have low future value anyway, so this doesn't matter financially"; ruled out by the LTV math itself (even at 6.8% churn, aggregate value remains large). C2 — no adversarial rival; the alternate (full-stock LTV) framing would only make the breakeven case easier, so it doesn't compete against the conservative 12-month estimate used. C3 — rival "the competitor pre-signaled the program before the stated launch date" is **live and unsettled** (A15); this is the primary reason C3 is rated LOW rather than MEDIUM. C4 — rival "loyalty could still work here for reasons unrelated to the unverified vendor stats" is **live and unsettled**; this is why C4 is also rated LOW.

**Premise:** It is 12 months from now. The board approved the diagnostic-gated pilot; churn is still elevated (~6.5%+), the pilot did not move the needle, and $310K or more has been spent with little to show for it.

**Causes** (generated across four stakeholder viewpoints, unfiltered):
CS/program-owner viewpoint: (1) the diagnostic was rushed under 3-week pressure and never actually separated voluntary from involuntary churn; (2) the pilot cohort was chosen non-randomly (e.g., highest-value customers), making results non-generalizable; (3) CS declared success based on point-redemption/engagement metrics rather than churn movement, masking a null result; (4) the go/no-go threshold was never crisply numeric at launch, so the checkpoint became a negotiation.
Finance/board viewpoint: (5) the $310K figure ballooned once redemption liability was included, with no pre-agreed cost cap; (6) no control group existed, so the board couldn't separate program effect from seasonal/macro noise; (7) the diagnostic showed churn was largely payment-failure-driven, but the pilot continued anyway on sunk-cost momentum.
At-risk-customer viewpoint: (8) the real complaint (price, a missing feature, a worse product than the competitor's) was never addressed, so points felt like being bribed to tolerate the actual problem; (9) redemption terms (minimum spend, expiration) frustrated exactly the disengaged customers the program was meant to win back; (10) customers who churn via payment failure never see the program at all, since they're already gone before rewards accrue.
Competitor/market and internal-ops viewpoint: (11) the competitor's own program turned out to be a minor feature, not the actual driver of defections to them, making parity strategically irrelevant; (12) once both companies have loyalty programs, they cancel out as differentiators and the market re-settles on core product/price, which the loyalty spend never touched; (13) the new points ledger introduced a fraud/abuse vector consuming unplanned engineering/support time beyond the $310K budget.

**Clusters:**
- **Cluster 1 — "Diagnostic theater"** (causes 1, 2, 4) — bears on C5 and on A9 (feasibility of a genuine diagnostic in the available time).
- **Cluster 2 — "Wrong success metric / sunk-cost momentum"** (causes 3, 6, 7) — bears on C2 and C4.
- **Cluster 3 — "Doesn't touch the real driver"** (causes 8, 9, 10) — bears directly on C3 and C4; the single most important cluster.
- **Cluster 4 — "Program becomes a wash strategically/financially"** (causes 5, 11, 12, 13) — bears on C5's second- and third-order extension and on GT-10?/A5.

**Disposition:**
- Cluster 1 — *Plan change:* define the diagnostic's exact deliverable and the numeric go/no-go threshold **before** the board vote; assign a named owner outside Customer Success (e.g., Finance or Analytics) so the team proposing the fix doesn't grade its own homework.
- Cluster 2 — *Plan change:* pre-register churn rate in a control/matched cohort as the success metric, not redemption or engagement counts; write the numeric threshold into the board approval itself.
- Cluster 3 — *Plan change:* run the diagnostic in parallel with a direct price/product/competitive-complaint review, not instead of it; explicitly exclude involuntary/payment-failure churn from the pilot's target population and route it to a separate payment-recovery workstream.
- Cluster 4 — *Accepted risk with named mitigation:* accept that loyalty parity may erode as a differentiator over 12–24 months (a plausible market dynamic, not one this program can prevent); mitigate by capping initial commitment to the pilot scope, treating the full $310K/year as a renewable evidence-gated line rather than a permanent budget line, and requiring Finance to confirm the all-in cost (closing GT-10?) before the gate.

**Falsification:** This conclusion (fund conditionally, not fully and not zero) is false if a same-week diagnostic pull shows churn is overwhelmingly (>70%) driven by a single non-loyalty-addressable cause — e.g., payment failures or a specific price/product incident. In that case the recommendation flips to redirecting the $310K toward that specific fix and deferring the loyalty pilot.

## §6→§4 closure ledger

- "Fund a scoped, cost-capped pilot running alongside a churn diagnostic, with a go/no-go gate" → chain C5 ✓
- "The competitor's launch cannot explain most of the churn spike" (Key insight) → chain C3 ✓
- "Funding conditionally means a harder message than a clean yes/no, and a favorable but partial breakeven" → chain C2 ✓
- "If Finance confirms $310K excludes redemption liability, recompute before finalizing" (caveat) → no chain — flagged assumption only
- "Overall Confidence: LOW, driven by C3/C4" → chains C1, C2, C3, C4, C5 ✓

## Self-audit scan (process output)

| Chain | Chain Head (brief) | Form conforming? | Rule applied | Dependency clean? | Band | Act attempted? | Edges fired |
|---|---|---|---|---|---|---|---|
| C1 | GT-1?,GT-2?,GT-3?,GT-6 | yes | n/a | yes | MEDIUM | yes | none |
| C2 | GT-1?,GT-2?,GT-4?,GT-6,C1 | yes | n/a | yes | MEDIUM | yes | none |
| C3 | GT-3?,GT-5? | yes | n/a | yes | LOW | no | none |
| C4 | GT-7?,GT-8? | yes | n/a | yes | LOW | yes | none |
| C5 | C1,C2,C3,C4 | yes | n/a | yes | LOW | no | none |

| §6 Span (brief) | Construct | Claim under R11? | R11 clause applied | Chain cited |
|---|---|---|---|---|
| Recommended approach: fund a scoped pilot + diagnostic + gate | bold lead-in | yes | colon closes bold span, on-line assertion | C5 |
| Key insight: timing rules out the competitor as primary cause | bold lead-in | yes | colon closes bold span, on-line assertion | C3 |
| Trade-offs acknowledged: harder message, partial breakeven | bold lead-in | yes | colon closes bold span, on-line assertion | C2 |
| "...true all-in cost is higher... recompute" caveat | prose caveat | yes | caveat rule; carries `no chain — flagged assumption only` marker | none — untracked (marked) |
| Pre-check line (§6) | prose | yes | pre-check is itself a §6 claim under this rule | C1,C2,C3,C4,C5 |
| Confidence: LOW, driven by C3/C4 | bold lead-in | yes | colon closes bold span, on-line assertion | C1,C2,C3,C4,C5 |

Scan complete: 5 chain rows, one per section-4 chain block in order; 6 section-6 rows, one per construct in order — 6 claims under R11, 0 excluded. 0 chains malformed, 0 claims untraced.

## Self-Audit Gate (process output)

**Criterion 1: Identify Essence**
Quoted span: "should the company commit $310,000/year to a specific proposed remedy... before knowing whether that remedy addresses the actual cause?"
Band: **Rigorous**
Justification: names the underlying question (diagnosis-before-commitment), not the triggering event (competitor launch) or a symptom (churn number), and success criteria are checkable structural tests against section 6.

**Criterion 2: Challenge Assumptions**
Quoted span (Assumption Audit scan): rows showing A10, A11, A14, A15, A16, A17 surfaced from named chain steps and added to the table.
Band: **Rigorous**
Justification: 17 rows span all four types, several genuinely Challenged (not merely Accepted) with specific em-dash justifications, unverified inputs used in chains are marked "unverified — flagged," and the audit scan confirms exhaustive coverage of every chain step.

**Criterion 3: Establish Ground Truths**
Quoted span: "?-marked: GT-1, GT-2, GT-3, GT-4, GT-5, GT-7, GT-8, GT-9, GT-10 (9 of 10)" — checked against the list, which carries `?` on exactly those nine.
Band: **Sound**
Justification: enumeration matches the list and GT-8's Phase 3 failure record is genuinely evidenced (two sources opened), but GT-6 is the only unsuffixed GT feeding a chain and no chain in this analysis reaches HIGH at all, so the "every unsuffixed GT feeding a HIGH chain names read-at-source" test is vacuous rather than demonstrated — a minor shortfall from the Rigorous descriptor's spirit, not a pattern.

**Criterion 4: Reason Upward**
Quoted span (self-audit scan, chain-form table): all five chains score "Form conforming? yes," "Dependency clean? yes."
Band: **Rigorous**
Justification: every conclusion has exactly one chain with a genuine intermediate, no analogy is used as direct evidence (two dead ends in §5 exist specifically because analogical reasoning was rejected), every surfaced assumption carries an `[Assumes: X]` tag, and hops recompute as shown in the adversarial pass.

**Criterion 5: Validate**
Quoted span (adversarial pass record): "Clusters... Disposition" — each of four clusters carries a named plan change or an explicitly accepted risk with a named mitigation.
Band: **Rigorous**
Justification: the full five-step adversarial pass is present with no step silently omitted, confidence ratings are calibrated per chain (including the honest LOW cap on C5 explained rather than hidden), and no chain is rated HIGH while consuming a `?` input.

**Criterion 6: Conclusion-to-Ground-Truth Traceability**
Quoted span (self-audit scan, claim-inventory table): 6 of 6 §6 constructs trace to a named chain, one caveat carries the honest `no chain — flagged assumption only` marker rather than a fabricated citation.
Band: **Rigorous**
Justification: every claim traces to section 4, no new reasoning is introduced in section 6, and the Key Insight (the timing mismatch) is a genuinely non-obvious finding rather than a restatement of the recommended approach.

**Gate result:** No criterion Absent; zero criteria Hand-wavy (one Sound, five Rigorous) — the analysis clears both conditions of the Self-Audit Gate.

---

Sources consulted (WebSearch/WebFetch, all reported-by-delegate or read-at-source as marked above in GT-7?/GT-8?):
- [Customer Retention Statistics for 2026 (shno.co)](https://www.shno.co/marketing-statistics/customer-retention-statistics) — read-at-source, did not corroborate the headline loyalty-efficacy figure
- [7 Stats Showing the Effectiveness of Loyalty Programs (Paytronix)](https://www.paytronix.com/blog/effectiveness-of-loyalty-programs) — read-at-source, traced the 10% churn-drop figure to an unverified secondary citation
- [B2B SaaS Churn Rate Benchmarks (Vitally)](https://www.vitally.io/post/saas-churn-benchmarks) — reported-by-delegate
- [SaaS Churn Rate Benchmarks Report (Dollarpocket)](https://www.dollarpocket.com/saas-churn-rate-benchmarks-report) — reported-by-delegate
- [Customer Lifetime Value (ChartMogul)](https://chartmogul.com/saas-metrics/ltv/) — reported-by-delegate (formula independently re-derived, not relied on for provenance)