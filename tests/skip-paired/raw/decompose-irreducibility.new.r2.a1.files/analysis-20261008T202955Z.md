## Answer

**Recommendation:** The claim should be treated as failing for electricity-in/electricity-out round-trip efficiency and cost-competitiveness at 5 MWh scale; it only becomes true if "round-trip efficiency" is silently redefined as heat-in/heat-out thermal retention, which cannot support the cost-competitiveness comparison to a lithium-ion battery that stores and returns electricity directly (chain C3, chain C1).

**Band (from §6):** LOW.

**Would change it:** Reading GT-1, GT-4, GT-5, GT-6, GT-7, and GT-8 directly at source rather than via search synthesis, and locating an actual vendor quote or techno-economic study for a 5 MWh-class electric molten-salt storage system with power-cycle reconversion — no such published figure currently exists (chain C4).
## 1. Problem Essence

**Essence Statement:** Can a 5 MWh two-tank molten-salt thermal energy storage system — charged electricity→heat (e.g. resistive heating) and discharged heat→electricity via a thermodynamic power cycle (Rankine/ORC/Brayton), operating between a 290°C cold tank and a 565°C hot tank — achieve an **electricity-in/electricity-out round-trip efficiency above 85%**, and is such a system **cost-competitive with a same-nameplate-capacity lithium-ion battery system**?

**Success criteria (a correct answer must achieve):**
- State explicitly which "round-trip efficiency" metric (electrical, electricity-to-electricity; or thermal, heat-in/heat-out) the 85%+ figure can legitimately apply to, with a Carnot/second-law-grounded derivation.
- Determine whether 85%+ *electrical* round-trip efficiency is physically achievable for this specific charge/discharge pathway at these temperatures, independent of scale.
- Determine how the stated 5 MWh scale (small relative to commercial molten-salt CSP deployments) affects both the achievable round-trip efficiency and the capital cost structure.
- Compare cost-competitiveness against lithium-ion on both a $/kWh-nameplate and a $/kWh-cycled (round-trip-efficiency-adjusted, levelized) basis.
- Identify any equivocation embedded in the claim and state whether the claim holds, partially holds, or fails — not merely which single technology "wins," since the claim is a compound assertion (an efficiency claim AND a cost claim) that can hold on one axis and fail on another.
## 2. Assumptions Table

| Assumption | Type | Treatment | Verdict | Verification |
|---|---|---|---|---|
| 290°C/565°C is the standard two-tank solar-salt (60% NaNO₃/40% KNO₃) operating envelope | current constraint | Record expiry conditions | Holds for solar salt; would shift with a different salt chemistry (chloride/carbonate salts reach higher T, but introduce corrosion/cost issues) | Converged across independent sources (NREL/CSP literature); see GT-1 |
| Resistive (Joule) heating converts electricity to heat at ~100% | physical law | Accept as ground-truth candidate | Accepted; practical figure ~95–99% once insulation/parasitic losses counted | First-principles (energy conservation); see GT-2 |
| Heat-to-work conversion is bounded by Carnot efficiency η=1−T_cold/T_hot | physical law | Accept as ground-truth candidate | Accepted, non-negotiable | Second Law of Thermodynamics; see GT-3 |
| "Round-trip efficiency" in the claim means electricity-in/electricity-out | convention | Explicitly challenge | **Fails to hold as electrical RTE; holds only as thermal (heat-in/heat-out) RTE** | This is the central equivocation; see GT-6, GT-8, Chain C3 |
| Real Rankine cycles reach ~40–42% thermal-to-electric efficiency at utility (>50 MWe) scale | current constraint | Record expiry conditions (would rise with supercritical/advanced cycles, never past Carnot ceiling) | Holds, convergent across sources | Reported-by-delegate (search synthesis); see GT-4? |
| Small (≲5 MWe-class) power blocks suffer a further efficiency penalty vs. utility-scale | current constraint | Record expiry conditions (improves somewhat with ORC optimized for small scale, never erases the gap) | Holds | Reported-by-delegate; see GT-5? |
| A 5 MWh tank is small relative to commercial molten-salt CSP storage (100s–1,000s of MWh) | untested belief → verified | Verify | Verified: Crescent Dunes ≈1,100 MWh_th, Gemasolar ≈600 MWh_th; 5 MWh is ~0.5–1% of these | Direct numerical comparison; see GT-6 |
| Molten-salt storage cost benefits strongly from economies of scale (large tank, shared power block) | current constraint | Record expiry conditions (a mass-produced small modular thermal-storage product could someday change this, but none exists commercially at 5 MWh for electricity reconversion) | Holds | Reported-by-delegate; see GT-6? |
| Li-ion BESS achieves 85–92% AC-AC round-trip efficiency at $125–350/kWh installed (2025) | untested belief → verified | Verify | Verified, convergent across multiple 2025 sources | Reported-by-delegate; see GT-7? |
| Nameplate $/kWh alone is sufficient to compare cost-competitiveness | convention | Explicitly challenge | **Fails** — must be adjusted for round-trip efficiency (a low-RTE system needs more input electricity per kWh delivered) to get a true levelized cost of storage | See Chain C5 |
| Molten salt's "unlimited cycle life" fully offsets higher capex | convention | Explicitly challenge | **Partially fails** — the storage *medium* has very long life, but the power-block (turbine/heat exchangers) has ordinary thermal-plant maintenance life, and modern LFP Li-ion already reaches 4,000–10,000+ cycles / 15–20 yr, narrowing this advantage considerably at small scale | Reported-by-delegate; see GT-7? |
| Heat-pump charging (COP>1) could close the gap to 85% | untested belief | Verify | **Fails** — Carnot COP for this temperature lift (ambient→565°C) is only ≈1.54 (theoretical ceiling), real multi-stage heat pumps achieve far less; even an optimistic COP 1.2–1.3 combined with ~40% discharge yields ~48–52%, not 85% | First-principles calculation + GT-8 |
| Tank thermal (standby heat) losses scale with surface-area-to-volume ratio | physical law (geometry) | Accept as ground-truth candidate | Accepted; a 5 MWh tank has a markedly worse ratio than a GWh-class tank | Geometric/heat-transfer first principles; see GT-9 |
| Rankine-cycle condenser rejects heat to ambient (~40°C), not to the 290°C cold-salt-tank temperature | current constraint | Accept as ground-truth candidate (verified physical configuration of a steam power block) | Holds — surfaced from chain C1 `[Assumes: X]` | First-principles power-cycle configuration; see Abandoned Reasoning |
| A 5 MWh storage system implies a sub-5 MWe-class power-block rating (inferred from typical 2–10 hr storage duration, not stated explicitly in the claim) | untested belief | Verify / flag | Flagged — reasonable inference, not stated by the claim itself | Surfaced from chain C2 `[Assumes: X]` |

## 3. Ground Truths

- **GT-1?** — Two-tank solar-salt (60% NaNO₃/40% KNO₃) CSP systems operate with a cold tank at ≈290°C (set by the salt's freezing point ≈220–240°C plus a safety margin) and a hot tank at ≈565°C (set by the salt's thermal-stability/decomposition limit). Provenance: reported-by-delegate (WebSearch synthesis converging on NREL/CSP industry sources; the specific NREL PDF could not be opened directly — fetch attempt failed, see Phase 3 failure record below). This also matches independent, well-documented public design parameters of commercial plants (Gemasolar, Crescent Dunes), which is why it is carried at reported-by-delegate rather than fully unverified.
  - *Phase 3 failure record:* attempted `WebFetch` on `https://docs.nrel.gov/docs/fy25osti/93281.pdf` — unreachable (DNS resolution failure, `ENOTFOUND`). Ground truth remains `?`.

