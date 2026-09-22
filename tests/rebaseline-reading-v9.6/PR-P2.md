**Missing inputs.** I couldn't ask you for clarification in this session, so I'm stating the gaps up front and doing a best-effort analysis. I don't have your database engine, how it's billed (you pay per query, or you pay for a fixed instance size), your bill broken down by cost line, your reporting queries or their execution plans, how much data is written versus read, or how fresh reports need to be. This repository doesn't hold any of it either: searching the tracked files for schema, query or reporting code found only `scripts/report-conformance.py`, which is this project's conformance reporter. Every conclusion below that depends on those facts is marked `?` and capped at MEDIUM.

- **Process disclosures:** No re-entry step fired. The output template, the Self-Audit Gate rubric and the pre-mortem procedure were each opened and read.
- **Mode:** No technique-specific phrase matched, so the full analysis ran. Fishbone and inversion weren't needed because the assumption set was small and listed directly. Estimate had no figures to rebuild, and theoretical-limit didn't apply. Trade-off was replaced by a dominance argument (see Dead End 1). Second-order was applied to C3, and pre-mortem was used in the adversarial pass.

---

## 1. Problem Essence

**Core problem:** Should you change your schema to lower the cost of your reporting queries, given that the claim "normalized is slower" hasn't been tested against your workload?

**Success criteria:**
- The Conclusion says whether "normalized is slower" is a property of normalization or a conditional trade.
- The Conclusion names a first action that doesn't depend on unmeasured facts about your workload.
- The Conclusion says where denormalization should happen, if it happens at all, and under what measured condition.

## 2. Assumptions Table

| Assumption | Type | Treatment | Verdict | Verification |
|---|---|---|---|---|
| A1: Normalized schemas are slower than denormalized ones ("everyone knows") | untested belief | Verify, or flag it as unverified | Challenge — C1 shows it's one side of a read-versus-write trade, not a general property | Derived in C1 from GT-1 and GT-2 |
| A2: Denormalization stores one fact in several places, and a join combines rows when the query runs | physical law | Accept as a ground-truth candidate | Accept — these are definitions (formal logic) | Definitional; becomes GT-1 and GT-2 |
| A3: Joins are the main cost in your reporting queries | untested belief | Verify, or flag it as unverified | Challenge — no execution plans were supplied | unverified — flagged (GT-3?) |
| A4: Reporting queries run against the same database your application writes to | untested belief | Verify, or flag it as unverified | Challenge — your setup is unknown | unverified — flagged (GT-4?) |
| A5: Reporting compute is the biggest line on your database bill | untested belief | Verify, or flag it as unverified | Challenge — storage, backups, data transfer or idle capacity could be bigger | unverified — flagged (GT-5?) |
| A6: Doing less query work lowers the bill (surfaced by the Assumption Audit) | current constraint | Record when it stops holding | Accept — only while billing is per query; on a fixed-size instance, less work saves nothing until the instance is made smaller | unverified — flagged; C2's measurement step records the billing model |
| A7: "Denormalize the source tables" is the only way to get pre-joined data | convention | Challenge it explicitly | Discard — a separate read copy also provides pre-joined data (C3) | C3 hop 2 |
| A8: Reports can tolerate the read copy lagging behind the live data (surfaced by the Assumption Audit) | untested belief | Verify, or flag it as unverified | Challenge — how fresh reports must be is unknown; the cost of this being false is assessed on C3's confidence line | unverified — flagged |

## 3. Ground Truths

