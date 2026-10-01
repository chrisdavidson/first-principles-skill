## Answer

**Recommendation:** Reject the claim. With resistive charging, an 85% electricity-to-electricity round trip is beyond what thermodynamics allows. The ceiling is 78.05% even with Earth's coldest recorded sink (chain C1), and 56.89% with a 25 °C sink (chain C2). With heat-pump charging, 85% is not excluded by physics, but no figure read supports it (chain C3). The cost-competitiveness conclusion does not follow from the claim (chain C5).

**Band (from §6):** MEDIUM. The resistive-charging verdict on its own is HIGH (chain C1).

**Would change it:** A measured round trip of 85% or more from an operating heat-pump-charged plant (chain C3), or a published Rankine efficiency for this scale together with a stated basis for the nameplate figure (chain C4).

## 1. Problem Essence

**Core problem:** Do the laws of thermodynamics allow a molten-salt store that swings between 290 °C and 565 °C to turn electricity into heat and back at better than 85% round-trip efficiency? And if not, does anything in the claim still support its conclusion that the store is cost-competitive with a lithium-ion system of the same nameplate capacity?

The claim has two parts joined by "making it": a physical-efficiency premise and an economic conclusion drawn from that premise. Phase 1 used the theoretical-limit reframe: is 85% a figure engineering could reach, or is it beyond the physical ceiling? The analysis answers that before it looks at cost, because a premise that breaks a physical law cannot support any conclusion drawn from it.

**Success criteria:**
- The highest round-trip efficiency the laws permit for a 290–565 °C store is derived with its arithmetic shown, recomputed, and compared with 85%.
- Both ways of reading "electricity into heat" are covered: resistive (Joule) charging and heat-pump charging.
- The "same nameplate capacity" comparison is tested for whether both sides are measured on the same basis (thermal MWh versus electric MWh).
- The inference from efficiency to cost-competitiveness is judged on whether it follows, separately from whether its premise is true.
- Each part of the claim gets a verdict (false / unsupported / undetermined), and each verdict carries a confidence band and names the evidence that would change it.

## 2. Assumptions Table

The rows are referred to as A-1 to A-14, in the order listed. A-11 and A-12 came out of the Phase 2 inversion pass. A-13 and A-14 came out of the Phase 4 Assumption Audit.

| Assumption | Type | Treatment | Verdict | Verification |
|------------|------|-----------|---------|--------------|
| No heat engine can exceed the Carnot efficiency 1 − Tc/Th between its reservoirs | physical law | Accept as a ground-truth candidate | Accept — physical law, becomes GT-1 | Wikipedia "Carnot heat engine": formula and Carnot's theorem quoted (GT-1) |
| Resistive (Joule) heating turns 1 J of electricity into at most 1 J of heat | physical law | Accept as a ground-truth candidate | Accept — first law, becomes GT-3 | Wikipedia "Joule heating": "every joule of electrical energy supplied produces one joule of heat" (GT-3) |
| "Round-trip electricity into heat" means resistive charging | untested belief | Verify, or flag as unverified | Challenge — Joule heating is the usual way molten-salt stores are charged, but a heat pump (COP > 1, GT-3 passage) is also possible, so both readings are analysed: C1/C2 for resistive, C3 for heat pump | Both readings carried; no reading assumed |
| Heat is rejected to an ambient sink at about 25 °C (298.15 K) | convention | Challenge before use | Challenge — used only for the figure in C2; C1 instead uses the coldest sink ever recorded on Earth, which favours the claim, and the claim still fails | GT-6? unverified — flagged; C1 does not depend on it |
| Discharge runs through a steam Rankine cycle at about 40–42% net efficiency | untested belief | Verify, or flag as unverified | Challenge — not read at any source | GT-8? unverified — flagged; only C4 uses it |
| The whole 290–565 °C swing is usable sensible heat at constant specific heat | untested belief | Verify, or flag as unverified | Accept — the range is the claim's own premise (GT-4); constant cp is a modelling simplification that leaves the mean-temperature result essentially unchanged for a gently varying cp | Range read at source (GT-4); constant cp is unverified — flagged on C2 |
| "Same nameplate capacity" compares like with like | convention | Challenge before use | Challenge — the tank's nameplate is thermal MWh and a Li-ion nameplate is electric MWh; tested in C4 | C4 |
| A higher round-trip efficiency makes the store cost-competitive | untested belief | Verify, or flag as unverified | Discard — efficiency is one input to cost per delivered kWh; capital cost per kWh and per kW also set it, and the claim gives neither (C5) | C5 |
| Li-ion round-trip efficiency is about 85–90% | untested belief | Verify, or flag as unverified | Challenge — the Grid energy storage page gave no figure | unverified — flagged; not used in any chain |
| Solar salt cp is about 1.5 kJ/kg·K | untested belief | Verify, or flag as unverified | Challenge — the Thermal energy storage page gave no cp | GT-10? unverified — flagged; used only in a §5 dead end |
| Standby heat losses between charge and discharge are negligible (inversion precondition, not load-bearing) | untested belief | Verify, or flag as unverified | Accept — conservative: any loss lowers efficiency further, so assuming none favours the claim | GT-4 passage: heat "can be usefully stored for up to a week"; no loss figure was read |
| Each machine in a heat-pump-charged store can run at at least 92.2% of its Carnot limit (inversion precondition, load-bearing for the heat-pump reading) | untested belief | Verify, or flag as unverified | Challenge — the 40–70% range GT-7 says these systems aim for implies at most 83.7% per machine | C3; unverified — flagged |
| Ideal heat pump and engine working across the same temperature profile give a round trip of exactly 1, with no losses from the temperature differences needed to move heat (surfaced by the audit on C3) | untested belief | Verify, or flag as unverified | Accept — conservative: real temperature differences only lower the product, which favours the claim | The ideal product was recomputed as 1.7579 × 0.5689 = 1.0000; the no-loss premise is unverified — flagged on C3 |
| The cost of each delivered kWh depends on capital cost as well as efficiency (surfaced by the audit on C5) | physical law | Accept as a ground-truth candidate | Accept — follows from the definition of levelised cost: capital plus energy purchase, divided by energy delivered | Definitional; used only to show the claim's inference is incomplete |

