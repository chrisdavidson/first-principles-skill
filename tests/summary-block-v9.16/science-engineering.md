**Disclosed:** The daily electrical load was not supplied. This analysis builds an assumed winter load of 6.1 kWh/day (DC), for two adults with propane or wood for heating, cooking and hot water. It also gives per-kWh/day ratios so the result can be rescaled to a metered load. Site irradiance and equipment figures could not be read at source because the network was unreachable, so every sourced input carries a `?`.

## Answer

**Recommendation:** For the assumed load, use about 2.4 kWp of PV at a 50° south tilt (1.993 kWp minimum) and about 20.4 kWh of LFP nameplate, kept above 0 °C. For any other load, scale at 0.326 kWp and 3.333 kWh per DC kWh/day (chains C3, C4).

**Band (from §6):** MEDIUM (chains C1, C2, C3, C4, C5).

**Would change it:** Metering the actual winter load (chain C1) and a site-specific December irradiance run at 50° tilt (chain C2).
# First-Principles Analysis — Off-grid PV array and battery sizing, high-desert New Mexico (35° N)

## 1. Problem Essence

**Core problem:** How many kW of PV and how many kWh of battery must be sized so that PV and battery alone supply the cabin's daily electrical energy every day, including through the worst sustained low-sun stretch the design has to ride out. The binding case is the lowest-sun month, not the annual average. The inputs that drive the size are the daily load, December irradiance on the array plane, the chain of conversion losses, and how many sunless days the design must bridge.

The trigger for this analysis is "what size system", but the question it has to answer is an energy balance: how much energy goes in (PV yield in the worst month) and how much goes out (daily load plus losses), and how much storage is needed to carry the load across a gap in input. The daily load was **not supplied**. It is the input the whole answer scales with, so this analysis (a) builds an explicit bottom-up load for two adults in a cabin with non-electric heat, cooking and water heating, and (b) states the result as ratios per kWh/day of load, so the answer carries over to any metered load.

**Success criteria:**
1. The array is large enough to cover the daily DC load **plus** refilling a drawn-down battery in the binding month (December), and also in a below-average December.
2. The battery's *usable* capacity covers a stated number of sunless days at the design load. The nameplate figure includes the depth-of-discharge limit.
3. Every figure is shown as arithmetic and has been recomputed on its own.
4. The answer also works for a load other than the assumed one: it gives kWp and kWh per kWh/day of DC load.
5. It names the physical conditions (temperature, tilt) that the sizes depend on, so the stated capacities actually deliver.
6. Before scoring, a composite of PV + battery + a backup generator was tested as an option (§5). It is not assumed away.

## 2. Assumptions Table

| Assumption | Type | Treatment | Verdict | Verification |
|------------|------|-----------|---------|--------------|
| A1: Space heating, cooking and water heating use propane or wood, not electricity | untested belief | Verify or flag. This is a scope condition of the load build | Challenge — not supplied by user. If any of these is electric, the load rises several-fold. The per-kWh ratios in C3/C4 still apply | unverified — flagged; disclosed at top of response |
| A2: The appliance-level daily energies in GT-5? represent this household | untested belief | Verify or flag | Challenge — built from typical ratings × hours, not metered | unverified — flagged GT-5? |
| A3: December is the binding design month | physical law | Accept as ground-truth candidate | Accept — follows from solar geometry (GT-2?) combined with the winter irradiance data (GT-3?) | GT-2?, GT-3? |
| A4: Albuquerque-area irradiance data represent this site | untested belief | Verify or flag | Challenge — the site is in high-desert NM at 35° N, but local horizon shading and valley fog are unknown | unverified — flagged; the poor-December bracket (GT-4?) gives a 15% cushion |
| A5: The design bridges D = 3 fully sunless days | convention | Challenge before use | Accept — challenged. The 3-day figure is convention and is not derived from site storm statistics. It is used as the reliability specification, and D = 2 and D = 4 are also given | convention; sensitivity shown in C3 |
| A6: "Reliably" means PV + battery alone, with no generator | convention | Challenge before use | Accept — challenged in §5. The composite with a generator is a real option. Kept out because the question asks for panel and battery sizes that meet the load, and "no grid" signals self-sufficiency | §5 Dead End 2 |
| A7: Conversion-efficiency figures (GT-7?) apply | untested belief | Verify or flag | Challenge — published design values, not measured on this equipment | unverified — flagged GT-7? |
| A8: The battery is kept above 0 °C | current constraint | Record expiry | Accept — binds while the chemistry is LFP. It lifts with a heated-battery product or a chemistry rated for cold charging | GT-8? |
| A9: A drawn-down bank must be refilled within 7 days | convention | Challenge before use | Accept — challenged. A 7-day refill keeps a second storm from arriving while the bank is still low. A 14-day refill is the rival and is priced in §5 | convention; priced in C4 |
| A10: Snow does not cover the array for more than one day at a time | untested belief | Verify or flag | Challenge — at a 50° tilt snow slides off readily, but this has not been measured at the site | unverified — flagged; covered by the autonomy days |
| A11: The load is roughly flat from day to day. The winter blower is the main seasonal addition | untested belief | Verify or flag | Challenge — summer cooling may add load. Checked in C5 | unverified — flagged |
| A12: An evaporative cooler (0.5 kW × 8 h) is added in summer | untested belief | Verify or flag | Challenge — added by the Phase 4 audit as a second-order scenario, not part of the base load | unverified — flagged |
| A13: LFP fades to 80% of nameplate within the system's service life | untested belief | Verify or flag | Challenge — datasheet-typical, not read | unverified — flagged GT-9? |

