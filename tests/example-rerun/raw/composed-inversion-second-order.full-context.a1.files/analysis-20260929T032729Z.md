# First-Principles Analysis: Redis Read-Through Cache as Grounds to Defer a Scheduled Postgres Upgrade

**Mode:** full-composer (the request asks for a full first-principles breakdown combining
decomposition, assumption-challenge, pre-mortem, second-order thinking and a trade-off
recommendation — not a single focused technique).

---

## 1. Problem Essence

**Core problem:** Given that canceling/deferring the scheduled Postgres upgrade is expensive
to reverse (procurement lead time) while adopting the Redis cache is cheap to reverse before
rollout, does the evidence cited (peak read-QPS, next-tier instance cost) actually establish
that a read-through cache will cut p95 latency and database load enough to safely defer the
upgrade for two quarters — and if not, what decision sequencing correctly respects that
reversibility asymmetry?

**Success criteria:**
1. The analysis states which load-bearing sub-claims inside the platform lead's claim are
   established by the cited evidence and which are not, with each traced to a named ground
   truth or flagged unverified.
2. The analysis identifies the specific failure modes (stampede/thundering herd, hot-key skew,
   staleness, non-read-driven DB load, tail-latency composition) that could make the claim
   false even if the cache ships successfully, via pre-mortem and second-order analysis.
3. The Conclusion section names a single recommendation among (a), (b), or a hybrid, with a
   confidence rating that reflects how much of the mechanism is actually verified versus
   asserted.
4. The Conclusion section names the cheapest evidence that would most efficiently de-risk the
   decision before the expensive-to-reverse action (canceling/deferring the upgrade) is taken.

---

## 2. Assumptions Table

Sixteen assumptions were identified directly from decomposing the claim and applying inversion
(Phase 2); four more (A17–A20) were surfaced later, during the Phase 4 end-of-phase Assumption
Audit, and are folded back into this table per the methodology (see the Assumption Audit scan
in the process-output appendix). A lightweight fishbone pass across the default six-category
set (People, Process, Technology and Tools, Environment, Information, Resources) was used to
make sure "what actually drives Postgres load" was not enumerated from intuition alone — it
surfaced A9, A15, and the vacuum/connection material behind GT-2/GT-3.

Inversion procedure applied to the headline claim: stated precisely as "adding the cache will
reduce DB load and p95 enough to safely defer the upgrade two quarters"; inverted as "the cache
will not reduce load/latency enough, and deferring causes a problem within two quarters."
Failure-guaranteeing conditions enumerated (low hit rate; load is not read-QPS-driven; p95 is
tail-dominated by uncacheable queries; the cache itself spikes load via stampede; growth
consumes freed headroom; staleness forces short TTLs that cap hit rate; the 2-week estimate is
optimistic; procurement interacts badly with a late discovery) map directly to A1–A10, A13.

