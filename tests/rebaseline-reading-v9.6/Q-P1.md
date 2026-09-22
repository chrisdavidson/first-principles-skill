**Disclosures:** No re-entry edge fired. The closure ledger, the self-audit scan and the Self-Audit Gate all ran. I read all four reference files: output template, validation rubric, trade-off and pre-mortem. The figures in your message (22 services, 340k rpm, 48ms, 5 engineers × 10 weeks, a 3-person rotation) came with no source, so they are marked `?` (unverified) below.

**Short answer:** Don't commit five engineers now. Don't wait a year either. Spend a short, fixed period measuring where your p99 latency actually goes, then pilot gRPC on one service. Decide the go/no-go threshold before you measure.

## §6→§4 closure ledger (process output)

- "Run a timeboxed measure-then-pilot on one service, threshold fixed in advance" → chain C4 ✓
- "gRPC can only remove time spent in what it replaces; the 30% figure says nothing about that share for your services; the consumer-redeploy cost comes from cutover style" → chains C1, C3 ✓
- "Accepting a short delay, pilot effort and a temporary dual stack" → chains C2, C4 ✓
- "Pre-check line" → chains C1, C2, C3, C4 ✓
- "Confidence MEDIUM" → chains C1, C4 ✓

---

## 1. Problem Essence

**Core problem:** Does moving your six highest-traffic services to gRPC give a latency gain for *your* request paths that is worth at least 50 engineer-weeks, the consumer teams' redeploy work and more load on a 3-person on-call rotation, and is "now or in a year" the only choice?

**Success criteria:**
- The Conclusion says whether the competitor's 30% p99 figure is usable evidence, and why.
- The Conclusion names one recommended action, chosen from options that include more than the two you were given.
- The Conclusion names what would reverse the recommendation.
- The Conclusion states the costs and risks being accepted.

## 2. Assumptions Table

| Assumption | Type | Treatment | Verdict | Verification |
|---|---|---|---|---|
| A1: The competitor's 30% p99 gain carries over to our services | untested belief | Verify, or flag unverified | Discard — ruled out by C1: the gain depends on each system's own path composition, and the competitor's was not ours | GT-2, GT-3 (definitional) |
| A2: Latency is causing a problem today (missed SLO, customer impact) | untested belief | Verify, or flag unverified | Challenge — no SLO miss or incident was supplied; the 48ms is a median, not a failure | unverified — flagged |
| A3: A large share of p99 latency is spent in JSON serialization and connection handling | untested belief | Verify, or flag unverified | Challenge — this is the variable the decision turns on, and it has not been measured | unverified — flagged (GT-4?) |
| A4: Every consumer must regenerate stubs and redeploy at cutover | convention | Challenge before use | Challenge — true only if the REST endpoint is removed at cutover (C3) | unverified — flagged (GT-10?) |
| A5: 5 engineers × 10 weeks is an accurate estimate | untested belief | Verify, or flag unverified | Accept — used as a lower bound only; consumer-side effort is extra | unverified — flagged (GT-6?) |
| A6: On-call has only 3 people | current constraint | Record expiry conditions | Accept — expires when the rotation grows; until then it caps rollout risk tolerance | unverified — flagged (GT-7?) |
| A7: Rollout periods on high-traffic services raise the incident rate (surfaced by audit, C2) | untested belief | Verify, or flag unverified | Accept — widely observed pattern, not measured here | unverified — flagged |
| A8: The choice is binary, now or in a year | convention | Challenge before use | Discard — a third option outscores both (C4) | C4 weighted totals |
| A9: The trade-off scores reflect the options (surfaced by audit, C4) | untested belief | Verify, or flag unverified | Accept — sensitivity-checked: B only beats C if the evidence weight drops to 2 or below | recomputed in the adversarial pass |
| A10: HTTP/2's long-lived connections need L7 or client-side load balancing (surfaced by audit, C4 2nd-order) | untested belief | Verify, or flag unverified | Accept — affects only the second-order extension | unverified — flagged (GT-11?) |
| A11: Percentile definitions and latency additivity along a request path | physical law | Accept as ground-truth candidate | Accept — mathematical definition | GT-2, GT-3 |

## 3. Ground Truths

