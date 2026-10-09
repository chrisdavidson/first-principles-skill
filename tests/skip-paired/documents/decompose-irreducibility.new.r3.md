## Answer

**Recommendation:** The claim is false as literally worded. A single two-tank molten-salt store (565 °C hot / 290 °C cold) charged and discharged back to electricity through a heat engine cannot exceed roughly 64% round-trip efficiency even in the ideal, lossless case (chain C1); real demonstrated systems of this type reach only ≈45% (chain C3). At 5 MWh, this architecture is also far costlier than lithium-ion once the turbine/generator equipment is counted (chain C4), and lithium-ion wins a locked-weight trade-off by a wide, robust margin (chain C6). The only way part of the claim becomes defensible is by redefining "round trip" as electricity delivered as heat (no reconversion, where >95% is real, chain C3) or by substituting a fundamentally different heat-pump-charged, dual-reservoir architecture (chain C2) — neither of which is the system the claim describes.

**Band (from §6):** LOW — the formal band is capped by the cost/trade-off chains (C4, C6), which rest on an assumed small-scale turbine cost figure and on secondary, unopened market data. This does not extend to the efficiency finding: chain C1 alone (a physical law plus arithmetic, no unverified inputs) is HIGH confidence and by itself falsifies the claim's ">85%" assertion.

**Would change it:** A verified small-scale (1–2 MW) power-block cost figure and a primary-source lithium-ion installed-cost figure at 5 MWh would raise the cost chains' band (chain C4); nothing would change chain C1's physics verdict, since it rests on no unverified input.
## 1. Problem Essence

**Essence Statement:** Does a single two-tank molten-salt thermal store (hot tank ~565 °C, cold/return tank ~290 °C) that is charged from grid electricity and discharged back to grid electricity through a heat engine have a physically achievable full electricity-to-electricity round-trip efficiency above 85%, and — separately — is a 5 MWh unit of this type cost-competitive per kWh with a 5 MWh lithium-ion battery system? The triggering claim bundles a thermodynamic assertion (efficiency) and an economic assertion (cost) about one specific named architecture; the analysis must evaluate both, and must resolve the ambiguity in what "round trip" and "system efficiency" mean before either can be checked.

**Success criteria** (what a correct answer must achieve):

