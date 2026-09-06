Both remaining reads landed with verbatim wording located. Phase 3 verification is complete — one attempted read failed and is recorded below rather than papered over.

---

## §6→§4 closure ledger (process output)

```text
- "Recommended approach: run a bounded measurement and a single-service spike..." → chain C8 ✓
- "Time-box a three-week measurement of where the 48 ms actually goes" → chain C1 ✓
- "Enable HTTP/2 on the existing REST stack and raise connection-pool limits" → chain C2 ✓
- "Staff the on-call rotation independently of this decision" → chain C3 ✓
- "Re-scope any eventual migration to the services the measurement implicates" → chain C4 ✓
- "Key insight: the tail mechanism is separable from the migration" → chain C2 ✓
- "Trade-offs acknowledged: deferral is not free" → chain C8 ✓
- "Deferral carries a political cost with the infra lead" → chain C8 (2nd-order) ✓
- "If measurement shows transport is material, this delays a real win by one quarter" → chain C1 ✓
- "Overall confidence: HIGH" → chains C1, C2, C3, C4, C8 ✓
- "The 30 percent figure is not evidence for or against" → chain C6 ✓
- "The encoding-cost bracket is an estimate, not a measurement" → chain C7 ✓
```

Ledger clean — every §6 claim names a chain, nothing cut.

---

# First-Principles Analysis: gRPC Migration Commitment

## 1. Problem Essence

**Essence Statement:** Is inter-service transport the binding constraint on this platform's latency, and is now the moment to spend roughly 50 engineer-weeks plus an unbounded 22-team coordination cost changing it — when the magnitude of the claimed benefit has never been measured on this system and the rotation that would absorb the resulting operational risk is staffed at three?

The triggering event is the infrastructure lead's proposal. The core decision is a capacity allocation under an unmeasured hypothesis. Those are not the same question, and answering the first does not answer the second.

**Success criteria** — each is checkable by scanning section 6:

- **SC-1:** The Conclusion states the share of the 48 ms median attributable to transport and serialization, or states that share is unmeasured and names the measurement that supplies it.
- **SC-2:** The Conclusion states a decision that stays correct whether the competitor's 30 percent claim is true or false.
- **SC-3:** The Conclusion prices the migration including consumer-side coordination, not the 5×10 build cost alone.
- **SC-4:** The Conclusion addresses the three-person rotation explicitly as blocker, prerequisite, or accepted risk.
- **SC-5:** The Conclusion either selects one of the two offered options or names a third and states why the offered binary is incomplete.

## 2. Assumptions Table

Assumption space enumerated by fishbone (default six-category set: People, Process, Technology and Tools, Environment, Information, Resources) and by inversion on the claim "migrating the six services will materially improve our latency."

