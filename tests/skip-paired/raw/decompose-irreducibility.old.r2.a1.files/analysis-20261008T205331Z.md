# First-Principles Analysis: 85% Round-Trip Molten-Salt Electricity Storage Claim

**Mode:** full-composer (no single-technique trigger phrase fired; the request asks for a
full decomposition-to-ground-truths analysis of a bundled multi-part claim).

**Re-entry disclosure:** No re-entry edge fired in this run. No bounded re-entry (Criterion 1
Absent / mid-run `AskUserQuestion` / second-order return to Phase 2 / Fix-Repeat loop) was
triggered; this section is included to satisfy the disclosure requirement even when empty.

---

## 1. Problem Essence

**Core problem:** Does the specific bundled claim — that a 5 MWh molten-salt thermal storage
tank operating 290–565 °C achieves above-85% **electricity-in/electricity-out** round-trip
efficiency and is **cost-competitive per nameplate kWh** with an equal-capacity lithium-ion
battery system — survive first-principles thermodynamic and cost scrutiny, or does it conflate
heat-storage efficiency/cost (a real, well-precedented quantity) with battery-equivalent
electrical-storage efficiency/cost (a different quantity the claim's own wording asserts but
does not deliver)?

This is a convention-vs-physical-law question at its root (a theoretical-limit reframe, applied
here in Phase 1 rather than deferred): "round-trip efficiency" has two live meanings in the CSP
and storage literature — a thermal-retention convention (heat stored ÷ heat recovered, often
93–99%) and a hard-physics quantity (electricity stored ÷ electricity recovered, Carnot-bounded
on the discharge leg). The essence question is which meaning the claim is actually trading on,
and whether 85% is defensible under the meaning the claim's own words specify.

**Success criteria:**
1. The Conclusion states, with a numeric bracket, whether >85% **electrical** round-trip
   efficiency is physically achievable at 290–565 °C for the architecture(s) consistent with the
   claim's own wording ("electricity into heat and back").
2. The Conclusion states whether the stated cost comparison is scoped on a consistent accounting
   basis (thermal vs. electrical capacity; tank-only vs. turnkey system) and what the comparison
   becomes once corrected.
3. The Conclusion names the specific mechanism, if any, by which an 85% figure and/or a favorable
   cost comparison can be real while describing a different quantity than "battery-equivalent
   electrical round-trip efficiency/cost" — i.e., whether this is a case of conflation, and what
   the conflated quantities actually are.

---

## 2. Assumptions Table

| Assumption | Type | Treatment | Verdict | Verification |
|------------|------|-----------|---------|--------------|
| A-1: "Round-trip efficiency" in the claim means electricity-in/electricity-out, not heat-in/heat-out. | convention | Explicitly challenge — industry sources routinely use "round-trip efficiency" for thermal-only retention (93–99%), creating equivocation risk. | Accept — the claim's own wording ("round-trip **electricity** into heat and back") specifies the electrical reading; that reading is adopted as the one under test. | GT-2 (claim text itself, electrical-reading forced by wording) |
| A-2: The architecture is resistive (Joule) heating + conventional heat engine ("architecture a"), not a heat-pump-based PTES/Carnot battery ("architecture c"). | convention | Explicitly challenge — the claim does not name a heat pump or a separate cold store, and the 290/565 °C pair is the CSP two-tank signature (GT-2), not a PTES spec sheet. | Accept as primary reading (matches claim wording + signature); architecture c tested separately as the most charitable alternative (chain C2). | GT-2, GT-3 |
| A-3: 290–565 °C is achievable with standard nitrate salt (no exotic chloride-salt chemistry required). | current constraint | Record expiry — holds while top temperature ≤~565–600 °C; nitrate salt degrades above that, motivating NREL's chloride-salt R&D track. | Accept — expires only if operating temperature is pushed above ~600 °C, which the claim does not do. | corroborated by multiple independent secondary sources (Sandia, SolarPACES/NREL project DB, group.sener); not separately load-bearing for the verdict |
| A-4: "Nameplate capacity" means the same thing (comparable 1:1 in MWh) for a thermal tank and a battery. | convention | Explicitly challenge — this is the crux of the cost sub-claim's sleight-of-hand. | Challenge — a battery's nameplate MWh is usable electrical capacity; a tank's "5 MWh" could mean thermal content or electrical-output-after-losses, which differ by the round-trip-efficiency factor (~2.5–3×, chain C1). | derived precondition P3 of the Phase-2 inversion pass below |
| A-5: Tank-only $/kWh-thermal cost (CSP convention) and turnkey Li-ion $/kWh (all-in system price) are comparable on the same equipment boundary. | convention | Explicitly challenge. | Challenge — GT-5? prices the storage medium only; GT-6/GT-7? price cells+BMS+inverter+enclosure+integration; not the same scope. | derived precondition P3 of the Phase-2 inversion pass below; chain C4 |
| A-6: A standalone 5 MWh unit of this exact architecture is a commercially representative scale. | untested belief | Verify or flag unverified. | Challenge — flagged unverified; no commercially deployed 5 MWh standalone unit of this architecture was located. All demonstrated analogs (Solar Two, Gemasolar, Malta M100) are utility-scale (100+ MWe class). | unverified — flagged; derived precondition P4 of inversion pass |
| A-7 (inversion-derived): For 85% round-trip to be true, either (i) the discharge leg evades the Carnot bound, or (ii) "round trip" silently excludes electrical reconversion. | untested belief | Verify. | Challenge — both fail: (i) is physically impossible per GT-1/GT-9/GT-10; (ii) contradicts the claim's own wording (A-1). This is the load-bearing finding of the Phase-2 inversion pass. | GT-1, GT-9, GT-10 |
| A-8: Molten-salt tank, power-block, and charging-equipment capex scale linearly down to 5 MWh with no diseconomy-of-scale penalty. | untested belief | Flag unverified. | Challenge — process equipment (tanks, turbines) typically follows cost ∝ capacity^0.6–0.8; a 5 MWh unit would carry materially higher $/kWh than the 100+ MWh reference plants GT-5? describes. Directionally weakens the cost claim further if true. | unverified — flagged; chain C4 |
| A-9: Two-tank sensible-heat storage retains ~95–99% of stored heat per charge–discharge cycle. | untested belief | Flag unverified; used as an Estimate-procedure bracket input. | Accept, flagged — standard order-of-magnitude figure for short-duration (daily-cycle) sensible-heat storage in this literature; not independently sourced this session. | unverified — flagged; chain C1 `[Assumes: A-9]` |
| A-10: Project financing (debt covenants, PPA pricing, capacity guarantees) for a system like this would embed the vendor's stated RTE/cost figures rather than independently verified ones. | untested belief | Flag unverified; used only in the second-order extension, not load-bearing for the core verdict. | Accept, flagged — standard project-finance practice, not independently sourced this session. | unverified — flagged; chain C5 `[Assumes: A-10]` |

### Phase 2 — Inversion pass (companion technique, applied here per Step 0: conclusion-under-test felt "too clean")

**Claim, precisely:** "A 5 MWh molten-salt TES system, 290–565 °C, achieves >85% electricity-in/
electricity-out round-trip efficiency AND costs less per nameplate kWh than an equal-capacity
Li-ion system."

**Inverted:** "The system does NOT achieve >85% round-trip electrical efficiency, OR does NOT
cost less than equal-capacity Li-ion."

**Failure-guaranteeing conditions (≥5):**
1. The discharge leg (heat→electricity) runs a conventional single-reservoir heat engine whose
   efficiency is Carnot-capped between 565 °C and the ambient heat-rejection temperature
   (~62% ideal ceiling before real-machine losses) — any electrical reconversion step at all
   makes >85% round-trip impossible once this leg exists.
2. The charging leg is simple resistive heating with no heat-pump COP advantage, so it cannot
   contribute a multiplier to offset the discharge leg's losses.
