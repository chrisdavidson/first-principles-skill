<!-- GENERATED — DO NOT EDIT. Source: shared/examples/theoretical-limit-carnot.md. Regenerate via: scripts/sync-content.py --write. -->

# Worked Example: Theoretical Limit — Carnot Constraint-Relaxation (Thermal Energy Storage)

A focused demonstration of the **theoretical-limit** (constraint relaxation / physical-bound
derivation) technique applied to the same molten-salt thermal energy storage domain used in
the five-whys (reduce-to-primitives) and estimate examples — showing the cross-technique handoff from Phase 3
(verified primitives) and Phase 4 (quantitative derivation chain) to the physical-bound step.
The drill makes the constraint-relaxation story visible: strip the conventional figure,
name the governing law explicitly, identify the reservoir pair the machine actually operates
between, derive the law-permitted ceiling from first-principles values, and bracket the gap
between that ceiling, what has been measured, and current design practice.

**Target:** the thermal-to-electric conversion efficiency of the steam Rankine power block in
a molten-salt power tower — heat delivered from the hot salt tank in, gross electricity out.
The hot reservoir is the 565 °C hot tank established in the five-whys (reduce-to-primitives)
example as GT-4. The cold reservoir is the power cycle's condenser, **not** the 290 °C cold
tank: the cold tank is the return leg of the heat *source* loop, and nothing in the plant
rejects waste heat at 290 °C. The question: how far below the law-permitted ceiling is current
practice, and how much of that distance is recoverable?

**Why this matters.** The estimate example (Phase 4) rebuilt the cost magnitude from
unit-factors. This theoretical-limit drill asks a different question of the same domain:
given the hot-reservoir temperature that the five-whys reduce-to-primitives pass established as a
ground truth, and the temperature at which the cycle actually rejects heat, what does the
Second Law permit for the heat engine operating between them? The bracket reveals whether the
efficiency headroom is real or illusory — and getting the cold reservoir right is what decides
the answer.

---

## Theoretical-Limit Drill

### Step 1 — Name the conventional figure and the conventions embedded in it

**Conventional figure:** Current-technology molten-salt power towers with hot salt at 565 °C
drive a subcritical steam Rankine cycle whose design-point gross cycle efficiency —
thermal energy into the steam generator, gross electricity out — is approximately **43.0%
with wet cooling** and **41.2% with an air-cooled condenser**. The dry-cooled figure is the
value NREL's Annual Technology Baseline carries as the representative commercial power tower,
anchored on the Crescent Dunes plant.

**Conventions embedded in this figure:**
- Subcritical steam conditions: the 565 °C salt limits live steam to roughly 125 bar / 537 °C,
  because molten-salt technology was developed around conventional subcritical plant equipment.
  The ~28 °C shortfall between salt and steam is finite heat-exchanger ΔT, not a law.
- Turbine configuration: a reheat cycle is a design choice. The one molten-salt tower whose
  measured power-block efficiency was located for this drill used a non-reheat turbine, and its
  own test report attributes its ~34% ceiling to that choice.
- Cooling method: wet versus dry cooling is a siting and water-availability choice, and it
  moves the figure by ~1.8 points.
- Gross basis: parasitic loads — salt pumps, feedwater pumps, cooling fans — are excluded from
  a gross cycle efficiency and consume roughly 7–13% of gross output.

These are engineering and siting conventions, not physical constraints. The governing law sets
a ceiling independent of all of them — but only once the ceiling is computed between the
reservoirs the machine actually works across.

**A different quantity, named here so it stays out of the bracket.** Whole-plant *annual
solar-to-electric* efficiency for power towers is usually quoted in a ~20–25% band. That is
not the quantity bounded below, and the two must not be bracketed against each other. Solar
Two's own test report makes the difference explicit: it reports the power block at 34%
measured (42% predicted for a commercial plant) and the whole plant at 13% measured (22%
predicted) — the whole-plant figure being the product of collection efficiency, the power
block, and the parasitic fraction. The difference between a ~42% power-block number and a
~22% whole-plant number is almost entirely optical and receiver loss *upstream* of the power
block. Bounding the whole-plant quantity would need optical and receiver limits, not just
Carnot, and is a different analysis.

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

