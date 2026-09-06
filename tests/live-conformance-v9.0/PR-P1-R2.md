**Before the analysis — two disclosures required at the top of the response.**

1. **`AskUserQuestion` is unavailable in this session**, so I could not ask for the missing inputs. Per the Input Contract I proceeded best-effort and name here what I could not obtain: your bill's decomposition by service, per-service duty cycle, invocation counts and durations, log volume per invocation, and your existing Savings Plan / RI coverage. Every one of those is a constraint whose value changes the answer's *sign*, not just its magnitude. They are recorded as GT-11 and are what Chain C4 turns on.
2. **Step 0:** no technique-specific trigger phrase fired, so `MODE = full-composer`. All five phases ran; Phase 4 walked all eight companion techniques.

Phase 3 verification opened five sources (AWS Lambda pricing, Fargate pricing, CloudWatch pricing, Lambda quotas, Compute Savings Plans). One read failed to locate its asserted figure and carries a Phase 3 failure record (GT-3).

The six-section analysis document begins after the process output below.

---

## §6→§4 closure ledger (process output)

```text
- "The premise as stated is false: Lambda is not universally cheaper..." → chain C1 ✓
- "Recommended approach: measure the bill and the duty cycles first..." → chain C4 ✓
- "Key insight: the crossover sits at roughly 26-82% duty cycle..." → chain C2 ✓
- "Trade-offs acknowledged: you trade a lower idle cost for a higher busy-rate price..." → chain C3 ✓
- "Pull a 90-day Cost Explorer breakdown by service..." → chain C4 ✓
- "Measure per-service duty cycle before comparing platforms..." → chain C2 ✓
- "Screen each service against the 900-second and 10,240 MB envelope..." → chain C8 ✓
- "Model Provisioned Concurrency into any latency-sensitive target..." → chain C6 ✓
- "Model CloudWatch Logs ingestion into any high-invocation target..." → chain C7 ✓
- "Overall confidence: HIGH on the crossover arithmetic, MEDIUM on your own threshold" → chain C9 ✓
```

Ledger clean: 10 §6 claims, 10 chains cited, 0 cut.

---

## Assumption Audit (process output)

| Chain | Step | Step Text (brief) | Assumption surfaced? | Added to Table? |
|---|---|---|---|---|
| C1 | 1 | 1,769 MB Lambda vs 1 vCPU/2 GB Fargate hourly cost | A10 (configs do equivalent work) | yes |
| C1 | 2 | ratio 2.10x CPU-matched, 2.43x at 2,048 MB | none | n/a |
| C1 | 3 | 2.1-2.4x cannot be cheaper as a general rule | none | n/a |
| C1 | 4 | universal claim false; depends on execution share | none | n/a |
| C2 | 1 | Lambda charge proportional to D, container constant | none | n/a |
| C2 | 2 | equate curves → D* = 41% / 48% | A10 | yes (already) |
| C2 | 3 | request charge lowers D* to 26% at 10 ms | none | n/a |
| C2 | 4 | overprovisioned baseline raises D* to 82% | A6 (containers right-sized) | yes |
| C2 | 5 | Compute SP scales both sides, crossover unmoved | none | n/a |
| C2 | 6 | crossover band 26-82%, central 39-48% | none | n/a |
| C2 | 7 | Lambda lowers cost only below crossover | none | n/a |
| C3 | 1 | swap recovers only idle fraction (1 − D) | none | n/a |
| C3 | 2 | swap pays unit-price premium on busy fraction | A11 (same work either platform) | yes |
| C3 | 3 | ceiling bounded by idle fraction; negative past D* | none | n/a |
| C3 | 4 | irreducible floor is cost of work performed | A17 (cost ≥ work performed) | yes |
| C3 | 5 | storage/transfer/NAT/DB/log lines outside ceiling | none | n/a |
| C3 | 6 | headroom is idle fraction of one line, not the bill | none | n/a |
| C4 | 1 | reachable share unknown; crossover position unknown | none | n/a |
| C4 | 2 | choosing one unmeasured lever over unranked others | A12 (billing detail accessible) | yes |
| C4 | 3 | measurement is prerequisite for ranking | none | n/a |
| C4 | 4 | same measurement scopes the migration | none | n/a |
| C4 | 5 | sequence: measure, harvest, then selectively migrate | none | n/a |
| C5 | 1 | lock weights before scoring | none | n/a |
| C5 | 2 | scores: B 117, C 65, A 64, D 33 | none | n/a |
| C5 | 3 | 52-point lead outside sensitivity band | none | n/a |
| C5 | 4 | C and A one point apart — real near-tie | none | n/a |
| C5 | 5 | near-tie dissolves; B and C compose | none | n/a |
| C6 | 1 | cold starts drive Provisioned Concurrency adoption | A9 (all paths tolerate cold start) | yes |
| C6 | 2 | PC adds $0.030/hr = 61% of container cost | none | n/a |
| C6 | 3 | requests and duration billed on top of PC | none | n/a |
| C6 | 4 | PC tier pays for idle at a higher unit price | none | n/a |
| C6 | 5 | premise contradicted on latency-sensitive paths | none | n/a |
| C7 | 1 | request $2.0e-7 vs log byte $5.0e-10 → 400 bytes | none | n/a |
| C7 | 2 | >400 bytes costs more to observe than to invoke | A13 (per-invocation charges small) | yes |
| C7 | 3 | 512 MB/10 ms/1 KB worked example | none | n/a |
| C7 | 4 | logs 64% of invocation cost, ~6x duration | none | n/a |
| C7 | 5 | GB-second-only model systematically optimistic | none | n/a |
| C8 | 1 | 900 s and 10,240 MB envelope blocks lift-and-shift | A14 (work units fit envelope) | yes |
| C8 | 2 | blocked services need rewrite plus orchestration | A4 (migration cost negligible) | yes |
| C8 | 3 | eligible population is a strict subset, size unknown | none | n/a |
| C8 | 4 | plan not costable until work units measured | none | n/a |
| C9 | 1 | both-sided instrument leaves crossover unmoved | none | n/a |
| C9 | 2 | EC2-only instrument strands committed spend | A8 (no commitment stranded) | yes |
| C9 | 3 | tiered duration moves crossover by unquantified amount | none | n/a |
| C9 | 4 | residuals point in opposite directions | none | n/a |
| C9 | 5 | own crossover must be read off billing console | none | n/a |

