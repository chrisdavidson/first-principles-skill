**Disclosed:** The Self-Audit Gate's Fix/Repeat loop fired once. On the first pass, Criterion 1 scored Sound (one success criterion could not be checked against the Conclusion) and Criterion 3 scored Hand-wavy (the unsuffixed GT-4 and GT-5 fed only MEDIUM chains). The gate had cleared, but the criterion was reworded and chain C7 (HIGH, definitions only) was added. All six criteria then re-scored Rigorous. No input magnitudes were supplied, so every dollar figure is an illustrative estimate.

## Answer

**Recommendation:** Build the reporting rewrite this quarter, scoped to the contract's acceptance criteria. Give sales a no-code Slack stopgap and build native Slack next quarter (chain C6). Deferring the rewrite forfeits about $480,000, against $12,000 to $120,000 for deferring Slack (chain C4).

**Band (from §6):** MEDIUM: the decision rule is HIGH (chain C7), and the magnitudes applied to it are MEDIUM (chain C4).

**Would change it:** a contract showing the expansion does not lapse on a one-quarter delay. Slack should then go first if its measured win-rate uplift exceeds about 5.6 points (chain C5).

## 1. Problem Essence

**Core problem:** Next quarter's engineering capacity can go to only one of two investments. Which order of the two loses the least value: the committed-expansion reporting rewrite first, or the prospect-requested Slack integration first?

The question says "build next", and capacity comes back every quarter. So this is an ordering decision, not a permanent either/or. The choice that triggered the analysis ("which one do we build?") is not the quantity the analysis has to answer ("what does each option lose by waiting a quarter?"). Treating the decision as never building the loser is examined, and abandoned, in section 5.

No magnitudes were supplied: no contract value, deadline, pipeline size, deal size or win rates. Every dollar figure below is an **illustrative estimate**, labelled as one. The analysis therefore yields a **decision rule with explicit break-even thresholds**, plus a recommendation under the most natural reading of the problem statement.

**Success criteria:**
- The answer names what to build this quarter and what happens to the other option. It need not be one of the two named options alone; a composite was tested (section 4, C6).
- For every dollar figure it states, the Conclusion cites the section-4 chain whose hop shows that figure's arithmetic.
- The answer names the single fact that would reverse it, and the threshold at which it reverses.
- The answer states what is being given up, in dollars or deals, with a bracket.

## 2. Assumptions Table

| Assumption | Type | Treatment | Verdict | Verification |
|------------|------|-----------|---------|--------------|
| A-1: One engineering quarter funds at most one of the two investments | current constraint | Record expiry conditions | Accept — expires if capacity is added (contractors, pulling people off other work) or if either scope shrinks well below a quarter; until then it binds | unverified — flagged GT-1? (user-stated, no source) |
| A-2: The committed expansion is time-bound: it lapses, or is put at risk, if the rewrite is not delivered this quarter | untested belief | Verify or flag | Challenge — "committed expansion against" the rewrite reads naturally as conditional on timely delivery, but no deadline was stated; this is the decisive assumption (C4 vs C5) | unverified — flagged GT-2?; resolved only by reading the contract or order form |
| A-3: The expansion commitment is binding (signed), not verbal intent | untested belief | Verify or flag | Challenge — "committed" covers everything from a signed order form to a sponsor's promise; priced via p_on = 0.9 in GT-6? | unverified — flagged GT-2? |
| A-4: Repeated prospect requests mean a Slack integration materially raises win rate | untested belief | Verify or flag | Challenge — a request is a stated preference, not a measured purchase cause; carried as a bracket of 2 to 20 win-rate points, not a point value | unverified — flagged GT-3?, GT-7? |
| A-5: Whichever option is not chosen gets built next quarter (sequencing, not permanent exclusion) | untested belief | Verify or flag | Accept — "build next" implies an order; the failure case (loser never built) is priced on C1's confidence line | unverified — flagged |
| A-6: The decision is a permanent either/or ("build one, never the other") | convention | Challenge before use | Discard — capacity recurs quarterly and the question asks what to build next; see section 5 | contradicted by the problem statement's wording "next" |
| A-7: Work a customer has committed money against should take priority by default | convention | Challenge before use | Discard — priority is decided by cost of delay (C1); C5 shows this convention gives the wrong answer when the commitment is not time-bound | section 5 |
| A-8: The reporting rewrite fits in one quarter | untested belief | Verify or flag | Challenge — rewrites of existing surfaces routinely overrun; overrun is carried as a second-order effect on C6 and as pre-mortem cluster K2 | unverified — flagged |
| A-9: Late delivery raises churn risk on the account's existing base ARR | untested belief | Verify or flag | Accept — a missed commitment to an enterprise sponsor plausibly harms renewal; sized as an estimate (Δc = 0.10) in GT-6? and shown separately so it can be zeroed | unverified — flagged GT-6? |
| A-10: The Slack integration's value comes only through new-logo win rate | untested belief | Verify or flag | Challenge — it may also lift retention or engagement among existing customers; the upper bracket (Δw = 0.20) stands in for that extra value | unverified — flagged |
| A-11: A no-engineering Slack stopgap (Slack Workflow Builder, Zapier, or email-to-channel) can address part of the sales objection | untested belief | Verify or flag | Challenge — its feasibility depends on the product's existing webhook or email events | unverified — flagged GT-9? |
| A-12: Dollar figures compare on a nominal, undiscounted, pre-tax lifetime-revenue basis | convention | Challenge before use | Accept — discounting a one-quarter shift at any plausible rate moves figures by a few percent, far below the 4x to 40x gaps in C4 | stated basis, applied to both sides |
| A-13: The expected lifetime L = 3 years applies equally to expansion ARR and new-logo ARR (added by Assumption Audit) | untested belief | Verify or flag | Accept — L multiplies both sides of C4, so it cancels in the comparison; it affects only the absolute dollar figures | unverified — flagged GT-8? |
| A-14: A prospect who decides during the Slack-less quarter is lost permanently, not merely delayed (added by Assumption Audit) | untested belief | Verify or flag | Accept — this is the conservative (Slack-favourable) reading; if some prospects wait, C3's deferral cost falls | unverified — flagged |
| A-15: The rewrite's acceptance criteria are defined narrowly enough to deliver within the quarter (added by Assumption Audit) | untested belief | Verify or flag | Challenge — becomes pre-mortem cluster K2's plan change (scope to contracted acceptance criteria) | unverified — flagged |

## 3. Ground Truths

Verification step: none of GT-1? to GT-3? or GT-6? to GT-9? cites a source, so this analysis had nothing to open. They come from the problem statement or are estimates this analysis made. Each carries a Phase 3 failure record: **no source cited, nothing to open (ambiguous citation: none given)**. GT-4 and GT-5 are definitions, stated and derived in full in their own entries.

