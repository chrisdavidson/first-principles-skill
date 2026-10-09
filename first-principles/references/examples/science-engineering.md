<!-- GENERATED — DO NOT EDIT. Source: shared/examples/science-engineering.md. Regenerate via: scripts/sync-content.py --write. -->

# Worked Example: Science and Engineering

A complete first-principles analysis of a science and engineering sizing question,
following the standardized output format with quantitative derivation chains anchored in
physical law and a genuine unverified input (GT-5?). Authored in Phase 5.

---

## 1. Problem Essence

**Core problem:** Given a fixed site (high-desert New Mexico, 35° N, year-round occupancy
by 2 adults, no grid connection), what panel array capacity and battery bank capacity are
required to meet the cabin's daily electrical load reliably?

**Success criteria:**

- A panel array size (watts of rated capacity) is derived from the site's solar resource
  and the estimated daily load — not guessed from a rule of thumb.
- A battery bank size (kilowatt-hours of rated capacity) is derived from the desired
  days-of-autonomy, the battery chemistry's depth-of-discharge limit, and the estimated
  daily load.
- Every sizing number traces to a named ground truth or a derivation chain — no number
  is introduced without an antecedent.
- Uncertainty in the daily load estimate is explicitly propagated to the sizing outputs;
  the analysis does not present a confident number where the input is unverified.

---

## 2. Assumptions Table

| Assumption | Type | Treatment | Verdict | Verification |
|------------|------|-----------|---------|--------------|
| Energy conservation: energy out equals energy in divided by system efficiency | physical law | Accept as ground-truth candidate; promote to GT | Accept — conservation of energy; a physical law requiring no verification | Conservation of energy — physics; no verification needed |
| A panel array's daily output equals rated wattage × Peak Sun Hours × system derating factor | physical law | Accept as ground-truth candidate; promote to GT | Accept — derived directly from energy conservation and the PSH definition | Derived directly from energy conservation and the definition of PSH |
| Annual-average Peak Sun Hours at this site are approximately 5.5 h/day | convention | Challenge before use: PSH is site-specific; verify against NREL PVWatts data for the coordinates; treat as illustrative | Accept — NREL solar radiation maps; illustrative, verifiable via PVWatts for this site | Source: NREL solar radiation maps (illustrative; verifiable via PVWatts for 35° N high-desert NM) |
| A system derating factor of 0.80 accounts for all losses in the energy path from panels to delivered load (temperature, wiring, MPPT, inverter, and battery charge/discharge round-trip) | convention | Challenge before use: 0.80 is a conservative design-practice figure; verify against site-specific equipment specs; confirm the factor bundles battery round-trip loss since this is a battery-mediated off-grid system | Accept — standard NREL/NABCEP off-grid design value; bundles LiFePO4 round-trip loss with wiring/MPPT/inverter losses | 0.80 is the independently-sourced design-practice value (source: NREL and NABCEP off-grid design guidelines), not a figure derived from the enumerated losses; those losses (temperature, wiring, MPPT, inverter, LiFePO4 round-trip) compound to approximately 0.75–0.77, slightly below 0.80 — see GT-2 |
| LiFePO4 batteries can be discharged to 80% depth-of-discharge (DoD) safely | convention | Challenge before use: 80% is a manufacturer convention trading usable capacity against cycle life, not a physical limit; confirm against the selected cell's datasheet cycle-life curve; promote to GT as a stated convention | Accept — manufacturer convention trading usable capacity against cycle life, per manufacturer and electrochemical design literature | Manufacturer convention (usable capacity versus cycle life), not a physical law; source: manufacturer specifications and electrochemical design literature |
| 3 days of autonomy is the correct design target | current constraint | Record expiry condition: if occupants can accept load-shedding in multi-day overcast periods, fewer days of autonomy are acceptable; if the site has more severe winter weather, more days may be needed | Accept — current design decision; expires on site-specific weather analysis or owner preference change | Current design decision; expiry: site-specific weather analysis or owner preference change |
| The daily energy load is approximately 1.5 kWh/day | untested belief | Flag as unverified; may be used in chains but must carry GT-5? notation; any conclusion depending on it inherits MEDIUM confidence and a stated verification path | Accept — unverified; flagged and carried as GT-5? through the derivation chains | unverified — flagged |
| Sizing the battery to sustain peak instantaneous load continuously is the correct approach | untested belief | Challenge: peak load (250 W from the water pump) runs only 30 min/day; sizing for continuous 250 W is not the correct method for battery/panel capacity | Discard — ruled out; see Abandoned Reasoning, Section 5 | Ruled out — see Abandoned Reasoning, Section 5 |
| The battery bank can be charged, and delivers its rated capacity, at the cabin's winter night temperatures (high-desert nights fall below 0 °C) | untested belief | Flag as unverified: LiFePO4 charged below 0 °C risks lithium plating, so a BMS blocks the charge or the pack needs a heater, and capacity also drops in the cold; require a heated or temperature-buffered bank location, or a heater with a low-temperature charge cutoff | Challenge — unverified; carried as a caveat on C2, discharged by heated or buffered siting or a heater with a low-temperature charge cutoff | Verify the selected pack's datasheet low-temperature charge and discharge limits and the bank location's winter minimum temperature before purchase |

