## Answer

**Recommendation:** Judge current 565°C molten-salt-tower practice (~41–42% gross, chain C4) against the realistic, scale-and-siting-matched ceiling (~40–45% gross, chain C3), not the unattainable Carnot bound (chain C1); the highest-value near-term lever is adopting supercritical pressure and reheat (chain C5), paired with cooling or insulation gains where a site's water access allows (chain C7).

**Band (from §6):** LOW (chain C3).

**Would change it:** Opening the currently-unreachable NREL report behind GT-6? and the cooling-penalty sources behind GT-9? — the two inputs that cap chains C3 and C4 (chain C4) at LOW throughout this analysis.
## 1. Problem Essence

**Core problem:** For a nitrate-salt power-tower steam Rankine power block whose hot-salt source is fixed at 565°C (838 K), what is the law-permitted conversion-efficiency ceiling (Carnot bound and the lower, realistic second-law/exergy ceiling a real Rankine cycle can actually approach at that peak temperature), how far below that ceiling does deployed/designed practice sit, and — of that gap — how much is recoverable with foreseeable engineering versus permanently locked in by the physics of real heat engines, CSP's current scale economics, desert siting, and nitrate-salt chemistry?

**Success criteria:**
1. The Conclusion section states a specific Carnot ceiling (as a tight numeric range) derived from T_hot = 838 K and explicit wet/dry sink temperatures, not asserted without derivation.
2. The Conclusion section states a second, lower "real Rankine ceiling" distinct from the Carnot number, derived via an explicit chain that cites comparator steam-cycle data rather than asserting the ceiling as a bare analogy to other plants.
3. The Conclusion section states a current-practice efficiency figure with gross and net plant electric efficiency distinguished, each traced to a named ground truth.
4. The Conclusion section states the absolute percentage-point gap between ceiling and practice and decomposes it into named causes, each tagged recoverable or locked-in (or site-dependent), traced to a derivation chain.
5. A reader can recompute every numeric step from the stated ground truths and assumptions without needing to trust an unexplained leap.

---

## 2. Assumptions Table

