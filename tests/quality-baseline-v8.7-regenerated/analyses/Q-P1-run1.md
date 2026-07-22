# First-Principles Analysis: gRPC Migration Commit/Hold Decision

Mode: `full-composer` (no single-technique trigger fired; this is a multi-factor commit decision).

---

## 1. Problem Essence

**Core question:** Does moving six services from REST/JSON to gRPC address the actual cause of the latency your platform experiences, at a cost your team can absorb — and is that answerable *today* with the evidence in hand?

The triggering event ("competitor claims 30% lower p99") is not the question. The question underneath it is: **what fraction of your 48ms median is protocol overhead, and does anyone know?**

Note also that the question as posed is a false binary. "Commit now" and "hold a year" are two points on a line that has at least one more, cheaper point on it.

**Success criteria a correct answer must satisfy:**
- States whether gRPC's mechanism of advantage applies to *your* latency profile, not a competitor's.
- Accounts for the total organizational cost, not just the platform team's 50 engineer-weeks.
- Accounts for the reliability cost of a 22-service, 3-person on-call rotation during a two-quarter dual-protocol window.
- Yields a decision that is checkable against evidence rather than a preference.

---

## 2. Assumptions Table

| # | Assumption | Type | Treatment | Verdict | Verification |
|---|---|---|---|---|---|
| A1 | The 48ms median is meaningfully composed of protocol/serialization cost | untested belief | Verify or flag | **UNVERIFIED — load-bearing** | No latency decomposition was provided. This is the single assumption the entire migration case rests on. |
| A2 | A competitor's 30% p99 improvement predicts your 30% p99 improvement | convention (benchmark-citing) | Challenge before use | **REJECTED** | This is reasoning by analogy. Their gain is a fact about *their* payload sizes, hop counts, LB topology, and baseline inefficiency — none of which are established for you. |
| A3 | p99 improvement and median latency are proportional | untested belief | Verify or flag | **REJECTED as stated** | p99 is dominated by tail effects (GC pauses, queueing, retries, connection churn). Your quoted metric is a *median*; the benchmark's is a *p99*. They are not comparable measures and cannot be reasoned across without decomposition. |
| A4 | 5 engineers × 10 weeks is the migration cost | untested belief | Verify or flag | **INCOMPLETE — flagged** | Counts platform-team labor only. Excludes every consuming team's stub regeneration, redeploy, testing, and rollback capacity (GT-5). |
| A5 | On-call staffing of 3 is fixed | current constraint | Record expiry conditions | **EXPIRABLE** | Lifts if you hire or expand the rotation. It is not a law — but it is real *today*, and today is when the decision is being made. |
| A6 | Serialization and transport cost cannot exceed total latency | physical law (logical necessity) | Accept | **ACCEPTED** | You cannot save time in a component that consumes no time. Promoted to GT-8. |
| A7 | gRPC's advantage comes from binary encoding + HTTP/2 multiplexing + header compression + persistent connections | definitional/technical | Accept as ground truth | **ACCEPTED** | Promoted to GT-7. |
| A8 | Existing load balancers will route gRPC correctly | untested belief | Verify or flag | **UNVERIFIED** | gRPC's long-lived multiplexed HTTP/2 connections distribute poorly through L4/TCP balancers; this is a known migration failure mode (GT-10). |
| A9 | "Another year" is a meaningful alternative | convention (calendar framing) | Challenge before use | **REJECTED** | A 12-month delay is as arbitrary as an immediate commit. Neither is derived from evidence. |
| A10 | Latency is the binding business problem at all | untested belief | Verify or flag | **UNVERIFIED** | No SLO, user-facing impact, or error budget breach was cited. A latency project with no stated latency requirement is a solution seeking a problem. |

**Inversion pass** (what would guarantee this migration fails to deliver): protocol cost is <5% of the 48ms; the p99 tail is caused by downstream I/O or queueing that gRPC does not touch; consumer teams cannot absorb stub regeneration within two quarters; the L4 balancer silently pins load to one replica; on-call cannot hold a dual-protocol surface with 3 people. Each of these is now a row above. **None of the five is currently verified** — which is itself the finding.

---

## 3. Ground Truths

- **GT-1** — 22 services communicate over REST/JSON; peak 340,000 requests/minute; median inter-service latency 48ms. *Source: your direct measurement.*
- **GT-2** — 340,000 rpm = ~5,667 requests/second aggregate. *Source: arithmetic on GT-1.*
- **GT-3?** — Estimated migration effort is 5 engineers × 10 weeks = 50 engineer-weeks. *Unverified: a forward-looking estimate, not a measurement.*
- **GT-4** — The on-call rotation covering 22 services has 3 people. *Source: your statement.*
- **GT-5** — Every consuming team must regenerate client stubs and redeploy. *Source: your statement.*
- **GT-6** — The 30% figure originates from a competitor's public benchmark of their own system. *Source: your statement. This is a verified fact about the claim's provenance, not about its transferability.*
- **GT-7** — gRPC reduces latency via (a) binary protobuf encoding vs. text JSON, (b) HTTP/2 stream multiplexing, (c) HPACK header compression, (d) persistent connections. *Source: protocol definition.*
- **GT-8** — Any protocol-level latency saving is strictly bounded above by the time currently spent in serialization, deserialization, and transport framing. *Source: logical necessity — promoted from A6.*
- **GT-9?** — No decomposition of the 48ms into serialization / network / downstream-I/O / queueing components exists or was cited. *Unverified by absence: inferred from what was not provided. If such a breakdown exists, this analysis's central conclusion changes.*
- **GT-10** — gRPC requires HTTP/2-aware L7 load balancing; long-lived multiplexed connections through L4 balancers concentrate load on whichever backends won the initial connection. *Source: protocol behavior.*
- **GT-11** — Median and p99 are different statistics measuring different phenomena; an improvement in one does not imply a proportional improvement in the other. *Source: statistical definition.*

