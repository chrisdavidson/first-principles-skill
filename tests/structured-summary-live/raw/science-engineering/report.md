**Disclosed:** The user did not supply the cabin's daily electrical load, and every size in this analysis is proportional to it. This analysis could not ask, so it rebuilds the load bottom-up as an estimate (C1, flagged GT-5?) and states the sizing per kWh/day so that a measured load can replace the estimate. The cabin's exact coordinates were also not supplied, and chain C7 shows they matter. No re-entry edge fired.

## Answer

**Recommendation:** Measure the load first. Then size at 0.502 kWp of PV (50° tilt) and 3.35 kWh of nominal LiFePO4 per kWh/day. The estimated 5.07 kWh/day gives 2.7 kWp + 18 kWh (chain C6), which ran empty on 3 days in 11 years at Albuquerque (chains C4, C5). Simulate your exact site (chain C7); if it resembles the eastern-plains cell, add a 2 kW generator (chain C8).

**Band (from §6):** MEDIUM (chains C1, C4, C5, C6, C8).

**Would change it:** metered load (chain C1), a site-coordinate simulation (chain C7), the battery's datasheet and the NSRDB September 2012 quality flags (chain C4), and current price quotes (chain C5).

## 1. Problem Essence

**Core problem:** What fixed-tilt PV capacity (kWp) and battery capacity (kWh nominal) let an off-grid cabin at about 35° N in high-desert New Mexico carry two adults' year-round electrical load through the worst run of short, cloudy winter days in the solar record, given that the daily load itself was not supplied and every size scales with it?

The triggering question asks about the *daily* load; the cause that actually sets the size is the *sequence* of low-sun days in winter. A design that balances the average day can still run out of energy.

**Success criteria:**

1. The Conclusion states a PV capacity in kWp and a battery capacity in kWh nominal, and ties each to a stated daily-load figure.
2. The Conclusion states the sizing as a ratio per kWh/day of load, so the reader can rescale it to their measured load.
3. The Conclusion states the reliability the design achieves, as battery-empty days per year from an hour-by-hour simulation over a multi-year record, against the threshold of 0.5 days/year or fewer (excluding months flagged as suspect data).
4. Every computed figure in section 4 shows its arithmetic, and the adversarial pass record recomputes it to a matching value.
5. The Conclusion says whether a split design (smaller PV and battery plus a backup generator) beats PV plus battery alone, and why.
6. The Conclusion states how strongly the answer depends on where the cabin sits within "high-desert New Mexico at 35° N".

## 2. Assumptions Table

Rows are numbered A-1 to A-20 by position. Rows A-15 to A-20 were added by the end-of-Phase-4 Assumption Audit. Phase 2 inversion of the claim "the recommended system meets the load reliably" produced the precondition rows A-2, A-3, A-4, A-8, A-12 and A-14 (see the inversion block in the appendix).

| Assumption | Type | Treatment | Verdict | Verification |
|------------|------|-----------|---------|--------------|
| The cabin's electrical load is about 4.59 kWh/day AC at the appliances (bracket 2.99–7.11), from a bottom-up appliance estimate | untested belief | Verify, or flag as unverified | Challenge — the user gave no load; it is rebuilt from GT-4 and GT-5?, and every size in the answer scales with it | unverified — flagged (GT-5?); 2–4 weeks of metered consumption, or the user's appliance list, verifies it |
| Space heating, water heating and cooking use propane or wood, not electricity | untested belief | Verify, or flag as unverified | Challenge — electric resistance heating would add tens of kWh/day and change the order of magnitude of the answer; the user did not say | unverified — flagged; asking the user settles it |
| The PVGIS grid cell at 35.08° N, 106.65° W, 1507 m (Albuquerque) represents the site | untested belief | Verify, or flag as unverified | Challenge — the user gave only latitude and climate class; GT-11 shows that two other 35° N high-desert cells give 0.18 and 1.91 empty days/yr for the same design | partially verified by GT-11 (the site range was probed); exact site unverified — flagged; re-running GT-3 at the cabin's coordinates verifies it |
| The 2005–2015 NSRDB record (11 winters) contains the worst winter sequence to design for | untested belief | Verify, or flag as unverified | Challenge — 11 years is a short sample for a rare event, and a worse winter outside the record is plausible | unverified — flagged; a longer record (NSRDB 1998–present) would test it |
| "Reliably" means 0.5 battery-empty days/yr or fewer, averaged over the record, excluding months flagged as suspect data | convention | Explicitly challenge before use | Challenge — the user did not define reliability, so this threshold is this analysis's choice; a user who needs zero days reads the per-design counts in C4 instead | set by this analysis and stated so the user can replace it |
| Fixed south-facing array tilted at 50° | convention | Explicitly challenge before use | Accept — winter is the binding season (C2); the annual-optimum 34° (GT-2) favours summer, when GT-3 shows surplus energy is already being spilled | GT-1, GT-2, GT-3 |
| Required PV and battery scale linearly with daily load | untested belief | Verify, or flag as unverified | Accept — GT-10 models the whole system with one proportional performance ratio (0.67) and a fixed hourly profile, so the model is homogeneous in PV, battery and load; the one fixed loss (standby, A-15) is added to the load explicitly | GT-10 (model structure read at source); linearity of real hardware unverified — flagged |
| The battery is kept above 0 °C while charging (it is housed indoors) | current constraint | Record expiry conditions | Accept — lapses if the battery is moved to an unheated shed, because high-desert winter nights go below 0 °C and LFP charging below 0 °C is prohibited (GT-7?); a self-heating battery lifts the constraint | unverified — flagged (GT-7?) |
| The LFP bank can be discharged to 10% state of charge (90% usable) | untested belief | Verify, or flag as unverified | Accept — matches the 10% cutoff used in every GT-3 run; no datasheet was opened | unverified — flagged (GT-7?) |
| Energy delivered to loads cannot exceed the energy harvested minus conversion and storage losses | physical law | Accept as a ground-truth candidate | Accept — conservation of energy; it underpins the monthly-balance floor in C2 | first law of thermodynamics |
| The daily load is the same every day of the year (SHScalc uses a constant consumption) | untested belief | Verify, or flag as unverified | Challenge — summer evaporative cooling raises the load to about 6.04 kWh AC; checked separately for July in C6 | checked in C6 against GT-1 July irradiance; intra-day profile unverified — flagged |
| The roughly 7 September and 3 October empty days that appear at every size are a data artefact (Sep 2012), not real weather | untested belief | Verify, or flag as unverified | Challenge — Sep 2012 horizontal irradiation is 0.567 of the other Septembers' mean (GT-2), which is implausible for a desert month but not proven | unverified — flagged (GT-9?) |
| Installed prices are about $1.00/W for PV (with mounting and controller), $300/kWh for LFP, and $1,000 for a 2 kW inverter-generator | untested belief | Verify, or flag as unverified | Challenge — used only for the cost criterion in the trade-off; prices vary widely by vendor and date | unverified — flagged (GT-8?) |
| Snow cover does not take panel output away for several days at a time | untested belief | Verify, or flag as unverified | Accept — a 50° tilt sheds snow faster than shallow tilts, and PVGIS irradiance does not model snow on the module | unverified — flagged |
| Inverter standby draw of about 20 W runs continuously and is not covered by PVGIS's proportional performance ratio | untested belief | Verify, or flag as unverified | Accept — adding it to the load is conservative (C1) | unverified — flagged (GT-6?) |
| The worst-to-mean December irradiation ratio measured at 34° tilt also holds at 50° | untested belief | Verify, or flag as unverified | Accept — both tilts see the same weather and the ratio is set by cloudiness; priced in C2 | unverified — flagged; a MRcalc run at 50° verifies it |
| After installation, occupant load stays at the design figure (no load creep) | untested belief | Verify, or flag as unverified | Challenge — summer surplus invites new loads (C6 second-order effects) | unverified — flagged; a battery-monitor log over the first year verifies it |
| Battery capacity fade over the system's life is not separately modelled by PVGIS | untested belief | Verify, or flag as unverified | Accept — GT-10's PR covers "degradation" in aggregate but has no explicit capacity-fade term; treated as a late-life risk in C6 | unverified — flagged |
| A backup generator starts and has fuel when it is needed | untested belief | Verify, or flag as unverified | Challenge — option C's reliability depends on it; cold starts at 2000 m and fuel storage are real failure modes | unverified — flagged |
| The two extra PVGIS cells (Grants 35.15° N 107.85° W; eastern plains 35.0° N 105.67° W) span the climate range of high-desert NM at 35° N | untested belief | Verify, or flag as unverified | Accept — they lie west and east of the Albuquerque cell, at higher elevations; other microclimates may lie outside them | unverified — flagged |

## 3. Ground Truths

PVGIS figures were read by opening the PVGIS v5.2 API JSON responses for the parameters stated; the fields named were extracted from each response. Every figure below is a modelled or measured-derived value from the PVGIS-NSRDB satellite dataset (2005–2015). None of them is a measurement taken at the cabin.

