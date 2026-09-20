I have everything the methodology requires. Both Phase 3 reads landed, and one of them cuts directly against the proposal's own premise.

---

## Process disclosures (read first)

**A re-entry edge fired.** The Phase 4 second-order pass produced a third-order effect — a translating hop at the REST/gRPC boundary — that **contradicts C3's premise that the migration is confined to framing and encoding**. Per the second-order procedure, that routed the conclusion **back to Phase 2 for re-challenging**. What changed: two assumptions (A21, A22) were added to the Classified Assumptions Table, A21 was **Discarded**, and chain C8 carries the contradiction explicitly. This edge has now fired its one permitted re-perception pass.

**Nothing was omitted.** The closure ledger, the self-audit scan and the Self-Audit Gate all ran; the output template and validation rubric both read successfully.

**Phase 4 technique sweep (full-composer, all eight).** Five-whys (reduce-to-primitives) decomposed the 48 ms median → C4. Fishbone mapped the p99 cause space across six categories; only one branch of ~18 is touched by gRPC. Inversion produced six unverified preconditions → A3, A5, A24, A27, A33, A36. Estimate produced C4's bracket. Theoretical-limit derived the intra-datacenter RPC floor at ~0.05 ms — a ~1000× gap to 48 ms, >99.9% of it convention rather than physics — recorded but **not** promoted to a chain (Dead End 5). Trade-off produced C7. Second-order produced C8's extension and the Phase 2 return. Pre-mortem is the Phase 5 adversarial pass.

---

# 1. Problem Essence

**Core problem:** Whether the transport layer a gRPC migration would replace is where this platform's latency actually lives — and whether a three-person on-call rotation can absorb a two-quarter, twenty-two-service-wide change — rather than whether to start that migration now or in a year.

**Success criteria** (each scannable against section 6 without interpretation):

- **SC1** — The Conclusion names the specific latency statistic the decision turns on and states whether this platform has measured it.
- **SC2** — The Conclusion attributes the p99 tail to a cause this analysis can point at, or states explicitly that no such attribution exists.
- **SC3** — The Conclusion gives the on-call rotation a disposition that does not depend on the gRPC decision.
- **SC4** — The Conclusion carries a named trigger condition and a date, not a now/later verdict alone.
- **SC5** — The Conclusion's recommended action costs fewer engineer-weeks than the ~50 the migration would cost.

The question as posed ("now or in a year?") is a framing artifact: it presupposes the migration is the right intervention and only its timing is open. That presupposition is the assumption most in need of challenge.

---

# 2. Assumptions Table

| Assumption | Type | Treatment | Verdict | Verification |
|---|---|---|---|---|
| A1 There is a latency problem here worth ~50 engineer-weeks | untested belief | Verify or flag | **Challenge** — no SLO, error budget or user-facing symptom is named anywhere in the input | unverified — flagged (GT-15) |
| A2 p99 inter-service latency is the metric that matters here | untested belief | Verify or flag | **Challenge** — the only figure supplied is a median | unverified — flagged (GT-14) |
| A3 A competitor's 30% p99 result transfers to this platform | untested belief | Verify or flag | **Discard** — transfer requires matched workload, payload size, concurrency and baseline, none supplied; using it directly is reasoning by analogy, barred as direct evidence | unverified — flagged (GT-7?) |
| A4 The 48 ms median is dominated by transport and serialization | untested belief | Verify or flag | **Discard** — contradicted by C4's bracket of 0.4%–8% | unverified — flagged |
| A5 The p99 tail is dominated by application-layer connection queueing | untested belief | Verify or flag | **Challenge** — this is the one mechanism gRPC addresses, and nothing in the input confirms or excludes it | unverified — flagged |
| A6 gRPC is carried over HTTP/2 | untested belief | Verify | **Accept** — read at source | grpc/grpc `PROTOCOL-HTTP2.md`, §"gRPC over HTTP2"; promoted to GT-8 |
| A7 Protobuf is materially cheaper than JSON for *these* payloads | untested belief | Verify or flag | **Challenge** — protobuf is the default (GT-9) but the advantage depends entirely on payload shape | unverified — flagged |
| A8 5 engineers × 10 weeks is accurate | untested belief | Verify or flag | **Challenge** — an estimate, not a measurement; treated as a floor | unverified — flagged (GT-4?) |
| A9 On-call load is unchanged during the migration | untested belief | Verify or flag | **Discard** — a dual-stack period widens the incident surface while the system is being changed | unverified — flagged |
| A10 A 3-person rotation is adequate today | untested belief | Verify or flag | **Challenge** — ~1 week in 3 per engineer, with no depth for leave, illness or departure | unverified — flagged (GT-5?) |
| A11 Consumers will regenerate stubs on the platform team's schedule | untested belief | Verify or flag | **Challenge** — a cross-team dependency the platform team does not control | unverified — flagged (GT-6?) |
| A12 REST/JSON is required rather than merely established | convention | Challenge before use | **Discard** — it is a convention; its incumbency is not an argument for keeping it, and inertia is cited nowhere in these chains | challenged; no chain rests on REST's incumbency |
| A13 The six highest-traffic services are the right six to change | untested belief | Verify or flag | **Challenge** — traffic volume is not latency contribution | unverified — flagged |
| A14 Headcount and budget are fixed over the two-quarter window | current constraint | Record expiry | **Accept** — expires at the next hiring or budget cycle; until then the 5 engineers are genuinely zero-sum | stated in the input |
| A15 The migration is phased, not a flag day | untested belief | Verify or flag | **Accept** — a two-quarter phased migration entails a dual-stack period | unverified — flagged |
| A16 Waiting a year is costless | untested belief | Verify or flag | **Discard** — a real problem would persist all year, and C1 shows nobody would know either way | unverified — flagged |
| A17 Queueing delay grows without bound as utilization → 1 | physical law | Accept as GT candidate | **Accept** — standard queueing result | carried as GT-13? — no text opened by this analysis |
| A18 Serialization cost is bounded below by payload size and memory bandwidth | physical law | Accept as GT candidate | **Accept** — used only to bound C4's factors, not to assert a figure | dimensional reasoning |
| A19 HTTP/2 does not address TCP head-of-line blocking | untested belief | Verify | **Accept** — read at source | RFC 9113 §1; promoted to GT-11 |
| A20 An improvement matters only above the measurement noise floor | physical law | Accept as GT candidate | **Accept** — used in C4's decision-resolution step | statistical |
| **A21 The migration is architecturally neutral — transport only, no coupling change** | untested belief | Verify or flag | **Discard** — contradicted by GT-6?; mandatory stub regeneration across every consumer is a lockstep release dependency | surfaced by the Phase 4 second-order pass; unverified — flagged |
| **A22 A partially migrated estate needs no translating hop at the boundary** | untested belief | Verify or flag | **Challenge** — 16 of 22 stay on REST; each boundary needs dual-stack endpoints or a hop, and a hop adds latency to the targeted calls | surfaced by the same pass; unverified — flagged |
| A23 grpc.io's introduction is where a performance claim would appear | untested belief | Verify or flag | **Challenge** — other gRPC pages and the project blog were not swept | unverified — flagged |
| A24 The current REST stack is HTTP/1.1, not already HTTP/2 | untested belief | Verify or flag | **Challenge** — if already HTTP/2, GT-10's mechanism is captured and the tail case collapses | unverified — flagged |
| A25 gRPC adds no latency-relevant behaviour beyond framing and encoding | untested belief | Verify or flag | **Challenge** — flow control, deadlines and default retry policy are all latency-relevant | unverified — flagged |
| A26 JSON encode/decode throughput is 100 MB/s–1 GB/s | untested belief | Verify or flag | **Challenge** — assumed range, not measured here; bracketed rather than pointed | unverified — flagged |
| A27 Payloads are 1–50 KB and connections are pooled in one datacenter | untested belief | Verify or flag | **Challenge** — the single factor C4 is most sensitive to | unverified — flagged |
| A28 Encode/decode and transit are additive, not overlapped | untested belief | Verify or flag | **Accept** — additivity is the conservative direction; it enlarges the transport share and C4 survives the bracket's upper end | unverified — flagged |
| A29 Connection queueing would be bursty rather than sustained | untested belief | Verify or flag | **Challenge** — a sustained bottleneck would move the median too, which the input cannot settle | unverified — flagged |
| A30 On-call is weekly with no secondary tier or follow-the-sun | untested belief | Verify or flag | **Challenge** — the roster was not supplied | unverified — flagged |
| A31 The 5 migration engineers overlap the on-call pool | untested belief | Verify or flag | **Challenge** — plausible on a 22-service platform team, not stated | unverified — flagged |
| A32 Three weeks suffices for decision-quality attribution | untested belief | Verify or flag | **Challenge** — the recommendation's own timebox; pre-mortem Cluster 2 names how it fails | unverified — flagged |
| A33 The six in-scope services are called from outside the six | untested belief | Verify or flag | **Challenge** — a call-graph-closed set would make the boundary cost vanish | unverified — flagged |
| A34 Schema changes are frequent enough for lockstep cost to be real | untested belief | Verify or flag | **Challenge** — a stable schema makes A21's coupling cost largely theoretical | unverified — flagged |
| A35 A translating hop is chosen over dual-stack endpoints | untested belief | Verify or flag | **Challenge** — dual-stack avoids the hop at the cost of maintaining both | unverified — flagged |
| A36 Deployed server/client libraries can enable HTTP/2 without code change | untested belief | Verify or flag | **Challenge** — C9's entire cost advantage depends on it | unverified — flagged |

