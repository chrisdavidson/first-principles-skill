**Short answer: no, not as a committed move before the renewal.** The plan might meet the deadline, but its cost hasn't been priced and the data-transfer question hasn't been checked, and either one could sink it. Keep running on the leased server and run a short pilot with pass/fail checks. Switch only if every check passes before the renewal date; if one fails, renew. The full analysis follows. The audit tables and the checks against the methodology's review criteria come first because the method requires them before the conclusions; the analysis itself is under **Analysis** at the bottom.

No repeated steps, skipped steps or failed file reads occurred.

---

## §6→§4 closure ledger (process output)

- "Do not commit to moving the rebuild before the lease renews…" → chain C7 ✓
- "Worker restarts are not the real timing risk…" → chain C5 ✓
- "…a 1 Gbps link alone needs about 9 hours per direction…" → chain C3 ✓
- "The 600 dollar figure is unpriced…" → chain C6 ✓
- "…four engineer-weeks takes roughly 7 to 17 months to pay back…" → chain C6 ✓
- "Renewing is not risk-free either…" → chain C8 ✓
- Gate 1 "A priced bill covering compute, storage and data transfer…" → chain C6 ✓
- Gate 2 "Measured link throughput, or a data layout…" → chain C3 ✓
- Gate 3 "Two to three weeks of shadow rebuilds on spot…" → chain C5 ✓
- Gate 4 "An on-demand fallback for the merge instance…" → chain C5 ✓
- "The pilot takes engineering time before you have any savings…" → chain C7 ✓
- "MEDIUM — the arithmetic chains C1 and C4 are HIGH…" → chain C6 ✓

## Assumption Audit scan (process output)

| Chain | Step | Step Text (brief) | Assumption surfaced? | Added to Table? |
|---|---|---|---|---|
| C1 | 1 | extra workers shrink only the parallel term | none | n/a |
| C1 | 2 | no worker count goes below the serial merge time | none | n/a |
| C2 | 1 | 5 h can run in parallel; 2 h is a serial floor | none | n/a |
| C2 | 2 | 8 workers bring 5 h down to about 0.6 h | linear scaling (A17); cloud cores as fast as on-prem (A8) | yes (A17, A8) |
| C2 | 3 | compute takes about 2.6 h, leaving about 5.4 h | none | n/a |
| C3 | 1 | 4 TB takes about 8.9 h at 1 Gbps, 0.9 h at 10 Gbps | none | n/a |
| C3 | 2 | at 1 Gbps one crossing takes longer than the window | data crosses nightly (A9); link speed (A10) | yes (A9, A10) |
| C3 | 3 | only fits with about 10 Gbps or no nightly crossing | none | n/a |
| C4 | 1 | P(at least one of 8 reclaimed) ≥ p | none (independence not needed; A14 discarded) | n/a |
| C4 | 2 | restart time must be budgeted on more nights | none | n/a |
| C5 | 1 | a reclaimed worker loses at most about 0.6 h | equal shares (covered by A17) | n/a (A17 exists) |
| C5 | 2 | a reclaimed merge instance loses up to 2 h | none | n/a |
| C5 | 3 | margin absorbs several worker restarts or two merge restarts | none | n/a |
| C5 | 4 | nights with no capacity cannot be absorbed | spot capacity available (A11) | yes (A11) |
| C5 | 5 | risk sits in merge, capacity, transfer | none | n/a |
| C6 | 1 | claimed saving is $1,500/month | none | n/a |
| C6 | 2 | payback takes 7 to 17 months | four weeks is enough (A13); engineer cost (A12) | yes (A13, A12) |
| C6 | 3 | little or no net saving in year one | none | n/a |
| C6 | 4 | egress would be about $6k to $11k/month if data crosses | egress price (A15) | yes (A15) |
| C6 | 5 | $600 is unsupported | none | n/a |
| C7 | 1 | weighted totals 66 > 60 > 33 | none | n/a |
| C7 | 2 | effort weight 5 ties the pilot with renewal | none | n/a |
| C7 | 3 | pilot's lead depends on falling back to renewal | lease still renewable on the same terms (A5) | yes (A5) |
| C7 | 4 | recommend a gated pilot | none | n/a |
| C7 | 5 | [2nd] stale-index exposure does not rise during the pilot | none | n/a |
| C7 | 6 | [2nd] estimates replaced by measurements | none | n/a |
| C7 | 7 | [3rd] renewal decided on a measured bill | none | n/a |
| C7 | 8 | [2nd] engineering time spent before any saving | none | n/a |
| C7 | 9 | [3rd] an overrun locks in the lease by default | none | n/a |
| C8 | 1 | 1 h of slack; about 14% growth breaks the window | rebuild time grows with the index (A16) | yes (A16) |
| C8 | 2 | renewing is not risk-free | none | n/a |
| C8 | 3 | the merge is the term no worker count removes | none | n/a |
| C8 | 4 | shortening the merge helps on either platform | none | n/a |

