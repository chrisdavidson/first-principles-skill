<!-- GENERATED — DO NOT EDIT. Source: shared/examples/software-systems.md. Regenerate via: scripts/sync-content.py --write. -->

# Worked Example: Software and Systems

A complete first-principles analysis of a software or systems design question, following the
standardized output format and showing at least one abandoned reasoning path. Authored in Phase 5.

**Scenario.** A 6-year-old e-commerce platform — catalog, cart, checkout, and fulfillment in a
single Rails monolith (~350 KLOC) — has a CI/CD pipeline that takes approximately 45 minutes
end-to-end. Every deploy requires a full test suite run and a coordinated application restart,
and the team of 12 engineers ships roughly 2 deploys per day. Engineering leadership has
concluded: "deploys are too slow, we need microservices."

---

## 1. Problem Essence

**Core problem:** What is the actual bottleneck in the deploy cycle for this monolith, and what
is the minimum intervention that removes it — evaluated independently of whether microservices
are the solution?

The triggering statement — "we need microservices" — is a proposed solution, not a problem
statement. First-principles analysis requires stripping the proposed solution away and asking
what problem it is supposed to solve. The symptom is slow deploys; the cause is unknown. This
analysis reframes the question from "should we migrate to microservices?" to "what is actually
preventing faster deploys, and what is the cheapest intervention that removes that constraint?"

**Success criteria:**

- The deploy bottleneck is identified and measured: a specific cause (test suite wall-clock time,
  pipeline step serialization, database schema coupling, or another identified constraint) is named
  with supporting data from pipeline profiling.
- The recommended intervention is the lowest-cost change that demonstrably reduces the bottleneck.
  "Lowest-cost" is measured by time-to-implement, architectural risk, and reversibility, not by
  engineering effort alone.
- After the intervention, deploy frequency increases above the current ~2/day ceiling — the change
  is confirmed to have removed the bottleneck, not just altered the pipeline.
- If architecture is not the primary bottleneck, the recommendation does not require a
  monolith-to-microservices migration.
- If architecture is the primary bottleneck, the analysis identifies which coupling constraint is
  the barrier and recommends the minimum structural change to remove it.

---

## 2. Assumptions Table

| Assumption | Type | Treatment | Verdict | Verification |
|------------|------|-----------|---------|--------------|
| Microservices enable faster deploys | convention | Challenge before use — this is a widely-held claim but depends on team maturity, pipeline design, inter-service dependency topology, and the nature of the coupling; it is not a physical or logical necessity | Challenge — unverified for this team; synchronous dependencies and shared infrastructure can deploy slower than a well-configured monolith | Unverified for this team and codebase — flagged; microservices with synchronous dependencies and shared infrastructure can deploy more slowly than a well-configured monolith |
| The deploy bottleneck is architectural coupling in the monolith | untested belief | Verify before use — the test suite runtime and pipeline structure have not been profiled to determine their contribution; alternative non-architectural causes exist and must be ruled out | Challenge — no pipeline profiling data collected; the runtime is consistent with non-architectural causes too | Unverified — flagged; no pipeline profiling data has been collected; the 45-minute runtime is consistent with both architectural and non-architectural bottleneck causes |
| A 12-person team can operate a microservices estate at acceptable overhead | untested belief | Verify — distributed systems require per-service monitoring, independent CI pipelines, inter-service communication contracts, and distributed tracing; the ops burden scales with service count and is well-documented to exceed small-team capacity below a threshold | Challenge — no evidence the team has run distributed services; DORA data shows headwinds below ~50 engineers / ~10 services | Unverified — flagged; no evidence the team has operated distributed services; DORA research documents that teams below ~50 engineers operating more than ~10 services face significant reliability and velocity headwinds |
| Slow deploys are causing meaningful, ongoing business harm | current constraint | Record expiry conditions — this constraint holds as long as the business requires more than ~2 deploys per day; it expires if product velocity requirements decrease or if the team ships features whose release cadence is compatible with the current ceiling | Accept — measured ~2/day ceiling; business impact is real even without a quantified dollar value | Observed: ~2 deploys/day maximum is the measured ceiling; business impact is real (engineering velocity is blocked; hotfixes require manual bypass procedures) even if the precise dollar value of the constraint is not quantified |
| A full rewrite or big-bang migration is required to change the architecture | untested belief | Discard — the strangler fig pattern enables incremental extraction of services from a monolith while the monolith continues to handle remaining traffic; no big-bang rewrite is required; this assumption frames the decision as binary when it is not | Discard — the strangler fig pattern enables incremental extraction; no big-bang rewrite is required | Contradicted by published incremental migration patterns; the strangler fig approach is the documented industry mechanism for this exact scenario (Newman "Building Microservices", chapter on the strangler fig application) |
| Schema-level coupling is equivalent to application-level deploy coupling — a shared relational schema blocks truly independent releases in the same way a shared application binary does | untested belief | Accept with verification — the inference in Chain 2 ("splitting the application while retaining the shared schema produces a distributed monolith") requires this to hold; the specific coupling mechanism is that any service performing a schema migration must either apply it to the shared schema (affecting all co-tenant services) or coordinate migration timing with all services that read those tables | Accept — a shared schema forces coordinated migration windows; deploy-independence is negated without decomposition | Verified by technical analysis: a shared schema forces coordinated migration windows across all services; the deploy-independence that microservices nominally provide is negated at the data layer if schema ownership is not decomposed first — this is the documented definition of a distributed monolith (Newman "Building Microservices", 2nd ed., Chapter 4) |

