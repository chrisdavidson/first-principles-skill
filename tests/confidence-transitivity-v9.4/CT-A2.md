**Bottom line:** No. Don't move the rebuild to spot before the lease renews. Renew the lease, or take a shorter term if the lessor offers one. Then run the spot rebuild as a shadow pilot for 60 nights, with the server still producing the index you serve. The case for moving rests on three figures nobody has measured: how fast your network link is, where search is served from, and how often spot workers are reclaimed. With the wrong answers, the move either misses the window or costs more than the lease.

No re-entry edge fired, and no closure ledger, self-audit scan, Self-Audit Gate or template read was left out. Every fact you gave me carries a `?` because it names no source I could open, so the overall confidence is MEDIUM.

---

## Process output

**Technique sweep (full-composer):**
- **Inversion** (assumptions phase): I listed what would make "splitting finishes comfortably" false. That produced assumptions A2, A4, A5 and A9.
- **Fishbone** (assumptions phase): no separate map. The inversion already covered each cause category.
- **Five-whys, reduce-to-primitives mode** (ground-truths phase): I broke the $600 figure into compute, storage, transfer and egress. None of them has been priced, so A6 and A18 are flagged.
- **Estimate** (reasoning phase): used for the time budget (C3) and the egress bracket (C4).
- **Theoretical-limit** (reasoning phase): used for the 3.5× speedup ceiling in C3.
- **Trade-off** (reasoning phase): the matrix below, collapsed into C6.
- **Second-order** (reasoning phase): extends C6. No effect contradicts a ground truth.
- **Pre-mortem** (validation phase): stated as "we moved and it failed." The causes cluster into two structural weaknesses:
  - **No fallback once the lease lapses.** Causes: the merge instance reclaimed near the end, or no spot capacity on some night. Plan change in C5 and C6: keep the server.
  - **Costs and rates nobody measured.** Causes: an egress bill, a slow link, the migration overrunning. Plan change in C3, C4 and C6: measure them in the pilot.

**Trade-off matrix** (weights locked before any scoring; higher is always better):

| Criterion | Weight | A: migrate before renewal | B: renew + shadow pilot | C: short extension + pilot | D: renew, no pilot |
|---|---|---|---|---|---|
| Avoids missed 06:00 | 5 | 2 | 5 | 5 | 4 |
| 12-month cost | 3 | 3 | 2 | 3 | 2 |
| Evidence before commitment | 4 | 1 | 5 | 4 | 2 |
| Engineer effort | 2 | 3 | 3 | 3 | 5 |
| Reversibility | 4 | 1 | 5 | 5 | 4 |
| **Total** | | **33** | **77** | **76** | **60** |

B and C are within 10% of each other. The tie turns on whether the lessor offers a shorter term, which nobody has asked.

**Assumption Audit scan:**

