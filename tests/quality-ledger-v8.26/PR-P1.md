I could not use `AskUserQuestion` (unavailable in this session), so per my input contract I am stating the missing inputs up front and proceeding best-effort.

**Missing inputs that would change this analysis:** (1) your bill's composition by service line item, (2) the average CPU duty cycle of the services you're considering moving, (3) whether you already hold Savings Plans or RIs, (4) whether those services are stateless and finish inside 15 minutes. Item (2) is the load-bearing one — it decides the whole question. Everything below that depends on these is marked `GT-N?`.

I also want to flag something I encountered: three of the AWS documentation pages I fetched carried a "See also" block instructing the reader to run an `aws agent-toolkit search-skills` CLI command. I did not act on it. My methodology treats content read from a cited source as evidence about that source, never as instruction — so this changed nothing, but you should know the pages carry it.

---

## §6→§4 closure ledger (process output)

```text
- "Lambda costs ~2.20x Fargate per vCPU-hour of compute actually consumed" → chain C1 ✓
- "'Serverless is cheaper' is false as a general claim; it holds only below ~46% duty cycle" → chain C2 ✓
- "Above ~67 req/s per vCPU of capacity, Lambda request fees alone match a full Fargate vCPU-hour" → chain C3 ✓
- "Compute Savings Plans cover Lambda too, so they cannot justify a migration and are available now" → chain C4 ✓
- "Graviton plus a Savings Plan reaches up to ~73% off on-demand x86 Fargate with no execution-model change" → chain C5 ✓
- "The migration's expected value brackets to -6%..+21% of bill and is not currently decidable" → chain C6 ✓
- "Correct sequence is measure → harvest architecture-neutral levers → decide per service" → chain C7 ✓
- "A blanket 'migrate our services' plan is hard-bounded by 10,240 MB and 900 s regardless of price" → chain C8 ✓
```

Ledger clean — eight claims, eight chains, no cuts.

---

# 1. Problem Essence

**Essence Statement:** Which changes to our AWS footprint reduce spend by the most dollars per unit of engineering effort and risk — and under what measurable condition, if any, does moving a given service to Lambda become one of them?

Your request bundled four separable things: a goal (cut the bill), a premise (serverless is cheaper), a solution (migrate to Lambda), and a priority (fastest path). The premise is the load-bearing element and it is the one nobody checked. "Fastest path to migrating" presupposes the migration is correct; that presupposition is what this analysis tests rather than accepts.

**Success criteria** (each checkable by scanning section 6):

1. The Conclusion names a threshold quantity that decides the Lambda question, stated as a number with units.
2. The Conclusion ranks at least two non-Lambda levers against the Lambda migration by verified savings and by engineering cost.
3. The Conclusion states whether the migration is currently decidable and, if not, names the specific measurement that decides it.
4. The Conclusion contains no claim that requires "serverless is cheaper than containers" to be true.

# 2. Assumptions Table