---

## 3. Ground Truths

- **GT-1?** Peak Sun Hours at the site: approximately 5.5 PSH (annual average daily
  equivalent hours of full 1,000 W/m² irradiance at 35° N high-desert New Mexico) and
  approximately 4.5 PSH in the winter minimum, the design month for a year-round cabin —
  source: NREL solar radiation maps; illustrative figure verifiable via NREL PVWatts
  for the specific site coordinates. **Unverified in this analysis:** the figure is
  illustrative, not read for this site, so the entry carries the `?`; a PVWatts run at
  the site coordinates, quoted, would remove it.

- **GT-2** System derating factor: 0.80 — accounts for all losses in the energy path
  from panels to delivered load in a well-designed off-grid system: temperature losses
  (~8%), wiring losses (~5%), MPPT controller efficiency (~3%), inverter efficiency (~4%),
  and battery charge/discharge round-trip efficiency for LiFePO4 (~5–8% loss, i.e., ~92–95%
  round-trip efficiency). Combined, these losses compound to a retained fraction of
  0.92 × 0.95 × 0.97 × 0.96 × (0.92 to 0.95) ≈ 0.749 to 0.773 — slightly below the 0.80
  conservative derating factor used throughout this analysis, so 0.80 is modestly optimistic
  (by roughly 3–5 percentage points) relative to this enumerated list. 0.80 is retained here on
  its independent basis (NREL and NABCEP conservative off-grid design practice, cited below),
  not as a figure derived from the list above. Because this is a battery-mediated off-grid system — essentially all
  generated energy passes through the battery before reaching the load — battery round-trip
  loss is a real, non-negligible term in the energy path and is explicitly included here —
  source: NREL and NABCEP off-grid design guidelines; LiFePO4 round-trip efficiency from
  manufacturer specifications and electrochemical battery design literature.

- **GT-3** LiFePO4 battery safe depth-of-discharge: 80% DoD — this chemistry can
  deliver 80% of rated capacity without significant cycle-life degradation (a manufacturer convention trading usable capacity against cycle life, not a physical limit) — source:
  LiFePO4 manufacturer specifications and electrochemical battery design literature.

- **GT-4** Desired days of autonomy: 3 days — covers the longest typical consecutive
  overcast period for this climate zone (winter storm scenarios in high-desert NM
  rarely exceed 2 consecutive heavily overcast days; 3 days provides margin) —
  source: current design constraint and occupant decision; expiry: revision based on
  site weather data or occupant risk tolerance.

- **GT-5?** Daily energy load estimate: approximately 1.5 kWh/day — unverified:
  this figure is derived from the per-appliance load breakdown below, which depends
  on occupant behavior (actual hours of use), seasonal variation (lighting hours
  increase in winter, refrigerator duty cycle varies with ambient temperature), and
  the actual level of "occasional AC loads" which could range from near-zero to
  several hundred Wh/day. The 1.5 kWh/day figure cannot be verified without an
  energy-monitoring period or on-site metered measurement over at least one
  representative month.

  Per-appliance load breakdown (basis for GT-5?):

  | Appliance | Power (W) | Hours/day | Daily energy (Wh) |
  |-----------|-----------|-----------|-------------------|
  | LED lighting (6 fixtures × 10 W) | 60 W total | 4 h | 240 Wh |
  | 12 V DC refrigerator (45 W × 50% duty cycle) | 22.5 W avg | 24 h | 540 Wh |
  | Laptop | 65 W | 6 h | 390 Wh |
  | Water pump | 250 W | 0.5 h | 125 Wh |
  | AC inverter loads (occasional) | 100 W avg | 2 h | 200 Wh |
  | **Estimated total daily load** | | | **~1,495 Wh ≈ 1.5 kWh/day** |

  Verification path: install a revenue-grade energy monitor for at least 30 days
  spanning a season with high load variation. If measured load consistently exceeds
  1.6 kWh/day (6 kWh rated bank × 0.80 DoD ÷ 3 days autonomy = 1.6 kWh/day, the load at
  which the recommended battery bank stops meeting the 3-day autonomy target, and the
  binding constraint since it is reached before the panel array's own winter limit of
  600 W × 4.5 PSH × 0.75 = 2.03 kWh/day), the sizing outputs below must be revised upward.