46 rows, one per chain per step, in order, no step skipped.

---

## Self-audit scan (process output)

| Chain | Chain Head (brief) | Form conforming? | Rule applied | Dependency clean? |
|---|---|---|---|---|
| C1 | GT-2 + GT-4 + GT-9 | yes | n/a | yes |
| C2 | GT-2 + GT-4 + GT-10 + GT-1 + GT-8 | yes | n/a | yes |
| C3 | GT-10 + GT-2 + C2 | yes | n/a | yes |
| C4 | GT-11 + C3 + C2 | yes | n/a | yes |
| C5 | C4 + C2 + GT-11 | yes | n/a | yes |
| C6 | GT-5 + GT-4 + C2 | yes | n/a | yes |
| C7 | GT-1 + GT-6 + GT-2 | yes | n/a | yes |
| C8 | GT-7 + GT-9 + GT-11 | yes | n/a | yes |
| C9 | GT-3? + GT-12? + C2 | yes | n/a | yes |

| §6 Span (brief) | Construct | Claim under R11? | R11 clause applied | Chain cited |
|---|---|---|---|---|
| "The answer to the question as posed..." | prose | no | prose carrying neither bold colon lead-in nor list marker | n/a |
| "**The premise as stated is false:**" | bold lead-in | yes | bold lead-in whose colon closes the bold span | C1 |
| "**Recommended approach:**" | bold lead-in | yes | prescribed lead-in, always a claim | C4 |
| "**Key insight:**" | bold lead-in | yes | prescribed lead-in, always a claim | C2 |
| "**Trade-offs acknowledged:**" | bold lead-in | yes | prescribed lead-in, always a claim | C3 |
| "**Concrete next steps, in order:**" | bold lead-in | no | section-intro label: colon-terminated span is the whole line, no citation of its own | n/a |
| "Pull a 90-day Cost Explorer breakdown…" | list item | yes | list item closing its own sentence | C4 |
| "Measure per-service duty cycle…" | list item | yes | list item closing its own sentence | C2 |
| "Screen each service against the 900-second…" | list item | yes | list item closing its own sentence | C8 |
| "Model Provisioned Concurrency into…" | list item | yes | list item closing its own sentence | C6 |
| "Model CloudWatch Logs ingestion into…" | list item | yes | list item closing its own sentence | C7 |
| "**Overall confidence:**" | bold lead-in | yes | bold lead-in whose colon closes the bold span | C9 |

Scan complete: 9 chain rows, one per section-4 chain block in order; 12 section-6 rows, one per construct in order — 10 claims under R11, 2 excluded. 0 chains malformed, 0 claims untraced.

---

## Self-Audit Gate verdicts

**Criterion 1: Identify Essence**
Quoted span: "Which lever removes the most dollars from our AWS bill per unit of engineering cost and delivery risk, given that compute-platform choice is only one such lever and its sign depends on measured duty cycle rather than on the platform category?"
Band: **Rigorous**
Justification: single sentence naming the underlying question rather than the triggering event ("migrate to Lambda"), and each of the five success criteria is a scannable pass/fail test against the Conclusion section (e.g. "states a numeric duty-cycle threshold ... not a directional preference").

**Criterion 2: Challenge Assumptions**
Quoted span (Assumption Audit scan): "| C6 | 1 | cold starts drive Provisioned Concurrency adoption | A9 (all paths tolerate cold start) | yes |"
Band: **Rigorous**
Justification: all 17 rows carry a Type from exactly the four-type scheme with matching prescribed treatments, two rows carry a Discard verdict with specific justification (A5, A13), unverified rows read "unverified — flagged", and the audit scan is exhaustive at 46 rows — one per chain per step — with six assumptions surfaced from chain steps and added back.

**Criterion 3: Establish Ground Truths**
Quoted span: enumerated `?`-marked GT-3, GT-12; the Ground Truths list carries `?` on exactly those two of twelve entries, checked entry by entry.
Band: **Rigorous**
Justification: every unsuffixed GT names its read-at-source location (page, table or worked example) and feeds at least one HIGH chain — GT-8 feeds C2, GT-5 feeds C6, GT-6 feeds C7, GT-7 feeds C8 — and GT-3 carries the Phase 3 failure record naming the source opened and why the figure was not located.

