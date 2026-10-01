## Answer

**Recommendation:** The law-permitted gross ceiling is 54.32%, not the 62.27% isothermal Carnot figure, because the salt delivers its heat while cooling from 565 °C to 290 °C (chain C1, chain C2). Practice, at circa 42% gross, sits about 12.3 points below this ceiling on the wet condenser basis, or about 8–10 points below on a dry basis (chain C4).

**Band (from §6):** MEDIUM (chain C3, chain C4, chain C5)

**Would change it:** Reading a commercial salt tower's steam-generator design data would change it, as would reading its condenser back-pressure. Those reads would close GT-9? and GT-10? (chain C3, chain C4).

# First-Principles Analysis — Law-permitted ceiling on the steam Rankine power block of a 565 °C molten-salt tower

## 1. Problem Essence

**Core problem:** What gross thermal-to-electric efficiency does the second law permit for heat that a 565 °C → 290 °C Solar Salt stream gives up to a power block rejecting at its condenser, and how much of the distance between that ceiling and the roughly 42% achieved in practice is set by the law, by the salt window, by the steam cycle's structure, or by component losses?

The framing turns on one distinction. The user is right that the 290 °C cold tank is not the cold reservoir: no heat is rejected at 290 °C. But the 290 °C return temperature still matters, on the *source* side. The salt hands over its heat while cooling from 565 °C to 290 °C, so the heat is not all delivered at 565 °C. A Carnot figure computed with an isothermal 565 °C source is a true bound, but it is not the tightest one for this boundary.

**Success criteria:**
1. The Conclusion states a law-permitted gross efficiency for the stated boundary (565 °C hot tank in, condenser as sink), with every input temperature in kelvin and the arithmetic shown and recomputed.
2. The Conclusion states whether the isothermal Carnot figure or a tighter bound is the governing ceiling, and why.
3. The Conclusion states how many percentage points current practice sits below the governing ceiling, with practice and ceiling put on the same condenser basis.
4. The Conclusion splits that distance into named parts (salt window, steam-cycle structure, component and regeneration losses), and says for each part whether it is irreducible at this boundary, recoverable by changing a convention, or recoverable only with better hardware.
5. Every figure in the Conclusion carries a label saying whether it is derived from a law, read from a source, or estimated.

## 2. Assumptions Table

| Assumption | Type | Treatment | Verdict | Verification |
|------------|------|-----------|---------|--------------|
| A reversible engine taking heat Q from a source whose entropy falls by ΔS, and rejecting heat to a sink at T0, delivers at most W = Q − T0·ΔS (for an isothermal source this is Carnot, η = 1 − T0/Th) | physical law | Accept as a ground-truth candidate | Accept — second law (Clausius inequality); promoted to GT-1 | Carnot form read in decompose-irreducibility.md lines 96–101 and 108–110; the glide form follows by integrating dS = δQ/T |
| The hot reservoir is the 565 °C hot tank (838.15 K) | current constraint | Record expiry conditions | Accept — user-stipulated; lifts only if the salt chemistry changes, because the ~600 °C nitrate decomposition onset caps it | GT-4, read in decompose-irreducibility.md lines 231–233 |
| The cold reservoir is the 290 °C cold tank | convention | Challenge before use | Discard — nothing rejects heat at 290 °C; using it gives η ≤ 32.81%, which the ~42% achieved in practice (GT-7) would violate (§5) | User statement; GT-5; GT-7 |
| The heat crossing the boundary is delivered isothermally at 565 °C | untested belief | Verify or flag | Discard — in a two-tank design the salt gives up its heat while cooling from 565 °C to 290 °C (GT-5); isothermal delivery would need zero glide | GT-4 + GT-5, both read |
| The condenser sits at the 0.087 bar wet-cooled design pressure used in the five-whys example (Tsat = 43.11 °C) | convention | Challenge before use | Accept — accepted as the reference basis because it is the condenser condition the cited example fixes; challenged by bracketing the dry-cooled case (C4) and by naming ambient as the true floor (§5) | GT-2: pressure read at decompose-irreducibility.md lines 97–99; Tsat computed with IAPWS-IF97 |
| Solar Salt cp is close enough to constant over 290–565 °C that the log-mean temperature is the right source temperature | untested belief | Verify or flag | Accept — checked: the linear correlation cp = 1396.044 + 0.172·T(K) gives T_eff = 692.27 K, against a constant-cp log-mean of 691.56 K, a 0.05-point difference in η | GT-6, read in Serrano-López et al. Eq. (18) |
| Conventional salt-tower steam conditions are about 100–126 bar / 540–550 °C main steam, single reheat to the same temperature, and feedwater at about 240–245 °C | untested belief | Verify or flag | Challenge — used only to place the subcritical ideal-cycle tier; a range of conditions is computed so the sensitivity is visible | unverified — flagged (GT-9?) |
| The "circa 42%" gross efficiency for salt towers is on a dry-cooled condenser basis, like the reference plant described in the same report | untested belief | Verify or flag | Challenge — the sentence states no cooling basis, so the gap is reported as a range covering both readings | unverified — flagged; GT-7 and GT-8 read, but the link between them is not stated in the source |
| An air-cooled condenser's design initial temperature difference is 20–30 K above the dry-bulb temperature | untested belief | Verify or flag | Challenge — sets only the lower end of the dry-basis gap range | unverified — flagged (GT-10?) |
| Steam-cycle states are given correctly by IAPWS-IF97 | physical law | Accept as a ground-truth candidate | Accept — international standard formulation of water properties; promoted to GT-3 | Computed with the `iapws` IAPWS-IF97 implementation; Tsat(0.087 bar) = 43.11 °C agrees with the example's "≈ 43 °C" |
| The best-demonstrated gross efficiency of a salt-tower Rankine block is known | untested belief | Verify or flag | Discard — no figure was located (searches returned none; the solarpaces.nrel.gov plant pages did not resolve), so the best-demonstrated tier is left empty rather than filled from recollection | unverified — no source located |
| When salt temperature is plotted against heat delivered, the curve is close enough to a straight line for the pinch check | untested belief | Verify or flag | Accept — cp varies only from 1493 to 1540 J/kg·K across the window (GT-6), about ±1.6%, which moves a pinch by well under 1 K | GT-6 read; arithmetic in C3 |
| Ideal-tier steam cycles take main steam and reheat at 550 °C, a 15 K approach below the 565 °C salt | convention | Challenge before use | Accept — a design convention; a smaller approach raises the ideal tiers slightly, and none of them can reach the C1 ceiling | Stated as a choice; its effect is bounded by C1 |

## 3. Ground Truths