- **GT-1** A denormalized table stores one fact in more than one row or table. Source: the definition of denormalization; read-at-source: none (it's a definition, and reducing it further ends at the definition itself).
- **GT-2** A join combines rows from separately stored tables at the moment the query runs. Source: the definition of a relational join; read-at-source: none (it's a definition).
- **GT-3?** Your reporting cost is mostly join work. Unverified: no execution plans or query-level cost data were supplied.
- **GT-4?** Your reporting queries run against the database your application writes to. Unverified: your setup wasn't supplied.
- **GT-5?** Reporting compute is the largest line on your database bill. Unverified: no bill breakdown was supplied.

```text
?-marked: GT-3?, GT-4?, GT-5? (3 of 5)
Read-at-source: GT-1, GT-2 — definitional; no external document holds them
```

## 4. Derivation Chains

### Conclusion C1: "Normalized is slower" is one side of a read-versus-write trade

GT-1 (denormalization duplicates facts, definitional) + GT-2 (join combines rows at query time, definitional)
→ a denormalized table has already done, at write time, the combining a join does at read time
→ every write to a duplicated fact must update each copy or leave the copies inconsistent
→ normalization's read-speed penalty is one side of a read-versus-write trade, not a general property

**Pre-check:** head GT-1, GT-2 · ?-marked: none · lowest cited: none · Inputs ceiling: HIGH
**Confidence:** HIGH. Both inputs are definitions, and each hop follows by deduction. The rival conclusion, "denormalized is simply faster", is ruled out by hop 2 (see §5, Dead End 2).

### Conclusion C2: Measure before changing any schema

C1 (read/write trade) + GT-3? (joins dominate reporting cost) + GT-5? (reporting is the main cost line)
→ denormalizing can cut reporting cost by at most the share of that cost that is join work [Assumes: A6 — less query work lowers the bill]
→ neither the join share nor reporting's share of the bill has been measured
→ the first action is to break the bill down by cost line, record how it's billed, and read execution plans for the top reporting queries

**Pre-check:** head C1 (HIGH), GT-3?, GT-5? · ?-marked: GT-3?, GT-5? · lowest cited: HIGH · Inputs ceiling: MEDIUM
**Confidence:** MEDIUM. The weak side is the inputs: GT-3? becomes verified by reading the execution plans, and GT-5? by breaking down the bill. If A6 is false (a fixed-size instance), the saving only shows up once the instance is resized, and measuring first is still the right step. Nothing competes with "measure first" once the maximum saving is unknown (see §5, Dead End 1).

### Conclusion C3: If joins still dominate, denormalize in a separate read copy, not the source tables

C1 (read/write trade) + C2 (measure first) + GT-4? (reporting runs on the application database)
→ if execution plans show join work still dominates after index and query tuning, reports need pre-joined data
→ a separate read copy (materialized view, replica or warehouse table) supplies pre-joined data without adding copies to the application's write path [Assumes: A8 — reports tolerate refresh lag]
→ denormalize in a separate read copy, not in the source tables
→[2nd] reports show data as of the copy's last refresh
→[2nd] storage and refresh compute are added to the bill
→[3rd] the refresh job becomes a component someone must own and monitor

**Pre-check:** head C1 (HIGH), C2 (MEDIUM), GT-4? · ?-marked: GT-4? · lowest cited: MEDIUM · Inputs ceiling: MEDIUM
**Confidence:** MEDIUM. The weak side is the inputs: C2 is rated below HIGH, and GT-4? becomes verified once you confirm which database the reports actually query. If GT-4? is false, you already have a separate copy, and the conclusion still stands: denormalize that copy. The cost of A8 being false is also accounted for. If reports need zero lag, the copy has to be updated on every write. That is the same write cost that denormalizing the source tables would add (C1, hop 2), so the conclusion doesn't change.

## 5. Abandoned Reasoning

### Dead End 1: Denormalize the source tables now, on the strength of the common belief

**What was tried:** Flatten the tables the application writes to, so reports skip the joins.

**Why abandoned:** C2 shows the saving is capped by a join share nobody has measured. C1 shows this option puts the duplication cost on every application write, while a separate read copy gets the same read benefit without that cost (C3). A separate copy is at least as good on every point except freshness, and freshness is dealt with on C3's confidence line, so a scoring matrix wasn't needed.

**What it ruled out:** Any schema change made before measuring, and denormalizing the source tables whenever a separate copy is possible.

### Dead End 2: Treat "normalized is slower" as simply true

**What was tried:** Taking A1 as a ground truth.

**Why abandoned:** C1, hop 2, contradicts it: the read speed is paid for at write time, so the belief describes one side of a trade, not a fact.

**What it ruled out:** Any reasoning that starts from "normalization is the problem" without looking at the ratio of reads to writes.

## 6. Conclusion

**Recommended approach:** Measure first. Break your database bill down by cost line, record whether you pay per query or for a fixed instance, and read the execution plans for your top reporting queries before changing any schema (chain C2).

**Key insight:** Being slower isn't a property of normalization. It's a trade of read speed for write cost, and a separate read copy gets the read benefit without adding the write cost to your application's tables (chains C1, C3).

**Conditional next step:** If joins still dominate after index and query tuning, denormalize into a separate read copy (materialized view, replica or warehouse table), not the source tables (chain C3).

**Trade-offs acknowledged:** The read copy adds storage and refresh compute, shows data only as of its last refresh, and needs an owner (chain C3).

**Pre-check:** head C1 (HIGH), C2 (MEDIUM), C3 (MEDIUM) · ?-marked: none · lowest cited: MEDIUM · Inputs ceiling: MEDIUM
**Confidence:** MEDIUM. Chains C2 and C3 are rated below HIGH, and their confidence lines name what would verify their inputs. The Conclusion adds no weaknesses of its own.

---

## Assumption Audit scan (process output)

| Chain | Step | Step Text (brief) | Assumption surfaced? | Added to Table? |
|---|---|---|---|---|
| C1 | 1 | Denormalized table did the join at write time | none | n/a |
| C1 | 2 | Writes must update each copy | none | n/a |
| C1 | 3 | A trade, not a property | none | n/a |
| C2 | 1 | Saving capped at the join share | A6 (billing model) | yes |
| C2 | 2 | Shares are unmeasured | none (GT-3?, GT-5?) | n/a |
| C2 | 3 | Measure first | none | n/a |
| C3 | 1 | If joins dominate after tuning, reports need pre-joined data | none | n/a |
| C3 | 2 | A read copy supplies it off the write path | A8 (refresh lag tolerated) | yes |
| C3 | 3 | Denormalize in the copy, not the source | none | n/a |
| C3 | [2nd] | Reports lag | none | n/a |
| C3 | [2nd] | Storage and refresh cost added | none | n/a |
| C3 | [3rd] | Refresh job needs an owner | none | n/a |

## Adversarial pass (process output)

**Recompute:** Not applicable, because no chain contains a computed figure.

**Sensitivity:** GT-3? (joins dominate reporting cost) is the ground truth whose falsity would change the result. It is `?`-marked. If it's false, C3's condition never triggers and the plan stops at measuring and tuning. It is carried as a caveat on C2 and C3. The weakest link in each chain:
- C1: hop 2, which reaches its conclusion by deduction only.
- C2: hop 1, which depends on A6 (the billing model).
- C3: hop 2, which depends on A8 (refresh lag).

**Rival:** "Denormalize the source tables now" is ruled out by C1 and C2 in §5, Dead End 1.

**Premise:** Six months on, the plan has failed: the database bill is no lower and people trust the reports less.

**Causes** (from four viewpoints: the database administrator doing the work, the analyst reading the reports, whoever pays the bill, and the application developer):
1. We optimized query speed instead of the billed cost.
2. We're billed for a fixed instance size, so query work fell but the instance was never made smaller.
3. The new indexes slowed writes to the application tables.
4. Refreshing the read copy costs as much compute as the joins it replaced.
5. Report figures lag behind the live application and don't match it.
6. New ad-hoc reports needed joins the copy didn't have, so they ran against the source tables anyway.
7. The real cost driver was storage or backups, not reporting.
8. The warehouse brought a second bill that was bigger than the savings.
9. Someone flattened the source tables anyway "for speed", and duplicated values started disagreeing after updates.
10. The refresh broke silently after a schema migration.

**Clusters:**
- K1, the target was never measured (causes 1, 2, 7). Bears on C2, GT-3?, GT-5? and A6.
- K2, the read copy's own cost and freshness (causes 4, 5, 8, 10). Bears on C3 and A8.
- K3, the scope of the pre-joined data drifted (causes 3, 6, 9). Bears on C1 and C3.

**Disposition:**
- K1, plan change: success is measured as billed cost, not latency, and the billing model is recorded before any change (now part of C2's conclusion).
- K2, plan change: before building the copy, compare its estimated refresh cost with the join cost it removes, agree a freshness target with the people who read the reports, and put an alert on refresh failures.
- K3, accepted risk with a named mitigation: the copy covers only the top reporting queries that were measured, everything else stays on the tuned source, and denormalizing the source tables is ruled out unless the measured write rate on those columns is low.

**Falsification:** The conclusion is false if measurements show a small join share but denormalizing still lowers the bill substantially, or if, at every freshness level the report owners will accept, refreshing the copy costs more than the joins it removes.

## §6→§4 closure ledger (process output)

```text
- "Measure first ... before changing any schema" → chain C2 ✓
- "Being slower isn't a property of normalization ..." → chains C1, C3 ✓
- "If joins still dominate ... separate read copy" → chain C3 ✓
- "The read copy adds storage and refresh compute ..." → chain C3 ✓
- "Pre-check: head C1, C2, C3 ..." → chains C1, C2, C3 ✓
- "Confidence: MEDIUM — Chains C2 and C3 ..." → chains C2, C3 ✓
```

## Self-audit scan (process output)

| Chain | Chain Head (brief) | Form conforming? | Rule applied | Dependency clean? |
|---|---|---|---|---|
| C1 | GT-1 + GT-2 | yes | n/a | yes |
| C2 | C1 + GT-3? + GT-5? | yes | n/a | yes |
| C3 | C1 + C2 + GT-4? | yes | n/a | yes |

| §6 Span (brief) | Construct | Claim under R11? | R11 clause applied | Chain cited |
|---|---|---|---|---|
| Recommended approach: measure first | bold lead-in | yes | prescribed lead-in; colon closes the bold span | C2 |
| Key insight: a trade, not a property | bold lead-in | yes | prescribed lead-in | C1, C3 |
| Conditional next step: read copy | bold lead-in | yes | colon closes the bold span | C3 |
| Trade-offs acknowledged: storage, lag, owner | bold lead-in | yes | prescribed lead-in | C3 |
| Pre-check | bold lead-in | yes | colon closes the bold span | C1, C2, C3 |
| Confidence: MEDIUM | bold lead-in | yes | colon closes the bold span | C2, C3 |

```text
Scan complete: 3 chain rows, one per section-4 chain block in order; 6 section-6 rows, one per construct in order — 6 claims under R11, 0 excluded. 0 chains malformed, 0 claims untraced.
```

## Self-Audit Gate (process output)

**Criterion 1: Identify Essence**
Quoted span: "Should you change your schema to lower the cost of your reporting queries, given that the claim "normalized is slower" hasn't been tested against your workload?"
Band: **Rigorous**
Justification: The statement names the decision rather than the prompt's framing, and each success criterion can be checked against a specific lead-in in §6.

**Criterion 2: Challenge Assumptions**
Quoted span: "| C2 | 1 | Saving capped at the join share | A6 (billing model) | yes |"
Band: **Rigorous**
Justification: Every row uses one of the four types, challenges are recorded (A1, A3–A5, A8), A7 is discarded, and the audit covers all 12 chain steps, with the two assumptions it surfaced added to the table.

**Criterion 3: Establish Ground Truths**
Quoted span: "Enumerated GT-3?, GT-4?, GT-5?; the list carries `?` on exactly those three." For GT-1 and GT-2, the read-at-source entry is "none (it's a definition)".
Band: **Sound**
Justification: The list of `?`-marked items matches the ground truths, but the two unmarked ground truths feeding the HIGH chain C1 are definitions and have no external source location to name.

**Criterion 4: Reason Upward**
Quoted span: "| C3 | C1 + C2 + GT-4? | yes | n/a | yes |"
Band: **Rigorous**
Justification: All three chains follow the required form, have clean dependencies and include intermediate steps. §5 records two dead ends with the structural reason each was abandoned, and no analogy is used as evidence.

**Criterion 5: Validate**
Quoted span: "**Confidence:** MEDIUM. The weak side is the inputs: C2 is rated below HIGH, and GT-4? becomes verified once you confirm which database the reports actually query."
Band: **Rigorous**
Justification: Each rating is the one its axes allow (C1 HIGH; C2 and C3 MEDIUM, with the weak side named). The cost of A6 and A8 being false is assessed, and the adversarial pass has all eight parts, with a disposition for every cluster.

**Criterion 6: Conclusion-to-Ground-Truth Traceability**
Quoted span: "6 claims under R11, 0 excluded. 0 chains malformed, 0 claims untraced."
Band: **Rigorous**
Justification: Every §6 claim cites a chain, and the Key Insight (a trade, not a property) is a finding the common belief doesn't reach.

The gate is cleared: no criterion scored Absent and none scored Hand-wavy.

---

**Bottom line:** Don't denormalize yet. "Normalized is slower" is really a trade. Pre-joined data is faster to read, but every write then has to update each duplicate copy. Denormalizing can only save the part of your reporting cost that is join work, and nobody has measured that part. First, break down the bill by cost line and find out whether you pay per query or for a fixed instance size. If it's a fixed instance, faster queries save nothing until you shrink it. Then read the execution plans for your worst reporting queries. If joins still dominate after index tuning, put the denormalized data in a separate read copy (materialized view, replica or warehouse table), not in the tables your application writes to.

If you send me the engine, the billing model, the bill breakdown and two or three slow report queries with their execution plans, I can check the three `?`-marked facts and raise C2 and C3 to HIGH where the evidence supports it.