## Self-audit scan (process output)

| Chain | Chain Head (brief) | Form conforming? | Rule applied | Dependency clean? |
|---|---|---|---|---|
| C1 | GT-8 (serial-floor identity) | yes | n/a | yes |
| C2 | C1 + GT-1? + GT-2? | yes | n/a | yes |
| C3 | GT-9 + GT-1? + GT-2? | yes | n/a | yes |
| C4 | GT-10 (union ≥ member) | yes | n/a | yes |
| C5 | C2 + C3 + C4 + GT-5? | yes | n/a | yes |
| C6 | GT-3? + GT-4? + GT-6? + GT-12? + GT-11? + C3 | yes | n/a | yes |
| C7 | C2 + C3 + C5 + C6 + GT-7? | yes | n/a | yes |
| C8 | GT-1? + GT-2? + C1 | yes | n/a | yes |

| §6 Span (brief) | Construct | Claim under R11? | R11 clause applied | Chain cited |
|---|---|---|---|---|
| Recommended approach: do not commit… | bold lead-in | yes | prescribed lead-in, always a claim | C7 |
| Key insight: worker restarts are not… | bold lead-in | yes | prescribed lead-in, always a claim | C5 |
| Transfer gate: 1 Gbps needs about 9 h… | bold lead-in | yes | bold lead-in whose colon closes the bold span | C3 |
| Cost gate: $600 is unpriced… | bold lead-in | yes | bold lead-in whose colon closes the bold span | C6 |
| Payback: 7 to 17 months… | bold lead-in | yes | bold lead-in whose colon closes the bold span | C6 |
| Baseline risk: one hour of slack… | bold lead-in | yes | bold lead-in whose colon closes the bold span | C8 |
| Pilot checks label | bold lead-in | no | label only: the bold text is the whole line and cites no chain | n/a |
| Check 1: priced bill… | list item | yes | list item over forty characters | C6 |
| Check 2: link throughput… | list item | yes | list item over forty characters | C3 |
| Check 3: shadow rebuilds… | list item | yes | list item over forty characters | C5 |
| Check 4: on-demand merge fallback… | list item | yes | list item over forty characters | C5 |
| Trade-offs acknowledged: engineering time… | bold lead-in | yes | prescribed lead-in, always a claim | C7 |
| Confidence: MEDIUM… | bold lead-in | yes | bold lead-in whose colon closes the bold span | C6 |

```text
Scan complete: 8 chain rows, one per section-4 chain block in order; 13 section-6 rows, one per construct in order — 12 claims under R11, 1 excluded. 0 chains malformed, 0 claims untraced.
```

## Self-Audit Gate verdicts (process output)

**Criterion 1: Identify Essence**
Quoted span: "Is it worth giving up a known 2,100 dollar-a-month lease before its renewal date for a spot-instance rebuild whose deadline reliability, transfer time and total cost have not been measured?"
Band: **Rigorous**
Justification: One sentence names this specific decision rather than the triggering proposal. Each success criterion is a test that can be checked against section 6.

**Criterion 2: Challenge Assumptions**
Quoted span: "| C3 | 2 | at 1 Gbps one crossing takes longer than the window | data crosses nightly (A9); link speed (A10) | yes (A9, A10) |"
Band: **Rigorous**
Justification: Every row uses one of the four types and the matching treatment, and each verdict gives its reason after an em dash. Several rows are challenged (A1–A3, A7) and one is discarded (A14). The audit covers all 33 chain steps, and each assumption it surfaced is in the table and flagged.