| Assumption | Type | Treatment | Verdict | Verification |
|---|---|---|---|---|
| A1: Peak read-QPS is the dominant driver of current Postgres load (CPU/memory/IO). | untested belief | Verify via load-attribution breakdown (e.g., query-level resource accounting) before relying on it. | Challenge — the cited evidence (peak QPS) measures traffic volume, not resource attribution; GT-2/GT-3 show at least some load is structurally independent of read-QPS. | unverified — flagged (elevated as GT-7? input to chain C1) |
| A2: A large, stable fraction of listing read-QPS is cache-hittable (repeated reads of a bounded key set). | untested belief | Verify against real query-key cardinality / access-frequency histogram. | Challenge — GT-5? shows hit rate is highly sensitive to the access-skew exponent and effective key-space size, neither measured. | unverified — flagged |
| A3: p95 latency is dominated by the same cacheable reads that dominate QPS. | untested belief | Verify via latency breakdown by query shape. | Challenge — GT-4 shows p95 is a tail statistic by definition; the tail is typically populated by a different query mix than the bulk of QPS. | unverified — flagged |
| A4: The next-tier instance cost is a valid proxy for the capacity problem the upgrade addresses. | convention | Challenge explicitly — ask what resource the upgrade actually adds (CPU, buffer-cache RAM, IOPS, connection ceiling) versus what the cache would relieve. | Challenge — cost is a budget fact, not a capacity-mechanism fact; substituting it for mechanism evidence is a reporting convention, not a justification. | unverified — flagged |
| A5: "At least two quarters" of deferral is derived from an actual headroom ÷ growth-rate calculation. | untested belief | Verify the runway math is shown, not asserted. | Challenge — no growth-rate or headroom figures appear in the cited evidence; the duration reads as an assertion. | unverified — flagged |
| A6: The Redis rollout itself will not add new load spikes to Postgres (stampede/thundering herd, cold-cache restart). | untested belief | Verify the implementation plan includes stampede mitigation. | Challenge — GT-1 and GT-6 show stampede/thundering herd is a standard, common failure mode of exactly this pattern, not a remote edge case. | unverified — flagged (elevated as GT-1/GT-6-grounded input to chain C4) |
| A7: The two-engineer-week estimate covers production hardening (invalidation, stampede protection, hot-key handling, monitoring, Redis-down fallback), not a naive implementation. | untested belief / convention | Challenge the convention that "add a cache" estimates typically undercount hardening work. | Challenge — no scope breakdown is cited; two weeks is far more consistent with a naive cache-aside prototype than with everything GT-1/GT-6 show is needed to avoid new risk. | unverified — flagged (used as `[Assumes: A7]` on chain C4) |
| A8: Listings data (price, stock) can tolerate the staleness window implied by the TTL needed to hit the target hit rate. | untested belief | Verify business tolerance for stale price/stock display against the required TTL. | Challenge — GT-6 shows short TTLs are the standard mitigation for freshness-sensitive fields, but short TTLs lower hit rate and, unless jittered, reintroduce synchronized-expiry risk; no evidence this tension is resolved. | unverified — flagged |
| A9: DB load is overwhelmingly read-query-execution load, not connection-count, vacuum/write-amplification, replication, or lock-contention load. | untested belief | Verify via categorical load breakdown (fishbone: Technology/Tools, Process, Resources categories). | Challenge — GT-2 (vacuum is write-driven) and GT-3 (connections cost resources regardless of activity) are both independent of read-QPS. | unverified — flagged |
| A10: The scheduled upgrade was sized specifically for read-QPS pressure, not buffer-cache memory, write throughput, connection ceiling, storage growth, or a known upcoming feature/campaign. | untested belief | Check the upgrade's original sizing justification/ticket. | Challenge — this is the single most decision-relevant unknown and is unaddressed anywhere in the cited evidence. | unverified — flagged |
| A11: Reversing the cache decision is cheap right up to rollout, with no earlier organizational action (notifying procurement, reallocating the two engineer-weeks) becoming entangled or costly first. | current constraint | Record expiry — holds only until the organization acts on "defer the upgrade" (e.g., tells procurement to stand down); treat the technical cache decision and the organizational cancellation act as two separable decisions. | Accept — expires the moment procurement/finance is told the upgrade may not be needed, which is exactly the organizational act this analysis recommends sequencing carefully (see A19, A20). | n/a — logical/definitional distinction, not an empirical fact |
| A12: Procurement lead time is long enough that a late-discovered cache shortfall cannot be corrected in time. | current constraint | Record expiry — holds only under the current procurement/vendor path; expires entirely if this is managed/cloud Postgres with same-day vertical resize. | Accept — stipulated by the decision context (GT-8?); this is the single highest-leverage fact to confirm, since its falsity would change the whole analysis (see Sensitivity, adversarial pass). | unverified — flagged (GT-8?) |
| A13: Traffic or catalog growth during the deferral window will not consume the freed capacity before two quarters elapse. | untested belief | Check growth trend and forward calendar (seasonal peaks, planned campaigns) against the two-quarter window. | Challenge — not addressed in cited evidence; a known peak season inside the window materially raises risk. | unverified — flagged |
| A14: A monitoring/tripwire mechanism exists, or will be built, that detects cache underperformance early enough to still re-order the upgrade within lead time. | untested belief | Verify a concrete tripwire metric and decision date are defined before canceling anything. | Challenge — nothing in the architecture-review document as described establishes this; absent it, "defer" is a one-way door disguised as a monitored one. | unverified — flagged |
| A15: The Postgres instance serves only the listings API (no noisy-neighbor load from other services/teams on the same instance). | untested belief | Verify DB tenancy — dedicated instance or shared. | Challenge — not addressed in cited evidence; shared tenancy caps what listings-focused caching can achieve regardless of hit rate. | unverified — flagged |
| A16: The listings endpoint's query space is a large combinatorial space (filters × sorts × pagination) rather than a small set of canonical keys. | untested belief | Verify against the actual API contract / query-log key cardinality. | Challenge — no query-key analysis is cited; this is the specific mechanism behind GT-5?'s hit-rate sensitivity. | unverified — flagged (elevated to GT-9?, input to chain C2) |
| A17 *(surfaced at Phase 4 audit)*: Under a long procurement lead time, avoiding an uncorrectable capacity shortfall is treated as a hard must-have rather than merely one weighted trade-off criterion. | convention | Challenge explicitly — this is a risk-management convention (gate irreversible/high-switching-cost risks rather than trading them off continuously), not a law; state it so it can be disagreed with. | Accept — standard capacity-planning practice under asymmetric reversibility; consistent with the reversibility framing given in the decision context (GT-8?). | n/a — methodological convention, disclosed as `[Assumes: A17]` on chain C5 |
| A18 *(surfaced at Phase 4 audit)*: The trade-off criterion weights used reflect a reasonable risk posture but are not ratified by the actual decision-makers (platform lead, finance, SRE). | convention | Challenge — invite the real stakeholders to re-run the weighting with their own priorities. | Accept, with explicit invitation to re-weight — the flip test (chain C5) shows the ranking is insensitive to any single weight moving within its 1–5 range, which bounds but does not eliminate this exposure. | n/a — methodological judgment, disclosed as `[Assumes: A18]` on chain C5 |
| A19 *(surfaced at Phase 4 audit)*: Absent an explicitly named independent owner, the team that authored the original claim also controls what counts as "success" at the evidence checkpoint. | current constraint | Record expiry — resolved the moment an independent decision-owner is named (the Cluster C mitigation in the adversarial pass). | Accept — default organizational state absent an explicit fix; disclosed as `[Assumes: A19]` on chain C5's second-order extension. | unverified — flagged |
| A20 *(surfaced at Phase 4 audit)*: Communicating "the upgrade might not be needed" triggers informal deprioritization by procurement/finance even without a formal cancellation. | untested belief | Verify against how this organization's procurement function actually behaves; mitigate regardless via explicit instruction. | Challenge — plausible, organization-specific, and mitigated by disposition (explicit instruction to proceed at normal priority) regardless of whether it is literally true here. | unverified — flagged; disclosed as `[Assumes: A20]` on chain C5's second-order extension |

## 3. Ground Truths

Reduce-to-primitives note: GT-1, GT-2, GT-3, and GT-6 each bottom out at a directly-quoted
primary/official source (a definitional mechanism or a documented system behavior), so no
further recursive five-whys decomposition was needed to reach an irreducible fact. GT-4 is a
mathematical definition (a percentile statistic), which is accepted directly as a
definitional/physical-law-type ground truth per the Phase 2 treatment for that type, requiring
no external verification beyond its definition. GT-5, GT-7 through GT-10 remain irreducibly
unverified within this analysis because the scenario is explicitly hypothetical — there is no
real telemetry, repo, or query log to open, so the honest ceiling on their verification is
"unverified," not a deeper decomposition.

- **GT-1** A cache stampede (thundering herd) occurs when a popular cached entry expires under
  heavy concurrent load, causing many requests to fall through to the backend and recompute or
  re-query it simultaneously, with congestion collapse as the worst-case outcome — source:
  Wikipedia, "Cache stampede"; read-at-source: fetched directly, quoting "Multiple threads of
  execution will all attempt to render the content of that page simultaneously" and the
  congestion-collapse worst case.
- **GT-2** PostgreSQL requires vacuuming/autovacuum driven by insert/update/delete volume and
  transaction-ID-wraparound protection, independent of read query volume — a table can require
  intensive vacuum work with zero reads against it — source: PostgreSQL official docs, "Routine
  Vacuuming" (postgresql.org/docs/current/routine-vacuuming.html); read-at-source: fetched
  directly, quoting "autovacuum checks for tables that have had a large number of inserted,
  updated or deleted tuples" and the two-billion-transaction wraparound requirement.
- **GT-3** Each PostgreSQL connection consumes dedicated backend resources (memory, process
  slot) up to `max_connections`, regardless of whether it is actively executing a query; these
  resources are sized directly off `max_connections` — source: PostgreSQL official docs,
  "Connection Settings" (postgresql.org/docs/current/runtime-config-connection.html);
  read-at-source: fetched directly, quoting "PostgreSQL sizes certain resources based directly
  on the value of `max_connections`. Increasing its value leads to higher allocation of those
  resources, including shared memory."
- **GT-4** By definition, "p95 latency" is the value at the 95th percentile of the response-time
  distribution — it characterizes the slowest ~5% of requests, not the median/typical request,
  and is therefore governed by whatever drives the tail of the distribution rather than by
  whatever drives its bulk — source: definition of a percentile (order statistics); accepted
  directly as a mathematical/definitional ground truth (Phase 2 "physical law" treatment), no
  external verification required beyond the definition itself.
