**Answer: no, not as proposed.** Don't commit $310,000 a year on the bet that churn falls to 5%. Tell the board **"gated yes"**: fund a 90-day randomized pilot for about $62k, and scale up only if the measured drop in churn clears break-even. The program is cheap to be wrong about. But it has no evidence behind it, and it targets a churn rise whose cause nobody has diagnosed.

**Disclosures.**
- Every figure in your question is your own and unverified, so every chain below is MEDIUM at best. No local file or URL was cited, so there was nothing to open.
- One re-entry edge fired: the second-order pass returned to Phase 2 once. Extending C4 surfaced a contradiction. Pulling a loyalty program after launch can itself cause churn, which breaks the premise that the downside is capped at the run cost. That became assumption A11 (Discard), and the plan changed to a time-boxed beta.
- Nothing else was skipped. The template, rubric, trade-off and pre-mortem references were all opened and read.

---

## Assumption Audit scan (process output)

| Chain | Step | Step Text (brief) | Assumption surfaced? | Added to Table? |
|---|---|---|---|---|
| C1 | 1 | $25,833/mo cost vs $912k/mo revenue | none | n/a |
| C1 | 2 | 1pp of churn removed ≈ $512k revenue kept in 12 months | A7 (saved members then churn at 5%) | already present |
| C1 | 3 | 12-month break-even 0.61 / 0.86 / 1.51pp | A6 (margin 40–100%) | already present |
| C1 | 4 | lifetime break-even 0.14–0.35pp | A6, A7 | already present |
| C1 | 5 | must deliver a third or more of 1.8pp | none | n/a |
| C2 | 1 | $0.54/member/mo = 2.8% of price | none | n/a |
| C2 | 2 | if credit included, a 2.8% rebate asked to cut churn by 26% relative | A2, A3 | already present |
| C2 | 3 | if credit excluded, $1/mo redemption adds $576k | A2 | already present |
| C2 | 4 | cost scope decides the case | none | n/a |
| C3 | 1 | ~5 of 6 rising months predate the rival | none | n/a |
| C3 | 2 | the rival can't explain most of the rise | A13 (no pre-launch effect) | yes |
| C3 | 3 | cause undiagnosed | A4 | already present |
| C4 | 1 | weighted totals 85 > 56 > 49 | none | n/a |
| C4 | 2 | 20% holdout gives SE ≈ 0.17pp over 3 months | A10 (holdout feasible), A12 (months independent) | yes |
| C4 | 3 | 0.6pp shows at ~3.6 SE | A12 | yes (A12 already added at step 2) |
| C4 | 4 | gated yes, ~$62k pilot | none | n/a |
| C4 | 5 | [2nd] withdrawing the program triggers churn | A11 | yes (Phase 2 re-entry) |
| C4 | 6 | launch as a time-boxed beta | none | n/a |
| C4 | 7 | [2nd] accrued points are a liability | A2 | already present |
| C4 | 8 | [3rd] rival parity erodes differentiation | none | n/a |

## Adversarial pass (process output)

**Recompute.** Each figure was recomputed in Python, separately from the chain text:
- Revenue is 48,000 × $19 = $912,000 a month.
- The program costs $310,000 / 12 = $25,833 a month, which is $0.538 per member per month, or 2.83% of the price.
- 12-month break-even is 0.605pp at 100% gross margin, 0.865pp at 70% and 1.514pp at 40%.
- Lifetime break-even is 0.142, 0.202 and 0.354pp at the same margins.
- 1.8 / 6.8 = 26.5%, so the target is a 26% relative cut in churn.
- Redemption of $1 per member per month would cost $576,000 a year.
- The churn difference in a 20% holdout has a standard error of 0.287pp per month, or 0.166pp pooled over 3 months. A 0.6pp effect is therefore about 3.6 SE.
- The pilot costs $310,000 / 4 × 0.8 = $62,000.
- Weighted totals: pilot 16+12+25+12+12+8 = 85, full launch 16+6+5+15+4+10 = 56, decline 4+15+5+15+8+2 = 49.
- All of these match the chain text.

