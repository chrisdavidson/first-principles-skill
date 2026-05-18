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
| Energy conservation: energy out equals energy in divided by system efficiency | physical law | Accept as ground-truth candidate; promote to GT | Accept | Conservation of energy — physics; no verification needed |
| A panel array's daily output equals rated wattage × Peak Sun Hours × system derating factor | physical law | Accept as ground-truth candidate; promote to GT | Accept | Derived directly from energy conservation and the definition of PSH |
| Annual-average Peak Sun Hours at this site are approximately 5.5 h/day | convention | Challenge before use: PSH is site-specific; verify against NREL PVWatts data for the coordinates; treat as illustrative | Accept | Source: NREL solar radiation maps (illustrative; verifiable via PVWatts for 35° N high-desert NM) |
| A system derating factor of 0.80 accounts for all losses in the energy path from panels to delivered load (temperature, wiring, MPPT, inverter, and battery charge/discharge round-trip) | convention | Challenge before use: 0.80 is a conservative design-practice figure; verify against site-specific equipment specs; confirm the factor bundles battery round-trip loss since this is a battery-mediated off-grid system | Accept | Standard conservative design-practice value for off-grid systems; source: NREL and NABCEP off-grid design guidelines; LiFePO4 round-trip efficiency (~92–95%) is reflected in the conservative 0.80 factor alongside wiring (~5%), MPPT (~3%), and inverter (~4%) losses |
| LiFePO4 batteries can be discharged to 80% depth-of-discharge (DoD) safely | physical law | Accept as ground-truth candidate; promote to GT | Accept | Battery chemistry fact; source: manufacturer specifications and electrochemical design literature |
| 3 days of autonomy is the correct design target | current constraint | Record expiry condition: if occupants can accept load-shedding in multi-day overcast periods, fewer days of autonomy are acceptable; if the site has more severe winter weather, more days may be needed | Accept | Current design decision; expiry: site-specific weather analysis or owner preference change |
| The daily energy load is approximately 1.5 kWh/day | untested belief | Flag as unverified; may be used in chains but must carry GT-5? notation; any conclusion depending on it inherits MEDIUM confidence and a stated verification path | Accept | unverified — flagged |
| Sizing the battery to sustain peak instantaneous load continuously is the correct approach | untested belief | Challenge: peak load (250 W from the water pump) runs only 30 min/day; sizing for continuous 250 W is not the correct method for battery/panel capacity | Discard | Ruled out — see Abandoned Reasoning, Section 5 |

---

## 3. Ground Truths

- **GT-1** Peak Sun Hours at the site: approximately 5.5 PSH (annual average daily
  equivalent hours of full 1,000 W/m² irradiance at 35° N high-desert New Mexico) —
  source: NREL solar radiation maps; illustrative figure verifiable via NREL PVWatts
  for the specific site coordinates.

- **GT-2** System derating factor: 0.80 — accounts for all losses in the energy path
  from panels to delivered load in a well-designed off-grid system: temperature losses
  (~8%), wiring losses (~5%), MPPT controller efficiency (~3%), inverter efficiency (~4%),
  and battery charge/discharge round-trip efficiency for LiFePO4 (~5–8% loss, i.e., ~92–95%
  round-trip efficiency). Combined, these losses are consistent with a 0.80 conservative
  derating factor. Because this is a battery-mediated off-grid system — essentially all
  generated energy passes through the battery before reaching the load — battery round-trip
  loss is a real, non-negligible term in the energy path and is explicitly included here —
  source: NREL and NABCEP off-grid design guidelines; LiFePO4 round-trip efficiency from
  manufacturer specifications and electrochemical battery design literature.

- **GT-3** LiFePO4 battery safe depth-of-discharge: 80% DoD — this chemistry can
  deliver 80% of rated capacity without significant cycle-life degradation — source:
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
  1.8 kWh/day, the sizing outputs below must be revised upward.

---

## 4. Derivation Chains

### Conclusion: A 400 W panel array is required to meet the estimated daily load

GT-2 (0.80 derating factor — covers temperature, wiring, MPPT, inverter, and battery
round-trip losses; see GT-2 for the full enumerated loss list) + GT-5? (1.5 kWh/day
estimated load) + GT-1 (5.5 PSH)
→ Required gross daily panel output = 1.5 kWh ÷ 0.80 = 1,875 Wh/day
  (Neither GT-2 nor GT-5? alone specifies how many watt-hours the panels must generate;
  combining them via the energy-conservation relationship yields the gross generation target.
  The 0.80 factor is the complete loss model — it accounts for every loss between panel
  output and delivered load, including battery round-trip loss, so no further derating is
  needed for battery inefficiency.)
