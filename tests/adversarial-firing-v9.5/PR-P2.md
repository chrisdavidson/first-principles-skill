Reads complete. Emitting process output first (as the methodology prescribes), then the analysis, then the gate.

---

**A note before the analysis:** the sentence "everyone knows normalized schemas are slower than denormalized ones" is the first thing this analysis tests, not something it builds on. It does not survive Phase 2.

---

## Assumption Audit (process output)

One row per chain per step, in order.

| Chain | Step | Step Text (brief) | Assumption surfaced? | Added to Table? |
|---|---|---|---|---|
| C1 | 1 | normal form defined by dependency/anomaly properties | none | n/a |
| C1 | 2 | Codd's 4th objective is neutrality to query statistics | A17 — secondary source faithfully renders Codd | yes |
| C1 | 3 | premise is a workload claim in schema grammar | none | n/a |
| C1 | 4 | premise cannot anchor a decision until measured | none | n/a |
| C2 | 1 | every term in the cost identity is a measured quantity | none | n/a |
| C2 | 2 | not one term has a value for this system | none | n/a |
| C2 | 3 | ranking needs the targeted term and its share | none | n/a |
| C2 | 4 | no intervention rankable on expected saving | none | n/a |
| C2 | 5 | only measurement's value is assumption-free | none | n/a |
| C3 | 1 | columnar layout reads only the wanted chunks | none | n/a |
| C3 | 2 | row layout reads whole rows to reach few columns | none | n/a |
| C3 | 3 | bytes read set by layout, not by fact placement | none | n/a |
| C3 | 4 | layout and normal form are independent axes | none | n/a |
| C3 | 5 | bytes-scanned lever belongs to layout | none | n/a |
| C4 | 1 | MV and denormalized column both store a fact twice | none | n/a |
| C4 | 2 | MV's copy has a named reconciliation mechanism | none | n/a |
| C4 | 3 | denormalized copy reconciled by ad-hoc app code | A11 — the team controls the reading application code | yes |
| C4 | 4 | MV divergence bounded and locatable; schema copy neither | none | n/a |
| C4 | 5 | defensible denormalization = named reconciliation step | none | n/a |
| C5 | 1 | K recomputations do the same work K times | none | n/a |
| C5 | 2 | precomputing collapses K executions into one | A22 — bounded staleness acceptable to report consumers | yes |
| C5 | 3 | saving scales with K, not with schema shape | none | n/a |
| C5 | 4 | where K ≫ 1, precomputation outranks reshaping | none | n/a |
| C6 | 1 | denormalization removes joins but widens rows | none | n/a |
| C6 | 2 | denormalization writes each changed fact per copy | A8 — these tables are read-dominated | yes |
| C6 | 3 | net effect = join saving minus scan-and-write penalty | none | n/a |
| C6 | 4 | neither term measured for this system | none | n/a |
| C6 | 5 | sign unknown; denormalizing is an unpriced bet | none | n/a |
| C7 | 1 | weights locked before scoring, reversibility top-weighted | A20 — weights reflect this org's real risk posture | yes |
| C7 | 2 | weighted totals E=134 > B=116 > C=96 > D=89 > A=51 | A18 — reports are column-selective | yes |
| C7 | 3 | the proposed option ranks last | none | n/a |
| C7 | 4 | pre-mortem moved replica to a placement decision | A9 — reporting currently shares the transactional instance | yes |
| C7 | 5 | trigger set on a measured threshold, not a price | none | n/a |
| C7 | 6 | recommended plan: decompose, tune, precompute, trigger | none | n/a |
| C7 | 7 [2nd] | tuning with capture produces the missing attribution | A21 — tuning will actually be instrumented | yes |
| C7 | 8 [2nd] | reporting indexes add write amplification | A19 — index maintenance is transactional in this engine | yes |
| C7 | 9 [2nd] | cheap reports run more often, raising K | none | n/a |
| C7 | 10 [3rd] | columnar decision becomes evidence-decidable | none | n/a |
| C7 | 11 [3rd] | unused MVs accumulate refresh cost | A12 — data volume is growing | yes |

Audit complete: 39 steps visited, 10 assumptions surfaced, all 10 added to the Assumptions Table.

---

## Adversarial pass (process output)

The conclusion is a plan, so the pre-mortem procedure applies (inversion stress-tests a claim; pre-mortem stress-tests a plan).

**Premise.** It is six months from now. The plan — decompose the cost, tune, then materialize — has failed badly: reporting costs are higher than when we started, and the team has lost credibility on the topic.

**Causes** (unfiltered, written before grouping, from four named viewpoints).

*The engineer doing the work:*
1. Tuning was done without a baseline, so no saving could be shown and the quarter looked empty.
2. Reporting indexes regressed write latency on the transactional path; an incident followed and every one was reverted.
3. Tuning hit its ceiling in week three and the plan had no next step queued.
4. The instrumentation that was supposed to be a by-product was never built because it was not on a ticket.
14. Index bloat lengthened the primary's maintenance window until it overran the nightly slot.

