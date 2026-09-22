**Bottom line: your AWS pricing does not support the premise. Per second of actual work, Lambda costs about 2.1× what a Fargate container costs. It only saves money on services that sit idle most of the time.** So the fastest way to cut the bill is not a Lambda migration. First measure where the money goes. Then use discounts that need no code change on steady services, and move only the services that measure mostly idle.

**Inputs I didn't have.** I couldn't ask you mid-run, so I proceeded without three things:
1. How your bill splits by service and usage type (compute vs. databases vs. NAT Gateway and data transfer).
2. How busy each service really is, and how many requests it handles at once.
3. What your containers run on now (Fargate or EC2, on-demand or discounted).

The analysis still stands without them, but the savings figure depends on them. It's the one open question left (C3).

**Process notes:**
- **Mode:** full analysis; no single-technique trigger fired.
- **Re-entry edges:** none fired.
- **Omissions:** the closure ledger, self-audit scan and Self-Audit Gate all ran. The output template, validation rubric and pre-mortem procedure were all opened and read.
- **Not applied:** the trade-off matrix (see §5), plus fishbone, five-whys, theoretical-limit and inversion. None of those was needed: the claim fell to arithmetic from published prices. The estimate procedure fed the bracket in C2. Second-order thinking extended C5. The pre-mortem ran in Phase 5.
- **Where the prices came from:** GT-1, GT-3, GT-5 and GT-8 were read through WebFetch, which returns a verbatim quote pulled out by a summarizing model. The quotes are internally consistent (checked in the Recompute step). GT-2 came from the raw page text.

---

## 1. Problem Essence

**Core problem:** Which changes to how your services are billed would cut the total AWS bill? And does moving to Lambda cut it at all, given how busy your workloads actually are?

**Success criteria:**
- The Conclusion states under what measured condition Lambda costs less than your current containers. That condition is a number, not "serverless is cheaper."
- The Conclusion names the first action, and says whether that action needs code changes.
- The Conclusion says which unknown inputs decide the size of the saving, and how to measure them.

## 2. Assumptions Table

| Assumption | Type | Treatment | Verdict | Verification |
|---|---|---|---|---|
| A1: Serverless is cheaper than containers | untested belief | Verify, or flag as unverified | Discard — per busy second Lambda costs 2.10× Fargate on-demand (C1); it only holds for mostly-idle services (C2) | GT-1, GT-2, GT-3 read at source |
| A2: Migration speed is what matters | convention | Challenge before use | Challenge — the goal is a lower bill; migration is only one way to get there, and it needs code changes while the alternatives don't (C4) | Challenged in Phase 1: the Essence was reframed around the bill |
| A3: Compute is a large share of the bill | untested belief | Verify, or flag as unverified | Challenge — not measured; if compute is a small share, no compute lever matters much | unverified — flagged (GT-6?) |
| A4: Your services are mostly idle (low utilization) | untested belief | Verify, or flag as unverified | Challenge — not measured; this is the quantity that decides C2 | unverified — flagged (GT-6?) |
| A5: Lambda bills each request's full wall-clock time, and each environment handles one request at a time | untested belief | Verify, or flag as unverified | Accept — used as GT-4? with a confidence caveat | unverified — flagged |
| A6: Your containers today run on Fargate on-demand in us-east-1 | untested belief | Verify, or flag as unverified | Accept — priced: if they run on discounted Fargate (GT-5), Lambda's 2.10× gap only widens | unverified — flagged |
| A7: The engineering cost of migrating is material | untested belief | Verify, or flag as unverified | Accept — used only in C5's second-order extension | unverified — flagged |
| A8: Published list prices hold | current constraint | Record expiry | Accept — expires when AWS changes prices; figures as read 2026-09-22 | GT-1, GT-3, GT-5 pages |
| A9: Lambda's run-time limits and cold starts are acceptable | current constraint | Record expiry | Challenge — not read in this analysis; long-running jobs are excluded regardless of cost | not verified; not used in any chain |
| A10: Lambda gets CPU in proportion to its memory setting | current constraint | Record expiry | Accept — lasts until AWS changes how it allocates CPU | GT-2 read at source |
| A11: A Fargate task with 1 vCPU and 2 GB is a fair comparison shape (found in audit) | convention | Challenge before use | Accept — challenged: from 1.73 GB to 8 GB of memory per vCPU the ratio runs 2.15× down to 1.36×, always above 1 | arithmetic on GT-3 |
| A12: The Lambda function is sized at 1,769 MB (found in audit) | convention | Challenge before use | Accept — challenged: smaller sizes make request fees a bigger share, which lowers the breakeven, so 48% stays the ceiling | arithmetic on GT-1 |