**Sensitivity.** The flip ground truth is GT-4?, whose scope is not stated. It is `?`-marked. If redeemed credit is excluded and uncapped, the true cost could exceed any plausible return. The mitigation is caveat and condition: confirm the cost scope and cap credit (C2). Weakest link per chain:
- **C1:** hop 3 (depends on margin, A6).
- **C2:** hop 2 (A3 is not in evidence).
- **C3:** hop 2 (A13).
- **C4:** hop 2 (A10, A12).

**Rival.**
- "Fund in full now": §5 Dead End 1.
- "Decline outright": §5 Dead End 2.
- Both are ruled out there. Neither is carried live.

**Premise.** It is six months from now, and the gated pilot has failed badly.

**Causes.** The unfiltered list, by viewpoint:
- **Customer success (the implementer):**
  - The holdout was dropped as operationally awkward, so there was never a clean read.
  - The kill line was never pre-registered, and a 0.3pp result was argued up to "promising".
  - Churn diagnosis was skipped because the pilot was already running.
- **Finance (who pays):**
  - The $310k excluded credit redemptions, and the true cost ran 2–3× higher.
  - Gross margin turned out near 40%, which pushed 12-month break-even to 1.5pp.
- **Members:**
  - The people leaving were failed-payment churners, and credit was irrelevant to them.
  - $0.54 a month was too small to notice, so enrollment was low.
  - Holdout members found out about the program, complained, and left.
- **Rival:**
  - The rival raised its credits and neutralized ours.
- **Board:**
  - The board read "pilot" as indecision and forced a full rollout before the readout.

**Clusters.**
- **K1, measurement design never secured.** Holdout dropped, no pre-registered kill line, holdout contamination. Bears on C4, A10, A12.
- **K2, cost and margin mis-specified.** Credit excluded, low margin. Bears on C1, C2, GT-4?, A6.
- **K3, remedy mismatched to cause.** Involuntary churn, an incentive too small to notice, diagnosis skipped. Bears on C2, C3, A4.
- **K4, outside pressure overrides the gate.** Rival escalation, board forcing rollout. Bears on C4, GT-6?, GT-7?.

**Disposition.**
- **K1, plan change:** randomize at account level and pre-register the kill line in the board memo, before launch.
- **K2, plan change:** finance confirms cost scope and gross margin before launch, and credit is capped per member.
- **K3, plan change:** split churn into voluntary and involuntary within the three weeks. If payment failures dominate, redirect the budget to payment recovery.
- **K4, accepted risk:** mitigated by writing the day-90 decision date and the scale/kill thresholds into the board memo, and by not matching rival credits beyond break-even spend per member.

**Falsification.** The conclusion is false if either of these turns out to be true:
- Even the pilot isn't worth running: the true all-in cost per member, credit included, exceeds the lifetime value of the largest effect the holdout could plausibly show.
- The churn rise is mostly involuntary, so credit cannot touch it.

## §6→§4 closure ledger (process output)

```text
- "Recommended approach: gated yes, 90-day holdout pilot" → chain C4 ✓
- "confirm $310k scope, cap credit" → chain C2 ✓
- "split voluntary/involuntary churn first" → chain C3 ✓
- "pre-register kill line at break-even" → chain C1 ✓
- "launch as time-boxed beta" → chain C4 ✓
- "Key insight: cheap to be wrong, no evidence behind it" → chains C1, C2, C3 ✓
- "Trade-offs acknowledged" → chain C4 ✓
- "Pre-check" → chain C4 ✓
- "Confidence: MEDIUM" → chain C4 ✓
```

## Self-audit scan (process output)

| Chain | Chain Head (brief) | Form conforming? | Rule applied | Dependency clean? |
|---|---|---|---|---|
| C1 | GT-1? + GT-2? + GT-3? + GT-4? + GT-5? | yes | n/a | yes |
| C2 | GT-1? + GT-4? | yes | n/a | yes |
| C3 | GT-3? + GT-6? | yes | n/a | yes |
| C4 | C1 + C2 + C3 + GT-7? | yes | n/a | yes |

