## Answer

**Recommendation:** Do not approve buying faster CI runners as the primary fix. First instrument the pipeline to find its serial/I/O-vs-parallel split (chain C1); in parallel, run a software/process bundle (caching, test-impact selection, flaky-test quarantine) plus a fast pre-merge gate with a slower post-merge suite, which beats a hardware-only purchase on a locked, weighted, flip-tested comparison (chain C4); use a targeted runner upgrade only for stages confirmed genuinely CPU-bound (chain C1, chain C3).

**Band (from §6):** LOW — every contributing chain (C1, C2, C3, C4) is capped LOW by missing team-specific profiling data and by an unverified interruption-cost mechanism (GT-5?); the qualitative ranking is nonetheless comparatively robust per chain C4's flip test.

**Would change it:** Per-stage CI instrumentation showing this team's actual serial/I/O-vs-parallel-CPU split and flaky-retry contribution (chain C1, chain C3) — and, if that instrumentation instead shows the 47 minutes is genuinely dominated by an already-maximally-parallel, purely CPU-bound stage with no caching/selection headroom, the recommendation reverses in favor of hardware (chain C1, chain C3).

## 1. Problem Essence

**Core problem:** Should this organization direct its next infrastructure-improvement spend toward faster/larger CI runners as the primary fix for a 47-minute pipeline and the merge-batching behavior it has induced, or does a different lever (or ordered combination of levers) deliver more of the actual goal — a pre-merge feedback loop short and reliable enough that developers stop batching — per dollar and per week of engineering time than a hardware purchase alone?

**Success criteria:**
1. The Conclusion section (§6) names a single recommended lever or ordered combination of levers — not a bare "runners: yes/no" verdict — and states, for each lever included or excluded, the specific factor that drove that call.
2. The Conclusion section's `**Recommended approach:**` line names the specific behavioral bar (a stated target duration or equivalent condition) the fix must clear to count as addressing the batching behavior, not only the average-duration metric leadership named.
3. The Conclusion section's `**Confidence:**` line names, for each contributing derivation chain rated below HIGH, the specific unverified input or assumption responsible and the verification that would remove it.
4. The Conclusion section's `**Trade-offs acknowledged:**` line states the condition under which the recommendation reverses — the circumstance under which "buy faster runners" would in fact be the correct primary call.

A skeptic can check all four against §6 directly, without asking this analysis for further clarification.

---

## 2. Assumptions Table

Phase 2 applied the inversion procedure to the claim under test — "buying faster CI runners is the right call" — inverted to "buying faster CI runners does not fix the problem," and enumerated the conditions that would guarantee that inversion. Those failure-guaranteeing conditions populate assumptions A2, A3, A4, A6 and A9 below; the remaining rows come from direct examination of the leadership ask and the cost model built in §4.