**Criterion 4: Reason Upward**
Quoted span (self-audit scan, chain-form table): "| C2 | GT-2 + GT-4 + GT-10 + GT-1 + GT-8 | yes | n/a | yes |"
Band: **Rigorous**
Justification: all nine chain blocks score form-conforming and dependency-clean in the scan, each carries at least one genuine intermediate hop, the Abandoned Reasoning section documents four dead ends in What-was-tried / Why-abandoned / What-it-ruled-out form, and the one analogy-shaped path is recorded there as *rejected* rather than used as evidence.

**Criterion 5: Validate**
Quoted span: "Confidence: MEDIUM — consumes GT-3? and GT-12?; verification is locating the Lambda tiered-duration table and confirming whether EC2 Instance Savings Plans extend to Lambda, which would raise this to HIGH."
Band: **Sound**
Justification: every chain names its weakest link and no chain consuming a `?` input is rated HIGH, but one Conclusion claim — **Overall confidence:** — rests on C9, which is MEDIUM and is covered by neither EXCEPT clause; a single such conclusion bands Sound rather than Rigorous, and no exception is claimed.

**Criterion 6: Conclusion-to-Ground-Truth Traceability**
Quoted span (self-audit scan, claim-inventory table): "| \"**Key insight:**\" | bold lead-in | yes | prescribed lead-in, always a claim | C2 |"
Band: **Rigorous**
Justification: all ten claims trace to a named section-4 chain with zero untraced, the section introduces no claim absent from section 4, and the Key Insight names the crossover threshold — a quantitative result convention does not reach — rather than restating the recommended approach, which is the measurement sequence.

**Gate: PASS.** No criterion Absent; one criterion at Sound, zero at Hand-wavy.

---
---

# First-Principles Analysis: Cutting the AWS Bill

## 1. Problem Essence

**Essence Statement:** Which lever removes the most dollars from our AWS bill per unit of engineering cost and delivery risk, given that compute-platform choice is only one such lever and its sign depends on measured duty cycle rather than on the platform category?

Note what this is *not*. "Migrate our services to Lambda" is a candidate means; "everyone knows serverless is cheaper" is a premise, not a ground truth; and "the fastest path to migrating" is the fastest path to a *migration*, which is a different object from the fastest path to a *saving*. The analysis must answer the second.

**Success criteria** — each checkable by scanning section 6:

1. The Conclusion names a first action executable without any workload data this analysis lacks.
2. The Conclusion states a numeric duty-cycle threshold above which Lambda *increases* compute cost, not a directional preference.
3. The Conclusion states an upper bound on what a compute-platform swap can save, expressed as a fraction of a named line item rather than of the bill.
4. The Conclusion names at least one cost line a Lambda migration cannot reach at all.
5. The Conclusion recommends migrating no named service, because no service's duty cycle was measured.

## 2. Assumptions Table

Two companion techniques fed this table. **Inversion** on "migrating to Lambda will materially cut our bill" produced seven failure-guaranteeing conditions, each converted to the precondition the claim silently depends on (A2, A3, A4, A8, A9, A13, A14). **Fishbone** on "our AWS bill is higher than we want" used the default six-category set and produced candidate causes the compute-platform lever does not touch — *Process*: no tagging discipline, no decommissioning step at service retirement; *Technology*: non-production environments running 24×7, unattached EBS volumes, NAT Gateway per AZ, no VPC endpoints so S3/DynamoDB traffic traverses NAT; *Information*: log retention never expiring; *Resources*: no commitment discounts on steady baseline, no Graviton adoption, no S3 lifecycle policies. Those branches are consolidated into A16.