| §6 Span (brief) | Construct | Claim under R11? | R11 clause applied | Chain cited |
|---|---|---|---|---|
| Recommended approach: gated yes | bold lead-in | yes | prescribed lead-in | C4 |
| confirm $310k scope | list item | yes | list item over 40 chars | C2 |
| split churn voluntary/involuntary | list item | yes | list item over 40 chars | C3 |
| pre-register kill line | list item | yes | list item over 40 chars | C1 |
| time-boxed beta | list item | yes | list item over 40 chars | C4 |
| Key insight | bold lead-in | yes | prescribed lead-in | C1, C2, C3 |
| Trade-offs acknowledged | bold lead-in | yes | prescribed lead-in | C4 |
| Pre-check | bold lead-in | yes | bold lead-in whose colon closes the span | C4 |
| Confidence | bold lead-in | yes | bold lead-in whose colon closes the span | C4 |

```text
Scan complete: 4 chain rows, one per section-4 chain block in order; 9 section-6 rows, one per construct in order — 9 claims under R11, 0 excluded. 0 chains malformed, 0 claims untraced.
```

## Self-Audit Gate verdicts (process output)

**Criterion 1: Identify Essence**
Quoted span: "Is there enough evidence that a ~$310k/yr points-for-credit program will cut monthly churn by more than its break-even amount to justify committing now, when the cause of the 4.2%→6.8% rise is unknown?"
Band: **Rigorous**
Justification: it names the decision, not the symptom, and each success criterion is a verb, subject and outcome that can be checked against §6.

**Criterion 2: Challenge Assumptions**
Quoted span: "C3 | 2 | the rival can't explain most of the rise | A13 (no pre-launch effect) | yes"
Band: **Rigorous**
Justification: every row uses the four-type scheme and an em-dash verdict. A5, A8 and A11 are challenged and discarded. Unverified rows used in chains read "unverified — flagged". The audit covers all 20 chain steps.

**Criterion 3: Establish Ground Truths**
Quoted span: "enumerated GT-1?, GT-2?, GT-3?, GT-4?, GT-5?, GT-6?, GT-7?; the list carries `?` on exactly those seven, and there are no unsuffixed GTs"
Band: **Rigorous**
Justification: the enumeration matches the list. Each entry carries a provenance label (unverified, user-supplied, no source named). No GT feeds a HIGH chain.

**Criterion 4: Reason Upward**
Quoted span: "C4 | C1 + C2 + C3 + GT-7? | yes | n/a | yes"
Band: **Rigorous**
Justification: all four chains conform and have clean dependencies. The arithmetic recomputes. §5 has three structured dead ends. The only analogy ("match the rival") is discarded as A8, not used as evidence.

**Criterion 5: Validate**
Quoted span: "MEDIUM — Inputs axis short: GT-1?, GT-2?, GT-3?, GT-4?, GT-5? are unverified; confirming them from billing and finance data removes the downgrade. A6 is priced by the 40–100% bracket."
Band: **Rigorous**
Justification: every band is MEDIUM because the Inputs axis is short, and each line names its inputs and how to close them. The adversarial record has all parts, and every cluster has a disposition.

**Criterion 6: Conclusion-to-Ground-Truth Traceability**
Quoted span: "Scan complete: … 9 claims under R11, 0 excluded. 0 chains malformed, 0 claims untraced."
Band: **Rigorous**
Justification: every §6 claim cites a chain. The Key Insight (a 2.8% rebate aimed at an undiagnosed cause, which is cheap to test but unevidenced) is not a restatement of the recommendation.

Gate cleared: no Absent, no Hand-wavy.

---

# First Principles Analysis

## 1. Problem Essence

**Core problem:** Is there enough evidence that a ~$310k/yr points-for-credit program will cut monthly churn by more than its break-even amount to justify committing now, when the cause of the 4.2%→6.8% rise is unknown?

**Success criteria:**
- The Conclusion states a fund, don't-fund or conditional decision on the $310k program.
- The Conclusion states the churn reduction, in percentage points, that the program needs to pay back.
- The Conclusion names the checks that must pass before money is committed, and a kill line.
- The Conclusion states whether the rival's launch explains the churn rise.

