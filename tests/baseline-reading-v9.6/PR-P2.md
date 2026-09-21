**Before the analysis: gaps and disclosures**

- **Inputs I could not get.** I couldn't ask you questions in this session, so this is a best-effort analysis. Six things would change it:
  1. Which database engine or managed service you use.
  2. Whether "cost" means the bill or query latency.
  3. How the bill splits between compute, storage, I/O and licence.
  4. Which reports run, how often, and over how much data.
  5. Whether reporting runs on the same database as your transactional traffic.
  6. How fresh the reports need to be.
- **Nothing to inspect here.** This repository (`/home/chrisdavidson/Projects/first-principles-skill`) is a Markdown plugin. It has no SQL, schema or migration files, so "our database" is outside anything I can read (GT-1).
- **Mode.** No technique-specific phrase appeared in the request, so this runs as a full analysis.
- **Re-entry edges.** None fired.
- **Reference reads.** The output template, Self-Audit Gate, trade-off procedure and pre-mortem procedure were all opened and read.

## §6→§4 closure ledger (process output)

- "Recommended approach: measure first, fix indexes and queries next, add a derived read model where needed, keep the primary schema normalized" → chains C1, C2, C5, C4 ✓
- "Key insight: 'normalized is slower' describes where the join work is paid, not a property of the schema" → chains C3, C4 ✓
- "Trade-offs acknowledged: staleness, write-path overhead, refresh ownership" → chains C4, C5 ✓
- "Confidence: MEDIUM" → chains C1–C5 ✓

---

## 1. Problem Essence

**Core problem:** The question is which change actually lowers what your reporting queries cost you. The follow-on question is whether denormalizing is that change, or just the conventional answer inherited from "normalized schemas are slower."

**Success criteria:**
- The Conclusion names the first action and says why it has to come before any schema change.
- The Conclusion says whether "normalized is slower" is true, false or conditional, and names the condition.
- The Conclusion says when denormalized reads are worth having, and whether they require denormalizing the primary schema.
- The Conclusion names the correctness and write-path costs of whatever it recommends.

## 2. Assumptions Table

| Assumption | Type | Treatment | Verdict | Verification |
|---|---|---|---|---|
| A1: Normalized schemas are slower than denormalized ones | convention | Challenge before use | Challenge — holds only for read-heavy queries whose plans are dominated by joins; on write paths it reverses (C3) | unverified — flagged; tested by reasoning in C3 from GT-4? and GT-5? |
| A2: Reporting queries are the main driver of database cost | untested belief | Verify, or flag as unverified | Challenge — no bill breakdown was given (GT-2); storage, I/O, licence or transactional load could dominate | unverified — flagged; closed by the bill split in C2 |
| A3: Reporting shares a database with transactional traffic | untested belief | Verify, or flag as unverified | Challenge — not stated; it decides whether isolating the reporting load matters | unverified — flagged; closed by checking which host the report connections use |
| A4: "Cost" means dollars | untested belief | Verify, or flag as unverified | Challenge — "costs" could mean latency; if so, a read replica becomes a live option (§5) | unverified — flagged; closed by naming which metric is being reduced |
| A5: Joins dominate the reporting queries' cost | untested belief | Verify, or flag as unverified | Challenge — missing indexes, full scans, stale statistics or wide-row scans cause the same symptom | unverified — flagged; closed by the execution plans captured in C2 |
| A6: Reports need real-time freshness | convention | Challenge before use | Challenge — reports are usually read on an hourly or daily cadence; ask the people who read them | unverified — flagged; C4's conclusion is conditional on it |
| A7: Denormalized reads require a denormalized primary schema | convention | Challenge before use | Discard — contradicted by GT-6?; a derived read model gives the same shape while writes stay normalized (C4) | GT-6? |
| A8: A query's work is at least the data it reads and the rows it processes | physical law | Accept as ground-truth candidate | Accept — a computational lower bound; becomes GT-3? | unverified — flagged (definitional; no source opened) |
| A9: A fact stored twice must be updated twice, or the copies diverge | physical law | Accept as ground-truth candidate | Accept — follows from the definition; becomes GT-5? | unverified — flagged (definitional; no source opened) |
| A10: The engine supports materialized views, summary tables or an external reporting store | current constraint | Record expiry conditions | Accept — holds unless the engine or service tier forbids scheduled jobs or extra tables; until then any engine can keep a table refreshed by a job | unverified — flagged |
| A11: The C5 "magnitude" scores assume a reporting workload dominated by scans or joins | untested belief | Verify, or flag as unverified | Challenge — the scores are judgements made before measurement; C2's plans replace them | unverified — flagged |
| A12: Reporting load varies over the business cycle | untested belief | Verify, or flag as unverified | Accept — if the load turns out flat, capturing a full cycle only costs elapsed time (priced in C2) | unverified — flagged |