*The analyst who lives with the reports:*
5. A materialized view went stale, a board number was wrong, and trust in reporting collapsed.
6. The refresh window collided with the reporting window, blocking the very reports the view was meant to speed up.
7. Nobody told the analysts which reports were now served from a view, so they chased phantom discrepancies for weeks.
8. The retention policy deleted history a quarterly report needed.

*The person who pays the bill:*
9. The bill did not move, because the cost was storage and idle provisioned compute, not query compute — the plan optimized the wrong term.
10. Engineering time spent on tuning exceeded the money saved.
11. Savings were real but were immediately consumed by new reports scheduled because reports had become cheap.

*A rival team that benefits:*
12. They shipped the columnar warehouse we deferred and now own analytics.
13. "We measured first" was read by leadership as "they did nothing for a quarter."

**Adversarial interrogation.** Cause 9 is the one that embarrasses the recommendation: it contradicts the plan's own premise that query cost is where the money is, and GT-10? concedes we never established which cost is meant. Causes 12–13 embarrass the sequencing. Cause 11 was independently surfaced by the second-order pass, which is evidence the pass was real rather than decorative.

**Clusters and dispositions.**

| Cluster | Causes | Bears on | Disposition |
|---|---|---|---|
| 1 — The plan optimizes a term nobody confirmed is dominant | 9, 10, 11 | GT-10?, GT-6, C7 | **Plan change:** a bill/latency decomposition naming the dominant movable term becomes deliverable #1, ahead of tuning. If query compute is not the largest movable term, the plan stops and re-enters Phase 2. |
| 2 — No escalation trigger past tuning's ceiling | 3, 12, 13 | C3, C7 | **Plan change:** the threshold and date that trigger the columnar migration are agreed now, in writing, before tuning starts — not re-debated later. |
| 3 — Precomputation's correctness and communication surface is unstaffed | 5, 6, 7, 8 | GT-2, C4, C5 | **Plan change:** no materialized view ships without all three of a refresh schedule, a published staleness bound, and an on-report freshness indicator. Retention changes require a named sign-off from report owners. |
| 4 — Reporting optimization charged to the transactional path | 2, 14 | GT-7, C7 | **Plan change:** reporting-serving indexes and materialized views go on a read replica, not the primary. This promotes the replica from ranked alternative (score 96) to a structural placement decision. |
| 5 — The by-product measurement is never produced | 1, 4 | GT-6, C2 | **Accepted risk, with named mitigation:** instrumentation may not fall out of tuning. Mitigation — Cluster 1's decomposition is a separately-ticketed, separately-owned deliverable ordered *before* tuning, so the measurement does not depend on tuning happening. |

All five dispositions are folded into chain C7 below; the pass materially changed the plan.

---

## §6→§4 closure ledger (process output)

- "Do not denormalize; name the dominant cost term first, then reduce it with reversible measures placed off the transactional path" → chains C1, C7 ✓
- "Produce a one-page decomposition of the database bill … and name the term this work targets" → chain C2 ✓
- "Tune the reporting queries, indexes, partitioning and retention against that term on a read replica … capturing a before-and-after figure per report" → chains C2, C7 ✓
- "Add materialized views for the reports whose execution count between input changes is materially greater than one …" → chains C4, C5 ✓
- "Fix the escalation trigger now …" → chains C3, C7 ✓
- "A materialized view and a denormalized column are the same redundancy …" → chain C4 ✓
- "Tuning buys time rather than headroom … materialized views trade per-execution freshness for cost …" → chains C3, C5, C7 ✓
- "MEDIUM — contributing chains rated below HIGH are C5, C6 and C7 …" → chains C1, C2, C3, C4, C5, C6, C7 ✓

Ledger clean: 8 claims, 8 traced, 0 cut.

---

## Self-audit scan (process output)

| Chain | Chain Head (brief) | Form conforming? | Rule applied | Dependency clean? |
|---|---|---|---|---|
| C1 | GT-1 + GT-7 | yes | n/a | yes |
| C2 | GT-6 + GT-4 + GT-5 | yes | n/a | yes |
| C3 | GT-3 + GT-5 | yes | n/a | yes |
| C4 | GT-2 + GT-7 | yes | n/a | yes |
| C5 | GT-4 + C4 + GT-9? | yes | n/a | yes |
| C6 | GT-5 + GT-7 + GT-8? + GT-11? | yes | n/a | yes |
| C7 | GT-10? + GT-12? + C1 + C2 + C3 + C6 | yes | n/a | yes |

| §6 Span (brief) | Construct | Claim under R11? | R11 clause applied | Chain cited |
|---|---|---|---|---|
| "Recommended approach:" | bold lead-in | yes | prescribed lead-in, colon closes bold span, text follows | C1, C7 |
| "Execute in this order:" | prose | no | carries neither a bold colon lead-in nor a list marker | n/a |
| item 1 — cost decomposition | list item | yes | list item past forty characters, closes its sentence | C2 |
| item 2 — tune on a replica | list item | yes | list item past forty characters, closes its sentence | C2, C7 |
| item 3 — materialized views | list item | yes | list item past forty characters, closes its sentence | C4, C5 |
| item 4 — escalation trigger | list item | yes | list item past forty characters, closes its sentence | C3, C7 |
| "Key insight:" | bold lead-in | yes | prescribed lead-in, colon closes bold span, text follows | C4 |
| "Trade-offs acknowledged:" | bold lead-in | yes | prescribed lead-in, colon closes bold span, text follows | C3, C5, C7 |
| "Confidence:" | bold lead-in | yes | colon closes bold span, text follows | C1–C7 |

