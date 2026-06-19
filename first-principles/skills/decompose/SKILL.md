---
name: decompose
description: Runs a focused decompose only — reduces a claim to its irreducible primitives. Invoke via /decompose only.
disable-model-invocation: true
metadata:
  version: "7.1.0"
license: MIT
---
<!-- DO NOT EDIT — generated from shared/skills/decompose/SKILL.md by sync-content.py -->

# Focused Decompose Mode

You are running in focused-decompose mode. Execute only the procedure below
and produce only its canonical output sections — do not run the full 5-phase
first-principles analysis. Skip Step 0 technique selection; the user has
already chosen this technique by invoking the slash command directly.

## When to reach for this

Use decompose when you are holding a compound claim — an assertion built out of
multiple sub-claims — and you cannot tell whether the claim is solid or whether
one of its hidden constituents is assumed. The claim may be a cost estimate, a
performance promise, a design requirement, or a qualitative conclusion. The
question you are really asking is: "What is this actually made of, and is THAT
verified?"

**Good fit:** the claim can be broken into named constituent facts; at least one
constituent might be assumed rather than verified; the claim matters enough that
an unverified constituent would change the decision.

**Not a good fit:** the problem involves a recurring symptom with a traceable
causal chain — that pattern calls for 5-Whys, which drills down to an actionable
corrective rather than an irreducible primitive. It is also not the right tool
when the primary need is to map all the *categories* of contributing cause
across a complex system — that is a fishbone (Ishikawa) diagram, which works
across cause categories in parallel rather than reducing a single claim to its
definitional or physical foundations.

**Decision rule — choosing among the three:**

- **Decompose** = definitional/physical reduction: *What is this claim made of?*
  Stops when each constituent bottoms out at a physical law, a definition, or a
  direct measurement — an irreducible primitive that cannot be broken down further
  without losing the claim's meaning.
- **5-Whys** = causal depth: *Why does this symptom keep recurring?* Stops when
  a branch reaches a specific corrective action that is within the analyst's
  practical control.
- **Fishbone** = causal breadth: *What categories of cause could explain this
  effect?* Stops when the cause map is complete enough to select and test
  hypotheses.

A single analysis can use all three: decompose the performance claim, apply 5-Whys
to the failure that prompted the analysis, and use a fishbone to structure the
initial hypothesis space.

---

## Procedure

**State the claim.** Write one sentence naming the claim to be decomposed. Do not
start decomposing yet — just name the claim precisely.

**Identify its immediate constituents.** Ask: "What sub-claims is this claim built
out of?" List every component fact, assumption, or parameter the claim depends on.
Do not recurse yet; complete the lateral scan of one level before descending.

**Apply the irreducibility test to each constituent.** For each component, ask:
"Is this constituent itself reducible — can I state what *it* is made of?" If yes,
add its sub-constituents to the queue and recurse. If no, apply the stop test.

**Stop test.** Stop recursing a branch *only* when the branch bottoms out at one of:

- A **physical law** (a law of thermodynamics, conservation law, Ohm's law,
  Planck's relation, Newton's laws, etc.) — the branch is irreducible because
  physics does not reduce further.
- A **definition** (a formal or conventional definition that is true by construction,
  e.g. "one kilowatt-hour = 3.6 MJ") — reducible no further because the definition
  terminates the chain.
- A **direct measurement** (an observation you can point to: a datasheet spec,
  a calibrated instrument reading, a published standard value with a traceable
  source) — the branch stops because the fact is empirically anchored.

A branch that stops on a guess, an industry rule of thumb, or a vague recollection
has **not** passed the stop test — flag it as assumed.

**Record the verdict for each branch.**
- Branches that pass the stop test: mark the leaf `Verified — [physical law /
  definition / measurement]: <source or statement>`.
- Branches that fail (no irreducible anchor found): mark `Assumed — unverified`.
  These become GT-N? entries in Phase 3.

**Validate the parent claim.** Once all branches are exhausted, re-read the
original claim. A claim is verified only if every branch that feeds it is verified.
A claim that contains even one assumed branch inherits the `?` flag.

---

## Example

**Claim:** "A 200 W solar panel can charge a 100 Ah / 12 V battery from flat in
roughly one day of good sunlight."

**Immediate constituents:**

