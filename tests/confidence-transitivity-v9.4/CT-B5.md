**Answer: no. Don't move the rebuild to spot instances before the lease renews, on what's known today.** Build the cloud version and run it every night alongside the current server, which keeps publishing the real index. Move over only if that trial passes the checks in section 6.

Everything you gave me came from your description, and I checked none of it against logs, the lease or any price list. The only parts that stand on their own are arithmetic.

Process notes: this is a full analysis, since the question didn't ask for one specific technique. I read the output template and the scoring rubric. Every check ran, nothing had to be redone, and no question had to go back to you.

---

## Assumption Audit scan (process output)

| Chain | Step | Step Text (brief) | Assumption surfaced? | Added to Table? |
|---|---|---|---|---|
| C1 | 1 | parallel workers shorten only the parallel steps | none | n/a |
| C1 | 2 | merge and data movement set the floor | none | n/a |
| C1 | 3 | worker count alone cannot prove fit | none | n/a |
| C2 | 1 | 5 non-merge hours over 8 workers ≈ 0.6 h | A11 (even split) | yes |
| C2 | 2 | plus the 2 h merge ≈ 2.6 h | A12 (cloud core no slower) | yes |
| C2 | 3 | ≈ 5.4 h reserve, before data movement | none | n/a |
| C2 | 4 | compute alone fits comfortably | none | n/a |
| C3 | 1 | a reclaimed worker costs ≈ 0.6 h | none (A7 already in table) | n/a |
| C3 | 2 | reserve absorbs several worker reclaims | none (A8 already in table) | n/a |
| C3 | 3 | a late merge-node reclaim adds up to 2 h, absorbable at most twice | none | n/a |
| C3 | 4 | a night with no spot capacity is not absorbed | none (A9 already in table) | n/a |
| C3 | 5 | needs an on-demand fallback the proposal lacks | none | n/a |
| C4 | 1 | 4 TB takes ≈ 8.9 h at 1 Gbps, ≈ 53 min at 10 Gbps | none | n/a |
| C4 | 2 | whether and how fast the data moves is unstated | none | n/a |
| C4 | 3 | the description cannot show a 06:00 finish | none | n/a |
| C5 | 1 | a nightly 4 TB transfer is 120,000 GB a month | none | n/a |
| C5 | 2 | more than $0.005/GB exceeds $600 on its own | none | n/a |
| C5 | 3 | the $600 can't be relied on | none | n/a |
| C6 | 1 | 1 h of slack ≈ 14% of run time | none | n/a |
| C6 | 2 | growth past ≈ 14% misses 06:00 | A13 (run time scales with data volume) | yes |
| C6 | 3 | staying put is not risk-free | none | n/a |
| C7 | 1 | cutting over removes the only proven path | none | n/a |
| C7 | 2 | a first-weeks miss costs a day with no fallback | none | n/a |
| C7 | 3 | the claimed $1,500/month saving is unproven | none | n/a |
| C7 | 4 | weighted totals 82 > 69 > 45 | A16 (a stale day outweighs the saving) | yes |
| C7 | 5 | shadow-run while the leased server serves | A14 (lease can overlap the trial) | yes |
| C7 | [2nd] | the trial replaces unknowns with measurements | A15 (four weeks fit before renewal) | yes |
| C7 | [3rd] | renew or shorten the term if the trial runs late | A14 (existing row, referenced) | n/a |

## §6→§4 closure ledger (process output)

```text
- "Do not move the nightly rebuild to spot instances before the lease renews..." → chains C4, C5, C7 ✓
- "Adding spot workers cannot on its own show that the rebuild fits..." → chains C1, C4 ✓
- "Measure the link speed and where the input data and served index live..." → chain C4 ✓
- "Get a priced quote that includes data transfer, storage and on-demand fallback..." → chain C5 ✓
- "Run the trial nightly and log the finish time, every worker reclaim..." → chain C3 ✓
- "Cut over only if the trial finishes with time to spare every night..." → chain C7 ✓
- "Renewing, or running the trial past the renewal date, keeps paying $2,100..." → chains C5, C6, C7 ✓
- "MEDIUM — the recommendation and key insight rest on HIGH chains..." → chains C1–C7 ✓
```

## Self-audit scan (process output)

