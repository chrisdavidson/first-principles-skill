## Answer

**Recommendation:** Use molten-salt TES only where a genuine thermal end-use can consume the stored heat directly, and use Li-ion for any electricity-shifting need at this 5 MWh scale — do not pair this TES with a small power block as an electricity-storage product (chain C10). A composite (TES-for-heat plus Li-ion-for-electricity) scores marginally highest in the formal trade-off, but the margin is thin and Li-ion-alone is the safer default (chain C10).

**Band (from §6):** LOW

**Would change it:** Vendor quotes for the heat exchanger, pumps and valves (chain C4), and pinning down the system's actual discharge-duration/power rating rather than the 4-hour assumption used throughout (chain C9).
## 1. Problem Essence

**Essence Statement:** What does a 5 MWh two-tank molten-salt thermal energy storage (TES) system cost per kWh of capacity when its capital cost is rebuilt bottom-up from constituent unit costs (salt, tanks, heat exchanger, pumps/piping/trace heating, BOP/EPC), what does that capital cost become per kWh *delivered* once amortised over a realistic cycle life with round-trip efficiency and O&M folded in, and — on that $/kWh-delivered basis — is it cost-competitive with lithium-ion, with the thermal-vs-electrical end-use distinction made explicit rather than assumed away?

This is not simply "is TES cheap" — the triggering curiosity is a single oft-quoted industry figure (~$20–40/kWh-th for molten-salt TES) that is almost always quoted at GWh utility-CSP scale. The real question is whether that figure, or anything near it, survives being rebuilt from first principles at a 5 MWh scale, and whether "cost-competitive with Li-ion" even means the same thing once the end-use (heat vs. electricity) is pinned down.

**Success criteria** — a correct answer must:
1. Produce a $/kWh capital-cost figure for the 5 MWh system that is traceable, line by line, to the 5 MWh spec, a stated ΔT, and explicit unit costs — not asserted from a single industry source.
2. Produce a $/kWh-*delivered* (LCOS-style) figure that accounts for cycle life, cycles/year, round-trip efficiency, and O&M — not capital cost alone.
3. State explicitly what the Li-ion comparison basis is (thermal output vs. electrical output) and show, quantitatively, how the competitiveness verdict changes depending on which basis is used — including the case where a power block is added so the comparison is electricity-to-electricity.
4. Not force the answer into "TES wins" or "Li-ion wins" as a single verdict — the success criterion is a correctly *scoped* verdict (competitive for X, not for Y), not a pick of exactly one of the two named technologies. A composite answer (each technology used where its physics favours it) is in scope if the ground truths support it.
5. Name the assumptions whose plausible variation would flip the verdict, not just report a point estimate.

## 2. Assumptions Table

**Assumption-space generation.** The unit-cost space here is wide (a dozen+ independent cost line items), so a fishbone pass (default six-category set: People / Process / Technology & Tools / Environment / Information / Resources) was used to brainstorm categories of risk before drafting the table, and an inversion pass was used specifically against the headline claim "molten-salt TES at 5 MWh is cost-competitive with Li-ion for electricity storage" to surface the preconditions that claim silently depends on.

*Fishbone category scan (brief):* **Process** → discharge-duration choice, cycles/year, design life. **Technology & Tools** → salt chemistry, tank materials, power-block technology choice. **Environment** → ambient temperature, commodity price volatility, discount rate. **Information** → unsourced small-scale unit costs, vintage of Li-ion benchmark data. **Resources** → salt/steel price levels, availability of economies of scale. **People** → niche molten-salt fabrication/EPC labor availability for a one-off small project. Each branch below is tagged with its category in brackets.

*Inversion scan (brief):* inverting "TES+power-block is competitive with Li-ion for electricity," the necessary preconditions whose failure would guarantee that claim false are: (i) small-scale power-block efficiency stays well below Carnot [load-bearing], (ii) small-scale power-block capital cost stays high per kW [load-bearing], (iii) TES fixed costs (HX/pumps/controls) don't scale down with energy capacity [load-bearing], (iv) Li-ion capital costs stay in the $130–300/kWh region rather than spiking upward [load-bearing]. All four are carried into the table below (A-11, A-12, A-5/A-4, A-13) and checked in Phase 4/5.

| # | Assumption | Type | Treatment | Verdict | Verification |
|---|---|---|---|---|---|
| A-1 | Solar-salt operating window ≈ 290°C (cold) / 565°C (hot), ΔT≈275°C [Technology & Tools] | Convention | Challenged: holds for solar salt (NaNO₃/KNO₃) specifically, not other salt chemistries; within its known freeze point (~220°C) and thermal-decomposition ceiling (~600°C) | Accepted for solar salt as specified | Corroborated by GT-3? (unverified, consistent across sources) |
| A-2 | Solar-salt cp=1.50 kJ/kg·K, ρ=1870 kg/m³ [Information] | Untested belief | Flagged unverified; primary source (PMC6041306) blocked by reCAPTCHA | Used with `?` flag | GT-1?, GT-2? — Phase 3 failure record below |
| A-3 | +15% salt mass margin (heel/ullage) [Technology & Tools] | Untested belief | Engineering-judgment default; not independently sourced | Used with `?` flag, low leverage on conclusion (small $ impact) | Unverified |
| A-4 | Discharge duration = 4 h → thermal power = 1.25 MWth [Process] | Convention (arbitrary design choice — not fixed by the 5 MWh spec) | **Challenged explicitly** — this is the single largest swing variable: HX/pump/piping/power-block costs scale with power (kW), not energy (kWh), so duration choice directly moves $/kWh | Accepted as a stated, clearly-flagged design choice, not a given fact — flagged `[Assumes: A-4]` wherever a chain depends on it | Unverified by nature (a choice, not a measurement) — sensitivity run in Phase 5 |
| A-5 | Fabricated unit costs: carbon steel ≈$4/kg, refractory ≈$1,000/m³, insulation ≈$200/m², HX ≈$200/kWth, pumps ≈$60k each, piping ≈$1,100/m, valves ≈$7k each [Information/Resources] | Untested belief | Bracketed ±30–40% (estimate technique); not individually sourced this session | Used with `?` flag on every line item; aggregate cross-checked against literature benchmarks in Phase 5 | Unverified — GT-10? through GT-16? |
| A-6 | EPC markup 20%, contingency 15% [People/Process] | Convention | Challenged: first-of-kind small specialty system could plausibly carry 25–30%; used as stated with sensitivity noted | Accepted with ±10–15% sensitivity band | Unverified (industry-typical range, not individually cited) |
| A-7 | 1 cycle/day, 350 op-days/yr, 25-yr design life [Process] | Current constraint, physically grounded | Thermal/mechanical (not electrochemical) degradation genuinely supports multi-decade life; expiry condition: would shorten if daily ΔT cycling induces refractory spalling or tank fatigue faster than CSP experience suggests | Accepted — backed by CSP operating history (Gemasolar/Andasol >10 yr daily cycling) | Reported-by-delegate (not opened directly this session) — treated as reasonably solid |
| A-8 | Discount rate 7% for capital recovery [Environment] | Convention | Challenged: plausible range 5–10%; moves annualized capital cost mildly | Accepted with sensitivity noted | Unverified (typical infrastructure WACC) |
| A-9 | O&M ≈2% of CAPEX/yr + parasitic pump/trace-heat electricity at $0.08/kWh [Information/Environment] | Untested belief | Estimated bottom-up from assumed pump/heater ratings and run-hours | Used with `?` flag | Unverified |
| A-10 | Thermal round-trip efficiency ≈94% at 5 MWh scale, from conductive heat-loss through 300 mm mineral-wool insulation (k≈0.08 W/m·K) at ΔT_ambient | Physical law (mechanism) + untested belief (numeric inputs) | Mechanism (Fourier conduction) accepted as physical law; specific insulation thickness/conductivity values flagged unverified | Mechanism accepted; numeric result carries `?` | Reduce-to-primitives drill below (Phase 3) |
| A-11 | Power-block (small ORC) electrical efficiency 18–26%, central 22% [Technology & Tools] | Untested belief, convention-adjacent | Cross-checked against Carnot ceiling (64.4%) and small-ORC techno-economic literature | Used with `?` flag; load-bearing per inversion scan | GT-17? |
| A-12 | Power-block installed cost $1,800–3,200/kW, central $2,400/kW [Resources] | Untested belief | Scaled informally from 2–50 kWe literature data points up to 275 kWe; not a regression | Used with `?` flag; load-bearing per inversion scan | GT-18? |
| A-13 | Li-ion comparison basis: Lazard LCOS v7.0 (2021) direct figures + 2024–2026 secondary reporting [Information] | Current constraint | Expiry condition: superseded by any newer Lazard LCOS edition or NREL ATB release (≈annual cadence); figures already shown moving upward since 2021 | Accepted as best-available, vintage-flagged | GT-5 (read-at-source) / GT-6? (reported-by-delegate) |
| A-14 | Unit-basis discipline: 5,000 kWh is thermal (kWh-th); Li-ion figures are electrical (kWh-e) — the two are not interchangeable without a stated conversion | Convention (declared scope boundary) | Challenged throughout — this is the crux of the whole apples-to-oranges question | Accepted as the organizing constraint of the entire analysis | N/A — definitional |

**Phase 3 failure record (forward reference):** Attempted read of `pmc.ncbi.nlm.nih.gov/articles/PMC6041306` for solar-salt cp/density — blocked by reCAPTCHA (source unreachable). GT-1/GT-2 carry `?` as a result; see Ground Truths section.

## 3. Ground Truths

**Irreducibility drill (reduce-to-primitives mode), applied to the two claims the whole cost build rests on:**

*Claim A: "Stored sensible heat energy = mass × specific heat × ΔT."* Constituents: (1) definition of specific heat capacity (a material property relating heat input to temperature rise at constant pressure — a textbook thermodynamic definition, not itself reducible further) → **verified, definition**. (2) mass and ΔT are design choices/measurements, not further reducible. (3) the assumption that no phase change occurs across the ΔT window (salt stays liquid 290–565°C, between its melting point 220°C and decomposition ceiling ~600°C) → reducible to GT-4/GT-3, which are read-at-source. All branches bottom out at a definition or a sourced measurement → **Claim A verified**.