Scan complete: 7 chain rows, one per section-4 chain block in order; 9 section-6 rows, one per construct in order — 8 claims under R11, 1 excluded. 0 chains malformed, 0 claims untraced.

---
---

# First-Principles Analysis: Reporting Query Costs

## 1. Problem Essence

**Core problem:** Which term of our reporting workload's cost is actually dominant, and which intervention reduces that term at the lowest total cost — where "denormalize the schema" is one candidate among several, not the premise.

**Success criteria.** A reader applies each by scanning section 6:

1. The Conclusion names the dominant cost term, or names the measurement that would identify it, rather than assuming it is join processing.
2. The Conclusion states whether the prompt's premise ("normalized is slower") is true, false, or ill-formed, and cites a chain for that verdict.
3. The Conclusion's recommended action is ordered, and each step names the chain that put it in that position.
4. The Conclusion states which interventions were ranked *below* denormalization and which above, with weighted totals visible in section 4.
5. Every step whose value depends on an unmeasured quantity is identified as such in the Conclusion's confidence line.

**Noted ambiguity, carried rather than resolved:** "database costs" could mean cloud spend, wall-clock latency, contention with transactional traffic, or engineering time (GT-10?). The analysis is constructed to hold across all four senses, and step 1 of the recommendation is the act that disambiguates. This did not rise to the Input Contract's re-open threshold because the headline finding — that nothing has been measured and the premise is not a cost claim — is invariant across all four.

---

## 2. Assumptions Table

The assumption space was enumerated with a fishbone pass over six categories (People, Process, Technology and Tools, Environment, Information, Resources), because "reporting queries cost too much" is multi-causal and intuition cannot enumerate it confidently. Schema normal form turned out to be one twig on one branch. An inversion pass on "denormalizing will meaningfully reduce our reporting costs" supplied rows A4–A8 as necessary preconditions.

| Assumption | Type | Treatment | Verdict | Verification |
|---|---|---|---|---|
| A1 — Normalized schemas are slower than denormalized ones | convention | challenge explicitly before use | **Discard** — contradicted by GT-1; it is a workload claim wearing the grammar of a schema claim | GT-1, read-at-source |
| A2 — The schema is what is wrong | untested belief | verify or flag | **Challenge** — GT-6 shows nothing measured; the fishbone puts schema on one of six branches | unverified — flagged |
| A3 — "Cost" means cloud spend | untested belief | verify or flag | **Challenge** — four candidate senses, none stated | unverified — flagged (GT-10?) |
| A4 — Joins dominate reporting query cost *(inversion P1)* | untested belief | verify or flag | **Challenge** — the load-bearing precondition of A1 | unverified — flagged (GT-8?) |
| A5 — Wider denormalized rows do not offset the join saving *(inversion P2)* | untested belief | verify or flag | **Challenge** — sign unknown per C6 | unverified — flagged (GT-8?, GT-11?) |
| A6 — Added write/ETL/storage cost is smaller than the read saving *(inversion P3)* | untested belief | verify or flag | **Challenge** — GT-7 makes the cost certain; the magnitude is not | unverified — flagged |
| A7 — Reports need per-execution freshness *(inversion P4)* | untested belief | verify or flag | **Challenge** — if false, precomputation dominates (C5) | unverified — flagged (GT-9?) |
| A8 — These tables are read-dominated *(inversion P5)* | untested belief | verify or flag | **Challenge** — surfaced again by the C6 audit | unverified — flagged |
| A9 — Reporting shares an instance with transactional traffic | untested belief | verify or flag | **Challenge** — decides whether contention is the real driver | unverified — flagged |
| A10 — The engine is a mainstream relational row-store | untested belief | verify or flag | **Challenge** — if already columnar, C3's lever is spent | unverified — flagged (GT-11?) |
| A11 — The team controls the application code reading the schema | current constraint | record expiry conditions | **Accept** — expires the moment a vendor or external consumer reads the schema directly, at which point denormalization's blast radius grows and option A falls further | unverified — flagged |
| A12 — Data volume is growing | untested belief | verify or flag | **Challenge** — if flat, tuning's ceiling matters less | unverified — flagged |
| A13 — Reporting SQL is BI-tool-generated and over-selects columns *(fishbone: Process)* | untested belief | verify or flag | **Challenge** — cheap to check, common, and directly amplifies C3 | unverified — flagged |
| A14 — Reports scan unbounded date ranges with no partitioning *(fishbone: Information)* | untested belief | verify or flag | **Challenge** — cheap to check; a frequent order-of-magnitude finding | unverified — flagged |
| A15 — Planner statistics are current *(fishbone: Technology)* | untested belief | verify or flag | **Challenge** — stale statistics produce bad plans at any normal form | unverified — flagged |
| A16 — Arithmetic and storage-bandwidth bounds hold | physical law | accept as ground-truth candidate | **Accept** — survives challenge; promoted to GT-4 and GT-5 | definitional / physical law |
| A17 — The secondary source faithfully renders Codd's objectives | untested belief | verify or flag | **Challenge** — Wikipedia read at source; Codd 1971 not opened. Non-load-bearing: C1's definitional leg stands without it | unverified — flagged |
| A18 — Reporting queries touch few of many columns *(audit: C7 step 2)* | untested belief | verify or flag | **Challenge** — sets the size of C3's lever for this system | unverified — flagged |
| A19 — Index maintenance is transactional in this engine *(audit: C7 step 8)* | untested belief | verify or flag | **Challenge** — not read at source; kept off every chain head for that reason | unverified — flagged |
| A20 — The locked weights reflect this org's real risk posture *(audit: C7 step 1)* | untested belief | verify or flag | **Challenge** — weights were locked before scoring and are stated openly for rebuttal | unverified — flagged |
| A21 — Tuning will be instrumented rather than done blind *(audit: C7 step 7)* | untested belief | verify or flag | **Challenge** — pre-mortem Cluster 5; mitigated by ticketing the measurement separately | unverified — flagged |
| A22 — Bounded staleness is acceptable to report consumers *(audit: C5 step 2)* | untested belief | verify or flag | **Challenge** — pre-mortem Cluster 3; mitigated by the published staleness bound | unverified — flagged |