- **GT-1?** Next quarter's engineering capacity funds at most one of the two investments. Unverified: stated by the user with no source; failure record: no source cited.
- **GT-2?** An existing enterprise account has committed contract expansion that depends on the reporting rewrite. Unverified: stated by the user with no source. The amount, binding status, deadline and acceptance criteria are all unknown. Failure record: no source cited. A reduce-to-primitives drill in the appendix splits this claim into four primitives, all of them assumed.
- **GT-3?** Sales prospects have repeatedly requested a Slack integration. Unverified: stated by the user with no source. Request counts, deal values and closed-lost reasons are unknown. Failure record: no source cited.
- **GT-4** *(definition)* The value lost by deferring an option is what the delay **forfeits**, not what it merely **shifts**. The expected value of an uncertain cash flow is probability × magnitude. Source: definitions of expected value and cost of delay; read-at-source: stated in full in this entry.
- **GT-5** *(definition / derivation)* Take two jobs X and Y, each one quarter long, both to be built in sequence. Building X first incurs Y's one-quarter deferral cost D_Y. Building Y first incurs D_X. So X goes first if and only if D_X > D_Y. Source: derivation; read-at-source: derived in full in this entry.
- **GT-6?** *(estimate, illustrative)* Enterprise account figures:
  - committed expansion E = $150,000 ARR
  - base ARR B = $400,000
  - probability the expansion is realised if the rewrite is delivered on time: p_on = 0.9
  - probability it is realised if the rewrite is late: p_late = 0.1
  - added churn probability on the base if the rewrite is late: Δc = 0.10

  Unverified: these are estimates, not measured values; failure record: no source exists.
- **GT-7?** *(estimate, illustrative)* Slack pipeline figures:
  - N = 20 Slack-requesting deals deciding per year, so 20 / 4 = 5 per quarter
  - ACV = $40,000
  - incremental win-rate uplift from having Slack: Δw = 0.10, bracketed from 0.02 to 0.20

  Unverified: these are estimates; failure record: no source exists.
- **GT-8?** *(estimate)* Expected customer lifetime L = 3 years. Unverified: an estimate.
- **GT-9?** Common no-code tools (Slack Workflow Builder, Zapier, email-to-channel) can post a product's existing webhook or email events into Slack without the vendor writing code. Unverified: recalled general knowledge; no source was opened, and it is unknown whether this product emits such events. Failure record: no source cited.

?-marked: GT-1?, GT-2?, GT-3?, GT-6?, GT-7?, GT-8?, GT-9? (7 of 9)
Read-at-source: GT-4 (definition stated in full in its entry); GT-5 (derivation stated in full in its entry)

## 4. Derivation Chains

Basis for every dollar figure: nominal, undiscounted, pre-tax revenue in US dollars. "ARR" means annual recurring revenue. "Lifetime" means ARR × L years (GT-8?). Every figure was recomputed independently of this text; the Recompute part of the appendix's adversarial pass lists each one.

### Conclusion C1: The decision is an ordering, so the deciding quantity is each option's one-quarter deferral cost

GT-1? (one quarter funds at most one) + GT-5 (order rule for equal-length jobs)
→ both options are finished within two quarters whichever goes first, so the order only changes which one waits *[Assumes: A-5]*
→ the deciding quantity is each option's one-quarter deferral cost, not its total value

**Pre-check:** head GT-1?, GT-5 · ?-marked: GT-1? · lowest cited: none · Inputs ceiling: MEDIUM
**Confidence:** MEDIUM. The Inputs axis is short: GT-1? is user-stated. An engineering estimate showing each item takes about one quarter, and both together do not fit, would remove it as a cause of the downgrade. Inference is priced: A-5 might fail and the loser never be built. The comparison then becomes full-year value: Slack's full-year ARR is 20 × 0.10 × $40,000 = $80,000, against the rewrite's $160,000 ARR at risk (C2). The rewrite still leads unless Δw ≥ $160,000 ÷ (20 × $40,000) = 0.20, the top of the bracket. So the endpoint survives A-5 failing everywhere except at that edge. Rivals: "total value decides" is section 5 Dead End 1, ruled out by GT-5.

### Conclusion C2: Deferring the rewrite one quarter forfeits about $480,000 lifetime revenue if the commitment is time-bound

GT-2? (committed expansion) + GT-4 (forfeit vs shift) + GT-6? (account figures) + GT-8? (lifetime)
→ under a time-bound commitment, delay forfeits (0.9 − 0.1) × $150,000 = $120,000 of expansion ARR *[Assumes: A-2, A-3]*
→ delay also exposes 0.10 × $400,000 = $40,000 of base ARR to added churn risk *[Assumes: A-9]*
→ ARR at risk from deferring the rewrite totals $120,000 + $40,000 = $160,000
→ over three years that is $160,000 × 3 = $480,000 of lifetime revenue forfeited *[Assumes: A-13]*

**Pre-check:** head GT-2?, GT-4, GT-6?, GT-8? · ?-marked: GT-2?, GT-6?, GT-8? · lowest cited: none · Inputs ceiling: MEDIUM
**Confidence:** MEDIUM. The Inputs axis is short:
- GT-2? and GT-6? need the order form or contract read for the expansion amount, binding status and any delivery deadline, and the account's base ARR taken from billing.
- GT-8? needs the company's measured gross retention.

Inference is priced:
- A-2 failing is computed in C5: the cost becomes $33,750.
- A-9 failing (Δc = 0) leaves $120,000 × 3 = $360,000.
- A-3 is carried in p_on = 0.9.
- A-13 cancels in C4 because L multiplies both sides.

Rivals: "the expansion is lost even if the rewrite is delivered" is priced by p_on = 0.9. Nothing else competes with the endpoint.

### Conclusion C3: Deferring Slack one quarter forfeits about $60,000 lifetime revenue, bracketed $12,000 to $120,000

GT-3? (repeated prospect requests) + GT-4 (forfeit vs shift) + GT-7? (pipeline figures) + GT-8? (lifetime)
→ 20 deals per year ÷ 4 = 5 Slack-requesting deals decide during the deferral quarter
→ at Δw = 0.10 the quarter forfeits 5 × 0.10 = 0.5 incremental wins *[Assumes: A-4, A-14]*
→ 0.5 wins × $40,000 = $20,000 of ARR forfeited
→ central lifetime forfeit is $20,000 × 3 = $60,000 *[Assumes: A-13]*
→ bracket runs from 5 × 0.02 × $40,000 × 3 = $12,000 to 5 × 0.20 × $40,000 × 3 = $120,000

