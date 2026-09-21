**Short answer:** Don't commit five engineers to the full migration now, and don't just wait a year either. Spend about three weeks measuring and piloting, then decide on a fixed date. Nobody has yet measured how much of your 48ms is spent on the part gRPC changes, and that number decides whether the migration pays off. The full analysis follows. The working steps come first, as the method requires, and the six-part analysis follows them.

Process notes: the analysis ran in full mode (Step 0 found no single-technique trigger phrase). No re-entry edge fired. The template, rubric, trade-off and pre-mortem files were all read before use.

## Trade-off working (process output)

**Options:** A = commit to the full migration now. B = hold off one year. C = measure, then decide (time-boxed profiling plus a one-service pilot, with a fixed decision date).

**Criteria and weights, locked before scoring** (higher is always better): Decision evidence quality ×5, Engineering cost avoided ×3, Operational safety ×4, Consumer stability ×3, Reversibility ×4, Speed to benefit ×2.

| Option | Evidence ×5 | Cost ×3 | Ops safety ×4 | Consumer ×3 | Reversibility ×4 | Speed ×2 | Total |
|---|---|---|---|---|---|---|---|
| A commit now | 1→5 | 1→3 | 1→4 | 1→3 | 1→4 | 5→10 | **29** |
| B hold a year | 2→10 | 5→15 | 5→20 | 5→15 | 4→16 | 1→2 | **78** |
| C measure-then-decide | 5→25 | 4→12 | 4→16 | 4→12 | 5→20 | 3→6 | **91** |

**Sensitivity:** C leads B by 13 points (14%), outside the near-tie band. B beats C only if the Evidence weight drops below 1, which means not caring whether the benefit is real. A beats C only if the Speed weight exceeds 33.

## Adversarial pass (process output)

**Premise:** It is three months from now, and the measure-then-decide plan has failed badly.

**Causes** (unfiltered, from four viewpoints):
- Infrastructure lead: the pilot covered one service, and its result did not carry over to the other five.
- Infrastructure lead: profiling captured only the median, so the p99 benefit the benchmark was about was never measured.
- Infrastructure lead: felt overruled, the pilot was under-resourced, and the result was inconclusive.
- On-call engineer: the pilot cutover caused an incident that the three-person rotation absorbed alone.
- On-call engineer: HTTP/2 long-lived connections were unevenly balanced by the existing load balancers, and pages followed.
- Consuming team: the pilot forced a consumer redeploy anyway, so the disruption we meant to avoid happened regardless.
- Engineering director: the decision date slipped, and "measure first" became a year of nothing.
- Engineering director: several engineer-weeks were spent and the answer was still ambiguous, because no threshold had been set in advance.
- Competitor: they kept improving latency while we measured. This only matters if latency is a competitive factor, which is A2 and unverified.
- Measurement: tracing overhead distorted the latency split.

**Interrogation:** The cause that most embarrasses the recommendation is "the pilot forced a consumer redeploy anyway." It attacks the reversibility score that C's win depends on.

**Clusters:**
- **K1: Measurement design cannot settle the question.** Absorbs: one-service scope, median-only profiling, tracing distortion, ambiguity with no threshold. Bears on C3 and C2.
  **Disposition, plan change:** measure the serialization-plus-transport share across all six services at both p50 and p99, and write down the commit threshold before reading the data (C5 hop 3).
- **K2: The pilot lands on a thin rotation.** Absorbs: the cutover incident, HTTP/2 balancing, the forced consumer redeploy. Bears on C4, GT-6?, A7 and A9.
  **Disposition, plan change:** pilot with REST left running so no consumer has to redeploy (C5 hop 4), and put the pilot's engineers on the on-call rotation while it runs (C5 hop 5).
- **K3: Governance drift.** Absorbs: the slipped date, the disengaged lead, the competitor moving. Bears on C5, A11 and A2.
  **Disposition, plan change:** set a fixed decision date and have the infrastructure lead own the pilot (C5 hop 6).
  **Accepted risk with a named mitigation:** the competitor moving is accepted. The mitigation is to check A2 (whether any latency target is actually being missed) inside the same time-box.

## §6→§4 closure ledger (process output)

