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
primitives — that is the five-whys reduce-to-primitives mode, which traces a claim's structure down to physical
laws and definitions rather than rebuilding a quantity's order of magnitude.

**Decision rule — choosing among the three quantitative-ish techniques:**

- **Estimate** = quantitative magnitude rebuild: *HOW BIG is this quantity?*
  Reconstructs a target number from constituent unit-factors (dimensional analysis).
  Stops when the factor product yields a bracketed magnitude — lower, central, upper.
- **Trade-off** = qualitative weighted scoring: *WHICH option wins on weighted
  criteria?* Assigns importance weights to criteria before scoring, preventing the
  reverse-engineering of weights to justify an intuitive pick.
- **Five-whys (reduce-to-primitives)** = definitional/physical reduction: *WHAT is this claim made of?*
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

**Read [estimate-detail.md](estimate-detail.md) when you need:**
- a worked example of this technique
- the failure modes and how to avoid them
- handoff guidance to another technique
