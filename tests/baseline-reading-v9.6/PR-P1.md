I couldn't ask you for the missing inputs, because the question tool isn't available in this session. So this is a best-effort analysis. Four facts would settle it, and I have none of them:

1. **Your AWS bill by service.** Cost Explorer, grouped by service and usage type.
2. **How your containers run today.** For example ECS on Fargate, EKS, or EC2.
3. **Traffic per service.** Request rate, typical latency and how many tasks you run.
4. **Latency targets.** How much delay each service can tolerate.

Where I needed a baseline, I used Fargate on-demand pricing in US East (N. Virginia).

## Assumption Audit scan (process output)

| Chain | Step | Step Text (brief) | Assumption surfaced? | Added to Table? |
|---|---|---|---|---|
| C1 | 1 | one Lambda vCPU-equivalent costs $0.000028792/s | none | n/a |
| C1 | 2 | 1 vCPU + 2 GB Fargate x86 task costs $0.000013714/s | none | n/a |
| C1 | 3 | Lambda 2.10× per busy second, ~14% less memory | A5 (already in table) | n/a |
| C1 | 4 | Lambda can only win by not paying for idle time | none | n/a |
| C2 | 1 | Lambda bills each in-flight request's full wall-clock time | none | n/a |
| C2 | 2 | a container pays once for time Lambda bills k times | A6 (already in table) | n/a |
| C2 | 3 | effective premium is 2.10 × k | none | n/a |
| C2 | 4 | request fee adds ~7% at 100 ms | none | n/a |
| C2 | 5 | Lambda wins only below busy fraction ≈ 1/(2.10 × k) | none | n/a |
| C2 | 6 | ~48% at k=1, ~10% at k=5 | none | n/a |
| C3 | 1 | no service can be placed against the threshold unmeasured | none | n/a |
| C3 | 2 | the saving is capped at the unmeasured compute share | A2 (already in table) | n/a |
| C3 | 3 | a fleet-wide migration is unsupported | none | n/a |
| C3 | 4 | the first step is measurement | none | n/a |
| C4 | 1 | Arm 1 vCPU/2 GB costs $0.0000109722/s | none | n/a |
| C4 | 2 | Graviton cuts cost 20.0% | none | n/a |
| C4 | 3 | Spot cuts up to a further 70% | none | n/a |
| C4 | 4 | both are config changes where the preconditions hold | A7, A8 (already in table) | n/a |
| C5 | 1 | new environment per uncovered concurrent request | none | n/a |
| C5 | 2 | [2nd] first request on a new environment is a cold start | none | n/a |
| C5 | 3 | [2nd] throttling above 1,000 concurrent by default | none | n/a |
| C5 | 4 | [3rd] provisioned concurrency incurs additional charges | none | n/a |
| C5 | 5 | [3rd] the threshold can only fall | none | n/a |
| C6 | 1 | Lambda candidates must fall below a threshold that migration costs push lower | none | n/a |
| C6 | 2 | Fargate levers need no per-service measurement | A11 surfaced | yes |
| C6 | 3 | rightsizing cuts the bill in proportion | A12 surfaced | yes |
| C6 | 4 | fastest cut: config levers now, Lambda only under threshold | none | n/a |

## Adversarial pass (process output)

**Premise:** It is March 2027. This plan has failed: the AWS bill barely moved, and a Lambda-migrated service had to be rolled back.

**Causes** (unfiltered, from four viewpoints):
- *Finance (pays for it):* Container compute turned out to be a small slice of the bill. Data transfer, NAT gateways and databases dominated, and nobody touched them.
- *Finance:* The Lambda migration used up the quarter, so the savings arrived late.
- *Platform engineer (implements it):* Busy fraction was measured from CPU utilisation. Lambda bills wall-clock time including I/O wait, so the migrated service cost more than predicted.
- *Platform engineer:* Concurrency per container (k) was assumed to be 1. It was actually 8, so a migrated API cost roughly 17× more.
- *Platform engineer:* A native dependency would not build for arm64, so the Graviton switch stalled for half the fleet.
- *On-call SRE (lives with it):* A stateful service put on Spot was interrupted mid-transaction.
- *On-call SRE:* Cold starts on a migrated service breached its latency target. Provisioned concurrency was bought to fix that, and the saving disappeared.
- *On-call SRE:* A traffic spike hit the regional limit of 1,000 concurrent Lambda executions, and unrelated functions were throttled.
- *Leadership:* The plan was overridden with "migrate everything anyway", because everyone knows serverless is cheaper.

