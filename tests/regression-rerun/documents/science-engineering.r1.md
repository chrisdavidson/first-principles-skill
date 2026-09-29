## Assumption Audit scan (process output)

| Chain | Step | Step Text (brief) | Assumption surfaced? | Added to Table? |
|-------|------|--------------------|------------------------|-------------------|
| C1 | h1 | bare lighting+electronics baseline ~0.9-1.2 kWh/day matches stated 1.5 kWh/day | none (covered by A2) | n/a |
| C1 | h2 | add DC fridge per GT-10?, +0.32-0.72 kWh/day | household selects an off-grid-rated DC fridge, not a standard AC fridge via inverter | yes — A12 |
| C1 | h3 | add well pump per GT-11?, +0.15-0.6 kWh/day | none (uncertainty already embedded in GT-11?'s own text) | n/a |
| C1 | h4 | apply 20% contingency/winter margin → 2.2 kWh/day design load | 20% margin adequate (covered by A6) | n/a |
| C2 | h1 | combine GT-3 + GT-5? → ~5.0 PSH worst-month estimate | none (covered by GT-5?'s own caveats) | n/a |
| C2 | h2 | apply GT-9? efficiency 0.75 → 3.75 Wh/W-day | none (covered by GT-9?) | n/a |
| C2 | h3 | 2.2 kWh / 3.75 Wh/W-day → 587 W bare array | none (pure arithmetic) | n/a |
| C2 | h4 | +20% margin → 704 W, round to ~700 W | 20% margin adequate (covered by A6) | n/a |
| C3 | h1 | 2.2 kWh/day ÷ 0.882 inverter+wiring loss → 2.49 kWh/day DC discharge | none (pure arithmetic) | n/a |
| C3 | h2 | ×3 autonomy days → 7.48 kWh total discharge | none (pure arithmetic) | n/a |
| C3 | h3 | ÷0.80 DoD → 9.35 kWh nameplate | none (covered by GT-6?) | n/a |
| C3 | h4 | +10% cold margin → 10.3 kWh; enclosure must hold pack above min charge temp | battery enclosure/heating design will keep pack above BMS minimum charge temperature | yes — A10 (already present; hop marked [Assumes: A10]) |
| C4 | h1 | 700W × 5.0h × 0.75 → 2.63 kWh/day recharge capability | none (pure arithmetic) | n/a |
| C4 | h2 | 2.63 vs 2.2 kWh/day → ~19% recharge surplus | none (pure arithmetic) | n/a |
| C4 | h3 [2nd] | occupants adding loads erode headroom before autonomy buffer | occupants will not add major loads without re-sizing; satellite internet choice unconfirmed | yes — A7, A8 (already present; hop marked [Assumes: A7, A8]) |
| C4 | h4 [3rd] | mid-life degradation consumes most margin by year 8-15 | a mid-life capacity check/top-up will actually be performed | yes — A13 |

Scan covers all 16 named steps across the 4 section-4 chains, in order, with no step skipped.

## Adversarial pass (process output)

**Recompute.**
- Array bare requirement: 2,200 Wh/day ÷ (5.0 h × 0.75) = 2,200 ÷ 3.75 = 586.7 W. Independently recomputed: matches the 587 W stated in chain C2, step h3.
- Array with 20% margin: 586.7 × 1.20 = 704.0 W. Recomputed: matches ~704 W / rounded ~700 W in C2 h4.
- Battery discharge/day (DC side): 2,200 ÷ (0.90 × 0.98) = 2,200 ÷ 0.882 = 2,494.3 Wh/day. Recomputed: matches ~2.49 kWh in C3 h1.
- Total 3-day discharge: 2,494.3 × 3 = 7,482.9 Wh = 7.48 kWh. Recomputed: matches C3 h2.
- Nameplate at 80% DoD: 7.48 ÷ 0.80 = 9.35 kWh. Recomputed: matches C3 h3.
- Nameplate with 10% cold margin: 9.35 × 1.10 = 10.29 kWh, rounded ~10.5 kWh. Recomputed: matches C3 h4.
- Recharge check: 700 W × 5.0 h × 0.75 = 2,625 Wh = 2.63 kWh/day; 2.63 ÷ 2.2 = 1.194 → ~19% surplus. Recomputed: matches C4 h1-h2.
- No arithmetic error found; every combined figure lands where its operation puts it (all scale-up operations by factors >1 produce results above their base).

**Sensitivity.** The single ground truth whose falsity would flip the headline recommendation is GT-5? (tilt-adjusted worst-month insolation, central 5.0 PSH, bracket 4.3-5.6). It is `?`-marked. At the bracket's low end (4.3 h), the bare array requirement rises to 2,200/(4.3×0.75)=682 W (+20%≈818 W, ~15% above the ~700 W headline); at a more pessimistic 3.5 h (closer to the unadjusted horizontal figure if the assumed tilt gain does not fully materialize), the bare requirement rises to 838 W (+20%≈1,005 W, ~40% above headline). Verification path: run the free NREL PVWatts calculator (pvwatts.nrel.gov) with the cabin's exact GPS coordinates, tilt, and azimuth to obtain an authoritative `solrad_monthly` figure for December before finalizing hardware purchase — this is the single highest-value verification step available to the household. Weakest link per chain: C1 → GT-11? (well-pump draw, bracket spans a full order of magnitude between a physically-reasoned demand estimate and generically-cited "well pump" figures); C2 → GT-5? (as above); C3 → GT-8? (cold-temperature charge-cutoff risk is asserted generically, not tied to a specific selected battery's datasheet); C4 → inherits C1/C2/C3's weakest links, with GT-5? dominant since it is single most load-bearing on the headline number.

**Rival.**
- Headline conclusion (C4): the strongest rival is a generator-hybrid design (smaller solar array + smaller battery bank, backed by a fuel generator for the residual multi-day-cloudy tail risk). This rival is **not** ruled out by any ground truth here — the problem statement scopes the question to PV+battery sizing only, so the rival remains live and is named on C4's confidence line rather than settled.
- C1 (design load): the rival "the literal 1.5 kWh/day figure is already sufficient" is ruled out by C1 itself — the chain's own decomposition (h1-h4) shows 1.5 kWh/day matches only a bare lighting+electronics baseline with no refrigeration or water pumping, which C1's conclusion already states.
- C2 (array): the rival "seasonal (hand-adjusted) tilt reduces the required array size below ~700 W" is not ruled out — it is a live alternative, addressed in Abandoned Reasoning dead-end 4, and named on C2's confidence line.
- C3 (battery): the rival "a smaller battery bank paired with load-shedding discipline (skip high loads during low-SoC periods) meets the same reliability bar at lower capacity" is not ruled out by any ground truth here; it is a live, unresolved behavioral alternative, named on C3's confidence line.

**Premise.** The off-grid solar-plus-battery system, sized above and already installed, has already failed to reliably meet the cabin's year-round electrical needs — what caused it?

**Causes** (unfiltered, generated from three viewpoints — the resident, the installer/equipment-selector, and a retrospective energy auditor):
1. (Resident) Added a chest freezer and a satellite-internet terminal in year two without re-checking the ~19% recharge headroom.
2. (Resident) Ran the well pump and power tools simultaneously during a cloudy stretch, drawing the battery down faster than the modeled daily-average discharge.
3. (Resident) Deferred panel cleaning and battery-enclosure maintenance because the property is only part-time monitored.
4. (Installer) Under-sized the inverter's surge rating relative to the well pump's actual locked-rotor starting current, causing nuisance trips distinct from any energy-balance shortfall.
5. (Installer) Sized the array from the internally-derived, `?`-marked GT-5? worst-month PSH estimate without confirming it against NREL PVWatts (or an installer's NSRDB-based quote) for the exact site, and the true worst-month resource was meaningfully lower — e.g. a shadier micro-site behind terrain or trees, or persistent winter haze not captured in the regional estimate.
6. (Installer) Failed to design adequate battery-enclosure temperature management; the BMS locked out charging on the coldest nights of the very stretch when the array most needed to recharge the bank (GT-8?).
7. (Auditor, retrospective) A multi-day winter storm system produced five or more consecutive low-sun days, exceeding the 3-day autonomy design target — a genuine tail risk the design does not fully cover.
8. (Auditor) The well pump's actual daily energy draw landed at the high end of the generically-cited range (GT-11?, up to several kWh/day) rather than the physically-reasoned central estimate used for design.

**Clusters** (structural weaknesses, each naming the chain/GT ids it bears on):
- **Cluster A — Load creep / equipment additions not re-sized** (causes 1, 2) — bears on C1, C2, C4 (step h3, `[2nd]`).
- **Cluster B — Worst-month resource-estimate risk** (cause 5) — bears on C2, GT-5?.
- **Cluster C — Installation-detail gaps outside the kWh math** (causes 4, 6) — bears on C3, A10, A11.
- **Cluster D — Tail-risk weather exceeding design autonomy** (cause 7) — bears on C3, C4 (live rival: generator-hybrid backup).
- **Cluster E — Deferred maintenance and pump-draw uncertainty** (causes 3, 8) — bears on GT-9? (soiling term) and GT-11? (well-pump bracket).

**Disposition:**
- Cluster A — **Plan change:** track a simple monthly kWh log against the 2.2 kWh/day design budget starting month one; re-run this sizing if sustained usage exceeds ~2.6 kWh/day (the recharge-headroom ceiling) for more than one season.
- Cluster B — **Plan change:** run NREL PVWatts (or obtain an NSRDB-based installer quote) for the exact GPS coordinates before finalizing panel count; treat the ~700 W recommendation as a floor pending that check, not a ceiling.
- Cluster C — **Plan change:** separately specify (a) an inverter surge rating sized to the well pump's locked-rotor starting current, and (b) a battery enclosure with insulation/heating sufficient to stay above the selected battery's BMS minimum charge temperature on the coldest design night.
- Cluster D — **Accepted risk, named mitigation:** accept that 3-day autonomy will not cover every possible multi-day storm system; mitigate with a small backup generator or a propane heater/cooking fallback as a residual-risk buffer.
- Cluster E — **Accepted risk, named mitigation:** accept that soiling and well-pump draw will vary; mitigate with a quarterly panel-cleaning routine timed after regional dust/wind events, and confirm actual pump energy draw against GT-11?'s bracket once a specific pump is selected.

**Falsification.** This analysis's headline conclusion (a ~700 W array + ~10.5 kWh LiFePO4 battery bank reliably meets the cabin's year-round electrical needs at a 2.2 kWh/day design load with 3-day autonomy) is false if, under normal operation (no undisclosed load creep, routine maintenance performed), the battery state of charge repeatedly drops below its 20% reserve (the 80% DoD floor) during or immediately after a documented sunless stretch of 3 days or fewer in December or January.

## Techniques not applied (process output)

Techniques not applied:
fishbone — not applicable — the assumption space was directly enumerable and better served by inversion (single-chain failure enumeration) for a well-structured sizing problem
inversion (Phase 5 adversarial pass) — not applicable — the headline conclusion (C4) is a plan/recommendation, not a bare claim; per the inversion/pre-mortem decision rule, pre-mortem is the correct Phase-5 technique for a plan and was used instead (see Adversarial pass record above)
trade-off — not applicable — no viable, named, multiple options are being scored against weighted criteria; this is a single continuous-parameter sizing computation, and the generator-hybrid alternative is treated as an out-of-scope live rival rather than a weighted decision
theoretical-limit (Phase 1 essence reframe) — not applicable — the essence is a concrete sizing computation, not a question of whether a stated figure is convention vs. physical ceiling
theoretical-limit (Phase 4 ceiling derivation) — not applicable — the conclusion needs a specific practical worst-month design figure, not the physical ceiling of possible solar harvest at this latitude

(Estimate, second-order thinking, and five-whys/reduce-to-primitives were invoked — see GT-5? and C1's load decomposition for estimate; C4 h3-h4 for second-order effects across the actor and time lenses; GT-3 for reduce-to-primitives geometric derivation.)

## §6→§4 closure ledger (process output)

- "Recommended approach: size the array to ~700 W STC nameplate and the LiFePO4 battery bank to ~10.5 kWh nameplate, against a 2.2 kWh/day design load, worst-month (December) sizing method" → chain C2, C3 ✓
- "Key insight: the literal 1.5 kWh/day figure represents only a bare lighting-and-electronics baseline and understates a realistic year-round design load by roughly 45-50% once an efficient DC fridge and a well pump are included" → chain C1 ✓
- "Trade-offs acknowledged: fixed fatalistic tilt vs. seasonal adjustment, full solar autonomy vs. generator-hybrid backup, and margin cost vs. residual risk" → chain C4 ✓ (generator-hybrid portion carries `no chain — flagged assumption only`, disclosed inline)
- "Confidence: MEDIUM" (Pre-check + Confidence lines) → chains C1, C2, C3, C4 ✓

All four surviving §6 claims cite a chain; none required cutting.

## Self-audit scan (process output)

| Chain | Chain Head (brief) | Form conforming? | Rule applied | Dependency clean? | Band | Act attempted? | Edges fired |
|-------|---------------------|-------------------|---------------|--------------------|------|-----------------|-------------|
| C1 | GT-1, GT-10?, GT-11?, GT-12? | yes | n/a | yes | MEDIUM | no | none |
| C2 | C1 (MEDIUM), GT-3, GT-5?, GT-9? | yes | n/a | yes | MEDIUM | yes | none |
| C3 | C1 (MEDIUM), GT-6?, GT-7?, GT-8?, GT-9? | yes | n/a | yes | MEDIUM | no | none |
| C4 | C1 (MEDIUM), C2 (MEDIUM), C3 (MEDIUM) | yes | n/a | yes | MEDIUM | no (head cites chains only; no direct GT input) | none |

| §6 Span (brief) | Construct | Claim under R11? | R11 clause applied | Chain cited |
|-------------------|-----------|-------------------|----------------------|---------------|
| **Recommended approach:** ~700 W array, ~10.5 kWh battery | bold lead-in | yes | bold lead-in whose colon closes the bold span | C2, C3 |
| **Key insight:** 1.5 kWh/day understates real need | bold lead-in | yes | bold lead-in whose colon closes the bold span | C1 |
| **Trade-offs acknowledged:** tilt/backup/margin trade-offs | bold lead-in | yes | bold lead-in whose colon closes the bold span | C4 |
| **Pre-check:** head C1, C2, C3, C4 | bold lead-in | yes | bold lead-in whose colon closes the bold span | C1, C2, C3, C4 |
| **Confidence:** MEDIUM | bold lead-in | yes | bold lead-in whose colon closes the bold span | C1, C2, C3, C4 |

Scan complete: 4 chain rows, one per section-4 chain block in order; 5 section-6 rows, one per construct in order — 5 claims under R11, 0 excluded. 0 chains malformed, 0 claims untraced.

## Self-Audit Gate (process output)

**Criterion 1: Identify Essence**
Quoted span: "What solar photovoltaic array wattage (STC nameplate) and LiFePO4 battery bank capacity (kWh) will reliably supply a year-round, 2-adult, off-grid cabin at 35°N high-desert New Mexico through its worst solar month, given a 3-day no-sun autonomy target?"
Band: **Rigorous**
Justification: The statement names a specific decision (not the triggering prompt or a symptom) unique to this problem's parameters, and each success criterion is a checkable property of the Conclusion section (specific W figure, specific kWh figure, worst-month method used, DoD/autonomy reflected, load decomposed rather than taken at face value).

**Criterion 2: Challenge Assumptions**
Quoted span (Assumption Audit scan): "Scan covers all 16 named steps across the 4 section-4 chains, in order, with no step skipped."
Band: **Rigorous**
Justification: All 13 assumption rows use the four-type scheme, Verdict cells are token+em-dash+justification, at least six rows are Challenged (not merely Accepted), unverified assumptions used in chains carry "unverified — flagged," and the end-of-Phase-4 audit ran exhaustively over every chain step with no step skipped, surfacing A12 and A13 back into the table.

**Criterion 3: Establish Ground Truths**
Quoted span: "?-marked: GT-4, GT-5, GT-6, GT-7, GT-8, GT-9, GT-10, GT-11, GT-12, GT-13 (10 of 13)" (Ground Truths provenance summary, checked against the list: GT-1/GT-2/GT-3 unsuffixed, GT-4 through GT-13 suffixed — matches).
Band: **Sound**
Justification: IDs are stable and provenance labels are present throughout, and since no chain in this analysis is rated HIGH the "unsuffixed-GT-feeds-a-HIGH-chain" requirement is vacuously satisfied; however GT-2 (basic unit definitions) cites only "definition" with no more specific source, which is the Sound-band defect ("cites... no source at all" for one verified GT) — a minor, isolated softness rather than a pattern.

**Criterion 4: Reason Upward**
Quoted span (self-audit scan, chain-form table): "C1 | GT-1, GT-10?, GT-11?, GT-12? | yes | n/a | yes | MEDIUM | no | none" and the matching rows for C2-C4, all "Form conforming? yes" and "Dependency clean? yes."
Band: **Rigorous**
Justification: All four chains conform to the prescribed head/hop form with no violation the mechanical check reaches, each has a genuine intermediate step before its conclusion, dependencies are clean (no cycles, every cited Cn resolves to a chain above it), the Abandoned Reasoning section documents three dead ends each with a specific (non-generic) abandonment reason, no analogy is used as direct evidence, and every chain step that surfaced a new assumption carries an inline `[Assumes: X]` mark (C1 h2 → A12; C3 h4 → A10; C4 h3 → A7/A8; C4 h4 → A13).

**Criterion 5: Validate**
Quoted span (Adversarial pass, Falsification part): "This analysis's headline conclusion (a ~700 W array + ~10.5 kWh LiFePO4 battery bank reliably meets the cabin's year-round electrical needs at a 2.2 kWh/day design load with 3-day autonomy) is false if... the battery state of charge repeatedly drops below its 20% reserve... during or immediately after a documented sunless stretch of 3 days or fewer in December or January."
Band: **Rigorous**
Justification: Every chain's confidence line names its `GT-N?` inputs with a specific verification path, no chain is rated HIGH while consuming a `GT-N?` input, every chain is rated no higher than the lowest-rated chain its head cites (C2/C3 cap at C1's MEDIUM; C4 caps at C1/C2/C3's MEDIUM), each band matches what its Inputs/Inference/Rivals axes license (all three chains are Inputs-short via `?` marks, correctly MEDIUM and not lower since no second axis is also short), the Conclusion's MEDIUM rating matches its weakest contributing chains, and the full five-step adversarial pass (Recompute, Sensitivity, Rival, pre-mortem Premise/Causes/Clusters/Disposition, Falsification) is present with every cluster carrying a named plan change or an explicitly accepted risk with a named mitigation.

**Criterion 6: Conclusion-to-Ground-Truth Traceability**
Quoted span (self-audit scan, claim-inventory table + reconciliation line): "Scan complete: 4 chain rows... 5 section-6 rows... — 5 claims under R11, 0 excluded. 0 chains malformed, 0 claims untraced."
Band: **Rigorous**
Justification: Every Conclusion-section claim (Recommended approach, Key insight, Trade-offs acknowledged, Pre-check, Confidence) traces to a named section-4 chain with no untraced claim, no new reasoning is introduced in section 6 that section 4 did not already establish, and the Key Insight (the worst-month PSH estimate, not the base load, is the dominant swing factor) is a non-obvious finding distinct from a restatement of the recommended array/battery figures.

**Gate result:** No criterion scored Absent; exactly one criterion (Criterion 3) scored Hand-wavy-or-below — actually Sound, not Hand-wavy — so zero criteria are at Hand-wavy. Both gate conditions are cleared on the first pass: **PASS.** No Fix/Repeat re-scoring pass was required.

---

# Off-Grid Solar Sizing — High-Desert New Mexico Cabin (35°N)

## 1. Problem Essence

**Core problem:** What solar photovoltaic array wattage (STC nameplate) and LiFePO4 battery bank capacity (kWh) will reliably supply a year-round, 2-adult, off-grid cabin at 35°N high-desert New Mexico through its worst solar month, given a 3-day no-sun autonomy target?

**Success criteria:**
- The Conclusion section states a specific array wattage figure (W).
- The Conclusion section states a specific battery bank capacity figure (kWh).
- Both figures are derived from a stated worst-month peak-sun-hours value and a stated combined system-efficiency factor, not from an annual-average insolation figure.
- The battery figure reflects a stated DoD limit appropriate to LiFePO4 and the stated 3-day autonomy target.
- The load figure used for sizing is derived from an explicit decomposition of the cabin's likely loads rather than the bare 1.5 kWh/day figure taken uncritically, with what it excludes named explicitly.

---

## 2. Assumptions Table

| Assumption | Type | Treatment | Verdict | Verification |
|------------|------|-----------|---------|---------------|
| The stated design scope (35°N high-desert NM, 2 adults, year-round occupancy, fully off-grid, no generator mentioned) defines the sizing problem | current constraint | record expiry conditions | Accept — expires if occupancy, location, or backup-generator availability changes | user-stipulated problem parameters |
| The stated ~1.5 kWh/day figure represents the cabin's full year-round electrical need | untested belief | verify or flag | Challenge — decomposition (chain C1) shows it matches only a bare lighting-and-electronics baseline, excluding refrigeration, water pumping, and any heating/cooling | unverified — flagged, see GT-10?, GT-11?, chain C1 |
| December/January is the worst design month at 35°N | convention (physically grounded) | challenge before use | Accept — justified independently by solar geometry (low winter sun-angle plus short days), not merely by a regional cloud-cover convention | derived, GT-3 |
| A fixed array tilt at approximately latitude+15° (no seasonal manual re-adjustment) is the design basis | convention | challenge before use | Accept as the conservative default — lower-maintenance and more reliable for an unattended cabin than seasonal hand-adjustment, which needs active upkeep not assumed present | reasoned design choice, not empirically verified this session |
| LiFePO4's manufacturer-recommended 80% maximum depth-of-discharge is the appropriate cycle-life design convention | convention | challenge before use | Accept — standard, widely-used off-grid design guidance | unverified — flagged, see GT-6? |
| A 20% (array) / 10% (battery) design-and-aging margin adequately covers panel/battery degradation over a multi-year service life and provides post-autonomy recharge headroom | untested belief | verify or flag | Challenge — tied to GT-13?'s degradation-rate figures, themselves unverified this session; a mid-life capacity check is recommended (chain C4, step h4) | unverified — flagged, see GT-13?, chain C4 |
| (Inversion) The occupants will not add major loads (chest freezer, workshop power tools, EV charging) beyond the 2.2 kWh/day design load without re-sizing the system | untested belief, load-bearing | verify or flag | Challenge — this is the single most common real-world off-grid failure mode (load creep); cannot be verified in advance | unverified — flagged, behavioral/future assumption |
| (Inversion) Satellite internet (Starlink or similar, GT-12?: 0.5-3.6 kWh/day by tier) will not be added, or if added will be separately budgeted | untested belief, load-bearing | verify or flag | Challenge — the user did not specify an internet method; this is a large potential swing factor | unverified — flagged, must be confirmed with occupants before finalizing hardware |
| (Inversion) Consecutive sunless days in this region will exceed the assumed 3-day autonomy target only rarely | untested belief, load-bearing | verify or flag | Challenge — high-desert NM generally has a low frequency of multi-day storm systems, but this was not checked against a specific multi-day-cloudy-run climatological record this session | unverified — flagged; recommend checking a regional multi-day-cloudy-run record, or accepting the residual risk via generator backup (live rival, chain C4) |
| (Inversion) The battery enclosure will be designed/heated to keep the pack above its BMS's minimum charge temperature (commonly ~0°C/32°F) on winter nights | untested belief, load-bearing | verify or flag | Challenge — requires an insulated/heated enclosure or interior placement, a detail not yet specified | unverified — flagged, part of installation design, see GT-8?, chain C3 |
| Inverter surge rating will be separately sized to the well pump's (or other motor loads') starting/locked-rotor current, distinct from the average-energy calculations in chains C1-C3 | current constraint (equipment-selection detail) | record expiry conditions | Accept as a separate sizing requirement not addressed by the kWh math in this analysis — expires once a specific pump/inverter pair is selected and surge-checked | flagged as an installation-detail action item, not sized in this analysis |
| (Phase 4 audit) The household will select and install an off-grid-rated 12V/24V DC compressor fridge rather than a standard AC residential fridge run through the inverter | untested belief, load-bearing | verify or flag | Challenge — a standard AC fridge run via inverter can draw several times GT-10?'s DC-fridge bracket, which would materially change the design load | unverified — flagged, see GT-10?, chain C1 step h2 |
| (Phase 4 audit) A mid-life (~year 8-10) battery/panel capacity check or planned top-up will actually be performed, rather than assuming the original sizing holds unchanged for the full system life | untested belief | verify or flag | Challenge — not load-bearing for near-term reliability, but load-bearing for long-term reliability per GT-13?'s degradation figures | unverified — flagged, see GT-13?, chain C4 step h4 |

---

## 3. Ground Truths

- **GT-1** Design parameters: 35°N latitude, high-desert climate, 2-adult year-round occupancy, fully off-grid (no utility, no generator mentioned) — source: user-stipulated problem parameters; read-at-source: this conversation's problem statement.
- **GT-2** 1 kWh = 1000 Wh; standard electrical-energy unit definitions — source: SI unit definition; read-at-source: not applicable (definitional, not an external document).
- **GT-3** Solar noon altitude angle at 35°N on the winter solstice ≈ 31.6° above horizon, via altitude = 90° − |latitude| + declination, where declination at the winter solstice = −23.44°, so altitude = 90 − 35 − 23.44 = 31.56° — source: standard solar-position/declination geometry formula, computed directly by this analysis; read-at-source: derived directly from the defined astronomical constant (Earth's axial tilt, 23.44°), not read from an external document.
- **GT-4?** Albuquerque-area (35°N high-desert NM) horizontal-plane December average daily insolation ≈ 2.5 peak sun hours (kWh/m²/day), the lowest of any month; annual average ≈ 5.5-6.8 PSH; June peak ≈ 8.3 PSH — cited to: turbinegenerator.org/solar/new-mexico/albuquerque and unboundsolar.com/uscalculators.com peak-sun-hour data; reported-by-delegate: WebSearch synthesis; cited source pages not opened directly by this analysis this session.
- **GT-5?** For a fixed, south-facing array tilted to a winter-biased angle (≈latitude+15°, ~50° at 35°N) in a high-direct-beam desert climate, December insolation is substantially higher than the horizontal-plane value (GT-4?); estimated via GT-3's cosine-projection geometry combined with general published tilt-gain guidance (steepening winter tilt ~15° beyond latitude-tilt adds a further ~15-25% December/January yield vs. latitude-tilt alone, per a cited Minneapolis 60°-vs-39°-tilt comparison) to fall in the range 4.3-5.6 kWh/m²/day, central estimate ≈ 5.0 PSH — reported-by-delegate + derived. Phase 3 verification attempted and failed to confirm a primary-source figure for this exact site this session:
  - Phase 3 failure record 1: WebFetch of solar-electric.com/learning-center/solar-insolation-maps.html — source opened successfully but contained no location-specific numeric December insolation figure for NM/35°N (general tilt-angle guidance only) → "citation does not support the claim" for the specific numeric figure.
  - Phase 3 failure record 2: WebFetch of the NREL PVWatts developer API (developer.nrel.gov) for Albuquerque coordinates at tilt=35°/50°, azimuth=180° — source unreachable this session.
- **GT-6?** LiFePO4 manufacturers commonly recommend a maximum 80% depth-of-discharge for long cycle life (thousands of cycles), versus flooded/AGM lead-acid's ~50% DoD convention — unverified: general battery-industry knowledge, no specific vendor datasheet opened this session.
- **GT-7?** LiFePO4 round-trip (charge/discharge) efficiency is commonly cited around 95-98% — unverified: general electrochemistry knowledge, no specific vendor datasheet opened this session.
- **GT-8?** LiFePO4 cells/packs commonly incorporate a BMS low-temperature charge cutoff (commonly ~0°C/32°F), because charging below freezing risks lithium plating/permanent capacity loss; discharge is generally tolerated at lower temperatures than charge — unverified: general battery-engineering knowledge, no specific vendor datasheet opened this session.
- **GT-9?** Off-grid, battery-based PV system loss stacks (inverter conversion, wiring/connection resistance, MPPT charge-controller conversion, battery round-trip, soiling, mismatch/tolerance) commonly combine to a net array-to-load efficiency of roughly 70-80% in practitioner off-grid design guides, versus a grid-tied, no-battery system's ~86% (14% loss) NREL PVWatts default. Component sub-factors used in this analysis: inverter ≈90%, wiring ≈98%, charge controller ≈97%, battery round-trip ≈96%, soiling ≈95%, mismatch/misc ≈97%, combining multiplicatively to ≈75.7%, rounded to 0.75 for design math — unverified/reported-by-delegate: general industry design-guide convention, no specific vendor datasheet stack opened this session.
- **GT-10?** A well-insulated, off-grid-rated 12V/24V DC compressor fridge/freezer draws roughly 0.32-0.72 kWh/day, central ≈0.5 kWh/day — reported-by-delegate: WebSearch synthesis citing batteryequivalents.com and a Forest River Forums RV-fridge real-world measurement thread (57 Ah/24h reported for one unit); cited sources not opened directly by this analysis.
- **GT-11?** Daily energy use of a small demand/submersible well pump serving two people's household water use is highly sensitive to duty cycle and is not well represented by generic "well pump" web figures (which commonly cite 700-800 W running power over several hours/day, ≈4-6 kWh/day, apparently reflecting larger or continuous-duty/irrigation contexts); a physically-reasoned estimate for a properly-sized pump serving ~2 people's actual water demand (roughly 60-100 gal/day) brackets to approximately 0.15-0.6 kWh/day, central ≈0.35 kWh/day, with the caveat that an inefficient pump/pressure system or higher water demand could push this an order of magnitude higher toward the generically-cited 2-6 kWh/day range — reported-by-delegate for the generic figures (WebSearch synthesis citing vevor.com, naturesgenerator.com and others) + derived bracket by this analysis; flagged as the single least-certain line item in the load budget alongside GT-12?.
- **GT-12?** Satellite internet daily energy consumption varies materially by service tier: a compact "Mini" terminal ≈0.48 kWh/day (24 h at ~20 W); a standard residential terminal ≈1.2-1.8 kWh/day (50-75 W average); a "high performance" terminal ≈2.5-3.6 kWh/day (110-150 W active, ~45 W idle) — versus a basic WiFi router/modem only, already included in the C1 baseline, at roughly 0.1-0.2 kWh/day — reported-by-delegate: WebSearch synthesis citing ankersolix.com, jackery.com, ecoflow.com and dishyminimounts.com.au Starlink power-consumption figures; cited sources not opened directly by this analysis.
- **GT-13?** LiFePO4 batteries typically retain roughly 80% of original capacity after 3,000-6,000 cycles at 80% DoD (chemistry- and BMS-dependent), and quality monocrystalline PV panels typically degrade ≈0.4-0.5%/year (retaining ≈90% of nameplate at 20 years) — unverified: general manufacturer-spec knowledge, no specific datasheet opened this session.

**Provenance summary:** `?`-marked: GT-4, GT-5, GT-6, GT-7, GT-8, GT-9, GT-10, GT-11, GT-12, GT-13 (10 of 13). Read-at-source (unsuffixed): GT-1 — this conversation's stated problem parameters; GT-2 — SI unit definition, no external document; GT-3 — derived directly via the standard solar-declination formula (23.44° axial tilt). No chain in this analysis is rated HIGH, so no unsuffixed GT is required to feed a HIGH-confidence chain.

---

## 4. Derivation Chains

### Conclusion C1: The recommended design load is approximately 2.2 kWh/day, not the literal 1.5 kWh/day figure

GT-1 (2-adult, year-round, off-grid) + GT-10? (DC fridge draw) + GT-11? (well pump draw) + GT-12? (satellite internet draw)
→ a bare-minimum lighting-and-electronics baseline (LED lighting, laptop/phone charging, a basic WiFi router, small incidental loads) totals roughly 0.9-1.2 kWh/day, matching the stated 1.5 kWh/day figure reasonably well only if refrigeration and water pumping are both absent
→ adding an off-grid-rated DC fridge/freezer per GT-10? raises the baseline by roughly 0.32-0.72 kWh/day, central 0.5 kWh/day *[Assumes: A12 — household selects an off-grid-rated DC fridge, not a standard AC fridge run through the inverter]*
→ adding a properly-sized well pump per GT-11? raises the baseline further by roughly 0.15-0.6 kWh/day, central 0.35 kWh/day, though this is the least certain line item in the whole budget
→ applying a 20% contingency-and-winter-lighting margin to the fridge-and-pump-inclusive central total of 1.85 kWh/day yields a recommended design load of approximately 2.2 kWh/day, which explicitly excludes satellite internet (GT-12?, an additional 0.5-3.6 kWh/day depending on service tier) and any electric space heating or cooling

**Pre-check:** head GT-1, GT-10?, GT-11?, GT-12? · ?-marked: GT-10?, GT-11?, GT-12? · lowest cited: none · Inputs ceiling: MEDIUM
**Confidence:** MEDIUM — this chain rests on GT-10? (DC fridge draw, reported-by-delegate; verification: confirm against the datasheet of the specific fridge model selected), GT-11? (well-pump draw, unverified with an unusually wide bracket; verification: meter actual draw once a specific pump/pressure-system is installed, or obtain the running-wattage and expected daily run-time of the exact selected pump), and GT-12? (satellite-internet draw, reported-by-delegate; verification: confirm the household's chosen internet method and its power draw before finalizing sizing). No `Cn` is cited on this chain's head.

### Conclusion C2: The recommended solar array is approximately 700 W STC nameplate capacity

C1 (design load ≈2.2 kWh/day, MEDIUM) + GT-3 (winter solar-noon geometry) + GT-5? (tilt-adjusted December PSH) + GT-9? (combined system efficiency)
→ combining GT-3's low winter sun-angle with GT-5?'s tilt-gain reasoning gives a worst-month (December) insolation estimate of approximately 5.0 peak sun hours/day (bracket 4.3-5.6)
→ applying GT-9?'s combined system efficiency factor of approximately 0.75 to that insolation means each rated watt of STC array capacity delivers about 3.75 Wh of usable daily energy in December
→ dividing C1's 2.2 kWh/day design load by 3.75 Wh/W-day gives a bare, zero-margin array requirement of approximately 587 W of STC nameplate capacity
→ applying a 20% design-and-aging margin, to cover panel/inverter degradation over a multi-year service life and to leave headroom for post-autonomy battery recharge, raises the recommended array to approximately 704 W, rounded to a practical ~700 W nameplate array

**Pre-check:** head C1 (MEDIUM), GT-3, GT-5?, GT-9? · ?-marked: GT-5?, GT-9? · lowest cited: MEDIUM · Inputs ceiling: MEDIUM
**Confidence:** MEDIUM — this chain cites C1 (MEDIUM; see C1's own confidence line, not re-explained here) and rests directly on GT-5? (tilt-adjusted worst-month PSH estimate, the single most consequential unverified input in this analysis; verification: run NREL PVWatts, pvwatts.nrel.gov, with the cabin's exact coordinates/tilt/azimuth to obtain an authoritative December `solrad_monthly` figure) and GT-9? (combined system efficiency factor, reported-by-delegate/general design-guide convention; verification: confirm against the specific selected inverter/charge-controller datasheets and measure actual wiring runs). A live rival (seasonal, hand-adjusted tilt) is not ruled out; see Abandoned Reasoning dead-end 3.

### Conclusion C3: The recommended LiFePO4 battery bank is approximately 10.5 kWh nameplate capacity

C1 (design load ≈2.2 kWh/day, MEDIUM) + GT-6? (80% DoD convention) + GT-7? (round-trip efficiency) + GT-8? (cold-weather charge cutoff) + GT-9? (inverter/wiring efficiency)
→ delivering C1's 2.2 kWh/day of useful load through inverter-and-wiring losses (η≈0.90×0.98=0.882, per GT-9?'s component breakdown) requires the battery to discharge approximately 2.49 kWh/day of DC energy
→ over the stated 3-day autonomy target, the battery must discharge approximately 2.49 kWh/day × 3 days ≈ 7.48 kWh of DC energy in total
→ applying GT-6?'s 80% maximum-DoD convention for LiFePO4 cycle life, the required nameplate battery capacity is 7.48 kWh ÷ 0.80 ≈ 9.35 kWh
→ adding a 10% cold-weather capacity margin, per GT-8?'s charge-cutoff risk, raises the recommended nameplate battery bank to approximately 10.3 kWh, rounded to a practical ~10.5 kWh *[Assumes: A10 — battery enclosure/heating design will keep the pack above its BMS's minimum charge temperature]*

**Pre-check:** head C1 (MEDIUM), GT-6?, GT-7?, GT-8?, GT-9? · ?-marked: GT-6?, GT-7?, GT-8?, GT-9? · lowest cited: MEDIUM · Inputs ceiling: MEDIUM
**Confidence:** MEDIUM — this chain cites C1 (MEDIUM, not re-explained here) and rests on GT-6? (80% DoD convention; verification: confirm against the selected battery's datasheet), GT-7?/GT-9? (round-trip and inverter/wiring efficiency, both unverified; verification: confirm against selected component datasheets), and GT-8? (cold-temperature charge-cutoff risk, generic rather than tied to a specific selected battery's BMS spec; verification: confirm the selected battery's minimum charge temperature and design the enclosure accordingly). A live rival (a smaller bank paired with load-shedding discipline) is not ruled out; named in the Adversarial pass Rival step.

### Conclusion C4: The sized system (≈700 W array + ≈10.5 kWh battery) meets the design load with a recharge margin, subject to two named long-term risks

C1 (design load ≈2.2 kWh/day, MEDIUM) + C2 (array ≈700 W, MEDIUM) + C3 (battery ≈10.5 kWh, MEDIUM)
→ at C2's worst-month insolation and efficiency assumptions, the recommended ~700 W array can recharge approximately 700 W × 5.0 h × 0.75 ≈ 2.63 kWh/day in December
→ since 2.63 kWh/day of December recharge capability exceeds C1's 2.2 kWh/day design load by roughly 19%, the array can both meet daily consumption and gradually refill C3's battery bank after a multi-day autonomy event, rather than merely breaking even
→[2nd] once the system is in place, occupants who add appliances or services without re-checking this ~19% headroom will erode the recharge margin first and the 3-day autonomy buffer second, making load creep the most likely long-term failure path rather than a single catastrophic event *[Assumes: A7, A8 — occupants will not add major loads without re-sizing; satellite internet choice is unconfirmed]*
→[3rd] by roughly year 8-15, per GT-13?'s degradation figures, battery capacity fade and panel degradation will have consumed most of the 10-25% margins built into C2 and C3, so a mid-life capacity check or a planned bank/array top-up should be budgeted rather than assuming the original sizing holds unchanged for the system's full service life *[Assumes: A13 — a mid-life capacity check/top-up will actually be performed]*

**Pre-check:** head C1 (MEDIUM), C2 (MEDIUM), C3 (MEDIUM) · ?-marked: none · lowest cited: MEDIUM · Inputs ceiling: MEDIUM
**Confidence:** MEDIUM — this chain cites C1, C2, and C3, all MEDIUM (each chain's own confidence line carries its explanation and is not re-explained here); C4 rests on no additional `GT-N?` input directly. Two live rivals remain unresolved: the generator-hybrid alternative (named in the Adversarial pass Rival step) and, for the load-creep extension specifically, whether the household will in practice track usage against the stated headroom (A7/A8, unverified).

---

## 5. Abandoned Reasoning

### Dead End: Annual-average insolation sizing

**What was tried:** Initially considered sizing the array using the region's annual-average peak sun hours (~5.5-6.8 PSH per GT-4?) rather than the December worst-month figure.

**Why abandoned:** This systematically undersizes the array for the December/January trough — using ~6 PSH instead of ~5 PSH in the array formula would understate the required array by roughly 15-20%, producing chronic winter under-generation exactly when autonomy needs are highest. It also contradicts the problem statement's explicit instruction to use the worst-month design method.

**What it ruled out:** Confirms that any design using annual-average or "typical" monthly figures for this location is not reliable and should not be substituted for the worst-month method used in chains C2-C4.

### Dead End: Lead-acid battery chemistry as a lower-cost alternative

**What was tried:** Considered whether a flooded or AGM lead-acid bank (typically lower upfront $/kWh) could substitute for LiFePO4 while still meeting the reliability goal.

**Why abandoned:** Lead-acid's ~50% DoD convention (versus LiFePO4's ~80%, GT-6?) means a lead-acid bank would need roughly 1.6× the nameplate capacity of the LiFePO4 recommendation to deliver the same usable 3-day autonomy energy, and its lower round-trip efficiency (~80-85% versus LiFePO4's ~95-98%, GT-7?) would further inflate the required array. Combined with shorter cycle life and stronger cold-temperature capacity derating, this path was abandoned in favor of the prompt's specified LiFePO4 chemistry, which this analysis confirms is also the better-justified engineering choice rather than merely a stipulation accepted uncritically.

**What it ruled out:** Confirms LiFePO4 is not an arbitrary constraint but a chemistry that reduces both battery and (indirectly) array sizing relative to the lead-acid alternative for the same reliability target.

### Dead End: Seasonal (manually re-adjusted) array tilt as the default design basis

**What was tried:** Considered designing around a seasonally-adjusted tilt schedule (flatter in summer, steeper in winter) rather than a single fixed lat+15° tilt, which published guidance (GT-5?) suggests could further increase December yield.

**Why abandoned:** A seasonal-tilt design introduces a human-maintenance dependency (someone must physically re-tilt the array on schedule) for a cabin that may be unattended for stretches, which is a less robust default for a system whose central goal is unattended, year-round reliability. The fixed lat+15° tilt was adopted as the more conservative default instead.

**What it ruled out:** Rules out treating "seasonal tilt" as a way to shrink the recommended array size in this analysis's headline numbers; it remains a legitimate cost-reduction option only if the household commits to reliable manual adjustment, noted as a live rival on chain C2's confidence line rather than adopted.

---

## 6. Conclusion

**Recommended approach:** Size the solar array to approximately 700 W STC nameplate capacity and the LiFePO4 battery bank to approximately 10.5 kWh nameplate capacity, against a recommended 2.2 kWh/day design load, using the December worst-month sizing method (chain C2, C3). A practical build might use two 350 W panels (or three ~235 W panels) and a 10-12 kWh rack of server-style LiFePO4 modules, rounding up from the bare calculated minimums for available stock sizes.

**Key insight:** The stated ~1.5 kWh/day figure is a defensible bare-minimum lighting-and-electronics estimate but understates a realistic year-round design load by roughly 45-50% once an efficient DC fridge and a modest well pump are included (chain C1). The single largest additional uncertainty is not the base load but the worst-month solar resource figure itself (GT-5?), which is the input most worth independently verifying — via the free NREL PVWatts calculator — before purchasing hardware, since it swings the headline array size by 15-40% at its bracket's edges (chain C2).

**Trade-offs acknowledged:** This design accepts a fixed lat+15° tilt over a seasonal-adjustment schedule that could shrink the array further but adds a maintenance dependency (chain C2). It also accepts full solar-plus-battery autonomy for the stated 3-day target rather than pairing a smaller system with a generator-hybrid backup that would better cover rarer multi-day storm tails — no chain — flagged assumption only. Finally, it accepts a 10-25% capacity margin now in exchange for deferring a mid-life battery/panel capacity check to roughly year 8-15 rather than over-building for a multi-decade horizon today (chain C4).

**Pre-check:** head C1 (MEDIUM), C2 (MEDIUM), C3 (MEDIUM), C4 (MEDIUM) · ?-marked: none · lowest cited: MEDIUM · Inputs ceiling: MEDIUM
**Confidence:** MEDIUM — every chain contributing to this Conclusion (C1, C2, C3, C4) is rated MEDIUM; none is rated HIGH because each rests on at least one `GT-N?` input (see each chain's own confidence line above, not re-explained here). The single highest-value action to raise this rating is independently verifying GT-5? (worst-month peak sun hours) via NREL PVWatts for the exact site coordinates; the second highest-value action is confirming GT-11? (well-pump draw) and GT-12? (internet-method choice) once specific equipment is selected.