---

## 3. Ground Truths

**Verified (`read-at-source` — no suffix):**

- **GT-1** Codd's stated objectives for normalization beyond first normal form are: to free the collection of relations from undesirable insertion, update and deletion dependencies; to reduce the need for restructuring as new data types are introduced; to make the relational model more informative to users; and "to make the collection of relations neutral to the query statistics, where these statistics are liable to change as time goes by." — source: Wikipedia, *Database normalization*, Codd's four objectives; read-at-source: the four numbered objectives, objective 4 quoted verbatim above. (Primary source Codd 1971 not opened — see A17.)
- **GT-2** A PostgreSQL materialized view "persist[s] the results in a table-like form"; "the data is not always current"; fresh data is generated with `REFRESH MATERIALIZED VIEW`. — source: PostgreSQL documentation, *Materialized Views* (`rules-materializedviews.html`); read-at-source: all three phrases quoted verbatim from that page.
- **GT-3** In the Parquet columnar format, column chunks are stored separately, "File metadata contains the locations of all the column chunk start locations," and "Readers are expected to first read the file metadata to find all the column chunks they are interested in." — source: parquet.apache.org, *File Format*; read-at-source: both phrases quoted verbatim from that page.
- **GT-4** Total cost of serving a report over a period = (per-execution cost × number of executions) + (cost of building and maintaining any precomputed structure it reads). — arithmetic identity; read-at-source: definitional, being the decomposition of a total into its terms; no external figure exists to read.
- **GT-5** Reading N bytes from a storage device takes at least N/B seconds, where B is the device's achievable bandwidth, and no query can read fewer bytes than the data it must examine. — physical law (bandwidth bound); read-at-source: physical law, no external citation required.
- **GT-6** This analysis was supplied no measurement of the system in question: no schema, no query text, no execution plans, no per-query cost attribution, no bill breakdown, no data volumes, no read/write ratio and no engine identification. — source: direct observation of the request as received; read-at-source: the request text, which contains none of these.
- **GT-7** Denormalization stores a given fact in more than one physical location, so any change to that fact must be applied in more than one location for the database to remain consistent. — definitional consequence of redundancy; read-at-source: definitional, no external figure exists to read.

**Unverified (`?` required):**

- **GT-8?** The fraction of reporting-query cost attributable to join processing, versus scan, aggregation, sort or network transfer, in this system. — unverified: no execution plans or profiles supplied (follows from GT-6).
- **GT-9?** How often each report executes relative to how often its inputs change — the K term in GT-4. — unverified: not supplied.
- **GT-10?** Which cost is meant: cloud spend, wall-clock latency, transactional contention or engineering time. — unverified: the request says "database costs" without disambiguating.
- **GT-11?** The storage engine and physical layout in use — row-store versus column-store, partitioning scheme, existing index set. — unverified: not supplied.
- **GT-12?** Cloud analytical engines commonly bill on-demand query compute by bytes processed, which would convert bytes scanned directly into money. — cited to: Google Cloud BigQuery pricing page. **Phase 3 failure record:** source opened twice (`cloud.google.com/bigquery/pricing` and its `#analysis_pricing_details` anchor); unreachable — retrieved content truncated before the pricing table, and the asserted per-TiB figure was not located.

**Second Phase 3 failure record (resolved at a different citation):** `parquet.apache.org/docs/overview/` was opened and the asserted wording about selective column reading was **not located — citation does not support the claim**. The claim was re-cited to the *File Format* page, where it was read at source; GT-3 carries no suffix on the strength of that second read, not the first.

**Provenance summary.**