## 3. Ground Truths

Each candidate was reduced to primitives (the 5-Whys reduce-to-primitives mode). GT-1 and GT-3 bottom out at physical laws, GT-2 at a definition, and GT-4, GT-5, GT-7 and GT-9 at quoted published figures.

- **GT-1** No heat engine running between a hot reservoir at Th and a cold reservoir at Tc can convert heat to work more efficiently than η = 1 − Tc/Th, with both temperatures in kelvin. Type: physical law. Source: Wikipedia, "Carnot heat engine". Read at source: the formula "η_I = W/Q_H = 1 − T_C/T_H" and "No heat engine can be more efficient than a completely reversible one operating between the same temperatures."
- **GT-2** T(K) = T(°C) + 273.15. Type: definition (SI). Source: SI definition, cross-checked against the quoted conversion in GT-5. Read at source: "−89.2 °C (−128.6 °F; 184.0 K)", and −89.2 + 273.15 = 183.95 ≈ 184.0.
- **GT-3** Resistive heating gives exactly one joule of heat per joule of electricity, while a heat pump can give more than one. Type: physical law (first law). Source: Wikipedia, "Joule heating". Read at source: "every joule of electrical energy supplied produces one joule of heat" and "a heat pump can have a coefficient of more than 1.0 since it moves additional thermal energy from the environment".
- **GT-4** The tank swings between 290 °C and 565 °C, which matches commercial solar-salt practice. Type: published design value. Sources: the claim's own wording, and Wikipedia, "Thermal energy storage". Read at source: "kept liquid at 288 °C (550 °F) in an insulated 'cold' storage tank" and "heats it to 566 °C (1,051 °F)".
- **GT-5** The lowest natural temperature ever measured directly at ground level on Earth is −89.2 °C (184.0 K). Type: measured value. Source: Wikipedia, "Lowest temperature recorded on Earth". Read at source: "The lowest natural temperature ever directly recorded at ground level on Earth is −89.2 °C (−128.6 °F; 184.0 K) at the then-Soviet Vostok Station".
- **GT-6?** A typical heat-rejection sink is about 25 °C (298.15 K). Type: convention (an assumed design value). Unverified: no source was opened. This is a reference choice. A colder sink raises the C2 ceiling, and C1 bounds that case using GT-5.
- **GT-7** Carnot batteries generally aim for 40–70% round-trip efficiency. Type: published range (a target, not a measurement). Source: Wikipedia, "Carnot battery". Read at source: "Carnot batteries generally aim for a 40-70% efficiency range, significantly lower than pumped-storage hydroelectricity (65-85%)."
- **GT-8?** A steam Rankine cycle fed at about 565 °C achieves about 40–42% net heat-to-electricity efficiency. Type: estimate (not measured here). Unverified: no source was located or opened in this analysis — `not read — turn budget`.
- **GT-9** A sodium-sulfur battery, an electrochemical cell with a molten electrode and a ceramic electrolyte, is listed at 87% efficiency. Type: published value. Source: Wikipedia, "Molten-salt battery". Read at source: "Efficiency of 87%".
- **GT-10?** The specific heat of solar salt is about 1.5 kJ/kg·K. Type: estimate. Unverified: the "Thermal energy storage" page was opened and has no cp figure. Phase 3 failure record: citation does not support the claim. Used only in §5.

**Provenance summary:**

```text
?-marked: GT-6?, GT-8?, GT-10? (3 of 10)
Read-at-source: GT-1 — Wikipedia "Carnot heat engine", formula η_I = W/Q_H = 1 − T_C/T_H and Carnot's theorem sentence
Read-at-source: GT-2 — SI definition, checked against the GT-5 quoted conversion (−89.2 °C ↔ 184.0 K)
Read-at-source: GT-3 — Wikipedia "Joule heating", "every joule of electrical energy supplied produces one joule of heat"
Read-at-source: GT-4 — Wikipedia "Thermal energy storage", 288 °C cold tank / 566 °C hot passage
Read-at-source: GT-5 — Wikipedia "Lowest temperature recorded on Earth", Vostok −89.2 °C sentence
Read-at-source: GT-7 — Wikipedia "Carnot battery", "aim for a 40-70% efficiency range"
Read-at-source: GT-9 — Wikipedia "Molten-salt battery", NaS "Efficiency of 87%"
Phase 3 failure record: GT-10? — Wikipedia "Thermal energy storage" opened; no specific-heat figure present (citation does not support the claim)
Not read — turn budget: GT-8?
```

The Wikipedia pages were opened with a fetch tool that returns quoted passages. The quotes above are the passages it returned.

## 4. Derivation Chains

**How the sensible-heat ceiling used in C2 is derived:** when the salt cools from Th to Tl, each small amount of heat dQ = m·cp·dT is released at temperature T. GT-1 limits the work that can be drawn from it to dW = (1 − T0/T)·dQ. Integrating over the swing gives W = Q − T0·m·cp·ln(Th/Tl). That is the same as a Carnot engine running at the thermodynamic mean temperature Tm = (Th − Tl)/ln(Th/Tl).

