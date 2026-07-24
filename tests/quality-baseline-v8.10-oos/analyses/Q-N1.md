## Step 0 — technique selection

No focused-technique trigger phrase fires (the prompt names no technique and asks a multi-option decision question). **MODE = full-composer**: Phases 1–5 run in full, with trade-off, estimate, second-order, and inversion applied inside Phase 4.

---

## Process output — end-of-Phase-4 Assumption Audit

| Chain | Step | Step text (brief) | Assumption surfaced? | Added to table? |
|---|---|---|---|---|
| C1 | 1 | search 3mo + org-ramp 1–2mo → productive month 4–5 | none (covered by GT-11?) | n/a |
| C1 | 2 | hire cannot cover months 0–3 | architecture decisions land in months 0–3 | yes |
| C2 | 1 | trainees skip search and skip org-ramp | 8-wk program yields usable partial capability at wk 8 | yes |
| C2 | 2 | training yields earlier low-grade capability | both trainees complete and retain the material | yes |
| C3 | 1 | $24k → 2 holders vs $195k → 1 holder | attrition events are independent across holders | yes |
| C3 | 2 | training dominates on capability-per-dollar and survival | none | n/a |
| C3 | 2nd | $195k hire creates comp compression vs mid-levels | none | n/a |
| C3 | 3rd | compression raises attrition among the passed-over | none | n/a |
| C3 | 2nd' | training raises trainees' market value | none (GT-14?) | n/a |
| C3 | 3rd' | post-training comp adjustment is unbudgeted | none | n/a |
| C4 | 1 | 2 of 7 partially out for 8 weeks, in months 0–2 | program has an open cohort startable now | yes |
| C4 | 2 | real cost is $24k + ~29% capacity in the leveraged window | none | n/a |
| C5 | 1 | weighted totals D=79 > B=76 > C=69 > A=50 | weights reflect the org's true priorities | yes |
| C5 | 2 | recommend train-two + contractor bridge | contractor knowledge transfers without a contractual requirement | yes |
| C6 | 1 | within-menu totals B=76 > C=69 > A=50 | none | n/a |
| C6 | 2 | "both" justified only if streaming is durable strategy | streaming is a one-off feature, not a standing capability | yes |

## Process output — §6→§4 closure ledger

- "Train the two mid-levels now; bridge the 6-month window with contracted Kafka/Flink expertise; defer the permanent hire" → chain **C5** ✓
- "Within the three options offered: train (B) > both (C) > hire (A)" → chain **C6** ✓
- "Hiring is not the fast path — the training path puts partial capability on the ground sooner" → chain **C2** ✓
- "No option on the table covers months 0–3" → chain **C1** ✓
- "Trade-off accepted: near-term capacity loss of ~29% during the design window" → chain **C4** ✓
- "Trade-off accepted: trained engineers become more poachable; budget a retention adjustment" → chain **C3** (3rd-order extension) ✓

Ledger clean — every §6 claim carries a chain reference.

---

# First-Principles Analysis

## 1. Problem Essence

**Core problem:** Which capability-acquisition path maximizes the probability of shipping a committed streaming feature in 6 months *while* leaving the team with Kafka/Flink capability that survives the next attrition event?

**Success criteria** (each checkable against section 6):

1. The recommendation names a single path and states the calendar month at which usable capability exists.
2. The recommendation states how many people hold the capability afterward, and what happens if one leaves.
3. The recommendation names the first-year cash cost and what is *not* included in it.
4. The recommendation states which input, if wrong, flips the answer.

Note what the essence excludes: "should we hire or train" is the *presented* question, not the underlying one. The underlying question couples a hard schedule to a durable-capability goal, and those two goals are served by different instruments.

## 2. Assumptions Table

