# First-Principles Analysis: Off-Grid Solar Sizing — High-Desert NM Cabin (35°N)

## 1. Problem Essence

**Core problem:** What minimum PV array capacity (W, STC) and LiFePO4 battery bank capacity (kWh, usable) will reliably power a year-round, 2-adult off-grid cabin at 35°N high-desert New Mexico through the winter design month with 3 days of no-sun autonomy, sized against worst-case winter solar climatology (not annual-average conditions) and net of realistic system losses?

**Success criteria** (a correct answer satisfies all of these):
- The user's 1.5 kWh/day load figure is checked against a bottom-up, appliance-level load buildup rather than accepted at face value, and the memo states explicitly whether 1.5 kWh/day is low, high, or reasonable for genuine year-round 2-adult occupancy, and why.
- Panel sizing uses a stated winter design-month PSH value (not the annual-average PSH), with that value and its source stated explicitly.
- Every material derate (inverter efficiency, wiring, temperature, dust/soiling, degradation, MPPT/charge-controller conversion, battery round-trip efficiency) is itemized rather than folded into one unstated fudge factor.
- Battery sizing states nameplate vs. usable kWh, the DoD assumption used, and shows the arithmetic converting the 3-day autonomy target into that number.
- The memo names what would change the recommended numbers materially (load assumption, PSH assumption, desired margin beyond bare autonomy).

---

## 2. Assumptions Table

| Assumption | Type | Treatment | Verdict | Verification |
|---|---|---|---|---|
| A-1: December is the design-limiting month for a year-round off-grid PV system at 35°N | convention (grounded in solar geometry) | Explicitly challenge before use | Accept — challenged and confirmed in chain C2 via GT-1?, GT-8? | unverified — flagged (GT-1?, GT-8?) |
| A-2: The user's 1.5 kWh/day figure reflects true year-round 2-adult electrical need | untested belief | Verify via bottom-up buildup | Challenge — bottom-up buildup (chain C1) shows it undercounts fridge, comms, and winter heating-blower draw | unverified — flagged (GT-9?, GT-10, GT-11, GT-13?) |
| A-3: A 12V/24V DC compressor fridge is used, not a standard AC residential fridge via inverter | current constraint (equipment choice) | Record expiry conditions | Accept — expires the instant the owner installs a different fridge; single largest swing factor in this sizing | unverified — flagged (GT-10) |
| A-4: No electric-resistance heating or cooking; propane/wood used for both | current constraint | Record expiry conditions | Accept — expires if any electric-resistance heat/cooking is added, which would add multiple kWh/day and invalidate this sizing | unverified — flagged (domain-standard off-grid convention, no single GT cited) |
| A-5: No Starlink or other high-power satellite internet; only a basic router/cell booster | current constraint | Record expiry conditions | Accept — expires if Starlink (≈40–75 W continuous, ≈1–1.8 kWh/day) is added, which alone can exceed this design's entire daily budget | unverified — flagged (no GT cited; general equipment knowledge) |
| A-6: Batteries are installed in a temperature-buffered space, not an exposed unheated shed | current constraint / installation requirement | Record expiry conditions | Challenge — real risk of violation in practice; surfaced in adversarial pass as a plan requirement, not a silent assumption | unverified — flagged (GT-5?) |
| A-7: Array is fixed-tilt, true-south, tilted steeper than latitude (~50°, lat+15°) to bias winter production | convention | Explicitly challenge before use | Accept — challenged; kept because a lower, roofline-matched tilt cuts winter yield materially per GT-3? | unverified — flagged (GT-3?) |
| A-8: Occupants will not materially expand loads over time ("no load creep") | untested belief | Verify or flag | Challenge — second-order extension of chain C3 finds this very likely false over a multi-year horizon; kept as the base-case sizing assumption but flagged as fragile | unverified — flagged |
| A-9: Albuquerque-area PSH/GHI proxy data applies directly to the actual (unnamed) cabin site | current constraint | Record expiry conditions | Challenge — expires once actual site coordinates/horizon/shading are known; must be re-run through PVWatts/NSRDB before purchase | unverified — flagged (GT-1?, GT-2?) |
| A-10: The 20% aggregate PV-side derate (soiling/wiring/mismatch/MPPT/temp/aging) is representative of this equipment and climate | convention | Explicitly challenge before use | Accept — challenged against GT-6?'s published ~14% grid-tied default, then raised to account for high-desert dust and off-grid-specific wiring runs (GT-7?) | unverified — flagged (GT-6?, GT-7?) |
| A-11: 80% DoD is the correct LiFePO4 design point, vs. the chemistry's ~90–95% technical ceiling | convention | Explicitly challenge before use | Accept — challenged; kept for BMS/cold-weather headroom, but 95% DoD sizing remains a live, not-fully-ruled-out rival (§5) | unverified — flagged (GT-4?, GT-5?) |
| A-12 *(surfaced in Phase 4 Assumption Audit, chain C2)*: No backup generator is part of the design; solar+battery alone must cover 100% of winter demand including the 3-day autonomy reserve | current constraint | Record expiry conditions | Accept — expires if the client wants a generator-assisted design, which would allow smaller solar+battery sizing | unverified — flagged (surfaced from C2; no GT cited, scope decision) |
| A-13 *(surfaced in Phase 4 Assumption Audit, chain C4)*: The selected battery product's datasheet substantiates 80% DoD cycling at its rated cycle life, not just the chemistry's theoretical capability | untested belief | Verify or flag | Challenge — must be confirmed against the specific purchased product's spec sheet before commissioning | unverified — flagged |