## 2. Assumptions Table

| Assumption | Type | Treatment | Verdict | Verification |
|---|---|---|---|---|
| A1: The member, price, churn and cost figures you gave are accurate | untested belief | verify or flag | Challenge — basis of every chain; all GTs carry `?` | unverified — flagged; confirm from billing and finance |
| A2: $310k includes the cost of redeemed credit | untested belief | verify or flag | Challenge — scope not stated; changes true cost by up to ~$576k/yr | unverified — flagged |
| A3: The program will bring churn back toward 5% | untested belief | verify or flag | Challenge — no evidence given; this is the quantity the pilot must measure | unverified — flagged |
| A4: The churn rise is voluntary (price or value), not payment failures | untested belief | verify or flag | Challenge — credit cannot touch involuntary churn | unverified — flagged; split cancellations by reason code |
| A5: The rival's program caused the rise | untested belief | verify or flag | Discard — ~5 of 6 rising months predate it (C3) | contradicted by GT-3? + GT-6? timing |
| A6: Gross margin per member is 40–100% | untested belief | verify or flag | Challenge — bracketed rather than assumed | unverified — flagged; finance to confirm |
| A7: Saved members then churn at ~5%/mo | untested belief | verify or flag | Accept — used as the decay rate; faster churn only raises break-even and C1's endpoint holds | unverified — flagged |
| A8: Matching the competitor is reason enough | convention | challenge before use | Discard — analogy, not evidence about our members | n/a — not used in a chain |
| A9: Board needs a final call within three weeks | current constraint | record expiry | Accept — expires at the board update; a conditional decision with dated thresholds meets it | stated by you (GT-7?) |
| A10: A 20% randomized holdout is operationally and legally feasible | untested belief | verify or flag | Challenge — if not, fall back to staged cohorts, which is weaker evidence | unverified — flagged |
| A11: Withdrawing a launched program causes no churn spike | untested belief | verify or flag | Discard — surfaced by second-order pass; plan changed to time-boxed beta | re-entry edge, see disclosures |
| A12: Monthly churn readings are roughly independent, so pooling 3 months is valid | untested belief | verify or flag | Accept — even the 1-month SE (0.29pp) puts 0.6pp at ~2 SE, so C4 holds | unverified — flagged |
| A13: The rival's program had no pre-launch effect | untested belief | verify or flag | Accept — if it did, the cause is still undiagnosed, so C3 holds | unverified — flagged |

## 3. Ground Truths

- **GT-1?** 48,000 active members. Unverified: supplied in your question, no source named.
- **GT-2?** $19/month price. Unverified: supplied, no source.
- **GT-3?** Monthly churn rose from 4.2% to 6.8% over the last two quarters. Unverified: supplied, no source.
- **GT-4?** The program costs ~$310,000/yr to run; whether redeemed credit is included is not stated. Unverified: supplied, no source.
- **GT-5?** Customer success's target is churn back toward 5%. Unverified: supplied, no source.
- **GT-6?** A rival launched a similar program last month. Unverified: supplied, no source.
- **GT-7?** A decision is needed within three weeks for the board update. Unverified: supplied, no source.

```text
?-marked: GT-1?, GT-2?, GT-3?, GT-4?, GT-5?, GT-6?, GT-7? (7 of 7)
Read-at-source: none — no source was cited, so no read was possible, and no GT feeds a HIGH chain
```

## 4. Derivation Chains

### Conclusion C1: The program pays back within a year only if it delivers a third or more of its promised 1.8pp

GT-1? (48,000 members) + GT-2? ($19/mo) + GT-3? (6.8% churn) + GT-4? ($310k/yr) + GT-5? (5% target)
→ the program costs $25,833 a month against $912,000 of monthly revenue
→ each 1pp of monthly churn removed keeps about $512k of revenue in the first 12 months *[Assumes: A7]*
→ on 12-month payback it breaks even at 0.61pp (100% margin), 0.86pp (70%) or 1.51pp (40%) *[Assumes: A6]*
→ on a lifetime basis it breaks even at 0.14–0.35pp across the same margins
→ against the 1.8pp promised, the program must deliver a third or more of its target to pay back within a year, and most of it if margin is low