- **GT-1** Second law, entropy-balance form. A reversible engine that takes heat Q from a source whose entropy falls by ΔS_src, and rejects heat to a sink at T0, delivers at most W_max = Q − T0·ΔS_src. For a source at constant temperature Th this reduces to Carnot, η = 1 − T0/Th. For a stream with heat capacity cp cooling from Th to Tr: Q = ∫cp dT and ΔS_src = ∫cp dT/T, so η_max = 1 − T0/T_eff, where T_eff = Q/ΔS_src. With constant cp, T_eff is the log-mean (Th − Tr)/ln(Th/Tr). *Physical law (derived).* Source: second law of thermodynamics and Carnot's theorem; read-at-source: decompose-irreducibility.md lines 96–101 ("η_Carnot = 1 − T_cold / T_hot (temperatures in Kelvin)") and lines 108–110 ("physical law (second law of thermodynamics / Carnot's theorem). Irreducible."). The glide form is the integral of dS = δQ/T, shown here, so it adds no external figure.
- **GT-2** Condenser sink temperature T0 = 316.26 K (43.11 °C): the saturation temperature of water at 0.087 bar. *Pressure read from a source; temperature computed from the IAPWS-IF97 standard.* Source: decompose-irreducibility.md lines 97–99 ("T_cold ≈ 43 °C = 316 K — the saturation temperature at the 0.087 bar wet-cooled design condenser pressure"); read-at-source: those lines, plus `IAPWS97(P=0.0087 MPa, x=0).T = 316.260 K`, computed in this analysis.
- **GT-3** Water and steam states used in C3, from IAPWS-IF97 (*computed*). At 126 bar / 550 °C: h = 3475.5 kJ/kg, s = 6.6270 kJ/kg·K. Feedwater at 126 bar / 245 °C: h = 1062.2, s = 2.7277. Isentropic HP exhaust at 22 bar: h = 2968.0, T = 279.0 °C. Reheat to 22 bar / 550 °C: h = 3577.0, s = 7.5266. Source: IAPWS-IF97 via the `iapws` Python library; read-at-source: library output recorded in this analysis.
- **GT-4** Solar Salt (60% NaNO₃ / 40% KNO₃) operates across a 290–565 °C window: hot tank 565 °C = 838.15 K, cold tank 290 °C = 563.15 K. *Published operating window (direct measurement in the source).* This is the GT-4 the user named. Source: five-whys reduce-to-primitives example; read-at-source: decompose-irreducibility.md lines 231–233 ("GT-4 Solar Salt (60% NaNO₃ / 40% KNO₃) is thermally stable across the 290–565 °C operating window").
- **GT-5** In a salt tower the heat-transfer fluid is stored directly in a hot tank and a cold tank. So the heat delivered to the power block is the salt's sensible heat as it flows from the hot tank (565 °C), through the steam generator, to the cold tank (290 °C). *Definition of the plant configuration.* Source: Turchi & Heath, NREL/TP-5500-57625 (2013), p. 1; read-at-source: "Molten salt towers incorporate direct storage of the HTF in hot- and cold-salt storage tanks". The user's statement that the cold tank is "the return leg of the heat source loop" agrees.
- **GT-6** Solar Salt specific heat: cp (J/kg·K) = 1396.044 + 0.172·T(K). *Published correlation, fitted to measurements; identical to the Zavoico/SAM expression.* Source: Serrano-López, Fradera & Cuesta-López, "Molten salts database for energy applications", arXiv:1307.7343v2; read-at-source: Eq. (18) and Table entry "Solar Salt 1396.044+0.172·T … 2.36 %".
- **GT-7** Current practice: salt towers run "well-developed thermodynamic power cycles running at gross conversion efficiencies of circa 42%". *Published design-level figure. It is not stated as a measurement of a specific plant.* Source: Turchi & Heath, NREL/TP-5500-57625, p. 1; read-at-source: that sentence, quoted verbatim.
- **GT-8** The same report's reference plant is "~100MWe net (115MWe gross) … using 100% dry cooling", with a "Design conditions dry-bulb temperature (°C) 42". *Published design value.* Source: Turchi & Heath, NREL/TP-5500-57625; read-at-source: Appendix project description ("100% dry cooling") and Table 2, p. 8 (dry-bulb 42 °C).
- **GT-9?** Conventional main-steam conditions for salt towers: about 100–126 bar / 540–550 °C, single reheat, feedwater about 240–245 °C. *Estimate.* Unverified. A delegate search summary reported Crescent Dunes at "115 Bar" (reported-by-delegate). **Phase 3 failure record:** solarpaces.nrel.gov/project/crescent-dunes-solar-energy-project and solarpaces.nrel.gov/noor-iii were unreachable (DNS: ENOTFOUND). The other figures in this range come from recollection, and no source for them was located.
- **GT-10?** An air-cooled condenser's design initial temperature difference is about 20–30 K, which puts the dry-cooled condensing temperature at 62–72 °C for a 42 °C dry bulb. *Estimate.* Unverified: no source was located or opened in this analysis.

**Provenance summary:**

```text
?-marked: GT-9, GT-10 (2 of 10)
Read-at-source: GT-1 — decompose-irreducibility.md L96–101, L108–110; GT-2 — same file L97–99 + IAPWS-IF97 Tsat output;
GT-3 — IAPWS-IF97 library output; GT-4 — decompose-irreducibility.md L231–233; GT-5 — NREL/TP-5500-57625 p.1;
GT-6 — arXiv:1307.7343v2 Eq. (18); GT-7 — NREL/TP-5500-57625 p.1 ("circa 42%"); GT-8 — NREL/TP-5500-57625 Table 2 + project description
Phase 3 failure record: GT-9? — solarpaces.nrel.gov unreachable (ENOTFOUND); GT-10? — no source located
```

## 4. Derivation Chains

Theoretical-limit framing, applied to this boundary. **Direction:** higher is better (efficiency), so the bound is an **ideal ceiling**. **Governing constraint:** the second law, entropy-balance form (GT-1). **Tiers** (all on the 0.087 bar / 316.26 K condenser basis unless stated otherwise):

- **Isothermal Carnot (loose, valid):** 62.27%
- **Ideal ceiling at this boundary (tight):** 54.32%
- **Ideal-component supercritical steam, 10 K pinch:** 52.36%
- **Ideal-component subcritical steam:** 48.7–49.8%
- **Best demonstrated:** not located (A-11)
- **Conventional:** circa 42% gross (GT-7)

### Conclusion C1: The law-permitted gross efficiency for heat drawn from 565 °C salt returning at 290 °C, rejected at a 43.11 °C condenser, is 54.32%