**Clusters:**
- **K1: Optimised the wrong line item.** Causes: bill composition, override by conviction. Bears on C3 and GT-9?.
- **K2: Break-even inputs mis-measured.** Causes: CPU-based busy fraction, wrong k. Bears on C2 and GT-8?.
- **K3: Operational fallout of the cost levers.** Causes: arm64 build failure, Spot interruption, cold starts and provisioned concurrency, concurrency throttling. Bears on C4, C5, GT-7, GT-11 and GT-12.
- **K4: Schedule.** Causes: migration used up the quarter. Bears on C6 and A11.

**Disposition:**
- **K1: plan change.** Step 1 is a Cost Explorer breakdown by service and usage type. Compute work starts only on the line items that are actually largest. This is caveated in C3 and C6.
- **K2: plan change.** Measure busy fraction as requests/s × mean wall-clock latency ÷ provisioned vCPU, taken from load balancer or APM data, not from CPU utilisation. Pilot one candidate on Lambda for a full billing cycle before any wider decision. This is the named weak link in C3.
- **K3: accepted risk, with named mitigations.**
  - Add an arm64 CI build-and-test gate before any Graviton switch.
  - Use Spot only for stateless tasks, with an on-demand base capacity.
  - A Lambda candidate must pass its latency target in the pilot, cold starts included.
  - Request a concurrency quota increase before cutover.
  - These are written into the conditions of C4 and the extension in C5.
- **K4: plan change.** Configuration levers first, then migration only for candidates that pass the threshold. This is the ordering in C6.

## §6→§4 closure ledger (process output)

```text
- "Do not start a fleet-wide Lambda migration; measure, apply Graviton/Spot/rightsizing, migrate only services under threshold" → chain C6 ✓
- "Lambda ~2.10× per busy second and bills each concurrent request's I/O wait separately; wins only by not paying for idle" → chain C2 ✓
- "No service can be placed without measured busy fraction and k; saving capped by unmeasured compute share" → chain C3 ✓
- "Graviton needs arm64 images, Spot needs interruption tolerance; Lambda moves carry cold-start and quota exposure" → chain C4 ✓ (and C5)
- "Confidence MEDIUM" → chain C6 ✓
```

## Self-audit scan (process output)

| Chain | Chain Head (brief) | Form conforming? | Rule applied | Dependency clean? |
|---|---|---|---|---|
| C1 | GT-1 + GT-3 + GT-5 | yes | n/a | yes |
| C2 | C1 + GT-2 + GT-4 + GT-10 | yes | n/a | yes |
| C3 | GT-8? + GT-9? + C2 | yes | n/a | yes |
| C4 | GT-5 + GT-6 + GT-7 | yes | n/a | yes |
| C5 | C2 + GT-10 + GT-11 + GT-12 | yes | n/a | yes |
| C6 | C3 + C4 + C5 | yes | n/a | yes |

| §6 Span (brief) | Construct | Claim under R11? | R11 clause applied | Chain cited |
|---|---|---|---|---|
| Recommended approach: do not start fleet-wide migration… | bold lead-in | yes | prescribed lead-in, colon closes bold span | C6 |
| Key insight: Lambda ~2.10× per busy second… | bold lead-in | yes | prescribed lead-in, colon closes bold span | C2 |
| Why measurement comes first: … | bold lead-in | yes | bold lead-in whose colon closes the bold span | C3 |
| Trade-offs acknowledged: … | bold lead-in | yes | prescribed lead-in, colon closes bold span | C4, C5 |
| Confidence: MEDIUM … | bold lead-in | yes | bold lead-in whose colon closes the bold span | C6 |