**First-principles values.** T_hot comes from GT-4. T_cold does not, and that is the whole
point of this step.

The hot reservoir is the hot salt tank. Converting to kelvin (the conversion
definition: T [K] = T [°C] + 273.15):

    T_hot = 565 °C + 273 ≈ 838 K   (hot tank / upper reservoir, GT-4)

**Why the cold tank is not the cold reservoir.** The salt gives up heat between 565 °C and
290 °C and returns to the cold tank at 290 °C. That loop is the heat *source*: it carries
energy into the steam generator. The steam cycle rejects its waste heat somewhere else
entirely — into a condenser at near-ambient temperature. Nothing in the plant rejects heat at
290 °C, so a bound computed from the tank pair bounds a machine that does not exist. The test
any candidate bound has to survive is that real hardware does not beat it, and this one fails
that test on measured data, not on a design projection: the tank pair permits at most 32.8%,
and Solar Two — whose tanks sat at exactly 290 °C and 565 °C — measured 34.1% at full load.

The cold reservoir is therefore the condenser, and its temperature follows from the design
condenser pressure (GT-5):

    T_cold ≈ 43 °C + 273 ≈ 316 K   (wet-cooled, 0.087 bar condenser pressure)
    T_cold ≈ 57 °C + 273 ≈ 330 K   (air-cooled, 0.17 bar condenser pressure)

Which of the two applies is a plant- and site-specific design choice that GT-4 does not
settle, so it is carried as an assumption (§2) and the ceiling is stated as a range.

---

### Step 3 — Derive the law-permitted ceiling

Substituting the GT-4 hot-reservoir temperature and each GT-5 heat-rejection temperature into
the Carnot formula:

    wet-cooled:  η_Carnot = 1 − 316 / 838 = 1 − 0.377 = 0.623
    air-cooled:  η_Carnot = 1 − 330 / 838 = 1 − 0.394 = 0.606

**Law-permitted ceiling: ~61–62%** — 62.3% wet-cooled, 60.6% air-cooled.

This is the highest thermal-to-electric conversion efficiency any heat engine can achieve
while drawing heat from a 838 K reservoir and rejecting it at the condenser temperature a
real plant of this class is designed for — not for any specific cycle or working fluid, but
for any thermodynamically conceivable process. A law-permitted ceiling is only as applicable
as its reservoir pair: the Second Law forbids exceeding the bound between the reservoirs the
engine actually uses, and says nothing about a pair the engine never sees.

---

### Step 4 — Bracket the gap explicitly

| Tier | Figure | Kind |
|---|---|---|
| Ideal ceiling (Carnot, 838 K → 316 K wet / 330 K dry) | 62.3% wet-cooled, 60.6% air-cooled | derived |
| Current design practice (565 °C salt, subcritical steam) | 43.0% wet-cooled, 41.2% air-cooled | published design figure, cited |
| Measured (Solar Two, full load, non-reheat 12.8 MWe block) | 34.1% | observed, cited |

- **Ideal ceiling → current design practice: ~19 points.** 62.3 − 43.0 = 19.3 points
  wet-cooled; 60.6 − 41.2 = 19.4 points air-cooled. The gap barely moves with the cooling
  assumption, because raising T_cold lowers the ceiling and the achievable figure together.
  This is headroom nobody has reached, and most of it is not reachable — see the gap
  discussion below.
- **Current design practice → the one measured figure: ~7 points.** 41.2 − 34.1 = 7.1 points.
  Read the basis caveat before quoting this one.

**Basis caveat — read this before quoting the 7-point gap.** The 34.1% figure is the only
*measured* thermal-to-gross-electric efficiency at these reservoir conditions, and it comes
from a 12.8 MWe power block refurbished from a 1980s plant, with no reheat. The report that
measured it attributes the limit to that configuration directly — it states the non-reheat
turbine was limited to about 34%, and that newer reheat designs exceed 41% gross. So the
7 points is mostly a difference of turbine scale and configuration between a 1990s
demonstration and a commercial unit, not a shortfall of practice against design. The two
figures describe different populations, and no measured thermal-to-electric figure for a
commercial-scale molten-salt tower was located for this drill. That absence is why the middle
tier is labelled a design figure rather than promoted to "best demonstrated": the technique's
own rule is that the demonstrated tier takes an observed figure, never a calculated one.

