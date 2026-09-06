## Missing inputs — stated before the analysis, per the Input Contract

`AskUserQuestion` is not available in this session, so I cannot ask. Four inputs are absent and each would change the analysis materially:

1. **The database product and its pricing model** (bytes-scanned, compute-seconds/credits, or provisioned node-hours). This determines whether "faster" and "cheaper" are even the same objective.
2. **A bill breakdown** — what share of spend is query execution vs. storage, replication, egress, idle capacity, non-production environments.
3. **The current schema** and whether denormalizing is an available change.
4. **The reporting workload** — which queries, how often, and whether per-query cost attribution exists.

I proceed best-effort. Everything downstream of these is marked accordingly, and the analysis is deliberately structured so its load-bearing conclusions do **not** depend on them.

**Process disclosures:** Step 0 detected no technique-specific trigger, so `MODE = full-composer`. No re-entry edge fired. Phase 3 verification step: no read was attempted because the prompt cites no source to open and names no vendor whose pricing page could be located; GT-6 was read at source (the prompt itself). No Phase 3 failure records.

---

## §6→§4 closure ledger (process output)

```text
- "Stop treating the schema as the variable and start from the bill…" → chain C5 ✓
- "Name the metered unit that actually generates your bill." → chain C5 ✓
- "Attribute spend per query and per table over one full billing period." → chain C5 ✓
- "Confirm reporting query execution is a material share of the bill." → chain C5 ✓
- "Apply reversible levers to the top consumers before anything else." → chain C5 ✓
- "Re-measure, and consider denormalizing only whatever residual survives." → chain C4 ✓
- "In parallel, set a spend cap or per-query scan quota." → chain C5 ✓
- "'Faster' and 'cheaper' are different objectives…" → chain C2 ✓
- "We defer the denormalization win in the regime where it is real…" → chain C4 ✓
- "HIGH on the procedure…" → chain C5 ✓
```

Ledger clean: 10 §6 claims, 10 chain references, 0 cut.

---

## Assumption Audit scan (process output)

| Chain | Step | Step Text (brief) | Assumption surfaced? | Added to Table? |
|---|---|---|---|---|
| C1 | 1 | attribute repeated once per fact row | none | n/a |
| C1 | 2 | column length equals fact row count | A9 fan-out > 1 | yes |
| C1 | 3 | columnar query reads strictly more bytes | A10 engine is column-oriented | yes |
| C1 | 4 | a counterexample regime exists | none | n/a |
| C1 | 5 | premise false as a universal | none | n/a |
| C2 | 1 | schema alters bill only via metered units | none | n/a |
| C2 | 2 | latency-as-metered-unit is a pricing property | none | n/a |
| C2 | 3 | pricing model unnamed, so undecidable | none | n/a |
| C2 | 4 | faster and cheaper are distinct objectives | A15 objective is cost, not latency | yes |
| C3 | 1 | schema is one lever among several | A4 alternative levers available | yes |
| C3 | 2 | no lever has a measured impact | A8 no attribution in place | yes |
| C3 | 3 | choosing now is choosing without the input | none | n/a |
| C3 | 4 | attribution is the first action | none | n/a |
| C4 | 1 | duplication creates a write-path obligation | A12 values are mutable | yes |
| C4 | 2 | obligation lands on ETL, backfill, consumers | none | n/a |
| C4 | 3 | one migration to make, a second to unmake | A5 schema is currently normalized | yes |
| C4 | 4 | highest reversal cost among levers | none | n/a |
| C4 | 5 | schema change belongs last | none | n/a |
| C4 | 6 [2nd] | one writer updates one copy, reports disagree | A13 more than one write path | yes |
| C4 | 7 [2nd] | wide table becomes de-facto interface | none | n/a |
| C4 | 8 [3rd] | reconciliation consumes off-bill analyst time | none | n/a |
| C4 | 9 [3rd] | second reconciliation pipeline adds cost | none | n/a |
| C5 | 1 | must start from the bill, not the schema | none | n/a |
| C5 | 2 | name unit, attribute spend, confirm share | none | n/a |
| C5 | 3 | act on top consumers, re-measure, then schema | none | n/a |
| C5 | 4 | runs on data the team already holds | A14 query history + attribution available | yes |
| C5 | 5 | the answer is the procedure, not denormalizing | none | n/a |
| C5 | 6 [2nd] | procedure has lead time, bill keeps accruing | none | n/a |
| C5 | 7 [2nd] | a cap bounds accrual without committing | A16 product exposes a cap or quota | yes |
| C5 | 8 [3rd] | a binding cap surfaces the top consumers | none | n/a |
| C6 | 1 | skew favours targeting the top queries | none | n/a |
| C6 | 2 | provisioned capacity: right-size, don't optimize | A11 capacity not saturated | yes |
| C6 | 3 | bytes-scanned: reduce bytes read | none | n/a |
| C6 | 4 | partition, cluster, pre-aggregate; all deletable | none | n/a |
| C6 | 5 | ordering decidable once model named | none | n/a |