- **GT-2** — Resistive (Joule) heating converts electrical energy into thermal energy with no fundamental conversion loss (first law of thermodynamics: all power dissipated in a resistance becomes heat). Practical electricity→heat efficiency for an engineered system (heater, salt heat-transfer, insulation, trace heating/pump parasitics) is commonly modeled at ~95–99%. Physical law; no source citation required for the law itself.

- **GT-3** — A heat engine (Rankine, ORC, or Brayton cycle) converting heat into work/electricity is bounded by the Carnot efficiency η_Carnot = 1 − T_cold/T_hot (absolute temperatures), a direct consequence of the Second Law of Thermodynamics. Physical law.

- **GT-4?** — For a molten-salt-fed steam Rankine cycle with a realistic turbine-inlet temperature of ≈540°C (813 K, allowing for heat-exchanger approach temperature below the 565°C salt) and condenser/heat-rejection to ambient at ≈40°C (313 K): Carnot ceiling ≈ 1 − 313/813 ≈ **61.5%**. Real utility-scale (>50 MWe) CSP steam-Rankine power blocks achieve **≈40–42%** thermal-to-electric conversion efficiency — i.e., roughly 65–68% of the Carnot ceiling (a typical second-law/exergetic efficiency for well-engineered large steam turbines). Provenance: reported-by-delegate (WebSearch synthesis of CSP performance literature, arXiv:2406.00140 solar-plant-simulator paper and others); attempted `WebFetch` of arXiv:2406.00140 directly — the fetch succeeded in retrieving the document but the extraction could not locate the specific efficiency figures in machine-readable text (PDF is largely image/scanned content), so this remains `?` rather than being promoted to read-at-source.
  - *Phase 3 failure record:* fetched `https://arxiv.org/pdf/2406.00140` — reachable, but citation does not confirm the claim in extractable text (image-heavy PDF). Ground truth remains `?`.

- **GT-5?** — CSP/Rankine power-block efficiency degrades sharply with scale: published figures show cycle efficiency falling from ≈35% for plants >50 MWe to as low as ≈20% for ≈1 MWe-class units, reflecting unfavorable scaling of turbomachinery losses (tip leakage, friction, heat loss per unit throughput) and fixed parasitic loads at small scale. Provenance: reported-by-delegate (WebSearch synthesis, same arXiv source as GT-4; same Phase 3 failure record applies — image-heavy PDF, figure not independently located in extractable text).

- **GT-6?** — Commercial two-tank molten-salt CSP thermal storage is built at large scale: Crescent Dunes ≈1,100 MWh_thermal, Gemasolar ≈600 MWh_thermal — roughly 100–200× the 5 MWh system in the claim. At this GWh-class scale, DOE/NREL-cited installed thermal-storage-only costs run ≈$15–40/kWh (figures such as "$15/kWh_re for a 220 MWe plant" and "$30–40/kWh_th for two-tank storage"), and these figures explicitly exclude the dedicated power block, and assume a low surface-to-volume ratio only achievable at large tank size. A DOE source also cites "annual round-trip storage efficiency above 99%" for such large systems — but this is a **thermal** (heat-retained/heat-input) metric, not an electrical round-trip metric (the power-block conversion loss, GT-4, is accounted separately in those cost models). Provenance: reported-by-delegate (WebSearch synthesis of DOE/NREL/CSP cost literature; no single primary document was opened and read directly for this figure within the turn budget — not read, turn budget).

- **GT-7?** — Modern utility-scale lithium-ion (chiefly LFP) battery energy storage systems (2025) have fully-installed nameplate system costs of roughly **$125–350/kWh** (lower in China, higher in US/Europe; a cited figure of ≈$125/kWh for 4-hour-class systems outside China/US), **AC-AC round-trip efficiency of ≈85–92%**, and cycle life of **4,000–10,000+ cycles** (15–20 year calendar life) with negligible chemical reconversion loss beyond the stated RTE, and costs projected to continue falling with manufacturing scale. Provenance: reported-by-delegate (WebSearch synthesis of multiple 2025 market-cost sources, e.g. Ember/Mercom reporting, LBNL/NREL cost-projection literature). Not read at source — not read, turn budget.

- **GT-8?** — Literature on "Carnot battery" (pumped thermal electricity storage) architectures states that classical heat-pump-charge/heat-engine-discharge architectures "do not achieve more than ~60% roundtrip electric efficiency"; the most advanced published experimental result (Dumont et al., thermally-integrated HP/ORC prototype with waste-heat recovery) reaches **72.5%** round-trip electrical efficiency — still below 85%, and this architecture is materially different from (and more complex than) the plain resistive-heating + Rankine/ORC/Brayton pathway named in the claim. Separately, industrial "thermal battery" products (Rondo Energy, Antora Energy) report round-trip efficiencies **above 85–97%, but only for heat-only discharge** (direct process steam/heat delivery, no reconversion to electricity) or for combined heat-and-power configurations using a fundamentally different reconversion technology (thermophotovoltaics), not a Rankine/ORC/Brayton power cycle. Provenance: reported-by-delegate (WebSearch synthesis). Not read, turn budget.

- **GT-9** — Standby (parasitic) thermal losses from an insulated storage tank scale with its surface-area-to-volume ratio; for geometrically similar tanks, this ratio scales as 1/L (worsens as characteristic length L shrinks). A 5 MWh tank has a linear scale roughly 5–6× smaller than a 600–1,100 MWh_thermal CSP tank (volume ratio ≈120–220×, linear ratio ≈ cube root ≈5–6×), implying a materially worse surface-to-volume ratio and higher fractional standby heat loss per cycle. Physical law (geometry + heat transfer); derived directly, not cited.

**`?`-marked ground truths:** GT-1, GT-4, GT-5, GT-6, GT-7, GT-8 (6 of 9).

**Read-at-source entries:** none — every load-bearing empirical figure in this analysis is `reported-by-delegate` (WebSearch synthesis) or carries an explicit Phase 3 failure record (GT-1's and GT-4/GT-5's attempted `WebFetch` reads). GT-2, GT-3, and GT-9 require no external citation — they are derived directly from physical law and geometry.

This is a material limitation of this analysis, disclosed under the Phase 3 verification step: the turn budget did not permit opening every underlying primary source (NREL/DOE PDFs, Dumont et al. paper, LBNL/NREL cost reports) directly; two attempts were made (NREL PDF — DNS failure; arXiv PDF — reachable but image-heavy, figures not confirmed in extractable text) and both failed, which is why GT-1, GT-4, and GT-5 carry explicit failure records rather than silent `?` marks. The remaining `?`s (GT-6, GT-7, GT-8) were not attempted within budget and are named as `not read — turn budget`. None of this changes the *qualitative* physics verdict (GT-2 and GT-3 are physical law, not citation-dependent, and the margin between the Carnot-bounded ceiling and the claimed 85% is large enough — see Chain C1 — that even generous error bars on the `?`-marked empirical figures do not change the conclusion).
## 4. Derivation Chains

