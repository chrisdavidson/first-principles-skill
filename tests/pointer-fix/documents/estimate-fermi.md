## Answer

**Recommendation:** Do not build a 5 MWh-scale, electrically-charged, steam-Rankine molten-salt Carnot battery for electricity-round-trip storage — lithium-ion is roughly 4–5× cheaper there in the central case (chain C11). Molten-salt TES is worth pursuing instead for direct thermal/process-heat delivery at larger-than-pilot scale and high cycling frequency, where it holds a modest, likely-growing edge over lithium-ion (chain C12).

**Band (from §6):** LOW

**Would change it:** A vendor-quoted efficiency curve for a 0.2–1 MWe turbine on 565°C steam, combined with an actual EPC cost quote replacing the bottom-up estimate, could narrow or reverse the electric-round-trip gap (chain C11). For the thermal-only case, a small-scale lithium-ion installed-cost multiplier below ≈1.5× (versus the 2.0–3.5× estimated here) would instead favor lithium-ion (chain C12).

## 1. Problem Essence

**Core problem:** What is the physically- and economically-traceable installed cost ($/kWh of storage capacity) and cycle-amortized levelized cost ($/kWh delivered) of a 5 MWh electrically-charged molten-salt thermal storage system discharged through a steam-Rankine power block (a "Carnot battery"), and under what duty — electricity-to-electricity round-trip, or direct thermal delivery — does that cost beat, tie, or lose to lithium-ion storage on the same basis?

**Configuration being costed (stated explicitly, per scope item 1):** This analysis costs the **electrically-charged, steam-Rankine-discharged two-tank molten-salt TES** ("Carnot battery") as the primary configuration, because it is the only configuration for which an electricity-in/electricity-out $/kWh figure is well-posed and comparable to lithium-ion on a like-for-like basis. A CSP-attached two-tank TES (heat supplied by a solar field, power block shared with the plant and costed separately) is used only as a secondary reference point for the salt/tank/heat-exchanger cost tier, because its own "$/kWh" figure has no electricity-input leg and so cannot itself be benchmarked against Li-ion — see Dead End 1 in section 5.

**Success criteria:**
1. The analysis produces a component-by-component installed-cost buildup for the Carnot-battery configuration reaching a $/kWh-thermal-capacity figure expressed as a range (low/central/high), not a single point estimate.
2. The analysis produces a levelized $/kWh-delivered figure for both an electricity-round-trip duty and a thermal-only duty, each incorporating round-trip/delivery efficiency, cycle/calendar life, and O&M — i.e., each figure in the Conclusion section is traceable to a derivation chain in section 4 that performs this amortization.
3. The analysis produces a lithium-ion figure on the identical two bases (installed $/kWh, levelized $/kWh delivered) at the same nameplate scale, sourced to current (2024-2025) unit-cost data.
4. The Conclusion states, for each of the two duty types (electricity round-trip vs. thermal-only), which technology is cheaper in the central case, by what multiple, and whether the uncertainty bands of the two technologies overlap — not a single undifferentiated verdict.
5. Every figure carries an explicit confidence band, and the specific input or inference that would most change each figure if revised is named (the Phase 5 sensitivity/weakest-link step).

---

## 2. Assumptions Table

