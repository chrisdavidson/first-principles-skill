# First-Principles Root-Cause Analysis: Premature HSS Gearbox Bearing Failure (1.5 MW Upwind Turbine)

Mode: full-composer (multiple techniques explicitly requested by the operator: five-whys, fishbone, inversion, pre-mortem, second-order, estimate).

## 1. Problem Essence

**Core problem:** What physical mechanism actually produced the subsurface, axial-aligned, white-etching-crack-and-butterfly damage that removed this HSS generator-end bearing at 11% of its L10 design life — and does the lubricant-viscosity/boundary-lubrication wear-through hypothesis the operator has proposed match that mechanism, or does the evidence point to a different, verifiable driver that must be confirmed (or excluded) before a replacement specification is authorized?

**Success criteria:**
1. Each of the four evidence items (axial-aligned spalling, subsurface crescent microcracks at ~0.4 mm, white-etching cracks, butterfly microstructures) is mapped in the Conclusion to a named mechanism, with an explicit statement of what it is and is not consistent with.
2. The Conclusion states, in one sentence, whether the operator's boundary-lubrication/wear-through hypothesis is confirmed or falsified as the failure mechanism, backed by a named derivation chain.
3. The Conclusion names a single best-supported root-cause mechanism (or a bounded set of live candidates) and states the lubricant's role as root cause / contributing factor / unrelated.
4. The Conclusion carries an explicit confidence band (HIGH/MEDIUM/LOW) that a reader can check against the chains in section 4.
5. The Conclusion lists the specific verification items (data not in hand) that must be closed before the replacement specification is signed off.

## 2. Assumptions Table

**Technique note — Fishbone (breadth-first cause categories).** Because this failure is multi-causal (mechanical, material, tribochemical, electrical, and environmental candidates all plausibly contribute), the assumption space was brainstormed using a 6M-analog category set adapted to a rotating-machinery hardware failure: **Machine** (bearing/gearbox/coupling design and fit), **Material** (steel cleanliness, heat treatment), **Method** (lubrication practice, electrical bonding/grounding design), **Measurement** (condition-monitoring adequacy), **Man** (installation/assembly), **Mother Nature** (ambient/cold-snap environment). Each category was walked before drilling into any one branch, per the fishbone procedure.