**Pre-check:** head GT-3?, GT-4, GT-7?, GT-8? · ?-marked: GT-3?, GT-7?, GT-8? · lowest cited: none · Inputs ceiling: MEDIUM
**Confidence:** MEDIUM. The Inputs axis is short:
- GT-3? and GT-7? need CRM closed-lost reasons from the last two to four quarters. A count of deals lost with Slack named as a reason, and the open pipeline of Slack-requesting deals with their ACVs, would replace the estimates.
- GT-8? needs measured retention.

Inference is priced:
- A-4 is carried as a bracket rather than a point value.
- A-14 is the reading that favours Slack; relaxing it only lowers this figure.

Rivals: Slack may also add value through existing-customer retention (A-10). That is absorbed by the upper bracket rather than left open.

### Conclusion C4: Under a time-bound commitment, build the rewrite first

C1 (MEDIUM) + C2 (MEDIUM) + C3 (MEDIUM)
→ deferring the rewrite forfeits $480,000, against $12,000 to $120,000 for deferring Slack
→ the rewrite's deferral cost is $480,000 ÷ $120,000 = 4× Slack's at the upper end and $480,000 ÷ $60,000 = 8× at the centre
→ Slack would only match at Δw = $480,000 ÷ (5 × $40,000 × 3) = 0.80, an 80-point win-rate uplift no single integration plausibly delivers
→ even with zero churn exposure the rewrite leads whenever E exceeds $120,000 ÷ (0.8 × 3) = $50,000 of expansion ARR
→ under a time-bound commitment, the rewrite goes first

**Pre-check:** head C1 (MEDIUM), C2 (MEDIUM), C3 (MEDIUM) · ?-marked: none · lowest cited: MEDIUM · Inputs ceiling: MEDIUM
**Confidence:** MEDIUM. The Inputs axis is short through C1, C2 and C3, each rated MEDIUM; their own lines carry their verification paths. Inference holds: each hop is arithmetic that recomputes. Rivals: "Slack first" under this reading is section 5 Dead End 4, ruled out by the 0.80 break-even computed here.

### Conclusion C5: If the commitment is not time-bound, the order turns on Slack's measured win-rate uplift, with break-even near 5.6 points

C1 (MEDIUM) + C3 (MEDIUM) + GT-6? (account figures)
→ without a deadline, delay shifts the expansion by one quarter rather than forfeiting it *[Assumes: A-2 is false]*
→ the shift costs one quarter of expected expansion, $150,000 × 0.9 × 0.25 = $33,750
→ $33,750 lies inside Slack's $12,000 to $120,000 bracket, so the two ends of the bracket recommend opposite orders
→ Slack goes first when Δw exceeds $33,750 ÷ (5 × $40,000 × 3) = 0.05625, about 5.6 win-rate points
→ in this reading the order is settled by a measured Slack win-rate uplift, not by the commitment

**Pre-check:** head C1 (MEDIUM), C3 (MEDIUM), GT-6? · ?-marked: GT-6? · lowest cited: MEDIUM · Inputs ceiling: MEDIUM
**Confidence:** MEDIUM. The Inputs axis is short:
- C1 and C3 are rated MEDIUM.
- GT-6? needs the contract's expansion amount and start date.

The endpoint is a conditional decision rule, not a pick, so the open bracket is its content rather than an unsettled rival. The observation that settles it is the measured uplift: the CRM win rate on Slack-requesting deals against comparable deals.

### Conclusion C6: Recommend the composite: rewrite now, a no-code Slack stopgap for sales, native Slack next quarter

C2 (MEDIUM) + C3 (MEDIUM) + C4 (MEDIUM) + GT-9? (no-code stopgap) + GT-1? (capacity)
→ weighted totals are D = 78 > A = 76 > B = 46 > C = 35, driven by irreversible value protected (×5) and certainty of value (×4)
→ no single weight change within 1 to 5 flips the winner
→ the closest move, Certainty 4 → 1, narrows D's lead over B only from 32 to 23
→ recommend D: rewrite this quarter, a no-code Slack stopgap for sales, and native Slack next quarter *[Assumes: A-11, A-15]*
→[2nd] actor lens, sales (immediate): the Slack objection stays open for a quarter, tempting reps to pre-sell a ship date
→[2nd] actor lens, enterprise account (immediate): the expansion lands
→[2nd] actor lens, enterprise account (next renewal): the account learns that committed money buys roadmap
→[2nd] actor lens, competitors (this quarter): rivals that already have Slack integrations press the gap in head-to-head deals
→[3rd] time lens (a few cycles): contract-bought roadmap requests crowd out market-wide work unless each passes a deferral-cost test
→[3rd] time lens (overrun): if the rewrite spills into a second quarter, Slack's deferral cost doubles to 2 × 5 × 0.10 × $40,000 × 3 = $120,000 central, still below $480,000

**Pre-check:** head C2 (MEDIUM), C3 (MEDIUM), C4 (MEDIUM), GT-9?, GT-1? · ?-marked: GT-9?, GT-1? · lowest cited: MEDIUM · Inputs ceiling: MEDIUM
**Confidence:** MEDIUM. The Inputs axis is short:
- C2, C3 and C4 are rated MEDIUM.
- GT-9? needs a half-day spike confirming the product emits events that a no-code tool can route to Slack.
- GT-1? needs the engineering estimate.

Inference is priced:
- If A-11 fails, D collapses to A (76), which still beats B (46) by 30.
- A-15 is handled by pre-mortem cluster K2.

Rivals: A against D is a 2-point gap, but D is at least as good as A on every criterion, so A is not a rival. Second-order check: no effect contradicts a ground truth, so no route back to Phase 2. The "roadmap-for-sale" effect works against the decision's purpose of durable, market-wide revenue; it is carried as pre-mortem cluster K4 with a named mitigation.

### Conclusion C7: Only value an option forfeits by waiting counts against deferring it, so a time-bound commitment can outweigh a larger stream that can be shifted

GT-4 (forfeit vs shift) + GT-5 (order rule for equal-length jobs)
→ choosing X first imposes exactly D_Y, and D_Y counts only what Y forfeits by waiting, never what it still receives a quarter later
→ value that merely shifts by a quarter adds only one quarter of its stream to its deferral cost
→ so a smaller, time-bound commitment can outweigh a larger revenue stream that can be shifted, and the reverse holds when the commitment can wait

**Pre-check:** head GT-4, GT-5 · ?-marked: none · lowest cited: none · Inputs ceiling: HIGH
**Confidence:** HIGH. Inputs: GT-4 and GT-5 are definitions stated in full in their entries. Inference: each hop is deduction from those definitions. Rivals: "total value decides" (section 5 Dead End 1) is ruled out by GT-5, which is unsuffixed. This chain fixes the decision rule only; every magnitude applied to it sits in the MEDIUM chains C2 to C5.

## 5. Abandoned Reasoning

### Dead End 1: Compare the two investments by total value

**What was tried:** Rank the options by total expected value, as if the loser were never built: the rewrite's $160,000 ARR at risk against Slack's $80,000 full-year ARR (20 × 0.10 × $40,000).

