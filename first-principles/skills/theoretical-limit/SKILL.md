---
name: theoretical-limit
description: Strips conventions to the law-permitted ceiling. Invoke via /theoretical-limit only.
disable-model-invocation: true
metadata:
  version: "9.9.0"
license: MIT
---
<!-- DO NOT EDIT — generated from shared/skills/theoretical-limit/SKILL.md by sync-content.py -->

# Focused Theoretical-Limit Mode

You are running in focused-theoretical-limit mode. Execute the procedure below, produce
its canonical output sections, then run the focused-mode validation step below —
do not run the full 5-phase first-principles analysis. Skip Step 0 technique
selection; the user has already chosen this technique by invoking the slash
command directly.

## When to reach for this

Use theoretical-limit when a decision hinges on whether a current figure is
close to what the laws permit or whether there is substantial headroom the
convention has not captured. The question you are really asking is: "If every
convention were removed, what do the laws actually permit here — and how far
below that ceiling are we operating?"

**Good fit:** a conventional figure exists (industry practice, historical
precedent, accepted engineering default) and you suspect it may embed a
convention — a rule of thumb, a legacy design choice, a practical constraint —
rather than a governing hard constraint; you want to know the upper bound on
what is achievable; a claim about performance or cost rests on an assumption
that current practice is near-optimal.

**Not a good fit:** the question is "what would cause this claim to fail?" —
that is inversion, which enumerates necessary preconditions for failure rather
than deriving what the laws permit. It is also not the right tool when the
primary need is to rebuild a magnitude from constituent unit-factors — that is
estimate (Fermi / dimensional analysis), which reconstructs HOW BIG a quantity
is from its units, not what ceiling the fundamentals impose on it.

**Decision rule — separating the upper-bound move from its neighbours:**

- **Theoretical-limit** = what the laws permit once conventions are stripped:
  *what is the ceiling the fundamentals allow?* Names the governing hard
  constraint, derives the bound it imposes, and brackets the conventional figure
  against both the best demonstrated result and that bound.
- **Inversion** = adversarial attack on a claim/plan: *what would guarantee
  failure?* Enumerates necessary preconditions for collapse — the closest
  neighbour and the real collision risk; theoretical-limit asks what is
  *possible*, inversion asks what is *fatal*.
- **Estimate** = quantitative magnitude rebuild from units: *how big is this
  quantity?* Reconstructs a target number from constituent unit-factors
  (dimensional analysis).

A single analysis often uses all three: apply theoretical-limit to find the
law-permitted ceiling, estimate to rebuild the conventional figure from
unit-factors, and inversion to surface which assumptions would need to break
for the ceiling to be unreachable.

---

## Procedure

**Name the conventional figure and its embedded conventions** (a performance
metric, efficiency, or cost ceiling) before stripping anything.

**Strip each convention back to a governing hard constraint, definition, or
direct measurement.** Name the constraint explicitly (e.g., "the Second Law of
Thermodynamics," "Carnot efficiency bound," "the speed of light in fiber"). A
governing hard constraint is whatever genuinely cannot be negotiated in this
domain — a physical law, a mathematical bound, a conservation identity, a
protocol's minimum round trips. It is often not thermodynamic, and the technique
applies wherever such a constraint exists. Do not reason by analogy to what
others currently achieve — the ceiling is set by the constraint, not by the best
incumbent.

**Derive the limit the fundamentals permit**, using the governing constraint and
first-principles values (constants, definitions, direct measurements). This is
the ideal ceiling: the highest the figure can go if every convention is removed
and only the constraint remains.

**Use the tightest applicable bound — a valid bound is not automatically the
right one.** The loosest true bound is always available and is nearly always
useless: it is true, unfalsifiable, and overstates headroom, so an analysis
bracketed against it reports far more room than really exists. Ask what else
binds before the ideal ceiling does — materials, cost, a practical operating
point, a regulatory floor — and bracket against that too.

**Bracket in three tiers.** State each explicitly, and label which is which:

- **Ideal ceiling:** what the governing hard constraint permits. Derived, not
  observed. Nothing can exceed it.
- **Best demonstrated:** the best figure anyone has actually achieved, **cited**
  — a record, a measured result, a published benchmark. This tier is an
  *observation*, never a calculation.
- **Conventional figure:** what current practice in this context achieves.

Then state two gaps rather than one: **conventional → best demonstrated** is
headroom somebody has already proven reachable, and **best demonstrated → ideal
ceiling** is headroom nobody has reached yet. The two are different claims with
very different risk, and collapsing them into a single "gap" is what makes a
theoretical-limit analysis sound more actionable than it is.

Identify how much of the gap is irreducible (the constraint imposes it — a
process converting X → Y can never be 100% efficient under the Second Law)
versus how much is convention (headroom the constraint allows but practice has
not reached).

**A model-dependent bound is not a ceiling.** Many published "limits" are the
answer to a narrower question than the one being asked, and real systems exceed
them. Before using a bound as a tier, ask *what exactly does this bound
constrain, and under what assumptions?* If it is model-dependent, either label
it as an illustrative reference rather than a ceiling, or drop it. The
Curzon-Ahlborn efficiency is the standard cautionary case: it is the efficiency
of an endoreversible engine **at maximum power**, not a maximum efficiency, and
real plants that trade power density for efficiency exceed it — so using it as a
"practical ceiling" understates what is achievable. Put an observed record in the
demonstrated tier instead of a computed one.

**Apply the stop criterion.** The analysis is complete when: (1) the governing
hard constraint is named explicitly, (2) the ideal ceiling is derived from
first-principles values — not from what competitors achieve, (3) the best
demonstrated figure is cited as an observation, and (4) both gaps are stated
explicitly. A theoretical-limit analysis that names a ceiling without bracketing
those gaps is incomplete — the bracket, not the ceiling alone, is the
deliverable.

**Read [theoretical-limit-detail.md](references/theoretical-limit-detail.md) when you need:**
- a worked example of this technique
- the failure modes and how to avoid them
- handoff guidance to another technique

## Focused-mode validation

**Check the output against its own completion condition before presenting it.** The
procedure above states one, in whichever form this technique uses — an exit criterion, a
stop test, or an output contract. Read that condition again and confirm the output actually
produced meets every requirement it names, not just the ones that were easiest to satisfy.

**This is a scope-proportionate check, not the six-criterion Self-Audit Gate.** That gate
scores a six-section analysis document; this run produced one technique's output sections,
not six, so walking all six criteria against it would score structure that was never
produced. The larger of the two components: a focused run does not acquire evidence — it
opens no cited source — so a claim resting on a source this run did not open stays marked
rather than being resolved as confirmed.

**Carry the mark forward.** Anything this run could not verify is carried into the output
marked with a `?` rather than dropped or silently asserted as fact.

**Revise once, then stop.** If the check fails, revise the output and check it again.
Revise at most one time. If it still fails after that pass, present the output with the
gap named rather than revising again.

**End every run with a validation line, without exception.** State exactly one of the
following, verbatim, never silently:

- `Focused-mode validation: satisfied`
- `Focused-mode validation: revised once, now satisfied`
- `Focused-mode validation: not satisfied - <reason>`

Close with the reason this line is unconditional: a silent run is indistinguishable from a
run that skipped the check.

---

If a fuller analysis is needed afterward, invoke the main `first-principles`
agent with this output as candidate inputs for Phase 2. Carry the `?` marks
with it — this run opened no cited source.