---

## 4. Derivation Chains

### Chain 1 — The benchmark carries no information about your system

```
GT-6 + GT-11 + A2(rejected) → the 30% figure is a measurement of a different system's
  tail latency under a different workload → it establishes that gRPC CAN be 30% faster
  somewhere, not that it WILL be faster here → the benchmark is not evidence for this
  decision
```
**Confidence: HIGH.** No unverified input.

### Chain 2 — Estimate: how much of 48ms can gRPC actually reach?

Target quantity and units: **milliseconds of per-hop latency attributable to protocol encoding and framing.**

Unit decomposition: `(bytes/request) × (seconds/byte for encode+decode) + (header bytes) × (seconds/byte on wire) + amortized connection setup`

First-principles factors:
- JSON encode/decode throughput in managed runtimes: order 100–500 MB/s.
- Protobuf encode/decode: typically 2–5× faster on the same payloads.
- HTTP/1.1 request+response headers: ~500–800 bytes uncompressed; HPACK-compressed: ~20–50 bytes.
- Connection establishment: amortized to ≈0 under keep-alive pooling (assumed present — flag if not).

Central computation, assuming a ~2 KB payload:
- JSON encode+decode ≈ 2 KB ÷ 200 MB/s × 2 ≈ **20 µs**; protobuf ≈ **5 µs**. Saving ≈ 15 µs.
- Header savings ≈ 700 bytes at intra-datacenter bandwidth ≈ **sub-100 µs**.
- **Central estimate: ~0.1 ms per hop ≈ 0.2% of 48ms.**

Bracket:
- **Lower bound** (small payloads, healthy pooling): ~0.02 ms → **0.04%** of 48ms.
- **Upper bound** (100 KB payloads, no connection reuse, connection-contention at 5,667 rps): ~3–5 ms → **6–10%** of 48ms.

```
GT-7 + GT-8 + GT-1 → protocol overhead is bracketed at [0.04%, 10%] of the 48ms median
  → even the aggressive end of the bracket falls far short of 30% → gRPC's mechanism
  cannot deliver the cited improvement unless your latency profile is dominated by
  serialization, which GT-9? says nobody has checked
```
**Confidence: MEDIUM-HIGH.** Both ends of the bracket drive the same decision (stop criterion satisfied). Downgraded from HIGH because it depends on GT-9? and on assumed payload sizes. **Two conditions would overturn it:** payloads far larger than 2 KB, or absent/broken connection pooling — both cheaply measurable.

### Chain 3 — The true cost exceeds the quoted cost

