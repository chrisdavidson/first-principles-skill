**Disclosed:** Missing input — no workload data was supplied: which resource triggers the scheduled upgrade, the cacheable share of its load, hit rates, growth rate, utilization, or current p95. AskUserQuestion was not available, so the analysis went ahead. Its formulas hold for any workload, and every workload number in it is an illustrative scenario value marked GT-9? or GT-7?. Re-entry edge fired — the Self-Audit Gate's Fix/Repeat loop. Trigger: Criterion 3 scored Hand-wavy on pass 1, because the read-at-source GT-5, GT-6 and GT-8 fed only MEDIUM chains. What changed: section 4 was restructured so that C1–C3 rest only on definitions, identities and sources that were read (now HIGH). All illustrative workload arithmetic moved into C5, and A-8 was flagged as unverified. Pass 2 cleared.

## Answer

**Recommendation:** Don't defer the upgrade on the strength of the claim as stated. First find out which resource triggers the upgrade and measure s, h_c and g. Defer only if the upgrade is read-bound and f = s × h_c ≥ 1 − (1 + g)^−2, and keep the upgrade ready rather than cancelling it (chain C5, chain C2).

**Band (from §6):** MEDIUM (chain C4, chain C5)

**Would change it:** Finding out which resource the capacity plan names as the trigger for the upgrade, and measuring the workload figures s, h_c and g (chain C5).

## 1. Problem Essence

**Core problem:** Under what measurable conditions does a Redis read-through cache in front of the Postgres listings API (a) lower p95 latency and (b) remove enough of the load on whichever resource triggers the scheduled vertical scale-up to move that trigger date at least two quarters later — and does the claim, as stated, establish those conditions?

**Success criteria:**

- The analysis states the condition for the load half as a formula over quantities the team can measure, and recomputes every figure it derives from that formula.
- The analysis states the condition for the p95 half separately, because latency and load depend on different hit-rate measures.
- The analysis says whether the claim as stated is supported, refuted, or conditional, and names the measurement that would settle it.
- The answer is allowed to be a combination (cache plus a kept-ready upgrade path, for example) rather than "cache instead of upgrade"; no criterion requires picking exactly one of the two options the claim contrasts.

Split/combination test (Phase 1): the claim frames cache *versus* upgrade. A composite — cache now, with the upgrade kept ready rather than cancelled — is carried as an option, because the second-order pass (chain C5) shows the deferral changes the database's failure tolerance.

## 2. Assumptions Table

| Assumption | Type | Treatment | Verdict | Verification |
|------------|------|-----------|---------|--------------|
| A-1: A read-through cache absorbs only reads; every write still reaches Postgres | physical law | Accept as ground-truth candidate (definition of the pattern) | Accept — follows from the definition recorded as GT-1 | GT-1 (definition) |
| A-2: Database load is additive across queries, so removing a set of queries removes their share of the binding resource | untested belief | Verify or flag | Accept — first-order approximation; under contention the real relief is at least this large for CPU-bound load, so the estimate errs conservative | unverified — flagged; measurable as per-query-class share via pg_stat_statements total execution time |
| A-3: The scheduled vertical-scale upgrade is driven by read load (CPU / memory / read I/O), not by writes, WAL, storage or connections | untested belief | Verify or flag | Challenge — the claim silently assumes it; nothing stated supports it; load-bearing | unverified — flagged as GT-7? |
| A-4: Listings requests hit the cache at a high rate | untested belief | Verify or flag | Challenge — listings endpoints with filters, sort orders, pagination and per-user fields have high key cardinality, which lowers hit rate | unverified — flagged as GT-9? |
| A-5: Cost-weighted hit rate equals request-count hit rate | untested belief | Verify or flag | Discard — hits concentrate on cheap hot-key reads and misses on expensive long-tail queries; with request hit rate 0.80 and misses costing 5x, cost-weighted hit rate is 0.444 (chain C5) | GT-2 identity; deduction in chain C1, worked in chain C5 |
| A-6: Load on the binding resource grows at one uniform compound rate g across cacheable and non-cacheable components | convention | Challenge before use | Accept — standard capacity-planning convention; if the non-cacheable component grows faster, the deferral is shorter than computed, so the threshold becomes necessary rather than sufficient | modelling convention; flagged on chain C2 |
| A-7: Cache misses have the same latency distribution as today's requests | untested belief | Verify or flag | Discard — misses are biased toward rare, uncacheable, slower queries; chain C3 does not use it | contradicted by the selection effect in GT-4's mixture; see section 5 |
| A-8: Every cache hit completes faster than every cache miss | untested belief | Verify or flag | Accept — a miss is a Redis lookup plus a Postgres query, so it exceeds the hit path of the same request; across requests it is an approximation whose failure blurs, but does not reverse, the quantile mapping | unverified — flagged; GT-8 sizes the hit path (about 200 us on 1 Gbit/s); priced on chain C3 |
| A-9: Postgres request queueing behaves like an M/M/1 queue | convention | Challenge before use | Accept — used only for direction and illustrative magnitude; the endpoint of chain C4 claims direction and requires measurement for size | GT-5 (formula read at source); applicability unverified — flagged |
| A-10: The upgrade fires at a fixed utilization threshold C | convention | Challenge before use | Accept — the deferral formula does not depend on C or on current utilization, so the convention's value does not matter (section 5) | GT-3 identity |
| A-11: Product accepts cached listings stale by the TTL (price, stock, availability) | current constraint | Record expiry conditions | Accept — holds only while product tolerates a TTL long enough for the needed hit rate; lapses if pricing/stock freshness requirements tighten | unverified — flagged; owned by product |
| A-12: "Defer for at least two quarters" means the threshold-crossing date moves two quarters later than the scheduled date | convention | Challenge before use | Accept — the only reading under which the claim is about the cache's effect rather than about current headroom | interpretation stated here |
| A-13: A cold or failed cache (deploy, eviction storm, Redis outage, synchronized TTL expiry) does not send more load to Postgres than the deferred instance can absorb | untested belief | Verify or flag | Challenge — surfaced by inversion; after deferral the database is sized for (1 − f) of demand; load-bearing for whether deferral is safe | unverified — flagged |
| A-14: On a miss the request pays the Redis lookup round trip in addition to the Postgres query | physical law | Accept as ground-truth candidate (sequence of the read-through pattern) | Accept — the lookup precedes the query by definition (GT-1); size from GT-8 | surfaced by the Assumption Audit at chain C3 |

## 3. Ground Truths