35 rows, one per chain per step, in order. Nine assumptions surfaced (A4, A5, A8, A9, A10, A11, A12, A13, A14, A15, A16 — eleven marks across ten distinct rows, A11 and A16 newly created by this audit); all recorded in §2.

---

## Self-audit scan (process output)

| Chain | Chain Head (brief) | Form conforming? | Rule applied | Dependency clean? |
|---|---|---|---|---|
| C1 | `GT-2 (…) + GT-3 (…) + GT-4 (…)` | yes | n/a | yes |
| C2 | `GT-1 (…) + GT-6 (…)` | yes | n/a | yes |
| C3 | `GT-5 (…) + GT-6 (…)` | yes | n/a | yes |
| C4 | `GT-3 (…)` | yes | n/a | yes |
| C5 | `C1 (…) + C2 (…) + C3 (…) + C4 (…)` | yes | n/a | yes |
| C6 | `GT-7? (…) + GT-8? (…) + GT-9? (…) + C3 (…)` | yes | n/a | yes |

| §6 Span (brief) | Construct | Claim under R11? | R11 clause applied | Chain cited |
|---|---|---|---|---|
| "The bill is the variable, not the schema." | prose | no | prose carrying neither a bold colon lead-in nor a list marker | n/a |
| "**Recommended approach:** Stop treating the schema…" | bold lead-in | yes | colon closes the bold span, assertion follows on same line | C5 |
| "1. Name the metered unit…" | list item | yes | list item closing its own sentence | C5 |
| "2. Attribute spend per query and per table…" | list item | yes | list item closing its own sentence | C5 |
| "3. Confirm reporting query execution…" | list item | yes | list item closing its own sentence | C5 |
| "4. Apply reversible levers to the top consumers…" | list item | yes | list item closing its own sentence | C5 |
| "5. Re-measure, and consider denormalizing…" | list item | yes | list item closing its own sentence | C4 |
| "6. In parallel, set a spend cap…" | list item | yes | list item closing its own sentence | C5 |
| "**Key insight:** 'Faster' and 'cheaper'…" | bold lead-in | yes | colon closes the bold span, assertion follows on same line | C2 |
| "**Trade-offs acknowledged:** We defer…" | bold lead-in | yes | colon closes the bold span, assertion follows on same line | C4 |
| "**Confidence:** HIGH on the procedure…" | bold lead-in | yes | colon closes the bold span, assertion follows on same line | C5 |

Scan complete: 6 chain rows, one per section-4 chain block in order; 11 section-6 rows, one per construct in order — 10 claims under R11, 1 excluded. 0 chains malformed, 0 claims untraced.

---

# First-Principles Analysis: Reporting Query Cost

## 1. Problem Essence

**Core problem:** Which change to the reporting data path removes the most cost per unit of engineering effort and irreversibility — where "cost" means the metered resource that actually generates the bill, not query latency.

**Success criteria** (each checkable by scanning §6):

- The Conclusion names the metered unit that generates the bill, or names it as unknown and states how to obtain it.
- The Conclusion states whether the supplied premise survived challenge, and if not, names the chain that falsified it.
- The Conclusion either ranks at least two levers against each other or names the specific missing measurement that makes ranking undecidable.
- The Conclusion's recommended first action is executable with data the team already holds, and names that data.
- No claim in the Conclusion rests on the supplied premise.