- **GT-2** The median (p50) and p99 are different order statistics: a change in one says nothing about the other. Source: definition of a percentile. Read-at-source: definitional, stated in full here (no external document).
- **GT-3** A request's latency is the sum of the time spent in its components along the path, so replacing a component can remove at most the time spent in that component. Source: additivity of sequential durations. Read-at-source: definitional, stated in full here.
- **GT-4?** The share of your p99 path spent in serialization and connection handling. Unverified: no profiling data was supplied.
- **GT-5?** The competitor's benchmark shows 30% lower p99 with gRPC. Unverified: no citation was supplied and none was opened.
- **GT-6?** The migration needs 5 engineers for about 10 weeks. Unverified: user-supplied estimate.
- **GT-7?** Three people cover on-call. Unverified: user-supplied.
- **GT-8?** Every consuming team would regenerate stubs and redeploy. Unverified: user-supplied.
- **GT-9?** The targets are the six highest-traffic of 22 services (340k rpm peak, 48ms median). Unverified: user-supplied.
- **GT-10?** One service can serve REST and gRPC at the same time (for example via transcoding or a gateway). Unverified: no source opened in this analysis.
- **GT-11?** Long-lived HTTP/2 connections defeat per-connection L4 load balancing. Unverified: no source opened in this analysis.

`?`-marked: GT-4, GT-5, GT-6, GT-7, GT-8, GT-9, GT-10, GT-11 (8 of 10).
Read-at-source: GT-2 and GT-3 are definitional, stated in full above; together they feed the only HIGH chain, C1.
No Phase 3 failure record is needed: no source was opened and failed, and the HIGH chain rests only on definitions.

## 4. Derivation Chains

### Conclusion C1: The competitor's benchmark is not evidence for your migration

GT-2 (p99 and median are distinct statistics) + GT-3 (a change removes at most the time spent in what it changes)
→ a p99 reduction from gRPC is capped by the p99-path time your services spend in serialization and connection handling
→ that cap depends on your own path composition, which another system's benchmark does not measure
→ the competitor's 30 percent p99 figure is not evidence about your six services

**Pre-check:** head GT-2, GT-3 · ?-marked: none · lowest cited: none · Inputs ceiling: HIGH
**Confidence:** HIGH — every hop is a deduction. The rival ("the benchmark transfers because the systems are similar") is ruled out in §5, via GT-3. The endpoint is itself a ruling-out, and the 48ms median cannot stand in for p99 (GT-2).

### Conclusion C2: The cost-and-risk side is large and partly known

GT-6? (5 engineers × 10 weeks) + GT-8? (consumer regeneration) + GT-7? (3-person on-call) + GT-9? (six highest-traffic services)
→ direct cost is 5 × 10 = 50 engineer-weeks
→ consumer teams' regeneration and redeploys add an unquantified cost on top
→ rollouts on the highest-traffic services land on a rotation where each engineer covers one third of shifts [Assumes: A7 — rollout periods raise incident rate]
→ the cost-and-risk side is at least 50 engineer-weeks plus on-call exposure concentrated on 3 people

**Pre-check:** head GT-6?, GT-8?, GT-7?, GT-9? · ?-marked: GT-6?, GT-8?, GT-7?, GT-9? · lowest cited: none · Inputs ceiling: MEDIUM
**Confidence:** MEDIUM — the Inputs axis is short. GT-6?, GT-7?, GT-8? and GT-9? are your own figures, not checked here; confirming the staffing estimate, the rotation roster and the consumer count for the six services would clear them. A7 is priced: if rollouts did not raise the incident rate, the cost side would still be at least 50 engineer-weeks, so the endpoint stands.

### Conclusion C3: The consumer-redeploy cost can be decoupled from cutover

GT-8? (consumers must regenerate and redeploy) + GT-10? (one service can serve REST and gRPC side by side)
→ the regenerate-and-redeploy cost falls due only when the REST endpoint is removed
→ each consumer team can migrate on its own schedule instead of at each service's cutover

**Pre-check:** head GT-8?, GT-10? · ?-marked: GT-8?, GT-10? · lowest cited: none · Inputs ceiling: MEDIUM
**Confidence:** MEDIUM — the Inputs axis is short. GT-10? would clear if your framework's REST/gRPC dual-serving support were confirmed against its documentation. GT-8? would clear if the consumer list were confirmed.

