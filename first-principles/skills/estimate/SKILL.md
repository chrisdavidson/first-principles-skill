---
name: estimate
description: Runs a focused estimate only — magnitude rebuild from units. Invoke via /estimate only.
disable-model-invocation: true
metadata:
  version: "8.14.0"
license: MIT
---
<!-- DO NOT EDIT — generated from shared/skills/estimate/SKILL.md by sync-content.py -->

# Focused Estimate Mode

You are running in focused-estimate mode. Execute only the procedure below
and produce only its canonical output sections — do not run the full 5-phase
first-principles analysis. Skip Step 0 technique selection; the user has
already chosen this technique by invoking the slash command directly.

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

**Name the target quantity and its units** (e.g., "$/kWh of delivered storage")
before decomposing.

**Decompose into unit-factors and show the cancellation.** List the sub-quantities
that multiply to the target's units, confirming they cancel correctly — dimensional
analysis. Show the unit arithmetic explicitly (e.g., "kg/kWh × $/kg × 1/cycles →
$/kWh").

**Assign a first-principles value to each factor**, sourced from one of:

- A **physical constant or definition** (e.g., specific heat capacity) —
  traceable and invariant.
- A **direct measurement** (e.g., a datasheet spec) — empirically anchored.

Do **not** cite a similar past project as the value — "a comparable project cost X"
is an analogy, not a first-principles value. If no first-principles value exists,
flag it as assumed with a defensible range.

**Compute the central magnitude** by multiplying the factors' central values, with
the unit arithmetic explicit.

**Bracket the result.** For each uncertain factor, substitute its conservative and
aggressive values to compute the lower and upper ends: [lower bound, central
estimate, upper bound]. A Fermi estimate without an explicit bound range is
incomplete — the bracket, not the single central value, is the deliverable.

**Apply the decision-resolution stop criterion.** The estimate is "good enough"
when both the bracket's lower and upper ends drive the same decision. If the
bracket spans an order of magnitude and straddles the decision threshold, tighten
the dominant uncertain factor with a better measurement or escalate the
uncertainty explicitly.

**Read [estimate-detail.md](references/estimate-detail.md) when you need:**
- a worked example of this technique
- the failure modes and how to avoid them
- handoff guidance to another technique

---

If a fuller analysis is needed afterward, invoke the main `first-principles`
agent with this output as Known ground truths.