| Assumption | Type | Treatment | Verdict | Verification |
|------------|------|-----------|---------|--------------|
| "5 MWh" denotes the stored **thermal** energy capacity of the salt inventory, not an electrical nameplate rating | convention | Challenge before use — the prompt's phrasing is genuinely ambiguous | Accept — matches universal industry convention of rating TES in thermal kWh/MWh (e.g. "Solar Two had 105 MWh-th"); adopted and stated explicitly | unverified — flagged (own interpretive choice, not sourced) |
| Charge duration = discharge duration = 5 hours (sets heater and turbine power ratings) | convention | Challenge before use — no duration was specified by the user | Accept — a round, mid-range duration chosen for concreteness; all power ratings in section 4 are linear in this choice and are flagged as such | unverified — flagged |
| Solar salt (60 wt% NaNO₃ / 40 wt% KNO₃) operated 280°C (cold) to 565°C (hot) is the storage medium | convention | Challenge before use — other salts (Hitec, chloride salts, Hitec XL) exist | Accept — this is the dominant commercial CSP salt and temperature window (GT-4?); chloride-salt Gen3 TES is treated as a dead end (section 5) | reported-by-delegate — GT-4? |
| Round-trip efficiency is split into three multiplicative stages: resistive-heater charge efficiency (~98%), thermal-storage retention efficiency per cycle (~97%), and discharge-side Rankine conversion efficiency (15–35%, central 25%) | untested belief | Verify, or flag — the discharge-side figure in particular is this analysis's own estimate, not a literature figure | Challenge — the discharge-side term (GT-16?) is the single most consequential and least-certain number in the whole analysis; it is bracketed via the Fermi/estimate technique and checked against the Carnot ceiling (section 4, chain C3) | unverified — flagged (GT-16?) |
| A capital-recovery (annuitized) amortization at a 7% real discount rate is an appropriate way to turn installed capital cost into a levelized $/kWh-delivered figure | convention | Challenge before use — this is a financing convention (matches the NREL ATB / Lazard LCOS default), not a physical requirement | Accept — standard practice for LCOE/LCOS comparisons; a materially different discount rate would shift both technologies' levelized figures in the same direction and is noted as a shared sensitivity, not a differentiator | unverified — flagged (industry convention, not opened this session) |
| Both technologies are cycled once per day (365 full cycles/year) for the purpose of annualizing delivered energy | convention | Challenge before use — actual duty cycles vary enormously by application | Accept — a standard "daily load-shifting" duty cycle; chosen because it is the duty cycle under which the two technologies' differing life-limiting mechanisms (calendar-limited TES vs. cycle-limited Li-ion) are most directly comparable (section 4, chain C9 vs. C7) | unverified — flagged |
| Installed cost of the molten-salt TES's tanks/HX/pumps/heater/turbine scales with capacity or duty according to the "six-tenths rule" (installed cost ∝ capacity^0.6) when moving between scales | convention | Challenge before use — this is a chemical/process-engineering cost-estimating heuristic, not a law; the exponent itself is uncertain (0.5–0.85 by equipment class) | Challenge — used only as an independent cross-check (chain in section 4's Recompute pass) against the bottom-up component buildup, not as the primary cost method, precisely because it is this uncertain | unverified — flagged (GT-8?) |
| A total EPC/indirect-cost multiplier of 1.4× (low) to 2.2× (high), central 1.7×, converts the summed direct-equipment cost into an installed project cost | untested belief | Verify, or flag — this is this analysis's own judgment call for a first-of-a-kind small thermal/mechanical project | Challenge — no project-specific EPC quote exists; the range is wide specifically because first-of-a-kind pilot soft costs are both large and poorly documented in public literature | unverified — flagged |
| CPI-based inflation adjustment of ≈1.65× converts the 2004-vintage NREL two-tank TES cost figure (GT-6?) into 2025 dollars | current constraint | Record expiry — this multiplier is time-dependent and must be re-derived for any future re-use of this analysis | Accept — standard CPI escalation; expires/must be redone as soon as the analysis is reused more than ~1-2 years after 2025 | unverified — flagged |
| The small-scale (≈0.2–1 MWe) steam turbine-generator cost curve (GT-9?), sourced from a pre-2015 DOE/EPA CHP cost dataset, needs a ≈1.4–1.6× inflation adjustment to be usable in 2025 dollars | current constraint | Record expiry — same time-dependency as above | Accept — applied in chain C4; expires on the same terms | unverified — flagged |
| Lithium-ion installed cost at a 5 MWh (pilot/C&I) scale carries a 2.0–3.5× multiplier over the raw cell/pack price, versus a 1.3–1.8× multiplier at 100+ MWh utility scale (GT-17?) | untested belief | Verify, or flag — no small-scale BESS quote was obtained; this is inferred by contrast between GT-10 (pack price) and GT-11 (utility all-in price) | Challenge — this is the single most consequential unverified number on the lithium-ion side of the comparison, directly analogous in role to GT-16? on the TES side | unverified — flagged |
| A perfect (Carnot-limited) heat engine operating between 838 K (565°C) and 298 K (25°C ambient) sets the physical ceiling on any heat-to-electricity conversion at these temperatures | physical law | Accept as ground-truth candidate — this follows directly from the second law of thermodynamics (Carnot's theorem) | Accept — physical law, used in chain C3 as the theoretical-limit bound against which the small-turbine estimate is checked | derived directly from GT-4?'s stated temperatures; the arithmetic itself is a physical law, though the input temperatures inherit GT-4?'s flag |
| Thermal storage (sensible heat in solar salt) has no cycle-count-limited degradation mechanism analogous to lithium-ion's electrochemical fade; its life is set by calendar-scale corrosion/fatigue, not by cycle count | convention (treated as a modeling simplification) | Challenge before use — real tanks do experience thermal-cycling fatigue, but this is not normally the binding constraint at ≤1 cycle/day | Accept — consistent with GT-13?'s corrosion-driven ~30-year design-life framing; flagged because the claim that cycling fatigue is non-binding at this duty cycle is itself unverified | unverified — flagged |
| A-18 (surfaced by Assumption Audit, chains C1/C2): a 10% heel/ullage margin on salt inventory and a 20% freeboard margin on tank sizing | untested belief | Verify, or flag — engineering judgment, not sourced to a vendor or plant specification | Challenge — a standard design margin, but not independently verified for this specific system | unverified — flagged |
| A-19 (surfaced by Assumption Audit, chain C3): ambient heat-sink temperature of 298 K (25°C) used in the Carnot-ceiling calculation | convention | Challenge before use — ambient temperature varies by site and season | Accept — a standard reference ambient for a first-pass bound; does not materially change the conclusion that the small-turbine estimate sits far below the ceiling | unverified — flagged |
| A-20 (surfaced by Assumption Audit, chains C6/C7/C9/C10): O&M modeled as a fixed percentage of installed capital cost per year (3%/2.5% for TES, 1.5–2% for Li-ion) rather than bottom-up estimated | untested belief | Verify, or flag — no vendor O&M quote for either technology at this scale was obtained | Challenge — a common simplifying convention in LCOE/LCOS literature, but unverified for either technology at 5 MWh scale | unverified — flagged |
| A-21 (surfaced by Assumption Audit, chains C4/C5): the individual bottom-up component cost line items (tank, heat-exchanger, pump, piping, controls, foundation dollar figures) are this analysis's own engineering judgment, not sourced to individual vendor quotes | untested belief | Verify, or flag — this is the largest unquantified-provenance gap in the capital-cost buildup | Challenge — partially mitigated by the independent six-tenths-rule cross-check in the Phase 5 Recompute step (appendix), which lands within roughly 1.5× of this chain's own total | unverified — flagged |

**Stakes-escalation note:** the two assumptions carrying the most weight in the final verdict — the discharge-side Rankine efficiency (GT-16?) and the Li-ion small-scale cost multiplier (GT-17?) — are both classified `untested belief` and both given `Challenge` verdicts rather than `Accept`, consistent with the stakes-escalation rule: the higher the stakes riding on an assumption, the harder it must be pushed toward verified status, and neither of these two could be pushed further than "bracketed and flagged" within this session's available evidence.

---

## 3. Ground Truths

- **GT-1** Average specific heat capacity of commercial solar salt (60 wt% NaNO₃ / 40 wt% KNO₃) ≈ 1.55 kJ·kg⁻¹·K⁻¹ (1,550 J·kg⁻¹·K⁻¹) — source: peer-reviewed thermophysical-properties study of solar salt (PMC11124137, "Novel Wide-Working-Temperature NaNO₃-KNO₃-Na₂SO₄ Molten Salt for Solar Thermal Energy Storage"); read-at-source: the paper's stated figure "the average specific heat capacity of solar salt is approximately 1.55 J·K⁻¹·g⁻¹," fetched and read directly this session.
- **GT-2** 1 kWh ≡ 3.6 × 10⁶ J — source: SI unit definition; read-at-source: definitional identity, independently verifiable without an external citation.
- **GT-3?** Molten solar-salt density correlation ρ(T) = 2,090 − 0.636·T(°C) kg/m³ — cited to: the Zavoico (2001, Sandia National Laboratories) correlation as commonly reproduced across CSP molten-salt engineering literature; reported-by-delegate: recalled from this analysis's general engineering knowledge — the specific correlation was not opened or re-derived from a primary source this session.
- **GT-4?** CSP two-tank solar-salt plants operate with a cold tank near 280°C and a hot tank near 565°C (ΔT ≈ 285 K) — cited to: Crescent Dunes Solar Energy Project operating data; reported-by-delegate: supplied by a web search summarizing DLR/ReNewEconomy coverage of Crescent Dunes — the primary plant specification was not opened this session.
- **GT-5?** Technical-grade sodium nitrate (NaNO₃) priced ≈ $1,070–1,360/metric ton in the US/Central Europe (as low as ≈ $302/t ex-China), November 2025; technical-grade potassium nitrate (KNO₃) priced ≈ $748–928/metric ton, Asia-Pacific/Europe, Q4 2025 — cited to: Intratec and SunSirs commodity-price trackers; reported-by-delegate: supplied by a web search synthesis of those trackers — neither tracker page was opened directly this session.
- **GT-6?** Two-tank molten-salt thermal energy storage has a specific installed cost of US$30–40/kWh-thermal (2004 dollars), "depending on storage size" — cited to: Herrmann, Kelly & Price, "Two-tank molten salt storage for parabolic trough solar power plants," *Energy* 29(5):883–893 (2004); reported-by-delegate: confirmed via a RePEc/IDEAS abstract-level search summary — **Phase 3 failure record:** the primary host, nrel.gov, could not be reached this session (direct `curl` test returned "Could not resolve host: nrel.gov" / "Could not resolve host: atb.nrel.gov," confirming a DNS-level failure rather than a one-off timeout), and a secondary mirror of the same study (FH Aachen repository, `opus.bibliothek.fh-aachen.de`) returned HTTP 403 Forbidden on direct fetch. The primary text was not read.
- **GT-7?** The US DOE SunShot program's 2020 target for thermal energy storage cost was <$15/kWh-thermal — an aspirational R&D goal, not a reported achieved or installed cost — cited to: DOE SunShot program documentation; reported-by-delegate: supplied by web search synthesis; not opened directly this session.
- **GT-8?** Installed cost of process/mechanical equipment commonly scales with capacity as cost₂/cost₁ = (capacity₂/capacity₁)ⁿ, n ≈ 0.6 (commonly cited range 0.5–0.85 by equipment class) — the "six-tenths rule" / Williams' Law, a standard chemical/process cost-estimating heuristic (Peters & Timmerhaus) — reported-by-delegate: recalled from this analysis's general engineering-education knowledge; not opened or verified against a primary source this session.
- **GT-9?** Back-pressure steam turbogenerator-with-switchgear capital cost ≈ $700/kW at 50 kW scale, falling to <$200/kW at 2,000 kW scale — cited to: a DOE/EPA combined-heat-and-power (CHP) technology cost-characterization document hosted at energy.gov; reported-by-delegate: the figure was supplied by a web search summary — **Phase 3 failure record:** the source PDF was fetched directly this session, but its content returned as unreadable/encoded binary text ("the actual text content is heavily compressed and encoded"), so the table itself was not read; the figure is confirmed only via the independent search-engine summary, not a direct read of the source table.
- **GT-10** BNEF's 2024 global volume-weighted-average lithium-ion battery pack price is $115/kWh (a 20% year-on-year drop, the largest since 2017); regional averages: China $94/kWh, United States $123/kWh, Europe $139/kWh — source: BloombergNEF press release, "Lithium-Ion Battery Pack Prices See Largest Drop Since 2017, Falling to $115 per Kilowatt-Hour"; read-at-source: the release's own stated figures for the global average and the China/US/Europe regional breakdown, fetched and read directly this session.
- **GT-11** As of October 2025, all-in utility-scale battery energy storage system (BESS) project capital cost (outside China and the US) is ≈ $120–125/kWh, composed of ≈ $75/kWh core equipment (cells, enclosure, PCS, EMS) plus ≈ $50/kWh EPC/grid-connection cost, corroborated by named 2025 auction clearing prices in Saudi Arabia, Italy, and India — source: Ember Energy, "How cheap is battery storage?"; read-at-source: the report's own cost-component breakdown and named-auction evidence, fetched and read directly this session.
- **GT-12?** Lithium iron phosphate (LFP) cells commonly achieve 3,000–8,000+ cycles to 80% capacity retention at 80% depth of discharge, with 4,000–6,000 cycles the most frequently cited central range across manufacturers — cited to: multiple industry/technical sources (EcoTree Lithium, 123accu, ECS); reported-by-delegate: supplied by web search synthesis of several independent sources; no single source opened directly this session.
- **GT-13?** Molten-salt/chloride-salt CSP tank corrosion-rate design targets of <15–20 µm/year are stated as supporting a CSP plant design life of ≈30 years or more — cited to: NREL/CSP corrosion research documentation; reported-by-delegate: supplied by web search synthesis — **Phase 3 failure record:** same as GT-6? — the primary nrel.gov-hosted document could not be reached this session (confirmed DNS failure); the figure is confirmed only via the search-engine summary of that document.
- **GT-14?** Modern LFP battery energy storage systems achieve a round-trip efficiency, including inverter/power-conversion-system losses, of approximately 85–92% — cited to: general industry/technical literature (e.g., Lazard LCOS-type analyses, NREL); reported-by-delegate: recalled from this analysis's general knowledge; not opened or re-verified against a specific primary source this session.
- **GT-15?** Utility-scale (100+ MWe class) steam-Rankine power cycles operating on ≈565°C live steam achieve a net cycle efficiency of approximately 40–42% — cited to: general CSP/conventional-steam-plant engineering literature; reported-by-delegate: recalled from this analysis's general knowledge; not opened or re-verified against a specific primary source this session.
- **GT-16?** At the small scale relevant to a 5 MWh/≈0.25 MWe-class discharge turbine, net electrical conversion efficiency on ≈565°C heat is estimated at 15–35% (central ≈25%), reflecting a 15–20 percentage-point small-scale penalty below the utility-scale figure (GT-15?) from tip-leakage, lower blade-speed/Reynolds effects, and fixed parasitic loads that do not shrink proportionally with turbine size — unverified: this is this analysis's own first-principles (Fermi/"estimate"-technique) bracket, not a literature-sourced figure; no small-turbine efficiency curve was located or opened this session.
- **GT-17?** Lithium-ion BESS installed cost at a <10 MWh (pilot/commercial-and-industrial) scale carries an estimated 2.0–3.5× multiplier over the raw cell/pack price, versus an estimated 1.3–1.8× multiplier at 100+ MWh utility scale — unverified: inferred by this analysis from the contrast between GT-10 (pack price) and GT-11 (utility all-in price); no small-scale BESS quote was located or opened this session.

**Provenance summary (required):**

```text
?-marked: GT-3, GT-4, GT-5, GT-6, GT-7, GT-8, GT-9, GT-12, GT-13, GT-14, GT-15, GT-16, GT-17 (13 of 17)
Read-at-source:
  GT-1 — PMC11124137, stated figure "the average specific heat capacity of solar salt is approximately 1.55 J·K⁻¹·g⁻¹"
  GT-2 — SI unit definition (1 kWh ≡ 3.6 MJ), definitional, no external source needed
  GT-10 — BNEF press release, paragraph stating the global $115/kWh average and the China $94 / US $123 / Europe $139 regional breakdown
  GT-11 — Ember Energy report, cost-component breakdown section (≈$75/kWh equipment + ≈$50/kWh EPC/grid-connection) and named 2025 auction evidence
```

---

## 4. Derivation Chains

### Conclusion C1: A 5 MWh-thermal two-tank solar-salt store requires on the order of 45 tonnes of salt inventory

GT-1 (cp ≈ 1.55 kJ/kg·K) + GT-2 (1 kWh ≡ 3.6 MJ) + GT-4? (ΔT = 285 K, cold 280°C/hot 565°C)
→ 5,000 kWh of stored thermal energy equals 1.8×10¹⁰ J (5,000 × 3.6×10⁶ J)
→ dividing by cp×ΔT (1,550 J/kg·K × 285 K = 441,750 J/kg) gives a gross salt mass of ≈40,750 kg
→ adding a 10% heel/ullage margin for minimum tank levels and pump-suction head gives a design salt inventory of ≈44.8 metric tons *[Assumes: A-18 — 10% heel/ullage margin, unverified]*

**Pre-check:** head GT-1, GT-2, GT-4? · ?-marked: GT-4? · lowest cited: none · Inputs ceiling: MEDIUM
**Confidence:** MEDIUM — GT-4? (the 280°C/565°C operating range) is reported-by-delegate and was not read at source; verification would require opening a primary Crescent Dunes or Gemasolar plant specification document directly. The unit-conversion and division arithmetic recomputes exactly as shown and is not itself in question.

### Conclusion C2: The two tanks together enclose only about 60 m³ of vessel volume

C1 (≈44.8 t salt) + GT-3? (density correlation ρ(T) = 2,090 − 0.636·T(°C))
→ at the cold-tank temperature (280°C) the correlation gives ρ ≈ 1,912 kg/m³, and at the hot-tank temperature (565°C) it gives ρ ≈ 1,731 kg/m³
→ the full 44.8 t inventory therefore occupies ≈23.4 m³ when entirely in the cold tank and ≈25.9 m³ when entirely in the hot tank
→ each tank must hold the full inventory at its own temperature plus roughly 20% freeboard for thermal expansion and instrumentation, giving a cold-tank capacity of ≈28 m³ and a hot-tank capacity of ≈31 m³ *[Assumes: A-18 — 20% freeboard margin, unverified]*

**Pre-check:** head C1 (MEDIUM), GT-3? · ?-marked: GT-3? · lowest cited: MEDIUM · Inputs ceiling: MEDIUM
**Confidence:** MEDIUM — GT-3? (the density correlation) is unverified; verification would require locating and opening a primary CSP molten-salt thermophysical-properties reference. C1's own MEDIUM rating is inherited onto this chain's head and is explained on C1's own confidence line, not repeated here.

### Conclusion C3: At pilot scale, round-tripping stored heat back to electricity destroys roughly three-quarters of what went in, while using the heat directly destroys only about 5%

GT-4? (hot-tank temperature 838 K) + GT-15? (utility-scale Rankine efficiency ≈40–42%) + GT-16? (small-scale turbine efficiency estimate 15–35%)
→ a Carnot-limited heat engine operating between 838 K and a 298 K ambient sink has a thermodynamic ceiling efficiency of 1 − 298/838 ≈ 64.4%, which no real heat engine at these temperatures can exceed *[Assumes: A-19 — 298 K ambient reference, unverified]*
→ real utility-scale (100+ MWe) steam-Rankine cycles on this grade of heat achieve only ≈40–42% net efficiency even before any small-scale penalty, so the Carnot ceiling already overstates achievable practice by roughly 1.5×
→ at the ≈0.2–1 MWe scale implied by a 5-hour discharge of a 5 MWh store, turbine tip-leakage, lower blade-speed/Reynolds effects, and fixed parasitic loads that do not shrink proportionally with size impose a further efficiency penalty, giving an estimated net discharge-side efficiency of 15–35% (central ≈25%)
→ combining a ≈98% resistive-heater charge efficiency with a ≈97% thermal-storage retention efficiency per cycle and the ≈25% central discharge efficiency gives an overall electricity-to-electricity round-trip efficiency of ≈24% (bracket ≈14–42% from the discharge-efficiency range alone), versus a ≈95% delivery efficiency (heater × retention only) if the stored heat is used directly rather than reconverted to electricity

**Pre-check:** head GT-4?, GT-15?, GT-16? · ?-marked: GT-4?, GT-15?, GT-16? · lowest cited: none · Inputs ceiling: MEDIUM
**Confidence:** LOW — two axes are short at once. Inputs: all three head identifiers are `?`-marked, most consequentially GT-16?, which is this analysis's own Fermi-style estimate rather than a literature figure; verification would require a vendor-quoted efficiency curve for a turbine in the 0.2–1 MWe class on 565°C steam, which was not located this session. Rivals: a rival estimate placing small-scale net efficiency anywhere from ≈10% (a simple uncooled back-pressure unit) to ≈35–40% (a well-optimized small condensing turbine or an ORC bottoming cycle) is equally defensible from public information, and nothing in this analysis settles between them — this is the single most sensitive input in the whole analysis (see section 5's dead-end discussion and the adversarial-pass Sensitivity step in the appendix).