| Chain | Chain Head (brief) | Form conforming? | Rule applied | Dependency clean? |
|---|---|---|---|---|
| C1 | GT-9 (serial step) + GT-10 (transfer time) | yes | n/a | yes |
| C2 | GT-2? + GT-1? + GT-9 | yes | n/a | yes |
| C3 | C2 + GT-4? + GT-7? + GT-8? | yes | n/a | yes |
| C4 | GT-10 + GT-11 | yes | n/a | yes |
| C5 | GT-11 + GT-12 | yes | n/a | yes |
| C6 | GT-1? + GT-2? | yes | n/a | yes |
| C7 | C1…C6 + GT-3? + GT-5? + GT-6? | yes | n/a | yes (depends only on upstream C1–C6; no cycle) |

| §6 Span (brief) | Construct | Claim under R11? | R11 clause applied | Chain cited |
|---|---|---|---|---|
| Recommended approach: don't move before renewal… | bold lead-in | yes | bold lead-in whose colon closes the bold span; prescribed lead-in | C4, C5, C7 |
| Key insight: adding workers can't show fit… | bold lead-in | yes | prescribed lead-in | C1, C4 |
| Checks before cut-over: | bold lead-in | no | section-intro label: colon-terminated span is the whole line, no citation | n/a |
| Measure link speed and data location… | list item | yes | list item over forty characters | C4 |
| Get a priced quote… | list item | yes | list item over forty characters | C5 |
| Run the trial nightly and log… | list item | yes | list item over forty characters | C3 |
| Cut over only if… | list item | yes | list item over forty characters | C7 |
| Trade-offs acknowledged: renewing keeps paying… | bold lead-in | yes | prescribed lead-in | C5, C6, C7 |
| Confidence: MEDIUM… | bold lead-in | yes | bold lead-in whose colon closes the bold span | C1–C7 |

```text
Scan complete: 7 chain rows, one per section-4 chain block in order; 9 section-6 rows, one per construct in order — 8 claims under R11, 1 excluded. 0 chains malformed, 0 claims untraced.
```

---

## 1. Problem Essence

**Core problem:** Does the current evidence justify giving up the one setup known to finish the rebuild by 06:00, at the moment a one-year lease is up for renewal, in exchange for a spot setup that nobody has priced, whose reclaim rate is unknown, and whose data movement nobody has stated? If not, what must be shown before the renewal date?

**Success criteria:**
- The Conclusion gives a clear yes or no on moving before renewal.
- The Conclusion says whether "splitting finishes comfortably" holds, treating compute time, the single-core merge and data movement separately.
- The Conclusion says whether the $600/month figure can be relied on.
- The Conclusion names the specific checks that would change the answer.

## 2. Assumptions Table