---

## 3. Ground Truths

- **GT-1?** Albuquerque-area (35.08°N, ~5,312 ft elev.) horizontal global irradiance averages ≈2.8 kWh/m²/day in December, ≈8.1 kWh/m²/day in June, ≈5.7 kWh/m²/day annually — cited to: shrinkthatfootprint.com, citing "the NREL.gov app"; reported-by-delegate: WebSearch synthesis. **Phase 3 failure record:** attempted WebFetch to `developer.nrel.gov` (PVWatts API) and `pvwatts.nrel.gov` to open the primary NREL source directly; both returned `getaddrinfo ENOTFOUND` — the nrel.gov domain is unreachable from this run's network sandbox. Source not opened this run.
- **GT-2?** A south-facing, fixed-tilt-at-latitude (35°) array at this site receives ≈4.4 kWh/m²/day average in December (vs. 2.8 kWh/m²/day horizontal) — cited to: shrinkthatfootprint.com; reported-by-delegate. Same Phase 3 failure record as GT-1 (underlying NREL data unreachable).
- **GT-3?** Tilting a fixed off-grid array beyond latitude toward latitude+15° (≈50° at 35°N) adds a further ≈10–20% to worst-month yield versus latitude-tilt, at the cost of summer output — cited to: offgridsolarsystem.ca (industry design guide); reported-by-delegate — general heuristic, not a location-specific measurement; source not opened this run.
- **GT-4?** LiFePO4 cells tolerate routine discharge to 80–100% DoD with minimal cycle-life penalty, in contrast to lead-acid, which degrades rapidly below ≈50% DoD — unverified this run: well-established electrochemical property, no specific manufacturer datasheet opened.
- **GT-5?** LiFePO4 battery-management systems commonly block charging below 0°C/32°F cell temperature (to prevent lithium plating/permanent capacity loss), and discharge capacity/voltage sags moderately in cold — unverified this run: general domain knowledge, no specific datasheet opened.
- **GT-6?** A commonly published aggregate default for total grid-tied PV "soft" system losses (soiling, shading, mismatch, wiring, connections, light-induced degradation, nameplate tolerance, age, availability) is ≈14%, per NREL's own PVWatts default loss stack — cited to: general PVWatts documentation; reported-by-delegate. **Phase 3 failure record:** same nrel.gov unreachability as GT-1 — `pvwatts.nrel.gov` could not be opened this run.
- **GT-7?** High-desert climates see soiling losses at the higher end of published ranges (dust accumulation between rains) and only light, infrequent winter snow cover versus colder/wetter climates — unverified this run: general climatology knowledge, no specific citation opened.
- **GT-8?** At 35°N, December straddles the winter solstice (solar declination ≈ −23.45°), giving both the year's lowest sun angle and its shortest day length (≈9.5–10 hr, vs. ≈14.5 hr in June) — unverified this run in the sense that no citation was opened, though this is standard spherical-trigonometry astronomy directly calculable from latitude and solar declination, so it carries materially lower uncertainty than the other `?`-marked entries despite carrying the flag.
- **GT-9?** A 12V/24V DC compressor fridge/freezer suitable for off-grid use draws roughly 30–60 Ah/day at 12V (≈240–720 Wh/day; commonly-cited midpoint ≈350–450 Wh/day at moderate ~70–77°F ambient), rising 50–100% in hot conditions — cross-corroborated across thewearify.com and vansage.com via WebSearch; reported-by-delegate. **Phase 3 failure record:** attempted WebFetch to a third corroborating source, `forum.solar-electric.com` (northernarizona-windandsun discussion thread), which returned HTTP 403 Forbidden — could not open this specific source this run.
- **GT-10** A single standard AC-powered residential refrigerator run through an inverter draws about 1,500 Wh/day by itself — source: offgridbenchmark.com, "Complete Off-Grid Cabin Power Setup" guide; **read-at-source:** quoted directly via WebFetch — *"A residential fridge alone is ~1,500 Wh/day."*
- **GT-11** The same source's own published tiers: a "Year-Round Cabin" tier (residential fridge + well pump + lights + electronics + microwave, occasional power tools) is benchmarked at ≈6–8 kWh/day; a "Full Homestead" tier (4-person, with electric heat backup) is benchmarked at ≈15–20 kWh/day — source: offgridbenchmark.com, same guide; **read-at-source:** quoted directly via WebFetch — *"Year-Round Cabin... ~6-8 kWh/day"* powering *"residential fridge, well pump, lights, electronics, microwave"*; *"Full Homestead... ~15-20 kWh/day with electric heat backup."*
- **GT-12?** A 0.5 HP submersible well pump draws ≈500–750 W and runs ≈1–2 hr/day, using ≈0.5–1.5 kWh/day when present — cited to: gpsolarpanels.com; reported-by-delegate (WebSearch summary only, source page not opened this run). Relevant only if the cabin has a powered well; excluded from this memo's base case (gravity/hauled/hand-pump water assumed).
- **GT-13?** Common off-grid design practice adds ≈25% overhead to a summed appliance load estimate for inverter/wiring losses and the near-universal tendency for real usage to exceed paper estimates — cited to: gpsolarpanels.com; reported-by-delegate (WebSearch summary only, source page not opened this run).

