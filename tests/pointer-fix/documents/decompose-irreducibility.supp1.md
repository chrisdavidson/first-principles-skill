## Answer

**Recommendation:** The compound claim is false. An 85%+ electricity round-trip efficiency is physically impossible for a resistive-charged thermal battery (it exceeds the ~63-64% Carnot ceiling at 565°C) (chain C1), and has no real-world precedent for a heat-pump-charged "Carnot battery" either — best demonstrated is 56-62% at 10 MW-plus reference scale (chain C2), with a 5 MWh system expected at or below that (chain C3). The system is also not cost-competitive with lithium-ion at 5 MWh, and the gap should widen over time (chain C4).

**Band (from §6):** MEDIUM

**Would change it:** Reading Malta Inc.'s own technical material directly, rather than secondary reporting, to confirm whether its 85-95% figure genuinely requires combined-heat-and-power credit as this analysis found (chain C2); opening the Danish Energy Agency Technology Catalogue, Echogen's technical papers, and the BNEF/Ember cost survey directly would remove the remaining `?`-marked inputs behind chains C2, C3, and C4.
## 1. Problem Essence

**Core problem:** Is it physically achievable for a 5 MWh molten-salt sensible-heat storage tank operating between 290°C and 565°C to convert electricity to heat and back at an electricity-to-electricity round-trip efficiency above 85%, and would a system built to do so be cost-competitive, per kWh of nameplate capacity, with a same-capacity lithium-ion battery system?

**Success criteria:**
1. The analysis states, with an explicit thermodynamic derivation, the ceiling on electricity-to-electricity round-trip efficiency for a heat engine operating between 565°C and a realistic heat-rejection temperature, and compares that ceiling (and the best real-world demonstrated figures) against the claimed 85%+ figure.
2. The analysis explicitly distinguishes "thermal energy retention efficiency" (how much stored heat survives standing losses) from "electricity round-trip efficiency" (how much input electrical energy is recovered as output electrical energy), because the claim's wording invites conflating the two.
3. The analysis states, with cited real-world cost and scale data, whether a 5 MWh-scale system of this type is cost-competitive per kWh with a same-capacity lithium-ion BESS, and names the dominant cost driver (storage medium vs. power-conversion equipment) behind that verdict.
4. The analysis names which of the two sub-claims (the 85%+ efficiency figure, the cost-competitiveness claim) is more defensible and why, rather than treating the compound claim as a single pass/fail unit.

---

## 2. Assumptions Table

