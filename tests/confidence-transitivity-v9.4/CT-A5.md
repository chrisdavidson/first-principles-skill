Short answer: no. Don't move the rebuild before the lease renews. Renew, and run the spot version as a priced trial alongside the leased server. The reasoning is in section 6, and the self-check comes first.

**How this run went:** this was a full analysis of the whole question. I read the output template and the scoring rubric once each, and both reads worked. The claim check, self-audit scan and scoring all ran. No step was re-run. Every figure in your message came with no source, so each one is marked unverified (`?`). That caps every chain using those figures at MEDIUM.

---

## Assumption Audit scan (process output)

| Chain | Step | Step Text (brief) | Assumption surfaced? | Added to Table? |
|---|---|---|---|---|
| C1 | 1 | unsplit stage is a fixed floor on wall time | none | n/a |
| C1 | 2 | reclaim in unsplit stage costs up to its full length | none | n/a |
| C1 | 3 | reclaim in a split stage costs one worker's share | none | n/a |
| C1 | 4 | longest unsplit stage sets both limits | none | n/a |
| C2 | 1 | one link moves a full file at one speed whatever the worker count | none | n/a |
| C2 | 2 | transfer behaves as an unsplit stage | none | n/a |
| C2 | 3 | data movement is a second floor | none | n/a |
| C3 | 1 | eight-worker compute floor 2.625 h | A16 (cloud worker matches server per share); A17 (merge takes ~2 h on a cloud core) | yes |
| C3 | 2 | 5.375 h headroom | none | n/a |
| C3 | 3 | a 2× split gives a 4.5 h floor | none | n/a |
| C3 | 4 | 4 TB takes ~8.9 h at 1 Gbps, ~0.9 h at 10 Gbps | none | n/a |
| C3 | 5 | a 1 Gbps transfer alone exceeds the window | none (A7 already in table) | n/a |
| C3 | 6 | fits only if split is near-linear and path is fast enough | none | n/a |
| C4 | 1 | per-reclaim costs 2 h / 0.625 h | none | n/a |
| C4 | 2 | three late merge reclaims reach 8.625 h | none | n/a |
| C4 | 3 | holds only if replacement capacity starts at once | none (A6 already in table) | n/a |
| C4 | 4 | on-demand merge removes 2 h exposure | A19 (on-demand single instance reliably obtainable) | yes |
| C4 | 5 | capacity shortage has no arithmetic bound | none | n/a |
| C5 | 1 | saving at most $1,500/month | none | n/a |
| C5 | 2 | ~120,000 GB/month returned | A18 (full index, not a delta, returns nightly) | yes |
| C5 | 3 | break-even transfer price $0.0125/GB | none | n/a |
| C5 | 4 | above $0.0175/GB transfer exceeds the lease | none | n/a |
| C5 | 5 | $600 omits the deciding term | none | n/a |
| C6 | 1 | gross saving ≤ $18,000 | none | n/a |
| C6 | 2 | engineer cost ~$11,500–$19,200 | none (A10 already in table) | n/a |
| C6 | 3 | year-one net ~−$1,200 to +$6,500 | none | n/a |
| C6 | 4 | first-year case is marginal | none | n/a |
| C7 | 1 | three deciding quantities unmeasured | none | n/a |
| C7 | 2 | cancelling lease removes proven path | A20 (no other on-prem machine can run the rebuild) | yes |
| C7 | 3 | [2nd] spot shortage becomes a stale business day | none | n/a |
| C7 | 4 | [2nd] on-demand fallback raises bill above $600 | none | n/a |
| C7 | 5 | [3rd] team takes on spot operations unpriced | none | n/a |
| C7 | 6 | renew + priced shadow pilot | none | n/a |

## §6→§4 closure ledger (process output)

```text
- "Do not move the rebuild before the renewal; renew ... priced shadow pilot" → chain C7 ✓
- "Splitting the work does not decide this move ..." → chains C1, C2, C5 ✓
- "Renewing commits up to $25,200 ..." → chain C6 ✓
- "The trial finishes inside the window on every night ..." → chains C3, C4 ✓
- "The actual cloud bill, including transfer and storage ..." → chain C5 ✓
- "No trial night fails to obtain capacity ..." → chain C4 ✓
- "MEDIUM — the decision-bearing chains rest on ..." → chains C3, C4, C5, C6, C7 ✓
```

## Self-audit scan (process output)

