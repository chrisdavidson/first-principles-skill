<!-- GENERATED — DO NOT EDIT. Source: shared/references/theoretical-limit-detail.md. Regenerate via: scripts/sync-content.py --write. -->

<!-- markdownlint-disable MD041 -->

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
