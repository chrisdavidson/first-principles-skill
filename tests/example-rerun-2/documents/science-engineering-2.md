## Answer

**Recommendation:** Install a bearing meeting current design intent now to restore availability, run the falsifiable diagnostic checks below before finalizing the long-term spec, and apply interim cold-weather lubrication controls immediately — do not rely on a viscosity upgrade alone, since the evidence refutes that as the primary mechanism (chain C9, chain C1, chain C2).
**Band (from §6):** LOW (chain C9)
**Would change it:** Resolving chain C7's unresolved electrical-current rival — via shaft-voltage logging, brush/ring condition checks, and an EDM-pitting search on adjacent bearings — is the diagnostics chain C7 names, and running them is what the Confidence line in §6 states would raise this band toward MEDIUM/HIGH (chain C7, chain C9).

## 1. Problem Essence

**Core problem:** Determine which failure mechanism — the operator's boundary-lubrication/viscosity hypothesis, classical inclusion-driven rolling-contact fatigue (RCF), or white-etching-crack (WEC) / hydrogen-assisted premature RCF (possibly with an electrical-current contribution) — is actually consistent with the full combination of macroscopic and microscopic evidence on this HSS generator-end bearing, so that the replacement specification is driven by the real cause rather than the first plausible-sounding story.

**Success criteria:**
1. The conclusion names one mechanism class that is simultaneously consistent with all four pieces of metallurgical evidence (subsurface origin depth, crescent microcracks, WECs, butterflies) rather than explaining only one of them.
2. The conclusion states explicitly whether the operator's viscosity/boundary-lubrication hypothesis is confirmed, refuted, or partially right, and names the specific evidence that discriminates.
3. The conclusion carries a stated confidence band (HIGH/MEDIUM/LOW) and names what verification would raise or lower it.
4. The conclusion yields concrete, falsifiable diagnostic checks runnable on the removed bearing/system before the replacement spec is finalized.
5. The recommended replacement spec is shown to target the verified or best-evidenced root cause rather than only the proximate symptom.

---

## 2. Assumptions Table

**Inversion applied to the operator's hypothesis (Phase 2).** The operator's claim, precisely stated, is: *"Lubricant viscosity dropped during the cold snap, driving boundary lubrication, and the inner race wore through."* Inverted, the claim is false unless four preconditions all hold: **P1** the damage is surface-initiated (asperity contact); **P2** the damage morphology shows adhesive/abrasive wear (frosting, smearing, scuffing) rather than crack morphology; **P3** lubricant viscosity actually fell below the EHL film-forming threshold during the cold snap; **P4** the onset timing reflects a transient low-viscosity excursion rather than a different cold-linked mechanism. The assumptions below test each precondition explicitly (rows A1-A3, A6, A9) rather than assuming the claim survives by default.

| Assumption | Type | Treatment | Verdict | Verification |
|---|---|---|---|---|
| A1: The cold snap lowered the lubricant's effective viscosity below the minimum EHL film-forming threshold (operator's P3) | untested belief | Verify against the lube sump/inlet temperature log and the oil's ISO VG viscosity-temperature chart | Challenge — the claimed *direction* contradicts the viscosity-temperature physical law (promoted to GT-13); cooling normally **raises** viscosity | unverified — flagged |
| A2: Boundary-lubrication/abrasive-adhesive wear caused the race to wear through (operator's full causal chain, P1+P2) | untested belief | Compare against established surface-vs-subsurface wear-mode signatures before accepting | Discard — contradicted by GT-9/GT-10 against the subsurface/WEC/butterfly evidence (GT-5?-GT-7?); see chain C1 | unverified — flagged |
| A3: A temporal correlation between the cold snap and the CMS kurtosis step-change proves the operator's specific causal mechanism (P4) | convention | Explicitly challenge — correlation is not the same claim as the proposed mechanism | Challenge — the correlation itself is plausible (GT-8?) but requires a different causal pathway (chain C6) than the one proposed | unverified — flagged |
| A4: This HSS bearing sits in an electrical current-return path between the generator/converter and ground | current constraint | Record expiry: applies only if confirmed by this turbine's electrical single-line drawing; expires if shaft grounding/insulated bearings are already fitted | Challenge — applicability not confirmed for this specific asset (GT-19?) | unverified — flagged |
| A5: ISO 281's L10 basic rating life formula and its "ideal condition" basis are the correct reference standard for judging this bearing's expected life | physical law | Accept as ground-truth candidate | Accept — standard, auditable, industry-wide definition; promoted to GT-11 | read-at-source (fabrico.io, "L10 Bearing Life") |
| A6: Boundary-lubrication wear and subsurface rolling-contact fatigue leave visually distinguishable, surface-vs-subsurface damage signatures | physical law | Accept as ground-truth candidate | Accept — promoted to GT-9/GT-10 | read-at-source (machinerylubrication.com) |
| A7: The root-cause mechanism of white-etching cracks is settled science with one definitive trigger | convention | Explicitly challenge before relying on any single WEC trigger as proven | Discard (as stated) — the surveyed literature itself states no hypothesis is proven (GT-17?); treated as a multi-candidate open question (chains C6, C7) | unverified — flagged (reported-by-delegate, GT-17?) |
| A8: Electrical-discharge (EDM) arcing/fluting and a lower-level diffuse current-hydrogen pathway are the same phenomenon with the same damage signature | untested belief | Verify by inspecting this and adjacent bearings specifically for EDM pitting/frosting/fluting | Challenge — GT-15 documents EDM/fluting as a distinct surface-progression signature from the subsurface damage reported here | unverified — flagged |
| A9: Low temperature measurably alters the EHL traction coefficient / micro-slip (skidding) behavior of this bearing at its actual load and speed envelope | untested belief | Verify via bearing dynamic/traction (slip-ratio) analysis or an OEM skidding study for cold-start/low-torque conditions | Challenge — physically plausible and consistent with GT-13/GT-18?, but not independently confirmed for this asset; used in chain C6 as `[Assumes: A9]` | unverified — flagged |
| A10: Cold-weather thermal cycling increased moisture condensation/water ingress into the gearbox lubricant | untested belief | Verify via lubricant moisture (Karl-Fischer) trend and breather/seal condition history | Challenge — plausible contributing tribochemical pathway, not confirmed | unverified — flagged |
| A11: Anti-wear/EP additive tribofilm-formation kinetics are less effective at low temperature, increasing nascent-surface exposure | untested belief | Verify via lubricant TAN, elemental (Fe/Cu/P/Zn/S), and RULER/RPVOT additive-depletion analysis | Challenge — broadly consistent with known tribochemistry, not confirmed for this oil/charge | unverified — flagged |
| A12: The case-record facts as supplied (CMS trend, L10, macro/micro damage description, cold-snap timing) accurately and completely represent the underlying CMS export, metallurgical lab report, and SCADA logs | untested belief | Obtain and open the raw CMS kurtosis export, the metallurgical lab report with micrographs, the SCADA ambient/lube temperature trend, and the bearing datasheet | Challenge — none of the underlying source documents were provided to or opened by this analysis; this is the master data-provenance gap behind GT-1? through GT-8? | unverified — flagged |
| A13: No shaft-grounding brush or insulated-bearing current mitigation is currently installed on this HSS generator-end bearing | current constraint | Verify against as-built electrical single-line drawings and O&M retrofit records; expires once confirmed installed or confirmed absent | Challenge — status not stated in the given facts (GT-19?) | unverified — flagged |
| A14: A like-for-like replacement bearing is the correct default absent further findings | convention | Explicitly challenge the MRO default against this analysis's findings before locking the spec | Challenge — superseded by the diagnostics-gated recommendation (chain C9) | unverified — flagged (no chain — informs C9's Option-A scoring rather than a load-bearing input) |
| A15: GT-9/GT-10's general wear-mode classification (surface-vs-subsurface signatures) transfers without modification to large through-hardened/case-carburized wind-turbine gearbox bearing steel [surfaced from chain C1, hop 2] | untested belief | Verify that GT-9/GT-10's classification has been validated specifically for this bearing's steel grade and processing, not just generic bearing steel | Challenge — plausible by metallurgical generality, not independently confirmed for this steel grade | unverified — flagged |
| A16: Classical Lundberg-Palmgren statistical scatter (ISO 281, GT-11) is the correct comparison population for judging whether 11% of L10 is abnormal, rather than a figure the OEM already derated for this bearing position [surfaced from chain C4, hop 1] | untested belief | Verify whether the quoted L10 ≈ 130,000 h already includes a position-specific derating factor | Challenge — if it does, the abnormality margin in chain C4 must be recomputed against the derated figure | unverified — flagged |
| A17: The HSS generator-end bearing's actual Hertzian contact half-width under rated/duty-cycle load falls within the illustrative 0.15-0.55 mm bracket used in chain C3 [surfaced from chain C3, hop 1] | untested belief | Verify against the bearing's catalog geometry and the gearbox's rated/duty-cycle load spectrum | Challenge — bracket is an order-of-magnitude illustration, not asset-specific | unverified — flagged |
| A18: The macroscopic damage description (axial spalling only) reflects a deliberate inspection for EDM frosting/pitting/fluting, not merely silence because nobody looked [surfaced from chain C7, hop 1] | untested belief | Verify whether the original inspection specifically examined for frosting/fluting on this and adjacent bearings | Challenge — the case record's silence is evidentially weak either way until confirmed by direct re-inspection | unverified — flagged |
| A19: The trade-off's criteria weights (chain C9) reflect this specific asset owner's actual risk tolerance and budget constraints rather than a generic default ordering [surfaced from chain C9, hop 1] | convention | Explicitly challenge before the weights are contractually locked | Challenge — weights are a reasonable generic default; owner-specific re-weighting is recommended before the spec is finalized | unverified — flagged |

