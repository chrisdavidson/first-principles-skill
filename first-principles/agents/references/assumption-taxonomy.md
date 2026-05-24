# Assumption Taxonomy (v3.2 Subtype Refinement)

> **Scope:** This is a Layer-3 reference that refines the four-type assumption-classification
> scheme defined in `output-template.md` and scored by `validation-rubric.md` (Criterion 2).
> The four top-level types — `physical law`, `current constraint`, `convention`,
> `untested belief` — are preserved verbatim. This file adds **within-type subtypes**, each
> with a prescribed treatment that refines (does not replace) the parent type's treatment.
> Subtypes are grounded exclusively in evidence from the six shipped worked examples under
> `first-principles/agents/references/examples/`.
>
> Come here when classifying a non-trivial assumption and the parent-type treatment feels too
> coarse to prescribe a specific next action. Stay in `output-template.md` if the parent
> treatment is already sufficient; this file is a refinement layer, not a replacement.

---

## How to Apply This Taxonomy

The four top-level types (`physical law`, `current constraint`, `convention`,
`untested belief`) are the canonical scheme. Every assumption in a Classified Assumptions
Table **must** carry one of these four top-level types — this is unchanged from v1.0 and is
the property `validation-rubric.md` Criterion 2 enforces.

This file adds optional within-type **subtypes** that refine the parent type's prescribed
treatment with a more specific verification or challenge procedure.

**Naming pattern (locked):** `<parent> — <discriminator>` using an em-dash with a single
space on each side. Examples: `convention — analogy-as-evidence`,
`untested belief — economic-hinge`. Analysts may coin new subtypes that follow this pattern
when shipped-example evidence later warrants them; consistency comes from the pattern, not
from a fixed enumeration.

**Subtype force:** Subtype use is **recommended-but-not-required**. The most specific
applicable subtype should be used for non-trivial assumptions; falling back to the parent
type alone remains a valid classification when no subtype clearly applies. Shipped worked
examples authored before v3.2 use parent types only and remain valid without modification.

**Reserved tokens:** The four top-level type names (`physical law`, `current constraint`,
`convention`, `untested belief`) are reserved. A subtype name always begins with one of
those four tokens followed by ` — ` and the discriminator.

---

## Subtype Catalog

Each subtype below lists: a one-line definition, the **refined treatment** (what to do
beyond the parent type's prescribed treatment), and an inline `Cited evidence:` line
naming the shipped worked-example rows that warrant the subtype's inclusion.

### Subtypes under `convention`

Parent-type treatment (from `output-template.md`): *Explicitly challenge before use. Ask
whether the convention holds in this context or merely carries inherited inertia.*

#### `convention — context-dependent technical`

*A widely-held technical claim that holds in some operating contexts but is not a
physical or logical necessity; its truth depends on contextual variables (team maturity,
pipeline design, dependency topology, scale, workload shape).*

**Refined treatment:** Challenge specifically by naming the contextual variables that
would have to be true for the convention to hold in this case. Do not accept the
convention until those variables have been observed (or stated as expiry conditions on
the chain that consumes it).

**Cited evidence:**
- `first-principles/agents/references/examples/software-systems.md` — assumption row
  "Microservices enable faster deploys" (Type: convention; Verdict: Challenge; depends on
  team maturity, pipeline design, inter-service dependency topology).
- `first-principles/agents/references/examples/composed-inversion-second-order.md` —
  assumption row "Redis-in-front-of-Postgres is a viable read-through pattern at our
  scale" (Type: convention; Treatment: "convention is correct in general but says nothing
  about whether our specific read shape benefits"; Verdict: Challenge — pattern viability
  is not pattern fit).

#### `convention — design-practice (codified)`

*A convention codified in a named industry standard, design guideline, or engineering
practice (NEC, NREL/NABCEP guidelines, ASME pressure-vessel rules, DORA capacity
guidance, etc.) whose domain of validity is defined in the standard itself.*

