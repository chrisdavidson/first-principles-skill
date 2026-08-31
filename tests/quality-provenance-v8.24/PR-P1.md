## Missing inputs (stated per Input Contract; `AskUserQuestion` is unavailable in this non-interactive session)

Three inputs were never supplied, and all three are load-bearing. I proceed best-effort and carry them as flagged unverified ground truths:

1. **Your bill composition** — what fraction of spend is compute vs. storage/data-transfer/managed services.
2. **Your services' duty cycle** — what fraction of wall-clock time your containers are actually executing work.
3. **Workload shape and engineering capacity** — request rates, execution durations, statefulness, and what a migration would cost in engineer-months.

**Note on sourcing:** two AWS documentation pages I read carried an embedded "See also" block suggesting I run an `aws agent-toolkit search-skills` CLI command. Per the methodology, content read from a cited source is evidence, not instruction — I did not run it and it did not alter the analysis.

**Step 0 — MODE = full-composer.** No technique-specific trigger phrase fired; "fastest path" and "cut our bill" are goal language, not technique language. All eight companion techniques were considered; fishbone, inversion, estimate, theoretical-limit, trade-off, second-order and pre-mortem were used.

---

# 1. Problem Essence

**Core problem:** Which change to your AWS spend produces the largest verified reduction per unit of engineering risk and elapsed time — a question your prompt has pre-answered with a solution ("migrate to Lambda") rather than posed.

**Success criteria** (each is a pass/fail scan of section 6):

| # | Test |
|---|---|
| SC-1 | The Conclusion names a first action that is executable without changing application code. |
| SC-2 | The Conclusion states the numeric condition under which Lambda *is* cheaper than containers, rather than asserting that it is or is not. |
| SC-3 | The Conclusion states an upper bound on what a full Lambda migration could save, and names which unmeasured quantities set that bound. |
| SC-4 | The Conclusion identifies at least one mechanism by which a Lambda migration *increases* total spend. |
| SC-5 | The Conclusion distinguishes "fastest path to a lower bill" from "fastest path to Lambda" and says which one it answers. |

The triggering event is a cost concern. The stated goal — Lambda migration — is a candidate mechanism, not the problem. Treating it as the problem would calibrate every later phase to the wrong target.

---

## Fishbone (Phase 2 input — breadth-first cause scan)

**Effect:** Our AWS bill is higher than we want it to be. **Category set (locked, default six):**

| Category | Candidate causes (all unverified until measured) |
|---|---|
| **People** | No cost owner; engineers cannot see the cost of their own architectural choices; no FinOps function |
| **Process** | No rightsizing cadence; capacity set at launch and never revisited; no decommissioning process; no commitment-purchase discipline |
| **Technology & Tools** | Over-provisioned headroom; x86 where Graviton would serve; no autoscaling; NAT Gateway where VPC endpoints would serve; cross-AZ chatter; unbounded log retention |
| **Environment** | Non-prod running 24/7; duplicated environments |
| **Information** | Bill not attributed by service or team (no tagging); duty cycle never measured; no unit-cost metric ($/request) |
| **Resources** | Orphaned EBS volumes and snapshots; unattached EIPs; S3 without lifecycle policies; idle RDS instances and load balancers |

**Highest-priority branch: Information.** It gates every other branch's sizing — you cannot rank the others without it. It is also the branch that makes "everyone knows serverless is cheaper" feel like an answer: absent attribution, a plausible-sounding mechanism substitutes for a measured cause.

## Inversion (Phase 2 input)

**Claim:** Migrating our services to Lambda will cut our AWS bill.
**Inverted:** Migrating our services to Lambda will not cut our AWS bill.

Failure-guaranteeing conditions → the precondition the original claim silently depends on:

| Would guarantee failure | Silent precondition |
|---|---|
| Compute is a minority of the bill | Compute is a material share |
| Services run above the cost crossover duty cycle | Aggregate duty cycle sits below crossover |
| Migration adds a per-request front door costlier than the compute saved | No costlier front door is introduced |
| Services exceed Lambda's execution envelope | Workloads fit the envelope |
| The same discount instrument was already available on the current platform | Current platform is not already discountable |
| Migration engineering cost exceeds the annual saving | Engineering capacity is effectively free |

All six preconditions are untested beliefs. That is six load-bearing dependencies under a claim presented as settled fact.

