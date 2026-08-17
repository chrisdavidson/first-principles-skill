---
name: theoretical-limit
description: Strips conventions to the law-permitted ceiling. Invoke via /theoretical-limit only.
disable-model-invocation: true
metadata:
  version: "8.17.4"
license: MIT
---
<!-- DO NOT EDIT — generated from shared/skills/theoretical-limit/SKILL.md by sync-content.py -->

# Focused Theoretical-Limit Mode

You are running in focused-theoretical-limit mode. Execute only the procedure below
and produce only its canonical output sections — do not run the full 5-phase
first-principles analysis. Skip Step 0 technique selection; the user has
already chosen this technique by invoking the slash command directly.

## When to reach for this

Use theoretical-limit when a decision hinges on whether a current figure is
close to what the laws permit or whether there is substantial headroom the
convention has not captured. The question you are really asking is: "If every
convention were removed, what do the laws actually permit here — and how far
below that ceiling are we operating?"

**Good fit:** a conventional figure exists (industry practice, historical
precedent, accepted engineering default) and you suspect it may embed a
convention — a rule of thumb, a legacy design choice, a practical constraint —
rather than a hard physical limit; you want to know the upper bound on what is
achievable; a claim about performance or cost rests on an assumption that current
practice is near-optimal.

**Not a good fit:** the question is "what would cause this claim to fail?" —
that is inversion, which enumerates necessary preconditions for failure rather
than deriving what the laws permit. It is also not the right tool when the
primary need is to rebuild a magnitude from constituent unit-factors — that is
estimate (Fermi / dimensional analysis), which reconstructs HOW BIG a quantity
is from its units, not what ceiling the fundamentals impose on it.

**Decision rule — separating the upper-bound move from its neighbours:**

- **Theoretical-limit** = what the laws permit once conventions are stripped:
  *what is the ceiling the fundamentals allow?* Names the governing law, derives
  the bound it imposes, brackets the gap between that bound and the conventional
  figure.
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

**Strip each convention back to a governing physical law, definition, or direct
measurement.** Name the law explicitly (e.g., "the Second Law of Thermodynamics,"
"Carnot efficiency bound"). Do not reason by analogy to what others currently
achieve — the ceiling is set by the laws, not by the best incumbent.

**Derive the limit the fundamentals permit**, using the governing law and
first-principles values (constants, definitions, direct measurements). This is
the law-permitted ceiling: the highest the figure can go if every convention is
removed and only physics remains as a constraint.

**Bracket the gap between the law-permitted ceiling and the conventional
figure.** State explicitly:

- **Law-permitted ceiling:** the value the governing law allows.
- **Conventional figure:** the figure in current practice.
- **Gap:** the headroom between current practice and what the laws permit.

Identify how much of the gap is irreducible (the laws impose it — a process
converting X → Y can never be 100% efficient under the Second Law) versus how
much is convention (headroom the laws allow but practice has not reached).

**Apply the stop criterion.** The analysis is complete when: (1) the governing
law is named explicitly, (2) the limit is derived from first-principles values
— not from what competitors achieve — and (3) the gap to the conventional
figure is stated explicitly. A theoretical-limit analysis that names a ceiling
without bracketing that gap is incomplete — the bracket, not the ceiling alone,
is the deliverable.

**Read [theoretical-limit-detail.md](references/theoretical-limit-detail.md) when you need:**
- a worked example of this technique
- the failure modes and how to avoid them
- handoff guidance to another technique

---

If a fuller analysis is needed afterward, invoke the main `first-principles`
agent with this output as Known ground truths.
