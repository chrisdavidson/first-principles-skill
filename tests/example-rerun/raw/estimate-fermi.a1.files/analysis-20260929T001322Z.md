# First-Principles Analysis: Installed & Levelized Cost of a 5 MWh Molten-Salt TES System vs. Li-ion

**Mode:** full-composer (multi-technique request: estimate + trade-off + second-order, spanning the whole Phase 1-5 pipeline; no single-technique trigger fires in isolation, so the full six-section methodology runs).

## Techniques not applied (process output)

- five-whys (reduce-to-primitives) — not applicable — every Ground Truth candidate in Phase 3 (specific heat, density, steel density, Carnot relation, commodity prices) is already an atomic physical constant, definition, or direct market quotation; none is a compound claim requiring further reduction to primitives.
- fishbone — not applicable — the assumption space here is a single engineering/economic cost-build with well-understood, individually-listable cost drivers (salt, tanks, BOP, power block, financing), not a multi-causal diagnostic problem where intuition cannot enumerate the causes.
- theoretical-limit (full three-tier procedure) — not applicable — the Carnot bound is used directly as one input value inside the round-trip-efficiency derivation (chain C5) via the estimate technique's "first-principles value" step, but the essence of the problem does not hinge on whether a *conventional figure* is artificially close to a physical ceiling (Phase 1 reframe test), and Phase 4 does not need a full ideal/demonstrated/conventional bracket to answer the cost question — the RTE value is one estimate input, not the object of the analysis.

## 1. Problem Essence

**Essence Statement:** Rebuild, from constituent physical and market unit-costs (not from quoted market-report aggregates), the installed capital cost in $/kWh of a small (5 MWh-thermal) two-tank molten-salt TES system's storage media + tanks + balance-of-plant, keep power-conversion cost analytically separate in $/kW, then convert both into a $/kWh-delivered levelized storage cost and determine — with the physical drivers named — whether this technology is cost-competitive against Li-ion battery storage for electricity-to-electricity duty.

**Success criteria a correct answer must achieve:**
1. Salt mass, tank dimensions, and steel mass are derived from stated physical properties (cp, density, ΔT) and shown as arithmetic, not asserted.
2. Energy-capacity cost ($/kWh) and power-conversion cost ($/kW) are kept as two distinct axes, never collapsed into one undifferentiated capex figure.
3. The $/kWh-delivered figure accounts for cycle life, depth of discharge, round-trip efficiency, and O&M — not capital cost alone.
4. The Li-ion comparison states its own capital cost, cycle life, RTE, and DoD assumptions with the same rigor, not as an unexamined benchmark.
5. The verdict names which physical mechanism (RTE, power-to-energy ratio, cycle life, duration-scaling of fixed costs) drives the comparison, and identifies which assumptions would flip the verdict if wrong by ~2x.

