**Process disclosures (read first):**

- **MODE = full-composer.** No technique-specific trigger fired; all phases ran with the full companion-technique sweep.
- **One re-entry edge fired:** the second-order pass's return to Phase 2. Extending C6 forward surfaced a 3rd-order effect (redeemed credits lower realised ARPU for retained members) that contradicts an input the benefit calculation depended on — the assumption that a retained member is worth the full $19/month. That routed back to Phase 2, added assumption A22, and re-marked GT-14's $733k as an **upper bound** rather than a central estimate. The direction is conservative (it weakens the case for funding, which was already the leaning), so no conclusion reversed. No other edge fired.
- **Phase 3 verification step:** no external source is cited anywhere in this analysis. Every non-derived ground truth is a figure you stated, whose cited source is your own brief — read directly, with the sentence named. Every other ground truth is arithmetic shown in full. No fetch was attempted because there was nothing external to fetch.
- **Both other gates ran:** closure ledger clean, self-audit scan emitted, six verdict blocks below.

---

# 1. Problem Essence

**Essence Statement:** Is a $310,000/year account-credit loyalty program the correct instrument for a churn deterioration whose cause has not been diagnosed, and does the three-week deadline actually require committing the money now?

**Success criteria.** A correct answer must:

1. Size the churn deterioration in money, not in percentage points.
2. State what churn reduction $310k must buy to break even, under stated margin and redemption assumptions.
3. Bound what any credit scheme *could* deliver, independent of this program's design.
4. Distinguish a deadline to decide from a deadline to spend.
5. Be actionable inside three weeks without new data collection.

The triggering event — the rival's launch — is explicitly **not** the question. C5 shows why.

---

# 2. Assumptions Table

