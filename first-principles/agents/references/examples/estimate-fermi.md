<!-- GENERATED — DO NOT EDIT. Source: shared/examples/estimate-fermi.md. Regenerate via: scripts/sync-content.py --write. -->

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

This is the installed salt-plus-system capital. Adding an O&M reserve (≈ $5–10/kWh of capacity
over the plant life, from NREL CSP O&M data):

    central installed capital ≈ $25–35/kWh of capacity (take ~$30/kWh)

This is consistent with NREL's published TES installed-cost range of $20–50/kWh and confirms
the GT-5 anchor from the five-whys (reduce-to-primitives) example. The unit-factor rebuild explains the range.

---

### Step 5 — Explicit bracket (installed capital)

**Conservative values** (lower bound): low salt cost ($0.40/kg), lean system (3.5×), low O&M:

    8.6 × 0.40 × 3.5  =  $12.0/kWh  +  O&M(low ≈ $3)   ≈  $15/kWh

**Aggressive values** (upper bound): high salt cost ($0.80/kg), full system (5×), high O&M:

    8.6 × 0.80 × 5.0  =  $34.4/kWh  +  O&M(high ≈ $8)  ≈  $42/kWh

Every factor in the bracket is load-bearing — there is no canceling term. The spread is driven
by salt-procurement cost, the system multiple, and the O&M reserve.

**Explicit bracket (installed capital):**

| Bound | Installed capital | Dominant driver |
|-------|-------------------|-----------------|
| **Lower bound** | ~$15/kWh | Low salt cost, lean 3.5× system, low O&M |
| **Central estimate** | ~$30/kWh | Mid salt cost ($0.60/kg), 4× system |
| **Upper bound** | ~$42/kWh | High salt cost, full 5× system, high O&M |

---

### Step 6 — Amortise to levelised cost (cycle life enters here)

Installed capital is a one-time cost; the **levelised cost per kWh *delivered*** divides it
across the energy the system delivers over its life — one capacity-kWh delivered per cycle:

    LCOS = installed_capital / cycle_life     [$/kWh capacity ÷ cycles = $/kWh delivered]

Cycle life is load-bearing here, and it pairs with the installed bound: the cheapest installs
are mature, low-stress designs that also run longest, so the bounds compound. Unlike Steps 4–5,
the cycle term does **not** cancel — it is the divisor that converts one-time capital into cost
per delivered kWh.

| Bound | Installed | Cycle life | Levelised cost |
|-------|-----------|-----------|----------------|
| **Lower** | ~$15/kWh | 12,000 cycles | ~$0.0013/kWh delivered |
| **Central** | ~$30/kWh | 10,000 cycles | ~$0.0030/kWh delivered |
| **Upper** | ~$42/kWh | 8,000 cycles | ~$0.0053/kWh delivered |

The ~4× spread in levelised cost is driven jointly by installed capital and cycle life.

**Decision-resolution check:** The installed-capital bracket [$15–$42/kWh] vs. utility-scale
lithium-ion [$150–$300/kWh] installed (GT-6) keeps the cost-competitiveness conclusion stable
across the entire width of the estimate bracket — even the upper bound ($42/kWh) is ~3.5×
below the lithium-ion lower bound. Amortised, the gap only widens: molten-salt's long cycle
life drives its levelised cost to ~$0.001–0.005/kWh delivered. Molten-salt TES is
cost-competitive under all combinations of factor uncertainty. The estimate is decision-grade.

---

## Phase 4 Handoff — Quantitative Derivation Chain

The unit-factor rebuild and bracketed result enter **Phase 4 (Reason Upward)** as a
quantitative **Derivation Chain**, citing the Phase 3 ground truths (GT-1 through GT-8
established in the five-whys (reduce-to-primitives) example) that anchor each factor:

**Chain: Molten-Salt TES Cost-Competitiveness**

```text
GT-4  (Solar Salt stable 290–565 °C; c_p ≈ 1.52 kJ/kg·°C — direct measurement)
GT-5  (Molten-salt TES installed capital ≈ $20–50/kWh — NREL direct measurement)
GT-6  (Lithium-ion storage ≈ $150–300/kWh installed — BloombergNEF direct measurement)
  +
  unit-factor rebuild (installed capital):
    material_mass [8.6 kg/kWh] × cost_per_kg [$0.40–0.80/kg] × system_factor [3.5–5×]
  →
  installed-capital bracket: [Lower: ~$15/kWh | Central: ~$30/kWh | Upper: ~$42/kWh]
  →  amortise over cycle_life [8,000–12,000 cycles]
  →  levelised cost: [~$0.0013 | ~$0.0030 | ~$0.0053  /kWh delivered]
  →
  [Conclusion: Molten-salt TES is cost-competitive with lithium-ion under all bracket
   scenarios. Confidence: HIGH — installed upper bound ($42/kWh) is still ~3.5× below the
   lithium-ion installed lower bound ($150/kWh), and the levelised gap is larger still.]
```

**Cross-technique continuity.** The five-whys reduce-to-primitives drill (Phase 3) produced GT-4, which
anchored the Solar Salt specific heat and operating window. The estimate drill (Phase 4)
consumed GT-4 to derive `material_mass`, converting a verified primitive into a
quantitative unit-factor. The Phase 3 → Phase 4 handoff is complete: verified
primitives (five-whys reduce-to-primitives output) become the anchored per-unit values the estimate rebuilds
the magnitude from. The derivation chain cites GT-N ids so the connection is traceable.

**Uncertainty carried forward.** The installed bracket width [$15–$42/kWh] reflects the
uncertainty in salt-procurement cost and the system multiple; cycle life additionally drives
the levelised spread (Step 6). The conclusion (cost-competitive) is rated **HIGH confidence**
because even the installed upper bound is well below the lithium-ion installed lower bound. If
a future lithium-ion installed quote reached ~$40/kWh (emerging cost trajectory), the installed
brackets would straddle the threshold and confidence would drop to MEDIUM — at that point,
tighten `cost_per_kg` and the `system_factor` with current procurement and engineering quotes
before drawing the conclusion.
