# Worked Example: Estimate — Fermi Magnitude Rebuild (Thermal Energy Storage)

A focused demonstration of the **estimate** (Fermi / dimensional-analysis) technique applied to
a science and engineering cost question in the molten-salt thermal energy storage domain —
the same domain used in the five-whys (reduce-to-primitives) example, showing the cross-technique handoff
from Phase 3 (verified primitives) to Phase 4 (quantitative derivation chain).
The drill makes the unit-factor rebuild visible and the explicit lower/upper bracket legible:
the bracket, not the single central value, is the deliverable.

**Target quantity.** Installed capital cost of a 5 MWh molten-salt thermal energy storage
(TES) system, in **$/kWh of storage capacity**, rebuilt from constituent first-principles
unit-factors — then amortised over cycle life to a levelised cost per kWh delivered.

**Why this estimate matters.** The five-whys (reduce-to-primitives) example (Phase 3) established ground truths
GT-5 and GT-6: molten-salt TES capital cost ≈ $20–50/kWh installed vs. lithium-ion
≈ $150–300/kWh installed. The estimate drill rebuilds that installed figure from the
underlying unit-factors, showing *why* those numbers hold and making the uncertainty source
explicit, then amortises it over cycle life to show why molten-salt's *levelised* cost is so
low. The bracketed result becomes the Phase 4 quantitative derivation chain step that anchors
the cost-competitiveness conclusion.

---

## Estimate Drill

### Step 1 — Target quantity and units

**Target:** installed capital cost of molten-salt TES, in **$/kWh of storage capacity** (the
GT-5 / GT-6 basis), with a levelised cost per kWh *delivered* derived from it by amortising
over cycle life (Step 6).

The installed cost must be reconstructed as a product of factors whose units cancel to
$/kWh of capacity. This is the dimensional analysis constraint that anchors the entire drill.

---

### Step 2 — Unit-factor decomposition

A first-principles unit-factor decomposition of installed capital cost per kWh of capacity:

    material_mass     [kg / kWh]           — how much salt per unit of storage capacity
  × cost_per_kg       [$ / kg]             — bulk commodity cost of salt
  × system_factor     [dimensionless]      — tank, insulation, piping, heat-exchanger
                                             multiple on bare salt-material cost
  ────────────────────────────────────────
  = capital_per_kWh   [$ / kWh capacity]

**Unit-cancellation check:** kg/kWh × $/kg × (dimensionless) = $/kWh of capacity. Units cancel
correctly to the target's units. ✓

Cycle life does **not** enter this installed-capital product — installation is a one-time build
cost. Cycle life enters separately in Step 6, where the one-time capital is amortised over
delivered energy to a levelised cost; keeping it out of the product here is what stops it from
silently cancelling.

---

### Step 3 — First-principles values for each factor

**Factor 1: `material_mass` [kg/kWh]**

Solar Salt (60% NaNO₃ / 40% KNO₃) has a specific heat capacity of ~1.52 kJ/(kg·°C)
and is operated across a ΔT of 275 °C (290 °C cold tank, 565 °C hot tank).

Stored energy per kg of salt:

    Q/m = c_p × ΔT = 1.52 kJ/(kg·°C) × 275 °C = 418 kJ/kg

Converting to kWh: 418 kJ ÷ 3,600 kJ/kWh ≈ 0.116 kWh/kg

Therefore: `material_mass` = 1 / 0.116 ≈ **8.6 kg/kWh**

*Source:* specific heat capacity from published material data for Solar Salt (direct
measurement, GT-4 domain); ΔT from documented commercial operating window.

*First-principles anchors used:*
- Definition: 1 kWh = 3,600 kJ (unit conversion definition — irreducible)
- Direct measurement: c_p ≈ 1.52 kJ/(kg·°C) for Solar Salt (GT-4 extends here)

**Factor 2: `cost_per_kg` [$/kg]**

