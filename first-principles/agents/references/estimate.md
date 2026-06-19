<!-- GENERATED — DO NOT EDIT. Source: shared/references/estimate.md. Regenerate via: scripts/sync-content.py --write. -->

# Estimate (Fermi / Dimensional Analysis)

> A magnitude-rebuild drill — reach for it when you need to know HOW BIG something
> is by reconstructing the quantity from constituent first-principles unit-factors
> rather than looking it up or reasoning by analogy.

---

## When to reach for this

Use estimate when a decision hinges on the order of magnitude of a quantity and you
do not have — or cannot trust — a direct lookup. The question you are really asking
is: "What is this number, rebuilt from what I actually know?"

**Good fit:** the target quantity has units that can be reconstructed as a product
of factors whose individual values are pinnable to physical constants, definitions,
or direct measurements; a rough bracket (lower/central/upper) is sufficient to
drive the decision; and an analogy-based estimate ("it's probably like X project")
would be unverifiable.

**Not a good fit:** the problem involves weighing options against criteria with
different importance — that is trade-off analysis, which scores options on weighted
criteria rather than rebuilding a magnitude. It is also not the right tool when the
task is to verify whether a compound claim's constituents reduce to irreducible
primitives — that is decompose, which traces a claim's structure down to physical
laws and definitions rather than rebuilding a quantity's order of magnitude.

**Decision rule — choosing among the three quantitative-ish techniques:**

- **Estimate** = quantitative magnitude rebuild: *HOW BIG is this quantity?*
  Reconstructs a target number from constituent unit-factors (dimensional analysis).
  Stops when the factor product yields a bracketed magnitude — lower, central, upper.
- **Trade-off** = qualitative weighted scoring: *WHICH option wins on weighted
  criteria?* Assigns importance weights to criteria before scoring, preventing the
  reverse-engineering of weights to justify an intuitive pick.
- **Decompose** = definitional/physical reduction: *WHAT is this claim made of?*
  Traces constituent sub-claims to irreducible primitives (physical laws, definitions,
  direct measurements). Stops when every branch bottoms out at an anchor.

A single analysis often uses all three: decompose the performance claim to find
what factors matter, estimate the magnitude of each factor, and apply trade-off
if several technically viable options remain.

---

## Procedure