| Assumption | Type | Treatment | Verdict | Verification |
|------------|------|-----------|---------|--------------|
| A1: The stipulated 47-minute CI duration and merge-batching behavior described in the prompt accurately characterize this team's actual situation. | untested belief | Verify, or flag unverified; accepted here as the operating premise of a general/hypothetical analysis. | Accept — treated as the scenario's given premise per the domain framing ("reasonable assumptions... should be made explicit and flagged, not treated as given facts"); no specific team or repo was named to verify against. | unverified — flagged (feeds GT-1?) |
| A2: A materially-sized, strictly-serial or I/O-bound portion of the pipeline (checkout, dependency/cache restore, container startup, artifact upload) exists and does not shrink as CPU/core speed increases. | current constraint | Record expiry conditions — what would have to change for this constraint to lift. | Accept — expires only if the org eliminates network/registry/disk I/O from the critical path entirely (e.g., fully pre-warmed, locally-cached, in-memory execution), which is itself a software/infra engineering investment, not a runner-speed purchase. | supported by GT-3 (Amdahl's Law) and GT-4 (Shopify's fixed-overhead stages were shrunk via caching/skip-logic, not compute speed) |
| A3: The team has not already implemented mature build caching, test-impact selection, and parallel test sharding. | untested belief | Verify before committing spend. | Challenge — leadership's framing ("buy faster runners") reads as more consistent with these levers being unexplored than exhausted, but this is not confirmed; if false, the balance shifts toward hardware at the margin (this analysis's stated falsification condition). | unverified — flagged |
| A4: Flaky tests requiring automatic retries contribute meaningfully to the 47-minute duration. | untested belief | Verify via instrumentation. | Challenge — common at this pipeline duration per industry pattern (GT-4: Shopify had to raise test stability from 88% to 97%), but not confirmed for this team. | unverified — flagged |
| A5: A CI duration must fall to roughly 10-15 minutes or below — not merely "somewhat faster" — to change merge-batching behavior. | convention | Explicitly challenge before relying on it; no universally-validated precise threshold exists. | Challenge — supported directionally by GT-4 (Shopify's explicit sub-10-minute p95 target) and by GT-5?'s general interruption-cost research, but the specific 10-15 minute figure for this team is not independently verified. | unverified — flagged; see chain C2 |
| A6: Purchasing faster/larger CI runners requires negligible engineering effort and is effectively a "free" lever compared to software-side fixes. | convention | Explicitly challenge — leadership's implicit framing. | Discard — larger-runner migration still requires workflow reconfiguration and validation for parallel-safety, and it is a recurring cost commitment, not a one-time action; treated in this analysis as a real, if smaller, cost. | contradicted by GT-2 (recurring per-minute billing) via chain C3 |
| A7: The test suite is at least partially parallelizable/shardable. | untested belief | Verify. | Challenge — assumed true to a moderate, bracketed degree (40-80% parallel fraction) for illustrative estimation in chain C3; the true figure for this team is unknown. | unverified — flagged |
| A8: Illustrative team size (~50 developers) and CI run volume (~150 runs/day), used only to size the Fermi bracket in chain C3. | current constraint | Record as an explicit illustrative stand-in with stated expiry. | Accept — accepted only for illustrating order of magnitude; expires the moment a real team's numbers are substituted. | unverified — flagged (illustrative, not sourced) |
| A9: Developer behavior toward CI wait time responds via a fairly sharp threshold (tied to interruption/context-switch cost) rather than as a smooth, continuous function of average duration. | untested belief | Verify. | Challenge — plausible mechanism, partially supported by GT-5?'s general interruption-cost research, but that research concerns general workplace interruptions, not CI-wait specifically, so transfer to this context is untested. | unverified — flagged; live rival noted on chain C2 |
| A10: The relative weights and 1-5 anchor scores assigned to the trade-off criteria in chain C4 (impact, cost, durability, time-to-first-benefit, safety risk, threshold-crossing) reflect this team's actual priorities. | convention | Challenge — a different, still-reasonable weighting could be applied by an actual team. | Challenge — the flip test in chain C4 shows the ranking of hardware-only versus the composite/software options is robust to any single-weight change within the procedure's 1-5 scale, which substantially (though not completely) blunts this convention's fragility. | robustness demonstrated in chain C4 (flip test), not independently sourced |
| A11: An 8-core larger runner (versus a 2-core standard runner) is a representative illustrative choice of hardware upgrade for costing purposes. | convention | Acknowledge as illustrative. | Accept — chosen as a plausible mid-tier upgrade for illustration in chain C3; the qualitative conclusion (cost rises faster than wall-clock time falls, and the result fails to resolve the decision) holds directionally across the other tiers GT-2 lists too, since per-core cost is roughly flat-to-declining while Amdahl's ceiling applies regardless of tier. | derived from GT-2 + GT-3 reasoning |

## 3. Ground Truths

- **GT-1?** The CI pipeline's stated duration is 47 minutes and developers have begun batching merges (combining multiple changes into fewer, larger merge events) specifically to reduce how often they incur that wait. — cited to: the user-supplied problem statement; no independent source was named for this figure. unverified: this is the scenario's stipulated premise, accepted as the operating condition of a general/hypothetical analysis per the domain framing, not independently verified for any named team.

- **GT-2** GitHub-hosted Linux x64 runner pricing scales as follows: 2-core (standard) $0.006/min; 4-core $0.012/min; 8-core $0.022/min; 16-core $0.042/min; 32-core $0.082/min; 64-core $0.162/min. — source: GitHub Docs, "Actions runner pricing" reference; read-at-source: the six per-minute figures above were read directly from the pricing reference table (docs.github.com/en/billing/reference/actions-runner-pricing) via a direct fetch of that page.

- **GT-3** Amdahl's Law: for a task with a proportion P parallelizable and (1-P) strictly serial, the maximum possible speedup from parallelization — including infinite processors or infinite clock speed — is 1/(1-P); the serial fraction sets a hard floor on wall-clock duration regardless of how much parallel compute is applied. — source: formal computer-science theorem (Amdahl, 1967); provenance note: this is a mathematical/definitional identity rather than an empirical claim reported by a document, so it is verified by direct derivation from the definitions of serial and parallel execution time rather than by opening a cited source; it is treated as a physical-law-type ground truth per the Phase 2 classification scheme and is not suffixed `?`. Reduce-to-primitives check: decomposing this claim finds no further constituent to verify — it bottoms out immediately as a mathematical primitive, requiring no additional recursion.

- **GT-4** At Shopify, the core monolith CI pipeline's p95 duration fell from 45 minutes to 18 minutes (with an explicit target of well under 10 minutes p95). The reductions came from: Docker container start time improving from 90s to 25s p95 (disk sizing and read-only cache mounts); a dependency/asset-build step improving from ~5 minutes to ~3 minutes (skipping unchanged work); the share of builds that skip running the full test suite rising from 45% to over 60% (test-impact selection); test stability rising from 88% to 97%; and temporarily quarantining flaky tests alone cutting p95 by 10 minutes (44 to 34 minutes). None of these interventions was a runner-hardware upgrade. — source: Shopify Engineering, "Faster Shopify CI" (shopify.engineering/faster-shopify-ci); read-at-source: figures quoted directly from the article via a direct fetch of that page.

- **GT-5?** Field research by Gloria Mark (UC Irvine) following workers across several days found that, for interrupted work resumed the same day, the average time to return to the original task was approximately 23 minutes 15 seconds — an interval that includes time spent on the interruption itself and on other intervening tasks, not pure idle/lost time. — cited to: UC Irvine ICS reporting and secondary press coverage of Mark's field studies; reported-by-delegate: supplied via web search synthesis of secondary sources; Mark's original dataset/publication was not opened by this analysis.

- **GT-6?** Independently reported benchmarks found remote build caching produced measured time reductions of up to roughly 41% (Gradle projects) and up to roughly 92% (Bazel projects) in tested open-source projects, and a cited Google-internal study associated a 13% build-time reduction with higher developer satisfaction, faster iteration, and more frequent code changes. — cited to: search-engine-synthesized secondary summaries; reported-by-delegate: the underlying Google study and the benchmark write-ups were not opened by this analysis. Used only as non-load-bearing corroborating context (chain C1); no chain head cites this ground truth directly.

- **GT-7?** Broad, long-running industry survey findings (in the DORA "State of DevOps" research tradition) report that organizations with markedly higher deployment frequency also report markedly shorter lead time for changes than lower-performing peers; a specific numeric multiplier for the most recent report year was returned by a web search summary but could not be confirmed against the primary source when checked. — cited to: search-engine-synthesized secondary summaries of DORA reporting; unverified: an attempt was made to open a primary DORA/Google Cloud source for the specific multiplier and it could not be confirmed there; the qualitative ordinal relationship is long-replicated in this literature, but the specific figures are not verified by this analysis. Used only as non-load-bearing corroborating context (§5, Abandoned Reasoning); no chain head cites this ground truth directly.

**Provenance summary:**
```text
?-marked: GT-1, GT-5, GT-6, GT-7 (4 of 7)
Read-at-source: GT-2 — GitHub Docs "Actions runner pricing" reference table, all six per-core-count figures quoted verbatim
Read-at-source: GT-4 — shopify.engineering/faster-shopify-ci, p95/stage figures quoted verbatim
Not read-at-source (definitional, not source-dependent): GT-3 — verified by direct mathematical derivation, see reduce-to-primitives check above
```
No chain in this analysis is rated HIGH (see §4), so the requirement that every unsuffixed ground truth feeding a HIGH-confidence chain name its read-at-source location is vacuously satisfied; GT-2 and GT-4 nonetheless carry named read-at-source locations above as a matter of practice.

## 4. Derivation Chains

**Theoretical-limit technique applied in C1.** Governing hard constraint: Amdahl's Law (GT-3). Ideal bound: the pipeline's strictly-serial/I/O-bound fraction, which no amount of parallel or faster compute can shrink. Best demonstrated: Shopify's real, cited reduction of fixed-overhead stages via caching/skip-logic (GT-4) — an observation, not a calculation. Conventional figure: this team's current 47 minutes (GT-1?). The two gaps (conventional → best-demonstrated-style fix, and best-demonstrated → the Amdahl ideal bound) are both currently unmeasured for this specific pipeline, which is exactly what chain C1's confidence caveat reports.

### Conclusion C1: A hardware-only upgrade has a mathematically fixed ceiling on how much it can shorten this pipeline, and that ceiling is conventionally lowered by software engineering, not compute speed.

GT-3 (Amdahl's Law: serial fraction bounds max speedup) + GT-4 (Shopify: fixed-overhead stages cut via caching/skip-logic, not compute speed)
→ a strictly serial or I/O-bound portion of a CI pipeline — checkout, dependency/cache restore, container startup, artifact upload — does not shrink as core speed or count increases [Assumes: A2]
→ therefore total pipeline duration cannot fall below that serial/I/O-bound portion's size regardless of how fast or numerous the runners are
→ the Shopify case study's largest reductions to exactly this kind of fixed-overhead stage came from caching and skip-logic engineering rather than from purchasing faster compute (GT-4), consistent with independently-reported benchmarks showing up to roughly 92% build-time reductions from remote caching alone (GT-6?)
→ a hardware-only intervention therefore has a mathematically fixed ceiling on its achievable time reduction, and the available evidence suggests that ceiling is conventionally lowered by software engineering rather than by hardware spend

**Pre-check:** head GT-3, GT-4 · ?-marked: none · lowest cited: none · Inputs ceiling: HIGH
**Confidence:** LOW — Inputs are clean (GT-3 is a physical/mathematical law verified by direct derivation; GT-4 is read-at-source), but two other axes are short: Inference rests on `[Assumes: A2]` — that this specific, unnamed team's pipeline actually contains a non-trivial serial/I/O-bound fraction — which is architecturally near-certain in general but unmeasured for this team; verification: instrument the pipeline with per-stage timing (see §6 Recommended approach, step 1). Rivals: a live, unruled-out rival holds that this specific pipeline's serial/I/O floor is negligible (well under 5% of total time), making it almost entirely CPU-bound parallel work; no team-specific profiling data exists in this analysis to settle it either way — see the Falsification condition in the adversarial pass record.

### Conclusion C2: The bar this problem must clear is "CI fast enough to stop batching" (roughly 10-15 minutes), not merely "CI faster than 47 minutes."

GT-4 (Shopify: explicit target of well under 10 minutes p95 for CI) + GT-5? (Gloria Mark et al.: ~23-minute average interruption-recovery time)
→ industry practice treats "well under 15, and ideally under 10, minutes" as the credible target for preserving a tight merge feedback loop, not merely "faster than before" [Assumes: A5]
→ recovering focus after an interruption takes on the order of twenty-plus minutes (GT-5?), so a CI wait long enough to make a developer switch to unrelated work imposes a roughly fixed cost per wait rather than one that scales smoothly with the minutes saved [Assumes: A9]
→ a reduction from 47 minutes to some smaller-but-still-long duration may therefore fail to reduce the number of context-switch events at all, if that smaller duration still comfortably exceeds the switch-triggering interval
→ the behaviorally-relevant bar this problem must clear is therefore closer to "under roughly 10-15 minutes" than to "faster than 47 minutes," and a fix that improves the average without crossing that bar may leave the batching behavior fully intact

**Pre-check:** head GT-4, GT-5? · ?-marked: GT-5? · lowest cited: none · Inputs ceiling: MEDIUM
**Confidence:** LOW — three axes are short. Inputs: capped at MEDIUM by GT-5? (reported-by-delegate; verification: locate and read Mark's original published dataset directly, or replace it with a CI-wait-specific measurement of this team's own context-switch behavior). Inference: hop 2 rests on `[Assumes: A9]` — that developer behavior here follows a threshold shape rather than a smooth one — which is untested for CI-wait specifically (Mark's research concerns general workplace interruption, not CI waiting); verification: instrument merge-frequency against actual CI duration for this team and look for a step change versus a smooth trend. Rivals: a live, unruled-out rival holds that developer behavior responds smoothly and continuously to average wait time rather than via a sharp threshold, in which case any reduction helps proportionally; nothing in this analysis settles between the two models.

### Conclusion C3: A hardware-only upgrade's own cost/benefit bracket cannot resolve whether it clears the behaviorally-relevant bar, even though its dollar cost is modest.

GT-2 (GitHub Actions per-minute pricing by core count) + C1 (hardware has a mathematical ceiling set by the serial/I/O floor) + C2 (the behaviorally-relevant bar is roughly 10-15 minutes, not merely "faster")
→ moving from a 2-core standard runner ($0.006/min) to an 8-core larger runner ($0.022/min) raises the per-minute compute rate by about 3.7x [Assumes: A11]
→ under the ceiling established in C1, an 8-core upgrade speeds up only the parallelizable fraction of the run, not the serial/I/O-bound remainder [Assumes: A7]
→ at an illustrative 40-80% parallel fraction, this model puts the pipeline's wall-clock time between about 14 and 30.5 minutes, with roughly 22.3 minutes at the 60% midpoint
→ over that same bracket the cost per run rises from $0.282 (47 min at $0.006/min) to between roughly $0.31 and $0.67 (at $0.022/min)
→ at an illustrative volume of 150 CI runs/day, that per-run cost increase compounds to a compute-spend increase on the order of one hundred to roughly two thousand dollars a month [Assumes: A8]
→ the bracket's low end (about 14 minutes) sits below the roughly 10-15 minute bar named in C2 while its high end (about 30.5 minutes) sits well above it, so this estimate cannot by itself resolve whether hardware-only clears the bar that actually matters

**Pre-check:** head GT-2, C1 (LOW), C2 (LOW) · ?-marked: none · lowest cited: LOW · Inputs ceiling: LOW
**Confidence:** LOW — capped by the Inputs ceiling: this chain's head cites C1 and C2, both rated LOW, and a chain is rated no higher than the lowest-rated chain its head cites (D-07). Independently, Inference is also short on two counts: `[Assumes: A7]` (the true parallel fraction of this team's suite, bracketed here at 40-80% without measurement; verification: per-stage CI timing plus a controlled shard-count experiment) and `[Assumes: A8]` (illustrative team size/run volume; verification: substitute this team's real developer count and CI run volume). Rivals: a live, unruled-out rival holds that the true parallel fraction is much higher than this bracket (e.g., ~95%), which would make hardware upgrade both cheap and highly effective; no team-specific data available here settles it.

### Conclusion C4: A software/process-led composite, not a hardware-only purchase, is the best available response to the stated problem — a ranking that is robust to how the deciding criteria are weighted.

GT-4 (Shopify: caching/selection/flake-fixing delivered a 60% p95 reduction without new hardware) + C1 (hardware's ceiling is set by an unmeasured serial floor) + C2 (the behaviorally-relevant bar is roughly 10-15 minutes) + C3 (hardware-only's cost/impact bracket straddles that bar and does not resolve the decision)
→ scoring five candidate interventions — hardware-only, a software/process bundle, a pipeline split into fast pre-merge and slow post-merge stages, status quo, and a composite of the bundle plus split with hardware as a secondary lever — against six pre-locked weighted criteria (impact, cost, durability, time-to-first-benefit, safety risk, and whether the fix crosses the behavioral bar) ranks the composite highest (107) and hardware-only fourth of five (68) [Assumes: A10]
→ a flip test shows no single criterion's weight, moved anywhere within the procedure's 1-5 scale, reverses hardware-only's low rank relative to the software-led options
→ that ranking is therefore not an artifact of the particular weights chosen, but a comparatively robust result
→ hardware-only is therefore not the best available response to the stated problem under any reasonably-weighted version of the criteria that matter, and a composite led by software and process fixes, with hardware retained only as a secondary and targeted lever, dominates it

**Second-order effects (both lenses walked), extending this chain in place:**
→[2nd] leadership and the platform/infra team commit to a recurring compute-cost increase and may treat the purchase as "solved," reducing pressure to fund the software/process track that GT-4 shows produces the larger, more durable gain (actor lens: leadership, platform/infra team)
→[3rd] if that deprioritization happens, the codebase and test suite continue growing while the hardware ceiling from C1 does not move, so pipeline duration and batching both tend to re-emerge on a similar timeframe, while the org has meanwhile normalized "buy more hardware" as its default response to slowness (time lens: few-cycles-to-long-term; actor lens: developers, who attribute continued pain to "runners still too slow" and escalate further hardware asks — a ratchet; and the competitor/talent market, where teams that invested in build/test engineering compound a release-cadence advantage and may attract engineers who value tooling quality)
Contradiction check: neither extension contradicts a named ground truth, so no return to Phase 2 is triggered; the leadership-declares-victory effect does, however, work against this analysis's own Phase 1 success criterion of durably stopping batching — this is reported as an undermining second-order effect and is the basis for Disposition Cluster 3 in the adversarial pass record below, not a chain-invalidating contradiction.

**Pre-check:** head GT-4, C1 (LOW), C2 (LOW), C3 (LOW) · ?-marked: none · lowest cited: LOW · Inputs ceiling: LOW
**Confidence:** LOW — capped by the Inputs ceiling: this chain's head cites C1, C2 and C3, all rated LOW (D-07). Independently, Inference is short on `[Assumes: A10]` (the weights and anchors used to score the five options reflect a plausible but unvalidated judgment call about this team's priorities; verification: have the actual accountable team re-run the scoring with its own locked weights) — though the flip test materially bounds this shortfall by showing the ranking survives any single-weight change within the procedure's scale. Rivals: the strongest rival — "buy the runners now as a fast, low-organizational-risk stopgap while separately starting the software track" — is addressed, not left live: it is ruled out as a reason to lead with hardware because the composite option already scores nearly as well on time-to-first-benefit (4) as hardware-only (5) while dominating on every other criterion (§5, Abandoned Reasoning, "Leadership's implicit 'hardware now' rival").

## 5. Abandoned Reasoning

### Dead End: Citing a reported Uber CI build-time improvement as corroborating evidence

**What was tried:** Considered citing a reported figure (CI build time cut from roughly 25 to 16 minutes via caching and test-shard parallelization) as a second corroborating case study alongside Shopify's.

**Why abandoned:** The only source located for this figure was a search-engine synthesis of what appears to be an individual's resume bullet point, not a primary engineering publication. Its provenance could not be lifted above "unverified" — it is weaker than even a delegate-reported ground truth, since there is no named institutional source to eventually open and check.

**What it ruled out:** Prevents this analysis (or a future one reusing it) from re-citing that figure as though it carried institutional backing. GT-2 (GitHub Actions pricing) and GT-4 (Shopify's case study) remain this analysis's verified evidentiary anchors instead.

### Dead End: Mandating more frequent merges without shortening CI

**What was tried:** Considered recommending a policy mandate ("merge at least once per day") as a direct fix for the batching behavior, without touching pipeline duration at all.

**Why abandoned:** This treats developers' batching as an irrational habit rather than as adaptive behavior in response to a real, measured cost (GT-1?). Forcing more frequent merges into a still-47-minute wait would increase, not decrease, total wait-time exposure per developer — it multiplies the number of times each developer must clear the same unshortened gate. Chain C2's threshold reasoning shows the actual lever that matters is crossing the behaviorally-relevant duration bar, which this option does not touch.

**What it ruled out:** A policy-only fix that ignores the underlying cost driver, which chain C2 establishes as the actual lever, and which this option leaves completely unaddressed.

### Dead End: Accepting 47 minutes and reframing batching as acceptable risk management

**What was tried:** Considered the rival position that the status quo is fine — that batching is a rational risk-management adaptation and no intervention is needed at all.

**Why abandoned:** This is inconsistent with the stipulated scenario itself (GT-1?), in which leadership already treats the situation as a problem worth solving, and it is the position formally scored as option "status quo" in chain C4's trade-off, where it ranked last (44 of a possible high near 107) on every criterion except pure dollar cost. It receives only weak, non-load-bearing corroboration from broadly-reported industry findings that shorter lead times correlate with better delivery outcomes (GT-7?), which this analysis could not verify at the primary source and does not rely on for this ruling.

**What it ruled out:** A "do nothing" conclusion, which chain C4's own scoring — not GT-7?'s unverified multipliers — is what actually rules it out.

### Dead End: Recommending a full pipeline/toolchain rearchitecture

**What was tried:** Considered scoring a sixth option — rebuilding the CI pipeline on a different build system or language toolchain — as a "nuclear option" alongside the five options in chain C4.

**Why abandoned:** This option fails the implicit must-have that any candidate be actionable within weeks, not require a multi-quarter platform rewrite, given that developers are already adapting workaround behavior now. It was excluded before scoring rather than scored and ranked last.

**What it ruled out:** A sixth column in chain C4's trade-off matrix that would have added scoring overhead without changing the ranking, since this option would fail the same must-have that made it a non-candidate in the first place.

### Dead End: Leadership's implicit "hardware now, cheap optionality" rival to the trade-off ranking

**What was tried:** Considered the argument that hardware-only deserves to win, or at least to be done first, because it is faster to deploy and carries lower organizational risk (no process change, no cross-team coordination) than the software/process track — a real-options argument for taking the lower-expected-value-but-faster action first.

**Why abandoned:** Chain C4's own scoring already prices this argument: hardware-only's time-to-first-benefit score (5) is only one point above the composite's (4), while the composite dominates hardware-only on every other criterion (impact, durability, safety risk, threshold-crossing) and roughly ties it on cost. The speed advantage hardware-only offers is too small, relative to the composite's advantages elsewhere, to justify leading with hardware alone — and the composite explicitly retains a fast-moving component (the pipeline split) that captures most of hardware-only's speed advantage without its ceiling and cost problems.

**What it ruled out:** Treating "hardware is faster to deploy" as a reason to lead with hardware-only; chain C4 shows the composite captures nearly the same speed advantage while dominating everywhere else.

---

## 6. Conclusion

**Recommended approach:** Do not approve a blanket "buy faster CI runners" purchase as the primary or sole response. First, instrument the pipeline to measure its serial/I/O-bound-versus-parallel/CPU-bound split and its flaky-retry contribution, because a hardware-only fix has a mathematical ceiling set by the pipeline's non-parallelizable portion and its payoff cannot be sized without that data (chain C1). In parallel, pursue the software-and-process bundle (build/dependency caching, test-impact selection, flaky-test quarantine) and split the pipeline into a fast pre-merge gate plus a slower post-merge/nightly suite; against a locked, weighted comparison whose ranking survives every single-criterion reweighting the procedure allows, this combination dominates a hardware-only purchase (chain C4). Treat a targeted runner upgrade as a secondary lever, applied only to stages instrumentation confirms are genuinely CPU-bound and already well-parallelized (chain C1, chain C3).

**Key insight:** The leadership question conflates "make CI faster" with "make CI fast enough to stop batching" — these are different bars. Batching is better modeled as crossing a threshold tied to context-switch cost than as responding smoothly to average duration, so a hardware upgrade's plausible wall-clock gain can land on either side of the bar that actually matters, depending on facts nobody has yet measured (chain C2, chain C3), while the one verified real-world precedent available shows the largest and most durable gains came from caching, test-selection and flake-fixing, not compute speed (chain C1, chain C4).

**Trade-offs acknowledged:** The recommended path costs more total engineering time up front than simply approving a purchase order, and in the worst case delays relief by weeks rather than days (chain C4). It also requires new operational discipline — fast-revert-on-post-merge-failure for the pipeline split — that a hardware-only path would not have required (chain C4). If pipeline instrumentation later shows the 47 minutes is genuinely dominated (e.g., over 80%) by an already-maximally-parallelized, purely CPU-bound stage with no caching, test-selection, or sharding headroom, hardware becomes the correct primary lever instead — this analysis does not rule that scenario out, it rules out choosing hardware without first checking for it (chain C1, chain C3).

**Pre-check:** head C1 (LOW), C2 (LOW), C3 (LOW), C4 (LOW) · ?-marked: none · lowest cited: LOW · Inputs ceiling: LOW
**Confidence:** LOW — every contributing chain is capped LOW by a combination of: (i) this being a general analysis with no team-specific profiling data — chains C1, C3 and C4 all rest on an unverified assumption about this specific team's serial/parallel split (A2/A7); verification: instrument the pipeline, per Recommended approach step 1; (ii) chain C2's use of GT-5? (Gloria Mark's general interruption research, not CI-wait-specific); verification: a controlled before/after measurement of this team's merge frequency against actual CI duration; and (iii) live, unsettled rivals named on C1 and C2 (a negligible serial floor; a smooth rather than threshold-shaped behavioral response) that no evidence available to this analysis rules out. Despite the LOW numeric band, the qualitative ranking behind the recommendation — that hardware-only underperforms a software/process-led composite — is comparatively robust: chain C4's flip test shows no single-criterion reweighting within the trade-off procedure's 1-5 scale reverses that ordering.

## Appendix — process output

## §6→§4 closure ledger (process output)

- "Do not approve a blanket "buy faster CI runners" purchase as the primary or sole response... instrument the pipeline... pursue the software-and-process bundle... split the pipeline... treat a targeted runner upgrade as a secondary lever" → chains C1, C3, C4 ✓ (inline)
- "The leadership question conflates "make CI faster" with "make CI fast enough to stop batching"... the one verified real-world precedent... came from caching, test-selection and flake-fixing, not compute speed" → chains C1, C2, C3, C4 ✓ (inline)
- "The recommended path costs more total engineering time up front... requires new operational discipline... If pipeline instrumentation later shows the 47 minutes is genuinely dominated... hardware becomes the correct primary lever instead" → chains C1, C3, C4 ✓ (inline)
- "**Pre-check:** head C1 (LOW), C2 (LOW), C3 (LOW), C4 (LOW)..." → chains C1, C2, C3, C4 ✓ (inline)
- "**Confidence:** LOW — every contributing chain is capped LOW by..." → chains C1, C2, C3, C4 ✓ (inline)

All five §6 claims (Recommended approach, Key insight, Trade-offs acknowledged, Pre-check, Confidence) carry inline chain citations; no claim required ledger discharge and none was cut.

## Techniques not applied (process output)

- five-whys (causal mode) — not applicable — no team-specific diagnostic data exists yet to drill a causal chain into; this analysis instead recommends the instrumentation step (§6, Recommended approach) that would supply the data a causal five-whys would need.
- fishbone — not applicable — the relevant cause-breadth for this decision (serial/IO overhead, flakiness, absent caching/selection/sharding, suite growth) was already surfaced directly through assumption enumeration (§2) and the inversion procedure's failure-conditions; a dedicated 6M/8P/4S fishbone would relabel the same candidates under generic categories without adding a category this problem actually needs.
- inversion, second invocation point (Phase 5 adversarial technique) — not applicable — the headline conclusion is a plan/recommendation, not a bare claim, so the decision rule routes Phase 5's adversarial technique to pre-mortem instead; inversion fired at its first invocation point (Phase 2, populating assumptions A2/A3/A4/A6/A9).
- theoretical-limit, first invocation point (Phase 1 essence reframe) — not applicable — the essence question here is a resource-allocation decision between named levers, not a claim about whether "47 minutes" is itself a convention versus a physical bound; that question is instead resolved substantively within Phase 4 (chain C1), theoretical-limit's second invocation point, where it fired.

(estimate, trade-off, second-order, and theoretical-limit's second invocation point all fired — chain C3, chain C4, chain C4's second-order extension, and chain C1 respectively — so no not-applicable line is required for them.)

## Assumption Audit scan (process output)

| Chain | Step | Step Text (brief) | Assumption surfaced? | Added to Table? |
|-------|------|--------------------|-----------------------|------------------|
| C1 | 1 | serial/I/O portion does not shrink with core speed | A2 (current constraint) | yes (already in Table) |
| C1 | 2 | therefore duration floor exists regardless of runner speed | none | n/a |
| C1 | 3 | Shopify's fixed-overhead gains came from caching/skip-logic, not compute | none (GT-4/GT-6? direct) | n/a |
| C1 | 4 | hardware-only ceiling is conventionally lowered by software, not hardware | none | n/a |
| C2 | 1 | industry target of well under 15/10 minutes p95 | A5 (convention) | yes (already in Table) |
| C2 | 2 | interruption recovery ~20+ min implies roughly-fixed cost per wait | A9 (untested belief) | yes (already in Table) |
| C2 | 3 | smaller-but-still-long duration may not reduce context-switch events | none | n/a |
| C2 | 4 | behaviorally-relevant bar is ~10-15 min, not "faster than 47" | none | n/a |
| C3 | 1 | 8-core tier raises per-minute rate ~3.7x | A11 (convention) | yes (already in Table) |
| C3 | 2 | 8-core upgrade speeds only the parallelizable fraction | A7 (untested belief) | yes (already in Table) |
| C3 | 3 | 40-80% parallel fraction implies 14-30.5 min bracket | none new (uses A7) | n/a |
| C3 | 4 | cost per run rises to $0.31-$0.67 | none new (arithmetic on GT-2) | n/a |
| C3 | 5 | at illustrative 150 runs/day, monthly delta is $100-$2,000 | A8 (current constraint) | yes (already in Table) |
| C3 | 6 | bracket straddles the C2 bar and does not resolve the decision | none | n/a |
| C4 | 1 | trade-off scoring ranks composite 107, hardware-only 68 (4th of 5) | A10 (convention) | yes (already in Table) |
| C4 | 2 | flip test: no single weight change within 1-5 scale reverses the ranking | none new | n/a |
| C4 | 3 | ranking is not an artifact of chosen weights | none | n/a |
| C4 | 4 | hardware-only is not the best available response; composite dominates | none | n/a |
| C4 | 5 (2nd-order) | leadership/platform may treat hardware purchase as "solved," deprioritizing the software track | none new (uses established scenario facts) | n/a |
| C4 | 6 (3rd-order) | suite growth + unmoved hardware ceiling re-creates the problem; org normalizes "buy hardware" as default; developers escalate; competitors/talent compound an advantage | none new | n/a |

Every named derivation-chain step from §4 has a row above, in order, with no step skipped. All assumptions surfaced during this scan (A2, A5, A7, A8, A9, A10, A11) were already present in the §2 Classified Assumptions Table at authoring time — this scan confirms exhaustiveness rather than adding new rows.

## Adversarial pass (process output)

**Recompute.** Pricing ratios: $0.022 / $0.006 = 3.667 ("about 3.7x") ✓. Per-core-minute cost across GT-2's tiers: 2-core $0.0030, 4-core $0.0030, 8-core $0.00275, 16-core $0.002625, 32-core $0.0025625, 64-core $0.0025313 — confirms per-core cost is flat-to-slightly-declining as tier rises, not rising. C3 bracket at 80% parallel: serial 9.4 min + parallel 37.6/8 = 4.7 min → 14.1 min ✓. At 40% parallel: serial 28.2 min + parallel 18.8/8 = 2.35 min → 30.55 min ✓. At 60% (central): serial 18.8 + parallel 28.2/8 = 3.525 → 22.325 min ("roughly 22.3") ✓. Cost per run: 47 min × $0.006 = $0.282 (baseline); 14.1 min × $0.022 = $0.310; 30.55 min × $0.022 = $0.672 → range "$0.31 to $0.67" ✓. Monthly delta at 150 runs/day: low end (0.310-0.282)×150×30 = $126/mo; high end (0.672-0.282)×150×30 = $1,755/mo → "one hundred to roughly two thousand dollars a month" ✓. C4 weighted totals recomputed from the criterion-by-criterion scores stated in this analysis's own working: hardware-only 5(2)+3(3)+4(2)+3(5)+4(4)+5(2)=10+9+8+15+16+10=68 ✓; software bundle 5(5)+3(4)+4(5)+3(3)+4(3)+5(5)=25+12+20+9+12+25=103 ✓; pipeline split 5(5)+3(3)+4(4)+3(4)+4(2)+5(5)=25+9+16+12+8+25=95 ✓; status quo 5(1)+3(5)+4(1)+3(1)+4(3)+5(1)=5+15+4+3+12+5=44 ✓; composite 5(5)+3(3)+4(5)+3(4)+4(4)+5(5)=25+9+20+12+16+25=107 ✓. All figures recompute to the values stated in §4.

**Sensitivity.** The single most consequential unresolved input across the whole analysis is this team's actual serial-vs-parallel and CPU-vs-I/O split (assumptions A2/A7), which is `?`-adjacent in effect even though it is recorded as "current constraint"/"untested belief" rather than as a `GT-N?`: it directly drives chain C1's ceiling, chain C3's bracket, and — through both — chain C4's ranking. It is not `GT-N?`-marked because no ground truth asserts a specific value for it; instead the entire analysis brackets around it. Verification: per-stage CI instrumentation (§6, Recommended approach, step 1) resolves this directly and is the single highest-leverage next action in the whole analysis.

**Rival.** Headline rival: "hardware-only, full commitment, no software track" — ruled out by chain C4's weighted ranking (68 vs. 107) and its flip test (§5, "Leadership's implicit 'hardware now, cheap optionality' rival"). Chain-level rivals: C1 (negligible serial floor) and C2 (smooth rather than threshold-shaped behavioral response) are named live on their own confidence lines above and are not ruled out by any evidence available to this analysis; C3 (much higher true parallel fraction than bracketed) is likewise named live on its own confidence line.

**Premise.** It is twelve months from now. The organization followed the recommended plan — instrument, run the software/process bundle, split the pipeline, apply hardware only where confirmed CPU-bound — and it has already failed: developers are still batching merges and the pipeline still effectively gates merges for 40-plus minutes.

**Causes** (unfiltered, generated from four viewpoints before any grouping):
- Build-engineer viewpoint: instrumentation was added but nobody acted on the data because it had no executive owner; the software-bundle project was deprioritized in favor of feature work since it carried no external deadline; test-impact selection was implemented naively, skipped a test that should have caught a regression, and leadership mandated reverting to "run everything," erasing the gains; sharding introduced cross-shard shared-state flakiness that added new instability.
- Developer viewpoint: the pipeline-split's fast gate was defined too narrowly (excluded checks developers actually trust), so developers kept waiting for the full suite anyway out of caution; post-merge failures on main became frequent and the revert-and-fix cycle felt slower and more public than the old wait, so developers quietly reverted to batching to avoid "being the one who broke main"; the fast gate's scope crept upward over time (more checks added "just to be safe") until it was 40 minutes again.
- Leadership/budget-owner viewpoint: the software-bundle project ran longer than estimated (a well-known pattern for this class of work) and, growing impatient, leadership approved the runner upgrade anyway mid-project "just in case," compounding recurring cost without compounding benefit; success was never measured against the actual behavioral target (merge-batching rate), only against average pipeline duration, so nobody could tell whether the plan had actually worked, and the initiative quietly stalled.
- Competitor/adversarial viewpoint: a rival team that invested consistently in build/test engineering now ships multiple times a day while this organization still debates infrastructure spend; engineers who value tooling quality notice the gap and some leave for the faster-moving competitor, compounding the original problem with an attrition problem.

**Clusters** (structural weaknesses the causes above fall into):
- Cluster 1 — "Gate scope creep and trust erosion" (bears on: chain C4's safety-risk score for the pipeline-split option; chain C2's threshold reasoning). Disposition: named plan change — require a written "fast-gate charter" fixing exactly what belongs in the pre-merge gate, changes to which are explicitly reviewed, paired with automated fast-revert/rollback tooling delivered as a first-class part of the pipeline-split work rather than an afterthought; track gate duration itself as an SLO with an alert if it creeps above target.
- Cluster 2 — "Optimistic engineering estimates and project deprioritization" (bears on: chain C4's cost and time-to-first-benefit scores for the software-bundle and composite options). Disposition: named plan change — timebox the software-bundle work with an executive-visible milestone (for example, "flaky-test quarantine live in two weeks," mirroring GT-4's staged Shopify rollout) so it carries the same visibility pressure as a hardware purchase order and cannot be silently bumped by feature work.
- Cluster 3 — "No behavioral success metric" (bears on: chain C2 directly; the Phase 1 essence statement's success criteria). Disposition: named plan change — instrument and report "PRs per developer per week" and "commits per merge" as explicit tracked metrics alongside raw pipeline duration from day one, so the plan's actual target (behavior, not just minutes) is measured and visible, not inferred after the fact.
- Cluster 4 — "Hardware spend as an anxiety purchase mid-project" (bears on: chain C3; chain C4's cost score for hardware-only). Disposition: accepted risk with a named mitigation — pre-approve a small, capped "targeted runner upgrade" budget as an explicit, already-planned part of the composite (per §6, Recommended approach, step 3), so that impulse is channeled into the instrumentation-gated lever the plan already contains rather than spent on an uncontrolled parallel purchase.

**Falsification.** This conclusion is false if pipeline instrumentation shows the 47 minutes is genuinely dominated (for example, over 80%) by an already-maximally-parallelized, purely CPU-bound stage with no viable caching, test-selection, or sharding headroom — in that specific case, upgrading runner hardware is the correct primary lever, not a secondary one.

## Self-audit scan (process output)

| Chain | Chain Head (brief) | Form conforming? | Rule applied | Dependency clean? | Band | Act attempted? | Edges fired |
|-------|---------------------|-------------------|---------------|--------------------|------|-----------------|-------------|
| C1 | GT-3 + GT-4 | yes | n/a | yes | LOW | yes | none |
| C2 | GT-4 + GT-5? | yes | n/a | yes | LOW | yes | none |
| C3 | GT-2 + C1 + C2 | yes | n/a | yes | LOW | yes | none |
| C4 | GT-4 + C1 + C2 + C3 | yes | n/a | yes | LOW | yes | none |

| §6 Span (brief) | Construct | Claim under R11? | R11 clause applied | Chain cited |
|-------------------|-----------|-------------------|----------------------|---------------|
| Recommended approach | bold lead-in | yes | colon closes bold span, assertion follows on same line | C1, C3, C4 |
| Key insight | bold lead-in | yes | colon closes bold span, assertion follows on same line | C1, C2, C3, C4 |
| Trade-offs acknowledged | bold lead-in | yes | colon closes bold span, assertion follows on same line | C1, C3, C4 |
| Pre-check line | bold lead-in | yes | colon closes bold span; Pre-check is itself a Conclusion-section claim per the pre-check-line rule | C1, C2, C3, C4 |
| Confidence | bold lead-in | yes | colon closes bold span, assertion follows on same line, names each below-HIGH chain | C1, C2, C3, C4 |

Scan complete: 4 chain rows, one per section-4 chain block in order; 5 section-6 rows, one per construct in order — 5 claims under R11, 0 excluded. 0 chains malformed, 0 claims untraced.

## Self-Audit Gate (process output)

**Criterion 1: Identify Essence**
Quoted span: "Should this organization direct its next infrastructure-improvement spend toward faster/larger CI runners as the primary fix for a 47-minute pipeline and the merge-batching behavior it has induced, or does a different lever (or ordered combination of levers) deliver more of the actual goal... per dollar and per week of engineering time than a hardware purchase alone?" / Success criterion 2: "The Conclusion section's `**Recommended approach:**` line names the specific behavioral bar... the fix must clear to count as addressing the batching behavior, not only the average-duration metric leadership named."
Band: **Rigorous**
Justification: the Essence Statement names the underlying resource-allocation decision rather than restating the prompt's triggering event, and each success criterion is a verb+subject+outcome triplet checkable directly against a named bold lead-in in §6 without further interpretation.

**Criterion 2: Challenge Assumptions**
Quoted span (Assumption Audit scan): "Every named derivation-chain step from §4 has a row above, in order, with no step skipped. All assumptions surfaced during this scan (A2, A5, A7, A8, A9, A10, A11) were already present in the §2 Classified Assumptions Table at authoring time..."
Band: **Rigorous**
Justification: all eleven rows use the four-type scheme, Verdict cells use the Accept/Challenge/Discard token-plus-em-dash form throughout, several rows are Challenged or Discarded rather than blanket-Accepted, unverified rows read "unverified — flagged," and the Assumption Audit scan confirms exhaustive coverage of every named chain step with no new row required.

**Criterion 3: Establish Ground Truths**
Quoted span: "?-marked: GT-1, GT-5, GT-6, GT-7 (4 of 7) / Read-at-source: GT-2 — GitHub Docs... / Read-at-source: GT-4 — shopify.engineering/faster-shopify-ci..." — enumerated GT-1, GT-5, GT-6, GT-7; the Ground Truths list carries `?` on exactly those four IDs and no others.
Band: **Rigorous**
Justification: all seven IDs are stable and match the identifiers cited in §4's chain heads; every unsuffixed GT (GT-2, GT-3, GT-4) carries either a named read-at-source location or an explicit definitional-provenance note for GT-3; the `?` enumeration matches the list on inspection; since no chain in this analysis is rated HIGH, the "every unsuffixed GT feeding a HIGH-confidence chain names its read-at-source location" clause is vacuously satisfied and does not apply.

**Criterion 4: Reason Upward**
Quoted span (self-audit scan, chain-form table): "C1 | GT-3 + GT-4 | yes | n/a | yes | LOW | yes | none" and equivalent rows for C2, C3, C4 — all four chains score `yes` on Form conforming and `yes` on Dependency clean. Quoted span (analysis text, Abandoned Reasoning): five dead ends each documented with What-was-tried / Why-abandoned / What-it-ruled-out, e.g. "The only source located for this figure was a search-engine synthesis of what appears to be an individual's resume bullet point, not a primary engineering publication."
Band: **Rigorous**
Justification: every conclusion in §6 has exactly one chain in §4, every chain's self-audit-scan row reads conforming and dependency-clean, each chain contains multiple genuine intermediate steps, every chain step introducing a new assumption carries an inline `[Assumes: A-N]` tag per the Assumption Audit scan, no analogy is used as standalone evidence (GT-4's Shopify data is always cited to GT-4 rather than offered as "industry does X"), and Abandoned Reasoning documents five specific, non-generic dead ends rather than using the escape valve.

**Criterion 5: Validate**
Quoted span: "**Confidence:** LOW — capped by the Inputs ceiling: this chain's head cites C1 and C2, both rated LOW, and a chain is rated no higher than the lowest-rated chain its head cites (D-07). Independently, Inference is also short on two counts: `[Assumes: A7]`... and `[Assumes: A8]`... Rivals: a live, unruled-out rival holds that the true parallel fraction is much higher than this bracket..." (chain C3's confidence line) — plus the Adversarial pass record's Falsification line: "This conclusion is false if pipeline instrumentation shows the 47 minutes is genuinely dominated... by an already-maximally-parallelized, purely CPU-bound stage with no viable caching, test-selection, or sharding headroom..."
Band: **Rigorous**
Justification: every chain's confidence line names its specific weak link(s) by axis and by ID, no chain rated HIGH consumes a `GT-N?` input (indeed no chain is rated HIGH at all, so the unverified-input-HIGH prohibition is never at risk), C3 and C4 are correctly capped at the lowest-rated chain their heads cite, the Conclusion's own LOW rating matches its weakest contributing chains, and the adversarial pass record is complete: Recompute, Sensitivity, Rival, Premise, Causes (four viewpoints), Clusters (each citing the chain it bears on), Disposition (each cluster given a named plan change or an accepted risk with a named mitigation), and Falsification are all present with content.

**Criterion 6: Conclusion-to-Ground-Truth Traceability**
Quoted span (self-audit scan, claim-inventory table): "Recommended approach | bold lead-in | yes | colon closes bold span, assertion follows on same line | C1, C3, C4" and the corresponding rows for Key insight, Trade-offs acknowledged, Pre-check line, and Confidence — all five rows cite at least one chain and none read "none — untraced." Quoted span (analysis text, Key Insight): "The leadership question conflates 'make CI faster' with 'make CI fast enough to stop batching' — these are different bars."
Band: **Rigorous**
Justification: every §6 claim traces inline to a specific named §4 chain per the claim-inventory table, no claim reads "none — untraced," §6 introduces no reasoning absent from §4, and the Key Insight states a non-obvious finding (the threshold-versus-average conflation) rather than restating the Recommended approach's action items.

**Gate result:** No criterion scored Absent; zero criteria scored Hand-wavy (all six scored Rigorous). Both gate conditions are cleared on the first pass — no Fix/Repeat re-perception pass was required.