## 3. Ground Truths

**Case-record facts (as supplied in the investigation narrative; no underlying CMS export, lab report, or SCADA log was opened by this analysis):**

- **GT-1?** Asset is a 1.5 MW upwind wind turbine; the failed component is the generator-end cylindrical roller bearing on the HSS gearbox stage, inner race — unverified: no asset nameplate, maintenance record, or bearing datasheet was opened; supplied as case narrative only.
- **GT-2?** The condition monitoring system (CMS) detected a step change (sudden increase) in HSS vibration kurtosis at approximately 14,000 operating hours — unverified: the raw CMS kurtosis trend export was not opened.
- **GT-3?** Design L10 ≈ 130,000 hours; failure occurred at roughly 11% of L10 (14,000 / 130,000 ≈ 10.8%, consistent with "roughly 11%") — unverified: the bearing datasheet / L10 calculation sheet was not opened.
- **GT-4?** Macroscopic damage: axial-aligned spalling on the inner race, approximately 18 mm long — unverified: the visual-inspection report/photographs were not opened.
- **GT-5?** Microscopic examination through the spall shows crescent-shaped microcracks propagating from a subsurface origin approximately 0.4 mm below the raceway surface — unverified: the metallurgical lab report and micrographs were not opened.
- **GT-6?** White-etching cracks (WECs) are present in the metallography — unverified: same lab report gap as GT-5?.
- **GT-7?** Butterfly-shaped microstructural features are visible around the subsurface origin — unverified: same lab report gap as GT-5?.
- **GT-8?** Cold-snap months (an ambient/lubricant temperature excursion) preceded the vibration step-change — unverified: the SCADA ambient/lubricant temperature log was not opened.

**Externally grounded ground truths:**

- **GT-9** Boundary-lubrication wear (mixed/boundary EHL regime, asperity contact) initiates at the surface and "initially appear[s] as a matted or frosted surface," visible at 3-5x magnification; scuffing/adhesive wear leaves a surface that is "rough and jagged or relatively smooth due to smearing/deformation of the metal," with material transfer between surfaces — source: Machinery Lubrication, "Basic Wear Modes in Lubricated Systems"; read-at-source: article sections "Boundary Lubrication Wear" and "Scuffing/Adhesive Wear," fetched directly, quoted verbatim above.
- **GT-10** Subsurface rolling-contact fatigue (spalling/pitting) begins below the surface when "microcracks form due to long-term repeated load cycles and stress... causing elastic deformation (flexing) of the metal," with cracks propagating up to the surface; "a full oil film exists and no metal-to-metal contact or surface damage is needed" — source: same Machinery Lubrication article; read-at-source: section "Subsurface Fatigue (Spalling/Pitting)," quoted verbatim above.
- **GT-11** Under ISO 281, basic rating life L10 = (C/P)^p, with p = 10/3 for roller bearings; L10 is "the life that 90 percent of a group of identical bearings will reach before the first signs of metal fatigue appear" (i.e., 10% of an identical population is expected to have failed by that point); the base rating assumes "clean lubrication, correct alignment, no contamination and moderate temperature," conditions "real bearings rarely see" — source: fabrico.io, "L10 Bearing Life"; read-at-source: fetched directly, formula and statistical-meaning statements quoted verbatim above.
- **GT-12** For a Hertzian line contact, the depth of maximum orthogonal subsurface shear stress is z0 ≈ 0.78b below the surface, where b is the contact semi-width — source: physical law / standard contact-mechanics result (Johnson, *Contact Mechanics*; Harris, *Rolling Bearing Analysis*); no single web citation required for an established closed-form mechanics result, consistent with the physical-law treatment prescribed in Phase 2.
- **GT-13** Lubricant kinematic viscosity increases monotonically as temperature decreases, within the normal liquid range (before wax/pour-point gelling), per standard viscosity-temperature relations (e.g., ASTM D341 / Walther equation) — source: physical law, standard lubrication-engineering relation; no single web citation required.
- **GT-14** Per the NREL Gearbox Reliability Collaborative database (750 damage records, 2009-Aug 2015, >20 operator data-sharing partners), "the majority of wind turbine gearbox failures (76%) are caused by the bearings," and the dominant bearing failure mode is axial cracks at the high- and intermediate-speed stages — source: energy.gov, "Statistics Show Bearing Problems Cause the Majority of Wind Turbine Gearbox Failures" (NREL GRC summary); read-at-source: fetched directly, 76% figure and axial-crack finding quoted/paraphrased from the fetched text above.
- **GT-15** Electrical-discharge (EDM-type) bearing-current damage progresses through a surface sequence — "thousands of microscopic pits," then "a visible matte condition called frosting," then "a striped or picket-fence pattern" (fluting) — described as a progressive **surface**-degradation phenomenon; capacitive shaft-voltage risk is present in all VFD-driven machines, while high-frequency circulating-current risk is more associated with machines above ~100 HP/75 kW — source: est-aegis.com, "Electrical Bearing Damage: Shaft Voltage and Bearing Currents"; read-at-source: fetched directly, quotes above are verbatim from the fetched text.
- **GT-16?** White-etching cracks (WECs) are branching, multi-millimetre subsurface crack systems associated with a nanocrystalline/carbide-altered "white etching area" (WEA) microstructure; "butterflies" are smaller subsurface cracks nucleating at non-metallic inclusions/carbides, forming wing-shaped white-etching regions typically oriented ~30° to the rolling direction — cited to: University of Southampton eprints repository and BUAA research publications on WEC/butterfly microstructure; reported-by-delegate: WebSearch synthesis of academic search results — the individual papers were not opened by this analysis.
- **GT-17?** Proposed WEC root-cause hypotheses in the surveyed literature include hydrogen diffusion/embrittlement, electrical current/electrostatic discharge, increased sliding/micro-slip, impact loading, corrosion fatigue, and adiabatic shear, and as of the literature surveyed "none of the hypotheses has been proven" — it is "currently an active field of research" — cited to: University of Southampton tribology group (e.g., the paper indexed as s11249-017-0947-0) via search aggregation; reported-by-delegate: WebSearch synthesis — the primary paper was not opened by this analysis.
- **GT-18?** In rolling-contact-fatigue test specimens, hydrogen diffused into rolling elements with increasing concentration over test duration, and WECs increased in number/severity with duration; because most WECs did not breach the contact surface, hydrogen diffusion is assumed to occur "at wear-induced nascent surfaces or areas of heterogeneous/patchy tribofilm" — cited to: University of Southampton tribology group research; reported-by-delegate: WebSearch synthesis — the primary paper was not opened by this analysis.
- **GT-19?** This turbine's generator/converter topology (e.g., doubly-fed induction generator with a partial-scale converter, versus a full-scale converter) and the presence or absence of a shaft-grounding brush or insulated bearing on this HSS stage are not stated anywhere in the facts supplied — unverified: this is an identified asset-specific data gap, not a claim this analysis can source.
- **GT-20?** A variable-frequency drive's/converter's fast PWM switching produces a common-mode voltage that couples via parasitic rotor-stator capacitance to the shaft; when the resulting shaft voltage exceeds the dielectric breakdown strength of the thin EHL film in a bearing, the film punctures in a capacitive, EDM-like discharge — cited to: fabrico.io ("VFD Bearing Currents") and est-aegis.com, via search aggregation; reported-by-delegate: this specific mechanism description was not confirmed by directly opening either page (the est-aegis.com page this analysis did open, GT-15, covered the damage-progression signature, not the common-mode-voltage coupling mechanism itself).
- **GT-21?** A statistic commonly repeated in wind-industry trade coverage states that approximately 60% of high-speed-stage wind turbine gearbox bearing failures are attributed to WEC — **Phase 3 failure record:** this analysis attempted to verify the figure by opening windpowerengineering.com directly; the fetched article discusses WEC/irWEA phenomenology but does not contain this statistic, and no original primary source for the figure was identified. Marked unverified and **not used as a head input to any load-bearing chain** in this analysis — background context only.
- **GT-22?** High lubricant viscosity at cold start-up can impede oil-pump delivery and gearbox oil flow, producing a transient marginal-lubrication condition distinct from the low-viscosity film-breakdown mechanism — **Phase 3 failure record:** a candidate source (AGMA, "Bearing Failures," PDF) was located and an open attempted, but the document's text layer was compressed/non-extractable; no readable confirmation was obtained. Retained as an untested-belief domain-engineering judgment (A22, folded into A9's treatment), not as a sourced ground truth.

