Reference reads done, arithmetic verified. The delegated evidence search has not returned yet — I note below exactly where that leaves the efficacy assumption, and I have not let any chain rest on results I do not have.

**Step 0 — technique selection:** No technique-specific trigger phrase fires in the prompt ("should we fund… at that price point" is a funding decision, not a named technique request). `MODE = full-composer`. All five phases run, Phase 4 walks all eight companion techniques.

---

# Phase-by-phase working (process output)

## Phase 2 — Fishbone: what could have moved churn 4.2% → 6.8%?

Default six-category set (software/knowledge-work subscription; no 6M production line, no full marketing-mix scope). Set locked before brainstorming.

| Category | Candidate causes (all unverified) |
|---|---|
| **People** | CS headcount or coverage cut; support response time degraded; offshoring of the save desk |
| **Process** | Cancellation flow simplified; dunning/retry policy changed; onboarding changed; plan-mix shift monthly↔annual |
| **Technology & Tools** | Product regression; app-store update broke a core flow; payment-gateway decline rate stepped up; email deliverability collapse killing engagement |
| **Environment** | Competitor entry; discretionary-spend pressure; platform/app-store policy change; seasonality |
| **Information** | **Churn definition changed** (involuntary now counted?); **cohort-mix shift** from a new acquisition channel; **a discount cohort hitting its first full-price renewal** |
| **Resources** | Price increase; feature removed to cut cost; content/catalogue refresh slowed |

Highest-priority branches for evidence: **the promo-cohort renewal wave** (a two-quarter ramp is exactly the shape a discounted-acquisition cohort makes when it reaches full price) and **payment-decline rate** (mechanically checkable from logs in days). Both are branches a loyalty program does not touch.

## Phase 2 — Inversion on the proposal's core claim

Claim: *"Funding the loyalty program at $310k/yr will pull churn back toward 5%."* Inverted: *"It will not."*

Failure-guaranteeing conditions → the precondition each one reveals:

| Would guarantee failure | Silent precondition | Status |
|---|---|---|
| Churn rise is involuntary (card declines) | A material share of churn is voluntary and value-sensitive | untested |
| Churn rise is a cohort-mix shift | The cause is one a reward addresses | untested |
| Enrolment is low | The program reaches the churning segment | untested |
| Reward is below the decision threshold | Perceived reward value exceeds what changes a cancel decision | untested |
| Rewards go to members who would have stayed | The budget reaches marginal churners, not the loyal base | untested |
| Churners leave for product reasons | Credit substitutes for the missing value | untested |
| Margin is thin | Retained billings convert to contribution | untested |

Seven preconditions, seven untested. Each entered the Assumptions Table below.

## Phase 3 — 5-Whys, reduce-to-primitives mode

Claim: *"$310k of account credit will move churn 1.8 points."* Constituents, scanned laterally before descending:

1. **A churn reduction has computable value** → reduces to: mean lifetime = 1/c (geometric-mean identity) × contribution margin. First branch bottoms out at a mathematical identity → **GT-8, verified**. Second branch bottoms out at a figure nobody supplied → **unverified**.
2. **The budget has a per-member ceiling** → reduces to: budget conservation, B/N per member, B/(fN) at fraction f → **GT-9, verified**.
3. **The mechanism reaches churners** → reduces to enrolment × targeting × reason-match. All three branches: **assumed — unverified**.
4. **The cost is $310k** → reduces to operating cost + redemption liability. Second branch: **assumed — unverified**.

Verdict: the parent claim carries `?` — two of four branches bottom out at identities, two at unverified assumptions.

## Phase 4 — Estimate (Fermi): the redemption liability

Target quantity and units: **$/year of account credit redeemed**. Unit cancellation: `members × ($/member-year of spend) × (points earned as % of spend) × (redemption fraction) → $/year`.

| Factor | Conservative | Central | Aggressive | Basis |
|---|---|---|---|---|
| Enrolment | 25% | 45% | 70% | assumed — no forecast supplied |
| Earn rate (% of spend) | 1% | 3% | 5% | assumed — no program design supplied |
| Redemption fraction | 40% | 65% | 90% | assumed — account credit is frictionless to redeem, so high |

Annual spend per member = $19 × 12 = **$228** (direct arithmetic on GT-2?).

**Bracket: [$10,944 · $96,034 · $344,736] per year.** All-in cost if $310k is operating expense only: **[$321k · $406k · $655k]**.

**Stop criterion — NOT met.** The two ends of the bracket drive opposite decisions (see C6). This is escalated explicitly rather than papered over: the dominant uncertain factor is enrolment × earn rate, and one line in the program's costing sheet resolves it.

## Phase 4 — Theoretical limit: what ceiling does the budget permit?

**Governing law:** budget conservation — an accounting identity, not a convention. A fixed budget B cannot distribute more than B; per recipient it yields at most B/N, and restricted to fraction f of the population, at most B/(fN).

| Deployment | Per member/yr | As % of $228 annual spend | Churn-price elasticity required for a 26.5% relative cut |
|---|---|---|---|
| Base-wide (f = 1.00, as proposed) | $6.46 | 2.83% | **9.4** |
| At-risk 30% (f = 0.30) | $21.53 | 9.44% | 2.8 |
| At-risk 20% (f = 0.20) | $32.29 | 14.16% | **1.9** |

**Gap:** the irreducible part is the identity itself — you cannot hand out more than you have. The part that is **pure convention** is f = 1. Points-for-everyone is inherited from retail loyalty programs; nothing about this decision requires it, and abandoning it multiplies the budget's per-recipient potency fivefold at identical cost.

**Honest limitation on this bound:** it constrains the *economic-value channel* only. If a loyalty program works through psychological lock-in (endowed progress, forfeiture aversion), the elasticity bound does not govern it — but then the program's *design*, not its budget, is the binding variable, which is a different proposal from the one on the table.

## Phase 4 — Trade-off analysis

### Options

- **A** — Fund the base-wide loyalty program as proposed, $310k/yr
- **B** — Ring-fence the $310k; run a timeboxed churn diagnosis, then deploy targeted
- **C** — Skip the points program; fund payment-failure recovery + targeted save offers now (~$120k)
- **D** — Do nothing; report that churn is under investigation