| Assumption | Type | Treatment | Verdict | Verification |
|---|---|---|---|---|
| A1. Encoding cost is bounded by parser throughput; propagation is bounded by light speed in fiber | physical law | Accept as ground-truth candidate | Accept — sets the ceiling used in C7 | Definitional; SI constant, dimensional analysis |
| A2. The competitor's 30 percent p99 result transfers to this platform | untested belief | Verify or flag | Discard — no shared property can be named, so it is analogy not evidence | unverified — flagged; benchmark unidentified, Phase 3 failure record on GT-7? |
| A3. The 48 ms median is a real, currently-measured inter-service figure | current constraint | Record expiry conditions | Accept — treated as given per the Input Contract | Expiry: invalid if topology, traffic mix, or instrumentation changes |
| A4. Transport plus serialization is a material fraction of the 48 ms | untested belief | Verify or flag | Challenge — this is the pivot of the whole decision and nobody has measured it | unverified — flagged; drives C1 |
| A5. The current REST stack runs HTTP/1.1, so HTTP/2 multiplexing is a new gain | untested belief | Verify or flag | Challenge — if false, the tail benefit is already banked | unverified — flagged; drives C2 |
| A6. The p99 tail is transport-caused rather than GC, queueing, or downstream | untested belief | Verify or flag | Challenge — competing causes are at least as likely a priori | unverified — flagged |
| A7. 5 engineers × 10 weeks is the full cost of the migration | convention | Challenge before use | Challenge — project estimates conventionally price the producing team only | Refuted by GT-6, which places mandatory work on consumers |
| A8. On-call capacity stays at three through the migration | current constraint | Record expiry conditions | Accept — treated as the present state | Expiry: lifts on hiring or rotation redesign |
| A9. The decision is binary — commit now or wait a year | convention | Challenge before use | Discard — a framing artifact of the question, not a property of the problem | Refuted by C8's dominant third option |
| A10. gRPC uses long-lived multiplexed HTTP/2 connections that pin under L4 balancing | physical law | Accept as ground-truth candidate | Accept — promoted to GT-9 | kubernetes.io 2018-11-07, verbatim passage located |
| A11. HTTP/2 multiplexing removes HTTP/1.1 application-layer head-of-line blocking | physical law | Accept as ground-truth candidate | Accept — promoted to GT-8 | RFC 9113, verbatim passage located |
| A12. All consuming teams can regenerate stubs inside the two-quarter window | untested belief | Verify or flag | Challenge — coordination cost scales with team count, which is unstated | unverified — flagged; drives C4 |
| A13. Protobuf schema-versioning discipline exists across consuming teams | untested belief | Verify or flag | Challenge — a new failure class if absent | unverified — flagged |
| A14. The six services are on the critical path for user-visible latency | untested belief | Verify or flag | Challenge — highest-traffic is not the same as latency-critical | unverified — flagged |
| A15. The 5 engineers are free without displacing higher-value work | untested belief | Verify or flag | Challenge — opportunity cost is the real denominator | unverified — flagged; drives C5 |
| A16. The 48 ms median is representative of the six candidate services | untested belief | Verify or flag | Challenge — surfaced by Assumption Audit at C1 step 4 | unverified — flagged |
| A17. No atomic org-wide cutover is available | untested belief | Verify or flag | Accept — surfaced by Assumption Audit at C3 step 1; near-certain at 22 services | unverified — flagged |
| A18. Encoding cost is roughly constant per call | physical law | Accept as ground-truth candidate | Accept — surfaced by Assumption Audit at C2 step 1; follows from A1 | Dimensional: bytes ÷ throughput has no load term |
| A19. Consumer-side work is coordination-bound rather than effort-bound | untested belief | Verify or flag | Challenge — surfaced by Assumption Audit at C4 step 2 | unverified — flagged |
| A20. 50 engineer-weeks is the platform team's largest discretionary block in the window | untested belief | Verify or flag | Challenge — surfaced by Assumption Audit at C5 step 1 | unverified — flagged |
| A21. Payloads fall within the 1–50 KB bracket | untested belief | Verify or flag | Challenge — surfaced by Assumption Audit at C7 step 4; bracket chosen to span it | unverified — flagged |
| A22. A measurement can complete in a time-box short relative to two quarters | untested belief | Verify or flag | Challenge — surfaced by Assumption Audit at C8 step 2 | unverified — flagged |

## 3. Ground Truths

**Provenance note, stated once:** for GT-1 through GT-6 and GT-13, the cited source is your problem statement, and the read confirms *you asserted the figure* — it is not an independent measurement of your platform. That distinction is why A3 carries expiry conditions rather than being treated as invariant.

