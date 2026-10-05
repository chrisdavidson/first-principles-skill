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
the cost-competitiveness conclusion — and, as Step 6b shows, rebuilding the figure from its
factors is also what exposes that the GT-5/GT-6 comparison, taken at face value, puts a
storage-only price against a whole-system price.

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

**Decision-resolution check — on the storage-only boundary:** on the common electrical basis,
the **installed-only** upper bound (~$83/kWh_e) sits ~1.8× below the lithium-ion lower bound
(150 ÷ 83.5 = 1.80), and the installed-plus-O&M upper bound (~$107/kWh_e) sits ~1.4× below it
(150 ÷ 106.8 = 1.40). **That comparison is not yet like for like, and Step 6b shows it does not
survive.** Dividing by η moves the store's cost onto an electrical basis; it does not buy the
turbine and generator that make electricity out of the stored heat, and GT-6 is the installed
price of a whole battery system that delivers electricity.

> **What this step is doing in a worked example.** The earlier version of this analysis compared
> $34.4/kWh_th directly against $150/kWh_e and reported the conclusion clearing by ~4.4×. That
> number was wrong by the conversion factor: it divided electrical dollars by thermal dollars and
> read the quotient as a margin. The defect is invisible to inspection because both quantities are
> spelled "$/kWh" — which is the whole reason Step 4's unit-cancellation discipline exists, and the
> reason it has to be applied to the *comparison* and not only to the rebuild that feeds it.
### Step 6b — Price the equipment the electrical basis requires (system-boundary check)

A unit check asks whether two quantities are in the same units; a **boundary check** asks whether
they cost the same *scope*. `system_factor` (Step 3) covers the tanks, insulation, foundations,
piping, pumps and the salt-to-steam heat exchanger — the **store**. Storage that returns
electricity also needs the **power block** — the steam turbine, generator and their auxiliaries —
and none of it is in the rebuild. GT-8 prices it at **$1,000–1,200 per kW_e** of turbine capacity.

A per-kW cost becomes a per-kWh cost through the discharge duration `h`:

    power_block_per_kWh_e = power_block_per_kW_e ÷ h      [$/kW_e ÷ h = $/kWh_e]

GT-6 is a utility-scale battery price; taking the common four-hour duration for it (h = 4) —
an assumption, A-8 below — the like-for-like comparison is:

| Installed, per kWh_e | Store (Step 6a) | + power block (÷ 4 h) | **System** | vs lithium-ion $150–300/kWh_e |
|---|---|---|---|---|
| Lower (best case for molten-salt) | ~$29.1 | +$250 | **~$279** | 1.9× above the floor; 0.93× the ceiling |
| Central | ~$50.0 | +$275 | **~$325** | above the whole range |
| Upper | ~$83.5 | +$300 | **~$384** | 2.6× above the floor |

**Decision-resolution check — on the system boundary:** at a four-hour duration, molten-salt TES
is **not** cost-competitive with lithium-ion. Only the most favourable molten-salt case edges under
the most expensive lithium-ion case (279 < 300); every other pairing puts molten-salt above.

**The conclusion now turns on duration, not on η.** The store is cheap per kWh and the power block
is expensive per kW, so the system cost falls as `h` rises. Setting `store + power_block ÷ h`
equal to the lithium-ion price gives the break-even duration `h = power_block ÷ (Li-ion − store)`:
~3.7 h at the most favourable pairing (1,000 ÷ (300 − 29.1)), ~6.3 h at the central values
(1,100 ÷ (225 − 50.0)), and ~18 h at the least favourable (1,200 ÷ (150 − 83.5)). And η no longer
decides anything: even at a physically impossible η = 1 the upper store figure plus the four-hour
power block is ~$34 + $300 = ~$334/kWh_e, still above the $150 floor.

**Two omissions, both in molten-salt's favour, so neither can rescue the old conclusion.** GT-8's
figures are for a 115 MWe reference plant; a 5 MWh store at a four-hour duration drives a turbine
of roughly 0.5 MW_e (5,000 kWh_th × 0.412 ÷ 4 h ≈ 515 kW_e), where cost per kW is higher, not
lower. And the charging heater — the equipment that turns electricity into stored heat — is not
priced here at all. Each only adds cost to the molten-salt side.

> **A second boundary error, corrected here.** The previous version of this example stopped at
> Step 6a and concluded that molten-salt TES is cost-competitive with lithium-ion "once both sides
> are placed on a common electrical basis". The basis conversion was right; the comparison was
> not, because it set a store's cost against a whole system's price. Like the ~4.4× margin before
> it, the defect was invisible to inspection — both figures read "$/kWh_e" — and it was caught by
> re-running the problem on a later agent, which priced the power conversion the example had left
> out.

Amortised over cycle life, the **store** alone reaches ~$0.0014–0.0055/kWh_th delivered — a
measure of how cheap it is to hold heat, not of the cost of delivered electricity, and not compared
against GT-6, which is an installed capital cost. The capital question is resolved at Step 6b: at
the durations lithium-ion is usually bought for, molten-salt storage is dearer; at long durations,
it is cheaper.

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
is electrical. It is carried `?`-marked as **GT-7?** and caps chain C1 at MEDIUM. Once the power block is priced
(Step 6b) it no longer decides the comparison: the conclusion holds at any η.