| Assumption | Type | Treatment | Verdict | Verification |
|---|---|---|---|---|
| The 6-month date is fixed and cannot be rescoped | current constraint | Record expiry conditions | Challenge — expires if the customer accepts a phased delivery or reduced v1 scope; this is the single highest-leverage unknown | unverified — flagged (requester did not state whether the commitment is contractual or a stated intent) |
| Elapsed calendar time cannot be shortened by spending money | physical law | Accept as ground-truth candidate | Accept — no amount of budget compresses a 3-month search below its own duration | Definitional (GT-9) |
| A person cannot hold codebase/org-specific knowledge before exposure to it | physical law | Accept as ground-truth candidate | Accept — implies every external hire carries a nonzero post-start ramp | Definitional (GT-6) |
| "Hiring is the fast way to close a capability gap" | convention | Challenge explicitly before use | Discard — contradicted by C2; search (3mo) alone exceeds the training program (2mo), before any ramp is counted | Challenged against GT-2 + GT-3 |
| "A senior hire is the higher-quality option, so pay for it" | convention | Challenge explicitly before use | Challenge — quality-per-person is real, but capability-per-dollar and capability-survival both favor two holders (C3) | Challenged against GT-4 + GT-13? |
| Search completes in ~3 months | untested belief | Verify or flag | Challenge — specialist Kafka/Flink searches are right-skewed; the estimate is a median, not a bound | unverified — flagged (GT-10?) |
| A senior hire reaches independent productivity in 1–2 months | untested belief | Verify or flag | Challenge — org-dependent; ranges from 1 to 4 months | unverified — flagged (GT-11?) |
| "Several more months" of OJT ≈ 3–4 months | untested belief | Verify or flag | Challenge — the requester's own phrasing is indefinite; this is the training path's largest uncertainty | unverified — flagged (GT-12?) |
| Last year's 2-of-7 loss implies ~29% forward attrition | untested belief | Verify or flag | Challenge — n=7 over one year has enormous variance; directionally real, numerically unreliable | unverified — flagged (GT-13?) |
| Training raises the trainees' external market value | untested belief | Verify or flag | Accept-provisionally — strongly expected, drives the retention caveat in C3 | unverified — flagged (GT-14?) |
| Contract Kafka/Flink expertise is sourceable in weeks | untested belief | Verify or flag | Challenge — load-bearing for the recommendation; verifiable in days by contacting two firms | unverified — flagged (GT-15?) |
| Streaming architecture decisions land in months 0–3 *(audit: C1 step 2)* | untested belief | Verify or flag | Accept-provisionally — near-universal for a 6-month greenfield capability, but org-specific | unverified — flagged |
| The 8-week program yields usable partial capability at week 8 *(audit: C2 step 1)* | untested belief | Verify or flag | Challenge — depends entirely on program quality; ask for graduate outcomes, not curriculum | unverified — flagged |
| Both trainees complete and retain the material *(audit: C2 step 2)* | untested belief | Verify or flag | Challenge — a 50% success rate collapses the path to one holder, i.e. to hiring's bus factor at 1/8 the cost | unverified — flagged |
| Attrition events are independent across capability holders *(audit: C3 step 1)* | untested belief | Verify or flag | Challenge — if attrition has a common cause (comp, management, burnout), two holders are far less than 2× the protection | unverified — flagged |
| The training program has an open cohort startable now *(audit: C4 step 1)* | untested belief | Verify or flag | Challenge — a cohort starting in 10 weeks silently destroys the training path's entire timing advantage | unverified — flagged |
| The criteria weights below reflect the org's true priorities *(audit: C5 step 1)* | convention | Challenge explicitly before use | Challenge — weights are the analyst's; the delivery weight is the one that flips the result (see sensitivity check) | Challenged and exposed in the sensitivity check |
| Contractor knowledge transfers to staff without a contractual requirement *(audit: C5 step 2)* | untested belief | Verify or flag | Discard — false by default; knowledge transfer that is not a deliverable does not happen. Mitigation folded into the recommendation | Challenged; discarded and converted to a stated contract term |
| Streaming is a one-off feature rather than a standing capability *(audit: C6 step 2)* | untested belief | Verify or flag | Challenge — this determines whether "both" is waste or investment | unverified — flagged |

## 3. Ground Truths