| Chain | Step | Step Text (brief) | Assumption surfaced? | Added to Table? |
|---|---|---|---|---|
| C1 | 1 | splitting removes time only from the parallel part | none | n/a |
| C1 | 2 | reclaim wastes up to full elapsed task length | none | n/a |
| C1 | 3 | longest unsplit task is both unshortened and costliest | none | n/a |
| C1 | 4 | run it on non-reclaimable capacity or checkpoint it | none | n/a |
| C2 | 1 | transfer is serial w.r.t. compute | none | n/a |
| C2 | 2 | link rate bounds cross-boundary designs | none | n/a |
| C3 | 1 | best-case compute ≈2.6 h | A2, A4 | yes |
| C3 | 2 | 3.5× ceiling even with unlimited workers | none | n/a |
| C3 | 3 | ≈5.4 h slack left | none | n/a |
| C3 | 4 | 4 TB at 1 Gbps ≈8.9 h | A5 | yes |
| C3 | 5 | "comfortably" needs ≳10 Gbps or cloud-resident data | none | n/a |
| C4 | 1 | ≈120 TB/month returned | A7 | yes |
| C4 | 2 | ≈$6,000–$10,800/month egress | none (A18 already present) | n/a |
| C4 | 3 | bracket straddles the lease | none | n/a |
| C4 | 4 | cost case undecided | none | n/a |
| C5 | 1 | no measured bound on miss probability | none | n/a |
| C5 | 2 | each miss costs a stale business day | none | n/a |
| C5 | 3 | lapse removes the only proven path | none | n/a |
| C5 | 4 | trades ≤$1,500/month for unmeasured risk | none | n/a |
| C6 | 1 | weighted totals 77/76/60/33 | none | n/a |
| C6 | 2 | lead driven by miss-risk and reversibility | none | n/a |
| C6 | 3 | B and C near-tie | none | n/a |
| C6 | 4 | tie flips on shorter-term availability | A12 | yes |
| C6 | 5 | recommend B | none | n/a |
| C6 | 6 | [2nd] pilot yields measurements | none | n/a |
| C6 | 7 | [3rd] next renewal decided on measurements | none | n/a |
| C6 | 8 | [2nd] forgoes ≤$18,000 of $25,200 | none | n/a |
| C6 | 9 | [2nd] renewal removes deadline pressure | none | n/a |
| C6 | 10 | [3rd] dated exit criterion prevents drift | A19 | yes |

**§6→§4 closure ledger:**
- "do not move before the lease renews; renew … and run spot as a shadow pilot" → chain C6 ✓
- "Measure the link rate and where search is served first" → chain C3, chain C4 ✓
- "Run the merge on on-demand capacity or checkpoint it" → chain C1 ✓
- "Price the real bill from pilot invoices, egress included" → chain C4 ✓
- "Set a dated exit criterion for the pilot" → chain C6 ✓
- "Ask the lessor now whether a shorter term exists" → chain C6 ✓
- "the binding terms are the ones splitting cannot touch" → chain C2, chain C3, chain C4 ✓
- "Renewing forgoes at most about $18,000" → chain C6 ✓
- "Confidence MEDIUM" → chain C3, chain C4, chain C5, chain C6 ✓

## Self-audit scan (process output)

| Chain | Chain Head (brief) | Form conforming? | Rule applied | Dependency clean? |
|---|---|---|---|---|
| C1 | GT-1 + GT-3 | yes | n/a | yes |
| C2 | GT-2 + GT-1 | yes | n/a | yes |
| C3 | GT-4? + GT-5? + GT-6? + C1 + C2 | yes | n/a | yes |
| C4 | GT-6? + GT-13? + GT-8? + GT-7? | yes | n/a | yes |
| C5 | GT-9? + GT-11? + GT-12? + GT-7? + GT-8? + C1 + C3 + C4 | yes | n/a | yes |
| C6 | GT-7? + GT-10? + C3 + C4 + C5 | yes | n/a | yes |

| §6 Span (brief) | Construct | Claim under R11? | R11 clause applied | Chain cited |
|---|---|---|---|---|
| Recommended approach: do not move before renewal | bold lead-in | yes | prescribed lead-in, always a claim | C6 |
| What to do, in order: | bold lead-in | no | section-intro label: its colon-terminated span is the whole line and it carries no citation | n/a |
| Measure link rate and serving location first | list item | yes | list item over forty characters | C3, C4 |
| Run the merge on on-demand capacity | list item | yes | list item over forty characters | C1 |
| Price the real bill from pilot invoices | list item | yes | list item over forty characters | C4 |
| Set a dated exit criterion | list item | yes | list item over forty characters | C6 |
| Ask the lessor about a shorter term | list item | yes | list item over forty characters | C6 |
| Key insight: binding terms splitting cannot touch | bold lead-in | yes | prescribed lead-in, always a claim | C2, C3, C4 |
| Trade-offs acknowledged: forgoes ≤$18,000 | bold lead-in | yes | prescribed lead-in, always a claim | C6 |
| Confidence: MEDIUM | bold lead-in | yes | a bold lead-in whose colon closes the bold span | C3, C4, C5, C6 |
| What would raise confidence (prose) | prose | no | prose with neither a bold colon lead-in nor a list marker | n/a |