---

## 3. Ground Truths

- **GT-1** The full CI/CD pipeline runs end-to-end in approximately 45 minutes — test suite
  execution plus artifact build, deploy/restart and health-check wait; the per-stage split is
  not measured (that is exactly what chain C3's profiling step would read) — source: measured
  pipeline execution time (CI dashboard logs; 30-day average of successful pipeline runs)

- **GT-2** A deploy requires a full pipeline pass — a complete test suite run plus a coordinated
  application restart across all app server instances — before traffic is cut over; no partial-
  pipeline path, blue-green swap, or rolling deploy strategy currently exists in the pipeline
  configuration — source: observed CI pipeline configuration file (deploy stage definition)

- **GT-3** The team ships approximately 2 deploys per day at maximum, measured. What imposes that
  ceiling is not established here — no named ground truth accounts for it. The 45-minute
  pipeline bounds sequential deploys at roughly 10 per working day
  (480 minutes ÷ 45 minutes ≈ 10.7), so the measured 2/day ceiling sits about five times below
  the pipeline's own throughput limit — source: measured deploy frequency from CI/CD
  deployment records (30-day trailing count)

- **GT-4** Operating a microservices estate requires per-service monitoring, independent deployment
  pipelines, inter-service communication contracts (API versioning, schema registries), and
  distributed tracing infrastructure; each additional service multiplies the operational overhead
  the team must maintain — source: architectural fact documented in microservices engineering
  literature (Newman "Building Microservices", 2nd ed.; Sam Newman "Monolith to Microservices";
  DORA State of DevOps annual reports on team cognitive load and deployment frequency)

- **GT-5** The current monolith uses a single shared relational database schema that all
  application modules read from and write to; no service boundary currently has exclusive
  ownership of any schema table — source: observed codebase structure (direct inspection of
  database schema and ORM model relationships)

---

## 4. Derivation Chains

### Conclusion C1: Architecture is not demonstrably the primary bottleneck

GT-1 (45-minute full pipeline runtime) + GT-2 (every deploy requires a full pipeline pass including a complete test suite run) + GT-3 (2 deploys/day measured ceiling, not explained by the 45-minute pipeline alone)
→ The deploy cycle floor is set by the whole-pipeline wall-clock duration, of which the test suite is the largest unmeasured share; the 45-minute pipeline bounds sequential deploys at roughly 10 per working day (480 minutes ÷ 45 minutes ≈ 10.7), well above the observed 2-deploy/day ceiling, so the floor constrains cadence without explaining the observed ceiling — the gap between the two is not accounted for by any named ground truth. A monolith running a fully-parallelized test suite in 8 minutes with a blue-green deploy strategy contributes only 8 minutes of test-suite time to each deploy; the test-suite contribution to per-deploy time is set by pipeline structure, and no architectural change is needed to shorten it; architecture determines whether services can deploy independently, but whether the pipeline structure (sequential execution + full-suite requirement), the monolithic architecture itself, or some other unmeasured factor is what actually binds the observed 2-deploy/day ceiling has not been established
→ Architecture cannot be concluded to be the primary deploy bottleneck until the test suite runtime, pipeline step serialization, and deployment restart time have been profiled and ruled out as the dominant cause. The 45-minute pipeline is a NECESSARY constraint on deploy cadence — no deploy can complete faster than one pipeline run — but it is not a SUFFICIENT explanation of the 2-deploy/day ceiling, since it bounds deploys at roughly five times the observed rate; neither the pipeline runtime nor the architecture has been shown to be the binding constraint, and the unexplained factor — deploy windows, approval gates, release batching policy, or something else entirely — has not been measured.

**Confidence:** HIGH — this chain's conclusion is a negative claim (architecture cannot yet be concluded to be the primary bottleneck), directly supported by GT-1 and GT-2 plus the documented absence of profiling data; the chain's head cites no `GT-N?`, so the D-07 ceiling rule does not reach it. This rating does not rest on the withdrawn sufficient-explanation claim: the corrected hops establish only that the 45-minute pipeline is a necessary but not sufficient constraint on cadence, and the conclusion — that architecture's role is unestablished pending profiling — holds independently of that withdrawn claim.

---

### Conclusion C2: The shared database coupling problem is separable from a microservices migration

GT-5 (single shared relational database schema with no service-boundary ownership) + GT-4 (microservices require per-service independent deployment pipelines and inter-service contracts)
→ Splitting the application layer into separate services while retaining the shared schema produces a distributed monolith: services that deploy independently in theory but cannot actually execute schema migrations or release independently because all services share the same database state; true independent deploys require that each service owns its schema boundaries exclusively; this means schema decomposition is a prerequisite of, not a consequence of, a microservices migration
→ Schema decomposition can be executed incrementally on the monolith — by establishing bounded contexts, identifying which modules own which tables, and progressively enforcing that only the owning module accesses those tables — without splitting the application into separately-deployed services. The coupling reduction that enables independent deploys is separable from the service-boundary split. The two problems can be addressed in sequence rather than as a single large migration.

**Confidence:** HIGH

---

### Conclusion C3: The minimum viable intervention is to profile the bottleneck and apply the lowest-cost fix

GT-1 (45-minute pipeline, per-stage split unmeasured) + GT-3 (2 deploys/day ceiling, not explained by the 45-minute pipeline alone) + GT-4 (microservices estate multiplies per-service ops overhead that a 12-engineer team must absorb)
→ The cost-risk profile of available interventions varies by orders of magnitude; the pipeline has four measurable stages: test suite execution, artifact build, deployment and restart, and health-check wait; profiling these stages, together with the gap between one pipeline completion and the next deploy start (readable from the same CI/CD deployment records GT-3 is measured from, and where the approval gates, deploy windows or release batching that GT-3 leaves unexplained would show up), is a configuration-level instrumentation taking approximately 1 day that identifies which stage or gap is the dominant cost without requiring any code change; pipeline parallelization (splitting the test suite across concurrent CI workers) is a configuration-level change achievable in days to 2 weeks with no architectural risk and is fully reversible; schema decomposition along bounded-context lines is weeks-to-months of careful migration work with moderate risk and is largely reversible; a full monolith-to-microservices migration is months-to-years of architectural work with high risk and is not easily reversible, and it introduces the full GT-4 operational overhead before delivering any deploy-speed benefit; committing to the highest-cost option before ruling out lower-cost options is not consistent with minimum viable intervention principles
→ The rational sequencing is: profile the deploy cycle to identify the specific bottleneck, apply the lowest-cost intervention that removes it (parallelization first if profiling identifies a pipeline stage as binding; a release-process change first if the binding factor is an approval gate, deploy window or batching policy), and revisit microservices only after profiling demonstrates that the bottleneck is architectural and schema decoupling alone is insufficient.

**Confidence:** HIGH

---

## 5. Abandoned Reasoning

### Dead End: Split the monolith as specified

**What was tried:** Accept "microservices enable faster deploys" as an established fact and
reason from it directly to a migration recommendation. The attempted chain was:

```text
Current deploys take 45 minutes, limiting releases to ~2/day.
Microservices enable each service to deploy independently.
Independent deploys are faster than full-monolith deploys.
Therefore: migrate to microservices → deploys become faster.
```

This path had initial appeal because each step sounds individually plausible, and the
general premise that "small services deploy faster than large monoliths" is a common
engineering belief. The analysis spent time working through what such a migration would
require: identifying service boundaries, extracting the first service from the monolith,
establishing a separate CI pipeline for it, and measuring whether its independent deploys
were faster.

**Why abandoned:** The anchor premise — "microservices enable faster deploys" — is an untested
belief for this team and codebase, not a verified fact. Phase 2 classification assigns it
Verdict: Challenge, meaning it cannot anchor a derivation chain without being verified first.
Probing the premise reveals why it fails here:

1. The 45-minute pipeline is driven principally by test execution — its largest but unmeasured
   stage (GT-1) — and by the full-pipeline-per-
   deploy requirement (GT-2). Neither of these is caused by the monolithic architecture. A
   monolith with a parallelized 8-minute test suite and a blue-green deploy strategy deploys
   faster than many microservices systems. Architecture has not been shown to be the cause of
   the current ceiling — and neither has the pipeline: at 45 minutes it bounds sequential
   deploys at roughly 10 per working day, five times the observed 2/day rate, so what binds
   the observed ceiling is not established by any named ground truth.

2. Even after splitting the application layer into services, the shared database schema (GT-5)
   means each service cannot execute schema migrations independently — they all share the same
   schema. Deploying the application services independently while the database remains shared
   creates a distributed monolith: the services look independent but are coordinated at the data
   layer. This does not remove the coordination requirement; it moves it from the application
   layer to the data layer, where it is harder to observe and manage.

3. The GT-4 operational overhead of running a microservices estate is real and front-loaded.
   The team pays the full ops cost (per-service monitoring, distributed tracing, independent
   CI pipelines, inter-service contracts) before gaining any deploy-speed benefit. For a 12-
   engineer team, this overhead can consume enough velocity that deploy frequency decreases in
   the months after migration while the team is still standing up the infrastructure.

The chain collapses at step 1: the premise does not survive Phase 2 scrutiny, and GT-1 and GT-2
establish a pipeline-level constraint the migration premise never addresses, so the premise is
unsupported on its own terms and no architectural claim is needed to reject it.

**What it ruled out:** This dead end establishes that "microservices enable faster deploys" may
not be used as a ground truth for this analysis without empirical evidence specific to this team
and pipeline. Any future argument for a microservices migration must start from a verified claim
that architecture is the bottleneck — not from the general belief that microservices are faster.
It also rules out any migration plan that does not address the shared schema before or alongside
the application split, because a split-application-only migration produces a distributed monolith,
not independent services.

---

### Dead End: Move the test suite to a faster test runner

**What was tried:** Reduce the 45-minute pipeline runtime — whose largest but unmeasured stage is
test execution (GT-1) — by switching to a faster test runner
or test execution framework. The motivation was GT-1 (45-minute runtime) combined with the
observation that test runner performance varies significantly across frameworks, and some runners
can execute the same test suite in a fraction of the time of others. This path was lower-cost
than architectural changes and seemed to directly address the measured 45-minute runtime (GT-1).

**Research conducted on this path:** The test runner substitution approach was evaluated by
examining what fraction of the 45-minute pipeline runtime (GT-1) is attributable to runner
overhead versus test
count. For a 6-year-old, 350 KLOC codebase, accumulated test suites typically contain thousands
of individual test cases. Runner framework overhead (the time to load the runner, discover tests,
and report results) is typically 5–10% of total runtime for large suites — the dominant cost is
test execution time, not runner overhead. Switching from a slower runner to a faster one reduces
the overhead component by at most that 5–10% — removing all of the runner overhead cannot reduce
total runtime by more than the overhead itself accounts for. A faster runner could in principle
also shorten test execution (in-process parallelism, cheaper fixtures), but nothing here measures
that, so 5–10% is the only bound this analysis can defend. For the
45-minute pipeline, an 8% improvement yields approximately 41.4 minutes (45 × 0.92 = 41.4). No
pipeline-time threshold for raising deploy frequency is established here: at 45 minutes the
pipeline already admits roughly five times the observed 2/day rate (GT-3), so a shorter runtime
raises deploy frequency only if profiling shows runtime is what binds.

**Why abandoned:** Runner substitution alone does not address the structural constraint in GT-2:
every deploy requires a full pipeline pass. Even reducing the test suite to 30 minutes does not
change the constraint that the full suite must run before every deploy. The larger lever on
pipeline time is not the test runner — it is the pipeline architecture:

- **Test suite parallelization** (running test shards concurrently across multiple CI workers)
  addresses GT-1's dominant stage directly: if test execution is essentially all of the 45
  minutes — the per-stage split GT-1 leaves unmeasured and profiling would read — splitting it
  across 8 parallel workers brings that stage to approximately 6–8 minutes of wall-clock time,
  without changing any test or application code.
  This is a configuration change in the CI system, not a framework substitution.

- **Blue-green or rolling deployment** addresses GT-2 directly: by pre-building a new application
  version alongside the live version and cutting traffic over atomically, the "coordinated
  restart" requirement is removed. Deploys no longer require coordinated downtime and can be
  triggered immediately after the test suite passes.

Runner substitution addresses neither constraint. It trims pipeline time by the 5–10% estimated
above while leaving the pipeline's structure — sequential and full-suite-required — completely
intact.

**What it ruled out:** This dead end establishes that "replace the test runner" is not a viable
standalone solution and is not worth investing time in before profiling identifies pipeline
parallelization as the binding fix. If profiling shows test-suite time is what binds, the
stronger intervention is parallelization, which cuts test-suite time 5.6–7.5× (from the 45
minutes GT-1 measures for the whole pipeline, if test execution dominates it, to
6–8 minutes) versus runner substitution's 5–10% (from 45 minutes to ~40.5–42.75 minutes). Runner-level optimization may be worthwhile
as a follow-on after parallelization, but it is not the primary intervention.

---

## Assumption Audit (pre-scoring; completed before §6)

This audit was completed before scoring. It covers every derivation chain in section 4: the
bottleneck-diagnosis chain, the shared-database separability chain, and the minimum
viable intervention chain. Each chain step is visited in order; any assumption required to hold
that was not already in the Assumptions Table has been added there before this table was finalised.

| Chain | Step | Step Text (brief) | Assumption surfaced? | Added to Table? |
|-------|------|-------------------|----------------------|-----------------|
| Bottleneck | 1 | GT-1 + GT-2 + GT-3 → whole-pipeline wall-clock sets the deploy-cycle floor (~10 deploys per working day at 45 min); the observed 2/day ceiling is not explained by that floor | the cause of the gap between the ~10/day pipeline bound and the observed 2/day ceiling is unnamed — surfaced here as an open measurement gap, not resolvable from the named GTs | not added — carried as an open measurement gap in chain C1's second hop, not a classified assumption |
| Bottleneck | 2 | → Architecture cannot be concluded as primary bottleneck until pipeline stages are profiled | none — this is a logical negation step: without profiling data, the architectural claim is unestablished; no additional bridging fact required | n/a |
| DB coupling | 1 | GT-5 + GT-4 → retaining shared schema after app split produces a distributed monolith; schema decomposition is a prerequisite of migration | Schema-level coupling blocks truly independent releases in the same way application-level coupling does | already present (added above in this audit) |
| DB coupling | 2 | → Schema decomposition is executable incrementally on the monolith without splitting into separate services | none — this step follows from the separability claim in Step 1 and the existing Discard verdict on the big-bang assumption | n/a |
| Min viable | 1 | GT-1 + GT-3 + GT-4 → cost-risk of interventions varies by orders of magnitude; four measurable pipeline stages plus the completion-to-next-deploy gap; profiling takes ~1 day | none — the ~1-day profiling estimate is a practical engineering judgement consistent with GT-2 (pipeline configuration is observable) and with GT-3's source (deployment records timestamp every deploy); no separate factual claim is required | n/a |
| Min viable | 2 | → Rational sequencing: profile first, apply lowest-cost fix, revisit microservices only if bottleneck is architectural | none — this sequencing follows directly from the cost-risk ordering established in Step 1; no additional assumption beyond the prior chains | n/a |

---

## 6. Conclusion

**Recommended approach:** (chains C1 and C3) Profile first, then take whichever of the following
branches profiling indicates, stopping when deploy frequency reaches the target:

1. **Profile the pipeline and the release process** (chain C3; approximately 1 day): instrument the CI/CD
   pipeline to measure the wall-clock contribution of each stage — test suite execution, artifact
   build, deployment and restart, health-check wait — and read, from the deployment records GT-3 is
   measured from, the gap between one pipeline completion and the next deploy start, where an approval
   gate, deploy window or batching policy would show. Identify which stage or gap binds the 2/day
   ceiling. Within the pipeline, the test suite runtime (GT-1) is usually the dominant stage for a
   codebase of this profile; profiling confirms or refutes this. If the binding factor lies outside the
   pipeline, change that release process first — it is cheaper than either step below.

2. **If profiling identifies a pipeline stage as binding, parallelize the test suite and decouple the restart** (chain C3; days to 2 weeks): split the test suite into shards and run them
   concurrently across multiple CI workers; introduce a blue-green or rolling deploy strategy
   to eliminate the coordinated-restart requirement from GT-2. These are CI configuration
   changes with no changes to application code and no architectural risk. After this step,
   measure deploy frequency. If the target is met, stop.

3. **If profiling identifies schema coupling as a bottleneck** (chain C2): begin incremental schema
   decomposition along bounded-context lines, guided by the module boundaries already present in
   the monolith. This is weeks-to-months of careful migration work (establishing exclusive table
   ownership per module, eliminating cross-module schema access, introducing service-level schema
   boundaries). This step delivers the coupling reduction that enables genuinely independent
   deploys — and it does not require splitting the application into separately-deployed services.

Revisit the microservices question as a separate analysis after whichever of steps 1–3 fired have completed. If,
after removing whatever constraint profiling identified as binding and decoupling the schema, the team's deploy frequency
still does not meet business needs — or if the team's real goal is independent team ownership
and feature velocity rather than deploy speed — that is a different problem and warrants a
fresh first-principles analysis with the real goal stated in the Essence Statement (Section 1,
Problem Essence).

**Key insight:** (chains C1, C2 and C3) "Deploys are too slow" is a symptom with multiple independent possible causes
— test suite runtime, pipeline step serialization, deployment restart overhead, and database
schema coupling are each candidate causes that profiling would discriminate between, and they
require different interventions. None of them has been shown sufficient: the 45-minute pipeline
alone bounds deploys at roughly 10 per working day, five times the observed 2/day ceiling, so
the binding constraint is still unmeasured. Architecture migration is the highest-cost,
highest-risk, and least reversible intervention in the solution space. Selecting it as the first response to a symptom that has
not been diagnosed is not reasoning from first principles — it is reasoning from convention
(the convention that "microservices solve deploy problems"). What the analysis does show is the order
of the work: about a day of profiling identifies what binds the ceiling; if it is a pipeline stage
or a release process, configuration or policy changes that take days to weeks address it, whereas an
architectural migration takes months to years and introduces the full GT-4 operational overhead
before the team sees any benefit, whichever constraint turns out to bind.

**Trade-offs acknowledged:**

- (chain C3) Pipeline parallelization and blue-green deploys shorten each deploy and remove the
  coordinated restart — they raise deploy frequency only if profiling identifies a pipeline stage as binding —
  but do not address the longer-term question of whether the monolith's architecture limits feature
  velocity, team autonomy, or scalability under load. Those are different problems. If they are
  real problems for this team, they warrant a separate analysis with those specific goals stated
  in the Essence Statement.

- (chain C2) Schema decomposition is a real cost even when done incrementally. It requires identifying and
  enforcing module-level table ownership across a 6-year-old codebase where cross-module schema
  access is likely widespread. This is careful, high-attention work that carries risk of
  introducing data-consistency regressions if not executed with discipline. The recommendation
  is to pursue it only after profiling confirms it is the bottleneck, not preemptively.

- (chains C1 and C3) The recommendation defers the microservices decision explicitly. Engineering leadership's
  stated position is "we need microservices." This analysis does not validate that position —
  it identifies it as an untested belief and recommends against acting on it before the actual
  bottleneck is measured. If there is organizational pressure to begin a migration regardless
  of the analysis, that pressure should be surfaced as a constraint and addressed separately.

**Confidence:** HIGH
