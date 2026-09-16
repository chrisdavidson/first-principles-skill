No re-entry edge fired, and no step was skipped: the closure ledger, the self-audit scan and the Self-Audit Gate all ran, and I read both the output template and the rubric.

**Short answer:** No. Don't let the lease lapse on the strength of this plan. Renew the server and run a spot pilot alongside it. Move only once real nights, real bills and real reclaim counts pass the thresholds below. The case against moving now doesn't rest on showing spot fails. It rests on this: the three things that decide the move are unmeasured, and a wrong guess costs a full business day of stale search.

## Technique sweep (process output)

| Technique | Where applied | Result |
|---|---|---|
| Fishbone | Phase 2 | Six cause categories were checked for assumptions. Technology gave A1, A2, A15 and A16; Process gave A11 and A12; Resources gave A5, A10 and A18; Information gave A3 and A14; Environment gave A7; People gave A10. |
| Inversion | Phase 2 | "What would guarantee spot fails?" surfaced three things: data can't move within the window (A7), transfer charges swamp the bill (A6), and replacement capacity is unavailable (A4). |
| 5-Whys (reduce to primitives) | Phase 3 | "Splitting finishes comfortably" breaks down into parallel share, serial share, per-core speed, transfer and reclaims. Only the serial-step identity (GT-3) is verified. |
| Estimate | Phase 4 | Transfer time (C2, C5), money spent sending data out of the cloud (C6) and payback (C7) are rebuilt from unit figures with low and high bounds. |
| Theoretical limit | Phase 4 | With a 2 h serial step, no number of workers can make the 7 h rebuild more than 3.5× faster (Dead End 1). |
| Trade-off | Phase 4 | Weights were fixed before scoring: on-time reliability 5, cost confidence 4, reversibility 4, low engineering effort 2, headroom for growth 3. Totals: renew and pilot 73, renew unchanged 64, move and drop the lease 40 (C9). |
| Second-order | Phase 4 | C9 was extended with [2nd] and [3rd] effects. None contradicts a ground truth, so nothing went back to Phase 2. |
| Pre-mortem | Phase 5 | Imagined failure: "It's spring, the lease is gone, and search served yesterday's index on several days." The causes fall into three groups, each with a fix. No fallback: fixed by C9. Reclaim rates never measured: fixed by pilot criterion 1 (C4). Data transfer never priced: fixed by pilot criteria 2 and 3 (C5, C6). |

## §6→§4 closure ledger (process output)

```text
- "Renew the server lease on the shortest term offered and pilot spot in parallel" → chain C9 ✓
- "Run real nightly rebuilds on spot with the on-prem server as fallback, recording every reclaim" → chain C4 ✓
- "Measure transfer time on the real data path, or redesign so data stays in the cloud" → chain C5 ✓
- "Price the full bill from actual invoices, including storage and nightly data transfer" → chain C6 ✓
- "Splitting only shortens the part that already parallelizes; the serial merge and the data movement decide the move" → chains C1, C2 ✓
- "Keeping the server means paying lease plus pilot, and the status quo has only ~14% headroom" → chains C8, C7 ✓
- "Confidence: MEDIUM" → chains C3–C9 ✓
```

## Assumption Audit scan (process output)