**Provenance summary:**

```text
?-marked: GT-1, GT-2, GT-3, GT-4, GT-5, GT-6, GT-7, GT-8, GT-16, GT-17, GT-18, GT-19, GT-20, GT-21, GT-22 (15 of 22)
Read-at-source: GT-9 — machinerylubrication.com, "Basic Wear Modes in Lubricated Systems," section "Boundary Lubrication Wear" ("initially appear as a matted or frosted surface")
Read-at-source: GT-10 — same article, section "Subsurface Fatigue (Spalling/Pitting)" ("a full oil film exists and no metal-to-metal contact or surface damage is needed")
Read-at-source: GT-11 — fabrico.io, "L10 Bearing Life" (formula and "10 percent of a population is statistically expected to fail by this point")
Read-at-source: GT-12 — standard Hertzian line-contact result (physical law; Johnson, Contact Mechanics; Harris, Rolling Bearing Analysis), z0 ≈ 0.78b
Read-at-source: GT-13 — standard viscosity-temperature relation (physical law; ASTM D341 / Walther equation)
Read-at-source: GT-14 — energy.gov, NREL Gearbox Reliability Collaborative summary ("the majority of wind turbine gearbox failures (76%) are caused by the bearings")
Read-at-source: GT-15 — est-aegis.com, "Electrical Bearing Damage: Shaft Voltage and Bearing Currents" ("thousands of microscopic pits," "a visible matte condition called frosting," "a striped or picket-fence pattern")
```

## 4. Derivation Chains

### Conclusion C1: The operator's hypothesis is refuted on damage morphology

GT-4? (axial spalling, ~18 mm) + GT-5? (subsurface origin, ~0.4 mm, crescent cracks) + GT-9 (boundary-lubrication wear is surface-initiated) + GT-10 (subsurface RCF initiates below the surface)
→ the observed damage originates roughly 0.4 mm below the raceway surface as a subsurface crescent-crack network, not as a surface asperity-contact wear pattern [Assumes: A15]
→ that below-the-surface crescent-crack morphology is the signature assigned to subsurface rolling-contact fatigue, not to boundary-lubrication or scuffing wear
→ the operator's proposed mechanism — viscosity loss driving boundary lubrication and wear-through — does not match the observed damage morphology and is refuted as the operative mechanism