3. "Round trip" is measured honestly as electricity-delivered ÷ electricity-drawn, not as
   heat-retained ÷ heat-stored.
4. The $/kWh figures compared are not normalized to the same energy-accounting basis (thermal
   MWh stored vs. electrical MWh deliverable).
5. The power block and charging equipment — excluded from the tank-only $/kWh figure — carry
   capex that does not shrink proportionally at 5 MWh scale.
6. No commercially deployed 5 MWh standalone unit of this exact architecture exists to validate
   either figure, so the claim extrapolates from utility-scale CSP and/or nascent PTES
   demonstrations never built or costed at this scale.

**Derived necessary preconditions (each a falsifiable claim, tagged load-bearing):**
- **P1** [load-bearing] "The heat→electricity conversion step exceeds the Carnot limit for
  565 °C/ambient, or is absent from the round trip." — Status: **FALSE** (GT-1, GT-9, GT-10; the
  claim's own wording includes a reconversion step).
- **P2** [load-bearing] "'Round trip' in the claim is measured as electricity-out ÷
  electricity-in." — Status: **TRUE** per the claim's literal wording — and it is exactly the
  conjunction of P2-true with P1-false that breaks the claim.
- **P3** [load-bearing, cost sub-claim] "The compared $/kWh figures share the same
  energy-accounting basis and system scope." — Status: **unverified, likely FALSE** (A-4, A-5).
- **P4** [load-bearing, cost sub-claim only] "A 5 MWh unit of this architecture has been built,
  demonstrated, or credibly costed." — Status: **unverified, no evidence found** (A-6, A-8).

---

## 3. Ground Truths

- **GT-1** Carnot efficiency bound: for a heat engine operating between hot reservoir T_h and
  cold reservoir T_c (absolute temperatures), the maximum possible thermal-to-work conversion
  efficiency is η = 1 − T_c/T_h; no real heat engine exceeds this. — source: Carnot's theorem
  (second law of thermodynamics), standard result in any thermodynamics text (e.g., Cengel &
  Boles, *Thermodynamics: An Engineering Approach*); provenance: **physical law** — verified by
  derivation, not by document read.

- **GT-2** At Solar Two and Gemasolar (the two-tank nitrate-salt central-receiver plants that
  define the 290–565 °C signature), the cold salt tank operates at ≈290 °C and the hot salt tank
  at ≈565 °C. — source: Sandia National Laboratories, "Receiver System Lessons Learned from
  Solar Two" (2002); read-at-source: quoted passage, "A molten-nitrate-salt heat transfer fluid
  was pumped from a storage tank at grade level, heated from 290 to 565 C by the receiver."
  Independently corroborated (not separately read-at-source) by SolarPACES/NREL's Gemasolar
  project page and group.sener.

- **GT-3** The Malta M100-10 pumped-heat-energy-storage (PHES) plant's stated **Overall System
  Efficiency AC-to-AC (RTE_AC)** — defined in the spec sheet as "ratio of the delivered discharge
  energy to the delivered charge energy at the output terminals, parasitics included" — is
  **53%–65%**. — source: Malta Inc., "Malta M100 System Technical Specifications" (PDF); read-at-
  source: page 2, "Key Technical Specification for the Malta M100-10 Plant" table, row "Overall
  System Efficiency AC to AC (RTEAC)," value "53% - 65%."

- **GT-4?** The same Malta PHES technology family reports materially different round-trip figures
  depending on output accounting: power-to-power ≈55–60%, power-to-heat ≈96%, and cogeneration
  (heat + power blended) ≈85–95%. — cited to: Malta Inc. technical/marketing materials
  (incl. a SwRI-sourced presentation and a Malta CHP white paper); reported-by-delegate: supplied
  by a web-search summary; this analysis attempted to open the underlying Malta "Replacing
  Fossil-Fueled CHP" PDF directly and received HTTP 404 — cited source not opened by this
  analysis. **Phase 3 failure record:** source `maltainc.com/assets/pdf/Replacing Fossil-Fueled
  Combined Heat and Power Plants...pdf` — unreachable (404 Not Found).

- **GT-5?** Two-tank molten-nitrate-salt thermal storage (Solar Two / Solana reference scale)
  costs approximately **$22–30/kWh-thermal** (storage medium and tank only). — cited to: NREL
  cost analyses, reported across multiple secondary CSP-industry sources (pv-magazine "Next-gen
  concentrated solar power now under development," Reuters Events "Carving costs with
  single-tank thermal storage"). **Phase 3 failure record:** this analysis opened the underlying
  primary source — NREL/TP-5500-57625, "Molten Salt Power Tower Cost Model for the System
  Advisor Model (SAM)" — directly (PDF fetched and converted to text), but the specific
  $/kWh-thermal storage-cost figure could not be located in the extracted text; the report's cost
  tables lost row/value alignment on PDF→text conversion. Reason: **citation does not support the
  claim** (figure not located in accessible content) — mark retained `?`.

- **GT-6** Lithium-ion battery **pack** prices: the global average fell 8% year-on-year to a
  record low of **$108/kWh in 2025** (all applications); pack prices for **stationary storage**
  specifically fell to **$70/kWh in 2025**, 45% lower than in 2024 (≈$127/kWh implied for 2024
  stationary). — source: BloombergNEF press release, "Lithium-ion battery pack prices fall to
  $108 per kilowatt-hour despite rising metal prices"; read-at-source: quoted directly,
  "lithium-ion battery pack prices have dropped 8% since 2024 to a record low of $108 per
  kilowatt-hour" and "Battery pack prices for stationary storage dropped to $70/kWh in 2025,
  45% lower than in 2024."

- **GT-7?** **Turnkey** battery energy storage system (BESS) prices — complete installed systems
  including cells, inverter, BMS, enclosure, and integration, not cells/packs alone — averaged
  **$169/kWh globally in 2024** and **$117/kWh in 2025** (2-hour duration ≈$124/kWh, 4-hour
  ≈$110/kWh); regional 2025 figures: China $73/kWh, Europe $177/kWh, US $219/kWh. — cited to:
  BloombergNEF/Ember reporting, via energy-storage.news and ess-news.com; reported-by-delegate:
  supplied by a web-search summary; the BNEF primary press release opened directly for GT-6 did
  not itself contain the turnkey-system breakdown — cited source not opened by this analysis for
  this specific figure.

- **GT-8?** Published/credited round-trip efficiencies for heat-pump-based pumped thermal
  electricity storage ("Carnot battery") systems other than Malta: Echogen's PTES design is
  generally cited around **55–56%**; the broader PTES technical literature reports a **~40–60%**
  range. — cited to: Echogen technical materials and a Cambridge University repository PTES
  thermodynamics paper, via web-search summary; reported-by-delegate — neither primary source
  opened directly by this analysis.

- **GT-9** Resistive (Joule) electrical heating converts electrical energy to heat at
  near-unity efficiency (commonly ≥98%, limited only by minor convective/radiative losses from
  the heating-element enclosure before the heat reaches the storage medium). — source: Joule's
  first law / conservation of energy, standard electrical-engineering result; provenance:
  **physical law** — verified by derivation.

- **GT-10** For the NREL reference molten-salt power-tower plant (Daggett, CA), the design
  ambient dry-bulb temperature used for the power-block condenser/cooling system is **42 °C**;
  in a Rankine-cycle power block, the heat engine's cold reservoir is set by this ambient
  heat-rejection temperature, not by the thermal-storage medium's cold-tank temperature (the
  290 °C cold salt tank is a storage-loop return temperature, not the power cycle's condenser
  temperature). — source: NREL/TP-5500-57625, "Molten Salt Power Tower Cost Model for the System
  Advisor Model (SAM)"; read-at-source: Table 2 ("SAM modeling results using the spreadsheet cost
  model"), row "Design conditions dry-bulb temperature (°C)," value "42," column "Daggett, CA."
  The general Rankine-cycle architecture point (condenser decoupled from storage cold-tank
  temperature) is standard power-plant engineering, carried as definitional support for this GT
  rather than separately cited.