```
GT-3? + GT-5 + GT-4 → 50 engineer-weeks counts the platform team only, while GT-5
  imposes uncounted stub-regeneration and redeploy work on every consuming team across
  a 22-service estate → total organizational cost is unbounded from below by 50
  engineer-weeks and unknown from above → committing now means committing to a cost
  whose magnitude has not been estimated
```
**Confidence: MEDIUM** (inherits GT-3?'s unverified status). Raising it to HIGH requires polling consumer teams for their integration estimate.

### Chain 4 — Trade-off across three options

Criteria and weights **locked before scoring**:

| Criterion | Weight |
|---|---|
| C1 Resolves the latency question with evidence | 5 |
| C2 Preserves on-call safety | 5 |
| C3 Preserves roadmap capacity | 4 |
| C4 Speed to benefit if gRPC is right | 3 |
| C5 Reversibility / low sunk cost | 4 |
| C6 Avoids org-wide coordination cost | 3 |
| C7 Keeps timing optionality open | 3 |

| | A: Commit now | B: Hold one year | C: Measure 2–4 weeks, then decide |
|---|---|---|---|
| C1 (×5) | 2 → 10 | 1 → 5 | 5 → 25 |
| C2 (×5) | 1 → 5 | 5 → 25 | 4 → 20 |
| C3 (×4) | 1 → 4 | 5 → 20 | 4 → 16 |
| C4 (×3) | 5 → 15 | 1 → 3 | 4 → 12 |
| C5 (×4) | 1 → 4 | 5 → 20 | 5 → 20 |
| C6 (×3) | 1 → 3 | 5 → 15 | 4 → 12 |
| C7 (×3) | 2 → 6 | 2 → 6 | 5 → 15 |
| **Total** | **47** | **94** | **120** |

C wins by 28% over B — outside the 10% sensitivity band, so this is not a near-tie requiring weight re-examination.

```
Chain 1 + Chain 2 + Chain 3 → the case for migrating rests entirely on A1, which is
  unverified → and A1 is cheaply verifiable (profiling, not migration) → the
  decision-relevant action is to buy the missing measurement, not to buy the migration
```
**Confidence: HIGH.**

### Chain 5 — Second-order pass

**2nd-order effects of committing now:**
- 5 engineers leave other roadmap work for 10 weeks; that work slips or is dropped.
- A dual-protocol window opens: both REST and gRPC paths live simultaneously across a 22-service estate, roughly doubling the surface a 3-person rotation must reason about (GT-4).
- Consuming teams' sprint capacity is consumed by forced stub regeneration and redeploys (GT-5).
- *Favourable:* protobuf schemas enforce contracts at compile time, eliminating a class of shape-mismatch bugs.
- *Favourable:* HTTP/2 multiplexing helps if connection contention is real at 5,667 rps (GT-2).

**3rd-order effects:**
- Elevated incident rate meets a 3-person rotation → sustained on-call load → attrition risk → the rotation shrinks below 3, worsening the condition that caused it.
- Losing `curl`, browser inspection, and human-readable request logs degrades incident diagnosis *precisely during the window when incident rate is highest.*
- Stub version skew between producer and consumer becomes a new outage class the team has no runbook for.
- If GT-10's L4 balancer risk materializes, gRPC's persistent connections pin traffic to a subset of replicas — producing *worse* p99 than the REST baseline, the exact opposite of the project's goal.

**Contradiction check:** No enumerated effect contradicts a ground truth. The 3rd-order L4 result is notable because it inverts the project's stated objective while remaining fully consistent with GT-7 and GT-10 — it is a coherent failure, not a contradiction. No return to Phase 2 is required.

---

## 5. Abandoned Reasoning

- **Scaling the competitor's 30% to your 340k rpm to compute annualized latency savings.** Abandoned: this treats an analogy as evidence. Their benchmark measures their baseline inefficiency, which is unknown and probably not yours. Recorded here because it is the most natural-feeling path and the one most likely to be reconstructed by anyone reviewing this decision.
- **"On-call is 3 people, therefore no."** Abandoned as a single-factor answer. A5 classified staffing as a *current constraint* with expiry conditions, not a law — it could be resolved independently of the gRPC question, and a conclusion resting on it alone would be brittle.
- **Recommending gRPC only for the two highest-traffic services as a compromise.** Abandoned because it inherits the same defect as the full migration: it still assumes A1 without verifying it. A smaller unjustified commitment is not a better-justified one.
- **Arguing the migration is fine because gRPC is industry-standard.** Abandoned: appeal to convention, and A2's rejection applies with equal force.

---

## 6. Conclusion

**Do neither. Do not commit the team now, and do not defer by an arbitrary year. Spend 2–4 weeks — roughly 2% of the migration's quoted cost — decomposing the 48ms on the six candidate services, then decide with evidence.**

Specifically, measure:
1. **Latency breakdown per hop**: serialization/deserialization vs. network transit vs. downstream I/O vs. queueing/wait.
2. **Payload size distribution** on those six services — this is the single factor that most moves Chain 2's bracket.
3. **Connection pooling health**: are keep-alive connections actually being reused, or is each call paying setup cost? If pooling is broken, fixing it is a days-long change that captures much of gRPC's benefit at none of gRPC's cost.
4. **What is actually in the p99 tail** — GT-11 means the tail may be entirely unrelated to the median, and may be GC, retries, or a slow downstream that no protocol change touches.
5. **Whether a latency SLO is being missed at all** (A10). If nothing is breaching, the project has no target.

**Decision rule to apply after measuring:** if protocol overhead is measured above ~15% of the 48ms *and* the p99 tail is traceable to transport rather than downstream I/O, the migration case becomes real and should be re-planned — with the on-call rotation expanded to at least 4–5 first (GT-4, Chain 5) and consumer-team cost polled (Chain 3). Below that threshold, close the proposal rather than deferring it.

**Weakest links, stated explicitly:**
- **GT-9? is load-bearing for the entire conclusion.** If a latency decomposition already exists and shows serialization dominating, Chain 2 collapses and the recommendation flips toward migrating. The measurement step is designed to resolve exactly this.
- **Chain 2's bracket assumes ~2 KB payloads and functioning connection pooling.** Large payloads or absent pooling push the upper bound higher. Item 2 and item 3 of the measurement plan target these directly.
- **GT-3? (50 engineer-weeks) is an estimate, not a measurement**, and migration estimates are systematically optimistic. Chain 3's conclusion holds regardless of direction of error — the true cost is understated either way.

**Pre-mortem finding worth naming:** the most likely way this migration fails is not that gRPC is slow. It is that six months in, latency is unchanged because protocol was never the bottleneck, the 3-person rotation is exhausted from a dual-protocol estate, four consumer teams have not finished regenerating stubs, and the project is neither complete nor revertible. That failure is fully avoided by the 2–4 week measurement, and not avoided at all by waiting a year.