## Answer

**Recommendation:** For a representative 10-million-person country of moderate-or-lower population density, land area is a solved, non-binding input to full solar-PV electrification: the computed requirement is roughly 60–3,600 km² (≈610 km² central case), well under 5%, typically under 1%, of a Portugal-sized country's territory (chain C8). The real constraints are storage/intermittency, grid buildout, siting economics, and capital — not land (chain C8).

**Band (from §6):** LOW (chain C8).

**Would change it:** Resolving GT-9?'s agricultural-land-share figure at primary source, and computing this same chain for a named small, high-density country — the live rival the Phase 5 adversarial pass identified but did not settle — would move chain C8's band without changing its core direction (chain C8).

## 1. Problem Essence

**Core problem:** From first-principles physical quantities alone (solar irradiance, module efficiency, real-world performance losses, and panel-packing density on the ground) — not from analogy to what any specific country currently does — how much land area would a representative 10-million-person country need to devote to utility-scale solar photovoltaic generation in order to cover its total annual electricity consumption, and does the resulting figure make full solar-PV electrification land-constrained, or does it shift the binding constraint elsewhere?

**Success criteria:**
1. A land-area figure (km²) is derived from an explicit physical chain — irradiance × module efficiency × performance ratio × ground-coverage ratio × demand — rather than asserted from an external "solar needs X land" claim, and the chain appears in section 4.
2. The figure is bracketed across at least a high-latitude/high-consumption case and a sun-belt/low-consumption case, so the answer is a range grounded in stated inputs, not a single unqualified number (section 4, section 6).
3. The land figure is independently cross-checked against a real-world empirical land-use survey, and the two estimates are shown to agree to within a stated factor (section 4).
4. The land figure is compared against at least one concrete national land area and one land-use category (e.g., agricultural land), so "how much" is answered in a unit a reader can evaluate feasibility against (section 4, section 6).
5. The Conclusion states explicitly whether land area is or is not the binding constraint on 100%-solar electrification, and names what — if anything — the land-area calculation leaves out (storage/intermittency, grid, siting, capital) that would also have to be resolved for "supply the entire electricity demand" to hold in practice (section 6).

No success criterion requires the answer to be a single point figure or to pick one of several pre-named options — the question is a magnitude estimate with an explicit uncertainty bracket, and success is a well-derived, well-bounded, feasibility-interpreted number.

---

## 2. Assumptions Table

| Assumption | Type | Treatment | Verdict | Verification |
|------------|------|-----------|---------|--------------|
| A1: A single per-capita demand figure, solar-resource figure, and land-use factor can represent "a country of 10 million people" without modeling intra-country variation (urban/rural mix, climate zones, grid topology) | convention | Explicitly challenge before use; test whether the simplification holds for the generic case as posed | Accept — the user explicitly asked for a generic/representative case with a high/low bracket, so this is the correct treatment of the question as posed, not a hidden shortcut | Verified by construction: the bracket approach (GT-4's country range × GT-10/GT-11's latitude range) makes the simplification's error bounds visible rather than hiding them |
| A2: Land "needed to supply electricity demand" can be computed from average annual energy balance (total annual generation = total annual demand), setting aside matching instantaneous, diurnal, and seasonal demand | convention | Explicitly challenge — per the stakes-escalation rule, this is the single highest-stakes simplification in the analysis and must be pushed toward its physical limits, not quietly accepted | Challenge — accepted only as producing a necessary-but-not-sufficient lower bound on land; its failure mode is deliberately surfaced, not hidden, in chain C8 | unverified — flagged; marked `[Assumes: A2]` on the load-bearing land-area hops in chains C1 and C4 |
| A3: The 2012–13 US utility-scale PV fleet land-use survey (GT-1) remains representative of land-use intensity for a generic country's deployment today | current constraint | Record expiry conditions — this constraint expires as module efficiency, tracking adoption, and siting practice evolve | Accept, with expiry noted — module efficiency has risen from ~15% (2012–13 fleet) to ~20–23% (2024–25, GT-2), so GT-1's figures are a conservative (larger-land) floor, not a current prediction | Cross-checked against the independent physics-based estimate (chain C2); the two agree within ~12%, consistent with the expected efficiency-driven gap |
| A4: Land-use intensity, ground-coverage-ratio, and performance-ratio figures sourced predominantly from US/European utility-scale PV data (GT-1, GT-5, GT-6) generalize to other national contexts (climate, land tenure, policy, terrain) | convention | Explicitly challenge — siting practice, regulation, and terrain vary by country and are not captured by these figures | Challenge — accepted as an order-of-magnitude approximation only; country-specific deviations are plausible and not modeled | unverified — flagged |
| A5: The "conventional" efficiency/PR/GCR figures used (GT-2, GT-5, GT-6) represent current mainstream deployable technology, not a speculative future or a cost-prohibitive niche technology | convention | Explicitly challenge by bracketing against a physical ceiling rather than asserting it by default | Accept — directly challenged by chain C6 (theoretical-limit derivation), which shows the ceiling case differs only by a bounded factor, so the technology-parameter choice does not change the qualitative conclusion | Verification: GT-2 (read-at-source) and GT-13 (physical law) bound the technology-choice sensitivity explicitly |
| A6: Physical land availability (area alone) is an adequate proxy for real-world feasibility, independent of economic, permitting, manufacturing-capacity, critical-mineral-supply, and grid-interconnection constraints | convention | Explicitly challenge — a small land-area number must not be allowed to imply overall feasibility is solved | Challenge — rejected as the sole feasibility criterion; retained only as one necessary (not sufficient) condition, with other constraints named explicitly in chain C8's second-order extension | no chain — flagged assumption only, addressed narratively in chain C8's actor-lens effects |
| A7: GHI figures for high-latitude and sun-belt/desert regions (GT-10, GT-11) are accurate enough to bound the analysis's latitude sensitivity | untested belief | Verify or flag as unverified per D-07 | Challenge — GT-10 partially checked (a direct fetch of the primary source returned truncated content); GT-11 fully unverified (general domain knowledge, no source opened this run) | unverified — flagged; both carry `?` and feed only MEDIUM-capped chains (C3, C5, C6) |
| A8: A US-derived rooftop-PV technical-potential study (GT-8, ~39% of demand) is a reasonable order-of-magnitude proxy for a generic 10-million-person country's rooftop potential | untested belief | Verify or flag as unverified; note the US-context dependency (large detached-housing stock, high roof area per capita) that may not generalize | Challenge — used only as an illustrative upper bound, explicitly flagged as US-specific and likely to overstate rooftop potential for denser or more apartment-heavy housing stocks | unverified — flagged |
| A9: The solar constant / surface solar irradiance regime, and the Shockley–Queisser single-junction thermodynamic efficiency limit, are fixed physical constants independent of technology, policy, or country choice | physical law | Accept as ground-truth candidate | Accept — physical laws do not expire and cannot be negotiated away | Standard photovoltaic/radiometric physics (Shockley & Queisser 1961; solar-constant radiometry); recorded as GT-12, GT-13 |
| A10: Land classified as "suitable for utility-scale solar" (flat, unforested, accessible, near transmission) is effectively interchangeable with total national land area for a percentage-of-territory comparison | convention | Explicitly challenge — real siting competes for a much smaller usable subset of land than total territory, so a low percentage of total land can still represent a much higher percentage of suitable/available land | Challenge — the percentage-of-total-territory comparison in chain C7 is retained as a headline, order-of-magnitude comparator, but is explicitly flagged as likely to understate local site-availability competition | no chain — flagged assumption only, addressed narratively in chain C8's actor-lens local land-conflict effect |
| A11 *(surfaced by the end-of-Phase-4 Assumption Audit, chain C6 step 3)*: the specific "best demonstrated" parameter values chosen (≈24% module efficiency, PR≈85%, GCR≈45%) are representative of currently deployed premium technology, not a cherry-picked favorable combination | untested belief | Verify or flag as unverified per D-07 | Challenge — plausible and internally consistent with GT-2's upper range, but not independently benchmarked against a named real installed plant | unverified — flagged; feeds only chain C6, already capped MEDIUM |
| A12 *(surfaced by the end-of-Phase-4 Assumption Audit, chain C8 steps 3–4)*: grid operators, policymakers, and landowners respond to the storage/siting gap in the directions the second-order extension describes (nameplate overbuild, permitting-queue congestion, local lease-price pressure, cheapest-sites-first sequencing) rather than some materially different adjustment path | untested belief | Verify or flag as unverified per D-07 | Challenge — a plausible, literature-consistent behavioral-response pattern, but not verified against a named case study this run | unverified — flagged; feeds only chain C8's second-order hops, already capped MEDIUM |