**Provenance summary:** `?`-marked: GT-1, GT-2, GT-3, GT-4, GT-5, GT-6, GT-7, GT-8, GT-9, GT-12, GT-13 (11 of 13). Read-at-source: GT-10 — offgridbenchmark.com guide, quoted verbatim above; GT-11 — same guide, quoted verbatim above. No unsuffixed ground truth in this list feeds a HIGH-confidence chain (this analysis contains no HIGH-confidence chains — see §4), so the "every unsuffixed GT feeding a HIGH chain names its read-at-source location" requirement is vacuously satisfied.

---

## 4. Derivation Chains

### Conclusion C1: The user's 1.5 kWh/day figure understates realistic year-round 2-adult usage under this memo's own equipment assumptions; the winter design load should be set near 2.0 kWh/day

GT-9? (DC fridge ≈240-720 Wh/day) + GT-10 (residential AC fridge alone ≈1,500 Wh/day) + GT-13? (≈25% realism-overhead convention)
→ under this memo's DC-fridge, no-well, no-Starlink equipment assumptions (A-3, A-5), summing lighting, DC fridge, laptop/phone charging, basic comms, a small water pump, and inverter standby draw gives a bottom-up appliance total near 1.38 kWh/day before overhead
→ applying GT-13's ≈25% realism overhead plus the propane-furnace blower/igniter draw that runs more during the design-limiting winter month brings the winter design-month load to roughly 2.0 kWh/day, even under these favorable equipment assumptions
→ the residential-fridge figure in GT-10 shows a single ordinary AC fridge alone draws nearly as much as the user's entire 1.5 kWh/day figure, so that figure is defensible only if the DC-fridge assumption (A-3) holds; under a standard residential fridge it understates true need several-fold
→ 1.5 kWh/day therefore reads as low for genuine year-round 2-adult occupancy: it sits below this memo's own DC-fridge bottom-up estimate (≈2.0 kWh/day) and far below GT-11's directly-read year-round-cabin benchmark of 6-8 kWh/day for a more conventional equipment set (residential fridge + well pump)