Reduce-to-primitives pass: "the cache defers the upgrade two quarters" reduces to (i) which queries the cache removes (definition, GT-1), (ii) how removed queries map to load on the binding resource (identity, GT-2), (iii) how a load reduction maps to time under growth (identity, GT-3), and (iv) which resource the upgrade is for (measurement not supplied, GT-7?). "p95 falls" reduces to the quantile of a hit/miss mixture (GT-4), the hit-path latency (GT-8) and miss-path queueing (GT-5, GT-6). Every branch bottoms out at a definition, a mathematical identity, a published figure read here, or an unsupplied measurement.

- **GT-1** Read-through cache definition: a request whose key is present is answered from the cache and issues no database query; a request whose key is absent looks up the cache, queries the database, and stores the result; writes are not intercepted. — source: definition of the pattern named in the claim; provenance: definition, stated here (no external figure asserted).
- **GT-2** Load-decomposition identity: if a fraction s of the binding resource's consumption comes from cacheable reads and a fraction h_c of that consumption is served by hits, the removed fraction is f = s × h_c and residual load is L1 = L0 × (1 − f). — source: arithmetic identity; provenance: derived in this analysis (the product of two shares), derivation shown in this entry.
- **GT-3** Threshold-crossing identity under compound growth: load L growing at rate g per quarter, L(t) = L(1+g)^t, reaches threshold C when (1+g)^t = C/L, i.e. after t = ln(C/L)/ln(1+g) quarters. — source: algebra on the compound-growth definition; provenance: derived in this analysis, derivation shown in this entry.
- **GT-4** Quantile of a two-population mixture: if a fraction h of requests are hits and every hit is faster than every miss, the overall 95th percentile lies in the hit population when h ≥ 0.95; when h < 0.95 it equals the q-quantile of the miss population with h + (1 − h)q = 0.95, i.e. q = (0.95 − h)/(1 − h). — source: definition of a quantile; provenance: derived in this analysis, derivation shown in this entry.
- **GT-5** M/M/1 mean response (sojourn) time is 1/(μ − λ); with service time S = 1/μ and utilization ρ = λ/μ this is S/(1 − ρ). — source: Wikipedia, "M/M/1 queue"; read-at-source: section "Response time", formula "1/(μ − λ)" (the S/(1 − ρ) form is the same expression divided through by μ).
- **GT-6** PostgreSQL already holds hot data in memory: the docs recommend shared_buffers at "25% of the memory in your system" and state "PostgreSQL also relies on the operating system cache". — source: PostgreSQL documentation, Server Configuration → Resource Consumption; read-at-source: the shared_buffers parameter description, both phrases quoted.
- **GT-7?** The resource whose exhaustion schedules the vertical-scale upgrade (CPU, memory, read I/O, write I/O / WAL, storage, or connection count) is not stated. — unverified: no capacity plan or metrics were supplied; no source exists to open.
- **GT-8** A Redis hit costs roughly one network round trip: Redis docs state "The typical latency of a 1 Gbit/s network is about 200 us" and that Redis processing is "usually ... in the sub microsecond range"; they also show virtualized intrinsic latency of 9.7 ms on a loaded VM. — source: redis.io, "Diagnosing latency issues"; read-at-source: section "Latency induced by network and communication" (200 us) and the introduction (sub-microsecond processing). Labelled a published typical value, not a measurement of this system.
- **GT-9?** The workload figures — cacheable share s, request hit rate h, cost-weighted hit rate h_c, growth rate g, current utilization ρ0, current p95 — are not supplied. Every numeric value of these used below is an illustrative input, never a measured one. — unverified: not supplied by the user; no source exists to open.

**Provenance summary:**

```text
?-marked: GT-7?, GT-9? (2 of 9)
Read-at-source: GT-5 — Wikipedia "M/M/1 queue", section "Response time"; GT-6 — PostgreSQL docs, shared_buffers description; GT-8 — redis.io "Diagnosing latency issues", section "Latency induced by network and communication"
Derived in this analysis (derivation shown in the entry): GT-2, GT-3, GT-4
Definition stated here: GT-1
Not read — no source exists: GT-7?, GT-9? (user-side measurements)
```

## 4. Derivation Chains

Chains C1–C4 are structural: they hold for any workload and use only definitions, identities and figures read at source. Chain C5 applies them to illustrative workload values from GT-9?, which are scenario inputs, never measurements. Every computed figure is recomputed in the adversarial pass record (appendix, Recompute).

### Conclusion C1: The cache removes f = s × h_c of the binding resource's load, where h_c is cost-weighted — and roughly nothing if the upgrade is write-bound

GT-1 (hits skip the DB; misses and writes reach it) + GT-2 (f = s × h_c) + GT-6 (Postgres already caches hot pages)
→ only the cacheable-read share s of the binding resource's consumption can be removed by the cache *[Assumes: A-2 — load additive over queries]*
→ the hit rate that governs load is h_c, weighted by per-query cost, which equals the request hit rate only when hit and miss queries cost the same
→ because hot pages already sit in Postgres memory, a hit on a hot key saves mainly CPU, executor and connection work rather than disk reads
→ if the binding resource is write I/O, WAL, storage or write connections, s ≈ 0 and so f ≈ 0 whatever the hit rate

**Pre-check:** head GT-1, GT-2, GT-6 · ?-marked: none · lowest cited: none · Inputs ceiling: HIGH
**Confidence:** HIGH — Inputs: GT-1 is a definition, GT-2 is derived in its entry, GT-6 was read at the PostgreSQL shared_buffers description. Inference: A-2 is priced — s is defined as the measured consumption share of cacheable queries, so f = s × h_c is exact for the consumption those queries account for; if load is not additive, contention effects add relief outside this endpoint without changing it. Rivals: "f equals s × request hit rate" is ruled out by this chain's second hop, recorded in section 5, Dead End "Request-count hit rate as the load measure".

### Conclusion C2: The deferral is Δt = −ln(1 − f)/ln(1 + g) quarters, independent of current utilization and threshold, so two quarters requires f ≥ 1 − (1 + g)^−2 — 17.36% at 10% quarterly growth

GT-2 (residual load L0 × (1 − f)) + GT-3 (crossing time ln(C/L)/ln(1 + g))
→ multiplying load by (1 − f) raises ln(C/L) by −ln(1 − f), so the crossing moves by Δt = −ln(1 − f)/ln(1 + g) *[Assumes: A-6 — uniform growth across components]*
→ current utilization L0 and threshold C both cancel out of Δt
→ two quarters of deferral requires (1 − f) ≤ (1 + g)^−2, that is f ≥ 1 − (1 + g)^−2
→ that threshold is 1 − 1/1.1025 = 9.30% at g = 5%, 1 − 1/1.21 = 17.36% at 10%, 1 − 1/1.3225 = 24.39% at 15%, and 1 − 1/1.5625 = 36.00% at 25%