```text
?-marked: GT-8, GT-9, GT-10, GT-11, GT-12 (5 of 12)
Read-at-source (unsuffixed GTs feeding HIGH-confidence chains):
  GT-1 — Wikipedia "Database normalization", the four-objective list; objective 4 quoted verbatim
  GT-2 — PostgreSQL docs rules-materializedviews.html; three phrases quoted verbatim
  GT-3 — parquet.apache.org/docs/file-format/; two phrases quoted verbatim
  GT-4 — definitional (decomposition of a total into its terms); no external figure exists
  GT-5 — physical law (bandwidth bound); no external figure exists
  GT-6 — the request text as received; absence observed directly
  GT-7 — definitional (consequence of redundancy); no external figure exists
```

---

## 4. Derivation Chains

### Conclusion C1: The prompt's premise is not a claim about schemas and cannot anchor the decision

```text
GT-1 (Codd's four stated objectives for normalization) + GT-7 (redundancy multiplies the sites a change must be written to)
→ a normal form is defined by the functional-dependency and anomaly properties of a relation, not by the execution cost of any query over it
→ Codd's fourth stated objective is neutrality to the query statistics, so the form makes no claim about speed in either direction *[Assumes: A17 — the secondary source renders Codd faithfully; C1 stands on the definitional leg without it]*
→ "normalized schemas are slower than denormalized ones" is a claim about one workload on one engine wearing the grammar of a claim about schemas
→ the premise cannot anchor a schema decision until that workload is measured
```

**Confidence:** HIGH — GT-1 read at source (four-objective list, objective 4 verbatim); GT-7 definitional, no external figure to read.

### Conclusion C2: No intervention can be ranked on expected saving from the information available, so measurement is the binding action

```text
GT-6 (no schema, query, plan, volume or bill data supplied) + GT-4 (total cost is per-execution cost times executions plus maintenance of precomputed structures) + GT-5 (bytes read bound query time from below)
→ every term in that cost identity is a quantity somebody has to measure
→ not one of those terms has a value for this system
→ ranking any intervention by expected saving requires the term it targets and that term's share of the total
→ no intervention can be ranked on expected saving from the information available
→ the only action whose value does not depend on an unmeasured quantity is the one that produces the measurement
```

**Confidence:** HIGH — GT-6 observed directly in the request text; GT-4 and GT-5 definitional and physical-law respectively, with no external figure to read.

### Conclusion C3: Bytes scanned is governed by physical layout, and normal form does not reach that lever

```text
GT-3 (Parquet stores column chunks separately and readers read only the chunks they want) + GT-5 (bytes read bound query time from below)
→ a columnar layout lets a query touching a few of many columns locate and read only those columns' chunks
→ a row-oriented layout forces the same query to read whole rows to reach those same few columns
→ the bytes a reporting query must read is therefore set by the physical layout rather than by which tables hold which facts
→ physical layout and normal form are independent design axes
→ the bytes-scanned lever belongs to layout, and changing normal form does not reach it
```

**Confidence:** HIGH — GT-3 read at source (two phrases verbatim from the Parquet *File Format* page); GT-5 physical law, no external figure to read.

### Conclusion C4: A materialized view and a denormalized column are the same redundancy, distinguished only by whether reconciliation is named

```text
GT-2 (a materialized view persists results, is not always current, and is refreshed by REFRESH MATERIALIZED VIEW) + GT-7 (redundancy multiplies the sites a change must be written to)
→ a materialized view and a denormalized column both store the same fact in a second place
→ the materialized view's second copy has one named mechanism that reconciles it and a documented non-currency property between reconciliations
→ the denormalized column's second copy is reconciled by whatever application code happens to write it *[Assumes: A11 — the team controls that application code]*
→ the materialized view's divergence is therefore bounded and locatable, and the schema copy's is neither
→ the defensible form of "denormalize for reads" is redundancy carrying a named reconciliation step
```

**Confidence:** HIGH — GT-2 read at source (three phrases verbatim from the PostgreSQL *Materialized Views* page); GT-7 definitional, no external figure to read.

### Conclusion C5: Precomputation's saving scales with execution count and is independent of schema shape

```text
GT-4 (total cost is per-execution cost times executions plus maintenance of precomputed structures) + C4 (redundancy with a named reconciliation step) + GT-9? (execution-to-change ratio unmeasured)
→ a report recomputed K times between two changes to its inputs performs the same work K times for the same answer
→ precomputing that answer once per input change collapses those K executions into one *[Assumes: A22 — bounded staleness is acceptable to report consumers]*
→ the resulting saving scales with K and is set by how often the report runs, not by how the schema is shaped
→ wherever K is materially greater than one, precomputation outranks reshaping the schema as a cost lever
```

**Confidence:** MEDIUM — rests on GT-9? (how often each report runs relative to input changes), removed as a cause of the downgrade by counting executions per report in the query log against the change frequency of its source tables. C4 on this head is HIGH and imposes no ceiling. The chain carries no downgrade cause of its own.

### Conclusion C6: The sign of denormalization's net effect on cost is unknown, making it an unpriced bet