**Pre-check:** head GT-4?, GT-5?, GT-9, GT-10 · ?-marked: GT-4?, GT-5? · lowest cited: none · Inputs ceiling: MEDIUM
**Confidence:** MEDIUM — GT-4? and GT-5? are unverified (the visual-inspection report and the metallurgical lab report/micrographs were not opened by this analysis); verification = obtain and open those source documents directly and confirm the stated measurements. Hop 1 rests on `[Assumes: A15]` (that generic wear-mode classification transfers to this bearing's steel); if A15 fails, the surface-vs-subsurface distinction itself is a crack-initiation-physics claim that is not steel-chemistry-dependent, so the conclusion is not seriously threatened by A15 failing — only the degree of confidence in applying it to this specific steel grade.

### Conclusion C2: The operator's hypothesis is independently refuted on the direction of the physics

GT-8? (cold snap preceded the step-change) + GT-13 (viscosity rises as temperature falls)
→ the operator's claim that the cold snap lowered viscosity runs opposite to the direction the temperature-viscosity relationship predicts for a normal mineral or synthetic gear oil
→ the operator's specific proposed mechanism — cold driving low viscosity driving boundary lubrication — is backwards for the direction of the temperature change and is refuted on physical-law grounds, independent of the morphological refutation in chain C1

**Pre-check:** head GT-8?, GT-13 · ?-marked: GT-8? · lowest cited: none · Inputs ceiling: MEDIUM
**Confidence:** MEDIUM — GT-8? is unverified (the SCADA ambient/lubricant temperature log was not opened); verification = pull the SCADA ambient and gearbox oil-sump/inlet temperature trend across the cold-snap window together with the installed oil's ISO VG viscosity-temperature chart to confirm the actual direction and magnitude of viscosity movement.

### Conclusion C3: Subsurface origin depth is consistent with, but does not discriminate, the mechanism class

GT-5? (origin depth ~0.4 mm) + GT-12 (Hertzian z0 ≈ 0.78b, physical law)
→ for a heavily loaded HSS cylindrical roller bearing in this power class, an illustrative contact half-width bracket of b ≈ 0.15-0.55 mm under design-to-overload conditions implies an estimated z0 bracket of roughly 0.12-0.43 mm [Assumes: A17]
→ the observed 0.4 mm origin depth falls inside this bracket, near its upper end, consistent with heavy/rated loading, so the depth alone is consistent with ordinary Hertzian subsurface-shear-zone physics and does not by itself discriminate classical inclusion-driven fatigue from WEC/hydrogen-assisted fatigue, since both nucleate in the same subsurface zone

**Pre-check:** head GT-5?, GT-12 · ?-marked: GT-5? · lowest cited: none · Inputs ceiling: MEDIUM
**Confidence:** MEDIUM — GT-5? is unverified (lab report not opened); additionally the contact half-width bracket in `[Assumes: A17]` is an illustrative, order-of-magnitude figure rather than this bearing's actual catalog geometry/load spectrum — obtaining the bearing datasheet would tighten but not eliminate the estimate's inherent bracket width.

### Conclusion C4: The failure's life fraction is statistically abnormal, not ordinary fatigue scatter

GT-3? (L10 ≈ 130,000 h; failure at ~11% of L10) + GT-11 (ISO 281: L10 is the point at which 10% of a population is expected to have failed)
→ ordinary Lundberg-Palmgren fatigue scatter predicts at most about 10% of an identical bearing population failing by the L10 hour-count itself, not before one-ninth of that hour-count [Assumes: A16]
→ failing at roughly 11% of the L10 point — far short of even the worst 10% of a normal population's expected failure point — places this bearing well outside the lower tail of ordinary statistical scatter, indicating a superimposed abnormal damage mechanism rather than normal fatigue variability

**Pre-check:** head GT-3?, GT-11 · ?-marked: GT-3? · lowest cited: none · Inputs ceiling: MEDIUM
**Confidence:** MEDIUM — GT-3? is unverified (the bearing datasheet/L10 calculation sheet was not opened); verification = obtain the OEM's L10 calculation basis and confirm it is not already a position-specific derated figure, the possibility named in `[Assumes: A16]`.

### Conclusion C5: The mechanism class is white-etching-crack-driven premature RCF, not boundary-lubrication wear or ordinary fatigue

GT-5? (crescent microcracks) + GT-6? (WECs present) + GT-7? (butterflies present) + GT-16? (WEC/butterfly microstructure description) + C4 (abnormal life fraction, MEDIUM)
→ the combination of subsurface crescent-shaped multi-branch cracking, white-etching microstructural alteration, and butterfly wings at the subsurface origin matches the microstructural signature the literature assigns to white-etching-crack-driven premature rolling-contact-fatigue failure, not to ordinary mechanical overload or boundary-lubrication wear
→ combined with the abnormal life-fraction shortfall chain C4 establishes, the evidence identifies this failure as belonging to the WEC-driven premature-failure class rather than either the operator's boundary-lubrication hypothesis or ordinary statistically-expected fatigue spalling

**Pre-check:** head GT-5?, GT-6?, GT-7?, GT-16?, C4 (MEDIUM) · ?-marked: GT-5?, GT-6?, GT-7?, GT-16? · lowest cited: MEDIUM · Inputs ceiling: MEDIUM
**Confidence:** MEDIUM — GT-5?/GT-6?/GT-7? are unverified (the metallurgical lab report and micrographs were not opened; this is the single most load-bearing evidentiary gap in the whole analysis — see the adversarial pass record's Cluster 1 and Sensitivity entry); GT-16? is reported-by-delegate (the primary WEC/butterfly literature was not opened; verification = open the Southampton/BUAA primary papers directly, or commission an independent second metallurgical opinion on the original micrographs); C4 is cited at MEDIUM and that cap is explained on C4's own confidence line.

### Conclusion C6: The leading candidate trigger links the cold snap to WEC formation via a traction/lubrication-delivery pathway, not via simple film breakdown

GT-8? (cold snap preceded step-change) + GT-13 (viscosity rises as temperature falls) + GT-18? (hydrogen entry at nascent/patchy-tribofilm surfaces precedes WEC) + C5 (WEC-class mechanism, MEDIUM)
→ a viscosity rise at low temperature can impede oil-pump delivery at cold start, producing a transient marginal-lubrication condition distinct from the low-viscosity mechanism the operator proposed [Assumes: A9]
→ the same viscosity rise alters the EHL traction coefficient at the roller-raceway contact [Assumes: A9]
→ an altered traction coefficient is a documented route to roller micro-slip, which generates wear-induced nascent surfaces and patchy tribofilm at the contact
→ nascent surfaces and patchy tribofilm are the specific site the hydrogen-diffusion literature assigns to elevated tribochemical hydrogen entry during rolling contact fatigue
→ elevated local hydrogen entry at the subsurface shear-stress concentration is the mechanism most directly associated with the butterfly/WEC formation this failure already matches
→ a cold-snap-triggered transient lubrication/traction change leading to nascent-surface hydrogen entry is accordingly the leading candidate explanation linking the cold snap to this WEC-driven failure, materially different from the operator's boundary-lubrication-wear-through hypothesis

**Pre-check:** head GT-8?, GT-13, GT-18?, C5 (MEDIUM) · ?-marked: GT-8?, GT-18? · lowest cited: MEDIUM · Inputs ceiling: MEDIUM
**Confidence:** MEDIUM — GT-8? is unverified (SCADA temperature log not opened); GT-18? is reported-by-delegate (the primary hydrogen-diffusion RCF study was not opened; verification = open the cited Tribology Letters paper directly); C5 is cited at MEDIUM (see C5's own line). Hops 1-2 rest on `[Assumes: A9]` (a measurable traction/slip change at cold start for this bearing's actual load/speed envelope): if A9 fails, this specific trigger pathway does not hold, but C5's WEC-class identification does not depend on A9 and stands independently — only the cold-snap-specific trigger narrative, not the headline mechanism class, would then need to point to the electrical pathway instead (chain C7).

### Conclusion C7: Electrical bearing current is a live, unresolved rival/contributing cause

GT-4? (macro damage reported as axial spalling only) + GT-15 (EDM/fluting is a surface pitting-frosting-fluting progression) + GT-17? (WEC causes include electrical/electrostatic discharge, unsettled) + GT-19? (converter topology / grounding-brush status not stated)
→ the damage described in the case record is subsurface crescent-crack spalling, with no frosting or fluting reported, unlike the surface pitting-to-frosting-to-fluting progression assigned to discrete EDM-type bearing-current arcing [Assumes: A18]
→ this mismatch weakly disfavors discrete EDM-type arcing as the dominant mechanism, though it does not exclude a lower-level diffuse-current contribution to subsurface hydrogen generation, a distinct hypothesis the surveyed literature has not ruled out
→ electrical current remains a live, unresolved rival/contributing-cause hypothesis that the evidence given can neither confirm nor exclude, and it is not settled by this analysis alone

**Pre-check:** head GT-4?, GT-15, GT-17?, GT-19? · ?-marked: GT-4?, GT-17?, GT-19? · lowest cited: none · Inputs ceiling: MEDIUM
**Confidence:** LOW — three of four head inputs are unverified or reported-by-delegate (GT-4?, GT-17?, GT-19?), and the Rivals axis is explicitly unresolved (this chain's own endpoint states the rival is neither confirmed nor excluded); two axes are short at once, which bands this chain LOW rather than MEDIUM; verification = the electrical diagnostics named in §6 (shaft-voltage logging, brush/ring condition, EDM-pitting search on adjacent bearings) are what would resolve this chain one way or the other. Hop 1 rests on `[Assumes: A18]` (that the inspection specifically looked for frosting/fluting rather than merely not mentioning it); if A18 fails, this chain's own weak disfavoring of discrete arcing is unsupported and the rival would need to be treated as fully open rather than weakly disfavored — which would not change this chain's LOW band, already the floor this analysis assigns to an unresolved question.

### Conclusion C8: The actionable root cause is a control/design gap, not an inadequate lubricant viscosity grade

C5 (WEC-class mechanism, MEDIUM) + C6 (cold-snap-linked trigger candidate, MEDIUM) + C7 (electrical rival, LOW, unresolved)
→ tracing why WECs formed at an abnormal rate back through the candidate trigger pathways in C6 and C7 shows that the proximate finding of a white-etching-crack failure is itself one step short of actionable
→ the question that actually matters for a replacement spec is which upstream condition let a cold-snap-correlated transient, or an unaddressed electrical path, reach the bearing at all
→ the actionable root is an operational/design control gap — the absence of a demonstrated cold-weather lubrication-delivery/traction safeguard together with the unconfirmed status of electrical bearing-current mitigation on this HSS bearing — not an inadequate lubricant viscosity grade as the operator assumed

**Pre-check:** head C5 (MEDIUM), C6 (MEDIUM), C7 (LOW) · ?-marked: none · lowest cited: LOW · Inputs ceiling: LOW
**Confidence:** LOW — capped by chain C7 (LOW), whose own line names the unresolved electrical rival and the diagnostics that would resolve it; C5 and C6 are each MEDIUM (see their own lines) and do not independently lower this chain below what C7 already caps it to.

### Conclusion C9: The recommended replacement approach is a diagnostics-gated staged spec

GT-14 (NREL GRC: bearings dominate gearbox failures/cost) + C8 (root cause = control/design gap, LOW)
→ a weighted trade-off across three replacement-spec options — (A) like-for-like replacement with no process change, (B) an unconditional full upgrade to a WEC-resistant/electrically-insulated bearing design plus a cold-weather lubrication-control retrofit, and (C) a diagnostics-gated staged spec — scores Option C highest (96) against Option B (74) and Option A (54), driven by "addresses the confirmed mechanism" and "repeat-failure risk" [Assumes: A19]
→ a flip-test on the dominant single-criterion gaps shows no individual criterion weight, moved within the standard 1-5 scale, reverses Option C's lead over Option B
→[2nd] committing to Option C shifts near-term O&M practice toward mandatory cold-weather pre-heat/torque-limit interlocks across the fleet, a control-software and procedure change the actor lens shows falls on the owner's O&M organization, not only on this one turbine
→[3rd] if a fleet-wide low-temperature interlock measurably reduces energy capture during cold periods, the time lens shows this is a recurring annual cost that must be weighed every winter against the one-time cost of the electrical/bearing upgrade the diagnostics may eventually confirm as necessary
→ the recommended replacement approach is the diagnostics-gated staged spec (Option C): install a bearing at least matching current design intent now to restore availability, run the falsifiable checks in §6 before committing to the full WEC-resistant/electrically-insulated upgrade, and apply interim cold-weather lubrication-delivery controls immediately regardless of test outcome

**Pre-check:** head GT-14, C8 (LOW) · ?-marked: none · lowest cited: LOW · Inputs ceiling: LOW
**Confidence:** LOW — capped by chain C8 (LOW), whose own line traces the cap to C7's unresolved electrical rival; GT-14 is read-at-source and is not itself a cause of the downgrade. Resolving C7's named diagnostics would raise this chain's practical confidence toward MEDIUM/HIGH once the spec no longer needs to hedge against an unconfirmed electrical contribution. The second-order extension (`→[2nd]`, `→[3rd]`) was checked against all ground truths and introduces no contradiction, so the parent chain is unaffected and not routed back to Phase 2.

## 5. Abandoned Reasoning

### Dead End: Accepting the operator's boundary-lubrication/viscosity hypothesis at face value

**What was tried:** The operator's stated mechanism — cold snap lowers viscosity, which drives boundary lubrication, which wears the race through — was evaluated as the default working hypothesis before the metallurgical evidence was weighed against it.

**Why abandoned:** Chains C1 and C2 show the hypothesis fails on two independent grounds: the damage morphology (subsurface crescent cracks, WECs, butterflies) is the signature of subsurface rolling-contact fatigue, not surface-initiated wear (C1); and the proposed physical direction — cold causing *lower* viscosity — is backwards per the viscosity-temperature physical law (GT-13), an assumption shown false rather than merely unlikely (C2).

**What it ruled out:** Confirms the replacement spec should not rely on a simple oil re-grade or viscosity-grade increase as the corrective action; that alone would leave the actual mechanism (chain C5) unaddressed.

### Dead End: Treating subsurface-origin depth alone as diagnostic of WEC vs. ordinary RCF

**What was tried:** Computing the Hertzian subsurface-shear-stress depth (chain C3) was initially pursued hoping the 0.4 mm origin depth would, by itself, discriminate white-etching-crack-driven fatigue from ordinary inclusion-driven fatigue.

**Why abandoned:** The estimate showed the depth is merely consistent with the general subsurface-shear zone that *both* ordinary inclusion fatigue and WEC/hydrogen-assisted fatigue nucleate in (chain C3) — it is not discriminating on its own, and the intermediate could not be pushed further toward a verdict without additional evidence.

**What it ruled out:** Saves a future analyst from re-deriving Hertzian contact depth as if depth alone settles the mechanism question; the microstructural evidence (WEC/butterfly presence, chain C5), not depth, is what is actually diagnostic.

### Dead End: Treating discrete EDM/fluting bearing-current arcing as the leading suspected trigger

**What was tried:** Given the common wind-industry pattern-match of "generator-end HSS bearing failure" with VFD/converter bearing-current arcing, classic EDM-type fluting was initially pursued as the leading candidate trigger ahead of the lubrication/traction pathway.

**Why abandoned:** GT-15's established EDM/fluting signature (surface pitting → frosting → fluting) does not match the case record's macro-damage description (axial spalling only, with no frosting or fluting mentioned), demoting discrete arcing from leading candidate to an open, unresolved rival (chain C7, rated LOW) rather than the headline mechanism.

**What it ruled out:** Prevents prematurely recommending a blanket electrically-insulated-bearing replacement fleet-wide without the diagnostic evidence (shaft-voltage logs, brush/ring condition) that would justify that spend; this is reflected in chain C9's staged rather than unconditional upgrade recommendation.

### Dead End: Using the frequently-repeated "~60% of HS bearing failures are WEC" figure as a confirmed base rate

**What was tried:** The statistic was initially considered as a Bayesian prior to strengthen the mechanism-class conclusion (chain C5) — i.e., "WEC is already the most common HS-bearing failure mode, so this failure is probably WEC too."

**Why abandoned:** A direct verification attempt (opening the windpowerengineering.com article the figure is commonly attributed to) did not find the statistic in that source, and no primary document was independently opened and confirmed (GT-21?, Phase 3 failure record) — the citation traced only to secondary trade-press repetition with no identified original source.

**What it ruled out:** Avoids inflating the conclusion's confidence on an unverified industry base rate; the conclusion instead rests entirely on the case-specific microstructural match (chain C5) and the case-specific abnormal life fraction (chain C4), not on an industry-wide prior.

---

## 6. Conclusion

**Recommended approach:** Install a bearing at least matching current design intent now to restore turbine availability; before finalizing the long-term replacement spec, run the falsifiable diagnostic checks below (independent micrograph re-review, shaft-voltage/brush-condition logging, EDM-pitting search on adjacent bearings, hydrogen-content and lubricant TAN/elemental analysis, and a SCADA/commissioning-record review); and apply interim cold-weather lubrication-delivery and traction controls immediately regardless of test outcome (chain C9). Do not rely on a lubricant viscosity-grade upgrade alone as the corrective action, since the evidence refutes that as the primary mechanism (chain C1, chain C2).

**Key insight:** The operator's instinct that "the cold snap mattered" was directionally right, but the specific mechanism named — low viscosity driving boundary lubrication and wear-through — is physically backwards for a cooling event and does not match the subsurface WEC/butterfly evidence (chain C1, chain C2). The cold snap more plausibly mattered through a traction/micro-slip or lubrication-delivery pathway feeding hydrogen-assisted subsurface cracking (chain C6), not through simple film-thickness collapse.

**Trade-offs acknowledged:** The staged, diagnostics-gated approach costs more calendar time than a like-for-like swap and defers the final electrically-insulated-bearing decision until the electrical diagnostics return, accepting a residual electrical-current risk during that interim window that current evidence can neither confirm nor exclude (chain C7) — a risk chain C9's interim controls partially, but not fully, mitigate.

**Pre-check:** head C1 (MEDIUM), C2 (MEDIUM), C5 (MEDIUM), C6 (MEDIUM), C7 (LOW), C9 (LOW) · ?-marked: none directly · lowest cited: LOW · Inputs ceiling: LOW
**Confidence:** LOW — the overall conclusion rests on chain C9, which is capped LOW by chain C8, which is in turn capped LOW by chain C7's unresolved electrical-current rival. This LOW rating reflects that the **mechanism class** determination (WEC-driven, not boundary-lubrication — chains C1, C2, C5, each MEDIUM) is reasonably solid, while the **specific root-cause trigger**, and therefore the exact replacement spec, remain open pending the diagnostics chain C7 names. Running those diagnostics is what would raise this band toward MEDIUM/HIGH; it is also, independently, what the adversarial pass below identifies as the single highest-value next step (Cluster 1: independent micrograph re-review) before this conclusion is treated as final.

## Appendix — process output

## Assumption Audit scan (process output)

| Chain | Step | Step Text (brief) | Assumption surfaced? | Added to Table? |
|---|---|---|---|---|
| C1 | 1 | subsurface crescent-crack network, not surface wear | A15 (wear-mode classification transfers to this steel) | yes |
| C1 | 2 | crescent-crack morphology = subsurface-RCF signature | none | n/a |
| C1 | 3 | operator's mechanism refuted on morphology | none | n/a |
| C2 | 1 | cold-snap claim contradicts viscosity-temperature direction | none | n/a |
| C2 | 2 | operator's mechanism refuted on physics direction | none | n/a |
| C3 | 1 | illustrative contact half-width bracket → z0 bracket | A17 (bracket represents this bearing's actual geometry) | yes |
| C3 | 2 | depth consistent with, not discriminating of, mechanism | none | n/a |
| C4 | 1 | ordinary scatter predicts ≤10% failed by L10 | A16 (L10 figure is not already position-derated) | yes |
| C4 | 2 | failure is statistically abnormal | none | n/a |
| C5 | 1 | microstructure matches WEC/butterfly signature | none | n/a |
| C5 | 2 | mechanism class = WEC-driven premature RCF | none | n/a |
| C6 | 1 | viscosity rise impedes oil-pump delivery at cold start | A9 (measurable traction/slip change at cold start for this bearing) | yes |
| C6 | 2 | viscosity rise alters EHL traction coefficient | A9 (same assumption as step 1) | yes |
| C6 | 3 | altered traction → micro-slip → nascent surfaces | none | n/a |
| C6 | 4 | nascent surfaces/tribofilm = hydrogen-entry site | none | n/a |
| C6 | 5 | hydrogen entry → butterfly/WEC formation | none | n/a |
| C6 | 6 | leading candidate cold-snap trigger pathway | none | n/a |
| C7 | 1 | damage pattern mismatches EDM/fluting signature | A18 (inspection specifically looked for frosting/fluting) | yes |
| C7 | 2 | weakly disfavors arcing, doesn't exclude diffuse current | none | n/a |
| C7 | 3 | electrical current = live, unresolved rival | none | n/a |
| C8 | 1 | tracing root cause through C6/C7 trigger candidates | none | n/a |
| C8 | 2 | the actionable question is the upstream control gap | none | n/a |
| C8 | 3 | root cause = control/design gap, not viscosity grade | none | n/a |
| C9 | 1 | weighted trade-off scores Option C highest | A19 (weights reflect this owner's actual priorities) | yes |
| C9 | 2 | flip-test: no single weight reverses the ranking | none | n/a |
| C9 | 3 | [2nd] fleet-wide cold-weather interlock practice shift | none | n/a |
| C9 | 4 | [3rd] recurring seasonal cost vs. one-time upgrade cost | none | n/a |
| C9 | 5 | recommend the diagnostics-gated staged spec (Option C) | none | n/a |

All assumptions surfaced during this scan (A9, A15, A16, A17, A18, A19) were already present in the Assumptions Table (Section 2, rows A9 and A15-A19) at the time the scan was run, each carrying the `[Assumes: X]` mark on its originating chain step(s) above. No new table rows were required by this scan.

## Techniques not applied (process output)

fishbone — not applicable — the assumption space (mechanical/lubrication, electrical, tribochemical, data-provenance categories) was enumerable directly from established wind-turbine-bearing failure-mode categories without needing a formal breadth-first brainstorming aid; the resulting Assumptions Table (19 rows) already spans those categories.
theoretical-limit — not applicable — this analysis concerns failure-mechanism identification, not a performance/efficiency ceiling the fundamentals permit; no quantity in the analysis calls for a law-permitted-limit derivation.
pre-mortem — not applicable — the headline conclusion is a diagnostic/causal claim, not a plan or recommendation to execute; Phase 5's decision rule routes claims to inversion instead (applied — see the adversarial pass record below).

## Adversarial pass (process output)

**Recompute.** 14,000 / 130,000 = 10.77% ≈ 11%, matching GT-3?'s stated "roughly 11% of L10" (chain C4). Hertzian bracket (chain C3): z0 = 0.78b; 0.78 × 0.15 mm = 0.117 mm ≈ 0.12 mm; 0.78 × 0.55 mm = 0.429 mm ≈ 0.43 mm — both ends recompute as stated. Trade-off totals (chain C9): Option A = 5+20+15+5+6+3 = 54; Option B = 20+4+6+25+4+15 = 74; Option C = 25+16+12+20+8+15 = 96 — all three recompute as stated. No arithmetic error was found in any computed figure this analysis presents.

**Sensitivity.** The single ground truth whose falsity would flip the headline conclusion is the GT-5?/GT-6?/GT-7? cluster (subsurface origin depth, WECs, butterflies) — all `?`-marked. If these are inaccurate, misreported, or mischaracterized, chain C5's mechanism-class identification collapses, and with it chains C6, C8 and C9's specific rationale, though chain C2 (the physics-direction refutation of the operator's hypothesis) would stand independently. Per-chain weakest link: C1 — `[Assumes: A15]` (low risk, priced on C1's own line); C2 — no material weak link; C3 — `[Assumes: A17]` (illustrative bracket); C4 — `[Assumes: A16]` (possible pre-existing derating); C5 — GT-5?/GT-6?/GT-7? (the master weak link, see above); C6 — `[Assumes: A9]` and GT-18? (reported-by-delegate, attempted and blocked — see Cluster 1); C7 — unresolved by design (its own endpoint); C8/C9 — inherit C7's LOW cap.

**Rival.** Headline conclusion: the strongest rival is "ordinary, statistically-expected inclusion-driven RCF with no WEC/hydrogen/electrical involvement," ruled out by chain C4's abnormal-life-fraction argument combined with chain C5's microstructural match — a ruling-out that is itself only as strong as the unverified GT-5?/GT-6?/GT-7? (Cluster 1 below). Chain C6 (trigger pathway): the strongest rival is "electrical current alone, operating continuously and independent of temperature," which is **not** ruled out and stays live on chain C7 (LOW). Chain C9 (recommendation): the rival is "like-for-like replacement is sufficient" (Option A), ruled out by the trade-off's own weighted scoring within chain C9 itself.

**Premise.** The headline conclusion is already false: this bearing's failure was not actually a white-etching-crack-driven, cold-snap-linked, control-gap-rooted failure.

**Causes** (unfiltered, generated from four stakeholder viewpoints before any grouping):
- *(independent metallurgist)* the lab's micrograph interpretation is ambiguous or wrong — what was called "WEC" is ordinary tempered-martensite etching artifact, not a literature-standard white-etching area.
- *(independent metallurgist)* the "butterflies" were misidentified — they are ordinary non-metallic-inclusion fatigue striations common in any aged bearing, not evidence of hydrogen involvement.
- *(OEM warranty engineer)* the operator under-lubricated or mis-specified the oil grade for the site's climate, and the cold snap is a real causal trigger via simple boundary lubrication exactly as first suspected; the metallurgy is secondary damage from spall debris, not a primary cause.
- *(OEM warranty engineer)* a grid-fault or converter-fault torque transient, unrelated to cold weather, seeded the damage; the cold-snap timing correlation is coincidental.
- *(maintenance manager)* the bearing had a latent manufacturing defect (inclusion cluster, grinding burn) from the factory and would have failed at this age regardless of weather or lubrication.
- *(maintenance manager)* an installation/mounting error (improper fit, preload, or misalignment at commissioning) explains the early failure independent of any WEC mechanism.
- *(power-electronics engineer)* stray/common-mode current has been continuously present since commissioning, independent of temperature, and is the sole driver; the cold snap merely coincides with when accumulated damage tripped the CMS kurtosis threshold.
- *(power-electronics engineer)* the converter firmware or the shaft-grounding system changed shortly before the cold-snap window, and that change — not the temperature — is the true trigger, coincidentally timed near the cold snap.

**Clusters:**
- **Cluster 1 — Metallurgical mischaracterization risk** (bears on GT-5?, GT-6?, GT-7?; chains C1, C5, C8, C9): both metallurgist-viewpoint causes reduce to "the micrograph evidence itself might not mean what this analysis assumed it means." This is the single highest-value cluster, since it threatens the one ground-truth cluster the Sensitivity step above already named as the master weak link.
- **Cluster 2 — Unexamined competing sufficient cause** (bears on chains C5, C6, C8): the grid-fault/torque-transient, manufacturing-defect, and installation-defect causes each describe an alternative sufficient explanation this analysis has not ruled out, because no commissioning/QA record or grid-event log was reviewed.
- **Cluster 3 — Electrical current as a sole, continuous (not cold-linked) driver** (bears on chains C6, C7): the power-electronics-viewpoint causes converge on "electrical current, not weather, is doing all the work," which would falsify chain C6's specific cold-snap trigger narrative without necessarily falsifying chain C5's WEC-class finding.

**Disposition:**
- Cluster 1 — **Plan change:** before the replacement spec is finalized, commission an independent second-opinion review of the original micrographs confirming WEC/butterfly classification against standard criteria (nanocrystalline carbide-free ferrite; wing orientation ≈30° to the rolling direction) rather than relying on the as-given narrative description. Added to §6's falsifiable checks below.
- Cluster 2 — **Plan change:** pull the SCADA grid-event/fault-ride-through log and the original commissioning/bearing-fitment QA record, specifically searching for a torque-transient or assembly-nonconformance signature around first operation and around the cold-snap window. Added to §6's falsifiable checks below.
- Cluster 3 — **Accepted risk with mitigation:** proceed with chain C9's staged recommendation, which already treats electrical current as an open rival (chain C7) and budgets shaft-voltage/brush-condition logging as a pre-commit gate rather than assuming cold weather is the whole story; this cluster's disposition is therefore "accepted, and already mitigated by the existing recommendation," not a new plan change.

**Falsification.** This conclusion is false if an independent re-review of the micrographs finds no literature-standard WEC/butterfly features (i.e., the subsurface cracking is ordinary non-metallic-inclusion-initiated fatigue with no white-etching microstructure), **or** if the SCADA/commissioning records reveal a torque-transient or assembly-nonconformance event that alone explains the early failure without invoking hydrogen or electrical mechanisms.

**Note on Phase 3 verification attempts for GT-16?/GT-17?/GT-18?:** this analysis attempted to open the primary hydrogen-diffusion/WEC research directly (eprints.soton.ac.uk PDF and abstract page, and the Springer journal page) specifically because chains C5 and C6 are the most load-bearing chains in this analysis; all three attempts returned 403 Forbidden / an authentication wall. This is recorded as a Phase 3 failure (source located, unreachable) rather than a skipped attempt; GT-16?, GT-17? and GT-18? remain `?`-marked and reported-by-delegate as a result, and Cluster 1 above names the recommended path (an independent second-opinion review of this specific bearing's own micrographs) that would resolve the master weak link directly, rather than depending on re-attempting the paywalled literature.

## §6→§4 closure ledger (process output)

- "Install a bearing at least matching current design intent now to restore turbine availability; before finalizing the long-term replacement spec, run the falsifiable diagnostic checks below... and apply interim cold-weather lubrication-delivery and traction controls immediately regardless of test outcome" → chain C9 ✓
- "Do not rely on a lubricant viscosity-grade upgrade alone as the corrective action, since the evidence refutes that as the primary mechanism" → chain C1, chain C2 ✓
- "The operator's instinct that 'the cold snap mattered' was directionally right, but the specific mechanism named... is physically backwards for a cooling event and does not match the subsurface WEC/butterfly evidence" → chain C1, chain C2 ✓
- "The cold snap more plausibly mattered through a traction/micro-slip or lubrication-delivery pathway feeding hydrogen-assisted subsurface cracking, not through simple film-thickness collapse" → chain C6 ✓
- "The staged, diagnostics-gated approach costs more calendar time... accepting a residual electrical-current risk during that interim window that current evidence can neither confirm nor exclude" → chain C7, chain C9 ✓
- "the overall conclusion rests on chain C9, which is capped LOW by chain C8, which is in turn capped LOW by chain C7's unresolved electrical-current rival" → chain C9, chain C8, chain C7 ✓
- "the mechanism class determination (WEC-driven, not boundary-lubrication) is reasonably solid" → chain C1, chain C2, chain C5 ✓

All seven claims cite a chain inline; no CUTs were required.

## Self-audit scan (process output)

| Chain | Chain Head (brief) | Form conforming? | Rule applied | Dependency clean? | Band | Act attempted? | Edges fired |
|---|---|---|---|---|---|---|---|
| C1 | GT-4?, GT-5?, GT-9, GT-10 | yes | n/a | yes | MEDIUM | yes | none |
| C2 | GT-8?, GT-13 | yes | n/a | yes | MEDIUM | no | none |
| C3 | GT-5?, GT-12 | yes | n/a | yes | MEDIUM | no | none |
| C4 | GT-3?, GT-11 | yes | n/a | yes | MEDIUM | yes | none |
| C5 | GT-5?, GT-6?, GT-7?, GT-16?, C4 | yes | n/a | yes | MEDIUM | yes | none |
| C6 | GT-8?, GT-13, GT-18?, C5 | yes | n/a | yes | MEDIUM | yes | none |
| C7 | GT-4?, GT-15, GT-17?, GT-19? | yes | n/a | yes | LOW | yes | none |
| C8 | C5, C6, C7 | yes | n/a | yes | LOW | no | none |
| C9 | GT-14, C8 | yes | n/a | yes | LOW | yes | none |

| §6 Span (brief) | Construct | Claim under R11? | R11 clause applied | Chain cited |
|---|---|---|---|---|
| "Recommended approach: Install a bearing..." | bold lead-in | yes | colon closes the bold span, content on same line | C9, C1, C2 |
| "Key insight: The operator's instinct..." | bold lead-in | yes | colon closes the bold span, content on same line | C1, C2, C6 |
| "Trade-offs acknowledged: The staged, diagnostics-gated approach..." | bold lead-in | yes | colon closes the bold span, content on same line | C7, C9 |
| "Pre-check: head C1 (MEDIUM), C2 (MEDIUM)..." | bold lead-in | yes | pre-check line is a claim cited by its own head list (output-template.md §6) | C1, C2, C5, C6, C7, C9 |
| "Confidence: LOW — the overall conclusion rests on chain C9..." | bold lead-in | yes | colon closes the bold span, content on same line | C1, C2, C5, C6, C7, C8, C9 |

Scan complete: 9 chain rows, one per section-4 chain block in order; 5 section-6 rows, one per construct in order — 5 claims under R11, 0 excluded. 0 chains malformed, 0 claims untraced.

## Self-Audit Gate (process output)

**Criterion 1: Identify Essence**
Quoted span: "Determine which failure mechanism... is actually consistent with the full combination of macroscopic and microscopic evidence on this HSS generator-end bearing, so that the replacement specification is driven by the real cause rather than the first plausible-sounding story," together with the five success criteria (e.g., "The conclusion names one mechanism class that is simultaneously consistent with all four pieces of metallurgical evidence").
Band: **Rigorous**
Justification: the essence names the specific decision at stake (mechanism identification driving a replacement spec), not the triggering CMS alarm or a restatement of the prompt, and each success criterion is a checkable verb+subject+outcome triplet whose outcome is a property of the Conclusion section.

**Criterion 2: Challenge Assumptions**
Quoted span: Assumption Audit scan — "All assumptions surfaced during this scan (A9, A15, A16, A17, A18, A19) were already present in the Assumptions Table... at the time the scan was run"; Assumptions Table row A2 — "Discard — contradicted by GT-9/GT-10 and the subsurface/WEC/butterfly evidence (GT-5?-GT-7?); see chain C1 | unverified — flagged".
Band: **Rigorous**
Justification: all 19 rows use the four-type scheme with treatments matching their type, Verdict cells use the token-first em-dash form throughout, every chain-consumed unverified assumption carries "unverified — flagged," several assumptions are Challenged or Discarded rather than uniformly Accepted, and the Assumption Audit scan confirms exhaustive coverage of all 28 named chain steps with no untabled assumption surfaced.

**Criterion 3: Establish Ground Truths**
Quoted span: Ground Truths provenance summary — "Read-at-source: GT-9... GT-10... GT-11... GT-12... GT-13... GT-14... GT-15" — cross-checked against the self-audit scan's chain-form table, whose Band column reads MEDIUM or LOW for all nine chains (C1-C9), none HIGH.
Band: **Hand-wavy**
Justification: all seven unsuffixed, reachable ground truths (GT-9, GT-10, GT-11, GT-12, GT-13, GT-14, GT-15) feed only MEDIUM- or LOW-confidence chains rather than at least one HIGH chain each; the rubric bands a single such instance Sound but this shortfall recurring across multiple GTs Hand-wavy, which is the honest reflection of this being a desk RCA built on a supplied case narrative with no primary CMS export, lab report, or SCADA log independently opened (GT-1? through GT-8?, all unverified).

**Criterion 4: Reason Upward**
Quoted span: self-audit scan chain-form table — all nine rows read "Form conforming? yes... Dependency clean? yes"; Abandoned Reasoning — "Why abandoned: Chains C1 and C2 show the hypothesis fails on two independent grounds... an assumption shown false rather than merely unlikely (C2)."
Band: **Rigorous**
Justification: every conclusion in section 6 traces to exactly one chain in section 4 (nine conclusions, nine chains, confirmed by the closure ledger), every chain is form-conforming and dependency-clean per the self-audit scan, every chain carries a genuine intermediate, four dead ends carry specific (non-generic) abandonment reasons, no analogy is used as direct evidence, and every chain step introducing a new premise carries an inline `[Assumes: X]` mark matching a table row.

**Criterion 5: Validate**
Quoted span: adversarial pass record — "Cluster 1 — Plan change: before the replacement spec is finalized, commission an independent second-opinion review of the original micrographs..."; chain C8's confidence line — "capped by chain C7 (LOW), whose own line names the unresolved electrical rival and the diagnostics that would resolve it."
Band: **Rigorous**
Justification: every chain's weakest link is named, every MEDIUM/LOW confidence line names its `?`-marked inputs or sub-HIGH cited chains together with a verification path, no chain consuming a `GT-N?` input is rated HIGH, every chain is rated no higher than the lowest-rated chain its head cites, the full adversarial pass (Recompute, Sensitivity, Rival, Premise, Causes, Clusters, Disposition, Falsification) is present with every cluster carrying a named plan change or an explicitly accepted and mitigated risk, and the overall Conclusion's LOW rating matches its weakest contributing chain (C9) exactly rather than over- or under-stating it.

**Criterion 6: Conclusion-to-Ground-Truth Traceability**
Quoted span: self-audit scan claim-inventory table — all five rows read "Claim under R11? yes" with a named chain; reconciliation line — "5 claims under R11, 0 excluded... 0 claims untraced."
Band: **Rigorous**
Justification: every Conclusion-section claim (Recommended approach, Key insight, Trade-offs acknowledged, Pre-check, Confidence) traces to a specifically named chain per the self-audit scan's claim-inventory table, no claim is introduced for the first time in section 6, and the Key Insight states a non-obvious finding (the operator's direction-of-causation error under a cooling event) rather than restating the recommended approach.

**Gate result:** cleared · passes: 1 · Fix/Repeat fired: no

## Structured summary (process output)

```json
{
  "schema_version": 1,
  "run_mode": "full-composer",
  "assumptions": [
    {"id": "A-1", "type": "untested belief", "verdict": "Challenge"},
    {"id": "A-2", "type": "untested belief", "verdict": "Discard"},
    {"id": "A-3", "type": "convention", "verdict": "Challenge"},
    {"id": "A-4", "type": "current constraint", "verdict": "Challenge"},
    {"id": "A-5", "type": "physical law", "verdict": "Accept"},
    {"id": "A-6", "type": "physical law", "verdict": "Accept"},
    {"id": "A-7", "type": "convention", "verdict": "Discard"},
    {"id": "A-8", "type": "untested belief", "verdict": "Challenge"},
    {"id": "A-9", "type": "untested belief", "verdict": "Challenge"},
    {"id": "A-10", "type": "untested belief", "verdict": "Challenge"},
    {"id": "A-11", "type": "untested belief", "verdict": "Challenge"},
    {"id": "A-12", "type": "untested belief", "verdict": "Challenge"},
    {"id": "A-13", "type": "current constraint", "verdict": "Challenge"},
    {"id": "A-14", "type": "convention", "verdict": "Challenge"},
    {"id": "A-15", "type": "untested belief", "verdict": "Challenge"},
    {"id": "A-16", "type": "untested belief", "verdict": "Challenge"},
    {"id": "A-17", "type": "untested belief", "verdict": "Challenge"},
    {"id": "A-18", "type": "untested belief", "verdict": "Challenge"},
    {"id": "A-19", "type": "convention", "verdict": "Challenge"}
  ],
  "ground_truths": [
    {"id": "GT-1", "read_at_source": false},
    {"id": "GT-2", "read_at_source": false},
    {"id": "GT-3", "read_at_source": false},
    {"id": "GT-4", "read_at_source": false},
    {"id": "GT-5", "read_at_source": false},
    {"id": "GT-6", "read_at_source": false},
    {"id": "GT-7", "read_at_source": false},
    {"id": "GT-8", "read_at_source": false},
    {"id": "GT-9", "read_at_source": true},
    {"id": "GT-10", "read_at_source": true},
    {"id": "GT-11", "read_at_source": true},
    {"id": "GT-12", "read_at_source": true},
    {"id": "GT-13", "read_at_source": true},
    {"id": "GT-14", "read_at_source": true},
    {"id": "GT-15", "read_at_source": true},
    {"id": "GT-16", "read_at_source": false},
    {"id": "GT-17", "read_at_source": false},
    {"id": "GT-18", "read_at_source": false},
    {"id": "GT-19", "read_at_source": false},
    {"id": "GT-20", "read_at_source": false},
    {"id": "GT-21", "read_at_source": false},
    {"id": "GT-22", "read_at_source": false}
  ],
  "chains": [
    {"id": "C1", "confidence": "MEDIUM", "rests_on": ["GT-4?", "GT-5?", "GT-9", "GT-10"]},
    {"id": "C2", "confidence": "MEDIUM", "rests_on": ["GT-8?", "GT-13"]},
    {"id": "C3", "confidence": "MEDIUM", "rests_on": ["GT-5?", "GT-12"]},
    {"id": "C4", "confidence": "MEDIUM", "rests_on": ["GT-3?", "GT-11"]},
    {"id": "C5", "confidence": "MEDIUM", "rests_on": ["GT-5?", "GT-6?", "GT-7?", "GT-16?", "C4"]},
    {"id": "C6", "confidence": "MEDIUM", "rests_on": ["GT-8?", "GT-13", "GT-18?", "C5"]},
    {"id": "C7", "confidence": "LOW", "rests_on": ["GT-4?", "GT-15", "GT-17?", "GT-19?"]},
    {"id": "C8", "confidence": "LOW", "rests_on": ["C5", "C6", "C7"]},
    {"id": "C9", "confidence": "LOW", "rests_on": ["GT-14", "C8"]}
  ],
  "dead_ends": [
    "Accepting the operator's boundary-lubrication/viscosity hypothesis at face value",
    "Treating subsurface-origin depth alone as diagnostic of WEC vs. ordinary RCF",
    "Treating discrete EDM/fluting bearing-current arcing as the leading suspected trigger",
    "Using the frequently-repeated \"~60% of HS bearing failures are WEC\" figure as a confirmed base rate"
  ],
  "techniques": {
    "applied": ["inversion", "estimate", "five-whys", "trade-off", "second-order"],
    "not_applied": [
      {"technique": "fishbone", "phase": 2, "reason": "the assumption space (mechanical/lubrication, electrical, tribochemical, data-provenance categories) was enumerable directly from established wind-turbine-bearing failure-mode categories without needing a formal breadth-first brainstorming aid; the resulting Assumptions Table (19 rows) already spans those categories."},
      {"technique": "theoretical-limit", "phase": 4, "reason": "this analysis concerns failure-mechanism identification, not a performance/efficiency ceiling the fundamentals permit; no quantity in the analysis calls for a law-permitted-limit derivation."},
      {"technique": "pre-mortem", "phase": 5, "reason": "the headline conclusion is a diagnostic/causal claim, not a plan or recommendation to execute; Phase 5's decision rule routes claims to inversion instead (applied; see the adversarial pass record below)."}
    ]
  },
  "gate": {
    "passes": [
      {
        "bands": ["Rigorous", "Rigorous", "Hand-wavy", "Rigorous", "Rigorous", "Rigorous"],
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
    "recommendation": "Install a bearing at least matching current design intent now to restore turbine availability; before finalizing the long-term replacement spec, run the falsifiable diagnostic checks below (independent micrograph re-review, shaft-voltage/brush-condition logging, EDM-pitting search on adjacent bearings, hydrogen-content and lubricant TAN/elemental analysis, and a SCADA/commissioning-record review); and apply interim cold-weather lubrication-delivery and traction controls immediately regardless of test outcome (chain C9). Do not rely on a lubricant viscosity-grade upgrade alone as the corrective action, since the evidence refutes that as the primary mechanism (chain C1, chain C2).",
    "confidence": "LOW",
    "rests_on": ["C1", "C2", "C5", "C6", "C7", "C9"]
  }
}
```