- **GT-1** PVGIS PVcalc output for 35.08° N, 106.65° W, 1 kWp, 50° slope, due south, 14% system loss, PVGIS-NSRDB. Grid-tied-basis daily yield E_d (kWh/kWp/day), Jan to Dec: 5.12, 5.33, 5.43, 5.34, 4.83, 4.51, 4.29, 4.60, 4.83, 5.35, 5.19, 4.57. Plane-of-array irradiation H(i)_d is 5.5 kWh/m²/day in December and 5.9 in July. December E_m is 141.77 kWh with an inter-year SD_m of 12.3 kWh; E_y is 1805.27 kWh. Measured-derived (satellite) modelled values — source: PVGIS API v5.2 PVcalc; read-at-source: JSON `outputs.monthly.fixed` fields E_d, E_m, H(i)_d, SD_m and `outputs.totals.fixed.E_y`. Cross-check: E_m ÷ days-in-month equals E_d for all 12 months (for example 141.77 ÷ 31 = 4.573).
- **GT-2** PVGIS MRcalc monthly irradiation at the same point. December H(i_opt)_m for 2005–2015 (kWh/m²): 183.32, 143.19, 154.20, 140.61, 160.67, 138.32, 149.09, 159.84, 164.91, 150.41, 153.30, giving a minimum of 138.32 (2010) and a mean of 154.35. The optimal inclination reported is 34°. September 2012 horizontal H(h)_m is 101.71 kWh/m², while the other ten Septembers range from 170.40 to 190.94. Measured-derived values — source: PVGIS API v5.2 MRcalc; read-at-source: JSON `outputs.monthly` records (year, month, H(h)_m, H(i_opt)_m) and `inputs` optimal-angle field.
- **GT-3** PVGIS SHScalc hourly off-grid simulation at the same point: 50° slope, 10% discharge cutoff, consumption 5376 Wh/day, 4017 simulated days. Modelled values. Percentage of days on which the battery became empty (f_e):

  | PV (W) / battery (Wh) | Total f_e | Jan | Feb | Sep | Oct | Nov | Dec | Spilled E_lost (Wh/day) |
  |---|---|---|---|---|---|---|---|---|
  | 1400 / 9000 | 6.42 | 11.08 | 13.96 | 5.15 | 5.57 | 6.36 | 24.63 | 1245.78 |
  | 1400 / 18000 | 2.36 | 4.08 | 6.49 | 2.12 | 0.88 | 1.21 | 13.78 | 1239.77 |
  | 1700 / 18000 | 0.72 | 0.58 | 0.0 | 2.12 | 0.88 | 0.91 | 4.11 | 2392.13 |
  | 2000 / 12000 | 1.39 | 3.21 | 0.97 | 2.42 | 0.88 | 1.82 | 7.33 | 3641.02 |
  | 2000 / 18000 | 0.50 | 0.29 | 0.0 | 2.12 | 0.88 | 0.91 | 1.76 | 3641.20 |
  | 2000 / 27000 | 0.22 | 0.0 | 0.0 | 1.82 | 0.88 | 0.0 | 0.0 | 3638.93 |
  | 2700 / 18000 | 0.32 | 0.0 | 0.0 | 2.12 | 0.88 | 0.61 | 0.29 | 6633.66 |

  Months not shown are 0.0 in every run, except Jul 2.35, Aug 1.76, Mar 4.99, Apr 0.91, May 0.29, Jun 0.30 in the 1400/9000 run and Jul–Aug 0.0 elsewhere. Source: PVGIS API v5.2 SHScalc; read-at-source: JSON `outputs.totals` (f_e, E_lost_d) and `outputs.monthly` f_e for each of the seven requests.
- **GT-4** The energy needed to lift water is E = ρ·g·h·V, with ρ = 1000 kg/m³ and g = 9.81 m/s², and 1 kWh = 3.6 × 10⁶ J. Physical law and SI definition — read-at-source: definition of gravitational potential energy and of the kilowatt-hour. It is irreducible.
- **GT-5?** Appliance figures, all estimates: an efficient full-size refrigerator uses 350 kWh/yr; an LED lamp is 9 W; a laptop draws 50 W; a satellite-internet terminal draws 50 W continuously; a cold wash uses 0.5 kWh; a microwave draws 1.1 kW; a furnace blower draws 100 W; a well pump's wire-to-water efficiency is 0.40; two adults use 200 L of water/day; well head is 100 m (bracket 250 m). Unverified: these are typical nameplate values from memory and site-specific guesses. No Energy Guide label or datasheet is cited, so the Phase 3 step found no source it could open.
- **GT-6?** An off-grid inverter's standby draw is about 20 W. Unverified: a typical datasheet range from memory; no datasheet cited, nothing to open.
- **GT-7?** LFP cells may be cycled to 10% state of charge and must not be charged below 0 °C. Unverified: typical manufacturer terms from memory; no datasheet cited, nothing to open.
- **GT-8?** Installed prices: PV about $1.00/W including mounting and controller, LFP about $300/kWh, a 2 kW inverter-generator about $1,000. Unverified estimates: no price list cited, and prices are date-sensitive.
- **GT-9?** The September 2012 NSRDB record at this location is a data artefact, not real weather. Unverified: no NSRDB quality flag and no ground-station record was opened. The only supporting evidence is GT-2's 0.567 ratio, plus the fact that the same September/October f_e values (2.12% and 0.88%) appear at all three cells in GT-3 and GT-11.
- **GT-10** The PVGIS off-grid model simulates "hour by hour" over several years. It uses "a performance ratio of the whole off-grid system of 0.67", which is "intended to include losses from the performance of the battery, the inverter and degradation". Consumption is "the energy consumption of all the electrical equipment connected to the system during a 24 hour period", spread over the hours as typical home use. A day counts as "empty" when the state of charge reaches the cutoff in any hour. Source: PVGIS 5 user manual, section 6 (off-grid); read-at-source: the quoted sentences.
- **GT-11** PVGIS SHScalc with the same settings (50°, 10% cutoff, 5376 Wh/day) at two other 35° N high-desert cells. Modelled values:

  | Cell | PV / battery | Total f_e | Jan | Feb | Sep | Oct | Nov | Dec |
  |---|---|---|---|---|---|---|---|---|
  | Grants area 35.15° N 107.85° W, 1968 m | 2700 / 18000 | 0.30 | 0.0 | 0.0 | 2.12 | 0.88 | 0.61 | 0.0 |
  | Eastern plains 35.0° N 105.67° W, 2147 m | 2700 / 18000 | 0.77 | 2.33 | 2.60 | 2.12 | 0.88 | 0.91 | 0.59 |
  | Eastern plains | 2000 / 27000 | 0.75 | 1.17 | 5.19 | 1.82 | 0.88 | 0.30 | 0.0 |
  | Eastern plains | 2700 / 27000 | 0.42 | 0.29 | 2.27 | 1.82 | 0.88 | 0.0 | 0.0 |

  Source: PVGIS API v5.2 SHScalc; read-at-source: JSON `inputs.location` (lat, lon, elevation), `outputs.totals.f_e` and `outputs.monthly` f_e for each of the four requests.

**Phase 3 verification record.** GT-1, GT-2, GT-3, GT-10 and GT-11 were opened at source. GT-5?, GT-6?, GT-7?, GT-8? and GT-9? carry no openable citation (they are estimates or an attribution), so they keep the `?`, and no read was possible. Phase 3 failure record: the NREL PVWatts v8 API (developer.nrel.gov) was attempted as an irradiance source and was unreachable (DNS lookup failed). It was replaced by PVGIS, which uses the same underlying NSRDB satellite data for the Americas.

`?`-marked: GT-5, GT-6, GT-7, GT-8, GT-9 (5 of 11)
Read-at-source: GT-1 — PVcalc JSON `outputs.monthly.fixed` (E_d, E_m, H(i)_d, SD_m); GT-2 — MRcalc JSON `outputs.monthly` records; GT-3 — SHScalc JSON totals and monthly f_e for seven runs; GT-4 — SI definitions; GT-10 — PVGIS 5 user manual §6 quoted sentences; GT-11 — SHScalc JSON for four runs at two further cells

## 4. Derivation Chains

The load is rebuilt in C1 as a power × time estimate. C2 and C3 establish what sets the size and what sizing cannot fix. C4 finds the feasible designs, C5 chooses among them, C6 rescales to any load and extends it forward, C7 tests the site assumption, and C8 handles the site where PV plus battery alone does not qualify. All simulated reliability figures convert a percentage to days as f_e × days-in-record: Jan, Mar, May, Jul, Aug, Oct and Dec have 11 × 31 = 341 days; Apr, Jun, Sep and Nov have 11 × 30 = 330; Feb has 11 × 28 + 3 leap days = 311.

### Conclusion C1: The estimated design load is 5.07 kWh/day (4.59 kWh at the appliances plus 0.48 kWh inverter standby), with a bracket of 3.47–7.59; the simulated 5.376 kWh/day covers the central case with a 6.1% margin

Appliance energy table (power × hours, or annual ÷ 365), using GT-5? figures:

| Load | Arithmetic | kWh/day |
|---|---|---|
| Refrigerator | 350 ÷ 365 | 0.959 |
| LED lighting | 8 lamps × 9 W × 5 h ÷ 1000 | 0.360 |
| Well pump | 1000 × 9.81 × 100 m × 0.2 m³ ÷ 0.40 ÷ 3.6×10⁶ | 0.136 |
| Laptops | 2 × 50 W × 4 h ÷ 1000 | 0.400 |
| Satellite internet | 50 W × 24 h ÷ 1000 | 1.200 |
| Washer | 5 loads/week × 0.5 kWh ÷ 7 | 0.357 |
| Kitchen | microwave 1.1 kW × 0.25 h + 0.2 small appliances | 0.475 |
| Furnace blower (propane furnace) | 100 W × 4 h ÷ 1000 | 0.400 |
| Miscellaneous | allowance | 0.300 |
| **Sum at appliances (AC)** | | **4.587** |

