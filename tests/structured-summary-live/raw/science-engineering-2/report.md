**Disclosed:** One re-entry edge fired: the Self-Audit Gate's Fix/Repeat loop. On the first pass Criterion 3 scored Hand-wavy and Criteria 1, 2 and 4 scored Sound. The Fix made four changes:

- rewrote success criterion 5 so it can be checked in §6
- added assumption rows A-20 to A-23
- added chains C9 and C10 (HIGH), which consume the read-at-source GT-5 and GT-7
- added GT-15? to C7's head

The gate then cleared on the second pass. The details are in the appendix under Self-Audit Gate.

## Answer

**Recommendation:** Reject the lubricant-viscosity specification. Fit a dimensionally interchangeable WEC-resistant bearing (black-oxide and/or case-carburized) now, and lock no fleet specification until a driver investigation reports (chain C8).

**Band (from §6):** MEDIUM (chains C1, C8)

**Would change it:** The metallographer confirming WEC in sections away from the spall, and confirming the origin depth and beach-mark direction, would settle the mechanism (chains C3, C7). Bearing-maker or field data on how often WEC occurs in black-oxide and case-carburized bearings would settle option D's benefit (chain C8).

## 1. Problem Essence

**Core problem:** What physical mechanism initiated and propagated the inner-race damage on this HSS cylindrical roller bearing at about 10.8% of its L10 life, does the operator's "cold-snap low viscosity → boundary lubrication → wore through" hypothesis survive contact with the evidence, and what replacement specification would act on the actual mechanism rather than the hypothesised one?

The triggering event (a kurtosis step at ~14,000 h) is a symptom; the operator's hypothesis is a candidate cause; neither is the question. The question is mechanism → driver → specification.

**Success criteria:**

1. The operator's hypothesis is either supported or refuted, with each step of the verdict traceable to a named ground truth.
2. The failure mechanism class (surface-initiated wear/distress vs. subsurface-initiated rolling-contact fatigue, and classical vs. white-etching-crack type) is identified from the reported evidence, with the evidence that discriminates them named.
3. The driver of the mechanism is either identified or explicitly declared undetermined, with the observations that would discriminate among candidate drivers named.
4. The replacement-specification recommendation acts on the identified mechanism; the option set includes doing nothing and at least one composite (part bearing change, part driver investigation/correction), and the recommendation may be any of them.
5. Every figure the Conclusion states cites a §4 chain whose hops show that figure's arithmetic, and the figure recomputes when redone independently of the chain text.

---

## 2. Assumptions Table