1. **GT-1** — 22 internal microservices communicate over REST/JSON. *Source: problem statement, clause "runs 22 internal microservices that talk to each other over REST/JSON." Provenance: read-at-source.*
2. **GT-2** — Peak load is 340,000 requests per minute. *Source: problem statement, clause "handling 340,000 requests per minute at peak." Provenance: read-at-source.*
3. **GT-3** — Median inter-service latency is 48 ms. *Source: problem statement, clause "a median inter-service latency of 48ms." Provenance: read-at-source.*
4. **GT-4** — The proposal is six highest-traffic services, two quarters, 5 engineers, ~10 weeks. *Source: problem statement, clauses "migrate the six highest-traffic services" and "needs 5 engineers for about 10 weeks." Provenance: read-at-source.*
5. **GT-5** — The on-call rotation has 3 people. *Source: problem statement, clause "our on-call rotation currently has only 3 people covering it." Provenance: read-at-source.*
6. **GT-6** — Every consuming team must regenerate client stubs and redeploy. *Source: problem statement, clause "every team that consumes those services would have to regenerate client stubs and redeploy." Provenance: read-at-source.*
7. **GT-7?** — A competitor published a benchmark claiming 30 percent lower p99 latency. *Source: problem statement asserts the claim exists; the benchmark itself is unnamed. Provenance: unverified.* **Phase 3 failure record:** ambiguous citation — no benchmark title, publisher, or URL given, so no source could be located to open.
8. **GT-8** — HTTP/2 carries multiple concurrent streams per connection, and "a blocked or stalled request or response does not prevent progress on other streams"; HTTP/1.1 pipelining "still suffers from application-layer head-of-line blocking." *Source: RFC 9113. Provenance: read-at-source — both passages located verbatim in the retrieved text.*
9. **GT-9** — "HTTP/2 is designed to have a single long-lived TCP connection, across which all requests are multiplexed… connection-level balancing isn't very useful. Once the connection is established, there's no more balancing to be done. All requests will get pinned to a single destination pod." *Source: kubernetes.io blog, 2018-11-07, "gRPC Load Balancing on Kubernetes without Tears." Provenance: read-at-source — passage located verbatim.* **Disclosed first attempt:** `grpc.io/blog/grpc-load-balancing/` was opened first and did not contain the asserted wording; that citation would have carried `?`, so an alternative source was acquired rather than the claim downgraded.
10. **GT-10** — The share of the 48 ms median attributable to transport framing and serialization is stated nowhere in the inputs. *Source: problem statement, by exhaustive scan — no such figure appears. Provenance: read-at-source (absence directly checkable in the prompt).*
11. **GT-11** — Which HTTP version the current REST stack uses is stated nowhere in the inputs. *Source: problem statement, by exhaustive scan. Provenance: read-at-source (absence directly checkable).*
12. **GT-12** — The quoted build cost is 50 engineer-weeks. *Source: arithmetic over GT-4 — 5 engineers × 10 weeks; both factors located in the problem statement. Provenance: read-at-source (derived).*
13. **GT-13** — The number of distinct consuming teams is not stated; only that "every team that consumes those services" is affected. *Source: problem statement, same clause as GT-6. Provenance: read-at-source (the scope is stated, the cardinality is not).*
14. **GT-14?** — Mainstream JSON encode/decode throughput is order 10² MB/s; protobuf order 10³ MB/s. *Source: none opened. Provenance: unverified.* **Phase 3 record:** no read attempted — this GT feeds only the MEDIUM chain C7, whose bracket already spans an order of magnitude in both directions, so under the verification step's own scoping rule it does not earn a read.

**`?`-marked: GT-7, GT-14 (2 of 14).**

## 4. Derivation Chains

**C1 — the benefit's magnitude is undefined, not merely uncertain** *(HIGH)*

```text
GT-3 (48 ms median inter-service latency) + GT-10 (transport share of that median never stated)
→ gRPC changes how bytes are framed and encoded, leaving application time, queueing time and downstream I/O untouched
→ the ceiling on what the migration can remove is therefore the share of the 48 ms spent framing and encoding
→ that share is the one quantity the proposal never states, so the proposal's own upper bound on benefit is undefined
→ committing two quarters now is a wager on a term nobody has measured [Assumes: A16 — the 48 ms median is representative of the six candidate services]
```

*Weakest link:* hop 1's claim that framing and encoding are the only terms gRPC changes. C2 isolates the one further term — multiplexing — and shows it does not rescue the migration.

**C2 — the tail mechanism is separable from the migration** *(HIGH)*

```text
GT-8 (HTTP/2 multiplexes concurrent streams; HTTP/1.1 pipelining still suffers application-layer head-of-line blocking) + GT-11 (current stack's HTTP version never stated)
→ encoding cost is roughly constant per call, so it shifts a distribution's centre rather than its tail [Assumes: A18 — encoding cost is roughly constant per call]
→ head-of-line blocking is load-dependent and bursty, which is the shape that produces a heavy p99 tail
→ the tail mechanism gRPC brings is therefore HTTP/2 multiplexing, not protobuf encoding
→ that mechanism belongs to HTTP/2, which REST and JSON can use directly, so it is separable from gRPC
→ the p99 benefit the migration is bought for is reachable without the migration, by enabling HTTP/2 and raising connection-pool limits
```

*Weakest link:* hop 4's separability holds structurally, but GT-11 means we do not know which branch applies — already on HTTP/2 (benefit banked) or not (benefit cheap). Both branches defeat the migration case.

**C3 — the operational risk lands on a rotation that cannot absorb it** *(HIGH)*