GT-1 (entropy-balance bound) + GT-2 (T0 = 316.26 K) + GT-4 (838.15 K hot, 563.15 K return) + GT-5 (sensible heat over the glide) + GT-6 (Solar Salt cp correlation)
→ the heat crossing the boundary arrives while the source cools from 838.15 K to 563.15 K, not at a constant 838.15 K
→ per kg of salt, Q = 1396.044 × 275 + 0.086 × (838.15² − 563.15²) = 383,912.1 + 33,140.7 = 417,052.8 J/kg
→ per kg of salt, ΔS_src = 1396.044 × ln(838.15/563.15) + 0.172 × 275 = 1396.044 × 0.397651 + 47.30 = 602.438 J/kg·K
→ the entropic-mean source temperature is T_eff = 417,052.8 / 602.438 = 692.27 K (constant-cp log-mean: 275 / 0.397651 = 691.56 K)
→ the least heat that must be rejected at the condenser is 316.26 × 602.438 = 190,527 J/kg, leaving W_max = 226,526 J/kg
→ the law-permitted gross efficiency at this boundary is 226,526 / 417,052.8 = 1 − 316.26/692.27 = 54.32% (constant cp: 54.27%)

**Weakest link:** the cp correlation (GT-6). Replacing it with constant cp moves the result by only 0.05 points.

**Pre-check:** head GT-1, GT-2, GT-4, GT-5, GT-6 · ?-marked: none · lowest cited: none · Inputs ceiling: HIGH
**Confidence:** HIGH — Inputs: every head input was read at source (§3). Inference: each hop is deduction or arithmetic, recomputed independently in the adversarial pass. Rivals: the isothermal-565 °C reading (62.27%) and the 290 °C-sink reading (32.81%) are both ruled out in §5, by GT-5 and by GT-7 respectively.

### Conclusion C2: The isothermal Carnot figure of 62.27% is a valid but loose bound, and its 7.95-point excess over C1 is charged by the salt window, not by the power block

GT-1 (Carnot form) + GT-2 (T0 = 316.26 K) + GT-4 (Th = 838.15 K, return 563.15 K) + C1 (54.32% ceiling)
→ the isothermal-source Carnot bound is 1 − 316.26/838.15 = 62.27%
→ that bound exceeds the C1 ceiling by 62.27 − 54.32 = 7.95 percentage points
→ the 7.95 points are lost to entropy that the source hands over below 838.15 K, before any power cycle is chosen
→ so no power block, however perfect, can recover them while the salt returns at 290 °C
→ a 400 °C return would lift the constant-cp ceiling to 1 − 316.26 / (165/ln(838.15/673.15)) = 1 − 316.26/752.64 = 57.98%
→ the same 400 °C return would cut the heat stored per kg of salt to 165/275 = 60% of today's

**Weakest link:** the 400 °C illustration uses constant cp (A-6). C1 shows this moves the ceiling by about 0.05 points.

**Pre-check:** head GT-1, GT-2, GT-4, C1 (HIGH) · ?-marked: none · lowest cited: HIGH · Inputs ceiling: HIGH
**Confidence:** HIGH — Inputs: all head inputs were read, and C1 is HIGH. Inference: arithmetic only, recomputed. Rivals: the reading that Carnot 62.27% is the governing ceiling is ruled out in §5 ("Isothermal 565 °C Carnot as the ceiling").

### Conclusion C3: With ideal components, a subcritical reheat steam cycle reaches about 48.7–49.8%, and a supercritical single-reheat cycle with a 10 K pinch reaches 52.36%, so about 2.6 points of structural loss can be recovered by the choice of cycle and about 2 points cannot

GT-1 (entropy-balance bound) + GT-2 (T0 = 316.26 K) + GT-3 (IAPWS-IF97 states) + GT-9? (conventional steam conditions) + C1 (54.32% ceiling)
→ with reversible regeneration, the water takes in outside heat only from the 245 °C feedwater state to main steam, plus the reheat leg
→ Q_w = (3475.5 − 1062.2) + (3577.0 − 2968.0) = 2413.3 + 609.0 = 3022.3 kJ/kg
→ ΔS_w = (6.6270 − 2.7277) + (7.5266 − 6.6270) = 3.8993 + 0.8996 = 4.7989 kJ/kg·K
→ the water's entropic-mean heat-addition temperature is 3022.3 / 4.7989 = 629.81 K, which is 692.27 − 629.81 = 62.46 K below the salt's
→ an ideal-component 126 bar cycle therefore reaches 1 − 316.26/629.81 = 49.78%, with a feasible 13.4 K salt-to-water pinch [Assumes: A-12] [Assumes: A-13]
→ the 126 bar case sits 54.32 − 49.78 = 4.54 points below the C1 ceiling
→ a 100 bar / 540 °C / 240 °C-feedwater variant reaches 48.69%, so the subcritical ideal tier spans about 48.7–49.8%
→ the best supercritical single-reheat case in a scan that keeps a pinch of at least 10 K is 300 bar, reheat at 50 bar, 250 °C feedwater, with Q_w = 2912.0 kJ/kg and ΔS_w = 4.38643 kJ/kg·K
→ that case reaches 1 − 316.26 / (2912.0/4.38643) = 1 − 316.26/663.87 = 52.36%
→ about 52.36 − 49.78 = 2.58 points of the subcritical structural loss can be recovered by the choice of cycle
→ the remaining 54.32 − 52.36 = 1.96 points (1.39 at zero pinch, where the cycle reaches 52.93%) is the salt-to-water mismatch that a single-reheat steam cycle pays even with ideal components

**Weakest link:** the conventional steam conditions (GT-9?) that place the subcritical tier.

**Pre-check:** head GT-1, GT-2, GT-3, GT-9?, C1 (HIGH) · ?-marked: GT-9? · lowest cited: HIGH · Inputs ceiling: MEDIUM
**Confidence:** MEDIUM — the Inputs axis is short on GT-9? (conventional main-steam pressure, temperature, reheat pressure and feedwater temperature). It would be removed by reading the steam-generator design data of a commercial salt tower (the solarpaces.nrel.gov plant pages were unreachable). The computed 100–126 bar spread bounds its effect at about 1.1 points. Inference: A-12 is priced — cp varies about ±1.6% across the window (GT-6), which moves the pinch by well under 1 K, so the endpoint stands. A-13 (550 °C, a 15 K approach) shifts the subcritical and supercritical tiers in the same direction, and C1 caps both, so the 2.58-point difference stands to first order. Rivals: none live — alternative steam conditions are carried as the stated range.

### Conclusion C4: Practice (circa 42% gross) sits between about 8 and 12.5 points below its own law ceiling, depending on the condenser basis