**Pre-check:** head GT-2, GT-3 · ?-marked: none · lowest cited: none · Inputs ceiling: HIGH
**Confidence:** HIGH — Inputs: GT-2 and GT-3 are identities derived in their entries. Inference: every hop is algebra that recomputes (appendix, Recompute). A-6 is priced — if the non-cacheable component grows faster than the cacheable one, Δt is shorter than the formula, so the threshold remains a necessary floor and the endpoint stands. Rivals: "deferral depends on current headroom" is ruled out by the second hop, recorded in section 5, Dead End "Deferral computed from current headroom".

### Conclusion C3: p95 falls from the hit/miss mix only if some of today's slowest 5% of requests become hits; below a 95% request hit rate the p95 sits in the miss population

GT-1 (a miss does the cache lookup before the query) + GT-4 (mixture quantile) + GT-8 (a hit costs about one 200 us round trip)
→ for latency the relevant hit rate is the request-count rate h, not the cost-weighted h_c that governs load *[Assumes: A-8 — hits faster than misses]*
→ when h ≥ 0.95 the overall p95 lies inside the hit population and drops to roughly cache round-trip latency
→ when h < 0.95 the overall p95 is the miss population's q-quantile, q = (0.95 − h)/(1 − h): 0.15/0.20 = 0.75 at h = 0.80, and 0.35/0.40 = 0.875 at h = 0.60
→ if every request in today's slowest 5% would be a miss, the number of requests slower than today's p95 is unchanged by caching the others
→ in that case p95 rises by the Redis lookup each miss now pays, unless queueing relief on misses offsets it *[Assumes: A-14 — misses pay the lookup round trip]*

**Pre-check:** head GT-1, GT-4, GT-8 · ?-marked: none · lowest cited: none · Inputs ceiling: HIGH
**Confidence:** HIGH — Inputs: GT-1 is a definition, GT-4 is derived in its entry, GT-8 was read at redis.io, section "Latency induced by network and communication". Inference: A-8 is priced — if some hits are slower than some misses the q mapping becomes approximate, but the endpoint's slowest-5% test counts requests above a fixed latency and does not use A-8; A-14 follows from GT-1's sequence. Rivals: "any hit rate lowers p95" is ruled out by the fourth hop, recorded in section 5, Dead End "Hits are faster, so p95 must fall".

### Conclusion C4: Lower database utilization shortens miss-path queueing, so a miss-dominated p95 can still fall — by an amount that must be measured, not computed

GT-1 (hits issue no query) + GT-5 (M/M/1 response S/(1 − ρ))
→ removing f of the query load moves utilization from ρ0 to ρ0 × (1 − f) *[Assumes: A-9 — M/M/1 applies]*
→ for an illustrative ρ0 = 0.70, mean response is S/0.30 = 3.333 S before the cache
→ with f = 0.68, ρ = 0.70 × 0.32 = 0.224, so response is S/0.776 = 1.289 S
→ with f = 0.18, ρ = 0.70 × 0.82 = 0.574, so response is S/0.426 = 2.347 S
→ miss-path latency therefore falls through load relief even when the hit/miss mix alone leaves p95 in the miss population
→ the magnitude is model-dependent, so the p95 effect must be measured under a load test rather than taken from this formula

**Pre-check:** head GT-1, GT-5 · ?-marked: none · lowest cited: none · Inputs ceiling: HIGH
**Confidence:** MEDIUM — Inference axis short: the first hop rests on A-9 (Postgres queueing behaves like M/M/1), and the analysis has no cited regularity that response time falls with utilization for the queue Postgres actually is; it is closed by a load test plotting miss-path latency against database utilization. Inputs are clean (GT-5 read at Wikipedia, section "Response time"). Rivals: "load relief is negligible at low utilization" does not compete with the endpoint, which already leaves magnitude to measurement.

### Conclusion C5: The claim is a testable conditional, not a supported statement — and deferring the upgrade makes Redis availability-critical

C1 (removable fraction, HIGH) + C2 (two-quarter threshold, HIGH) + C3 (p95 slowest-5% test, HIGH) + C4 (miss-path relief, MEDIUM) + GT-7? (binding resource unknown) + GT-9? (workload figures unknown)
→ illustrative: request hit rate 0.80, misses costing 5 units and hits 1, gives h_c = 0.80/(0.80 + 0.20 × 5) = 0.80/1.80 = 0.444 *[Assumes: A-4 — illustrative workload]*
→ illustrative: with s = 0.85 that gives f = 0.85 × 0.444 = 0.378, where the request hit rate would suggest 0.85 × 0.80 = 0.68
→ at g = 10% (ln 1.10 = 0.09531), f = 0.378 defers −ln(0.622)/0.09531 = 0.4745/0.09531 = 4.98 quarters
→ at g = 10%, the optimistic f = 0.68 defers −ln(0.32)/0.09531 = 1.1394/0.09531 = 11.96 quarters
→ at g = 10%, a pessimistic high-cardinality f = 0.60 × 0.30 = 0.18 defers −ln(0.82)/0.09531 = 0.1985/0.09531 = 2.08 quarters
→ at g = 15% (ln 1.15 = 0.13976), the same f = 0.18 defers 0.1985/0.13976 = 1.42 quarters, so the claim fails there
→ the load half therefore holds if and only if the upgrade is read-bound and f = s × h_c ≥ 1 − (1 + g)^−2
→ the latency half holds if and only if some of today's slowest 5% become hits or load relief on misses exceeds the added Redis lookup
→ nothing the claim states establishes either condition, so as stated it is a conditional to be tested rather than a supported prediction
→[2nd] (actor lens — SRE / on-call) a database sized for (1 − f) of demand cannot absorb a cold or failed cache, so Redis becomes availability-critical *[Assumes: A-13 — cold-cache load fits the deferred instance]*
→[2nd] (actor lens — product and customers) TTLs long enough for a high h_c serve stale price and stock, so freshness pressure shortens TTLs and lowers h_c *[Assumes: A-11 — staleness tolerated]*
→[2nd] (time lens — a few quarters) catalog and filter-combination growth enlarge the key space, so h_c and therefore f decay after launch
→[3rd] (time lens — long run) Δt is a one-time shift of the crossing date, so the upgrade is deferred rather than avoided and the cache becomes an assumed part of database capacity