## 3. Ground Truths

- **GT-1?** A PV module's kWp rating is its DC output at standard test conditions of 1000 W/m² irradiance. So peak-sun-hours (PSH, in h/day) numerically equals plane-of-array irradiation in kWh/m²/day, and 1 kWp produces PSH kWh/day before losses. Unit check: kWh/m²/day ÷ 1 kW/m² = h/day; × 1 kW = kWh/day. — definition; unverified: the STC standard text (IEC 60904-3) was not opened. Phase 3 failure record: no network (DNS resolution failed), so the source was not reachable.
- **GT-2?** Noon solar elevation = 90° − latitude + declination. At 35° N this gives 90 − 35 − 23.44 = **31.56°** at the December solstice and 90 − 35 + 23.44 = **78.44°** at the June solstice. December also has the shortest day. — geometry (physical law); unverified: the obliquity figure 23.44° was not read at a source. The arithmetic was recomputed.
- **GT-3?** Monthly-average plane-of-array irradiation for Albuquerque (≈35.1° N), fixed south-facing array: December ≈ **5.4** kWh/m²/day at 50° tilt and ≈ **4.9** at 35° tilt; annual average ≈ **6.4** at 35° tilt; June ≈ **6.0** at 50° tilt. These are estimates recalled from the NREL typical-year data (NREL Solar Radiation Data Manual / PVWatts), not measured by this analysis. — unverified. Phase 3 failure record: the PVWatts v8 API (developer.nrel.gov) was attempted for 35° and 50° tilt and was unreachable (DNS resolution failure, no network).
- **GT-4?** A below-average December at 50° tilt ≈ **4.6** kWh/m²/day. This is an estimate of year-to-year minimum monthly variability recalled from the same NREL data. — unverified; same Phase 3 failure record as GT-3?.
- **GT-5?** Appliance daily energies. These are estimates (rating × hours), not measurements:
  - refrigerator 1.100 kWh
  - LED lighting 10 lamps × 8 W × 4 h = 0.320 kWh
  - well pump: 2 people × 60 gal = 120 gal ÷ 10 gal/min = 12 min = 0.2 h × 1.0 kW = 0.200 kWh
  - propane-furnace blower 0.4 kW × 4 h = 1.600 kWh (winter)
  - satellite internet terminal 0.050 kW × 24 h = 1.200 kWh
  - laptops/phones 2 × 0.05 kW × 4 h = 0.400 kWh
  - washer 0.3 kWh × 4 loads ÷ 7 days = 0.171 kWh
  - microwave/kettle 1.0 kW × 0.3 h = 0.300 kWh

  — unverified: estimated, not metered.
- **GT-6?** Usable depth of discharge: LFP 0.90 and flooded lead-acid 0.50, taken at cycle-life-preserving design values. These are published design values. — unverified: manufacturer datasheets not opened (no network).
- **GT-7?** Published design values for the conversion chain:
  - inverter conversion efficiency 0.94
  - inverter idle draw 20 W
  - MPPT charge-controller efficiency 0.97
  - battery charge-path efficiency 0.95
  - PV derate 0.88, covering soiling, wiring, mismatch and temperature (cold winter cells partly offset these)

  — unverified: datasheets not opened.
- **GT-8?** LFP cells must not be charged below 0 °C (a manufacturer charge-temperature limit). — unverified: datasheet not opened.
- **GT-9?** LFP banks fade to about 80% of nameplate after several thousand cycles, and at roughly one cycle per day that is the system's service life. — unverified: published design value, not read.
- **GT-10** First law of thermodynamics applied to a battery: across any interval with no charging input, the energy delivered cannot exceed the usable stored energy. So a bank of usable energy U supplies a load of L per day for at most U ÷ L days. — physical law; no external figure is asserted.

**Provenance summary:**

```text
?-marked: GT-1?, GT-2?, GT-3?, GT-4?, GT-5?, GT-6?, GT-7?, GT-8?, GT-9? (9 of 10)
Read-at-source: none. GT-10 is unsuffixed as a physical law and asserts no sourced figure; no chain rests on a read-at-source figure.
Phase 3 failure records: GT-3?, GT-4? — PVWatts API unreachable (DNS failure, no network); GT-1?, GT-6?, GT-7?, GT-8?, GT-9? — sources not reachable for the same reason; GT-2? — obliquity not read; GT-5? — no source exists (estimate, would need metering).
```

## 4. Derivation Chains

### Conclusion C1: The winter design DC load is 6.109 kWh/day for two adults in a cabin with non-electric heat, cooking and water heating

GT-5? (appliance kWh/day estimates) + GT-7? (inverter 0.94 efficiency, 20 W idle)
→ AC loads sum to 1.100 + 0.320 + 0.200 + 1.600 + 1.200 + 0.400 + 0.171 + 0.300 = 5.291 kWh/day
→ inverter conversion raises the draw on the DC bus to 5.291 ÷ 0.94 = 5.629 kWh/day
→ adding inverter idle of 0.020 kW × 24 h = 0.480 kWh gives 5.629 + 0.480 = 6.109 kWh/day of DC load in the winter design month