```text
Scan complete: 6 chain rows, one per section-4 chain block in order; 11 section-6 rows, one per construct in order — 9 claims under R11, 2 excluded. 0 chains malformed, 0 claims untraced.
```

**Self-Audit Gate verdicts:**

**Criterion 1: Identify Essence**
Quoted span: "Should the team let a $2,100/month lease lapse and commit its nightly 4 TB rebuild to reclaimable spot capacity before the renewal date…"
Band: **Rigorous**
Justification: The statement is one sentence specific to this decision, and each success criterion can be checked by reading the Conclusion.

**Criterion 2: Challenge Assumptions**
Quoted span: "| C3 | 4 | 4 TB at 1 Gbps ≈8.9 h | A5 | yes |"
Band: **Rigorous**
Justification: Every row uses one of the four types with its prescribed treatment and a token-plus-justification verdict, several rows are challenged or discarded, and the audit covers all 29 chain steps.

**Criterion 3: Establish Ground Truths**
Quoted span: I compared the enumeration, "GT-4?, GT-5?, … GT-13? (10 of 13)", against the list, which carries `?` on exactly GT-4 through GT-13. GT-1 to GT-3 are labelled derived-in-analysis.
Band: **Sound**
Justification: The enumeration matches the list. The three unsuffixed ground truths each feed a HIGH chain, but their read location is an in-line derivation rather than an opened external source, which falls short of the read-at-source form.

**Criterion 4: Reason Upward**
Quoted span: "| C6 | GT-7? + GT-10? + C3 + C4 + C5 | yes | n/a | yes |" — and from §5: "Why abandoned: no ground truth describes reclaim behaviour in your region"
Band: **Rigorous**
Justification: All six chains conform, with clean dependencies and at least one intermediate each. The dead ends carry specific reasons, and the one analogy (A20) is discarded rather than used as evidence.

**Criterion 5: Validate**
Quoted span: "**Confidence:** MEDIUM … (chain C3; chain C4; chain C5; chain C6)"
Band: **Hand-wavy**
Justification: Each chain names its weakest link and its `GT-N?` inputs. But several Conclusion claims (the recommendation, the trade-off, and the measurement and pricing items) rest only on MEDIUM chains. The Fix of reading the sources is unavailable because every workload and price fact is user-supplied or unpriced with no source to open, so this is reported as an unresolved gap. No exception is claimed.

**Criterion 6: Conclusion-to-Ground-Truth Traceability**
Quoted span: "| Key insight: binding terms splitting cannot touch | bold lead-in | yes | prescribed lead-in, always a claim | C2, C3, C4 |" — and from §6: "a 4 TB nightly transfer at 1 Gbps takes about 8.9 hours"
Band: **Rigorous**
Justification: All 9 claims cite a chain, and the key insight (transfer time and egress, not compute, are the binding terms) is a finding the splitting argument misses, not a restatement of the recommendation.

The gate is cleared: no criterion is Absent and only one is Hand-wavy.

---

## 1. Problem Essence

**Core problem:** Should the team let a $2,100/month lease lapse and commit its nightly 4 TB rebuild to reclaimable spot capacity before the renewal date, given that neither the time case nor the cost case for spot has been measured and a missed 06:00 costs a full day of stale search?

**Success criteria:**
- The Conclusion states one go/no-go answer on moving before the renewal.
- The Conclusion names the unmeasured quantities that decide whether spot fits the 8-hour window.
- The Conclusion names the unmeasured quantities that decide whether spot costs less than the lease.
- The Conclusion states how the 2-hour single-core merge would be protected from reclaim.
- The Conclusion states what the recommendation costs in forgone savings.

## 2. Assumptions Table

