## Disclosures (read first)

**Missing inputs.** `AskUserQuestion` is not available in this runtime, so per the Input Contract I state what is missing and proceed best-effort. Four inputs would materially change this analysis and were not supplied: (1) your cost-and-usage report broken down by service, (2) per-service average CPU duty cycle, (3) per-service sustained request rate, (4) your existing committed-spend instruments and their remaining terms. Everything below that depends on those is marked `?` and confidence-capped accordingly.

**Re-entry edge fired (one, bounded).** The Phase 4 second-order pass produced an effect — provisioned concurrency bills continuously — that contradicted the premise underlying the low-duty-cycle advantage. Per the methodology this routed the conclusion back to **Phase 2 for re-challenging**. Result: assumption A-11 ("Lambda scales to zero, so idle costs nothing") was added and given a **Discard** verdict, and chain C6 was added to quantify the effect. No artifact was retired. This edge has now fired and will not fire again.

**Premise flagged.** Your prompt embeds "everyone knows serverless is cheaper than containers" as a given. That is a convention, not a ground truth, and Phase 2 challenges it rather than building on it. It does not survive.

---

## §6→§4 closure ledger (process output)

- "Measure before you migrate: rank the bill by service, then rank each service by duty cycle and request rate" → chain C9 ✓
- "Step 1 — pull the CUR and rank spend by service before touching any compute platform" → chain C9 ✓
- "Step 2 — apply the container-path levers that need no re-architecture" → chains C3, C4 ✓
- "Step 3 — adopt Lambda selectively, only for workloads measured below both thresholds" → chains C1, C2 ✓
- "Key insight: above roughly 69 requests per second per vCPU-equivalent, Lambda's per-request charge alone exceeds the entire price of the container it would replace" → chain C2 ✓
- "Trade-offs acknowledged: the case for Lambda is a duty-cycle case, and three separate forces narrow it" → chain C1 ✓
- "Latency-sensitive services are the worst Lambda candidates, not the best" → chain C6 ✓
- "A Compute Savings Plan is not an argument against migrating" → chain C4 ✓
- "Every lever applied to the container path narrows the band where Lambda wins" → chain C3 ✓
- "The premise you started from is false as stated" → chain C8 ✓
- "Overall confidence: HIGH on the platform economics, and the organisation-specific ranking is deliberately left open" → chains C1, C9 ✓

Ledger clean: 11 claims, 11 chains cited, 0 cut.

---

# First-Principles Analysis: Cutting the AWS Bill

## 1. Problem Essence

**Essence Statement:** Which change to our AWS spend produces the largest dollar reduction per unit of engineering effort and operational risk — a question about *where the money is and what moves it*, not about which compute platform we prefer?

Success criteria (each checkable by scanning section 6):

1. The Conclusion names a spend-ranking step that precedes any platform choice.
2. The Conclusion states a numeric threshold, derived from published unit prices, above which Lambda is more expensive than containers.
3. The Conclusion states a second numeric threshold based on request rate, independent of the first.
4. The Conclusion either affirms or refutes "serverless is cheaper than containers" as a general claim, and names the derivation that settles it.
5. No claim in the Conclusion rests on an analogy to what other companies did.

The trigger for this analysis was a desire to migrate to Lambda. The question the analysis must answer is not "how fast can we get to Lambda" — that presupposes the answer. Lambda is one candidate mechanism among several for one line item among many.

## 2. Assumptions Table

**Fishbone (breadth-first cause scan).** Effect: *our AWS bill is higher than we want it to be.* Default six-category set (no preset fits a cloud bill cleanly). Locked before brainstorming.

- **People** — no per-team cost ownership; instance sizes chosen by habit; nobody's objective is the bill.
- **Process** — no rightsizing cadence; non-production runs 24/7; no commitment-renewal review; tagging too sparse to attribute spend.
- **Technology and Tools** — oversized tasks; x86 where Graviton would serve; NAT Gateway data-processing charges on traffic that could use VPC endpoints; inter-AZ chatter; verbose CloudWatch log ingest; unattached EBS volumes and stale snapshots; no S3 lifecycle policy; over-provisioned managed databases.
- **Environment** — multi-AZ and multi-region duplication beyond the stated availability requirement; non-production at production parity.
- **Information** — the bill is read as a total rather than by line; no per-service unit cost exists.
- **Resources** — on-demand rates covering a steady baseline; or the wrong commitment instrument held.

Highest-priority branches for evidence gathering: **Information** (nothing else can be ranked until this is done), **Technology and Tools**, **Resources**. These are carried into the table below as `untested belief` rows.

**Inversion.** Claim: *migrating our services to Lambda will cut our AWS bill.* Inverted: *migrating our services to Lambda will not cut our AWS bill.* Conditions that would **guarantee** the inverted form: average CPU duty cycle above the break-even; sustained request rate above the request-charge ceiling; compute being a minority of the bill; latency targets forcing provisioned concurrency; executions exceeding Lambda's duration ceiling or holding long-lived connections; unexpired instance-scoped commitments; migration labour exceeding the annual saving; log-ingest and API-Gateway charges rising more than compute falls; VPC-attached functions still traversing the same NAT Gateway. Each necessary precondition below its failure condition enters the table as an `untested belief`.