**Pre-check:** head GT-5?, GT-7? · ?-marked: GT-5?, GT-7? · lowest cited: none · Inputs ceiling: MEDIUM
**Confidence:** MEDIUM — the Inputs axis is short. GT-5? is an estimate: metering the cabin for one winter week (or measuring each appliance with a plug-in meter) would remove it as a cause of the downgrade. GT-7? would be removed by the chosen inverter's datasheet efficiency and idle figures. Inference: arithmetic only; it recomputes. Rivals: the rival load profile (electric heat or cooking) is excluded by the scope condition in the conclusion text, and the per-kWh ratios in C3/C4 carry any other load.

### Conclusion C2: One kWp tilted at 50° delivers 4.379 kWh/day into storage in an average December, and 3.730 kWh/day in a poor one

GT-2? (Dec noon elevation 31.56°) + GT-3? (Dec POA 5.4 at 50°, 4.9 at 35°) + GT-4? (poor Dec 4.6 at 50°) + GT-1? (PSH × kWp) + GT-7? (derate chain)
→ December combines the lowest sun and the shortest day, so it is the month whose irradiation limits a fixed array
→ tilting to latitude + 15° = 50° raises December POA from 4.9 to 5.4 kWh/m²/day, a gain of 5.4 ÷ 4.9 − 1 = 10.2% *[Assumes: A4]*
→ the PV-to-battery path keeps 0.88 × 0.97 × 0.95 = 0.8109 of STC-rated energy
→ one kWp at 50° stores 5.4 × 0.8109 = 4.379 kWh/day in an average December, and 4.6 × 0.8109 = 3.730 kWh/day in a poor one

**Pre-check:** head GT-2?, GT-3?, GT-4?, GT-1?, GT-7? · ?-marked: GT-2?, GT-3?, GT-4?, GT-1?, GT-7? · lowest cited: none · Inputs ceiling: MEDIUM
**Confidence:** MEDIUM — the Inputs axis is short:
- GT-3? and GT-4? would be removed as causes of the downgrade by a PVWatts run (or an NSRDB typical-year file) for the exact site coordinates at 50° tilt.
- GT-1? and GT-2? would be removed by reading IEC 60904-3 and an ephemeris value for the obliquity.
- GT-7? would be removed by reading the equipment datasheets.

A4 is priced: if the site's December is up to 15% worse than Albuquerque's average, the value is still within the poor-December figure this endpoint already states, so the endpoint stands. Rivals: sizing on the annual average is ruled out in §5 Dead End 1, by the solar geometry in GT-2?.

### Conclusion C3: The battery needs 20.36 kWh of LFP nameplate (3.333 kWh per DC kWh/day), housed above 0 °C, for a 3-day autonomy target

C1 (6.109 kWh/day DC load) + GT-10 (energy balance, U ÷ L days) + GT-6? (LFP usable depth 0.90) + GT-8? (no LFP charging below 0 °C)
→ bridging D sunless days needs D × 6.109 kWh of usable storage *[Assumes: A5]*
→ at D = 3 that is 3 × 6.109 = 18.33 kWh usable
→ at 0.90 usable depth the nameplate is 18.33 ÷ 0.90 = 20.36 kWh, which is 3 ÷ 0.90 = 3.333 kWh of nameplate per DC kWh/day
→ the bank must be kept in space held above 0 °C, because a cold LFP bank cannot accept the charge that refills it *[Assumes: A8]*

**Pre-check:** head C1 (MEDIUM), GT-10, GT-6?, GT-8? · ?-marked: GT-6?, GT-8? · lowest cited: MEDIUM · Inputs ceiling: MEDIUM
**Confidence:** MEDIUM — the Inputs axis is short:
- C1 is MEDIUM.
- GT-6? would be removed as a cause of the downgrade by the chosen battery's datasheet usable-capacity rating.
- GT-8? would be removed by its charge-temperature specification.

A5 is priced: the endpoint is stated at the D = 3 reliability specification. At D = 2 the nameplate is 2 × 6.109 ÷ 0.90 = 13.58 kWh, and at D = 4 it is 4 × 6.109 ÷ 0.90 = 27.15 kWh. The per-D ratio of 1 ÷ 0.90 = 1.111 kWh of nameplate per kWh of daily load per day of autonomy stands for any D. A8 is priced: if the bank cannot be kept warm, the endpoint moves to a cold-rated chemistry, not to a different energy figure. Rivals: the lead-acid bank (§5 Dead End 3) and the generator composite (§5 Dead End 2) are both settled in §5.

### Conclusion C4: The array needs at least 1.993 kWp (0.326 kWp per DC kWh/day); 2.4 kWp at 50° tilt keeps a 7-day refill even in a poor December

C1 (6.109 kWh/day, MEDIUM) + C2 (4.379 / 3.730 kWh per kWp-day, MEDIUM) + C3 (18.33 kWh usable, MEDIUM)
→ covering the load alone in an average December needs 6.109 ÷ 4.379 = 1.395 kWp
→ refilling a fully drawn 3-day bank within 7 days adds 18.33 ÷ 7 = 2.618 kWh/day *[Assumes: A9]*
→ load plus recovery is 6.109 + 2.618 = 8.727 kWh/day, which needs 8.727 ÷ 4.379 = 1.993 kWp, i.e. 1.993 ÷ 6.109 = 0.326 kWp per DC kWh/day
→ a 2.4 kWp array (6 × 400 W) yields 2.4 × 3.730 = 8.953 kWh/day in a poor December, refilling the bank in 18.33 ÷ (8.953 − 6.109) = 6.45 days