| Chain | Chain Head (brief) | Form conforming? | Rule applied | Dependency clean? |
|---|---|---|---|---|
| C1 | GT-1 + GT-2 | yes | n/a | yes |
| C2 | GT-13 + GT-1 | yes | n/a | yes |
| C3 | C1 + C2 + GT-3? + GT-4? + GT-12? + GT-14? | yes | n/a | yes |
| C4 | C1 + GT-3? + GT-7? + GT-10? | yes | n/a | yes |
| C5 | GT-5? + GT-6? + GT-12? + GT-11? | yes | n/a | yes |
| C6 | GT-5? + GT-6? + GT-8? + GT-15? | yes | n/a | yes |
| C7 | C3 + C4 + C5 + C6 + GT-9? | yes | n/a | yes |

| §6 Span (brief) | Construct | Claim under R11? | R11 clause applied | Chain cited |
|---|---|---|---|---|
| Recommended approach: do not move before renewal | bold lead-in | yes | prescribed lead-in is always a claim | C7 |
| Key insight: splitting does not decide this move | bold lead-in | yes | prescribed lead-in is always a claim | C1, C2, C5 |
| Trade-offs acknowledged: $25,200 commitment | bold lead-in | yes | prescribed lead-in is always a claim | C6 |
| Trial exit criteria, move only if all three hold | bold lead-in | no | section-intro label: colon-terminated span is the whole line, no citation | n/a |
| finishes inside the window every night | list item | yes | list item past forty characters, closes its sentence | C3, C4 |
| actual bill incl. transfer and storage below lease | list item | yes | list item past forty characters, closes its sentence | C5 |
| no night fails to obtain capacity | list item | yes | list item past forty characters, closes its sentence | C4 |
| Confidence: MEDIUM | bold lead-in | yes | bold lead-in whose colon closes the bold span | C3, C4, C5, C6, C7 |
| what would raise confidence to HIGH | prose | no | prose with neither a bold colon lead-in nor a list marker | n/a |

```text
Scan complete: 7 chain rows, one per section-4 chain block in order; 9 section-6 rows, one per construct in order — 7 claims under R11, 2 excluded. 0 chains malformed, 0 claims untraced.
```

## Self-Audit Gate (process output)

**Criterion 1: Identify Essence**
Quoted span: "Can the nightly 4 TB rebuild move from the leased server to eight restartable spot instances before the 12-month renewal, reliably finishing by 06:00 at lower total cost than renewing, and is enough known today to commit?"
Band: **Rigorous**
Justification: The single sentence names the decision and its two tests, time and total cost, rather than the lead's proposal, and each of the four success criteria is a pass/fail property of the Conclusion section.

**Criterion 2: Challenge Assumptions**
Quoted span: "C7 | 2 | cancelling lease removes proven path | A20 (no other on-prem machine can run the rebuild) | yes"
Band: **Rigorous**
Justification: Every row uses one of the four types with its matching treatment and an Accept/Challenge/Discard verdict plus reason, and eight rows are challenged. Every unverified input used in a chain reads "unverified — flagged". The audit scan covers all 33 chain steps, and the five assumptions it surfaced (A16–A20) were added to the table.

**Criterion 3: Establish Ground Truths**
Quoted span: "enumerated GT-3, GT-4, GT-5, GT-6, GT-7, GT-8, GT-9, GT-10, GT-11, GT-12, GT-14, GT-15; the list carries `?` on exactly those twelve, and the three unsuffixed entries GT-1, GT-2, GT-13 each feed a HIGH chain (C1, C2) and name their read location"
Band: **Rigorous**
Justification: The IDs are stable, and the `?` list matches the Ground Truths list exactly. Each unsuffixed entry feeding a HIGH chain names where it was checked: a definition worked through in its own entry, since there is no outside document to open. That definitional basis is disclosed rather than presented as a document read.

**Criterion 4: Reason Upward**
Quoted span: "Scan complete: 7 chain rows, one per section-4 chain block in order; ... 0 chains malformed, 0 claims untraced."
Band: **Rigorous**
Justification: All seven chain rows read form-conforming with clean dependencies. Section 5 records three dead ends in the What-was-tried / Why-abandoned / What-it-ruled-out form. The one analogy-type claim, that cloud is cheaper, is discarded as A12, not used as evidence. The steps that surfaced new assumptions carry `[Assumes:` marks.