| Assumption | Type | Treatment | Verdict | Verification |
|---|---|---|---|---|
| A-1 "Serverless is cheaper than containers" | convention | Challenge before use | **Discard** — refuted by two independent counterexample families (C1, C2); true only below both thresholds | Derived from GT-1, GT-2, GT-3, GT-5, GT-6 (all read-at-source) |
| A-2 Compute is the dominant share of our bill | untested belief | Verify, or flag as unverified | **Challenge** — not supplied; bounds the entire migration's ceiling | unverified — flagged (GT-12?) |
| A-3 Non-compute lines are invariant under a compute-platform change | untested belief | Verify, or flag as unverified | **Challenge** — true of NAT, inter-AZ transfer and storage; false of log ingest and API Gateway, which typically *rise* | unverified — flagged |
| A-4 Our services fit Lambda's execution-duration ceiling | untested belief | Verify, or flag as unverified | **Challenge** — any batch or long-poll service likely fails | unverified — flagged; no read attempted (feeds no chain) |
| A-5 "Fastest path" is the right optimisation target | convention | Challenge before use | **Discard** — speed to a platform is not speed to a saving; the target is dollars per engineering-week | Derived from the Essence Statement's success criteria |
| A-6 Current container tasks are right-sized | untested belief | Verify, or flag as unverified | **Challenge** — if false, the container-path option saves more than scored | unverified — flagged; AWS Compute Optimizer would settle it |
| A-7 We hold no committed-spend instruments | untested belief | Verify, or flag as unverified | **Challenge** — determines whether C5 applies at all | unverified — flagged (GT-13?) |
| A-8 Published on-demand prices are the applicable rates | current constraint | Record the expiry conditions | **Accept** — expires on any AWS price change, or on purchase of any Savings Plan | Read-at-source: GT-1, GT-2, GT-5, GT-7 |
| A-9 Lambda bills only executing time | current constraint | Record the expiry conditions | **Accept** — expires only if AWS changes its billing rule | Read-at-source: GT-4 ("rounded up to the nearest 1ms") |
| A-10 Unit identities (seconds↔hours, MB↔GB) | physical law | Accept as ground-truth candidate | **Accept** — definitional, cannot be negotiated | Definitional |
| A-11 Lambda scales to zero, so idle costs nothing | convention | Challenge before use | **Discard** — false whenever provisioned concurrency is enabled, which is exactly when latency matters (C6) | Read-at-source: GT-8 ("from the time you enable it on your function until it is disabled") — **added by the second-order re-entry** |
| A-12 Migration labour is a small one-off cost | untested belief | Verify, or flag as unverified | **Challenge** — dominates the first-year net for any multi-service migration | unverified — flagged; loaded engineering cost not supplied |
| A-13 Our existing commitments would be stranded by migration | convention | Challenge before use | **Discard** — refuted at source: Compute Savings Plans apply to Fargate *and* Lambda (GT-9) | Read-at-source: Savings Plans user guide |
| A-14 EC2 Instance Savings Plans and Standard RIs are instance-family-scoped | untested belief | Verify, or flag as unverified | **Challenge** — asserted from general knowledge, not read at source in this analysis | unverified — flagged; caps C5 at MEDIUM |
| A-15 Equal work is done per vCPU-second on Lambda and Fargate | untested belief | Verify, or flag as unverified | **Challenge** — surfaced by the Assumption Audit on C1 step 1; a per-service benchmark would settle it | unverified — flagged |
| A-16 The compared Fargate task is sized 1 vCPU / 2 GB | untested belief | Verify, or flag as unverified | **Accept** — a stated modelling choice, with sensitivity given: at 1 vCPU / 4 GB the task costs $0.0583/hr and the break-even rises to ~55% | Arithmetic from GT-5 |
| A-17 Our runtimes and dependencies have arm64 builds | untested belief | Verify, or flag as unverified | **Challenge** — surfaced by the Assumption Audit on C3 step 3 | unverified — flagged |
| A-18 Non-production environments run continuously | untested belief | Verify, or flag as unverified | **Challenge** — fishbone Process branch; a scheduled shutdown is the cheapest lever that exists if true | unverified — flagged |
| A-19 Log volume rises under Lambda | untested belief | Verify, or flag as unverified | **Challenge** — per-invocation log streams and cold-start noise push CloudWatch ingest up | unverified — flagged |
| A-20 Some services have latency targets requiring pre-warmed environments | untested belief | Verify, or flag as unverified | **Challenge** — if false for a given service, C6's 22% break-even does not apply to it | unverified — flagged |
| A-21 The locked trade-off weights reflect the organisation's actual priorities | untested belief | Verify, or flag as unverified | **Challenge** — weights were locked before scoring, but by this analysis rather than by you | unverified — flagged |

## 3. Ground Truths

**Verified (read-at-source).** Each entry names where the asserted figure was located.

