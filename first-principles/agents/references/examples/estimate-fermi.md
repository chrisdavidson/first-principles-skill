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
plants document design lives of 25–30 years at ~365 cycles/year — approximately 9,100–11,000
cycles (25 × 365 = 9,125; 30 × 365 = 10,950). The bracket below widens that in both directions
to cover early-retirement and life-extension cases the design-life figure does not model; the
widening is a judgement, not a reading of the cited source:

- Low estimate: 8,000 cycles (22 years × 365 — below documented design life, early retirement)
- Central estimate: 10,000 cycles (27 years × 365 — inside the documented range)
- High estimate: 12,000 cycles (33 years × 365 — above documented design life, life extension)

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

Only the **Installed capital** column is like-for-like with GT-5's installed range. The
**Installed + lifetime O&M** column is the Step 6 amortisation basis and carries a scope that
cited source does not.

**GT-6 is not on this basis at all, and the difference is load-bearing.** Every figure in this
table is dollars per kWh of *thermal* capacity — the whole rebuild runs from a heat capacity in
kJ/(kg·°C), so its kWh is a kWh of stored heat (kWh_th). GT-6's lithium-ion figure is dollars per
kWh of *electrical* capacity (kWh_e). Those are different units that share a name, and dividing
one by the other produces a ratio with no physical meaning. Step 6a converts before comparing.

---

### Step 6 — Amortise to levelised cost (cycle life enters here)

Installed capital is a one-time cost; the **levelised cost per kWh *delivered*** divides it
across the energy the system delivers over its life — one capacity-kWh delivered per cycle:

    LCOS = installed_capital / cycle_life     [$/kWh capacity ÷ cycles = $/kWh delivered]

Cycle life is load-bearing here. The table below pairs the cheapest install with the longest life
and the dearest with the shortest — an assumption, not a measurement: it presumes lean, mature
designs also run longest. Nothing in this drill verifies that correlation; the opposite pairing
would narrow the levelised spread to roughly 1.7× rather than the ~4× shown. The conclusion below
does not depend on which pairing holds: the comparison against GT-6 is settled on installed
capital at Step 6a, on a converted basis, not on the levelised column at all.
Unlike Steps 4–5,
the cycle term does **not** cancel — it is the divisor that converts one-time capital into cost
per delivered kWh.

| Bound | Installed + lifetime O&M | Cycle life | Levelised cost |
|-------|-------------------------|-----------|----------------|
| **Lower** | ~$17/kWh | 12,000 cycles | ~$0.0014/kWh delivered |
| **Central** | ~$28/kWh | 10,000 cycles | ~$0.0028/kWh delivered |
| **Upper** | ~$44/kWh | 8,000 cycles | ~$0.0055/kWh delivered |

The ~4× spread in levelised cost is driven jointly by installed capital and cycle life.

### Step 6a — Convert to a common basis before comparing (unit check)

The molten-salt bracket is $/kWh_th; GT-6 is $/kWh_e. To compare them, one side must be moved onto
the other's basis. Storage that exists to return **electricity** is paid for in electricity, so the
thermal figures convert to a delivered-electrical basis through the heat-to-power efficiency:

    cost_per_kWh_e = cost_per_kWh_th ÷ η_th→e     [$/kWh_th ÷ (kWh_e/kWh_th) = $/kWh_e]

η_th→e ≈ **0.412** for a steam cycle at these salt temperatures — the design-point gross cycle
efficiency for 565 °C subcritical molten-salt tower technology with an air-cooled condenser, which
the companion Carnot worked example carries as its GT-6 from Sandia's design characterization
(OSTI 1035342, Table 2). Two choices in that sentence are deliberate and are what make the
conversion defensible rather than convenient:

- **Design-point, not measured.** GT-6 here is lithium-ion *installed capacity* in $/kWh_e, so this
  is a nameplate-to-nameplate conversion, and installed electrical capacity is defined at the design
  point. The only *measured* figure at these reservoir conditions is 34.1% at Solar Two
  (OSTI 793226, §5.3.2), which is the right factor for a *delivered-energy* comparison and the wrong
  one here.