**Pre-check:** head C1 (HIGH), C2 (HIGH), C3 (HIGH), C4 (MEDIUM), GT-7?, GT-9? · ?-marked: GT-7?, GT-9? · lowest cited: MEDIUM · Inputs ceiling: MEDIUM
**Confidence:** MEDIUM — Inputs axis short: GT-7? (which resource triggers the upgrade) is removed by reading the capacity plan or metric that scheduled it; GT-9? (s, h, h_c, g) is removed by measuring per-query-class share of that resource from pg_stat_statements total execution time, replaying logged request keys against the intended TTL, and fitting the resource's quarterly trend; C4 is MEDIUM. The A-4 mark makes the scenario hops illustrative only; the endpoint does not rest on their values, only on there being read-bound scenarios on both sides of the threshold. The A-13 and A-11 marks qualify second-order extensions, not the endpoint. Rivals "holds as stated" and "false as stated" are ruled out in section 5, Dead End "Unconditional verdicts". Second-order contradiction check: no extension contradicts a ground truth; the SRE extension works against the success criterion that deferral must not trade capacity for availability risk, and is carried into the Conclusion's trade-offs.

## 5. Abandoned Reasoning

### Dead End: Request-count hit rate as the load measure

**What was tried:** Estimating database relief as s × h with h the request-count hit rate (0.85 × 0.80 = 0.68).

**Why abandoned:** Load is consumed per unit of query cost, not per request; GT-2 requires the cost-weighted share. Hits concentrate on cheap hot-key reads, and h_c equals the request rate only when hit and miss costs are equal (chain C1); with misses costing 5x the cost-weighted rate is 0.444, giving f = 0.378 (chain C5). A-5 was discarded on this basis.

**What it ruled out:** Quoting the cache's hit-rate dashboard as the database saving; it over-states f whenever misses are more expensive than hits.

### Dead End: Deferral computed from current headroom

**What was tried:** Computing the crossing date with and without the cache from an illustrative current utilization 0.70 and threshold 0.80 at g = 10%: t0 = ln(0.80/0.70)/0.09531 = 0.13353/0.09531 = 1.40 quarters; t1 = ln(0.80/0.224)/0.09531 = 1.27297/0.09531 = 13.36 quarters.

**Why abandoned:** The difference, 13.36 − 1.40 = 11.96 quarters, equals −ln(1 − 0.68)/ln 1.10 exactly; current utilization and threshold cancel (GT-3, chain C2). Headroom decides *when* the upgrade is due, not *how far* the cache moves it.

**What it ruled out:** The need to know current utilization or the scale-up threshold to test the two-quarter claim; only f and g matter.

### Dead End: Hits are faster, so p95 must fall

**What was tried:** Reasoning that any non-zero hit rate lowers p95 because hits are faster than database reads, implicitly assuming misses keep today's latency distribution (A-7).

**Why abandoned:** Misses are a selected population — the rare, uncacheable, often slowest queries. Under GT-4, if today's slowest 5% are all misses, the count of requests slower than today's p95 is unchanged and p95 rises by the lookup round trip (chain C3). A-7 was discarded on this basis.

**What it ruled out:** Reading a mean-latency improvement or a high hit rate as evidence of a p95 improvement.

### Dead End: Unconditional verdicts

**What was tried:** Two rival headline conclusions from the same ground truths: "the claim holds as stated" and "the claim is false as stated".

**Why abandoned:** "Holds as stated" is ruled out by chain C1 — if the upgrade is write-bound, f ≈ 0 and Δt = 0 whatever the hit rate. "False as stated" is ruled out by chain C2's threshold — any read-bound workload removing more than 17.36% at 10% quarterly growth defers more than two quarters; the f = 0.378 scenario in chain C5 defers 4.98.

**What it ruled out:** Any verdict on the claim that does not first name the binding resource and measure f and g; the claim's truth value is not decidable from its own content (chain C5).

## 6. Conclusion

**Recommended approach:** Do not schedule the deferral on the claim as stated; first identify the resource that triggers the upgrade, measure s, h_c and g, and defer only if the upgrade is read-bound and f = s × h_c ≥ 1 − (1 + g)^−2 — keeping the upgrade ready rather than cancelled (chain C5, chain C2).

**Key insight:** The deferral depends only on the removed fraction and the growth rate, Δt = −ln(1 − f)/ln(1 + g), independent of current utilization; at 10% quarterly growth the cache must remove at least 17.36% of the binding resource's load, and it removes about nothing if the upgrade is write-bound (chain C2, chain C1).

**Latency condition:** Below a 95% request hit rate the p95 sits in the miss population, so p95 falls only if some of today's slowest 5% become hits or miss-path queueing relief outweighs the added Redis lookup (chain C3, chain C4).

**Trade-offs acknowledged:** Deferring makes Redis availability-critical, because a database sized for (1 − f) of demand cannot absorb a cold or failed cache, and TTLs long enough for a high hit rate serve stale price and stock (chain C5).

**Pre-check:** head C1 (HIGH), C2 (HIGH), C3 (HIGH), C4 (MEDIUM), C5 (MEDIUM), GT-7? · ?-marked: GT-7? · lowest cited: MEDIUM · Inputs ceiling: MEDIUM
**Confidence:** MEDIUM — the structural results in chains C1, C2 and C3 are HIGH; the Conclusion is MEDIUM because it also rests on chain C4 (MEDIUM, M/M/1 applicability) and chain C5 (MEDIUM, unmeasured workload), and directly on GT-7?, which is removed as a cause of the downgrade by identifying the resource named in the capacity plan that scheduled the upgrade.

## Appendix — process output

## Assumption Audit scan (process output)

