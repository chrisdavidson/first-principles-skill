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
the five-whys reduce-to-primitives mode, not estimate. Estimate answers HOW BIG; five-whys reduce-to-primitives answers WHAT IS IT.

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

**Cross-technique handoff from five-whys (reduce-to-primitives) → estimate:** The five-whys reduce-to-primitives pass (Phase 3) hands
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