**Pre-check:** head C1 (MEDIUM), C2 (MEDIUM), C3 (MEDIUM) · ?-marked: none · lowest cited: MEDIUM · Inputs ceiling: MEDIUM
**Confidence:** MEDIUM — the Inputs axis is short: C1, C2 and C3 are each MEDIUM, and their own confidence lines carry the verification paths. A9 is priced: with a 14-day refill instead, the minimum becomes (6.109 + 18.33 ÷ 14) ÷ 4.379 = 1.694 kWp. The 2.4 kWp endpoint still stands because it exceeds both. Rivals: the 14-day refill rival is settled in §5 Dead End 4.

### Conclusion C5: The 2.4 kWp / 20.4 kWh design absorbs a summer cooling load, but late in life its autonomy falls to 2.4 days unless the bank is bought with about 25% headroom

C4 (2.4 kWp, MEDIUM) + C3 (20.36 kWh nameplate, MEDIUM) + GT-3? (June POA 6.0 at 50°) + GT-9? (LFP fades to 80%)
→[2nd] actor lens: the occupants, seeing a summer surplus, add an evaporative cooler at 0.5 kW × 8 h = 4.0 kWh/day *[Assumes: A12]*
→[2nd] summer DC load becomes (5.291 − 1.600 + 4.000) ÷ 0.94 + 0.480 = 8.662 kWh/day against a June yield of 2.4 × 6.0 × 0.8109 = 11.677 kWh/day, so it still closes
→[3rd] time lens: after fading to 80% of nameplate, usable storage falls to 20.36 × 0.80 × 0.90 = 14.66 kWh, which is 14.66 ÷ 6.109 = 2.40 days of winter load *[Assumes: A13]*
→ holding the 3-day target at end of life needs 20.36 ÷ 0.80 = 25.45 kWh of nameplate bought up front

**Pre-check:** head C4 (MEDIUM), C3 (MEDIUM), GT-3?, GT-9? · ?-marked: GT-3?, GT-9? · lowest cited: MEDIUM · Inputs ceiling: MEDIUM
**Confidence:** MEDIUM — the Inputs axis is short:
- C4 and C3 are MEDIUM.
- GT-3? would be removed as a cause of the downgrade by the site PVWatts run.
- GT-9? would be removed by the battery's warranty end-of-life capacity figure.

A12 is priced: without the cooler, summer load is lower still, so the "still closes" hop only strengthens. A13 is priced: with milder fade, the headroom needed shrinks, and the endpoint remains an upper bound on what is needed. No extension step contradicts a ground truth. Rivals: none live — this is an extension of C3/C4, not a competing answer.

## 5. Abandoned Reasoning

### Dead End 1: Sizing the array on the annual-average irradiance

**What was tried:** Using the annual average of 6.4 kWh/m²/day (35° tilt, GT-3?). That gives a yield of 6.4 × 0.8109 = 5.190 kWh per kWp-day and an array of 8.727 ÷ 5.190 = 1.682 kWp.

**Why abandoned:** The December geometry in GT-2? makes December the limiting month. The annual-sized array delivers only 1.682 × 4.379 = 7.364 kWh/day in December. That covers the 6.109 load but leaves only 7.364 − 6.109 = 1.255 kWh/day to refill 18.33 kWh, a refill time of 18.33 ÷ 1.255 = 14.6 days. That fails success criterion 1 (C2, C4).

**What it ruled out:** Any sizing rule that uses an average across seasons. It also ruled out the 35° latitude tilt: in December that tilt needs 8.727 ÷ (4.9 × 0.8109) = 2.196 kWp, against 1.993 kWp at 50°.

### Dead End 2: The composite — PV + smaller battery + backup generator

**What was tried:** A split: D = 1.5 days of battery (1.5 × 6.109 ÷ 0.90 = 10.18 kWh), with a generator covering longer storms.

**Why abandoned:** It is feasible, and it is the cheaper composite. But it answers a different reliability specification. It adds a fuel-supply and maintenance dependency to the system, and the question ("panel array and battery bank ... to meet the load reliably", no grid) sets out to size PV + battery to carry the load by themselves (A6). Under that specification the generator is outside the system being sized. Chains C3 and C4 establish the self-sufficient sizes.

**What it ruled out:** Treating the generator composite as the default answer. It remains the named alternative in §6 Trade-offs if the owner accepts a fuel dependency.

### Dead End 3: A flooded lead-acid bank instead of LFP

**What was tried:** The same 18.33 kWh of usable storage at 0.50 usable depth (GT-6?), which needs 18.33 ÷ 0.50 = 36.66 kWh of nameplate.

**Why abandoned:** It needs 36.66 ÷ 20.36 = 1.80 times the nameplate. Lead-acid also loses usable capacity in cold, and it must be refilled to full regularly, which a winter-limited array (C2) cannot guarantee.

