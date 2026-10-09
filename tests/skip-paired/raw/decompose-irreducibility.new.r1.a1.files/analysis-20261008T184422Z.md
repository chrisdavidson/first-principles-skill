## Answer

**Recommendation:** Reject both parts of the claim as stated. Full electricity-to-electricity round-trip efficiency for a Joule-heated molten-salt system discharging through a conventional heat engine is capped at roughly 60-63% by the Carnot limit and realistically runs 33-43% in credible real-world designs, not 85%+ (chain C1, chain C2). A 5 MWh instance of this architecture is very likely not cost-competitive with a same-capacity lithium-ion system once small-scale power-block cost penalties and the efficiency-driven throughput penalty are included (chain C4), with competitiveness plausible only at much larger scale/longer duration or via a hybrid design (chain C5).

**Band (from §6):** MEDIUM — the efficiency-impossibility finding alone is HIGH (chain C1, chain C3), but the Conclusion bundles it with the MEDIUM-rated realistic-efficiency estimate and cost verdict (chain C2, chain C4, chain C5), so the combined band is MEDIUM.

**Would change it:** A documented CSP plant's gross-cycle-efficiency specification would replace chain C2's engineering heuristic with a sourced figure; a stated power rating/duration for the 5 MWh system would let chain C4 and chain C5 be recomputed exactly instead of bracketed (chain C4, chain C5).
## 1. Problem Essence

**Core problem:** Does a Joule-heated molten-salt thermal storage system operating between roughly 290°C and 565°C deliver a true electricity-to-electricity round-trip efficiency above 85%, and is a 5 MWh instance of such a system cost-competitive with a 5 MWh lithium-ion battery system, once the power rating/duration implied by that energy capacity is accounted for?

**Success criteria:**
- The analysis states, for every efficiency figure it cites, whether that figure measures charging (electricity→heat), discharging (heat→electricity), or the full round trip (electricity→heat→electricity) — and the Conclusion section's efficiency verdict does not rest on a figure whose stage is unstated.
- The analysis derives the physical (Carnot/second-law) ceiling on heat-to-electricity reconversion at ~565°C hot-side / ambient heat-rejection temperature, and the Conclusion states explicitly whether 85%+ sits above or below that ceiling.
- The analysis cites at least one real, operating or publicly documented ETES/CSP-with-storage project's measured or design round-trip figure, distinct from vendor marketing copy, and the Conclusion states how the claimed 85%+ compares to it.
- The analysis states what power rating (MW) and duration (hours) it assumes for the 5 MWh system, and the cost-competitiveness verdict is conditioned on that stated duration rather than on energy capacity alone.
- The Conclusion reaches a stated, falsifiable verdict on each of the two sub-claims (efficiency ≥85%; cost-competitive with Li-ion at 5 MWh) rather than a single undifferentiated verdict on "the claim."

**Theoretical-limit reframe (carried forward from Step 0):** the question as posed implicitly borrows "round-trip efficiency" as a single, convention-bound number from battery-storage vocabulary. Stripping that convention and asking what the underlying physics actually permits — before looking at any vendor figure — is the move that exposes the claim's central flaw, so it is applied here rather than deferred to Phase 4.

---

## 2. Assumptions Table

| Assumption | Type | Treatment | Verdict | Verification |
|------------|------|-----------|---------|--------------|
| A1: "Round-trip efficiency" in the claim means full electricity-to-electricity conversion, not just the charging/storage stage | convention | explicitly challenge before use | Challenge — the claim's own wording ("round-trip electricity into heat and back") commits to the full-electricity reading, not the looser storage-only sense some vendors use | textual reading of the claim as given |
| A2: Resistive (Joule) heating of salt converts electricity to heat with efficiency near 100% | physical law | accept as ground-truth candidate | Accept — consistent with the first law of thermodynamics | GT-1, GT-4 |
| A3: The claim's own 290°C and 565°C tank temperatures are the correct reservoir temperatures for a Carnot-limit calculation on the power-block (discharge) side | convention / misconception | explicitly challenge | Discard — 290°C is the storage loop's cold-tank return temperature, not the power cycle's heat-rejection (condenser) temperature; the correct cold reservoir is ambient/condenser temperature | GT-3; standard two-tank molten-salt CSP architecture |
| A4: 85%+ electricity-to-electricity round-trip efficiency is physically achievable for a Joule-heating-plus-heat-engine architecture at a ~565°C hot side with realistic ambient heat rejection | untested belief, testable against physical law | verify against Carnot bound | Discard — contradicted by GT-2/GT-3; the ideal (Carnot) ceiling itself is only ~60-63% | GT-2, GT-3 |
| A5: "Molten salt" as the storage medium implies a particular (CSP-grade) round-trip performance | convention / misconception | explicitly challenge | Discard — storage medium does not determine power-cycle efficiency; architecture does | GT-4, GT-5, GT-7? |
| A6: Existing commercial/demonstration ETES and CSP-with-storage systems validate round-trip efficiencies at or near 85% | untested belief | verify | Discard — best documented figures are ~44.6% (Hamburg) and "up to 60%" (Malta); no independently-opened source supports 85% for a full electricity round trip | GT-4, GT-5; GT-6? unverified — flagged |
| A7: Turbine/power-block and balance-of-plant specific capital costs ($/kW) scale down linearly from utility CSP scale to 5 MWh / sub-2 MW scale | convention / untested belief | explicitly challenge | Discard — contradicted by GT-8; $/kW rises sharply below ~1 MW | GT-8 |
| A8: A 5 MWh "nameplate capacity" figure alone is sufficient to compare system costs across technologies, without specifying power rating/duration | convention / methodological flaw | explicitly challenge | Challenge — incomplete as stated; duration materially changes both technologies' $/kWh, and the thermal system is far more duration-sensitive | GT-10; unverified — flagged (no duration is given in the claim) |
| A9: Lithium-ion cost benchmarks drawn from utility-scale (≥100 MWh, ≥4 hr) deployments are directly representative of a 5 MWh lithium-ion system's cost | convention | explicitly challenge | Challenge — $/kWh rises at small scale for batteries too, but materially less steeply than the turbine/BOP scale penalty on the thermal side, so the comparison direction is preserved even though the absolute Li-ion number is understated | GT-9, GT-10; unverified — flagged (no small-scale Li-ion $/kWh source opened this session) |
| A10: The round-trip efficiency shortfall has a direct, first-order effect on levelized cost of storage, since all throughput electricity must be purchased per unit delivered | current constraint (holds under standard LCOS accounting; could be waived only if input electricity were free) | record expiry conditions | Accept — expires only if input electricity cost is zero or negative (e.g., pure curtailed power), a non-default special case | GT-10; standard LCOS definition |
| A11: Ambient heat-rejection (condenser) temperature for the power block is in the typical range ~30-45°C | current constraint (depends on site climate/cooling technology, not fixed physical law) | record expiry conditions | Accept — reasonable default; expires for an unusually hot ambient site or dry-cooling in a desert climate, which would raise T_cold and lower the Carnot ceiling by a few more percentage points without changing the verdict | standard power-plant thermal design practice; GT-3 |
| A12 *(surfaced during Phase 4 Assumption Audit, chain C2)*: real steam/ORC/sCO2 power blocks achieve roughly 55-70% of their Carnot ideal efficiency (second-law/exergetic effectiveness) | untested belief | verify or flag unverified | Challenge — plausible, standard engineering heuristic, but not independently read-at-source in this session | unverified — flagged; indirectly corroborated by GT-4 and GT-5 falling inside the resulting bracket |
| A13 *(surfaced during Phase 4 Assumption Audit, chain C5 second-order extension)*: sophisticated financiers, offtakers, and regulators will, over a few duty cycles or financing rounds, independently check or discover a project's true round-trip efficiency rather than relying on an unverified vendor figure indefinitely | untested belief (market/institutional behavior, not physics) | verify or flag unverified | Challenge — plausible for well-advised capital providers, not guaranteed for all market participants; used only to support the second-order extension, not any headline physics or cost finding | unverified — flagged |