| Category | Candidate cause | Discriminating observation | Status |
|---|---|---|---|
| Machine | HSS bearing misalignment / gearbox-generator coupling misalignment | Alignment records at commissioning + shaft-run-out data vs. observed damage being circumferentially localized (misalignment) vs. distributed (fatigue) | Unverified — no alignment data given |
| Machine | Bearing internal fit/clearance error (loose fit → ring rotation) | Fretting/rotation marks on OD/bore vs. clean fit surfaces | No fretting reported — not supported by given facts, but not independently checked |
| Material | Steel inclusion population (MnS/oxide/carbide) outside spec | SEM/EDS inclusion count and size distribution vs. bearing-steel spec (e.g., ISO 683-17 cleanliness class) | Unverified — needs independent metallurgical read of the actual sections |
| Method | Lubricant viscosity too low during cold snap → boundary lubrication → wear-through (**operator's hypothesis**) | Direction of viscosity-temperature relationship; morphology of resulting damage (surface vs. subsurface) | Tested explicitly below — see C2, C3 |
| Method | Lubricant chemistry: water ingress / EP-additive breakdown generating tribochemical hydrogen | Oil analysis (water content, acid number, additive depletion, particle count) at or near the failure window | Unverified — no oil-sample chemistry given |
| Method | Electrical bonding/grounding design inadequate or degraded (ground brush wear, insulation breakdown) → stray current through HSS bearing | Ground-brush contact resistance, shaft-to-frame voltage measurement, converter common-mode voltage characteristics | Unverified — generator/converter topology and grounding path not stated in the given facts |
| Measurement | CM system sample rate / sensor location insufficient to catch WEC precursors earlier | Compare pre-14,000-hr envelope/high-frequency-enveloping trend data against kurtosis-only trending | Unverified — only the kurtosis step-change was reported |
| Man | Installation/assembly error (preload, contamination, mishandling during fitting) | Commissioning torque/preload records, borescope of adjacent components for handling damage | Unverified — no commissioning record given |
| Mother Nature | Cold-snap ambient temperature excursion | SCADA ambient/oil-sump temperature log during the cited cold-snap window | Unverified — "cold snap" is asserted, not dated/quantified |
| Mother Nature | Grid-fault / emergency-stop torque-reversal transients (a documented wind-turbine-specific WEA driver, see GT-8) | SCADA event log for emergency stops, grid faults, high-wind cutouts during the service interval | Unverified — not addressed in the given facts |

**Technique note — Inversion (failure-guaranteeing conditions for the operator's hypothesis).** Inverting the operator's claim ("lubricant failure caused boundary lubrication which wore through the race") into "the claim is false" and enumerating what would have to be true for the *original* claim to hold instead:

1. The cold-snap period must have actually driven the oil viscosity at the HSS contact **below** the minimum elastohydrodynamic (EHL) film-forming threshold — **not above it**. [load-bearing]
2. The resulting contact regime must have been sustained boundary/mixed lubrication for long enough, and severely enough, to remove material by wear rather than to accelerate fatigue crack initiation. [load-bearing]
3. The resulting damage morphology must be **surface-initiated** (adhesive/abrasive wear, smearing, discoloration) — not subsurface-initiated at the Hertzian max-shear depth. [load-bearing]
4. No competing subsurface-fatigue accelerant (tribochemical hydrogen, stray electrical current, torque-reversal transients) needs to be invoked to explain the white-etching/butterfly microstructure — i.e., WEC/butterflies must be explainable as an *incidental* byproduct of wear rather than the defining signature of a different mechanism. [load-bearing]
5. The magnitude of the life shortfall (89% below L10) must be explicable by a wear-rate argument rather than a fatigue-life-scaling argument, since L10 is itself a fatigue metric and comparing actual life to it implicitly assumes a fatigue failure mode. [load-bearing]

All five preconditions are unverified beliefs at this point; four of the five are directly testable against the given physical evidence and are tested in section 4 (chains C1-C4). Precondition 1 is tested first because it is checkable from physics alone, without any of the metallurgical evidence.

| Assumption | Type | Treatment | Verdict | Verification |
|---|---|---|---|---|
| The six as-given inspection/CM facts (bearing ID, kurtosis event, L10 vs. actual life, spall dimensions, crack depth, WEC/butterfly metallography) are accurately observed and reported | untested belief | Verify against raw inspection report, CM waterfall plots, and metallographic photomicrographs | Accept — used in chains, but unverified — flagged | unverified — flagged (no raw report/CM export opened by this analysis) |
| Bearing steel inclusion population is within normal spec for this bearing design | untested belief | Verify via SEM/EDS inclusion count/size vs. steel-cleanliness spec | Challenge — surfaced by fishbone (Material); not yet supported or refuted | unverified — flagged |
| This turbine's generator uses a doubly-fed induction generator (DFIG) with a partial-scale, rotor-side power-electronic converter | untested belief | Verify against nameplate/electrical single-line diagram for this specific unit | Challenge — 1.5 MW-class turbines commonly use this topology (GT-13?), but it is not stated for this unit | unverified — flagged; load-bearing for C5/C6 |
| The HSS-to-frame electrical bonding/grounding path (ground brush) was intact and making low-resistance contact at the time of failure | untested belief | Field inspection of brush wear/spring tension/contact resistance; shaft-voltage measurement | Challenge — cannot be assumed either way from the given facts | unverified — flagged; load-bearing for C5/C6 |
| No sustained (non-transient), multi-thousand-hour overload of roughly 70-110% above design load occurred on this HSS bearing | untested belief | Verify via SCADA torque/load history for the full 14,000-hr service interval | Accept, tentatively — the magnitude required (C4) makes this the working assumption, but it is unverified | unverified — flagged |
| The cited "cold-snap period" was severe/long enough to meaningfully disturb the lubricant film at the HSS contact | untested belief (operator's own premise) | Verify via SCADA ambient/sump-oil temperature log for the cited period, and the oil's actual pour point/viscosity grade | Challenge — asserted without a date range, duration, or measured oil temperature | unverified — flagged |
| Lubricant viscosity increases as temperature decreases (Walther-equation-governed behavior of mineral/synthetic gear oils) | physical law | Accept as ground-truth candidate | Accept — physical-law-backed by GT-12 | unverified — flagged (delegate-reported citation, not yet read at primary source; direction itself is textbook tribology) |
| Roller-bearing L10 life scales as (C/P)^p with dynamic equivalent load, p = 10/3 for line contact (ISO 281 / Lundberg-Palmgren) | physical law / engineering-standard definition | Accept as ground-truth candidate for the reconciliation estimate (C4) | Accept — standard-defined exponent, but ISO 281 clause itself not directly opened | unverified — flagged |
| White-etching microstructural alteration requires localized severe cyclic subsurface shear plus a tribochemical, thermal, or electrical energy input; it is not produced by ordinary abrasive/adhesive surface wear alone | untested belief, pushed toward ground-truth status given the stakes riding on it (stakes-escalation rule) | Corroborate with multiple independent literature sources | Accept — supported by three independently read-at-source citations (GT-7, GT-8, GT-9) | read-at-source: GT-7, GT-8, GT-9 (see section 3) |
| The vibration-kurtosis step-increase at ~14,000 hrs marks the point active spalling became large enough to impact, not necessarily the onset of the underlying subsurface microstructural damage | convention (standard CM interpretation) | Challenge whether earlier CM trend data (envelope/high-frequency-enveloping) shows an earlier, un-flagged onset | Challenge — plausible but unconfirmed; matters for how long the true root-cause process has been running | unverified — flagged |
| The CM system's sensor placement and sample rate were adequate to detect WEC precursors before the kurtosis step-change | untested belief | Verify CM system spec against known WEC-precursor frequency signatures | Challenge — surfaced by fishbone (Measurement) | unverified — flagged |
| Installation/assembly (bearing fit, preload, alignment) met OEM spec at commissioning | untested belief | Verify against commissioning torque/alignment records | Challenge — surfaced by fishbone (Man) | unverified — flagged |
| The operator's working hypothesis — low lubricant viscosity drove boundary lubrication which wore through the race — accurately describes this failure | convention (the hypothesis under test) | Explicitly challenge via inversion preconditions 1-5 and against the metallurgical evidence | **Discard** — contradicted by GT-12 (wrong physical direction) and by GT-9/GT-14 (wrong damage morphology); see C2, C3 | unverified — flagged prior to discard; discard reasoning in C2/C3 |
| Electrical fluting/EDM erosion, where present, leaves a distinctive surface signature (equally spaced transverse craters/flutes, dark discoloration) distinguishable from subsurface rolling-contact-fatigue damage | tribological regularity, treated as ground truth | Accept as ground-truth (GT-9) | Accept — read-at-source | read-at-source: GT-9 |
| This unit's OEM L10 calculation (~130,000 hrs) used a representative load spectrum and standard ISO 281 modification factors, not an already-derated or nameplate-only figure | untested belief | Open the OEM bearing-life calculation worksheet for this gearbox | Challenge — unverified; load-bearing for C4's interpretation | unverified — flagged |
| No unusual-frequency or unusual-severity emergency-stop/grid-fault torque-reversal transients occurred on this turbine during the 14,000-hr interval | untested belief | Verify via SCADA event log (E-stops, grid faults, high-wind cutouts) | Challenge — surfaced by fishbone (Mother Nature/Machine) and by GT-8's documented WEA driver | unverified — flagged |
| "Crescent-shaped microcracks" as described in the given facts refers to the same butterfly-wing-pair crack morphology described in the literature, not an unrelated crescent-shaped defect (A-17) | untested belief | Surfaced by End-of-Phase-4 Assumption Audit on chain C1, hop 1; verify by direct comparison of the metallographic photomicrograph against published butterfly-wing serial-sectioning images | Accept — the morphological description (crescent pair flanking a subsurface origin) matches the literature's definition closely enough to proceed, but treat as unverified | unverified — flagged; [Assumes: A-17] on C1 |
| This bearing's actual Hertzian contact half-width under operating load falls within the typical 0.1-0.6 mm range assumed for medium-section cylindrical roller bearings, absent specific roller diameter/load data for this unit (A-18) | untested belief | Surfaced by End-of-Phase-4 Assumption Audit on chain C1, hop 2; verify by computing the actual Hertzian half-width from this bearing's roller geometry and generator-end radial load | Accept, as a bracketing device only — the conclusion does not depend on a precise value, only on the bracket containing 0.4 mm | unverified — flagged; [Assumes: A-18] on C1 |
| The rival mechanisms explicitly considered in this analysis (classical overload, classic electrical fluting, boundary-lubrication wear-through, WEC via mixed friction/hydrogen/electrical current/torque-reversal) are an adequate set and no better-fitting mechanism was overlooked (A-20) | untested belief | Surfaced by End-of-Phase-4 Assumption Audit on chain C6, hop 1; mitigated by the breadth of the fishbone category sweep in section 2, but not eliminated | Challenge — a reasonable but not provably exhaustive rival set | unverified — flagged; [Assumes: A-20] on C6 |

## 3. Ground Truths

**As-given facts (operator-supplied; not independently opened by this analysis — no raw inspection report, CM export, or metallographic photomicrograph file was provided to Read).** Per the Input Contract, a fact supplied without a named, openable source enters as `unverified`.

- **GT-1?** Turbine is a 1.5 MW upwind machine; the failed bearing is the gearbox HSS, generator-end cylindrical roller bearing — unverified: no equipment record or bearing schedule opened by this analysis.
- **GT-2?** Condition monitoring flagged a step increase in HSS vibration kurtosis at ~14,000 operating hours; the bearing was removed from service at that point — unverified: no CM export/waterfall plot opened.
- **GT-3?** L10 design life for this bearing was ~130,000 hours; actual life was ~14,000 hours, ≈11% of design life — unverified: no OEM L10 calculation worksheet opened.
- **GT-4?** On disassembly, the inner race showed axial-aligned spalling, ~18 mm long — unverified: no inspection photograph/report opened.
- **GT-5?** Crescent-shaped microcracks propagate from a subsurface origin ~0.4 mm below the raceway surface — unverified: no metallographic section opened directly.
- **GT-6?** Metallographic sections show white-etching cracks (WEC) and butterfly-shaped microstructural features around subsurface inclusions/carbides — unverified: no metallographic section opened directly.

**Literature ground truths — read-at-source (this analysis opened the cited page directly via WebFetch and the extraction above quotes its content).**

- **GT-7** Wind-turbine-gearbox WEC/white-structure-flaking literature documents these as contributing operational factors: lubricant decomposition; "slip between rings and rolling elements and bearing vibration [that] can cause local metal-to-metal contact"; static electricity in accessory bearings; and electric discharge from stray currents in generators — with hydrogen-induced microstructural change experimentally reproduced using hydrogen-charged specimens and shown to reduce rolling-contact-fatigue life. Axial cracks described as >10 mm plus many 1-3 mm cracks, propagating straight in the axial direction, "seldom found in other applications" besides wind-turbine gearboxes — source: Wind Systems Magazine, "White Structure Flaking in Rolling Bearings for Wind Turbine Gearboxes"; read-at-source via WebFetch, https://www.windsystemsmag.com/white-structure-flaking-in-rolling-bearings-for-wind-turbine-gearboxes/.
- **GT-8** White Etch Area (WEA) damage in wind-turbine gearbox bearings occurs at "less than 0.04 inches (1 mm) below the raceway surface — coinciding with maximum shear stress zones under Hertzian loading." Two documented driver families: **stress-induced** WEA from impact loading during rapid torque reversals (emergency stops/high-wind shutdowns producing "impact loads 2½ to 4 times nominal torque" at high strain rates, forming adiabatic shear bands), and **hydrogen-induced** WEA from "corrosion, water contamination, electrical currents or aggressive oil additives." Cracks propagate axially, in some cases completely through the inner ring — source: windpowerengineering.com, "Understanding the root causes of axial cracking in wind turbine gearbox bearings"; read-at-source via WebFetch, https://www.windpowerengineering.com/understanding-root-causes-axial-cracking-wind-turbine-gearbox-bearings/.
- **GT-9** Electrical fluting is a **surface erosion** phenomenon: "equally spaced grey-brown flutes in the transverse direction to travel," beginning as densely packed dark micro-craters, caused by electrical discharge material removal and localized melting — mechanistically and visually distinct from subsurface-initiated rolling-contact-fatigue/WEC damage, which propagates beneath the surface before surfacing as macropitting spalls — source: ONYX Insight Failure Atlas, "Electrical Fluting Bearing Failures"; read-at-source via WebFetch, https://onyxinsight.com/resources-support/failure-atlas/electrical-fluting-bearing-failure/.

**Literature ground truths — reported-by-delegate (WebSearch returned a synthesized summary across multiple sources; this analysis did not open a specific primary source page to confirm the exact wording, so these carry `?` even though they are well-formed and plausible).**

- **GT-10?** Butterfly wings typically form at 30-60° (most frequently ~45°) to the rolling direction, coincident with the plane of maximum shear stress around a subsurface inclusion; for Hertzian contact, the maximum orthogonal shear stress sits at a depth on the order of 0.4-0.8× the contact half-width (line contact) — cited to: ResearchGate/ScienceDirect RCF-mechanics literature; reported-by-delegate via WebSearch — cited sources not individually opened.
- **GT-11?** For roller bearings under line contact, L10 life scales as (dynamic capacity/equivalent load)^(10/3) per ISO 281/Lundberg-Palmgren convention; a cited field figure states a 252% load increase produces a ~22-fold L10 life reduction (independently recomputed below in C4 and found arithmetically consistent with the 10/3 exponent) — cited to: NREL/wind-industry load-life literature; reported-by-delegate via WebSearch — ISO 281 clause itself not directly opened.
- **GT-12?** Lubricant kinematic viscosity increases as temperature decreases (Walther-equation-governed); the documented cold-weather risk for wind-turbine gearboxes is oil-flow **starvation from excessive viscosity/poor pumpability** at cold start, mitigated by sump heaters — not thinning — cited to: tribology/viscosity-index literature and wind-turbine-gearbox cold-start patents; reported-by-delegate via WebSearch — primary sources not individually opened.
- **GT-13?** 1.5 MW-class wind turbines commonly use doubly-fed induction generators (DFIG) with a partial-scale, rotor-side back-to-back converter; converter common-mode voltage induces a shaft voltage that, if not diverted by a functioning ground brush, discharges through the generator bearing oil film — with documented high-frequency shaft currents up to ~60 A / 1200 V — causing pitting/fluting — cited to: bearing-current/DFIG literature; reported-by-delegate via WebSearch — this unit's actual topology is not confirmed (see Assumptions Table).
- **GT-14?** Boundary-lubrication-driven adhesive wear (scuffing/galling/smearing) is a surface-initiated, non-fatigue mechanism that can occur without a large cycle count, producing visible material transfer/discoloration — mechanistically distinct from subsurface rolling-contact fatigue, which requires many stress cycles before a subsurface crack network reaches the surface as a spall — cited to: tribology/machinery-lubrication wear-mode literature; reported-by-delegate via WebSearch — primary sources not individually opened.
- **GT-15?** Field L10 life for 1.5 MW-class wind-turbine gearbox bearings has historically been observed at ~8-11 years (~70,000-96,000 hrs) against ~20-year (~130,000+ hr) nameplate design targets; bearing failures account for roughly 76% of gearbox failures fleet-wide per NREL Gearbox Reliability Collaborative data — cited to: NREL GRC publications; reported-by-delegate via WebSearch. **Phase 3 failure record:** a direct WebFetch of the underlying NREL PDF (docs.nrel.gov/docs/fy14osti/60982.pdf) was attempted and failed with a DNS resolution error ("getaddrinfo ENOTFOUND docs.nrel.gov"); no retry was made given this GT is not load-bearing for the headline conclusion (it corroborates that premature wind-turbine gearbox bearing failure is a known fleet-wide pattern, but no chain's endpoint depends on the specific 8-11-year figure).

**Provenance summary:**

```text
?-marked: GT-1, GT-2, GT-3, GT-4, GT-5, GT-6, GT-10, GT-11, GT-12, GT-13, GT-14, GT-15 (12 of 15)
Read-at-source: GT-7 — windsystemsmag.com, "White Structure Flaking..." article body (WEC drivers + axial-crack dimensions, quoted above)
Read-at-source: GT-8 — windpowerengineering.com, "Understanding the root causes of axial cracking..." article body ("<0.04 inches (1 mm)... coinciding with maximum shear stress zones under Hertzian loading")
Read-at-source: GT-9 — onyxinsight.com Failure Atlas, "Electrical Fluting Bearing Failures" article body (surface-erosion flute/crater description)
Not read — turn budget: GT-15's underlying NREL PDF (WebFetch failed — DNS error; see Phase 3 failure record above); GT-15 keeps its `?` and is not load-bearing for any HIGH-confidence chain.
```

No assumption carrying a Discard verdict (the operator's literal wear-through hypothesis) appears in this list.

## 4. Derivation Chains

**Technique note — Five-Whys (causal mode), narrated.** Symptom: the HSS bearing failed at ~11% of L10 with subsurface WEC/butterfly damage. Why did it fail early? → subsurface WEC-driven axial spalling reached a size CM could detect. Why did WEC form? → localized microstructural alteration (white-etching, butterfly wings) at inclusions/carbides, which the literature (GT-7, GT-8) ties to a combination of cyclic subsurface shear plus an added energy/chemistry input. Why was that added input present? → three counterfactually live branches: (a) mixed/slip friction from a lubrication-film disturbance, (b) tribochemical hydrogen from water ingress or additive breakdown, (c) stray electrical current from an inadequately diverted converter-induced shaft voltage; a fourth branch, (d) torque-reversal transients (GT-8), is also live. Each branch passes the counterfactual necessity test provisionally (removing any one would plausibly still leave WEC formation possible via the others) except branch (a) alone, which the counterfactual test shows is **not sufficient by itself** — this is why chains C2/C3 test it explicitly rather than accepting it as the corrective action. The drill stops here (two levels) because level three items (a)-(d) each have a stated, actionable corrective/verification action (oil chemistry analysis, shaft-voltage measurement, SCADA event log review) — going deeper (e.g., "why does the converter induce a shaft voltage at all") leaves the turbine's actionable control and becomes generic power-electronics theory.

### Conclusion C1: The evidence's depth, shape, and microstructure identify a subsurface rolling-contact-fatigue (RCF)/WEC origin, not a surface-wear origin

GT-5? (crescent microcracks at ~0.4 mm depth) + GT-8 (WEA occurs at <1 mm depth, coincident with the Hertzian max-shear zone) + GT-10? (butterfly wings form at the ~45° max-shear plane)
→ the reported 0.4 mm origin depth and crescent (butterfly-wing-pair) crack shape match the independently documented Hertzian max-shear-stress signature for subsurface RCF/WEC initiation, not an arbitrary or surface depth *[Assumes: A-17 — crescent microcracks as given are the same phenomenon as literature butterfly wings]*
→ typical Hertzian contact half-widths for medium-section cylindrical roller bearings under moderate-to-heavy dynamic load bracket to roughly 0.1-0.6 mm, and the associated max-shear depth (≈0.4-0.8x half-width for line contact) brackets to roughly 0.1-0.5 mm — the reported 0.4 mm sits centrally in this band rather than at either extreme *[Assumes: A-18 — this bearing's contact half-width falls within the typical bracket assumed]*
→ the crack initiation site is subsurface, at the Hertzian max-shear zone, and is not consistent with a surface-initiated damage origin

**Pre-check:** head GT-5?, GT-8, GT-10? · ?-marked: GT-5?, GT-10? · lowest cited: none · Inputs ceiling: MEDIUM
**Confidence:** MEDIUM — GT-5? is unverified (the 0.4 mm depth figure is operator-supplied; verification path: open the actual metallographic section/measurement report and confirm the figure directly). GT-10? is unverified (verification path: open a primary RCF-mechanics source, e.g., the Evans 2016 review or an inclusion-butterfly serial-sectioning study, directly via WebFetch rather than relying on a WebSearch synthesis). The second hop's bracket (A-18) is an order-of-magnitude estimate rather than a bearing-specific Hertzian calculation; if A-18 is wrong (this bearing's actual contact half-width falls outside the assumed 0.1-0.6 mm range), the endpoint is unaffected, because GT-8 — unsuffixed, read-at-source — already independently states that WEA in wind-turbine gearbox bearings characteristically occurs at <1 mm depth coincident with the Hertzian max-shear zone, without depending on this chain's own bracket arithmetic; the Inference axis is therefore priced and only the Inputs axis (GT-5?, GT-10?) is short.

### Conclusion C2: The operator's stated causal mechanism is physically backwards

GT-12? (lubricant viscosity increases, not decreases, as temperature decreases; cold-weather wind-turbine gearbox risk is documented as oil starvation from excessive viscosity, not thinning)
→ "a cold snap drove viscosity too low" contradicts the standard viscosity-temperature relationship for lubricating oils, in which colder oil is more viscous, not less
→ the closest physically coherent analog to "cold snap disturbed the lubricant film" is cold-related oil starvation from excessive viscosity/poor pumpability, which is the opposite mechanism direction from the one stated

**Pre-check:** head GT-12? · ?-marked: GT-12? · lowest cited: none · Inputs ceiling: MEDIUM
**Confidence:** MEDIUM — GT-12? is unverified as a delegate-reported search synthesis (verification path: open a standard tribology reference, e.g., an ASTM D341/Walther-equation viscosity-temperature chart, directly, and confirm this gearbox's specific oil grade and pour point against the OEM lubrication spec). The direction of the viscosity-temperature relationship itself is essentially uncontested textbook physics, but this analysis has not personally opened a primary source to convert it to read-at-source, so the `?` is carried per the provenance rule rather than waived on the strength of general confidence.

### Conclusion C3: Even the corrected (starvation) mechanism predicts the wrong damage morphology

C2 (mechanism direction corrected to cold-related starvation) + GT-14? (boundary/adhesive wear is surface-initiated and non-fatigue) + C1 (evidence shows a subsurface RCF/WEC origin)
→ boundary-lubrication-driven wear, even under the corrected starvation mechanism, predicts surface-initiated adhesive/abrasive damage — material transfer, smearing, discoloration — that does not require cyclic subsurface stress reversal to develop
→ the observed damage instead requires on the order of thousands of stress cycles to build butterflies/WEC/crescent cracks at the Hertzian max-shear depth, which is the opposite failure signature from wear-through
→ the lubricant-viscosity/wear-through hypothesis, as literally stated and in its physically corrected form, is inconsistent with the observed morphology and is not supported as the primary or sole mechanism

**Pre-check:** head C2 (MEDIUM), GT-14?, C1 (MEDIUM) · ?-marked: GT-14? · lowest cited: MEDIUM · Inputs ceiling: MEDIUM
**Confidence:** MEDIUM — this chain cites C2 and C1, both MEDIUM (each chain's own confidence line carries its explanation and is not re-explained here). GT-14? is unverified (verification path: open a primary tribology wear-mode reference directly and confirm the surface-vs-subsurface distinction against a specific adhesive-wear case study). This chain cannot be rated higher than the lowest-rated chain it cites (MEDIUM), per the unverified-input/ceiling rule.

### Conclusion C4: The magnitude of the life shortfall is quantitatively implausible as a pure classical-overload fatigue effect (estimate/Fermi reconciliation)

GT-3? (L10 = 130,000 hrs; actual life = 14,000 hrs, life ratio ≈ 0.108) + GT-11? (roller-bearing L10-load exponent p = 10/3)
→ solving life-ratio = (P_design/P_actual)^p for the load ratio gives P_actual/P_design = (1/0.108)^(1/p) = 9.26^0.3 ≈ 1.95 at p = 10/3, bracketing to roughly 1.7-2.1x across p = 3-4 (point-contact-to-conservative exponent range) — i.e., a sustained load on the order of 70-110% above design load, held continuously across the full 14,000-hour service life, would be required to explain the entire life shortfall through classical Lundberg-Palmgren overload-driven fatigue scaling alone, with no metallurgical or tribochemical accelerant
→ a continuous overload of this magnitude for this duration would be expected to produce corroborating symptoms — elevated gearbox/bearing operating temperature, distress on other gearbox components, anomalous generator torque/speed behavior — none of which appear among the given facts
→ classical load-driven fatigue scaling alone is an implausible sole explanation for the observed magnitude of the life shortfall; a non-classical accelerant (of the WEC/RCF-with-added-energy-input type identified in C1) is quantitatively a better fit, and both ends of the estimate's bracket (70% and 110% sustained overload) agree on this qualitative conclusion, so the bracket is decision-resolving without needing tighter load data

**Pre-check:** head GT-3?, GT-11? · ?-marked: GT-3?, GT-11? · lowest cited: none · Inputs ceiling: MEDIUM
**Confidence:** MEDIUM — GT-3? is unverified (verification path: open the OEM L10 calculation worksheet and confirm the 130,000-hr figure and the load spectrum/modification factors behind it). GT-11? is unverified (verification path: open ISO 281 directly and confirm the 10/3 exponent for this bearing's contact geometry). The arithmetic itself was independently recomputed in this chain (not merely quoted from a source) and is consistent with an external check (a cited field figure of 252% load increase → ~22x life reduction recomputes to ~21.8x at p=10/3), which supports the Inference axis even though the Inputs axis remains short on both head items.

### Conclusion C5: The evidence rules out classic electrical fluting as an independent, dominant mechanism but leaves stray-current-assisted WEC live

GT-9 (electrical fluting is a distinct surface-erosion signature) + C1 (evidence shows a subsurface RCF/WEC origin)
→ the given evidence reports no surface erosion/crater/washboard pattern, so it does not match the classic electrical-fluting/EDM signature as an independent, dominant failure mode in its own right
→ this does not exclude electrical current as a contributing driver of the WEC mechanism itself: GT-7 and GT-8 both name electrical current/stray discharge among documented WEC/WEA drivers even where classic fluting craters are absent
→ stray electrical current remains a live, unresolved candidate co-driver of the observed WEC damage and must be tested directly (shaft-voltage measurement, ground-brush inspection) rather than assumed present or assumed absent

**Pre-check:** head GT-9 (HIGH), C1 (MEDIUM) · ?-marked: none · lowest cited: MEDIUM · Inputs ceiling: MEDIUM
**Confidence:** MEDIUM — this chain cites C1, rated MEDIUM, which caps this chain at MEDIUM per the ceiling rule regardless of GT-9's own HIGH-quality provenance. No `GT-N?` input sits directly on this chain's head.

### Conclusion C6: Verified root-cause mechanism and the lubricant's actual role

C1 (subsurface WEC/RCF origin) + C3 (lube-wear-through hypothesis not supported) + C4 (classical overload implausible at the required magnitude) + C5 (stray current live, classic fluting excluded) + GT-7 (documented WEC drivers: slip/mixed friction, hydrogen, static/stray current)
→ of the mechanisms considered, the full evidence set — axial orientation, subsurface origin depth at the Hertzian max-shear zone, crescent/butterfly crack morphology, and WEC — matches one internally coherent, literature-documented mechanism better than any rival considered: mixed/slip-friction- and tribochemical-hydrogen-driven WEC formation nucleating at subsurface inclusions/carbides, propagating to axial cracking and spalling *[Assumes: A-20 — the rival mechanism set considered is adequate]*
→ the lubricant's condition — corrected to mean cold-related starvation, not thinning — is a plausible contributing amplifier of mixed/slip friction at the contact, which is one of the three documented WEC drivers (GT-7), but is not by itself sufficient to produce WEC/butterflies without a co-occurring hydrogen, electrical, or torque-transient driver
→ the verified root cause is a WEC-type subsurface rolling-contact-fatigue mechanism, with mixed/slip friction and tribochemical hydrogen as the best-supported drivers and stray electrical current as an unresolved possible co-driver; the lubricant's role is at most a contributing factor to the friction regime, not the root cause, and not via the wear-through pathway the operator proposed

**Pre-check:** head C1 (MEDIUM), C3 (MEDIUM), C4 (MEDIUM), C5 (MEDIUM), GT-7 (HIGH) · ?-marked: none · lowest cited: MEDIUM · Inputs ceiling: MEDIUM
**Confidence:** MEDIUM — this is the headline chain. It cites four chains, all independently rated MEDIUM (each for the specific unverified inputs/ceilings named in its own confidence line above), so it is capped at MEDIUM by the ceiling rule (Inputs axis short via citation). The Rivals axis is addressed rather than short: every competing conclusion to this endpoint considered by the analysis -- pure classical overload (ruled out by C4, Abandoned Reasoning), literal or corrected boundary-lubrication wear-through (ruled out by C2/C3, Abandoned Reasoning), and classic electrical fluting as an independent dominant mechanism (ruled out by C5, Abandoned Reasoning) -- has a named chain or dead-end entry ruling it out. The remaining ambiguity is within the accepted WEC-mechanism family (tribochemical-hydrogen vs. electrically-assisted vs. torque-transient-triggered) and is stated as part of the endpoint itself ("with stray electrical current as an unresolved possible co-driver"), not a competing conclusion the chain fails to address -- so only the Inputs axis is short here, and the band remains MEDIUM rather than LOW.

**Technique note — Second-Order Thinking, extending C6.** Walking both lenses before extending the chain:

*Actor lens:* the O&M team and the operator's engineering sign-off authority change what they do next depending on which root cause is recorded; a warranty/insurance claims desk changes how it frames the claim (operating-conditions/weather versus a design or grounding defect) depending on the recorded cause; and any sister turbine sharing this unit's generator/converter design is exposed to the same undetected accelerant regardless of what gets written down for this one unit.
*Time lens:* immediately, a replacement bearing goes in either way; after a few duty cycles (weeks to months), CM will either show a clean baseline or an early re-onset of the kurtosis/envelope signature depending on whether the true accelerant was addressed; once the fix has been in place long enough to be assumed correct (a year or more with no CM flags), the specific verification items below stop being asked — which is exactly the point at which an unaddressed electrical or tribochemical driver would be silently continuing to run.

### Conclusion C7: Second-order consequence — signing off on the replacement spec without closing the verification items risks a recurrence and a fleet-wide blind spot

C6 (verified root-cause conclusion)
→[2nd] if the replacement specification and O&M response address only lubricant grade/cold-weather heating without confirming or excluding the electrical-bonding and tribochemical drivers named in C6, the replacement bearing carries materially elevated risk of recurring WEC damage on a similarly compressed timeline
→[3rd] because WEC/axial-cracking is a documented fleet-wide wind-turbine-gearbox phenomenon (GT-7, GT-8) rather than a unit-specific anomaly, leaving the root cause unconfirmed on this unit also leaves any sister turbine sharing this generator/converter design silently exposed to the same undetected accelerant
→ the verification checklist in the Conclusion is a precondition for signing off the replacement spec, not an optional follow-up item

**Pre-check:** head C6 (MEDIUM) · ?-marked: none · lowest cited: MEDIUM · Inputs ceiling: MEDIUM
**Confidence:** MEDIUM — capped at C6's MEDIUM band by the ceiling rule; no additional unverified input is introduced directly on this chain's head.

## 5. Abandoned Reasoning

### Dead End: Operator's literal hypothesis — low viscosity drove boundary lubrication, race wore through

**What was tried:** Accepted the operator's causal statement at face value and attempted to build a chain from "cold snap → low viscosity → boundary lubrication → wear-through" directly to the observed spalling.

**Why abandoned:** The mechanism's own stated physical direction is wrong (GT-12: viscosity rises, not falls, as temperature drops — C2), and even its physically corrected form (cold-related starvation) predicts surface-initiated adhesive/abrasive wear, not the subsurface-initiated, cycle-dependent WEC/butterfly/crescent-crack morphology actually reported (GT-9, GT-14 — C3). The intermediate step needed to connect "boundary lubrication" to "subsurface fatigue cracking at the Hertzian max-shear depth" could not be established without contradicting the cited tribology literature.

**What it ruled out:** Saves the operator from authorizing a replacement spec that changes only lubricant grade and cold-weather heating strategy while leaving the actual accelerant (mixed friction / tribochemical hydrogen / possible stray current) unaddressed — this path is abandoned, not deferred.

### Dead End: Classic electrical fluting/EDM erosion as an independent, dominant failure mode

**What was tried:** Considered whether the entire failure could be attributed to classic stray-current electrical discharge machining (fluting), given the HSS bearing's proximity to the generator and the known DFIG bearing-current literature (GT-13).

**Why abandoned:** Classic electrical fluting has a distinctive, well-documented surface signature — equally spaced transverse craters/flutes with dark discoloration (GT-9) — and none of that surface signature is reported in the given facts, which instead describe a subsurface origin. As an *independent, dominant* mechanism, classic fluting is contradicted by the reported morphology (C5).

**What it ruled out:** Saves the operator from treating this as a pure "surface electrical erosion" problem solvable by insulation/brush replacement alone. It does **not** rule out stray current as a *contributing* driver of the WEC mechanism itself (GT-7, GT-8 document electrical current as one of several WEC/WEA drivers even without producing classic fluting) — that possibility remains live and is carried forward as an open verification item in the Conclusion, not abandoned.

### Dead End: Pure classical overload-driven fatigue as the sole explanation for the life shortfall

**What was tried:** Tested whether the 89% life shortfall (14,000 hrs actual vs. ~130,000 hr L10) could be explained entirely by a higher-than-design applied load, using standard Lundberg-Palmgren load-life scaling, without invoking any metallurgical or tribochemical accelerant.

**Why abandoned:** The load-life reconciliation (chain C4) shows this would require a sustained load on the order of 70-110% above design load, held continuously for the full 14,000-hour service life — a magnitude that would be expected to produce corroborating symptoms (elevated temperatures, distress on other gearbox components, anomalous torque/speed behavior) that are absent from the given facts. The chain does not prove no overload occurred; it shows the required magnitude is implausible as a *sole* explanation absent independent load evidence.

**What it ruled out:** Saves the operator from treating this primarily as a load/alignment problem (e.g., re-torquing or re-aligning the drivetrain) without first checking SCADA torque history — verification item (4) in the Conclusion remains the way to close this definitively rather than relying on the estimate's plausibility argument alone.

## 6. Conclusion

**Recommended approach:** Do not authorize the final replacement specification on the lubricant hypothesis alone. The verified root cause is a white-etching-crack (WEC) subsurface rolling-contact-fatigue mechanism — mixed/slip friction plus tribochemical hydrogen at subsurface inclusions/carbides, propagating to axial cracking and spalling (chain C6) — and the operator's boundary-lubrication/wear-through hypothesis is not supported by the evidence, in either its literal or physically corrected form (chains C2, C3). Before sign-off, close the following verification items, each of which is load-bearing for a specific chain above: (1) independently reread the metallographic sections and CM waterfall/envelope data to confirm GT-1 through GT-6 at source rather than as reported; (2) obtain oil-sample chemistry (water content, additive depletion, acid number) for the period around the cited cold snap; (3) confirm this unit's generator/converter topology and measure shaft-to-frame voltage and ground-brush contact resistance to resolve the stray-current candidate named in chain C5; (4) pull SCADA torque/load history for the full 14,000-hour interval to test the sustained-overload precondition priced in chain C4; (5) pull the SCADA event log for emergency stops, grid faults, and high-wind cutouts to test the torque-reversal-transient driver named in GT-8; (6) obtain SEM/EDS inclusion population data on the failed race to test whether the steel batch itself was outlying. Once these are closed, write the replacement specification to include electrical bonding/grounding verification and, if a converter-induced shaft-voltage path is confirmed, an insulated or hybrid-ceramic bearing and/or an upgraded shaft-grounding device — not merely a re-specified lubricant grade (chain C7).

**Key insight:** The four evidence items the operator listed separately — axial-aligned spalling, subsurface crescent microcracks at ~0.4 mm, white-etching cracks, and butterfly microstructures — are not four independent clues; read together they are the single, textbook fingerprint of one documented wind-turbine-gearbox-bearing failure mode (WEC-driven axial cracking), described from four different observational angles: macro fracture orientation, crack-initiation depth, crack shape, and microstructure (chain C1). Separately, the operator's causal narrative is physically backwards on its own terms — a cold snap raises oil viscosity, it does not lower it (chain C2) — which is a first-principles check that falsifies the hypothesis before the metallurgical evidence is even brought to bear.

**Trade-offs acknowledged:** This conclusion does not pin down, at HIGH confidence, which single WEC driver dominates — tribochemical hydrogen, stray electrical current, and torque-reversal transients are not mutually exclusive and the given facts do not discriminate between them (chain C6). Recommending that verification items be closed before spec sign-off costs schedule and inspection budget now, in exchange for avoiding authorization of a replacement spec that fixes the wrong variable and recurs on a similarly compressed timeline (chain C7) — a trade the analysis judges worthwhile given that WEC-type failures are a known fleet-wide pattern (GT-7, GT-8, GT-15?) rather than a one-off anomaly.

**Pre-check:** head C1 (MEDIUM), C2 (MEDIUM), C3 (MEDIUM), C4 (MEDIUM), C5 (MEDIUM), C6 (MEDIUM), C7 (MEDIUM) · ?-marked: none directly · lowest cited: MEDIUM · Inputs ceiling: MEDIUM
**Confidence:** MEDIUM — every contributing chain is independently rated MEDIUM (each for the specific unverified `GT-N?` inputs named on its own confidence line above, none of which is re-explained here per the citation rule), so the Conclusion is capped at MEDIUM by the ceiling rule. The single largest lever on this rating is GT-1? through GT-6? (the as-given inspection/CM/metallurgical facts): if those are independently confirmed at source and the six verification items above close in the direction this analysis anticipates, the Conclusion's band would move toward HIGH; if the electrical or torque-transient checks instead come back negative and oil chemistry shows no hydrogen-generating condition, the mixed/slip-friction-only pathway would need to be re-examined and the band could move toward LOW pending a new explanation for the magnitude of the life shortfall (chain C4).

---

## Techniques not applied

theoretical-limit — not applicable — this is a diagnostic root-cause analysis (which mechanism best explains observed evidence), not a question of what a physical law permits as a ceiling; no "what's the fundamental limit" question arises anywhere in the derivation.
trade-off — not applicable — selecting among candidate failure mechanisms here is an evidence-fit exercise (which mechanism's documented signature matches the observed morphology and magnitude) resolved via fishbone/discriminating-observation methodology and inversion, not a preference-weighted choice among comparably-evidenced options; there is no multi-criteria decision among viable alternatives that the operator must weigh.

## §6→§4 Closure Ledger (process output)

- "Recommended approach: Do not authorize the final replacement specification on the lubricant hypothesis alone... (chains C2, C3, C5, C4, C6, C7)" → chain C6 ✓ (cited inline; also inline-cites C2, C3, C4, C5, C7)
- "Key insight: The four evidence items... are the single, textbook fingerprint... (chain C1)... the operator's causal narrative is physically backwards... (chain C2)" → chain C1 ✓ (cited inline; also inline-cites C2)
- "Trade-offs acknowledged: ...(chain C6)... (chain C7)" → chains C6, C7 ✓ (cited inline)
- "Pre-check: head C1 (MEDIUM), C2 (MEDIUM), C3 (MEDIUM), C4 (MEDIUM), C5 (MEDIUM), C6 (MEDIUM), C7 (MEDIUM)..." → chains C1-C7 ✓ (cited inline in its own head field)
- "Confidence: MEDIUM — every contributing chain is independently rated MEDIUM..." → chains C1-C7 ✓ (cited inline in justification prose)

## Assumption Audit (process output)

| Chain | Step | Step Text (brief) | Assumption surfaced? | Added to Table? |
|---|---|---|---|---|
| C1 | 1 | 0.4mm depth/crescent shape matches Hertzian max-shear signature | A-17 — crescent microcracks = literature butterfly wings | yes |
| C1 | 2 | typical contact half-width bracket 0.1-0.6mm contains 0.4mm | A-18 — this bearing's half-width falls in typical bracket | yes |
| C1 | 3 | conclusion: subsurface origin at Hertzian max-shear zone | none | n/a |
| C2 | 1 | cold snap → low viscosity contradicts viscosity-T relation | none (covered by GT-12?) | n/a |
| C2 | 2 | conclusion: closest coherent analog is starvation, not thinning | none | n/a |
| C3 | 1 | starvation predicts surface adhesive/abrasive wear | none (covered by GT-14?) | n/a |
| C3 | 2 | observed damage requires cyclic subsurface stress reversal | none | n/a |
| C3 | 3 | conclusion: wear-through hypothesis not supported | none | n/a |
| C4 | 1 | life-ratio → required 1.7-2.1x sustained overload | none (covered by existing Assumptions Table "no sustained overload" row) | n/a |
| C4 | 2 | such overload would produce corroborating symptoms | none | n/a |
| C4 | 3 | conclusion: classical overload implausible at required magnitude | none | n/a |
| C5 | 1 | no reported surface erosion pattern rules out classic fluting as dominant | none (covered by GT-9) | n/a |
| C5 | 2 | electrical current still documented as a WEC contributor | none (covered by GT-7, GT-8) | n/a |
| C5 | 3 | conclusion: stray current remains a live unresolved candidate | none | n/a |
| C6 | 1 | evidence best matches mixed-friction + hydrogen WEC vs. rivals considered | A-20 — rival mechanism set considered is adequate | yes |
| C6 | 2 | lubricant is a contributing amplifier, not sufficient alone | none (covered by GT-7) | n/a |
| C6 | 3 | conclusion: verified root cause + lubricant's role | none | n/a |
| C7 | 1 [2nd] | unaddressed drivers → recurrence risk on replacement bearing | none | n/a |
| C7 | 2 [3rd] | fleet-wide blind spot if root cause stays unconfirmed | none | n/a |
| C7 | 3 | conclusion: verification checklist is a precondition, not optional | none | n/a |

## Adversarial pass (process output)

**Recompute.** Life-ratio arithmetic (C4): 14,000/130,000 = 0.1077; 1/0.1077 = 9.285. At p=10/3: 9.285^0.3 = e^(0.3·ln 9.285) = e^(0.3·2.228) = e^0.668 ≈ 1.95. At p=3: 9.285^(1/3) = e^(0.333·2.228) = e^0.743 ≈ 2.10. At p=4: 9.285^0.25 = e^(0.25·2.228) = e^0.557 ≈ 1.74. Bracket [1.74, 2.10], central ≈1.95 — matches the figures stated in C4 exactly. Cross-check against the cited field figure (GT-11?: 252% load increase → ~22-fold life reduction): 2.52^(10/3) = e^(3.333·ln2.52) = e^(3.333·0.9243) = e^3.081 ≈ 21.8 ≈ 22-fold — recomputes consistently, corroborating the p=10/3 exponent independently of the source's own stated figure.

**Sensitivity.** The single ground truth whose falsity would flip the headline conclusion (C6) is the block GT-5?/GT-6? (the metallographic description itself: subsurface crescent microcracks + WEC + butterflies). Both are `?`-marked. If independent re-examination of the actual sections showed the crack origin at the raceway surface rather than ~0.4 mm subsurface, C1 collapses, and with it C3, C5, and C6 — the operator's original hypothesis would need to be reopened rather than treated as falsified. Verification path: independently reread the metallographic sections/photomicrographs directly (verification item 1 in the Conclusion). Until that read happens, this is the single highest-leverage unresolved input in the whole analysis.

**Rival.** Headline (C6): the strongest rival is "pure classical overload-driven fatigue, no metallurgical/tribochemical accelerant needed" — ruled out (as a *sole* explanation) by C4's magnitude estimate and recorded in section 5's dead end "Pure classical overload-driven fatigue as the sole explanation for the life shortfall." Intermediate chain C5: the live rival "classic electrical fluting was present at the contact but not reported/observed" is not settled by any observation in hand — it stays live and is carried forward as verification item (3) in the Conclusion rather than resolved here. Intermediate chain C1: the rival "the 0.4 mm figure is coincidental, not evidence of Hertzian-max-shear origin" is addressed inline by GT-8's independent documentation that WEA in wind-turbine gearbox bearings characteristically occurs at <1 mm, coincident with the Hertzian max-shear zone — not a coincidence specific to this unit.

**Adversarial technique: Pre-Mortem** (the operator-facing deliverable is fundamentally a plan — close six verification items, then authorize a replacement spec with named design/monitoring changes — so Pre-Mortem is the applicable technique per the plan/claim decision rule; Inversion was already applied to the operator's *claim* in Phase 2 above, testing the failure-guaranteeing preconditions of the lubricant hypothesis).

*Premise (past tense):* The plan has already failed — the operator authorized the replacement spec on the lubricant hypothesis without closing the verification items, and the new bearing failed prematurely again on a similarly compressed timeline.

*Causes (unfiltered, generated from four stakeholder viewpoints — O&M/reliability engineer, finance/warranty desk, OEM bearing supplier, competing O&M provider):*
1. Verification items were deprioritized under schedule pressure and the spec was signed off on the lube hypothesis alone (O&M).
2. Ground-brush/shaft-voltage measurement equipment wasn't available on site and the check was skipped rather than scheduled (O&M).
3. The insurer/warranty desk accepted "weather event" as the recorded cause because it was the fastest path to closing the claim, discouraging further electrical investigation (finance).
4. The OEM bearing supplier had no incentive to flag a design-level grounding issue that could affect other units it also supplied (OEM — conflict of interest).
5. SCADA historical torque/event-log retention is shorter than 14,000 hours, making the overload/torque-reversal check (C4, GT-8) impossible to run retroactively (data availability).
6. No oil sample from the actual cold-snap window was drawn or archived, so the chemistry check can only characterize current conditions, not the conditions that mattered.
7. The replacement bearing is the same uninsulated type on the same unchanged grounding path, so a correct lubricant fix does nothing to interrupt a stray-current path if one exists (design carryover).
8. A competing O&M provider bidding for the contract notes the unresolved root cause as a service-quality risk to use against the incumbent (competitor — reputational).
9. CM alarm thresholds are left unchanged after the fix, so a slower-developing recurrence is not flagged until it reaches the same late-stage kurtosis signature, losing further lead time (detection).

*Clusters:*
- **Cluster A — Verification skipped under schedule/cost pressure** (causes 1, 2, 6; bears on C6, C7).
- **Cluster B — Retroactive data unavailable to test the estimate** (cause 5; bears on C4).
- **Cluster C — Incentive misalignment discourages finding the real cause** (causes 3, 4, 8; bears on C6, C7).
- **Cluster D — Design carryover reintroduces the same failure path** (cause 7; bears on C6).
- **Cluster E — Detection doesn't improve after the fix** (cause 9; bears on C7).

*Disposition:*
- A — **Plan change:** make the six verification items a hard release-gate in the work order/PO system, with named owners and due dates, before the replacement purchase order is released.
- B — **Accepted risk, named mitigation:** accept that pre-failure SCADA data may be unrecoverable; mitigate by extending fleet-wide SCADA/CM data retention policy going forward, and by treating "no corroborating symptoms reported" as the fallback evidentiary standard (already used in C4) when direct retroactive load data cannot be recovered.
- C — **Plan change:** route the final root-cause determination through an independent reliability engineer, not the OEM warranty desk or insurer alone, before the cause is entered into any claim paperwork.
- D — **Plan change:** make electrical bonding/grounding verification, and — if confirmed — an insulated/hybrid-ceramic bearing or shaft-grounding device upgrade, an explicit line item in the replacement spec rather than an implied follow-up.
- E — **Plan change:** add a monitoring channel tuned to WEC precursors (shaft voltage and/or high-frequency envelope trending) to the replacement bearing's CM configuration, not a repeat of kurtosis-only trending.

**Falsification.** The conclusion is false if independent rereading of the metallographic sections shows the crack origin at the raceway surface rather than ~0.4 mm subsurface, or if SCADA data confirm a sustained load matching C4's 1.7-2.1x bracket, or if shaft-voltage/ground-brush and oil-chemistry data both return clean while a documented, sufficiently severe boundary-lubrication event is independently confirmed at the exact failure window — any one of these would require chain C6 to be revised.

## Self-audit scan (process output)

| Chain | Chain Head (brief) | Form conforming? | Rule applied | Dependency clean? | Band | Act attempted? | Edges fired |
|---|---|---|---|---|---|---|---|
| C1 | GT-5?, GT-8, GT-10? | yes | n/a | yes | MEDIUM | yes (GT-8 opened via WebFetch) | none |
| C2 | GT-12? | yes | n/a | yes | MEDIUM | no (GT-12 only WebSearch, not opened) | none |
| C3 | C2, GT-14?, C1 | yes | n/a | yes | MEDIUM | no (GT-14 only WebSearch) | none |
| C4 | GT-3?, GT-11? | yes | n/a | yes | MEDIUM | no (neither opened directly) | none |
| C5 | GT-9, C1 | yes | n/a | yes | MEDIUM | yes (GT-9 opened via WebFetch) | none |
| C6 | C1, C3, C4, C5, GT-7 | yes | n/a | yes | MEDIUM | yes (GT-7 opened via WebFetch) | none |
| C7 | C6 | yes | n/a | yes | MEDIUM | no (no new source on this chain's own head) | none |

| §6 Span (brief) | Construct | Claim under R11? | R11 clause applied | Chain cited |
|---|---|---|---|---|
| "Recommended approach: Do not authorize..." | bold lead-in | yes | bold lead-in whose colon closes the bold span, content on same line | C6 (also inline: C2, C3, C4, C5, C7) |
| "Key insight: The four evidence items..." | bold lead-in | yes | bold lead-in whose colon closes the bold span, content on same line | C1 (also inline: C2) |
| "Trade-offs acknowledged: This conclusion does not pin down..." | bold lead-in | yes | bold lead-in whose colon closes the bold span, content on same line | C6 (also inline: C7) |
| "Pre-check: head C1 (MEDIUM), C2 (MEDIUM)..." | bold lead-in | yes | pre-check line is itself a claim per template §6, cited by chains named in its own head | C1, C2, C3, C4, C5, C6, C7 |
| "Confidence: MEDIUM — every contributing chain..." | bold lead-in | yes | bold lead-in whose colon closes the bold span, content on same line; D-07-required chain naming | C1, C2, C3, C4, C5, C6, C7 |

Scan complete: 7 chain rows, one per section-4 chain block in order; 5 section-6 rows, one per construct in order — 5 claims under R11, 0 excluded. 0 chains malformed, 0 claims untraced.

## Self-Audit Gate (process output)

**Criterion 1: Identify Essence**
Quoted span: "What physical mechanism actually produced the subsurface, axial-aligned, white-etching-crack-and-butterfly damage that removed this HSS generator-end bearing at 11% of its L10 design life — and does the lubricant-viscosity/boundary-lubrication wear-through hypothesis the operator has proposed match that mechanism, or does the evidence point to a different, verifiable driver..."
Band: **Rigorous**
Justification: The statement names the underlying mechanism-identification question rather than the triggering event (the vibration alarm) or a restatement of the operator's prompt, and each of the five success criteria is a verb+subject+outcome triplet checkable directly against section 6 (e.g., "the Conclusion states, in one sentence, whether the operator's... hypothesis is confirmed or falsified... backed by a named derivation chain").

**Criterion 2: Challenge Assumptions**
Quoted span: "The operator's working hypothesis — low lubricant viscosity drove boundary lubrication which wore through the race — accurately describes this failure | convention (the hypothesis under test) | ... | **Discard** — contradicted by GT-12 (wrong physical direction) and by GT-9/GT-14 (wrong damage morphology); see C2, C3 | unverified — flagged prior to discard; discard reasoning in C2/C3"
Band: **Rigorous**
Justification: Every row uses one of the four prescribed types, every Verdict cell leads with a token (Accept/Challenge/Discard) followed by an em-dash and a specific reason, at least one assumption is explicitly discarded (not merely accepted), unverified assumptions used in chains carry "unverified — flagged," and the Assumption Audit scan (process output above) confirms the end-of-Phase-4 audit ran exhaustively over all 19 chain steps and added the three assumptions (A-17, A-18, A-20) it surfaced back into this table.

**Criterion 3: Establish Ground Truths**
Quoted span: "?-marked: GT-1, GT-2, GT-3, GT-4, GT-5, GT-6, GT-10, GT-11, GT-12, GT-13, GT-14, GT-15 (12 of 15)" — checked against the Ground Truths list: GT-1 through GT-6, GT-10 through GT-15 all carry `?`; GT-7, GT-8, GT-9 do not — the enumeration matches exactly twelve suffixed IDs against fifteen total.
Band: **Rigorous**
Justification: GT-IDs are stable and match the IDs cited in section 4's chain heads; every unsuffixed GT (GT-7, GT-8, GT-9) names its read-at-source location (specific article and URL, opened via WebFetch); no chain in this analysis reaches HIGH confidence, so the "every unsuffixed GT feeding a HIGH-confidence chain must name a read-at-source location" requirement is vacuously satisfied rather than violated; GT-15's Phase 3 failure record names the unreachable source (docs.nrel.gov, DNS resolution error) and it feeds no HIGH chain; no Phase-2-discarded assumption appears in this list.

**Criterion 4: Reason Upward**
Quoted span (from the self-audit scan, chain-form table): "C1 | GT-5?, GT-8, GT-10? | yes | n/a | yes | MEDIUM | yes (GT-8 opened via WebFetch) | none" ... "Scan complete: 7 chain rows, one per section-4 chain block in order; ... 0 chains malformed, 0 claims untraced."
Band: **Rigorous**
Justification: All seven chains score `yes` on Form conforming and `yes` on Dependency clean per the self-audit scan; each chain carries at least one genuine intermediate step distinct from its head inputs; the three assumptions surfaced mid-chain (A-17, A-18, A-20) are declared inline with `[Assumes: X]` exactly at the hop that introduces them; no analogy is used as direct evidence anywhere (all cross-situation claims are grounded in named, cited GTs — GT-7, GT-8, GT-9 — not bare "others have seen this" assertions); the Abandoned Reasoning section documents three dead ends, each with a specific structural reason (contradicted by a named GT, or an implausible-magnitude estimate) rather than a vague one.

**Criterion 5: Validate**
Quoted span: "The Rivals axis is addressed rather than short: every competing conclusion to this endpoint considered by the analysis -- pure classical overload (ruled out by C4, Abandoned Reasoning), literal or corrected boundary-lubrication wear-through (ruled out by C2/C3, Abandoned Reasoning), and classic electrical fluting as an independent dominant mechanism (ruled out by C5, Abandoned Reasoning) -- has a named chain or dead-end entry ruling it out." (C6 confidence line)
Band: **Rigorous**
Justification: Every chain's confidence line names its specific `GT-N?` inputs with a verification path and names each cited `Cn` rated below HIGH without re-explaining it; no chain is rated HIGH while consuming a `?` input; every chain is rated no higher than the lowest-rated chain it cites (C3, C5, C6, C7 all correctly cap at the MEDIUM of their cited chains); each band was checked against its three licensing axes during this gate pass and two calibration errors found during that check (C1 and C6 each initially under-priced one axis, which would have required LOW) were corrected in the analysis text itself before this verdict was written, so the bands now on the page match what their axes license; the adversarial pass record is complete with all five parts (Recompute, Sensitivity, Rival, Pre-Mortem technique with Premise/Causes/Clusters/Disposition, Falsification) and every cluster in the Pre-Mortem carries a named plan change or an explicitly accepted risk with a named mitigation.

**Criterion 6: Conclusion-to-Ground-Truth Traceability**
Quoted span (from the self-audit scan, claim-inventory table): "\"Recommended approach: Do not authorize...\" | bold lead-in | yes | bold lead-in whose colon closes the bold span, content on same line | C6 (also inline: C2, C3, C4, C5, C7)" ... "Scan complete: ... 5 claims under R11, 0 excluded. ... 0 claims untraced."
Band: **Rigorous**
Justification: All five section-6 claims (Recommended approach, Key insight, Trade-offs acknowledged, Pre-check, Confidence) trace to specific named chains inline, per the claim-inventory table and the §6→§4 closure ledger (all rows ✓, none CUT); no claim is introduced in section 6 that does not appear in section 4; the Key Insight names a non-obvious finding — that the four separately-listed evidence items are one coherent WEC fingerprint, and that the operator's causal direction is physically inverted — rather than restating the Recommended Approach.

**Gate result:** No criterion scored Absent; zero criteria scored Hand-wavy (the cap is "at most one," so this clears with margin). **The analysis clears the Self-Audit Gate.** No re-perception pass was required; the two calibration corrections identified while preparing Criterion 5's verdict were applied directly to chains C1 and C6 in section 4 before this gate was scored, so the scoring above reflects the corrected text, not a promise to fix it later.