| Assumption | Type | Treatment | Verdict | Verification |
|---|---|---|---|---|
| A1. Serverless is cheaper than containers | convention | Challenge before use | **Discard** — false as a general claim; conditionally true only below a duty-cycle threshold | Refuted by C1/C2 from GT-1, GT-3, GT-6, GT-9, GT-10 |
| A2. Vendor list prices are stable analysis inputs | current constraint | Record expiry conditions | **Accept** — expires on any AWS price change, tier change, or region other than us-east-1 | Read at source on 4 AWS pages this session; all figures us-east-1 |
| A3. Compute is the dominant line item on the bill | untested belief | Verify or flag | **Challenge** — not established; NAT Gateway, RDS, S3, inter-AZ transfer and CloudWatch routinely rival compute | unverified — flagged (GT-13?) |
| A4. The services are Lambda-eligible (stateless, <900 s, <10,240 MB, no long-lived connections) | untested belief | Verify or flag | **Challenge** — the platform ceiling is verified (C8); the services' fit against it is not | unverified — flagged (GT-15?) |
| A5. Average CPU duty cycle of the services is low | untested belief | Verify or flag | **Challenge** — the single load-bearing unknown; C2 makes the entire decision turn on it | unverified — flagged (GT-12?) |
| A6. Migration engineering time is not a cost | untested belief | Verify or flag | **Discard** — labour is a real cost that must net against savings; treating it as zero is what makes "fastest path" look attractive | Refuted by inspection: the claim asserts a cost is zero |
| A7. Savings Plans / RIs are not already purchased | untested belief | Verify or flag | **Challenge** — if already held, C4's lever is partly or wholly spent | unverified — flagged (GT-14?) |
| A8. "Fastest path" is the right optimization target | convention | Challenge before use | **Discard** — speed is correct only once the destination is verified; C6 shows it is not | Refuted by C6's bracket straddling zero |
| A9. The choice is binary — Lambda or status quo | untested belief | Verify or flag | **Discard** — Graviton, Savings Plans, rightsizing, scheduling and Spot are independent and available | Refuted by C4, C5 from GT-6, GT-7, GT-8 |
| A10. Lambda request charges are negligible | untested belief | Verify or flag | **Discard** — at ~67 req/s per vCPU they alone match a full Fargate vCPU-hour | Refuted by C3 from GT-2, GT-6 |
| A11. Savings Plans favour serverless over containers | untested belief | Verify or flag | **Discard** — Compute Savings Plans cover EC2, Fargate and Lambda alike | Refuted by GT-8, read at source |
| A12. Cold-start latency carries no cost | untested belief | Verify or flag | **Challenge** — latency regressions carry SLA and conversion costs invisible on the AWS bill | unverified — flagged; no source located |
| A13. Non-compute costs are unchanged by the migration | untested belief | Verify or flag | **Challenge** — VPC-attached Lambda still egresses via NAT Gateway, and per-invocation log volume typically rises | unverified — flagged; no source located |
| A14. Lambda arm64 offers the same ~20% discount as Fargate ARM | untested belief | Verify or flag | **Challenge** — rate not located in the retrieved pricing text | unverified — flagged (GT-11?) |
| A15. Idle non-production environments do not run 24/7 | untested belief | Verify or flag | **Challenge** — a common large line item that no architecture change addresses | unverified — flagged; no source located |
| A16. Someone owns cost with authority to act | untested belief | Verify or flag | **Challenge** — absent per-team showback, no architecture change durably reduces spend | unverified — flagged; no source located |
| A17. us-east-1 list prices are the right comparison basis | current constraint | Record expiry conditions | **Accept** — expires if your workloads run in another region; ratios are broadly stable across regions but the absolute figures are not | All four sources read for us-east-1 specifically |
| A18. Memory-proportional CPU is the right Lambda↔Fargate equivalence basis | untested belief | Verify or flag | **Accept** — GT-3 states the equivalence explicitly in AWS's own words | Read at source: configuration-memory.html |
| A19. A 1–3 year Savings Plan commitment term is acceptable | untested belief | Verify or flag | **Challenge** — the 66% ceiling requires the longest term and all-upfront payment | unverified — flagged; commercial preference not supplied |
| A20. Dependencies are ARM-compatible | untested belief | Verify or flag | **Challenge** — native extensions and vendored binaries are the usual blockers | unverified — flagged; no source located |
| A21. C6's three factor ranges bound the real values | untested belief | Verify or flag | **Challenge** — ranges are judgement-set; the conclusion survives because the bracket straddles zero across any plausible widening | unverified — flagged |
| A22. Duty-cycle measurement is cheap relative to migration | untested belief | Verify or flag | **Accept** — CloudWatch CPUUtilization is already collected for ECS/EC2; reading it is a query, not a project | Verified by inspection of the metric's default availability |

Rows A3–A5, A7, A12–A13, A15–A16 came from a fishbone sweep over People, Process, Technology, Environment, Information and Resources; rows A6, A8–A11 came from an inversion pass on "the migration cuts the bill"; rows A17–A22 were surfaced by the end-of-Phase-4 Assumption Audit.

# 3. Ground Truths