- "Do not commit five engineers now … run a time-boxed measure-then-decide step" → chain C5 ✓
- "Measure the serialization-plus-transport share at p50 and p99 across all six services…" → chain C3, chain C5 ✓
- "Pilot gRPC on the lowest-risk of the six with REST left running…" → chain C5 ✓
- "Decide on the fixed date…" → chain C5 ✓
- "The competitor's 30% is not a property of gRPC…" → chain C1, chain C2 ✓
- "Measuring first delays any real benefit…" → chain C5 ✓
- "Confidence: MEDIUM…" → chain C5 ✓

## Assumption Audit scan (process output)

| Chain | Step | Step Text (brief) | Assumption surfaced? | Added to Table? |
|---|---|---|---|---|
| C1 | 1 | protocol change shortens only serialization+transport | none | n/a |
| C1 | 2 | percentage gain = s × r, system-specific | none | n/a |
| C1 | 3 | benchmark % transfers only at matching share | none | n/a |
| C2 | 1 | benchmark is p99 on their workload; ours is a median | none | n/a |
| C2 | 2 | nothing shows our share matches theirs | none | n/a |
| C2 | 3 | 30% cannot serve as our expected benefit | none | n/a |
| C3 | 1 | saving = s × r × 48ms | A3, A4 (already in table) | n/a |
| C3 | 2 | bracket 0.7–13.4ms, central 3.6ms | A3, A4 (already in table) | n/a |
| C3 | 3 | ends of the bracket recommend opposite actions | A2 (already in table) | n/a |
| C3 | 4 | cannot resolve without measuring s | none | n/a |
| C4 | 1 | 50 engineer-weeks plus consumer redeploys | A5 (already in table) | n/a |
| C4 | 2 | highest-traffic services carry the widest blast radius | none | n/a |
| C4 | 3 | 3 people on-call for 22 services during rollout | A12 | yes |
| C4 | 4 | certain, front-loaded cost on a thin rotation | none | n/a |
| C5 | 1 | weighted totals 91 > 78 > 29 | none | n/a |
| C5 | 2 | recommend measure-then-decide | none | n/a |
| C5 | 3 | six services, p50/p99, pre-registered threshold | none | n/a |
| C5 | 4 | one-service pilot with REST retained | A7 (already in table) | n/a |
| C5 | 5 | pilot engineers join on-call | none | n/a |
| C5 | 6 | ~3-week time-box, fixed decision date | A11, A13 | yes |
| C5 | 7 | [2nd] small s: avoid one engineer-year | none | n/a |
| C5 | 8 | [2nd] large s: internal benchmark replaces competitor's | none | n/a |
| C5 | 9 | [2nd] pilot surfaces HTTP/2 balancing on one service | A9 (already in table) | n/a |
| C5 | 10 | [2nd] adverse: benefit arrives later by the time-box | none | n/a |
| C5 | 11 | [3rd] consumer regen sequenced service by service | A7 (already in table) | n/a |
| C5 | 12 | [3rd] adverse: open-ended measure-first drifts to hold | A11 (already in table) | n/a |

## Self-audit scan (process output)

| Chain | Chain Head (brief) | Form conforming? | Rule applied | Dependency clean? |
|---|---|---|---|---|
| C1 | GT-8 + GT-9 | yes | n/a | yes |
| C2 | GT-4? + GT-3? + C1 | yes | n/a | yes |
| C3 | GT-8 + GT-3? | yes | n/a | yes |
| C4 | GT-5? + GT-6? + GT-7? + GT-1? + GT-2? | yes | n/a | yes |
| C5 | C2 + C3 + C4 | yes | n/a | yes |