## 3. Ground Truths

- **GT-1** This repository contains no SQL, schema, migration or engine-specific files. Source: `git ls-files` filtered for `.sql`, `.prisma`, `.dbml`, migration, schema and alembic patterns; read-at-source: zero matches, and zero matches for postgres, mysql, sqlite, bigquery or snowflake.
- **GT-2** The request names no engine, query text, data volume, bill or latency figure. Source: the request itself; read-at-source: the full text, "Reason from ground truth about our database costs. Everyone knows normalized schemas are slower than denormalized ones. What should we do about our reporting queries?"
- **GT-3?** A query's cost is at least the bytes it reads and the rows it processes. Unverified: this is a computational truism, but no engine cost-model documentation was opened.
- **GT-4?** A join across normalized tables is computed when the query runs. A pre-joined table pays that work when it is written or refreshed instead. Unverified: no engine documentation was opened.
- **GT-5?** A fact stored in more than one place must be updated in every copy, or the copies diverge (the update anomaly that normalization exists to prevent). Unverified: Codd's normal-form definitions were not opened.
- **GT-6?** A precomputed result, such as a materialized view or summary table, costs work once per refresh rather than once per query. Unverified: no engine documentation was opened.
- **GT-7?** Without an index the predicate can use, the engine scans the whole table; with a B-tree index, lookup cost grows roughly with log n. Unverified: no documentation was opened.
- **GT-8?** Columnar storage reads only the columns a query references; row storage reads whole rows. Unverified: no documentation was opened.

```text
?-marked: GT-3, GT-4, GT-5, GT-6, GT-7, GT-8 (6 of 8)
Read-at-source: GT-1 — git ls-files pattern scan, zero matches; GT-2 — request text quoted above
```

No source-read was attempted in Phase 3. Only GT-1 and GT-2 feed a HIGH chain (C1), and both were read directly. GT-3 through GT-8 feed only MEDIUM chains.

## 4. Derivation Chains

### Conclusion C1: Any specific fix named here depends on measurements only you can take

GT-1 (no schema, plans or bill in this repository) + GT-2 (request names no engine, query, volume or bill)
→ neither the repository nor the request contains the query text, execution plans, data volumes or the bill
→ this analysis cannot see which reporting query or which cost component dominates
→ every intervention named below is conditional on measurements only you can take

**Confidence:** HIGH. Inputs: GT-1 and GT-2 were both read at source. Inference: each hop follows by deduction. Rivals: the endpoint is itself a ruling-out, so no separate rival needs settling. Weakest link: hop 1, which would fail only if you had pointed to a schema elsewhere; GT-2 shows you did not.

### Conclusion C2: The first action is measurement, not a schema change

C1 (conditional on your measurement) + GT-3? (cost is at least the work done)
→ the costly component can only be found from each query's measured work, not from the schema's shape
→ total reporting cost is per-run work times run frequency, summed across queries
→ query changes can reduce only the compute share of the bill, so the bill's compute versus storage split bounds any saving
→ reporting load follows the reporting calendar, so a capture shorter than one full cycle can miss the costliest runs [Assumes: A12 — reporting load varies over the business cycle]
→ the first action is to measure over one full reporting cycle, ranking queries by total cost and capturing their execution plans, before any schema change

**Confidence:** MEDIUM. The Inputs axis is short. GT-3? stops being a cause of the downgrade once it is confirmed against your engine's cost-model documentation, or seen to hold in your own `EXPLAIN ANALYZE` output. C1 is HIGH, so it adds no cap. A12 is priced: if the load turns out flat, a full-cycle capture costs only elapsed time and the endpoint still stands. Weakest link: hop 3 depends on A4. If "cost" means latency, the bill split doesn't matter, but the endpoint still stands. Rival: "skip measurement and denormalize" is settled in §5.