## 3. Ground Truths

- **GT-1** Lambda x86 in US East (N. Virginia) costs $0.0000166667 per GB-second (Arm: $0.0000133334), plus $0.20 per million requests. The free tier is 1M requests and 400,000 GB-seconds a month. Source: aws.amazon.com/lambda/pricing. Read at source: verbatim quote of the first-tier duration row and the request row.
- **GT-2** "Lambda allocates CPU power in proportion to the amount of memory configured… At 1,769 MB, a function has the equivalent of one vCPU." Source: AWS Lambda Developer Guide, "Configure Lambda function memory". Read at source: opening paragraph, quoted.
- **GT-3** Fargate Linux/x86 in US East (N. Virginia) costs $0.000011244 per vCPU-second and $0.000001235 per GB-second. Source: aws.amazon.com/fargate/pricing. Read at source: Example 1, which states the region.
- **GT-4?** Lambda bills each invocation for its full wall-clock time, including time spent waiting on I/O, and a standard environment handles one request at a time. Unverified: this analysis didn't open the execution-environment docs.
- **GT-5** "Fargate Spot… at up to a 70% discount" and "Savings Plans offer savings of up to 50% on your AWS Fargate usage." Source: aws.amazon.com/fargate/pricing. Read at source: both sentences quoted.
- **GT-6?** Two things are unknown to this analysis: how your bill splits by service and usage type, and each service's utilization (u). Unverified: you didn't supply them.
- **GT-8** Compute Savings Plans "also apply to Fargate or Lambda usage." Source: aws.amazon.com/savingsplans/compute-pricing. Read at source: quoted sentence. **Phase 3 failure record:** I also looked for the size of the Savings Plan discount on Lambda, on the Compute Savings Plans page and the Lambda pricing page. Neither states it (`citation does not support the claim`). C4 therefore claims only that the plans apply to Lambda, not how much they save.

(GT-7 is not assigned.)

```text
?-marked: GT-4?, GT-6? (2 of 7)
Read-at-source: GT-1 — Lambda pricing page, x86/Arm first-tier duration and request rows; GT-2 — Lambda memory docs, opening paragraph; GT-3 — Fargate pricing Example 1 (us-east-1); GT-5 — Fargate pricing, Spot and Savings Plans sentences; GT-8 — Compute Savings Plans page, applicability sentence
```

## 4. Derivation Chains

### Conclusion C1: Per second of busy compute, Lambda costs 2.10× Fargate on-demand

GT-1 (Lambda $/GB-s) + GT-2 (1,769 MB = 1 vCPU) + GT-3 (Fargate $/vCPU-s and $/GB-s)
→ one vCPU of Lambda bills 1.7275 GB, at $0.00002879 per second or $0.1036 per hour
→ a 1 vCPU / 2 GB Fargate task costs $0.000013714 per second or $0.0494 per hour [Assumes: A11]
→ per second of busy compute, Lambda costs 2.10× Fargate on-demand before request fees
→ "serverless is cheaper" is false as a general rule about unit price

**Pre-check:** head GT-1, GT-2, GT-3 · ?-marked: none · lowest cited: none · Inputs ceiling: HIGH
**Confidence:** HIGH — all inputs were read at source and the arithmetic recomputes. A11 is priced: across 1.73–8 GB per vCPU the ratio stays between 2.15× and 1.36×, so the endpoint holds. The Arm Lambda rival is ruled out in §5. Weakest link: the WebFetch extraction of GT-3, which is internally consistent.

### Conclusion C2: Lambda only costs less when a service is busy less than about 35–48% of its provisioned time