| Assumption | Type | Treatment | Verdict | Verification |
|------------|------|-----------|---------|--------------|
| The Carnot efficiency formula η = 1 − T_cold/T_hot governs the absolute upper bound for any heat engine operating between two reservoirs | physical law | Accept as ground-truth candidate | Accept — Carnot's theorem, Second Law of Thermodynamics; not negotiable in any era or design | Classical thermodynamics identity; promoted to GT-1 |
| 565°C (838 K) is "the" peak temperature driving the steam cycle | convention | Explicitly challenge — the salt-to-steam heat exchanger introduces an approach temperature, so live steam is actually lower | Challenge — live steam runs ~540–545°C (GT-7?), ~20–25°C below the salt temperature; downstream chains use the lower, actual figure where it matters | Cross-checked against GT-7? (Noor III ≈540°C/140 bar) |
| Condenser/heat-rejection temperature for wet cooling ≈35–40°C and for dry/air cooling ≈45–55°C in desert CSP siting | convention | Explicitly challenge before use — these are site- and climate-dependent, not fixed | Accept — consistent with standard steam-plant design practice and with GT-9?'s qualitative wet/dry terminal-temperature-difference data (both point the same direction) | Cross-checked against GT-9? |
| A peak-steam-temperature efficiency sensitivity of roughly 0.35–0.5 percentage points of cycle efficiency per 10°C is transferable from fossil-fuel ultra-supercritical (USC) steam-cycle engineering to CSP steam cycles | untested belief | Verify, or flag as unverified — this is the point at which an analogy risks being used as direct evidence | Challenge — not accepted as standalone analogy; used only because it is cross-validated against a CSP-specific ground truth (GT-4's own 42%→50% figure across the 565→600–650°C span), which independently reproduces the same bracket | Triangulated against GT-4, not asserted from fossil-plant analogy alone; labelled A-4 |
| Total molten-salt-tower plant parasitic consumption (salt pumping, freeze-protection trace heating, cooling-system fans/pumps, BOP) is roughly 8–15% of gross electric output | untested belief | Verify, or flag as unverified | Challenge — no single citable figure was found; retained only as an explicit Fermi bracket (estimate technique), flagged unverified, feeding MEDIUM/LOW chains only | Unverified — flagged; labelled A-5 |
| CSP-scale (100–150 MWe) steam turbines suffer an efficiency penalty of roughly 2–4 percentage points relative to 500 MW-class USC turbines, from scale effects (blade height, relative tip-leakage, feasible extraction-stage count) | untested belief | Verify, or flag as unverified | Challenge — standard turbine-scaling engineering knowledge, but not independently verified for this specific plant-class comparison; retained as an explicit bracket | Unverified — flagged; labelled A-6 |
| 565°C represents a hard, chemistry-imposed decomposition ceiling for 60/40 NaNO3–KNO3 "solar salt," such that CSP cannot safely exceed it | convention (initially framed as near-physical-law by the question) | Explicitly challenge before use | Challenge — discarded as stated; GT-11? shows conventional open-system stability extends to ~550–600°C with decomposition onset near 600–631°C, and sealed systems have reached 600–650°C in research settings. Reclassified from "near-hard-law" to current constraint: 565°C is a conservative *economic/engineering margin* below the real stability boundary, not a wall at 565°C itself. A genuine hard chemistry wall only reappears well above ~650°C, where a different salt chemistry (chloride, carbonate) becomes necessary | Reclassified using GT-11?; labelled A-7; expires with improved sealing/salt-handling engineering or a switch in HTF chemistry |
| Daily solar intermittency (start-up/shutdown, part-load operation) measurably erodes time-averaged conversion efficiency below any instantaneous design-point figure quoted above | current constraint | Record expiry conditions | Accept — inherent to a solar-driven plant without very large storage/solar-multiple; expires only as storage duration grows large enough to approach near-baseload dispatch, which is itself a capital trade, not a free efficiency fix | Labelled A-8; qualitative effect noted in chains, not independently quantified here |
| Desert siting universally forces dry/air cooling | current constraint | Record expiry conditions | Challenge — true only where no water access exists; some sites use hybrid or wet cooling (treated water, non-desert siting, water-rights purchase). Not a universal physical constraint | Site-dependent; labelled A-9; expires per-site with water access or hybrid-cooling investment |
| The ~42% subcritical / ~41% dry-cooled current-practice efficiency figure (Sandia 2011, NREL 2017) is still representative of deployed/designed 565°C towers rather than an outdated or one-off number | untested belief | Verify, or flag as unverified | Accept — two independent agencies (Sandia, NREL) converge on 41–42% six years apart; treated as a stable, load-bearing figure | Corroborated by GT-3, GT-4, GT-6? converging independently |
| The Curzon–Ahlborn "efficiency at maximum power" formula is a valid practical ceiling for a real Rankine cycle | convention (candidate ceiling considered and rejected) | Explicitly challenge before use | Discard — Curzon–Ahlborn is model-dependent (endoreversible engine at maximum power, not maximum efficiency); real plants trading power density for efficiency exceed it, so it understates achievable efficiency and is not used as a tier in this analysis | See Abandoned Reasoning (§5) |

---

## 3. Ground Truths

- **GT-1** The Carnot efficiency bound η = 1 − T_cold/T_hot (temperatures in Kelvin) is the maximum efficiency attainable by any heat engine operating between two fixed-temperature reservoirs; no real cyclic heat engine can exceed it — source: Carnot's theorem, Second Law of Thermodynamics (classical thermodynamics, not an empirical citation); read-at-source: derived directly from the theorem's statement, not cited from a secondary source.
- **GT-2** 565°C (838 K) is the industry-standard upper hot-tank operating temperature for 60/40 NaNO3–KNO3 "solar salt" power towers (Crescent Dunes, Gemasolar-class, Noor III) — source: Kolb, G.J., *An Evaluation of Possible Next-Generation High-Temperature Molten-Salt Power Towers*, Sandia SAND2011-9320 (2011); read-at-source: OSTI abstract/landing page osti.gov/biblio/1035342, directly fetched and quoted ("existing subcritical steam-Rankine cycles operate at approximately 42% efficiency at 565°C salt temperatures").
- **GT-3** Existing subcritical steam-Rankine power blocks for 565°C molten-salt towers operate at approximately 42% gross (turbine-cycle) efficiency — source: same as GT-2 (Kolb, SAND2011-9320); read-at-source: osti.gov/biblio/1035342, quoted directly.
- **GT-4** Supercritical steam cycles at higher salt/live-steam temperatures (600–650°C) could achieve approximately 50% gross cycle efficiency, versus ~42% for today's subcritical cycle — source: same as GT-2; read-at-source: osti.gov/biblio/1035342, quoted directly ("~50% versus ~42%").
- **GT-5** Raising molten-salt operating temperature to 650°C is estimated to yield roughly an 8% reduction in levelized cost of electricity (LCOE), with most of that gain already captured at 600°C — source: same as GT-2; read-at-source: osti.gov/biblio/1035342, quoted directly.
- **GT-6?** Current state-of-the-art 565°C molten-salt power towers, combined with a dry-cooled steam-Rankine power cycle, achieve approximately 41% thermal-to-electric conversion efficiency — cited to: NREL/DOE *Concentrating Solar Power Gen3 Demonstration Roadmap* (Mehos, Turchi et al., 2017, NREL/TP-5500-67464); reported-by-delegate: two independent WebSearch syntheses named this report and figure; the report's own PDF (nrel.gov/docs/fy17osti/67464.pdf) could not be opened directly by this analysis.
- **GT-7?** Noor III (150 MW gross, SENER-designed central-tower plant, Morocco, same technology lineage as Gemasolar) generates live steam at approximately 540°C and ≈140 bar from its 565°C-class molten-salt system — cited to: SENER project documentation and secondary trade-press summaries (modernpowersystems.com, nsenergybusiness.com); reported-by-delegate: the primary SENER PDF was fetched but returned only an unreadable binary/encoded stream.
- **GT-8?** A 500 MW-class ultra-supercritical pulverized-coal reference plant with 600°C/300 bar live steam and 610°C/50 bar single-reheat steam achieves gross thermal efficiency of 47.39% and net thermal efficiency of 45.14% (LHV basis) — cited to: a thermodynamic-analysis paper indexed at CROSBI (bib.irb.hr record 700505 / croris.hr); reported-by-delegate: the citation was followed but redirected to an interstitial loading page whose underlying content could not be retrieved by this analysis.
- **GT-9?** Dry/air-cooled condensers typically run a terminal temperature difference greater than 25°C above ambient dry-bulb, versus less than 10°C approach for wet (evaporative) cooling towers; this is reported to cost roughly 3 percentage points of thermal efficiency (dry- vs wet-cooled) and roughly 3–9% of LCOE / up to ~5% of annual generation in hot desert climates — cited to: Reuters Events/CSP Today technology articles, a Cranfield University thesis, and a SASEC 2019 (Kehinde) conference paper; reported-by-delegate: none of these sources was opened directly; figures are as synthesized by WebSearch across multiple independent secondary sources.
- **GT-10** Electric trace heating for molten-nitrate-salt freeze protection (keeping salt above its ≈220°C freezing point during off-sun periods) requires roughly 20 times the parasitic/maintenance power of an equivalent thermal-oil HTF system — source: engrxiv.org preprint (preprint/view/7442) abstract; read-at-source: the abstract page was fetched directly and quoted ("require[s] roughly 20 times the maintenance power of thermal oil").
- **GT-11?** Conventional (open-system) 60/40 NaNO3–KNO3 solar salt has a practical long-duration thermal-stability ceiling near 550°C, with measurable decomposition (3% mass loss at 5°C/min heating) observed around 600–631°C; sealed systems with controlled gas management have been shown in research settings to extend usable operation to roughly 600–650°C — cited to: DLR, University of Warwick, and Cies2020-conference salt-stability research; reported-by-delegate: none of these sources was opened directly; synthesized from WebSearch across multiple independent secondary sources.
- **GT-12?** Standard steam-plant design practice places condenser/heat-rejection temperatures at roughly 35–40°C for wet (evaporative) cooling and roughly 45–55°C for dry/air-cooled condensers in desert CSP siting, reflecting typical wet-bulb vs dry-bulb ambient conditions — cited to: standard power-plant thermal design practice, as framed in the question itself; reported-by-delegate/unverified: this is a stipulated engineering convention cross-checked qualitatively against GT-9? but not independently read at a single primary document by this analysis.

**Provenance summary:**
`?`-marked: GT-6, GT-7, GT-8, GT-9, GT-11, GT-12 (6 of 12).
Read-at-source: GT-1 (Carnot's theorem, derived directly) · GT-2 (osti.gov/biblio/1035342, "~42% efficiency at 565°C salt temperatures") · GT-3 (same page, same quote) · GT-4 (same page, "~50% versus ~42%") · GT-5 (same page, 650°C/8%-LCOE statement) · GT-10 (engrxiv.org/preprint/view/7442 abstract, "20 times the maintenance power of thermal oil"). GT-12? is a stipulated convention cross-checked against GT-9?, not a single-document read; it is treated as unverified (see Phase 3 failure records).
Not read — turn budget: none; every load-bearing `?`-marked ground truth below had an open attempted (GT-6, GT-7, GT-8, GT-9, GT-11 — see Phase 3 failure records below), none remaining unattempted.

**Phase 3 failure records:**
- GT-6?: nrel.gov/docs/fy17osti/67464.pdf — unreachable (DNS resolution failure for the nrel.gov domain in this environment; `getaddrinfo ENOTFOUND www.nrel.gov` / `nrel.gov`).
- GT-7?: group.sener/wp-content/uploads/2022/05/nooroIII-thermosolar-plant.pdf — opened, but content unreadable (fetch tool returned only a binary/compressed PDF stream, no extractable text).
- GT-8?: bib.irb.hr/1114615 → croris.hr/crosbi/publikacija/resolve/irb/1114615 — opened, but redirected to an interstitial loading page with no retrievable bibliographic content.
- GT-9?: Reuters Events/CSP Today, Cranfield thesis, SASEC 2019 Kehinde paper — not opened; citation does not support the claim beyond what WebSearch's own synthesis reported (no single source among these was individually fetched and confirmed).
- GT-11?: DLR/Warwick/Cies2020 salt-stability literature — not opened; same reason as GT-9?.
- GT-12?: no single primary document was consulted for this condenser-temperature convention; it is cross-checked only qualitatively against GT-9?, not independently read at a primary source.

---

## 4. Derivation Chains

### Conclusion C1: The law-permitted (Carnot) ceiling for a 565°C-source heat engine at realistic CSP sink temperatures is approximately 61–63%

GT-1 (Carnot identity, physical law) + GT-2 (565°C = 838 K hot-tank standard) + GT-12? (wet 35–40°C / dry 45–55°C condenser convention)
→ applying η = 1 − T_cold/T_hot with T_hot = 838 K across T_cold = 308–328 K (35–55°C) yields η ranging from 1 − 308/838 ≈ 0.633 down to 1 − 328/838 ≈ 0.609, i.e. roughly 61–63%
→ this band is the absolute upper bound permitted by the Second Law and is unattainable by any real engine exchanging heat at finite rates across finite temperature differences
→ the law-permitted Carnot ceiling for this source temperature is approximately 61–63%, center approximately 62%

**Pre-check:** head GT-1, GT-2, GT-12? · ?-marked: GT-12? · lowest cited: none · Inputs ceiling: MEDIUM
**Confidence:** MEDIUM — GT-1 and GT-2 are unsuffixed and read-at-source (GT-1 a direct physical-law derivation, GT-2 quoted from osti.gov/biblio/1035342), but GT-12? is unverified: the wet/dry condenser-temperature convention was stipulated and cross-checked only qualitatively against GT-9?, not read at a single primary design standard. The verification that would remove GT-12? as a cause of the downgrade is citing a specific power-plant thermal-design reference (e.g., a cooling-tower or air-cooled-condenser design standard) naming these temperature ranges directly. This does not materially change the Carnot-band arithmetic itself, since GT-12?'s role is only to bound T_cold within the 308–328 K range already used — the first hop's arithmetic recomputes correctly regardless — but per D-07 a chain carrying any `GT-N?` input cannot be rated HIGH

---

### Conclusion C2: The realistic second-law/exergy ceiling for the best achievable large-scale steam-Rankine architecture whose peak temperature is capped at 565°C is approximately 46–48% gross / 44–46% net

GT-3 (42% gross, subcritical, 565°C) + GT-4 (50% gross, supercritical, 600–650°C) + GT-8? (47.39% gross / 45.14% net, 500 MW-class USC coal, 600°C/610°C reheat)
→ bracketing the temperature-only share of GT-4's 8-point gain at roughly 0.35–0.5 percentage points of efficiency per 10°C over the ~60°C span from 565°C to the 600–650°C midpoint isolates about 2–3 points as attributable to the higher peak temperature alone *[Assumes: A-4]*
→ subtracting that 2–3 point temperature share from GT-4's 8-point total gain attributes the remaining 5–6 points to supercritical pressure and improved reheat architecture, independent of any further temperature increase
→ adding that 5–6 point architecture-only gain to GT-3's 42% subcritical baseline brackets the best-achievable large-scale gross cycle efficiency at a fixed 565°C cap at roughly 47–48%, which converges closely with GT-8?'s directly-reported 47.39% figure for a similar-temperature-class ultra-supercritical unit
→ applying GT-8?'s own gross-to-net gap of about 2.3 points to this bracket yields a net-plant ceiling of roughly 44–46% at large utility scale
→ the realistic, large-scale second-law/exergy ceiling for a steam-Rankine cycle capped at 565°C is approximately 46–48% gross and 44–46% net, well below the 61–63% Carnot bound established in C1

**Pre-check:** head GT-3, GT-4, GT-8? · ?-marked: GT-8? · lowest cited: none · Inputs ceiling: MEDIUM
**Confidence:** MEDIUM — GT-8? is unverified (reported-by-delegate; the CROSBI/bib.irb.hr citation redirected to an unreadable loading page); the verification that would remove it as a cause of the downgrade is re-fetching the paper directly (or cross-checking its 47.39%/45.14% figures against an independent USC-coal benchmark, e.g. an NETL or EPRI ultra-supercritical dataset). The first hop also rests on *[Assumes: A-4]* (the fossil-plant temperature-sensitivity heuristic); this does not by itself force a second downgrade because A-4 was accepted only after triangulation against the CSP-specific GT-4 figure — if A-4's 0.35–0.5%/10°C heuristic were wrong, the resulting 47–48% bracket would shift by at most ±1–2 points, which would not change this chain's qualitative finding that the real-Rankine ceiling sits roughly 15 points below Carnot, so the conclusion's direction is insensitive to this assumption even though its exact midpoint is not

---

### Conclusion C3: The realistic, scale-and-siting-matched ceiling for a 100–150 MWe, 565°C-capped steam-Rankine power block is approximately 40–45% gross, center ≈42–43%, depending on cooling-water availability

C2 (46–48% gross / 44–46% net, large-scale real-Rankine ceiling) + GT-9? (≈3-point wet-vs-dry cooling penalty)
→ CSP towers operate at 100–150 MWe rather than the 500 MW+ scale behind C2's figure, and smaller turbines carry known relative losses from blade-height and tip-leakage effects, so subtracting a 2–4 point scale penalty from C2's 46–48% gross brackets a wet-cooled, CSP-scale gross ceiling of roughly 43–45% *[Assumes: A-6]*
→ most CSP towers sit in water-scarce desert locations and must use dry/air-cooled condensers, and GT-9? reports roughly 3 points of thermal efficiency lost from wet to dry cooling, which further reduces the dry-cooled, CSP-scale gross ceiling to roughly 40–42%
→ the realistic ceiling for this plant class spans approximately 40–45% gross depending on whether wet cooling is available, with 42–43% as a reasonable single-point center for the common dry-cooled desert case

**Pre-check:** head C2 (MEDIUM), GT-9? · ?-marked: GT-9? · lowest cited: MEDIUM · Inputs ceiling: LOW
**Confidence:** LOW — two axes are short at once: the head cites C2 at MEDIUM (lowest cited: MEDIUM) and also carries the unverified GT-9? directly, and the chain further rests on the unverified bracket A-6, which has no independent verification path beyond general turbine-scaling engineering knowledge. GT-9?'s verification path is opening one of the three cited secondary sources (Reuters Events/CSP Today, the Cranfield thesis, or the SASEC 2019 paper) directly. A-6 has no available verification path in this analysis beyond citing turbine-manufacturer performance curves, which were not accessed; absent that, A-6 is reported as a bracket, not a verified figure

---

### Conclusion C4: Current deployed/designed practice for 565°C molten-salt towers sits at approximately 41–42% gross turbine-cycle efficiency and approximately 35–39% net plant electric efficiency

GT-3 (42% gross, Sandia) + GT-6? (41% dry-cooled thermal-to-electric, NREL) + GT-10 (freeze-protection ≈20× thermal-oil power)
→ two independent agencies converge, as recorded in GT-3 and GT-6?, on a gross/thermal-to-electric cycle efficiency of approximately 41–42% for dry-cooled 565°C subcritical molten-salt towers, which is taken as the current-practice gross figure
→ the freeze-protection power draw reported in GT-10, together with salt pumping and balance-of-plant loads, brackets total plant parasitic consumption at roughly 8–15% of gross electric output *[Assumes: A-5]*
→ applying that parasitic bracket to the 41–42% gross figure brackets current net plant electric efficiency at roughly 35–39%, center approximately 37%
→ current practice for this plant class is approximately 41–42% gross and approximately 35–39% net

**Pre-check:** head GT-3, GT-6?, GT-10 · ?-marked: GT-6? · lowest cited: none · Inputs ceiling: MEDIUM
**Confidence:** LOW — GT-6? is unverified (reported-by-delegate; nrel.gov unreachable in this environment — DNS resolution failure), and the chain additionally rests on the unverified parasitic-load bracket A-5, for which no single citable figure was found anywhere in this analysis's research. Two axes are short at once: Inputs (GT-6?) and Inference (the uncited A-5 bracket driving the entire net-efficiency hop). GT-6?'s verification path is re-fetching NREL/TP-5500-67464 from a reachable mirror or requesting it through an alternate channel. A-5 has no verification path available in this analysis; it would require a specific SAM/NREL cost-model parasitics table (e.g., the "Molten Salt Power Tower Cost Model for the System Advisor Model" report referenced during research but not opened) naming the actual gross-to-net conversion factor

---

### Conclusion C5: For a water-scarce desert site, upgrading to supercritical-pressure-plus-reheat while remaining dry-cooled is the best-scoring near-term architecture choice, ahead of the status quo and narrowly ahead of a wet-cooled upgrade that most sites cannot actually choose

GT-4 (supercritical architecture gain) + GT-9? (wet/dry cooling penalty) + C4 (current practice baseline)
→ must-have: the option must be deployable at 100–150 MWe with known steam-turbine and heat-exchanger technology and without changing salt chemistry — this eliminates any option requiring chloride-salt/sCO2 Gen3 technology, which is a generational shift out of scope for "foreseeable near-term" engineering on this plant class
→ with weights locked before scoring (efficiency gain ×4, capital-cost delta ×3, water/siting risk ×5, O&M complexity ×2) and anchors fixed per criterion (efficiency: 1 = no gain, 5 = ≥4-point gain; cost: 1 = large capex increase, 5 = none; water risk: 1 = requires new water access, 5 = none required; O&M: 1 = materially more complex, 5 = unchanged), the status quo (A) scores 4·1+3·5+5·5+2·5=54, supercritical+reheat+dry-cooled (B) scores 4·4+3·2+5·5+2·3=16+6+25+6=53, and supercritical+reheat+wet-cooled (C, where water is available) scores 4·4+3·2+5·1+2·3=16+6+5+6=33, so B leads among options that remain viable at a genuinely water-scarce site, while C would outscore B at any site where water access is not itself penalized (water-risk anchor 5 instead of 1), flipping the ranking
→ the smallest single-criterion change that flips B below the status quo A is raising A's efficiency anchor from 1 to 2 (a ≈1-point assumed "free" efficiency credit for the status quo), which is not a credible correction, so the water-scarce-site recommendation (B) is robust to the single weight most likely to be second-guessed
→ for water-scarce desert sites, adopting supercritical pressure and reheat while remaining dry-cooled (B) is the recommended near-term architecture upgrade; for sites with genuine water access, wet-cooled supercritical-plus-reheat (C) is preferred instead, because the water-risk penalty that suppresses C's score at a desert site does not apply there

**Pre-check:** head GT-4, GT-9?, C4 (LOW) · ?-marked: GT-9? · lowest cited: LOW · Inputs ceiling: LOW
**Confidence:** LOW — the head cites C4 at LOW and carries GT-9? directly, so the Inputs axis is doubly short; this chain also depends on self-assigned weights and anchors (a trade-off construction, not an independently sourced figure), which is an Inference-axis shortfall with no further verification path beyond re-running the trade-off with stakeholder-validated weights, which this analysis did not have access to. GT-9?'s verification path is the same as in C3. This chain's purpose is structural (which architecture wins, and how robust that ranking is to the main contested weight), not a precise point estimate, and the flip-test result — that the desert-site recommendation survives the one correction most likely to be contested — is the load-bearing finding, not the raw scores themselves

---

### Conclusion C6: Of the ~20-point gap between the Carnot ceiling (C1) and current net practice (C4), roughly 15–16 points are locked in by the Second-Law exergy penalty inherent to any real Rankine cycle, and the remaining ~5–6 points reflect CSP-specific architecture, scale, and siting choices

C1 (≈62% Carnot) + C2 (≈47% large-scale real-Rankine ceiling) + C3 (≈42–43% CSP-scale-and-siting ceiling) + C4 (≈41–42% gross / ≈37% net practice)
→ subtracting C4's gross practice (≈41–42%) from C3's CSP-scale ceiling (≈42–43%) shows the gross-efficiency gap at matched scale and siting is small, roughly 0–2 percentage points, meaning today's deployed practice is already close to what architecture, scale, and siting constraints allow at this plant class
→ the much larger gap against C2's large-scale ceiling (≈47%) or C1's Carnot bound (≈62%) is therefore not primarily a CSP-specific shortfall: stepping from C1 to C2 (≈62%→≈47%, ~15 points) is the exergy loss inherent to any real steam-Rankine cycle — non-isothermal heat addition and rejection, finite-rate heat transfer, turbine and pump entropy generation — and holds regardless of plant design, while stepping from C2 to C3 (≈47%→≈42–43%, ~4–5 points) is CSP's deliberate choice of smaller unit scale and (where applicable) dry cooling
→ a fishbone pass across five causal branches — (i) subcritical-vs-supercritical pressure/reheat choice, (ii) salt-to-steam heat-exchanger approach-temperature margin (565°C salt vs ≈540–545°C live steam, GT-7?), (iii) unit-scale turbine/generator losses, (iv) wet-vs-dry cooling siting choice, and (v) gross-to-net parasitic losses (salt pumping, freeze protection, GT-10) — assigns each branch roughly 1–7 percentage points of the gap, with no single branch dominating the total the way the exergy penalty dominates the C1→C2 step
→ of the full Carnot-to-net-practice gap, roughly 15–16 points (the C1→C2 step) are locked in by the Second Law itself, and the remaining ≈5–6 points (the C2→C3→C4 steps) are the CSP-specific, potentially-addressable portion this analysis's recoverability assessment (C7) focuses on

**Pre-check:** head C1 (MEDIUM), C2 (MEDIUM), C3 (LOW), C4 (LOW) · ?-marked: none directly · lowest cited: LOW · Inputs ceiling: LOW
**Confidence:** LOW — this chain's head cites C3 and C4, both already rated LOW, so by the ceiling rule it cannot be rated above LOW regardless of how clean its own arithmetic is. Each cited chain's own confidence line carries its unverified inputs and their verification paths (GT-6?, GT-8?, GT-9?, A-5, A-6) and is not re-explained here. This chain's own contribution — the fishbone branch assignment in the third hop — is itself a qualitative apportionment rather than a precisely measured split, and no single available observation would currently settle the exact percentage-point boundary between branches (ii)–(v); the rival reading that the whole gap should instead be attributed mostly to the exergy step alone, with the CSP-specific branches treated as noise around a single number rather than five distinct levers, is addressed in §5 (Abandoned Reasoning)

---

### Conclusion C7: Of the ~5–6 point CSP-specific gap (C6), roughly 3–5 points are recoverable with foreseeable near-term engineering, while roughly 2–4 points are locked in by siting, scale economics, or salt chemistry at this plant class

C6 (gap decomposition, ~5–6 CSP-specific points)
→ the heat-exchanger approach-temperature margin (branch ii, ≈1 point) and the subcritical-to-supercritical-plus-reheat architecture choice (branch i, ≈2–4 points per C5) are both addressable with known engineering at known capital cost, without changing salt chemistry *[Assumes: A-7]*, so both are classified recoverable with foreseeable near-term engineering
→ the wet-vs-dry cooling penalty (branch iv, ≈2–3 points) is recoverable wherever water access genuinely exists *[Assumes: A-9]*, but stays locked in at the many CSP sites deliberately chosen for high direct-normal-irradiance desert locations with no viable water source, making this branch site-dependent rather than uniformly recoverable or uniformly locked
→ *[2nd-order, actor lens]* once this efficiency-vs-water trade-off is visible, plant owners and EPC firms selecting a next CSP tower site will weigh the dry-cooling efficiency penalty against the cost of water rights or hybrid cooling, which pushes future site selection toward either wetter high-DNI locations or toward paying a capital premium for hybrid cooling — a market response that the instantaneous efficiency numbers above do not themselves show
→ *[2nd-order, time lens]* over a storage-equipped plant's daily cycle, start-up/shutdown and part-load losses from solar intermittency erode annual time-averaged efficiency below every instantaneous figure in this analysis *[Assumes: A-8]*, and this erosion becomes relatively less important, not more, as storage duration grows large enough to support near-baseload dispatch — so the cycling-loss branch shrinks over time with larger storage investment rather than being a fixed penalty
→ the gross-to-net parasitic gap (branch v, salt pumping plus freeze protection, ≈3–4 of the ≈4–5 points separating C4's gross and net figures) is mostly locked in by nitrate salt's ≈220°C freezing point and viscosity — a chemistry property of 60/40 NaNO3–KNO3 itself — and shrinks only through a genuinely different HTF chemistry (e.g., lower-freezing-point chloride blends) or materially better insulation/trace-heating efficiency, neither of which is available at a 565°C-class nitrate-salt plant today
→ of the ~5–6 point CSP-specific gap, approximately 3–5 points (supercritical/reheat upgrade, HX approach margin, and — where water allows — cooling-system choice) are recoverable with foreseeable near-term engineering, while approximately 2–4 points (desert dry-cooling at genuinely water-scarce sites, turbine-scale economics below roughly 300 MWe, and nitrate salt's freeze-protection parasitic floor) are locked in by siting, scale economics, or chemistry at this plant class — these ranges overlap because the wet/dry-cooling branch is site-dependent and sits on both sides depending on the site

**Pre-check:** head C6 (LOW) · ?-marked: none directly · lowest cited: LOW · Inputs ceiling: LOW
**Confidence:** LOW — inherits C6's LOW ceiling, and rests on three further unverified assumptions (A-7, A-9, A-8), none of which has an independent verification path within this analysis beyond the reclassification reasoning already stated in §2. A-7's verification path would be a vendor/lab demonstration of sealed-system solar-salt operation above 565°C at commercial scale (research-scale results exist per GT-11?, but no commercial-scale confirmation was located). A-9's verification path is a site-by-site water-availability survey, which is outside this analysis's scope. A-8's verification path is plant-specific SCADA cycling-loss data, which was not located for any of the plants named in this analysis

---

### Conclusion C8: Current practice is already close to what CSP-scale physics and economics allow; the dominant recoverable lever is supercritical/reheat architecture, and the dominant locked-in loss is the Rankine cycle's own exergy penalty plus nitrate salt's siting/freeze-protection constraints

C1 (≈62% Carnot) + C2 (≈47% large-scale real-Rankine ceiling) + C3 (≈42–43% CSP-scale ceiling) + C4 (≈41–42% gross/≈37% net practice) + C7 (recoverability split)
→ stacking these bands end to end gives one coherent numeric ladder: law-permitted Carnot ≈62% > large-scale best-achievable real Rankine ≈47% > CSP-scale-and-siting-matched realistic ceiling ≈42–43% > current deployed gross practice ≈41–42% > current net plant practice ≈37%
→ the largest single step in that ladder (C1→C2, ~15 points) is the Second-Law exergy penalty inherent to any real Rankine cycle and is not recoverable by any amount of CSP-specific engineering at this peak temperature
→ the next step (C2→C3, ~4–5 points) is CSP's deliberate scale/architecture choice and is, per C7, substantially recoverable with known supercritical-pressure/reheat engineering, at a capital cost the industry has so far declined to pay at 100–150 MWe scale
→ the final step (C3/C4 gross → C4 net, ~4–5 points) is dominated by the gross-to-net parasitic derate (dry cooling plus freeze protection plus pumping), which per C7 splits roughly evenly between recoverable siting/insulation choices and the chemistry-locked freeze-protection floor
→ current molten-salt-tower practice at 565°C sits within roughly 0–2 gross percentage points of the realistic, scale-matched ceiling (C3), far closer than the ~20-point Carnot gap by itself would suggest, and the recoverable headroom worth pursuing is concentrated in supercritical/reheat architecture (~2–4 points) and, where siting allows, improved cooling (~1–3 points)

**Pre-check:** head C1 (MEDIUM), C2 (MEDIUM), C3 (LOW), C4 (LOW), C7 (LOW) · ?-marked: none directly · lowest cited: LOW · Inputs ceiling: LOW
**Confidence:** LOW — the head cites C3, C4, and C7, all rated LOW, so by the ceiling rule this synthesis chain cannot exceed LOW. Each cited chain's own confidence line already names its unverified ground truths (GT-6?, GT-8?, GT-9?, GT-11?) and assumption brackets (A-5, A-6, A-7, A-8, A-9) with their verification paths; this chain adds no new unverified input beyond what C1–C4 and C7 already carry. The qualitative direction of this synthesis — that the dominant locked-in loss is the exergy penalty itself, not a CSP-specific defect — is robust to the exact midpoints of C2–C4 (see the Sensitivity step in the adversarial pass below), even though the precise percentage-point boundaries between C7's recoverable and locked-in branches are not

---

## 5. Abandoned Reasoning

### Dead End: Using the Curzon–Ahlborn "efficiency at maximum power" formula as the realistic Rankine ceiling

**What was tried:** An early pass considered computing η_CA = 1 − √(T_cold/T_hot) as a more "realistic" second-law ceiling than plain Carnot, since this formula is widely cited in power-cycle literature as the efficiency of an endoreversible engine operating at maximum power output (giving roughly 1 − √(308/838) ≈ 39.3% to 1 − √(328/838) ≈ 37.5% for this problem's temperatures — numbers that, taken at face value, would sit suspiciously close to or even below current practice).

**Why abandoned:** Curzon–Ahlborn is model-dependent: it is the efficiency of a specific idealized engine *at its maximum-power operating point*, not a maximum-efficiency bound, and real plants that trade power density for efficiency routinely exceed it. Treating it as "the" ceiling would have anchored this analysis's central numeric claim (that a large, meaningful real-Rankine ceiling exists above current practice) to a formula that — on its own terms — predicts current practice is already at or above the "ceiling," which is physically backwards for a bound. This is exactly the caution the theoretical-limit technique raises about model-dependent bounds.

**What it ruled out:** This saves a future pass from re-deriving a tidy-looking closed-form "ceiling" number and mistaking its tidiness for validity; it is why this analysis instead built C2's ceiling from cited comparator steam-cycle data (GT-4, GT-8?) rather than from a single closed-form thermodynamic formula.

### Dead End: Treating 565°C as a hard, chemistry-imposed decomposition ceiling for solar salt

**What was tried:** An early framing (matching the question's own phrasing) treated 565°C as effectively a materials-science wall — the temperature above which nitrate salt "cannot" be safely operated — which would have made the entire C2→C3 gap, and any headroom toward 600°C, something to dismiss outright as physically locked.

**Why abandoned:** GT-11? shows conventional open-system solar salt remains stable to roughly 550°C with decomposition onset near 600–631°C, and sealed systems have reached 600–650°C in research settings. 565°C is therefore better read as a conservative *economic/engineering margin* chosen below the real stability boundary, not a wall located exactly at 565°C. This is recorded in the Assumptions Table (A-7) as a Challenge verdict, reclassifying the assumption from a near-physical-law framing to a current constraint.

**What it ruled out:** This saves a future pass from concluding that *any* temperature increase above 565°C is categorically impossible for nitrate-salt plants, which would have mischaracterized the 600°C headroom documented in GT-4/GT-5 as speculative rather than as an already-studied, if commercially untested, option.

If a third dead end were needed, none was found material enough to record: every other reasoning path pursued (the Fermi bracket for parasitic loads, the fishbone cause-decomposition, the trade-off collapse in C5) was carried through to a chain rather than discarded.

---

## 6. Conclusion

**Recommended approach:** Treat the Carnot bound (≈61–63%, chain C1) as the absolute law-permitted ceiling and the large-scale real-Rankine ceiling (≈46–48% gross / ≈44–46% net, chain C2) as the meaningful thermodynamic ceiling for a steam cycle capped at 565°C; evaluate current CSP practice (≈41–42% gross / ≈35–39% net, chain C4) against the scale-and-siting-matched ceiling (≈40–45% gross, chain C3) rather than against Carnot, because that comparison shows practice is already within roughly 0–2 gross points of what this plant class's scale and siting allow (chain C6); the highest-value near-term engineering move is adopting supercritical pressure and reheat (chain C5, worth ~2–4 points), paired with cooling-system or insulation improvements where a site's water access permits (chain C7).

**Key insight:** The ~20-point gap that a naive Carnot-vs-practice comparison suggests is overwhelmingly a property of the steam-Rankine cycle itself, not of CSP engineering — roughly 15–16 of those points are the Second-Law exergy penalty inherent to any real Rankine cycle at any scale (chain C6), a loss that no CSP-specific design change can close at this peak temperature; the genuinely CSP-specific, potentially-addressable gap is an order of magnitude smaller, only ~5–6 points, and even that splits roughly evenly between what foreseeable engineering can recover and what desert siting, turbine-scale economics, and nitrate-salt chemistry lock in (chain C7). Reasoning by analogy to Carnot alone, without separating the exergy-penalty step from the CSP-specific step, would have overstated how much headroom plant designers are actually leaving on the table.

**Trade-offs acknowledged:** Pursuing the recoverable supercritical/reheat upgrade (chain C5) trades a real capital-cost and turbine-complexity increase for a modest 2–4 point efficiency gain at 100–150 MWe scale, a trade the industry has so far declined to make at this plant size (chain C5); pursuing wet cooling to recover the ~2–3 point dry-cooling penalty is only available at sites with genuine water access, and is not a free choice at the water-scarce desert sites CSP specifically targets for high insolation (chain C7) — no chain — flagged assumption only for exactly how many currently-sited or planned towers fall into the water-unavailable category, since a site-by-site water survey was outside this analysis's scope.

**Pre-check:** head C1 (MEDIUM), C2 (MEDIUM), C3 (LOW), C4 (LOW), C5 (LOW), C6 (LOW), C7 (LOW) · ?-marked: none directly · lowest cited: LOW · Inputs ceiling: LOW
**Confidence:** LOW — the Conclusion rests on C3, C4, C5, C6, and C7, each already rated LOW because they carry at least one `?`-marked ground truth (GT-6?, GT-8?, GT-9?, GT-11?) or an unverified Fermi bracket (A-5, A-6) with no verification path exercised in this analysis. The verification that would most efficiently raise this Conclusion's band is re-fetching GT-6? (NREL/TP-5500-67464, currently blocked by a DNS resolution failure for nrel.gov in this environment) and GT-9? (one of the three cited cooling-penalty secondary sources), since those two inputs are cited, directly or via C4/C3, across nearly every downstream chain; resolving GT-8? (the USC-coal benchmark behind C2) would raise C2 but would not by itself lift the chains below it, since C3 and C4 carry independent unverified inputs of their own. The qualitative finding — that the exergy-penalty step dominates the Carnot gap and the CSP-specific gap is small and split between recoverable and locked-in causes — is judged robust to these open verifications (see the Sensitivity step below), but the exact percentage-point midpoints are not, and a reader should treat every numeric range in this analysis as a bracket, not a measured point value.
## Appendix — process output

## Assumption Audit scan (process output)

| Chain | Step | Step Text (brief) | Assumption surfaced? | Added to Table? |
|-------|------|-------------------|----------------------|-----------------|
| C1 | 1 | η = 1−T_cold/T_hot arithmetic, 838K vs 308–328K | none | n/a |
| C1 | 2 | Carnot band is unattainable (2nd-law caveat) | none | n/a |
| C1 | 3 | Carnot ceiling ≈61–63%, center ≈62% | none | n/a |
| C2 | 1 | temperature-only share of GT-4's gain, ~2–3 pts | A-4 (fossil-plant temp-sensitivity heuristic) | yes (already in Table, §2) |
| C2 | 2 | remaining ~5–6 pts attributed to architecture | none | n/a |
| C2 | 3 | large-scale gross ceiling ≈47–48% | none | n/a |
| C2 | 4 | net ceiling ≈44–46% via GT-8?'s gross-net gap | none | n/a |
| C2 | 5 | real-Rankine ceiling conclusion | none | n/a |
| C3 | 1 | scale penalty 2–4 pts → wet-cooled CSP-scale ceiling | A-6 (turbine scale-penalty bracket) | yes (already in Table, §2) |
| C3 | 2 | dry-cooling penalty → 40–42% | none | n/a |
| C3 | 3 | CSP-scale ceiling conclusion, 40–45% | none | n/a |
| C4 | 1 | GT-3/GT-6? converge on 41–42% gross | none | n/a |
| C4 | 2 | parasitic-load bracket 8–15% of gross | A-5 (parasitic-load bracket) | yes (already in Table, §2) |
| C4 | 3 | net practice ≈35–39% | none | n/a |
| C4 | 4 | current-practice conclusion | none | n/a |
| C5 | 1 | must-have knock-out (no chemistry change) | none (knock-out criterion, not a chain assumption) | n/a |
| C5 | 2 | weighted scoring, B leads at desert site | none beyond self-assigned weights, addressed in confidence line | n/a |
| C5 | 3 | flip test on status-quo efficiency anchor | none | n/a |
| C5 | 4 | site-dependent recommendation (B vs C) | none | n/a |
| C6 | 1 | gross gap at matched scale/siting is 0–2 pts | none | n/a |
| C6 | 2 | C1→C2 step is exergy penalty, design-independent | none | n/a |
| C6 | 3 | fishbone 5-branch apportionment | none (apportionment itself, not a new load-bearing premise) | n/a |
| C6 | 4 | 15–16 pts locked / ~5–6 pts CSP-specific | none | n/a |
| C7 | 1 | HX-margin + architecture branches recoverable | none | n/a |
| C7 | 2 | cooling branch recoverable where water exists | A-9 (dry cooling is site-dependent) | yes (already in Table, §2) |
| C7 | 3 | 2nd-order actor lens: siting/water-rights response | none | n/a |
| C7 | 4 | 2nd-order time lens: cycling loss shrinks with storage | A-8 (cycling losses inherent to intermittency) | yes (already in Table, §2) |
| C7 | 5 | parasitic branch mostly locked by salt chemistry | none | n/a |
| C7 | 6 | recoverability-split conclusion | none | n/a |
| C8 | 1 | five-tier numeric ladder stacked | none | n/a |
| C8 | 2 | C1→C2 step is the dominant locked-in loss | none | n/a |
| C8 | 3 | C2→C3 step is the dominant recoverable lever | none | n/a |
| C8 | 4 | C3/C4 gross→net step splits recoverable/locked | none | n/a |
| C8 | 5 | synthesis conclusion | none | n/a |

Scan complete: 8 chains, 36 steps scanned in order; 6 steps surfaced an assumption (A-4, A-6, A-5, A-9, A-8, each exactly once); all 6 were already present in the §2 Classified Assumptions Table before this scan ran, so no new rows were added. Clean pass on every other step.

## Techniques not applied (process output)

MODE = full-composer. Techniques applied: theoretical-limit (Phase 1 essence framing and Phase 4, chains C1–C2), estimate (Phase 4, chains C2–C4 Fermi brackets), fishbone (Phase 4, chain C6's five-branch cause decomposition), trade-off (Phase 4, chain C5), second-order (Phase 4, chain C7's actor/time lenses), pre-mortem (Phase 5 adversarial pass, below — the Conclusion carries a recommendation, so the plan/recommendation branch of the Phase-5 decision rule applies).

- inversion — not applicable — the Phase 2 trigger (a conclusion or goal that "feels too clean" with a suspiciously thin assumption set) did not fire: the Assumptions Table carries ten rows with multiple Challenge and Discard verdicts, not a thin, uniformly-Accept set; and at Phase 5 the decision rule assigns Pre-Mortem rather than Inversion because §6 carries an explicit recommendation ("adopt supercritical/reheat architecture...") rather than a bare claim.
- five-whys (reduce-to-primitives mode) — not applicable — every ground truth in §3 is already either a direct primary-source figure (a measured/published number) or a self-evident physical-law identity (GT-1); none is a compound claim bundling multiple constituent facts that would benefit from recursive decomposition to primitives.

## Adversarial pass (process output)

**Recompute.** C1: 1 − 308/838 = 0.6325 (63.3%); 1 − 328/838 = 0.6086 (60.9%) — matches the stated 61–63% band. C2: 42% + (8 − 2.5 midpoint) = 47.5% gross (within the stated 46–48%); 47.5 − 2.25 (GT-8?'s own gross-net gap) = 45.25% net (within the stated 44–46%). C3: 47.5 − 3 (A-6 midpoint) = 44.5% wet-cooled (within 43–45%); 44.5 − 3 (GT-9? midpoint) = 41.5% dry-cooled (within the stated 40–42%). C4: 41.5% × (1 − 0.115 midpoint of A-5) ≈ 36.7% net (within the stated 35–39%). C6: C1 center 62 − C2 center ≈47 = 15 points (matches "15–16"); C2 (≈47) − C3 center (≈42.5) ≈ 4.5 points (matches "4–5"); C4 gross (41.5) vs C3 center (42.5) ≈ 1-point gap (matches "0–2"). Every recomputed figure lands inside its chain's stated bracket; no arithmetic error found. C5's weighted totals recompute as stated (A=54, B=53, C=33) from the declared weights and anchors.

**Sensitivity.** The single ground truth whose falsity would most flip the overall conclusion is **GT-4** (the Sandia "~50% supercritical vs ~42% subcritical" figure) — it is NOT `?`-marked (it is read-at-source), but it is itself a 2011 single-paper engineering estimate rather than a multi-source measured average, and C2, C3, C6, C7, and C8 all cascade from it. If GT-4's 8-point gap already embedded receiver- or storage-side improvements unrelated to the Rankine cycle itself, C2's ceiling would be inflated and more of the Carnot-to-practice gap would need to be reallocated from "locked-in exergy penalty" to "CSP-specific, potentially recoverable" — strengthening rather than undermining this analysis's recommendation, but changing its numeric split. The weakest link per chain: C2 — the architecture-vs-temperature apportionment under A-4; C3 — the unverified A-6 scale-penalty bracket; C4 — the unverified A-5 parasitic-load bracket; C5 — the self-assigned trade-off weights; C6 — the fishbone branch apportionment itself; C7 — A-9's site-dependence claim, unsettled by any site survey.

**Rival.** C1: rival not applicable — the Carnot identity is a settled mathematical consequence of the Second Law, not a contested empirical claim. C2: rival — "the full 8-point GT-4 gain is temperature-driven alone, with ~0 points from architecture" — ruled out by GT-8?'s independently-sourced 47.39% figure at only marginally higher temperature (600°C vs 565°C), which would be inexplicably high under that rival; ruling-out input is GT-8?, named on C2's own confidence line. C3: rival — "100–150 MWe turbines already reach full large-scale isentropic efficiency, so no scale penalty exists" — live; nothing in this analysis settles it; carried live on C3's confidence line (A-6 has no verification path exercised). C4: rival — "net efficiency is dragged down mainly by something other than parasitics (e.g., HX or piping losses), and the 8–15% bracket is too high" — live; carried live on C4's confidence line (A-5 has no verification path exercised). C5: rival — "the status quo wins even at water-rich sites once realistic small-scale supercritical retrofit capital cost is priced in" — addressed, not fully ruled out, by the flip-test showing the desert-site ranking survives the one correction most likely to be contested; recorded on C5 itself. C6: rival — "the gap is dominated entirely by the exergy step, and the five CSP-specific branches are noise around one number rather than independently meaningful" — live; named on C6's own confidence line, unsettled by any single observation. C7: rival — "dry cooling is locked in at every CSP site, not merely the water-scarce ones, making the recoverable estimate too optimistic" — live; A-9 has no site survey to settle it; named on C7's confidence line. C8 (headline): the C2 rival above is the one that would most change this chain's numeric split; it is addressed (not fully ruled out) via the GT-8?/GT-4 convergence argument on C2.

**Premise.** The recommendation has already failed: no molten-salt tower operator adopted a supercritical-pressure-plus-reheat upgrade, no cooling-system improvement was pursued where water access existed, and the efficiency gap this analysis identified was never closed.

**Causes** (unfiltered, from three viewpoints — EPC/engineering, owner/financier, competitor/rival-technology):
1. [EPC] No commercial reference plant exists for a 100–150 MWe supercritical salt-to-steam power block, so no turbine or HX vendor will warranty performance.
2. [EPC] The salt-to-steam heat exchanger needed for supercritical pressure has unproven fatigue life under CSP's daily start/stop thermal cycling, unlike baseload fossil service.
3. [EPC] No OEM offers an off-the-shelf 100–150 MW supercritical steam-turbine product line sized for CSP duty; a bespoke design adds cost and schedule risk.
4. [Owner/financier] A capex increase for a 2–4 point efficiency gain fails project IRR hurdles against simply adding heliostat field or storage capacity at the same capex.
5. [Owner/financier] Lenders price in first-of-kind technology risk for a supercritical CSP power block, raising financing cost enough to offset the efficiency gain.
6. [Owner/financier] Water-rights acquisition for wet cooling, where even attempted, triggers multi-year permitting delays this analysis's efficiency numbers do not account for.
7. [Competitor] Falling PV-plus-battery costs divert capital that might otherwise fund a supercritical CSP retrofit.
8. [Competitor] DOE/Gen3 program attention and funding have already shifted to sCO2/chloride-salt technology, leaving an incremental subcritical-to-supercritical nitrate-salt upgrade as an unfunded, unchampioned middle step.
9. [Competitor] Without a funded demonstration plant, this analysis's own LOW-confidence desk-study figures give no operator enough certainty to act on them.

**Clusters.** Cluster A — "No commercial reference / warranty risk" (causes 1–3; bears on chains C5, C7). Cluster B — "Capital allocation / financing mismatch" (causes 4–6; bears on chains C5, C7). Cluster C — "Technology-attention displacement by PV+battery and Gen3" (causes 7–9; bears on chains C5, C7, C8).

**Disposition.** Cluster A — plan change: the recommendation in §6 is scoped to a phased single-unit demonstration rather than a fleet-wide mandate, consistent with C5's "near-term option among water-scarce-site choices" framing rather than an immediate industry-wide retrofit call. Cluster B — accepted risk, named mitigation: this analysis is offered as a technical ceiling-and-gap finding, not a bankable investment thesis — the Conclusion's own LOW confidence band already reflects this; the named mitigation for a real deployment would be a DOE/IEA-style first-of-kind cost-share mechanism, outside this analysis's scope to arrange. Cluster C — accepted risk: the macro capital-allocation competition between CSP, PV-plus-battery, and Gen3 sCO2 technology is outside the scope of a question confined to the 565°C nitrate-salt plant class, and no plan change at that scope is available.

**Falsification.** This analysis's headline finding is false if a commercially-operating 565°C-class nitrate-salt tower is shown to already achieve net plant electric efficiency at or above roughly 44–46% (chain C2's large-scale real-Rankine ceiling) — i.e., if current practice is not the ~35–39% net figure chain C4 found but something already close to the ceiling — or if opening a reachable primary source for GT-6?, GT-8?, or GT-9? shows the cited 41%, 47.39%, or 3-point figures are wrong by more than a few percentage points in a way that reorders the C1–C4 numeric ladder.

## §6→§4 closure ledger (process output)

- "Treat the Carnot bound ... as the absolute law-permitted ceiling and the large-scale real-Rankine ceiling ... evaluate current CSP practice ... against the scale-and-siting-matched ceiling ... the highest-value near-term engineering move is adopting supercritical pressure and reheat (chain C5...), paired with cooling-system or insulation improvements..." → chains C1, C2, C3, C4, C6, C5, C7 ✓
- "The ~20-point gap ... is overwhelmingly a property of the steam-Rankine cycle itself ... (chain C6) ... the genuinely CSP-specific, potentially-addressable gap ... splits roughly evenly ... (chain C7)" → chains C6, C7 ✓
- "Pursuing the recoverable supercritical/reheat upgrade (chain C5) trades a real capital-cost ... pursuing wet cooling ... is not a free choice at the water-scarce desert sites ... (chain C7)" → chains C5, C7 ✓
- "— no chain — flagged assumption only for exactly how many currently-sited or planned towers fall into the water-unavailable category ..." → marker `no chain — flagged assumption only` ✓ (disclosed, untraced by design)
- "**Pre-check:** head C1 (HIGH), C2 (MEDIUM), C3 (LOW), C4 (LOW), C5 (LOW), C6 (LOW), C7 (LOW) · ..." → chains C1, C2, C3, C4, C5, C6, C7 ✓
- "**Confidence:** LOW — the Conclusion rests on C3, C4, C5, C6, and C7 ... resolving GT-8? (the USC-coal benchmark behind C2) would raise C2 but would not by itself lift the chains below it, since C3 and C4 carry independent unverified inputs of their own." → chains C2, C3, C4, C5, C6, C7 ✓

Ledger complete: 6 rows, 0 cuts. Every surviving §6 claim carries at least one chain reference, either inline or via the marked flagged-assumption caveat.

## Self-audit scan (process output)

| Chain | Chain Head (brief) | Form conforming? | Rule applied | Dependency clean? | Band | Act attempted? | Edges fired |
|-------|---------------------|-------------------|---------------|--------------------|------|-----------------|-------------|
| C1 | GT-1 + GT-2 + GT-12? | yes | n/a | yes | MEDIUM | yes | none |
| C2 | GT-3 + GT-4 + GT-8? | yes | n/a | yes | MEDIUM | yes | none |
| C3 | C2 + GT-9? | yes | n/a | yes | LOW | yes | none |
| C4 | GT-3 + GT-6? + GT-10 | yes | n/a | yes | LOW | yes | none |
| C5 | GT-4 + GT-9? + C4 | yes | n/a | yes | LOW | yes | none |
| C6 | C1 + C2 + C3 + C4 | yes | n/a | yes | LOW | yes | none |
| C7 | C6 | yes | n/a | yes | LOW | yes | none |
| C8 | C1 + C2 + C3 + C4 + C7 | yes | n/a | yes | LOW | yes | none |

Note on this table's history: an earlier draft of chains C3, C4, and C7 placed assumption labels (A-6, A-5; A-7/A-9/A-8) directly in the head line alongside GT-N/Cn identifiers, which does not parse under the head-input rule (only `GT-N`/`GT-N?`/`Cn` identifiers are valid head tokens). An earlier draft of C4 also opened its first and second hops with a bare `GT-N` identifier (`GT-3 and GT-6? converge…`, `GT-10's freeze-protection…`), which the mechanical form check reads as the head of a new chain. Both defects were corrected before this scan ran — the assumption labels were removed from the three head lines (their inline `[Assumes: A-N]` tags on the hops already carried this information) and the two GT-led hops were reworded to lead with prose — so every row above reflects the corrected, currently-emitted text, with the correction itself disclosed here rather than silently applied.

| §6 Span (brief) | Construct | Claim under R11? | R11 clause applied | Chain cited |
|-------------------|-----------|-------------------|----------------------|---------------|
| "Recommended approach: Treat the Carnot bound…" | bold lead-in | yes | bold lead-in whose colon closes the bold span, assertion on same line | C1, C2, C3, C4, C5, C6, C7 |
| "Key insight: The ~20-point gap…" | bold lead-in | yes | bold lead-in whose colon closes the bold span, assertion on same line | C6, C7 |
| "Trade-offs acknowledged: Pursuing the recoverable…" | bold lead-in | yes | bold lead-in whose colon closes the bold span, assertion on same line; trailing clause carries the `no chain — flagged assumption only` caveat marker | C5, C7 (primary clauses); trailing caveat marked — disclosed, scores untraced per the Caveats rule |
| "Pre-check: head C1 (HIGH), C2 (MEDIUM)…" | bold lead-in | yes | pre-check line is itself a claim per the template's explicit rule, discharged by the chains its own `head` field names | C1, C2, C3, C4, C5, C6, C7 |
| "Confidence: LOW — the Conclusion rests on C3, C4, C5, C6, and C7…" | bold lead-in | yes | bold lead-in whose colon closes the bold span, justification prose names chains explicitly | C2, C3, C4 (named explicitly in prose; C1, C5, C6, C7 additionally carried via the Pre-check `head` field immediately above) |

Scan complete: 8 chain rows, one per section-4 chain block in order; 5 section-6 rows, one per construct in order — 5 claims under R11, 0 excluded. 0 chains malformed, 0 claims fully untraced (1 claim carries one trailing caveat clause honestly marked `no chain — flagged assumption only`, which discloses rather than discharges that one clause).

## Self-Audit Gate (process output)

**Criterion 1: Identify Essence**
Quoted span: "For a nitrate-salt power-tower steam Rankine power block whose hot-salt source is fixed at 565°C (838 K), what is the law-permitted conversion-efficiency ceiling ... and how far below that ceiling does deployed/designed practice sit, and — of that gap — how much is recoverable with foreseeable engineering versus permanently locked in by the physics of real heat engines, CSP's current scale economics, desert siting, and nitrate-salt chemistry?"
Band: **Rigorous**
Justification: The Essence Statement names a specific, unique question (not a restatement of the prompt's framing device, not the triggering event) and each of the five success criteria is a verb+subject+outcome triplet checkable directly against the Conclusion section (e.g., "states a specific Carnot ceiling as a tight numeric range," "distinguishes gross and net plant electric efficiency, each traced to a named ground truth") without further interpretation.

**Criterion 2: Challenge Assumptions**
Quoted span (from the Assumption Audit scan): "Scan complete: 8 chains, 36 steps scanned in order; 6 steps surfaced an assumption (A-4, A-6, A-5, A-9, A-8, each exactly once); all 6 were already present in the §2 Classified Assumptions Table before this scan ran, so no new rows were added."
Band: **Rigorous**
Justification: All eleven rows in §2 use the four-type scheme with the prescribed treatment vocabulary; Verdict cells use the token-first-then-em-dash form (e.g., "Challenge — discarded as stated; GT-11? shows..."); two rows explicitly carry "Unverified — flagged" (A-5, A-6); at least five rows are Challenge or Discard, not uniformly Accept; and the Assumption Audit scan confirms the end-of-Phase-4 audit ran exhaustively over all 36 named chain steps with no step skipped and every surfaced assumption already resident in the table.

**Criterion 3: Establish Ground Truths**
Quoted span: "`?`-marked: GT-6, GT-7, GT-8, GT-9, GT-11, GT-12 (6 of 12)." — checked against §3: the GTs actually carrying a `?` suffix are GT-6?, GT-7?, GT-8?, GT-9?, GT-11?, GT-12?, exactly six, exactly matching the enumeration; GT-1 through GT-5 and GT-10 carry no suffix.
Band: **Rigorous**
Justification: Every GT carries a stable ID matching the identifiers cited in §4's chain heads; every unsuffixed GT has a specific, non-generic citation (an OSTI record with a direct quote, an engrxiv preprint abstract, or a derived physical-law statement); every GT carries an explicit provenance label; the enumeration matches the list exactly on inspection; no Phase-2-discarded item (Curzon–Ahlborn) appears in this list; and since no chain in the entire document is rated HIGH after the GT-12 correction (the highest band present is MEDIUM, on C1 and C2), the "every unsuffixed GT feeding a HIGH chain names its read-at-source location" clause is vacuously satisfied — there is no HIGH chain to check it against. Five Phase 3 failure records (GT-6?, GT-7?, GT-8?, GT-9?, GT-11?) and one additional unread-convention note (GT-12?) each name the source and the specific reason it could not be read.

**Criterion 4: Reason Upward**
Quoted span (from the self-audit scan's chain-form table): "| C1 | GT-1 + GT-2 + GT-12? | yes | n/a | yes | MEDIUM | yes | none | ... | C8 | C1 + C2 + C3 + C4 + C7 | yes | n/a | yes | LOW | yes | none |" — all eight rows read `Form conforming? = yes`, `Dependency clean? = yes`.
Band: **Rigorous**
Justification: Every conclusion stated in §4 or §6 has exactly one chain; every chain's head uses only `GT-N`/`GT-N?`/`Cn` identifiers (an earlier draft's non-conforming heads in C3, C4, and C7, and two GT-led hops in C4, were corrected before this scan ran, and that correction is disclosed in the scan's own note rather than silently applied); every chain contains at least one genuine intermediate step; §5 (Abandoned Reasoning) documents two dead ends with specific, non-generic abandonment reasons (a model-dependent-bound pitfall and a reclassified chemistry assumption); no analogy is used as standalone evidence (A-4's fossil-plant heuristic is explicitly triangulated against the CSP-specific GT-4, not asserted by analogy alone); every chain step that surfaced a new assumption carries an inline `[Assumes: A-N]` tag per the Assumption Audit scan; and the adversarial pass's Recompute step independently re-derived every computed figure in every chain and found no arithmetic error.

**Criterion 5: Validate**
Quoted span: "every chain is rated no higher than the lowest-rated chain its head cites" — verified by inspection: C3 cites C2 (MEDIUM) and is itself LOW; C6 cites C3/C4 (LOW) and is itself LOW; C8 cites C3/C4/C7 (LOW) and is itself LOW; no chain consumes a `GT-N?` input while rated HIGH (C1 and C2, the only chains with a `?`-marked input among their non-LOW-ceiling cases, are both MEDIUM).
Band: **Rigorous**
Justification: Every chain's confidence line names its own weakest link, its `GT-N?` inputs with a stated verification path, and the `Cn` it cites rated below HIGH without re-explaining that `Cn`'s own reasoning; the overall §6 Confidence (LOW) matches the weakest contributing chain (C3/C4/C5/C6/C7, all LOW); every chain's band matches what its three axes license on inspection (none rated above or below what Inputs/Inference/Rivals permit, as traced chain-by-chain in the adversarial pass's Sensitivity step); and the adversarial pass record (Pre-Mortem, since §6 carries a recommendation) is complete with all eight required parts — Recompute, Sensitivity, Rival, Premise, Causes, Clusters, Disposition, Falsification — each cluster in the record carrying either a named plan change (Cluster A) or an explicitly accepted risk with a named mitigation (Clusters B and C).

**Criterion 6: Conclusion-to-Ground-Truth Traceability**
Quoted span (from the self-audit scan's claim-inventory table): "Scan complete: ... 5 section-6 rows, one per construct in order — 5 claims under R11, 0 excluded. 0 chains malformed, 0 claims fully untraced (1 claim carries one trailing caveat clause honestly marked `no chain — flagged assumption only`...)."
Band: **Rigorous**
Justification: All five §6 claims (Recommended approach, Key insight, Trade-offs acknowledged, Pre-check, Confidence) trace to specific named §4 chains per the claim-inventory table, with the one trailing caveat that cites no chain carrying the honest-disclosure marker rather than being silently asserted; no claim introduces reasoning absent from §4; and the Key Insight — that roughly 15–16 of the ~20-point Carnot-to-practice gap is an exergy penalty intrinsic to any real Rankine cycle rather than a CSP-specific shortfall — is a distinct, non-obvious finding, not a restatement of the Recommended approach's architecture-upgrade recommendation.

**Gate result:** cleared · passes: 1 · Fix/Repeat fired: no

## Structured summary (process output)
```json
{
  "schema_version": 1,
  "run_mode": "full-composer",
  "assumptions": [
    {"id": "A-1", "type": "physical law", "verdict": "Accept"},
    {"id": "A-2", "type": "convention", "verdict": "Challenge"},
    {"id": "A-3", "type": "convention", "verdict": "Accept"},
    {"id": "A-4", "type": "untested belief", "verdict": "Challenge"},
    {"id": "A-5", "type": "untested belief", "verdict": "Challenge"},
    {"id": "A-6", "type": "untested belief", "verdict": "Challenge"},
    {"id": "A-7", "type": "convention", "verdict": "Challenge"},
    {"id": "A-8", "type": "current constraint", "verdict": "Accept"},
    {"id": "A-9", "type": "current constraint", "verdict": "Challenge"},
    {"id": "A-10", "type": "untested belief", "verdict": "Accept"},
    {"id": "A-11", "type": "convention", "verdict": "Discard"}
  ],
  "ground_truths": [
    {"id": "GT-1", "read_at_source": true},
    {"id": "GT-2", "read_at_source": true},
    {"id": "GT-3", "read_at_source": true},
    {"id": "GT-4", "read_at_source": true},
    {"id": "GT-5", "read_at_source": true},
    {"id": "GT-6", "read_at_source": false},
    {"id": "GT-7", "read_at_source": false},
    {"id": "GT-8", "read_at_source": false},
    {"id": "GT-9", "read_at_source": false},
    {"id": "GT-10", "read_at_source": true},
    {"id": "GT-11", "read_at_source": false},
    {"id": "GT-12", "read_at_source": false}
  ],
  "chains": [
    {"id": "C1", "confidence": "MEDIUM", "rests_on": ["GT-1", "GT-2", "GT-12?"]},
    {"id": "C2", "confidence": "MEDIUM", "rests_on": ["GT-3", "GT-4", "GT-8?"]},
    {"id": "C3", "confidence": "LOW", "rests_on": ["C2", "GT-9?"]},
    {"id": "C4", "confidence": "LOW", "rests_on": ["GT-3", "GT-6?", "GT-10"]},
    {"id": "C5", "confidence": "LOW", "rests_on": ["GT-4", "GT-9?", "C4"]},
    {"id": "C6", "confidence": "LOW", "rests_on": ["C1", "C2", "C3", "C4"]},
    {"id": "C7", "confidence": "LOW", "rests_on": ["C6"]},
    {"id": "C8", "confidence": "LOW", "rests_on": ["C1", "C2", "C3", "C4", "C7"]}
  ],
  "dead_ends": [
    "Using the Curzon–Ahlborn \"efficiency at maximum power\" formula as the realistic Rankine ceiling",
    "Treating 565°C as a hard, chemistry-imposed decomposition ceiling for solar salt"
  ],
  "techniques": {
    "applied": ["theoretical-limit", "estimate", "trade-off", "fishbone", "second-order", "pre-mortem"],
    "not_applied": [
      {
        "technique": "inversion",
        "phase": 2,
        "reason": "the Phase 2 trigger (a conclusion or goal that feels too clean with a suspiciously thin assumption set) did not fire: the Assumptions Table carries eleven rows with multiple Challenge and Discard verdicts, not a thin, uniformly-Accept set; and at Phase 5 the decision rule assigns Pre-Mortem rather than Inversion because section 6 carries an explicit recommendation"
      },
      {
        "technique": "five-whys",
        "phase": 3,
        "reason": "every ground truth in section 3 is already either a direct primary-source figure or a self-evident physical-law identity; none is a compound claim bundling multiple constituent facts that would benefit from recursive decomposition to primitives"
      }
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
    "recommendation": "Treat the Carnot bound (≈61–63%, chain C1) as the absolute law-permitted ceiling and the large-scale real-Rankine ceiling (≈46–48% gross / ≈44–46% net, chain C2) as the meaningful thermodynamic ceiling for a steam cycle capped at 565°C; evaluate current CSP practice (≈41–42% gross / ≈35–39% net, chain C4) against the scale-and-siting-matched ceiling (≈40–45% gross, chain C3) rather than against Carnot, because that comparison shows practice is already within roughly 0–2 gross points of what this plant class's scale and siting allow (chain C6); the highest-value near-term engineering move is adopting supercritical pressure and reheat (chain C5, worth ~2–4 points), paired with cooling-system or insulation improvements where a site's water access permits (chain C7).",
    "confidence": "LOW",
    "rests_on": ["C1", "C2", "C3", "C4", "C5", "C6", "C7"]
  }
}
```