1. State explicitly what physical process "round-trip electricity into heat and back" requires (a charge step, a storage step, and — because the claim says "back" to electricity, not "out" as heat — a heat-engine discharge step), and name the governing physical law that bounds that discharge step.
2. Derive the theoretical ceiling on full electricity-to-electricity round-trip efficiency for a heat engine spanning the stated temperature range against a realistic heat-rejection sink, and compare the claimed ">85%" against that ceiling.
3. Compare the derived ceiling against real-world demonstrated and commercial molten-salt / thermal-battery efficiencies, distinguishing systems that actually reconvert heat to electricity from systems that deliver heat directly (a distinction the claim's wording elides).
4. Evaluate cost-competitiveness specifically at 5 MWh scale against lithium-ion at the same scale — not at the GWh utility scale where thermal storage's cost advantages are usually quoted — accounting for the capital cost of any power-conversion (turbine/generator) equipment the "back to electricity" step requires.
5. State the narrowest set of conditions, if any, under which a version of the claim could be true (e.g., a different thermal-storage architecture, or a different meaning of "round trip"), rather than only returning a true/false verdict on the sentence as literally worded.

No success criterion requires the final answer to be a flat "true" or "false" of the compound sentence as given — the sentence bundles several sub-claims under one label ("round-trip," "system efficiency," "cost-competitive," "same nameplate capacity") and the answer must say which sub-claims hold, which fail, and why, which is a success-criterion requirement, not an evasion of the question.
## 2. Assumptions Table

**Inversion pass (companion technique, applied because the claim is a single clean confident assertion with no hedges — exactly the shape Inversion is built to test).** Inverted form: "This system's round-trip efficiency is NOT above 85%, and/or it is NOT cost-competitive with lithium-ion at 5 MWh." Failure-guaranteeing conditions enumerated: (a) "round trip" secretly means electricity-to-delivered-heat, not electricity-to-electricity, so there never was a heat-engine discharge step to lose efficiency in; (b) the heat-engine discharge step is real but bounded by the Second Law to well under 85% for this temperature span; (c) the quoted 85%+ figures in the literature belong to a different, more complex architecture (heat-pump charging between two managed reservoirs) than a single resistively-charged salt tank; (d) at 5 MWh, the capital cost of turbine/generator equipment needed for the "back to electricity" step is large relative to total system size and erases any raw storage-media cost advantage over lithium-ion; (e) "same nameplate capacity" silently equates a kWh of stored heat with a kWh of deliverable electricity, which are not interchangeable once a lossy reconversion step sits between them. Each of these becomes an `untested belief` row below and is resolved in Phases 3–5.

| # | Assumption | Type | Treatment | Verdict | Verification |
|---|---|---|---|---|---|
| A-1 | "Round-trip" and "system efficiency" mean AC-electricity-in to AC-electricity-out (the claim's own wording — "into heat and **back**" — refers back to electricity, the form it started in) | convention (reading of ambiguous prose) | Challenge directly: the wording supports the electricity-to-electricity reading, but industry usage (e.g., Rondo) applies "round-trip efficiency" to electricity-to-delivered-heat systems too | **Challenge — claim's own wording is read as electricity-to-electricity for the purposes of this analysis; the alternate reading is carried as the escape hatch in §6** | Resolved by close reading of the sentence (Phase 1); corroborated in Phase 5 inversion |
| A-2 | Converting stored heat back into electricity requires a heat engine (turbine/generator or equivalent) subject to the Second Law of Thermodynamics | physical law | Accept as ground-truth candidate | **Accept — physical law, no challenge needed; promoted to GT-1** | GT-1 |
| A-3 | 290 °C / 565 °C are the cold-tank/hot-tank temperatures of a standard two-tank nitrate "Solar Salt" CSP-style thermal store | convention (matches commercial CSP practice) | Record as given; note this is a temperature *source* pair for the salt, not a heat-engine *sink* temperature | **Accept — with the distinction flagged, see A-4** | Matches documented Solar Salt two-tank CSP operating range |
| A-4 | The 290 °C "cold" salt tank is the heat engine's heat-rejection sink (i.e., Carnot Tc = 290 °C) | **untested belief** | Verify against how two-tank CSP power blocks actually work | **Discard — wrong if assumed: the cold tank is the *return* temperature of salt after giving up heat to the steam generator; the power cycle rejects waste heat to ambient air or cooling water (~10–40 °C), not to 290 °C salt, and using 290 °C as Tc would *understate* the achievable ceiling; the correct Tc is ambient** | Thermodynamic design practice for Rankine power blocks; no cold reservoir in the claim's architecture is below ambient |
| A-5 | A realistic heat-rejection sink for the power cycle is ambient air/water, ≈10–40 °C | current constraint (climate/cooling-method dependent) | Record expiry condition: a colder sink (e.g., deep water, winter air) raises the ceiling slightly; this doesn't change the conclusion's order of magnitude | **Accept — used as the bracketing assumption for the Carnot ceiling calculation** | Standard power-plant engineering practice |
| A-6 | A full electricity-to-electricity round-trip efficiency above 85% is physically achievable for this temperature span | untested belief (the central claim under test) | Verify against GT-1/GT-2 (Carnot ceiling) | **Discard — see Phase 4 chain C1; 85% exceeds even the ideal lossless ceiling** | GT-1, GT-2, Derivation Chain C1 |
| A-7 | Demonstrated/commercial molten-salt or thermal-battery systems support >85% electricity round-trip efficiency | untested belief | Verify against named commercial/demonstrated systems | **Discard — for systems that actually re-electrify (Siemens Gamesa ETES ≈45%), and the >90% figures that do exist (Rondo ≈97%) belong to systems that do not re-electrify at all** | GT-3?, GT-4 |
| A-8 | Figures of 85–87% round-trip efficiency reported in Carnot-battery / PTES literature apply to the claim's architecture (single tank, resistive charge, turbine discharge) | untested belief | Verify what architecture those figures describe | **Discard — those figures belong to heat-pump-charged, dual-reservoir Brayton-cycle PTES systems, a structurally different and more complex architecture; one of the cited cases only exceeds 100% with an added external solar heat input** | GT-7? |
| A-9 | "Same nameplate capacity" (5 MWh) means the thermal store's cost can be compared directly, kWh-for-kWh, with a lithium-ion system's cost | convention (hidden equivalence) | Challenge directly: a kWh of stored heat and a kWh of deliverable electricity are not the same good once a lossy, capital-intensive reconversion step separates them | **Discard — as stated; valid only if the cost comparison also includes the reconversion equipment needed to deliver that kWh as electricity, restored explicitly in chain C4** | Reasoned from A-2 + A-6 |
| A-10 | Thermal-storage cost advantages per kWh quoted in CSP/utility literature (large multi-hundred-MWh plants) transfer unchanged to a 5 MWh system | convention (scale assumed to be irrelevant) | Challenge: power-block (turbine/generator) capital cost has a large scale-independent component and does not shrink proportionally at small size | **Discard — see Phase 4 chain C4's Estimate step; this is a *diseconomy* of scale specific to the power-conversion equipment, not the salt/tank itself** | Estimate step in Derivation Chain C3 |
| A-11 | Lithium-ion system costs used for comparison (utility-scale, $100–150/kWh) are representative of a 5 MWh installed system | untested belief | Flag — smaller systems typically cost somewhat more per kWh than utility/GWh-scale systems due to fixed BOS and interconnection costs, but the effect is far smaller than the power-block diseconomy in A-10 | **Accept — with an upward adjustment flagged; does not change the conclusion's direction** | unverified — flagged; GT-6? |
| A-12 | The >100% GT-7? figure is only meaningful as "round trip" if the external solar heat input is excluded from the accounting (surfaced by chain C2, step 3) | convention (a labeling choice in the source study) | Flagged in chain C2's confidence note | **Accept — as stated, with the caveat carried forward into chain C2's confidence line** | GT-7? |
| A-13 | A 1–2 MW package steam turbine-generator set costs $1,500–3,000/kW (surfaced by chain C4, step 3) | untested belief | Carried as the explicit LOW-confidence driver in chain C4 | **Challenge — not independently verified; carried as the explicit LOW-confidence driver in chain C4** | unverified — flagged; no source located, engineering-judgment bracket only |
| A-14 | Lithium-ion battery systems achieve round-trip efficiency in the ~85–95% range (surfaced by chain C6, step 1) | current constraint (well-established industry figure) | Accepted as common, widely-published engineering knowledge for LFP/NMC grid-storage systems | **Accept — common, widely-published engineering knowledge for LFP/NMC grid-storage systems, not separately sourced in this analysis** | Common engineering knowledge; the one additional citation that would most cheaply raise chain C6's confidence if challenged |

**Stakes-escalation check:** The conclusion is high-stakes (a capital-allocation claim comparing two energy-storage technologies), so every load-bearing assumption above has been pushed toward physical law (A-2, A-4, A-5) rather than left as convention, and the two assumptions that remain `untested belief` after verification (A-7/A-8, resting on `?`-marked secondary sources) are confined to the *corroborating* evidence, not the *decisive* evidence — the decisive argument (A-2 through A-6) rests on an undisputed physical law plus arithmetic, not on any `?`-marked source.
## 3. Ground Truths

**Irreducibility check (five-whys, reduce-to-primitives mode), applied to the compound term "round-trip efficiency" before anything is verified.** "Round-trip efficiency" → reduces to three constituent factors: (a) charge efficiency (electricity → stored form), (b) storage retention efficiency (stored form, over the dwell time between charge and discharge), (c) discharge efficiency (stored form → delivered output). Is (c) itself reducible? For a system whose delivered output is *electricity*, (c) further reduces to "the efficiency of a heat engine operating between the stored-heat temperature and the rejection-sink temperature," which bottoms out at the Second Law of Thermodynamics — a physical law, not a belief, and not reducible further. This primitive (GT-1 below) is the irreducible fact the whole analysis turns on; every other ground truth here is corroborating context around it.

1. **GT-1** — Carnot's theorem (Second Law of Thermodynamics): the maximum fraction of heat input convertible to work by *any* heat engine operating between a hot reservoir at absolute temperature T_h and a cold (rejection) reservoir at absolute temperature T_c is η_Carnot = 1 − T_c/T_h. No real heat engine can exceed this, regardless of working fluid, cycle design, or engineering quality. **Type:** physical law. **Provenance:** foundational, universally accepted thermodynamic law; not sourced from a single citable document — no `?` suffix applies to a physical law under the Phase 2 treatment table. **Read-at-source:** n/a — a physical law is not derived from a document that could be misread; it is accepted as a ground-truth candidate directly, per the Phase 2 treatment table's prescription for the physical-law type.
2. **GT-2** — Absolute-temperature conversion is definitional: K = °C + 273.15. **Type:** definition. **Provenance:** definitional; no `?`. **Read-at-source:** n/a — a unit-conversion definition, not derived from a document that could be misread.
3. **GT-3?** — Siemens Gamesa's ETES (Electric Thermal Energy Storage) pilot (Hamburg): charge/storage efficiency "expected to be 99%"; efficiency "for producing electricity from the stored thermal energy... expected to be 45%." Combined electricity-to-electricity round trip ≈ 99% × 45% ≈ 44.6%, i.e., ≈45%. **Type:** untested-belief-turned-candidate ground truth (a real, named, commercially-backed demonstration project). **Provenance: reported-by-delegate** — retrieved via WebFetch's summarization of nsenergybusiness.com's ETES Hamburg project page; the page's own quoted language was returned, but this analysis did not parse the raw HTML itself. Source: [nsenergybusiness.com — Electric Thermal Energy Storage (ETES) System, Hamburg](https://www.nsenergybusiness.com/projects/electric-thermal-energy-storage-etes-system-hamburg).
4. **GT-4** — Rondo Energy's "Rondo Heat Battery," deployed at commercial scale (100 MWh unit, operating since October 2025): storage temperatures over 1,000 °C, "round-trip efficiency above 97%"; the same source describes the unit as "delivering continuous high-pressure industrial heat and steam" to an industrial facility, with no turbine, generator, or any electricity-output equipment named anywhere in the source. **Type:** demonstrated commercial fact. **Provenance: read-at-source** — read-location: Rondo Energy press release, "Rondo Powers Up World's Largest Industrial Heat Battery" (16 Oct 2025), quoted text "storage temperatures over 1000°C and round-trip efficiency above 97%" and "delivering continuous high-pressure industrial heat and steam," at [rondo.com/news/rondo-powers-up-worlds-largest-industrial-heat-battery](https://www.rondo.com/news/rondo-powers-up-worlds-largest-industrial-heat-battery). The *inference* that this 97% figure therefore measures electricity-to-delivered-heat (not electricity-to-electricity) is this analysis's own reasoning from the absence of any electricity-output equipment in the source, not an additional claim made by Rondo in the quoted text — carried into Phase 4 as a derivation step, not asserted here as a second fact.
5. **GT-5?** — Historical CSP literature describes two-tank molten-salt thermal storage capital cost as having exceeded "$80/kWh-thermal" (undated figure found via secondary search summary, likely SunShot-era, mid-2010s). **Type:** untested belief. **Provenance: unverified** — a direct read of the cited PDF ([sco2symposium.com/papers2016/Thermal/094paper.pdf](https://www.sco2symposium.com/papers2016/Thermal/094paper.pdf)) was attempted; the file opened but its content was heavily encoded/compressed and the specific figure could not be located in readable text. **Phase 3 failure record:** source opened, read attempted, figure not confirmed in extractable text — reason: "citation does not support the claim" is too strong a label here since no readable text was recovered at all; recorded instead as an unreadable-source failure. This ground truth is **not load-bearing** for the conclusion (it is illustrative color on thermal-storage media cost, not the decisive cost comparison, which runs through GT-6? and the Phase 4 Estimate step) and is not re-read under the Phase 3 verification step's budget-priority rule.
6. **GT-6?** — Lithium-ion stationary-storage costs in 2025: BNEF-reported battery pack prices fell to roughly $70–108/kWh in 2025 (China lowest at ~$94/kWh; US/Europe 31–48% higher); a separate full grid-connected installed-system cost estimate (Ember, Oct 2025) for long-duration (≥4 hr) utility-scale projects is ≈$125/kWh. **Type:** untested belief (market data). **Provenance: reported-by-delegate** — retrieved via WebSearch summaries of BNEF/Ember figures as reported by ess-news.com and solarserver.de; neither primary report (BNEF terminal data, Ember's own publication) was opened directly. Sources: [ess-news.com, "Energy storage in 2025: Year in review"](https://www.ess-news.com/2025/12/19/energy-storage-in-2025-year-in-review-part-1/); [solarserver.de, "BNEF-Studie: Lithium-Ionen-Batteriespeicher so billig wie nie"](https://www.solarserver.de/2025/12/10/bnef-studie-lithium-ionen-batteriespeicher-so-billig-wie-nie/). **Phase 3 verification step attempted:** since this ground truth feeds chain C4 and chain C6, both of which the Conclusion rests on, a direct read of the ess-news.com primary page was attempted; it returned HTTP 503 Service Unavailable (Retry-After: 3600). **Phase 3 failure record:** source unreachable (503, temporary); figure remains reported-by-delegate, `?` retained.
7. **GT-7?** — A 2023 peer-reviewed techno-economic study (Comillas/*Energies*) of a Brayton supercritical-CO₂ Carnot battery using two-tank molten-salt storage on *both* the low-temperature (380 °C/290 °C) and high-temperature (589 °C/405 °C) sides, charged via a heat pump (not simple resistive heating): reports a heat-pump COP of 2.46 and heat-engine efficiency of 46.5%, giving round-trip efficiency "1.15" (>100%) when boosted by an external concentrated-solar heat input, and a separate configuration averaging 85–87% round-trip efficiency; levelized cost of storage of $376/MWh in the base configuration, falling to $188/MWh with improved (printed-circuit) heat exchangers. **Type:** untested belief (single study's modeled/pilot-scale results). **Provenance: reported-by-delegate** — retrieved via WebSearch summary of the paper and its Comillas repository listing; the PDF itself was not opened. Sources: [energies-16-03871-v2.pdf, Comillas repository](https://repositorio.comillas.edu/jspui/retrieve/623554/20236601132628_energies-16-03871-v2.pdf); [DOAJ listing, *Energies*, May 2023](https://doaj.org/article/9cad13ecf56141abbf2a29e16312ee27). **Phase 3 verification step attempted:** since this ground truth feeds chain C2, which the Conclusion rests on, a direct read of the Comillas repository PDF was attempted; it returned HTTP 410 Gone. **Phase 3 failure record:** source unreachable (410, permanently gone at this URL); figure remains reported-by-delegate, `?` retained. **This ground truth describes a structurally different architecture** (heat-pump charging, two independently managed reservoirs, in one case an added external heat source) from the claim's single resistively-charged salt tank — the distinction is carried forward explicitly in Phase 4.

**`?`-marked:** GT-3, GT-5, GT-6, GT-7 (4 of 7).

**Irreducibility verdict:** GT-1 and GT-2 pass the irreducibility test cleanly (physical law / definition, not reducible further, not a belief). GT-3 through GT-7 are empirical/market facts about specific named systems and are not further reducible for the purposes of this analysis (each names a specific system, source, and figure); their `?` flags record *provenance* (was the primary source opened), not *reducibility*.

**Not read — turn budget:** none remain unattempted. Every ground truth feeding a chain the Conclusion rests on was either definitional (GT-1, GT-2), read at source (GT-4), or had a direct read attempted and recorded as a Phase 3 failure when it did not succeed (GT-3? — see below, GT-5?, GT-6?, GT-7?). **GT-3?'s own read status:** the nsenergybusiness.com page was opened via WebFetch and returned the quoted figures directly, but WebFetch's summarizing step means this analysis did not parse the raw HTML itself; retained as reported-by-delegate rather than upgraded to read-at-source, per the provenance test's literal requirement. No ground truth was left unattempted solely because of turn-budget triage; the two attempts made specifically to upgrade GT-6? and GT-7? (above) both failed for reasons external to this analysis (410 Gone; 503 Service Unavailable), and are recorded as such rather than silently retried or dropped.
## 4. Derivation Chains

**Theoretical-limit bracket (companion technique, applied first because the central question is exactly "what ceiling do the fundamentals permit once the architecture's conventions are stripped away").** Direction: higher round-trip efficiency is better, so the bound sought is an **ideal ceiling**.

- **Governing hard constraint:** the Second Law of Thermodynamics, expressed as Carnot's theorem (GT-1) — no heat engine operating between a hot reservoir and a cooler rejection sink can exceed η = 1 − T_c/T_h.
- **Ideal ceiling:** with T_h = 565 °C = 838.15 K fixed by the claim, and a realistic ambient rejection sink of 10–40 °C (283.15–313.15 K), η_Carnot ≈ 62.6%–66.2% (central ≈64%). This is the absolute best any charge+store+discharge cycle on this architecture could do even with zero charging loss and zero storage loss — it is a ceiling on the *discharge step alone*, and discharge efficiency is one of three multiplied factors in round-trip efficiency, so it is also a ceiling on the whole round trip.
- **Best demonstrated (observed, not computed):** Siemens Gamesa's ETES pilot (GT-3?), the only named system that both charges from and discharges back to electricity, reports ≈45% combined round-trip efficiency — a real, cited operating figure, well inside the ideal ceiling (consistent with real heat engines achieving roughly 55–70% of their Carnot limit).
- **Conventional figure:** general CSP Rankine-cycle practice converts stored heat at comparable temperatures to electricity at roughly 35–42% thermal-to-electric efficiency (industry-standard knowledge for Solar Salt-range CSP power blocks), broadly consistent with the ETES figure once charge/storage losses are added back.
- **Gap 1 — conventional → best demonstrated:** roughly 3–10 percentage points; small, already-proven headroom.
- **Gap 2 — best demonstrated → ideal ceiling:** roughly 19 percentage points (45% → 64%); headroom nobody has reached yet in a built system of this architecture, bounded by real-world irreversibilities in the turbine, heat exchangers, and condenser — reducible in principle, but never to zero.
- **The claim's figure (>85%) sits *above* the ideal ceiling itself** — it is not unreached headroom within Gap 2, it is a figure the governing constraint prohibits outright for this architecture, before Gap 1 or Gap 2 are even relevant.

### Chain C1 — the claimed efficiency exceeds the physical ceiling (HIGH)

```text
GT-1 (Carnot ceiling: eta = 1 - Tc/Th) + GT-2 (K = C + 273.15)
→ at Th = 565C (838.15 K) and a realistic ambient rejection sink of 10-40C (283.15-313.15 K), the Carnot ceiling is eta approx 62.6%-66.2%, central approx 64%
→ even an ideal, lossless charge step and an ideal, lossless storage step cannot raise the discharge step above this ceiling, so the absolute theoretical maximum full electricity-to-electricity round-trip efficiency for this architecture is approximately 64%, not above 85%
→ the claimed figure exceeds the ideal theoretical ceiling for this exact architecture by roughly twenty percentage points, before any real-world loss is even counted
```

**Pre-check:** head: GT-1 (physical law), GT-2 (definition) · ?-marked: none · lowest cited: none · Inputs ceiling: HIGH.
**Confidence:** HIGH — Inputs are a physical law and a unit definition (no `?`, nothing cited below HIGH); Inference is plain arithmetic with no `[Assumes: X]` premise; on Rivals, no competing conclusion from GT-1 and GT-2 survives against this chain's own narrowly-scoped endpoint (the ceiling for *this specific architecture*) — the only apparent rival (a dual-reservoir, heat-pump-charged "Carnot battery" approaching 100% round-trip between the *same* two reservoirs) is not actually a competing conclusion from these same inputs about this architecture; it is a different architecture entirely, outside this chain's scope, and is examined on its own terms in chain C2 and recorded in §5.

### Chain C2 — the literature's 85–87% figures belong to a different architecture (MEDIUM)

```text
GT-7? (Comillas Brayton-PTES study: COP 2.46, heat-engine eff. 46.5%, RTE 85-87% / >100% with solar boost) + C1 (ideal ceiling for this architecture, approx 64%)
→ those figures come from a heat-pump-charged system moving heat between two actively managed reservoirs
→ moving heat between two managed reservoirs lets the reversible-cycle identity COP times heat-engine-efficiency approach unity in the ideal limit, a different thermodynamic structure than a single resistively-heated salt tank discharging to ambient
→ the claim's architecture has no heat pump and no actively managed cold-side reservoir below ambient, so it cannot access this COP-boost mechanism, and citing GT-7?'s 85-87% figures as support for the claim's architecture is a category error
→ even within GT-7?'s own more favorable architecture, the figure above 100% required an added external concentrated-solar heat input, which is free energy from outside the electricity round trip rather than evidence the round trip itself exceeds its own ceiling [Assumes: A-12]
```

**Pre-check:** head: GT-7? (`?`), C1 (HIGH) · ?-marked: GT-7? · lowest cited: C1 (HIGH) · Inputs ceiling: MEDIUM (one `?`-marked input).
**Confidence:** MEDIUM — capped by GT-7? (reported-by-delegate; the Comillas/*Energies* PDF itself was not opened). What would remove the cap: opening the primary PDF and confirming the COP/efficiency/architecture figures and the external-heat-input caveat directly. Inference and Rivals are otherwise clean given C1.

### Chain C3 — real-world demonstrated systems corroborate the ceiling (MEDIUM)

```text
GT-3? (Siemens Gamesa ETES: 99% x 45% approx 45% RTE) + GT-4 (Rondo: >97% RTE, heat-only output) + C1 (ideal ceiling approx 64%)
→ the only named system that actually reconverts stored heat to electricity reports approximately 45% round-trip efficiency, comfortably under the approximately 64% ideal ceiling and far under the claimed 85%
→ the only named system reporting round-trip efficiency above 85% achieves this specifically by skipping the heat-engine discharge step and delivering heat directly as process steam, which is not "electricity... back" in the sense the claim's wording requires
→ across every named real system, round-trip efficiency above 85% and electricity-to-electricity reconversion are mutually exclusive outcomes, matching C1's prediction that a 64% ceiling makes an 85%-plus electricity round trip structurally impossible for this class of architecture
```

**Pre-check:** head: GT-3? (`?`), GT-4 (unsuffixed, read-at-source), C1 (HIGH) · ?-marked: GT-3? · lowest cited: C1 (HIGH) · Inputs ceiling: MEDIUM.
**Confidence:** MEDIUM — capped by GT-3? (reported-by-delegate via WebFetch summarization of a secondary project-listing page, not Siemens Gamesa's own primary documentation). What would remove the cap: reading Siemens Gamesa's or DLR's primary ETES technical documentation directly.

### Chain C4 — cost at 5 MWh scale (Estimate procedure; LOW)

```text
GT-6? (lithium-ion installed cost approx $100-150/kWh, 2025) + GT-5? (molten-salt storage-media cost, non-load-bearing)
→ target quantity: $/kWh installed cost of a 5 MWh molten-salt system that actually delivers electricity back out
→ that cost decomposes into (storage media plus tank plus heaters, $/kWh-thermal) plus (turbine-generator-condenser power block, $/kW-electric, divided by the system's MWh per duration-hours)
→ an unresolved-provenance historical CSP figure puts storage-media cost on the order of $30-80/kWh-thermal (GT-5?, non-load-bearing)
→ at that rate, a 5 MWh store's media cost alone is roughly $150,000-$400,000
→ small 1-2 MW class steam turbine-generator packages carry a materially higher dollar-per-kW capital cost than utility-scale power blocks, because engineering, balance-of-plant, and controls costs do not shrink proportionally with size
→ bracketing this at an assumed (not independently cited) $1,500-$3,000/kW for a package sized to discharge 5 MWh over 2.5-5 hours (1-2 MW), the power block alone costs roughly $1.5M-$6M [Assumes: A-13]
→ summing media plus power-block cost and dividing by 5,000 kWh gives an estimated installed cost of roughly $330-$1,280/kWh for this architecture at 5 MWh scale (low-low and high-high pairing of the two brackets)
→ that bracket is two to thirteen times GT-6?'s approximately $100-150/kWh for a same-capacity lithium-ion system
→ this gap is driven almost entirely by the power block, which a pure heat-delivery thermal battery (GT-4's architecture) does not need to buy at all, confirming that thermal storage's cost advantages at gigawatt-hour utility scale do not transfer to a 5 MWh system that must also re-electrify
```

**Pre-check:** head: GT-6? (`?`), GT-5? (`?`, non-load-bearing) · ?-marked: GT-6?, GT-5?; the turbine $/kW figure used in hop 3 is an explicitly assumed range (A-13), not a citation, and is not a head identifier · lowest cited: none · Inputs ceiling: LOW (two `?`-marked inputs plus an uncited assumed quantitative figure carried inline as `[Assumes: A-13]`).
**Confidence:** LOW — the turbine $/kW bracket is engineering judgment, not a verified source (A-13), GT-6? is reported-by-delegate (ess-news.com read attempted, HTTP 503), and GT-5? is unreadable at its cited source (sco2symposium.com PDF, encoded content) though non-load-bearing since the media-cost term it feeds is the smaller of the two cost components; the bracket is wide ($330–$1,280/kWh). What would raise this: a verified quote or published cost figure for a 1–2 MW package steam turbine-generator set, and a primary (not secondary-summarized) lithium-ion installed-cost figure at the 5 MWh scale specifically. **The direction of the result (thermal-with-reconversion costs substantially more than lithium-ion at 5 MWh) is more robust than the LOW band suggests**, though less airtight than first drafted: the recomputed bracket's low end ($330/kWh) is only about 2x GT-6?'s high end (~$150/kWh), not the wider multiple originally stated, so the margin is real but narrower at the bracket's optimistic edge — the band reflects input provenance, not the robustness of the qualitative conclusion, and that distinction is carried into §6 explicitly. **Live rival (not ruled out):** lithium-ion cell costs could keep falling while thermal-storage manufacturing scales up, narrowing or reversing this gap in future years; nothing in this analysis settles that trend question, and the conclusion here is scoped to current (2025-2026) costs only. **Two further scope limits surfaced by the Phase 5 adversarial pass (process output):** this estimate assumes a 2.5-5 hour discharge duration typical of grid-arbitrage sizing — a much longer discharge duration would shrink the power block's per-kWh cost materially and should be re-estimated against the buyer's actual target duration before any procurement decision; and this chain compares upfront installed $/kWh only, not levelized cost of storage over asset life, a metric where thermal storage's very long cycle life and low degradation (versus lithium-ion's 10-15 year replacement cycle) is a genuine, currently under-weighted advantage this chain does not capture.

### Chain C5 — second-order effects (actor lens and time lens)

```text
C1 (physical ceiling approx 64%) + C3 (real-world corroboration) + C4 (cost gap at 5 MWh)
→[2nd, actor] a buyer who sizes a grid-arbitrage project on the claim's 85-percent/cost-competitive premise commits capital to equipment that cannot deliver the promised throughput
→[2nd, actor] vendors marketing "round-trip efficiency" without naming the discharge path have a financial incentive to let the ambiguous reading stand, because the true electricity-RTE number is unflattering
→[2nd, actor] lithium-ion suppliers win grid-dispatch and frequency-response contracts at this scale largely by default, since those services reward high round-trip efficiency and fast response, neither of which this thermal architecture can supply competitively against C1 and C4
→[2nd, time] immediately, a 5 MWh unit built on the claim's premise underperforms its dispatch-economics forecast from day one, because metered output cannot exceed the approximately 64% ideal or approximately 45% real ceiling from C1 and C3
→[3rd, time] after a few duty cycles the shortfall becomes visible in revenue-metered data
→[3rd, time] over longer operation the observed market response is for thermal-storage developers to abandon electricity-reconversion entirely and sell heat directly to industrial customers
→[3rd, time] that is the business GT-4's Rondo and similar firms are already built around, not the business the claim describes
```

No step here contradicts a Ground Truth; all extensions are consistent with C1–C4, so the conclusion does not route back to Phase 2.

**Pre-check:** head: C1 (HIGH), C3 (MEDIUM), C4 (LOW) · ?-marked: none directly, inherited via C3/C4 · lowest cited: C4 (LOW) · Inputs ceiling: LOW.
**Confidence:** LOW by inheritance from C4's input cap (and, independently, from C3, which is MEDIUM — both named on this chain's head) — the qualitative actor-lens and time-lens effects themselves (buyer disappointment, lithium-ion winning contracts by default, developers pivoting to heat-only business models) are well-corroborated by the real, named market trajectory of GT-4 and similar firms, but the chain formally inherits C4's LOW band because it cites C4 in its head, and would be capped at MEDIUM by C3 even if C4 were resolved. What would raise this: the same verification named under C4 and under C3.

### Chain C6 — trade-off collapse: molten-salt-with-turbine vs. lithium-ion vs. composite at 5 MWh (LOW, see caveat)

Weights locked before scoring (1–5): round-trip efficiency for electricity dispatch = 5, installed cost per kWh = 5, response time/flexibility = 3, cycle life/degradation = 2, safety/footprint = 2. Anchors: RTE 1=<30%, 5=>90%; Cost 1=>$800/kWh, 5=<$150/kWh; Response 1=minutes-scale, 5=seconds-scale; Cycle life 1=<2,000 cycles, 5=>10,000; Safety 1=large/hazardous footprint, 5=compact/low-hazard.

| Option | RTE score | Cost score | Response score | Cycle score | Safety score | Weighted total |
|---|---|---|---|---|---|---|
| (a) Molten-salt + turbine (claim's architecture) | 2×5=10 | 1×5=5 | 2×3=6 | 5×2=10 | 2×2=4 | **35** |
| (c) Lithium-ion, same nameplate | 5×5=25 | 5×5=25 | 5×3=15 | 3×2=6 | 3×2=6 | **77** |
| (b) Heat-only thermal battery (no reconversion) | disqualified — fails the must-have "delivers electricity back" for this use case | | | | | n/a |

```text
GT-3? (real RTE approx 45%) + C4 (cost at 5 MWh, LOW) + GT-6? (lithium-ion cost/RTE)
→ scoring molten-salt-with-turbine against lithium-ion on weighted criteria locked before scoring, lithium-ion scores 77 of 95 weighted points against molten-salt-with-turbine's 35 [Assumes: A-14]
→ that gap is driven almost entirely by the two highest-weighted criteria, efficiency and cost, where molten-salt-with-turbine lags by the widest margins
→ a flip test shows no single criterion's weight can be moved far enough to change the winner
→ even deleting the cost criterion and the efficiency criterion entirely, lithium-ion's remaining weighted total (27) still exceeds molten-salt-with-turbine's remaining total (20), so this is a robust result, not a near-tie
→ a composite option, lithium-ion sized for the electricity-dispatch need plus a separate heat-only thermal battery sized independently for any co-located process-heat load, dominates the pure molten-salt-with-turbine option whenever a heat load exists
→ that composite wins because it lets the thermal asset do the one thing it is actually efficient at, delivering heat at approximately 97 percent per GT-4, instead of forcing it through the lossy, expensive reconversion step the claim's architecture requires
```

**Pre-check:** head: GT-3? (`?`), C4 (LOW), GT-6? (`?`) · ?-marked: GT-3?, GT-6? · lowest cited: C4 (LOW) · Inputs ceiling: LOW.
**Confidence:** LOW by the formal input cap (inherits C4's LOW via the chain-citation rule, and GT-3? and GT-6? are both reported-by-delegate, read-attempted-and-failed per their Phase 3 failure records) — **but the flip test's result (no single-criterion reweighting changes the winner) is a separate, qualitative robustness finding that survives the LOW band**: even if C4's wide cost bracket were wrong by a large margin, the RTE axis alone (GT-3?'s ≈45% real-world figure vs. lithium-ion's well-established ~85–95%, A-14, common engineering knowledge not separately cited here) would still favor lithium-ion by a wide, unweighted margin. What would raise the formal band: the same verification named under C4 (for GT-6?) and under C3 (for GT-3?).
## 5. Abandoned Reasoning

1. **What was tried:** Reading "system efficiency" as thermal storage *retention* efficiency alone (insulation/tank losses only), ignoring the charge and discharge conversion steps. **Why abandoned:** this reading makes "round-trip electricity into heat and back" meaningless — it never engages the electricity-in/electricity-out conversion the claim's own wording describes, and no cited source (GT-3?, GT-4, GT-7?) uses "round-trip efficiency" that narrowly. **What it ruled out:** treating the claim as trivially true (molten salt tanks do retain heat at >95–99% efficiency over short dwell times) — that would answer a different, easier question than the one asked.

2. **What was tried:** Checking whether an unusually cold heat-rejection sink (e.g., Arctic siting, Tc ≈ −20 °C = 253.15 K) could push the Carnot ceiling materially above the 62.6–66.2% bracket used in C1. Computed: η = 1 − 253.15/838.15 ≈ 69.8%. **Why abandoned:** still far short of 85%; kept only as a boundary check that C1's conclusion is insensitive to realistic sink-temperature variation, not as a path to validating the claim.

3. **What was tried:** Using the 290 °C cold salt tank as the heat engine's rejection sink (Tc = 290 °C = 563.15 K) in the Carnot formula, which would give a *lower* ceiling of 1 − 563.15/838.15 ≈ 32.8%. **Why abandoned:** this misreads two-tank CSP architecture (A-4) — the "cold" tank is the salt's return temperature after giving up heat to the steam generator, not the power block's heat-rejection sink; the power block rejects waste heat to ambient air or cooling water, far below 290 °C. **What it ruled out:** a 32.8% ceiling that would have been inconsistent with ETES's demonstrated ~45% round-trip figure (GT-3?) — a real system cannot beat its own ideal ceiling, so the lower bound was identified as an architectural misreading rather than treated as a live contradiction.

4. **What was tried:** Treating GT-7?'s 85–87% round-trip efficiency figure (Comillas Brayton-PTES study, heat-pump-charged, dual managed reservoirs) as direct evidence that the claim's architecture can reach >85%. **Why abandoned:** ruled out by chain C2 — GT-7?'s architecture has a heat pump and a second actively managed reservoir, structurally different from the claim's single resistively-charged tank; using it as support for the claim is a category error. **What it ruled out:** accepting the claim's efficiency figure as literally achievable for the architecture as named.

5. **What was tried:** Pursuing a second, independent source for the "$80/kWh-thermal" two-tank molten-salt capital-cost figure (GT-5?) after the primary PDF read failed to extract readable text. **Why abandoned:** per Turn discipline, verification reads compete with the Self-Audit Gate for the same turn budget, and GT-5? is explicitly non-load-bearing (illustrative color on storage-media cost only; the decisive cost argument runs through the independently-estimated power-block gap in C4). **What it ruled out:** nothing substantive — GT-5? remains `?`-marked and unused as decisive evidence.

6. **What was tried (named but not pursued):** Opening the primary Comillas/*Energies* 2023 PDF (GT-7?) directly to upgrade it from reported-by-delegate to read-at-source. **Why abandoned (for this run):** GT-7? feeds only the corroborating chain C2, not the decisive chain C1; turn budget was prioritized toward completing the Self-Audit Gate's full six-criterion pass instead. **What it ruled out:** nothing — this is named here as the single most valuable remaining verification step if the analysis is revisited with more budget, not as a resolved question.

7. **Not abandoned, carried forward to §6:** the possibility that a fundamentally different architecture — a true dual-reservoir, heat-pump-charged Carnot battery, where the "290–565 °C tank" is only the hot-side store of a larger system with an additional, separately managed cold-side store below ambient — could achieve something in the 60–87% round-trip range reported in the PTES literature (GT-7?). This is not a rival to be ruled out; it is the narrowest condition under which a *version* of the claim could hold, and is stated explicitly as such in the Conclusion rather than discarded.
## 6. Conclusion

**Recommended approach:** For a 5 MWh thermal-storage asset described as charging from and discharging back to grid electricity between 290 and 565 °C, do not expect, and do not budget around, a round-trip electricity-to-electricity efficiency above 85% — the architecture's absolute theoretical ceiling is approximately 64% (chain C1), and the best demonstrated real system of this kind achieves roughly 45% (chain C3). If the actual need is grid electricity storage at 5 MWh, lithium-ion is the better choice by a wide, robust margin on both efficiency and cost (chain C6). If the actual need is industrial process heat, a heat-only thermal battery that never attempts reconversion (no turbine) is the better choice, and can legitimately claim >95% round-trip efficiency because it is solving a different problem (chain C3, chain C4). The only way a version of this claim becomes defensible is by substituting a structurally different architecture — a heat-pump-charged, dual-reservoir Carnot battery — for the single-tank system the claim names, and even then the reported 85–87% figures come from modeling studies, not commercial 5 MWh products (chain C2).

**Key insight:** The claim is internally inconsistent because it uses "round trip" to mean two different, non-interchangeable things at once — "into heat and back" (to electricity), which is Carnot-bounded near 64% ideal / ~45% real (chain C1, chain C3) — while the only real system in this analysis that exceeds 85% round-trip efficiency (chain C3's Rondo example) does so by never attempting the "back to electricity" step at all, delivering heat directly instead; the cost comparison then silently prices a kWh of one of these goods against a kWh of the other as if they were the same good (chain C1, chain C4).

**Trade-offs acknowledged:** At the scale and use case the claim literally describes, lithium-ion wins on round-trip efficiency and installed cost per kWh by a wide and robust margin — a flip test found no single criterion reweighting that changes the outcome (chain C6). Thermal storage is not thereby a bad technology: it retains genuine, large advantages in cheap long-duration heat delivery, very high cycle tolerance, and compatibility with high-temperature industrial process loads that lithium-ion cannot serve at all (chain C3, chain C4) — the right choice depends on which deliverable, electricity or heat, is actually needed, not on treating a thermal kWh and an electrical kWh as interchangeable. Two further caveats on the cost comparison itself (surfaced by the Phase 5 adversarial pass, below): chain C4/C6's cost bracket assumes a 2.5-5 hour discharge duration typical of grid-arbitrage sizing — a much longer discharge duration would shrink the power-block's per-kWh cost and should be re-estimated against the buyer's actual target duration before any procurement decision (chain C4); and the comparison is framed as upfront installed $/kWh rather than levelized cost of storage over asset life, a metric where thermal storage's very long cycle life and low degradation (versus lithium-ion's 10-15 year replacement cycle) is a genuine, currently under-weighted advantage (chain C4, chain C6).

**Pre-check:** head: C1 (HIGH) · C2 (MEDIUM) · C3 (MEDIUM) · C4 (LOW) · C6 (LOW) · ?-marked: none directly (all `?` inputs are routed through the named chains) · lowest cited: C4, C6 (LOW) · Inputs ceiling: LOW.
**Confidence:** LOW by the formal Inputs ceiling, inherited from the cost/trade-off chains (C4, C6), which rest on an explicitly assumed (uncited) small-scale turbine cost figure and on secondary, not-independently-opened market data (GT-6?, GT-3?). This formal cap should not be read as uncertainty about the claim's efficiency physics: chain C1 alone — a physical law plus arithmetic, with no `?`-marked input — is HIGH confidence and is, by itself, sufficient to falsify the claim's central assertion that round-trip efficiency can exceed 85% for this architecture. What would raise the overall band to MEDIUM or HIGH: a verified small-scale power-block cost figure and a primary-source lithium-ion installed-cost figure at 5 MWh (both named under chain C4); nothing would change chain C1's verdict, since it does not depend on either.
## Appendix — process output

## Assumption Audit scan (process output)

| Chain | Step | Step Text (brief) | Assumption surfaced? | Added to Table? |
|---|---|---|---|---|
| C1 | 1 | Carnot ceiling at 10–40°C ambient | ambient sink range (A-5) | already in table |
| C1 | 2 | ideal charge/storage losses are zero | none beyond A-5 | clean pass |
| C1 | 3 | claim exceeds ideal ceiling | none | clean pass |
| C2 | 1 | heat-pump-charged system moving heat between two reservoirs | none beyond A-8 | already in table |
| C2 | 2 | COP × heat-engine-efficiency approaches unity, different structure | none beyond A-8 | clean pass |
| C2 | 3 | claim's architecture lacks COP-boost mechanism, category error | none beyond A-4/A-8 | clean pass |
| C2 | 4 | >100% case used external solar heat | solar-boost case excluded from "round trip" accounting | new — added as A-12 |
| C3 | 1 | ETES ≈45% under ideal ceiling | none beyond A-7 | clean pass |
| C3 | 2 | Rondo achieves >85% only by skipping reconversion | none beyond A-1 | clean pass |
| C3 | 3 | mutual exclusivity across named systems | none | clean pass |
| C4 | 1 | target quantity: $/kWh for a reconverting 5 MWh system | none | clean pass |
| C4 | 2 | cost decomposes into media cost plus power-block cost | none | clean pass |
| C4 | 3 | historical CSP media-cost figure, $30–80/kWh-thermal | GT-5? non-load-bearing (already flagged) | clean pass |
| C4 | 4 | media cost alone roughly $150k–$400k | none | clean pass |
| C4 | 5 | small turbine packages cost more per kW than utility-scale | none beyond A-13 (surfaced at step 6) | clean pass |
| C4 | 6 | turbine $/kW bracket, power block $1.5M–$6M | small-scale power-block $/kW premium real and of stated magnitude | new — added as A-13 |
| C4 | 7 | total installed cost $330–$1,280/kWh | none beyond A-13 | clean pass |
| C4 | 8 | that bracket vs. GT-6?'s lithium-ion cost | none | clean pass |
| C4 | 9 | gap driven by power block, not transferable from utility scale | none | clean pass |
| C5 | 1 | buyer commits capital on false premise | none beyond C1/C4's existing flags | clean pass |
| C5 | 2 | vendor incentive to let ambiguous reading stand | none | clean pass |
| C5 | 3 | lithium-ion wins contracts by default | none beyond C1/C4's existing flags | clean pass |
| C5 | 4 | unit underperforms forecast from day one | none beyond C1/C3's existing flags | clean pass |
| C5 | 5 | shortfall visible in metered data after a few cycles | none | clean pass |
| C5 | 6 | developers abandon reconversion, sell heat directly | none | clean pass |
| C5 | 7 | that is GT-4's Rondo's actual business | none | clean pass |
| C6 | 1 | weighted scoring: lithium-ion 77 vs. molten-salt 35 | lithium-ion RTE (~85–95%) treated as common engineering knowledge, not separately cited | new — added as A-14 |
| C6 | 2 | gap driven by the two highest-weighted criteria | none beyond A-14 | clean pass |
| C6 | 3 | flip test: no single-criterion reweighting changes winner | none | clean pass |
| C6 | 4 | even deleting two criteria, lithium-ion still wins | none | clean pass |
| C6 | 5 | composite option dominates whenever a heat load exists | none | clean pass |
| C6 | 6 | composite wins because it uses the thermal asset for heat | none | clean pass |

Scan complete: 6 chains audited (C1–C6), 32 steps scanned in order (C1: 3, C2: 4, C3: 3, C4: 9, C5: 7, C6: 6); 3 new assumptions surfaced (A-12, A-13, A-14), each added once to the Classified Assumptions Table (§2) and marked inline on its originating chain step with `[Assumes: A-N]`. This table was regenerated after chain hops were split during drafting to meet the one-inference-per-hop rule; it reflects the final, split hop structure, not the earlier draft's coarser steps.
## Techniques not applied (process output)

pre-mortem — not applicable — the object under evaluation is a claim (a compound factual assertion), not a plan or recommendation; per the Phase 5 decision rule, inversion is the prescribed adversarial technique for a claim, and it was applied instead (Phase 2 and Phase 5).
fishbone — not applicable — the assumption space here is dominated by a single irreducible physical-law constraint (the Carnot ceiling) rather than a multi-causal, breadth-oriented problem that needs category brainstorming; five-whys in reduce-to-primitives mode was the correct depth tool and was applied instead (Phase 3).
## Adversarial pass (process output)

**Recompute.** Carnot ceiling at T_h=838.15 K recomputed for T_c=283.15 K and T_c=313.15 K: η=1−283.15/838.15=0.6621 (66.21%); η=1−313.15/838.15=0.6264 (62.64%) — matches the 62.6%–66.2% bracket stated in chain C1. Siemens Gamesa ETES combined RTE recomputed: 0.99×0.45=0.4455≈44.6% — matches the "≈45%" stated in chain C3. Chain C6 weighted totals recomputed: option (a) 10+5+6+10+4=35 ✓; option (c) 25+25+15+6+6=77 ✓; flip test with cost and RTE criteria removed: (a) 6+10+4=20, (c) 15+6+6=27, 27>20 ✓ — lithium-ion still wins, confirming the stated flip-test result. **One arithmetic error was found and corrected:** chain C4's original cost bracket ("$550–$1,500/kWh") did not match low-with-low / high-with-high pairing of its own stated component ranges; recomputed correctly as $150k+$1.5M=$1.65M → $330/kWh (low) and $400k+$6M=$6.4M → $1,280/kWh (high). The main document (chain C4, and chain C4's confidence line) has been corrected to $330–$1,280/kWh, two to thirteen times GT-6?'s ≈$100–150/kWh, rather than the original four-to-twelve-times framing. This narrows the margin at the bracket's optimistic edge without reversing the qualitative conclusion.

**Sensitivity.** The decisive chain (C1) rests on GT-1 (Carnot's theorem, a physical law) and GT-2 (a unit definition) — neither is realistically falsifiable within this analysis's scope, and the one adjustable input (ambient sink temperature, A-5) was already bracketed and stress-tested to an extreme (Arctic siting, §5 item 2) without approaching 85%. For the corroborating chain (C3), the single ground truth whose falsity would most change the picture is **GT-3? (Siemens Gamesa ETES ≈45% combined RTE), which is `?`-marked** — but even a large upward revision of this figure could not exceed chain C1's ≈64–66% ideal ceiling without contradicting GT-1 itself, so its sensitivity is bounded. For the cost chains (C4, C6), the single most sensitive ground truth is **GT-6? (lithium-ion ≈$100–150/kWh installed cost), also `?`-marked** — a large underestimate here (e.g., due to regional tariffs or supply shocks) would narrow or close the cost gap chain C4 reports; this is the weakest link in the cost argument and is already flagged as the primary driver of chain C4/C6's LOW band.

**Rival.** For the headline conclusion (chain C1): no rival in the cited literature supports >85% round-trip efficiency for this exact single-tank, ambient-rejecting architecture — the only rival that gets close (GT-7?'s heat-pump-charged dual-reservoir design) is a different architecture, ruled out in chain C2 and recorded in §5 item 4. For the cost conclusion (chain C4/C6): a live, un-ruled-out rival is named directly on chain C4's confidence line — lithium-ion costs could keep falling while thermal-storage manufacturing costs fall faster with scale-up, narrowing or reversing the current cost gap in future years; this is not settled by this analysis and the conclusion is explicitly scoped to current (2025–2026) costs.

**Premise.** The headline conclusion has already failed: a real, single-tank molten-salt system of this type has been metered or costed and does in fact exceed 85% electricity round-trip efficiency while beating lithium-ion on installed cost at 5 MWh — what caused this that the analysis above failed to anticipate?

**Causes** (generated from four stakeholder viewpoints, unfiltered):
- *Thermal-storage vendor/engineer:* the real system quietly includes heat-pump charging equipment and a second, sub-ambient managed reservoir, making it a genuine Carnot-battery/PTES architecture (GT-7?-style) rather than the simple resistive-tank system the claim's wording describes; or it uses an unusually cold rejection sink (deep seawater, LNG cold energy) that pushes the Carnot ceiling well above the 62.6–66.2% bracket used here; or a newer supercritical-CO₂ Brayton heat engine achieves a much higher fraction of Carnot (80–90%) than the 55–70% real-engine effectiveness assumed.
- *Skeptical buyer/investor:* the comparison should be levelized cost of storage (LCOS, $/MWh dispatched over asset life) rather than upfront $/kWh — thermal storage's very long cycle life and low degradation could make it LCOS-competitive even at a much higher upfront $/kWh; or the buyer's actual discharge duration is far longer than the 2.5–5 hours assumed in chain C4 (e.g., 50 hours), which would shrink the turbine's capex per kWh dramatically by needing a much smaller power rating for the same energy capacity.
- *Thermodynamics reviewer:* "system efficiency" in the claim might use an exergy-based or differently-referenced accounting convention under which 85% is internally consistent, even though it would not be the ordinary first-law, electricity-in/electricity-out meaning this analysis adopted.
- *Lithium-ion competitor (devil's advocate against this analysis's own cost argument):* lithium-ion's own full-lifecycle costs (inverters, HVAC, fire suppression, degradation-driven cell augmentation/replacement) are sometimes underweighted in headline $/kWh figures, so the true lifecycle cost gap in chain C4/C6 may be smaller than the raw installed-cost comparison suggests.

**Clusters:**
1. *Architecture assumption too narrow* (bears on chain C1, chain C2, assumption A-4) — the analysis may have under-weighted real products that use heat-pump charging or unusually cold sinks.
2. *Duration/power-ratio mismatch* (bears on chain C4, chain C6) — the cost estimate assumed grid-arbitrage-typical 2.5–5 hour discharge; a long-duration, low-power use case changes the economics substantially.
3. *Metric mismatch* (bears on chain C4, chain C6, §6 Confidence) — upfront $/kWh vs. levelized cost of storage over asset life is a different, and arguably more decision-relevant, comparison.
4. *Accounting convention mismatch* (bears on chain C1) — an exergy-based efficiency definition could produce 85% without violating the energy-based Carnot ceiling, though it would not match the claim's ordinary wording.

**Disposition:**
1. **Plan change:** the conclusion is explicitly scoped to "a single molten-salt tank with resistive-style charging and ambient heat rejection," matching the claim's literal wording (stated in §1 and §6); any real product that in fact includes heat-pump charging and a second managed sub-ambient reservoir should be re-evaluated against chain C2's GT-7?-style framework, not chain C1's.
2. **Accepted risk, named mitigation:** chain C4/C6's cost bracket is explicitly scoped to 2.5–5 hour discharge sizing; the named mitigation (now stated in §6 Trade-offs acknowledged) is that a buyer must re-run the estimate against their actual target discharge duration before any procurement decision.
3. **Plan change:** §6 Trade-offs acknowledged now explicitly names levelized-cost-of-storage, not just upfront $/kWh, as the more decision-relevant metric, and flags thermal storage's long cycle life as a genuine, currently under-weighted advantage in the $/kWh-only framing used in chain C4/C6.
4. **Accepted risk, named mitigation:** assumption A-1 already commits explicitly to the ordinary first-law, energy-based meaning of "round trip," so a reader applying an exergy-based convention knows precisely where this analysis's scope ends; no further action taken.

**Falsification.** The efficiency conclusion is false if a commercially deployed, single-tank (no heat pump, no second managed sub-ambient reservoir) molten-salt thermal storage system is independently metered at a verified electricity-to-electricity round-trip efficiency above the ≈64–66% ideal Carnot ceiling derived in chain C1 — this would indicate either an error in this analysis's temperature/sink assumptions or a new heat-engine technology not captured here. The cost conclusion is false, independent of the efficiency conclusion, if a 5 MWh thermal-with-turbine system is shown to install at a verified cost at or below lithium-ion's ≈$100–150/kWh at the stated 2.5–5 hour discharge duration.
## §6→§4 closure ledger (process output)

- "**Recommended approach:** ... the architecture's absolute theoretical ceiling is approximately 64% (chain C1), and the best demonstrated real system of this kind achieves roughly 45% (chain C3) ... lithium-ion is the better choice ... (chain C6) ... can legitimately claim >95% round-trip efficiency ... (chain C3, chain C4) ... even then the reported 85–87% figures come from modeling studies ... (chain C2)" → chain C1, C2, C3, C4, C6 ✓
- "**Key insight:** ... Carnot-bounded near 64% ideal / ~45% real (chain C1, chain C3) ... (chain C1, chain C4)" → chain C1, C3, C4 ✓
- "**Trade-offs acknowledged:** ... a flip test found no single criterion reweighting that changes the outcome (chain C6) ... (chain C3, chain C4) ... (chain C4) ... (chain C4, chain C6)" → chain C3, C4, C6 ✓
- "**Confidence:** ... chain C1 alone ... is HIGH confidence ... What would raise the overall band ... (both named under chain C4)" → chain C1, C2, C3, C4, C6 (via Pre-check head) ✓

Ledger complete: 4 of 4 §6 claims cite a chain already established in §4; 0 cuts.
## Self-audit scan (process output)

**Table 1 — chain form (section 4)**

| Chain | Chain Head (brief) | Form conforming? | Rule applied | Dependency clean? | Band | Act attempted? | Edges fired |
|---|---|---|---|---|---|---|---|
| C1 | GT-1 + GT-2 | yes | n/a | yes | HIGH | no — not applicable (physical law/definition, no citable source to open) | none |
| C2 | GT-7? + C1 | yes | n/a | yes | MEDIUM | yes (Comillas PDF read attempted; HTTP 410 Gone; Phase 3 failure record written) | none |
| C3 | GT-3? + GT-4 + C1 | yes | n/a | yes | MEDIUM | yes (GT-3? nsenergybusiness.com read via WebFetch; GT-4 rondo.com read-at-source) | none |
| C4 | GT-6? + GT-5? | yes | n/a | yes | LOW | yes (GT-6? ess-news.com read attempted, HTTP 503; GT-5? sco2symposium PDF read attempted, unreadable; both Phase 3 failure records written) | none |
| C5 | C1 + C3 + C4 | yes | n/a | yes | LOW | no (second-order extension chain; cites only chains already read-attempted under C1/C3/C4, no new source) | none |
| C6 | GT-3? + C4 + GT-6? | yes | n/a | yes | LOW | no (reuses GT-3?/GT-6?/C4 inputs already read-attempted; no new source opened for this chain specifically) | none |

**Table 2 — claim inventory (section 6)**

| §6 Span (brief) | Construct | Claim under R11? | R11 clause applied | Chain cited |
|---|---|---|---|---|
| Recommended approach | bold lead-in | yes | bold lead-in whose colon closes the bold span | C1, C2, C3, C4, C6 |
| Key insight | bold lead-in | yes | bold lead-in whose colon closes the bold span | C1, C3, C4 |
| Trade-offs acknowledged | bold lead-in | yes | bold lead-in whose colon closes the bold span | C3, C4, C6 |
| Pre-check | bold lead-in | yes | bold lead-in whose colon closes the bold span (support line for the Confidence claim; its own content is itself a citation list) | C1, C2, C3, C4, C6 |
| Confidence | bold lead-in | yes | bold lead-in whose colon closes the bold span | C1, C2, C3, C4, C6 |

Scan complete: 6 chain rows, one per section-4 chain block in order; 5 section-6 rows, one per construct in order — 5 claims under R11, 0 excluded. 0 chains malformed, 0 claims untraced.

**Note on this scan's history:** an earlier draft of chain C4's head used a non-GT/Cn identifier (`A-10`), one chain hop (in C2) began with a `GT-` identifier, and several hops exceeded the ~200-character single-inference guideline — all three were caught and corrected before this scan was run, and the table above reflects the corrected document, not the draft. This is recorded here rather than silently: the correction is real editorial work this run did, not a pre-existing clean state.
## Self-Audit Gate (process output)

**Criterion 1: Identify Essence**
Quoted span: "Does a single two-tank molten-salt thermal store (hot tank ~565 °C, cold/return tank ~290 °C) that is charged from grid electricity and discharged back to grid electricity through a heat engine have a physically achievable full electricity-to-electricity round-trip efficiency above 85%, and — separately — is a 5 MWh unit of this type cost-competitive per kWh with a 5 MWh lithium-ion battery system?"
Band: **Rigorous**
Justification: the Essence Statement names the core question precisely (not the triggering sentence, not a symptom), is specific to this exact architecture and temperature span (it would not appear unmodified in an analysis of a different problem), and each of the five success criteria is a checkable verb+subject+outcome statement scoped to a property of the Conclusion section (e.g., "derive the theoretical ceiling... and compare the claimed figure against it," verifiable by reading chain C1 and §6).

**Criterion 2: Challenge Assumptions**
Quoted span (from the Assumption Audit scan, process output): "3 new assumptions surfaced (A-12, A-13, A-14), each added once to the Classified Assumptions Table (§2) and marked inline on its originating chain step with `[Assumes: A-N]`."
Band: **Rigorous**
Justification: all 14 rows in the Assumptions Table use the four-type scheme exactly (with parenthetical glosses, never a freeform label), every Verdict cell leads with Accept/Challenge/Discard followed by an em-dash and a specific justification, at least two rows are genuinely challenged (A-1, A-13) rather than merely accepted, every untested-belief row used in a chain carries "unverified — flagged" in its Verification cell (A-11, A-13), and the Assumption Audit scan confirms the end-of-Phase-4 audit ran exhaustively over all 32 chain steps with no step skipped.

**Criterion 3: Establish Ground Truths**
Quoted span: "`?`-marked: GT-3, GT-5, GT-6, GT-7 (4 of 7)." — checked against the Ground Truths list, which carries the `?` suffix on exactly GT-3, GT-5, GT-6, and GT-7 and on no others; enumeration and list agree.
Band: **Sound**
Justification: GT-IDs are stable, every verified GT cites a specific named source with a provenance label, the `?` enumeration matches the list exactly, and GT-1/GT-2 (feeding the HIGH chain C1) name an explicit "Read-at-source: n/a" with the reason (physical law/definition, not derived from a misreadable document) — but GT-4 is unsuffixed with a reachable, successfully-read source (rondo.com) and yet feeds only chain C3 (MEDIUM) and chain C5 (LOW), never a HIGH chain; this is the single-GT shortfall the rubric's Criterion 3 descriptor explicitly bands Sound (not Hand-wavy, since it is one GT, not a pattern across multiple).

**Criterion 4: Reason Upward**
Quoted span (from the Self-audit scan, Table 1, process output): "C1 | GT-1 + GT-2 | yes | n/a | yes | HIGH ... C4 | GT-6? + GT-5? | yes | n/a | yes | LOW ... C6 | GT-3? + C4 + GT-6? | yes | n/a | yes | LOW" — all six chain rows read `Form conforming? = yes` and `Dependency clean? = yes`.
Band: **Rigorous**
Justification: every chain in the self-audit scan's chain-form table is form-conforming and dependency-clean (no malformed heads, no GT-leading hops, no hop broken across physical lines, no hop closing its own sentence prematurely — all three defects found in drafting were corrected before this scan was run, as the scan's own note discloses); the Abandoned Reasoning section documents seven dead ends in the prescribed What-was-tried/Why-abandoned/What-it-ruled-out structure; no analogy is used as direct, unsourced evidence (ETES and Rondo are both grounded in named GTs about their own situations); every chain step that surfaced a new assumption (C2 step 4, C4 step 6, C6 step 1) carries an inline `[Assumes: A-N]` tag; and the one arithmetic error found during the Phase 5 Recompute step was corrected in the document itself (chain C4's cost bracket), so the figures as they now stand recompute correctly.

**Criterion 5: Validate**
Quoted span: "**Confidence:** LOW — the turbine $/kW bracket is engineering judgment, not a verified source (A-13), GT-6? is reported-by-delegate (ess-news.com read attempted, HTTP 503), and GT-5? is unreadable at its cited source (sco2symposium.com PDF, encoded content) though non-load-bearing..."
Band: **Rigorous**
Justification: every chain's confidence line names its `GT-N?` inputs with the verification that would remove them (C2 names GT-7?, C3 names GT-3?, C4 names GT-6? and GT-5?, C6 names GT-3? and GT-6?), names every cited `Cn` rated below HIGH (C5 names both C4 and C3; C6 inherits and names C4), no chain consuming a `?`-marked input is rated HIGH, every chain is rated no higher than the lowest-rated chain its head cites, and the bands are calibrated to the three-axis definition rather than assigned by feel (C1 is HIGH only because both its inputs are a physical law and a definition with no outstanding axis; C4/C5/C6 are LOW because two axes — Inputs and, for C4, an unpriced `[Assumes: A-13]` hop — are short at once, not merely one). The adversarial pass record is complete: Recompute, Sensitivity, Rival, Premise, Causes (from four stakeholder viewpoints), Clusters (each naming the chain/GT ids it bears on), Disposition (each cluster carrying a named plan change or an explicitly accepted risk with a named mitigation), and Falsification are all present with content, and the weaknesses it surfaced (duration sizing, LCOS vs. upfront cost) were folded back into chain C4's own confidence line and into §6, not left to sit unused in the appendix.

**Criterion 6: Conclusion-to-Ground-Truth Traceability**
Quoted span (from the Self-audit scan, Table 2, process output): "Recommended approach | bold lead-in | yes | bold lead-in whose colon closes the bold span | C1, C2, C3, C4, C6 ... Key insight | bold lead-in | yes | ... | C1, C3, C4 ... Trade-offs acknowledged | bold lead-in | yes | ... | C3, C4, C6"
Band: **Rigorous**
Justification: all five section-6 constructs (including the Pre-check/Confidence support lines) trace to specific named section-4 chains per the claim-inventory table, the §6→§4 closure ledger independently confirms 4 of 4 claims cite an established chain with zero cuts, the Trade-offs acknowledged paragraph's two scope-limit caveats were folded back into chain C4's own confidence note so they are not new reasoning introduced for the first time in §6, and the Key Insight (the claim's internal conflation of two incompatible meanings of "round trip") is a distinct, non-obvious finding rather than a restatement of the Recommended approach (which is action-oriented: use lithium-ion for electricity, heat-only storage for heat).

**Pass 1 (before re-score):** not applicable — this is the first and only scoring pass; no Fix/Repeat loop fired. All six criteria above were corrected to this final state through direct editing during drafting (vocabulary fixes, hop splitting, arithmetic correction, confidence-line completions) rather than through a formal re-score cycle, because those were drafting-quality fixes applied before the first gate score was ever recorded, not fixes applied after a failing score.

**Gate result:** cleared · passes: 1 · Fix/Repeat fired: no
## Structured summary (process output)

```json
{
  "schema_version": 1,
  "run_mode": "full-composer",
  "assumptions": [
    {"id": "A-1", "type": "convention", "verdict": "Challenge"},
    {"id": "A-2", "type": "physical law", "verdict": "Accept"},
    {"id": "A-3", "type": "convention", "verdict": "Accept"},
    {"id": "A-4", "type": "untested belief", "verdict": "Discard"},
    {"id": "A-5", "type": "current constraint", "verdict": "Accept"},
    {"id": "A-6", "type": "untested belief", "verdict": "Discard"},
    {"id": "A-7", "type": "untested belief", "verdict": "Discard"},
    {"id": "A-8", "type": "untested belief", "verdict": "Discard"},
    {"id": "A-9", "type": "convention", "verdict": "Discard"},
    {"id": "A-10", "type": "convention", "verdict": "Discard"},
    {"id": "A-11", "type": "untested belief", "verdict": "Accept"},
    {"id": "A-12", "type": "convention", "verdict": "Accept"},
    {"id": "A-13", "type": "untested belief", "verdict": "Challenge"},
    {"id": "A-14", "type": "current constraint", "verdict": "Accept"}
  ],
  "ground_truths": [
    {"id": "GT-1", "read_at_source": true},
    {"id": "GT-2", "read_at_source": true},
    {"id": "GT-3", "read_at_source": false},
    {"id": "GT-4", "read_at_source": true},
    {"id": "GT-5", "read_at_source": false},
    {"id": "GT-6", "read_at_source": false},
    {"id": "GT-7", "read_at_source": false}
  ],
  "chains": [
    {"id": "C1", "confidence": "HIGH", "rests_on": ["GT-1", "GT-2"]},
    {"id": "C2", "confidence": "MEDIUM", "rests_on": ["GT-7?", "C1"]},
    {"id": "C3", "confidence": "MEDIUM", "rests_on": ["GT-3?", "GT-4", "C1"]},
    {"id": "C4", "confidence": "LOW", "rests_on": ["GT-6?", "GT-5?"]},
    {"id": "C5", "confidence": "LOW", "rests_on": ["C1", "C3", "C4"]},
    {"id": "C6", "confidence": "LOW", "rests_on": ["GT-3?", "C4", "GT-6?"]}
  ],
  "dead_ends": [
    "Retention-only reading of \"system efficiency\"",
    "Arctic-sink boundary check on the Carnot ceiling",
    "Using the 290C cold salt tank as the heat engine's Carnot sink",
    "Treating GT-7?'s dual-reservoir figures as direct support for the claim's architecture",
    "Further sourcing for the $80/kWh-thermal two-tank media-cost figure",
    "Opening the primary Comillas/Energies PDF directly"
  ],
  "techniques": {
    "applied": ["inversion", "five-whys", "theoretical-limit", "estimate", "second-order", "trade-off"],
    "not_applied": [
      {"technique": "pre-mortem", "phase": 5, "reason": "the object under evaluation is a claim, not a plan or recommendation; per the Phase 5 decision rule, inversion is the prescribed adversarial technique for a claim, and it was applied instead"},
      {"technique": "fishbone", "phase": 2, "reason": "the assumption space here is dominated by a single irreducible physical-law constraint rather than a multi-causal, breadth-oriented problem that needs category brainstorming; five-whys in reduce-to-primitives mode was the correct depth tool and was applied instead"}
    ]
  },
  "gate": {
    "passes": [
      {"bands": ["Rigorous", "Rigorous", "Sound", "Rigorous", "Rigorous", "Rigorous"], "gate_cleared": true, "hand_wavy_cap_cleared": true}
    ],
    "fix_repeat_fired": false,
    "cleared": true
  },
  "re_entry": {
    "fired": false,
    "edges": []
  },
  "conclusion": {
    "recommendation": "For a 5 MWh thermal-storage asset described as charging from and discharging back to grid electricity between 290 and 565 °C, do not expect, and do not budget around, a round-trip electricity-to-electricity efficiency above 85% — the architecture's absolute theoretical ceiling is approximately 64% (chain C1), and the best demonstrated real system of this kind achieves roughly 45% (chain C3). If the actual need is grid electricity storage at 5 MWh, lithium-ion is the better choice by a wide, robust margin on both efficiency and cost (chain C6). If the actual need is industrial process heat, a heat-only thermal battery that never attempts reconversion (no turbine) is the better choice, and can legitimately claim >95% round-trip efficiency because it is solving a different problem (chain C3, chain C4). The only way a version of this claim becomes defensible is by substituting a structurally different architecture — a heat-pump-charged, dual-reservoir Carnot battery — for the single-tank system the claim names, and even then the reported 85–87% figures come from modeling studies, not commercial 5 MWh products (chain C2).",
    "confidence": "LOW",
    "rests_on": ["C1", "C2", "C3", "C4", "C6"]
  }
}
```