```text
Scan complete: 6 chain rows, one per section-4 chain block in order; 5 section-6 rows, one per construct in order — 5 claims under R11, 0 excluded. 0 chains malformed, 0 claims untraced.
```

---

# First Principles Analysis: Cutting the AWS bill, and whether Lambda is the way

## 1. Problem Essence

**Core problem:** Which parts of your AWS spend can be cut soonest, and for which services, if any, would moving from containers to Lambda lower cost rather than raise it, given that "serverless is cheaper" has never been tested against your workload?

**Success criteria:**
- The Conclusion states whether Lambda is cheaper per unit of busy compute, and gives a numeric ratio.
- The Conclusion names the per-service test (a numeric threshold) that decides which services should move to Lambda.
- The Conclusion names at least one cost lever faster than migration, and states its size.
- The Conclusion names the measurements required before any migration decision.

## 2. Assumptions Table

| Assumption | Type | Treatment | Verdict | Verification |
|---|---|---|---|---|
| A1: Serverless is cheaper than containers | untested belief | Verify or flag | Discard — per busy second Lambda costs 2.10× Fargate (C1). It is cheaper only below a busy-fraction threshold (C2). | GT-1, GT-3, GT-5 read at source |
| A2: Container compute is the dominant share of the bill | untested belief | Verify or flag | Challenge — no bill data was supplied; carried as GT-9? | unverified — flagged |
| A3: Your services are idle most of the time | untested belief | Verify or flag | Challenge — no utilisation data was supplied; carried as GT-8? | unverified — flagged |
| A4: Migrating to Lambda is the fastest path to a lower bill | convention | Challenge before use | Discard — configuration levers exist that do not change how the application runs (C4) | GT-5, GT-6, GT-7 read at source |
| A5: The Lambda rate I read (page showed US East Ohio) equals the N. Virginia rate | untested belief | Verify or flag | Accept — the sensitivity is priced in C1. The conclusion holds unless the regional gap exceeds 2.10×. | unverified — flagged |
| A6: A container serves k concurrent I/O-bound requests on one vCPU | untested belief | Verify or flag | Challenge — k is carried as a variable in C2, not assumed | unverified — flagged |
| A7: Your container images build and run on arm64 | untested belief | Verify or flag | Challenge — stated as a condition in C4's conclusion | unverified — flagged |
| A8: Some tasks tolerate interruption | untested belief | Verify or flag | Challenge — stated as a condition in C4's conclusion | unverified — flagged |
| A9: Compute Savings Plans discount Lambda | untested belief | Verify or flag | Discard — the Lambda pricing page was opened and this statement was not found (Phase 3 failure record). Not used. | citation does not support the claim |
| A10: The 1,000 concurrent-execution limit per region applies | current constraint | Record expiry | Accept — lifts on a quota increase; a default, not a hard limit | GT-11 |
| A11: A configuration change ships sooner than moving a service onto Lambda | untested belief | Verify or flag | Accept — priced in C6: if false, the order changes but the threshold test does not | unverified — flagged |
| A12: Fargate bills configured vCPU and memory, not used | untested belief | Verify or flag | Accept — priced in C6: if false, rightsizing saves nothing and the other two levers stand | unverified — flagged |

## 3. Ground Truths

