No re-entry edges fired, and no clarification was needed: the problem statement and constraints were enough to proceed. This ran in full-composer mode. All three reference reads succeeded: the output template, the Pre-Mortem and Trade-off procedures, and the Self-Audit Gate rubric.

## Process output

### Trade-off matrix

**Options.** A: fund the full program at $310k/yr now. B: decline. C: fund a randomized ~90-day pilot with a holdout group, plus a churn-driver diagnosis.

**Criteria and weights (locked before scoring):**

| Criterion (higher is better) | Weight |
|---|---|
| Expected financial return | 5 |
| Downside protection / reversibility | 4 |
| Evidence generated about what drives churn and what the program does | 4 |
| Board-readiness within 3 weeks | 3 |
| Speed of churn impact | 3 |
| Competitive response to rival | 2 |

**Scores (weight × score):**

| Option | Return ×5 | Downside ×4 | Evidence ×4 | Board ×3 | Speed ×3 | Competitive ×2 | Total |
|---|---|---|---|---|---|---|---|
| A full fund | 3→15 | 1→4 | 2→8 | 4→12 | 4→12 | 5→10 | **61** |
| B decline | 2→10 | 3→12 | 1→4 | 2→6 | 1→3 | 1→2 | **37** |
| C pilot + diagnosis | 4→20 | 5→20 | 5→20 | 4→12 | 3→9 | 3→6 | **87** |

**Sensitivity:** C beats A by 26 points, so this is not a near-tie. C falls behind A (47 vs 49) only if both the evidence weight and the downside weight are set to zero.

### Assumption Audit scan

| Chain | Step | Step Text (brief) | Assumption surfaced? | Added to Table? |
|---|---|---|---|---|
| C1 | 1 | year-1 revenue = N·p·S(c) | A-11 closed-cohort year-1 frame | yes |
| C1 | 2 | full cost = operating + redeemed credit | none | n/a |
| C1 | 3 | break-even inequality | none | n/a |
| C2 | 1 | 5% preserves ≈$733k, ≈$407k/pt | none (A-1, A-2 already in table) | n/a |
| C2 | 2 | $440k–$733k contribution vs $310k | none (A-3, A-8 already in table) | n/a |
| C2 | 3 | break-even needs 0.76–1.27 pt cut | none | n/a |
| C2 | 4 | net-negative if redemptions > $130k–$423k | none (A-3 already) | n/a |
| C3 | 1 | pre-launch drivers act in post-launch window | none | n/a |
| C3 | 2 | before/after mixes effects | none | n/a |
| C3 | 3 | only a holdout attributes | none | n/a |
| C4 | 1 | ~5 of 6 months predate rival launch | none (A-2 already) | n/a |
| C4 | 2 | rival's launched program not the driver | none | n/a |
| C4 | 3 | cause still unidentified | none | n/a |
| C5 | 1 | weighted totals 87 > 61 > 37 | A-9 weights reflect priorities | yes |
| C5 | 2 | 20% cell detects 1-pt gap in 90 days | A-10 account-level randomization feasible | yes |
| C5 | 3 | recommend pilot, not full funding | none | n/a |
| C5 | 4 | [2nd] delay forgoes ≤ ≈$147k | none | n/a |
| C5 | 5 | [3rd] bounded cost < $310k upfront | none | n/a |
| C5 | 6 | [2nd] diagnosis may find cheaper lever | none (A-12 already) | n/a |
| C5 | 7 | [3rd] $310k stays redirectable | none | n/a |

Second-order check: no extension step contradicts a ground truth, so there is no return to Phase 2.

## Adversarial pass (process output)

**Premise:** It is six months from now. The recommendation (a randomized pilot plus a diagnosis, with no full funding) has failed badly.