```text
GT-5 (three people on-call across 22 services) + GT-9 (gRPC pins multiplexed requests to a single backend under connection-level balancing) + GT-2 (340,000 requests per minute at peak)
→ consumers cut over on their own schedules, so both stacks run concurrently for the migration's duration [Assumes: A17 — no atomic org-wide cutover is available]
→ the rotation therefore carries REST and gRPC failure modes at the same time rather than in sequence
→ connection pinning is a load-distribution failure that appears under production load, not in staging
→ the six services chosen are the highest-traffic ones, placing new failure modes where blast radius is largest
→ a three-person rotation would absorb a novel load-distribution failure mode on the platform's busiest paths
```

*Weakest link:* GT-9 was observed in a Kubernetes/kube-proxy context; it generalises to any connection-level balancer but the severity depends on your balancing layer, which is unstated.

**C4 — the true elapsed cost exceeds the quoted cost by an unbounded term** *(HIGH)*

```text
GT-4 (five engineers, roughly ten weeks) + GT-6 (every consuming team regenerates stubs and redeploys) + GT-1 (22 services on REST and JSON) + GT-13 (number of consuming teams never stated)
→ the quoted figure prices the producing team only, while mandatory work also lands on every consuming team
→ that consumer work is coordination-bound rather than effort-bound, since no REST endpoint retires until its slowest consumer redeploys [Assumes: A19 — consumer work is coordination-bound]
→ elapsed schedule is therefore set by the slowest of an unstated number of teams
→ the ten-week figure is a lower bound on elapsed time, and the gap to the real figure is unstated
```

*Weakest link:* GT-13 — with a small, co-located consumer set the coordination term could be modest; the point is that it is unpriced, not that it is large.

**C5 — the allocation favours the unmeasured term over the known deficit** *(HIGH)*

```text
GT-12 (50 engineer-weeks) + GT-4 (two-quarter window) + GT-5 (three people on-call across 22 services) + C1 (benefit magnitude unmeasured)
→ 50 engineer-weeks is approximately one engineer-year, and is the platform team's largest discretionary block in the window [Assumes: A20 — this is the largest discretionary block available]
→ spending it on transport leaves every product surface unchanged, so its entire return is the latency term C1 shows is unmeasured
→ the same block could close the rotation deficit, which is a stated present shortfall rather than an unmeasured future gain
→ allocating to the unmeasured term over the known deficit is a choice the proposal makes without naming it
```

*Weakest link:* A20 — if other discretionary capacity exists, the trade is less stark, though the direction of the argument is unchanged.

**C6 — the competitor benchmark is not admissible evidence here** *(MEDIUM)*

```text
GT-7? (competitor benchmark claiming 30 percent lower p99, benchmark itself unidentified) + GT-10 (this platform's transport share never measured)
→ a benchmark result is a fact about the system that was measured, and transfers only through named properties shared with this system
→ the benchmark is unidentified, so its payload sizes, baseline HTTP version, runtimes and balancing topology are all unknown
→ no shared property can be named, so invoking the figure here is reasoning by analogy rather than from a ground truth about the competitor
→ the 30 percent figure sets no expectation for this platform in either direction
```

*Confidence caveat:* MEDIUM because the chain consumes **GT-7?**, unverified — the benchmark could not be located to open. Verification that raises this to HIGH: obtain the named benchmark and read its payload profile, baseline HTTP version, and load-balancing topology.

**C7 — Fermi bound on the encoding term** *(MEDIUM)*

```text
GT-3 (48 ms median inter-service latency) + GT-14? (JSON encode/decode throughput order 10^2 MB/s; protobuf order 10^3 MB/s)
→ the target quantity is milliseconds of median latency removable by an encoding change, rebuilt as payload bytes divided by throughput, summed over encode and decode at both ends
→ at a 5 KB payload and 200 MB/s, one encode or decode costs about 25 microseconds, so four of them cost about 0.1 ms
→ protobuf at roughly ten times that throughput removes about 0.09 ms of the 48 ms median, which is under 0.2 percent
→ bracketing payload from 1 KB to 50 KB and throughput from 50 to 500 MB/s puts the removable share between roughly 0.02 and 2 percent [Assumes: A21 — payloads fall within the 1–50 KB bracket]
→ both ends of that bracket drive the same decision, so the estimate resolves without further tightening
→ a claimed 30 percent gain cannot come from the encoding change, and must, if real, come from the multiplexing term
```