**Criterion 3: Establish Ground Truths**
Quoted span: "enumerated GT-1? through GT-7?, GT-11?, GT-12?; the list carries `?` on exactly those nine. GT-9 is unsuffixed and feeds only the MEDIUM chain C3."
Band: **Sound**
Justification: The enumeration matches the list, and the read locations for GT-8 and GT-10 are named. One unsuffixed ground truth with a reachable source (GT-9) feeds only a MEDIUM chain, which bands this Sound.

**Criterion 4: Reason Upward**
Quoted span: "| C7 | C2 + C3 + C5 + C6 + GT-7? | yes | n/a | yes |"
Band: **Rigorous**
Justification: All eight chains have well-formed headers and clean dependencies. Section 5 records three dead ends with specific reasons, including one rejected analogy, and each assumption a step introduces is marked `[Assumes:]`.

**Criterion 5: Validate**
Quoted span: "**Confidence:** MEDIUM — the arithmetic chains C1 and C4 are HIGH, but every applied chain depends on figures from your description"
Band: **Hand-wavy**
Justification: Each chain names its weakest link and gives a MEDIUM rating with the verification that would raise it, but several section-6 claims rest only on MEDIUM chains. No exception is claimed. This is the one Hand-wavy score the gate allows; the gap remains open and is caveated, because your own figures can't be checked against a source.

**Criterion 6: Conclusion-to-Ground-Truth Traceability**
Quoted span: "Scan complete: … 12 claims under R11, 1 excluded. 0 chains malformed, 0 claims untraced."
Band: **Rigorous**
Justification: Every claim cites a chain. The key insight is non-obvious (restarts are not the main timing risk) and does not restate the recommendation.

The gate passes: nothing scored Absent, and one criterion scored Hand-wavy. The Criterion 5 gap remains open and is covered by the MEDIUM confidence rating.

---

# Analysis

## 1. Problem Essence

**Core problem:** Is it worth giving up a known 2,100 dollar-a-month lease before its renewal date for a spot-instance rebuild whose deadline reliability, transfer time and total cost have not been measured?

**Success criteria:**
- The Conclusion states whether to move before renewal, and under what conditions.
- The Conclusion says whether the spot design finishes before 06:00, with the margin stated in hours.
- The Conclusion says whether the $600/month figure holds, and names the cost items it leaves out.
- The Conclusion lists pass/fail checks that turn the unknowns into measurements before anything is committed.

## 2. Assumptions Table