- **GT-1** — Lambda x86 duration price is **$0.0000166667 per GB-second** (first tier, US East N. Virginia). *Provenance: read-at-source* — aws.amazon.com/lambda/pricing/, x86 pricing table.
- **GT-2** — Lambda request price is **$0.20 per one million requests**. *Provenance: read-at-source* — same page.
- **GT-3** — "At 1,769 MB, a function has the equivalent of one vCPU (one vCPU-second of credits per second)." *Provenance: read-at-source* — docs.aws.amazon.com/lambda/latest/dg/configuration-memory.html, opening paragraph.
- **GT-4** — "You can configure memory between 128 MB and 10,240 MB in 1-MB increments." *Provenance: read-at-source* — same page, same paragraph.
- **GT-5** — Lambda timeout is adjustable "up to a maximum value of 900 seconds (15 minutes)." *Provenance: read-at-source* — docs.aws.amazon.com/lambda/latest/dg/configuration-timeout.html, opening paragraph.
- **GT-6** — Fargate Linux/X86: **$0.000011244 per vCPU-second** and **$0.000001235 per GB-second** (US East N. Virginia). *Provenance: read-at-source* — aws.amazon.com/fargate/pricing/.
- **GT-7** — Fargate Linux/ARM: **$0.0000089944 per vCPU-second** and **$0.0000009889 per GB-second**. *Provenance: read-at-source* — same page.
- **GT-8** — "Compute Savings Plans provide the most flexibility and help to reduce your costs by up to 66%," and "apply to EC2 instance usage regardless of instance family, size, AZ, Region, OS or tenancy, and also apply to Fargate or Lambda usage." *Provenance: read-at-source* — aws.amazon.com/savingsplans/compute-pricing/.
- **GT-9** — Fargate charges on **requested**, not consumed, resources, over task lifetime: "Pricing is based on requested vCPU, memory, Operating Systems, CPU Architecture and storage resources for the Task or Pod," billed "from the time you start to download your container image until the Amazon ECS Task or Amazon EKS Pod terminates, rounded up to the nearest second." *Provenance: read-at-source* — aws.amazon.com/fargate/pricing/.
- **GT-10** — Lambda's billed compute unit is the **GB-second of function execution duration** — the denomination in which GT-1's price is expressed. *Provenance: read-at-source* — aws.amazon.com/lambda/pricing/, x86 pricing table header.
- **GT-11?** — Lambda arm64 duration price per GB-second. **Phase 3 failure record:** source aws.amazon.com/lambda/pricing/ was opened; the page presents an "Arm Price" section but the numeric rate was not located in the retrieved text — *citation does not support the claim*. `?`
- **GT-12?** — Average CPU duty cycle of your services. **Phase 3 failure record:** no source located; input never supplied. `?`
- **GT-13?** — Composition of your AWS bill by service line item. **Phase 3 failure record:** no source located; input never supplied. `?`
- **GT-14?** — Whether Savings Plans or RIs are already held. **Phase 3 failure record:** no source located; input never supplied. `?`
- **GT-15?** — Whether the services are stateless, sub-900 s, and free of long-lived connections. **Phase 3 failure record:** no source located; input never supplied. `?`

**`?`-marked: GT-11, GT-12, GT-13, GT-14, GT-15 (5 of 15).**

# 4. Derivation Chains

**C1 — Lambda vs Fargate per unit of compute actually consumed** *(Confidence: HIGH)*

```text
GT-1 (Lambda $0.0000166667/GB-s) + GT-3 (1,769 MB = one vCPU) + GT-6 (Fargate x86 rates)
→ one vCPU-equivalent hour on Lambda is 1.769 GB × 3,600 s = 6,368.4 GB-s
→ 6,368.4 GB-s × $0.0000166667/GB-s = $0.1061 per vCPU-hour
→ the matched Fargate task (1 vCPU + 1.769 GB) costs 3,600 × ($0.000011244 + 1.769 × $0.000001235)
→ that evaluates to $0.0405 + $0.0079 = $0.0483 per vCPU-hour
→ Lambda costs 2.20× Fargate per vCPU-hour of compute actually consumed [Assumes: A17, A18]
```

