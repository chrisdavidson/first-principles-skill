# Recommendation (for the board)

**Don't fund the $310K/year loyalty program as proposed. Fund a capped pilot (~$40–60K) plus an immediate root-cause diagnostic instead, and bring the full-year decision back in 60–90 days with real data.**

Why: the churn spike predates the rival's loyalty launch by five of its six months, so the rival's program can't be the dominant cause and this program isn't a proven fix for the actual driver — which is currently unknown. The arithmetic *could* justify $310K if the program works exactly as claimed, instantly and at full strength — but realistic ramp-up, an unquantified redemption-liability cost, and likely adverse selection (rewarding members who'd have stayed anyway) put the real year-one payoff in a range that straddles the cost, not clearly above it. A blind full-year commit is a bet with no control group; a capped, randomized pilot answers the actual question inside the three-week window without giving up a full year of spend on an unverified causal claim.

Full analysis follows.

---

## 1. Problem Essence

**Core problem:** Should the company commit ~$310,000/year, on a three-week decision clock, to a loyalty/points program whose success depends on an unverified causal claim — that it is *this specific intervention*, rather than something else (price, product, onboarding, support, seasonality, cohort effects, or reversion to the mean), that will pull monthly churn from 6.8% back toward ~5%?

**Success criteria** (checkable directly against Section 6):
1. The Conclusion states whether the loyalty program addresses the churn increase's actual driver or only a downstream symptom.
2. The Conclusion states a quantified breakeven bar (in dollars and in churn-points) and compares it explicitly to the claimed 1.8-point reduction.
3. The Conclusion names at least one concrete mechanism by which the program could fail to move churn or actively backfire.
4. The Conclusion states how the rival's one-month-earlier launch changes the strategic framing (differentiator vs. defensive parity).
5. The Conclusion gives one clear call — fund / fund conditionally / don't fund — plus a test design executable inside the three-week window.

---

## 2. Assumptions Table

| # | Assumption | Type | Treatment | Verdict | Verification |
|---|---|---|---|---|---|
| 1 | The loyalty/points program will cause churn to fall toward 5% | untested belief | verify via controlled test | Challenge — this is the central hypothesis under evaluation, not yet tested | unverified — flagged (feeds C2/C3/C6) |
| 2 | The churn increase has a single, identifiable dominant cause | convention (CS narrative simplification) | challenge before use | Discard — no data supports a single-cause frame; multiple candidate drivers exist (price, product, onboarding, support, seasonality, cohort, competitive) | rejected on the absence of any root-cause data in the prompt |
| 3 | The rival's loyalty launch caused our churn spike | untested belief | verify | Discard — falsified by timing: rival's program has existed for only ~1 of the ~6 months over which churn rose | verified by date arithmetic on the prompt's own stated timeline (see GT-6) |
| 4 | Redemption participation will skew toward at-risk (about-to-churn) members | untested belief | verify/flag | Challenge — no targeting mechanism is described; default opt-in design more plausibly skews toward already-engaged members | unverified — flagged (feeds C4) |
| 5 | Customer lifetime behaves as a constant-hazard (geometric) process, so 1/churn ≈ average lifetime | convention/definition | apply with caveat | Accept — standard subscription-analytics approximation, used for the estimate; real hazard is likely front-loaded (new members churn faster), which this model doesn't capture | accepted as a modeling convention, not verified against this company's own survival curve (not provided) |
| 6 | Gross contribution margin is in the typical subscription 50–75% range | convention (industry-typical range) | challenge/flag | Challenge — no company-specific financial data given | unverified — flagged (feeds C2) |
| 7 | The stated $310,000/year cost is fully loaded, including projected redemption/account-credit liability | untested belief | verify | Challenge — ambiguous as stated | unverified — flagged (feeds C3); needs a direct question to CS/Finance before the board date |
| 8 | Three weeks is enough time to design and approve a test, not to observe a churn outcome | current constraint | accept, record expiry | Accept — expires once the pilot has run long enough to reach statistical power (likely 60–90 days beyond approval), not at the 3-week mark | standard fact about churn measurement timelines given monthly-granularity churn |
| 9 | A churn move back toward ~5% could happen anyway via reversion to the mean or seasonality, independent of the program | untested belief | verify via control group | Challenge — live risk; only a treatment/control design (not before/after) can rule this out | unverified — flagged (feeds C6, motivates the pilot design) |
| 10 | The churn-reduction effect applies to the existing 48,000-member base's ongoing risk, not only to newly acquired members | untested belief (surfaced in Assumption Audit, chain C2) | verify via pilot segment tracking | Challenge — reasonable default scope for a retention program, but not confirmed | unverified — flagged (feeds C2) |
| 11 | Program adoption/engagement in year one will be partial (ramp-up), not instant or universal | untested belief (surfaced in Assumption Audit, chain C3) | verify via pilot enrollment data | Accept as a modeling caveat — consistent with typical loyalty-program adoption curves, but no company-specific data exists | unverified — flagged (feeds C3) |
| 12 | A 40–60% realization haircut is a reasonable bound on year-one effect realization | untested belief (analyst judgment/estimate bracket, surfaced in Assumption Audit, chain C3) | flag as a bracketing choice, not a fact | Challenge — a judgment call used to bound the estimate, not a measured figure | unverified — flagged (feeds C3) |
| 13 | The proposed program design includes no explicit mechanism targeting at-risk members | untested belief (surfaced in Assumption Audit, chain C4) | verify with CS/product spec | Challenge — inferred from the absence of design detail in the proposal, not confirmed either way | unverified — flagged (feeds C4) |
| 14 | The broader member base increasingly perceives loyalty/points as a standard category feature after the rival's launch | convention (surfaced in Assumption Audit, chain C5) | challenge before use | Challenge — a single rival launch is thin evidence for "category normalization"; treated as a working hypothesis, not a verified trend | unverified — flagged (feeds C5) |
| 15 | A randomized pilot design and a root-cause data pull can both be scoped and approved within 3 weeks | current constraint / feasibility (surfaced in Assumption Audit, chain C6) | accept, record expiry | Accept — expires once the pilot moves from *design/approval* to full completion, which needs months beyond the 3-week board window | standard scoping fact: design and data-pull tasks are days-to-weeks efforts, not multi-month builds |

---

## 3. Ground Truths

- **GT-1** 48,000 active members × $19/month = $912,000/month ≈ $10.94M annual run-rate — source: user-stated problem parameters; read-at-source: "Situation" bullets 1 ("48,000 active members, $19/month")
- **GT-2** Monthly churn rose from 4.2% to 6.8% over the last two quarters (~6 months) — source: user-stated problem parameters; read-at-source: "Situation" bullet 2
- **GT-3** The proposed loyalty/points-for-credit program costs ~$310,000/year to run — source: user-stated problem parameters; read-at-source: "Situation" bullet 3
- **GT-4** The claim under evaluation is a reduction toward ~5% (not fully back to 4.2%) — source: user-stated problem parameters; read-at-source: "The bet/claim" bullet
- **GT-5** A rival service launched a similar loyalty/points program approximately one month before this decision — source: user-stated problem parameters, cross-checked against the session date (2026-09-27); read-at-source: "Context" bullet
- **GT-6** The rival's program has existed for only ~1 of the ~6 months over which churn rose (derived arithmetic on GT-2 + GT-5) — source: arithmetic on GT-2 and GT-5; read-at-source: direct computation from the two cited bullets, no external source needed
- **GT-7** Under a constant-hazard (geometric) churn model, expected average customer lifetime ≈ 1/monthly churn rate — source: standard subscription-analytics identity (definitional/mathematical); read-at-source: applied directly as a modeling convention, with the explicit caveat (Assumption 5) that real churn hazard is typically front-loaded rather than constant
- **GT-8** The board wants a final go/no-fund call within three weeks — source: user-stated problem parameters; read-at-source: "Constraint" bullet
- **GT-9?** Gross contribution margin on subscription revenue for this business is unknown — unverified: no financial/COGS data was provided
- **GT-10?** Whether the $310,000/year figure includes projected redemption/account-credit liability, or is administrative/platform cost only, is unspecified — unverified: the proposal as described does not state this
- **GT-11?** The root cause(s) of the churn increase (price, product/outages, onboarding, support, seasonality, cohort effects, competitive substitution) are not established by any data in the prompt — unverified: no diagnostic data (exit surveys, cohort breakdown, outage timeline, pricing history) has been run
- **GT-12?** The proposed design, as described ("members redeem points for account credit"), appears to be an undifferentiated opt-in mechanism with no stated targeting toward at-risk members — unverified: inferred from the absence of design detail, not confirmed with customer success

**Provenance summary:** `?`-marked: GT-9, GT-10, GT-11, GT-12 (4 of 12). Read-at-source: GT-1, GT-2, GT-3, GT-4, GT-5, GT-8 — each read directly from the user's own "Situation" bullets in this conversation (no external document exists to open); GT-6 — computed directly from GT-2 and GT-5's own stated figures; GT-7 — a standard mathematical identity applied as a modeling convention, not a citation-based fact. No assumption discarded in Phase 2 (Assumptions #2, #3) appears in this list.

---

## 4. Derivation Chains

### Conclusion C1: The rival's loyalty launch is not the dominant explanation for the churn spike

GT-2 (churn rose over ~6 months) + GT-5 (rival launched ~1 month ago) + GT-11? (root cause not established)
→ the rival's program overlaps only the most recent of the six months over which churn rose, so it cannot be the primary driver of the prior five months of increase
→ competitive substitution from the rival's program is a plausible contributor to at most the tail of the rise, not its bulk
→ the dominant driver of the churn increase is very likely a factor other than the rival's launch, and that factor is currently unidentified

**Confidence:** MEDIUM
GT-11? (root cause unestablished) is unverified — a rapid root-cause diagnostic (exit surveys, cohort/vintage breakdown, outage and pricing timeline correlation) would identify the actual dominant driver and could raise this to HIGH.

### Conclusion C2: If the claimed effect is realized in full, the program's idealized year-one value exceeds its cost

GT-1 (48,000 members at $19/month) + GT-7 (churn-to-lifetime identity) + GT-9? (margin unverified)
→ modeling the current 48,000-member cohort's runoff over 12 months at 6.8% versus 5.0% monthly churn yields roughly 43,800 additional member-months retained in year one, if the reduction is instant and fully sustained *[Assumes: the churn-reduction effect applies to the existing base's ongoing risk, not only to newly acquired members]*
→ at $19 per member-month that is approximately $833,000 of incremental pure revenue in year one before any margin is applied
→ applying an unverified 50-75% margin range brings margin-adjusted incremental contribution to roughly $415,000-$625,000, which exceeds the $310,000 program cost under this idealized scenario

**Confidence:** MEDIUM
GT-9? (gross contribution margin) is unverified — obtaining actual margin data from Finance would replace the range with a precise figure.

### Conclusion C3: Under realistic (not idealized) assumptions, year-one payback is genuinely uncertain

C2 (idealized margin-adjusted benefit of $415,000-$625,000) + GT-4 (claim is a return toward ~5%, not instant) + GT-10? (redemption-liability scope unresolved)
→ real loyalty programs ramp up through enrollment and partial engagement rather than an overnight step-function, so only a minority of the base typically engages meaningfully with a new points mechanic in its first year *[Assumes: year-one engagement is partial rather than immediate and complete]*
→ applying a realistic 40-60% realization haircut brings plausible year-one margin-adjusted benefit down to roughly $165,000-$375,000 *[Assumes: a 40-60% haircut is a reasonable bound on year-one realization]*
→ this range straddles the $310,000 cost, so the program's year-one payback is uncertain even if the churn claim is directionally correct, and turns negative once any unbudgeted redemption-liability cost is added on top

**Confidence:** LOW
GT-10? (redemption-liability scope) is unverified and GT-9? is inherited from C2; both a clarified cost scope from Finance and a completed pilot would raise this to at least MEDIUM.

### Conclusion C4: Absent targeting, program spend likely skews toward members who would have stayed anyway

GT-12? (undifferentiated opt-in design) + GT-4 (target is a minority segment, 1.8 of the 6.8 churn points)
→ an undifferentiated opt-in mechanism cannot structurally distinguish members who were going to churn from members who were always going to stay, so redemption activity will include members whose behavior the program never needed to change
→ the dollar cost of serving already-retained members is dead-weight spend that does not contribute to the claimed 1.8-point reduction, so C2's and C3's benefit estimates are best read as optimistic upper bounds rather than expected values *[Assumes: redemption participation is not restricted to or weighted toward members flagged as churn-risk]*

**Confidence:** LOW
GT-12? is an inference from the absence of a stated targeting mechanism, not a confirmed design detail — obtaining the actual program design spec from customer success would resolve this directly.

### Conclusion C5: The program is better framed as defensive parity than as a differentiated fix

GT-5 (rival launched first) + C1 (temporal mismatch limits attribution)
→ by the time this program could ship, the category will already have partly normalized loyalty points as a feature via the rival's head start, so the program functions more as defensive parity than as a differentiated churn-reversal lever *[Assumes: the broader member base increasingly perceives loyalty/points as a standard category feature]*
→ the funding decision should be sized and communicated to the board as a parity/defensive investment, with the primary churn-reversal effort directed at root-cause diagnosis in parallel, not as the single fix for the 6.8% churn rate

**Confidence:** MEDIUM
Inherits C1's MEDIUM rating (GT-11? unresolved root cause); resolving root cause would raise this to HIGH.

### Conclusion C6: The decision-ready move is a capped pilot plus root-cause diagnostic, not a blind full-year commit

C3 (uncertain, possibly sub-$310,000 realized benefit) + C4 (untargeted-spend risk) + GT-8 (3-week deadline)
→ committing the full $310,000 per year uncapped, on an unverified causal claim, an unverified margin figure, an unresolved redemption-cost scope, and an untargeted delivery mechanism, is not a decision-ready ask against the evidence available today
→ a capped pilot with a randomized treatment and control cohort, sized for statistical power and budgeted well below $310,000, run alongside an immediate root-cause diagnostic using data the company already holds, is achievable inside the three-week window as the board deliverable *[Assumes: a randomized pilot design and a root-cause data pull can both be scoped and approved within 3 weeks]*
→ the full-year funding decision should be deferred to a follow-up checkpoint once the pilot and diagnostic produce real causal and response data, rather than committed now on the strength of the loyalty hypothesis alone

**Confidence:** HIGH
This is a decision-under-uncertainty conclusion whose validity does not depend on which way GT-9?, GT-10?, or GT-12? ultimately resolve — it holds precisely because they are currently unresolved and the stakes ($310,000/year, ongoing) are high enough to warrant closing that gap before committing.

**End-of-phase Assumption Audit (process output):**

| Chain | Step | Step Text (brief) | Assumption surfaced? | Added to Table? |
|---|---|---|---|---|
| C1 | 1 (head) | GT-2+GT-5+GT-11? | none | n/a |
| C1 | 2 (hop1) | rival overlaps only 1 of 6 months | none (covered by #3) | n/a |
| C1 | 3 (hop2) | rival is at most a tail contributor | none (covered by #2) | n/a |
| C1 | 4 (hop3) | dominant driver is likely something else | none (covered by #2) | n/a |
| C2 | 1 (head) | GT-1+GT-7+GT-9? | none | n/a |
| C2 | 2 (hop1) | ~43,800 member-months from cohort runoff | effect applies base-wide, not just new cohorts | yes (#10) |
| C2 | 3 (hop2) | ~$833k incremental revenue | none | n/a |
| C2 | 4 (hop3) | margin-adjusted $415k-$625k | none (covered by #6/GT-9?) | n/a |
| C3 | 1 (head) | C2+GT-4+GT-10? | none | n/a |
| C3 | 2 (hop1) | real programs ramp up, partial engagement | year-one engagement is partial | yes (#11) |
| C3 | 3 (hop2) | 40-60% haircut applied | haircut range is a reasonable bound | yes (#12) |
| C3 | 4 (hop3) | range straddles cost, turns negative with liability | none (covered by GT-10?) | n/a |
| C4 | 1 (head) | GT-12?+GT-4 | none | n/a |
| C4 | 2 (hop1) | opt-in can't distinguish at-risk members | none (covered by GT-12?) | n/a |
| C4 | 3 (hop2) | dead-weight spend risk, benefit estimates are ceilings | redemption not restricted/weighted to at-risk (inline) | yes (#4, already present) |
| C5 | 1 (head) | GT-5+C1 | none | n/a |
| C5 | 2 (hop1) | category normalization via rival's head start | member base perceives points as standard feature | yes (#14) |
| C5 | 3 (hop2) | frame as parity/defensive investment | none | n/a |
| C6 | 1 (head) | C3+C4+GT-8 | none | n/a |
| C6 | 2 (hop1) | full commit is not decision-ready | none | n/a |
| C6 | 3 (hop2) | capped pilot + diagnostic achievable in 3 weeks | pilot design/diagnostic scopable in 3 weeks | yes (#15) |
| C6 | 4 (hop3) | defer full-year decision to checkpoint | none | n/a |

---

## 5. Abandoned Reasoning

### Dead End: Linear per-point breakeven approximation

**What was tried:** An initial breakeven calculation treated retained members as a simple linear function of churn-point reduction — 1 percentage point of monthly churn reduction ≈ 480 members/month × 12 = 480 member-years/year — implying the program would need roughly a 2.8-3.8 percentage-point sustained churn reduction to cover $310,000, well above the claimed 1.8-point target.

**Why abandoned:** This approximation ignores compounding: a member retained in month 1 is also not at risk of the same churn event in later months, and the two churn rates (6.8% vs. 5.0%) diverge geometrically, not linearly, over a 12-month horizon. Recomputing via the geometric survival-curve method (GT-7) on the same inputs produced roughly 4x the member-years of retention (~43,800 member-months vs. the linear method's ~10,400), which flips the apparent conclusion — the idealized case clears the $310,000 bar rather than falling short of it (see Chain C2). The linear method was mathematically incorrect for this question, not merely a rougher estimate.

**What it ruled out:** A superficially plausible but wrong "the claimed 1.8-point reduction can't possibly cover $310k" conclusion. This dead end matters for the board conversation: the real problem with the economics is not that the arithmetic fails in the idealized case, but that the *idealized case is unrealistic* (C3, C4) — a subtler and more decision-relevant finding than a simple arithmetic shortfall would have been.

### Dead End: Attributing the churn spike primarily to the rival's loyalty launch

**What was tried:** Treating "a rival launched a competing loyalty program" as the headline explanation for the churn spike, which would have made "launch our own loyalty program" a clean, symmetric response.

**Why abandoned:** Contradicted by GT-6 — the rival's program has existed for only about one of the six months over which churn rose from 4.2% to 6.8%. A cause cannot explain an effect that mostly preceded it. This path was abandoned once the timeline arithmetic was checked against the stated dates, not on intuition.

**What it ruled out:** The framing that would have made this a "differentiation" decision rather than a "root-cause-unknown, defensive-parity-at-best" decision (see C1, C5) — a materially different frame for the board.

---

## 6. Conclusion

**Recommended approach:** Don't fund the $310,000/year loyalty program as proposed; fund a capped, randomized pilot (target budget well under $100,000) with a genuine control group, run in parallel with an immediate root-cause diagnostic using data the company already holds (exit-survey push, cohort/vintage churn breakdown, outage-incident timeline, pricing-history check, support-ticket volume trend), and bring the full-year funding decision back to the board at a 60-90 day follow-up once real causal and response data exist (chain C6).

**Key insight:** The timing alone rules out the tidiest story — "a rival's loyalty program caused our churn spike, so our own loyalty program is the fix" — because the rival's program has existed for only one of the six months over which churn rose (chain C1). That means the loyalty program, even if it works exactly as claimed, is very likely treating a symptom of an unidentified root cause rather than the cause itself, and its best-supportable role today is defensive category parity, not a churn-reversal lever (chain C5).

**Trade-offs acknowledged:** Delaying a full-year commitment costs three months of not having a scaled loyalty program in market, during which the rival's head start persists (chain C5) — no chain — flagged assumption only, since the size of that competitive cost is not itself quantified in this analysis. In exchange, the pilot avoids locking in $310,000/year against numbers that, under realistic (not idealized) assumptions about ramp-up and adverse selection, plausibly fall short of covering the cost (chains C3, C4) — a risk a before/after launch with no control group would never surface, since any partial reversion toward 5% would be credited to the program whether or not the program caused it (assumption #9).

**Confidence:** LOW
This reflects the weakest chains feeding the Conclusion: GT-9? (unverified gross margin, chain C2), GT-10? (unresolved redemption-liability scope, chain C3), GT-11? (unestablished root cause, chains C1/C5), and GT-12? (unconfirmed absence of targeting, chain C4). Verifying margin and cost-scope with Finance, running the root-cause diagnostic, and confirming the program's actual design with Customer Success would raise this substantially — likely to HIGH on whether to fund the pilot (already HIGH via chain C6) and to at least MEDIUM on the underlying ROI case. The recommendation itself does not require those unknowns to resolve in any particular direction to be correct — it is precisely the decision that make sense to make while they remain unresolved.

---

## Process output (required before presentation)

**§6→§4 closure ledger:**
- "Don't fund the $310,000/year loyalty program as proposed; fund a capped pilot... bring the full-year decision back in 60-90 days" → chain C6 ✓
- "The timing alone rules out... loyalty program... is very likely treating a symptom... its best-supportable role today is defensive category parity" → chain C1, C5 ✓
- "Delaying a full-year commitment costs three months... rival's head start persists" → no chain — flagged assumption only
- "In exchange, the pilot avoids locking in $310,000/year against numbers that... plausibly fall short of covering the cost" → chain C3, C4 ✓
- "Confidence: LOW... reflects the weakest chains..." → chain C1, C2, C3, C4 ✓ (weakest-link rule, Criterion 5)

## Self-audit scan (process output)

**Table 1 — chain form**

| Chain | Chain Head (brief) | Form conforming? | Rule applied | Dependency clean? |
|---|---|---|---|---|
| C1 | GT-2+GT-5+GT-11? | yes | n/a | yes |
| C2 | GT-1+GT-7+GT-9? | yes | n/a | yes |
| C3 | C2+GT-4+GT-10? | yes | n/a | yes |
| C4 | GT-12?+GT-4 | yes | n/a | yes |
| C5 | GT-5+C1 | yes | n/a | yes |
| C6 | C3+C4+GT-8 | yes | n/a | yes |

**Table 2 — claim inventory (section 6)**

| §6 Span (brief) | Construct | Claim under R11? | R11 clause applied | Chain cited |
|---|---|---|---|---|
| Recommended approach: | bold lead-in | yes | prescribed lead-in, always a claim | C6 |
| Key insight: | bold lead-in | yes | prescribed lead-in, always a claim | C1, C5 |
| Trade-offs acknowledged: (sentence 1, competitive cost) | prose within lead-in span | yes | closes own sentence, asserts a cost | no chain — flagged assumption only |
| Trade-offs acknowledged: (sentence 2, pilot avoids lock-in) | prose within lead-in span | yes | closes own sentence, asserts a benefit | C3, C4 |
| Confidence: | bold lead-in | yes | prescribed weakest-link rating, treated as a claim | C1, C2, C3, C4 |

Scan complete: 6 chain rows, one per section-4 chain block in order; 5 section-6 rows, one per construct in order — 5 claims under R11, 0 excluded. 0 chains malformed, 0 claims untraced.

## Self-Audit Gate

**Criterion 1: Identify Essence**
Quoted span: "Should the company commit ~$310,000/year, on a three-week decision clock, to a loyalty/points program whose success depends on an unverified causal claim..."
Band: **Rigorous**
Justification: The statement names the core decision (not the CS team's proposal framing, not the churn symptom alone) and each success criterion is a checkable verb+subject+outcome triplet scannable against Section 6.

**Criterion 2: Challenge Assumptions**
Quoted span (from Assumption Audit scan): rows #10-#15 show assumptions surfaced from chain steps C2, C3, C4, C5, C6 and added to the table with specific verdicts (e.g., "#3 ... Discard — falsified by timing").
Band: **Rigorous**
Justification: All 15 rows use the four-type scheme, Verdict cells lead with a token plus em-dash justification, unverified assumptions used in chains are marked "unverified — flagged," and the Assumption Audit table confirms exhaustive coverage of every chain step.

**Criterion 3: Establish Ground Truths**
Quoted span: "`?`-marked: GT-9, GT-10, GT-11, GT-12 (4 of 12)."
Band: **Sound**
Justification: IDs are stable and the enumeration matches the list on inspection; however, GT-7 (a HIGH-confidence-chain-adjacent convention, feeding MEDIUM chain C2) is a definitional rather than externally-cited fact, so no external read-at-source location applies — this is disclosed but is a departure from the strict citation form, landing one entry short of Rigorous.

**Criterion 4: Reason Upward**
Quoted span (from self-audit scan Table 1): "C1 | GT-2+GT-5+GT-11? | yes | n/a | yes" through "C6 | C3+C4+GT-8 | yes | n/a | yes" — all six chains conforming, dependencies clean.
Band: **Rigorous**
Justification: Every chain has a genuine intermediate step, no analogy is used as direct evidence (C4 and C5's market-perception claims are grounded in named GTs/assumptions about this specific situation, not "others have done this"), the Abandoned Reasoning section documents two genuine dead ends with specific structural reasons, and surfaced assumptions are declared inline with `[Assumes: X]`.

**Criterion 5: Validate**
Quoted span: "C3 ... Confidence: LOW / GT-10? ... and GT-9? ... both a clarified cost scope from Finance and a completed pilot would raise this to at least MEDIUM."
Band: **Sound**
Justification: Every chain names its weakest link and every GT-N? input carries a confidence caveat naming the specific unverified input and the path to HIGH; the one shortfall is that the overall Conclusion rests partly on LOW-confidence chains (C3, C4) rather than every contributing claim resting on a HIGH chain, which the Confidence line discloses rather than obscures.

**Criterion 6: Conclusion-to-Ground-Truth Traceability**
Quoted span (from self-audit scan Table 2): all 5 section-6 constructs carry a chain citation or the explicit `no chain — flagged assumption only` marker; 0 claims untraced.
Band: **Rigorous**
Justification: No new claim is introduced in Section 6 that doesn't trace to Section 4, and the Key Insight (the timing mismatch reframes causation) is a non-obvious finding that a same-story-as-the-rival's-launch analogy would have missed — not a restatement of the Recommended Approach.

**Gate result:** No criterion Absent; one criterion (Criterion 3) at Sound-not-Rigorous is not a Hand-wavy occurrence, so the hand-wavy cap (at most one Hand-wavy) is not implicated. **Gate cleared.**