Two further inputs enter at Step 6b. **GT-8**, the power-block cost, read at source for this
revision. And **A-8, a four-hour discharge duration** for the comparison — the usual duration for a
utility-scale lithium-ion system, taken as the basis on which GT-6's per-kWh price is quoted. A-8 is
the input the conclusion now turns on, which is why Step 6b states the result as a break-even
duration rather than a single verdict. GT-8's reference plant is 115 MWe and this system is about
0.5 MW_e; carrying the large-plant cost is an assumption that favours molten-salt.

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

- **GT-8** The power block of a molten-salt power tower — steam turbine, generator and
  auxiliaries, dry-cooled — costs ≈ $1,000–1,200 per kW_e of gross turbine capacity; the steam
  generation system (salt-to-steam heat exchangers and circulation pumps) is priced separately
  as balance of plant at ≈ $350–365/kW_e — source: NREL, *Molten Salt Power Tower Cost Model for
  the System Advisor Model (SAM)*, Turchi & Heath, NREL/TP-5500-57625 (2013), Table 1 (Tower
  Roadmap and WorleyParsons $1,000/kW; SAM default $1,200/kW; balance of plant $350 and $365/kW),
  for a 115 MWe reference plant with 10 hours of storage (Table 2). Read at source for this
  revision. Only the power block is added in Step 6b: the balance-of-plant line is the salt-to-steam
  exchanger that `system_factor` already includes, and counting it twice would bias the comparison
  against molten-salt.

```text
?-marked: GT-7? (1 of 5)
Read-at-source: none — no chain is rated HIGH
```

---

## 4. Derivation Chains

### Conclusion C1: Molten-salt TES is not cost-competitive with lithium-ion at a four-hour duration once its power block is priced; it becomes competitive only at long durations

GT-4 (Solar Salt stable 290–565 °C; c_p ≈ 1.52 kJ/(kg·°C) — direct measurement) + GT-5 (molten-salt TES installed capital ≈ $20–50/kWh — NREL direct measurement) + GT-6 (lithium-ion storage ≈ $150–300/kWh_e installed — BloombergNEF direct measurement) + GT-7? (thermal-to-electric conversion ≈ 0.412) + GT-8 (power block ≈ $1,000–1,200/kW_e — NREL/TP-5500-57625, read at source)
→ The unit-factor rebuild (material_mass 8.6 kg/kWh × cost_per_kg $0.40–0.80/kg × system_factor 3.5–5×, GT-4-anchored) reconstructs the installed-capital bracket from first principles — Lower ~$12.0/kWh, Central ~$20.6/kWh, Upper ~$34.4/kWh installed, or ~$17/~$28/~$44 per kWh once the separate lifetime O&M reserve of $5–10/kWh is added — overlapping the GT-5 range this rebuild explains rather than merely assumes over $20–$34.4/kWh, with the installed lower bound falling 40% below GT-5's $20/kWh floor. That shortfall is not resolved here: it may mean the lean-system factor values are optimistic, in which case the upper bound is understated in the same direction. The cost-competitiveness conclusion below is binding at the upper bound, not the lower, and only after the Step 6a basis conversion: the rebuilt bracket is $/kWh_th and GT-6 is $/kWh_e, so the installed upper bound converts to ~$83/kWh_e at η ≈ 0.412 and clears GT-6's $150/kWh_e floor by ~1.8×, not by the ~4.4× a direct division of the two unconverted figures reports. If the installed upper bound were itself understated by the same 40% ($34.4 → ~$57/kWh_th → ~$139/kWh_e), the installed-only conclusion would narrow to ~1.1× rather than reverse — it takes a ~44% understatement ($34.4 → ~$62/kWh_th) to cross the floor on that arm. The same 40% applied to the O&M-inclusive upper bound ($44 → ~$73/kWh_th → ~$178/kWh_e) DOES reverse it, so the fragility is real but sits on the wider scope, not the narrower one [Assumes: GT-7? η_th→e ≈ 0.412]
→ Amortising the installed-capital bracket over cycle life (8,000–12,000 cycles) converts one-time capital into levelised cost per kWh delivered — Lower ~$0.0014/kWh, Central ~$0.0028/kWh, Upper ~$0.0055/kWh
→ On the storage-only boundary the installed upper bound converts to ~$83/kWh_e at η ≈ 0.412 and sits ~1.8× below the lithium-ion floor, but that sets the cost of a store against the installed price of a whole battery system, and a store returns no electricity without a power block
→ Adding the power block at a four-hour discharge (A-8), $1,000–1,200/kW_e ÷ 4 h = $250–300/kWh_e, puts the molten-salt system at ~$279 / ~$325 / ~$384 per kWh_e (lower / central / upper) against lithium-ion's $150–300/kWh_e, so only the most favourable molten-salt case edges under the most expensive lithium-ion case [Assumes: A-8 four-hour duration]
→ The system cost falls as duration rises because the store is cheap per kWh and the power block is costly per kW, so the break-even is a duration — ~3.7 h at the most favourable pairing, ~6.3 h at the central values, ~18 h at the least favourable — and the verdict no longer depends on η, since even η = 1 leaves the four-hour upper case at ~$334/kWh_e
→ Molten-salt TES is not cost-competitive with lithium-ion at a four-hour duration, and becomes competitive only at long durations; the large-plant power-block cost and the unpriced charging heater both favour molten-salt, so neither can reverse this [Assumes: A-8 four-hour duration]