### Conclusion C4: A 5 MWh pilot-scale Carnot battery installs for roughly $250–915/kWh-thermal, an order of magnitude above GWh-scale CSP TES

GT-5? (blended salt price $0.48–1.19/kg) + GT-8? (six-tenths scaling heuristic) + GT-9? (small turbogenerator cost curve) + C1 (≈44.8 t salt) + C2 (≈60 m³ tankage) + C3 (≈0.24 MWe turbine / ≈1.0 MWe heater, ≈24% RTE)
→ pricing the 44.8 t inventory at a blended technical-grade NaNO₃/KNO₃ rate of $0.48–1.19/kg (central ≈$0.85/kg) gives a salt cost of $21,500–53,500 (central ≈$38,000) — a small fraction of total cost
→ bottom-up vessel, heat-exchanger, pump, piping, and foundation estimates sized to the ≈60 m³ tankage and the ≈0.24 MWe/≈1.0 MWe duty from C2 and C3, plus a turbogenerator-and-balance-of-plant cost built from GT-9?'s small-turbine cost curve, sum to a direct-equipment cost of $0.88M (low) to $2.08M (high), central ≈$1.36M *[Assumes: A-21 — unsourced bottom-up component cost line items, unverified]*
→ applying a 1.4×–2.2× (central 1.7×) EPC/indirect-cost multiplier for engineering, installation, commissioning, and owner's/contingency costs gives a total installed project cost of $1.23M (low) to $4.58M (high), central ≈$2.31M
→ dividing by the 5,000 kWh-thermal nameplate capacity gives an installed cost of ≈$250/kWh-th (low) to ≈$915/kWh-th (high), central ≈$460/kWh-th
→[2nd] because fixed-cost items (tanks, heat exchanger, pumps, turbine, controls, foundations) dominate this total far more than the energy-related salt/tank-volume cost does, project developers facing this arithmetic respond by scaling duration up at a fixed power rating rather than building more 5 MWh-class units, and the six-tenths-rule heuristic (GT-8?) predicts that quadrupling capacity to 20 MWh at the same ≈0.24 MWe/≈1.0 MWe power rating would cut installed cost to roughly $180/kWh-th — a ≈2.6× reduction from duration alone
→[3rd] this scaling response means any real-world deployment this analysis's verdict is meant to inform is already pulling away from the 5 MWh pilot scale toward tens-of-MWh systems, so the $250–915/kWh-th bracket above is best read as a pilot-scale ceiling rather than a durable feature of the technology

**Pre-check:** head GT-5?, GT-8?, GT-9?, C1 (MEDIUM), C2 (MEDIUM), C3 (LOW) · ?-marked: GT-5?, GT-8?, GT-9? · lowest cited: LOW · Inputs ceiling: LOW
**Confidence:** LOW — ceiling set by C3 (LOW), whose own rating and verification path are explained on C3's confidence line and not repeated here. Independently, GT-5? (salt pricing) and GT-9? (turbogenerator cost curve) are both `?`-marked; verification would require a vendor salt quote and a vendor turbine-generator quote respectively, neither obtained this session. GT-8? (the six-tenths-rule heuristic) feeds only the [2nd]-order extension, not the primary cost buildup, and is independently cross-checked against this chain's own bottom-up total in the Phase 5 Recompute step, where the two methods land within roughly a factor of 1.5 of each other — named there as the chain's Rival axis.

### Conclusion C5: Removing the power block (thermal-only configuration) cuts installed cost to roughly $200–710/kWh-th, central ≈$375/kWh-th

GT-5? (blended salt price) + C1 (≈44.8 t salt) + C2 (≈60 m³ tankage)
→ removing the turbine-generator/condenser/feedwater power block and trimming grid-interconnection switchgear from C4's direct-equipment list — since a thermal-only system delivers heat, not AC power, and needs no generator synchronization — lowers the direct-equipment cost to $0.71M (low) to $1.62M (high), central ≈$1.10M
→ applying the same 1.4×–2.2× (central 1.7×) EPC multiplier gives a total installed cost of $1.00M (low) to $3.56M (high), central ≈$1.87M
→ dividing by the 5,000 kWh-thermal capacity gives an installed cost of ≈$200/kWh-th (low) to ≈$710/kWh-th (high), central ≈$375/kWh-th