| # | Assumption | Type | Treatment | Verdict | Verification |
|---|---|---|---|---|---|
| A1 | Churn is a constant monthly hazard (geometric decay) | convention | Challenge before use | Accepted as a modelling convention | Real churn is duration-dependent (higher early). Biases C1/C14 estimates; direction depends on cohort mix. Used because no tenure curve was supplied |
| A2 | $19/month is realised ARPU | untested belief | Verify or flag | **Unverified — flagged** | Discounts, annual plans, taxes and payment fees not stated. Overstates benefit if false |
| A3 | The $310k includes point-redemption credit | untested belief | Verify — stakes-escalated | **Unverified — flagged, LOAD-BEARING** | "To run" conventionally denotes operating cost, not liability. C3 shows this single question moves the decision |
| A4 | The churn rise is voluntary and money-responsive | untested belief | Verify — stakes-escalated | **Unverified — flagged, LOAD-BEARING** | Nothing in the brief diagnoses cause. C4 bounds the consequence |
| A5 | The program delivers 1.8pp of churn reduction | untested belief | Verify — stakes-escalated | **Unverified — flagged, LOAD-BEARING** | Your own word is "betting." No holdout is proposed, so it would remain unverified after launch |
| A6 | Contribution margin suffices to convert retained revenue to profit | untested belief | Verify or flag | **Unverified — flagged** | Margin never stated. C6 shows the decision inverts around 74% |
| A7 | Three weeks is a deadline to commit spend | convention | Challenge before use | **Challenged — rejected** | The brief says "final call … before the next board update." That is a deadline for a defensible position. C8 |
| A8 | The rival's launch requires a matching program | convention | Challenge before use | **Challenged — rejected as causal justification** | Timing rules it out as the cause of the observed rise. C5. Survives only as forward-looking parity risk |
| A9 | The program can be withdrawn if it underperforms | untested belief | Verify or flag | **Unverified — flagged; likely false** | Withdrawing an accrued-credit scheme is itself a churn event. Treated as a one-way door |
| A10 | Churn was measured identically across both quarters | untested belief | Verify or flag | **Unverified — flagged** | A definition or window change manufactures an apparent rise. Cheap to check |
| A11 | 4.2% was a true baseline, not a seasonal low | untested belief | Verify or flag | **Unverified — flagged** | Two quarters is one seasonal swing |
| A12 | Cohort mix is stable across the window | untested belief | Verify or flag | **Unverified — flagged** | A promo cohort acquired ~2 quarters ago hitting first renewal reproduces this exact curve |
| A13 | Points accrue fast enough to change behaviour within two quarters | untested belief | Verify or flag | **Unverified — flagged** | *(inversion-derived)* If false, the board sees cost with no signal at the following update |
| A14 | Redeemers are not predominantly members who would have stayed | untested belief | Verify or flag | **Unverified — flagged** | *(inversion-derived)* An untargeted points scheme selects for engagement, which correlates with retention. Deadweight risk |
| A15 | The offer is perceived before the cancel decision | untested belief | Verify or flag | **Unverified — flagged** | *(inversion-derived)* Feeds GT-10's reachability condition |
| A16 | The advantage is durable against rival escalation | untested belief | Challenge | **Challenged — implausible** | *(inversion-derived)* An account-credit scheme is copyable in weeks; the rival already demonstrated the capability |
| A17 | Involuntary (payment-failure) churn share is unchanged across the window | untested belief | Verify or flag | **Unverified — flagged** | *(fishbone: Technology/Process)* Highest-priority branch; derivable from billing records in days |
| A18 | No price, packaging or product change occurred in the window | untested belief | Verify or flag | **Unverified — flagged** | *(fishbone: Resources)* |
| A19 | Renewal and dunning communications are functioning | untested belief | Verify or flag | **Unverified — flagged** | *(fishbone: Technology)* A deliverability drop reproduces this curve at near-zero visibility |
| A20 | The base decays without new acquisition | convention | Challenge before use | Accepted as a modelling convention | Isolates the retention effect. Adding acquisition scales both arms similarly and changes no comparison |
| A21 | Per-point churn sensitivity is linear over the 5–7% range | convention | Challenge before use | **Verified approximately true** | Computed: $396k for the first point, $418k for the second — a 5% spread, immaterial at this precision |
| A22 | Credits offset revenue at ~100% margin | untested belief | Verify or flag | **Unverified — flagged** | *(added by second-order re-entry)* A credit avoids no COGS, so it lands near-fully on contribution |
| A23 | No untargeted points scheme converts ~88% of its money-addressable population | untested belief | Verify or flag | **Unverified — flagged, no source** | Asserted structurally, not from a benchmark. Deliberately not supported by analogy |
| A24 | 25% involuntary share; 40% price/value share of voluntary cancellations | untested belief | Verify or flag | **Unverified — flagged, assumed values** | Illustrative parameters for C4's ceiling. Both measurable in days |
| A25 | The rise was progressive across two quarters, not a step change last month | untested belief | Verify or flag | **Unverified — flagged** | Load-bearing for C5. "Climbed over the last two quarters" implies progressive; confirm from the monthly series |
| A26 | The business holds billing, cohort and cancellation-reason data | untested belief | Verify — stakes-escalated | **Partially verified by construction, LOAD-BEARING** | Payment-failure share and cohort mix are derivable from billing and signup records regardless of instrumentation; only the *reason* split requires an exit survey. The recommendation survives partial availability |
| A27 | Three weeks is sufficient analyst time for the decomposition | untested belief | Verify or flag | **Unverified — flagged** | It is a query against existing tables, not a study |
| A28 | The board accepts a decomposition plus a pre-committed rule as a decision | convention | Challenge before use | Accepted with caveat | Politically contingent; the mitigation is to present the break-even arithmetic alongside the rule |
| A29 | 0.3pp is a generous attribution of churn to the rival | untested belief | Verify or flag | **Unverified — flagged** | Deliberately generous; C9 is robust because even this figure yields a trivial delay cost |
| A30 | Credit tiers lower the reference price and reduce future pricing power | untested belief | Verify or flag | **Unverified — flagged, no source** | A behavioural claim stated as a risk, not used as a load-bearing input |
| A31 | The trade-off weights reflect your actual priorities | untested belief | Verify or flag | **Unverified — flagged** | Weights were locked before scoring; sensitivity stated in Phase 4 |

---

# 3. Ground Truths

**Provenance note:** the cited source for every non-derived ground truth is your brief. "Read-at-source" here means the figure was located in that text at the named sentence — it does **not** mean the figure has been checked against your systems. That second verification is yours to do and is not claimed here.