- **Dry-cooled, not wet.** 41.2% air-cooled is the lower end of the design bracket (43.0% wet), and
  it is the figure NREL's Annual Technology Baseline carries as the representative commercial power
  tower. Taking the low end makes this analysis's own conclusion *harder* to reach, which is the
  direction a sensitive assumption should be pushed.

**This factor is still carried rather than established here** — this drill does not open
OSTI 1035342; it takes the figure from the companion example that did. That is exactly what the `?`
in GT-7? records, and the conclusion is sensitive to it, which is why it is named rather than folded
silently into a ratio.

| Basis | Installed-only upper | Installed + O&M upper |
|---|---|---|
| Thermal (as rebuilt) | ~$34.4/kWh_th | ~$44/kWh_th |
| **Electrical (÷ 0.412)** | **~$83/kWh_e** | **~$107/kWh_e** |

**Decision-resolution check:** on the common electrical basis, the **installed-only** upper bound
(~$83/kWh_e) sits ~1.8× below the lithium-ion lower bound (150 ÷ 83.5 = 1.80), and the
installed-plus-O&M upper bound (~$107/kWh_e) sits ~1.4× below it (150 ÷ 106.8 = 1.40). The
cost-competitiveness conclusion survives at both scopes, and the conversion factor still dominates
the margin rather than the capital rebuild: at η ≈ 0.29 the installed-plus-O&M arm crosses
$150/kWh_e and the conclusion reverses. **That reversal threshold does not depend on which
efficiency is chosen** — it is 44 ÷ 150 = 0.293 either way — so re-anchoring the factor widened the
margin without moving the point at which the conclusion breaks.

> **What this step is doing in a worked example.** The earlier version of this analysis compared
> $34.4/kWh_th directly against $150/kWh_e and reported the conclusion clearing by ~4.4×. That
> number was wrong by the conversion factor: it divided electrical dollars by thermal dollars and
> read the quotient as a margin. The defect is invisible to inspection because both quantities are
> spelled "$/kWh" — which is the whole reason Step 4's unit-cancellation discipline exists, and the
> reason it has to be applied to the *comparison* and not only to the rebuild that feeds it.
Amortised, the gap widens on the thermal basis: molten-salt's long cycle
life drives its levelised cost to ~$0.0014–0.0055/kWh_th delivered. That column is not compared
against GT-6 — GT-6 states an installed capital cost, not a levelised one, and the decision is
resolved at Step 6a on installed capital with the basis conversion applied. Molten-salt TES is
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

The GT-4/GT-5/GT-6 anchors are consumed unchanged from the five-whys (reduce-to-primitives)
example this drill hands off from (Step 3 above). Three inputs are NEW to this drill and are not
covered by any ground truth above: `cost_per_kg` ($0.40–0.80/kg), `system_factor` (3.5–5×) and the
lifetime O&M reserve ($5–10/kWh). Each is cited to NREL engineering cost data (Step 3, Step 4) and
each is carried as a range rather than a point precisely because none is verified here; together
they are what the Step 5 bracket's width measures.

A fourth input is new and is of a different kind: **GT-7? — the thermal-to-electric conversion factor (≈ 0.412)**, introduced at Step 6a. The first three set the *width* of the capital bracket; GT-7? sets
whether the comparison against GT-6 is meaningful at all, because GT-5's kWh is thermal and GT-6's
is electrical. It is carried `?`-marked as **GT-7?**, it caps chain C1 at MEDIUM, and it is the one input whose
refinement would change the decision — the sensitivity named on C1's `**Confidence:**` line is
η ≈ 0.29, not a movement in any capital factor.

---

## 3. Ground Truths

