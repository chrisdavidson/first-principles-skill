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

## 1. Problem Essence

**Target:** the thermal-to-electric conversion efficiency of the Rankine-cycle heat engine
operating across the molten-salt reservoir temperature pair — the same 290–565 °C window
established in the five-whys (reduce-to-primitives) example as GT-4. The question: how far
below the law-permitted ceiling is current practice?

Given the reservoir temperatures the five-whys reduce-to-primitives pass established as
ground truths, what does the Second Law permit for the heat engine operating between them?
The ceiling-vs-convention bracket reveals whether the efficiency headroom is real or
illusory.

---

## 2. Assumptions Table

Nothing material here — this is a single-technique physical-bound derivation consuming a
ground truth already classified and verified in the five-whys (reduce-to-primitives)
example (GT-4, Step 2 above); it introduces no new untested belief of its own to classify.

---

## 3. Ground Truths

- **GT-4** Solar Salt (60% NaNO₃ / 40% KNO₃) is stable across the 290–565 °C commercial
  operating window, giving reservoir temperatures T_cold ≈ 563 K and T_hot ≈ 838 K — source:
  published material data for Solar Salt (direct measurement), established in the five-whys
  (reduce-to-primitives) example this drill hands off from.

---

## 4. Derivation Chains

### Conclusion C1: The conventional 20–25% Rankine efficiency is engineering headroom, not a physical ceiling

GT-4 (Solar Salt stable 290–565 °C; T_cold ≈ 563 K, T_hot ≈ 838 K — direct measurement, established in the five-whys reduce-to-primitives example)
→ The Second Law of Thermodynamics' Carnot bound (η = 1 − T_cold/T_hot) applied to the GT-4 reservoir temperatures yields a law-permitted ceiling of η_Carnot = 1 − 563/838 ≈ 33% — the highest thermal-to-electric conversion efficiency any heat engine operating between these reservoirs can achieve, independent of working fluid, cycle design, or engineering refinement
→ The conventional figure for a real Rankine cycle at these reservoir conditions is ~20–25%, so the bracketed gap between the law-permitted ceiling and current practice is ~8–13 percentage points
→ The ~8–13 point gap is engineering headroom, not a physical barrier — it is governed by turbine isentropic losses (~4–5 points), heat-exchanger ΔT losses (~2–3 points), and parasitic loads (~1–2 points), none of which the Carnot bound itself forbids closing.

**Confidence:** HIGH — the Carnot ceiling is irreducible; the conventional figure is anchored
in published turbine operating data for this temperature range.

---

## 5. Abandoned Reasoning

Nothing material here — the Carnot bound is the only governing law applicable to a heat
engine operating between two fixed thermal reservoirs; no competing physical-bound
derivation was tried and discarded.

---

## 6. Conclusion

**Recommended approach:** Treat the ~8–13 percentage-point gap (chain C1) as recoverable
engineering headroom rather than an acceptable ceiling — prioritise turbine isentropic
efficiency, heat-exchanger ΔT reduction, and parasitic-load reduction, in that order of
gap-share, before treating 20–25% as the practical limit for this reservoir pair.

**Key insight:** The Carnot bound (chain C1) reveals that the conventional 20–25% figure is
not near a physical ceiling — the laws permit ~33% for these reservoir temperatures, so the
real question is whether the gap is a recoverable engineering opportunity or a permanently
foregone constraint, not whether 20–25% is "good enough."

- Cross-technique continuity (chain C1): the five-whys reduce-to-primitives drill
  established GT-4 — the Solar Salt temperature window — which chain C1's Carnot-bound
  derivation consumes directly, the same ground truth the estimate drill's chain also
  anchors to.
- The irreducible fraction of the gap is zero (chain C1): the Carnot bound is a ceiling, not
  a floor, and no physical law prevents approaching it, though a finite-power machine never
  reaches it in finite time.

**Confidence:** HIGH — matches chain C1. The Carnot ceiling is irreducible; the conventional
figure is anchored in published turbine operating data for this temperature range.