*Confidence caveat:* MEDIUM because the chain consumes **GT-14?**, unverified — no throughput benchmark was opened. Verification that raises this to HIGH: measure your own services' encode and decode cost on real payloads, which is the same instrumentation C8 recommends.

**C8 — the offered binary is incomplete and a third option dominates** *(HIGH)*

```text
C1 (benefit magnitude unmeasured) + C2 (tail mechanism separable from the migration) + C3 (risk lands on a three-person rotation) + C4 (elapsed cost exceeds the quoted cost) + C7 (encoding term bounded near zero)
→ both offered options resolve the central uncertainty by waiting rather than by measuring, so neither changes what is known at the decision point [Assumes: A22 — a measurement completes in a time-box short relative to two quarters]
→ a third option measures the binding term directly, at a cost C7 brackets far below the migration's
→ that option is strictly cheaper than committing and strictly more informative than waiting, so it dominates both on the locked criteria
→ the decision is to run a bounded measurement and a single-service spike, defer the commitment to their result, and staff the rotation independently
→[2nd] deferring on measurement rather than on judgement gives the infra lead a testable proposal, but reads as obstruction if they do not own the measurement
→[2nd] enabling HTTP/2 on the existing REST stack may capture most of the available tail gain and remove the gRPC case entirely
→[3rd] a measurement-gated culture raises platform-wide decision quality, at the cost of a slower path for proposals that are in fact correct
```

*Second-order contradiction check:* no extension step contradicts a Ground Truth. The adverse effect at the first `[2nd]` step is a real cost, routed into section 6 as a named trade-off rather than back to Phase 2.

**Supporting apparatus for C8 — weighted trade-off (not a separate conclusion).** Criteria and weights locked before any option was scored; higher score is always better.

| Criterion | Weight | Commit now | Hold a year | Measure then decide |
|---|---|---|---|---|
| Resolves the benefit uncertainty | 5 | 2 | 1 | 5 |
| Low cost in engineer-weeks | 4 | 1 | 5 | 4 |
| Preserves on-call capacity | 5 | 1 | 5 | 4 |
| Reversibility if wrong | 4 | 1 | 5 | 5 |
| Avoids consumer-team disruption | 3 | 1 | 5 | 5 |
| Preserves infra-lead engagement | 2 | 5 | 1 | 3 |
| Speed to a latency win if one exists | 3 | 3 | 1 | 5 |
| **Weighted total** | | **45** | **90** | **117** |

The 117 vs 90 margin is well outside the 10 percent sensitivity band, so no weight is re-examined post hoc.

## 5. Abandoned Reasoning

**Tried:** scale the competitor's 30 percent figure onto the 48 ms median to compute an expected saving of ~14 ms.
**Why abandoned:** the benchmark is unidentified (GT-7?), so no property shared with this platform can be named — the step is reasoning by analogy used as direct evidence, which the methodology bans.
**What it ruled out:** the 30 percent figure as a planning input in either direction, including as a pessimistic floor.

**Tried:** settle the decision on a straight ROI comparison — 50 engineer-weeks against the expected latency saving.
**Why abandoned:** the intermediate could not be established. The saving depends on GT-10, which is unmeasured, so the comparison has an undefined right-hand side and any number produced would be fabricated precision.
**What it ruled out:** any financial framing of this decision until the measurement exists; it is a decision under structural ignorance, not under quantified risk.

**Tried:** treat the three-person rotation as a hard veto that settles the question by itself.
**Why abandoned:** it proves too much — the same argument blocks every infrastructure change indefinitely, and the rotation deficit is separable from this migration since it should be fixed either way.
**What it ruled out:** staffing as the primary argument. It survives as a risk-pricing input to C3, not as a veto.

**Tried:** recommend a one-service gRPC trial without a pre-registered measurement plan.
**Why abandoned:** it reproduces the original error at smaller scale — a spike with no instrumentation of the transport term yields an anecdote, not a fraction, and the decision would still rest on GT-10 being unknown.
**What it ruled out:** unmeasured spikes. The spike must carry C1's measurement or it is not worth running.

*Pre-mortem findings folded in:* imagining the recommended plan failed at six months surfaced three clusters — deferral-without-a-deadline, ownership vacuum, and political cost. Each is answered by a specific plan element in section 6 (a named decision date, a named owner, and giving the infra lead ownership of the measurement) rather than accepted as unmitigated risk.

## 6. Conclusion

