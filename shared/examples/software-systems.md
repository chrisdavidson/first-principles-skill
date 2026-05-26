# Worked Example: Software and Systems

A complete first-principles analysis of a software or systems design question, following the
standardized output format and showing at least one abandoned reasoning path. Authored in Phase 5.

**Scenario.** A 6-year-old e-commerce platform — catalog, cart, checkout, and fulfillment in a
single Rails monolith (~350 KLOC) — has a CI/CD pipeline that takes approximately 45 minutes
end-to-end. Every deploy requires a full test suite run and a coordinated application restart,
limiting the team of 12 engineers to roughly 2 deploys per day. Engineering leadership has
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
| Microservices enable faster deploys | convention | Challenge before use — this is a widely-held claim but depends on team maturity, pipeline design, inter-service dependency topology, and the nature of the coupling; it is not a physical or logical necessity | Challenge | Unverified for this team and codebase — flagged; microservices with synchronous dependencies and shared infrastructure can deploy more slowly than a well-configured monolith |
| The deploy bottleneck is architectural coupling in the monolith | untested belief | Verify before use — the test suite runtime and pipeline structure have not been profiled to determine their contribution; alternative non-architectural causes exist and must be ruled out | Challenge | Unverified — flagged; no pipeline profiling data has been collected; the 45-minute runtime is consistent with both architectural and non-architectural bottleneck causes |
| A 12-person team can operate a microservices estate at acceptable overhead | untested belief | Verify — distributed systems require per-service monitoring, independent CI pipelines, inter-service communication contracts, and distributed tracing; the ops burden scales with service count and is well-documented to exceed small-team capacity below a threshold | Challenge | Unverified — flagged; no evidence the team has operated distributed services; DORA research documents that teams below ~50 engineers operating more than ~10 services face significant reliability and velocity headwinds |
| Slow deploys are causing meaningful, ongoing business harm | current constraint | Record expiry conditions — this constraint holds as long as the business requires more than ~2 deploys per day; it expires if product velocity requirements decrease or if the team ships features whose release cadence is compatible with the current ceiling | Accept | Observed: ~2 deploys/day maximum is the measured ceiling; business impact is real (engineering velocity is blocked; hotfixes require manual bypass procedures) even if the precise dollar value of the constraint is not quantified |
| A full rewrite or big-bang migration is required to change the architecture | untested belief | Discard — the strangler fig pattern enables incremental extraction of services from a monolith while the monolith continues to handle remaining traffic; no big-bang rewrite is required; this assumption frames the decision as binary when it is not | Discard | Contradicted by published incremental migration patterns; the strangler fig approach is the documented industry mechanism for this exact scenario (Newman "Building Microservices", chapter on the strangler fig application) |
| Schema-level coupling is equivalent to application-level deploy coupling — a shared relational schema blocks truly independent releases in the same way a shared application binary does | untested belief | Accept with verification — the inference in Chain 2 ("splitting the application while retaining the shared schema produces a distributed monolith") requires this to hold; the specific coupling mechanism is that any service performing a schema migration must either apply it to the shared schema (affecting all co-tenant services) or coordinate migration timing with all services that read those tables | Accept | Verified by technical analysis: a shared schema forces coordinated migration windows across all services; the deploy-independence that microservices nominally provide is negated at the data layer if schema ownership is not decomposed first — this is the documented definition of a distributed monolith (Newman "Building Microservices", 2nd ed., Chapter 4) |

---

## 3. Ground Truths

- **GT-1** The full test suite runs end-to-end in approximately 45 minutes on the current CI/CD
  pipeline — source: measured pipeline execution time (CI dashboard logs; 30-day average of
  successful pipeline runs)

- **GT-2** A deploy requires a full pipeline pass — a complete test suite run plus a coordinated
  application restart across all app server instances — before traffic is cut over; no partial-
  pipeline path, blue-green swap, or rolling deploy strategy currently exists in the pipeline
  configuration — source: observed CI pipeline configuration file (deploy stage definition)

- **GT-3** The team ships approximately 2 deploys per day at maximum under the current pipeline
  constraint; higher frequency is mechanically blocked by the 45-minute pipeline assuming
  sequential execution — source: measured deploy frequency from CI/CD deployment records
  (30-day trailing count)

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

