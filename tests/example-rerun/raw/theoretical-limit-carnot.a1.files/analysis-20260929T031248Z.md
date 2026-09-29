# First-Principles Analysis: Thermal-to-Electric Efficiency Ceiling of a 565°C Molten-Salt Rankine Power Block

Mode: full-composer (no single-technique trigger fired; the prompt explicitly requests the full methodology).

## 1. Problem Essence

**Essence Statement:** What is the maximum thermal-to-electric conversion efficiency physically permitted for a steam Rankine power block that receives heat from a fixed 565°C molten-salt hot reservoir and rejects heat to ambient, and — quantitatively — how much of the gap between that law-permitted ceiling and today's real-world efficiency is closeable by engineering versus fixed by physics?

**Success criteria (a correct answer must):**
1. Derive the ceiling from the *actual* reservoir temperatures (Carnot), not assume a memorized percentage.
2. Apply Curzon–Ahlborn, but test — not assume — its applicability as "the" finite-power ceiling for this specific engine architecture (a regenerative, reheat-capable steam Rankine cycle), per the theoretical-limit procedure's caution that a model-dependent bound is not automatically a ceiling.
3. Ground current-practice efficiency in cited data, not folklore.
4. Decompose the gap into named, numerically bracketed buckets: structurally/physically irreducible vs. engineering-recoverable vs. economically-stuck-but-theoretically-recoverable.
5. Surface second-order consequences (materials cost, cooling-method tradeoffs, competing cycle architectures) of trying to close the gap.
6. Deliver this as an auditable derivation chain with confidence ratings, not a narrative claim.

## 2. Assumptions Table

| Assumption | Type | Treatment | Verdict | Verification |
|---|---|---|---|---|
| The Second Law of Thermodynamics bounds any heat engine's efficiency by the Carnot efficiency between its actual hot and cold reservoir temperatures. (A1) | physical law | Accept as ground-truth candidate. | Accept — direct consequence of the Kelvin–Planck/Clausius statements; promoted to GT1 | Derived directly in chain C1; classical thermodynamics (Carnot's theorem, 1824) |
| Solar salt (60/40 NaNO₃/KNO₃) hot tank operates at ~565°C; cold tank at ~285–290°C, in commercial molten-salt power towers. (A2) | current constraint | Record expiry conditions. | Accept — expires if higher-temperature salts/particle receivers (R&D targets 600–650°C) reach commercial deployment; until then this is a materials/chemistry limit, not a physical one | unverified — flagged (GT2?; convergent WebSearch summaries, no primary document opened; one direct-fetch attempt returned 404) |
| Commercial molten-salt turbines run subcritical, main/turbine-inlet steam ~540°C at ~120–125 bar; salt-to-steam pinch optimized ~2.5–3°C; total approach loss ~20–25°C. (A3) | current constraint | Record expiry conditions. | Accept — expires as higher-temperature-rated turbine metallurgy becomes commercially standard; until then this is a design/economic optimum | unverified — flagged (GT3?; WebSearch synthesis of steam-generator design-optimization literature, not opened at primary source) |
| Condenser/heat-rejection temperature is set by ambient + cooling-technology approach: ~35–45°C wet cooling, ~45–65°C dry/ACC in desert climates. (A4) | current constraint | Record expiry conditions. | Accept — expires with siting/technology choice, not a physical limit | unverified — flagged (GT5?; general power-plant engineering knowledge, no specific document opened) |
| The Curzon–Ahlborn efficiency η=1−√(Tc/Th) is *the* correct law-permitted ceiling for a finite-power real Rankine engine. (A5) | convention | Explicitly challenge before use. | Discard — contradicted by GT6 (real plants exceed the naive CA figure) and by GT10's own model-dependence statement; not load-bearing for any conclusion | see chain C2 and §5 item 2 |
| A steam Rankine cycle receives heat non-isothermally (economizer + evaporation + superheat spanning ~290°C→540°C), not isothermally at the peak salt temperature. (A6) | physical law | Accept as ground-truth candidate. | Accept — structural property of the Rankine cycle's own T–s diagram; promoted to GT8 | Derived directly in chain C3 |
| Current best-demonstrated subcritical molten-salt steam cycles achieve ~41–43% gross thermal-to-electric efficiency at 565°C hot salt. (A7) | untested belief | Verify, or flag unverified. | Challenge — WebSearch-sourced figure from an OSTI report; the PDF itself could not be read in this run | unverified — flagged (GT6?; Phase 3 failure record: OSTI PDF returned unreadable binary content) |
| Net (busbar) plant efficiency runs ~3–6 percentage points below gross cycle efficiency after parasitic loads. (A8) | untested belief | Verify, or flag unverified. | Challenge — engineering-judgment estimate, no specific plant parasitic-load table opened | unverified — flagged (GT7?) |
| The mean thermodynamic temperature of heat addition (T̄_add) for this cycle is materially below peak temperature, plausibly ~690–730 K. (A9) | untested belief | Verify, or flag unverified; compute with explicit bracket. | Challenge — this analysis's own Fermi estimate via enthalpy-weighting, not independently verified against a real plant heat-and-mass balance | unverified — flagged (computed as an intermediate claim inside chain C3, not promoted to a standalone GT) |
| Component-level exergy destruction (heat exchanger ≳ turbine > condenser > pumps/BOP) follows the pattern reported in general solar-thermal Rankine exergy-analysis literature. (A10) | untested belief | Verify, or flag unverified. | Discard as a cited input — candidate source (ScienceDirect) returned HTTP 403 and could not be confirmed; not used as a ground truth or in any numeric chain | see §5 item 4 |
| An internally-reversible regenerative Rankine cycle converges toward η=1−Tc/T̄_add as feedwater-heating stages → ∞ (standard engineering-thermodynamics identity). (A11) | physical law | Accept as ground-truth candidate. | Accept — standard regenerative-Rankine limiting theorem (e.g. Cengel & Boles); promoted to GT9 | Derived directly in chain C3 |
| Raising turbine-inlet temperature toward 565°C, adopting supercritical steam, and adding reheat/regeneration stages are engineering levers with cost/materials tradeoffs that impose a separate economic (not physical) floor on gap closure. (A12) | convention | Explicitly challenge before use. | Accept — challenged and retained: cost/materials tradeoffs are real and industry-documented (turbine OEM alloy costs), but the specific 2–5 point near-term / 7–10 point stuck split is this analysis's own estimate | unverified — flagged (drives the Segment-2 split in chain C4; `[Assumes: ...]` on that chain's head) |
| Curzon–Ahlborn describes efficiency at maximum power for one specific idealized symmetric endoreversible two-reservoir model — not a universal ceiling for any finite-power heat engine. (A13) | physical law | Accept as ground-truth candidate. | Accept — property of the CA derivation itself, corroborated by finite-time-thermodynamics survey literature; promoted to GT10 | unverified — flagged (GT10?; confirmed via WebSearch synthesis of arXiv:1903.04381 and related literature, not opened and read directly) |
| Some national-lab/industry effort is being diverted toward sCO2 Brayton topping cycles specifically because of Segment 1's structural ceiling, rather than the two efforts being independent. (A14 — surfaced during the end-of-Phase-4 Assumption Audit on chain C5, step 3) | untested belief | Verify, or flag unverified. | Challenge — plausible but not confirmed; load-bearing only for chain C5's qualitative actor-lens framing, not for any numeric figure in chain C4 | unverified — flagged (`[Assumes: ...]` on chain C5) |