```text
?-marked: GT-1?, GT-5? (2 of 5)
Read-at-source: GT-2 — NREL and NABCEP off-grid design guidelines for the 0.80 factor; LiFePO4 round-trip efficiency from manufacturer specifications
Read-at-source: GT-4 — current design constraint and occupant decision (a decision, not a measurement)
```

---

## 4. Derivation Chains

### Conclusion C1: A panel array of 417–444 W minimum, 600 W recommended, is required to meet the estimated daily load in the winter design month

GT-2 (0.80 derating factor — covers temperature, wiring, MPPT, inverter, and battery round-trip losses; see GT-2 for the full enumerated loss list) + GT-5? (1.5 kWh/day estimated load) + GT-1? (4.5 PSH winter minimum, the design basis for a year-round cabin; 5.5 PSH annual average kept as a cross-check)
→ Required gross daily panel output = 1.5 kWh ÷ 0.80 = 1,875 Wh/day (Neither GT-2 nor GT-5? alone specifies how many watt-hours the panels must generate; combining them via the energy-conservation relationship yields the gross generation target. The 0.80 factor is the complete loss model — it accounts for every loss between panel output and delivered load, including battery round-trip loss, so no further derating is needed for battery inefficiency.)
→ Applying GT-1? at the winter design basis (4.5 PSH) to 1,875 Wh/day yields panel capacity = 1,875 Wh ÷ 4.5 PSH ≈ 417 W; at the enumerated 0.75 loss factor (GT-2 is optimistic by roughly 3–5 percentage points against its own loss list), 1,500 Wh ÷ (4.5 × 0.75) ≈ 444 W. Cross-check on the annual average: 1,875 Wh ÷ 5.5 PSH ≈ 341 W, but a 400 W array sized to that basis delivers only 400 × 4.5 × 0.80 = 1,440 Wh/day in winter (1,350 Wh/day at 0.75), below the 1,500 Wh/day load, so the annual-average figure is not the design basis for a year-round cabin
→ Recommendation: 600 W array (3 × 200 W panels), about 44% above the 417 W minimum and 35% above the 444 W figure. Winter output is 600 × 4.5 × 0.80 = 2,160 Wh/day (2,025 Wh/day at 0.75) against the 1,500 Wh/day load, so the margin carries both the derate uncertainty and some load growth without relying on load shedding.

**Pre-check:** head GT-2, GT-5?, GT-1? · ?-marked: GT-5?, GT-1? · lowest cited: none · Inputs ceiling: MEDIUM
**Confidence: MEDIUM** — GT-5? (daily energy load estimate of 1.5 kWh/day) is unverified,
and so is GT-1? (5.5 PSH), an illustrative map figure not yet read for this site: a PVWatts
run at the site coordinates would remove it, and a lower figure raises the array in proportion.
If measured load consistently exceeds 2.03 kWh/day (600 W × 4.5 PSH × 0.75 = 2,025 Wh/day;
2.16 kWh/day at 0.80), the required panel capacity exceeds 600 W and the array must be
upsized (e.g., to 4 × 200 W = 800 W). Verification: install energy monitor for 30 days; confirm
measured load before finalizing the array specification.

---

### Conclusion C2: A 6 kWh LiFePO4 battery bank is required for 3 days of autonomy

GT-5? (1.5 kWh/day estimated load) + GT-4 (3 days of autonomy)
→ Total usable energy to store = 1.5 kWh/day × 3 days = 4.5 kWh of usable capacity (Neither GT-5? nor GT-4 alone specifies how much energy the bank must deliver; combining them yields the usable-capacity requirement.)
→ Applying GT-3 (80% DoD) yields required rated battery capacity = 4.5 kWh ÷ 0.80 = 5.625 kWh
→ Recommendation: 6 kWh LiFePO4 bank (practical sizing rounds up to the next available configuration above 5.625 kWh; a 6 kWh bank satisfies the requirement with a small margin).
→ Caveat (A-9): this capacity holds only if the bank is not charged below 0 °C and is not cold-derated. LiFePO4 charged below freezing risks lithium plating (a BMS will block the charge, or the pack needs a heater), and capacity also drops in the cold. The bank must sit in a heated or temperature-buffered space, or have a heater plus a low-temperature charge cutoff; otherwise effective autonomy shrinks in the design season (winter).