| §6 Span (brief) | Construct | Claim under R11? | R11 clause applied | Chain cited |
|---|---|---|---|---|
| Recommended approach: do not commit now… | bold lead-in | yes | prescribed lead-in, colon closes bold span | C5 |
| Measure serialization-plus-transport share… | list item | yes | list item past forty characters | C3, C5 |
| Pilot gRPC on the lowest-risk… | list item | yes | list item past forty characters | C5 |
| Decide on the fixed date… | list item | yes | list item past forty characters | C5 |
| Key insight: the competitor's 30%… | bold lead-in | yes | prescribed lead-in, colon closes bold span | C1, C2 |
| Trade-offs acknowledged: measuring first delays… | bold lead-in | yes | prescribed lead-in, colon closes bold span | C5 |
| Confidence: MEDIUM… | bold lead-in | yes | bold lead-in whose colon closes the bold span | C5 |
| Explanation paragraph after Confidence | prose | no | prose with neither bold colon lead-in nor list marker | n/a |

```text
Scan complete: 5 chain rows, one per section-4 chain block in order; 8 section-6 rows, one per construct in order — 7 claims under R11, 1 excluded. 0 chains malformed, 0 claims untraced.
```

## Self-Audit Gate verdict blocks (process output)

**Criterion 1: Identify Essence**
Quoted span: "Does the latency gain gRPC would deliver on these six services' own request profile justify about one engineer-year of work plus consumer redeploys on a three-person on-call rotation, and what evidence must exist before committing?"
Band: **Rigorous**
Justification: The statement names the decision, not the triggering benchmark. Each of the three success criteria can be checked against a property of §6: one named course of action, the evidence basis and whether it was measured here, and the flip condition.

**Criterion 2: Challenge Assumptions**
Quoted span: "| C4 | 3 | 3 people on-call for 22 services during rollout | A12 | yes |"
Band: **Rigorous**
Justification: Every row uses one of the four types with its prescribed treatment, an "Accept/Challenge/Discard —" verdict, and a named verification. A1 and A8 are discarded. The audit scan covers all 26 chain steps and added A12 and A13 to the table.

**Criterion 3: Establish Ground Truths**
Quoted span: "enumerated GT-1, GT-2, GT-3, GT-4, GT-5, GT-6, GT-7; the list carries `?` on exactly those seven. The unsuffixed GT-8 and GT-9 feed HIGH chain C1 and each names its definitional read-at-source location."
Band: **Rigorous**
Justification: The enumeration matches the list when checked. Both unsuffixed ground truths feed a HIGH chain and name where they were read. No `?`-marked ground truth feeds a HIGH chain, so no Phase 3 read was owed.

**Criterion 4: Reason Upward**
Quoted span: "| C5 | C2 + C3 + C4 | yes | n/a | yes |" (and every other chain row: yes / n/a / yes)
Band: **Rigorous**
Justification: All five chains conform in form, have clean dependencies and carry genuine intermediate steps. §5 records three dead ends in the full structure. The benchmark is not used as analogy evidence: C2 exists to reject that use. A12 and A13 are declared inline with `[Assumes:]`.

**Criterion 5: Validate**
Quoted span: "C5 Confidence: MEDIUM — capped by C2, C3 and C4 (each MEDIUM, explained on their own lines); A11 and A13 are priced: if the date slips, C degrades to B (78), still far above A (29), so the recommendation over committing now stands"
Band: **Rigorous**
Justification: C1's HIGH rating is licensed on all three axes. Every MEDIUM line names its `?` inputs or cited chains and gives the verification that would close them. The Conclusion's MEDIUM equals its weakest contributing chain. The adversarial pass has a past-tense premise, causes, clusters citing chain and ground-truth ids, and a disposition for every cluster.

**Criterion 6: Conclusion-to-Ground-Truth Traceability**
Quoted span: "| Key insight: the competitor's 30%… | bold lead-in | yes | prescribed lead-in, colon closes bold span | C1, C2 |" (all 7 claim rows cite a chain; 0 untraced)
Band: **Rigorous**
Justification: Every §6 claim cites a §4 chain. The Key Insight says the benchmark's gain is a property of the competitor's transport share rather than of gRPC. Reasoning from the benchmark as an analogy would not reach that finding.

The gate is cleared: no criterion is Absent, and none is Hand-wavy.

---

# First-Principles Analysis: REST → gRPC migration timing

## 1. Problem Essence

**Core problem:** Does the latency gain gRPC would deliver on these six services' own request profile justify about one engineer-year of work plus consumer redeploys on a three-person on-call rotation, and what evidence must exist before committing?

