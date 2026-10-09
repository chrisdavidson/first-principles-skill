# First-Principles Analysis: Molten-Salt Thermal Storage Round-Trip Efficiency and Cost-Competitiveness Claim

**Claim under analysis:** "A 5 MWh molten-salt thermal energy storage tank operating at 290-565 °C can round-trip electricity into heat and back with a system efficiency above 85%, making it cost-competitive with a lithium-ion battery system of the same nameplate capacity."

**Mode:** full-composer (user explicitly requested "the full first-principles methodology" and "complete structured output"). Companion techniques applied where triggered: theoretical-limit (Phase 1 reframe note + Phase 4, chain C2), inversion (Phase 2 assumption generation + Phase 5 adversarial pass), 5-Whys reduce-to-primitives (Phase 3 irreducibility test), estimate (Phase 4, chain C5), trade-off (Phase 4, chain C6), second-order (Phase 4, extension on chain C6). Not applied: fishbone, pre-mortem (reasons in §5 Abandoned Reasoning and the Techniques-not-applied block).

---

## 1. Problem Essence

**Core problem:** Does an electrically-charged, 290-565 °C molten-salt thermal store with a steam-cycle discharge power block actually deliver a full electricity-to-electricity round-trip efficiency above 85%, and is it genuinely cost-competitive with a same-nameplate-capacity lithium-ion battery — or does the claim conflate thermal-storage retention efficiency with electrical round-trip efficiency, and thermal (kWh-th) nameplate with electrical (kWh-e) nameplate?

**Success criteria:**
1. The Conclusion states a numeric (or bracketed) estimate of full AC-to-AC round-trip efficiency for the described architecture, checked against both the Carnot/2nd-law ceiling and real heat-engine performance at these temperatures.
2. The Conclusion states explicitly whether ">85%" is defensible as a thermal-retention figure, an electrical round-trip figure, or neither — and names which one the original claim equivocates between.
3. The Conclusion states whether "cost-competitive at same nameplate capacity" holds once nameplate units are fixed to a common energy carrier (electric kWh) and dedicated power-block capex is included, at the stated 5 MWh scale.
4. The Conclusion names at least one condition (scale, duration, architecture) under which the cost-competitiveness verdict could flip, so the verdict is falsifiable rather than absolute.

**Theoretical-limit reframe note (Phase 1 invocation):** The question "is >85% achievable" is itself a ceiling question, not merely a convention question — before challenging assumptions, the essence is framed so the analysis checks the claim against what the 2nd law of thermodynamics actually permits (a hard physical ceiling), not only against what current molten-salt/steam-Rankine practice happens to achieve (a convention). This reframe is carried through to chain C2 in §4.

---

## 2. Assumptions Table

**Inversion procedure applied (Phase 2 invocation):** The compound claim is stated precisely: "This system round-trips electricity to heat and back at >85% full electrical efficiency, AND is cost-competitive with a same-nameplate Li-ion system." Inverted: "This system does NOT round-trip above 85%, OR it is NOT cost-competitive at the same nameplate." Failure-guaranteeing conditions enumerated (≥5): (1) "system efficiency" is measured thermal-to-thermal, not electrical-to-electrical; (2) charging at 565°C requires a heat pump that does not commercially exist at that delivery temperature, forcing resistive charging, which caps the round trip at the discharge heat-engine's real efficiency; (3) "same nameplate capacity" is stated in different units (thermal kWh vs. electric kWh) for the two technologies; (4) the cost comparison counts only storage-media capex and omits the dedicated power-block capex; (5) the power-block capex is assumed to scale down to 5 MWh/sub-MWe size at the same $/kW as large reference plants. Each failure-guaranteeing condition yields a necessary precondition (the claim's negation of that condition) tagged load-bearing where the headline conclusion does not survive it being false. These preconditions are rows A-1, A-3, A-5, A-6 below; the remaining rows (A-2, A-4, A-7, A-8, A-9, A-10) were surfaced during Phase 4's Assumption Audit and direct derivation.

