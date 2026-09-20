**Bottom line before the machinery:** the premise in your question is the thing that most needs checking. Lambda is cheaper than Fargate only below roughly a 46.5% duty cycle, and I can derive that threshold from AWS's own price list — but I cannot tell you which side of it you're on, and more importantly nobody has established that compute is where your money goes.

---

## Disclosures (process output, top of response per Turn discipline)

**Re-entry edge fired — one, bounded, as specified.** The Phase 4 second-order pass produced an effect that contradicted a Ground Truth: "provisioned concurrency reintroduces paying for idle" contradicted the then-scoped GT "Lambda bills only during invocation." Per the second-order routing rule this returned to **Phase 2 for re-challenging**, not to Phase 3. What changed: the ground truth was re-scoped to *on-demand* Lambda, provisioned concurrency was added as a separate billing mode with its own rates (now GT-3), and the arithmetic was redone — which **reversed the naive finding**. The superseded version is recorded in Abandoned Reasoning. No other re-entry edge fired; no mid-run `AskUserQuestion` was needed.

**Step 0:** no technique-specific trigger phrase fired, so `MODE = full-composer` — all phases run, all eight companion techniques enumerated.

---

## Companion-technique process output

### Fishbone (Phase 2) — default six-category set, locked before brainstorming

Effect: *our AWS bill is higher than we want it to be.*

| Category | Candidate causes (all unverified unless marked) |
|---|---|
| People | No named cost owner; engineers cannot see the cost of an instance-type choice at the time they make it |
| Process | No right-sizing cadence; ephemeral environments never torn down; no budget alarm in CI |
| Technology and Tools | Over-provisioned task sizes; x86 where arm64 would do; no autoscaling; **compute platform choice** ← *the only branch the prompt considers* |
| Environment | Cross-AZ and egress data transfer; NAT Gateway hourly + per-GB processing; duplicated multi-region footprint |
| Information | No cost allocation tags, no CUR; the bill's composition is unknown ← **highest-priority branch** |
| Resources | Zero Savings Plan coverage; orphaned EBS volumes, snapshots, idle load balancers, unattached EIPs |

Highest-priority branches for evidence gathering: **Information** (nothing else can be prioritised until the breakdown exists) and **Resources** (unconditional, no code change). Every branch above entered the Assumptions Table as an `untested belief` or folded into an existing row.

### Inversion (Phase 2)

**Claim:** Migrating our services to Lambda will cut our AWS bill.
**Inverted:** Migrating our services to Lambda will not cut our AWS bill.

Failure-guaranteeing conditions → necessary preconditions → status:

| # | Would guarantee failure | Necessary precondition the claim silently needs | Status |
|---|---|---|---|
| F1 | Services run above the break-even duty cycle | Duty cycle below 46.5% | untested → A-2 |
| F2 | Sustained request rate is high per vCPU | Request rate below ~67/s per vCPU-equivalent | untested → A-3 |
| F3 | Compute is a small slice of the bill | Compute is a large share of the bill | untested → A-4 |
| F4 | Services are IO-bound with high concurrency per vCPU | Services are CPU-bound, low concurrency | untested → A-5 |
| F5 | Cold starts force provisioned concurrency sized to peak | Cold-start latency is acceptable | untested → A-6 |
| F6 | Migration adds new billed components (RDS Proxy, API Gateway, Step Functions) | No new billed components required | untested → A-7 |
| F7 | Engineering cost exceeds the annualised saving | Migration cost is small relative to saving | untested → A-8 |
| F8 | Containers are over-provisioned, so right-sizing alone captures the saving | Containers are already right-sized | untested → A-9 |

**Eight preconditions. Zero verified.** That is the shape of "everyone knows."

### Estimate (Phase 4) — Fermi, with bounds

Target quantity and units: **$ per month of compute** = (vCPU-equivalents) × ($ / vCPU-eq·hour) × (hours / month). Unit cancellation: `vCPU-eq × $·vCPU-eq⁻¹·h⁻¹ × h → $`. ✓

| Factor | First-principles value | Source type |
|---|---|---|
| $/vCPU-eq·hour, Fargate x86 on-demand | $0.048159 | direct measurement (price list, GT-4/GT-6) |
| arm64 multiplier | 0.800 | direct measurement (GT-5) |
| Savings Plan multiplier | bracket [1.00, 0.34] | ceiling read at source (GT-9); realised rate not located (GT-16?) |
| hours/month | 730 | definition |
| vCPU-equivalents deployed | **unknown** | GT-13? |

Three brackets, three different verdicts under the decision-resolution stop criterion:

1. **Compute-unit reduction from the unconditional levers:** [20.0% (arm64 only), ~50% (arm64 + partial SP), 72.8% (arm64 + max SP)]. Both ends recommend the same action. **Resolved — proceed.**
2. **Compute-line change from a Lambda migration:** [−115.2% at full duty, +89.2% at 5% duty]. **Straddles zero — the two ends recommend opposite actions. Not resolved; escalate the dominant uncertain factor (duty cycle).**
3. **Bill reduction from either:** compute-share × the above. Compute share unmeasured. **Not resolved; escalate.** This is what makes measurement a gate rather than a parallel task.

### Trade-off analysis (Phase 4) — weights locked before any scoring

## Options

- **A** — Migrate to Lambda now (the fastest-path plan as asked)
- **B** — Measure the bill, then decide
- **C** — Apply unconditional levers now, with a bill-composition measurement as a gate
- **D** — Do nothing

## Criteria & Weights

| Criterion (phrased so higher is better) | Weight |
|---|---|
| Expected dollars saved | 5 |
| Certainty of the predicted saving | 5 |
| Speed to first realised saving | 4 |
| Engineering effort economy | 4 |
| Reversibility | 3 |
| Option preservation (does not foreclose Lambda later) | 3 |
| Operational simplicity | 3 |

## Scoring