### Conclusion: Architecture is not demonstrably the primary bottleneck

GT-1 (45-minute full test suite runtime) + GT-2 (every deploy requires a full pipeline pass
including a complete test suite run) + GT-3 (2 deploys/day measured ceiling imposed by the
sequential pipeline)
→ The deploy cycle floor is set by the test suite wall-clock duration, and the 2-deploy/day
  ceiling follows directly from that floor combined with the full-pipeline-per-deploy
  requirement. A monolith running a fully-parallelized test suite in 8 minutes with a
  blue-green deploy strategy requires only 8 minutes per deploy — no architectural change is
  needed to remove the deploy-frequency bottleneck. Architecture determines whether services
  can deploy independently, but the pipeline structure (sequential execution + full-suite
  requirement), not the monolithic architecture itself, is the sufficient cause of the
  measured 2-deploy/day ceiling.
→ Architecture cannot be concluded to be the primary deploy bottleneck until the test suite
  runtime, pipeline step serialization, and deployment restart time have been profiled and
  ruled out as the dominant cause. The 45-minute pipeline is a sufficient explanation of the
  2-deploy/day ceiling without any architectural coupling claim.

**Confidence:** HIGH

---

### Conclusion: The shared database coupling problem is separable from a microservices migration

GT-5 (single shared relational database schema with no service-boundary ownership) + GT-4
(microservices require per-service independent deployment pipelines and inter-service contracts)
→ Splitting the application layer into separate services while retaining the shared schema
  produces a distributed monolith: services that deploy independently in theory but cannot
  actually execute schema migrations or release independently because all services share the
  same database state. True independent deploys require that each service owns its schema
  boundaries exclusively. This means schema decomposition is a prerequisite of, not a
  consequence of, a microservices migration.
→ Schema decomposition can be executed incrementally on the monolith — by establishing bounded
  contexts, identifying which modules own which tables, and progressively enforcing that only
  the owning module accesses those tables — without splitting the application into separately-
  deployed services. The coupling reduction that enables independent deploys is separable from
  the service-boundary split. The two problems can be addressed in sequence rather than as a
  single large migration.

**Confidence:** HIGH

---

### Conclusion: The minimum viable intervention is to profile the bottleneck and apply the lowest-cost fix

GT-1 (45-minute test suite) + GT-3 (2 deploys/day ceiling imposed by the sequential pipeline)
+ GT-4 (microservices estate multiplies per-service ops overhead that a 12-engineer team must absorb)
→ The cost-risk profile of available interventions varies by orders of magnitude. The pipeline
  has four measurable stages: test suite execution, artifact build, deployment and restart, and
  health-check wait. Profiling these stages (a configuration-level instrumentation taking
  approximately 1 day) identifies which stage is the dominant cost without requiring any code
  change. Pipeline parallelization (splitting the test suite across concurrent CI workers) is
  a configuration-level change achievable in days to 2 weeks with no architectural risk and
  is fully reversible; schema decomposition along bounded-context lines is weeks-to-months of
  careful migration work with moderate risk and is largely reversible; a full
  monolith-to-microservices migration is months-to-years of architectural work with high risk
  and is not easily reversible, and it introduces the full GT-4 operational overhead before
  delivering any deploy-speed benefit. Committing to the highest-cost option before ruling out
  lower-cost options is not consistent with minimum viable intervention principles.
→ The rational sequencing is: profile the pipeline to identify the specific bottleneck, apply
  the lowest-cost intervention that removes it (almost certainly parallelization first), and
  revisit microservices only after profiling demonstrates that the bottleneck is architectural
  and schema decoupling alone is insufficient.

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

1. The 45-minute pipeline is driven by the test suite runtime (GT-1) and the full-pipeline-per-
   deploy requirement (GT-2). Neither of these is caused by the monolithic architecture. A
   monolith with a parallelized 8-minute test suite and a blue-green deploy strategy deploys
   faster than many microservices systems. Architecture is not the cause of the current ceiling.

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

The chain collapses at step 1: the premise does not survive Phase 2 scrutiny, and GT-1 + GT-2
together provide a fully sufficient explanation of the current bottleneck that does not require
any architectural claim.