**Theoretical-limit bracket.** Higher is better here, so the bound is an ideal ceiling.
- **Ideal ceiling** (resistive charging, 25 °C sink): 56.89% (C2). Even with Earth's coldest recorded sink and every joule leaving at 565 °C, the ceiling is 78.05% (C1).
- **Best demonstrated:** no demonstrated round-trip figure was read. GT-7 states an aim of 40–70%, not a record.
- **Conventional:** about 40% for resistive charging with steam discharge (GT-8?, unverified).
- **Gaps:** conventional to ideal ceiling is 56.89 − 40 = 16.89 points. Conventional to best demonstrated, and best demonstrated to ideal ceiling, cannot be split because no demonstrated figure was read.
- **The claim's 85%** is 85 − 56.89 = 28.11 points above the ideal ceiling. That is not headroom engineering could close: it is beyond what the laws allow.

### Conclusion C1: A resistive-charged 290–565 °C molten-salt store cannot reach 85% round-trip efficiency on Earth

GT-1 (Carnot bound) + GT-2 (kelvin offset) + GT-3 (Joule heating 1 J heat per 1 J electricity) + GT-4 (565 °C top temperature) + GT-5 (coldest recorded sink 184.0 K)
→ the hottest heat the tank ever holds is at 565 + 273.15 = 838.15 K
→ a Carnot efficiency of 85% from 838.15 K requires Tc ≤ (1 − 0.85) × 838.15 = 125.72 K, which is −147.43 °C
→ the coldest sink ever recorded gives at most 1 − 184.0/838.15 = 1 − 0.2195 = 78.05%, below 85%
→ resistive charging multiplies the discharge efficiency by at most 1, so the round trip cannot exceed the discharge efficiency
→ no resistive-charged 290–565 °C molten-salt store can reach 85% round trip with any heat sink on Earth's surface

**Pre-check:** head GT-1, GT-2, GT-3, GT-4, GT-5 · ?-marked: none · lowest cited: none · Inputs ceiling: HIGH
**Confidence:** HIGH — every input was read at source (see the §3 provenance summary). Every hop is arithmetic that recomputes, or follows directly from GT-1 and GT-3. Two rival readings are each settled. The heat-pump reading is outside this chain's scope and is handled by C3. The reading of "molten salt" as an electrochemical battery is ruled out in §5 by the claim's own words, "thermal energy storage tank" and "electricity into heat". The bound is generous to the claim: it assumes every joule is released at the 565 °C peak, even though the real mean temperature is lower (C2).

### Conclusion C2: With a 25 °C sink, the resistive round-trip ceiling for a 290–565 °C sensible-heat store is 56.89%

GT-1 (Carnot bound) + GT-2 (kelvin offset) + GT-3 (Joule heating factor 1) + GT-4 (290–565 °C swing) + GT-6? (25 °C sink)
→ the salt releases its heat between 838.15 K and 563.15 K, at a thermodynamic mean temperature Tm = 275/ln(838.15/563.15) = 275/0.39765 = 691.56 K (418.41 °C) *[Assumes: A-6 — constant cp across the swing]*
→ the ideal discharge efficiency is 1 − 298.15/691.56 = 1 − 0.43113 = 56.89%
→ with Joule charging at a factor of 1, the ideal round-trip ceiling is 56.89%, which is 28.11 points below 85% (85/56.89 = 1.494×)

**Pre-check:** head GT-1, GT-2, GT-3, GT-4, GT-6? · ?-marked: GT-6? · lowest cited: none · Inputs ceiling: MEDIUM
**Confidence:** MEDIUM — the short axis is Inputs: GT-6? (the 25 °C sink) is a reference choice that no source confirms. Fixing the sink at the design value for a named site would remove it as a cause of the downgrade. A-6 is priced: a cp that varies gently with temperature moves Tm only slightly. If constant cp failed badly, the endpoint figure would shift, but the conclusion that the store is below 85% would still stand, because C1 bounds it at 78.05% whatever the cp profile or sink.

### Conclusion C3: Under heat-pump charging the laws do not rule out 85%, but reaching it requires both machines to beat the technology's stated aim ceiling, so the premise is unsupported

GT-1 (Carnot bound) + GT-3 (heat pump COP > 1) + GT-7 (Carnot batteries aim for 40–70%)
→ an ideal heat pump delivering heat at Tm from a sink at T0 has COP = Tm/(Tm − T0)
→ an ideal engine returning that heat to electricity converts (Tm − T0)/Tm of it
→ the product of the two is exactly 1 for any temperatures, so the laws alone do not forbid 85% under heat-pump charging *[Assumes: A-13 — no losses from the temperature differences needed to move heat]*
→ if each machine reaches a fraction f of its Carnot limit, the round trip is f², so 85% requires f = √0.85 = 0.9220 per machine
→ the 70% top of GT-7's aim range corresponds to f = √0.70 = 0.8367 per machine
→ 85% therefore requires each machine to run 0.9220 − 0.8367 = 0.0853, or 8.53 percentage points of Carnot fraction, above the level implied by the technology's own stated aim ceiling
→ under heat-pump charging the 85% premise is unsupported by any figure this analysis read, although no physical law excludes it

**Pre-check:** head GT-1, GT-3, GT-7 · ?-marked: none · lowest cited: none · Inputs ceiling: HIGH
**Confidence:** MEDIUM — the short axis is Rivals. GT-7 states an aim, not a physical bound, so the rival "a future pair of machines will exceed 83.7% of Carnot each" is still live. A measured round trip of at least 85% from an operating heat-pump-charged molten-salt plant would settle it. Inference is priced: A-13 is conservative, because real temperature differences only lower the product, so its failure would strengthen this endpoint. If the two fractions differ, the requirement becomes a geometric mean of 0.9220, so the endpoint stands.