**Pre-check:** head GT-5?, GT-4 · ?-marked: GT-5? · lowest cited: none · Inputs ceiling: MEDIUM
**Confidence: MEDIUM** — GT-5? (daily energy load estimate of 1.5 kWh/day) is unverified.
If measured load is significantly higher (e.g., 2.0 kWh/day), the required rated capacity
rises to 2.0 × 3 ÷ 0.80 = 7.5 kWh, and the 6 kWh bank is inadequate. Verification:
same 30-day energy monitoring period; if measured daily load exceeds 1.6 kWh/day
(6 kWh × 0.80 ÷ 3 days = 1.6 kWh/day) consistently, upsize the battery bank before
installation. The bank's winter temperature caveat (A-9) is a second condition on this
band: if the bank cannot be kept above 0 °C for charging, effective autonomy in winter is
below the 3-day target regardless of the load measurement.

---

## 5. Abandoned Reasoning

### Dead End: Size the system to the peak instantaneous load

**What was tried:** Identify the highest-wattage appliance (the water pump at 250 W) and
use that as the primary sizing constraint — build a panel array and battery bank capable
of sustaining 250 W of continuous output.

**Why abandoned:** The assumption "size battery and panel capacity to sustain the peak
load continuously" was discarded in Phase 2 (Verdict: Discard) because peak instantaneous
power is not the correct sizing variable for daily energy storage and generation. The
water pump runs for only 30 minutes per day; sizing the system to sustain 250 W
continuously would require roughly 250 W × 24 h = 6 kWh/day of panel output — exactly
four times the actual 1.5 kWh/day load (6 ÷ 1.5 = 4.0) — producing a massively overbuilt installation.
The correct sizing variable is daily energy throughput in watt-hours: how much total
energy the system must store and deliver each day. Peak instantaneous power (watts) is the
correct variable only for inverter sizing and wire gauge selection, not for panel array
capacity or battery bank capacity.

**What it ruled out:** Using peak load as the primary sizing metric for battery storage
and panel capacity. This path is not merely suboptimal — it produces a specification that
is structurally wrong for the problem, confusing an instantaneous power demand with an
energy throughput requirement.

---

## 6. Conclusion

**Recommended approach:** (chains C1 and C2) Install a 600 W panel array (3 × 200 W panels) and a 6 kWh
LiFePO4 battery bank. These sizes are derived from the site's 4.5 PSH winter minimum, the
design month (GT-1?), the 0.80 system derating factor (GT-2), the 80% DoD convention for LiFePO4
(GT-3), the 3-day autonomy target (GT-4), and the estimated 1.5 kWh/day daily load
(GT-5?). Site the bank in a heated or temperature-buffered space, or fit a heater with a
low-temperature charge cutoff, so it is never charged below 0 °C. Commission a 30-day
energy-monitoring period before finalizing the order; above
approximately 1.6 kWh/day (6 kWh × 0.80 DoD ÷ 3 days) the 6 kWh bank no longer meets the
3-day autonomy target and should be upsized to 7.5–8 kWh, and above approximately
2.03 kWh/day (600 W × 4.5 PSH × 0.75) the 600 W array no longer meets the winter daily load and
should be upsized to 800 W.

**Key insight:** (chains C1 and C2) The binding sizing constraint is daily energy throughput (Wh/day), not
peak instantaneous power (W). The water pump's 250 W draw appears to dominate the load,
but because it runs only 30 minutes per day it contributes only 125 Wh to the daily
total — less than the refrigerator (540 Wh) or the laptop (390 Wh). A peak-power framing
produces a specification four times too large; an energy-throughput framing
produces the correct specification. The largest single uncertainty in the sizing outputs
is not the physics (PSH, derating factor, and DoD are well-characterized) but the load
estimate: occupant behavior and seasonal variation can shift the daily load by 30–50%
without any change in the appliance list.