---

# 2. Assumptions Table

| Assumption | Type | Treatment | Verdict | Verification |
|---|---|---|---|---|
| A1. "Serverless is cheaper than containers" | convention | Challenge before use | **Discard** — contradicted by GT-1+GT-2+GT-3; the relation is conditional on duty cycle, and inverts above ~47.6% | Computed from read-at-source rates; see C1 |
| A2. The problem is "how to migrate to Lambda" | convention | Challenge before use | **Discard** — a mechanism stated as a goal; the goal is bill reduction, and Lambda is one of at least five mechanisms | Trade-off matrix, C5 |
| A3. "Fastest path" means fastest migration | convention | Challenge before use | **Discard** — fastest path to a *lower bill* is a commitment purchase (hours), not a migration (quarters) | GT-4, GT-7; C2 |
| A4. Unit-price arithmetic is deterministic | physical law | Accept as ground-truth candidate | **Accept** — arithmetic over published rates | Mathematical necessity |
| A5. us-east-1 rates apply to your region | current constraint | Record expiry conditions | **Challenge** — expires if you run outside us-east-1; per-region rates differ, and AWS revises them | AWS pricing pages are region-scoped |
| A6. A Savings Plan is a $/hour commitment over a fixed term | current constraint | Record expiry conditions | **Accept** — expires at term end (1 or 3 years) | GT-7, read-at-source |
| A7. Compute is a material share of your bill | untested belief | Verify or flag | **Challenge** — unverified; drives C4's bound | unverified — flagged (GT-8?) |
| A8. Aggregate duty cycle sits below the crossover | untested belief | Verify or flag | **Challenge** — unverified; the single most decisive unknown | unverified — flagged (GT-9?) |
| A9. No costlier front door is introduced | untested belief | Verify or flag | **Challenge** — falsified for API Gateway REST at any nontrivial request rate | GT-1 + GT-5; C3 |
| A10. Workloads fit Lambda's execution envelope | untested belief | Verify or flag | **Challenge** — envelope is hard-bounded; fit is per-service and unmeasured | GT-6 read-at-source; fit unverified (GT-10?) |
| A11. Current platform is not already discountable | untested belief | Verify or flag | **Discard** — false; Compute Savings Plans cover EC2, Fargate *and* Lambda | GT-4, read-at-source |
| A12. Migration engineering cost is immaterial | untested belief | Verify or flag | **Challenge** — unverified; a re-architecture, not a lift-and-shift | unverified — flagged (GT-10?) |
| A13. Bill is attributed well enough to rank levers | untested belief | Verify or flag | **Challenge** — the fishbone's highest-priority branch; likely absent | unverified — flagged (GT-8?) |
| A14. Provisioned container capacity must exceed peak demand | current constraint | Record expiry conditions | **Accept** — expires with autoscaling responsive enough to track demand at second granularity | Structural to any pre-provisioned platform |
| A15. Fargate task memory floor is 2 GB per vCPU | current constraint | Record expiry conditions | **Challenge** — used in C1's comparator; AWS may revise task-size combinations | unverified — flagged (GT-10?) |
| A16. Free-tier allowances are immaterial at your scale | untested belief | Verify or flag | **Challenge** — 1M requests + 400,000 GB-s/month is material only below roughly 0.15 vCPU-equivalent of continuous load | GT-1, read-at-source |

*(A14, A15, A16 were surfaced by the end-of-Phase-4 Assumption Audit and added here.)*

---

# 3. Ground Truths

