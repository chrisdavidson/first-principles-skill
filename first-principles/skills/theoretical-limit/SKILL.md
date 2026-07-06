---
name: theoretical-limit
description: Strips conventions to the law-permitted ceiling. Invoke via /theoretical-limit only.
disable-model-invocation: true
metadata:
  version: "8.0.0"
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

**Name the conventional figure and the conventions embedded in it.** Write one
sentence naming the target figure — a performance metric, an efficiency, a cost
ceiling, a throughput rate — and describe the conventions it rests on: industry
practice, current engineering norms, historical precedent, or accepted defaults.
Do not strip yet — first make the convention visible.

**Strip each convention back to a governing physical law, definition, or direct
measurement.** For each convention identified, ask: "What physical law, formal
definition, or direct measurement determines what is actually possible here?"
Name the law explicitly (e.g., "the Second Law of Thermodynamics," "Carnot
efficiency bound," "Planck's radiation law," "Betz limit for wind turbines").
Do not reason by analogy to what others currently achieve — the ceiling is set
by the laws, not by the best incumbent.

**Derive the limit the fundamentals permit.** Using the governing law and the
first-principles values already in play (physical constants, definitions,
direct measurements), compute the theoretical upper bound the law allows. This
is the law-permitted ceiling: the highest the figure can go if every convention
is removed and only physics remains as a constraint.

**Bracket the gap between the law-permitted ceiling and the conventional
figure.** State explicitly:

- **Law-permitted ceiling:** the value the governing law allows.
- **Conventional figure:** the figure in current practice.
- **Gap:** the difference — how much headroom the fundamentals leave between
  current practice and what the laws actually permit.

Identify how much of the gap is irreducible (the laws impose it: a process that
converts X → Y can never be 100% efficient if the Second Law applies) versus
how much is convention (engineering headroom not yet captured — the laws allow
more, but practice has not reached it).

**Apply the stop criterion.** The analysis is complete when: (1) the governing
law is named explicitly, (2) the limit it imposes is derived from first-principles
values (constants, definitions, or direct measurements — not from what competitors
currently achieve), and (3) the gap between the law-permitted ceiling and the
conventional figure is stated explicitly. A theoretical-limit analysis that names
a ceiling without bracketing the gap to the conventional figure is incomplete —
the bracket, not the ceiling alone, is the deliverable.

---

## Example

**Target:** thermal-to-electric conversion efficiency of a molten-salt
concentrating solar power (CSP) plant — conventionally quoted at ~40–42% for
modern plants.

**Conventions embedded:** the 40–42% figure reflects the current power-cycle
engineering (steam Rankine cycle with supercritical parameters), real-world
turbine isentropic efficiency, practical heat-exchanger ΔT losses, and parasitic
loads — all of which are engineering choices, not physical laws.

**Governing law:** the Carnot efficiency bound (Second Law of Thermodynamics):
η_Carnot = 1 − T_cold / T_hot (temperatures in kelvin). No heat engine
operating between two reservoirs can exceed this bound regardless of engineering
sophistication.

**First-principles derivation:** Solar Salt operates at T_cold ≈ 290 °C =
563 K (cold tank) and T_hot ≈ 565 °C = 838 K (hot tank).
η_Carnot = 1 − 563/838 ≈ 0.33. Wait — this is lower than the conventional
figure. The Carnot bound here is a *hard ceiling on the ideal reversible
cycle*; the conventional figure exceeds it only because the 40–42% quote
uses the live-steam temperature in the turbine (≈ 560 °C / 833 K) as T_hot
and the condenser temperature (≈ 30–40 °C / 303–313 K) as T_cold:
η_Carnot (turbine cycle) = 1 − 308/833 ≈ 0.63. This is the physical ceiling
the cycle's steam conditions permit; 40–42% is well below it.

**Bracket:**

- Law-permitted ceiling (Carnot, turbine cycle): ~63%
- Conventional figure (modern CSP plants): ~40–42%
- Gap: ~21 percentage points — the laws permit far more than current practice
  captures. Most of this gap is engineering headroom (turbine efficiency losses,
  regeneration losses, parasitics); a small irreducible fraction is the
  Carnot penalty from non-zero ΔT across heat exchangers.

---

## Failure modes

**Citing best-in-class practice as the ceiling.** Using "the best plant in
the world achieves X%" as the theoretical limit. That is still a conventional
figure — a physical bound must derive from a named law, not from observation
of incumbents. Even the best incumbent may be far below the law-permitted
ceiling.

**Omitting the bracket.** Deriving the Carnot ceiling without comparing it
to the conventional figure defeats the purpose. The bracket (ceiling vs.
convention, and the gap between them) is the deliverable. A theoretical-limit
analysis that reports only a ceiling is half-finished.

**Confusing theoretical-limit with estimate.** If the question is "how big is
this quantity rebuilt from units?" reach for estimate. Theoretical-limit answers
"what is the highest this quantity can be, given the governing laws?" — it is
asking about a bound, not a magnitude rebuild.

**Confusing theoretical-limit with inversion.** If the question is "what would
guarantee this claim fails?" reach for inversion. Theoretical-limit asks what
is *possible* once conventions are stripped; inversion asks what is *fatal* if
a necessary precondition breaks.

**Naming the law but not deriving the bound from first-principles values.**
Saying "the Carnot bound applies" without computing η_Carnot from the actual
reservoir temperatures is an incomplete analysis. The ceiling must be derived
from the specific physical constants, definitions, or measurements at hand —
not stated in the abstract.

---

## Handoff

The law-permitted ceiling and the bracketed gap produced by a theoretical-limit
drill are the natural input to **Phase 4 (Reason Upward)**, which is
theoretical-limit's primary destination in the 5-phase methodology.

**Feeding Phase 4:** The governing law and the bracketed gap become the steps
of a quantitative **Derivation Chain**: `GT-N → [governing law] →
[law-permitted ceiling] → [gap to convention]`. Each step cites the ground
truth that anchors it — a physical constant, a definition, or a measurement
assigned a GT-N identifier in Phase 3. The gap is the key intermediate claim:
a conclusion that depends on a figure being near its physical limit is sound
only if the gap confirms that; a conclusion that depends on substantial
remaining headroom is contingent only if the gap confirms there is headroom to
capture.

**Lighter Phase 1 anchor:** A theoretical-limit analysis often reframes the
core question identified in **Phase 1 (Identify the Essence)**. Establishing
the law-permitted ceiling forces the essence question into sharper focus: "Is
the performance limited by the laws, or by a convention we have not questioned?"
If the analysis reveals the conventional figure is far below the Carnot ceiling,
the Essence Statement may need to be revised to name the real constraint — not
"can we exceed 42%?" but "what engineering convention is blocking capture of the
21-point headroom the laws allow?"

**Cross-technique continuity (five-whys reduce-to-primitives → estimate → theoretical-limit):**
In the molten-salt running example, the five-whys reduce-to-primitives pass (Phase 3) produced the verified
primitives for the operating window and material properties; estimate (Phase 4)
rebuilt the cost magnitude from unit-factors. Theoretical-limit takes the same
domain and asks: given the reservoir temperatures that the five-whys reduce-to-primitives pass established as
ground truths, what does the Second Law permit? The three techniques form a
traceable chain across the same set of GT-N identifiers.

Theoretical-limit differs from estimate at the handoff boundary: estimate hands
off a *bracketed magnitude* (a quantity with explicit lower/upper bounds from
factor uncertainty); theoretical-limit hands off a *law-permitted ceiling and
a gap* (a hard bound the laws impose, and the distance current practice sits
below it). Both feed Phase 4, but they populate different steps in a Derivation
Chain — estimate populates the quantitative magnitude step; theoretical-limit
populates the physical-bound step.

---

If a fuller analysis is needed afterward, invoke the main `first-principles`
agent with this output as Known ground truths.