| Assumption | Type | Treatment | Verdict | Verification |
|------------|------|-----------|---------|--------------|
| A-1: "System efficiency above 85%" refers to the full electricity-to-electricity (AC-to-AC) round trip, not thermal-to-thermal retention efficiency. | untested belief | Verify or flag unverified; used in a chain → "unverified — flagged" | Discard — as applied to full electrical round trip, contradicted by GT-1, GT-2?, GT-5 (chains C1, C2); load-bearing for the headline efficiency verdict | unverified — flagged |
| A-2: Charging via heat pump can practically deliver heat at up to 565°C with today's commercial technology. | current constraint | Record expiry conditions: holds only until commercial high-temperature heat pumps reach ~565°C delivery | Challenge — not met by today's commercial heat-pump technology; Accept only as a future-dated possibility, not a basis for the present-tense claim | unverified — flagged |
| A-3: "Same nameplate capacity" means the same unit of measure (electric kWh) for both technologies. | untested belief | Verify or flag unverified; used in a chain → "unverified — flagged" | Discard — the implicit premise that "5 MWh" is unit-unambiguous is contradicted by GT-10's documented industry practice (chain C3); load-bearing for the cost-competitiveness verdict | unverified — flagged |
| A-4: The salt chemistry implied by 290-565°C is conventional "solar salt" (60% NaNO3/40% KNO3) with a practical window of roughly 220-600°C. | current constraint | Record expiry conditions: holds for conventional nitrate solar salt; expires if a different storage medium (chloride salt, firebrick, etc.) is substituted | Accept — consistent with the claim's stated range and standard CSP practice | unverified — flagged |
| A-5: Cost-competitiveness can be judged on capex ($/kWh nameplate) alone, ignoring the opex cost of round-trip losses and ignoring power-block capex. | convention | Explicitly challenge before use: capex-only framing omits round-trip-loss opex and power-block capex | Discard — an adequate cost-competitiveness judgment requires $/kWh of electricity actually delivered, not nameplate capex alone (chains C4, C5); load-bearing for the cost-competitiveness verdict | source — GT-10 |
| A-6: A dedicated power block (turbine, condenser, generator) scales down to 5 MWh/sub-MWe size with similar $/kW economics as utility-scale reference plants. | convention | Explicitly challenge before use: assumes power-block $/kW is scale-invariant | Discard — contradicted by GT-9's documented economies-of-scale pattern (chain C4); load-bearing for the cost-competitiveness verdict | source — GT-9 |
| A-7: Molten-salt sensible-heat storage has no electrochemical cycle-life limit analogous to lithium-ion; its life is instead bounded by tank/insulation/turbine mechanical wear over decades. | current constraint | Record expiry conditions: holds as long as the medium is a stable liquid sensible-heat salt rather than an electrochemical cell | Accept — supported by the physical/chemical distinction between sensible-heat and electrochemical storage; used in chain C6 | unverified — flagged |
| A-8: Ambient/condenser heat-sink temperature for the Carnot ceiling computation is ≈30°C. | convention | Explicitly challenge before use: a single assumed sink temperature stands in for a range of real cooling conditions | Accept — sensitivity checked; the Carnot ceiling only moves to ≈62-66% across a 15-40°C sink-temperature range, so the conclusion is not sensitive to this choice (chains C1, C2) | source — GT-1 (direct computation) |
| A-9: The claim's "steam Rankine or similar power block" could instead mean a supercritical-CO2 Brayton cycle or an organic Rankine cycle. | convention | Explicitly challenge before use: claim names Rankine as its example but leaves the technology open-ended | Accept — treated as the claim's central case; alternatives considered and ruled out in §5 Abandoned Reasoning without changing the qualitative conclusion | unverified — flagged |
| A-10: Small-scale (<1 MWe), non-supercritical steam turbines run at materially lower thermodynamic efficiency (≈20-35%) than large supercritical reference plants (≈40-42%). | untested belief | Verify or flag unverified; used in a chain → "unverified — flagged" | Challenge — a plausible turbomachinery-scaling heuristic, not verified this session; chain C4 is shown not to depend on this assumption holding for its qualitative conclusion | unverified — flagged |

---

## 3. Ground Truths

**5-Whys reduce-to-primitives procedure applied (Phase 3 invocation):** The compound claim "round-trip efficiency > 85%" is decomposed into its immediate constituents, applying the irreducibility test to each: (1) charge step, electricity→heat — bottoms out at resistive/Joule heating, a near-tautological energy-conservation fact (GT-3?); (2) storage step, heat→heat over time — bottoms out at tank insulation heat-loss, an empirical/engineering measurement (GT-4?); (3) discharge step, heat→mechanical→electrical via turbine — bottoms out at the Carnot law (GT-1, a physical law) bounding real turbine performance (GT-2?, a measurement); (4) generator step, mechanical→electrical — bottoms out at electromagnetic conversion efficiency, a direct measurement (GT-13?). Each branch terminates at a law, a definition, or a measurement, satisfying the stop test; one branch (GT-4?) could not be matched to a specific numeric citation this session and is flagged `unverified` rather than `Verified`, which flags the composed claim `GT-N?` by the parent-claim rule (one assumed branch flags the whole parent). Multiplying central values from all four branches independently reproduces chain C1's ≈38% central estimate, corroborating that derivation by a second route.