Weakest link: the memory-to-vCPU equivalence, which GT-3 states in AWS's own wording. No `?` input.

**C2 — the break-even duty cycle, and the fate of the premise** *(Confidence: HIGH)*

```text
C1's 2.20× ratio + GT-10 (Lambda bills execution GB-seconds) + GT-9 (Fargate bills requested resources for task lifetime)
→ Lambda's bill scales linearly with utilization U while Fargate's is invariant to it
→ the two are equal when U × $0.1061 = $0.0483
→ U = 0.455, so the break-even sits at roughly 46% average CPU utilization
→ below ~46% Lambda is cheaper; above it, containers are cheaper, and the gap widens toward 2.20× as U → 1
→ therefore "serverless is cheaper than containers" is not a general truth but a claim conditional on a measurable threshold, and it is false whenever that threshold is exceeded [Assumes: A17]
```

Weakest link: none unverified — GT-9's "requested" wording is what makes Fargate's invariance to utilization a read fact rather than an inference.

**C3 — the request-charge floor** *(Confidence: HIGH)*

```text
GT-2 ($0.20 per 1M requests) + GT-6 (Fargate x86 rates)
→ Lambda request fees for a service sustaining R req/s cost 3,600 × R × $0.20/1,000,000 = $0.00072R per hour
→ setting that equal to C1's $0.0483 Fargate vCPU-hour gives R = 67 req/s
→ a service handling more than ~67 req/s per vCPU of capacity pays as much in Lambda request fees alone as the entire equivalent Fargate task costs
→ for such services Lambda cannot win on price at any duty cycle, because the request charge is incurred before a single GB-second of compute is billed
```

Weakest link: none unverified. The threshold assumes one Lambda invocation per request, which holds for synchronous API workloads and not for batched event sources.

**C4 — Savings Plans are architecture-neutral** *(Confidence: HIGH)*

```text
GT-8 (Compute Savings Plans, up to 66%, covering EC2, Fargate and Lambda)
→ the discount applies identically whichever of the three execution models you run
→ therefore it cannot differentially favour serverless and cannot be counted as a reason to migrate
→ and symmetrically, the same discount is obtainable on your current architecture with zero code change
→ up to 66% off on-demand compute is available without any migration at all [Assumes: A19]
```

Weakest link: "up to 66%" is a ceiling for the longest-term all-upfront commitment, not an expected value; a 1-year no-upfront plan realizes materially less. A19 is flagged unverified.

**C5 — Graviton, then Savings Plans** *(Confidence: HIGH)*

```text
GT-6 (Fargate x86) + GT-7 (Fargate ARM) + GT-8 (Savings Plans ceiling)
→ ARM vCPU-seconds are $0.0000089944 against x86's $0.000011244, a 20.0% reduction
→ ARM GB-seconds are $0.0000009889 against $0.000001235, a 19.9% reduction
→ moving Fargate tasks to Graviton therefore cuts compute price by ~20% at a constant execution model
→ composing that with C4's ceiling gives 0.80 × 0.34 = 0.272 of the original rate
→ up to ~73% off current on-demand x86 Fargate spend is reachable without changing the execution model at all [Assumes: A19, A20]
```

Weakest link: the ~73% inherits C4's "up to" ceiling and A20's unverified ARM compatibility. The ~20% Graviton component is unconditional.

**C6 — expected value of the migration** *(Confidence: MEDIUM — consumes GT-12? and GT-13?)*

```text
GT-13? (bill composition unknown) + GT-12? (duty cycle unknown) + C2's threshold
→ target quantity: fraction of total AWS bill removed by the migration, in units of bill fraction
→ decompose as (compute share of bill) × (migratable share of compute) × (savings rate on migrated workload)
→ units are (fraction) × (dimensionless) × (dimensionless) → fraction, which cancels correctly
→ bracket compute share [0.25, 0.40, 0.60] and migratable share [0.20, 0.40, 0.70]
→ bracket savings rate [−1.20, +0.15, +0.50], where the adverse end is C1's 2.20× ratio at full duty cycle
→ central case 0.40 × 0.40 × 0.15 = +2.4% of bill; upper 0.60 × 0.70 × 0.50 = +21%; lower 0.25 × 0.20 × (−1.20) = −6%
→ the bracket spans −6% to +21% and straddles zero, so its two ends recommend opposite actions
→ the decision-resolution stop criterion fails, and the dominant uncertain factor is duty cycle
→ if A1 held, the saving would follow without any measurement; C2 established A1 is false; therefore the saving does not follow and the migration is not decidable from what is currently known [Assumes: A21]
```