**Why abandoned:** The question asks what to build *next*, and capacity comes back every quarter (A-6 discarded). With equal one-quarter durations, GT-5 shows that only each option's deferral cost matters. Total value counts the part of each option's value that arrives whichever order is chosen.

**What it ruled out:** Total-value ranking as the decision quantity (C1). It survives only as the A-5 failure case, priced on C1's confidence line.

### Dead End 2: "The paying customer comes first" as a rule

**What was tried:** Choosing the rewrite because an existing customer has committed money and prospects have not (A-7).

**Why abandoned:** This is a convention, not a ground truth. C5 shows it gives the wrong answer when the commitment is not time-bound: the rewrite's deferral cost falls to $33,750, and Slack goes first whenever Δw > 0.05625.

**What it ruled out:** Deciding by who is asking. The deciding fact is whether waiting forfeits the expansion (A-2).

### Dead End 3: Split the quarter between the two

**What was tried:** Half the quarter on each investment.

**Why abandoned:** GT-1? says the quarter funds at most one investment. Half a rewrite meets no contracted acceptance criteria, and half a Slack integration ships nothing to prospects. Splitting delays both, so it incurs both deferral costs, $480,000 + $60,000 = $540,000 central, under a time-bound commitment.

**What it ruled out:** An engineering split. The composite that survives (option D in C6) adds only non-engineering work alongside the rewrite.

### Dead End 4: Slack first, unconditionally (the strongest rival to the headline)

**What was tried:** Building Slack first because demand comes from many prospects rather than one account.

**Why abandoned:** Under a time-bound commitment, Slack's deferral cost matches the rewrite's only at Δw = 0.80 (C4), an 80-point win-rate uplift. Breadth of demand is already priced into C3's bracket.

**What it ruled out:** Slack-first under the natural reading of the problem. Slack-first stays live only in the no-deadline reading, and only above about 5.6 points of uplift (C5).

### Dead End 5: Use the count of requests as the measure of Slack demand

**What was tried:** Treating "repeatedly requested" as evidence of how much revenue Slack would bring.

**Why abandoned:** A request is a stated preference. The revenue quantity is the win-rate change on deals that would otherwise be lost (A-4). Request counts carry no information about that change.

**What it ruled out:** Request volume as an input. C3 uses a win-rate bracket instead, and C5 names the measurement that would replace it.

## 6. Conclusion

**Recommended approach:** Build the reporting rewrite this quarter, scoped to the contract's acceptance criteria. Give sales a no-code Slack stopgap now, and build the native Slack integration next quarter (chain C6). This holds under the natural reading that the committed expansion depends on delivery this quarter. Under that reading, deferring the rewrite forfeits about $480,000 of lifetime revenue, against $12,000 to $120,000 for deferring Slack (chain C4).

**Key insight:** This is an ordering decision, not an either/or. The question is not which investment is worth more but which one loses more by waiting a quarter (chain C1). A time-bound contractual commitment forfeits value when delayed, while most Slack demand survives a one-quarter wait. That asymmetry, not the fact that a customer is paying, is what favours the rewrite (chain C7, chain C4).

**Verify before committing engineers:** Read the order form or contract for the expansion's deadline and binding status. If the expansion does not lapse on a one-quarter delay, the rewrite's deferral cost falls to $33,750. Slack should then go first if its measured win-rate uplift exceeds about 5.6 points (chain C5).

**Trade-offs acknowledged:** About 0.5 Slack-requesting deals, $20,000 ARR (bracket $4,000 to $40,000), are expected to be lost during the quarter (chain C3). Rewrite overrun would double Slack's deferral cost to $120,000 central, still below the rewrite's $480,000. Buying roadmap with contracts sets a precedent that needs a deferral-cost test on future requests (chain C6).

**Pre-check:** head C1 (MEDIUM), C2 (MEDIUM), C3 (MEDIUM), C4 (MEDIUM), C5 (MEDIUM), C6 (MEDIUM), C7 (HIGH) · ?-marked: none · lowest cited: MEDIUM · Inputs ceiling: MEDIUM
**Confidence:** MEDIUM. The decision rule itself is HIGH (chain C7). Every chain that applies magnitudes to it (chains C1, C2, C3, C4, C5 and C6) is rated MEDIUM, because every magnitude is an illustrative estimate or a user statement with no source. The single input that would reverse the recommendation is whether the expansion is time-bound (A-2, carried in C2). Reading the contract removes it as a cause of the downgrade. The illustrative magnitudes matter far less: the rewrite leads under a time-bound commitment for any expansion above $50,000 ARR, even at Slack's upper bracket with zero churn exposure (chain C4).
## Appendix — process output

## Reduce-to-primitives drill on GT-2? (process output)

**Claim:** "An existing enterprise account has committed contract expansion against the reporting rewrite."

| Constituent | Reducible? | Verdict |
|---|---|---|
| Expansion amount E | No, a contract figure | Assumed — unverified (GT-6? estimate $150,000 ARR) |
| Binding status (signed or verbal) | No, a contract fact | Assumed — unverified (A-3) |
| Deadline: does a late rewrite void or endanger the expansion? | No, a contract clause | Assumed — unverified (A-2), the decisive branch |
| Acceptance criteria that define "delivered" | No, a contract or SOW fact | Assumed — unverified (A-15) |

Parent claim: all four branches are assumed, so the parent keeps its `?`. All four primitives sit in one document, the order form or contract, so a single read verifies the whole drill.

## Trade-off analysis (process output)

### Options
- **A**: rewrite this quarter, Slack next quarter.
- **B**: Slack this quarter, rewrite next quarter.
- **C**: status quo, neither (the quarter goes to other backlog).
- **D** (composite): A, plus a no-code Slack stopgap (Workflow Builder, Zapier or email-to-channel) run by sales and solutions staff with no product engineering.
- **Engineering split (half and half)**: knocked out by must-have M1 (GT-1?: at most one investment funded); see section 5 Dead End 3.

Must-haves: M1, respects GT-1? (no engineering spend on both). A, B, C and D pass.

### Criteria & Weights
Weights were locked before scoring. Higher is always better.

| Criterion | Weight | 1 means | 5 means |
|---|---|---|---|
| Irreversible value protected (lifetime revenue that choosing this avoids forfeiting) | 5 | < $10k | > $250k (2 = $10–50k, 3 = $50–100k, 4 = $100–250k) |
| Certainty of the protected value | 4 | inferred from unprompted requests | signed contract term (3 = written intent) |
| Existing-revenue retention | 3 | no existing ARR exposed | > $250k base ARR protected |
| Delivery predictability within one quarter | 3 | rewrite of an existing surface with migration, scope unknown | bounded additive feature, or nothing to deliver |
| Breadth (accounts or prospects benefiting) | 2 | one account | > 20 accounts or prospects |
| Option value (keeps the other option viable next quarter) | 2 | forecloses the other | other fully viable next quarter |

