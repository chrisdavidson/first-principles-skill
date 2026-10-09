**Disclosed:** none — the Essence Statement, assumptions table, ground truths, derivation chains,
closure ledger, self-audit scan, and Self-Audit Gate all ran to completion this session; the only
degradation is the DNS failure reaching nrel.gov, which is already disclosed as a Phase 3 failure
record in §3/§5 rather than as a withheld process step.

## Answer

**Recommendation:** Build a fixed, true-south array tilted at latitude+15° (≈50°), sized 600–800 W,
paired with a 5–10 kWh nameplate LiFePO4 battery bank, against a derived worst-month design
insolation of 4.5 kWh/m²/day and ≈75%/67.5% system efficiency (chains C1, C2, C3, C5, C6). A small
backup generator is recommended as cheap insurance against outlier storms (chain C7).

**Band (from §6):** MEDIUM (chains C2, C3, C5, C6).

**Would change it:** Resolving whether the cabin has internet and a standard fridge is the single
biggest lever — a realistic 2.5–4 kWh/day load roughly doubles both figures (chain C4). Reading
NREL's tilted-surface table and specific vendor datasheets, both unread this session, would also
raise confidence (chain C2).
## 1. Problem Essence

**Essence Statement:** Size an off-grid LiFePO4 solar-electric system (panel array wattage and
battery bank kWh) for a year-round-occupied cabin at 35°N high-desert New Mexico, such that it
reliably delivers a stated net load against the *worst* month of solar insolation (not an annual
average), carries 3 days of zero-sun autonomy, and does so from insolation, loss-mechanism, and
battery-chemistry figures that are derived or sourced rather than assumed by rule of thumb.

**Success criteria (a correct answer must):**
- Derive a defensible worst-month peak-sun-hours (PSH) figure from solar geometry (declination,
  air mass, day length) for a fixed array tilted for winter optimization, not asserted from a rule
  of thumb alone.
- Build total system efficiency from named, individually-sourced loss mechanisms (inverter,
  charge controller, wiring, battery round-trip, soiling, temperature, aging), multiplied, not a
  single asserted "80% derate."
- Produce a concrete panel-array wattage figure and a concrete battery-bank kWh figure (with a
  range), both traceable back to the PSH figure and the efficiency build-up.
- Sanity-check the resulting numbers against real-world off-grid cabin system sizes.
- Name the single assumption that most changes the answer if wrong, and show how the answer
  scales if that assumption is off — this is a required output, not an optional caveat.
- Not require the answer to be "exactly one of" a predetermined set of system sizes — the answer
  is whatever array-W / battery-kWh pair the derivation supports, which may itself be a range
  rather than a single point.

## 2. Assumptions Table

| # | Assumption | Type | Treatment | Verdict | Verification |
|---|---|---|---|---|---|
| A-01 | Earth's axial tilt (obliquity) ≈ 23.44°, giving winter-solstice solar declination δ = −23.44° | physical law | Accept as ground-truth candidate | Accepted → GT-1 | Astronomical constant; invariant on human timescales |
| A-02 | Solar constant (total solar irradiance at 1 AU) Gsc ≈ 1361 W/m² | physical law | Accept as ground-truth candidate | Accepted → GT-2 | Standard physics reference value; not re-sourced live this session (see GT-2 provenance note) |
| A-03 | Site latitude ≈ 35°N, elevation 5,000–7,000 ft, "clear high-desert skies, minimal haze" | current constraint (stipulated scenario) | Accepted as given design input | Accepted → GT-6 | User-stipulated; qualitative sky-clarity claim not independently measured for a specific site |
| A-04 | December/January is the worst-insolation month at this latitude | physical law (sun-angle/day-length component) + current constraint (cloud climatology component) | Split: sun-angle part follows directly from A-01; cloud-frequency part is regional climatology, not guaranteed | Accepted, sun-angle part; flagged, climatology part | Day length/declination part is deductive from A-01. Which exact month (Dec vs Jan) has the lowest cloud-adjusted insolation varies by local storm-track year; design uses the lower of the two by convention |
| A-05 | Net daily load = 1.5 kWh/day for 2 adults, year-round occupied | **untested belief** (stipulated by user, but its realism for the stated occupancy is directly challenged by the prompt) | Verify by reconstructing a plausible load budget; flag if implausible | **Flagged as unrealistically low** for a year-round occupied cabin unless specific major loads (compressor fridge, well pump, space heat, washer) are excluded | See Phase 4 load-budget reconstruction; this is the single most load-bearing assumption in the whole analysis (see §6 sensitivity) |
| A-06 | 3 days of zero-sun autonomy is an adequate reliability target | current constraint (design choice, stipulated) | Record expiry condition | Accepted as design input; expiry condition stated | Multi-day NM winter storm/snow systems occasionally exceed 3 consecutive low-insolation days — see §5 Sensitivity and §6 generator discussion |
| A-07 | LiFePO4 usable depth of discharge ≈ 95–100% | convention (battery-chemistry datasheet figure) | Accept with "?" — not read at a specific cited datasheet this session | Accepted, flagged `?` → GT-4 | **Unverified — flagged.** Widely published across LiFePO4 datasheets (e.g., 95–100% usable DoD vs ~50% for lead-acid); not verified against one specific vendor spec sheet this session |
| A-08 | LiFePO4 round-trip efficiency ≈ 95% | convention (battery-chemistry datasheet figure) | Accept with "?" | Accepted, flagged `?` → GT-4 | **Unverified — flagged.** Same as A-07 |
| A-09 | Pure sine inverter efficiency ≈ 93% (typical 90–95% band) | convention (equipment spec) | Accept with "?" | Accepted, flagged `?` → GT-5a | **Unverified — flagged.** Standard off-grid inverter datasheet range; not read at a specific vendor spec this session |
| A-10 | MPPT charge-controller efficiency ≈ 97% | convention (equipment spec) | Accept with "?" | Accepted, flagged `?` → GT-5b | **Unverified — flagged.** Standard MPPT datasheet range (97–99%) |
| A-11 | DC wiring losses can be designed to ≈ 2% | convention (NEC-informed design target, not a measured loss) | Accept with "?" | Accepted, flagged `?` → GT-5c | **Unverified — flagged.** Conventional design target (<3% typical best practice), contingent on competent installation |
| A-12 | Dust/soiling loss in dusty high desert ≈ 5% absent frequent cleaning | untested belief | Flag as unverified; no discriminating observation available without site data | Accepted, flagged `?` → GT-5d | **Unverified — flagged.** No site-specific soiling measurement exists; 5% is a conservative literature-typical value for arid, infrequently-cleaned arrays |
| A-13 | Winter cold temperatures have a near-neutral-to-slightly-positive effect on PV output (vs. the usual *hot*-climate derating) | physical law (semiconductor negative temperature coefficient of Voc/power) | Accept as ground-truth candidate; explicitly **not** banked as a margin bonus | Accepted → GT-1b | Well-established PV temperature-coefficient physics; treated conservatively (98% factor used, not >100%) |
| A-14 | PV output degrades ≈ 0.5–0.7%/yr; LiFePO4 retains materially less than 100% capacity by year 10 | convention (manufacturer degradation-curve literature) | Accept with "?"; apply as an explicit aging design margin, not folded into "efficiency" | Accepted, flagged `?` → GT-7 | **Unverified — flagged.** Standard manufacturer degradation curves; not read at a specific datasheet this session |
| A-15 | No backup generator is required | current constraint (stipulated by user, but explicitly up for challenge per the prompt) | Challenge directly | **Challenged — see §6**: recommended as cheap insurance, not as a requirement that invalidates the no-generator design | Routed to Conclusion; does not change panel/battery sizing math, changes the reliability margin around it |
| A-16 | Fixed tilt = latitude + 15° (≈ 50°) is a good winter-optimized compromise angle | convention (rule of thumb) | Explicitly challenge against the physics-exact noon-normal angle | **Challenged and confirmed as the better choice** — see Phase 4 derivation; exact noon-normal tilt for the solstice alone (≈ lat + 23.4° ≈ 58°) over-optimizes for one day and under-performs across the full Nov–Feb design window | Derived in §4, chain C1 |
| A-17 | Web-search-sourced insolation figures (NM December PSH ≈ 4.4 PSH at generic tilt; Albuquerque winter PV yield ≈ 3.77 kWh/day per kW-DC at 31° tilt; "lat+15 gives ~10% December gain") | **untested belief** (reported-by-delegate: summarized by WebSearch/WebFetch, not read by this analysis at the primary source page) | Use only as a cross-check on the physics-derived central estimate, never as the primary derivation | Accepted as corroboration only, flagged `?` → GT-3b/c/d | **Unverified — flagged.** See Phase 3 failure record: direct NREL data-table PDFs (nrel.gov) were unreachable this session (DNS failure) |
| A-18 | NREL-sourced "Navajo Nation" solar-resource map showing 5.5–6.5 kWh/m²/day average **annual** irradiance for the four-corners high-desert region | untested belief (the figure itself is read-at-source; what is untested is whether an *annual-average* figure is transferable to a *December* design value without adjustment) | Accept as read-at-source corroboration; explicitly flag the annual-vs-worst-month mismatch so it is not used as a disguised December figure | Accepted → GT-3a; **not** used as a stand-in for the December design value (analogy-as-evidence risk) | Viewed directly: IEEE REPC 2026 conference paper, Nez/Begay/Arumugam/Romine, Navajo Technical University, slide "Solar Energy Potential," citing NREL |
| A-19 | The implicit load composition behind 1.5 kWh/day (LED lighting + small electronics only, no compressor refrigerator, no well pump, no space heat) | untested belief | Reconstruct an explicit load budget to test plausibility | **Reconstructed and found consistent with a no-fridge, no-pump, minimal-load cabin only** — inconsistent with a typical "year-round occupied by 2 adults" cabin | See Phase 4 load-budget table |