| Chain | Step | Step Text (brief) | Assumption surfaced? | Added to Table? |
|---|---|---|---|---|
| C1 | 1 | Workers shrink only P/N | none | n/a |
| C1 | 2 | Speedup ceiling (P+S)/S | none | n/a |
| C1 | 3 | Serial step decides timing | none | n/a |
| C2 | 1 | 8.9 h at 1 Gbit/s, 53 min at 10 | none | n/a |
| C2 | 2 | Round trip 17.8 h at 1 Gbit/s | none | n/a |
| C2 | 3 | Needs ≥2.2 Gbit/s to fit 8 h | none | n/a |
| C3 | 1 | Shares take 37.5 min, total ~2 h 38 min | Eight outputs feed the merge with no extra combine step | yes (A16) |
| C3 | 2 | ~5 h 22 min unused | none | n/a |
| C3 | 3 | "Comfortably" holds with no reclaims | none (A1, A15 already present) | n/a |
| C4 | 1 | Split reclaim costs ≤37.5 min, ~8 absorbable | Replacement capacity available promptly | yes (A4) |
| C4 | 2 | Merge reclaim costs ≤2 h | same as A4 | n/a (marked, not duplicated) |
| C4 | 3 | Tolerance rests on unmeasured rate | none (A3 present) | n/a |
| C4 | 4 | Merge on non-reclaimable capacity | none | n/a |
| C4 | 5 | Split phase needs measured reclaim data | none | n/a |
| C5 | 1 | On-prem data means copies must fit in slack | none (A7 present) | n/a |
| C5 | 2 | Needs ~3.3 Gbit/s | none | n/a |
| C5 | 3 | Timing claim unproven | none | n/a |
| C6 | 1 | ~120 TB/month returned | 30 rebuilds per month | yes (A17) |
| C6 | 2 | $2,400–$10,800/month | none (A6 present) | n/a |
| C6 | 3 | Low end exceeds lease | none | n/a |
| C6 | 4 | $600 can't support the decision | none | n/a |
| C7 | 1 | $1,500/month, $18,000/year | none | n/a |
| C7 | 2 | Engineer cost consumes most of it | Loaded cost $10k–$20k | yes (A18) |
| C7 | 3 | First-year case marginal | none | n/a |
| C8 | 1 | ~14% headroom | none | n/a |
| C8 | 2 | Growth >14% breaks deadline | none (A14 present) | n/a |
| C8 | 3 | Renewing unchanged carries risk | none | n/a |
| C8 | 4 | Pilot has value if lease kept | none | n/a |
| C9 | 1 | Weighted totals 73 > 64 > 40 | none | n/a |
| C9 | 2 | Shorter renewal term lowers fallback cost | Lessor offers a term shorter than a year | yes (A19) |
| C9 | 3 | Recommend renew and pilot | none | n/a |
| C9 | 4 | [2nd] pay lease plus pilot during overlap | none | n/a |
| C9 | 5 | [3rd] remaining lease months become sunk cost | none | n/a |

## Self-audit scan (process output)

| Chain | Chain Head (brief) | Form conforming? | Rule applied | Dependency clean? |
|---|---|---|---|---|
| C1 | GT-3 (serial-step identity) | yes | n/a | yes |
| C2 | GT-10 (transfer arithmetic) | yes | n/a | yes |
| C3 | GT-1? + GT-2? + GT-4? + C1 | yes | n/a | yes |
| C4 | C3 + GT-5? + GT-6? | yes | n/a | yes |
| C5 | C2 + GT-11? + C3 | yes | n/a | yes |
| C6 | GT-7? + GT-8? + GT-11? + GT-12? | yes | n/a | yes |
| C7 | GT-7? + GT-8? + GT-9? | yes | n/a | yes |
| C8 | GT-1? + GT-13? | yes | n/a | yes |
| C9 | C4 + C5 + C6 + C7 + C8 | yes | n/a | yes |

| §6 Span (brief) | Construct | Claim under R11? | R11 clause applied | Chain cited |
|---|---|---|---|---|
| Recommended approach: renew, pilot in parallel | bold lead-in | yes | bold lead-in whose colon closes the bold span | C9 |
| Pilot exit criteria label | bold lead-in | no | section-intro label: colon-terminated span is the whole line, no citation | n/a |
| Run real nightly rebuilds… | list item | yes | list item over forty characters | C4 |
| Measure transfer time… | list item | yes | list item over forty characters | C5 |
| Price the full bill… | list item | yes | list item over forty characters | C6 |
| Key insight: split shortens only the parallel part | bold lead-in | yes | bold lead-in whose colon closes the bold span | C1, C2 |
| Trade-offs acknowledged: lease plus pilot; 14% headroom | bold lead-in | yes | bold lead-in whose colon closes the bold span | C8, C7 |
| Confidence: MEDIUM | bold lead-in | yes | bold lead-in whose colon closes the bold span | C3–C9 |
| MEDIUM explanation paragraph | prose | no | prose with neither a bold colon lead-in nor a list marker | n/a |