GT-7 (circa 42% gross) + GT-8 (dry-cooled, 42 °C design dry bulb) + GT-1 (heat flows down a temperature gradient) + GT-10? (ACC ITD 20–30 K) + C1 (T_eff = 692.27 K)
→ on the 0.087 bar condenser basis, practice sits 54.32 − 42 = 12.32 points below the ceiling, which is 42/54.32 = 77.3% of it
→ a condenser rejecting heat to 42 °C air cannot condense below 315.15 K
→ on any basis using that air, the ceiling is at most 1 − 315.15/692.27 = 54.48%, so the gap is at most 54.48 − 42 = 12.48 points
→ if the circa-42% figure shares the reference plant's dry cooling, a 20–30 K ITD puts condensing at 335.15–345.15 K [Assumes: A-8]
→ the ceiling at that sink is 1 − 335.15/692.27 = 51.59% to 1 − 345.15/692.27 = 50.14%
→ on a matched dry basis, practice therefore sits 51.59 − 42 = 9.59 to 50.14 − 42 = 8.14 points below its own ceiling
→ comparing a dry-cooled 42% with a wet-basis ceiling overstates the gap by up to 12.32 − 8.14 = 4.18 points

**Weakest link:** the ITD range (GT-10?), which sets the lower end of the range.

**Pre-check:** head GT-7, GT-8, GT-1, GT-10?, C1 (HIGH) · ?-marked: GT-10? · lowest cited: HIGH · Inputs ceiling: MEDIUM
**Confidence:** MEDIUM — the Inputs axis is short on GT-10? (air-cooled-condenser design ITD). It would be removed by reading the design back-pressure or condensing temperature of a dry-cooled salt-tower turbine. GT-7 is also stated only as "circa": each point of error in it moves every gap figure by one point. Inference: A-8 is priced. The upper end (≤12.48 points) holds whether or not A-8 holds, and only the lower end depends on it. Rivals: the wet-versus-dry reading of GT-7 is not left live — the stated range spans both readings.

### Conclusion C5: Of the distance between practice and the law ceiling, about 2.6 points can be recovered by changing the steam-cycle structure, about 2 points stay with any single-reheat steam cycle, and the remaining 3–8 points of component loss are permitted by the law but not quantified as achievable

C1 (54.32% ceiling) + C2 (7.95 points charged by the glide) + C3 (structural tiers) + C4 (8–12.5-point gap)
→ the 62.27% Carnot figure is not the ceiling, so the 7.95 points above 54.32% are not part of the gap
→ of the wet-basis 12.32-point gap, 4.54 points is the subcritical cycle's salt-to-water temperature mismatch
→ about 2.58 of those 4.54 points can be recovered by a supercritical reheat steam cycle, a change of convention rather than of law
→ about 1.96 of those points stay with any single-reheat steam cycle that keeps a 10 K pinch
→ the rest of the wet-basis gap, 49.78 − 42 = 7.78 points, is turbine, pump, generator and finite-regeneration irreversibility
→ on a dry basis the same component share is 1 − 335.15/629.81 = 46.79% less 42 to 1 − 345.15/629.81 = 45.20% less 42, i.e. 4.79 to 3.20 points
→ the law permits recovering all of the component share, but how much of it hardware can recover is not quantified here, because no best-demonstrated figure was located (A-11)
→[2nd] (actor lens) a developer or funder chasing efficiency gets more from changing the cycle structure than from small turbine gains, because cycle structure carries the only quantified recoverable share
→[2nd] (actor lens) benchmarking against 62.27% overstates every developer's headroom by 7.95 points, which inflates the expected return on power-block R&D
→[2nd] (time lens) at the next design iteration, raising the return temperature is the only lever that lifts the ceiling itself (C2)
→[3rd] (time lens) a narrower glide stores less heat per kg of salt, which raises salt-inventory cost per MWh and works against the plant's storage purpose
→[3rd] (time lens) over the long run the 565 °C top is held by nitrate decomposition (A-2), so the ceiling stays where it is until the salt chemistry changes

**Weakest link:** the component share. Its size depends on the condenser basis (C4), and its recoverable fraction is unquantified (A-11).

**Pre-check:** head C1 (HIGH), C2 (HIGH), C3 (MEDIUM), C4 (MEDIUM) · ?-marked: none · lowest cited: MEDIUM · Inputs ceiling: MEDIUM
**Confidence:** MEDIUM — capped by C3 (MEDIUM) and C4 (MEDIUM), whose own lines carry their verification paths. No further downgrade cause belongs to this chain: the unquantified recoverable fraction is stated as unquantified rather than estimated. The second-order effects contradict no ground truth. The narrower-glide effect works against the storage purpose but not against the success criteria of this efficiency question.

## 5. Abandoned Reasoning

### Dead End: Isothermal 565 °C Carnot as the ceiling

**What was tried:** Taking η = 1 − 316.26/838.15 = 62.27% as the law-permitted ceiling, which would put practice 62.27 − 42 = 20.27 points below it.

**Why abandoned:** The bound assumes all the heat is delivered at 838.15 K. GT-5 shows the salt delivers it while cooling to 563.15 K, so the source gives up 602.438 J/kg·K of entropy per kg, not 417,052.8/838.15 = 497.59 J/kg·K. The tighter bound C1 (54.32%) therefore governs. The 62.27% figure is true, but it is not the tightest bound.

**What it ruled out:** Reporting a 20-point gap. About 7.95 of those points (C2) cannot be recovered by any power block at this salt window.

### Dead End: The 290 °C cold tank as the cold reservoir

**What was tried:** η = 1 − 563.15/838.15 = 32.81%.

**Why abandoned:** No heat is rejected at 290 °C (GT-5: the cold tank is the return leg of the source loop). The figure is also refuted by GT-7: plants achieve circa 42% gross, and a figure above a true second-law bound would be impossible.

**What it ruled out:** Any reading that places practice *above* the ceiling, and the confusion of a source's return temperature with a sink.

### Dead End: Ambient air as the cold reservoir

**What was tried:** Stripping the condenser convention down to its law-level floor, ambient. With a 25 °C sink, the constant-cp glide ceiling is 1 − 298.15/691.56 = 56.89%.

**Why abandoned:** The user fixed the cold reservoir as the power cycle's condenser. The condenser's approach to ambient is a cooling-system design choice outside the stated boundary. Ambient also has no single value: it varies by site and by hour.

**What it ruled out:** Counting cooling-system headroom (about 2.6 points from 43 °C down to 25 °C) as power-block headroom. It is a separate convention, priced separately.

### Dead End: Comparing practice with the five-whys example's "35–45% net"

**What was tried:** Using the example's Rankine range (decompose-irreducibility.md lines 103–106) as the practice tier.

**Why abandoned:** That range is *net*, while the boundary is gross electricity. The example cites no specific source that this analysis could open. Mixing net with a gross ceiling would compare figures on different bases.

**What it ruled out:** A net/gross basis error, which would have overstated the gap by the auxiliary-load fraction.