| Option | Saved (×5) | Certainty (×5) | Speed (×4) | Effort (×4) | Revers. (×3) | Options (×3) | Ops (×3) | Total |
|---|---|---|---|---|---|---|---|---|
| A (Lambda now) | 3→15 | 1→5 | 1→4 | 1→4 | 2→6 | 2→6 | 2→6 | **46** |
| B (measure then decide) | 1→5 | 4→20 | 3→12 | 5→20 | 5→15 | 5→15 | 5→15 | **102** |
| C (levers + gate) | 4→20 | 5→25 | 5→20 | 4→16 | 4→12 | 5→15 | 4→12 | **120** |
| D (do nothing) | 1→5 | 5→25 | 1→4 | 5→20 | 5→15 | 4→12 | 5→15 | **96** |

## Recommendation

**C, at 120 vs. 102 for the runner-up** — a 17.6% margin, outside the ~10% sensitivity band, so no near-tie handling applies. Driven by the two weight-5 criteria. Note A is *not* dominated on "expected dollars saved" (a very spiky workload could beat C's ceiling), which is why this was a legitimate trade-off rather than a direct decision.

### Second-order pass (Phase 4)

| Effect | Order | Contradicts a GT? | Routing |
|---|---|---|---|
| Cold starts appear on user-facing paths | 2nd | no | extends C9 |
| Provisioned concurrency bought to fix them → pay for idle | 3rd | **yes — contradicted the then-scoped "Lambda bills only when running"** | **→ Phase 2 (fired)** |
| Savings Plan creates a committed spend floor | 2nd | no | extends C10 |
| Waste present at sizing time becomes contractual for the term | 3rd | no | extends C10 |
| Per-invocation DB connections → RDS Proxy or pool exhaustion | 2nd | no | → A-7 |
| Two compute platforms to operate; runbooks and pipelines duplicate | 2nd | no | → pre-mortem cluster 4 |

Stopping rule applied at 3rd order; the 4th order (e.g. "team attrition from operational burden") is non-actionable speculation here.

---

## Assumption Audit scan (process output, end of Phase 4)

| Chain | Step | Step Text (brief) | Assumption surfaced? | Added to Table? |
|---|---|---|---|---|
| C1 | H | GT-1 + GT-4 + GT-6 | A-10 same region (us-east-1) both sides | yes |
| C1 | 1 | one vCPU + 1.727 GB is the comparable unit | A-11 unit representative of their CPU:memory ratio | yes |
| C1 | 2 | $0.10365/h vs $0.04816/h | A-12 Lambda GB-second uses GB = 1024 MB | yes |
| C1 | 3 | Lambda is 2.15× per compute-hour | A-13 Fargate task sizes treated as continuous | yes |
| C2 | H | C1 + GT-11 + GT-2 | none | n/a |
| C2 | 1 | Fargate bills wall-clock, Lambda bills the busy fraction | A-9 containers already right-sized | yes |
| C2 | 2 | break-even at 46.5% | none | n/a |
| C2 | 3 | request fee adds $0.00072/h per sustained req/s | none | n/a |
| C2 | 4 | at 66.9 req/s no duty cycle helps | A-14 one vCPU can actually serve that rate | yes |
| C3 | H | C1 + GT-11 + GT-15? | none | n/a |
| C3 | 1 | Lambda bills elapsed duration including waits | none | n/a |
| C3 | 2 | container cost is flat in concurrency | A-14 (already added) | yes |
| C3 | 3 | effective multiple exceeds 2.15× | none | n/a |
| C4 | H | GT-6 + GT-7 + GT-8 | none | n/a |
| C4 | 1 | >900 s work cannot run on a standard invocation | A-15 work not splittable into sub-900 s units | yes |
| C4 | 2 | >5.8 vCPU cannot be expressed | A-11 (already added) | yes |
| C4 | 3 | scope bounded before cost is reached | none | n/a |
| C5 | H | GT-10 + GT-4 | none | n/a |
| C5 | 1 | a compute-line change leaves other lines untouched | A-16 no cross-line coupling (e.g. NAT, egress) | yes |
| C5 | 2 | total reduction = share × within-line reduction | none | n/a |
| C5 | 3 | no compute change beats compute's share | none | n/a |
| C6 | H | C2 + GT-13? + GT-14? | none | n/a |
| C6 | 1 | the sign is fixed by two unmeasured quantities | none | n/a |
| C6 | 2 | bracket runs −115% to +89% | A-17 measurement window is representative | yes |
| C6 | 3 | bracket straddles zero | none | n/a |
| C7 | H | C5 + GT-12? | none | n/a |
| C7 | 1 | the C5 ceiling evaluates to an unmeasured number | none | n/a |
| C7 | 2 | fastest path optimises an unbounded-unknown lever | none | n/a |
| C7 | 3 | the same ceiling bounds the C8 levers | none | n/a |
| C8 | H | GT-4 + GT-5 + GT-9 | none | n/a |
| C8 | 1 | arm64 takes the unit to $0.03853/h, 20.0% off | A-18 images rebuild and run correctly on arm64 | yes |
| C8 | 2 | a Compute Savings Plan covers Fargate and Lambda alike | none | n/a |
| C8 | 3 | stacked ceiling $0.01310/h, ~73% off | none | n/a |
| C9 | H | GT-3 + GT-4 + GT-6 | none | n/a |
| C9 | 1 | holding the unit warm costs $0.02591/h | none | n/a |
| C9 | 2 | execution rate falls to $0.06046/h | none | n/a |
| C9 | 3 | idle PC is 0.54× an idle Fargate task | none | n/a |
| C9 | 4 | break-even falls to 36.8% | none | n/a |
| C9 | 5 | PC must be pre-sized to peak concurrency | A-19 PC is configured to a fixed number ahead of demand | yes |
| C10 | H | C8 + GT-9 + GT-16? | none | n/a |
| C10 | 1 | the plan commits a fixed hourly spend for its term | A-20 terms are 1 or 3 years | yes |
| C10 | 2 | sizing before cleanup commits the waste | none | n/a |
| C10 | 3 | the plan also covers Lambda, so migration draws it down | none | n/a |
| C11 | H | C6 + C7 + C8 | none | n/a |
| C11 | 1 | weighted totals 120 > 102 > 96 > 46 | A-21 weights reflect the org's real priorities | yes |
| C11 | 2 | levers now, gated, Lambda decided per service | none | n/a |

46 rows, one per chain per step, in order. Twelve assumptions surfaced; all twelve added to the Assumptions Table (A-9 through A-21, with A-11 and A-14 each surfacing on two steps and added once).

---

## Adversarial pass (process output)

Conclusion type: **plan / recommendation** → Pre-Mortem (procedure opened at `/home/chrisdavidson/Projects/first-principles-skill/first-principles/agents/references/pre-mortem.md`).

**Premise.** It is six months from now. We applied the levers, measured, and migrated the qualifying services — and the AWS bill is not lower. We are paying more than when we started and the platform team has lost a quarter.

**Causes** (unfiltered, written before grouping; generated from four named viewpoints).

*Implementing engineer:* the arm64 rebuild stalled on a native dependency with no ARM wheel, so the 20% never landed. Right-sizing was done from CloudWatch means, and p99-driven autoscaling reverted every size within a month. The duty-cycle measurement week contained a product launch and was not typical. Per-service tagging was never finished, so 40% of spend landed in "untagged" and the breakdown was unusable.

*Finance owner who pays:* we sized the Savings Plan against pre-cleanup spend because the cleanup slipped and quarter-end did not, so we are committed to our own waste for three years. Compute turned out to be 15% of the bill; RDS and data transfer were 60%, so even a perfect compute result was immaterial. Engineering hours spent exceeded the annualised saving.

*On-call engineer who lives with it:* migrated services cold-start on the user-facing path, we bought provisioned concurrency, and most of the saving evaporated. We now operate two compute platforms and every runbook, dashboard and deploy pipeline exists twice. Lambda concurrency exhausted the RDS connection pool during a spike and caused an outage.

*Competitor who benefits:* their platform team spent two quarters on a cost project while we shipped features. Their engineers now avoid the migrated services because the local development story got worse.

**Adversarial interrogation.** The highest-signal item is the one that embarrasses *my own* recommendation rather than yours: "compute turned out to be 15% of the bill." My recommended levers are also compute levers. If that cause fires, option C is nearly as immaterial as option A. I had softened this into "measure in parallel"; that was the hedge, and it is the item to un-hedge.

**Clusters and dispositions.**

| Cluster | Bears on | Disposition |
|---|---|---|
| **1. The analysis optimises compute without establishing that compute matters** | C5, C7, C11, GT-12? | **Plan change.** The Cost Explorer breakdown becomes a **gate, not a parallel task**: if compute is under ~25% of the bill, stop and re-target the whole analysis at the dominant line item before taking any other action. This changed the recommendation and is reflected in §6. |
| **2. Measurement windows and tags are assumed good** | C6, GT-12?, GT-13?, A-17 | **Plan change.** Require ≥2 weeks spanning a full business cycle; require ≥90% tag coverage before trusting any breakdown; use p95 CPU, not mean, for both right-sizing and the duty-cycle test. |
| **3. Commitment ordering fails under schedule pressure** | C10, A-20 | **Plan change.** Use a 1-year no-upfront plan sized to the *measured post-cleanup* floor, explicitly decoupled from any quarter-end date. **Accepted residual risk:** a 1-year plan yields a lower discount than 3-year; **mitigation:** Compute Savings Plans cover Lambda as well as Fargate (GT-9), so a later migration draws the commitment down rather than stranding it. |
| **4. The Lambda leg's hidden costs sit outside the cost model** | C2, C3, C9, A-7 | **Accepted risk with named mitigation.** Migrate at most one non-user-facing, low-duty-cycle service first and measure its realised bill delta over a full month before migrating a second. The mitigation is blast radius: at one service the decision is cheaply reversible. |
| **5. Graviton is assumed to be a free 20%** | C8, A-18 | **Plan change.** Spike the arm64 rebuild on the single highest-spend service first, time-boxed to one week; if it exceeds the box, drop Graviton and keep the Savings Plan lever, which requires no rebuild at all. |

**Weakest link per chain** (Phase 5 inspection):

| Chain | Weakest link |
|---|---|
| C1 | A-12 — the GB = 1024 MB base; if it is 1000 MB the multiple is 2.20× and break-even 45.4%, which does not change any conclusion |
| C2 | A-14 — whether one vCPU can physically serve ~67 req/s for the workload in question |
| C3 | GT-15? — the one-invocation-per-environment property was not read at source |
| C4 | A-15 — whether long-running work is splittable into sub-900-second units |
| C5 | A-16 — cross-line coupling; a Lambda-in-VPC migration can move NAT Gateway cost, violating line independence |
| C6 | GT-13?/GT-14? — the entire chain is an absent-evidence result |
| C7 | GT-12? — single unmeasured number the conclusion turns on |
| C8 | A-18 — the arm64 rebuild assumption (now time-boxed per cluster 5) |
| C9 | A-19 — that provisioned concurrency must be pre-sized |
| C10 | GT-16? — the realised term-specific discount was not located |
| C11 | Inherits C6 and C7; also A-21, the weights |

---

## §6→§4 closure ledger (process output)

```text
- "Apply the two unconditional compute levers ... gated on a bill-composition measurement" → chains C8, C11 ✓
- "Pull a Cost Explorer breakdown by service ... treat it as a gate" → chain C5 ✓
- "Switch Fargate tasks to arm64 and right-size them from p95" → chain C8 ✓
- "Size a Compute Savings Plan to the post-cleanup floor, not today's spend" → chains C8, C10 ✓
- "Instrument per-service CPU duty cycle and request rate for two weeks" → chain C2 ✓
- "Migrate only services that clear the eligibility screen and fall below the threshold" → chains C2, C4 ✓
- "Serverless is not categorically cheaper; it is cheaper below a derivable threshold" → chain C2 ✓
- "Trade-offs acknowledged: ~73% is a ceiling, not a forecast" → chain C8 ✓
- "Confidence: LOW overall, though the compute arithmetic is HIGH" → chains C1, C11 ✓
```

Ledger clean: 9 of 9 §6 claims carry a chain reference. 0 cut.

---

## Self-audit scan (process output)

| Chain | Chain Head (brief) | Form conforming? | Rule applied | Dependency clean? |
|---|---|---|---|---|
| C1 | GT-1 + GT-4 + GT-6 | yes | n/a | yes |
| C2 | C1 + GT-11 + GT-2 | yes | n/a | yes |
| C3 | C1 + GT-11 + GT-15? | yes | n/a | yes |
| C4 | GT-6 + GT-7 + GT-8 | yes | n/a | yes |
| C5 | GT-10 + GT-4 | yes | n/a | yes |
| C6 | C2 + GT-13? + GT-14? | yes | n/a | yes |
| C7 | C5 + GT-12? | yes | n/a | yes |
| C8 | GT-4 + GT-5 + GT-9 | yes | n/a | yes |
| C9 | GT-3 + GT-4 + GT-6 | yes | n/a | yes |
| C10 | C8 + GT-9 + GT-16? | yes | n/a | yes |
| C11 | C6 + C7 + C8 | yes | n/a | yes |

| §6 Span (brief) | Construct | Claim under R11? | R11 clause applied | Chain cited |
|---|---|---|---|---|
| "This analysis does not tell you..." | prose | no | prose carrying neither a bold colon lead-in nor a list marker | n/a |
| "**Recommended approach:** Apply the two unconditional..." | bold lead-in | yes | prescribed lead-in, always a claim | C8, C11 |
| "1. Pull a Cost Explorer breakdown..." | list item | yes | closes its own sentence and runs past forty characters | C5 |
| "2. Switch Fargate tasks to arm64..." | list item | yes | closes its own sentence and runs past forty characters | C8 |
| "3. Size a Compute Savings Plan..." | list item | yes | closes its own sentence and runs past forty characters | C8, C10 |
| "4. Instrument per-service CPU duty cycle..." | list item | yes | closes its own sentence and runs past forty characters | C2 |
| "5. Migrate only services that clear..." | list item | yes | closes its own sentence and runs past forty characters | C2, C4 |
| "**Key insight:** Serverless is not categorically..." | bold lead-in | yes | prescribed lead-in, always a claim | C2 |
| "**Trade-offs acknowledged:** the ~73% is a ceiling..." | bold lead-in | yes | prescribed lead-in, always a claim | C8 |
| "The arm64 leg assumes images rebuild..." | prose | no | prose carrying neither a bold colon lead-in nor a list marker; carries the flagged-assumption marker | n/a |
| "**Confidence:** LOW overall, though..." | bold lead-in | yes | bold lead-in whose colon closes the bold span | C1, C11 |

```text
Scan complete: 11 chain rows, one per section-4 chain block in order; 11 section-6 rows, one per construct in order — 9 claims under R11, 2 excluded. 0 chains malformed, 0 claims untraced.
```

---

## Self-Audit Gate (process output)

**Criterion 1: Identify Essence**
Quoted span: *"Which changes to our AWS account reduce total spend the most per unit of engineering effort and risk — of which a Lambda migration is one candidate answer, not the question."*
Band: **Rigorous**
Justification: the statement names the underlying decision rather than the triggering event ("cut our AWS bill") or the prompt's pre-committed solution, and each success criterion below it is a scannable pass/fail test against the Conclusion section.

**Criterion 2: Challenge Assumptions**
Quoted span (Assumption Audit scan): *"C9 | 5 | PC must be pre-sized to peak concurrency | A-19 PC is configured to a fixed number ahead of demand | yes"*
Band: **Rigorous**
Justification: the audit visited all 46 named chain steps in order, every Type value is drawn from exactly the four-type scheme, the convention row A-1 is actually challenged rather than labelled Accept, and each of the twelve surfaced assumptions was written back into the table.

**Criterion 3: Establish Ground Truths**
Quoted span: enumerated GT-12, GT-13, GT-14, GT-15, GT-16; the list carries `?` on exactly those five and on no others, checked entry by entry against §3.
Band: **Rigorous**
Justification: all sixteen IDs are stable and referenced in §4, every unsuffixed GT names a read-at-source location and feeds at least one HIGH-confidence chain (GT-1→C1, GT-2→C2, GT-3→C9, GT-4→C1, GT-5→C8, GT-6→C1, GT-7→C4, GT-8→C4, GT-9→C8, GT-10→C5, GT-11→C2), and the one Phase 3 failure record names its source and reason.

**Criterion 4: Reason Upward**
Quoted span (self-audit scan): *"C11 | C6 + C7 + C8 | yes | n/a | yes"*
Band: **Rigorous**
Justification: all eleven chain blocks score form-conforming with clean dependencies, every conclusion has exactly one chain with a genuine intermediate, Abandoned Reasoning documents four dead ends in the What-was-tried / Why-abandoned / What-it-ruled-out structure, and the one place an industry-typical bill composition could have been used as evidence is instead recorded as a dead end under the no-analogies ban.

**Criterion 5: Validate**
Quoted span: *"**Confidence:** LOW — capped by C6 and C7, both LOW..."* on chain C11, against the Conclusion section's own **Confidence: LOW**.
Band: **Sound**
Justification: the adversarial pass ran with a past-tense premise, a four-viewpoint unfiltered cause list written before grouping, and five clusters each citing chain ids and carrying a named plan change or an accepted risk with a named mitigation — but the overall Conclusion rating is LOW rather than HIGH, which the criterion bands below Rigorous even though every §6 claim does rest on at least one HIGH chain. Neither EXCEPT clause is claimed.

**Criterion 6: Conclusion-to-Ground-Truth Traceability**
Quoted span (self-audit scan): *"9 claims under R11, 2 excluded. 0 chains malformed, 0 claims untraced."*
Band: **Rigorous**
Justification: every one of the nine §6 claims cites a named §4 chain inline, no claim introduces reasoning absent from §4, and the Key Insight (a derivable 46.5% threshold that converts a category belief into a measurable test) is a distinct non-obvious finding rather than a restatement of the recommended approach.

**Gate result: PASS.** No criterion Absent; one criterion at Sound and none at Hand-wavy, so the hand-wavy cap is cleared. No Fix/Repeat pass was required.

---

# First-Principles Analysis: Reducing AWS Spend

## 1. Problem Essence

**Core problem:** Which changes to our AWS account reduce total spend the most per unit of engineering effort and risk — of which a Lambda migration is one candidate answer, not the question.

**Success criteria.** A correct answer must:

1. Identify where the money actually goes before prescribing where it should go — the Conclusion names a measurement action ahead of any migration action.
2. Trace every cost claim to a price-list figure or an explicit arithmetic bound, not to a category belief — no claim in the Conclusion rests on "serverless is cheaper" as a premise.
3. Rank actions by dollars saved per unit of engineering effort and risk — the Conclusion orders its actions and states the ordering's reason.
4. Remain correct in the case where compute is *not* the dominant line item — the Conclusion states what happens if that case obtains.
5. Give a falsifiable per-service test for Lambda rather than a blanket verdict — the Conclusion names a numeric threshold and how to measure against it.

**Symptom vs. cause.** "The bill is too high" is the symptom. "We do not know the bill's composition, and we are about to spend a quarter of engineering time on one branch of one category of it" is the cause of the *decision* problem, which is what this analysis addresses.

## 2. Assumptions Table

| Assumption | Type | Treatment | Verdict | Verification |
|---|---|---|---|---|
| A-1 "Everyone knows serverless is cheaper than containers" | convention | Explicitly challenge before use | **Discard** — contradicted by GT-1/GT-4/GT-6; the claim is true only below a 46.5% duty cycle and false above it, so it is not a category fact | Arithmetic from AWS price list, chain C1/C2 |
| A-2 Our services run below the break-even duty cycle | untested belief | Verify or flag | **Challenge** — determines the sign of the entire saving, flagged GT-13? | unverified — flagged |
| A-3 Request rate is below ~67/s per vCPU-equivalent | untested belief | Verify or flag | **Challenge** — flagged GT-14? | unverified — flagged |
| A-4 Compute is the dominant line item on the bill | untested belief | Verify or flag | **Challenge** — highest-stakes assumption in the analysis, flagged GT-12? | unverified — flagged |
| A-5 Services are CPU-bound with low concurrency per vCPU | untested belief | Verify or flag | **Challenge** — if false, C3 applies and the multiple worsens | unverified — flagged |
| A-6 Cold-start latency is acceptable on these paths | untested belief | Verify or flag | **Challenge** — drives the C9 provisioned-concurrency branch | unverified — flagged |
| A-7 Migration adds no new billed components | untested belief | Verify or flag | **Challenge** — RDS Proxy and API Gateway are the named candidates | unverified — flagged |
| A-8 Migration engineering cost is small vs. the saving | untested belief | Verify or flag | **Challenge** — pre-mortem cluster 1 names the case where it is not | unverified — flagged |
| A-9 Current containers are right-sized to actual use | untested belief | Verify or flag | **Challenge** — if false, right-sizing alone captures most of the apparent Lambda win | unverified — flagged |
| A-10 Both platforms priced in the same region (us-east-1) | current constraint | Record expiry conditions | **Accept** — expires if the estate is not in us-east-1; re-run the same arithmetic with that region's rates, which changes the magnitudes but not the structure | AWS pricing pages, us-east-1 tab |
| A-11 One vCPU + 1.727 GB is representative of their CPU:memory ratio | untested belief | Verify or flag | **Challenge** — a memory-heavy service shifts the break-even toward Lambda; recompute per service | unverified — flagged |
| A-12 Lambda's GB-second uses GB = 1024 MB | untested belief | Verify or flag | **Accept** — sensitivity tested: the 1000-MB reading gives 2.20× and a 45.4% threshold, changing no conclusion | Sensitivity analysis, §4 C1 |
| A-13 Fargate task sizes are continuous rather than discrete steps | untested belief | Verify or flag | **Challenge** — discrete sizing rounds a task up and inflates the Fargate side, favouring Lambda | unverified — flagged |
| A-14 One vCPU can physically serve ~67 req/s for this workload | untested belief | Verify or flag | **Challenge** — the bound is real arithmetic but the rate may be unreachable for heavy handlers | unverified — flagged |
| A-15 Long-running work is not splittable into sub-900-second units | untested belief | Verify or flag | **Challenge** — splittable work escapes the C4 exclusion via Step Functions | unverified — flagged |
| A-16 No cross-line coupling between compute and other bill lines | untested belief | Verify or flag | **Challenge** — a Lambda-in-VPC migration moves NAT Gateway cost, which violates C5's line independence | unverified — flagged |
| A-17 A measurement window will be representative | untested belief | Verify or flag | **Challenge** — pre-mortem cluster 2; mitigated by requiring ≥2 weeks across a business cycle | unverified — flagged |
| A-18 Container images rebuild and run correctly on arm64 | untested belief | Verify or flag | **Challenge** — pre-mortem cluster 5; mitigated by a one-week time-boxed spike | unverified — flagged |
| A-19 Provisioned concurrency is configured to a fixed number ahead of demand | untested belief | Verify or flag | **Challenge** — near-definitional but not read at source; declared inline on C9 step 5 | unverified — flagged |
| A-20 Savings Plan terms are 1 or 3 years | untested belief | Verify or flag | **Challenge** — the term lengths were not located on the fetched page | unverified — flagged |
| A-21 The trade-off weights reflect the organisation's real priorities | untested belief | Verify or flag | **Challenge** — weights were locked before scoring, but they are mine, not yours; re-weight and re-run if effort or reversibility matters more | unverified — flagged |
| A-22 Prices read on 2026-09-20 hold through the decision window | current constraint | Record expiry conditions | **Accept** — expires on any AWS price change; AWS price changes have historically been downward, which would strengthen C8 and weaken nothing | AWS pricing pages, read 2026-09-20 |

## 3. Ground Truths

- **GT-1** Lambda x86 on-demand duration is $0.0000166667 per GB-second in us-east-1 — source: aws.amazon.com/lambda/pricing/; read-at-source: the figure appears in the us-east-1 on-demand pricing examples.
- **GT-2** Lambda charges $0.20 per one million requests — source: aws.amazon.com/lambda/pricing/; read-at-source: stated consistently across the us-east-1 pricing examples.
- **GT-3** Lambda provisioned concurrency is $0.0000041667 per GB-s for the concurrency charge plus $0.0000097222 per GB-s for execution while active — source: aws.amazon.com/lambda/pricing/; read-at-source: the provisioned-concurrency pricing block.
- **GT-4** Fargate Linux/x86 is $0.000011244 per vCPU-second and $0.000001235 per GB-second in us-east-1 — source: aws.amazon.com/fargate/pricing/; read-at-source: the us-east-1 per-second rates in the pricing examples.
- **GT-5** Fargate Linux/ARM is $0.0000089944 per vCPU-second and $0.0000009889 per GB-second — source: aws.amazon.com/fargate/pricing/; read-at-source: the same us-east-1 example block, ARM rows.
- **GT-6** At 1,769 MB a Lambda function has the equivalent of one vCPU — source: docs.aws.amazon.com/lambda/latest/dg/configuration-memory.html; read-at-source: quoted verbatim, *"At 1,769 MB, a function has the equivalent of one vCPU (one vCPU-second of credits per second)."*
- **GT-7** Lambda's function timeout is 900 seconds (15 minutes); Managed Instances async and event-source-mapping invocations allow 5,400 seconds — source: docs.aws.amazon.com/lambda/latest/dg/gettingstarted-limits.html; read-at-source: the "Function timeout" row of the function-configuration quota table.
- **GT-8** Lambda memory is configurable from 128 MB to 10,240 MB, and *"Lambda allocates CPU power in proportion to the amount of memory configured"* — source: same quotas page; read-at-source: the "Function memory allocation" row.
- **GT-9** Compute Savings Plans *"reduce your costs by up to 66%"* and *"also apply to Fargate or Lambda usage"* — source: aws.amazon.com/savingsplans/compute-pricing/; read-at-source: quoted verbatim from the Compute Savings Plans description.
- **GT-10** A total bill is the sum of independently-priced line items, so a change confined to one line reduces the total by that line's share multiplied by the fractional reduction within it — source: arithmetic (the distributive property over a sum); read-at-source: definitional, no external citation required.
- **GT-11** Lambda's on-demand billing unit is GB-seconds of invocation duration, while Fargate's is vCPU-seconds and GB-seconds of task lifetime — source: GT-1 and GT-4's unit definitions on both pricing pages; read-at-source: the per-unit denominators as printed on each page.
- **GT-12?** The composition of this account's bill by service — unverified: no cost data was supplied and this analysis has no access to the account.
- **GT-13?** The average CPU duty cycle of the services under consideration — unverified: not supplied and not measurable from here.
- **GT-14?** The sustained request rate per service per vCPU-equivalent — unverified: not supplied and not measurable from here.
- **GT-15?** A Lambda execution environment serves one invocation at a time, so IO wait is billed — unverified: the quotas page states a rate limit (*"Each instance of your execution environment can serve up to 10 requests per second"*) which does not by itself establish the concurrency model; **Phase 3 failure record** — source opened, `citation does not support the claim`.
- **GT-16?** The realised Compute Savings Plan discount for a specific term and payment option — unverified: only the "up to 66%" ceiling was located; **Phase 3 failure record** — source opened, the term-and-payment rate table did not render in the fetched content.

**Provenance summary.** `?`-marked: GT-12, GT-13, GT-14, GT-15, GT-16 (5 of 16). Read-at-source for every unsuffixed GT feeding a HIGH-confidence chain: GT-1, GT-2, GT-3 — us-east-1 pricing examples on the Lambda pricing page; GT-4, GT-5 — us-east-1 per-second rates on the Fargate pricing page; GT-6 — `configuration-memory.html`, sentence quoted verbatim; GT-7, GT-8 — the quota table rows named above; GT-9 — the Compute Savings Plans description, quoted verbatim; GT-10 — definitional arithmetic; GT-11 — the billing denominators printed on both pricing pages.

## 4. Derivation Chains

### Conclusion C1: Per hour of actual compute, Lambda costs 2.15× Fargate.

```text
GT-1 (Lambda $0.0000166667/GB-s) + GT-4 (Fargate $/vCPU-s and $/GB-s) + GT-6 (1,769 MB = one vCPU)
→ the one unit comparable across both services is a single vCPU plus the 1.727 GB Lambda attaches to it *[Assumes: A-11]*
→ that unit costs $0.10365 per hour of billed Lambda duration against $0.04816 per hour of Fargate task lifetime *[Assumes: A-12]*
→ Lambda is 2.15× the price of Fargate per hour of actual compute *[Assumes: A-13]*
```

**Confidence:** HIGH

### Conclusion C2: Lambda wins only below a 46.5% duty cycle, and above ~67 requests per second per vCPU it cannot win at any duty cycle.

```text
C1 (2.15× per compute-hour) + GT-11 (invocation-duration vs task-lifetime billing units) + GT-2 ($0.20 per million requests)
→ Fargate bills the unit for every wall-clock hour while Lambda bills only the fraction of that hour spent executing *[Assumes: A-9]*
→ the two are equal at a duty cycle of 1/2.15, putting the break-even at 46.5% busy time
→ the request fee adds $0.00072 per wall-clock hour for each sustained request per second, independent of duty cycle
→ at 66.9 requests per second the fee alone equals the entire Fargate bill, so below that no duty cycle rescues Lambda *[Assumes: A-14]*
```

**Confidence:** HIGH

### Conclusion C3: For IO-bound services the 2.15× understates Lambda's cost.

```text
C1 (2.15× per compute-hour) + GT-11 (invocation-duration billing) + GT-15? (one invocation per execution environment)
→ Lambda bills the elapsed duration of every invocation, including time spent waiting on a database or a downstream call
→ one container vCPU holds many such waits concurrently at no extra charge, so its billed cost is flat in concurrency while Lambda's is linear *[Assumes: A-14]*
→ for a service whose latency is dominated by waiting rather than computing, the effective multiple exceeds 2.15× by roughly the mean concurrency per vCPU
```

**Confidence:** LOW — rests on GT-15?, whose asserted property was not found in the opened source (Phase 3 failure record: `citation does not support the claim`); reading the Lambda execution-environment and concurrency documentation directly would remove it as a cause of the downgrade. It also cites C1, rated HIGH, which imposes no ceiling.

### Conclusion C4: Hard service limits exclude part of the estate before any cost argument is reached.

```text
GT-6 (1,769 MB = one vCPU) + GT-7 (900-second function timeout) + GT-8 (128–10,240 MB ceiling, CPU proportional to memory)
→ any task whose single unit of work exceeds 900 seconds cannot execute on a standard Lambda invocation at all *[Assumes: A-15]*
→ any task requiring more than about 5.8 vCPU cannot be expressed, since 10,240 MB is the ceiling and 1,769 MB buys one vCPU *[Assumes: A-11]*
→ the migration's scope is bounded by hard service limits independently of whether it would save money
```

**Confidence:** HIGH

### Conclusion C5: No compute-platform change can cut the bill by more than compute's share of it.

```text
GT-10 (a bill is a sum over independently-priced line items) + GT-4 (Fargate compute is one such line, priced per vCPU-second and GB-second)
→ a change confined to the compute line alters that line's price or quantity and leaves every other line's price and quantity untouched *[Assumes: A-16]*
→ the fractional reduction in the total is therefore the compute line's share multiplied by the fractional reduction achieved within it
→ no compute-platform change, Lambda or otherwise, can reduce the bill by more than compute's share of it
```

**Confidence:** HIGH

### Conclusion C6: Whether a Lambda migration saves money is undecidable from the information available.

```text
C2 (46.5% duty-cycle threshold) + GT-13? (duty cycle unmeasured) + GT-14? (request rate unmeasured)
→ the sign of the compute saving is fixed entirely by two quantities this analysis has not measured
→ the bracket on the compute line runs from an 89.2% saving at a 5% duty cycle to a 115.2% increase at full duty *[Assumes: A-17]*
→ the bracket straddles zero, so its two ends recommend opposite actions and the estimate does not resolve the decision
```

**Confidence:** LOW — rests on GT-13? and GT-14?, both removed as causes of the downgrade by two weeks of CloudWatch per-service CPU-utilisation and request-count data. It cites C2, rated HIGH, which imposes no ceiling.

### Conclusion C7: The migration's maximum effect on the bill is an unmeasured number, and the same bound gates every other option.

```text
C5 (compute-share ceiling) + GT-12? (line-item composition unknown)
→ the ceiling C5 establishes evaluates to an unmeasured number for this estate
→ the fastest path to Lambda therefore optimises a lever whose maximum effect on the bill nobody has stated
→ that same ceiling bounds the C8 levers equally, so the measurement gates every option rather than the migration alone
```

**Confidence:** LOW — rests on GT-12?, removed as a cause of the downgrade by a single Cost Explorer or CUR query grouped by service, which is under an hour of work. It cites C5, rated HIGH, which imposes no ceiling.

### Conclusion C8: Two levers cut the compute unit by up to ~73% with no change to the execution model.

```text
GT-4 (Fargate x86 rates) + GT-5 (Fargate ARM rates) + GT-9 (Compute Savings Plans, up to 66%, covering Fargate and Lambda)
→ moving the same task from Linux/x86 to Linux/ARM takes the unit from $0.04816 to $0.03853 per hour, a 20.0% cut with no change to the billing model *[Assumes: A-18]*
→ a Compute Savings Plan applies on top and covers Fargate and Lambda alike, so committing to one is not a bet on either platform
→ stacking both bounds the unit at $0.01310 per hour, a ceiling of about 73% off on-demand x86
```

**Confidence:** HIGH

### Conclusion C9: Provisioned concurrency improves Lambda's cost position and destroys its operational one.

```text
GT-3 (provisioned-concurrency rates) + GT-4 (Fargate rates) + GT-6 (1,769 MB = one vCPU)
→ holding the unit warm under provisioned concurrency costs $0.02591 per hour of idle time
→ the execution rate falls from $0.10365 to $0.06046 per hour of billed duration
→ idle provisioned concurrency therefore costs 0.54× an idle Fargate task
→ the break-even duty cycle falls from 46.5% to 36.8%
→[2nd] the cold-start fix improves Lambda's cost position rather than destroying it
→[3rd] provisioned concurrency must be sized to peak concurrency in advance, reinstating the capacity planning that serverless was adopted to remove *[Assumes: A-19]*
```

**Confidence:** HIGH

### Conclusion C10: Clean up and right-size before sizing any Savings Plan commitment.

```text
C8 (Savings Plan ceiling) + GT-9 (the plan is a term commitment covering EC2, Fargate and Lambda) + GT-16? (term-specific realised rate not located)
→ a Savings Plan commits a fixed hourly spend for its whole term, so any waste present at sizing time is committed to for that term *[Assumes: A-20]*
→[2nd] sizing the plan before the cleanup converts a one-off waste problem into a contractual floor
→[3rd] because the plan also covers Lambda, a later migration still draws the commitment down, so the ordering risk is waste-sizing rather than platform choice
```

**Confidence:** MEDIUM — rests on GT-16?, removed as a cause of the downgrade by pricing the specific term and payment option in the console's Savings Plans recommendations view. It cites C8, rated HIGH, which imposes no ceiling.

### Conclusion C11: Apply the unconditional levers now under a measurement gate, and decide Lambda per service afterwards.

```text
C6 (Lambda's sign undecidable) + C7 (bill-share unmeasured) + C8 (~73% unconditional ceiling)
→ weighted totals: levers-with-gating-measurement 120 > measure-then-decide 102 > do-nothing 96 > migrate-now 46, driven by expected saving and certainty at weight 5 each *[Assumes: A-21]*
→ apply the unconditional levers now under a measurement gate, then decide Lambda per service against the threshold established in C2
```

**Confidence:** LOW — capped by C6 and C7, both rated LOW, whose own confidence lines carry their verification paths. The rating is a ceiling inherited from those two chains, not a judgement that the recommendation is weak: the recommendation is in fact robust across the entire width of C6's bracket, because both ends of that bracket prescribe the same first move.

## 5. Abandoned Reasoning

### Dead End: "Provisioned concurrency destroys Lambda's cost advantage"

**What was tried:** The second-order pass produced the intuitive result that buying provisioned concurrency to fix cold starts reintroduces paying for idle capacity, thereby erasing the only property that made Lambda cheaper.

**Why abandoned:** It contradicted a Ground Truth, which routed it back to Phase 2 for re-challenging — and the arithmetic then falsified it. The provisioned-concurrency rate ($0.0000041667/GB-s) is a quarter of the on-demand duration rate, so idle provisioned concurrency costs 0.54× an idle Fargate task and the break-even duty cycle *falls* from 46.5% to 36.8%. The original ground truth was too coarsely scoped; it now reads "on-demand Lambda bills only during invocation," with provisioned concurrency as a separate mode (GT-3).

**What it ruled out:** It saves the reader from the widespread claim that provisioned concurrency makes Lambda pointless on cost grounds. The real objection to provisioned concurrency is operational, not financial — it reinstates capacity planning (C9) — and confusing the two leads to arguing the wrong case.

### Dead End: Using a typical industry AWS bill composition as a stand-in for GT-12?

**What was tried:** Substituting a published or commonly-cited distribution of AWS spend (EC2/compute ~X%, RDS ~Y%, data transfer ~Z%) to give the Amdahl bound in C5 a concrete value and make C7 decidable.

**Why abandoned:** This is reasoning by analogy used as direct evidence, which the methodology bans in Phase 4. Another organisation's bill composition is a fact about their architecture, not about yours, and there is no ground truth connecting the two. The substitution would have made the analysis feel decisive while making its central number fictional.

**What it ruled out:** It rules out every version of this analysis that produces a dollar figure. No dollar figure is derivable from the information supplied, and an analysis that produces one has smuggled in an assumption. The honest output is a bound plus a one-hour query that collapses it.

### Dead End: Comparing Lambda on arm64 against Lambda on x86

**What was tried:** Extending the Graviton lever in C8 to the Lambda side, so that the migration option and the levers option could be compared on equal architectural footing.

**Why abandoned:** The Lambda pricing page's Arm tab did not render its rates in the fetched content, so the arm64 duration rate could not be read at source. Rather than carry a remembered figure into a chain, the comparison was dropped — the analysis never needs it, since the arm64 discount applies to whichever platform is chosen and therefore cancels out of the platform decision.

**What it ruled out:** It rules out treating Graviton as a reason to prefer one platform over the other. Like the Savings Plan (GT-9), it is orthogonal to the Lambda-versus-Fargate question and belongs in the unconditional bucket.

### Dead End: A theoretical-limit pass on the floor of the bill

**What was tried:** Deriving a law-permitted lower bound on the cost of serving this workload — energy per unit of computation, a Landauer-style or datacentre-PUE-anchored floor — on the model of a Carnot-efficiency analysis, to establish how much headroom exists between current spend and physics.

**Why abandoned:** The governing constraint here is a published price list, which is a contract, not a physical law. AWS's margin, its amortisation schedule and its pricing strategy sit between the physics and the invoice, and none of them is derivable from first principles. A Carnot-style ceiling would have been numerically impressive and decision-irrelevant. The real ceiling on this decision is the arithmetic bound in C5 — compute's share of the bill — which is an accounting identity rather than a physical law, and which is the correct instrument for this problem.

**What it ruled out:** It rules out the framing that there is large untapped headroom waiting to be unlocked by cleverness. The headroom is bounded by C5 and by GT-9's 66%, both of which are contractual numbers you can look up rather than physical ones you must derive.

## 6. Conclusion

This analysis does not tell you whether to move to Lambda, because the two quantities that decide it have not been measured — and that absence is itself the finding, not a shortfall in the analysis.

**Recommended approach:** Apply the two unconditional compute levers, which cut the compute unit by up to ~73% with no change to the execution model and no bet on either platform (chain C8), gated on a bill-composition measurement that bounds every option on the table (chain C11).

In this order:

1. Pull a Cost Explorer breakdown by service for the last 90 days and treat it as a gate, not a parallel task — if compute is under ~25% of the bill, stop and re-target this analysis at the dominant line item (chain C5).
2. Switch Fargate tasks to arm64 and right-size them from p95 rather than mean utilisation, spiking the highest-spend service first under a one-week time box (chain C8).
3. Size a Compute Savings Plan to the post-cleanup floor, not today's spend, and decouple the decision from any quarter-end date (chains C8 and C10).
4. Instrument per-service CPU duty cycle and request rate for two weeks spanning a full business cycle (chain C2).
5. Migrate only services that clear the eligibility screen and then fall below the threshold, starting with exactly one non-user-facing service measured over a full month (chains C2 and C4).

**Key insight:** Serverless is not categorically cheaper or dearer than containers — it is cheaper below a duty cycle of 46.5% and dearer above it, and above roughly 67 requests per second per vCPU the per-request fee alone exceeds the whole container bill, so no duty cycle rescues it (chain C2). This converts the category belief in your question into a per-service measurement with a number attached, which is something reasoning by analogy cannot reach: the belief is not wrong, it is *conditional*, and nobody has checked the condition.

**Trade-offs acknowledged:** the ~73% is a ceiling requiring the maximum Savings Plan commitment, not a forecast; taking the unconditional levers first defers any architectural upside, and for a genuinely spiky workload a Lambda migration could eventually beat this path — which is why step 5 keeps that door open rather than closing it (chain C8).

The arm64 leg assumes images rebuild cleanly for ARM, and the realised Savings Plan discount for a 1-year no-upfront commitment is materially below the 66% ceiling — no chain — flagged assumption only.

**Confidence:** LOW overall, though the compute-unit arithmetic underneath it is HIGH (chain C1) — the rating is set by C11, capped by C6 and C7, both LOW because GT-12?, GT-13? and GT-14? are unmeasured; roughly one hour of Cost Explorer work removes GT-12?, and two weeks of CloudWatch data removes GT-13? and GT-14?, at which point this analysis re-runs at HIGH with actual numbers (chain C11).

---

**Files read in this analysis** (all absolute, per the reference convention): `/home/chrisdavidson/Projects/first-principles-skill/first-principles/agents/references/trade-off.md`, `/home/chrisdavidson/Projects/first-principles-skill/first-principles/agents/references/pre-mortem.md`, `/home/chrisdavidson/Projects/first-principles-skill/first-principles/agents/references/output-template.md`, `/home/chrisdavidson/Projects/first-principles-skill/first-principles/agents/references/validation-rubric.md`. All four reads succeeded; no template or rubric read failed, and no omission disclosure is required beyond the re-entry edge declared at the top.