Neither option you offered is the right one, and the reason is structural rather than a matter of taste.

**Recommended approach:** Do not commit now, and do not defer for a year — both resolve the same uncertainty by waiting instead of by measuring; run a time-boxed measurement and a single-service spike, and make the commitment conditional on their result (chain C8).

- Time-box a three-week measurement of where the 48 ms actually goes, decomposed into application time, downstream I/O, queueing, framing, and serialization, with a named owner and a fixed decision date (chain C1).
- Enable HTTP/2 on the existing REST stack and raise connection-pool limits first, since that is where the p99 mechanism actually lives and it costs a rounding error against 50 engineer-weeks (chain C2).
- Staff the on-call rotation independently of this decision, because the deficit is real today regardless of which transport you end up running (chain C3).
- Re-scope any eventual migration to only the services the measurement implicates, rather than to the six with the highest traffic (chain C4).

**Key insight:** The competitor's 30 percent p99 improvement, if it is real, almost certainly came from HTTP/2 multiplexing eliminating head-of-line blocking — not from protobuf encoding — and that mechanism is available to your existing REST/JSON stack without migrating anything, which means the benefit the migration is being bought for is separable from the migration (chain C2).

**Trade-offs acknowledged:** Deferral is not free, and the costs are specific rather than generic (chain C8).

- Deferring carries a political cost with your infrastructure lead, which is why they should own the measurement rather than have it imposed on them — a tested proposal is not a blocked one (chain C8, second-order extension).
- If the measurement does show transport is material, this delays a genuine win by roughly one quarter; that is the price of not spending an engineer-year on an unmeasured term (chain C1).

**Overall confidence:** HIGH — the four chains the recommendation rests on (C1, C2, C3, C4) consume only read-at-source ground truths and carry no `GT-N?` inputs, and C8 aggregates them (chains C1, C2, C3, C4, C8).

The 30 percent figure is not evidence for or against the migration, because the benchmark is unidentified and no property shared with your platform can be named (chain C6). The encoding-cost bracket of 0.02 to 2 percent is a first-principles estimate rather than a measurement of your system, and both ends of it drive the same decision (chain C7).

---

## Assumption Audit scan (process output)

| Chain | Step | Step Text (brief) | Assumption surfaced? | Added to Table? |
|---|---|---|---|---|
| C1 | 1 | gRPC changes framing and encoding only | none | n/a |
| C1 | 2 | ceiling is the framing/encoding share | none | n/a |
| C1 | 3 | that share is never stated | none | n/a |
| C1 | 4 | committing is a wager on an unmeasured term | A16 median representative of six services | yes |
| C2 | 1 | encoding cost constant per call | A18 encoding cost roughly constant | yes |
| C2 | 2 | HOL blocking is load-dependent and bursty | none | n/a |
| C2 | 3 | tail mechanism is multiplexing not encoding | none | n/a |
| C2 | 4 | mechanism belongs to HTTP/2, separable | none | n/a |
| C2 | 5 | p99 benefit reachable without migration | none | n/a |
| C3 | 1 | both stacks run concurrently | A17 no atomic cutover available | yes |
| C3 | 2 | rotation carries both failure sets at once | none | n/a |
| C3 | 3 | pinning appears under production load | none | n/a |
| C3 | 4 | six services are highest blast radius | none | n/a |
| C3 | 5 | three-person rotation absorbs novel failure mode | none | n/a |
| C4 | 1 | quoted figure prices producing team only | none | n/a |
| C4 | 2 | consumer work is coordination-bound | A19 coordination-bound not effort-bound | yes |
| C4 | 3 | schedule set by slowest team | none | n/a |
| C4 | 4 | ten weeks is a lower bound | none | n/a |
| C5 | 1 | 50 EW is largest discretionary block | A20 largest discretionary block | yes |
| C5 | 2 | return is the unmeasured latency term | none | n/a |
| C5 | 3 | same block could close rotation deficit | none | n/a |
| C5 | 4 | allocation choice made without naming it | none | n/a |
| C6 | 1 | benchmark transfers via named shared properties | none | n/a |
| C6 | 2 | benchmark unidentified, properties unknown | none | n/a |
| C6 | 3 | invoking it is reasoning by analogy | none | n/a |
| C6 | 4 | figure sets no expectation either way | none | n/a |
| C7 | 1 | target quantity rebuilt from unit-factors | none | n/a |
| C7 | 2 | 5 KB at 200 MB/s costs ~25 µs per operation | none | n/a |
| C7 | 3 | protobuf removes ~0.09 ms, under 0.2 percent | none | n/a |
| C7 | 4 | bracket gives 0.02 to 2 percent | A21 payloads within 1–50 KB | yes |
| C7 | 5 | both bracket ends drive same decision | none | n/a |
| C7 | 6 | 30 percent cannot come from encoding | none | n/a |
| C8 | 1 | both options wait rather than measure | A22 measurement fits a short time-box | yes |
| C8 | 2 | third option measures the binding term | none | n/a |
| C8 | 3 | third option dominates on locked criteria | none | n/a |
| C8 | 4 | decision is measure, spike, defer, staff | none | n/a |
| C8 | 5 [2nd] | deferral reads as obstruction absent ownership | none | n/a |
| C8 | 6 [2nd] | HTTP/2 may remove the gRPC case entirely | none | n/a |
| C8 | 7 [3rd] | measurement-gated culture raises decision quality | none | n/a |