**Gap decomposition — what is claimed and what is not.**

The loss mechanisms standing between the ~61–62% ceiling and ~41–43% design practice are
named in Step 1 and each is real: finite heat-exchanger ΔT (the salt is at 565 °C and the live
steam at 537 °C), turbine irreversibility, and the condensation and boiling irreversibilities
of a real steam cycle. Two of these carry sourced magnitudes: the cooling-method choice is
worth ~1.8 points (43.0% versus 41.2%), and reheat versus no reheat is worth ~7 points (34%
versus >41% gross, in the same measuring report).

**The relative shares of the remaining loss mechanisms are not measured here, and this drill
does not assert a split.** Apportioning ~19 points across turbine, heat exchanger and cycle
irreversibilities would require a heat-and-mass-balance model of a specific plant reporting
exergy destruction per component. That is what would measure it; nothing read here does.

**Most of the ~19 points is not recoverable, and that is a statement about the law, not about
engineering effort.** Carnot's bound is the efficiency of a *reversible* cycle, and reversible
heat transfer requires either infinite exchanger area or infinite time. A machine that
delivers finite power through finite hardware necessarily destroys exergy at every heat
exchange, so it cannot approach the ceiling however good the equipment gets. The gap is
mostly the price of operating at all, not a design defect.

**Constraint-relaxation conclusion:** At fixed T_hot the remaining headroom is modest and
expensive, so the demonstrated lever in this technology is **raising T_hot**. A 650 °C salt
design with an ultra-supercritical cycle is designed for 49.6% wet-cooled — but that is a
different reservoir pair, with its own Carnot ceiling of ~66% (1 − 316/923), so the bracket
translates upward rather than closing: the gap narrows only from ~19 to ~16 points. Raising
the source temperature buys efficiency; it does not buy reversibility.

---

## 1. Problem Essence

**Target:** the thermal-to-electric conversion efficiency of the steam Rankine power block in
a molten-salt power tower, drawing heat from the 565 °C hot tank established in the five-whys
(reduce-to-primitives) example as GT-4 and rejecting it to the cycle's condenser. The
question: how far below the law-permitted ceiling is current practice, and how much of that
distance is recoverable?

Getting the reservoir pair right is the substance of the analysis, not a preliminary to it. A
bound derived from the wrong pair is not a weaker bound — it is a bound on a different
machine, and a real plant can exceed it without violating anything.

---

## 2. Assumptions Table

| Assumption | Type | Treatment | Verdict | Verification |
|------------|------|-----------|---------|--------------|
| The plant rejects heat through either a wet cooling tower or an air-cooled condenser; which one is not established by GT-4 | convention | Carry both ends rather than picking one — cooling method is a siting and water-availability choice, and towers in arid siting are frequently dry-cooled; published design condenser pressures for this plant class give 0.087 bar wet-cooled and 0.17 bar dry-cooled | Accept — carried as a range, not a point; both ends are published design values and the conclusion holds at both | Verified as a range: GT-5 sources both condenser pressures, and chain C1 computes the ceiling at both ends. The ceiling-to-practice gap differs by 0.1 point between them, so nothing in the conclusion turns on the choice |
| Published design-point cycle efficiency for this technology class describes what commercial plants achieve in operation | untested belief | Verify before use — no measured thermal-to-electric figure for a commercial-scale molten-salt tower was located for this drill; the only measurement at these reservoir conditions comes from a 12.8 MWe non-reheat block that its own report calls configuration-limited | Challenge — unverified; no measured commercial-plant figure located, and the one measured figure comes from a non-representative power block | Unverified — flagged; GT-6 carries the design figure and the Solar Two measurement as separate readings rather than merging them, and chain C1's conclusion is directional under this gap: a lower measured figure widens the ceiling-to-practice gap rather than narrowing it |

---

## 3. Ground Truths