- **GT-4** Solar Salt (60% NaNO₃ / 40% KNO₃) has a specific heat capacity of ~1.52 kJ/(kg·°C)
  and is stable across the 290–565 °C commercial operating window — source: published
  material data for Solar Salt (direct measurement), established in the five-whys
  (reduce-to-primitives) example this drill hands off from.

- **GT-5** Molten-salt TES installed capital cost is ≈ $20–50/kWh installed — source: NREL
  direct measurement, established in the five-whys (reduce-to-primitives) example.

- **GT-6** Utility-scale lithium-ion storage installed capital cost is ≈ $150–300/kWh
  **electrical** installed — source: BloombergNEF direct measurement, established in the
  five-whys (reduce-to-primitives) example. The basis is electrical; GT-5's is thermal.

- **GT-7?** Thermal-to-electric conversion efficiency for a steam cycle at this salt's
  temperatures is ≈ 0.412 — **unverified in this drill**. Carried from the companion Carnot
  worked example's GT-6, the design-point gross cycle efficiency for 565 °C subcritical
  molten-salt tower technology with an air-cooled condenser (43.0% wet-cooled, 41.2%
  air-cooled), which that example sources to Sandia's design characterization (OSTI 1035342,
  Table 2). The air-cooled end is taken because it is the lower of the two and because NREL's
  Annual Technology Baseline carries it as the representative commercial power tower. It is
  `?`-marked because this drill does not open that source — it carries the figure from the
  companion example that did — and because the conclusion's margin turns on it. Not to be
  confused with two neighbouring figures in the same companion example: its law-permitted
  Carnot ceiling (~61–62%), which no real cycle reaches, and the single *measured* figure at
  these reservoir conditions (34.1% at Solar Two, OSTI 793226 §5.3.2), which is the right
  factor for a delivered-energy comparison and the wrong one for the nameplate-to-nameplate
  conversion this drill performs against GT-6's installed capacity.

---

## 4. Derivation Chains

### Conclusion C1: Molten-salt TES is cost-competitive with lithium-ion once both sides are on a common electrical basis

GT-4 (Solar Salt stable 290–565 °C; c_p ≈ 1.52 kJ/(kg·°C) — direct measurement) + GT-5 (molten-salt TES installed capital ≈ $20–50/kWh — NREL direct measurement) + GT-6 (lithium-ion storage ≈ $150–300/kWh_e installed — BloombergNEF direct measurement) + GT-7? (thermal-to-electric conversion ≈ 0.412)
→ The unit-factor rebuild (material_mass 8.6 kg/kWh × cost_per_kg $0.40–0.80/kg × system_factor 3.5–5×, GT-4-anchored) reconstructs the installed-capital bracket from first principles — Lower ~$12.0/kWh, Central ~$20.6/kWh, Upper ~$34.4/kWh installed, or ~$17/~$28/~$44 per kWh once the separate lifetime O&M reserve of $5–10/kWh is added — overlapping the GT-5 range this rebuild explains rather than merely assumes over $20–$34.4/kWh, with the installed lower bound falling 40% below GT-5's $20/kWh floor. That shortfall is not resolved here: it may mean the lean-system factor values are optimistic, in which case the upper bound is understated in the same direction. The cost-competitiveness conclusion below is binding at the upper bound, not the lower, and only after the Step 6a basis conversion: the rebuilt bracket is $/kWh_th and GT-6 is $/kWh_e, so the installed upper bound converts to ~$83/kWh_e at η ≈ 0.412 and clears GT-6's $150/kWh_e floor by ~1.8×, not by the ~4.4× a direct division of the two unconverted figures reports. If the installed upper bound were itself understated by the same 40% ($34.4 → ~$57/kWh_th → ~$139/kWh_e), the installed-only conclusion would narrow to ~1.1× rather than reverse — it takes a ~44% understatement ($34.4 → ~$62/kWh_th) to cross the floor on that arm. The same 40% applied to the O&M-inclusive upper bound ($44 → ~$73/kWh_th → ~$178/kWh_e) DOES reverse it, so the fragility is real but sits on the wider scope, not the narrower one [Assumes: GT-7? η_th→e ≈ 0.412]
→ Amortising the installed-capital bracket over cycle life (8,000–12,000 cycles) converts one-time capital into levelised cost per kWh delivered — Lower ~$0.0014/kWh, Central ~$0.0028/kWh, Upper ~$0.0055/kWh
→ Molten-salt TES is cost-competitive with lithium-ion (GT-6) across the rebuilt bracket once both sides are placed on a common electrical basis — the installed-only upper bound converts to ~$83/kWh_e and sits ~1.8× below the lithium-ion installed lower bound ($150/kWh_e), and adding the lifetime O&M reserve leaves it ~$107/kWh_e, ~1.4× below; the margin is dominated by the carried η_th→e ≈ 0.412 rather than by the capital rebuild, and the reversal threshold on the wider scope (η ≈ 0.29) is set by the cost figures alone and so is unchanged by the choice of efficiency [Assumes: GT-7? η_th→e ≈ 0.412].