- **GT-1** Lambda (x86) duration costs $0.0000166667 per GB-second (first tier). Source: aws.amazon.com/lambda/pricing. Read-at-source: quoted "$0.0000166667 per GB-s". The page returned the US East (Ohio) region; see A5.
- **GT-2** Lambda requests cost $0.20 per million. Source: same page. Read-at-source: "$0.20 per one million requests".
- **GT-3** Lambda allocates CPU in proportion to memory: 1,769 MB equals one vCPU. Memory ranges from 128 to 10,240 MB. Source: docs.aws.amazon.com/lambda/latest/dg/configuration-memory.html. Read-at-source: first paragraph, "At 1,769 MB, a function has the equivalent of one vCPU".
- **GT-4** Lambda bills duration from when your code starts running until it returns, rounded up to 1 ms. Source: Lambda pricing page. Read-at-source: "Duration is calculated from the time your code begins executing until it returns or otherwise terminates, rounded up to the nearest 1ms."
- **GT-5** Fargate Linux/x86 in US East (N. Virginia) costs $0.000011244 per vCPU-second and $0.000001235 per GB-second. Source: aws.amazon.com/fargate/pricing. Read-at-source: Example 1, "CPU cost: $0.000011244 per vCPU second", "memory cost: $0.000001235 per GB per second".
- **GT-6** Fargate Linux/Arm in US East (N. Virginia) costs $0.0000089944 per vCPU-second and $0.0000009889 per GB-second. Source: same page. Read-at-source: Example 2, quoted.
- **GT-7** Fargate Spot runs interrupt-tolerant ECS tasks at up to 70% off the regular Fargate price. Source: same page. Read-at-source: "up to a 70% discount off the regular Fargate price".
- **GT-8?** Each service's busy fraction and its concurrency per container (k). Unverified: not supplied.
- **GT-9?** The share of your AWS bill that is container compute. Unverified: not supplied.
- **GT-10** Lambda creates a separate execution environment for each concurrent request. A busy environment cannot take other requests, and a new environment runs an Init phase first (a cold start). Source: docs.aws.amazon.com/lambda/latest/dg/lambda-concurrency.html. Read-at-source: "For each concurrent request, Lambda provisions a separate instance of your execution environment"; "this execution environment is busy and cannot process other requests"; "this is known as a cold start".
- **GT-11** The default account limit is 1,000 concurrent executions per region. Source: same page. Read-at-source: "a total concurrency limit of 1,000 concurrent executions across all functions in an AWS Region".
- **GT-12** Provisioned concurrency incurs additional charges. Source: same page. Read-at-source: "Using provisioned concurrency incurs additional charges to your account."

```text
?-marked: GT-8, GT-9 (2 of 12)
Read-at-source: GT-1, GT-2, GT-4 — Lambda pricing page, quoted; GT-3 — configuration-memory doc para 1; GT-5, GT-6, GT-7 — Fargate pricing Examples 1–2 and Spot paragraph; GT-10, GT-11, GT-12 — lambda-concurrency doc, quoted
Phase 3 failure record: A9 — Lambda pricing page opened; Savings Plans discount for Lambda not located — citation does not support the claim
```

A note on how the sources were read: the two AWS pricing pages came back through a web-fetch extraction that quoted the page wording. The two docs pages came back as raw text. As a cross-check, $0.000011244/s × 3600 = $0.04048 per vCPU-hour, which matches the published hourly figure.

## 4. Derivation Chains

### Conclusion C1: Per second of busy compute, Lambda costs about 2.10× Fargate, so "serverless is cheaper" is false as a price claim

```text
GT-1 (Lambda $/GB-s) + GT-3 (1,769 MB = 1 vCPU) + GT-5 (Fargate x86 $/vCPU-s and $/GB-s)
→ one Lambda vCPU-equivalent costs 1.7275 GB × $0.0000166667 = $0.000028792 per second
→ a Fargate x86 task with 1 vCPU and 2 GB costs $0.000011244 + 2 × $0.000001235 = $0.000013714 per second
→ Lambda costs 2.10× Fargate per busy second while giving about 14% less memory [Assumes: A5]
→ Lambda can only come out cheaper by not paying for idle time, never on unit price
```

**Confidence:** HIGH. Every input was read at source, and the arithmetic reproduces when redone. A5 is priced: if the Ohio-labelled rate differed from N. Virginia's, the ratio would shift in proportion, and the conclusion fails only if the regional gap exceeded 2.10×. The rival conclusion ("Lambda is cheaper because you pay per use") is not a unit-price claim; it is handled in C2 and in §5.

### Conclusion C2: Lambda beats an always-on container only when the service's busy fraction is below about 1/(2.10 × k)