**What the essence is not.** "Should we denormalize?" is a candidate *answer* smuggled in as the *question*. The triggering event is a bill; the question asked is about schema shape; those are not the same thing, and Phase 2 is where the substitution gets caught.

---

## 2. Assumptions Table

The assumption space here is multi-causal — a database bill has many independent drivers — so I enumerated candidate cost drivers by category before classifying (default six-category set), which is what produced rows A3, A4 and A8:

- **Technology and Tools** — storage layout, missing partitioning/clustering, no result cache, engine mismatch to workload
- **Process** — duplicated or over-scheduled report runs, auto-refreshing dashboards, no retention policy, non-production environments left running
- **Information** — no per-query attribution, no bill breakdown, no retained query history
- **Resources** — over-provisioned capacity, wrong instance class, on-demand vs. reserved mix
- **People** — unbounded `SELECT *` from BI tools, no cost ownership per team
- **Environment** — cross-region egress, replication, multi-AZ, snapshot and backup retention

Schema shape is one twig on the Technology branch. That is the first signal that the prompt's framing is narrower than the problem.

| Assumption | Type | Treatment | Verdict | Verification |
|---|---|---|---|---|
| A1: Normalized schemas are slower than denormalized ones (the supplied premise) | convention | explicitly challenge before use | **Discard** — falsified as a universal by the columnar counterexample; not load-bearing anywhere in this analysis | challenged in C1 against GT-2, GT-3, GT-4 |
| A2: Slower means more expensive | untested belief | verify, or flag as unverified | **Discard** — the slow→expensive mapping is a property of the pricing model, not of the schema | challenged in C2 against GT-1 |
| A3: Reporting query execution is a material share of the database bill | untested belief | verify, or flag as unverified | **Challenge** — storage, replication, egress, idle provisioned capacity and non-production environments are untested alternatives that commonly dominate | unverified — flagged; no bill breakdown supplied |
| A4: Alternative levers (pre-aggregation, partitioning, caching, scheduling, retention, workload isolation) are available on this product | untested belief | verify, or flag as unverified | **Challenge** — the product is unnamed, so availability is unconfirmed | unverified — flagged; declared inline at C3 step 1 |
| A5: The current schema is normalized enough that denormalizing is an available change | untested belief | verify, or flag as unverified | **Challenge** — no schema was supplied; the premise presumes its own applicability | unverified — flagged; declared inline at C4 step 3 |
| A6: Reporting cost is concentrated in a small number of queries | untested belief | verify, or flag as unverified | **Challenge** — a general skew observation, not measured on this workload; elevated for use as GT-7? | unverified — flagged (GT-7?) |
| A7: A schema change is cheap and reversible | untested belief | verify, or flag as unverified | **Discard** — contradicted by the write-path, backfill and consumer-coupling obligations derived in C4 | challenged in C4 against GT-3 |
| A8: Per-query cost attribution is currently in place | untested belief | verify, or flag as unverified | **Challenge** — nothing in the prompt indicates it, and C3's recommendation exists precisely because it probably is not | unverified — flagged; declared inline at C3 step 2 |
| A9: Dimension fan-out exceeds 1 (fact rows outnumber dimension rows) | untested belief | verify, or flag as unverified | **Accept** — entailed by GT-3 in any model where denormalization is even proposed; at fan-out 1 there is nothing to duplicate | entailed by GT-3; surfaced by the Phase 4 audit at C1 step 2 |
| A10: The storage engine is column-oriented | current constraint | record the expiry conditions | **Challenge** — unknown; the constraint expires the instant the product is named. C1 needs only that *some* such regime exists, which GT-4 supplies definitionally, so C1 does not depend on this being true here | unverified — flagged; declared inline at C1 step 3 |
| A11: Provisioned capacity, if used, is not already saturated | current constraint | record the expiry conditions | **Accept** — expires at the saturation point, beyond which marginal query cost becomes positive; until then GT-8?'s zero-marginal-cost claim holds | unverified — flagged (GT-8?); declared inline at C6 step 2 |
| A12: The duplicated values are mutable, not append-only immutable facts | untested belief | verify, or flag as unverified | **Challenge** — append-only event data weakens C4's write-path arm, though not its backfill or consumer-coupling arms | unverified — flagged; declared inline at C4 step 1 |
| A13: More than one write path reaches these tables | untested belief | verify, or flag as unverified | **Challenge** — a strict single-writer system does not produce the copy drift described in C4's second-order extension | unverified — flagged; declared inline at C4 step 6 |
| A14: Query history is retained and per-query cost or bytes-scanned attribution is obtainable | untested belief | verify, or flag as unverified | **Challenge** — C5's entire procedure is unexecutable if this is false, which makes it the most consequential unknown in the analysis | unverified — flagged; declared inline at C5 step 4 |
| A15: The team's objective is to reduce the bill, not to reduce report latency | untested belief | verify, or flag as unverified | **Challenge** — the prompt says "database costs" but asks about "queries"; C2 shows these two objectives can diverge completely | unverified — flagged; declared inline at C2 step 4 |
| A16: The product exposes a spend cap or per-query scan quota | untested belief | verify, or flag as unverified | **Challenge** — available on some products and not others; only the parallel mitigation depends on it, not the main procedure | unverified — flagged; declared inline at C5 step 7 |