- **GT-4** Solar Salt (60% NaNO₃ / 40% KNO₃) is stable across the 290–565 °C commercial
  operating window, giving a hot-tank temperature T_hot ≈ 838 K and a 290 °C cold-tank return
  temperature — source: published material data for Solar Salt (direct measurement),
  established in the five-whys (reduce-to-primitives) example this drill hands off from. The
  cold-tank figure is the source loop's return temperature, not the power cycle's
  heat-rejection temperature; this drill consumes the hot-tank value only.

- **GT-5** Design condenser pressure for a 565 °C molten-salt power tower is 0.087 bar with a
  wet-cooled condenser and 0.17 bar with a dry-cooled one, giving heat-rejection temperatures
  of ≈ 43 °C (316 K) and ≈ 57 °C (330 K) — source: published design characterization of
  1000 MWt-receiver molten-salt power tower plants (Sandia, *An Evaluation of Possible
  Next-Generation High Temperature Molten-Salt Power Towers*, OSTI 1035342, Table 2), with the
  temperatures read from water saturation data at those pressures (definition, not estimate).

- **GT-6** Design-point gross cycle efficiency for current 565 °C subcritical molten-salt
  tower technology is 43.0% with wet cooling and 41.2% with an air-cooled condenser, at live
  steam conditions of 125 bar / 537 °C — source: the same Sandia design characterization
  (OSTI 1035342, Table 2), restated in Sandia's *Incorporating Supercritical Steam Turbines
  into Molten-Salt Power Tower Plants* (OSTI 1088078, §1.1), with the 41.2% dry-cooled figure
  carried as the representative commercial power tower in NREL's Annual Technology Baseline
  (*The Role of Concentrating Solar-Thermal Technologies in a Decarbonized U.S. Grid*,
  OSTI 1820100), anchored on the Crescent Dunes plant — that source states 575 °C hot salt,
  10 °C above GT-4's window top, for the same 41.2% dry-cooled cycle efficiency, so the two
  citations agree on the figure while describing salt temperatures 10 °C apart. The only
  *measured* figure at these reservoir conditions is 34.1% thermal-to-gross-electric at full
  load at Solar Two — direct measurement, *Final Test and Evaluation Results from the Solar Two
  Project* (OSTI 793226, §5.3.2) — whose 12.8 MWe power block had no reheat, a configuration
  the same report says limited it to about 34% where reheat designs exceed 41%.

- **GT-7** Whole-plant peak solar-to-electric efficiency for a power tower is a different
  quantity from the power block's efficiency, being the product of collection efficiency, the
  power block, and the net/gross parasitic fraction: 13 ± 0.4% measured at Solar Two against
  22% predicted for a commercial plant, with the power-block term alone at 34% measured and
  42% predicted — direct measurement, *Final Test and Evaluation Results from the Solar Two
  Project* (OSTI 793226, Table 6-1). Recorded here to keep the two bases apart, not consumed
  by any chain below.

---

## 4. Derivation Chains

### Conclusion C1: Current practice sits ~19 points below the Carnot ceiling for the cycle's actual reservoir pair, and most of that distance is not recoverable headroom

GT-4 (Solar Salt stable 290–565 °C; hot tank T_hot ≈ 838 K — direct measurement, established in the five-whys reduce-to-primitives example) + GT-5 (design condenser pressures 0.087 bar wet-cooled and 0.17 bar dry-cooled, giving T_cold ≈ 316 K and ≈ 330 K — published design characterization) + GT-6 (design-point gross cycle efficiency 43.0% wet-cooled and 41.2% air-cooled at 565 °C salt — published design characterization)
→ The cycle's cold reservoir is its condenser and not the 290 °C cold tank, because the salt loop carries heat into the steam generator and returns at 290 °C while the steam cycle rejects its waste heat to a condenser at near-ambient temperature
→ The Second Law's Carnot bound (η = 1 − T_cold/T_hot) applied to that reservoir pair yields a law-permitted ceiling of 62.3% wet-cooled and 60.6% air-cooled
→ Against the wet-cooled pair the gap from ceiling to current design practice is 62.3 − 43.0 = 19.3 percentage points
→ Against the air-cooled pair that gap is 60.6 − 41.2 = 19.4 percentage points
→ The two cooling cases agree to within 0.1 point, so the unresolved cooling-method assumption in §2 does not bear on this conclusion
→ Closing the ~19-point gap at fixed T_hot would require heat transfer approaching reversibility, which needs either infinite exchanger area or infinite time, so most of it is not recoverable by better equipment
→ The demonstrated lever is therefore raising T_hot rather than perfecting the cycle at fixed T_hot, and raising it translates the whole bracket upward: a 650 °C ultra-supercritical design is rated 49.6% against its own ~66% ceiling, a gap of ~16 points rather than none.

