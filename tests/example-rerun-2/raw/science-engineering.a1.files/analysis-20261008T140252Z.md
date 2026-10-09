## Answer

**Recommendation:** Build a 700-800 W STC PV array and a 7.5-8 kWh nameplate (6.0 kWh usable) LiFePO4 battery bank, sized against a recommended 2.0 kWh/day design load rather than the stated 1.5 kWh/day, on the condition that the battery bank sits in a temperature-conditioned enclosure (chain C2, chain C4, chain C5, chain C1). If satellite internet is wanted, rescale both numbers to a ≈3.5 kWh/day design load using the same formulas (chain C1).

**Band (from §6):** MEDIUM.

**Would change it:** Running the exact site coordinates, elevation, and chosen tilt through PVWatts directly (chain C2, chain C8); a week or more of metered consumption from the actual fridge, router, and any satellite terminal installed (chain C1); the specific battery vendor's own cold-temperature discharge datasheet (chain C5); and the owner confirming the real appliance list, generator plans, and battery-enclosure plan — the three missing inputs this analysis flags throughout (chain C5, chain C6).
## 1. Problem Essence

**Core problem:** What STC-rated PV array wattage and raw/usable LiFePO4 battery-bank kWh are required to reliably carry a year-round, 2-adult off-grid cabin load through the winter design month (the solar-resource-constrained season) with a stated 3-day no-sun autonomy reserve, starting from a user-supplied ~1.5 kWh/day load estimate that must itself be checked rather than taken as fixed?

**Success criteria:**
1. A PV array wattage (STC nameplate), with a range, is produced from a derivation chain that starts at a sourced winter-design-month insolation figure and a component-built-up system-efficiency factor — not an asserted round number.
2. A battery bank capacity is produced in both usable kWh and raw/nameplate kWh, derived from the stated autonomy target and an explicitly justified LiFePO4 depth-of-discharge convention, with round-trip efficiency and low-temperature derating addressed as separate, named effects.
3. The 1.5 kWh/day load figure is checked against a bottom-up appliance tally and explicitly labeled low, reasonable, or optimistic, with the loads commonly excluded (space heat, cooking, hot water) and the loads commonly smuggled back in (satellite internet, space heaters) both named.
4. The "3 days, zero sun" risk framing, the choice of winter (not annual-average) as the design month, tilt strategy, and generator backup are each explicitly challenged rather than accepted as given, and the absence of a stated generator decision is named as a material gap in the input, not silently assumed away.
5. The final numbers are explicitly conditioned on the daily-load figure actually used — the recommendation does not collapse to a single number that silently stops being valid if the reader's real load differs from the one assumed.

## 2. Assumptions Table

| Assumption | Type | Treatment | Verdict | Verification |
|------------|------|-----------|---------|--------------|
| The site is accurately characterized as 35°N, high-desert, 5000-7000 ft elevation, clear skies with real seasonal cloud/monsoon variation, with no more specific coordinates given | untested belief | Verify or flag; use a well-documented nearby proxy site | Accept — em-dash justification: no exact site named, so Albuquerque, NM (35.08°N, ~5,312 ft) is used as the closest well-documented 35°N high-desert proxy; actual site elevation (up to 7,000 ft) would plausibly improve clarity slightly, partially offsetting any difference | unverified — flagged |
| December/January is the lowest-insolation month at this latitude, making winter the correct design month | physical law | Accept as ground-truth candidate | Accept — survives challenge; backed by GT-3's direct solar-geometry computation (shortest days, lowest sun angle at solstice) | GT-3 |
| Winter design-month insolation ≈ 4.0 kWh/m²/day (bracket 3.5-4.5) for a reasonably tilted, south-facing fixed array near this latitude | untested belief / delegate-reported | Verify or flag | Challenge — three independent secondary sources disagreed by up to ~2× depending on tilt and whether losses were pre-applied; central estimate adopted with an explicit bracket rather than a single point value | unverified — flagged (GT-1?) |
| Annual-average insolation ≈ 6.0 kWh/m²/day (bracket 5.8-6.9) for the same site | untested belief / delegate-reported | Verify or flag | Challenge — same sourcing caveat as above; used only for the oversizing cross-check, not for headline sizing | unverified — flagged (GT-2?) |
| PVWatts-v8/NSRDB- and NASA-POWER-derived figures from secondary aggregator sites are an adequate proxy for the actual, unnamed cabin site | convention / delegate-reported | Explicitly challenge before use | Challenge — accepted as a planning-stage proxy only; the Conclusion names re-running the exact site coordinates/tilt through PVWatts directly as a required pre-purchase step | unverified — flagged |
| 80% usable depth-of-discharge is the right LiFePO4 design convention for this bank | convention | Explicitly challenge before use | Accept — challenged against the alternative conventions in the same manufacturer spec (50% DoD for 5,000 cycles, 70% for 3,000, 80% for 2,500); 80% is adopted as the standard balance of usable capacity against cycle life for a residence, not merely "because that's the number everyone quotes" | GT-4 |
| LiFePO4 round-trip efficiency ≈ 95% | untested belief | Verify or flag | Challenge — not independently re-checked against a specific source this session; carried as a general domain figure with a stated plausible range | unverified — flagged; not read — turn budget (GT-5?) |
| The battery bank sits in an unconditioned space exposed to NM winter nighttime lows (vs. a conditioned/heated enclosure) | current constraint | Record expiry conditions | Challenge — this is a design decision the owner has not yet made, not a fixed fact; it expires the moment the owner commits to locating the bank inside the cabin's heated envelope or in a heated battery box — and the Conclusion's single highest-leverage recommendation is to make that commitment now | unverified — flagged; key missing input |
| No backup generator is planned (unstated by the user, so treated as absent) | current constraint | Record expiry conditions | Challenge — a materially consequential unstated input; expires the instant the user confirms generator ownership or intent, and the recommended autonomy/backup strategy changes substantially depending on the answer | unverified — flagged; key missing input |
| "3 consecutive days of literally zero solar production" is the correct and sufficient risk threshold for autonomy sizing | convention | Explicitly challenge before use | Challenge — literal zero-production days are rare in high-desert climates (diffuse insolation persists under all but the heaviest overcast); the more realistic risk is a multi-day *sustained low* (not zero) production event during a slow-moving winter storm, which a 3-day-zero spec does not strictly dominate — surfaced via the inversion procedure below | unverified — flagged; carried into Conclusion as an explicit caveat |
| 1.5 kWh/day accurately represents 2 year-round adult occupants' electrical load | untested belief | Verify via bottom-up tally (Estimate procedure) | Challenge — bottom-up tally brackets roughly 1.1-1.6 kWh/day for a lean, no-satellite-internet household, and 2.5-3.8 kWh/day if satellite internet is added; 1.5 kWh/day is defensible only under the lean case | Chain C1 (this analysis) |
| Space heating, cooking, and hot water are handled by propane/wood, not electricity, and stay outside this system's budget | current constraint | Record expiry conditions | Accept — consistent with typical off-grid cabin practice in this climate and explicitly matches the user's framing; expires, with severe consequences (5-20× load increase), if any of these is later electrified | unverified — flagged; high-stakes boundary condition |
| The array uses a fixed tilt (no seasonal adjustment, no tracker) | convention | Explicitly challenge before use | Challenge — a manually seasonally-adjustable tilt rack is cheap and common in off-grid builds and would improve the winter number beyond the conservative bracket used here; the fixed-tilt assumption is kept as the conservative baseline, with the unused upside left as margin | unverified — flagged; design choice left open |
| LiFePO4's cold-discharge derate (~30% loss at 0°F) applies at this cabin's actual, low-current overnight draw | untested belief | Verify or flag | Challenge — sourced data shows the derate is current-rate dependent (as low as ~18% loss at 1A-class draw vs. ~45% at higher rates near -20°C); the cabin's low average draw likely sits toward the milder end, but the conservative 30%-at-0°F figure is retained rather than assumed away | unverified — flagged (GT-6?) |
| Charging LiFePO4 below freezing risks permanent damage absent a heater/BMS cutoff | physical/chemical fact | Accept as ground-truth candidate | Accept — well-corroborated lithium-ion electrochemistry; treated as a hard constraint on the "unconditioned battery space" design option, not a soft preference | GT-7? (reported-by-delegate this session) |
| The charge controller is a high-quality MPPT type, not a cheaper PWM type | convention | Explicitly challenge before use | Accept — MPPT is the de facto standard for serious off-grid builds and materially improves winter low-sun-angle harvest versus PWM; adopted as the baseline design choice, not assumed without comment | unverified — flagged; design choice |
| The compiled component efficiency stack (MPPT 97%, DC wiring 98%, temperature 97%, soiling 96%, inverter 94%, aging/safety margin 90% → ≈75% combined) correctly represents this system's real-world losses | convention | Explicitly challenge before use | Accept — challenged against, and found consistent with, the independently-sourced PVWatts default loss stack (~82.5% before any extra aging/safety margin) and the classic off-grid "0.75 rule of thumb" cited in sizing handbooks; the convergence of two independent routes to the same ≈0.75 figure is treated as corroboration, not coincidence | GT-8? (reported-by-delegate, cross-validated) |
| The owner is able to place the battery bank inside the cabin's heated envelope, or build a heated battery box (A-battery-enclosure; surfaced by the end-of-Phase-4 Assumption Audit from chain C5) | current constraint | Record expiry conditions | Accept — assumed feasible as the baseline recommendation; expires if site or budget constraints make a heated enclosure impractical, in which case chain C5's unconditioned 10.7 kWh figure is the correct design target instead | unverified — flagged |
| The battery bank cycles roughly once per day (A-cycle-rate; surfaced by the end-of-Phase-4 Assumption Audit from chain C7) | untested belief | Verify or flag | Challenge — reasonable for a daily solar-charge / evening-discharge pattern but not metered; the 6.8-year cycle-life estimate in chain C7 scales inversely if the real cycling rate differs | unverified — flagged |