1. **GT-1** — Lambda x86 on-demand duration is **$0.0000166667 per GB-second**, US East. *Provenance: read-at-source* — `aws.amazon.com/lambda/pricing/`, "Lambda Functions Pricing" section: "The monthly compute price is $0.0000166667 per GB-s".
2. **GT-2** — Lambda charges **$0.20 per 1 million requests**. *Provenance: read-at-source* — same page, requests pricing.
3. **GT-3** — **At 1,769 MB a Lambda function has the equivalent of one vCPU.** *Provenance: read-at-source* — `docs.aws.amazon.com/lambda/latest/dg/configuration-memory.html`: "At 1,769 MB, a function has the equivalent of one vCPU (one vCPU-second of credits per second)."
4. **GT-4** — Lambda duration is billed from execution start until return, **rounded up to 1 ms**; idle time is not billed. *Provenance: read-at-source* — pricing page: "Duration is calculated from the time your code begins executing until it returns or otherwise terminates, rounded up to the nearest 1ms."
5. **GT-5** — Fargate Linux/x86 costs **$0.000011244 per vCPU-second** and **$0.000001235 per GB-second**, US East. *Provenance: read-at-source* — `aws.amazon.com/fargate/pricing/`.
6. **GT-6** — Fargate is billed **from container image pull until task termination**, per second, 1-minute minimum — wall-clock, not busy time. *Provenance: read-at-source* — same page: "Duration is calculated from the time you start to download your container image (Docker pull) until the task terminates, rounded up to the nearest second."
7. **GT-7** — Fargate Linux/ARM costs **$0.0000089944 per vCPU-second** and **$0.0000009889 per GB-second**. *Provenance: read-at-source* — same page.
8. **GT-8** — Provisioned Concurrency costs **$0.0000041667 per GB-second** and is billed **from enable to disable**, rounded up to five minutes. *Provenance: read-at-source* — pricing page, Provisioned Concurrency section.
9. **GT-9** — Savings Plans commit to a specified amount of compute power measured per hour for a one- or three-year term; **Compute Savings Plans apply to EC2, Fargate and Lambda**. *Provenance: read-at-source* — `docs.aws.amazon.com/savingsplans/latest/userguide/what-is-savings-plans.html`: "This also applies to AWS Fargate and AWS Lambda usage."
10. **GT-10** — Lambda memory is configurable **128 MB to 10,240 MB in 1-MB increments**. *Provenance: read-at-source* — configuration-memory doc.
11. **GT-11** — This analysis was supplied **no bill composition, no per-service duty cycle and no request-rate data**. *Provenance: read-at-source* — the task prompt as received, which names only the goal ("cut our AWS bill") and a preferred mechanism ("migrating our services to Lambda").

**Unverified.**

12. **GT-12?** — The compute share of your AWS bill. *unverified* — not supplied; no source located.
13. **GT-13?** — Which committed-spend instruments you hold and their remaining terms. *unverified* — not supplied; no source located.

**`?`-marked: GT-12?, GT-13? (2 of 13).**

**Phase 3 failure record.** Source: `aws.amazon.com/lambda/pricing/`, opened twice. Reason: **citation does not support the claim** — the Lambda arm64 per-GB-second duration rate was not located in the retrieved text; the only Graviton figure surfaced ($0.0000036667/GB-second) is a MicroVM memory rate, a different product line. No GT-ID is assigned because no chain consumes it; the consequence is recorded in C3, which is stated as ARM-Fargate against **x86**-Lambda rather than as a like-for-like ARM comparison, and in Abandoned Reasoning #3.

## 4. Derivation Chains

**C1 — the duty-cycle break-even.** Confidence: **HIGH**.

```text
GT-1 (Lambda $0.0000166667 per GB-s) + GT-3 (1,769 MB equals one vCPU) + GT-4 (duration billed only while executing) + GT-5 (Fargate per-vCPU-s and per-GB-s rates) + GT-6 (Fargate billed wall-clock) + GT-10 (memory range 128 MB to 10,240 MB)
→ a function configured at 1,769 MB is a one-vCPU-equivalent unit, and that setting lies inside the configurable range [Assumes: A-15, equal work per vCPU-second on both platforms]
→ that unit costs 1.769 GB × $0.0000166667 per GB-s × 3600 s, which is $0.1061 per vCPU-hour of executing time
→ a Fargate task of one vCPU and 2 GB costs (0.000011244 + 2 × 0.000001235) × 3600, which is $0.0494 per wall-clock hour [Assumes: A-16, the compared task is sized 1 vCPU / 2 GB]
→ the Lambda figure is charged only for busy time while the Fargate figure is charged for elapsed time whether busy or idle
→ the two are equal where $0.1061 × d equals $0.0494, so d is 0.0494 divided by 0.1061
→ the break-even average CPU duty cycle is approximately 47 percent
→ Lambda duration billing is cheaper only for workloads averaging below roughly 47 percent CPU utilisation, and more expensive above it
```

Weakest link: step 1's equal-work assumption (A-15), which a per-service benchmark would settle. Confidence remains HIGH because both price inputs were read at source and the arithmetic is definitional.

**C2 — the request-rate ceiling.** Confidence: **HIGH**.