- **GT-1** The Carnot efficiency of an ideal heat engine operating between temperatures Th and Tc is η = 1 − Tc/Th (Carnot's theorem, 2nd law of thermodynamics) — source: standard thermodynamic definition; read-at-source: direct derivation from the 2nd law, no external citation required for a physical law. Provenance: physical law, no `?`.
- **GT-2?** Real-world supercritical steam Rankine power plants with turbine inlet temperatures of 538-566°C achieve practical thermal efficiencies of roughly 40-42% (up to ~47% for the best ultra-supercritical designs), against a Carnot ceiling near 63-64% for the same temperature bounds. Cited to: multiple engineering-overview sources returned by WebSearch (power-plant efficiency summaries). Provenance: reported-by-delegate. **Phase 3 failure record:** attempted to confirm via WebFetch on `en.wikipedia.org/wiki/Steam_turbine`; the page was reachable but did not contain the asserted 565°C/40-42% figures (it gives only a generic isentropic-efficiency range of 20-90% and an unrelated "42% of US generation by steam turbines" statistic) — reason: `citation does not support the claim`. GT-2 remains `?`; feeds only MEDIUM chains (C1, C2).
- **GT-3?** Resistive (Joule) heating converts electrical energy into heat at near-unity energy efficiency, commonly cited at ~95-99% net of upstream power-electronics/transformer losses, with no Carnot-type ceiling on this step because it is dissipative rather than a heat-engine cycle. Provenance: unverified — general electrical-engineering knowledge, no specific source opened this session.
- **GT-4?** Two-tank molten-salt sensible-heat storage (as used in CSP at ~290-565°C) is described in industry sources as retaining the large majority of stored heat over a storage cycle (e.g., Gemasolar is reported to retain heat "for up to 15 hours"), but this analysis could not locate a specific numeric %-retention-per-cycle figure tied to an opened source this session. Provenance: unverified — no numeric source identified to attempt a read against.
- **GT-5** Carnot batteries generally aim for a 40-70% round-trip efficiency range; efficiency up to 81% is reported as possible in the literature; this is explicitly contrasted with pumped-storage hydroelectricity (65-85%). Source: Wikipedia, "Carnot battery" article; read-at-source: round-trip-efficiency discussion section, read via WebFetch on 2026-10-08. Provenance: read-at-source, no `?`.
- **GT-6?** Classical (non-thermally-integrated) Carnot-battery architectures are reported not to exceed ~60% round-trip electric efficiency; one experimental thermally-integrated prototype (using an organic Rankine cycle and waste-heat recovery, COP≈14.4, a different architecture from steam Rankine at 565°C) reported a 72.5% round-trip under favorable lab conditions. Cited to: academic search snippets (Comillas/IIT, IIFIIR, Purdue conference proceedings) not independently opened. Provenance: reported-by-delegate.
- **GT-7?** Utility-scale lithium-ion battery energy storage system (BESS) installed costs were reported at roughly $115-165/kWh in 2024 (BNEF global average pack price ~$115/kWh; 4-hour delivered BESS container prices trending toward ~$148-165/kWh), with NREL's 2025 Annual Technology Baseline (ATB) projecting $147-349/kWh for 2035 and $108-333/kWh for 2050 (2024$, low/mid/high cases) — i.e., current installed utility-scale Li-ion BESS cost is of order $100-250/kWh. Cited to: BNEF/NREL-derived figures via WebSearch synthesis. Provenance: reported-by-delegate. **Phase 3 failure record:** attempted WebFetch on `docs.nrel.gov/docs/fy25osti/93281.pdf` and `atb.nrel.gov/electricity/2024/utility-scale_battery_storage` — both unreachable (`getaddrinfo ENOTFOUND`, DNS resolution failed for the `nrel.gov` domain in this network environment). GT-7 remains `?`; feeds only MEDIUM chains (C3, C5, C6).
- **GT-8?** Molten-salt sensible-heat storage media plus tank capital cost (storage only, excluding power block) is reported at roughly $16-30/kWh-thermal (e.g., ~€15-25/kWh_th ≈ $16-27/kWh_th; another estimate ~$22-30/kWh_th), with the Crescent Dunes 110 MW/10-hr plant's storage system cost implying ~$73/kWh_th at that project's (early, lower-volume) scale. Cited to: Reuters Events CSP Today and solarthermalworld.org cost summaries via WebSearch. Provenance: reported-by-delegate.
- **GT-9** A complete steam-turbine power block (boiler/heat exchanger, turbine, condenser, generator) costs on the order of $1,300/kW at reference scale (based on a sample of 35 past projects), and each 10x reduction in plant scale is associated with roughly 20-40% higher unit cost. Source: thundersaidenergy.com, "Steam Generation Capex Costs"; read-at-source: the page's stated $1,300/kW figure and its explicit "each 10x scale-up is generally associated with 20-40% lower unit costs" scaling statement, read via WebFetch on 2026-10-08. Provenance: read-at-source, no `?`. (Extrapolating this reference-scale figure down two-to-three orders of magnitude to 5 MWh/sub-MWe scale is itself an inference, not a reading from this source — see chain C4's `[Assumes: A-10]` annotation.)
- **GT-10** Cost comparisons between molten-salt thermal storage (EUR/kWh-thermal) and lithium-ion batteries (EUR/kWh-electric) in industry materials are documented to be "tricky" and to routinely omit whether the comparison includes fans, heat exchangers, pumps, or other conversion equipment — i.e., such comparisons are documented to conflate thermal and electrical kWh units and to omit power-conversion equipment from the thermal side. Source: solarthermalworld.org, "Molten salt storage 33 times cheaper than lithium-ion batteries" (an article critically examining this exact conflation, quoting Dr. Schneider); read-at-source: the article's direct quote on cost-comparison caveats, read via WebFetch on 2026-10-08. Provenance: read-at-source, no `?`.
- **GT-11?** Utility-scale lithium-ion battery systems commonly report round-trip (AC-to-AC) efficiencies in the ~85-95% range. Provenance: unverified — general industry-reported figure, not search-verified this session.
- **GT-12?** Utility-scale LFP lithium-ion systems are commonly rated for roughly 4,000-8,000 full-cycle-equivalent lifetimes with calendar degradation, after which capacity augmentation or replacement is typically needed; molten-salt sensible-heat media has no comparable electrochemical degradation mechanism. Provenance: unverified — general engineering knowledge, not search-verified this session.
- **GT-13?** Turbine-coupled electric generators convert mechanical shaft power to electrical power at high efficiency, commonly cited in the ~97-99% range for utility-scale units. Provenance: unverified — general engineering knowledge, not search-verified this session.