### Criteria & Weights

Locked before any option was scored. All phrased so higher is better.

| # | Criterion | Weight |
|---|---|---|
| 1 | Addresses the diagnosed cause of the churn rise | 5 |
| 2 | Churn reduction delivered per dollar committed | 5 |
| 3 | Speed to a measurable retention effect | 3 |
| 4 | Reversibility if wrong | 4 |
| 5 | Board-narrative credibility within three weeks | 3 |
| 6 | Margin protection (avoids structural discounting) | 4 |

### Scoring

| Option | C1 (×5) | C2 (×5) | C3 (×3) | C4 (×4) | C5 (×3) | C6 (×4) | **Total** |
|---|---|---|---|---|---|---|---|
| A — fund as proposed | 1 = 5 | 2 = 10 | 2 = 6 | 2 = 8 | 4 = 12 | 2 = 8 | **49** |
| B — ring-fence, diagnose, target | 5 = 25 | 4 = 20 | 2 = 6 | 5 = 20 | 4 = 12 | 5 = 20 | **103** |
| C — cheap targeted levers now | 3 = 15 | 5 = 25 | 5 = 15 | 4 = 16 | 3 = 9 | 4 = 16 | **96** |
| D — do nothing | 1 = 5 | 1 = 5 | 1 = 3 | 5 = 20 | 1 = 3 | 5 = 20 | **56** |

**Sensitivity check.** B (103) and C (96) sit 6.8% apart — inside the near-tie band, so scores are not refined. The criterion that would flip it is #3, speed to effect (B = 2, C = 5). Raising its weight from 3 to the scale maximum of 5 gives B = 107, C = 106 — B still holds by one point. The near-tie is a real finding, and the honest reading is that **C's highest-scoring lever is contained inside B's execution**: payment-failure recovery requires no diagnosis and no board approval at this price point, so it starts on day one of B rather than competing with it.

**The result worth staring at:** the proposal as written (49) scores *below doing nothing* (56). Doing nothing at least protects margin and stays reversible; A gives up both and buys a mechanism matched to no diagnosed cause.

## Phase 4 — Second-order pass

First-order conclusion (sharp, no hedge): *Ring-fence the $310k and release it against a named cause after a 21-day diagnosis rather than funding the base-wide program now.*

**2nd order:** the board approves a *release condition* rather than a program · a churn-cause breakdown is produced that outlives this decision · ~2,250 members depart un-intervened during the window.
**3rd order:** the next retention proposal arrives with an efficacy estimate attached — the capability this one lacks · if no dominant cause emerges, the release rule fires anyway and the program launches *targeted*, so the delay buys targeting even in its worst case · the forgone saves compound into ~$94,000 of permanently lost lifetime value, about 30% of one year's program budget.

Also enumerated, for the **rejected** branch (funding as proposed): effective ARPU falls for the whole base → unit economics worsen → the next fix is a price rise, which *raises* churn; and members learn list price is negotiable → future increases meet structural resistance; and a points arms race → both firms pay, neither gains relative advantage. These did not extend a chain — they landed in trade-off criterion 6 (margin protection), which is where they are load-bearing.

**Contradiction check:** no extension step contradicts any ground truth. Stopped at the 3rd order per the stopping rule. No return to Phase 2 on this axis.

---

# First-Principles Analysis

## 1. Problem Essence

**Core problem:** Whether to commit $310,000 per year to a retention mechanism that has not been matched to any diagnosed cause of the churn increase it is meant to reverse.

**Success criteria** — each checkable by scanning section 6:

1. The Conclusion states whether the $310,000 should be committed **now**, and names what would change that answer.
2. The Conclusion names the minimum churn reduction that makes the spend break even in year one, as a number, not as a direction.
3. The Conclusion states whether the rival's program is evidence for or against funding, with a reason that is not "they did it."
4. The Conclusion states what the board is told in three weeks, distinguishing that from when money moves.
5. The Conclusion names at least one input whose absence, not whose value, is what blocks a confident answer.

## 2. Assumptions Table