**Criterion 5: Validate**
Quoted span: "**Confidence:** MEDIUM — the decision-bearing chains rest on figures supplied without a source (GT-3?, GT-5?, GT-6?, GT-12?) and on quantities nobody has measured (GT-7?, GT-10?, GT-11?, GT-14?)"
Band: **Hand-wavy**
Justification: Every chain names its weakest link and its unverified inputs, and no chain using a `?` input is rated HIGH. But the recommendation, the trade-offs, the exit criteria and the confidence line all rest on MEDIUM chains, with no exception claimed. By the rubric's multiple-conclusion clause that caps this criterion at Hand-wavy. This is an unresolved gap: the missing evidence is your own unsourced figures and unmeasured spot behaviour, which this run could not obtain.

**Criterion 6: Conclusion-to-Ground-Truth Traceability**
Quoted span: "Key insight: splitting does not decide this move | bold lead-in | yes | prescribed lead-in is always a claim | C1, C2, C5"
Band: **Rigorous**
Justification: All seven section-6 claims cite a chain, and none is untraced. The Key Insight is a non-obvious finding, that the merge and the data path set floors and the transfer bill decides the cost, rather than a restatement of the recommendation.

**Gate result:** passed. No criterion is Absent and one is Hand-wavy (Criterion 5), which the rubric tolerates. Nothing was re-run.

---

## 1. Problem Essence

**Core problem:** Can the nightly 4 TB rebuild move from the leased server to eight restartable spot instances before the 12-month renewal, reliably finishing by 06:00 at lower total cost than renewing, and is enough known today to commit?

**Success criteria:**
- The Conclusion gives a go/no-go on moving before the renewal.
- The Conclusion names what decides whether a spot rebuild finishes by 06:00.
- The Conclusion compares the move's first-year cost with the lease, including costs the $600 figure leaves out.
- The Conclusion names the measurements that would change the recommendation.

## 2. Assumptions Table

| Assumption | Type | Treatment | Verdict | Verification |
|---|---|---|---|---|
| A1 — The rebuild takes 7 h, and its last 2 h are a single-core merge. | untested belief | verify, or flag unverified | Accept — your own operational figure; no run log supplied | unverified — flagged (GT-3?) |
| A2 — Splitting across eight workers finishes "comfortably" inside the window. | untested belief | verify, or flag unverified | Challenge — the merge does not split, and the other stages' speedup was never measured (C3) | unverified — flagged |
| A3 — The cloud bill will be about $600/month. | untested belief | verify, or flag unverified | Challenge — nobody priced it, and it omits transfer and storage (C5) | unverified — flagged (GT-6?) |
| A4 — The lease renews at $2,100/month for 12 months. | current constraint | record expiry conditions | Accept — expires at the end of the renewed term; whether a shorter term is available is untested | unverified — flagged (GT-5?) |
| A5 — A reclaimed worker restarts its share from the beginning. | current constraint | record expiry conditions | Accept — expires if the rebuild gains checkpoints within each share | unverified — flagged (GT-7?) |
| A6 — Spot capacity (including replacements) can be obtained whenever it is requested. | untested belief | verify, or flag unverified | Challenge — no buying history, and no regional reclaim or availability data (C4) | unverified — flagged (GT-10?) |
| A7 — Search serving stays on-premises, so the built index must come back every night. | untested belief | verify, or flag unverified | Challenge — your message does not say where search is served; if serving is in the same cloud, the transfer term disappears (C5) | unverified — flagged (GT-14?) |
| A8 — Cloud transfer out is billed at a rate above break-even. | untested belief | verify, or flag unverified | Challenge — no provider price list was opened in this analysis | unverified — flagged (GT-11?) |
| A9 — The move takes one engineer four weeks. | untested belief | verify, or flag unverified | Accept — the lead's estimate, with no task breakdown | unverified — flagged (GT-8?) |
| A10 — An engineer's fully loaded cost is $150k–$250k a year. | untested belief | verify, or flag unverified | Challenge — my own range; no payroll data | unverified — flagged (GT-15?) |
| A11 — Missing 06:00 means yesterday's index serves for the whole business day. | current constraint | record expiry conditions | Accept — expires if search can swap in a new index mid-day | unverified — flagged (GT-9?) |
| A12 — Cloud capacity is cheaper than leased hardware. | convention | challenge before use | Discard — industry framing, not a fact about this workload; replaced by the arithmetic in C5 and C6 | not used in any chain |
| A13 — Wall time ≥ serial time + parallel time ÷ workers. | physical law | accept as ground-truth candidate | Accept — follows from the definitions of serial and parallel time (GT-1) | definition, checked in GT-1 |
| A14 — Transfer time = bits ÷ link speed. | physical law | accept as ground-truth candidate | Accept — definition of data rate (GT-13) | definition, checked in GT-13 |
| A15 — A restart from zero costs at most the length of the restarted stage. | physical law | accept as ground-truth candidate | Accept — follows from the definition of restarting (GT-2) | definition, checked in GT-2 |
| A16 — Each cloud worker matches the server's throughput on its one-eighth share (added by audit). | untested belief | verify, or flag unverified | Challenge — instance size and disk speed are unspecified | unverified — flagged |
| A17 — The merge takes about 2 h on a cloud core (added by audit). | untested belief | verify, or flag unverified | Challenge — cloud and on-prem single-core speeds are not compared | unverified — flagged |
| A18 — The full index, not just the changes, returns each night (added by audit). | untested belief | verify, or flag unverified | Challenge — a full nightly rebuild implies a full artifact, but shipping only changes was not ruled out | unverified — flagged |
| A19 — A single on-demand instance for the merge is reliably obtainable (added by audit). | untested belief | verify, or flag unverified | Challenge — no buying history | unverified — flagged |
| A20 — No other on-prem machine could run the rebuild as a fallback (added by audit). | current constraint | record expiry conditions | Accept — expires if spare on-prem hardware exists | unverified — flagged |

