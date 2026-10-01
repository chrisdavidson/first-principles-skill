**Disclosed:** The Self-Audit Gate's Fix/Repeat edge fired once. On the first scoring pass, Criteria 3 and 4 scored Hand-wavy: two read-at-source ground truths fed only MEDIUM chains, and C6 had assumption steps without `[Assumes:]` marks. The fix added chains C7 and C8 and the missing marks, then the gate was re-scored; details are in the appendix.

## Answer

**Recommendation:** Do not migrate to microservices to fix deploy speed. Keep the monolith: first measure what decides when a deploy happens, then split the tests across runners, use rolling restarts, and deploy each merge (chain C6).

**Band (from §6):** MEDIUM (chain C6)

**Would change it:** CI stage timings and the deploy log. Pipeline utilisation above about 80%, or tests below half of the 45 minutes, would reopen the case (chain C1, chain C3).

## 1. Problem Essence

**Core problem:** What actually limits how quickly a merged change reaches customers on this platform, and which intervention removes that limit at the lowest cost and risk — given that "deploys are too slow" can mean either that each deploy takes too long (pipeline latency, 45 min) or that too few deploys happen (throughput, 2/day), and those two readings call for different fixes?

The triggering event is leadership's conclusion ("we need microservices"); that is a proposed solution, not the question. The question is the binding constraint on merge-to-production speed.

**Success criteria:**

1. The answer separates pipeline duration from deploy frequency and from merge-to-production lead time, with the arithmetic shown and recomputed for each.
2. The answer names the binding constraint the given figures support, and states which measurement would confirm or overturn it.
3. The recommended intervention, costed in engineer-months against the team's annual capacity, improves merge-to-production lead time by more than it costs, compared on the same process basis for every option considered.
4. The recommendation does not introduce new correctness risk into checkout without saying so and pricing it.
5. The option set includes keeping things as they are and at least one combination of options, so the answer is not forced to be "microservices: yes/no".

## 2. Assumptions Table

Assumptions are labelled A-1 … A-21 inside the Assumption cell; chains refer to them as `[Assumes: A-N]`. Rows A-6 to A-13, A-15, A-16 and A-22 were surfaced by the Phase 4 Assumption Audit and added back here.

| Assumption | Type | Treatment | Verdict | Verification |
|------------|------|-----------|---------|--------------|
| A-1: "Deploys are too slow" means the 45-minute pipeline is too long | untested belief | Verify or flag | Challenge — the phrase mixes up latency (45 min per deploy) and throughput (2 deploys/day); C1 and C2 show the pipeline accounts for about 27% of merge-to-production time | Derived in C1, C2 from GT-1?, GT-2? |
| A-2: Splitting into microservices shortens merge-to-production time | untested belief | Verify or flag | Challenge — true only if (a) each service's pipeline is shorter and (b) the release process changes; (b) is available to the monolith too (C2, C6) | Derived; unverified — flagged |
| A-3: Every deploy must run the whole test suite on one runner, in series | convention | Challenge before use | Discard — splitting tests across runners and choosing tests by what changed are standard practice; nothing physical requires serial execution (GT-8) | GT-8 (arithmetic identity) |
| A-4: Every deploy needs a coordinated full-application restart | convention | Challenge before use | Discard — Puma's phased restart replaces workers one at a time while the rest keep serving (GT-10), provided A-13 holds | GT-10 read at source |
| A-5: The reported figures (45 min, 2/day, 12 engineers, ~350 KLOC) are accurate | untested belief | Verify or flag | Accept — used as GT-1? to GT-5?; no CI or deploy log was supplied to check them | unverified — flagged |
| A-6: Deploys happen inside an 8-hour (480-minute) working window | convention | Challenge before use | Accept — a business-hours window is the conservative choice; a 24-hour window (1,440 min) only makes the pipeline less binding | Used in C1, C3; unverified — flagged |
| A-7: Merges arrive roughly evenly through the day and the 2 deploys are evenly spaced | untested belief | Verify or flag | Accept — gives a mean wait of half the interval between deploys (GT-7); clustered merges change the wait but not the order of magnitude | unverified — flagged |
| A-8: Running tests takes 50–80% of the 45-minute pipeline | untested belief | Verify or flag | Accept — for bracketing only; a stage-by-stage CI timing breakdown settles it | unverified — flagged |
| A-9: The suite splits across 4–8 runners with about 2 min of setup per runner and no order-dependent tests | untested belief | Verify or flag | Accept — for bracketing only; a test suite six years old usually has some order-dependent tests to fix first | unverified — flagged |
| A-10: Extracting the four domains into services costs 24–144 engineer-months (2–6 engineers for 12–24 months), and splitting tests plus phased restarts costs 1–6 engineer-months (1–2 engineers for 1–3 months) | untested belief | Verify or flag | Accept — as a Fermi bracket, not a quote; no comparable project is used as evidence | unverified — flagged |
| A-11: 12 engineers supply 144 engineer-months of capacity a year | convention | Challenge before use | Accept — this is an upper bound (it ignores support, on-call, leave); less real capacity makes the migration a larger share, which strengthens C5 | Arithmetic: 12 × 12 = 144 |
| A-12: A checkout today reads and writes cart, catalog (price/stock) and fulfillment data in one database transaction | untested belief | Verify or flag | Accept — the default for a Rails monolith covering all four; a code read of the checkout service object settles it | unverified — flagged |
| A-13: Schema migrations can be written so old and new code run side by side (expand/contract) | untested belief | Verify or flag | Accept — required for rolling restarts; a discipline, not a rewrite | unverified — flagged |
| A-14: Faster merge-to-production has business value here | untested belief | Verify or flag | Accept — this is the premise of leadership's request; if false, the status quo is fine | unverified — flagged |
| A-15: About 12 merges a day (roughly one per engineer) | untested belief | Verify or flag | Accept — for the capacity check in C3; the merge log settles it | unverified — flagged |
| A-16: Fulfillment is the most loosely coupled domain (it runs after the order is placed and can be asynchronous) | untested belief | Verify or flag | Accept — only for scoring option D; a code read settles it | unverified — flagged |
| A-17 (inversion): Most of the 45 min goes to work that microservices would remove, such as tests unrelated to the changed domain | untested belief | Verify or flag | Challenge — if true, choosing tests by what changed removes the same work without splitting the code into services (C3) | unverified — flagged |
| A-18 (inversion): 12 engineers can run several separately deployed services, each with its own monitoring, alerts and on-call | current constraint | Record expiry | Challenge — expires if the team grows to several separate teams or gains a platform team; until then GT-9's operational cost falls on the same 12 people | GT-9 read at source |
| A-19: The 2-deploys/day cap is set by process (restart coordination, release batching), not by pipeline capacity | untested belief | Verify or flag | Accept — as the leading hypothesis, supported by C1's 18.75% pipeline utilisation; the deploy log and the release procedure settle it | Derived in C1; unverified — flagged |
| A-22: Puma runs two or more workers (or the app runs on two or more instances) | untested belief | Verify or flag | Accept — the usual production setup; a one-worker deployment has no one left serving during a restart, which is why C7 states it as a condition | unverified — flagged |
| A-20: Work W split across N independent runners takes at least W/N wall-clock time | physical law | Accept as GT candidate | Accept — arithmetic identity; promoted to GT-8 | Definition |
| A-21: Merge-to-production lead time = time waiting for a deploy + pipeline duration | physical law | Accept as GT candidate | Accept — a definition (it partitions the elapsed time); promoted to GT-7 | Definition |

**Inversion applied to leadership's claim (Phase 2).** Claim: "Moving to microservices will make deploys fast enough." Inverted: "After moving to microservices, changes still reach production no faster." Conditions that would guarantee that inversion: (1) the release process still batches changes into ~2 deploys/day; (2) most changes touch checkout, which spans several services, so they need coordinated multi-service deploys; (3) each service's pipeline stays slow because the tests are integration tests that need the other services; (4) the team spends 12–24 months migrating and ships fewer features in the meantime; (5) operating several services takes up the time the speed-up was meant to free. Necessary preconditions, stated as claims that can be false:

- "Pipeline duration, not release process, caps delivery." → A-1, A-19 (**load-bearing**, unverified; C1 and C2 argue it is false)
- "Most changes stay inside one service boundary." → A-12, A-16 (**load-bearing**, unverified)
- "The 45 min comes from test volume that splitting into services would remove." → A-17 (not load-bearing for the recommendation; the monolith can remove it too)
- "12 engineers can absorb the operating cost of services." → A-18 (load-bearing for option B)
- "The migration cost is small relative to capacity." → A-10, A-11 (**load-bearing**, C5 argues it is false)

The load-bearing, unverified preconditions (A-1/A-19, A-12) are this analysis's sharpest open questions, and the Conclusion's verification steps target them.

## 3. Ground Truths

**Figure labels:** GT-1? to GT-5? are *reported operating figures* (stated by the user, not measured by this analysis). GT-6 to GT-8 are *definitions or arithmetic identities*. GT-9 and GT-10 are *published statements* read at their source. All derived figures in §4 are either *arithmetic* on these inputs or *estimates* (Fermi brackets), and are labelled as such where they appear.

- **GT-1?** The CI/CD pipeline takes about 45 minutes end to end. — unverified: stated in the user's problem statement, which names no measurement source; no CI timing data was supplied or pointed at, so there was nothing to open. Phase 3 failure record: source = CI run history; reason = not supplied (no path or URL given).
- **GT-2?** The team ships about 2 deploys a day. — unverified: user statement, no deploy log supplied. Phase 3 failure record: source = deploy log; reason = not supplied.
- **GT-3?** The team has 12 engineers. — unverified: user statement, no roster supplied.
- **GT-4?** Every deploy runs the full test suite and needs a coordinated application restart. — unverified: user statement; the pipeline configuration and restart procedure were not supplied. Phase 3 failure record: source = CI config and deploy runbook; reason = not supplied.
- **GT-5?** The platform is one Rails monolith of about 350 KLOC covering catalog, cart, checkout and fulfillment, 6 years old. — unverified: user statement, no repository pointed at.
- **GT-6** Serial pipeline capacity per window = window length ÷ pipeline duration; pipeline utilisation = (deploys × pipeline duration) ÷ window length. — source: definition; capacity and utilisation are defined this way, so the statement is its own derivation.
- **GT-7** Merge-to-production lead time = wait for the next deploy + pipeline duration. When deploys are spaced I minutes apart and merges arrive evenly, the mean wait is I/2. — source: definition (lead time partitioned into wait and pipeline), plus the mean of a uniform distribution on [0, I], which is (0 + I) ÷ 2.
- **GT-8** Work of W minutes split across N independent runners takes at least W/N minutes of wall-clock time; with a fixed per-runner setup overhead o, it takes about W/N + o. — source: arithmetic identity (dividing W equally among N runners gives W/N each; setup adds o to each).
- **GT-9** A microservice architecture carries a fixed cost in engineering effort, and that cost is only justified once a system is too complex to manage as a monolith. — source: Martin Fowler, "MicroservicePremium", martinfowler.com/bliki/MicroservicePremium.html; read-at-source: "When you use microservices you have to work on automated deployment, monitoring, dealing with failure, eventual consistency, and other factors that a distributed system introduces." and "don't even consider microservices unless you have a system that's too complex to manage as a monolith". This is a published expert position; it does not measure this system's complexity.
- **GT-10** Puma, the standard Rails application server, supports a phased restart that replaces workers one at a time while the rest keep serving. — source: Puma docs, github.com/puma/puma/blob/master/docs/restart.md; read-at-source: "A phased restart works by first killing an old worker, then starting a new worker, waiting until the new worker has successfully started before proceeding to the next worker." Limitation read at the same place: it needs `prune_bundler` enabled and `preload_app!` disabled. Rolling instances behind a load balancer works the same way one level up; that extension is not cited here.

**Provenance summary:**

```text
?-marked: GT-1?, GT-2?, GT-3?, GT-4?, GT-5? (5 of 10)
Read-at-source: GT-9 — MicroservicePremium, two quoted sentences above (feeds HIGH chain C8); GT-10 — Puma docs/restart.md, "Phased restart" passage quoted above (feeds HIGH chain C7)
Definitions (no source needed): GT-6, GT-7, GT-8
Not read — turn budget: none
```

Every `?` here has the same cause: the user supplied the figures without the logs they come from, and no files were pointed at. That is why every chain that uses them is capped at MEDIUM. Pulling the CI stage timings and the deploy log would remove the cause.

## 4. Derivation Chains

Every computed figure below was recomputed with an exact-fraction calculator; the Recompute part of the adversarial pass (appendix) lists each one. Figures are marked *arithmetic* (exact, given the inputs) or *estimate* (a Fermi bracket resting on a flagged assumption).

### Conclusion C1: Pipeline capacity is not what limits deploys to 2 a day

GT-1? (45-min pipeline, reported) + GT-2? (2 deploys/day, reported) + GT-6 (capacity and utilisation identity)
→ serial capacity in a 480-min window is 480 ÷ 45 = 10.67 deploys a day (arithmetic) [Assumes: A-6]
→ 2 deploys use 2 × 45 = 90 pipeline-minutes, a utilisation of 90 ÷ 480 = 18.75% (arithmetic)
→ the pipeline could carry 10.67 ÷ 2 = 5.33 times as many deploys as are shipped (arithmetic)
→ pipeline duration is not what caps deploy frequency at 2 a day

**Pre-check:** head GT-1?, GT-2?, GT-6 · ?-marked: GT-1?, GT-2? · lowest cited: none · Inputs ceiling: MEDIUM
**Confidence:** MEDIUM — the Inputs axis is short: GT-1? and GT-2? are user-reported; the CI run history and deploy log for the last 90 days would remove them as a cause. Inference: A-6 is priced — with a 24-hour window, utilisation is 90 ÷ 1,440 = 6.25%, which strengthens the endpoint, so it holds either way. Rivals: the flaky-rerun rival is ruled out in §5 ("Reruns make the pipeline the real limit").

### Conclusion C2: Waiting for the next deploy, not the pipeline, dominates merge-to-production time

GT-1? (45-min pipeline, reported) + GT-2? (2 deploys/day, reported) + GT-7 (lead-time identity, mean wait I/2)
→ 2 evenly spaced deploys in 480 min are I = 480 ÷ 2 = 240 min apart (arithmetic) [Assumes: A-6]
→ a merge waits on average 240 ÷ 2 = 120 min for the next deploy (arithmetic) [Assumes: A-7]
→ mean merge-to-production lead time is 120 + 45 = 165 min (arithmetic)
→ the pipeline is 45 ÷ 165 = 27.3% of that time and the wait is 120 ÷ 165 = 72.7% (arithmetic)
→ a zero-minute pipeline would cut lead time by at most 27.3%, while deploying each merge promptly removes up to 72.7%

**Pre-check:** head GT-1?, GT-2?, GT-7 · ?-marked: GT-1?, GT-2? · lowest cited: none · Inputs ceiling: MEDIUM
**Confidence:** MEDIUM — the Inputs axis is short: GT-1? and GT-2? as in C1; merge timestamps joined to deploy timestamps would measure the real wait directly. Inference: A-7 is priced — if engineers bunch merges just before each deploy, the wait moves from after the merge to before it (finished work held back unmerged), so lead time measured from "change ready" is unchanged and the endpoint stands. A-6 is priced the same way as in C1: a longer window lengthens the interval and the wait, which strengthens the endpoint. Rivals: the "microservices cut lead time more" rival is ruled out in §5.

### Conclusion C3: Splitting the test suite across runners cuts the monolith's pipeline by about a third to two-thirds

GT-1? (45-min pipeline, reported) + GT-8 (split work takes W/N + o)
→ tests take T = 0.5 × 45 = 22.5 to 0.8 × 45 = 36 min of the pipeline, central 30 min (estimate) [Assumes: A-8]
→ split across N = 4 to 8 runners with o = 2 min setup, the test stage takes T/N + 2 (estimate) [Assumes: A-9]
→ central pipeline is (45 − 30) + 30/4 + 2 = 15 + 7.5 + 2 = 24.5 min (estimate)
→ best case (T = 36, N = 8) is 9 + 4.5 + 2 = 15.5 min, worst case (T = 22.5, N = 4) is 22.5 + 5.625 + 2 = 30.125 min (estimate)
→ that is a reduction of 33.1% (worst) to 65.6% (best), central 45.6%, with no change to architecture (arithmetic on the estimate)
→ serial capacity rises to 480 ÷ 30.125 = 15.9 to 480 ÷ 15.5 = 31.0 deploys a day, central 480 ÷ 24.5 = 19.6 (arithmetic)
→ every point in that range exceeds the ~12 merges a day assumed, which today's 10.67 does not [Assumes: A-15]
→ deploying each merge, or small groups of merges, fits within pipeline capacity once tests are split