GT-4 (lift energy) + GT-5? (appliance figures) + GT-6? (standby) + GT-10 (PVGIS consumption is all connected equipment; PR 0.67 includes inverter loss)
→ lifting 0.2 m³/day through 100 m at 40% wire-to-water efficiency costs 0.136 kWh/day, small next to refrigeration
→ the appliance energies in the table sum to 4.587 kWh/day at the outlets [Assumes: A-2 — heat, hot water and cooking are non-electric]
→ inverter conversion loss is already inside the PVGIS 0.67 PR, so only the fixed standby draw is added: 20 W × 24 h = 0.48 kWh/day [Assumes: A-15]
→ the central design load is 4.587 + 0.48 = 5.067 kWh/day
→ the low bracket drops internet and the blower: 4.587 − 1.200 − 0.400 + 0.48 = 3.467 kWh/day
→ the high bracket adds a freezer (300 ÷ 365 = 0.822), 250 m well head (+0.204) and induction cooking (+1.5): 7.114 + 0.48 = 7.594 kWh/day
→ the 5.376 kWh/day used in every simulation exceeds the central 5.067 by 5.376 ÷ 5.067 − 1 = 6.1%

**Pre-check:** head GT-4, GT-5?, GT-6?, GT-10 · ?-marked: GT-5?, GT-6? · lowest cited: none · Inputs ceiling: MEDIUM
**Confidence:** MEDIUM — the Inputs axis is short. GT-5? (appliance figures) and GT-6? (standby) are estimates, and 2–4 weeks of metered consumption (a shunt battery monitor, or a plug-in meter on each major appliance) removes them as a cause of the downgrade. A-2 on the second hop is priced: if heat, hot water or cooking were electric, the endpoint would not stand, so it is stated conditional on A-2. A-15 is priced: dropping the standby term lowers the load to 4.587, which leaves the endpoint's coverage claim standing with a wider margin. Every hop recomputes. No rival load figure exists in the analysis; the bracket is the stated spread. Weakest link: the 1.2 kWh/day satellite-internet line, the largest single item, which is an occupant choice.

### Conclusion C2: The winter energy balance sets a PV floor of 1.46 kWp (mean December) to 1.63 kWp (worst December) for 5.376 kWh/day; simulation shows this floor is necessary but not sufficient, so the day-by-day sequence sets the final size

GT-1 (Dec plane-of-array 5.5 kWh/m²/day at 50°) + GT-2 (Dec irradiation by year) + GT-10 (off-grid PR 0.67) + GT-3 (simulated empty days)
→ by energy conservation, each kWp at 50° delivers 5.5 × 0.67 = 3.685 kWh/day to loads in a mean December
→ the mean-December floor is 5.376 ÷ 3.685 = 1.459 kWp
→ the worst December in the record (2010) received 138.32 ÷ 154.35 = 0.8961 of mean irradiation [Assumes: A-16 — the 34° ratio holds at 50°]
→ the worst-December floor is 5.376 ÷ (3.685 × 0.8961) = 1.628 kWp
→ at 1.4 kWp, below both floors, the simulated battery empties on 13.78% × 341 = 47.0 December days even with 18 kWh
→ at 1.7 kWp, above both floors, December empty days are still 4.11% × 341 = 14.0
→ meeting the monthly balance does not prevent shortfalls, so the sequence of cloudy days, not the monthly total, sets the size

**Pre-check:** head GT-1, GT-2, GT-10, GT-3 · ?-marked: none · lowest cited: none · Inputs ceiling: HIGH
**Confidence:** HIGH — every head input was read at source (Ground Truths list) and every hop recomputes. A-16 is priced: the worst-December floor would rise above the 1.7 kWp test point only if the 50° ratio were below 5.376 ÷ (3.685 × 1.7) = 0.858, against 0.896 measured at 34°. Even then the endpoint stands, because it rests on the 1.4 and 1.7 kWp simulations, not on that floor. The rival ("the monthly balance with the grid-tied 14% loss is sufficient") is ruled out by GT-10 and GT-3 in the §5 entry "Monthly-balance sizing on grid-tied yield". Weakest link: the A-16 ratio hop, which the endpoint does not depend on.

### Conclusion C3: About 10 empty days in September and October appear at every tested size, and nearly doubling the PV or adding 50% more storage removes at most one of them

GT-3 (Sep/Oct f_e across seven runs) + GT-2 (Sep 2012 irradiation)
→ September empty days are 2.12% × 330 = 7.0 at 1.4, 1.7, 2.0 and 2.7 kWp with 18 kWh, 2.42% × 330 = 8.0 at 2.0/12, and 1.82% × 330 = 6.0 at 2.0/27
→ October empty days are 0.88% × 341 = 3.0 in every run from 1.4/18 to 2.7/18 and in 2.0/27
→ going from 1.4 to 2.7 kWp (×1.93) or from 18 to 27 kWh (×1.5) removes at most one of these roughly 10 days
→ in the same month, the record holds one anomalous September (2012) at 101.71 ÷ 179.43 = 0.567 of the other ten Septembers' mean horizontal irradiation
→ this residual cannot be bought down by PV or battery size in the tested range, so it is either excluded as suspect data or covered by a non-solar source

**Pre-check:** head GT-3, GT-2 · ?-marked: none · lowest cited: none · Inputs ceiling: HIGH
**Confidence:** HIGH — both inputs were read at source and the day counts recompute. The endpoint is a disjunction and does not depend on whether the anomaly is an artefact; that question (GT-9?) is carried in C4, where it matters. The rival ("a larger system would remove the residual") is ruled out by the 2.0/27 and 2.7/18 rows of GT-3, in the §5 entry "Sizing up to remove the September–October residual". Weakest link: attributing the residual to 2012 specifically, which monthly f_e cannot show; the endpoint does not rest on that attribution.

### Conclusion C4: At the Albuquerque cell, under the 0.5 days/yr criterion, two PV-plus-battery designs qualify: A = 2.0 kWp + 27 kWh (0 days) and B = 2.7 kWp + 18 kWh (0.27 days/yr); 2.0 kWp + 18 kWh and every smaller run do not

GT-3 (seven simulated designs) + GT-7? (10% cutoff is usable LFP depth) + GT-9? (Sep/Oct residual is an artefact) + C2 (HIGH) + C3 (HIGH)
→ excluding the September–October residual per C3, B's empty days are 0.61% × 330 = 2.0 in November plus 0.29% × 341 = 1.0 in December [Assumes: A-12]
→ that is 3.0 days in 11 years, or 0.27 per year, under the 0.5 threshold [Assumes: A-5]
→ A shows 0.0% empty in every month outside September–October
→ 2.0 kWp + 18 kWh gives 1.0 (Jan) + 3.0 (Nov) + 6.0 (Dec) = 10.0 days, or 0.91 per year, over the threshold
→ 1.7 kWp + 18 kWh gives 2.0 + 3.0 + 14.0 = 19.0 days (1.73 per year), and the 2.0/12 and 1.4 kWp runs are worse
→ usable storage at a 10% cutoff is 27 × 0.9 = 24.3 kWh (4.52 days of 5.376 kWh) for A and 18 × 0.9 = 16.2 kWh (3.01 days) for B
→ A and B are the feasible PV-plus-battery designs within the tested grid, and 2.0/18 shows that 3 days of storage is not enough with 2.0 kWp

**Pre-check:** head GT-3, GT-7?, GT-9?, C2 (HIGH), C3 (HIGH) · ?-marked: GT-7?, GT-9? · lowest cited: HIGH · Inputs ceiling: MEDIUM
**Confidence:** MEDIUM — the Inputs axis is short. GT-7? (whether a real LFP bank delivers 90% of nameplate in winter) is removed by the chosen battery's datasheet and a capacity test. GT-9? (whether the Sep/Oct residual is an artefact) is removed by opening the NSRDB hourly data and quality flags for September 2012, or a ground-station record. If the residual is real weather, every design here has about 10 extra days per 11 years (0.9/yr), the threshold fails for both, and backup becomes necessary. A-5 is priced: it is the stated criterion, so the endpoint holds as written; a user who needs zero days picks A, and one who accepts 1/yr can also take 2.0/18. A-12 is the GT-9? input, already named. Weakest link: the GT-9? exclusion.

### Conclusion C5: Weighted trade-off at the Albuquerque cell: B (2.7 kWp + 18 kWh) scores 76, A (2.0 kWp + 27 kWh) 71, and composite C (2.0 kWp + 12 kWh + 2 kW generator) 58, so B is recommended there