Solar Salt is a bulk commodity (mixed nitrate salts). Published engineering procurement
surveys and NREL cost studies (2023) cite a range of **$0.40–0.80/kg**; mid-range ≈ $0.60/kg.

*Source:* direct measurement (NREL engineering cost data, 2023 procurement surveys).

**Factor 3: `system_factor` [dimensionless]**

Bare salt is only part of an installed TES system: the two tanks, insulation, foundations,
piping, pumps, and the salt-to-steam heat exchanger add cost on top of the salt itself. NREL
TES system cost breakdowns put the installed system at roughly **3.5–5× the bare salt-material
cost** for large-scale plants; mid ≈ 4×.

*Source:* NREL TES system cost breakdowns (direct measurement / engineering cost data, 2023).

**Amortisation input: `cycle_life` [cycles]** *(used in Step 6, deliberately not a factor in the installed-capital product)*

Molten salt has no electrochemical degradation mechanism at 290–565 °C. Design life is
governed by tank and piping mechanical fatigue, not chemical degradation. Commercial CSP
plants document design lives of 25–30 years at ~365 cycles/year:

- Low estimate: 8,000 cycles (22 years × 365, conservative)
- Central estimate: 10,000 cycles (27 years × 365)
- High estimate: 12,000 cycles (33 years × 365, optimistic)

*Source:* inorganic salt chemistry (physical law: no redox mechanism at these temperatures,
GT-4 domain); commercial CSP plant operating records (direct measurement). Cycle life is
load-bearing for the *levelised* cost (Step 6), not for the installed capital (Steps 4–5).

---

### Step 4 — Central magnitude (installed capital)

Using central values:

    capital_per_kWh = material_mass × cost_per_kg × system_factor
                    = 8.6 kg/kWh × $0.60/kg × 4
                    = $20.6 / kWh of capacity

This is the installed salt-plus-system capital — the figure directly comparable to GT-5's and
GT-6's installed ranges. A lifetime O&M reserve (≈ $5–10/kWh of capacity over the plant life,
from NREL CSP O&M data) is a separate term, carried here because Step 6's levelised cost needs
it; it is NOT part of any "installed" comparison:

    installed capital           ≈ $20.6/kWh          (comparable to GT-5, GT-6)
    installed + lifetime O&M    ≈ $25.6–30.6/kWh     (the Step 6 amortisation basis, ~$28/kWh)

The installed-only figure sits inside NREL's published TES installed-cost range of $20–50/kWh and
confirms the GT-5 anchor from the five-whys (reduce-to-primitives) example. The unit-factor rebuild
explains the range.

---

### Step 5 — Explicit bracket (installed capital)

**Conservative values** (lower bound): low salt cost ($0.40/kg), lean system (3.5×), low O&M:

    8.6 × 0.40 × 3.5  =  $12.0/kWh  +  O&M(low ≈ $5)   ≈  $17/kWh

**Aggressive values** (upper bound): high salt cost ($0.80/kg), full system (5×), high O&M:

    8.6 × 0.80 × 5.0  =  $34.4/kWh  +  O&M(high ≈ $10) ≈  $44/kWh

Every factor in the bracket is load-bearing — there is no canceling term. The spread is driven
by salt-procurement cost, the system multiple, and the O&M reserve.

**Explicit bracket (installed capital, with and without the lifetime O&M reserve):**

| Bound | Installed capital | Installed + lifetime O&M | Dominant driver |
|-------|-------------------|--------------------------|-----------------|
| **Lower bound** | ~$12.0/kWh | ~$17/kWh | Low salt cost, lean 3.5× system, low O&M ($5) |
| **Central estimate** | ~$20.6/kWh | ~$28/kWh | Mid salt cost ($0.60/kg), 4× system, mid O&M ($7.5) |
| **Upper bound** | ~$34.4/kWh | ~$44/kWh | High salt cost, full 5× system, high O&M ($10) |

Only the **Installed capital** column is like-for-like with GT-5's and GT-6's installed ranges.
The **Installed + lifetime O&M** column is the Step 6 amortisation basis and carries a scope those
cited sources do not.