## 3. Ground Truths

- **GT-1** Wall time on *n* workers is at least *s + p/n*, where *s* is the unsplit time and *p* the splittable time — source: Amdahl's bound, reduced here to definitions; read-at-source: the unsplit stage takes *s* whatever *n* is, and *p* shared *n* ways cannot finish in under *p/n* (derivation in this entry; no outside document is involved)
- **GT-2** If a stage restarts from zero, one reclaim adds at most that stage's full length — source: definition of a restart; read-at-source: the worst case is a reclaim just before completion, which repeats the whole stage (derivation in this entry)
- **GT-3?** The rebuild takes 7 h, of which the final 2 h are a single-core merge, leaving 5 h of other work — unverified: your figure, no source or log
- **GT-4?** The window runs 22:00–06:00, which is 8 h — unverified: your figure
- **GT-5?** The lease renews at $2,100/month for 12 months, $25,200 in total — unverified: your figure
- **GT-6?** The lead expects about $600/month, and nobody has priced it — unverified: your statement
- **GT-7?** Regional reclaim frequency is unknown, and a reclaimed worker restarts its share from the beginning — unverified: your statement
- **GT-8?** The move needs one engineer for four weeks — unverified: the lead's estimate
- **GT-9?** A missed 06:00 serves yesterday's index for the whole business day — unverified: your statement
- **GT-10?** The team has never bought spot capacity, so whether capacity will be available is unknown — unverified: your statement
- **GT-11?** The cloud price per GB for data transferred out — unverified: no provider price list opened
- **GT-12?** The index is 4 TB and is rebuilt every night — unverified: your figure
- **GT-13** Transfer time = size in bits ÷ link speed — source: definition of data rate; read-at-source: 4 TB = 4×10¹² bytes = 3.2×10¹³ bits (derivation in this entry)
- **GT-14?** Where search is served, and the speed of the link between your site and the cloud — unverified: not stated
- **GT-15?** An engineer's fully loaded cost is $150k–$250k a year — unverified: my own range

**Unverified (`?`) entries:** GT-3, GT-4, GT-5, GT-6, GT-7, GT-8, GT-9, GT-10, GT-11, GT-12, GT-14, GT-15 (12 of 15)

**Checked at the source:** GT-1, GT-2 and GT-13 are definitions, each worked through in its own entry. They feed the HIGH chains C1 and C2. No outside document needed opening, so no source was unreachable.

## 4. Derivation Chains

### Conclusion C1: The longest unsplit stage limits both the speedup and the worst single reclaim

GT-1 (serial/parallel wall-time bound) + GT-2 (restart-from-zero penalty)
→ adding workers shrinks only the split stages, so the unsplit stage's length is a fixed floor on wall time
→ a reclaim during the unsplit stage costs up to that stage's full length
→ a reclaim during a split stage costs at most one worker's share of it
→ on a restart-from-zero design, the longest unsplit stage sets both the speedup ceiling and the worst single-reclaim penalty