**Note on the type distribution.** No row classifies as **physical law**. That is itself a finding: the premise was delivered in the register of a law ("everyone knows") while classifying as a convention — a heuristic that was true in a specific regime and has been generalized past it.

---

## 3. Ground Truths

**Verified — definitional terminus** (the irreducibility drill bottoms out at a definition, so no external figure is asserted and no citation is owed; the read-at-source cell names the definitional reduction):

- **GT-1** A metered bill equals the sum, over each metered dimension, of units consumed × unit price for that dimension. — source: the definition of consumption-metered pricing; read-at-source: definitional — true by the meaning of "metered pricing"; no external figure is asserted
- **GT-2** A universally quantified claim is falsified by a single counterexample. — source: the definition of universal quantification in first-order logic; read-at-source: definitional
- **GT-3** Denormalization stores one logical value in more than one physical location. — source: the definition of denormalization; read-at-source: definitional — this *is* what the word denotes
- **GT-4** A column-oriented engine reads only the columns a query references; a row-oriented engine reads whole rows, including columns the query does not reference. — source: the defining property of the two storage layouts; read-at-source: definitional
- **GT-5** Ranking a set of options by a quantity requires a value of that quantity for each option. — source: the definition of a ranking over a set; read-at-source: definitional

**Verified — read at source:**

- **GT-6** The prompt names no database product, no pricing model, no schema, no query workload, and no bill breakdown. — source: the user's prompt; read-at-source: the prompt in full — *"Reason from ground truth about our database costs. Everyone knows normalized schemas are slower than denormalized ones. What should we do about our reporting queries?"* — checked term by term against each of the five categories

**Unverified (D-07):**

- **GT-7?** Cost distributions over a repeated reporting workload are heavily right-skewed: a small minority of distinct queries account for the majority of spend. — unverified: a general observation about workload shape; no source was opened in this analysis and no measurement of this workload exists
- **GT-8?** Under provisioned or reserved capacity pricing, the marginal price of an additional query-second is approximately zero until the cluster saturates. — unverified: a property of flat-rate capacity pricing; no vendor pricing page was opened, and this team's pricing model is unknown per GT-6
- **GT-9?** Adding a materialized aggregate, a partition key, or a result cache is reversible by deletion; changing a table's schema shape is not reversible without a second migration and a backfill. — unverified: a general property of these operations, not confirmed against this team's tooling

**Provenance summary:**

```text
?-marked: GT-7, GT-8, GT-9 (3 of 9)
Read-at-source: GT-6 — the user's prompt, quoted verbatim above and checked term by term
Read-at-source: GT-1..GT-5 — definitional terminus, no external figure asserted (see Criterion 3)
```

---

## 4. Derivation Chains