**Causes (unfiltered; from the viewpoints of the implementer/CS, members, the CFO, the rival, and the board):**
1. The pilot could not be cleanly randomized. Treated and holdout members compared notes, so the groups contaminated each other. (CS)
2. 90 days was too short. Points work through an accumulated balance, and the effect only showed after month 4, so the pilot read as a false negative. (members)
3. Churn kept climbing toward 8% while we waited, and the board read the pilot as inaction. (board)
4. The rival used the 90 days to pull members over with its program, and those members never came back. (rival)
5. The diagnosis found most churn was failed payments. The loyalty framing had used up the three weeks. (CS)
6. Credit redemptions sat outside the $310k. The pilot "worked" on churn and lost money. (CFO)
7. Holdout members complained in public about being treated unequally. (members)
8. Fixed platform costs meant the pilot cost close to the full $310k. (CFO)
9. The effect showed up only among long-tenure members who were never going to leave. (members)
10. CS ran a program it had not been funded for half-heartedly. (implementer)
11. The churn definition changed partway through the pilot. (analytics)

**Clusters:**
- **K1 Measurement design** (causes 1, 2, 7, 9, 11). Bears on C3 and C5.
- **K2 Unverified cost basis** (causes 6, 8). Bears on C2 and GT-3?.
- **K3 Cost of waiting and competitive pressure** (causes 3, 4, 10). Bears on C5 and GT-4?. Causes 3 and 4 directly challenge the recommendation.
- **K4 Wrong lever** (causes 5, 9). Bears on C4.

**Disposition:**
- **K1, plan change:** Randomize at account level, stratified by tenure. Fix the churn definition before launch. Report results by tenure cohort. Commit in advance to extend to 150 days if the 90-day trend is positive but not conclusive.
- **K2, plan change:** Before the board meeting, finance confirms whether the $310k includes the face value of redeemed credit, and how much of it is fixed versus variable. Pilot approval depends on that answer.
- **K3, accepted risk with a named mitigation:** The delay cost is capped at about $147k of gross revenue (C5). Mitigation: start the cheap fixes (failed-payment recovery, win-back outreach) in parallel. Commit in advance that a positive readout triggers full rollout within two weeks.
- **K4, plan change:** The churn-driver diagnosis is delivered with the board update. It covers voluntary vs involuntary churn, tenure, exit reasons and where churners went.

These show up as weak links on C2 (K2), C4 (K4) and C5 (K1), and as a caveat on the Conclusion (K3).

---

## 1. Problem Essence

**Core problem:** Would a $310k/yr points-for-credit program change the part of churn that rose from 4.2% to 6.8%, enough to more than cover its full cost including redeemed credit? And can the board decision due in three weeks be made in a way that reveals the answer, rather than betting on it?

**Success criteria:**
- The Conclusion states a break-even churn reduction as a number, with the cost basis it assumes.
- The Conclusion states whether the rival's launch can explain the churn rise.
- The Conclusion names a decision the board can take within three weeks, with scale and kill conditions.
- The Conclusion states what the recommended option gives up, as a number.

## 2. Assumptions Table