---

## 3. Ground Truths

- **GT-1** Resistive (Joule) heating converts electrical energy into heat with efficiency at or near 100%, limited only by minor parasitic losses (wiring resistance, radiative/convective losses from heating elements, insulation/standby losses) — a direct consequence of the first law of thermodynamics: electrical energy dissipated through a pure resistive element has no competing non-heat output. — source: first law of thermodynamics (physical law); read-at-source: not applicable (physical law, no external citation to open). Provenance: physical law.

- **GT-2** The maximum theoretical efficiency of any heat engine converting heat into work (e.g., electricity) between a hot reservoir at absolute temperature T_hot and a cold (heat-rejection) reservoir at absolute temperature T_cold is the Carnot efficiency, η = 1 − T_cold/T_hot — a direct consequence of the second law of thermodynamics. — source: second law of thermodynamics (physical law); read-at-source: not applicable (physical law). Provenance: physical law.

- **GT-3** Applying GT-2 with T_hot = 565°C (838.15 K, the claim's stated hot-tank/turbine-design temperature) and T_cold = 40°C (313.15 K, a representative ambient-cooled condenser temperature) yields a Carnot (ideal) ceiling of η = 1 − 313.15/838.15 ≈ 62.6%. Using the claim's own 290°C cold-*tank* figure (563.15 K) instead — physically the wrong reservoir for this calculation, see A3 — would yield an even lower ≈32.8%, so neither reading rescues an 85%+ figure. — source: direct computation from GT-2 and the stated design temperature; read-at-source: not applicable (arithmetic derivation; computation shown inline, no external source to open). Provenance: derived / physical-law application.

- **GT-4** Siemens Gamesa / Hamburg Energie's "Electric Thermal Energy Storage" (ETES) demonstration system (Hamburg) has a stated energy efficiency of 99% for "storing direct heat or heat converted from electricity" (charging stage) and a stated energy efficiency of 45% for "producing electricity from the stored thermal energy" (discharging stage) — implying a full electricity-to-electricity round-trip efficiency of 0.99 × 0.45 ≈ 44.6%. — source: nsenergybusiness.com, "Electric Thermal Energy Storage (ETES) System, Hamburg"; read-at-source: fetched and quoted directly — "The energy efficiency for storing direct heat or heat converted from electricity is expected to be 99%" and "the energy efficiency for producing electricity from the stored thermal energy is expected to be 45%." Provenance: read-at-source.

- **GT-5** Malta Inc.'s pumped heat energy storage (PHES) system — which stores heat in molten salt and cold in an antifreeze-like fluid using a heat-pump/heat-engine architecture, not pure resistive heating alone — is reported by Southwest Research Institute (SwRI) to offer "high potential system performance up to 60% round-trip efficiency," described as electricity-to-electricity. — source: pv-magazine.com, "Pumped heat energy storage seeks to demonstrate commercial readiness"; read-at-source: fetched and quoted directly — "high potential system performance up to 60% round-trip efficiency." Provenance: read-at-source. Note: a more sophisticated, heat-pump-assisted architecture than the pure Joule-heating system the claim describes; cited as the best-in-class reference point, not as evidence the claim's own architecture reaches it (see Abandoned Reasoning, Dead End 3).

- **GT-6?** SEHRENE's electro-thermal energy storage (ETES) concept is described, in secondary aggregator coverage, as targeting "very high energy efficiency (80-85%)." — cited to: a SEHRENE announcement, reported via search-aggregator summaries; reported-by-delegate: search results only, the primary SEHRENE source was not opened in this session and the exact metric definition (full electricity round trip vs. heat-delivery efficiency) is not stated in the secondary summary. Provenance: reported-by-delegate / unverified. This is the only source found anywhere in this analysis's research naming a figure near the claim's 85%; per chains C1/C3 it would itself violate the Carnot ceiling (GT-3) if it meant a full electricity round trip, making it far more likely to describe a heat-delivery or charge-only metric (as GT-4's 99% and GT-7?'s 97% do).

- **GT-7?** Rondo Energy's "Heat Battery" (resistively-heated firebrick, not molten salt) is reported to have "over 97 percent" efficiency for "the complete load and discharge cycle" — but Rondo's discharge output is heat/hot air/steam delivered to an industrial process, not electricity regenerated through a power block. — cited to: secondary business-profile coverage; reported-by-delegate: search results only, primary Rondo technical documentation not opened in this session. Provenance: reported-by-delegate / unverified. Cited only to illustrate the recurring pattern: every near-100% "round trip" figure found in this space describes a heat-in/heat-out cycle, not an electricity-in/electricity-out cycle.

- **GT-8** The specific capital cost ($/kW) of steam-turbine heat engines (and CSP power blocks generally) drops rapidly with increasing size up to approximately 1 MW, with much smaller further economies of scale above that size (e.g., only a ~€100/kW reduction scaling a steam turbine from 2 MW to 3 MW); at full utility CSP scale the turbine/power-block is typically less than 20% of total project cost. — source: archive.ilsr.org, "Distributed Concentrating Solar Thermal Power — Yes!"; read-at-source: fetched and quoted directly — "the cost of heat engines per kilowatt (kW) of capacity drops rapidly as size increases up to 1 megawatt (MW). But beyond that, the economies of scale are much smaller," with the 2 MW→3 MW / ~€100/kW example and the "<20% of project costs" figure. Provenance: read-at-source.

- **GT-9** As of October 2025, a full lithium-ion battery energy storage system (cells + BOS + installation + grid connection) for a long-duration (≥4 hour) utility-scale project costs approximately $125/kWh, yielding a levelized cost of storage (LCOS) of approximately $65/MWh, in global markets outside China and the US. — source: ember-energy.org, "Batteries now cheap enough to deliver solar when it is needed"; read-at-source: fetched and quoted directly — "$125/kWh for the full battery storage system connected to the grid" and "$65/MWh" LCOS, stated as applying to "long-duration (four hours or more) utility-scale battery projects." Provenance: read-at-source. Note: describes utility scale (typically 100+ MWh), not the 5 MWh scale this analysis evaluates (see A9).

- **GT-10** By definition, energy capacity (MWh) = power rating (MW) × discharge duration (hours). For lithium-ion systems, power and energy capacity scale nearly independently at comparatively modest, roughly duration-flat cost per kWh. For a Joule-heated-salt-plus-heat-engine system, the storage medium (tank + salt) is cheap per kWh of energy capacity, but the power block (turbine/generator and its balance of plant) is a large, duration-insensitive fixed cost sized to the power rating alone — making thermal-storage economics strongly favor long discharge durations and disfavor short ones, while battery economics are comparatively duration-insensitive. — source: basic systems-engineering identity (E = P × t) combined with the cost-structure consensus underlying GT-8's source and general CSP economics literature; read-at-source: not applicable (definitional identity). Provenance: physical law / definition.

**Provenance summary:** `?`-marked: GT-6, GT-7 (2 of 10). Read-at-source locations for unsuffixed ground truths feeding load-bearing chains: GT-1 (physical law, first law of thermodynamics, no external source), GT-2 (physical law, second law of thermodynamics, no external source), GT-3 (arithmetic computation shown inline from GT-2), GT-4 (nsenergybusiness.com article body, two quoted sentences on charging/discharging efficiency), GT-5 (pv-magazine.com article body, quoted "up to 60%" sentence), GT-8 (archive.ilsr.org article body, quoted scale-economics sentences and example figures), GT-9 (ember-energy.org article body, quoted $125/kWh and $65/MWh figures), GT-10 (definitional identity, E = P × t).

---

## 4. Derivation Chains

### Conclusion C1: An 85%+ full electricity-to-electricity round-trip efficiency is not physically achievable by a Joule-heated-salt-plus-heat-engine architecture at these temperatures

GT-1 (Joule heating ~100% electricity-to-heat) + GT-2 (Carnot efficiency law) + GT-3 (computed ~62.6% ideal ceiling at 565°C hot / 40°C ambient)
→ even granting a perfect, lossless charging stage, the discharge stage still must pass stored heat through a heat engine whose maximum possible work output is capped by the Carnot efficiency between the hot salt and the ambient heat-rejection temperature
→ that ideal ceiling is only about 62.6 percent, meaning no physically possible heat engine operating between these two temperatures can turn more than about 62.6 percent of the delivered heat back into electricity
→ multiplying a best-case 100 percent charging efficiency by a best-case 62.6 percent discharge ceiling bounds the full electricity-to-electricity round trip at about 62.6 percent, strictly below the claimed 85 percent
→ an 85-percent-or-higher full round-trip efficiency is not physically achievable for this architecture at these temperatures, independent of any engineering-quality assumption

**Pre-check:** head GT-1, GT-2, GT-3 · ?-marked: none · lowest cited: none · Inputs ceiling: HIGH
**Confidence:** HIGH — rests entirely on physical law (GT-1, GT-2) and a direct computation (GT-3), no `?` inputs and no cited chains on the head line. Rival: the only candidate rival found in this analysis's research, SEHRENE's unverified 80-85% claim (GT-6?), is ruled out in Abandoned Reasoning Dead End 2, because read as a full-electricity-round-trip figure it would itself violate this chain's own Carnot ceiling.

### Conclusion C2: Real, credible full electricity-to-electricity round-trip efficiency for this class of system is roughly 33-44%, not 85%+

C1 (≈62.6% ideal ceiling) + GT-4 (Hamburg ≈44.6% implied round trip) + GT-5 (Malta "up to 60%")
→ real heat engines never reach their Carnot ceiling because of irreversibilities such as turbine/generator losses, heat-exchanger approach-temperature differences, and part-load operation, so practical second-law effectiveness for steam/ORC/sCO2 power blocks typically runs 55 to 70 percent of the Carnot ideal, which applied to C1's ceiling brackets realistic discharge-stage efficiency at roughly 34 to 44 percent of the heat delivered *[Assumes: A12 — real power-block second-law effectiveness is 55-70% of Carnot; a standard engineering heuristic, not read at a cited source this session]*
→ combining that realistic discharge-stage range with a near-lossless charging stage brackets the full electricity-to-electricity round-trip efficiency for a Joule-heated-plus-conventional-heat-engine architecture at roughly 33 to 43 percent
→ this estimated range matches the two best-documented real systems closely, Hamburg's implied 44.6 percent sitting just above the top of the bracket and Malta's "up to 60 percent" exceeding it only because Malta uses a more sophisticated heat-pump-assisted cycle rather than pure resistive heating
→ the claimed 85-percent-plus figure is therefore roughly 1.9 to 2.6 times higher than every credible real-world or physics-derived figure found for this class of system

**Pre-check:** head C1 (HIGH), GT-4, GT-5 · ?-marked: none · lowest cited: HIGH · Inputs ceiling: HIGH
**Confidence:** MEDIUM — the first hop rests on the `[Assumes: A12]` second-law-effectiveness heuristic (55-70% of Carnot), which was not read at a cited source this session; verification that would remove this as a cause of downgrade: reading a documented CSP plant's gross-cycle-efficiency specification (e.g., Gemasolar or Crescent Dunes design basis) to replace the heuristic with a sourced figure. No `GT-N?` input is consumed directly by this chain.

### Conclusion C3: The claimed 85%+ figure exceeds not just current practice but the physical ceiling itself, with almost no headroom remaining between the best demonstrated system and that ceiling

GT-3 (ideal ceiling ≈62.6%) + GT-5 (best demonstrated, Malta "up to 60%") + GT-4 (conventional practice, Hamburg ≈44.6%)
→ ordering these three figures shows the gap from conventional practice to the best demonstrated architecture is about 15 percentage points (44.6 to 60), proven reachable by switching to a heat-pump-assisted cycle rather than pure resistive heating
→ the further gap from the best demonstrated architecture to the absolute ideal ceiling is only about 2 to 3 percentage points (60 to 62.6), meaning almost no headroom remains to reach through better engineering of the same temperature bounds
→ reaching materially above roughly 62 percent would require raising the hot-side temperature well above 565°C or lowering the heat-rejection temperature well below ambient, not incremental engineering of a Joule-heating-plus-turbine design, so the 85-percent-plus claim is not merely unachieved, it is unachievable at these stated temperatures by any architecture

**Pre-check:** head GT-3, GT-5, GT-4 · ?-marked: none · lowest cited: none · Inputs ceiling: HIGH
**Confidence:** HIGH — rests on physical law/computation (GT-3) and two read-at-source figures (GT-4, GT-5), no `?` inputs; hops recompute directly (60 − 44.6 ≈ 15; 62.6 − 60 ≈ 2-3). Rival: same as chain C1, ruled out in Abandoned Reasoning Dead End 2.

### Conclusion C4: A 5 MWh Joule-heated-molten-salt-plus-turbine system is very likely not cost-competitive with a 5 MWh lithium-ion system under the claim's bare nameplate-capacity framing

GT-8 (turbine/BOP $/kW scale penalty below 1MW) + GT-10 (duration-dependent cost-structure identity) + C2 (realistic round trip ≈33-43%)
→ a 5 MWh thermal storage tank implies a power rating in roughly the 0.5 to 2 MW range for typical 2.5-to-10-hour discharge durations, which sits squarely inside the steep, high-$/kW portion of the turbine/power-block cost curve GT-8 documents, so the power block's specific capital cost per kW is far higher here than at the multi-10-MW scale where CSP turbine economics are normally quoted
→ because the power block is the dominant, duration-insensitive fixed cost for a thermal system while the salt/tank energy-capacity cost is comparatively small, GT-10's cost-structure asymmetry means this small-scale power-block cost penalty falls almost entirely on the thermal system's $/kWh figure, unlike a comparably-sized lithium-ion system whose power and energy costs both scale far more gently with size
→ C2's realistic round-trip efficiency of roughly 33 to 43 percent also means roughly 2.0 to 2.7 times more input electricity must be purchased per unit of electricity ultimately delivered than for a lithium-ion system near 90%+ round-trip efficiency, which raises the thermal system's effective levelized cost of storage on top of its higher capital cost per kW
→ combining a small-scale power-block capital-cost penalty with a large efficiency-driven energy-throughput penalty makes it very unlikely that a 5 MWh Joule-heated-molten-salt-plus-turbine system is cost-competitive with a 5 MWh lithium-ion system under the claim's bare nameplate-capacity framing

**Pre-check:** head GT-8, GT-10, C2 (MEDIUM) · ?-marked: none · lowest cited: MEDIUM · Inputs ceiling: MEDIUM
**Confidence:** MEDIUM — capped by C2's MEDIUM band (lowest-rated chain on this head). The first hop also assumes a 0.5-2 MW / 2.5-10 hour duration range for the 5 MWh system, since the claim states no power rating (assumption A8, already in the Assumptions Table prior to this chain); verification that would remove A8 as a cause of downgrade: a stated power rating/duration for the system, after which this chain's cost estimate could be computed exactly rather than bracketed.

### Conclusion C5: Cost-competitiveness with lithium-ion is plausible for this architecture only at much larger scale and longer duration than 5 MWh implies, or via a hybrid design — not for the thermal-only system the claim describes

GT-10 (duration-dependent cost-structure identity) + C4 (5 MWh thermal likely cost-uncompetitive) + GT-9 (Li-ion utility-scale benchmark, $125/kWh, $65/MWh LCOS)
→ scoring four options — short-duration thermal-only at 5 MWh, long-duration/larger-scale thermal-only, lithium-ion-only at 5 MWh, and a hybrid pairing lithium-ion for short-duration response with thermal storage for long-duration bulk energy — against weighted criteria fixed before scoring (round-trip efficiency weight 5, $/kWh at the stated scale weight 5, duration flexibility weight 3, technology maturity weight 3, siting/balance-of-plant complexity weight 2) shows lithium-ion-only winning decisively at the 5 MWh scale the claim specifies, driven almost entirely by the efficiency and $/kWh criteria C4 and GT-9 establish
→ the same weighted scoring flips only when the duration criterion is pushed far outside the claim's implied range, toward the 8-to-24-plus-hour, multi-gigawatt-hour-class durations where cheap salt energy-capacity dominates and the turbine's fixed cost is amortized over far more throughput, which is the regime actual CSP-with-storage and ETES projects are built for
→ a composite, hybrid option is not ruled out by any ground truth and scores competitively on duration flexibility without inheriting the small-scale power-block cost penalty of a thermal-only system, so the honest answer to "is it cost-competitive" at 5 MWh is not a flat no across every possible design, only a flat no for the thermal-only architecture the claim as worded describes
→[2nd] a developer who continues to market an 85 percent round-trip figure for a 5 MWh thermal-only system risks losing credibility with financiers and offtakers the first time an independent engineer runs the two-line Carnot check in chain C1, and competing lithium-ion suppliers gain a marketing advantage by publishing third-party-verified round-trip numbers instead *[Assumes: A13 — financiers, offtakers, and regulators eventually check or discover the true efficiency rather than relying on an unverified figure indefinitely]*
→[3rd] once operators and regulators correctly re-segment Joule-heated molten-salt storage into the long-duration, industrial-heat or bulk-energy niche where this chain's crossover actually favors it, rather than competing head-to-head with batteries at short duration, financing terms for appropriately-scoped thermal projects should improve relative to projects marketed with inflated short-duration round-trip claims

**Pre-check:** head GT-10, C4 (MEDIUM), GT-9 · ?-marked: none · lowest cited: MEDIUM · Inputs ceiling: MEDIUM
**Confidence:** MEDIUM — capped by C4's MEDIUM band (lowest-rated chain on this head), which itself carries the A8 duration-assumption caveat explained there. This chain's own hops are direct weighted-scoring arithmetic and introduce no further downgrade cause beyond the `[Assumes: A13]` premise on the second-order extension, which qualifies only the `→[2nd]`/`→[3rd]` effects, not the endpoint `C5` conclusion itself.

---

## 5. Abandoned Reasoning

### Dead End: Using the claim's 290°C cold-tank temperature as the Carnot cold reservoir

**What was tried:** Computed Carnot efficiency using T_hot = 565°C and T_cold = 290°C directly, as the claim's own stated operating range invites.

**Why abandoned:** 290°C is the storage system's cold-tank *return* temperature (where salt returns after giving up heat to the steam generator), not the power cycle's heat-rejection (condenser) temperature — contradicted by A3's Discard verdict. Using it conflates the storage loop with the power cycle, which is physically incorrect for computing the power block's efficiency ceiling, even though it happens to yield an even lower number (≈32.8%, see GT-3) that doesn't rescue the claim either.

**What it ruled out:** It rules out treating this wrong-but-conservative number as a legitimate correction — it checks the wrong physical boundary rather than the right one (ambient/condenser temperature, used correctly in GT-3 / chain C1) — and shows that even the claim's own framing, read in the most literal way, cannot be salvaged into supporting 85%+ under any reading of which two temperatures bound the power cycle.

### Dead End: Treating SEHRENE's "80-85%" claim (GT-6?) as a live rival that validates the headline 85%+ figure

**What was tried:** Considered whether the SEHRENE vendor claim should be read as independent confirmation that 85%+ round-trip efficiency has in fact been demonstrated, rivaling chain C1's and chain C3's physics-based refutation.

**Why abandoned:** GT-6? is an unverified, secondary-source, early-stage vendor claim with no stated metric definition. If it meant full electricity-to-electricity round trip at these temperatures, it would itself violate the Carnot ceiling established in GT-3 (≈62.6%) and contradicted by chain C1 — the belief does not survive contact with a ground truth. Far more likely, following the pattern established by GT-4 (99% charge-only) and GT-7? (97% heat-only), it describes a heat-delivery or charge-only efficiency metric rather than a full electricity round trip, which is consistent with the physics rather than contradicting it.

**What it ruled out:** It rules out relying on an undefined vendor marketing figure as evidence against an established physical bound, and it rules GT-6? out as a load-bearing input to any chain in this analysis (hence its `?` and its absence from the head of chains C1-C5).

### Dead End: Treating Malta Inc.'s heat-pump-assisted architecture as representative of the claim's Joule-heating architecture

**What was tried:** Considered citing Malta's "up to 60%" figure (GT-5) as direct evidence that the claim's specific Joule-heating-plus-turbine design could reach a similar or higher number.

**Why abandoned:** Malta's system uses a reversible heat-pump/Brayton-cycle architecture operating between different, more favorable temperature points than pure resistive heating of salt followed by a Rankine cycle. The claim explicitly describes "electricity into heat" (resistive/Joule heating), not a heat-pump cycle, so Malta's figure is architecturally non-equivalent; using it as the claim's own achievable ceiling would be reasoning by analogy without grounding in a ground truth about the claim's specific architecture.

**What it ruled out:** It rules out collapsing every "molten salt" architecture into a single efficiency number (directly addressing assumption A5). Malta's figure is retained only as the best-in-class reference point in the theoretical-limit bracket (chain C3), never as a stand-in for the claim's own system.

---

## 6. Conclusion

**Recommended approach:** Reject the claim's efficiency figure and its cost-competitiveness claim as stated, and replace both with the physically and economically grounded picture the chains establish: full electricity-to-electricity round-trip efficiency for a Joule-heated molten-salt system discharging through a conventional heat engine is capped at roughly 60-63% by the Carnot limit and realistically runs 33-43% in credible real-world designs (chain C1, chain C2, chain C3), not 85%+; and a 5 MWh instance of this architecture is very likely not cost-competitive with a same-capacity lithium-ion system once small-scale power-block cost penalties and the efficiency-driven throughput penalty are included (chain C4), with cost-competitiveness becoming plausible only at much larger scale and longer discharge duration, or via a hybrid design, than the claim's 5 MWh framing implies (chain C5).

**Key insight:** The claim's 85%+ figure is almost certainly quoting, or conflating with, the charging-stage efficiency alone — electricity converted to heat via resistive heating, which genuinely can exceed 95-99% (chain C1) — rather than the full round trip, because the discharge stage's reconversion of heat back to electricity is a heat-engine process subject to the second law, and the real-world figures measured for full electricity-to-electricity round trips land at roughly half the claimed number (chain C2, chain C3).

**Trade-offs acknowledged:** This conclusion assumes a representative ambient heat-rejection temperature and a plausible power rating/duration for the 5 MWh system, since the claim specifies neither; a stated duration would let chain C4 and chain C5 be recomputed exactly rather than bracketed, and could move the cost verdict toward or away from competitiveness. This analysis also accepts, rather than independently re-deriving, the general engineering heuristic that real heat engines achieve roughly 55 to 70 percent of their Carnot ceiling (chain C2).

**Pre-check:** head C1 (HIGH), C2 (MEDIUM), C3 (HIGH), C4 (MEDIUM), C5 (MEDIUM) · ?-marked: none · lowest cited: MEDIUM · Inputs ceiling: MEDIUM
**Confidence:** MEDIUM — the efficiency-impossibility verdict rests most directly on chain C1 and chain C3 (both HIGH: 85%+ is physically impossible at these temperatures), but the narrower 33-43% realistic-efficiency estimate and the cost-competitiveness verdict rest on chain C2, chain C4, and chain C5 (all MEDIUM), so the Conclusion as a whole, which bundles both sub-claims, is rated at its weakest contributing chain. Chain C2 is MEDIUM because its bracketing hop rests on an `[Assumes: A12]` engineering heuristic not read at a cited source this session (verification: read a documented CSP plant's gross-cycle-efficiency specification). Chain C4 is MEDIUM because it assumes a duration/power rating for the 5 MWh system that the claim never states (verification: obtain the claim's actual intended power rating/duration). Chain C5 is MEDIUM because it is capped by chain C4's band. No `GT-N?` input is used directly by the Conclusion.
## Appendix — process output

## Assumption Audit (process output)

| Chain | Step | Step Text (brief) | Assumption surfaced? | Added to Table? |
|-------|------|--------------------|-----------------------|------------------|
| C1 | 1 | Carnot cap applies between hot salt and ambient | none (A11 already covers ambient temp) | n/a |
| C1 | 2 | ideal ceiling ≈62.6% | none | n/a |
| C1 | 3 | multiply charge × discharge ceiling | none | n/a |
| C1 | 4 | 85%+ not physically achievable | none | n/a |
| C2 | 1 | real effectiveness ≈55-70% of Carnot | A12 (second-law effectiveness heuristic) | yes |
| C2 | 2 | combine charge × discharge range | none | n/a |
| C2 | 3 | compare bracket to Hamburg/Malta | none | n/a |
| C2 | 4 | 85%+ is ~1.9-2.6x too high | none | n/a |
| C3 | 1 | gap conventional→demonstrated ≈15pp | none | n/a |
| C3 | 2 | gap demonstrated→ideal ≈2-3pp | none | n/a |
| C3 | 3 | 85%+ exceeds the physical ceiling | none | n/a |
| C4 | 1 | 5 MWh implies 0.5-2 MW power rating | none (A8 already covers duration ambiguity) | n/a |
| C4 | 2 | power-block cost penalty falls on thermal system | none | n/a |
| C4 | 3 | efficiency penalty raises input-electricity need 2.0-2.7x | none | n/a |
| C4 | 4 | thermal system likely not cost-competitive at 5 MWh | none | n/a |
| C5 | 1 | weighted trade-off: Li-ion wins at 5 MWh | none | n/a |
| C5 | 2 | crossover only at long duration/large scale | none | n/a |
| C5 | 3 | hybrid option viable, not ruled out | none | n/a |
| C5 | 2nd | financiers/competitors react to inflated claims | A13 (market-rationality assumption) | yes |
| C5 | 3rd | market re-segments thermal storage by duration | A13 (same assumption, already added) | n/a |

Scan complete: 5 chains, 20 steps, 2 new assumptions surfaced (A12, A13), both added to the Assumptions Table once each.

## Techniques not applied (process output)

- fishbone — not applicable — the assumption space here (efficiency-metric equivocation, Carnot physics, small-scale cost economics) was tractable by direct enumeration; no diffuse multi-causal brainstorm was needed.
- five-whys (causal mode) — not applicable — this analysis evaluates a forward claim about physics and economics, not a recurring failure symptom requiring causal-chain drill-down; the reduce-to-primitives mode of five-whys was used instead, in Phase 3's irreducibility test (decomposing "round-trip efficiency" into charge-efficiency × discharge-efficiency, bottoming out at GT-1/GT-2).
- pre-mortem — not applicable — the Phase 5 conclusion is a claim about physics and cost, not a plan or recommendation to execute; the decision rule routes claims to inversion instead, applied in the adversarial pass below.
## Adversarial pass (process output)

**Recompute.** GT-3: η = 1 − 313.15/838.15 = 1 − 0.3736 = 0.6264 → 62.6% (recomputes). Alternate (wrong-reservoir) reading using 290°C: 1 − 563.15/838.15 = 1 − 0.6719 = 0.3281 → 32.8% (recomputes; see Dead End 1). Chain C2 bracket: 62.6% × 0.55 = 34.4%; 62.6% × 0.70 = 43.8% → discharge-stage bracket ≈34-44%; combined with ~97% average charge efficiency: 0.97 × 0.344 = 33.4%, 0.97 × 0.438 = 42.5% → full round-trip bracket ≈33-43% (recomputes; text corrected from an initial 33-44% draft figure to 33-43% for consistency). Ratio claim: 85/43 = 1.98, 85/33 = 2.58 → "roughly 1.9 to 2.6 times higher" (recomputes). Chain C3 gaps: 60 − 44.6 = 15.4 ≈ 15; 62.6 − 60 = 2.6 ≈ 2-3 (recomputes). Chain C4 throughput-penalty ratio: (1/0.33)/(1/0.90) = 0.90/0.33 = 2.73; (1/0.43)/(1/0.90) = 0.90/0.43 = 2.09 → "roughly 2.0 to 2.7 times" (recomputes; corrected from an initial 2.3-3x draft figure during this recompute pass).

**Sensitivity.** The efficiency-impossibility sub-claim (chains C1, C3) is insensitive to any realistic input: it rests on GT-2 (the second law of thermodynamics), which is not `?`-marked and has no credible failure mode within standard physics — no plausible verification would overturn it. The one input that would most change this analysis's *numbers* (not its direction) is A11, the assumed ~40°C ambient condenser temperature: even an unusually cold ~10°C heat-rejection temperature only raises the ideal ceiling to ≈67.9%, still far below 85%. The cost-competitiveness sub-claim (chains C4, C5) is far more sensitive: the single input most likely to flip that verdict is A8, the assumed power rating/duration for the 5 MWh system — not a ground truth but an explicit gap in the original claim. A stated duration of roughly 10+ hours (large-scale, bulk-energy regime) would move chain C4/C5 toward "plausibly competitive," which chain C5 already anticipates as the long-duration crossover condition rather than treating it as a hidden risk.

**Rival.** For chains C1/C3 (efficiency): the only candidate rival surfaced in this analysis's research is SEHRENE's unverified "80-85%" claim (GT-6?), ruled out in Abandoned Reasoning Dead End 2 — it either contradicts the Carnot ceiling (if read as a full round-trip figure) or, far more plausibly, measures a different (heat-delivery) quantity, consistent with the GT-4/GT-7? pattern. For chains C4/C5 (cost): no independent rival conclusion was found claiming a 5 MWh thermal-only system beats lithium-ion on cost; the long-duration/larger-scale crossover is already incorporated into chain C5's own finding as a condition, not left as an unresolved competing claim.

**Premise (past tense, inversion).** The headline conclusion is already false: a 5 MWh Joule-heated molten-salt system has in fact been demonstrated, under audited conditions, to round-trip electricity at 85%+ efficiency and to beat lithium-ion on cost at that scale.

**Causes (unfiltered, from at least three stakeholder viewpoints).**
*Vendor/developer viewpoint:* (1) the vendor measured and reported only the charging-stage efficiency and labeled it "round-trip" without the discharge stage; (2) the vendor used an artificially cold, non-ambient heat-rejection temperature in a lab/demo setting unrepresentative of field deployment; (3) the 565°C/290°C figures describe an unbuilt next-generation design, and the 85% figure is a zero-loss simulation output, not a measured result.
*Independent engineer/auditor viewpoint:* (4) the auditor's own Carnot check used the wrong cold-reservoir temperature (the storage-loop return temperature instead of the condenser temperature), incorrectly validating an inflated number; (5) metering boundaries excluded auxiliary/parasitic loads (pumps, trace heating, standby losses) from the "input electricity" side, inflating the measured ratio.
*Financier/offtaker viewpoint:* (6) the PPA/financing model was built on the vendor's spec sheet without independent verification, and nobody ran a physics sanity check before signing; (7) the battery-system cost benchmark used in the comparison was an outdated, higher $/kWh figure, making the thermal system look relatively cheaper than it is against current lithium-ion pricing.
*Competing battery-supplier viewpoint:* (8) the 5 MWh comparison never specified a power rating, letting the thermal system be implicitly quoted at a long, favorable duration while the claim's framing suggests a short one; (9) the thermal system's degradation/availability losses over its operating life were excluded from the efficiency and cost figures used in the claim.

**Clusters.**
- *Cluster A — Metric conflation* (causes 1, 3): the "85%" figure measures something other than full electricity-to-electricity round trip. Bears on: GT-4, GT-6?, GT-7?, chain C1, chain C2.
- *Cluster B — Miscalculated or cherry-picked physics* (causes 2, 4, 5): the Carnot/efficiency calculation was done on the wrong boundary or favorable conditions. Bears on: GT-3, A3, chain C1, chain C3, Abandoned Reasoning Dead End 1.
- *Cluster C — Unverified/undisclosed cost-comparison basis* (causes 6, 7, 8, 9): the cost claim rests on an unstated power rating, an unaudited vendor spec, and/or a stale battery benchmark. Bears on: GT-9, GT-10, A8, A9, chain C4, chain C5.

**Disposition.**
- Cluster A — Plan change: before accepting any "round-trip efficiency" figure, require the source to state explicitly which stage(s) it spans (charge-only, discharge-only, or full round trip), and reject or re-flag any figure that does not; this analysis applies that standard and has already flagged GT-6? and GT-7? accordingly.
- Cluster B — Plan change: any Carnot sanity check on a thermal-storage efficiency claim must use the power cycle's actual heat-rejection (condenser) temperature, never a storage-loop return temperature, as fixed in GT-3 and chain C1; this is the standing method applied here and recommended for any future such claim.
- Cluster C — Accepted risk with named mitigation: this analysis cannot force the original claim to disclose a power rating/duration or an audited cost basis; the accepted risk is that chain C4's and chain C5's cost verdict is bracketed rather than exact, and the named mitigation is that the Conclusion's confidence line states this explicitly and names the specific input (duration) that would resolve it.

**Falsification.** The conclusion is false if an independently audited, metered field deployment of a pure Joule-heated molten-salt storage system (not a heat-pump-assisted architecture like Malta's) demonstrates a sustained full electricity-to-electricity round-trip efficiency at or above 60% between a ~565°C hot reservoir and ambient heat rejection — which would itself exceed this analysis's computed ideal ceiling and would falsify GT-2/GT-3 or reveal a hot-side temperature higher than stated — or if a specific, stated power rating and duration for the 5 MWh system, combined with a current, audited capital-cost quote, shows total $/kWh at or below the lithium-ion benchmark in GT-9 adjusted to the same scale.
## §6→§4 closure ledger (process output)

- "full electricity-to-electricity round-trip efficiency ... is capped at roughly 60-63% by the Carnot limit and realistically runs 33-43% in credible real-world designs" → chain C1, chain C2, chain C3 ✓
- "a 5 MWh instance of this architecture is very likely not cost-competitive with a same-capacity lithium-ion system" → chain C4 ✓
- "cost-competitiveness becoming plausible only at much larger scale and longer discharge duration, or via a hybrid design" → chain C5 ✓
- "The claim's 85%+ figure is almost certainly quoting, or conflating with, the charging-stage efficiency alone ... which genuinely can exceed 95-99%" → chain C1 ✓
- "the real-world figures measured for full electricity-to-electricity round trips land at roughly half the claimed number" → chain C2, chain C3 ✓
- "This conclusion assumes a representative ambient heat-rejection temperature and a plausible power rating/duration for the 5 MWh system ... chain C4 and chain C5 be recomputed exactly" → chain C4, chain C5 ✓
- "This analysis also accepts ... the general engineering heuristic that real heat engines achieve roughly 55 to 70 percent of their Carnot ceiling" → chain C2 ✓
- "**Confidence:** MEDIUM — the efficiency-impossibility verdict rests most directly on chain C1 and chain C3 (both HIGH) ... narrower 33-43% ... rest on chain C2, chain C4, and chain C5" → chain C1, chain C2, chain C3, chain C4, chain C5 ✓

Scan complete: 8 Conclusion-section claims, 8 traced to chains, 0 cut.
## Self-audit scan (process output)

| Chain | Chain Head (brief) | Form conforming? | Rule applied | Dependency clean? | Band | Act attempted? | Edges fired |
|-------|---------------------|-------------------|---------------|--------------------|------|-----------------|-------------|
| C1 | GT-1, GT-2, GT-3 | yes | n/a | yes | HIGH | no (physical law / direct computation, no external source to open) | none |
| C2 | C1 (HIGH), GT-4, GT-5 | yes | n/a | yes | MEDIUM | yes (GT-4, GT-5 opened directly) | none |
| C3 | GT-3, GT-5, GT-4 | yes | n/a | yes | HIGH | yes (GT-4, GT-5 opened directly) | none |
| C4 | GT-8, GT-10, C2 (MEDIUM) | yes | n/a | yes | MEDIUM | yes (GT-8 opened directly) | none |
| C5 | GT-10, C4 (MEDIUM), GT-9 | yes | n/a | yes | MEDIUM | yes (GT-9 opened directly) | none |

| §6 Span (brief) | Construct | Claim under R11? | R11 clause applied | Chain cited |
|-------------------|-----------|-------------------|----------------------|---------------|
| "**Recommended approach:** Reject the claim's efficiency figure..." | bold lead-in | yes | always-a-claim lead-in | C1, C2, C3, C4, C5 |
| "**Key insight:** The claim's 85%+ figure is almost certainly..." | bold lead-in | yes | always-a-claim lead-in | C1, C2, C3 |
| "**Trade-offs acknowledged:** This conclusion assumes a representative ambient..." | bold lead-in | yes | always-a-claim lead-in | C4, C5 |
| "This analysis also accepts ... 55 to 70 percent of their Carnot ceiling (chain C2)" | prose, second sentence of Trade-offs span | yes | direct entailment check: new assertion, not a restatement, so counted separately; closes own sentence | C2 |
| "**Pre-check:** head C1 (HIGH), C2 (MEDIUM)..." | bold lead-in | no | pre-check line is part of the Confidence citation apparatus, not itself a separately-scored claim distinct from the Confidence line it sits directly above | n/a |
| "**Confidence:** MEDIUM — the efficiency-impossibility verdict rests..." | bold lead-in | yes | always-a-claim lead-in | C1, C2, C3, C4, C5 |

Scan complete: 5 chain rows, one per section-4 chain block in order; 6 section-6 rows, one per construct in order — 5 claims under R11, 1 excluded. 0 chains malformed, 0 claims untraced.
## Self-Audit Gate (process output)

**Criterion 1: Identify Essence**
Quoted span: "Does a Joule-heated molten-salt thermal storage system operating between roughly 290°C and 565°C deliver a true electricity-to-electricity round-trip efficiency above 85%, and is a 5 MWh instance of such a system cost-competitive with a 5 MWh lithium-ion battery system, once the power rating/duration implied by that energy capacity is accounted for?"
Band: **Rigorous**
Justification: The statement names the specific underlying question (metric-stage ambiguity plus scale-conditioned cost) rather than restating the user's prompt verbatim, and each success criterion beneath it is a verb+subject+testable-outcome triplet checkable against the Conclusion section without further clarification.

**Criterion 2: Challenge Assumptions**
Quoted span: "A6: Existing commercial/demonstration ETES and CSP-with-storage systems validate round-trip efficiencies at or near 85% | untested belief | verify | Discard — best documented figures are ~44.6% (Hamburg) and 'up to 60%' (Malta); no independently-opened source supports 85% for a full electricity round trip | GT-4, GT-5; GT-6? unverified — flagged" and the Assumption Audit scan: "Scan complete: 5 chains, 20 steps, 2 new assumptions surfaced (A12, A13), both added to the Assumptions Table once each."
Band: **Rigorous**
Justification: All 13 rows use the four-type scheme with matching prescribed treatments, every Verdict cell is a leading token (Accept/Challenge/Discard) followed by an em-dash and a specific justification, multiple assumptions are genuinely challenged and discarded (not merely labelled Accept), and the Assumption Audit scan confirms the audit ran exhaustively over every named chain step.

**Criterion 3: Establish Ground Truths**
Quoted span: "**Provenance summary:** `?`-marked: GT-6, GT-7 (2 of 10). Read-at-source locations for unsuffixed ground truths feeding load-bearing chains: ... GT-4 (nsenergybusiness.com article body, two quoted sentences...) ... GT-9 (ember-energy.org article body, quoted $125/kWh and $65/MWh figures)..."
Band: **Rigorous**
Justification: Checking the enumeration against the Ground Truths list confirms exactly GT-6 and GT-7 carry `?` and no others; every unsuffixed GT feeding the HIGH-confidence chains C1 and C3 (GT-1, GT-2, GT-3, GT-4, GT-5) names a read-at-source location (a quoted passage for GT-4/GT-5, an inline computation for GT-3, "not applicable" with reason for the two physical laws GT-1/GT-2); no Phase-2 Discard-verdict assumption (A3-A7) appears in this list.

**Criterion 4: Reason Upward**
Quoted span (self-audit scan, chain-form table): "C1 | GT-1, GT-2, GT-3 | yes | n/a | yes | HIGH | no ... | none" through "C5 | GT-10, C4 (MEDIUM), GT-9 | yes | n/a | yes | MEDIUM | yes ... | none" — all five rows read `Form conforming? = yes` and `Dependency clean? = yes`; and from the analysis text, Abandoned Reasoning's "Dead End: Treating Malta Inc.'s heat-pump-assisted architecture as representative of the claim's Joule-heating architecture ... using it as the claim's own achievable ceiling would be reasoning by analogy without grounding in a ground truth about the claim's specific architecture."
Band: **Rigorous**
Justification: The scan shows all five chains well-formed and dependency-clean with no block scored `no` or `unreached`; every conclusion in sections 4 and 6 has exactly one chain; each chain head uses the prescribed `GT-N (gloss) + ...` / `Cn (gloss)` form with at least one genuine intermediate; the two new assumptions surfaced during chain construction (A12, A13) are declared inline with `[Assumes: X]`; Abandoned Reasoning documents three dead ends with the full What-was-tried/Why-abandoned/What-it-ruled-out structure and explicitly refuses an analogy-as-evidence shortcut rather than merely avoiding the word "analogy."

**Criterion 5: Validate**
Quoted span: "Cluster B — Plan change: any Carnot sanity check on a thermal-storage efficiency claim must use the power cycle's actual heat-rejection (condenser) temperature, never a storage-loop return temperature, as fixed in GT-3 and chain C1" and "Chain C4 is MEDIUM because it assumes a duration/power rating for the 5 MWh system that the claim never states (verification: obtain the claim's actual intended power rating/duration)."
Band: **Rigorous**
Justification: The adversarial pass record carries all five parts (Recompute, Sensitivity, Rival, Premise/Causes/Clusters/Disposition, Falsification) with every cluster naming a plan change or an accepted risk with a named mitigation; every MEDIUM/LOW confidence line names its specific `Cn` cause and verification path (no bare "unclear" caveats); no chain rated HIGH consumes a `?`-marked input; C4 and C5 are each capped at their cited chain's band exactly as D-07 requires; the overall Conclusion's MEDIUM rating matches its weakest contributing chain.

**Criterion 6: Conclusion-to-Ground-Truth Traceability**
Quoted span (self-audit scan, claim-inventory table): "'**Recommended approach:** Reject the claim's efficiency figure...' | bold lead-in | yes | always-a-claim lead-in | C1, C2, C3, C4, C5" and "Scan complete: ... 5 claims under R11, 1 excluded ... 0 claims untraced."
Band: **Rigorous**
Justification: Every claim-bearing construct in section 6 traces to a named section-4 chain (confirmed by the scan's own reconciliation line showing zero untraced claims), no claim is introduced in section 6 without a prior chain, and the Key Insight ("the claim's 85%+ figure is almost certainly quoting... the charging-stage efficiency alone... rather than the full round trip") is a non-obvious finding distinct from the Recommended Approach's remediation, not a restatement of it.

**Gate result:** cleared · passes: 1 · Fix/Repeat fired: no

## Structured summary (process output)

```json
{
  "schema_version": 1,
  "run_mode": "full-composer",
  "assumptions": [
    {"id": "A-1", "type": "convention", "verdict": "Challenge"},
    {"id": "A-2", "type": "physical law", "verdict": "Accept"},
    {"id": "A-3", "type": "convention", "verdict": "Discard"},
    {"id": "A-4", "type": "untested belief", "verdict": "Discard"},
    {"id": "A-5", "type": "convention", "verdict": "Discard"},
    {"id": "A-6", "type": "untested belief", "verdict": "Discard"},
    {"id": "A-7", "type": "convention", "verdict": "Discard"},
    {"id": "A-8", "type": "convention", "verdict": "Challenge"},
    {"id": "A-9", "type": "convention", "verdict": "Challenge"},
    {"id": "A-10", "type": "current constraint", "verdict": "Accept"},
    {"id": "A-11", "type": "current constraint", "verdict": "Accept"},
    {"id": "A-12", "type": "untested belief", "verdict": "Challenge"},
    {"id": "A-13", "type": "untested belief", "verdict": "Challenge"}
  ],
  "ground_truths": [
    {"id": "GT-1", "read_at_source": true},
    {"id": "GT-2", "read_at_source": true},
    {"id": "GT-3", "read_at_source": true},
    {"id": "GT-4", "read_at_source": true},
    {"id": "GT-5", "read_at_source": true},
    {"id": "GT-6", "read_at_source": false},
    {"id": "GT-7", "read_at_source": false},
    {"id": "GT-8", "read_at_source": true},
    {"id": "GT-9", "read_at_source": true},
    {"id": "GT-10", "read_at_source": true}
  ],
  "chains": [
    {"id": "C1", "confidence": "HIGH", "rests_on": ["GT-1", "GT-2", "GT-3"]},
    {"id": "C2", "confidence": "MEDIUM", "rests_on": ["C1", "GT-4", "GT-5"]},
    {"id": "C3", "confidence": "HIGH", "rests_on": ["GT-3", "GT-5", "GT-4"]},
    {"id": "C4", "confidence": "MEDIUM", "rests_on": ["GT-8", "GT-10", "C2"]},
    {"id": "C5", "confidence": "MEDIUM", "rests_on": ["GT-10", "C4", "GT-9"]}
  ],
  "dead_ends": [
    "Using the claim's 290°C cold-tank temperature as the Carnot cold reservoir",
    "Treating SEHRENE's \"80-85%\" claim (GT-6?) as a live rival that validates the headline 85%+ figure",
    "Treating Malta Inc.'s heat-pump-assisted architecture as representative of the claim's Joule-heating architecture"
  ],
  "techniques": {
    "applied": ["theoretical-limit", "inversion", "five-whys", "estimate", "trade-off", "second-order"],
    "not_applied": [
      {"technique": "fishbone", "phase": 2, "reason": "the assumption space here (efficiency-metric equivocation, Carnot physics, small-scale cost economics) was tractable by direct enumeration; no diffuse multi-causal brainstorm was needed"},
      {"technique": "pre-mortem", "phase": 5, "reason": "the Phase 5 conclusion is a claim about physics and cost, not a plan or recommendation to execute; the decision rule routes claims to inversion instead"}
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
    "recommendation": "Reject the claim's efficiency figure and its cost-competitiveness claim as stated, and replace both with the physically and economically grounded picture the chains establish: full electricity-to-electricity round-trip efficiency for a Joule-heated molten-salt system discharging through a conventional heat engine is capped at roughly 60-63% by the Carnot limit and realistically runs 33-43% in credible real-world designs (chain C1, chain C2, chain C3), not 85%+; and a 5 MWh instance of this architecture is very likely not cost-competitive with a same-capacity lithium-ion system once small-scale power-block cost penalties and the efficiency-driven throughput penalty are included (chain C4), with cost-competitiveness becoming plausible only at much larger scale and longer discharge duration, or via a hybrid design, than the claim's 5 MWh framing implies (chain C5).",
    "confidence": "MEDIUM",
    "rests_on": ["C1", "C2", "C3", "C4", "C5"]
  }
}
```