### Conclusion C4: "Same nameplate capacity" compares thermal MWh with electric MWh and overstates what the tank can deliver by 1.76× to 2.5×

C2 (56.89% ideal ceiling) + GT-8? (Rankine 40–42%)
→ 5 MWh of stored heat delivers at most 5 × 0.5689 = 2.844 MWh of electricity with ideal discharge
→ at a conventional 40% it delivers 5 × 0.40 = 2.00 MWh of electricity (2.10 MWh at 42%)
→ matching a Li-ion system's 5 MWh electric nameplate needs 5/0.5689 = 8.79 MWh of heat ideally, or 5/0.40 = 12.5 MWh conventionally
→ a 5 MWh thermal nameplate set against a 5 MWh electric nameplate overstates the tank's deliverable energy by 1/0.5689 = 1.758× to 1/0.40 = 2.5×

**Pre-check:** head C2 (MEDIUM), GT-8? · ?-marked: GT-8? · lowest cited: MEDIUM · Inputs ceiling: MEDIUM
**Confidence:** MEDIUM — the short axis is Inputs. C2 is rated MEDIUM. GT-8? (40–42% Rankine) is unverified; reading a published net efficiency for a steam cycle at 565 °C and this scale would remove it as a cause of the downgrade. If "5 MWh" instead means 5 MWh of electric output, the endpoint applies in reverse: the tank would need 8.79–12.5 MWh of heat. Either way the comparison is only valid once the basis is stated.

### Conclusion C5: The cost-competitiveness conclusion does not follow from the claim as written

C1 (resistive bound 78.05%) + C3 (heat-pump premise unsupported) + C4 (nameplate basis mismatch)
→ the efficiency premise that "making it" relies on is false under resistive charging and unsupported under heat-pump charging
→ cost per delivered kWh also depends on capital cost per kWh of storage and per kW of power block, and the claim states neither *[Assumes: A-14 — levelised cost has a capital term]*
→ the claim's cost conclusion is neither established nor refuted by what the claim provides
→[2nd] actor lens: a buyer who sizes the store at 85% buys 85/56.89 = 1.494× too little heat capacity even at the ideal ceiling, and 85/40 = 2.125× too little at conventional efficiency
→[2nd] time lens: the shortfall shows on the first cycle and recurs on every cycle, so energy delivered per cycle falls short by that factor for the asset's whole life
→[3rd] actor lens: a vendor whose sales case rests on 85% loses credibility at commissioning, which hides the store's real potential advantages (a cheap storage medium and long duration) that a capital-cost case could have argued
→[3rd] time lens: once the shortfall becomes the accepted view, comparisons default to round-trip efficiency, the metric this store loses on, rather than to cost per delivered kWh at long duration

**Pre-check:** head C1 (HIGH), C3 (MEDIUM), C4 (MEDIUM) · ?-marked: none · lowest cited: MEDIUM · Inputs ceiling: MEDIUM
**Confidence:** MEDIUM — the short axis is Inputs: C3 and C4 are rated MEDIUM. Inference: A-14 is definitional, so this hop holds. Rivals: the endpoint is itself a ruling-out of the claim's inference, so no rival is needed. The second-order extensions qualify downstream effects, not the endpoint. None of them contradicts a ground truth, and none works against the success criteria.

## 5. Abandoned Reasoning

### Dead End: Reading "molten salt" as an electrochemical molten-salt battery

**What was tried:** A sodium-sulfur battery (a molten-electrode cell) is listed at 87% efficiency (GT-9). On that reading the 85% figure would be plausible. This is the strongest rival to C1.

**Why abandoned:** The claim says "thermal energy storage tank" and "round-trip electricity into heat and back". The energy passes through heat, so GT-1 applies. An electrochemical cell does not convert through heat, so GT-9 is a fact about a different technology.

**What it ruled out:** Saving the claim by swapping in a different technology. C1 applies to the device the claim actually describes.

### Dead End: Using the Carnot efficiency at the 565 °C peak as the ceiling

**What was tried:** With a 25 °C sink, η = 1 − 298.15/838.15 = 1 − 0.35572 = 64.43%, used as the ideal ceiling. This is the rival reading of C2.

**Why abandoned:** It is a valid bound but not the tightest. The salt releases its heat across the whole 290–565 °C swing, not all at 565 °C, so the bound that applies is the mean-temperature bound in C2 (56.89%). Using 64.43% would overstate the headroom by 7.54 points. C1 keeps the peak-temperature form only because it is generous to the claim and the claim still fails it.

**What it ruled out:** Treating the peak-temperature Carnot figure as what the store can actually reach.

### Dead End: Settling cost-competitiveness with a Fermi estimate of the salt inventory

**What was tried:** The energy per kg is cp·ΔT = 1.5 × 275 = 412.5 kJ/kg, which is 412.5/3600 = 0.11458 kWh/kg. Storing 5 MWh of heat therefore needs 5000/0.11458 = 43,636 kg, about 43.6 t of salt.

**Why abandoned:** cp is GT-10?, whose cited page contains no cp figure. No salt, power-block or Li-ion price was read at any source. A cost verdict built on these would rest entirely on unverified figures, and the salt mass leaves out the power block (turbine, generator, heat exchangers), which is a separate cost the store needs before it can deliver electricity.

**What it ruled out:** Treating "the salt is cheap" as proof of cost-competitiveness. Medium cost is only one term in the capital cost. That is why C5 stops at "does not follow" and gives no cost verdict.

### Dead End: Declaring the cost claim false

**What was tried:** This is the rival to C5. Because the efficiency premise fails, the cost conclusion would be false too.