### Conclusion C4: Measure, then pilot; don't commit now or wait a year

C1 (benchmark does not transfer) + C2 (cost side at least 50 engineer-weeks plus on-call exposure) + C3 (consumer cost can be decoupled) + GT-4? (your latency composition is unmeasured)
→ the benefit side of the decision is unsized while the cost side is not
→ weighted totals: measure-then-pilot 83 > hold a year 72 > commit now 38, driven by evidence (×5) and on-call risk (×4) [Assumes: A9 — the scores reflect the options]
→ recommend a timeboxed measure-then-pilot on one service, go/no-go threshold fixed in advance, over committing now or waiting a year
→[2nd] the pilot exercises gRPC load balancing and tracing on one service before six services depend on them [Assumes: A10 — HTTP/2 connections need L7 or client-side balancing]
→[3rd] a later go decision inherits a proven rollout path, which lowers on-call exposure across the other five services

**Trade-off matrix.** Weights were locked before any option was scored. Higher is always better.

| Option | Evidence of real benefit ×5 | On-call safety ×4 | Engineering cost efficiency ×3 | Low consumer disruption ×3 | Speed to benefit ×2 | Reversibility ×3 | Total |
|---|---|---|---|---|---|---|---|
| A: Commit now (6 services) | 1→5 | 2→8 | 2→6 | 1→3 | 5→10 | 2→6 | **38** |
| B: Hold a year | 1→5 | 5→20 | 5→15 | 5→15 | 1→2 | 5→15 | **72** |
| C: Measure, then pilot 1 service (dual-serve) | 5→25 | 4→16 | 4→12 | 4→12 | 3→6 | 4→12 | **83** |

**Other second-order effects considered.** On the unfavourable side, the infrastructure lead may read the pilot as stalling, and a dual stack may linger. Both are handled in the adversarial pass. No effect contradicts a Ground Truth, so nothing goes back to Phase 2.

**Pre-check:** head C1 (HIGH), C2 (MEDIUM), C3 (MEDIUM), GT-4? · ?-marked: GT-4? · lowest cited: MEDIUM · Inputs ceiling: MEDIUM
**Confidence:** MEDIUM — the Inputs axis is short. C2 and C3 are rated MEDIUM, and GT-4? clears only once production profiling measures the serialization and connection share of p99 (that measurement is the recommended first step). A9 is priced: B overtakes C only if the evidence weight falls to 2 or below, and A never leads unless speed dominates, so the endpoint stands. A10 affects only the second-order extension. The rivals, A and B, are ruled out in §5.

## 5. Abandoned Reasoning

### Dead End: Commit now on the strength of the benchmark

**What was tried:** Treating the competitor's 30% p99 reduction as a forecast for your six services.
**Why abandoned:** It is an analogy used as direct evidence. C1 shows the gain depends on path composition the benchmark doesn't measure. With the benefit unknown, option A scores 38 against C's 83 (C4).
**What it ruled out:** Any argument of the form "they got 30%, so we will."

### Dead End: Hold a year

**What was tried:** Deferring the whole question for twelve months.
**Why abandoned:** It produces no evidence about GT-4?, so in a year you would face the same unsized decision. It scores 72 against 83 (C4).
**What it ruled out:** Waiting as a way to reduce uncertainty.

### Dead End: Tune REST (HTTP/2, keep-alive, smaller payloads) instead of migrating

**What was tried:** Assuming any p99 problem comes from connection handling that REST can fix without changing the API contract.
**Why abandoned:** It is speculative. It rests on the same unmeasured GT-4?, so it can't be recommended either.
**What it ruled out:** Choosing *either* protocol before the measurement. It becomes a comparison arm inside the pilot.

## 6. Conclusion

**Recommended approach:** Don't commit five engineers for ten weeks now, and don't wait a year. First, profile production p99 on the six services to find how much time goes to serialization and connection handling. Then pilot gRPC on one service, serving REST and gRPC side by side, with a timebox and a go/no-go p99 threshold both set before the measurement starts. Only then decide on the other five (chain C4).

**Key insight:** gRPC can only remove the time spent in what it replaces. The 30% figure says nothing about that share on your paths, and neither does your 48ms median (chain C1). Much of the consumer-redeploy cost comes from cutting over in one step, not from gRPC itself (chain C3).