**Pre-check:** head GT-1?, GT-2?, GT-3?, GT-4?, GT-5? · ?-marked: GT-1?, GT-2?, GT-3?, GT-4?, GT-5? · lowest cited: none · Inputs ceiling: MEDIUM
**Confidence:** MEDIUM — the Inputs axis is short: GT-1?, GT-2?, GT-3?, GT-4? and GT-5? are unverified, and confirming them from billing and finance data removes the downgrade. A6 is priced by the 40–100% bracket in the endpoint. If A7 fails and saved members churn faster, break-even rises, so "a third or more" still holds. Weakest link: hop 3.

### Conclusion C2: The scope of the $310k figure must be settled before any commitment

GT-1? (48,000 members) + GT-4? ($310k/yr, scope unstated)
→ $310k spread over 48,000 members is $0.54 per member per month, 2.8% of the price
→ if it includes redeemed credit, the program is in effect a 2.8% rebate asked to cut churn by 26% relative *[Assumes: A2, A3]*
→ if it excludes redeemed credit, redemption of just $1 per member per month adds $576k a year
→ either reading changes the case, so the cost scope is a precondition for funding, not a detail

**Pre-check:** head GT-1?, GT-4? · ?-marked: GT-1?, GT-4? · lowest cited: none · Inputs ceiling: MEDIUM
**Confidence:** MEDIUM — the Inputs axis is short: GT-1? and GT-4? are unverified, and finance confirming the scope of the $310k closes it. A2 and A3 are the two branches the endpoint already covers. Weakest link: hop 2.

### Conclusion C3: The rival's program cannot explain the churn rise, so the cause is undiagnosed

GT-3? (rise over two quarters) + GT-6? (rival launched last month)
→ roughly five of the six months of rising churn predate the rival's program
→ the rival's program cannot explain most of the observed rise *[Assumes: A13]*
→ the cause of the rise is undiagnosed, so the loyalty program is a remedy chosen before its cause is known *[Assumes: A4]*

**Pre-check:** head GT-3?, GT-6? · ?-marked: GT-3?, GT-6? · lowest cited: none · Inputs ceiling: MEDIUM
**Confidence:** MEDIUM — the Inputs axis is short: GT-3? and GT-6? are unverified; month-by-month churn data and the rival's launch date close it. If A13 fails, pre-launch buzz explains at most part of the rise and the cause is still undiagnosed, so the endpoint stands. A4 is what the diagnosis will test. Weakest link: hop 2.

### Conclusion C4: The call for the board is a gated yes: a 90-day holdout pilot, not the full program

C1 (break-even 0.14–1.51pp) + C2 (cost scope open) + C3 (cause undiagnosed) + GT-7? (three-week deadline)
→ with weights locked before scoring, the gated pilot scores 85, full launch 56 and declining 49, driven by evidence generated (×5) and fit to the undiagnosed cause (×4)
→ a 20% randomized holdout gives a pooled 3-month standard error of about 0.17pp on the churn difference *[Assumes: A10, A12]*
→ a 0.6pp effect, the 12-month break-even at full margin, would show at about 3.6 standard errors by day 90
→ the board call is a gated yes: fund a 90-day pilot, about $62k at 80% exposure, conditional on the cost-scope and churn-reason checks
→[2nd] a launched loyalty program creates members who expect it, so withdrawing it can itself trigger churn (contradicts the capped-downside premise; routed back to Phase 2 as A11)
→ after that re-challenge, the pilot launches as an explicitly time-boxed beta so a kill does not read as a benefit taken away
→[2nd] points accrued during the pilot are a credit liability finance carries whether or not the pilot continues *[Assumes: A2]*
→[3rd] if the pilot works, the rival's matching program narrows the differentiation, so the lasting value is retention itself, not parity

Weights: evidence generated 5, retention upside 4, fit to undiagnosed cause 4, limited downside 3, fits deadline 3, competitive parity 2. Scores (full / decline / pilot):
- **Evidence generated:** 1 / 1 / 5
- **Retention upside:** 4 / 1 / 4
- **Fit to undiagnosed cause:** 1 / 2 / 3
- **Limited downside:** 2 / 5 / 4
- **Fits deadline:** 5 / 5 / 4
- **Competitive parity:** 5 / 1 / 4