| ID | Ground truth | Provenance | Read-location |
|---|---|---|---|
| GT-1 | 48,000 members × $19/mo = **$912,000 MRR**, $10.944M ARR | read-at-source + arithmetic | Brief, sentence 1: "48,000 active members paying $19 a month" |
| GT-2 | Monthly churn rose **4.2% → 6.8%** across two quarters | read-at-source | Brief, sentence 1: "churn has climbed from 4.2 percent to 6.8 percent over the last two quarters" |
| GT-3 | At 6.8%/mo: 12-month retention 0.932¹² = **42.95%**; annual attrition 57.05%; half-life 9.84 months; mean tenure 14.7 months; gross LTV $279 | definitional arithmetic | Computed here from GT-1, GT-2 |
| GT-4 | At 5.0%/mo: 12-month retention 0.95¹² = **54.04%**; half-life 13.5 months; mean tenure 20 months; gross LTV $380 | definitional arithmetic | Computed here |
| GT-5 | Stated program cost **$310,000/yr** = $25,833/mo = 2.83% of ARR | read-at-source + arithmetic | Brief, sentence 2: "costing around $310,000 a year to run" |
| GT-6? | Whether $310k includes point-redemption credit is **not stated** | unverified | Brief says "to run"; scope undetermined |
| GT-7 | A rival launched a similar program **last month** | read-at-source | Brief, sentence 3 |
| GT-8 | A decision is required **within three weeks**, framed against a board update | read-at-source | Brief, sentence 4: "final call within three weeks before the next board update" |
| GT-9 | Total churn = involuntary + voluntary (exhaustive partition) | definitional identity | — |
| GT-10 | A monetary retention incentive acts only on members who are (a) still reachable, (b) leaving for a money-responsive reason, (c) aware of the offer before deciding | definitional / logical | — |
| GT-11? | Contribution margin is **not stated** anywhere in the brief | unverified | — |
| GT-12? | Involuntary share of the 6.8% is **not stated** | unverified | — |
| GT-13 | The brief states **no diagnosed cause** for the churn rise | read-at-source (absence) | Whole brief; no causal claim appears |
| GT-14 | Year-one gross revenue from the standing base: **$7,650,857** at 6.8%, **$8,383,815** at 5.0%, **$8,738,629** at 4.2%. The 1.8pp delta is **$732,958**. Per-point sensitivity $396k (first) to $418k (second) | definitional arithmetic | Computed from GT-1: 912,000 × Σ(1−c)ᵗ, t = 0…11 |
| GT-15 | $310k breaks even at **0.78pp** of monthly churn reduction on gross revenue; **1.19pp** at a 65% contribution margin | derived arithmetic | Computed from GT-14 |
| GT-16? | Annual credit-redemption cost bracket: **[$50k, $228k, $855k]** | unverified — Fermi estimate | Unit-factors: members × participation × credit per redeemer. Central 40,000 × 30% × $19. Low 35,000 × 15% × $9.50. High 45,000 × 50% × $38. Participation and per-redeemer values are assumed, not sourced |
| GT-17 | Account credit redeemed against a subscription reduces realised revenue per retained member | definitional, given the program as described | Brief, sentence 2: "redeem points for account credit". Magnitude lives in GT-16? |
| GT-18? | Assumed split: 25% involuntary, 40% price/value share of voluntary cancellations | unverified — assumed parameters | Used only in C4's ceiling; both measurable from your own data |

**`?`-marked ground truths: GT-6, GT-11, GT-12, GT-16, GT-18 (5 of 18).**

**Phase 3 failure records:** none. No external source was cited, so no read was attempted and none failed. The `?` marks above are all `unverified` (no source exists), never `citation does not support the claim`.

**HIGH-confidence chains and their unsuffixed inputs, with read-locations named:** C1 (GT-1, GT-2 — brief sentence 1; GT-3 — computed in this section), C2 (GT-1 — brief sentence 1; GT-14 — computed in this section), C5 (GT-2 — brief sentence 1; GT-7 — brief sentence 3), C8 (GT-8 — brief sentence 4; GT-13 — absence across the whole brief).

---

# 4. Derivation Chains

**C1 — the deterioration, sized in money** *(HIGH)*

```text
GT-1 (MRR $912k) + GT-2 (churn 4.2% → 6.8%) + GT-3 (12-month retention 42.95% at 6.8%)
→ year-one revenue from the standing base is $7.65M at 6.8% against $8.74M at the former 4.2% rate [Assumes: A20]
→ the churn rise is destroying roughly $1.09M of year-one revenue from the existing base [Assumes: A1]
→ the proposed program targets 5.0%, recovering $733k of that $1.09M and leaving $355k of the deterioration unaddressed by design
```

**C2 — what $310k must buy** *(HIGH)*

```text
GT-1 (MRR $912k) + GT-14 (1.8pp ≈ $733k year-one retained gross revenue) + GT-15 (break-even arithmetic)
→ each point of monthly churn reduction is worth roughly $400k of year-one gross revenue on this base [Assumes: A21]
→ the $310k running cost breaks even at about 0.78pp measured in gross revenue
→ at a 65% contribution margin the same cost breaks even at about 1.19pp, which is two thirds of the entire hoped-for effect [Assumes: A6]
```

**C3 — the redemption-scope hole** *(LOW — three unverified inputs)*