```text
Scan complete: 9 chain rows, one per section-4 chain block in order; 9 section-6 rows, one per construct in order — 7 claims under R11, 2 excluded. 0 chains malformed, 0 claims untraced.
```

## Self-Audit Gate (process output)

**Criterion 1: Identify Essence**
Quoted span: "Pass if the Conclusion states whether to let the lease lapse before cloud viability is shown"
Band: **Rigorous**
Justification: The Essence Statement names this specific decision and its irreversibility. Each success criterion is a pass/fail test that a reader can check against the Conclusion section.

**Criterion 2: Challenge Assumptions**
Quoted span: "| C4 | 1 | Split reclaim costs ≤37.5 min, ~8 absorbable | Replacement capacity available promptly | yes (A4) |"
Band: **Rigorous**
Justification: The audit covers every hop of all nine chains, and each assumption it surfaced (A4, A16, A17, A18, A19) is a table row. All rows use the four types, verdicts lead with a token and an em-dash, and unverified rows used in chains read "unverified — flagged".

**Criterion 3: Establish Ground Truths**
Quoted span: "enumerated GT-1?, GT-2?, GT-4?, GT-5?, GT-6?, GT-7?, GT-8?, GT-9?, GT-11?, GT-12?, GT-13?; list carries ? on exactly those eleven; unsuffixed GT-3 and GT-10 feed HIGH chains C1 and C2"
Band: **Sound**
Justification: The enumeration matches the list, and both unsuffixed ground truths feed HIGH chains. However, their read-location is a derivation written in this document, not a location inside an opened external source, which is one identifiable departure from the Rigorous form.

**Criterion 4: Reason Upward**
Quoted span: "| C4 | C3 + GT-5? + GT-6? | yes | n/a | yes |"
Band: **Rigorous**
Justification: All nine chain rows conform and are dependency-clean. Abandoned Reasoning records three dead ends with the full structure, no analogy is used as evidence, and the new assumptions carry `[Assumes: X]` marks.

**Criterion 5: Validate**
Quoted span: "**Confidence:** MEDIUM — every decision-bearing chain (C3–C9) consumes figures taken from the problem statement that this analysis could not check"
Band: **Hand-wavy**
Justification: Every chain names its weakest link and caveat. But the Recommended approach, the Trade-offs, the pilot criteria and the Confidence line each rest only on MEDIUM chains, with no exception claimed. That is the multiple-conclusion shortfall the rubric bands Hand-wavy. It is an honest limit of the inputs, and I report it as such rather than raising any rating.