→ GT-1 (5.5 PSH annual average) applied to 1,875 Wh/day: panel capacity = 1,875 Wh ÷ 5.5 PSH ≈ 341 W
→ Recommendation: 400 W array (e.g., 2 × 200 W panels), providing a 17% margin above
  the minimum 341 W to buffer winter PSH variability (winter minimum ~4.5 PSH at this
  site would require ~417 W; the 400 W array is slightly undersized for worst-case winter
  but acceptable given the conservative derating and the option to reduce non-essential
  loads during extended low-sun periods).

**Confidence: MEDIUM** — GT-5? (daily energy load estimate of 1.5 kWh/day) is unverified.
If measured load consistently exceeds 1.8 kWh/day, the required panel capacity exceeds
400 W and the array must be upsized (e.g., to 3 × 200 W = 600 W). Verification: install
energy monitor for 30 days; confirm measured load before finalizing the array specification.

---

### Conclusion: A 6 kWh LiFePO4 battery bank is required for 3 days of autonomy

GT-5? (1.5 kWh/day estimated load) + GT-4 (3 days of autonomy)
→ Total usable energy to store = 1.5 kWh/day × 3 days = 4.5 kWh of usable capacity
  (Neither GT-5? nor GT-4 alone specifies how much energy the bank must deliver;
  combining them yields the usable-capacity requirement.)
→ GT-3 (80% DoD): required rated battery capacity = 4.5 kWh ÷ 0.80 = 5.625 kWh
→ Recommendation: 6 kWh LiFePO4 bank (practical sizing rounds up to the next available
  configuration above 5.625 kWh; a 6 kWh bank satisfies the requirement with a small margin).

**Confidence: MEDIUM** — GT-5? (daily energy load estimate of 1.5 kWh/day) is unverified.
If measured load is significantly higher (e.g., 2.0 kWh/day), the required rated capacity
rises to 2.0 × 3 ÷ 0.80 = 7.5 kWh, and the 6 kWh bank is inadequate. Verification:
same 30-day energy monitoring period; if measured daily load exceeds 1.8 kWh/day
consistently, upsize the battery bank before installation.

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

**Recommended approach:** Install a 400 W panel array (2 × 200 W panels) and a 6 kWh
LiFePO4 battery bank. These sizes are derived from the site's 5.5 PSH annual average
(GT-1), the 0.80 system derating factor (GT-2), the 80% DoD limit of LiFePO4 chemistry
(GT-3), the 3-day autonomy target (GT-4), and the estimated 1.5 kWh/day daily load
(GT-5?). Commission a 30-day energy-monitoring period before finalizing the order; if
measured daily load consistently exceeds 1.8 kWh/day, upsize to a 600 W array and a
7.5–8 kWh battery bank.

**Key insight:** The binding sizing constraint is daily energy throughput (Wh/day), not
peak instantaneous power (W). The water pump's 250 W draw appears to dominate the load,
but because it runs only 30 minutes per day it contributes only 125 Wh to the daily
total — less than the refrigerator (540 Wh) or the laptop (390 Wh). A peak-power framing
produces a specification four times too large; an energy-throughput framing
produces the correct specification. The largest single uncertainty in the sizing outputs
is not the physics (PSH, derating factor, and DoD are well-characterized) but the load
estimate: occupant behavior and seasonal variation can shift the daily load by 30–50%
without any change in the appliance list.

**Trade-offs acknowledged:** The 400 W array is slightly undersized for worst-case winter
PSH (~4.5 h vs 5.5 h annual average), which means multi-day low-sun periods in winter may
require reducing non-essential loads or accepting partial battery state-of-charge going
into night. The 3-day autonomy target is a design decision, not a physical minimum; a
2-day target would reduce battery cost by roughly 33% at the cost of greater sensitivity
to consecutive overcast days. Both trade-offs are resolvable with confirmed load
measurement and site-specific weather data.

**Confidence: MEDIUM** — Both sizing chains depend on GT-5? (the estimated 1.5 kWh/day
daily load), which is unverified. GT-1 through GT-4 are well-established and do not
introduce material uncertainty; the load estimate is the only weak link. A 30-day
energy-monitoring period measuring actual consumption would verify or correct GT-5? and
raise confidence in both sizing outputs to HIGH.