**Refined treatment:** Accept tentatively if traceable to a named codified source and
the analysis's situation falls inside the standard's stated domain of applicability.
Record the domain assumptions explicitly as expiry conditions on any chain that consumes
the convention. The Challenge re-applies (with Verdict potentially shifting to Discard)
if those domain assumptions do not hold for the specific application.

**Cited evidence:**
- `first-principles/agents/references/examples/science-engineering.md` — assumption row
  "A system derating factor of 0.80 accounts for all losses in the energy path from
  panels to delivered load…" (Type: convention; Verdict: Accept; cited to
  NREL/NABCEP off-grid design guidelines; the 0.80 factor is a conservative
  design-practice value whose constituent loss budgets are traceable).

#### `convention — analogy-as-evidence`

*Reasoning of the form "others solved a similar problem this way, so we should too,"
where the other party's situation has not been characterized in terms of a named GT
that links their situation to ours.*

**Refined treatment:** **Discard** as standalone justification. An analogy may be
revived only if it is re-expressed as a named ground truth about the analogue (e.g., a
measured outcome under specified conditions) and a derivation chain shows those
conditions hold for our case. Treating analogy as direct evidence is also flagged by
`validation-rubric.md` Criterion 4 as a Hand-wavy pattern.

**Cited evidence:**
- `first-principles/agents/references/examples/product-business.md` — assumption row
  "All our competitors have a free tier, so we need one" (Type: convention; Verdict:
  Discard; Verification: "Analogy-as-evidence move. Competitor adoption of a pricing
  model is not evidence that the same model is economically viable for this product in
  this ICP segment at this ARR stage.").
- `first-principles/agents/references/examples/composed-inversion-second-order.md` —
  Dead End discussion in §Abandoned Reasoning where skipping the inversion pass by
  analogy to other caching projects is rejected because the analogy is not grounded in a
  named GT about the analogue.

#### `convention — default-response`

*A response so culturally available in a given domain that it is the first thing
reached for whenever a particular class of symptom appears, regardless of whether the
underlying cause has been diagnosed (e.g., "product overhaul to halt churn," "rewrite
to fix a slow service," "add a free tier to boost growth").*

**Refined treatment:** Challenge by asking whether the default response addresses the
highest-frequency observed signal versus the cognitively-available response. If the
observed signal points elsewhere (e.g., support-coverage gap, pipeline configuration,
ICP mismatch), the default response is reaching past the actual root cause and the
Verdict should reflect that mismatch rather than the default's general plausibility.

**Cited evidence:**
- `first-principles/agents/references/examples/ishikawa-fishbone.md` — assumption row
  "A full product overhaul is required to halt churn" (Type: convention; Verdict:
  Challenge; the highest-frequency exit-interview signal is "felt unsupported," not a
  product-feature complaint — the product-overhaul framing is the cognitively-available
  response, not the signal-driven one).

---

### Subtypes under `current constraint`

Parent-type treatment (from `output-template.md`): *Record expiry conditions and treat
as binding for the current decision; revisit when expiry conditions change.*

#### `current constraint — external-actor`

*A constraint that holds because another party (employer, partner, regulator, supplier,
business stakeholder) has made a decision the analyst does not control; expiry of the
constraint requires that external party to change their decision, not a measurement the
analyst can perform.*

**Refined treatment:** Name the external party, the specific decision they would need
to make for the constraint to lift, and a realistic probability/timeline for that
decision. Expiry is a negotiation or external-event move, not a measurement — chains
that depend on the constraint inherit that dependency explicitly.

**Cited evidence:**
- `first-principles/agents/references/examples/personal-general.md` — assumption row
  "The in-office three-days-per-week requirement is stable for this decision horizon"
  (Type: current constraint; expiry conditional on the offering company's remote policy
  changing or being renegotiated at signing).
- `first-principles/agents/references/examples/personal-general.md` — assumption row
  "The partner's Portland-based career cannot relocate" (Type: current constraint;
  expiry conditional on the partner's employer offering remote or an SF transfer).
- `first-principles/agents/references/examples/software-systems.md` — borderline case:
  assumption row "Slow deploys are causing meaningful, ongoing business harm"
  (Type: current constraint; expiry conditional on product velocity requirements
  decreasing — an external business-leadership decision rather than a measurement).

#### `current constraint — quantifiable-cost`

*A constraint whose binding force can be measured in a common unit (currency, time,
energy, headcount) and whose magnitude determines whether it is decision-relevant; the
constraint exists, but its weight in the decision is a function of the measured value.*

**Refined treatment:** Quantify the constraint's magnitude before recording expiry so
that the conclusion can be re-evaluated at any later value of the quantity without
re-running the whole analysis. The expiry condition should reference the measured value
("constraint inverts when X exceeds Y"), not the existence of the constraint.

**Cited evidence:**
- `first-principles/agents/references/examples/personal-general.md` — assumption row
  "San Francisco cost of living increase partially offsets the nominal compensation
  gain" (Type: current constraint; Verdict: Accept; the offset is real and quantified
  via GT-2's $1,300/month rent gap, making the constraint re-evaluable at any later
  rent figure).

---

### Subtypes under `untested belief`

Parent-type treatment (from `output-template.md`): *Verify before use; if used unverified
in a chain, mark with the "unverified — flagged" notation per D-07.*

#### `untested belief — diagnostic`

*A causal claim about which mechanism is responsible for an observed symptom (the
"deploy bottleneck is X," "the churn driver is Y") where multiple alternative mechanisms
could individually produce the same symptom.*

**Refined treatment:** Verify by ruling out alternative diagnoses with differential
evidence, not by collecting confirming evidence for the favoured diagnosis. A chain
that consumes a diagnostic belief without differential evidence inherits the diagnostic
ambiguity into the conclusion's confidence rating.

**Cited evidence:**
- `first-principles/agents/references/examples/software-systems.md` — assumption row
  "The deploy bottleneck is architectural coupling in the monolith" (Type: untested
  belief; Verdict: Challenge; Verification: "no pipeline profiling data has been
  collected; the 45-minute runtime is consistent with both architectural and
  non-architectural bottleneck causes" — the diagnostic ambiguity is exactly what the
  refined treatment names).

#### `untested belief — surface-from-tool`

*A belief surfaced by applying a structured Phase-2 tool (Ishikawa fishbone, inversion
pass, pre-mortem, five-whys) rather than stated as a direct claim. The surfacing tool
prescribes its own verification discipline, which the subtype inherits.*

**Refined treatment:** Inherit the surfacing tool's prescribed verification discipline
verbatim. For fishbone-surfaced beliefs, that is segment-and-compare across the
hypothesized cause category. For inversion-surfaced beliefs, that is precondition-test
of the specific assumption the inversion pass exposed. Do not re-derive a verification
plan from scratch — the tool already specifies one.

**Cited evidence:**
- `first-principles/agents/references/examples/ishikawa-fishbone.md` — assumption rows
  "Onboarding failure leaves customers under-activated" and "Accounts without a
  dedicated CSM churn at a higher rate" (Type: untested belief; both surfaced by the
  fishbone categorisation; both prescribe segment-and-compare verification — adoption
  scores by churn cohort; churn rate by CSM coverage status).
- `first-principles/agents/references/examples/composed-inversion-second-order.md` —
  the five assumption rows attributed in the **Source** column to `inversion pass`
  (e.g., "Cache hit rate at steady state is high enough to cross the read-QPS
  upgrade-threshold"; "The cached working set fits in the Redis memory budget"; "A
  correct invalidation path exists…"), each carrying a Treatment that is the specific
  precondition-test the inversion pass exposed.

#### `untested belief — economic-hinge`

*A belief on which the entire economic conclusion of the analysis hangs — if it is
false, the recommended approach is uneconomic regardless of how every other belief
resolves; if true, the recommendation is economic; intermediate truth does not exist
for the load-bearing question.*

**Refined treatment:** If a single belief is load-bearing for the entire conclusion, do
not enter Phase 5 (Validate) with it still flagged. Either verify it before signing off,
or downgrade the conclusion to a time-boxed pilot whose stated purpose is to measure
the hinge value. A HIGH-confidence rating on a chain that consumes an unverified
economic-hinge belief is incompatible with Criterion 5 of `validation-rubric.md`.

**Cited evidence:**
- `first-principles/agents/references/examples/product-business.md` — assumption row
  "Free users convert to paid at a meaningful rate" (Type: untested belief; Treatment:
  "Conversion rate is the economic hinge of the entire decision"; Verdict: Challenge;
  Verification: "no conversion data exists for this product in this ICP segment").

#### `untested belief — methodology`

*A belief that a particular calculation method, sizing rule, or estimation procedure is
the correct one for the problem at hand, where an alternative method exists and would
produce a different answer.*

**Refined treatment:** Verification is constructing the alternative method and
comparing outputs — not collecting more input data for the suspect method. Verdict is
typically Discard once the alternative produces a materially different (and more
defensible) answer. If both methods produce the same answer, the methodology belief is
verified and may be promoted to a `convention — design-practice (codified)` reference.

**Cited evidence:**
- `first-principles/agents/references/examples/science-engineering.md` — assumption row
  "Sizing the battery to sustain peak instantaneous load continuously is the correct
  approach" (Type: untested belief; Verdict: Discard; the alternative method —
  energy-balance over a 24-hour cycle accounting for actual run-time of the 250 W pump
  — produces a different (correct) answer, and the methodology belief is ruled out in
  the Abandoned Reasoning section).

#### `untested belief — false-dichotomy`

*A belief that frames the decision space as binary (A vs B, do-it-fully vs don't-do-it)
when intermediate or orthogonal options exist and have not been enumerated.*

**Refined treatment:** Challenge the binary framing — enumerate the omitted intermediate
options and check whether any of them dominates either pole on cost, risk, or
reversibility. Verdict is typically Discard once a non-binary path is documented in the
analysis.

**Cited evidence:**
- `first-principles/agents/references/examples/software-systems.md` — assumption row
  "A full rewrite or big-bang migration is required to change the architecture"
  (Type: untested belief; Verdict: Discard; the strangler-fig pattern is the documented
  intermediate path; the binary framing collapses once the intermediate is named).

---

### Subtypes under `physical law`

Parent-type treatment (from `output-template.md`): *Accept as ground-truth candidate;
promote to the Ground Truths section.*

#### `physical law — derived`

*A claim that follows by composition or definitional identity from one or more more
primitive physical laws (conservation, dimensional definitions, electrochemical rules)
and is reused as a calculation primitive in chains.*

**Refined treatment:** Promote to ground-truth candidate **and** record in the GT entry
the constituent physical laws / definitional identities the derivation rests on, so a
skeptic can re-derive the composite from the primitives without trusting the composite
as an axiom.

**Cited evidence:**
- `first-principles/agents/references/examples/science-engineering.md` — assumption row
  "A panel array's daily output equals rated wattage × Peak Sun Hours × system derating
  factor" (Type: physical law; Verification: "Derived directly from energy conservation
  and the definition of PSH" — the derivation explicitly names the constituent
  primitives).

> **Note on the rest of `physical law`:** v3.2 ships exactly one `physical law` subtype.
> The other shipped `physical law` rows (energy conservation; LiFePO4 80% DoD; chemistry
> facts) are flat parent-type uses and do not yet meet the D-06 evidence bar for further
> subtypes. Additional `physical law` subtypes await further shipped-example evidence.

---

## Application Notes

### Table presentation

The subtype, when used, appears **parenthetical-inline in the existing Type column** of
the Classified Assumptions Table defined in `output-template.md`. The schema is
unchanged — no Subtype column is added, no row reformatting is required, and shipped
worked examples that used parent types only remain valid without backfill.

Example Type-column cell values using the subtype-inline form:

| Type cell as written |
|----------------------|
| `convention (analogy-as-evidence)` |
| `untested belief (diagnostic)` |
| `untested belief (economic-hinge)` |
| `current constraint (external-actor)` |
| `convention (design-practice (codified))` |

The discriminator inside parentheses is the discriminator half of the subtype name
(everything after the em-dash). The parent token always leads. Authors who prefer the
full em-dash form (`convention — analogy-as-evidence`) inline in the cell may use it —
the parent token still leads either way; that is what `validation-rubric.md` Criterion
2 cares about.

### Rubric compatibility

`validation-rubric.md` Criterion 2 requires that every Type value be "drawn from exactly
the four-type scheme." Subtyped cells satisfy this requirement because the parent token
(`physical law` / `current constraint` / `convention` / `untested belief`) always leads
the cell value. A row with Type `convention (analogy-as-evidence)` is a `convention` row
for rubric purposes; the parenthetical refinement is metadata that prescribes a sharper
treatment, not a redefinition of the type. Existing rows that use only the parent type
also satisfy Criterion 2 — subtype use is recommended, not required.

### Notes on shipped examples that predate this taxonomy

Two shipped worked-example rows use types **outside** the four-type scheme:

- `first-principles/agents/references/examples/composed-inversion-second-order.md` —
  the row "The listings endpoint is the dominant contributor to Postgres read-QPS at
  peak" carries Type: `factual`. The nearest taxonomy slot is "a verified GT-candidate";
  it does not need a four-type slot because it was confirmed against the Q3 query-log
  sample at the time of the assumptions pass and behaves as a ground truth from there
  forward.
- `first-principles/agents/references/examples/composed-inversion-second-order.md` —
  the row "A two-engineer-week cache rollout is the lowest-cost intervention to defer
  the upgrade" carries Type: `value`. The nearest taxonomy slot is
  `convention — value-framing` (a candidate subtype that does not yet meet the D-06
  evidence bar with only one shipped example — flagged here for future inclusion if
  further evidence arrives).

Both rows **remain valid in their published form and must not be backfilled** into the
four-type scheme. The taxonomy refinement is forward-looking; shipped analyses authored
under v1.0 conventions stay as authored. Future analyses that encounter the same
patterns should map them to the four-type scheme (treating `factual` as a verified GT
inline, and treating `value` as a `convention` flagged for challenge until the
`convention — value-framing` subtype is itself adopted).

---

## Skeptic Self-Test Walkthrough

This section re-classifies the five assumption rows in
`first-principles/agents/references/examples/software-systems.md` (the Classified
Assumptions Table at lines 47–51) using only the subtypes catalogued above. A skeptic
reading this file in isolation should be able to follow the re-classification without
needing any context outside this file and the cited row's text.

### Row 1 — "Microservices enable faster deploys"

- **Original Type:** `convention`. **Original Verdict:** Challenge.
- **Proposed subtyped Type cell:** `convention (context-dependent technical)`.
- **Why this subtype:** The claim is widely held, but its truth depends on team
  maturity, pipeline design, inter-service dependency topology, and the nature of the
  coupling — these are exactly the contextual variables the
  `convention — context-dependent technical` subtype is for.
- **Refined treatment prescribed:** Challenge specifically by naming the contextual
  variables that would have to hold (e.g., parallelized CI per service, decoupled
  schemas, distributed-tracing-capable team) and observe whether they hold for this
  team and codebase before accepting the convention.
- **Resulting Verdict:** Challenge (unchanged from the original) — the refined treatment
  sharpens *why* the Challenge stands, not the Verdict itself.

### Row 2 — "The deploy bottleneck is architectural coupling in the monolith"

- **Original Type:** `untested belief`. **Original Verdict:** Challenge.
- **Proposed subtyped Type cell:** `untested belief (diagnostic)`.
- **Why this subtype:** The claim attributes a specific causal mechanism (architectural
  coupling) to an observed symptom (slow deploys) for which alternative mechanisms
  (test-suite wall-clock time, pipeline serialization, restart coordination) could
  independently produce the same symptom. That is the defining shape of
  `untested belief — diagnostic`.
- **Refined treatment prescribed:** Verify by ruling out the alternative diagnoses
  (parallelize the test suite; instrument the pipeline stages) with differential
  evidence — not by collecting more evidence that coupling is *consistent* with the
  symptom.
- **Resulting Verdict:** Challenge (unchanged) — the refined treatment makes the
  verification path explicit and points directly at the pipeline-profiling step the
  analysis ultimately recommends.

### Row 3 — "A 12-person team can operate a microservices estate at acceptable overhead"

- **Original Type:** `untested belief`. **Original Verdict:** Challenge.
- **Proposed subtyped Type cell:** `untested belief (economic-hinge)`.
- **Why this subtype:** Whether the team can absorb microservices ops overhead is
  load-bearing for the entire migration recommendation: if false, the migration is
  uneconomic regardless of any deploy-frequency gain; if true, the migration is at
  least feasible. There is no intermediate truth for the load-bearing question — the
  defining shape of `untested belief — economic-hinge`.
- **Refined treatment prescribed:** Do not enter Phase 5 with this belief flagged. Either
  verify it (e.g., by piloting a single extracted service and measuring ops load on the
  team) or downgrade any microservices recommendation to a time-boxed pilot whose
  stated purpose is to measure the overhead.
- **Resulting Verdict:** Challenge (unchanged) — the refined treatment escalates the
  Phase-5 obligation explicitly.

### Row 4 — "Slow deploys are causing meaningful, ongoing business harm"

- **Original Type:** `current constraint`. **Original Verdict:** Accept.
- **Proposed subtyped Type cell:** `current constraint (external-actor)`.
- **Why this subtype:** The constraint holds because business leadership has decided
  that more than ~2 deploys per day is required; expiry requires a leadership decision
  to lower velocity requirements, not a measurement the analyst can perform. That is
  the defining shape of `current constraint — external-actor` (the "external party" is
  business leadership; the borderline case in the subtype's own cited evidence).
- **Refined treatment prescribed:** Name the external party (business leadership) and
  the decision they would need to make (lowering required release cadence) as the
  expiry condition. Probability/timeline is "not foreseeable in this decision
  horizon" — which is itself a useful explicit statement.
- **Resulting Verdict:** Accept (unchanged) — the refined treatment makes the expiry
  condition's actor-dependent nature explicit, which the original Treatment cell only
  implies.

### Row 5 — "A full rewrite or big-bang migration is required to change the architecture"

- **Original Type:** `untested belief`. **Original Verdict:** Discard.
- **Proposed subtyped Type cell:** `untested belief (false-dichotomy)`.
- **Why this subtype:** The claim frames architectural change as binary (rewrite vs no
  change) when an intermediate option (the strangler-fig pattern for incremental
  extraction) exists and is documented in the engineering literature. That is the
  defining shape of `untested belief — false-dichotomy`.
- **Refined treatment prescribed:** Challenge the binary framing — enumerate the
  omitted intermediate options (strangler-fig, bounded-context schema decomposition,
  service-by-service extraction) and check whether any of them dominates either pole on
  cost, risk, or reversibility. Verdict typically Discard once a non-binary path is
  documented — which is exactly what the original Verification cell does.
- **Resulting Verdict:** Discard (unchanged) — the refined treatment names the
  general pattern (false-dichotomy) under which this specific binary framing falls,
  making the Verdict generalisable to future binary-framed assumptions of the same
  shape.

### Skeptic outcome

All five Verdicts are preserved under subtype refinement — subtypes sharpen the
treatment, they do not re-litigate the Verdict. Every row maps to a subtype whose
definition is fully resolved against text in this file alone, and the parent token
leads in every subtyped cell so `validation-rubric.md` Criterion 2 is satisfied
verbatim. A skeptic with only this file and the cited assumption-row text can audit
each step.