```text
GT-5 (bytes read bound query time from below) + GT-7 (redundancy multiplies the sites a change must be written to) + GT-8? (join share of reporting cost unmeasured) + GT-11? (engine and physical layout unidentified)
→ denormalization removes join work but widens each row, so a scan-bound query reads more bytes per qualifying row than before
→ denormalization also writes each changed fact once per copy, so write and ETL cost rises with the duplication factor *[Assumes: A8 — these tables are read-dominated]*
→ the net effect is a join saving minus a combined scan-and-write penalty
→ neither term of that difference has been measured for this system
→ the sign of the net effect is unknown, which makes denormalizing an unpriced bet rather than an optimization
```

**Confidence:** MEDIUM — rests on GT-8? (join versus scan share of cost), removed by a per-operator cost split from execution plans on the top reporting queries, and GT-11? (engine and storage layout), removed by naming the engine and confirming row versus column orientation. Rated MEDIUM rather than LOW because both unverified inputs are constitutive of the conclusion rather than weakening it: the inference from "unmeasured" to "sign unknown" is tight, and verifying either input would not strengthen this chain but replace it with a different one. The chain carries no downgrade cause of its own.

### Conclusion C7: Decompose the cost, tune on a replica, precompute under a freshness contract, and hold a pre-agreed escalation trigger

Revised in Phase 5: hops 4 and 5 and the disposition content come from the adversarial pass.

```text
GT-10? (which cost is meant is undetermined) + GT-12? (bytes-processed billing model, citation unreadable) + C1 (the premise is not a cost claim) + C2 (no option rankable without measurement) + C3 (layout, not normal form, governs bytes scanned) + C6 (denormalization's net sign unknown)
→ criteria were weighted before any option was scored, with reversibility and independence from unverified assumptions at the top weight, because C2 makes being wrong likely
→ weighted totals: E tune-and-retain = 134 > B materialized views = 116 > C read replica = 96 > D columnar store = 89 > A denormalize the schema = 51 *[Assumes: A18 — reports are column-selective]*
→ the option the prompt proposed ranks last, driven down by irreversibility and by its dependence on the one quantity nobody has measured
→ the adversarial pass moved the read replica from a ranked alternative to a placement decision, so reporting indexes cannot regress the transactional path *[Assumes: A9 — reporting currently shares the transactional instance]*
→ the billing model that would convert bytes scanned directly into money could not be read at its source, so the escalation trigger is set on a measured threshold rather than on a price
→ the recommended plan is to decompose the cost, tune on a replica, precompute under a published freshness contract, and hold a pre-agreed trigger to the columnar store
→[2nd] tuning performed with before-and-after capture produces the per-query cost attribution whose absence C2 names *[Assumes: A21 — tuning will actually be instrumented]*
→[2nd] indexes added to serve reporting add write amplification, which the replica placement confines to the replica *[Assumes: A19 — index maintenance is transactional in this engine]*
→[2nd] reports that become cheap get scheduled more often, so the execution count rises and total cost falls by less than per-execution cost does
→[3rd] with cost attribution in hand the columnar-store decision becomes decidable on evidence rather than on convention
→[3rd] unused materialized views accumulate refresh cost that grows with data volume and can exceed the saving they were built for *[Assumes: A12 — data volume is growing]*
```

**Confidence:** MEDIUM — rests on GT-10? (which cost is meant), removed by the bill/latency decomposition that is step 1 of the recommendation, and GT-12? (bytes-processed billing model), whose Phase 3 failure record names the BigQuery pricing page as unreachable (content truncated); its verification path is a successful read of that page or of the equivalent pricing page for the engine actually in use. Capped at MEDIUM by C6 on its head. C1, C2 and C3 on the head are HIGH and impose no ceiling. The chain carries no downgrade cause of its own.

**Second-order pass:** five downstream effects derived, none of which contradicts a Ground Truth, so no return to Phase 2 was triggered. The induced-demand effect at `[2nd]` qualifies C5's K term without contradicting GT-4, since K is a variable of that identity rather than a claim of it.

**Trade-off detail** (weights locked before any option was scored):

| Criterion | Weight | A denormalize | B mat. views | C replica | D columnar | E tune & retain |
|---|---|---|---|---|---|---|
| Cost reduction per unit effort | 5 | 2 | 5 | 2 | 4 | 5 |
| Reversibility / blast radius | 5 | 1 | 5 | 5 | 3 | 5 |
| Independence from unverified assumptions | 5 | 1 | 4 | 3 | 3 | 5 |
| Consistency safety (higher = safer) | 4 | 1 | 4 | 4 | 3 | 5 |
| Low implementation + maintenance effort | 3 | 2 | 4 | 4 | 2 | 5 |
| Freshness preserved | 3 | 5 | 2 | 4 | 2 | 5 |
| Headroom as data grows | 3 | 2 | 4 | 2 | 5 | 3 |
| **Weighted total** | | **51** | **116** | **96** | **89** | **134** |