### Conclusion C3: "Normalized is slower" is a conditional claim, not a ground truth

GT-4? (join work paid at read time) + GT-5? (duplicated facts must all be updated)
→ denormalizing does not remove join work, it moves that work from read time to write time
→ the move adds a consistency obligation to every write, which the normalized schema did not carry
→ a denormalized schema is faster only for read-heavy queries whose measured plans are dominated by joins
→ "normalized schemas are slower" is a conditional claim about where the work is paid, not a ground truth

**Confidence:** MEDIUM. The Inputs axis is short. GT-4? and GT-5? stop being causes of the downgrade once confirmed against your engine's join-execution documentation and a standard normal-form reference. Rivals: the endpoint rules out the unconditional claim, so it answers its own rival. Weakest link: hop 3, whose "read-heavy" condition is exactly what C2's measurement decides.

### Conclusion C4: Get denormalized reads from a derived read model, not by denormalizing the primary schema

C3 (conditional read benefit) + GT-6? (precomputed results cost once per refresh)
→ the read benefit comes from the shape the report query reads, not from where the source of truth lives
→ a derived read model supplies that shape while writes stay normalized [Assumes: A10 — the engine supports materialized views, summary tables or an external reporting store]
→ its consistency cost is staleness, bounded by the refresh interval
→ where measured plans stay join- or aggregation-dominated and reports tolerate that staleness (A6), build a derived read model rather than denormalizing the primary schema
→[2nd] the staleness bound holds only while the refresh job runs, so a silent refresh failure makes reports silently stale
→[3rd] each derived model therefore needs a named owner, failure alerting and a data-as-of stamp on every report

**Confidence:** MEDIUM. The Inputs axis is short. C3 is MEDIUM, which caps this chain; GT-6? stops being a cause once confirmed against your engine's materialized-view or scheduled-job documentation. A10 is priced: where views aren't supported natively, a plain table refreshed by a scheduled job gives the same shape, so the endpoint still stands. A6 is a condition written into the endpoint, not an unpriced premise. The [2nd] and [3rd] extensions qualify the operating plan, not the endpoint. Rival: "denormalize the primary schema" is settled in §5 and by C5. Weakest link: hop 3, whether the refresh interval your engine can sustain is short enough for your readers.

### Conclusion C5: Of the five options, index and query fixes come first; denormalizing the primary schema comes last

GT-5? (update anomaly) + GT-7? (missing index forces full scan) + GT-8? (columnar reads only referenced columns) + C2 (measure first) + C3 (conditional)
→ weighted totals: A index and query fixes 83, C read replica 80, B derived read model 76, D columnar warehouse 74, E denormalize primary schema 47 [Assumes: A11 — magnitude scores assume a scan- or join-dominated reporting workload]
→ the top four sit within 11% of each other, so the weights alone do not choose among them
→ E trails the nearest option by 27 points and stays last under every re-weighting tested
→ recommend A, index and query fixes, first wherever the plans from C2 show missing-index or avoidable full scans
→[2nd] each added index raises write cost and storage on its table
→[3rd] on write-heavy tables that overhead can exceed the read saving, so an index is kept only if total measured work falls

The trade-off procedure behind these totals:

- **Weights, locked before scoring:**

  | Criterion | Weight |
  |---|---|
  | Cost reduction magnitude | 5 |
  | Correctness safety | 5 |
  | Low effort | 3 |
  | Reversibility | 3 |
  | Isolation of transactional load | 3 |
  | Freshness | 2 |

- **Scores (1–5 per criterion, in the order above):**

  | Option | Scores | Weighted total |
  |---|---|---|
  | A: index and query fixes | 3, 5, 5, 5, 1, 5 | 83 |
  | C: read replica | 1, 5, 4, 5, 5, 4 | 80 |
  | B: derived read model | 4, 4, 4, 4, 2, 3 | 76 |
  | D: columnar warehouse | 4, 4, 2, 3, 5, 2 | 74 |
  | E: denormalize primary schema | 4, 1, 2, 1, 1, 5 | 47 |