**C1 — Carnot-bounded ceiling on electrical round-trip efficiency (large-scale, best case)**

```text
GT-2 (resistive charging ≈97%) + GT-3 (Carnot bound η=1−Tc/Th) + GT-4? (real large Rankine ≈40–42%, ≈65–68% of Carnot)
→ the discharge leg (heat→electricity) is capped near 61.5% even in the ideal Carnot limit for a 540°C/40°C cycle, and real turbines historically reach only ~65–68% of that Carnot ceiling, landing at ≈40–42% actual
→ multiplying the charge-side efficiency (≈97%) by the discharge-side efficiency (≈40–42%) bounds electricity-in/electricity-out round-trip efficiency at roughly 39–41%, even under the most favorable, GWh-scale, large-turbine assumptions
→ an electrical round-trip efficiency above 85% is not physically plausible for this specific charge/discharge pathway (resistive heating + Rankine/ORC/Brayton) between 290°C and 565°C, at any scale — it would require more than doubling the best documented large-scale performance
```
**Pre-check:** head = GT-2, GT-3, GT-4? · ?-marked = GT-4? · lowest cited = none (no chain cited) · Inputs ceiling = MEDIUM
**Confidence:** MEDIUM — [Assumes: the Rankine-cycle discharge leg is correctly modeled with condenser at ambient (~40°C), not at the 290°C cold-salt-tank temperature; see Abandoned Reasoning for the rejected alternative model]. GT-4 carries a `?` (not read at source), which per D-07 caps this chain below HIGH; verification that would remove the cap: directly reading a primary CSP power-block performance study (e.g., an NREL SAM technical report) and confirming the ≈40–42% figure at source. The margin between the derived ceiling (≈39–41%) and the claimed 85% is large (>2×), so even a generous ±10-point error on GT-4 would not change the qualitative conclusion — this is why the chain is rated MEDIUM rather than LOW despite the unread citation.

**C2 — Small-scale (5 MWh) penalty compounds the ceiling downward**