**Success criteria:**
- The Conclusion names exactly one course of action: commit now, hold, or a named alternative.
- The Conclusion states what evidence the benefit estimate rests on, and whether that evidence was measured on these services.
- The Conclusion states the condition under which the recommendation would flip to committing.

## 2. Assumptions Table

| Assumption | Type | Treatment | Verdict | Verification |
|---|---|---|---|---|
| A1: The competitor's 30% p99 gain transfers to our services | untested belief | verify or flag | Discard — C1 shows a benchmark percentage transfers only at a matching transport share, which is unmeasured | GT-8, GT-9 (definitions) |
| A2: Reducing latency is a business need (a latency target is being missed) | untested belief | verify or flag | Challenge — the brief states no SLO breach; the case is framed around a benchmark, not a user-facing problem | unverified — flagged; check SLO dashboards inside the time-box |
| A3: Serialization plus transport is a large share (s) of the 48ms median | untested belief | verify or flag | Challenge — no profiling supplied; bracketed at 0.05–0.40 in C3 | unverified — flagged; read from existing distributed traces |
| A4: gRPC removes a fraction r of that share (0.3–0.7) | untested belief | verify or flag | Challenge — depends on payload shape and HTTP/2 connection reuse | unverified — flagged; the pilot measures it |
| A5: The migration takes 5 engineers × 10 weeks | untested belief | verify or flag | Challenge — a planning estimate, not a measurement | unverified — flagged (GT-5?) |
| A6: On-call has only 3 people | current constraint | record expiry | Accept — expires when the rotation grows through hiring or cross-training; until then it caps safe change rate | user-supplied (GT-6?) |
| A7: All consumers must cut over when the provider migrates | convention | challenge before use | Challenge — dual-protocol serving (REST beside gRPC) lets consumers move on their own schedule | unverified — pilot confirms feasibility |
| A8: The choice is binary, commit now or wait a year | convention | challenge before use | Discard — C5 shows a third option dominates both | trade-off working |
| A9: Existing load balancers spread long-lived HTTP/2 connections evenly | untested belief | verify or flag | Challenge — L4 balancing of persistent connections can concentrate load | unverified — the pilot surfaces it on one service |
| A10: The two-quarter window is a hard deadline | convention | challenge before use | Challenge — no driver for the date is stated | none supplied |
| A11: A fixed decision date will be honoured | untested belief | verify or flag | Challenge — surfaced by the audit on C5 hop 6; mitigated by named ownership (K3) | unverified — flagged |
| A12: A protocol cutover raises incident rate during rollout | untested belief | verify or flag | Challenge — surfaced by the audit on C4 hop 3 | unverified — flagged; check the incident history of past cutovers |
| A13: About three weeks for one to two engineers is enough to measure s and run a pilot | untested belief | verify or flag | Challenge — surfaced by the audit on C5 hop 6 | unverified — flagged |

Phase 2 used an inversion: what would guarantee the migration fails to pay off? The answers produced A2, A3, A7, A9 and A12.

## 3. Ground Truths