*Claim B: "Round-trip efficiency loss ≈ conductive heat loss through tank insulation."* Constituents: (1) Fourier's law of heat conduction, Q̇=U·A·ΔT — a physical law, irreducible → **verified, physical law**. (2) insulation thermal conductivity k≈0.08 W/m·K at mean operating temperature, insulation thickness 0.3 m, tank external area ≈56.7 m² per tank, ambient temperature 25°C — these are engineering estimates, not independently sourced this session → **flagged `?`, carried as GT-10?-adjacent inputs** (folded into the RTE derivation in Phase 4 rather than given a separate GT-ID, since they are inputs to a chain step, not standalone facts).

**Ground Truths list:**

| ID | Fact | Provenance | Source / read-location |
|---|---|---|---|
| GT-1 | Solar salt (NaNO₃/KNO₃, "baseline") specific heat capacity = 1.5 J/g·K = 1.50 kJ/kg·K (liquid) | read-at-source | Gomez-Vidal & Kruizenga (NREL/SNL), *CSP Gen 3 Roadmap — Molten Salt Pathway*, DOE SunShot, Feb 2017 — slide "Technology Gap – Salt Chemistry," table "Candidate MS–HTFs (SunShot goal = 15 $/kWhth)," row "NaNO₃ KNO₃ (baseline)," column "Heat Capacity, J/g-K" = 1.5 |
| GT-2 | Solar salt density (liquid, tank-relevant) = 1.7 kg/L = 1,700 kg/m³ | read-at-source | Same source/table, column "Density, Tank kg/L" = 1.7 (supersedes an earlier, unverified 1,870 kg/m³ figure drawn from a WebSearch snippet — the directly-read DOE figure governs) |
| GT-3 | Solar-salt CSP operating window: Hot Tank 585°C (or 565°C baseline variant elsewhere in the same deck), Cold Tank 290°C | read-at-source | Same source, slide "State-of-the-Art Molten Salt Technology" ("Hot Tank = 585°C"; "Cold Tank = 290°C") and slide 33/"Baseline (solar salt at 565°C)" callout |
| GT-4 | Solar salt melting/freezing point = 220°C | read-at-source | Same source/table, column "Melting Point (°C)" = 220, row "NaNO₃ KNO₃ (baseline)" |
| GT-5 | Lazard *Levelized Cost of Storage, v7.0* (2021), 100 MW/400 MWh (4-hr) Wholesale Standalone Li-ion: Initial Capital Cost (DC) $147–231/kWh; O&M $1.5–2.5/kWh-yr; Efficiency of Storage Technology 84–91%; LCOS (Energy) $131–232/MWh | read-at-source | lazard.com, "Levelized Cost of Storage Version 7.0" PDF, fetched and text-extracted directly (pdftotext); rows "Initial Capital Cost—DC," "O&M," "Efficiency of Storage Technology," "Levelized Cost of Storage," column "(100 MW / 400 MWh)" in the cross-technology comparison table |
| GT-6? | Lazard LCOS, most recent vintage (~v11, 2025/2026): 100 MW/4-hr standalone Li-ion LCOS risen to ≈$210–292/MWh (unsubsidized), attributed to tariffs/FEOC restrictions on Chinese cells; other 2025 reporting cites $115–254/MWh without ITC / $83–192/MWh with ITC | reported-by-delegate | WebSearch summaries of energy-storage.news coverage of Lazard LCOS v11; direct fetch attempted and failed — **Phase 3 failure record:** `energy-storage.news` article → HTTP 403 Forbidden |
| GT-7? | Historical two-tank molten-salt TES specific capital cost ≈$30–40/kWh-th (2004-era utility/CSP-scale study) | reported-by-delegate | WebSearch summary citing a 2004 energy-economics study; not opened directly this session |
| GT-8? | A chloride-based alternative sensible-heat salt mixture (NaKMg–Cl) reported storage-media cost ≈$4.95/kWh-th | reported-by-delegate | WebSearch summary of a recent (2023–2024) research paper; not opened directly this session |
| GT-9 | 5,000 kWh_th is the declared design storage capacity | definitional | Problem statement (not an external citation) |
| GT-10? | Fabricated carbon-steel vessel, installed, ≈$3.5–5/kg (central $4/kg) | untested belief / engineering estimate | Not sourced this session — generic industrial cost-estimating judgment, bracketed, no citation attempted |
| GT-11? | High-temperature castable refractory lining, installed, ≈$800–1,200/m³ (central $1,000/m³) | untested belief / engineering estimate | Not sourced this session |
| GT-12? | External mineral-wool/calcium-silicate insulation, installed, ≈$150–250/m² (central $200/m²) | untested belief / engineering estimate | Not sourced this session |
| GT-13? | Salt-to-working-fluid heat exchanger, corrosion-resistant, installed, ≈$150–300/kW-th (central $200/kW-th) | untested belief / engineering estimate | **Phase 3 failure record:** searched for a published $/kW figure for molten-salt shell-and-tube HX cost; sources discuss design/corrosion challenges but no commercial $/kW figure was found in accessible results — bracket retained, unverified |
| GT-14? | Molten-salt vertical cantilever pump, hot-service, installed, ≈$40,000–80,000 each at this small scale (central $60,000) | untested belief / engineering estimate | Not sourced this session |
| GT-15? | Specialty high-temperature trace-heated piping, installed, ≈$800–1,500/m (central $1,100/m) | untested belief / engineering estimate | Not sourced this session |
| GT-16? | High-temperature isolation/control valves, installed, ≈$5,000–10,000 each (central $7,000) | untested belief / engineering estimate | Not sourced this session |
| GT-17? | Small-scale (sub-500 kWe) ORC power-block thermal-to-electric efficiency ≈18–26% (central 22%) | reported-by-delegate / partially unverified | **Phase 3 failure record:** MDPI "Small Scale Organic Rankine Cycle: A Techno-Economic Review" fetch → HTTP 403 Forbidden; figure instead inferred from WebSearch summaries of small-ORC cost/performance literature, not read at source |
| GT-18? | Small-scale ORC installed cost data points: 2 kWe ≈€5,775/kW; 50 kWe ≈€3,034/kW; optimized minimum ≈€1,600–1,630/kW | reported-by-delegate | WebSearch summary of academic techno-economic ORC studies; not opened directly this session |
| GT-19 | DOE/SunShot-era (2017) target capital cost for a two-tank molten-salt TES system ≈$15/kWh-th | read-at-source | Same Gen3 Roadmap source, table header "Candidate MS–HTFs (SunShot goal = 15 $/kWhth)" |
| GT-20 | Carnot efficiency ceiling between T_hot=838 K (565°C) and T_cold=298 K (25°C) = 1 − 298/838 = 64.4% | physical law (direct calculation from GT-3 and a stated ambient assumption) | Second Law of Thermodynamics (Carnot's theorem); no external citation needed beyond its inputs |

**`?`-marked: GT-6, GT-7, GT-8, GT-10, GT-11, GT-12, GT-13, GT-14, GT-15, GT-16, GT-17, GT-18 (12 of 20).**

All twelve feed load-bearing chains in Phase 4. GT-6, GT-13 and GT-17 each carry a Phase 3 failure record above (source blocked or not found) recording a genuine attempted read. GT-7, GT-8, GT-18 were used only as cross-check/rival figures (Phase 5), not as primary chain inputs, so no further read was attempted against the turn budget. GT-10–GT-12, GT-14–GT-16 are disclosed as unattributed engineering-judgment estimates rather than mis-cited to a source that was never opened — per the estimate procedure's own rule, an assumed value with a defensible bracket is preferred over a false citation.

**Addendum — three further ground truths surfaced while building the Derivation Chains in Phase 4** (the same disclosed pattern as the end-of-phase Assumption Audit, applied one phase earlier because these are numeric chain inputs rather than qualitative assumptions):

| ID | Fact | Provenance | Source / read-location |
|---|---|---|---|
| GT-21? | Solar-salt (NaNO₃/KNO₃) commodity price ≈$0.60–1.20/kg, central $0.80/kg | untested belief / engineering estimate | Not sourced this session — commodity price judgment, bracketed, no citation attempted |
| GT-22? | Design ambient temperature = 25°C (298 K), used for both heat-loss and Carnot-ceiling calculations | untested belief / engineering default | Not sourced this session — generic design-basis default, no specific site given |
| GT-23? | External insulation effective thermal conductivity k≈0.08 W/m·K at mean operating temperature, thickness 0.30 m | untested belief / engineering estimate | Not sourced this session — mineral-wool/calcium-silicate performance at high mean temperature, bracketed, no citation attempted |

**Updated `?`-marked count: GT-6, GT-7, GT-8, GT-10 through GT-18, GT-21, GT-22, GT-23 (15 of 23).**

**Second addendum — one further ground truth needed for the theoretical-limit cross-check on round-trip efficiency:**

| ID | Fact | Provenance | Source / read-location |
|---|---|---|---|
| GT-24? | Utility-scale (GWh-class) two-tank molten-salt CSP TES is commonly reported to achieve ≈98–99% round-trip thermal efficiency | reported-by-delegate / unverified | Not sourced this session — this is the domain convention the user's own prompt also cites; carried here as a best-demonstrated benchmark, not independently verified |

**Final `?`-marked count: GT-6, GT-7, GT-8, GT-10 through GT-18, GT-21, GT-22, GT-23, GT-24 (16 of 24).**

## 4. Derivation Chains

*Notation: chain heads cite `GT-N` / `GT-N?` / `Cn` identifiers only; hops are prose and may carry `[Assumes: A-N]` tags where a hop leans on a Phase-2 assumption beyond its head inputs.*

### C1 — Salt inventory sizing and cost (estimate/Fermi decomposition)

```text
GT-1 (cp=1.50 kJ/kg·K) + GT-2 (ρ=1,700 kg/m³) + GT-3 (ΔT=565–290°C) + GT-9 (5,000 kWh_th target) + GT-21? (salt price $0.80/kg)
→ required salt mass = 5,000 kWh × 3,600 kJ/kWh ÷ (1.50 kJ/kg·K × 275 K) = 43,636 kg
→ a 15% heel/ullage margin [Assumes: A-3] raises the working inventory to 50,182 kg
→ at 1,700 kg/m³ that inventory occupies 29.5 m³ of liquid salt, sized up ~10% for tank freeboard to ≈32.5 m³ of salt-handling volume per tank (the two-tank architecture requires each tank individually sized for the full inventory, since one tank is nearly full while the other is nearly empty at each extreme of the cycle)
→ at $0.80/kg (bracket $0.60–1.20/kg) the salt inventory costs ≈$40,100 (bracket $30,100–$60,200)
→ the salt-only cost of this 5,000 kWh_th system is ≈$40,100, or $8.02/kWh-th, before any tank, HX, pump, or BOP cost is added [Assumes: A-5]
```
**Pre-check:** head = GT-1, GT-2, GT-3, GT-9, GT-21? · ?-marked = GT-21? · lowest cited = none · Inputs ceiling = MEDIUM
**Confidence: MEDIUM** — GT-1/GT-2/GT-3 are read-at-source and GT-9 is definitional, but GT-21? (salt commodity price) is an unverified engineering estimate; verifying current solar-salt spot/contract pricing (e.g., a supplier quote or a recent SolarPACES cost paper) would let this chain clear to HIGH. The $/kg price is a linear multiplier on only one line of the eventual capital stack, so even a 50% price miss moves the total $/kWh by <2% — low leverage despite the `?`.

### C2 — Tank, insulation and foundation capital cost

```text
C1 (salt volume ≈32.5 m³/tank) + GT-3 (565°C hot / 290°C cold) + GT-10? (steel $4/kg) + GT-11? (refractory $1,000/m³) + GT-12? (insulation $200/m²)
→ sizing both tanks as vertical cylinders ≈3.2 m diameter × ≈4.0 m height gives an external shell area of ≈57 m² per tank
→ the hot tank operates above carbon steel's practical service limit for direct salt contact, so it needs a 12 mm carbon-steel shell (≈5,370 kg, ≈$21,500) plus a 175 mm refractory lining (≈10.0 m³, ≈$10,000) to protect the steel [Assumes: A-1]
→ the cold tank stays within carbon steel's service range at 290°C, so it needs only a thinner 10 mm shell (≈4,475 kg, ≈$17,900) plus a minor corrosion allowance (≈$2,000)
→ 300 mm external insulation on both tanks (≈114 m² total) costs ≈$22,800, and twin tank foundations add ≈$20,000
→ tanks + insulation + foundation together cost ≈$94,200
```
**Pre-check:** head = C1 (MEDIUM), GT-3, GT-10?, GT-11?, GT-12? · ?-marked = GT-10?, GT-11?, GT-12? · lowest cited = C1 (MEDIUM) · Inputs ceiling = MEDIUM
**Confidence: LOW** *(revised from an initial MEDIUM during the Self-Audit Gate's Fix step — see Criterion 5 below)* — two axes are short, not one: **Inputs** (GT-10?, GT-11?, GT-12? are unverified engineering estimates) and **Rivals** (a live, unresolved rival — a single-tank thermocline design, which trades one tank for a cheaper filler medium and is a recognized alternative TES architecture — is named in the Phase 5 Rival check and not ruled out there, nor in §5 Abandoned Reasoning). Two short axes license LOW under the three-axis rule.

### C3 — Heat exchanger, pumps, piping, trace heating, valves and BOP capital cost

```text
GT-13? (HX $200/kW-th) + GT-14? (pumps $60k ea.) + GT-15? (piping $1,100/m) + GT-16? (valves $7k ea.)
→ a 4-hour discharge duration [Assumes: A-4] sets thermal discharge power at 5,000 kWh ÷ 4 h = 1.25 MWth, which sizes every component in this chain — HX, pumps, piping and valves all scale with power (kW), not energy (kWh), so this single design choice is the largest lever on the whole $/kWh figure
→ the salt-to-working-fluid HX costs ≈1,250 kW × $200/kW ≈ $250,000
→ two hot-service salt pumps plus ≈40 m of trace-heated specialty piping plus electrical trace heating plus 8 high-temperature valves cost ≈$120,000 + $44,000 + $15,000 + $56,000 ≈ $235,000
→ adding controls/instrumentation (≈$60,000), electrical (≈$30,000) and site civil (≈$25,000) brings this whole non-tank, non-salt balance-of-plant to ≈$700,000
```
**Pre-check:** head = GT-13?, GT-14?, GT-15?, GT-16? · ?-marked = GT-13?, GT-14?, GT-15?, GT-16? · lowest cited = none · Inputs ceiling = MEDIUM
**Confidence: LOW** — every numeric input is an unverified engineering estimate (Inputs axis short) **and** the chain's single biggest lever, the 4-hour discharge-duration choice, is an arbitrary design assumption the 5 MWh spec does not fix (Inference axis short — a step the chain's endpoint depends on rests on `[Assumes: A-4]` whose failure, e.g. an 8-hour duration halving the power rating, the chain has not priced). Verification path: vendor quotes for a molten-salt HX and hot-service pumps at this exact duty, plus a stated power/duration requirement from whoever specifies the project.

### C4 — Total installed capital cost and $/kWh-th

```text
C1 ($40,100 salt) + C2 ($94,200 tanks) + C3 ($700,000 BOP/HX/pumps)
→ direct cost = 40,100 + 94,200 + 700,000 ≈ $734,300
→ a 20% EPC markup [Assumes: A-6] adds ≈$146,900
→ a 15% contingency on direct cost + EPC [Assumes: A-6] adds ≈$132,200
→ total installed capital cost ≈$1,013,300, or $1,013,300 ÷ 5,000 kWh ≈ $203/kWh-th
→ bracketing every major line item ±30–40% (the estimate procedure's decision-resolution check) gives a range of ≈$139–269/kWh-th, so the bracket does not cross any obvious decision threshold — it is uniformly "far above the oft-quoted utility figure," not uncertain about *which side* of that figure it lands on
```
**Pre-check:** head = C1 (MEDIUM), C2 (MEDIUM), C3 (LOW) · ?-marked = n/a (chain-level) · lowest cited = C3 (LOW) · Inputs ceiling = LOW
**Confidence: LOW** — mechanically capped by C3. The qualitative finding (small-scale TES capital cost sits far above the GWh-scale literature figure) is robust across the full $139–269/kWh bracket; what is **not** HIGH-confidence is the specific $203/kWh point estimate, which would need vendor quotes (C3) and a firm power/duration spec (A-4) to tighten.

### C5 — Theoretical-limit cross-check: how much of C4 is scale, and how much is physics

```text
C1 (salt-only cost $8.02/kWh-th) + C2 (bare steel-shell cost, excl. refractory/insulation/foundation ≈$39,400 → $7.88/kWh-th) + GT-19 ($15/kWh-th DOE/SunShot 2017 goal) + GT-7? ($30–40/kWh-th 2004 utility-scale study) + C4 ($203/kWh-th, bracket $139–269)
→ stripping every convention (no refractory, no insulation, no HX, no pumps, no controls, no EPC, no contingency — just the salt and the minimum steel needed to physically contain it) gives an **ideal cost floor** of ≈$15.9/kWh-th
→ that floor sits almost exactly at the DOE/SunShot 2017 *goal* of $15/kWh-th, and close to the 2004 study's *best-demonstrated* utility-scale figure of $30–40/kWh-th — utility-scale two-tank molten-salt TES is already operating within roughly 2× of its own physical materials floor
→ this project's conventional, fully-engineered small-scale figure ($203/kWh-th, bracket $139–269) sits 5–13× above that floor
→ the gap between the conventional (small-scale) figure and the best-demonstrated (utility-scale) figure is therefore almost entirely a **scale-economy gap** (fixed HX/pump/control/EPC costs not shrinking with energy capacity), not a materials-science or technology-maturity gap — there is very little room left to close by better engineering at *this* scale; the only lever that moves the number by more than ~30% is building bigger
```
**Pre-check:** head = C1 (MEDIUM), C2 (MEDIUM), GT-19, GT-7?, C4 (LOW) · ?-marked = GT-7? · lowest cited = C4 (LOW) · Inputs ceiling = LOW
**Confidence: LOW** — mechanically capped by C4, but note the direction of this specific finding (scale, not physics, explains the gap) is corroborated by two independently-sourced benchmarks (GT-19 read-at-source, GT-7? reported) landing close together and close to the independently-derived bare-materials floor — a genuine convergence, even though the headline $203/kWh point estimate itself remains LOW-confidence.

### C6 — Round-trip thermal efficiency, built bottom-up from conductive heat loss (estimate/Fermi decomposition)

```text
GT-3 (565°C hot / 290°C cold) + GT-22? (ambient 25°C) + GT-23? (insulation k≈0.08 W/m·K, 0.30 m thick) + C2 (tank external area ≈57 m²/tank)
→ Fourier conduction gives U = k/L = 0.08/0.30 ≈ 0.267 W/m²K
→ hot-tank standby loss = U×A×ΔT = 0.267 × 57 × (565−25) ≈ 8.2 kW; cold-tank standby loss = 0.267 × 57 × (290−25) ≈ 4.0 kW; combined ≈12.25 kW continuous
→ over one full daily cycle [Assumes: A-7] that is ≈12.25 kW × 24 h ≈ 294 kWh of loss against a 5,000 kWh capacity, i.e. ≈5.9% of stored energy lost to standby conduction per cycle
→ round-trip thermal efficiency at this scale ≈1 − 0.059 ≈ 94%, bracket ≈88–97% depending on insulation quality
```
**Pre-check:** head = GT-3, GT-22?, GT-23?, C2 (LOW) · ?-marked = GT-22?, GT-23? · lowest cited = C2 (LOW) · Inputs ceiling = LOW
**Confidence: LOW** *(mechanically capped by C2, revised above)* — on its own mechanism this chain would be MEDIUM: Fourier conduction is a physical law, not an assumption, and only the Inputs axis (ambient temperature, insulation k/thickness — GT-22?, GT-23?) is short. The LOW cap comes entirely from C2's head, not from this chain's own mechanism. Verification path for the uncapped MEDIUM: an actual insulation spec sheet at the mean operating temperature; the cap itself lifts only if C2's thermocline rival is resolved.

### C7 — Theoretical-limit cross-check: why small-scale RTE is lower than the oft-quoted utility figure

```text
C6 (≈94% at 5 MWh scale) + GT-24? (utility-scale "commonly reported" 98–99%)
→ the governing physical driver is surface-area-to-volume ratio: conductive loss scales with tank *surface area* (∝ r²) while stored energy scales with tank *volume* (∝ r³), so fractional standby loss scales roughly as 1/r — a utility-scale tank with 10× the linear dimension of this one loses roughly 10× less heat as a fraction of its contents
→ the **ideal ceiling** for round-trip thermal efficiency is 100% (zero loss, infinite insulation — unreachable); the **best-demonstrated** utility-scale figure (≈98–99%) sits close to that ceiling precisely because utility tanks are large enough that the surface-area penalty is small; this project's **conventional** small-scale figure (≈94%) sits further from the ceiling for the same geometric reason C5 found for capital cost
→ closing most of the conventional→best-demonstrated gap at fixed 5 MWh capacity would require disproportionately thicker/better insulation (diminishing returns against the R-value-vs-cost curve), not a technology change — the 98–99% figure people reach for when citing molten-salt TES efficiency is a **scale-contingent** number, not a material property of the salt
```
**Pre-check:** head = C6 (LOW), GT-24? · ?-marked = GT-24? · lowest cited = C6 (LOW) · Inputs ceiling = LOW
**Confidence: LOW** — mechanically capped by C6 (now LOW; see C6's revised Pre-check above). The qualitative mechanism (surface-to-volume scaling) is a geometric identity and is unaffected by this cap.

### C8 — Levelized cost of storage for a thermal end-use (amortized $/kWh-delivered)

```text
C4 ($1,013,300 capital, LOW) + C6 (≈94% RTE, MEDIUM) + [Assumes: A-7 (25-yr life, 350 cycles/yr), A-8 (7% discount rate), A-9 (O&M ≈2% CAPEX/yr + parasitics)]
→ capital recovery factor at 7%/25-yr ≈8.58%/yr, so annualized capital recovery ≈0.0858 × $1,013,300 ≈ $86,960/yr
→ O&M (maintenance ≈2% CAPEX ≈$20,270/yr) plus parasitic pump/trace-heat electricity (≈$13,440/yr at $0.08/kWh industrial rate) ≈$34,000/yr total
→ total annualized cost ≈$86,960 + $34,000 ≈ $120,960/yr
→ annual thermal energy delivered = 5,000 kWh × 350 cycles/yr × 0.94 RTE ≈1,645,000 kWh-th/yr
→ LCOS (thermal) = $120,960 ÷ 1,645,000 kWh ≈ **$0.0735/kWh-th ≈ $73.5/MWh-th delivered**
```
**Pre-check:** head = C4 (LOW), C6 (LOW, revised above) · ?-marked = n/a (chain-level) · lowest cited = C4/C6 (LOW) · Inputs ceiling = LOW
**Confidence: LOW** — mechanically capped by C4; also carries three further unverified financial/O&M assumptions (A-7/A-8/A-9) on the Inference axis. This figure is a *storage-adder* cost on top of whatever heat source charges the salt in the first place (electric resistance, solar receiver, waste heat) — it is not an all-in delivered-heat price, a scope point carried forward to §6.

### C9 — Levelized cost of storage for an electrical end-use (TES + small power block)

```text
C8 ($73.5/MWh-th, LOW) + GT-17? (small-ORC efficiency 18–26%, central 22%) + GT-18? (small-ORC cost €1,600–5,775/kW → ≈$1,800–3,200/kW at this size) + GT-20 (Carnot ceiling 64.4%)
→ a 275 kWe power block (1.25 MWth × 22%) costs ≈275 × $2,400/kW ≈ $660,000 to add [Assumes: A-11, A-12]
→ total capital rises to ≈$1,673,300; annualized capital recovery ≈$143,600/yr; combined O&M (TES + power block) ≈$50,500/yr; total annualized cost ≈$194,100/yr
→ electricity delivered = 1,645,000 kWh-th/yr × 22% ≈361,900 kWh-e/yr
→ LCOS (electric) = $194,100 ÷ 361,900 ≈ **$0.536/kWh-e ≈ $536/MWh-e delivered**, bracket ≈$434–678/MWh-e across the GT-17?/GT-18? plausible range
→ the 22% achieved efficiency is barely a third of the 64.4% Carnot ceiling (GT-20) for this hot/cold temperature pair — the shortfall is a small-plant irreversibility penalty (turbine, generator and heat-exchanger losses that do not shrink proportionally at sub-MW scale), the same scale-economy story C5 and C7 already told for capital cost and RTE
```
**Pre-check:** head = C8 (LOW), GT-17?, GT-18?, GT-20 · ?-marked = GT-17?, GT-18? · lowest cited = C8 (LOW) · Inputs ceiling = LOW
**Confidence: LOW** — mechanically capped by C8; GT-17?/GT-18? add further unresolved Inputs. The qualitative finding (electric-to-electric round trip is dominated by the power-block conversion penalty, not by the TES itself) is robust even though the $536/MWh-e point estimate is not.

### C10 — Trade-off analysis: which technology should serve which need (weighted, locked before scoring)

**Options** (status quo and a composite included, per the trade-off procedure): (a) molten-salt TES, bare, for a thermal end-use; (b) molten-salt TES + small power block, for electricity; (c) Li-ion, for electricity; (d) do nothing (no storage); (e) composite — route genuine thermal loads to bare TES and route electricity-shifting needs to Li-ion, rather than forcing one technology to cover both. **Must-haves:** must deliver useful energy to at least one end use — all five options pass (including "do nothing," trivially, since it is the explicit baseline); no option is knocked out.

**Criteria, weights (locked before scoring, out of 15) and anchors:**

| Criterion | Weight | 1 = | 5 = |
|---|---|---|---|
| Cost-effectiveness, heat delivery | 3 | >$300/MWh-th | <$50/MWh-th |
| Cost-effectiveness, electricity delivery | 5 | >$600/MWh-e | <$150/MWh-e |
| Round-trip efficiency | 2 | <30% | >85% |
| Maturity/risk at this scale (5 MWh / sub-MW) | 2 | unproven, one-off | many reference deployments at this exact scale |
| Lifetime/degradation certainty | 2 | largely undocumented | decades-long documented track record |
| Scalability ($/kWh improvement if built utility-scale) | 1 | flat with scale | falls sharply with scale |

**Scores (cited to the chain or GT that justifies each):**

| Option | Heat cost-eff | Elec cost-eff | RTE | Maturity | Lifetime | Scalability | **Weighted total** |
|---|---|---|---|---|---|---|---|
| (a) TES bare | 4 (C8: $73.5/MWh-th) | 1 (cannot deliver electricity without add-on) | 5 (C6: ≈94%) | 2 (no small-scale commercial track record found) | 4 (A-7, CSP operating history) | 5 (C5: scale gap is large) | **44** |
| (b) TES+PB | 3 (heat path retained but secondary) | 2 (C9: $536/MWh-e) | 1 (C9: ≈27–28% electric-to-electric) | 1 (no commercial small-ORC+TES product found) | 3 (ORC overhaul risk inside a 25-yr horizon) | 5 (C9: scale gap is large) | **34** |
| (c) Li-ion | 2 (GT-5/GT-6?: ≈$135–300/MWh-th-equiv. via resistive heating) | 4 (GT-5/GT-6?: ≈$131–292/MWh-e) | 5 (GT-5: 84–91%) | 5 (GT-5: mature, widely deployed at this scale) | 4 (well-documented, but 10–15 yr calendar/cycle life inside a 25-yr horizon) | 2 (GT-5: cost falls only modestly with scale) | **56** |
| (d) do nothing | 1 | 1 | 1 (no shifting service) | 5 (no new technology risk) | 5 (nothing to degrade) | 1 (no scalable benefit) | **31** |
| (e) composite | 4 (= option a's path) | 4 (= option c's path) | 4 (each sub-path performs within its own strong range) | 3 (two proven components, but added integration/dispatch-split risk) | 4 | 4 (TES-for-heat share improves with scale; Li-ion share roughly flat) | **58** |

**Flip test:** the composite (58) beats Li-ion-alone (56) by only 2 points. Decomposing the margin: composite gains +6 on heat cost-effectiveness and +2 on scalability, but loses −2 on RTE and −4 on maturity/risk, net +2. The single-criterion change that flips the result is **raising the weight on "maturity/risk at this scale" from 2 to 3** (margin = 6 − 2w₄ + 2, zero at w₄=3) — a one-point, ~50% increase in that one weight, which is not an obviously-wrong weight to hold for a real near-term deployment decision (combining two different storage technologies in one project genuinely carries integration/dispatch-split execution risk that a single mature technology does not). **This is a near-tie, not a robust result**, and is reported as such rather than refined into a false precision.

**Pre-check:** head = C8 (LOW), C9 (LOW), GT-5, GT-6? · ?-marked = GT-6? · lowest cited = C8/C9 (LOW) · Inputs ceiling = LOW
**Confidence: LOW** — mechanically capped by C8/C9, and the Rivals axis is explicitly short by the trade-off's own flip test: Li-ion-alone is a live, near-tied rival to the composite, unresolved by this analysis and reported rather than argued away.

### C11 — Second-order effects of the headline finding (actor lens and time lens)

```text
C4 (small-scale TES capital cost ≈5–13× the utility-scale literature figure) + C9 (small-scale TES+PB electric LCOS ≈2–4× Li-ion's)
→[2nd, actor] project developers and EPCs who had priced small distributed TES by analogy to utility CSP figures (GT-7?/GT-19) lose that cost argument once a real small-scale bottom-up build is done — second-order effect: due-diligence standards for small-scale TES proposals rise, requiring vendors to show actual component quotes and a stated power/duration basis rather than quoting the GWh-scale number
→[2nd, actor] battery vendors and financiers see this finding as reinforcing Li-ion's position in the sub-10 MWh / sub-2 MW segment, which is a competitive response that further reduces the incentive for ORC/TES vendors to productize at small scale, which in turn keeps GT-10 through GT-18's "no economies of scale yet" cost structure from improving — a self-reinforcing lock-in loop
→[2nd, time] immediately, a developer sizing a 5 MWh/sub-MW system today should choose Li-ion for any electricity-shifting need and reserve molten-salt TES only for a genuine, separately-metered thermal load it can serve directly
→[3rd, time] over a few years, if battery-cell tariffs/FEOC restrictions (GT-6?) keep pushing Li-ion LCOS upward (from GT-5's $131–232/MWh in 2021 toward GT-6?'s $210–292/MWh by 2025–26) while small-scale TES costs stay flat for lack of productization, the gap narrows mechanically without TES improving at all — worth re-running this analysis in 2–3 years
→[3rd, time] over the long run, once (if) a genuine thermal end-use market pulls small-scale molten-salt TES into volume production, GT-10–GT-18's unit costs could fall via ordinary learning-curve effects the way Li-ion's already have — but that pull has to come from the heat-delivery use case (where this analysis shows TES already wins, C8), not from the electricity use case (where it currently loses, C9); nothing here contradicts a Ground Truth, so no return to Phase 2 is triggered
```
**Pre-check:** head = C4 (LOW), C9 (LOW) · ?-marked = n/a (chain-level) · lowest cited = C4/C9 (LOW) · Inputs ceiling = LOW
**Confidence: LOW** — mechanically capped; these are qualitative, directionally-argued consequences rather than newly quantified figures, so the band reflects the chains they extend, not a fresh calculation of their own.

**End-of-phase Assumption Audit:** every `[Assumes: A-N]` tag above was checked against the Classified Assumptions Table in §2; all resolve to A-1 through A-12, each already present there. No new undeclared assumption surfaced during chain construction beyond the ground truths (GT-21?–GT-24?) already folded into §3's addenda. The full per-step scan is emitted as process output immediately before the Self-Audit Gate, below.

## 5. Abandoned Reasoning

### Dead End: Hitec salt instead of solar salt

**What was tried:** Pricing the hot/cold media as Hitec salt (lower ~142°C melting point, wider low-temperature margin) instead of solar salt (NaNO₃/KNO₃).
**Why abandoned:** Solar salt is the documented state-of-the-art choice for two-tank CSP TES (GT-3's own source labels it so), is cheaper per unit mass than Hitec, and the user's prompt anchors the analysis on it; switching media would not plausibly change the small-scale-penalty conclusion, only the salt-cost line (C1), which is already a low-leverage input.
**What it ruled out:** A second full media-cost rebuild was not needed to support the headline finding, since C5's theoretical-limit cross-check shows the capital-cost gap is driven by scale (HX/pumps/controls/EPC), not by salt chemistry.

### Dead End: Single-tank thermocline architecture

**What was tried:** Costing a single-tank thermocline design (one tank, filler material, no second vessel) as an alternative to the two-tank architecture priced in C2.
**Why abandoned:** Turn/scope budget — the user's prompt specifies a *two-tank* system, and a thermocline rebuild would be a second, parallel Fermi estimate rather than a refinement of this one.
**What it ruled out:** Nothing — this was **not** ruled out by evidence. It remains a live, unresolved rival to C2/C4's tank-cost figure and is carried forward explicitly into Phase 5's Rival step rather than closed here.

### Dead End: Independent utility-scale rebuild for cross-check

**What was tried:** Rebuilding the capital-cost stack at a utility scale (500+ MWh) to generate an independent, first-principles "fair" comparison point for C5, instead of relying on literature benchmarks GT-7?/GT-19.
**Why abandoned:** Out of scope — the problem statement specifies the 5 MWh system; a second full bottom-up build was judged not to be worth its own turn cost when two independent literature figures (GT-7?, GT-19) already bracket the utility-scale benchmark and agree closely with the bare-materials floor independently derived in C5.
**What it ruled out:** Nothing new quantitatively; it narrowed *how* the utility-scale comparison is supported (by convergent external benchmarks rather than a matching from-scratch build), which is disclosed as a limit on C5's confidence rather than presented as settled.

### Dead End: 2-cycles/day duty-cycle case

**What was tried:** Assuming 2 cycles/day (faster industrial duty cycle) instead of 1 cycle/day as the central case for C8/C9's annual-throughput calculation.
**Why abandoned:** The salt chemistry, ΔT window and tank architecture used throughout this analysis read as solar-CSP-pattern (once-daily charge/discharge), and A-7's once-per-day assumption is grounded in that documented operating pattern (Gemasolar/Andasol).
**What it ruled out:** A materially lower thermal/electric LCOS case (roughly half of C8/C9's figures) was not adopted as the central case, but is named explicitly as a swing variable in §6 rather than silently dropped — a faster-cycling industrial application of the same hardware would roughly halve both LCOS figures without changing the capital-cost or RTE chains at all.

### Dead End: Bottom-up Li-ion capital/efficiency rebuild

**What was tried:** Rebuilding Li-ion's own capital cost and efficiency bottom-up (steel/aluminum, cell chemistry, BMS, inverter, etc.) to match the bottom-up treatment given to TES.
**Why abandoned:** Deliberate scope decision, not a failure — the user's question asks whether TES is competitive against the Li-ion benchmark as commonly reported (an LCOS-style comparison), not whether Li-ion itself survives a first-principles rebuild. Lazard's directly-read figures (GT-5) serve that comparison role as intended.
**What it ruled out:** A matched-rigor Li-ion Fermi build was not produced; this means GT-5/GT-6? carry only the provenance of their own report, not an independent cross-check of the kind C5/C7 provide for the TES side — disclosed as an asymmetry in verification depth, not hidden.

## 6. Conclusion

**Recommended approach:** Use molten-salt TES where there is a genuine thermal end-use that can consume the stored heat directly, and use Li-ion where the need is to shift electricity — do not use a 5 MWh molten-salt TES plus a small power block as an electricity-storage product at this scale (chain C10). The formal weighted trade-off scores a composite (TES-for-heat + Li-ion-for-electricity) marginally above Li-ion-alone (58 vs 56), but that margin flips under a modest, defensible re-weighting toward integration/maturity risk (chain C10's flip test), so the practical recommendation leans on Li-ion as the default for any electricity-shifting need and reserves TES specifically for a metered thermal load (chains C8, C9).

**Key insight:** The commonly-quoted "$20–40/kWh" molten-salt TES figure is a utility/GWh-scale number; rebuilt bottom-up at 5 MWh it comes to ≈$203/kWh, bracket $139–269/kWh (chain C4) — 5–13× higher — because heat-exchanger, pump, piping, control and EPC costs scale with power and system complexity, not with stored energy, while the bare salt-plus-steel materials floor is ≈$15.9/kWh, almost exactly the DOE/SunShot utility-scale goal (chain C5). The entire small-scale cost penalty is a scale-economy effect, not a materials-science or technology-maturity gap.

**Trade-offs acknowledged:** Thermal round-trip efficiency at this scale (≈94%, chain C6) is itself lower than the ≈98–99% figure usually cited for CSP-scale TES, for the identical surface-to-volume reason that inflates the capital cost (chain C7). If TES is instead made to deliver *electricity* through a small power block, the dominant loss is the power block's achieved efficiency relative to its own Carnot ceiling (22% achieved vs. 64.4% ideal, chain C9) — not the TES hardware at all. This is why the thermal-vs-electrical distinction the prompt asked to make explicit is not a labeling nuance: it is the single largest quantitative lever on the competitiveness verdict, swinging the comparison from "TES wins by ~2–4×" (thermal end-use, chain C8 vs. GT-5/GT-6?) to "TES loses by ~2–4×" (electrical end-use, chain C9 vs. GT-5/GT-6?).

**Pre-check:** head = C4 (LOW), C5 (LOW), C6 (LOW), C7 (LOW), C8 (LOW), C9 (LOW), C10 (LOW), GT-6? · ?-marked = GT-6? · lowest cited = C4/C5/C6/C7/C8/C9/C10 (LOW) · Inputs ceiling = LOW
**Confidence: LOW** on the specific point estimates ($203/kWh capital; $73.5/MWh-th thermal LCOS; $536/MWh-e electric LCOS) — every contributing chain is formally LOW (C6/C7 were revised from an initial MEDIUM to LOW during the Self-Audit Gate's Fix step, once Phase 5's Rival check surfaced a live, unresolved rival on C2 that cascades through C6/C7) — because C2/C3/C4/C6/C7/C8/C9/C10 are mechanically capped by unverified small-scale unit costs (GT-10?–GT-18?), an unresolved discharge-duration design choice (A-4), and an unresolved rival architecture (the thermocline design). Substantially more robust, though not formally HIGH, is the **qualitative ordering** — TES beats Li-ion for direct thermal delivery and loses to Li-ion for electricity delivery at this 5 MWh scale — because that ordering holds across the entire bracket on every chain it depends on and is independently reinforced by a geometric mechanism (surface-to-volume scaling, chains C5/C7) rather than resting on the point estimates alone; no formal band exists above LOW to express that distinction, so it is stated here in prose rather than claimed as a higher band. What would move the band to HIGH: vendor quotes for the HX/pumps/valves (resolving GT-13?/GT-14?/GT-16?), a firm power/duration spec replacing A-4, resolving the thermocline rival against C2, and an opened (not just reported) current Lazard or NREL ATB figure replacing GT-6?.
## Appendix — process output

## §6→§4 closure ledger (process output)

- "Use molten-salt TES where there is a genuine thermal end-use ... do not use a 5 MWh molten-salt TES plus a small power block as an electricity-storage product at this scale" → chain C10 ✓
- "The commonly-quoted '$20–40/kWh' molten-salt TES figure is a utility/GWh-scale number; rebuilt bottom-up at 5 MWh it comes to ≈$203/kWh ... the entire small-scale cost penalty is a scale-economy effect" → chain C4, chain C5 ✓
- "Thermal round-trip efficiency at this scale (≈94%) is itself lower than the ≈98–99% figure usually cited ... the dominant loss is the power block's achieved efficiency relative to its own Carnot ceiling" → chain C6, chain C7, chain C9 ✓
- "Confidence: LOW on the specific point estimates ... MEDIUM-to-robust on the qualitative ordering" → chain C4, chain C5, chain C6, chain C7, chain C8, chain C9, chain C10 ✓ (discharged per D-07's own naming requirement, reproduced on the Pre-check line directly above it)

Scan complete: 4 §6 claims, all carry inline chain citations. 0 cut.
## Assumption Audit scan (process output)

| Chain | Step | Step Text (brief) | Assumption surfaced? | Added to Table? |
|---|---|---|---|---|
| C1 | 1 | salt mass from E=m·cp·ΔT | no | n/a — clean pass |
| C1 | 2 | +15% heel/ullage margin | A-3 (margin) | already in §2 table |
| C1 | 3 | mass→volume at ρ | no | n/a — clean pass |
| C1 | 4 | mass×price→cost | no (uses GT-21? in head) | n/a — clean pass |
| C1 | 5 (concl.) | salt-only $/kWh-th | A-5 (unit costs) | already in §2 table |
| C2 | 1 | tank geometry sizing | no | n/a — clean pass |
| C2 | 2 | hot tank needs refractory | A-1 (ΔT window / salt service limits) | already in §2 table |
| C2 | 3 | cold tank, carbon steel only | no | n/a — clean pass |
| C2 | 4 (concl.) | insulation + foundation | no | n/a — clean pass |
| C3 | 1 | 4-hr duration sets power | A-4 (discharge duration) | already in §2 table |
| C3 | 2 | HX cost | no | n/a — clean pass |
| C3 | 3 | pumps/piping/trace/valves | no | n/a — clean pass |
| C3 | 4 (concl.) | controls/electrical/civil | no | n/a — clean pass |
| C4 | 1 | direct cost sum | no | n/a — clean pass |
| C4 | 2 | +20% EPC | A-6 (EPC/contingency rates) | already in §2 table |
| C4 | 3 | +15% contingency | A-6 (EPC/contingency rates) | already in §2 table (same row as step 2) |
| C4 | 4 | total capital | no | n/a — clean pass |
| C4 | 5 (concl.) | bracket ±30–40% | no | n/a — clean pass |
| C5 | 1 | bare-materials floor | no | n/a — clean pass |
| C5 | 2 | floor ≈ DOE goal / 2004 figure | no | n/a — clean pass |
| C5 | 3 | conventional figure vs. floor | no | n/a — clean pass |
| C5 | 4 (concl.) | gap = scale, not physics | no | n/a — clean pass |
| C6 | 1 | U=k/L | no | n/a — clean pass |
| C6 | 2 | standby loss, two tanks | no | n/a — clean pass |
| C6 | 3 | loss over one daily cycle | A-7 (1 cycle/day) | already in §2 table |
| C6 | 4 (concl.) | RTE ≈94% | no | n/a — clean pass |
| C7 | 1 | surface/volume mechanism | no | n/a — clean pass |
| C7 | 2 | ideal ceiling vs. best-demonstrated | no | n/a — clean pass |
| C7 | 3 (concl.) | 98–99% is scale-contingent | no | n/a — clean pass |
| C8 | 1 | capital recovery factor | A-8 (discount rate) | already in §2 table |
| C8 | 2 | O&M + parasitics | A-9 (O&M rate, electricity price) | already in §2 table |
| C8 | 3 | total annualized cost | no | n/a — clean pass |
| C8 | 4 | annual energy delivered | A-7 (350 cycles/yr) — same assumption as C6 step 3, not a new row | already in §2 table |
| C8 | 5 (concl.) | LCOS thermal | no | n/a — clean pass |
| C9 | 1 | power-block capex | A-11, A-12 (ORC efficiency, ORC cost) | already in §2 table |
| C9 | 2 | total capital, electric case | no | n/a — clean pass |
| C9 | 3 | electricity delivered/yr | no | n/a — clean pass |
| C9 | 4 | LCOS electric | no | n/a — clean pass |
| C9 | 5 (concl.) | 22% vs. 64.4% Carnot | no | n/a — clean pass |
| C10 | 1 | options/must-haves | no | n/a — clean pass |
| C10 | 2 | weights locked, anchors set | A-8-adjacent discount-rate-style judgment calls on weights — not a factual assumption, no table row needed | n/a |
| C10 | 3 (concl.) | flip test, composite vs. Li-ion | no new assumption (restates C8/C9 inputs) | n/a — clean pass |
| C11 | 1–5 | 2nd/3rd-order actor and time effects | no new factual assumption beyond C4/C9's own | n/a — clean pass |

Scan complete: 11 chains, 37 steps scanned in order; every surfaced assumption (A-1, A-3 through A-9, A-11, A-12) was already present in the §2 Classified Assumptions Table before this scan ran — no new table row was required. 0 undeclared assumptions found.
## Self-audit scan (process output)

**Table 1 — chain form (section 4)**

| Chain | Chain Head (brief) | Form conforming? | Rule applied | Dependency clean? | Band | Act attempted? | Edges fired |
|---|---|---|---|---|---|---|---|
| C1 | GT-1+GT-2+GT-3+GT-9+GT-21? | yes | n/a | yes | MEDIUM | yes | none |
| C2 | C1+GT-3+GT-10?+GT-11?+GT-12? | yes | n/a | yes | LOW (revised, Fix step) | yes | none |
| C3 | GT-13?+GT-14?+GT-15?+GT-16? | yes | n/a | yes | LOW | yes | none |
| C4 | C1+C2+C3 | yes | n/a | yes | LOW | no | none |
| C5 | C1+C2+GT-19+GT-7?+C4 | yes | n/a | yes | LOW | yes | none |
| C6 | GT-3+GT-22?+GT-23?+C2 | yes | n/a | yes | LOW (revised, Fix step) | yes | none |
| C7 | C6+GT-24? | yes | n/a | yes | LOW (revised, Fix step) | no | none |
| C8 | C4+C6 | yes | n/a | yes | LOW | no | none |
| C9 | C8+GT-17?+GT-18?+GT-20 | yes | n/a | yes | LOW | yes | none |
| C10 | C8+C9+GT-5+GT-6? | yes | n/a | yes | LOW | yes | none |
| C11 | C4+C9 | yes | n/a | yes | LOW | no | none |

**Table 2 — claim inventory (section 6)**

| §6 Span (brief) | Construct | Claim under R11? | R11 clause applied | Chain cited |
|---|---|---|---|---|
| Recommended approach | bold lead-in | yes | bold lead-in whose colon closes the bold span | C10 |
| Key insight | bold lead-in | yes | bold lead-in whose colon closes the bold span | C4, C5 |
| Trade-offs acknowledged | bold lead-in | yes | bold lead-in whose colon closes the bold span | C6, C7, C9, C8 |
| Pre-check | bold lead-in | yes | bold lead-in whose colon closes the bold span | C4, C5, C6, C7, C8, C9, C10 |
| Confidence | bold lead-in | yes | bold lead-in whose colon closes the bold span | C4, C5, C6, C7, C8, C9, C10 |

Scan complete: 11 chain rows, one per section-4 chain block in order; 5 section-6 rows, one per construct in order — 5 claims under R11, 0 excluded. 0 chains malformed, 0 claims untraced.
## Adversarial pass (process output)

**Recompute.** Independently recomputed: salt mass (18,000,000 kJ ÷ 412.5 = 43,636 kg ✓); capital recovery factor at 7%/25-yr (0.07×1.07²⁵/(1.07²⁵−1) = 0.0858 ✓); total installed capital ($734,300×1.20×1.15 = $1,013,330 ✓, matches C4's stated $1,013,300 within rounding); thermal LCOS ($120,940 ÷ 1,645,000 kWh = $0.0735/kWh ✓, matches C8's $73.5/MWh); electric LCOS ($194,070 ÷ 361,900 kWh = $0.536/kWh ✓, matches C9's $536/MWh); Carnot ceiling (1 − 298/838 = 0.644 ✓, matches GT-20/C9). No combined figure lands on the wrong side of its own inputs (every scaled-up multiplier produces a larger, not smaller, output) and no arithmetic error was found.

**Sensitivity.** The procedure asks for the single ground truth whose falsity would flip the conclusion. Honestly, none of this analysis's formally `?`-marked ground truths is, by itself, a single flip away from reversing the headline verdict — even swinging GT-17?/GT-18? (power-block efficiency/cost) to their most optimistic literature-bracket extremes only moves C9's electric LCOS to ≈$434/MWh-e, still above Li-ion's own pessimistic recent band (GT-6?, $292/MWh-e). The genuine single point of fragility is **assumption A-4** (the 4-hour discharge-duration design choice), which is not a ground truth at all — it is an unresolved design input the 5 MWh spec never fixed. Because HX/pump/power-block capex scale with power, not energy, a materially longer assumed duration (8–24 h) would shrink C3's capex per kWh substantially and could close or reverse the electric-delivery gap. This is disclosed as the sharpest actionable finding of the whole analysis, not papered over with a confidence caveat on a GT that isn't actually the pivot.

**Rival.** Headline conclusion: Li-ion-alone is a live, near-tied rival to the "composite" recommendation (chain C10's flip test, margin 58 vs. 56, flips under a one-point reweighting) — unresolved, not ruled out. Per intermediate chain: **C4** — a single-tank thermocline design is a live, unruled-out rival to the two-tank architecture priced here (§5, abandoned for budget, not for evidence). **C5, C7** — rival not applicable: these are convergence checks against independent benchmarks, not competing causal claims. **C6** — rival not applicable: only parameter uncertainty (insulation spec) already bracketed, no competing loss mechanism proposed. **C8** — rival not applicable: a genuine scope question (what the LCOS "adder" is added to) is already carried as a caveat in §6, not a competing figure. **C9** — a small steam-Rankine power block (instead of the small-ORC assumed) is a live, unruled-out rival technology choice for the electric case; it is not priced here and stays live. **C11** — rival not applicable in a strong sense: these are qualitative directional claims already carried at LOW confidence, not substantially contested by a specific competing account.

**Adversarial technique — Inversion** (the conclusion under test is a claim — a cost-competitiveness verdict — not a plan with timelines, so inversion is the applicable technique per the decision rule stated in both the inversion and pre-mortem procedures; procedure opened via Read immediately before this pass, not recalled from memory).

- *Inverted Claim:* "Molten-salt TES plus a small power block **is** cost-competitive with Li-ion for electricity-storage delivery at this 5 MWh scale" (inverting chain C9/C10's headline finding that it is not).

- *Failure-Guaranteeing Conditions* (conditions that would guarantee the original "not competitive" claim false), viewed from three angles — an EPC/engineer's angle, a vendor's angle, and a financier's angle: (1) achievable small-ORC efficiency is actually far above 22%, nearer Carnot [engineer]; (2) achievable small-ORC installed cost is actually far below $2,400/kW [vendor]; (3) this analysis's bottom-up TES capital-cost build is grossly overestimated relative to real vendor pricing [vendor]; (4) Li-ion LCOS spikes well above its reported $131–292/MWh-e band [financier]; (5) the real discharge duration is much longer than the 4-hour assumption used here, shrinking power-sized capex per kWh [engineer]; (6) the real cycling frequency is much higher than 1/day, cutting annualized cost per kWh delivered [engineer/financier].

- *Necessary Preconditions* of the original ("not competitive") claim, each a checkable assertion, tagged load-bearing/unverified status: **P1** [load-bearing, unverified — GT-17?] achievable small-ORC efficiency at ≈275 kWe stays materially below 45%. **P2** [load-bearing, unverified — GT-18?] achievable small-ORC installed cost stays above ≈$1,800/kW. **P3** [load-bearing, unverified — GT-10?–GT-16?] TES bottom-up capital stays within the $139–269/kWh bracket, not collapsing toward the $16–40/kWh utility range. **P4** [load-bearing, requires an extreme swing — GT-5/GT-6?] Li-ion LCOS stays within its reported band rather than roughly doubling. **P5** [load-bearing, unverified, and unanchored by any literature bracket — A-4] the real discharge duration is near 4 hours, not 8–24 hours. **P6** [load-bearing, requires an extreme (3×) swing, grounded in CSP convention — A-7] cycling frequency stays near 1/day.

- *Stress-Test Verdict:* the "not cost-competitive for electricity delivery" conclusion survives the inversion test across every bracket this analysis examined for P1–P4 and P6, **but P5 is its genuinely weak point** — it rests on an arbitrary design choice with no literature anchor at all, unlike P1–P4 which are at least bracketed against (unverified but sourced-attempt) external figures. The conclusion is therefore sound *given the stated 4-hour duration*, but that duration was never actually specified by the problem — it is this analysis's own stand-in for a missing design fact.

**Clusters (naming the chains/GTs each bears on) and Disposition:**

| Cluster | Preconditions | Bears on | Disposition |
|---|---|---|---|
| Power-block performance/cost uncertainty | P1, P2 | GT-17?, GT-18?, C9 | Accepted risk — mitigation: obtain actual ORC vendor quotes at the specific kWe rating before any investment decision |
| TES capital-cost uncertainty | P3 | GT-10?–GT-16?, C3, C4 | Accepted risk — mitigation: obtain vendor quotes for HX/pumps/valves before using the $203/kWh figure as final |
| **Design-basis gap: discharge duration never specified** | **P5** | A-4, C3, C4, C9 | **Plan change** — pin the actual power rating/discharge duration before accepting the electric-delivery "not competitive" verdict for any real system; this is the one finding that changes the analysis's own next step, not just its confidence |
| Li-ion benchmark vintage/volatility | P4 | GT-5, GT-6? | Accepted risk — mitigation: re-run against the current-year Lazard/NREL ATB release before finalizing |
| Cycling-frequency assumption | P6 | A-7, C6, C8 | Accepted risk, low priority — mitigation: verify against the project's actual duty cycle if and when known |

**Falsification.** The "TES + a small power block is not cost-competitive with Li-ion for electricity delivery at this 5 MWh scale" conclusion is false if a real, vendor-quoted build of this exact system (power block at the stated kWe rating, TES at 5 MWh) yields an installed electric LCOS at or below Li-ion's current reported band (≈$131–292/MWh-e) — most plausibly achieved if the real discharge duration is materially longer than the 4-hour design-basis assumption used throughout this analysis.
## Techniques not applied (process output)

- pre-mortem — not applicable — the headline conclusion under adversarial test (§5 Phase-5 adversarial pass) is a claim (a cost-competitiveness verdict), not a plan with timelines and dependencies; per the decision rule stated in both the inversion and pre-mortem reference procedures, inversion is the applicable technique for a claim, and it was applied instead (see the Adversarial pass record above).

(five-whys/reduce-to-primitives, fishbone, inversion [Phase 2 and Phase 5], trade-off, second-order, estimate, and theoretical-limit [Phase 4] all fired during this run and are not listed here.)
## Self-Audit Gate (process output)

**Pass 1 (before re-score):** Criterion 1 Rigorous · Criterion 2 Sound · Criterion 3 Sound · Criterion 4 Rigorous · Criterion 5 Hand-wavy · Criterion 6 Rigorous · Gate cleared: yes · Hand-wavy cap cleared: yes

*(Pass 1 would already have cleared the gate under both conditions — no Absent, and only one Hand-wavy — but Criterion 5's Hand-wavy finding was a genuine miscalibration, not a borderline call, so it was fixed rather than left standing: chains C2, C6 and C7 were originally banded MEDIUM despite a live, unresolved Rivals-axis finding (the single-tank thermocline design, surfaced during the Phase 5 Rival check) that, combined with each chain's already-short Inputs axis, licenses LOW under the three-axis rule — two or more chains carrying a band their own axes do not license is exactly Criterion 5's Hand-wavy descriptor. The Fix: C2, C6 and C7 were revised to LOW in section 4, the self-audit scan's Table 1 was updated to match, and section 6's Pre-check/Confidence lines were updated to cite the revised bands. This is the single re-perception pass the Turn-discipline rule allows; no further re-scoring follows.)*

**Criterion 1: Identify Essence**
Quoted span: "What does a 5 MWh two-tank molten-salt thermal energy storage (TES) system cost per kWh of capacity when its capital cost is rebuilt bottom-up from constituent unit costs ... and is it cost-competitive with lithium-ion, with the thermal-vs-electrical end-use distinction made explicit rather than assumed away?"
Band: **Rigorous**
Justification: The statement names the real underlying question (whether a specific, oft-quoted cost figure survives a bottom-up rebuild at this scale, and whether "competitive" means the same thing across two different end-uses) rather than restating the prompt or a symptom, and each of the five numbered success criteria is a checkable, problem-specific test against the Conclusion section (e.g., "show the arithmetic explicitly... traceable... not asserted").

**Criterion 2: Challenge Assumptions**
Quoted span (from the Assumption Audit scan, process output): "Scan complete: 11 chains, 37 steps scanned in order; every surfaced assumption (A-1, A-3 through A-9, A-11, A-12) was already present in the §2 Classified Assumptions Table before this scan ran — no new table row was required. 0 undeclared assumptions found." Also, from §2 directly: "| A-4 | Discharge duration = 4 h ... | Convention (arbitrary design choice...) | **Challenged explicitly**... | Accepted as a stated, clearly-flagged design choice, not a given fact | Unverified by nature (a choice, not a measurement) — sensitivity run in Phase 5 |"
Band: **Sound**
Justification: All 14 rows use the four-type scheme correctly, several are genuinely challenged (not merely labelled Accept — A-4, A-6, A-8, A-14 explicitly say "Challenged"), and the Assumption Audit ran exhaustively over every chain step with no gaps; but the Verdict cells do not consistently use the prescribed "Accept/Challenge/Discard — justification" leading-token form (they instead carry free-form specific verdicts), and several Verification cells for chain-used unverified assumptions read as specific-but-free-form rather than the literal string "unverified — flagged" — a specific, identifiable format shortfall rather than generic or empty content, which is the Sound descriptor rather than Hand-wavy's listed patterns (empty cells, out-of-scheme Types, or blanket unchallenged Accepts), none of which apply here.

**Criterion 3: Establish Ground Truths**
Quoted span: "`?`-marked: GT-6, GT-7, GT-8, GT-10 through GT-18, GT-21, GT-22, GT-23, GT-24 (16 of 24)." — checked against the Ground Truths list directly: IDs carrying `?` are exactly GT-6, GT-7, GT-8, GT-10, GT-11, GT-12, GT-13, GT-14, GT-15, GT-16, GT-17, GT-18, GT-21, GT-22, GT-23, GT-24 — 16 entries, matching the enumeration exactly.
Band: **Sound**
Justification: Every GT-ID is stable and matches chain-head usage; every verified GT cites a specific, non-generic source (a named DOE/NREL/SNL slide deck with slide/table identifiers, or a directly-extracted Lazard PDF table row); provenance labels are present throughout; the `?` enumeration was checked against the list (not merely quoted) and matches exactly; GT-6, GT-13 and GT-17 each carry a Phase 3 failure record naming the source and why unreachable. The shortfall from Rigorous: no chain in the document is rated HIGH, so the Rigorous bullet requiring every reachable unsuffixed GT to feed at least one HIGH-confidence chain is not met for GT-1, GT-2, GT-3, GT-4, GT-5, GT-9, GT-19 and GT-20 — a specific, identifiable, and disclosed consequence of this analysis mixing verified and unverified inputs in every chain it builds, not a labeling or stability defect, which keeps it at Sound rather than Hand-wavy (no Hand-wavy descriptor — unstable IDs, a Discard-verdict assumption reappearing, multiple unread GTs missing `?`, a disagreeing enumeration, or an unsuffixed GT feeding HIGH without a read-location — actually matches).

**Criterion 4: Reason Upward**
Quoted span (from the self-audit scan's Table 1, process output): "| C4 | C1+C2+C3 | yes | n/a | yes | LOW | no | none |" and "Scan complete: 11 chain rows, one per section-4 chain block in order... 0 chains malformed, 0 claims untraced." Directly from the analysis text: the Abandoned Reasoning section (output section 5) documents five dead ends in the prescribed What-was-tried / Why-abandoned / What-it-ruled-out structure, and the Phase 5 Recompute step independently reverified every headline figure with no arithmetic error found.
Band: **Rigorous**
Justification: All 11 chains score "yes" on Form conforming and Dependency clean in the self-audit scan, each carries at least one genuine intermediate step, every GT-ID referenced resolves to a Ground Truths entry, no analogy is used as direct evidence anywhere in section 4, every chain step introducing a genuinely new assumption carries an inline `[Assumes: X]` tag (verified exhaustively by the Assumption Audit scan), and Abandoned Reasoning documents five specific dead ends rather than using the escape valve.

**Criterion 5: Validate**
Quoted span (from §4, post-Fix): "**Confidence: LOW** *(revised from an initial MEDIUM during the Self-Audit Gate's Fix step — see Criterion 5 below)* — two axes are short, not one: **Inputs** (GT-10?, GT-11?, GT-12? are unverified engineering estimates) and **Rivals** (a live, unresolved rival — a single-tank thermocline design... — is named in the Phase 5 Rival check and not ruled out there)." Also, from the Adversarial pass record (process output): all five parts (Recompute, Sensitivity, Rival, the Inversion technique's four sub-parts, Falsification) carry content, and every cluster in the Clusters/Disposition table carries either a named plan change or an explicitly accepted risk with a named mitigation.
Band: **Sound**
Justification: Post-Fix, every chain is rated no higher than the lowest-rated chain its head cites, no chain consumes a GT-N? input while rated HIGH, the three-axis miscalibration found in Pass 1 (C2/C6/C7) was corrected rather than left standing, and the adversarial pass record is complete with every cluster disposed. The remaining Sound-level (not Rigorous-level) shortfall: several Confidence-line prose sentences (e.g., C1, C3) describe their unverified inputs in aggregate ("every numeric input is an unverified engineering estimate") rather than re-naming each GT-N? ID individually in that sentence — the IDs themselves are present and correct one line above, on each chain's required Pre-check line, so this is an omission in the prose restatement rather than a missing or generic weak-link identification, which is the Sound descriptor ("a MEDIUM or LOW confidence line omits a GT-N? input it rests on directly") rather than Hand-wavy's ("described in general terms... without naming the specific... GT-N? input" anywhere in the chain block, which is not the case here since the Pre-check line does name them).

**Criterion 6: Conclusion-to-Ground-Truth Traceability**
Quoted span (from the self-audit scan's Table 2, process output): "| Key insight | bold lead-in | yes | bold lead-in whose colon closes the bold span | C4, C5 |" and the reconciliation line "5 claims under R11, 0 excluded... 0 claims untraced."
Band: **Rigorous**
Justification: Every one of the five §6 constructs traces to a specific, named section-4 chain (per Table 2 and the §6→§4 closure ledger, consistent with each other), no claim introduces reasoning absent from section 4, and the Key Insight ("the $20–40/kWh figure is a utility-scale number; at 5 MWh the physics-vs-scale decomposition shows the gap is almost entirely economies of scale") is a non-obvious finding distinct from the Recommended Approach's technology-routing recommendation, not a restatement of it.

**Gate result:** cleared · passes: 2 · Fix/Repeat fired: yes
## Structured summary (process output)
```json
{
  "schema_version": 1,
  "run_mode": "full-composer",
  "assumptions": [
    {"id": "A-1", "type": "convention", "verdict": "Accept"},
    {"id": "A-2", "type": "untested belief", "verdict": "Challenge"},
    {"id": "A-3", "type": "untested belief", "verdict": "Accept"},
    {"id": "A-4", "type": "convention", "verdict": "Challenge"},
    {"id": "A-5", "type": "untested belief", "verdict": "Challenge"},
    {"id": "A-6", "type": "convention", "verdict": "Challenge"},
    {"id": "A-7", "type": "current constraint", "verdict": "Accept"},
    {"id": "A-8", "type": "convention", "verdict": "Challenge"},
    {"id": "A-9", "type": "untested belief", "verdict": "Accept"},
    {"id": "A-10", "type": "physical law", "verdict": "Accept"},
    {"id": "A-11", "type": "untested belief", "verdict": "Challenge"},
    {"id": "A-12", "type": "untested belief", "verdict": "Challenge"},
    {"id": "A-13", "type": "current constraint", "verdict": "Accept"},
    {"id": "A-14", "type": "convention", "verdict": "Challenge"}
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
    {"id": "GT-9", "read_at_source": true},
    {"id": "GT-10", "read_at_source": false},
    {"id": "GT-11", "read_at_source": false},
    {"id": "GT-12", "read_at_source": false},
    {"id": "GT-13", "read_at_source": false},
    {"id": "GT-14", "read_at_source": false},
    {"id": "GT-15", "read_at_source": false},
    {"id": "GT-16", "read_at_source": false},
    {"id": "GT-17", "read_at_source": false},
    {"id": "GT-18", "read_at_source": false},
    {"id": "GT-19", "read_at_source": true},
    {"id": "GT-20", "read_at_source": true},
    {"id": "GT-21", "read_at_source": false},
    {"id": "GT-22", "read_at_source": false},
    {"id": "GT-23", "read_at_source": false},
    {"id": "GT-24", "read_at_source": false}
  ],
  "chains": [
    {"id": "C1", "confidence": "MEDIUM", "rests_on": ["GT-1", "GT-2", "GT-3", "GT-9", "GT-21?"]},
    {"id": "C2", "confidence": "LOW", "rests_on": ["C1", "GT-3", "GT-10?", "GT-11?", "GT-12?"]},
    {"id": "C3", "confidence": "LOW", "rests_on": ["GT-13?", "GT-14?", "GT-15?", "GT-16?"]},
    {"id": "C4", "confidence": "LOW", "rests_on": ["C1", "C2", "C3"]},
    {"id": "C5", "confidence": "LOW", "rests_on": ["C1", "C2", "GT-19", "GT-7?", "C4"]},
    {"id": "C6", "confidence": "LOW", "rests_on": ["GT-3", "GT-22?", "GT-23?", "C2"]},
    {"id": "C7", "confidence": "LOW", "rests_on": ["C6", "GT-24?"]},
    {"id": "C8", "confidence": "LOW", "rests_on": ["C4", "C6"]},
    {"id": "C9", "confidence": "LOW", "rests_on": ["C8", "GT-17?", "GT-18?", "GT-20"]},
    {"id": "C10", "confidence": "LOW", "rests_on": ["C8", "C9", "GT-5", "GT-6?"]},
    {"id": "C11", "confidence": "LOW", "rests_on": ["C4", "C9"]}
  ],
  "dead_ends": [
    "Hitec salt instead of solar salt",
    "Single-tank thermocline architecture",
    "Independent utility-scale rebuild for cross-check",
    "2-cycles/day duty-cycle case",
    "Bottom-up Li-ion capital/efficiency rebuild"
  ],
  "techniques": {
    "applied": ["fishbone", "inversion", "five-whys", "estimate", "theoretical-limit", "trade-off", "second-order"],
    "not_applied": [
      {
        "technique": "pre-mortem",
        "phase": 5,
        "reason": "the headline conclusion under adversarial test (§5 Phase-5 adversarial pass) is a claim (a cost-competitiveness verdict), not a plan with timelines and dependencies; per the decision rule stated in both the inversion and pre-mortem reference procedures, inversion is the applicable technique for a claim, and it was applied instead"
      }
    ]
  },
  "gate": {
    "passes": [
      {"bands": ["Rigorous", "Sound", "Sound", "Rigorous", "Hand-wavy", "Rigorous"], "gate_cleared": true, "hand_wavy_cap_cleared": true},
      {"bands": ["Rigorous", "Sound", "Sound", "Rigorous", "Sound", "Rigorous"], "gate_cleared": true, "hand_wavy_cap_cleared": true}
    ],
    "fix_repeat_fired": true,
    "cleared": true
  },
  "re_entry": {
    "fired": true,
    "edges": [
      {
        "edge": "the Self-Audit Gate's Fix/Repeat loop",
        "trigger": "Criterion 5 scored Hand-wavy on the first pass because chains C2, C6 and C7 carried a MEDIUM band their own axes no longer licensed once Phase 5's Rival check surfaced a live, unresolved rival (the single-tank thermocline design) that shorted a second axis on each."
      }
    ]
  },
  "conclusion": {
    "recommendation": "Use molten-salt TES where there is a genuine thermal end-use that can consume the stored heat directly, and use Li-ion where the need is to shift electricity — do not use a 5 MWh molten-salt TES plus a small power block as an electricity-storage product at this scale (chain C10). The formal weighted trade-off scores a composite (TES-for-heat + Li-ion-for-electricity) marginally above Li-ion-alone (58 vs 56), but that margin flips under a modest, defensible re-weighting toward integration/maturity risk (chain C10's flip test), so the practical recommendation leans on Li-ion as the default for any electricity-shifting need and reserves TES specifically for a metered thermal load (chains C8, C9).",
    "confidence": "LOW",
    "rests_on": ["C4", "C5", "C6", "C7", "C8", "C9", "C10", "GT-6?"]
  }
}
```