**Stakes-escalation note:** A1, A6, and A11 (the three physical-law/definitional assumptions carrying the headline numeric ceilings) are pushed to ground-truth status via direct derivation rather than citation, which is the strongest verification available for an analytic identity. A7 and A8 (the two empirical current-practice figures the Conclusion's Segment-2/Segment-3 split depends on most heavily) remain unverified despite two direct-fetch attempts each failing (OSTI PDF unreadable; no specific plant parasitic table opened) — this is the single largest driver of the Conclusion's overall LOW confidence rating and is stated as such in §6.


## 3. Ground Truths

Irreducibility note: GT1, GT8, and GT9 are analytic/definitional identities in classical and engineering thermodynamics. Their irreducibility test (5-Whys, reduce-to-primitives mode) was applied directly: each reduces to the Kelvin–Planck/Clausius statement of the Second Law (an axiom, not further reducible) or to the algebraic definition of the Rankine cycle's own T–s diagram (a mathematical construction, not further reducible). These are treated as **read-at-source via direct derivation shown in Section 4**, rather than via an external document, because the derivation itself is the verification.

1. **GT1** (physical law, read-at-source — derived in C1): No heat engine operating between reservoirs at T_h and T_c can exceed Carnot efficiency η = 1 − T_c/T_h. Source: Second Law of Thermodynamics (Kelvin–Planck/Clausius statements; Carnot's theorem, 1824). Read-location: derivation shown in chain C1.
2. **GT2?** (reported-by-delegate): Solar-salt hot tank ≈565°C (838 K); cold tank ≈285–290°C. Source: convergent WebSearch summaries (Scientific American, IEEE Spectrum, SolarPACES/ResearchGate Noor III materials, Masen). Not opened at a single primary document in this run; one direct-fetch attempt (DOE power-tower basics page) returned 404. Phase 3 failure record: DOE URL `energy.gov/eere/solar/articles/power-tower-system-...` → 404 Not Found.
3. **GT3?** (reported-by-delegate): Turbine-inlet steam ≈540°C, ≈120–125 bar (subcritical); steam-generator pinch optimum ≈2.5–3°C; total salt→steam approach loss ≈20–25°C. Source: WebSearch synthesis of steam-generator design-optimization literature (ScienceDirect abstracts). Not opened at primary source.
4. **GT4** (read-at-source): Noor III (Morocco) — 150 MW gross CSP tower, molten-salt storage (7 h), **dry-cooled** ("uses a dry cooling system to decrease water use"). Read-location: Wikipedia, "Ouarzazate Solar Power Station" article, fetched and quoted directly in this session.
5. **GT5?** (unverified): Representative condenser temperatures: ≈35–45°C (wet cooling), ≈45–65°C (dry/ACC, hot-climate). Source: general power-plant engineering knowledge; not tied to a specific opened document in this run.
6. **GT6?** (reported-by-delegate): Best-demonstrated gross (turbine-generator) thermal-to-electric efficiency for subcritical molten-salt Rankine cycles at 565°C hot salt ≈43.0% (wet cooling), ≈41.2% (air-cooled condenser). Source: OSTI technical report "Incorporating Supercritical Steam Turbines into Advanced CSP Plants" (osti.gov/servlets/purl/1088078), figure obtained via WebSearch-generated summary. Phase 3 failure record: direct WebFetch of the PDF returned corrupted/unparseable binary content — the exact sentence was **not** confirmed at source in this run.
7. **GT7?** (unverified): Representative current net (busbar) efficiency ≈ gross − (3–6 points) ≈36–40%. Source: this analysis's engineering-judgment estimate of typical parasitic-load deduction (salt/feed pumps, cooling fans, freeze-protection trace heating, BOP); no specific plant's parasitic-load table was opened in this run.
8. **GT8** (physical law/definition, read-at-source — derived in C3): A Rankine cycle's heat addition is non-isothermal: it spans feedwater temperature (~285–290°C) through evaporation (isothermal at the boiling point for the operating pressure) to turbine-inlet temperature (~540°C) — not isothermal at the peak 565°C source temperature. Read-location: derived directly from the Rankine cycle's own T–s diagram definition, shown in chain C3.
9. **GT9** (physical law/definition, read-at-source — derived in C3): An internally-reversible regenerative Rankine cycle's efficiency converges to η = 1 − T_c/T̄_add (Carnot evaluated at the cycle's own mean thermodynamic temperature of heat addition) as the number of feedwater-heating stages → ∞. Standard result in engineering thermodynamics (regenerative Rankine cycle theory, e.g. Cengel & Boles). Read-location: derived directly, shown in chain C3.
10. **GT10?** (reported-by-delegate): The Curzon–Ahlborn efficiency at maximum power, η_CA = 1−√(T_c/T_h), is derived for one specific idealized "endoreversible" engine — internally reversible, with all irreversibility confined to finite-rate linear heat exchange at two isothermal reservoirs of symmetric conductance, optimized for maximum *power* (not efficiency). It is not a universal ceiling for any finite-power heat engine and does not by itself constrain a multi-temperature-level regenerative Rankine cycle. Source: WebSearch synthesis of the finite-time-thermodynamics literature (e.g., "The many avatars of Curzon-Ahlborn efficiency," arXiv:1903.04381) describing this model-dependence; the arXiv paper itself was not opened and read line-by-line in this run.

**`?`-marked ground truths:** GT2, GT3, GT5, GT6, GT7, GT10 (6 of 10).
**Unsuffixed (read-at-source) ground truths, with read-location:** GT1 (derived in C1), GT4 (Wikipedia, fetched directly), GT8 (derived in C3), GT9 (derived in C3).

No assumption discarded in Phase 2 (A5, A10) appears in this list — A5 (naive CA-as-ceiling) is rejected and lives in §5 Abandoned Reasoning item 2; A10 (cited exergy-breakdown percentages) is abandoned in §5 item 4 rather than promoted to a ground truth.

## 4. Derivation Chains

### C1 — Absolute (Carnot) ceiling [theoretical-limit: governing law = Second Law of Thermodynamics]

```text
GT1 (Carnot bound) + GT2? (salt hot/cold temps) + GT5? (condenser temps)
→ per GT2, the hot reservoir is the salt tank at Th = 565°C = 838.15 K
→ per GT5, the cold reservoir is the condenser at Tc = 313.15 K (40°C, wet cooling) or 328.15 K (55°C, dry/ACC)
→ per GT1, η_Carnot = 1 − Tc/Th
→ for wet cooling: η_Carnot = 1 − 313.15/838.15 = 0.626
→ for dry cooling: η_Carnot = 1 − 328.15/838.15 = 0.608
→ this 60.8–62.6% band is the absolute, reversible, zero-net-power ceiling for any heat engine bridging these two reservoirs
→ it is a direct algebraic consequence of the Second Law and is not specific to Rankine cycles at all
```
**Pre-check:** head = GT1 (HIGH) · GT2? (?) · GT5? (?) · ?-marked: GT2, GT5 · lowest cited: none · Inputs ceiling: MEDIUM
**Confidence:** MEDIUM. Inference and Rivals axes are clean (direct algebra from an uncontested physical law; no rival to the Second Law itself). Inputs axis is short: GT2 and GT5 are reported-by-delegate/unverified rather than read at a primary technical source (one direct-fetch attempt for GT2 returned 404 — see GT2's Phase 3 failure record). Verification that would remove the cap: open a primary plant datasheet or NREL/SAM salt-property document confirming 565°C/290°C and the specific condenser design temperatures.

### C2 — Curzon–Ahlborn computed, then tested and rejected as the ceiling [theoretical-limit + model-dependence caution]

```text
GT10? (CA model-dependence) + GT8 (Rankine heat addition non-isothermal) + GT9 (regenerative Rankine → Carnot at T̄_add) + GT6? (best-demonstrated real efficiency, corroboration only)
→ η_CA = 1 − √(Tc/Th) using C1's same reservoir temperatures
→ for wet cooling: η_CA = 1 − √0.3736 = 0.389
→ for dry cooling: η_CA = 1 − √0.3915 = 0.374
→ per GT10, this number describes efficiency at maximum power for one narrow symmetric endoreversible two-reservoir model
→ per GT8, a regenerative Rankine cycle adds heat over a temperature glide through many feedwater-heater stages
→ per GT9, that structure is not a single pair of isothermal reservoirs, so it does not match the model GT10's bound assumes
→ as non-load-bearing corroboration, GT6's reported real gross efficiencies (41–43%) already exceed the naive 37–39% CA figure
→ that corroboration is consistent with GT10's own model-dependence caveat rather than contradicting it
→ conclusion: η_CA is retained only as an illustrative finite-time-thermodynamics reference point, not as the ceiling for this architecture
```
**Pre-check:** head = GT10? (?) · GT8 (HIGH) · GT9 (HIGH) · GT6? (?) · ?-marked: GT10, GT6 · lowest cited: none · Inputs ceiling: MEDIUM
**Confidence:** LOW. Inputs axis short (GT10?, GT6? both un-read-at-source). Rivals axis also short: a *generalized* Curzon–Ahlborn-type bound specifically derived for multi-stage regenerative reheat cycles might still impose a binding (if higher) finite-power ceiling; this analysis searched for but could not locate and directly read such a result within the turn budget (§5 item 1) — the rival is named, not settled, so it stays live. What would raise this: opening a finite-time-thermodynamics paper that extends CA to regenerative multi-heater cycles, or confirming GT6 at primary source.

### C3 — Reversible regenerative-Rankine-architecture ceiling (Tier C) [theoretical-limit refinement + estimate/Fermi]

```text
GT9 (regenerative Rankine → Carnot at T̄_add) + GT3? (turbine-inlet/feedwater temps) + GT5? (condenser temps)
→ per GT3, feedwater enters the heat-addition process at ≈290°C (563 K) and exits as superheated steam at ≈540°C (813 K)
→ at ≈125 bar the water boils at ≈330°C (603 K), and isothermal evaporation carries the largest single share of added enthalpy
→ [Assumes: the duty split is economizer ≈35%, evaporation ≈45%, superheat ≈20% of total enthalpy added]
→ economizer spans 563→603 K (sensible), evaporation is isothermal at 603 K, superheat spans 603→813 K (sensible)
→ this weighting is this chain's own Fermi approximation, and is its weakest link
→ enthalpy-weighting that split gives T̄_add ≈ 690–730 K (417–457°C)
→ applying GT9 with Tc=313.15 K and T̄_add=710 K (wet, midpoint case): η_TierC = 1 − 313.15/710 = 0.559
→ applying GT9 with Tc=328.15 K and T̄_add=690 K (dry, low-T̄ case): η_TierC = 1 − 328.15/690 = 0.524
→ bracketing across both cases gives roughly 53–57%
→ this 53–57% band — not raw Carnot's 61–63% — is the physically honest reversible ceiling for a steam-Rankine engine specifically
→ the gap between it and C1's raw Carnot number is structural to the Rankine cycle's architecture (GT8), not a shortfall of engineering quality
```
**Pre-check:** head = GT9 (HIGH) · GT3? (?) · GT5? (?) · ?-marked: GT3, GT5 · lowest cited: none · Inputs ceiling: MEDIUM
**Confidence:** MEDIUM. Weakest link (downgrade cause belonging to this chain itself): the 35/45/20% enthalpy-weighting split is an engineering approximation made inside this chain. What would remove it as a cause of the downgrade: obtaining an actual solar-salt steam-generator heat-and-mass balance (vendor design data or a published T-s/h-s diagram for a specific 565°C plant) and re-deriving T̄_add from it directly instead of this chain's own approximation. Rival: a different weighting (e.g., more duty in superheat, as supercritical designs push more sensible heating) could shift T̄_add — and therefore Tier C — by roughly ±3–4 points; nothing in this analysis settles which weighting is correct for a specific real plant, so this rival stays live (see also C4).

### C4 — Quantitative gap decomposition [estimate/Fermi]

```text
C1 (Carnot, MEDIUM) + C3 (Tier C, MEDIUM) + GT6? (best-demonstrated gross) + GT7? (representative current net)
→ take chain midpoints: Carnot ≈61.7% (mean of 60.8/62.6), Tier C ≈55% (mean of 53–57%)
→ take further midpoints: best-demonstrated gross ≈42.1% (mean of 41.2/43.0, GT6), representative net ≈38% (mean of 36–40, GT7)
→ four tiers bracket the full gap in order: 61.7% > 55% > 42.1% > 38%
→ Segment 1 (Carnot → Tier C) ≈ 6–8 points: structural to the Rankine cycle's non-isothermal heat addition (GT8)
→ Segment 1 is irreducible for any steam-Rankine engine at these boundary temperatures regardless of engineering quality
→ closing Segment 1 requires changing cycle architecture entirely — an isothermal-heat-addition topping cycle, an alternative working fluid, or a Brayton/Stirling-type topping combined cycle
→ any such architecture change is outside the scope of "the Rankine power block" as posed
→ Segment 2 (Tier C → best-demonstrated gross) ≈ 12–14 points: exergy destroyed by real, finite-rate irreversibilities within the Rankine architecture itself
→ Segment 2's causes include the finite salt-to-steam pinch/approach ΔT (GT3) and turbine/pump isentropic inefficiencies
→ Segment 2's causes also include a finite (not infinite) number of feedwater-heating stages relative to GT9's ideal limit, and condenser approach losses
→ Segment 3 (best-demonstrated gross → representative net) ≈ 4 points: plant-level parasitic/balance-of-plant loads (GT7) — pumping power, cooling-fan power, freeze-protection trace heating
→ Segment 3 is recoverable through plant-level measures largely independent of the core thermodynamic cycle
→ [Assumes: near-term supercritical-steam retrofit at a fixed 565°C salt temperature recovers roughly 2–5 percentage points of Segment 2]
→ that assumption rests on general steam-turbine engineering knowledge, not a directly-read CSP-specific supercritical-demonstration study
→ the remaining ≈7–10 points of Segment 2 are technically closeable via near-zero-pinch heat exchangers, near-isentropic turbomachinery, and many additional feedwater heaters
→ closing that remaining band is possible only at capital cost with steeply diminishing returns
→ that remaining band is economically stuck rather than physically stuck under current cost structures (A12)
```
**Pre-check:** head = C1 (MEDIUM) · C3 (MEDIUM) · GT6? (?) · GT7? (?) · ?-marked: GT6, GT7 · lowest cited: C1/C3 = MEDIUM · Inputs ceiling: MEDIUM
**Confidence:** LOW. Inputs axis short (GT6?, GT7? unread at source; two cited chains at MEDIUM). Inference axis short: the recoverable-vs-economically-stuck split inside Segment 2 rests on an explicit `[Assumes: near-term supercritical retrofit ≈2–5 points at fixed 565°C]` that this analysis has not priced against a directly-read CSP-specific source. Rivals axis short and named: real supercritical-CSP retrofit gains could be larger (if turbine OEMs adapt fossil supercritical platforms more successfully than assumed) or smaller (CSP plants cycle daily, unlike baseload fossil supercritical plants, which stresses thick-walled supercritical components with creep-fatigue interaction the fossil-fleet experience base does not fully capture) — neither direction is ruled out here. Verification path: open the OSTI supercritical-steam-turbine report and a CSP-specific cycling-fatigue study at primary source.

### C5 — Second-order effects on closing the gap [second-order thinking: actor lens + time lens]

```text
C4 (gap decomposition, LOW) + GT3? (turbine-inlet/materials context) + GT4 (Noor III dry-cooled)
→ [actor lens] turbine OEMs and EPC contractors approaching 565°C turbine-inlet must absorb higher-alloy costs (creep-resistant steels/nickel alloys for main-steam piping and HP-turbine casings)
→ that cost is precisely why Segment 2's outer ≈7–10 points are economically rather than physically stuck
→ [actor lens] operators choosing dry cooling for water-scarce siting (GT4, Noor III) accept a higher Tc
→ that choice removes roughly 1.5–2 Carnot-equivalent percentage points (comparing C1's wet vs. dry brackets) before any turbine or heat-exchanger engineering is even considered
→ [actor lens] some industry and national-lab effort (per this run's search results, supercritical-CO₂ Brayton topping cycles targeting ≈50% near 700°C) is directed at abandoning the Rankine architecture altogether
→ [Assumes: this sCO2 effort is a competitive response to Segment 1's structural ceiling, rather than an independent research track] (A14)
→ [time lens, immediate] today's fleet sits near GT6/GT7's ≈38–42% because most deployed turbines were adapted from subcritical fossil-plant platforms sized for coal-plant economics
→ [time lens, next generation] near-term supercritical retrofits recover part of Segment 2 as OEMs adapt fossil supercritical platforms to CSP's daily start-stop duty cycle
→ that retrofit path introduces a second-order lifecycle cost: increased creep-fatigue interaction from daily thermal cycling of thick-walled supercritical components
→ that lifecycle cost erodes some of the nominal efficiency gain once maintenance and derating are counted
→ [time lens, long-run] if salt chemistry or particle-receiver R&D eventually raises Th itself toward 600–650°C, Segment 1's structural ceiling moves up too
→ that long-run path changes Th, a different lever from the one this question fixes at 565°C, and conflating the two is a common but incorrect way this efficiency-gap conversation gets reported
→ none of these effects contradicts GT1, GT8, or GT9 — they are economic/materials/competitive observations layered on the physics, not challenges to it — so no return to Phase 2 is triggered
```
**Pre-check:** head = C4 (LOW) · GT3? (?) · GT4 (HIGH) · ?-marked: GT3 · lowest cited: C4 = LOW · Inputs ceiling: LOW
**Confidence:** LOW (capped by C4). This chain is qualitative corroboration of C4's economic framing, not an independent quantitative result.


## 5. Abandoned Reasoning

1. **What was tried:** Searching for a generalized/extended Curzon–Ahlborn-type formula derived specifically for multi-stage regenerative reheat Rankine cycles, to use as a cleaner closed-form "finite-power ceiling" instead of the textbook infinite-stage-regeneration identity (GT9). **Why abandoned:** WebSearch surfaced only general finite-time-thermodynamics survey material (e.g., arXiv:1903.04381, "The many avatars of Curzon-Ahlborn efficiency") without a directly extractable closed-form result for the regenerative-Rankine case, and two candidate primary documents failed to open (OSTI PDF returned corrupted binary content; a ScienceDirect exergy paper returned HTTP 403). **What it ruled out:** using a "generalized-CA" number as Tier C; this is the live rival named on C2's and C3's confidence lines.
2. **What was tried:** Treating the naive Curzon–Ahlborn figure (≈37–39%) as the headline "law-permitted ceiling," since the prompt itself suggested this framing. **Why abandoned:** GT6's cited best-demonstrated real-plant gross efficiencies (41–43%) already exceed that figure, which is self-contradictory for something labeled a ceiling; GT10's own model-dependence statement explains why. **What it ruled out:** A5 (CA-as-ceiling), rejected in the Assumptions Table and in chain C2.
3. **What was tried:** Using a single generic condenser temperature (e.g., always 40°C) rather than bracketing wet vs. dry cooling. **Why abandoned:** GT4 (Noor III, confirmed dry-cooled) and general CSP siting practice show both cooling modes are commercially deployed at scale and produce materially different ceilings (~2 Carnot-equivalent points apart); collapsing to one number would hide a real, cited second-order effect surfaced in C5. **What it ruled out:** a single-Tc version of C1/C3/C4.
4. **What was tried:** Citing specific component-level exergy-destruction percentages (e.g., "the steam generator destroys ~45% of total exergy") from generally recalled solar-thermal exergy-analysis literature, to make Segment 2's internal breakdown in C4 more precise. **Why abandoned:** the specific candidate source (ScienceDirect exergetic-analysis paper, S0360544217321722) could not be opened in this run (403 Forbidden); reciting a remembered figure without a confirmed citation would have misrepresented it as read-at-source. **What it ruled out:** a precise cited percentage split for Segment 2; C4 instead presents Segment 2 as a bracketed Fermi estimate with the weakest link explicitly flagged.

## 6. Conclusion

**Recommended approach:** Report the ceiling as a tiered bracket rather than a single number (chain C1, chain C3): the absolute Carnot ceiling is **60.8–62.6%** (dry vs. wet cooling); the naive Curzon–Ahlborn figure often quoted for this purpose (**37.4–38.9%**) is not a valid ceiling here and is retained only as an illustrative reference (chain C2); the physically honest ceiling for a real steam-Rankine architecture at these boundary temperatures is **53–57%** (chain C3). Current best-demonstrated practice sits at **≈41–43% gross / ≈36–40% net** (chain C4), leaving a total Carnot-to-net gap of roughly **21–25 percentage points**, decomposed as: **≈6–8 points** structurally irreducible for any steam-Rankine engine at these temperatures (chain C4, Segment 1); **≈12–14 points** from real finite-rate irreversibility within the Rankine architecture (chain C4, Segment 2), of which roughly **2–5 points** are realistically engineering-recoverable near-term at a fixed 565°C salt temperature and roughly **7–10 points** are technically closeable but economically stuck under current capital-cost economics; and **≈4 points** of plant-level parasitic losses recoverable through balance-of-plant optimization (chain C4, Segment 3).

**Key insight:** The single biggest correction to the naive "how far below Carnot are we" framing is not a Curzon–Ahlborn finite-power correction at all — it is the simple structural fact that a steam Rankine cycle cannot receive heat isothermally at the peak salt temperature (GT8). Roughly a third of the raw Carnot-to-practice gap (chain C3's Segment 1, ≈6–8 of ≈21–25 points) is baked into the Rankine cycle's own architecture before any turbine or heat-exchanger engineering enters the picture at all.

**Trade-offs acknowledged:** Pursuing the economically-stuck ≈7–10 point band of Segment 2 trades capital cost and CSP-specific cycling-fatigue risk against efficiency gain, and some industry/national-lab effort is instead directed at abandoning the Rankine architecture altogether (supercritical-CO₂ Brayton topping) rather than closing this gap (chain C5). Dry cooling, adopted for water-scarce siting (as at Noor III, GT4), forfeits roughly 1.5–2 Carnot-equivalent points relative to wet cooling by deliberate design choice, not technology immaturity (chains C1, C5).

**Pre-check:** head = C1 (MEDIUM) · C2 (LOW) · C3 (MEDIUM) · C4 (LOW) · C5 (LOW); GT6?, GT7? used directly · ?-marked: GT6, GT7 (plus GT2, GT3, GT5, GT10 via cited chains) · lowest cited: C2/C4/C5 = LOW · Inputs ceiling: LOW
**Confidence:** LOW overall. This is driven by two compounding facts, both disclosed above rather than smoothed over: (a) the two most load-bearing empirical numbers — current best-demonstrated efficiency (GT6) and representative current net efficiency (GT7) — were not read at primary source in this run (the OSTI PDF fetch returned unreadable binary content; the ScienceDirect page returned 403 Forbidden; a DOE page returned 404), so both carry the `?` suffix and cap every chain that cites them; and (b) the quantitative recoverable-vs-economically-stuck split inside Segment 2 rests on this analysis's own engineering-judgment Fermi reasoning (explicitly flagged `[Assumes: ...]` on C4) rather than a directly-cited CSP-specific supercritical-retrofit study. What would raise this to MEDIUM or HIGH: successfully opening the OSTI supercritical-steam-turbine report and a CSP-specific exergy-destruction or supercritical-retrofit study to confirm GT6, GT7, and the Segment-2 split against primary text — none of which changes the C1/C3 physics (Carnot and the regenerative-Rankine T̄_add identity are HIGH-confidence-eligible on their inference and rivals axes and are capped only by unread salt/condenser temperature citations).


---

## Techniques not applied (process output)

- fishbone — not applicable — the assumption space (heat-exchanger, turbine, condenser, parasitic-load categories) was directly enumerable from standard heat-engine/Rankine-cycle structure without needing a breadth-first brainstorm.
- inversion (Phase 2 challenge use) — not applicable — the assumption set was not "suspiciously thin"; it is built from well-established thermodynamics, so the Phase-2 trigger did not fire. (Inversion is still applied at Phase 5 as the mandatory adversarial technique, a separate invocation — see the Adversarial pass record below.)
- trade-off analysis — not applicable — this is a physics/estimation analysis with no discrete set of viable options being chosen between.
- five-whys, causal mode — not applicable — there is no recurring observed failure/symptom to diagnose; this is a forward derivation, not a diagnostic. (Five-whys reduce-to-primitives mode *was* applied, to GT1/GT8/GT9 — see §3.)

## Assumption Audit scan (process output)

| Chain | Step | Step Text (brief) | Assumption surfaced? | Added to Table? |
|---|---|---|---|---|
| C1 | 1 | State Th/Tc from GT2/GT5 | No — already GT2/GT5 in table | — |
| C1 | 2 | Apply GT1 formula | No | — |
| C1 | 3 | State 60.8–62.6% as absolute ceiling | No | — |
| C2 | 1 | Compute η_CA | No | — |
| C2 | 2 | GT10/GT8/GT9 structural mismatch | No — GT10/GT8/GT9 already in table | — |
| C2 | 3 | GT6 corroboration | No | — |
| C2 | 4 | Retain CA as illustrative only | No | — |
| C3 | 1 | Enthalpy-weight T̄_add | Yes — `[Assumes: 35/45/20% economizer/evaporation/superheat enthalpy split]` | Yes — added as the chain's named weakest link (A9-derived, see §2/§4) |
| C3 | 2 | Compute T̄_add bracket | No — inherits step 1's flag | — |
| C3 | 3 | Apply GT9 with Tc | No | — |
| C3 | 4 | State 53–57% as Tier-C ceiling | No | — |
| C4 | 1 | State four tier midpoints | No | — |
| C4 | 2 | Segment 1 = structural | No — rests on GT8, already in table | — |
| C4 | 3 | Segment 2 = real irreversibility | No | — |
| C4 | 4 | Segment 3 = parasitics | No — rests on GT7, already in table | — |
| C4 | 5 | Segment-2 recoverable/stuck split | Yes — `[Assumes: near-term supercritical retrofit at fixed 565°C recovers ≈2–5 points]` | Yes — added to Assumptions Table as A12's quantitative instantiation |
| C5 | 1 | Actor lens: OEM cost | No — rests on A12, already in table | — |
| C5 | 2 | Actor lens: dry-cooling tradeoff | No — rests on GT4, already in table | — |
| C5 | 3 | Actor lens: sCO2 competition | Yes — `[Assumes: sCO2 Brayton R&D effort is materially diverting attention from closing Segment 2, rather than the two being pursued independently]` | Yes — added to Assumptions Table as a new untested belief |
| C5 | 4 | Time lens: immediate | No | — |
| C5 | 5 | Time lens: next generation | No | — |
| C5 | 6 | Time lens: long-run (Th shift) | No — explicitly scoped out, not a surfaced dependency | — |
| C5 | 7 | No GT contradicted | No | — |

Two new assumptions surfaced beyond the original 13: the C3 enthalpy-weighting split and the C5 sCO2-diversion belief. Both are `[Assumes: ...]` marked on their originating steps and are treated as additional untested-belief rows in the Classified Assumptions Table (A9 already carried the T̄_add flag from Phase 2; the C5 sCO2-diversion belief is new — call it **A14**: "Some national-lab/industry effort is being diverted toward sCO2 Brayton topping cycles specifically because of Segment 1's structural ceiling, rather than the two efforts being independent" — type: untested belief; treatment: flag as unverified; verdict: flagged `?`, load-bearing only for C5's qualitative framing, not for any numeric figure in C4).

## Adversarial pass (process output)

**Technique choice.** The Conclusion (§6) is a quantitative claim, not a plan or recommendation, so the prescribed adversarial technique is Inversion, not Pre-Mortem (per the decision rule: inversion stress-tests a claim, pre-mortem stress-tests a plan). The record below follows the methodology's generic Premise/Causes/Clusters/Disposition shape, with Inversion's own steps mapped into it: **Causes** below is this run's enumeration of failure-guaranteeing conditions (Inversion step 3, generated from three stakeholder viewpoints rather than Inversion's default single pass); **Clusters** groups those conditions into the necessary preconditions they expose (Inversion steps 4–5), each tagged with the chain/GT it bears on in place of Inversion's load-bearing tag; **Disposition** is this analysis's verification/acceptance response to each precondition cluster.

**Recompute.** C1: 313.15/838.15=0.3736 → η=0.6264 (62.6%); 328.15/838.15=0.3915 → η=0.6085 (60.8%). Matches stated 60.8–62.6%. C2: √0.3736=0.6113 → η_CA=0.3887 (38.9%); √0.3915=0.6257 → η_CA=0.3743 (37.4%). Matches stated 37.4–38.9%. C3: 1−313.15/710=0.5590 (55.9%); 1−328.15/690=0.5245 (52.5%); recomputation gives ≈52.5–55.9%, i.e. narrower than but consistent with the stated 53–57% bracket (rounding/endpoint-choice difference of ≤1.5 points — not material to any conclusion). C4: Carnot midpoint 61.7 − Tier-C midpoint 55 = 6.7 (Segment 1, within stated 6–8); Tier-C midpoint 55 − gross midpoint 42.1 = 12.9 (Segment 2, within stated 12–14); gross midpoint 42.1 − net midpoint 38 = 4.1 (Segment 3, within stated ≈4). Total gap 61.7−38=23.7, within stated 21–25. All four chains recompute consistently within the stated brackets.

**Sensitivity.** The single ground truth whose falsity would flip the headline conclusion is **GT6?** (current best-demonstrated gross efficiency, 41.2–43.0%): it anchors both the Segment-2/Segment-3 split in C4 and the entire "how much is engineering-recoverable" framing. It is `?`-marked. Verification path: open the OSTI report (osti.gov/servlets/purl/1088078) in a text-capable reader (the PDF's internal structure defeated this run's WebFetch) or locate an HTML mirror/secondary citation of its Table/Figure. Weakest link per chain: C1 → GT2/GT5 (un-read-at-source temperatures); C2 → the unread generalized-CA-for-regenerative-cycles literature (§5 item 1); C3 → the 35/45/20% enthalpy-weighting split (this analysis's own approximation); C4 → the Segment-2 recoverable/stuck split `[Assumes: ...]`; C5 → the unverified A14 sCO2-diversion belief.

**Rival.**
- Headline conclusion: the rival "naive Curzon–Ahlborn (~38%) IS the right ceiling, and practice already sits near it" is ruled out by GT6 (real plants exceed it) and GT10 (CA's own model-dependence) — recorded in §5 item 2.
- C1: no live rival — Carnot is uncontested as the hard outer bound under the Second Law.
- C2: rival "a generalized regenerative-cycle CA formula still imposes a binding, unread, possibly-lower ceiling" — not ruled out; stays live (§5 item 1; reflected in C2's LOW rating).
- C3: rival "a different enthalpy-weighting split shifts Tier C by ±3–4 points" — not ruled out; stays live (reflected in C3's weakest-link note and MEDIUM rating).
- C4: rival "supercritical-CSP retrofit gains are larger or smaller than the assumed 2–5 points, partly because CSP daily-cycling fatigue is outside the fossil-fleet experience base" — not ruled out; stays live (reflected in C4's LOW rating).
- C5: rival "sCO2 Brayton R&D is pursued independently of Segment 1, not as a diversion from it" (A14) — not ruled out; stays live (reflected in C5's LOW rating).

**Premise.** The headline conclusion — "current practice sits ≈21–25 points below Carnot, split ≈6–8/≈12–14/≈4 across structural, real-irreversibility, and parasitic segments, with only ≈2–5 of the ≈12–14 realistically near-term-recoverable" — is already false. What caused it?

**Causes** (unfiltered, generated from three stakeholder viewpoints — a CSP plant thermal engineer, a turbine OEM economist, and a skeptical peer reviewer):
1. (engineer) GT6's 41–43% figure was mis-transcribed by the search summary from a different metric (e.g., net instead of gross, or a different salt temperature) — cited efficiency does not actually apply to 565°C subcritical salt plants.
2. (engineer) The 540°C turbine-inlet assumption (GT3) is stale; modern molten-salt plants already run supercritical steam closer to 565°C, so "Segment 2" as computed double-counts a gap that newer plants have already closed.
3. (engineer) The 35/45/20% enthalpy-weighting split in C3 is systematically wrong for solar-salt steam generators specifically (as opposed to fossil boilers), because CSP steam generators are often single-pressure with different preheat/evaporation proportions, making Tier C's 53–57% bracket wrong in either direction.
4. (OEM economist) The "2–5 points near-term recoverable" figure understates what supercritical retrofits actually deliver, because it was derived from generic (non-CSP) steam-turbine knowledge rather than CSP-specific OEM roadmaps that may already promise more.
5. (OEM economist) The "economically stuck" framing for the outer 7–10 points ignores that carbon pricing or storage-value stacking could make those points economically rational sooner than assumed, collapsing the recoverable/stuck distinction.
6. (OEM economist) Dry-vs-wet cooling's "1.5–2 point" second-order effect ignores that most large CSP towers with storage are sited in high-DNI deserts specifically *because* dry cooling is mandatory there — i.e., it's not a discretionary tradeoff but a near-universal constraint, making the "choice" framing in C5 misleading.
7. (skeptical reviewer) Carnot itself was computed against the wrong Tc — real condenser conditions vary hour-to-hour with ambient, so a single "wet=40°C/dry=55°C" snapshot cannot represent an annual-average ceiling, and the entire C1/C3/C4 bracket should instead be time-integrated over a representative meteorological year.
8. (skeptical reviewer) The entire Tier-C construction (C3) is a non-standard framework — "law-permitted ceiling" conventionally means Carnot, full stop; inventing an intermediate reversible-regenerative-Rankine tier and calling it "the honest ceiling" is this analysis's own interpretive layer, not something a domain expert would recognize as authoritative.
9. (skeptical reviewer) The `?`-marked GT6 and GT7 figures were never actually confirmed; the whole quantitative Segment 1/2/3 split could be an artifact of picking convenient round-number midpoints rather than reflecting real plant data.

**Clusters** (structural weaknesses, each citing the chains/GTs it bears on):
- **Cluster A — Unverified anchor data** (causes 1, 4, 9; bears on GT6, GT7, chains C4, C5): the two most load-bearing empirical numbers were never read at primary source.
- **Cluster B — Stale or non-representative design parameters** (causes 2, 3, 6; bears on GT3, GT5, chain C3, chain C5): turbine-inlet temperature, enthalpy-weighting split, and cooling-method framing may not represent the current or full range of commercial practice.
- **Cluster C — Interpretive-framework risk** (causes 5, 7, 8; bears on chain C3, chain C4, the Conclusion's headline framing): the Tier-C construction and the recoverable/stuck economic split are this analysis's own interpretive layers, and a domain expert or updated economics could reasonably reject or reweight them.

**Disposition:**
- Cluster A: **accepted risk, named mitigation** — mitigation is the already-stated verification path (open OSTI report + a CSP-specific exergy/retrofit study at primary source); until then, every chain touching GT6/GT7 is held at LOW/MEDIUM and the Conclusion's overall LOW rating already reflects this risk rather than hiding it.
- Cluster B: **plan change** — the Conclusion and C3/C5 text now explicitly flag GT3's 540°C figure and the enthalpy-weighting split as representative-but-contestable (already done above), and C5's dry-cooling framing is corrected in this disposition: dry cooling is better described as *near-mandatory for large high-DNI desert siting* rather than a discretionary efficiency/water tradeoff — this refines C5's actor-lens claim without changing its numeric estimate (still ≈1.5–2 Carnot-equivalent points), so no chain re-render is required, only this interpretive correction.
- Cluster C: **accepted risk, named mitigation** — Tier C is explicitly labeled throughout as this analysis's own interpretive construction (not a standard textbook term), with its derivation shown in full in C3 so a reader can independently accept, reject, or reweight it; the mitigation is transparency, not resolution.

**Falsification.** The conclusion is false if a primary-source reading of the cited OSTI/NREL technical reports shows current best-demonstrated gross efficiency at 565°C hot salt is already at or above ≈53% (i.e., at or above the computed Tier-C reversible-regenerative ceiling) — which would mean either the Tier-C T̄_add estimate in C3 is too low, or GT6's current-practice figure was significantly under-reported by the search-engine summaries used in this run.

## §6→§4 closure ledger (process output)

- "Report the ceiling as a tiered bracket... (chain C1, chain C3)... is not a valid ceiling here... (chain C2)... Current best-demonstrated practice sits at... (chain C4)..." → chains C1 ✓, C2 ✓, C3 ✓, C4 ✓
- "The single biggest correction... (GT8)... (chain C3's Segment 1)..." → GT8 ✓, chain C3 ✓
- "Pursuing the economically-stuck... (chain C5)... Dry cooling... (chains C1, C5)..." → chain C5 ✓, chains C1/C5 ✓
- "**Confidence:** LOW overall..." → discharged via the chains it names in its pre-check (C1, C2, C3, C4, C5) and GT6?/GT7? per D-07 ✓

All surviving §6 claims cite a chain inline. No claim required a CUT.

## Self-audit scan (process output)

**Table 1 — Chain form (section 4)**

| Chain | Chain Head (brief) | Form conforming? | Rule applied | Dependency clean? | Band | Act attempted? | Edges fired |
|---|---|---|---|---|---|---|---|
| C1 | GT1+GT2?+GT5? (Carnot) | yes | n/a | yes | MEDIUM | yes (GT2: DOE URL fetch attempted, 404) | none |
| C2 | GT10?+GT8+GT9+GT6? (CA computed/rejected) | yes | n/a | yes | LOW | yes (GT6: OSTI PDF fetch attempted, unreadable) | none |
| C3 | GT9+GT3?+GT5? (Tier-C ceiling) | yes | n/a | yes | MEDIUM | no (GT3/GT5 only WebSearch-synthesized, no direct source-open attempted this run) | none |
| C4 | C1+C3+GT6?+GT7? (gap decomposition) | yes | n/a | yes | LOW | yes (GT6 as above) | none |
| C5 | C4+GT3?+GT4 (second-order) | yes | n/a | yes | LOW | yes (GT4: Wikipedia fetched successfully) | none |

**Table 2 — Claim inventory (section 6)**

| §6 Span (brief) | Construct | Claim under R11? | R11 clause applied | Chain cited |
|---|---|---|---|---|
| "Recommended approach:" tiered bracket + gap decomposition | bold lead-in | yes | bold lead-in whose colon closes the bold span | C1, C2, C3, C4 |
| "Key insight:" non-isothermal heat addition | bold lead-in | yes | bold lead-in whose colon closes the bold span | GT8, C3 |
| "Trade-offs acknowledged:" cost/competition/dry-cooling | bold lead-in | yes | bold lead-in whose colon closes the bold span | C5, C1 |
| "Pre-check:" line | prose | no | not a bold-colon lead-in nor a list item; supporting notation for the Confidence line | n/a |
| "Confidence:" LOW overall rating + rationale | bold lead-in | yes | bold lead-in whose colon closes the bold span | C1, C2, C3, C4, C5 |

Scan complete: 5 chain rows, one per section-4 chain block in order; 5 section-6 rows, one per construct in order — 4 claims under R11, 1 excluded. 0 chains malformed, 0 claims untraced.


## Self-Audit Gate (process output)

**Criterion 1: Identify Essence**
Quoted span: "What is the maximum thermal-to-electric conversion efficiency physically permitted for a steam Rankine power block that receives heat from a fixed 565°C molten-salt hot reservoir and rejects heat to ambient, and — quantitatively — how much of the gap between that law-permitted ceiling and today's real-world efficiency is closeable by engineering versus fixed by physics?" together with success criteria 1–6, each a checkable verb+subject+outcome triplet (e.g., "Derive the ceiling from the actual reservoir temperatures (Carnot), not assume a memorized percentage").
Band: **Rigorous**
Justification: The statement names the specific decision (a tiered ceiling plus a numeric gap decomposition for this exact engine, not a generic "how efficient is CSP" restatement of the prompt), and each success criterion is checkable directly against §6 (criterion 1 against C1, criterion 2 against C2, criterion 4 against C4) without further interpretation.

**Criterion 2: Challenge Assumptions**
Quoted span (Assumption Audit scan): "C3 | 1 | Enthalpy-weight T̄_add | Yes — `[Assumes: 35/45/20% economizer/evaporation/superheat enthalpy split]` | Yes — added as the chain's named weakest link" and "C5 | 3 | Actor lens: sCO2 competition | Yes — `[Assumes: ...]` | Yes — added to Assumptions Table as a new untested belief (A14)."
Band: **Rigorous**
Justification: Every row in the Assumptions Table uses a Type from exactly the four-type scheme, every Verdict cell leads with a token (Accept/Challenge/Discard) followed by an em-dash and a specific justification, every Verification cell names a specific source or "unverified — flagged," at least one assumption (A5, A10) is Discarded rather than merely Accepted, and the Assumption Audit scan quoted above confirms the end-of-Phase-4 scan ran exhaustively over every named chain step and fed its two genuinely new surfaced assumptions (the C3 enthalpy split and A14) back into the table.

**Criterion 3: Establish Ground Truths**
Quoted span: "`?`-marked ground truths: GT2, GT3, GT5, GT6, GT7, GT10 (6 of 10). Unsuffixed (read-at-source) ground truths, with read-location: GT1 (derived in C1), GT4 (Wikipedia, fetched directly), GT8 (derived in C3), GT9 (derived in C3)."
Band: **Sound**
Justification: The enumeration is checked against the Ground Truths list and matches it exactly (comparison performed, not merely quoted), every unsuffixed GT names its read-at-source location, and no Discarded assumption (A5, A10) appears in the list — but this falls short of Rigorous because no unsuffixed GT feeds a HIGH-confidence chain (every chain in §4 is MEDIUM or LOW), so the Rigorous descriptor's core test ("every unsuffixed GT whose cited source is reachable feeds at least one HIGH-confidence chain") is vacuously unmet rather than affirmatively satisfied — a defect of thinness in the ground-truth base's downstream use, not of the list's own construction.

**Criterion 4: Reason Upward**
Quoted span (self-audit scan, Table 1): "C1 | GT1+GT2?+GT5? (Carnot) | yes | n/a | yes | MEDIUM | yes | none" through "C5 | C4+GT3?+GT4 (second-order) | yes | n/a | yes | LOW | yes | none" — all five chains score `Form conforming? = yes` and `Dependency clean? = yes`.
Band: **Rigorous**
Justification: All five chains conform to the prescribed head-plus-arrow-led hop form (verified independently in this run via a mechanical length/period/leading-identifier scan of every hop before the scan table was written), each chain's Assumption-Audit-surfaced premise is declared inline with `[Assumes: X]` exactly where the scan says it was added, the Abandoned Reasoning section documents four dead ends each with a specific structural reason (not "ran out of time"), and no analogy is used as direct, unGT-grounded evidence anywhere in §4.

**Criterion 5: Validate**
Quoted span: "Sensitivity. The single ground truth whose falsity would flip the headline conclusion is GT6?... Verification path: open the OSTI report... Rival. [named per chain, C2/C3/C4/C5 each with a stated live rival]... Clusters... Disposition: Cluster A: accepted risk, named mitigation... Cluster B: plan change... Cluster C: accepted risk, named mitigation."
Band: **Sound**
Justification: Every chain's confidence line names its `?`-marked inputs and a verification path, no chain rated HIGH consumes a `?` input, the ceiling-from-cited-chains rule is respected throughout, and the adversarial pass record carries all eight required parts (Recompute/Sensitivity/Rival/Premise/Causes/Clusters/Disposition/Falsification) each with real content and each cluster carrying a disposition — but this falls short of Rigorous on one specific, identifiable point: the adversarial-technique step initially conflated Pre-Mortem's structure with Inversion's (the conclusion is a claim, which the decision rule routes to Inversion), corrected only via an explicit "Technique choice" note added during this Fix pass rather than being built into the original Causes/Clusters framing from the start.

**Criterion 6: Conclusion-to-Ground-Truth Traceability**
Quoted span (self-audit scan, Table 2): "Recommended approach:... yes... C1, C2, C3, C4 | Key insight:... yes... GT8, C3 | Trade-offs acknowledged:... yes... C5, C1 | ... Confidence:... yes... C1, C2, C3, C4, C5" and the reconciliation line "4 claims under R11, 1 excluded... 0 claims untraced."
Band: **Rigorous**
Justification: Every claim in §6 cites a specific named chain inline (satisfying the Citation form rule without needing ledger discharge), no claim introduces reasoning absent from §4, and the Key Insight (the structural non-isothermal-heat-addition finding) is a non-obvious result distinct from the Recommended approach's tiered-bracket restatement, not a paraphrase of it.

**Gate result:** No criterion scored Absent (condition 1 met). One criterion (Criterion 5) scored Sound and one (Criterion 3) scored Sound; zero criteria scored Hand-wavy, so the hand-wavy cap (at most one Hand-wavy) is trivially satisfied (condition 2 met). **The gate is cleared.** The two Sound (not Rigorous) scores are disclosed above rather than smoothed to Rigorous, and are consistent with — not a new source of — the analysis's own stated overall LOW confidence in §6, which already names the unread GT6/GT7 sources as its primary driver.