### Scoring
| Option | Irrev. (×5) | Certainty (×4) | Retention (×3) | Delivery (×3) | Breadth (×2) | Option value (×2) | Total |
|---|---|---|---|---|---|---|---|
| A | 5×5=25 (C2 $480k) | 4×4=16 (GT-2? "committed", unsigned status unknown) | 5×3=15 (GT-6? $400k base) | 2×3=6 (A-8) | 2×2=4 (one account) | 5×2=10 (Slack viable next quarter, C3) | **76** |
| B | 3×5=15 (C3 $60k central) | 1×4=4 (GT-3? requests only) | 1×3=3 | 4×3=12 | 4×2=8 (GT-7? 20 deals per year) | 2×2=4 (expansion may lapse, C2) | **46** |
| C | 1×5=5 | 1×4=4 | 1×3=3 | 5×3=15 | 1×2=2 | 3×2=6 | **35** |
| D | 5×5=25 | 4×4=16 | 5×3=15 | 2×3=6 | 3×2=6 (stopgap reaches prospects, GT-9?) | 5×2=10 | **78** |

Sum checks: A = 25+16+15+6+4+10 = 76; B = 15+4+3+12+8+4 = 46; C = 5+4+3+15+2+6 = 35; D = 25+16+15+6+6+10 = 78. All four were recomputed by script and match.

### Recommendation
**D (78)**, ahead of A (76), B (46) and C (35).

**Flip test:** every single-criterion weight move across 1 to 5 was enumerated, and none flips the winner. D is at least as good as A on every criterion, so no weight makes A win. Against B (gap 32), the closest move is Certainty 4 → 1, which narrows the gap to 32 − 3×3 = 23. Retention 3 → 1 or Irreversible value 5 → 1 each narrow it to 24. Delivery 3 → 5 narrows it to 28.

The result is robust to weights. It is not robust to the A-2 input, which varies scores rather than weights; C5 covers that case.

## Assumption Audit scan (process output)

| Chain | Step | Step Text (brief) | Assumption surfaced? | Added to Table? |
|---|---|---|---|---|
| C1 | 1 | both finished in two quarters, order decides who waits | A-5 (already in table) | no, already present |
| C1 | 2 | deferral cost is the deciding quantity | none | n/a |
| C2 | 1 | delay forfeits $120,000 expansion | A-2, A-3 (already in table) | no, already present |
| C2 | 2 | $40,000 base exposed | A-9 (already in table) | no, already present |
| C2 | 3 | $160,000 ARR at risk | none | n/a |
| C2 | 4 | × 3 years = $480,000 | A-13: L applies equally to both sides | yes, A-13 added |
| C3 | 1 | 5 deals per quarter | none | n/a |
| C3 | 2 | 0.5 incremental wins | A-4 (present); A-14: prospects deciding in the quarter are lost permanently | yes, A-14 added |
| C3 | 3 | $20,000 ARR | none | n/a |
| C3 | 4 | $60,000 lifetime | A-13 (same assumption as C2 step 4) | no, already added once |
| C3 | 5 | bracket $12,000 to $120,000 | none | n/a |
| C4 | 1 | $480,000 vs $12,000–$120,000 | none | n/a |
| C4 | 2 | 4× / 8× | none | n/a |
| C4 | 3 | break-even Δw 0.80 | none | n/a |
| C4 | 4 | E floor $50,000 | none | n/a |
| C4 | 5 | rewrite first | none | n/a |
| C5 | 1 | delay shifts rather than forfeits | not-A-2 (A-2 present) | no, already present |
| C5 | 2 | $33,750 | none | n/a |
| C5 | 3 | inside bracket, ends disagree | none | n/a |
| C5 | 4 | break-even Δw 0.05625 | none | n/a |
| C5 | 5 | settled by measured uplift | none | n/a |
| C6 | 1 | weighted totals | none | n/a |
| C6 | 2 | no single weight change flips | none | n/a |
| C6 | 3 | closest flip narrows gap to 23 | none | n/a |
| C6 | 4 | recommend D | A-11 (present); A-15: rewrite scope narrow enough to deliver in the quarter | yes, A-15 added |
| C6 | 5 | [2nd] sales objection open | none | n/a |
| C6 | 6 | [2nd] expansion lands | none | n/a |
| C6 | 7 | [2nd] account learns money buys roadmap | none | n/a |
| C6 | 8 | [2nd] competitors press the gap | none | n/a |
| C6 | 9 | [3rd] contract-bought requests crowd out market work | none | n/a |
| C6 | 10 | [3rd] overrun doubles Slack cost | A-8 (already in table) | no, already present |
| C7 | 1 | X first imposes exactly D_Y; only forfeited value counts | none | n/a |
| C7 | 2 | shifted value adds one quarter of its stream | none | n/a |
| C7 | 3 | time-bound can outweigh larger stream that can be shifted, and the reverse | none | n/a |

## Techniques not applied (process output)

Techniques not applied:
- theoretical-limit (Phase 1) — not applicable — the core question compares two cash flows and has no physical or law-imposed ceiling to separate from a convention
- theoretical-limit (Phase 4) — not applicable — no conclusion needs a law-permitted ceiling; the binding quantities are contract terms and win rates
- fishbone (Phase 2) — not applicable — the assumption space split cleanly by option and contract term (15 rows) without a cause-category brainstorm
- inversion (Phase 2) — not applicable — the assumption set was not thin, and failure enumeration for this plan runs as the Phase 5 pre-mortem

## Adversarial pass (process output)

**Recompute:** each figure was redone by script, independently of the chain text:

| Figure | Arithmetic | Recomputed value | Matches? |
|---|---|---|---|
| Deals per quarter | 20 ÷ 4 | 5 | yes (C3) |
| Expansion forfeited | (0.9 − 0.1) × 150,000 | 120,000 | yes (C2) |
| Churn exposure | 0.10 × 400,000 | 40,000 | yes (C2) |
| ARR at risk | 120,000 + 40,000 | 160,000 | yes (C2) |
| Rewrite lifetime forfeit | 160,000 × 3 | 480,000 | yes (C2) |
| Slack wins, low / central / high | 5 × 0.02 / 0.10 / 0.20 | 0.1 / 0.5 / 1.0 | yes (C3) |
| Slack ARR, low / central / high | wins × 40,000 | 4,000 / 20,000 / 40,000 | yes (C3, section 6) |
| Slack lifetime, low / central / high | ARR × 3 | 12,000 / 60,000 / 120,000 | yes (C3) |
| Ratio to Slack upper / centre | 480,000 ÷ 120,000; 480,000 ÷ 60,000 | 4 / 8 | yes (C4) |
| Break-even Δw, time-bound | 480,000 ÷ (5 × 40,000 × 3 = 600,000) | 0.80 | yes (C4) |
| E floor, Δc = 0, at Slack's upper bracket | 120,000 ÷ (0.8 × 3 = 2.4) | 50,000 | yes (C4) |
| Rewrite shift cost, no deadline | 150,000 × 0.9 × 0.25 | 33,750 | yes (C5) |
| Break-even Δw, no deadline | 33,750 ÷ 600,000 | 0.05625 | yes (C5) |
| Slack full-year ARR (A-5 failure case) | 20 × 0.10 × 40,000 | 80,000 | yes (C1) |
| Break-even Δw (A-5 failure case) | 160,000 ÷ (20 × 40,000) | 0.20 | yes (C1) |
| Slack cost on a two-quarter slip | 2 × 5 × 0.10 × 40,000 × 3 | 120,000 | yes (C6) |
| A-9 failure (Δc = 0) | 120,000 × 3 | 360,000 | yes (C2) |
| Split-quarter cost | 480,000 + 60,000 | 540,000 | yes (section 5) |
| Trade-off totals | see trade-off block | A 76, B 46, C 35, D 78 | yes (C6) |

Direction check: each scaled-up figure lands above its base, and every lifetime figure is three times its ARR.

**Sensitivity:** the ground truth whose falsity flips the conclusion is **GT-2?**, through its deadline primitive A-2. It is `?`-marked and cannot be verified within this analysis because no contract was supplied. A confidence caveat applies, named on section 6's Confidence line, and the C5 decision rule covers the case where it is false.

Weakest link per chain:
- C1: A-5, priced on its line.
- C2: A-2.
- C3: the Δw bracket, A-4.
- C4: inherited from C2's A-2.
- C5: the measured Δw.
- C6: GT-9? feasibility, A-11. If it fails, D collapses to A and the recommendation stands.