### Dead End: Filling the best-demonstrated tier from recollection

**What was tried:** Naming a best-demonstrated gross efficiency for a commercial salt-tower turbine.

**Why abandoned:** Searches returned no plant-level gross efficiency figure, and the plant pages were unreachable (GT-9? failure record). A recalled figure would be an unverified number presented as an observation (A-11).

**What it ruled out:** A quantified "practically recoverable" component share. The analysis states that share as permitted by the law but not quantified as achievable.

## 6. Conclusion

**Recommended approach:** Use 54.32% gross as the law-permitted ceiling for this power block. It is the second-law limit for heat delivered by Solar Salt cooling from 565 °C to 290 °C and rejected at a 43.11 °C condenser, and it is tighter than the 62.27% isothermal Carnot figure (chain C1, chain C2). Against it, practice (circa 42% gross) sits about 12.3 points below on the wet condenser basis, or about 8–10 points below if the 42% is a dry-cooled figure (chain C4).

**Key insight:** The user correctly excludes the 290 °C cold tank as a sink, but 290 °C still caps the ceiling from the source side. The salt hands over its heat across a 275 K glide, which costs 7.95 points (62.27% → 54.32%) before any power cycle is chosen. No turbine can recover those points while the window stays 290–565 °C (chain C2).

**Trade-offs acknowledged:** Narrowing the glide is the only way to lift the ceiling itself. A 400 °C return reaches about 58% but stores only 60% as much heat per kg of salt, which works against the plant's storage purpose (chain C2, chain C5).

**How the gap divides (wet basis, 12.32 points):**

- About 2.58 points can be recovered by changing the steam-cycle structure to supercritical reheat — a convention change, not a law change (chain C3, chain C5).
- About 1.96 points stay with any single-reheat steam cycle that keeps a 10 K salt-to-water pinch (chain C3).
- About 7.78 points (3.2–4.8 on a dry basis) is component and finite-regeneration loss; the law permits recovering all of it, but this analysis does not quantify how much is achievable, because no best-demonstrated figure was located (chain C5).

**Pre-check:** head C1 (HIGH), C2 (HIGH), C3 (MEDIUM), C4 (MEDIUM), C5 (MEDIUM) · ?-marked: none · lowest cited: MEDIUM · Inputs ceiling: MEDIUM
**Confidence:** MEDIUM — the ceiling itself (chain C1) and the 7.95-point glide charge (chain C2) are HIGH. The gap size and its division rest on chain C3 (MEDIUM: GT-9?, conventional steam conditions), chain C4 (MEDIUM: GT-10?, the air-cooled condenser ITD) and chain C5 (MEDIUM, capped by C3 and C4), whose own lines carry the verification paths.
## Appendix — process output

## Techniques not applied (process output)

Run mode: full-composer (Step 0: no technique trigger phrase matched literally; "law-permitted limit" and "five-whys (reduce-to-primitives)" do not match the declared patterns).

Techniques not applied:
- inversion — not applicable — at Phase 2 the assumption set was not thin: the two framing assumptions (isothermal delivery, 290 °C sink) were already challenged and discarded directly; inversion was applied at Phase 5 instead
- fishbone — not applicable — the assumption space is a single thermodynamic chain, not a multi-causal one needing category brainstorming
- five-whys — not applicable — every ground truth is already at primitive level (a physical law, an IAPWS-IF97 state, or a figure read at source), so there was no compound claim to reduce
- trade-off — not applicable — the question asks for a bound and a decomposition, not a choice between viable options

## Assumption Audit scan (process output)

| Chain | Step | Step Text (brief) | Assumption surfaced? | Added to Table? |
|-------|------|-------------------|----------------------|-----------------|
| C1 | 1 | heat arrives while source cools 838.15→563.15 K | none (A-4 already in table, discarded) | n/a |
| C1 | 2 | Q = 417,052.8 J/kg | none (A-6 already in table) | n/a |
| C1 | 3 | ΔS_src = 602.438 J/kg·K | none | n/a |
| C1 | 4 | T_eff = 692.27 K | none | n/a |
| C1 | 5 | min rejected heat 190,527 J/kg | none (A-5 already in table) | n/a |
| C1 | 6 | ceiling 54.32% | none | n/a |
| C2 | 1 | isothermal Carnot 62.27% | none | n/a |
| C2 | 2 | excess 7.95 points | none | n/a |
| C2 | 3 | points lost to entropy handed over below 838.15 K | none | n/a |
| C2 | 4 | no power block recovers them at 290 °C return | none | n/a |
| C2 | 5 | 400 °C return → 57.98% | none (A-6 already in table) | n/a |
| C2 | 6 | storage per kg falls to 60% | none | n/a |
| C3 | 1 | reversible regeneration; outside heat only FW→main + reheat | none (A-7 already in table) | n/a |
| C3 | 2 | Q_w = 3022.3 kJ/kg | none (A-10 already in table) | n/a |
| C3 | 3 | ΔS_w = 4.7989 kJ/kg·K | none | n/a |
| C3 | 4 | water mean temperature 629.81 K | none | n/a |
| C3 | 5 | ideal 126 bar cycle 49.78%, pinch 13.4 K | A-12 (linear salt T–Q profile), A-13 (550 °C approach) | yes |
| C3 | 6 | 4.54 points below ceiling | none | n/a |
| C3 | 7 | 100 bar variant 48.69% | none (A-7) | n/a |
| C3 | 8 | best supercritical case, 300/50 bar, FW 250 °C | none (A-12, A-13 already added) | n/a |
| C3 | 9 | 52.36% | none | n/a |
| C3 | 10 | 2.58 points recoverable by cycle choice | none | n/a |
| C3 | 11 | 1.96 points residual | none | n/a |
| C4 | 1 | wet basis gap 12.32 points | none | n/a |
| C4 | 2 | condenser cannot be below 315.15 K | none (second law, A-1) | n/a |
| C4 | 3 | ceiling ≤54.48%, gap ≤12.48 points | none | n/a |
| C4 | 4 | dry ITD → 335.15–345.15 K | A-8 (dry basis of the 42% figure); A-9 already in table | A-8 already in table — marked inline |
| C4 | 5 | ceiling 51.59–50.14% | none | n/a |
| C4 | 6 | dry gap 9.59–8.14 points | none | n/a |
| C4 | 7 | overstatement up to 4.18 points | none | n/a |
| C5 | 1 | 7.95 points not part of the gap | none | n/a |
| C5 | 2 | 4.54 points subcritical mismatch | none | n/a |
| C5 | 3 | 2.58 points recoverable by supercritical | none | n/a |
| C5 | 4 | 1.96 points stay | none | n/a |
| C5 | 5 | 7.78 points component share (wet) | none | n/a |
| C5 | 6 | 3.20–4.79 points component share (dry) | none (A-8, A-9) | n/a |
| C5 | 7 | component share permitted but not quantified | none (A-11 already in table) | n/a |
| C5 | 8 | [2nd] cycle structure beats turbine gains | none | n/a |
| C5 | 9 | [2nd] Carnot benchmark overstates headroom by 7.95 | none | n/a |
| C5 | 10 | [2nd] return temperature is the only ceiling lever | none | n/a |
| C5 | 11 | [3rd] narrower glide stores less per kg | none | n/a |
| C5 | 12 | [3rd] 565 °C top fixed by nitrate decomposition | none (A-2 already in table) | n/a |