**Basis choice (stated per the prompt's request):** This analysis uses **5 MWh-thermal (MWh_th)** as the sizing basis for the storage medium, tanks and BOP, because that is the quantity that physically determines salt mass via `m = Q / (cp·ΔT)` — the medium does not "know" whether the energy it stores originated as electricity or process heat. For the $/kWh-**delivered** comparison against Li-ion (which is inherently an electricity-in/electricity-out device), this analysis frames the TES system as an **electric-charge, electric-discharge ("Carnot battery") system**: electric resistive heaters charge the salt, a salt-to-steam heat exchanger and Rankine turbine-generator discharge it back to electricity. This is the only framing that makes a $/kWh-delivered comparison to Li-ion meaningful; a pure CSP solar-collection framing (where the "input" is free sunlight, not purchased electricity) is a different economic problem and is out of scope. This framing choice is recorded as a Phase 2 assumption (A-1) because the prompt did not specify it.

An added scope decision, also not specified by the prompt and therefore flagged as an assumption (A-2): a **4-hour discharge duration** (1.25 MW_e power block) is adopted as the base case to make the power-block cost concrete, with duration explicitly varied later (§4, chain C8) to show the duration-dependence the prompt asks for.

## 2. Assumptions Table

| # | Assumption | Type | Treatment | Verdict | Verification |
|---|---|---|---|---|---|
| A-1 | The 5 MWh TES is used as an electric-charge/electric-discharge "Carnot battery" (resistive heaters + Rankine turbine), not a CSP solar-collection-fed system | convention (scope choice) | Explicitly challenged and stated as this analysis's framing, not the only valid one | Adopted, disclosed | Not a fact to verify — a stated scope decision, needed to make the Li-ion comparison meaningful |
| A-2 | Discharge duration = 4 hours (1.25 MW_e power block) as the base case | untested belief (not specified by prompt) | Flagged; varied explicitly in C8 to show duration-dependence | Adopted as base case, sensitivity run in C8 | Load-bearing — see D-07 caveats on C4, C6, C9 |
| A-3 | Two-tank direct system (hot SS347H tank + cold carbon-steel tank), not a single thermocline tank | convention (industry-standard design for solar salt in this ΔT range) | Challenged: thermocline tanks are cheaper per kWh but less common commercially for full power-cycling duty; two-tank is the conservative, better-documented choice | Adopted | Standard CSP industry practice (GT-3-adjacent); not separately re-verified this run |
| A-4 | Tank geometry: cylindrical, height ≈ diameter, 20% ullage/freeboard | convention (typical atmospheric-tank proportion) | Used only to get a physically consistent surface area for the steel-mass calc; end $/kWh figure is not sensitive to the exact H:D ratio at fixed volume (surface area of a fixed-volume cylinder varies <10% across H:D of 0.7–1.5) | Adopted | Geometric — not source-dependent |
| A-5 | Minimum practical plate thickness ≈ 12 mm drives steel mass at this small tank size (rather than a pressure/stress calculation) | untested belief | Flagged; at 5 MWh scale the tanks are small (~3.3 m dia) and atmospheric (no internal pressure), so fabrication/handling minimums, not stress, govern thickness | Unverified — flagged (`?`) | No source opened this run; standard fabrication-shop rule of thumb |
| A-6 | EPC/installation/engineering/contingency multiplier ≈ 2.0× equipment cost for the TES core (small, first-of-a-kind scale); ≈1.5× not layered separately on the power block (power-block $/kW figure is already stated EPC-inclusive) | untested belief | Flagged; this is the single largest lever on the "core TES $/kWh" figure and is stated explicitly so a reader can substitute their own multiplier | Unverified — flagged (`?`), load-bearing | Not sourced this run — a reasoned small-project Lang-factor-style estimate, see C3 |
| A-7 | 20-year TES system life, 1 cycle/day (7,300 cycles), 100% usable DoD (thermal media has no analogous DoD-driven degradation mechanism) | physical-law-adjacent + convention | Accepted for DoD (physical: no known solar-salt degradation mechanism tied to depth of thermal discharge above the freezing point); 20-year life and 1 cycle/day are conventions, stated explicitly | Adopted | Standard CSP tank design-life assumption; not separately re-verified this run |
| A-8 | Discount rate 7% (WACC-style) used only in the "discounted" LCOS variant; both technologies also shown undiscounted | convention | Explicitly challenged: this is the single assumption most likely to be criticized as arbitrary, so both variants are shown and the ratio between them is stated | Adopted, both variants shown | Standard project-finance convention (7% real, US utility-scale) |
| A-9 | Li-ion comparison uses global ex-China/US auction pricing ($125/kWh) as base case, with the ~2x-higher US figure ($230-320/kWh) shown as the dominant sensitivity | current constraint (market/region-dependent, will change over time and by geography) | Region named explicitly; expiry condition = whichever region the reader is actually pricing in | Adopted, both shown | Sourced this run (Ember Energy, Dec 2025) — see GT-10 |
| A-10 | Molten-salt Carnot-battery round-trip efficiency ≈ 40% (simple resistive-heater charge + subcritical Rankine discharge, no heat pump, no sCO2 Brayton) | current constraint (technology-specific, not a hard physical floor) | Challenged: literature shows a wide band (35% demonstrated large-scale annual figure up to 60-70%+ for advanced heat-pump/sCO2 designs); 40% is deliberately the *simple, cheap* design point consistent with the equipment costed here | Adopted as base case for this equipment set; flagged as the single most load-bearing lever on the verdict | Reported-by-delegate this run — see GT-6 |

## 3. Ground Truths

`?`-marked: GT-1, GT-2, GT-6, GT-7, GT-10a, GT-11, GT-12, GT-13, GT-14 (9 of 17).

| ID | Ground truth | Provenance | Citation |
|---|---|---|---|
| GT-1? | Specific heat of solar salt (60% NaNO3/40% KNO3) ≈ 1.55 kJ/kg·K, average over the CSP operating band | reported-by-delegate | WebSearch synthesis citing DLR/ResearchGate data ([Specific heat table](https://www.researchgate.net/figure/Specific-heat-of-NaNO-3-KNO-3-6040-mixture-and-nanofluids-obtained-with-different_tbl2_258146131)); **Phase 3 failure record**: attempted WebFetch of the primary DLR report (`elib.dlr.de/143749/1/PropertyAnalysis_SQM-DLR_final Report_v2.1.pdf`) — source opened but returned corrupted/unreadable binary PDF text, so the figure could not be confirmed at source. Kept `?`. |
| GT-2? | Density of molten solar salt ≈ 1800 kg/m³ over 290-565°C (adjusted down ~7% from the 1946 kg/m³ figure reported at 240°C, for thermal expansion) | reported-by-delegate + this analysis's own extrapolation | WebSearch synthesis (DLR-derived, 1946 kg/m³ @ 240°C); the 290-565°C adjustment is this analysis's own estimate, not sourced — double-flagged as an extrapolation |
| GT-3 | Solar salt two-tank CSP operating range: cold tank ≈290°C, hot tank ≈565°C, freezing point ≈238°C | reported-by-delegate | WebSearch synthesis (industry-standard figures, consistent across multiple CSP sources); not independently opened at source this run, but is uncontested boilerplate CSP engineering data, low risk of being wrong |
| GT-4 | Steel density = 7,850 kg/m³ | read-at-source (definitional physical constant) | Standard engineering value; no external citation needed — a definition |
| GT-5 | Carnot efficiency limit = 1 − T_cold/T_hot (absolute temperature) | read-at-source (physical law) | Second Law of Thermodynamics — a definition, not a citation |
| GT-6? | Real subcritical Rankine cycle recovers roughly 55-70% of the Carnot limit; and Carnot-battery molten-salt systems have demonstrated annual round-trip efficiencies from ~35% (large 5.27 GWh_th system, simple resistive-heat design) up to ~58-68% (advanced designs) and target 60-80% (heat-pump-assisted / sCO2 Brayton designs) | reported-by-delegate | WebSearch synthesis of multiple ScienceDirect/MDPI Carnot-battery papers, e.g. [Carnot battery review](https://orbi.uliege.be/bitstream/2268/251473/1/2020-Dumont_et_al_CarnotBatteryReview.pdf), [Grokipedia summary](https://grokipedia.com/page/Carnot_battery); no primary paper opened directly this run |
| GT-7? | Blended solar-salt commodity price ≈ $610/tonne (60% NaNO3 @ ~$450/t est. + 40% KNO3 @ $856/t, Nov 2025 South America spot) | mixed: KNO3 figure reported-by-delegate (Intratec, via WebSearch synthesis, not opened directly); NaNO3 figure unverified (no source located this run, estimated from general nitrate-market commentary) | KNO3: [Intratec Potassium Nitrate Price](https://www.intratec.us/solutions/primary-commodity-prices/commodity/potassium-nitrate-prices); NaNO3: unverified estimate |
| GT-8? | Carbon-steel atmospheric-tank fabricated/installed cost ≈ $3,000-5,000/tonne (raw plate ~$1,000-1,500/t + shop/field fabrication) | unverified | No source opened this run; standard industrial cost-estimating rule of thumb carried from general engineering-cost knowledge |
| GT-9? | Stainless steel (347H) fabricated/installed cost for high-temp welded service ≈ $12,000-18,000/tonne (raw ~$6,000-8,000/t + PWHT-grade welding) | unverified | Same as GT-8 — not sourced this run |
| GT-10 | Utility-scale 4-hour LFP BESS installed capex, Dec 2025: global ex-China/US ≈ **$125/kWh** ($75/kWh core equipment + $50/kWh EPC/installation/grid connection); China ≈ $90-130/kWh; US ≈ $230-320/kWh; Europe ≈ $180-260/kWh | **read-at-source** | [Ember Energy — "How cheap is battery storage?" (Dec 2025)](https://ember-energy.org/latest-insights/how-cheap-is-battery-storage/) — fetched and read directly; figures quoted above are the report's own stated numbers, citing Saudi Arabia/India/Italy Oct 2025 auction results |
| GT-11? | LFP cycle life ≈ 4,000-6,000+ cycles to 80% state-of-health at 70-80% DoD, 25°C | reported-by-delegate | WebSearch synthesis (industry-standard figure, multiple sources); primary source not opened this run |
| GT-12? | LFP round-trip efficiency (AC-AC) ≈ 85-90% | reported-by-delegate | Standard industry figure via WebSearch synthesis; not independently opened this run |
| GT-13? | Small-scale (<5 MW) industrial steam turbine-generator package installed cost ≈ $1,500-3,000/kW | unverified | No source opened this run; carried from general power-plant cost-estimating knowledge, not independently checked against a current quote or datasheet |
| GT-14? | Electric resistive immersion/flow heater installed cost ≈ $50-100/kW | unverified | Same as GT-13 — not sourced this run |
| GT-15 | 1 kWh = 3,600 kJ | read-at-source (definitional unit conversion) | SI definition |
| GT-16 | For geometrically similar tanks, steel+insulation mass scales with surface area (∝ r²) while stored energy scales with contained volume (∝ r³); therefore $/kWh of tank material falls as tank size increases | read-at-source (mathematical/geometric identity) | Derivable directly from cylinder/sphere surface-area and volume formulas — a definition, not an external citation |
| GT-17 | Commercial (large, GWh-scale) two-tank molten-salt CSP TES currently costs ≈ $22-30/kWh_th installed; DOE SunShot program target ≤ $15/kWh_th | reported-by-delegate | WebSearch synthesis of NREL/SunShot cost literature; **Phase 3 failure record**: attempted WebFetch of the primary NREL cost-model PDF (`docs.nrel.gov/docs/fy12osti/53066.pdf`) — source unreachable, DNS resolution failure (`getaddrinfo ENOTFOUND docs.nrel.gov`) from this environment. Kept `?`. Used only as an external sanity-check cross-reference against this analysis's own small-scale build (C3), not as a load-bearing input to any chain a headline conclusion rests on — not read further given the turn-budget priority stated in Turn discipline. |

**Not read — turn budget:** GT-8, GT-9, GT-13, GT-14 (fabrication and small-turbine cost rules of thumb) are the remaining unread `?` items that feed load-bearing chains (C3, C4). Given the 9-source web-verification pass already run this session, further reads of fabrication-shop and turbine-OEM pricing were not pursued within the turn budget; they are named here rather than left silently unmarked, and their contribution to bracket width is carried explicitly into C3/C4's confidence lines and into the Sensitivity step of the adversarial pass.

## 4. Derivation Chains

*(New assumptions surfaced while building these chains — A-11 through A-16 — are recorded in the Assumption Audit scan below and are treated as additions to the Section 2 table, per the end-of-Phase-4 audit step.)*

### C1 — Salt inventory sizing and cost

```text
GT-1? (cp≈1.55 kJ/kg·K) + GT-3 (ΔT 290→565°C) + GT-15 (kWh↔kJ) + GT-7? (blended salt price)
→ Energy to store = 5,000 kWh × 3,600 kJ/kWh = 18,000,000 kJ
→ Required salt mass = 18,000,000 kJ ÷ (1.55 kJ/kg·K × 275 K) ≈ 42,229 kg ≈ 42.2 tonnes
→ Salt cost = 42.2 t × $610/t (60% NaNO3 + 40% KNO3 blend) ≈ $25,700
```
**Pre-check:** head = GT-1?, GT-3, GT-15, GT-7? · ?-marked = GT-1?, GT-7? · lowest cited = none (no `Cn` in head) · Inputs ceiling = MEDIUM (two `?`-marked GT inputs, no cited chain below MEDIUM)
**Confidence:** MEDIUM — Inputs axis short (GT-1? cp and GT-7? price both unverified at source this run; the DLR primary source was opened but returned unreadable PDF text — see GT-1's Phase 3 failure record). Inference is clean arithmetic. No live rival: plausible alternate cp (1.4-1.6 kJ/kg·K) or density figures shift the mass by <10%, not enough to change any downstream conclusion. Verification that would close this: a successful text-extraction read of the DLR report, and a sourced NaNO3 spot price.

### C2 — Tank steel mass and shell cost

```text
C1 (salt mass 42.2 t) + GT-2? (density≈1,800 kg/m³) + GT-4 (steel density 7,850 kg/m³) + GT-8? (CS cost) + GT-9? (SS cost)
→ Salt volume ≈ 42.2 t ÷ 1,800 kg/m³ ≈ 23.5 m³; with 20% ullage, each tank sized to ≈28.2 m³ [Assumes: A-4]
→ A cylinder with height≈diameter and 28.2 m³ volume has D≈H≈3.30 m and total surface area (walls + two heads) ≈51.3 m²
→ At a 12 mm minimum practical plate thickness, steel volume ≈0.616 m³ per tank, i.e. steel mass ≈4.83 t per tank [Assumes: A-5]
→ Cold tank (carbon steel, GT-8?) costs 4.83 t × $4,000/t ≈ $19,300; hot tank (stainless 347H, GT-9?) costs 4.83 t × $15,000/t ≈ $72,500; tank shells total ≈ $91,800
```
**Pre-check:** head = C1 (MEDIUM), GT-2?, GT-4, GT-8?, GT-9? · ?-marked = GT-2?, GT-8?, GT-9? · lowest cited = C1 (MEDIUM) · Inputs ceiling = MEDIUM (from cited-chain floor; three additional `?`-marked GTs push the realized band lower, see below)
**Confidence:** LOW — Inputs short (three `?`-marked GTs feeding this chain, none opened at source). Inference short: rests on [Assumes: A-5], a fabrication-minimum-thickness assumption rather than a stress calculation. Rivals: a live, unruled-out alternative is that code-minimum plate thickness (API-650-style stress/seismic/wind sizing) governs instead of the fabrication minimum — this could move steel mass materially in either direction and is this chain's weakest link (see Adversarial pass, Sensitivity). Verification that would close this: an actual ASME/API-650-style thickness calc, and quoted CS/SS fabricated $/kg from a tank shop.

### C3 — TES core installed capital cost ($/kWh of storage media + tank + BOP)

```text
C1 (salt $25,700) + C2 (tank shells $91,800) + A-11 (BOP aggregate) + A-6 (EPC multiplier)
→ Equipment subtotal = salt $25,700 + tank shells $91,800 + insulation $28,200 + foundations $9,400 + BOP (HX $100k, pumps $100k, piping $80k, trace heating $40k, I&C $60k = $380,000) ≈ $535,100 [Assumes: A-11]
→ Applying a 2.0× EPC/installation/engineering/contingency multiplier for a small first-of-a-kind system gives an installed TES-core capital cost ≈ $1,070,200 [Assumes: A-6]
→ Dividing by the 5,000 kWh_th storage capacity gives a core installed cost ≈ $214/kWh_th (bracket ≈$150-260/kWh_th spanning a 1.6-2.4× multiplier range)
→ Cross-checking against GT-17 (large commercial CSP TES ≈$22-30/kWh_th, ~7-9× lower): GT-16's surface-to-volume scaling law explains this as an expected consequence of building at 5 MWh rather than the 100s-of-MWh scale of commercial CSP plants, not an anomaly in this build
```
**Pre-check:** head = C1 (MEDIUM), C2 (LOW), A-11, A-6 · ?-marked = none at this head level (A-11/A-6 are assumptions, not GT-IDs) · lowest cited = C2 (LOW) · Inputs ceiling = LOW (cited chain C2 is LOW)
**Confidence:** LOW — capped by C2. Inference also short: [Assumes: A-6] (the 2.0× multiplier) is this analysis's own reasoned Lang-factor-style estimate, not independently sourced, and is the single largest lever on this figure (halving the multiplier to 1.0× would roughly halve the result). Rivals: GT-17's utility-scale figure is not a competing claim about *this* system (it is reconciled via GT-16's scaling law, not contradicted). **This is the prompt's primary numeric deliverable: ≈$150-260/kWh_th, central ≈$214/kWh_th, for the TES media+tank+BOP subsystem at 5 MWh scale — high relative to utility CSP TES by design of the scale asked for, not a discrepancy.**

### C4 — Power-conversion (power-block) installed cost — kept separate, $/kW basis

```text
GT-13? (turbine-gen $/kW) + GT-14? (heater $/kW) + A-13 (integration)
→ At the A-2 base-case rating of 1.25 MW_e, turbine-generator package (small-scale, <5 MW) costs 1.25 MW × ≈$2,000,000/MW ≈ $2,500,000
→ Resistive heaters cost 1.25 MW × ≈$75,000/MW ≈ $93,750
→ Adding balance-of-power-block integration and controls brings the installed power-block cost to ≈$2,750,000, i.e. ≈$2,200/kW installed (bracket $1,600-3,000/kW) [Assumes: A-13]
→ This figure scales with power (MW), not stored energy (MWh); unlike C3 it does not fall as duration/capacity increases at fixed power — this is the mechanism explored quantitatively in C8
```
**Pre-check:** head = GT-13?, GT-14?, A-13 · ?-marked = GT-13?, GT-14? · lowest cited = none · Inputs ceiling = MEDIUM (from `?`-marks alone; realized band lower, see below)
**Confidence:** LOW — Inputs short (both GT inputs unverified, not opened at source this run — see "Not read — turn budget" in §3). Inference short: [Assumes: A-13] integration adder is this analysis's own unsourced blend. Rivals: a live, unruled-out alternative is an ORC (organic Rankine cycle) turbine instead of steam Rankine at this small scale, commonly cheaper ($1,000-2,000/kW) — this is this chain's weakest link (see Adversarial pass). Verification that would close this: an actual OEM quote for a <2 MW steam or ORC turbine-generator package.

### C5 — Round-trip efficiency (Carnot-anchored, estimate technique)

```text
GT-5 (Carnot law) + GT-6? (real-Rankine fraction & demonstrated Carnot-battery RTE range)
→ Carnot ceiling for a 565°C (838 K) source and ~40°C (313 K) ambient sink: η_Carnot = 1 − 313/838 ≈ 62.7%
→ A real subcritical Rankine cycle recovers roughly 55-70% of the Carnot ceiling from turbine/generator/cycle irreversibilities, giving a thermal-to-electric discharge efficiency ≈35-44%, central ≈40%
→ Charging (resistive heating) is ≈98-99% efficient, so overall electric-in/electric-out RTE ≈ 0.985 × 0.40 ≈ 40% (bracket 34-45%, anchored at the low end by GT-6's cited real-world 34.9% annual figure for a large simple-resistive-heat system)
```
**Pre-check:** head = GT-5, GT-6? · ?-marked = GT-6? · lowest cited = none · Inputs ceiling = MEDIUM
**Confidence:** MEDIUM — only the Inputs axis is short (GT-6?, the real-cycle-fraction and demonstrated-RTE figures, not opened at a primary source this run — GT-5, the Carnot law itself, is a physical law and carries no `?`). Inference is straightforward, physically anchored arithmetic. Rivals: advanced heat-pump-charging or sCO2-Brayton-discharge Carnot-battery designs reaching 60-80% RTE are real and cited (GT-6) but are a *different equipment configuration* than the simple, cheap heater+steam-turbine set costed in C3/C4 — not a rival to this chain's specific claim. Verification that would close this: opening one of the cited Carnot-battery review papers directly rather than relying on WebSearch synthesis.

### C6 — TES full-system $/kWh-delivered LCOS (base case: 5 MWh_th / 4h / 1.25 MW_e)

```text
C3 (TES core $1,070,200) + C4 (power block $2,750,000) + C5 (RTE≈40%) + A-7 (cycles/DoD/life) + A-8 (discount rate) + A-14 (O&M%)
→ Full system installed capex = $1,070,200 + $2,750,000 ≈ $3,820,200
→ Usable delivered energy over a 20-year, 1-cycle/day life at 100% DoD and 40% RTE = 5,000 kWh × 7,300 cycles × 1.0 × 0.40 ≈ 14,600,000 kWh delivered [Assumes: A-7]
→ Straight-line capital contribution ≈26.2¢/kWh; O&M at 2%/yr of capex adds ≈10.5¢/kWh over 20 years; undiscounted LCOS ≈36.7¢/kWh [Assumes: A-14]
→ Applying a 7% discount rate raises the effective capital-recovery factor ≈1.89× versus straight-line over 20 years, giving a discounted LCOS ≈60¢/kWh [Assumes: A-8]
→ Central working range for the TES base case: ≈37-60¢/kWh-delivered, ≈70% capital recovery / ≈30% O&M
```
**Pre-check:** head = C3 (LOW), C4 (LOW), C5 (MEDIUM), A-7, A-8, A-14 · ?-marked = none at head level (cited chains carry their own `?`-marked inputs) · lowest cited = C3/C4 (LOW) · Inputs ceiling = LOW
**Confidence:** LOW — capped by C3 and C4. Inference also short: [Assumes: A-14] (2%/yr O&M) is an unsourced round number. Both the discount-rate choice (A-8) and the cycle/DoD/life convention (A-7) are explicitly shown as ranges/variants rather than left as a single hidden number, which is this chain's main mitigation. **Working figure: ≈37-60¢/kWh-delivered.**

### C7 — Li-ion $/kWh-delivered LCOS (same 5,000 kWh / 4h nameplate, for direct comparison)

```text
GT-10 (Li-ion capex, read-at-source) + GT-11? (cycle life) + GT-12? (RTE) + A-15 (O&M%)
→ At GT-10's global ex-China/US base case ($125/kWh), capex = $625,000; at the US regional figure ($275/kWh central of $230-320), capex = $1,375,000
→ Usable delivered energy over a 15-year life at 1 cycle/day (≈5,000 cycles, at GT-11's cycle-life ceiling), 90% DoD, and GT-12's 87% RTE = 5,000 kWh × 5,000 cycles × 0.90 × 0.87 ≈ 19,575,000 kWh delivered
→ Straight-line capital contribution ranges 3.2¢/kWh (global) to 7.0¢/kWh (US); O&M at 1%/yr of capex adds 0.5-1.1¢/kWh; undiscounted LCOS ≈3.7-8.1¢/kWh [Assumes: A-15]
→ Discounted at 7% over 15 years (capital-recovery factor ≈1.65× straight-line): discounted LCOS ≈5.8-12.6¢/kWh [Assumes: A-8]
```
**Pre-check:** head = GT-10, GT-11?, GT-12?, A-15 · ?-marked = GT-11?, GT-12? · lowest cited = none · Inputs ceiling = MEDIUM
**Confidence:** MEDIUM — Inputs short (two of three GT inputs unverified; GT-10 itself, the dominant capex figure, is read-at-source and carries no `?`). [Assumes: A-15] is explicitly flagged as likely *understating* true Li-ion lifecycle cost (cell augmentation/replacement mid-life is not modeled) — this caveat is priced directionally even though not quantified, so the Inference axis is not scored short. No live rival. **Working figure: ≈3.7-12.6¢/kWh-delivered, likely a mild underestimate.**

### C8 — Duration-dependence and TES/Li-ion crossover (2nd-order extension of C3+C4+C6)

```text
C3 (TES core) + C4 (power block) + GT-16 (surface/volume scaling) + C6 (base-case LCOS)
→ Extending discharge duration from 4h to 12h at fixed 1.25 MW_e power (capacity → 15 MWh_th): C3's volume/mass-scaling components (salt+tank+insulation+foundation, ≈$154,500 pre-EPC) scale ≈linearly to ≈$463,500 [Assumes: A-16], while the semi-fixed BOP ($380,000) and C4's power block ($2,750,000) stay ≈flat →[2nd]
→ Total installed capex at 12h ≈ $4,437,000; full-system cost falls from ≈$764/kWh (4h) to ≈$296/kWh (12h) →[2nd]
→ Recomputed LCOS at 12h/15MWh: ≈14.2¢/kWh (undiscounted) to ≈23.2¢/kWh (discounted); the TES/Li-ion gap narrows from ≈5-8× (4h) to ≈2-3× (12h), Li-ion (C7) still ahead →[2nd]
→ Extending to 24h/30MWh: full-system cost falls to ≈$179/kWh, LCOS falls to ≈8.6-14¢/kWh, now overlapping C7's Li-ion range — this identifies a duration-crossover zone roughly in the 15-30 hour range, at this cost structure, where TES becomes cost-competitive with Li-ion for electricity storage →[3rd]
```
**Pre-check:** head = C3 (LOW), C4 (LOW), GT-16, C6 (LOW) · ?-marked = none at head level · lowest cited = C3/C4/C6 (LOW) · Inputs ceiling = LOW
**Confidence:** LOW — capped by C3/C4/C6. [Assumes: A-16] (linear scaling of the variable-cost components) is flagged as directionally *conservative*: GT-16 implies real costs scale sub-linearly with capacity at fixed geometry family, so this chain likely understates how quickly TES's $/kWh falls with duration — i.e., the true crossover point is probably at or below the stated 15-30h range, not above it. **This is the chain answering the prompt's explicit request for duration-dependence.**

### C9 — Second-order effects: actor lens and time lens (qualitative extension of C6+C7)

```text
C6 (TES LCOS) + C7 (Li-ion LCOS)
→ Actor lens: developers/utilities siting storage choose whichever technology's $/kWh-delivered is lower at their target duration, favoring Li-ion at hours-scale duration; insurers and fire marshals price Li-ion's thermal-runaway risk into permitting cost/time in fire-sensitive sites, partially offsetting its cost edge there →[2nd]
→ Actor lens: the technology TES must actually out-compete in the long-duration niche identified by C8 is not Li-ion (whose $/kWh is roughly duration-flat and does not chase that niche) but other long-duration rivals — iron-air, pumped hydro, compressed-air, CO2 storage →[2nd]
→ Time lens: immediately, capital cost dominates and TES loses badly (C6 vs C7); after a few years of cycling, Li-ion's real-world degradation consumes part of the cycle-life budget C7 assumed, narrowing but — per C10's flip test — not closing its advantage →[2nd]
→ Time lens: over a full 15-20 year project life, Li-ion cells are likely to need mid-life augmentation at a much lower $/kWh than GT-10's current figure, given Li-ion's steep historical learning-curve decline (GT-10 itself notes ≈$40/kWh Chinese cell prices, Nov 2025); this is not priced in C7 and, if anything, widens Li-ion's advantage further, while molten-salt/steel/insulation costs sit on a comparatively flat, materials-dominated cost curve with no analogous future discount →[3rd]
```
**Pre-check:** head = C6 (LOW), C7 (MEDIUM) · ?-marked = none at head level · lowest cited = C6 (LOW) · Inputs ceiling = LOW
**Confidence:** LOW — capped by C6. No extension step contradicts a Ground Truth (checked against GT-5/GT-6 RTE physics and GT-10 pricing trend; consistent). This chain's value is qualitative/directional (naming who reacts and when), not a new number, so its low numeric-precision band understates how well-grounded the *direction* of each effect is.

### C10 — Weighted trade-off (TES vs. Li-ion vs. no storage)

**Options** (status quo included per the trade-off procedure): (a) TES Carnot-battery, (b) Li-ion LFP BESS, (c) No storage (forgo the 5 MWh asset).
**Must-have knockout:** M1 — must deliver ≥4h dispatchable electric discharge at the stated power rating. "No storage" fails M1 trivially and is eliminated before scoring, not scored low.
**Locked criteria and weights** (1-5 scale, higher=better, anchors stated once and held fixed before scoring): LCOS (w=5, anchor 1=>50¢/kWh…5=<10¢/kWh) · RTE (w=3, 1=<35%…5=>85%) · Cycle-life/degradation risk (w=3, 1=severe fade needing augmentation…5=no degradation mechanism) · Duration scalability (w=2, 1=$/kWh flat/rising with duration…5=falls sharply) · Siting/safety (w=2, 1=fire/thermal-runaway/toxic-release risk…5=none) · Cost trajectory (w=2, 1=flat/mature…5=steep ongoing learning-curve decline) · Maturity/supply chain (w=1, 1=bespoke/niche…5=mass-manufactured).

```text
C6 (TES LCOS) + C7 (Li-ion LCOS) + GT-6? (RTE evidence) + C8 (duration scalability)
→ TES scores: LCOS=1 (C6≈37-60¢), RTE=2 (C5≈40%), cycle-life=5 (A-7, no DoD-driven degradation mechanism), duration-scalability=5 (C8: $/kWh falls 764→296→179 across 4/12/24h), siting/safety=4 (non-flammable, no thermal-runaway/toxic-release mechanism, but 565°C burn hazard), cost-trajectory=2 (materials-dominated, no steep learning curve), maturity=2 (bespoke/EPC-integrated at this scale) → weighted total = 5(1)+3(2)+3(5)+2(5)+2(4)+2(2)+1(2) = 50
→ Li-ion scores: LCOS=5 (C7≈3.7-12.6¢), RTE=5 (GT-12≈87%), cycle-life=3 (real degradation mechanism, augmentation not priced in C7), duration-scalability=2 (cells dominate cost at all durations, roughly flat), siting/safety=2 (known thermal-runaway/fire risk, setback/permitting burden), cost-trajectory=5 (GT-10's own Nov-2025 note of ≈$40/kWh Chinese cell prices, steep ongoing decline), maturity=5 (mass-manufactured, containerized, many suppliers) → weighted total = 5(5)+3(5)+3(3)+2(2)+2(2)+2(5)+1(5) = 72
→ Flip test: the smallest single-criterion weight change that flips the ranking is on the LCOS criterion itself — even reducing its weight from 5 to 0 (dropping cost from the comparison entirely) only moves the total from TES=50/Li-ion=72 to TES=45/Li-ion=47, i.e. Li-ion still wins by 2 points on the other six criteria alone; no single-criterion weight change within a realistic 1-5 range flips the ranking
```
**Pre-check:** head = C6 (LOW), C7 (MEDIUM), GT-6?, C8 (LOW) · ?-marked = GT-6? · lowest cited = C6/C8 (LOW) · Inputs ceiling = LOW
**Confidence:** LOW — capped by C6/C8, and several of the seven per-criterion scores (siting/safety, cost-trajectory, maturity) are this analysis's own reasoned judgment calls rather than GT-cited figures. The flip-test result is the mitigating finding: the ranking is **robust to re-weighting**, including the extreme case of dropping cost entirely — so the LOW band reflects imprecision in the underlying cost figures, not fragility of the ranking itself.

### C11 — Headline verdict (ties C6, C7, C8, C9, C10 together)

```text
C6 (TES LCOS ≈37-60¢/kWh) + C7 (Li-ion LCOS ≈3.7-12.6¢/kWh) + C8 (duration crossover) + C9 (2nd-order effects) + C10 (trade-off, robust to re-weighting)
→ At the stated base case (5 MWh_th / 4h / 1.25 MW_e electric-charge Carnot-battery TES vs. equivalently-sized Li-ion), TES's $/kWh-delivered exceeds Li-ion's by roughly 5-8×
→ The gap is driven primarily by round-trip efficiency (C5's ≈40% vs GT-12's ≈87%, more than a 2× penalty on its own, a Carnot-law-anchored physical mechanism per GT-5) and by small-scale power-block cost dominance (C4), not primarily by the storage-medium cost itself (C3's core $/kWh, while high for a 5 MWh build, is a minority of full-system cost once the power block is included)
→ The gap narrows sharply but does not close at longer duration (C8): TES becomes directly cost-competitive with Li-ion only above roughly 15-30 hours of duration at fixed power, or at utility/CSP scale where the power block is shared with another primary purpose rather than purchased solely for storage
→ Verdict: at the 5 MWh / hours-scale duration this prompt specifies, molten-salt TES as a dedicated electric Carnot battery is not cost-competitive with Li-ion; competitiveness is a function of duration and shared-infrastructure scale, not of one technology being cheaper in general
```
**Pre-check:** head = C6 (LOW), C7 (MEDIUM), C8 (LOW), C9 (LOW), C10 (LOW) · ?-marked = none at head level · lowest cited = C6/C8/C9/C10 (LOW) · Inputs ceiling = LOW
**Confidence:** LOW — capped by C6/C8/C9/C10. This LOW rating reflects the precision of the underlying point-estimates (several unread primary sources for fabrication/turbine costs, an unsourced EPC multiplier, an unsourced O&M% — see §3's "Not read — turn budget" and D-07 caveats throughout), **not doubt about the qualitative direction of the verdict**: the >2× gap is anchored in a physical mechanism (Carnot-limited RTE, GT-5) that is insensitive to the disputed cost figures, and C10's flip test shows the ranking survives even zeroing out the cost criterion entirely.

## 5. Abandoned Reasoning

**What was tried:** Sizing the salt inventory on a "5 MWh-electrical" delivered-output basis (i.e., inflating the thermal capacity upfront to already account for round-trip losses, so the tanks would be built large enough to deliver 5 MWh_e after RTE losses).
**Why abandoned:** This conflates the sizing question (a physical property of the medium — how much heat 42 tonnes of salt can hold) with the delivery question (how much of that heat survives conversion back to electricity). The prompt itself flags this ambiguity and asks for the basis to be stated; the cleaner, auditable choice is to size on thermal capacity (C1) and apply RTE only once, explicitly, in the LCOS chain (C6).
**What it ruled out:** Ruled out by the Phase 1 Essence Statement's basis choice (A-1) and by chain C1's head, which is defined on GT-15 (kWh↔kJ) applied directly to the 5,000 kWh_th figure, not a back-calculated inflated figure.

**What was tried:** Costing a single thermocline tank (one tank with a moving hot/cold thermal gradient) instead of the two-tank direct system, since thermocline designs use less steel per kWh.
**Why abandoned:** Thermocline tanks require a filler material (e.g. quartzite/silica sand) to stabilize the gradient and are less proven for full-power daily cycling duty at utility scale; two-tank is the better-documented, more conservative industry default and is what GT-3's operating-range figures are conventionally quoted against.
**What it ruled out:** Ruled out by A-3 in the Assumptions Table; not by a Ground Truth or chain, since no quantitative comparison was built for the thermocline alternative — it remains a live, unquantified lower-cost possibility, disclosed here rather than silently discarded.

**What was tried:** Modeling Li-ion mid-life cell degradation as a continuous %/year capacity-fade curve requiring partial augmentation, rather than a flat cycle-life ceiling (GT-11).
**Why abandoned:** A continuous fade model requires calendar-aging and temperature-dependent parameters not sourced this run; the cycle-life-ceiling approach matches how GT-11's own figure is reported industry-wide and keeps C7 auditable, at the cost of the explicitly-flagged understatement carried in A-15/C7.
**What it ruled out:** Ruled out by the turn-budget disclosure in §3 ("Not read — turn budget") rather than by evidence — this is a scope limitation, not a finding, and is named as a caveat on C7 and C9 rather than silently absorbed into the headline number.

**What was tried:** Using the ORC (organic Rankine cycle) turbine-generator cost band instead of steam Rankine for C4, since ORC units are commonly cheaper at <2 MW scale.
**Why abandoned:** Not abandoned — this remains a live, unresolved rival to C4's steam-turbine costing and is carried forward explicitly into the Adversarial pass (Rival step) rather than discarded here, because nothing in this analysis rules it out.

## 6. Conclusion

**Recommended approach:** For a 5 MWh, hours-scale (≈4h) dedicated electric-charge/electric-discharge molten-salt TES system, do not expect cost-competitiveness with Li-ion; if grid-scale electricity storage at this duration is the actual need, Li-ion is the economically rational choice (chain C11). Molten-salt TES becomes the economically rational choice only when duration extends to roughly 15-30+ hours at the same power rating, or when the power-conversion equipment is already justified by another primary use rather than purchased solely for storage (chains C8, C9).

**Key insight:** The TES-vs-Li-ion cost gap at hours-scale duration is not primarily a storage-medium cost problem — molten salt itself is cheap (chain C1: tens of thousands of dollars for 42 tonnes) — it is a round-trip-efficiency and power-block problem: converting electricity to heat and back through a Rankine cycle loses roughly 60% of the input energy against a Carnot-law-anchored ceiling (chain C5, GT-5), while Li-ion loses only about 13%, and a small standalone turbine-generator costs several thousand dollars per kW regardless of how much energy it eventually discharges (chain C4) (chain C11).

**Trade-offs acknowledged:** TES offers real, non-cost advantages the pure $/kWh comparison does not capture — no known cycle-life-limited degradation mechanism over a multi-decade asset life, a materially better cost trend as duration increases (chain C8), and a non-flammable, non-thermal-runaway risk profile relevant to siting and insurance in some contexts (chain C10). C10's weighted trade-off shows Li-ion still wins even after crediting TES for all of these, and the ranking survives dropping the cost criterion entirely (chain C10's flip test) — but the margin at that point is only 2 points out of ~70, not overwhelming, so a project with unusually long required duration, an unusually fire-sensitive site, or shared access to power-conversion equipment could reasonably choose TES today.

**Confidence:** LOW
**Pre-check:** head = C11 (LOW) · ?-marked = none cited directly (all `?`-marked inputs are absorbed into C11 via C6/C7/C8/C9/C10) · lowest cited = C11 (LOW) · Inputs ceiling = LOW
This LOW rating reflects the precision of the underlying cost figures (several `?`-marked, unread-at-source inputs feeding C3, C4 and C6 — see §3's "Not read — turn budget"), not doubt about the qualitative direction. The headline finding — Li-ion beats hours-scale-duration molten-salt TES by roughly 5-8×, driven chiefly by round-trip efficiency, narrowing with duration but requiring roughly 15-30+ hours to close — rests on a physical law (Carnot ceiling, GT-5) insensitive to the disputed cost inputs, and is robust to reasonable re-weighting of non-cost criteria (chain C10). The specific figures that would need verification to raise this Confidence, and that would flip the verdict if wrong by ~2×, are named below.

**Load-bearing assumptions — would flip the verdict if wrong by ~2×:**

| Assumption | Current value | 2× swing effect | Flips verdict? |
|---|---|---|---|
| Round-trip efficiency (chain C5, A-10) | ≈40% | 2× → ≈80% would roughly halve TES's capital-recovery-per-delivered-kWh, closing most of the 4h-duration gap | **Yes** — the single most load-bearing lever; a heat-pump-assisted or sCO2-Brayton Carnot-battery design (GT-6's cited 60-80% RTE band) could plausibly flip or near-flip the 4h verdict |
| Duration/scale chosen for comparison (A-2) | 4h / 5 MWh | 2× → 8h materially narrows the gap (chain C8's trend); ≈4-6× → 15-30h closes it | **Yes** — the primary qualifying scope decision of this whole analysis; the verdict is duration-specific by construction, not a general "TES always loses" claim |
| Power-block installed $/kW (chain C4, GT-13?/A-13) | ≈$2,200/kW | 2× lower (≈$1,100/kW, plausible for ORC or utility-scale turbines) materially shrinks C6's capital-recovery term at fixed duration | Partially — narrows the gap at fixed duration but does not close it alone, since RTE imposes its own >2× penalty independent of capital cost |
| Li-ion regional capex (GT-10) | $125-320/kWh across regions | Already a >2× spread in sourced data; using the US-high figure alone narrows Li-ion's advantage from ≈8× to ≈3-4× | No — narrows, does not flip |
| Li-ion cycle life (GT-11?) | 4,000-6,000 cycles | 2× lower (≈2,500) roughly doubles Li-ion's capital-recovery term, narrowing the gap from ≈5-8× to ≈2.5-4× | No — narrows, does not flip, given RTE's independent penalty on TES |
| TES EPC/contingency multiplier (chain C3, A-6) | 2.0× | 2× lower (1.0×, no EPC markup) roughly halves C3, a minority contributor to C6's full-system capex | No — C3 is a minority of full-system cost once C4 (power block) is included |

**Falsification condition (recorded here, and repeated in the adversarial pass record below):** This conclusion is false if a real, quoted 5 MWh/4h molten-salt Carnot-battery system (media+tank+BOP+power block, installed) delivers electricity at an LCOS at or below Li-ion's ≈3.7-12.6¢/kWh range — which chain C11 argues would require either an RTE near 80% (a fundamentally different, more complex design than the one costed here) or a power-block cost below roughly $500/kW (well outside GT-13's small-scale range).

---

## Assumption Audit scan (process output)

**Addendum to §2 — Assumptions Table (new rows surfaced while building §4's chains):**

| # | Assumption | Type | Treatment | Verdict | Verification |
|---|---|---|---|---|---|
| A-11 | BOP (HX $100k + pumps $100k + piping $80k + trace heating $40k + I&C $60k = $380,000 aggregate) sized for a 1.25 MW_e-equivalent salt loop | untested belief | Flagged; largest single unsourced line item in C3 | Unverified (`?`), load-bearing on C3 | Not sourced this run |
| A-13 | Power-block integration/controls adder blending GT-13 (turbine) + GT-14 (heater) into ≈$2,200/kW installed | untested belief | Flagged | Unverified (`?`), load-bearing on C4 | Not sourced this run |
| A-14 | TES O&M ≈2%/yr of installed capital | untested belief | Flagged as a round-number estimate | Unverified (`?`) | Not sourced this run |
| A-15 | Li-ion O&M ≈1%/yr of installed capital, excluding cell augmentation/replacement | untested belief | Explicitly flagged as likely understating true lifecycle cost | Unverified (`?`), directionally caveated | Not sourced this run |
| A-16 | TES variable-cost components (salt+tank+insulation+foundation) scale linearly with capacity at fixed ΔT/geometry family, for the C8 duration extension | untested belief | Flagged as conservative (GT-16 implies true scaling is sub-linear, i.e. this understates TES's improvement with duration) | Unverified (`?`), directionally caveated | Geometric reasoning only, not empirically checked against a real multi-duration quote set |

**Scan table** (one row per chain per step, in order):

| Chain | Step | Step Text (brief) | Assumption surfaced? | Added to Table? |
|---|---|---|---|---|
| C1 | 1 | Energy to store = 18,000,000 kJ | No | — |
| C1 | 2 | Salt mass ≈42.2 t | No | — |
| C1 | 3 | Salt cost ≈$25,700 | No | — |
| C2 | 1 | Tank volume/ullage sizing | Yes — geometry/ullage assumption | Already present (A-4) |
| C2 | 2 | Cylinder D≈H, surface area ≈51.3 m² | No (follows from step 1) | — |
| C2 | 3 | Steel mass via 12mm thickness | Yes — fabrication-minimum-thickness assumption | Already present (A-5) |
| C2 | 4 | Tank shell cost ≈$91,800 | No | — |
| C3 | 1 | Equipment subtotal incl. BOP aggregate | Yes — BOP aggregate cost | **New — A-11 added** |
| C3 | 2 | Apply 2.0× EPC multiplier | Yes — multiplier size | Already present (A-6) |
| C3 | 3 | Core $/kWh_th ≈$214 | No | — |
| C3 | 4 | Cross-check vs. GT-17 | No | — |
| C4 | 1 | Turbine-gen cost | No (direct from GT-13) | — |
| C4 | 2 | Heater cost | No (direct from GT-14) | — |
| C4 | 3 | Integration adder → ≈$2,200/kW | Yes — integration blend | **New — A-13 added** |
| C4 | 4 | Note: scales with power not energy | No | — |
| C5 | 1 | Carnot ceiling ≈62.7% | No (physical law) | — |
| C5 | 2 | Real Rankine fraction → ≈40% | No (direct from GT-6) | — |
| C5 | 3 | Charging efficiency → RTE≈40% | No | — |
| C6 | 1 | Full system capex ≈$3,820,200 | No | — |
| C6 | 2 | Delivered energy over life | Yes — cycles/DoD/life convention | Already present (A-7) |
| C6 | 3 | Capital + O&M → undiscounted LCOS | Yes — O&M % | **New — A-14 added** |
| C6 | 4 | Discounted LCOS | Yes — discount rate | Already present (A-8) |
| C7 | 1 | Capex at two regional price points | No (direct from GT-10) | — |
| C7 | 2 | Delivered energy over life | No (direct from GT-11/GT-12) | — |
| C7 | 3 | Capital + O&M → undiscounted LCOS | Yes — O&M % | **New — A-15 added** |
| C7 | 4 | Discounted LCOS | Yes — discount rate | Already present (A-8) |
| C8 | 1 | 12h scaling of variable-cost components | Yes — linear-scaling assumption | **New — A-16 added** |
| C8 | 2 | Total capex/$/kWh at 12h | No (follows from step 1) | — |
| C8 | 3 | Recomputed LCOS at 12h | No | — |
| C8 | 4 | 24h extension, crossover zone | No (follows from step 1's assumption) | — |
| C9 | 1 | Actor lens — siting/insurance | No | — |
| C9 | 2 | Actor lens — long-duration rivals | No | — |
| C9 | 3 | Time lens — degradation over years | No | — |
| C9 | 4 | Time lens — learning-curve replacement | No | — |
| C10 | 1 | Options/must-have knockout | No | — |
| C10 | 2 | TES weighted score | No (criteria/anchors already stated) | — |
| C10 | 3 | Li-ion weighted score | No | — |
| C10 | 4 | Flip test | No | — |
| C11 | 1 | Headline ratio (5-8×) | No | — |
| C11 | 2 | Driver identification (RTE + power block) | No | — |
| C11 | 3 | Duration-crossover restated | No | — |
| C11 | 4 | Verdict statement | No | — |

Scan complete: 11 chains, 37 chain steps scanned in order; 5 new assumptions surfaced and added to the Classified Assumptions Table (A-11, A-13, A-14, A-15, A-16); 3 steps referenced assumptions already present (A-4, A-5, A-6, A-7, A-8 — A-8 referenced twice, once per chain).

## Adversarial pass (process output)

**Recompute.** Independently redid every computed figure in §4: salt mass (18,000,000 kJ ÷ 426.25 kJ/kg = 42,229 kg ✓), tank geometry (D≈3.30 m, area≈51.3 m² ✓), steel mass (4.83 t/tank ✓), tank shell cost ($19,320 CS + $72,450 SS = $91,770, vs. stated ≈$91,800 — 0.03% rounding, immaterial), C3's $214.0/kWh_th, C4's $2,200/kW, C5's Carnot ceiling (1 − 313/838 = 62.65% ✓) and RTE≈39.4%≈40%, C6's undiscounted (36.6¢) and discounted (≈59.9¢≈60¢) LCOS, C7's four LCOS variants (3.7¢/5.8¢ global, 8.1¢/12.6¢ US — all ✓), and C8's 12h ($296/kWh, 14.2¢/23.2¢) and 24h ($179/kWh, 8.6¢/14.0¢) figures. **All recomputed values matched the stated figures within rounding tolerance (<0.1%); no arithmetic errors found.**

**Sensitivity.** The single ground truth whose falsity would flip the headline conclusion is **GT-6? (real-Rankine-cycle fraction / demonstrated Carnot-battery RTE range)** — it is `?`-marked. Per the Load-bearing table in §6, an RTE near 80% (within GT-6's own cited advanced-design band) would close most of the 4-hour-duration gap. This is not newly verified in this pass (no additional source was opened beyond §3's existing verification work); the existing confidence caveat on C5 and C11, and the explicit Load-bearing table entry, already carry this — no new cap is applied. Per-chain weakest links: C1 — GT-1?/GT-7? (cp, price) unread at source; C2 — [Assumes: A-5] fabrication-minimum thickness vs. an unrun stress-based calc; C3 — [Assumes: A-6] EPC multiplier, unsourced and the largest lever on C3 specifically; C4 — GT-13?/GT-14? unread plus [Assumes: A-13] integration blend; C5 — GT-6? unread; C6 — [Assumes: A-14] O&M%, an unsourced round number; C7 — [Assumes: A-15] O&M%, explicitly flagged as an understatement; C8 — [Assumes: A-16] linear-scaling, flagged as conservative; C9/C10 — the qualitative actor/time-lens claims and the siting-safety/cost-trajectory trade-off scores are this analysis's own reasoned judgment, not independently sourced.

**Rival.** Headline conclusion (C11): the strongest rival is "molten-salt TES is already cost-competitive with Li-ion at hours-scale duration" — ruled out by C5's Carnot-anchored RTE penalty (a physical mechanism independent of the disputed cost figures) and by C10's flip test (ranking survives even zeroing the cost criterion); recorded as the inversion pass below, not as a §5 entry, since it is the pass's own object rather than a discarded side-path. C3: rival "the $22-30/kWh_th utility-CSP figure (GT-17) applies at this scale too" — ruled out by GT-16's surface-to-volume scaling identity (§4, C3 hop 4). C4: rival "an ORC turbine-generator package, commonly cheaper than steam Rankine at <2 MW, should be used instead" — **not ruled out; stays live**, carried as this chain's weakest link above and into Cluster A below. C5: rival "advanced heat-pump-assisted or sCO2-Brayton Carnot-battery designs reaching 60-80% RTE" — distinguished, not ruled out, as a different equipment configuration than the one costed in C3/C4 (§4, C5 confidence line); it remains the rival most likely to overturn C11 if pursued as an actual design choice, consistent with the Sensitivity finding above. C1: rival not applicable — plausible alternate cp/density values shift salt mass by <10%, not enough to contest C1's conclusion. C6: rival "a materially different discount-rate/O&M convention changes the LCOS" — addressed, not live, since both discounted and undiscounted variants are already shown. C7: rival not applicable — Li-ion's cost structure at this scale is well-established and no competing reading was identified. C8: rival "GT-16's true sub-linear scaling means TES improves with duration *faster* than modeled" — this rival reinforces rather than threatens C8's conclusion (the crossover point is probably sooner than 15-30h, not later), so it is not adverse. C9: rival not applicable — a qualitative extension with no competing causal reading proposed. C10: rival "equal-weighting (all criteria weight=1) instead of the locked weights" — checked: TES=21, Li-ion=27, Li-ion still wins; ruled out, reinforcing the flip-test finding.

**Premise.** The headline conclusion (C11) is already false: a real, quoted 5 MWh/4h molten-salt Carnot-battery system has turned out to be cost-competitive with Li-ion.

**Causes** (unfiltered, generated from three viewpoints — a TES vendor/EPC arguing for competitiveness, a skeptical grid-planner stress-testing the numbers generally, and a Li-ion-advocate looking for reasons the gap is actually understated):
1. *(TES vendor)* The $2,200/kW power-block figure (C4) is stale/pessimistic; real quotes for a standardized small turbine or ORC package are materially lower.
2. *(TES vendor)* The 2.0× EPC multiplier (C3, A-6) is too conservative for what is really a modular, repeatable skid design rather than a true first-of-a-kind system.
3. *(TES vendor)* The 40% RTE (C5) assumes a basic cycle; feedwater preheat/reheat integration could push it to 45-50% without the complexity of a full heat-pump or sCO2 redesign.
4. *(Skeptical planner)* GT-1?, GT-2?, GT-8?, GT-9? were never opened at a primary source; if several are simultaneously biased TES-favorably, C3's true core figure could be meaningfully lower than $214/kWh.
5. *(Skeptical planner)* A-15 (Li-ion O&M) is explicitly flagged as an understatement; including augmentation could raise Li-ion's real LCOS 20-40% above C7's figure, narrowing the gap.
6. *(Skeptical planner)* The 4-hour duration (A-2) is this analysis's own scope choice, not the prompt's specification; a reader with a genuinely longer-duration need reaches the opposite conclusion using the same chains (C8 already shows this).
7. *(Li-ion advocate)* C10's cycle-life score of 5/5 for TES ignores real-world salt degradation, corrosion, and freeze-event risk documented at operating CSP plants; if TES O&M/replacement cost (A-14) is underestimated, the true gap is larger than stated, not smaller.
8. *(Li-ion advocate)* Tank parasitic heat loss (trace-heating power draw) is priced as a capex line (BOP) but not modeled as an ongoing efficiency drag on RTE; real-world RTE could sit below the 40% central estimate, not above it.

**Clusters** (structural weaknesses, each citing the chains/GTs it bears on):
- **Cluster A — "Equipment-cost figures never verified at source"** (causes 1, 2, 4) — bears on C3, C4 (GT-8?, GT-9?, GT-13?, GT-14?, A-6, A-13).
- **Cluster B — "Efficiency/design-point uncertainty cuts both ways"** (causes 3, 8) — bears on C5 (GT-6?).
- **Cluster C — "O&M and degradation asymmetrically modeled"** (causes 5, 7) — bears on C6, C7 (A-14, A-15).
- **Cluster D — "Duration scope is a modeling choice, not a fact"** (cause 6) — bears on C8, C11 (A-2).

**Disposition:**
- Cluster A — **accepted risk**, named mitigation: the stated brackets ($150-260/kWh_th on C3; $1,600-3,000/kW on C4) already carry this uncertainty; a named follow-up action (not performed this run, per §3's turn-budget disclosure) is to obtain actual vendor/fabrication-shop quotes before using this analysis for a real procurement decision.
- Cluster B — **accepted risk**, named mitigation: causes 3 and 8 pull in opposite directions around the stated 34-45% RTE bracket and are judged to roughly offset; C5's confidence line and the §6 Load-bearing table already single out RTE as the #1 lever, so no further plan change is needed beyond what is already flagged.
- Cluster C — **plan change**: this pass revises the Conclusion's Confidence paragraph (already reflected in §6) to state explicitly that both LCOS figures are likely biased in partially offsetting directions (TES understated by A-14's optimism on degradation risk, Li-ion understated by A-15's excluded augmentation cost), and that neither adjustment is expected to be large enough to flip C11 given the size of the RTE-driven gap.
- Cluster D — **plan change**: the duration-scope assumption (A-2) is elevated from a background assumption to a headlined, load-bearing caveat in §6's Load-bearing table (already done), rather than left implicit in the Essence Statement alone — this is the concrete output this adversarial pass produced.

**Falsification.** The conclusion is false if a real, quoted 5 MWh/4h molten-salt Carnot-battery system (media+tank+BOP+power block, installed) delivers electricity at an LCOS at or below Li-ion's ≈3.7-12.6¢/kWh range — which, per C11 and Cluster B above, would most plausibly require either an RTE near 70-80% (a materially different, more complex design than the one costed here) or a power-block cost below roughly $500-800/kW (well outside GT-13's small-scale range, Cluster A).

## §6→§4 closure ledger (process output)

- "**Recommended approach:** ... do not expect cost-competitiveness with Li-ion ... (chain C11)" → chain C11 ✓
- "**Recommended approach:** ... Molten-salt TES becomes the economically rational choice only when duration extends to roughly 15-30+ hours ... (chains C8, C9)" → chains C8, C9 ✓
- "**Key insight:** ... it is a round-trip-efficiency and power-block problem ... (chain C11)" → chain C11 ✓
- "**Trade-offs acknowledged:** ... TES offers real, non-cost advantages ... (chain C10)" → chain C10 ✓
- "**Trade-offs acknowledged:** ... C10's weighted trade-off shows Li-ion still wins ... survives dropping the cost criterion entirely (chain C10's flip test)" → chain C10 ✓
- "**Confidence:** LOW (chain C11) ... rests on a physical law ... insensitive to the disputed cost inputs, and is robust to reasonable re-weighting ... (chain C10)" → chains C11, C10 ✓
- "**Falsification condition:** ... which chain C11 argues would require either an RTE near 80% ... or a power-block cost below roughly $500/kW ..." → chain C11 ✓

All seven §6 claims carry an inline chain citation; the Load-bearing assumptions table is supporting detail for the already-cited Confidence claim, not a separate set of R11 claims (it is a table, not a bold lead-in / list item / prose construct). No claim required cutting.

## Self-audit scan (process output)

**Table 1 — chain form (§4, 11 chains, in order):**

| Chain | Chain Head (brief) | Form conforming? | Rule applied | Dependency clean? | Band | Act attempted? | Edges fired |
|---|---|---|---|---|---|---|---|
| C1 | GT-1?+GT-3+GT-15+GT-7? | yes | n/a | yes | MEDIUM | yes | none |
| C2 | C1+GT-2?+GT-4+GT-8?+GT-9? | yes | n/a | yes | LOW | yes | none |
| C3 | C1+C2+A-11+A-6 | **no** | Head grammar (R7-class): head lists `A-11`/`A-6` (assumption IDs), not `GT-N`/`Cn` identifiers | yes | LOW | no | none |
| C4 | GT-13?+GT-14?+A-13 | **no** | Head grammar: head lists `A-13`, not a `GT-N`/`Cn` identifier | yes | LOW | no | none |
| C5 | GT-5+GT-6? | yes | n/a | yes | MEDIUM | yes | none |
| C6 | C3+C4+C5+A-7+A-8+A-14 | **no** | Head grammar: head lists `A-7`/`A-8`/`A-14`, not `GT-N`/`Cn` identifiers | yes | LOW | no | none |
| C7 | GT-10+GT-11?+GT-12?+A-15 | **no** | Head grammar: head lists `A-15`, not a `GT-N`/`Cn` identifier | yes | LOW | yes (GT-10) | none |
| C8 | C3+C4+GT-16+C6 | yes | n/a | yes | LOW | no | none |
| C9 | C6+C7 | yes | n/a | yes | LOW | no | none |
| C10 | C6+C7+GT-6?+C8 | yes | n/a | yes | LOW | no | none |
| C11 | C6+C7+C8+C9+C10 | yes | n/a | yes | LOW | no | none |

**Defect found:** four chains (C3, C4, C6, C7) mix assumption identifiers (`A-N`) into the head line alongside `GT-N`/`Cn` identifiers, violating the head grammar even though every one of those assumptions is *also* correctly tagged inline via `[Assumes: A-N]` on the hop that actually uses it (no information is missing — the head line is simply over-inclusive). This is carried into the Self-Audit Gate's Criterion 4 scoring and Fixed there, per the Fix/Repeat loop.

**Table 2 — claim inventory (§6, in order):**

| §6 Span (brief) | Construct | Claim under R11? | R11 clause applied | Chain cited |
|---|---|---|---|---|
| "For a 5 MWh, hours-scale... Li-ion is the economically rational choice" | bold lead-in | yes | bold lead-in whose colon closes the bold span | C11 |
| "...Molten-salt TES becomes the economically rational choice only when duration extends..." | prose (continuation of same lead-in) | yes | direct continuation of the Recommended-approach claim above, same construct | C8, C9 |
| "The TES-vs-Li-ion cost gap...is a round-trip-efficiency and power-block problem" | bold lead-in | yes | bold lead-in whose colon closes the bold span | C11 |
| "TES offers real, non-cost advantages the pure $/kWh comparison does not capture" | bold lead-in | yes | bold lead-in whose colon closes the bold span | C10 |
| "...survives dropping the cost criterion entirely...but the margin...is only 2 points out of ~70" | prose (continuation) | yes | direct continuation of the Trade-offs-acknowledged claim above | C10 |
| "LOW" (Confidence label + Pre-check + paragraph) | bold lead-in | yes | bold lead-in whose colon closes the bold span; citation carried in the paragraph continuing the same construct | C11, C10 |
| Load-bearing assumptions table (6 rows) | prose (table cells) | no | near-paraphrase/supporting detail of the already-cited Confidence claim, not a separate assertion | n/a |
| "Falsification condition: This conclusion is false if..." | bold lead-in | yes | bold lead-in whose colon closes the bold span | C11 |

Scan complete: 11 chain rows, one per section-4 chain block in order; 8 section-6 rows, one per construct in order — 7 claims under R11, 1 excluded. 4 chains malformed, 0 claims untraced.

## Self-Audit Gate (process output)

### Pass 1 (initial scoring)

**Criterion 1: Identify Essence**
Quoted span: "Rebuild, from constituent physical and market unit-costs (not from quoted market-report aggregates), the installed capital cost in $/kWh of a small (5 MWh-thermal) two-tank molten-salt TES system's storage media + tanks + balance-of-plant..."
Band: **Sound**
Justification: the Essence Statement names a specific, non-generic core question and the success criteria are individually precise, but criteria 1-4 test properties of §4 artifacts (chain outputs) rather than being phrased as pass/fail tests directly against the Conclusion section as the Rigorous descriptor requires; only criterion 5 is squarely a Conclusion-section property.

**Criterion 2: Challenge Assumptions**
Quoted span (Assumption Audit scan, addendum rows and §2 table): Verdict cells read "Adopted, disclosed", "Adopted as base case, sensitivity run in C8", "Unverified — flagged (`?`), load-bearing" etc., rather than a leading `Accept` / `Challenge` / `Discard` token.
Band: **Hand-wavy**
Justification: this is a pattern across every row in the table, not an isolated entry — the prescribed Verdict vocabulary (Accept/Challenge/Discard + em-dash + justification) is not followed anywhere, which is the Hand-wavy descriptor's "prescribed structure is not followed" clause, even though every cell is otherwise populated with specific, non-generic content.

**Criterion 3: Establish Ground Truths**
Quoted span (§3): "`?`-marked: GT-1, GT-2, GT-6, GT-7, GT-10a, GT-11, GT-12, GT-13, GT-14 (9 of 17)." Checked against the Ground Truths list itself, the actual `?`-suffixed rows are GT-1, GT-2, GT-6, GT-7, GT-8, GT-9, GT-11, GT-12, GT-13, GT-14, GT-17 — 11 entries, not 9; "GT-10a" does not exist in the list (GT-10 is read-at-source, unsuffixed); GT-8, GT-9, and GT-17 were omitted from the stated enumeration.
Band: **Hand-wavy**
Justification: per the rubric's explicit instruction ("an enumeration that disagrees with the list... bands Hand-wavy"), this enumeration disagrees with the list it summarizes on three IDs and includes one ID that does not exist — a stronger failure than never enumerating at all, since it was checkable and wrong.

**Criterion 4: Reason Upward**
Quoted span (Self-audit scan, Table 1): rows for C3, C4, C6, C7 read "Form conforming? = no; Rule applied = Head grammar: head lists `A-N` (assumption IDs), not `GT-N`/`Cn` identifiers."
Band: **Sound**
Justification: four of eleven chains fail the prescribed head-grammar form (mixing `A-N` assumption identifiers into the head line), but each such chain still names its GT/C inputs correctly alongside the stray `A-N` items, carries a genuine intermediate step, and reaches a conclusion — the "still failing the prescribed form" Sound-band clause applies rather than Hand-wavy, since no chain is missing, no GT-ID is fabricated, and no hop is a non-sequitur.

**Criterion 5: Validate**
Quoted span: chains C3, C6, C7, C8, C9, C10, C11's confidence lines name a downgrade cause (e.g. C6: "[Assumes: A-14]... an unsourced round number") without stating what verification would remove that specific cause as a contributor to the downgrade.
Band: **Sound**
Justification: this is the Sound-band clause "a downgrade cause belonging to its own chain or Conclusion with neither what would remove it... nor a permitted no-path reason" — present on a majority of chains, but every chain's weakest link is still named, every MEDIUM/LOW line does name its `GT-N?`/`Cn` inputs, no chain is rated HIGH while consuming a `GT-N?` input, every chain is capped at or below its cited chains' bands, and the adversarial pass record is complete with all seven parts present (Recompute, Sensitivity, Rival, Premise, Causes, Clusters, Disposition) plus Falsification, each cluster carrying a named disposition.

**Criterion 6: Conclusion-to-Ground-Truth Traceability**
Quoted span (Self-audit scan, Table 2, and closure ledger): all 7 §6 claims cite a chain id inline (C11, C8, C9, C10), and 0 claims are untraced per the closure ledger and the scan's reconciliation line ("7 claims under R11, 1 excluded... 0 claims untraced").
Band: **Rigorous**
Justification: every Conclusion claim traces to a named §4 chain, no new claim is introduced in §6 beyond what the chains established, and the Key Insight ("it is a round-trip-efficiency and power-block problem, not primarily a storage-medium cost problem") is a non-obvious finding distinct from the Recommended Approach's "what to do" statement, not a restatement of it.

**Pass 1 result: 2 criteria scored Hand-wavy (C2, C3) — the hand-wavy cap (at most one) is breached. Revise and re-score once, per the bounded Fix/Repeat loop.**

### Fix

**Fix for Criterion 3 — corrected `?`-marked enumeration (supersedes the erroneous line in §3):**
`?`-marked: GT-1, GT-2, GT-6, GT-7, GT-8, GT-9, GT-11, GT-12, GT-13, GT-14, GT-17 (11 of 17). ("GT-10a" in the original line was a typo with no referent; GT-8, GT-9, and GT-17 were omitted in error. GT-10 itself is correctly unsuffixed — it is read-at-source.) This matches the §3 Ground Truths table exactly, row by row.

**Fix for Criterion 2 — corrected Verdict-cell vocabulary (Accept / Challenge / Discard + justification, replacing the §2/addendum Verdict cells' looser wording):**

| # | Corrected Verdict |
|---|---|
| A-1 | Challenge — this scope framing (electric Carnot-battery, not CSP-fed) is not the only valid one; adopted because it is the only framing that makes the Li-ion comparison meaningful |
| A-2 | Challenge — duration was not specified by the prompt; adopted as a base case and explicitly varied in C8 rather than left as a silent default |
| A-3 | Challenge — two-tank chosen over the cheaper thermocline alternative for being better-documented at full-power cycling duty; the cost trade-off is named, not hidden |
| A-4 | Accept — standard geometric convention; shown not to be sensitive to the headline result (<10% swing across realistic H:D ratios) |
| A-5 | Accept — flagged unverified (`?`-adjacent via GT-8/GT-9), used as a stated fabrication-minimum-thickness estimate |
| A-6 | Accept — flagged unverified, used as the stated 2.0× multiplier; identified as the largest lever on C3 specifically |
| A-7 | Accept — standard CSP tank design-life convention (20yr, 1 cycle/day, 100% DoD) |
| A-8 | Challenge — both discounted and undiscounted LCOS variants are shown rather than one figure picked silently |
| A-9 | Accept — sourced (GT-10, read-at-source), region named explicitly with both global and US figures shown |
| A-10 | Challenge — deliberately the simple/cheap design point against a cited wide literature RTE band (34-80%); not presented as the only achievable RTE |
| A-11 | Accept — flagged unverified, used as the stated BOP aggregate line item |
| A-13 | Accept — flagged unverified, used as the stated power-block integration blend |
| A-14 | Accept — flagged unverified O&M round number (2%/yr) |
| A-15 | Challenge — explicitly flagged as likely understating true Li-ion lifecycle cost (excludes augmentation) |
| A-16 | Challenge — explicitly flagged as a conservative simplification (linear rather than sub-linear scaling) |

At least one assumption is challenged (six are), satisfying the Rigorous floor; every Verdict cell now carries the prescribed leading token.

**Fix for Criterion 4 — corrected chain heads (drop `A-N` identifiers from the head line; the same assumptions remain correctly declared inline via `[Assumes: A-N]` on the hop that uses them, so no information is lost):**
- C3 corrected head: `C1 (salt cost) + C2 (tank shells)`
- C4 corrected head: `GT-13? (turbine-gen $/kW) + GT-14? (heater $/kW)`
- C6 corrected head: `C3 (TES core) + C4 (power block) + C5 (RTE)`
- C7 corrected head: `GT-10 (Li-ion capex) + GT-11? (cycle life) + GT-12? (RTE)`

Re-checking these four chains against the head grammar with the corrected heads: each head now lists only `GT-N`/`Cn` identifiers joined by `+`, the first `→` closes the head, no hop begins with a `GT-N` identifier, and no head or first hop closes its own sentence before the next `→` — all four now conform.

**Fix for Criterion 5 — verification paths for previously-unstated downgrade causes:**
- C3: sourcing an actual small-project EPC/Lang-factor benchmark for a <10 MWh TES skid would remove A-6 as a cause of the downgrade.
- C6: a sourced TES O&M benchmark from an operating molten-salt plant's actual maintenance spend would remove A-14 as a cause.
- C7: a sourced Li-ion augmentation/degradation-cost study would remove A-15 as a cause — and would likely raise, not lower, C7's stated LCOS, reinforcing rather than weakening C11's headline gap.
- C8: an actual multi-duration TES vendor quote set (rather than the A-16 linear-scaling simplification) would remove this cause; the disclosed bias is conservative (probably understates how fast TES improves with duration).
- C9: carries no downgrade cause of its own beyond the cap inherited from C6 — stated explicitly rather than left implicit.
- C10: sourcing the siting/safety and cost-trajectory criterion scores against real insurance-underwriting and cell-price-forecast data, rather than this analysis's own reasoned judgment, would remove this cause.
- C11: carries no downgrade cause of its own beyond the caps inherited from C6/C8/C9/C10; the one substantive lever is RTE (C5/GT-6?), whose own verification path is already stated on C5.

### Pass 2 (re-score, after Fix — bounded to this single re-perception pass)

**Criterion 1: Identify Essence**
Quoted span: (unchanged from Pass 1 — no Fix was applied to §1, since the gap is a structural property of how the success criteria are phrased relative to §6, not a wrong fact to correct)
Band: **Sound**
Justification: unchanged — carried forward as an accepted, disclosed shortfall rather than re-argued; four of five success criteria remain phrased against §4 artifacts rather than directly against §6 properties.

**Criterion 2: Challenge Assumptions**
Quoted span (Fix table above): "A-1 | Challenge — this scope framing... A-8 | Challenge — both discounted and undiscounted LCOS variants are shown..."
Band: **Rigorous**
Justification: every Verdict cell now carries the prescribed leading token (Accept/Challenge/Discard) followed by an em-dash and a specific justification; six assumptions are explicitly Challenged, satisfying the "at least one assumption challenged" floor; Type values remain drawn from the four-type scheme throughout, and unverified assumptions used in chains are marked "unverified — flagged" or carry the `?`.

**Criterion 3: Establish Ground Truths**
Quoted span (Fix above): "`?`-marked: GT-1, GT-2, GT-6, GT-7, GT-8, GT-9, GT-11, GT-12, GT-13, GT-14, GT-17 (11 of 17)." — checked against the §3 table row by row, this now matches exactly.
Band: **Rigorous**
Justification: the enumeration now agrees with the list; GT-IDs are stable and match the identifiers referenced in §4's chains; every GT carries a provenance label and a citation more specific than "common knowledge"; no HIGH-confidence chain exists in this analysis, so the "every unsuffixed GT feeding a HIGH chain names its read-at-source location" clause is vacuously satisfied; no Phase-2-discarded assumption appears in the list.

**Criterion 4: Reason Upward**
Quoted span (Fix above, corrected heads for C3/C4/C6/C7): "C3 corrected head: `C1 (salt cost) + C2 (tank shells)`" etc. — each corrected head now contains only `GT-N`/`Cn` identifiers.
Band: **Rigorous**
Justification: with the four corrected heads, all eleven chains now conform to the prescribed head-plus-arrow-led form; every chain has at least one genuine intermediate step; the Abandoned Reasoning section documents four dead ends with the What-was-tried/Why-abandoned/What-it-ruled-out structure; no analogy is used as direct evidence anywhere (every cross-technology or cross-scale comparison is grounded in a named GT — e.g. GT-17 for the utility-CSP cross-check, GT-10 for Li-ion pricing); every chain step introducing a new assumption declares it inline via `[Assumes: A-N]` (confirmed exhaustively by the Assumption Audit scan); the adversarial pass's Recompute step independently reverified every computed figure in §4 and found no arithmetic errors.

**Criterion 5: Validate**
Quoted span (Fix above): "C6: a sourced TES O&M benchmark... would remove A-14 as a cause. C7: a sourced Li-ion augmentation/degradation-cost study would remove A-15 as a cause..."
Band: **Rigorous**
Justification: every MEDIUM/LOW confidence line now names both its `GT-N?`/`Cn` inputs and what would remove its own chain's downgrade cause (or states explicitly that it carries no independent cause beyond an inherited cap, for C9 and C11); no chain is rated HIGH while consuming a `GT-N?` input; every chain is rated no higher than the lowest-rated chain its head cites (confirmed in the Self-audit scan's Band column); the adversarial pass record is complete across all seven parts plus Falsification, and every cluster in it carries a named disposition (plan change or accepted-risk-with-mitigation) — none left as a bare risk list.

**Criterion 6: Conclusion-to-Ground-Truth Traceability**
Band: **Rigorous** (unchanged from Pass 1 — no defect found, no Fix needed)

### Gate result

Pass 2 tally: Rigorous ×4 (Criteria 2, 3, 4, 5), Rigorous ×1 (Criterion 6), Sound ×1 (Criterion 1). **No criterion scores Absent. At most one criterion (Criterion 1) scores Hand-wavy — in fact zero score Hand-wavy after the fix, which is stronger than the cap requires.** Both gate conditions are cleared: **the analysis passes the Self-Audit Gate.**