**Fishbone (Phase 2, default six-category set) — the p99 cause space.** *People:* on-call depth, remediation latency. *Process:* no per-hop attribution, no SLO, peak-window deploys. *Technology:* connection-pool exhaustion, GC pauses, cold-pool TLS handshakes, retry storms, thread-pool saturation, serialization. *Environment:* cross-AZ hops, noisy neighbours, service-discovery lookups. *Information:* no p99 captured, no payload-size distribution, no fan-out map. *Resources:* cgroup CPU throttling, pool sizing, DB connection limits. **Roughly eighteen candidate branches; gRPC touches one and a half of them.**

---

# 3. Ground Truths

- **GT-1?** The estate is 22 internal microservices communicating over REST/JSON — *unverified:* user-supplied architecture figure; no service registry or call graph opened by this analysis.
- **GT-2?** Peak throughput is 340,000 requests per minute (≈5,667/s) — *unverified:* user-supplied; no telemetry export opened.
- **GT-3?** Median inter-service latency is 48 ms — *unverified:* user-supplied; no latency histogram or dashboard opened.
- **GT-4?** Proposed scope is 6 of 22 services, 5 engineers × 10 weeks (≈50 engineer-weeks) across two quarters — *unverified:* an estimate, not a measurement.
- **GT-5?** The on-call rotation covering these services has 3 people — *unverified:* user-supplied; no roster opened.
- **GT-6?** Every consuming team must regenerate client stubs and redeploy — *unverified:* stated as a requirement; the dependency map was not inspected.
- **GT-7?** A competitor's public benchmark claims 30% lower p99 latency under gRPC — **Phase 3 failure record: ambiguous citation.** The source is named only as "a competitor's public benchmark"; no document, URL, workload description, payload distribution or methodology was supplied, so the cited source could not be located or opened.
- **GT-8** gRPC's wire protocol is carried over HTTP/2 framing — source: grpc/grpc `doc/PROTOCOL-HTTP2.md`; *read-at-source:* §"gRPC over HTTP2", opening line: "This document serves as a detailed description for an implementation of gRPC carried over HTTP2 framing."
- **GT-9** gRPC uses Protocol Buffers as its default serialization mechanism — source: grpc.io "Introduction to gRPC"; *read-at-source:* §"Working with Protocol Buffers": "By default, gRPC uses Protocol Buffers, Google's mature open source mechanism for serializing structured data".
- **GT-10** HTTP/2 permits multiple concurrent requests over one TCP connection; HTTP/1.0 allowed one outstanding request per connection and HTTP/1.1 pipelining "still suffers from application-layer head-of-line blocking" — source: RFC 9113; *read-at-source:* §1 (Introduction).
- **GT-11** TCP head-of-line blocking is **not** addressed by HTTP/2 — source: RFC 9113; *read-at-source:* §1: "Note, however, that TCP head-of-line blocking is not addressed by this protocol."
- **GT-12** grpc.io's "Introduction to gRPC" page states no performance or efficiency claim — source: grpc.io "Introduction to gRPC"; *read-at-source:* whole page checked for such wording, none located.
- **GT-13?** Queueing delay rises without bound as utilization approaches 1 — *unverified:* standard queueing result, but no text was opened by this analysis.
- **GT-14** The input supplies a median latency and no percentile — source: the problem statement as supplied; *read-at-source:* "a median inter-service latency of 48ms", with no p50/p95/p99 distribution given.
- **GT-15** The input names the competitor benchmark as the sole stated justification; no SLO, error budget, or user-facing symptom is named — source: the problem statement as supplied; *read-at-source:* "citing a competitor's public benchmark claiming 30 percent lower p99 latency".