## Self-audit scan (process output)

| Chain | Chain Head (brief) | Form conforming? | Rule applied | Dependency clean? |
|---|---|---|---|---|
| C1 | GT-3 + GT-10 | yes | n/a | yes |
| C2 | GT-8 + GT-11 | yes | n/a | yes |
| C3 | GT-5 + GT-9 + GT-2 | yes | n/a | yes |
| C4 | GT-4 + GT-6 + GT-1 + GT-13 | yes | n/a | yes |
| C5 | GT-12 + GT-4 + GT-5 + C1 | yes | n/a | yes |
| C6 | GT-7? + GT-10 | yes | n/a | yes |
| C7 | GT-3 + GT-14? | yes | n/a | yes |
| C8 | C1 + C2 + C3 + C4 + C7 | yes | n/a | yes — acyclic, all inputs resolve |

| §6 Span (brief) | Construct | Claim under R11? | R11 clause applied | Chain cited |
|---|---|---|---|---|
| "Neither option you offered is the right one…" | prose | no | prose carrying neither a bold colon lead-in nor a list marker | n/a |
| "Recommended approach: Do not commit now…" | bold lead-in | yes | prescribed lead-in, colon closes bold span, text follows on same line | C8 |
| "Time-box a three-week measurement…" | list item | yes | list item running past forty characters | C1 |
| "Enable HTTP/2 on the existing REST stack…" | list item | yes | list item running past forty characters | C2 |
| "Staff the on-call rotation independently…" | list item | yes | list item running past forty characters | C3 |
| "Re-scope any eventual migration…" | list item | yes | list item running past forty characters | C4 |
| "Key insight: The competitor's 30 percent…" | bold lead-in | yes | prescribed lead-in, colon closes bold span | C2 |
| "Trade-offs acknowledged: Deferral is not free…" | bold lead-in | yes | prescribed lead-in, colon closes bold span | C8 |
| "Deferring carries a political cost…" | list item | yes | list item running past forty characters | C8 (2nd-order) |
| "If the measurement does show transport is material…" | list item | yes | list item running past forty characters | C1 |
| "Overall confidence: HIGH…" | bold lead-in | yes | bold lead-in, colon closes bold span, carries own citation | C1, C2, C3, C4, C8 |
| "The 30 percent figure is not evidence…" | prose | no | prose carrying neither a bold colon lead-in nor a list marker; caveat names its chain inline | C6 |

```text
Scan complete: 8 chain rows, one per section-4 chain block in order; 12 section-6 rows, one per construct in order — 10 claims under R11, 2 excluded. 0 chains malformed, 0 claims untraced.
```

## Self-Audit Gate

**Criterion 1: Identify Essence**
Quoted span: "Is inter-service transport the binding constraint on this platform's latency, and is now the moment to spend roughly 50 engineer-weeks plus an unbounded 22-team coordination cost changing it — when the magnitude of the claimed benefit has never been measured on this system and the rotation that would absorb the resulting operational risk is staffed at three?"
Band: **Rigorous**
Justification: a single sentence naming the allocation decision rather than the triggering proposal, with five success criteria each carrying a verb-subject-outcome test scannable against section 6.