**Inversion check (Phase 2 companion technique — triggered because the "3 days, zero sun" autonomy spec is exactly the kind of clean, unquestioned convention this technique exists to probe).**

Claim inverted: *"The system fails to keep the cabin powered."* Failure-guaranteeing conditions enumerated, with the necessary precondition each implies and a load-bearing tag:

1. A sustained winter storm delivers 20-40% of normal production (not zero) for 5-7 days → precondition: *the battery holds enough energy to ride through a multi-day low-production event, not just a literal zero-production one* — **load-bearing**.
2. A load is added after commissioning that was never part of the sizing budget (satellite internet, space heater, guests) → precondition: *the installed system carries headroom above the originally-budgeted load, or the owner re-sizes before adding major loads* — **load-bearing**.
3. The battery bank is charged while below freezing with no heater/BMS cutoff, suffering permanent capacity loss → precondition: *the battery enclosure is conditioned, or carries active low-temperature protection* — **load-bearing**.
4. There is no generator and the battery is drawn down with no backup for the residual multi-day-storm or load-creep risk → precondition: *either a generator exists, or the autonomy margin is large enough to make its absence an accepted, explicit risk* — **load-bearing**.
5. The array underperforms its design-month estimate because the real site's shading, elevation, or tilt differs materially from the Albuquerque-proxy figures used here → precondition: *the exact site is re-run through PVWatts before purchase* — not load-bearing for this analysis's own conclusions (it bears on execution, not on the sizing logic itself).

Each load-bearing precondition becomes, or reinforces, an `untested belief` row in the table above (rows for battery location, generator, 3-day-zero threshold, and load estimate) and is carried forward into the Derivation Chains and Conclusion as an explicit caveat rather than silently assumed to hold.

## 3. Ground Truths