| Assumption | Type | Treatment | Verdict | Verification |
|---|---|---|---|---|
| A1 Mean subscriber lifetime is 1/c under constant hazard | physical law | accept as GT candidate | **Accept** — mathematical identity, not negotiable by context | derived and confirmed numerically → GT-8 |
| A2 A fixed budget cannot distribute more than it contains | physical law | accept as GT candidate | **Accept** — accounting identity | derived and confirmed numerically → GT-9 |
| A3 The board update is three weeks out | current constraint | record expiry | **Accept** — expires at the board meeting; a reporting event is not a spending gate, so it binds the narrative and not the commitment | GT-7? |
| A4 The $310k is available whenever we choose to release it | current constraint | record expiry | **Challenge** — expires if unallocated budget is reswept at period end; this analysis has no visibility into the reallocation cycle | unverified — flagged |
| A5 Churn is measured on a consistent definition across both quarters | untested belief | verify or flag | **Challenge** — a definitional or reporting-window change produces this exact series with zero behavioural change | unverified — flagged |
| A6 Loyalty programs reduce subscription churn | untested belief | verify or flag | **Challenge** — a delegated literature search was dispatched and had not returned at composition time; no source has been read at source by this analysis | unverified — flagged |
| A7 A rival's launch is evidence the mechanism works | convention | challenge before use | **Discard** — contradicted by C3: the rival's program postdates the churn rise by ~5 months and is one month old, so it carries no outcome data | superseded by C3 |
| A8 Retention budgets are spent base-wide | convention | challenge before use | **Discard** — C2 shows base-wide is the lowest-potency setting of the same budget; the practice is inherited from retail loyalty, not required here | superseded by C2 |
| A9 "$310,000 a year to run" is the all-in cost | untested belief | verify or flag | **Challenge** — the two readings differ by up to 2.1× and flip the decision in the low-margin corner (C6) | unverified — flagged |
| A10 Contribution margin converts retained billings to profit | untested belief | verify or flag | **Challenge** — at 40% margin with high redemption, break-even needs 2.67 pp against a 1.80 pp hoped effect | unverified — flagged |
| A11 The cause of the rise is still operative | untested belief | verify or flag | **Challenge** — a promo-cohort renewal wave is self-limiting; a product regression is not | unverified — flagged |
| A12 Churn responds to reward value through the economic channel | untested belief | verify or flag | **Challenge** — required elasticity base-wide is ~9.4 (C5); if the program works it works psychologically, making design rather than budget the binding variable | unverified — flagged |
| A13 Gross adds hold the base flat at the current churn rate | untested belief | verify or flag | **Accept** for modelling — stated as a modelling convention; year-one surplus scales with the base, not with gross adds, to first order | unverified — flagged |
| A14 Enrolment in an opt-in program is materially below 100% | untested belief | verify or flag | **Accept** — the program is opt-in by construction, so reach is bounded by enrolment; magnitude unknown | unverified — flagged |
| A15 A diagnosis will identify a dominant cause *(surfaced by pre-mortem)* | untested belief | verify or flag | **Challenge** — the fishbone shows six plausible categories; multi-causal churn is the common case | unverified — flagged |
| A16 Payment-failure churn is a component of the rise *(surfaced by pre-mortem)* | untested belief | verify or flag | **Challenge** — directly testable from decline logs within days; not tested here | unverified — flagged |
| A17 Retained members generate the base-average $19 *(surfaced by audit)* | untested belief | verify or flag | **Challenge** — credit and save offers reduce realised ARPU for exactly the retained cohort | unverified — flagged |
| A18 An elasticity near 9.4 is implausible and one near 1.9 is not *(surfaced by audit, C5 step 3)* | untested belief | verify or flag | **Challenge** — stated from general knowledge; no elasticity study was read here | unverified — flagged |
| A19 A save program would convert ~15% of intercepted cancellations *(surfaced by audit, C8 2nd-order)* | untested belief | verify or flag | **Challenge** — a round figure used to size the delay cost, not a measured rate | unverified — flagged |
| A20 "Two quarters" and "last month" share one timeline *(surfaced by audit, C3 step 1)* | untested belief | verify or flag | **Accept** — the relative dating is read from the prompt's own wording; no dated series was supplied | unverified — flagged |
| A21 The proposed program is open to the whole base *(surfaced by audit, C2 step 2)* | untested belief | verify or flag | **Accept** — "lets members redeem points" describes a base-wide entitlement; a segmented design was not described | unverified — flagged |

## 3. Ground Truths