**Pre-check:** head C1 (MEDIUM), C2 (MEDIUM), C3 (MEDIUM), GT-7? · ?-marked: GT-7? · lowest cited: MEDIUM · Inputs ceiling: MEDIUM
**Confidence:** MEDIUM — the Inputs axis is short: the cited chains C1, C2 and C3 are all MEDIUM, and GT-7? is unverified (confirm the board date). A10 is priced: without a holdout, staged cohorts still let you decide, though on weaker evidence. A12 is priced: even the 1-month SE puts 0.6pp at ~2 SE. The rivals are settled in §5. Weakest link: hop 2.

## 5. Abandoned Reasoning

### Dead End: Fund the full program now because break-even is low

**What was tried:** C1 shows the program needs only 0.14–1.51pp to pay back, so committing the full $310k looked like a safe bet.

**Why abandoned:** A low break-even makes being wrong cheap, but it is not evidence the program works. C2 shows the incentive is a 2.8% rebate against a claimed 26% relative cut in churn, and C3 shows the cause is undiagnosed. The pilot keeps 80% of the upside and also produces the missing evidence (C4, 85 vs 56).

**What it ruled out:** Treating a favorable break-even as a reason to skip measurement.

### Dead End: Decline, because the cause is unknown

**What was tried:** With the cause undiagnosed (C3), don't fund at all and put the effort into root-cause work.

**Why abandoned:** C1 and C4 make testing cheap. A $62k pilot, run alongside the diagnosis, costs less than the ~$154k of 12-month revenue that even a 0.3pp effect would keep. Declining scores 49 against the pilot's 85.

**What it ruled out:** Making "diagnose first" and "test the program" an either/or. They run in parallel within the three weeks.

### Dead End: Match the rival

**What was tried:** The rival launched a similar program, so we should too.

**Why abandoned:** It is an analogy used as evidence (A8, discarded). The timing in C3 also shows the rival isn't what drove the rise.

**What it ruled out:** Competitive parity as a standalone reason to fund.

## 6. Conclusion

**Recommended approach:** Don't fund the program as proposed. Take "gated yes" to the board: fund a 90-day randomized holdout pilot, about $62k at 80% exposure, and scale to the full $310k only if the measured churn gap clears break-even (chain C4).

- Before launch, finance confirms whether the $310k includes redeemed credit and caps credit per member (chain C2).
- Before launch, split the churn rise into voluntary and involuntary cancellations, and redirect the budget to payment recovery if failed payments dominate (chain C3).
- Pre-register the kill line: continue only if treated churn beats the holdout by the margin-appropriate 12-month break-even, 0.6pp at full margin or 0.86pp at 70% (chain C1).
- Launch the pilot as an explicitly time-boxed beta so that ending it does not read as a benefit taken away (chain C4).

**Key insight:** The program is cheap to be wrong about but has no evidence behind it. It breaks even at a fraction of its promised effect, yet it is effectively a 2.8% rebate aimed at a churn rise that began about five months before the rival's program existed (chains C1, C2, C3).

**Trade-offs acknowledged:** The pilot delays full parity with the rival by about a quarter and withholds the benefit from a fifth of members, and points accrued during the pilot are a liability whether or not it continues (chain C4).

**Pre-check:** head C1 (MEDIUM), C2 (MEDIUM), C3 (MEDIUM), C4 (MEDIUM) · ?-marked: none · lowest cited: MEDIUM · Inputs ceiling: MEDIUM (chain C4)
**Confidence:** MEDIUM — every contributing chain (C1, C2, C3, C4) is MEDIUM because all the figures are yours and unverified. Confirming them from billing and finance data, especially the scope of the $310k and gross margin, removes that cause (chain C4).

---

The claude.ai Gmail, Google Calendar and Google Drive connectors need to be authorized in your claude.ai connector settings before they can be used. None of them was needed for this analysis.