**Pre-check:** head GT-1?, GT-8 · ?-marked: GT-1? · lowest cited: none · Inputs ceiling: MEDIUM
**Confidence:** MEDIUM — the Inputs axis is short: GT-1?; a stage-by-stage CI timing breakdown would remove it as a cause, and would also replace A-8's bracket with a measurement. Inference: A-8 is priced by the bracket itself (every point in 15.5–30.125 min supports the endpoint). A-9 is priced — if order-dependent tests must be fixed before the suite can be split, that is extra cost (absorbed by C5's 6 engineer-month upper end), not a failure of the endpoint. A-15 is priced — above ~19.6 merges a day, pairs of merges share a deploy, adding about half a pipeline duration to the wait, which is why the endpoint says "or small groups". Rivals: the "code size causes the 45 min" rival is ruled out in §5.

### Conclusion C4: The coordinated restart is a deployment choice, removable without splitting the codebase

GT-4? (full suite and coordinated restart every deploy, reported) + GT-10 (Puma phased restart, read at source)
→ the restart requirement belongs to how the app server is restarted, not to the app being one codebase
→ replacing workers one at a time lets the monolith deploy without downtime or a coordinated window [Assumes: A-13]
→ the coordination that makes each deploy an event can be removed without splitting the codebase

**Pre-check:** head GT-4?, GT-10 · ?-marked: GT-4? · lowest cited: none · Inputs ceiling: MEDIUM
**Confidence:** MEDIUM — the Inputs axis is short: GT-4?; the current deploy runbook, and whether `preload_app!` is enabled (GT-10's stated limitation), would remove it as a cause. Inference: A-13 is priced — if some schema changes cannot be made backward-compatible, deploys that carry them still need coordination; deploys without one do not, and a service architecture has the same migration constraint per service plus cross-service API compatibility, so the endpoint holds for schema-free deploys and the comparison with microservices is unaffected. Rivals: the "only microservices fix locking migrations" rival is ruled out in §5.

### Conclusion C5: A microservice migration costs about 24 times the pipeline fix at the central estimate, and more at every point in both brackets

GT-3? (12 engineers, reported) + GT-5? (350 KLOC, four domains, reported) + GT-9 (microservice premium, read at source)
→ extracting four domains costs 2 × 12 = 24 to 6 × 24 = 144 engineer-months, central 4 × 18 = 72 (estimate) [Assumes: A-10]
→ against 12 × 12 = 144 engineer-months a year, that is 16.7% to 100% of a year, central 72 ÷ 144 = 50% (arithmetic on the estimate) [Assumes: A-11]
→ test splitting plus phased restarts cost 1 × 1 = 1 to 2 × 3 = 6 engineer-months, central 1.5 × 2 = 3 (estimate)
→ the central fix is 3 ÷ 144 = 2.1% of a year and 72 ÷ 3 = 24 times cheaper than the central migration (arithmetic on the estimates)
→ the migration's low end (24) is 24 ÷ 6 = 4 times the fix's high end, so the ordering holds everywhere in both brackets (arithmetic)
→ the migration figures leave out the ongoing costs GT-9 names (deployment automation, monitoring, failure handling, eventual consistency), so they understate its total
→ the microservice route is at least 4 and centrally 24 times the cost of the monolith fix for the same lead-time goal

**Pre-check:** head GT-3?, GT-5?, GT-9 · ?-marked: GT-3?, GT-5? · lowest cited: none · Inputs ceiling: MEDIUM
**Confidence:** MEDIUM — the Inputs axis is short: GT-3? and GT-5?; the team roster and a line count by domain (for example `cloc` per directory) would remove them as causes. Inference: A-10 is priced — the migration's low end would have to be 4 times smaller than estimated (24 → 6) before the orderings met. A-11 is priced — real capacity below 144 engineer-months makes the migration a larger share, which strengthens the endpoint. Rivals: the incremental-extraction ("strangler") rival is ruled out in §5.

### Conclusion C6: Recommend fixing the monolith's pipeline and deploy process, not migrating to microservices

The full matrix, anchors and flip test are in the appendix under "Trade-off analysis (process output)". Weights were locked before any option was scored. Options: A status quo (ruled out by the must-have "reduces merge-to-production lead time"), B full microservices, C monolith pipeline and deploy fixes, D composite (C now, then extract one domain later only if evidence justifies it). B and C are scored on the same process basis: both assume deploy-per-merge.

C1 (MEDIUM) + C2 (MEDIUM) + C3 (MEDIUM) + C4 (MEDIUM) + C5 (MEDIUM) + GT-9 (microservice premium)
→ with per-merge deploys on the split pipeline, mean merge-to-production time falls from 165 to about 24.5 min, (165 − 24.5) ÷ 165 = 85.2% less (arithmetic on the estimate) [Assumes: A-15]
→ weighted totals are C = 117, D = 100, B = 58, with A ruled out (arithmetic) [Assumes: A-12, A-16]
→ C's 17-point lead over D comes from cost (weight 4), checkout safety (weight 5) and reversibility (weight 2)
→ no single weight change within 1–5 flips C and D, since the nearest (cost 4 → 1) still leaves C ahead by 17 − 3 × 2 = 11
→ recommend C, keeping the monolith and fixing tests, restarts and release cadence
→[2nd] (actor: engineers) each deploy carries one or a few merges, so a bad change is found and rolled back in one step
→[2nd] (actor: engineers) rolling restarts require schema changes to be split into expand and contract steps, a new habit with a per-change cost [Assumes: A-13]
→[2nd] (actor: leadership) the answer to "we need microservices" changes, so the result must be shown in lead-time figures leadership can check
→[2nd] (time: immediate) split tests use 15 + 4 × (7.5 + 2) = 53 runner-minutes per pipeline against 45, 8 ÷ 45 = 17.8% more CI compute (arithmetic on the estimate) [Assumes: A-9]
→[3rd] (time: long run) the suite grows with the code, so the split pipeline creeps back toward 45 min unless runners are added with it
→[3rd] (time: long run) once the team outgrows one codebase, module boundaries enforced now become extraction seams, so C does not rule out B later

**Pre-check:** head C1 (MEDIUM), C2 (MEDIUM), C3 (MEDIUM), C4 (MEDIUM), C5 (MEDIUM), GT-9 · ?-marked: none · lowest cited: MEDIUM · Inputs ceiling: MEDIUM
**Confidence:** MEDIUM — the Inputs axis is short: C1, C2, C3, C4 and C5 are each MEDIUM, and their own confidence lines name the verification that closes them. Inference: A-15 is priced in C3. A-12 is priced — if checkout does not span one transaction, B's checkout-safety score could rise from 1 to 3, adding 2 × 5 = 10 to reach 68, still 49 below C. A-16 is priced — if fulfillment is not loosely coupled, D's checkout-safety and cost scores fall, which widens C's lead. The A-13 and A-9 marks are on second-order extension steps only, outside the axis. The flip test shows the endpoint does not rest on any single weight. Rivals: the "microservices cut lead time more" rival and the team-independence rival (B wins if independence dominates — raising that weight 3 → 5 still leaves C ahead of B by 59 − 2 × 3 = 53) are ruled out in §5. Second-order check: no extension step contradicts a ground truth; the 17.8% CI compute increase and the expand/contract habit each work against the cost criterion and are reported in §6. Pre-mortem weak link K1: what actually caps deploys at 2 a day (A-19) is not identified by any chain; the recommendation's first step now maps it, and a two-week tripwire on the deploy log catches the case where the cap is something else.

### Conclusion C7: A Puma-served monolith can take new code without stopping all its workers at once

GT-10 (Puma phased restart, read at source)
→ a phased restart kills and replaces one worker at a time, waiting for each new worker to start before moving on
→ with two or more workers, at every moment of the restart at least one worker is serving requests [Assumes: A-22]
→ a Puma-served Rails monolith with two or more workers can take new code without stopping every worker, provided `preload_app!` is disabled as the source requires

**Pre-check:** head GT-10 · ?-marked: none · lowest cited: none · Inputs ceiling: HIGH
**Confidence:** HIGH — the only input, GT-10, was read at source (Puma docs/restart.md, passage quoted in §3); each hop follows by deduction from the quoted mechanism; A-22 is priced because the endpoint states "two or more workers" as a condition, so a one-worker setup falls outside the claim instead of falsifying it. Rivals: rival not applicable — the endpoint restates the documented mechanism together with its two documented or stated conditions, and nothing competes with it. Whether *this* platform meets the conditions is carried by C4 (MEDIUM, GT-4?).

### Conclusion C8: Migration effort alone understates what the microservice route costs

GT-9 (microservice premium, read at source)
→ the costs the source names — automated deployment, monitoring, dealing with failure, eventual consistency — continue for as long as the system is distributed
→ an estimate counting only the one-time migration effort leaves those continuing costs out
→ any migration-only cost figure is a lower bound on the microservice route's total cost

**Pre-check:** head GT-9 · ?-marked: none · lowest cited: none · Inputs ceiling: HIGH
**Confidence:** HIGH — GT-9 was read at source (the two sentences quoted in §3); each hop follows by deduction; rival: "this team has already paid the premium (it already has deployment automation)" — even at a premium of zero the migration-only figure is still a lower bound (≥), so the rival does not compete with the endpoint, only with how large the gap is. That size is not claimed here.

## 5. Abandoned Reasoning

### Dead End: Reruns make the pipeline the real limit (rival to C1)

**What was tried:** Supposing flaky tests force reruns, so the effective pipeline is 2 or 3 times 45 minutes, and checking whether that makes pipeline capacity the cap on deploys.

**Why abandoned:** At 2 runs per deploy, 2 deploys use 2 × 90 = 180 minutes, 180 ÷ 480 = 37.5% utilisation. At 3 runs, 2 × 135 = 270 minutes, 270 ÷ 480 = 56.25%. Both are well below 100%, so the arithmetic in C1 still holds: the pipeline is not full.

**What it ruled out:** Flakiness costs engineer attention and is worth fixing, but it does not explain the 2-deploys-a-day ceiling. C1 stands.

### Dead End: Microservices cut lead time more than the monolith fix (rival to C2 and C6)

**What was tried:** Giving the microservice option its best case: a 10-minute pipeline per service [estimate, A-2]. With today's 2 deploys a day, lead time is 120 + 10 = 130 min, only (165 − 130) ÷ 165 = 21.2% better than today. With deploy-per-merge, it is about 10 min, (165 − 10) ÷ 165 = 93.9% better, against C's 24.5 min, (165 − 24.5) ÷ 165 = 85.2% better.

**Why abandoned:** On the same process basis, microservices add 93.9 − 85.2 = 8.8 percentage points of lead-time improvement over the monolith fix, at 4 to 24 times the cost (C5), plus the ongoing costs in GT-9. Without the process change they deliver 21.2%, less than the monolith's 72.7% from deploying promptly (C2).

**What it ruled out:** The idea that architecture is what makes changes reach production faster here. Most of the gain comes from the release-process change, which the monolith can make too (ruled out by C2 and C5).

### Dead End: The 350 KLOC size itself causes the 45 minutes (rival to C3)

**What was tried:** Treating pipeline time as proportional to code size, which would mean only smaller codebases give faster pipelines.

**Why abandoned:** Wall-clock pipeline time is set by the test work and how many runners share it (GT-8), not by line count. Splitting tests across runners gives each run a smaller slice of the suite without splitting the code (C3).

**What it ruled out:** "Smaller services are needed for faster pipelines" as a necessary step (ruled out by C3).

### Dead End: Only microservices fix migrations that lock tables (rival to C4)

**What was tried:** Supposing the coordinated restart exists because schema migrations lock tables, and that separate services would avoid it.

**Why abandoned:** Each service still owns a database with the same migration constraint, and adds cross-service API version compatibility; GT-9 lists eventual consistency and failure handling as costs that splitting introduces. Splitting moves the constraint without removing it.

**What it ruled out:** Migration locking as an argument for microservices (ruled out by C4 and GT-9).

### Dead End: Incremental ("strangler") extraction makes the migration cheap (rival to C5)

**What was tried:** Supposing extracting one domain at a time spreads the cost thin enough to compete with the pipeline fix.

**Why abandoned:** Incremental extraction lowers the risk of each step, not the total effort; even the bracket's low end of 24 engineer-months is 24 ÷ 6 = 4 times the fix's high end (C5). Extracting one domain on evidence is kept as option D and scored (C6); it came second, 100 to 117.

**What it ruled out:** Treating "incremental" as meaning "cheap" (ruled out by C5 and C6).

### Dead End: Team independence is the real bottleneck (rival to C6)

**What was tried:** Supposing the delay comes from 12 engineers blocking each other in one codebase, which microservices address through independent deploys.

**Why abandoned:** Nothing in the reported figures measures such blocking, and the trade-off already scores it (the team-independence criterion). Raising that weight from 3 to 5 moves B up by 2 × 3 = 6 points against C, leaving C ahead by 59 − 6 = 53. It stays a trigger to revisit, not a reason to migrate now.

**What it ruled out:** Migrating now on the independence argument alone (ruled out by C6's flip test). The Conclusion names the measurement that would reopen it.

## 6. Conclusion

**Recommended approach:** Do not start a microservice migration to solve deploy speed. Keep the monolith and fix the delivery process, in this order: measure CI stage times, the merge-to-deploy wait, and whatever decides when a deploy happens (approvals, QA sign-off, restart windows); split the test suite across 4–8 runners; switch to Puma phased (rolling) restarts with expand/contract migrations; then deploy each merge, or small groups of merges, as it lands (chain C6).

**Key insight:** "Deploys are too slow" describes two different problems. The pipeline is only 18.75% utilised (chain C1), and it accounts for 27.3% of the 165-minute merge-to-production time, while waiting for one of two daily deploys accounts for 72.7% (chain C2). The main delay is release cadence, which microservices do not change by themselves.

**Expected effect:** Splitting tests brings the pipeline from 45 minutes to about 24.5 (15.5–30.1) and raises capacity to about 19.6 deploys a day (chain C3). With restarts no longer coordinated (chain C4, chain C7), mean merge-to-production time falls from about 165 minutes toward the 24.5-minute pipeline, an 85.2% reduction (chain C6).

**Cost comparison:** The fix is estimated at about 3 engineer-months (1–6), 2.1% of a year's team capacity, against about 72 (24–144) for a migration, 50% of a year, and the migration figure leaves out the ongoing costs of running services (chain C5, chain C8).

**Trade-offs acknowledged:** The 12 engineers keep sharing one codebase and release train; schema changes need expand/contract discipline; CI compute rises by about 17.8%; and the suite's growth will slowly lengthen the pipeline again unless runners are added (chain C6).

**Revisit when:**

- CI stage timings show pipeline utilisation above about 80%, or tests below half the 45 minutes, which would reopen C1 and C3 (chain C1, chain C3).
- Measured delay shifts from pipeline and wait time to engineers blocking each other; then extract the most loosely coupled domain first (chain C6).

**Pre-check:** head C1 (MEDIUM), C2 (MEDIUM), C3 (MEDIUM), C4 (MEDIUM), C5 (MEDIUM), C6 (MEDIUM), C7 (HIGH), C8 (HIGH) · ?-marked: none · lowest cited: MEDIUM · Inputs ceiling: MEDIUM
**Confidence:** MEDIUM — C7 and C8 are HIGH, but the recommendation also rests on C1, C2, C3, C4, C5 and C6, which are MEDIUM for one shared reason: the operating figures (45 min, 2 deploys a day, 12 engineers, the restart procedure, 350 KLOC) are reported, not measured. Each chain's own line names the log or breakdown that would close it; the CI stage timings and the deploy log together would close most of them. No axis other than Inputs is short on any of them (chain C6).
## Appendix — process output

## Trade-off analysis (process output)

This is the trade-off procedure's own output, which collapses into chain C6.

### Options

- **A — Status quo:** keep the 45-min pipeline, coordinated restarts, ~2 deploys a day. **Knocked out** by the must-have "reduces merge-to-production lead time", since A-14 (speed has value) is the premise of the request.
- **B — Full microservices:** extract catalog, cart, checkout and fulfillment into separately deployed services, with deploy-per-merge per service.
- **C — Monolith pipeline and deploy fixes:** split the test suite across 4–8 runners, Puma phased restarts with expand/contract migrations, deploy-per-merge.
- **D — Composite:** C now, then extract one loosely coupled domain (fulfillment, A-16) if measured evidence justifies it.

Must-haves: (1) reduces merge-to-production lead time; (2) keeps checkout working throughout (no planned outage of order-taking). B, C and D pass both; A fails (1).

### Criteria & Weights

Locked before scoring. Higher is always better.

| Criterion | Weight | 1 means | 5 means |
|---|---|---|---|
| Lead-time reduction (same process basis) | 5 | < 10% | > 50% (2 = 10–25, 3 = 25–40, 4 = 40–50) |
| Time to first benefit | 4 | > 12 months | < 1 month (2 = 6–12, 3 = 3–6, 4 = 1–3) |
| Engineering cost (central estimate) | 4 | > 50 eng-months | < 6 eng-months (2 = 30–50, 3 = 12–30, 4 = 6–12) |
| Checkout safety | 5 | adds distributed transactions across cart/checkout/fulfillment | no change to transaction boundaries |
| Operational fit for 12 engineers | 3 | 4+ separately operated deployables | 1 deployable |
| Team independence | 3 | all 12 on one release train, blocking each other | each team deploys on its own |
| Reversibility | 2 | cannot be undone within a year | can be reverted within a week |

### Scoring

| Option | Lead time ×5 | Time to benefit ×4 | Cost ×4 | Checkout safety ×5 | Ops fit ×3 | Independence ×3 | Reversibility ×2 | Total |
|---|---|---|---|---|---|---|---|---|
| B | 5 × 5 = 25 | 1 × 4 = 4 | 1 × 4 = 4 | 1 × 5 = 5 | 1 × 3 = 3 | 5 × 3 = 15 | 1 × 2 = 2 | **58** |
| C | 5 × 5 = 25 | 4 × 4 = 16 | 5 × 4 = 20 | 5 × 5 = 25 | 5 × 3 = 15 | 2 × 3 = 6 | 5 × 2 = 10 | **117** |
| D | 5 × 5 = 25 | 4 × 4 = 16 | 3 × 4 = 12 | 4 × 5 = 20 | 4 × 3 = 12 | 3 × 3 = 9 | 3 × 2 = 6 | **100** |

Ground truths behind the scores: lead time — C2, C3 and the §5 same-basis comparison (B 93.9%, C and D 85.2%, both > 50%); time to benefit and cost — C5 (B 72 eng-months central → 1; C 3 → 5; D 3 + 12 to 24 for one extraction = 15 to 27 → 3); checkout safety — A-12 (unverified) and GT-9 (eventual consistency); ops fit — GT-9 and A-18; independence — a **preference** score with no ground truth behind it; reversibility — C4 (rolling restarts can be turned off) and C5 (the size of the migration).

### Recommendation

C wins with 117, ahead of D (100) and B (58). **Flip test:** C versus D — D leads only on independence (3 against 2), so raising that weight 3 → 5 gives D 2 more points: gap 17 → 15. C leads on cost (by 2 points), checkout safety (1), ops fit (1) and reversibility (2): cost 4 → 1 cuts the gap by 3 × 2 = 6 to 11; checkout 5 → 1 cuts 4 × 1 = 4 to 13; ops 3 → 1 cuts 2 to 15; reversibility 2 → 1 cuts 2 to 15. **No single weight change flips C and D**; the closest leaves C ahead by 11. C versus B: B leads only on independence (by 3); weight 3 → 5 adds 2 × 3 = 6, and the gap goes from 59 to 53. No single weight change flips it. Inputs rest on MEDIUM chains and on A-12, so the chain this collapses into is MEDIUM.

## Assumption Audit scan (process output)

| Chain | Step | Step Text (brief) | Assumption surfaced? | Added to Table? |
|---|---|---|---|---|
| C1 | 1 | capacity 480 ÷ 45 = 10.67 | A-6 (480-min window) | yes |
| C1 | 2 | utilisation 90 ÷ 480 = 18.75% | none beyond A-6 | n/a |
| C1 | 3 | 5.33 times headroom | none | n/a |
| C1 | 4 | pipeline not the cap | none | n/a |
| C2 | 1 | interval 240 min | A-6 | already present |
| C2 | 2 | mean wait 120 min | A-7 (even spacing, uniform merges) | yes |
| C2 | 3 | lead time 165 min | none | n/a |
| C2 | 4 | 27.3% / 72.7% split | none | n/a |
| C2 | 5 | pipeline removal caps gain at 27.3% | none | n/a |
| C3 | 1 | tests are 22.5–36 min | A-8 (test share 50–80%) | yes |
| C3 | 2 | split to T/N + 2 | A-9 (shardable, 2-min overhead) | yes |
| C3 | 3 | central 24.5 min | none | n/a |
| C3 | 4 | bracket 15.5–30.125 | none | n/a |
| C3 | 5 | 33.1–65.6% reduction | none | n/a |
| C3 | 6 | capacity 15.9–31.0 a day | A-6 | already present |
| C3 | 7 | exceeds ~12 merges a day | A-15 (merge rate) | yes |
| C3 | 8 | per-merge deploys fit | none | n/a |
| C4 | 1 | restart is a deployment property | none | n/a |
| C4 | 2 | worker-by-worker restart | A-13 (backward-compatible migrations) | yes |
| C4 | 3 | coordination removable | none | n/a |
| C5 | 1 | migration 24–144 eng-months | A-10 (migration effort) | yes |
| C5 | 2 | 16.7–100% of a year | A-11 (144 eng-months capacity) | yes |
| C5 | 3 | fix 1–6 eng-months | A-10 (fix-cost bracket, now stated in A-10's row) | yes (amended in the gate's Fix step) |
| C5 | 4 | 2.1% of a year, 24× cheaper | none | n/a |
| C5 | 5 | ordering holds across brackets | none | n/a |
| C5 | 6 | ongoing premium excluded | none | n/a |
| C5 | 7 | migration at least 4× cost | none | n/a |
| C6 | 1 | 165 → 24.5 min, 85.2% | A-15 (mark added in Fix step) | already present |
| C6 | 2 | weighted totals | A-12, A-16 (mark added in Fix step) | yes |
| C6 | 3 | lead drivers | none | n/a |
| C6 | 4 | flip test | none | n/a |
| C6 | 5 | recommend C | none | n/a |
| C6 | [2nd] 6 | smaller deploys, easy rollback | none | n/a |
| C6 | [2nd] 7 | expand/contract habit | A-13 | already present |
| C6 | [2nd] 8 | leadership needs figures | none | n/a |
| C6 | [2nd] 9 | +17.8% CI compute | A-9 (mark added in Fix step) | already present |
| C6 | [3rd] 10 | suite growth creeps back | none | n/a |
| C6 | [3rd] 11 | seams preserve option B | none | n/a |
| C7 | 1 | one worker replaced at a time | none | n/a |
| C7 | 2 | at least one worker serving | A-22 (two or more workers) | yes |
| C7 | 3 | no full stop needed, preload_app! disabled | none | n/a |
| C8 | 1 | named costs continue | none | n/a |
| C8 | 2 | migration-only estimate omits them | none | n/a |
| C8 | 3 | migration figure is a lower bound | none | n/a |


Techniques not applied:
- theoretical-limit (Phase 1) — not applicable — whether 45 min is a convention or a hard bound does not decide the question; C1 shows the pipeline is not the binding constraint either way
- theoretical-limit (Phase 4) — not applicable — the lead-time floor (pipeline duration with zero wait) is already stated in C2 and C3; no physical ceiling is in play
- fishbone (Phase 2) — not applicable — the assumption space was enumerated through the inversion pass and the latency/throughput split; it is not multi-causal enough to need category brainstorming
- inversion (Phase 5) — not applicable — the conclusion is a plan, so Phase 5 used pre-mortem (the adversarial pass below); inversion was applied at Phase 2

## Adversarial pass (process output)

**Recompute** — every figure was redone with an exact-fraction calculator, separately from the chain text:
480/45 = 32/3 ≈ 10.67 ✓; 2 × 45 = 90 ✓; 90/480 = 3/16 = 18.75% ✓; 10.67/2 = 16/3 ≈ 5.33 ✓; 90/1440 = 6.25% ✓; 480/2 = 240 ✓; 240/2 = 120 ✓; 120 + 45 = 165 ✓; 45/165 = 3/11 ≈ 27.3% ✓; 120/165 = 8/11 ≈ 72.7% ✓; 0.5 × 45 = 22.5 ✓; 0.8 × 45 = 36 ✓; (2/3) × 45 = 30 ✓; 15 + 7.5 + 2 = 24.5 ✓; 9 + 4.5 + 2 = 15.5 ✓; 22.5 + 5.625 + 2 = 30.125 ✓; (45 − 30.125)/45 = 33.1% ✓; (45 − 15.5)/45 = 65.6% ✓; (45 − 24.5)/45 = 45.6% ✓; 480/30.125 ≈ 15.93 ✓; 480/15.5 ≈ 30.97 ✓; 480/24.5 ≈ 19.59 ✓; 2 × 12 = 24, 6 × 24 = 144, 4 × 18 = 72 ✓; 12 × 12 = 144 ✓; 24/144 = 16.7%, 144/144 = 100%, 72/144 = 50% ✓; 1 × 1 = 1, 2 × 3 = 6, 1.5 × 2 = 3 ✓; 3/144 ≈ 2.08% ✓; 72/3 = 24 ✓; 24/6 = 4 ✓; 6/144 ≈ 4.2% ✓; 15 + 4 × 9.5 = 53, 8/45 ≈ 17.8% ✓; 180/480 = 37.5%, 270/480 = 56.25% ✓; 120 + 10 = 130, 35/165 ≈ 21.2% ✓; 155/165 ≈ 93.9% ✓; 140.5/165 ≈ 85.2% ✓; 93.94 − 85.15 = 29/330 ≈ 8.8 pp ✓; weighted totals B 58, C 117, D 100 ✓; gaps 17 and 59 ✓; flip results 15, 11, 13, 15, 15 and 53 ✓. Direction check: every "reduction" is a smaller figure than its base, and every capacity after splitting (15.9–31.0) exceeds today's 10.67, as it must when the divisor falls. Correction made during recompute: in a first pass, the independence flip for C against D was computed as 17 − 2 × 2 = 13; D leads by only 1 point on that criterion, so the right value is 17 − 2 × 1 = 15, which is what the trade-off block states.

**Sensitivity** — the single ground truth whose falsity would flip the conclusion is **GT-2?** (2 deploys a day), read together with GT-1?: if real deploy volume were near pipeline capacity (above about 0.8 × 10.67 ≈ 8.5 a day, 80% utilisation), the pipeline would be the binding constraint and the microservice argument would gain ground. It is `?`-marked and cannot be verified here (no deploy log supplied), so the Conclusion carries the MEDIUM caveat naming the deploy log. Weakest link per chain: C1 — GT-2?; C2 — the A-7 hop (priced); C3 — A-9, shardability of a six-year-old suite; C4 — GT-4?, specifically whether `preload_app!` blocks phased restart; C5 — A-10, the migration bracket; C6 — the checkout-safety scores resting on A-12, and the independence score, which is a preference.

**Rival** — headline: "migrate to microservices" (option B) → §5 "Microservices cut lead time more than the monolith fix" and §5 "Team independence is the real bottleneck". Per intermediate chain: C1 → §5 "Reruns make the pipeline the real limit"; C2 → §5 "Microservices cut lead time more…"; C3 → §5 "The 350 KLOC size itself causes the 45 minutes"; C4 → §5 "Only microservices fix migrations that lock tables"; C5 → §5 "Incremental (strangler) extraction makes the migration cheap"; C6 → option D, scored and placed second (100 against 117), plus the independence rival. C7 → rival not applicable — the endpoint restates the documented mechanism with its conditions. C8 → the "premium already paid" rival, ruled out on C8's own confidence line (a zero premium still leaves a lower bound). No rival is left live on any `**Confidence:**` line.

**Premise** — It is six months from now. The monolith pipeline-and-deploy plan has failed: changes still take hours to reach production, and leadership has started the microservice migration anyway.

**Causes** (unfiltered; viewpoints: implementing engineer, on-call operator, leadership who pays, customer, competitor):
1. (engineer) Order-dependent tests made the split suite flaky, so the team turned splitting off.
2. (engineer) Expand/contract migrations felt like overhead; schema changes were bundled, rolling restarts broke, and the team went back to coordinated restarts.
3. (engineer) `preload_app!` could not be disabled because of memory limits, so phased restart was unavailable.
4. (engineer) The pipeline got faster, but deploys stayed gated by a twice-daily manual QA sign-off that nobody had named as the real cap.
5. (on-call) More deploys brought a burst of incidents at first, and a deploy freeze put the team back at 2 a day.
6. (on-call) Without feature flags, unfinished work could not ship per merge, so batching stayed.
7. (leadership) The plan read as a refusal of microservices, and a parallel migration took half the team.
8. (leadership) No baseline lead time was recorded, so nobody could show the improvement.
9. (leadership) The CI bill rose and runners were cut.
10. (customer) A rolling deploy mixed old and new code mid-checkout and caused an order-total bug.
11. (competitor) Three months on delivery plumbing slowed feature work, and a competitor shipped the features customers wanted.
12. (engineer) The real delay was code review and merge conflicts, which nobody measured.

Adversarial re-read: causes 4 and 12 contradict the recommendation's own premise. C1 shows the pipeline is not the cap, but no chain identifies what *is*; the plan assumed restart coordination is the gate (C4) without evidence. This is the highest-signal finding.

**Clusters:**
- **K1 — The real release gate was never identified** (causes 4, 5, 6, 12) — bears on C1, C2, A-19. Triage: **fatal** (if the real gate is untouched, nothing improves). Tripwire: two weeks after splitting and rolling restarts go live, the deploy log still shows 3 or fewer deploys a day; the engineering manager checks it at the weekly review.
- **K2 — Technical prerequisites fail** (causes 1, 2, 3, 10) — bears on C3, C4, GT-10, A-9, A-13, A-12. Triage: **costly but survivable**. Tripwire: split-suite flake rate above 2% of runs in any week, or a phased-restart dry run failing in staging; the CI owner sees it on the CI dashboard daily.
- **K3 — The stakeholder case and measurement were lost** (causes 7, 8, 9, 11) — bears on C5, C6. Triage: **costly but survivable**. Tripwire: no baseline lead-time figure by the end of week 2, or effort passing 3 engineer-months (C5's central estimate); the tech lead reports both to leadership every two weeks.

**Disposition:**
- K1 → **plan change:** the first step of the recommendation now includes mapping whatever decides when a deploy happens (approvals, QA sign-off, restart windows) before building anything; §6's Recommended approach was edited to say so.
- K2 → **plan change:** spike each prerequisite in the first two weeks (a trial split run, a `preload_app!` check, one expand/contract migration in staging). **Accepted risk** for cause 10, with a named mitigation: blue-green at the load balancer as a fallback where phased restart is unsafe.
- K3 → **accepted risk** with named mitigation: record a baseline now, time-box the work at 3 engineer-months, and report lead time to leadership every two weeks, so the plan is judged on figures rather than on its label.

**Falsification** — The conclusion is false if the CI stage timings and deploy log show pipeline utilisation above about 80% of the deploy window, or if, after tests are split and restarts are rolling, most changes still require coordinated changes across domains that only separately deployable services would decouple.

## §6→§4 closure ledger (process output)

- "Recommended approach: Do not start a microservice migration … deploy each merge, or small groups of merges, as it lands" → chain C6 ✓
- "Key insight: 'Deploys are too slow' describes two different problems … 18.75% … 27.3% … 72.7%" → chain C1, chain C2 ✓
- "Expected effect: … about 24.5 (15.5–30.1) … 19.6 deploys a day … an 85.2% reduction" → chain C3, chain C4, chain C7, chain C6 ✓
- "Cost comparison: … about 3 engineer-months (1–6) … about 72 (24–144) … leaves out the ongoing costs" → chain C5, chain C8 ✓
- "Trade-offs acknowledged: … expand/contract … 17.8% … suite's growth" → chain C6 ✓
- "CI stage timings show pipeline utilisation above about 80% …" → chain C1, chain C3 ✓
- "Measured delay shifts … extract the most loosely coupled domain first" → chain C6 ✓
- "Pre-check: head C1 (MEDIUM) … Inputs ceiling: MEDIUM" → chains C1–C8 (its own head) ✓
- "Confidence: MEDIUM — C7 and C8 are HIGH, but …" → chains C1–C8 ✓

No claim cut. (Rows re-verified after the gate's Fix step added C7 and C8.)

## Self-audit scan (process output)

| Chain | Chain Head (brief) | Form conforming? | Rule applied | Dependency clean? | Band | Act attempted? | Edges fired |
|---|---|---|---|---|---|---|---|
| C1 | GT-1? + GT-2? + GT-6 | yes | n/a | yes | MEDIUM | no | none |
| C2 | GT-1? + GT-2? + GT-7 | yes | n/a | yes | MEDIUM | no | none |
| C3 | GT-1? + GT-8 | yes | n/a | yes | MEDIUM | no | none |
| C4 | GT-4? + GT-10 | yes | n/a | yes | MEDIUM | yes | none |
| C5 | GT-3? + GT-5? + GT-9 | yes | n/a | yes | MEDIUM | yes | none |
| C6 | C1–C5 + GT-9 | yes | n/a | yes | MEDIUM | yes | Self-Audit Gate Fix/Repeat (assumption marks added) |
| C7 | GT-10 | yes | n/a | yes | HIGH | yes | Self-Audit Gate Fix/Repeat (chain added) |
| C8 | GT-9 | yes | n/a | yes | HIGH | yes | Self-Audit Gate Fix/Repeat (chain added) |

C1, C2 and C3 are load-bearing, and every `?` input on their heads is `Act attempted? = no`: the figures came from the user's statement, and no CI log, deploy log or repository was supplied, so there was no source to open. Each chain's confidence line names the log that would close it.

| §6 Span (brief) | Construct | Claim under R11? | R11 clause applied | Chain cited |
|---|---|---|---|---|
| Recommended approach: no migration; measure, split tests, phased restarts, deploy per merge | bold lead-in | yes | bold lead-in whose colon closes the bold span | C6 |
| Key insight: two problems; 18.75%, 27.3%, 72.7% | bold lead-in | yes | bold lead-in whose colon closes the bold span | C1, C2 |
| Expected effect: 24.5 min, 19.6/day, 85.2% | bold lead-in | yes | bold lead-in whose colon closes the bold span | C3, C4, C7, C6 |
| Cost comparison: 3 vs 72 eng-months, ongoing costs excluded | bold lead-in | yes | bold lead-in whose colon closes the bold span | C5, C8 |
| Trade-offs acknowledged: shared codebase, expand/contract, +17.8% CI, suite growth | bold lead-in | yes | bold lead-in whose colon closes the bold span | C6 |
| Revisit when: | bold lead-in | no | section-intro label whose colon-terminated span is the whole line, with no citation of its own | n/a |
| utilisation above ~80% or tests under half | list item | yes | list item over forty characters | C1, C3 |
| delay shifts to engineers blocking each other | list item | yes | list item over forty characters | C6 |
| Pre-check: head C1–C6 (MEDIUM), C7–C8 (HIGH) | bold lead-in | yes | bold lead-in whose colon closes the bold span | C1–C8 |
| Confidence: MEDIUM, reported operating figures | bold lead-in | yes | bold lead-in whose colon closes the bold span | C1–C8 |

```text
Scan complete: 8 chain rows, one per section-4 chain block in order; 10 section-6 rows, one per construct in order — 9 claims under R11, 1 excluded. 0 chains malformed, 0 claims untraced.
```

## Self-Audit Gate (process output)

**Pass 1 (before re-score):** Criterion 1 Rigorous · Criterion 2 Sound · Criterion 3 Hand-wavy · Criterion 4 Hand-wavy · Criterion 5 Rigorous · Criterion 6 Rigorous · Gate cleared: yes · Hand-wavy cap cleared: no

Criterion 2's reason: the fix-cost bracket in C5 step 3 had no Assumptions Table row of its own. Criterion 3's reason: GT-9 and GT-10 were unsuffixed, their sources reachable and read, yet each fed only MEDIUM chains. Criterion 4's reason: C6's weighted-totals hop, which the endpoint depends on, rested on A-12 and A-16 without an `[Assumes:]` mark; C6 steps 1 and 9 were also unmarked. Two Hand-wavy bands broke the hand-wavy cap, so the **Fix/Repeat edge fired** once.

**Fix applied:** A-10 now states both cost brackets; A-22 added; `[Assumes: A-15]`, `[Assumes: A-12, A-16]` and `[Assumes: A-9]` added to C6 steps 1, 2 and 9, with A-12 and A-16 priced on C6's confidence line (B reaches at most 68 against C's 117); new chains C7 (GT-10, HIGH) and C8 (GT-9, HIGH) added and cited in §6; GT-6 to GT-8 now carry their derivation as their source; ledger, Assumption Audit scan and self-audit scan rows re-run against the current text. Re-score below.

**Criterion 1: Identify Essence**
Quoted span: "What actually limits how quickly a merged change reaches customers on this platform, and which intervention removes that limit at the lowest cost and risk — given that "deploys are too slow" can mean either that each deploy takes too long (pipeline latency, 45 min) or that too few deploys happen (throughput, 2/day)"
Band: **Rigorous**
Justification: One sentence naming the binding-constraint question rather than leadership's proposed solution, specific to this platform's 45-min/2-per-day figures, followed by five success criteria each checkable against §6 (latency/frequency/lead-time split shown, binding constraint named with a confirming measurement, cost in engineer-months against capacity on the same process basis, checkout risk priced, status quo and a composite included).

**Criterion 2: Challenge Assumptions**
Quoted span: "| C5 | 3 | fix 1–6 eng-months | A-10 (fix-cost bracket, now stated in A-10's row) | yes (amended in the gate's Fix step) |" and "| A-3: Every deploy must run the whole test suite on one runner, in series | convention | Challenge before use | Discard — splitting tests across runners …"
Band: **Rigorous**
Justification: Every row uses the four-type scheme with its prescribed treatment and an em-dash verdict; several are challenged or discarded (A-1, A-2, A-3, A-4, A-17, A-18); every unverified assumption used in a chain reads "unverified — flagged"; and the Assumption Audit scan covers every step of C1–C8 in order, with each surfaced assumption present in the table.

**Criterion 3: Establish Ground Truths**
Quoted span: comparison — enumeration "?-marked: GT-1?, GT-2?, GT-3?, GT-4?, GT-5? (5 of 10)"; the list carries `?` on exactly GT-1? to GT-5?, and the count 5 equals the enumeration's length. Unsuffixed GT-9 and GT-10 name read-at-source passages and feed HIGH chains C8 and C7; GT-1? to GT-5? each carry a Phase 3 failure record (source not supplied).
Band: **Rigorous**
Justification: Stable IDs match the chains, every entry has a provenance label, the enumeration matches the list, every reachable unsuffixed source feeds a HIGH chain, and GT-6 to GT-8 are definitions whose derivation is stated as their source.

**Criterion 4: Reason Upward**
Quoted span: "| C6 | C1–C5 + GT-9 | yes | n/a | yes | MEDIUM | yes | Self-Audit Gate Fix/Repeat (assumption marks added) |" and, for the assumption-mark limb, "→ weighted totals are C = 117, D = 100, B = 58, with A ruled out (arithmetic) [Assumes: A-12, A-16]"
Band: **Rigorous**
Justification: All eight chains conform in head-plus-arrow form, with clean dependencies and at least one intermediate each; every assumption-introducing step now carries its `[Assumes:]` mark; every figure recomputes (Recompute part of the adversarial pass); §5 records six dead ends in the What-was-tried / Why-abandoned / What-it-ruled-out form; and no analogy is used as evidence (the one external position, GT-9, is a read-at-source ground truth).

**Criterion 5: Validate**
Quoted span: "**Confidence:** MEDIUM — the Inputs axis is short: GT-1? and GT-2? are user-reported; the CI run history and deploy log for the last 90 days would remove them as a cause." and "K1 → **plan change:** the first step of the recommendation now includes mapping whatever decides when a deploy happens"
Band: **Rigorous**
Justification: Each chain names its weakest link and the axis that is short, with a verification path; C7 and C8 are HIGH on all three axes, and C1–C6 are MEDIUM with only Inputs short, which is what their axes license; the Conclusion's MEDIUM equals its weakest contributing chain; and the adversarial record has every part, with each pre-mortem cluster carrying a plan change or an accepted risk with a named mitigation, and K1 landing on C6's confidence line.

**Criterion 6: Conclusion-to-Ground-Truth Traceability**
Quoted span: "| Cost comparison: 3 vs 72 eng-months, ongoing costs excluded | bold lead-in | yes | bold lead-in whose colon closes the bold span | C5, C8 |" and, for the Key Insight limb, "\"Deploys are too slow\" describes two different problems. The pipeline is only 18.75% utilised (chain C1)"
Band: **Rigorous**
Justification: Every one of the nine §6 claims cites a §4 chain in the claim-inventory table, with zero untraced; and the Key Insight (the delay is release cadence, not pipeline time) is a finding the convention "slow deploys → microservices" does not reach, not a restatement of the recommendation.

No criterion Absent, no criterion Hand-wavy — gate cleared after one Fix/Repeat pass.

**Gate result:** cleared · passes: 2 · Fix/Repeat fired: yes

## Structured summary (process output)

```json
{
  "schema_version": 1,
  "run_mode": "full-composer",
  "assumptions": [
    {
      "id": "A-1",
      "type": "untested belief",
      "verdict": "Challenge"
    },
    {
      "id": "A-2",
      "type": "untested belief",
      "verdict": "Challenge"
    },
    {
      "id": "A-3",
      "type": "convention",
      "verdict": "Discard"
    },
    {
      "id": "A-4",
      "type": "convention",
      "verdict": "Discard"
    },
    {
      "id": "A-5",
      "type": "untested belief",
      "verdict": "Accept"
    },
    {
      "id": "A-6",
      "type": "convention",
      "verdict": "Accept"
    },
    {
      "id": "A-7",
      "type": "untested belief",
      "verdict": "Accept"
    },
    {
      "id": "A-8",
      "type": "untested belief",
      "verdict": "Accept"
    },
    {
      "id": "A-9",
      "type": "untested belief",
      "verdict": "Accept"
    },
    {
      "id": "A-10",
      "type": "untested belief",
      "verdict": "Accept"
    },
    {
      "id": "A-11",
      "type": "convention",
      "verdict": "Accept"
    },
    {
      "id": "A-12",
      "type": "untested belief",
      "verdict": "Accept"
    },
    {
      "id": "A-13",
      "type": "untested belief",
      "verdict": "Accept"
    },
    {
      "id": "A-14",
      "type": "untested belief",
      "verdict": "Accept"
    },
    {
      "id": "A-15",
      "type": "untested belief",
      "verdict": "Accept"
    },
    {
      "id": "A-16",
      "type": "untested belief",
      "verdict": "Accept"
    },
    {
      "id": "A-17",
      "type": "untested belief",
      "verdict": "Challenge"
    },
    {
      "id": "A-18",
      "type": "current constraint",
      "verdict": "Challenge"
    },
    {
      "id": "A-19",
      "type": "untested belief",
      "verdict": "Accept"
    },
    {
      "id": "A-20",
      "type": "untested belief",
      "verdict": "Accept"
    },
    {
      "id": "A-21",
      "type": "physical law",
      "verdict": "Accept"
    },
    {
      "id": "A-22",
      "type": "physical law",
      "verdict": "Accept"
    }
  ],
  "ground_truths": [
    {
      "id": "GT-1",
      "read_at_source": false
    },
    {
      "id": "GT-2",
      "read_at_source": false
    },
    {
      "id": "GT-3",
      "read_at_source": false
    },
    {
      "id": "GT-4",
      "read_at_source": false
    },
    {
      "id": "GT-5",
      "read_at_source": false
    },
    {
      "id": "GT-6",
      "read_at_source": true
    },
    {
      "id": "GT-7",
      "read_at_source": true
    },
    {
      "id": "GT-8",
      "read_at_source": true
    },
    {
      "id": "GT-9",
      "read_at_source": true
    },
    {
      "id": "GT-10",
      "read_at_source": true
    }
  ],
  "chains": [
    {
      "id": "C1",
      "confidence": "MEDIUM",
      "rests_on": [
        "GT-1?",
        "GT-2?",
        "GT-6"
      ]
    },
    {
      "id": "C2",
      "confidence": "MEDIUM",
      "rests_on": [
        "GT-1?",
        "GT-2?",
        "GT-7"
      ]
    },
    {
      "id": "C3",
      "confidence": "MEDIUM",
      "rests_on": [
        "GT-1?",
        "GT-8"
      ]
    },
    {
      "id": "C4",
      "confidence": "MEDIUM",
      "rests_on": [
        "GT-4?",
        "GT-10"
      ]
    },
    {
      "id": "C5",
      "confidence": "MEDIUM",
      "rests_on": [
        "GT-3?",
        "GT-5?",
        "GT-9"
      ]
    },
    {
      "id": "C6",
      "confidence": "MEDIUM",
      "rests_on": [
        "C1",
        "C2",
        "C3",
        "C4",
        "C5",
        "GT-9"
      ]
    },
    {
      "id": "C7",
      "confidence": "HIGH",
      "rests_on": [
        "GT-10"
      ]
    },
    {
      "id": "C8",
      "confidence": "HIGH",
      "rests_on": [
        "GT-9"
      ]
    }
  ],
  "dead_ends": [
    "Reruns make the pipeline the real limit (rival to C1)",
    "Microservices cut lead time more than the monolith fix (rival to C2 and C6)",
    "The 350 KLOC size itself causes the 45 minutes (rival to C3)",
    "Only microservices fix migrations that lock tables (rival to C4)",
    "Incremental (\"strangler\") extraction makes the migration cheap (rival to C5)",
    "Team independence is the real bottleneck (rival to C6)"
  ],
  "techniques": {
    "applied": [
      "inversion",
      "trade-off",
      "second-order",
      "pre-mortem"
    ],
    "not_applied": [
      {
        "technique": "theoretical-limit",
        "phase": 1,
        "reason": "whether 45 min is a convention or a hard bound does not decide the question; C1 shows the pipeline is not the binding constraint either way"
      },
      {
        "technique": "theoretical-limit",
        "phase": 4,
        "reason": "the lead-time floor (pipeline duration with zero wait) is already stated in C2 and C3; no physical ceiling is in play"
      },
      {
        "technique": "fishbone",
        "phase": 2,
        "reason": "the assumption space was enumerated through the inversion pass and the latency/throughput split; it is not multi-causal enough to need category brainstorming"
      },
      {
        "technique": "inversion",
        "phase": 5,
        "reason": "the conclusion is a plan, so Phase 5 used pre-mortem (the adversarial pass below); inversion was applied at Phase 2"
      }
    ]
  },
  "gate": {
    "passes": [
      {
        "bands": [
          "Rigorous",
          "Sound",
          "Hand-wavy",
          "Hand-wavy",
          "Rigorous",
          "Rigorous"
        ],
        "gate_cleared": true,
        "hand_wavy_cap_cleared": false
      },
      {
        "bands": [
          "Rigorous",
          "Rigorous",
          "Rigorous",
          "Rigorous",
          "Rigorous",
          "Rigorous"
        ],
        "gate_cleared": true,
        "hand_wavy_cap_cleared": true
      }
    ],
    "fix_repeat_fired": true,
    "cleared": true
  },
  "re_entry": {
    "fired": true,
    "edges": [
      {
        "edge": "the Self-Audit Gate's Fix/Repeat loop",
        "trigger": "On the first scoring pass, Criteria 3 and 4 scored Hand-wavy: two read-at-source ground truths fed only MEDIUM chains, and C6 had assumption steps without `[Assumes:]` marks."
      }
    ]
  },
  "conclusion": {
    "recommendation": "Do not start a microservice migration to solve deploy speed. Keep the monolith and fix the delivery process, in this order: measure CI stage times, the merge-to-deploy wait, and whatever decides when a deploy happens (approvals, QA sign-off, restart windows); split the test suite across 4–8 runners; switch to Puma phased (rolling) restarts with expand/contract migrations; then deploy each merge, or small groups of merges, as it lands (chain C6).",
    "confidence": "MEDIUM",
    "rests_on": [
      "C1",
      "C2",
      "C3",
      "C4",
      "C5",
      "C6",
      "C7",
      "C8"
    ]
  }
}
```