| Assumption | Type | Treatment | Verdict | Verification |
|---|---|---|---|---|
| A1: "Serverless is cheaper than containers" holds universally | convention | Explicitly challenge before use | **Challenge** — falsified as a universal; C1 shows Lambda at 2.10-2.43x a right-sized container at full duty cycle | GT-2, GT-4, GT-9 read at source; arithmetic in C1/C2 |
| A2: Target services run at low duty cycle | untested belief | Verify, or flag as unverified | **Challenge** — this is the single variable determining the answer's sign | unverified — flagged (GT-11) |
| A3: Compute dominates the AWS bill | untested belief | Verify, or flag as unverified | **Challenge** — C3 shows the swap cannot reach storage, transfer, NAT, database or log lines | unverified — flagged (GT-11) |
| A4: Migration engineering cost is negligible | untested belief | Verify, or flag as unverified | **Challenge** — a real cash cost that must clear the same hurdle as the saving | unverified — flagged |
| A5: "Fastest path to migrating" is the objective | convention | Explicitly challenge before use | **Discard** — the stated goal is cutting the bill; migration speed is a property of one candidate means | Essence Statement, section 1 |
| A6: Current containers are right-sized | untested belief | Verify, or flag as unverified | **Challenge** — if false, C2's crossover is computed against a strawman and rises toward 82% | unverified — flagged; C2 hop 4 quantifies |
| A7: Lambda duration is a flat per-GB-second rate | current constraint | Record expiry conditions | **Challenge** — a tiered structure exists whose thresholds were not located; expires on any AWS re-pricing and above an unlocated monthly aggregate | unverified — flagged (GT-3?) |
| A8: No commitment coverage would be stranded | untested belief | Verify, or flag as unverified | **Challenge** — depends entirely on which instrument is held; Compute SPs cover both platforms, EC2-only instruments may not | unverified — flagged (GT-12?); GT-8 read at source |
| A9: All migrated paths tolerate cold-start latency | untested belief | Verify, or flag as unverified | **Challenge** — surfaced by the second-order pass; if false, Provisioned Concurrency restores time-proportional billing | unverified — flagged; C6 quantifies at $0.030/hr per 2 GB |
| A10: A 2,048 MB Lambda and a 1 vCPU/2 GB Fargate task do equivalent work | untested belief | Verify, or flag as unverified | **Accept** — 1,769 MB equals one vCPU with CPU proportional to memory, making the two comparable within ~16% on CPU | GT-9, Lambda quotas table, read at source |
| A11: The useful work performed is platform-independent | current constraint | Record expiry conditions | **Accept** — holds while application code is unchanged; expires where C8 forces a rewrite | GT-7, read at source |
| A12: Billing detail is accessible to the team | untested belief | Verify, or flag as unverified | **Challenge** — Cost Explorer/CUR access and resource tagging are prerequisites for C4's measurement | unverified — flagged |
| A13: Per-invocation request and log charges are small relative to compute | untested belief | Verify, or flag as unverified | **Discard** — falsified by C7: any invocation emitting >400 bytes of logs costs more to observe than to invoke | GT-1, GT-6 read at source; arithmetic in C7 |
| A14: All work units fit Lambda's execution envelope | untested belief | Verify, or flag as unverified | **Challenge** — unverified per service; GT-7 fixes the ceiling at 900 s and GT-9 at 10,240 MB | unverified — flagged; envelope read at source |
| A15: The AWS bill is the right measure of cost | convention | Explicitly challenge before use | **Challenge** — the second-order pass finds re-coupling and operational burden are costs absent from the bill, so a bill-only metric can register a win while total cost rises | unverified — flagged; second-order pass |
| A16: Idle resources, non-prod environments and log retention are already cleaned up | untested belief | Verify, or flag as unverified | **Challenge** — the fishbone's Process/Technology/Information/Resources branches name these as candidate causes C4's measurement would size | unverified — flagged |
| A17: Cost is bounded below by the work actually performed | physical law | Accept as ground-truth candidate | **Accept** — an accounting identity that does not expire and cannot be negotiated away; promoted into C3's irreducible-floor hop. *Classified physical law for its non-negotiability, not because it is a law of physics* | definitional; C3 |

## 3. Ground Truths

**GT-1** — AWS Lambda on-demand requests: "$0.20 per one million requests" (us-east-1). *Provenance: read-at-source* — aws.amazon.com/lambda/pricing, request-pricing statement.

**GT-2** — AWS Lambda on-demand duration: "$0.0000166667 per GB-s" (us-east-1, x86). *Provenance: read-at-source* — same page, located in the page's worked calculation examples; the headline x86 duration table did not render in the retrieved text.

**GT-3?** — Lambda duration pricing is tiered downward above high monthly aggregate volume; thresholds and per-tier rates unknown. *Provenance: unverified.* **Phase 3 failure record:** aws.amazon.com/lambda/pricing was opened; the page references pricing tiers but the tier table was not located in the retrieved text — `citation does not support the claim` for any specific threshold.

**GT-4** — AWS Fargate (Linux/x86, us-east-1): "CPU cost: $0.000011244 per vCPU second" and "memory cost: $0.000001235 per GB per second". *Provenance: read-at-source* — aws.amazon.com/fargate/pricing, worked example. Hourly equivalents by arithmetic: $0.040478 per vCPU-hour, $0.004446 per GB-hour.

**GT-5** — Lambda Provisioned Concurrency: "$0.0000041667 per GB-s"; "Provisioned Concurrency is calculated from the time you enable it on your function until it is disabled, rounded up to the nearest five minutes"; "When Provisioned Concurrency is enabled and executed for your function, you also pay for Requests and Duration based on the prices below." *Provenance: read-at-source* — aws.amazon.com/lambda/pricing, Provisioned Concurrency section.

**GT-6** — Amazon CloudWatch Logs, standard log class: $0.50 per GB ingested beyond the 5 GB free tier; $0.03 per GB-month archived storage. *Provenance: read-at-source* — aws.amazon.com/cloudwatch/pricing, Examples 9 and following. The page states "pricing varies by Region" and did not render a us-east-1-specific table; the figures are those the page's own worked examples use.

**GT-7** — Lambda function timeout quota: "900 seconds (15 minutes)". *Provenance: read-at-source* — docs.aws.amazon.com/lambda/latest/dg/gettingstarted-limits.html, "Function configuration, deployment, and execution" quota table.

**GT-8** — Compute Savings Plans: "automatically apply to EC2 instance usage regardless of instance family, size, AZ, Region, OS or tenancy, and also apply to Fargate or Lambda usage"; available for "a 1 or 3 year term"; "reduce your costs by up to 66%". *Provenance: read-at-source* — aws.amazon.com/savingsplans/compute-pricing.

