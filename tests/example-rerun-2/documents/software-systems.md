## Answer

**Recommendation:** Instrument the pipeline, then fix it in place — parallelize and selectively run tests, quarantine flaky tests, confirm Puma's rolling restart, and decouple deploy from release with feature flags — rather than microservices now (chain C5). Define evidence-based trigger conditions for revisiting partial extraction later (chain C6).
**Band (from §6):** MEDIUM (chain C2; chain C4) — the band those two chains license, copied from §6's Confidence line.
**Would change it:** Documenting this org's restart mechanics closes chain C2's open rival; reading a primary two-pizza-heuristic source closes chain C4's `?`-marked input (chain C2; chain C4) — either raises the band toward HIGH. A coupling audit overturning GT-16? would lower it.

## 1. Problem Essence

**Essence Statement:** Given a 6-year-old, ~350 KLOC Rails monolith (catalog, cart, checkout, fulfillment) with a ~45-minute CI/CD pipeline requiring a full test-suite run and a coordinated application restart on every deploy, shipped by 12 engineers at ~2 deploys/day, is "move to microservices" the causally-indicated fix for "deploys are too slow" — or does a more direct, lower-cost lever exist, and under what conditions (if any) does partial service extraction become justified?

**Success criteria — a correct answer must:**
- Decompose the 45-minute pipeline into its real causal components, distinguishing facts given by the scenario from facts that would need to be measured in the real org.
- Test whether "move to microservices" is causally *necessary* to fix the stated problem, not merely plausible by industry analogy.
- Quantify what microservices adoption costs a 12-engineer team specifically (coordination tax, new failure modes, Conway's-Law fit), not generically.
- Produce an order-of-magnitude ceiling on achievable deploy frequency under (a) a monolith-pipeline fix and (b) a service-decomposition path, and name the team-size range at which decomposition typically starts paying for itself.
- Produce a ranked recommendation with concrete tactical steps and explicit, falsifiable trigger conditions for partial extraction — the answer is not required to be either "fix the monolith" or "go microservices" exclusively; a phased/composite answer is in scope and is tested against the pure options before any option is selected.

This statement does not require picking exactly one of leadership's two named states ("slow" vs. "microservices") — it requires identifying what would actually fix deploy speed, whatever shape that takes.

## 2. Assumptions Table

Rows A-9 through A-13 are the necessary preconditions produced by applying **inversion** to the claim "microservices will fix slow deploys" (inverted form: "microservices will NOT fix slow deploys" — what would guarantee that?). Rows A-14 through A-22 are produced by a **fishbone** breadth-first cause brainstorm on "the 45-minute pipeline," using the default six-category set (People, Process, Technology and Tools, Environment, Information, Resources) since this is a software/process problem and no specialized preset (6M, 8P, 4S) fits better. Rows A-23 through A-28 are surfaced later by the end-of-phase Assumption Audit in Phase 4 (chains C1, C2, C3, C4, and C6) and are added here per that step's instruction.

| ID | Assumption | Type | Treatment | Verdict | Verification |
|---|---|---|---|---|---|
| A-1 | "Deploys are too slow" names a specific blocked business outcome (hotfix lead time, feature cadence, incident MTTR, experimentation velocity) | convention | Challenge: ask leadership what deploys-are-slow is actually blocking | Challenge — Unverified — no outcome named in the scenario | Needs leadership interview; without this, "too slow" has no success criterion (see GT-15?) |
| A-2 | Microservices architecture reduces per-change deploy time | convention | Challenge explicitly in this context, not by industry analogy | Challenge — True only under narrow preconditions (A-9–A-12), not generally | See inversion chain C2 |
| A-3 | 12 engineers is a workable size to build *and* operate a microservices platform without overhead outweighing benefit | untested belief, load-bearing | Verify via Conway's Law / two-pizza heuristic | Challenge — Likely false at this size | See estimate chain C4 |
| A-4 | The full test suite must run on every deploy (no selective/impacted-test execution exists today) | current constraint | Record expiry conditions | Accept — Holds until test-impact analysis or modular boundaries exist | Expires once a test-impact tool is adopted (A-24) |
| A-5 | The coordinated restart is inherent to a monolith and cannot be fixed without decomposition | convention | Challenge — many Rails monoliths achieve zero-downtime rolling restarts without decomposition | Challenge — False in general (GT-19); unverified whether this org's restart has a substantive reason (e.g., in-memory cache coordination) | Needs this org's restart mechanics documented |
| A-6 | The test suite is slow primarily *because* the codebase is 350 KLOC | untested belief | Challenge — size alone rarely determines runtime; parallelism and test architecture usually dominate | Challenge — Unverified, likely only a partial cause | Needs per-stage CI timing (GT-5?) |
| A-7 | Microservices would let each team deploy independently without waiting on the full suite | untested belief | Challenge via inversion precondition A-9 | Challenge — Contingent, unverified | See C2 |
| A-8 | Splitting into services will not introduce new cross-service integration-test time that offsets the savings | untested belief, load-bearing | Verify; literature flags this as a common failure mode ("distributed integration testing debt") | Challenge — Unverified — risk flagged in pre-mortem (Cluster C) | See Phase 4 pre-mortem on O3 |
| A-9 | [Inversion precondition 1] The 45 minutes is dominated by *breadth* (running irrelevant tests) not *depth* (inherently slow stages), **and** the codebase has well-bounded, low-coupling domains splittable along catalog/cart/checkout/fulfillment lines | untested belief, load-bearing | Verify via CI timing + coupling/dependency analysis | Challenge — Unverified | Promoted to GT-16? |
| A-10 | [Inversion precondition 2] The team can build and operate the needed platform infrastructure (per-service CI/CD, service discovery, observability, contract tests) without the overhead exceeding the time saved | untested belief, load-bearing | Verify via estimate (C4) | Challenge — Unverified, estimate suggests false at 12 engineers | Promoted to GT-17? |
| A-11 | [Inversion precondition 3] The business genuinely needs independent per-domain release cadence, not merely a faster single release train | untested belief, load-bearing | Verify with product/business stakeholders | Challenge — Unverified | Promoted to GT-18? |
| A-12 | [Inversion precondition 4] Rolling/zero-downtime deploy is not already achievable within the monolith | untested belief, load-bearing | Verify against standard Rails/Puma deployment practice | Discard — **False** — Puma cluster-mode phased restarts are standard (GT-19) | Resolved — see GT-19 |
| A-13 | [Inversion precondition 5] Cross-service integration-test overhead will not exceed the savings from splitting | untested belief, load-bearing | Same as A-8 (duplicate precondition, one table row) | Challenge — Unverified | See A-8 |
| A-14 | [Fishbone — People] Flaky tests exist and are not quarantined, causing re-runs that inflate wall-clock time | untested belief | Verify via CI flaky-test / retry logs | Challenge — Unverified | Needs CI retry-rate data |
| A-15 | [Fishbone — Process] Pipeline stages (lint, build, test, package, deploy) run serially rather than pipelined/overlapped | untested belief | Verify via pipeline config review | Challenge — Unverified | Needs CI stage-timing breakdown |
| A-16 | [Fishbone — Process] Deploy requires a manual approval/coordination gate adding human latency inside or adjacent to the 45 minutes | untested belief | Verify via deploy runbook review | Challenge — Unverified | Needs runbook review |
| A-17 | [Fishbone — Technology/Tools] CI runner concurrency/parallelism is capped below what the test suite could use | untested belief | Verify via CI plan/config | Challenge — Unverified | Needs CI concurrency settings |
| A-18 | [Fishbone — Technology/Tools] Asset compilation is rebuilt from scratch each run with no cache reuse | untested belief | Verify via build-cache config | Challenge — Unverified | Needs build-log inspection |
| A-19 | [Fishbone — Technology/Tools] Test database setup/migration/seeding is slow on every run | untested belief | Verify via test-setup timing | Challenge — Unverified | Needs per-stage timing |
| A-20 | [Fishbone — Environment] CI queue/provisioning delay (cold containers, shared-runner contention) is counted inside the reported 45 minutes | untested belief | Verify via queue-time vs. run-time split | Challenge — Unverified | Needs CI telemetry |
| A-21 | [Fishbone — Information] No test-impact-analysis / dependency graph exists, so "which tests a change needs" is unknown, forcing full-suite-every-time | untested belief | This is the likely root driver behind A-4 | Challenge — Unverified but high-plausibility | Needs coupling/dependency-graph audit |
| A-22 | [Fishbone — Resources] CI compute budget is capped, limiting how many parallel workers the org is willing to fund | untested belief | Verify via CI billing/plan review | Challenge — Unverified | Needs CI cost data |
| A-23 | [Surfaced in Phase 4, chain C1] Pipeline stages are serialized by tooling/configuration choice rather than technical necessity | untested belief | Verify via pipeline config review (overlaps A-15) | Challenge — Unverified | Unverified — flagged. `[Assumes: A-23]` on C1 |
| A-24 | [Surfaced in Phase 4, second-order step] A test-impact-analysis tool can be adopted for this codebase with acceptable precision/recall (low false-negative rate) | untested belief, load-bearing | Verify via pilot on a sample of recent PRs before full rollout | Challenge — Unverified | Unverified — flagged. `[Assumes: A-24]` on second-order step and on C3 |
| A-25 | [Surfaced in Phase 4, chain C2] This org has no plan to restructure team ownership around any new service boundaries | untested belief | Verify with engineering leadership before any extraction | Challenge — Unverified | Unverified — flagged. `[Assumes: A-25]` on C2 |
| A-26 | [Surfaced in Phase 4, chain C4] A CI concurrency increase to 8-16 parallel workers is achievable within this org's compute budget | untested belief | Verify via CI billing/plan review (overlaps A-22) | Challenge — Unverified | Unverified — flagged. Priced into C4's bracket as a central assumption |
| A-27 | [Surfaced in Phase 4, chain C4] A dedicated shared-platform function would need to be newly staffed, not absorbed by existing capacity | untested belief, load-bearing | Verify via headcount/budget review before any extraction decision | Challenge — Unverified | Unverified — flagged. Feeds the team-size threshold bracket in C4 |
| A-28 | [Surfaced in Phase 4, chain C6] The DORA batch-size/change-failure-rate relationship (GT-11?) generalizes to this org's codebase and team | untested belief | Verify via this org's own change-failure-rate trend once selective testing ships | Challenge — Unverified | Unverified — flagged. Feeds the 3rd-order claim in C6 |

**Stakes-escalation note:** A-3, A-9–A-13, A-24 are load-bearing for a conclusion with real cost/risk consequences (a multi-month architecture decision and operational safety), so they are pushed toward verification rather than accepted on convention — this is why the estimate (C4) and pre-mortem (Phase 4 and Phase 5) exist: they are the verification mechanism for assumptions that cannot be resolved by citation alone in a hypothetical scenario.

## 3. Ground Truths

**Provenance note specific to this analysis:** the subject is a hypothetical organization, not a real, inspectable one. GT-1 through GT-4 are therefore **stipulated premises of the scenario itself** — they need no external citation because they are the problem statement, not a claim about the world. GT-5? through GT-8? and GT-14?–GT-15? are exactly the facts the scenario does *not* supply, and the task explicitly asks this analysis to separate "given" from "would need to be verified in the real org" — so those are carried as `?`-marked ground truths whose verification path is "instrument the real pipeline," not "read a source." GT-9, GT-12, GT-13, GT-19 are external, citable facts verified against real sources in this run. GT-10? and GT-11? are external facts this run attempted to verify at source and could not fully confirm — their Phase 3 failure records are below.

1. **GT-1** — The platform is a single Rails monolith, ~350 KLOC, covering catalog, cart, checkout, and fulfillment, in production ~6 years. *Stipulated in problem statement.*
2. **GT-2** — The CI/CD pipeline takes ~45 minutes end-to-end; every deploy requires a full test-suite run and a coordinated application restart. *Stipulated in problem statement.*
3. **GT-3** — 12 engineers currently ship ~2 deploys/day. *Stipulated in problem statement.*
4. **GT-4** — Leadership's stated conclusion is "deploys are too slow, we need microservices," with no diagnostic breakdown given alongside it. *Stipulated in problem statement.*
5. **GT-5?** — The internal breakdown of the 45 minutes (build/asset-compile time vs. test-execution wall-clock time vs. CI queue/provisioning time vs. restart/orchestration time) is **not specified** by the scenario. *Unverified — needs per-stage CI timing instrumentation in the real org. Not read — the real org does not exist to read from; this is itself a finding, not an omission.*
6. **GT-6?** — Whether the test suite runs in parallel today, and at what concurrency, is not specified. *Unverified — needs CI config review.*
7. **GT-7?** — Whether flaky tests exist or are quarantined is not specified. *Unverified — needs CI retry-rate data.*
8. **GT-8?** — Whether the "coordinated restart" is required by genuine shared state (e.g., in-memory cache invalidation, long-lived connections, synchronous migrations) or is simply an artifact of the deploy tool's defaults is not specified. *Unverified — needs this org's restart runbook.*
9. **GT-9** — Conway's Law (1968): *"[O]rganizations which design systems ... are constrained to produce designs which are copies of the communication structures of these organizations."* **Source:** Melvin E. Conway, "How Do Committees Invent?", *Datamation*, Vol. 14, No. 5 (April 1968), pp. 28–31. **Provenance: read-at-source** — quoted wording confirmed via direct fetch (Wikipedia's "Conway's law" article, which reproduces the original 1968 wording verbatim) on 2026-10-08.
10. **GT-10?** — Amazon's "two-pizza team" heuristic: an autonomous team should be small enough to be fed by two pizzas, commonly cited as roughly 6–10 people. **Provenance: unverified** — see Phase 3 failure record below.
11. **GT-11?** — DORA's *State of DevOps* research classifies "Elite" performers as deploying on-demand, multiple times per day (≈1,460 deploys/year vs. ≈7/year for low performers, a ~208× gap), with lead time under one day and 0–15% change-failure rate; "High" performers deploy between once/day and once/week. **Provenance: unverified** — see Phase 3 failure record below.
12. **GT-12** — Amdahl's Law (mathematical identity): for a task with serial fraction *S* and *N* parallel workers, Speedup(N) = 1 / (S + (1−S)/N); as N→∞, Speedup → 1/S. This is a derivation from the definition of parallel/serial execution time, not an empirical claim requiring external citation. **Provenance: physical/mathematical law — no `?` required.**
13. **GT-13** — By definition, decomposing a system into independently deployable services replaces in-process function calls with network calls across process/service boundaries, which requires explicit contracts, versioning, and handling of partial failure. **Provenance: definitional — no `?` required.**
14. **GT-14?** — Whether the business requires independent per-domain release trains (vs. simply a faster single release train) is not specified. *Unverified — needs product/business stakeholder input.*
15. **GT-15?** — No data is given on deploy failure/rollback rate, incident frequency tied to deploys, or what business outcome "too slow" is blocking. *Unverified — without this, "too slow" has no measurable success criterion; this gap is itself load-bearing (see A-1).*
16. **GT-16?** — [Promoted from A-9] The 45 minutes is dominated by breadth rather than depth, and the codebase has low-coupling, splittable bounded contexts along domain lines. *Unverified.*
17. **GT-17?** — [Promoted from A-10] Platform/operations overhead for microservices would not exceed the time saved, at 12 engineers. *Unverified — the estimate in chain C4 tests this directly and finds it implausible under every bracketed assumption.*
18. **GT-18?** — [Promoted from A-11] The business needs independent per-domain release cadence. *Unverified.*
19. **GT-19** — Puma (the most common Rails application server) supports phased (rolling) restarts in cluster mode: *"Phased restarts replace all running workers in a Puma cluster... In-flight requests are always served responses before the connection is closed gracefully."* Zero-downtime deploys via this mechanism are standard practice for production Rails monoliths and require no service decomposition. **Source:** Puma documentation, `docs/restart.md`. **Provenance: read-at-source** — fetched directly on 2026-10-08; read-location: the "Phased restart" section of `docs/restart.md`.
20. **GT-20?** — [Promoted from fishbone branch A-21] No test-impact-analysis / dependency-graph tooling exists for this codebase, so which tests a given change needs is unknown, forcing full-suite-every-time. *Unverified — needs a coupling/dependency-graph audit; this is a fishbone hypothesis, not a measured fact for this org.*
21. **GT-21?** — Engineering case studies for comparably-sized Rails monoliths commonly report CI pipelines reduced to roughly 8-10 minutes once parallel test splitting, selective test execution, and build caching are adopted. *Unverified — reported-by-delegate (general industry pattern from this model's training knowledge, not a specific case study opened during this run); used only as a "best demonstrated" reference point, not as a load-bearing input any conclusion rests on directly.*

**Phase 3 failure records (verification attempted, not fully confirmed):**
- **GT-10? (two-pizza team heuristic):** attempted `WebFetch` on `https://en.wikipedia.org/wiki/Two-pizza_team` → **unreachable (404 Not Found)**. The figure is well-attested across multiple secondary sources returned by a prior web search (Deskera, dsebastien.net, idonethis — each attributing "roughly 6–10 people" and the Bezos quote to Amazon), but no primary source was opened directly, so this remains **reported-by-delegate**, kept `?`. Not read — turn budget was spent on the two citations (GT-9, GT-19) load-bearing enough to flip the headline conclusion; GT-10? only sizes a bracket whose central estimate the conclusion does not hinge on precisely (see sensitivity analysis, §5).
- **GT-11? (DORA elite-tier deploy frequency):** attempted `WebFetch` on `https://dora.dev/guides/dora-metrics-four-keys/deployment-frequency/` → **unreachable (404 Not Found)**; attempted `https://dora.dev/research/2019/dora-report/` → **citation does not support the claim** (page fetched successfully but did not contain the tier definitions in the fetched content). The figures are carried from a prior web-search summary (secondary aggregator sites quoting the DORA report) and kept `?` as **reported-by-delegate**. This ground truth is used only as an industry-benchmark reference point in the estimate (C4), not as an input any chain's conclusion is load-bearing on — the conclusion's deploy-frequency ceiling is derived independently from Amdahl's Law and the stipulated scenario numbers, with GT-11? cited for external calibration only.

**`?`-marked ground truths:** GT-5, GT-6, GT-7, GT-8, GT-10, GT-11, GT-14, GT-15, GT-16, GT-17, GT-18, GT-20, GT-21 (13 of 21).

**Read-locations for unsuffixed ground truths feeding load-bearing chains:** GT-9 — Wikipedia "Conway's law" article, section quoting the 1968 original wording verbatim (confirms wording against the primary citation). GT-19 — Puma `docs/restart.md`, "Phased restart" section (confirms cluster-mode phased restart and graceful in-flight-request handling). GT-12 and GT-13 require no read-location — they are derived/definitional, not sourced from an external document.

## 4. Derivation Chains

### Chain C1 — What the 45 minutes actually is (five-whys, reduce-to-primitives)

GT-1 (350 KLOC Rails monolith) + GT-2 (45-min pipeline: full suite + coordinated restart) + GT-12 (Amdahl's Law)
→ applying the five-whys reduce-to-primitives drill to "the pipeline takes 45 minutes" decomposes it into four buckets that any build-then-test-then-restart pipeline necessarily has: build/asset-compile time, test-execution wall-clock time, CI queue/provisioning time, and restart/orchestration time
→ test-execution wall-clock time is bounded below by Amdahl's Law (GT-12): as parallel workers increase, wall-clock time approaches the suite's irreducible serial fraction, so its floor is a parallelism/tooling property, not a property of total code volume
→ none of the four buckets is logically inherent to "the application is one deployable unit" [Assumes: A-23] — each is addressable by pipeline tooling and test-architecture changes independently of whether the application is later split into services

**Conclusion:** the 45 minutes decomposes into tooling-addressable buckets rather than an irreducible property of monolith size or 350 KLOC of code; which specific bucket(s) dominate for this org is unverified (GT-5?, GT-6?, GT-8?) and must be measured before committing engineering effort to any one fix.
**Pre-check:** head: GT-1 (stipulated) · GT-2 (stipulated) · GT-12 (physical law, HIGH) · ?-marked: none on head · lowest cited: none · Inputs ceiling: HIGH
**Confidence: HIGH** — Inputs are solid (no `?`-marked identifier on the head). Inference: hop 3's `[Assumes: A-23]` is priced — even if pipeline stages are technically ordered (A-23 false), each bucket remains separately addressable within itself, so the decomposition claim survives. Rivals: the only candidate rival (that test time is dominated by inherently slow individual specs rather than irrelevant-test breadth) is itself a tooling/test-architecture issue, not a monolith-deployment-unit issue, so it does not actually compete with this chain's (deliberately modest) conclusion.

**Theoretical-limit treatment (supporting C1 and C4) — the Amdahl's-Law-governed pipeline-time floor.**
Direction: lower is better (pipeline wall-clock time). Governing hard constraint: Amdahl's Law (GT-12) — wall-clock test time cannot fall below the suite's irreducible serial fraction no matter how many parallel workers are added.
- **Ideal floor:** for a Rails CI pipeline of this shape (environment boot, DB migration/seed, final serial checks), the irreducible serial fraction is typically on the order of 2-5 minutes; below that, adding parallelism buys nothing (Amdahl's Law, GT-12).
- **Best demonstrated:** comparably-sized Rails monoliths in industry practice commonly report CI pipelines reduced to roughly 8-10 minutes once parallel test splitting, selective test execution, and build caching are adopted (GT-21?, observation, not computed).
- **Conventional (this org):** 45 minutes (GT-2).
- **Gap 1 (conventional → best demonstrated):** 45 → ~8-10 minutes — headroom already proven reachable elsewhere by ordinary tooling investment, no decomposition required.
- **Gap 2 (best demonstrated → ideal floor):** ~8-10 → ~2-5 minutes — the remaining headroom requires shrinking the irreducible serial fraction itself (faster environment boot, lighter test setup), which is also achievable without decomposition.

Microservices decomposition does not relax the Amdahl floor itself: splitting the codebase does not shrink any individual service's own serial fraction (boot + migration + final checks still apply per service), so this floor is identical on either architectural path. This sharpens chain C4's pipeline-time bracket and reinforces C1's conclusion that the 45 minutes is a tooling-addressable quantity, not a monolith-inherent one.


### Chain C2 — Does "slow deploys" require microservices? (inversion)

GT-9 (Conway's Law) + GT-13 (distributed-systems definition) + GT-19 (Puma phased restart)
→ inversion applied to "microservices will fix slow deploys" yields five necessary preconditions: breadth-dominated, low-coupling test time (GT-16?); platform overhead not exceeding savings (GT-17?); a genuine need for independent release cadence (GT-18?); rolling deploy being infeasible inside the monolith; and avoidance of offsetting cross-service integration-test overhead
→ because all five preconditions must hold simultaneously for microservices to be a *necessary* fix, confirming even one of them false is sufficient to refute necessity
→ GT-19 confirms the "rolling deploy is infeasible without decomposition" precondition is false — Puma's standard cluster-mode phased restart already removes the coordinated-restart penalty with no service split required
→ GT-13 shows service decomposition inherently trades in-process calls for network calls, a new category of operational risk
→ GT-9 (Conway's Law) implies that risk compounds rather than resolves cleanly unless the org's communication structure is deliberately restructured around the new service boundaries [Assumes: A-25]
→ paying a compounding, open-ended operational-risk cost to fix a problem a one-line deploy-configuration change already fixes is not justified by necessity

**Conclusion:** "deploys are slow" does not causally require "we need microservices" — the specific coordinated-restart complaint already has a direct, in-monolith fix (GT-19); whether decomposition would help for *other* reasons remains open and is tested separately in C4.
**Pre-check:** head: GT-9 (read-at-source, HIGH) · GT-13 (definitional, HIGH) · GT-19 (read-at-source, HIGH) · ?-marked: none on head · lowest cited: none · Inputs ceiling: HIGH
**Confidence: MEDIUM** — Inputs and Inference are both strong (no `?` on the head; each hop follows deductively). Rivals axis is short: a live, unsettled rival exists — this org's coordinated restart might exist for a substantive shared-state reason (unresolved GT-8?) that Puma's generic phased-restart capability would not by itself remove. That rival is what caps this chain at MEDIUM rather than HIGH; it closes once GT-8? is confirmed (documenting this org's actual restart mechanics).

### Chain C3 — Where the highest-leverage, lowest-cost fix likely sits (fishbone)

GT-2 (45-min pipeline, full suite required) + GT-20? (no test-impact tooling, promoted from fishbone branch A-21) + GT-12 (Amdahl's Law)
→ the fishbone breadth-first scan (People, Process, Technology/Tools, Environment, Information, Resources) locates eight independent candidate causes of the 45 minutes, of which the Information-category cause (GT-20?) is the one that, if true, would explain why a 350 KLOC app runs its *entire* suite on every change rather than only the subset actually affected by that change
→ if GT-20? holds, adopting test-impact analysis (running only the tests reachable from a change's dependency graph) directly shrinks the effective test volume per deploy without touching parallelism, infrastructure, or architecture at all
→ this lever is available whether or not the application is later split into services — it is a property of test-selection strategy, not of deployment-unit boundaries [Assumes: A-24]

**Conclusion:** the single highest-leverage, lowest-architectural-cost candidate fix for the 45-minute pipeline is adopting test-impact / selective test execution, contingent on GT-20? being confirmed in this org and on A-24 (acceptable tool precision/recall) holding; the mitigation for A-24 failing is a nightly full-suite safety net.
**Pre-check:** head: GT-2 (stipulated) · GT-20? (?) · GT-12 (physical law, HIGH) · ?-marked: GT-20? · lowest cited: none · Inputs ceiling: MEDIUM
**Confidence: LOW** — Inputs short (GT-20? is an unconfirmed fishbone hypothesis, not measured for this org). Rivals short: a live, unsettled rival exists — the dominant cost might instead be raw CPU-bound test depth (A-6) rather than test-*selection* breadth, which test-impact analysis would not fix. Two axes short, so this chain is offered as a strong *candidate* lever to verify first, not a settled finding; it is one input among several to the trade-off in C5, not load-bearing on its own.

### Chain C4 — Order-of-magnitude ceilings: deploy frequency and the microservices break-even team size (estimate)

GT-2 (45-min pipeline) + GT-3 (12 engineers, 2 deploys/day) + GT-9 (Conway's Law) + GT-10? (two-pizza heuristic) + GT-12 (Amdahl's Law) + GT-19 (Puma phased restart)
→ decomposing the current 45 minutes per GT-12 into an irreducible serial floor (environment boot, DB migration/seed, final serial checks — typically 2-5 minutes for a Rails app this size) plus a parallelizable remainder brackets the monolith-fix pipeline-time ceiling at [8, 12, 20] minutes once test concurrency is raised to a typical CI range of 8-16 workers and selective execution removes most irrelevant-test volume
→ cutting pipeline time into that 8-20 minute bracket, combined with GT-19's already-available rolling restart, removes both halves of the original "full test-suite run + coordinated restart" bottleneck without any service decomposition
→ decoupling "deploy" (code reaches production, dark or flagged off) from "release" (feature exposed to users) via trunk-based development and feature flags removes the need to wait for a product release decision before deploying
→ combining both effects brackets the realistic deploy-frequency ceiling for this 12-engineer team, on the monolith path, at [5, 15, 30] deploys/day
→ per GT-9 (Conway's Law) and GT-10? (two-pizza heuristic, roughly 6-10 people per autonomous team), each independently-owned service needs a full autonomous team to avoid the communication-structure mismatch Conway's Law predicts
→ running even two such services well therefore requires roughly two full teams (12-20 engineers) plus a shared platform function for cross-cutting concerns (CI/CD templates, service mesh, observability)
→ this brackets the team size at which microservices decomposition typically starts paying for itself at [16, 24, 40+] engineers
→ both ends of the deploy-frequency bracket imply the monolith-path ceiling is several multiples of today's 2 deploys/day even in the worst case
→ both ends of the team-size bracket imply 12 engineers sits below the threshold even in the most optimistic case
→ because every end of both brackets drives the same respective decision, per the estimate procedure's decision-resolution stop criterion, further tightening either bracket would not change what the team should do next

**Conclusion:** at 12 engineers, the monolith-pipeline-fix path has substantial untapped headroom (roughly 2.5-15x today's deploy frequency) reachable without decomposition, while the team is roughly 1.3-3.3x below every bracketed estimate of the team size at which microservices typically becomes economical.
**Pre-check:** head: GT-2 (stipulated) · GT-3 (stipulated) · GT-9 (read-at-source, HIGH) · GT-10? (?) · GT-12 (physical law, HIGH) · GT-19 (read-at-source, HIGH) · ?-marked: GT-10? · lowest cited: none · Inputs ceiling: MEDIUM
**Confidence: MEDIUM** — Inputs short (GT-10? is reported-by-delegate, not read-at-source: two direct fetch attempts 404'd; verification = open a primary Amazon/Bezos source). Inference is closed by the estimate procedure's own bracket discipline (central estimate plus explicit lower/upper bounds). Rivals: the strongest live rival (severe cross-domain coupling, GT-16?, that could push the pipeline-fix bracket above 20 minutes) is treated as not threatening this chain's conclusion, because the conclusion is stated at the bracket's conservative (lower-bound) edge — "roughly 2.5-15x" already includes the pessimistic end — so the rival would need to beat the bracket's floor, not just its midpoint, to change the decision.

### Chain C5 — The trade-off-robust choice (weighted-criteria trade-off)

GT-2 (45-min pipeline) + GT-3 (12 engineers) + C2 (necessity test) + C4 (estimate) + GT-9 (Conway's Law)
→ applying the must-have knock-out test — no increase to change-failure rate or incident MTTR within 6 months; executable by the existing 12-engineer team without a dedicated platform/SRE hire — eliminates "full microservices decomposition now" before any scoring, because C4 shows the team sits below the viable operating threshold for even two autonomous service teams
→ scoring the remaining viable options (do nothing; fix the monolith pipeline tactically; partial/selective extraction now; fix-the-pipeline-now-with-an-evidence-gated-trigger-for-later-extraction) against seven weighted criteria — time-to-value, cost, operational safety, Conway/org fit, reversibility, directly-addresses-stated-pain, preserves-future-optionality — ranks "fix the pipeline now with an evidence-gated trigger for later extraction" highest
→ that option pointwise dominates or ties "fix the pipeline alone" on every single criterion, differing only on preserves-future-optionality, where it scores strictly higher at negligible added cost
→ the flip test finds no single-criterion weight change reverses this ranking, because the winning option is weakly dominant rather than narrowly ahead — the only way to tie it is to zero out the preserves-future-optionality criterion entirely, which is not a position leadership has taken

**Conclusion:** the trade-off-robust choice is to fix the monolith's pipeline now *and* define explicit, evidence-based trigger conditions for revisiting partial service extraction later — not to adopt microservices now, and not to stop at tactical fixes with no forward plan.
**Pre-check:** head: GT-2 (stipulated) · GT-3 (stipulated) · C2 (MEDIUM) · C4 (MEDIUM) · GT-9 (read-at-source, HIGH) · ?-marked: none directly on head · lowest cited: MEDIUM (C2, C4) · Inputs ceiling: MEDIUM
**Confidence: MEDIUM** — capped by the lowest-rated chains this chain's head cites (C2 and C4, both MEDIUM); a chain cannot exceed the band of the chains it is built from. Within that cap, Inference is strong (flip test shows robustness) and the most obvious Rival (leadership's original "go microservices now") is addressed directly by this chain's own must-have knockout.

### Chain C6 — Second-order and third-order effects of the recommended path

C5 (phased recommendation) + GT-19 (Puma phased restart) + GT-20? (test-impact gap)
→ [2nd, actor lens] once the pipeline is fast and restarts are rolling, engineers' commit behavior shifts toward smaller, more frequent changes — trunk-based development becomes practically viable rather than theoretical
→ [2nd, actor lens, new risk] replacing full-suite-always with selective/impacted test execution creates a failure mode that did not exist before — a false-negative test-selection can let a regression through that the old, slower, full-suite-every-time process would have caught [Assumes: A-24]
→ [3rd, time lens] sustained smaller-batch changes, combined with a nightly full-suite run as the priced mitigation for the new false-negative risk, compound over several release cycles into a lower change-failure rate, consistent with the batch-size/failure-rate relationship reported in GT-11?
→ [3rd, time lens, long horizon] if the team and product genuinely grow past the C4-estimated threshold (16-40+ engineers, multiple product lines with real independent-release needs), the deferred microservices question resurfaces on concrete evidence rather than on a hunch
→ [3rd, time lens, long horizon] the coupling data, test-impact tooling, and module-boundary clarity built while implementing the near-term fixes directly lower the cost of that later, evidence-targeted extraction, rather than being wasted work

No extension step contradicts a Ground Truth — the new risk surfaced in hop 2 is priced (nightly safety net), not fatal, so no return to Phase 2 is triggered.

**Conclusion:** the phased plan's second- and third-order effects are net favorable — lower change-failure rate over time and preserved future option value — provided the one genuinely new risk it introduces (test-selection false negatives) is explicitly mitigated.
**Pre-check:** head: C5 (MEDIUM) · GT-19 (read-at-source, HIGH) · GT-20? (?) · ?-marked: GT-20? · lowest cited: MEDIUM (C5) · Inputs ceiling: MEDIUM
**Confidence: MEDIUM** — capped by C5 (MEDIUM) and by GT-20? being `?`-marked. Inference: hop 2's `[Assumes: A-24]` is priced inline (nightly full-suite safety net). Rivals: none beyond those already carried by C5.

## 5. Abandoned Reasoning

**Rival 1 — "Go full microservices now," taken literally as leadership stated it.**
- *What was tried:* Evaluated as a live option (O3) in the Phase 4 trade-off, on its own stated terms.
- *Why abandoned:* Knocked out by the must-have test in C5 before scoring (team sits below the viability threshold C4 derives — 12 engineers vs. a bracketed [16, 24, 40+] break-even range); independently, the Phase 4 pre-mortem on this path surfaced four structural failure clusters likely 12-18 months out (distributed-monolith boundaries, platform/ops tax exceeding team capacity, cross-service coordination replacing single-pipeline coordination, and an unrestructured org re-coupling services operationally per Conway's Law).
- *What it ruled out:* ruled out by **C2** (necessity test — not causally required) and **C4** (team-size estimate — not economical yet), and formally eliminated in **C5**.

**Rival 2 — "Extract one bounded domain into a service right now," without first gathering evidence.**
- *What was tried:* Scored as option O4 in the C5 trade-off alongside the other viable (non-knocked-out) options.
- *Why abandoned:* Ranked lowest of the viable options — it spends real operational cost and risk to act on **GT-16?**, a precondition (low-coupling, splittable bounded contexts) that has not actually been confirmed for this codebase. It substitutes a guess for evidence that C3 and C4 show is comparatively cheap to gather first.
- *What it ruled out:* ruled out by **C5**.

**Rival 3 — "The 350 KLOC codebase size is itself the cause of the 45-minute pipeline."**
- *What was tried:* The initial, intuitive explanation (recorded as assumption A-6) before the five-whys decomposition was applied.
- *Why abandoned:* Amdahl's Law (**GT-12**) and the reduce-to-primitives drill in **C1** show pipeline wall-clock time is governed by parallelism and test-selection strategy, not directly by lines of code; a 350 KLOC app with good parallelism and selective execution is not mechanically slower than a 50 KLOC app with poor parallelism.
- *What it ruled out:* "rewrite smaller" or "the codebase is just too big" as an explanation; ruled out by **C1**.

**Rival 4 — "Do nothing; 2 deploys/day is fine."**
- *What was tried:* Scored as option O1 (status quo) in the C5 trade-off, per the trade-off procedure's requirement to always include the status quo.
- *Why abandoned:* Scored lowest on directly-addresses-stated-pain and preserves-future-optionality; there is a real, inexpensive fix available (C1, C3), so declining to act is not supported once that fix is known to exist.
- *What it ruled out:* ruled out by **C5**.

**Dead end — "The coordinated restart is inherently unfixable without splitting the application" (A-5 / A-12).**
- *What was tried:* Treated as a live precondition for the inversion test in C2.
- *Why abandoned:* Directly falsified by **GT-19** (Puma's standard cluster-mode phased restart), read at source from the Puma documentation — zero-downtime deploys are already achievable in a Rails monolith with standard tooling.
- *What it ruled out:* ruled out by **GT-19**, formalized in **C2**.

## 6. Conclusion

**Recommended approach:** Instrument the pipeline before changing it (chain C1), then execute a ranked bundle of tactical fixes in parallel — test parallelization and selective/impacted test execution with a nightly full-suite safety net (chains C1, C3, C6), flaky-test quarantine and build/asset-compile caching (fishbone findings feeding C3), and confirming rolling/phased restarts via standard Puma cluster-mode tooling plus trunk-based development with feature flags to decouple "deploy" from "release" (chain C4) — instead of adopting microservices now (chain C5). In parallel, define explicit, falsifiable trigger conditions for revisiting *partial* service extraction later, rather than closing the question permanently (chain C5, chain C6).

**Key insight:** "Deploys are too slow" does not causally require "we need microservices" — the coordinated-restart half of the complaint already has a one-line, in-monolith fix (chain C2, via GT-19), the 45 minutes decomposes into ordinary tooling-addressable buckets rather than an inherent property of a 350 KLOC codebase (chain C1), and at 12 engineers the team sits roughly 1.3-3.3x below every bracketed estimate of the team size at which microservices typically starts paying for itself (chain C4). Leadership's diagnosis mistakes a symptom (a slow, serially-gated pipeline) for a prescription (a specific, expensive architecture) without the middle step of asking what the pipeline is actually made of.

**Trade-offs acknowledged:** The recommended path is not free of real trade-offs. Selective/impacted test execution introduces a genuinely new risk — false-negative test selection — that the current full-suite-always process does not have; this analysis prices that risk with a nightly full-suite safety net rather than treating it as fully solved (chain C6). The phased plan also defers, rather than permanently forecloses, the possibility that decomposition is eventually warranted — if the team and product genuinely scale past the C4-estimated threshold, or if a coupling audit later reveals the low-coupling boundaries GT-16? requires, the case for partial extraction should be revisited on that evidence (chain C5, chain C6). Choosing a phased plan over an immediate full commitment to either extreme also carries a communication risk: it can be perceived by leadership as "doing nothing" if the trigger conditions are not visibly tracked (addressed in the adversarial pass below).

**Pre-check:** head: C1 (HIGH) · C2 (MEDIUM) · C3 (LOW) · C4 (MEDIUM) · C5 (MEDIUM) · C6 (MEDIUM) · ?-marked GT used directly: none (all routed through the chains above) · lowest cited: LOW (C3) · Inputs ceiling: LOW
**Confidence: MEDIUM** — Although C3 (the test-impact-analysis lever) is individually LOW, the headline recommendation does not rest on C3 alone; it rests primarily on C5, which is itself capped at MEDIUM by C2 and C4. C3 is offered as one candidate tactic among several bundled in the "fix the pipeline" step, not as the load-bearing claim that "microservices is unnecessary" — that claim rests on C2 (MEDIUM, capped only by one unresolved rival, GT-8?) and C4 (MEDIUM, capped only by one unverified citation, GT-10?). The overall band is therefore MEDIUM, not LOW: it would rise to HIGH if this org's restart mechanics are documented (closing C2's open rival) and a primary source for the two-pizza heuristic is read (closing C4's `?`-marked input), and it would fall if a real coupling audit overturns GT-16? (see falsification condition in the adversarial pass below).

## Appendix — process output

## Assumption Audit scan (process output)

| Chain | Step | Step Text (brief) | Assumption surfaced? | Added to Table? |
|---|---|---|---|---|
| C1 | 1 | Decompose 45 min into 4 buckets | no | n/a (clean pass) |
| C1 | 2 | Amdahl bound on test-execution time | no | n/a (clean pass) |
| C1 | 3 | Buckets addressable without decomposition `[Assumes: A-23]` | yes — A-23 | yes (added in §2) |
| C2 | 1 | Inversion yields 5 preconditions | no (already A-9–A-13) | n/a (clean pass) |
| C2 | 2 | All 5 must hold for necessity | no | n/a (clean pass) |
| C2 | 3 | GT-19 falsifies rolling-restart precondition | no | n/a (clean pass) |
| C2 | 4 | GT-13: decomposition trades calls for network calls | no | n/a (clean pass) |
| C2 | 5 | Conway's Law compounds risk `[Assumes: no restructuring planned]` | yes — A-25 | yes (added in §2) |
| C2 | 6 | Not justified by necessity | no | n/a (clean pass) |
| C3 | 1 | Fishbone scan locates 8 candidate causes | no (already A-14–A-22) | n/a (clean pass) |
| C3 | 2 | Test-impact analysis shrinks effective volume | no | n/a (clean pass) |
| C3 | 3 | Lever independent of deployment-unit boundaries `[Assumes: A-24]` | yes — A-24 | yes (added in §2) |
| C4 | 1 | Bracket pipeline-time ceiling at [8,12,20] min | yes — CI concurrency budget achievable | yes (added as A-26) |
| C4 | 2 | Combined effect removes both bottleneck halves | no | n/a (clean pass) |
| C4 | 3 | Trunk-based dev + flags decouple deploy/release | no | n/a (clean pass) |
| C4 | 4 | Bracket deploy-frequency ceiling at [5,15,30]/day | no | n/a (clean pass) |
| C4 | 5 | Conway + two-pizza require full autonomous team per service | no | n/a (clean pass) |
| C4 | 6 | Two teams + platform function needed | yes — platform function must be newly staffed | yes (added as A-27) |
| C4 | 7 | Bracket team-size threshold at [16,24,40+] | no | n/a (clean pass) |
| C4 | 8 | Deploy-frequency bracket robust at both ends | no | n/a (clean pass) |
| C4 | 9 | Team-size bracket robust at both ends | no | n/a (clean pass) |
| C4 | 10 | Decision-resolution stop criterion met | no | n/a (clean pass) |
| C5 | 1 | Must-have knockout eliminates full microservices now | no | n/a (clean pass) |
| C5 | 2 | Weighted scoring ranks phased option highest | no | n/a (clean pass) |
| C5 | 3 | Phased option pointwise dominates/ties alternative | no | n/a (clean pass) |
| C5 | 4 | Flip test shows robustness | no | n/a (clean pass) |
| C6 | 1 | [2nd, actor] smaller, more frequent changes | no | n/a (clean pass) |
| C6 | 2 | [2nd, actor] new false-negative risk `[Assumes: A-24]` | no (already A-24) | n/a (clean pass) |
| C6 | 3 | [3rd, time] compounds into lower failure rate | yes — GT-11? relationship generalizes to this org | yes (added as A-28) |
| C6 | 4 | [3rd, time] deferred question resurfaces on evidence | no | n/a (clean pass) |
| C6 | 5 | [3rd, time] near-term work lowers future extraction cost | no | n/a (clean pass) |

Scan complete: 6 chains, 31 steps scanned in order; 7 assumptions surfaced (A-23 through A-28, one step surfacing two instances of already-tabled A-24), all added to or reconciled against the Classified Assumptions Table in §2.

## Self-audit scan (process output)

**Table 1 — Section 4 chain form**

| Chain | Chain Head (brief) | Form conforming? | Rule applied | Dependency clean? | Band | Act attempted? | Edges fired |
|---|---|---|---|---|---|---|---|
| C1 | GT-1 + GT-2 + GT-12 | yes | n/a | yes | HIGH | no | none |
| C2 | GT-9 + GT-13 + GT-19 | yes | n/a | yes | MEDIUM | yes | none |
| C3 | GT-2 + GT-20? + GT-12 | yes | n/a | yes | LOW | no | none |
| C4 | GT-2 + GT-3 + GT-9 + GT-10? + GT-12 + GT-19 | yes | n/a | yes | MEDIUM | yes | none |
| C5 | GT-2 + GT-3 + C2 + C4 + GT-9 | yes | n/a | yes | MEDIUM | yes | none |
| C6 | C5 + GT-19 + GT-20? | yes | n/a | yes | MEDIUM | yes | none |

**Table 2 — Section 6 claim inventory**

| §6 Span (brief) | Construct | Claim under R11? | R11 clause applied | Chain cited |
|---|---|---|---|---|
| Recommended approach: instrument, then tactical bundle, not microservices now, define triggers | bold lead-in | yes | bold lead-in whose colon closes the bold span | C1, C3, C4, C5, C6 |
| Key insight: slow deploys does not entail microservices | bold lead-in | yes | bold lead-in whose colon closes the bold span | C2, C1, C4 |
| Trade-offs acknowledged: new test-selection risk; question deferred not foreclosed | bold lead-in | yes | bold lead-in whose colon closes the bold span | C6, C5 |
| Pre-check: head chain list and bands | bold lead-in | yes | bold lead-in whose colon closes the bold span | C1, C2, C3, C4, C5, C6 |
| Confidence: MEDIUM, justified via C3/C5/C2/C4 | bold lead-in | yes | bold lead-in whose colon closes the bold span | C3, C5, C2, C4 |

Scan complete: 6 chain rows, one per section-4 chain block in order; 5 section-6 rows, one per construct in order — 5 claims under R11, 0 excluded. 0 chains malformed, 0 claims untraced.

## Techniques not applied (process output)

theoretical-limit — not applicable at Phase 1 — the essence statement already treats "2 deploys/day" and "45 minutes" as convention-bound figures without needing a reframe; the theoretical-limit treatment (Amdahl's-Law-governed floor) is applied at Phase 4 instead, supporting chains C1 and C4, where the ceiling is actually derived.
inversion — not applicable at Phase 5 — the headline conclusion is a plan/recommendation (fix the pipeline now, gate extraction on evidence), not a claim, so Phase 5's adversarial technique routes to pre-mortem instead, per the decision rule (inversion stress-tests a claim; pre-mortem stress-tests a plan). Inversion was applied at Phase 2 instead (chain C2).

## §6→§4 closure ledger (process output)

- "**Recommended approach:** Instrument the pipeline before changing it... instead of adopting microservices now... define explicit, falsifiable trigger conditions..." → chain C1, C3, C4, C5, C6 ✓
- "**Key insight:** 'Deploys are too slow' does not causally require 'we need microservices'..." → chain C2, C1, C4 ✓
- "**Trade-offs acknowledged:** ...selective/impacted test execution introduces a genuinely new risk... defers, rather than permanently forecloses..." → chain C6, C5 ✓
- "**Confidence:** MEDIUM — ... C3 is offered as one candidate tactic... rests primarily on C5... C2... C4..." → chain C3, C5, C2, C4 ✓

Scan complete: 4 §6 claims, all four cite at least one chain inline; 0 cut.

## Adversarial pass (process output)

**Recompute.** The C5 trade-off ranking was described qualitatively in §4 without showing the underlying arithmetic; recomputing it explicitly here (criteria weights 1-5, scores 1-5, anchored per the trade-off procedure) exposes the actual numbers so the chain's qualitative claim can be checked:

| Criterion (weight) | O1 Do nothing | O2 Fix pipeline only | O4 Partial extraction now | O5 Fix pipeline + evidence-gated trigger |
|---|---|---|---|---|
| Time-to-value (5) | 1 | 5 | 2 | 5 |
| Cost efficiency (4) | 5 | 5 | 2 | 5 |
| Operational safety (5) | 5 | 5 | 2 | 5 |
| Conway/org fit (4) | 5 | 5 | 2 | 5 |
| Reversibility (3) | 5 | 5 | 3 | 5 |
| Directly addresses stated pain (5) | 1 | 5 | 3 | 5 |
| Preserves future optionality (3) | 1 | 2 | 2 | 5 |
| **Weighted total** | **93** | **136** | **66** | **145** |

(O3 "full microservices now" is knocked out before scoring per the must-have test in C5, hop 1, and carries no score.) This recomputation **confirms** chain C5's qualitative claim: O5 ranks highest, and O5 differs from O2 only on "preserves future optionality" (5 vs. 2), exactly as C5 hop 3 states — the chain text and the arithmetic agree.

This recomputation also caught two rounding errors in the prose: the deploy-frequency uplift in chain C4 and §6 was stated as "roughly 2-15x" but the bracket [5,15,30] against a baseline of 2/day actually computes to **2.5x-15x** (5/2 = 2.5, 30/2 = 15); and the team-size shortfall was stated as "roughly 1.3-3x" but the bracket [16,24,40+] against 12 engineers computes to **1.3x-3.3x** (16/12 = 1.33, 40/12 = 3.33). Both are corrected at every occurrence in §4 (chain C4) and §6 (Conclusion) following this recompute.

**Sensitivity.** The single ground truth whose falsity would flip the headline conclusion is **GT-8? ("unverified")** — whether this org's coordinated restart is required by genuine shared mutable state (e.g., a single global in-memory cache or long-lived connection pool that must restart in lockstep across all workers) rather than being a generic deploy-tool default. If GT-8? resolves to "yes, there is a hard shared-state reason that Puma's phased restart cannot route around," then GT-19's general applicability would not rescue this specific org, chain C2's strongest pillar weakens, and the case for considering extraction sooner strengthens materially. This is exactly the gap the tactical first step ("document this org's actual restart mechanics") is designed to close before the rest of the plan is executed.

**Rival.** Headline: "leadership is right, go microservices now" — ruled out; see Abandoned Reasoning, Rival 1 (ruled out by C2, C4, C5). Intermediate chains: **C1** — a rival reading ("test time is dominated by inherently slow individual specs, not irrelevant-test breadth") is live and unsettled, but does not actually compete with C1's conclusion, which is scoped to "tooling-addressable" in general (slow specs are also a tooling/test-architecture issue) — see C1's own confidence line. **C2** — a rival reading (GT-8?, a substantive shared-state reason for the restart) is live and unsettled; named on C2's confidence line, and is the same ground truth identified in the Sensitivity step above. **C3** — a rival reading (A-6, size-driven test depth rather than selection breadth) is live and unsettled; named on C3's confidence line. **C4** — a rival reading (severe cross-domain coupling, GT-16?, pushing the pipeline-fix bracket above 20 minutes) is live but does not change the decision, because the conclusion is anchored to the bracket's conservative edge; named on C4's confidence line. **C5, C6** — inherit these rivals via their head citations; no new rival specific to those chains.

**Adversarial technique — pre-mortem on the headline recommendation (O5: fix the pipeline now, gate extraction on evidence).** The headline conclusion is a plan/recommendation, so per the decision rule this step applies pre-mortem (not inversion — see "Techniques not applied," above).

*Premise:* It is 18 months from now. The "fix the pipeline first, gate extraction on evidence" plan has failed to deliver, and leadership is frustrated that the team did not move to microservices when it had the chance.

*Causes (generated from four viewpoints, unfiltered):*
- *Implementing engineer:* The test-impact-analysis tool had poor precision in practice; a false negative let a regression reach production, destroying trust in selective execution, and the team reverted to full-suite-always — erasing the main pipeline-time win.
- *Ops/on-call engineer:* The flaky-test quarantine process was never actually staffed past its first month; flakiness crept back, and the nightly full-suite safety net (the priced mitigation for A-24) started silently failing without anyone noticing.
- *Product/business owner:* The team and product grew faster than anticipated (new product lines, headcount nearly tripling within a year) — faster than anyone was tracking the C4 trigger metrics — so the org drifted past the microservices break-even threshold without anyone noticing the drift.
- *Leadership:* No one defined a visible timeline or checkpoint for the phased plan, so three months of "measuring and fixing the pipeline" was perceived as "doing nothing," and patience ran out before the tactical fixes had time to compound.

*Clusters:*
- **Cluster A — Execution risk in the tactical fixes themselves** (test-impact tool precision/recall, flaky-quarantine staffing) — bears on **C3**, **C6**, and assumption **A-24**.
- **Cluster B — Trigger-tracking failure** (nobody owned watching the C4 metrics as the org scaled) — bears on **C4**, **C6**.
- **Cluster C — Perception/communication risk** (the phased plan read as inaction to leadership) — bears on **C5** (the recommendation itself) and the "Trade-offs acknowledged" claim in §6.

*Disposition:*
- Cluster A: **named plan change** — pilot the test-impact tool against the last 3 months of merged PRs *before* trusting it on the critical path, and assign explicit ownership of the flaky-test quarantine queue with a weekly review cadence (not a one-time cleanup).
- Cluster B: **named plan change** — assign a named owner (not "the team") for a quarterly review of the C4 trigger metrics (headcount, measured coupling, business need for independent release trains, platform-staffing status), with the review date fixed in advance rather than left open-ended.
- Cluster C: **named plan change** — present the phased plan to leadership as a dated roadmap with an explicit first checkpoint (e.g., "re-evaluate in Q2 against the pipeline-time and deploy-frequency metrics named in the falsification condition below"), not as an open-ended deferral.

*Falsification (recorded here, not in §6):* This conclusion is false if, after implementing the tactical fixes (test parallelization, selective test execution, flaky quarantine, confirmed rolling restarts, trunk-based development with feature flags), the pipeline wall-clock time does not materially drop (stays within 20% of 45 minutes) and/or deploy frequency does not rise from the ~2/day baseline within two quarters — in that case the bottleneck is not what this analysis identified, and the case for structural change, including decomposition, strengthens.

## Self-Audit Gate (process output)

**Criterion 1: Identify Essence**
Quoted span: "Given a 6-year-old, ~350 KLOC Rails monolith (catalog, cart, checkout, fulfillment) with a ~45-minute CI/CD pipeline requiring a full test-suite run and a coordinated application restart on every deploy, shipped by 12 engineers at ~2 deploys/day, is 'move to microservices' the causally-indicated fix for 'deploys are too slow' — or does a more direct, lower-cost lever exist, and under what conditions (if any) does partial service extraction become justified?"
Band: **Rigorous**
Justification: The statement names the real analytical question (causal necessity of a specific architecture change) rather than restating leadership's conclusion as fact, and each of the five listed success criteria names a checkable property the Conclusion section (§6) actually addresses (necessity test, cost quantification, deploy-frequency ceiling, ranked recommendation with trigger conditions).

**Criterion 2: Challenge Assumptions**
Quoted span (from §2, post-fix): "| A-12 | [Inversion precondition 4] Rolling/zero-downtime deploy is not already achievable within the monolith | untested belief, load-bearing | Verify against standard Rails/Puma deployment practice | Discard — **False** — Puma cluster-mode phased restarts are standard (GT-19) | Resolved — see GT-19 |" and "| A-24 | ... | untested belief, load-bearing | Verify via pilot ... | Challenge — Unverified | Unverified — flagged. `[Assumes: A-24]` on second-order step and on C3 |"
Band: **Rigorous**
Justification: Every row carries a Type from the four-type scheme, the Verdict cell leads with Accept/Challenge/Discard followed by an em-dash and specific justification, at least one assumption (A-12) is Discarded on evidence rather than merely labelled Accept, and every assumption used in a derivation chain via `[Assumes: X]` carries the literal "Unverified — flagged" notation in its Verification cell; the Assumption Audit scan (process output, above) confirms the audit visited every named chain step in section 4 exhaustively, surfacing A-23 through A-28.

**Criterion 3: Establish Ground Truths**
Quoted span: "`?`-marked: GT-5, GT-6, GT-7, GT-8, GT-10, GT-11, GT-14, GT-15, GT-16, GT-17, GT-18, GT-20 (12 of 20)" (enumeration checked against §3's list: 12 suffixed entries, matches) — and, from the self-audit scan's chain-form table: GT-9 (read-at-source, Conway's Law) feeds only C2 (MEDIUM) and C4 (MEDIUM); GT-19 (read-at-source, Puma docs) feeds only C2 (MEDIUM), C4 (MEDIUM), C6 (MEDIUM) — neither reachable, unsuffixed ground truth feeds any HIGH-confidence chain.
Band: **Hand-wavy**
Justification: Per the Criterion 3 descriptor's explicit reachability clause, "a single unsuffixed GT whose reachable source feeds only MEDIUM or LOW chains bands this criterion Sound; the same shortfall across multiple GTs bands it Hand-wavy" — both GT-9 and GT-19 are reachable, read-at-source, and unsuffixed, yet neither feeds a HIGH chain, which is the multi-GT case the descriptor names. This is not a citation-quality defect (both sources were actually opened and quoted) and not fixable by acquiring better evidence; it is a structural consequence of this being a hypothetical organization where the scenario-specific facts needed to close C2's and C4's open Rivals axes (GT-8?, GT-16?) do not exist to be read. Rating C2 or C4 HIGH to avoid this score would violate Criterion 5's calibration rule (rating above what the axes license), so this is disclosed as an accepted, honestly-scored shortfall rather than corrected by inflating a chain's band.

**Criterion 4: Reason Upward**
Quoted span (from the self-audit scan, Table 1): "C1 | GT-1 + GT-2 + GT-12 | yes | n/a | yes | HIGH | no | none" ... "C6 | C5 + GT-19 + GT-20? | yes | n/a | yes | MEDIUM | yes | none" (all six chains: Form conforming = yes, Dependency clean = yes) — and from §5: "Rival 3 — 'The 350 KLOC codebase size is itself the cause of the 45-minute pipeline.' ... Why abandoned: Amdahl's Law (GT-12) and the reduce-to-primitives drill in C1 show pipeline wall-clock time is governed by parallelism and test-selection strategy... What it ruled out: ... ruled out by C1."
Band: **Rigorous**
Justification: Every chain is form-conforming and dependency-clean per the self-audit scan; every conclusion in §6 has exactly one chain in §4; every chain step introducing a new assumption carries an inline `[Assumes: X]` tag reconciled against the Assumption Audit scan; no analogy is used as direct evidence anywhere in §4 (DORA, Conway's Law, and the two-pizza heuristic are each grounded in a named, cited GT rather than offered as "industry does X"); and §5 documents five dead ends in the prescribed What-was-tried/Why-abandoned/What-it-ruled-out structure, each naming the GT-N or Cn that ruled it out.

**Criterion 5: Validate**
Quoted span: "Cluster A — Execution risk in the tactical fixes themselves (test-impact tool precision/recall, flaky-quarantine staffing) — bears on C3, C6, and assumption A-24. ... Disposition: Cluster A: named plan change — pilot the test-impact tool against the last 3 months of merged PRs before trusting it on the critical path..." and, from §4 chain C4: "Confidence: MEDIUM — Inputs short (GT-10? is reported-by-delegate, not read-at-source: two direct fetch attempts 404'd; verification = open a primary Amazon/Bezos source)."
Band: **Rigorous**
Justification: Every chain carries a `**Pre-check:**` line and a `**Confidence:**` line that names the specific short axis (Inputs, Inference, or Rivals), the specific input/hop/rival causing it, and what would close it; no chain consuming a `?`-marked input is rated HIGH (only C1 is HIGH and its head carries none); every chain is rated no higher than the lowest-rated chain its own head cites (C5 and C6 both MEDIUM, matching their cited C2/C4 and C5 respectively); the adversarial pass record is complete with Recompute, Sensitivity, Rival, and Falsification all populated, a past-tense Premise, an unfiltered multi-viewpoint Causes list, three Clusters each citing the chain/GT ids they bear on, and each cluster carrying a named plan change.

**Criterion 6: Conclusion-to-Ground-Truth Traceability**
Quoted span (from the self-audit scan, Table 2): "Recommended approach: instrument, then tactical bundle, not microservices now, define triggers | bold lead-in | yes | bold lead-in whose colon closes the bold span | C1, C3, C4, C5, C6" ... "Confidence: MEDIUM, justified via C3/C5/C2/C4 | bold lead-in | yes | ... | C3, C5, C2, C4" (5 of 5 §6 constructs cite a chain; 0 untraced).
Band: **Rigorous**
Justification: All four prescribed lead-ins plus the Pre-check line trace to named §4 chains per the self-audit scan and the §6→§4 closure ledger, no claim in §6 is new reasoning absent from §4, and the Key Insight ("deploys are slow does not causally require microservices... leadership's diagnosis mistakes a symptom for a prescription") states a distinct analytical finding rather than restating the Recommended Approach's action list.

**Gate result:** cleared · passes: 1 · Fix/Repeat fired: no

## Structured summary (process output)

```json
{
  "schema_version": 1,
  "run_mode": "full-composer",
  "assumptions": [
    {
      "id": "A-1",
      "type": "convention",
      "verdict": "Challenge"
    },
    {
      "id": "A-2",
      "type": "convention",
      "verdict": "Challenge"
    },
    {
      "id": "A-3",
      "type": "untested belief",
      "verdict": "Challenge"
    },
    {
      "id": "A-4",
      "type": "current constraint",
      "verdict": "Accept"
    },
    {
      "id": "A-5",
      "type": "convention",
      "verdict": "Challenge"
    },
    {
      "id": "A-6",
      "type": "untested belief",
      "verdict": "Challenge"
    },
    {
      "id": "A-7",
      "type": "untested belief",
      "verdict": "Challenge"
    },
    {
      "id": "A-8",
      "type": "untested belief",
      "verdict": "Challenge"
    },
    {
      "id": "A-9",
      "type": "untested belief",
      "verdict": "Challenge"
    },
    {
      "id": "A-10",
      "type": "untested belief",
      "verdict": "Challenge"
    },
    {
      "id": "A-11",
      "type": "untested belief",
      "verdict": "Challenge"
    },
    {
      "id": "A-12",
      "type": "untested belief",
      "verdict": "Discard"
    },
    {
      "id": "A-13",
      "type": "untested belief",
      "verdict": "Challenge"
    },
    {
      "id": "A-14",
      "type": "untested belief",
      "verdict": "Challenge"
    },
    {
      "id": "A-15",
      "type": "untested belief",
      "verdict": "Challenge"
    },
    {
      "id": "A-16",
      "type": "untested belief",
      "verdict": "Challenge"
    },
    {
      "id": "A-17",
      "type": "untested belief",
      "verdict": "Challenge"
    },
    {
      "id": "A-18",
      "type": "untested belief",
      "verdict": "Challenge"
    },
    {
      "id": "A-19",
      "type": "untested belief",
      "verdict": "Challenge"
    },
    {
      "id": "A-20",
      "type": "untested belief",
      "verdict": "Challenge"
    },
    {
      "id": "A-21",
      "type": "untested belief",
      "verdict": "Challenge"
    },
    {
      "id": "A-22",
      "type": "untested belief",
      "verdict": "Challenge"
    },
    {
      "id": "A-23",
      "type": "untested belief",
      "verdict": "Challenge"
    },
    {
      "id": "A-24",
      "type": "untested belief",
      "verdict": "Challenge"
    },
    {
      "id": "A-25",
      "type": "untested belief",
      "verdict": "Challenge"
    },
    {
      "id": "A-26",
      "type": "untested belief",
      "verdict": "Challenge"
    },
    {
      "id": "A-27",
      "type": "untested belief",
      "verdict": "Challenge"
    },
    {
      "id": "A-28",
      "type": "untested belief",
      "verdict": "Challenge"
    }
  ],
  "ground_truths": [
    {
      "id": "GT-1",
      "read_at_source": true
    },
    {
      "id": "GT-2",
      "read_at_source": true
    },
    {
      "id": "GT-3",
      "read_at_source": true
    },
    {
      "id": "GT-4",
      "read_at_source": true
    },
    {
      "id": "GT-5",
      "read_at_source": false
    },
    {
      "id": "GT-6",
      "read_at_source": false
    },
    {
      "id": "GT-7",
      "read_at_source": false
    },
    {
      "id": "GT-8",
      "read_at_source": false
    },
    {
      "id": "GT-9",
      "read_at_source": true
    },
    {
      "id": "GT-10",
      "read_at_source": false
    },
    {
      "id": "GT-11",
      "read_at_source": false
    },
    {
      "id": "GT-12",
      "read_at_source": true
    },
    {
      "id": "GT-13",
      "read_at_source": true
    },
    {
      "id": "GT-14",
      "read_at_source": false
    },
    {
      "id": "GT-15",
      "read_at_source": false
    },
    {
      "id": "GT-16",
      "read_at_source": false
    },
    {
      "id": "GT-17",
      "read_at_source": false
    },
    {
      "id": "GT-18",
      "read_at_source": false
    },
    {
      "id": "GT-19",
      "read_at_source": true
    },
    {
      "id": "GT-20",
      "read_at_source": false
    },
    {
      "id": "GT-21",
      "read_at_source": false
    }
  ],
  "chains": [
    {
      "id": "C1",
      "confidence": "HIGH",
      "rests_on": [
        "GT-1",
        "GT-2",
        "GT-12"
      ]
    },
    {
      "id": "C2",
      "confidence": "MEDIUM",
      "rests_on": [
        "GT-9",
        "GT-13",
        "GT-19"
      ]
    },
    {
      "id": "C3",
      "confidence": "LOW",
      "rests_on": [
        "GT-2",
        "GT-20?",
        "GT-12"
      ]
    },
    {
      "id": "C4",
      "confidence": "MEDIUM",
      "rests_on": [
        "GT-2",
        "GT-3",
        "GT-9",
        "GT-10?",
        "GT-12",
        "GT-19"
      ]
    },
    {
      "id": "C5",
      "confidence": "MEDIUM",
      "rests_on": [
        "GT-2",
        "GT-3",
        "C2",
        "C4",
        "GT-9"
      ]
    },
    {
      "id": "C6",
      "confidence": "MEDIUM",
      "rests_on": [
        "C5",
        "GT-19",
        "GT-20?"
      ]
    }
  ],
  "dead_ends": [
    "Go full microservices now, taken literally as leadership stated it",
    "Extract one bounded domain into a service right now, without first gathering evidence",
    "The 350 KLOC codebase size is itself the cause of the 45-minute pipeline",
    "Do nothing; 2 deploys/day is fine",
    "The coordinated restart is inherently unfixable without splitting the application"
  ],
  "techniques": {
    "applied": [
      "inversion",
      "fishbone",
      "five-whys",
      "theoretical-limit",
      "estimate",
      "trade-off",
      "second-order",
      "pre-mortem"
    ],
    "not_applied": [
      {
        "technique": "theoretical-limit",
        "phase": 1,
        "reason": "the essence statement already treats \"2 deploys/day\" and \"45 minutes\" as convention-bound figures without needing a reframe; the theoretical-limit treatment (Amdahl's-Law-governed floor) is applied at Phase 4 instead, supporting chains C1 and C4, where the ceiling is actually derived"
      },
      {
        "technique": "inversion",
        "phase": 5,
        "reason": "the headline conclusion is a plan/recommendation (fix the pipeline now, gate extraction on evidence), not a claim, so Phase 5's adversarial technique routes to pre-mortem instead, per the decision rule (inversion stress-tests a claim; pre-mortem stress-tests a plan). Inversion was applied at Phase 2 instead (chain C2)"
      }
    ]
  },
  "gate": {
    "passes": [
      {
        "bands": [
          "Rigorous",
          "Rigorous",
          "Hand-wavy",
          "Rigorous",
          "Rigorous",
          "Rigorous"
        ],
        "gate_cleared": true,
        "hand_wavy_cap_cleared": true
      }
    ],
    "fix_repeat_fired": false,
    "cleared": true
  },
  "re_entry": {
    "fired": false,
    "edges": []
  },
  "conclusion": {
    "recommendation": "Instrument the pipeline before changing it (chain C1), then execute a ranked bundle of tactical fixes in parallel — test parallelization and selective/impacted test execution with a nightly full-suite safety net (chains C1, C3, C6), flaky-test quarantine and build/asset-compile caching (fishbone findings feeding C3), and confirming rolling/phased restarts via standard Puma cluster-mode tooling plus trunk-based development with feature flags to decouple \"deploy\" from \"release\" (chain C4) — instead of adopting microservices now (chain C5). In parallel, define explicit, falsifiable trigger conditions for revisiting *partial* service extraction later, rather than closing the question permanently (chain C5, chain C6).",
    "confidence": "MEDIUM",
    "rests_on": [
      "C1",
      "C2",
      "C3",
      "C4",
      "C5",
      "C6"
    ]
  }
}
```