- C1: A 200 W panel delivers approximately 200 W under standard test conditions.
- C2: "Good sunlight" corresponds to approximately 5 peak sun hours per day.
- C3: Usable energy delivered = panel wattage × peak sun hours × system efficiency.
- C4: The battery's energy capacity is 100 Ah × 12 V = 1,200 Wh.

**Recursive decomposition:**

- C1: *Rated panel output* — bottoms out at the panel's datasheet specification
  (a direct measurement by the manufacturer under IEC 61215 standard conditions).
  **Stop — verified (measurement).**

- C2: *Peak sun hours* — depends on the site's solar irradiance. The 5 PSH figure
  is a location-specific empirical value (verifiable via NREL PVWatts for a given
  coordinate). For a concrete claim, a specific site must be named.
  **Stop — assumed (no specific site named); mark C2 as unverified.**

- C3: *Energy delivered = power × time × efficiency* — decomposes to energy
  conservation (energy out cannot exceed energy in, reduced by losses).
  **Stop — physical law (conservation of energy / first law of thermodynamics).
  Irreducible.**

- C4: *Battery capacity in watt-hours* — decomposes to the definition
  watt-hour = watts × hours = volts × amp-hours. 100 Ah × 12 V = 1,200 Wh is a
  unit-conversion definition.
  **Stop — definition. Irreducible.**

**Verdict:** C3 and C4 are verified; C1 is verified if the specific panel
datasheet is in hand; C2 is unverified for any claim that omits the specific
site. The parent claim inherits C2's uncertainty — "roughly one day of good
sunlight" is not verified until the site is named and the PSH figure is confirmed.

---

## Failure modes

**Stopping on familiarity, not on the test.** Accepting a constituent as
"obviously true" because it feels familiar — an industry rule of thumb, a
remembered figure — without checking whether it passes the physical-law /
definition / measurement stop test. Every branch must reach an irreducible anchor,
not just feel reducible enough.

**Halting the recursion mid-branch.** Decomposing two levels and then treating a
still-compound claim as a leaf because it became harder to unpack. The stop test
is the correct halt criterion, not the depth or the effort.

**Confusing decompose with 5-Whys.** Asking "Why is this wrong?" rather than
"What is this made of?" Decompose is a structural drill, not a causal drill. If
you find yourself tracing backwards through event chains or corrective actions,
you have shifted into 5-Whys territory.

**Treating "it's in the spec" as a verified primitive.** A spec value bottoms out
at a *direct measurement* only if the spec was produced by a calibrated,
traceable process. A vendor promise in a slide deck is not a measurement; it is an
untested belief and must be flagged as assumed.

**Over-decomposing definitions.** Continuing to recursively unpack a formal
definition beyond its defined boundary — the definition of a watt-hour does not
need to be derived from quantum electrodynamics. A definition terminates the chain.

---

## Handoff

The primitives produced by a decompose drill are the natural inputs to **Phase 3
(Establish Ground Truths)**, which is decompose's primary destination in the
5-phase methodology.

**Feeding Phase 3:** Each branch that passes the stop test (physical law /
definition / measurement) becomes a candidate ground truth. Assign it a stable
GT-N identifier and record the source citation (law name, definition reference,
measurement provenance). A branch that stops as `Assumed — unverified` enters the
ground truths list with the `GT-N?` suffix, inheriting the confidence caveat rules:
any derivation chain that consumes it is rated MEDIUM until the assumption is
verified.

**If reached during Phase 2 (Challenge Assumptions):** Add each verified primitive
as an `Accept` verdict in the Classified Assumptions Table; add each assumed
branch as an `untested belief` row with a `Challenge` verdict and a stated
verification path.

**If reached during Phase 4 (Reason Upward):** Add each verified primitive as
a validated step in the relevant Derivation Chain, citing the GT-N identifier
that anchors it.

Decompose differs from 5-Whys at the handoff boundary: 5-Whys hands off *causal
root causes* (the actionable corrective that stops recurrence); decompose hands
off *verified primitives* (the irreducible facts that anchor a claim). Both may
enter Phase 3, but they populate different rows of the Ground Truths list.

---

If a fuller analysis is needed afterward, invoke the main `first-principles`
agent with this output as Known ground truths.