- **GT-11?** Real Rankine steam-cycle hardware typically achieves roughly **55–65% of its Carnot
  limit** (second-law/exergy efficiency) at CSP-relevant operating conditions. — unverified:
  general power-plant engineering range, not independently sourced via a fresh citation this
  session; used only as an Estimate-procedure bracket input in chain C1, and the conclusion's
  robustness to this input is checked explicitly in the Phase 5 sensitivity/adversarial pass.

- **GT-12?** The DOE SunShot CSP thermal-energy-storage R&D target is a storage cost below
  **$15/kWh-thermal** paired with a round-trip efficiency target of **≥93%** — and this 93%
  figure is a **thermal** (heat-retained ÷ heat-stored) round-trip target for the storage medium,
  not an electricity-reconversion figure, consistent with its pairing against a $/kWh-**thermal**
  cost metric in CSP program literature. — cited to: DOE SunShot program materials, via
  pv-magazine's CSP cost-model coverage and a NETL/climateinvestmentfunds.org presentation;
  reported-by-delegate. **Phase 3 failure record:** two targeted attempts to open a primary
  energy.gov page for this target both returned HTTP 404 Not Found — unreachable.

**Provenance summary:**
`?`-marked: GT-4, GT-5, GT-7, GT-8, GT-11, GT-12 (6 of 12)
Read-at-source: GT-2 — Sandia "Receiver System Lessons Learned from Solar Two" (2002), quoted
passage above. GT-3 — Malta M100 Technical Specifications PDF, p.2 table, "Overall System
Efficiency AC to AC (RTEAC)" row. GT-6 — BNEF press release, two quoted passages above. GT-10 —
NREL/TP-5500-57625, Table 2, "Design conditions dry-bulb temperature (°C)" row. GT-1, GT-9 —
physical law, verified by derivation (no document read applicable).

---

## 4. Derivation Chains

### Theoretical-limit tiers (companion technique, applied here per Step 0 — governs chains C1/C2)

**Direction:** higher is better (efficiency is being maximized).