```text
GT-5 ($310k stated) + GT-6? (scope unverified) + GT-16? (redemption $50k–$855k, central $228k)
→ if credits sit outside the stated figure the fully-loaded annual cost runs from $360k at the low bracket to $1.17M at the high one [Assumes: A3]
→ break-even rises to 0.91pp at the low bracket, 1.34pp at the central one and past 2.8pp at the high one
→ the high bracket exceeds the entire hoped-for 1.8pp effect, so one unanswered scoping question moves this from marginally fundable to unfundable
```

The estimate's stop criterion is **not met**: the bracket spans an order of magnitude and straddles the decision threshold. That is the finding, not a defect — escalated explicitly rather than papered over with a point estimate.

**C4 — the ceiling on any credit scheme** *(MEDIUM — structure firm, parameters assumed)*

```text
GT-9 (churn = voluntary + involuntary) + GT-10 (an incentive reaches only reachable, money-motivated, aware leavers) + GT-12? (involuntary share unmeasured) + GT-18? (assumed 25% / 40% split)
→ the maximum reduction any credit scheme can deliver is bounded by the money-addressable share of the 6.8pp, not by the program's generosity [Assumes: A15]
→ at a 25% involuntary share and a 40% price-or-value share of voluntary cancellations the addressable ceiling is about 2.04pp [Assumes: A24]
→ reaching 1.8pp would require converting roughly 88% of that addressable population, which no untargeted points scheme achieves [Assumes: A23, A14]
→ a structurally defensible expectation is 0.5–0.8pp, between a third and a half of what the plan assumes
```