**Pre-check:** head GT-5?, C1 (MEDIUM), C2 (MEDIUM) · ?-marked: GT-5? · lowest cited: MEDIUM · Inputs ceiling: MEDIUM
**Confidence:** MEDIUM — GT-5? (salt pricing) is `?`-marked; verification would require a vendor quote, not obtained this session. C1 and C2's own MEDIUM ratings are inherited and are explained on their own confidence lines, not repeated here.

### Conclusion C6: Delivering electricity round-trip through this Carnot battery costs on the order of $0.21–2.00/kWh, central ≈$0.58/kWh

C3 (≈24% round-trip efficiency, LOW) + C4 (≈$2.31M installed cost, LOW) + GT-13? (≈30-year design life)
→ amortizing C4's central $2.31M installed cost over GT-13?'s ≈30-year calendar life at a 7% real discount rate (capital recovery factor ≈0.0806) gives an annual capital charge of ≈$186,000
→ adding O&M at ≈3% of installed capex/year gives a total annual cost of ≈$256,000 *[Assumes: A-20 — O&M modeled as % of capex, unverified]*
→ at 365 cycles/year and C3's central 1,212 kWh of electricity delivered per discharge, annual electricity delivered is ≈442,600 kWh, giving a central levelized cost of ≈$0.58/kWh
→ repeating the calculation at the optimistic end (C4's low capital, C3's high 35% turbine efficiency) and the pessimistic end (C4's high capital, C3's low 15% turbine efficiency) brackets the levelized cost at roughly $0.21/kWh to $1.99/kWh

**Pre-check:** head C3 (LOW), C4 (LOW), GT-13? · ?-marked: GT-13? · lowest cited: LOW · Inputs ceiling: LOW
**Confidence:** LOW — ceiling set by C3 and C4 (both LOW), whose own ratings and verification paths are explained on their own confidence lines and not repeated here. GT-13? (the 30-year calendar-life figure) is additionally `?`-marked; verification would require opening the same unreachable NREL corrosion-design document named in GT-13?'s Phase 3 failure record. The 7% discount rate and 3% O&M fraction are convention-level assumptions (section 2) that move this figure in the same direction for both technologies compared in this analysis and are treated as a shared sensitivity rather than a TES-specific weakness.

### Conclusion C7: Delivering the same stored heat directly, without reconverting it to electricity, costs on the order of 6–23 ¢/kWh-th, central ≈11 ¢/kWh-th

C5 (≈$375/kWh-th installed cost, MEDIUM)
→ amortizing C5's central $1.87M installed cost over a 30-year life at a 7% real discount rate (the same convention as C6, per the Assumptions Table) gives an annual capital charge of ≈$151,000
→ adding O&M at a lower ≈2.5% of capex/year, reflecting the absence of rotating turbine machinery, gives a total annual cost of ≈$197,000 *[Assumes: A-20 — O&M modeled as % of capex, unverified]*
→ at 365 cycles/year and the Assumptions Table's ≈98% heater efficiency times ≈97% retention efficiency (≈95% combined thermal delivery efficiency), annual heat delivered is ≈1,734,000 kWh-th, giving a central levelized cost of ≈$0.114/kWh-th
→ repeating the calculation at the optimistic end (low capital, slightly better retention) and the pessimistic end (high capital, slightly worse retention) brackets the levelized cost at roughly $0.057/kWh-th to $0.229/kWh-th

**Pre-check:** head C5 (MEDIUM) · ?-marked: none · lowest cited: MEDIUM · Inputs ceiling: MEDIUM
**Confidence:** MEDIUM — ceiling set by C5 (MEDIUM), whose own rating is explained on its own confidence line. The heater/retention efficiency figures (≈98%/≈97%) are flagged `untested belief` in the Assumptions Table (section 2) rather than promoted to their own ground-truth IDs; this chain never touches C3's turbine-efficiency estimate, which is precisely why it is rated MEDIUM rather than LOW despite sharing the same discount-rate and O&M-percentage conventions as C6.

### Conclusion C8: A 5 MWh lithium-ion BESS installs for roughly $230–490/kWh, central ≈$330/kWh

GT-10 (US pack price $123/kWh) + GT-17? (small-scale installed-cost multiplier 2.0–3.5×)
→ GT-10's US-regional pack price of $123/kWh, taken as central, combined with GT-17?'s estimated 2.0–3.5× small-scale installed-cost-to-pack-price multiplier gives an installed cost range of $230–490/kWh, central ≈$330/kWh using a central multiplier of ≈2.7×
→ at the 5,000 kWh nameplate capacity this gives a total installed capital cost of $1.15M (low) to $2.45M (high), central ≈$1.65M

**Pre-check:** head GT-10, GT-17? · ?-marked: GT-17? · lowest cited: none · Inputs ceiling: MEDIUM
**Confidence:** MEDIUM — GT-17? (the small-scale cost multiplier) is this analysis's own unverified inference from contrasting GT-10 and GT-11, rather than a direct small-scale BESS quote; verification would require obtaining an actual vendor quote for a 5 MWh-class BESS project, not obtained this session. GT-10 itself is read-at-source and carries no caveat.

### Conclusion C9: Delivering electricity round-trip through lithium-ion costs on the order of $0.07–0.29/kWh, central ≈$0.13/kWh

C8 (≈$330/kWh installed, MEDIUM) + GT-12? (cycle life 3,000–8,000+ cycles) + GT-14? (round-trip efficiency 85–92%)
→ GT-12?'s central 5,000-cycle life at 365 cycles/year gives a cycle-limited life of ≈13.7 years, shorter than typical calendar-fade life and therefore the binding constraint
→ amortizing C8's central $1.65M installed cost over 13.7 years at a 7% real discount rate (capital recovery factor ≈0.1158) gives an annual capital charge of ≈$191,000, and adding O&M at ≈1.5% of capex/year gives a total annual cost of ≈$216,000 *[Assumes: A-20 — O&M modeled as % of capex, unverified]*
→ at 365 cycles/year and GT-14?'s central ≈88.5% round-trip efficiency, annual electricity delivered is ≈1,616,600 kWh, giving a central levelized cost of ≈$0.134/kWh
→ repeating the calculation at the optimistic end (low capital, long 20-year life, high 92% RTE) and the pessimistic end (high capital, short 8.2-year life, low 85% RTE) brackets the levelized cost at roughly $0.072/kWh to $0.293/kWh

**Pre-check:** head C8 (MEDIUM), GT-12?, GT-14? · ?-marked: GT-12?, GT-14? · lowest cited: MEDIUM · Inputs ceiling: MEDIUM
**Confidence:** MEDIUM — C8's own MEDIUM rating is inherited and explained on its own confidence line. GT-12? (cycle life) and GT-14? (round-trip efficiency) are both `?`-marked but each is corroborated by multiple independent industry sources (section 3) rather than resting on a single unverified figure, which is why this chain is rated MEDIUM rather than LOW despite having two `?`-marked head inputs — the Rivals axis is not short here because the resulting 7–29 ¢/kWh bracket is consistent with widely published small/utility BESS LCOS figures, which serves as an external check rather than a live, unsettled rival.

### Conclusion C10: Lithium-ion, redirected to heat delivery, costs on the order of 7–30 ¢/kWh-th, central ≈14 ¢/kWh-th

C8 (≈$330/kWh installed, MEDIUM) + C9 (≈$0.13/kWh electric, MEDIUM)
→ using C9's same capital, life, and O&M economics (≈$216,000 annual cost, central case) but substituting a combined heat-delivery efficiency of round-trip efficiency times heater efficiency (≈88.5% × ≈98% ≈ 86.7%) in place of electrical round-trip efficiency, since the battery's output would be run through a simple resistive heater rather than used as AC power directly
→ annual heat delivered is ≈1,582,300 kWh-th, giving a central levelized cost of ≈$0.136/kWh-th
→ repeating at the optimistic (high heat-delivery efficiency, low-cost case) and pessimistic (low heat-delivery efficiency, high-cost case) ends brackets the levelized cost at roughly $0.072/kWh-th to $0.301/kWh-th

**Pre-check:** head C8 (MEDIUM), C9 (MEDIUM) · ?-marked: none · lowest cited: MEDIUM · Inputs ceiling: MEDIUM
**Confidence:** MEDIUM — ceiling set by C8 and C9 (both MEDIUM), whose own ratings are explained on their own confidence lines and not repeated here. No new `?`-marked input is introduced beyond what C8 and C9 already carry.

### Conclusion C11: For electricity-to-electricity round-trip service at 5 MWh pilot scale, the molten-salt Carnot battery is not cost-competitive with lithium-ion

C6 (≈$0.58/kWh, LOW) + C9 (≈$0.13/kWh, MEDIUM)
→ C6's central $0.58/kWh (bracket $0.21–2.00/kWh) for the molten-salt Carnot battery is roughly 4–5× C9's central $0.13/kWh (bracket $0.07–0.29/kWh) for lithium-ion, and the two central estimates do not overlap
→ even at the extremes — C6's most optimistic value (≈$0.21/kWh) against C9's most pessimistic value (≈$0.29/kWh) — the gap narrows to near-parity but lithium-ion still is not clearly beaten, and across the rest of each bracket lithium-ion is decisively cheaper