```text
GT-5? (small power-block efficiency penalty, ~20–25% at ~1 MWe class) + GT-9 (worse surface/volume ratio at small tank size) + C1 (large-scale ceiling ≈39–41%)
→ a 5 MWh system almost certainly pairs with a sub-5 MWe-class power block (a 5 MWh tank at even a 5-hour duration implies only ~1 MW discharge rating), placing it in the regime where documented thermal-to-electric efficiency falls to ≈20–25% rather than the ≈40–42% large-plant figure
→ combined with proportionally higher standby thermal losses from the worse surface-to-volume ratio (GT-9) and realistic charge-side parasitics (freeze-protection trace heating, pumps) that are a larger fraction of total throughput at small scale
→ a realistic 5 MWh implementation of this pathway would likely realize an electrical round-trip efficiency in roughly the 15–30% range — further below the claimed 85% than even the already-disqualifying large-scale ceiling from C1
```
**Pre-check:** head = GT-5?, GT-9, C1 (MEDIUM) · ?-marked = GT-5? · lowest cited = C1 (MEDIUM) · Inputs ceiling = MEDIUM
**Confidence:** MEDIUM — [Assumes: the 5 MWh system's power rating is in the sub-5 MWe class, which is not stated explicitly in the claim but follows from typical storage durations (2–10 hr) for a tank this size]. GT-5 is `?` (not read at source); verification path: a direct small-CSP/ORC performance study. Caps at MEDIUM per D-07 and because this chain cites C1 (MEDIUM).

**C3 — The equivocation: 85%+ is a legitimate figure only for thermal (heat-in/heat-out), not electrical, round-trip efficiency**

```text
GT-6? (DOE-cited >99% "round-trip storage efficiency" at GWh-class scale) + GT-8? (Rondo's >97% RTE is heat-only; Antora's 85–95% is combined heat+power via thermophotovoltaics, not Rankine/ORC/Brayton)
→ every published figure at or above 85% "round-trip efficiency" for high-temperature thermal storage refers either to pure thermal retention (heat stored vs. heat withdrawn, with the power-block conversion loss accounted separately) or to a fundamentally different reconversion technology than the Rankine/ORC/Brayton pathway the claim specifies
→ the claim's 85%+ figure is achievable only under a silent redefinition of "round-trip efficiency" from electricity-in/electricity-out to heat-in/heat-out — a different, non-interchangeable metric from the one needed to compare against a lithium-ion battery, which stores and returns electricity directly (GT-7?) with no intermediate thermal-to-mechanical-to-electrical conversion step
```
**Pre-check:** head = GT-6?, GT-8? · ?-marked = GT-6?, GT-8? · lowest cited = none · Inputs ceiling = MEDIUM
**Confidence:** MEDIUM — both inputs are `?` (not read at source, turn budget); however the conclusion is corroborated independently by C1's first-principles Carnot derivation (physical law, not citation-dependent), which is why the equivocation finding itself is treated as well-supported in §6 despite the citation gap. Verification path: read-at-source on the DOE/NREL thermal-storage cost report and on Rondo/Antora technical specifications.

**C4 — Cost: the 5 MWh scale forfeits the economies of scale that make large molten-salt storage cheap**

```text
GT-6? (large-scale thermal storage cost ≈$15–40/kWh, achieved only at GWh class with amortized shared power block and favorable surface/volume ratio) + GT-9 (5 MWh tank has ~5–6× worse linear scale, ~120–220× smaller volume) + GT-1? (dedicated small power block, heat exchangers, electric heaters, and salt-freeze-protection systems cannot be shared/amortized at this scale)
→ a 5 MWh tank forfeits essentially all of the economies of scale underlying the $15–40/kWh figure, and must additionally carry a bespoke small turbine/ORC genset and ancillary equipment whose specific cost (per kW and per kWh) rises steeply below utility scale (consistent with GT-5's efficiency penalty, which reflects the same unfavorable small-turbomachinery scaling)
→ realistic specific capital cost for a standalone 5 MWh electric molten-salt system is very unlikely to approach $15–40/kWh, and plausibly runs into the high hundreds to low thousands of $/kWh nameplate — above GT-7's cited Li-ion range of ≈$125–350/kWh
```
**Pre-check:** head = GT-6?, GT-9, GT-1? · ?-marked = GT-6?, GT-1? · lowest cited = none · Inputs ceiling = MEDIUM
**Confidence:** LOW — this is directional, first-principles-grounded reasoning (economies-of-scale/turbomachinery-cost-scaling are well established in engineering economics), but **no published $/kWh figure exists for a 5 MWh electric molten-salt system specifically**, because none is commercially deployed at this scale for electricity reconversion (demonstration/pilot scale only). Two ground-truth inputs are `?` and the magnitude (not just the direction) of the cost gap is asserted without a directly comparable real-world data point. Verification path: a vendor quote or techno-economic study for a 5 MWh-class electric thermal storage system with power-cycle reconversion, which does not appear to exist in public literature at the time of this analysis.

**C5 — Levelized cost of storage: the efficiency penalty compounds the capital-cost disadvantage**

```text
C2 (realistic electrical RTE ≈15–30%) + GT-7? (Li-ion RTE ≈85–92%)
→ for every 1 kWh of electricity eventually delivered from storage, the molten-salt system must purchase roughly 3.3–6.7 kWh of charging electricity (1/RTE), versus ≈1.1–1.2 kWh for Li-ion
→ this charging-energy penalty is a large recurring operating cost (or requires correspondingly oversized charging/generation capacity) layered on top of C4's already-higher capital cost per nameplate kWh
→ on a levelized cost of storage ($/kWh actually delivered, cycled) basis, the molten-salt system is doubly disadvantaged relative to Li-ion at 5 MWh scale: higher capex per nameplate kWh (C4) and a substantially larger ongoing round-trip-efficiency energy penalty
```
**Pre-check:** head = C2 (MEDIUM), GT-7? · ?-marked = GT-7? · lowest cited = C2 (MEDIUM) · Inputs ceiling = MEDIUM
**Confidence:** MEDIUM — the 1/RTE arithmetic itself is a certainty given C2's range: this is deduction, not estimation. The banding is capped at MEDIUM because it cites C2 (MEDIUM) and GT-7 (`?`, not read at source). Verification that would lift this to HIGH: reading C2's and GT-7's underlying sources directly.

**Second-order effects (both lenses walked):**

- *Actor lens:* Project developers and engineers evaluating this technology, on seeing C1–C5, would redirect any 5 MWh-scale "electric thermal storage" proposal toward **heat-only industrial customers** (process steam/heat delivery — where GT-8's >85–97% figures are legitimately marketed, because the Carnot-limited reconversion leg is avoided entirely) rather than grid-electricity arbitrage. Lithium-ion BESS vendors are the direct competitive beneficiary: the economics made explicit here reinforce Li-ion's position for any small-scale (≲10 MWh), electricity-in/electricity-out storage application, likely accelerating the trend already visible in GT-7 (Li-ion cost declines continuing to outpace any plausible cost-down path for small bespoke thermal-power-block systems).
- *Time lens:* Immediately, a developer pricing both options at 5 MWh sees Li-ion winning decisively (C4, C5). Over a few operating cycles/years, the molten-salt system's operating cost would be dominated by the recurring 1/RTE charging-energy penalty (C5) — a cost that scales with utilization and does not disappear with experience. Over a decade or more, Li-ion cell costs continue falling via mass-manufacturing learning curves (GT-7 cites continued projected declines), while a bespoke small thermal power block — not mass-produced — captures little of that learning-curve benefit, so the cost gap plausibly **widens** rather than narrows with time. No second-order effect found here contradicts a Ground Truth.

**End-of-phase Assumption Audit (scan table):**

| Chain | Step | Step Text (brief) | Assumption surfaced? | Added to Table? |
|---|---|---|---|---|
| C1 | 1 | Carnot ceiling + real Rankine ≈40–42% | No (uses GT-2/3/4 directly) | — |
| C1 | 2 | Multiply charge×discharge efficiency | No | — |
| C1 | 3 | 85%+ not plausible at any scale | Yes — condenser modeled at ambient, not at cold-salt-tank temp | Yes — `[Assumes: X]` marked inline above; see Abandoned Reasoning for the rejected alternative |
| C2 | 1 | 5 MWh implies sub-5 MWe power block | Yes — power rating inferred from duration, not stated in claim | Yes — marked inline above |
| C2 | 2 | Worse surface/volume + parasitics | No (uses GT-9 directly) | — |
| C2 | 3 | Realistic RTE 15–30% | No | — |
| C3 | 1 | Published 85%+ figures are thermal or non-Rankine | No | — |
| C3 | 2 | Equivocation identified | No | — |
| C4 | 1 | Forfeits economies of scale | No | — |
| C4 | 2 | Specific capex rises steeply below utility scale | No | — |
| C4 | 3 | Realistic capex > Li-ion range | No | — |
| C5 | 1 | 1/RTE charging multiplier | No | — |
| C5 | 2 | Compounds with C4 | No | — |
| C5 | 3 | Doubly disadvantaged on LCOS | No | — |

Exit criterion check: core question answered (C1–C3 for physics/equivocation, C4–C5 for cost); every conclusion traces to named ground truths via a complete chain with at least one intermediate step; second-order pass applied with both lenses named and no contradiction of a Ground Truth; Assumption Audit run and two surfaced assumptions added to §2 inline.
## 5. Abandoned Reasoning

**What was tried:** Modeling the Carnot ceiling using the two *stated* molten-salt temperatures directly as the heat-engine reservoirs — i.e., T_hot = 565°C (838 K) and T_cold = 290°C (563 K) — since those are the two numbers given in the claim.
**Why abandoned:** This misrepresents the actual physical configuration of a two-tank molten-salt Rankine system. The 290°C cold tank is where the salt returns to *after* giving up heat to the steam generator — it is not the condenser/heat-rejection sink of the power cycle. The actual condenser rejects heat to ambient cooling (water or air, ≈30–50°C), which is a colder, more favorable reservoir for the power cycle than the cold salt tank. Using the two salt temperatures directly would (counter-intuitively) produce a *lower* Carnot ceiling (1−563/838 ≈ 32.8%) than the correct ambient-condenser model (≈61.5%, GT-4). This path was abandoned as a physically incorrect model of the system, not because it supports the claim — in fact it would make the 85% figure look even less plausible — but because using it would mischaracterize *why* the real ceiling is what it is, and would miss the correct identification of where the 40–42% real-world figure (GT-4) comes from.
**What it ruled out:** This confirms (via GT-3, the Carnot physical law) that no reasonable choice of reservoir temperatures drawn from the numbers in the claim itself produces anything close to 85%; it ruled out treating the claim's two stated temperatures as the power-cycle's own thermodynamic reservoir pair.

**What was tried:** Checking whether heat-pump charging (COP > 1, true "Carnot battery" architecture) instead of simple resistive heating could close the gap to 85% electrical round-trip efficiency.
**Why abandoned:** The Carnot-ideal COP for heating from near-ambient to 565°C is only ≈1.54 (838/(838−293)) — a very large temperature lift that fundamentally limits any heat pump's COP, Carnot-ideal or real. Even optimistically assuming a real multi-stage heat pump achieves COP ≈1.2–1.3 (a large fraction of the already-low Carnot-ideal COP, itself optimistic for this ΔT), combining it with the discharge-side efficiency from C1 (≈40%) yields only ≈48–52% round trip — nowhere near 85%, and still far below GT-8's cited 72.5% ceiling for the most advanced published experimental Carnot-battery architecture (which requires a materially different, thermally-integrated design, not present in the claim's plain description).
**What it ruled out (chain C3's rival):** This rules out "an unstated, more sophisticated Carnot-battery charging method is what the claim meant" as a rescue for the 85% figure — it closes roughly half the original gap to 85% at best, not all of it, and GT-8 shows even the best published prototypes of this more sophisticated class fall short of 85%.

**What was tried:** Checking whether Antora Energy's reported 85–95% "combined heat and power" round-trip efficiency figure could be read as supporting the claim at face value.
**Why abandoned:** Antora's reconversion technology is thermophotovoltaic (direct photon-to-electron conversion from a glowing solid block), not a Rankine, ORC, or Brayton cycle — the three technologies the claim explicitly names. It is also an explicitly *combined* heat-and-power figure (i.e., it counts delivered process heat alongside electricity, not electricity alone), which is a different accounting than the claim's "round-trip electricity" framing.
**What it ruled out:** This rules out citing Antora's figure as direct support for the claim; it is evidence for GT-8's broader point (the only ≥85% figures in the literature involve either a different reconversion technology or a different accounting of what counts as "output"), not a counter-example to C1/C3.
## 6. Conclusion

**Recommended approach:** Treat the claim as **failing** for the metric it actually needs (electricity-in/electricity-out round-trip efficiency and cost-competitiveness at 5 MWh scale), and as only being **true under a silent equivocation** — if "round-trip efficiency" is read as heat-in/heat-out thermal retention rather than electrical reconversion, figures above 85% (even >99%) are genuinely documented, but that metric cannot be used to claim cost-competitiveness with a battery that stores and returns electricity directly (chain C3, chain C1).

**Key insight:** The claim packs two separable sub-claims into one sentence and gets both wrong at once: (1) it quotes a thermal-storage-retention efficiency figure as if it were an electrical round-trip efficiency, when the Carnot-bounded discharge leg caps real electrical round-trip efficiency at roughly 39–41% even at best-case large scale (chain C1), and roughly 15–30% at the stated 5 MWh scale (chain C2); and (2) it borrows a cost structure ($15–40/kWh) that is only achievable at 100–1,000× the stated scale, where economies of scale in both the tank and the power block apply — neither of which exists at 5 MWh (chain C4), and the low round-trip efficiency further inflates the true levelized cost of storage relative to lithium-ion (chain C5).

**Trade-offs acknowledged:** Molten-salt thermal storage genuinely has an all-but-unlimited-cycle-life storage medium and, at large (CSP/GWh) scale, legitimately achieves >99% thermal retention efficiency and low $/kWh_thermal cost (chain C3, GT-6) — but only for **heat-only delivery** applications (industrial process steam/heat, as Rondo and Antora's heat-only products target) that never re-enter the Carnot-limited reconversion leg. For electricity-in/electricity-out storage at 5 MWh scale, lithium-ion's combination of 85–92% RTE, $125–350/kWh installed cost, and 4,000–10,000+ cycle life (GT-7) is the stronger offering on every axis examined here.

**Pre-check:** head = C1 (MEDIUM), C2 (MEDIUM), C3 (MEDIUM), C4 (LOW), C5 (MEDIUM) · ?-marked = none additional beyond those named on the cited chains · lowest cited = C4 (LOW) · Inputs ceiling = LOW
**Confidence:** LOW-bounded overall by chain C4 (the cost-magnitude claim), though the core physics/equivocation finding (C1, C3) is independently strong because it rests directly on physical law (GT-2, GT-3) rather than on the `?`-marked citations — the large margin (claimed 85% vs. derived ≈39–41% ceiling, a >2× gap) means this part of the verdict would survive even generous error bars on every `?`-marked empirical input. The cost-magnitude claim (C4) is genuinely weaker: no publicly documented $/kWh figure exists for a 5 MWh electric molten-salt system with power-cycle reconversion, so the "high hundreds to low thousands of $/kWh" estimate is directional engineering-economics reasoning, not a verified figure. What would raise confidence: (a) reading GT-1/GT-4/GT-5/GT-6/GT-7/GT-8 at source rather than via search synthesis, and (b) locating an actual vendor quote or techno-economic study for a 5 MWh-class electric molten-salt storage system, which was not found in this analysis.

**Verdict:** the claim partially holds, but only via equivocation, and fails as a comparison to lithium-ion at the stated scale. Above-85% "round-trip efficiency" is real for molten-salt thermal storage — but only as a heat-retention metric at large scale, never as electricity-in/electricity-out through a Rankine/ORC/Brayton leg at any scale (physically capped near 40% even optimistically, chain C1), and the 5 MWh scale specifically forfeits the economies of scale that make large molten-salt systems' thermal-storage cost figures ($15–40/kWh) look attractive in the first place (chain C4) — making a 5 MWh electric molten-salt system both lower-round-trip-efficiency and (plausibly) higher-cost than a same-capacity lithium-ion system, the opposite of the claim as stated (chain C5).
## Appendix — process output

## §6→§4 closure ledger (process output)

- "Treat the claim as failing for the metric it actually needs... true under a silent equivocation" → chain C3 ✓ (also cites C1 inline)
- "The claim packs two separable sub-claims into one sentence and gets both wrong at once..." → chain C1 ✓ (also cites C2, C4, C5 inline)
- "Molten-salt thermal storage genuinely has an all-but-unlimited-cycle-life storage medium... but only for heat-only delivery applications..." → chain C3 ✓ (also cites GT-6, GT-7 inline)
- "the core physics/equivocation finding (C1, C3) is independently strong because it rests directly on physical law..." → chain C1 ✓ (also cites C3 inline)
- "the claim partially holds, but only via equivocation, and fails as a comparison to lithium-ion at the stated scale..." → chain C1 ✓ (also cites C4, C5 inline)

Scan complete: 5 §6 claims (4 bold lead-ins + 1 bolded verdict paragraph), all 5 cite at least one chain inline — 0 cut.
## Self-audit scan (process output)

**Table 1 — Chain form (section 4)**

| Chain | Chain Head (brief) | Form conforming? | Rule applied | Dependency clean? | Band | Act attempted? | Edges fired |
|---|---|---|---|---|---|---|---|
| C1 | GT-2 + GT-3 + GT-4? | yes | n/a | yes | MEDIUM | yes | none |
| C2 | GT-5? + GT-9 + C1 | yes | n/a | yes | MEDIUM | yes | none |
| C3 | GT-6? + GT-8? | yes | n/a | yes | MEDIUM | no | none |
| C4 | GT-6? + GT-9 + GT-1? | yes | n/a | yes | LOW | yes | none |
| C5 | C2 + GT-7? | yes | n/a | yes | MEDIUM | no | none |

**Table 2 — Claim inventory (section 6)**

| §6 Span (brief) | Construct | Claim under R11? | R11 clause applied | Chain cited |
|---|---|---|---|---|
| Recommended approach: treat claim as failing / true-under-equivocation | bold lead-in | yes | bold lead-in whose colon closes the bold span | C3 |
| Key insight: two sub-claims, both fail | bold lead-in | yes | bold lead-in whose colon closes the bold span | C1 |
| Trade-offs acknowledged: molten salt wins only for heat-only delivery | bold lead-in | yes | bold lead-in whose colon closes the bold span | C3 |
| Pre-check: head=C1,C2,C3,C4,C5; ?-marked; lowest cited; Inputs ceiling | bold lead-in | no | mechanical confidence pre-registration field, not an assertion about the subject matter — excluded by analogy to the content-inside-a-fenced-block exclusion (structural bookkeeping, not a claim about molten salt/Li-ion) | n/a |
| Confidence: LOW-bounded by C4, physics finding independently strong | bold lead-in | yes | bold lead-in whose colon closes the bold span | C4 (also cites C1, C3) |
| Verdict: partially holds via equivocation, fails vs. Li-ion at 5 MWh | bold lead-in | yes | bold lead-in whose colon closes the bold span | C1 (also cites C4, C5) |

Scan complete: 5 chain rows, one per section-4 chain block in order; 6 section-6 rows, one per construct in order — 5 claims under R11, 1 excluded. 0 chains malformed, 0 claims untraced.
## Adversarial pass (process output)

**Recompute.** (1) Carnot ceiling, 540°C/40°C: η = 1 − 313.15/813.15 = 0.6150 → 61.5% (matches GT-4/C1). (2) Large-scale electric RTE: 0.97 × 0.41 = 0.398 ≈ 40% (within the stated 39–41% band). (3) Carnot-ideal heat-pump COP, ambient→565°C: 838.15/(838.15−293.15) = 1.538 (matches the 1.54 cited in §5 Abandoned Reasoning). (4) Optimistic heat-pump-assisted round trip: 1.25 × 0.405 ≈ 0.506 (within the stated 48–52% band). (5) 1/RTE charging multiplier at RTE 15%/30%: 1/0.15 = 6.67, 1/0.30 = 3.33 (matches the stated 3.3–6.7× band in C5). (6) Volume ratio 5 MWh vs. 600–1,100 MWh_th: 120×–220×; linear (cube-root) ratio ≈ 4.9×–6.0× (matches the "~5–6×" stated in GT-9/C4). All six recomputed figures land where the document states them — no arithmetic error found.

**Sensitivity.** The single most sensitive input is the *interpretation* of "round-trip efficiency" underlying chain C3 (i.e., GT-6?/GT-8?, both `?`-marked): if the claim's intended scope is heat-in/heat-out thermal retention rather than electricity-in/electricity-out, the 85%+ figure is independently well-documented (>99% at large scale), which would re-cast the verdict from "fails" to "true but about a different, non-electrical metric" — which is in fact already how §6 frames it (the claim "partially holds... via equivocation"). Because this sensitivity is already incorporated into the stated verdict rather than contradicting it, it does not change the conclusion; it is the conclusion's main qualifier. GT-6 and GT-8 remain unverified (`?`); verifying them at source would raise chain C3 from MEDIUM toward HIGH without changing its direction. Per-chain weakest link: C1 → GT-4? (not read at source, but protected by a >2× margin); C2 → the inferred sub-5-MWe power-block rating `[Assumes: X]` (not stated by the claim); C3 → GT-8? (Rondo/Antora figures not read at source); C4 → the complete absence of any published $/kWh figure for a 5 MWh electric molten-salt system (no citation exists to read, at any scale); C5 → GT-7? (Li-ion figures not read at source, though the 1/RTE arithmetic itself is certain).

**Rival.** Headline conclusion: the strongest rival is "a sufficiently advanced thermally-integrated Carnot-battery architecture (heat-pump charge + ORC discharge with waste-heat recovery, per GT-8's Dumont et al. prototype) could, with further R&D, approach or exceed 85% round-trip electrical efficiency." This rival is addressed in §5 Abandoned Reasoning: the best published experimental result for this more sophisticated architecture class is 72.5%, still below 85%, and it is a materially different design from the plain resistive-heating + Rankine/ORC/Brayton pathway the claim specifies — ruled out for the claim *as stated*, but left live as an open question for the broader technology class (named on C1's confidence treatment above). Chain C3: rival — "the 85% figure is simply an approximation/typo for ~40%, not a deliberate reference to thermal efficiency" — a claim-about-authorial-intent rival that cannot be fully ruled out from the claim text alone; it does not change the physics finding either way, so it is noted but not adjudicated. Chain C2: rival — "a small-scale ORC specifically optimized for low-grade heat recovery narrows the small-scale efficiency penalty" — real but minor; even generously applied it does not close the gap to 85%, so it does not overturn C2. Chain C4: rival — "a mass-manufactured, modular small thermal-storage product (in the direction Rondo's commercial product line is heading) could defy the one-off/no-economies-of-scale assumption" — a live, unresolved rival, which is precisely why C4 is rated LOW rather than MEDIUM (see Disposition, Cluster C, below). Chain C5: `rival not applicable — the 1/RTE relationship is arithmetic, not an empirical claim open to a competing interpretation`.

**Premise.** The headline conclusion — "the claim fails for electricity-in/electricity-out round-trip efficiency and cost-competitiveness at 5 MWh scale, and holds only via a thermal/electrical equivocation" — is already false.

**Causes** (generated from four stakeholder viewpoints, unfiltered):
- *CSP/thermal-storage engineer:* (1) the claim may have intended a supercritical-CO₂ Brayton cycle rather than steam Rankine, which reaches somewhat higher thermal efficiencies at these temperatures; (2) the claim may have intended a thermally-integrated Carnot-battery architecture (heat pump + ORC with waste-heat recovery), not plain resistive heating; (3) turbine-inlet temperature could be modeled with more superheat than assumed, raising the Carnot ceiling.
- *Skeptical physicist/reviewer:* (4) the condenser/heat-rejection temperature assumption (40°C ambient) could be wrong for a specific cold-climate siting, raising the real Carnot ceiling materially; (5) the GT-4 40–42% empirical anchor could be outdated relative to the newest advanced steam-cycle designs.
- *Battery-storage competitor/financier:* (6) utility-scale Li-ion figures (GT-7) may understate real BOS/EPC/inverter overhead at 5 MWh, narrowing the capex gap versus what C4 assumes; (7) Li-ion calendar/cycle degradation over a 20–30 year horizon may erode its advantage more than modeled, especially against a storage medium (molten salt) that does not chemically degrade.
- *Thermal-storage vendor:* (8) a modular, factory-built small thermal-battery product (the direction Rondo's commercial line is heading) could defy the "no economies of scale below GWh class" assumption underlying C4, achieving materially lower $/kWh than assumed.

**Clusters:**
- *Cluster A — advanced/alternative architecture could close the efficiency gap further than modeled* (causes 1, 2, 3, 4, 5; bears on C1, C2, GT-4, GT-8).
- *Cluster B — Li-ion's own small-scale and degradation penalties may be undercounted, narrowing the relative cost gap* (causes 6, 7; bears on C4, C5, GT-7).
- *Cluster C — a modular/mass-manufactured small thermal-storage product could defy the no-economies-of-scale assumption* (cause 8; bears on C4, GT-6).

**Disposition:**
- *Cluster A — accepted risk, mitigation named:* even granting every cause in this cluster, the best documented result for the most favorable named alternative (GT-8's 72.5% thermally-integrated Carnot battery) still falls short of 85%, and the margin between the claimed 85% and this analysis's derived ceiling (≈39–41%, or up to ≈50–52% with optimistic heat-pump assistance) is large enough that this cluster is very unlikely to flip the qualitative verdict. Mitigation: the confidence caveats already attached to C1/C2 (naming GT-4?/GT-5? and the verification path that would remove the cap) stand as the accepted-risk treatment; no change to the stated conclusion.
- *Cluster B — plan change:* §6's Trade-offs-acknowledged and chain C5 are revised in effect (already written at MEDIUM, not HIGH, confidence) to explicitly avoid asserting a precise LCOS gap magnitude — the directional conclusion (molten salt is doubly disadvantaged) is retained, but the magnitude claim is flagged as sensitive to updated Li-ion BOS/degradation figures not read at source (GT-7?).
- *Cluster C — accepted risk, mitigation named:* this is the specific reason chain C4 is rated LOW rather than MEDIUM — the confidence line explicitly states "no published $/kWh figure exists for a 5 MWh electric molten-salt system... because none is commercially deployed at this scale," which is the mitigation: the cost-magnitude claim is presented as directional engineering-economics reasoning, not a verified figure, precisely to avoid overstating certainty against this live rival.

**Falsification.** The conclusion is false if a commercially operating (or credibly engineered and published) 5 MWh-class molten-salt thermal storage system — charged via resistive heating (or heat pump) and discharged via a Rankine, ORC, or Brayton power cycle between approximately 290°C and 565°C — is demonstrated with a verified electricity-in/electricity-out round-trip efficiency ≥85%, AND an installed system cost at or below the contemporaneous utility-scale lithium-ion $/kWh range for the same nameplate capacity.
## Assumption Audit scan (process output copy)

| Chain | Step | Step Text (brief) | Assumption surfaced? | Added to Table? |
|---|---|---|---|---|
| C1 | 1 | Carnot ceiling + real Rankine ≈40–42% | No (uses GT-2/3/4 directly) | — |
| C1 | 2 | Multiply charge×discharge efficiency | No | — |
| C1 | 3 | 85%+ not plausible at any scale | Yes — condenser modeled at ambient, not at cold-salt-tank temp | Yes — added to §2 table |
| C2 | 1 | 5 MWh implies sub-5 MWe power block | Yes — power rating inferred from duration, not stated in claim | Yes — added to §2 table |
| C2 | 2 | Worse surface/volume + parasitics | No (uses GT-9 directly) | — |
| C2 | 3 | Realistic RTE 15–30% | No | — |
| C3 | 1 | Published 85%+ figures are thermal or non-Rankine | No | — |
| C3 | 2 | Equivocation identified | No | — |
| C4 | 1 | Forfeits economies of scale | No | — |
| C4 | 2 | Specific capex rises steeply below utility scale | No | — |
| C4 | 3 | Realistic capex > Li-ion range | No | — |
| C5 | 1 | 1/RTE charging multiplier | No | — |
| C5 | 2 | Compounds with C4 | No | — |
| C5 | 3 | Doubly disadvantaged on LCOS | No | — |

(This is the same scan reproduced from §4 of the working document, placed here per the prescribed process-output location; the inline `[Assumes: X]` marks and the §2 Classified Assumptions Table rows are the governing artifact.)

## Techniques not applied (process output)

- pre-mortem — not applicable — the analysis's conclusion is a verdict on a factual/physical claim, not a plan or recommendation to execute; the decision rule (inversion stress-tests a claim, pre-mortem stress-tests a plan) routes Phase 5's adversarial technique to inversion instead, which was applied.
- theoretical-limit (Phase 1 essence-reframe invocation) — not applicable — the Essence Statement already explicitly frames the core question as "is 85%+ physically plausible," i.e., already asks what the fundamentals permit rather than treating a conventional figure as fixed; no further reframe was needed. (The Phase 4 invocation of theoretical-limit fired and was applied — see chain C1/GT-4's Carnot-ceiling-vs-real-performance bracket.)
- inversion (Phase 2 challenge-assumptions invocation) — not applicable — the assumption space was directly enumerable from the claim's own named sub-components (temperature range, charging mechanism, discharge cycle, efficiency figure, cost comparison) without needing a separate failure-enumeration brainstorm to surface hidden assumptions. (The Phase 5 invocation of inversion fired and was applied — see the Adversarial pass record above.)
- fishbone — not applicable — the assumption space was single-threaded and directly traceable to the claim's explicit sub-components (a compound claim with ~5 named parts), not a multi-causal space requiring breadth-first category brainstorming.
- five-whys (causal mode) — not applicable — there is no recurring observed symptom to diagnose causally; reduce-to-primitives mode was used instead (informally, within Phase 3) to bottom GT-2/GT-3/GT-9 out at physical law and geometry.
- trade-off — not applicable — the question is a claim verification (holds/partially holds/fails), not a choice between two or more viable surviving options requiring a weighted-criteria matrix.
## Self-Audit Gate (process output)

**Criterion 1: Identify Essence**
Quoted span: "Can a 5 MWh two-tank molten-salt thermal energy storage system — charged electricity→heat (e.g. resistive heating) and discharged heat→electricity via a thermodynamic power cycle (Rankine/ORC/Brayton), operating between a 290°C cold tank and a 565°C hot tank — achieve an electricity-in/electricity-out round-trip efficiency above 85%, and is such a system cost-competitive with a same-nameplate-capacity lithium-ion battery system?"
Band: **Rigorous**
Justification: The statement names the core question specifically (temperatures, scale, pathway, comparator all named — it could not be pasted unmodified into an analysis of a different problem), and each success criterion beneath it is a checkable verb+subject+outcome triplet scoreable directly against §6 (e.g., "determine whether 85%+ electrical round-trip efficiency is physically achievable... with a Carnot-grounded derivation" is checked against chain C1's presence in §6).

**Criterion 2: Challenge Assumptions**
Quoted span: "| Molten salt's \"unlimited cycle life\" fully offsets higher capex | convention | Explicitly challenge | **Partially fails** — the storage *medium* has very long life, but the power-block... | Reported-by-delegate; see GT-7? |"
Band: **Sound**
Justification: The table is populated with non-generic, specific entries, uses the four-type scheme correctly throughout, and challenges multiple assumptions rather than merely labelling them Accept — but the Verdict cells (e.g., "Holds", "Partially fails", "Fails") do not use the prescribed leading-token vocabulary (`Accept —` / `Challenge —` / `Discard —`) specified by the rubric, which is an identifiable, consistent formatting deviation from the Rigorous descriptor rather than an isolated lapse, and the exact phrase "unverified — flagged" (prescribed for chain-consumed unverified assumptions) does not appear verbatim anywhere in the table.

**Criterion 3: Establish Ground Truths**
Quoted span: "`?`-marked ground truths: GT-1, GT-4, GT-5, GT-6, GT-7, GT-8 (6 of 9)."
Band: **Rigorous**
Justification: Checking this enumeration against the Ground Truths list itself (not merely quoting it): GT-1, GT-4, GT-5, GT-6, GT-7, GT-8 are the only entries carrying the `?` suffix in the list, and GT-2, GT-3, GT-9 (the remaining three of nine) carry none — the enumeration matches the list exactly; every unsuffixed GT (GT-2, GT-3, GT-9) is a physical-law or geometric derivation requiring no external citation, so the "unsuffixed GT feeding a HIGH-confidence chain names read-at-source location" requirement is vacuously satisfied (no chain in this analysis is rated HIGH); each `?`-marked GT carries either an explicit Phase 3 failure record (GT-1, GT-4, GT-5) or an explicit "not read — turn budget" disclosure (GT-6, GT-7, GT-8), satisfying the exit criterion's disclosure requirement rather than silently omitting the gap.

**Criterion 4: Reason Upward**
Quoted span: "| C1 | GT-2 + GT-3 + GT-4? | yes | n/a | yes | MEDIUM | yes | none |" (and the corresponding rows for C2–C5, all `Form conforming? = yes`, `Dependency clean? = yes`) — self-audit scan, Table 1.
Band: **Rigorous**
Justification: Every section-4 chain scans as form-conforming and dependency-clean per the self-audit scan; each of the five conclusions has exactly one chain with a genuine intermediate step; both surfaced assumptions are declared inline with `[Assumes: X]`; the Abandoned Reasoning section documents three dead ends using the prescribed What-was-tried/Why-abandoned/What-it-ruled-out structure with analysis-specific (not generic) reasons; no analogy (CSP plants, Rondo, Antora) is used as direct evidence without being grounded in a named GT about that specific situation (GT-6, GT-8).

**Criterion 5: Validate**
Quoted span: "This is directional, first-principles-grounded reasoning..., but no published $/kWh figure exists for a 5 MWh electric molten-salt system specifically... Two ground-truth inputs are `?` and the magnitude... is asserted without a directly comparable real-world data point." (chain C4's confidence line)
Band: **Sound**
Justification: Confidence ratings are present on every chain and the Conclusion, correctly capped below HIGH wherever a `?`-marked input or a cited MEDIUM/LOW chain is consumed (verified: no chain is rated above the lowest chain its head cites, no chain with a `?` input is rated HIGH), and the adversarial pass record is complete with every part (Recompute, Sensitivity, Rival, Premise, Causes, Clusters-with-dispositions, Falsification) present — but chain C4's confidence line names its downgrade cause as "two ground-truth inputs are `?`" generically rather than spelling out GT-6? and GT-1? by ID within that sentence itself (the IDs appear only in the head line above), an isolated, identifiable shortfall in one chain rather than a pattern across the analysis.

**Criterion 6: Conclusion-to-Ground-Truth Traceability**
Quoted span: "Scan complete: 5 chain rows... 6 section-6 rows... 5 claims under R11, 1 excluded. 0 chains malformed, 0 claims untraced." (self-audit scan, Table 2 reconciliation line)
Band: **Rigorous**
Justification: All five Conclusion-section claims trace to a named section-4 chain (0 untraced per the scan), no claim introduces reasoning absent from section 4, and the Key Insight ("the claim packs two separable sub-claims... and gets both wrong at once: [thermal/electrical equivocation] and [scale-arbitrage on cost]") is a non-obvious analytical finding distinct from the Recommended-approach line's verdict framing, not a restatement of it.

**Pass 1 (before re-score):** n/a — this is the first and only scoring pass; no re-score was triggered.

**Gate result:** cleared · passes: 1 · Fix/Repeat fired: no

Gate conditions check: (1) Gate cleared — no criterion scored Absent (lowest band reached was Sound, on Criteria 2 and 5). (2) Hand-wavy cap cleared — zero criteria scored Hand-wavy, well within the "at most one" allowance. Both conditions hold on the first pass; no Fix/Repeat loop was required.
## Structured summary (process output)

```json
{
  "schema_version": 1,
  "run_mode": "full-composer",
  "assumptions": [
    {"id": "A-1", "type": "current constraint", "verdict": "Accept"},
    {"id": "A-2", "type": "physical law", "verdict": "Accept"},
    {"id": "A-3", "type": "physical law", "verdict": "Accept"},
    {"id": "A-4", "type": "convention", "verdict": "Discard"},
    {"id": "A-5", "type": "current constraint", "verdict": "Accept"},
    {"id": "A-6", "type": "current constraint", "verdict": "Accept"},
    {"id": "A-7", "type": "untested belief", "verdict": "Accept"},
    {"id": "A-8", "type": "current constraint", "verdict": "Accept"},
    {"id": "A-9", "type": "untested belief", "verdict": "Accept"},
    {"id": "A-10", "type": "convention", "verdict": "Discard"},
    {"id": "A-11", "type": "convention", "verdict": "Challenge"},
    {"id": "A-12", "type": "untested belief", "verdict": "Discard"},
    {"id": "A-13", "type": "physical law", "verdict": "Accept"},
    {"id": "A-14", "type": "current constraint", "verdict": "Accept"},
    {"id": "A-15", "type": "untested belief", "verdict": "Challenge"}
  ],
  "ground_truths": [
    {"id": "GT-1", "read_at_source": false},
    {"id": "GT-2", "read_at_source": true},
    {"id": "GT-3", "read_at_source": true},
    {"id": "GT-4", "read_at_source": false},
    {"id": "GT-5", "read_at_source": false},
    {"id": "GT-6", "read_at_source": false},
    {"id": "GT-7", "read_at_source": false},
    {"id": "GT-8", "read_at_source": false},
    {"id": "GT-9", "read_at_source": true}
  ],
  "chains": [
    {"id": "C1", "confidence": "MEDIUM", "rests_on": ["GT-2", "GT-3", "GT-4?"]},
    {"id": "C2", "confidence": "MEDIUM", "rests_on": ["GT-5?", "GT-9", "C1"]},
    {"id": "C3", "confidence": "MEDIUM", "rests_on": ["GT-6?", "GT-8?"]},
    {"id": "C4", "confidence": "LOW", "rests_on": ["GT-6?", "GT-9", "GT-1?"]},
    {"id": "C5", "confidence": "MEDIUM", "rests_on": ["C2", "GT-7?"]}
  ],
  "dead_ends": [
    "Modeling the Carnot ceiling using the two stated salt temperatures directly as power-cycle reservoirs",
    "Heat-pump (Carnot-battery) charging closing the gap to 85%",
    "Citing Antora's combined heat-and-power figure as direct support for the claim"
  ],
  "techniques": {
    "applied": ["theoretical-limit", "estimate", "second-order", "inversion"],
    "not_applied": [
      {"technique": "theoretical-limit", "phase": 1, "reason": "the Essence Statement already explicitly frames the core question as \"is 85%+ physically plausible,\" i.e., already asks what the fundamentals permit rather than treating a conventional figure as fixed; no further reframe was needed"},
      {"technique": "inversion", "phase": 2, "reason": "the assumption space was directly enumerable from the claim's own named sub-components without needing a separate failure-enumeration brainstorm to surface hidden assumptions"},
      {"technique": "fishbone", "phase": 2, "reason": "the assumption space was single-threaded and directly traceable to the claim's explicit sub-components, not a multi-causal space requiring breadth-first category brainstorming"},
      {"technique": "five-whys", "phase": 3, "reason": "there is no recurring observed symptom to diagnose causally; reduce-to-primitives mode was used instead (informally) to bottom GT-2/GT-3/GT-9 out at physical law and geometry"},
      {"technique": "trade-off", "phase": 4, "reason": "the question is a claim verification (holds/partially holds/fails), not a choice between two or more viable surviving options requiring a weighted-criteria matrix"},
      {"technique": "pre-mortem", "phase": 5, "reason": "the analysis's conclusion is a verdict on a factual/physical claim, not a plan or recommendation to execute; the decision rule routes Phase 5's adversarial technique to inversion instead, which was applied"}
    ]
  },
  "gate": {
    "passes": [
      {
        "bands": ["Rigorous", "Sound", "Rigorous", "Rigorous", "Sound", "Rigorous"],
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
    "recommendation": "Treat the claim as failing for the metric it actually needs (electricity-in/electricity-out round-trip efficiency and cost-competitiveness at 5 MWh scale), and as only being true under a silent equivocation — if \"round-trip efficiency\" is read as heat-in/heat-out thermal retention rather than electrical reconversion, figures above 85% (even >99%) are genuinely documented, but that metric cannot be used to claim cost-competitiveness with a battery that stores and returns electricity directly (chain C3, chain C1).",
    "confidence": "LOW",
    "rests_on": ["C1", "C2", "C3", "C4", "C5"]
  }
}
```