| Assumption | Type | Treatment | Verdict | Verification |
|---|---|---|---|---|
| A1: Splitting across 8 spot instances finishes comfortably inside the window | untested belief | Verify or flag unverified | Challenge — holds only under A2, A4 and A5 (C3) | unverified — flagged |
| A2: The first 5 h splits evenly across machines, and each cloud instance matches the current server's throughput | untested belief | Verify or flag unverified | Challenge — the current server may already use many cores, which would shrink the gain | unverified — flagged |
| A3: The merge cannot run on more than one core | current constraint | Record expiry conditions | Accept — lifts if the merge is re-engineered to run in parallel | your statement; unverified — flagged |
| A4: The merge runs no slower on a cloud core | untested belief | Verify or flag unverified | Challenge — per-core speed varies by instance type | unverified — flagged |
| A5: The index or its inputs cross the on-prem/cloud boundary every night | untested belief | Verify or flag unverified | Challenge — decides whether the transfer term exists at all | unverified — flagged |
| A6: The cloud bill is about $600/month | untested belief | Verify or flag unverified | Challenge — unpriced by your own account, and omits transfer and egress | unverified — flagged |
| A7: Search is served on-prem, so the built index leaves the cloud every night | untested belief | Verify or flag unverified | Challenge — decides whether the egress term exists | unverified — flagged |
| A8: Spot reclaims are rare in your region | untested belief | Verify or flag unverified | Challenge — no regional data exists | unverified — flagged |
| A9: Spot capacity is available every night | untested belief | Verify or flag unverified | Challenge — never tested, since you have never bought spot | unverified — flagged |
| A10: A reclaimed worker restarts its share from the beginning | current constraint | Record expiry conditions | Accept — lifts if shares are checkpointed | your statement; unverified — flagged |
| A11: The lease renews for 12 months at $2,100/month | current constraint | Record expiry conditions | Accept — expires on the renewal date | your statement; unverified — flagged |
| A12: Renewal is a binary choice between a 12-month term and letting it lapse | convention | Challenge before use | Challenge — a shorter or month-to-month term may exist; nobody has asked | unverified — flagged |
| A13: The rebuild window is 22:00–06:00 | current constraint | Record expiry conditions | Accept — lifts if business hours or tolerance for staleness change | your statement; unverified — flagged |
| A14: A missed 06:00 leaves yesterday's index serving all day | current constraint | Record expiry conditions | Accept — lifts if a mid-day index swap is built | your statement; unverified — flagged |
| A15: The migration takes one engineer four weeks | untested belief | Verify or flag unverified | Challenge — the team has no spot experience (GT-12?) | unverified — flagged |
| A16: Adding workers cannot shorten serial work | physical law | Accept as ground-truth candidate | Accept — Amdahl's law; promoted to GT-1 | definition, derived in GT-1 |
| A17: Transfer time equals size divided by link rate | physical law | Accept as ground-truth candidate | Accept — unit arithmetic; promoted to GT-2 | definition, derived in GT-2 |
| A18: Cloud egress costs about $0.05–$0.09/GB | untested belief | Verify or flag unverified | Challenge — no pricing page was opened; feeds only C4 (MEDIUM) | unverified — flagged |
| A19: 60 shadow nights are enough to observe the regional reclaim rate | untested belief | Verify or flag unverified | Challenge — surfaced by the audit; the pilot should extend if reclaims are rare but not zero | unverified — flagged |
| A20: Others run batch jobs on spot successfully, so we can too | convention | Challenge before use | Discard — an analogy with no ground truth about those teams' workloads or regions | not used as evidence |

## 3. Ground Truths