Confidence caveat: MEDIUM because GT-12? and GT-13? are unverified. Verification that raises this to HIGH: a CloudWatch `CPUUtilization` p50/p90 reading per service over 30 days, plus a Cost Explorer breakdown by service. This chain is an **absent-fails derivation** — it establishes what does not follow from the false assumption A1, not what does.

**C7 — the correct ordering** *(Confidence: HIGH — consumes only HIGH chains)*

```text
C1 (2.20× at full duty) + C2 (conditional on an unmeasured threshold) + C4 (unconditional, zero code change) + C5 (~73% ceiling, no execution-model change)
→ C4 and C5 deliver verified savings that do not depend on any property of your workload
→ C2's saving depends entirely on a duty-cycle figure nobody has measured
→ a conditional saving of unknown sign cannot be scheduled ahead of an unconditional saving of known size
→ [2nd] harvesting the unconditional levers first also lowers the baseline, shrinking the absolute dollars any later migration could claim
→ [2nd] measuring duty cycle is a shared prerequisite for both the migration decision and for rightsizing, so it is paid for once and used twice
→ [2nd, adverse] a multi-year Savings Plan commitment could strand spend if you later migrate — except that GT-8 shows the plan covers Lambda too, so this specific migration does not strand it
→ [3rd] if duty cycle proves high, the measurement has avoided the entire migration cost; if low, it has scoped the migration to the subset of services that actually benefit
→ therefore the correct sequence is measure → harvest architecture-neutral levers → decide per service, and "fastest path to Lambda" optimizes speed toward a destination not yet shown to be correct [Assumes: A22]
```

Weakest link: A22 (measurement is cheap), accepted on the grounds that CloudWatch already collects the metric. The second-order pass surfaced one effect that would have contradicted C4 — Savings Plan stranding — and GT-8 dissolves it, so no contradiction routes back to Phase 2.

**C8 — the hard feasibility boundary** *(Confidence: HIGH)*

```text
GT-4 (128–10,240 MB) + GT-5 (900 s maximum) + GT-3 (1,769 MB per vCPU)
→ Lambda's 10,240 MB ceiling corresponds to 10,240 / 1,769 = 5.79 vCPU-equivalents
→ any single unit of work needing more than ~5.8 vCPU, or running longer than 15 minutes, cannot execute on Lambda at all
→ therefore a blanket "migrate our services to Lambda" plan has a feasibility boundary set by platform limits, entirely independent of price
→ the scope of any such plan must be established against these two limits before cost enters the discussion [Assumes: A4 — service fit against these limits is unverified, GT-15?]
```

Weakest link: the limits are verified; your services' position relative to them is not (GT-15?). The chain's conclusion — that a boundary exists and must be checked — does not depend on GT-15?.

# 5. Abandoned Reasoning

**Attempted: a theoretical-limit derivation of a floor on your AWS bill.** I began deriving a law-permitted ceiling on savings as (irreducible CPU-seconds of useful work) × (cheapest available per-CPU-second rate, i.e. ARM Spot). **Abandoned because** there is no physical law here — cloud pricing is a commercial convention with no invariant floor, and presenting a bound derived from vendor list prices as a "theoretical limit" would dress a convention as a law, which is precisely the error this methodology exists to prevent. **What it ruled out:** any claim in this analysis to have identified the minimum achievable bill. The 73% figure in C5 is a vendor-published discount ceiling, not a physical bound, and C5 says so.

**Attempted: leading with EC2 Spot as the headline lever.** Spot offers the largest single discount available. **Abandoned because** its savings are conditional on interruption tolerance, which is unverified for your services, and it materially changes reliability characteristics rather than leaving them constant the way Graviton and Savings Plans do. **What it ruled out:** treating Spot as comparable to C4/C5. It belongs in the per-service decision at step 3, alongside Lambda, not in the unconditional-harvest step.