```text
C1 (2.10× per busy second) + GT-2 ($0.20 per 1M requests) + GT-4 (billed wall-clock to 1 ms) + GT-10 (one request per environment)
→ Lambda bills every in-flight request's full wall-clock time, including time spent waiting on I/O
→ a container serving k concurrent requests on one vCPU pays once for time Lambda bills k times [Assumes: A6]
→ Lambda's effective premium over a busy container is therefore 2.10 × k
→ the request fee adds about 7% to a 100 ms invocation at one vCPU-equivalent, lowering the threshold slightly
→ Lambda wins only when busy fraction, meaning Lambda-billable seconds per task-second, is under about 1/(2.10 × k)
→ that threshold is about 48% at k = 1 and about 10% at k = 5
```

**Confidence:** HIGH. C1 is HIGH, and GT-2, GT-4 and GT-10 were read at source. A6 is priced: k is a variable, so if containers do not overlap requests (k = 1) the formula still holds, with the threshold at 48%. Request fee arithmetic: $0.0000002 / (0.1 s × $0.000028792/s) = 6.9%.

### Conclusion C3: No service can be assigned to Lambda or containers until its busy fraction, its k and the bill's compute share are measured

```text
GT-8? (busy fraction and k unmeasured) + GT-9? (bill composition unmeasured) + C2 (threshold 1/(2.10 × k))
→ no service can be placed on either side of the threshold without its measured busy fraction and k
→ even a perfect compute saving is capped at the compute share of the bill, which is unmeasured
→ a fleet-wide Lambda migration is supported by nothing established in this analysis
→ the first step is measurement: bill by service, then request rate × latency against provisioned vCPU per service
```

**Confidence:** MEDIUM. The weakness is in the inputs: GT-8? and GT-9? are unmeasured.
- **To remove GT-9?:** pull three months of Cost Explorer grouped by SERVICE and USAGE_TYPE.
- **To remove GT-8?:** for each service, compute (requests/s × mean wall-clock latency) ÷ provisioned vCPU, from load balancer or APM metrics.
- **Weakest link:** the second hop, if the bill turns out to be dominated by non-compute items.

### Conclusion C4: Graviton (20.0%) and Fargate Spot (up to 70%) cut container cost without changing how the application runs, where their preconditions hold

```text
GT-5 (Fargate x86 rates) + GT-6 (Fargate Arm rates) + GT-7 (Spot up to 70% off)
→ an Arm task with 1 vCPU and 2 GB costs $0.0000109722 per second against $0.000013714 on x86
→ Graviton therefore cuts Fargate compute cost by 20.0% at identical task size
→ Spot removes up to a further 70% for interrupt-tolerant ECS tasks
→ where images build for arm64 and tasks tolerate interruption, both are configuration changes with no rewrite [Assumes: A7, A8]
```

**Confidence:** HIGH. All inputs were read at source, and the arithmetic reproduces (0.80007). A7 and A8 are written into the conclusion as conditions, so if either fails, the conclusion applies to fewer services but is not false. The rival, "migration is the bigger or faster saving", is ruled out in §5 (Dead End 1). Spot's 70% is a ceiling, not a guaranteed figure.

### Conclusion C5: Moving a service to Lambda adds cold-start and throttling exposure, and fixing cold starts only lowers the break-even point

```text
C2 (threshold 1/(2.10 × k)) + GT-10 (environment per request, cold start) + GT-11 (1,000 default concurrency) + GT-12 (provisioned concurrency billed)
→ a service on Lambda creates a new execution environment for each concurrent request no warm one can take
→[2nd] each new environment serves its first request after an Init phase, which is a cold start
→[2nd] requests beyond 1,000 concurrent executions per region are throttled under the default quota
→[3rd] provisioned concurrency removes cold starts but incurs additional charges
→[3rd] any such charge adds to Lambda's side of the comparison, so the busy-fraction threshold can only fall
```

**Confidence:** HIGH. C2 is HIGH, and GT-10, GT-11 and GT-12 were read at source. Each hop is either quoted behaviour or the step "a positive added cost lowers the break-even point". None of these effects contradicts a ground truth, so the analysis did not need to go back to re-challenge assumptions.