| Chain | Step | Step Text (brief) | Assumption surfaced? | Added to Table? |
|---|---|---|---|---|
| C1 | 1 | only cacheable-read share s removable | A-2 (load additive) | already in table |
| C1 | 2 | load-relevant hit rate is cost-weighted h_c | A-5 (challenged) | already in table |
| C1 | 3 | hot-key hits save CPU/executor, not disk reads | none | n/a |
| C1 | 4 | write-bound upgrade gives f ≈ 0 | A-1, A-3 | already in table |
| C2 | 1 | Δt = −ln(1−f)/ln(1+g) | A-6 (uniform growth) | already in table |
| C2 | 2 | L0 and C cancel | A-10 (fixed threshold) | already in table |
| C2 | 3 | two quarters needs f ≥ 1 − (1+g)^−2 | A-12 (meaning of "defer") | already in table |
| C2 | 4 | thresholds 9.30 / 17.36 / 24.39 / 36.00 % | none | n/a |
| C3 | 1 | latency uses request-count h | A-8 (hits faster than misses) | already in table |
| C3 | 2 | h ≥ 0.95 puts p95 in hit population | none | n/a |
| C3 | 3 | q = 0.75 at h = 0.80, 0.875 at h = 0.60 | none | n/a |
| C3 | 4 | slowest 5% all misses leaves count unchanged | A-7 (discarded; not used) | already in table |
| C3 | 5 | p95 rises by the lookup each miss pays | A-14 (miss pays lookup round trip) | yes — added as A-14 |
| C4 | 1 | ρ moves to ρ0 × (1 − f) | A-9 (M/M/1), A-2 | already in table |
| C4 | 2 | 3.333 S at illustrative ρ0 = 0.70 | none | n/a |
| C4 | 3 | ρ = 0.224, response 1.289 S at f = 0.68 | none | n/a |
| C4 | 4 | ρ = 0.574, response 2.347 S at f = 0.18 | none | n/a |
| C4 | 5 | miss-path latency falls through relief | none | n/a |
| C4 | 6 | magnitude model-dependent, must be measured | none | n/a |
| C5 | 1 | h_c = 0.80/1.80 = 0.444 | A-4 (illustrative workload) | already in table |
| C5 | 2 | f = 0.85 × 0.444 = 0.378 vs 0.68 | none | n/a |
| C5 | 3 | f = 0.378, g = 10% gives 4.98 quarters | none | n/a |
| C5 | 4 | f = 0.68 gives 11.96 quarters | none | n/a |
| C5 | 5 | f = 0.60 × 0.30 = 0.18 gives 2.08 quarters | A-4 (high key cardinality) | already in table |
| C5 | 6 | g = 15%, f = 0.18 gives 1.42 | none | n/a |
| C5 | 7 | load half iff read-bound and f ≥ threshold | A-3 | already in table |
| C5 | 8 | latency half iff slowest-5% hits or relief > lookup | none | n/a |
| C5 | 9 | claim is a testable conditional | none | n/a |
| C5 | 10 | [2nd] Redis becomes availability-critical | A-13 (cold-cache load fits) | already in table (surfaced by inversion) |
| C5 | 11 | [2nd] staleness pressure lowers h_c | A-11 | already in table |
| C5 | 12 | [2nd] key-space growth decays h_c | none | n/a |
| C5 | 13 | [3rd] one-time shift, deferred not avoided | none | n/a |