**Pre-check:** head GT-4, GT-5, GT-6, GT-7?, GT-8 · ?-marked: GT-7? · lowest cited: none · Inputs ceiling: MEDIUM
**Confidence:** MEDIUM — GT-7? (the thermal-to-electric conversion factor, ≈ 0.412) is carried
rather than read at source here, and a `?`-marked input on the head caps the chain at MEDIUM.
It no longer decides the verdict: once GT-8's power block is priced the four-hour conclusion holds
at any η. What the verdict does turn on is A-8, the four-hour duration — the break-even runs from
~3.7 h to ~18 h — so the conclusion is stated per duration rather than as a single answer.
Verification path: opening OSTI 1035342 Table 2 would move η off `?`; a power-block quotation at
this system's ~0.5 MW_e scale would replace GT-8's large-plant figure, and would move the
break-even durations up, not down.

---

## 5. Abandoned Reasoning

### Dead End: Comparing the store's cost with the battery's installed price

**What was tried:** Converting the rebuilt store cost to an electrical basis (Step 6a) and setting it
directly against lithium-ion's installed price (GT-6), which reports molten-salt ~1.4–1.8× cheaper.

**Why abandoned:** GT-6 is the price of a whole battery system that delivers electricity; the
rebuild prices only the store. The equipment that turns stored heat back into electricity is
missing from one side, and pricing it (GT-8, Step 6b) reverses the four-hour verdict.

**What it ruled out:** Any cost comparison whose two sides do not cover the same equipment —
the boundary check that Step 6b makes explicit.

---

## 6. Conclusion

**Recommended approach:** Per chain C1, treat molten-salt TES as **not** cost-competitive with
lithium-ion for four-hour storage: once the power block is priced the system costs ~$279–384 per
kWh_e against lithium-ion's $150–300. Consider it where the discharge is long — the break-even runs from
~3.7 h to ~18 h — and size the decision on duration rather than on the store's per-kWh cost.

**Key insight:** In chain C1 the store is cheap per kWh and the power block is costly per kW, so
the comparison is decided by discharge duration and by what equipment each price covers — not by
the store's installed cost, which the unit-factor rebuild explains and which was never in doubt.

- The store's bracket (chain C1) reflects the uncertainty in salt-procurement cost, the system
  multiple and the O&M reserve: [$12.0–$34.4/kWh_th] installed, [$17–$44/kWh_th] with the lifetime
  O&M reserve; cycle life additionally drives the levelised spread of holding heat.
- Cross-technique continuity (chain C1): the five-whys reduce-to-primitives drill produced GT-4,
  which anchored the Solar Salt specific heat and operating window that chain C1's `material_mass`
  factor derives from.

**Pre-check:** head C1 (MEDIUM) · ?-marked: none · lowest cited: MEDIUM · Inputs ceiling: MEDIUM
**Confidence:** MEDIUM — matches chain C1, which is capped at MEDIUM by GT-7? (the carried-not-read
thermal-to-electric conversion factor), although the verdict no longer depends on it. The input
that decides the answer is the discharge duration (A-8): the recommendation is stated for four
hours and the break-even is given as a range for the others. A power-block quotation at this
system's scale would sharpen that range, and could only move it toward longer durations.

---

## Appendix — process output

## Structured summary (process output)

```json
{
  "schema_version": 1,
  "run_mode": null,
  "assumptions": [],
  "ground_truths": [
    {
      "id": "GT-4",
      "read_at_source": true
    },
    {
      "id": "GT-5",
      "read_at_source": true
    },
    {
      "id": "GT-6",
      "read_at_source": true
    },
    {
      "id": "GT-7",
      "read_at_source": false
    },
    {
      "id": "GT-8",
      "read_at_source": true
    }
  ],
  "chains": [
    {
      "id": "C1",
      "confidence": "MEDIUM",
      "rests_on": [
        "GT-4",
        "GT-5",
        "GT-6",
        "GT-7?",
        "GT-8"
      ]
    }
  ],
  "dead_ends": [
    "Comparing the store's cost with the battery's installed price"
  ],
  "techniques": null,
  "gate": null,
  "re_entry": null,
  "conclusion": {
    "recommendation": "Per chain C1, treat molten-salt TES as **not** cost-competitive with\nlithium-ion for four-hour storage: once the power block is priced the system costs ~$279–384 per\nkWh_e against lithium-ion's $150–300. Consider it where the discharge is long — the break-even runs from\n~3.7 h to ~18 h — and size the decision on duration rather than on the store's per-kWh cost.",
    "confidence": "MEDIUM",
    "rests_on": [
      "C1"
    ]
  }
}
```