### Conclusion C6: The fastest bill cut is Graviton, Spot and rightsizing now, then Lambda only for services measured under the threshold

```text
C3 (measure first) + C4 (Graviton 20.0%, Spot up to 70%) + C5 (threshold only falls)
→ the only services that belong on Lambda are those measured under a threshold that migration costs push lower
→ the Fargate levers apply to every compatible service without waiting on per-service measurement [Assumes: A11]
→ rightsizing each task to its measured vCPU use cuts the per-second bill in proportion [Assumes: A12]
→ the fastest bill cut is Graviton, Spot and rightsizing now, then Lambda only for services measured under threshold
```

**Confidence:** MEDIUM. The weakness is in the inputs: C3 is MEDIUM, because GT-8? and GT-9? are unmeasured; C3's confidence line gives the verification path. A11 is priced: if moving a service to Lambda shipped as fast as a config change, the order would change but not the test for which services move. A12 is priced: if Fargate billed used rather than configured vCPU, rightsizing would save nothing and Graviton and Spot would still stand. The weak link from the stress test (K1) is that if the bill is dominated by non-compute items, every lever in this chain is small.

## 5. Abandoned Reasoning

### Dead End 1: "Migrate everything to Lambda" as the fastest path

**What was tried:** Taking the stated premise at face value and planning a fleet-wide migration.

**Why abandoned:** The premise is contradicted by ground truth. Lambda is 2.10× more expensive per busy second (C1). It wins only below a busy-fraction threshold that is unmeasured for your services (C2, C3). Levers exist that don't change how your code runs (C4).

**What it ruled out:** Any migration plan that does not first measure each service against the threshold.

### Dead End 2: A weighted trade-off matrix (Lambda vs Fargate vs EC2)

**What was tried:** Scoring the options against weighted criteria.

**Why abandoned:** The decision comes down to one measurable quantity per service: busy fraction relative to 1/(2.10 × k). Scoring that against weights would dress an unmeasured number up as false precision.

**What it ruled out:** Picking one option for the whole fleet. The answer is decided service by service.

### Dead End 3: Lambda on Arm, and Savings Plans

**What was tried:** Comparing Lambda's Arm pricing, and applying Savings Plans discounts.

**Why abandoned:** The Lambda Arm rate did not render on the pricing page. The Savings Plans statement was not found when I read the page (A9, Phase 3 failure record). Neither can serve as a ground truth.

**What it ruled out:** Nothing about the conclusion. It is an open lever worth checking separately: a Savings Plan commitment is another configuration-level cut.

## 6. Conclusion

**Recommended approach:** Don't start a fleet-wide Lambda migration. First pull the bill by service. Then move compatible Fargate tasks to Graviton, put interrupt-tolerant ones on Spot, and rightsize every task. Move a service to Lambda only once its measured busy fraction is below about 1/(2.10 × k) (chain C6).

**Key insight:** Per second of busy compute, Lambda costs about 2.10× Fargate. It also bills each concurrent request's I/O wait separately, where a container overlaps those waits. So Lambda saves money only by not paying for idle time. A service must be busy less than about 48% of the time (with one request per container), or less than about 10% (with five concurrent requests per container), before Lambda wins (chain C2).

**Why measurement comes first:** No service can be placed on either side of that threshold without its measured busy fraction and k, and the whole saving is capped by a compute share of the bill that nobody has measured yet (chain C3).

**Trade-offs acknowledged:** Graviton requires images that build for arm64, and Spot requires tasks that tolerate interruption. Neither is verified for your fleet (chain C4). Services that do move to Lambda take on cold starts and the 1,000-execution default limit, and buying provisioned concurrency to fix cold starts pushes the threshold lower (chain C5).

**Confidence:** MEDIUM. C3 and C6 are rated MEDIUM because GT-8? (per-service busy fraction and k) and GT-9? (bill composition) are unmeasured. Measuring them as C3 describes would raise this conclusion to HIGH (chain C6).