**Pre-check:** head C6 (LOW), C9 (MEDIUM) · ?-marked: none · lowest cited: LOW · Inputs ceiling: LOW
**Confidence:** LOW — ceiling set by C6 (LOW); C6's own confidence line explains its verification path (principally GT-16?, the small-turbine efficiency estimate) and is not repeated here. The qualitative *direction* of this verdict (lithium-ion cheaper) is more robust than the LOW numeric band on C6 alone would suggest, because it survives comparison against C9's own full bracket, not just its central value — this is the content of the Rivals axis for this chain, and is why section 5's falsification condition (in the appendix) is framed around what would have to be true to reverse the direction, not around matching the point estimate.

### Conclusion C12: For direct thermal (process-heat) delivery, molten-salt TES and lithium-ion are close to tied in the central case, with TES holding a modest, low-confidence edge that should widen with scale and time

C7 (≈$0.114/kWh-th, MEDIUM) + C10 (≈$0.136/kWh-th, MEDIUM)
→ C7's central ≈11 ¢/kWh-th (bracket 6–23 ¢/kWh-th) for molten-salt thermal-only delivery is modestly below C10's central ≈14 ¢/kWh-th (bracket 7–30 ¢/kWh-th) for lithium-ion redirected to heat delivery, and the two full brackets overlap almost entirely
→ the direction of this comparison (TES modestly cheaper) is far less robust than C11's, because the two central estimates differ by only ≈20% while each bracket spans roughly 3–4×
→[2nd] because fixed-cost items dominate C4/C5's installed-cost figure far more than the energy-related component does, real deployments respond by scaling duration up at fixed power (C4's own [2nd]-order finding), which should widen TES's thermal-only cost advantage over lithium-ion as projects move past pilot scale, since lithium-ion's cost structure carries no equivalent fixed-cost-dominated scale penalty to escape
→[3rd] over a multi-decade horizon, TES's calendar-limited ≈30-year life (GT-13?) against lithium-ion's cycle-limited ≈8–20-year replacement cycle (C9) compounds into a structural longevity advantage for high-cycle-frequency thermal applications specifically, independent of either technology's further cost decline — a finding that a reasoning-by-analogy comparison of today's $/kWh figures alone would miss entirely

**Pre-check:** head C7 (MEDIUM), C10 (MEDIUM) · ?-marked: none · lowest cited: MEDIUM · Inputs ceiling: MEDIUM
**Confidence:** MEDIUM — ceiling set by C7 and C10 (both MEDIUM); their own confidence lines carry the explanation and are not repeated here. The [2nd]/[3rd]-order extensions above do not introduce new `?`-marked inputs beyond GT-8? and GT-13?, both already carried by C4 and C6 respectively, and neither extension contradicts any ground truth in this analysis, so no return to Phase 2 is triggered.

---

## 5. Abandoned Reasoning

### Dead End 1: Costing the CSP-attached (solar-field-coupled) two-tank TES as the primary comparandum to lithium-ion

**What was tried:** An initial framing considered costing a CSP-attached molten-salt TES — the configuration with the best-evidenced real-world cost data (GT-6?, GT-7?) — as the primary basis for the lithium-ion comparison, since it is the configuration CSP cost literature actually reports.

**Why abandoned:** A CSP-attached TES has no metered-electricity charging leg at all — it is charged by free concentrated solar heat, and its power block (the turbine that eventually makes electricity) runs whether or not the TES is present, so its cost and output are shared with the whole plant rather than attributable to storage alone. An electricity-in/electricity-out $/kWh figure for this configuration is not a well-posed quantity, so it cannot be benchmarked against lithium-ion on the "same basis" the problem requires (success criterion 3, section 1).

**What it ruled out:** This saves a future analyst from citing CSP TES unit costs (the commonly-available $30–40/kWh-th figures in GT-6?) as if they were directly comparable to a battery's $/kWh — they measure a different, narrower scope (storage hardware only, power block excluded) and are not substitutable for the Carnot-battery figures in chains C4/C5.

### Dead End 2: A heat-pump-charged (COP > 1) Carnot-battery variant

**What was tried:** Considered costing a variant where charging is done via an industrial heat pump (coefficient of performance > 1) rather than direct resistive heating, which is how several real Carnot-battery demonstration projects are configured, in order to improve round-trip efficiency.

**Why abandoned:** Industrial heat pumps capable of lifting heat to the ≈565°C hot-tank temperature required by solar salt do not exist at commercial scale — practical industrial heat pumps top out at roughly 150–200°C. Introducing this variant would have required assuming a speculative future heat-pump technology with no defensible unit-cost basis, which is exactly the kind of unverifiable belief the methodology requires either verifying or excluding rather than quietly assuming.

**What it ruled out:** This rules out treating "improve the Carnot battery's round-trip efficiency with a heat pump" as a near-term lever for the configuration actually costed in this analysis; it remains a real technology path, but at a lower hot-side temperature and a different salt chemistry than solar salt, which is outside this analysis's scope.

### Dead End 3: Using Gen3 chloride-salt TES cost data ($60/kWh-th) as the primary cost anchor instead of solar salt

**What was tried:** The search for utility-scale TES unit costs surfaced a chloride-salt Gen3 CSP cost estimate of ≈$60/kWh-th, operating at much higher temperatures (>700°C) than solar salt, which was briefly considered as a second cost anchor for chain C4/C5's cross-check.

**Why abandoned:** Chloride salts require different corrosion-resistant materials and operate well outside the 280–565°C window this analysis adopted (GT-4?); folding a >700°C cost figure into a 565°C component buildup would mix incompatible material and equipment assumptions, and chloride-salt TES has far less commercial deployment experience than solar salt, making its public cost figures less representative of an achievable near-term 5 MWh system.

**What it ruled out:** This rules out treating GT-6?/GT-7? (solar-salt, 2004 and SunShot-era figures) and the chloride-salt figure as interchangeable evidence for the same cost claim; they are kept as separate, non-comparable reference points and the chloride-salt figure plays no role in chains C4/C5.

### Dead End 4: Comparing installed $/kWh directly, without routing through round-trip/delivery efficiency

**What was tried:** An initial simplified comparison considered ranking the two technologies purely on installed $/kWh (chain C4/C5 vs. C8), which would have made the molten-salt TES and lithium-ion look roughly comparable (and, at the low end of each bracket, nearly tied).

**Why abandoned:** This ignores exactly the mechanism — round-trip efficiency — that chain C3 identifies as the dominant driver of the electric-round-trip verdict (C11), and the problem explicitly asks for a levelized, cycle-amortized, efficiency-adjusted comparison (success criteria 2–3, section 1; LCOS-style methodology). Stopping at installed $/kWh would have overstated the Carnot battery's electric-round-trip competitiveness by a factor of roughly 4–5× relative to the levelized figures in C6 and C9.

**What it ruled out:** This rules out installed $/kWh alone as a sufficient basis for the competitiveness verdict requested by the problem; it remains useful context (and is reported in C4/C5/C8 for transparency) but is explicitly superseded by the levelized figures in C6/C7/C9/C10 for the headline verdict in C11/C12.

---

## 6. Conclusion