- **Sensitivity:**
  - E stays last with the correctness weight cut to 1 (E 43 vs D 58), and with E's magnitude score raised to 5 (E 52).
  - A and C are a near-tie. Raising the isolation weight from 3 to 4 flips them (C 85, A 84). That is only justified if A3 and A4 hold, as covered in §5.

**Confidence:** MEDIUM. The Inputs axis is short:
- GT-5?, GT-7? and GT-8? each stop being causes once confirmed against engine documentation.
- C2 and C3 are MEDIUM and cap this chain.

A11 is priced. If the plans show no index or scan fault, A's magnitude score drops to 1 (total 73) and B leads at 76. But the endpoint is already conditioned on the plans showing such faults, and E stays last under every weighting, so the endpoint still stands.

Rival: the replica is settled in §5 for the dollar-cost reading. If A4 fails, it reopens.

Weakest link: hop 1's magnitude scores, which are judgements made before measurement.

## 5. Abandoned Reasoning

### Dead End: Denormalize the primary schema now

**What was tried:** Taking the request's premise at face value and moving straight to schema denormalization for the reporting tables.

**Why abandoned:**
- Its premise (A1) holds only under a condition nobody has measured (C3).
- It scores last by 27 points under every weighting tested (C5).
- It permanently adds a consistency obligation to every write (GT-5?).

**What it ruled out:** A schema migration as the first move. Denormalized reads stay available through C4 without this cost.

### Dead End: A read replica as the cost fix

**What was tried:** Offloading reporting to a replica, the second-highest total in C5.

**Why abandoned:**
- A replica duplicates capacity and removes none of the work (GT-3?), so under the dollar reading of "cost" it can only raise the bill.
- It wins only if the isolation weight is raised, which is justified only if reporting shares the transactional database (A3) and "cost" means contention latency (A4). Both are unverified.

**What it ruled out:** A replica as a cost reduction. It stays the right tool for a latency problem caused by contention, if your answer to A4 turns out to be latency.

### Dead End: A Fermi estimate of the achievable saving

**What was tried:** Estimating the saving as per-run bytes × run frequency × compute share of the bill.

**Why abandoned:** Every one of those factors lacks a first-principles value (GT-2). Each would be an assumed range, so the bracket would span orders of magnitude and straddle every decision threshold.

**What it ruled out:** Committing budget to any option before C2's measurement.

## 6. Conclusion

**Recommended approach:** Nothing in this repository or the request shows which query costs the most (chain C1), so the first step is measurement. Capture one full reporting cycle, including period-close. Rank queries by per-run work × frequency, with their execution plans, and set that against the bill's compute-versus-storage split (chain C2). Fix indexes and query shape first wherever those plans show missing-index or avoidable full scans (chain C5). Where plans stay dominated by joins or aggregation, add a derived read model (materialized view, summary table or reporting store) and keep the primary schema normalized (chain C4).

**Key insight:** "Normalized is slower" is not a property of a schema. It describes where the join work gets paid. Denormalizing moves that work from read time to write time and adds a consistency obligation (chain C3). A derived read model gets the same read speed-up without placing that obligation on the primary schema (chain C4).

**Trade-offs acknowledged:** Reports read from a derived model are stale by up to one refresh interval. Each one needs a named owner, failure alerting and a data-as-of stamp (chain C4). Every added index or refresh job puts work on the write path, so keep each one only if total measured work falls (chain C5).

**Confidence:** MEDIUM. The contributing chains C2, C3, C4 and C5 are all rated MEDIUM, and only C1 is HIGH (chains C1, C2, C3, C4, C5). The Conclusion rests on no `?`-marked ground truth directly. It rises once your execution plans and bill breakdown replace the unverified inputs and the pre-measurement scores.

---

## Adversarial pass (process output)

**Premise:** Six months on, the reporting-cost plan has failed: the bill did not fall and reports got worse.

**Causes** (unfiltered; viewpoints: implementer/DBA, report reader, whoever pays the bill, transactional-app developer):

1. (implementer) Plans were captured off-peak, so the month-end reports never made the top-N.
2. (payer) The bill was mostly storage and licence, so tuning queries cut almost nothing.
3. (report reader) BI-tool-generated SQL was the real load, and the hand-tuned queries didn't include it.
4. (app developer) New indexes slowed ingest and caused a transactional latency regression.
5. (implementer) View refresh ran at peak and caused lock contention.
6. (implementer) The engine had no incremental refresh, and full refreshes cost more than they saved.
7. (report reader) A stale report went to a board meeting.
8. (implementer) The refresh job failed silently for weeks, and nobody owned it.
9. (payer) The team denormalized anyway on "everyone knows" and skipped measurement.