- **GT-5?** Web/catalog access patterns typically follow a Zipf-like (power-law) distribution in
  which a small fraction of items receives a large fraction of requests, but the exact skew
  (the Zipf exponent) determines how much of the catalog must be cached to reach a given hit
  ratio — a flatter distribution over a larger effective key space requires caching a much
  larger share of results to reach the same hit ratio — source: aggregated web search
  (IEEE, "Effective caching of Web objects using Zipf's Law"; Java Code Geeks explainer on
  Zipf's Law and cache hit ratios); reported-by-delegate: a search-tool synthesis across
  multiple sources, not a single document opened and quote-checked directly — cited source not
  opened by this analysis.
- **GT-6** In the cache-aside/read-through pattern, TTL-based expiration trades staleness
  against load: "Always apply a time to live (TTL) to all of your cache keys, except those you
  are updating by write-through caching," and for rapidly-changing data the pragmatic mitigation
  is a short TTL — but "using consistent TTL lengths creates another problem — many keys expire
  simultaneously, causing the 'thundering herd' effect," mitigated by adding randomness/jitter to
  TTL values — source: AWS, "Caching Best Practices" (aws.amazon.com/caching/best-practices/);
  read-at-source: fetched directly, quotes above checked against the fetched page content.
- **GT-7?** The peak read-QPS figure, the next-tier Postgres instance cost figure, and the
  two-engineer-week effort estimate are all asserted by the platform team lead in the
  architecture-review document; this analysis has not independently observed the underlying
  telemetry, cost quote, or effort breakdown — source: cited to the architecture-review document
  per the decision context; reported-by-delegate: the platform team lead is the delegate, and in
  this hypothetical there is no underlying dashboard/quote/ticket to open — cited source not
  opened by this analysis (none exists to open).
- **GT-8?** The decision's reversibility is asymmetric as stipulated: adopting the cache is
  cheaply reversible before rollout, while canceling/deferring the scheduled Postgres upgrade is
  expensive to reverse late because of procurement lead time — source: stipulated by the
  decision context supplied for this analysis, naming no further source; unverified: this is a
  defining premise of the scenario rather than an independently confirmed fact about a real
  procurement process, and per the Sensitivity finding (adversarial pass) it is the single fact
  whose falsity would most change the recommendation.
- **GT-9?** The listings endpoint's query space is likely a large combinatorial space (filters ×
  sorts × pagination) rather than a small set of canonical keys — source: none; unverified — no
  API schema, query log, or repository is available in this hypothetical to confirm actual
  key-space cardinality; elevated from assumption A16 for use in chain C2.
- **GT-10?** Product listings typically include mutable fields (price, inventory/stock count)
  that change on a timescale shorter than a read-heavy endpoint's typical cache TTL, creating a
  staleness risk (e.g., displaying out-of-stock items as available) if cached aggressively —
  source: none; unverified — general e-commerce domain plausibility, not confirmed against this
  specific system's schema or mutation frequency.

**Provenance summary:** `?`-marked: GT-5, GT-7, GT-8, GT-9, GT-10 (5 of 10).
Read-at-source: GT-1 — Wikipedia "Cache stampede," congestion-collapse passage quoted verbatim;
GT-2 — postgresql.org "Routine Vacuuming," autovacuum-threshold and wraparound passages quoted
verbatim; GT-3 — postgresql.org "Connection Settings," `max_connections`-sizing passage quoted
verbatim; GT-6 — AWS "Caching Best Practices," TTL and thundering-herd passages quoted verbatim.
GT-4 is a mathematical definition and carries no read-at-source location by nature (see Phase 2
"physical law" treatment above); it is not counted among the unverified `?`-marked set.

No assumption that received a Discard verdict in Phase 2 appears in this list — every
assumption above received an Accept or Challenge verdict, and the Challenge verdicts
(A1–A10, A13–A16, A20) are exactly the untested beliefs elevated here as `GT-N?` for use in the
Derivation Chains, carrying their `?` forward as D-07 requires.

## 4. Derivation Chains

Estimate (Fermi) and theoretical-limit were considered for this phase and did not fire — see
"Techniques not applied" in the process-output appendix. Trade-off and second-order thinking
both fired and are converted into chain form per the rules below.

### Conclusion C1: The claim's premise that cutting read-QPS load "reduces database load enough" is unverified at the most basic level

GT-2 (vacuum load is write-driven) + GT-3 (connections consume fixed resources) + GT-7? (QPS, cost and effort figures are asserted, not load-attributed)
→ vacuum overhead and reserved per-connection resources are structurally independent of read-QPS volume
→ so some share of current Postgres load cannot be reduced by caching reads no matter how effective the cache is
→ the architecture-review document's cited evidence measures traffic volume and price, not a resource-attribution breakdown of load
→ the claim's premise that cutting read-QPS load reduces database load enough is therefore unverified at the most basic level

**Pre-check:** head GT-2, GT-3, GT-7? · ?-marked: GT-7? · lowest cited: none · Inputs ceiling: MEDIUM
**Confidence:** LOW — Inputs axis short: GT-7? is asserted by the platform lead and not independently observed; verification = pull the actual load-attribution telemetry (e.g., per-query resource accounting) and the upgrade's original sizing justification. Rivals axis also short: a live, unsettled rival holds that read-QPS genuinely is the dominant load driver in this specific system; nothing in this hypothetical's available evidence settles it either way, since no real telemetry exists to inspect — the same load-attribution pull that resolves GT-7? would also settle this rival. Two axes short → LOW per the calibration rule in the output template.

### Conclusion C2: The achievable cache hit rate — and the fraction of read-QPS actually offloaded — is not derivable from the cited evidence and could plausibly sit far below what deferring the upgrade requires

GT-5? (Zipf skew sets the keyspace coverage needed for a hit-rate target) + GT-9? (listings query space is likely combinatorial)
→ a combinatorial query space is effectively a much larger keyspace than a small set of canonical listing-page keys
→ per GT-5?, a larger keyspace with a flatter access skew requires caching a much bigger share of results to reach the same hit ratio
→ the achievable cache hit rate for this endpoint is therefore not derivable from the cited evidence and could plausibly sit far below what deferring the upgrade would require

**Pre-check:** head GT-5?, GT-9? · ?-marked: GT-5?, GT-9? · lowest cited: none · Inputs ceiling: MEDIUM
**Confidence:** LOW — Inputs axis short: GT-5? is a reported-by-delegate literature synthesis, not one primary source opened and quote-checked; GT-9? is an unverified belief about this system's actual query-key cardinality; verification for both = measure real access-frequency and key-cardinality against production query logs or a representative sample. Rivals axis also short: a live rival holds that most listings traffic hits a small, hot default/unfiltered view, which would make hit rate high regardless of the combinatorial filter tail; unsettled without the same key-cardinality measurement. Two axes short → LOW.