**What it ruled out:** Lead-acid as the default chemistry. LFP's charge-temperature limit (GT-8?) is handled by housing the bank indoors (C3).

### Dead End 4: A 14-day refill target

**What was tried:** Relaxing A9 to a 14-day refill: (6.109 + 18.33 ÷ 14) ÷ 4.379 = (6.109 + 1.309) ÷ 4.379 = 1.694 kWp.

**Why abandoned:** High-desert winter storms come in series. A bank still half-empty from the previous storm cannot bridge the next one, so the effective autonomy drops below D = 3 and success criterion 2 fails (C3, C4).

**What it ruled out:** Arrays smaller than about 2.0 kWp at this load.

## 6. Conclusion

**Recommended approach:** For the assumed 6.1 kWh/day winter DC load, the recommended system has three parts (chains C3, C4):
- a PV array of about **2.4 kWp** (6 × 400 W), fixed facing south at a **50° tilt**; 1.993 kWp is the minimum
- an **LFP battery bank of about 20.4 kWh nameplate** (18.3 kWh usable, 3 days of autonomy)
- housing for the bank in space kept above 0 °C

**Key insight:** The answer is set by December, not by the sunny annual average, and it scales linearly with load. Size **0.326 kWp and 3.333 kWh of LFP nameplate per kWh/day of DC load**. Continuous 24-hour loads dominate that load: refrigerator, internet terminal and inverter idle total 1.100 + 1.200 + 0.480 = 2.78 of the 6.11 kWh/day. So metering and trimming them is the cheapest way to shrink the whole system (chains C1, C4).

**Trade-offs acknowledged:** The system is PV + battery only. A backup generator would let the bank shrink to about 10 kWh, at the cost of a fuel dependency (chain C3). The array produces a summer surplus, which can absorb an evaporative cooler (chain C5). The 3-day autonomy falls to 2.4 days as the battery fades, unless about 25.5 kWh is bought up front (chain C5).

**Pre-check:** head C1 (MEDIUM), C2 (MEDIUM), C3 (MEDIUM), C4 (MEDIUM), C5 (MEDIUM) · ?-marked: none · lowest cited: MEDIUM · Inputs ceiling: MEDIUM
**Confidence:** MEDIUM — chains C1, C2, C3, C4 and C5 are each rated MEDIUM, and their own lines carry the verification paths. The two that would move the numbers most:
- metering the actual winter load (C1)
- a site-specific December irradiance run at 50° tilt (C2)
## Appendix — process output

## Assumption Audit scan (process output)

| Chain | Step | Step Text (brief) | Assumption surfaced? | Added to Table? |
|---|---|---|---|---|
| C1 | 1 | AC loads sum to 5.291 | no (A1/A2 already in table; A1 is a scope condition in the endpoint) | n/a |
| C1 | 2 | ÷0.94 → 5.629 | no (A7) | n/a |
| C1 | 3 | +0.480 idle → 6.109 | no | n/a |
| C2 | 1 | December limits | no (A3) | n/a |
| C2 | 2 | 50° tilt +10.2% | yes — A4 site ≈ Albuquerque | already present; marked [Assumes: A4] |
| C2 | 3 | derate 0.8109 | no (A7) | n/a |
| C2 | 4 | 4.379 / 3.730 per kWp | no | n/a |
| C3 | 1 | D × 6.109 | yes — A5 D = 3 | already present; marked |
| C3 | 2 | 18.33 usable | no | n/a |
| C3 | 3 | ÷0.90 → 20.36 | no | n/a |
| C3 | 4 | above 0 °C | yes — A8 | already present; marked |
| C4 | 1 | 1.395 kWp | no | n/a |
| C4 | 2 | +2.618 refill | yes — A9 7-day refill | already present; marked |
| C4 | 3 | 1.993 kWp; 0.326/kWh | no | n/a |
| C4 | 4 | 2.4 kWp poor-Dec 6.45 d | no (A10 snow is covered by autonomy; already in table) | n/a |
| C5 | 1 | cooler 4.0 kWh | yes — A12 | added in audit (new row); marked |
| C5 | 2 | summer 8.662 vs 11.677 | no | n/a |
| C5 | 3 | fade → 2.40 days | yes — A13 | added in audit (new row); marked |
| C5 | 4 | 25.45 kWh | no | n/a |

## Techniques not applied (process output)

- theoretical-limit (Phase 1) — not applicable — the essence is an energy balance on a given load, not a question of whether a conventional figure is a hard bound
- theoretical-limit (Phase 4) — not applicable — no conclusion needs the law-permitted ceiling. Module efficiency is already folded into kWp, so array area is not the binding quantity
- inversion (Phase 2) — not applicable — the assumption set is explicit and wide (13 rows), not suspiciously thin
- fishbone (Phase 2) — not applicable — the question is a sizing derivation, not a multi-causal cause space
- trade-off (Phase 4) — not applicable — the sizes are derived, not chosen among viable options. The one composite (PV + battery + generator) answers a different reliability specification and is recorded in §5 Dead End 2

## Adversarial pass (process output)