### Conclusion C1: The supplied premise is false as a universal and cannot serve as a ground truth

```text
GT-2 (a universal claim falls to one counterexample) + GT-3 (denormalization duplicates a logical value) + GT-4 (a columnar engine reads only referenced columns)
→ in a denormalized wide table each dimension attribute is repeated once per fact row
→ that repetition makes the attribute column's physical length equal to the fact row count rather than the dimension row count *[Assumes: A9 — dimension fan-out exceeds 1]*
→ a columnar query filtering on that attribute therefore reads strictly more bytes than the same filter reads from the small normalized dimension table *[Assumes: A10 — the engine is column-oriented]*
→ a regime exists in which the normalized shape scans strictly fewer bytes than the denormalized one
→ the supplied premise is false as a universal and cannot be carried into this analysis as a ground truth
```

**Confidence:** HIGH — all three head inputs are unsuffixed and definitional; the conclusion is a falsification, which needs only that one counterexample regime exist, not that this team occupies it.

**Weakest link:** step 3's dependence on A10. If the engine is a row store, this particular counterexample does not describe *your* system. It does not need to: GT-4 supplies the regime's existence definitionally, and GT-2 needs only existence to falsify a universal.

### Conclusion C2: "Faster" and "cheaper" are distinct objectives, and the premise speaks only to the first

```text
GT-1 (a metered bill is units consumed × unit price, summed over metered dimensions) + GT-6 (the prompt names no product, pricing model, schema, workload or bill breakdown)
→ a schema change alters the bill only through the metered units that change moves
→ whether query latency is among the metered units is a property of the pricing model, not a property of the schema
→ the pricing model is unnamed here, so it is not currently decidable whether making these queries faster makes them cheaper at all
→ "faster" and "cheaper" are distinct objectives, and the premise as supplied speaks only to the first *[Assumes: A15 — the objective is the bill, not report latency]*
```

**Confidence:** HIGH — both head inputs are unsuffixed; the conclusion is that a question is undecided, which is exactly what GT-6 establishes.

**Weakest link:** step 4's dependence on A15. If the team's real objective is report latency rather than spend, C2's conclusion remains true but stops being decision-relevant, and the question should be re-framed before anything else happens.

### Conclusion C3: Per-query cost attribution is the first action, and it precedes any schema decision

```text
GT-5 (ranking options by a quantity requires a value per option) + GT-6 (the prompt names no product, pricing model, schema, workload or bill breakdown)
→ schema shape is one candidate lever among several — pre-aggregation, partitioning and clustering, result caching, run deduplication, retention trimming, and workload isolation *[Assumes: A4 — the alternative levers are available on this product]*
→ none of these levers has a measured cost impact on this workload, because no cost has been attributed to any query or table *[Assumes: A8 — no attribution is currently in place]*
→ choosing among them now is choosing without the one input that decides the ranking
→ per-query and per-table cost attribution is therefore the first action, and it precedes any schema decision
```

**Confidence:** HIGH — both head inputs are unsuffixed; the conclusion follows from GT-5 by construction once GT-6 establishes the values are missing.

**Weakest link:** step 3's dependence on A8. If attribution already exists, C3's conclusion collapses to "read the report you already have" — still the correct first action, but not new work.

### Conclusion C4: Schema change carries the highest reversal cost and belongs last among comparable levers

```text
GT-3 (denormalization stores one logical value in more than one physical location)
→ every duplicated value creates a standing obligation on the write path to keep its copies consistent *[Assumes: A12 — the values are mutable, not append-only]*
→ that obligation lands on ingest and ETL code, on a backfill of all existing history, and on every downstream consumer coupled to the old shape
→ the change therefore costs one migration to make and a second migration to unmake *[Assumes: A5 — the schema is currently normalized enough for this to be an available change]*
→ among levers of comparable expected saving, schema change carries the highest reversal cost
→ schema change therefore belongs last in the ordering, not first
→[2nd] once copies exist, a writer that updates one and not another produces reports that disagree with the source system *[Assumes: A13 — more than one write path reaches these tables]*
→[2nd] the wide table becomes the de-facto reporting interface, so new consumers couple to the duplication and the change grows harder to unwind over time
→[3rd] reconciling reports that disagree consumes analyst time that never appears on the database bill, so any measured saving overstates the realized saving
→[3rd] the usual organizational response to distrusted reports is a second reconciliation pipeline, which adds cost in the direction opposite to the one intended
```