| Assumption | Type | Treatment | Verdict | Verification |
|---|---|---|---|---|
| A1: The rebuild must finish by 06:00, giving an 8 h window | current constraint | record expiry conditions | Accept — lapses if opening hours change or search can switch to a new index during the day | your description; unverified — flagged (GT-1?) |
| A2: The rebuild takes 7 h, and its last 2 h are a single-core merge | untested belief | verify or flag | Accept — used as stated; job logs would confirm it | unverified — flagged (GT-2?) |
| A3: Splitting the work will finish it comfortably inside the window | untested belief | verify or flag | Challenge — holds for compute time (C2) but leaves out the merge and data movement (C1, C4) | unverified — flagged; tested in C1, C2, C4 |
| A4: The cloud bill will be about $600/month | untested belief | verify or flag | Challenge — your description says nobody has priced it, and it lists no costs for transfer, storage or fallback (C5) | your description (GT-11); unverified — flagged |
| A5: The merge has to run on one core | convention | challenge before use | Challenge — unclear whether that is inherent or just how the tool works today; if the merge can be split, the minimum time in C1 drops | unverified — not used as a hard limit in any chain |
| A6: The whole index has to be rebuilt every night | convention | challenge before use | Challenge — incremental rebuilds would cut both compute and transfer; the description doesn't consider them | unverified — outside the chains; noted as an option |
| A7: A reclaimed worker restarts its share from the beginning | convention | challenge before use | Challenge — a design choice: saving progress partway would limit the loss; kept as the worst case | unverified — flagged (GT-4?) |
| A8: Spot reclaims in your region are rare enough to live with | untested belief | verify or flag | Challenge — you have no data and have never bought spot | unverified — flagged (GT-7?) |
| A9: Spot capacity will be available every night | untested belief | verify or flag | Challenge — capacity for an instance type can run out on a given night | unverified — flagged (GT-8?) |
| A10: The lease renews next quarter for 12 months at $2,100/month | current constraint | record expiry conditions | Accept — lapses at renewal; whether a shorter term can be negotiated is unknown | unverified — flagged (GT-3?) |
| A11: The 5 non-merge hours split evenly across 8 workers | untested belief | verify or flag | Challenge — uneven shards let the slowest worker set the time | unverified — flagged (found by the audit, C2) |
| A12: A cloud core runs the merge no slower than the current server's core | untested belief | verify or flag | Challenge — CPU and disk speed may differ | unverified — flagged (found by the audit, C2) |
| A13: Rebuild time grows roughly in line with data volume | untested belief | verify or flag | Accept — used only as a rough model | unverified — flagged (found by the audit, C6) |
| A14: The lease can overlap a trial, or be renewed or shortened, while the trial runs | current constraint | record expiry conditions | Challenge — lapses at the renewal date unless the terms allow otherwise | unverified — flagged (found by the audit, C7) |
| A15: The four engineer-weeks fit before the renewal date | untested belief | verify or flag | Challenge — "next quarter" may leave little time for the trial | unverified — flagged (found by the audit, C7) |
| A16: A day of stale search costs more than the claimed saving | untested belief | verify or flag | Challenge — the cost of a stale day isn't quantified; it sets the reliability weight in C7 | your description (GT-5?); unverified — flagged |
| A17: A single-core step takes the same time however many workers there are, and transfer time = data size ÷ link speed | physical law | accept as a ground-truth candidate | Accept — true by definition; see GT-9 and GT-10 | the identities written out in GT-9 and GT-10 |

## 3. Ground Truths

