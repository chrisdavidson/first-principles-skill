# Worked Example: Theoretical Limit — Carnot Constraint-Relaxation (Thermal Energy Storage)

A focused demonstration of the **theoretical-limit** (constraint relaxation / physical-bound
derivation) technique applied to the same molten-salt thermal energy storage domain used in
the five-whys (reduce-to-primitives) and estimate examples — showing the cross-technique handoff from Phase 3
(verified primitives) and Phase 4 (quantitative derivation chain) to the physical-bound step.
The drill makes the constraint-relaxation story visible: strip the conventional figure,
name the governing law explicitly, derive the law-permitted ceiling from first-principles
values, and bracket the gap between that ceiling and current practice.

**Target:** the thermal-to-electric conversion efficiency of the Rankine-cycle heat engine
operating across the molten-salt reservoir temperature pair — the same 290–565 °C window
established in the five-whys (reduce-to-primitives) example as GT-4. The conventional (engineering-practice) figure
for this temperature pair is the efficiency a real Rankine cycle achieves at these reservoir
conditions. The question: how far below the law-permitted ceiling is current practice?

**Why this matters.** The estimate example (Phase 4) rebuilt the cost magnitude from
unit-factors. This theoretical-limit drill asks a different question of the same domain:
given the reservoir temperatures that the five-whys reduce-to-primitives pass established as ground truths, what does
the Second Law permit for the heat engine operating between them? The ceiling-vs-convention
bracket reveals whether the efficiency headroom is real or illusory.

---

## Theoretical-Limit Drill

### Step 1 — Name the conventional figure and the conventions embedded in it

**Conventional figure:** A real Rankine-cycle heat engine operating across the Solar Salt
temperature pair (T_hot = 565 °C, T_cold = 290 °C) achieves a practical heat-to-electricity
conversion efficiency of approximately **20–25%** under commercial operating conditions.

**Conventions embedded in this figure:**
- Real turbine isentropic efficiency: commercial steam turbines operating in this temperature
  range achieve 75–85% isentropic efficiency — well below the reversible ideal.
- Heat-exchanger thermal losses: finite ΔT across the heat exchangers between salt and steam
  reduces effective T_hot below the salt's 565 °C.
- Parasitic loads: pumps, controls, and auxiliary systems consume part of the gross output.
- Working fluid: the Rankine cycle uses steam, which introduces condensation and boiling
  irreversibilities not present in an ideal reversible cycle.

These are engineering conventions — design and practice choices that current technology
has not yet optimised to the physical limit. The governing law sets a ceiling independent
of all of them.

---

### Step 2 — Name the governing law and the first-principles values

**Governing law: the Carnot efficiency bound (Second Law of Thermodynamics)**

No heat engine operating between two thermal reservoirs can exceed the Carnot efficiency,
regardless of the working fluid, the cycle design, the equipment quality, or any
engineering refinement. This is not an engineering limitation — it is an irreducible
physical law.

The Carnot bound for a heat engine operating between reservoir temperatures T_hot and
T_cold (both in kelvin) is:

    η_Carnot = 1 − T_cold / T_hot

**First-principles values** (from GT-4, established in the five-whys (reduce-to-primitives) example):

The Solar Salt operating window is 290–565 °C. Converting to kelvin (the conversion
definition: T [K] = T [°C] + 273.15):

    T_cold = 290 °C + 273 ≈ 563 K   (cold tank / lower reservoir)
    T_hot  = 565 °C + 273 ≈ 838 K   (hot tank / upper reservoir)

These are the reservoir temperatures the heat engine must operate between. They are direct
measurements anchored by GT-4 — not engineering estimates or analogy-based figures.

---

### Step 3 — Derive the law-permitted ceiling

Substituting the GT-4 reservoir temperatures into the Carnot formula:

    η_Carnot = 1 − T_cold / T_hot
             = 1 − 563 / 838
             ≈ 1 − 0.672
             ≈ 0.328

**Law-permitted ceiling: ~33%**