C4 (MEDIUM) + GT-3 (empty days and spill) + GT-8? (prices) + GT-1 (December irradiation)
→ the status quo (no system) is knocked out by the no-grid constraint, and the weights were locked before scoring (appendix trade-off block)
→ capital cost is $10,100 for A (2,000 + 27 × 300), $8,100 for B (2,700 + 18 × 300) and $6,600 for C (2,000 + 12 × 300 + 1,000) [Assumes: A-13]
→ the December PV-to-load ratio, a measure of headroom for load growth, is 2.7 × 5.5 × 0.67 ÷ 5.376 = 1.85 for B and 2.0 × 5.5 × 0.67 ÷ 5.376 = 1.37 for A and C
→ C needs its generator on about 56.0 days in 11 years (5.1 per year), which costs it on fuel independence and maintenance [Assumes: A-19]
→ weighted totals: B = 76 > A = 71 > C = 58, driven by load-growth headroom (×3) and capital cost (×4)
→ no single weight change in the 1–5 range flips B to A (the closest is load-growth 3 → 1, leaving B ahead 66 to 65)
→ recommend B at the Albuquerque cell, with A as the choice when zero simulated empty days outweighs about $2,000

**Pre-check:** head C4 (MEDIUM), GT-3, GT-8?, GT-1 · ?-marked: GT-8? · lowest cited: MEDIUM · Inputs ceiling: MEDIUM
**Confidence:** MEDIUM — the Inputs axis is short. C4 is MEDIUM (its own line carries the reason), and GT-8? (prices) is removed by current installed quotes for the two designs; the cost score decides 4 of the 5 points between A and B. A-13 is GT-8?. A-19 is priced: if the generator were unreliable, C's reliability score would fall further and B still wins. The rival (A) is ruled out under the locked weights in the §5 entry "Option A (more battery, less PV) as the recommendation". Weakest link: the cost criterion's dependence on GT-8?.

### Conclusion C6: Size to the measured load at 0.502 kWp and 3.35 kWh nominal per kWh/day (appliance load plus standby); the central estimate rounds to 2.7 kWp + 18 kWh, and the bracket runs from 1.74 kWp + 11.6 kWh to 3.81 kWp + 25.4 kWh

C1 (MEDIUM) + C5 (MEDIUM) + GT-1 (July irradiation) + GT-10 (proportional PR) + GT-3 (spill at B)
→ B's ratios are 2.7 ÷ 5.376 = 0.5022 kWp and 18 ÷ 5.376 = 3.348 kWh nominal per kWh/day [Assumes: A-7]
→ the central 5.067 kWh/day needs 5.067 × 0.5022 = 2.54 kWp and 5.067 × 3.348 = 17.0 kWh, below the simulated 2.7/18 point, which is adopted with its 6.1% margin
→ the low bracket 3.467 needs 1.74 kWp and 11.6 kWh, and the high bracket 7.594 needs 3.81 kWp and 25.4 kWh
→ in July, 2.7 kWp × 5.9 × 0.67 = 10.67 kWh/day covers the cooled-summer load of 6.523 kWh/day by a factor of 1.64 [Assumes: A-11]
→ size the system to the measured load at 0.502 kWp and 3.35 kWh per kWh/day
→[2nd] (actor lens, occupants; immediate) B spills 6.63 kWh/day on average once the battery is full
→[3rd] daytime-shiftable loads such as laundry and pumping to a storage tank therefore cost no storage when run on sunny afternoons
→[2nd] (actor lens, occupants; time lens, first years) that visible surplus invites load creep [Assumes: A-17]
→[3rd] +1 kWh/day of creep raises the need to 6.067 × 0.5022 = 3.05 kWp, above the 2.7 installed
→[2nd] (time lens, about a decade) LFP capacity fade toward roughly 80% shrinks 18 kWh to 18 × 0.8 = 14.4 kWh [Assumes: A-18]
→[3rd] no simulated point exists at 2.7 kWp with 14.4 kWh, so the late-life rise in winter shortfalls is unquantified
→[2nd] (actor lens, payer) mounting and wiring sized for about 4 kWp from day one lets the array grow when creep or fade appears, at lower cost than rebuilding

**Pre-check:** head C1 (MEDIUM), C5 (MEDIUM), GT-1, GT-10, GT-3 · ?-marked: none · lowest cited: MEDIUM · Inputs ceiling: MEDIUM
**Confidence:** MEDIUM — the Inputs axis is capped by C1 and C5, which are MEDIUM and carry their own reasons. A-7 is priced: GT-10's single proportional PR makes the simulated system homogeneous in PV, battery and load, and the one fixed loss is already inside the load, so the ratio holds within the model. Real-hardware non-linearity (controller and inverter minimum sizes) would only push small systems up, and the endpoint stands for loads near the simulated 5.376. A-11 is priced by the 1.64 summer factor: the endpoint stands unless summer load exceeds 10.67 kWh/day. A-17 and A-18 qualify only the second- and third-order extensions, not the endpoint. No extension contradicts a Ground Truth. Load creep works against success criterion 3, and this is reported as a weak link (pre-mortem cluster K2), not a contradiction. Weakest link: the A-7 hop at loads far from 5.376 kWh/day.

### Conclusion C7: Within "high-desert NM at 35° N" the simulated reliability of one fixed design varies about tenfold between cells, so the final sizing needs a simulation at the cabin's own coordinates

GT-11 (two further cells) + GT-3 (Albuquerque cell)
→ at the Grants cell, B's only empty days outside September–October are 0.61% × 330 = 2.0 in November, which is 0.18 per year
→ at the Albuquerque cell, B gives 0.61% × 330 + 0.29% × 341 = 2.0 + 1.0 = 3.0 days, which is 0.27 per year
→ on the eastern plains, B gives 2.33% × 341 + 2.60% × 311 + 0.91% × 330 + 0.59% × 341 = 7.9 + 8.1 + 3.0 + 2.0 = 21.0 days, or 1.91 per year
→ the spread across three cells is 1.91 ÷ 0.18 = about 10.6 times for an identical system and load
→ the cabin's exact coordinates move the answer by about ten times, so the final sizing needs one simulation at the actual site [Assumes: A-20]

**Pre-check:** head GT-11, GT-3 · ?-marked: none · lowest cited: none · Inputs ceiling: HIGH
**Confidence:** HIGH — both inputs were read at source, and every hop recomputes. The September–October residual is excluded identically at all three cells, so GT-9? does not enter the comparison. A-20 is priced: a site outside the two probed cells could do better or worse, which widens the spread and leaves the endpoint standing. Rival: the east–west difference is grid-cell data noise rather than climate. That reading does not contest the endpoint, because noisy cell data also call for a simulation (and ideally a local record) at the actual site. Weakest link: only three cells were sampled.

### Conclusion C8: At the eastern-plains cell no tested PV-plus-battery design meets the 0.5 days/yr criterion, even 2.7 kWp + 27 kWh (0.73/yr), so a cabin whose site simulation looks like that cell needs B plus a 2 kW generator for about 2 days a year

C7 (HIGH) + GT-11 (eastern-plains runs) + C4 (MEDIUM)
→ eastern A (2.0/27) gives 1.17% × 341 + 5.19% × 311 + 0.30% × 330 = 4.0 + 16.1 + 1.0 = 21.1 days (1.92 per year), no better than B's 21.0
→ eastern 2.7 kWp + 27 kWh gives 0.29% × 341 + 2.27% × 311 = 1.0 + 7.1 = 8.1 days (0.73 per year), still above 0.5
→ adding 50% storage to B still leaves 8.1 mostly-February days, so February storms are not suppressed in the tested grid
→ including the September–October residual would only add days, so this result holds whether or not that residual is an artefact
→ for a site whose own simulation resembles this cell, a 2 kW generator covering B's roughly 21 days in 11 years (about 1.9 per year) is the cheapest tested way to meet the criterion [Assumes: A-19]

**Pre-check:** head C7 (HIGH), GT-11, C4 (MEDIUM) · ?-marked: none · lowest cited: MEDIUM · Inputs ceiling: MEDIUM
**Confidence:** MEDIUM — the Inputs ceiling comes from C4 (MEDIUM; its own line names GT-7? and GT-9?). A-19 is priced: if a generator cannot be relied on, the design shifts to "larger than 2.7 kWp + 27 kWh, unsimulated", and the claim that no tested PV-plus-battery design qualifies still stands. The "cell data noise" rival from C7 does not contest this endpoint, because the endpoint is conditional on the cabin's own site simulation resembling the cell rather than on the cell being representative; the §5 entry "Composite C as the general recommendation" records why the generator is not the default elsewhere. Weakest link: the single eastern cell.

## 5. Abandoned Reasoning

### Dead End: Monthly-balance sizing on grid-tied yield

**What was tried:** Sizing PV as load ÷ worst-month yield, using GT-1's grid-tied E_d. That gives 5.376 ÷ 4.57 = 1.18 kWp for a mean December, or 5.376 ÷ (4.57 × 0.8961) = 1.31 kWp for the worst December.

**Why abandoned:** It contradicts GT-3 and GT-10. GT-1's 14% loss is a grid-tied figure and leaves out battery round-trip loss, which GT-10's off-grid PR of 0.67 includes. GT-3 shows that even 1.4 kWp, above both figures, empties the battery on 47 December days in 11 years.

**What it ruled out:** Any "divide by the worst month's yield" rule of thumb as the final answer. It survives only as the necessary floor stated in C2.

### Dead End: A separate inverter-efficiency division on top of PVGIS

**What was tried:** Converting the AC load to a DC battery draw (5.0 ÷ 0.93 = 5.376 kWh/day) before entering it into the simulator.