**Confidence:** HIGH
Weakest link: this holds only for designs that restart from zero (A5). Adding checkpoints would shrink the reclaim penalty but not the speedup ceiling.

### Conclusion C2: Moving the data is a second floor that more workers cannot lower

GT-13 (transfer time equals bits over link rate) + GT-1 (serial/parallel wall-time bound)
→ shipping a full artifact across one link takes the same time however many workers produced it
→ that transfer behaves as an unsplit stage inside the window
→ data movement is a second wall-time floor that adding spot workers cannot lower

**Confidence:** HIGH
Weakest link: this applies only if a full artifact crosses a single link. Parallel links, or keeping the data in the cloud, change the link speed or remove the transfer.

### Conclusion C3: The plan fits the window only under two conditions nobody has measured

C1 (unsplit-stage floor) + C2 (transfer floor) + GT-3? (7 h rebuild, 2 h merge) + GT-4? (8 h window) + GT-12? (4 TB index) + GT-14? (link speed unstated)
→ the eight-worker compute floor is 2 h + 5 h / 8 = 2.625 h *[Assumes: A16 — cloud worker matches server per share]* *[Assumes: A17 — merge ~2 h on a cloud core]*
→ that floor leaves at most 5.375 h of headroom inside the 8 h window
→ a 2× rather than 8× split of the non-merge 5 h raises the floor to 4.5 h
→ moving 3.2×10¹³ bits takes about 8.9 h at 1 Gbps and about 0.9 h at 10 Gbps before protocol overhead
→ a single 1 Gbps transfer of the index alone would overrun the 8 h window
→ the plan fits only if the split is near-linear and the data path runs at roughly 10 Gbps or better, or the index never leaves the cloud

**Confidence:** MEDIUM
Downgraded by GT-3?, GT-4?, GT-12? and GT-14?. Weakest link: step 1's speedup assumption (A16) and the unknown link speed (GT-14?). A timed trial run plus the actual link speed and search-serving location would raise this to HIGH.

### Conclusion C4: A few reclaims fit in the headroom; a night without capacity has no bound

C1 (worst single-reclaim penalty) + GT-3? (2 h single-core merge) + GT-7? (reclaim rate unknown, restart from zero) + GT-10? (capacity availability unknown)
→ at the 2.625 h floor, each late merge reclaim adds up to 2 h and each late worker reclaim up to 0.625 h
→ three late merge reclaims in one night reach 2.625 + 3 × 2 = 8.625 h, past 06:00
→ this tolerance holds only if replacement capacity starts at once
→ running the merge on on-demand capacity would remove its 2 h exposure at an unpriced cost *[Assumes: A19 — on-demand single instance reliably obtainable]*
→ the reclaim count looks survivable on paper, but no arithmetic can bound a night when no capacity can be obtained

**Confidence:** MEDIUM
Downgraded by GT-3?, GT-7? and GT-10?. Weakest link: step 3 (A6, replacement capacity). Several weeks of recorded reclaim and launch-failure data from your region would raise this to HIGH.

### Conclusion C5: The $600 figure leaves out the cost that decides the comparison

GT-5? ($2,100/month lease) + GT-6? ($600/month, unpriced) + GT-12? (4 TB nightly) + GT-11? (transfer price unread)
→ the claimed saving is at most $2,100 − $600 = $1,500 a month
→ returning a 4 TB index every night moves about 120,000 GB a month *[Assumes: A18 — full index, not a delta, returns nightly]*
→ that saving disappears once transfer is billed above $1,500 / 120,000 GB = $0.0125 per GB
→ above $2,100 / 120,000 GB = $0.0175 per GB, transfer alone would cost more than the whole lease
→ the $600 estimate leaves out the cost term that decides the comparison, so it cannot yet support the move

**Confidence:** MEDIUM
Downgraded by GT-5?, GT-6?, GT-11? and GT-12?, and by A7 (where search is served). Weakest link: GT-11?. A written quote covering compute, storage and transfer, plus confirmation of where search is served, would raise this to HIGH. The break-even prices themselves depend only on your own figures.

### Conclusion C6: Even on the lead's own figures, the first-year gain is marginal

GT-5? (lease term and price) + GT-6? ($600/month, unpriced) + GT-8? (four engineer-weeks) + GT-15? (loaded engineer cost)
→ over the 12-month term, the gross compute saving is at most 12 × $1,500 = $18,000
→ four engineer-weeks at a $150k–$250k loaded annual cost comes to about $11,500–$19,200
→ year-one net lands between about −$1,200 and +$6,500 before any transfer, storage or fallback cost
→ the first-year financial case for moving before renewal is marginal even on the lead's $600 figure