## Adversarial pass (process output)

**Recompute:** Every figure was recomputed independently of the chain text. The exact-fraction calculator and a separate Python pass gave the same values:
- 1 − 316.26/838.15 = 0.62267
- ln(838.15/563.15) = 0.397651, by series: ln 1.5 + ln(0.992216) = 0.405465 − 0.007814
- 275/0.397651 = 691.56 K
- Q = 417,052.845 J/kg
- ΔS = 602.4383 J/kg·K
- T_eff = 692.27 K
- 1 − 316.26/692.27 = 0.54316
- 316.26 × 602.438 = 190,527.0 J/kg
- 226,525.8/417,052.8 = 0.54316
- 62.27 − 54.32 = 7.95
- 165/0.219229 = 752.64 K, and 1 − 316.26/752.64 = 0.57980
- 3022.3/4.7989 = 629.81 K, and 1 − 316.26/629.81 = 0.49785
- 2912.0/4.38643 = 663.87 K, and 1 − 316.26/663.87 = 0.52361
- 1 − 315.15/692.27 = 0.54476
- 1 − 335.15/692.27 = 0.51587
- 1 − 345.15/692.27 = 0.50142
- 1 − 335.15/629.81 = 0.46786
- 1 − 345.15/629.81 = 0.45198
- 42/54.32 = 0.7732
- 1 − 563.15/838.15 = 0.32810
- 417,052.8/838.15 = 497.59 J/kg·K

Every combined figure lands on the side its operation puts it on: each ceiling below Carnot, each ideal steam tier below C1, and each dry-basis ceiling below the wet-basis one. One rounding difference: Q_w 3022.3 here against 3022.4 from the IAPWS run, from rounding the displayed enthalpies; it does not change the endpoint.

**Sensitivity:** The flip ground truth for the headline ceiling is GT-5 (heat delivered across the 565→290 °C glide); if it were false, the ceiling would revert to 62.27%. It is not `?`-marked. The ceiling is only mildly sensitive to the tank temperatures (constant cp): a hot tank at 555 °C gives 53.98%; a return at 300 °C gives 54.64%; a return at 280 °C gives 53.89%. For the gap, the flip input is GT-7 (circa 42%): each point of error in it moves every gap figure by one point. Weakest links per chain: C1 — GT-6 (cp form, 0.05-point effect); C2 — the constant-cp 400 °C illustration; C3 — GT-9?; C4 — GT-10?; C5 — the unquantified recoverable fraction (A-11).