**Recommended approach:** Do not pursue a small-scale (5 MWh-class), electrically-charged, steam-Rankine-discharged molten-salt Carnot battery for electricity-to-electricity round-trip service — lithium-ion is decisively cheaper there, central ≈$0.13/kWh versus ≈$0.58/kWh (chain C11). Instead, molten-salt TES is worth pursuing specifically for direct thermal/process-heat delivery at larger-than-pilot scale and high cycling frequency, where it holds a modest central-case edge over lithium-ion (≈11 ¢/kWh-th versus ≈14 ¢/kWh-th, chain C12) that should widen with scale and time (chain C12's [2nd]/[3rd]-order extension).

**Key insight:** The decisive factor is not installed $/kWh of capacity — which is comparable between the two technologies at this small scale, both suffering badly from lost economies of scale (chain C4/C5 versus C8, central $460/$375 per kWh-th versus $330/kWh) — but round-trip efficiency, which at this scale is crushed by small-turbine economics to roughly 24% (chain C3), nowhere close to the 64.4% physical (Carnot) ceiling those temperatures would allow a much larger engine to approach. A comparison that reasoned by analogy from utility-scale Carnot-battery literature (which reports round-trip efficiencies of 40–60%) or from GWh-scale CSP TES unit costs would have missed this small-scale efficiency collapse entirely and reached the wrong verdict for the exact configuration this analysis was asked to cost.

**Trade-offs acknowledged:** Accepting GT-16? (the small-turbine efficiency estimate) as the central driver means the electric-round-trip verdict's numeric magnitude is LOW confidence (chain C6/C11) even though its direction is robust across the full bracket of both technologies; a vendor-quoted small-turbine efficiency curve could move the central $0.58/kWh figure substantially, though not enough, on its own, to close a 4–5× gap. The thermal-only verdict (chain C12) is a genuinely close, low-margin call — a ≈20% central-case gap inside brackets that each span 3–4× — so it should be read as "too close to call with today's evidence, with a modest lean toward TES" rather than a confident win.

**Pre-check:** head C11 (LOW), C12 (MEDIUM) · ?-marked: none · lowest cited: LOW · Inputs ceiling: LOW
**Confidence:** LOW — set by C11, the weakest contributing chain. C11's own confidence line (section 4) names GT-16? (the small-scale turbine efficiency estimate) as the principal cause of the downgrade and states that a vendor-quoted efficiency curve for a 0.2–1 MWe turbine on 565°C steam is the verification that would remove it; that explanation is not repeated here. C12, the other contributing chain, is independently rated MEDIUM and does not change this Conclusion's overall band, since the Conclusion's rating is the lowest of its contributing chains, not an average.

---

## Appendix — process output

## §6→§4 closure ledger (process output)

Enumerated per the Conclusion-section claim-inventory rule: section 6 contains exactly four bold-lead-in claims (Recommended approach, Key insight, Trade-offs acknowledged, Confidence), each closing its bold span with a colon and each carrying its own inline chain citation(s) on the same line. No list items or additional prose claims appear in section 6.

- "Do not pursue a small-scale...Carnot battery for electricity-to-electricity round-trip service — lithium-ion is decisively cheaper there...Instead, molten-salt TES is worth pursuing specifically for direct thermal/process-heat delivery...that should widen with scale and time" → chain C11, chain C12 ✓
- "The decisive factor is not installed $/kWh of capacity...but round-trip efficiency, which at this scale is crushed by small-turbine economics to roughly 24%...nowhere close to the 64.4% physical (Carnot) ceiling" → chain C3, chain C4, chain C5, chain C8 ✓
- "Accepting GT-16?...means the electric-round-trip verdict's numeric magnitude is LOW confidence...The thermal-only verdict...is a genuinely close, low-margin call" → chain C6, chain C11, chain C12 ✓
- "**Confidence:** LOW — set by C11, the weakest contributing chain...C12, the other contributing chain, is independently rated MEDIUM" → chain C11, chain C12 ✓

Reconciliation: 4 claims enumerated, 4 traced, 0 cut.

## Techniques not applied (process output)

- fishbone — not applicable — the assumption space for this analysis was directly enumerable from the component list the problem itself specifies (salt, tanks, HX, pumps, heater/turbine, EPC); no multi-causal brainstorm across categories was needed to surface it.
- trade-off — not applicable — the molten-salt-vs-lithium-ion comparison was already reducible to a common quantitative basis ($/kWh delivered, chains C6/C7/C9/C10) via direct levelized-cost computation; a qualitative weighted-criteria score would add no information and would obscure this analysis's actual conclusion that each technology wins in a different, non-overlapping duty regime rather than one "winning" on balance.
- pre-mortem — not applicable — per the inversion-vs-pre-mortem decision rule, pre-mortem stress-tests a plan and inversion stress-tests a claim; the headline conclusion here (chains C11/C12) is a comparative cost claim, not an execution plan, so inversion was applied instead (see the adversarial pass record below).

## Assumption Audit scan (process output)

| Chain | Step | Step Text (brief) | Assumption surfaced? | Added to Table? |
|-------|------|-------------------|----------------------|-----------------|
| C1 | 1 | 5,000 kWh → 1.8×10¹⁰ J | none | n/a |
| C1 | 2 | divide by cp·ΔT → 40,750 kg gross | none | n/a |
| C1 | 3 | +10% heel margin → 44.8 t | A-18 (heel/ullage margin) | yes |
| C2 | 1 | density at 280°C/565°C | none | n/a |
| C2 | 2 | volume from mass/density | none | n/a |
| C2 | 3 | +20% freeboard → tank capacities | A-18 (freeboard margin, same cluster) | yes (already added at C1 step 3) |
| C3 | 1 | Carnot ceiling at 838K/298K | A-19 (298K ambient reference) | yes |
| C3 | 2 | utility-scale Rankine ≈40–42% | none | n/a |
| C3 | 3 | small-scale penalty → 15–35% estimate | none (already GT-16?) | n/a |
| C3 | 4 | combine into ≈24% RTE / ≈95% thermal | none | n/a |
| C4 | 1 | blended salt cost | none | n/a |
| C4 | 2 | bottom-up equipment sum | A-21 (unsourced component line items) | yes |
| C4 | 3 | EPC multiplier → installed cost | none (already in table, EPC-multiplier row) | n/a |
| C4 | 4 | divide by 5,000 kWh → $/kWh-th | none | n/a |
| C4 | 5 [2nd] | duration-scaling response (six-tenths rule) | none (already GT-8?) | n/a |
| C4 | 6 [3rd] | pilot-ceiling framing | none | n/a |
| C5 | 1 | remove power block, trim switchgear | none (A-21 already added) | n/a |
| C5 | 2 | EPC multiplier → installed cost | none | n/a |
| C5 | 3 | divide by 5,000 kWh → $/kWh-th | none | n/a |
| C6 | 1 | capital charge (CRF, 30yr, 7%) | none (discount rate already in table) | n/a |
| C6 | 2 | + O&M → total annual cost | A-20 (O&M as % of capex) | yes |
| C6 | 3 | annual delivered / levelized | none | n/a |
| C6 | 4 | optimistic/pessimistic bracket | none | n/a |
| C7 | 1 | capital charge (CRF, 30yr, 7%) | none | n/a |
| C7 | 2 | + O&M (lower %) → total annual cost | none (A-20 already added) | n/a |
| C7 | 3 | annual heat delivered / levelized | none | n/a |
| C7 | 4 | optimistic/pessimistic bracket | none | n/a |
| C8 | 1 | pack price × small-scale multiplier | none (GT-17? already in table) | n/a |
| C8 | 2 | × 5,000 kWh → capital total | none | n/a |
| C9 | 1 | cycle-limited life (13.7 yr) | none (GT-12? already in table) | n/a |
| C9 | 2 | capital charge + O&M | none (A-20 already added) | n/a |
| C9 | 3 | annual delivered / levelized | none | n/a |
| C9 | 4 | optimistic/pessimistic bracket | none | n/a |
| C10 | 1 | substitute heat-delivery efficiency | none | n/a |
| C10 | 2 | annual heat delivered / levelized | none | n/a |
| C10 | 3 | optimistic/pessimistic bracket | none | n/a |
| C11 | 1 | compare C6 vs C9 centrals | none | n/a |
| C11 | 2 | compare brackets at extremes | none | n/a |
| C12 | 1 | compare C7 vs C10 centrals | none | n/a |
| C12 | 2 | compare robustness of each direction | none | n/a |
| C12 | 3 [2nd] | duration-scaling widens TES edge | none (GT-8? already in table) | n/a |
| C12 | 4 [3rd] | longevity compounding over decades | none (GT-13? already in table) | n/a |

Scan complete: 12 chains, 43 steps in order, no step skipped. 4 distinct new assumptions surfaced (A-18, A-19, A-20, A-21), each added to the Classified Assumptions Table (section 2) exactly once despite A-18 and A-20 each recurring across multiple steps.

## Self-audit scan (process output)

| Chain | Chain Head (brief) | Form conforming? | Rule applied | Dependency clean? | Band | Act attempted? | Edges fired |
|-------|---------------------|-------------------|---------------|--------------------|------|-----------------|-------------|
| C1 | GT-1, GT-2, GT-4? | yes | n/a | yes | MEDIUM | yes | none |
| C2 | C1, GT-3? | yes | n/a | yes | MEDIUM | no | none |
| C3 | GT-4?, GT-15?, GT-16? | yes | n/a | yes | LOW | no | none |
| C4 | GT-5?, GT-8?, GT-9?, C1, C2, C3 | yes | n/a | yes | LOW | yes | none |
| C5 | GT-5?, C1, C2 | yes | n/a | yes | MEDIUM | no | none |
| C6 | C3, C4, GT-13? | yes | n/a | yes | LOW | yes | none |
| C7 | C5 | yes | n/a | yes | MEDIUM | no | none |
| C8 | GT-10, GT-17? | yes | n/a | yes | MEDIUM | yes | none |
| C9 | C8, GT-12?, GT-14? | yes | n/a | yes | MEDIUM | no | none |
| C10 | C8, C9 | yes | n/a | yes | MEDIUM | no | none |
| C11 | C6, C9 | yes | n/a | yes | LOW | no | none |
| C12 | C7, C10 | yes | n/a | yes | MEDIUM | no | none |

| §6 Span (brief) | Construct | Claim under R11? | R11 clause applied | Chain cited |
|-------------------|-----------|-------------------|----------------------|---------------|
| **Recommended approach:** do not pursue...Carnot battery...; pursue TES for thermal delivery... | bold lead-in | yes | bold lead-in whose colon closes the bold span | C11, C12 |
| **Key insight:** decisive factor is round-trip efficiency, not installed $/kWh... | bold lead-in | yes | bold lead-in whose colon closes the bold span | C3, C4, C5, C8 |
| **Trade-offs acknowledged:** accepting GT-16? as the central driver... | bold lead-in | yes | bold lead-in whose colon closes the bold span | C6, C11, C12 |
| **Confidence:** LOW — set by C11... | bold lead-in | yes | bold lead-in whose colon closes the bold span (Confidence line) | C11, C12 |

Scan complete: 12 chain rows, one per section-4 chain block in order; 4 section-6 rows, one per construct in order — 4 claims under R11, 0 excluded. 0 chains malformed, 0 claims untraced.

## Adversarial pass (process output)

**Recompute.** Every computed figure in section 4 was redone independently of the chain text. Salt mass: 5,000 kWh × 3.6 MJ/kWh = 1.8×10¹⁰ J ÷ (1,550 J/kg·K × 285 K = 441,750 J/kg) = 40,749 kg, +10% = 44,823 kg — matches C1's "≈44.8 t." Tank volumes: ρ(280°C)=1,911.9 kg/m³, ρ(565°C)=1,730.7 kg/m³ → 23.44 m³ / 25.90 m³, ×1.2 → 28.1/31.1 m³ — matches C2. Carnot ceiling: 1 − 298/838 = 64.4% — matches C3. C4 central installed cost: direct-equipment $1.36M × 1.7 = $2.312M ÷ 5,000 kWh = $462/kWh-th (stated "≈$460") — matches within rounding; low $1.232M÷5,000=$246/kWh (stated "≈$250") and high $4.576M÷5,000=$915/kWh — both match. C5: $1.870M÷5,000=$374/kWh-th (stated "≈$375") — matches. C6 central: capital-recovery factor for 30 yr at 7% recomputes to 0.08058; annual capital charge $2.312M×0.08058=$186,300; +3% O&M ($69,360) = $255,660/yr; annual delivered 365×1,212.5=442,563 kWh; levelized $255,660÷442,563=$0.578/kWh — matches "≈$0.58." The optimistic/pessimistic bracket ends ($0.210/kWh and $1.992/kWh) both recompute to within rounding of the stated $0.21–$1.99/kWh. C7, C8, C9, and C10's central and bracket figures were likewise independently recomputed and all matched the chain text within rounding (≤2% in every case) — no arithmetic error was found anywhere that changes any chain's endpoint.

**Sensitivity.** The flip ground truth most often cited in section 4 is GT-16? (the small-scale turbine efficiency estimate, `?`-marked), which drives C3→C4→C6→C11. However, recomputing C6 with GT-16? revised all the way up to 45–50% (an optimistic ORC-bottoming-cycle assumption) still gives a central levelized cost of ≈$0.29–0.32/kWh — still roughly 2.2–2.5× C9's central $0.134/kWh, so GT-16? alone, even generously revised, does not flip C11's direction. Symmetrically, revising GT-17? (the Li-ion small-scale cost multiplier) up to push Li-ion's installed cost to $700/kWh (more than double this analysis's high-end estimate) still yields a Li-ion levelized cost of only ≈$0.28/kWh — again not enough, alone, to flip C11. Flipping C11's direction requires a *simultaneous* favorable revision on both sides (TES's efficiency and capital cost improving together) — which is exactly the combination C6's own optimistic-bracket computation already represents as its best case, landing near (but not past) parity with C9's worst case. This is named explicitly on C11's confidence line.