**What it ruled out:** This dead end establishes that "microservices enable faster deploys" may
not be used as a ground truth for this analysis without empirical evidence specific to this team
and pipeline. Any future argument for a microservices migration must start from a verified claim
that architecture is the bottleneck — not from the general belief that microservices are faster.
It also rules out any migration plan that does not address the shared schema before or alongside
the application split, because a split-application-only migration produces a distributed monolith,
not independent services.

---

### Dead End: Move the test suite to a faster test runner

**What was tried:** Reduce the 45-minute test suite runtime by switching to a faster test runner
or test execution framework. The motivation was GT-1 (45-minute runtime) combined with the
observation that test runner performance varies significantly across frameworks, and some runners
can execute the same test suite in a fraction of the time of others. This path was lower-cost
than architectural changes and seemed to directly address the measured bottleneck.

**Research conducted on this path:** The test runner substitution approach was evaluated by
examining what fraction of the 45-minute runtime is attributable to runner overhead versus test
count. For a 6-year-old, 350 KLOC codebase, accumulated test suites typically contain thousands
of individual test cases. Runner framework overhead (the time to load the runner, discover tests,
and report results) is typically 5–10% of total runtime for large suites — the dominant cost is
test execution time, not runner overhead. Switching from a slower runner to a faster one might
reduce total runtime by 10–30% depending on the specific frameworks compared. For a 45-minute
suite, a 25% improvement yields approximately 34 minutes — still well above the threshold needed
to increase deploy frequency meaningfully.

**Why abandoned:** Runner substitution alone does not address the structural constraint in GT-2:
every deploy requires a full pipeline pass. Even reducing the test suite to 30 minutes does not
change the constraint that the full suite must run before every deploy. The correct lever is not
the test runner — it is the pipeline architecture:

- **Test suite parallelization** (running test shards concurrently across multiple CI workers)
  addresses GT-1 directly: a 45-minute suite split across 8 parallel workers runs in
  approximately 6–8 minutes of wall-clock time, without changing any test or application code.
  This is a configuration change in the CI system, not a framework substitution.

- **Blue-green or rolling deployment** addresses GT-2 directly: by pre-building a new application
  version alongside the live version and cutting traffic over atomically, the "coordinated
  restart" requirement is removed. Deploys no longer require coordinated downtime and can be
  triggered immediately after the test suite passes.

Runner substitution addresses neither constraint. It reduces the bottleneck by a single-digit
percentage while leaving the core problem — a sequential, full-suite-required pipeline —
completely intact.

**What it ruled out:** This dead end establishes that "replace the test runner" is not a viable
standalone solution and is not worth investing time in before CI parallelization has been
implemented. The correct intervention is parallelization, which delivers an order-of-magnitude
improvement (from 45 minutes to 6–8 minutes) versus the marginal improvement from runner
substitution (from 45 minutes to ~30–35 minutes). Runner-level optimization may be worthwhile
as a follow-on after parallelization, but it is not the primary intervention.

---

## Assumption Audit

This audit was completed before scoring. It covers every derivation chain in section 4: the
pipeline-bottleneck diagnosis chain, the shared-database separability chain, and the minimum
viable intervention chain. Each chain step is visited in order; any assumption required to hold
that was not already in the Assumptions Table has been added there before this table was finalised.

| Chain | Step | Step Text (brief) | Assumption surfaced? | Added to Table? |
|-------|------|-------------------|----------------------|-----------------|
| Bottleneck | 1 | GT-1 + GT-2 + GT-3 → test-suite wall-clock sets the deploy-cycle floor; 2-deploy/day ceiling follows from sequential pipeline | none — step consumes only named, already-classified GTs and the logical consequence is definitional | n/a |
| Bottleneck | 2 | → Architecture cannot be concluded as primary bottleneck until pipeline stages are profiled | none — this is a logical negation step: without profiling data, the architectural claim is unestablished; no additional bridging fact required | n/a |
| DB coupling | 1 | GT-5 + GT-4 → retaining shared schema after app split produces a distributed monolith; schema decomposition is a prerequisite of migration | Schema-level coupling blocks truly independent releases in the same way application-level coupling does | already present (added above in this audit) |
| DB coupling | 2 | → Schema decomposition is executable incrementally on the monolith without splitting into separate services | none — this step follows from the separability claim in Step 1 and the existing Discard verdict on the big-bang assumption | n/a |
| Min viable | 1 | GT-1 + GT-3 + GT-4 → cost-risk of interventions varies by orders of magnitude; four measurable pipeline stages; profiling takes ~1 day | none — the ~1-day profiling estimate is a practical engineering judgement consistent with GT-2 (pipeline configuration is observable); no separate factual claim is required | n/a |
| Min viable | 2 | → Rational sequencing: profile first, apply lowest-cost fix, revisit microservices only if bottleneck is architectural | none — this sequencing follows directly from the cost-risk ordering established in Step 1; no additional assumption beyond the prior chains | n/a |