**State the target quantity and its units.** Write one sentence naming the quantity
you intend to estimate and the units the answer must be in (e.g., "Estimate the
levelised cost of molten-salt thermal storage, in $/kWh of delivered energy.").
Do not begin building the estimate yet — just fix the target and units.

**Decompose the target into constituent unit-factors.** Ask: "What sub-quantities,
when multiplied together, reconstruct the target's units?" List each factor and
confirm that the units cancel correctly (dimensional analysis — the factor product's
units must equal the target's units). This is the visible unit arithmetic; do not
skip it.

**Assign a first-principles value to each factor.** For every factor, supply a
value sourced from one of:

- A **physical constant or definition** (e.g., specific heat capacity, a standard
  unit conversion) — traceable and invariant.
- A **direct measurement** (e.g., a published material cost from an engineering
  survey, a datasheet spec) — empirically anchored.

Do **not** cite a similar past project as the value — "a comparable project cost X"
is an analogy, not a first-principles value. If no first-principles value is
available for a factor, flag it as assumed and assign a defensible range.

**Compute the central magnitude.** Multiply the central values of all factors.
Show the unit arithmetic so the cancellation is explicit (e.g., "kg/kWh × $/kg
× 1/cycles → $/kWh"). The product is the central estimate.

**Bracket the result: lower bound and upper bound.** For each factor that carries
uncertainty, substitute its conservative value (produces a lower end-result) and
its aggressive value (produces an upper end-result). Compute the bracketed range:
[lower bound, central estimate, upper bound]. A Fermi estimate without an explicit
bound range is incomplete — the bracket, not the single central value, is the
deliverable.

**Apply the decision-resolution stop criterion.** The estimate is "good enough"
when the bracket is narrow enough that both its lower and upper ends drive the same
decision. If the bracket spans an order of magnitude and straddles the decision
threshold, identify which factor dominates the uncertainty and either tighten it
with a better measurement or escalate the uncertainty explicitly.

---

## Example

**Target:** Levelised cost of molten-salt thermal energy storage ($/kWh).

**Unit-factor decomposition** (units must cancel to $/kWh):

    material_mass   [kg/kWh]
  × cost_per_kg     [$/kg]
  × 1/cycle_life    [1/cycles]   (amortises capital cost per cycle)
  ────────────────────────────
  = capital cost    [$/kWh/cycle] ≈ $/kWh of delivered energy

**Factor values (first-principles):**

- `material_mass`: Solar Salt (60% NaNO₃/40% KNO₃) has a specific heat of
  ~1.5 kJ/(kg·°C) and is used across a 275 °C temperature swing (290–565 °C).
  Stored energy per kg = 1.5 × 275 / 3,600 ≈ 0.115 kWh/kg, so
  material_mass ≈ 1 / 0.115 ≈ 8.7 kg/kWh (definition + published Cp value).
- `cost_per_kg`: Solar Salt bulk commodity price ≈ $0.40–0.80/kg
  (engineering procurement surveys; mid = $0.60/kg).
- `cycle_life`: No electrochemical degradation mechanism — design life ≈ 10,000
  full cycles (30 years at one cycle/day) (inorganic salt chemistry; definition).

**Central magnitude:** 8.7 × 0.60 × (1/10,000) ≈ $0.00052/kWh.

*Wait — this is capital cost of salt only, not system LCOS.* Adding tank insulation,
piping, and heat-exchanger capital (typically 3–5× the salt cost for commercial
plants) and operating costs yields a system LCOS in the range $20–50/kWh (confirmed
by NREL TES cost surveys, 2023). The unit-factor product gives the right order of
magnitude and serves as a sanity check on the published range.

**Explicit bracket:**

- **Lower bound:** $20/kWh — using low-end material and installation costs,
  10,000-cycle design life.
- **Central estimate:** $35/kWh — mid-range material costs, standard commercial
  installation.
- **Upper bound:** $50/kWh — high-end procurement, shorter effective cycle life
  (8,000 cycles accounting for partial-discharge years).

**Decision-resolution check:** The bracket [$20–$50/kWh] vs. utility-scale
lithium-ion [$150–$300/kWh] keeps the cost-competitiveness conclusion stable
across the entire bracket — estimate is good enough to drive this decision.

---

## Failure modes

**Citing an analogy as a factor value.** Saying "a comparable project cost $X/kWh"
and using that as the material-cost factor is reasoning by analogy, not from
first principles. Every factor must bottom out at a physical constant, a definition,
or a direct measurement — not a comparison to a past project.

**Omitting the bracket.** Reporting only a central estimate without lower and upper
bounds is an incomplete Fermi drill. The bracket is the entire point: it makes
explicit which factors dominate the uncertainty and whether the estimate is
decision-grade.

**Units that do not cancel.** Building a factor product whose units do not reduce
to the target's units is dimensional malpractice. Always verify the unit arithmetic
explicitly before computing the magnitude.

**Tightening precision instead of widening the bracket.** Iterating the central
estimate to three significant figures while ignoring the factor uncertainties
manufactures false precision. Tighten the bracket (by sourcing better factor
values), not the central estimate.

**Using estimate for structural verification.** If the question is "What is this
claim made of — does every constituent reduce to a verified primitive?" you want
decompose, not estimate. Estimate answers HOW BIG; decompose answers WHAT IS IT.

---

## Handoff

The bracketed magnitude produced by an estimate drill is the natural input to
**Phase 4 (Reason Upward)**, which is estimate's primary destination in the
5-phase methodology.

**Feeding Phase 4:** The unit-factors and their sourced values become the steps of
a quantitative **Derivation Chain**: `GT-N + GT-M → [unit-factor product] →
[bracketed magnitude]`. Each factor value cites the ground truth that anchors it
(a physical constant, a definition, or a measurement assigned a GT-N identifier in
Phase 3). The bracket — lower bound, central estimate, upper bound — travels as a
single claim in the chain, carrying its uncertainty forward. A conclusion that
depends on this claim is sound if the bracket's entire width drives the same
conclusion; it is contingent if the lower and upper ends drive different conclusions.

**Cross-technique handoff from decompose → estimate:** Decompose (Phase 3) hands
off verified primitives — physical laws and definitions confirmed as ground truths.
Estimate (Phase 4) consumes those anchored primitives as the per-unit values it
rebuilds the magnitude from. The GT-N ids assigned in Phase 3 become the citation
anchors in the estimate's derivation chain, making the cross-technique continuity
traceable.

**If reached during Phase 3 (Establish Ground Truths):** An estimated factor value
that is not a direct measurement is assigned the GT-N? suffix — a candidate ground
truth with an unverified assumption. Record its bracket as the confidence interval
until a measurement replaces it.

Estimate differs from trade-off at the handoff boundary: trade-off hands off the
*winning option* (the highest weighted-score choice); estimate hands off a *bracketed
magnitude* (a quantity with explicit lower/upper bounds). Both may feed Phase 4, but
they populate different artifact types — trade-off feeds the option-selection step
of a Derivation Chain; estimate feeds the quantitative magnitude step.