**Why abandoned:** It double-counts a loss. GT-10 states that the 0.67 PR already includes inverter losses and that consumption is the energy of the connected equipment. Only the fixed standby draw (A-15) is not proportional, so only that is added (C1).

**What it ruled out:** Treating 5.376 as the DC equivalent of 5.0 kWh AC. It is retained only as a simulated load that covers the central 5.067 with a 6.1% margin.

### Dead End: Days-of-autonomy as the sizing rule

**What was tried:** Sizing the battery as a fixed number of days of load (the common 3–5-day convention), then choosing PV separately.

**Why abandoned:** C4 shows that the same 18 kWh (3.0 days usable) passes at 2.7 kWp and fails at 2.0 kWp (0.91 days/yr). C8 shows that 27 kWh (4.5 days) fails on the eastern plains. Reliability is a property of the PV-plus-battery pair at a site, not of storage days alone.

**What it ruled out:** Quoting a battery size without its paired PV size and site.

### Dead End: Sizing up to remove the September–October residual

**What was tried:** Raising PV (to 2.7 kWp) and storage (to 27 kWh) until the roughly 10 September/October empty days disappear.

**Why abandoned:** GT-3 shows they persist at about 9–10 days across every size tested (C3), and GT-11 shows identical September/October percentages at all three cells. This is the rival to C3's endpoint, ruled out by GT-3.

**What it ruled out:** Treating that residual as a sizing problem. It is a data-validation question (GT-9?) or a backup-source question.

### Dead End: Option A (more battery, less PV) as the recommendation

**What was tried:** Recommending 2.0 kWp + 27 kWh at the Albuquerque cell because it is the only design with zero simulated empty days there.

**Why abandoned:** Under the weights locked before scoring, A totals 71 against B's 76 (C5). A's zero-day advantage is outweighed by lower load-growth headroom (December PV ratio 1.37 vs 1.85) and a capital cost about $2,000 higher at GT-8? prices. C8 also shows A is no better than B on the eastern plains (21.1 vs 21.0 days).

**What it ruled out:** Storage-heavy designs as the default. A remains the stated alternative for a zero-day requirement at a central or western site.

### Dead End: Composite C as the general recommendation

**What was tried:** A smaller system (2.0 kWp + 12 kWh) with a 2 kW generator covering the shortfall days, to minimise capital cost.

**Why abandoned:** At the Albuquerque cell, C needs the generator on about 56 days in 11 years and scores 58 against B's 76 (C5), losing on fuel independence and maintenance (A-19).

**What it ruled out:** Generator-first designs at central and western sites. C7 shows that a generator added to B is the right composite on the eastern plains, where no tested PV-plus-battery size qualifies.

### Dead End: Tilting at the 34° annual optimum

**What was tried:** Using the 34° optimum GT-2 reports.

**Why abandoned:** C2 shows winter is the binding season. An annual optimum maximises summer energy, which GT-3 shows is already spilled (6.63 kWh/day at B), so it adds nothing to reliability. No simulation at 34° was run, so the size of the winter penalty is not quantified.

**What it ruled out:** Annual-yield tilt as the design tilt for a battery-limited off-grid system.

## 6. Conclusion

**Recommended approach:** Measure or list the load first. Then size to it at 0.502 kWp of south-facing PV at a 50° tilt and 3.35 kWh of nominal LiFePO4 storage per kWh/day of appliance load plus inverter standby (chain C6). For the central estimate of 5.07 kWh/day, that is a 2.7 kWp array and an 18 kWh bank (16.2 kWh usable). At the Albuquerque cell, an hour-by-hour simulation of 2005–2015 shows that bank empty on 3 days in 11 years outside the suspect September–October records (chains C4, C5). The load bracket of 3.47–7.59 kWh/day maps to 1.74 kWp + 11.6 kWh up to 3.81 kWp + 25.4 kWh (chain C6). Re-run the same simulation at the cabin's exact coordinates before buying (chain C7), and if that simulation looks like the eastern-plains cell, add a 2 kW generator for about 2 days a year, because no tested PV-plus-battery size meets the criterion there (chain C8).

**Key insight:** The usual "load ÷ worst-month yield" rule gives only a floor of 1.46–1.63 kWp. The run of cloudy winter days sets the real size, so PV and storage trade against each other as a pair: 2.0 kWp + 27 kWh and 2.7 kWp + 18 kWh both work, while 2.0 kWp + 18 kWh does not (chains C2, C4). Within "35° N high desert", the cabin's location changes the empty-day count of one fixed design by about ten times (chain C7).

**Trade-offs acknowledged:** Design B accepts about 0.27 empty days a year (chain C5) and an average 6.6 kWh/day of energy spilled once the battery is full (chain C6), in exchange for roughly $2,000 less capital than the zero-day option A, at unverified prices (chain C5). About 10 September–October empty days in the record cannot be removed by any tested size; if they are real weather rather than a data artefact, a generator inlet is needed everywhere (chains C3, C4). Leaving mounting and wiring room for about 4 kWp hedges against load creep and battery fade (chain C6).

**Pre-check:** head C1 (MEDIUM), C2 (HIGH), C3 (HIGH), C4 (MEDIUM), C5 (MEDIUM), C6 (MEDIUM), C7 (HIGH), C8 (MEDIUM) · ?-marked: none · lowest cited: MEDIUM · Inputs ceiling: MEDIUM
**Confidence:** MEDIUM — chains C1, C4, C5, C6 and C8 are rated MEDIUM, and each one's own line names its unverified input and how to verify it: the load estimate (GT-5?, GT-6?), the LFP usable depth (GT-7?), the September 2012 artefact (GT-9?) and prices (GT-8?). C2, C3 and C7 are HIGH. The Conclusion adds no downgrade cause of its own: the site-representativeness question (A-3) is carried by chain C7, whose endpoint makes the recommendation conditional on a simulation at the actual site.
## Appendix — process output

## Inversion — Phase 2 (process output)

**Claim:** A PV array and battery sized from the solar record will meet the cabin's load on effectively every day of the year.
**Inverted:** The system runs the battery empty on days that matter.
**Failure-guaranteeing conditions:** (1) the real load is well above the design load; (2) heating, hot water or cooking are electric; (3) the site's weather is worse than the modelled cell; (4) a winter worse than any in the record occurs; (5) the battery cannot charge because it is below 0 °C; (6) snow covers the array for days; (7) the record's worst months are bad data, so the design is tuned to noise.
**Preconditions (as falsifiable claims) and tags:**
- the load is within the stated bracket — load-bearing, unverified → A-1
- space heat, water heat and cooking are non-electric — load-bearing, unverified → A-2
- the modelled cell represents the site — load-bearing, unverified → A-3, then probed in GT-11, C7 and C8
- the 11-year record contains the design winter — load-bearing, unverified → A-4
- the battery stays above 0 °C when charging — load-bearing, current constraint → A-8
- snow does not cover the array for days — not load-bearing at 50° tilt, unverified → A-14
- the anomalous September is bad data — load-bearing for the reliability count, unverified → A-12

Sharpest findings, load-bearing and unverified: A-1, A-2, A-3.

## Trade-off analysis — Phase 4 (process output)

### Options
- **A**: 2.0 kWp + 27 kWh LFP.
- **B**: 2.7 kWp + 18 kWh LFP.
- **C** (composite): 2.0 kWp + 12 kWh LFP + a 2 kW inverter-generator.
- **Status quo** (no electrical system): knocked out by the must-have below.