**GT-9** — Lambda memory/CPU envelope: "128 MB to 10,240 MB, in 1-MB increments"; "Lambda allocates CPU power in proportion to the amount of memory configured"; "At 1,769 MB, a function has the equivalent of one vCPU." *Provenance: read-at-source* — same quotas table as GT-7.

**GT-10** — Billing-basis asymmetry: Lambda duration is billed per GB-second of *execution*, so its charge is proportional to duty cycle D; Fargate is billed per vCPU-second and GB-second of *task lifetime*, so its charge is independent of D. *Provenance: read-at-source* — both billing bases stated on the two pricing pages read (GT-2, GT-4); the D-proportionality is their definitional consequence, and the irreducibility drill bottoms this branch out at the definition of the two metering units rather than at any further claim.

**GT-11** — No billing decomposition, per-service duty cycle, request rate, invocation duration, log volume, or commitment-coverage data was supplied to this analysis. *Provenance: read-at-source* — the task prompt.

**GT-12?** — EC2 Instance Savings Plans and Reserved Instances do not extend to Lambda or Fargate usage. *Provenance: unverified.* **Phase 3 failure record:** inferred from the Compute Savings Plans page's contrast ("*also* apply to Fargate or Lambda usage", with EC2 Instance Savings Plans described separately at up to 72%); no source stating the exclusion was opened.

**`?`-marked ground truths, enumerated: GT-3, GT-12 (2 of 12).** All ten unsuffixed entries name a read location and each feeds at least one HIGH-confidence chain.

## 4. Derivation Chains

**C1 — the premise as stated is false** *(Confidence: HIGH — all three inputs read at source; the chain consumes no `?` input)*

```text
GT-2 (Lambda duration per GB-second) + GT-4 (Fargate per vCPU-second and per GB-second) + GT-9 (1,769 MB equals one vCPU)
→ a Lambda function sized at 1,769 MB holds one vCPU-equivalent and costs $0.10365 per hour executing continuously, while a Fargate task holding one vCPU and 2 GB costs $0.04937 per hour whether it executes or not [Assumes: A10]
→ at full duty cycle the CPU-matched Lambda is 2.10 times the price of the container it would replace, and a 2,048 MB Lambda at $0.1200 per hour is 2.43 times that price
→ a platform costing between 2.1 and 2.4 times as much for the same continuously-executed work cannot be cheaper as a general rule
→ the claim that serverless is universally cheaper than containers is false as stated, and what it actually depends on is what share of the time the service is executing
```

*Weakest link:* hop 1, which rests on A10 — configuration comparability. GT-9's "one vCPU at 1,769 MB" is what discharges it.

**C2 — the crossover** *(Confidence: HIGH — five read-at-source inputs, no `?` input; the 26% and 82% ends are sizing and invocation-length variations of the same read figures, not separate estimates)*

```text
GT-2 (Lambda per GB-second of execution) + GT-4 (Fargate per vCPU-second and GB-second of task lifetime) + GT-10 (execution-time billing scales with duty cycle, wall-clock billing does not) + GT-1 ($0.20 per one million requests) + GT-8 (Compute Savings Plans cover EC2, Fargate and Lambda alike at up to 66 percent)
→ Lambda's hourly charge is proportional to duty cycle D while the container's hourly charge is constant in D, so the two cost curves cross at exactly one value of D
→ equating $0.1200 × D against $0.04937 for a 2,048 MB function and a right-sized 1 vCPU / 2 GB task puts the crossover at 41 percent, and the CPU-matched 1,769 MB comparison puts it at 48 percent [Assumes: A10]
→ adding the per-request charge lowers the crossover for short invocations, reaching 26 percent at 10 ms per invocation and staying near 41 percent at 1 s per invocation
→ comparing instead against a container overprovisioned by a factor of two raises the crossover toward 82 percent, because an oversized baseline is what the swap would then be beating [Assumes: A6]
→ a Compute Savings Plan applies to both sides of this comparison, so a commitment of that type scales both curves together and leaves the crossover approximately where list prices put it
→ the crossover therefore sits between roughly 26 and 82 percent of duty cycle, with a central band of 39 to 48 percent against a right-sized on-demand container
→ Lambda lowers compute cost only for services measured below their own crossover and raises it for services above, which makes duty cycle the variable the decision turns on
```

*Weakest link:* hop 4 — the 82% upper end rests on A6, which is unverified; the central band 39-48% rests only on read figures. *Estimate-procedure stop criterion:* the bracket straddles the decision threshold and therefore does **not** resolve the migrate/don't-migrate decision universally — which is the finding. It does resolve one thing decisively: at D → 1 the sign is negative.

**C3 — the ceiling a platform swap can reach** *(Confidence: HIGH — arithmetic and definitional given GT-2, GT-4, GT-10)*