- **GT-1?** Winter (December) design-month insolation for 35°N high-desert NM (Albuquerque-area proxy, ~5,312 ft) ≈ 4.0 kWh/m²/day equivalent peak sun hours for a reasonably tilted (20°-31°), fixed, south-facing array; a bracket of 3.5-4.5 kWh/m²/day spans the independent sources found. — cited to: a secondary aggregator (thegreenwatt.com) stating "NREL PVWatts v8 / NSRDB ... December (Lowest Month): 4.4 PSH" at 20° tilt with 14% losses pre-applied, and a second aggregator (profilesolar.com) stating a NASA-POWER-derived winter-seasonal average of 3.77 kWh/day at an optimal 31° tilt; reported-by-delegate: both secondary pages were fetched directly this session, but the primary NREL/NASA datasets were not opened directly. Phase 3 failure record: `pvwatts.nrel.gov` — unreachable (DNS resolution failure, `ENOTFOUND`); `solarpathfinder.com` — unreachable (HTTP 403 Forbidden).
- **GT-2?** Annual-average insolation for the same site ≈ 6.0 kWh/m²/day, bracket 5.8-6.9 kWh/m²/day. — cited to: the same two aggregator pages (thegreenwatt.com: "Annual Average: 6.42 PSH"; a third search summary citing "Albuquerque specifically has 6.9 peak sun hours/day"); reported-by-delegate, same Phase 3 failure record as GT-1.
- **GT-3** At 35°N on the winter solstice (Dec 21), solar-noon elevation angle ≈ 31.6° (computed as 90° − |35° − (−23.44°)| using Earth's axial tilt of 23.44°). — source: direct computation from the standard solar-elevation formula and the physical constant of Earth's axial tilt; read-at-source: computed directly in this analysis, not reported by any secondary source — this is a first-principles astronomical fact, not a looked-up figure.
- **GT-4** LiFePO4 manufacturers commonly publish cycle-life-vs-DoD tables with an 80% DoD design point; one major manufacturer's LFP-Smart range is rated 2,500 cycles at 80% DoD, 3,000 cycles at 70% DoD, and 5,000 cycles at 50% DoD, each to 80% of nominal capacity retained. — source: Victron LFP-Smart datasheet figures as quoted at communityarchive.victronenergy.com/questions/10779; read-at-source: this URL was fetched directly this session and the cycle-count-vs-DoD table was read and quoted above.
- **GT-5?** LiFePO4 round-trip (charge/discharge) efficiency is commonly cited in the 92-98% range, with ≈95% as a typical central design value. — unverified: not checked against a specific source this session; not read — turn budget (this GT was deliberately not pursued further to preserve budget for the higher-leverage battery-location and insolation reads; it feeds only MEDIUM-or-below chains, so the shortfall is bounded, not silent).
- **GT-6?** LiFePO4 discharge capacity derates meaningfully below freezing: at 0°F (−17.8°C), roughly 70% of rated capacity is available (≈30% reduction); the derate is current-rate dependent — at −20°C, capacity retention ranges from ≈55% at higher discharge rates down to ≈82% at low (1A-class) discharge rates. — cited to: a search summary aggregating endless-sphere forum test data and a vatrerpower blog post; reported-by-delegate: the search summary was reviewed, but the primary vatrerpower page could not be opened. Phase 3 failure record: `vatrerpower.com` — unreachable (HTTP 403 Forbidden).
- **GT-7?** Charging LiFePO4 cells below 0°C (32°F) risks permanent capacity loss from lithium plating unless the pack has internal heating and/or a BMS low-temperature charge cutoff; discharging below freezing is generally permitted (at reduced capacity) but charging is not. — cited to: the same search summary as GT-6 (battery-chemistry explainer content); reported-by-delegate — no primary source opened this session for this specific claim.
- **GT-8?** NREL's PVWatts v8 default "system loss" stack for a standard reference system totals ≈14% (soiling, shading, snow, mismatch, wiring, connections, light-induced degradation, nameplate rating, age, availability) before a separately-modeled ≈96% inverter efficiency is applied, yielding a combined DC-to-AC derate of ≈82.5%. — cited to: thegreenwatt.com, fetched directly this session, which states the PVWatts-based calculation "account[s] for 14% real-world losses"; reported-by-delegate: the ten-component breakdown itself is this analysis's own recalled knowledge of the published PVWatts default stack and was not independently re-opened at `pvwatts.nrel.gov` this session (same unreachable-source failure record as GT-1).
- **GT-9?** Off-grid-rated 12V/24V DC compressor refrigerators (e.g., Danfoss/Secop-based units common in cabins) typically consume roughly 250-650 Wh/day in normal household use, varying with unit size, ambient temperature, and door-opening frequency. — cited to: a search summary aggregating RV/off-grid-fridge sources (bluettipower.com, autoroamer.com, solar-electric.com forum); reported-by-delegate — no single primary datasheet opened this session.
- **GT-10?** A Starlink "Standard" satellite internet terminal (dish + router) draws roughly 60-90 W continuously in normal operation (idle ≈45 W, active/cold-weather-heated up to ≈125 W), equivalent to roughly 1.4-2.2 kWh/day if run continuously. — cited to: a search summary aggregating dishytech.com, nerdtechy.com, and forum.dishytech.com; reported-by-delegate — no single primary source opened this session.

**Provenance summary:** `?`-marked: GT-1, GT-2, GT-5, GT-6, GT-7, GT-8, GT-9, GT-10 (8 of 10). Read-at-source: GT-3 — computed directly from the axial-tilt constant and solar-elevation formula; GT-4 — communityarchive.victronenergy.com/questions/10779, cycle-count-vs-DoD table quoted directly.

## 4. Derivation Chains

### Conclusion C1: The 1.5 kWh/day load estimate is defensible only as a lean, no-satellite-internet baseline; the recommended design load is 2.0 kWh/day without satellite internet, or ≈3.5 kWh/day with it

GT-9? (DC compressor fridge ≈250-650 Wh/day, central 500) + GT-10? (Starlink terminal ≈1.4-2.2 kWh/day if run continuously, central ≈1.7)
→ a lean no-satellite household (lighting ≈200 Wh, fridge ≈500 Wh, water pump ≈50 Wh, phone/laptop charging ≈100 Wh, a small hardwired router ≈120 Wh, misc/tools ≈150 Wh) totals roughly 1.1-1.6 kWh/day, which places the user's 1.5 kWh/day figure at the upper end of lean but still inside the plausible range
→ adding satellite internet alone adds more than the entire lean budget on top of it, pushing a realistic total to roughly 2.5-3.8 kWh/day
→ recommend designing to 2.0 kWh/day as the no-satellite baseline, with explicit re-scaling to ≈3.5 kWh/day if satellite internet is wanted, rather than treating 1.5 kWh/day as a safe fixed design point

**Pre-check:** head GT-9?, GT-10? · ?-marked: GT-9?, GT-10? · lowest cited: none · Inputs ceiling: MEDIUM
**Confidence:** MEDIUM — GT-9? and GT-10? are both reported-by-delegate (search-summary sourced, no single primary datasheet opened); the verification that would remove both as a cause of the downgrade is a week of actual metered consumption at the specific fridge/router the owner installs, or direct vendor datasheets for the chosen models

---

### Conclusion C2: The required PV array is approximately 700-800 W STC under the no-satellite design load, with a defensible bracket of roughly 556-816 W

GT-1? (winter design-month insolation ≈4.0 kWh/m²/day, bracket 3.5-4.5) + C1 (recommended design load 2.0 kWh/day, no-satellite baseline)
→ combining GT-1 with a component-built efficiency stack of ≈75% (MPPT 97% x DC wiring 98% x temperature 97% x soiling 96% x inverter 94% x aging/safety margin 90%, cross-validated against GT-8) gives a central required array size of 2,000 Wh ÷ (4.0 kWh/m²/day x 0.75) ≈ 667 W STC
→ bracketing both the insolation uncertainty (3.5-4.5) and the efficiency-stack uncertainty (0.70-0.80) gives a design range of roughly 556-816 W STC
→ rounding toward the conservative end for standard module sizing and the asymmetric cost of under- versus over-building, recommend a 700-800 W STC array for the no-satellite design load

**Pre-check:** head GT-1?, C1 (MEDIUM) · ?-marked: GT-1? · lowest cited: MEDIUM · Inputs ceiling: MEDIUM
**Confidence:** MEDIUM — GT-1? is reported-by-delegate (secondary PVWatts/NASA-POWER aggregator pages, primary source unreachable this session); the verification that would remove it as a cause of the downgrade is running the exact cabin coordinates, elevation, and chosen tilt through PVWatts directly once a site is fixed. C1 is itself MEDIUM (see C1's own confidence line) and caps this chain at MEDIUM regardless of GT-1's status

---

### Conclusion C3: Winter-month-based array sizing is roughly 1.5x what annual-average-based sizing would call for, which is the quantitative form of the standard off-grid oversizing convention

GT-1? (winter PSH ≈4.0) + GT-2? (annual-average PSH ≈6.0) + C1 (design load 2.0 kWh/day, no-satellite baseline)
→ sizing the same array against the annual-average insolation instead of the winter design-month figure, holding the same ≈75% efficiency factor, would call for only ≈444 W STC
→ the winter-based array from C2 (≈667 W) is therefore about 1.5x the size an annual-average-based calculation would produce
→ this 1.5x factor matches the 1.3-1.6x winter-vs-annual oversizing commonly cited in off-grid design guidance, and it exists because a grid-tied system can borrow against the annual average while an off-grid system facing a continuous winter deficit cannot

**Pre-check:** head GT-1?, GT-2?, C1 (MEDIUM) · ?-marked: GT-1?, GT-2? · lowest cited: MEDIUM · Inputs ceiling: MEDIUM
**Confidence:** MEDIUM — GT-1? and GT-2? are both reported-by-delegate with the same unreachable-primary-source record as C2; the verification path is identical (direct PVWatts run at the exact site). C1's MEDIUM rating also caps this chain

---

### Conclusion C4: The battery bank must hold 6.0 kWh usable / 7.5-8 kWh nameplate, assuming the bank sits in a temperature-conditioned space

C1 (design load 2.0 kWh/day, no-satellite baseline) + GT-4 (80% DoD design convention, 2,500 cycles at 80% DoD per manufacturer spec)
→ three days of autonomy at the full baseline load requires 2.0 kWh/day x 3 days = 6.0 kWh of usable, discharge-side capacity
→ reserving the 20% buffer GT-4's 80%-DoD convention calls for, the raw/nameplate bank must be 6.0 kWh ÷ 0.80 = 7.5 kWh, on the assumption that the bank sits in a temperature-conditioned space
→ recommend a 7.5-8 kWh nameplate / 6.0 kWh usable bank as the headline figure for the conditioned-space case

**Pre-check:** head C1 (MEDIUM), GT-4 · ?-marked: none · lowest cited: MEDIUM · Inputs ceiling: MEDIUM
**Confidence:** MEDIUM — GT-4 is read-at-source and carries no downgrade of its own; the chain is capped at MEDIUM solely because its head cites C1, whose own MEDIUM rating (load-estimate uncertainty) is explained on C1's confidence line

---

### Conclusion C5: Where the battery bank is located is a bigger lever on nameplate sizing than any single component-efficiency assumption, and an unconditioned enclosure both inflates the nameplate requirement by roughly 40% and risks permanent charge damage

C4 (nameplate 7.5 kWh, conditioned-space case) + GT-6? (cold-discharge derate ≈30% at 0°F) + GT-7? (charging LiFePO4 below freezing risks permanent damage absent a heater/BMS cutoff)
→ if the same bank instead sits in an unconditioned space exposed to typical high-desert winter lows near or below 0°F, its usable capacity at the moment of need is only ≈70% of nameplate, so the nameplate required to still deliver the same 6.0 kWh usable rises to 7.5 kWh ÷ 0.70 ≈ 10.7 kWh
→ the choice of where the battery lives therefore swings the nameplate requirement by roughly 40% (7.5 kWh versus 10.7 kWh), which is a larger effect than any single line item in C2's component-efficiency stack
→ recommend locating the bank in a conditioned or actively heated enclosure as the single highest-leverage design decision in this analysis, both to avoid this capacity penalty and to avoid GT-7's charging-damage risk *[Assumes: A-battery-enclosure — the owner is able to place the bank inside the cabin's heated envelope or build a heated battery box; if not, the 10.7 kWh unconditioned figure is the correct design target instead, and that substitution is exactly what this chain already computes]*

**Pre-check:** head C4 (MEDIUM), GT-6?, GT-7? · ?-marked: GT-6?, GT-7? · lowest cited: MEDIUM · Inputs ceiling: MEDIUM
**Confidence:** MEDIUM — GT-6? and GT-7? are both reported-by-delegate (GT-6's primary source, vatrerpower.com, returned HTTP 403 this session); the verification path is a primary cell-level cold-temperature datasheet from the specific battery vendor chosen. C4's own MEDIUM rating also caps this chain. The A-battery-enclosure assumption is priced directly in the hop that states it (the chain computes both outcomes), so it does not independently lower the band further

---

### Conclusion C6 [Speculative]: A 3-day battery baseline with a small backup generator held as emergency-only use narrowly outranks a battery-only design in a weighted trade-off, but the margin is thin and the decision is not load-bearing for the headline PV/battery sizing above

GT-1? (winter insolation variability underlying multi-day-storm risk) + C4 (battery nameplate 7.5 kWh at 3-day autonomy, conditioned case)
→ weighing battery-only autonomy (raised to 4-5 days), a fully generator-reliant design, and a composite of the C4 battery baseline plus an emergency-only generator, on resilience / upfront cost / maintenance / noise / simplicity (weights 5/3/2/2/3, each anchored 1-5) gives weighted totals of 56 (battery-only), 51 (generator-reliant), and 58 (composite)
→ the composite wins by only 2 points over battery-only, and the flip test shows dropping the resilience weight from 5 to 3 flips the ranking back to battery-only, so the result is real but not robust
→ recommend the composite as the default (keep the C4 battery baseline as the daily-cycling design, add a small backup generator for emergency-only use against the multi-day-storm and load-creep risk the inversion check surfaced), while naming battery-only at 4-5 days autonomy as a nearly-tied, legitimate alternative for an owner who does not want to own or maintain a generator — this choice does not change the C2/C4 headline sizing numbers, which hold under either option

**Pre-check:** head GT-1?, C4 (MEDIUM) · ?-marked: GT-1? · lowest cited: MEDIUM · Inputs ceiling: MEDIUM
**Confidence:** MEDIUM — marked `[Speculative]`: the claim this chain supports (which generator strategy to adopt) is not load-bearing for the headline PV-array/battery-capacity conclusion, which stands on C2/C3/C4/C5 regardless of how the generator question is resolved; it is offered as a secondary, explicitly flagged recommendation. Even so, its own downgrade causes are named: GT-1? is reported-by-delegate (same verification path as C2/C3), C4's MEDIUM rating is explained on its own line, and the live, unsettled rival (battery-only, trailing by only 2 weighted points) is not ruled out by anything in this analysis — the specific fact that would settle it is the owner's own generator preference/ownership, which this analysis does not have and names in the Conclusion as a key missing input

---

### Conclusion C7: Battery cycle aging and typical load growth both erode the designed 3-day margin over the system's life, so the nameplate battery should carry roughly 15-20% extra headroom at purchase

C4 (nameplate 7.5 kWh, conditioned case) + GT-4 (2,500 cycles at 80% DoD before capacity falls to 80% of original)
→ at roughly one discharge cycle per day *[Assumes: A-cycle-rate — the bank cycles about once per day; a faster or slower real cycling rate scales the following year-count inversely]*, 2,500 cycles corresponds to about 6.8 years before the bank is warranted to only 80% of its own original nameplate, which, through the actor lens of the owner living with the result, means the real autonomy margin shrinks from 3.0 days toward roughly 2.4 days over that period even if nothing else about the load changes
→ through the actor lens of future behavior, a work-from-cabin routine, a second fridge or chest freezer, or satellite internet (GT-10) are in practice more likely to erode the margin faster than battery aging alone, because the load side of the equation tends to creep upward rather than stay fixed
→ through the time lens, the system has its full designed margin immediately after commissioning, a partially eroded margin after a few years from aging and load growth together, and once the system has been in place long enough to be "just how the cabin works," any later load addition is the one most likely to go unexamined against the original energy budget
→ none of these effects contradicts a ground truth; recommend buying roughly 15-20% headroom on the nameplate battery figure now (≈9 kWh rather than the bare 7.5 kWh) to absorb cycle aging and modest load growth without a mid-life redesign, plus an annual check of actual load against the original budget

**Pre-check:** head C4 (MEDIUM), GT-4 · ?-marked: none · lowest cited: MEDIUM · Inputs ceiling: MEDIUM
**Confidence:** MEDIUM — capped by C4's own MEDIUM rating (explained on C4's line); the A-cycle-rate assumption is priced in the hop that states it (the 6.8-year figure is explicitly conditioned on it and scales inversely if false), so it is not an independent cause of the downgrade

---

### Conclusion C8: An independent clear-sky physics estimate lands in the same 3-4 kWh/m²/day neighborhood as GT-1's reported bracket, raising confidence that GT-1 is a physically plausible figure rather than a data or tilt-mismatch artifact

GT-3 (solar-noon elevation ≈31.6° and ≈9h20m daylight at 35°N on the winter solstice) + GT-1? (claimed winter design-month insolation ≈4.0 kWh/m²/day, bracket 3.5-4.5)
→ reducing GT-1's claimed figure to its physical primitives, a ≈31.6° peak sun angle and a ≈9.3-hour daylight window deliver meaningfully less direct energy per hour than midsummer's >78° elevation, consistent with a winter figure well below the ≈7-8 kWh/m²/day peak-summer figures found in the same searches
→ an independent estimate built from extraterrestrial irradiance (≈1,361 W/m²) scaled by the sine of a ≈32° elevation, a clear-sky atmospheric transmission factor appropriate to 5,000-7,000 ft, and a ≈9.3-hour daylight window lands in the same 3-4 kWh/m²/day neighborhood as GT-1's reported bracket, rather than an order of magnitude away
→ this independent physical check raises confidence that GT-1's bracket is a physically plausible figure for this latitude and season, even though the exact value still was not read at a primary NREL/NASA source this session

**Pre-check:** head GT-3, GT-1? · ?-marked: GT-1? · lowest cited: none · Inputs ceiling: MEDIUM
**Confidence:** MEDIUM — GT-3 is read-at-source and carries no downgrade of its own; the chain is capped at MEDIUM solely by GT-1?, whose verification path (direct PVWatts run at the exact site) is the same one named on C2, C3, and C8 alike

## 5. Abandoned Reasoning

### Dead End: Sizing the PV array to annual-average insolation

**What was tried:** An early pass considered sizing the array against the annual-average insolation figure (GT-2?, ≈6.0 kWh/m²/day), which would have produced a smaller, cheaper array (≈444 W at the same load and efficiency factor, per chain C3).

**Why abandoned:** This contradicts the Essence Statement's own success criterion that the design-constraining month must be winter for a year-round occupancy, and it contradicts GT-3's physical-geometry fact that winter is unambiguously the lowest-resource month at this latitude — an annual-average design would leave the cabin undersupplied for roughly half the year, not just on rare bad days.

**What it ruled out:** Using any single annual-average figure as the headline design basis for a year-round off-grid system; it also produced the 1.5x oversizing ratio reported in chain C3 as a useful byproduct, turning a rejected approach into a validating cross-check for the winter-based number.

### Dead End: Using the 1970s NREL West Solar Monitoring Network's global-horizontal December figure (≈2.6-2.95 kWh/m²/day) as GT-1

**What was tried:** The first search results returned a December figure of 2.6-2.95 kWh/m²/day for Albuquerque, sourced to 1970s-80s NREL ground-station records, which was briefly considered as the winter design-month ground truth.

**Why abandoned:** That figure is global horizontal irradiance (on a flat, unty tilted surface), not insolation on a south-facing array tilted toward the winter sun; it systematically understates what a properly tilted off-grid array actually collects, and later sources explicitly describing fixed-tilt (20-31°) arrays reported roughly 1.5-2x higher December figures (3.77-4.4 kWh/m²/day) for the same location.

**What it ruled out:** Treating "insolation" as a single tilt-independent number; GT-1 is instead built from sources that already describe a tilted, south-facing array, which is the correct basis for sizing a fixed-tilt off-grid PV array.

### Dead End: Treating the stated "3 days of literal zero sun" autonomy spec as a complete, self-sufficient risk model

**What was tried:** An initial pass took the autonomy requirement entirely at face value — size the battery for exactly 3 days of zero production and call the risk fully addressed.

**Why abandoned:** The inversion check (Phase 2) showed that literal zero-production days are rare in a high-desert climate (diffuse insolation persists under all but the heaviest overcast), while a multi-day *sustained low* (not zero) production event during a slow-moving winter storm is both more statistically likely and can impose a comparable or larger cumulative energy deficit than three literal zero-sun days — a risk the "3 days, zero sun" framing does not strictly dominate.

**What it ruled out:** Presenting the 3-day/7.5 kWh battery figure as a complete, risk-free guarantee; it is instead carried forward as the named autonomy *design point* in C4, with the residual multi-day-storm risk explicitly surfaced in C6's trade-off and in the Conclusion's caveats rather than silently absorbed into the number.

## 6. Conclusion

**Recommended approach:** Design the PV array to roughly 700-800 W STC and the battery bank to roughly 7.5-8 kWh nameplate / 6.0 kWh usable, against a recommended 2.0 kWh/day design load (not the stated 1.5 kWh/day) with no satellite internet, assuming the battery bank is located in a temperature-conditioned enclosure (chain C2, chain C4, chain C5); if satellite internet is wanted, rescale both numbers using the same formulas against a ≈3.5 kWh/day design load instead (chain C1).

**Key insight:** Where the battery bank physically lives is a bigger lever on the nameplate battery requirement (≈7.5 kWh conditioned versus ≈10.7 kWh unconditioned, a ≈40% swing) than any single component-efficiency assumption in the entire PV sizing chain, including the insolation figure itself — reasoning by the usual shorthand of "usable kWh ÷ DoD% = nameplate kWh" misses this entirely because it treats DoD as the only lever on nameplate sizing (chain C5).

**Trade-offs acknowledged:** A small backup generator held as emergency-only use narrowly outranks a battery-only design (58 vs. 56 weighted points) as protection against the multi-day, low-but-nonzero-production storms that the literal "3 days, zero sun" spec does not fully cover, but the margin is thin enough that a generator-averse owner choosing battery-only (at 4-5 days autonomy instead of 3) is a legitimate, nearly-tied alternative, not a mistake (chain C6). Whether this trade-off actually favors a generator depends on the owner's own generator preference, which this analysis does not have — no chain — flagged assumption only. Separately, buying roughly 15-20% nameplate battery headroom above the bare 7.5 kWh figure (≈9 kWh) is recommended to absorb battery cycle-aging and ordinary load growth over the system's life without a mid-life redesign (chain C7).

**Pre-check:** head C1 (MEDIUM), C2 (MEDIUM), C4 (MEDIUM), C5 (MEDIUM), C7 (MEDIUM); C6 (MEDIUM, `[Speculative]`, non-load-bearing for this Conclusion per its own confidence line) · ?-marked: none directly · lowest cited: MEDIUM · Inputs ceiling: MEDIUM
**Confidence:** MEDIUM — every chain this Conclusion rests on (C1, C2, C4, C5, C7) is itself MEDIUM, each capped by at least one reported-by-delegate ground truth whose primary source could not be opened this session (GT-1?, GT-9?, GT-10? for the load and array figures; GT-6?, GT-7? for the battery-location figure). C6 is excluded from this calculation under the speculative-chain exception (its own confidence line states why) and does not independently lower this rating. What would move the band toward HIGH: (1) running the exact cabin coordinates, elevation, and chosen tilt through PVWatts directly, closing GT-1/GT-2; (2) a week or more of metered consumption from the specific fridge, router, and any satellite terminal the owner actually installs, closing GT-9/GT-10; (3) the specific LiFePO4 vendor's own cold-temperature discharge datasheet, closing GT-6/GT-7; and (4) the owner confirming the actual appliance list, generator plans, and battery-enclosure plan, which are the three missing inputs named throughout this analysis.
## Appendix — process output

## Section 6 to Section 4 closure ledger (process output)

- "Design the PV array to roughly 700-800 W STC and the battery bank to roughly 7.5-8 kWh nameplate / 6.0 kWh usable, against a recommended 2.0 kWh/day design load..." → chain C2 ✓ (also cites C1, C4, C5 inline)
- "Where the battery bank physically lives is a bigger lever on the nameplate battery requirement... than any single component-efficiency assumption..." → chain C5 ✓
- "A small backup generator held as emergency-only use narrowly outranks a battery-only design (58 vs. 56 weighted points)..." → chain C6 ✓
- "Whether this trade-off actually favors a generator depends on the owner's own generator preference, which this analysis does not have" → no chain — flagged assumption only (marked caveat, retained per the Caveats rule; the parent claim it qualifies is already traced to chain C6)
- "buying roughly 15-20% nameplate battery headroom above the bare 7.5 kWh figure (≈9 kWh) is recommended..." → chain C7 ✓
- "**Pre-check:** head C1 (MEDIUM), C2 (MEDIUM), C4 (MEDIUM), C5 (MEDIUM), C7 (MEDIUM); C6 (MEDIUM, [Speculative]...)" → chains C1, C2, C4, C5, C6, C7 ✓ (self-citing per the template's Pre-check-is-a-claim note)
- "**Confidence:** MEDIUM — every chain this Conclusion rests on (C1, C2, C4, C5, C7) is itself MEDIUM..." → chains C1, C2, C4, C5, C7 ✓ (C6 explicitly excluded per its own speculative-chain exception)

Ledger clean: every §6 claim either cites a chain inline or carries the permitted caveat marker. No claim cut.
## Assumption Audit scan (process output)

| Chain | Step | Step Text (brief) | Assumption surfaced? | Added to Table? |
|-------|------|-------------------|----------------------|-----------------|
| C1 | 1 | Lean no-satellite household totals ~1.1-1.6 kWh/day | none | n/a |
| C1 | 2 | Satellite internet alone adds more than the entire lean budget | none | n/a |
| C1 | 3 | Recommend 2.0 kWh/day baseline, rescale to ~3.5 kWh/day with satellite | none | n/a |
| C2 | 1 | Combine GT-1 with ~75% efficiency stack for central 667 W | none (efficiency stack already an Assumptions Table row) | n/a |
| C2 | 2 | Bracket insolation + efficiency uncertainty to 556-816 W | none | n/a |
| C2 | 3 | Recommend 700-800 W STC array | none | n/a |
| C3 | 1 | Annual-average-based sizing would call for ~444 W | none | n/a |
| C3 | 2 | Winter-based array is ~1.5x the annual-average-based figure | none | n/a |
| C3 | 3 | 1.5x matches the standard off-grid oversizing convention | none | n/a |
| C4 | 1 | 3 days autonomy requires 6.0 kWh usable | none | n/a |
| C4 | 2 | 20% DoD buffer gives 7.5 kWh nameplate, assuming conditioned space | battery-location assumption (conditioned case) | n/a — already covered by the existing Assumptions Table row on battery-enclosure conditioning |
| C4 | 3 | Recommend 7.5-8 kWh nameplate / 6.0 kWh usable | none | n/a |
| C5 | 1 | Unconditioned case: ~70% capacity -> 10.7 kWh nameplate | none (uses GT-6, already in table) | n/a |
| C5 | 2 | Battery location swings nameplate ~40%, more than any efficiency line item | none | n/a |
| C5 | 3 | Recommend conditioned/heated enclosure `[Assumes: A-battery-enclosure]` | A-battery-enclosure | yes — added to Assumptions Table |
| C6 | 1 | Weighted trade-off totals: 56 / 51 / 58 across three generator-strategy options | none | n/a |
| C6 | 2 | Flip test: resilience weight 5→3 flips the winner | none | n/a |
| C6 | 3 | Recommend the composite, battery-only named as a near-tied alternative | none | n/a |
| C7 | 1 | ~1 cycle/day gives ~6.8 years to 80% capacity `[Assumes: A-cycle-rate]` | A-cycle-rate | yes — added to Assumptions Table |
| C7 | 2 | Load growth likely erodes margin faster than aging alone | none (ties to existing load-estimate / satellite-internet rows) | n/a |
| C7 | 3 | Time-lens: margin erodes immediately → a few years → "just how it works" | none | n/a |
| C7 | 4 | Recommend ~15-20% nameplate headroom and an annual load check | none | n/a |
| C8 | 1 | Winter sun angle/day-length delivers less direct energy per hour than midsummer | none | n/a |
| C8 | 2 | Independent clear-sky physics estimate lands in the same 3-4 kWh/m²/day neighborhood | none | n/a |
| C8 | 3 | Raises confidence that GT-1's bracket is physically plausible | none | n/a |

Audit complete: 24 steps scanned across 8 chains, in order, no step skipped. Two new assumptions surfaced (A-battery-enclosure from C5, A-cycle-rate from C7) and both were added to the Section 2 Assumptions Table with inline `[Assumes: X]` marks left on their originating chain steps.
## Adversarial pass (process output)

**Recompute.** C2 central: 2,000 Wh ÷ (4.0 kWh/m²/day × 0.75) = 667 W — recomputes to 666.7 W, matches. C2 bracket: 2,000 ÷ (3.5 × 0.70) = 816 W and 2,000 ÷ (4.5 × 0.80) = 556 W — both recompute exactly. C3 annual-average basis: 2,000 ÷ (6.0 × 0.75) = 444 W — recomputes to 444.4 W, and 667/444 = 1.50x, matches. C4: 2.0 kWh/day × 3 days = 6.0 kWh usable; 6.0 ÷ 0.80 = 7.5 kWh nameplate — both recompute exactly. C5: 7.5 ÷ 0.70 = 10.71 kWh — recomputes to 10.71 kWh, matches "≈10.7 kWh." C6 weighted totals: Option A (battery-only) = 3×5+2×3+5×2+5×2+5×3 = 15+6+10+10+15 = 56; Option B (generator-reliant) = 5×5+4×3+2×2+2×2+2×3 = 25+12+4+4+6 = 51; Option C (composite) = 5×5+4×3+3×2+3×2+3×3 = 25+12+6+6+9 = 58 — all three recompute exactly as stated. C7: 2,500 cycles ÷ 365 cycles/year ≈ 6.85 years — recomputes to "about 6.8 years," matches. Efficiency stack: 0.97×0.98×0.97×0.96×0.94×0.90 = 0.7489 ≈ 0.75 — recomputes, matches.

**Sensitivity.** The single ground truth whose falsity would flip the headline PV-array conclusion (C2) is GT-1? (winter design-month insolation): if the real site's December resource is materially below the 3.5 kWh/m²/day low end of the bracket (e.g., due to shading or a lower actual elevation than assumed), the recommended 700-800 W array would be undersized. GT-1 is `?`-marked, and its verification path (a direct PVWatts run at the exact site coordinates and chosen tilt) is named on C2's own confidence line. For the battery conclusion (C4/C5), the flip ground truth is the battery-enclosure assumption (A-battery-enclosure, surfaced in the Assumption Audit): if the enclosure is not actually conditioned, the correct nameplate target is 10.7 kWh, not 7.5 kWh — a 43% difference, larger than any other single sensitivity in this analysis. Weakest link per chain: C1 (fridge/Starlink wattage, both `?`-marked and search-sourced only); C2/C3/C8 (GT-1?, unreachable primary source); C4 (inherits C1's load uncertainty); C5 (the battery-enclosure decision itself, not yet made by the owner); C6 (the unsettled generator-preference rival, see Rival below); C7 (the A-cycle-rate assumption, priced inline).

**Rival.** Headline conclusion (recommended sizing): the strongest rival is "trust the stated 1.5 kWh/day figure as given and skip the bottom-up tally," which chain C1 does not fully rule out — it shows 1.5 kWh/day is a defensible lean-case number, not a wrong one — so the rival survives as a live, legitimate alternative for a confirmed-lean household; this is named on C1's own chain as the Abandoned-Reasoning-adjacent caveat (not a formal dead end, since 1.5 kWh/day was not shown to be false, only bracketed). For C3's oversizing cross-check, the rival "size to annual average" is fully ruled out and is recorded as a Dead End in Section 5 (physical-geometry contradiction, GT-3). For C6, the rival "battery-only, no generator" is explicitly live and NOT ruled out — it trails the recommended composite by only 2 weighted points, and the flip test (resilience weight 5→3) shows how little it would take to reverse the ranking; this is carried live on C6's own confidence line and in the Conclusion's trade-offs caveat, per the speculative-chain exception, rather than forced to a false certainty.

**Premise.** It is now 18 months after installation, deep in a January cold spell, and the cabin has already lost power for the first time — the system has failed to keep the lights, fridge, and pump running.

**Causes** (unfiltered, from three stakeholder viewpoints):
*Owner/occupant:* (1) Starlink was added for work-from-cabin and the system was never resized. (2) A space heater or electric kettle was run on the inverter "just this once" during a cold snap. (3) Snow/dust accumulated on the panels for weeks without clearing. (4) A week of houseguests roughly doubled normal load. (5) Nobody monitored the battery closet temperature and it sat well below freezing all week.
*Installer/designer:* (6) The December insolation figure (aggregator-sourced, not the exact site) was optimistic relative to real on-site shading/elevation/tilt. (7) The charge controller or inverter was undersized relative to the array/battery, causing nuisance shutdowns. (8) Wiring voltage-drop losses in practice exceeded the 2% design assumption.
*Adversarial/skeptical-engineer viewpoint:* (9) A multi-day storm produced sustained 20-30% output for 5-7 days — longer than the literal "3-day zero-sun" design threshold — and the battery ran out on day 4 or 5. (10) The battery degraded faster than the 80%-DoD convention assumed, because a misconfigured low-voltage cutoff allowed deeper, more damaging discharges. (11) No generator existed, so when the battery did run low there was no fallback at all.

**Clusters** (structural weaknesses, with chain/GT references):
- **Cluster A — Load creep / hidden loads** (bears on C1, GT-9, GT-10): causes 1, 2, 4.
- **Cluster B — Multi-day low-but-nonzero production exceeds the zero-sun autonomy design** (bears on C2, C6): cause 9.
- **Cluster C — Site/installation shortfall versus the aggregator-sourced design figures** (bears on GT-1, GT-2, C2, C3): causes 3, 6, 7, 8.
- **Cluster D — Battery cold exposure and degradation beyond the 80%-DoD convention** (bears on C4, C5, GT-4, GT-6, GT-7): causes 5, 10.
- **Cluster E — No backup for the residual risk** (bears on C6): cause 11.

**Disposition:**
- Cluster A — **Plan change:** do not add Starlink, a second fridge, or other continuous loads >~200 Wh/day without first re-running C1/C2/C4 at the new load figure; document the commissioning-time energy budget so a later addition is checked against it, not silently absorbed.
- Cluster B — **Plan change:** adopt C6's composite recommendation (keep the C4 battery baseline, add a small emergency-only backup generator) specifically to cover this residual risk; if the owner declines a generator, **accepted risk with named mitigation:** raise autonomy from 3 to 4-5 days instead (battery-only alternative named on C6).
- Cluster C — **Accepted risk with named mitigation:** before final purchase, run the exact site coordinates, elevation, and chosen tilt through PVWatts directly (closing GT-1/GT-2's unreachable-source gap) and keep the already-built-in 10% aging/safety margin rather than removing it to cut cost.
- Cluster D — **Plan change (mandatory, not optional):** locate the battery bank in a conditioned or actively heated enclosure with a BMS low-temperature charge cutoff — this is C5's single highest-leverage recommendation, and the Classified Assumptions Table's A-battery-enclosure row makes explicit that this is a decision the owner has not yet made.
- Cluster E — **Covered by Cluster B's disposition**; no separate action needed.

**Falsification.** This conclusion is false if, under the stated 2.0 kWh/day design load and a properly conditioned battery enclosure, the delivered system (array per C2, battery per C4) cannot sustain that load through a documented worst-case December week at the actual installed site — for example, if first-winter monitoring shows battery state-of-charge reaching the 20% reserve floor before day 3 of a low-sun stretch under normal, non-added-load operation.
## Techniques not applied (process output)

fishbone — not applicable — the assumption space here (solar resource, battery chemistry, load estimate, generator/backup, battery location) was directly enumerable without a multi-causal brainstorm; the inversion check and direct Phase 2 challenge already surfaced the live risks.
theoretical-limit (Phase 1 reframe invocation) — not applicable — the core question is a sizing/engineering-margin decision, not a question of whether a stated figure is an artificial convention masking a higher physical ceiling.
theoretical-limit (Phase 4 invocation) — not applicable — no conclusion here turns on "the ceiling the fundamentals permit once conventions are stripped"; the solar-resource and battery-chemistry figures used are already near-physical/measured values, not conventions worth stripping back further.
inversion (Phase 5 invocation) — not applicable — the Conclusion is a plan/recommendation, not a bare claim, so pre-mortem applies per the decision rule instead (inversion was already used at Phase 2 to challenge the autonomy-threshold and generator assumptions).
## Self-audit scan (process output)

| Chain | Chain Head (brief) | Form conforming? | Rule applied | Dependency clean? | Band | Act attempted? | Edges fired |
|-------|---------------------|-------------------|---------------|--------------------|------|-----------------|-------------|
| C1 | GT-9? (fridge) + GT-10? (Starlink) | yes | n/a | yes | MEDIUM | yes | none |
| C2 | GT-1? (winter PSH) + C1 | yes | n/a | yes | MEDIUM | yes | none |
| C3 | GT-1? + GT-2? (annual PSH) + C1 | yes | n/a | yes | MEDIUM | yes | none |
| C4 | C1 + GT-4 (80% DoD) | yes | n/a | yes | MEDIUM | yes | none |
| C5 | C4 + GT-6? (cold derate) + GT-7? (cold-charge risk) | yes | n/a | yes | MEDIUM | yes | none |
| C6 | GT-1? + C4 | yes | n/a | yes | MEDIUM | yes | none |
| C7 | C4 + GT-4 | yes | n/a | yes | MEDIUM | yes | none |
| C8 | GT-3 + GT-1? | yes | n/a | yes | MEDIUM | yes | none |

| §6 Span (brief) | Construct | Claim under R11? | R11 clause applied | Chain cited |
|-------------------|-----------|-------------------|----------------------|---------------|
| "Recommended approach:" lead-in | bold lead-in | yes | colon closes the bold span, same-line assertion follows | C1, C2, C4, C5 |
| "Key insight:" lead-in | bold lead-in | yes | colon closes the bold span, same-line assertion follows | C5 |
| "Trade-offs acknowledged:" lead-in (generator sentence) | bold lead-in | yes | colon closes the bold span, same-line assertion follows | C6 |
| "Whether this trade-off actually favors a generator depends on..." | prose caveat | yes | caveat qualifying an existing claim; carries the marker `no chain — flagged assumption only` | none — untraced (marked caveat) |
| "Separately, buying roughly 15-20% nameplate battery headroom..." | prose (continuation of Trade-offs claim) | yes | direct entailment / continuation of the same bold-lead-in claim, carries its own citation | C7 |
| "Pre-check:" line | bold lead-in | yes | explicitly named as a claim under the template's Pre-check-is-a-claim note; self-cites its own head | C1, C2, C4, C5, C6, C7 |
| "Confidence:" line | bold lead-in | yes | colon closes the bold span; discharges via the chains D-07 requires it to name | C1, C2, C4, C5, C7 (C6 explicitly excluded per its speculative-chain exception) |

Scan complete: 8 chain rows, one per section-4 chain block in order; 7 section-6 rows, one per construct in order — 7 claims under R11, 0 excluded. 0 chains malformed, 0 claims untraced (1 caveat carries the permitted `no chain — flagged assumption only` marker, which is honest disclosure rather than untraced status for a main claim).
## Self-Audit Gate (process output)

**Criterion 1: Identify Essence**
Quoted span: "What STC-rated PV array wattage and raw/usable LiFePO4 battery-bank kWh are required to reliably carry a year-round, 2-adult off-grid cabin load through the winter design month... starting from a user-supplied ~1.5 kWh/day load estimate that must itself be checked rather than taken as fixed?"
Band: **Rigorous**
Justification: The statement names the specific decision (two concrete outputs, a named design-constraining season, and an explicit instruction to check rather than accept the input load) rather than restating the prompt, and each of the five success criteria names a checkable, structural property of the Conclusion section (e.g., "a range is produced from a derivation chain... not an asserted round number").

**Criterion 2: Challenge Assumptions**
Quoted span (from the Assumption Audit scan): "Audit complete: 24 steps scanned across 8 chains, in order, no step skipped. Two new assumptions surfaced (A-battery-enclosure from C5, A-cycle-rate from C7) and both were added to the Section 2 Assumptions Table with inline `[Assumes: X]` marks left on their originating chain steps."
Band: **Rigorous**
Justification: All 18 table rows use the four-type scheme, Verdict cells carry a leading Accept/Challenge token with an em-dash justification, every chain-consumed unverified assumption reads "unverified — flagged," multiple rows are explicitly Challenged rather than rubber-stamped Accept, and the exhaustive end-of-Phase-4 audit confirms no chain step's assumption escaped the table.

**Criterion 3: Establish Ground Truths**
Quoted span: "`?`-marked: GT-1, GT-2, GT-5, GT-6, GT-7, GT-8, GT-9, GT-10 (8 of 10). Read-at-source: GT-3 — computed directly...; GT-4 — communityarchive.victronenergy.com/questions/10779, cycle-count-vs-DoD table quoted directly." Checking the comparison: the Ground Truths list carries `?` on exactly GT-1, GT-2, GT-5, GT-6, GT-7, GT-8, GT-9, GT-10, and no `?` on GT-3 or GT-4 — the enumeration matches the list exactly.
Band: **Rigorous**
Justification: Every GT carries a stable ID matching the IDs used in section 4, a provenance label, and a citation more specific than "common knowledge"; the `?` enumeration is checked against the list and matches; no chain in this analysis is rated HIGH, so the "every unsuffixed GT feeding a HIGH chain names a read-at-source location" requirement is vacuously satisfied; no Phase-2-discarded assumption appears in this list.

**Criterion 4: Reason Upward**
Quoted span (from the Self-audit scan's chain-form table): all 8 rows read "Form conforming? = yes," "Rule applied = n/a," "Dependency clean? = yes," matched against Section 5's three Dead-End entries, each with a specific, non-generic abandonment reason ("contradicts GT-3's physical-geometry fact," "systematically understates what a properly tilted off-grid array actually collects," "does not strictly dominate" a multi-day low-production event).
Band: **Rigorous**
Justification: Every conclusion has exactly one chain with a genuine intermediate step, every chain is rendered in the prescribed arrow-led one-hop-per-line form with no leading-GT-identifier or premature-sentence-closing violations (confirmed by direct grep of the working file), Abandoned Reasoning documents three specific dead ends rather than using the escape valve, no analogy stands as unsupported direct evidence, and both surfaced assumptions carry inline `[Assumes: X]` marks.

**Criterion 5: Validate**
Quoted span: "C6 [Speculative]... the claim this chain supports (which generator strategy to adopt) is not load-bearing for the headline PV-array/battery-capacity conclusion, which stands on C2/C3/C4/C5 regardless of how the generator question is resolved" and the Adversarial pass record's five clusters, each carrying a named plan change or an explicitly accepted risk with a named mitigation.
Band: **Rigorous**
Justification: Every chain's confidence line names its own `GT-N?` inputs with a verification path or points to a cited chain's own explanation without re-deriving it; every chain is rated no higher than the lowest-rated chain its head cites (verified by direct inspection: C2/C3/C4/C6/C7 all cite C1 or C4, both MEDIUM, and are themselves MEDIUM); the one EXCEPT clause used (C6, speculative) is explicitly claimed with its required evidence; the overall Conclusion's MEDIUM rating matches its weakest non-excepted contributing chain; and the adversarial (pre-mortem) pass record is complete, with every cluster carrying a named disposition.

**Criterion 6: Conclusion-to-Ground-Truth Traceability**
Quoted span (from the Self-audit scan's claim-inventory table): "Scan complete: 8 chain rows... 7 section-6 rows... 7 claims under R11, 0 excluded. 0 chains malformed, 0 claims untraced."
Band: **Rigorous**
Justification: Every Conclusion-section claim traces to a named section-4 chain inline, the one caveat not citing a chain carries the permitted `no chain — flagged assumption only` marker rather than being left bare, no claim introduces reasoning absent from section 4, and the Key Insight (battery-location leverage exceeding any single efficiency assumption) is a distinct, non-obvious finding rather than a restatement of the Recommended Approach's wattage/kWh figures.

**Gate result:** cleared · passes: 1 · Fix/Repeat fired: no
## Structured summary (process output)

```json
{
  "schema_version": 1,
  "run_mode": "full-composer",
  "assumptions": [
    {"id": "A-1", "type": "untested belief", "verdict": "Accept"},
    {"id": "A-2", "type": "physical law", "verdict": "Accept"},
    {"id": "A-3", "type": "untested belief", "verdict": "Challenge"},
    {"id": "A-4", "type": "untested belief", "verdict": "Challenge"},
    {"id": "A-5", "type": "convention", "verdict": "Challenge"},
    {"id": "A-6", "type": "convention", "verdict": "Accept"},
    {"id": "A-7", "type": "untested belief", "verdict": "Challenge"},
    {"id": "A-8", "type": "current constraint", "verdict": "Challenge"},
    {"id": "A-9", "type": "current constraint", "verdict": "Challenge"},
    {"id": "A-10", "type": "convention", "verdict": "Challenge"},
    {"id": "A-11", "type": "untested belief", "verdict": "Challenge"},
    {"id": "A-12", "type": "current constraint", "verdict": "Accept"},
    {"id": "A-13", "type": "convention", "verdict": "Challenge"},
    {"id": "A-14", "type": "untested belief", "verdict": "Challenge"},
    {"id": "A-15", "type": "physical law", "verdict": "Accept"},
    {"id": "A-16", "type": "convention", "verdict": "Accept"},
    {"id": "A-17", "type": "convention", "verdict": "Accept"},
    {"id": "A-18", "type": "current constraint", "verdict": "Accept"},
    {"id": "A-19", "type": "untested belief", "verdict": "Challenge"}
  ],
  "ground_truths": [
    {"id": "GT-1", "read_at_source": false},
    {"id": "GT-2", "read_at_source": false},
    {"id": "GT-3", "read_at_source": true},
    {"id": "GT-4", "read_at_source": true},
    {"id": "GT-5", "read_at_source": false},
    {"id": "GT-6", "read_at_source": false},
    {"id": "GT-7", "read_at_source": false},
    {"id": "GT-8", "read_at_source": false},
    {"id": "GT-9", "read_at_source": false},
    {"id": "GT-10", "read_at_source": false}
  ],
  "chains": [
    {"id": "C1", "confidence": "MEDIUM", "rests_on": ["GT-9?", "GT-10?"]},
    {"id": "C2", "confidence": "MEDIUM", "rests_on": ["GT-1?", "C1"]},
    {"id": "C3", "confidence": "MEDIUM", "rests_on": ["GT-1?", "GT-2?", "C1"]},
    {"id": "C4", "confidence": "MEDIUM", "rests_on": ["C1", "GT-4"]},
    {"id": "C5", "confidence": "MEDIUM", "rests_on": ["C4", "GT-6?", "GT-7?"]},
    {"id": "C6", "confidence": "MEDIUM", "rests_on": ["GT-1?", "C4"]},
    {"id": "C7", "confidence": "MEDIUM", "rests_on": ["C4", "GT-4"]},
    {"id": "C8", "confidence": "MEDIUM", "rests_on": ["GT-3", "GT-1?"]}
  ],
  "dead_ends": [
    "Sizing the PV array to annual-average insolation",
    "Using the 1970s NREL West Solar Monitoring Network's global-horizontal December figure (≈2.6-2.95 kWh/m²/day) as GT-1",
    "Treating the stated \"3 days of literal zero sun\" autonomy spec as a complete, self-sufficient risk model"
  ],
  "techniques": {
    "applied": ["inversion", "estimate", "trade-off", "second-order", "five-whys", "pre-mortem"],
    "not_applied": [
      {"technique": "fishbone", "phase": 2, "reason": "the assumption space here (solar resource, battery chemistry, load estimate, generator/backup, battery location) was directly enumerable without a multi-causal brainstorm; the inversion check and direct Phase 2 challenge already surfaced the live risks"},
      {"technique": "theoretical-limit", "phase": 1, "reason": "the core question is a sizing/engineering-margin decision, not a question of whether a stated figure is an artificial convention masking a higher physical ceiling"},
      {"technique": "theoretical-limit", "phase": 4, "reason": "no conclusion here turns on the ceiling the fundamentals permit once conventions are stripped; the solar-resource and battery-chemistry figures used are already near-physical/measured values, not conventions worth stripping back further"},
      {"technique": "inversion", "phase": 5, "reason": "the Conclusion is a plan/recommendation, not a bare claim, so pre-mortem applies per the decision rule instead"}
    ]
  },
  "gate": {
    "passes": [
      {
        "bands": ["Rigorous", "Rigorous", "Rigorous", "Rigorous", "Rigorous", "Rigorous"],
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
    "recommendation": "Design the PV array to roughly 700-800 W STC and the battery bank to roughly 7.5-8 kWh nameplate / 6.0 kWh usable, against a recommended 2.0 kWh/day design load (not the stated 1.5 kWh/day) with no satellite internet, assuming the battery bank is located in a temperature-conditioned enclosure (chain C2, chain C4, chain C5); if satellite internet is wanted, rescale both numbers using the same formulas against a ≈3.5 kWh/day design load instead (chain C1).",
    "confidence": "MEDIUM",
    "rests_on": ["C1", "C2", "C4", "C5", "C7", "C6"]
  }
}
```