**Recompute:** each figure was recomputed independently with a script and by hand. All match the chain text, and every product with a factor above 1 lands above its base:
- 5.291 AC → 5.291 ÷ 0.94 = 5.629 → +0.480 = 6.109
- 0.88 × 0.97 × 0.95 = 0.8109
- 5.4 × 0.8109 = 4.379; 4.6 × 0.8109 = 3.730
- 5.4 ÷ 4.9 = 1.102 (+10.2%)
- 3 × 6.109 = 18.33; 18.33 ÷ 0.90 = 20.36; 3 ÷ 0.90 = 3.333
- 13.58 and 27.15 (D = 2, 4)
- 6.109 ÷ 4.379 = 1.395; 18.33 ÷ 7 = 2.618; 8.727 ÷ 4.379 = 1.993; 1.993 ÷ 6.109 = 0.326
- 2.4 × 3.730 = 8.953; 18.33 ÷ 2.844 = 6.45
- summer (5.291 − 1.6 + 4.0) ÷ 0.94 + 0.48 = 8.662; 2.4 × 6.0 × 0.8109 = 11.677
- 20.36 × 0.8 × 0.9 = 14.66; ÷ 6.109 = 2.40; 20.36 ÷ 0.8 = 25.45
- §5 checks: 1.682, 7.364, 14.6, 2.196, 10.18, 36.66, 1.80, 1.694

**Sensitivity:** the flip ground truth is GT-5? (the load), and it is `?`-marked. Every size scales linearly with it, so doubling the load doubles both sizes. It cannot be verified in this analysis (it needs metering), so it carries the confidence caveat on C1, and the answer is given per kWh/day so that it survives. Weakest link per chain:
- C1: GT-5?
- C2: GT-3? (site irradiance unread)
- C3: A5 (D = 3 is convention)
- C4: the refill-period convention A9
- C5: GT-9?

**Rival:** Headline rival: size on the annual average (about 1.7 kWp). Ruled out in §5 Dead End 1 by GT-2?/C2. Intermediate chains:
- C3: generator composite (§5 Dead End 2) and lead-acid (§5 Dead End 3)
- C4: 14-day refill (§5 Dead End 4)
- C1: rival not applicable — the rival electric-load profile is excluded by the scope condition in the conclusion, and the ratios carry it
- C2: tilt 35° (§5 Dead End 1)
- C5: rival not applicable — an extension, not a competing answer

**Premise:** It is a year after commissioning. The cabin ran out of power repeatedly last winter, and the 2.4 kWp / 20.4 kWh system has failed.

**Causes:**
- Installer: the bank was placed in an unheated shed and refused charge on cold mornings.
- Occupants: the real load was about 9 kWh/day — a second freezer, electric blanket, a space heater on cold nights.
- Occupants: the furnace blower ran 8 h, not 4.
- Owner/payer: a cheaper battery with 80% usable depth was bought.
- Installer: the array was mounted at 30° for aesthetics or roof pitch.
- Site: winter afternoon shade from a ridge or trees, missing from the Albuquerque data.
- Weather: a 5-day storm series with snow on the panels.
- Installer: the inverter idle draw was 50 W, not 20 W.
- Owner/payer: the bank has already faded.
- Supplier: the charge controller was undersized and clipped.

**Clusters:**
- K1 "real load exceeded the design load": second freezer, electric heating, blower hours, idle draw. Bears on GT-5?, GT-7?, C1, and through it C3/C4.
- K2 "installed conditions differ from design conditions": unheated shed, 30° tilt, site shading, snow. Bears on GT-8?, GT-3?, A4, A10, C2, C3.
- K3 "capacity delivered below nameplate": 80% usable depth, fade, clipped controller. Bears on GT-6?, GT-9?, C3, C5.
- K4 "weather beyond the design event": 5-day storm. Bears on A5, C3.

**Disposition:**
- K1 (fatal): plan change. Size from a metered winter week using the per-kWh ratios (C4 key-insight ratios), and ban resistive heating loads. Tripwire: battery state of charge below 40% at dawn on 3 consecutive clear days — the owner sees it on the monitor app.
- K2 (fatal): plan change. The recommendation specifies 50° tilt, an unshaded December solar window, and the bank above 0 °C (C3, C4). Tripwire: a battery-management "charge inhibited — low temperature" event, seen by the owner.
- K3 (costly but survivable): accepted risk, with mitigation — buy about 25.5 kWh nameplate or check the datasheet usable depth (C5).
- K4 (costly but survivable): accepted risk, with mitigation — the D = 4 sizing (27.15 kWh) or a portable generator as a named fallback (§5 Dead End 2). Tripwire: a forecast of 4 or more overcast days, seen by the owner.

**Falsification:** the conclusion is false if a site-specific December plane-of-array irradiation at 50° tilt comes in below about 4.0 kWh/m²/day, or if the metered winter DC load exceeds about 7.4 kWh/day. At that load the 2.4 kWp poor-December yield of 8.953 kWh/day leaves less than 1.5 kWh/day to refill 18.33 kWh, and refill time exceeds about 12 days.

## §6→§4 closure ledger (process output)

- "Recommended approach: ~2.4 kWp at 50°, ~20.4 kWh LFP, above 0 °C" → chain C3, C4 ✓
- "Key insight: December-set, linear; 0.326 kWp and 3.333 kWh per kWh/day; continuous loads dominate" → chain C1, C4 ✓
- "Trade-offs acknowledged: generator composite; summer surplus; fade to 2.4 days" → chain C3, C5 ✓
- "Pre-check line" → chains C1–C5 ✓
- "Confidence: MEDIUM" → chains C1–C5 ✓