**Trade-offs acknowledged:** You accept a short delay before any gain, the pilot's engineering time and a temporary REST+gRPC dual stack. In exchange, you avoid putting at least 50 engineer-weeks and concentrated on-call risk behind an unsized benefit (chains C2, C4).

**Pre-check:** head C1 (HIGH), C2 (MEDIUM), C3 (MEDIUM), C4 (MEDIUM) · ?-marked: none · lowest cited: MEDIUM · Inputs ceiling: MEDIUM
**Confidence:** MEDIUM — C2, C3 and C4 are rated below HIGH, and each one's own confidence line gives its verification path. The recommendation reverses if profiling shows serialization and connection handling dominate p99 while an SLO is already being missed (chains C1, C4).

---

## Adversarial pass (process output)

**Recompute** — 5 × 10 = 50 engineer-weeks ✓. A: 5+8+6+3+10+6 = 38 ✓. B: 5+20+15+15+2+15 = 72 ✓. C: 25+16+12+12+6+12 = 83 ✓. C−B = 4(5)−4−3−3+2(2)−3 = 11 ✓. At evidence weight 2, C−B = 8−13+4 = −1, so B wins ✓. Each engineer's rotation share = 1/3 ✓.
**Sensitivity** — The flip ground truth is GT-4? (the share of p99 in serialization and connection handling), and it is `?`-marked. It can't be verified in this analysis, so it is carried as the confidence caveat on C4 and §6. It is also the recommended first measurement.
**Rival** — "Commit now" and "hold a year" are both ruled out in §5 (via C1 and C4). The REST-tuning rival is left unsettled in §5 and becomes a comparison arm inside the pilot.
**Premise** — The measure-then-pilot plan has already failed.
**Causes** —
- Infrastructure lead: the pilot was seen as a stall, so the lead pushed a full migration anyway without data.
- Infrastructure lead: the measurement ran six weeks instead of a short timebox and lost momentum.
- On-call engineer: the pilot service had an incident during its rollout and burned out the 3-person rotation.
- On-call engineer: a pilot engineer was also on call that week, so the response was slow.
- Consumer team: with dual-serve in place nobody migrated, and two stacks were kept forever.
- Consumer team: gRPC stubs broke their build tooling.
- Manager paying for it: no threshold was set, so an ambiguous result was argued both ways.
- Manager paying for it: the pilot was run on a low-traffic service, so the result didn't represent the six.
- Manager paying for it: the team measured the median, not p99.
- Competitor view: while you measured, latency didn't matter to customers anyway, so the effort bought nothing.
**Clusters** —
- K1, a moveable decision rule (stall, overrun, no threshold, unrepresentative service, wrong metric). Bears on C4 and GT-4?.
- K2, on-call exposure during the pilot (pilot incident, on-call overlap). Bears on C2 and GT-7?.
- K3, the dual stack becoming permanent (nobody migrated, tooling friction). Bears on C3 and GT-10?.
**Disposition** —
- K1, plan change: fix the timebox, the p99 threshold, the metric (p99 on production traffic) and a highest-traffic pilot service before starting. This change was applied to C4's endpoint.
- K2, plan change: take pilot engineers out of the rotation during rollout, and use a canary with instant fallback to REST.
- K3, accepted risk with mitigation: set a REST sunset date only if the decision is go.
**Falsification** — The conclusion is false if production profiling shows serialization and connection handling make up most of p99 and a latency SLO is already being missed, so that even a short delay has material cost.

## Assumption Audit scan (process output)

| Chain | Step | Step Text (brief) | Assumption surfaced? | Added to Table? |
|---|---|---|---|---|
| C1 | 1 | p99 gain capped by time in replaced components | none | n/a |
| C1 | 2 | cap depends on your own path composition | none | n/a |
| C1 | 3 | the 30% figure is not evidence | none | n/a |
| C2 | 1 | 50 engineer-weeks direct | none | n/a |
| C2 | 2 | unquantified consumer cost | none | n/a |
| C2 | 3 | rollouts land on a one-third-share rotation | A7 | yes |
| C2 | 4 | cost side ≥ 50 engineer-weeks plus exposure | none | n/a |
| C3 | 1 | redeploy cost falls due only at REST removal | none | n/a |
| C3 | 2 | per-team migration schedule | none | n/a |
| C4 | 1 | benefit unsized, cost not | none | n/a |
| C4 | 2 | weighted totals 83 > 72 > 38 | A9 | yes |
| C4 | 3 | recommend timeboxed measure-then-pilot | none | n/a |
| C4 | 4 | [2nd] pilot exercises load balancing and tracing | A10 | yes |
| C4 | 5 | [3rd] proven rollout path lowers exposure | none | n/a |