**Confidence:** HIGH — the single head input is unsuffixed and definitional; the second- and third-order extensions contradict no ground truth, so no return to Phase 2 is triggered.

**Weakest link:** step 1's dependence on A12. On append-only immutable fact tables the write-path consistency arm weakens substantially — but steps 2 and 3 (backfill, consumer coupling) survive A12 being false, so the conclusion holds on the remaining arms.

### Conclusion C5: The answer is to execute an ordered measurement-first procedure, not to denormalize

```text
C1 (premise false as a universal) + C2 (faster and cheaper are distinct objectives) + C3 (attribution precedes lever choice) + C4 (schema change is least reversible)
→ the premise supplies neither a fact to build on nor a criterion to decide by, so the analysis must start from the bill rather than from the schema
→ an ordered procedure follows — name the metered unit, attribute spend per query and per table, then confirm reporting is a material share of the bill
→ only then act on the top consumers with reversible levers, re-measure, and consider schema shape for whatever residual remains
→ every step of that procedure runs on data the team already holds, a billing console and a query history, and commits nothing irreversible *[Assumes: A14 — query history is retained and per-query attribution is obtainable]*
→ the answer to "what should we do about our reporting queries" is to execute that procedure, not to denormalize
→[2nd] the procedure has a lead time before it yields a ranking, during which the bill keeps accruing
→[2nd] a spend cap or per-query scan quota bounds that accrual without committing to any lever *[Assumes: A16 — the product exposes a cap or quota]*
→[3rd] a cap that binds will fail some reports, which surfaces exactly the top-consuming queries the attribution step is looking for
```

**Confidence:** HIGH — all four head inputs are HIGH-confidence chains and no `GT-N?` input is consumed anywhere in this chain. The second- and third-order extensions contradict no ground truth.

**Weakest link:** step 4's dependence on A14. This is the single most consequential unverified assumption in the analysis: if the product exposes no query history and no per-query cost or bytes-scanned attribution, the procedure is unexecutable as written and the substitute is coarser — tag-level or table-level attribution, or a controlled A/B over a billing period.

### Conclusion C6: The lever ordering becomes decidable the moment the pricing model is named

```text
GT-7? (reporting cost distributions are right-skewed) + GT-8? (marginal query cost is near zero on unsaturated provisioned capacity) + GT-9? (aggregates, partitions and caches are reversible by deletion; schema shape is not) + C3 (attribution precedes lever choice)
→ under skew, a lever applied to the few top-spending queries can outperform a change applied to the whole schema
→ under provisioned capacity the highest-yield lever is not query optimization at all, but right-sizing or rescheduling the capacity itself *[Assumes: A11 — the capacity is not already saturated]*
→ under bytes-scanned pricing the highest-yield levers are instead the ones that reduce bytes read
→ that means partitioning and clustering on the columns the top queries actually filter on, and materialized pre-aggregates for repeated rollups, all of which are removable by deletion if they do not pay off
→ the lever ordering is therefore decidable as soon as the pricing model is named and the top consumers are attributed, and not before
```

**Confidence:** MEDIUM — three of the four head inputs are `?`-marked. GT-7? (skew) is unmeasured on this workload, GT-8? (zero marginal cost on provisioned capacity) rests on an unnamed pricing model, and GT-9? (reversibility) is unconfirmed against this team's tooling. Naming the product and pricing model, plus one billing period of per-query attribution, raises this chain to HIGH. Nothing in §6 rests on this chain alone.

**Weakest link:** the head itself. Three of four inputs are unverified, which is why this chain informs the confidence caveat rather than the recommendation.

---

## 5. Abandoned Reasoning

### Dead End: Rebut the premise by arguing that joins are never expensive

**What was tried:** Countering "normalized is slower" with its symmetric opposite — that join cost is always negligible on a modern engine because hash joins are roughly linear in the sum of their input sizes.

