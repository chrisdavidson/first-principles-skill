<!-- GENERATED — DO NOT EDIT. Source: shared/examples/estimate-fermi.md. Regenerate via: scripts/sync-content.py --write. -->

# Worked Example: Estimate — Fermi Magnitude Rebuild (Thermal Energy Storage)

A focused demonstration of the **estimate** (Fermi / dimensional-analysis) technique applied to
a science and engineering cost question in the molten-salt thermal energy storage domain —
the same domain used in the decompose example, showing the cross-technique handoff
from Phase 3 (verified primitives) to Phase 4 (quantitative derivation chain).
The drill makes the unit-factor rebuild visible and the explicit lower/upper bracket legible:
the bracket, not the single central value, is the deliverable.

**Target quantity.** Levelised cost of storage (LCOS) for a 5 MWh molten-salt thermal energy
storage (TES) system, in **$/kWh of delivered thermal energy**, rebuilt from constituent
first-principles unit-factors.

**Why this estimate matters.** The decompose example (Phase 3) established ground truths
GT-5 and GT-6: molten-salt TES capital cost ≈ $20–50/kWh installed vs. lithium-ion
≈ $150–300/kWh installed. The estimate drill rebuilds that figure from the underlying
unit-factors, showing *why* those numbers hold and making the uncertainty source explicit.
The bracketed result becomes the Phase 4 quantitative derivation chain step that anchors
the cost-competitiveness conclusion.

---

## Estimate Drill

### Step 1 — Target quantity and units

**Target:** LCOS of molten-salt TES, in **$/kWh** of delivered thermal energy.

The units must be reconstructed as a product of factors whose units cancel to $/kWh.
This is the dimensional analysis constraint that anchors the entire drill.

---

### Step 2 — Unit-factor decomposition

A first-principles unit-factor decomposition of LCOS:

    material_mass     [kg / kWh]           — how much salt per unit of storage
  × cost_per_kg       [$ / kg]             — bulk commodity cost of salt
  × amortisation      [1 / cycles]         — capital cost spread over cycle life
  ────────────────────────────────────────
  = capital_per_kWh   [$ / kWh / cycle]   → $/kWh of delivered energy

**Unit-cancellation check:** kg/kWh × $/kg × 1/cycles = $/(kWh·cycles). Dividing by
cycles amortises across the design life, yielding $/kWh per cycle delivered — the LCOS
capital component. Units cancel correctly. ✓

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

**Factor 3: `amortisation` [1/cycles]**

Molten salt has no electrochemical degradation mechanism at 290–565 °C. Design life is
governed by tank and piping mechanical fatigue, not chemical degradation. Commercial CSP
plants document design lives of 25–30 years at ~365 cycles/year:

- Low estimate: 8,000 cycles (22 years × 365, conservative)
- Central estimate: 10,000 cycles (27 years × 365)
- High estimate: 12,000 cycles (33 years × 365, optimistic)

*Source:* inorganic salt chemistry (physical law: no redox mechanism at these temperatures,
GT-4 domain); commercial CSP plant operating records (direct measurement).

---

### Step 4 — Central magnitude

Using central values:

    capital_per_kWh = material_mass × cost_per_kg × (1 / cycle_life)
                    = 8.6 kg/kWh × $0.60/kg × (1 / 10,000 cycles)
                    = $0.000516 / kWh per cycle

This is salt-material capital only. Commercial LCOS must also include:
- Tank, insulation, piping, and heat-exchanger capital (typically 3–5× salt material cost for
  large-scale plants, based on NREL TES system cost breakdowns)
- Operating and maintenance costs (≈ 1–2% of capital per year for CSP plants)

Incorporating system factor (mid = 4×) and 20-year O&M (~$5/kWh amortised):

    system_capital = salt_capital × 4 = $0.000516 × 4 = $0.00206/kWh/cycle

At 10,000 cycles: **$0.00206 × 10,000 cycles ≈ $20.6/kWh** capital component.
Adding O&M: **central LCOS ≈ $25–35/kWh**.