**Confidence:** MEDIUM
Downgraded by GT-5?, GT-6?, GT-8? and GT-15?. Weakest link: GT-15?, which is my own range. Your actual loaded cost and a priced bill would raise this to HIGH.

### Conclusion C7: Renew, and trial spot beside the lease instead of replacing it

C3 (fit conditions unmeasured) + C4 (capacity risk unbounded) + C5 ($600 omits transfer) + C6 (marginal year-one gain) + GT-9? (a miss serves yesterday's index all day)
→ none of the three quantities that decide the move (split speedup, data-path cost, capacity reliability) has been measured
→ cancelling the lease before measuring them removes the only proven way to finish by 06:00 *[Assumes: A20 — no other on-prem machine can run the rebuild]*
→[2nd] with no fallback server, any night of spot shortage becomes a full business day on yesterday's index
→[2nd] adding on-demand fallback to cover that pushes the bill above the unpriced $600
→[3rd] the team takes on running spot capacity, with no buying history, while the savings case is still unpriced
→ renewing the lease and running the spot rebuild beside it as a priced trial on a copy (a "shadow" run) measures all three quantities without risking a stale day

**Confidence:** MEDIUM
Capped by C3–C6, all MEDIUM, and downgraded by GT-9?. Weakest link: step 2 (A20). The downstream effects contradict no verified ground truth; the fallback cost only undermines GT-6?, which is already flagged, so nothing needed re-examining. Measuring the three quantities in the trial would raise this to HIGH.

## 5. Abandoned Reasoning

### Dead End: Deciding on $600 versus $2,100

**What was tried:** Treating the move as a comparison of the lead's $600 against the $2,100 lease.
**Why abandoned:** The $600 is an unpriced belief (GT-6?), and it leaves out the transfer term that can exceed the lease on its own (C5).
**What it ruled out:** Any decision based on the headline monthly figures alone.

### Dead End: Computing an expected rate of missed mornings from reclaim probability

**What was tried:** Estimating the chance a night misses 06:00 as a function of each worker's reclaim probability.
**Why abandoned:** There is no reclaim data for your region (GT-7?), so the intermediate probability could not be established. Any number would be invented.
**What it ruled out:** A numeric miss probability. C4's count of how many reclaims the headroom absorbs replaces it.

### Dead End: Speeding up the on-prem merge instead

**What was tried:** Reasoning that making the 2 h merge parallel on the existing server would remove the pressure to move.
**Why abandoned:** No ground truth describes the merge algorithm or the server's core count, so whether the merge can be split could not be established.
**What it ruled out:** Recommending it here. It stays an open option to investigate, not a conclusion.

## 6. Conclusion

**Recommended approach:** Do not move the rebuild before the renewal. Renew the lease and run the spot rebuild beside it as a priced trial on a copy, then decide at a later exit point once the trial has measured what matters (chain C7).

**Key insight:** Splitting the work does not decide this move. The single-core merge and the 4 TB data path are floors that more spot workers cannot lower, and an unpriced nightly transfer bill could exceed the entire lease on its own (chains C1, C2, C5).

**Trade-offs acknowledged:** Renewing commits up to $25,200 of lease cost for a year and gives up a best-case first-year gain of roughly −$1,200 to +$6,500 on the lead's own figures (chain C6).

**Trial exit criteria, move only if all three hold:**

- The trial rebuild, including the index transfer, finishes inside the 22:00–06:00 window on every trial night (chains C3, C4).
- The actual cloud bill, including transfer and storage, comes in below the lease with margin (chain C5).
- No trial night fails to obtain capacity, and reclaim restarts stay within the headroom computed for the merge (chain C4).

**Confidence:** MEDIUM. The decision-bearing chains rest on figures supplied without a source (GT-3?, GT-5?, GT-6?, GT-12?) and on quantities nobody has measured (GT-7?, GT-10?, GT-11?, GT-14?), and chains C3 through C7 are each MEDIUM (chains C3, C4, C5, C6, C7).

Four things would raise this to HIGH: a timed trial run, the actual link speed and where search is served, a written price quote that includes transfer, and a few weeks of reclaim and launch-failure records from your region.

---

Separately: the Gmail, Google Calendar and Google Drive connectors need authorising in your claude.ai connector settings before they can be used. This analysis didn't need them.