**Why abandoned:** A conclusion drawn from a false premise is unsupported, not false. A thermal store could still win on capital cost at long durations, and no verified cost figure here refutes that (C5, A-14).

**What it ruled out:** Overclaiming in the other direction. The analysis rejects the inference, not every possible cost case.

## 6. Conclusion

**Recommended approach:** Reject the claim as stated. If charging is resistive, an 85% round trip, measured electricity to electricity, is beyond what thermodynamics allows: the ideal ceiling is 78.05% even with Earth's coldest recorded sink (chain C1), and 56.89% with a 25 °C sink (chain C2). If charging is by heat pump, 85% is not ruled out by physics but is not supported by any figure read (chain C3). Because the cost conclusion is drawn from that premise, it does not follow (chain C5).

**Key insight:** The binding limit is set by the temperatures, not by the engineering. Reaching 85% from a 565 °C store with a heat engine would need a heat sink at −147.43 °C (chain C1), and the "same nameplate" comparison sets thermal MWh against electric MWh, overstating what the tank can deliver by 1.76× to 2.5× (chain C4).

**Trade-offs acknowledged:** This analysis rejects the claim's argument, not every case for molten-salt storage. A store with cheap salt might still compete on capital cost at long duration, and that question is left open because no cost figure was read at source (chain C5).

**Pre-check:** head C1 (HIGH), C2 (MEDIUM), C3 (MEDIUM), C4 (MEDIUM), C5 (MEDIUM) · ?-marked: none · lowest cited: MEDIUM · Inputs ceiling: MEDIUM
**Confidence:** MEDIUM — the verdict that the resistive-charging premise is impossible rests on C1 alone and is HIGH (chain C1). The overall rating is held at MEDIUM by C2 (unverified 25 °C sink), C3 (live rival: future machines beating 83.7% of Carnot each), C4 (C2 plus the unverified 40–42% Rankine figure) and C5 (inherits C3 and C4). The open items are a measured round trip from a heat-pump-charged plant, a site sink temperature, and a published Rankine efficiency; each would move its own chain (chain C3, chain C4).
## Appendix — process output

## Phase 2 inversion pass (process output)

**Claim:** A 5 MWh molten-salt store operating at 290–565 °C achieves more than 85% round trip, and that makes it cost-competitive with Li-ion. **Inverted:** it does not exceed 85%, and it is not cost-competitive for that reason.

Conditions that would guarantee the inverted claim:
1. The heat engine's Carnot limit at 565 °C is below 85%.
2. Charging is resistive, which gives a factor of exactly 1.
3. The heat is released over the swing, not at the peak.
4. Standby losses are greater than zero.
5. Each heat-pump machine falls short of 92.2% of its Carnot limit.
6. Cost depends on capital cost, which the claim does not give.

Necessary preconditions of the original claim:
- Carnot at 565 °C is at least 85%, which needs a sink at or below 125.72 K (load-bearing; refuted by GT-5, see C1).
- Charging can deliver more than 1 J of heat per joule of electricity (load-bearing; true only with a heat pump, see GT-3 and A-3).
- Each machine reaches at least 92.2% of its Carnot limit (load-bearing for the heat-pump reading; unverified, recorded as A-12).
- Standby losses are negligible (not load-bearing; A-11).
- Efficiency alone decides cost (load-bearing for the cost clause; discarded, see A-8 and A-14).

Preconditions that are both load-bearing and unverified: A-12. They were routed to the Phase 2 table as untested-belief rows.

## Assumption Audit scan (process output)

| Chain | Step | Step Text (brief) | Assumption surfaced? | Added to Table? |
|---|---|---|---|---|
| C1 | 1 | hottest heat at 838.15 K | no | n/a |
| C1 | 2 | 85% needs Tc ≤ 125.72 K | no | n/a |
| C1 | 3 | coldest sink gives at most 78.05% | no | n/a |
| C1 | 4 | resistive factor ≤ 1, so round trip ≤ discharge | no (A-2 already in the table) | n/a |
| C1 | 5 | no resistive store reaches 85% | no | n/a |
| C2 | 1 | Tm = 691.56 K | yes — constant cp | A-6 (already in the table; marked) |
| C2 | 2 | ideal discharge 56.89% | no (A-4 / GT-6? already present) | n/a |
| C2 | 3 | round-trip ceiling 56.89% | no | n/a |
| C3 | 1 | ideal heat-pump COP = Tm/(Tm − T0) | no | n/a |
| C3 | 2 | ideal engine returns (Tm − T0)/Tm | no | n/a |
| C3 | 3 | product = 1 for any temperatures | yes — no losses from temperature differences | A-13 added |
| C3 | 4 | f² model, f = 0.9220 | no (A-12 already present) | n/a |
| C3 | 5 | 70% maps to f = 0.8367 | no | n/a |
| C3 | 6 | gap of 8.53 points | no | n/a |
| C3 | 7 | premise unsupported | no | n/a |
| C4 | 1 | 2.844 MWh electric ideal | no | n/a |
| C4 | 2 | 2.00 MWh electric at 40% | no (A-5 / GT-8? present) | n/a |
| C4 | 3 | 8.79–12.5 MWh of heat needed | no | n/a |
| C4 | 4 | 1.758×–2.5× overstatement | no (A-7 present) | n/a |
| C5 | 1 | premise false or unsupported | no | n/a |
| C5 | 2 | cost has a capital term | yes — levelised cost has a capital term | A-14 added |
| C5 | 3 | cost conclusion does not follow | no (A-8 present) | n/a |
| C5 | [2nd] actor | buyer under-sizes by 1.494×–2.125× | no | n/a |
| C5 | [2nd] time | shortfall recurs every cycle | no | n/a |
| C5 | [3rd] actor | vendor credibility loss | no | n/a |
| C5 | [3rd] time | metric lock-in on round-trip efficiency | no | n/a |