**Confidence:** HIGH — the Carnot ceiling is a physical law applied to a reservoir pair whose
hot end is GT-4 and whose cold end is a published design condenser pressure, and the chain's
head cites no `GT-N?`. The conclusion holds at both ends of the unresolved cooling-method
range, and it is directional under §2's second assumption: if commercial plants measure below
their design figure, the gap this chain reports widens rather than narrows. What this rating
does *not* rest on is any apportionment of the gap across components, which this analysis
declines to assert.

---

## 5. Abandoned Reasoning

**The Curzon-Ahlborn bound, tried as a tighter middle tier and rejected.** An endoreversible
engine at maximum power is bounded by η_CA = 1 − √(T_cold/T_hot), which for this reservoir
pair gives 38.6% wet-cooled and 37.2% air-cooled. That is tighter than Carnot and looks like
the "practical" ceiling the bracket wants. It was discarded because the design figure already
**exceeds** it — 43.0% against 38.6% — so it is not a bound on this machine at all.
Curzon-Ahlborn describes an engine tuned for maximum power output, and a plant tuned for
efficiency beats it. Promoting it to a tier would have understated what is already designed and built.

**The molten-salt tank pair, tried as the reservoir pair and rejected.** Taking the 290 °C
cold tank as the cold reservoir is arithmetically well-formed and yields a much tighter
ceiling. It was discarded because the salt loop is the heat source, not the heat sink: no part
of the plant rejects waste heat at 290 °C, and the resulting bound is exceeded by operating
equipment, which is the one thing a law-permitted ceiling cannot be.

---

## 6. Conclusion

**Recommended approach:** Treat the ~19-point ceiling-to-practice gap (chain C1) as mostly
irreducible rather than as recoverable headroom, and pursue efficiency by raising the source
temperature — supercritical and ultra-supercritical cycles at 600–650 °C salt — rather than by
chasing component refinements at fixed T_hot.
Before quoting any figure in the bracket, state whether it is a power-block or a whole-plant
number; the two differ by roughly a factor of two and are routinely confused.

**Key insight:** The Carnot bound (chain C1) is only as applicable as the reservoir pair it is
computed from — and identifying that pair, not evaluating the formula, is where this analysis
does its work. Applied to the molten-salt tank pair the bound is tight, arithmetically
correct, and wrong: it bounds a machine that rejects heat at 290 °C, which no plant does, and
real equipment exceeds it. Applied to the cycle's actual condenser it permits ~61–62%, which
reframes the question from "why is practice so far below the law?" to "how much of a
19-point gap can a finite-power machine ever recover?"

- Cross-technique continuity (chain C1): the five-whys reduce-to-primitives drill
  established GT-4 — the Solar Salt temperature window — from which chain C1 consumes the
  hot-tank temperature, the same ground truth the estimate drill's chain also anchors to; the
  heat-rejection temperature is separately sourced here as GT-5 because GT-4 does not supply
  it.
- The gap's shares are not apportioned (chain C1): the loss mechanisms are named and two of
  them carry sourced magnitudes — ~1.8 points for cooling method, ~7 points for reheat — but
  the split of the ~19 points across turbine, heat-exchanger and cycle
  irreversibilities is not measured here, and a per-component exergy balance for a specific
  plant is what would measure it.

**Confidence:** HIGH — matches chain C1. The ceiling is a physical law applied to a sourced
reservoir pair, the ceiling-to-practice gap holds at both ends of the cooling range, and the
one unverified belief in §2 can only widen it. The rating covers the bracket and the direction
of the gap, not any apportionment of it across components.