```text
GT-2 (Lambda $0.20 per 1M requests) + GT-5 (Fargate per-vCPU-s and per-GB-s rates) + GT-6 (Fargate billed wall-clock)
→ the per-invocation charge is $0.0000002 and is levied independently of how long the invocation runs
→ the $0.0494 hourly price of a one-vCPU Fargate task buys 0.0494 divided by 0.0000002 invocations, which is about 247,000
→ 247,000 invocations per hour is a sustained rate of about 69 requests per second
→ above that rate the Lambda request charge alone exceeds the entire Fargate task price before any duration is billed
→ no duty cycle, however low, makes Lambda cheaper for a service sustaining more than roughly 69 requests per second per vCPU-equivalent
```

Weakest link: none unverified; the chain consumes only read-at-source prices and arithmetic.

**C3 — the Graviton lever narrows the band.** Confidence: **HIGH**.

```text
GT-5 (Fargate x86 rates) + GT-7 (Fargate ARM rates) + C1 (47 percent x86 break-even)
→ a one vCPU and 2 GB task on Linux/ARM costs (0.0000089944 + 2 × 0.0000009889) × 3600, which is $0.0395 per hour
→ that is about 20 percent below the equivalent x86 task at $0.0494 per hour
→ recompiling for Graviton lowers the container hourly cost without changing the application's request semantics [Assumes: A-17, arm64 builds exist for the runtime and dependencies]
→ against the unchanged x86 Lambda price the break-even duty cycle falls from about 47 percent to about 37 percent
→ every cost lever applied to the container path narrows the band of workloads for which Lambda is the cheaper platform
```

Weakest link: the comparison is ARM-Fargate against x86-Lambda, because the Lambda arm64 rate could not be located (Phase 3 failure record). A symmetric Lambda discount would move the 37 percent figure back up; the *direction* of the conclusion — that container-side levers narrow Lambda's band — is unaffected, since the same lever applied to both platforms leaves the ordering intact.

**C4 — a Compute Savings Plan follows the workload.** Confidence: **HIGH**.

```text
GT-9 (Compute Savings Plans commit per-hour for one or three years and apply to EC2, Fargate and Lambda)
→ the discount attaches to compute usage across all three platforms rather than to a particular platform
→ moving a workload between those platforms therefore does not forfeit the commitment's benefit
→ "we must migrate before the commitment renews" is not a valid urgency argument for a Compute Savings Plan holder
→ the commitment instrument held, not the fact of migrating, is what determines whether a migration strands committed spend
```

Weakest link: none unverified.

**C5 — instance-scoped commitments do strand.** Confidence: **MEDIUM**. **Not load-bearing** — no Conclusion claim depends on it.

```text
GT-9 (Compute Savings Plans cover all three platforms) + GT-13? (commitment portfolio held, unknown)
→ an instrument scoped to an instance family does not enjoy the cross-platform flexibility the Compute plan has [Assumes: A-14, EC2 Instance Savings Plans and Standard RIs are family-scoped — not read at source]
→[2nd] a holder of such an instrument would pay the Lambda bill and the unused commitment concurrently until term expiry
→[3rd] the earliest date such a migration can realise a net saving is bounded by that expiry
→ the commitment portfolio must be inventoried in Cost Explorer before any migration date is set
```

Confidence caveat: GT-13? is unverified and A-14 was not read at source. Reading the Savings Plans plan-types documentation and pulling the account's active commitments from Cost Explorer would raise this to HIGH.

**C6 — provisioned concurrency removes the advantage where latency matters.** Confidence: **HIGH**.

```text
GT-8 (Provisioned Concurrency $0.0000041667 per GB-s, billed from enable to disable) + GT-1 (Lambda duration rate) + C1 (47 percent break-even)
→ a latency-sensitive service needs pre-warmed execution environments to hold a p99 target [Assumes: A-20, at least one service has such a target]
→ keeping one vCPU-equivalent warm costs 1.769 × $0.0000041667 × 3600, which is $0.0265 per hour whether or not it is invoked
→[2nd] the total becomes $0.0265 plus $0.1061 × d, so the break-even against $0.0494 falls to (0.0494 − 0.0265) divided by 0.1061
→[2nd] the break-even duty cycle drops from about 47 percent to about 22 percent for any service with provisioned concurrency enabled
→[3rd] the scale-to-zero property that produced the advantage is removed for precisely the services whose latency made them seem worth migrating
→ latency-sensitive request-serving services are the worst Lambda candidates on cost grounds, not the best
```

This is the extension that contradicted assumption A-11 and routed back to Phase 2. Weakest link: A-20, which is a per-service fact you can check against your own latency SLOs.

**C7 — the saving ceiling is bounded by the compute share.** Confidence: **MEDIUM**. **Not load-bearing** — no Conclusion claim depends on it.

```text
GT-11 (no bill composition supplied) + GT-12? (compute share of the bill, unknown)
→ data transfer, NAT processing, storage and managed-database charges are billed independently of which compute platform runs the code [Assumes: A-3, non-compute lines are invariant under a platform change]
→ a compute-platform migration therefore has no leverage on whatever fraction of the bill those lines represent
→ the theoretical ceiling on any Lambda migration's saving is the compute fraction of the bill, and the realised saving is strictly below it
→ that fraction is unmeasured here, so the migration's ceiling is currently unknown rather than merely uncertain
```