E beats B by 13.4%, outside the ~10% band, so no sensitivity tie-break is required. The three top weights are all consequences of GT-6: when nothing is measured, being wrong is the modal outcome, so reversibility and assumption-independence dominate. **If you hand over measurements, those weights change and D can win** — that is precisely what the escalation trigger in step 4 is for.

---

## 5. Abandoned Reasoning

### Dead End: Scoring normalized versus denormalized as the decision axis

**What was tried.** Treating the prompt at face value and running the trade-off with "normalized" and "denormalized" as the two options.

**Why abandoned.** C1 shows the axis carries no cost gradient — a normal form is defined over dependency and anomaly properties, so comparing two points on it does not compare two costs. The matrix would have produced a confident-looking number describing nothing.

**What it ruled out.** No amount of further reasoning about schema shape settles this question. The blocker is the missing join-versus-scan measurement (GT-8?), and no restructuring of the argument substitutes for it.

### Dead End: Deriving a theoretical cost floor for the reporting queries

**What was tried.** Using GT-5 to compute a bytes-scanned lower bound for the reports and bracketing the gap to the actual bill — a theoretical-limit pass.

**Why abandoned.** The derivation requires row counts, column widths and selectivity, none of which exist here (GT-6). The resulting bracket would span several orders of magnitude and straddle every decision threshold, failing the estimate procedure's decision-resolution stop criterion.

**What it ruled out.** A Fermi estimate cannot stand in for the missing measurement in this case. Anyone tempted to bound the problem analytically instead of instrumenting it should expect the same unusable bracket.

### Dead End: Recommending the columnar store outright

**What was tried.** Taking C3 at full strength — layout owns the bytes-scanned lever — and jumping straight to option D.

**Why abandoned.** D scored 89 against E's 134, pushed down by effort and by depending on the same unverified assumptions (A18, GT-11?) as option A. More importantly, the pre-mortem's Cluster 2 showed the real failure is not *choosing* D late but having no trigger that reaches it at all.

**What it ruled out.** Both "go straight to the warehouse" and "never build the warehouse" are wrong here. The defensible position is a pre-committed threshold, which is why step 4 exists.

### Dead End: The read replica as the primary answer

**What was tried.** Option C at 96, second-highest before materialized views were scored.

**Why abandoned.** A replica relocates load without reducing total work — GT-4's per-execution term is unchanged and the maintenance term grows by one instance. It addresses contention only, which is one of four candidate senses of "cost" (GT-10?).

**What it ruled out.** The replica is not an answer to a cost question. It survives in the recommendation as a *placement* decision from pre-mortem Cluster 4, which is a different claim than the one that scored 96.

---

## 6. Conclusion

**Recommended approach:** Do not denormalize; name the dominant cost term first, then reduce it with reversible measures placed off the transactional path (chain C1, chain C7).

Execute in this order:

1. Produce a one-page decomposition of the database bill — or of the latency budget, if latency is what "cost" means here — into storage, idle provisioned compute, query compute and data transfer, and name the term this work targets (chain C2).
2. Tune the reporting queries, indexes, partitioning and retention against that term on a read replica rather than on the primary, capturing a before-and-after figure per report (chain C2, chain C7).
3. Add materialized views for the reports whose execution count between input changes is materially greater than one, each shipping with a refresh schedule, a published staleness bound, and a freshness indicator visible on the report itself (chain C4, chain C5).
4. Fix the escalation trigger now: if steps 2 and 3 do not move the targeted term by an agreed threshold, begin the columnar-store migration without re-litigating it (chain C3, chain C7).

**Key insight:** A materialized view and a denormalized column are the same redundancy, and the only difference that matters is that one of them carries a named reconciliation step and a documented staleness property while the other leaves reconciliation to whatever application code happens to write it (chain C4).

**Trade-offs acknowledged:** Tuning buys time rather than headroom because it does not reach the bytes-scanned lever that layout owns, materialized views trade per-execution freshness for cost, and deferring the columnar store accepts the risk that data growth outruns the tuning before the trigger fires (chain C3, chain C5, chain C7).

**Confidence:** MEDIUM — the contributing chains rated below HIGH are C5, C6 and C7; C5 rests on GT-9?, C6 on GT-8? and GT-11?, and C7 on GT-10? and GT-12?, each with its verification path given on its own chain's confidence line. Chains C1, C2, C3 and C4 are HIGH and every claim above rests on at least one of them. The Conclusion carries no downgrade cause of its own beyond those three chains (chains C1–C7).

---

## Self-Audit Gate

**Criterion 1: Identify Essence**
Quoted span: "Which term of our reporting workload's cost is actually dominant, and which intervention reduces that term at the lowest total cost — where 'denormalize the schema' is one candidate among several, not the premise."
Band: **Rigorous**
Justification: a single sentence naming the underlying decision rather than the triggering complaint, followed by five success criteria each stating a verb-subject-outcome test applicable by scanning section 6 without interpretation.

**Criterion 2: Challenge Assumptions**
Quoted span (Assumption Audit scan): "Audit complete: 39 steps visited, 10 assumptions surfaced, all 10 added to the Assumptions Table."
Band: **Rigorous**
Justification: every Type value is drawn from the four-type scheme, every Verdict leads with Accept/Challenge/Discard followed by an em-dash justification, A1 is genuinely discarded rather than labelled, A11's current-constraint verdict records its expiry in the justification rather than the token slot, and the audit table carries one row per chain per step across all 39 steps with no step skipped.