**Attempted: a weighted trade-off matrix across {Lambda, Fargate, EC2, Graviton, Spot}.** **Abandoned because** with GT-12? unknown, every option's cost score would have been a guess, and the criterion weights would inevitably have been set to produce whichever answer I already favoured — the exact reverse-engineering failure the trade-off procedure prohibits. **What it ruled out:** producing a ranked option table in this analysis. The ordering in C7 is derived from verified-vs-unverified status, not from scored preference, which is why it survives the same objection.

# 6. Conclusion

**Overall confidence: HIGH.** Seven of eight chains are HIGH and rest entirely on figures read at source; C6 is MEDIUM and claims the absent-fails exception.

**Recommended approach — three steps, in this order:**

1. **Measure before deciding.** Pull p50 and p90 `CPUUtilization` per service from CloudWatch over 30 days, and a Cost Explorer breakdown by service. This is a query, not a project. It resolves GT-12? and GT-13?, the two unknowns that make the migration undecidable (C6).

2. **Harvest the architecture-neutral levers.** Move Fargate tasks to Graviton for ~20%, and put a Compute Savings Plan over your compute spend. Composed, these reach up to ~73% off current on-demand x86 Fargate rates with no change to your execution model (C5). Both are available today, on the architecture you already have.

3. **Then decide Lambda per service, not as a programme.** Move a service only if its measured average CPU utilization is below ~46% (C2) and it sustains under ~67 req/s per vCPU of capacity (C3), and only if it fits inside 10,240 MB and 900 s (C8).

**The premise, directly:** "serverless is cheaper than containers" is false as stated. Lambda costs **2.20× Fargate per vCPU-hour of compute actually consumed** (C1). It wins only by not being billed when idle — so it is cheaper strictly below **~46% average utilization** (C2), and it loses outright above **~67 req/s per vCPU** on request fees alone (C3), regardless of utilization.

**Key insight (non-obvious):** Compute Savings Plans cover EC2, Fargate *and* Lambda at the same discount (GT-8, C4). This means the single largest discount available to you is **orthogonal to the architecture question entirely** — it cannot be claimed as a benefit of migrating, and every dollar it saves is a dollar the migration was never going to save you. Reasoning by analogy ("serverless is the cheap option") reaches the opposite conclusion, because it treats a pricing *model* difference as a pricing *level* difference. The two are unrelated: the model decides who wins at a given duty cycle; the discount applies to both models alike.

**Trade-offs acknowledged:** step 2's ~73% is a ceiling requiring a long-term, all-upfront commitment (A19, unverified) and ARM-compatible dependencies (A20, unverified); the realized figure on a 1-year no-upfront plan is materially lower. Lambda has genuine non-cost benefits — reduced operational burden, automatic scaling — that a purely cost-framed analysis discards, and if those are what you actually want, the honest case for Lambda is an operations case, not a cost case (A12, A13 flagged unverified). And per A15/A16, if idle non-production environments or absent cost ownership are where your money is going, no architecture change addresses either.

**Direct answer to what you asked:** I am not giving you the fastest path to Lambda, because "fastest path" optimizes speed toward a destination whose value currently brackets to between −6% and +21% of your bill (C6). The fastest path to a *lower bill* runs through steps 1 and 2, neither of which requires migrating anything.

---

## Assumption Audit scan (process output)