C1 (2.10× per busy second) + GT-1 (request fee) + GT-4? (per-invocation wall-clock billing)
→ Lambda cost equals 2.10 × container cost × u, where u is total invocation wall-clock seconds divided by provisioned container seconds
→ request fees add between 0.7% (at a 1 s average request) and 35% (at 20 ms) on top of duration cost at 1,769 MB [Assumes: A12]
→ Lambda costs less than an on-demand container only when u is below roughly 35–48%
→ requests that run concurrently push u above CPU utilization, because I/O-bound requests share one container vCPU but are each billed in full on Lambda
→ always-on, steady or high-concurrency services cost more on Lambda, while spiky, low-traffic and scheduled jobs cost less

**Pre-check:** head C1 (HIGH), GT-1, GT-4? · ?-marked: GT-4? · lowest cited: HIGH · Inputs ceiling: MEDIUM
**Confidence:** MEDIUM — Inputs axis. GT-4? is unverified; reading the Lambda execution-environment and billing-duration docs would close it. A12 is priced: smaller function sizes only lower the breakeven, so 48% stays the ceiling. Weakest link: the concurrency hop, which depends entirely on GT-4?.

### Conclusion C3: Until the bill is measured, a Lambda migration's saving could be positive, zero or negative

GT-6? (bill split and u unknown) + C2 (breakeven u ≈ 35–48%)
→ migration can remove at most the compute share of the bill, and only for services below breakeven
→ with neither the compute share nor any service's u measured, the net saving could be positive, zero or negative
→ ranking "fastest path to Lambda" above other levers has no basis until both are measured

**Pre-check:** head GT-6?, C2 (MEDIUM) · ?-marked: GT-6? · lowest cited: MEDIUM · Inputs ceiling: MEDIUM
**Confidence:** MEDIUM — Inputs axis. GT-6? closes with Cost Explorer grouped by service and usage type, plus per-service request duration and concurrency metrics over a representative window. C2 is MEDIUM. Weakest link: GT-6?.

### Conclusion C4: Discounts on the existing containers are available now, with no migration and no code change

GT-3 (Fargate on-demand rates) + GT-5 (Savings Plans up to 50%, Spot up to 70%) + GT-8 (Compute Savings Plans cover Fargate and Lambda)
→ the 1 vCPU / 2 GB task's $0.0494 per hour can fall as low as $0.0247 with a Savings Plan or $0.0148 on Spot
→ those cuts need only a commitment or tolerance for interruption, not code changes
→ because Compute Savings Plans also cover Lambda, a commitment made now doesn't block a later migration
→ discount levers on the existing container fleet are available immediately, without migrating

**Pre-check:** head GT-3, GT-5, GT-8 · ?-marked: none · lowest cited: none · Inputs ceiling: HIGH
**Confidence:** HIGH — all inputs were read and the arithmetic recomputes. The endpoint claims the levers are available, not that you'll get the full discount; the "up to" ceilings are stated as ceilings. Weakest link: the realized discount depends on the plan's term and payment option, which the endpoint doesn't claim.

### Conclusion C5: Measure first, discount steady services second, move only measured-idle services to Lambda

C1 (2.10× per busy second) + C2 (breakeven 35–48%) + C3 (saving unknown until measured) + C4 (no-code discounts)
→ the order that can't lose money is measure, then discount steady services, then migrate only services measured below breakeven
→ step one is a Cost Explorer breakdown by service and usage type, plus each service's u from invocation duration and concurrency
→ step two applies a Savings Plan sized to the measured usage floor, or Spot for stateless, interruption-tolerant tasks
→ step three moves to Lambda only services measured below about 35% u, where both ends of C2's bracket agree
→ the first migration is a single pilot service with a rollback trigger at the breakeven u
→[2nd] the fleet becomes mixed, containers plus Lambda
→[3rd] two deployment and observability stacks must be run, a cost that sits outside the AWS bill [Assumes: A7]

**Pre-check:** head C1 (HIGH), C2 (MEDIUM), C3 (MEDIUM), C4 (HIGH) · ?-marked: none · lowest cited: MEDIUM · Inputs ceiling: MEDIUM
**Confidence:** MEDIUM — Inputs axis: C2 and C3 are MEDIUM. A7 applies only to the 3rd-order extension, not to the endpoint. The rival "migrate everything now" is ruled out in §5 by C1 and C2. Weakest link: step three's threshold, which rests on C2.

## 5. Abandoned Reasoning