**Clusters:**

- **K1, measurement mis-scoped** (causes 1, 2, 3, 9). Bears on C1, C2 and GT-3?. The measurement window, bill composition or query population was wrong, or measurement was skipped.
- **K2, work moved rather than removed** (causes 4, 5, 6). Bears on C3, C4, C5, GT-4? and GT-6?. Read savings were paid for on the write or refresh path.
- **K3, derived-data freshness and ownership** (causes 7, 8). Bears on C4 and A6. The staleness bound had nobody holding it.

**Disposition:**

- **K1, plan change.** Capture a full cycle including period-close, split the bill first, and take queries from the engine's query log (e.g. `pg_stat_statements` or its equivalent) so BI-generated SQL is included. Now in C2's hops 3–4 and endpoint.
- **K2, plan change.** Keep each index or view only if total measured work, including writes and refresh, falls, and schedule refreshes off-peak. Now in C5's [2nd]/[3rd] extension and the Trade-offs line.
- **K3, accepted risk with a named mitigation.** Staleness is accepted. The mitigation is a named owner, refresh-failure alerting and a data-as-of stamp on every report. Now in C4's [2nd]/[3rd] extension.

## Assumption Audit (process output)

| Chain | Step | Step Text (brief) | Assumption surfaced? | Added to Table? |
|---|---|---|---|---|
| C1 | 1 | no query text, plans, volumes or bill available | none | n/a |
| C1 | 2 | analysis cannot see the dominant cost | none | n/a |
| C1 | 3 | interventions conditional on your measurement | none | n/a |
| C2 | 1 | cost identified from measured work | none (A5 already in table) | n/a |
| C2 | 2 | total = per-run work × frequency | none | n/a |
| C2 | 3 | query changes cut only compute share | none (A4 already in table) | n/a |
| C2 | 4 | capture must span a full cycle | A12 | yes |
| C2 | 5 | first action is measurement | none | n/a |
| C3 | 1 | denormalizing moves join work to writes | none | n/a |
| C3 | 2 | adds a consistency obligation | none | n/a |
| C3 | 3 | faster only when reads dominate and plans are join-heavy | none (A5 already in table) | n/a |
| C3 | 4 | claim is conditional | none | n/a |
| C4 | 1 | benefit comes from read shape | none | n/a |
| C4 | 2 | derived model supplies the shape | A10 | yes |
| C4 | 3 | cost is bounded staleness | none | n/a |
| C4 | 4 | build derived model when conditions hold | none (A6 already in table) | n/a |
| C4 | 5 [2nd] | silent refresh failure means silent staleness | none | n/a |
| C4 | 6 [3rd] | owner, alerting, data-as-of stamp | none | n/a |
| C5 | 1 | weighted totals | A11 | yes |
| C5 | 2 | top four within 11% | none | n/a |
| C5 | 3 | E last under every re-weighting | none | n/a |
| C5 | 4 | recommend A where plans show scan faults | none | n/a |
| C5 | 5 [2nd] | indexes raise write cost | none | n/a |
| C5 | 6 [3rd] | keep an index only if net work falls | none | n/a |

## Self-audit scan (process output)

| Chain | Chain Head (brief) | Form conforming? | Rule applied | Dependency clean? |
|---|---|---|---|---|
| C1 | GT-1 + GT-2 | yes | n/a | yes |
| C2 | C1 + GT-3? | yes | n/a | yes |
| C3 | GT-4? + GT-5? | yes | n/a | yes |
| C4 | C3 + GT-6? | yes | n/a | yes |
| C5 | GT-5? + GT-7? + GT-8? + C2 + C3 | yes | n/a | yes |

| §6 Span (brief) | Construct | Claim under R11? | R11 clause applied | Chain cited |
|---|---|---|---|---|
| Recommended approach: measure, fix, derived model | bold lead-in | yes | bold lead-in whose colon closes the bold span | C1, C2, C5, C4 |
| Key insight: where the join work is paid | bold lead-in | yes | bold lead-in whose colon closes the bold span | C3, C4 |
| Trade-offs acknowledged: staleness, write overhead | bold lead-in | yes | bold lead-in whose colon closes the bold span | C4, C5 |
| Confidence: MEDIUM | bold lead-in | yes | bold lead-in whose colon closes the bold span | C1–C5 |