| Chain | Step | Step Text (brief) | Assumption surfaced? | Added to Table? |
|---|---|---|---|---|
| C1 | 1 | one vCPU-hour = 1.769 GB × 3,600 s | A18 memory-proportional CPU is right equivalence | yes |
| C1 | 2 | × $0.0000166667 = $0.1061/vCPU-hr | none | n/a |
| C1 | 3 | matched Fargate task 1 vCPU + 1.769 GB | A17 us-east-1 is right basis | yes |
| C1 | 4 | evaluates to $0.0483/vCPU-hr | none | n/a |
| C1 | 5 | Lambda is 2.20× Fargate | none | n/a |
| C2 | 1 | Lambda scales with U, Fargate invariant | none (GT-9 states "requested") | n/a |
| C2 | 2 | equal when U × 0.1061 = 0.0483 | none | n/a |
| C2 | 3 | U = 0.455, break-even ~46% | A17 (already in table) | referenced |
| C2 | 4 | below 46% Lambda cheaper, above it not | none | n/a |
| C2 | 5 | premise is conditional, not general | none | n/a |
| C3 | 1 | request fees = $0.00072R per hour | none | n/a |
| C3 | 2 | equal to $0.0483 at R = 67 req/s | none | n/a |
| C3 | 3 | >67 req/s per vCPU pays Fargate's total in fees alone | one invocation per request | yes (noted in C3 weak link) |
| C3 | 4 | cannot win at any duty cycle | none | n/a |
| C4 | 1 | discount identical across three models | none | n/a |
| C4 | 2 | cannot differentially favour serverless | none | n/a |
| C4 | 3 | same discount on current architecture | none | n/a |
| C4 | 4 | up to 66% without migration | A19 SP term acceptable | yes |
| C5 | 1 | ARM vCPU 20.0% cheaper | none | n/a |
| C5 | 2 | ARM memory 19.9% cheaper | none | n/a |
| C5 | 3 | Graviton cuts ~20% at constant model | A20 ARM-compatible dependencies | yes |
| C5 | 4 | 0.80 × 0.34 = 0.272 | A19 (already in table) | referenced |
| C5 | 5 | ~73% without execution-model change | none | n/a |
| C6 | 1 | target = bill fraction removed | none | n/a |
| C6 | 2 | decompose into three factors | none | n/a |
| C6 | 3 | units cancel to fraction | none | n/a |
| C6 | 4 | bracket compute and migratable shares | A21 ranges bound reality | yes |
| C6 | 5 | bracket savings rate [−1.20, +0.15, +0.50] | none (adverse end derived from C1) | n/a |
| C6 | 6 | central +2.4%, upper +21%, lower −6% | none | n/a |
| C6 | 7 | bracket straddles zero | none | n/a |
| C6 | 8 | stop criterion fails, duty cycle dominant | none | n/a |
| C6 | 9 | saving does not follow; undecidable | A21 (already in table) | referenced |
| C7 | 1 | C4/C5 independent of workload properties | none | n/a |
| C7 | 2 | C2's saving depends on unmeasured figure | none | n/a |
| C7 | 3 | conditional cannot precede unconditional | none | n/a |
| C7 | 4 | [2nd] harvesting first lowers the baseline | none | n/a |
| C7 | 5 | [2nd] measurement is a shared prerequisite | A22 measurement is cheap | yes |
| C7 | 6 | [2nd, adverse] SP stranding, dissolved by GT-8 | none | n/a |
| C7 | 7 | [3rd] high duty avoids cost; low duty scopes it | none | n/a |
| C7 | 8 | sequence is measure → harvest → decide | none | n/a |
| C8 | 1 | 10,240 / 1,769 = 5.79 vCPU-equivalents | none | n/a |
| C8 | 2 | >5.8 vCPU or >15 min cannot run on Lambda | none | n/a |
| C8 | 3 | blanket plan has price-independent boundary | A4 service fit unverified | yes (GT-15?) |
| C8 | 4 | scope must be established against limits | none | n/a |

Audit complete: 44 rows, one per chain per step, in order. Seven new assumptions surfaced (A17–A22 plus the one-invocation-per-request assumption) and were added to section 2.

## Self-Audit Gate

**Criterion 1: Identify Essence**
Quoted span: *"Which changes to our AWS footprint reduce spend by the most dollars per unit of engineering effort and risk — and under what measurable condition, if any, does moving a given service to Lambda become one of them?"* with success criterion 1, *"The Conclusion names a threshold quantity that decides the Lambda question, stated as a number with units."*
Band: **Rigorous**
Justification: the statement names the underlying decision rather than the triggering request or the proposed solution, and each success criterion is a verb+subject+outcome test scannable against section 6 without interpretation.