- **GT-1** The streaming feature is committed to a customer with a 6-month horizon — source: requester's statement.
- **GT-2** The hire path is estimated at ~3 months of search and ~$195,000 first-year compensation — source: requester's estimate.
- **GT-3** The training path is an 8-week external program at ~$12,000 per engineer for two engineers ($24,000), plus "several more months" of on-the-job ramp — source: requester's statement.
- **GT-4** The team is 7 engineers and lost 2 to attrition in the prior year — source: requester's statement.
- **GT-5** The team currently has no Kafka/Flink capability — source: requester's statement ("capability gap").
- **GT-6** Codebase- and organization-specific knowledge cannot be held prior to exposure; every external hire therefore carries a strictly positive post-start ramp — source: definitional.
- **GT-7** Training adds capability without adding headcount; hiring adds both — source: definitional.
- **GT-8** The two training candidates already hold the org's codebase and domain context — source: entailed by GT-5's framing ("our current mid-level engineers").
- **GT-9** Elapsed calendar time is unaffected by expenditure — source: physical law.
- **GT-10?** Time-to-fill distributions for senior specialist roles are right-skewed: overruns are more likely and larger than underruns — unverified: no org-specific hiring data supplied.
- **GT-11?** A senior hire requires roughly 1–2 months post-start to reach independent productivity in an unfamiliar org — unverified: org-specific, no onboarding data supplied.
- **GT-12?** "Several more months" of post-program ramp ≈ 3–4 months — unverified: requester's phrasing is indefinite.
- **GT-13?** The observed 2-of-7 loss implies a forward annual attrition rate near 29% — unverified: single-year, n=7 sample; wide confidence interval.
- **GT-14?** Completing a recognized streaming program raises an engineer's external market value — unverified: strongly expected, not measured here.
- **GT-15?** Contract Kafka/Flink expertise is sourceable within weeks at roughly $150–250/hour — unverified: no vendor quotes obtained.

## 4. Derivation Chains

### Conclusion C1: No option on the table puts capability on the ground during months 0–3, the window in which the streaming architecture is chosen

GT-2 (3-month search) + GT-6 (hires carry a ramp) + GT-11? (ramp ≈ 1–2 months) + GT-9 (time is not purchasable)
→ **[estimate]** earliest independent productivity for the hire = 3 + 1 = **month 4** (aggressive), central **month 4.5**, and — applying GT-10?'s right skew (search slips to 4–5 months) — **month 6–7** (conservative). Bracket: **[month 4, month 4.5, month 7]**. Under GT-3 + GT-12?, the training path's full-fluency date brackets to **[month 4, month 5.5, month 6+]** — the two brackets overlap almost entirely.
→ neither presented path delivers senior-grade capability with meaningful schedule margin; both land at or past the point where the architecture is already committed, so months 0–3 will be executed by engineers who do not yet hold the capability regardless of which option is chosen. `[Assumes: streaming architecture decisions land in months 0–3]`

**Confidence: MEDIUM.** Downgraded by GT-10?, GT-11?, GT-12?. Confirming the actual cohort start date and obtaining two real time-to-fill data points from the recruiter would raise this to HIGH. Weakest link: GT-12? — "several more months" is the single loosest input in the whole analysis, and it sets the training path's upper bracket.

### Conclusion C2: Hiring is not the fast path — training puts *partial* capability on the ground sooner than hiring puts *any*

GT-2 (3-month search) + GT-3 (8-week program) + GT-8 (trainees already hold org context) + GT-6 (hires do not)
→ the hire path pays two serial time costs (search, then org-ramp) while the training path pays only one (skill-ramp), because the trainees' org-ramp is already zero; the program ends at **month 2**, one full month before the hire's *start date* under the optimistic search estimate. `[Assumes: 8-week program yields usable partial capability at week 8]`
→ usable-if-supervised streaming capability exists in-house at month 2 on the training path versus month 3 (start) / month 4+ (productive) on the hire path — the convention that hiring is the time-optimal response to a capability gap is false for these specific numbers. `[Assumes: both trainees complete and retain the material]`

**Confidence: MEDIUM.** Downgraded by the two flagged inline assumptions and by GT-10?. Verification that raises it to HIGH: the program's graduate-outcome evidence, and a recruiter-supplied time-to-fill distribution for this role in this market.