| ID | Assumption | Type | Treatment | Verdict | Verification |
|---|---|---|---|---|---|
| A1 | Splitting the work across 8 workers finishes it comfortably inside the window | untested belief | Verify, or flag as unverified | Challenge — holds for compute alone at best (C2); the serial merge (C1) and nightly transfer (C3) can each break it | Shadow rebuilds on spot; unverified — flagged |
| A2 | The cloud bill is about $600/month | untested belief | Verify, or flag as unverified | Challenge — explicitly unpriced; leaves out storage and data transfer (C6) | A priced bill from the provider's calculator for compute + storage + egress; unverified — flagged |
| A3 | Spot reclaims are rare enough to tolerate | untested belief | Verify, or flag as unverified | Challenge — no regional data; eight instances raise exposure (C4) | Reclaim log from 2–3 weeks of shadow runs |
| A4 | The merge step stays single-core | current constraint | Record expiry conditions | Accept — expires if the merge is re-engineered to run in parallel or in stages | Stated in your description |
| A5 | The lease can still be renewed on the stated terms up to the renewal date | current constraint | Record expiry conditions | Accept — expires on the renewal date; whether a shorter term is available is untested | Ask the lessor; unverified — flagged |
| A6 | The deadline window is 22:00–06:00 | current constraint | Record expiry conditions | Accept — expires if business hours or the index-swap process change | Stated in your description |
| A7 | A missed deadline means serving yesterday's index for the whole day | convention | Challenge before use | Challenge — true only if the index can swap solely at 06:00; if a late swap were possible, a miss would cost hours, not a day | Check whether the serving layer can swap in the index during the day |
| A8 | Cloud cores run the rebuild and the merge at least as fast as the on-prem server | untested belief | Verify, or flag as unverified | Challenge — instance types vary widely | Time one shard and one merge on the target instance type; unverified — flagged |
| A9 | The source data or the finished index crosses between your site and the cloud every night | untested belief | Verify, or flag as unverified | Challenge — your description doesn't say where the source data or the search servers live | Map the data flow; unverified — flagged |
| A10 | The on-prem↔cloud link runs at about 1–10 Gbps | untested belief | Verify, or flag as unverified | Challenge — not stated | Measure sustained throughput; unverified — flagged |
| A11 | Spot capacity for all instances is available every night | untested belief | Verify, or flag as unverified | Challenge — you have never bought spot capacity | Shadow-run log of any nights without capacity; unverified — flagged |
| A12 | Four engineer-weeks costs about $10k–25k fully loaded | untested belief | Verify, or flag as unverified | Accept — used only as a range | Payroll figure; unverified — flagged |
| A13 | Four weeks is enough for the migration | untested belief | Verify, or flag as unverified | Challenge — a first spot build tends to include unplanned work | Pilot burn-down; unverified — flagged |
| A14 | Reclaims on different instances are independent | untested belief | Verify, or flag as unverified | Discard — C4 was reworded so it holds under any correlation; nothing depends on this now | n/a |
| A15 | Internet egress costs about $0.05–0.09 per GB | untested belief | Verify, or flag as unverified | Challenge — background knowledge; no price list was opened | Provider price list for your region and tier; unverified — flagged |
| A16 | Rebuild time grows with index size | untested belief | Verify, or flag as unverified | Accept — typical of this kind of rebuild, but not measured here | Rebuild time vs. index size from past runs; unverified — flagged |
| A17 | The parallel part splits into 8 equal shares that scale linearly | untested belief | Verify, or flag as unverified | Challenge — C2 is a best case; uneven shards lengthen it | Shadow-run timings; unverified — flagged |
| A18 | Wall-clock time = serial time + parallel time ÷ N | physical law | Accept as ground-truth candidate | Accept — follows from the definition (Amdahl) | GT-8 |
| A19 | The chance that any one of several events happens is at least the chance of each | physical law | Accept as ground-truth candidate | Accept — a basic rule of probability | GT-10 |
| A20 | Transfer time = size ÷ throughput | physical law | Accept as ground-truth candidate | Accept — follows from the definition of bit rate | GT-9 |

## 3. Ground Truths