**Why abandoned:** It commits exactly the error the premise commits, in the opposite direction. It is a universal claim with known counterexamples: a nested-loop join without a supporting index is quadratic in its inputs; a hash join whose build side spills to disk degrades sharply; a multi-join chain with a mis-estimated cardinality can produce an intermediate result larger than either input. Adopting it would have violated GT-2 in precisely the way A1 does.

**What it ruled out:** It rules out the over-correction, and it concedes what the premise gets right. Join elimination is a genuine effect in a genuine regime — row-store, many-table joins, poor cardinality estimates, no covering index. The error in the premise is not that this regime is imaginary; it is that the premise asserts it universally. The correct move is not to deny the regime but to determine which regime this team is actually in, which is C3's conclusion.

### Dead End: Estimate the saving from denormalization directly

**What was tried:** A Fermi estimate of the bill reduction — bytes scanned per query × queries per period × price per byte, computed before and after denormalization, bracketed with conservative and aggressive values.

**Why abandoned:** The estimate procedure requires a first-principles value for each unit-factor. Every factor here is unknown per GT-6: price per metered unit, bytes per query, query count, and dimension fan-out. The resulting bracket runs from "denormalization removes most of the bill" to "denormalization increases the bill," which straddles the decision threshold and drives opposite actions at its two ends. The stop criterion is not met and the estimate carries no information.

**What it ruled out:** It rules out any quantified recommendation in this response, and it is direct evidence for C3 — the four missing factors are exactly the four measurements C5's procedure acquires.

### Dead End: Recommend materialized views as the default answer

**What was tried:** Skipping the measurement step entirely and recommending pre-aggregation, the lever with the strongest general reputation for reporting workloads.

**Why abandoned:** This is reasoning by analogy used as direct evidence. "Materialized views usually help reporting workloads" is an appeal to what has worked elsewhere with no named ground truth about *this* situation, which the methodology forbids as standalone justification. It also fails against GT-8?: on unsaturated provisioned capacity, a query that runs faster because it reads a pre-aggregate saves latency and saves nothing on the bill, while the aggregate itself adds storage cost.

**What it ruled out:** It rules out treating any lever as a default — including denormalization, the one being asked about. The symmetry is the point: the reason not to denormalize by default is the same reason not to materialize by default.

---

## 6. Conclusion

The bill is the variable, not the schema.

**Recommended approach:** Stop treating the schema as the variable and start from the bill — name the metered unit, attribute spend, then act on the top consumers with reversible levers before touching schema shape (chain C5).

1. Name the metered unit that actually generates your bill — bytes scanned, compute-seconds or credits, or provisioned node-hours (chain C5).
2. Attribute spend per query and per table over one full billing period (chain C5).
3. Confirm reporting query execution is a material share of the bill, rather than storage, egress, idle capacity or non-production environments (chain C5).
4. Apply reversible levers to the top consumers before anything else (chain C5).
5. Re-measure, and consider denormalizing only whatever residual survives steps 1 through 4 (chain C4).
6. In parallel, set a spend cap or per-query scan quota so the bill stops growing while the measurement runs (chain C5).

**Key insight:** "Faster" and "cheaper" are different objectives that coincide only under specific pricing models, so the premise you supplied is not merely false as a universal — it is answering a different question than the one you asked, because it is a claim about latency offered in response to a question about cost (chain C2).

**Trade-offs acknowledged:** We defer the denormalization win in the regime where it is genuinely real — row-store, many-table joins, poor cardinality estimates — accepting that if you are in that regime the measurement step costs you a billing period before you act on it; the trade is one period of delay against a migration and a backfill you cannot cheaply unmake (chain C4).

**Confidence:** HIGH on the procedure — chains C1 through C5 rest entirely on unsuffixed ground truths and consume no `GT-N?` input; the *choice* of which lever to apply at step 4 is MEDIUM, resting on chain C6, which consumes GT-7? (workload skew unmeasured), GT-8? (marginal cost on provisioned capacity, pricing model unnamed) and GT-9? (reversibility unconfirmed against your tooling), and naming your product and pricing model plus one billing period of per-query attribution raises that to HIGH (chain C5).