**Criterion 3: Establish Ground Truths**
Quoted span: enumerated GT-8, GT-9, GT-10, GT-11, GT-12; the Ground Truths list carries `?` on exactly those five and on no others, and the stated count (5 of 12) equals the enumeration's length. Each of GT-1 through GT-7 feeds at least one HIGH-confidence chain (GT-1→C1, GT-2→C4, GT-3→C3, GT-4→C2, GT-5→C2/C3, GT-6→C2, GT-7→C1/C4) and each names its read-at-source location.
Band: **Rigorous**
Justification: stable IDs matching section 4, provenance labels throughout, a correct ID-level enumeration, read-at-source locations named for every unsuffixed GT feeding a HIGH chain, and two Phase 3 failure records (GT-12? unreachable; the Parquet overview page recorded as *citation does not support the claim* before re-citation) distinguishing a downgrade from a skipped attempt. Exception (a) is claimed for GT-12?, which feeds only the MEDIUM chain C7.

**Criterion 4: Reason Upward**
Quoted span (self-audit scan, chain-form table): all seven rows read "Form conforming? yes / Rule applied n/a / Dependency clean? yes". Directly from section 5: "Why abandoned. C1 shows the axis carries no cost gradient — a normal form is defined over dependency and anomaly properties, so comparing two points on it does not compare two costs."
Band: **Rigorous**
Justification: seven chains in the prescribed head-plus-arrow-led form with one hop per physical line, each carrying genuine intermediates; four dead ends using the What-was-tried / Why-abandoned / What-it-ruled-out structure with specific structural abandonment reasons; ten `[Assumes: X]` declarations on the steps that introduce them; no analogy used as direct evidence — the one reference to common industry practice (GT-12?) is carried as a flagged ground truth with a failure record rather than offered as justification.

**Criterion 5: Validate**
Quoted span: "**Confidence:** MEDIUM — rests on GT-8? (join versus scan share of cost), removed by a per-operator cost split from execution plans on the top reporting queries, and GT-11? (engine and storage layout), removed by naming the engine and confirming row versus column orientation."
Band: **Sound**
Justification: every chain names its weakest link and every MEDIUM line names each `GT-N?` input with its verification path and each below-HIGH `Cn` on its head; the adversarial pass record is complete with a past-tense premise, fourteen causes from four viewpoints written before grouping, five clusters each citing the chain and GT ids it bears on, and a named plan change or an accepted risk with a named mitigation per cluster. It bands **Sound** rather than Rigorous for one stated reason: the overall Conclusion rating is MEDIUM rather than HIGH, because C5, C6 and C7 contribute to it. Neither EXCEPT clause is claimed. Per the criterion's own banding rule this is a legitimate honestly-caveated analysis, and the verdict says so rather than reporting Rigorous alongside a MEDIUM rating.

**Criterion 6: Conclusion-to-Ground-Truth Traceability**
Quoted span (self-audit scan, claim-inventory table): all eight claim rows carry a chain id in the "Chain cited" column and none reads "none — untraced"; the single excluded row is "Execute in this order:", excluded under the clause that prose carrying neither a bold colon lead-in nor a list marker is not a claim. Directly from section 6: "**Key insight:** A materialized view and a denormalized column are the same redundancy…"
Band: **Rigorous**
Justification: all eight section-6 claims trace to named section-4 chains, no claim is introduced that does not appear in a chain, and the Key Insight names a non-obvious finding — the identity between a materialized view and a denormalized column — rather than restating the recommended approach, which is about ordering the work.

**Gate result: PASS.** No criterion Absent; exactly one criterion (5) at Sound, none at Hand-wavy. No Fix/Repeat pass was required, and no re-entry edge fired. The output template and the Self-Audit Gate rubric were both read successfully; the closure ledger, the self-audit scan and the gate all ran.

---

## The short version

Your premise is the part to drop. Normalization is defined over update-anomaly and functional-dependency properties — Codd's fourth stated objective is explicitly *neutrality to the query statistics*. "Normalized is slower" is a claim about one workload on one engine, and you have not measured that workload.

The lever you are actually reaching for belongs to **physical layout**, not normal form. Bytes scanned is set by whether a query reads whole rows or just the columns it wants — a different axis entirely, and one you can move without touching which tables hold which facts.

So: **decompose the bill before you touch the schema.** If query compute is not the largest movable term — if it is storage or idle provisioned compute — the whole conversation is about the wrong thing. Then tune on a replica, precompute the reports that run more often than their data changes, and pre-commit the threshold that sends you to a columnar store. Denormalizing the schema scored last of five options, mostly because it is irreversible and because its payoff depends entirely on the one number nobody has measured.

And the reframe worth keeping: an index and a materialized view *are* denormalization — redundancy, the same fact stored twice. The difference is that they come with a named reconciliation step and a documented staleness property. Schema-level denormalization is the same bet without either.