- **GT-1** AWS Lambda x86 on-demand, us-east-1: **$0.0000166667 per GB-second** and **$0.20 per one million requests**; free tier "one million requests and 400,000 GB-seconds per month" — source: aws.amazon.com/lambda/pricing/; read-at-source: x86 on-demand pricing table, figures quoted verbatim. *Provenance: read-at-source.*
- **GT-2** "Lambda allocates CPU power in proportion to the amount of memory configured… **At 1,769 MB, a function has the equivalent of one vCPU** (one vCPU-second of credits per second)." Memory configurable 128 MB–10,240 MB. Docs note: "MB (rather than MiB) to refer to 1,024 KB." — source: AWS Lambda Developer Guide, `configuration-memory.html`; read-at-source: opening paragraph, quoted verbatim. *Provenance: read-at-source.*
- **GT-3** AWS Fargate (ECS, Linux) us-east-1 on-demand: **x86 $0.040478 per vCPU-hour and $0.004446 per GB-hour**; **ARM/Graviton2 $0.032380 per vCPU-hour and $0.003560 per GB-hour**; "Fargate Spot allows customers to run interrupt-tolerant Amazon ECS Tasks on spare capacity at up to a 70% discount off the regular Fargate price." — source: aws.amazon.com/fargate/pricing/; read-at-source: Linux/x86 and Linux/ARM per-second rate tables plus the Spot paragraph. *Provenance: read-at-source.*
- **GT-4** Compute Savings Plans "apply to EC2 instance usage regardless of instance family, size, AZ, Region, OS or tenancy, **and also apply to Fargate or Lambda usage**", at discounts "up to 66%" — source: aws.amazon.com/savingsplans/compute-pricing/; read-at-source: coverage sentence quoted verbatim. *Provenance: read-at-source.*
- **GT-5** Amazon API Gateway, us-east-1: **REST APIs $3.50 per million** API calls; **HTTP APIs $1.00 per million** for the first 300 million requests monthly, $0.90/million thereafter; data transfer $0.09/GB — source: aws.amazon.com/api-gateway/pricing/; read-at-source: REST and HTTP API first-tier rate rows. *Provenance: read-at-source.*
- **GT-6** Lambda hard quotas: **function timeout 900 seconds (15 minutes)**; memory 128 MB–10,240 MB; **invocation payload 6 MB request and 6 MB response (synchronous), 1 MB (asynchronous)**; default concurrent executions 1,000. "Lambda is designed for short-lived compute tasks that do not retain or rely upon state between invocations." — source: AWS Lambda Developer Guide, `gettingstarted-limits.html`; read-at-source: "Function configuration, deployment, and execution" quota table plus the intro paragraph. *Provenance: read-at-source.*
- **GT-7** A Savings Plan is "a commitment to a consistent amount of usage (measured in $/hour) **for a 1 or 3 year term**" — source: aws.amazon.com/savingsplans/pricing/; read-at-source: commitment definition, quoted verbatim. *Provenance: read-at-source.*
- **GT-8?** The composition of your AWS bill (compute share vs. storage, data transfer, managed services) — **unverified:** not supplied, and not derivable without Cost Explorer access to your account. *Provenance: unverified.*
- **GT-9?** The aggregate duty cycle of your services (fraction of wall-clock time spent executing work) — **unverified:** not supplied; requires CloudWatch CPU/request telemetry from your account. *Provenance: unverified.*
- **GT-10?** Per-service fit with Lambda's execution envelope, current Fargate task-size configuration, and the engineer-months a migration would consume — **unverified:** not supplied. *Provenance: unverified.*

**Provenance summary:**
```text
?-marked: GT-8, GT-9, GT-10 (3 of 10)
Read-at-source: GT-1 — Lambda pricing page, x86 on-demand table ($0.0000166667/GB-s; $0.20/1M)
                GT-2 — configuration-memory.html, opening paragraph ("At 1,769 MB… one vCPU")
                GT-3 — Fargate pricing page, Linux/x86 and Linux/ARM rate tables
                GT-4 — Compute Savings Plans page, coverage sentence ("…also apply to Fargate or Lambda usage")
                GT-5 — API Gateway pricing page, REST ($3.50/M) and HTTP ($1.00/M) first-tier rows
                GT-6 — gettingstarted-limits.html, function-configuration quota table (900 s; 6 MB)
                GT-7 — Savings Plans pricing page, commitment definition ("$/hour… 1 or 3 year term")
```

---

# 4. Derivation Chains

### Conclusion C1: Lambda's compute advantage is a duty-cycle function with a crossover at ~47.6%, not a general property — and it applies only inside Lambda's execution envelope