## Self-audit scan (process output)

| Chain | Chain Head (brief) | Form conforming? | Rule applied | Dependency clean? |
|---|---|---|---|---|
| C1 | GT-2 + GT-3 | yes | n/a | yes |
| C2 | GT-6? + GT-8? + GT-7? + GT-9? | yes | n/a | yes |
| C3 | GT-8? + GT-10? | yes | n/a | yes |
| C4 | C1 + C2 + C3 + GT-4? | yes | n/a | yes |

| §6 Span (brief) | Construct | Claim under R11? | R11 clause applied | Chain cited |
|---|---|---|---|---|
| Recommended approach | bold lead-in | yes | prescribed lead-in, always a claim | C4 |
| Key insight | bold lead-in | yes | prescribed lead-in, always a claim | C1, C3 |
| Trade-offs acknowledged | bold lead-in | yes | prescribed lead-in, always a claim | C2, C4 |
| Pre-check | bold lead-in | yes | bold lead-in whose colon closes the bold span | C1, C2, C3, C4 |
| Confidence | bold lead-in | yes | bold lead-in whose colon closes the bold span | C1, C4 |

Scan complete: 4 chain rows, one per section-4 chain block in order; 5 section-6 rows, one per construct in order — 5 claims under R11, 0 excluded. 0 chains malformed, 0 claims untraced.

## Self-Audit Gate verdicts (process output)

**Criterion 1: Identify Essence**
Quoted span: "Does moving your six highest-traffic services to gRPC give a latency gain for *your* request paths that is worth at least 50 engineer-weeks..."
Band: **Rigorous**
Justification: It is one sentence naming the real decision, not the triggering benchmark, and each success criterion is a test a reader can check against §6.

**Criterion 2: Challenge Assumptions**
Quoted span: "C4 | 2 | weighted totals 83 > 72 > 38 | A9 | yes"
Band: **Rigorous**
Justification: All rows use the four-type scheme, the verdicts are justified, A1 and A8 are discarded, the unverified rows are flagged, and the audit covers all 14 chain steps.

**Criterion 3: Establish Ground Truths**
Quoted span: "enumerated GT-4, GT-5, GT-6, GT-7, GT-8, GT-9, GT-10, GT-11; the list carries `?` on exactly those eight"
Band: **Sound**
Justification: The enumeration matches the list. However, the read-at-source locations for GT-2 and GT-3 are definitional rather than a located document, so that label is looser than the Rigorous test intends.

**Criterion 4: Reason Upward**
Quoted span: "0 chains malformed, 0 claims untraced" / "C4 | C1 + C2 + C3 + GT-4? | yes | n/a | yes"
Band: **Rigorous**
Justification: Every chain conforms and depends only on defined inputs, the arithmetic recomputes, §5 records three structured dead ends, and the benchmark is explicitly not used as evidence.

**Criterion 5: Validate**
Quoted span: "B overtakes C only if the evidence weight falls to 2 or below, and A never leads unless speed dominates, so the endpoint stands."
Band: **Rigorous**
Justification: Each band matches what its axes allow (C1 HIGH, C2–C4 MEDIUM, §6 matching the weakest chain), each [Assumes] is priced, and the adversarial record is complete with a disposition for every cluster.

**Criterion 6: Conclusion-to-Ground-Truth Traceability**
Quoted span: "Key insight | bold lead-in | yes | prescribed lead-in, always a claim | C1, C3"
Band: **Rigorous**
Justification: All five §6 claims cite chains, and the key insight (the benefit is capped by an unmeasured share, and the consumer cost comes from cutover style) is not a restatement of the recommendation.

Gate cleared: no Absent verdicts, zero Hand-wavy verdicts.