| Assumption | Type | Treatment | Verdict | Verification |
|---|---|---|---|---|
| A-1: 48,000 members paying $19/month | untested belief | verify or flag | Accept — used as given; nothing contradicts it | unverified — flagged (GT-1?) |
| A-2: churn 4.2%→6.8% measured the same way throughout ~6 months | untested belief | verify or flag | Challenge — the definition may have changed, or mix voluntary and failed-payment churn | unverified — flagged (GT-2?); check against the billing churn series |
| A-3: $310k is all-in, including redeemed credit | untested belief | verify or flag | Challenge — C2 shows the sign of the return depends on this | unverified — flagged (GT-3?); finance line-item breakdown |
| A-4: the program will bring churn to ~5% | untested belief | verify or flag | Challenge — no mechanism or evidence given; C3 shows it can't be measured without a holdout | unverified; the only source is CS's target (GT-5?) |
| A-5: the rival's program is driving our churn | untested belief | verify or flag | Discard — timing rules it out for ~5 of the 6 months (C4) | contradicted by GT-2? + GT-4? + GT-7 |
| A-6: we must match a rival's feature to compete | convention | challenge before use | Challenge — parity only matters if the rival's feature is what's causing churn, and C4 says it did not start the rise | fails in this context |
| A-7: final call due within 3 weeks | current constraint | record expiry | Accept — expires after the board update; it sets the decision date, not the decision type | stated by user |
| A-8: contribution margin between 60% and 100% | untested belief | verify or flag | Accept — 100% is a hard ceiling by definition; 60% is an assumed floor | unverified — flagged (GT-10?) |
| A-9: trade-off weights reflect company priorities | untested belief | verify or flag | Accept — the result flips only if both the evidence and downside weights go to 0 | sensitivity check, process output |
| A-10: members can be randomized one account at a time | untested belief | verify or flag | Challenge — if not, a staggered rollout gives weaker attribution | unverified — confirm with CS/engineering |
| A-11: a closed-cohort, year-1 frame values the program | convention | challenge before use | Challenge — it ignores new cohorts and value after year 1, so it understates benefit; kept as a conservative bound | recomputed in GT-6 |
| A-12: churn drivers (fishbone): failed payments (Process), price vs value (Resources), product quality (Technology), support (People), value communication (Information), competitor/economy (Environment) | untested belief | verify or flag | Challenge — the diagnosis in C5 tests these | unverified; not used as fact in any chain |
| A-13: churners are mostly early-tenure members who have earned few points | untested belief | verify or flag | Challenge — if true, points reach the wrong members | unverified; not used in chains; the pilot reports by tenure |

## 3. Ground Truths

- **GT-1?** 48,000 active members at $19/month ($912,000 MRR) — unverified: supplied by the user, no source cited
- **GT-2?** Monthly churn rose from 4.2% to 6.8% over the last two quarters (~6 months) — unverified: user-supplied
- **GT-3?** The program costs about $310,000/yr to run; the figure does not say whether redeemed credit is included — unverified: user-supplied
- **GT-4?** A rival launched a similar program last month — unverified: user-supplied
- **GT-5?** CS's target is churn back toward 5% — unverified: a reported target, not evidence
- **GT-6** In a closed cohort at constant monthly churn c, the share remaining after t months is (1−c)^t, and total member-months over 12 months are S(c) = (1−(1−c)^12)/c — source: geometric-series identity; read-at-source: definitional, recomputed here: S(6.8%) = 8.390, S(5.9%) = 8.778, S(5.0%) = 9.193
- **GT-7** A cause cannot produce an effect that comes before it — source: causal ordering; read-at-source: definitional
- **GT-8** Account credit applied to a bill reduces cash collected by the credit's face value — source: definition of account credit; read-at-source: definitional
- **GT-9** Attributing an outcome change to an intervention needs a comparison group that did not get it. A before/after comparison assumes nothing else changed — source: counterfactual definition of a causal effect; read-at-source: definitional

- **GT-10?** Contribution margin per member is between 60% and 100% of $19 — unverified: margin not supplied

```text
?-marked: GT-1, GT-2, GT-3, GT-4, GT-5, GT-10 (6 of 10)
Read-at-source: GT-6, GT-7, GT-8, GT-9 — definitional, stated and recomputed in their entries (they feed HIGH chains C1, C3)
Phase 3 failure record: GT-1–GT-5 and GT-10 cite no source (user-supplied), so there is nothing to open; none feeds a HIGH chain
```

## 4. Derivation Chains

### Conclusion C1: Break-even must count redeemed credit as cost

GT-6 (closed-cohort survival identity) + GT-8 (credit reduces cash collected)
→ year-1 revenue from today's base at monthly churn c is N·p·S(c) *[Assumes: A-11 — closed-cohort year-1 frame]*
→ the program's full year-1 cost is its operating cost plus the face value of credit redeemed
→ the program pays back in year 1 only when m·N·p·[S(c_new) − S(c_old)] ≥ operating cost + redeemed credit

**Confidence:** HIGH — Inputs: GT-6 and GT-8 are definitional and read at source. Inference: each hop is algebra on the line above. Priced assumption: if A-11 fails, benefit is larger, so the inequality is still a sufficient condition. Rival: "the $310k is the whole cost" is ruled out by GT-8.