```text
Scan complete: 5 chain rows, one per section-4 chain block in order; 4 section-6 rows, one per construct in order — 4 claims under R11, 0 excluded. 0 chains malformed, 0 claims untraced.
```

## Self-Audit Gate verdicts

**Criterion 1: Identify Essence**
Quoted span: "The Conclusion says whether "normalized is slower" is true, false or conditional, and names the condition."
Band: **Rigorous**
Justification: The essence names the actual decision rather than the prompt's framing, and each success criterion is a verb-subject-outcome test that can be checked by reading §6.

**Criterion 2: Challenge Assumptions**
Quoted span: "| C4 | 2 | derived model supplies the shape | A10 | yes |"
Band: **Rigorous**
Justification: All twelve rows use the four-type scheme with matching treatments and token-plus-justification verdicts, one is discarded (A7), and the audit covers every hop of every chain with surfaced assumptions added to the table.

**Criterion 3: Establish Ground Truths**
Quoted span: "enumerated GT-3, GT-4, GT-5, GT-6, GT-7, GT-8; list carries `?` on exactly those six; GT-1 and GT-2, the only unsuffixed entries, feed HIGH chain C1 with named read locations"
Band: **Rigorous**
Justification: The enumeration matches the list, every entry carries a provenance label, and the unsuffixed ground truths feed a HIGH chain with named read-at-source locations.

**Criterion 4: Reason Upward**
Quoted span: "| C5 | GT-5? + GT-7? + GT-8? + C2 + C3 | yes | n/a | yes |" (with every other chain row also conforming), and in §5, "**Why abandoned:** A replica duplicates capacity and removes none of the work (GT-3?)"
Band: **Rigorous**
Justification: Every chain conforms with clean dependencies, each has genuine intermediate steps, §5 records three specific dead ends in the What-was-tried / Why-abandoned / What-it-ruled-out form, no analogy is used as evidence, and assumptions introduced by hops carry inline `[Assumes:]` marks.

**Criterion 5: Validate**
Quoted span: "A11 is priced. If the plans show no index or scan fault, A's magnitude score drops to 1 (total 73) and B leads at 76. But the endpoint is already conditioned on the plans showing such faults, and E stays last under every weighting, so the endpoint still stands."
Band: **Rigorous**
Justification: Every chain names its weakest link and the axis that sets its band. Each MEDIUM line names its `?` inputs with a verification path and its capping chains, and every `[Assumes:]` premise is priced. The Conclusion's MEDIUM equals the weakest contributing chain, and the pre-mortem record has a past-tense premise, causes written before clusters, clusters citing ids, and a disposition for each.

**Criterion 6: Conclusion-to-Ground-Truth Traceability**
Quoted span: "| Key insight: where the join work is paid | bold lead-in | yes | bold lead-in whose colon closes the bold span | C3, C4 |" and "Denormalizing moves that work from read time to write time and adds a consistency obligation (chain C3)."
Band: **Rigorous**
Justification: All four §6 claims cite chains, none are untraced, and the Key Insight (that denormalization relocates work rather than removing it) is a finding the "everyone knows" convention does not reach, not a restatement of the recommendation.

The gate is cleared: no criterion scored Absent and none scored Hand-wavy.

---

**Bottom line:** "Normalized is slower" isn't a fact about schemas. Denormalizing just moves the join work from read time to write time and adds a consistency burden on every write. The right order is:

1. **Measure.** Capture a full reporting cycle, rank queries by per-run work × frequency, get their execution plans, and see how the bill splits between compute and storage.
2. **Fix indexes and query shape** wherever the plans show scan faults.
3. **Add a derived read model** (materialized view or summary table) where joins or aggregation still dominate, and keep the primary schema normalized.

Denormalizing the primary schema came last among the five options under every weighting I tried. Confidence is MEDIUM: I had no access to your engine, queries or bill, and that was the only thing holding it back. Tell me which engine you use and what "cost" means for you, and I can make the recommendation specific.