Confidence caveat: GT-12? is unverified. One Cost Explorer query grouped by service raises this to HIGH and converts the ceiling from unknown to a number.

**C8 — the starting premise is false as stated.** Confidence: **HIGH**.

```text
C1 (47 percent duty-cycle break-even) + C2 (69 requests per second ceiling)
→ the claim that serverless is categorically cheaper than containers is universally quantified over workloads
→ the duty-cycle break-even exhibits a counterexample at every average utilisation above roughly 47 percent
→ the request-rate ceiling exhibits a second, independent counterexample at every sustained rate above roughly 69 requests per second per vCPU-equivalent
→ a universally quantified claim is refuted by a single counterexample, and two independent families of them exist here
→ "serverless is cheaper than containers" is false as stated, and survives only as a conditional bounded by duty cycle and request rate
```

**C9 — measure before migrating.** Confidence: **HIGH**.

```text
C1 (47 percent duty-cycle break-even) + C2 (69 requests per second ceiling) + GT-11 (no duty-cycle or request-rate data supplied)
→ whether Lambda is cheaper for a given service is decided entirely by that service's position relative to two measurable thresholds
→ a service's position relative to a threshold cannot be known without measuring the quantity the threshold is expressed in
→ no such measurement was supplied to this analysis, so no service can currently be placed on either side of either threshold
→ a migration decision taken now would be a coin flip dressed as a strategy, whatever its direction [Assumes: A-21, the trade-off weights below reflect your priorities, which affects only the ordering of the intermediate steps]
→ measurement is a precondition for the migration decision rather than a preliminary to it
```

**Trade-off analysis (weighted criteria; weights locked before any option was scored).**

Criteria and weights: dollars saved per engineering-week (5); time to first realised saving (4); certainty of the saving on current evidence (4); reversibility and blast radius (4); ceiling of total achievable saving (3); operational safety for latency and availability (4); fit with current team capability (2). All phrased so higher is better.

| Option | $/eng-wk (5) | Time (4) | Certainty (4) | Reversibility (4) | Ceiling (3) | Op safety (4) | Capability (2) | **Total** |
|---|---|---|---|---|---|---|---|---|
| **A** Migrate all services to Lambda | 1 | 1 | 1 | 2 | 3 | 2 | 2 | **42** |
| **B** Rightsize + Graviton + commitment optimisation on containers | 5 | 5 | 5 | 4 | 3 | 4 | 5 | **116** |
| **C** Selective Lambda for workloads below both thresholds | 3 | 3 | 3 | 4 | 4 | 4 | 3 | **89** |
| **D** Attack non-compute lines (NAT, inter-AZ, log retention, orphaned storage, idle non-prod) | 5 | 5 | 4 | 5 | 3 | 5 | 4 | **118** |

**Sensitivity check.** D and B are 1.7% apart — inside the 10% near-tie band. The criterion that would flip the result is *certainty* (B scores 5, D scores 4); raising its weight puts B ahead, raising *operational safety* puts D further ahead. Neither weight is wrong, so per the procedure this is a **real finding, not a scoring artifact**: B and D are both defensible, they are not mutually exclusive, and the correct reading is to run both rather than to refine the scores. Option A — the path you asked for — scores lowest of the four on weights fixed before it was scored.

## 5. Abandoned Reasoning

**Dead end 1 — "any existing commitment is stranded by migrating to Lambda."**
*What was tried:* building the stranded-commitment cost into the migration's first-year net as a general objection to migrating at all.
*Why abandoned:* the Savings Plans user guide states directly that Compute Savings Plans apply to Fargate and Lambda usage (GT-9). The objection is false for the most commonly held instrument. Assumption A-13 was given a Discard verdict as a result.
*What it ruled out:* the stranding argument as a *general* reason not to migrate. It survives only in the narrower, conditional form now carried by C5.

**Dead end 2 — comparing Lambda against EC2 on-demand.**
*What was tried:* an initial unit-cost comparison against EC2 instance-hours, which is the intuitive "containers" baseline.
*Why abandoned:* it varies two things at once — the execution model *and* the capacity-management model — so any cost difference is unattributable. Fargate is the commensurable comparison because both it and Lambda are per-second-billed and fully managed with no instance capacity planning.
*What it ruled out:* a comparison that would have overstated Lambda's advantage by charging container idle-capacity waste to the container *model* rather than to capacity *planning*, which is a separately fixable problem.

**Dead end 3 — a like-for-like arm64 break-even.**
*What was tried:* computing the break-even with both platforms on Graviton, which is the fair modern comparison.
*Why abandoned:* the Lambda arm64 per-GB-second rate was not located in the retrieved pricing text across two reads (Phase 3 failure record).
*What it ruled out:* nothing — it leaves the ARM-versus-ARM break-even unquantified, and C3 is stated in the mixed form instead, with that limitation named in the chain itself.