GT-1 (Lambda $0.0000166667/GB-s) + GT-2 (1,769 MB = 1 vCPU) + GT-3 (Fargate $0.040478/vCPU-hr, $0.004446/GB-hr) + GT-6 (900 s timeout; 6 MB sync payload; stateless design)
→ one Lambda vCPU-equivalent costs 1,769/1024 = 1.72754 GB × 3600 s × $0.0000166667 = **$0.10365 per hour of *busy* time**, whereas a Fargate task of 1 vCPU + 2 GB costs $0.040478 + 2×$0.004446 = **$0.04937 per hour of *wall-clock* time** *[Assumes: A15 — Fargate 2 GB memory floor per vCPU]*
→ Lambda's unit price per unit of actual work is **2.10× Fargate's**, but Lambda bills zero for idle while Fargate bills full rate for it *[Assumes: A14 — container capacity is provisioned to exceed peak]*
→ the two are equal at duty cycle D where 2.10·D = 1, i.e. **D = 47.6%**; below it Lambda is cheaper, above it Fargate is (crossover falls to **38.1%** against Fargate Graviton and **14.3%** against Fargate Spot, per GT-3; adding GT-1's $0.20/1M request charge shifts it to roughly 44.6% at 100 req/s)
→ and this crossover exists *at all* only for services inside Lambda's envelope: anything needing more than 900 seconds of execution, more than 10,240 MB, more than a 6 MB synchronous payload, or in-process state across requests has **no** crossover, because it cannot run on Lambda at any price

**Confidence: HIGH.** Every input is read-at-source; the derivation is arithmetic over published rates. Weakest link: A15 (Fargate's 2 GB-per-vCPU memory floor), which sets the comparator's memory term — but memory is only 18% of the Fargate figure, so a different task shape moves the crossover by a few points, not across the decision boundary.

### Conclusion C2: The commitment-discount lever is migration-independent, so it is available today at equal or greater value without touching code — but must be sized after cleanup, not before

GT-4 (Compute Savings Plans cover EC2, Fargate *and* Lambda, up to 66%) + GT-7 (commitment is a consistent $/hour for a 1- or 3-year term)
→ the discount instrument is identical on both sides of the proposed migration, so migrating cannot unlock a discount unavailable on the source platform — the two commonly-conflated savings ("we went serverless" and "we committed") are separable, and only the second requires no code change
→ therefore the largest single lever is purchasable in hours, with zero application risk, and remains fully available *after* any future Lambda migration
→[2nd] a purchased commitment locks a $/hour floor for 1–3 years, reducing architectural freedom — but **not** the freedom to adopt Lambda later, since GT-4 places Lambda inside the same coverage; this second-order effect contradicts no ground truth and does not route back to Phase 2
→[2nd] committing at a *pre-optimization* baseline commits you to paying for capacity you are about to rightsize away — the commitment is to spend, not to resources, so eliminated waste below the commitment line is billed anyway
→[3rd] therefore the correct sequence is measure → cleanup/rightsize → size the commitment to the *post-cleanup* baseline (or buy partial coverage now and top up), which changes the ordering of two actions that both look "fast"

**Confidence: HIGH.** Both inputs read-at-source; the second-order extension follows from GT-7's "$/hour" commitment structure rather than from an unverified input. Weakest link: the 66% figure is an "up to" ceiling — your realized discount depends on term and payment option, which does not affect the *direction* of the conclusion.

### Conclusion C3: For request-heavy synchronous services, the serverless front door can cost more than all the compute the migration saves

GT-1 ($0.20 per 1M Lambda requests) + GT-5 (API Gateway REST $3.50/M; HTTP API $1.00/M)
→ the standard synchronous Lambda entry point charges **17.5× more per request** than the Lambda invocation itself under REST APIs, and 5× more under HTTP APIs — a per-request cost that a container behind a load balancer does not incur per-request at all
→ at a worked example of 100 req/s (262.8M requests/month, 100 ms mean, 1 vCPU-equivalent), Lambda compute is 10 concurrent × 1.72754 GB × 2,628,000 s × $0.0000166667 = **$756.67**, plus **$52.56** of request charges = **$809 total**; the same traffic through API Gateway REST adds **$919.80** — a front door that exceeds the entire compute bill it fronts *[Assumes: A16 — free-tier allowances immaterial at this scale]*
→ therefore a service can sit comfortably *below* C1's duty-cycle crossover and still get more expensive after migration, because the crossover analysis prices compute and the migration also buys a per-request toll

**Confidence: HIGH.** Both rates read-at-source; the worked magnitudes are arithmetic. Weakest link: the comparison assumes API Gateway is the entry point — a Lambda function URL or an ALB target avoids this toll, which is precisely the design choice the analysis surfaces.

### Conclusion C4: The ceiling on what a full Lambda migration can save is fixed by two quantities you have not measured, and is negative above 47.6% duty cycle

GT-1 + GT-2 + GT-3 (yielding C1's 2.10× unit-price ratio)
→ if compute is share S of the total bill and aggregate duty cycle is D, then post-migration compute cost is 2.10·D times pre-migration compute cost, so the **maximum** total-bill reduction is bounded above by **S × (1 − 2.10·D)**
→ this bound is a ceiling, not an estimate: it credits the migration with perfect execution and charges it nothing for the API Gateway toll (C3), added CloudWatch Logs ingestion, NAT Gateway data-processing for VPC-attached functions, or a single engineer-hour
→ therefore the decision-relevant question is entirely determined by S and D — for illustration, S = 0.40 and D = 0.30 caps the saving at 0.40 × (1 − 0.63) = **14.8% of the bill**, while any D above 47.6% makes the bound **negative** *[illustrative values only — S and D are GT-8? and GT-9?, unmeasured]*
→ so a Lambda migration cannot be ranked against any other lever until S and D are measured, and measuring them takes days while the migration takes quarters

**Confidence: HIGH.** The bound itself derives only from read-at-source rates and arithmetic; GT-8? and GT-9? enter solely as the illustrative plug-in values, which are marked and are not the chain's conclusion. The conclusion — that the ceiling is a known function of two unmeasured numbers — is established without them. Weakest link: the bound assumes the migration does not change *which* work is done, only where it runs.

### Conclusion C5: Ranked against four alternatives, a full Lambda migration is the worst available lever; a commitment purchase is the best

**Trade-off matrix.** Criteria and weights locked before any scoring; all criteria phrased higher-is-better.

| Criterion | Wt | A: Compute Savings Plan | B: Rightsize + Graviton | C: Non-compute cleanup | D: Full Lambda migration | E: Selective Lambda (sub-crossover services only) |
|---|---|---|---|---|---|---|
| Expected bill reduction | 5 | 4 | 3 | 3 | 2 | 3 |
| Speed to realized saving | 5 | 5 | 4 | 5 | 1 | 3 |
| Low engineering effort | 4 | 5 | 4 | 4 | 1 | 3 |
| Reversibility / small blast radius | 4 | 2 | 5 | 5 | 1 | 3 |
| Certainty of the saving | 4 | 5 | 4 | 3 | 1 | 4 |
| Low ongoing operational burden | 3 | 5 | 4 | 4 | 3 | 3 |
| **Weighted total** | | **108** | **99** | **100** | **36** | **79** |

GT-4 + GT-7 (criterion facts for A) + GT-3 (Graviton is 20.0% cheaper than x86 Fargate at 1 vCPU + 2 GB: $0.03950 vs $0.04937, criterion fact for B) + GT-8? + GT-9? (certainty scoring for C and D)
→ weighted totals: **A = 108 > C = 100 > B = 99 > E = 79 > D = 36**, driven by the two weight-5 criteria (expected reduction and speed), on both of which the full migration scores at or near the floor
→ A and C fall within 7.4% of each other, a genuine near-tie; the criterion that would flip it is *certainty of the saving*, where C scores 3 only because GT-8? leaves the non-compute share unmeasured — were it measured and material, C rises to 108 and ties A exactly, resolved by the deterministic tiebreak (fewer unverified inputs among winning criteria) back to A
→ **recommend A**, with C run in parallel rather than sequenced behind it, and with C2's second-order finding governing the ordering: measure and clean up *before* sizing the commitment

**Confidence: MEDIUM.** GT-8? and GT-9? feed the certainty scores for options C and D. Raising this to HIGH requires one week of Cost Explorer grouping (by service and by tag) plus CloudWatch CPU-utilization and request-rate data per service — the same two measurements C4 identifies. Note the ranking's *direction* is robust to those inputs: A wins under both states of GT-8?, and D ranks last by a 63-point margin that no plausible re-scoring of the unverified criteria closes.

---

## End-of-Phase-4 Assumption Audit

| Chain | Step | Step text (brief) | Assumption surfaced? | Added to Table? |
|---|---|---|---|---|
| C1 | 1 | Compute per-hour unit costs from published rates | A15 — Fargate 2 GB/vCPU memory floor | yes |
| C1 | 2 | Lambda 2.10× unit price but zero idle billing | A14 — container capacity provisioned above peak | yes |
| C1 | 3 | Solve for equality → D = 47.6% | none | n/a |
| C1 | 4 | Crossover applies only inside Lambda's envelope | none | n/a |
| C2 | 1 | Discount instrument identical on both sides | none | n/a |
| C2 | 2 | Largest lever purchasable in hours, code-free | none | n/a |
| C2 | 3 [2nd] | Commitment does not foreclose later Lambda adoption | none | n/a |
| C2 | 4 [2nd] | Pre-cleanup commitment over-commits to eliminated waste | none | n/a |
| C2 | 5 [3rd] | Correct sequence is measure → cleanup → size commitment | none | n/a |
| C3 | 1 | Gateway charges 17.5× the invocation charge | none | n/a |
| C3 | 2 | Worked magnitudes at 100 req/s | A16 — free-tier allowances immaterial at scale | yes |
| C3 | 3 | Sub-crossover service can still get costlier | none | n/a |
| C4 | 1 | Bound is S × (1 − 2.10·D) | none (inherits A14, A15 via C1) | n/a |
| C4 | 2 | Bound is a ceiling, credits perfect execution | none | n/a |
| C4 | 3 | Illustrative plug-in; negative above 47.6% | none (GT-8?/GT-9? already tabled as A7/A8) | n/a |
| C4 | 4 | Cannot rank the migration until S and D measured | none | n/a |
| C5 | 1 | Weighted totals A=108 … D=36 | none | n/a |
| C5 | 2 | Near-tie sensitivity on certainty criterion | none | n/a |
| C5 | 3 | Recommend A, run C in parallel | none | n/a |

Three assumptions surfaced (A14, A15, A16); all three were added to the section-2 table. No chain step contradicts a ground truth, so the second-order pass routes nothing back to Phase 2.

---

## Pre-mortem (Phase 5 stress test)

*The plan has already failed — the bill did not go down. What caused it?* Causes clustered into three structural weaknesses:

| Cluster | Failure causes | Plan change or accepted risk |
|---|---|---|
| **Committed at the wrong baseline** | Savings Plan bought before cleanup; committed $/hour exceeds post-cleanup steady state; paying for waste you already removed | **Plan change:** buy partial coverage (~70% of current baseline) now, top up after cleanup measurement lands |
| **Measurement never happened** | "Measure S and D first" became indefinitely deferred; the Lambda question returns in six months with the same absent data | **Plan change:** time-box measurement to one week with a named owner; it is a Cost Explorer grouping plus a CloudWatch query, not a project |
| **Selective migration expanded** | Option E ("only sub-crossover services") drifted into option D as adjacent services got pulled in for consistency | **Accepted risk,** mitigated by a written entry gate: no service migrates without a measured D below 47.6% (38.1% if on Graviton) and a front-door cost check per C3 |

---

# 5. Abandoned Reasoning

### Dead End: Deriving a dollar-denominated savings target

**What was tried:** Producing a concrete "$X/month reduction" recommendation, which is what the question implicitly asks for.
**Why abandoned:** It requires GT-8? and GT-9?, both unverified. Every candidate figure would have been reverse-engineered from an assumed bill composition — a fabricated number wearing an arithmetic costume, and precisely the failure mode "everyone knows serverless is cheaper" already represents.
**What it ruled out:** Do not expect a dollar target from this analysis. C4 gives you the formula instead; plug in your own S and D and the target computes in under a minute.

### Dead End: Deriving a second crossover against EC2 with Savings Plans

**What was tried:** Computing a Lambda-vs-EC2 duty-cycle crossover in parallel with C1's Lambda-vs-Fargate one, since much container spend sits on EC2-backed ECS/EKS rather than Fargate.
**Why abandoned:** No EC2 on-demand rate was read at source in this analysis. Feeding an unread figure into a HIGH-confidence chain is exactly the defect the provenance discipline exists to catch, and the alternative — carrying it as `GT-N?` — would have made the crossover claim MEDIUM for no analytical gain.
**What it ruled out:** The EC2 crossover is *not* established here; do not extrapolate C1's 47.6% to EC2. It is, however, unnecessary: GT-4 establishes that Compute Savings Plans span EC2, Fargate and Lambda alike, which carries C2's conclusion without any EC2 rate at all. If you need the EC2 number, it is the same arithmetic with a read EC2 rate substituted for GT-3.

### Dead End: Treating "serverless is cheaper" as a current constraint rather than a convention

**What was tried:** Classifying A1 as a current constraint — a real limitation that holds now and could later lift — which would have let the analysis proceed from the premise as given and merely note its expiry conditions.
**Why abandoned:** It fails the classification test. A current constraint is a limitation that *obtains*; A1 is a belief about a price relation that is conditional on a variable (duty cycle) the belief does not mention. No source states it unconditionally, and GT-1 through GT-3 falsify it above 47.6%. Classifying it as a constraint would have smuggled a false premise past Phase 2 with an expiry note attached — a false premise labelled "temporarily true" is more dangerous than one labelled false, because it survives challenge.
**What it ruled out:** Any framing in which the migration is the default and the analysis merely schedules it.

---

# 6. Conclusion

**Recommended approach:** Do not start with Lambda. Start with two actions that require no application code change and land within days: **(1)** measure your bill composition and per-service duty cycle — one week, one owner, Cost Explorer grouped by service and tag plus CloudWatch CPU/request telemetry; **(2)** purchase Compute Savings Plan coverage, sized to your *post-cleanup* baseline rather than today's, running non-compute cleanup in parallel rather than behind it. The same commitment discount covers Lambda, so this forecloses nothing. Revisit Lambda afterward, per service, gated on measured duty cycle.

**Key insight:** Lambda's cost advantage is not that it is cheap — **it is 2.10× more expensive per unit of actual compute than Fargate.** Its advantage is that it bills nothing for idle. Those two facts define a crossover at 47.6% duty cycle, and reasoning by convention ("serverless is cheaper") reaches the wrong answer for every workload above it. Worse, the two things a migration is credited with — going serverless and getting a discount — are separable, and only one of them requires the migration.

**Trade-offs acknowledged:** A Savings Plan commits you to a $/hour floor for 1–3 years and is not reversible, which is why the second-order analysis moves cleanup *ahead* of sizing it — accept partial coverage now over full coverage at the wrong baseline. Choosing measurement first defers all savings by roughly one week. Ranking the full Lambda migration last does not rule out selective migration of genuinely bursty, low-duty-cycle, envelope-fitting services (option E, 79 points) — it rules out migration as a *bill-reduction strategy*, not as an architectural choice made on other merits.

**Confidence: MEDIUM.** The individual findings are HIGH — C1 (crossover), C2 (discount independence and sequencing), C3 (front-door inversion) and C4 (savings ceiling) rest entirely on read-at-source AWS rates and arithmetic. The lever *ranking* (C5) is MEDIUM because GT-8? (bill composition) and GT-9? (duty cycle) feed the certainty scores for the cleanup and migration options. One week of the measurement recommended above raises C5 to HIGH; the ranking's direction — commitment first, full migration last — is already robust to both unknowns.

**Success criteria check:** SC-1 ✓ (commitment purchase and measurement, both code-free) · SC-2 ✓ (47.6%; 38.1% Graviton; 14.3% Spot) · SC-3 ✓ (S × (1 − 2.10·D), bounded by GT-8?/GT-9?) · SC-4 ✓ (API Gateway front door, C3) · SC-5 ✓ (stated explicitly in the recommendation).

---

## §6→§4 closure ledger

```text
- "Do not start with Lambda; start with measurement + commitment purchase"     → chain C5 ✓
- "The same commitment discount covers Lambda, so this forecloses nothing"     → chain C2 ✓
- "Size the commitment to the post-cleanup baseline, cleanup in parallel"      → chain C2 ✓ (2nd/3rd-order extension)
- "Lambda is 2.10× more expensive per unit of actual compute than Fargate"     → chain C1 ✓
- "Crossover at 47.6% duty cycle (38.1% Graviton, 14.3% Spot)"                 → chain C1 ✓
- "Migration only applies to services inside Lambda's execution envelope"      → chain C1 ✓
- "Going serverless and getting a discount are separable"                      → chain C2 ✓
- "The front door can exceed the compute saving"                               → chain C3 ✓
- "Savings ceiling is S × (1 − 2.10·D), negative above 47.6%"                  → chain C4 ✓
- "Selective migration (option E) not ruled out on other merits"               → chain C5 ✓
```
All ten surviving claims carry a chain reference; nothing cut.

---

## Self-Audit Gate

*(Scores this analysis's own structure, not AWS or your architecture.)*

**Criterion 1: Identify Essence**
Quoted span: *"Which change to your AWS spend produces the largest verified reduction per unit of engineering risk and elapsed time — a question your prompt has pre-answered with a solution ("migrate to Lambda") rather than posed."*
Band: **Rigorous**
Justification: Names the core decision rather than the triggering event, explicitly separates the proposed mechanism from the goal, and each of SC-1 through SC-5 is a verb+subject+outcome test applied by scanning section 6 without interpretation.

**Criterion 2: Challenge Assumptions**
Quoted span: *"A11. Current platform is not already discountable | untested belief | Verify or flag | **Discard** — false; Compute Savings Plans cover EC2, Fargate *and* Lambda | GT-4, read-at-source"*
Band: **Rigorous**
Justification: All 16 rows draw Type from exactly the four-type scheme, Verdict cells lead with Accept/Challenge/Discard followed by an em-dash and specific justification, four assumptions are genuinely discarded rather than labelled, unverified rows read "unverified — flagged", and the Assumption Audit table covers all 19 chain steps in order with A14/A15/A16 fed back into this table.

**Criterion 3: Establish Ground Truths**
Quoted span: enumeration checked against the list — *"?-marked: GT-8, GT-9, GT-10 (3 of 10)"*; reading the Ground Truths list, the IDs actually carrying `?` are GT-8, GT-9, GT-10 — exactly those three, and the count of 3 matches the enumeration length.
Band: **Rigorous**
Justification: Every GT carries a stable ID referenced in section 4, a provenance label, and either a named read-at-source location or an explicit unverified reason; all seven unsuffixed GTs feed at least one HIGH-confidence chain (GT-1/2/3 → C1 and C4; GT-4/7 → C2; GT-5 → C3; GT-6 → C1); no Discarded assumption appears in the list.

**Criterion 4: Reason Upward**
Quoted span: *"GT-1 (Lambda $0.0000166667/GB-s) + GT-2 (1,769 MB = 1 vCPU) + GT-3 (Fargate $0.040478/vCPU-hr, $0.004446/GB-hr) + GT-6 (900 s timeout; 6 MB sync payload; stateless design) → one Lambda vCPU-equivalent costs … → Lambda's unit price per unit of actual work is 2.10× Fargate's …"*
Band: **Rigorous**
Justification: All five chains use arrow-led continuation form with no numbered-list hops, each carries at least one genuine intermediate not statable from any single GT, the trade-off matrix collapses into exactly one chain (C5) with a single named endpoint, second-order effects carry `[2nd]`/`[3rd]` marks in place on C2, `[Assumes: X]` marks appear on the three steps that introduced new assumptions, no analogy is used as evidence, and three dead ends are documented with the full What-was-tried / Why-abandoned / What-it-ruled-out structure.

**Criterion 5: Validate**
Quoted span: *"**Confidence: MEDIUM.** GT-8? and GT-9? feed the certainty scores for options C and D. Raising this to HIGH requires one week of Cost Explorer grouping (by service and by tag) plus CloudWatch CPU-utilization and request-rate data per service…"*
Band: **Sound**
Justification: Every chain names its weakest link and every `GT-N?` input is named in its chain's confidence line with the specific verification that would raise it — but one Conclusion-section claim (the lever ranking) rests only on C5 at MEDIUM, with neither EXCEPT clause claimed, which the descriptor bands Sound rather than Rigorous. The overall MEDIUM rating correctly matches the weakest contributing chain rather than overstating to HIGH.

**Criterion 6: Conclusion-to-Ground-Truth Traceability**
Quoted span: the closure ledger — *"All ten surviving claims carry a chain reference; nothing cut."*
Band: **Rigorous**
Justification: Every section 6 claim maps to a specific named chain, no new reasoning is introduced in the Conclusion, and the Key Insight ("Lambda is 2.10× more expensive per unit of actual compute; its advantage is that it bills nothing for idle") is a non-obvious inversion of the premise the question was built on rather than a restatement of the recommendation.

**Gate result: PASS** — no criterion Absent; exactly one at Hand-wavy-or-below (Criterion 5, Sound, which is above the cap). No re-perception pass was required, and no re-entry edge fired.