### Conclusion C3: The p95 latency improvement the claim asserts is a hypothesis, not a demonstrated mechanism

GT-4 (p95 is a tail statistic by definition) + C2 (achievable hit rate is uncertain)
→ p95 characterizes the slowest five percent of requests rather than the typical request
→ whatever caching does to the average case does not mechanically move p95 unless the specific queries populating that slow tail are themselves cache-hittable
→ C2 already shows the endpoint's cacheable share is uncertain, so the p95 improvement the claim asserts is a hypothesis rather than a demonstrated mechanism

**Pre-check:** head GT-4, C2 (LOW) · ?-marked: none · lowest cited: LOW · Inputs ceiling: LOW
**Confidence:** LOW — capped by the Inputs ceiling: C2 is rated LOW (see C2's own confidence line for its verification path, not re-explained here). Additionally, a live rival holds that the endpoint's current p95 offenders are simple, popular queries hitting an already-loaded database rather than genuinely uncacheable long-tail queries, which would make caching help p95 directly — unsettled without a latency-by-query-shape breakdown.

### Conclusion C4: Absent confirmed stampede protection, adopting the cache does not monotonically reduce peak DB load — it changes the load profile from steady-and-growing to mostly-reduced-with-periodic-correlated-spikes

GT-1 (cache stampede mechanism) + GT-6 (uniform TTL causes synchronized expiry)
→ absent explicit jitter or request-coalescing, a uniform-TTL cache expires many popular keys together under load [Assumes: A7]
→ per GT-1, that synchronized expiry sends a burst of concurrent requests to Postgres at once, reproducing a load spike closer to the uncached baseline than the steady-state cached average
→ this spike risk is worst exactly when the deferral decision has removed the upgrade's headroom, so shipping the cache can transiently recreate the failure mode the upgrade exists to prevent

**Pre-check:** head GT-1, GT-6 · ?-marked: none · lowest cited: none · Inputs ceiling: HIGH
**Confidence:** LOW — Inference axis short: `[Assumes: A7]` — whether the implementation plan includes jittered TTL, request-coalescing, or a circuit breaker to Postgres is unconfirmed; if confirmed present, this chain's spike-risk finding no longer applies and should be downgraded to a monitored residual rather than a live concern — verification = confirm the implementation plan before rollout. Rivals axis also short: a live, unsettled rival holds that even an unmitigated stampede would be small relative to normal peak load and not materially affect capacity planning; no magnitude estimate is available in this hypothetical to settle it — verification = a back-of-envelope stampede-magnitude estimate against real peak-QPS figures once they exist. Two axes short → LOW.

### Conclusion C5: Adopt the hybrid — ship the cache now, keep the upgrade on schedule, gate cancellation on a pre-defined evidence checkpoint — with named organizational safeguards against reversibility quietly eroding before that checkpoint

C1 (load composition unverified) + C2 (hit rate uncertain) + C3 (p95 mechanism unconfirmed) + C4 (stampede risk under uniform TTL) + GT-8? (upgrade cancellation is expensive to reverse, cache adoption is cheap pre-rollout)
→ an option that forecloses the upgrade's corrective path before C1 through C4's open questions are resolved fails the survival must-have this reversibility asymmetry imposes, eliminating "ship the cache and cancel the upgrade now" before any weighted scoring [Assumes: A17]
→ weighted scoring of the two surviving options across cost efficiency, latency-improvement speed, engineering effort, evidence quality and corrective-path insurance gives the hybrid checkpoint option the higher total, seventy-two against fifty-seven [Assumes: A18]
→ the flip test shows no single criterion's weight can move within its one-to-five range to reverse that ranking
→ the trade-off therefore resolves to shipping the cache now while keeping the upgrade on schedule and gating cancellation on a pre-defined evidence checkpoint
→[2nd] absent an independent checkpoint owner, the team that authored the original claim also controls what counts as success at the checkpoint, creating an evaluation conflict of interest [Assumes: A19]
→[2nd] once procurement hears the upgrade might not be needed, informal deprioritization can erode the lead-time buffer even without a formal cancellation [Assumes: A20]
→[2nd] a seasonal or growth-driven traffic spike inside the two-quarter window can consume freed headroom faster than modeled, shortening the runway before the checkpoint date arrives
→[3rd] left unaddressed, these effects let the hybrid's paper reversibility drift away from its practical reversibility by the time the checkpoint date arrives, reproducing the exact risk the hybrid exists to avoid

**Pre-check:** head C1 (LOW), C2 (LOW), C3 (LOW), C4 (LOW), GT-8? · ?-marked: GT-8? · lowest cited: LOW · Inputs ceiling: LOW
**Confidence:** LOW — capped by the Inputs ceiling: every chain this recommendation cites (C1–C4) is rated LOW (see each chain's own confidence line for its verification path, not re-explained here). GT-8? (the procurement-lead-time/reversibility asymmetry) is itself unverified as a fact about this org's actual infrastructure — verification = confirm whether Postgres here is managed/cloud with fast vertical resize (which would remove the asymmetry and much of this decision's urgency) or a slower procurement path (which would confirm it). The chain's own inference also rests on two named judgment calls — `[Assumes: A17]` treating corrective-path preservation as a hard must-have, and `[Assumes: A18]` the specific criterion weights used — neither ratified by the actual decision-makers; the flip test above bounds, but does not eliminate, A18's exposure. None of the four second-order/third-order hops contradicts any ground truth, so no return to Phase 2 is required; they extend the chain as disclosed organizational risks instead.

**No contradiction check (second-order, Phase 4 step 5):** none of C5's `→[2nd]`/`→[3rd]` hops contradicts GT-1 through GT-10 — they identify organizational-behavior risk, not a factual conflict with an established ground truth, so the conclusion is not routed back to Phase 2.

**Success-criteria check (second-order, Phase 4 step 6):** this decision's stated purpose is to avoid an uncorrectable capacity shortfall while not wasting engineering effort on an unnecessary upgrade. The `[Assumes: A19]`/`[Assumes: A20]` effects directly threaten that purpose by eroding the reversibility the hybrid depends on even when every measured number looks fine — which is exactly why they are carried forward as required disposition items (Cluster C) in the adversarial pass rather than left as background risk.

## 5. Abandoned Reasoning

### Dead End: Accepting the claim at face value because peak-QPS and cost evidence were cited

**What was tried:** An initial reading treated "peak read-QPS" and "next-tier instance cost" as
sufficient evidence that the cache would relieve the load driving the upgrade, since both
figures are concrete and were the only evidence offered.

**Why abandoned:** Chain C1 shows QPS is a traffic-volume measure and cost is a budget measure —
neither is a resource-attribution measure, and GT-2/GT-3 establish that a real, non-trivial share
of Postgres load (vacuum, connection overhead) is structurally independent of read-QPS. Treating
the cited figures as if they answered the load-mechanism question was a category error, not a
verified conclusion.

**What it ruled out:** Saves a future reviewer from re-accepting "the evidence looks concrete, so
the mechanism must be sound" — concreteness of a cited number is not the same as its relevance to
the specific mechanism the claim requires.

### Dead End: Modeling the decision as a pure cache-hit-rate problem

**What was tried:** A simplified model that treated cache hit rate as the only variable
determining whether the upgrade could be deferred, on the theory that "hit rate high enough"
implies "database load low enough."

**Why abandoned:** GT-2 and GT-3 show DB load has components (vacuum/write-amplification,
connection-slot overhead) that no achievable hit rate touches. A hit-rate-only model silently
assumes A9 and A15 are both true (all load is read-execution load, on a dedicated instance);
neither is established, so the model was an incomplete decomposition of "database load," not a
wrong calculation within a correct one.

**What it ruled out:** Saves a future reviewer from sizing "how much cache hit rate is needed"
without first pinning down what fraction of load a perfect cache could even remove.

### Dead End: Recommending outright rejection of the cache (upgrade-only, cache never built)

**What was tried:** Considered a strict reading of option (b) that treats the cache idea itself
as unsound because so much of the mechanism is unverified, and recommends building it later,
separately, with no committed timeline.

**Why abandoned:** Nothing in GT-1 through GT-10 shows caching is a bad idea in general — the
risk identified throughout is specifically about *sequencing an irreversible cancellation before
evidence arrives*, not about the cache itself. Chain C5's trade-off shows the hybrid option
dominates a pure upgrade-only path on cost efficiency, latency-improvement speed, and evidence
quality (72 vs. 57) while matching it on corrective-path insurance, so outright rejection of the
cache is dominated by the hybrid and was not carried further as a live option.

**What it ruled out:** Saves a future reviewer from treating "we don't yet have proof" as
equivalent to "don't build it" — the correct response to unverified mechanism claims combined
with cheap reversibility on one side is to build-and-measure, not to abstain.

### Dead End: Treating C4's stampede-mitigation rival as a genuine settled ruling-out

**What was tried:** Initially considered marking chain C4's live rival ("engineers will obviously
implement standard stampede protection as basic hygiene") as ruled out by convention, which would
have let C4 sit at MEDIUM confidence instead of LOW.

**Why abandoned:** Nothing in this analysis's ground truths actually settles whether the
2-engineer-week implementation includes jittered TTL, request-coalescing, or a Postgres-down
circuit breaker (that is exactly what `[Assumes: A7]` flags as unconfirmed); calling the rival
"obviously" ruled out would have been an analogy to how careful teams *usually* behave, not
evidence about this team's actual plan — precisely the kind of reasoning-by-convention the
methodology prohibits as direct evidence.

**What it ruled out:** Saves a future reviewer from over-crediting "good engineers would surely
do X" as if it were a verified ground truth; C4 stays LOW until the implementation plan is
actually checked.

---

## 6. Conclusion

**Recommended approach:** Adopt the hybrid: ship the Redis read-through cache now on its current
two-engineer-week timeline, but do not cancel, defer, or deprioritize the scheduled Postgres
vertical-scale upgrade; keep procurement proceeding at normal priority and hold the upgrade
budget, gating any actual deferral decision on a hard, pre-defined evidence checkpoint set with
comfortable margin before procurement's last cancellable date, owned by someone other than the
team that authored the original claim (chain C5).

**Key insight:** The claim bundles four independently uncertain mechanisms — how much of DB load
is read-QPS-driven at all, how much of that read-QPS is actually cacheable, whether the queries
populating the p95 tail are the same ones being cached, and whether the cache rollout itself adds
new load-spike risk — into one asserted conclusion, while the only evidence cited (peak QPS,
instance cost) speaks to none of the four mechanisms directly (chains C1, C2, C3, C4). Because
mechanism confidence is this thin and the reversibility of the two options is this asymmetric,
the correct response does not require first resolving which way those four mechanisms actually
break — gathering the evidence while doing the cheap-to-reverse thing first is the right move
regardless of how C1–C4 eventually resolve, which is what the trade-off in chain C5 formalizes
(chain C5).

**Trade-offs acknowledged:** The hybrid costs slightly more in the worst realistic case than
committing to cancellation now would (it keeps holding an upgrade budget/slot that might turn
out to be unnecessary) and delivers "certainty" more slowly than a binary decision would; it also
requires organizational discipline this analysis's ground truths show is not yet in place — an
independently owned checkpoint, hard numeric pass/fail bars, and an explicit instruction to
procurement to proceed at normal priority — without which the hybrid's paper reversibility can
quietly erode into the same one-way door option (a) represents (chain C5). The specific cost of
that coordination overhead was not separately quantified in this analysis — no chain — flagged
assumption only.

**Cheapest de-risking evidence (highest priority first):**
- Confirm what the scheduled upgrade was actually sized for, and whether this Postgres is
  managed/cloud with fast vertical resize or a slower procurement path (chain C1; chain C5).
- Pull a load-attribution breakdown (CPU/IO/connections by query, and by non-query sources such
  as vacuum/WAL) to size the ceiling on what caching can even address (chain C1).
- Measure the listings endpoint's real query-key cardinality and access-frequency skew (chain
  C2).
- Break down p95 by query shape to confirm the slow tail is actually cache-hittable (chain C3).
- Confirm the cache implementation plan includes jittered TTL, request-coalescing, and a
  Postgres-down circuit breaker before rollout (chain C4).

**Pre-check:** head C1 (LOW), C2 (LOW), C3 (LOW), C4 (LOW), C5 (LOW); GT-8? · ?-marked: GT-8? · lowest cited: LOW · Inputs ceiling: LOW
**Confidence:** LOW — every chain this conclusion rests on is rated LOW (C1–C5; see each chain's
own confidence line for its verification path, not re-explained here), and the conclusion also
rests directly on GT-8?, whose confirmation (managed/cloud fast-resize vs. slower procurement) is
the single fact most likely to change the recommendation per the Sensitivity finding in the
adversarial pass. This LOW rating describes the state of the *mechanism evidence* behind the
claim, not the soundness of the *decision logic* recommending the hybrid: that logic (do the
cheap-to-reverse thing first, gate the expensive-to-reverse thing on evidence) does not require
C1–C4 to resolve in any particular direction to be correct, which is exactly why chain C5's
must-have/trade-off structure — rather than a bet on how the mechanism questions come out — is
the load-bearing argument for the recommendation. Running the five de-risking checks above would
raise every contributing chain toward HIGH and let the checkpoint in chain C5 resolve on real
data instead of on the asymmetric-reversibility argument alone.

---

# Process Output

*(Everything below this line is process output produced while assembling the analysis above —
not a seventh output section. It documents the audit trail the methodology requires: the
end-of-Phase-4 Assumption Audit, which companion techniques were and were not invoked, the
Phase 5 adversarial pass, the §6→§4 closure ledger, the self-audit scan, and the Self-Audit
Gate's six verdict blocks.)*

## Assumption Audit scan (process output)

| Chain | Step | Step Text (brief) | Assumption surfaced? | Added to Table? |
|---|---|---|---|---|
| C1 | 1 | vacuum/connection overhead independent of read-QPS | none | n/a |
| C1 | 2 | some load cannot be reduced by caching | none | n/a |
| C1 | 3 | cited evidence measures volume/price, not attribution | none | n/a |
| C1 | 4 (conclusion) | premise unverified at the basic level | none | n/a |
| C2 | 1 | combinatorial query space = larger effective keyspace | none — already in table (A16) | n/a |
| C2 | 2 | flatter skew over larger keyspace needs more caching | none | n/a |
| C2 | 3 (conclusion) | achievable hit rate not derivable, plausibly low | none | n/a |
| C3 | 1 | p95 characterizes slowest 5% by definition | none | n/a |
| C3 | 2 | average-case improvement doesn't move p95 unless tail is cacheable | none | n/a |
| C3 | 3 (conclusion) | p95 improvement is a hypothesis, not demonstrated | none | n/a |
| C4 | 1 | uniform-TTL cache expires keys together `[Assumes: A7]` | none — already in table (A7) | n/a |
| C4 | 2 | synchronized expiry bursts requests to Postgres | none | n/a |
| C4 | 3 (conclusion) | spike risk worst when headroom is removed | none | n/a |
| C5 | 1 | must-have eliminates option (a) `[Assumes: A17]` | A17 | yes |
| C5 | 2 | weighted scoring favors hybrid `[Assumes: A18]` | A18 | yes |
| C5 | 3 | flip test: no single weight change reverses ranking | none | n/a |
| C5 | 4 (1st-order conclusion) | resolves to hybrid | none | n/a |
| C5 | 5 (2nd-order) | no independent owner → conflict of interest `[Assumes: A19]` | A19 | yes |
| C5 | 6 (2nd-order) | procurement informally deprioritizes `[Assumes: A20]` | A20 | yes |
| C5 | 7 (2nd-order) | seasonal/growth spike shortens runway | none — already in table (A13) | n/a |
| C5 | 8 (3rd-order, conclusion) | paper reversibility drifts from practical reversibility | none | n/a |

All 21 named derivation-chain steps across C1–C5 are covered, in order, with no step skipped.
Four genuinely new assumptions (A17–A20) were surfaced and folded back into the Phase 2
Classified Assumptions Table; all other steps either introduce no assumption beyond deduction
from their named inputs, or rest on an assumption already present in the table before this scan.

## Techniques not applied (process output)

- **theoretical-limit** — not applicable — no governing physical/hard constraint ceiling is
  relevant to this capacity-planning decision; the open questions are about uncertain empirical
  load composition and organizational sequencing, not about a limit imposed by physics or math.
- **estimate (Fermi)** — not applicable — this hypothetical supplies no numeric telemetry (real
  QPS figures, real cost figures, real query-key counts) to rebuild a magnitude from unit-factors;
  the uncertainty here is about which mechanism applies, not about sizing a known mechanism.
- **inversion (Phase 5 adversarial-technique slot)** — not applicable — the headline conclusion is
  a plan/recommendation, not a bare claim, so the Phase 5 decision rule routes to pre-mortem
  instead (inversion was already invoked, and fired, at Phase 2 for assumption-challenging).

## Adversarial pass (process output)

**Recompute:** Chain C5's trade-off totals recompute independently: option (b) =
3(2)+3(2)+2(4)+4(3)+5(5) = 6+6+8+12+25 = 57; option (c) = 3(3)+3(4)+2(3)+4(5)+5(5) =
9+12+6+20+25 = 72 — both match the values stated in chain C5. The flip-test boundary
recomputes as Total(b)=49+4w, Total(c)=66+3w, crossing at w=17 (outside the 1–5 weight range);
substituting w=5 gives 69 vs. 81 and w=1 gives 53 vs. 69 — (c) wins across the entire valid
range, confirming "no single weight change flips this."

**Sensitivity:** The single ground truth whose falsity would most directly flip the
recommendation is **GT-8?** (the procurement-lead-time/reversibility asymmetry) — it is
`?`-marked. If this Postgres is actually managed/cloud infrastructure with same-day vertical
resize, the entire asymmetric-reversibility argument for gating cancellation on a checkpoint
collapses, and the decision reduces to a much lower-stakes "ship the cache, resize whenever
needed" problem where option (a)-style reasoning becomes far more defensible. Weakest link per
chain: C1 — A1/A9/A10 (no load-attribution data exists); C2 — GT-9? (key-space cardinality
unmeasured); C3 — no latency-by-query-shape breakdown exists; C4 — A7 (scope of the two-week
estimate is unconfirmed); C5 — GT-8? (as above) and A18 (unratified criterion weights).

**Rival:** Headline conclusion (adopt the hybrid): strongest rival is "execute the upgrade now,
full stop, treat caching as unrelated later work" (option b) — this is not a dominated straw
option; chain C5's own weighted scoring shows it loses by a moderate margin (57 vs. 72), and is
ruled out only by the Evidence-quality and Latency-speed criteria, not overwhelmingly (see
Abandoned Reasoning, "Dead End: Recommending outright rejection of the cache," which documents
the ruling-out). For chain C1: rival not settled — "read-QPS genuinely is the dominant load
driver in this system" remains live; this is exactly why C1 is rated LOW rather than concluding
either way. For chain C2: rival not settled — "most traffic hits a small, hot default/unfiltered
view" remains live. For chain C3: rival not settled — "current p95 offenders are simple popular
queries hitting an overloaded DB" remains live. For chain C4: **rival not applicable** — the
candidate rival ("an unmitigated stampede would be too small to matter") collapses into the same
unresolved magnitude question already carried as this chain's Rivals-axis shortfall on its own
confidence line, so it is not treated as a second, independent rival requiring its own §5 entry.

**Premise:** The hybrid plan has already failed — six months from now the organization either
wasted the upgrade spend anyway, or got caught with insufficient capacity and had to firefight.
What caused it?

**Causes (unfiltered, from three stakeholder viewpoints):**
1. *(Engineer)* The two-week cache implementation shipped without jittered TTL or stampede
   protection because of time pressure, causing periodic spikes.
2. *(Engineer)* Cache hit rate came in far below hoped-for because filter/sort/pagination
   combinations fragmented the key space, and nobody instrumented hit-rate-by-query-shape early
   enough to catch it.
3. *(Engineer)* Redis itself became a new latency/availability risk (restart, network blip)
   causing a cold-cache stampede that was never part of the original capacity model.
4. *(SRE/capacity owner)* The checkpoint bar was defined loosely ("looks like it's helping")
   rather than as a hard numeric threshold on a hard calendar date, so the decision slipped
   month after month until it was too late to re-order.
5. *(SRE/capacity owner)* A seasonal or marketing traffic spike inside the two-quarter window
   consumed the freed headroom faster than modeled, and by the time DB metrics turned red the
   procurement lead time had already made re-ordering impossible.
6. *(SRE/capacity owner)* The upgrade was actually sized for something other than read-QPS
   (write throughput, connection ceiling, a second service being onboarded), which the cache
   never touched — the clock ran out with the real driver still unaddressed.
7. *(Finance/procurement)* Once the architecture-review document suggested the upgrade "might
   not be needed," procurement informally slow-walked the order even without a formal
   cancellation, so part of the lead-time buffer was already spent by the checkpoint date.
8. *(Finance/procurement)* Budget for the next-tier instance was reallocated elsewhere the
   moment the document suggested it might be unnecessary, so even a "yes, we still need it"
   checkpoint result could not be acted on quickly.

**Clusters:**
- **Cluster A — cache hardening/reliability gap** (causes 1, 3) — bears on chain C4, A7, GT-1,
  GT-6.
- **Cluster B — hit-rate/mechanism uncertainty realized** (causes 2, 6) — bears on chains C1,
  C2, C3, and A1, A9, A10.
- **Cluster C — soft erosion of the reversible option** (causes 4, 5, 7, 8) — bears on chain C5,
  GT-8?, A11, A14, A19, A20.

**Disposition:**
- Cluster A — *plan change*: require jittered TTL, request-coalescing, and a Postgres-down
  circuit breaker as explicit ship-acceptance criteria for the cache, not optional hardening
  backlog; add a "Redis unavailable" fallback test before rollout.
- Cluster B — *plan change*: define the checkpoint as a hard numeric bar (e.g., a stated minimum
  reduction in listings-attributable DB CPU/IO and a stated minimum p95 improvement, measured
  over a stated stable window) on a hard calendar date set with margin before the procurement
  deadline; separately confirm what the upgrade was actually sized for before relying on the
  cache to substitute for it.
- Cluster C — *plan change plus accepted risk*: instruct procurement/finance in writing that the
  upgrade proceeds at normal priority and the budget hold remains until the checkpoint date
  passes or fails; name a single decision-owner who is not the platform team that authored the
  original claim; accept the residual risk that informal social deprioritization may still occur,
  mitigated by that named, independent ownership.

**Falsification:** This analysis's headline conclusion (adopt the hybrid; do not cancel the
upgrade yet) is false if a load-attribution and query-shape study, run before shipping anything,
shows conclusively that read-QPS is the dominant load driver, the listings key-space is small and
steeply skewed enough for a simple cache to clear a high hit rate, the p95 tail is dominated by
those same cache-hittable queries, and the resulting headroom provides a comfortably-verified
two-quarter runway — in which case canceling the upgrade immediately becomes the evidence-backed,
correct choice rather than the currently-unsupported one.

## §6→§4 closure ledger (process output)

- "Adopt the hybrid: ship the Redis read-through cache now... gating any actual deferral
  decision on a hard, pre-defined evidence checkpoint..." → chain C5 ✓
- "The claim bundles four independently uncertain mechanisms... gathering the evidence while
  doing the cheap-to-reverse thing first is the right move regardless of how C1–C4 eventually
  resolve" → chains C1, C2, C3, C4, C5 ✓
- "The hybrid costs slightly more in the worst realistic case... without which the hybrid's
  paper reversibility can quietly erode into the same one-way door option (a) represents" →
  chain C5 ✓
- "The specific cost of that coordination overhead was not separately quantified" → no chain —
  flagged assumption only ✓ (marker present, honestly discharged as untraced-by-design)
- "Confirm what the scheduled upgrade was actually sized for... (chain C1; chain C5)" → chains
  C1, C5 ✓
- "Pull a load-attribution breakdown... (chain C1)" → chain C1 ✓
- "Measure the listings endpoint's real query-key cardinality... (chain C2)" → chain C2 ✓
- "Break down p95 by query shape... (chain C3)" → chain C3 ✓
- "Confirm the cache implementation plan includes jittered TTL... (chain C4)" → chain C4 ✓
- "**Pre-check:** head C1 (LOW), C2 (LOW), C3 (LOW), C4 (LOW), C5 (LOW); GT-8?..." → chains
  C1–C5, GT-8? ✓ (named directly in the pre-check's own head field)
- "**Confidence:** LOW — every chain this conclusion rests on is rated LOW (C1–C5...)" → chains
  C1–C5, GT-8? ✓

Every surviving §6 claim carries a chain reference or the flagged-assumption marker; no claim
was cut.

## Self-audit scan (process output)

**Table 1 — chain form (section 4):**

| Chain | Chain Head (brief) | Form conforming? | Rule applied | Dependency clean? | Band | Act attempted? | Edges fired |
|---|---|---|---|---|---|---|---|
| C1 | GT-2 + GT-3 + GT-7? | yes | n/a | yes | LOW | yes | none |
| C2 | GT-5? + GT-9? | yes | n/a | yes | LOW | yes | none |
| C3 | GT-4 + C2 | yes | n/a | yes | LOW | yes | none |
| C4 | GT-1 + GT-6 | yes | n/a | yes | LOW | yes | none |
| C5 | C1 + C2 + C3 + C4 + GT-8? | yes | n/a | yes | LOW | no | none |

**Table 2 — claim inventory (section 6):**

| §6 Span (brief) | Construct | Claim under R11? | R11 clause applied | Chain cited |
|---|---|---|---|---|
| Recommended approach: adopt the hybrid... | bold lead-in | yes | colon closes bold span; one of the four prescribed lead-ins, always a claim | C5 |
| Key insight: claim bundles four mechanisms... | bold lead-in | yes | colon closes bold span; always a claim | C1, C2, C3, C4, C5 |
| Trade-offs acknowledged: hybrid costs slightly more... | bold lead-in | yes | colon closes bold span; always a claim | C5 |
| Cheapest de-risking evidence (highest priority first): | bold lead-in | no | colon-terminated span is the entire physical line, carries no citation of its own — section-intro label | n/a |
| - Confirm what the scheduled upgrade was actually sized for... | list item | yes | closes its own sentence, exceeds forty characters | C1, C5 |
| - Pull a load-attribution breakdown... | list item | yes | closes its own sentence, exceeds forty characters | C1 |
| - Measure the listings endpoint's real query-key cardinality... | list item | yes | closes its own sentence, exceeds forty characters | C2 |
| - Break down p95 by query shape... | list item | yes | closes its own sentence, exceeds forty characters | C3 |
| - Confirm the cache implementation plan includes jittered TTL... | list item | yes | closes its own sentence, exceeds forty characters | C4 |
| Pre-check: head C1 (LOW), C2 (LOW)... | bold lead-in | yes | colon closes bold span | C1, C2, C3, C4, C5, GT-8? |
| Confidence: LOW — every chain this conclusion rests on... | bold lead-in | yes | colon closes bold span; always a claim | C1, C2, C3, C4, C5, GT-8? |

Neither table's columns reach every limb its criterion bands on: Criterion 4 also draws on the
Abandoned Reasoning section (§5, quoted directly above) and the no-analogy-as-direct-evidence
ban (also §5's fourth dead end); Criterion 6 also draws on whether the Key Insight is a
non-obvious finding (quoted directly from §6 above, not from this table).

Scan complete: 5 chain rows, one per section-4 chain block in order; 11 section-6 rows, one per
construct in order — 10 claims under R11, 1 excluded. 0 chains malformed, 0 claims untraced.

## Self-Audit Gate (process output)

**Criterion 1: Identify Essence**
Quoted span: "Given that canceling/deferring the scheduled Postgres upgrade is expensive to
reverse (procurement lead time) while adopting the Redis cache is cheap to reverse before
rollout, does the evidence cited... actually establish that a read-through cache will cut p95
latency and database load enough to safely defer the upgrade for two quarters — and if not, what
decision sequencing correctly respects that reversibility asymmetry?"
Band: **Rigorous**
Justification: The statement names the specific decision (this claim, this reversibility
asymmetry) rather than a generic "should we cache" question, and each of the four success
criteria is a checkable verb+subject+outcome triplet scannable against sections 3, 4/5, and 6
respectively, with no wording reusable verbatim in an unrelated analysis.

**Criterion 2: Challenge Assumptions**
Quoted span: from the Assumption Audit scan — "A17 | yes", "A18 | yes", "A19 | yes", "A20 | yes"
— confirming the audit visited all 21 named chain steps and surfaced exactly four new
assumptions, folded back into the table above with full Type/Treatment/Verdict/Verification.
Band: **Rigorous**
Justification: Every one of the 20 rows uses one of the four canonical types, every Verdict cell
leads with Accept/Challenge and an em-dash justification, every unverified belief used in a
chain carries "unverified — flagged," and the audit table confirms the scan ran exhaustively
rather than being asserted.

**Criterion 3: Establish Ground Truths**
Quoted span: "?`-marked: GT-5, GT-7, GT-8, GT-9, GT-10 (5 of 10)." — checked against the Ground
Truths list, which carries `?` on exactly GT-5, GT-7, GT-8, GT-9, GT-10 and no others; the
enumeration matches.
Band: **Rigorous**
Justification: Every GT-ID is stable and matches its chain-head usage; every unsuffixed GT
(GT-1, GT-2, GT-3, GT-6) names a read-at-source location with a verbatim-quoted passage; GT-4 is
correctly treated as a definitional/physical-law type requiring no external source; no chain in
this analysis is rated HIGH, so the "every unsuffixed GT feeding a HIGH chain names its
read-at-source location" requirement holds vacuously; no Phase-2 Discard appears in the list.

**Criterion 4: Reason Upward**
Quoted span: from the self-audit scan's Table 1 — "C1 | GT-2 + GT-3 + GT-7? | yes | n/a | yes |
LOW | yes | none" through "C5 | ... | yes | n/a | yes | LOW | no | none" — all five chains score
`Form conforming? = yes` and `Dependency clean? = yes`.
Band: **Rigorous**
Justification: All five conclusions in section 6 have exactly one chain each in section 4, every
chain carries a genuine intermediate (not a restatement of a head input) plus a real conclusion,
every hop is one physical line with no leading `GT-N` identifier and no premature sentence
closure, four dead ends in §5 each give a specific structural abandonment reason (category
error, incomplete decomposition, dominated option, unsettled-not-ruled-out), no analogy is used
as direct evidence (§5's fourth dead end explicitly rejects "good engineers would surely do X" as
evidence), and every chain step introducing a new assumption (A7, A17, A18, A19, A20) carries an
inline `[Assumes: X]` mark confirmed by the Assumption Audit scan.

**Criterion 5: Validate**
Quoted span: from the Adversarial pass record — "Recompute," "Sensitivity," "Rival," "Premise,"
"Causes," "Clusters," "Disposition," and "Falsification" sections are all present, and each of
the three clusters carries a named disposition ("plan change," "plan change," "plan change plus
accepted risk") rather than a bare risk list.
Band: **Rigorous**
Justification: Every MEDIUM-or-LOW confidence line (all five chains plus the Conclusion) names
its `GT-N?` inputs with a specific verification, names cited `Cn` inputs rated below HIGH without
re-explaining them, and gives its own downgrade causes (short axes) with what would close them;
the ceiling rule is honored mechanically (C3 capped by C2's LOW, C5 capped by C1–C4's LOW); no
chain consuming a `GT-N?` input is rated HIGH; every band matches what its own three axes license
(none rated above or below); the adversarial pass ran in full with every cluster acted on.

**Criterion 6: Conclusion-to-Ground-Truth Traceability**
Quoted span: from the self-audit scan's Table 2 — every row from "Recommended approach" through
"Confidence" reads `Claim under R11? = yes` with a named chain in `Chain cited`, except the
section-intro label row, which correctly reads `no`; reconciliation line: "10 claims under R11,
1 excluded... 0 claims untraced."
Band: **Rigorous**
Justification: Every Conclusion-section claim traces to a named section-4 chain (or, for the one
caveat sentence, carries the explicit flagged-assumption marker rather than an unbacked claim);
no new reasoning is introduced in section 6 beyond what sections 4/5 established; the Key Insight
states a non-obvious decision-theoretic finding (mechanism confidence need not resolve for the
sequencing recommendation to be correct) rather than restating the Recommended Approach's action
items.

**Gate result:** No criterion scored Absent; zero criteria scored Hand-wavy (well under the
one-Hand-wavy cap). The gate clears on the first scoring pass — no Fix/Repeat re-perception pass
was required, and no bounded re-entry edge fired anywhere in this analysis (confirmed by the
"Edges fired: none" column in the self-audit scan's Table 1).