- **GT-1** Amdahl's law: with serial fraction *s* and *N* workers, speedup ≤ 1 / (s + (1−s)/N). A serial step is not shortened by adding workers. — source: definition (Amdahl, 1967); provenance: derived-in-analysis; read location: the formula stated in this entry. No external figure is asserted.
- **GT-2** Transfer time: 1 TB = 8×10¹² bits, so at 1 Gbps one TB takes 8,000 s ≈ 2.2 h, and at 10 Gbps ≈ 0.22 h. — source: SI prefix definitions; provenance: derived-in-analysis; read location: the arithmetic in this entry.
- **GT-3** Restart-from-zero waste: if a task of length L restarts completely when interrupted at elapsed time t, the interruption wastes t, which can be as much as L. — source: definition; provenance: derived-in-analysis; read location: this entry.
- **GT-4?** The window runs 22:00–06:00, which is 8 h. — unverified: your statement, no source named.
- **GT-5?** The rebuild takes 7 h today, and its last 2 h are a single-core merge. — unverified: your statement.
- **GT-6?** The index is 4 TB. — unverified: your statement.
- **GT-7?** The lease renews next quarter at $2,100/month for 12 months. — unverified: your statement.
- **GT-8?** The cloud estimate is about $600/month and has not been priced. — unverified: your statement, which itself says it is unpriced.
- **GT-9?** A reclaimed worker restarts its share from the beginning, and the regional reclaim rate is unknown. — unverified: your statement.
- **GT-10?** The migration needs one engineer for four weeks. — unverified: your statement.
- **GT-11?** A missed 06:00 leaves yesterday's index serving for the whole business day. — unverified: your statement.
- **GT-12?** The team has never bought spot capacity. — unverified: your statement.
- **GT-13?** Internet egress from major cloud providers is billed at roughly $0.05–$0.09/GB. — unverified: no pricing page was opened. It feeds only a MEDIUM chain, so no read was attempted.

```text
?-marked: GT-4?, GT-5?, GT-6?, GT-7?, GT-8?, GT-9?, GT-10?, GT-11?, GT-12?, GT-13? (10 of 13)
Read-at-source: GT-1 — the Amdahl formula stated in-entry; GT-2 — the SI unit arithmetic in-entry; GT-3 — the restart-waste definition in-entry
```

**Phase 3 verification note:** GT-1 to GT-3 are definitions checked by derivation, with no external figure to open. GT-4? to GT-12? are your own statements with no cited source, so there is nothing to read. GT-13? feeds only MEDIUM chains, so no read was attempted.

## 4. Derivation Chains

### Conclusion C1: A spot design must keep its longest unsplit task off reclaimable capacity, or checkpoint it

GT-1 (serial work bound) + GT-3 (restart-from-zero waste)
→ splitting removes time only from the parallel part of a job
→ a reclaim wastes up to the full elapsed length of the interrupted task
→ the longest unsplit task is both the part splitting cannot shorten and the costliest one to lose
→ a spot design must run its longest unsplit task on non-reclaimable capacity or checkpoint it

**Confidence:** HIGH
**Weakest link:** Step 3 depends on correctly identifying the longest unsplit task. In your case that is the merge (C3), but that identification comes from GT-5?.

### Conclusion C2: Link rate, not instance count, bounds any design that moves the index across the boundary

GT-2 (≈2.2 h per TB at 1 Gbps) + GT-1 (serial work bound)
→ a transfer over one link is serial with respect to compute, so adding instances does not shorten it
→ link rate, not instance count, bounds the time of any design that moves the index across the on-prem/cloud boundary nightly

**Confidence:** HIGH
**Weakest link:** The chain is conditional on a nightly transfer existing at all (A5). It holds as stated, but applies only if that transfer happens.

### Conclusion C3: "Comfortably inside the window" is unproven and turns on the link and data location

GT-4? (8 h window) + GT-5? (7 h, last 2 h single-core) + GT-6? (4 TB) + C1 (serial bound) + C2 (link bound)
→ with 8 workers, best-case compute is ≈5 h ÷ 8 + 2 h ≈ 2.6 h *[Assumes: A2 — even split, matching throughput]* *[Assumes: A4 — merge no slower on a cloud core]*
→ even with unlimited workers, compute cannot fall below the 2 h merge, a 3.5× ceiling on today's 7 h
→ the best case leaves ≈5.4 h of the 8 h window for data movement and reclaim re-runs
→ at 1 Gbps a single 4 TB transfer takes ≈8.9 h, longer than the whole window *[Assumes: A5 — data crosses the boundary nightly]*
→ "comfortably inside the window" holds only with a link of roughly 10 Gbps or more, or data that never leaves the cloud