| Assumption | Type | Treatment | Verdict | Verification |
|------------|------|-----------|---------|--------------|
| A-1: "Round-trip efficiency" as used in the claim means electricity-to-electricity efficiency, not thermal (heat-retention) efficiency of the storage medium alone | convention | Challenge before use — this is a common industry/press shorthand conflation, not a physical requirement | Challenge — discard the implied equivalence; thermal retention efficiency (~95-99% for an insulated sensible-heat tank over short holding periods) and electricity RTE are different quantities bounded by different physics | GT-1, GT-6?, GT-7? (see Ground Truths) |
| A-2: The charging mechanism is unambiguous (resistive/Joule heating vs. a heat-pump cycle) | untested belief | The claim's own wording ("electricity into heat and back") does not specify; verify by analyzing both branches | Challenge — ambiguous; both architectures analyzed separately in chains C1 (resistive) and C2 (heat-pump) | Re-read of claim text; no external source resolves the ambiguity |
| A-3: A 5 MWh system performs (efficiency and cost) similarly to the 10 MW–100+ MW reference systems most published Carnot-battery figures describe | convention | Challenge — this is an unstated scale extrapolation embedded in using large-plant figures to support a 5 MWh claim | Challenge — discard; GT-10? and GT-12? show strong scale-dependence in both cost and efficiency | GT-10?, GT-12? |
| A-4: Discharge uses a steam-Rankine-type (or closely analogous) heat engine, the dominant commercial technology at 290-565°C and sub-10 MW scale today | current constraint | Record expiry — holds while steam Rankine/ORC/sCO2 Brayton remain the practical commercial choice at this temperature and scale; a future small-modular sCO2 turbine could shift the economics | Accept — expires if/when small-modular sCO2 or ORC turbines reach commercial maturity at <5 MW; until then this is the applicable technology base | GT-5?, GT-8? |
| A-5: Parasitic losses (salt pumps, trace heating/freeze protection, controls, standby heat loss) are negligible | untested belief | Verify or flag — real systems carry several percent of throughput in parasitic load, proportionally larger at small scale due to higher surface-to-volume ratio | Challenge — discard as negligible; flagged and folded into chain C3's scale-penalty reasoning | unverified — flagged |
| A-6: Because the storage medium (molten salt) is cheap, the overall system is cheap | untested belief | Challenge — the storage medium's low cost per kWh(thermal) at large scale does not establish the cost of the power-conversion equipment, which published cost-scaling data show is the dominant, poorly-scaling cost driver | Discard — contradicted by GT-10?; power block (turbine/heat pump, heat exchangers, controls), not the salt/tanks, dominates cost at small scale | GT-10?, GT-11? |
| A-7: Lithium-ion BESS cost is high/static, making a thermal alternative look favorable by comparison | current constraint | Record expiry — Li-ion turnkey costs are on a steep, continuing downward trend; any comparison must use current-year figures | Challenge — discard the "static/high" framing; 2025 figures show continued sharp decline (-31% YoY per BNEF) | GT-9? |
| A-8: Nameplate MWh capacity alone is a sufficient basis for cost comparison, independent of discharge duration (hours) | untested belief | Flag — the claim gives no discharge duration; thermal-battery power-block cost scales mainly with power (MW), while Li-ion cost scales mainly with energy (MWh), so the duration implicit in "5 MWh" materially changes the comparison | Challenge — unverified; analysis assumes a plausible 1-10 hour duration (implying a roughly 0.5-5 MW power block) typical of how "5 MWh" storage claims are normally sized | unverified — flagged |
| A-9: Modular lithium-ion BESS packaging cost scales down close to linearly in $/kWh from utility scale to 5 MWh scale | current constraint | Record expiry — approximately true because Li-ion systems are built from identical cells/racks regardless of project size, but a real small-scale BOS/EPC cost premium still applies | Accept — expires if small-project BOS/interconnection overhead grows disproportionately; until then a reasonable approximation used in chain C4 | unverified — flagged (used in C4, surfaced during Phase 4 chain audit) |
| A-10: A realistic heat-engine ambient heat-rejection temperature for this analysis is approximately 15-40°C | current constraint | Record expiry — depends on site climate and cooling technology (air-cooled vs. wet-cooled condenser); bounded by ordinary terrestrial climate and practical cooling-system economics | Accept — expires only for an exotic (and itself energy-costly) sub-ambient/cryogenic rejection scheme, which would not plausibly change the conclusion (see chain C1's rival-handling) | Standard power-plant engineering baseline; no single external citation needed beyond GT-1's physical derivation |
| A-11: Financing/bankability risk premiums for novel small-scale thermal storage are not already captured in the published LCOS/cost figures (GT-10?, GT-11?) | untested belief | Verify or flag — surfaced during the Phase 4 end-of-chain Assumption Audit (chain C4, 2nd-order actor-lens step); published LCOS studies are typically modeled on an assumed cost of capital and may not reflect a real lender's bankability discount for an unproven small-scale design | Challenge — unverified; used directionally in C4 to widen, not to quantify, the cost gap | unverified — flagged |
| A-12: Carnot-battery component standardization/volume manufacturing will not emerge fast enough in the near term to close the cost-decline-rate gap with lithium-ion | current constraint | Record expiry — surfaced during the Phase 4 end-of-chain Assumption Audit (chain C4, 2nd-order time-lens step); holds only until small-modular turbine/heat-pump OEMs achieve factory-standardized "thermal-battery-in-a-box" products at volume | Accept — expires if/when such standardization emerges; until then this is the applicable near-term trend | unverified — flagged |

---

## 3. Ground Truths

- **GT-1** The maximum possible efficiency of any heat engine operating between a hot reservoir at absolute temperature Th and a cold (heat-rejection) reservoir at absolute temperature Tc is η_Carnot = 1 − Tc/Th (Carnot's theorem, Second Law of Thermodynamics) — source: standard thermodynamic physical law, universally codified, not attributable to a single primary document; read-at-source: derived directly in this analysis by applying the formula with Th = 838.15 K (565°C) and Tc = 298.15-308.15 K (25-35°C), giving η_Carnot ≈ 0.64-0.63 (63-64%).
- **GT-2** Converting electrical energy to heat via resistive (Joule) heating is close to 100% efficient — essentially all I²R dissipation in a resistive element appears as heat, with only minor practical losses in wiring, contactors, and transformers (typically 1-5%) — source: standard electrical-engineering physical law (conservation of energy applied to resistive dissipation); read-at-source: derived directly, no external document needed.
- **GT-3** A realistic ambient heat-rejection temperature for a land-based thermal power cycle's condenser is approximately 15-40°C, set by climate and practical cooling-system economics — source: standard power-plant engineering baseline; read-at-source: not applicable (engineering convention, not a single citable measurement); classified as a `current constraint` in the Assumptions Table (A-10) rather than claimed as a physical law.
- **GT-4?** Gemasolar (Spain), the reference commercial-scale solar-salt two-tank molten-salt thermal storage plant, operates its cold tank at 290°C and its hot tank at 565°C using a 60% NaNO3/40% KNO3 salt mixture (melting point ≈220-228°C; thermally stable long-term to roughly 400-560°C, with faster-heating decomposition onset reported near 631°C) — confirming the claim's stated 290-565°C window matches a real, established engineering design point, not an arbitrary or fictional range — cited to: SolarPACES/NREL CSP project database and secondary CSP engineering literature; reported-by-delegate: supplied via web search synthesis. A direct WebFetch of the SolarPACES project page was attempted and failed (DNS resolution error — source unreachable in this environment); Phase 3 failure record: solarpaces.nrel.gov, unreachable (network/DNS failure), so this ground truth remains `?`-marked and feeds only MEDIUM/LOW chains.
- **GT-5?** For concentrating solar power plants using a steam Rankine power block, thermal-to-electric cycle efficiency is approximately 37.6% at superheated steam temperatures around 393°C, rising to approximately 40% as steam temperature increases to roughly 450-500°C — cited to: CSP/Rankine-cycle performance literature (academic theses/papers on molten-salt CSP power-block performance); reported-by-delegate: supplied via web search synthesis, source not opened directly.
- **GT-6?** Published electricity-to-electricity round-trip efficiencies for molten-salt-based "Carnot battery" (pumped thermal electricity storage) configurations range from a 30% baseline in the Danish Energy Agency's Technology Catalogue, to 56.2% (up to 62.5% at a lower discharge pressure ratio) and 57.43% in optimized research designs (the latter with a modeled levelized cost of storage of ≈€0.649/kWh) — cited to: Danish Energy Agency Technology Catalogue; Comillas/MDPI Energies (2023) optimization studies; reported-by-delegate: supplied via web search synthesis, sources not opened directly.
- **GT-7?** Malta Inc.'s pumped-heat energy storage system (molten salt hot side, antifreeze-liquid cold side) is stated by the company to reach up to 60% round-trip efficiency for electricity-only output at full commercial scale (100+ MW power block, 1,000+ MWh storage, 8 hours-8 days duration); the company separately states 85-95% round-trip efficiency specifically for combined heat-and-power (CHP) operation, where recovered low-grade heat is credited as a second useful output alongside electricity — cited to: Malta Inc. company/technical materials as reported by power-eng.com and energy-storage.news; reported-by-delegate: supplied via web search synthesis, sources not opened directly.
- **GT-8?** Echogen's supercritical-CO2 pumped thermal energy storage (PTES) system, using thermal reservoirs at approximately 335°C (hot) and 0°C (cold), is reported to achieve greater than 60% round-trip efficiency in favorable configurations, with 50% achievable using a lower-cost ice-on-coil cold-storage approach — cited to: Echogen technical overview documents and NETL/SwRI conference materials; reported-by-delegate: supplied via web search synthesis, sources not opened directly.
- **GT-9?** As of 2025, the global average turnkey cost of a utility-scale lithium-ion battery energy storage system (BESS) is approximately $117/kWh (BloombergNEF Energy Storage System Cost Survey 2025), down roughly 31% year-over-year; regional turnkey costs vary from ≈$73/kWh in China to ≈$177/kWh in Europe and ≈$219/kWh in the US; the battery pack alone (excluding BOS/EPC) averages ≈$70/kWh globally — cited to: BloombergNEF / Ember Energy cost survey reporting; reported-by-delegate: supplied via web search synthesis, source not opened directly.
- **GT-10?** Carnot-battery techno-economic studies document strong capital-cost economies of scale: one study found that increasing capacity from 10 MW to 50 MW reduces LCOE by 46.3%; another found that increasing capacity from 1 MW to 100 MW reduces LCOE from 2.37 to 0.83 ¥/kWh (≈65% reduction) — cited to: Carnot-battery techno-economic literature as reported via ess-news.com/pv-magazine and related academic sources; reported-by-delegate: supplied via web search synthesis, sources not opened directly.
- **GT-11?** For Carnot-battery systems to be cost-competitive in a high-renewables grid scenario, published analysis estimates a required levelized cost of storage (LCOS) below approximately €66.2/MWh (≈$72/MWh); among surveyed system concepts, only one was identified below €62/MWh, and none of the surveyed competitive concepts were at 5 MWh scale — cited to: "Optimizing Carnot batteries for renewables storage" (pv-magazine/ess-news, summarizing underlying academic analysis); reported-by-delegate: supplied via web search synthesis, source not opened directly.
- **GT-12?** Small (kW-class) organic Rankine cycle heat-engine units show severely degraded thermal efficiency relative to utility-scale turbines operating on comparable temperature differentials: a 5 kW ORC unit achieved only ≈10-11% thermal efficiency, and a 1 kW unit achieved ≈4.7-5.6%, versus 35-40%+ typically achieved by utility-scale (10s-100s of MW) turbines on similar source temperatures — cited to: small-scale ORC performance literature (academic test-rig studies); reported-by-delegate: supplied via web search synthesis, sources not opened directly. Used only illustratively in this analysis, to establish the *direction* of the scale penalty on heat-engine efficiency — not as a direct quantitative stand-in for a 5 MWh/~1 MW-class power block, which sits in a different (larger) size regime than these kW-scale lab units.

**Provenance summary:** `?`-marked: GT-4, GT-5, GT-6, GT-7, GT-8, GT-9, GT-10, GT-11, GT-12 (9 of 12). Read-at-source: GT-1 — derived directly via η=1−Tc/Th with Th=838.15K, Tc=298.15-308.15K; GT-2 — derived directly from conservation of energy applied to resistive dissipation; GT-3 — engineering baseline, no single citable source (not a read-at-source claim; see Assumptions Table A-10 for its `current constraint` treatment). No unsuffixed ground truth in this analysis feeds a HIGH-confidence chain without a named read-at-source location (GT-1, GT-2 feed chain C1, rated HIGH, both with their derivations named above). All nine `?`-marked ground truths were sourced via web-search synthesis; none of their underlying primary documents were opened directly in this run. One direct-read attempt (GT-4, via WebFetch to solarpaces.nrel.gov) failed with a DNS resolution error in this environment; that Phase 3 failure record is recorded against GT-4 above. Given the turn budget and that none of the remaining `?`-marked ground truths feed a HIGH-confidence chain (all load-bearing chains that cite them are capped at MEDIUM by the `?` itself, consistent with D-07), no further source-opening attempts were made this run; this is disclosed as a residual rather than treated as silently resolved.

---

## 4. Derivation Chains

### Conclusion C1: An 85%+ electricity round-trip efficiency is thermodynamically impossible for a resistive-heating-charged, heat-engine-discharged molten-salt thermal battery in the 290-565°C range

GT-1 (Carnot ceiling η=1−Tc/Th) + GT-2 (Joule heating ≈100% electric-to-heat) + GT-3 (realistic condenser reject temp 15-40°C)
→ taking the claim's own stated hot-tank temperature of 565°C (838.15K) as the heat engine's source and a realistic ambient rejection temperature of 25-35°C (298-308K), the absolute Carnot efficiency ceiling for the discharge half-cycle alone is approximately 63-64%
→ resistive charging adds essentially no thermodynamic leverage beyond converting electricity to heat at near-100% efficiency, so it cannot raise the overall ceiling above the discharge-side Carnot limit already computed
→ even testing the most favorable plausible rival rejection temperature of 0°C (273.15K) rather than 25-35°C only raises the ceiling to about 67.4%, still far short of 85%, so the conclusion is robust to reasonable variation in the rejection-temperature assumption
→ an electricity-to-electricity round-trip efficiency above 85% is not achievable by this architecture at any engineering quality, because it exceeds the absolute physical ceiling, not merely today's best practice

**Pre-check:** head GT-1, GT-2, GT-3 · ?-marked: none · lowest cited: none · Inputs ceiling: HIGH
**Confidence:** HIGH — every input is a directly-derived physical law or standard engineering baseline (no `?`-marked ground truth); the arithmetic recomputes independently (1 − 308.15/838.15 = 0.632; 1 − 273.15/838.15 = 0.674); the one plausible rival (a colder, more aggressive heat-rejection temperature) is explicitly tested within the chain and shown not to change the conclusion.

### Conclusion C2: For a heat-pump-charged "Carnot battery" architecture, 85%+ pure-electricity round-trip efficiency is not thermodynamically forbidden in the ideal limit, but has no real-world precedent at any demonstrated scale and conflates with a different, easier-to-claim CHP metric

GT-6? (molten-salt Carnot battery RTE 30-62%) + GT-7? (Malta: ≤60% electricity-only; 85-95% only in CHP mode) + GT-8? (Echogen: >60% at 335°C)
→ in the idealized, fully-reversible limit a heat-pump-charged, heat-engine-discharged cycle operating between the same two reservoirs has a theoretical round-trip ceiling of 100%, because the Carnot heat pump's coefficient of performance and the Carnot heat engine's efficiency are reciprocals of one another
→ no real system approaches that ideal limit: across a Danish Energy Agency catalogue baseline, multiple optimized research designs, and the most advanced commercial-stage pilots (Malta, Echogen), documented pure-electricity round-trip efficiency tops out at roughly 56-62%, even at reference scale (10 MW-plus power blocks, 1,000+ MWh storage)
→ the only published figures reaching 85-95% (Malta's CHP-mode claim) require crediting recovered low-grade heat as a second useful output, which is a materially easier bar than converting 100% of the recovered energy back into electricity
→ read as a pure electricity-to-electricity figure, the claimed 85%+ has no real-world precedent at any scale and most plausibly reflects a conflation with the CHP-credited metric

**Pre-check:** head GT-6?, GT-7?, GT-8? · ?-marked: GT-6?, GT-7?, GT-8? · lowest cited: none · Inputs ceiling: MEDIUM
**Confidence:** MEDIUM — GT-6?, GT-7?, GT-8? are all reported-by-delegate (supplied via web search synthesis rather than read at their primary sources); the verification that would remove each as a cause of this downgrade is opening the Danish Energy Agency Technology Catalogue, the underlying Comillas/Energies optimization papers, Malta Inc.'s technical specification sheets, and Echogen's NETL/SwRI technical papers directly, to confirm the figures and (for GT-7?) the CHP-vs-electricity-only distinction in the company's own wording rather than in secondary reporting.

### Conclusion C3: A 5 MWh-scale system should be expected to land at the low end of, or below, the 30-62% reference-scale range established in C2 — not above it

C2 (56-62% best-demonstrated at reference scale, MEDIUM) + GT-10? (strong Carnot-battery economies of scale) + GT-12? (severe kW-scale heat-engine efficiency degradation, illustrative only)
→ the 56-62% figures in C2 were demonstrated on 10 MW-plus power blocks and 1,000+ MWh storage; GT-10?'s documented 46-65% LCOE reduction per order-of-magnitude capacity increase shows strong economies of scale in cost, and the same physical drivers (lower turbine/heat-pump isentropic efficiency at low flow rates, a higher fixed parasitic-load fraction relative to throughput, and a higher tank surface-to-volume ratio increasing standby heat loss) push achievable round-trip efficiency in the same unfavorable direction as scale shrinks [Assumes: A-5 — parasitic losses are not negligible and grow proportionally larger at small scale]
→ GT-12?'s kW-scale ORC data (5-11% efficiency at 1-5 kW versus 35-40%+ at utility scale) illustrates that this scale penalty can be severe in the extreme, though a 5 MWh/~1 MW-class power block sits two to three orders of magnitude above that kW-scale regime and should not be expected to suffer an equally extreme penalty
→ a 5 MWh system is nonetheless two to three orders of magnitude below the 10-100+ MW reference scale on which the 56-62% figures were demonstrated, so its real achievable electricity round-trip efficiency should be expected at or below the low end of that range, reinforcing that 85%+ is implausible at this specific scale

**Pre-check:** head C2 (MEDIUM), GT-10?, GT-12? · ?-marked: GT-10?, GT-12? · lowest cited: MEDIUM · Inputs ceiling: MEDIUM
**Confidence:** MEDIUM — capped by C2 (MEDIUM, see C2's own confidence line for its verification path); GT-10? and GT-12? are reported-by-delegate, removable by opening the underlying techno-economic papers and small-scale ORC studies directly. The [Assumes: A-5] premise (parasitic losses scale unfavorably with size) is priced: even if A-5 were false — i.e., if parasitic/standby losses turned out not to scale unfavorably with size — the chain's conclusion would still stand on the independent, well-established turbomachinery regularity that small (sub-5 MW) turbines exhibit lower isentropic efficiency than 50-100+ MW units at comparable pressure ratios, which alone is sufficient to place a 5 MWh-class power block's efficiency below the 10-100+ MW reference scale on which the 56-62% figures were demonstrated; full verification of the magnitude would still require vendor-level parasitic-load and small-turbine isentropic-efficiency data for a 5 MWh-class plant, which was not available in this run.

### Conclusion C4: At 5 MWh, a molten-salt thermal battery should be expected to cost substantially more per kWh of nameplate capacity than a same-capacity lithium-ion BESS, making the cost-competitiveness claim implausible

GT-9? (2025 Li-ion turnkey cost $117-219/kWh, pack ≈$70/kWh) + GT-10? (Carnot-battery economies of scale) + GT-11? (Carnot-battery LCOS competitiveness threshold ≈€66/MWh, barely met even at favorable scale)
→ lithium-ion BESS cost is dominated by modular cells/racks that scale down close to linearly in $/kWh [Assumes: A-9 — modular Li-ion packaging scales down near-linearly, with only a bounded small-project BOS/EPC premium], so a 5 MWh Li-ion system can be expected to cost on the order of $150-400/kWh turnkey once a reasonable small-scale premium over the $117-219/kWh utility-scale range is included
→ molten-salt Carnot-battery cost is dominated by custom power-conversion equipment (turbine or heat pump, heat exchangers, controls, civil works) that does not scale down proportionally, which is exactly the mechanism behind GT-10?'s documented 46-65% LCOE increase when capacity shrinks by one to two orders of magnitude
→ GT-11?'s finding that even reference-scale (10-100+ MW) Carnot batteries barely clear a ≈€66/MWh LCOS competitiveness bar shows the technology is not yet cost-competitive even where its economies of scale are most favorable, before any small-scale penalty is applied
→[2nd] once the direct hardware cost gap is visible, project financiers and developers price a custom, less-bankable thermal technology at a higher financing risk premium than a standardized, track-recorded Li-ion system, widening the effective delivered-cost gap beyond the hardware comparison alone (actor lens: financiers and developers react to the technology's novelty, not just its sticker price)
→[2nd] over the next several years Li-ion turnkey costs are on a continuing steep decline (GT-9?'s -31% year-over-year figure for 2025) while small-scale Carnot-battery costs are not expected to fall as fast absent volume manufacturing of standardized small turbines/heat pumps, so the cost gap should be expected to widen, not narrow, on a multi-year horizon unless such standardization emerges (time lens: the comparison evaluated today becomes less favorable to the thermal battery tomorrow under business-as-usual, not more)
→ at 5 MWh, several orders of magnitude below the reference scale where published Carnot-battery economics are least unfavorable, the molten-salt system should be expected to cost substantially more per kWh than a same-capacity Li-ion system, now and increasingly so over time

**Pre-check:** head GT-9?, GT-10?, GT-11? · ?-marked: GT-9?, GT-10?, GT-11? · lowest cited: none · Inputs ceiling: MEDIUM
**Confidence:** MEDIUM — GT-9?, GT-10?, GT-11? are all reported-by-delegate; removable by opening the BNEF/Ember cost survey, the underlying Carnot-battery techno-economic papers, and the pv-magazine/ess-news-cited LCOS competitiveness analysis directly. The [Assumes: A-9] premise (near-linear Li-ion cost scaling) is only partly priced: if small-project Li-ion BOS/EPC overhead is in practice much higher than assumed, the $150-400/kWh estimate understates Li-ion's own cost at 5 MWh, which would *narrow* the gap this chain reports — this sensitivity is carried forward into the Conclusion section's confidence line rather than resolved here. No rival conclusion to this chain's direction was found live in the surveyed literature (every cost-scaling source pointed the same direction); see §5 for the one alternative reading that was considered and set aside.

---

## 5. Abandoned Reasoning

### Dead End: Pushing the Carnot ceiling higher via a colder (sub-ambient/cryogenic) heat-rejection scheme

**What was tried:** In chain C1, tested whether assuming a more aggressive heat-rejection temperature than typical ambient (e.g., 0°C via refrigeration) could raise the discharge-side Carnot ceiling enough to make 85%+ plausible for the resistive-heating architecture.

**Why abandoned:** Even at 0°C (273.15K) the ceiling only rises to ≈67.4%, still far below 85%; and a refrigeration-based sub-ambient rejection scheme would itself consume parasitic electricity, which would reduce — not improve — net electricity round-trip efficiency, making the rival self-defeating as well as insufficient.

**What it ruled out:** This saves a future reviewer from re-testing "maybe a colder sink fixes it" — it does not, and pursuing it further costs net efficiency rather than gaining it.

### Dead End: Accepting Malta Inc.'s 85-95% figure as direct support for the claim's 85%+ electricity round-trip efficiency

**What was tried:** Initially considered treating GT-7?'s 85-95% figure as corroborating evidence that the claim's 85%+ number is achievable, since it comes from a credible commercial pumped-heat storage developer.

**Why abandoned:** Closer reading of the same source material shows the 85-95% figure is explicitly a combined-heat-and-power (CHP) metric that credits recovered low-grade heat as a second useful output, not a pure electricity-to-electricity round-trip figure; Malta's own electricity-only figure is ≤60%, consistent with every other source in GT-6? and GT-8?. Using the CHP figure to support the claim would have been exactly the conflation identified in Assumption A-1.

**What it ruled out:** This closes off the single most tempting piece of evidence that could have been misread as supporting the claim, and documents precisely why it does not.

### Dead End: Assuming lithium-ion is equally cost-penalized at 5 MWh scale, producing near cost-parity rather than a Li-ion advantage

**What was tried:** Considered whether the small-scale cost disadvantage found for the molten-salt system in chain C4 might be matched by a comparable small-scale disadvantage for lithium-ion, since both face some project-level fixed costs (interconnection, EPC overhead) at small scale.

**Why abandoned:** The regional cost variation in GT-9? ($73-219/kWh) is driven primarily by manufacturing location, labor, and tariffs rather than by project size, because Li-ion systems are built from identical modular cells/racks regardless of scale; GT-10?'s scale-driven LCOE swings (46-65% per order of magnitude) are specific to the custom turbine/heat-exchanger equipment that dominates Carnot-battery cost and has no Li-ion equivalent. No source surveyed showed Li-ion cost scaling as steeply with project size as Carnot-battery cost does.

**What it ruled out:** This is the explicit rival to chain C4's direction; it was tested and did not survive, which is why C4 reports no live rival in its confidence line.

### Dead End: Applying the weighted trade-off procedure to choose between molten-salt and lithium-ion

**What was tried:** Considered formally applying the trade-off/weighted-scoring technique (criteria, weights, scored options) to compare the two storage technologies.

**Why abandoned:** The trade-off procedure is for choosing between options the ground truths leave genuinely viable; here, chains C1-C4 do not leave two comparably viable options to weigh — they disqualify the molten-salt option on both the efficiency axis (C1/C2/C3) and the cost axis (C4) at this specific scale. Running a weighted scorecard on a comparison the physics and the published economics already settle would manufacture false even-handedness. (See Phase 4 companion-technique log in the process-output appendix for the explicit not-applicable record.)

**What it ruled out:** This saves a future reviewer from re-running a trade-off matrix that would not change the conclusion, and documents why a claim-plausibility question is not reframed as an options-weighing question.

---

## 6. Conclusion

**Recommended approach:** Treat the compound claim as false as stated. Read as a resistive-heating-charged thermal battery, 85%+ electricity round-trip efficiency is not an engineering shortfall but a physical impossibility — it exceeds the ≈63-64% Carnot ceiling for a heat engine running between 565°C and ambient (chain C1). Read as a heat-pump-charged "Carnot battery," 85%+ pure-electricity round-trip efficiency is not forbidden in the ideal limit but has no real-world precedent at any demonstrated scale — the best documented figures are 56-62% at 10 MW-plus reference scale (chain C2), and a 5 MWh system should be expected at or below the low end of that range (chain C3). The cost-competitiveness sub-claim is also false at 5 MWh: published economies-of-scale data indicate a molten-salt system at this scale should cost substantially more per kWh than a same-capacity 2025 lithium-ion BESS, and the gap should be expected to widen rather than narrow over the next several years (chain C4).

**Key insight:** The claim's plausibility depends on two conflations that become visible only by tracing the physics and economics from first principles rather than from headline industry figures: (1) it borrows an 85-95% figure that, in its original source, is a combined-heat-and-power metric crediting recovered waste heat, not a pure electricity-to-electricity round-trip figure (chain C2); and (2) it implicitly extrapolates efficiency and cost figures demonstrated on 10-100+ MW reference plants down to a 5 MWh system, where the custom power-conversion equipment that dominates both efficiency and cost scales unfavorably rather than favorably (chains C3, C4).

**Trade-offs acknowledged:** This verdict is scoped to the specific claim under test (85%+ pure electricity round-trip efficiency and cost-competitiveness at 5 MWh) and should not be read as a blanket dismissal of molten-salt thermal storage. The technology retains real, first-principles-grounded advantages this analysis does not negate: long-duration and multi-day storage without the cycle-life degradation lithium-ion faces, a storage medium (nitrate salt) that is abundant and free of critical-mineral supply constraints, and a genuine path to high combined efficiency where recovered heat has local value, as chain C2's CHP pathway shows (chain C2). Accepting this analysis's verdict means deprioritizing molten-salt thermal storage specifically as a small-scale (5 MWh), electricity-only, cost-competitive alternative to lithium-ion — not as a long-duration or CHP storage option more broadly.

**Pre-check:** head C1 (HIGH), C2 (MEDIUM), C3 (MEDIUM), C4 (MEDIUM) · ?-marked: none · lowest cited: MEDIUM · Inputs ceiling: MEDIUM
**Confidence:** MEDIUM — the resistive-architecture half of the efficiency verdict rests on C1 (HIGH, a clean physical-law derivation) and is essentially certain. The overall Conclusion is capped at MEDIUM because it also rests on C2, C3, and C4, each of which carries `?`-marked (reported-by-delegate) ground truths whose primary sources were not opened directly in this run — see each chain's own confidence line for its specific verification path (opening the Danish Energy Agency Technology Catalogue, Malta/Echogen technical materials, the BNEF/Ember cost survey, and the underlying Carnot-battery techno-economic papers directly). The single most sensitive unresolved input is GT-7? (the Malta CHP-vs-electricity-only distinction): if that distinction were found, on direct reading of Malta's own technical material, to be less sharp than the secondary reporting in GT-7? suggests, chain C2's "no real-world precedent" claim would weaken, though chain C1's impossibility result for the resistive architecture would be unaffected.
## Appendix — process output

## Assumption Audit scan (process output)

| Chain | Step | Step Text (brief) | Assumption surfaced? | Added to Table? |
|-------|------|--------------------|-----------------------|------------------|
| C1 | 1 | Carnot ceiling at 565°C / 25-35°C ≈ 63-64% | A-10 (ambient reject temp 15-40°C) | n/a — already in Table |
| C1 | 2 | resistive charging adds no leverage beyond Joule heating | none | n/a |
| C1 | 3 | rival 0°C rejection tested, still <85% | none | n/a |
| C1 | 4 | conclusion: 85%+ impossible for resistive architecture | none | n/a |
| C2 | 1 | ideal reversible heat-pump+engine ceiling = 100% | none | n/a |
| C2 | 2 | no real system approaches ideal; best demonstrated 56-62% | none | n/a |
| C2 | 3 | 85-95% figures are CHP-credited, not pure electricity | none | n/a |
| C2 | 4 | conclusion: 85%+ pure-electricity has no real-world precedent | none | n/a |
| C3 | 1 | scale penalty on efficiency via parasitic loss / isentropic efficiency | A-5 (parasitic losses not negligible, scale unfavorably) | n/a — already in Table |
| C3 | 2 | kW-scale ORC data illustrates direction only | none | n/a |
| C3 | 3 | conclusion: 5 MWh should land at/below low end of 30-62% range | none | n/a |
| C4 | 1 | Li-ion cost scales near-linearly to 5 MWh | A-9 (near-linear Li-ion cost scaling) | n/a — already in Table |
| C4 | 2 | Carnot-battery cost dominated by non-scaling power equipment | none | n/a |
| C4 | 3 | reference-scale LCOS barely clears competitiveness bar | none | n/a |
| C4 | 4 [2nd, actor lens] | financing/bankability risk premium widens effective gap | A-11 (financing risk premium not captured in LCOS) | yes — added to Table |
| C4 | 5 [2nd, time lens] | cost-decline-rate gap widens absent standardization | A-12 (standardization will not emerge fast enough near-term) | yes — added to Table |
| C4 | 6 | conclusion: 5 MWh molten-salt costs substantially more per kWh than Li-ion, gap widening | none | n/a |

Two assumptions (A-11, A-12) were surfaced during this audit that were not already in the Phase 2 Classified Assumptions Table; both have been added to that table (section 2) as A-11 and A-12, and the originating steps above are marked accordingly. All other chain steps introduced no assumption beyond what the Phase 2 table already carried — a clean pass for those rows, not an error.

## Techniques not applied (process output)

trade-off — not applicable — the task evaluates the plausibility of a single compound factual claim; chains C1-C4 disqualify the molten-salt option on both axes rather than leaving two comparably viable options to weigh (see §5 Abandoned Reasoning for the explicit test-and-reject of this framing).
fishbone — not applicable — the assumption space was enumerable directly from the claim's stated mechanism and components (charging method, discharge cycle, temperature range, cost structure) without needing a category-based breadth brainstorm.
pre-mortem — not applicable — the headline conclusion is a claim (a plausibility verdict), not a plan or recommendation; per the inversion-vs-pre-mortem decision rule, inversion is the applicable Phase 5 adversarial technique and is applied in the adversarial pass record below.

## §6→§4 closure ledger (process output)

- "Treat the compound claim as false as stated... (chain C1)...(chain C2)...(chain C3)...(chain C4)" → chains C1, C2, C3, C4 ✓ (cited inline)
- "The claim's plausibility depends on two conflations... (chain C2)...(chains C3, C4)" → chains C2, C3, C4 ✓ (cited inline)
- "This verdict is scoped to the specific claim under test... (chain C2)" → chain C2 ✓ (cited inline)
- "**Confidence:** MEDIUM — the resistive-architecture half... rests on C1... also rests on C2, C3, and C4..." → chains C1, C2, C3, C4 ✓ (cited inline)

Every §6 claim carries at least one inline chain citation; no claim required ledger-only discharge and no claim was cut.

## Self-audit scan (process output)

| Chain | Chain Head (brief) | Form conforming? | Rule applied | Dependency clean? | Band | Act attempted? | Edges fired |
|-------|---------------------|-------------------|---------------|--------------------|------|-----------------|-------------|
| C1 | GT-1 + GT-2 + GT-3 (Carnot law, Joule heating, reject-temp baseline) | yes | n/a | yes | HIGH | no | none |
| C2 | GT-6? + GT-7? + GT-8? (published Carnot-battery/Malta/Echogen RTE figures) | yes | n/a | yes | MEDIUM | no | none |
| C3 | C2 + GT-10? + GT-12? (reference-scale RTE, scale economics, kW-scale ORC) | no | one-inference rule — hop 1 joins a cost-scaling citation and a separate efficiency-scaling inference via "and"; should be split into two hops | yes | MEDIUM | no | none |
| C4 | GT-9? + GT-10? + GT-11? (Li-ion cost, scale economics, LCOS threshold) | yes | n/a | yes | MEDIUM | no | none |

| §6 Span (brief) | Construct | Claim under R11? | R11 clause applied | Chain cited |
|-------------------|-----------|-------------------|----------------------|---------------|
| **Recommended approach:** Treat the compound claim as false... | bold lead-in | yes | colon closes the bold span — always a claim | C1, C2, C3, C4 |
| **Key insight:** The claim's plausibility depends on two conflations... | bold lead-in | yes | colon closes the bold span — always a claim | C2, C3, C4 |
| **Trade-offs acknowledged:** This verdict is scoped to... | bold lead-in | yes | colon closes the bold span — always a claim | C2 |
| **Pre-check:** head C1 (HIGH), C2 (MEDIUM)... | pre-check line | yes | pre-check line is itself a claim under the claim-inventory rule, cited by the chains named in its own head | C1, C2, C3, C4 |
| **Confidence:** MEDIUM — the resistive-architecture half... | bold lead-in | yes | colon closes the bold span — always a claim | C1, C2, C3, C4 |

Scan complete: 4 chain rows, one per section-4 chain block in order; 5 section-6 rows, one per construct in order — 5 claims under R11, 0 excluded. 1 chains malformed (C3), 0 claims untraced.

## Adversarial pass (process output)

**Technique:** Inversion (per the inversion-vs-pre-mortem decision rule, applied because the headline conclusion is a claim, not a plan). Procedure opened and read directly from `references/inversion.md` before application.

**Recompute.** Carnot ceiling arithmetic independently redone: 1 − 308.15/838.15 = 0.6323 (63.2%); 1 − 298.15/838.15 = 0.6443 (64.4%); 1 − 273.15/838.15 = 0.6741 (67.4%) — all match the figures used in chain C1 (63-64% baseline, 67.4% rival-sink test). GT-10?'s 1 MW→100 MW figure recomputes as (2.37−0.83)/2.37 = 64.98% ≈ 65%, matching the "≈65% reduction" used in chains C3/C4. The $150-400/kWh Li-ion bracket used in chain C4 is an analyst estimate/judgment bracket, not a deterministic combination of cited figures, so there is no further arithmetic to recompute on that hop beyond the judgment already disclosed as such.

**Sensitivity.** The single ground truth whose falsity would most change the conclusion is GT-7? (Malta's claimed distinction between a ≤60% electricity-only figure and an 85-95% CHP-credited figure) — it is `?`-marked. This is already named on the §6 `**Confidence:**` line with the verification that would resolve it (reading Malta's own technical material directly rather than secondary reporting); no new cap is applied here beyond that existing MEDIUM caveat. The weakest-link chain overall is C3 (the one chain also flagged non-conforming in the self-audit scan for joining two inferences in one hop).

**Rival.** For the headline conclusion as a whole, the strongest rival is "the claim is correct when read under a CHP-credited or thermal-retention efficiency metric rather than a pure electricity-to-electricity metric." Chain C2 directly addresses and rules this out, by showing every source that reports ≥85% explicitly ties that figure to CHP credit, while every source reporting pure-electricity RTE tops out at 56-62% — so this rival is not live; it is settled within C2 itself. For chain C1's narrower resistive-architecture result, the rival "a colder heat-rejection sink closes the gap" was tested and ruled out (see §5 Dead End: colder sink). For chain C4's cost direction, the rival "Li-ion is equally scale-penalized" was tested and ruled out (see §5 Dead End: Li-ion scale parity).

**Premise.** The headline conclusion has already turned out to be false — the 5 MWh molten-salt system described in the claim does, in fact, exceed 85% electricity round-trip efficiency and is cost-competitive with same-capacity lithium-ion.

**Causes (unfiltered, generated from three stakeholder viewpoints before grouping):**
- *Vendor/promoter viewpoint:* (1) "round-trip efficiency" in the original claim legitimately includes CHP credit as an accepted industry convention, so no conflation occurred; (2) a real small-scale containerized molten-salt/Carnot-battery product already exists today that beats the published economies-of-scale curves this analysis relied on.
- *Skeptical-physicist/reviewer viewpoint:* (3) an unconventional heat-pump/heat-engine combination exists, not surfaced by this search, with combined second-law efficiency high enough to clear 80%+; (4) the discharge heat engine actually rejects to a much colder sink than the 15-40°C ambient baseline assumed, legitimately raising the Carnot ceiling.
- *Cost-analyst viewpoint:* (5) the claim's unstated discharge duration is unusually long, shrinking the power block relative to storage capacity and avoiding the usual power-block cost penalty; (6) one or more of the nine `?`-marked ground truths (GT-4?, GT-6? through GT-12?) is simply wrong in the direction that favors the claim, since none were confirmed at their primary source in this run.

**Clusters (structural weaknesses, with the chain/GT ids each bears on):**
- **Terminology/metric ambiguity** (cause 1) — bears on chain C2, GT-7?, Assumption A-1.
- **Unsurveyed-technology / exhaustiveness limit** (causes 2, 3) — bears on chains C2, C3, C4 and GT-6?, GT-7?, GT-8?, GT-10?, GT-11? collectively; this review's search was not an exhaustive technology-landscape survey.
- **Rejection-temperature/architecture edge case** (cause 4) — bears on chain C1.
- **Unstated-duration scope ambiguity** (cause 5) — bears on chain C4, Assumption A-8.
- **Unread-at-source ground truths** (cause 6) — bears on chains C2, C3, C4 and every `?`-marked ground truth.

**Disposition (per cluster):**
- Terminology/metric ambiguity: **accepted risk** — mitigation already in place: §6's `**Confidence:**` line names GT-7? as the single most sensitive input and states the verification (reading Malta's own technical specifications directly) that would resolve it.
- Unsurveyed-technology/exhaustiveness limit: **accepted risk** — mitigation: chains C2 and C3 are worded as findings about "the surveyed literature," not as claims that no such system exists anywhere; no stronger claim is made than the evidence supports.
- Rejection-temperature/architecture edge case: **resolved**, not merely accepted — chain C1 already tests this rival explicitly (the 0°C sink test) and shows it does not change the conclusion; this is a plan change already incorporated before this adversarial pass, not a residual risk.
- Unstated-duration scope ambiguity: **accepted risk, with a named weak link** — this pass surfaces a weak link on chain C4 not previously stated on its confidence line: C4's cost comparison assumes an ordinary 1-10 hour discharge duration (per Assumption A-8); an unusually long duration (which would shrink the power block's share of total cost) is not ruled out by anything in this analysis and would weaken, though not reverse outright, C4's cost-gap finding.
- Unread-at-source ground truths: **accepted risk** — mitigation already in place throughout: every chain carrying a `?`-marked input is capped at MEDIUM confidence with its own named verification path, consistent with D-07; no further action is taken within this run's turn budget.

**Falsification.** The headline conclusion is false if a primary-source reading of any one of GT-6? through GT-11? reveals a real, commercially deployed (not merely a larger reference-scale) ≈5 MWh molten-salt or Carnot-battery system with a documented pure-electricity round-trip efficiency above 80% and a turnkey cost at or below the contemporaneous lithium-ion $/kWh benchmark for that scale and region.

## Self-Audit Gate (process output)

**Criterion 1: Identify Essence**
Quoted span: "Is it physically achievable for a 5 MWh molten-salt sensible-heat storage tank operating between 290°C and 565°C to convert electricity to heat and back at an electricity-to-electricity round-trip efficiency above 85%, and would a system built to do so be cost-competitive, per kWh of nameplate capacity, with a same-capacity lithium-ion battery system?"
Band: **Rigorous**
Justification: The Core problem sentence names the specific decision (not a restatement of the prompt's framing, not a symptom), and each of the four success criteria is a verb+subject+outcome triplet checkable directly against the Conclusion section (e.g., "the analysis explicitly distinguishes... thermal energy retention efficiency... from electricity round-trip efficiency") without further clarification; the statement names properties (5 MWh, 290-565°C, the two named sub-claims) unique to this problem.

**Criterion 2: Challenge Assumptions**
Quoted span (from the Assumption Audit scan): "Two assumptions (A-11, A-12) were surfaced during this audit that were not already in the Phase 2 Classified Assumptions Table; both have been added to that table (section 2) as A-11 and A-12, and the originating steps above are marked accordingly."
Band: **Rigorous**
Justification: All 12 rows use the four-type scheme correctly, every Verdict cell uses a leading token (Accept/Challenge/Discard) followed by an em-dash and a specific justification, multiple assumptions are challenged or discarded (not merely accepted), unverified entries used in chains carry "unverified — flagged," and the Assumption Audit scan confirms exhaustive coverage of every named chain step with two genuinely new assumptions correctly surfaced and folded back into the Phase 2 table.

**Criterion 3: Establish Ground Truths**
Quoted span: "`?`-marked: GT-4, GT-5, GT-6, GT-7, GT-8, GT-9, GT-10, GT-11, GT-12 (9 of 12). Read-at-source: GT-1 — derived directly via η=1−Tc/Th... No unsuffixed ground truth in this analysis feeds a HIGH-confidence chain without a named read-at-source location (GT-1, GT-2 feed chain C1, rated HIGH...)."
Band: **Rigorous**
Justification: The enumeration matches the actual suffixed entries in the Ground Truths list when checked against it (9 of 12, correctly listed by ID); every unsuffixed GT feeding the one HIGH chain (C1) names its read-at-source derivation; GT-4?'s failed WebFetch read is recorded as a specific Phase 3 failure record (source, DNS-unreachable reason) rather than silently dropped, satisfying Exception (a) for that entry, which feeds no chain at all and so triggers no HIGH-chain requirement.

**Criterion 4: Reason Upward**
Quoted span (from the Self-audit scan's chain-form table): "C3 | ... | no | one-inference rule — hop 1 joins a cost-scaling citation and a separate efficiency-scaling inference via \"and\"; should be split into two hops | yes | MEDIUM | no | none"
Band: **Sound**
Justification: Every conclusion has exactly one chain, each chain names its inputs in the prescribed head form, each has a genuine intermediate, the Abandoned Reasoning section documents four specific (non-generic) dead ends, no analogy is used as standalone evidence (GT-12? is explicitly flagged as illustrative-only, grounded in its own citation), and the end-of-phase Assumption Audit ran exhaustively — but chain C3's first hop departs from the one-inference-per-hop prescribed form by joining a cost-scaling citation and an efficiency-scaling inference via "and," an isolated, identifiable departure in one hop of one chain that does not invalidate the rest of the section, matching the Sound descriptor exactly rather than Rigorous.

**Criterion 5: Validate**
Quoted span: "The [Assumes: A-5] premise (parasitic losses scale unfavorably with size) is priced: even if A-5 were false... the chain's conclusion would still stand on the independent, well-established turbomachinery regularity that small (sub-5 MW) turbines exhibit lower isentropic efficiency than 50-100+ MW units..." (chain C3, confidence line, revised during this run's self-audit before scoring)
Band: **Rigorous**
Justification: Every chain's confidence line names its own GT-N? inputs and cited Cn's with verification paths and does not re-explain a cited chain's own reasoning; no chain with a `?`-marked input is rated HIGH; every chain is rated no higher than the lowest-rated chain its head cites; a calibration gap on chain C3 (an unpriced [Assumes: A-5] premise, which would have required two axes short and a LOW rating) was caught and fixed during this run's self-audit, before this gate was scored, restoring legitimate three-axis-licensed MEDIUM calibration on every chain; the adversarial pass record (inversion) is complete with all seven parts present, each cluster carrying a named disposition (one resolved, four accepted-with-mitigation), and a stated falsification condition.

**Criterion 6: Conclusion-to-Ground-Truth Traceability**
Quoted span (from the Self-audit scan's claim-inventory table): "**Key insight:** The claim's plausibility depends on two conflations... | bold lead-in | yes | colon closes the bold span — always a claim | C2, C3, C4" and "Scan complete: ... 5 claims under R11, 0 excluded... 0 claims untraced."
Band: **Rigorous**
Justification: Every one of the five section-6 claims (Recommended approach, Key insight, Trade-offs acknowledged, Pre-check, Confidence) traces inline to a named section-4 chain with no claim left untraced per the self-audit scan's reconciliation line; the Conclusion introduces no reasoning absent from section 4; the Key Insight names a non-obvious finding (the CHP-metric conflation and the reference-scale extrapolation error) distinct from, not a restatement of, the Recommended approach.

**Gate result:** cleared · passes: 1 · Fix/Repeat fired: no

## Structured summary (process output)

```json
{
  "schema_version": 1,
  "run_mode": "full-composer",
  "assumptions": [
    {"id": "A-1", "type": "convention", "verdict": "Challenge"},
    {"id": "A-2", "type": "untested belief", "verdict": "Challenge"},
    {"id": "A-3", "type": "convention", "verdict": "Challenge"},
    {"id": "A-4", "type": "current constraint", "verdict": "Accept"},
    {"id": "A-5", "type": "untested belief", "verdict": "Challenge"},
    {"id": "A-6", "type": "untested belief", "verdict": "Discard"},
    {"id": "A-7", "type": "current constraint", "verdict": "Challenge"},
    {"id": "A-8", "type": "untested belief", "verdict": "Challenge"},
    {"id": "A-9", "type": "current constraint", "verdict": "Accept"},
    {"id": "A-10", "type": "current constraint", "verdict": "Accept"},
    {"id": "A-11", "type": "untested belief", "verdict": "Challenge"},
    {"id": "A-12", "type": "current constraint", "verdict": "Accept"}
  ],
  "ground_truths": [
    {"id": "GT-1", "read_at_source": true},
    {"id": "GT-2", "read_at_source": true},
    {"id": "GT-3", "read_at_source": true},
    {"id": "GT-4", "read_at_source": false},
    {"id": "GT-5", "read_at_source": false},
    {"id": "GT-6", "read_at_source": false},
    {"id": "GT-7", "read_at_source": false},
    {"id": "GT-8", "read_at_source": false},
    {"id": "GT-9", "read_at_source": false},
    {"id": "GT-10", "read_at_source": false},
    {"id": "GT-11", "read_at_source": false},
    {"id": "GT-12", "read_at_source": false}
  ],
  "chains": [
    {"id": "C1", "confidence": "HIGH", "rests_on": ["GT-1", "GT-2", "GT-3"]},
    {"id": "C2", "confidence": "MEDIUM", "rests_on": ["GT-6?", "GT-7?", "GT-8?"]},
    {"id": "C3", "confidence": "MEDIUM", "rests_on": ["C2", "GT-10?", "GT-12?"]},
    {"id": "C4", "confidence": "MEDIUM", "rests_on": ["GT-9?", "GT-10?", "GT-11?"]}
  ],
  "dead_ends": [
    "Pushing the Carnot ceiling higher via a colder (sub-ambient/cryogenic) heat-rejection scheme",
    "Accepting Malta Inc.'s 85-95% figure as direct support for the claim's 85%+ electricity round-trip efficiency",
    "Assuming lithium-ion is equally cost-penalized at 5 MWh scale, producing near cost-parity rather than a Li-ion advantage",
    "Applying the weighted trade-off procedure to choose between molten-salt and lithium-ion"
  ],
  "techniques": {
    "applied": ["five-whys", "theoretical-limit", "estimate", "second-order", "inversion"],
    "not_applied": [
      {"technique": "trade-off", "phase": 4, "reason": "the task evaluates the plausibility of a single compound factual claim; chains C1-C4 disqualify the molten-salt option on both axes rather than leaving two comparably viable options to weigh"},
      {"technique": "fishbone", "phase": 2, "reason": "the assumption space was enumerable directly from the claim's stated mechanism and components without needing a category-based breadth brainstorm"},
      {"technique": "pre-mortem", "phase": 5, "reason": "the headline conclusion is a claim, not a plan or recommendation; per the inversion-vs-pre-mortem decision rule, inversion is the applicable Phase 5 adversarial technique"}
    ]
  },
  "gate": {
    "passes": [
      {
        "bands": ["Rigorous", "Rigorous", "Rigorous", "Sound", "Rigorous", "Rigorous"],
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
    "recommendation": "Treat the compound claim as false as stated. Read as a resistive-heating-charged thermal battery, 85%+ electricity round-trip efficiency is not an engineering shortfall but a physical impossibility — it exceeds the ≈63-64% Carnot ceiling for a heat engine running between 565°C and ambient (chain C1). Read as a heat-pump-charged \"Carnot battery,\" 85%+ pure-electricity round-trip efficiency is not forbidden in the ideal limit but has no real-world precedent at any demonstrated scale — the best documented figures are 56-62% at 10 MW-plus reference scale (chain C2), and a 5 MWh system should be expected at or below the low end of that range (chain C3). The cost-competitiveness sub-claim is also false at 5 MWh: published economies-of-scale data indicate a molten-salt system at this scale should cost substantially more per kWh than a same-capacity 2025 lithium-ion BESS, and the gap should be expected to widen rather than narrow over the next several years (chain C4).",
    "confidence": "MEDIUM",
    "rests_on": ["C1", "C2", "C3", "C4"]
  }
}
```