### Conclusion C3: Training dominates hiring on capability-per-dollar and on capability survival

GT-3 ($24,000 → two holders) + GT-2 ($195,000 → one holder) + GT-4 (2 of 7 lost last year) + GT-13? (~29% forward rate)
→ first-year cost per capability-holder is ~$12,000 trained versus ~$195,000 hired, a ratio near 16:1; and a single holder is a bus-factor-1 dependency whose loss probability over the first year is material, whereas two holders retain the capability unless both depart. `[Assumes: attrition events are independent across holders]`
→ on both the cost axis and the survival axis, two trained engineers strictly dominate one senior hire; the hire's advantage must therefore come entirely from depth-of-expertise, not from economics or resilience.
→**[2nd]** a $195,000 senior placed above a team of mid-levels creates compensation compression against the engineers who were passed over for the growth opportunity
→**[3rd]** that compression raises departure risk among exactly the engineers who were the training candidates, on a team already at 2-of-7 — the hire path partially manufactures the attrition it is meant to insure against
→**[2nd']** completing the program raises the trainees' external market value (GT-14?)
→**[3rd']** retaining them requires a post-training compensation adjustment that is not in the $24,000 figure — an unbudgeted cost that erodes, but does not reverse, the 16:1 ratio

No extension step contradicts a ground truth; the 3rd' effect qualifies C3's cost claim and is carried forward as a stated trade-off rather than routing back to Phase 2.

**Confidence: MEDIUM.** Downgraded by GT-13? (attrition rate from n=7) and GT-14?. Verification: 3-year attrition history rather than 1, and a market-rate check on post-program compensation, would raise this to HIGH.

### Conclusion C4: The training path's real cost is $24,000 *plus* a ~29% capacity reduction in the schedule's most leveraged window

GT-4 (7 engineers) + GT-3 (8-week program for 2 of them) + GT-9 (the 6 months run regardless)
→ two of seven engineers — 29% of the team — are partially unavailable for 8 weeks, and under GT-1's clock those 8 weeks fall in months 0–2, the same window in which the committed feature's design and scaffolding must begin. `[Assumes: the program has an open cohort startable now]`
→ the training path's honest cost is $24,000 in cash plus roughly a quarter of the team's throughput during the highest-leverage stretch of the delivery — a cost that never appears in the $12,000-per-head figure and that partially cancels C2's timing advantage.

**Confidence: MEDIUM.** Downgraded by the inline cohort-availability assumption. Verification: the program's actual next start date and its weekly time commitment (full-time versus part-time changes this conclusion's magnitude substantially) would raise it to HIGH.

### Conclusion C5: Train the two engineers *and* contract a Kafka/Flink specialist as the delivery bridge; defer the permanent hire

Trade-off matrix — criteria and weights locked before any scoring:

| Criterion | Weight | A: hire only | B: train only | C: both | D: train + contract bridge |
|---|---|---|---|---|---|
| On-time delivery probability | 5 | 2 | 2 | 3 | 4 |
| Durable capability retention (bus factor) | 4 | 2 | 4 | 5 | 4 |
| First-year cost efficiency | 3 | 2 | 5 | 1 | 3 |
| Team morale / retention effect | 4 | 2 | 5 | 4 | 4 |
| Near-term capacity preservation (months 0–3) | 3 | 4 | 2 | 2 | 3 |
| Execution risk (fewest fragile dependencies) | 3 | 2 | 3 | 3 | 3 |
| **Weighted total** | | **50** | **76** | **69** | **79** |

GT-1 + GT-2 + GT-3 + GT-4 (the criteria's factual basis) + GT-13? + GT-15?
→ weighted totals **D=79 > B=76 > C=69 > A=50**, driven by the two highest-weight criteria: delivery (w5), where only D puts expertise on the ground in weeks rather than months, and retention (w4), where every option beats A. `[Assumes: the weights reflect the org's true priorities]`
→ recommend D — enrol the two mid-levels now, and contract senior Kafka/Flink expertise for months 0–4 with paired-work and written knowledge transfer as an explicit deliverable, not a hope. `[Assumes: contractor knowledge transfers without a contractual requirement — DISCARDED, which is why the transfer is written into the contract]`

**Sensitivity check:** D beats B by 3 points (3.8%) — inside the 10% band, so the near-tie is a real finding rather than a resolved one. The flip criterion is the **delivery weight**. At weight 5 (hard, contractual commitment): D=79 > B=72... at weight 3 (soft, rescopeable commitment): B=72 > D=71 and the contractor is unjustified expense. I am not adjusting the weight after seeing the result; I am naming it as the decision's true hinge: **how hard the 6-month date actually is decides this, and nothing else does.**

**Confidence: MEDIUM.** Downgraded by GT-15? (no contractor quotes obtained) and GT-13?. Verification: two contractor quotes with availability dates, plus a direct answer on whether the customer commitment is contractual or directional, would raise this to HIGH. Weakest link: GT-15? — if specialist contract capacity is not available inside 4–6 weeks, option D collapses into option B.

### Conclusion C6: Restricted to the three options offered, the ranking is train (B) > both (C) > hire (A)

GT-2 ($195,000, 3-month search) + GT-3 ($24,000, 8-week program) + GT-13? (~29% attrition)
→ within the offered menu, weighted totals are B=76 > C=69 > A=50; "both" loses to "train only" not because hedging is wrong in principle but because the hire's $195,000 and its comp-compression second-order effect (C3) are not repaid inside a 6-month window that the hire barely enters. `[Assumes: streaming is a one-off feature rather than a standing capability]`
→ choose training; "both" becomes the correct answer if and only if Kafka/Flink is a multi-year platform bet rather than one committed feature, because only a multi-year horizon gives the $195,000 time to amortize — and hiring alone is the weakest option under every weighting tested.

**Confidence: MEDIUM.** Downgraded by GT-13? and the inline one-off-versus-standing-capability assumption. Verification: a stated 2–3 year streaming roadmap (or its absence) would raise this to HIGH and could legitimately promote C over B.

## 5. Abandoned Reasoning

### Dead End: the straight schedule race — "hiring is the fast path"

**What was tried:** Comparing the training path's total ramp (8 weeks + several months) against the hire's search (3 months) to conclude that hiring reaches capability sooner.

**Why abandoned:** The comparison is not like-for-like — it charges the training path with a ramp while charging the hire path only with a search. Under GT-6, a hire's ramp is strictly positive and, per GT-8, the trainees' organizational ramp is already zero. Correcting the asymmetry inverts the result (C2).

**What it ruled out:** The default intuition that a capability gap under schedule pressure is a hiring problem. For these specific numbers it is not, and the reader does not need to re-derive it.

### Dead End: "both" as the automatic hedge

**What was tried:** Treating option C as dominant on the reasoning that two independent paths to the same capability multiply the odds that at least one lands.

**Why abandoned:** The independence premise fails. Both paths draw on the same 7-person team's supervisory attention, and C3's second-order chain shows the hire actively raises departure risk among the trainees — the two paths are negatively coupled, not independent. Its weighted total (69) also sits below train-only (76) once the $195,000 is charged against a 6-month horizon.

**What it ruled out:** The reflex that when two options are affordable, doing both is free insurance. It is not, when the options share a scarce resource and one degrades the other.

## 6. Conclusion

**Recommended approach:** Enrol both mid-level engineers in the program now, and separately contract senior Kafka/Flink expertise for months 0–4 with paired work and written knowledge transfer as a contractual deliverable. Defer the permanent hire until after delivery, when you will know whether streaming is a standing capability worth $195,000/year (C5). If contracting is off the table, **train** — within the three options you named, the ranking is train > both > hire, with hiring last under every weighting tested (C6).

**Key insight:** Hiring is not the fast path here. Search alone (3 months) exceeds the entire training program (2 months), and the hire then pays an organizational ramp that your own engineers have already paid — so the training path puts supervised capability in the room at month 2, before the hire's likely start date (C2). Reasoning by convention ("close a senior gap with a senior hire") gets this backwards. The deeper finding is that *none* of the three options you offered covers months 0–3, when the streaming architecture actually gets decided (C1) — which is why the answer is not on your menu.

**Trade-offs acknowledged:** Training removes ~29% of a 7-person team's throughput for 8 weeks, precisely during the design window, and that cost is invisible in the $12,000-per-head price (C4). Trained engineers become more poachable; budget a retention adjustment that is not in the $24,000 (C3, 3rd-order). You are also accepting less individual depth than a senior hire would bring, on the bet that two supervised holders plus contracted expertise beats one unsupervised expert who arrives late.

**Confidence: MEDIUM.** The downgrade comes from GT-15? (no contractor quotes — if specialist capacity is not sourceable within 4–6 weeks, the recommendation collapses to train-only), GT-12? ("several more months" is undefined and sets the training path's worst case), and GT-13? (a 29% attrition rate inferred from 2 losses in a team of 7 is directionally real but numerically unreliable). Three checks, all completable this week, would raise this to HIGH: **(1)** two contractor quotes with availability dates; **(2)** the program's next cohort start date and weekly time commitment; **(3)** a direct answer on whether the 6-month date is contractual or directional — that third one is the hinge, because at a softer delivery weight the contractor bridge stops being worth its cost and plain training wins outright.

---

## Validation record (rubric scoring, applied to the completed analysis)

**Criterion 1: Identify Essence**
Quoted span: "Which capability-acquisition path maximizes the probability of shipping a committed streaming feature in 6 months *while* leaving the team with Kafka/Flink capability that survives the next attrition event?"
Band: **Rigorous**
Justification: Names the underlying coupled question rather than the prompt's three-option framing, and each of the four success criteria is a scan-the-conclusion structural test (names a month, names a holder count, names a cash figure, names the flipping input).

**Criterion 2: Challenge Assumptions**
Quoted span: "Discard — false by default; knowledge transfer that is not a deliverable does not happen. Mitigation folded into the recommendation"
Band: **Rigorous**
Justification: Every row's Type is drawn from the four-type scheme; verdicts lead with Accept/Challenge/Discard followed by specific justification; unverified rows read "unverified — flagged"; the audit's seven surfaced assumptions were each written back into the table and marked inline.

**Criterion 3: Establish Ground Truths**
Quoted span: "**GT-13?** The observed 2-of-7 loss implies a forward annual attrition rate near 29% — unverified: single-year, n=7 sample; wide confidence interval."
Band: **Rigorous**
Justification: All fifteen items carry stable IDs matching the chain references, verified items cite the requester's statement or a definitional basis, and every unverified item carries the `?` suffix with a specific non-verification reason.

**Criterion 4: Reason Upward**
Quoted span: "→ the hire path pays two serial time costs (search, then org-ramp) while the training path pays only one … `[Assumes: 8-week program yields usable partial capability at week 8]`"
Band: **Rigorous**
Justification: Six conclusions, six chains, each with a genuine intermediate not statable from either GT alone; every assumption-introducing step carries an inline `[Assumes:` token; two dead ends use the What-was-tried / Why-abandoned / What-it-ruled-out structure with structural abandonment reasons.

**Criterion 5: Validate**
Quoted span: "Weakest link: GT-15? — if specialist contract capacity is not available inside 4–6 weeks, option D collapses into option B."
Band: **Sound**
Justification: Every chain carries a confidence line naming its unverified inputs and the verification that would raise it, and no chain consuming a `GT-N?` is rated HIGH; the band is Sound rather than Rigorous because C3 and C6 state their downgrade inputs without naming a single weakest link as explicitly as C1, C4, and C5 do.

**Criterion 6: Conclusion-to-Ground-Truth Traceability**
Quoted span: "Hiring is not the fast path here. Search alone (3 months) exceeds the entire training program (2 months) … (C2)"
Band: **Rigorous**
Justification: All six Conclusion claims cite a named chain per the closure ledger, no new reasoning is introduced in section 6, and the Key Insight names a convention-defeating finding (hiring is slower than training here) rather than restating the recommendation.

**Gate:** no criterion Absent. **Hand-wavy cap:** zero at Hand-wavy. **Rubric: PASS.**