**Rival:** For the headline (C1): the isothermal Carnot ceiling, ruled out by GT-5 → §5 "Isothermal 565 °C Carnot as the ceiling"; and the 290 °C sink, ruled out by GT-7 → §5 "The 290 °C cold tank as the cold reservoir". For C2: the same isothermal rival (§5). For C3: rival not applicable — the endpoint is a computed ideal-component tier, and alternative steam conditions are carried as a stated range rather than as a competing reading. For C4: the wet-basis versus dry-basis reading of GT-7 is not left live — the range spans both (stated on C4's confidence line). For C5: the reading that the gap is mostly turbine inefficiency is ruled out by C3, which assigns 4.54 points to cycle structure before any component loss is counted.

**Premise:** The headline conclusion is already false: 54.32% was not the law-permitted ceiling for this power block, and practice did not sit 8–12.5 points below it.

**Causes:**
- *Thermodynamicist:* (1) the salt did not return at 290 °C in operation, so T_eff was different; (2) cp was not as the correlation states; (3) some heat entered the block from another source at a different temperature; (4) the bound used the wrong sink temperature.
- *Plant operator:* (5) the hot tank ran below 565 °C; (6) the condenser ran at a dry-cooled back-pressure far from 0.087 bar; (7) steam-generator heat losses meant the heat "delivered" was less than the salt gave up.
- *Cycle developer:* (8) the scan missed a better steam configuration, so the structural split was wrong; (9) the IAPWS states were computed at the wrong units or pressure.
- *Funder/analyst:* (10) "circa 42%" was net, an annual average, or a different plant class, not design-point gross; (11) the figure was rounded far enough that the gap moved by more than a point.

**Clusters:**
- **K1 — operating temperatures differ from nominal** (causes 1, 5): bears on GT-4 and C1.
- **K2 — basis of the practice figure** (causes 4, 6, 10, 11): bears on GT-7, GT-8, GT-10? and C4.
- **K3 — model fidelity** (causes 2, 8, 9): bears on GT-3, GT-6 and C3.
- **K4 — boundary leakage** (causes 3, 7): bears on GT-5 and C1.

**Disposition:**
- **K1 — accepted risk.** Mitigation: C1 is stated in closed form (1 − T0/T_eff) with the sensitivities above (about 0.3 points per 10 K on either tank), so it can be recomputed at measured temperatures.
- **K2 — plan change made.** The gap is reported as a range spanning wet and dry bases rather than as one figure (C4). Mitigation for the remainder: reading a plant's design heat balance (gross output, steam-generator duty, condenser back-pressure) closes GT-10? and the rounding in GT-7.
- **K3 — accepted risk.** Mitigation: all figures were recomputed by a second method; the cp form was checked against a constant-cp alternative (0.05 points); the steam scan is stated as a coarse grid, so 52.36% is a found value, not a proven optimum, and C3 says so.
- **K4 — accepted risk.** Mitigation: the boundary is user-stipulated (heat from the hot tank in, gross electricity out). Steam-generator losses fall inside the gap as practice losses, not as a change in the ceiling, and no other heat input exists in a solar-only salt tower (GT-5).

**Falsification:** The conclusion is false if a power block on this boundary — salt in at 565 °C, returning at 290 °C, condensing at 0.087 bar — is measured delivering more than 54.32% gross of the heat the salt gave up; or if the measured salt return temperature in normal operation differs from 290 °C by enough to move T_eff materially (about 0.3 points of ceiling per 10 K).

## §6→§4 closure ledger (process output)

```text
- "Use 54.32% gross as the law-permitted ceiling … tighter than the 62.27% isothermal Carnot figure; practice sits about 12.3 points below (wet) or 8–10 (dry)" → chain C1, C2, C4 ✓
- "the 290 °C still caps the ceiling from the source side … costs 7.95 points … no turbine can recover them" → chain C2 ✓
- "Narrowing the glide is the only way to lift the ceiling … 400 °C return about 58% but 60% of the heat per kg" → chain C2, C5 ✓
- "About 2.58 points recoverable by supercritical reheat — a convention change" → chain C3, C5 ✓
- "About 1.96 points stay with any single-reheat steam cycle at a 10 K pinch" → chain C3 ✓
- "About 7.78 points (3.2–4.8 dry) is component loss; permitted by the law, not quantified as achievable" → chain C5 ✓
- "Pre-check: head C1 (HIGH) … Inputs ceiling: MEDIUM" → chain C1, C2, C3, C4, C5 ✓
- "Confidence: MEDIUM — …" → chain C1, C2, C3, C4, C5 ✓
```
No claim cut.

## Self-audit scan (process output)

| Chain | Chain Head (brief) | Form conforming? | Rule applied | Dependency clean? | Band | Act attempted? | Edges fired |
|-------|---------------------|-------------------|---------------|--------------------|------|-----------------|-------------|
| C1 | GT-1 + GT-2 + GT-4 + GT-5 + GT-6 | unreached | n/a | yes | HIGH | yes | none |
| C2 | GT-1 + GT-2 + GT-4 + C1 | unreached | n/a | yes | HIGH | yes | none |
| C3 | GT-1 + GT-2 + GT-3 + GT-9? + C1 | unreached | n/a | yes | MEDIUM | yes (GT-9? fetch failed, ENOTFOUND) | none |
| C4 | GT-7 + GT-8 + GT-1 + GT-10? + C1 | unreached | n/a | yes | MEDIUM | yes | none |
| C5 | C1 + C2 + C3 + C4 | unreached | n/a | yes | MEDIUM | no (head cites chains only) | none |

`unreached` on every row: each head has more than one input, and each chain has more than two hops. So the prose-input rule in non-final head positions, the GT-led-hop rule from the third hop on, and the terminal-period rule from the second hop on all bind at positions the mechanical check does not reach. The positions it does reach (the final head input, the first two hops, and the first hop's punctuation) conform on every row. Dependencies are acyclic: C1 → C2, C3, C4 → C5. Every GT-N cited exists in §3.

| §6 Span (brief) | Construct | Claim under R11? | R11 clause applied | Chain cited |
|-------------------|-----------|-------------------|----------------------|---------------|
| Recommended approach: 54.32% ceiling, gap 12.3 / 8–10 | bold lead-in | yes | bold lead-in whose colon closes the bold span (prescribed lead-in) | C1, C2, C4 |
| Key insight: 290 °C caps from the source side, 7.95 points | bold lead-in | yes | bold lead-in whose colon closes the bold span (prescribed lead-in) | C2 |
| Trade-offs acknowledged: narrowing the glide, 400 °C, 60% | bold lead-in | yes | bold lead-in whose colon closes the bold span (prescribed lead-in) | C2, C5 |
| How the gap divides (wet basis, 12.32 points): | bold lead-in | no | section-intro label: colon-terminated span is the whole line and carries no citation of its own | n/a |
| About 2.58 points recoverable by supercritical | list item | yes | list item over forty characters | C3, C5 |
| About 1.96 points stay with single-reheat | list item | yes | list item over forty characters | C3 |
| About 7.78 points component loss | list item | yes | list item over forty characters | C5 |
| Pre-check: head C1 … Inputs ceiling MEDIUM | bold lead-in | yes | bold lead-in whose colon closes the bold span | C1, C2, C3, C4, C5 |
| Confidence: MEDIUM | bold lead-in | yes | bold lead-in whose colon closes the bold span (prescribed lead-in) | C1, C2, C3, C4, C5 |

```text
Scan complete: 5 chain rows, one per section-4 chain block in order; 9 section-6 rows, one per construct in order — 8 claims under R11, 1 excluded. 0 chains malformed, 0 claims untraced.
```

## Self-Audit Gate (process output)

**Criterion 1: Identify Essence**
Quoted span: "What gross thermal-to-electric efficiency does the second law permit for heat that a 565 °C → 290 °C Solar Salt stream gives up to a power block rejecting at its condenser, and how much of the distance … is set by the law, by the salt window, by the steam cycle's structure, or by component losses?" and "The Conclusion splits that distance into named parts … and says for each part whether it is irreducible at this boundary, recoverable by changing a convention, or recoverable only with better hardware."
Band: **Rigorous**
Justification: The essence names a question specific to this problem (a gliding salt source against a condenser sink), not a restatement of the prompt, and each success criterion is a "the Conclusion states …" test a reviewer can check by scanning §6.

**Criterion 2: Challenge Assumptions**
Quoted span: "| Steam-cycle states are given correctly by IAPWS-IF97 | physical law | Accept as a ground-truth candidate | Accept — international standard formulation of water properties; promoted to GT-3 |" together with the Assumption Audit scan row "| C3 | 5 | ideal 126 bar cycle 49.78%, pinch 13.4 K | A-12 (linear salt T–Q profile), A-13 (550 °C approach) | yes |"
Band: **Sound**
Justification: All thirteen rows use the four-type scheme with em-dash verdicts, three assumptions are discarded, the audit scan covers every step of every chain, and unverified rows carry "unverified — flagged". One row departs from the prescribed form: IAPWS-IF97 is an empirical standard formulation, not strictly a physical law, so it would be better typed as a verified measurement-based belief.

**Criterion 3: Establish Ground Truths**
Quoted span: Comparison of enumeration against list: "?-marked: GT-9, GT-10 (2 of 10)" — the §3 list carries `?` on exactly GT-9? and GT-10?. But unsuffixed GT-3, GT-7 and GT-8 feed only C3 and C4, which are rated "**Confidence:** MEDIUM".
Band: **Hand-wavy**
Justification: The enumeration matches, and every read location is named, but the rubric requires each unsuffixed, reachable ground truth to feed at least one HIGH chain. Three (GT-3, GT-7, GT-8) feed only MEDIUM chains, because those chains also carry GT-9? or GT-10?, and the rubric bands that shortfall across multiple GTs as Hand-wavy. Unresolved gap: separating the GT-9?/GT-10?-free parts of C3 and C4 (the supercritical tier, and the ≤12.48-point upper bound) into their own HIGH chains would clear it. This pass did not restructure them, because the gate clears with this single Hand-wavy.

**Criterion 4: Reason Upward**
Quoted span: Scan row "| C4 | GT-7 + GT-8 + GT-1 + GT-10? + C1 | unreached | n/a | yes | MEDIUM | yes | none |" and the C4 hop "→ on any basis using that air, the ceiling is at most 1 − 315.15/692.27 = 54.48%, so the gap is at most 54.48 − 42 = 12.48 points"
Band: **Sound**
Justification: Every conclusion has exactly one arrow-led chain with genuine intermediates. Five §5 dead ends use the What-was-tried / Why-abandoned / What-it-ruled-out structure. No analogy is used as evidence, `[Assumes:]` marks are present, and every figure recomputes. A few hops (this one, and C1's "leaving W_max" hop) pack two inferences joined by "so" or "leaving", against the one-inference rule; the scan's `unreached` cells disclose rule positions the check cannot reach.

**Criterion 5: Validate**
Quoted span: "**Confidence:** MEDIUM — the Inputs axis is short on GT-10? (air-cooled-condenser design ITD). It would be removed by reading the design back-pressure or condensing temperature of a dry-cooled salt-tower turbine." and the adversarial record "**K2 — plan change made.** The gap is reported as a range spanning wet and dry bases rather than as one figure (C4)."
Band: **Rigorous**
Justification: Every chain names its weakest link, and every MEDIUM line names its `?` input with a verification path. C5 and §6 sit at the MEDIUM ceiling of their weakest contributors, while C1 and C2 are HIGH on all three axes. The adversarial record carries every part — recompute, sensitivity, rival, a past-tense premise, causes from four named viewpoints, clusters citing GT/C ids, and per-cluster dispositions — plus a falsification condition.

**Criterion 6: Conclusion-to-Ground-Truth Traceability**
Quoted span: Scan row "| Key insight: 290 °C caps from the source side, 7.95 points | bold lead-in | yes | bold lead-in whose colon closes the bold span (prescribed lead-in) | C2 |" and the reconciliation line "8 claims under R11, 1 excluded. 0 chains malformed, 0 claims untraced."
Band: **Rigorous**
Justification: Every §6 claim cites its chain inline, and §6 introduces nothing absent from §4. The Key Insight — that the excluded 290 °C tank still caps the ceiling from the source side, costing 7.95 points — is a finding that reasoning from the conventional Carnot formula misses, not a restatement of the recommended approach.

**Gate result:** cleared · passes: 1 · Fix/Repeat fired: no

## Structured summary (process output)

```json
{
  "schema_version": 1,
  "run_mode": "full-composer",
  "assumptions": [
    {"id": "A-1", "type": "physical law", "verdict": "Accept"},
    {"id": "A-2", "type": "current constraint", "verdict": "Accept"},
    {"id": "A-3", "type": "convention", "verdict": "Discard"},
    {"id": "A-4", "type": "untested belief", "verdict": "Discard"},
    {"id": "A-5", "type": "convention", "verdict": "Accept"},
    {"id": "A-6", "type": "untested belief", "verdict": "Accept"},
    {"id": "A-7", "type": "untested belief", "verdict": "Challenge"},
    {"id": "A-8", "type": "untested belief", "verdict": "Challenge"},
    {"id": "A-9", "type": "untested belief", "verdict": "Challenge"},
    {"id": "A-10", "type": "physical law", "verdict": "Accept"},
    {"id": "A-11", "type": "untested belief", "verdict": "Discard"},
    {"id": "A-12", "type": "untested belief", "verdict": "Accept"},
    {"id": "A-13", "type": "convention", "verdict": "Accept"}
  ],
  "ground_truths": [
    {"id": "GT-1", "read_at_source": true},
    {"id": "GT-2", "read_at_source": true},
    {"id": "GT-3", "read_at_source": true},
    {"id": "GT-4", "read_at_source": true},
    {"id": "GT-5", "read_at_source": true},
    {"id": "GT-6", "read_at_source": true},
    {"id": "GT-7", "read_at_source": true},
    {"id": "GT-8", "read_at_source": true},
    {"id": "GT-9", "read_at_source": false},
    {"id": "GT-10", "read_at_source": false}
  ],
  "chains": [
    {"id": "C1", "confidence": "HIGH", "rests_on": ["GT-1", "GT-2", "GT-4", "GT-5", "GT-6"]},
    {"id": "C2", "confidence": "HIGH", "rests_on": ["GT-1", "GT-2", "GT-4", "C1"]},
    {"id": "C3", "confidence": "MEDIUM", "rests_on": ["GT-1", "GT-2", "GT-3", "GT-9?", "C1"]},
    {"id": "C4", "confidence": "MEDIUM", "rests_on": ["GT-7", "GT-8", "GT-1", "GT-10?", "C1"]},
    {"id": "C5", "confidence": "MEDIUM", "rests_on": ["C1", "C2", "C3", "C4"]}
  ],
  "dead_ends": [
    "Isothermal 565 °C Carnot as the ceiling",
    "The 290 °C cold tank as the cold reservoir",
    "Ambient air as the cold reservoir",
    "Comparing practice with the five-whys example's \"35–45% net\"",
    "Filling the best-demonstrated tier from recollection"
  ],
  "techniques": {
    "applied": ["theoretical-limit", "estimate", "second-order", "inversion"],
    "not_applied": [
      {"technique": "inversion", "phase": 2, "reason": "at Phase 2 the assumption set was not thin: the two framing assumptions (isothermal delivery, 290 °C sink) were already challenged and discarded directly; inversion was applied at Phase 5 instead"},
      {"technique": "fishbone", "phase": 2, "reason": "the assumption space is a single thermodynamic chain, not a multi-causal one needing category brainstorming"},
      {"technique": "five-whys", "phase": 3, "reason": "every ground truth is already at primitive level (a physical law, an IAPWS-IF97 state, or a figure read at source), so there was no compound claim to reduce"},
      {"technique": "trade-off", "phase": 4, "reason": "the question asks for a bound and a decomposition, not a choice between viable options"}
    ]
  },
  "gate": {
    "passes": [
      {"bands": ["Rigorous", "Sound", "Hand-wavy", "Sound", "Rigorous", "Rigorous"], "gate_cleared": true, "hand_wavy_cap_cleared": true}
    ],
    "fix_repeat_fired": false,
    "cleared": true
  },
  "re_entry": {"fired": false, "edges": []},
  "conclusion": {
    "recommendation": "Use 54.32% gross as the law-permitted ceiling for this power block. It is the second-law limit for heat delivered by Solar Salt cooling from 565 °C to 290 °C and rejected at a 43.11 °C condenser, and it is tighter than the 62.27% isothermal Carnot figure (chain C1, chain C2). Against it, practice (circa 42% gross) sits about 12.3 points below on the wet condenser basis, or about 8–10 points below if the 42% is a dry-cooled figure (chain C4).",
    "confidence": "MEDIUM"
  }
}
```