### Conclusion C2: Payback needs a ~0.8–1.3 point churn cut, and the sign depends on where credit is booked

C1 (break-even condition) + GT-1? (48,000 × $19) + GT-2? (6.8% now) + GT-5? (5.0% target) + GT-3? ($310k) + GT-10? (margin 60–100%)
→ S(6.8%) = 8.39 vs S(5.0%) = 9.19 member-months, so reaching 5% preserves ≈$733k of year-1 gross revenue, ≈$407k per point
→ at 60–100% margin that is $440k–$733k of contribution against $310k, if the $310k is all-in
→ break-even therefore needs churn cut by 0.76 points at 100% margin up to 1.27 points at 60%, landing at ~5.5–6.0%
→ if redemptions sit outside the $310k, full success at 5% turns net-negative once they exceed $130k–$423k a year (1.2–3.9% of revenue)

**Confidence:** MEDIUM. The Inputs axis is short: GT-1?, GT-2?, GT-3?, GT-5? and GT-10? are user-supplied. That closes by pulling member count, average revenue per member (ARPU) and the churn series from billing, margin from finance, and a line-item breakdown of the $310k. Inference is arithmetic: S is linear over this range to within 0.2%, since S(5.9%) = 8.778 vs a midpoint of 8.791. There is no live rival. Weak link (K2): GT-3?'s composition.

### Conclusion C3: Only a randomized holdout can attribute a churn change to the program

GT-7 (cause precedes effect) + GT-9 (attribution needs a counterfactual)
→ churn drivers already running before launch keep acting after launch, inside the same measurement window
→ a before/after reading after a full rollout blends the program's effect with every concurrent driver
→ only a randomized holdout that does not receive the program can attribute a churn change to it

**Confidence:** HIGH — Inputs: GT-7 and GT-9 are definitional. Inference: deductive. Rival: "a before/after reading is good enough" is ruled out by GT-9, because it needs an assumption of no concurrent change, and GT-7 shows the pre-existing rise is exactly such a change.

### Conclusion C4: The rival's launch cannot explain the rise, so its cause is still unidentified

GT-2? (rise over ~6 months) + GT-4? (rival launched ~1 month ago) + GT-7 (cause precedes effect)
→ about five of the six months of rising churn came before the rival's launch
→ the rival's launched program cannot have caused that rise, and can at most have accelerated its last month
→ whatever started the rise is still unidentified, and a program designed to match the rival does not target it

**Confidence:** MEDIUM. The Inputs axis is short: GT-2? and GT-4? are user-reported. That closes by reading the dated monthly churn series against the rival's launch and announcement dates. Inference: deductive. Rival: an announcement effect is addressed in §5. Weak link (K4): the drivers in A-12 are untested.

### Conclusion C5: Fund a randomized pilot and a diagnosis, not the full program

C2 (sign depends on cost basis) + C3 (only a holdout attributes) + C4 (cause unidentified)
→ weighted totals: pilot 87 > full funding 61 > decline 37, driven by evidence (×4) and downside protection (×4) *[Assumes: A-9]*
→ a 20% treatment group of ~9,600 against an equal holdout detects a 1-point monthly churn gap in 90 days (≈2.6 pt cumulative gap vs SE ≈0.55 pt) *[Assumes: A-10]*
→ do not fund the full $310k now; fund a ~90-day randomized pilot plus a churn-driver diagnosis, with scale and kill criteria fixed in advance
→[2nd] if the program does work, the delay forgoes at most ≈$147k of gross revenue on the untreated 80% (0.8 × $733k × 3/12)
→[3rd] that bounded cost is below the $310k a full rollout commits upfront, whose sign C2 cannot yet fix
→[2nd] the diagnosis may find a cheaper lever, such as failed-payment churn, that points would not reach
→[3rd] the $310k stays uncommitted and can be redirected until the diagnosis and the pilot read out

**Confidence:** MEDIUM. The head cites C2 and C4, both rated MEDIUM. The two assumptions are priced:
- A-9: the result flips only if both the evidence and downside weights go to zero.
- A-10: if account-level randomization is infeasible, a staggered rollout gives weaker attribution, but the endpoint still stands because C3 shows a full rollout attributes nothing.