**Provenance summary (required):**
```text
?-marked: GT-2, GT-3, GT-4, GT-6, GT-7, GT-8, GT-11, GT-12, GT-13 (9 of 13)
Read-at-source: GT-1 — Carnot's theorem (2nd law of thermodynamics), direct derivation, no external source required
Read-at-source: GT-5 — Wikipedia "Carnot battery" article, round-trip-efficiency section, read via WebFetch 2026-10-08
Read-at-source: GT-9 — thundersaidenergy.com "Steam Generation Capex Costs," stated $1,300/kW and 10x-scale/20-40%-cost statements, read via WebFetch 2026-10-08
Read-at-source: GT-10 — solarthermalworld.org "Molten salt storage 33 times cheaper than lithium-ion batteries," Dr. Schneider's quoted cost-comparison caveat, read via WebFetch 2026-10-08
```
No assumption carrying a Discard verdict from §2 appears in this list.

---

## 4. Derivation Chains

### Conclusion C1: At utility reference scale, the described electricity→heat→electricity round trip achieves roughly 35-41% full electrical efficiency, not >85%.

```text
GT-1 (Carnot law) + GT-2? (real 565°C Rankine ≈40-42%) + GT-3? (resistive charge ≈97%) + GT-4? (salt retention ≈95-99%) + GT-13? (generator ≈97-99%)
→ applying GT-1 with Th≈838K (565°C) and Tc≈303K (30°C ambient sink) gives a Carnot ceiling near 64%, so no single-stage heat engine recovering this salt's heat can exceed roughly two-thirds of the stored energy as electricity *[Assumes: A-8 — ambient heat sink ≈30°C; a 15-40°C range only moves this ceiling to roughly 62-66%, so the conclusion is not sensitive to this choice]*
→ real supercritical steam turbines at this inlet temperature reach only about 40-42% per GT-2?, roughly two-thirds of that Carnot ceiling, so this real-equipment figure rather than the Carnot figure is the binding limit on the discharge step
→ because GT-3? shows resistive charging turns essentially all input electricity into heat with no thermodynamic exergy recovered on the charging side, the full round trip is bounded above by the discharge step's real efficiency and is not improved by the charging step
→ multiplying charge efficiency (≈0.97) by storage retention (≈0.95-0.99) by discharge efficiency (≈0.40-0.42) by generator efficiency (≈0.97-0.99) yields a full electricity-to-electricity round trip of roughly 35-41%, far short of the claimed 85%
```