---

## Self-Audit Gate (process output)

The Assumption Audit scan covers all 27 chain steps across C1–C6, in order. The self-audit scan has 6 chain rows and 5 construct rows, and its reconciliation line recounts against the text.

**Criterion 1: Identify Essence**
Quoted span: "Which parts of your AWS spend can be cut soonest, and for which services, if any, would moving from containers to Lambda lower cost rather than raise it"
Band: **Rigorous**
Justification: It is a single sentence naming the underlying decision rather than restating the prompt, and each of the four success criteria is a pass/fail property that can be checked by scanning §6 (ratio, threshold, faster lever with size, required measurements).

**Criterion 2: Challenge Assumptions**
Quoted span: "| C6 | 2 | Fargate levers need no per-service measurement | A11 surfaced | yes |"
Band: **Rigorous**
Justification: Every row uses the four-type scheme and a verdict token followed by a justification. A1, A4 and A9 are discarded with evidence, every unverified assumption used in a chain reads "unverified — flagged", and the audit covers all 27 steps and added A11 and A12.

**Criterion 3: Establish Ground Truths**
Quoted span: enumerated GT-8, GT-9; the list carries `?` on exactly those two. Each of the other ten names a read location and feeds C1, C2, C4 or C5, all rated HIGH.
Band: **Rigorous**
Justification: The enumeration matches the list, every unsuffixed ground truth feeding a HIGH chain names where it was read, the Phase 3 failure record for A9 is present, and no discarded assumption appears in the list.

**Criterion 4: Reason Upward**
Quoted span: "| C1 | GT-1 + GT-3 + GT-5 | yes | n/a | yes |" through "| C6 | C3 + C4 + C5 | yes | n/a | yes |"
Band: **Rigorous**
Justification: All six chains conform to the arrow format and have clean dependencies. §5 records three dead ends in the What-was-tried / Why-abandoned / What-it-ruled-out structure, no analogy is used as evidence, and every step introducing an assumption carries an `[Assumes:]` tag.

**Criterion 5: Validate**
Quoted span: "**Confidence:** MEDIUM. C3 and C6 are rated MEDIUM because GT-8? (per-service busy fraction and k) and GT-9? (bill composition) are unmeasured."
Band: **Rigorous**
Justification: The bands are calibrated on the three axes (C1, C2, C4 and C5 HIGH; C3 MEDIUM on inputs; C6 capped by C3), and each MEDIUM line names its `?` inputs or cited chain with a verification path. The pre-mortem record has a past-tense premise, causes from four viewpoints, clusters citing chain and ground-truth IDs, and a disposition for each cluster.

**Criterion 6: Conclusion-to-Ground-Truth Traceability**
Quoted span: "| Key insight: Lambda ~2.10× per busy second… | bold lead-in | yes | prescribed lead-in, colon closes bold span | C2 |"
Band: **Rigorous**
Justification: All five §6 claims cite a chain and none is untraced. The Key Insight (Lambda's premium is 2.10 × k, so it wins only on idle time) is a finding that reasoning by analogy doesn't reach, not a restatement of the recommendation.

Gate cleared: no criterion scored Absent and none scored Hand-wavy, so no fix pass or re-entry was needed.

---

**Sources read:**
- https://aws.amazon.com/lambda/pricing/
- https://aws.amazon.com/fargate/pricing/
- https://docs.aws.amazon.com/lambda/latest/dg/configuration-memory.html
- https://docs.aws.amazon.com/lambda/latest/dg/lambda-concurrency.html

**Method files used:**
- /home/chrisdavidson/Projects/first-principles-skill/first-principles/agents/references/output-template.md
- /home/chrisdavidson/Projects/first-principles-skill/first-principles/agents/references/validation-rubric.md
- /home/chrisdavidson/Projects/first-principles-skill/first-principles/agents/references/pre-mortem.md

The claude.ai Gmail, Google Calendar and Google Drive connectors need authorising in your claude.ai connector settings. They can't be used until that's done. Nothing in this analysis depended on them.