**Pre-mortem (Phase 5 stress test).** Premise restated: *it is twelve months later, every service runs on Lambda, and the bill went up.* Causes written before filtering: provisioned concurrency enabled on the latency-sensitive tier; CloudWatch Logs ingest up sharply from per-invocation streams; API Gateway per-request charges added on top of Lambda's own; Step Functions state transitions replacing in-process control flow; DynamoDB calls replacing in-memory caches that the stateless model forbade; VPC-attached functions traversing the same NAT Gateway as before, so data-processing charges unchanged; an unexpired EC2 Instance Savings Plan paid alongside the Lambda bill; six engineer-months of migration labour never entered the business case; fan-out patterns multiplying invocation counts.

Adversarial pass ("would I have suppressed this in a group?"): the labour cost and the "we never measured the baseline" item — both are the ones a migration's sponsor is least rewarded for raising.

Clustered into three structural weaknesses, each with a plan change:
1. **No unit-cost model existed before the platform was chosen.** → Plan change: C1 and C2 are that model; no service migrates without being placed against both thresholds.
2. **Non-compute spend was invisible to the decision.** → Plan change: the CUR ranking (option D) runs first, and its result sets the migration's ceiling (C7).
3. **Ancillary charges were assumed constant.** → Accepted risk with named mitigation: log retention policies and sampling set *before* any migration, and API Gateway per-request cost modelled alongside Lambda's, not after it.

## 6. Conclusion

**Recommended approach: measure before you migrate — rank the bill by service, then rank each service by duty cycle and request rate (chain C9).** The sequence, in order:

- **Step 1 — pull the cost-and-usage report and rank spend by service before touching any compute platform (chain C9).** This is the only step that can tell you whether compute is even where your money is, and it takes hours rather than months.
- **Step 2 — apply the container-path levers that need no re-architecture: rightsizing, Graviton, and a Compute Savings Plan (chains C3, C4).** Graviton alone is about 20% off the Fargate task price, and a Compute Savings Plan does not lock you out of Lambda later.
- **Step 3 — adopt Lambda selectively, only for workloads measured below both thresholds (chains C1, C2).** Cron jobs, event handlers, spiky low-volume APIs and glue code qualify; steady high-throughput request servers do not.

**Key insight: above roughly 69 requests per second per vCPU-equivalent, Lambda's per-request charge alone exceeds the entire price of the container it would replace — before a single millisecond of execution is billed (chain C2).** This is the non-obvious result. The intuition behind "serverless is cheaper" is about *idle*, and it is correct about idle; but Lambda has a second price axis that containers do not have at all, and at production request rates that axis dominates. Reasoning by analogy to other companies' serverless success stories never surfaces it, because those stories are told by teams whose workloads sat below the threshold.

**Trade-offs acknowledged: the case for Lambda is a duty-cycle case, and three separate forces narrow it (chain C1).**

- **Latency-sensitive services are the worst Lambda candidates, not the best (chain C6).** Provisioned concurrency costs $0.0265 per vCPU-equivalent-hour whether invoked or not, which drops the break-even duty cycle from ~47% to ~22% — it removes the scale-to-zero advantage from exactly the services you would most want to keep fast.
- **A Compute Savings Plan is not an argument against migrating (chain C4).** It covers EC2, Fargate and Lambda alike, so it neither strands you nor creates urgency. Check which instrument you actually hold before treating commitments as a blocker either way.
- **Every lever applied to the container path narrows the band where Lambda wins (chain C3).** Graviton alone moves the break-even from ~47% to ~37%; rightsizing moves it further. The comparison is against your *optimised* container cost, not your current one.

**The premise you started from is false as stated (chain C8).** "Serverless is cheaper than containers" has two independent counterexample families and survives only as a conditional bounded by duty cycle and request rate. It is a useful heuristic for event-driven glue and a costly one for steady request serving.

**Overall confidence: HIGH on the platform economics, and the organisation-specific ranking is deliberately left open (chains C1, C9).** Every chain feeding a claim above consumes only ground truths read at source in AWS's own pricing and documentation pages. What this analysis cannot tell you is *your* numbers — which is why step 1 is measurement rather than a recommendation.

The fastest path to a lower bill is almost certainly not a migration at all. It is a Cost Explorer query, a scheduled shutdown of non-production, a log retention policy, and a Graviton rebuild — measured in days, reversible, and requiring no architectural change.

---

## Assumption Audit (process output)