---

### Step 6 — Amortise to levelised cost (cycle life enters here)

Installed capital is a one-time cost; the **levelised cost per kWh *delivered*** divides it
across the energy the system delivers over its life — one capacity-kWh delivered per cycle:

    LCOS = installed_capital / cycle_life     [$/kWh capacity ÷ cycles = $/kWh delivered]

Cycle life is load-bearing here, and it pairs with the installed bound: the cheapest installs
are mature, low-stress designs that also run longest, so the bounds compound. Unlike Steps 4–5,
the cycle term does **not** cancel — it is the divisor that converts one-time capital into cost
per delivered kWh.

| Bound | Installed + lifetime O&M | Cycle life | Levelised cost |
|-------|-------------------------|-----------|----------------|
| **Lower** | ~$17/kWh | 12,000 cycles | ~$0.0014/kWh delivered |
| **Central** | ~$28/kWh | 10,000 cycles | ~$0.0028/kWh delivered |
| **Upper** | ~$44/kWh | 8,000 cycles | ~$0.0055/kWh delivered |

The ~4× spread in levelised cost is driven jointly by installed capital and cycle life.

**Decision-resolution check:** Like for like, the **installed-only** bracket [$12.0–$34.4/kWh] vs.
utility-scale lithium-ion [$150–$300/kWh] installed (GT-6) keeps the cost-competitiveness
conclusion stable across the entire width of the estimate bracket — even the installed upper bound
($34.4/kWh) is ~4.4× below the lithium-ion lower bound (150 ÷ 34.4 = 4.4). Adding the lifetime
O&M reserve to the molten-salt side — a scope GT-6's installed figure does not carry — still
leaves that upper bound ~3.4× below it (150 ÷ 44 = 3.4). Both arms clear the threshold, so the
conclusion does not turn on which scope is used.
Amortised, the gap only widens: molten-salt's long cycle
life drives its levelised cost to ~$0.0014–0.0055/kWh delivered. Molten-salt TES is
cost-competitive under all combinations of factor uncertainty. The estimate is decision-grade.

---

## 1. Problem Essence

**Target quantity.** Installed capital cost of a 5 MWh molten-salt thermal energy storage
(TES) system, in $/kWh of storage capacity, rebuilt from constituent first-principles
unit-factors — then amortised over cycle life to a levelised cost per kWh delivered.

The unit-factor rebuild (Steps 2–5 above) makes explicit *why* the GT-5/GT-6 installed-cost
figures hold, rather than treating them as an unexplained given, and the amortisation
(Step 6) converts the one-time installed-capital bracket into the levelised figure the
cost-competitiveness question actually turns on.

---

## 2. Assumptions Table

Nothing material here — this is a single-technique Fermi-estimation drill rebuilding an
installed-cost figure from unit-factors; it consumes ground truths already classified and
verified in the five-whys (reduce-to-primitives) example it hands off from (Step 3 above)
and introduces no new untested belief of its own to classify.

---

## 3. Ground Truths

- **GT-4** Solar Salt (60% NaNO₃ / 40% KNO₃) has a specific heat capacity of ~1.52 kJ/(kg·°C)
  and is stable across the 290–565 °C commercial operating window — source: published
  material data for Solar Salt (direct measurement), established in the five-whys
  (reduce-to-primitives) example this drill hands off from.

- **GT-5** Molten-salt TES installed capital cost is ≈ $20–50/kWh installed — source: NREL
  direct measurement, established in the five-whys (reduce-to-primitives) example.

- **GT-6** Utility-scale lithium-ion storage installed capital cost is ≈ $150–300/kWh
  installed — source: BloombergNEF direct measurement, established in the five-whys
  (reduce-to-primitives) example.

---

## 4. Derivation Chains

### Conclusion C1: Molten-salt TES is cost-competitive with lithium-ion under all bracket scenarios