**Criterion 6: Conclusion-to-Ground-Truth Traceability**
Quoted span: "| Key insight: split shortens only the parallel part | bold lead-in | yes | bold lead-in whose colon closes the bold span | C1, C2 |"
Band: **Rigorous**
Justification: All seven claims cite chains and none is untraced. The Key Insight (the serial merge and the data movement decide the move, and the split doesn't touch them) is a finding the proposal's own framing doesn't reach, not a restatement of the recommendation.

**Gate result:** No criterion is Absent and one is Hand-wavy (Criterion 5), so the gate is cleared and no re-scoring pass was run.

---

# First Principles Analysis: nightly index rebuild, on-prem lease vs. cloud spot instances

## 1. Problem Essence

**Core problem:** Should the team give up its only proven way to finish a 4 TB nightly rebuild by 06:00 (the leased server, which renews for a year next quarter) before spot capacity has shown it can meet that deadline at lower total cost?

**Success criteria:**
- Pass if the Conclusion states whether to let the lease lapse before cloud viability is shown.
- Pass if the Conclusion names the measurements that would justify cutting over, each tied to a chain.
- Pass if the Conclusion states how much of the proposal's timing and cost claims survive once the serial merge, data movement and reclaims are counted.

## 2. Assumptions Table

| # | Assumption | Type | Treatment | Verdict | Verification |
|---|---|---|---|---|---|
| A1 | The 5 h pre-merge work splits evenly across 8 workers with negligible coordination overhead | untested belief | Verify, or flag as unverified | Challenge — no split build has ever been run | unverified — flagged (GT-4?) |
| A2 | The merge stays a 2 h single-core step in the cloud | untested belief | Verify, or flag as unverified | Challenge — cloud per-core speed differs from the server's | unverified — flagged (GT-2?) |
| A3 | The regional spot reclaim rate is low enough to finish on time | untested belief | Verify, or flag as unverified | Challenge — the prompt says no data exists | unverified — flagged (GT-5?) |
| A4 | Replacement spot capacity is available within minutes of a reclaim (surfaced at C4) | untested belief | Verify, or flag as unverified | Challenge — capacity availability at 22:00 is unmeasured | unverified — flagged |
| A5 | The cloud bill will be about $600/month | untested belief | Verify, or flag as unverified | Challenge — the prompt says nobody has priced it | unverified — flagged (GT-8?) |
| A6 | The $600 figure covers data transfer and storage (from inversion) | untested belief | Verify, or flag as unverified | Challenge — sending 4 TB out of the cloud nightly could dwarf the compute cost | unverified — flagged (GT-12?) |
| A7 | Where the data lives, and the link speed, allow nightly movement within the window (from inversion) | untested belief | Verify, or flag as unverified | Challenge — the prompt names neither | unverified — flagged (GT-11?) |
| A8 | The lease is $2,100/month for 12 months, renewing next quarter | current constraint | Record expiry conditions | Accept — expires at the renewal date; a shorter term or exit clause would change it | unverified — flagged (GT-7?); contract not seen |
| A9 | Missing 06:00 serves yesterday's index for the whole business day | current constraint | Record expiry conditions | Accept — holds until the serving layer can swap in a new index mid-day | unverified — flagged (GT-6?) |
| A10 | One engineer for four weeks is enough | untested belief | Verify, or flag as unverified | Challenge — no prior spot work to calibrate against | unverified — flagged (GT-9?) |
| A11 | Each night must be a full rebuild from scratch | convention | Challenge before use | Challenge — nothing in the prompt rules out incremental builds; appears only as an alternative in C2 | Not verified; not load-bearing |
| A12 | Splitting across machines is the way to speed up the rebuild | convention | Challenge before use | Discard — the serial merge caps any split (C1); parallelizing the merge is an untried alternative | GT-3 derivation |
| A13 | A serial step's duration bounds wall time regardless of worker count | physical law | Accept as a ground-truth candidate | Accept — mathematical identity | GT-3 |
| A14 | Index size and runtime stay flat through the lease year | untested belief | Verify, or flag as unverified | Challenge — no growth data given | unverified — flagged (GT-13?) |
| A15 | Spot workers are at least as fast per share as the current server | untested belief | Verify, or flag as unverified | Challenge — instance type not chosen | unverified — flagged (GT-4?) |
| A16 | Eight worker outputs feed the merge with no extra combine step (surfaced at C3) | untested belief | Verify, or flag as unverified | Challenge — the pipeline's split points are unknown | unverified — flagged |
| A17 | 30 rebuilds per month (surfaced at C6) | current constraint | Record expiry conditions | Accept — holds while the rebuild runs every night; would drop if some nights were skipped | Prompt: "every night" |
| A18 | Loaded engineer cost is $10k–$20k per four weeks (surfaced at C7) | untested belief | Verify, or flag as unverified | Challenge — no salary data given | unverified — flagged |
| A19 | The lessor offers a renewal term shorter than a year (surfaced at C9) | untested belief | Verify, or flag as unverified | Challenge — contract terms not seen | unverified — flagged |

## 3. Ground Truths

- **GT-1?** The window is 22:00→06:00 = 8 h. Today's run takes 7 h, leaving 1 h of slack. — unverified: user-stated; no runtime logs seen.
- **GT-2?** The last 2 h of the run is a single-core merge, so the pre-merge work is 5 h. — unverified: user-stated.
- **GT-3** If a job has P hours of parallelizable work and S hours of serial work, then with N workers the wall time is P/N + S, which is never less than S. The speedup is therefore capped at (P+S)/S. — source: the definition of serial execution (Amdahl's identity); read-at-source: the derivation is written in this entry and can be checked by inspection.
- **GT-4?** The pre-merge work splits evenly across 8 workers with negligible overhead, on workers at least as fast as the server. — unverified: never tried.
- **GT-5?** A reclaimed worker restarts its share from the beginning. The regional reclaim rate and replacement-capacity availability are unknown. — unverified: user-stated; no data exists.
- **GT-6?** A missed 06:00 means search serves yesterday's index all business day. — unverified: user-stated.
- **GT-7?** The lease is $2,100/month and renews for 12 months next quarter. — unverified: user-stated; contract not seen.
- **GT-8?** The cloud bill is expected to be about $600/month but has not been priced. — unverified: the user states nobody priced it.
- **GT-9?** The move needs one engineer for four weeks, and the team has never bought spot capacity. — unverified: user-stated estimate.
- **GT-10** 4 TB = 3.2×10¹³ bits. At 1 Gbit/s that takes 32,000 s ≈ 8.9 h; at 10 Gbit/s, 3,200 s ≈ 53 min. — source: unit definitions (decimal TB, 8 bits per byte); read-at-source: the arithmetic is written in this entry.
- **GT-11?** Where the source data lives, where the index is served from, and the link speed between them. — unverified: the prompt does not say.
- **GT-12?** Cloud providers charge roughly $0.02–$0.09 per GB for data sent out of the cloud. — unverified: no pricing page was opened by this analysis.
- **GT-13?** Index size and runtime will not grow over the lease year. — unverified: no growth data.

```text
?-marked: GT-1, GT-2, GT-4, GT-5, GT-6, GT-7, GT-8, GT-9, GT-11, GT-12, GT-13 (11 of 13)
Read-at-source: GT-3 — derivation inline in the entry (feeds HIGH chain C1); GT-10 — arithmetic inline in the entry (feeds HIGH chain C2)
```

No Phase 3 source reads were attempted. The two HIGH-feeding ground truths are derivations written into their own entries, and every other ground truth feeds only MEDIUM chains.

## 4. Derivation Chains

### Conclusion C1: A split plan's timing is decided by its serial step, not by its worker count

GT-3 (serial-step identity)
→ adding workers shrinks only the parallel term P/N
→ wall time therefore never drops below the serial duration S
→ the speedup ceiling for any number of workers is (P+S)/S
→ a split plan's timing is governed by its serial step, which the split leaves unchanged

**Confidence:** HIGH. The chain rests only on a mathematical identity. Weakest link: none beyond the identity itself.

### Conclusion C2: A nightly 4 TB round trip needs at least ~2.2 Gbit/s sustained just to fit in eight hours

GT-10 (4 TB transfer arithmetic)
→ one full 4 TB copy takes about 8.9 h at 1 Gbit/s and about 53 min at 10 Gbit/s
→ copying 4 TB in and 4 TB out takes about 17.8 h at 1 Gbit/s
→ fitting both copies into eight hours, before any compute, needs at least ~2.2 Gbit/s sustained, or an incremental design

**Confidence:** HIGH. The chain is unit arithmetic only. Weakest link: the "sustained" rate. Real throughput runs below the rated link speed, which only makes the requirement stricter.

### Conclusion C3: On compute alone, with no reclaims, the lead's "comfortably inside the window" holds

GT-1? (8 h window) + GT-2? (5 h parallel, 2 h serial merge) + GT-4? (even split, equal speed) + C1 (serial step governs)
→ eight even shares of the 5 h pre-merge work take about 37.5 min each, so compute ends after about 2 h 38 min *[Assumes: A16 — eight outputs feed the merge with no extra combine step]*
→ that leaves about 5 h 22 min of the 8 h window unused
→ with no reclaims and no data movement, the proposal's timing claim holds

**Confidence:** MEDIUM. Weakest link: GT-4? (even split at equal per-core speed). Timing a real split build on the chosen instance type would raise this to HIGH.

### Conclusion C4: The merge must not run on spot, and the split phase can't be trusted until reclaims are measured

C3 (about 5 h 22 min slack) + GT-5? (restart from scratch, unknown rate) + GT-6? (miss costs a business day)
→ a reclaim during the split phase costs at most one 37.5 min share, so about eight such restarts fit in the slack *[Assumes: A4 — replacement capacity arrives within minutes]*
→ a reclaim during the 2 h merge costs up to 2 h, so two merge reclaims use about three quarters of the slack *[Assumes: A4]*
→ whether the slack suffices depends on a reclaim rate nobody has measured, while a miss costs a full business day
→ the merge step belongs on capacity that can't be reclaimed (on-demand or on-prem)
→ the split phase needs measured reclaim counts from real nights before the deadline can rest on it

**Confidence:** MEDIUM. Weakest link: GT-5? (reclaim rate and replacement capacity). A record of reclaims and replacement delays over real 22:00–06:00 runs in the target region would raise this to HIGH.

### Conclusion C5: The timing claim is unproven until the data path is known

C2 (round-trip bound) + GT-11? (data location and link unknown) + C3 (about 5 h 22 min slack)
→ if the 4 TB source and the served index both stay on-premises, both copies must fit inside the unused 5 h 22 min
→ that needs about 3.3 Gbit/s sustained (17.8 h of 1 Gbit/s transfer squeezed into 5.37 h)
→ the proposal's "comfortably inside the window" is unproven until data location, link speed or an incremental-transfer design is established

**Confidence:** MEDIUM. Weakest link: GT-11? (where data lives, and the link speed). If the data already lives in the cloud, this concern disappears. Measuring one full transfer on the real path would raise this to HIGH.

### Conclusion C6: The $600 figure cannot support the decision until data transfer and storage are priced

GT-7? ($2,100 lease) + GT-8? ($600 unpriced) + GT-11? (serving location unknown) + GT-12? ($0.02–$0.09/GB outbound)
→ if the finished 4 TB index returns on-premises every night, about 120 TB leaves the cloud each month *[Assumes: A17 — 30 rebuilds per month]*
→ at $0.02–$0.09/GB, that outbound transfer alone costs about $2,400–$10,800 a month
→ even the low end exceeds the $2,100 lease the move is meant to replace
→ the $600 estimate cannot support the decision until the bill is priced with transfer and storage included

**Confidence:** MEDIUM. Weakest links: GT-12? (the per-GB price) and GT-11? (whether the index comes back on-prem at all). The provider's current price sheet for your region and path, plus confirming where search is served, would raise this to HIGH.

### Conclusion C7: Even if the $600 figure holds, the first-year financial case is marginal

GT-7? ($2,100 lease) + GT-8? ($600 estimate) + GT-9? (four engineer-weeks)
→ taking $600 at face value, the move saves $1,500 a month, or $18,000 over the lease year
→ four engineer-weeks at a loaded cost of about $10,000–$20,000 uses up most or all of that first-year saving *[Assumes: A18 — loaded cost $10k–$20k]*
→ even if the bill estimate is right, the first-year financial case is marginal

**Confidence:** MEDIUM. Weakest link: GT-8? (the bill), then A18. A priced bill and your actual loaded engineering cost would raise this to HIGH.

### Conclusion C8: Keeping the server unchanged is not risk-free either

GT-1? (7 h run in 8 h window) + GT-13? (no growth assumed)
→ a 7 h run in an 8 h window has about 14% headroom
→ runtime growth beyond about 14% breaks the deadline on the current server, with no platform change involved
→ renewing unchanged also carries deadline risk
→ a pilot is worth running even if the lease is kept

**Confidence:** MEDIUM. Weakest link: GT-13? (growth). The rebuild-time trend over recent months would raise this to HIGH.

### Conclusion C9: Renew the server and pilot spot in parallel; don't move before renewal

C4 (reclaim risk unmeasured) + C5 (transfer unproven) + C6 (cost unpriced) + C7 (thin payback) + C8 (status-quo risk)
→ weighted totals: renew-and-pilot 73 > renew-unchanged 64 > move-and-drop-lease 40, driven by on-time reliability × 5 and reversibility × 4
→ a shorter renewal term, if offered, lowers the cost of keeping the fallback *[Assumes: A19 — lessor offers a sub-year term]*
→ recommend renewing the server lease and piloting spot in parallel, not moving before renewal
→[2nd] the business pays the lease plus pilot spend during the overlap
→[3rd] if the pilot succeeds mid-term, the remaining lease months are a sunk cost to weigh against the saving

**Confidence:** MEDIUM. Weakest link: the input chains' MEDIUM ratings (GT-5?, GT-8?, GT-11?, GT-12?). The recommendation holds up against those unknowns: each one that resolves badly strengthens it, and each one that resolves well only postpones the move. It would reach HIGH once the pilot measurements exist. No second-order effect contradicts a ground truth.

## 5. Abandoned Reasoning

### Dead End: Use more spot workers to buy more margin

**What was tried:** Scaling the split beyond eight workers to widen the timing margin against reclaims.

**Why abandoned:** C1 caps the speedup at (5+2)/2 = 3.5×, which is a best case of about 2 h no matter how many workers. Eight workers already reach 7/2.625 ≈ 2.67×, and extra workers leave the 2 h merge and its exposure to reclaims unchanged.

**What it ruled out:** Worker count as the lever. The remaining levers are parallelizing the merge itself (untried; A12) or moving the merge onto capacity that can't be reclaimed (C4).

### Dead End: Decide by comparing $600 against $2,100

**What was tried:** Treating the move as a $1,500/month saving and deciding on that basis.

**Why abandoned:** GT-8? is an unpriced guess, and C6 shows that data transfer alone could exceed the lease, so the comparison has no verified term on the cloud side.

**What it ruled out:** Any decision based on the headline estimate before a priced, all-in bill exists.

### Dead End: One large on-demand cloud instance as a middle path

**What was tried:** Replacing the server with one on-demand cloud machine to avoid reclaims.

**Why abandoned:** No step could be established that makes it better. It keeps the full 7 h runtime with only 1 h of headroom (C8), keeps the whole data-movement problem (C5, C6), and no ground truth prices it below the lease.

**What it ruled out:** A lift-and-shift of the current setup as a fix for either deadline risk or cost.

## 6. Conclusion

**Recommended approach:** Do not move the nightly rebuild before the lease renews. Renew the server, on the shortest term the lessor offers, and pilot spot instances in parallel with the server kept as the fallback; run the merge step on capacity that can't be reclaimed (chain C9).

**Pilot exit criteria — cut over only when all three hold:**

- Run real nightly rebuilds on spot with the on-prem server as fallback, and record every reclaim and replacement delay until the counts show comfortable slack (chain C4).
- Measure transfer time on the real data path, or redesign so data stays in the cloud, and confirm it fits the unused window (chain C5).
- Price the full monthly bill from actual invoices, including storage and nightly data transfer, and confirm it beats the lease after engineering cost (chain C6).

**Key insight:** The lead's speed claim is true but beside the point. Splitting only shortens the part of the rebuild that already parallelizes. What decides whether the move works is the 2 h serial merge (still exposed to reclaims) and moving 4 TB each night (which may cost more than the lease and need a link of several Gbit/s), and splitting changes neither (chains C1, C2).

**Trade-offs acknowledged:** Keeping the server means paying the lease plus pilot spend for a while, and even at the claimed $600 the first-year saving is roughly eaten by the engineering time. Meanwhile the current server has only about 14% headroom, so the pilot is worth running even if the lease is kept (chains C8, C7).

**Confidence:** MEDIUM — every decision-bearing chain (C3–C9) consumes figures taken from the problem statement that this analysis could not check (chains C3, C4, C5, C6, C7, C8, C9).

Where the downgrade comes from, and what would raise it to HIGH:
- **GT-5? (reclaim rate):** real reclaim counts from pilot nights.
- **GT-8? and GT-12? (the bill and outbound transfer price):** a priced, all-in bill.
- **GT-11? (data location and link speed):** knowing where the data and the served index live, and the link speed.
- **GT-4? (split scaling and per-core speed):** one timed split build.

Only C1 and C2 are HIGH, and they are pure arithmetic. None of the decision-bearing conclusions reaches HIGH on current information, which is itself the main reason not to give up the fallback now.