| Chain | Step | Step Text (brief) | Assumption surfaced? | Added to Table? |
|---|---|---|---|---|
| C1 | 1 | 1,769 MB is a one-vCPU-equivalent unit | A-15 equal work per vCPU-second | yes |
| C1 | 2 | 1.769 × rate × 3600 = $0.1061/vCPU-h | none | n/a |
| C1 | 3 | Fargate 1 vCPU / 2 GB = $0.0494/hr | A-16 task sizing | yes |
| C1 | 4 | busy-time versus elapsed-time billing | none | n/a |
| C1 | 5 | equality at d = 0.0494 / 0.1061 | none | n/a |
| C1 | 6 | break-even ≈ 47 percent | none | n/a |
| C1 | 7 | cheaper only below 47 percent | none | n/a |
| C2 | 1 | per-invocation charge is duration-independent | none | n/a |
| C2 | 2 | $0.0494 buys ~247,000 invocations | none | n/a |
| C2 | 3 | 247,000/hr is ~69 rps | none | n/a |
| C2 | 4 | request charge alone exceeds task price | none | n/a |
| C2 | 5 | no duty cycle rescues it above ~69 rps | none | n/a |
| C3 | 1 | ARM task = $0.0395/hr | none | n/a |
| C3 | 2 | ~20 percent below x86 | none | n/a |
| C3 | 3 | recompile lowers cost, semantics unchanged | A-17 arm64 builds exist | yes |
| C3 | 4 | break-even falls 47 → 37 percent | none | n/a |
| C3 | 5 | container levers narrow Lambda's band | none | n/a |
| C4 | 1 | discount attaches to usage, not platform | none | n/a |
| C4 | 2 | moving between platforms forfeits nothing | none | n/a |
| C4 | 3 | renewal urgency argument is invalid | none | n/a |
| C4 | 4 | instrument, not migration, determines stranding | none | n/a |
| C5 | 1 | family-scoped instruments lack that flexibility | A-14 family scoping not read at source | yes |
| C5 | 2 | [2nd] pay Lambda and unused commitment concurrently | none | n/a |
| C5 | 3 | [3rd] net saving bounded by term expiry | none | n/a |
| C5 | 4 | inventory the portfolio before setting a date | none | n/a |
| C6 | 1 | latency target needs pre-warmed environments | A-20 a latency target exists | yes |
| C6 | 2 | warm vCPU-equivalent costs $0.0265/hr | none | n/a |
| C6 | 3 | [2nd] break-even = (0.0494 − 0.0265) / 0.1061 | none | n/a |
| C6 | 4 | [2nd] break-even drops to ~22 percent | none | n/a |
| C6 | 5 | [3rd] scale-to-zero removed where it mattered | none | n/a |
| C6 | 6 | latency-sensitive services are worst candidates | none | n/a |
| C7 | 1 | non-compute lines billed independently of platform | A-3 invariance of non-compute lines | yes |
| C7 | 2 | migration has no leverage on those lines | none | n/a |
| C7 | 3 | ceiling is the compute fraction | none | n/a |
| C7 | 4 | that fraction is unmeasured, so ceiling unknown | none | n/a |
| C8 | 1 | the claim is universally quantified | none | n/a |
| C8 | 2 | duty-cycle counterexample above 47 percent | none | n/a |
| C8 | 3 | request-rate counterexample above 69 rps | none | n/a |
| C8 | 4 | one counterexample refutes; two families exist | none | n/a |
| C8 | 5 | false as stated, survives as a conditional | none | n/a |
| C9 | 1 | position decided by two measurable thresholds | none | n/a |
| C9 | 2 | position unknowable without measuring | none | n/a |
| C9 | 3 | no measurement supplied, so no service placeable | none | n/a |
| C9 | 4 | a decision now is a coin flip | A-21 trade-off weights reflect priorities | yes |
| C9 | 5 | measurement is a precondition, not a preliminary | none | n/a |

## Self-audit scan (process output)

| Chain | Chain Head (brief) | Form conforming? | Rule applied | Dependency clean? |
|---|---|---|---|---|
| C1 | GT-1 + GT-3 + GT-4 + GT-5 + GT-6 + GT-10 | yes | n/a | yes |
| C2 | GT-2 + GT-5 + GT-6 | yes | n/a | yes |
| C3 | GT-5 + GT-7 + C1 | yes | n/a | yes |
| C4 | GT-9 | yes | n/a | yes |
| C5 | GT-9 + GT-13? | yes | n/a | yes |
| C6 | GT-8 + GT-1 + C1 | yes | n/a | yes |
| C7 | GT-11 + GT-12? | yes | n/a | yes |
| C8 | C1 + C2 | yes | n/a | yes |
| C9 | C1 + C2 + GT-11 | yes | n/a | yes |

| §6 Span (brief) | Construct | Claim under R11? | R11 clause applied | Chain cited |
|---|---|---|---|---|
| "Recommended approach: measure before you migrate…" | bold lead-in | yes | prescribed lead-in, colon closes the bold span | C9 |
| "Step 1 — pull the cost-and-usage report…" | list item | yes | closes its own sentence, over forty characters | C9 |
| "Step 2 — apply the container-path levers…" | list item | yes | closes its own sentence, over forty characters | C3, C4 |
| "Step 3 — adopt Lambda selectively…" | list item | yes | closes its own sentence, over forty characters | C1, C2 |
| "Key insight: above roughly 69 requests per second…" | bold lead-in | yes | prescribed lead-in, colon closes the bold span | C2 |
| "This is the non-obvious result. The intuition behind…" | prose | no | carries neither a bold colon lead-in nor a list marker | n/a |
| "Trade-offs acknowledged: the case for Lambda…" | bold lead-in | yes | prescribed lead-in, colon closes the bold span | C1 |
| "Latency-sensitive services are the worst Lambda candidates…" | list item | yes | closes its own sentence, over forty characters | C6 |
| "A Compute Savings Plan is not an argument against migrating…" | list item | yes | closes its own sentence, over forty characters | C4 |
| "Every lever applied to the container path narrows the band…" | list item | yes | closes its own sentence, over forty characters | C3 |
| "The premise you started from is false as stated…" | bold lead-in | yes | bold lead-in, colon closes the bold span | C8 |
| "Overall confidence: HIGH on the platform economics…" | bold lead-in | yes | bold lead-in, colon closes the bold span | C1, C9 |
| "The fastest path to a lower bill is almost certainly not…" | prose | no | carries neither a bold colon lead-in nor a list marker | n/a |