GT-4 (Solar Salt stable 290–565 °C; c_p ≈ 1.52 kJ/(kg·°C) — direct measurement) + GT-5 (molten-salt TES installed capital ≈ $20–50/kWh — NREL direct measurement) + GT-6 (lithium-ion storage ≈ $150–300/kWh installed — BloombergNEF direct measurement)
→ The unit-factor rebuild (material_mass 8.6 kg/kWh × cost_per_kg $0.40–0.80/kg × system_factor 3.5–5×, plus an O&M reserve of $5–10/kWh, GT-4-anchored) reconstructs the installed-capital bracket from first principles — Lower ~$17/kWh, Central ~$28/kWh, Upper ~$44/kWh — overlapping the GT-5 range this rebuild explains rather than merely assumes, with the lower bound falling below GT-5's $20/kWh floor; that direction is conservative for the cost-competitiveness conclusion below, since a lower installed-cost estimate only widens the margin against lithium-ion's $150/kWh floor (GT-6)
→ Amortising the installed-capital bracket over cycle life (8,000–12,000 cycles) converts one-time capital into levelised cost per kWh delivered — Lower ~$0.0014/kWh, Central ~$0.0028/kWh, Upper ~$0.0055/kWh
→ Molten-salt TES is cost-competitive with lithium-ion (GT-6) under every combination of factor uncertainty in the bracket — on the like-for-like installed-only comparison the upper bound ($34.4/kWh) is ~4.4× below the lithium-ion installed lower bound ($150/kWh), and adding the lifetime O&M reserve to the molten-salt side alone still leaves it ~3.4× below ($44/kWh vs $150/kWh); the levelised gap is larger still.

**Confidence:** HIGH — the installed upper bound is well below the lithium-ion installed
lower bound across the full width of the estimate bracket. If a future lithium-ion installed
quote reached ~$40/kWh (emerging cost trajectory), the two would nearly meet — $34.4/kWh
installed, $44/kWh once the lifetime O&M reserve is added, so the O&M-inclusive band would
straddle that threshold — and confidence would drop to MEDIUM. At that point, tighten `cost_per_kg`, the
`system_factor`, and the O&M reserve with current procurement and engineering quotes before
drawing the conclusion.

---

## 5. Abandoned Reasoning

Nothing material here — the unit-factor decomposition (Step 2) was the only rebuild path
considered; the factor set (material_mass, cost_per_kg, system_factor) is the standard
installed-cost decomposition for tank-based thermal storage and no competing decomposition
was tried and discarded.

---

## 6. Conclusion

**Recommended approach:** Treat the molten-salt TES installed-cost figure (chain C1) as
decision-grade for the cost-competitiveness question — the rebuilt installed-only bracket
[$12.0–$34.4/kWh], and the [$17–$44/kWh] band that adds the lifetime O&M reserve,
both hold under every combination of factor uncertainty, so no further estimate refinement is
required before comparing against lithium-ion.

**Key insight:** The unit-factor rebuild (chain C1) explains *why* the GT-5 installed-cost
range holds rather than treating it as an unexplained given, and the amortisation over cycle
life (8,000–12,000 cycles) shows that molten-salt's long cycle life widens the
cost-competitiveness gap further at the levelised-cost level than at the installed-capital
level alone.

- The bracket width (chain C1) reflects the uncertainty in
  salt-procurement cost, the system multiple, and the O&M reserve: [$12.0–$34.4/kWh] installed,
  [$17–$44/kWh] once the lifetime O&M reserve is added; cycle life additionally
  drives the levelised spread.
- Cross-technique continuity (chain C1): the five-whys reduce-to-primitives drill produced
  GT-4, which anchored the Solar Salt specific heat and operating window that chain C1's
  `material_mass` factor derives from.

**Confidence:** HIGH — matches chain C1. Raising the bracket's precision further would
require tightening `cost_per_kg`, the `system_factor`, and the O&M reserve with current
procurement and engineering quotes, but the cost-competitiveness conclusion itself does not
depend on that tightening.