**Provenance summary.**
`?`-marked: **GT-1, GT-2, GT-3, GT-4, GT-5, GT-6, GT-7, GT-13 (8 of 15).**
Read-at-source (unsuffixed GTs feeding HIGH-confidence chains): **GT-8** — `PROTOCOL-HTTP2.md` §"gRPC over HTTP2", opening line; **GT-9** — grpc.io §"Working with Protocol Buffers"; **GT-10** — RFC 9113 §1; **GT-11** — RFC 9113 §1; **GT-12** — grpc.io Introduction, full page, no such wording located; **GT-14** — the problem statement as supplied; **GT-15** — the problem statement as supplied.

---

# 4. Derivation Chains

### Conclusion C1: The migration currently has no measured justification originating on this platform.

```text
GT-15 (benchmark is the sole stated justification) + GT-14 (input supplies a median, no percentile) + GT-12 (grpc.io introduction states no performance claim)
→ the only justification on offer is external to this platform and was produced by measuring a different system
→ the statistic the proposal promises to move has never been measured on this platform at all *[Assumes: A2 — that p99 is the metric that matters here]*
→ the protocol's own introductory documentation states no performance claim the external justification could anchor to *[Assumes: A23 — that the introduction page is where such a claim would appear]*
→ the decision as posed rests on no measurement of this system and on no claim the protocol's own documentation makes
```