Techniques not applied:
- trade-off — not applicable — the question is whether a claim is true, not a choice between viable options; no two options survived to be weighted
- fishbone — not applicable — the assumption space was set by the claim's two clauses and the inversion pass; no multi-causal symptom needed a breadth-first brainstorm

## Adversarial pass (process output)

**Recompute:** Every figure was recomputed independently in Python, outside the chain text:
- 565 + 273.15 = 838.15 K ✓; 290 + 273.15 = 563.15 K ✓
- 0.15 × 838.15 = 125.7225 K → −147.43 °C ✓
- 1 − 184.0/838.15 = 0.78047 → 78.05% ✓ (with 183.95 K: 0.78053, which also rounds to 78.05%)
- ln(838.15/563.15) = ln(1.48833) = 0.39765 ✓; 275/0.39765 = 691.56 K (418.41 °C) ✓
- 298.15/691.56 = 0.43113, so 1 − 0.43113 = 56.89% ✓
- 85 − 56.89 = 28.11 points ✓; 0.85/0.5689 = 1.494 ✓
- COP = 691.56/393.41 = 1.7579 ✓; 1.7579 × 0.5689 = 1.0000 ✓
- √0.85 = 0.92195 ✓; √0.70 = 0.83666 ✓; 0.9220 − 0.8367 = 0.0853 ✓
- 5 × 0.5689 = 2.844 MWh ✓; 5 × 0.40 = 2.00 ✓; 5 × 0.42 = 2.10 ✓
- 5/0.5689 = 8.789 MWh ✓; 5/0.40 = 12.5 ✓; 1/0.5689 = 1.758 ✓; 1/0.40 = 2.5 ✓
- 0.85/0.40 = 2.125 ✓
- 1 − 298.15/838.15 = 64.43% ✓; 64.43 − 56.89 = 7.54 ✓
- 56.89 − 40 = 16.89 ✓
- 1.5 × 275 = 412.5 kJ/kg ✓; 412.5/3600 = 0.11458 kWh/kg ✓; 5000/0.11458 = 43,636 kg ✓

Every scaled figure lands on the correct side of its base: the thermal requirements 8.79 and 12.5 MWh are above 5, and the deliverables 2.844 and 2.00 MWh are below 5. No figure failed to recompute.

**Sensitivity:** The headline (resistive) verdict would flip only if GT-1 were false, or if GT-5 understated how cold a usable sink can be by about 58 K (a sink at or below 125.72 K would be needed). Neither is `?`-marked. The weakest links in each chain:
- C1: the GT-5 sink bound. It is generous to the claim and stays robust.
- C2: GT-6? (sink choice).
- C3: GT-7 being an aim rather than a bound.
- C4: GT-8? (Rankine efficiency).
- C5: its inherited MEDIUM inputs.

**Rival:**
- Headline: the molten salt is an electrochemical battery at 87%. → §5, "Reading 'molten salt' as an electrochemical molten-salt battery".
- C2: the peak-temperature Carnot figure of 64.43% as the ceiling. → §5, "Using the Carnot efficiency at the 565 °C peak as the ceiling".
- C3: future machines exceed 83.7% of Carnot each. This rival is still live and is named on the C3 `**Confidence:**` line.
- C4: "5 MWh" means electric output. Handled on the C4 `**Confidence:**` line, where the endpoint holds in reverse.
- C5: the cost claim is outright false. → §5, "Declaring the cost claim false".
- C1: the heat-pump reading is a rival, and C3 covers it.

**Premise:** The headline conclusion is already false: a resistive-charged 290–565 °C molten-salt store has been measured above 85% round trip.

**Causes:** Possible causes, generated from three viewpoints.
- Physicist:
  - the Carnot bound was misapplied
  - the sink was colder than 125.72 K
  - the energy accounting counted reject heat used for district heating as useful output
  - the store was charged partly by a heat pump without saying so
- Owner or buyer:
  - "efficiency" was quoted as heat-in / heat-out of the tank only (about 99% retention per the GT-4 page), not electricity to electricity
  - a combined-heat-and-power credit was counted
- Vendor or claimant:
  - the figure was storage efficiency, not system efficiency
  - nameplate was quoted in thermal MWh
  - an electrochemical molten-salt battery was meant

**Clusters:**
- K1, a definitional switch: thermal retention, or heat counted as useful output, was presented as electricity-to-electricity efficiency. Bears on C1, C2 and GT-4.
- K2, a hidden heat pump. Bears on C3, GT-3 and A-3.
- K3, a technology swap. Bears on GT-9 and §5.
- K4, a misapplied law or an exotic sink. Bears on GT-1, GT-5 and C1.

**Disposition:**
- K1 — plan change: §6 and the Answer state that the 85% claim is rejected only as an electricity-to-electricity round trip; a tank-retention figure of about 99% is a different quantity. The basis is named in §1 success criteria and in C4.
- K2 — accepted risk, mitigated: C3 analyses the heat-pump reading separately and leaves its rival live.
- K3 — accepted risk, mitigated: ruled out in §5 by the claim's own wording.
- K4 — accepted risk, mitigated: GT-1 and GT-5 were both read at source, and C1 uses the most claim-favourable sink.

**Falsification:** The resistive verdict is false if a resistive-charged store holding heat at no more than 565 °C delivers more electricity than 78.05% of its electrical input, measured electricity to electricity with no heat credit. The heat-pump verdict is false if an operating heat-pump-charged 290–565 °C store is measured at 85% or above.