---

## Self-Audit Gate — verdict blocks (process output)

Assumption Audit scan confirmed present, 35 rows, one per chain per step in order, no step skipped. Self-audit scan confirmed present, both tables, reconciliation line recounts against §4 and §6.

**Criterion 1: Identify Essence**
Quoted span: *"Which change to the reporting data path removes the most cost per unit of engineering effort and irreversibility — where 'cost' means the metered resource that actually generates the bill, not query latency."*
Band: **Rigorous**
Justification: a single sentence naming the underlying decision rather than the triggering event or the prompt's restatement, and each of the five success criteria is a verb-subject-outcome test whose outcome is a scannable property of the Conclusion section.

**Criterion 2: Challenge Assumptions**
Quoted span (Assumption Audit scan): *"| C4 | 1 | duplication creates a write-path obligation | A12 values are mutable | yes |"*
Band: **Rigorous**
Justification: every Type is drawn from the four-type scheme, every Verdict leads with Accept/Challenge/Discard followed by an em-dash justification, three assumptions carry a Discard verdict so challenge was genuinely attempted, every chain-used unverified assumption reads "unverified — flagged", and the audit table covers all 35 chain steps in order.

**Criterion 3: Establish Ground Truths**
Quoted span: enumerated GT-7, GT-8, GT-9; the Ground Truths list carries `?` on exactly those three of nine, and the six unsuffixed entries are GT-1 through GT-6.
Band: **Sound**
Justification: IDs are stable and match §4's references, the enumeration agrees with the list, and no Discard-verdict assumption appears — but five unsuffixed ground truths (GT-1 through GT-5) name a definitional reduction rather than a document page or passage as their read-at-source location, which is a legitimate irreducibility terminus under the methodology and simultaneously falls short of the Rigorous descriptor's document-citation wording; this is disclosed rather than resolved by downgrading the chains, since acquiring a citation for the definition of "denormalization" would not make the claim more verified than it already is.

**Criterion 4: Reason Upward**
Quoted span (self-audit scan, chain-form table): *"| C5 | `C1 (…) + C2 (…) + C3 (…) + C4 (…)` | yes | n/a | yes |"*
Band: **Rigorous**
Justification: all six chain blocks score form-conforming with clean dependencies, every conclusion has exactly one chain with at least one genuine intermediate, three dead ends in §5 use the What-was-tried / Why-abandoned / What-it-ruled-out structure with specific structural reasons, one of which explicitly rejects a path *for* being an analogy used as direct evidence, and eleven chain steps carry inline `[Assumes: X]` declarations.

**Criterion 5: Validate**
Quoted span: *"Weakest link: step 4's dependence on A14. This is the single most consequential unverified assumption in the analysis: if the product exposes no query history and no per-query cost or bytes-scanned attribution, the procedure is unexecutable as written."*
Band: **Rigorous**
Justification: every one of the six chains names its weakest link specifically rather than generically; the only chain consuming `GT-N?` inputs (C6) is rated MEDIUM with all three unverified inputs named and the verification that would raise it stated; no HIGH chain consumes a `?` input; every §6 claim rests on at least one HIGH chain (C1–C5), so the overall HIGH rating matches the weakest contributing chain. No EXCEPT clause is claimed.

**Criterion 6: Conclusion-to-Ground-Truth Traceability**
Quoted span (self-audit scan, claim-inventory table): *"| '**Key insight:** \"Faster\" and \"cheaper\"…' | bold lead-in | yes | colon closes the bold span, assertion follows on same line | C2 |"*
Band: **Rigorous**
Justification: all ten §6 claims trace to a named §4 chain with zero untraced, no claim introduces reasoning absent from §4, and the Key Insight names a finding distinct from the recommended approach — that the premise answers a latency question rather than the cost question asked — which neither convention nor analogy reaches.

**Gate result:** No criterion Absent; one criterion (3) at Sound, none at Hand-wavy. **Gate cleared.** No Fix/Repeat pass was needed, so no re-entry edge fired.