**Confidence:** HIGH — every head input is read-at-source (GT-12 at grpc.io's Introduction, whole page checked with no such wording located; GT-14 and GT-15 at the problem statement as supplied), and the chain asserts only what those three records contain.

### Conclusion C2: The competitor's 30% figure can carry no weight in this decision at any confidence level.

```text
GT-7? (competitor p99 claim, citation unlocatable) + C1 (no measurement of this platform exists)
→ the benchmark's workload, payload-size distribution, concurrency level and HTTP/1.1 baseline configuration are all undescribed
→ a result measured on an undescribed system cannot bound the same statistic on a second undescribed system
→ the 30% figure is therefore an analogy, which this methodology bars from standing as direct evidence *[Assumes: A3 — that no matched-workload evidence exists that would convert it into a ground truth]*
→ the figure is inadmissible as a justification for committing engineering capacity
```

**Confidence:** MEDIUM — GT-7? is unverified; the Phase 3 verification step could not open it because the citation names no document, URL, workload or methodology, and its Phase 3 failure record gives the reason as an ambiguous citation. Supplying the benchmark's URL, payload-size distribution, concurrency level and HTTP/1.1 baseline configuration would remove GT-7? as a cause of the downgrade. C1 is cited on the head and rated HIGH, so it imposes no ceiling.

### Conclusion C3: gRPC's latency mechanism is confined to framing and encoding, and the specification itself excludes TCP-level tail effects.

```text
GT-8 (gRPC carried over HTTP/2 framing) + GT-9 (protobuf is the default serialization) + GT-10 (HTTP/2 multiplexes concurrent requests on one connection) + GT-11 (TCP head-of-line blocking not addressed by HTTP/2)
→ the migration changes exactly two things on the wire: the framing layer and the message encoding *[Assumes: A24 — that the current REST stack is HTTP/1.1 and not already HTTP/2]*
→ its one genuine tail-latency mechanism is the removal of application-layer head-of-line blocking and connection-count pressure
→ the specification itself excludes TCP-level head-of-line blocking from what that change fixes
→ any p99 improvement must come from application-layer connection queueing or from encoding size, and from nothing else *[Assumes: A25 — that gRPC adds no latency-relevant behaviour beyond framing and encoding]*
```

**Confidence:** HIGH — all four head inputs are read-at-source (GT-8 at `PROTOCOL-HTTP2.md` §"gRPC over HTTP2"; GT-9 at grpc.io §"Working with Protocol Buffers"; GT-10 and GT-11 at RFC 9113 §1), and the chain asserts only what those specifications state.

### Conclusion C4: Transport plus serialization can account for at most a few percent of the stated 48 ms median.

```text
GT-3? (48 ms median inter-service latency) + C3 (change confined to framing and encoding)
→ target quantity: milliseconds per call attributable to JSON encode and decode plus intra-datacenter transit
→ encode and decode across a 1-50 KB payload at 100 MB/s-1 GB/s, four times per round trip, brackets to 0.004-2 ms *[Assumes: A26, A27 — assumed throughput and payload ranges, not measured here]*
→ intra-datacenter transit on a pooled connection brackets to 0.2-2 ms
→ the two factors sum to 0.2-4 ms against a 48 ms median, a central estimate near 0.5 ms *[Assumes: A28 — that the two are additive rather than overlapped]*
→ transport plus serialization is 0.4%-8% of the median budget, so removing all of it would move 48 ms to between 47.8 ms and 44 ms
→ both ends of the bracket drive the same decision, so the estimate is resolved and needs no tightening
```

**Confidence:** MEDIUM — GT-3? is unverified; the 48 ms median is user-supplied with no telemetry, dashboard or trace export opened by this analysis, and exporting the platform's own latency histogram would remove it as a cause of the downgrade. The chain carries a second downgrade cause of its own: the JSON-throughput and payload-size factors (A26, A27) are assumed ranges rather than measurements of this platform, and measuring the actual payload-size distribution and encode/decode cost on the six services would remove that cause. C3 is cited on the head and rated HIGH, imposing no ceiling.

### Conclusion C5: C4 bounds the median and leaves the p99 the proposal is actually about entirely unevaluated.

```text
GT-14 (input supplies a median, no percentile) + GT-2? (340,000 requests per minute at peak) + GT-13? (queueing delay unbounded as utilization approaches 1) + C4 (transport is 0.4%-8% of the median) + C3 (one tail mechanism remains open)
→ the figure this platform has measured and the figure the proposal claims to improve are different statistics
→ at roughly 5,700 requests per second, one call in a hundred is about 57 calls every second sitting in the tail
→ queueing delay rises without bound as utilization approaches one, so a tail can be generated by load concentration alone *[Assumes: A29 — that the queueing is bursty rather than sustained]*
→ a bound on the median budget therefore says nothing about a tail generated by queueing rather than by per-call work
→ the connection-queueing mechanism C3 leaves open is exactly the mechanism that produces a tail without moving a median
→ the proposal is not refuted by C4, it is unevaluated, and nothing in this analysis or in the proposal can evaluate it
```

**Confidence:** MEDIUM — GT-2? and GT-13? are unverified: GT-2? is a user-supplied throughput figure that a telemetry export would settle, and GT-13? is a standard queueing result for which no text was opened, which opening a queueing-theory reference would settle. C4 is cited on the head and rated MEDIUM, which caps this chain. C5's own downgrade cause is that it asserts a gap in the evidence rather than a measured value; capturing a p99 histogram with per-hop attribution at peak would remove that cause by replacing the gap with a figure.

### Conclusion C6: The 3-person on-call rotation is a standing operational risk independent of the gRPC question, and any migration aggravates it.

```text
GT-5? (3-person on-call rotation) + GT-4? (5 engineers for 10 weeks) + GT-6? (every consumer regenerates stubs and redeploys)
→ a 3-person rotation puts each engineer on call roughly one week in three, with no depth if one is on leave, ill or departs *[Assumes: A30 — a weekly rotation with no secondary tier]*
→ a phased migration runs two protocol stacks at once, widening the incident surface precisely while the system is being changed *[Assumes: A15 — phased rather than flag-day]*
→ the same migration diverts five engineers for ten weeks, and those engineers are the plausible source of rotation depth *[Assumes: A31 — that the five overlap the on-call pool]*
→ the staffing risk is load-bearing on its own and is aggravated, not created, by the migration
```

**Confidence:** MEDIUM — GT-5?, GT-4? and GT-6? are all unverified user-supplied operational figures, with no roster, staffing plan or service-dependency map opened by this analysis; producing the on-call roster, the staffing plan for the ten weeks, and the consumer dependency list would remove all three as causes of the downgrade.

### Conclusion C7: Buying the attribution dominates both committing now and holding a year.

```text
C2 (the stated justification carries no weight) + C5 (the relevant statistic is unevaluated) + C6 (staffing risk is independent) + GT-4? (about 50 engineer-weeks of scope)
→ three options survive: commit now, hold a year, or measure the attribution first and gate the migration on it
→ scored against seven criteria weighted before any option was scored, weighted totals are measure-first 125, hold-a-year 83, commit-now 35, out of 130
→ the spread is driven by the two criteria weighted 5, addressing a measured cause and preserving operational safety, on which committing now scores 1 and 1
→ dropping the measured-cause criterion entirely still leaves measure-first at 100 against 78 and 30, so the result is not an artefact of that one weight
→ recommend a bounded measurement with a pre-committed decision date, in place of both the migration and the deferral *[Assumes: A32 — that three weeks suffices for decision-quality attribution]*
```

**Trade-off matrix** (weights locked at step 3, before any option was scored; higher is better throughout):

| Criterion | Weight | A: commit now | B: hold a year | C: measure first |
|---|---|---|---|---|
| Addresses a measured cause | 5 | 1 → 5 | 1 → 5 | 5 → 25 |
| Preserves operational safety | 5 | 1 → 5 | 4 → 20 | 5 → 25 |
| Cost-efficiency per unit confirmed benefit | 4 | 1 → 4 | 3 → 12 | 5 → 20 |
| Reversibility / optionality | 4 | 2 → 8 | 5 → 20 | 5 → 20 |
| Low cross-team coordination burden | 3 | 1 → 3 | 5 → 15 | 4 → 12 |
| Speed to a decision-quality answer | 3 | 2 → 6 | 1 → 3 | 5 → 15 |
| Preserves architectural flexibility | 2 | 2 → 4 | 4 → 8 | 4 → 8 |
| **Total** | **26** | **35** | **83** | **125** |

*Weight rationale, recorded before scoring:* criteria 1 and 2 carry 5 because the stated motivation is unmeasured and the rotation is below any redundancy floor — the two conditions under which a wrong decision is expensive and hard to reverse. Criteria 3 and 4 carry 4 because ~50 engineer-weeks is a large, sticky commitment. Criteria 5 and 6 carry 3: real but recoverable. Criterion 7 carries 2: transport lock-in moves slowly.

**Confidence:** MEDIUM — C2, C5 and C6 are all cited on the head and all three are rated MEDIUM, which caps this chain; GT-4? is unverified as stated in C6. C7's own downgrade cause is that the option scores are judgements rather than measurements, and re-running the scoring with the platform team assigning scores against the already-locked weights would remove that cause.

### Conclusion C8: Mandatory stub regeneration makes the migration an increase in coupling, not a neutral transport swap.

```text
GT-6? (every consumer regenerates stubs and redeploys) + GT-1? (22 services, six in scope) + C3 (change confined to framing and encoding)
→ sixteen of twenty-two services stay on REST, so every boundary between the two sets needs dual-stack endpoints or a translating hop *[Assumes: A33 — that the six are called from outside the six]*
→ a shared schema whose change forces every consumer to regenerate and redeploy is a lockstep release dependency across team boundaries *[Assumes: A34 — that schema changes are frequent enough to matter]*
→[2nd] the estate's independent deployability falls during and after the migration, which is the property a 22-service split exists to provide
→[3rd] a translating hop at the boundary adds latency to exactly the calls the migration was meant to speed up *[Assumes: A35 — that a translating hop is chosen over dual-stack endpoints]*
→[3rd] that added hop contradicts C3's premise that the change is confined to framing and encoding, so this conclusion routed back to Phase 2 for re-challenging, producing A21 (Discard) and A22 (Challenge)
```

**Confidence:** MEDIUM — GT-6? and GT-1? are unverified user-supplied architecture figures, with no service-dependency map or call graph opened by this analysis; producing the call graph and confirming which of the 22 services consume the six in scope would remove both as causes of the downgrade. C3 is cited on the head and rated HIGH, imposing no ceiling.

### Conclusion C9: HTTP/2 on the existing REST stack captures C3's one genuine tail mechanism without the migration.

```text
C3 (the tail mechanism is application-layer connection queueing) + C8 (stub regeneration is what creates the coupling cost) + GT-10 (HTTP/2 multiplexes concurrent requests on one connection)
→ the multiplexing that removes application-layer head-of-line blocking is a property of HTTP/2, not of protobuf and not of gRPC's service definitions
→ the coupling cost C8 identifies comes entirely from the generated-stub contract, which HTTP/2 alone does not introduce
→ enabling HTTP/2 on the existing REST stack therefore tests the same mechanism without any consumer stub regeneration *[Assumes: A36 — that deployed server and client libraries support HTTP/2 without code change]*
→ if the attribution implicates connection queueing, this is the intervention to try before any protocol migration
```

**Confidence:** MEDIUM — C8 is cited on the head and rated MEDIUM, which caps this chain; C3 is HIGH and GT-10 is read-at-source, so neither contributes a downgrade. C9's own downgrade cause is A36, the assumption that the deployed server and client libraries can enable HTTP/2 without code change; confirming HTTP/2 support in the deployed libraries for the six services would remove that cause, and it is the cheapest assumption in this analysis to check.

---

# 5. Abandoned Reasoning

### Dead End 1: Verifying the competitor benchmark

**What was tried:** Locating and opening the cited 30%-lower-p99 benchmark in order to promote GT-7? to read-at-source.
**Why abandoned:** The citation is ambiguous — it names "a competitor's public benchmark" with no document, URL, workload, payload distribution, concurrency level or baseline configuration. A different benchmark found by search would not be the cited one, so a search result could not have verified the claim; it would have substituted one unverified figure for another while appearing to resolve it.
**What it ruled out:** The 30% figure cannot be made load-bearing at any confidence level, and no amount of further searching changes that — only the infra lead producing the specific document does.

### Dead End 2: Grounding the decision in industry practice

**What was tried:** Arguing from the prevalence of gRPC in large microservice estates ("Google uses it internally", "it is the industry direction").
**Why abandoned:** This is reasoning by analogy, which this methodology bars as direct evidence. Admitting it would require a verified ground truth about those estates' call-graph shape, payload-size distribution and fan-out depth — none of which is available, and all of which are exactly the variables that decide whether the analogy transfers.
**What it ruled out:** No conclusion here rests on anyone else's adoption, so "everyone is moving to gRPC" is not a counter-argument to this analysis; it is the argument this analysis declined to make.

### Dead End 3: Deriving a p99 from the 48 ms median

**What was tried:** Estimating p99 by assuming a distribution shape — the common p99 ≈ 3–5× median heuristic — so that C4's bracket could be applied to the tail directly.
**Why abandoned:** Service-latency distributions are heavy-tailed and that multiplier varies by more than an order of magnitude across real systems. Any figure derived this way would be manufactured precision, and it would have become the single load-bearing number in the analysis.
**What it ruled out:** There is no analytical shortcut from the median you have to the p99 you need. This is precisely why C7 recommends buying the measurement rather than deriving it.

### Dead End 4: Answering the now-or-later binary as posed

**What was tried:** Scoring "commit now" against "hold a year" as a two-option trade-off.
**Why abandoned:** The binary presupposes the migration is the right intervention and only its timing is open — the assumption most in need of challenge (Phase 1). A two-option matrix would have produced "hold a year" at 83 vs 35 and presented deferral as the finding, when deferral scores badly on the criterion that matters most (it learns nothing, scoring 1 on the weight-5 measured-cause criterion).
**What it ruled out:** "Hold off another year" is not the right answer either, and an analysis that accepted the framing would have recommended it.

### Dead End 5: Reasoning from the theoretical latency floor

**What was tried:** A theoretical-limit derivation — intra-datacenter propagation at ~2/3 c over 100–300 m, plus ~1–5 µs per switch hop across a 3-hop leaf-spine path, plus kernel/NIC/userspace overhead — putting the law-permitted floor for one intra-DC RPC on the order of tens of microseconds, ~0.05 ms. Against the 48 ms median that is a gap of roughly 1000×, of which >99.9% is convention (application work, waits, fan-out depth) rather than physics.
**Why abandoned as a recommendation:** The gap is real and it reframes the problem usefully, but this analysis has no information about what the 48 ms is actually spent on. Any redesign recommendation built on it would rest on GT-13? and nothing else — an intermediate that could not be established.
**What it ruled out:** It rules out treating 48 ms as a natural floor that only a faster protocol can improve; it does *not* license a rearchitecture recommendation. The finding survives as context for the attribution measurement, not as a conclusion.

---

## Assumption Audit (process output)

| Chain | Step | Step Text (brief) | Assumption surfaced? | Added to Table? |
|---|---|---|---|---|
| C1 | 1 | only justification is external | none | n/a |
| C1 | 2 | statistic never measured here | A2 | yes |
| C1 | 3 | protocol docs state no claim | A23 | yes |
| C1 | 4 | rests on no measurement | none | n/a |
| C2 | 1 | benchmark's conditions undescribed | none | n/a |
| C2 | 2 | undescribed cannot bound undescribed | none | n/a |
| C2 | 3 | figure is an analogy | A3 | yes |
| C2 | 4 | inadmissible as justification | none | n/a |
| C3 | 1 | changes framing and encoding only | A24 | yes |
| C3 | 2 | one genuine tail mechanism | none | n/a |
| C3 | 3 | spec excludes TCP HOL | none | n/a |
| C3 | 4 | improvement from queueing or encoding only | A25 | yes |
| C4 | 1 | target quantity named | none | n/a |
| C4 | 2 | encode/decode brackets 0.004–2 ms | A26, A27 | yes |
| C4 | 3 | transit brackets 0.2–2 ms | none | n/a |
| C4 | 4 | sums to 0.2–4 ms | A28 | yes |
| C4 | 5 | 0.4%–8% of median | none | n/a |
| C4 | 6 | bracket ends agree, estimate resolved | none | n/a |
| C5 | 1 | different statistics | none | n/a |
| C5 | 2 | ~57 tail calls per second | none | n/a |
| C5 | 3 | queueing unbounded as ρ→1 | A29 | yes |
| C5 | 4 | median bound says nothing about tail | none | n/a |
| C5 | 5 | queueing produces tail without moving median | none | n/a |
| C5 | 6 | unevaluated, not refuted | none | n/a |
| C6 | 1 | one week in three, no depth | A30 | yes |
| C6 | 2 | dual stack widens incident surface | A15 (already in table) | referenced |
| C6 | 3 | five engineers are the depth source | A31 | yes |
| C6 | 4 | risk aggravated, not created | none | n/a |
| C7 | 1 | three options survive | none | n/a |
| C7 | 2 | weighted totals 125 / 83 / 35 | none | n/a |
| C7 | 3 | spread driven by the two weight-5 criteria | none | n/a |
| C7 | 4 | sensitivity: ranking holds at 100 / 78 / 30 | none | n/a |
| C7 | 5 | recommend bounded measurement | A32 | yes |
| C8 | 1 | sixteen stay on REST, boundary needs a bridge | A33 | yes |
| C8 | 2 | shared schema is a lockstep dependency | A34 | yes |
| C8 | 3 | [2nd] independent deployability falls | none | n/a |
| C8 | 4 | [3rd] translating hop adds latency | A35 | yes |
| C8 | 5 | [3rd] contradicts C3, routed to Phase 2 | A21, A22 | yes |
| C9 | 1 | multiplexing is an HTTP/2 property | none | n/a |
| C9 | 2 | coupling comes from the stub contract | none | n/a |
| C9 | 3 | HTTP/2-on-REST tests same mechanism | A36 | yes |
| C9 | 4 | try it before a protocol migration | none | n/a |

42 rows, one per chain per step, in order.

---

## Adversarial pass (process output)

Phase 5 stress-tests the **recommendation this analysis makes**, not the gRPC plan it declines to endorse. The conclusion is a plan, so the pre-mortem procedure applies (inversion stress-tests a claim; pre-mortem stress-tests a plan).

**Premise.** It is six months from now. We did not commit to the migration; we ran the measurement and said we would fix on-call. **That plan has failed badly.** What caused it?

**Causes** (unfiltered, written before grouping, from five named viewpoints):

*Platform engineer who ran the measurement* — the tracing instrumentation itself added overhead and changed the profile we were measuring; sampling was head-based at 1%, which drops precisely the tail we were after; we instrumented the six services but not their downstream dependencies, so attribution stopped at the boundary; adding tracing to six services needed the same consumer coordination we were trying to avoid, and took nine weeks not three; the measurement window fell in a quiet quarter and never saw 340k rpm.

*Infrastructure lead whose proposal was deferred* — the attribution confirmed transport was ~1%, everyone agreed, and then nobody did anything about the 99%, so latency was identical a year later; "measure first" became the standing answer to every infrastructure proposal and the platform ossified; I left, and the will to do any transport work left with me; we lost the two-quarter window and the five engineers were committed elsewhere by the time we decided.

*Budget owner* — we spent three weeks measuring and two quarters not deciding; the deferral had no expiry and quietly became permanent; the on-call fix was approved in principle and never staffed because it needed headcount, not reassignment; a customer-visible latency incident in month four produced a post-mortem reading "we knew about this and chose to measure."

*Consumer team that has to live with it* — nothing changed for us; we still cannot tell whether a slow call is our fault or theirs, because the tracing never reached our client side.

*Competitor who benefits* — they shipped the transport work and we shipped a document; two of their engineers were ours, and they left because the interesting infrastructure project kept getting deferred.

**Clusters.**

**Cluster 1 — The deferral has no expiry.** *(absorbs: "measure first became the standing answer", "deferral became permanent", "lost the two-quarter window", "engineers committed elsewhere", "the lead left")* — bears on **C7**.
**Disposition (named plan change):** the recommendation now carries a hard decision date and a pre-committed branch. The measurement completes within three weeks of start; within one week of completion the team commits **in writing** to one of exactly three outcomes — migrate what the attribution implicates, apply the cheaper fix it implicates, or close the question for twelve months with a written rationale. There is no fourth outcome, and "keep measuring" is explicitly not one.

**Cluster 2 — The measurement is built to miss the very thing it is for.** *(absorbs: "1% head-based sampling missed the tail", "instrumentation overhead changed the profile", "attribution stopped at the boundary", "quiet-quarter window", "tracing never reached the client side")* — bears on **C5**, **C7**, **GT-14**.
**Disposition (named plan change):** the measurement specification is fixed up front rather than left to the implementer — tail-biased or unsampled collection for the window, not head-based 1%; the window must include a peak period matching GT-2?'s 340k rpm; attribution must span the full call graph including the sixteen unmigrated services and client-side timing at the consumer; and the deliverable is a per-hop breakdown of the **p99 path**, not another median dashboard.

**Cluster 3 — Attribution is not improvement.** *(absorbs: "transport was 1% and nobody did anything about the 99%", "latency unchanged a year later", "consumers still cannot localise a slow call")* — bears on **C4**, **C5**, **C9**.
**Disposition (named plan change):** the deliverable is ranked by **addressable** latency, not merely attributed latency, and the same one-week decision window commits the team to the single largest addressable item — which, on C4's bracket, is very unlikely to be transport. The tracing capability is retained as a permanent platform asset with consumer-side client instrumentation in scope.

**Cluster 4 — The on-call fix is load-bearing and is the item most likely to be silently dropped.** *(absorbs: "approved in principle, never staffed", "needed headcount not reassignment", "incident in month four", "post-mortem said we knew")* — bears on **C6**, **GT-5?**.
**Disposition (named plan change):** the rotation is decoupled from the gRPC decision entirely and given its own owner and its own date. It is not a rider on the measurement. A 3-person rotation is a standing operational risk whether or not any migration happens, and **this recommendation is invalid as a package if only the cheap half of it is executed.**

**Cluster 5 — The human cost of deferring the interesting work.** *(absorbs: "engineers wanted the infrastructure project", "two of them left", "the lead read it as obstruction", "the next proposal routes around the process")* — bears on **C7**, and on the second-order effects the Phase 4 pass surfaced.
**Disposition (explicitly accepted risk with a named mitigation):** deferring a proposal the infra lead is invested in carries real retention and political cost, and this analysis accepts it rather than pretending it away. **Mitigation:** the infra lead owns the measurement — the proposal's author gets the instrument that can vindicate it, on a three-week clock, with Cluster 1's pre-committed decision date so the outcome is a decision rather than an indefinite hold. If the attribution implicates transport, the migration proceeds at the lead's original scope and this analysis's objection is withdrawn.

**Weakest link, per chain.**

- **C1** — the third hop rests on A23; other gRPC pages and the project blog were not swept.
- **C2** — argues from an absence; if the benchmark is produced and its workload matches, the chain collapses.
- **C3** — A24. **If the platform already runs HTTP/2 under REST, the migration's only tail mechanism is already captured and this chain's "one genuine mechanism" is zero.** This is the highest-value thing to check in the entire analysis.
- **C4** — A27, the payload-size range. At 500 KB payloads the serialization term grows tenfold and the upper bracket reaches ~8 ms; still under 17% of the median, but no longer negligible.
- **C5** — an absent-fails derivation in form (it establishes the proposal is *unevaluated*, not wrong), and its strength depends on A29; sustained rather than bursty queueing would show in the median.
- **C6** — A31. If the five migration engineers are disjoint from the on-call pool, the chain's third hop weakens, though the 1-in-3 rotation risk stands alone.
- **C7** — criterion 1 ("addresses a measured cause", weight 5) arguably favours any information-gathering option by construction. The sensitivity hop answers this by dropping the criterion entirely and showing the ranking holds; that hop exists because of this objection.
- **C8** — A34, schema-change frequency. A stable schema makes the lockstep coupling cost largely theoretical.
- **C9** — A36, HTTP/2 support in the deployed libraries; the cheapest assumption here to check and the one that most changes the recommendation if false.

---

## §6→§4 closure ledger (process output)

```text
- "Do not commit the five engineers now, and do not simply defer for a year either" → chains C1, C7 ✓
- "Staff the on-call rotation to at least five, decoupled from the gRPC question" → chain C6 ✓
- "Instrument a peak-window p99 attribution across the full call graph" → chains C5, C3 ✓
- "Within one week of the attribution landing, commit in writing to one of three outcomes" → chain C7 ✓
- "If the attribution implicates connection queueing, enable HTTP/2 on the existing REST stack first" → chains C3, C9 ✓
- "The one mechanism by which the migration could move p99 is a property of HTTP/2, not of gRPC" → chains C3, C9 ✓
- "This defers rather than rejects the migration" → chains C3, C5, C8 ✓
- "MEDIUM — seven of nine chains are rated MEDIUM" → chains C2, C4, C5, C6, C7, C8, C9 ✓
```

Ledger clean — eight §6 claims, eight chain references, no cuts.

---

## Self-audit scan (process output)

| Chain | Chain Head (brief) | Form conforming? | Rule applied | Dependency clean? |
|---|---|---|---|---|
| C1 | GT-15 + GT-14 + GT-12 | yes | n/a | yes |
| C2 | GT-7? + C1 | yes | n/a | yes |
| C3 | GT-8 + GT-9 + GT-10 + GT-11 | yes | n/a | yes |
| C4 | GT-3? + C3 | yes | n/a | yes |
| C5 | GT-14 + GT-2? + GT-13? + C4 + C3 | yes | n/a | yes |
| C6 | GT-5? + GT-4? + GT-6? | yes | n/a | yes |
| C7 | C2 + C5 + C6 + GT-4? | yes | n/a | yes |
| C8 | GT-6? + GT-1? + C3 | yes | n/a | yes |
| C9 | C3 + C8 + GT-10 | yes | n/a | yes |

| §6 Span (brief) | Construct | Claim under R11? | R11 clause applied | Chain cited |
|---|---|---|---|---|
| "Do not commit… do not simply defer…" | bold lead-in | yes | prescribed lead-in `**Recommended approach:**`, always a claim | C1, C7 |
| "The proposal is not refuted by this analysis…" | prose | no | prose carrying neither a bold colon lead-in nor a list marker | n/a |
| "**The plan, in the order it should run:**" | bold lead-in | no | section-intro label — colon-terminated span is the whole line, no citation of its own | n/a |
| "Staff the on-call rotation to at least five…" | list item | yes | list item closing its own sentence, past forty characters | C6 |
| "Instrument a peak-window p99 attribution…" | list item | yes | list item closing its own sentence, past forty characters | C5, C3 |
| "Within one week of the attribution landing…" | list item | yes | list item closing its own sentence, past forty characters | C7 |
| "If the attribution implicates connection queueing…" | list item | yes | list item closing its own sentence, past forty characters | C3, C9 |
| "The one mechanism by which…" | bold lead-in | yes | prescribed lead-in `**Key insight:**`, always a claim | C3, C9 |
| "This defers rather than rejects…" | bold lead-in | yes | prescribed lead-in `**Trade-offs acknowledged:**`, always a claim | C3, C5, C8 |
| "MEDIUM — seven of nine chains…" | bold lead-in | yes | bold lead-in whose colon closes the bold span, content follows | C2, C4, C5, C6, C7, C8, C9 |

```text
Scan complete: 9 chain rows, one per section-4 chain block in order; 10 section-6 rows, one per construct in order — 8 claims under R11, 2 excluded. 0 chains malformed, 0 claims untraced.
```

---

# 6. Conclusion

**Recommended approach:** Do not commit the five engineers now, and do not simply defer for a year either — buy the measurement that decides the question, on a three-week clock with a pre-committed decision date (chains C1, C7).

The proposal is not refuted by this analysis. It is unevaluated, and the cheapest thing available is the evidence that would evaluate it.

**The plan, in the order it should run:**

- Staff the on-call rotation to at least five people, with its own owner and its own date, decoupled entirely from the gRPC question (chain C6).
- Instrument a peak-window p99 attribution across the full call graph — tail-biased or unsampled, including consumer-side client timing (chains C5, C3).
- Within one week of the attribution landing, commit in writing to one of exactly three outcomes: migrate what the data implicates, apply the cheaper fix it implicates, or close the question for twelve months (chain C7).
- If the attribution implicates application-layer connection queueing, enable HTTP/2 on the existing REST stack before considering any protocol migration (chains C3, C9).

**Key insight:** The one mechanism by which this migration could genuinely move p99 — removal of application-layer head-of-line blocking — is a property of HTTP/2, not of gRPC, so it is obtainable without protobuf, without generated stubs, and without a single consumer redeploying; and the specification the proposal leans on states in its own introduction that it does not address TCP-level head-of-line blocking at all (chains C3, C9).

**Trade-offs acknowledged:** This defers rather than rejects the migration and accepts that a genuine tail problem, if one exists, persists through the measurement window; C3 establishes exactly one mechanism by which the migration could still pay off, and the recommendation is built to find out rather than to foreclose it, at the cost of an accepted retention and political risk with the infra lead — mitigated by giving that lead ownership of the measurement (chains C3, C5, C8).

**Confidence:** MEDIUM — seven of nine chains are rated MEDIUM (chains C2, C4, C5, C6, C7, C8, C9) and the Conclusion inherits the weakest contributing chain; every operational figure this recommendation rests on is user-supplied and unverified (GT-1?, GT-3?, GT-4?, GT-5?, GT-6?), and exporting the platform's own latency histogram, on-call roster, staffing plan and service call graph would remove all five as causes of the downgrade. The Conclusion's own downgrade cause is that its central recommendation is a judgement about how much attribution three weeks buys (A32), which only running the measurement settles.

---

## Self-Audit Gate

**Criterion 1: Identify Essence**
Quoted span: *"Whether the transport layer a gRPC migration would replace is where this platform's latency actually lives — and whether a three-person on-call rotation can absorb a two-quarter, twenty-two-service-wide change — rather than whether to start that migration now or in a year."*
Band: **Rigorous**
Justification: a single sentence naming the underlying question rather than the triggering event, explicitly displacing the prompt's own framing, with five success criteria each carrying a verb + subject + outcome triplet checkable by scanning section 6 (SC1–SC5 are all satisfied there).

**Criterion 2: Challenge Assumptions**
Quoted span (Assumption Audit scan): *"| C8 | 5 | [3rd] contradicts C3, routed to Phase 2 | A21, A22 | yes |"*
Band: **Rigorous**
Justification: all 36 rows carry a Type from exactly the four-type scheme with the prescribed treatment, verdicts lead with Accept/Challenge/Discard followed by an em-dash and a specific justification, chain-used unverified assumptions read "unverified — flagged", and the audit scan covers all 42 chain steps in order, with A21/A22 demonstrably added by the scan rather than pre-existing.

**Criterion 3: Establish Ground Truths**
Quoted span: enumeration check — enumerated GT-1, GT-2, GT-3, GT-4, GT-5, GT-6, GT-7, GT-13; the Ground Truths list carries `?` on exactly those eight and on no others (count 8 of 15 agrees with the enumeration).
Band: **Rigorous**
Justification: IDs are stable and match section 4's references; all seven unsuffixed GTs name a read-at-source location and each feeds a HIGH-confidence chain (GT-8/9/10/11 → C3, GT-12/14/15 → C1); GT-7?'s Phase 3 failure record names the source and the reason (ambiguous citation), invoking **Exception (a) unreachable source**, which confines it to MEDIUM chains; no Discard-verdict assumption appears in the list.

**Criterion 4: Reason Upward**
Quoted span (self-audit scan, chain-form table): *"| C5 | GT-14 + GT-2? + GT-13? + C4 + C3 | yes | n/a | yes |"* — and, for the limbs the table carries no column for, from section 5: *"Why abandoned: This is reasoning by analogy, which this methodology bars as direct evidence."*
Band: **Rigorous**
Justification: all nine chain blocks score form-conforming and dependency-clean with no cycles and every input resolving; every conclusion in sections 4 and 6 has exactly one chain; every chain carries at least one genuine intermediate; five structured dead ends use the What-was-tried / Why-abandoned / What-it-ruled-out form with specific structural reasons; the analogy ban is honoured explicitly (Dead End 2, A3); and every step introducing a new assumption carries its inline `[Assumes: X]`.

**Criterion 5: Validate**
Quoted span: *"Staff the on-call rotation to at least five people, with its own owner and its own date, decoupled entirely from the gRPC question (chain C6)."*
Band: **Sound**
Justification: the adversarial pass ran with a complete record (past-tense premise, unfiltered five-viewpoint cause list written before grouping, five clusters each citing the chain and GT ids it bears on, and per cluster a named plan change or an explicitly accepted risk with a named mitigation), every chain has a named weakest link, and every MEDIUM line names its `GT-N?` inputs, its below-HIGH `Cn` citations and its own downgrade causes with verification paths — but **one Conclusion claim (the on-call staffing item) rests on no HIGH-confidence chain**, which the descriptor bands Sound rather than Rigorous. **Exception (c) absent-fails** is claimed for C5, whose named false assumption is A4 ("the 48 ms median is dominated by transport and serialization", Discarded) and which establishes what does not follow rather than what does; it remains MEDIUM on that basis.

**Criterion 6: Conclusion-to-Ground-Truth Traceability**
Quoted span (self-audit scan, claim-inventory table): *"| 'The one mechanism by which…' | bold lead-in | yes | prescribed lead-in `**Key insight:**`, always a claim | C3, C9 |"* — and, for the restatement limb, from section 6: *"the one mechanism… is a property of HTTP/2, not of gRPC, so it is obtainable without protobuf, without generated stubs, and without a single consumer redeploying."*
Band: **Rigorous**
Justification: all eight section-6 claims trace to specific named chains with zero untraced, no claim introduces reasoning absent from section 4, and the Key Insight names a non-obvious finding — that the migration's sole tail mechanism is separable from the migration — rather than restating the recommended approach, which is to buy a measurement.

**Gate result: PASS.** No criterion Absent; exactly one criterion below Sound is zero, and one criterion at Sound with none at Hand-wavy. No Fix/Repeat pass was required, so the Self-Audit Gate's re-entry edge did not fire.

---

**The short answer:** neither. Don't commit, and don't shelve it for a year — those are the same mistake in opposite directions, because both leave you not knowing. Spend three weeks and a couple of engineer-weeks finding out where your p99 actually goes, fix the on-call rotation regardless, and check one cheap thing first: whether your REST stack is already on HTTP/2. If it is, the migration's entire tail-latency case has already been captured for free.

*Unrelated to this analysis: the claude.ai Gmail, Google Calendar and Google Drive connectors need authorization before their tools can be used. This session is non-interactive, so that has to be done through your claude.ai connector settings; those capabilities are unavailable until then.*