```text
GT-10 (container billing is wall-clock, Lambda billing is execution-time) + GT-2 (Lambda unit price per GB-second) + C2 (crossover is duty-cycle dependent)
→ the only quantity a platform swap can recover is the idle fraction of provisioned capacity, which is one minus D of the compute line and nothing else
→ the same swap pays a higher unit price on the busy fraction, so the recoverable amount is the idle fraction minus the unit-price premium applied to D [Assumes: A11]
→ the ceiling on savings from a platform swap alone is bounded above by the compute line's idle fraction, and turns negative once D passes the crossover established in C2
→ beneath that ceiling sits an irreducible floor, the cost of the CPU-seconds and GB-seconds of work actually performed, which no platform choice can go under [Assumes: A17]
→ storage, data transfer, NAT, managed-database and log-retention lines lie entirely outside the quantity this ceiling bounds, so a platform swap cannot move them at all
→ the headroom a Lambda migration addresses is the idle fraction of one line item, not the bill, and its size is the product of that line's share and its idle fraction
```

*Weakest link:* hop 2's premium term, which depends on C2's crossover position. This is the theoretical-limit result: **law-permitted ceiling** = idle fraction of the compute line; **conventional figure** = the whole bill, which is how "migrate to Lambda" is usually spoken about; **the gap** is everything the swap cannot reach.

**C4 — measurement is the prerequisite, not the migration** *(Confidence: HIGH)*

```text
GT-11 (no billing decomposition, duty cycle, request rate or commitment data was supplied) + C3 (the swap reaches only the idle fraction of the compute line) + C2 (crossover is set by measured duty cycle)
→ the share of the bill a Lambda migration can reach is unknown to this analysis, and so is whether any given service sits above or below its own crossover
→ choosing the compute-platform lever now means choosing one lever of unmeasured size over an unranked set of other levers of unmeasured size [Assumes: A12]
→ the measurement that sizes every lever is a prerequisite for ranking any of them, so it is the only action whose expected value is positive before that ranking exists
→ that same measurement is what scopes a migration, because C2 cannot be applied to a service whose duty cycle has never been recorded
→ the sequence that follows is measure the bill and the duty cycles, act on whatever the measurement ranks highest, and migrate only the services the measurement places below their own crossover
```

*Weakest link:* hop 2's dependence on A12 — if billing detail is genuinely inaccessible, obtaining access becomes the first action instead.