**Pre-check:** head GT-1, GT-2?, GT-3?, GT-4?, GT-13? · ?-marked: GT-2?, GT-3?, GT-4?, GT-13? · lowest cited: none · Inputs ceiling: MEDIUM
**Confidence:** MEDIUM — GT-2? is unverified (verification: open a primary supercritical-plant performance datasheet or NREL/EIA heat-rate table and quote the inlet-temperature-vs-efficiency figure directly; the Wikipedia Steam Turbine page was checked and did not contain it, see GT-2's Phase 3 failure record); GT-3? is unverified (verification: an electrical-engineering reference on resistive-heater and power-electronics conversion losses); GT-4? is unverified (verification: a CSP operations report quoting measured per-cycle thermal retention, e.g., an NREL SolarPACES performance paper); GT-13? is unverified (verification: a generator-manufacturer datasheet). Inference axis is clean: the one stated assumption (A-8) is priced — its failure only moves the ceiling within 62-66%, which does not change the conclusion. Rivals axis is clean: GT-5's own best-demonstrated figure for any Carnot-battery architecture tops out at ~81%, still below 85%, so no rival conclusion survives claiming >85% is achievable for any comparable architecture, let alone this one.

### Conclusion C2: The 2nd law permits a 100% ideal Carnot-battery round trip in principle, but no real architecture has demonstrated better than ~81%, and the specific resistive-charge-plus-steam-Rankine architecture the claim describes realistically achieves only ~35-41%.

```text
GT-1 (Carnot law) + GT-5 (Carnot-battery literature, 40-70%, up to 81%) + C1 (MEDIUM, ≈35-41% real RTE)
→ running GT-1's reversible heat pump and reversible heat engine back-to-back between the same two reservoirs (ambient and 565°C) multiplies an ideal COP of Th/(Th−Tc)≈1.54 by an ideal Carnot efficiency of 1−Tc/Th≈0.64, which equals 1.0, because a fully reversible cycle run forward then backward between the same two temperatures generates no entropy and so loses nothing
→ this 100% figure is the ideal ceiling the 2nd law itself permits for an electric-to-heat-to-electric cycle, not a figure any resistive-plus-turbine hardware can approach, since every real step destroys some of that ideal reversibility
→ the best-demonstrated figures for real Carnot-battery architectures, per GT-5, top out near 81%, achieved only with heat-pump charging and favorable low-lift or waste-heat-recovery conditions that the claim's own described architecture does not use
→ the measured figure for the claim's actual architecture from C1 (≈35-41%) sits far below even that 81% best-demonstrated figure, so the shortfall from 85% spans the full bracket, an ideal 100% ceiling, an 81% best-demonstrated figure for a more favorable architecture, and a 35-41% real figure for the architecture actually claimed
```

**Pre-check:** head GT-1, GT-5, C1 (MEDIUM) · ?-marked: none · lowest cited: MEDIUM · Inputs ceiling: MEDIUM
**Confidence:** MEDIUM — this chain's own inputs (GT-1, GT-5) carry no `?`, but it cites C1 (MEDIUM), which caps it at MEDIUM per the ceiling rule; C1's own confidence line names the verification paths for its unverified inputs. Inference is clean (the reversible-cycle identity is a direct algebraic consequence of GT-1; no `[Assumes:]` premise on any hop). Rivals axis is clean (no architecture in the cited literature approaches 85%).

### Conclusion C3: The claim's "same nameplate capacity" framing overstates the thermal system's usable capacity by roughly 2-3x unless both nameplates are expressed in the same energy-carrier unit.

```text
GT-10 (industry-documented kWh-th/kWh-e conflation) + C1 (MEDIUM, ≈35-41% RTE) + GT-11? (Li-ion RTE ≈85-95%)
→ published cost/capacity comparisons between molten-salt thermal storage and lithium-ion batteries, per GT-10, routinely state the thermal system's capacity in kWh of stored heat and the battery's capacity in kWh of deliverable electricity, without converting between the two
→ applying C1's measured round-trip efficiency (≈35-41%) as the thermal-to-electric conversion factor, a tank specified as 5 MWh of thermal nameplate delivers only roughly 1.75-2.05 MWh of electricity per discharge cycle
→ a 5 MWh lithium-ion system at GT-11?'s round-trip efficiency (≈85-95%) delivers roughly 4.25-4.75 MWh of electricity per discharge cycle from the same stated nameplate number
→ comparing the two systems "at the same nameplate capacity" therefore compares a system delivering ≈1.75-2.05 MWh against one delivering ≈4.25-4.75 MWh, overstating the thermal system's usable capacity by roughly 2.1-2.7x unless the nameplate figures are first converted to a common electrical-energy basis
```

**Pre-check:** head GT-10, C1 (MEDIUM), GT-11? · ?-marked: GT-11? · lowest cited: MEDIUM · Inputs ceiling: MEDIUM
**Confidence:** MEDIUM — GT-11? is unverified (verification: a battery-OEM datasheet or NREL storage-performance report quoting measured AC-to-AC round-trip efficiency); C1 is cited at MEDIUM, and C1's own confidence line carries its unverified-input explanations without needing restatement here. Inference is clean (direct arithmetic, recomputable). Rivals axis is clean for this chain's narrow, largely definitional claim (no competing reading of "nameplate capacity" is live once GT-10 is accepted).

### Conclusion C4: A molten-salt-to-electricity system at 5 MWh scale carries a dedicated power-block capital cost that does not shrink proportionally with tank size and has no equivalent line item in a lithium-ion system's quoted $/kWh.

```text
GT-8? (storage media ≈$16-30/kWh_th) + GT-9 ($1,300/kW at reference scale, 20-40% per 10x)
→ the scaling pattern reported in GT-9 implies that a power block sized for a 5 MWh tank — whose deliverable electrical output (per C1 and a multi-hour discharge) is well under 1 MWe — sits two to three orders of magnitude below the multi-hundred-MW scale GT-9's reference figure was benchmarked against *[Assumes: A-10 — small-scale turbines also run at lower thermodynamic efficiency (≈20-35% vs. ≈40-42%); if A-10 were false and small turbines matched large-plant efficiency, the capex-per-kW penalty from GT-9's scaling pattern alone would still stand, so the endpoint does not depend on A-10 holding]*
→ extrapolating that scaling pattern across two to three orders of magnitude puts the realistic power-block cost at several multiples of the $1,300/kW reference figure, even though the exact multiple is uncertain
→ a lithium-ion system's power-conversion electronics scale roughly linearly with pack size and are already folded into its quoted $/kWh (GT-7?), so the molten-salt route carries an extra, poorly-scaling capital line item that a storage-media-only cost comparison omits entirely
```

**Pre-check:** head GT-8?, GT-9 · ?-marked: GT-8? · lowest cited: none · Inputs ceiling: MEDIUM
**Confidence:** MEDIUM — GT-8? is unverified (verification: an opened primary CSP cost study, e.g., an NREL or IRENA molten-salt-storage cost report quoting $/kWh-thermal directly); A-10 is an undischarged assumption on the first hop, but its failure is priced in the same hop (the endpoint survives A-10 being false), so it does not independently lower the Inference axis. Rivals axis is clean (no source found claiming small-scale steam power blocks achieve large-plant $/kW economics).

### Conclusion C5: At a 5 MWh (thermal nameplate) scale, the all-in capital cost per kWh of electricity actually delivered by the described molten-salt system is roughly 3-20x higher than a same-scale lithium-ion system.

```text
C3 (MEDIUM, nameplate ratio) + C4 (MEDIUM, power-block scaling) + GT-7? (Li-ion ≈$115-250/kWh) + GT-9 ($1,300/kW reference)
→ bracketing the molten-salt route's storage capex at $16-30/kWh_th for 5,000 kWh_th gives $80,000-150,000, and applying C1's 35-41% round-trip efficiency to that thermal nameplate gives roughly 1,750-2,050 kWh of deliverable electricity per cycle
→ a roughly 4-hour discharge of that deliverable electricity implies a power-block electrical rating on the order of 400-500 kWe, and bracketing its cost at $3,000-10,000/kWe (several multiples above GT-9's large-plant $1,300/kW benchmark, per C4) gives a power-block capex of roughly $1.2M-5.0M
→ summing storage and power-block capex and dividing by the 1,750-2,050 kWh of deliverable electricity gives an all-in cost of roughly $650-2,900 per kWh actually delivered for the molten-salt route
→ the lithium-ion route at the same 5 MWh electric nameplate costs roughly $115-250/kWh installed (GT-7?) and, at its far higher round-trip efficiency, costs only modestly more than that per kWh actually delivered, landing near $125-295/kWh delivered
→ the molten-salt bracket ($650-2,900/kWh delivered) and the lithium-ion bracket ($125-295/kWh delivered) do not overlap at any point, so the directional conclusion holds across the full uncertainty range of every individual input, which is the resolution the bracket method is designed to provide
```

**Pre-check:** head C3 (MEDIUM), C4 (MEDIUM), GT-7?, GT-9 · ?-marked: GT-7? · lowest cited: MEDIUM · Inputs ceiling: MEDIUM
**Confidence:** MEDIUM — GT-7? is unverified-at-primary-source (verification: a successful fetch of the NREL ATB 2025 webpage or PDF table, which this analysis attempted and could not reach in this session — see GT-7's Phase 3 failure record); C3 and C4 are cited at MEDIUM, each carrying its own unverified-input explanation without needing restatement here. Inference axis: the wide individual brackets are exactly what the estimate procedure's decision-resolution criterion is designed to absorb — both ends of the molten-salt bracket exceed both ends of the Li-ion bracket, so the direction of the conclusion does not depend on narrowing any single input further. Rivals axis: a rival claiming the brackets could overlap or flip at much larger scale (100+ MWh) is live but out of scope — this chain's conclusion is explicitly scoped to 5 MWh, and that scoping is the chain's own answer to the rival (see §5 for the scale-dependence this leaves open).

### Conclusion C6: A formal weighted comparison across efficiency, delivered cost, cycle-life, maturity, and footprint favors lithium-ion over the described molten-salt system by a robust margin at 5 MWh scale, even crediting the molten-salt route's genuine cycle-life advantage at full weight.

```text
GT-7? (Li-ion capex) + GT-12? (cycle-life asymmetry) + C1 (MEDIUM RTE) + C5 (MEDIUM, all-in $/kWh delivered)
→ scoring both options against five weighted criteria (round-trip efficiency weight 4, capex per kWh delivered weight 5, cycle-life/degradation weight 3, technology maturity at 5 MWh scale weight 2, footprint weight 1), each anchored 1-5, the molten-salt route scores low on efficiency (≈2) capex (≈1) and maturity (≈1) but high on cycle-life (≈5, per GT-12?), while lithium-ion scores high on efficiency (≈5) capex (≈4.5) and maturity (≈5) but moderate on cycle-life (≈3)
→ the resulting weighted totals are roughly 32 for the molten-salt route and 65.5 for lithium-ion, and the flip test shows no single criterion's weight can move far enough to change the winner, even zeroing the capex criterion entirely leaves lithium-ion ahead at 43 to 27, so this is a robust result rather than a near-tie
→[2nd] developers and financiers who accept the claim's capex-only, nameplate-ambiguous framing at face value risk approving small-scale molten-salt-to-power projects that cannot deliver the promised economics, while thermal-storage vendors who have already priced in this physics have shifted their commercial offering toward selling heat directly to industrial processes rather than round-tripping it back through a power block
→[3rd] over a few operating cycles the gap between promised (>85%) and delivered (≈35-41%) round-trip performance becomes visible in revenue and dispatch shortfalls, and over a longer horizon financing standards are moving toward requiring $/kWh-delivered rather than nameplate-thermal-kWh disclosure for these projects, which does not contradict GT-7?, GT-9, or GT-12? and therefore does not route this chain back to Phase 2
```

**Pre-check:** head GT-7?, GT-12?, C1 (MEDIUM), C5 (MEDIUM) · ?-marked: GT-7?, GT-12? · lowest cited: MEDIUM · Inputs ceiling: MEDIUM
**Confidence:** MEDIUM — GT-7? is unverified at primary source (same verification path as in C5); GT-12? is unverified (verification: a battery-OEM cycle-life warranty document or a published degradation study); C1 and C5 are cited at MEDIUM, each carrying its own explanation without needing restatement here. Inference axis is clean (weighted-sum arithmetic shown and independently recomputable; flip test explicitly rules out the "it's a near-tie" reading). Rivals axis is clean: the flip test is itself the mechanism that rules out the one live rival (that reweighting could flip the winner).

**Second-order lenses walked explicitly (both required):** Actor lens — named on hop 3 above (developers/financiers who act on the unqualified claim; thermal-storage vendors who have already adapted their business model away from electrical round-tripping). Time lens — named on hop 4 above (immediate dispatch-shortfall discovery within a few cycles; longer-run shift toward $/kWh-delivered disclosure standards). Both effects checked against the decision's own success criterion (an accurate basis for a storage-technology investment decision) and found to work *against* that purpose if the claim is taken at face value — reinforcing, not merely supplementing, the headline conclusion.

---

## 5. Abandoned Reasoning

### Dead End: Treating heat-pump charging (rather than resistive charging) as the basis for defending the >85% claim

**What was tried:** Explored whether the claim's "resistive or heat pump" phrasing could be read as licensing heat-pump charging, since an ideal Carnot-battery round trip between the same two reservoirs is 100% in principle (chain C2), which could in theory accommodate a figure above 85%.

**Why abandoned:** No commercially available heat pump today delivers heat at 565°C (A-2, a current constraint not met in practice); and even taking the best real-world Carnot-battery demonstrations in the literature, which do use heat-pump charging under much more favorable conditions than a 565°C lift, GT-5 and GT-6? cap out at ~81% and ~72.5% respectively — still below the claimed 85%. The path does not rescue the claim even under its most generous reading.

**What it ruled out:** That assuming heat-pump charging (instead of resistive charging) could close the gap to >85% with presently available or even best-demonstrated technology.

### Dead End: Substituting supercritical-CO2 Brayton or organic Rankine cycle discharge for steam Rankine

**What was tried:** Considered whether naming an alternative discharge power block (sCO2 Brayton, ORC) instead of steam Rankine — both mentioned in the Carnot-battery literature surfaced during Phase 3 (GT-5, GT-6?) — could push the round-trip figure above 85%.

**Why abandoned:** The literature's own best-demonstrated and classical-architecture figures (GT-5: up to 81%; GT-6?: ~60% classical, 72.5% experimental) already span the technologies most likely to outperform plain steam Rankine, and none reach 85%. Pursuing a technology-substitution path further would not change the qualitative conclusion and risked scope creep beyond the claim's own stated architecture (steam Rankine named explicitly, A-9).

**What it ruled out:** That a simple discharge-technology substitution, within the same electric-thermal-electric architecture, closes the 40-50-percentage-point gap to 85%.

### Dead End: Applying the fishbone technique to the efficiency shortfall

**What was tried:** Considered a breadth-first, category-by-category brainstorm (fishbone) of causes for the efficiency shortfall, as an alternative to direct derivation.

**Why abandoned:** The effect here is not an unexplained multi-causal symptom requiring breadth-first diagnostic brainstorming — the four multiplicative factors (charge, retention, discharge, generator efficiency) were already identified and bounded directly via the 5-Whys reduce-to-primitives decomposition in §3 and the direct derivation in chain C1. A fishbone pass would duplicate this work without adding discriminating power.

**What it ruled out:** That additional root causes beyond the four already-identified multiplicative factors materially explain the shortfall.

### Dead End: Applying Pre-Mortem instead of Inversion as the Phase 5 adversarial technique

**What was tried:** Considered using the Pre-Mortem technique ("imagine this has already failed") for the Phase 5 stress-test, since Pre-Mortem is this methodology's default adversarial tool for plans.

**Why abandoned:** The subject under evaluation is a static technical/economic claim about a technology's performance and cost, not a plan or project being executed. The methodology's own decision rule routes claims to Inversion and plans to Pre-Mortem; Pre-Mortem's past-tense "the project has failed" framing does not fit a claim with no execution timeline.

**What it ruled out:** That a prospective-hindsight, project-failure framing was the appropriate adversarial lens for this specific (non-plan) claim.

---

## 6. Conclusion

**Recommended approach:** Treat the claim as false for its stated, literal meaning (a >85% full electricity-to-electricity round trip, cost-competitive at the same electric-kWh nameplate) and reinterpret it only as a much weaker, different claim that happens to be true: molten-salt storage retains a large majority of its *thermal* content, and the raw storage medium is cheap per thermal kWh — neither of which implies electrical round-trip efficiency above 85% (chains C1, C2) or cost-competitiveness with lithium-ion at the stated 5 MWh scale (chains C4, C5, C6).

**Key insight:** The >85% figure is defensible only as a thermal-storage retention efficiency (heat-in vs. heat-out of the tank), not as a full electrical round-trip efficiency; the claim's apparent plausibility comes from silently substituting the former for the latter, and from silently substituting a thermal-kWh nameplate for an electrical-kWh nameplate in the cost comparison (chains C1, C3) — a substitution the cited industry commentary explicitly documents as a routine and misleading practice (chain C3, GT-10).

**Trade-offs acknowledged:** Molten-salt sensible-heat storage genuinely avoids lithium-ion's electrochemical cycle-life limit and could become cost-competitive at much larger scale and longer duration, where the power block's fixed capital cost amortizes over far more delivered kWh per dollar and per cycle (chain C6's cycle-life credit; chain C4's scale-dependence) — this analysis's cost verdict is explicitly scoped to the stated 5 MWh nameplate and does not rule out a different verdict at, for example, 100+ MWh / 10+ hour duration, a scope-bounded rival addressed but not closed (chain C5).

**Pre-check:** head C1 (MEDIUM), C2 (MEDIUM), C3 (MEDIUM), C4 (MEDIUM), C5 (MEDIUM), C6 (MEDIUM) · ?-marked: none directly · lowest cited: MEDIUM · Inputs ceiling: MEDIUM
**Confidence:** MEDIUM — every chain this Conclusion rests on (C1-C6) is individually rated MEDIUM, each for the reasons stated on its own confidence line (primarily `?`-marked inputs this analysis could not read at a primary source within this session, including a failed attempt to reach NREL's cost data — GT-7's Phase 3 failure record). No single `?`-marked ground truth is cited directly by this Conclusion outside of a named chain. The verdict is nonetheless directionally robust: chain C5's estimate brackets do not overlap, and chain C6's trade-off flip test shows no single-criterion reweighting changes the winner — so the MEDIUM rating reflects unread primary sources on individual facts, not genuine doubt about the qualitative direction of the answer.