This is the highest thermal-to-electric conversion efficiency that any heat engine
operating between the Solar Salt reservoir temperatures (563 K and 838 K) can achieve —
not for any specific cycle or working fluid, but for any thermodynamically conceivable
process. The Second Law imposes this ceiling absolutely.

---

### Step 4 — Bracket the gap explicitly

| | Value | Basis |
|---|---|---|
| **Law-permitted ceiling (Carnot)** | ~33% | Second Law; GT-4 reservoir temperatures |
| **Conventional figure (real Rankine)** | ~20–25% | Engineering practice at these conditions |
| **Gap** | ~8–13 percentage points | Engineering headroom not yet captured |

**Gap decomposition:**

The ~8–13 point gap between the Carnot ceiling and real Rankine efficiency breaks into:

- **Irreducible fraction:** zero — in principle, the gap is entirely engineering headroom.
  The Carnot bound is a ceiling, not a floor: a perfect reversible process operating at
  these reservoir temperatures would reach 33%, and no physical law prevents
  approaching it (though never reaching it in finite time for a finite-power machine).

- **Engineering convention fraction:** ~8–13 points — current turbine isentropic losses
  (~4–5 points), heat-exchanger ΔT losses (~2–3 points), and parasitic loads (~1–2 points)
  account for the gap. These are design choices, not physical constraints.

**Constraint-relaxation conclusion:** The conventional 20–25% efficiency figure is not
near a physical ceiling — the laws permit ~33%. There is meaningful headroom (~8–13
percentage points) available through engineering improvement: higher isentropic efficiency
turbines, tighter heat-exchanger ΔT, lower parasitic loads. The headroom is real, not
illusory. A plant that captures all the engineering headroom (impossible in practice, but
the theoretical limit) approaches 33%.

---

## Phase 4 Handoff — Physical-Bound Derivation Chain

The law-permitted ceiling and the bracketed gap enter **Phase 4 (Reason Upward)** as a
physical-bound step in a **Derivation Chain**, citing the Phase 3 ground truths that
anchor the governing law and the reservoir temperatures:

**Chain: Molten-Salt TES Heat-Engine Efficiency Bound**

    GT-4  (Solar Salt stable 290–565 °C; T_cold ≈ 563 K, T_hot ≈ 838 K — direct measurement,
           five-whys (reduce-to-primitives) example Phase 3 ground truth)
      +
      Second Law of Thermodynamics: Carnot bound η = 1 − T_cold/T_hot
      →
      Law-permitted ceiling: η_Carnot = 1 − 563/838 ≈ 33%
      →
      Conventional figure (real Rankine at these conditions): ~20–25%
      →
      Bracketed gap: ~8–13 percentage points of engineering headroom
      →
      [Conclusion: ~8–13 percentage points of thermal-to-electric conversion efficiency
       are available as engineering headroom above current practice at these reservoir
       temperatures. The headroom is governed by engineering conventions (turbine
       isentropic losses, heat-exchanger ΔT, parasitics), not by a physical barrier.
       Confidence: HIGH — the Carnot ceiling is irreducible; the conventional figure
       is anchored in published turbine operating data for this temperature range.]

**Cross-technique continuity.** The five-whys reduce-to-primitives drill (Phase 3) established GT-4 — the
Solar Salt temperature window. The estimate drill (Phase 4) consumed GT-4 to rebuild the
cost magnitude from unit-factors. This theoretical-limit drill (Phase 4) consumes GT-4
to derive the physical ceiling the Second Law imposes on the heat engine operating across
those same reservoir temperatures. The three techniques form a traceable chain:
five-whys reduce-to-primitives → estimate → theoretical-limit, all anchored to GT-4.

**Phase 1 reframe.** The theoretical-limit result invites a Phase 1 (Identify Essence)
reframe: the core question is no longer "is 20–25% acceptable?" but "is the ~8–13 point
gap a recoverable engineering opportunity or a permanently foregone constraint?" The
Carnot ceiling reveals the real question — are we limited by physics, or by a convention
we have not yet challenged?