**C5 — weighted option comparison** *(Confidence: MEDIUM — the option scores are this analysis's judgement, not measured quantities; the 52-point margin is what makes the ranking robust to those judgements rather than the scores being verified. **This chain is not load-bearing**: its conclusion is not restated in section 6, and it corroborates C4 rather than supporting a presented claim.)*

Criteria and weights, locked before any option was scored:

| Criterion (higher score always better) | Weight |
|---|---|
| Expected reduction in total AWS spend | 5 |
| Time to first realised saving | 4 |
| Evidence-grounding (5 = derivable from data pullable today) | 5 |
| Low engineering effort | 3 |
| Reversibility / low lock-in | 3 |
| Low risk to reliability and latency | 4 |

| Option | Spend | Time | Evidence | Effort | Revers. | Risk | **Total** |
|---|---|---|---|---|---|---|---|
| A — do nothing | 1 | 1 | 1 | 5 | 5 | 5 | **64** |
| B — measure and harvest (right-size, kill waste, commitments, log retention, NAT/VPC endpoints) | 5 | 5 | 5 | 4 | 5 | 5 | **117** |
| C — selective Lambda migration of measured low-duty-cycle services | 3 | 2 | 3 | 2 | 3 | 3 | **65** |
| D — fastest-path full migration to Lambda | 2 | 1 | 1 | 1 | 1 | 2 | **33** |

```text
C4 (measurement is the prerequisite) + C2 (crossover is duty-cycle dependent) + GT-11 (no workload data supplied)
→ locking six weighted criteria before scoring rather than after prevents the weights being reverse-engineered to favour a pre-held preference
→ scoring four options against those locked weights ranks measure-and-harvest at 117, selective migration at 65, doing nothing at 64 and fastest-path full migration at 33
→ the winner leads by 52 points, far outside the roughly ten percent band in which a single weight could flip the result, so the ranking does not turn on any one judgement
→ selective migration and doing nothing land one point apart, which is a real near-tie rather than a scoring artefact, and what it says is that an unsequenced migration is barely better than inaction
→ that near-tie dissolves once the two are recognised as composable rather than exclusive, because measure-and-harvest is what produces the per-service duty-cycle data selective migration needs to be scoped at all
```

*Sensitivity check:* B's margin is 52 points — no single weight change flips it. The A/C near-tie at 64 vs 65 is inside the 10% band and is reported as a real finding rather than refined away.

**C6 — the second-order contradiction** *(Confidence: HIGH — GT-5's price and its billing semantics were both read at source, including "calculated from the time you enable it ... until it is disabled")*

```text
GT-5 (Provisioned Concurrency at $0.0000041667 per GB-second, billed from enable to disable, with Requests and Duration charged on top) + GT-4 (Fargate per vCPU-second and per GB-second) + C2 (crossover is duty-cycle dependent)
→[2nd] cold-start latency on a user-facing path drives adoption of Provisioned Concurrency, which bills from the moment it is enabled until it is disabled rather than per execution [Assumes: A9]
→[2nd] enabling it on a 2 GB function adds $0.030 per hour of reserved capacity, which is 61 percent of the $0.04937 hourly cost of the right-sized container it replaced, before a single invocation is billed
→[3rd] request and duration charges still apply on top of that reserved-capacity charge, so the migrated path pays a time-proportional charge and a usage-proportional charge where the container paid only the first
→[3rd] a Lambda tier running Provisioned Concurrency is paying for idle capacity at a higher unit price, which is precisely the cost structure the migration was undertaken to escape
→ the premise that Lambda removes payment for idle capacity is contradicted on every latency-sensitive path, and that contradiction is what routed assumption A9 back into the Phase 2 table
```

*Weakest link:* hop 1's dependence on A9 — if genuinely no path is latency-sensitive, this chain does not fire. *Second-order routing:* this is a contradicting effect, so it returned to Phase 2 rather than extending forward; A9 is its Phase 2 row.

**C7 — the log-ingestion line the compute model omits** *(Confidence: HIGH — pure arithmetic on three read-at-source figures)*

```text
GT-1 (Lambda $0.20 per one million requests) + GT-6 (CloudWatch Logs ingestion $0.50 per GB) + GT-2 (Lambda duration $0.0000166667 per GB-second)
→[2nd] a request costs 2.0 × 10⁻⁷ dollars to invoke while a byte of emitted log costs 5.0 × 10⁻¹⁰ dollars to ingest, so the two charges are equal at exactly 400 bytes per invocation
→[2nd] any invocation emitting more than 400 bytes of logs therefore costs more to observe than to invoke, and log volume scales with invocation count rather than with execution time [Assumes: A13]
→[3rd] a 512 MB function running for 10 ms and emitting 1 KB of logs pays $0.083 × 10⁻⁶ in duration, $0.200 × 10⁻⁶ in requests and $0.512 × 10⁻⁶ in log ingestion
→[3rd] log ingestion is 64 percent of that invocation's total cost and roughly six times its duration charge, so the line the migration set out to optimise is no longer the dominant one
→ a Lambda cost model built from GB-seconds alone omits the charge that dominates for short high-frequency functions, which makes any such model systematically optimistic
```

*Weakest link:* the 1 KB log-volume figure is an illustrative parameter, not a measured one; the 400-byte break-even is parameter-free and is what the claim rests on.

**C8 — the eligibility envelope** *(Confidence: HIGH — both quota figures read at source)*

```text
GT-7 (Lambda function timeout quota is 900 seconds) + GT-9 (memory 128 MB to 10,240 MB with CPU proportional to memory, one vCPU at 1,769 MB) + GT-11 (no per-service workload data supplied)
→ a service whose unit of work runs longer than 900 seconds cannot be lifted onto Lambda unchanged, and neither can one needing more parallel CPU than a 10,240 MB function provides [Assumes: A14]
→ such a service must be decomposed into orchestrated steps or left on a container platform, which is a rewrite carrying its own engineering cost and its own orchestration charges [Assumes: A4]
→ the population eligible for a lift-and-shift is therefore a strict subset of the fleet whose size is unknown to this analysis
→ a plan whose unit is migrating our services to Lambda cannot be costed at all until each service's actual work unit has been measured against that envelope
```

*Weakest link:* hop 1's dependence on A14, which is precisely what the screening step in section 6 exists to resolve.

**C9 — the two residuals that decide your own threshold** *(Confidence: MEDIUM — consumes GT-3? and GT-12?; verification is locating the Lambda tiered-duration table and confirming whether EC2 Instance Savings Plans extend to Lambda, either of which would raise this to HIGH)*

```text
GT-3? (Lambda tiered duration thresholds not located) + GT-12? (EC2-only commitment instruments assumed not to cover Lambda) + C2 (crossover computed at list on-demand prices)
→ a commitment instrument covering both platforms leaves the crossover unmoved, as C2's fifth hop establishes, so the stranding question turns entirely on which instrument is held
→ an EC2-only instrument, if it does not extend to Lambda, would leave its committed hourly spend billed while the usage backing it moves away [Assumes: A8]
→ Lambda's tiered duration discount, whose thresholds the pricing page did not render when this analysis opened it, moves the crossover in Lambda's favour at high monthly aggregate volume by an amount that could not be quantified here
→ the two residuals point in opposite directions and neither could be closed from the sources this analysis read
→ this organisation's own crossover and its stranding exposure must be read off its billing console and its Savings Plans coverage report rather than derived any further
```

*Weakest link:* both `?` inputs. This chain exists to name what the analysis could not close rather than to close it.

**Pre-mortem (Phase 5 stress test).** Premise: it is nine months later, the migration completed, and the bill went up. Causes written from that stance clustered into three structural weaknesses:

- *The premise was never tested against our own duty cycle.* → **Plan change:** the duty-cycle measurement in section 6 precedes any migration decision.
- *The bill was never decomposed, so the wrong line was optimised.* → **Plan change:** the Cost Explorer breakdown precedes platform work entirely.
- *Migration side-costs were not in the model — Provisioned Concurrency, log ingestion, orchestration for over-900-second work units, stranded commitments.* → **Plan change:** the cost model for any Lambda target must include all four, per C6, C7, C8 and C9.

The item most likely to have been suppressed in a group discussion — and therefore the highest-signal one — is that the migration could complete successfully and still lose money, because "we shipped the migration" and "we cut the bill" are different outcomes and only the first is visible in a project tracker.

## 5. Abandoned Reasoning

**Dead end 1 — producing a dollar figure for the achievable saving.**
*What was tried:* running the estimate procedure to a target saving in dollars or percent.
*Why abandoned:* GT-11 — no billing decomposition, duty cycle or invocation data was supplied, so every factor in the unit-factor product would have been a free parameter. The estimate procedure's decision-resolution stop criterion cannot be met when the bracket is unbounded at both ends.
*What it ruled out:* any recommendation phrased as a target percentage, and it forced the deliverable to be the crossover *rule* (C2) plus a measurement plan (C4) instead of a number.

**Dead end 2 — grounding the recommendation in how comparable organisations fared.**
*What was tried:* reasoning from published Lambda migration outcomes at other companies.
*Why abandoned:* the no-analogies-as-direct-evidence ban. Another organisation's outcome bears on yours only through a named ground truth about *their* duty cycle, bill composition and commitment position — and published case studies do not state those variables, so the analogy would have been standalone justification.
*What it ruled out:* the entire "everyone knows" form of the premise, and it is why A1 is classified **convention** and challenged rather than accepted.

**Dead end 3 — treating Provisioned Concurrency as the fix for cold starts, keeping the migration thesis intact.**
*What was tried:* preserving "migrate everything" by patching the latency objection with Provisioned Concurrency.
*Why abandoned:* C6's arithmetic — the reserved-capacity charge is 61% of the container it replaces *before* any invocation, and requests and duration are billed on top, so the fix reinstates the cost structure the migration was meant to remove.
*What it ruled out:* blanket migration of latency-sensitive paths, and it generated assumption A9.

**Dead end 4 — using a commitment-discounted container baseline for a tighter lower crossover bound.**
*What was tried:* comparing on-demand Lambda against EC2/Fargate under a Savings Plan, which would have put the crossover near 15%.
*Why abandoned:* GT-8, read at source, states Compute Savings Plans "also apply to Fargate or Lambda usage" — so that discount scales *both* sides and cancels, producing no tighter bound. Only an EC2-only instrument would move it, and that is a stranding question rather than a crossover question.
*What it ruled out:* the ~15% figure this analysis would otherwise have published, which is why C2's bracket bottoms out at 26%; it relocated the commitment issue out of C2's bracket and into C9's stranding hop.

## 6. Conclusion

The answer to the question as posed is that the fastest path to migrating and the fastest path to a saving are different paths, and the analysis can determine the second without any data you have not yet supplied.

**The premise as stated is false:** at full duty cycle a Lambda function costs 2.10 to 2.43 times the right-sized container it would replace, so "serverless is cheaper than containers" is not a property of the platforms but a conditional statement about how busy your services are (chain C1).

**Recommended approach:** measure the bill's composition and each service's duty cycle first, act on whatever that measurement ranks highest, and migrate only the services the measurement places below their own crossover — because a lever of unmeasured size cannot be ranked against other levers of unmeasured size, and the same measurement is what scopes a migration in the first place (chain C4).

**Key insight:** the crossover sits between roughly 26% and 82% duty cycle, with a central band of 39-48% against a right-sized on-demand container — below it Lambda cuts compute cost, above it Lambda raises compute cost, and a Compute Savings Plan does not move that line because it applies to both platforms alike (chain C2).

**Trade-offs acknowledged:** a platform swap buys you the idle fraction of your compute line in exchange for a higher unit price on the busy fraction, which means its savings ceiling is bounded by that one line item's idle share rather than by the bill, and it cannot move your storage, data transfer, NAT, managed-database or log-retention lines by a single dollar (chain C3).

**Concrete next steps, in order:**

1. Pull a 90-day Cost Explorer breakdown by service, then by resource within the top three lines, and rank every candidate lever by measured dollars before touching any platform (chain C4).
2. Measure per-service duty cycle — busy CPU-seconds divided by wall-clock seconds — and compare each service against the 39-48% central band before considering it a Lambda candidate (chain C2).
3. Screen each service against the 900-second timeout and the 10,240 MB / 1,769-MB-per-vCPU envelope, because anything outside it is a rewrite rather than a migration and must be costed as one (chain C8).
4. Model Provisioned Concurrency into the cost of any latency-sensitive Lambda target at $0.030 per hour per 2 GB, on top of requests and duration, rather than treating cold starts as a free problem (chain C6).
5. Model CloudWatch Logs ingestion into any high-invocation Lambda target, using the 400-byte-per-invocation break-even against the request charge as the screening test (chain C7).

**Overall confidence:** HIGH on the crossover arithmetic and the platform-swap ceiling, since every figure behind them was read directly from AWS's own pricing and quota pages; MEDIUM on where *your* threshold actually sits, because two residuals remain open — Lambda's tiered duration thresholds (GT-3?), which the pricing page referenced but did not render, and whether an EC2-only commitment instrument would strand on migration (GT-12?), which no source I opened stated. Both are closable by reading your billing console and Savings Plans coverage report, and neither changes the recommended sequence (chain C9).

---

**Residual, disclosed rather than hidden:** Criterion 5 banded **Sound**, not Rigorous, because the **Overall confidence** claim rests on C9, which is MEDIUM. That is the honest state — I could not close GT-3 or GT-12 from the sources available, and no EXCEPT clause covers them.