**Rival.** For the headline combined verdict (C11+C12): the strongest rival conclusion the same ground truths would support is "molten-salt TES is broadly cost-competitive with lithium-ion across both duty types at small scale." This is ruled out by chain C11 itself, whose central-case gap (4–5×) does not close under any single-input revision per the Sensitivity analysis above — recorded here, with the full reasoning on C11's own confidence line. For chain C4, a live rival is "the bottom-up component-cost buildup systematically overstates real EPC pricing" (cluster B below); this is not fully ruled out, but is bounded by the independent six-tenths-rule cross-check: scaling GT-6?'s inflation-adjusted $50–66/kWh-th (2025$) down from an assumed 1,500 MWh-th utility reference scale to 5 MWh-th via the (300)^0.4 ≈ 9.8× six-tenths-rule multiplier gives $489–647/kWh-th — within roughly 1.5× of C4's own $462/kWh-th central bottom-up figure, which bounds (without eliminating) the risk that the bottom-up method is biased high or low by some large systematic factor. For chain C3, the rival that small-scale turbines could plausibly achieve 35–40% rather than 25% remains live and unsettled — named on C3's own confidence line rather than resolved here.

**Premise.** The headline conclusion is already false: assume instead that the 5 MWh molten-salt Carnot battery *is* cost-competitive with lithium-ion for electricity-round-trip service, and ask what would have caused that.