This is the theoretical-limit pass. **Law-permitted ceiling** 2.04pp; **conventional figure** (the plan's bet) 1.8pp; **gap** — the plan is claiming 88% of the ceiling. The irreducible portion is the ~4.8pp of involuntary and non-money-reason churn, which no price on this instrument can touch.

**C5 — the rival is not the cause** *(HIGH)*

```text
GT-2 (rise began two quarters ago) + GT-7 (rival launched last month)
→ the deterioration predates the rival's program by roughly five months [Assumes: A25]
→ a launch cannot cause a rise that was already largely complete before it happened
→ matching the rival is forward-looking parity maintenance against a future risk, not a remedy for the observed churn, and must be budgeted and justified as such [Assumes: A16]
```

**C6 — net contribution on the program's own best case** *(LOW — two unverified inputs)*

```text
GT-14 ($733k retained gross revenue if the full 1.8pp lands) + GT-11? (margin unmeasured) + GT-16? (central redemption $228k) + GT-17 (credits reduce realised revenue)
→ at a 65% contribution margin the retained contribution is $476k [Assumes: A6, A2]
→ subtracting $228k of credits, which offset revenue at close to full margin, and $310k of running cost leaves negative $62k [Assumes: A22]
→ if credits already sit inside the $310k the same $733k needs only a 42% contribution margin to clear
→ if they do not, it needs a margin above 74%, so the decision turns on a scoping question nobody has answered [Assumes: A3]
```

**C7 — second-order and third-order extension** *(LOW)*

```text
C6 (net negative at the central case) + GT-17 (credits reduce realised ARPU) + GT-14 (benefit valued at full $19)
→[2nd] every member the program retains arrives at a lower effective price, so the $19 used to value retention overstates the benefit [Assumes: A22]
→[2nd] the $733k figure is therefore an upper bound rather than a central estimate
→[3rd] a permanent credit tier lowers the reference price members anchor on, making future increases harder to land [Assumes: A30]
→[3rd] a copyable credit scheme invites escalation, ending with both firms at lower margin and unchanged relative position [Assumes: A16]
```

**Contradiction found and routed.** The first 2nd-order step contradicts an input GT-14 depended on. Routed back to Phase 2 per the procedure; A22 added; GT-14 re-marked as an upper bound. The remaining three effects contradict no ground truth and extend the chain as shown.

**C8 — the deadline is not what it appears** *(HIGH)*

```text
GT-8 (three weeks, tied to a board update) + GT-13 (no diagnosed cause stated)
→ the deadline constrains when a decision must be defensible, not when money must be committed [Assumes: A7]
→ the measurement that decides this question is a query against data the business already holds rather than a study needing new collection [Assumes: A26]
→ three weeks is enough to decompose the 6.8pp into involuntary, cohort-mix and voluntary-by-reason shares [Assumes: A27, A10]
→ presenting the board a decomposition plus a pre-committed funding rule is a decision, not a deferral [Assumes: A28]
```

**C9 — the cost of waiting three weeks** *(MEDIUM)*

```text
GT-1 (MRR $912k) + GT-3 (gross LTV $279 at 6.8% churn) + GT-7 (rival launched last month)
→ a three-week delay exposes about 0.7 months of any rival-attributable churn increment
→ at a generous 0.3pp of rival-attributable monthly churn that is roughly 100 members, worth about $28k in lifetime value [Assumes: A29]
→ the delay costs under a tenth of one year of program spend, so deadline pressure does not justify committing ahead of the diagnosis
```

**C10 — the recommendation** *(MEDIUM)*

```text
C2 (break-even 0.78–1.19pp) + C4 (defensible effect 0.5–0.8pp) + C6 (net negative at the central case) + C8 (the deadline permits diagnosis) + C9 (delay costs ~$28k)
→ the defensible effect range sits at or below break-even on gross revenue and below it once margin and credits are applied
→ the weighted trade-off scores diagnose-then-decide at 109, against 87 for a holdout pilot, 62 for declining outright and 59 for funding as proposed [Assumes: A31]
→ funding as specified is the lowest-scoring of the four options, and the highest-scoring one costs analyst time rather than $310k
→ decline the $310k commitment now, run the three-week churn decomposition, and bring the board a pre-committed funding rule keyed to the measured addressable share
```

*Trade-off detail — weights locked before any option was scored (1–5, higher better throughout):*

| Criterion | W | A: fund now | B: decline | C: diagnose first | D: holdout pilot |
|---|---|---|---|---|---|
| Expected net contribution | 5 | 2 | 3 | 4 | 4 |
| Information gained per dollar | 4 | 2 | 1 | 5 | 4 |
| Reversibility preserved | 4 | 1 | 5 | 5 | 4 |
| Speed to a defensible board answer | 3 | 3 | 4 | 4 | 2 |
| Addresses the actual churn driver | 5 | 2 | 1 | 5 | 3 |
| Organisational cost | 2 | 5 | 1 | 3 | 4 |
| Competitive-position risk | 2 | 4 | 2 | 3 | 3 |
| **Weighted total** | | **59** | **62** | **109** | **87** |

No pair falls within 10%, so no sensitivity tie-break is required. The weight that would flip C→A is *speed to a defensible answer* — if the three weeks were a hard **launch** deadline rather than a decision deadline, its weight rises sharply and the ranking changes. C5 and C8 are what establish that it is not.

**C11 — conditions on any eventual launch** *(MEDIUM)*

```text
C10 (diagnose before funding) + GT-14 (a 1.8pp effect is worth $733k gross) + GT-6? (redemption scope unverified)
→ if the diagnosis clears the funding rule, the residual risks are that the effect is unmeasurable and the cost unbounded [Assumes: A5, A3]
→ an untargeted launch with no control group cannot separate the program's effect from the underlying trend, which makes it unkillable once live [Assumes: A9]
→ any funded launch therefore requires a randomised holdout, a capped annual redemption liability and a kill criterion pre-registered before launch
```

*Pre-mortem (Phase 5 input, clustered):* imagining it is twelve months on, the program is funded and churn sits at 6.5% — the causes cluster into five structural weaknesses, each with a plan change or a named accepted risk. **(i) Unmeasurable effect** → randomised holdout, mandatory. **(ii) Unbounded redemption cost** → annual liability cap. **(iii) Undiagnosed cause** → diagnosis precedes funding. **(iv) Non-durable, copyable advantage** → *accepted risk*, mitigated by budgeting it as parity maintenance and crediting it with zero churn reduction in the business case. **(v) Unkillable once live** → pre-registered kill criterion and wind-down design.

---

## Assumption Audit (process output)

| Chain | Step | Step text (brief) | Assumption surfaced? | Added to table? |
|---|---|---|---|---|
| C1 | H1 | year-one revenue $7.65M vs $8.74M | A20 base decays without acquisition | Yes |
| C1 | H2 | rise destroys ~$1.09M | A1 constant hazard | Already present |
| C1 | H3 | recovers $733k, leaves $355k | — | Clean pass |
| C2 | H1 | ~$400k per point | A21 linearity over 5–7% | Yes |
| C2 | H2 | break-even 0.78pp gross | — | Clean pass |
| C2 | H3 | 1.19pp at 65% margin | A6 margin | Already present |
| C3 | H1 | loaded cost $360k–$1.17M | A3 scope | Already present |
| C3 | H2 | break-even 0.91–2.8pp | — | Clean pass |
| C3 | H3 | high bracket exceeds the effect | — | Clean pass |
| C4 | H1 | ceiling set by addressable share | A15 offer perceived pre-decision | Yes |
| C4 | H2 | 2.04pp ceiling | A24 25%/40% split | Yes |
| C4 | H3 | needs 88% conversion | A23 no scheme converts 88%; A14 deadweight | Yes (both) |
| C4 | H4 | defensible 0.5–0.8pp | — | Clean pass |
| C5 | H1 | predates by ~5 months | A25 progressive rise | Yes |
| C5 | H2 | cannot cause a prior rise | — | Clean pass |
| C5 | H3 | parity maintenance, budget separately | A16 durability | Already present |
| C6 | H1 | $476k contribution at 65% | A6 margin; A2 realised ARPU | Already present |
| C6 | H2 | minus credits and cost = −$62k | A22 credits at ~100% margin | Yes |
| C6 | H3 | 42% margin if credits inside | — | Clean pass |
| C6 | H4 | 74% margin if outside | A3 scope | Already present |
| C7 | H1 | retained members worth less than $19 | A22 | Already present |
| C7 | H2 | $733k is an upper bound | — | Clean pass |
| C7 | H3 | reference-price anchoring | A30 anchoring | Yes |
| C7 | H4 | escalation to lower margin | A16 durability | Already present |
| C8 | H1 | deadline to decide, not to spend | A7 deadline type | Already present |
| C8 | H2 | query, not a study | A26 data availability | Yes |
| C8 | H3 | three weeks suffices | A27 analyst time; A10 measurement consistency | Yes / already present |
| C8 | H4 | a rule is a decision | A28 board acceptance | Yes |
| C9 | H1 | 0.7 months of exposure | — | Clean pass |
| C9 | H2 | ~100 members, ~$28k | A29 generous attribution | Yes |
| C9 | H3 | under a tenth of program spend | — | Clean pass |
| C10 | H1 | effect at or below break-even | — | Clean pass |
| C10 | H2 | 109 / 87 / 62 / 59 | A31 weights | Yes |
| C10 | H3 | funding is lowest-scoring | — | Clean pass |
| C10 | H4 | decline, diagnose, bring a rule | A26, A28 | Already present |
| C11 | H1 | effect unmeasurable, cost unbounded | A5, A3 | Already present |
| C11 | H2 | unkillable once live | A9 reversibility | Already present |
| C11 | H3 | holdout, cap, kill criterion | — | Clean pass |

*38 steps scanned across 11 chains; 13 new assumptions added (A20–A31 plus A14's second surfacing, folded into the existing row).*

---

# 5. Abandoned Reasoning

**LTV-uplift framing, abandoned.** I first sized the decision as an LTV gain per member: $279 at 6.8% versus $380 at 5.0%, ×48,000 = $4.85M. Abandoned — it treats the entire standing base as though it were re-acquired at the new rate and silently books a multi-year benefit as though it landed in year one. The cohort-decay framing in GT-14 is the honest version and yields $733k, not $4.85M. A 6.6× difference, entirely from framing.

**Benchmark anchoring, abandoned.** I considered anchoring the expected effect on typical published loyalty-program retention results. Abandoned on two grounds: I have no verified source in front of me and will not manufacture one, and the methodology forbids analogy as direct evidence regardless. Replaced by C4's addressable-share ceiling, which is structural and derived from your own churn decomposition rather than someone else's.

**Competitive-response framing, abandoned at C5.** I began building the analysis around whether to match the rival. The timing arithmetic killed it: a launch last month cannot explain a rise that began five months earlier. The framing survives only as forward-looking parity risk, which is a separate and much smaller decision.

**Multi-year NPV, abandoned.** At 57% annual attrition the standing base beyond year one is small enough that discounting changes no ranking, and it would add decimal places the inputs cannot support.

---

## §6→§4 closure ledger (process output)

```text
- "Do not fund the loyalty program at $310,000 on the current evidence" → chain C10 ✓
- "The plan's 1.8pp bet sits at roughly 88% of the arithmetic ceiling" → chain C4 ✓
- "The three-week deadline constrains when the decision must be defensible, not when money must move" → chain C8 ✓
- "The rival's launch cannot be the cause of the observed rise" → chain C5 ✓
- "The program is net-negative on its own best case at a 65% margin" → chain C6 ✓
- "Fund only if the diagnosis clears three pre-committed conditions" → chains C4, C3, C6 ✓
- "Any eventual launch requires a holdout, a liability cap and a kill criterion" → chain C11 ✓
- "Waiting three weeks costs about $28k against $310k of spend" → chain C9 ✓
- "The churn rise is destroying about $1.09M of year-one revenue" → chain C1 ✓
- "Break-even is 0.78pp gross, 1.19pp at margin" → chain C2 ✓
- "Retained members are worth less than the $19 used to value them" → chain C7 ✓
```

No claim was cut; all eleven carry a chain.

---

## Self-audit scan (process output)

**Table 1 — section 4 chain form**

| Chain | Chain head (brief) | Form conforming? | Rule applied | Dependency clean? |
|---|---|---|---|---|
| C1 | GT-1 + GT-2 + GT-3 | yes | n/a | yes |
| C2 | GT-1 + GT-14 + GT-15 | yes | n/a | yes |
| C3 | GT-5 + GT-6? + GT-16? | yes | n/a | yes |
| C4 | GT-9 + GT-10 + GT-12? + GT-18? | yes | n/a | yes |
| C5 | GT-2 + GT-7 | yes | n/a | yes |
| C6 | GT-14 + GT-11? + GT-16? + GT-17 | yes | n/a | yes |
| C7 | C6 + GT-17 + GT-14 | yes | n/a | yes |
| C8 | GT-8 + GT-13 | yes | n/a | yes |
| C9 | GT-1 + GT-3 + GT-7 | yes | n/a | yes |
| C10 | C2 + C4 + C6 + C8 + C9 | yes | n/a | yes |
| C11 | C10 + GT-14 + GT-6? | yes | n/a | yes |

**Table 2 — section 6 claim inventory**

| §6 span (brief) | Construct | Claim under R11? | R11 clause applied | Chain cited |
|---|---|---|---|---|
| "Recommended approach:" | bold lead-in | yes | bold lead-in whose colon closes the bold span | C10 |
| "Key insight:" | bold lead-in | yes | bold lead-in whose colon closes the bold span | C4 |
| "Trade-offs acknowledged:" | bold lead-in | yes | bold lead-in whose colon closes the bold span | C9, C5 |
| "The funding rule:" | bold lead-in, whole line, no own citation | no | section-intro label; obligation falls to items beneath | n/a |
| Rule item 1 (addressable share) | list item | yes | list item over forty characters | C4 |
| Rule item 2 (redemption scope) | list item | yes | list item over forty characters | C3 |
| Rule item 3 (margin threshold) | list item | yes | list item over forty characters | C6 |
| Rule item 4 (launch conditions) | list item | yes | list item over forty characters | C11 |
| "What this costs you:" | bold lead-in | yes | bold lead-in whose colon closes the bold span | C9 |
| "Confidence caveat:" | bold lead-in | yes | bold lead-in whose colon closes the bold span | C6, C3 |
| Opening framing sentence | prose | no | prose carrying neither a bold colon lead-in nor a list marker | n/a |
| Closing sentence on the board framing | prose | no | prose carrying neither a bold colon lead-in nor a list marker | n/a |

```text
Scan complete: 11 chain rows, one per section-4 chain block in order; 12 section-6 rows, one per construct in order — 9 claims under R11, 3 excluded. 0 chains malformed, 0 claims untraced.
```

---

## Self-Audit Gate (process output — scores this analysis's structure, not your business)

**Criterion 1 — Essence.** RIGOROUS. The Essence Statement names the decision *and* the reframe that makes it decidable ("does the three-week deadline actually require committing the money now?"), with five checkable success criteria. It is not a restatement of your prompt — the prompt asks "should we fund," the essence asks whether the instrument matches an undiagnosed cause and whether the deadline binds spending at all.

**Criterion 2 — Assumptions.** RIGOROUS. 31 rows, every one carrying a four-type classification, a treatment and a verdict. Three are stakes-escalated (A3, A4, A5) and one more added on re-entry (A26). Two conventions were challenged and **rejected** (A7, A8), which is the treatment doing real work rather than labelling. The Assumption Audit scan above shows 38 steps walked and 13 assumptions added back.

**Criterion 3 — Evidence.** SOUND, not rigorous. Quoting the ground-truths section: *"'Read-at-source' here means the figure was located in that text at the named sentence — it does not mean the figure has been checked against your systems."* Five of eighteen ground truths carry `?`. No HIGH-confidence chain depends on a `?` input. The band is capped below RIGOROUS because GT-16? and GT-18? are assumed parameters with no source, and they carry C4 and C6 — the two chains that do most of the analytical work.

**Criterion 4 — Chains.** RIGOROUS. Quoting the self-audit scan: *"0 chains malformed."* Eleven chains, every one with at least two intermediate hops, no dependency cycles, every input resolving to a listed ground truth or an upstream chain. The Abandoned Reasoning section records four discarded paths including the $4.85M framing error, which is the one that would have inverted the conclusion. No analogy is used as direct evidence — the benchmark-anchoring path was abandoned explicitly on those grounds. Every `[Assumes: X]` mark traces to a table row.

**Criterion 5 — Conclusion.** SOUND, not rigorous. The recommendation is unambiguous and actionable within your window, and the funding rule is falsifiable. Capped below RIGOROUS because the load-bearing chain C10 inherits `?` inputs through C4 and C6, so the recommendation carries an explicit confidence caveat rather than standing on verified ground truths alone.

**Criterion 6 — Traceability.** RIGOROUS. Quoting the self-audit scan: *"9 claims under R11, 3 excluded … 0 claims untraced."* The Key Insight (C4 — the plan is claiming 88% of the arithmetic ceiling) is a distinct claim from the Recommended Approach (C10 — decline and diagnose), not a restatement of it: one is a bound on the instrument, the other is an action.

No criterion failed. The Fix/Repeat loop did not need to fire.

---

# 6. Conclusion

The question you asked has an answer, and it is not the one the three-week clock implies you need.

**Recommended approach:** Do not fund the loyalty program at $310,000 on the current evidence (chain C10). Spend the three weeks running a churn decomposition against data you already hold, and bring the board that decomposition plus a pre-committed funding rule. Diagnose-then-decide scored 109 on the weighted trade-off against 59 for funding as proposed — funding as specified is the lowest-scoring of the four options considered.

**Key insight:** The plan is not mildly optimistic — the 1.8pp it assumes is roughly 88% of the arithmetic ceiling any credit scheme could reach (chain C4). Total churn partitions into involuntary and voluntary, and an incentive can only touch voluntary leavers whose reason is money-responsive and who see the offer before deciding. At a 25% involuntary share and a 40% price/value share of cancellations, the entire addressable population is 2.04pp of the 6.8pp. Hitting 1.8pp means converting nearly all of it, with an untargeted points scheme. A structurally defensible expectation is 0.5–0.8pp, which sits at or below break-even before a single dollar of credit is redeemed.

**Trade-offs acknowledged:** Waiting three weeks is not free — if the rival's program is causing even 0.3pp of monthly churn, the delay costs roughly 100 members and about $28,000 in lifetime value (chain C9). That is under a tenth of one year of program spend, so the trade is heavily favourable, but it is a real cost and the board should see it named. Separately, declining does nothing about a churn rate that halves your base in under ten months; the diagnosis is what converts that from an unaddressed problem into a targeted one (chain C5).

**The funding rule:**

1. **Addressable share.** Fund only if involuntary churn is under roughly 1.0pp of the 6.8pp *and* price-or-value is the leading cited cancellation reason. Both are measurable from billing records and exit data inside three weeks (chain C4).
2. **Redemption scope.** Fund only if the $310,000 is confirmed to include point-redemption credit, or a hard annual redemption cap is added. If credits sit outside that figure, plausible redemption of $50k–$855k moves break-even from 0.91pp to past 2.8pp — the high end exceeds the entire hoped-for effect (chain C3).
3. **Margin threshold.** Fund only if contribution margin exceeds 42% with credits inside the $310k, or 74% with them outside. At a 65% margin with $228k of credits, the program returns **negative $62,000 even if the full 1.8pp bet lands** (chain C6).
4. **Launch conditions.** If the rule clears, launch with a randomised holdout, a capped annual redemption liability and a kill criterion pre-registered before go-live — otherwise the effect is unmeasurable and the program becomes unkillable (chain C11).

**What this costs you:** the decomposition is analyst time, not a study — payment-failure share comes from billing records and cohort mix from signup dates, regardless of whether you instrument exit reasons (chain C8). The deadline is a deadline to be defensible, not a deadline to spend. A board that receives "here is the 6.8pp broken into its parts, here is the break-even arithmetic, and here is the rule that decides it" has received a decision.

**Confidence caveat:** MEDIUM overall. The break-even arithmetic (C2), the problem sizing (C1), the rival-timing finding (C5) and the deadline reframe (C8) are HIGH — they rest on your stated figures and arithmetic alone. The magnitude claims in C3, C4 and C6 rest on `?`-marked inputs: contribution margin (GT-11?), involuntary share (GT-12?), redemption cost (GT-16?) and the assumed 25%/40% split (GT-18?). What would raise this to HIGH is precisely what the recommendation asks you to measure — three weeks of your own data. The conclusion is robust to that measurement in one direction: every plausible value of the unverified inputs makes the program *less* attractive than the plan assumes, never more.

One residual worth flagging before you present this: churn at 6.8% monthly means the base halves in under ten months. That is an existential-scale rate, not a loyalty-program-scale one, and the diagnosis may well surface something that costs $40,000 to fix and recovers more than this program was ever going to.