## Self-audit scan (process output)

| Chain | Chain Head (brief) | Form conforming? | Rule applied | Dependency clean? | Band | Act attempted? | Edges fired |
|---|---|---|---|---|---|---|---|
| C1 | GT-5? + GT-7? | yes | n/a | yes | MEDIUM | no | none |
| C2 | GT-2? + GT-3? + GT-4? + GT-1? + GT-7? | yes | n/a | yes | MEDIUM | yes | none |
| C3 | C1 + GT-10 + GT-6? + GT-8? | yes | n/a | yes | MEDIUM | no | none |
| C4 | C1 + C2 + C3 | yes | n/a | yes | MEDIUM | no | none |
| C5 | C4 + C3 + GT-3? + GT-9? | yes | n/a | yes | MEDIUM | yes | none |

| §6 Span (brief) | Construct | Claim under R11? | R11 clause applied | Chain cited |
|---|---|---|---|---|
| Recommended approach | bold lead-in | yes | a bold lead-in whose colon closes the bold span | C3, C4 |
| Recommended approach — array item | list item | no | direct entailment of the already-cited Recommended approach claim above it | n/a |
| Recommended approach — battery item | list item | no | direct entailment of the already-cited Recommended approach claim above it | n/a |
| Recommended approach — housing item | list item | no | direct entailment of the already-cited Recommended approach claim above it | n/a |
| Key insight | bold lead-in | yes | a bold lead-in whose colon closes the bold span | C1, C4 |
| Trade-offs acknowledged | bold lead-in | yes | a bold lead-in whose colon closes the bold span | C3, C5 |
| Pre-check | bold lead-in | yes | a bold lead-in whose colon closes the bold span | C1–C5 (its head) |
| Confidence | bold lead-in | yes | a bold lead-in whose colon closes the bold span | C1, C2, C3, C4, C5 |
| Confidence — metering item | list item | no | direct entailment of the already-cited Confidence claim above it | n/a |
| Confidence — irradiance item | list item | no | direct entailment of the already-cited Confidence claim above it | n/a |

Scan complete: 5 chain rows, one per section-4 chain block in order; 10 section-6 rows, one per construct in order — 5 claims under R11, 5 excluded. 0 chains malformed, 0 claims untraced.
## Self-Audit Gate (process output)

**Criterion 1: Identify Essence**
Quoted span: "How many kW of PV and how many kWh of battery must be sized so that PV and battery alone supply the cabin's daily electrical energy every day, including through the worst sustained low-sun stretch the design has to ride out. The binding case is the lowest-sun month, not the annual average."
Band: **Sound**
Justification: The core question is named, and each of the six success criteria is checkable against §6. But the Core problem runs to three sentences rather than one, which falls short of the Rigorous single-sentence test.

**Criterion 2: Challenge Assumptions**
Quoted span: "| C5 | 1 | cooler 4.0 kWh | yes — A12 | added in audit (new row); marked |" and the A3 row's Verification cell "GT-2?, GT-3?"
Band: **Sound**
Justification: Every row uses the four-type scheme, has an em-dash verdict and was challenged where needed, and the audit covers all 19 chain steps. One row (A3) feeds a chain through unverified ground truths, and its Verification cell cites those IDs without the "unverified — flagged" notation.

**Criterion 3: Establish Ground Truths**
Quoted span: comparison — enumerated GT-1?–GT-9?; the list carries `?` on exactly those nine, and GT-10 is the only unsuffixed entry. Failure records name developer.nrel.gov as unreachable (DNS failure).
Band: **Sound**
Justification: The enumeration matches the list and the unreachable-source records are present. However, GT-10 is unsuffixed with no specific source citation ("physical law; no external figure is asserted"), which is the one-entry shortfall the Sound band describes.

**Criterion 4: Reason Upward**
Quoted span: "| C4 | C1 + C2 + C3 | yes | n/a | yes | MEDIUM | no | none |" (all five rows read `yes` / `yes`), and §5 "**Why abandoned:** The December geometry in GT-2? makes December the limiting month."
Band: **Rigorous**
Justification: Every chain conforms and is dependency-clean. Every hop's arithmetic recomputes (Adversarial Recompute part). Assumption-bearing hops carry `[Assumes:]` marks. The four dead ends use the What-was-tried / Why-abandoned / What-it-ruled-out structure with specific reasons, and no analogy is used as evidence.

**Criterion 5: Validate**
Quoted span: C3 "**Confidence:** MEDIUM — the Inputs axis is short … A5 is priced: the endpoint is stated at the D = 3 reliability specification … Rivals: the lead-acid bank (§5 Dead End 3) and the generator composite (§5 Dead End 2) are both settled in §5."
Band: **Sound**
Justification: Every line names its `?` inputs and cited chains with verification paths, prices its assumptions, and the pre-mortem record is complete with dispositions. But the generator-composite rival to C3/C4 is settled by the scope convention A6, not by an unsuffixed ground truth. A strict reading of the Rivals axis would put C3 and C4 at LOW rather than MEDIUM. That calibration question is left disclosed rather than resolved.