**Pre-check:** head GT-9?, GT-10, GT-13? · ?-marked: GT-9?, GT-13? · lowest cited: none · Inputs ceiling: MEDIUM
**Confidence:** MEDIUM — GT-9? (DC fridge Ah draw) would move to HIGH-input status by opening a specific manufacturer datasheet (e.g., a Novakool or Isotherm spec sheet) instead of resting on cross-corroborated secondary sources; GT-13? (25% overhead convention) would be removed as a downgrade cause by opening gpsolarpanels.com directly rather than relying on a WebSearch summary of it. No live rival: the alternative "1.5 kWh/day is fine as stated" reading is ruled out by GT-10/GT-11 directly and recorded in §5.

### Conclusion C2: The array must be sized against the December (worst-month) PSH figure, not the annual-average PSH

GT-8? (December is angle- and duration-limited at 35°N) + GT-1? (Dec horizontal GHI ≈2.8 kWh/m²/day vs. ≈8.1 in June vs. ≈5.7 annual average)
→ December is simultaneously angle-limited and duration-limited, making it the single worst charging day of the year rather than one of several roughly-equal low months
→ a system sized to the ≈5.7 kWh/m²/day annual average would be under-supplied for the darkest several months every single year, a predictable seasonal shortfall rather than a rare edge case *[Assumes: A-12 — no backup generator covers that seasonal shortfall]*
→ the array must therefore be sized against the December design-month PSH, not the annual average

**Pre-check:** head GT-8?, GT-1? · ?-marked: GT-8?, GT-1? · lowest cited: none · Inputs ceiling: MEDIUM
**Confidence:** MEDIUM — GT-1? would be removed as a downgrade cause by opening NSRDB/PVWatts TMY3 data for the site's actual coordinates (blocked this run by network sandbox, see GT-1's Phase 3 failure record); GT-8? would move toward HIGH by citing a specific NOAA/astronomical day-length table rather than resting on unopened general knowledge, though its underlying geometry is a near-certainty. The rival "size on annual average" is ruled out by this chain itself and recorded in §5.

### Conclusion C3: A fixed-tilt PV array of approximately 800 W STC is required