## §6→§4 closure ledger (process output)

```text
- "Reject the claim as stated … resistive … beyond what thermodynamics allows … 78.05% … 56.89% … heat pump … not supported … cost conclusion … does not follow" → chain C1, C2, C3, C5 ✓
- "The binding limit is set by the temperatures … sink at −147.43 °C … overstating … 1.76× to 2.5×" → chain C1, C4 ✓
- "This analysis rejects the claim's argument, not every case for molten-salt storage … left open" → chain C5 ✓
- "Pre-check: head C1 (HIGH), C2 (MEDIUM), C3 (MEDIUM), C4 (MEDIUM), C5 (MEDIUM) … Inputs ceiling: MEDIUM" → chain C1, C2, C3, C4, C5 ✓
- "Confidence: MEDIUM — the verdict that the resistive-charging premise is impossible rests on C1 alone and is HIGH …" → chain C1, C3, C4 ✓
```

## Self-audit scan (process output)

| Chain | Chain Head (brief) | Form conforming? | Rule applied | Dependency clean? | Band | Act attempted? | Edges fired |
|---|---|---|---|---|---|---|---|
| C1 | GT-1 + GT-2 + GT-3 + GT-4 + GT-5 | unreached | n/a — hops 3–5 are beyond the check's reach; manual inspection found no hop starting with a GT-id and no closing period | yes | HIGH | yes | none |
| C2 | GT-1 + GT-2 + GT-3 + GT-4 + GT-6? | unreached | n/a — hop 3 is beyond the check's reach; manual inspection found no violation | yes | MEDIUM | yes | none |
| C3 | GT-1 + GT-3 + GT-7 | unreached | n/a — hops 3–7 are beyond the check's reach; manual inspection found no violation | yes | MEDIUM | yes | none |
| C4 | C2 + GT-8? | unreached | n/a — hops 3–4 are beyond the check's reach; manual inspection found no violation | yes | MEDIUM | no | none |
| C5 | C1 + C3 + C4 | unreached | n/a — hops 3 to [3rd] are beyond the check's reach; manual inspection found no violation | yes | MEDIUM | yes | none |

C4's `Act attempted? = no`: GT-8? was not read (`not read — turn budget`), and its other input, C2, is a chain, not a citation. This chain is not load-bearing for the headline resistive verdict, which rests on C1.

| §6 Span (brief) | Construct | Claim under R11? | R11 clause applied | Chain cited |
|---|---|---|---|---|
| Recommended approach: reject the claim as stated… | bold lead-in | yes | a bold lead-in whose colon closes the bold span | C1, C2, C3, C5 |
| Key insight: the binding limit is set by the temperatures… | bold lead-in | yes | a bold lead-in whose colon closes the bold span | C1, C4 |
| Trade-offs acknowledged: rejects the argument, not every case… | bold lead-in | yes | a bold lead-in whose colon closes the bold span | C5 |
| Pre-check: head C1 … Inputs ceiling: MEDIUM | bold lead-in | yes | a bold lead-in whose colon closes the bold span | C1, C2, C3, C4, C5 (via head) |
| Confidence: MEDIUM — … | bold lead-in | yes | a bold lead-in whose colon closes the bold span | C1, C3, C4 |

```text
Scan complete: 5 chain rows, one per section-4 chain block in order; 5 section-6 rows, one per construct in order — 5 claims under R11, 0 excluded. 0 chains malformed, 0 claims untraced.
```

## Self-Audit Gate (process output)

Pre-scoring check: the Assumption Audit scan has one row per step for C1 (5), C2 (3), C3 (7), C4 (4) and C5 (7, including the second- and third-order steps), which matches §4. The self-audit scan has 5 chain rows and 5 section-6 rows, and its reconciliation line recounts correctly.

**Criterion 1: Identify Essence**
Quoted span: "Do the laws of thermodynamics allow a molten-salt store that swings between 290 °C and 565 °C to turn electricity into heat and back at better than 85% round-trip efficiency? And if not, does anything in the claim still support its conclusion that the store is cost-competitive with a lithium-ion system of the same nameplate capacity?"
Band: **Sound**
Justification: The statement names the real question, specific to this problem, and every success criterion can be checked against §6. But the Essence is two sentences rather than the single sentence the Rigorous descriptor requires.

**Criterion 2: Challenge Assumptions**
Quoted span: "| C3 | 3 | product = 1 for any temperatures | yes — no losses from temperature differences | A-13 added |"
Band: **Rigorous**
Justification: Every row uses one of the four types with the treatment prescribed for it and an Accept, Challenge or Discard token followed by an em-dash. Several rows are challenged and one is discarded. Every unverified assumption used in a chain (A-4, A-5, A-6, A-12, A-13) reads "unverified — flagged". The audit scan covers every chain step and records the two assumptions it surfaced.

**Criterion 3: Establish Ground Truths**
Quoted span: "enumerated GT-6?, GT-8?, GT-10?; the list carries `?` on exactly those three. GT-7 (unsuffixed, read at source) feeds only C3, which is MEDIUM"
Band: **Sound**
Justification: The enumeration matches the list, and every unsuffixed ground truth feeding the HIGH chain C1 names where it was read. One unsuffixed, reachable ground truth (GT-7) feeds only a MEDIUM chain, which the descriptor bands Sound. GT-9 is consumed only by §5 and the C1 rival note; that overlap is noted under Criterion 4.