**Criterion 6: Conclusion-to-Ground-Truth Traceability**
Quoted span: "| Key insight | bold lead-in | yes | a bold lead-in whose colon closes the bold span | C1, C4 |", and Key insight text "Size 0.326 kWp and 3.333 kWh of LFP nameplate per kWh/day of DC load … Continuous 24-hour loads dominate that load"
Band: **Rigorous**
Justification: All five §6 claims cite chains and none is untraced. The Key Insight states a non-obvious finding (the December-set linear ratios and the dominance of continuous loads) rather than restating the recommendation.

No Absent, 0 Hand-wavy — cleared on first scoring pass; Fix/Repeat not fired. Unresolved caveat carried: the C3/C4 Rivals-axis calibration noted under Criterion 5.

**Gate result:** cleared · passes: 1 · Fix/Repeat fired: no

## Structured summary (process output)

```json
{
  "schema_version": 1,
  "run_mode": "full-composer",
  "assumptions": [
    {
      "id": "A-1",
      "type": "untested belief",
      "verdict": "Challenge"
    },
    {
      "id": "A-2",
      "type": "untested belief",
      "verdict": "Challenge"
    },
    {
      "id": "A-3",
      "type": "physical law",
      "verdict": "Accept"
    },
    {
      "id": "A-4",
      "type": "untested belief",
      "verdict": "Challenge"
    },
    {
      "id": "A-5",
      "type": "convention",
      "verdict": "Accept"
    },
    {
      "id": "A-6",
      "type": "convention",
      "verdict": "Accept"
    },
    {
      "id": "A-7",
      "type": "untested belief",
      "verdict": "Challenge"
    },
    {
      "id": "A-8",
      "type": "current constraint",
      "verdict": "Accept"
    },
    {
      "id": "A-9",
      "type": "convention",
      "verdict": "Accept"
    },
    {
      "id": "A-10",
      "type": "untested belief",
      "verdict": "Challenge"
    },
    {
      "id": "A-11",
      "type": "untested belief",
      "verdict": "Challenge"
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
    }
  ],
  "ground_truths": [
    {
      "id": "GT-1",
      "read_at_source": false
    },
    {
      "id": "GT-2",
      "read_at_source": false
    },
    {
      "id": "GT-3",
      "read_at_source": false
    },
    {
      "id": "GT-4",
      "read_at_source": false
    },
    {
      "id": "GT-5",
      "read_at_source": false
    },
    {
      "id": "GT-6",
      "read_at_source": false
    },
    {
      "id": "GT-7",
      "read_at_source": false
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
      "read_at_source": true
    }
  ],
  "chains": [
    {
      "id": "C1",
      "confidence": "MEDIUM",
      "rests_on": [
        "GT-5?",
        "GT-7?"
      ]
    },
    {
      "id": "C2",
      "confidence": "MEDIUM",
      "rests_on": [
        "GT-2?",
        "GT-3?",
        "GT-4?",
        "GT-1?",
        "GT-7?"
      ]
    },
    {
      "id": "C3",
      "confidence": "MEDIUM",
      "rests_on": [
        "C1",
        "GT-10",
        "GT-6?",
        "GT-8?"
      ]
    },
    {
      "id": "C4",
      "confidence": "MEDIUM",
      "rests_on": [
        "C1",
        "C2",
        "C3"
      ]
    },
    {
      "id": "C5",
      "confidence": "MEDIUM",
      "rests_on": [
        "C4",
        "C3",
        "GT-3?",
        "GT-9?"
      ]
    }
  ],
  "dead_ends": [
    "Sizing the array on the annual-average irradiance",
    "The composite — PV + smaller battery + backup generator",
    "A flooded lead-acid bank instead of LFP",
    "A 14-day refill target"
  ],
  "techniques": {
    "applied": [
      "second-order",
      "pre-mortem"
    ],
    "not_applied": [
      {
        "technique": "theoretical-limit",
        "phase": 1,
        "reason": "the essence is an energy balance on a given load, not a question of whether a conventional figure is a hard bound"
      },
      {
        "technique": "theoretical-limit",
        "phase": 4,
        "reason": "no conclusion needs the law-permitted ceiling. Module efficiency is already folded into kWp, so array area is not the binding quantity"
      },
      {
        "technique": "inversion",
        "phase": 2,
        "reason": "the assumption set is explicit and wide (13 rows), not suspiciously thin"
      },
      {
        "technique": "fishbone",
        "phase": 2,
        "reason": "the question is a sizing derivation, not a multi-causal cause space"
      },
      {
        "technique": "trade-off",
        "phase": 4,
        "reason": "the sizes are derived, not chosen among viable options. The one composite (PV + battery + generator) answers a different reliability specification and is recorded in §5 Dead End 2"
      }
    ]
  },
  "gate": {
    "passes": [
      {
        "bands": [
          "Sound",
          "Sound",
          "Sound",
          "Rigorous",
          "Sound",
          "Rigorous"
        ],
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
    "recommendation": "For the assumed 6.1 kWh/day winter DC load, the recommended system has three parts (chains C3, C4):\n- a PV array of about **2.4 kWp** (6 × 400 W), fixed facing south at a **50° tilt**; 1.993 kWp is the minimum\n- an **LFP battery bank of about 20.4 kWh nameplate** (18.3 kWh usable, 3 days of autonomy)\n- housing for the bank in space kept above 0 °C",
    "confidence": "MEDIUM"
  }
}
```