**Trade-offs acknowledged:** (chains C1 and C2) The 600 W array is sized on the winter design
month (~4.5 PSH), not the 5.5 h annual average, so in summer it produces well above the
load (600 × 5.5 × 0.80 = 2,640 Wh/day against 1,500 Wh/day); the cost is roughly 200 W of
panels beyond the 400 W that annual-average sizing suggests, in exchange for not relying on
load shedding in winter. Multi-day low-sun periods in winter still draw on the battery
autonomy. The 3-day autonomy target is a design decision, not a physical minimum; a
2-day target would reduce battery cost by roughly 33% at the cost of greater sensitivity
to consecutive overcast days. The bank's rated capacity also assumes it is kept above
0 °C for charging (A-9); an unheated location would shrink effective winter autonomy.
These trade-offs are resolvable with confirmed load measurement, site-specific weather
data and a decision on where the bank is sited.

**Pre-check:** head C1 (MEDIUM), C2 (MEDIUM) · ?-marked: none · lowest cited: MEDIUM · Inputs ceiling: MEDIUM
**Confidence: MEDIUM** — Both sizing chains depend on GT-5? (the estimated 1.5 kWh/day
daily load), which is unverified. The panel chain C1 also rests on GT-1? (5.5 PSH), an
illustrative map figure not yet read for this site; a PVWatts run at the site coordinates
would settle it, and a lower figure raises the required array in proportion. GT-3 and
GT-4 are well-established and do not introduce material uncertainty. GT-2's 0.80 derate is well-established on its own
independent basis, but it is optimistic by roughly 3–5 percentage points against the
enumerated loss list (which compounds to 0.749–0.773) — a second, bounded uncertainty
that the 600 W winter-design array absorbs (at 0.75 it still delivers 2,025 Wh/day against
the 1,500 Wh/day load). The unverified load estimate
remains the larger weak link of the two. A 30-day energy-monitoring period measuring
actual consumption would verify or correct GT-5?, and confirming the site-specific
equipment efficiencies against the installed hardware would close GT-2's 3–5 pp gap;
those two together with the site PVWatts reading for GT-1? would raise confidence in the
sizing outputs to HIGH. The battery chain C2 additionally carries the winter charging
caveat (A-9): the bank must be kept above 0 °C for charging, or autonomy shrinks.

---

## Appendix — process output

## Structured summary (process output)

```json
{
  "schema_version": 1,
  "run_mode": null,
  "assumptions": [
    {
      "id": "A-1",
      "type": "physical law",
      "verdict": "Accept"
    },
    {
      "id": "A-2",
      "type": "physical law",
      "verdict": "Accept"
    },
    {
      "id": "A-3",
      "type": "convention",
      "verdict": "Accept"
    },
    {
      "id": "A-4",
      "type": "convention",
      "verdict": "Accept"
    },
    {
      "id": "A-5",
      "type": "convention",
      "verdict": "Accept"
    },
    {
      "id": "A-6",
      "type": "current constraint",
      "verdict": "Accept"
    },
    {
      "id": "A-7",
      "type": "untested belief",
      "verdict": "Accept"
    },
    {
      "id": "A-8",
      "type": "untested belief",
      "verdict": "Discard"
    },
    {
      "id": "A-9",
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
    }
  ],
  "chains": [
    {
      "id": "C1",
      "confidence": "MEDIUM",
      "rests_on": [
        "GT-2",
        "GT-5?",
        "GT-1?"
      ]
    },
    {
      "id": "C2",
      "confidence": "MEDIUM",
      "rests_on": [
        "GT-5?",
        "GT-4"
      ]
    }
  ],
  "dead_ends": [
    "Size the system to the peak instantaneous load"
  ],
  "techniques": null,
  "gate": null,
  "re_entry": null,
  "conclusion": {
    "recommendation": "(chains C1 and C2) Install a 600 W panel array (3 × 200 W panels) and a 6 kWh\nLiFePO4 battery bank. These sizes are derived from the site's 4.5 PSH winter minimum, the\ndesign month (GT-1?), the 0.80 system derating factor (GT-2), the 80% DoD convention for LiFePO4\n(GT-3), the 3-day autonomy target (GT-4), and the estimated 1.5 kWh/day daily load\n(GT-5?). Site the bank in a heated or temperature-buffered space, or fit a heater with a\nlow-temperature charge cutoff, so it is never charged below 0 °C. Commission a 30-day\nenergy-monitoring period before finalizing the order; above\napproximately 1.6 kWh/day (6 kWh × 0.80 DoD ÷ 3 days) the 6 kWh bank no longer meets the\n3-day autonomy target and should be upsized to 7.5–8 kWh, and above approximately\n2.03 kWh/day (600 W × 4.5 PSH × 0.75) the 600 W array no longer meets the winter daily load and\nshould be upsized to 800 W.",
    "confidence": "MEDIUM",
    "rests_on": [
      "C1",
      "C2"
    ]
  }
}
```