Scan complete: 9 chain rows, one per section-4 chain block in order; 13 section-6 rows, one per construct in order — 11 claims under R11, 2 excluded. 0 chains malformed, 0 claims untraced.

## Self-Audit Gate

**Criterion 1: Identify Essence**
Quoted span: "Which change to our AWS spend produces the largest dollar reduction per unit of engineering effort and operational risk — a question about *where the money is and what moves it*, not about which compute platform we prefer?"
Band: **Rigorous**
Justification: the statement is a single sentence naming the underlying question rather than the triggering event (a desire to migrate), and each of the five success criteria states a verb-subject-outcome test applied by scanning section 6 — criteria 2 and 3 name specific numeric thresholds unique to this problem.

**Criterion 2: Challenge Assumptions**
Quoted span (Assumption Audit scan): "| C6 | 1 | latency target needs pre-warmed environments | A-20 a latency target exists | yes |"
Band: **Rigorous**
Justification: all 21 rows carry a Type from the four-type scheme, treatments match the prescribed treatment per type, four rows carry Discard verdicts with specific justifications rather than bare tokens, unverified rows read "unverified — flagged", and the audit scan visits all 46 chain steps in order with each of the five surfaced assumptions recorded in the table.

**Criterion 3: Establish Ground Truths**
Quoted span: enumerated GT-12?, GT-13?; the Ground Truths list carries `?` on exactly those two entries and on no others, and each of GT-1 through GT-11 names its read location (e.g. GT-3: "At 1,769 MB, a function has the equivalent of one vCPU").
Band: **Rigorous**
Justification: every GT carries a stable ID referenced in section 4, a provenance label, and — for the eleven unsuffixed entries, each of which feeds at least one HIGH-confidence chain — a named read-at-source location; the Phase 3 failure record names the source and the reason (`citation does not support the claim`) for the one read that did not confirm its figure; no Discard-verdict assumption appears in the list.

**Criterion 4: Reason Upward**
Quoted span (self-audit scan, chain-form table): "| C1 | GT-1 + GT-3 + GT-4 + GT-5 + GT-6 + GT-10 | yes | n/a | yes |" — and, for the Abandoned Reasoning limb the table carries no column for, "Why abandoned: the Savings Plans user guide states directly that Compute Savings Plans apply to Fargate and Lambda usage (GT-9)."
Band: **Rigorous**
Justification: all nine chains score conforming with clean dependencies in the scan; each carries at least one genuine intermediate; three dead ends are documented with the What-was-tried / Why-abandoned / What-it-ruled-out structure and specific structural abandonment reasons; five chain steps declare surfaced assumptions inline with `[Assumes: X]`; no analogy is used as evidence — the pre-mortem's reference to other teams' serverless success is grounded in C2's threshold, not offered as standalone justification.

**Criterion 5: Validate**
Quoted span: "Confidence caveat: GT-13? is unverified and A-14 was not read at source. Reading the Savings Plans plan-types documentation and pulling the account's active commitments from Cost Explorer would raise this to HIGH."
Band: **Rigorous**
Justification: every chain names its weakest link; both chains consuming a `GT-N?` input (C5, C7) are rated MEDIUM, carry a caveat naming the specific unverified input and the verification that would raise it, and are explicitly marked not load-bearing; the seven chains that contribute to section 6 are all HIGH, so the section's stated HIGH rating matches its weakest contributing chain. No EXCEPT clause is claimed.

**Criterion 6: Conclusion-to-Ground-Truth Traceability**
Quoted span (self-audit scan, claim-inventory table): "| 'Key insight: above roughly 69 requests per second…' | bold lead-in | yes | prescribed lead-in, colon closes the bold span | C2 |" — and, for the Key-Insight-restatement limb the table carries no column for, "Reasoning by analogy to other companies' serverless success stories never surfaces it, because those stories are told by teams whose workloads sat below the threshold."
Band: **Rigorous**
Justification: all 11 section-6 claims trace to named section-4 chains with zero untraced, no claim introduces reasoning absent from section 4, and the Key Insight names a non-obvious result — the second pricing axis that has no container analogue — rather than restating the recommended approach, which is the measurement sequencing.

**Gate result: PASS.** No criterion Absent; zero criteria Hand-wavy. No Fix/Repeat pass was required, so the gate's re-entry edge did not fire; the one edge that did fire (second-order → Phase 2) is disclosed at the top.