- **GT-1?** There are 22 internal microservices on REST/JSON. Unverified: user-supplied, no source.
- **GT-2?** Peak load is 340,000 requests per minute (about 5,667 per second). Unverified: user-supplied.
- **GT-3?** Median inter-service latency is 48ms. Unverified: user-supplied, and no p99 was given.
- **GT-4?** A competitor's public benchmark claims 30% lower p99 latency with gRPC. Unverified: no URL or document was named, so it could not be opened.
- **GT-5?** The migration is estimated at 5 engineers for about 10 weeks. Unverified: user-supplied estimate.
- **GT-6?** The on-call rotation has 3 people. Unverified: user-supplied.
- **GT-7?** Every consuming team would regenerate client stubs and redeploy. Unverified: user-supplied.
- **GT-8** Latency-share identity: if a component takes fraction s of end-to-end latency T and is cut by fraction r, then T' = (1−s)T + s(1−r)T. The saving is s·r·T, and components the change does not touch are unchanged.
  Source: arithmetic identity (Amdahl's law form). Read-at-source: definitional, stated in full in this entry, and it recomputes independently.
- **GT-9** A percentile (p50, p99) is a statistic of one measured request distribution. A p99 measured on system X's workload is not a measurement of system Y, and a median and a p99 are distinct statistics.
  Source: definition of a percentile. Read-at-source: definitional, stated in this entry.

```text
?-marked: GT-1, GT-2, GT-3, GT-4, GT-5, GT-6, GT-7 (7 of 9)
Read-at-source: GT-8 — identity stated and recomputable in its entry; GT-9 — percentile definition stated in its entry
```

## 4. Derivation Chains

### Conclusion C1: A benchmark's latency gain transfers only to a system with a matching transport share

GT-8 (latency-share identity) + GT-9 (a percentile is a property of the measured distribution)
→ a protocol change shortens only the serialization-and-transport part of a request, leaving handler and downstream time unchanged
→ the percentage gain it produces equals s × r, which depends on the share s in the system being measured
→ a benchmark's percentage transfers to another system only when that system's transport share matches the benchmark system's

**Confidence:** HIGH. Inputs: GT-8 and GT-9 are unsuffixed, with definitional read-at-source locations. Inference: each hop follows by arithmetic from GT-8. Rivals: "the 30% is a property of gRPC itself" is ruled out by GT-8 (see §5, Dead End 1).

### Conclusion C2: The competitor's 30% cannot serve as our expected benefit

GT-4? (competitor claims 30% lower p99) + GT-3? (our median is 48ms) + C1 (transfer requires a matching transport share)
→ the benchmark reports p99 on the competitor's workload, while the only figure we hold is a median on ours
→ nothing in the brief establishes that our transport share matches the competitor's
→ the 30% figure cannot serve as the expected benefit of migrating these six services

**Confidence:** MEDIUM. The Inputs axis is short on GT-4? and GT-3?. Opening the competitor's benchmark methodology (payload sizes, what the p99 is measured over) and pulling our own per-service p99 from tracing would close it.

### Conclusion C3: The benefit cannot be sized without measuring our transport share

GT-8 (latency-share identity) + GT-3? (median is 48ms)
→ the saving from a faster protocol is s × r × 48ms on our services
→ with s bracketed 0.05–0.40 and r 0.3–0.7 the saving spans 0.72ms to 13.4ms, central 3.6ms at s = 0.15 and r = 0.5
→ that is 1.5% to 28% of the median, and a sub-millisecond gain could not justify an engineer-year while a 13ms one might
→ the decision cannot be resolved without measuring s on these six services

**Confidence:** MEDIUM. The Inputs axis is short on GT-3?: our p50 and p99 per service, read from traces, would close it. A3 and A4 are priced: if the true s or r lies outside the brackets, the range moves or widens, but only a measurement reveals which. So the endpoint, that we must measure s, stands. Rival: "JSON is obviously the bottleneck". No available observation other than measuring s settles it, and measuring s is this chain's endpoint.

### Conclusion C4: Committing now spends a certain, front-loaded cost on a thin rotation

GT-5? (5 engineers × 10 weeks) + GT-6? (3-person on-call) + GT-7? (every consumer regenerates and redeploys) + GT-1? (22 services) + GT-2? (340k req/min peak)
→ the direct cost is 50 engineer-weeks, roughly one engineer-year, before counting consumer-team redeploys
→ the change lands on the six services carrying the largest share of peak traffic, so a cutover defect has the widest blast radius available
→ three people carry on-call for all 22 services while that change rolls out [Assumes: A12 — a protocol cutover raises incident rate during rollout]
→ committing now spends a certain, front-loaded cost against a rotation with little slack to absorb rollout incidents

**Confidence:** MEDIUM. The Inputs axis is short on GT-5?, GT-6?, GT-7?, GT-1? and GT-2?. Confirming the staffing estimate, the current roster and the count of consuming teams would close it. A12 is priced: if cutovers do not raise the incident rate, the 50 engineer-week cost still holds, so the endpoint's "certain cost" stands.

### Conclusion C5: Measure, then decide, on a fixed date

C2 (benchmark is not our evidence) + C3 (benefit bracket straddles the decision) + C4 (certain, front-loaded cost)
→ weighted totals: measure-then-decide 91 > hold one year 78 > commit now 29, driven by decision evidence ×5 and reversibility ×4
→ recommend measure-then-decide over either committing now or holding a year
→ the measurement covers all six services at p50 and p99 against a commit threshold written down before the data is read
→ the pilot runs on one service with REST left in place, so no consumer is forced to redeploy
→ the pilot's engineers join the on-call rotation for its duration, so the three-person rotation does not absorb the pilot alone
→ the step is time-boxed to about three weeks for one to two engineers and ends on a fixed decision date owned by the infrastructure lead [Assumes: A11, A13]
→[2nd] if the measured s is small, the team avoids about one engineer-year of spend on a gain near the bracket's low end
→[2nd] if the measured s is large, an internal pilot benchmark replaces the competitor's as the justification
→[2nd] the pilot exposes infrastructure unknowns such as HTTP/2 connection balancing (A9) on one service instead of six
→[2nd] adverse: any real benefit arrives later by the length of the time-box
→[3rd] a migration that proceeds can sequence consumer stub regeneration service by service, capping concurrent change on the rotation
→[3rd] adverse: an open-ended measure-first drifts into the one-year hold by default, which the fixed decision date exists to prevent

**Confidence:** MEDIUM. The rating is capped by C2, C3 and C4, each MEDIUM and explained on its own line. A11 and A13 are priced: if the date slips or the time-box overruns, C degrades toward B (78), which still sits far above A (29). The recommendation against committing now therefore stands. No second-order effect contradicts a ground truth.

## 5. Abandoned Reasoning

### Dead End 1: Treat the 30% as a floor, since our traffic is high
**What was tried:** Reading the benchmark as a property of gRPC that would scale up with our 340k requests per minute.
**Why abandoned:** It contradicts GT-8. The gain is s × r of the measured system, not a constant of the protocol (C1).
**What it ruled out:** Any use of the competitor's figure as a sizing input, whether as a floor, a ceiling or a midpoint.

### Dead End 2: Hold off a year as the safe default
**What was tried:** Deferring with no action in the meantime.
**Why abandoned:** Waiting produces no new evidence about s, so a year from now the decision would rest on the same unmeasured premise. It scored 78 against 91 (C5).
**What it ruled out:** Treating delay as equivalent to caution.

### Dead End 3: Justify the migration by non-latency benefits (typed contracts, streaming)
**What was tried:** Rescuing the case with gRPC's other properties.
**Why abandoned:** The brief states no requirement for either one, and no ground truth supports them here. The intermediate step could not be established.
**What it ruled out:** Letting side benefits carry a proposal argued on latency. If those benefits matter, they need their own case.

## 6. Conclusion

**Recommended approach:** Do not commit five engineers to the full migration now, and do not simply wait a year; run a time-boxed measure-then-decide step with a fixed decision date (chain C5).

- Measure the serialization-plus-transport share at p50 and p99 across all six services from existing traces, and write down the commit threshold before reading the results (chain C3, chain C5).
- Pilot gRPC on the lowest-risk of the six with REST left running, and put the pilot's engineers on the on-call rotation while it runs (chain C5).
- Decide on the fixed date: commit if the measured saving clears the pre-registered threshold, otherwise close the question for this cycle (chain C5).

**Key insight:** The competitor's 30% is not a property of gRPC but of the competitor's transport share, so it transfers to your services only if your requests spend a similar fraction of their 48ms in serialization and transport, and nobody has measured that fraction (chain C1, chain C2).

**Trade-offs acknowledged:** Measuring first delays any real benefit by the length of the time-box and spends one to two engineers for about three weeks, against roughly one engineer-year for the full migration (chain C5).

**Confidence:** MEDIUM — the recommendation rests on C5, which is capped by C2, C3 and C4 (chain C5).

Every figure in the brief is user-supplied and unverified (GT-1? to GT-7?). The benchmark (GT-4?) was never opened, and no p99 for your own services was given. The one HIGH-confidence result, C1, is definitional. It is what makes the benchmark inapplicable whatever the missing figures turn out to be. Also check whether any latency target is actually being missed (A2). If none is, even a large measured saving may not be worth an engineer-year.