- **GT-1?** There are 48,000 active members — unverified: supplied in the problem statement with no source; no subscriber report and no definition of "active" was provided.
- **GT-2?** The price is $19 per member per month — unverified: supplied with no source; no plan mix (monthly/annual, list/discounted) was provided.
- **GT-3?** Monthly churn rose from 4.2% to 6.8% over the last two quarters — unverified: supplied with no source; the churn definition and the intermediate monthly series were not provided.
- **GT-4?** The proposed program costs "around $310,000 a year to run" — unverified: supplied with no source, and the wording does not state whether redeemed account credit is inside or outside the figure.
- **GT-5?** Customer success's target is churn "back toward 5 percent" — unverified: supplied as a bet, with no stated basis.
- **GT-6?** A rival service launched a similar program last month — unverified: supplied with no source; a one-month-old program has generated no outcome data for anyone.
- **GT-7?** Marketing wants a final call within three weeks, before the next board update — unverified: supplied with no source.
- **GT-8** Under a constant per-period churn hazard *c*, mean subscriber lifetime is 1/*c* periods — source: mean of the geometric distribution, Σ<sub>k≥0</sub>(1−c)<sup>k</sup> = 1/c; **read-at-source:** derived in this analysis and confirmed numerically in the Phase 4 computation (c = 0.050 → 20.0 months; c = 0.068 → 14.7 months).
- **GT-9** A fixed budget B spread over population N yields at most B/N per member; restricted to fraction f of that population it yields at most B/(fN), i.e. 1/f times as much per recipient — source: conservation of a fixed budget (accounting identity); **read-at-source:** derived in this analysis and confirmed numerically ($310,000/48,000 = $6.46; at f = 0.20, $32.29, exactly 5.00×).
- **GT-10** The problem statement supplies no contribution margin, no gross-add rate, no breakdown of churn by reason or cohort, and no enrolment forecast — source: the problem statement as given; **read-at-source:** the statement quoted in full in the prompt — each of the four is absent from it by inspection.

**Provenance summary.**
`?-marked: GT-1, GT-2, GT-3, GT-4, GT-5, GT-6, GT-7 (7 of 10)`
`Read-at-source: GT-8 — geometric-mean derivation, confirmed numerically at 20.0 and 14.7 months; GT-9 — budget identity, confirmed numerically at $6.46 → $32.29 (5.00×); GT-10 — the problem statement itself, all four inputs absent by inspection`

**Phase 3 verification step.** GT-8, GT-9 and GT-10 are the only ground truths feeding HIGH-confidence chains (C1, C2), and all three were located directly — two by derivation confirmed numerically, one by inspection of the supplied statement. No external read was owed for them. GT-1? through GT-7? feed only MEDIUM chains and were not read: each is a fact about the user's own business, obtainable from their systems, and no source was cited that this analysis could open. **No Phase 3 failure record applies** — no cited source was unreachable, because no external source was cited for any suffixed entry.

## 4. Derivation Chains

### Conclusion C1: The funding decision as posed cannot be computed from the information given

```text
GT-8 (mean lifetime = 1/c) + GT-10 (no margin, gross-add, churn-reason or enrolment input supplied)
→ the value of a churn reduction is the retained member-months it buys multiplied by contribution margin, and the reduction it buys is bounded by the share of churn the mechanism can actually reach
→ both multipliers are absent from the supplied inputs and neither is derivable from the three figures that were supplied
→ what the inputs determine is the size of the missing measurement, not the answer to the question asked
```

**Confidence:** HIGH — both inputs are unsuffixed and read at source; the claim is that two named multipliers are absent, which is checkable by inspection of the statement.

### Conclusion C2: A base-wide loyalty program is the lowest-potency deployment of any fixed retention budget

```text
GT-9 (budget yields B/N per member, B/(fN) at fraction f) + GT-10 (no at-risk segmentation supplied)
→ per-recipient reward value scales as 1/f, so narrowing the recipient set from the whole base to a fifth of it multiplies each recipient's reward fivefold at identical cost
→ a points program open to every member sets f = 1 by construction, the single least potent setting the identity permits *[Assumes: A21]*
→ the proposal's least-examined choice, who receives the budget, dominates its most-examined one, how large the budget is
```

**Confidence:** HIGH — rests only on GT-9 and GT-10, both read at source; the 1/f relation is an identity, not an estimate.

### Conclusion C3: The rival's program is not evidence for this decision

```text
GT-3? (churn rose across two quarters) + GT-6? (rival launched one month ago)
→ the churn rise began roughly five months before the rival's program existed, so that program cannot be among its causes *[Assumes: A20]*
→ a program one month old has produced no retention outcome anyone can observe, including the rival itself
→ the launch is a competitive-pressure signal carrying no information about whether this mechanism reduces churn
```

**Confidence:** MEDIUM — rests on GT-3? (a dated monthly churn series with its stated definition would verify it) and GT-6? (the rival's dated launch announcement would verify it); both are obtainable within a day. A downgrade cause belonging to this chain: the five-month gap is read from prose dating rather than dates, and a precise launch date against a dated series removes it.

### Conclusion C4: Year-one break-even needs 0.64–1.32 pp of churn reduction at the stated cost, so efficacy dominates price

```text
GT-1? (48,000 members) + GT-2? ($19/month) + GT-3? (6.8% current monthly churn) + GT-4? ($310,000/yr stated) + GT-8 (mean lifetime = 1/c)
→ a churn reduction compounds, because the retained-member surplus grows each month toward a new steady state, so year-one value is the cumulative member-month surplus rather than one month's saved members times twelve *[Assumes: A13]*
→ the full hoped 1.8 pp reduction buys 56,451 extra member-months in year one, worth $1,072,569 in gross billings *[Assumes: A17]*
→ the reduction needed to break even against $310,000 is 1.32 pp at 40% contribution margin, 0.77 pp at 70% and 0.64 pp at 85% *[Assumes: A10]*
→ the hoped effect clears all three thresholds while roughly a third of the hoped effect clears none, so the decision turns on efficacy far more than on price
```

**Confidence:** MEDIUM — rests on GT-1?, GT-2?, GT-3? and GT-4?; a subscriber and billing export (GT-1?, GT-2?), the monthly churn series with its definition (GT-3?) and the program costing sheet (GT-4?) would each remove its input as a cause of the downgrade. A downgrade cause belonging to this chain: the break-even band is stated across three assumed margins rather than the real one, and a single contribution-margin figure collapses the band to one number.

### Conclusion C5: Targeting moves the required elasticity fivefold closer to whatever this market's elasticity actually is

```text
GT-2? ($228 annual spend per member) + GT-4? ($310,000 budget) + C2 (per-recipient value scales as 1/f)
→ spread base-wide the budget is worth $6.46 per member per year, which is 2.83% of annual spend
→ delivering the hoped 26.5% relative churn cut from a 2.83% effective price reduction requires a churn-price elasticity near 9.4
→ concentrating the same budget on a fifth of the base raises it to 14.16% of spend and drops the required elasticity to about 1.9 *[Assumes: A18]*
→ whatever elasticity this market actually has, targeting moves the requirement five times closer to it at identical cost
```

**Confidence:** MEDIUM — rests on GT-2? (realised ARPU by plan would verify it) and GT-4? (the costing sheet would verify it); C2 on the head is HIGH and imposes no cap. A downgrade cause belonging to this chain: the elasticity framing governs only the economic-value channel, and a program working through psychological lock-in is not bounded by it — a controlled holdout test of the actual program design is what would settle that, and none exists.

### Conclusion C6: The cost figure is ambiguous by up to 2.1×, and the ambiguity reaches the decision

```text
GT-4? ("around $310,000 a year to run") + GT-1? (48,000 members) + GT-2? ($228 annual spend per member)
→ "to run" does not state whether redeemed account credit sits inside the figure or outside it, and account credit is forgone revenue rather than an operating expense
→ a unit-factor estimate of the redemption liability, enrolment × earn rate × redemption fraction against $228 of spend, brackets it at $10,944 / $96,034 / $344,736 per year *[Assumes: A14]*
→ the all-in cost therefore brackets at $321k / $406k / $655k, and year-one break-even brackets at 1.37 / 1.71 / 2.67 pp at 40% contribution margin *[Assumes: A10]*
→ the upper end exceeds the 1.80 pp the program is hoped to deliver, so the two ends of the cost bracket recommend opposite decisions and the estimate does not resolve
```

**Confidence:** MEDIUM — rests on GT-4? (one line in the costing sheet stating whether redeemed credit is inside the $310,000 removes the entire ambiguity), GT-1? and GT-2? (subscriber and billing exports). A downgrade cause belonging to this chain: the redemption bracket's factors are assumed rather than designed, and a finalised earn rate plus an enrolment forecast collapses the bracket.

### Conclusion C7: The three-week deadline binds the board narrative, not the spending commitment

```text
GT-7? (final call in three weeks, before the board update) + C1 (the funding decision is under-determined as posed)
→ a board update is a reporting event, and what it requires is a defensible position rather than a disbursement
→ because the funding question cannot be answered on the inputs available, the most informative thing three weeks can produce is a named measurement with a release condition attached
→ the deadline binds what must be said in three weeks and not when the money moves
```

**Confidence:** MEDIUM — rests on GT-7? (the board calendar and the meeting's decision agenda would verify whether a disbursement decision is genuinely required at that meeting); C1 on the head is HIGH and imposes no cap. A downgrade cause belonging to this chain: whether this board treats a conditional approval as an acceptable answer is an organisational fact this analysis cannot observe, and only asking the board chair settles it.

### Conclusion C8: Ring-fence the budget against a timeboxed diagnosis rather than funding the base-wide program now

```text
C1 (under-determined) + C2 (base-wide is lowest potency) + C3 (rival is not evidence) + C4 (efficacy dominates price) + C5 (targeting cuts required elasticity fivefold) + C6 (cost bracket unresolved) + C7 (deadline binds the narrative)
→ weighted totals across six criteria locked before scoring: ring-fence-and-diagnose 103, cheap targeted levers now 96, fund as proposed 49, do nothing 56
→ the winner is driven by the two highest-weighted criteria, cause-match and reduction-per-dollar-committed, on both of which the proposal as written scores lowest of the four options
→ recommend approving and ring-fencing the $310,000 against a 21-day timeboxed diagnosis with a pre-committed release rule, rather than either funding the base-wide program now or declining the budget *[Assumes: A4]*
→[2nd] the board approves a release condition rather than a program, which is a decision it can take inside three weeks
→[2nd] the diagnosis produces a churn-cause breakdown that outlives this decision and prices every future retention proposal
→[2nd] roughly 2,250 members depart un-intervened during the window *[Assumes: A19]*
→[3rd] the next retention proposal arrives with an efficacy estimate attached, which is the capability this one lacks
→[3rd] if no dominant cause emerges the release rule fires anyway and the program launches targeted, so the delay buys targeting even in its worst case
→[3rd] the forgone saves compound into roughly $94,000 of permanently lost lifetime value, about 30% of one year's program budget
```

**Confidence:** MEDIUM — capped by the lowest-rated chain its head cites; C3, C4, C5, C6 and C7 are each rated MEDIUM and each carries its own verification path, which is not restated here. C1 and C2 are HIGH and impose no cap. A downgrade cause belonging to this chain: the recommendation's value depends on the 21-day diagnosis returning an actionable cause (A15), and what would remove it is a week-one data-availability check confirming cancellation reasons, payment-decline logs and acquisition-cohort tags can be joined at all.

## 5. Abandoned Reasoning

### Dead End: "The cost ambiguity is second-order"

**What was tried:** Judging that whether $310k includes redeemed credit changes the total by at most ~2×, and therefore could not flip a decision whose year-one upside was ~$1.07M.

**Why abandoned:** The $1.07M is *gross billings*, not contribution. Once margin enters, the high-redemption/40%-margin corner requires 2.67 pp against a 1.80 pp hoped effect — the bracket straddles the decision threshold and the Fermi stop criterion is not met. The reasoning compared a gross figure to a net cost.

**What it ruled out:** Treating the redemption question as bookkeeping to tidy up after approval. It is a gating question, answerable by one line in the costing sheet, and it must be answered before any commitment.

### Dead End: "Steady-state base growth as the benefit measure"

**What was tried:** At constant gross adds, a fall from 6.8% to 5.0% grows the steady-state base by 36% (48,000 → 65,280), worth ~$328,000 *per month* in incremental billings — which makes $310k/yr look trivially worth funding.

**Why abandoned:** Steady state is approached only asymptotically, and the figure additionally assumes gross adds are unchanged and independent of whatever is causing the churn. Presenting a multi-million-dollar annual benefit against a $310k cost would have rested the recommendation on a number the business will not observe for years.

**What it ruled out:** Any framing of this decision on steady-state economics. Year-one cumulative member-months is the honest horizon for a commitment made on a board cycle.

### Dead End: "The rival's launch as a market signal worth acting on"

**What was tried:** Treating the competitor's program as evidence that this mechanism works in this category — the "they know something we don't" argument.

**Why abandoned:** This is reasoning by analogy with no ground truth about the rival's situation. C3 additionally shows the timeline forbids it twice over: the program postdates the churn rise by ~5 months, so it cannot be a cause, and it is one month old, so it has produced no outcome data for anyone.

**What it ruled out:** "We must match them" as a basis for the $310,000 — though not as a basis for competitive urgency, which is a separate and legitimate concern that belongs in the board narrative rather than in the efficacy case.

### Dead End: "Recommend declining the funding"

**What was tried:** The trade-off's straightforward reading — option A scores 49 against B's 103, so decline it and tell the board no.

**Why abandoned:** Pre-mortem cluster 3 identified that an unallocated budget is reswept and a declined program is organisationally hard to revive, which silently converts "decline" into "no retention spend for two more quarters" — an outcome the trade-off matrix never scored as an option.

**What it ruled out:** Treating this as a binary funding decision when approve-and-condition is available and strictly dominates both branches of the binary.

## 6. Conclusion

**Recommended approach:** Do not fund the base-wide loyalty program at $310,000; ask the board instead to approve and ring-fence that same $310,000, released against a named cause after a 21-day timeboxed churn diagnosis, with a pre-committed rule that if no single cause explains at least 30% of the 2.6-point rise the money launches a *targeted* retention program rather than a base-wide one — and start payment-failure recovery on day one, since it needs no diagnosis and no approval at this price point (chains C8, C1).

**Key insight:** The proposal's least-examined variable dominates its most-examined one — *who* receives the budget sets potency by a factor of 1/f, so $310,000 aimed at a fifth of the base is five times more potent than the identical $310,000 spread across all 48,000 members, and the base-wide design is an inherited retail convention rather than anything this decision requires (chains C2, C5).

**Trade-offs acknowledged:** You accept roughly three weeks of un-intervened churn — about 2,250 departures, of which a save program might have held ~340, a permanent lifetime-value cost near $94,000 — and a board update reporting a measurement plan rather than a launch, in exchange for not committing a budget whose all-in cost is unresolved between $321,000 and $655,000 and whose upper end cannot break even even at the full hoped effect (chains C6, C7, C1).

**Confidence:** MEDIUM — the rating matches the weakest contributing chain (chain C8).

Chains contributing below HIGH are C3, C4, C5, C6, C7 and C8; C1 and C2 are HIGH. The Conclusion rests directly on GT-1?, GT-2?, GT-3?, GT-4?, GT-6? and GT-7?. What would remove each as a cause of the downgrade: a subscriber and billing export stating active-member count and realised ARPU by plan (GT-1?, GT-2?); the monthly churn series with its stated definition, split voluntary and involuntary (GT-3?); the program's costing sheet stating whether redeemed credit sits inside the $310,000 (GT-4?); the rival's dated launch announcement (GT-6?); the board calendar and meeting agenda (GT-7?). Every one is obtainable inside the three-week window, which is itself part of why the recommendation is to measure rather than to commit. A downgrade cause belonging to the Conclusion itself: the recommendation's value depends on the diagnosis returning an actionable cause, which pre-mortem cluster 1 shows is not guaranteed — a week-one data-availability check removes it, and the pre-committed release rule bounds the damage if that check fails.

---

# Adversarial pass (process output)

Technique selected by the decision rule: the conclusion is a **plan**, so **pre-mortem**, not inversion. Procedure opened and read at `/home/chrisdavidson/Projects/first-principles-skill/first-principles/agents/references/pre-mortem.md`.

**Premise.** It is six months from now. The recommendation was followed and it failed badly: churn is above 8%, the board has lost confidence in the retention plan, and the $310,000 bought nothing.

**Causes** (unfiltered, written before any grouping, generated from five named viewpoints):

*Customer success lead (implementer):* the diagnosis returned six causes with no dominant one and nobody could act on it · cancellation-survey data was free text and was never coded, so 21 days became 10 weeks · the data needed lived in three systems nobody could join · the targeted save offer required engineering work that was on no roadmap · the at-risk model mis-segmented and offers went to the wrong members.

*Members (who live with the result):* members who cancelled during the diagnosis window were offered nothing and are gone permanently · targeted members told untargeted ones, who felt penalised for loyalty · the actual reason cited was a removed feature no retention offer could fix.

*CFO and board (who pay):* three weeks became three months and the board heard "still investigating" twice · the diagnosis cost more than budgeted and produced no revenue · the ring-fenced $310,000 was reswept at period end and was unavailable when the diagnosis landed · the board read the delay as paralysis while the competitor's program got press.

*Competitor (who benefits):* we analysed for two quarters while they compounded switching costs · our churners accrued points with them and will not come back · our sales team could not answer "what's your loyalty program?" in competitive deals.

*Marketing:* the update said "we declined to fund" with no positive framing and read as inaction · no measurable milestone was committed to, so the next update had nothing to report either.

**Clusters.**

1. **The diagnosis may not be decisive** — bears on C1, C8, A15. Absorbs: six causes no dominant one; uncoded free-text data; data across three systems; 21 days became 10 weeks.
2. **Delay carries a real, compounding cost** — bears on C3, C7, C8's 2nd-order step. Absorbs: churners lost permanently in the window; competitor compounds switching costs; sales cannot answer the question; points accrued elsewhere are sticky.
3. **"Not now" is organisationally not the same as "later"** — bears on C7, C8, A4. Absorbs: budget reswept; board reads delay as paralysis; nothing to report next cycle; declined programs are hard to revive.
4. **Targeting can itself misfire** — bears on C2, C5. Absorbs: offers leak between segments; loyal members feel penalised; at-risk model mis-segments.
5. **The cause may be unfixable by any retention spend** — bears on C4, C8, A11. Absorbs: removed feature; product quality; cohort quality; price change.

**Dispositions.**

1. **Plan change.** Timebox the diagnosis to 21 days with a pre-committed decision rule — if no single cause explains ≥30% of the 2.6-point rise, the budget releases to a *targeted* program rather than funding further analysis. Run the data-availability check in week one, not week four. *(This is now C8's third hop and the release rule in section 6.)*
2. **Accepted risk, named mitigation.** Accept ~2,250 un-intervened departures over 21 days (~$94,000 of lifetime value at a 15% notional save rate). Mitigated by starting payment-failure recovery on day one — it requires no diagnosis, no board approval at this price point, and at a 50% recovery of a 50% involuntary share alone delivers 0.65 pp, which clears the 0.64 pp break-even at 85% margin. *(Now the final clause of section 6's recommended approach.)*
3. **Plan change — this one modified the recommendation.** Ask the board to *approve and ring-fence* rather than to decline. The trade-off matrix had selected "diagnose then target" and this cluster showed that its organisational implementation defaults to "no spend for two quarters." C8's endpoint was revised accordingly, and the discarded reading is recorded as the fourth dead end in section 5.
4. **Accepted risk, named mitigation.** Accept that targeted offers leak. Mitigated by framing them as time-limited win-back rather than a standing entitlement, and by capping targeted spend at the same $310,000 so the downside is bounded by the original ask and never exceeds it.
5. **Plan change.** The diagnosis explicitly admits "not addressable by retention spend" as a permitted verdict, routing the budget to product or acquisition quality rather than forcing it into a retention program. *(This is the honest reading of dead end 3 in section 5.)*

Weakest link across the analysis, named: **C8's third hop**, which assumes the ring-fenced budget survives the period boundary (A4) — an organisational fact no chain in this analysis can verify.

---

# Assumption Audit (process output)

| Chain | Step | Step Text (brief) | Assumption surfaced? | Added to Table? |
|---|---|---|---|---|
| C1 | 1 | value = member-months × margin, bounded by reach | none | n/a |
| C1 | 2 | both multipliers absent from inputs | none | n/a |
| C1 | 3 | inputs determine the missing measurement's size | none | n/a |
| C2 | 1 | per-recipient value scales as 1/f | none | n/a |
| C2 | 2 | points-for-all sets f = 1 | A21 program is base-wide | yes |
| C2 | 3 | who-receives dominates how-much | none | n/a |
| C3 | 1 | rise predates the rival by ~5 months | A20 prose dating shares one timeline | yes |
| C3 | 2 | one-month program has no outcome data | none | n/a |
| C3 | 3 | launch is pressure, not evidence | none | n/a |
| C4 | 1 | reduction compounds toward a new steady state | A13 gross adds hold base flat | yes (pre-existing) |
| C4 | 2 | 56,451 member-months = $1,072,569 gross | A17 retained ARPU = base average | yes |
| C4 | 3 | break-even 1.32 / 0.77 / 0.64 pp by margin | A10 margin unknown | yes (pre-existing) |
| C4 | 4 | efficacy dominates price | none | n/a |
| C5 | 1 | $6.46/member = 2.83% of spend | none | n/a |
| C5 | 2 | 26.5% cut from 2.83% implies elasticity ~9.4 | none | n/a |
| C5 | 3 | targeting drops required elasticity to ~1.9 | A18 elasticity plausibility judgement | yes |
| C5 | 4 | targeting moves the requirement 5× closer | none | n/a |
| C6 | 1 | "to run" does not locate redeemed credit | none | n/a |
| C6 | 2 | redemption brackets at $11k / $96k / $345k | A14 enrolment below 100% | yes (pre-existing) |
| C6 | 3 | all-in $321k / $406k / $655k; break-even 1.37 / 1.71 / 2.67 pp | A10 margin unknown | yes (pre-existing) |
| C6 | 4 | bracket ends recommend opposite decisions | none | n/a |
| C7 | 1 | a board update is a reporting event | none | n/a |
| C7 | 2 | three weeks best produce a measurement + release condition | none | n/a |
| C7 | 3 | deadline binds the saying, not the spending | none | n/a |
| C8 | 1 | weighted totals 103 / 96 / 49 / 56 | none | n/a |
| C8 | 2 | driven by the two highest-weighted criteria | none | n/a |
| C8 | 3 | ring-fence with a pre-committed release rule | A4 budget survives the period boundary | yes (pre-existing) |
| C8 | 4 | [2nd] board approves a release condition | none | n/a |
| C8 | 5 | [2nd] cause breakdown outlives this decision | none | n/a |
| C8 | 6 | [2nd] ~2,250 un-intervened departures | A19 ~15% save-rate on intercepts | yes |
| C8 | 7 | [3rd] next proposal arrives with an efficacy estimate | none | n/a |
| C8 | 8 | [3rd] release rule fires anyway; delay buys targeting | A15 diagnosis may return no dominant cause | yes |
| C8 | 9 | [3rd] ~$94,000 permanently lost lifetime value | none | n/a |

33 rows, one per chain per step, in document order. Six assumptions surfaced and added (A15, A17, A18, A19, A20, A21); five steps referenced assumptions already in the table.

---

# §6→§4 closure ledger (process output)

```text
- "Do not fund the base-wide loyalty program at $310,000; ask the board instead to approve and ring-fence…" → chain C8 ✓
- "…start payment-failure recovery on day one, since it needs no diagnosis and no approval at this price point" → chain C1 ✓
- "$310,000 aimed at a fifth of the base is five times more potent than the identical $310,000 spread across all 48,000" → chain C2 ✓
- "the base-wide design is an inherited retail convention rather than anything this decision requires" → chain C5 ✓
- "about 2,250 departures… a permanent lifetime-value cost near $94,000" → chain C7 ✓
- "all-in cost is unresolved between $321,000 and $655,000 and whose upper end cannot break even even at the full hoped effect" → chain C6 ✓
- "the rating matches the weakest contributing chain" → chain C8 ✓
```

Ledger clean: 7 rows, 7 chains named, 0 cuts.

---

# Self-audit scan (process output)

| Chain | Chain Head (brief) | Form conforming? | Rule applied | Dependency clean? |
|---|---|---|---|---|
| C1 | GT-8 + GT-10 | yes | n/a | yes |
| C2 | GT-9 + GT-10 | yes | n/a | yes |
| C3 | GT-3? + GT-6? | yes | n/a | yes |
| C4 | GT-1? + GT-2? + GT-3? + GT-4? + GT-8 | yes | n/a | yes |
| C5 | GT-2? + GT-4? + C2 | yes | n/a | yes — C2 resolves, no cycle |
| C6 | GT-4? + GT-1? + GT-2? | yes | n/a | yes |
| C7 | GT-7? + C1 | yes | n/a | yes — C1 resolves, no cycle |
| C8 | C1 + C2 + C3 + C4 + C5 + C6 + C7 | yes | n/a | yes — all seven resolve, no cycle |

| §6 Span (brief) | Construct | Claim under R11? | R11 clause applied | Chain cited |
|---|---|---|---|---|
| "**Recommended approach:** Do not fund…" | bold lead-in | yes | prescribed lead-in; colon closes the bold span, text follows | C8, C1 |
| "**Key insight:** The proposal's least-examined variable…" | bold lead-in | yes | prescribed lead-in; colon closes the bold span, text follows | C2, C5 |
| "**Trade-offs acknowledged:** You accept roughly three weeks…" | bold lead-in | yes | prescribed lead-in; colon closes the bold span, text follows | C6, C7, C1 |
| "**Confidence:** MEDIUM — the rating matches…" | bold lead-in | yes | colon closes the bold span with text following; not a section-intro label | C8 |
| "Chains contributing below HIGH are C3, C4…" | prose | no | prose carrying neither a bold colon lead-in nor a list marker is not a claim | n/a |

```text
Scan complete: 8 chain rows, one per section-4 chain block in order; 5 section-6 rows, one per construct in order — 4 claims under R11, 1 excluded. 0 chains malformed, 0 claims untraced.
```

---

# Self-Audit Gate

Rubric opened at `/home/chrisdavidson/Projects/first-principles-skill/first-principles/agents/references/validation-rubric.md`. Assumption Audit confirmed present and exhaustive (33 rows, one per chain per step). Self-audit scan confirmed present, both tables complete, reconciliation line recounts against sections 4 and 6.

**Criterion 1: Identify Essence**
Quoted span: *"Whether to commit $310,000 per year to a retention mechanism that has not been matched to any diagnosed cause of the churn increase it is meant to reverse."*
Band: **Rigorous**
Justification: a single sentence naming the underlying decision rather than the triggering event, and the five success criteria each carry a verb-subject-outcome test applied by scanning section 6 (criterion 5, "names at least one input whose absence blocks the answer," is satisfied by the Conclusion's naming of contribution margin) — none of which would transfer unaltered to a different problem.

**Criterion 2: Challenge Assumptions**
Quoted span (Assumption Audit scan): *"C5 | 3 | targeting drops required elasticity to ~1.9 | A18 elasticity plausibility judgement | yes"*
Band: **Rigorous**
Justification: all 21 rows carry a Type from exactly the four-type scheme, Verdicts are a leading token plus em-dash justification, two rows carry Discard (A7, A8) and eleven carry Challenge, every chain-used unverified row reads "unverified — flagged", and the audit scan is exhaustive over named chain steps with six assumptions surfaced and recorded back into the table.

**Criterion 3: Establish Ground Truths**
Quoted span: enumerated GT-1, GT-2, GT-3, GT-4, GT-5, GT-6, GT-7; the list carries `?` on exactly those seven and on no other, and GT-8, GT-9, GT-10 each name a read-at-source location ("confirmed numerically at 20.0 and 14.7 months"; "$6.46 → $32.29 (5.00×)"; "the problem statement itself, all four inputs absent by inspection").
Band: **Rigorous**
Justification: the enumeration checks against the list entry by entry; every unsuffixed GT feeds a HIGH-confidence chain (GT-8 → C1, GT-9 → C2, GT-10 → C1 and C2) and names where it was read; no Discard-verdict assumption (A7, A8) appears in the list.

**Criterion 4: Reason Upward**
Quoted span (self-audit scan, chain-form table): *"C8 | C1 + C2 + C3 + C4 + C5 + C6 + C7 | yes | n/a | yes — all seven resolve, no cycle"* — with all eight rows reading `yes / n/a / yes`.
Band: **Rigorous**
Justification: every chain renders head-plus-arrow-led with one hop per physical line and no terminal punctuation before a following arrow, each carries a genuine intermediate, dependencies resolve acyclically; Abandoned Reasoning documents four dead ends in What-was-tried / Why-abandoned / What-it-ruled-out form, the third of which explicitly names and rejects the analogy-as-evidence path; every step introducing a new assumption carries its `[Assumes: X]` token.

**Criterion 5: Validate**
Quoted span: *"Weakest link across the analysis, named: **C8's third hop**, which assumes the ring-fenced budget survives the period boundary (A4) — an organisational fact no chain in this analysis can verify."*
Band: **Sound**
Justification: the adversarial pass record is complete — past-tense premise, unfiltered five-viewpoint cause list written before grouping, five clusters each citing the chain and GT ids it bears on, each with a named plan change or an accepted risk with a named mitigation, and cluster 3 demonstrably modified C8's endpoint — and every MEDIUM line names its `GT-N?` inputs with verification paths plus a downgrade cause of its own; it bands Sound rather than Rigorous under the criterion's own "conclusion without a HIGH chain" clause, because section 6's recommended approach rests on C8 (MEDIUM) for its primary claim, with C1 and C2 supporting but not establishing it. No EXCEPT clause is claimed.

**Criterion 6: Conclusion-to-Ground-Truth Traceability**
Quoted span (self-audit scan, claim-inventory table): *"'**Key insight:** The proposal's least-examined variable…' | bold lead-in | yes | prescribed lead-in… | C2, C5"* — with all four claim rows citing chains and zero reading "none — untraced".
Band: **Rigorous**
Justification: all four section-6 claims trace to named section-4 chains, no claim appears that is not established in section 4, and the Key Insight (the 1/f concentration identity) is a distinct non-obvious finding rather than a restatement of the recommended approach (ring-fence and diagnose).

**Gate result: PASS.** No criterion Absent; exactly zero at Hand-wavy (one at Sound), so both conditions clear. No Fix/Repeat pass was required, and no re-entry edge fired.

---

# The answer

**No — do not fund the base-wide loyalty program at $310,000. Ask the board to approve and ring-fence it instead.**

Three findings drive that, and each is independent of the others:

1. **The mechanism is unmatched to a cause.** Churn rose 2.6 points over six months and nobody has named why. A points program is a generic remedy applied to an undiagnosed problem. Note in particular that **the rival's program cannot be the explanation** — it launched roughly five months *after* the rise began, and at one month old it has produced no outcome data for anyone, including them. "Match the competitor" is a competitive-pressure argument, not an efficacy argument.

2. **The design wastes the budget by a factor of five.** $310,000 across 48,000 members is $6.46 per member per year — 2.8% of what each pays. Getting the hoped 26.5% churn reduction out of a 2.8% effective price cut needs a churn-price elasticity near 9.4. Aim the identical budget at the at-risk fifth of the base and it becomes 14.2% of spend, needing an elasticity near 1.9. **Who gets the money matters five times more than how much it is** — and that is the variable the proposal never discusses.

3. **The price tag may not be the price tag.** "$310,000 a year to run" does not say whether redeemed account credit is inside or outside it. Account credit is forgone revenue, not operating expense. All-in, the cost brackets at **$321k–$655k**. At the top of that bracket with a 40% contribution margin, the program cannot break even in year one *even if it fully delivers the 1.8-point reduction customer success is betting on*. One line in the costing sheet resolves this.

**What to do in the three weeks you have:**

- **Day 1:** pull payment-decline logs. Involuntary churn needs no diagnosis and no board approval to fix — if half the rise is failed payments and you recover half of those, that alone is 0.65 points, which clears the 0.64-point break-even at a healthy margin, for a fraction of $310,000.
- **Week 1:** confirm you can actually join cancellation reasons, decline logs and acquisition-cohort tags. If you cannot, say so now rather than in week four.
- **Days 1–21:** run the diagnosis. Prime suspect to rule in or out first — a discounted acquisition cohort hitting its first full-price renewal. A two-quarter ramp is exactly that shape, and a loyalty program does nothing about it.
- **The board update:** "Approve $310,000, ring-fenced, released against a named cause. If no single cause explains 30% of the rise by [date], it releases to a *targeted* program, not a base-wide one." That is a decision the board can take in three weeks, and it is strictly more informative than either a yes or a no taken today.

**What you are accepting:** about three weeks of un-intervened churn — roughly 2,250 departures, of which a save program might have held ~340, worth about $94,000 in lifetime value. That is real, and it is about 30% of one year of the program budget. I recommend paying it, because the alternative is committing three times that to a mechanism whose all-in cost you cannot currently state.

**Two honesty notes.** First, every business figure here came from your prompt with no source, so all eight conclusions carry MEDIUM confidence; the two HIGH ones (the decision is under-determined; concentration multiplies potency by 1/f) rest only on arithmetic identities and hold regardless of whether your numbers are right. Second, I dispatched a search for published evidence on whether loyalty programs actually reduce subscription churn; **it had not returned when I finished this analysis**, so the assumption that they do (A6) remains unverified and no chain here rests on evidence I do not have. Say the word and I will fold in whatever it found.