**Confidence:** MEDIUM — the chain consumes GT-4?, GT-5? and GT-6? plus assumptions A2, A4 and A5. Measuring the parallel speedup on one cloud instance, the merge time on a cloud core, the link rate, and where the data lives would raise it to HIGH. C1 and C2 are HIGH, so they impose no cap.
**Weakest link:** Step 1 (A2). If the current server already uses many cores, 8 instances beat it by less than 8×.

### Conclusion C4: The cost case is undecided and could exceed the lease

GT-6? (4 TB nightly) + GT-13? (egress ≈$0.05–$0.09/GB) + GT-8? ($600 unpriced) + GT-7? ($2,100 lease)
→ returning the index to on-prem serving every night moves ≈4 TB × 30 = 120 TB a month *[Assumes: A7 — search is served on-prem]*
→ at the unverified egress rate that is ≈$6,000–$10,800 a month
→ the cost bracket runs from about $600 (serving in the same cloud) to several times the $2,100 lease, so it straddles the decision threshold
→ the cost case stays undecided until serving location and egress terms are measured

**Confidence:** MEDIUM — the chain consumes GT-6?, GT-13?, GT-8? and GT-7?, plus A7. Confirming where search is served, reading the provider's egress price or interconnect contract, and pricing the compute would raise it to HIGH.
**Weakest link:** Step 2 (GT-13?). A private interconnect or a negotiated rate could shrink the egress term a lot.

### Conclusion C5: Committing to spot only, before renewal, trades a small unconfirmed saving for an unmeasured reliability risk

GT-9? (restart on reclaim, rate unknown) + GT-11? (a miss means a stale day) + GT-12? (no spot experience) + GT-7? (lease) + GT-8? ($600 estimate) + C1 (merge exposure) + C3 (≈5.4 h best-case slack) + C4 (cost undecided)
→ with no regional reclaim or capacity data, the chance that one night's reclaims exceed the slack has no measured upper bound
→ each miss costs a full business day of stale search, a loss no figure here prices
→ letting the lease lapse would remove the only rebuild path already proven to meet 06:00
→ spot-only before renewal trades a saving of at most ≈$1,500 a month, which C4 has not confirmed, for an unmeasured reliability risk

**Confidence:** MEDIUM — the chain consumes GT-9?, GT-11?, GT-12?, GT-7? and GT-8?, and is capped by C3 and C4 (both MEDIUM). Regional reclaim and capacity data from a pilot, and a priced cost of a stale day, would raise it to HIGH.
**Weakest link:** Step 1 — the risk is unmeasured, not shown to be large.

### Conclusion C6: Renew the lease and run spot as a shadow pilot

GT-7? (12-month renewal) + GT-10? (4 engineer-weeks) + C3 (time bound) + C4 (cost undecided) + C5 (reliability risk)
→ with weights locked before scoring, the totals are B renew and pilot = 77, C short extension and pilot = 76, D renew only = 60, A migrate before renewal = 33
→ the lead comes from miss-risk (weight 5) and reversibility (weight 4), where A scores lowest
→ B and C sit within 10% of each other, a near-tie under the sensitivity rule
→ the near-tie flips on whether the lessor offers a shorter term, which nobody has asked *[Assumes: A12 — the 12-month-or-lapse framing may not hold]*
→ recommend B: renew, and pilot spot during the lease with the server as fallback
→[2nd] the pilot yields measured reclaim rate, capacity misses, link rate and a real bill before the next renewal
→[3rd] the next renewal is decided on measurements rather than a $600 guess
→[2nd] renewing forgoes at most ≈$18,000 of the year's ≈$25,200 lease cost, the ceiling if the $600 figure held
→[2nd] a renewed lease removes deadline pressure, so the pilot can stall
→[3rd] a dated exit criterion, such as 60 consecutive shadow nights, keeps the pilot from drifting *[Assumes: A19 — 60 nights is enough to observe the reclaim rate]*