**Criterion 2: Challenge Assumptions**
Quoted span: "| C1 | 4 | committing is a wager on an unmeasured term | A16 median representative of six services | yes |"
Band: **Rigorous**
Justification: the Assumption Audit scan carries one row per chain per step across all 39 steps in order, and every surfaced assumption (A16–A22) was added to the table with a four-type classification, prescribed treatment, em-dash-justified verdict, and either a specific verification or "unverified — flagged."

**Criterion 3: Establish Ground Truths**
Quoted span: enumeration check — the analysis enumerates GT-7 and GT-14; reading the list, `?` appears on exactly GT-7 and GT-14 and on no other entry, and the stated count of 2 matches the enumeration's length.
Band: **Rigorous**
Justification: every GT carries a stable ID, a citation more specific than "common knowledge," and a provenance label; the two `?` entries are enumerated by ID and match the list; each unsuffixed GT feeding a HIGH chain names its read location (prompt clause, RFC section, or blog passage), and the two Phase 3 failure records name their source and reason.

**Criterion 4: Reason Upward**
Quoted span: "| C8 | C1 + C2 + C3 + C4 + C7 | yes | n/a | yes — acyclic, all inputs resolve |"
Band: **Rigorous**
Justification: all eight chain blocks score conforming with clean dependencies in the self-audit scan; separately, the Abandoned Reasoning section documents four dead ends in What-was-tried / Why-abandoned / What-it-ruled-out form with structural reasons (analogy-as-evidence, undefined intermediate, proves-too-much, reproduces-the-error), and the competitor benchmark is explicitly discarded as analogy rather than used as evidence.

**Criterion 5: Validate**
Quoted span: "MEDIUM because the chain consumes **GT-7?**, unverified — the benchmark could not be located to open. Verification that raises this to HIGH: obtain the named benchmark and read its payload profile, baseline HTTP version, and load-balancing topology."
Band: **Rigorous**
Justification: every chain names its weakest link; both `GT-N?`-consuming chains (C6, C7) are rated MEDIUM with a caveat naming the specific unverified input and the verification that raises it; no chain consuming a `?` input is rated HIGH; and every section-6 claim rests on at least one HIGH chain, so the aggregate HIGH rating matches. No EXCEPT clause is claimed.

**Criterion 6: Conclusion-to-Ground-Truth Traceability**
Quoted span: "10 claims under R11, 2 excluded. 0 chains malformed, 0 claims untraced."
Band: **Rigorous**
Justification: the claim-inventory table shows every one of the ten section-6 claims citing a named section-4 chain with none untraced; separately, the Key Insight — "that mechanism is available to your existing REST/JSON stack without migrating anything" — names a non-obvious finding that neither the analogy nor the convention reaches, rather than restating the recommended approach.

**Gate result: cleared.** No criterion scored Absent; zero criteria scored Hand-wavy, so the cap is clear. No re-entry edge fired — no Fix/Repeat pass was needed, no Criterion 1 return to Phase 1, and no mid-run input re-open. Nothing was omitted from the six-section output or from either scan.

---

## What this means in practice

The short version: **your infrastructure lead may be right about the destination and is definitely wrong about the order of operations.**

The proposal asks you to spend an engineer-year to change a term whose size nobody has measured. gRPC can only remove time your system actually spends framing and encoding bytes — it cannot touch application logic, queueing, or downstream I/O. Nobody has told you what fraction of your 48 ms that is, and a back-of-envelope rebuild puts the encoding portion somewhere between 0.02 and 2 percent. A 30 percent improvement cannot come from there.

If the competitor's number is real, it came from HTTP/2 multiplexing killing head-of-line blocking — and you can have that on your existing REST/JSON stack by enabling HTTP/2 and raising your connection pool limits. That is days of work, not two quarters, and it is the single highest-leverage thing to try first.

Meanwhile the migration would introduce gRPC's connection-pinning behaviour under connection-level load balancing onto your six busiest services, during a period when both stacks run at once, absorbed by three on-call engineers. That risk is unpriced in the proposal.

Three concrete asks, in order:

1. Instrument where the 48 ms goes. Three weeks, one named owner, a fixed decision date. Give this to the infrastructure lead — it tests their proposal rather than blocking it.
2. Enable HTTP/2 on the REST stack and raise pool limits. Measure p99 before and after. This may end the conversation entirely.
3. Fix the on-call rotation regardless of the outcome. It is a real deficit today and it is not contingent on this decision.

Then decide — and if the measurement implicates transport, migrate only the services it names, not all six.