Must-haves: (1) the load is met without a grid connection, and status quo fails this; (2) shortfall days are 0.5 per year or fewer outside suspect months, counting days covered by a generator as met. A, B and C pass at the Albuquerque cell (C4; C's shortfall days are covered by its generator).

### Criteria & Weights
Weights were locked before any scoring.

| Criterion | Weight | 1 means | 5 means |
|---|---|---|---|
| Reliability from solar alone | 5 | more than 5% of days empty with no backup | 0 empty days outside suspect months |
| Capital cost | 4 | over $15,000 | under $5,000 (linear, $2,500 per point) |
| Fuel independence | 3 | generator runs routinely (more than 20 days/yr) | no fuel needed |
| Load-growth headroom (December PV-to-load ratio, PR 0.67) | 3 | ratio 1.0 | ratio 1.8 or more (0.2 per point) |
| Maintenance simplicity | 2 | engine plus battery maintenance | solid-state only |

### Scoring

| Option | Reliability ×5 | Cost ×4 | Fuel ×3 | Growth ×3 | Maintenance ×2 | Total |
|---|---|---|---|---|---|---|
| A | 5 (0 days; GT-3) = 25 | 3 ($10,100 → 2.96; GT-8?) = 12 | 5 = 15 | 3 (1.37 → 2.86; GT-1, GT-10) = 9 | 5 = 10 | **71** |
| B | 4 (3 days in 11 yr; GT-3) = 20 | 4 ($8,100 → 3.76; GT-8?) = 16 | 5 = 15 | 5 (1.85; GT-1, GT-10) = 15 | 5 = 10 | **76** |
| C | 4 (generator covers about 56 days in 11 yr; GT-3, A-19) = 20 | 4 ($6,600 → 4.36; GT-8?) = 16 | 3 (about 5.1 generator days/yr) = 9 | 3 (1.37) = 9 | 2 (engine; preference — no GT) = 4 | **58** |

### Recommendation
B, 76 against A's 71 and C's 58. **Flip test:** no single weight change in 1–5 flips B to A. The closest is load-growth 3 → 1 (B 66, A 65), then cost 4 → 1 (B 64, A 62); reliability is already at the maximum weight of 5. B is robust to weights but narrow over A, and its cost scores rest on GT-8?, so the collapsed chain C5 is MEDIUM.

## Assumption Audit scan (process output)

| Chain | Step | Step Text (brief) | Assumption surfaced? | Added to Table? |
|---|---|---|---|---|
| C1 | 1 | pump lift 0.136 kWh/day | none | n/a |
| C1 | 2 | appliance sum 4.587 | A-2 non-electric heat/cooking (already in table) | n/a |
| C1 | 3 | add standby 0.48 only | A-15 standby not in PR | yes |
| C1 | 4 | central 5.067 | none | n/a |
| C1 | 5 | low bracket 3.467 | none | n/a |
| C1 | 6 | high bracket 7.594 | none | n/a |
| C1 | 7 | 6.1% margin | none | n/a |
| C2 | 1 | 3.685 kWh/kWp/day delivered | A-10 conservation (already in table) | n/a |
| C2 | 2 | mean floor 1.459 kWp | none | n/a |
| C2 | 3 | worst ratio 0.8961 | A-16 ratio holds at 50° | yes |
| C2 | 4 | worst floor 1.628 kWp | none | n/a |
| C2 | 5 | 1.4 kWp → 47.0 Dec days | none | n/a |
| C2 | 6 | 1.7 kWp → 14.0 Dec days | none | n/a |
| C2 | 7 | sequence sets size | none | n/a |
| C3 | 1 | Sep 6.0–8.0 days at all sizes | none | n/a |
| C3 | 2 | Oct 3.0 days at all sizes | none | n/a |
| C3 | 3 | ×1.93 PV or ×1.5 storage removes ≤1 | none | n/a |
| C3 | 4 | Sep 2012 at 0.567 of mean | none | n/a |
| C3 | 5 | not buyable by size | none | n/a |
| C4 | 1 | B Nov 2.0 + Dec 1.0 | A-12 artefact exclusion (already in table) | n/a |
| C4 | 2 | 0.27/yr under threshold | A-5 threshold (already in table) | n/a |
| C4 | 3 | A 0 days | none | n/a |
| C4 | 4 | 2.0/18 → 0.91/yr | none | n/a |
| C4 | 5 | 1.7/18 → 1.73/yr | none | n/a |
| C4 | 6 | usable 24.3 / 16.2 kWh | A-9 90% usable (already in table) | n/a |
| C4 | 7 | A and B feasible | none | n/a |
| C5 | 1 | status quo knocked out | none | n/a |
| C5 | 2 | capital costs | A-13 prices (already in table) | n/a |
| C5 | 3 | Dec PV ratio 1.85 / 1.37 | none | n/a |
| C5 | 4 | C generator 56.0 days | A-19 generator starts and is fuelled | yes |
| C5 | 5 | totals 76/71/58 | none | n/a |
| C5 | 6 | flip test | none | n/a |
| C5 | 7 | recommend B | none | n/a |
| C6 | 1 | ratios 0.5022 / 3.348 | A-7 linear scaling (already in table) | n/a |
| C6 | 2 | central 2.54 kWp / 17.0 kWh | none | n/a |
| C6 | 3 | bracket 1.74/11.6 to 3.81/25.4 | none | n/a |
| C6 | 4 | July factor 1.64 | A-11 constant load (already in table) | n/a |
| C6 | 5 | size at ratios | none | n/a |
| C6 | 6 | [2nd] spill 6.63 kWh/day when full | none | n/a |
| C6 | 7 | [3rd] daytime-shiftable loads cost no storage | none | n/a |
| C6 | 8 | [2nd] surplus invites load creep | A-17 no load creep | yes |
| C6 | 9 | [3rd] +1 kWh/day creep → 3.05 kWp | none | n/a |
| C6 | 10 | [2nd] capacity fade to 14.4 kWh | A-18 fade not modelled | yes |
| C6 | 11 | [3rd] late-life shortfall unquantified | none | n/a |
| C6 | 12 | [2nd] mounting for 4 kWp | none | n/a |
| C7 | 1 | Grants B 0.18/yr | none | n/a |
| C7 | 2 | Albuquerque B 0.27/yr | none | n/a |
| C7 | 3 | east B 21.0 days, 1.91/yr | none | n/a |
| C7 | 4 | spread 10.6× | none | n/a |
| C7 | 5 | simulate at actual site | A-20 two cells span the range | yes |
| C8 | 1 | east A 1.92/yr | none | n/a |
| C8 | 2 | east 2.7/27 0.73/yr | none | n/a |
| C8 | 3 | +50% storage leaves 8.1 days | none | n/a |
| C8 | 4 | holds whether or not residual is an artefact | none | n/a |
| C8 | 5 | B + 2 kW generator | A-19 (added from C5 step 4) | n/a |

Techniques not applied:
- theoretical-limit — not applicable — Phase 1: the essence is sizing a system to a load, and no current figure is in question as convention versus hard bound
- theoretical-limit — not applicable — Phase 4: no conclusion needs a law-permitted ceiling; the binding quantity is the weather sequence, not a physical limit
- fishbone — not applicable — Phase 2: no multi-causal effect needed category brainstorming, and the assumption space was enumerated by inverting the reliability claim

## Adversarial pass (process output)

**Recompute** — every figure was redone in a separate script, independently of the chain text, and all match. C1: 0.959, 0.360, 0.136, 0.400, 1.200, 0.357, 0.475, 0.400 → sum 4.587; central 5.067; low 3.467; high 7.594; margin 6.09%. C2: 3.685; 1.459 kWp; 0.8961; 1.628 kWp; 47.0 and 14.0 days; pricing threshold 0.8582. C3: 7.0, 8.0, 6.0 Sep days; 3.0 Oct days; 179.43 mean; 0.5668; ×1.929 PV. C4: 2.0 + 1.0 = 3.0 days → 0.273/yr; 2.0/18 → 9.99 days → 0.909/yr; 1.7/18 → 19.0 → 1.727/yr; 24.3 kWh → 4.52 days; 16.2 kWh → 3.01 days. C5: $10,100 / $8,100 / $6,600; ratios 1.851 / 1.371; generator 55.95 days → 5.09/yr; totals 71 / 76 / 58; growth→1 gives A 65, B 66; cost→1 gives A 62, B 64; no flip found by exhaustive single-weight search. C6: 0.5022; 3.348; 2.54 / 17.0; 1.74 / 11.6; 3.81 / 25.4; 10.67 vs 6.523 → 1.636; creep → 3.05 kWp; fade → 14.4 kWh. C7: Grants 2.0 days → 0.18/yr; Albuquerque 2.0 + 1.0 = 3.0 → 0.27/yr; east B 7.9 + 8.1 + 3.0 + 2.0 = 21.0 → 1.91/yr; spread 1.91 ÷ 0.18 = 10.6. C8: east A 4.0 + 16.1 + 1.0 = 21.1 → 1.92/yr; east 2.7/27 1.0 + 7.1 = 8.1 → 0.73/yr. Dead end 1: 1.18 and 1.31 kWp. Every scaled figure moves in the direction of its operation; no figure scaled by a factor above one comes out below its base.

**Sensitivity** — the ground truth whose falsity would flip the conclusion is GT-5? (the load estimate), and it is `?`-marked. A load at the high bracket of 7.594 kWh/day would make the recommended 2.7 kWp + 18 kWh fall short, needing 3.81 kWp + 25.4 kWh. It cannot be verified within this analysis, so the caveat is applied structurally: the recommendation is stated per kWh/day of measured load (C6). Second-most sensitive: the site (A-3, probed by GT-11 in C7 and C8). Weakest link per chain: C1 — the 1.2 kWh/day satellite-internet line; C2 — the A-16 ratio hop, which the endpoint does not rest on; C3 — attributing the residual to 2012; C4 — the GT-9? artefact exclusion; C5 — cost scores resting on GT-8?; C6 — the A-7 linear-scaling hop at loads far from 5.376; C7 — only three cells sampled; C8 — a single cell east of the mountains.

**Rival** — Headline: "a generator is required everywhere; PV plus battery alone is never reliable in this climate." This is ruled out at the central and western cells by GT-3 and GT-11 (B gives 0.27 and 0.18 empty days/yr); see the §5 entry "Composite C as the general recommendation". It stays live if GT-9? is false (the September 2012 residual is real weather), and it is named on C4's confidence line. Intermediate chains: C1 — rival not applicable — no competing load figure exists, and the bracket is the stated spread. C2 → §5 "Monthly-balance sizing on grid-tied yield". C3 → §5 "Sizing up to remove the September–October residual". C4 — rival not applicable — its endpoint is itself a ruling-out of the smaller designs, by the threshold arithmetic. C5 → §5 "Option A (more battery, less PV) as the recommendation". C6 — rival not applicable — the only alternative is sizing without measuring, which C1's MEDIUM band already rejects as the final basis. C7 — the "grid-cell noise rather than climate" rival does not contest C7's endpoint (as its confidence line states). C8 — the same rival does not contest C8's conditional endpoint (the site simulation must resemble the cell), as its confidence line states; the generator-everywhere rival is in the §5 entry "Composite C as the general recommendation".

**Premise** — It is the cabin's second winter. The 2.7 kWp / 18 kWh system has run the battery flat repeatedly in January and February, and the owners now run a generator every week. The plan has already failed. What caused it?

**Causes** (unfiltered; viewpoints: occupants, installer, payer, the weather/data record):
1. (occupants) The real load was about 8 kWh/day: a chest freezer, satellite internet and a small electric heater on the coldest nights.
2. (occupants) After a sunny first summer they added loads and never re-checked the winter balance.
3. (occupants) Laundry and water pumping ran at night, through the battery.
4. (installer) The battery went in an unheated shed, and on cold mornings the BMS blocked charging below 0 °C, so the morning sun was wasted.
5. (installer) A ridge to the south-east shades the array in December, which the PVGIS cell's default horizon does not capture.
6. (installer) The charge controller was sized for 2.7 kWp exactly, with no expansion headroom.
7. (installer) The cabin sits east of the Sandia–Manzano ranges, but the design used the Albuquerque cell.
8. (payer) The cheapest LFP bank delivered about 85% of nameplate.
9. (payer) The site-specific simulation was skipped to save a day.
10. (payer) The mounting was bought for exactly 2.7 kWp, so adding panels meant a new rack.
11. (weather/data) A winter worse than any in 2005–2015 arrived.
12. (weather/data) Wet snow sat on the panels for three days after a storm.
13. (weather/data) The September 2012 dip was real weather, and a similar autumn recurred.

**Clusters**
- **K1 Load under-estimated or grown** (causes 1, 2, 3) — bears on C1, C6, GT-5?, A-1, A-17. Triage: costly but survivable (more PV fixes it). Tripwire: the battery monitor's 30-day mean consumption goes above 5.4 kWh/day; the owner reads it monthly.
- **K2 Site differs from the modelled cell** (causes 5, 7, 9) — bears on C7, C8, GT-11, A-3, A-20. Triage: fatal to the sizing as bought. Tripwire: a site-coordinate SHScalc run (with the local horizon) shows more than 0.5 empty days/yr outside September–October; checked by the buyer before purchase.
- **K3 The battery delivers less than modelled** (causes 4, 8) — bears on C4, GT-7?, A-8, A-9. Triage: costly but survivable. Tripwire: state of charge reaches 10% after less than 15 kWh has been delivered since full; seen on the monitor at the commissioning capacity test and each winter.
- **K4 Weather beyond the record** (causes 11, 12, 13) — bears on C3, C4, GT-9?, A-4, A-14. Triage: costly but survivable. Tripwire: battery below 20% at 08:00 on two consecutive winter mornings; the occupants check daily in winter.
- **K5 No room to expand** (causes 6, 10) — bears on C6. Triage: costly but survivable. Tripwire: no observable signal before expansion is needed; it is found only when K1 or K3 fires.

**Disposition**
- K1 — plan change: measure the load for 2–4 weeks (or list appliances with nameplates) before buying, then size at 0.502 kWp and 3.35 kWh per kWh/day (C6, recommended approach).
- K2 — plan change: re-run the PVGIS off-grid simulation at the cabin's exact coordinates with its horizon before purchase, and on the eastern plains add a 2 kW generator (C7, C8, recommended approach).
- K3 — plan change: house the battery indoors, or buy a self-heating LFP, and do a capacity test at commissioning (A-8; carried in C4's confidence line).
- K4 — accepted risk with a named mitigation: install a generator inlet and transfer switch at build, so a generator can be connected when the tripwire fires (trade-offs in §6, C3/C4).
- K5 — plan change: buy mounting and charge controller sized for about 4 kWp (C6 second-order hop, trade-offs in §6).

**Falsification** — the conclusion is false if an hourly simulation at the cabin's real coordinates, or a first-winter battery-monitor log, at the measured load and a central or western site shows more than 0.5 battery-empty days per year outside the suspect September–October months for an array and bank sized at 0.502 kWp and 3.35 kWh per kWh/day.

## §6→§4 closure ledger (process output)

- "Recommended approach: measure the load, size at 0.502 kWp and 3.35 kWh per kWh/day; central 2.7 kWp + 18 kWh; bracket 1.74/11.6 to 3.81/25.4" → chain C6 ✓
- "3 empty days in 11 years at the Albuquerque cell" → chain C4 ✓ (and C5)
- "re-run the simulation at the exact coordinates" → chain C7 ✓
- "if the site resembles the eastern-plains cell, add a 2 kW generator" → chain C8 ✓
- "Key insight: the monthly rule gives only a floor; PV and storage trade as a pair" → chain C2 ✓ (and C4)
- "Key insight: location changes empty days about tenfold" → chain C7 ✓
- "Trade-offs: B accepts 0.27 days/yr and about $2,000 less capital than A" → chain C5 ✓
- "Trade-offs: 6.6 kWh/day spilled once full; mounting for about 4 kWp" → chain C6 ✓
- "Trade-offs: the Sep–Oct residual cannot be sized away; generator inlet if real weather" → chain C3 ✓ (and C4)
- "Pre-check: head C1–C8 with bands" → chains C1–C8 ✓
- "Confidence: MEDIUM, naming C1, C4, C5, C6, C8 below HIGH" → chains C1, C4, C5, C6, C8 ✓

No claim was cut.

## Self-audit scan (process output)

| Chain | Chain Head (brief) | Form conforming? | Rule applied | Dependency clean? | Band | Act attempted? | Edges fired |
|---|---|---|---|---|---|---|---|
| C1 | GT-4 + GT-5? + GT-6? + GT-10 | unreached | R-GT-lead hop and sentence-closing hop rules at hops 3–7 are beyond the mechanical check's reach (a text scan of every hop found no GT-led hop and no terminal period) | yes | MEDIUM | yes | none |
| C2 | GT-1 + GT-2 + GT-10 + GT-3 | unreached | same two rules unreached at hops 3–7 (text scan clean) | yes | HIGH | yes | none |
| C3 | GT-3 + GT-2 | unreached | same two rules unreached at hops 3–5 (text scan clean) | yes | HIGH | yes | none |
| C4 | GT-3 + GT-7? + GT-9? + C2 + C3 | unreached | same two rules unreached at hops 3–7 (text scan clean) | yes | MEDIUM | yes | none |
| C5 | C4 + GT-3 + GT-8? + GT-1 | unreached | same two rules unreached at hops 3–7 (text scan clean) | yes | MEDIUM | yes | none |
| C6 | C1 + C5 + GT-1 + GT-10 + GT-3 | unreached | same two rules unreached at hops 3–12 (text scan clean) | yes | MEDIUM | yes | none |
| C7 | GT-11 + GT-3 | unreached | same two rules unreached at hops 3–5 (text scan clean) | yes | HIGH | yes | none |
| C8 | C7 + GT-11 + C4 | unreached | same two rules unreached at hops 3–5 (text scan clean) | yes | MEDIUM | yes | none |

| §6 Span (brief) | Construct | Claim under R11? | R11 clause applied | Chain cited |
|---|---|---|---|---|
| Recommended approach: measure load, size per kWh/day … | bold lead-in | yes | bold lead-in whose colon closes the bold span (prescribed lead-in) | C6, C4, C5, C7, C8 |
| Key insight: monthly rule gives only a floor … | bold lead-in | yes | bold lead-in whose colon closes the bold span (prescribed lead-in) | C2, C4, C7 |
| Trade-offs acknowledged: B accepts 0.27 days/yr … | bold lead-in | yes | bold lead-in whose colon closes the bold span (prescribed lead-in) | C5, C6, C3, C4 |
| Pre-check: head C1 … C8 | bold lead-in | yes | bold lead-in whose colon closes the bold span | C1–C8 (in head) |
| Confidence: MEDIUM … | bold lead-in | yes | bold lead-in whose colon closes the bold span (prescribed lead-in) | C1, C4, C5, C6, C8, C7 |

```text
Scan complete: 8 chain rows, one per section-4 chain block in order; 5 section-6 rows, one per construct in order — 5 claims under R11, 0 excluded. 0 chains malformed, 0 claims untraced.
```

## Self-Audit Gate (process output)

Assumption Audit check: the Assumption Audit scan has one row per hop for C1 (7), C2 (7), C3 (5), C4 (7), C5 (7), C6 (12), C7 (5) and C8 (5), matching section 4 hop for hop. Self-audit scan check: 8 chain rows for 8 section-4 blocks and 5 rows for 5 section-6 constructs; the reconciliation line recounts.

**Criterion 1: Identify Essence**
Quoted span: "What fixed-tilt PV capacity (kWp) and battery capacity (kWh nominal) let an off-grid cabin at about 35° N in high-desert New Mexico carry two adults' year-round electrical load through the worst run of short, cloudy winter days in the solar record, given that the daily load itself was not supplied and every size scales with it?" and success criterion 3: "The Conclusion states the reliability the design achieves, as battery-empty days per year … against the threshold of 0.5 days/year or fewer"
Band: **Rigorous**
Justification: The single sentence names the binding cause (the winter sequence) rather than the triggering "daily load", and each of the six criteria is a verb–subject–outcome test checkable by scanning §6, none requiring a single named option.

**Criterion 2: Challenge Assumptions**
Quoted span: "| The 2005–2015 NSRDB record (11 winters) contains the worst winter sequence to design for | untested belief | Verify, or flag as unverified | Challenge — 11 years is a short sample for a rare event … | unverified — flagged; a longer record (NSRDB 1998–present) would test it |" and the Assumption Audit row "| C7 | 5 | simulate at actual site | A-20 two cells span the range | yes |"
Band: **Rigorous**
Justification: All 20 rows use the four types with matching treatments and em-dash verdicts, several are challenged, every unverified row used in a chain reads "unverified — flagged", and the audit scan covers every hop and added A-15 to A-20.

**Criterion 3: Establish Ground Truths**
Quoted span: comparison — enumeration "GT-5, GT-6, GT-7, GT-8, GT-9 (5 of 11)"; the list carries `?` on exactly GT-5?, GT-6?, GT-7?, GT-8?, GT-9?. Unsuffixed GT-1, GT-2, GT-3, GT-10 and GT-11 each feed a HIGH chain (C2, C3 or C7) and name read locations. "**GT-4** … read-at-source: definition of gravitational potential energy and of the kilowatt-hour" feeds only C1, which is MEDIUM.
Band: **Sound**
Justification: Enumeration and suffixes agree and read locations are named, but one unsuffixed ground truth with a reachable source (GT-4) feeds only a MEDIUM chain, which is the single-instance Sound case.

**Criterion 4: Reason Upward**
Quoted span: scan row "| C4 | GT-3 + GT-7? + GT-9? + C2 + C3 | unreached | same two rules unreached at hops 3–7 (text scan clean) | yes | MEDIUM | yes | none |" and §5 "**Why abandoned:** It contradicts GT-3 and GT-10. GT-1's 14% loss is a grid-tied figure and leaves out battery round-trip loss …"
Band: **Rigorous**
Justification: Every chain has a parsing head and multi-hop intermediates, is dependency-clean, carries `[Assumes: A-N]` on hops introducing table assumptions, and recomputes in the adversarial pass. Seven dead ends use the three-part structure with specific GT-based reasons, and no analogy is used as evidence. The `unreached` cells disclose positions beyond the mechanical check, which a text scan found clean.

**Criterion 5: Validate**
Quoted span: "**Confidence:** MEDIUM — the Inputs axis is short. GT-7? (whether a real LFP bank delivers 90% of nameplate in winter) is removed by the chosen battery's datasheet and a capacity test. GT-9? … is removed by opening the NSRDB hourly data and quality flags for September 2012" and the adversarial record's "**K2 Site differs from the modelled cell** (causes 5, 7, 9) — bears on C7, C8, GT-11, A-3, A-20. Triage: fatal to the sizing as bought."
Band: **Rigorous**
Justification: Each chain names its weakest link. Every MEDIUM line names its `?` inputs or cited sub-HIGH chains with verification paths, and prices its `[Assumes]` premises. No `?`-fed chain is HIGH, and the Conclusion's MEDIUM equals its weakest contributing chain. The record carries Recompute, Sensitivity, Rival, a past-tense Premise, a 13-item cause list from four viewpoints, five cited clusters each with a disposition, and Falsification. No exception clause is claimed.

**Criterion 6: Conclusion-to-Ground-Truth Traceability**
Quoted span: scan rows "| Recommended approach: measure load, size per kWh/day … | bold lead-in | yes | … | C6, C4, C5, C7, C8 |" through "| Confidence: MEDIUM … | bold lead-in | yes | … | C1, C4, C5, C6, C8, C7 |", and §6 "**Key insight:** The usual \"load ÷ worst-month yield\" rule gives only a floor of 1.46–1.63 kWp. The run of cloudy winter days sets the real size, so PV and storage trade against each other as a pair"
Band: **Rigorous**
Justification: All five §6 claims cite chains inline, and none introduces reasoning absent from §4. The Key Insight states a finding the convention misses (floor-not-size, PV and storage as a pair, the site effect) rather than restating the recommended approach.

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
      "type": "untested belief",
      "verdict": "Challenge"
    },
    {
      "id": "A-4",
      "type": "untested belief",
      "verdict": "Challenge"
    },
    {
      "id": "A-5",
      "type": "convention",
      "verdict": "Challenge"
    },
    {
      "id": "A-6",
      "type": "convention",
      "verdict": "Accept"
    },
    {
      "id": "A-7",
      "type": "untested belief",
      "verdict": "Accept"
    },
    {
      "id": "A-8",
      "type": "current constraint",
      "verdict": "Accept"
    },
    {
      "id": "A-9",
      "type": "untested belief",
      "verdict": "Accept"
    },
    {
      "id": "A-10",
      "type": "physical law",
      "verdict": "Accept"
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
    },
    {
      "id": "A-14",
      "type": "untested belief",
      "verdict": "Accept"
    },
    {
      "id": "A-15",
      "type": "untested belief",
      "verdict": "Accept"
    },
    {
      "id": "A-16",
      "type": "untested belief",
      "verdict": "Accept"
    },
    {
      "id": "A-17",
      "type": "untested belief",
      "verdict": "Challenge"
    },
    {
      "id": "A-18",
      "type": "untested belief",
      "verdict": "Accept"
    },
    {
      "id": "A-19",
      "type": "untested belief",
      "verdict": "Challenge"
    },
    {
      "id": "A-20",
      "type": "untested belief",
      "verdict": "Accept"
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
      "read_at_source": true
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
    },
    {
      "id": "GT-11",
      "read_at_source": true
    }
  ],
  "chains": [
    {
      "id": "C1",
      "confidence": "MEDIUM",
      "rests_on": [
        "GT-4",
        "GT-5?",
        "GT-6?",
        "GT-10"
      ]
    },
    {
      "id": "C2",
      "confidence": "HIGH",
      "rests_on": [
        "GT-1",
        "GT-2",
        "GT-10",
        "GT-3"
      ]
    },
    {
      "id": "C3",
      "confidence": "HIGH",
      "rests_on": [
        "GT-3",
        "GT-2"
      ]
    },
    {
      "id": "C4",
      "confidence": "MEDIUM",
      "rests_on": [
        "GT-3",
        "GT-7?",
        "GT-9?",
        "C2",
        "C3"
      ]
    },
    {
      "id": "C5",
      "confidence": "MEDIUM",
      "rests_on": [
        "C4",
        "GT-3",
        "GT-8?",
        "GT-1"
      ]
    },
    {
      "id": "C6",
      "confidence": "MEDIUM",
      "rests_on": [
        "C1",
        "C5",
        "GT-1",
        "GT-10",
        "GT-3"
      ]
    },
    {
      "id": "C7",
      "confidence": "HIGH",
      "rests_on": [
        "GT-11",
        "GT-3"
      ]
    },
    {
      "id": "C8",
      "confidence": "MEDIUM",
      "rests_on": [
        "C7",
        "GT-11",
        "C4"
      ]
    }
  ],
  "dead_ends": [
    "Monthly-balance sizing on grid-tied yield",
    "A separate inverter-efficiency division on top of PVGIS",
    "Days-of-autonomy as the sizing rule",
    "Sizing up to remove the September–October residual",
    "Option A (more battery, less PV) as the recommendation",
    "Composite C as the general recommendation",
    "Tilting at the 34° annual optimum"
  ],
  "techniques": {
    "applied": [
      "inversion",
      "five-whys",
      "estimate",
      "trade-off",
      "second-order",
      "pre-mortem"
    ],
    "not_applied": [
      {
        "technique": "theoretical-limit",
        "phase": 1,
        "reason": "Phase 1: the essence is sizing a system to a load, and no current figure is in question as convention versus hard bound"
      },
      {
        "technique": "theoretical-limit",
        "phase": 4,
        "reason": "Phase 4: no conclusion needs a law-permitted ceiling; the binding quantity is the weather sequence, not a physical limit"
      },
      {
        "technique": "fishbone",
        "phase": 2,
        "reason": "Phase 2: no multi-causal effect needed category brainstorming, and the assumption space was enumerated by inverting the reliability claim"
      }
    ]
  },
  "gate": {
    "passes": [
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
    "fix_repeat_fired": false,
    "cleared": true
  },
  "re_entry": {
    "fired": false,
    "edges": []
  },
  "conclusion": {
    "recommendation": "Measure or list the load first. Then size to it at 0.502 kWp of south-facing PV at a 50° tilt and 3.35 kWh of nominal LiFePO4 storage per kWh/day of appliance load plus inverter standby (chain C6). For the central estimate of 5.07 kWh/day, that is a 2.7 kWp array and an 18 kWh bank (16.2 kWh usable). At the Albuquerque cell, an hour-by-hour simulation of 2005–2015 shows that bank empty on 3 days in 11 years outside the suspect September–October records (chains C4, C5). The load bracket of 3.47–7.59 kWh/day maps to 1.74 kWp + 11.6 kWh up to 3.81 kWp + 25.4 kWh (chain C6). Re-run the same simulation at the cabin's exact coordinates before buying (chain C7), and if that simulation looks like the eastern-plains cell, add a 2 kW generator for about 2 days a year, because no tested PV-plus-battery size meets the criterion there (chain C8).",
    "confidence": "MEDIUM"
  }
}
```