**Confidence:** MEDIUM — the chain consumes GT-7? and GT-10?, and is capped by C3, C4 and C5 (all MEDIUM). Raising those three to HIGH, and getting the lessor's answer on term length, would raise this chain.
**Weakest link:** Step 1. The scores are judgements, and B's lead over C is one point.

## 5. Abandoned Reasoning

### Dead End: "Eight workers make it about eight times faster"
**What was tried:** Dividing the 7 h rebuild by 8.
**Why abandoned:** It contradicts GT-1. The 2 h single-core merge does not split, so the ceiling is 3.5× (C3).
**What it ruled out:** Any time estimate that ignores the serial merge.

### Dead End: Comparing compute alone, $600 against $2,100
**What was tried:** Setting the lease against the compute-only estimate.
**Why abandoned:** The intermediate claim could not be established. The estimate leaves out transfer and egress, and with egress included the bracket straddles the lease (C4).
**What it ruled out:** Treating the move as obviously cheaper.

### Dead End: Estimating miss probability from typical spot reclaim rates
**What was tried:** Borrowing a general reclaim rate to price the risk of a missed night.
**Why abandoned:** No ground truth describes reclaim behaviour in your region, so this would be an analogy used as evidence (A20, discarded).
**What it ruled out:** Any numerical miss probability before a pilot measures one.

### Dead End: Deciding on engineer-time payback
**What was tried:** Setting 4 engineer-weeks against $1,500/month of savings.
**Why abandoned:** The four weeks are spent in both option A and option B (GT-10?), so they don't separate the options, and the saving itself is unconfirmed (C4).
**What it ruled out:** A payback figure as the deciding factor.

## 6. Conclusion

**Recommended approach:** Do not move the rebuild before the lease renews. Renew, and run the spot rebuild as a shadow pilot while the server keeps producing the index you serve (chain C6).

**What to do, in order:**
- Measure your link rate and where search is served first, because together they decide both the time case and the cost case (chain C3; chain C4).
- In any spot design, run the 2-hour single-core merge on on-demand capacity or checkpoint it, and never put it on a reclaimable worker (chain C1).
- Price the real bill from the pilot's invoices, egress included, instead of relying on the $600 estimate (chain C4).
- Set a dated exit criterion for the pilot, such as 60 consecutive shadow nights, so the renewed lease does not let it stall (chain C6).
- Ask the lessor now whether a shorter or month-to-month term exists, because if it does at a modest premium it is an equally defensible choice (chain C6).

**Key insight:** The case for splitting is about compute, but the terms that decide the move are ones splitting cannot touch. A 4 TB nightly transfer at 1 Gbps takes about 8.9 hours, longer than the whole window. And sending the index back to on-prem serving could cost several times the lease in egress (chain C2; chain C3; chain C4).

**Trade-offs acknowledged:** Renewing commits about $25,200 for the year and gives up at most about $18,000 in savings, which is the most you would lose if the $600 figure turned out to be right (chain C6).

**Confidence:** MEDIUM. The recommendation rests on unmeasured workload, link, egress and reclaim figures (chain C3; chain C4; chain C5; chain C6).

These inputs pull the rating down: GT-4? through GT-13?, and the MEDIUM chains C3, C4 and C5. Confidence would rise to HIGH with five measurements: the link rate, where search is served, a quoted egress price, a single-instance timing of both the parallel phase and the merge, and pilot data on reclaim rate and capacity.

---

The claude.ai Gmail, Google Calendar and Google Drive connectors need authorization in your claude.ai connector settings before they can be used. This analysis didn't need them.