**Pre-check:** head GT-4, GT-5, GT-6, GT-7? · ?-marked: GT-7? · lowest cited: none · Inputs ceiling: MEDIUM

**Confidence:** MEDIUM — GT-7? (the thermal-to-electric conversion factor, ≈ 0.412) is carried
rather than read at source here, and after the Step 6a basis conversion the conclusion rests on it
rather than on the capital rebuild. On the common electrical basis the installed-only upper bound
(~$83/kWh_e) clears the lithium-ion floor by ~1.8× and the O&M-inclusive upper bound (~$107/kWh_e)
by ~1.4×; at η ≈ 0.29 the second arm crosses $150/kWh_e and the conclusion reverses. The ceiling is
MEDIUM because a `?`-marked input sits on the head, and the band stays there because the wider
scope's margin is still thin enough for a single input to decide it. Verification path: opening
OSTI 1035342 Table 2 in this analysis, or a measured or quoted efficiency for the specific power
block, either of which would move η off `?` and re-open HIGH if the margin held. The earlier HIGH on
this line was read against a ~4.4× margin that a basis error had manufactured; this is the same
conclusion at its real width, not a new finding.

---

## 5. Abandoned Reasoning

Nothing material here — the unit-factor decomposition (Step 2) was the only rebuild path
considered; the factor set (material_mass, cost_per_kg, system_factor) is the standard
installed-cost decomposition for tank-based thermal storage and no competing decomposition
was tried and discarded.

---

## 6. Conclusion

**Recommended approach:** Treat the molten-salt TES installed-cost rebuild (chain C1) as
decision-grade for the *capital* question — the rebuilt installed-only bracket
[$12.0–$34.4/kWh_th], and the [$17–$44/kWh_th] band that adds the lifetime O&M reserve, both hold
under every combination of factor uncertainty. Do **not** treat the comparison against lithium-ion
as settled at the same confidence: that comparison runs through the Step 6a basis conversion, and
its margin is ~1.4× at the O&M-inclusive scope, with the reversal threshold at η ≈ 0.29. Before
committing, either read the design-point efficiency at source (OSTI 1035342, Table 2) or obtain a
measured efficiency for the specific power block; further refinement of the capital factors would
not move the decision, and refinement of η would.

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

**Pre-check:** head C1 (MEDIUM) · ?-marked: none · lowest cited: MEDIUM · Inputs ceiling: MEDIUM

**Confidence:** MEDIUM — matches chain C1, which is capped at MEDIUM by GT-7? (the carried-not-read
thermal-to-electric conversion factor). Raising the bracket's precision further would require
tightening `cost_per_kg`, the `system_factor`, and the O&M reserve with current procurement and
engineering quotes — but that is not what the conclusion now turns on, so it would not raise this
band. The verification that would is reading the design-point efficiency at source (OSTI 1035342,
Table 2) or obtaining a measured efficiency for the specific power block.