Weak link (K1): the 90-day window may be too short for a program that pays off through accumulated points.

## 5. Abandoned Reasoning

### Dead End: Compare $310k to the total revenue lost to the churn rise

**What was tried:** Setting the $310k against the ≈$1.09M of year-1 revenue lost by moving from 4.2% to 6.8% churn (S(4.2%) = 9.58 vs 8.39).
**Why abandoned:** It compares cost to the whole problem rather than to what the program can be credited with, and it leaves out margin and redeemed credit (C1).
**What it ruled out:** "The problem is big, so the program is cheap" as an argument.

### Dead End: Lifetime-value frame

**What was tried:** The undiscounted lifetime revenue of the current base at 5% vs 6.8% churn ($18.2M vs $13.4M, a $4.8M gap).
**Why abandoned:** It assumes a permanent effect with no discounting, and that permanence cannot be established.
**What it ruled out:** Using the $4.8M as the benefit. It is an upper bound only.

### Dead End: Competitive parity ("the rival did it")

**What was tried:** Justifying the program because a rival launched one.
**Why abandoned:** It is an analogy used as evidence. The rival's results are unknown, and its launch came after the rise began (C4).
**What it ruled out:** Matching a feature as a reason on its own.
**Rival to C4 considered:** Churn could have been driven by an announcement before the launch. This bears on why churn rose, not on C4's endpoint (the launched program did not cause the earlier months). The diagnosis's question about where churners went settles it.

## 6. Conclusion

**Recommended approach:** Do not approve the full $310,000 program at the board update. Approve a ~90-day randomized pilot on about 20% of members with an equal holdout, on the condition that finance first confirms whether the $310,000 includes redeemed credit. Deliver a churn-driver diagnosis with the board update (chain C5).

**Key insight:** The rival's launch, the event that made this urgent, cannot explain a churn rise that started about five months earlier. Funding the program would answer the trigger, not the problem (chain C4).

- The program pays back in year 1 only if it cuts monthly churn by roughly 0.8–1.3 points. If redeemed credit sits outside the $310,000, even reaching 5% can lose money (chain C2).
- A full launch would produce a churn number nobody could attribute to the program (chain C3).

**Trade-offs acknowledged:** If the program works, waiting 90 days forgoes up to about $147,000 of gross revenue and gives the rival a head start. That is accepted as the price of knowing the program works before committing $310,000 a year (chain C5).

**Confidence:** MEDIUM. The contributing chains C2, C4 and C5 are rated below HIGH because the member, price, churn, cost and margin figures are user-supplied and have not been checked against billing and finance (chains C2, C4, C5).

---

## Process output: closure ledger, self-audit scan, verdicts

```text
- "Do not approve the full $310,000 program … diagnosis with the board update" → chain C5 ✓
- "The rival's launch … cannot explain a churn rise that started about five months earlier" → chain C4 ✓
- "pays back in year 1 only if it cuts monthly churn by roughly 0.8–1.3 points …" → chain C2 ✓
- "A full launch would produce a churn number nobody could attribute" → chain C3 ✓
- "waiting 90 days forgoes up to about $147,000 …" → chain C5 ✓
- "Confidence: MEDIUM …" → chains C2, C4, C5 ✓
```

## Self-audit scan (process output)

| Chain | Chain Head (brief) | Form conforming? | Rule applied | Dependency clean? |
|---|---|---|---|---|
| C1 | GT-6 + GT-8 | yes | n/a | yes |
| C2 | C1 + GT-1? + GT-2? + GT-5? + GT-3? + GT-10? | yes | n/a | yes |
| C3 | GT-7 + GT-9 | yes | n/a | yes |
| C4 | GT-2? + GT-4? + GT-7 | yes | n/a | yes |
| C5 | C2 + C3 + C4 | yes | n/a | yes |