**Rival:**
- Headline (C6, C4): Slack first, in section 5 Dead End 4, ruled out by C4.
- C1: total value decides, in section 5 Dead End 1, ruled out by GT-5.
- C2: the expansion is lost even if the rewrite is delivered. Priced by p_on = 0.9, so it is not live.
- C3: Slack also lifts existing-customer retention. Absorbed in the upper bracket (A-10).
- C5: rival not applicable. Its endpoint is a conditional rule whose two branches already contain both orders.
- Composite against A: D is at least as good as A on every criterion, so there is no live rival.
- C7 (added in the gate's Fix step): total value decides, in section 5 Dead End 1, ruled out by GT-5.

**Premise:** It is six months from now. We built the reporting rewrite, and the plan failed badly. What caused it?

**Causes** (unfiltered, from five named viewpoints):
- Engineering lead: the rewrite took two quarters because data migration and legacy report parity were never scoped.
- Engineering lead: "delivered" was argued over because no written acceptance criteria existed.
- Engineering lead: the no-code stopgap needed webhook events the product does not emit, so engineers were pulled in after all.
- Enterprise account sponsor: the expansion was a verbal promise; procurement never signed, and the budget moved.
- Enterprise account sponsor: the rewrite matched our idea of reporting, not the specific reports the sponsor needed.
- VP Sales: prospects asking for Slack went to a competitor; three named losses cited Slack.
- VP Sales: reps pre-sold a Slack date, the date slipped, and two prospects felt misled.
- CFO: the expansion had no deadline, so a quarter of Slack-driven deals was given up for nothing.
- CFO: the account now asks for a bespoke feature every renewal, priced as an expansion.
- Competitor: we used the quarter to make "no native Slack" the first slide of our competitive deck.

**Clusters:**
- **K1, unverified commitment terms.** Covers the verbal promise, no deadline, and mismatched reports. Bears on GT-2?, A-2, A-3, C2 and C4. Triage: costly but survivable.
- **K2, unscoped rewrite.** Covers the two-quarter overrun and the disputed "delivered". Bears on A-8, A-15 and C6. Triage: costly but survivable.
- **K3, Slack demand underestimated.** Covers the competitor losses, the competitive deck, and the failed stopgap. Bears on GT-3?, GT-7?, GT-9?, C3 and A-11. Triage: costly but survivable.
- **K4, roadmap capture.** Covers the bespoke feature each renewal and the pre-sold dates. Bears on C6's second-order hops. Triage: tolerable in one quarter, costly over many.

**Disposition:**
- **K1, plan change:** before sprint 1, account management obtains the signed order form. It must state the expansion amount, the delivery deadline and the report-level acceptance criteria. Tripwire: no signed terms by the end of week 2, seen by the head of product at the week-2 review. If it fires, re-decide using C5's 5.6-point rule.
- **K2, plan change:** scope the rewrite to the contracted acceptance criteria only, and defer legacy parity. Tripwire: under 50% of acceptance criteria demoed by week 6, seen by the engineering lead at the mid-quarter demo. If it fires, descope.
- **K3, accepted risk with named mitigation:** run the no-code stopgap after a half-day feasibility spike, and publish a dated Slack commitment for next quarter. Tripwire: three or more closed-lost deals in the quarter citing Slack (3 × $40,000 = $120,000 ARR, three times C3's upper ARR bracket of $40,000), seen by sales ops in the monthly loss review. If it fires, re-check C3's Δw.
- **K4, accepted risk with named mitigation:** adopt a rule that any contract-committed roadmap item must pass the same deferral-cost comparison as C4 before it is accepted. The product lead owns the rule.

**Falsification:** the conclusion is false if the contract shows the expansion does not lapse, and is not endangered, on a one-quarter delay, **and** measured Slack win-rate uplift exceeds about 5.6 points (C5). It is also false if the expansion turns out to be non-binding intent worth well under $50,000 ARR (C4's floor).

## §6→§4 closure ledger (process output)

- "Build the reporting rewrite this quarter ... no-code Slack stopgap ... native Slack integration next quarter" → chain C6 ✓ (and C4 for the $480,000 vs $12,000–$120,000 comparison) ✓
- "This is an ordering decision, not an either/or ... which one loses more by waiting a quarter" → chain C1 ✓, asymmetry → chain C7 ✓, chain C4 ✓
- "Read the order form or contract ... Slack should then go first if its measured win-rate uplift exceeds about 5.6 points" → chain C5 ✓
- "About 0.5 Slack-requesting deals, $20,000 ARR ... expected to be lost; overrun ...; precedent" → chain C3 ✓, chain C6 ✓
- "Pre-check: head C1 ... C6 (MEDIUM), C7 (HIGH) · Inputs ceiling: MEDIUM" → chains C1–C7 ✓
- "Confidence: MEDIUM ... decision rule HIGH ... rewrite leads for any expansion above $50,000 ARR" → chains C1–C7 ✓, floor → chain C4 ✓

No claim cut.

## Self-audit scan (process output)

| Chain | Chain Head (brief) | Form conforming? | Rule applied | Dependency clean? | Band | Act attempted? | Edges fired |
|---|---|---|---|---|---|---|---|
| C1 | GT-1? + GT-5 | yes | n/a | yes | MEDIUM | no | none |
| C2 | GT-2? + GT-4 + GT-6? + GT-8? | unreached | R8 (hop leading with a GT-N id) and R10 (hop closing its own sentence) at hops 3–4 sit outside the check's reach; a manual read found neither | yes | MEDIUM | no | none |
| C3 | GT-3? + GT-4 + GT-7? + GT-8? | unreached | R8 and R10 at hops 3–5 outside the check's reach; manual read found neither | yes | MEDIUM | no | none |
| C4 | C1 + C2 + C3 | unreached | R8 and R10 at hops 3–5 outside the check's reach; manual read found neither | yes | MEDIUM | no | none |
| C5 | C1 + C3 + GT-6? | unreached | R8 and R10 at hops 3–5 outside the check's reach; manual read found neither | yes | MEDIUM | no | none |
| C6 | C2 + C3 + C4 + GT-9? + GT-1? | unreached | R8 and R10 at hops 3–11 outside the check's reach; manual read found neither | yes (C2, C3, C4 upstream; no cycle) | MEDIUM | no | none |
| C7 | GT-4 + GT-5 | unreached | R8 and R10 at hop 3 outside the check's reach; manual read found neither | yes | HIGH | no (definitions stated in full in their entries; nothing external to open) | Fix/Repeat loop (added in the gate's Fix step) |

`Act attempted?` is `no` on every row because no ground truth cites a source that could be opened. Every `?` input is user-stated or an estimate, each with a Phase 3 failure record (no source cited). That shape is disclosed on every chain's Confidence line.

| §6 Span (brief) | Construct | Claim under R11? | R11 clause applied | Chain cited |
|---|---|---|---|---|
| Recommended approach: build rewrite, stopgap, Slack next quarter | bold lead-in | yes | bold lead-in whose colon closes the bold span | C6, C4 |
| Key insight: ordering decision, deferral cost | bold lead-in | yes | bold lead-in whose colon closes the bold span | C1, C7, C4 |
| Verify before committing engineers: contract read, 5.6-point rule | bold lead-in | yes | bold lead-in whose colon closes the bold span | C5 |
| Trade-offs acknowledged: 0.5 deals, overrun, precedent | bold lead-in | yes | bold lead-in whose colon closes the bold span | C3, C6 |
| Pre-check: head C1–C7, ceiling MEDIUM | bold lead-in | yes | bold lead-in whose colon closes the bold span | C1, C2, C3, C4, C5, C6, C7 (via head) |
| Confidence: MEDIUM, rule HIGH, A-2 decisive, $50,000 floor | bold lead-in | yes | bold lead-in whose colon closes the bold span | C7, C1, C2, C3, C4, C5, C6 |

```text
Scan complete: 7 chain rows, one per section-4 chain block in order; 6 section-6 rows, one per construct in order — 6 claims under R11, 0 excluded. 0 chains malformed, 0 claims untraced.
```

## Self-Audit Gate (process output)

**Pass 1 (before re-score):** Criterion 1 Sound · Criterion 2 Rigorous · Criterion 3 Hand-wavy · Criterion 4 Rigorous · Criterion 5 Rigorous · Criterion 6 Rigorous · Gate cleared: yes · Hand-wavy cap cleared: yes

Fix applied, a single re-perception pass:
- Criterion 1: the success criterion "every computed figure shows its arithmetic and was recomputed" was not a property of the Conclusion. It was rewritten so it can be checked against the Conclusion.
- Criterion 3: GT-4 and GT-5 are unsuffixed, with reachable sources (definitions stated in full), yet fed only MEDIUM chains. Chain C7, built from GT-4 and GT-5 alone and rated HIGH, was added; section 6 and both scan tables were updated.

**Criterion 1: Identify Essence**
Quoted span: "For every dollar figure it states, the Conclusion cites the section-4 chain whose hop shows that figure's arithmetic."
Band: **Rigorous**
Justification: The Essence Statement names the ordering question ("which order of the two loses the least value") rather than the triggering either/or. Every success criterion, including this rewritten one, is now a test a reviewer can apply by scanning section 6.

**Criterion 2: Challenge Assumptions**
Quoted span: "| C2 | 4 | × 3 years = $480,000 | A-13: L applies equally to both sides | yes, A-13 added |"
Band: **Rigorous**
Justification: All 15 rows use the four-type scheme, with token-first em-dash verdicts. Nine rows are challenged or discarded, and unverified rows read "unverified — flagged". The Assumption Audit has one row per step across C1 to C7 and added A-13, A-14 and A-15 to the table.

**Criterion 3: Establish Ground Truths**
Quoted span: "enumerated GT-1?, GT-2?, GT-3?, GT-6?, GT-7?, GT-8?, GT-9?; the list carries `?` on exactly those seven, and the unsuffixed GT-4 and GT-5 now feed HIGH chain C7 with read-at-source 'stated in full in this entry'"
Band: **Rigorous**
Justification: I checked the enumeration against the list and it matches. Every `?` entry carries a Phase 3 failure record (no source cited). Both unsuffixed ground truths with reachable sources now feed a HIGH chain and name their read location.

**Criterion 4: Reason Upward**
Quoted span: "| C1 | GT-1? + GT-5 | yes | n/a | yes | MEDIUM | no | none |" and, for hop validity, "→ Slack would only match at Δw = $480,000 ÷ (5 × $40,000 × 3) = 0.80"
Band: **Rigorous**
Justification: All seven chains are in arrow-led form with intermediate hops and parenthesised head inputs, and the dependency columns read clean. Six rows read `unreached` for positions beyond the check, a disclosed instrument gap; a direct read of section 4 found no GT-led or sentence-closing hop. Every figure recomputes in the adversarial pass. Section 5 holds five dead ends in What-was-tried / Why-abandoned / What-it-ruled-out form, and no analogy is used as evidence.

**Criterion 5: Validate**
Quoted span: "**Confidence:** MEDIUM. The decision rule itself is HIGH (chain C7). Every chain that applies magnitudes to it (chains C1, C2, C3, C4, C5 and C6) is rated MEDIUM"
Band: **Rigorous**
Justification: Each MEDIUM line names its short axis, its `?` inputs with the verification that would remove them (read the contract, CRM closed-lost data, the engineering estimate, a stopgap spike) and its sub-HIGH cited chains. C7 is HIGH on unsuffixed definitional inputs with its rival ruled out by GT-5. The Conclusion equals its weakest contributing chain. The adversarial record carries Recompute, Sensitivity, Rival, a past-tense Premise, causes from five named viewpoints, clusters K1 to K4 citing chain and ground-truth ids, a disposition per cluster, and Falsification.

**Criterion 6: Conclusion-to-Ground-Truth Traceability**
Quoted span: "| Key insight: ordering decision, deferral cost | bold lead-in | yes | bold lead-in whose colon closes the bold span | C1, C7, C4 |" and "the question is not which investment is worth more but which one loses more by waiting a quarter"
Band: **Rigorous**
Justification: All six section-6 constructs are claims, and each cites a chain (0 untraced). The Key Insight states a finding the "paying customer first" convention misses (section 5 Dead End 2) rather than restating the recommendation.

**Gate result:** cleared · passes: 2 · Fix/Repeat fired: yes

## Structured summary (process output)

```json
{
  "schema_version": 1,
  "run_mode": "full-composer",
  "assumptions": [
    {
      "id": "A-1",
      "type": "current constraint",
      "verdict": "Accept"
    },
    {
      "id": "A-2",
      "type": "untested belief",
      "verdict": "Challenge"
    },
    {
      "id": "A-3",
      "type": "untested belief",
      "verdict": "Challenge"
    },
    {
      "id": "A-4",
      "type": "untested belief",
      "verdict": "Challenge"
    },
    {
      "id": "A-5",
      "type": "untested belief",
      "verdict": "Accept"
    },
    {
      "id": "A-6",
      "type": "convention",
      "verdict": "Discard"
    },
    {
      "id": "A-7",
      "type": "convention",
      "verdict": "Discard"
    },
    {
      "id": "A-8",
      "type": "untested belief",
      "verdict": "Challenge"
    },
    {
      "id": "A-9",
      "type": "untested belief",
      "verdict": "Accept"
    },
    {
      "id": "A-10",
      "type": "untested belief",
      "verdict": "Challenge"
    },
    {
      "id": "A-11",
      "type": "untested belief",
      "verdict": "Challenge"
    },
    {
      "id": "A-12",
      "type": "convention",
      "verdict": "Accept"
    },
    {
      "id": "A-13",
      "type": "untested belief",
      "verdict": "Accept"
    },
    {
      "id": "A-14",
      "type": "untested belief",
      "verdict": "Accept"
    },
    {
      "id": "A-15",
      "type": "untested belief",
      "verdict": "Challenge"
    }
  ],
  "ground_truths": [
    {
      "id": "GT-1",
      "read_at_source": false
    },
    {
      "id": "GT-2",
      "read_at_source": false
    },
    {
      "id": "GT-3",
      "read_at_source": false
    },
    {
      "id": "GT-4",
      "read_at_source": true
    },
    {
      "id": "GT-5",
      "read_at_source": true
    },
    {
      "id": "GT-6",
      "read_at_source": false
    },
    {
      "id": "GT-7",
      "read_at_source": false
    },
    {
      "id": "GT-8",
      "read_at_source": false
    },
    {
      "id": "GT-9",
      "read_at_source": false
    }
  ],
  "chains": [
    {
      "id": "C1",
      "confidence": "MEDIUM",
      "rests_on": [
        "GT-1?",
        "GT-5"
      ]
    },
    {
      "id": "C2",
      "confidence": "MEDIUM",
      "rests_on": [
        "GT-2?",
        "GT-4",
        "GT-6?",
        "GT-8?"
      ]
    },
    {
      "id": "C3",
      "confidence": "MEDIUM",
      "rests_on": [
        "GT-3?",
        "GT-4",
        "GT-7?",
        "GT-8?"
      ]
    },
    {
      "id": "C4",
      "confidence": "MEDIUM",
      "rests_on": [
        "C1",
        "C2",
        "C3"
      ]
    },
    {
      "id": "C5",
      "confidence": "MEDIUM",
      "rests_on": [
        "C1",
        "C3",
        "GT-6?"
      ]
    },
    {
      "id": "C6",
      "confidence": "MEDIUM",
      "rests_on": [
        "C2",
        "C3",
        "C4",
        "GT-9?",
        "GT-1?"
      ]
    },
    {
      "id": "C7",
      "confidence": "HIGH",
      "rests_on": [
        "GT-4",
        "GT-5"
      ]
    }
  ],
  "dead_ends": [
    "Compare the two investments by total value",
    "\"The paying customer comes first\" as a rule",
    "Split the quarter between the two",
    "Slack first, unconditionally (the strongest rival to the headline)",
    "Use the count of requests as the measure of Slack demand"
  ],
  "techniques": {
    "applied": [
      "five-whys",
      "estimate",
      "trade-off",
      "second-order",
      "pre-mortem"
    ],
    "not_applied": [
      {
        "technique": "theoretical-limit",
        "phase": 1,
        "reason": "the core question compares two cash flows and has no physical or law-imposed ceiling to separate from a convention"
      },
      {
        "technique": "theoretical-limit",
        "phase": 4,
        "reason": "no conclusion needs a law-permitted ceiling; the binding quantities are contract terms and win rates"
      },
      {
        "technique": "fishbone",
        "phase": 2,
        "reason": "the assumption space split cleanly by option and contract term (15 rows) without a cause-category brainstorm"
      },
      {
        "technique": "inversion",
        "phase": 2,
        "reason": "the assumption set was not thin, and failure enumeration for this plan runs as the Phase 5 pre-mortem"
      }
    ]
  },
  "gate": {
    "passes": [
      {
        "bands": [
          "Sound",
          "Rigorous",
          "Hand-wavy",
          "Rigorous",
          "Rigorous",
          "Rigorous"
        ],
        "gate_cleared": true,
        "hand_wavy_cap_cleared": true
      },
      {
        "bands": [
          "Rigorous",
          "Rigorous",
          "Rigorous",
          "Rigorous",
          "Rigorous",
          "Rigorous"
        ],
        "gate_cleared": true,
        "hand_wavy_cap_cleared": true
      }
    ],
    "fix_repeat_fired": true,
    "cleared": true
  },
  "re_entry": {
    "fired": true,
    "edges": [
      {
        "edge": "the Self-Audit Gate's Fix/Repeat loop",
        "trigger": "Criterion 1 scored Sound and Criterion 3 Hand-wavy on the first pass; the gate cleared, but both were revised once and re-scored."
      }
    ]
  },
  "conclusion": {
    "recommendation": "Build the reporting rewrite this quarter, scoped to the contract's acceptance criteria. Give sales a no-code Slack stopgap now, and build the native Slack integration next quarter (chain C6). This holds under the natural reading that the committed expansion depends on delivery this quarter. Under that reading, deferring the rewrite forfeits about $480,000 of lifetime revenue, against $12,000 to $120,000 for deferring Slack (chain C4).",
    "confidence": "MEDIUM"
  }
}
```