### Dead End: Serverless is cheaper, so migrate everything as fast as possible
**What was tried:** Taking the brief's premise as given and planning the fastest migration.
**Why abandoned:** It contradicts C1: Lambda costs 2.10× per busy second, so moving steady services raises the bill (C2).
**What it ruled out:** Migrating everything as the default; per-service measurement comes first.

### Dead End: Arm Lambda closes the price gap
**What was tried:** Pricing Lambda on Arm at the GT-1 rate of $0.0000133334 per GB-s: 1.7275 GB × 3,600 s ≈ $0.0829 per hour.
**Why abandoned:** That is still 1.68× the x86 Fargate rate from GT-3.
**What it ruled out:** Picking a different CPU architecture doesn't overturn C1.

### Dead End: A weighted trade-off matrix across platforms
**What was tried:** Scoring Lambda, Fargate and a mix on weighted criteria.
**Why abandoned:** The cost decision comes down to one measurable threshold (u against C2's breakeven), and every weight would score quantities nobody has measured (GT-6?). Weighting unmeasured inputs just produces the preference already held.
**What it ruled out:** Deciding by qualitative scoring before measuring.

### Dead End: Lambda Managed Instances as a way around per-request billing
**What was tried:** The Lambda pricing page mentions Managed Instances that run on EC2 pricing.
**Why abandoned:** I didn't read that product's pricing or concurrency model, and running on EC2 pricing makes it a container-cost option under another name. No chain could be built on it.
**What it ruled out:** Nothing definitively. It's worth a look only if step three's pilot wants Lambda's deployment model at a container's cost.

## 6. Conclusion

**Recommended approach:** Don't start with a Lambda migration. First measure the bill by service and usage type, and measure each service's u. Then put Savings Plans or Spot on steady services. Move only services measured below about 35% u to Lambda, one pilot first (chain C5).

**Key insight:** "Serverless is cheaper" is really a claim about idle time. Lambda costs 2.10× per busy second, so it wins only for services idle more than roughly half the time, and concurrent requests make that worse (chains C1, C2).

**Fastest safe first move:** The discount levers on the existing containers are available today with no code change (chain C4).

**Trade-offs acknowledged:** Measuring first delays savings by the length of the measurement window. A mixed fleet also means running two deployment stacks, a cost that doesn't show up on the AWS bill (chain C5).

**Pre-check:** head C1 (HIGH), C2 (MEDIUM), C3 (MEDIUM), C4 (HIGH), C5 (MEDIUM) · ?-marked: none · lowest cited: MEDIUM · Inputs ceiling: MEDIUM (chains C1, C2, C3, C4, C5)
**Confidence:** MEDIUM — C2, C3 and C5 are rated below HIGH. Your cost-and-usage data (GT-6?) and the Lambda billing docs (GT-4?) would lift them (chain C5).

---

## Assumption Audit scan (process output)

| Chain | Step | Step Text (brief) | Assumption surfaced? | Added to Table? |
|---|---|---|---|---|
| C1 | 1 | Lambda 1 vCPU = $0.1036/hr | none | n/a |
| C1 | 2 | Fargate 1 vCPU/2 GB = $0.0494/hr | A11 comparison shape | yes |
| C1 | 3 | 2.10× per busy second | none | n/a |
| C1 | 4 | premise false as general rule | none | n/a |
| C2 | 1 | cost = 2.10 × container × u | none | n/a |
| C2 | 2 | request fees add 0.7–35% | A12 function size | yes |
| C2 | 3 | breakeven 35–48% | none | n/a |
| C2 | 4 | concurrency raises u | A5 (already in table as GT-4?) | n/a |
| C2 | 5 | steady services cost more on Lambda | none | n/a |
| C3 | 1 | saving bounded by compute share | A3 (already in table) | n/a |
| C3 | 2 | saving could be ±/0 | A4 (already in table) | n/a |
| C3 | 3 | no basis to rank migration first | none | n/a |
| C4 | 1 | $0.0247 / $0.0148 per hr | none | n/a |
| C4 | 2 | no code change needed | none | n/a |
| C4 | 3 | commitment doesn't block migration | none | n/a |
| C4 | 4 | levers available now | none | n/a |
| C5 | 1 | order that can't lose money | none | n/a |
| C5 | 2 | step one: measure | none | n/a |
| C5 | 3 | step two: commit or use Spot | none | n/a |
| C5 | 4 | step three: migrate below ~35% | none | n/a |
| C5 | 5 | single pilot with rollback | none | n/a |
| C5 | 6 | [2nd] mixed fleet | none | n/a |
| C5 | 7 | [3rd] two stacks, off-bill cost | A7 | yes (declared in Phase 2) |

## Adversarial pass (process output)

**Recompute.**
- Lambda: 1769/1024 = 1.72754 GB × $0.0000166667 = $0.000028792/s → $0.10365/hr ✓
- Fargate: $0.000011244 + 2 × $0.000001235 = $0.000013714/s → $0.049370/hr ✓
- Ratio: 2.0995 ✓
- Request fee as a share of duration cost: at 100 ms, 0.20/2.879 = 6.9% → 2.245× → breakeven 44.5%; at 20 ms, 34.7% → 2.829× → 35.4%; at 1 s, 0.7% → 47.3%; the limit is 1/2.0995 = 47.6% ✓
- Arm: $0.08292/hr → 1.68× ✓
- Discounts: 0.04937 × 0.5 = $0.02469; × 0.3 = $0.01481 ✓
- A11 bracket: 1.73 GB → 2.15×; 4 GB → 1.78×; 8 GB → 1.36× ✓

**Sensitivity.** The flip input is GT-6? (`?`-marked): if compute is a trivial share of the bill, every compute lever is secondary. Only your data can verify it, so it stays as the caveat on C3 and C5.

**Rival.** "Migrate everything now" is ruled out by C1 and C2 (§5, first dead end).

**Premise.** It is March 2027, and the bill-reduction effort has failed: the AWS bill is no lower, or higher.

**Causes** (from four viewpoints: implementing engineer, finance, on-call SRE, product team):
1. Compute turned out to be about 20% of the bill; NAT Gateway, data transfer and the databases were never looked at.
2. u was measured as CPU utilization, not invocation wall-clock time, so high-concurrency services looked cheap on Lambda.
3. Traffic grew and pushed a migrated service's u above breakeven.
4. A 3-year Savings Plan was sized to peak usage; after right-sizing it went partly unused.
5. Engineering months spent on migration outweighed the saving.
6. Cold starts and timeouts on a migrated service caused incidents, and it was rolled back.
7. Two stacks doubled the on-call surface.
8. Feature work froze for a quarter.
9. Overprovisioned containers were never right-sized.
10. A stateful service was put on Spot and interruptions caused an outage.

**Clusters:**
- **K1, wrong lever / unmeasured bill** (causes 1, 9). Bears on GT-6? and C3.
- **K2, wrong u metric / u drift** (causes 2, 3). Bears on C2 and GT-4?.
- **K3, misapplied discounts** (causes 4, 10). Bears on C4 and GT-5.
- **K4, off-bill costs** (causes 5–8). Bears on C5's [2nd]/[3rd] extension and A7.

**Disposition:**
- **K1, plan change:** C5 step one breaks the bill down by usage type, not just service.
- **K2, plan change:** u is defined as invocation wall-clock time ÷ provisioned seconds. Migrate only below 35% (the low end of the bracket), and use a rollback trigger at breakeven (C5 hops 4–5).
- **K3, plan change:** size the Savings Plan to the measured usage floor, and use Spot only for stateless tasks (C5 hop 3).
- **K4, accepted risk:** mitigated by a single-service pilot with a rollback trigger and total-cost accounting that includes engineer time (C5 hop 5).

**Falsification.** The conclusion is false if a pilot service measured above 48% u produces a lower actual bill on Lambda than on its container.

## §6→§4 closure ledger (process output)

```text
- "Don't start with a Lambda migration… one pilot first" → chain C5 ✓
- "'Serverless is cheaper' is really a claim about idle time…" → chains C1, C2 ✓
- "discount levers… available today with no code change" → chain C4 ✓
- "Measuring first delays savings… two deployment stacks" → chain C5 ✓
- "Pre-check: … Inputs ceiling: MEDIUM" → chains C1–C5 ✓
- "Confidence: MEDIUM…" → chain C5 ✓
```

## Self-audit scan (process output)

| Chain | Chain Head (brief) | Form conforming? | Rule applied | Dependency clean? |
|---|---|---|---|---|
| C1 | GT-1 + GT-2 + GT-3 | yes | n/a | yes |
| C2 | C1 + GT-1 + GT-4? | yes | n/a | yes |
| C3 | GT-6? + C2 | yes | n/a | yes |
| C4 | GT-3 + GT-5 + GT-8 | yes | n/a | yes |
| C5 | C1 + C2 + C3 + C4 | yes | n/a | yes |

| §6 Span (brief) | Construct | Claim under R11? | R11 clause applied | Chain cited |
|---|---|---|---|---|
| Recommended approach | bold lead-in | yes | prescribed lead-in | C5 |
| Key insight | bold lead-in | yes | prescribed lead-in | C1, C2 |
| Fastest safe first move | bold lead-in | yes | bold lead-in whose colon closes the bold span | C4 |
| Trade-offs acknowledged | bold lead-in | yes | prescribed lead-in | C5 |
| Pre-check | bold lead-in | yes | bold lead-in whose colon closes the bold span | C1–C5 |
| Confidence | bold lead-in | yes | bold lead-in whose colon closes the bold span | C5 |

```text
Scan complete: 5 chain rows, one per section-4 chain block in order; 6 section-6 rows, one per construct in order — 6 claims under R11, 0 excluded. 0 chains malformed, 0 claims untraced.
```

## Self-Audit Gate (process output)

**Criterion 1: Identify Essence**
Quoted span: "Which changes to how your services are billed would cut the total AWS bill? And does moving to Lambda cut it at all, given how busy your workloads actually are?"
Band: **Sound**
Justification: The core problem is framed as the bill rather than the migration, and each success criterion names an outcome checkable in §6. But it is stated as two questions rather than a single sentence, which the Rigorous band requires.

**Criterion 2: Challenge Assumptions**
Quoted span: "| C5 | 7 | [3rd] two stacks, off-bill cost | A7 | yes (declared in Phase 2) |"
Band: **Rigorous**
Justification: All rows use the four types, carry token–em-dash verdicts, and several are Challenged or Discarded. The audit covers every chain step, and unverified chain inputs read "unverified — flagged".

**Criterion 3: Establish Ground Truths**
Quoted span: "enumerated GT-4?, GT-6?; list carries `?` on exactly those two; GT-1, GT-2, GT-3 feed C1 (HIGH), GT-3, GT-5, GT-8 feed C4 (HIGH), each with a named read location"
Band: **Rigorous**
Justification: The enumeration matches the list, every unsuffixed GT feeds a HIGH chain with a read location, and a Phase 3 failure record is present for the Lambda Savings Plan discount. (Disclosed residual: four of the read locations came through WebFetch extraction.)

**Criterion 4: Reason Upward**
Quoted span: "| C2 | C1 + GT-1 + GT-4? | yes | n/a | yes |"
Band: **Rigorous**
Justification: All five chains conform and have clean dependencies, the arithmetic recomputes, assumptions are declared inline, no analogy is used as evidence, and §5 carries four structured dead ends.

**Criterion 5: Validate**
Quoted span: "**Confidence:** MEDIUM — Inputs axis. GT-6? closes with Cost Explorer grouped by service and usage type, plus per-service request duration and concurrency metrics over a representative window. C2 is MEDIUM."
Band: **Rigorous**
Justification: Each band matches its axes: HIGH where every input was read, MEDIUM where a `?` input or cited chain caps it. The Conclusion equals its weakest chain, and the adversarial record is complete with a disposition for every cluster.

**Criterion 6: Conclusion-to-Ground-Truth Traceability**
Quoted span: "| Key insight | bold lead-in | yes | prescribed lead-in | C1, C2 |"
Band: **Rigorous**
Justification: All six §6 claims cite chains, and the Key Insight (idle time, not the platform, decides cost) is a finding that "serverless is cheaper" reasoning doesn't reach.

Gate cleared: no Absent verdict, and no criterion scored Hand-wavy.

---

**Connectors:** Gmail, Google Calendar and Google Drive need authorizing in your claude.ai connector settings before they can be used. This analysis didn't need them.