- **GT-1?** The rebuild window runs 22:00–06:00, which is 8 hours. — unverified: from your description; no schedule or SLA document seen
- **GT-2?** The rebuild takes 7 h, and its last 2 h are a merge on a single core. — unverified: from your description; no job logs seen
- **GT-3?** The lease renews next quarter for 12 months at $2,100/month. — unverified: from your description; lease not seen
- **GT-4?** A reclaimed spot worker restarts its share of the rebuild from the beginning. — unverified: from your description of the planned design
- **GT-5?** Missing 06:00 leaves search serving yesterday's index for the whole business day. — unverified: from your description
- **GT-6?** The move needs one engineer for four weeks. — unverified: your team's estimate
- **GT-7?** You have no data on spot reclaim rates in your region and have never bought spot capacity. — unverified: from your description
- **GT-8?** Spot capacity for a requested instance type can be unavailable on a given night. — unverified: general platform behaviour; no provider documentation was opened (no provider is named)
- **GT-9** A step that runs on one core takes the same wall-clock time however many workers the other steps are spread across; parallel workers shorten only the parts that can be split. — source: definition (Amdahl's serial-fraction bound); read-at-source: the identity as stated in this entry
- **GT-10** Moving 4×10¹² bytes (32×10¹² bits) takes 32,000 s ≈ 8.9 h at 1 Gbps and 3,200 s ≈ 53 min at 10 Gbps, before protocol overhead. — source: definition (time = bits ÷ bit rate); read-at-source: the arithmetic shown in this entry
- **GT-11** Your description says the index is 4 TB and rebuilt nightly, that the ~$600/month figure has not been priced, and that nobody has bought spot. It says nothing about where the input data or served index live, the link speed, or any transfer, storage or fallback cost. — source: your description; read-at-source: "a 4 TB search index every night", "around 600 dollars a month, though nobody has priced it"; the full text contains no bandwidth, location or cost items
- **GT-12** A 4,000 GB transfer every night for 30 nights is 120,000 GB a month, and $600 ÷ 120,000 GB = $0.005/GB. — source: definition (arithmetic); read-at-source: the arithmetic shown in this entry

**Provenance summary:**

```text
?-marked: GT-1?, GT-2?, GT-3?, GT-4?, GT-5?, GT-6?, GT-7?, GT-8? (8 of 12)
Read-at-source: GT-9 — identity stated in its entry; GT-10 — arithmetic in its entry; GT-11 — your description, quoted; GT-12 — arithmetic in its entry
```

No Phase 3 failure records: nothing was fetched and failed. The eight `?` facts are your own statements, and no source exists that I could have opened for them.

## 4. Derivation Chains

### Conclusion C1: Adding spot workers cannot on its own show that the rebuild fits the window

GT-9 (single-core steps don't speed up) + GT-10 (transfer time = size ÷ link speed)
→ parallel workers shorten only the steps that can be split, never the single-core merge or the data movement
→ those two fixed costs set a minimum time for any split rebuild, whatever the worker count
→ the number of spot instances bought cannot by itself show that the rebuild finishes by 06:00

**Confidence:** HIGH — rests only on definitions. Weakest link: step 2 assumes data movement is needed at all, and C4 makes that dependency explicit.

### Conclusion C2: Compute time alone fits comfortably

GT-2? (7 h run, last 2 h single-core) + GT-1? (8 h window) + GT-9 (single-core steps don't speed up)
→ the 5 non-merge hours spread over eight workers take at best about 0.6 h *[Assumes: A11 — even split]*
→ adding the 2 h merge gives about 2.6 h of compute *[Assumes: A12 — cloud core no slower]*
→ that leaves about 5.4 h of the 8 h window as reserve, before any data movement
→ on compute time alone, the lead's "comfortably inside the window" holds

**Confidence:** MEDIUM — GT-2? and GT-1? are unconfirmed. Job logs showing the 7 h / 2 h split would raise it to HIGH. Weakest link: step 1, because uneven shards (A11) would stretch it.

### Conclusion C3: Reclaims are survivable, but only with a fallback the proposal doesn't include

C2 (≈5.4 h reserve) + GT-4? (restart from the beginning) + GT-7? (no reclaim data) + GT-8? (capacity can run out)
→ a reclaimed worker loses at most its own share, about 0.6 h
→ the reserve absorbs several worker reclaims in one night
→ a late reclaim of the merge node adds up to 2 h, which the reserve absorbs at most twice
→ a night with no spot capacity at all is not absorbed by any reserve
→ reliability requires an on-demand fallback for the merge node and for capacity outages, which the proposal does not include

**Confidence:** MEDIUM — GT-7? means the reclaim rate is unknown, and GT-8? means capacity outages are unconfirmed for your provider. Reclaim and capacity-failure counts from a real trial would raise it to HIGH. Weakest link: step 4, whose frequency nobody has measured.

### Conclusion C4: Your description cannot show that the cloud rebuild finishes by 06:00

GT-10 (4 TB move time at 1 vs 10 Gbps) + GT-11 (location and link speed not stated)
→ moving 4 TB takes about 8.9 h at 1 Gbps and about 53 min at 10 Gbps
→ whether the data moves each night, and at what speed, is exactly what the description leaves out
→ that one missing input decides whether the move blows the 8 h window or fits with room to spare
→ the plan cannot be called feasible until link speed and data location are measured

**Confidence:** HIGH — the conclusion is about what your description can establish, and it rests only on arithmetic and the description itself. Weakest link: none structural. If data never crosses the link, this chain shows the question is open, not that the plan fails.

### Conclusion C5: The $600/month figure is not a reliable estimate

GT-11 (4 TB nightly, $600 unpriced, no cost items) + GT-12 (120,000 GB/month; $0.005/GB break-even)
→ if the 4 TB index crosses between your site and the cloud each night, that is 120,000 GB a month
→ at any transfer charge above $0.005 per GB, that transfer alone exceeds the whole $600 estimate
→ with transfer, storage and fallback left out, the $600 is at best a lower bound on a bill nobody knows
→ even whether the move saves money against the $2,100 lease is unproven, let alone how much

**Confidence:** HIGH — conditional arithmetic plus what your description says. Weakest link: step 1 depends on whether data crosses the link, which C4 shows is unknown. Either way the conclusion stands, because $600 can't be relied on until that is known.

### Conclusion C6: Staying on the current server is not risk-free

GT-1? (8 h window) + GT-2? (7 h run)
→ today's run leaves 1 h of slack, about 14% of run time
→ growth in run time beyond about 14% misses 06:00 on the current server, with no way to spread the work *[Assumes: A13 — run time grows with data volume]*
→ keeping the lease means accepting a fixed time limit, so the cloud work is valuable even if the lease is renewed

**Confidence:** MEDIUM — GT-1? and GT-2? are unconfirmed, and so is the growth rate. Job logs plus the index's recent growth trend would raise it to HIGH. Weakest link: step 2 (A13).

### Conclusion C7: Don't move before renewal on this evidence; run a trial alongside first

C1 (workers can't prove fit) + C2 (compute fits) + C3 (fallback missing) + C4 (feasibility undetermined) + C5 ($600 unreliable) + C6 (1 h slack) + GT-3? (one-year renewal) + GT-5? (a miss costs a day) + GT-6? (four engineer-weeks)
→ moving before renewal and giving up the server removes the only setup shown to finish by 06:00
→ a cloud miss in the first weeks would then cost a whole business day of stale search with nothing to fall back on
→ the claimed saving is $1,500 a month, and C5 shows even whether it saves money is unproven
→ weighted totals: trial-then-decide 82 > renew-and-stay 69 > move-before-renewal 45, driven by reliability ×5 and reversibility ×4 *[Assumes: A16 — a stale day outweighs the saving]*
→ do not move before renewal; build the pipeline and run it alongside while the leased server keeps serving *[Assumes: A14 — lease can overlap the trial]*
→[2nd] the trial turns the unpriced bill, the unmeasured reclaim rate and the unstated link speed into measurements *[Assumes: A15 — four weeks fit before renewal]*
→[3rd] if the trial can't finish before the renewal date, renewing or negotiating a shorter term keeps the next decision point instead of forcing a blind one *[Assumes: A14 — lease terms]*

Scoring for the three options (weights fixed before any option was scored):

| Criterion (weight) | Renew and stay | Move before renewal | Trial, then decide |
|---|---|---|---|
| Finishes by 06:00 reliably (5) | 4 | 2 | 5 |
| Cost is predictable (3) | 5 | 1 | 4 |
| 12-month cost (3) | 2 | 3 | 3 |
| Easy to reverse (4) | 3 | 1 | 5 |
| Little engineering effort (2) | 5 | 2 | 2 |
| Room for growth (3) | 2 | 5 | 4 |
| **Total** | **69** | **45** | **82** |

The gap between the top two is 16%, so this is not a near-tie. Checked against the ground truths, the knock-on effects contradict none of them. One adverse effect is carried as a trade-off: engineer time is spent before any saving is proven.

**Confidence:** MEDIUM — GT-3? means the lease term and whether it can be shortened are unconfirmed, GT-5? means the cost of a stale day isn't quantified, and GT-6? means the four-week effort is an estimate. Raising this to HIGH needs the lease terms in writing, a cost for one stale-search day, and a delivery plan that fits before renewal. Weakest link: step 4's reliability weight, which depends on A16.

## 5. Abandoned Reasoning

### Dead End: Estimating the real cloud bill from typical spot and egress prices

**What was tried:** Replacing the $600 with a rough bottom-up estimate: instance-hours times a typical spot rate, plus a typical per-GB egress charge on 120,000 GB a month.

**Why abandoned:** No provider is named and no price page was opened, so every rate would be recalled from memory, not read. It would also be borrowed from general cases rather than your situation. C5 reaches the decision without it: the $0.005/GB break-even from GT-12 is enough to show the $600 can't be relied on.

**What it ruled out:** Offering a precise counter-estimate. The right next step is a real quote, not a better guess.

### Dead End: "Eight workers make it roughly eight times faster"

**What was tried:** Taking 7 h ÷ 8 ≈ 0.9 h as the cloud runtime to back "comfortably inside the window".

**Why abandoned:** It contradicts GT-9. The 2 h merge doesn't speed up, and data movement (GT-10) doesn't shrink with worker count either.

**What it ruled out:** Any claim that more instances alone secure the 06:00 deadline (see C1).

### Dead End: "Other teams run search indexing on spot, so it works"

**What was tried:** Using the general popularity of spot for batch work as evidence that your reclaim rate is acceptable.

**Why abandoned:** It is an analogy with no named ground truth about another team's region, instance types or restart design. Your only relevant fact (GT-7?) is that you have no data.

**What it ruled out:** Treating reclaim risk as settled before your own trial has measured it (see C3).

## 6. Conclusion

**Recommended approach:** Do not move the nightly rebuild to spot instances before the lease renews, on the current evidence. Build the cloud pipeline and run it alongside the current server while that server keeps serving, and move over only if the trial passes the checks below (chains C4, C5, C7).

**Key insight:** Adding spot workers cannot on its own show that the rebuild fits, because neither the single-core merge nor the nightly movement of 4 TB speeds up with more workers, and at 1 Gbps moving the data alone takes longer than the whole 8-hour window (chains C1, C4).

**Checks before cut-over:**

- Measure the link speed and where the input data and served index live; at 1 Gbps, moving 4 TB alone overruns the window (chain C4).
- Get a priced quote that includes data transfer, storage and on-demand fallback; any transfer charge above about half a cent per GB exceeds the $600 estimate on its own (chain C5).
- Run the trial nightly and log the finish time, every worker reclaim and any night spot capacity was unavailable, then add an on-demand fallback for the merge node and for capacity outages (chain C3).
- Cut over only if the trial finishes with time to spare every night and its full bill, fallback included, comes in clearly below the $2,100 lease (chain C7).

**Trade-offs acknowledged:** Renewing, or running the trial past the renewal date, keeps paying $2,100 a month for a server with only 1 hour of slack, which about 14% growth in run time would use up (chain C6). The four engineer-weeks are spent with no guaranteed saving (chains C5, C7).

**Confidence:** MEDIUM — the recommendation and key insight rest on HIGH chains C1, C4 and C5. Chains C2, C3, C6 and C7 rest on your unconfirmed figures GT-1? through GT-8?. Confirming the run and merge times from job logs, getting the lease terms in writing, and measuring the reclaim rate in the trial would raise this to HIGH (chains C2, C3, C6, C7).

---

## Self-Audit Gate verdicts (process output)

**Criterion 1: Identify Essence**
Quoted span: "Does the current evidence justify giving up the one setup known to finish the rebuild by 06:00, at the moment a one-year lease is up for renewal, in exchange for a spot setup that nobody has priced, whose reclaim rate is unknown, and whose data movement nobody has stated?"
Band: **Rigorous**
Justification: The core problem names the real decision (a commitment made without evidence at renewal), not the question as asked, and each of the four success criteria can be checked against a specific part of section 6.

**Criterion 2: Challenge Assumptions**
Quoted span: "| C7 | 4 | weighted totals 82 > 69 > 45 | A16 (a stale day outweighs the saving) | yes |"
Band: **Rigorous**
Justification: All 17 rows use the four-type scheme with matching treatments and a verdict-plus-reason. Nine are challenged, the unverified ones are flagged, and the Assumption Audit scan covers every chain step and fed A11–A16 back into the table.

**Criterion 3: Establish Ground Truths**
Quoted span: "enumerated GT-1? through GT-8?; the list carries `?` on exactly those eight; unsuffixed GT-9, GT-10, GT-11 and GT-12 each name a read location and each feeds HIGH chain C1, C4 or C5"
Band: **Rigorous**
Justification: The enumeration matches the list and every unsuffixed ground truth feeds a HIGH chain with a named read location. Overlap noted: three of those four "sources" are identities written out in their own entries rather than outside documents.

**Criterion 4: Reason Upward**
Quoted span: "| C7 | C1…C6 + GT-3? + GT-5? + GT-6? | yes | n/a | yes (depends only on upstream C1–C6; no cycle) |"
Band: **Rigorous**
Justification: All seven chain blocks conform with clean dependencies. Section 5 records three dead ends in the prescribed structure, rejects the one analogy as evidence, and every new assumption is marked `[Assumes: X]`.

**Criterion 5: Validate**
Quoted span: "Run the trial nightly and log the finish time, every worker reclaim and any night spot capacity was unavailable, then add an on-demand fallback for the merge node and for capacity outages (chain C3)."
Band: **Sound**
Justification: Every chain names its weakest link and every `?` input has a caveat saying what would raise it to HIGH. But this section 6 claim rests only on MEDIUM chain C3 and the overall rating is MEDIUM, so no exception is claimed and the band is below Rigorous.

**Criterion 6: Conclusion-to-Ground-Truth Traceability**
Quoted span: "| Key insight: adding workers can't show fit… | bold lead-in | yes | prescribed lead-in | C1, C4 |" together with the analysis text "at 1 Gbps moving the data alone takes longer than the whole 8-hour window"
Band: **Rigorous**
Justification: All eight claims name a section 4 chain and none are untraced. The key insight is a finding the "split it across workers" framing misses, not a restatement of the recommendation.

Gate cleared: no criterion Absent, none Hand-wavy.