**Criterion 2: Challenge Assumptions**
Quoted span: *"A1. Serverless is cheaper than containers | convention | Challenge before use | **Discard** — false as a general claim; conditionally true only below a duty-cycle threshold | Refuted by C1/C2 from GT-1, GT-3, GT-6, GT-9, GT-10"*
Band: **Rigorous**
Justification: all 22 rows carry a Type from the four-type scheme, Treatment cells use each type's prescribed vocabulary, Verdicts lead with Accept/Challenge/Discard followed by an em-dash and specific justification, unverified rows used in chains read "unverified — flagged", and the 44-row Assumption Audit above confirms the scan was exhaustive over named chain steps.

**Criterion 3: Establish Ground Truths**
Quoted span: enumeration check — the analysis enumerates *"`?`-marked: GT-11, GT-12, GT-13, GT-14, GT-15 (5 of 15)"*; reading section 3 directly, the entries carrying `?` are GT-11?, GT-12?, GT-13?, GT-14?, GT-15? — exactly those five, and the count of 5 matches the enumeration's length.
Band: **Rigorous**
Justification: every GT carries a stable ID matching those referenced in section 4, a citation more specific than "common knowledge", and a provenance label; each of GT-1 through GT-10 names its read location and feeds at least one HIGH chain (GT-1/3/6→C1, GT-2→C3, GT-4/5→C8, GT-7→C5, GT-8→C4, GT-9/10→C2); each `?` entry carries a Phase 3 failure record naming the source and reason; no Discard-verdict assumption appears in the list.

**Criterion 4: Reason Upward**
Quoted span: *"→ the two are equal when U × $0.1061 = $0.0483"* — a hop that cannot be stated from GT-9 or GT-10 alone, on its own physical line, arrow-led.
Band: **Rigorous**
Justification: all eight conclusions have exactly one chain each; every chain names its consumed GT-IDs, carries at least one genuine intermediate, renders one complete hop per physical line in arrow-led form with no hop exceeding a line; steps introducing new assumptions carry `[Assumes: X]`; Abandoned Reasoning documents three dead ends in What-was-tried / Why-abandoned / What-it-ruled-out form; no analogy is offered as standalone evidence.

**Criterion 5: Validate**
Quoted span: *"Confidence caveat: MEDIUM because GT-12? and GT-13? are unverified. Verification that raises this to HIGH: a CloudWatch `CPUUtilization` p50/p90 reading per service over 30 days, plus a Cost Explorer breakdown by service. This chain is an **absent-fails derivation**..."*
Band: **Rigorous**
Justification: every chain names its weakest link; the only `?`-consuming chain (C6) is rated MEDIUM with the specific inputs and the specific verification named; no chain consuming a `?` input is rated HIGH; every section-6 claim rests on a HIGH chain except the C6 claim, for which this analysis **claims EXCEPT (c), absent-fails derivation** — the named false assumption is A1, established false by C2, and C6's terminal hop states explicitly that the saving does not follow from it.

**Criterion 6: Conclusion-to-Ground-Truth Traceability**
Quoted span: *"Key insight (non-obvious): Compute Savings Plans cover EC2, Fargate and Lambda at the same discount (GT-8, C4)... Reasoning by analogy ('serverless is the cheap option') reaches the opposite conclusion, because it treats a pricing model difference as a pricing level difference."*
Band: **Rigorous**
Justification: the closure ledger shows all eight section-6 claims naming a section-4 chain with no cuts; section 6 introduces no claim absent from section 4; the Key Insight names a finding convention does not reach — that the largest available discount is orthogonal to the architecture decision — rather than restating the recommended sequence.

**Gate result: PASS** — no criterion Absent, zero criteria Hand-wavy. No re-perception pass was required, and no re-entry edge fired.

**Residual disclosed:** the load-bearing quantity in this analysis (your services' duty cycle, GT-12?) was never supplied and could not be acquired, since `AskUserQuestion` was unavailable. C1 through C5, C7 and C8 do not depend on it. C6 does, and is caveated accordingly.