---

## 6. Conclusion

**Recommended approach:** Execute a three-step intervention in order, stopping when deploy
frequency reaches the target:

1. **Profile the pipeline** (approximately 1 day, as established in the minimum-viable-intervention
   chain): instrument the CI/CD pipeline to measure the wall-clock contribution of each stage —
   test suite execution, artifact build, deployment and restart, health-check wait. Identify the
   dominant bottleneck. In most cases for a codebase of this profile, the test suite runtime
   (GT-1) is the dominant cost; profiling confirms or refutes this.

2. **Parallelize the test suite and decouple the restart** (days to 2 weeks, as established in
   the minimum-viable-intervention chain): split the test suite into shards and run them
   concurrently across multiple CI workers; introduce a blue-green or rolling deploy strategy
   to eliminate the coordinated-restart requirement from GT-2. These are CI configuration
   changes with no changes to application code and no architectural risk. After this step,
   measure deploy frequency. If the target is met, stop.

3. **If profiling identifies schema coupling as a bottleneck**: begin incremental schema
   decomposition along bounded-context lines, guided by the module boundaries already present in
   the monolith. This is weeks-to-months of careful migration work (establishing exclusive table
   ownership per module, eliminating cross-module schema access, introducing service-level schema
   boundaries). This step delivers the coupling reduction that enables genuinely independent
   deploys — and it does not require splitting the application into separately-deployed services.

Revisit the microservices question as a separate analysis after steps 1–3 are complete. If,
after removing the pipeline bottleneck and decoupling the schema, the team's deploy frequency
still does not meet business needs — or if the team's real goal is independent team ownership
and feature velocity rather than deploy speed — that is a different problem and warrants a
fresh first-principles analysis with the real goal stated in the Essence Statement (Section 1,
Problem Essence).

**Key insight:** "Deploys are too slow" is a symptom with multiple independent possible causes
— test suite runtime, pipeline step serialization, deployment restart overhead, and database
schema coupling are each sufficient to explain the current ceiling, and they require different
interventions. Architecture migration is the highest-cost, highest-risk, and least reversible
intervention in the solution space. Selecting it as the first response to a symptom that has
not been diagnosed is not reasoning from first principles — it is reasoning from convention
(the convention that "microservices solve deploy problems"). The analysis shows that the same
deploy-frequency improvement the team is seeking is achievable through pipeline configuration
changes that take days to weeks, not an architectural migration that takes months to years and
introduces the full GT-4 operational overhead before the team sees any benefit.

**Trade-offs acknowledged:**

- Pipeline parallelization and blue-green deploys address the deploy-frequency bottleneck but
  do not address the longer-term question of whether the monolith's architecture limits feature
  velocity, team autonomy, or scalability under load. Those are different problems. If they are
  real problems for this team, they warrant a separate analysis with those specific goals stated
  in the Essence Statement.

- Schema decomposition is a real cost even when done incrementally. It requires identifying and
  enforcing module-level table ownership across a 6-year-old codebase where cross-module schema
  access is likely widespread. This is careful, high-attention work that carries risk of
  introducing data-consistency regressions if not executed with discipline. The recommendation
  is to pursue it only after profiling confirms it is the bottleneck, not preemptively.

- The recommendation defers the microservices decision explicitly. Engineering leadership's
  stated position is "we need microservices." This analysis does not validate that position —
  it identifies it as an untested belief and recommends against acting on it before the actual
  bottleneck is measured. If there is organizational pressure to begin a migration regardless
  of the analysis, that pressure should be surfaced as a constraint and addressed separately.

**Confidence:** HIGH