- **GT-1?** The window runs 22:00–06:00, which is 8 hours. Unverified: this comes from your description, which cites no source.
- **GT-2?** Rebuilding the 4 TB index takes 7 h, and its last 2 h is a merge on a single core. Unverified: from your description.
- **GT-3?** The lease renews next quarter at $2,100/month for 12 months. Unverified: from your description.
- **GT-4?** The cloud bill is expected to be about $600/month, and nobody has priced it. Unverified: from your description, which itself says the figure is unpriced.
- **GT-5?** A reclaimed worker restarts its share from the beginning, and reclaim frequency in your region has not been measured. Unverified: from your description.
- **GT-6?** The migration needs one engineer for four weeks. Unverified: this is your estimate.
- **GT-7?** Missing 06:00 means serving yesterday's index for the whole business day. Unverified: from your description.
- **GT-8** For S serial hours and P parallel hours split across N workers, T(N) = S + P/N ≥ S. Source: the definition of wall-clock time for work with a fixed serial part (Amdahl's law). Read at source: derived in full in this entry.
- **GT-9** Transfer time = bytes × 8 ÷ link rate in bits per second. Source: the definition of bit rate. Read at source: derived in full in this entry.
- **GT-10** P(A₁ ∪ … ∪ Aₙ) ≥ P(Aᵢ) for every i. Source: the monotonicity rule of probability. Read at source: stated in full in this entry.
- **GT-11?** Major cloud providers charge about $0.05–0.09 per GB for internet egress. Unverified: from background knowledge; no price list was opened.
- **GT-12?** Four fully loaded engineer-weeks cost about $10k–25k. Unverified: an assumed range with no payroll data behind it.

```text
?-marked: GT-1, GT-2, GT-3, GT-4, GT-5, GT-6, GT-7, GT-11, GT-12 (9 of 12)
Read-at-source: GT-8 — definition derived in its entry (feeds HIGH chain C1); GT-10 — axiom stated in its entry (feeds HIGH chain C4)
```

**Phase 3 verification record:** No source reads were attempted. GT-8, GT-9 and GT-10 are definitions stated in full above. GT-11? and GT-12? feed only the MEDIUM chain C6, so they did not qualify for a read. GT-1? through GT-7? come from your description, which names no source. No failure records were written.

## 4. Derivation Chains

### Conclusion C1: No number of workers can bring the rebuild below the time of its serial merge

GT-8 (serial-floor identity)
→ adding workers divides only the parallel term P and leaves the serial term S unchanged
→ no number of workers can bring wall-clock time below the serial merge time

**Confidence:** HIGH. This follows from the definition. Weakest link: it applies only as long as the merge can't be split (A4).

### Conclusion C2: On compute alone, eight spot workers finish in about 2.6 hours

C1 (serial floor) + GT-1? (8-hour window) + GT-2? (7 h total, 2 h single-core merge)
→ the parallelizable part is 5 hours and the serial floor is 2 hours
→ eight workers cut the parallel part to about 0.6 hours *[Assumes: A17 — linear scaling]* *[Assumes: A8 — cloud core speed parity]*
→ compute finishes in about 2.6 hours, leaving about 5.4 hours of the 8-hour window as margin

**Confidence:** MEDIUM. The inputs GT-1? and GT-2? come from your description, and A8 and A17 are unmeasured. Weakest link: the speed-parity assumption in step 2. A timed shadow run on the target instance type would raise this to HIGH.

### Conclusion C3: Nightly data transfer can break the plan on its own

GT-9 (transfer-time identity) + GT-1? (8-hour window) + GT-2? (4 TB index)
→ 4 TB is 32,000 gigabits, which takes about 8.9 hours at 1 Gbps and about 0.9 hours at 10 Gbps
→ at 1 Gbps a single nightly crossing takes longer than the whole 8-hour window *[Assumes: A9 — data crosses nightly]* *[Assumes: A10 — link speed]*
→ the plan fits only if the link runs at roughly 10 Gbps or faster, or the data never crosses it nightly

**Confidence:** MEDIUM. GT-2? comes from your description, and A9 and A10 are unknown. Weakest link: we don't know where the data lives (A9). A data-flow map plus a measured link rate would raise this to HIGH.

### Conclusion C4: Running eight spot instances means restarts will happen on more nights

GT-10 (a union is at least as likely as any of its members)
→ the chance that at least one of eight concurrent instances is reclaimed is never lower than the single-instance chance p
→ the design must set aside restart time on more nights than a single spot instance would need it

**Confidence:** HIGH. This follows from the probability rule and holds however reclaims are correlated. As an illustration only: if reclaims were independent and p were 5%, about 34% of nights would see at least one reclaim. That figure rests on the discarded assumption A14, and nothing depends on it. Weakest link: none beyond the rule itself.

### Conclusion C5: Timing risk sits in the merge instance, spot shortages and transfer, not in worker restarts

C2 (about 5.4 h margin) + C3 (transfer may break the window) + C4 (restarts routine) + GT-5? (restart from the beginning)
→ a reclaimed worker loses at most its own share of about 0.6 hours
→ a reclaimed merge instance loses up to its full 2 hours
→ the margin absorbs about eight worker restarts or two merge restarts in one night
→ the margin cannot absorb a night with no spot capacity for the workers or the merge *[Assumes: A11 — capacity available]*
→ timing risk sits mainly in the merge instance, capacity shortfalls and data transfer rather than in worker restarts

**Confidence:** MEDIUM. GT-5? comes from your description, and the reclaim rate and spot availability (A3, A11) are unmeasured. Weakest link: step 4, since spot shortages have never been observed. A shadow-run log would raise this to HIGH. Two merge restarts: 2.6 + 2 + 2 = 6.6 h fits in 8 h; three would take 8.6 h and would not.

### Conclusion C6: The cost case is unproven

GT-3? (lease 2,100/month) + GT-4? (600/month, unpriced) + GT-6? (four engineer-weeks) + GT-12? (engineer cost) + GT-11? (egress per GB) + C3 (data may cross nightly)
→ the claimed saving is 1,500 dollars a month, or 18,000 dollars over the lease year
→ four engineer-weeks at 10,000 to 25,000 dollars take about 7 to 17 months of that saving to pay back *[Assumes: A13 — four weeks suffices]*
→ even at 600 dollars a month the move nets roughly +8,000 to −7,000 dollars in the first year
→ if 4 TB leaves the cloud nightly at 0.05 to 0.09 dollars per GB, egress alone is about 6,000 to 11,000 dollars a month *[Assumes: A15 — egress price]*
→ the 600 dollar figure is unsupported, and a single omitted cost item could exceed the lease it replaces

**Confidence:** MEDIUM. The inputs GT-3?, GT-4?, GT-6?, GT-11? and GT-12? are all unread. Weakest link: the egress price and whether the data crosses nightly (GT-11?, A9). A priced bill for compute, storage and egress, plus the data-flow map, would raise this to HIGH. First-year net = $25.2k lease avoided − $7.2k cloud − $10k–25k engineering.

### Conclusion C7: Run a pilot with pass/fail checks, and default to renewal

Weights were fixed before any scoring (1–5; higher is better):

| Criterion | Weight | A: Renew only | B: Migrate now | C: Pilot with checks |
|---|---|---|---|---|
| Deadline reliability | 5 | 3 (1 h of slack) | 2 (unmeasured) | 4 (switch only after measured on-time runs, plus a merge fallback) |
| Cost certainty | 4 | 5 | 1 | 4 |
| Expected cost | 3 | 2 | 3 | 3 |
| Engineering effort (low is good) | 2 | 5 | 2 | 3 |
| Reversibility | 3 | 3 | 2 | 5 |
| **Weighted total** | | **60** | **33** | **66** |

C2 (compute fits) + C3 (transfer unmeasured) + C5 (merge and capacity risk) + C6 (cost unproven) + GT-7? (a miss costs a stale day)
→ weighted totals: pilot with checks 66 > renew only 60 > migrate now 33, driven by deadline reliability (weight 5) and reversibility (weight 3)
→ raising the engineering-effort weight from 2 to 5 ties renewal with the pilot at 75, so renewal alone is equally defensible when engineering time is scarce
→ the pilot's lead depends on its ability to fall back to renewal at no extra lease cost *[Assumes: A5 — lease still renewable]*
→ recommend a pilot with pass/fail checks, with renewal as the default outcome
→[2nd] production stays on the leased server during the pilot, so the risk of serving a stale index does not rise
→[2nd] the pilot replaces the estimated reclaim rate, cloud bill and link speed with measurements
→[3rd] the renewal decision rests on a measured cloud bill rather than the 600 dollar estimate
→[2nd] the pilot uses engineering time before any saving arrives
→[3rd] a pilot that overruns the renewal date locks in the lease for another year by default

**Confidence:** MEDIUM. It inherits GT-7? and the MEDIUM ratings of C2, C3, C5 and C6. Weakest link: this is a near tie (a 9% gap), sensitive to the effort weight. None of the second- or third-order effects contradicts a ground truth, so the chain did not go back to Phase 2.

### Conclusion C8: Renewing does not remove the risk

GT-1? (8-hour window) + GT-2? (7 h today, 2 h serial merge) + C1 (serial floor)
→ the current rebuild has 1 hour of slack, so about 14 percent growth in rebuild time uses up the window *[Assumes: A16 — rebuild time grows with the index]*
→ renewing the lease is not a risk-free baseline
→ the 2-hour merge is the one term that no number of workers removes, on either platform
→ shortening the merge helps whichever platform you choose

**Confidence:** MEDIUM. GT-1? and GT-2? come from your description, and A16 is unmeasured. Weakest link: the growth assumption. Rebuild-time history would raise this to HIGH. The 14% figure: 7 h × 1.143 ≈ 8 h.

## 5. Abandoned Reasoning

### Dead End: Arguing from other teams' spot results

**What was tried:** Using how other companies run batch jobs on spot instances to support "comfortably inside the window."
**Why abandoned:** This is an analogy with no ground truth about those companies' reclaim rates, data sizes or network links, so it can't count as direct evidence.
**What it ruled out:** Any "others do this fine" justification. Only a measured shadow run can settle the question (C5).

### Dead End: Checking the $600 figure from compute hours alone

**What was tried:** Multiplying the instance-hours per night by a spot hourly rate to test the $600.
**Why abandoned:** The hourly rate was never read from a price list. More importantly, C6 shows that storage and egress on 4 TB could be far larger, so a compute-only check could make an unsupported number look confirmed.
**What it ruled out:** Treating a compute-only estimate as the bill. The priced bill has to include storage and data transfer.

### Dead End: Treating worker restarts as the main timing risk

**What was tried:** Estimating whether restart-from-the-beginning reclaims would push the rebuild past 06:00.
**Why abandoned:** C5 shows each worker's share takes only about 0.6 h against about 5.4 h of margin, so the intermediate claim that restarts decide the deadline could not be established.
**What it ruled out:** Checkpointing worker shares as the first fix. The merge instance and spot availability matter more.

## 6. Conclusion

**Recommended approach:** Do not commit to moving the rebuild before the lease renews on the evidence you have now; run a short pilot with pass/fail checks while production stays on the leased server, and switch only if every check below passes before the renewal date (chain C7).

**Key insight:** Worker restarts are not the real timing risk, because eight workers finish their shares in about 40 minutes and the window leaves over five hours of margin; the risks that can actually sink the plan are the single merge instance, nights with no spot capacity, and moving 4 TB across the network (chain C5).

**Transfer gate:** If the source data or the finished index crosses between your site and the cloud every night, a 1 Gbps link alone needs about 9 hours per direction, which is longer than the whole window (chain C3).

**Cost gate:** The 600 dollar figure is unpriced and leaves out storage and data-transfer charges, and at an assumed several cents per GB, moving 4 TB out nightly could cost more each month than the lease (chain C6).

**Payback:** At the claimed saving of 1,500 dollars a month, four engineer-weeks takes roughly 7 to 17 months to pay back, so the move saves little or nothing in the first year even if 600 dollars proves right (chain C6).

**Baseline risk:** Renewing is not risk-free either: the current rebuild has one hour of slack, so about 14 percent growth in rebuild time breaks the window on either platform unless the merge is shortened (chain C8).

**Pilot checks, all required before switching:**

1. A priced bill covering compute, storage and data transfer that comes in below 2,100 dollars a month (chain C6).
2. A measured link speed, or a data layout that keeps the 4 TB off the link, so that transfer fits inside the margin (chain C3).
3. Two to three weeks of shadow rebuilds on spot, logging reclaims and capacity shortfalls, with every run finishing before 06:00 (chain C5).
4. An on-demand fallback for the merge instance, because a reclaim there costs up to 2 hours (chain C5).

**Trade-offs acknowledged:** The pilot uses engineering time before you see any saving, it locks in the lease for another year if it runs past the renewal date, and if that engineer's time is your scarcest resource, simply renewing scores the same (chain C7).

**Confidence:** MEDIUM — the arithmetic chains C1 and C4 are HIGH, but every applied chain depends on figures from your description (GT-1? to GT-7?), on unpriced cloud and staff costs (GT-11?, GT-12?), and on an unmeasured link speed; a priced bill, a link measurement and a shadow-run log would raise it to HIGH (chain C6).

---

Two things outside the analysis:
- One assumption is worth checking cheaply today (A7): if your search servers can switch to a new index during the day, a missed 06:00 costs a few hours of stale results, not a full day. That lowers the stakes on either platform.
- The Gmail, Google Calendar and Google Drive connectors need authorization in your claude.ai connector settings before they can be used. This analysis didn't need them.