| §6 Span (brief) | Construct | Claim under R11? | R11 clause applied | Chain cited |
|---|---|---|---|---|
| Recommended approach: do not approve full… | bold lead-in | yes | prescribed lead-in, colon closes bold span | C5 |
| Key insight: rival's launch cannot explain… | bold lead-in | yes | prescribed lead-in | C4 |
| pays back only if 0.8–1.3 pt cut… | list item | yes | list item over forty characters | C2 |
| full launch unattributable… | list item | yes | list item over forty characters | C3 |
| Trade-offs acknowledged: forgo ≤$147k… | bold lead-in | yes | prescribed lead-in | C5 |
| Confidence: MEDIUM… | bold lead-in | yes | bold lead-in whose colon closes the bold span | C2, C4, C5 |

```text
Scan complete: 5 chain rows, one per section-4 chain block in order; 6 section-6 rows, one per construct in order — 6 claims under R11, 0 excluded. 0 chains malformed, 0 claims untraced.
```

**Criterion 1: Identify Essence**
Quoted span: "Would a $310k/yr points-for-credit program change the part of churn that rose from 4.2% to 6.8%, enough to more than cover its full cost including redeemed credit?"
Band: **Rigorous**
Justification: The statement names the decision rather than the trigger, and each success criterion is a pass/fail check against the Conclusion.

**Criterion 2: Challenge Assumptions**
Quoted span: "| C5 | 2 | 20% cell detects 1-pt gap in 90 days | A-10 account-level randomization feasible | yes |"
Band: **Rigorous**
Justification: All rows use the four types, verdicts lead with a token plus a justification, one assumption is discarded and several are challenged, and the audit covers all 20 chain steps.

**Criterion 3: Establish Ground Truths**
Quoted span: "enumerated GT-1, GT-2, GT-3, GT-4, GT-5, GT-10; list carries `?` on exactly those six; unsuffixed GT-6/7/8 and GT-9 feed HIGH chains C1/C3 with definitional read-at-source locations"
Band: **Rigorous**
Justification: The enumeration matches the list, every unsuffixed ground truth feeds a HIGH chain with a named location, and the unsourced inputs carry a failure record.

**Criterion 4: Reason Upward**
Quoted span: "| C5 | C2 + C3 + C4 | yes | n/a | yes |"
Band: **Rigorous**
Justification: All five chains conform and have clean dependencies, §5 records three dead ends with specific reasons, parity-by-analogy is rejected, and the audit's surfaced assumptions are marked inline.

**Criterion 5: Validate**
Quoted span: "The head cites C2 and C4, both rated MEDIUM. The two assumptions are priced"
Band: **Rigorous**
Justification: Each band matches its axes: HIGH on definitional C1 and C3, MEDIUM with the short axis named elsewhere, and the Conclusion equals its weakest contributor. The adversarial pass has a past-tense premise, a cause list, clusters citing chains and a disposition for each cluster.

**Criterion 6: Conclusion-to-Ground-Truth Traceability**
Quoted span: "| Key insight: rival's launch cannot explain… | bold lead-in | yes | prescribed lead-in | C4 |"
Band: **Rigorous**
Justification: All six claims cite chains, and the Key Insight (the trigger is not the cause) differs from the recommendation (run a pilot).

Gate cleared: no criterion Absent, 0 Hand-wavy.

---

**Bottom line:** Don't fund the full program at $310k/yr yet. Take a ~90-day randomized pilot (about 20% of members, with an equal holdout) to the board, plus a churn-driver diagnosis.

- **Break-even:** getting back to 5% keeps about $733k of first-year revenue from your current members. To pay back its $310k, the program has to cut monthly churn by about 0.8–1.3 points.
- **Open question for finance:** if redeemed credit is not included in the $310k, even hitting 5% loses money once redemptions pass $130k–$423k a year (1.2–3.9% of revenue). Get that answer before the board meeting.
- **The rival's launch didn't cause the rise:** churn started climbing about five months before the rival launched, so the actual cause is still unknown.
- **What waiting costs:** if the program works, the 90-day wait costs at most about $147k.

All figures come from your prompt and haven't been checked against billing or finance data, so the recommendation is MEDIUM confidence.