Re-run after the Fix pass restructured section 4 (see the Self-Audit Gate's Pass 1 line); rows are against the current text.

## Techniques not applied (process output)

Techniques not applied:
- theoretical-limit (Phase 1) — not applicable — the essence does not hinge on whether a current figure is a convention or a hard bound; the question is a conditional about workload shares
- theoretical-limit (Phase 4) — not applicable — no conclusion needs a law-permitted ceiling; the deferral formula is an exact identity, not a bound against convention
- fishbone (Phase 2) — not applicable — the assumption space was enumerable directly (14 rows) and is not multi-causal diagnosis
- trade-off (Phase 4) — not applicable — the request is to evaluate a claim, not to choose between surviving options; the composite (cache plus a kept-ready upgrade) is carried in the recommendation rather than scored
- pre-mortem (Phase 5) — not applicable — the conclusion under test is a claim, so inversion is the Phase 5 technique under the decision rule

Applied: inversion (Phase 2, surfacing A-3 and A-13; Phase 5, adversarial pass), five-whys reduce-to-primitives (Phase 3), estimate (Phase 4, bracketed f and Δt across scenarios), second-order (Phase 4, chain C5).

## Adversarial pass (process output)

**Recompute** — every figure redone independently of the chain text: rational figures with an exact-fraction calculator, logarithms with a separate floating-point evaluation.

| Figure (chain) | Arithmetic | Recomputed | Chain states | Holds? |
|---|---|---|---|---|
| threshold at g = 5% (C2) | 1 − 1/1.05² = 1 − 1/1.1025 | 41/441 ≈ 0.09297 | 9.30% | yes |
| threshold at g = 10% (C2) | 1 − 1/1.21 | 21/121 ≈ 0.17355 | 17.36% | yes |
| threshold at g = 15% (C2) | 1 − 1/1.3225 | 129/529 ≈ 0.24386 | 24.39% | yes |
| threshold at g = 25% (C2) | 1 − 1/1.5625 | 9/25 = 0.36 | 36.00% | yes |
| request-rate f (C5) | 0.85 × 0.80 | 17/25 = 0.68 | 0.68 | yes |
| h_c (C5) | 0.80/(0.80 + 0.20 × 5) | 4/9 ≈ 0.4444 | 0.444 | yes |
| cost-weighted f (C5) | 0.85 × 4/9 | 17/45 ≈ 0.3778 | 0.378 | yes |
| pessimistic f (C5) | 0.60 × 0.30 | 9/50 = 0.18 | 0.18 | yes |
| ln 1.10, ln 1.15 (C5) | natural log | 0.095310, 0.139762 | 0.09531, 0.13976 | yes |
| Δt, f = 17/45, g = 10% (C5) | −ln(28/45)/0.095310 | 4.978 | 4.98 | yes |
| Δt, f = 0.68, g = 10% (C5) | −ln(0.32)/0.095310 = 1.13943/0.095310 | 11.955 | 11.96 | yes |
| Δt, f = 0.18, g = 10% (C5) | −ln(0.82)/0.095310 = 0.19845/0.095310 | 2.082 | 2.08 | yes |
| Δt, f = 0.18, g = 15% (C5) | 0.19845/0.139762 | 1.420 | 1.42 | yes |
| t0, t1 (section 5) | ln(0.80/0.70)/0.09531; ln(0.80/0.224)/0.09531 | 1.401; 13.356; difference 11.955 | 1.40; 13.36; 11.96 | yes — difference equals the C2 Δt for f = 0.68, confirming the cancellation stated in C2 |
| q at h = 0.80, 0.60 (C3) | 0.15/0.20; 0.35/0.40 | 3/4; 7/8 | 0.75; 0.875 | yes |
| ρ after cache (C4) | 0.70 × 0.32; 0.70 × 0.82 | 28/125 = 0.224; 287/500 = 0.574 | 0.224; 0.574 | yes |
| R/S (C4) | 1/0.30; 1/0.776; 1/0.426 | 10/3 ≈ 3.333; 125/97 ≈ 1.2887; 500/213 ≈ 2.3474 | 3.333; 1.289; 2.347 | yes |
| low-ρ rival bound (C4) | 1/(1 − 0.3) | 10/7 ≈ 1.4286 | 1.43 S | yes |

Direction checks: Δt increases with f and decreases with g in every row; residual utilization is below ρ0 in every row; R/S falls as ρ falls. No figure lands outside where its operation puts it. One defect found and fixed during recompute: the pessimistic f = 0.18 appeared without its derivation; its hop (now in C5 after the Fix pass) states 0.60 × 0.30, and two-scenario hops were split into one inference each.

**Sensitivity** — the single ground truth whose falsity flips the headline is GT-7? (binding resource): if the upgrade is write-, WAL-, storage- or connection-bound, f ≈ 0 and the load half of the claim fails regardless of every other figure. It is `?`-marked and cannot be verified here (no source exists); a confidence caveat is carried on C5 and the Conclusion. Weakest link per chain: C1 — the additivity hop (A-2, priced); C2 — the uniform-growth hop (A-6, priced); C3 — the request-hit-rate hop (A-8, priced); C4 — the M/M/1 applicability hop (A-9, unpriced, the reason C4 is MEDIUM); C5 — the illustrative h_c hop (GT-9?) and the SRE second-order extension (A-13).

**Rival** — headline (C5): "the claim holds as stated" and "the claim is false as stated" → section 5, Dead End "Unconditional verdicts". C1: "f equals request hit rate × s" → section 5, Dead End "Request-count hit rate as the load measure". C2: "deferral depends on current headroom" → section 5, Dead End "Deferral computed from current headroom". C3: "any hit rate lowers p95" → section 5, Dead End "Hits are faster, so p95 must fall". C4: "load relief is negligible" — live below ρ0 ≈ 0.3, named on C4's confidence line.

**Premise** — The claim is already false: the cache shipped, and two quarters later the Postgres upgrade went ahead on its original date anyway — or p95 got worse.

**Causes** — unfiltered, by viewpoint:
- DBA / capacity planner: the upgrade was scheduled for write IOPS and WAL volume from inventory and price updates; storage growth forced it; connection count from more app pods drove it; autovacuum on the hot listings table was the CPU consumer; the hit rate quoted was request-weighted and the expensive searches all missed.
- SRE / on-call: a Redis failover sent full read load to Postgres and it fell over; a deploy flushed the cache and the cold start saturated the database; thousands of keys set with the same TTL expired together and stampeded the database; Redis memory filled and evictions dropped the hit rate.
- Product manager / customers: stale prices drew complaints, TTL was cut to 30 s and the hit rate collapsed; personalized and logged-in listings bypassed the cache; new filters multiplied the key space.
- Finance / growth: a marketing push lifted growth to 25%/quarter, so the 0.18 removed load bought 0.89 quarters (−ln 0.82/ln 1.25 = 0.19845/0.22314); growth landed in filtered search, which is uncacheable.
- Heavy API client / crawler (an adversary to the cache): a faster API invited more scraping; crawlers walked deep pagination, every request a miss, and the slowest 5% stayed exactly where they were.

Recompute of the figure introduced here: ln 1.25 = 0.22314; 0.19845/0.22314 = 0.889 quarters.

**Clusters**
- K1 Wrong resource — the upgrade is not read-bound (bears on GT-7?, C1, C5). Triage: fatal.
- K2 Removed fraction over-estimated — request-weighted hit rate, high key cardinality, TTL cuts, personalization (bears on GT-9?, A-4, A-5, A-11, C1). Triage: costly but survivable.
- K3 Growth outruns the one-time shift — g higher than planned or concentrated in uncacheable traffic (bears on GT-9?, A-6, C2). Triage: costly but survivable.
- K4 Cache failure overloads a database sized for (1 − f) of demand (bears on A-13, C5). Triage: fatal.
- K5 p95 tail is uncacheable — slowest 5% are misses (bears on C3, C4). Triage: tolerable for the service, fatal for the latency half of the claim.

**Disposition**
- K1 — plan change: identify the binding resource before any deferral decision (the Recommendation's first step). Tripwire: none needed in operation — it is a precondition checked once by the capacity planner.
- K2 — plan change: measure h_c by cost via request-log replay before launch. Tripwire: measured f on the binding resource below 1 − (1+g)^−2 four weeks after launch; owner: capacity planner, reviewed at the monthly capacity review.
- K3 — accepted risk with mitigation: re-fit g quarterly and recompute Δt. Tripwire: quarterly growth on the binding resource above the planning g; owner: capacity planner.
- K4 — plan change: keep the upgrade ready rather than cancelled (the composite carried in the Recommendation), add request coalescing, jittered TTLs and serve-stale-on-error; accepted residual risk. Tripwire: Postgres utilization during any cache restart or failover drill exceeding the threshold C; owner: SRE, observed in a scheduled cold-cache drill.
- K5 — plan change: tag today's slowest 5% as cacheable or not before claiming a p95 win, and load-test the miss path. Tripwire: p95 after launch not below p95 before; owner: API team dashboard.

Each cluster lands on the analysis: K1 and K2 are the Inputs-axis caveats on C5 and the Conclusion; K3 is the A-6 caveat on C2; K4 is the Trade-offs line in section 6; K5 is the endpoint of C3.

**Falsification** — the conclusion that the claim is a conditional governed by f ≥ 1 − (1+g)^−2 and the slowest-5% test is false if a deployment shows the threshold crossing moving two or more quarters with measured f below 1 − (1+g)^−2 under steady g, or p95 falling while every request in the former slowest 5% remained a miss and database utilization did not change.

## §6→§4 closure ledger (process output)

- "Recommended approach: do not schedule the deferral on the claim as stated; identify the resource, measure s, h_c and g, defer only if read-bound and f ≥ 1 − (1+g)^−2, keep the upgrade ready" → chain C5, chain C2 ✓
- "Key insight: Δt = −ln(1 − f)/ln(1 + g), independent of utilization; 17.36% at 10% growth; about nothing if write-bound" → chain C2, chain C1 ✓
- "Latency condition: below 95% request hit rate p95 sits in the miss population; falls only if slowest 5% become hits or relief outweighs lookup" → chain C3, chain C4 ✓
- "Trade-offs acknowledged: deferring makes Redis availability-critical; long TTLs serve stale price and stock" → chain C5 ✓
- "Pre-check: head C1–C3 (HIGH), C4–C5 (MEDIUM), GT-7? · Inputs ceiling MEDIUM" → chain C1, C2, C3, C4, C5 ✓
- "Confidence: MEDIUM — C1–C3 HIGH; MEDIUM via C4, C5 and GT-7?" → chain C1, C2, C3, C4, C5 ✓

Ledger rows re-verified against section 4 after the Fix pass re-banded C1–C3; no chain was added, removed or renamed.

No claim cut.

## Self-audit scan (process output)

| Chain | Chain Head (brief) | Form conforming? | Rule applied | Dependency clean? | Band | Act attempted? | Edges fired |
|---|---|---|---|---|---|---|---|
| C1 | GT-1 + GT-2 + GT-6 | yes | n/a | yes | HIGH | yes | Fix/Repeat |
| C2 | GT-2 + GT-3 | yes | n/a | yes | HIGH | no | Fix/Repeat |
| C3 | GT-1 + GT-4 + GT-8 | yes | n/a | yes | HIGH | yes | Fix/Repeat |
| C4 | GT-1 + GT-5 | yes | n/a | yes | MEDIUM | yes | Fix/Repeat |
| C5 | C1 + C2 + C3 + C4 + GT-7? + GT-9? | yes | n/a | yes | MEDIUM | no | Fix/Repeat |

Form notes: every hop of every chain, including positions past the second hop that the mechanical check does not reach, was inspected against the head grammar, the GT-led-hop rule and the terminal-punctuation rule; no violation found.

Act notes: C1 — GT-6 read at the PostgreSQL docs; C3 — GT-8 read at redis.io; C4 — GT-5 read at Wikipedia. C2 has no openable source on its head (GT-2 and GT-3 are derived here), and C5's ?-marked inputs GT-7? and GT-9? have no source to open, so no read was attempted for them. Rows re-run against section 4 after the Fix pass.

| §6 Span (brief) | Construct | Claim under R11? | R11 clause applied | Chain cited |
|---|---|---|---|---|
| Recommended approach: do not schedule the deferral … | bold lead-in | yes | prescribed lead-in, colon closes the bold span | C5, C2 |
| Key insight: deferral depends only on f and g … | bold lead-in | yes | prescribed lead-in, colon closes the bold span | C2, C1 |
| Latency condition: below 95% … | bold lead-in | yes | bold lead-in whose colon closes the bold span | C3, C4 |
| Trade-offs acknowledged: Redis availability-critical … | bold lead-in | yes | prescribed lead-in, colon closes the bold span | C5 |
| Pre-check: head C1–C3 HIGH, C4–C5 MEDIUM, GT-7? … | bold lead-in | yes | bold lead-in whose colon closes the bold span (pre-check is a claim per template) | C1, C2, C3, C4, C5 |
| Confidence: MEDIUM … | bold lead-in | yes | prescribed lead-in, discharged through the chains it names | C1, C2, C3, C4, C5 |

```text
Scan complete: 5 chain rows, one per section-4 chain block in order; 6 section-6 rows, one per construct in order — 6 claims under R11, 0 excluded. 0 chains malformed, 0 claims untraced.
```

## Self-Audit Gate (process output)

**Pass 1 (before re-score):** Criterion 1 Rigorous · Criterion 2 Sound · Criterion 3 Hand-wavy · Criterion 4 Sound · Criterion 5 Rigorous · Criterion 6 Rigorous · Gate cleared: yes · Hand-wavy cap cleared: yes

Pass 1 findings acted on by the Fix step: Criterion 3 — GT-5, GT-6 and GT-8 were read at source yet fed only MEDIUM chains, because every structural chain also carried the illustrative workload input GT-9?; section 4 was restructured so C1–C3 carry only definitions, identities and read sources (now HIGH) and all illustrative workload arithmetic moved into C5. Criterion 2 — A-8 was used in chain C3 unverified without the "unverified — flagged" notation; fixed. Criterion 4 — C1's cost-weighting hop carried an undeclared empirical premise ("hits concentrate on cheap hot-key reads"); the hop now states the deduction from GT-2 and the illustrative cost ratio sits in C5 under [Assumes: A-4]. The Assumption Audit scan, self-audit scan and closure ledger were re-run against the revised text.

**Criterion 1: Identify Essence**
Quoted span: "Under what measurable conditions does a Redis read-through cache in front of the Postgres listings API (a) lower p95 latency and (b) remove enough of the load on whichever resource triggers the scheduled vertical scale-up to move that trigger date at least two quarters later — and does the claim, as stated, establish those conditions?"
Band: **Rigorous**
Justification: One sentence naming the decision-relevant question (conditions on the binding resource, not the claim restated), with success criteria each checkable against section 6 (a formula for the load half, a separate p95 condition, a supported/refuted/conditional verdict) and an explicit refusal to force a one-option answer.

**Criterion 2: Challenge Assumptions**
Quoted span: "| C3 | 5 | p95 rises by the lookup each miss pays | A-14 (miss pays lookup round trip) | yes — added as A-14 |" (Assumption Audit scan) and, from section 2, "A-8: Every cache hit completes faster than every cache miss | untested belief | … | unverified — flagged; GT-8 sizes the hit path"
Band: **Rigorous**
Justification: All 14 rows use the four-type scheme with em-dash verdicts, four are challenged and two discarded, every unverified belief used in a chain reads "unverified — flagged", and the audit scan covers all 32 section-4 hops in order and surfaced one new assumption into the table.

**Criterion 3: Establish Ground Truths**
Quoted span: enumerated "?-marked: GT-7?, GT-9? (2 of 9)"; the list carries `?` on exactly GT-7? and GT-9?. Unsuffixed read sources: GT-6 feeds C1 (HIGH), GT-8 feeds C3 (HIGH), GT-5 feeds only C4 (MEDIUM).
Band: **Sound**
Justification: IDs are stable, provenance labels are present, the enumeration matches the list and every read GT names its location, but one unsuffixed GT with a reachable, read source (GT-5) feeds only a MEDIUM chain — the single-GT shortfall the Sound band names; this is an unresolved gap carried with C4's caveat (its MEDIUM is from the unpriced A-9 applicability, which no available reading closes).

**Criterion 4: Reason Upward**
Quoted span: "| C1 | GT-1 + GT-2 + GT-6 | yes | n/a | yes | HIGH | yes | Fix/Repeat |" … "| C5 | C1 + C2 + C3 + C4 + GT-7? + GT-9? | yes | n/a | yes | MEDIUM | no | Fix/Repeat |" (self-audit scan); and from section 4, "→ because hot pages already sit in Postgres memory, a hit on a hot key saves mainly CPU, executor and connection work rather than disk reads"
Band: **Rigorous**
Justification: Every chain is form-conforming and dependency-clean with a genuine intermediate, each hop follows by deduction, recomputed arithmetic or a regularity cited to an unsuffixed GT (GT-6 above), every premise-carrying hop declares `[Assumes: A-N]`, no analogy is used as evidence, and section 5 records four dead ends each with What-was-tried / Why-abandoned / What-it-ruled-out.

**Criterion 5: Validate**
Quoted span: "**Confidence:** MEDIUM — Inference axis short: the first hop rests on A-9 (Postgres queueing behaves like M/M/1), and the analysis has no cited regularity … it is closed by a load test plotting miss-path latency against database utilization."
Band: **Rigorous**
Justification: Each chain's band is the one its axes license — C1–C3 HIGH with every assumption priced and rivals pointed to section 5, C4 MEDIUM on a named Inference shortfall, C5 MEDIUM naming GT-7?, GT-9? and C4 with verifications — the Conclusion's MEDIUM equals its weakest contributing chain, weakest links are named per chain, and the adversarial pass record carries Recompute, Sensitivity, Rival, a past-tense Premise, a five-viewpoint cause list, clusters citing chain/GT ids, a disposition per cluster, and Falsification.

**Criterion 6: Conclusion-to-Ground-Truth Traceability**
Quoted span: "| Key insight: deferral depends only on f and g … | bold lead-in | yes | prescribed lead-in, colon closes the bold span | C2, C1 |" (self-audit scan); and from section 6, "The deferral depends only on the removed fraction and the growth rate, Δt = −ln(1 − f)/ln(1 + g), independent of current utilization"
Band: **Rigorous**
Justification: All six section-6 claims cite chains inline, none introduces reasoning absent from section 4, and the Key Insight is a non-obvious finding (current headroom cancels; only f and g matter) rather than a restatement of the recommended measure-then-decide approach.

**Gate result:** cleared · passes: 2 · Fix/Repeat fired: yes

## Structured summary (process output)

```json
{
  "schema_version": 1,
  "run_mode": "full-composer",
  "assumptions": [
    {
      "id": "A-1",
      "type": "physical law",
      "verdict": "Accept"
    },
    {
      "id": "A-2",
      "type": "untested belief",
      "verdict": "Accept"
    },
    {
      "id": "A-3",
      "type": "untested belief",
      "verdict": "Challenge"
    },
    {
      "id": "A-4",
      "type": "untested belief",
      "verdict": "Challenge"
    },
    {
      "id": "A-5",
      "type": "untested belief",
      "verdict": "Discard"
    },
    {
      "id": "A-6",
      "type": "convention",
      "verdict": "Accept"
    },
    {
      "id": "A-7",
      "type": "untested belief",
      "verdict": "Discard"
    },
    {
      "id": "A-8",
      "type": "untested belief",
      "verdict": "Accept"
    },
    {
      "id": "A-9",
      "type": "convention",
      "verdict": "Accept"
    },
    {
      "id": "A-10",
      "type": "convention",
      "verdict": "Accept"
    },
    {
      "id": "A-11",
      "type": "current constraint",
      "verdict": "Accept"
    },
    {
      "id": "A-12",
      "type": "convention",
      "verdict": "Accept"
    },
    {
      "id": "A-13",
      "type": "untested belief",
      "verdict": "Challenge"
    },
    {
      "id": "A-14",
      "type": "physical law",
      "verdict": "Accept"
    }
  ],
  "ground_truths": [
    {
      "id": "GT-1",
      "read_at_source": true
    },
    {
      "id": "GT-2",
      "read_at_source": true
    },
    {
      "id": "GT-3",
      "read_at_source": true
    },
    {
      "id": "GT-4",
      "read_at_source": true
    },
    {
      "id": "GT-5",
      "read_at_source": true
    },
    {
      "id": "GT-6",
      "read_at_source": true
    },
    {
      "id": "GT-7",
      "read_at_source": false
    },
    {
      "id": "GT-8",
      "read_at_source": true
    },
    {
      "id": "GT-9",
      "read_at_source": false
    }
  ],
  "chains": [
    {
      "id": "C1",
      "confidence": "HIGH",
      "rests_on": [
        "GT-1",
        "GT-2",
        "GT-6"
      ]
    },
    {
      "id": "C2",
      "confidence": "HIGH",
      "rests_on": [
        "GT-2",
        "GT-3"
      ]
    },
    {
      "id": "C3",
      "confidence": "HIGH",
      "rests_on": [
        "GT-1",
        "GT-4",
        "GT-8"
      ]
    },
    {
      "id": "C4",
      "confidence": "MEDIUM",
      "rests_on": [
        "GT-1",
        "GT-5"
      ]
    },
    {
      "id": "C5",
      "confidence": "MEDIUM",
      "rests_on": [
        "C1",
        "C2",
        "C3",
        "C4",
        "GT-7?",
        "GT-9?"
      ]
    }
  ],
  "dead_ends": [
    "Request-count hit rate as the load measure",
    "Deferral computed from current headroom",
    "Hits are faster, so p95 must fall",
    "Unconditional verdicts"
  ],
  "techniques": {
    "applied": [
      "inversion",
      "five-whys",
      "estimate",
      "second-order"
    ],
    "not_applied": [
      {
        "technique": "theoretical-limit",
        "phase": 1,
        "reason": "the essence does not hinge on whether a current figure is a convention or a hard bound; the question is a conditional about workload shares"
      },
      {
        "technique": "theoretical-limit",
        "phase": 4,
        "reason": "no conclusion needs a law-permitted ceiling; the deferral formula is an exact identity, not a bound against convention"
      },
      {
        "technique": "fishbone",
        "phase": 2,
        "reason": "the assumption space was enumerable directly (14 rows) and is not multi-causal diagnosis"
      },
      {
        "technique": "trade-off",
        "phase": 4,
        "reason": "the request is to evaluate a claim, not to choose between surviving options; the composite (cache plus a kept-ready upgrade) is carried in the recommendation rather than scored"
      },
      {
        "technique": "pre-mortem",
        "phase": 5,
        "reason": "the conclusion under test is a claim, so inversion is the Phase 5 technique under the decision rule"
      }
    ]
  },
  "gate": {
    "passes": [
      {
        "bands": [
          "Rigorous",
          "Sound",
          "Hand-wavy",
          "Sound",
          "Rigorous",
          "Rigorous"
        ],
        "gate_cleared": true,
        "hand_wavy_cap_cleared": true
      },
      {
        "bands": [
          "Rigorous",
          "Rigorous",
          "Sound",
          "Rigorous",
          "Rigorous",
          "Rigorous"
        ],
        "gate_cleared": true,
        "hand_wavy_cap_cleared": true
      }
    ],
    "fix_repeat_fired": true,
    "cleared": true
  },
  "re_entry": {
    "fired": true,
    "edges": [
      {
        "edge": "the Self-Audit Gate's Fix/Repeat loop",
        "trigger": "Criterion 3 scored Hand-wavy on the first pass (read-at-source GT-5, GT-6 and GT-8 fed only MEDIUM chains), with Criteria 2 and 4 Sound."
      }
    ]
  },
  "conclusion": {
    "recommendation": "Do not schedule the deferral on the claim as stated; first identify the resource that triggers the upgrade, measure s, h_c and g, and defer only if the upgrade is read-bound and f = s × h_c ≥ 1 − (1 + g)^−2 — keeping the upgrade ready rather than cancelled (chain C5, chain C2).",
    "confidence": "MEDIUM"
  }
}
```
