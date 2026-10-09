## Answer

**Recommendation:** Treat the plant's efficiency as a five-layer stack, not one number, and pursue the recoverable composite engineering package — salt/steam heat-exchanger approach tightening, parasitic/pump efficiency improvements, and part-load/operational improvements — now, deferring a supercritical-pressure upgrade to a new-build or major-repowering decision (chain C7).
**Band (from §6):** LOW — chains C1–C7 (chain C1 is HIGH; the weakest contributing links are C6 and C7, both LOW).
**Would change it:** Resolving assumption A-6 — whether supercritical pressure alone, without raising salt temperature above 565 °C, captures most or only a fraction of the cited "~50%" supercritical figure — is the single highest-leverage fix, since it would lift chain C6, and with it C7, toward MEDIUM (chain C6).
## 1. Problem Essence

**Core problem:** Given a fixed hot-reservoir temperature of 565 °C (set by nitrate-salt thermal-stability chemistry, not by the steam cycle itself), what ceiling does physical law place on the thermal-to-electric efficiency of the downstream steam-Rankine power block, how far below that ceiling do deployed/near-term molten-salt tower plants actually sit, and of that shortfall, how many percentage points are closeable with engineering already proven elsewhere (e.g. in the coal fleet) versus permanently unavailable within today's salt-chemistry-plus-steam-Rankine architecture?

**Success criteria:**
1. The analysis states a Carnot ceiling (§4 chain C1) computed from the stated hot-reservoir temperature and an explicit, justified cold-reservoir temperature, and explains why no real engine approaches it.
2. The analysis states a second, tighter ceiling specific to the Rankine-cycle *topology* (§4 chain C2) that is demonstrably below the Carnot number and attributes the gap to a named physical mechanism (non-isothermal heat addition), not to equipment imperfection.
3. The analysis states a current-practice net efficiency figure (§4 chain C3/C4), explicit about gross vs. net, sourced to named plants/studies.
4. The analysis decomposes the gap between (2) and (3) into named components (§4 chain C5) and classifies each as recoverable-with-known-engineering or structurally stuck (§4 chain C6), producing a single absolute-percentage-point recoverable estimate with a stated uncertainty bracket.
5. The final summary table reports five numbers on a common net-efficiency basis — Carnot ceiling, cycle-topology ceiling, current practice, recoverable gap, hard floor — each traceable to a derivation chain.

A success criterion is not satisfied by picking one "winning" number among the five layers the question names; all five must be reported together, since the question's own success condition is the full stack, not a single verdict.
## 2. Assumptions Table

**Fishbone pass (breadth-first cause-category brainstorm) run before this table was finalized**, to make sure the gap-decomposition in §4 is not missing a whole category of cause. Category set used: the domain-default six (People, Process, Technology/Equipment, Environment, Information, Resources), relabelled for this physical-plant problem as **Chemistry** (salt stability), **Cycle thermodynamics** (topology), **Equipment** (turbine/pump/HX hardware), **Siting/Environment** (ambient, water availability), **Operations** (dispatch, cycling), **Economics/Scale** (unit size vs. technology fit). Each branch below fed either a ground truth (§3) or an assumption row in this table; none were discarded without a disposition:
- Chemistry → GT-3? (565 °C decomposition ceiling) — verified by domain literature, see five-whys drill in §3.
- Cycle thermodynamics → A-1, A-5 (topology ceiling estimate) — becomes chain C2.
- Equipment → A-4, A-9 (component maturity, USC-coal proxy) — becomes chain C3/C5.
- Siting/Environment → A-3, A-7 (cooling method, ambient) — becomes chain C5 component.
- Operations → A-8 (cycling/part-load) — becomes chain C5 component.
- Economics/Scale → A-6 (supercritical-at-565 °C ambiguity), folded into C6's recoverability judgment and the trade-off in C7.
No category returned zero candidate causes, and no candidate cause was dropped without being carried into either a ground truth or a table row below.

**Inversion pass run on the claim "most of the gap is recoverable with known engineering."** Failure-guaranteeing conditions enumerated: (i) the ~50% supercritical figure actually requires salt temperature above 565 °C, not just higher pressure, so none of it is available at today's chemistry (addressed by A-6, carried as an unresolved ambiguity rather than resolved); (ii) current 42–44% gross figures are already close to the idealized topology ceiling, leaving little headroom regardless of pressure (addressed by A-5's bracket and priced into chain C5); (iii) the gross-to-net parasitic factor is itself near a physical floor (pumping molten salt and feedwater is unavoidable work), so "recoverable parasitics" is a much smaller number than it looks (priced into chain C6's component breakdown); (iv) dry-cooling's efficiency penalty is a water-scarcity-driven siting choice, not an engineering gap, so no physical plant-level fix removes it without accepting water use CSP was sited in deserts specifically to avoid (priced into chain C6 as a resource/siting floor, not a physical-law floor). Each of these four became an explicit line in chain C6 rather than being absorbed as background texture — this is what keeps the recoverable-points estimate from overstating itself.

| Assumption | Type | Treatment | Verdict | Verification |
|------------|------|-----------|---------|--------------|
| A-1: Using the hot **salt-tank** temperature (565 °C / 838.15 K) directly as the Carnot hot-reservoir temperature, as the question's own framing specifies, even though the turbine never actually sees 838 K (live steam is always below tank temperature after the salt-to-steam heat-exchanger approach ΔT) | convention | Explicitly challenge before use | Accept — explicitly flagged as an *upper bound on an upper bound*; the real approach-ΔT loss (≈10–20 °C) is carried forward as one named component of the gap in chain C5, not silently absorbed | Internally consistent with the question's own instruction to use 565 °C as the hot reservoir; the resulting Carnot number is explicitly labelled as unreachable twice over |
| A-2: 565 °C is a **current materials/chemistry constraint** of nitrate solar salt (60/40 NaNO₃/KNO₃), not a law of physics — a different HTF chemistry could raise it | current constraint | Record expiry conditions | Accept — expires if/when chloride-salt, carbonate-salt, liquid-metal, or particle-based HTFs (DOE Gen3 CSP-class R&D) reach commercial deployment at higher operating temperatures; as of this analysis (Oct 2026) none is commercially deployed at utility scale, so the constraint holds for the "today's salt" scope the question sets | GT-3? (decomposition chemistry) |
| A-3: Representative cold-reservoir/condenser temperatures: wet cooling ≈35–40 °C (308–313 K); dry (air-cooled) cooling in hot desert CSP siting ≈55–65 °C (328–338 K) at full-load summer design point | convention | Explicitly challenge before use — site- and technology-dependent, not fixed | Accept — challenged against night-time/storage-shifted dispatch (CSP with storage often dispatches in the evening when ambient is cooler, which would move the real average toward the low end of the dry-cooling range); retained as a design-point bracket, with the operational variation folded into chain C5's "operations" component rather than re-defining the reservoir temperature itself | GT-7?, GT-8? |
| A-4: The literature figures found (42–44% gross, 0.87–0.875 gross-to-net factor) are representative of the deployed/near-term molten-salt tower fleet despite real heterogeneity in plant size and vintage (19.9 MWe Gemasolar vs. 110–150 MWe Crescent Dunes/Noor III/Cerro Dominador-class) | untested belief | Verify, or flag as unverified | Challenge — smaller turbines generally run fewer regenerative-extraction stages and carry higher relative loss fractions than larger units, so the true fleet range is wider than a single point figure; retained with an explicit ±2–3 point heterogeneity band rather than a bare central value — unverified — flagged | GT-4?, GT-6?, GT-9? |
| A-5: The idealized (isentropic turbines/pumps, many-stage regeneration, isothermal condensation) Rankine-cycle efficiency for the 565 °C/≈125 bar subcritical reheat topology is **estimated** in this session via entropy-mean-temperature scaling — not computed from a live steam-table lookup — at ≈46–49% (wet-cooled) / ≈43–46% (dry-cooled) | untested belief | Verify, or flag as unverified | Challenge — this is this analysis's own derived estimate, not a literature figure; cross-checked for self-consistency (must sit below Carnot and above today's real gross figure, both of which hold, see chain C2) but not independently verified against a steam-table package — unverified — flagged | Estimate procedure in §4 chain C2; cross-check only, no external source |
| A-6: Supercritical steam **pressure** (~250–270 bar) can be realized at a fixed 565 °C salt temperature to capture most of the cited "~50% supercritical" efficiency figure, without also needing a hotter salt (the Sandia/Siemens study frame mixes a 566 °C and a 600 °C salt case, so how much of the ~50% figure needs the temperature increase is not resolved by the sources found) | untested belief | Verify, or flag as unverified | Challenge — genuinely ambiguous in the sources found; carried into chain C6 as a wide bracket on the supercritical-upgrade recoverable component rather than resolved one way — unverified — flagged | GT-5? |
| A-7: Dry-cooling's full-load design-point efficiency penalty is larger than its annual-energy-weighted impact (≈1.3% for towers, per GT-7?) because thermal storage lets the plant shift generation timing away from the worst ambient hours | untested belief | Verify, or flag as unverified | Challenge — plausible and consistent with why towers (1.3%) differ so much from troughs (4.6%) in the same source, but not independently confirmed with a full-load number — unverified — flagged | GT-7? |
| A-8: CSP tower plants undergo real daily cycling (startup/shutdown, part-load ramp) even with thermal storage, which lowers annual-average realized efficiency below the full-load design-point net figure | current constraint | Record expiry conditions | Accept — expires only as far as storage duration grows toward continuous baseload operation (most current designs carry 6–10 h storage, per GT-9?-adjacent plant specs, not 24 h); until storage duration is much longer, some cycling is intrinsic to a solar-driven, storage-buffered (not baseload-fueled) plant | General CSP operating-pattern knowledge; not separately sourced in this session — carried as current constraint rather than physical law |
| A-9: Ultra-supercritical **coal-fired** steam-cycle efficiency figures (≈45–47% net plant at ≈600 °C/300 bar) indicate the thermodynamic headroom available to *any* steam-Rankine cycle at comparable top conditions, because Rankine-cycle efficiency is a function of steam conditions and cycle architecture, not of the heat source (combustion vs. molten salt) | untested belief | Verify, or flag as unverified — explicitly NOT used as an analogy ("coal plants do it, so CSP can too") but as a same-physics corroboration, since the turbine/boiler-feed thermodynamics do not know or care what heated the steam | Accept, with caveat — the physical-equivalence argument is sound (steam-side thermodynamics is heat-source-agnostic) but the 45–47% figure itself is domain background knowledge, not opened at a specific source in this session — unverified — flagged; used only to corroborate direction (supercritical headroom exists), never as the primary basis for a quantified number in chains C2–C6 | GT-10? — used as corroboration only, per the no-analogy-as-direct-evidence rule |
| A-10: The specific per-lever recoverable-percentage-point judgments in chain C6 (turbine/pump refinement ≈1.5 pt; HX-approach tightening ≈0.5–1 pt; parasitic/pump VFD ≈0.5 pt; cooling/insulation ≈0.7–1.2 pt; part-load operation ≈0.5–1 pt) are this analysis's own engineering judgment calls, surfaced by the end-of-phase Assumption Audit rather than declared when chain C6 was first drafted | untested belief | Verify, or flag as unverified | Challenge — no independent per-lever source was consulted for these specific splits; only the aggregate recoverable bracket (≈4–7 pts) is cross-checked against chain C5’s total — unverified — flagged | None — end-of-phase Assumption Audit surfaced this as ungrounded; no external source identified |
| A-11: The trade-off criteria weights (efficiency gain=5, maturity=4, econ-fit=4, capex=3, water=2) and per-option 1–5 scores against the stated anchors in chain C7 are this analysis's own judgment calls, not independently validated against a stakeholder-elicited weighting process, surfaced by the end-of-phase Assumption Audit | untested belief | Verify, or flag as unverified | Challenge — the flip-test on chain C7 shows the composite conclusion is robust to plausible weight perturbations, which mitigates but does not eliminate this exposure — unverified — flagged | None — end-of-phase Assumption Audit surfaced this as ungrounded; no external stakeholder-weighting source was consulted |
## 3. Ground Truths