| Assumption | Type | Treatment | Verdict | Verification |
|------------|------|-----------|---------|--------------|
| A-1: A cold snap lowers the lubricant's viscosity (operator's premise) | untested belief | Verify or flag | Discard — contradicted by GT-1 and GT-2: liquid viscosity rises as temperature falls (chain C1) | GT-1, GT-2 read at source |
| A-2: Boundary lubrication (λ < 1) drove the damage | untested belief | Verify or flag | Discard — boundary-regime damage is surface-initiated; the reported origin is 0.4 mm subsurface (chain C3) | unverified — flagged; rests on GT-10?, GT-8? |
| A-3: The race "wore through" | untested belief | Verify or flag | Discard — a spall bounded by crescent beach marks radiating from a subsurface origin is progressive fatigue fracture, not material removal by wear (chain C3) | unverified — flagged; GT-14?, GT-8? |
| A-4: Liquid lubricant viscosity decreases monotonically with rising temperature | physical law | Accept as ground-truth candidate | Accept — read at source as GT-1, and the Walther form GT-2 is monotone for B > 0 | GT-1, GT-2 |
| A-5: Elastic Hertz line-contact theory governs the subsurface stress field under a roller | physical law | Accept as ground-truth candidate | Accept — governing relations read at source (GT-3); depth-of-max-shear factor recalled and recomputed but not read (GT-4?) | GT-3; GT-4? flagged |
| A-6: "Well short of L10" is itself evidence of an abnormal failure | convention | Challenge before use | Challenge — L10 is a 90%-survival population rating (GT-5), so 10% of a population is expected to fail before it; an early single failure is abnormal only by probability, which C5 quantifies | GT-5 |
| A-7: Classical RCF lives follow a 2-parameter Weibull with slope e between 9/8 and 1.5 | untested belief | Verify or flag | Challenge — used only to bracket a probability in C5; recalled Lundberg-Palmgren values, not read | unverified — flagged GT-6? |
| A-8: The reported findings (0.4 mm subsurface origin, beach marks, WEC, butterflies, axial spall) are accurate and were taken through the true origin | untested belief | Verify or flag | Accept — used, flagged; this analysis did not see the part or sections | unverified — flagged GT-8? |
| A-9: The gearbox oil is ISO VG 320 (ν40 = 320 cSt; ν100 ≈ 24 cSt mineral or ≈ 35 cSt PAO) running at a thermostatically held sump temperature of ~55–75 °C | untested belief | Verify or flag | Challenge — used only for the magnitude illustration in C2; the direction result (C1) does not depend on it | unverified — flagged GT-12? |
| A-10: HSS CRB geometry gives an effective contact radius R of 8.75–16.67 mm (roller Ø 20–40 mm, inner-raceway Ø 140–200 mm) and HSS speed 1,000–1,800 rpm | untested belief | Verify or flag | Challenge — bracket only; replace with the bearing drawing values | unverified — flagged GT-13? |
| A-11: The replacement must be dimensionally interchangeable (bore, OD, width, fit) with the existing housing and shaft | current constraint | Record expiry | Accept — expires if the gearbox OEM issues a superseding design or the gearbox is replaced; until then it is a fit constraint, not a physical one | operator constraint (stated: spec must support a replacement decision) |
| A-12: Black-oxide-coated and/or case-carburized bearings reduce WEC incidence in wind HSS positions | untested belief | Verify or flag | Challenge — read attempted, failed (Phase 3 failure records); scores resting on it carry the `?` | unverified — flagged GT-11? |
| A-13: At least one of the WEC drivers named in GT-7 (hydrogen, electrical current, sliding) is operating in this turbine | untested belief | Verify or flag | Challenge — which one is undetermined from the evidence given; discriminating observations named in C6 | unverified — flagged |
| A-14: Replacing like-for-like restores design life because the failure was a statistical early-tail event | convention | Challenge before use | Discard — a WEC morphology is not the classical RCF mode L10 models (GT-5, GT-7), so like-for-like reinstalls the same susceptibility under the same drivers (chains C5, C6) | GT-5, GT-7 |
| A-15: The white-etching cracks predate the spall (they are the initiation network, not a post-spall artefact of over-rolling debris) | untested belief | Verify or flag (load-bearing; surfaced by Phase 5 inversion) | Accept — GT-7 (read) characterises WEC as networks that commence subsurface in the initial phases of formation, so a WEC network is by definition a pre-spall feature; the residual question is only whether the reported features are correctly identified as WEC, which is GT-8?'s `?` | GT-7; observation part unverified — flagged via GT-8? |
| A-16: No surface-initiated origin elsewhere on the raceway was missed by the sectioning | untested belief | Verify or flag (load-bearing; surfaced by Phase 5 inversion) | Challenge — load-bearing for C3; full-raceway inspection and a second section plane would settle it | unverified — flagged |
| A-17: Cold-weather operation can raise roller-set slip (skidding) in a lightly loaded high-speed CRB because a thicker, higher-viscosity film raises cage/roller drag | untested belief | Verify or flag (surfaced by the Phase 4 Assumption Audit) | Challenge — plausible inversion of the operator's cold-snap link; not verified here | unverified — flagged |
| A-18: Nominal HSS raceway contact pressure p0 lies between 1.0 and 2.0 GPa | untested belief | Verify or flag (surfaced by the Phase 4 Assumption Audit on C4) | Challenge — bracket only; the gearbox load spectrum would replace it | unverified — flagged |
| A-19: A black-oxide conversion layer does not electrically insulate the bearing against shaft current | untested belief | Verify or flag (surfaced by the Phase 4 Assumption Audit on C8's second-order extension) | Challenge — the layer is a thin conversion coating, not a specified insulator; if wrong, the stray-current recurrence risk on C8 falls | unverified — flagged |
| A-20: EHL film thickness scales as roughly (η0·u)^0.7 and operating films are 0.1–1 µm | untested belief | Verify or flag (surfaced by the Fix pass of the Assumption Audit on C2/C3) | Challenge — used for magnitude only; read attempt failed (Phase 3 record on GT-9?) | unverified — flagged GT-9? |
| A-21: Boundary-regime damage (wear, scuffing, micropitting) acts within ~20 µm of the surface | untested belief | Verify or flag (surfaced by the Fix pass of the Assumption Audit on C3) | Challenge — load-bearing for C3's depth comparison; the 20× margin tolerates a several-fold error | unverified — flagged GT-10? |
| A-22: Crescent beach marks record progressive cyclic crack growth from their origin | untested belief | Verify or flag (surfaced by the Fix pass of the Assumption Audit on C3) | Challenge — standard fractography reading; not read here | unverified — flagged GT-14? |
| A-23: WEC failures in wind HSS bearings cluster at roughly 5–20% of calculated L10 | untested belief | Verify or flag (surfaced by the Fix pass of the Assumption Audit on C7) | Challenge — supporting only; GT-7's source does not state timing | unverified — flagged GT-15? |

**Cause-category brainstorm for the WEC driver (fishbone, 6M set, locked before brainstorming; every branch enters the table above as part of A-13 / A-17 as an untested belief):**

- **Machine** — stray electrical current through the generator-end bearing (DFIG converter common-mode voltage, failed shaft grounding or insulated coupling); roller skidding at low load / high speed. Discriminating observation: electrical-discharge craters or frosting/fluting on raceways and rollers under SEM; grounding-brush and coupling-insulation resistance check. Skidding: cage wear and smearing bands on rollers, low-load hours in SCADA.
- **Method (operation)** — transient torque reversals and emergency stops / grid events producing short overloads. Discriminating observation: SCADA count of e-stops and grid-loss events vs. sister turbines.
- **Material** — through-hardened steel, inclusion population (butterflies nucleate at inclusions), tensile hoop stress from inner-ring interference fit. Discriminating observation: inclusion rating of the failed ring; XRD residual-stress profile; heat-treatment record.
- **Measurement** — CMS kurtosis threshold and sensor placement determine *when* the damage was found, not why. Not a causal branch; recorded and not drilled.
- **Man (assembly)** — fit/press-fit error raising hoop stress. Discriminating observation: measured shaft and bore dimensions vs. drawing.
- **Mother Nature** — cold-snap condensation raising water in oil (a hydrogen source per GT-7); cold-start skidding (A-17). Discriminating observation: oil-analysis water ppm history across the cold months; thermal-desorption hydrogen measurement on the failed ring.

No single observation in the problem statement discriminates among these branches; that is a finding (C6), not a gap to be filled by picking the most plausible one.

---

## 3. Ground Truths

- **GT-1** Liquid viscosity "usually decreases with increasing temperature", because higher temperature gives molecules more thermal energy to overcome intermolecular attraction — source: Wikipedia, "Temperature dependence of viscosity"; read-at-source: quoted passages "In liquids it usually decreases with increasing temperature" and "Increasing temperature results in a decrease in viscosity because a larger temperature means particles have greater thermal energy…". Type: physical law (published regularity).
- **GT-2** Lubricant kinematic viscosity follows the Walther relation log10(log10(ν + 0.7)) = A − B·log10 T, with λ = 0.7 standard when two temperatures are specified — source: same article; read-at-source: quoted "The Walther formula is typically written in the form log₁₀(log₁₀(ν + λ)) = A − B log₁₀ T" and "a standard value of λ = 0.7 is normally assumed". Type: definition / empirical law. Because B > 0 for every real oil fitted to ν40 > ν100, ν falls monotonically with T.
- **GT-3** Parallel-cylinder (line) Hertz contact: 1/R = 1/R1 + 1/R2; F ≈ (π/4)E*·L·d; a = √(R·d); p0 = √(E*·F/(π·L·R)) — source: Wikipedia, "Contact mechanics", section on contact between two parallel cylinders; read-at-source: formulas quoted from that section. Derived identity used below (algebra from GT-3 only): from F/L = πRp0²/E* and a² = R·d = 4FR/(πE*L), a² = 4R²p0²/E*², so **b = 2·R·p0/E*** (b ≡ a, the half-width).
- **GT-4?** For line contact the maximum subsurface (Tresca) shear on the load axis is τ ≈ 0.300·p0 at depth z ≈ 0.786·b — unverified: recalled from the McEwen (1949) / Johnson *Contact Mechanics* §4.2 solution. **Phase 3 failure records:** (i) Wikipedia "Contact mechanics" opened — citation does not support the claim (it gives only the sphere value z ≈ 0.49a); (ii) amesweb.info Hertzian-contact page opened — citation does not support the claim (factors not on the page). Independent recomputation from the McEwen axis stresses σx/p0 = −[(1+2ζ²)/√(1+ζ²) − 2ζ], σz/p0 = −1/√(1+ζ²), τ = |σx − σz|/2, scanned at ζ = z/b step 0.0001: max τ/p0 = 0.3003 at ζ = 0.7862. The recomputation confirms the recalled factor but the stress expressions themselves were recalled, so the `?` stays.
- **GT-5** L10 is the basic life at 90% reliability — "no more than 10% of bearings are expected to have failed"; life exponent p = 10/3 (3.33) for roller bearings; bearing life is defined only statistically over populations — source: Wikipedia, "Rolling-element bearing", "Life calculation models"; read-at-source: quoted passages. Type: convention (ISO 281 definition).
- **GT-6?** Classical subsurface RCF lives follow a 2-parameter Weibull, F(t) = 1 − 0.9^((t/L10)^e), with slope e ≈ 9/8 (line contact, Lundberg-Palmgren) to 1.5 — unverified: recalled; the read GT-5 source does not contain Weibull terms (it says "the article does not contain specific Weibull distribution terminology").
- **GT-7** White-etching cracks are "sub-surface white crack networks" that "commence at subsurface during the initial phases of their formation, particularly at non-metallic inclusions"; contributing factors named are hydrogen embrittlement, electrical current, and sliding contact, with lubricant-derived hydrogen generation discussed — source: Wikipedia, "White etching cracks"; read-at-source: quoted passages. The article does not state WEC timing relative to L10, and does not discuss butterflies or mitigations.
- **GT-8?** Case findings as reported: CMS step in HSS kurtosis at ~14,000 h; L10 design life ~130,000 h; inner-race axial-aligned spall ~18 mm; crescent beach marks propagating from a subsurface origin ~0.4 mm deep; WEC and butterflies in sections through the spall — unverified: supplied in the problem statement; this analysis did not inspect the part, the sections, or the CMS record.
- **GT-9?** EHL minimum film thickness in line contact scales approximately as h ∝ (η0·u)^0.7 (Dowson-Higginson / Hamrock-Dowson; pressure-viscosity coefficient enters as α^0.54 and also rises at low temperature), with operating films of order 0.1–1 µm — unverified. **Phase 3 failure record:** Wikipedia "Elastohydrodynamic lubrication" (resolves to "Lubrication") opened — citation does not support the claim (no formula, exponent or film values).
- **GT-10?** Boundary / low-λ lubrication damage (adhesive and abrasive wear, scuffing, micropitting/grey staining) initiates at the surface and acts within roughly the first tens of µm (micropits ~10–20 µm deep) — unverified: tribology-text knowledge, source not opened (not read — turn budget).
- **GT-11?** Black-oxide conversion coating and case-carburized steel are reported to lower WEC incidence in wind-turbine HSS/IMS bearings — unverified. **Phase 3 failure records:** Wikipedia "Black oxide" opened — citation does not support the claim (no bearing or WEC content); Wikipedia "White etching cracks" opened — citation does not support the claim (mitigations not addressed).
- **GT-12?** Gearbox oil ISO VG 320; ν40 = 320 cSt by grade definition, ν100 ≈ 24 cSt (mineral) / ≈ 35 cSt (PAO); sump thermostatically held ~55–75 °C in operation — unverified: typical datasheet values, no datasheet for this turbine opened (the grade itself is not given in the problem statement).
- **GT-13?** HSS CRB geometry bracket: roller Ø 20–40 mm, inner-raceway Ø 140–200 mm; HSS speed 1,000–1,800 rpm — unverified: estimate; no bearing drawing or turbine data available.
- **GT-14?** Crescent "beach marks" are arrest lines of progressive, cyclic crack growth (fatigue fracture surfaces); butterflies are white-etching wings formed at inclusions under cyclic subsurface shear — unverified: metallurgy-text knowledge, source not opened (not read — turn budget).
- **GT-15?** WEC-type failures in wind HSS bearings are commonly reported at roughly 5–20% of calculated L10 — unverified: recalled; GT-7's source opened and does not state timing (failure record: citation does not support the claim).

**Provenance summary:**

```text
?-marked: GT-4?, GT-6?, GT-8?, GT-9?, GT-10?, GT-11?, GT-12?, GT-13?, GT-14?, GT-15? (10 of 15)
Read-at-source: GT-1 — Wikipedia "Temperature dependence of viscosity", quoted sentence on liquids
Read-at-source: GT-2 — same article, Walther-formula passage and λ = 0.7 passage
Read-at-source: GT-3 — Wikipedia "Contact mechanics", parallel-cylinders section, formulas quoted
Read-at-source: GT-5 — Wikipedia "Rolling-element bearing", "Life calculation models" passage
Read-at-source: GT-7 — Wikipedia "White etching cracks", subsurface-network and contributing-factor passages
Phase 3 failure records: GT-4? (2 sources), GT-9?, GT-11? (2 sources), GT-15?
Not read — turn budget: GT-10?, GT-14?
```

Irreducibility (5-Whys reduce-to-primitives applied to the operator's compound claim "the lubricant failed by low cold viscosity and the race wore through"): constituents are (a) cold lowers viscosity → reduces to GT-1/GT-2, a physical regularity, and is **false**; (b) low film → boundary regime → reduces to GT-9? (film law) and GT-10? (regime damage depth), both assumed; (c) "wore through" → reduces to GT-14? (fracture morphology) and GT-8? (observation), both assumed. Parent claim: one branch verified-false, so the parent fails regardless of the assumed branches.

---

## 4. Derivation Chains

All arithmetic below was computed once in a script and recomputed independently with an exact-fraction calculator; both results are given where they are compared (see the Recompute part of the adversarial pass record in the appendix).

### Conclusion C1: The operator's mechanism premise — "viscosity too low in the cold-snap months" — is physically inverted

GT-1 (liquid viscosity falls as temperature rises) + GT-2 (Walther relation, B > 0)
→ for any oil whose ν40 exceeds its ν100 the fitted Walther slope B is positive, so ν rises monotonically as T falls
→ at any given bearing or sump temperature a colder ambient can only hold the oil at the same or a higher viscosity, never a lower one
→ the premise that the cold snap lowered viscosity (A-1) is false, so cold-induced low viscosity cannot be the root cause

**Pre-check:** head GT-1, GT-2 · ?-marked: none · lowest cited: none · Inputs ceiling: HIGH
**Confidence:** HIGH — both inputs read at source (GT-1, GT-2 locations in §3); every hop is deduction from a monotone function; the endpoint is itself a ruling-out, and the one rival that would rescue a "thin film" story (viscosity lost by degradation rather than by cold) is a different hypothesis, recorded in §5 ("Degraded-oil thin film") and addressed by C3 (chain C1 needs no input from it).

### Conclusion C2: In magnitude, cold oil gives a film many times thicker, not thinner

GT-2 (Walther relation) + GT-12? (VG 320, ν100 24 cSt mineral / 35 cSt PAO) + GT-9? (h ∝ η^0.7)
→ fitting the mineral oil, y40 = log10(log10 320.7) = 0.39900 and y100 = log10(log10 24.7) = 0.14386, so B = 0.25514/(2.57189 − 2.49575) = 3.351 and A = 8.763
→ evaluating that fit gives ν(70 °C) = 69.2 cSt and ν(0 °C) = 9,159.6 cSt, a ratio 9159.6/69.2 = 132.4
→ under h ∝ η^0.7 the 0 °C film is 132.4^0.7 = e^(0.7 × 4.886) = 30.6× the 70 °C film
→ the PAO case gives ν(0 °C)/ν(70 °C) = 4363.6/88.8 = 49.1 and a film ratio 49.1^0.7 = 15.3
→ cold oil moves the contact further from the boundary regime by an order of magnitude, the opposite of the operator's mechanism

**Pre-check:** head GT-2, GT-12?, GT-9? · ?-marked: GT-12?, GT-9? · lowest cited: none · Inputs ceiling: MEDIUM
**Confidence:** MEDIUM — Inputs axis short only. GT-12? (oil grade and ν100 for this gearbox) is removed by reading the turbine's lubricant datasheet; GT-9? (film exponent ≈ 0.7) is removed by reading Hamrock-Dowson / Dowson-Higginson in a tribology text. Neither can reverse the direction, which C1 fixes at HIGH; they only move the ×15–×31 magnitude. Rival: none live — the extrapolation to −20 °C was abandoned (§5) rather than relied on.

### Conclusion C3: The damage is subsurface-initiated fatigue, not boundary-lubrication wear

GT-8? (origin 0.4 mm subsurface, beach marks) + GT-10? (boundary damage within ~20 µm) + GT-9? (film 0.1–1 µm) + GT-14? (beach marks record progressive fatigue)
→ the origin lies 0.4/0.020 = 20× deeper than the boundary-damage zone and 0.4/0.001 = 400× to 0.4/0.0001 = 4,000× deeper than the film itself *[Assumes: A-16 — no missed surface origin]*
→ a crack nucleated 0.4 mm below the raceway was not nucleated by the surface film condition
→ crescent beach marks radiating outward from that origin record cyclic crack growth to the surface, not material removal
→ the failure is subsurface-initiated rolling-contact fatigue that broke out as a spall, so "boundary lubrication wore the race through" (A-2, A-3) is refuted by morphology independently of C1

**Pre-check:** head GT-8?, GT-10?, GT-9?, GT-14? · ?-marked: GT-8?, GT-10?, GT-9?, GT-14? · lowest cited: none · Inputs ceiling: MEDIUM
**Confidence:** MEDIUM — Inputs axis short only. GT-8? is removed by the analyst confirming the origin depth and beach-mark direction on the fracture surface and sections; GT-10?, GT-14? and GT-9? are removed by reading a tribology/fractography reference for surface-distress depth, beach-mark morphology and film thickness. A-16 is priced: if a surface-initiated origin also exists elsewhere on the raceway, it does not explain the 0.4 mm origin of *this* spall, so the endpoint for this spall stands. Rival (a surface crack that grew down and back up) is ruled out in §5 ("Surface-initiated crack mistaken for subsurface").

### Conclusion C4: The 0.4 mm origin lies inside the Hertzian subsurface stress zone, but its depth alone does not discriminate classical RCF from WEC

GT-3 (b = 2Rp0/E*) + GT-4? (τmax = 0.300 p0 at z = 0.786 b) + GT-13? (R 8.75–16.67 mm) + GT-8? (origin depth 0.4 mm)
→ for steel on steel E* = 210/(2 × (1 − 0.3²)) = 210/1.82 = 115.4 GPa
→ the max-shear depth reaches 0.4 mm only if b = 0.4/0.786 = 0.509 mm
→ that half-width needs p0 = 0.509 × 115.4/(2R) = 3.36 GPa at R 8.75, 2.44 GPa at R 12.02 and 1.76 GPa at R 16.67 *[Assumes: A-18 — p0 1.0–2.0 GPa]*
→ at p0 = 1.5 GPa the max-shear depth is 0.786 × 2R × 1.5/115.4 = 0.18 mm (R 8.75) to 0.34 mm (R 16.67), and at 2.0 GPa 0.24–0.45 mm
→ the 0.4 mm origin sits at the deep end of, or just beyond, the nominal max-shear depth, inside the stressed zone and far from the surface
→ depth therefore confirms a subsurface stress-driven origin but cannot separate inclusion-sited WEC initiation from high-load classical RCF

**Pre-check:** head GT-3, GT-4?, GT-13?, GT-8? · ?-marked: GT-4?, GT-13?, GT-8? · lowest cited: none · Inputs ceiling: MEDIUM
**Confidence:** MEDIUM — Inputs axis short only. GT-4? is removed by reading the McEwen/Johnson line-contact solution (Phase 3 read attempted twice, both failed); GT-13? by the bearing drawing (roller and raceway diameters); GT-8? by the analyst's section measurement. A-18 is priced: if p0 is below 1.0 GPa the max-shear depth is ≤ 0.23 mm and the origin lies further below it, which strengthens the inclusion-sited reading and still does not move the origin toward the surface, so the endpoint ("subsurface, non-discriminating") stands; if above 2.0 GPa the bracket simply covers 0.4 mm, same endpoint. Rival ("depth discriminates") abandoned in §5.

### Conclusion C5: Time-to-failure alone cannot convict a non-classical mechanism; fleet counts can

GT-5 (L10 = 90% survival) + GT-6? (Weibull slope 9/8–1.5) + GT-8? (14,000 h vs. 130,000 h)
→ the life fraction is t/L10 = 14,000/130,000 = 7/65 = 0.1077
→ classical-RCF failure probability by 14,000 h is F = 1 − 0.9^(0.1077^1.125) = 1 − 0.9^0.0815 = 0.86% at e = 9/8, and 1 − 0.9^0.0353 = 0.37% at e = 1.5
→ a single classical failure this early is improbable (≤ 0.86%) but not impossible, so one bearing's timing is weak evidence on its own
→ in a 100-turbine fleet ≥ 5 such failures by 14,000 h would occur with probability 0.18% under classical RCF (binomial, p = 0.00855, expected 0.86 failures), so fleet failure counts discriminate where one bearing cannot

**Pre-check:** head GT-5, GT-6?, GT-8? · ?-marked: GT-6?, GT-8? · lowest cited: none · Inputs ceiling: MEDIUM
**Confidence:** MEDIUM — Inputs axis short only. GT-6? is removed by reading the Weibull-slope basis in ISO 281 or Lundberg-Palmgren; GT-8? by the CMS and service record. Both slopes are shown so the conclusion (≤ ~1%) holds across the bracket. Rival: none live — the endpoint is a statement about evidential weight, not a mechanism claim.

### Conclusion C6: The operator's hypothesis is refuted; the failure is subsurface-initiated RCF

C1 (HIGH) + C2 (MEDIUM) + C3 (MEDIUM) + C4 (MEDIUM)
→ the low-viscosity premise is false in direction on physics alone, as C1 shows
→ the boundary-wear consequence is false on morphology alone, because C3's subsurface origin and beach marks are a fatigue signature
→ C4's subsurface-stress location of the origin agrees with C3 and gives the wear reading no foothold
→ the root-cause hypothesis as stated fails on two independent grounds, and the mechanism class is subsurface-initiated rolling-contact fatigue

**Pre-check:** head C1 (HIGH), C2 (MEDIUM), C3 (MEDIUM), C4 (MEDIUM) · ?-marked: none · lowest cited: MEDIUM · Inputs ceiling: MEDIUM
**Confidence:** MEDIUM — Inputs axis short via C2, C3 and C4 (each rated MEDIUM on its own line). Note the refutation half rests on two independent legs: it would survive the loss of C3 on C1 (HIGH) alone, and the loss of C1 on C3 alone. Rival (the operator's hypothesis) is recorded and ruled out in §5 ("Operator hypothesis").

### Conclusion C7: The evidence points to a white-etching-crack failure whose driver is undetermined; the lubricant may still be implicated, but only chemically or through skidding

C6 (MEDIUM) + C5 (MEDIUM) + GT-7 (WEC: subsurface networks at inclusions; hydrogen, current, sliding) + GT-8? (WEC and butterflies at the origin) + GT-15? (WEC failures at ~5–20% of L10)
→ a subsurface origin carrying WEC networks and butterflies at ~10.8% of L10, inside the 5–20% band reported for WEC failures, matches the WEC mode GT-7 describes more closely than an early-tail classical failure that C5 puts at ≤ 0.86% *[Assumes: A-15 — WEC predate the spall]*
→ the drivers GT-7 names are hydrogen, electrical current and sliding, and none of the reported observations distinguishes one from another *[Assumes: A-13]*
→ the driver of this failure is therefore undetermined on the evidence supplied
→ the lubricant can still be implicated, via water or decomposition products supplying hydrogen, or via cold-start drag raising roller skidding *[Assumes: A-17]*
→ the discriminating observations are thermal-desorption hydrogen in the ring, oil water-ppm history, SEM for current-discharge craters with a grounding/insulation check, and roller smearing plus SCADA low-load hours

**Pre-check:** head C6 (MEDIUM), C5 (MEDIUM), GT-7, GT-8?, GT-15? · ?-marked: GT-8?, GT-15? · lowest cited: MEDIUM · Inputs ceiling: MEDIUM
**Confidence:** MEDIUM — Inputs axis short: GT-8? (the WEC and butterfly identification) is removed by the metallographer confirming WEC in sections remote from the spall, which also settles A-15; GT-15? (WEC timing band) is removed by reading a published WEC field survey, and the endpoint does not depend on it because C5 carries the timing argument alone; C6 and C5 are MEDIUM on their own lines. Inference: A-15 follows from GT-7 (read), which characterises WEC as networks commencing subsurface in the initial phases, so it is not an unpriced premise; A-13 and A-17 qualify only the driver and lubricant-involvement hops, and if both failed the endpoint's "driver undetermined" would still stand, so they are priced. Rival ("early-tail classical RCF with incidental WEC") is ruled out in §5 by GT-7 together with C5's ≤ 0.86% probability, with the residual tied to the same GT-8? verification.

### Conclusion C8: Specify a WEC-resistant replacement and run a driver investigation before locking a fleet specification (trade-off option D)

C6 (MEDIUM) + GT-7 (WEC drivers) + GT-11? (WEC-resistant bearing variants) + GT-5 (L10 models classical RCF)
→ option B (like-for-like plus a higher-viscosity or cold-rated oil) is knocked out because it targets the mechanism C6 refutes
→ weighted totals with weights locked before scoring are D = 74 > C = 52 > A = 35, driven by driver resolution (×4) and diagnostic value (×3)
→ no single weight change on the 1–5 scale flips the winner, and the smallest D-vs-C gap is 13 (driver weight 4 → 1)
→ setting the WEC-mode weight 5 → 1 still leaves D = 58 against C = 36, so the choice does not depend on C7's WEC reading being right
→ recommend D: a dimensionally interchangeable WEC-resistant bearing (black-oxide and/or case-carburized) now, plus the C7 driver investigation before any fleet-wide specification is locked
→[2nd] (actor lens: O&M, lubricant supplier, gearbox OEM) the investigation moves scrutiny from oil grade to oil water content, grounding/insulation and low-load hours, which the supplier and OEM have warranty incentives to contest
→[2nd] (time lens: a few cycles) if the driver is stray current and goes uncorrected, the coated bearing stays exposed, and a recurrence at a similar interval is the expected tripwire *[Assumes: A-19 — black oxide does not insulate]*
→[3rd] (time lens: fleet horizon) sister turbines of the same build share the driver, so the finding converts one replacement into a fleet inspection campaign keyed to CMS kurtosis
→[3rd] (actor lens: operator) the CMS kurtosis threshold that caught this failure becomes the fleet's early-warning instrument, so its alarm setting now carries replacement-planning weight

**Pre-check:** head C6 (MEDIUM), GT-7, GT-11?, GT-5 · ?-marked: GT-11? · lowest cited: MEDIUM · Inputs ceiling: MEDIUM
**Confidence:** MEDIUM — Inputs axis short: GT-11? (WEC-resistance of black-oxide/case-carburized variants) is removed by reading the bearing maker's or a published field study's WEC-incidence data (two read attempts failed, §3); C6 is MEDIUM on its own line. Inference: the trade-off arithmetic recomputes (appendix), and A-19 qualifies only a second-order extension, not the endpoint. Rival (option C, bearing change alone) is ruled out in §5 ("Bearing-only fix") by the flip test above. No extension step contradicts a ground truth; none works against the success criteria.

### Conclusion C9: "Well short of L10" is not by itself evidence of a defect

GT-5 (L10 = life at 90% reliability; populations only)
→ by definition up to 10% of a bearing population is expected to fail before L10
→ any single bearing failing before L10 is therefore an event the rating itself anticipates
→ the 14,000 h vs. 130,000 h comparison cannot carry the diagnosis on its own, and the mechanism has to come from the part, which is why C3 and C7 rest on morphology rather than timing

**Pre-check:** head GT-5 · ?-marked: none · lowest cited: none · Inputs ceiling: HIGH
**Confidence:** HIGH — the single input was read at source (GT-5, "Life calculation models" passage); each hop is deduction from the definition; the endpoint is itself a ruling-out (of using A-6 as evidence), so no rival is needed.

### Conclusion C10: If the failure is WEC-type, the specification lever is exposure to hydrogen, current and sliding, and an oil-viscosity increase is not one of the named drivers

GT-7 (WEC drivers: hydrogen, electrical current, sliding) + GT-1 (cold raises viscosity)
→ the contributing factors GT-7 names for WEC are hydrogen embrittlement, electrical current and sliding contact
→ low viscosity is not among those named factors
→ the operator's cold-snap factor, which GT-1 shows raises viscosity, can enter a WEC account only through one of those three routes
→ a replacement specification for a WEC-type failure has to be judged by its exposure to hydrogen, current and sliding, not by its low-temperature film thickness

**Pre-check:** head GT-7, GT-1 · ?-marked: none · lowest cited: none · Inputs ceiling: HIGH
**Confidence:** HIGH — both inputs read at source (GT-7, contributing-factors passage; GT-1, quoted sentence on liquids); the hops are deduction from the listed drivers; the endpoint is conditional on a WEC-type failure, so it does not inherit C7's MEDIUM, and it is a ruling-out of viscosity as a WEC specification lever, so no rival is needed.

---

## 5. Abandoned Reasoning

### Dead End: Operator hypothesis (cold-snap low viscosity → boundary lubrication → race wore through)

**What was tried:** Taking the operator's chain at face value and asking whether each link holds.

**Why abandoned:** Its first link is physically inverted: cold raises viscosity (GT-1, GT-2; chain C1). Its last link does not match the morphology: the origin is 0.4 mm subsurface with fatigue beach marks, not surface wear (chain C3). Two independent failures (chain C6).

**What it ruled out:** Any specification change whose only purpose is to raise low-temperature viscosity or film thickness.

### Dead End: Degraded-oil thin film (viscosity lost by shear-down, fuel/water dilution or additive loss rather than by cold)

**What was tried:** Rescuing a "thin film caused it" story by changing the cause of low viscosity.

**Why abandoned:** Any low-λ mechanism, whatever lowers the film, acts at the surface (GT-10?, GT-9?), while this origin is 0.4 mm down, 20× to 4,000× deeper (chain C3). Oil *chemistry* (water supplying hydrogen) survives, but as a WEC driver (chain C7), not as a film-thickness failure.

**What it ruled out:** Treating oil-condition findings as film-thickness evidence. Water-ppm history stays relevant, but only as a hydrogen-source test.

### Dead End: Surface-initiated crack mistaken for subsurface

**What was tried:** The rival reading of C3, in which a surface micro-pit grew down to 0.4 mm and then branched back to the surface.

**Why abandoned:** The beach marks are reported to radiate *from* a subsurface origin (GT-8?, GT-14?). A surface-initiated crack would put the origin and the earliest arrest lines at the surface. Ruled out by chain C3, subject to GT-8?'s verification.

**What it ruled out:** Re-sectioning only to look for surface origins at *this* spall. A-16 (missed origins elsewhere) remains a separate full-raceway check.

### Dead End: Early-tail classical RCF with incidental WEC

**What was tried:** The rival to C7: an ordinary inclusion-initiated classical fatigue failure that happened to fall in the early tail, with the white-etching features formed incidentally.

**Why abandoned:** C5 puts classical failure by 14,000 h at ≤ 0.86%. GT-7 characterises WEC as networks that commence subsurface in the initial phases, so they are an initiating mode rather than a by-product. Ruled out by GT-7 with C5 (chain C7). The residual depends on GT-8?: if the metallographer's "WEC" turns out to be dark-etching or white-etching *bands* typical of classical RCF, this rival revives.

**What it ruled out:** Treating the failure as bad luck and replacing like-for-like (option A).

### Dead End: Using the origin depth to discriminate WEC from classical RCF

**What was tried:** Testing whether 0.4 mm coincides with the Hertzian max-shear depth (pointing to classical RCF) or departs from it (pointing to inclusion/WEC).

**Why abandoned:** Over the plausible geometry and load brackets the max-shear depth spans 0.12–0.45 mm, which brackets 0.4 mm (chain C4). The test cannot discriminate without the actual R and load spectrum.

**What it ruled out:** Drawing a mechanism verdict from depth alone. Depth does confirm "subsurface", which is all C6 uses.

### Dead End: Walther extrapolation to −20 °C

**What was tried:** Quoting ν(−20 °C) = 129,371 cSt (mineral) as the cold-snap viscosity.

**Why abandoned:** That extrapolates the two-point fit far below its 40–100 °C basis and probably below the pour point, so the figure is not meaningful (GT-2 is a fit, not a law outside its range). The 0 °C value already makes the point, and the direction is fixed by C1 regardless.

**What it ruled out:** Leaning on extreme-cold magnitudes. The argument uses only 0 °C vs. 70 °C (chain C2).

### Dead End: Bearing-only fix (trade-off option C)

**What was tried:** Specifying a WEC-resistant bearing and stopping there.

**Why abandoned:** It scores 52 against D's 74. No single weight change flips the result: the closest is driver weight 4 → 1, which still leaves D ahead by 13 (chain C8). It also leaves an uncorrected driver in place. Stray current, for example, would attack a coated bearing as well (A-19).

**What it ruled out:** Locking a fleet specification before the driver investigation reports.

### Dead End: Like-for-like plus higher-viscosity / cold-rated oil (trade-off option B)

**What was tried:** The operator's implied specification.

**Why abandoned:** Knocked out on the must-have "acts on a mechanism the evidence does not refute": it targets the refuted mechanism (chain C6). Second-order check: a heavier oil in cold weather raises drag in a lightly loaded high-speed CRB and, if A-17 holds, raises skidding, which is one of GT-7's WEC drivers. It could therefore work *against* success criterion 4.

**What it ruled out:** Oil-grade changes as the replacement-spec lever.

---

## 6. Conclusion

**Recommended approach:** Do not authorise a specification built on the lubricant-viscosity hypothesis. Authorise trade-off option D: a dimensionally interchangeable WEC-resistant replacement bearing (black-oxide-finished and/or case-carburized) for this position now, and hold any fleet-wide specification lock until a driver investigation reports (chain C8).

**Key insight:** The operator's mechanism runs the wrong way. Cold raises gear-oil viscosity, giving about a 30× thicker film at 0 °C than at 70 °C for a mineral VG 320 (chains C1, C2). The damage also originates 0.4 mm below the surface, 20× deeper than any boundary-lubrication damage reaches (chain C3), so the hypothesis fails on physics and on morphology independently (chain C6).

**Trade-offs acknowledged:** Option D costs more and takes longer than like-for-like. It defers the fleet specification until the investigation reports. Its WEC-resistance benefit rests on unverified field-efficacy data (GT-11?), and it protects nothing if an electrical driver is left uncorrected (chain C8).

**Root-cause status for the analyst:**

- The stated root cause is refuted, and the mechanism class is subsurface-initiated rolling-contact fatigue (chain C6).
- The reported white-etching cracks and butterflies at a subsurface origin, at 10.8% of L10, point to a WEC-type failure whose driver (hydrogen, stray current or sliding) is not determined by the evidence supplied (chain C7).
- The lubricant may still be implicated, but only chemically (water or decomposition supplying hydrogen) or through cold-start skidding, never through low viscosity (chain C7).
- Before closing the root cause, run the discriminating tests: ring hydrogen by thermal desorption, oil water-ppm history, SEM for current craters plus a grounding/insulation check, and roller smearing against SCADA low-load hours (chain C7).
- One failure at 10.8% of L10 has a ≤ 0.86% classical-RCF probability, so check fleet failure counts: five or more in 100 turbines would be a 0.18% event under classical RCF (chain C5).
- Failing "well short of L10" is anticipated by the rating's own 90%-reliability definition, so the diagnosis rests on the part's morphology, not on its timing (chain C9).
- Judge any replacement specification by its exposure to hydrogen, stray current and sliding; low-temperature film thickness is not a WEC lever (chain C10).

**Pre-check:** head C1 (HIGH), C2 (MEDIUM), C3 (MEDIUM), C5 (MEDIUM), C6 (MEDIUM), C7 (MEDIUM), C8 (MEDIUM), C9 (HIGH), C10 (HIGH), GT-11? · ?-marked: GT-11? · lowest cited: MEDIUM · Inputs ceiling: MEDIUM
**Confidence:** MEDIUM — the refutation's physics leg is HIGH (chain C1), as are the timing and specification-lever findings (chains C9, C10). Every other chain the Conclusion rests on is MEDIUM: C2, C3, C5, C6, C7 and C8, each with its verification path on its own §4 line. The Conclusion also rests directly on GT-11?, which reading the bearing maker's or a published field study's WEC-incidence data would remove as a cause. The single verification that most moves this band is the metallographer's confirmation of WEC in sections away from the spall, together with the origin depth and beach-mark direction (GT-8?, via chains C3 and C7).
## Appendix — process output

## Trade-off (process output)

### Options

- **A — status quo:** like-for-like through-hardened replacement, same oil, no investigation.
- **B — operator's spec:** like-for-like bearing plus a higher-viscosity or cold-rated oil. **Knocked out** on M2 (below).
- **C — bearing-only change:** a WEC-resistant bearing (black-oxide and/or case-carburized), same envelope, no driver investigation.
- **D — composite:** C now, plus a driver investigation (hydrogen, current, skidding, water) and correction of whatever driver it finds, before a fleet specification is locked.

Must-haves (knock-outs): **M1** dimensionally interchangeable (A-11); A, C and D pass, and B passes. **M2** does not rest solely on a mechanism the evidence refutes: B fails, because C6 refutes the low-viscosity mechanism. A, C and D pass.

### Criteria & Weights

Locked before any scoring. All criteria are phrased so that higher is better.

| Criterion | Weight | 1 means | 5 means | GT basis |
|---|---|---|---|---|
| Addresses the WEC failure mode | 5 | same susceptibility as the failed part | a variant with documented lower WEC incidence | GT-7, GT-11? |
| Resolves the driver (prevents recurrence) | 4 | no driver addressed | the driver identified and corrected | GT-7 |
| Strength of efficacy evidence | 3 | the evidence shows the option failing (this event) | read-at-source field data | GT-11?, GT-8? |
| Lead time / availability | 2 | > 6 months | stock item | preference (no GT) |
| Cost | 2 | > 2× like-for-like | like-for-like | preference (no GT) |
| Diagnostic value for the fleet | 3 | nothing learned | the driver discriminated for the whole fleet | GT-7, C5 |

### Scoring

| Option | WEC ×5 | Driver ×4 | Evidence ×3 | Lead ×2 | Cost ×2 | Diagnostic ×3 | Total |
|---|---|---|---|---|---|---|---|
| A | 1×5=5 | 1×4=4 | 1×3=3 | 5×2=10 | 5×2=10 | 1×3=3 | **35** |
| C | 4×5=20 | 2×4=8 | 3×3=9 | 3×2=6 | 3×2=6 | 1×3=3 | **52** |
| D | 4×5=20 | 5×4=20 | 3×3=9 | 3×2=6 | 2×2=4 | 5×3=15 | **74** |

- **Recompute:** A = 5+4+3+10+10+3 = 35; C = 20+8+9+6+6+3 = 52; D = 20+20+9+6+4+15 = 74. The calculator returned 35, 52 and 74.
- The WEC and evidence scores rest on GT-11? (`?` carried forward, so C8 is capped at MEDIUM).
- The lead-time and cost scores are marked as preferences.

### Recommendation

D (74) beats C (52) and A (35). **Flip test:** every criterion was swept across weights 1–5, one at a time, and **no single weight change flips the winner**.

- Smallest D–C gap: 13, at Driver 4 → 1.
- Smallest D–A gap: 27, at WEC 5 → 1.
- With WEC 5 → 1 the totals are D 58, C 36, A 31. The recommendation is therefore robust to C7's WEC reading being wrong.

## Assumption Audit scan (process output)

| Chain | Step | Step Text (brief) | Assumption surfaced? | Added to Table? |
|---|---|---|---|---|
| C1 | 1 | B > 0 ⇒ ν rises as T falls | no | n/a |
| C1 | 2 | colder ambient cannot lower ν | no | n/a |
| C1 | 3 | A-1 false | no (A-1 already in table) | n/a |
| C2 | 1 | Walther fit A, B | no (GT-12? already A-9) | n/a |
| C2 | 2 | ν(70), ν(0), ratio 132.4 | no | n/a |
| C2 | 3 | film ratio 30.6 | yes: A-20 (film law, GT-9?) — surfaced in the Fix pass | yes (A-20) |
| C2 | 4 | PAO ratios | no | n/a |
| C2 | 5 | cold moves away from boundary | no | n/a |
| C3 | 1 | depth ratios 20×–4,000× | yes: A-16 (no missed surface origin); A-21 (boundary-damage depth, GT-10?) — Fix pass | yes (A-16 present from inversion, marked inline; A-21 added) |
| C3 | 2 | not nucleated by film | no | n/a |
| C3 | 3 | beach marks = cyclic growth | yes: A-22 (beach-mark reading, GT-14?) — Fix pass | yes (A-22) |
| C3 | 4 | subsurface RCF; A-2, A-3 refuted | no | n/a |
| C4 | 1 | E* = 115.4 GPa | no (A-5) | n/a |
| C4 | 2 | b = 0.509 mm | no | n/a |
| C4 | 3 | required p0 1.76–3.36 GPa | yes: A-18 (p0 1.0–2.0 GPa) | yes (A-18) |
| C4 | 4 | nominal depths 0.18–0.45 mm | yes: A-18 (same, referenced) | already added |
| C4 | 5 | origin at deep end of zone | no | n/a |
| C4 | 6 | depth non-discriminating | no | n/a |
| C5 | 1 | t/L10 = 0.1077 | no | n/a |
| C5 | 2 | F = 0.37–0.86% | no (A-7) | n/a |
| C5 | 3 | single event weak evidence | no (A-6) | n/a |
| C5 | 4 | fleet binomial 0.18% | no (illustrative n = 100 stated in hop) | n/a |
| C6 | 1 | premise false by C1 | no | n/a |
| C6 | 2 | wear false by C3 | no | n/a |
| C6 | 3 | C4 agrees | no | n/a |
| C6 | 4 | refuted; subsurface RCF | no | n/a |
| C7 | 1 | WEC mode matches (incl. 5–20% band) | yes: A-15 (WEC predate spall); A-23 (WEC timing, GT-15?) — Fix pass | yes (A-15, A-23) |
| C7 | 2 | drivers not distinguished | yes: A-13 | yes (A-13) |
| C7 | 3 | driver undetermined | no | n/a |
| C7 | 4 | lubricant implicated chemically or via skidding | yes: A-17 (cold drag → skidding) | yes (A-17) |
| C7 | 5 | discriminating observations | no | n/a |
| C8 | 1 | B knocked out | no (A-11 for M1) | n/a |
| C8 | 2 | totals 74/52/35 | no (A-12 / GT-11?) | n/a |
| C8 | 3 | flip test | no | n/a |
| C8 | 4 | robust to C7 reading | no | n/a |
| C8 | 5 | recommend D | no (A-14 discarded) | n/a |
| C8 | 6 [2nd] | actors contest the scrutiny | no | n/a |
| C8 | 7 [2nd] | stray-current recurrence tripwire | yes: A-19 (black oxide not insulating) | yes (A-19) |
| C8 | 8 [3rd] | fleet campaign | no | n/a |
| C8 | 9 [3rd] | CMS threshold gains weight | no | n/a |
| C9 | 1 | ≤ 10% expected to fail before L10 | no (A-6) | n/a |
| C9 | 2 | single early failure is anticipated | no | n/a |
| C9 | 3 | timing cannot carry the diagnosis | no | n/a |
| C10 | 1 | the WEC factors named in GT-7 | no (A-13) | n/a |
| C10 | 2 | low viscosity not among them | no | n/a |
| C10 | 3 | cold enters only via the three routes | no (A-17 already present) | n/a |
| C10 | 4 | spec judged by H / current / sliding exposure | no | n/a |

Techniques not applied:
- theoretical-limit (Phase 1) — not applicable — the essence is a diagnosis, not whether a figure is a convention or a hard bound
- theoretical-limit (Phase 4) — not applicable — no conclusion needs a law-permitted ceiling; the life and stress figures are compared with design values, not with physical limits
- inversion (Phase 2) — not applicable — the operator's hypothesis was not "too clean to challenge": its first link fails directly against GT-1. Inversion was applied to the headline conclusion in Phase 5 instead

## Adversarial pass (process output)

**Recompute** — each computed figure was redone with an exact-fraction calculator, independently of the script:

- t/L10 = 7/65 = 0.10769 ✓
- F(e = 9/8) = 0.0085511 ✓; F(e = 1.5) = 0.0037166 (chain text 0.37%) ✓
- E* = 1500/13 = 115.385 GPa ✓
- b_req = 200/393 = 0.50891 mm ✓
- p0_req = 2.4426 / 3.3555 / 1.7616 GPa ✓
- b(R 12.02, 1.5 GPa) = 0.31252 mm → z = 0.24561 mm ✓, and this lies inside the 0.18–0.34 mm range ✓
- ν ratios: 9159.6/69.2 = 132.36 ✓ and 46.6/69.2 = 0.673 ✓; PAO 4363.6/88.8 = 49.14 ✓
- Film ratio: 132.4^0.7 = exp(0.7 × 4.8858) = exp(3.4201) = 30.57 ✓
- Revolutions at 1,500 rpm: 1.26 × 10⁹ ✓
- Trade-off totals 74 / 52 / 35 ✓
- Binomial P(X ≥ 5 | n = 100, p = 0.00855) = 0.00176 ✓ (script)
- McEwen max τ/p0 = 0.3003 at z/b = 0.7862 ✓, matching the recalled factors 0.30 and 0.786
- Direction checks: every film ratio for an oil colder than 70 °C is > 1 and every warmer one is < 1 ✓; each required p0 rises as R falls ✓

**Sensitivity** — the ground truth whose falsity would flip the *mechanism* conclusion (C7) is GT-8? (the WEC/butterfly identification and the 0.4 mm subsurface origin). It is `?`-marked and cannot be verified from here, so the caveat is carried on C3, C7 and §6. The refutation of the operator's hypothesis (C6) has no single flip input: C1 rests on read GT-1/GT-2, and C3 independently on GT-8?. Weakest link per chain:

- C1: none material.
- C2: GT-12?, which sets the magnitude only.
- C3: GT-10?, the surface-damage depth.
- C4: GT-13?, the geometry.
- C5: GT-6?, the Weibull slope.
- C6: inherited from C3.
- C7: the A-13 hop (drivers indistinguishable).
- C8: GT-11?, efficacy. C9: none material (definitional). C10: the endpoint's WEC condition, which is carried by C7.

**Rival** — one rival per chain:

- Headline: early-tail classical RCF. Ruled out → §5 "Early-tail classical RCF with incidental WEC".
- C1: rival not applicable — the endpoint is itself a ruling-out; the thin-film rescue → §5 "Degraded-oil thin film".
- C2: rival not applicable — a magnitude illustration whose direction is fixed by C1; extreme-cold magnitudes → §5 "Walther extrapolation".
- C3: → §5 "Surface-initiated crack mistaken for subsurface".
- C4: → §5 "Using the origin depth to discriminate".
- C5: rival not applicable — the endpoint concerns evidential weight, not mechanism.
- C6: → §5 "Operator hypothesis".
- C7: → §5 "Early-tail classical RCF".
- C8: options C and B → §5 "Bearing-only fix" and "Like-for-like plus higher-viscosity oil".
- C9: rival not applicable — the endpoint is a ruling-out of timing as diagnostic evidence.
- C10: rival not applicable — the endpoint is a ruling-out of viscosity as a WEC lever, conditional on a WEC-type failure.

**Premise** — (inversion, applied to the headline claim "the failure is a WEC-type subsurface fatigue failure, not cold-snap low-viscosity boundary wear"): the headline conclusion is already false — the race failed by a lubrication-driven, or at least non-WEC, mechanism after all.

**Causes** (unfiltered, by stakeholder):

- *Metallographer:*
  - (1) the "WEC" were dark-etching regions or white-etching bands typical of classical RCF and were mislabelled
  - (2) the section missed a surface-initiated origin
  - (3) the 0.4 mm depth was measured on an oblique section
  - (4) the WEC formed after spalling, from debris over-rolling
- *Lubricant supplier:*
  - (5) the oil was water-contaminated in the cold months, so "the lubricant failed" is true chemically
  - (6) the oil heater failed, so the oil ran hot rather than cold
- *Bearing OEM / gearbox OEM:*
  - (7) an assembly fit error raised hoop stress, giving axial cracking from hoop tension rather than from a WEC driver
  - (8) a rogue inclusion in a dirty heat of steel gave classical early RCF
- *Operator (O&M):*
  - (9) the CMS step reflects a different component
  - (10) cold-start skidding smeared the race, so the lubricant regime was involved through drag, not thinness

**Clusters:**

- **K1, evidence-identification risk** (causes 1, 2, 3, 4) — bears on GT-8?, C3, C7.
- **K2, lubricant-chemistry or thermal involvement** (causes 5, 6, 10) — bears on C1, C7, A-17. Cause 6 is an operating-temperature excursion, not a cold one; it would lower viscosity by heat, so it does not rescue the cold-snap premise in C1, but it is a separate low-λ route and C3's morphology still excludes it.
- **K3, non-WEC material or assembly origin** (causes 7, 8) — bears on C4, C7, GT-7.
- **K4, misattributed signal** (cause 9) — bears on GT-8?.

**Disposition:**

- **K1** — plan change. Before closing the root cause, add a metallographic review with sections remote from the spall and a perpendicular section plane (named as the GT-8? verification on C3/C7). This also settles A-15 and A-16.
- **K2** — plan change, already inside D: oil water-ppm history, heater-log review and roller-smearing inspection are added to the C7 test list. Cause 6 is included as a heater-log check.
- **K3** — accepted risk with mitigation: the inclusion rating, steel-heat certificate and shaft/bore fit measurement are added to D's investigation. Option D's flip robustness (C8) means the specification does not change if K3 proves true.
- **K4** — accepted risk with mitigation: the disassembly confirms the damaged component, and the physical spall is itself the evidence. Mitigation: the CMS sensor/channel mapping is checked during the investigation.

**Falsification** — the conclusion is false if metallography remote from the spall shows no WEC networks and the origin is shown to be at the surface, or if a re-measured sump/bearing temperature record shows the oil was *below* its design viscosity during the damage period — a combination GT-1 makes possible only through overheating, not cold.

## §6→§4 closure ledger (process output)

```text
- "Recommended approach: do not authorise a specification built on the lubricant-viscosity hypothesis; authorise trade-off option D …" → chain C8 ✓
- "Key insight: the operator's mechanism runs the wrong way … fails on physics and on morphology independently" → chains C1, C2, C3, C6 ✓
- "Trade-offs acknowledged: option D costs more and takes longer … protects nothing if an electrical driver is left uncorrected" → chain C8 ✓
- "The stated root cause is refuted, and the mechanism class is subsurface-initiated rolling-contact fatigue" → chain C6 ✓
- "The reported white-etching cracks and butterflies … point to a WEC-type failure whose driver … is not determined" → chain C7 ✓
- "The lubricant may still be implicated, but only chemically … or through cold-start skidding" → chain C7 ✓
- "Before closing the root cause, run the discriminating tests …" → chain C7 ✓
- "One failure at 10.8% of L10 has a ≤ 0.86% classical-RCF probability, so check fleet failure counts …" → chain C5 ✓
- "Failing 'well short of L10' is anticipated by the rating's own 90%-reliability definition …" → chain C9 ✓ (added in Fix pass)
- "Judge any replacement specification by its exposure to hydrogen, stray current and sliding …" → chain C10 ✓ (added in Fix pass)
- "Pre-check: head C1 (HIGH), C2 … GT-11? · Inputs ceiling: MEDIUM" → chains C1, C2, C3, C5, C6, C7, C8, C9, C10 ✓
- "Confidence: MEDIUM — …" → chains C1, C2, C3, C5, C6, C7, C8, C9, C10 ✓
```

No claim was cut. Ledger clean.

## Self-audit scan (process output)

Table 1 — chain form (section 4). This scan inspected every hop position of every chain by hand, including the positions the mechanical check cannot reach: no non-first head input carries prose, no hop at any position leads with a `GT-N` identifier, and no hop at any position ends with terminal punctuation.

| Chain | Chain Head (brief) | Form conforming? | Rule applied | Dependency clean? | Band | Act attempted? | Edges fired |
|---|---|---|---|---|---|---|---|
| C1 | GT-1 + GT-2 | yes | n/a | yes | HIGH | yes | none |
| C2 | GT-2 + GT-12? + GT-9? | yes | n/a | yes | MEDIUM | yes | none |
| C3 | GT-8? + GT-10? + GT-9? + GT-14? | yes | n/a | yes | MEDIUM | yes | none |
| C4 | GT-3 + GT-4? + GT-13? + GT-8? | yes | n/a | yes | MEDIUM | yes | none |
| C5 | GT-5 + GT-6? + GT-8? | yes | n/a | yes | MEDIUM | yes | none |
| C6 | C1 + C2 + C3 + C4 | yes | n/a | yes | MEDIUM | no | none |
| C7 | C6 + C5 + GT-7 + GT-8? + GT-15? | yes | n/a | yes | MEDIUM | yes | none |
| C8 | C6 + GT-7 + GT-11? + GT-5 | yes | n/a | yes | MEDIUM | yes | none |
| C9 | GT-5 | yes | n/a | yes | HIGH | yes | Fix/Repeat (added in Fix pass) |
| C10 | GT-7 + GT-1 | yes | n/a | yes | HIGH | yes | Fix/Repeat (added in Fix pass) |

Rows re-run after the Fix pass (C7 head, C9, C10, two §6 list items, Pre-check and Confidence rows). C6's `Act attempted? = no` is structural: its head holds only chains, and the reads that feed it were attempted on the heads of C1–C4. It is not the shape of an all-`?` chain left unchecked.

Table 2 — claim inventory (section 6).

| §6 Span (brief) | Construct | Claim under R11? | R11 clause applied | Chain cited |
|---|---|---|---|---|
| Recommended approach: do not authorise … option D | bold lead-in | yes | bold lead-in whose colon closes the bold span | C8 |
| Key insight: mechanism runs the wrong way | bold lead-in | yes | bold lead-in whose colon closes the bold span | C1, C2, C3, C6 |
| Trade-offs acknowledged: costs more … | bold lead-in | yes | bold lead-in whose colon closes the bold span | C8 |
| Root-cause status for the analyst: | bold lead-in | no | section-intro label: the colon-terminated span is the whole line and carries no citation | n/a |
| stated root cause refuted … | list item | yes | list item past forty characters | C6 |
| WEC and butterflies … driver not determined | list item | yes | list item past forty characters | C7 |
| lubricant implicated only chemically … | list item | yes | list item past forty characters | C7 |
| run the discriminating tests … | list item | yes | list item past forty characters | C7 |
| ≤ 0.86% … check fleet counts | list item | yes | list item past forty characters | C5 |
| well short of L10 is anticipated … | list item | yes | list item past forty characters | C9 |
| judge spec by H / current / sliding exposure … | list item | yes | list item past forty characters | C10 |
| Pre-check: head … Inputs ceiling MEDIUM | bold lead-in | yes | bold lead-in whose colon closes the bold span | C1, C2, C3, C5, C6, C7, C8, C9, C10 |
| Confidence: MEDIUM — … | bold lead-in | yes | bold lead-in whose colon closes the bold span (prescribed lead-in) | C1, C2, C3, C5, C6, C7, C8, C9, C10 |

```text
Scan complete: 10 chain rows, one per section-4 chain block in order; 13 section-6 rows, one per construct in order — 12 claims under R11, 1 excluded. 0 chains malformed, 0 claims untraced.
```

## Self-Audit Gate (process output)

**Pass 1 (before re-score):** Criterion 1 Sound · Criterion 2 Sound · Criterion 3 Hand-wavy · Criterion 4 Sound · Criterion 5 Rigorous · Criterion 6 Rigorous · Gate cleared: yes · Hand-wavy cap cleared: yes

Pass 1 found four problems, and the Fix step revised every criterion below Rigorous:

- **C1:** success criterion 5 was not checkable in §6. It was rewritten.
- **C2:** the audit attributed GT-9?/GT-10?/GT-14?/GT-15? to existing rows they did not match. Rows A-20 to A-23 were added.
- **C3:** GT-5 and GT-7 were read at source and reachable but fed only MEDIUM chains. HIGH chains C9 and C10 were added.
- **C4:** GT-15? was consumed by no chain. It was added to C7's head.

The affected ledger and scan rows were re-run before this re-score.

**Criterion 1: Identify Essence**
Quoted span: "5. Every figure the Conclusion states cites a §4 chain whose hops show that figure's arithmetic, and the figure recomputes when redone independently of the chain text."
Band: **Rigorous**
Justification: The essence names a mechanism → driver → specification question unique to this bearing. Every success criterion, including the rewritten fifth, is now a verb-subject-outcome test applied by scanning §6 and the chains it cites.

**Criterion 2: Challenge Assumptions**
Quoted span: "| C3 | 1 | depth ratios 20×–4,000× | yes: A-16 (no missed surface origin); A-21 (boundary-damage depth, GT-10?) — Fix pass | yes (A-16 present from inversion, marked inline; A-21 added) |"
Band: **Rigorous**
Justification: All 23 rows carry a four-type label, a type-matched treatment, an em-dash verdict and a specific verification. Three are Discarded, ten Challenged, and every used unverified row reads "unverified — flagged". The audit scan covers every hop of C1–C10, and each surfaced assumption now has its own row.

**Criterion 3: Establish Ground Truths**
Quoted span: "Enumerated GT-4?, GT-6?, GT-8?, GT-9?, GT-10?, GT-11?, GT-12?, GT-13?, GT-14?, GT-15?; the list carries `?` on exactly those ten and on no other entry. GT-1 and GT-2 feed C1 (HIGH), GT-5 feeds C9 (HIGH), GT-7 feeds C10 (HIGH), and GT-3 feeds only C4 (MEDIUM)."
Band: **Sound**
Justification: Every ID is stable, labelled and correctly suffixed, and the enumeration matches the list. However, one unsuffixed, reachable ground truth (GT-3) feeds only a MEDIUM chain, because C4 also rests on GT-4?, whose two read attempts both have Phase 3 failure records. The rubric bands a single such instance Sound.

**Criterion 4: Reason Upward**
Quoted span: "| C10 | GT-7 + GT-1 | yes | n/a | yes | HIGH | yes | Fix/Repeat (added in Fix pass) |"
Band: **Rigorous**
Justification:
- All ten chain rows are form-conforming and dependency-clean.
- Every ground truth is consumed, including GT-15? since the Fix.
- Every assumption-bearing hop carries `[Assumes: A-N]`.
- All arithmetic recomputes (Recompute part).
- No analogy is used as evidence.
- §5 holds eight dead ends in What-was-tried / Why-abandoned / What-it-ruled-out form.

**Criterion 5: Validate**
Quoted span: "**Confidence:** MEDIUM — the refutation's physics leg is HIGH (chain C1), as are the timing and specification-lever findings (chains C9, C10). Every other chain the Conclusion rests on is MEDIUM: C2, C3, C5, C6, C7 and C8 …"
Band: **Rigorous**
Justification:
- Each MEDIUM line names its `?` inputs with a verification path, and the line also names which axis is short.
- No chain carrying a `?` is rated HIGH, and the HIGH chains C1, C9 and C10 meet all three axes.
- §6's MEDIUM equals its weakest contributing chain.
- The adversarial record carries every part: Recompute, Sensitivity, Rival, a past-tense Premise, ten causes from four stakeholders, four clusters citing ids, a disposition per cluster, and Falsification.

**Criterion 6: Conclusion-to-Ground-Truth Traceability**
Quoted span: "| judge spec by H / current / sliding exposure … | list item | yes | list item past forty characters | C10 |"
Band: **Rigorous**
Justification: All 12 claims under R11 in the claim inventory cite a §4 chain, and the one excluded construct is a citation-free section-intro label. The Key Insight states a non-obvious finding: the operator's mechanism runs the wrong way, since cold thickens the film about 30×, and the hypothesis fails on two independent grounds. It does not restate option D.

**Gate result:** cleared · passes: 2 · Fix/Repeat fired: yes

## Structured summary (process output)

```json
{
  "schema_version": 1,
  "run_mode": "full-composer",
  "assumptions": [
    {
      "id": "A-1",
      "type": "untested belief",
      "verdict": "Discard"
    },
    {
      "id": "A-2",
      "type": "untested belief",
      "verdict": "Discard"
    },
    {
      "id": "A-3",
      "type": "untested belief",
      "verdict": "Discard"
    },
    {
      "id": "A-4",
      "type": "physical law",
      "verdict": "Accept"
    },
    {
      "id": "A-5",
      "type": "physical law",
      "verdict": "Accept"
    },
    {
      "id": "A-6",
      "type": "convention",
      "verdict": "Challenge"
    },
    {
      "id": "A-7",
      "type": "untested belief",
      "verdict": "Challenge"
    },
    {
      "id": "A-8",
      "type": "untested belief",
      "verdict": "Accept"
    },
    {
      "id": "A-9",
      "type": "untested belief",
      "verdict": "Challenge"
    },
    {
      "id": "A-10",
      "type": "untested belief",
      "verdict": "Challenge"
    },
    {
      "id": "A-11",
      "type": "current constraint",
      "verdict": "Accept"
    },
    {
      "id": "A-12",
      "type": "untested belief",
      "verdict": "Challenge"
    },
    {
      "id": "A-13",
      "type": "untested belief",
      "verdict": "Challenge"
    },
    {
      "id": "A-14",
      "type": "convention",
      "verdict": "Discard"
    },
    {
      "id": "A-15",
      "type": "untested belief",
      "verdict": "Accept"
    },
    {
      "id": "A-16",
      "type": "untested belief",
      "verdict": "Challenge"
    },
    {
      "id": "A-17",
      "type": "untested belief",
      "verdict": "Challenge"
    },
    {
      "id": "A-18",
      "type": "untested belief",
      "verdict": "Challenge"
    },
    {
      "id": "A-19",
      "type": "untested belief",
      "verdict": "Challenge"
    },
    {
      "id": "A-20",
      "type": "untested belief",
      "verdict": "Challenge"
    },
    {
      "id": "A-21",
      "type": "untested belief",
      "verdict": "Challenge"
    },
    {
      "id": "A-22",
      "type": "untested belief",
      "verdict": "Challenge"
    },
    {
      "id": "A-23",
      "type": "untested belief",
      "verdict": "Challenge"
    }
  ],
  "ground_truths": [
    {
      "id": "GT-1",
      "read_at_source": true
    },
    {
      "id": "GT-2",
      "read_at_source": true
    },
    {
      "id": "GT-3",
      "read_at_source": true
    },
    {
      "id": "GT-4",
      "read_at_source": false
    },
    {
      "id": "GT-5",
      "read_at_source": true
    },
    {
      "id": "GT-6",
      "read_at_source": false
    },
    {
      "id": "GT-7",
      "read_at_source": true
    },
    {
      "id": "GT-8",
      "read_at_source": false
    },
    {
      "id": "GT-9",
      "read_at_source": false
    },
    {
      "id": "GT-10",
      "read_at_source": false
    },
    {
      "id": "GT-11",
      "read_at_source": false
    },
    {
      "id": "GT-12",
      "read_at_source": false
    },
    {
      "id": "GT-13",
      "read_at_source": false
    },
    {
      "id": "GT-14",
      "read_at_source": false
    },
    {
      "id": "GT-15",
      "read_at_source": false
    }
  ],
  "chains": [
    {
      "id": "C1",
      "confidence": "HIGH",
      "rests_on": [
        "GT-1",
        "GT-2"
      ]
    },
    {
      "id": "C2",
      "confidence": "MEDIUM",
      "rests_on": [
        "GT-2",
        "GT-12?",
        "GT-9?"
      ]
    },
    {
      "id": "C3",
      "confidence": "MEDIUM",
      "rests_on": [
        "GT-8?",
        "GT-10?",
        "GT-9?",
        "GT-14?"
      ]
    },
    {
      "id": "C4",
      "confidence": "MEDIUM",
      "rests_on": [
        "GT-3",
        "GT-4?",
        "GT-13?",
        "GT-8?"
      ]
    },
    {
      "id": "C5",
      "confidence": "MEDIUM",
      "rests_on": [
        "GT-5",
        "GT-6?",
        "GT-8?"
      ]
    },
    {
      "id": "C6",
      "confidence": "MEDIUM",
      "rests_on": [
        "C1",
        "C2",
        "C3",
        "C4"
      ]
    },
    {
      "id": "C7",
      "confidence": "MEDIUM",
      "rests_on": [
        "C6",
        "C5",
        "GT-7",
        "GT-8?",
        "GT-15?"
      ]
    },
    {
      "id": "C8",
      "confidence": "MEDIUM",
      "rests_on": [
        "C6",
        "GT-7",
        "GT-11?",
        "GT-5"
      ]
    },
    {
      "id": "C9",
      "confidence": "HIGH",
      "rests_on": [
        "GT-5"
      ]
    },
    {
      "id": "C10",
      "confidence": "HIGH",
      "rests_on": [
        "GT-7",
        "GT-1"
      ]
    }
  ],
  "dead_ends": [
    "Operator hypothesis (cold-snap low viscosity → boundary lubrication → race wore through)",
    "Degraded-oil thin film (viscosity lost by shear-down, fuel/water dilution or additive loss rather than by cold)",
    "Surface-initiated crack mistaken for subsurface",
    "Early-tail classical RCF with incidental WEC",
    "Using the origin depth to discriminate WEC from classical RCF",
    "Walther extrapolation to −20 °C",
    "Bearing-only fix (trade-off option C)",
    "Like-for-like plus higher-viscosity / cold-rated oil (trade-off option B)"
  ],
  "techniques": {
    "applied": [
      "fishbone",
      "five-whys",
      "estimate",
      "trade-off",
      "second-order",
      "inversion"
    ],
    "not_applied": [
      {
        "technique": "theoretical-limit",
        "phase": 1,
        "reason": "the essence is a diagnosis, not whether a figure is a convention or a hard bound"
      },
      {
        "technique": "theoretical-limit",
        "phase": 4,
        "reason": "no conclusion needs a law-permitted ceiling; the life and stress figures are compared with design values, not with physical limits"
      },
      {
        "technique": "inversion",
        "phase": 2,
        "reason": "the operator's hypothesis was not \"too clean to challenge\": its first link fails directly against GT-1. Inversion was applied to the headline conclusion in Phase 5 instead"
      }
    ]
  },
  "gate": {
    "passes": [
      {
        "bands": [
          "Sound",
          "Sound",
          "Hand-wavy",
          "Sound",
          "Rigorous",
          "Rigorous"
        ],
        "gate_cleared": true,
        "hand_wavy_cap_cleared": true
      },
      {
        "bands": [
          "Rigorous",
          "Rigorous",
          "Sound",
          "Rigorous",
          "Rigorous",
          "Rigorous"
        ],
        "gate_cleared": true,
        "hand_wavy_cap_cleared": true
      }
    ],
    "fix_repeat_fired": true,
    "cleared": true
  },
  "re_entry": {
    "fired": true,
    "edges": [
      {
        "edge": "the Self-Audit Gate's Fix/Repeat loop",
        "trigger": "Pass 1 scored Criteria 1, 2 and 4 Sound and Criterion 3 Hand-wavy, so the Fix step revised them and the gate was re-scored once."
      }
    ]
  },
  "conclusion": {
    "recommendation": "Do not authorise a specification built on the lubricant-viscosity hypothesis. Authorise trade-off option D: a dimensionally interchangeable WEC-resistant replacement bearing (black-oxide-finished and/or case-carburized) for this position now, and hold any fleet-wide specification lock until a driver investigation reports (chain C8).",
    "confidence": "MEDIUM"
  }
}
```