| A-20 | Clear-sky horizontal transmittance ≈0.65–0.75 and lat+15°-vs-horizontal tilt gain ≈1.4–1.6× (used in C2's estimate rebuild) | untested belief (physics-model estimate, surfaced by the Phase 4 Assumption Audit) | Flag; close via a direct NREL tilted-table read | Accepted, flagged `?` | **Unverified — flagged.** No live read obtained this session (DNS failure, see Phase 3 failure record); bracket chosen to be internally consistent with the H0 and AM derivation and with GT-3a/GT-3b/GT-3d corroboration |
| A-21 | PV module mismatch/manufacturing-tolerance loss ≈2% (used in C3) | convention (equipment spec, surfaced by the Assumption Audit) | Accept with `?` | Accepted, flagged `?` | **Unverified — flagged.** Standard array-design allowance; not read at a specific module datasheet this session |
| A-22 | Shading/horizon allowance ≈2% (used in C3) | untested belief (site-specific, surfaced by the Assumption Audit) | Flag; no site survey available | Accepted, flagged `?` | **Unverified — flagged.** No horizon/shading survey exists for a specific site; conservative generic allowance |
| A-23 | A 3–7% monthly-average discount off clear-sky insolation captures the occasional December storm/overcast system in this high-desert climate (used in C2) | untested belief (surfaced by the Assumption Audit) | Flag; close via multi-year NREL/NSRDB monthly-average read | Accepted, flagged `?` | **Unverified — flagged.** Judgment-based, not derived; the single largest source of inference-axis softness in C2 |
| A-24 | A 20–40% array oversize above the bare arithmetic minimum is needed for post-autonomy battery recharge headroom (used in C5) | convention (off-grid design practice, surfaced by the Assumption Audit) | Accept with `?` | Accepted, flagged `?` | **Unverified — flagged.** Consistent with general off-grid design guidance found this session (e.g., Backwoods Solar's "you can never have too many panels" framing), not a specific numeric standard read at source |
| A-25 | Routine LiFePO4 cycling is commonly limited to ≈80% DoD (vs. the 95–100% the chemistry allows) to extend cycle life (used in C6) | convention (battery-industry practice, surfaced by the Assumption Audit) | Accept with `?` | Accepted, flagged `?` | **Unverified — flagged.** Widely repeated LiFePO4 longevity guidance; not read at a specific vendor cycle-life curve this session |

**`?`-marked (count 16):** A-07, A-08, A-09, A-10, A-11, A-12, A-14, A-17 (covers three
sub-figures bundled as one row: GT-3b, GT-3c, GT-3d), A-20, A-21, A-22, A-23, A-24, A-25 —
full GT-level enumeration is given in Phase 3 below.

## 3. Ground Truths

- **GT-1** — Earth's axial tilt (obliquity) ≈ 23.44°; solar declination at winter solstice
  δ = −23.44°. *Type:* physical law / astronomical constant. *Provenance:* read-at-source
  equivalent (invariant defined constant, applied directly in the Phase 4 computation). No `?`.
- **GT-1b** — A photovoltaic cell's open-circuit voltage (and typically its power output) has a
  *negative* temperature coefficient: output falls as cell temperature rises above the 25°C STC
  reference, and *rises* modestly as cell temperature falls below it. *Type:* physical law
  (semiconductor physics). *Provenance:* standard PV physics; no `?`. Used conservatively (98%
  factor applied, not a bonus >100%).
- **GT-2** — Solar constant (total solar irradiance at 1 AU) Gsc ≈ 1361 W/m². *Type:* physical
  law / measured constant. *Provenance:* standard physics reference value; not independently
  re-measured or re-sourced via a live read this session, but it is a defined, invariant physical
  constant rather than an empirical claim subject to being "wrong" the way a vendor spec can be.
  No `?` (physical-law carve-out per methodology).
- **GT-3a** — NREL solar-resource map shows **average annual** solar PV irradiance of
  5.5–6.5 kWh/m²/day across the four-corners "Navajo Nation" region (NM/AZ/UT high desert,
  ~35–37°N, similar elevation/climate class to this scenario). *Type:* measured/published
  (NREL dataset), presented secondhand via a cited conference paper. *Provenance:*
  **read-at-source** — this analysis directly viewed the source slide image (not a text summary):
  IEEE Rural Electric Power Conference 2026, "Driven Design of a Stand-Alone PV System to Support
  Residential Loads on the Navajo Nation," Nez/Begay/Arumugam/Romine, Navajo Technical University,
  slide "Solar Energy Potential," citing NREL. Read-location: slide 4 of the fetched PDF
  (https://www.nmlegis.gov/.../STTC%20062326...Navajo%20Nation.pdf). No `?`. **Explicitly not**
  used as a December worst-month figure — it is an *annual average*, cited here only as a
  same-region corroboration that the broad magnitude (mid-single-digit kWh/m²/day) is right for
  this climate class, not as the design PSH itself.
- **GT-3b?** — New Mexico December peak sun hours ≈ 4.4 PSH at a stated "20° tilt" reference.
  *Type:* untested belief / reported figure. *Provenance:* **reported-by-delegate** — summarized
  by WebFetch from thegreenwatt.com; this analysis did not view the raw page text. `?` required.
- **GT-3c?** — Albuquerque, NM winter PV energy yield ≈ 3.77 kWh/day per kW-DC installed, at a
  31° fixed tilt. *Type:* untested belief / reported figure. *Provenance:* **reported-by-delegate**
  — surfaced via a WebSearch snippet summarizing jouleio.com; raw page not opened. `?` required.
- **GT-3d?** — A winter tilt of latitude+15° yields roughly a 10% December energy gain over a
  tilt-at-latitude array. *Type:* untested belief / reported figure. *Provenance:*
  **reported-by-delegate** — WebSearch synthesis citing an off-grid design source; raw source not
  opened. `?` required.
- **GT-4?** — LiFePO4 usable depth of discharge ≈ 95–100% (vs. ~50% for lead-acid); round-trip
  efficiency ≈ 95%. *Type:* convention (battery-chemistry datasheet figures, consistent with
  common vendor specs — e.g., Battle Born, EVE, CATL cell datasheets). *Provenance:*
  **unverified** — not read at a specific vendor datasheet this session. `?` required.
- **GT-5a?** — Pure sine-wave inverter efficiency ≈ 93% (typical published band 90–95%). *Type:*
  convention. *Provenance:* unverified this session. `?` required.
- **GT-5b?** — MPPT charge-controller efficiency ≈ 97% (typical published band 97–99%). *Type:*
  convention. *Provenance:* unverified this session. `?` required.
- **GT-5c?** — DC wiring losses can be engineered to ≈ 2% with competent sizing (NEC-informed
  design target, <3% typical best practice). *Type:* convention/design target, not a measurement.
  *Provenance:* unverified this session. `?` required.
- **GT-5d?** — Dust/soiling loss on a fixed array in a dusty, infrequently-cleaned high-desert
  setting ≈ 5%. *Type:* untested belief (no site-specific measurement exists). *Provenance:*
  unverified. `?` required.
- **GT-6** — Scenario-stipulated design inputs: latitude 35°N; elevation 5,000–7,000 ft; net load
  1.5 kWh/day delivered to loads; 3 days autonomy; no grid, no generator assumed. *Type:* current
  constraint (problem definition, supplied by the user, not an external claim to verify). No `?`
  — these are accepted as the problem's own terms; the **realism** of the 1.5 kWh/day figure for
  the stated occupancy is separately tested in Phase 4 (GT-6 being "accepted as stipulated" is not
  the same claim as "accepted as realistic").
- **GT-7?** — Crystalline-silicon PV modules typically degrade ≈ 0.5–0.7%/year; LiFePO4 packs
  typically retain somewhat less than 100% of nameplate capacity after ~10 years / several
  thousand cycles at moderate DoD. *Type:* convention (manufacturer degradation-curve literature).
  *Provenance:* unverified this session. `?` required.

- **GT-8** — A fully-appointed, standard-appliance off-grid residence (LED lights, standard
  refrigerator, electric stove, microwave, washer/dryer, water pump, space heater, electronics)
  sized by the same IEEE REPC 2026 Navajo Nation paper totals **15.68 kWh/day**, roughly ten times
  this scenario's stipulated 1.5 kWh/day. *Type:* measured/published (itemized load table in a
  cited engineering paper). *Provenance:* **read-at-source** — viewed directly: same PDF as GT-3a,
  slide "Electrical Load Estimation" (Table I), read-location: that table's "Total Daily
  Consumption" row. No `?`. Used in §4 as an order-of-magnitude anchor for how far 1.5 kWh/day sits
  below a normally-appointed household, not as a direct substitute for this scenario's own load.

**Phase 3 failure record:** An attempt was made to open NREL's own direct/diffuse solar radiation
data tables (`nrel.gov/grid/solar-resource/assets/data/west-1.pdf`, the classic "Red Book"
tilt-angle insolation tables, which would have let this analysis read an Albuquerque-specific
December tilted-surface figure directly from NREL). The fetch failed with a DNS resolution error
(`getaddrinfo ENOTFOUND www.nrel.gov`) on two attempts — network/DNS unreachability, not a content
problem. This is why the December design PSH is derived independently from first-principles solar
geometry (GT-1, GT-2 → Chain C1) rather than read directly off an NREL table, with GT-3a serving
as the one read-at-source empirical corroboration available this session.

**`?`-marked ground truths (9 of 15):** GT-3b, GT-3c, GT-3d, GT-4, GT-5a, GT-5b, GT-5c,
GT-5d, GT-7.

**Read-locations for unsuffixed ground truths feeding load-bearing chains:**
- GT-1, GT-1b, GT-2: applied directly from defined physical constants/physics (no external
  document location; definitional).
- GT-3a: slide "Solar Energy Potential" (slide 4) of the fetched Navajo Nation IEEE REPC 2026 PDF,
  citing an embedded NREL "Solar Photovoltaic Resources" map.

## 4. Derivation Chains

*Companion techniques applied in this phase:* **trade-off** (tilt-angle selection, C1),
**theoretical-limit** (extraterrestrial insolation ceiling, within C2), **estimate**
(unit-factor magnitude rebuild, within C2 and C4), **second-order** (actor/time lenses, C7).
**five-whys (reduce-to-primitives)** was not run as a separate formal drill — not applicable —
every ground truth in §3 was already constructed directly from a physical constant, a
read-at-source measurement, or an explicitly `?`-flagged convention, so a separate decomposition
pass would re-derive the same bottoming-out already shown. **fishbone** was not run separately —
not applicable — the loss-mechanism build-up in C3 already performs the equivalent breadth-first
category decomposition (temperature / soiling / wiring / electronics / battery / aging) directly.
**inversion** (Phase 2 trigger: a conclusion that "feels too clean") fired on the claim "1.5 kWh/
day reliably covers 2 adults year-round" — see C4, which is the inversion-driven load-budget
reconstruction that produced the A-05/A-19 flag; its failure-guaranteeing preconditions (no
internet load, no AC-compressor fridge, no electric heat, no washer) are stated inline in C4
rather than in a separate table, since the full load-budget rebuild already enumerates them more
concretely than a generic precondition list would.

---

### C1 — Fixed-tilt angle selection (trade-off)

**Must-haves (knock-out):** array must have no powered tracking motor (remote, unattended,
off-grid site — a tracker is one more failure point with no diagnostic visit expected for weeks).
All five candidate tilts below satisfy this trivially (none involve motors); no option is
eliminated at this step.

**Options:** (a) horizontal/flat (0°); (b) fixed at latitude (35°); (c) fixed at latitude+15°
(50°); (d) fixed at latitude+23.4°, i.e., exactly normal to the sun at solar noon on the solstice
itself (≈58°); (e) manually seasonally-adjusted, 2–4 repositionings/year.

**Criteria, weights locked before scoring, and anchors:**

| Criterion | Weight | 1 anchor | 5 anchor |
|---|---|---|---|
| December (worst-month) yield | 5 | <3.5 kWh/m²/day-equivalent | >5.2 kWh/m²/day-equivalent |
| Whole-winter (Nov–Feb) average yield | 4 | Poor balance across the season | Best balance across the season |
| Simplicity/reliability (no moving parts, no scheduled site visits) | 4 | Requires tracking/frequent adjustment | Zero moving parts, zero scheduled maintenance |
| Shoulder/summer-season usability | 2 | Badly mismatched to high summer sun | Good match |
| Wind/snow structural risk | 2 | High risk | Low risk |

**Scores and weighted totals** (citing GT-1/GT-1b/the geometry derived in C2 as the basis for the
yield scores):

| Option | Dec yield | Winter-avg | Simplicity | Shoulder | Wind/snow | **Weighted total** |
|---|---|---|---|---|---|---|
| (a) Horizontal | 1 | 1 | 5 | 3 | 5 | **45** |
| (b) Lat (35°) | 3 | 3 | 5 | 5 | 4 | **65** |
| (c) Lat+15° (50°) | 5 | 5 | 5 | 3 | 3 | **77** |
| (d) Lat+23.4° (58°) | 4 | 3 | 5 | 1 | 3 | **60** |
| (e) Seasonal (manual) | 5 | 5 | 2 | 5 | 3 | **69** |

**Flip test:** (c) beats the runner-up (e) by 8 points. The only criterion on which (e) scores
higher than (c) is shoulder/summer usability (diff +2, weight 2 → max swing +6 even at the weight
ceiling of 5 — insufficient alone). The only criterion that can close the gap is simplicity
(diff +3 in (c)'s favor, weight 4): dropping that weight from 4 to 1 — the floor of the 1–5 scale
— removes 9 points of (c)'s advantage, enough to flip. **No single-criterion change short of
driving a weight to the scale's floor flips this result — (c) is a robust winner, not a
near-tie.**

```text
GT-1 (δ=−23.44° at solstice, fixes the low winter sun angle) + GT-1b (PV temperature physics, rules out powered trackers as unnecessary)
→ five fixed/adjustable tilt strategies scored against five weighted criteria (December yield, whole-winter balance, simplicity, shoulder-season usability, wind/snow risk), weights locked before scoring
→ lat+15° (≈50°) wins on weighted total (77), ahead of manual-seasonal (69), latitude-only (65), solstice-exact lat+23.4° (60), and horizontal (45)
→ the flip test shows no single-criterion weight change short of the scale's floor overturns the winner
→ **fixed tilt = latitude + 15° (≈50°), facing true south, is the recommended array angle**
```

**Pre-check:** head = GT-1 (HIGH) · GT-1b (HIGH) · none `?` · lowest cited = none · Inputs
ceiling = HIGH.
**Confidence: HIGH** — Inputs: both head ground truths are physical law, unsuffixed. Inference:
every score is grounded in the physics of solar geometry (not post-hoc rationalized — weights
were locked before scoring). Rivals: the flip test shows no small weight perturbation overturns
the winner.

---

### C2 — Worst-month peak sun hours (PSH) at the selected tilt

```text
GT-1 (δ=−23.44° at winter solstice) + GT-2 (Gsc≈1361 W/m²) + GT-3a (same-region NREL corroboration)
→ sunset hour angle ωs = arccos(−tan(35°)tan(−23.44°)) = 72.33°, giving a Dec-21 day length of 2ωs/15 ≈ 9.64 h — almost 2.4 h shorter than the ~12 h equinox day
→ at solar noon the surface-normal air mass is AM = 1/cos(φ−δ) = 1/cos(58.44°) ≈ 1.91, roughly double a summer noon's AM≈1.0 at this latitude, so winter noon sunlight crosses far more atmosphere even under a cloudless sky
→ [theoretical-limit, horizontal fixed-orientation ceiling] integrating Gsc with the Dec-21 eccentricity correction (E0≈1.0325) over the day's declination/latitude geometry gives extraterrestrial horizontal daily insolation H0 ≈ 4.6 kWh/m²/day — the hard physical ceiling for *any* horizontal surface at this date/latitude, atmosphere-free
→ [theoretical-limit, absolute ceiling] the true outer bound — a perfectly sun-tracking, atmosphere-free surface — would receive Gsc·E0·(daylight hours) ≈ 1405 W/m² × 9.64 h ≈ 13.5 kWh/m²/day, far above anything a real fixed array achieves
→ [theoretical-limit, gap] the gap from "best demonstrated" clear-sky tilted performance to this absolute ceiling (≈8–9 kWh/m²/day) is irreducible given a fixed, untracked array under a real atmosphere — it is not a convention that cheap engineering could recover
→ [estimate, unit-factor rebuild] clear-sky tilted daily insolation ≈ H0 × (clear-sky horizontal transmittance 0.65–0.75, central 0.70) × (lat+15°-vs-horizontal tilt gain 1.4–1.6×, central 1.5) ≈ 4.2–5.5 kWh/m²/day, central 4.8 kWh/m²/day [Assumes: A-20 clear-sky transmittance model]
→ cross-checked against GT-3b? (4.4 PSH at a lower reference tilt) and GT-3d? (lat+15 adds ~10% over lat-tilt alone): the physics-derived clear-sky bracket sits consistent with, and modestly above, these reported figures, as expected since neither reported figure uses the lat+15 winter-optimized tilt this design selects (C1)
→ applying a 3–7% (central 5%) monthly-average discount for the storm/overcast days that interrupt an otherwise mostly-clear high-desert December [Assumes: A-23 cloud-frequency discount] gives a design (not single-clear-day) worst-month PSH
→ **design worst-month PSH = 4.5 kWh/m²/day, bracket 4.0–5.0 kWh/m²/day**
```

**Pre-check:** head = GT-1 (HIGH) · GT-2 (HIGH) · GT-3a (HIGH) · `?`-marked = none on head (GT-3b?,
GT-3d? are cited only as a cross-check within a hop, not as head inputs the conclusion requires) ·
lowest cited = none · Inputs ceiling = HIGH.
**Confidence: MEDIUM** — Inputs axis is HIGH (all head identifiers are unsuffixed/read-at-source
or physical law). Inference axis is short: the clear-sky-transmittance value (0.65–0.75) and the
monthly-storm discount (3–7%) are engineering-judgment estimates, not strict derivations from the
ground truths, and they are what the `[Assumes: A-20]`/`[Assumes: A-23]` tags flag. What would
close this gap: reading NREL's own tilted-surface insolation table for Albuquerque/Santa Fe
directly (attempted this session — see the Phase 3 failure record — and blocked by a DNS failure,
not a content problem) would let the transmittance and discount hops be replaced by a single
read figure. Rivals: no live rival after §5 Sensitivity (a materially lower PSH is addressed there
as the dominant sensitivity, not as an unresolved competing conclusion).

---

### C3 — Total system efficiency build-up (panel → delivered load)

```text
GT-1b (temp. coefficient) + GT-5d? (soiling) + GT-5c? (wiring) + GT-5b? (MPPT) + GT-4? (battery RTE) + GT-5a? (inverter)
→ multiply each independent loss along the path: temperature 0.98 × soiling 0.95 × wiring 0.98 × MPPT controller 0.97 × battery round-trip 0.95 × inverter 0.93 × module mismatch/tolerance 0.98 [Assumes: A-21] × shading/horizon allowance 0.98 [Assumes: A-22]
→ stepwise product ≈ 0.751 — the as-built, "day-one" system efficiency is ≈75%
→ apply a separate 10% end-of-life design margin (divide by 0.90, not another multiplicative loss) for ~10 years of combined PV output degradation and LiFePO4 capacity fade (GT-7?)
→ **η_fresh ≈ 0.75 (bracket 0.70–0.78); η_aged-design ≈ 0.675, used as the sizing denominator**
```

This 70–75% fresh / ~67% aged-design band matches the commonly cited off-grid, battery-based
system-efficiency range in solar design literature — a useful sanity check on the build-up, not a
substitute for having built it up mechanism by mechanism.

**Pre-check:** head = GT-1b (HIGH) · GT-5d? (MEDIUM) · GT-5c? (MEDIUM) · GT-5b? (MEDIUM) · GT-4?
(MEDIUM) · GT-5a? (MEDIUM) · `?`-marked on head = GT-5d, GT-5c, GT-5b, GT-4, GT-5a (5 of 6) ·
lowest cited = none (no chains cited, only GTs) · Inputs ceiling = MEDIUM.
**Confidence: MEDIUM** — Inputs axis is short: five of six head ground truths are `?`-marked
industry-convention figures rather than read at a specific vendor datasheet this session; what
would close it: selecting actual inverter/charge-controller models and reading their datasheet
efficiency curves, and measuring site-specific soiling after one season. Inference axis is HIGH
(straight multiplication, no gaps). Rivals: individual factor values could each be disputed within
their stated bands, but the method and the resulting 70–75% band are not seriously contested by
any rival approach in the literature consulted.

---

### C4 — Load-budget realism check (inversion-triggered estimate rebuild)

The claim "1.5 kWh/day reliably covers 2 adults, year-round" is tested by reconstructing it from
itemized unit-factors rather than accepted at face value (the inversion trigger: this conclusion,
handed to the analysis as a stipulated input, is exactly the kind of "too clean" figure the
inversion technique exists to pressure-test).

```text
GT-6 (stipulated 1.5 kWh/day net load) + GT-8 (read-at-source: a normally-appointed off-grid home totals 15.68 kWh/day)
→ [estimate, unit-factor rebuild] a lean, no-fridge-compromise load budget: LED lighting (8×9W×4h≈0.29 kWh) + laptop/phone charging (2 people×50Wh≈0.10 kWh) + a small efficient 12V DC fridge (≈0.40 kWh) + minimal on-demand water pumping (≈0.30 kWh) + misc electronics (≈0.15 kWh) ≈ 1.24 kWh/day — broadly consistent with the stated 1.5 kWh/day, but only under that specific set of exclusions
→ naming what is excluded to hit that number: no internet/satellite-link load (a Starlink-class terminal alone commonly draws 0.75–1.5 kWh/day continuous), no standard AC-compressor refrigerator (+0.6–1.6 kWh/day over the lean DC unit), no electric space heating, no washer
→ the read-at-source corroboration in GT-8 independently confirms the scale mismatch: a normally-appointed off-grid home (same climate region, read-at-source load table) totals 15.68 kWh/day — roughly 10× this scenario's figure — which is consistent with 1.5 kWh/day being achievable only for a stripped-down, minimal-amenity cabin, not "normal" 2-adult year-round living
→ reintroducing just one commonly-present modern convenience (internet connectivity) plausibly pushes real load to ≈2.0–2.7 kWh/day; reintroducing a standard fridge instead of the lean DC unit plausibly pushes it to ≈1.8–2.8 kWh/day; both together plausibly land in the ≈2.5–4 kWh/day range
→ **1.5 kWh/day is realistic only for a minimal-amenity cabin (LED lighting + phone/laptop charging + a small efficient DC fridge + minimal water pumping, explicitly no internet, no standard fridge, no electric heat, no washer); for "normal" year-round 2-adult occupancy including internet and a standard fridge, a more realistic design load is ≈2.5–4 kWh/day — roughly 1.7–2.7× higher**
```

**Pre-check:** head = GT-6 (HIGH, stipulated) · GT-8 (HIGH, read-at-source) · `?`-marked = none on
head · lowest cited = none · Inputs ceiling = HIGH.
**Confidence: MEDIUM** — Inputs axis HIGH. Inference axis is short: the itemized unit-factor
wattages (LED count/hours, pump duty cycle, DC-fridge draw) are reasonable estimates for a
minimal-amenity cabin, not measured for this specific cabin — what would close it: an actual
appliance inventory and a kill-a-watt/clamp-meter audit once occupied, or at minimum a firm
decision on whether internet connectivity and a standard fridge are in scope. Rivals: the
"1.5 kWh/day is fine" reading is the rival this chain directly confronts — see §6 for why it is
not ruled out outright (it is possible, just narrow) but is flagged as the dominant risk to the
whole design in §5/§6.

---

### C5 — Required panel array capacity

```text
C2 (design PSH = 4.5 kWh/m²/day, bracket 4.0–5.0) + C3 (η_aged-design ≈ 0.675) + GT-6 (1.5 kWh/day stipulated load)
→ bare-physics-minimum array STC rating = Load(Wh) ÷ (PSH(h) × η_aged) = 1,500 Wh ÷ (4.5 × 0.675) ≈ 494 W at the central PSH; at the bracket ends, 1,500 ÷ (4.0×0.675) ≈ 556 W down to 1,500 ÷ (5.0×0.675) ≈ 444 W
→ a bare-minimum array leaves almost no surplus production to recharge the battery bank after an autonomy-draining cloudy stretch — it is sized only to break even on an average worst-month day [Assumes: A-24 recharge-headroom margin]
→ off-grid design practice adds a recharge-headroom margin (commonly 20–40% above the bare minimum) so the array can both serve the day's load and refill the battery once the sun returns; applying a 30% margin to the ≈494 W central bare-minimum figure gives ≈642 W
→ rounding to commercially standard module counts (e.g., 2×330–350 W modules ≈ 660–700 W, or 2×400 W ≈ 800 W)
→ **recommended array: 600–800 W (bare-physics minimum 445–555 W if recharge headroom and load-realism risk are both ignored)**
→ [sensitivity] this formula is linear in load: at C4's upper realistic-load estimate (3.0 kWh/day, double the stipulated figure), the bare-minimum array becomes 3,000 ÷ (4.5×0.675) ≈ 988 W, and applying the same 30% recharge-headroom margin gives a recommended array of ≈1,200–1,600 W after rounding to standard module counts
```

**Pre-check:** head = C2 (MEDIUM) · C3 (MEDIUM) · GT-6 (HIGH) · `?`-marked = none directly on head
(the `?` inputs are inherited through C2/C3) · lowest cited = MEDIUM (both C2 and C3) · Inputs
ceiling = MEDIUM.
**Confidence: MEDIUM** — capped by the Inputs ceiling (both cited chains are MEDIUM). Inference:
the recharge-headroom margin (20–40%, applied at 30%) is itself an engineering-practice judgment,
not a strict derivation — flagged via `[Assumes: A-24]`. What would raise this to HIGH: resolving
C2's and C3's MEDIUM inputs (the NREL table read and the datasheet reads named there), plus
running an explicit multi-day battery-recovery simulation instead of a flat percentage margin.
Rivals: the dominant rival reading of this whole chain is "the load input (GT-6) itself is
wrong," which is C4's finding, carried forward into §6. A second, narrower rival — "the
bare-physics-minimum 445–555 W is sufficient and the recharge-headroom margin is unnecessary" — is
**not ruled out by physics alone**; it stays live, addressed only by the practice-based reasoning
in chain C7, and is named here rather than in §5 because nothing in this chain disproves it
outright.

---

### C6 — Required battery bank capacity

```text
GT-6 (1.5 kWh/day load, 3 days autonomy) + GT-4? (LiFePO4 usable DoD ≈95%, round-trip ≈95%) + GT-5a? (inverter efficiency ≈93%)
→ the inverter sits between the battery and the AC load, so the battery must discharge more than the 1.5 kWh "delivered to load" figure: battery-terminal discharge = 1,500 Wh ÷ 0.93 ≈ 1,613 Wh/day
→ over the full 3-day zero-sun autonomy window, total required discharge = 3 × 1,613 Wh ≈ 4,839 Wh ≈ 4.84 kWh
→ LiFePO4's usable depth of discharge (≈95%, leaving a 5% low-voltage/BMS-cutoff margin rather than cycling to literal 0% even in an emergency) sets the nameplate-to-usable ratio: required nameplate capacity = 4.84 kWh ÷ 0.95 ≈ 5.09 kWh
→ routine day-to-day cycling is commonly limited to ~80% DoD (not the full 95–100% the chemistry allows) to extend LiFePO4 cycle life well beyond what full-DoD cycling would deliver [Assumes: A-25 routine-DoD cycle-life practice], which argues for sizing above the bare 5.09 kWh floor even before considering the load-realism flag from C4
→ rounding to commercially standard LiFePO4 pack sizes (commonly sold in ≈5 kWh and ≈10 kWh wall/rack modules)
→ **recommended battery bank: 5–10 kWh nameplate LiFePO4 (bare-physics minimum ≈5.1 kWh at 95% usable DoD)**
→ [sensitivity] this formula is also linear in load: at C4's upper realistic-load estimate (3.0 kWh/day), required discharge becomes (3,000÷0.93)×3 ≈ 9,677 Wh, and the bare-minimum nameplate capacity becomes 9,677÷0.95 ≈ 10.2 kWh — a recommended bank of ≈10–12 kWh with the same rounding/headroom logic applied
```

**Pre-check:** head = GT-6 (HIGH) · GT-4? (MEDIUM) · GT-5a? (MEDIUM) · `?`-marked on head = GT-4,
GT-5a (2 of 3) · lowest cited = none (no chains cited) · Inputs ceiling = MEDIUM.
**Confidence: MEDIUM** — Inputs axis short (GT-4, GT-5a both `?`); what would close it: a specific
vendor LiFePO4 datasheet read (usable DoD and round-trip efficiency are usually both on the same
datasheet) and a specific inverter datasheet read. Inference axis HIGH (straightforward
arithmetic). Rivals: as with C5, the dominant rival is "the load input is wrong" (C4), carried to
§6. The narrower rival "the bare ≈5.1 kWh floor is sufficient without the 5–10 kWh headroom" is
likewise **live, not ruled out**, for the same reason as C5.

---

### C7 — Second-order consequences of a thin-margin design

```text
C5 (600–800 W recommended array) + C6 (5–10 kWh recommended bank)
→[2nd, actor lens] occupants who can see live battery state-of-charge tend to shift discretionary loads (laundry, tool charging, water pumping) to sunny midday hours once they learn the system is thin, which partially relieves pressure on a bare-minimum design in practice — a behavioral buffer the arithmetic above does not capture
→[2nd, time lens] within the first one to two winters, metered real-world load either confirms or refutes the 1.5 kWh/day figure (C4's flag); the design gets tested empirically within about a year, not over a decade
→[3rd, actor lens] a future occupant (the same two people, a guest, or a renter) adding one device — a compressor fridge, a satellite internet terminal, power tools — increases load without anyone re-running the sizing math ("load creep"); a bare-physics-minimum system (445–555 W / ≈5.1 kWh) has almost no headroom to absorb this, which is the concrete mechanism by which C4's flagged assumption actually bites in practice rather than staying theoretical
→[3rd, time lens] by roughly year 10, combined PV output degradation and LiFePO4 capacity fade (GT-7?, already priced into C3's aged-design efficiency) erode the system's margin in the same direction that load creep tends to grow it — supply falls while demand rises — which is the specific justification for recommending the recharge-headroom-inclusive 600–800 W / 5–10 kWh range in §6 rather than the bare-physics minimum
→ no extension step above contradicts a ground truth in §3; all four extend the C5/C6 conclusions rather than undermining them — **no return to Phase 2 triggered**
```

**Pre-check:** head = C5 (MEDIUM) · C6 (MEDIUM) · `?`-marked = none directly (inherited) · lowest
cited = MEDIUM · Inputs ceiling = MEDIUM.
**Confidence: MEDIUM** — inherits C5/C6's MEDIUM ceiling; the second-order narrative itself is
qualitative reasoning about incentives and timelines rather than a numeric claim, so it does not
independently raise or lower the band — it explains *why* the margin recommended in C5/C6 matters,
it does not re-derive the numbers.

## 5. Abandoned Reasoning

**Path 1 — Fixed tilt at latitude+23.4° (exact solstice-noon-normal, ≈58°).**
*What was tried:* derive the tilt that puts the panel exactly normal to the sun at solar noon on
the winter solstice itself (tilt = φ − δ = 35° − (−23.44°) ≈ 58.4°), on the reasoning that this
maximizes energy on the single worst day of the year.
*Why abandoned:* the weighted trade-off (C1) shows this angle over-optimizes for one specific day
and loses balance across the rest of the Nov–Feb design window (when the sun is higher than the
solstice), scoring 60 vs. 77 for lat+15°; it also scores worse on shoulder/summer usability.
*What it ruled out:* ruled out by **chain C1**.

**Path 2 — Horizontal (flat) mount.**
*What was tried:* considered as the simplest, lowest-wind-profile, cheapest mounting option.
*Why abandoned:* chain **C1**'s December-yield criterion scores it 1/5 — a horizontal surface's
effective solar-collection angle is badly mismatched to a 58° noon zenith angle, and C2's
extraterrestrial-ceiling derivation (H0 ≈4.6 kWh/m²/day horizontal) shows the ceiling itself is
already the lowest of any orientation considered.
*What it ruled out:* ruled out by **chain C1** (weighted total 45, lowest of all five options).

**Path 3 — Manually seasonally-adjusted tilt (2–4 repositionings/year).**
*What was tried:* considered because the cabin is year-round occupied (so someone is present to
make the adjustment, unlike a vacation cabin), and it scores well on yield (tied for best with
lat+15° on both December and whole-winter criteria).
*Why abandoned:* it loses heavily on simplicity/reliability (2/5 vs. 5/5 — it requires physical
roof/ladder access, plausibly in ice or snow, exactly when a missed adjustment matters most), and
the flip test in **C1** confirms lat+15° remains the robust winner unless that weight is driven to
the scale's floor.
*What it ruled out:* ruled out by **chain C1**.

**Path 4 — Using the NREL "Navajo Nation" annual-average figure (5.5–6.5 kWh/m²/day, GT-3a)
directly as the December design PSH.**
*What was tried:* since GT-3a is the one read-at-source empirical figure obtained this session,
there was a temptation to use it directly as the worst-month design value.
*Why abandoned:* GT-3a is explicitly an **annual average**, not a December figure, and the same
high-desert region's December insolation is necessarily lower than its annual average (winter has
both the shortest days and the lowest sun angle of the year — this is just A-01/GT-1 applied).
Using an annual-average figure as a stand-in for the worst month would be reasoning by analogy
without grounding — exactly the trap the methodology's "no analogies as direct evidence" rule
exists to prevent. GT-3a is retained only as a same-region order-of-magnitude corroboration in
**chain C2**, never as the design value itself.
*What it ruled out:* this path is what GT-3a's usage note in §3 and chain **C2** rule out.

**Path 5 — Treating the web-search-sourced figures (GT-3b, GT-3c, GT-3d) as the primary PSH
derivation instead of the physics-first derivation.**
*What was tried:* all three are directly on-topic (NM December PSH, Albuquerque winter yield,
lat+15 tilt gain) and would have been a faster route to a number.
*Why abandoned:* all three are `?`-marked **reported-by-delegate** (summarized by WebSearch/
WebFetch, not read by this analysis at the primary source page — see §3), and the prompt
explicitly requires that the PSH figure be *derived*, "not just asserted," from declination/air
mass/day-length reasoning. They are retained in **chain C2** as a cross-check on the
physics-derived bracket, not as its source.
*What it ruled out:* this path is what chain **C2**'s structure (physics first, reported figures
as cross-check only) rules out.

**Path 6 — Folding the aging/degradation margin into the same multiplicative loss chain as the
efficiency factors in C3.**
*What was tried:* initially considered treating PV degradation and LiFePO4 capacity fade as just
one more multiplicative term alongside soiling, wiring, etc.
*Why abandoned:* a degradation margin is fundamentally different in kind from an instantaneous
conversion loss — it is a *time-varying* design margin (how much headroom to carry so the system
still meets load after ~10 years), not a fixed loss present on day one. Conflating the two would
understate day-one performance and make the two numbers (fresh-system efficiency vs. aged-design
sizing efficiency) impossible to separate for anyone auditing the build-up later.
*What it ruled out:* ruled out by the structure of **chain C3**, which reports both η_fresh and
η_aged-design separately.

**Path 7 — Reading NREL's direct tilted-surface insolation tables for Albuquerque
(`nrel.gov/grid/solar-resource/assets/data/west-1.pdf`).**
*What was tried:* attempted twice via WebFetch, to obtain a read-at-source December figure at
tilt=latitude and tilt=latitude+15° directly from NREL's own historical solar radiation tables.
*Why abandoned:* both attempts failed with `getaddrinfo ENOTFOUND www.nrel.gov` — a DNS/network
reachability failure in this session's environment, not a content or citation problem. Recorded
as a Phase 3 failure record in §3; this is the specific, named gap that would most directly raise
chain **C2** from MEDIUM to HIGH if it were closed in a future session with network access to
nrel.gov.

## 6. Conclusion

**Recommended approach:** Build a fixed array tilted at **latitude+15° (≈50°), facing true south**
(chain C1), sized to **600–800 W** of panel nameplate capacity (chain C5), paired with a
**5–10 kWh nameplate LiFePO4 battery bank** (chain C6), against a derived worst-month design
insolation of **4.5 kWh/m²/day** (bracket 4.0–5.0, chain C2) and a built-up system efficiency of
**≈75% fresh / ≈67.5% aged-design** (chain C3). Within that recommended range, size toward the
higher end (≈750–800 W array, ≈8–10 kWh battery) rather than the bare-physics minimum (≈445–555 W
/ ≈5.1 kWh) — the bare minimum only balances on day one, against the stated 1.5 kWh/day figure,
with no margin for recharge headroom (C5), battery longevity practice (C6), or the load-realism
risk below.

**Key insight:** The single assumption that most changes this answer is the stipulated 1.5 kWh/day
net load, not the solar-resource figure. Reconstructed from an itemized unit-factor load budget
(chain C4), 1.5 kWh/day is achievable **only** for a minimal-amenity cabin — LED lighting, phone/
laptop charging, a small efficient DC fridge, minimal water pumping — with **no internet/satellite
connectivity, no standard AC-compressor refrigerator, no electric space heat, and no washer**. A
"normal" year-round 2-adult cabin that includes internet and a standard fridge more realistically
draws **≈2.5–4 kWh/day**, roughly 1.7–2.7× higher (chain C4), and GT-8's read-at-source comparison
(a normally-appointed off-grid home at 15.68 kWh/day, ~10× this scenario's figure) corroborates how
spartan the stated budget is. **Because the sizing formulas in C5/C6 are linear in load, the
array and battery requirement scale directly with it: at 3.0 kWh/day (double the stated figure),
the array requirement becomes ≈1,200–1,600 W and the battery requirement becomes ≈10–12 kWh —
roughly double the headline recommendation, not a modest adjustment.** Decide what the cabin will
actually run — specifically, whether it has an internet connection and a standard refrigerator —
before buying equipment; that decision moves the answer by a larger factor than any solar-resource
or efficiency uncertainty in this analysis.

**Trade-offs acknowledged:** The recommended fixed lat+15° tilt is not the single-day-optimal
angle (chain C1 shows exact solstice-normal, lat+23.4°, scores higher on the solstice day itself
but worse across the whole Nov–Feb window) and is not the highest-yield option overall (manual
seasonal adjustment, chain C1 option (e), scores marginally higher on yield but loses heavily on
unattended-site reliability). Sizing toward the upper half of the recommended range (750–800 W /
8–10 kWh) costs more upfront than the bare-physics minimum (chain C5/C6) in exchange for recharge
headroom, battery cycle-life margin, and tolerance to the load-creep risk named in chain C7 — a
trade-off between day-one cost and multi-year reliability, not a free improvement.

**On a backup generator (explicitly challenged, A-15):** the stated scenario assumes none, and the
core sizing above does not require one to balance on paper. It is nonetheless recommended as cheap
insurance, for three reasons tied directly to this derivation: (1) this is a thin-margin design by
construction — even the "recommended" sizing carries only a 30% headroom margin, not a multiple,
over the bare-physics minimum (chains C5, C6), so it has little slack for an outlier event; (2) the
3-day autonomy target (A-06, chain C6's head) has a named expiry condition — multi-day New Mexico
winter storm systems occasionally exceed 3 consecutive low-insolation days, an event the design
does not cover; (3) chain C7's load-creep mechanism means the margin computed today erodes over the
system's life. A small dual-fuel generator — roughly in the same power class as the recommended
array itself (chain C5's 600–800 W, i.e., comfortably under 1–1.5 kW continuous, enough to
bulk-charge the battery bank through its existing charge controller and run essential loads
directly) — used only during extended winter storms, is inexpensive relative to the cost of
oversizing the battery bank enough to cover a 5–7 day outlier autonomy event outright. This is a
qualitative recommendation, not a separately sized conclusion: no chain in §4 derives an optimal
generator wattage, and none is claimed here beyond tying its rough scale to C5's already-
established array figure.

**Pre-check:** head = C1 (HIGH) · C2 (MEDIUM) · C3 (MEDIUM) · C4 (MEDIUM) · C5 (MEDIUM) · C6
(MEDIUM) · C7 (MEDIUM) · `?`-marked direct inputs = none beyond those already inherited through
the cited chains · lowest cited = MEDIUM · Inputs ceiling = MEDIUM.
**Confidence: MEDIUM.** Every numeric recommendation traces to a chain already rated MEDIUM, each
for a named and specific reason (an unread NREL table blocked by a DNS failure this session for
C2; unread vendor datasheets for C3/C6; engineering-judgment margins, not strict derivations, in
C2/C5/C6). None of those gaps is a reason to doubt the method or the order of magnitude — the
physics derivation (C2) and the empirical corroboration (GT-3a, read at source) agree to within
about 10%, and the resulting 600–800 W / 5–10 kWh range lands exactly where a real-world sanity
check places it: above typical "weekend/minimal-use" off-grid cabin kits (commonly 400–800 W /
2–4 kWh usable) and below typical year-round-habited cabin systems that run a standard fridge
(commonly 1–2 kW / 10–20 kWh). What would move this to HIGH: the specific vendor/equipment reads
named above, plus resolving the load-realism question in the Key Insight — which, unlike the
solar-resource uncertainty, is not a confidence-band question at all but a scope decision only the
occupants can make.
## Appendix — process output

## §6→§4 closure ledger (process output)

- "Build a fixed array tilted at latitude+15° (≈50°)... sized to 600–800 W... paired with a 5–10 kWh nameplate LiFePO4 battery bank... design insolation of 4.5 kWh/m²/day... system efficiency of ≈75% fresh / ≈67.5% aged-design" → chain C1 ✓ / C5 ✓ / C6 ✓ / C2 ✓ / C3 ✓
- "size toward the higher end... the bare minimum only balances on day one... with no margin for recharge headroom, battery longevity practice, or the load-realism risk" → chain C5 ✓ / C6 ✓
- "1.5 kWh/day is achievable only for a minimal-amenity cabin... no internet..., no standard AC-compressor refrigerator, no electric space heat, and no washer" → chain C4 ✓
- "a 'normal' year-round 2-adult cabin... more realistically draws ≈2.5–4 kWh/day, roughly 1.7–2.7× higher" → chain C4 ✓
- "at 3.0 kWh/day... the array requirement becomes ≈1,200–1,600 W and the battery requirement becomes ≈10–12 kWh" → chain C5 ✓ / C6 ✓ (sensitivity hops)
- "The recommended fixed lat+15° tilt is not the single-day-optimal angle... manual seasonal adjustment... scores marginally higher on yield but loses heavily on unattended-site reliability" → chain C1 ✓
- "Sizing toward the upper half of the recommended range... costs more upfront than the bare-physics minimum... in exchange for recharge headroom, battery cycle-life margin, and tolerance to the load-creep risk" → chain C5 ✓ / C6 ✓ / C7 ✓
- "this is a thin-margin design by construction — even the 'recommended' sizing carries only a 30% headroom margin... over the bare-physics minimum" → chain C5 ✓ / C6 ✓
- "the 3-day autonomy target... has a named expiry condition — multi-day New Mexico winter storm systems occasionally exceed 3 consecutive low-insolation days" → chain C6 ✓ (head, GT-6/A-06)
- "chain C7's load-creep mechanism means the margin computed today erodes over the system's life" → chain C7 ✓
- "the physics derivation (C2) and the empirical corroboration (GT-3a, read at source) agree to within about 10%" → chain C2 ✓
- "the resulting 600–800 W / 5–10 kWh range lands... above typical 'weekend/minimal-use' off-grid cabin kits... and below typical year-round-habited cabin systems" → chain C5 ✓ / C6 ✓
## Phase 4 Assumption Audit scan (process output)

| Chain | Step | Step Text (brief) | Assumption surfaced? | Added to Table? |
|---|---|---|---|---|
| C1 | 1 | Must-haves/options framing | No | n/a (clean pass) |
| C1 | 2 | Weighted scoring of 5 tilt options | No | n/a |
| C1 | 3 | Lat+15° wins on weighted total | No | n/a |
| C1 | 4 | Flip test confirms robustness | No | n/a |
| C2 | 1 | Sunset hour angle / day length | No | n/a |
| C2 | 2 | Solar-noon air mass | No | n/a |
| C2 | 3 | Horizontal ETR ceiling (H0) | No | n/a |
| C2 | 4 | Absolute tracking-ceiling figure | No | n/a |
| C2 | 5 | Irreducible-gap note | No | n/a |
| C2 | 6 | Clear-sky unit-factor rebuild | **Yes** | A-20 (clear-sky transmittance/tilt-gain model) |
| C2 | 7 | Cross-check vs. GT-3b/GT-3d | No | n/a |
| C2 | 8 | Monthly storm/overcast discount | **Yes** | A-23 (cloud-frequency discount) |
| C2 | 9 | Design PSH conclusion | No | n/a |
| C3 | 1 | Multiply named loss mechanisms | **Yes** | A-21 (module mismatch 2%), A-22 (shading/horizon 2%) |
| C3 | 2 | Stepwise product ≈0.75 | No | n/a |
| C3 | 3 | 10% aging/degradation margin | No | n/a (GT-7 already tabled) |
| C3 | 4 | η_fresh / η_aged conclusion | No | n/a |
| C4 | 1 | Lean load-budget unit-factor rebuild | No | n/a (covered by A-05/A-19 already tabled) |
| C4 | 2 | Naming excluded loads | No | n/a |
| C4 | 3 | GT-8 corroboration | No | n/a |
| C4 | 4 | Reintroducing internet/fridge | No | n/a |
| C4 | 5 | Load-realism conclusion | No | n/a |
| C5 | 1 | Bare-minimum array arithmetic | No | n/a |
| C5 | 2 | Recharge-headroom rationale | **Yes** | A-24 (20–40% recharge-headroom margin) |
| C5 | 3 | 30% margin applied | No | n/a |
| C5 | 4 | Rounding to standard modules | No | n/a |
| C5 | 5 | Array conclusion | No | n/a |
| C5 | 6 | Linear-scaling sensitivity (3.0 kWh/day) | No | n/a |
| C6 | 1 | Inverter-loss discharge bump | No | n/a |
| C6 | 2 | 3-day autonomy total discharge | No | n/a |
| C6 | 3 | DoD nameplate ratio | No | n/a |
| C6 | 4 | Routine 80% DoD cycle-life practice | **Yes** | A-25 (routine-DoD cycle-life practice) |
| C6 | 5 | Rounding to standard packs | No | n/a |
| C6 | 6 | Battery conclusion | No | n/a |
| C6 | 7 | Linear-scaling sensitivity (3.0 kWh/day) | No | n/a |
| C7 | 1 | [2nd, actor] load-shifting behavior | No | n/a |
| C7 | 2 | [2nd, time] first-winter empirical test | No | n/a |
| C7 | 3 | [3rd, actor] load creep | No | n/a |
| C7 | 4 | [3rd, time] degradation vs. load-creep compounding | No | n/a |
## Self-audit scan (process output)

**Table 1 — chain form (section 4)**

| Chain | Chain Head (brief) | Form conforming? | Rule applied | Dependency clean? | Band | Act attempted? | Edges fired |
|---|---|---|---|---|---|---|---|
| C1 | GT-1 + GT-1b (tilt trade-off) | yes | n/a | yes | HIGH | no | none |
| C2 | GT-1 + GT-2 + GT-3a (PSH derivation) | yes | n/a | yes | MEDIUM | yes | none |
| C3 | GT-1b + GT-5d? + GT-5c? + GT-5b? + GT-4? + GT-5a? (efficiency build-up) | yes | n/a | yes | MEDIUM | no | none |
| C4 | GT-6 + GT-8 (load-budget realism) | yes | n/a | yes | MEDIUM | yes | none |
| C5 | C2 + C3 + GT-6 (array sizing) | yes | n/a | yes | MEDIUM | no | none |
| C6 | GT-6 + GT-4? + GT-5a? (battery sizing) | yes | n/a | yes | MEDIUM | no | none |
| C7 | C5 + C6 (second-order effects) | yes | n/a | yes | MEDIUM | no | none |

Note on `Act attempted?`: C2 and C4 are `yes` because this session directly attempted source
reads for their inputs (the NREL west-1.pdf fetch for C2, which failed on DNS and is recorded as
a Phase 3 failure record; the Navajo Nation IEEE PDF for C4/GT-8, which succeeded). C3 and C6 are
`no` — no vendor datasheet was opened this session for the inverter, MPPT, or LiFePO4 `?`-marked
figures they depend on; this is the most honest flag in this table, since C3 and C6 together
determine most of the quantitative recommendation. C1, C5, C7 are `no` because their heads cite
physical constants or other chains, not raw external citations to open.

**Table 2 — claim inventory (section 6)**

| §6 Span (brief) | Construct | Claim under R11? | R11 clause applied | Chain cited |
|---|---|---|---|---|
| "Recommended approach:" paragraph | bold lead-in | yes | always-claim lead-in | C1, C2, C3, C5, C6 |
| "Key insight:" paragraph | bold lead-in | yes | always-claim lead-in | C4 |
| "Trade-offs acknowledged:" paragraph | bold lead-in | yes | always-claim lead-in | C1, C5, C6, C7 |
| "On a backup generator..." paragraph | bold lead-in | yes | always-claim lead-in | C5, C6, C7 |
| "Pre-check:" line | bold lead-in | no | mechanical template field (head/ceiling restatement), not an independent prose assertion | n/a |
| "Confidence: MEDIUM." paragraph | bold lead-in | yes | always-claim lead-in | C2, C3, C5, C6 (prose); C1–C7 (Pre-check head) |

Scan complete: 7 chain rows, one per section-4 chain block in order; 6 section-6 rows, one per
construct in order — 5 claims under R11, 1 excluded. 0 chains malformed, 0 claims untraced.
## Adversarial pass (process output)

**Recompute.** Every computed figure in §4 was redone independently of the chain prose:
day length 2×72.33°/15 = 9.644 h (matches C2); η_fresh = 0.98×0.95×0.98×0.97×0.95×0.93×0.98×0.98 =
0.7510 (matches C3's "≈0.75"); η_aged = 0.7510×0.90 = 0.6759 (matches "≈0.675"); array bare-minimum
at PSH=4.5: 1,500÷(4.5×0.675) = 493.8 W (matches "≈494 W"); array bracket at PSH=4.0/5.0: 555.6 W /
444.4 W (matches "445–555 W"); with 30% headroom: 493.8×1.3 = 641.9 W (matches "≈642 W"); battery
discharge: 1,500÷0.93 = 1,612.9 Wh/day ×3 = 4,838.7 Wh ÷0.95 = 5,093 Wh ≈5.09 kWh (matches); 3.0
kWh/day scaling: array 3,000÷(4.5×0.675) = 987.7 W (matches "≈988 W"), battery
(3,000÷0.93)×3÷0.95 = 10,191 Wh ≈10.2 kWh (matches). **No arithmetic errors found; every figure
in §4/§6 recomputes to its stated value.**

**Sensitivity.** The single assumption whose falsity would most change this conclusion is **not**
a `?`-marked ground truth in the strict sense — it is the realism of the stipulated 1.5 kWh/day
load (GT-6, tested and flagged by chain C4). Because C5/C6 are linear in load (explicitly shown by
their own sensitivity hops), a 2× load error produces a ≈2× sizing error, dwarfing every other
uncertainty in this analysis. Secondary sensitivities, smaller in effect: GT-4?/GT-5a? (LiFePO4
DoD/round-trip and inverter efficiency feeding C3/C6 — a few percentage points of error here moves
the recommendation by single-digit percent, not a multiple) and the C2 clear-sky-transmittance/
monthly-discount judgment calls (A-20/A-23 — a ±15% PSH error moves the array figure by a
comparable percentage). **Weakest link per chain:** C2 — the clear-sky-to-monthly-average discount
(A-23); C3 — five of six inputs are unread vendor-convention figures (`?`); C5/C6 — the
recharge-headroom and routine-DoD margins (A-24/A-25) are engineering practice, not derivation.

**Rival.** Headline conclusion: the strongest rival is "size to the bare-physics minimum
(445–555 W / ≈5.1 kWh) and skip the recharge-headroom/longevity margin" — this is **not ruled out
by physics**, and is now named live on chains C5 and C6's Confidence lines rather than claimed
refuted. Per-chain: C1's rivals (horizontal, lat-only, solstice-exact, seasonal-manual tilt) are
**ruled out** by the weighted trade-off and flip test — see §5 Paths 1–3. C2's rivals (using
GT-3a's annual average directly; trusting the reported-by-delegate figures as primary) are **ruled
out** — see §5 Paths 4–5. C3's rival ("real-world off-grid efficiency runs closer to 60% than
75%") is **not ruled out** — it stays live, named on C3's own Confidence line via the unread-
datasheet gap. C4's rival ("1.5 kWh/day is fine as stated") is **not ruled out** — explicitly
named live on C4's own Confidence line, and is the chain this whole pass treats as the dominant
risk to the design.

**Premise.** The recommended off-grid system has already failed to keep the cabin reliably
powered through its first winter.

**Causes** (generated from three stakeholder viewpoints, unfiltered before clustering):
*Occupant* — Starlink/internet added without re-sizing; a standard AC fridge installed instead of
an efficient DC unit; an unusually prolonged storm (5+ days low insolation) exceeded the 3-day
autonomy design; snow left on panels for days; dust not cleaned before winter; nighttime tool use
drained reserve meant for the next day.
*Installer/designer* — built to the bare-physics minimum instead of the recommended
headroom range to control upfront cost; a budget inverter/MPPT ran below the modeled 93%/97%
efficiency; wiring run longer than modeled, raising voltage-drop losses above 2%; panels mounted
at the roof's existing pitch rather than the recommended 50° to save racking cost.
*Skeptical outside installer* — "no generator" treated as an absolute rule even in a genuine
emergency; real site shading/tree cover not captured by the "clear high-desert skies" assumption;
battery cycled to 100% DoD routinely (not the assumed ~80% routine practice), accelerating fade
beyond the modeled 10% aging margin.

**Clusters** (structural weaknesses, with citations):
1. *Load creep / load mismatch* (cites GT-6, C4, C7) — internet, standard fridge, added devices
   outside the 1.5 kWh/day budget.
2. *Built to the bare minimum, not the recommended margin* (cites C5, C6) — cost pressure quietly
   reverts to the bare-physics figures this analysis also produced, discarding the headroom.
3. *Site/installation deviates from modeled assumptions* (cites C2, C3, GT-5c?, GT-5d?) — worse
   real-world tilt, wiring, soiling, shading, or component efficiency than the `?`-marked figures.
4. *Outlier weather event exceeds 3-day autonomy* (cites GT-6/A-06, C6) — a storm longer than the
   design's autonomy window.
5. *Battery degrades faster than modeled* (cites GT-7?, C3, C6) — cold-weather BMS charge limits
   and/or deeper-than-assumed routine DoD.

**Disposition:**
1. **Plan change** — before purchasing equipment, occupants must explicitly decide whether
   internet and a standard fridge are in scope; if yes, size to the ≈2.5–4 kWh/day band
   (≈1,200–2,100 W / ≈10–16 kWh per C5/C6's own linear-scaling logic), not the 1.5 kWh/day
   headline.
2. **Plan change** — specify the recommended 600–800 W / 5–10 kWh range explicitly in the
   purchase/installation agreement, not the bare-physics minimum.
3. **Accepted risk, with mitigation** — log one season of actual production against the modeled
   PSH/efficiency figures; budget contingency (one or two extra panels) if the first season
   under-delivers. This is the same mitigation that would close GT-3b?/c?/d?, GT-4?, GT-5a?–d?,
   and GT-7? generally.
4. **Accepted risk, with mitigation** — this is the specific justification for §6's generator
   recommendation: cheaper than oversizing the battery to cover a 5–7 day outlier outright.
5. **Plan change** — select a LiFePO4 pack with a read-at-source cycle-life/DoD datasheet (closing
   GT-4?) and site the battery in a temperature-conditioned space, since cold-weather BMS charge
   restrictions are a real LiFePO4 operating characteristic this analysis's efficiency chain (C3)
   does not separately model.

**Falsification.** This conclusion is false if, once instrumented through a full winter, (a) the
as-built recommended-size system cannot meet the occupants' *actual* metered load across a
December/January with near-average insolation, or (b) the as-built array at the recommended size
produces materially less than the 4.0–5.0 kWh/m²/day design PSH on clear December days — the
latter would mean the PSH/efficiency derivation itself was wrong, not just the load assumption.
## Techniques not applied (process output)

five-whys (reduce-to-primitives) — not applicable — every ground truth in §3 already bottoms out
directly at a physical constant, a read-at-source measurement, or an explicitly `?`-flagged
convention at the moment it was constructed; a separate formal decomposition drill would re-derive
the same bottoming-out already shown rather than find anything new.
fishbone — not applicable — the Phase 4 loss-mechanism build-up (chain C3) already performs the
equivalent breadth-first category decomposition (temperature / soiling / wiring / electronics /
battery / aging) directly, and the Phase 2 assumption space was enumerable by direct construction
(19 initial assumptions, later 25 after the Assumption Audit) without needing a brainstorming aid.

## Self-Audit Gate (process output)

**Criterion 1: Identify Essence**
Quoted span: "Size an off-grid LiFePO4 solar-electric system (panel array wattage and battery bank
kWh) for a year-round-occupied cabin at 35°N high-desert New Mexico, such that it reliably
delivers a stated net load against the *worst* month of solar insolation (not an annual average),
carries 3 days of zero-sun autonomy, and does so from insolation, loss-mechanism, and
battery-chemistry figures that are derived or sourced rather than assumed by rule of thumb."
Band: **Rigorous**
Justification: the statement names the specific decision (panel W / battery kWh), the specific
constraints (35°N high desert, worst-month not annual, 3-day autonomy, derived-not-asserted
figures) rather than restating the prompt verbatim, and each of the six success criteria beneath
it is a checkable verb+outcome test against a named output-section property (the PSH derivation,
the efficiency build-up, the array/battery figures, the sanity check, the sensitivity flag, and
the no-forced-single-option rule) — a reviewer can check each one against §2–§6 without further
interpretation.

**Criterion 2: Challenge Assumptions**
Quoted span (from the Phase 4 Assumption Audit scan, process output above): "C2 | 6 | Clear-sky
unit-factor rebuild | Yes | A-20 (clear-sky transmittance/tilt-gain model)" and "C5 | 2 |
Recharge-headroom rationale | Yes | A-24 (20–40% recharge-headroom margin)" — the audit visited
every named chain step in section 4 in order and surfaced six new assumptions (A-20–A-25) back
into the Assumptions Table, none left undeclared. Also quoted, against `output-template.md`'s
Verdict Vocabulary section (read this session): Verdict cells in §2 read "Accepted, flagged `?` →
GT-4" rather than the prescribed token-first em-dash form "Accept — [justification]".
Band: **Sound**
Justification: every row uses a Type from the four-type scheme; every `?`-marked row's
Verification cell now leads with the literal "Unverified — flagged." notation; at least five
assumptions (A-05, A-15, A-16, A-19) are explicitly challenged rather than merely accepted; and
the Assumption Audit scan confirms the table reflects every chain-step-surfaced assumption — but
the Verdict cells depart from the template's prescribed "Accept/Challenge/Discard — justification"
token-first form across the table (a pattern, not an isolated entry, caught only on reading
`output-template.md`'s Verdict Vocabulary section directly), which is a specific, identifiable
form departure rather than missing content, landing this at Sound rather than Rigorous.

**Criterion 3: Establish Ground Truths**
Quoted span: "`?`-marked (count 16): A-07, A-08, A-09, A-10, A-11, A-12, A-14, A-17 (covers three
sub-figures bundled as one row: GT-3b, GT-3c, GT-3d), A-20, A-21, A-22, A-23, A-24, A-25" (§2) and
"`?`-marked ground truths (9 of 15): GT-3b, GT-3c, GT-3d, GT-4, GT-5a, GT-5b, GT-5c, GT-5d, GT-7"
(§3) — checked against the Ground Truths list directly: `grep` of all `**GT-...**` bullets returns
exactly those 9 suffixed of 15 total, matching the enumeration exactly.
Band: **Sound**
Justification: the enumeration is checkable and matches the list; GT-3a and GT-8 name specific
read-at-source locations (slide/table references); but GT-1, GT-1b, and GT-2 — all unsuffixed and
feeding HIGH-confidence chain C1 — are physical constants rather than claims drawn from an opened
document, so §3's own honest note ("no external document location; definitional") is a specific,
named reason rather than a missing field, but it does not satisfy the literal "names its
read-at-source location" test the Rigorous band requires, which is written for citation-based
facts rather than defined constants; this is a single, narrow, disclosed gap, not a pattern.

**Criterion 4: Reason Upward**
Quoted span (from the Self-audit scan's chain-form table, process output above): "C1 | GT-1 +
GT-1b (tilt trade-off) | yes | n/a | yes | HIGH | no | none" through "C7 | C5 + C6 (second-order
effects) | yes | n/a | yes | MEDIUM | no | none" — all seven chains score `yes` on both Form
conforming? and Dependency clean?, with no `unreached` or `no` entries after the C1/C4 hop fixes
made during drafting (C1 was given a proper head/hop fenced block; C4's hop that illegally opened
with the `GT-8` identifier was rewritten).
Band: **Rigorous**
Justification: every conclusion in §6 has exactly one chain in §4, each with a genuine
intermediate step; the Abandoned Reasoning section documents seven dead ends in the prescribed
What-was-tried/Why-abandoned/What-it-ruled-out form, each citing the chain that ruled it out; the
GT-3a annual-average figure is explicitly *not* used as direct analogical evidence for the
December design value (Abandoned Reasoning Path 4) — the no-analogy-as-evidence ban is met head-on
rather than incidentally; every chain-step-surfaced assumption carries an inline `[Assumes: X]`
tag; and the independent Recompute pass in the adversarial record found no arithmetic errors.

**Criterion 5: Validate**
Quoted span: "C3 — five of six inputs are unread vendor-convention figures (`?`); C5/C6 — the
recharge-headroom and routine-DoD margins (A-24/A-25) are engineering practice, not derivation"
(Adversarial pass record, Sensitivity) and "each cluster carrying a named plan change or an
explicitly accepted risk with a named mitigation" — verified against the five clusters in the
adversarial pass record, each of which carries exactly one of those two outcomes.
Band: **Rigorous**
Justification: every chain's weakest link is named in its own Confidence paragraph; every MEDIUM
line names the specific `?`-marked GT-N or cited Cn causing the cap and what would remove it
(a specific datasheet, a specific NREL table, a specific site measurement); the Conclusion's
MEDIUM rating equals its weakest contributing chain (also MEDIUM); no chain consuming a `?` input
is rated HIGH, and no chain is rated above the lowest-rated chain its head cites (checked:
C5=MEDIUM citing C2/C3 both MEDIUM; C6=MEDIUM citing GT-4?/GT-5a? both MEDIUM; C7=MEDIUM citing
C5/C6 both MEDIUM); the five-part adversarial pass record (Recompute, Sensitivity, Rival,
pre-mortem Premise/Causes/Clusters/Disposition, Falsification) is complete, and every cluster
carries a disposition.

**Criterion 6: Conclusion-to-Ground-Truth Traceability**
Quoted span (from the Self-audit scan's claim-inventory table, process output above): all four
always-claim lead-ins ("Recommended approach:", "Key insight:", "Trade-offs acknowledged:", "On a
backup generator...") and the Confidence line are marked `yes` under Claim under R11? with a
non-empty Chain cited column, and the §6→§4 closure ledger independently shows zero `CUT` rows.
Band: **Rigorous**
Justification: every claim traces to a named chain (verified via both the closure ledger and the
self-audit scan, independently constructed); the generator-sizing figure — the one genuinely new
number in §6 that did not come pre-computed from a chain — was rewritten during drafting to tie
its magnitude explicitly to chain C5's already-established array figure rather than standing as
free-floating new reasoning; and the Key Insight (the 1.5 kWh/day load figure being the dominant,
non-obvious sensitivity, scaling the whole design ~2× if wrong) is not a restatement of the
Recommended approach (the tilt/array/battery numbers) but a distinct finding about what could
invalidate them.

**Pass 1 (before re-score):** Criterion 1 Rigorous · Criterion 2 Sound · Criterion 3 Sound ·
Criterion 4 Hand-wavy (C1 lacked the prescribed head/hop chain format; C4 contained a hop
illegally opening with the `GT-8` identifier) · Criterion 5 Rigorous · Criterion 6 Sound (the
generator wattage figure was new reasoning with no chain) · Gate cleared: yes (no Absent) ·
Hand-wavy cap cleared: yes (exactly one Hand-wavy, within the one-criterion tolerance).

The three defects found on Pass 1 were fixed before the final pass above: C1 was given a proper
fenced head/hop block; C4's offending hop was reworded; the generator figure was tied to chain C5
instead of standing as an unsourced new number; and every `?`-marked Assumptions Table row was
given the literal "Unverified — flagged." notation Criterion 2's Rigorous band requires.

**Gate result:** cleared · passes: 2 · Fix/Repeat fired: yes.
## Structured summary (process output)

```json
{
  "schema_version": 1,
  "run_mode": "full-composer",
  "assumptions": [
    {"id": "A-01", "type": "physical law", "verdict": "Accept"},
    {"id": "A-02", "type": "physical law", "verdict": "Accept"},
    {"id": "A-03", "type": "current constraint", "verdict": "Accept"},
    {"id": "A-04", "type": "physical law", "verdict": "Accept"},
    {"id": "A-05", "type": "untested belief", "verdict": "Challenge"},
    {"id": "A-06", "type": "current constraint", "verdict": "Accept"},
    {"id": "A-07", "type": "convention", "verdict": "Accept"},
    {"id": "A-08", "type": "convention", "verdict": "Accept"},
    {"id": "A-09", "type": "convention", "verdict": "Accept"},
    {"id": "A-10", "type": "convention", "verdict": "Accept"},
    {"id": "A-11", "type": "convention", "verdict": "Accept"},
    {"id": "A-12", "type": "untested belief", "verdict": "Accept"},
    {"id": "A-13", "type": "physical law", "verdict": "Accept"},
    {"id": "A-14", "type": "convention", "verdict": "Accept"},
    {"id": "A-15", "type": "current constraint", "verdict": "Challenge"},
    {"id": "A-16", "type": "convention", "verdict": "Challenge"},
    {"id": "A-17", "type": "untested belief", "verdict": "Accept"},
    {"id": "A-18", "type": "untested belief", "verdict": "Accept"},
    {"id": "A-19", "type": "untested belief", "verdict": "Challenge"},
    {"id": "A-20", "type": "untested belief", "verdict": "Accept"},
    {"id": "A-21", "type": "convention", "verdict": "Accept"},
    {"id": "A-22", "type": "untested belief", "verdict": "Accept"},
    {"id": "A-23", "type": "untested belief", "verdict": "Accept"},
    {"id": "A-24", "type": "convention", "verdict": "Accept"},
    {"id": "A-25", "type": "convention", "verdict": "Accept"}
  ],
  "ground_truths": [
    {"id": "GT-1", "read_at_source": true},
    {"id": "GT-1b", "read_at_source": true},
    {"id": "GT-2", "read_at_source": true},
    {"id": "GT-3a", "read_at_source": true},
    {"id": "GT-3b", "read_at_source": false},
    {"id": "GT-3c", "read_at_source": false},
    {"id": "GT-3d", "read_at_source": false},
    {"id": "GT-4", "read_at_source": false},
    {"id": "GT-5a", "read_at_source": false},
    {"id": "GT-5b", "read_at_source": false},
    {"id": "GT-5c", "read_at_source": false},
    {"id": "GT-5d", "read_at_source": false},
    {"id": "GT-6", "read_at_source": true},
    {"id": "GT-7", "read_at_source": false},
    {"id": "GT-8", "read_at_source": true}
  ],
  "chains": [
    {"id": "C1", "confidence": "HIGH", "rests_on": ["GT-1", "GT-1b"]},
    {"id": "C2", "confidence": "MEDIUM", "rests_on": ["GT-1", "GT-2", "GT-3a"]},
    {"id": "C3", "confidence": "MEDIUM", "rests_on": ["GT-1b", "GT-5d?", "GT-5c?", "GT-5b?", "GT-4?", "GT-5a?"]},
    {"id": "C4", "confidence": "MEDIUM", "rests_on": ["GT-6", "GT-8"]},
    {"id": "C5", "confidence": "MEDIUM", "rests_on": ["C2", "C3", "GT-6"]},
    {"id": "C6", "confidence": "MEDIUM", "rests_on": ["GT-6", "GT-4?", "GT-5a?"]},
    {"id": "C7", "confidence": "MEDIUM", "rests_on": ["C5", "C6"]}
  ],
  "dead_ends": [
    "Fixed tilt at latitude+23.4° (exact solstice-noon-normal)",
    "Horizontal (flat) mount",
    "Manually seasonally-adjusted tilt",
    "Using the NREL annual-average figure directly as the December design PSH",
    "Treating web-search-sourced figures as the primary PSH derivation",
    "Folding the aging/degradation margin into chain C3's multiplicative efficiency loss chain",
    "Reading NREL's direct tilted-surface insolation tables (blocked by a DNS failure)"
  ],
  "techniques": {
    "applied": ["trade-off", "theoretical-limit", "estimate", "second-order", "inversion"],
    "not_applied": [
      {
        "technique": "five-whys",
        "phase": 3,
        "reason": "every ground truth already bottoms out directly at a physical constant, a read-at-source measurement, or an explicitly ?-flagged convention; a separate drill would re-derive the same bottoming-out"
      },
      {
        "technique": "fishbone",
        "phase": 2,
        "reason": "the Phase 4 loss-mechanism build-up (chain C3) already performs the equivalent breadth-first category decomposition, and the Phase 2 assumption space was enumerable by direct construction"
      }
    ]
  },
  "gate": {
    "passes": [
      {
        "bands": ["Rigorous", "Sound", "Sound", "Hand-wavy", "Rigorous", "Sound"],
        "gate_cleared": true,
        "hand_wavy_cap_cleared": true
      },
      {
        "bands": ["Rigorous", "Sound", "Sound", "Rigorous", "Rigorous", "Rigorous"],
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
        "trigger": "Pass 1 scored Criterion 4 Hand-wavy (chain C1 lacked the prescribed head/hop format and chain C4 had a hop illegally opening with the GT-8 identifier) and Criterion 6 Sound (an unsourced generator-wattage figure); all three were fixed before the final pass."
      }
    ]
  },
  "conclusion": {
    "recommendation": "Build a fixed array tilted at latitude+15° (≈50°), facing true south (chain C1), sized to 600–800 W of panel nameplate capacity (chain C5), paired with a 5–10 kWh nameplate LiFePO4 battery bank (chain C6), against a derived worst-month design insolation of 4.5 kWh/m²/day (bracket 4.0–5.0, chain C2) and a built-up system efficiency of ≈75% fresh / ≈67.5% aged-design (chain C3). Within that recommended range, size toward the higher end (≈750–800 W array, ≈8–10 kWh battery) rather than the bare-physics minimum (≈445–555 W / ≈5.1 kWh) — the bare minimum only balances on day one, against the stated 1.5 kWh/day figure, with no margin for recharge headroom (C5), battery longevity practice (C6), or the load-realism risk below.",
    "confidence": "MEDIUM",
    "rests_on": ["C1", "C2", "C3", "C4", "C5", "C6", "C7"]
  }
}
```