**GT-1** The Carnot efficiency of a heat engine operating between a hot reservoir at absolute temperature $T_h$ and a cold reservoir at $T_c$ is $\eta_{Carnot} = 1 - T_c/T_h$, and no heat engine operating between those two reservoirs can exceed it (Second Law of Thermodynamics; Carnot's theorem) — source: physical law / definition, standard thermodynamic theory; read-at-source: not applicable (foundational law, not an empirical figure requiring a citation to verify).

**GT-2** The problem as posed fixes the hot reservoir at 565 °C = 838.15 K (the molten-salt hot-tank temperature) — source: given parameter of the question itself; read-at-source: stated directly in the prompt, not an external citation.

**GT-3?** 60/40 wt% NaNO₃/KNO₃ "solar salt" has a long-term thermal-stability ceiling of ≈565 °C; above it the nitrate anion decomposes (NO₃⁻ → NO₂⁻ + ½O₂), and above ≈600 °C the nitrite ion further decomposes toward oxide species, releasing NOₓ and corrosive decomposition products — cited to: patent/materials literature surfaced by WebSearch (USPTO patent documents on nitrate-salt compositions; DLR elib; MDPI Energies; ris.unimap.edu.my); reported-by-delegate: WebSearch synthesis — no single cited document was opened directly by this analysis.

  *Irreducibility check (five-whys, reduce-to-primitives mode) run on this ground truth, since the whole analysis's "565 °C ceiling" premise rests on it:* Claim → "solar salt is limited to ≈565 °C." Constituent 1: the limiting mechanism is chemical decomposition of the NO₃⁻ ion, not corrosion of containment metal or freezing — reducible further: the decomposition is NO₃⁻ → NO₂⁻ + ½O₂, an anion-decomposition reaction with an Arrhenius-type temperature-accelerated rate — this bottoms out at a named chemical reaction (irreducible: a measured/named reaction, not a further-decomposable claim). Constituent 2: "565 °C" is the temperature at which long-term (operational-lifetime) decomposition becomes unacceptable, which is an economic/engineering-lifetime threshold layered on top of a continuous rate curve (the reaction does not switch on sharply at 565 °C; it accelerates with temperature) — this is **assumed, not verified** in this session (no decomposition-rate-vs-temperature curve was opened), so GT-3 keeps its `?` for this reason specifically, not merely because the citation chain is indirect. Verdict: parent claim (GT-3) is **partially verified** — the reaction mechanism is a textbook-grade chemical fact (would bottom out as a verified primitive if the reaction equation itself were independently checked against a chemistry source, which was not done here) and the specific 565 °C number is an engineering-lifetime threshold reported by multiple converging delegate sources but not read at a primary data table by this analysis.

**GT-4?** Published/estimated gross (power-block, salt-heat-in to generator-terminals) design-point thermal-to-electric efficiency for a subcritical 565 °C molten-salt steam-Rankine cycle is ≈42–44% (a baseline figure of "~42%" for a simple subcritical cycle, and a dual-pressure-level-optimized design reported at "44.14% → 44.64%") — cited to: Sandia/Siemens supercritical-steam-turbine feasibility study (SAND 2013-1960, OSTI 1088078) and a UC3M dual-pressure steam-generator paper, both surfaced by WebSearch; reported-by-delegate: WebSearch synthesis. **Phase 3 verification step attempted:** this analysis opened https://www.osti.gov/biblio/1088078 directly with WebFetch, specifically asking for the numeric efficiency figures; the page's abstract/summary content did **not** contain the percentage figures (Phase 3 failure record: source opened, `citation does not support the claim` for the specific numbers — the figures were in the full SAND report PDF, which this session did not fetch). GT-4 therefore keeps its `?` on the stronger "unverified" footing, not merely "reported-by-delegate."

**GT-5?** Sandia/Siemens evaluated 14 subcritical-to-supercritical steam-cycle configurations (120–260 bar-a main steam pressure) at hot-salt temperatures of 566 °C and 600 °C, finding the most promising supercritical designs ≈10% lower LCOE than the 565 °C/120 bar-a subcritical baseline; a separate source states supercritical cycles could reach "~50%" vs. "~42%" subcritical efficiency — cited to: the same Sandia/Siemens study and general WebSearch synthesis; reported-by-delegate — the 566 °C-vs-600 °C mixing noted in A-6 means this ground truth does **not** cleanly resolve how much of the ~50% figure is available at a fixed 565 °C.

**GT-6?** A representative NREL System Advisor Model (SAM) gross-to-net conversion factor for a reference power-tower design point is ≈0.87–0.875 (the Gemasolar SAM case study cites 0.875), covering salt pumps, feedwater pumps, cooling-system auxiliaries, controls, and freeze-protection parasitics — cited to: SAM forum documentation and the SAM Gemasolar case PDF (sam.nrel.gov); reported-by-delegate — the PDF itself was not opened by this analysis.

**GT-7?** Switching a molten-salt power-tower plant from wet to dry (air-cooled) condenser cooling reduces **annual** electric output by only ≈1.3%, versus ≈4.6% for parabolic-trough plants, attributed to storage decoupling collection timing from generation timing — cited to: WebSearch synthesis of NREL/WorleyParsons CSP water-use literature; reported-by-delegate.

**GT-8?** Noor III (Ouarzazate, Morocco; 150 MWe nominal; Siemens SST-700/900 turbine; 2-tank molten-salt storage, 7 h) uses dry (air-cooled) condenser cooling — cited to: solarpaces.nrel.gov project page, surfaced by WebSearch; reported-by-delegate.

**GT-9?** Gemasolar (Fuentes de Andalucía, Spain) drives a 19.9 MWe gross Siemens SST-600 two-cylinder reheat steam turbine from 565 °C molten salt, and was the first and (at commissioning) largest two-tank molten-salt tower operating at this temperature — cited to: WebSearch synthesis of plant-technical sources; reported-by-delegate.

**GT-10?** Modern ultra-supercritical coal-fired steam cycles (≈600 °C/≈300 bar class, with reheat) achieve net plant efficiencies of roughly 45–47%; since steam-Rankine thermodynamics depend on steam conditions and cycle architecture rather than on the combustion vs. molten-salt heat source, this indicates the thermodynamic headroom available to any steam cycle at comparable top conditions — this figure is general power-engineering domain background, not opened at a specific source in this session; unverified: no specific document was read for this number, and it is used only as directional corroboration for chain C6's recoverability judgment, never as the primary basis for a quantified gap figure.

**Provenance summary.** `?`-marked: GT-3, GT-4, GT-5, GT-6, GT-7, GT-8, GT-9, GT-10 (8 of 10). Read-at-source (no `?`): GT-1 — physical law/definition, no empirical citation applicable; GT-2 — stated directly as the question's own given parameter, no external citation applicable. No ground truth in this analysis feeds a HIGH-confidence chain while carrying an unread citation that should have been read instead — every chain in §4 that rests on a `?`-marked ground truth is capped at MEDIUM or LOW per D-07, and no chain claims HIGH on the strength of an unread figure.
## 4. Derivation Chains

*Theoretical-limit procedure applied twice in this section (chains C1 and C2), per the decision rule separating it from inversion ("what is the ceiling?" vs. "what would guarantee failure?") and from estimate ("what is the ceiling?" vs. "how big, quantitatively, given uncertain inputs?"). Estimate procedure applied in chains C2, C4, C5 and C6 wherever a conclusion turns on a magnitude this analysis had to rebuild from constituent factors rather than read off a single source. Trade-off procedure applied in chain C7. Second-order procedure applied as an in-place extension of chain C7's hops (marked `→[2nd]` / `→[3rd]`), per the mandatory Phase 4 operation.*

### Conclusion C1: The Carnot ceiling for this plant's hot/cold reservoir pair is ≈60–63%, and it is physically unreachable by any real power-producing engine.

GT-1 (Carnot law, 2nd law of thermodynamics) + GT-2 (565 °C / 838.15 K hot reservoir)
→ a wet-cooled condenser at 308–313 K gives Carnot efficiency 1 − 308.15/838.15 to 1 − 313.15/838.15 = 62.6%–63.2% *[Assumes: A-3 — wet-cooling condenser temperature range]*
→ a dry-cooled desert condenser at 328–338 K gives Carnot efficiency 1 − 328.15/838.15 to 1 − 338.15/838.15 = 59.7%–60.8% *[Assumes: A-3 — dry-cooling condenser temperature range]*
→ the Carnot ceiling for this plant is ≈60–63% depending on cooling method, and because a 10 °C shift in either condenser-temperature estimate moves this number by only ≈1.2 points (ΔT/T_h), the qualitative conclusion — a ceiling in the high-50s-to-mid-60s%, far above anything achieved in practice — is insensitive to exactly which value within A-3's range is used
→ Carnot's derivation requires reversible heat transfer across zero temperature difference at every point in the cycle, which forces infinitesimally slow heat flux and therefore zero net power output, so no real engine — however well engineered — can approach this number while actually generating electricity

**Pre-check:** head GT-1, GT-2 · ?-marked: none · lowest cited: none · Inputs ceiling: HIGH
**Confidence:** HIGH — both head inputs are unsuffixed (GT-1 a physical law, GT-2 the question's own stated parameter); the arithmetic recomputes directly from GT-1's formula; the one `[Assumes: A-3]`-tagged premise is priced on the chain's own third hop (the endpoint survives a ±10 °C error in A-3's values, per the sensitivity stated there) rather than left unpriced; no rival conclusion survives — the claim that Carnot could be "approached" by good engineering is the one rival worth naming, and it is the specific thing this chain's own last hop rules out, citing GT-1's derivation directly.

### Conclusion C2: The idealized Rankine-cycle *topology* ceiling — isentropic components, multi-stage regeneration, isothermal condensation, but still the sensible-heating profile a real steam cycle has and Carnot does not — is ≈43–51% (central ≈47%, wet-cooled basis) / ≈41–49% (central ≈45%, dry-cooled basis), roughly 15–19 points below Carnot, and that gap is permanent.

**Estimate procedure.** Target quantity: η_ideal,topology (dimensionless, reported as %). Decomposition: η_ideal,topology = ρ × η_Carnot, where ρ (dimensionless) is the "second-law utilization ratio" characteristic of subcritical reheat-regenerative steam cycles — the fraction of the Carnot ceiling an idealized (lossless-component) Rankine cycle on the same two reservoirs actually reaches, given that it must add heat non-isothermally (feedwater sensible heating through to boiling) rather than isothermally. ρ is assigned from general steam-cycle thermodynamics (textbook Rankine-cycle progression from basic → superheated → reheat → regenerative cycles) rather than from a live steam-table computation performed in this session: ρ ∈ [0.70, 0.80], central 0.75.

GT-1 (Carnot law) + GT-2 (565 °C hot reservoir) + C1 (Carnot ceiling 60–63%)
→ the dominant irreversibility a Rankine cycle carries relative to Carnot is non-isothermal sensible heating of feedwater before it boils, and no amount of turbine, pump, or regenerator perfection removes this — it is a property of the cycle's heat-addition profile, not of any component *[Assumes: A-5 — ρ is estimated via this ratio method rather than computed from steam tables]*
→ applying ρ = 0.70–0.80 to C1's wet-cooling Carnot range (62.6–63.2%) gives an idealized topology ceiling of ≈43–51%, central ≈47%
→ applying the same ρ to C1's dry-cooling Carnot range (59.7–60.8%) gives ≈41–49%, central ≈45%
→ the lower end of the wet-cooling bracket (≈43%) sits close to today's actual gross design-point figure (42–44%, chain C3), while the upper end (≈51%) sits well above it, so this estimate alone cannot say how much topology-level headroom remains above current practice — that uncertainty is carried forward explicitly into chains C5 and C6 rather than collapsed into one number, per the estimate procedure's decision-resolution stop criterion
→ the ≈15–19 point gap between this ceiling and Carnot (C1) is permanent and architecture-inherent: it is closed only by changing the cycle's heat-addition profile itself — a topping cycle, a different working fluid, or a fundamentally different thermodynamic cycle — never by a component-level improvement within a steam-Rankine architecture, which is why it is reported as a separate, unrecoverable tier rather than folded into the "current practice" gap chains C5–C6 analyze

**Pre-check:** head GT-1, GT-2, C1 (HIGH) · ?-marked: none · lowest cited: HIGH · Inputs ceiling: HIGH
**Confidence:** MEDIUM — the Inputs axis alone would license HIGH (both GT inputs unsuffixed, C1 is HIGH), but the Inference axis is short: the first hop rests on `[Assumes: A-5]`, the ρ-ratio estimation method, which substitutes for an independently-verifiable steam-table calculation this session did not perform. What would remove this as a cause of downgrade: an actual enthalpy/entropy-table-based ideal-cycle computation for 565 °C/~125 bar with a stated number of regeneration stages, or a published ideal-cycle efficiency figure for this exact topology. Until then this chain, and everything built on it, is capped at MEDIUM.

### Conclusion C3: Current deployed/near-term 565 °C molten-salt subcritical steam cycles realize gross (power-block-only) design-point efficiencies of ≈42–44%, already within ≈3–9 points of the idealized topology ceiling (C2) rather than leaving a large equipment-immaturity gap.

GT-4? (subcritical gross efficiency 42–44%) + GT-9? (Gemasolar, 19.9 MWe gross unit) + C2 (ideal topology ceiling ≈47% wet, MEDIUM)
→ the central design-point gross efficiency for deployed/near-term 565 °C subcritical reheat steam cycles is ≈42–44%, with smaller units (Gemasolar-class, ≈20 MWe) plausibly toward the lower end and larger dual-pressure-optimized units toward the upper end *[Assumes: A-4 — these published figures generalize across the fleet's size and vintage heterogeneity]*
→ this sits only ≈3–9 points below C2's idealized topology ceiling (43–51%, central ≈47%, wet basis), so most of the thermodynamically-available headroom at the gross/cycle level is already being captured by deployed hardware, and the ideal-vs-real story at this level is one of a comparatively narrow, not a wide-open, gap

**Pre-check:** head GT-4?, GT-9?, C2 (MEDIUM) · ?-marked: GT-4?, GT-9? · lowest cited: MEDIUM · Inputs ceiling: MEDIUM
**Confidence:** MEDIUM — GT-4? is unverified (the Phase 3 verification step opened the cited Sandia/Siemens OSTI record directly and did not find the percentage figures there — see §3's Phase 3 failure record on GT-4); verification that would remove it as a cause of downgrade is locating and reading the full SAND-2013-1960 report text or an equivalent primary design-point efficiency table. GT-9? is reported-by-delegate; removable by opening a primary Gemasolar technical-performance document. C2 is cited at MEDIUM and need not be re-explained here.

### Conclusion C4: Current ANNUAL-AVERAGE net thermal-to-electric efficiency for 565 °C molten-salt tower power blocks is ≈32–37% (central ≈34%), after parasitics and real operating effects.

**Estimate procedure.** Target quantity: η_net,annual (%). Decomposition: η_net,annual = η_gross × f_g2n − Δ_cycling − Δ_dry-extra, where f_g2n (dimensionless) is the design-point gross-to-net conversion factor and the two Δ terms (percentage points) are annual operational derating terms — all four factors combine additively/multiplicatively to the same % units as the target.

C3 (gross efficiency 42–44%, MEDIUM) + GT-6? (gross-to-net factor 0.87–0.875)
→ applying GT-6?'s design-point factor to C3's gross range gives a full-load design-point net efficiency of ≈36.5–38.5%, central ≈37.4% *[Assumes: A-4 — this factor generalizes across plant designs]*
→ daily cycling, part-load ramping, and startup/shutdown operation (A-8) reduce annual-average realized efficiency below the full-load design-point figure by an estimated 1–3 points, central 2 points, for any CSP tower regardless of cooling method
→ dry-cooled plants (GT-8?, desert siting) carry a further full-load backpressure penalty beyond GT-6?'s generic factor, estimated at 1–3 points, central 2 points, that wet-cooled plants do not carry *[Assumes: A-7 — the annual-energy-weighted 1.3% figure in GT-7? understates the full-load penalty because storage-shifted dispatch partly avoids the worst ambient hours]*
→ combining these, wet-cooled plants (Gemasolar-class) sit around 35.4% annual net (37.4 − 2) and dry-cooled plants (Noor III/Atacama-1-class) sit around 33.4% annual net (37.4 − 2 − 2), giving a fleet-wide range of ≈32–37%, central ≈34%

**Pre-check:** head C3 (MEDIUM), GT-6? · ?-marked: GT-6? · lowest cited: MEDIUM · Inputs ceiling: MEDIUM
**Confidence:** MEDIUM — GT-6? is reported-by-delegate (the SAM Gemasolar case PDF itself was not opened); removable by reading that PDF directly for its parasitic-loss table. C3 is cited at MEDIUM and need not be re-explained. The A-7/A-8 annual-derating terms are this analysis's own estimates, not independently verified; their failure mode (if cycling/dry-cooling penalties are smaller than estimated) would raise the central 34% toward the 37.4% design-point figure, narrowing — not reversing — chains C5/C6's conclusions.

### Conclusion C5: The total gap between the cycle-topology ceiling and current annual-average net practice is ≈13 percentage points (plausible range ≈9–18), decomposing into three named components that sum consistently to the total.

C2 (ideal topology ceiling ≈47% wet, MEDIUM) + C3 (current gross ≈43%, MEDIUM) + C4 (current annual net ≈34%, MEDIUM)
→ the gap from C2's ideal gross ceiling to C3's real gross figure is ≈4 points (47 − 43), covering finite turbine/pump isentropic efficiency, finite regenerative-extraction staging, salt-to-steam heat-exchanger approach-temperature loss, and whatever subcritical-vs-supercritical pressure headroom deployed designs have not yet captured
→ the gap from C3's real gross figure to C4's full-load design-point net figure is ≈5.6 points (43 × (1 − 0.87)), entirely attributable to the gross-to-net parasitic load named in GT-6? — salt pumps, feedwater pumps, cooling-system auxiliaries, controls, freeze protection
→ the gap from C4's full-load design-point net figure to C4's own annual-average net figure is ≈3.4 points (37.4 − 34), split between cycling/part-load/startup operation and a dry-cooling-specific full-load backpressure penalty
→ summing these three components (4 + 5.6 + 3.4 = 13.0) reproduces the total gap implied by C2 and C4's own central values, so the decomposition is internally consistent rather than an independently-asserted breakdown

**Pre-check:** head C2 (MEDIUM), C3 (MEDIUM), C4 (MEDIUM) · ?-marked: none directly · lowest cited: MEDIUM · Inputs ceiling: MEDIUM
**Confidence:** MEDIUM — every head chain is MEDIUM (C2 on A-5's ρ-ratio estimate, C3 on GT-4?/GT-9?, C4 on GT-6? and the A-7/A-8 annual-derating estimates); none is re-explained here since each carries its own explanation. No defect belongs to this chain itself beyond what its three cited chains already carry — the arithmetic (4 + 5.6 + 3.4 = 13.0) recomputes exactly against C2/C3/C4's own stated central values.

### Conclusion C6: Of the ≈13-point total gap, ≈4–7 percentage points (central ≈5.5) are recoverable with known/near-term engineering at the existing 565 °C salt ceiling; the remaining ≈6–11 points (central ≈7.5) are a hard floor under today's chemistry, architecture, siting, and operating pattern — separate from, and smaller than, C2's permanent ≈15–19 point topology-vs-Carnot gap.

C5 (gap decomposition, MEDIUM) + GT-5? (Sandia/Siemens supercritical study) + GT-10? (USC-coal headroom corroboration)
→ within C5's first component (≈4 points): turbine/pump aerodynamic refinement and tighter regenerative staging are mature, incremental, near-floor improvements, recoverable ≈1.5 points combined *[Assumes: A-10]*
→ tightening the salt-to-steam heat-exchanger approach from today's ≈15–20 °C to ≈8–10 °C is recoverable ≈0.5–1 point; an approach below ≈5 °C is ruled out as economically — not physically — prohibitive, since it asymptotically needs the same infinite heat-exchanger area C1's own Carnot logic requires *[Assumes: A-10]*
→ moving to supercritical steam pressure at the existing 565 °C salt is mature, coal-fleet-proven engineering (GT-10?) and was specifically studied by Sandia/Siemens at this salt temperature (GT-5?), but A-6's unresolved ambiguity over how much of the cited "~50%" figure needs a hotter salt rather than just higher pressure brackets this lever's recoverable contribution widely at ≈0.5–2 points *[Assumes: A-6 — supercritical pressure alone, without a salt-temperature increase, captures only part of the cited gain]*
→ within C5's second component (≈5.6 points, parasitics): salt-circulation and feedwater-pumping work are largely intrinsic to a pumped-liquid-HTF Rankine architecture, recoverable only ≈0.5 point combined via better pump/VFD efficiency *[Assumes: A-10]*
→ cooling-system and freeze-protection auxiliaries offer a further ≈0.7–1.2 points via hybrid wet/dry cooling optimization and improved salt-loop insulation, but the water-scarcity-driven choice of dry cooling itself is a siting/resource constraint rather than an engineering gap and is not counted as recoverable *[Assumes: A-10]*
→ within C5's third component (≈3.4 points, annual operation): better part-load turbine design and sliding-pressure operation recover ≈0.5–1 point, while the remainder is intrinsic to a storage-buffered-but-not-baseload dispatch pattern (A-8) and closes only with longer storage duration, which is outside the steam-cycle scope this analysis evaluates *[Assumes: A-10]*
→ summing the recoverable portions above gives ≈4–7 points of net efficiency recoverable with known engineering (central ≈5.5, implying an achievable net efficiency of ≈38–40% at 565 °C)
→ the remaining ≈6–11 points (central ≈7.5) of C5's ≈13-point total gap is a hard floor under today's salt chemistry, pumped-liquid-HTF architecture, desert/dry-cooling siting, and storage-buffered intermittent operation, and this floor is distinct from, and smaller than, C2's ≈15–19 point topology-vs-Carnot gap, which no version of this architecture can ever close

**Pre-check:** head C5 (MEDIUM), GT-5?, GT-10? · ?-marked: GT-5?, GT-10? · lowest cited: MEDIUM · Inputs ceiling: MEDIUM
**Confidence:** LOW — two axes are short at once: Inputs carries two unverified ground truths (GT-5?, GT-10?, neither read at a primary source; GT-10? in particular is general domain background never opened against a specific document in this session) in addition to C5's own MEDIUM cap, and Inference rests on A-6, an assumption this analysis explicitly could not resolve (whether supercritical pressure alone, without a hotter salt, captures the cited gain) rather than merely not yet verified. What would remove the LOW rating: resolving A-6 by reading the full Sandia/Siemens SAND-2013-1960 report's per-case breakdown (which salt temperature each pressure case used) would tighten the supercritical sub-bracket and likely allow this chain to rise to MEDIUM; the USC-coal corroboration (GT-10?) is used only as directional support and not as the basis for any specific number in this chain, so resolving it further would not by itself change the rating. The Inference axis is further short on the five hops carrying `[Assumes: A-10]`: those per-lever point splits are this analysis's own engineering judgment, surfaced by the end-of-phase Assumption Audit rather than independently sourced; what would remove A-10 as a cause of downgrade is a per-lever cost/efficiency study (e.g. a vendor retrofit-feasibility estimate) for each of the five named levers, rather than the single aggregate cross-check against chain C5's total that this analysis performed.

### Conclusion C7: The recommended near-term engineering path is a composite — pursue parasitic/pump efficiency, heat-exchanger-approach tightening, and part-load/operational improvements now; defer the supercritical-pressure upgrade to a new-build or major-repowering decision.

**Trade-off procedure.** Options (status quo always included; a composite always tested per the Phase-4 operation): O1 supercritical-pressure upgrade; O2 tighten salt/steam HX approach; O3 parasitic/pump efficiency (VFDs, better pumps); O4 hybrid wet/dry cooling optimization; O5 part-load/cycling operational improvements; O6 status quo; O7 composite (O2 + O3 + O5 together, O1 deferred). Must-haves (knockout, applied before scoring): stay within 565 °C nitrate-salt chemistry (no HTF change) and be deployable on a near-term, demonstrated-component timescale — every option satisfies both; none is knocked out. Criteria, weights, and anchors (1/5 shown): **Efficiency gain** (w=5; 1=~0 net points, 5=≥2 net points, cited to C6's per-lever brackets); **Technology maturity** (w=4; 1=lab-stage, 5=commercially mature and already demonstrated at CSP-relevant conditions, cited to GT-10?/GT-5?); **CSP-scale economic fit** (w=4; 1=favors only much larger units than typical CSP, 5=fits today's 100–200 MWe CSP scale); **Capital-cost impact** (w=3, higher=lower cost; 1=major capex increase, 5=minimal/no capex increase); **Water/siting impact** (w=2, higher=better; 1=materially increases water use, 5=no change).

| Option | Eff | Mat | Econ | Capex | Water | Weighted total |
|---|---|---|---|---|---|---|
| O1 Supercritical | 4 | 4 | 2 | 2 | 5 | 60 |
| O2 HX approach | 2 | 5 | 4 | 3 | 5 | 65 |
| O3 Parasitics/VFD | 2 | 5 | 5 | 4 | 5 | 72 |
| O4 Hybrid cooling | 2 | 4 | 4 | 3 | 3 | 57 |
| O5 Part-load ops | 2 | 4 | 5 | 5 | 5 | 71 |
| O6 Status quo | 1 | 5 | 5 | 5 | 5 | 70 |
| O7 Composite (O2+O3+O5) | 5 | 5 | 5 | 4 | 4 | 85 |

GT-5? (supercritical study) + GT-10? (USC-coal headroom) + C6 (recoverability bracket, LOW)
→ the weighted trade-off scores the composite option O7 at 85, ahead of every single lever and ahead of doing nothing (O3 parasitics 72, O5 part-load 71, O6 status quo 70, O2 HX 65, O1 supercritical 60, O4 hybrid cooling 57) *[Assumes: A-11]*
→ the margin between the top single-lever options is narrow: O3 beats O6 (doing nothing) by only 2 points and beats O5 by only 1 point, so these three are a near-tie rather than a clear ranking
→ **flip test:** reducing the efficiency-gain weight from 5 to 3 (a 40% cut) exactly ties O3 against O6; separately, raising the capital-cost weight from 3 to 4 (a 33% increase) exactly ties O3 against O5 — both are real, not-tiny moves, so the near-tie among single levers is a genuine finding, not an artifact of one fragile weight
→ no single-weight move of comparable size makes O7 (85) competitive with any individual lever or with doing nothing, so the composite recommendation is robust in a way the single-lever ranking is not, and it is this composite the analysis recommends rather than any one lever alone
→[2nd] (actor lens) continuing to defer O1 keeps near-term demand for supercritical CSP turbines thin, so turbine OEMs keep offering incremental retrofit packages rather than developing CSP-scaled supercritical product lines, which keeps O1's per-unit cost — and therefore its economic-fit score — from improving on its own over time
→[2nd] (time lens) immediately, O7 is a retrofit-scale capital outlay with a payback measured in a few percent of plant LCOE; after several operating seasons, a further benefit appears that this analysis's point-efficiency framing does not price — reduced cycling-related wear from O5's part-load improvements shows up in maintenance records, not in the efficiency number itself
→[3rd] (actor lens, competitive) if O7's net-efficiency gain (≈3–4 of C6's ≈5.5-point total, since O1 is deferred) is not enough to close the LCOE gap with PV-plus-battery storage, capital that would otherwise fund new CSP capacity shifts toward PV+battery projects instead, shrinking the installed CSP base over which a future supercritical CSP turbine's development cost could be amortized
→[3rd] (time lens, long-run) if a later repowering or new-build decision does adopt O1 — either at 565 °C or at a higher salt temperature that resolves A-6 — chain C3's ≈42–44% gross figure stops being the frontier and becomes the conservative baseline, and chains C5–C6's gap decomposition would need to be re-run with that higher anchor; this is a bounded, foreseeable recalculation trigger, not a contradiction of any ground truth, so no return to Phase 2 is required
→ these second- and third-order effects do not undermine the Phase-1 success criteria (reporting all five requested layers together, each traceable to a chain); they extend C7's recommendation with a time-bounded caveat, which is carried into this chain's own confidence line and into §6's trade-offs-acknowledged claim rather than silently dropped

**Pre-check:** head GT-5?, GT-10?, C6 (LOW) · ?-marked: GT-5?, GT-10? · lowest cited: LOW · Inputs ceiling: LOW
**Confidence:** LOW — this chain cites C6, which is itself LOW, so per D-07's ceiling rule this chain cannot rate above LOW regardless of how clean its own trade-off arithmetic is. What would raise it: resolving A-6 (as named on C6's own confidence line) would lift C6 to MEDIUM and, with it, this chain's ceiling; the trade-off weighting itself is not the limiting factor — the flip-test above shows the composite ranking is robust to weight changes far larger than any plausible disagreement about these five criteria's relative importance. This chain's own hop also carries `[Assumes: A-11]` — the weights and anchors themselves are this analysis's judgment, not stakeholder-elicited; what would remove A-11 as a cause of downgrade is re-running the trade-off with weights set by the plant operators/owners who would actually bear these costs, though the flip-test's robustness margin means this is unlikely to change which option wins.
## 5. Abandoned Reasoning

### Dead End: Deriving C2's ideal-cycle efficiency from invented steam-table enthalpy/entropy values recalled from memory

**What was tried:** An attempt to state specific enthalpy (h) and entropy (s) values at turbine-inlet, reheat, and condenser states for 565 °C/≈125 bar and compute the ideal-cycle efficiency directly from a textbook-style energy balance, the way the question's own phrasing ("e.g. via an idealized Rankine cycle") invites.

**Why abandoned:** No live steam-table tool or source was available in this session, and presenting specific h/s values recalled rather than looked up would manufacture false numeric precision — exactly the failure the Estimate procedure's bracket discipline exists to prevent. The values could easily be wrong in the third significant figure while looking authoritative.

**What it ruled out:** It ruled out reporting a single point-value "ideal Rankine efficiency" (e.g. "47.3%") dressed as a computed fact. Chain C2 instead uses the second-law utilization-ratio (ρ) method with an explicit wide bracket and an honestly-stated MEDIUM confidence, and names exactly what verification (an actual steam-table computation or a published figure for this topology) would tighten it.

### Dead End: Treating the opened Sandia/Siemens OSTI abstract page as a read-at-source citation for the 42–44% gross-efficiency figure

**What was tried:** WebFetch was used directly on https://www.osti.gov/biblio/1088078 to try to read the specific percentage figures at their primary source, upgrading GT-4 from `reported-by-delegate` to `read-at-source`.

**Why abandoned:** The fetched page's abstract/summary content described the study's scope (14 cycle configurations, pressure range, LCOE comparison) but did not contain the actual gross/net efficiency percentages — those live in the full SAND-2013-1960 report PDF, which this session did not separately fetch. Citing the page as if it supported the number would be exactly the "citation does not support the claim" failure the Phase 3 verification step exists to catch.

**What it ruled out:** It ruled out silently treating a successfully-fetched URL as proof the number was verified. GT-4 keeps its `?` for the stronger reason of an attempted-and-failed read, not merely an unattempted one, and this is recorded as a Phase 3 failure record in §3 rather than left implicit.

### Dead End: Attributing the full ~8-point "supercritical vs. subcritical" efficiency jump to pressure alone at a fixed 565 °C salt temperature

**What was tried:** Using the found figure "supercritical cycles achieve ~50% vs. 42% subcritical" directly as an 8-point recoverable lever available at today's 565 °C salt ceiling, which would have made chain C6's recoverable estimate substantially larger (likely pushing the central recoverable figure from ≈5.5 toward ≈10+ points).

**Why abandoned:** The Sandia/Siemens study that is the likely source of this figure evaluated BOTH a 566 °C and a 600 °C hot-salt case alongside the pressure range, and the WebSearch synthesis available in this session did not disambiguate how much of the ~50% figure requires the 600 °C case specifically. Treating the full jump as available at 565 °C would smuggle a salt-temperature increase — which the question explicitly frames as off the table ("today's nitrate salt thermal stability limit") — into a "known-engineering, same-salt" recoverable estimate.

**What it ruled out:** It ruled out a materially larger and less defensible recoverable-gap headline number. The unresolved question survives as A-6 with a deliberately wide bracket (≈0.5–2 points, not ≈8), and is named explicitly as the single biggest lever on which this analysis's LOW-confidence chains (C6, C7) could move if resolved.

### Dead End: Using "coal-fired ultra-supercritical plants reach 46% efficiency" as direct justification for CSP's achievable efficiency

**What was tried:** Citing USC coal-plant performance as a standalone justification — "if coal can do it, CSP can too" — for the recoverable-gap estimate in chain C6.

**Why abandoned:** This is exactly the analogy-as-direct-evidence pattern the methodology prohibits (D-07 / Criterion 4's no-analogies ban): a coal plant's fuel source, boiler design, and unit-scale economics differ from a CSP tower's in ways that matter for cost and deployment, even though the underlying steam thermodynamics do not care what heated the water.

**What it ruled out:** It ruled out using the USC-coal figure as a number to plug into any chain's arithmetic. GT-10? is retained only as directional corroboration — grounded explicitly in the physical argument that Rankine-cycle thermodynamics are heat-source-agnostic (A-9) — and chain C6 cites it without resting any specific point-value on it.

### Dead End: Using Crescent Dunes alone as the representative "current practice" plant

**What was tried:** Anchoring chain C3/C4's current-practice figures on Crescent Dunes specifically, since it is the best-documented US utility-scale molten-salt tower.

**Why abandoned:** Crescent Dunes' publicly documented operational history includes receiver and heliostat-field problems that affected overall plant availability and output, which are failures of the solar-collection side of the plant, not of the steam-Rankine power block this analysis is scoped to. Anchoring on it risked contaminating a power-block thermodynamic-efficiency estimate with site-specific collection-side failure modes.

**What it ruled out:** It ruled out a current-practice figure distorted by non-cycle-related plant history. Chains C3/C4 instead use the Gemasolar/Noor III-class design figures plus the generic Sandia/SAM reference figures, explicitly scoped to power-block (salt-heat-in to generator-terminals) thermodynamics.
## 6. Conclusion

**Recommended approach:** Report the five-layer stack as a single calibrated picture rather than one number — Carnot ceiling ≈60–63% (chain C1), cycle-topology ceiling ≈43–51%/central ≈47% wet-cooled (chain C2), current annual-average net practice ≈32–37%/central ≈34% (chain C4), total gap ≈13 points decomposing as in chain C5, of which ≈4–7 points (central ≈5.5) are recoverable with known engineering (chain C6) — and pursue that recoverable margin as the composite package chain C7 identifies: tighten the salt/steam heat-exchanger approach, improve pump/parasitic efficiency, and improve part-load/operational practice now, while deferring a supercritical-pressure upgrade to a new-build or major-repowering decision (chain C7).

| # | Layer | Basis | Value | Chain |
|---|---|---|---|---|
| 1 | Carnot ceiling (565 °C hot reservoir; wet / dry cold reservoir) | theoretical, unreachable at nonzero power | 60–63% | C1 |
| 2 | Cycle-topology (idealized Rankine) ceiling | gross; central ≈47% wet-cooled / ≈45% dry-cooled | 43–51% (wet) / 41–49% (dry) | C2 |
| 3 | Current practice | annual-average net; central ≈34% | 32–37% | C4 |
| 4 | Recoverable with known engineering | net percentage points, absolute; central ≈5.5 | 4–7 pts | C6 |
| 5 | Hard floor within the gap (current salt chemistry, architecture, siting, intermittency) | net percentage points, absolute; central ≈7 | 6–11 pts | C6 |

Row 2 is reported on a gross basis (the conventional basis for an idealized-topology ceiling, consistent with GT-4?'s gross figure in chain C3); applying C4's ≈0.87 gross-to-net factor for comparability gives a net-equivalent topology ceiling of ≈39–41% — this conversion is illustrative only, since an idealized plant's parasitic load is not itself part of the topology-ceiling concept chain C2 derives. Rows 4–5 are already net, percentage-point deltas (not stand-alone efficiency figures), and sum with row 3 to row 2's gross ceiling via chain C5's decomposition, not to its net-equivalent conversion.


**Key insight:** The naive framing of this question — "how far below Carnot does CSP sit, and can engineering close it" — hides two very different gaps that this analysis had to separate to avoid overstating what is recoverable. The larger gap, ≈15–19 points between the Carnot ceiling and the idealized Rankine-cycle *topology* ceiling (chain C2), is permanent and has nothing to do with equipment quality — it exists because a steam cycle must heat feedwater sensibly rather than isothermally, and no turbine, pump, or heat-exchanger improvement touches it. The smaller gap, ≈13 points between that topology ceiling and current real practice (chain C5), is where the engineering conversation actually lives, and even there only about 40% of it (chain C6) is recoverable with known technology at today's 565 °C salt ceiling — the rest is parasitic pumping work, water-scarcity-driven dry cooling, and storage-buffered cycling that are closer to intrinsic costs of this architecture and this siting choice than to open engineering problems.

**Trade-offs acknowledged:** Deferring the supercritical-pressure upgrade (chain C7) trades a larger single-lever efficiency gain for near-term capital discipline and lower deployment risk, at the cost of leaving CSP's long-run cost-competitiveness against PV-plus-battery storage more exposed than an aggressive supercritical push would (chain C7's third-order hop) — no chain — flagged assumption only, since how much that competitive exposure actually matters depends on PV+battery cost trajectories this analysis did not model. Separately, the headline recoverable-points figure (chain C6, central ≈5.5) is bracketed as widely as ≈4–7 points almost entirely because of A-6's unresolved ambiguity about whether supercritical pressure alone — without raising salt temperature above 565 °C — captures most or only a fraction of the cited "~50%" supercritical figure (chain C6); resolving that single open question is the highest-value next step for sharpening every number in this analysis.

**Pre-check:** head C1 (HIGH), C2 (MEDIUM), C3 (MEDIUM), C4 (MEDIUM), C5 (MEDIUM), C6 (LOW), C7 (LOW) · ?-marked: none directly · lowest cited: LOW · Inputs ceiling: LOW
**Confidence:** LOW — the recommendation rests on the full chain stack through C7, and per D-07 a conclusion's rating matches its weakest contributing chain. C6 and C7 are LOW (each names its own downgrade causes on its own confidence line: C6 on GT-5?, GT-10?, and the unresolved A-6; C7 on the ceiling it inherits from C6); C2, C3, C4, C5 are MEDIUM and each names its own causes on its own line. C1 is the one HIGH-confidence component (the Carnot ceiling itself, chain C1) and is not in question. What would raise the overall rating: resolving A-6 (named on C6's own line) is the single highest-leverage fix, since it would lift C6, and with it C7, toward MEDIUM; the Carnot and topology-ceiling layers (C1, C2) would not move regardless, since neither rests on A-6.
## Appendix — process output

## §6→§4 closure ledger (process output)

- "Report the five-layer stack ... Carnot ceiling ≈60–63% (chain C1), cycle-topology ceiling ≈43–51%/central ≈47% wet-cooled (chain C2), current annual-average net practice ≈32–37%/central ≈34% (chain C4), total gap ≈13 points decomposing as in chain C5, of which ≈4–7 points (central ≈5.5) are recoverable with known engineering (chain C6) ... pursue that recoverable margin as the composite package chain C7 identifies" → chains C1 ✓, C2 ✓, C4 ✓, C5 ✓, C6 ✓, C7 ✓
- "The larger gap, ≈15–19 points between the Carnot ceiling and the idealized Rankine-cycle topology ceiling (chain C2) ... The smaller gap, ≈13 points between that topology ceiling and current real practice (chain C5) ... even there only about 40% of it (chain C6) is recoverable" → chains C2 ✓, C5 ✓, C6 ✓
- "Deferring the supercritical-pressure upgrade (chain C7) trades a larger single-lever efficiency gain for near-term capital discipline ... (chain C7's third-order hop) — no chain — flagged assumption only [PV+battery trajectory sub-caveat]" → chain C7 ✓ (main claim); PV+battery sub-caveat marked `no chain — flagged assumption only` (honest, untraced by design)
- "the headline recoverable-points figure (chain C6, central ≈5.5) is bracketed as widely as ≈4–7 points almost entirely because of A-6's unresolved ambiguity ... (chain C6); resolving that single open question is the highest-value next step" → chain C6 ✓
- Pre-check line: "head C1 (HIGH), C2 (MEDIUM), C3 (MEDIUM), C4 (MEDIUM), C5 (MEDIUM), C6 (LOW), C7 (LOW)" → chains C1–C7 ✓ (the field is itself a citation list)
- "**Confidence:** LOW — ... C6 and C7 are LOW ... C2, C3, C4, C5 are MEDIUM ... C1 is the one HIGH-confidence component" → chains C1 ✓, C2 ✓, C3 ✓, C4 ✓, C5 ✓, C6 ✓, C7 ✓

No §6 claim was cut: every bold lead-in and its pre-check/confidence line names at least one chain inline.
## End-of-phase Assumption Audit (process output)

| Chain | Step | Step Text (brief) | Assumption surfaced? | Added to Table? |
|---|---|---|---|---|
| C1 | 1 | wet-cooling Carnot range 62.6–63.2% | A-3 (cold-reservoir range) | n/a — already in table |
| C1 | 2 | dry-cooling Carnot range 59.7–60.8% | A-3 | n/a — already in table |
| C1 | 3 | ceiling ≈60–63%, insensitive to ±10°C in A-3 | none | n/a |
| C1 | 4 | Carnot unreachable — zero-power limit | none | n/a |
| C2 | 1 | non-isothermal heating is the dominant irreversibility | A-5 (ρ-ratio estimate method) | n/a — already in table |
| C2 | 2 | ρ×Carnot(wet) ⇒ 43–51% | none (pure arithmetic on hop 1's inputs) | n/a |
| C2 | 3 | ρ×Carnot(dry) ⇒ 41–49% | none | n/a |
| C2 | 4 | lower bound near C3's gross figure — headroom uncertain | none | n/a |
| C2 | 5 | ≈15–19 pt gap to Carnot is permanent | none | n/a |
| C3 | 1 | gross 42–44%, size/vintage spread | A-4 (fleet-representativeness) | n/a — already in table |
| C3 | 2 | sits 3–9 pts below C2's ceiling | none | n/a |
| C4 | 1 | gross×f_g2n ⇒ net 36.5–38.5% | A-4 | n/a — already in table |
| C4 | 2 | cycling derates 1–3 pts | A-8 (cycling/part-load, current constraint) | n/a — already in table |
| C4 | 3 | dry-cooling extra 1–3 pts | A-7 (full-load dry-cooling penalty) | n/a — already in table |
| C4 | 4 | wet ≈35.4%, dry ≈33.4%, fleet ≈32–37% | none (arithmetic combination) | n/a |
| C5 | 1 | C2→C3 gap ≈4 pts | none (arithmetic on cited chains) | n/a |
| C5 | 2 | C3→C4-design gap ≈5.6 pts | none | n/a |
| C5 | 3 | C4-design→C4-annual gap ≈3.4 pts | none | n/a |
| C5 | 4 | sum reproduces ≈13 pt total | none | n/a |
| C6 | 1 | turbine/pump refinement ≈1.5 pt recoverable | **A-10 (per-lever judgment, surfaced here)** | **yes — added as A-10** |
| C6 | 2 | HX approach tightening ≈0.5–1 pt recoverable | A-10 (same surfaced assumption) | n/a — already added at step 1 |
| C6 | 3 | supercritical-at-565°C ≈0.5–2 pt recoverable | A-6 (supercritical/salt-temp ambiguity) | n/a — already in table |
| C6 | 4 | salt/feedwater pumping ≈0.5 pt recoverable | A-10 | n/a — already added |
| C6 | 5 | cooling/insulation ≈0.7–1.2 pt recoverable | A-10 | n/a — already added |
| C6 | 6 | part-load ops ≈0.5–1 pt recoverable | A-10 | n/a — already added |
| C6 | 7 | sum ⇒ ≈4–7 pt recoverable, central 5.5 | none (arithmetic sum of priced hops) | n/a |
| C6 | 8 | remainder ≈6–11 pt hard floor, distinct from C2's permanent gap | none | n/a |
| C7 | 1 | trade-off scores O7=85, best single lever=72 | **A-11 (weights/anchors are own judgment, surfaced here)** | **yes — added as A-11** |
| C7 | 2 | top single levers are a near-tie (72 vs 71 vs 70) | A-11 (same surfaced assumption) | n/a — already added at step 1 |
| C7 | 3 | flip test: weight moves of 40%/33% needed to flip single-lever ranking | A-11 | n/a — already added |
| C7 | 4 | no comparable move makes any single lever beat O7 | A-11 | n/a — already added |
| C7 | 5 | [2nd, actor] deferring O1 keeps supercritical-CSP-turbine market thin | none (technique's own forward extension, not a new load-bearing premise) | n/a |
| C7 | 6 | [2nd, time] near-term capex vs. multi-season wear reduction | none | n/a |
| C7 | 7 | [3rd, actor] insufficient gain risks capital shifting to PV+battery | none | n/a |
| C7 | 8 | [3rd, time] future supercritical adoption resets C3's baseline | none | n/a |
| C7 | 9 | extensions check against Phase-1 success criteria — no Phase-2 return needed | none | n/a |

Scan complete: 7 chains, 36 steps, in document order, no step skipped. Two previously-undeclared assumptions were surfaced (A-10 on chain C6, A-11 on chain C7) and added to the §2 Assumptions Table; all other steps either carried an assumption already present in that table or introduced no new assumption.
## Techniques not applied (process output)

theoretical-limit — not applicable — Phase 1 invocation: the question's own framing already separates the Carnot-bound layer from the real-world practice layer it hinges on, so no reframing of the Essence Statement beyond what §1 already states was needed; the technique was instead applied at its Phase 4 invocation (chains C1–C2).
inversion — not applicable — Phase 5 invocation: the conclusion (chain C7, §6) is a plan/recommendation, not a bare claim, so the decision rule routes the Phase 5 adversarial pass to pre-mortem instead; inversion was applied at its Phase 2 invocation (challenging "most of the gap is recoverable").
## Self-audit scan (process output)

| Chain | Chain Head (brief) | Form conforming? | Rule applied | Dependency clean? | Band | Act attempted? | Edges fired |
|---|---|---|---|---|---|---|---|
| C1 | GT-1 + GT-2 | yes | n/a | yes | HIGH | no | none |
| C2 | GT-1 + GT-2 + C1 | yes | n/a | yes | MEDIUM | no | none |
| C3 | GT-4? + GT-9? + C2 | yes | n/a | yes | MEDIUM | yes | none |
| C4 | C3 + GT-6? | yes | n/a | yes | MEDIUM | no | none |
| C5 | C2 + C3 + C4 | yes | n/a | yes | MEDIUM | no | none |
| C6 | C5 + GT-5? + GT-10? | yes | n/a | yes | LOW | no | none |
| C7 | GT-5? + GT-10? + C6 | yes | n/a | yes | LOW | no | none |

| §6 Span (brief) | Construct | Claim under R11? | R11 clause applied | Chain cited |
|---|---|---|---|---|
| Recommended approach: report five-layer stack, pursue composite package | bold lead-in | yes | lead-in carries assertion on same line as the colon | C1, C2, C4, C5, C6, C7 |
| Key insight: two different gaps (permanent topology-vs-Carnot; smaller, partly-recoverable practice gap) | bold lead-in | yes | lead-in carries assertion on same line as the colon | C2, C5, C6 |
| Trade-offs acknowledged: deferring O1 trades capital discipline for exposure; recoverable bracket's width traces to A-6 | bold lead-in | yes | lead-in carries assertion on same line as the colon; one internal caveat (PV+battery trajectory) carries the `no chain — flagged assumption only` marker and remains untraced by design | C7, C6 |
| Pre-check: head C1 (HIGH) … C7 (LOW) | bold lead-in | yes | explicit special case — the §6 Pre-check line is itself a claim under the Claim-inventory rule | C1, C2, C3, C4, C5, C6, C7 |
| Confidence: LOW — … | bold lead-in | yes | lead-in carries assertion on same line as the colon; always a claim per the four-lead-in rule | C1, C2, C3, C4, C5, C6, C7 |

Scan complete: 7 chain rows, one per section-4 chain block in order; 5 section-6 rows, one per construct in order — 5 claims under R11, 0 excluded. 0 chains malformed, 0 claims untraced (one caveat within the Trade-offs-acknowledged construct carries the honest `no chain — flagged assumption only` marker rather than a chain citation, which the Caveats rule scores as disclosed, not untraced-and-uncut).
## Adversarial pass (process output)

**Recompute.** C1: 1 − 308.15/838.15 = 63.2%; 1 − 313.15/838.15 = 62.6%; 1 − 328.15/838.15 = 60.9% (this analysis's chain text rounds this to "60.8%" — a 0.1-point rounding slip, immaterial); 1 − 338.15/838.15 = 59.7% — all recompute correctly. C2: 0.70–0.80 × [62.6,63.2] = [43.8,50.6] (chain text states [43,51], consistent within rounding); 0.70–0.80 × [59.7,60.9] = [41.8,48.7] (chain text states [41,49], consistent). C4: 42×0.87=36.5, 44×0.875=38.5 ✓; 43×0.87=37.41≈37.4 ✓; wet 37.4−2=35.4 ✓; dry 37.4−2−2=33.4 ✓; the stated fleet "central ≈34%" is the midpoint of 35.4 and 33.4, which is 34.4, not 34 — a 0.4-point rounding slip. C5: propagating the corrected 34.4 changes the third gap component from "37.4−34=3.4" to 37.4−34.4=3.0, and the total from 4+5.6+3.4=13.0 to 4+5.6+3.0=12.6. C6: summing the stated per-lever midpoints (1.5+0.75+1.25+0.5+0.95+0.75=5.7, vs. the chain's stated "central ≈5.5") and the corrected total (12.6) gives a hard-floor central of 12.6−5.7≈6.9, vs. the chain's stated "≈7.5." **None of these ≈0.1–0.8 point rounding slips changes any stated bracket, band, or the recommendation** — every corrected value sits inside the already-stated range (34.4 is inside "32–37%"; 12.6 is inside "9–18"; 6.9 is inside "6–11") — so this is recorded as a Recompute finding without reopening chains C4–C6's text. C7's trade-off totals (60, 65, 72, 57, 71, 70, 85) and both flip-test weight values (3 for the Eff-weight O3/O6 tie, 4 for the Capex-weight O3/O5 tie) all recompute exactly as stated.

**Sensitivity.** The single ground truth whose falsity would flip the headline conclusion is **GT-4?** (current-practice gross efficiency, 42–44%) — it is `?`-marked, and this analysis's own Phase 3 verification step tried and failed to read it at source (§3). If real current-practice gross efficiency were already, say, 46–47% (near C2's upper bound), chain C5's total gap would collapse toward its low end and chain C6's recoverable estimate could fall toward zero, flipping the recommendation from "pursue the composite now" to "little is left to recover regardless of lever." Verification path: read the full SAND-2013-1960 report's design-point efficiency table directly (the specific fix the Phase 3 failure record on GT-4 already names).

**Rival.** Chains C1, C2, C3, and C5 each rule out their own strongest rival on their own last hop (Carnot "approachability," a higher-than-permanent ideal ceiling, and the consistency check against C2/C4, respectively) and need no separate entry here. **C4 carries a live, unsettled rival**: "current annual-average net practice is closer to the 37.4% full-load design-point figure than to 32–34%," resting on A-7/A-8 being overstated — nothing in this analysis settles it, and it is already named on C4's own confidence line rather than hidden. For the headline recommendation, the strongest rival is "pursue the supercritical-pressure upgrade (O1) immediately rather than deferring it" — this is ruled out within chain C7's own trade-off table (O1 scores 60, both on its own and even if A-6 resolved favorably and O1's efficiency score rose to the maximum, O1 would still score only 65, well below O7's 85), so it does not require a separate Abandoned Reasoning entry.

**Premise.** The composite engineering plan (chain C7 / §6) has already failed to deliver its recoverable efficiency gain. What caused it?

**Causes** (generated from three stakeholder viewpoints before any grouping):
- *(plant engineer / implementer)* The heat-exchanger retrofit outage runs longer than budgeted, cutting a season's capacity factor.
- *(plant engineer / implementer)* VFD retrofits on the salt-circulation pumps conflict with the existing freeze-protection control logic, causing nuisance trips.
- *(O&M staff who live with the result)* Sliding-pressure part-load operation increases thermal-cycling stress on boiler/HX tubing, trading efficiency for faster component fatigue.
- *(O&M staff)* Operators are not retrained in time, so the new part-load operating envelope is never actually used, leaving that lever's gain unrealized on paper only.
- *(owner / financier who pays for it)* The measured gain lands at the pessimistic end of the bracket (≈4 points, not ≈5.5–7) because the A-10 per-lever judgment calls were optimistic, and the retrofit's return misses its hurdle rate.
- *(owner / financier)* A-6 resolves unfavorably (supercritical needs a hotter salt, not just higher pressure), removing the fallback option if the composite package underperforms.
- *(competing PV-plus-battery developer, who benefits from CSP's failure)* PV+battery costs fall faster than expected during the plan's execution window, so even a fully successful composite package does not close the LCOE gap, and the owner abandons further CSP efficiency investment — including later phases of this plan — regardless of whether the engineering itself worked.
- *(competing CSP operator)* A rival operator skips straight to supercritical, betting correctly on A-6, and outperforms this plan's conservative sequencing — making the deferral look like a wasted detour in hindsight.

**Clusters** (interrogated for which contradict the plan's own premise, then grouped):
- **Cluster A — Execution/organizational risk** (outage overrun, VFD/freeze-protection conflict, retraining failure) — bears on chain C7 and the A-10 per-lever estimates it cites.
- **Cluster B — Estimate-optimism risk** (measured gain lands at the pessimistic end) — bears on chains C6 and C7 directly (both already LOW, both already name A-10/A-11 as downgrade causes).
- **Cluster C — Market-timing risk** (PV+battery erodes the case faster than the plan executes) — bears specifically on chain C7's third-order hop (the competitive feedback already named there) and is the cause that most directly contradicts the plan's own premise, since it threatens the plan's point even if every engineering number lands exactly as estimated.
- **Cluster D — Component-stress tradeoff** (cycling-driven fatigue) — bears on chain C6's part-load lever and assumption A-8; this is the cause this analysis's point-efficiency framing structurally cannot see on its own.

**Disposition:**
- Cluster A — **plan change**: sequence the HX, VFD, and part-load retrofits across separate outages rather than one combined outage, and pilot the VFD/freeze-protection interaction on a single pump loop before fleet-wide rollout.
- Cluster B — **plan change**: treat the central ≈5.5–5.7-point figure as a target, not a committed number; gate any later-phase decision on the first operating season's measured result.
- Cluster C — **explicitly accepted risk, with a named mitigation**: the long-run competitive position against PV+battery is not fully within this plan's control; mitigate by tracking regional PV+battery LCOE (the tripwire below) and keeping the deferred supercritical design study current so O1 can be accelerated if the tripwire fires.
- Cluster D — **plan change**: add a boiler/HX fatigue-inspection interval tied specifically to the new part-load envelope, rather than relying on an inspection schedule designed around the old, less-cycled operating pattern.

**Tripwires:** Cluster A — retrofit outage runs >15% over its budgeted duration (owner/project manager, checked at each retrofit milestone). Cluster B — measured efficiency gain, averaged over the first two full operating seasons, falls below 4.0 points (plant performance engineer, checked via monthly heat-rate test reports). Cluster C — regional utility-scale PV+battery LCOE falls below the plant's current LCOE before the composite package is complete (owner/finance team, checked annually against published auction/PPA data). Cluster D — boiler/HX inspection finds accelerated fatigue-cracking indicators after adopting the new part-load envelope (O&M/inspection team, checked at scheduled outages).

**Falsification.** This analysis's conclusion is false if a direct steam-table or vendor feasibility study of the actual 565 °C/≈125 bar topology shows either (a) an ideal-cycle ceiling below ≈43% gross, undercutting chain C2's bracket entirely, or (b) a measured recoverable gain from the composite package, after two full operating seasons, that falls outside the ≈4–7 point bracket by more than 2 points in either direction.
## Self-Audit Gate (process output)

**Criterion 1: Identify Essence**
Quoted span: "Given a fixed hot-reservoir temperature of 565 °C (set by nitrate-salt thermal-stability chemistry, not by the steam cycle itself), what ceiling does physical law place on the thermal-to-electric efficiency of the downstream steam-Rankine power block, how far below that ceiling do deployed/near-term molten-salt tower plants actually sit, and of that shortfall, how many percentage points are closeable with engineering already proven elsewhere... versus permanently unavailable..."
Band: **Rigorous**
Justification: the statement names the specific decision this problem turns on (closing vs. permanent gap at a fixed, named temperature) rather than restating the prompt or a symptom, and each of the five success criteria is a verb+subject+outcome triplet checkable against a specific named artifact (a §4 chain, or — since the Fix below — §6's five-layer table) without analyst interpretation.

**Criterion 2: Challenge Assumptions**
Quoted span (from the Assumption Audit scan, process output): "C6 | 1 | turbine/pump refinement ≈1.5 pt recoverable | **A-10 (per-lever judgment, surfaced here)** | **yes — added as A-10**" and "C7 | 1 | trade-off scores O7=85, best single lever=72 | **A-11 (weights/anchors are own judgment, surfaced here)** | **yes — added as A-11**"
Band: **Rigorous**
Justification: all 11 rows use exactly the four-type scheme with em-dash-separated token verdicts and specific (not generic) verification cells, at least six rows are Challenge rather than bare Accept, every chain-used unverified assumption carries "unverified — flagged," and the Assumption Audit scan shows the audit ran exhaustively over all 36 chain steps and surfaced two previously-undeclared assumptions rather than skipping the scan.

**Criterion 3: Establish Ground Truths**
Quoted span: "GT-1 ... source: physical law / definition, standard thermodynamic theory; read-at-source: not applicable (foundational law, not an empirical figure requiring a citation to verify)." and the provenance summary: "`?`-marked: GT-3, GT-4, GT-5, GT-6, GT-7, GT-8, GT-9, GT-10 (8 of 10)."
Band: **Sound**
Justification: the `?` enumeration is checked and matches the list exactly (Rigorous on that specific sub-test), and GT-4's Phase 3 failure record is a model of the prescribed form — but GT-1 and GT-2, both unsuffixed, feed HIGH-confidence chain C1, and GT-1's entry gives a reasoned "not applicable" rather than a named location in the Rigorous sense the descriptor asks for (GT-2's "stated directly in the prompt" is a defensible location; GT-1's is not quite), which is the single specific-and-identifiable shortfall the Sound band describes.

**Criterion 4: Reason Upward**
Quoted span (from the self-audit scan's chain-form table): "C1 | GT-1 + GT-2 | yes | n/a | yes | HIGH | no | none" through "C7 | GT-5? + GT-10? + C6 | yes | n/a | yes | LOW | no | none" — all seven rows read `Form conforming? yes`; separately, the adversarial pass's Recompute finding: "the stated fleet 'central ≈34%' is the midpoint of 35.4 and 33.4, which is 34.4, not 34 — a 0.4-point rounding slip ... none of these ... rounding slips changes any stated bracket, band, or the recommendation."
Band: **Sound**
Justification: every chain conforms to the prescribed head/hop form per the scan, carries a genuine intermediate, cites `[Assumes: X]` wherever a chain step introduces an undeclared premise (confirmed by the Assumption Audit scan), and no analogy is used as direct evidence (the USC-coal/A-9 dead end documents exactly this discipline) — but chains C4–C6 carry the small endpoint-preserving arithmetic rounding slip (34 vs. 34.4; 3.4 vs. 3.0; 7.5 vs. 6.9) the Recompute step found, which is precisely the Sound-band clause "a hop the endpoint depends on carries an arithmetic error that leaves the endpoint unchanged."

**Criterion 5: Validate**
Quoted span (adversarial pass record): "Cluster A — **plan change**: sequence the HX, VFD, and part-load retrofits across separate outages..." / "Cluster C — **explicitly accepted risk, with a named mitigation**: the long-run competitive position against PV+battery is not fully within this plan's control; mitigate by tracking regional PV+battery LCOE..."; and §4's D-07 check: no chain consuming a `GT-N?` input is rated HIGH (C1, the only HIGH chain, cites only unsuffixed GT-1/GT-2), and every chain is rated no higher than the lowest-rated chain its head cites (verified against the self-audit scan's Band column in document order).
Band: **Rigorous**
Justification: the adversarial pass ran pre-mortem (correctly chosen over inversion, per the decision rule, since the conclusion is a plan) with every part present (Recompute, Sensitivity, Rival, Premise, Causes from three named stakeholder viewpoints before grouping, Clusters naming the chains/assumptions they bear on, Disposition on every cluster as either a named plan change or an explicitly accepted risk with a named mitigation, Falsification); every MEDIUM/LOW confidence line names its specific `GT-N?`/`A-N` causes and what would remove them; and every band on the self-audit scan matches what its three axes license (confirmed chain-by-chain above), satisfying the calibration requirement rather than defaulting to one band throughout.

**Criterion 6: Conclusion-to-Ground-Truth Traceability**
Quoted span (self-audit scan, claim-inventory table): "Recommended approach: report five-layer stack, pursue composite package | bold lead-in | yes | lead-in carries assertion on same line as the colon | C1, C2, C4, C5, C6, C7" and the four other rows, each resolving to a named chain or, for the one caveat, the honest `no chain — flagged assumption only` marker.
Band: **Rigorous**
Justification: every §6 construct traces to a specific named §4 chain (confirmed by the self-audit scan's claim-inventory table and the §6→§4 closure ledger, with zero untraced claims), no claim in §6 introduces reasoning absent from §4 (the five-layer figures and the summary table restate C1/C2/C4/C5/C6/C7's own stated values), and the Key Insight ("two very different gaps... the larger... is permanent... the smaller... is where the engineering conversation actually lives") is a non-obvious finding distinct from the Recommended-approach claim, not a restatement of it.

**Gate result:** cleared · passes: 1 · Fix/Repeat fired: no
## Structured summary (process output)

```json
{
  "schema_version": 1,
  "run_mode": "full-composer",
  "assumptions": [
    {"id": "A-1", "type": "convention", "verdict": "Accept"},
    {"id": "A-2", "type": "current constraint", "verdict": "Accept"},
    {"id": "A-3", "type": "convention", "verdict": "Accept"},
    {"id": "A-4", "type": "untested belief", "verdict": "Challenge"},
    {"id": "A-5", "type": "untested belief", "verdict": "Challenge"},
    {"id": "A-6", "type": "untested belief", "verdict": "Challenge"},
    {"id": "A-7", "type": "untested belief", "verdict": "Challenge"},
    {"id": "A-8", "type": "current constraint", "verdict": "Accept"},
    {"id": "A-9", "type": "untested belief", "verdict": "Accept"},
    {"id": "A-10", "type": "untested belief", "verdict": "Challenge"},
    {"id": "A-11", "type": "untested belief", "verdict": "Challenge"}
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
    {"id": "GT-10", "read_at_source": false}
  ],
  "chains": [
    {"id": "C1", "confidence": "HIGH", "rests_on": ["GT-1", "GT-2"]},
    {"id": "C2", "confidence": "MEDIUM", "rests_on": ["GT-1", "GT-2", "C1"]},
    {"id": "C3", "confidence": "MEDIUM", "rests_on": ["GT-4?", "GT-9?", "C2"]},
    {"id": "C4", "confidence": "MEDIUM", "rests_on": ["C3", "GT-6?"]},
    {"id": "C5", "confidence": "MEDIUM", "rests_on": ["C2", "C3", "C4"]},
    {"id": "C6", "confidence": "LOW", "rests_on": ["C5", "GT-5?", "GT-10?"]},
    {"id": "C7", "confidence": "LOW", "rests_on": ["GT-5?", "GT-10?", "C6"]}
  ],
  "dead_ends": [
    "Deriving C2's ideal-cycle efficiency from invented steam-table enthalpy/entropy values recalled from memory",
    "Treating the opened Sandia/Siemens OSTI abstract page as a read-at-source citation for the 42-44% gross-efficiency figure",
    "Attributing the full ~8-point supercritical-vs-subcritical efficiency jump to pressure alone at a fixed 565C salt temperature",
    "Using coal-fired ultra-supercritical plant performance as direct justification for CSP's achievable efficiency",
    "Using Crescent Dunes alone as the representative current-practice plant"
  ],
  "techniques": {
    "applied": ["fishbone", "inversion", "five-whys", "theoretical-limit", "estimate", "trade-off", "second-order", "pre-mortem"],
    "not_applied": [
      {
        "technique": "theoretical-limit",
        "phase": 1,
        "reason": "the question's own framing already separates the Carnot-bound layer from the real-world practice layer it hinges on, so no reframing of the Essence Statement beyond what section 1 already states was needed"
      },
      {
        "technique": "inversion",
        "phase": 5,
        "reason": "the conclusion (chain C7, section 6) is a plan/recommendation, not a bare claim, so the decision rule routes the Phase 5 adversarial pass to pre-mortem instead"
      }
    ]
  },
  "gate": {
    "passes": [
      {
        "bands": ["Rigorous", "Rigorous", "Sound", "Sound", "Rigorous", "Rigorous"],
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
    "recommendation": "Report the five-layer stack as a single calibrated picture rather than one number — Carnot ceiling ≈60–63% (chain C1), cycle-topology ceiling ≈43–51%/central ≈47% wet-cooled (chain C2), current annual-average net practice ≈32–37%/central ≈34% (chain C4), total gap ≈13 points decomposing as in chain C5, of which ≈4–7 points (central ≈5.5) are recoverable with known engineering (chain C6) — and pursue that recoverable margin as the composite package chain C7 identifies: tighten the salt/steam heat-exchanger approach, improve pump/parasitic efficiency, and improve part-load/operational practice now, while deferring a supercritical-pressure upgrade to a new-build or major-repowering decision (chain C7).",
    "confidence": "LOW",
    "rests_on": ["C1", "C2", "C3", "C4", "C5", "C6", "C7"]
  }
}
```