This is consistent with NREL's published TES LCOS range of $20–50/kWh and confirms
the GT-5 anchor from the decompose example. The unit-factor rebuild explains the range.

---

### Step 5 — Explicit bracket

**Conservative values** (lower bound): low salt cost ($0.40/kg), 12,000-cycle life,
system factor 3.5×, low O&M:

    8.6 × 0.40 × (1/12,000) × 3.5 × 12,000 + O&M(low)
    ≈ $0.00029/kWh × 12,000 × 3.5 + $3/kWh
    ≈ $12.1 + $3 ≈ $15/kWh

**Aggressive values** (upper bound): high salt cost ($0.80/kg), 8,000-cycle life,
system factor 5×, high O&M:

    8.6 × 0.80 × (1/8,000) × 5 × 8,000 + O&M(high)
    ≈ $0.00086/kWh × 8,000 × 5 + $8/kWh
    ≈ $34.4 + $8 ≈ $42/kWh

**Explicit bracket:**

| Bound | LCOS | Dominant driver |
|-------|------|----------------|
| **Lower bound** | ~$15/kWh | Low salt cost, long life, lean install |
| **Central estimate** | ~$30/kWh | Mid-range material cost, 10,000 cycles |
| **Upper bound** | ~$42/kWh | High salt cost, shorter life, full install overhead |

**Decision-resolution check:** The bracket [$15–$42/kWh] vs. utility-scale
lithium-ion [$150–$300/kWh] (GT-6) keeps the cost-competitiveness conclusion stable
across the entire width of the estimate bracket. Molten-salt TES is cost-competitive
under all combinations of factor uncertainty. The estimate is decision-grade.

---

## Phase 4 Handoff — Quantitative Derivation Chain

The unit-factor rebuild and bracketed result enter **Phase 4 (Reason Upward)** as a
quantitative **Derivation Chain**, citing the Phase 3 ground truths (GT-1 through GT-8?
established in the decompose example) that anchor each factor:

**Chain: Molten-Salt TES Cost-Competitiveness**

```
GT-4  (Solar Salt stable 290–565 °C; c_p ≈ 1.52 kJ/kg·°C — direct measurement)
GT-5  (Molten-salt TES capital ≈ $20–50/kWh — NREL direct measurement)
GT-6  (Lithium-ion storage ≈ $150–300/kWh — BloombergNEF direct measurement)
  +
  unit-factor rebuild:
    material_mass [8.6 kg/kWh] × cost_per_kg [$0.40–0.80/kg]
    × amortisation [1/8,000–12,000 cycles] × system_factor [3.5–5×]
  →
  LCOS bracket: [Lower bound: ~$15/kWh | Central: ~$30/kWh | Upper: ~$42/kWh]
  →
  [Conclusion: Molten-salt TES LCOS is cost-competitive with lithium-ion under all
   bracket scenarios. Confidence: HIGH — bracket lower bound ($15/kWh) is still 10×
   below lithium-ion lower bound ($150/kWh); conclusion holds even at upper bound ($42/kWh).]
```

**Cross-technique continuity.** The decompose drill (Phase 3) produced GT-4, which
anchored the Solar Salt specific heat and operating window. The estimate drill (Phase 4)
consumed GT-4 to derive `material_mass`, converting a verified primitive into a
quantitative unit-factor. The Phase 3 → Phase 4 handoff is complete: verified
primitives (decompose output) become the anchored per-unit values the estimate rebuilds
the magnitude from. The derivation chain cites GT-N ids so the connection is traceable.

**Uncertainty carried forward.** The bracket width [$15–$42/kWh] reflects the
uncertainty in salt procurement cost and effective cycle life. The conclusion (cost-
competitive) is rated **HIGH confidence** because even the upper bound is well below
the lithium-ion lower bound. If a future project had a lithium-ion quote of $40/kWh
(emerging cost trajectory), the bracket would straddle the threshold and the
confidence would drop to MEDIUM — at that point, tighten `cost_per_kg` with a
current procurement quote before drawing the conclusion.