**Architecture (a) — resistive-heated tank + conventional single-reservoir heat engine** (the
claim's literal wording: "electricity resistively heats salt... recovered via a heat engine"):
- **Ideal ceiling:** governing hard constraint = the second law of thermodynamics (Carnot's
  theorem), applied to the single discharge-leg heat engine; the charging leg is capped at ≤100%
  by energy conservation (GT-9) and so cannot lift the round trip above the discharge leg's own
  ceiling. Derived value: **62.4%** (GT-1 + GT-10).
- **Best demonstrated:** no publicly demonstrated grid-scale resistive-heated nitrate-salt
  round-trip-electricity system was located in this research — an evidence gap, not a number, and
  itself a finding (the claim's exact architecture has no public track record).
- **Conventional/claimed figure:** 85% (the claim under test).
- **Gap, ideal ceiling → conventional:** the claimed 85% **exceeds the derived ideal ceiling by
  22.6 percentage points** — this is not unreached headroom, it is a figure the governing hard
  constraint forbids outright for this architecture.

**Architecture (c) — heat-pump-charged PTES/"Carnot battery"** (the most charitable alternative
reading, consistent with "electricity into heat and back" but not with the claim's resistive
wording or its silence on a cold store):
- **Ideal (reversible) bound:** not a clean closed-form Carnot number — a two-reservoir
  regenerative heat-pump/heat-engine cycle approaches 100% round trip in the fully reversible,
  loss-free limit. Flagged per the theoretical-limit procedure's own caution: this bound is
  **model-dependent and not usefully tight** for engineering purposes (the real constraint is
  compressor/expander/heat-exchanger irreversibility, not Carnot per se), so it is not used as
  the operative ceiling below.
- **Best demonstrated:** 53–65% AC-AC (GT-3, read-at-source, Malta M100); ~55–56% (GT-8?,
  Echogen).
- **Conventional/claimed figure:** 85%.
- **Gap, best demonstrated → conventional:** the claim exceeds the best publicly demonstrated
  grid-scale PTES figure by **20–32 percentage points** — in the most favorable architecture
  reading, still unreached headroom nobody has publicly proven.

### Conclusion C1: Under the claim's literal architecture, electrical round-trip efficiency brackets to ~32–39% (central ~36%), not >85%

GT-1 (Carnot law) + GT-10 (565 °C salt / 42 °C ambient condenser) + GT-11? (real cycles reach 55–65% of Carnot) + GT-9 (resistive charging ≈98%)
→ combining the 62.4% Carnot ceiling with real Rankine second-law efficiency (55–65% of Carnot) brackets the achievable discharge-leg efficiency to roughly 34–41%
→ multiplying near-unity resistive charging and an assumed 95–99% storage retention per cycle *[Assumes: A-9]* against that bracket yields round-trip electrical efficiency of roughly 32–39%, central ≈36%
→ a 36% central estimate sits far below the claimed 85%, so the claim's thermodynamic premise fails for the architecture its own wording describes

**Pre-check:** head GT-1, GT-10, GT-11?, GT-9 · ?-marked: GT-11? · lowest cited: none · Inputs ceiling: MEDIUM
**Confidence:** MEDIUM — GT-11? (real-cycle fraction of Carnot) is unverified this session; verification would be a vendor/engineering datasheet for a specific small steam-turbine generator's isentropic efficiency at 565 °C/42 °C conditions. Sensitivity check (Phase 5): even generous substitutes for GT-11? (see adversarial pass below) do not change the qualitative verdict. A-9's 95-99% retention range is already incorporated as the bracket's own span (hop 2), so the endpoint (36% central, far below 85%) is insensitive to A-9's specific value within its plausible range and the `[Assumes: A-9]` annotation does not short the Inference axis.

### Conclusion C2: Even under the most charitable architecture (genuine heat-pump PTES), demonstrated round-trip efficiency tops out at 53–65%, still far short of 85%

GT-3 (Malta M100 AC-AC RTE 53–65%) + GT-8? (Echogen ~55–56%, PTES literature range ~40–60%)
→ independently developed PTES/Carnot-battery systems built specifically to maximize electrical round-trip efficiency cluster in the 53–65% demonstrated/rated range
→ none of these best-in-class, purpose-built electrical-storage architectures reach 85%, so even the most charitable reading of the claim's architecture falls 20–32 percentage points short

**Pre-check:** head GT-3, GT-8? · ?-marked: GT-8? · lowest cited: none · Inputs ceiling: MEDIUM
**Confidence:** MEDIUM — GT-8? (Echogen/PTES-literature figures) is reported-by-delegate; verification would be opening the Echogen technical disclosures or the Cambridge PTES thermodynamics paper directly. This chain is itself the ruling-out of the rival "a different, undescribed architecture could plausibly reach 85%" — no publicly demonstrated architecture does.

### Conclusion C3: An 85% figure is real and precedented, but only under heat-retention or heat-heavy cogeneration accounting — not electricity-to-electricity accounting

GT-4? (Malta: power-to-heat 96%, cogeneration 85–95%, vs. power-to-power 55–60%) + GT-12? (DOE SunShot thermal-storage target ≥93% RTE, paired with $/kWh-thermal) + C1 (architecture-a electrical round trip ≈36%)
→ within a single technology family (Malta PHES), round-trip figures swing from ~55–60% (power-to-power) to 85–95% (cogeneration) to 96% (power-to-heat only), depending solely on how much output is counted as reconverted electricity versus retained/used heat
→ the DOE's own ≥93% RTE target for CSP thermal storage is explicitly a heat-retention figure paired with a $/kWh-thermal cost metric, not an electricity-reconversion figure, confirming that 90%+ "round-trip" numbers are an established convention for thermal-only accounting in this literature
→ an 85% figure is therefore physically real and well-precedented for heat-in/heat-out or heat-heavy cogeneration accounting, but the same hardware family delivers only ~36% once accounting is restricted to electricity-in/electricity-out, so quoting 85% as a round-trip *electrical* efficiency conflates two non-interchangeable accounting bases

**Pre-check:** head GT-4?, GT-12?, C1 (MEDIUM) · ?-marked: GT-4?, GT-12? · lowest cited: MEDIUM · Inputs ceiling: MEDIUM
**Confidence:** MEDIUM — GT-4? and GT-12? are both reported-by-delegate (verification: open the Malta CHP white paper and a primary DOE SunShot program page directly; both attempts 404'd this session, see Phase 3 failure records); C1 is cited at MEDIUM, which also caps this chain at MEDIUM.

### Conclusion C4: The tank-only cost figure is not obviously cheaper than Li-ion once efficiency-corrected, and the gap depends on an excluded, unsourced power-block/charging cost this analysis could not confirm

GT-5? (tank-only cost $22–30/kWh-thermal) + C1 (architecture-a round-trip 32–39%) + GT-7? (turnkey Li-ion $117–219/kWh, 2025)
→ dividing the tank-only thermal cost by C1's round-trip-efficiency bracket converts it to a cost per usable-electric-kWh of roughly $56–94/kWh — at or below the low end of current turnkey Li-ion prices, so the storage-medium leg alone does not obviously lose the comparison once efficiency-corrected
→ that $56–94/kWh figure excludes the power block (turbine/generator) and charging equipment the tank-only citation never priced, and both line items carry capex that does not shrink proportionally at 5 MWh scale the way utility-scale plants amortize it *[Assumes: A-8]*
→ because this analysis could not locate a sourced power-block/charging capex figure at 5 MWh scale, the cost-competitiveness claim is **unsupported and likely unfavorable once the excluded capex is added — not cleanly disproven** the way the thermodynamic claim is disproven by Carnot's theorem

**Pre-check:** head GT-5?, C1 (MEDIUM), GT-7? · ?-marked: GT-5?, GT-7? · lowest cited: MEDIUM · Inputs ceiling: MEDIUM
**Confidence:** MEDIUM — GT-5? and GT-7? are both unverified this session (GT-5?'s Phase 3 failure record: figure not locatable in extracted PDF text; GT-7? reported-by-delegate); C1 cited at MEDIUM also caps this chain. Verification path: (a) re-extract NREL/TP-5500-57625's cost table with a layout-preserving tool, (b) source a specific small-scale (≤5 MW) steam/ORC power-block $/kW figure, (c) open a primary BNEF/Wood Mackenzie system-price report for GT-7?'s regional breakdown. The `[Assumes: A-8]` annotation on hop 2 does not short the Inference axis beyond what Inputs already caps: hop 3's endpoint is already stated as "unsupported — not disproven" rather than a firm number, so if A-8 fails (capex *does* scale linearly to 5 MWh) the endpoint does not need to change — it already declines to assert a direction pending that figure.

### Conclusion C5: Second-order effects — actor lens and time lens (mandatory Phase 4 extension)

**Actor lens** (who changes what they do once C1/C4 hold): project developers who financed a unit
against the claimed 85% RTE and tank-only costs; competing Li-ion and genuine-PTES vendors;
lenders/off-takers who wrote performance guarantees. **Time lens** (immediate / after a few
cycles / once assumed true for years): the gap is invisible pre-commissioning, visible at first
metered performance test, and structurally embedded in financing terms if not corrected before
financial close.

C1 (architecture-a RTE ≈36%) + C4 (cost-competitiveness unsupported/likely unfavorable)
→[2nd, actor] project developers who financed a unit against an assumed 85% RTE and tank-only costs would need roughly 2–2.5× more charging electricity and face materially higher real capex per usable kWh than budgeted, eroding the investment case; competing Li-ion and genuine-PTES vendors gain a credibility advantage once measured performance is compared
→[3rd, time: near-term] debt covenants, PPA pricing, and capacity-performance guarantees written against the claimed figures *[Assumes: A-10]* would be exposed within the first commissioning cycles, well before any long-term degradation effect, triggering penalty or refinancing events
→[3rd, time: long-term] repeated exposure of this gap would damage market credibility for this specific small-scale configuration even in future proposals that quote honestly-scoped figures, chilling investment in a technology pathway that might be viable at the right scale and accounting basis

**Pre-check:** head C1 (MEDIUM), C4 (MEDIUM) · ?-marked: none · lowest cited: MEDIUM · Inputs ceiling: MEDIUM
**Confidence:** MEDIUM — capped by C1 and C4, both MEDIUM; no contradiction with any ground truth was found, so this extension stands without routing back to Phase 2. The `[Assumes: A-10]` annotation on hop 2 does not change this chain's band: if A-10 fails (financing does not mechanically embed the vendor's figures), hop 2 weakens from "would be exposed" to "may be exposed," but hop 1 and hop 3's effects (investment-case erosion, competitor advantage, credibility damage) stand regardless, and A-10 is not load-bearing for the core verdict (C1/C6), only for this non-load-bearing extension.

### Conclusion C6: Synthesis — the claim as stated is not defensible on either leg; it borrows battery vocabulary for CSP thermal-storage economics without the accounting that vocabulary requires

C1 (architecture-a RTE ≈36%) + C2 (best-architecture-c RTE 53–65%) + C3 (85% real only under thermal/cogeneration accounting) + C4 (cost comparison not apples-to-apples; direction likely unfavorable but unconfirmed)
→ under every architecture consistent with the claim's own description — resistive-heated two-tank, or best-case heat-pump PTES — genuine electricity-in/electricity-out round-trip efficiency tops out between roughly 36% and 65%, never approaching 85%
→ the only accounting basis under which 85% is a real, precedented number is heat-retention or heat-heavy cogeneration, which is not the electricity-to-electricity quantity a lithium-ion battery delivers, and the cost comparison inherits the identical category error (tank-only thermal $/kWh vs. turnkey electrical $/kWh)
→ the claim as literally stated is not defensible on its thermodynamic leg (a hard physical-law violation for architecture a, and a 20+ point unreached gap for the best alternative architecture) and is unsupported — not cleanly disproven — on its cost leg; it reads as CSP thermal-storage economics borrowing the vocabulary of battery round-trip efficiency without doing the accounting that vocabulary requires

**Pre-check:** head C1 (MEDIUM), C2 (MEDIUM), C3 (MEDIUM), C4 (MEDIUM) · ?-marked: none · lowest cited: MEDIUM · Inputs ceiling: MEDIUM
**Confidence:** MEDIUM — every cited chain is MEDIUM (driven by the `?`-marked ground truths named in each), so this synthesis is capped at MEDIUM; no cited chain is LOW and no rival conclusion survives unaddressed (C2 rules out "a better architecture reaches 85%"; C3 rules out "the figure is simply wrong" by explaining *why* 85% is a real number under a different accounting basis). Three independent chains below (C7, C8, C9) corroborate this synthesis's direction at HIGH confidence using only unsuffixed ground truths, without being required to lift this chain's own band — per the ceiling rule a chain is capped by the lowest-rated chain *its own head* cites, and this head cites only C1–C4.

### Conclusion C7: The ideal, loss-free Carnot ceiling for architecture (a)'s discharge leg is 62.4% — already below the claimed 85%, independent of any real-machine performance estimate

GT-1 (Carnot law) + GT-2 (confirms Th = 565 °C is the claim's own envelope) + GT-9 (charging capped ≤100%, no reservoir-exploiting multiplier) + GT-10 (Tc = 42 °C ambient condenser)
→ combining GT-1's formula with GT-10's 42 °C ambient sink and GT-2's confirmed 565 °C hot-salt temperature yields an ideal Carnot ceiling of 1 − 315.15⁄838.15 = 62.4% for the discharge leg alone
→ because GT-9 caps the charging leg at ≤100% with no reservoir-exploiting multiplier, the round trip cannot exceed this single-leg ceiling, so 62.4% is a hard upper bound on architecture (a)'s round-trip efficiency regardless of how well real machinery performs
→ this 62.4% hard bound already sits 22.6 percentage points below the claimed 85%, so the claim is refuted by the governing physical law alone, independent of any estimated or disputed engineering performance figure

**Pre-check:** head GT-1, GT-2, GT-9, GT-10 · ?-marked: none · lowest cited: none · Inputs ceiling: HIGH
**Confidence:** HIGH — every head identifier is an unsuffixed GT with a named read-at-source location, or physical law verified by derivation; every hop follows by direct arithmetic that recomputes (62.4%, confirmed independently in the Phase 5 Recompute step below) or by energy-conservation logic (GT-9's ≤100% cap); the obvious rival ("a colder ambient sink raises the ceiling above 85%") is ruled out quantitatively — even an unrealistic 0 °C ambient sink yields only 67.4% (Phase 5 sensitivity), still 17.6 points short, so no plausible ambient-temperature rival survives.

### Conclusion C8: A single, real, specified grid-scale PTES system (Malta M100) alone already shows the best publicly specified electrical-storage architecture falls well short of 85%

GT-3 (Malta M100 AC-AC RTE 53–65%)
→ comparing GT-3's directly-quoted 53–65% range against the claimed 85% yields a shortfall of 20–32 percentage points for this specific, real, named, grid-scale system — a derived gap figure not itself stated in the source
→ because this is the best publicly specified electrical-storage architecture this research located, and it alone (without needing any corroborating literature) already falls 20+ points short, the 85% claim is unsupported by the single strongest piece of real-world evidence available

**Pre-check:** head GT-3 · ?-marked: none · lowest cited: none · Inputs ceiling: HIGH
**Confidence:** HIGH — GT-3 is read-at-source (Malta spec sheet, page 2 table, quoted directly); the inference is a direct quote-and-compare with no modeling step; the rival "a different architecture might do better" is scoped out — this chain claims only about Malta's own specified figure, not about PTES architectures generally (that broader, more uncertain claim is C2's, which is correctly rated MEDIUM).

### Conclusion C9: Li-ion cell/pack prices alone establish a concrete, verified cost floor the comparison must be measured against

GT-6 (Li-ion pack price $70–108/kWh, 2025)
→ GT-6's two quoted figures — $108/kWh (2025, all applications) and $70/kWh, "45% lower than in 2024" (2025, stationary) — imply a 2024 stationary pack price of $70 ÷ (1 − 0.45) ≈ $127/kWh, a figure not itself stated directly in the source but derivable from it
→ even this pre-2024 cell/pack-level price, let alone the lower 2025 figures, already sits far below current turnkey Li-ion system prices (GT-7?), establishing a verified, independently-derived cost floor the comparison in C4 must be measured against

**Pre-check:** head GT-6 · ?-marked: none · lowest cited: none · Inputs ceiling: HIGH
**Confidence:** HIGH — GT-6 is read-at-source (BNEF press release, two quoted passages); the inference is a direct quote with no modeling step; no rival contests what BNEF itself reported for pack prices.

---

## 5. Abandoned Reasoning

### Dead End: Verifying the DOE SunShot thermal-storage target from a primary energy.gov page

**What was tried:** Two separate WebFetch attempts against distinct energy.gov URLs expected to
host the SunShot CSP thermal-energy-storage cost/RTE targets (the $15/kWh-thermal, ≥93%-RTE
figures underlying GT-12?).

**Why abandoned:** Both URLs returned HTTP 404 Not Found — the source is genuinely unreachable at
the addresses this session located, not merely inconvenient to parse.

**What it ruled out:** Saves a future analyst from re-trying those exact two energy.gov URLs
expecting them to resolve as of 2026-10-08; a current site search on energy.gov (or an
archive.org snapshot) is needed instead. GT-12? remains `?`-marked and MEDIUM-or-lower-only per
the Criterion 3 unreachable-source exception.

### Dead End: Extracting the exact $/kWh-thermal figure from NREL/TP-5500-57625 via pdftotext

**What was tried:** The NREL molten-salt power-tower cost-model report was fetched successfully
and converted to text with `pdftotext`; the text was searched for "Storage Cost per kWht" and
surrounding content.

**Why abandoned:** The report's cost tables lost row/value column alignment during PDF→text
conversion (labels and numeric values appeared in disconnected blocks), so the specific
$22–30/kWh-thermal figure could not be confirmed to the line-item level within this session's
tool budget. This is recorded as GT-5?'s Phase 3 failure record ("citation does not support the
claim") rather than re-attempted with alternate extraction tooling.

**What it ruled out:** Confirms the $22–30/kWh-thermal figure is real-but-unconfirmed-by-this-
analysis, not fabricated — multiple independent secondary sources converge on it — but it also
rules out treating GT-5 as read-at-source; it remains `?` and caps chain C4 at MEDIUM.

### Dead End: Using Malta's 53–65% AC-AC figure alone as the rebuttal, without the Carnot derivation

**What was tried:** Considered whether GT-3 (Malta's demonstrated 53–65% round-trip efficiency)
was sufficient on its own to rebut the claim, without separately deriving the Carnot-bounded
~36% figure for architecture (a).

**Why abandoned:** Malta's architecture (heat-pump charging, separate hot and cold thermal
stores) is not the architecture the claim describes — the claim specifies simple resistive
heating of salt and names no cold store, matching the plain CSP two-tank signature (GT-2) rather
than a PTES spec sheet. Using Malta's figure alone would compare the claim against the wrong
technology and *understate* how far architecture (a) actually misses 85%.

**What it ruled out:** Saves a future analyst from assuming a single demonstrated PTES figure
settles the question for a literal resistive-salt-tank claim; the two architectures require
separate chains (C1 and C2), which is why both exist.

### Dead End: Reinterpreting "cost-competitive" as an LCOS (levelized cost of storage) claim

**What was tried:** Considered whether the cost sub-claim could be rescued by reading
"cost-competitive... same nameplate capacity" as a levelized-cost-of-storage comparison (which
would credit molten salt's very long cycle life and low degradation) rather than an upfront
$/kWh-nameplate comparison.

**Why abandoned:** The claim as given is explicitly framed as a nameplate-capacity $/kWh
comparison (per the task's own framing), not a levelized comparison; pursuing LCOS would answer a
different question than the one posed and was out of scope for this analysis.

**What it ruled out:** Prevents quietly swapping in a more favorable metric (LCOS, where
long-cycle-life thermal tanks might fare better) to rescue a claim that, as literally worded, is
about nameplate $/kWh — this door is left open as a legitimate *follow-on* question, not answered
here.

---

## 6. Conclusion

**Recommended approach:** Reject the claim as stated and replace it with two separately-scoped,
defensible findings: (1) >85% **electricity-to-electricity** round-trip efficiency is not
achievable at 290–565 °C for any architecture consistent with the claim's own wording — real
figures bracket to ~32–39% for a resistive-heated system and 53–65% for the best demonstrated
heat-pump PTES alternative (chain C6); (2) the cost-competitiveness claim is unsupported as
stated because it compares a tank-only thermal $/kWh figure against a turnkey electrical $/kWh
figure on inconsistent accounting bases, and the direction of the true comparison cannot be
confirmed without a power-block/charging-capex figure this analysis could not source (chain C4,
folded into C6).

**Key insight:** The clearest evidence of conflation is not external — it is internal to a single
vendor's own numbers. The identical Malta PHES hardware reports round-trip efficiency figures
ranging from ~55–60% (power-to-power) to 85–95% (cogeneration) to 96% (power-to-heat only),
depending entirely on how much of the output is counted as re-electrified versus retained as
heat (chain C3). An 85% figure is therefore not an error or a fabrication — it is a real,
precedented number for a different, non-electrical accounting basis, relabeled as if it answered
the electrical question the claim actually asks.

**Trade-offs acknowledged:** Accepting this verdict means accepting that molten-salt thermal
storage's genuine strengths — very low $/kWh-thermal, long cycle life, no exotic materials, and
strong cogeneration economics — are real and valuable (chain C3, C4), but they are not evidence
that the technology is a drop-in battery replacement at small (5 MWh), standalone,
electricity-only scale under nameplate accounting (chain C4, C6). The cost finding in particular
is deliberately left as "unsupported/likely unfavorable" rather than "disproven" — overclaiming a
clean cost win the evidence does not support would repeat, in the opposite direction, the exact
error this analysis identifies in the original claim.

**Pre-check:** head C1 (MEDIUM), C2 (MEDIUM), C3 (MEDIUM), C4 (MEDIUM), C6 (MEDIUM) · ?-marked: none · lowest cited: MEDIUM · Inputs ceiling: MEDIUM
**Confidence:** MEDIUM — every contributing chain is MEDIUM, driven by `?`-marked ground truths
GT-4?, GT-5?, GT-7?, GT-8?, GT-11?, GT-12?, each with a named verification path in its own
chain's confidence line above. No chain here is LOW, and the headline thermodynamic finding
(C1/C2/C6) is robust to its one unverified input (GT-11?) under the sensitivity check in the
adversarial pass below — the cost finding (C4) is the more genuinely uncertain half of this
verdict and is stated with correspondingly more hedged language above.


---
---

## §6→§4 closure ledger (process output)

- "Reject the claim as stated and replace it with two separately-scoped, defensible findings... (1) ...(chain C6)" → chain C6 ✓
- "(2) the cost-competitiveness claim is unsupported as stated... (chain C4, folded into C6)" → chain C4 ✓
- "Key insight: ...the identical Malta PHES hardware reports round-trip efficiency figures ranging from ~55–60%... (chain C3)" → chain C3 ✓
- "Trade-offs acknowledged: ...are real and valuable (chain C3, C4), but they are not evidence... (chain C4, C6)" → chains C3, C4, C6 ✓
- "Confidence: MEDIUM — every contributing chain is MEDIUM..." → chains C1, C2, C3, C4, C6 ✓ (D-07 enumeration)

All five Conclusion-section claims cite a chain inline; no claim required cut.

## Techniques not applied (process output)

- fishbone — not applicable — the assumption space is narrow and fully enumerable from the
  claim's own three named sub-claims (thermodynamic, cost, provenance/architecture) without
  needing a breadth-first category brainstorm; the Phase 2 inversion pass was sufficient to
  surface the load-bearing preconditions.
- pre-mortem — not applicable — this analysis's conclusion is a claim (a verdict on a physical
  and economic assertion), not a plan or recommendation to execute; per the pre-mortem/inversion
  decision rule, inversion is used instead, applied at both Phase 2 (on the original claim) and
  Phase 5 (on this analysis's own headline conclusion, below).
- trade-off — not applicable — no two-or-more viable options survive the ground truths as a
  "which option should we choose" decision; the task is to verify a single stated claim, not
  select among alternatives, so the weighted-criteria procedure has no decision to score.
- five-whys, causal mode — not applicable — this analysis is not diagnosing why a past
  event/symptom occurred; it evaluates whether a forward-looking technical/economic assertion is
  defensible. (Five-whys *reduce-to-primitives* mode was applied informally in Phase 3's
  irreducibility test for GT-1 and GT-9, both of which bottom out at physical law.)

## Assumption Audit scan (process output)

| Chain | Step | Step Text (brief) | Assumption surfaced? | Added to Table? |
|-------|------|--------------------|-----------------------|------------------|
| C1 | 1 | Carnot ceiling (62.4%) × real-cycle fraction → discharge-leg bracket 34–41% | none | n/a |
| C1 | 2 | charging × storage retention × discharge bracket → round-trip 32–39%, central 36% | A-9 (storage retention ~95–99%) | yes — already present (pre-added at Phase 2); step marked `[Assumes: A-9]` |
| C1 | 3 | 36% central vs. 85% claimed → thermodynamic premise fails for architecture (a) | none | n/a |
| C2 | 1 | PTES systems built for electrical RTE cluster at 53–65% | none | n/a |
| C2 | 2 | none reach 85%; best architecture still falls short | none | n/a |
| C3 | 1 | Malta figures swing 55–60% / 85–95% / 96% by accounting basis | none | n/a |
| C3 | 2 | DOE's 93% RTE target is thermal, paired with $/kWh-thermal | none | n/a |
| C3 | 3 | 85% real under heat/cogen accounting; conflates with the 36% electrical figure | none | n/a |
| C4 | 1 | tank cost ÷ RTE bracket → $56–94/kWh usable-electric-equivalent | none | n/a |
| C4 | 2 | excludes power-block/charging capex, scale-resistant at 5 MWh | A-8 (no diseconomy-of-scale penalty) | yes — already present (pre-added at Phase 2); step marked `[Assumes: A-8]` |
| C4 | 3 | power-block capex unsourced → cost claim unsupported, not disproven | none | n/a |
| C5 | 1 | actor lens: developers need more charging electricity; competitors gain credibility | none | n/a |
| C5 | 2 | time (near-term): financing covenants exposed at first commissioning | A-10 (financing embeds vendor figures) | yes — already present (pre-added at Phase 2); step marked `[Assumes: A-10]` |
| C5 | 3 | time (long-term): credibility damage chills future investment | none | n/a |
| C6 | 1 | every architecture consistent with the claim tops out 36–65%, never 85% | none | n/a |
| C6 | 2 | 85% real only under heat/cogen accounting; cost inherits the same error | none | n/a |
| C6 | 3 | claim not defensible on either leg; borrows battery vocabulary without the accounting it needs | none | n/a |
| C7 | 1 | GT-1 + GT-10 + GT-2 → Carnot ceiling = 62.4% for the discharge leg alone | none | n/a |
| C7 | 2 | GT-9's ≤100% charging cap means round trip cannot exceed the discharge leg's own ceiling | none | n/a |
| C7 | 3 | 62.4% hard bound sits 22.6 points below the claimed 85%, refuting the claim via physical law alone | none | n/a |
| C8 | 1 | Malta's own spec states 53–65% AC-AC RTE, independent of corroborating literature | none | n/a |
| C8 | 2 | this single demonstrated figure alone already falls 20–32 points short of 85% | none | n/a |
| C9 | 1 | BNEF 2025 figures establish Li-ion pack prices at $70–108/kWh | none | n/a |
| C9 | 2 | any cost-competitive claim must beat this pack-level floor before adding turnkey-system premium | none | n/a |

All three `[Assumes: X]`-marked steps reference assumptions that were already present in the
Classified Assumptions Table (A-8, A-9, A-10 were anticipated during Phase 2 construction,
precisely because the Phase-2 inversion pass had already identified the storage-retention,
scale-diseconomy, and financing-practice preconditions as load-bearing). No chain step surfaced a
genuinely new, previously-uncaptured assumption — a clean audit result, not a skipped one.


## Self-audit scan (process output)

| Chain | Chain Head (brief) | Form conforming? | Rule applied | Dependency clean? | Band | Act attempted? | Edges fired |
|-------|---------------------|-------------------|---------------|--------------------|------|-----------------|-------------|
| C1 | GT-1 + GT-10 + GT-11? + GT-9 | yes | n/a | yes | MEDIUM | yes | none |
| C2 | GT-3 + GT-8? | yes | n/a | yes | MEDIUM | yes | none |
| C3 | GT-4? + GT-12? + C1 (MEDIUM) | yes | n/a | yes | MEDIUM | yes | none |
| C4 | GT-5? + C1 (MEDIUM) + GT-7? | yes | n/a | yes | MEDIUM | yes | none |
| C5 | C1 (MEDIUM) + C4 (MEDIUM) | yes | n/a | yes | MEDIUM | no | none |
| C6 | C1 (MEDIUM) + C2 (MEDIUM) + C3 (MEDIUM) + C4 (MEDIUM) | yes | n/a | yes | MEDIUM | no | none |
| C7 | GT-1 + GT-2 + GT-9 + GT-10 | yes | n/a | yes | HIGH | yes | none |
| C8 | GT-3 | yes | n/a | yes | HIGH | yes | none |
| C9 | GT-6 | yes | n/a | yes | HIGH | yes | none |

| §6 Span (brief) | Construct | Claim under R11? | R11 clause applied | Chain cited |
|-------------------|-----------|-------------------|----------------------|---------------|
| "Recommended approach: Reject the claim..." | bold lead-in | yes | bold lead-in whose colon closes the bold span, carrying its assertion on the same line | C6, C4 |
| "Key insight: The clearest evidence of conflation..." | bold lead-in | yes | bold lead-in whose colon closes the bold span | C3 |
| "Trade-offs acknowledged: Accepting this verdict means..." | bold lead-in | yes | bold lead-in whose colon closes the bold span | C3, C4, C6 |
| "Pre-check: head C1 (MEDIUM), C2 (MEDIUM)..." | bold lead-in | yes | pre-check line is itself a Conclusion-section claim under the Claim inventory rule | C1, C2, C3, C4, C6 |
| "Confidence: MEDIUM — every contributing chain..." | bold lead-in | yes | bold lead-in whose colon closes the bold span | C1, C2, C3, C4, C6 |

Scan complete: 9 chain rows, one per section-4 chain block in order; 5 section-6 rows, one per
construct in order — 5 claims under R11, 0 excluded. 0 chains malformed, 0 claims untraced.


## Adversarial pass (process output)

**Technique:** Inversion, applied to this analysis's own headline conclusion (C6) — per the
inversion/pre-mortem decision rule, inversion stress-tests a *claim* and this analysis's
conclusion is a claim/verdict, not an executable plan.

**Recompute.** Carnot ceiling: 1 − 315.15 K / 838.15 K = 0.6240 → **62.4%** (matches C1).
Round-trip bracket: lower 0.98 × 0.95 × 0.3432 = 0.3195 → **32.0%**; upper 0.98 × 0.99 × 0.4056 =
0.3934 → **39.3%**; central 0.98 × 0.97 × 0.3744 = 0.3558 → **35.6%** (matches C1's "32–39%,
central ≈36%"). Cost conversion: $22 ÷ 0.3934 = **$55.9/kWh**; $30 ÷ 0.3195 = **$93.9/kWh**
(matches C4's "$56–94/kWh"). All three recomputed figures match the chain text independently.

**Sensitivity.** The single most sensitive input to C1 is GT-11? (real-cycle fraction of
Carnot). Tested at its most favorable extreme (95% of Carnot, well above any publicly documented
steam-cycle performance): discharge efficiency rises to 59.3%, and round-trip rises to only
≈56.4% — still 29 points short of 85%. Tested jointly with an unrealistically cold 0 °C ambient
sink (GT-10 replaced, raising the Carnot ceiling to 67.4%): round-trip rises to ≈61.8% — still
23 points short. **No single `?`-marked ground truth, even pushed to its most favorable
plausible extreme, flips C1's qualitative conclusion.** For C4 (cost), the sensitive inputs are
GT-5? and GT-7? jointly with the unsourced power-block capex figure (named explicitly in C4's
confidence line) — this is the one place in the analysis where plausible evidence could change
the conclusion's direction, and it is disclosed as such rather than resolved.

**Rival.** Headline (C6): strongest rival is "the claim is defensible under a convention this
analysis hasn't considered" — ruled out by C3, which shows the same vendor's own numbers exhibit
the conflation mechanism directly, and by A-1 (the claim's own wording forces the electrical
reading; Li-ion has no thermal nameplate to compare against). C1: rival "a more advanced cycle
closes the gap to 85%" — ruled out by the Sensitivity computation above. C2: candidate rival "an undisclosed/future PTES architecture could reach 85%" — this contests only a broader claim ('no architecture could ever reach 85%') that C2 does not make; C2's actual endpoint is scoped to demonstrated efficiency ("tops out at 53-65%"), which the candidate rival does not contest, so it is not live against C2's endpoint as stated — the broader open question is acknowledged in C2's confidence line as out-of-scope-for-this-chain, consistent with the architecture-c ideal bound being flagged model-dependent in §4. C3: no live
rival — this chain itself resolves an apparent contradiction rather than asserting a contestable
claim. C4: rival "utility-scale (100+ MWh) molten salt genuinely is cost-competitive with
Li-ion" — plausibly true, but ruled **out of scope** rather than false: the claim under test
specifies 5 MWh nameplate, and C4's verdict is scoped accordingly (see Abandoned Reasoning,
Dead End 3, for the related LCOS-reframing deflection, which was also ruled out of scope).

**Premise.** This analysis's own verdict — that the claim is thermodynamically false for its
stated architecture and cost-unsupported as worded — has already been shown wrong. What caused
that?

**Causes (unfiltered, generated from three stakeholder viewpoints before grouping):**
1. (vendor) The ambient heat-rejection temperature used in the Carnot calculation is wrong — the
   real plant might use much colder cooling water, raising the true ceiling.
2. (vendor) The architecture is secretly heat-pump-based despite the claim's "resistively heats"
   wording, and real engineering achieves more than credited.
3. (engineer) GT-11?'s 55–65%-of-Carnot bracket is too conservative; advanced reheat/regenerative
   or sCO2 topping cycles could reach much closer to Carnot.
4. (engineer) A-9's storage-retention assumption is wrong in the *pessimistic* direction — actual
   per-cycle losses are larger than 1–5%, which would make the already-low estimate even lower.
5. (financial analyst) GT-5?'s $22–30/kWh-thermal figure is stale and real modern costs are much
   lower, while real-world (non-global-average) Li-ion system costs are higher than GT-7?'s
   figures suggest.
6. (financial analyst) The missing power-block/charging capex, once sourced, turns out small
   relative to tank cost even at 5 MWh scale, rescuing the cost comparison.
7. (vendor) "Nameplate capacity" was always meant loosely/thermally in industry marketing
   convention, and no reader is meant to take the electrical reading literally.

**Clusters, chain/GT ids borne on, and disposition:**
- **Cluster A — physical-bound miscalibration** (causes 1–3; bears on C1, C2, GT-10, GT-11?):
  fatal-if-true for C1's specific bracket, but the Sensitivity computation above shows that even
  generous, implausible substitutions on these exact inputs do not flip the qualitative verdict.
  **Disposition:** no plan change required; the sensitivity computation is reported explicitly in
  C1's confidence line and this record as the mitigation.
- **Cluster B — estimate-direction errors that would not rescue the claim** (cause 4; bears on
  A-9, C1): if true, strengthens rather than weakens the conclusion. **Disposition:** accepted
  explicitly as a low-risk-to-conclusion possibility; no action needed.
- **Cluster C — cost-side evidence gaps that could flip C4** (causes 5–6; bears on GT-5?, GT-7?,
  C4): the one cluster that is genuinely costly-but-survivable to this analysis's cost verdict.
  **Disposition:** explicitly accepted as an open risk, not resolved; named mitigation already
  present in C4's confidence line (re-extract the NREL cost table with a layout-preserving tool;
  source a specific small-scale power-block $/kW figure; open a primary BNEF/Wood Mackenzie
  system-price report) — this is why C4 and C6 are capped at MEDIUM and the Conclusion states
  the cost finding as "unsupported," not "disproven."
- **Cluster D — rhetorical defense not touching the technical finding** (cause 7; bears on A-1,
  C3): tolerable, not fatal. **Disposition:** explicitly rejected as a defense of the claim *as
  worded* — the claim's own text specifies an electrical round trip, and the literal-wording
  reading (A-1) is retained; no plan change, stated explicitly in the Conclusion's "Trade-offs
  acknowledged."

**Falsification.** This analysis's conclusion is false if a specific, named, grid-connected
molten-salt (or equivalent sensible-heat) thermal storage system in the 290–565 °C range is
demonstrated with third-party-measured AC-to-AC round-trip efficiency ≥80% at any scale, OR if an
apples-to-apples (same accounting basis, same system scope) installed-cost comparison shows a
5 MWh-nameplate thermal-electric storage system at or below current turnkey Li-ion $/kWh prices.


## Self-Audit Gate (process output)

**Criterion 1: Identify Essence**
Quoted span: "Does the specific bundled claim... survive first-principles thermodynamic and cost
scrutiny, or does it conflate heat-storage efficiency/cost... with battery-equivalent
electrical-storage efficiency/cost... the claim's own wording asserts but does not deliver?"
Band: **Rigorous**
Justification: The statement names the real underlying question (a conflation test, not a
restatement of the prompt), each of the three success criteria is a verb+subject+outcome
triplet checkable directly against the Conclusion section without further interpretation, and
the statement is specific to this exact claim (the 290–565 °C / 5 MWh / 85% figures), not a
generic template sentence reusable for a different analysis.

**Criterion 2: Challenge Assumptions**
Quoted span (Assumption Audit scan): "All three `[Assumes: X]`-marked steps reference
assumptions that were already present in the Classified Assumptions Table... No chain step
surfaced a genuinely new, previously-uncaptured assumption — a clean audit result, not a
skipped one."
Band: **Rigorous**
Justification: All 10 rows use the four-type scheme exactly; every Verdict cell is a
token-plus-em-dash with a specific justification; at least seven of ten rows are Challenge, not
merely Accept; every assumption used in a chain (A-8, A-9, A-10) carries "unverified — flagged"
in its Verification cell; and the Assumption Audit scan — confirmed present and exhaustive
(24 rows, one per chain step across C1–C9, no step skipped) — found no undeclared assumption,
satisfying the audit-exhaustiveness check this criterion requires before scoring.

**Criterion 3: Establish Ground Truths**
Quoted span: "?-marked: GT-4, GT-5, GT-7, GT-8, GT-11, GT-12 (6 of 12)... Read-at-source: GT-2...
GT-3... GT-6... GT-10... GT-1, GT-9 — physical law, verified by derivation."
Band: **Rigorous**
Justification: Checking the enumeration against the list (not merely quoting it): GT-4, GT-5,
GT-7, GT-8, GT-11, GT-12 are the only six IDs carrying `?` in the Ground Truths section, so the
enumeration matches exactly. Every unsuffixed, reachable-source GT (GT-1, GT-2, GT-3, GT-6,
GT-9, GT-10) now feeds at least one HIGH-confidence chain (C7 consumes GT-1/GT-2/GT-9/GT-10; C8
consumes GT-3; C9 consumes GT-6) — the Rigorous requirement this criterion is strictest about.
GT-5? and GT-12? carry explicit Phase 3 failure records naming the source and the unreachable/
not-located reason, satisfying the unreachable-source exception for the two GTs that remain
`?`-marked despite an attempted read. No assumption carrying a Discard verdict appears in this
list (none was discarded in Phase 2).

**Criterion 4: Reason Upward**
Quoted span (Self-audit scan, chain-form table): "C7 | GT-1 + GT-2 + GT-9 + GT-10 | yes | n/a |
yes | HIGH | yes | none" and seven further rows (C1–C6, C8, C9) each reading `Form conforming? =
yes`, `Dependency clean? = yes`.
Band: **Rigorous**
Justification: All nine chains in the self-audit scan's chain-form table read `yes` on both
`Form conforming?` and `Dependency clean?`, with no `unreached` or `no` cell; every chain has at
least one genuine intermediate (verified by direct inspection: C8 and C9, the two-hop chains,
were each revised during drafting specifically so their first hop states a derived quantity —
C8's percentage-point gap, C9's implied-2024-price — not a restatement of their single head
input); the Abandoned Reasoning section documents four dead ends, each with a specific
structural reason (unreachable source, lost PDF table alignment, architecture mismatch,
out-of-scope reframing) rather than a vague one; no analogy is used as direct evidence (every
comparison — Malta, Echogen, Solar Two — is grounded in a named, cited GT about that specific
situation); and every surfaced assumption on a chain step carries an inline `[Assumes: X]` mark
(A-8, A-9, A-10).

**Criterion 5: Validate**
Quoted span: "No single `?`-marked ground truth, even pushed to its most favorable plausible
extreme, flips C1's qualitative conclusion" (Adversarial pass, Sensitivity) and "each cluster
carrying a named plan change or an explicitly accepted risk with a named mitigation" (Clusters
A–D, each with a Disposition).
Band: **Rigorous**
Justification: Every chain's confidence line names its weakest link and, for each `[Assumes:
X]`-marked hop, states explicitly what happens to the endpoint if that assumption fails (A-9 in
C1, A-8 in C4, A-10 in C5) — satisfying the Inference-axis pricing requirement rather than
leaving it implicit; D-07 is satisfied throughout (no chain consuming a `GT-N?` input is rated
HIGH; every chain is rated no higher than the lowest-rated chain its own head cites — C3/C4 cite
C1 at MEDIUM and are themselves MEDIUM, C5 cites C1+C4 and is MEDIUM, C6 cites C1–C4 and is
MEDIUM; C7/C8/C9 cite only unsuffixed GTs and are correctly HIGH); the Rivals axis is
explicitly addressed per chain (C1's and C2's candidate rivals are each shown not to contest the
chain's own, correctly-scoped endpoint; C4's utility-scale rival is ruled out-of-scope rather
than ignored); the adversarial pass record is complete — Recompute, Sensitivity, Rival, Premise,
Causes, Clusters, Disposition, and Falsification are all present with substantive content, and
all four clusters (A–D) carry either a named plan change/mitigation or an explicit
accepted-risk disposition, not a bare risk list.

**Criterion 6: Conclusion-to-Ground-Truth Traceability**
Quoted span (Self-audit scan, claim-inventory table): `"Recommended approach: Reject the
claim..." | bold lead-in | yes | bold lead-in whose colon closes the bold span... | C6, C4` and
four further rows, each with a non-empty `Chain cited` value and no row reading `none —
untraced`.
Band: **Rigorous**
Justification: All five §6 constructs (Recommended approach, Key insight, Trade-offs
acknowledged, Pre-check, Confidence) trace to a specific named chain with no untraced row; the
§6→§4 closure ledger independently confirms the same five claims are discharged inline, not by
ledger-only marker; the Conclusion section introduces no reasoning absent from section 4 (every
sentence restates or synthesizes a chain already derived); and the Key Insight — that a single
vendor's own numbers (55–60% vs. 85–95% vs. 96%, chain C3) demonstrate the conflation mechanism
directly — is a non-obvious finding reasoning-by-analogy would not surface, not a restatement of
the Recommended Approach.

**Gate result:** 0 criteria Absent; 0 criteria Hand-wavy. Both pass conditions are met — the
gate clears without requiring a Fix/Repeat pass, and no re-entry edge fired.