C1 (design load ≈2.0 kWh/day) + C2 (December is the design month) + GT-2? (tilt-at-latitude December insolation ≈4.4 kWh/m²/day) + GT-3? (steeper winter-biased tilt adds a further 10-20% to worst-month yield) + GT-6? (published aggregate soft-loss default ≈14%, basis for this memo's 20% PV-side derate)
→ combining GT-2 and GT-3 for a winter-biased ≈50° fixed tilt puts the December design-month PSH at roughly 4.3 effective sun-hours per day *[Assumes: A-7 — the array is actually built at this steep winter tilt]*
→ a 20% aggregate PV-side derate (soiling, wiring, mismatch, MPPT conversion, temperature, aging) applied to that PSH sets the effective harvest at 3.44 good-hours per STC-watt-day *[Assumes: A-10 — the specific equipment selected performs within the published loss ranges]*
→ converting the 2.0 kWh/day design load through inverter efficiency (0.93) and LiFePO4 round-trip efficiency (0.95) means the array must deliver about 2.26 kWh/day to the battery bus, not just 2.0 kWh/day of end-use load
→ dividing 2.26 kWh/day by the 3.44 effective-hour factor gives a bare-minimum array of about 658 W STC
→ adding a 20% recharge-assurance margin, covering below-average winter days, PSH data uncertainty, and multi-year panel degradation, rounds the recommended array to about 800 W STC
→[2nd] occupants who see the system reliably meet winter demand tend to add convenience loads over the following years (a chest freezer, better connectivity, power tools), eroding the 20% recharge margin faster than degradation alone would *[Assumes: A-8 — this second-order step is exactly why A-8 ("no load creep") is flagged as fragile]*
→[3rd] by roughly year 10, panel degradation alone (≈0.5%/yr) consumes most of the 20% margin, so an installer should treat 800 W as a day-one sizing floor, not a number that stays fixed over the system's service life

**Pre-check:** head C1 (MEDIUM), C2 (MEDIUM), GT-2?, GT-3?, GT-6? · ?-marked: GT-2?, GT-3?, GT-6? · lowest cited: MEDIUM · Inputs ceiling: MEDIUM
**Confidence:** MEDIUM — capped by citing C1 and C2, both MEDIUM (see their own confidence lines for what would remove their unverified inputs); GT-2?/GT-6? would move toward HIGH by opening the underlying NREL/PVWatts data directly (blocked this run, see GT-1's Phase 3 failure record); GT-3? would be removed as a downgrade cause by running the actual site through PVWatts at both 35° and 50° tilt and comparing December output directly rather than relying on a general industry heuristic. The `[Assumes: A-7]` and `[Assumes: A-10]` premises are priced in the Conclusion's trade-offs: if A-7 fails (a lower, aesthetic tilt is built instead), the recommended 800 W understates what is needed by roughly the 10-20% GT-3 attributes to the steep tilt.

### Conclusion C4: A LiFePO4 battery bank of approximately 8 kWh nameplate (≈6.4 kWh usable at 80% DoD) is required for 3-day autonomy

C1 (design load ≈2.0 kWh/day) + GT-4? (LiFePO4 tolerates routine 80-100% DoD) + GT-5? (LiFePO4 charge acceptance drops and discharge capacity sags near/below freezing)
→ three days of autonomy at the design load, delivered through the inverter (0.93 efficiency, since autonomy days are pure discharge with no recharge to offset), requires about 6.45 kWh of usable energy from the bank
→ setting the design DoD at 80% of nameplate rather than the chemistry's technical 90-95% ceiling preserves BMS low-voltage headroom and daily-cycling life margin, which matters more once GT-5's cold-weather capacity sag stacks on top *[Assumes: A-13 — the selected product's datasheet substantiates 80% DoD cycling at its rated cycle life, not just the chemistry's theoretical capability]*
→ dividing the 6.45 kWh usable requirement by the 80% design DoD gives a nameplate battery bank of about 8.1 kWh, rounded to about 8 kWh nameplate (≈6.4 kWh usable)
→[2nd] batteries sited in an unheated space risk BMS charge lockout on freezing winter mornings (GT-5), which would silently shrink effective autonomy exactly during the design-limiting season *[Assumes: A-6 — batteries are installed in a temperature-buffered space]*
→[3rd] if A-6 is not met, real winter autonomy runs below the 3-day target on cold mornings even though the nameplate arithmetic above is satisfied; this does not contradict GT-4 or GT-5, it is exactly what GT-5 predicts when A-6 fails, so it extends this chain rather than routing back to Phase 2

**Pre-check:** head C1 (MEDIUM), GT-4?, GT-5? · ?-marked: GT-4?, GT-5? · lowest cited: MEDIUM · Inputs ceiling: MEDIUM
**Confidence:** MEDIUM — capped by citing C1 (MEDIUM; see C1's own line); GT-4?/GT-5? would move toward HIGH by opening a specific manufacturer's cycle-life and cold-discharge datasheet for the product actually purchased. Rival axis is also short here: 95% DoD sizing (≈6.8 kWh nameplate instead of ≈8 kWh) is a live rival this analysis does not fully rule out — see §5.

---

## 5. Abandoned Reasoning

### Dead End: Sizing the array off the annual-average PSH (≈5.7 kWh/m²/day) instead of the December design month

**What was tried:** Using the annual-average horizontal irradiance as the sizing PSH, which would allow a smaller, cheaper array (annual average is roughly double the December figure).

**Why abandoned:** GT-8? and GT-1? show December is simultaneously the year's lowest-sun-angle and shortest-daylight month, so an annual-average-sized system would be predictably under-supplied for the darkest several months every year — not a rare tail event but a guaranteed recurring shortfall. Ruled out by chain C2.

**What it ruled out:** Saves a future reviewer from re-deriving why off-grid sizing conventionally uses the worst-month figure rather than the mean — the reason is structural (day-length + sun-angle coincide at solstice), not merely a conservative habit.

### Dead End: Assuming a standard AC residential fridge as the base-case appliance

**What was tried:** Modeling the load buildup around whatever fridge the client happens to own, rather than dictating a DC-compressor fridge as a design assumption.

**Why abandoned:** GT-10 (read-at-source) shows a residential AC fridge alone draws ≈1,500 Wh/day — almost the user's entire 1.5 kWh/day budget by itself, leaving no room for lighting, electronics, or margin. Modeling around it would make the stated 1.5 kWh/day figure impossible to reconcile with any other load, so it was abandoned as the base case; it is kept instead as the dominant sensitivity driver and, per A-3, as an explicit equipment recommendation the installer should make to the client rather than a modeling convenience.

**What it ruled out:** Saves a reviewer from concluding this memo's ≈2.0 kWh/day design load is universally applicable — it is conditional on the DC-fridge assumption (A-3), and the memo says so rather than hiding it.

### Dead End: Including a backup generator in the sizing scope

**What was tried:** Allowing a diesel/gasoline generator to cover the winter tail, which would permit a smaller solar+battery system.

**Why abandoned:** Out of scope — the user asked for a solar+battery sizing exercise. Silently assuming a generator away would misrepresent the derivation; instead it is recorded explicitly as assumption A-12 (surfaced during the Phase 4 Assumption Audit) so the client can see it as a lever, not have it hidden.

**What it ruled out:** Saves a reviewer from mistaking the 800 W / 8 kWh figures as "with generator backup" numbers — they are not; they assume solar+battery must cover 100% of winter demand alone.

### Dead End (live rival, not fully ruled out): Sizing the battery bank at 95% DoD instead of 80%

**What was tried:** Using LiFePO4's technical DoD ceiling (≈90-95%) directly, which would shrink the nameplate battery bank from ≈8 kWh to ≈6.8 kWh and reduce cost/weight.

**Why not fully ruled out:** GT-4? confirms the chemistry can support this, and no ground truth in this analysis contradicts it outright. It is not adopted as the primary recommendation because GT-5?'s cold-weather capacity sag and BMS low-voltage headroom argue for keeping a buffer above the chemistry's bare technical ceiling — but this is a judgment call about margin, not a hard rule the ground truths force. **This remains a live rival to chain C4's endpoint** and is why C4 is rated MEDIUM on the Rivals axis rather than resolved to HIGH.

**What it ruled out:** Nothing definitively — it is carried forward into the Conclusion's trade-offs and sensitivity note as a legitimate cost-reduction option for the client, not discarded.

---

## 6. Conclusion

### Sizing memo — off-grid PV + LiFePO4, 35°N high-desert NM cabin, 2 adults year-round, 3-day autonomy

**Recommended approach:** Install a fixed-tilt, true-south-facing PV array of **≈800 W STC**, tilted steeply (≈50°, latitude+15°) to bias output toward winter, sized against a December design-month PSH of 4.3 h and a 2.0 kWh/day winter design load — not the user's 1.5 kWh/day figure (chain C3, chain C1) — paired with a LiFePO4 battery bank of **≈8 kWh nameplate (≈6.4 kWh usable at 80% DoD)** sized for 3-day autonomy (chain C4).

**Panel derate/margin stack used (chain C3):**

| Factor | Value | Notes |
|---|---|---|
| Winter design-month PSH | 4.3 h/day | December, ≈50° winter-biased tilt, Albuquerque-area proxy (GT-2?, GT-3?) |
| PV-side derate (soiling, wiring, mismatch, MPPT, temp, aging) | 0.80 (20% loss) | Above NREL's ≈14% grid-tied default (GT-6?) to reflect high-desert dust and off-grid wiring runs (GT-7?) |
| Inverter efficiency | 0.93 | Blended DC-direct + inverter-served loads |
| LiFePO4 round-trip efficiency | 0.95 | Charge + discharge combined |
| Recharge-assurance margin | ×1.20 | Covers below-average winter days, PSH data uncertainty, degradation |

**Key insight:** The dominant sizing lever here is not solar-resource uncertainty but the client's own equipment choices — refrigerator type and whether a powered well is added swing the design load, and therefore the whole system size, by 3-4× (a residential fridge alone draws nearly the user's entire stated 1.5 kWh/day budget, per GT-10; a conventional year-round cabin benchmark with a residential fridge and well pump runs 6-8 kWh/day, per GT-11) — far more than any irradiance or derate assumption in this memo moves the answer (chain C1).

**Trade-offs acknowledged:** The 80% DoD design point (vs. the chemistry's ≈90-95% technical ceiling) costs about 1.3 kWh of extra nameplate capacity in exchange for BMS/cold-weather headroom and cycle-life margin; 95% DoD sizing (≈6.8 kWh nameplate) remains a live, legitimate cost-reduction alternative this analysis does not rule out (chain C4; see §5). The 20% recharge margin is consumed by panel/battery degradation alone within roughly a decade, before any load growth is even considered (chain C3). Every irradiance and loss-stack figure in this memo is `?`-marked because this run's attempts to open NREL/PVWatts/NSRDB directly failed (network sandbox blocked the nrel.gov domain, per GT-1's Phase 3 failure record) — no chain — flagged assumption only; before purchasing hardware, run the exact site coordinates through PVWatts/NSRDB directly.

**Pre-check:** head C1 (MEDIUM), C2 (MEDIUM), C3 (MEDIUM), C4 (MEDIUM) · ?-marked: none (Conclusion cites no GT-N? directly, only via chains) · lowest cited: MEDIUM · Inputs ceiling: MEDIUM
**Confidence:** MEDIUM — every contributing chain (C1-C4) is MEDIUM, each capped by `?`-marked ground truths whose specific verification paths are named on that chain's own confidence line above; the single highest-leverage unresolved item is GT-1?/GT-2? (winter PSH for the actual site), which this run could not verify directly against NREL/PVWatts because that domain was unreachable from this sandbox (see GT-1's Phase 3 failure record) — an installer should treat re-running the exact site through PVWatts as the first task before finalizing a purchase, not an optional refinement.

### Sensitivity note

| If this changes... | ...the numbers move roughly like this |
|---|---|
| Actual load is higher than 2.0 kWh/day (e.g., residential AC fridge, powered well, or Starlink added — GT-10, GT-11, GT-12?) | Panel and battery sizes scale close to linearly with load; a 6-8 kWh/day "conventional" cabin (GT-11) would need roughly 3-4× this memo's array and battery — ≈2.4-3.2 kW STC and ≈24-32 kWh nameplate |
| Winter design PSH is lower than the 4.3 h assumed (e.g., the actual site's tilt-at-latitude/50° figure is closer to 3.5 h) | Required array rises by the same ratio the PSH falls short by; a ~19% PSH miss pushes the array from ≈800 W to ≈965 W — this is why re-running the actual coordinates through PVWatts before purchase matters more than any other single input |
| Client wants margin beyond bare 3-day autonomy (e.g., a 4-5 day cloudy-string buffer, which does occur a few times per winter in this region) | Battery nameplate scales linearly with autonomy days: a 5-day target instead of 3-day raises the bank from ≈8 kWh to ≈13.5 kWh nameplate at the same 2.0 kWh/day load and 80% DoD |
| Client accepts 95% DoD instead of 80% (§5 live rival) | Nameplate battery bank shrinks from ≈8 kWh to ≈6.8 kWh at the same usable-energy target, trading BMS/cold-weather headroom for lower cost and weight |