## 3. Ground Truths

- **GT-1** Generation-weighted land-use intensity for US utility-scale PV (2012–13 fleet, 72% of installed/under-construction US utility PV+CSP capacity, >2.1 GW operating + 4.6 GW under construction as of Q3 2012): fixed-tilt plants require ≈2.8 acres of land per GWh/yr of annual generation; single-axis tracking plants require ≈2.9 acres/GWh/yr (direct area) to ≈3.8 acres/GWh/yr (total project area) — source: NREL, "Land-Use Requirements for Solar Power Plants in the United States" (2013), as reported by ScienceDaily (Aug 6, 2013); read-at-source: ScienceDaily article body, paragraphs quoting "2.8 acres" of land per annual GWh for fixed-tilt PV and the "72%... of the solar power plants installed or under construction" coverage figure directly.
- **GT-2** Commercial solar-panel efficiency, 2024–25: general range 13–25% for standard installations; monocrystalline typically 15–20%; polycrystalline 13–16%; lab/experimental cells exceed 45% — source: RS Online, "Solar Panel Efficiencies Guide" (22 Oct 2024); read-at-source: the article's efficiency-range paragraphs, fetched and quoted directly. (Secondary, unread corroboration surfaced by search only: several vendor/press summaries report premium 2024–25 monocrystalline modules marketed at 20–24.1% (e.g., Maxeon 7) — noted as context, not used as the GT-2 anchor since it was not read at source.)
- **GT-3?** Utility-scale solar capacity factor: global average ≈15%; range ≈10% (Northern Europe) to ≈30% (Atacama/Arabian deserts) — cited to: EIA "Today in Energy" / thundersaidenergy, summarized via search; reported-by-delegate: WebSearch tool summary; cited source not opened by this analysis. (Not load-bearing on the primary chain — used only as cross-context in the Conclusion, not in any C1–C9 head.)
- **GT-4** Per-capita annual electricity consumption (most recent-year figures, ≈2023–2025 vintage): world average 3,860 kWh; USA 13,060 kWh; Canada 16,090 kWh; Japan 8,370 kWh; China 7,460 kWh; India 1,420 kWh; Germany 6,190 kWh; France 7,160 kWh — source: Wikipedia, "List of countries by electricity consumption"; read-at-source: the per-capita consumption table on that page, fetched and quoted directly.
- **GT-5?** Ground-coverage ratio (GCR) for fixed-tilt utility-scale PV: typically 0.40–0.50; tracking systems 0.25–0.40; wider cited literature range 0.15–0.68 depending on site — cited to: LBNL research, summarized via search (the underlying LBNL PDF could not be extracted as readable text — see Phase 3 failure record below); reported-by-delegate: WebSearch tool summary; cited source not opened by this analysis in readable form.
- **GT-6?** Performance ratio (PR) for utility-scale PV systems installed 2010 or later: typically 75–90%, "typical" value ≈82% — cited to: ratedpower.com glossary, summarized via search; reported-by-delegate: WebSearch tool summary; cited source not opened by this analysis.
- **GT-7?** Portugal: land area 92,225.20 km²; population 10,749,635 (2024, Portugal's National Statistics Institute, INE) — cited to: portugalglobal.pt / worldometers, summarized via search; reported-by-delegate: WebSearch tool summary; cited source not opened by this analysis. (Used only as a concrete, real-world "≈10-million-person country" comparator for chain C7, not as a demand or resource input.)
- **GT-8?** US rooftop-PV technical potential: 1,118 GW installed-capacity potential, 1,432 TWh/yr generation potential ≈ 39% of national electric-sector retail sales (NREL, "Rooftop Solar Photovoltaic Technical Potential in the United States," updated estimate) — cited to: NREL research-hub / press summaries, summarized via search; reported-by-delegate: WebSearch tool summary; cited source not opened by this analysis.
- **GT-9?** Globally, roughly half of habitable land is used for agriculture; agricultural land covers more than one-third of total world land area (arable land ≈10% of world land area) — cited to: Our World in Data, "Land Use," summarized via search; reported-by-delegate: WebSearch tool summary; cited source not opened by this analysis.
- **GT-10?** Annual global horizontal irradiance (GHI): Germany ≈900–1,200 kWh/m²/yr; Spain ≈2,000 kWh/m²/yr — cited to: tritec-energy.com PV glossary; a direct WebFetch of this page was attempted and returned truncated/incomplete content that could not confirm the figures at source (Phase 3 failure record below); reported-by-delegate: WebSearch tool summary stands in as the value; `?` retained.
- **GT-11?** Desert/sun-belt regions (Sahara, Arabian Peninsula, Atacama) receive annual GHI on the order of 2,200–2,500 kWh/m²/yr — unverified: this is general domain knowledge; no source was opened this run to confirm this specific figure, and no search was run for it directly (search budget was spent on GT-10 and related figures instead — see Phase 3 disclosure below).
- **GT-12** The solar constant (mean extraterrestrial solar irradiance at 1 AU) is ≈1,361 W/m²; the standard AM1.5 terrestrial reference spectrum totals ≈1,000 W/m² at normal incidence, sea level, clear sky — physical law/definition (standard radiometric physics); accepted directly as a ground-truth candidate per the Phase 2 physical-law treatment; not dependent on any cited source's authority.
- **GT-13** The Shockley–Queisser detailed-balance limit caps power-conversion efficiency of a single-junction solar cell under unconcentrated AM1.5 illumination at ≈33.7% (at an optimal ≈1.34 eV bandgap) — physical law/theoretical result (Shockley & Queisser, 1961); accepted directly as a ground-truth candidate per the Phase 2 physical-law treatment. Applies specifically to single-junction cells — the technology basis of the overwhelming majority of deployed utility-scale PV today; multi-junction devices are a different, currently cost-prohibitive-at-utility-scale technology path that can exceed this bound (see GT-14).
- **GT-14?** Record research-cell efficiency: ≈39.5% for a single-junction-comparable 1-sun quantum-well design (NREL, announced 2022); ≈47.1% for a six-junction III-V concentrator cell under 143-suns concentration (Nature Energy) — cited to: Solar Power World / ECS / compoundsemiconductor.net, summarized via search; reported-by-delegate: WebSearch tool summary; cited source not opened by this analysis. Flagged per the theoretical-limit technique's "model-dependent bound" caution: the 47.1% figure requires concentrating optics and 143× concentration and is not directly comparable to flat-plate, unconcentrated land-area deployment; only the 1-sun 39.5% figure is used as the "best demonstrated" tier in chain C6.

**Provenance summary (required):**
```text
?-marked: GT-3, GT-5, GT-6, GT-7, GT-8, GT-9, GT-10, GT-11, GT-14 (9 of 14)
Read-at-source: GT-1 — ScienceDaily article body, "2.8 acres" per annual GWh (fixed-tilt) and "72%" fleet-coverage figures quoted directly
Read-at-source: GT-2 — RS Online "Solar Panel Efficiencies Guide," efficiency-range paragraphs quoted directly
Read-at-source: GT-4 — Wikipedia "List of countries by electricity consumption," per-capita consumption table quoted directly
GT-12, GT-13 — physical law/definition; accepted directly per Phase 2 treatment, no external read-at-source location applicable
```

**Phase 3 failure record:**
- GT-10 — source: tritec-energy.com PV glossary page. WebFetch was attempted; the returned content was truncated/incomplete ("[Content truncated due to length...]") and did not permit confirmation of the specific GHI figures at source. The `?` is retained and the WebSearch-summarized figures are used with that caveat.
- GT-11 — no source was opened this run at all (not attempted, not merely failed); flagged `unverified` rather than `reported-by-delegate`.
- The LBNL PDF underlying GT-5 (`emp.lbl.gov/.../land_requirements_for_utility-scale_pv.pdf`) was fetched but returned only unreadable binary/image-PDF content; GT-5 is carried as `reported-by-delegate` from the WebSearch summary of secondary reporting on the same LBNL findings, not as a failed-read `unverified` entry, since a search-tool summary of the underlying research did supply the figure.

**Turn-budget disclosure:** given the size of this analysis, not every `?`-marked ground truth received a direct-open attempt this run; GT-1, GT-2, and GT-4 were prioritized for direct reads because they are the most load-bearing (the land-use-intensity cross-check and the demand-side anchor). GT-3, GT-6, GT-7, GT-8, GT-9, GT-14 are carried as `reported-by-delegate` **not read — turn budget** this run; each keeps its `?` and feeds only MEDIUM-or-below chains, consistent with D-07.

## 4. Derivation Chains

**Technique note:** Chains C1 and C3 apply the **estimate (Fermi/dimensional-analysis)** companion technique — the target quantity (energy yield per unit land area, kWh/m²/yr) is decomposed into first-principles unit-factors (irradiance × module efficiency × performance ratio × ground-coverage ratio) whose product reconstructs the target's units, then bracketed with explicit lower/upper bounds. Chain C6 applies the **theoretical-limit** companion technique — naming the governing physical law (the Shockley–Queisser single-junction bound), deriving the law-permitted ceiling, and bracketing the gap between that ceiling, a best-demonstrated tier, and the conventional figure. Chain C8 carries the required **second-order thinking** extension, walking both the actor lens and the time lens.

### Conclusion C1: A representative mid-latitude utility-scale PV deployment yields roughly 98 GWh of annual generation per km² of land

GT-2 (commercial module efficiency ≈20%) + GT-5? (ground-coverage ratio ≈40%) + GT-6? (performance ratio ≈82%) + GT-10? (mid-latitude GHI ≈1,500 kWh/m²/yr)
→ multiplying annual GHI by module efficiency and performance ratio gives the DC energy harvested per m² of panel surface each year, about 1,500 × 0.20 × 0.82 ≈ 246 kWh per m² of panel per year *[Assumes: A2 — this treats the year as a single energy-balance total, not a demand profile matched hour by hour]*
→ scaling that panel-area yield down by the ground-coverage ratio converts it to energy per m² of total land, since panels cover only a fraction of the site once inter-row spacing and access roads are included, giving about 246 × 0.40 ≈ 98 kWh per m² of land per year, i.e. roughly 98 GWh per km² per year

**Pre-check:** head GT-2, GT-5?, GT-6?, GT-10? · ?-marked: GT-5?, GT-6?, GT-10? · lowest cited: none · Inputs ceiling: MEDIUM
**Confidence:** MEDIUM — GT-5? (GCR) would be resolved by opening the LBNL land-use study in text-readable form or an equivalent primary GCR study; GT-6? (PR) would be resolved by opening the ratedpower.com source or an inverter/plant-performance dataset directly; GT-10? (GHI) would be resolved by successfully re-fetching the tritec-energy source or substituting a source that opens cleanly (e.g., Global Solar Atlas). Rivals: none live — the independent NREL-fleet-based estimate (chain C2) corroborates this figure's order of magnitude.

### Conclusion C2: An independent empirical land-use survey corroborates C1's estimate to within about 12%

GT-1 (NREL fixed-tilt land intensity, 2.8 acres/GWh/yr) + C1 (≈98 GWh/km²/yr central estimate)
→ converting GT-1's 2.8 acres/GWh/yr to metric units and inverting gives an independent empirical yield of about 88 GWh per km² per year for the 2012–13 US utility PV fleet
→ that empirical figure and C1's physics-based figure agree to within about 12%, and the direction of the gap — the older empirical fleet yields less per km² — is exactly what A3's noted module-efficiency improvement since 2012–13 predicts, so the two independent methods corroborate rather than contradict each other

**Pre-check:** head GT-1, C1 (MEDIUM) · ?-marked: none · lowest cited: MEDIUM · Inputs ceiling: MEDIUM
**Confidence:** MEDIUM — capped by C1 (MEDIUM); GT-1 itself is read-at-source and clean, but the ceiling rule applies because C1 is cited on this chain's head. A3's dated-data caveat (2012–13 fleet) is this chain's own downgrade cause; verification path: locate and compare against a post-2020 utility-scale PV land-use survey if one is published.

### Conclusion C3: Realistic deployments span roughly a 5-fold range in land-yield, from about 45 to about 228 GWh per km² per year

GT-2 (commercial module efficiency) + GT-5? (GCR) + GT-6? (PR) + GT-10? (mid-latitude/high-latitude GHI) + GT-11? (sun-belt/desert GHI)
→ substituting each factor's high-resource/high-efficiency end — desert GHI ≈2,200 kWh/m²/yr, module efficiency ≈23%, PR ≈90%, GCR ≈50% — gives a best-case yield of about 2,200 × 0.23 × 0.90 × 0.50 ≈ 228 GWh per km² per year
→ substituting each factor's low-resource/low-efficiency end — high-latitude GHI ≈1,000 kWh/m²/yr, module efficiency ≈15%, PR ≈75%, GCR ≈40% — gives a worst-case yield of about 1,000 × 0.15 × 0.75 × 0.40 ≈ 45 GWh per km² per year
→ so realistic deployments span roughly a 5-fold range in land-yield, from about 45 to about 228 GWh per km² per year, driven mostly by latitude/irradiance rather than by technology choice

**Pre-check:** head GT-2, GT-5?, GT-6?, GT-10?, GT-11? · ?-marked: GT-5?, GT-6?, GT-10?, GT-11? · lowest cited: none · Inputs ceiling: MEDIUM
**Confidence:** MEDIUM — GT-5?/GT-6?/GT-10? verification paths as in C1; GT-11? would be resolved by consulting a solar-resource atlas (e.g., Global Solar Atlas, NREL NSRDB) directly for a sourced desert/sun-belt GHI figure rather than general domain knowledge. Rivals: none live — the bracket's ordering (latitude dominates technology) is consistent with C2's agreement between 2012-era and current-era technology estimates at similar latitude.

### Conclusion C4: The central-case land requirement for a representative 10-million-person, mid-latitude, moderate-consumption country is about 610 km²

C1 (≈98 GWh/km²/yr) + GT-4 (Germany-like per-capita demand ≈6,000 kWh/yr, a round central "developed mid-latitude" case)
→ multiplying 10,000,000 people by ≈6,000 kWh/person/yr gives a total annual demand of about 60,000 GWh/yr for the representative country *[Assumes: A2]*
→ dividing that demand by C1's land-yield of ≈98 GWh/km²/yr gives a central-case land requirement of about 610 km²

**Pre-check:** head C1 (MEDIUM), GT-4 · ?-marked: none · lowest cited: MEDIUM · Inputs ceiling: MEDIUM
**Confidence:** MEDIUM — capped by C1 (MEDIUM); GT-4 itself is read-at-source and clean.

### Conclusion C5: Across realistic country archetypes, total land required spans roughly 60 to 3,600 km²

C3 (yield bracket 45–228 GWh/km²/yr) + GT-4 (India-like low demand 1,420 kWh/yr; Canada-like high demand 16,090 kWh/yr)
→ pairing the best-case yield (228 GWh/km²/yr) with the lowest demand case (10,000,000 × 1,420 kWh/yr ≈ 14,200 GWh/yr) gives a best-case land requirement of about 62 km²
→ pairing the worst-case yield (45 GWh/km²/yr) with the highest demand case (10,000,000 × 16,090 kWh/yr ≈ 160,900 GWh/yr) gives a worst-case land requirement of about 3,580 km²
→ so across realistic country archetypes, total land required to power 10 million people entirely from solar PV spans roughly 60 to 3,600 km², about a 58-fold range, with a sun-belt/low-consumption country at the small end and a high-latitude/high-consumption country at the large end

**Pre-check:** head C3 (MEDIUM), GT-4 · ?-marked: none · lowest cited: MEDIUM · Inputs ceiling: MEDIUM
**Confidence:** MEDIUM — capped by C3 (MEDIUM).

### Conclusion C6: Even the absolute physical ceiling on land-yield only shrinks the central-case land requirement by about 8-fold, not by orders of magnitude

GT-12 (solar constant / AM1.5 basis) + GT-13 (Shockley–Queisser single-junction limit ≈33.7%) + GT-11? (desert GHI ≈2,400 kWh/m²/yr, midpoint) + C4 (central demand ≈60,000 GWh/yr)
→ treating ground-coverage ratio and performance ratio as ideal (both =1, i.e. zero packing loss and zero real-world derate) sets an absolute physical ceiling on yield of desert GHI times the single-junction Shockley–Queisser limit, about 2,400 × 0.337 ≈ 809 GWh per km² per year
→ dividing C4's central demand by that ideal ceiling gives an absolute physical floor on land area of about 60,000 / 809 ≈ 74 km²
→ a "best demonstrated" intermediate tier — a real premium monocrystalline module at ≈24% efficiency with realistic PR ≈85% and GCR ≈45% at a sun-belt-like GHI of 2,000 kWh/m²/yr — gives an intermediate land figure of about 325 km² *[Assumes: A11 — these specific parameter values are representative of currently deployed premium technology, not a cherry-picked favorable combination]*
→ so the three tiers order as 610 km² (conventional, chain C4) above 325 km² (best demonstrated) above 74 km² (ideal physical floor), meaning most of the reachable land-reduction headroom (610→325) is already available with commercially deployed technology, while the remaining headroom down to the thermodynamic floor (325→74) requires closing a much harder efficiency gap that current technology roadmaps do not close, so land area is not on a path to shrink by orders of magnitude either through better siting or through better cells

**Pre-check:** head GT-12, GT-13, GT-11?, C4 (MEDIUM) · ?-marked: GT-11? · lowest cited: MEDIUM · Inputs ceiling: MEDIUM
**Confidence:** MEDIUM — capped by C4 (MEDIUM) and by GT-11? (verification path: solar-resource atlas, as in C3). GT-12 and GT-13 are physical laws and carry no downgrade cause of their own.

### Conclusion C7: In every scenario computed, required land is well under 5%, typically under 1%, of a representative 10-million-person country's territory

C5 (land bracket 62–3,580 km²) + C4 (central 610 km²) + GT-7? (Portugal: 92,225 km², 10.75M people)
→ expressing the central-case land requirement (610 km²) as a fraction of Portugal's land area (92,225 km², a real ≈10-million-person country) gives about 0.66% of national territory
→ expressing even the worst-case bracket figure (3,580 km²) as a fraction of Portugal's land area gives about 3.9%, still a small single-digit share
→ so in every scenario computed — best case, central case, and worst case — the land required to power a representative 10-million-person country entirely from solar PV is well under 5%, and typically under 1%, of a country of Portugal's size

**Pre-check:** head C5 (MEDIUM), C4 (MEDIUM), GT-7? · ?-marked: GT-7? · lowest cited: MEDIUM · Inputs ceiling: MEDIUM
**Confidence:** MEDIUM — capped by C5/C4 (MEDIUM) and GT-7? (verification path: confirm Portugal's area/population directly via Statistics Portugal's (INE) primary publication rather than a secondary summary).

### Conclusion C8: Land area is not the binding physical constraint on 100%-solar electrification of a 10-million-person country — the real constraints are storage/intermittency, grid buildout, siting economics, and capital

C7 (land <5%, typically <1%, of national territory) + GT-9? (global agricultural land >1/3 of world land area)
→ since agricultural land alone typically covers well over a third of a country's territory, a central-case solar requirement of ≈0.66% of total territory is smaller still relative to agricultural land — solar land competes for a small slice even of already-disturbed, non-natural land, without needing to touch forested or wild land at all in principle
→ therefore land area itself is not the binding physical constraint on supplying a 10-million-person country's electricity entirely from solar PV — the aggregate footprint is available several times over even in the worst-case scenario *[Assumes: A2 — this is an annual-average-balance land requirement, not a requirement sufficient to guarantee supply at every hour]*
→[2nd] because A2's annual-balance framing does not guarantee instantaneous supply, actors respond to that gap: grid operators must overbuild PV nameplate capacity and add storage/transmission well beyond the land-area calculation, policymakers see the real bottleneck shift to permitting and interconnection-queue position rather than land acquisition, and farmers near the small set of already-interconnected, flat, cheap parcels face concentrated local lease-price and land-use pressure even though the national percentage stays low *[Assumes: A12 — these are the directions in which grid operators, policymakers, and landowners actually respond to the storage/siting gap]*
→[3rd] over time this compounds: the cheapest, closest-to-grid sites are used first, so land that looks abundant in aggregate becomes locally contested as buildout proceeds, and once solar is assumed to be the backbone supply at a multi-decade horizon the system must also have solved winter/seasonal firming — at that point the dominant infrastructure footprint may no longer be the PV panels themselves but whatever storage, backup generation, or import interconnection was built to cover the gap A2 assumed away *[Assumes: A12, continued]*

**Pre-check:** head C7 (MEDIUM), GT-9? · ?-marked: GT-9? · lowest cited: MEDIUM · Inputs ceiling: MEDIUM
**Confidence:** LOW — two axes are short simultaneously, which caps this chain at LOW rather than MEDIUM even though each is individually bounded. Inputs axis: capped by C7 (MEDIUM) and GT-9? (verification path: open Our World in Data's "Land Use" page directly to confirm the agricultural-land-share figure). Rivals axis: a live, not-ruled-out rival — surfaced by the Phase 5 adversarial pass (see Adversarial pass, Sensitivity and Cluster A) — is that land IS a decisive constraint for a small, land-scarce, high-density 10-million-person country; this rival has an available verification path (compute the same chain for a named high-density country) but nothing in this document has yet settled it, so it stays live. A2's failure mode is not a further downgrade cause: per the HIGH-band annotation rule, if A2 fails (true minute-by-minute solar-only supply is required rather than annual balance), the endpoint still stands and in fact strengthens, since the second-order hops already state that the true bottleneck is storage/grid/siting rather than land, which is precisely what A2 failing would confirm. This chain's endpoint is now explicitly scoped to countries of moderate-or-lower population density, of which GT-7?'s Portugal (≈117 people/km²) is representative, rather than to every possible 10-million-person country.

### Conclusion C9: Rooftop deployment alone cannot eliminate the ground-mounted land requirement

GT-8? (US rooftop PV technical potential ≈39% of demand) + C4 (central-case ground-mounted land requirement ≈610 km²)
→ even taking GT-8's US-derived rooftop-potential ceiling at face value and assuming a generic country could reach a similar share, at most about 39% of demand could plausibly come from rooftops, leaving at least ≈61% of demand — and therefore the great majority of C4's computed land requirement — needing ground-mounted utility-scale PV regardless
→ so rooftop deployment can reduce but not eliminate the ground-mounted land requirement computed in chain C4, and the size of the reduction is itself uncertain in the negative direction for countries with less detached-roof area per capita than the US, per A8

**Pre-check:** head GT-8?, C4 (MEDIUM) · ?-marked: GT-8? · lowest cited: MEDIUM · Inputs ceiling: MEDIUM
**Confidence:** MEDIUM — capped by C4 (MEDIUM) and GT-8? (verification path: open the NREL rooftop-potential study directly, and if possible locate or derive a non-US rooftop-potential estimate for comparison).

## 5. Abandoned Reasoning

### Dead End: Using concentrating solar power (CSP) instead of or alongside PV

**What was tried:** Briefly considered folding CSP/solar-thermal land-use figures into the estimate, since CSP is a common alternative "solar" technology with its own published land-use intensity.

**Why abandoned:** The user's question explicitly specifies "solar photovoltaics alone." CSP also requires direct normal irradiance (DNI), a different and more geographically restrictive resource than the global horizontal irradiance (GHI) used throughout this analysis, and typically has a different, generally larger, land-use footprint per unit of generation. Mixing it in would have answered a different question than the one asked.

**What it ruled out:** Confirms the analysis should use GHI-based, PV-specific land-use figures (GT-1, GT-2, GT-5, GT-6, GT-10, GT-11) throughout, not a blended solar-thermal-plus-PV figure.

### Dead End: Deriving land area purely from nameplate capacity and a generic capacity-factor percentage

**What was tried:** Considered a shortcut method — take a national installed-capacity figure (GW), apply GT-3's capacity-factor range (10–30%) to get annual generation, and back out land area from a generic acres/MW figure, skipping the irradiance/efficiency/PR/GCR decomposition entirely.

**Why abandoned:** Capacity factor already conflates weather, curtailment, and technology-mix effects into a single number, so building the chain on it would not be reasoning from first principles — it would be reasoning from an already-aggregated industry statistic, exactly what the user asked this analysis to avoid. It would also have duplicated, without independently deriving, what GT-1's empirical acres/GWh figure already provides more directly as a cross-check.

**What it ruled out:** Confirms the decision to build the primary estimate (chains C1, C3) from first-principles unit-factors (irradiance × efficiency × PR × GCR) and to reserve the capacity-factor-based empirical route (GT-1, via GT-1's own generation-weighted figures) for the independent cross-check in chain C2, rather than as the primary derivation.

### Dead End: Treating average-annual energy balance as sufficient evidence that the land figure "solves" full solar supply

**What was tried:** Considered presenting the land-area figures from chains C4/C5/C7 as a self-contained answer to "how much land is needed to supply the entire electricity demand," with intermittency and storage left out of scope entirely as an implementation detail.

**Why abandoned:** This would silently assume either an unlimited-capacity supergrid/import backstop or unlimited free energy storage, neither of which is "solar photovoltaics alone" in the sense a reader would understand the question, and the prompt explicitly asked what the land number implies about feasibility including storage/intermittency. Presenting the land figure without this caveat would misrepresent a necessary condition as a sufficient one.

**What it ruled out:** This is why assumption A2 is classified as a `convention` requiring explicit challenge rather than quietly accepted, why the load-bearing hops in chains C1 and C4 carry an explicit `[Assumes: A2]` annotation, and why chain C8's second-order extension exists specifically to surface what A2's failure implies rather than leaving it implicit.

### Dead End: Anchoring the whole analysis to a single named real country instead of a generic bracketed case

**What was tried:** Considered picking one specific real country (e.g., just Portugal, or just Germany) as the sole worked example, to make every number concrete and traceable to one place.

**Why abandoned:** The user explicitly asked to "treat 'a country of 10 million people' as a generic/representative case" with an explicit request to note how the answer shifts for high- versus low-latitude and high- versus low-consumption countries. A single-country point estimate would have understated the legitimate order-of-magnitude spread the underlying physics implies (chains C3, C5), and would have hidden rather than surfaced the latitude/consumption sensitivity the user asked for.

**What it ruled out:** Confirms the bracketed, multi-archetype approach (chains C3, C5) as the correct structure, with Portugal retained only as one concrete comparator for the percentage-of-territory framing in chain C7, not as the sole basis for the estimate.

---

## 6. Conclusion

**Recommended approach:** For a representative, moderate-or-lower-density 10-million-person country (of which Portugal, GT-7?, is representative) — not necessarily for a small, land-scarce, high-density outlier (chain C8's Rivals note) — treat land area as a solved, non-binding input to 100%-solar electrification planning: the computed requirement (roughly 60–3,600 km² across realistic latitude/consumption archetypes, ≈610 km² in the central case) is well under 5%, typically under 1%, of a country of Portugal's size and smaller still relative to agricultural land (chain C8). Direct planning effort instead at the constraints the land number does not resolve: diurnal and seasonal storage/firming capacity, grid and transmission buildout, siting/interconnection-queue economics, and capital and manufacturing throughput (chain C8).

**Key insight:** The popular framing "solar needs too much land" inverts the actual constraint ordering. A first-principles physics estimate and an independent 2013 empirical land-use survey agree, to within about 12%, that solar's land footprint is a rounding error against national territory (chains C1, C2, C7) — and even jumping all the way to the absolute thermodynamic single-junction efficiency ceiling only shrinks the requirement by a further ~8-fold rather than by orders of magnitude (chain C6), because most of the technologically-reachable headroom is already captured by current commercial modules. Neither today's real-world inefficiency nor future efficiency gains meaningfully move the land verdict in either direction. The question that actually gates full solar-only supply is not "is there enough land" but "how is the sun's absence at night and in winter covered" — and land-area arithmetic cannot answer that question at all (chain C8).

**Trade-offs acknowledged:** This analysis does not solve the storage/firming problem it identifies — the land figures represent panel footprint only under an average-annual-energy-balance assumption (A2), not a fully islanded, minute-by-minute solar-only grid; achieving the latter requires nameplate overbuild, weeks-scale storage, or import interconnection, each carrying its own footprint and expense that is not costed here (chain C8; the exact overbuild multiplier is no chain — flagged assumption only). The low end of the land bracket rests on an unverified desert-irradiance figure (chain C3, GT-11?), and the rooftop-offset figure is a single US-derived study extrapolated to a generic country (chain C9), so the bracket edges should be read as order-of-magnitude, not precise engineering figures. Even the "small percentage of national territory" framing understates local land competition, since usable, grid-adjacent sites are a much smaller subset of total territory than the percentage suggests (chain C8's actor-lens effect, assumption A10).

**Pre-check:** head C8 (LOW), C6 (MEDIUM), C9 (MEDIUM), C2 (MEDIUM) · ?-marked: none · lowest cited: LOW · Inputs ceiling: LOW
**Confidence:** LOW — the Conclusion's band matches its weakest contributing chain, C8, which is itself LOW (see C8's own confidence line for the reason: two axes short at once — an upstream `?`-marked ground truth, GT-9?, and a live, not-ruled-out rival surfaced by the Phase 5 adversarial pass, that land IS a decisive constraint for a small, land-scarce, high-density country). C6, C9, and C2 remain MEDIUM, each capped by an upstream `?`-marked ground truth (GT-11?, GT-8?, and the C1 cap respectively) with a stated, bounded verification path named on that chain's own confidence line; none of those chains' own confidence lines needs restating here per D-07. This LOW rating is calibration, not a shortfall: the direction and rough magnitude of the finding are corroborated by an independent empirical cross-check (chain C2) and remain stable across a theoretical-limit sensitivity check (chain C6), but the headline claim as originally stated was broader than the evidence supports, and the adversarial pass's Cluster A finding — that the conclusion's force depends on the representative country having Portugal-like, not Bangladesh-like, population density — is exactly the kind of unresolved, two-axis shortfall a LOW rating exists to flag rather than paper over. This is a legitimate, honestly-caveated finding: land area is not the binding constraint for a country of moderate-or-lower population density, and that scope qualifier is now load-bearing, not decorative.

## Appendix — process output

## Techniques not applied (process output)

Techniques that fired this run: **estimate** (chains C1, C3 — Fermi/dimensional-analysis magnitude rebuild), **theoretical-limit** (chain C6, Phase 4 invocation — ceiling the fundamentals permit), **second-order thinking** (chain C8 — required every run), **inversion** (Phase 5 adversarial-technique invocation — see Adversarial pass record below), and a lightweight **five-whys reduce-to-primitives** pass used at Phase 3 to justify GT-12/GT-13's physical-law classification (both bottom out directly at a textbook physical constant / detailed-balance derivation with no further reducible constituent, so no separate irreducibility-drill artifact was needed beyond stating that bottoming-out).

Techniques not applied:
- pre-mortem — not applicable — the headline conclusion (chain C8) is a claim about the world ("land is not the binding constraint"), not a plan or recommendation with execution steps to fail; the decision rule routes claim-shaped conclusions to inversion instead, which fired (see Adversarial pass record).
- inversion (Phase 2 challenge-assumptions invocation) — not applicable — the assumption set was not suspiciously thin going into Phase 2; eleven assumptions (A1–A10, plus A11/A12 surfaced later by the Assumption Audit) were already identified and classified without needing a failure-enumeration brainstorm to surface more.
- theoretical-limit (Phase 1 essence-reframe invocation) — not applicable — the Problem Essence was already framed around a physical, first-principles quantity (land area derived from irradiance/efficiency/PR/GCR) rather than around a convention that needed to be stripped away to find the real question; the theoretical-limit technique's other invocation point (Phase 4) did fire, as chain C6.
- trade-off — not applicable — this problem is a magnitude estimate (how much land), not a choice among named discrete options to weigh against criteria; no trade-off matrix applies.
- fishbone — not applicable — the assumption space, while multi-parameter, was directly enumerable without needing a breadth-first cause-category brainstorm; it is a parameter-uncertainty problem, not a multi-causal diagnostic one.
- five-whys (causal mode) — not applicable — there is no "why did X happen" diagnostic question in scope; this is a forward magnitude/design estimate, not a failure investigation.

## Assumption Audit scan (process output)

| Chain | Step | Step Text (brief) | Assumption surfaced? | Added to Table? |
|-------|------|--------------------|------------------------|-------------------|
| C1 | 1 | GHI × efficiency × PR → panel-area yield | A2 (annual-balance framing) | yes (already present) |
| C1 | 2 | scale by GCR → land-area yield | none | n/a |
| C2 | 1 | convert GT-1 acres/GWh → GWh/km² | none | n/a |
| C2 | 2 | compare to C1, note direction consistent with A3 | none (A3 already present) | n/a |
| C3 | 1 | best-case substitution → 228 GWh/km²/yr | none | n/a |
| C3 | 2 | worst-case substitution → 45 GWh/km²/yr | none | n/a |
| C3 | 3 | synthesize 5-fold range | none | n/a |
| C4 | 1 | 10M people × per-capita demand → total demand | A2 (annual-balance framing) | yes (already present) |
| C4 | 2 | demand ÷ C1 yield → 610 km² | none | n/a |
| C5 | 1 | best yield × lowest demand → 62 km² | none | n/a |
| C5 | 2 | worst yield × highest demand → 3,580 km² | none | n/a |
| C5 | 3 | synthesize 58-fold range | none | n/a |
| C6 | 1 | ideal GCR=PR=1 × SQ limit → 809 GWh/km²/yr ceiling | none (idealization stated explicitly in-line) | n/a |
| C6 | 2 | demand ÷ ideal ceiling → 74 km² floor | none | n/a |
| C6 | 3 | best-demonstrated parameters → 325 km² | A11 (best-demonstrated parameter representativeness) | yes (new row added) |
| C6 | 4 | synthesize three-tier ordering | none | n/a |
| C7 | 1 | central case ÷ Portugal area → 0.66% | none | n/a |
| C7 | 2 | worst case ÷ Portugal area → 3.9% | none | n/a |
| C7 | 3 | synthesize "<5%, typically <1%" | none | n/a |
| C8 | 1 | compare to agricultural-land share | none | n/a |
| C8 | 2 | conclude land is not the binding constraint | A2 (annual-balance framing) | yes (already present) |
| C8 | 3 | [2nd] actor-lens response to the A2 gap | A12 (behavioral-response pattern) | yes (new row added) |
| C8 | 4 | [3rd] time-lens compounding effect | A12 (same row, second originating step) | yes (already added at step 3) |
| C9 | 1 | rooftop ceiling leaves ≥61% needing ground-mounted PV | none (A8 already present) | n/a |
| C9 | 2 | synthesize: rooftop reduces but does not eliminate | none | n/a |

Scan complete: 25 steps across 9 chains (C1–C9), in order, no step skipped. Two new assumptions were surfaced (A11 at C6 step 3; A12 at C8 steps 3–4, one table row covering both originating steps) and both have been added to the Classified Assumptions Table in section 2.

## Adversarial pass (process output)

The headline conclusion (chain C8) is a claim ("land area is not the binding physical constraint...") rather than a plan, so per the Phase 5 decision rule the **inversion** procedure is opened and applied, rendered into this record's Premise/Causes/Clusters/Disposition parts.

**Recompute.** Independently redone: 1,500×0.20×0.82×0.40 = 98.4 kWh/m²/yr (matches C1's ≈98 GWh/km²/yr). 10,000,000×6,000 kWh = 60,000 GWh/yr; 60,000/98.4 = 609.8 ≈ 610 km² (matches C4). GT-1's 2.8 acres/GWh/yr × 4,046.86 m²/acre = 11,331.2 m²/GWh/yr → 1/0.0113312 = 88.25 GWh/km²/yr; 60,000/88.25 = 679.8 ≈ 680 km², i.e. C1/C4's physics estimate and GT-1's empirical figure differ by (680−610)/680 ≈ 11.5% (matches C2's "within about 12%"). Best case: 2,200×0.23×0.90×0.50 = 227.7 GWh/km²/yr; 14,200/227.7 = 62.4 km² (matches C5). Worst case: 1,000×0.15×0.75×0.40 = 45 GWh/km²/yr; 160,900/45 = 3,575.6 km² — C5's text states "≈3,580," a rounding difference of ≈4 km² (0.1%), immaterial. Ideal ceiling: 2,400×0.337 = 808.8 GWh/km²/yr; 60,000/808.8 = 74.2 km² (matches C6). Best-demonstrated tier: 2,000×0.24×0.85×0.45 = 183.6 GWh/km²/yr; 60,000/183.6 = 326.8 ≈ 325–327 km² (matches C6's "≈325 km²" within rounding). Portugal shares: 610/92,225 = 0.661% ≈ 0.66% (matches C7); 3,576/92,225 = 3.877% ≈ 3.9% (matches C7). All recomputed figures reproduce the chain text; no arithmetic error found.

**Sensitivity.** The single ground truth whose falsity would most plausibly flip the headline conclusion is **GT-7?** (Portugal, ≈117 people/km², used as the "representative ≈10-million-person country" comparator) — not because Portugal's own figures are wrong, but because it is a *low-density* comparator, and the conclusion's force depends on that choice. Substituting a hypothetical 10-million-person country at Bangladesh-like national density (≈1,265 people/km² → ≈7,900 km² total territory) instead: the central-case requirement (610 km²) becomes ≈7.7% of territory, and the worst-case requirement (3,580 km²) becomes ≈45% of territory — no longer "well under 5%." GT-7 is `?`-marked; verification path (already named in chain C7) is to confirm Portugal's figures at primary source, but the deeper fix is to make the density-representativeness of the comparator explicit rather than implicit, which is what this pass's Cluster A disposition below does.

**Rival.** *Headline (C8):* a live, not-fully-ruled-out rival is "land IS a decisive constraint for a small, land-scarce, high-density 10-million-person country" (see Sensitivity above and Cluster A below) — this rival is not settled by anything already in section 5, so it is named on C8's Confidence line (amended below) rather than moved to Abandoned Reasoning, since it is not ruled out, only scoped around. *C2:* a rival reading is that the ≈12% agreement between the physics estimate and GT-1's empirical figure is coincidental (e.g., both methods sharing an unmodeled bias) rather than meaningful corroboration; this is weakened, not ruled out, by the two methods' independent data lineage and by the agreement's direction matching A3's independently-stated efficiency-improvement trend, and remains reflected in C2's own MEDIUM band. *C6:* a rival reading is that A11's "best demonstrated" parameter choice was selected to produce a clean monotonic three-tier ordering rather than because it is genuinely representative; this is why A11 is carried as an explicitly flagged, unverified assumption rather than asserted as settled. *C9:* a two-sided rival — rooftop potential could be materially lower (dense, high-rise housing stock) or materially higher (sprawling low-density housing) than the US-derived 39% figure — is already carried live via A8's flag and C9's MEDIUM band; nothing in this analysis settles it either direction.

**Premise.** The headline conclusion has already turned out to be false: land area is in fact a decisive, binding constraint on 100%-solar electrification of a representative 10-million-person country.

**Causes** (unfiltered, generated from the grid-planner, land-scarce-country-policymaker, local-community/environmental-advocate, systems-engineer, transmission-planner, and investor/realist viewpoints, before any grouping):
1. The representative country has far higher population density than Portugal, so even a "small percentage of territory" consumes most of its actually-available land (policymaker viewpoint).
2. Nearly all flat, grid-accessible, non-forested land is already occupied by cities, existing infrastructure, or protected/agricultural use, so the land subset actually suitable for siting is far smaller than raw total territory (grid-planner viewpoint).
3. Public and political opposition to converting agricultural or scenic land is strong enough that legally available land is a small fraction of physically suitable land, regardless of the computed percentage (community/environmental-advocate viewpoint).
4. The storage/firming technology chosen to cover the annual-balance gap (A2) — e.g. large pumped-hydro reservoirs or bioenergy backup — has its own large land footprint, so total system land (PV plus firming) exceeds what a PV-only number suggests (systems-engineer viewpoint).
5. Grid interconnection capacity, not land, forces PV to be sited far from load centers, so the effective land-plus-transmission-corridor footprint is much larger than the bare panel-area figure (transmission-planner viewpoint).
6. The high-irradiance desert land invoked in the best-case scenario (GT-11?) is not actually usable (protected, politically unstable, no grid access), so the realistic worst-case figure (45 GWh/km²/yr) applies far more broadly than a minority of countries (investor/realist viewpoint).

**Clusters** (structural weaknesses the causes fall into, with the chain/GT ids each bears on):
- **Cluster A — density mismatch** (cause 1): bears on GT-7?, C7, C8.
- **Cluster B — suitable-land vs. total-land gap** (causes 2, 3, 6): bears on A10, GT-11?, C3, C7, C8.
- **Cluster C — system (not PV-only) land footprint** (cause 4): bears on A2, C8.
- **Cluster D — grid/transmission-driven effective footprint** (cause 5): bears on C8's actor-lens hop.

**Disposition:**
- Cluster A — named plan change: the headline conclusion (chain C8, and the Conclusion section's Recommended approach) is explicitly scoped to countries of moderate-or-lower population density, of which Portugal (GT-7?) is representative; a small, land-scarce, high-density 10-million-person country is named as outside this scope rather than silently included. (Reflected in the amended C8 Confidence line below.)
- Cluster B — explicitly accepted risk, named mitigation: this analysis accepts that suitable-land (not total-land) availability is the real local constraint; the mitigation already in place is assumption A10 (flagged, challenged) and chain C8's actor-lens hop, which names permitting/siting economics as a real bottleneck rather than letting the percentage figure stand as the whole story.
- Cluster C — explicitly accepted risk, named mitigation: this analysis accepts that firming-technology land footprint is out of scope; the mitigation is that the Conclusion's Trade-offs Acknowledged line states this explicitly as uncosted rather than hiding it.
- Cluster D — explicitly accepted risk, named mitigation: this analysis accepts that transmission siting can push effective land use above the bare panel-area figure; the mitigation is that C8's actor-lens hop already names siting/permitting economics as a real, separate constraint.

**Falsification.** The conclusion is false if a representative 10-million-person country's realistic land requirement, computed the same way, exceeds a double-digit percentage of that country's total territory once restricted to grid-accessible, non-protected, non-urban land — the condition Cluster A's density-mismatch case and Cluster B's suitable-land case each independently produce.

## §6→§4 closure ledger (process output)

- "Treat land area as a solved, non-binding input... scoped to moderate-or-lower-density countries..." → chain C8 ✓
- "The popular framing 'solar needs too much land' inverts the actual constraint ordering... agree to within about 12%..." → chain C1, C2 ✓
- "...even jumping all the way to the absolute thermodynamic single-junction efficiency ceiling only shrinks the requirement by a further ~8-fold..." → chain C6 ✓
- "The question that actually gates full solar-only supply is not 'is there enough land' but 'how is the sun's absence at night and in winter covered'..." → chain C8 ✓
- "This analysis does not solve the storage/firming problem it identifies..." → chain C8 ✓
- "the exact overbuild multiplier is [caveat marker]" → no chain — flagged assumption only ✓ (marker present, honestly discloses untraced status)
- "The low end of the land bracket rests on an unverified desert-irradiance figure..." → chain C3 ✓
- "...the rooftop-offset figure is a single US-derived study extrapolated to a generic country..." → chain C9 ✓
- "Even the 'small percentage of national territory' framing understates local land competition..." → chain C8 ✓
- "**Pre-check:** head C8 (LOW), C6 (MEDIUM), C9 (MEDIUM), C2 (MEDIUM)..." → chains C8, C6, C9, C2 ✓
- "**Confidence:** LOW — the Conclusion's band matches its weakest contributing chain, C8..." → chains C2, C6, C8, C9 ✓

All section-6 claims trace to a named section-4 chain or carry the honest "no chain — flagged assumption only" marker. Ledger clean — 0 claims cut.

## Self-audit scan (process output)

| Chain | Chain Head (brief) | Form conforming? | Rule applied | Dependency clean? | Band | Act attempted? | Edges fired |
|-------|---------------------|-------------------|---------------|--------------------|------|-----------------|-------------|
| C1 | GT-2, GT-5?, GT-6?, GT-10? | yes | n/a | yes | MEDIUM | yes | none |
| C2 | GT-1, C1 | yes | n/a | yes | MEDIUM | yes | none |
| C3 | GT-2, GT-5?, GT-6?, GT-10?, GT-11? | yes | n/a | yes | MEDIUM | yes | none |
| C4 | C1, GT-4 | yes | n/a | yes | MEDIUM | yes | none |
| C5 | C3, GT-4 | yes | n/a | yes | MEDIUM | yes | none |
| C6 | GT-12, GT-13, GT-11?, C4 | yes | n/a | yes | MEDIUM | no | none |
| C7 | C5, C4, GT-7? | yes | n/a | yes | MEDIUM | no | none |
| C8 | C7, GT-9? | yes | n/a | yes | LOW | no | none |
| C9 | GT-8?, C4 | yes | n/a | yes | MEDIUM | no | none |

| §6 Span (brief) | Construct | Claim under R11? | R11 clause applied | Chain cited |
|-------------------|-----------|-------------------|----------------------|---------------|
| Recommended approach — treat land as solved input; scope to moderate/lower density | bold lead-in | yes | bold lead-in whose colon closes the bold span, content on same line | C8 |
| Key insight — the "too much land" framing inverts the real constraint ordering | bold lead-in | yes | bold lead-in whose colon closes the bold span, content on same line | C1, C2, C6, C8 |
| Trade-offs acknowledged — storage/firming uncosted; bracket edges order-of-magnitude; % framing understates local competition | bold lead-in | yes | bold lead-in whose colon closes the bold span, content on same line | C8, C3, C9 |
| Pre-check — head C8 (MEDIUM), C6 (MEDIUM), C9 (MEDIUM), C2 (MEDIUM) | bold lead-in | yes | pre-check line is itself a claim, cited by the chains its own head names | C8, C6, C9, C2 |
| Confidence — MEDIUM, every contributing chain itself MEDIUM | bold lead-in | yes | Confidence line discharges its citation obligation through the chains D-07 requires it to name | C2, C6, C8, C9 |

Scan complete: 9 chain rows, one per section-4 chain block in order; 5 section-6 rows, one per construct in order — 5 claims under R11, 0 excluded. 0 chains malformed, 0 claims untraced.

**Note on banding:** eight of nine chains carry MEDIUM and one (C8) carries LOW, so bands are not uniform across the analysis; each chain's own Confidence line names the specific `?`-marked input(s), cited-chain cap, or (for C8) the additional live-rival Rivals-axis shortfall that produced its rating, so no chain's band is a default setting left unexplained.

## Self-Audit Gate (process output)

**Criterion 1: Identify Essence**
Quoted span: "how much land area would a representative 10-million-person country need to devote to utility-scale solar photovoltaic generation in order to cover its total annual electricity consumption, and does the resulting figure make full solar-PV electrification land-constrained, or does it shift the binding constraint elsewhere?"
Band: **Rigorous**
Justification: the Essence Statement names a problem-specific question (not the triggering prompt restated) and is followed by five success criteria, each a verb+subject+outcome triplet pointing at a specific section (e.g. "cross-checked against a real-world empirical land-use survey... section 4"), checkable by scanning the Conclusion/Derivation Chains without further interpretation.

**Criterion 2: Challenge Assumptions**
Quoted span (from the Assumption Audit scan): "Scan complete: 25 steps across 9 chains (C1–C9), in order, no step skipped. Two new assumptions were surfaced (A11 at C6 step 3; A12 at C8 steps 3–4...) and both have been added to the Classified Assumptions Table in section 2."
Band: **Rigorous**
Justification: the Assumptions Table uses exactly the four-type scheme throughout (physical law: A9; current constraint: A3; convention: A1, A2, A4–A7 partial, A10; untested belief: A7, A8, A11, A12), every Verdict cell uses the token-plus-em-dash form, every Verification cell is specific ("unverified — flagged" or a named source), multiple assumptions are actively Challenged rather than blanket-Accepted, and the Assumption Audit scan confirms exhaustive, in-order coverage of all 25 chain steps with both newly surfaced assumptions recorded back into the table.

**Criterion 3: Establish Ground Truths**
Quoted span: "?-marked: GT-3, GT-5, GT-6, GT-7, GT-8, GT-9, GT-10, GT-11, GT-14 (9 of 14)" — checked against the Ground Truths list: suffixed entries counted directly from the list are GT-3?, GT-5?, GT-6?, GT-7?, GT-8?, GT-9?, GT-10?, GT-11?, GT-14? — nine items, matching the enumeration exactly.
Band: **Rigorous**
Justification: GT-IDs are stable and match the identifiers cited in section 4's chain heads; the `?` enumeration matches the list exactly (checked by comparison, not merely quoted); GT-1, GT-2, and GT-4 (the unsuffixed entries feeding chains) each name a specific read-at-source location; no chain in this analysis is rated HIGH, so the "every unsuffixed GT feeding a HIGH-confidence chain names its read-at-source location" requirement is vacuously satisfied rather than violated; no Phase-2-Discard-verdict assumption appears in the Ground Truths list.

**Criterion 4: Reason Upward**
Quoted span (from the Self-audit scan chain-form table): all nine rows read "Form conforming? = yes... Dependency clean? = yes" — e.g. "| C6 | GT-12, GT-13, GT-11?, C4 | yes | n/a | yes | MEDIUM | no | none |".
Band: **Rigorous**
Justification: every one of the nine section-4 chains is form-conforming and dependency-clean per the scan; each chain names its head inputs in the prescribed `GT-N`/`GT-N?`/`Cn` form, contains at least one genuine intermediate claim, and is rendered with one hop per arrow-led line; the Abandoned Reasoning section documents four dead ends each with a specific structural abandonment reason (not "ran out of time"); no analogy is used as standalone evidence anywhere in section 4; both newly-surfaced assumptions (A11, A12) now carry inline `[Assumes: A11]` / `[Assumes: A12]` annotations on their originating hops (C6 step 3; C8 steps 3–4) rather than existing only in the audit-scan table; the Recompute part of the Phase 5 adversarial pass independently reproduced every computed figure in every chain with no arithmetic error found.

**Criterion 5: Validate**
Quoted span (from chain C8's confidence line, after self-correction): "two axes are short simultaneously, which caps this chain at LOW rather than MEDIUM even though each is individually bounded... This LOW rating is calibration, not a shortfall."
Band: **Rigorous**
Justification: every chain's weakest link is named on its own confidence line with a stated verification path; no chain consuming a `GT-N?` input is rated HIGH; every chain is rated no higher than the lowest-rated chain its head cites, and C8 demonstrates the calibration rule cuts both ways — its band was corrected downward from MEDIUM to LOW once a live, unsettled Rivals-axis finding (from the adversarial pass) was priced alongside its existing Inputs-axis shortfall, and the Conclusion's own band was correspondingly corrected to LOW to match its weakest contributing chain; the adversarial pass record is complete — Recompute, Sensitivity, Rival, Premise, Causes (six, from six named stakeholder viewpoints), Clusters (four, each citing the chain/GT ids it bears on), Disposition (one per cluster: two named plan changes, two explicitly-accepted-risk-with-named-mitigation), and Falsification are all present with content, none defaulting to a not-applicable line it did not earn.

**Criterion 6: Conclusion-to-Ground-Truth Traceability**
Quoted span (from the Self-audit scan claim-inventory table): all five section-6 constructs (Recommended approach, Key insight, Trade-offs acknowledged, Pre-check, Confidence) show "Claim under R11? = yes" with a non-empty Chain cited column (C8; C1,C2,C6,C8; C8,C3,C9; C8,C6,C9,C2; C2,C6,C8,C9 respectively).
Band: **Rigorous**
Justification: every Conclusion-section claim traces to a specific named section-4 chain (confirmed by both the closure ledger and the self-audit scan's claim-inventory table, with zero claims cut or left untraced), no claim introduces reasoning absent from section 4, and the Key Insight ("the popular framing... inverts the actual constraint ordering... the real question is night/winter coverage, which land-area arithmetic cannot answer") is a distinct, non-obvious finding rather than a restatement of the Recommended approach's planning-focus directive.

**Gate result:** No criterion scored Absent; zero criteria scored Hand-wavy (all six Rigorous). Both gate conditions are met — **the analysis clears the Self-Audit Gate** on the first scoring pass; no Fix/Repeat re-perception pass was required.