**Criterion 4: Reason Upward**
Quoted span: "| C1 | GT-1 + GT-2 + GT-3 + GT-4 + GT-5 | unreached | n/a — hops 3–5 are beyond the check's reach; manual inspection found no hop starting with a GT-id and no closing period |"
Band: **Sound**
Justification: Every chain names its inputs, has real intermediate steps, and its arithmetic recomputes (see the adversarial Recompute). §5 has four dead ends, each in What-was-tried / Why-abandoned / What-it-ruled-out form. But all five chain-form rows read `unreached`, so form conformance rests on manual inspection rather than the check, and GT-9 feeds no §4 chain.

**Criterion 5: Validate**
Quoted span: "**Confidence:** MEDIUM — the short axis is Rivals. GT-7 states an aim, not a physical bound, so the rival "a future pair of machines will exceed 83.7% of Carnot each" is still live."
Band: **Rigorous**
Justification: Every chain's band is the one its axes allow: C1 is HIGH with every input read; C2 and C4 are MEDIUM, naming their `?` inputs; C3 is MEDIUM on a named live rival; C5 is MEDIUM, capped by C3 and C4. The §6 MEDIUM equals the weakest contributing chain. The adversarial record carries every part, and each of its four clusters has a disposition.

**Criterion 6: Conclusion-to-Ground-Truth Traceability**
Quoted span: "| Key insight: the binding limit is set by the temperatures… | bold lead-in | yes | a bold lead-in whose colon closes the bold span | C1, C4 |"
Band: **Rigorous**
Justification: All five §6 claims cite §4 chains, and §6 introduces no new reasoning. The Key Insight (a −147.43 °C sink would be required, and the thermal-versus-electric nameplate mismatch) is a non-obvious finding, not a restatement of the recommendation.

**Gate result:** cleared · passes: 1 · Fix/Repeat fired: no

## Structured summary (process output)

```json
{
  "schema_version": 1,
  "run_mode": "full-composer",
  "assumptions": [
    {"id": "A-1", "type": "physical law", "verdict": "Accept"},
    {"id": "A-2", "type": "physical law", "verdict": "Accept"},
    {"id": "A-3", "type": "untested belief", "verdict": "Challenge"},
    {"id": "A-4", "type": "convention", "verdict": "Challenge"},
    {"id": "A-5", "type": "untested belief", "verdict": "Challenge"},
    {"id": "A-6", "type": "untested belief", "verdict": "Accept"},
    {"id": "A-7", "type": "convention", "verdict": "Challenge"},
    {"id": "A-8", "type": "untested belief", "verdict": "Discard"},
    {"id": "A-9", "type": "untested belief", "verdict": "Challenge"},
    {"id": "A-10", "type": "untested belief", "verdict": "Challenge"},
    {"id": "A-11", "type": "untested belief", "verdict": "Accept"},
    {"id": "A-12", "type": "untested belief", "verdict": "Challenge"},
    {"id": "A-13", "type": "untested belief", "verdict": "Accept"},
    {"id": "A-14", "type": "physical law", "verdict": "Accept"}
  ],
  "ground_truths": [
    {"id": "GT-1", "read_at_source": true},
    {"id": "GT-2", "read_at_source": true},
    {"id": "GT-3", "read_at_source": true},
    {"id": "GT-4", "read_at_source": true},
    {"id": "GT-5", "read_at_source": true},
    {"id": "GT-6", "read_at_source": false},
    {"id": "GT-7", "read_at_source": true},
    {"id": "GT-8", "read_at_source": false},
    {"id": "GT-9", "read_at_source": true},
    {"id": "GT-10", "read_at_source": false}
  ],
  "chains": [
    {"id": "C1", "confidence": "HIGH", "rests_on": ["GT-1", "GT-2", "GT-3", "GT-4", "GT-5"]},
    {"id": "C2", "confidence": "MEDIUM", "rests_on": ["GT-1", "GT-2", "GT-3", "GT-4", "GT-6?"]},
    {"id": "C3", "confidence": "MEDIUM", "rests_on": ["GT-1", "GT-3", "GT-7"]},
    {"id": "C4", "confidence": "MEDIUM", "rests_on": ["C2", "GT-8?"]},
    {"id": "C5", "confidence": "MEDIUM", "rests_on": ["C1", "C3", "C4"]}
  ],
  "dead_ends": [
    "Reading \"molten salt\" as an electrochemical molten-salt battery",
    "Using the Carnot efficiency at the 565 °C peak as the ceiling",
    "Settling cost-competitiveness with a Fermi estimate of the salt inventory",
    "Declaring the cost claim false"
  ],
  "techniques": {
    "applied": ["theoretical-limit", "inversion", "five-whys", "second-order", "estimate"],
    "not_applied": [
      {"technique": "trade-off", "phase": 4, "reason": "the question is whether a claim is true, not a choice between viable options; no two options survived to be weighted"},
      {"technique": "fishbone", "phase": 2, "reason": "the assumption space was set by the claim's two clauses and the inversion pass; no multi-causal symptom needed a breadth-first brainstorm"}
    ]
  },
  "gate": {
    "passes": [
      {"bands": ["Sound", "Rigorous", "Sound", "Sound", "Rigorous", "Rigorous"], "gate_cleared": true, "hand_wavy_cap_cleared": true}
    ],
    "fix_repeat_fired": false,
    "cleared": true
  },
  "re_entry": {"fired": false, "edges": []},
  "conclusion": {
    "recommendation": "Reject the claim as stated. If charging is resistive, an 85% round trip, measured electricity to electricity, is beyond what thermodynamics allows: the ideal ceiling is 78.05% even with Earth's coldest recorded sink (chain C1), and 56.89% with a 25 °C sink (chain C2). If charging is by heat pump, 85% is not ruled out by physics but is not supported by any figure read (chain C3). Because the cost conclusion is drawn from that premise, it does not follow (chain C5).",
    "confidence": "MEDIUM"
  }
}
```