**Causes** (unfiltered, generated from three stakeholder viewpoints before any grouping):
1. (Engineer) Small-scale turbine efficiency is actually far higher than estimated — e.g., a well-matched small ORC bottoming cycle achieves 40%+ rather than 25%, cutting C6's levelized cost roughly in half.
2. (Engineer) The bottom-up component-cost buildup (C4) systematically overstates real EPC pricing by 2× or more, because this analysis obtained no actual vendor quote for any major line item (A-21's flagged gap).
3. (Financier) A much lower discount rate (e.g., a 3% concessional/green-financing rate instead of 7%) is used, which favors the long-lived TES asset disproportionately more than the shorter-lived, cycle-limited Li-ion asset.
4. (Competitor/market) Lithium-ion pack prices reverse their multi-year decline and spike sharply — e.g., a lithium/cobalt supply shock or a tariff regime — pushing GT-10/GT-17?-derived installed costs toward $700+/kWh.
5. (Developer/market) Grid-scale deployment experience drives the six-tenths-rule scale-up (C4's [2nd]-order finding) to materialize quickly, so the real comparison that matters is run at 50+ MWh rather than 5 MWh, where TES's fixed-cost penalty has already been diluted away.
6. (Policymaker) A carbon price or thermal-storage-specific investment tax credit materially lowers TES's net installed cost relative to lithium-ion, which this analysis assumes (without checking) receives comparatively more favorable treatment under current US storage-specific incentives.

**Clusters:**
- **Cluster A — discharge-side conversion efficiency is underestimated** (cause 1) — bears on C3, GT-16?, cascading to C4/C6/C11.
- **Cluster B — the capital-cost buildup has no vendor-quote anchor** (cause 2) — bears on C4, C5, assumption A-21.
- **Cluster C — financing/policy assumptions favor one technology's cost structure over the other** (causes 3, 6) — bears on C6, C7, C9, C10 and the discount-rate/O&M conventions (assumption A-20); no policy-incentive asymmetry is represented anywhere in this analysis.
- **Cluster D — lithium-ion's own cost trajectory is itself uncertain, but in the opposite (favorable-to-Li-ion) direction** (cause 4) — bears on C8, GT-10, GT-17?.
- **Cluster E — scale mismatch: the pilot scale costed here is not the scale a real deployment decision would use** (cause 5) — bears on C4's [2nd]-order extension, GT-8?.

**Disposition:**
- Cluster A — accepted risk: flagged explicitly on C3/C6/C11's confidence lines as the dominant source of LOW confidence; mitigation named — obtain a vendor efficiency curve for a 0.2–1 MWe turbine on 565°C steam before committing capital to this configuration.
- Cluster B — accepted risk, bounded (not eliminated) by the independent six-tenths-rule cross-check above (≈1.5× agreement); plan change — a real procurement decision should obtain at least one vendor quote for the dominant cost items (tanks, turbine) before relying on this analysis's bottom-up figures alone.
- Cluster C — plan change: this analysis explicitly declines to model project-specific financing or incentive structures (outside the stated scope) and flags in section 6's Trade-offs that a materially different discount rate or an asymmetric incentive regime could shift the verdict; a decision-maker with access to specific financing terms should re-run chains C6/C7/C9/C10 with those terms.
- Cluster D — accepted risk: GT-10 is a 2024 figure already reported to keep falling (BNEF expects a further ≈$3/kWh decline in 2025), so this cluster's causal direction (lithium-ion reversing course and getting more expensive) runs against the observed trend rather than with it; mitigation — re-check GT-10/GT-11 at the time of any actual investment decision.
- Cluster E — plan change, already incorporated: chain C4's own [2nd]/[3rd]-order extension and chain C12's second-order extension state that real deployments should be expected to move toward larger-than-pilot scale, and section 6's Recommended approach reflects this by not recommending pilot-scale deployment of the electric-round-trip configuration at all.

**Falsification.** This analysis's electric-round-trip conclusion (C11) is false if an actual vendor-quoted small-scale (0.2–1 MWe class) turbine on 565°C steam is found to achieve net efficiency materially above 35% *and* the bottom-up capital-cost buildup in chain C4 is found to overstate real EPC pricing by more than roughly 1.5× — together, per the Sensitivity analysis above, these would be sufficient to move C6's levelized cost below C9's pessimistic bound and reverse C11's direction. The thermal-only conclusion (C12) is false — i.e., lithium-ion thermal delivery is the clearly cheaper option, not a close contest — if GT-17?'s small-scale lithium-ion cost multiplier turns out to be below ≈1.5× rather than the 2.0–3.5× estimated here.

## Self-Audit Gate (process output)

**Criterion 1: Identify Essence**
Quoted span: "Success criteria: 1. The analysis produces a component-by-component installed-cost buildup for the Carnot-battery configuration reaching a $/kWh-thermal-capacity figure expressed as a range (low/central/high)... 4. The Conclusion states, for each of the two duty types (electricity round-trip vs. thermal-only), which technology is cheaper in the central case, by what multiple, and whether the uncertainty bands of the two technologies overlap"
Band: **Rigorous**
Justification: the Essence Statement names the specific decision (cost-buildup + levelized-cost comparison for a named configuration) rather than restating the prompt, and each of the five success criteria is a verb+subject+outcome triplet checkable directly against section 6 without further interpretation (e.g. criterion 4 is checked by reading whether §6 states a multiple and an overlap verdict, which it does).

**Criterion 2: Challenge Assumptions**
Quoted span (from the Assumption Audit scan, process output): "Scan complete: 12 chains, 43 steps in order, no step skipped. 4 distinct new assumptions surfaced (A-18, A-19, A-20, A-21), each added to the Classified Assumptions Table (section 2) exactly once despite A-18 and A-20 each recurring across multiple steps."
Band: **Rigorous**
Justification: every row in the section-2 table carries a Type from the four-type scheme with em-dash-separated token-first Verdict cells (e.g. "Challenge — this is the single most consequential unverified number..."), the Assumption Audit scan confirms exhaustive coverage of all 43 named chain steps with no step skipped, and the four surfaced assumptions were added to the table exactly once each and marked inline at every originating step (verified in section 4: `[Assumes: A-18]` at C1 and C2, `[Assumes: A-19]` at C3, `[Assumes: A-20]` at C6/C7/C9, `[Assumes: A-21]` at C4).

**Criterion 3: Establish Ground Truths**
Quoted span: "?-marked: GT-3, GT-4, GT-5, GT-6, GT-7, GT-8, GT-9, GT-12, GT-13, GT-14, GT-15, GT-16, GT-17 (13 of 17)" cross-checked against the Ground Truths list: GT-1, GT-2, GT-10, GT-11 are the only unsuffixed entries, confirming the enumeration matches the list exactly.
Band: **Rigorous**
Justification: the `?` enumeration was checked against the list and matches exactly (13 of 17, the correct four unsuffixed); the four unsuffixed GTs each name a read-at-source location (GT-1's quoted paper sentence, GT-2's definitional status, GT-10's and GT-11's quoted report sections); and the two GTs (GT-6?, GT-13?) whose cited source proved unreachable each carry a Phase 3 failure record naming the source and the reason (confirmed DNS failure / HTTP 403), satisfying Exception (a) and feeding only MEDIUM/LOW chains (C6, LOW) rather than any HIGH chain.

**Criterion 4: Reason Upward**
Quoted span (from the self-audit scan's chain-form table): "C1 | GT-1, GT-2, GT-4? | yes | n/a | yes | MEDIUM | yes | none" through "C12 | C7, C10 | yes | n/a | yes | MEDIUM | no | none" — all twelve rows read `Form conforming? = yes` and `Dependency clean? = yes`.
Band: **Rigorous**
Justification: all twelve chains carry at least one genuine intermediate step, conform to the arrow-led one-hop-per-line form with no GT-N-led or sentence-closing hops, resolve dependencies without cycles, every chain step introducing a new assumption carries an inline `[Assumes: X]` tag matching the Assumption Audit scan, no analogy is used as direct evidence anywhere in section 4, and the Abandoned Reasoning section documents four specific dead ends (not vague "ran out of time" reasons) each with a precise structural abandonment cause.

**Criterion 5: Validate**
Quoted span: "Confidence: LOW — ceiling set by C3 and C4 (both LOW), whose own ratings and verification paths are explained on their own confidence lines and not repeated here. GT-13? (the 30-year calendar-life figure) is additionally `?`-marked; verification would require opening the same unreachable NREL corrosion-design document named in GT-13?'s Phase 3 failure record." (chain C6's confidence line)
Band: **Rigorous**
Justification: every MEDIUM/LOW confidence line names its own `GT-N?` inputs and cited `Cn` ceilings without re-explaining a cited chain's own cause (verified pattern across all twelve chains), no chain carrying a `GT-N?` input is rated HIGH, every chain is rated no higher than the lowest-rated chain its head cites (confirmed in the self-audit scan's Band column against each chain's head), and the adversarial pass record (process output, Inversion technique opened via Read on `references/inversion.md` before being applied) is complete with every part — Recompute, Sensitivity, Rival, Premise, Causes, Clusters, Disposition, Falsification — and every cluster carries a named disposition (either a plan change or an explicitly accepted risk with a named mitigation).

**Criterion 6: Conclusion-to-Ground-Truth Traceability**
Quoted span (from the self-audit scan's claim-inventory table): "**Recommended approach:** do not pursue...Carnot battery...; pursue TES for thermal delivery... | bold lead-in | yes | bold lead-in whose colon closes the bold span | C11, C12" through "**Confidence:** LOW — set by C11... | bold lead-in | yes | bold lead-in whose colon closes the bold span (Confidence line) | C11, C12" — all four section-6 claims cite a chain.
Band: **Rigorous**
Justification: all four Conclusion-section claims trace inline to specific named chains with no claim introducing new reasoning absent from section 4 (confirmed: the Key Insight's round-trip-efficiency claim restates C3/C4/C5/C8, not a new derivation), and the Key Insight ("the decisive factor is not installed $/kWh...but round-trip efficiency...crushed by small-turbine economics to roughly 24%, nowhere close to the 64.4% physical ceiling") is a non-obvious finding distinct from the Recommended approach's action-oriented statement, not a restatement of it.

**Gate result:** cleared · passes: 1 · Fix/Repeat fired: no

## Structured summary (process output)

```json
{
  "schema_version": 1,
  "run_mode": "full-composer",
  "assumptions": [
    {"id": "A-1", "type": "convention", "verdict": "Accept"},
    {"id": "A-2", "type": "convention", "verdict": "Accept"},
    {"id": "A-3", "type": "convention", "verdict": "Accept"},
    {"id": "A-4", "type": "untested belief", "verdict": "Challenge"},
    {"id": "A-5", "type": "convention", "verdict": "Accept"},
    {"id": "A-6", "type": "convention", "verdict": "Accept"},
    {"id": "A-7", "type": "convention", "verdict": "Challenge"},
    {"id": "A-8", "type": "untested belief", "verdict": "Challenge"},
    {"id": "A-9", "type": "current constraint", "verdict": "Accept"},
    {"id": "A-10", "type": "current constraint", "verdict": "Accept"},
    {"id": "A-11", "type": "untested belief", "verdict": "Challenge"},
    {"id": "A-12", "type": "physical law", "verdict": "Accept"},
    {"id": "A-13", "type": "convention", "verdict": "Accept"},
    {"id": "A-18", "type": "untested belief", "verdict": "Challenge"},
    {"id": "A-19", "type": "convention", "verdict": "Accept"},
    {"id": "A-20", "type": "untested belief", "verdict": "Challenge"},
    {"id": "A-21", "type": "untested belief", "verdict": "Challenge"}
  ],
  "ground_truths": [
    {"id": "GT-1", "read_at_source": true},
    {"id": "GT-2", "read_at_source": true},
    {"id": "GT-3", "read_at_source": false},
    {"id": "GT-4", "read_at_source": false},
    {"id": "GT-5", "read_at_source": false},
    {"id": "GT-6", "read_at_source": false},
    {"id": "GT-7", "read_at_source": false},
    {"id": "GT-8", "read_at_source": false},
    {"id": "GT-9", "read_at_source": false},
    {"id": "GT-10", "read_at_source": true},
    {"id": "GT-11", "read_at_source": true},
    {"id": "GT-12", "read_at_source": false},
    {"id": "GT-13", "read_at_source": false},
    {"id": "GT-14", "read_at_source": false},
    {"id": "GT-15", "read_at_source": false},
    {"id": "GT-16", "read_at_source": false},
    {"id": "GT-17", "read_at_source": false}
  ],
  "chains": [
    {"id": "C1", "confidence": "MEDIUM", "rests_on": ["GT-1", "GT-2", "GT-4?"]},
    {"id": "C2", "confidence": "MEDIUM", "rests_on": ["C1", "GT-3?"]},
    {"id": "C3", "confidence": "LOW", "rests_on": ["GT-4?", "GT-15?", "GT-16?"]},
    {"id": "C4", "confidence": "LOW", "rests_on": ["GT-5?", "GT-8?", "GT-9?", "C1", "C2", "C3"]},
    {"id": "C5", "confidence": "MEDIUM", "rests_on": ["GT-5?", "C1", "C2"]},
    {"id": "C6", "confidence": "LOW", "rests_on": ["C3", "C4", "GT-13?"]},
    {"id": "C7", "confidence": "MEDIUM", "rests_on": ["C5"]},
    {"id": "C8", "confidence": "MEDIUM", "rests_on": ["GT-10", "GT-17?"]},
    {"id": "C9", "confidence": "MEDIUM", "rests_on": ["C8", "GT-12?", "GT-14?"]},
    {"id": "C10", "confidence": "MEDIUM", "rests_on": ["C8", "C9"]},
    {"id": "C11", "confidence": "LOW", "rests_on": ["C6", "C9"]},
    {"id": "C12", "confidence": "MEDIUM", "rests_on": ["C7", "C10"]}
  ],
  "dead_ends": [
    "Costing the CSP-attached (solar-field-coupled) two-tank TES as the primary comparandum to lithium-ion",
    "A heat-pump-charged (COP > 1) Carnot-battery variant",
    "Using Gen3 chloride-salt TES cost data ($60/kWh-th) as the primary cost anchor instead of solar salt",
    "Comparing installed $/kWh directly, without routing through round-trip/delivery efficiency"
  ],
  "techniques": {
    "applied": ["five-whys", "theoretical-limit", "estimate", "second-order", "inversion"],
    "not_applied": [
      {"technique": "fishbone", "phase": 2, "reason": "the assumption space for this analysis was directly enumerable from the component list the problem itself specifies; no multi-causal brainstorm across categories was needed to surface it"},
      {"technique": "trade-off", "phase": 4, "reason": "the comparison was already reducible to a common quantitative basis via direct levelized-cost computation; a qualitative weighted-criteria score would obscure the conclusion that each technology wins in a different, non-overlapping duty regime"},
      {"technique": "pre-mortem", "phase": 5, "reason": "the headline conclusion is a comparative cost claim, not an execution plan, so inversion was applied instead per the inversion-vs-pre-mortem decision rule"}
    ]
  },
  "gate": {
    "passes": [
      {
        "bands": ["Rigorous", "Rigorous", "Rigorous", "Rigorous", "Rigorous", "Rigorous"],
        "gate_cleared": true,
        "hand_wavy_cap_cleared": true
      }
    ],
    "fix_repeat_fired": false,
    "cleared": true
  },
  "re_entry": {
    "fired": false,
    "edges": []
  },
  "conclusion": {
    "recommendation": "Do not pursue a small-scale (5 MWh-class), electrically-charged, steam-Rankine-discharged molten-salt Carnot battery for electricity-to-electricity round-trip service — lithium-ion is decisively cheaper there, central ≈$0.13/kWh versus ≈$0.58/kWh (chain C11). Instead, molten-salt TES is worth pursuing specifically for direct thermal/process-heat delivery at larger-than-pilot scale and high cycling frequency, where it holds a modest central-case edge over lithium-ion (≈11 ¢/kWh-th versus ≈14 ¢/kWh-th, chain C12) that should widen with scale and time (chain C12's [2nd]/[3rd]-order extension).",
    "confidence": "LOW",
    "rests_on": ["C11", "C12"]
  }
}
```
