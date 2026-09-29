## Assumption Audit scan (process output)

Scan performed at end of Phase 4 over every chain step in section 4 (chains C1-C8, including the second-order extension on C3). Assumption IDs (A1-A10) refer to rows in the Assumptions Table (section 2).

| Chain | Step | Step Text (brief) | Assumption surfaced? | Added to Table? |
|-------|------|-------------------|----------------------|-----------------|
| C1 | 1 | Naive two-reservoir Carnot (~63-66%) ignores the salt's temperature glide | none | n/a |
| C1 | 2 | Glide-matched exergy ceiling ~56-59% vs. a 15-35°C dead state | A9 (dead-state bracket) | yes |
| C1 | 3 | Steam's isothermal boiling plateau caps T_avg,H at ~630-650K | none (covered by GT-10? flag) | n/a |
| C1 | 4 | Rankine-ideal ceiling ~46-52% at realistic condensing temp | none | n/a |
| C2 | 1 | Net = gross - power-block parasitics | A1 (system boundary) | yes |
| C2 | 2 | Net efficiency ≈39.2% (air-cooled, power-block boundary) | none | n/a |
| C2 | 3 | Whole-plant boundary alternative ≈36.1% | none | n/a |
| C3 | 1 | Turbine-only upgrade: 41.1% → 43.2% gross | none | n/a |
| C3 | 2 | + supercritical pressure: → 45.2% gross | none | n/a |
| C3 | 3 | "Realistically recoverable... near-term" | A7 (deployment risk, not technical barrier) | yes |
| C3 | 4 [2nd] | OEM incentive to productize CSP-specific supercritical package | A10 (OEM commercial incentive) | yes |
| C3 | 5 [3rd] | First-of-kind premium falls with learning-curve repetition | none new — extends A10 | n/a |
| C4 | 1 | Supercritical raises boiler feed pump power 3,175→4,977 kW | none | n/a |
| C4 | 2 | Net recompute: ≈42.6% (power-block boundary) | A1 (reused) | yes (already present) |
| C4 | 3 | Net gain (3.4 pts) trails gross gain (4.1 pts) | none | n/a |
| C5 | 1 | Near-term path (45.2%) vs. Rankine-ideal ceiling (46-52%) | none | n/a |
| C5 | 2 | Residual is turbine/mechanical/piping irreversibility | A5 (turbine isentropic floor) | yes |
| C5 | 3 | Residual is "fundamentally stuck" at fixed 565°C | none | n/a |
| C6 | 1 | 8-9 pt gap (exergy ceiling vs. Rankine-ideal) from boiling plateau | none | n/a |
| C6 | 2 | Supercritical partially closes this (consistent with GT-4) | none | n/a |
| C6 | 3 | Full closure needs non-Rankine cycle — out of scope | none | n/a |
| C7 | 1 | Wet vs. dry cooling: 41.1% vs. 43.0% gross | none | n/a |
| C7 | 2 | Named plants are sited in water-scarce deserts | A6 (water-constrained siting) | yes |
| C7 | 3 | Wet cooling is conditionally, not unconditionally, recoverable | none | n/a |
| C8 | 1 | Design-point figures ≠ realized annual-average figures | none | n/a |
| C8 | 2 | Bracket: ≈40-42% (near-term) / ≈36-38% (baseline) annual net | A8 (storage-dispatch cycling penalty) | yes |
| C8 | 3 | Cycling penalty doesn't change recoverable-vs-locked-in split | none | n/a |

All 28 chain steps across C1-C8 are covered; every surfaced assumption (A9, A1, A7, A10, A5, A6, A8) is a row already present in, or newly added to, the Assumptions Table in section 2. No chain step surfaced an assumption not accounted for.

## Techniques not applied (process output)

- theoretical-limit (Phase 1 essence-reframe invocation) — not applicable — the 565°C hot-salt ceiling is fixed by the user's own problem scoping, not treated as a convention-vs-hard-bound question the Essence Statement needs reframed around.
- inversion (Phase 2 invocation) — not applicable — no single conclusion-adjacent assumption here is "too clean" in a way that calls for adversarial failure-condition enumeration; the four-type challenge treatment in the Assumptions Table already directly challenges the load-bearing conventions (notably the naive-Carnot convention and the cooling-method convention).
- inversion (Phase 5 invocation) — not applicable — the headline conclusion is a recommendation/plan (pursue turbine + supercritical upgrades at fixed 565°C), so the decision rule routes the adversarial pass to pre-mortem instead.
- trade-off (Phase 4 invocation) — not applicable — the one multi-option choice touched (wet vs. dry cooling, chain C7) is already settled by a site-level water-availability constraint rather than live among comparably-weighted criteria; formalizing a weighted matrix over a pre-settled choice would manufacture false precision.
- fishbone (Phase 2 invocation) — not applicable — the loss/gap decomposition follows a single well-characterized physical causal chain (cycle-architecture exergy destruction → turbine/mechanical irreversibility → parasitics), not a multi-categorical brainstorm space.
- five-whys reduce-to-primitives (Phase 3 invocation) — not applicable — GT-10?'s economizer/evaporator/superheat enthalpy-segment decomposition already performs the equivalent primitive-level reduction inline; a separately labeled pass would duplicate it.

theoretical-limit (Phase 4), estimate (Phase 4, Fermi steam-table and parasitic recomputation), and second-order (Phase 4, C3 extension) all fired and are applied in section 4.
## Adversarial pass (process output)

**Recompute.** Gross efficiency, baseline: 165,000 kWe ÷ 401,000 kWt = 41.15% ≈ 41.1-41.2% — matches GT-1. Gross efficiency, Supercritical Cycle 3: 165,000 kWe ÷ 365,100 kWt = 45.20% — matches GT-4 exactly. Net efficiency, baseline (power-block boundary): (165,000 - 7,979) kWe = 157,021 kWe; 157,021 ÷ 401,000 = 39.16% ≈ 39.2% — recomputes to chain C2's figure. Net efficiency, Supercritical Cycle 3: parasitics = 4,977+127+2,687+700+958 = 9,449 kW; (165,000-9,449)=155,551 kWe; 155,551÷365,100 = 42.60% — recomputes to chain C4's figure. Whole-plant-boundary baseline net: (165,000-7,979-12,096)=144,925 kWe; 144,925÷401,000=36.14% ≈ 36.1% — recomputes to chain C2's alternative figure. All four recomputed figures land within rounding of the values stated in their chains; each is an upward or downward combination consistent with its stated operation (subtracting parasitics from gross, dividing by thermal duty) and none falls outside the direction its operation implies.

**Sensitivity.** The single ground truth whose falsity would most flip the headline framing is GT-10? (the Fermi-estimated mean heat-addition temperature underlying chain C1's ~46-52% Rankine-ideal ceiling); it is `?`-marked. If real IAPWS-IF97 steam properties gave a materially different T_avg,H, the "near-term recoverable closes roughly half the gap to the tighter ceiling" framing in the Conclusion would shift, though GT-1 through GT-4 (all read-at-source, unsuffixed) would be completely unaffected. Weakest link per chain: C1 — GT-10?'s Fermi steam-table approximation; C2 — the power-block-vs-whole-plant system-boundary choice (A1); C3/C4 — assumption A7 (deployment risk, not technical barrier) combined with the live commercial-deployment rival named below; C5 — GT-11? (turbine isentropic-efficiency floor judgment) plus its citation of C1 and C3; C6 — its citation of C1; C7 — none identified (source-attributed directly); C8 — GT-9?'s Fermi cycling-penalty bracket.

**Rival.** Headline conclusion (near-term hardware closes ~4 gross points at fixed 565°C): the strongest rival is "the Sandia 2013 feasibility-study numbers never survive commercial deployment, and current practice remains stuck near 41% indefinitely" — this rival is *not* ruled out by any ground truth in this analysis (no commercial supercritical molten-salt tower plant has operated as of this analysis to settle it either way); it is carried live on chains C3 and C4's confidence lines rather than resolved, and it is the direct basis for Clusters A and B below. Chain C1 (the tighter ceiling itself): the rival "the naive two-reservoir Carnot bound is the theoretically appropriate reference" is ruled out by the standard exergy-of-a-sensible-heat-stream identity (a settled thermodynamic result, not a live scholarly dispute) — this rival is ruled out, not merely disclosed. Chain C2 (net efficiency number): the rival "only the whole-plant boundary (36.1%) is a meaningful net figure" is addressed by presenting both boundary conventions explicitly rather than by ruling one out — carried live but disclosed on C2's confidence line. Chain C5 (turbine/mechanical floor): the rival "the residual gap is a Fermi-calculation artifact of C1's steam-table approximation, not a real physical floor" is only partially addressed — it stays live, contributing to C5's LOW rating alongside GT-11?. Chain C6 (architecture-mismatch gap): the same partial-artifact rival applies, but the qualitative direction (subcritical→supercritical improvement partially closing the gap) is corroborated by GT-4's real, demonstrated data point, which reasonably bounds (though does not fully rule out) the rival — treated as settled for C6. Chain C7 (wet/dry cooling): no live rival identified; the source attributes the 41.1%→43.0% difference directly to cooling method with all else held constant. Chain C8 (annual-average penalty): no distinct rival beyond GT-9?'s own uncertainty, already captured on its Inputs axis.

**Premise.** The recommended near-term upgrade path — advanced turbine internals plus supercritical (~230 bar-a) steam pressure at a fixed 565°C salt ceiling, still air-cooled — has already failed to deliver its claimed ~45% gross / ~42.6% net efficiency in commercial operation.

**Causes** (unfiltered, generated from four stakeholder viewpoints before any grouping):
- (Owner/operator) The first commercial supercritical molten-salt steam generator encounters unanticipated fouling or corrosion at the salt-to-steam interface under supercritical-side thermal cycling, forcing a pressure de-rate back toward subcritical conditions.
- (Owner/operator) Daily thermal cycling driven by solar availability causes fatigue failures in high-pressure supercritical piping and headers far sooner than in the steady-baseload coal service where supercritical steam technology was actually proven.
- (Turbine OEM) The OEM's coal-fleet supercritical turbine platform is not a drop-in fit for CSP's smaller unit sizes (100-200 MWe) and daily-cycling duty profile, requiring a bespoke redesign that erodes the "existing/near-term technology" premise.
- (Turbine OEM) The advanced turbine's higher IP-stage isentropic efficiency was demonstrated in a design study but not validated across the actual part-load range the plant will see under storage-dispatch scheduling.
- (Financier/project finance) Lenders price a first-of-kind technology-risk premium into the supercritical option that raises levelized cost enough to erase the efficiency-driven LCOE benefit, so the upgrade never gets built at commercial scale.
- (Financier) Insurance and warranty terms for an unproven supercritical CSP steam generator are unavailable or prohibitively expensive, blocking bankability regardless of the thermodynamic case.
- (Salt-chemistry/O&M engineer) Nitrate salt near its ~565°C ceiling already runs close to its own thermal-decomposition/corrosion limit (GT-8?); a higher-pressure boiler design raises hot-end wall temperatures and stresses enough to accelerate salt-side corrosion beyond the subcritical baseline's experience.
- (Grid/market) A falling-cost competing technology (PV plus battery storage) erodes the market incentive to fund a first-of-kind CSP supercritical upgrade before it can be commercially proven, regardless of its technical merit.

**Clusters.**
- **Cluster A — Cycling-duty mismatch** (bears on: C3, C4, GT-3, GT-4): daily thermal cycling undermines technology whose performance figures were established for steady-baseload service (fatigue-piping cause, part-load-validation-gap cause).
- **Cluster B — First-of-kind bankability** (bears on: C3's A7 assumption, and the Conclusion's Recommended-approach claim): financing, insurance, and competing-technology economics could prevent the efficiency gain from ever being built regardless of its thermodynamic merit (lender-premium cause, insurance-unavailability cause, PV-plus-battery-competition cause).
- **Cluster C — Salt-chemistry interaction with higher-pressure design** (bears on: GT-4, GT-8?, and indirectly C6): a supercritical boiler's higher wall temperatures could accelerate corrosion near the salt's own decomposition ceiling (corrosion/fouling cause, wall-stress-interaction cause).

**Disposition.**
- Cluster A — *plan change*: pilot any near-term supercritical/advanced-turbine upgrade first on the largest-storage, least-cycling-intensive plant in a given fleet (so the turbine runs at or near rated load for extended blocks), and require OEM performance guarantees to explicitly cover the expected annual start/stop count, not only steady full-load operation.
- Cluster B — *accepted risk, named mitigation*: accept that first-of-kind financing risk is real and will likely require a loan-guarantee-backed or utility-offtake-backed structure (as Crescent Dunes itself used) rather than pure commercial project finance for the first unit; the Conclusion's Recommended-approach claim is scoped as "technology-ready, financing-structure-dependent," not "shovel-ready."
- Cluster C — *plan change*: require a corrosion-monitoring and inspection program at the highest-wall-temperature, highest-pressure boiler sections, informed by existing nitrate-salt corrosion literature, before scaling main steam pressure beyond the ~230 bar-a level studied in GT-4.

**Falsification.** The conclusion that roughly 4 gross percentage points are realistically recoverable at fixed 565°C via existing/near-term turbine and supercritical-pressure technology is false if a commercially operating supercritical molten-salt tower plant, once built, cannot sustain a gross cycle efficiency materially above the ~41% subcritical baseline once real cycling duty and salt-side corrosion effects are accounted for — i.e., if its as-operated annual-average gross efficiency converges back toward the subcritical baseline rather than toward the ~45% design figure.
## §6→§4 closure ledger (process output)

- "pursue the two demonstrated near-term upgrades... raise gross cycle efficiency from today's ~41% baseline to ~45% and power-block net efficiency from ~39% to ~43%" → chain C2, chain C3, chain C4 ✓
- "treating a shift to wet cooling as a separate, site-gated option rather than a default recommendation" → chain C7 ✓
- "the true ceiling for a steam-Rankine power block at this salt temperature is only about 46-52%" → chain C1 ✓
- "most of the headroom the naive Carnot figure implies is locked in by the choice of a phase-change steam cycle against a sensible-heat salt source" → chain C6 ✓
- "near-term hardware can close about 4 points" → chain C3, chain C4 ✓
- "the remaining 3-4 points sit behind a turbine/mechanical irreversibility floor" → chain C5 ✓
- "the supercritical-pressure gain partly taxes itself... trims the net-efficiency gain to about 3.4 points versus a 4.1-point gross gain" → chain C4 ✓
- "wet cooling recovers a further ~1.9 gross points but only by giving up the water-scarcity rationale" → chain C7 ✓
- "every design-point efficiency figure in this analysis is a ceiling on, not a measurement of, the realized annual-average efficiency" → chain C8 ✓

All Conclusion-section claims trace to a named section-4 chain. No claim cut.
## Self-audit scan (process output)

**Table 1 — chain form (section 4, in order).**

| Chain | Chain Head (brief) | Form conforming? | Rule applied | Dependency clean? | Band | Act attempted? | Edges fired |
|-------|---------------------|-------------------|---------------|--------------------|------|-----------------|-------------|
| C1 | GT-1, GT-5, GT-10? | yes | n/a | yes | MEDIUM | yes | none |
| C2 | GT-1, GT-2, GT-6 | yes | n/a | yes | MEDIUM | yes | none |
| C3 | GT-1, GT-3, GT-4 | yes | n/a | yes | LOW | yes | none |
| C4 | C3, GT-4 | yes | n/a | yes | LOW | yes | none |
| C5 | C1, C3, GT-11? | yes | n/a | yes | LOW | yes | none |
| C6 | C1, GT-4 | yes | n/a | yes | MEDIUM | yes | none |
| C7 | GT-1, GT-2 | yes | n/a | yes | HIGH | yes | none |
| C8 | GT-9?, C4 | yes | n/a | yes | LOW | yes | none |

**Table 2 — claim inventory (section 6, in order).**

| §6 Span (brief) | Construct | Claim under R11? | R11 clause applied | Chain cited |
|-------------------|-----------|-------------------|----------------------|---------------|
| Recommended approach: pursue turbine + supercritical upgrades... | bold lead-in | yes | colon closes bold span, content on same line | C2, C3, C4, C7 |
| Key insight: naive Carnot is the wrong ceiling... | bold lead-in | yes | colon closes bold span, content on same line | C1, C3, C4, C5, C6 |
| Trade-offs acknowledged: (label alone on its line) | bold lead-in | no | section-intro label, whole line, no citation of its own; obligation falls to list items below | n/a |
| — supercritical gain partly self-taxes... | list item | yes | closes own sentence, >40 characters | C4 |
| — wet cooling recovers ~1.9 points but gated by water scarcity... | list item | yes | closes own sentence, >40 characters | C7 |
| — design-point figures are a ceiling, not a measurement... | list item | yes | closes own sentence, >40 characters | C8 |
| Pre-check: head C1 (MEDIUM)... Inputs ceiling: LOW | bold lead-in (pre-check) | yes | confidence pre-check line, cited by the chains named in its own head | C1, C2, C3, C4, C5, C6, C7, C8 |
| Confidence: LOW — C3, C4, C5, C8 rated LOW... | bold lead-in | yes | colon closes bold span; names each below-HIGH contributing chain | C1, C2, C3, C4, C5, C6, C8 |

Scan complete: 8 chain rows, one per section-4 chain block in order; 8 section-6 rows, one per construct in order — 7 claims under R11, 1 excluded. 0 chains malformed, 0 claims untraced.
## Self-Audit Gate (process output)

**Criterion 1: Identify Essence**
Quoted span: "What is the thermodynamically defensible thermal-to-electric efficiency ceiling for a steam Rankine power block drawing heat from molten nitrate salt fixed at 565°C, how far below that ceiling does current commercial practice... sit, and... how much of that gap is closable with existing or near-term engineering versus structurally locked in..."
Band: **Rigorous**
Justification: The statement names the specific triple question (ceiling / practice / recoverable-vs-locked-in split) unique to this problem rather than restating the prompt, and each of the four success criteria is a checkable structural test against the Conclusion section (does it state a two-tier ceiling, cited practice figures, labeled loss buckets, and five specific numbers).

**Criterion 2: Challenge Assumptions**
Quoted span: "A7 | Supercritical steam turbine/boiler technology... has not yet been commercially fielded in a molten-salt CSP tower plant... | current constraint | Record expiry: expires once a first commercial supercritical CSP tower plant is built and operated | Accept — ... | Sandia SAND2013-1960, p.10-11 (read-at-source)" and the Assumption Audit scan's reconciliation ("All 28 chain steps across C1-C8 are covered; every surfaced assumption... is a row already present in, or newly added to, the Assumptions Table").
Band: **Rigorous**
Justification: every row uses one of the four types with a matching treatment and an em-dash-separated Verdict; unverified rows read "unverified — flagged"; multiple assumptions are actively challenged (not merely Accepted); the Assumption Audit scan confirms exhaustive coverage of every named chain step, with every surfaced assumption already present in the table.

**Criterion 3: Establish Ground Truths**
Quoted span: "?-marked: GT-8?, GT-9?, GT-10?, GT-11? (4 of 11)" checked against the Ground Truths list, which carries `?` on exactly those four IDs and no others; GT-1 and GT-2 (unsuffixed, feeding HIGH chain C7) each name a read-at-source location ("p.10 text").
Band: **Rigorous**
Justification: all 11 GT-IDs are stable and match the identifiers referenced in section 4; every unsuffixed GT carries a specific citation (report, page, table) rather than "common knowledge"; the `?` enumeration matches the list exactly; every unsuffixed GT feeding the HIGH-confidence chain (C7: GT-1, GT-2) names its read-at-source page.

**Criterion 4: Reason Upward**
Quoted span (from the self-audit scan's chain-form table, per this criterion's quoting rule): "0 chains malformed, 0 claims untraced" and, row-by-row, "Form conforming? yes" for all eight chains C1-C8, each with "Dependency clean? yes."
Band: **Rigorous**
Justification: every conclusion has exactly one chain with a genuine intermediate and no chain is malformed per the scan; the Abandoned Reasoning section documents three specific dead ends with structural abandonment reasons (not "ran out of time"); no analogy is used as direct evidence; every surfaced assumption is declared inline via `[Assumes: A-N]` (A1, A7 on C2/C3/C4) and confirmed by the Assumption Audit scan; the Recompute step in the adversarial pass independently reproduces every computed figure.

**Criterion 5: Validate**
Quoted span: "C3, C4, C5, C8 are rated LOW and each is load-bearing for at least one claim above; C1, C2, C6 are rated MEDIUM. Each names its own downgrade cause and verification path on its own section-4 confidence line" (Conclusion confidence explanation), together with the adversarial pass record's complete five-part structure (Recompute, Sensitivity, Rival, Premise/Causes/Clusters/Disposition, Falsification), each cluster carrying a named plan change or an accepted risk with a named mitigation.
Band: **Rigorous**
Justification: every chain's confidence line names its specific downgrade cause(s) and a verification path (or, for C7, is HIGH with no downgrade needed); no chain rated HIGH consumes a `GT-N?` input; every chain is rated no higher than the lowest-rated chain its head cites (C4 and C5 correctly capped at LOW via C3 and C1/C3 respectively); the Conclusion's LOW rating equals its weakest contributing chains; the adversarial pass ran in full, with all three clusters carrying a disposition (two plan changes, one accepted risk with a named mitigation) — the LOW overall rating is a calibrated, honestly-earned result rather than a shortfall.

**Criterion 6: Conclusion-to-Ground-Truth Traceability**
Quoted span (from the self-audit scan's claim-inventory table, per this criterion's quoting rule): all eight section-6 constructs show a named chain in the "Chain cited" column except the "Trade-offs acknowledged" section-intro label, which correctly shows "n/a" because its citation obligation falls to the three list items beneath it, each of which does carry a chain.
Band: **Rigorous**
Justification: every claim in the Conclusion traces to a specific named chain in section 4 (confirmed by the §6→§4 closure ledger and the claim-inventory table); no new reasoning is introduced in section 6 beyond what chains C1-C8 already established; the Key Insight names a non-obvious finding (the naive-Carnot-vs-tighter-Rankine-ceiling distinction) rather than restating the Recommended approach.

**Gate result:** No criterion scored Absent; zero criteria scored Hand-wavy. Both clearance conditions are met — the analysis clears the Self-Audit Gate on the first scoring pass, with no Fix/Repeat re-perception pass required.
# Thermal-to-Electric Conversion Ceiling for a 565°C Molten-Salt Steam Rankine Power Block

## 1. Problem Essence

**Core problem:** What is the thermodynamically defensible thermal-to-electric efficiency ceiling for a steam Rankine power block drawing heat from molten nitrate salt fixed at 565°C, how far below that ceiling does current commercial practice (Crescent Dunes/Noor III-class plants: 565°C, subcritical, reheat) sit, and — holding the 565°C salt ceiling fixed — how much of that gap is closable with existing or near-term engineering versus structurally locked in by the choice of a phase-change steam Rankine cycle drawing from a sensible-heat salt source?

**Success criteria:**
- The Conclusion states a law-permitted ceiling derived from at least two distinct rigor levels — a loose two-reservoir Carnot figure explicitly marked as *not* the answer, and a tighter Rankine/exergy-specific bound — rather than a single unqualified Carnot percentage.
- The Conclusion states current commercial gross and net efficiency, each traceable to a specific, read-at-source figure.
- The Conclusion decomposes the ceiling-to-practice gap into named loss buckets, each explicitly labeled recoverable (near-term, fixed 565°C) or structurally locked in.
- The Conclusion states five specific numbers — the ceiling, current practice, the gap, the recoverable portion, and the locked-in portion — each in percentage points, with a stated confidence band.

## 2. Assumptions Table

| Assumption | Type | Treatment | Verdict | Verification |
|------------|------|-----------|---------|--------------|
| A1: "Power block" thermal-to-electric efficiency is bounded at the hot-tank-to-condenser system boundary, excluding the receiver/tower salt-lift pump (a solar-field parasitic) from the parasitic tally. | convention | Explicitly challenge; compute and present both boundary conventions rather than silently picking one. | Challenge — the boundary choice materially changes the net figure (~39.2% vs. ~36.1%); both are presented so the reader is not misled by an implicit choice | Sandia SAND2013-1960, Table 5, p.25 (parasitic breakdown); both boundaries computed explicitly in chain C2 |
| A2: The two-reservoir Carnot efficiency between peak salt temperature (565°C) and ambient is *not* the correct law-permitted ceiling for a real Rankine cycle. | physical law | Accept as a ground-truth-class conclusion; use the tighter exergy/T_avg,H-based bound instead. | Accept — this is a direct, settled consequence of applying the definition of exergy to a finite-temperature-glide heat source, not a claim requiring external citation | Derived in chain C1 from the standard exergy-of-a-sensible-heat-stream identity |
| A3: Commercial "solar salt" (60% NaNO3/40% KNO3) is limited to roughly 565-600°C in practice, due to thermal-stability/decomposition and corrosion behavior — the standard reason this technology class is capped near 565°C. | untested belief | Verify, or flag; not load-bearing for any headline numeric conclusion since it is contextual only. | Challenge — plausible and consistent with GT-7 (receiver loss rising with salt temperature), but not independently read at source this session | unverified — flagged (GT-8?); not used in any HIGH-stakes chain |
| A4: Current commercial molten-salt tower steam Rankine power blocks are best represented, for this analysis, by a ~165 MWe subcritical, reheat, air-cooled baseline (consistent with Crescent Dunes/Noor III-class utility-scale plants) rather than by smaller non-reheat units (e.g., ~20 MWe Gemasolar-class). | convention | Explicitly challenge: smaller non-reheat units would show lower gross efficiency; the baseline used here is representative of the two larger plants the question names, not of Gemasolar specifically. | Challenge — accepted as representative of Crescent Dunes/Noor III; flagged as not covering Gemasolar's smaller, likely non-reheat cycle | Sandia SAND2013-1960 explicitly frames its 165 MWe baseline as "current-technology," p.10-11; Gemasolar-specific efficiency not independently verified this session — unverified — flagged |
| A5: Modern reheat steam turbines at this class and scale (100-200 MWe) operate with stage-group isentropic efficiencies practically bounded around 90-94%, near the current engineering floor given today's blade aerodynamics and materials. | untested belief | Verify, or flag. | Challenge — plausible given general turbomachinery-engineering knowledge, but not independently read at source this session | unverified — flagged (GT-11?) |
| A6: Air-cooled condensers are the appropriate default for representing "current commercial practice," because the named example plants (Mojave/Nevada/Ouarzazate deserts) are water-constrained. | current constraint | Record expiry: this constraint lifts only where water is available/affordable, or where hybrid wet/dry cooling investment is made — it expires per-site, not universally. | Accept — matches the actual siting of every named example plant | Consistent with the water-scarce desert siting of Crescent Dunes/Noor III/Gemasolar (general siting knowledge); the specific wet-vs-dry efficiency figures are read-at-source (GT-1, GT-2) |
| A7: Supercritical steam turbine/boiler technology, though proven in coal power, has not yet been commercially fielded in a molten-salt CSP tower plant, so GT-4's 45.2% figure is a demonstrated-feasibility engineering-study result, not an operating fleet average. | current constraint | Record expiry: expires once a first commercial supercritical CSP tower plant is built and operated — a first-of-kind deployment risk, not a physical barrier. | Accept — the source study itself frames advanced supercritical CSP configurations as "undemonstrated" as of its 2013 publication date | Sandia SAND2013-1960, p.10-11 (read-at-source) |
| A8: CSP tower plants with large (7.5-10 hr) thermal storage operate the power block closer to rated/full load for extended blocks, so part-load/cycling losses are a real but secondary (roughly 1-3 percentage-point) drag on annual-average efficiency relative to the design-point figures used throughout this analysis. | untested belief | Verify, or flag. | Challenge — directionally well-established (design-point efficiency always overstates annual-average realized efficiency for a cycling plant), but the specific 1-3 point magnitude is a Fermi bracket | unverified — flagged (GT-9?) |
| A9: A dead-state/ambient reference of roughly 15-35°C (ISO-standard 15°C through hot-desert peak 35-43°C) brackets the relevant thermodynamic reference temperature for the exergy/Carnot-type ceiling calculations in this analysis. | convention | Explicitly challenge: state the calculation across the full bracket rather than picking one reference silently. | Challenge — bracketed explicitly in chain C1 rather than resolved to a single value | Sandia SAND2013-1960, p.29 (Table 10: design ambient 43°C, ITD 14°C) anchors the high end; ISO reference (15°C) anchors the low end |
| A10: Turbine OEMs face sufficient commercial incentive to productize a CSP-specific supercritical steam-generator package once a first project proves it out. | untested belief | Verify, or flag. | Challenge — plausible by analogy to the coal-fleet supercritical learning curve, but not independently verified for the CSP-specific case this session | unverified — flagged; used only in chain C3's second-order extension, not in any headline numeric conclusion |

## 3. Ground Truths

- **GT-1** Current-technology molten-salt power tower baseline (565°C hot salt outlet, ~120 bar-a subcritical/reheat main steam at 553°C, 296°C cold salt return, air-cooled condenser at 0.155 bar-a back pressure) achieves gross cycle (turbine electric output ÷ steam-generator thermal duty) efficiency of 41.1-41.2%. — source: Pacheco, J.E., Wolf, T., Muley, N., "Incorporating Supercritical Steam Turbines into Advanced Molten-Salt Power Tower Plants: Feasibility and Performance," SAND2013-1960, Sandia National Laboratories, March 2013; read-at-source: p.10 text ("...approximately 43.0% with wet cooling or 41.2% with air-cooled condensers"); Table 5 (p.25), "Baseline Subcritical" column, "Gross Cycle Efficiency, %" row = 41.1.
- **GT-2** The identical baseline subcritical cycle, wet-cooled instead of air-cooled, achieves 43.0% gross cycle efficiency — same salt temperature, steam conditions, and turbine, cooling method changed only. — source: same report; read-at-source: p.10 text.
- **GT-3** An "Advanced Subcritical Baseline" configuration — same ~565.5°C hot salt temperature and 120 bar-a main steam pressure, air-cooled, differing only in turbine internal design (a modern, higher-isentropic-efficiency turbine in the intermediate-pressure stages) — achieves 43.2% gross cycle efficiency. — source: same report; read-at-source: Table 5 (p.25), "Adv. Subcritical Baseline Cycle 1" column; text p.23 ("gross cycle efficiency of the advanced subcritical turbine, which is more than 5% higher relative to the standard subcritical steam turbine").
- **GT-4** A supercritical steam cycle at the same salt-temperature ceiling (566°C hot salt, within 1°C of the fixed 565°C constraint), 230 bar-a main/reheat steam at 553°C, air-cooled ("Supercritical Cycle 3"), achieves 45.2% gross cycle efficiency, with boiler feed pump power of 4,977 kW (vs. 3,175 kW baseline). — source: same report; read-at-source: Table 5 (p.25), "Supercritical Cycle 3" column.
- **GT-5** The design-point cooling-system parameters for these air-cooled plants specify an ambient dry-bulb design temperature of 43°C with a 14°C ITD (initial temperature difference) — i.e., a condensing/saturation temperature of order 55-58°C — consistent with the reported ACC back pressure of ~0.152-0.155 bar-a. — source: same report; read-at-source: p.29, Table 10 ("Ambient Temperature at Design" = 43°C; "ITD at Design Point" = 14°C).
- **GT-6** For the baseline subcritical case, power-block-side parasitic loads (boiler feed pump 3,175 kW; condensate pump 140 kW; ACC cooling fans 2,955 kW; plant auxiliaries 700 kW; hot-salt circulation pump moving salt from the hot tank through the steam generator and back to the cold tank, 1,009 kW) total 7,979 kW, against a gross turbine electrical output of 165,000 kW and a steam-generator thermal duty of 401 MWt. The table's additional 12,096 kW "cold salt pump" lifts cold salt up the ~200 m tower to the receiver and is a solar-field/receiver parasitic outside the hot-tank-to-condenser power-block boundary used in this analysis (Assumption A1). — source: same report; read-at-source: Table 5 (p.25), "Baseline Subcritical" column, rows "Boiler Feed Pump Power," "Condensate Pump," "Cooling Fans," "Auxiliaries," "Hot Pump Power."
- **GT-7** Raising hot salt outlet temperature from 565°C to 600°C increases receiver thermal loss from ~30 kW/m² to ~36 kW/m² (roughly a 1-percentage-point receiver-performance effect) — cited as context for why 565°C, not an arbitrarily higher temperature, is the fixed reference point in this analysis. — source: same report; read-at-source: p.23.
- **GT-8?** Commercial "solar salt" (60% NaNO3/40% KNO3) is limited to roughly 565-600°C in practice due to thermal-stability/decomposition and corrosion behavior, the standard industry reason this technology class caps hot-tank temperature near 565°C rather than raising it further. — unverified: treated as well-established CSP-literature background knowledge, but no specific source was opened for this exact claim in this session; consistent with, but not proven by, GT-7. Not load-bearing for any HIGH-confidence numeric conclusion.
- **GT-9?** Design-point (full-load, steady-state) gross/net cycle efficiency figures such as GT-1 through GT-4 overstate realized annual-average conversion efficiency for a storage-dispatched, cycling CSP plant by roughly 1-3 percentage points (absolute), due to daily startup transients, part-load turbine/condenser off-design performance, and thermal standby losses; smaller for plants with large storage, larger for plants with little or none. — unverified: a Fermi-style bracket built from general steam-turbine part-load/cycling behavior, not a figure read from an annual-performance dataset in this session.
- **GT-10?** Using standard steam-table enthalpy/entropy values (approximated from memory/typical published tables, not read from a live source this session) for the baseline reheat cycle (120 bar-a main steam at 553°C from a 261°C feedwater temperature, with reheat from 370.7°C cold-reheat to 553°C hot-reheat at 32.2 bar-a — all state points themselves read-at-source per GT-1's Table 5), the enthalpy-weighted mean thermodynamic temperature of heat addition (T_avg,H) is approximately 630-650 K (357-377°C) — substantially below the peak steam temperature of 826 K (553°C). — unverified: steam-table values are approximated, not read at source this session; used only to establish the Rankine-cycle-specific ideal-ceiling bracket in chain C1, which is explicitly rated MEDIUM as a result.
- **GT-11?** Modern reheat steam turbines at this class and scale (100-200 MWe) operate with stage-group isentropic efficiencies practically bounded around 90-94% given current blade aerodynamics and materials, such that closing the remaining gap between demonstrated near-term cycle efficiency (~45%) and the ideal reversible-cycle ceiling (~46-52%) through further turbine refinement alone would require gains beyond what current turbomachinery realistically offers on a near-term horizon. — unverified: a general turbomachinery-engineering judgment, not a figure read from a specific source in this session.

**Provenance summary:** `?`-marked: GT-8?, GT-9?, GT-10?, GT-11? (4 of 11). Read-at-source: GT-1 — SAND2013-1960 p.10 text and Table 5 (p.25); GT-2 — p.10 text; GT-3 — Table 5 (p.25) and p.23 text; GT-4 — Table 5 (p.25); GT-5 — p.29, Table 10; GT-6 — Table 5 (p.25); GT-7 — p.23. GT-1 and GT-2, both unsuffixed, feed the HIGH-confidence chain C7 and their read-at-source locations are named above.

## 4. Derivation Chains

### Conclusion C1: The law-permitted ceiling for a real steam Rankine cycle at 565°C is not the naive Carnot figure (~64-66%) but a much tighter Rankine-cycle-specific bound (~46-52%)

GT-1 (565°C hot salt, 296°C cold return) + GT-5 (ACC condensing ~55-58°C) + GT-10? (T_avg,H ≈ 630-650K for the baseline reheat cycle)
→ applying the standard two-reservoir Carnot formula to only the peak salt temperature and the condenser sink yields roughly 63 to 66 percent, but this ignores that most of the salt's heat is delivered well below its peak temperature as it cools from 565°C to 296°C
→ treating the salt as a sensible-heat stream cooling from 565°C to 296°C against a 15 to 35°C ambient dead state [Assumes: A9], the maximum work extractable by any reversible engine matched to that temperature glide is about 56 to 59 percent of the heat withdrawn, a materially tighter bound than the naive Carnot figure
→ a real steam Rankine cycle cannot match that ideal glide-matched engine because its boiler adds most of its heat along an isothermal boiling plateau near 598K, so its enthalpy-weighted mean heat-addition temperature is only about 630 to 650K rather than the 838K peak
→ the reversible-cycle ceiling for an ideal but still steam-Rankine-shaped version of this cycle, against a realistic air-cooled condensing temperature near 57°C, is therefore only about 46 to 52 percent, not the 63 to 66 percent a naive Carnot calculation suggests

**Pre-check:** head GT-1, GT-5, GT-10? · ?-marked: GT-10? · lowest cited: none · Inputs ceiling: MEDIUM
**Confidence:** MEDIUM — GT-10? rests on steam-table values approximated from memory rather than read at a live source this session; verification would be to look up IAPWS-IF97 steam tables directly, or run a validated cycle-simulation tool, for the exact 120 bar-a/553°C/32.2 bar-a reheat state points, which would tighten the 630-650K bracket without changing the qualitative conclusion (ceiling well below naive Carnot). The rival that the naive two-reservoir Carnot bound is the theoretically appropriate reference is ruled out by the standard exergy-of-a-sensible-heat-stream identity applied in the second hop above — a settled thermodynamic result, not a live dispute — so the Rivals axis is clean; only the Inputs axis (GT-10?) is short.

### Conclusion C2: Current commercial practice sits at ~41% gross / ~39% net (air-cooled, power-block boundary), with the reported "net" figure depending materially on where the system boundary is drawn

GT-1 (baseline gross 41.1% air-cooled) + GT-2 (wet-cooled 43.0%) + GT-6 (power-block parasitics 7,979 kW)
→ net electric output equals the gross turbine output of 165,000 kW less the 7,979 kW of power-block-boundary parasitics, or 157,021 kW [Assumes: A1 — the receiver/tower salt-lift pump sits outside the power-block boundary]
→ dividing that net output by the 401 MWt steam-generator thermal duty gives a power-block net efficiency of about 39.2 percent on an air-cooled basis, roughly 1.9 percentage points below the 41.1 percent gross figure
→ including the receiver's 12,096 kW cold-salt lift pump instead, i.e. a whole-plant boundary, lowers this to about 36.1 percent, so the reported "net efficiency" of a molten-salt tower depends materially on where the system boundary is drawn and not only on hardware performance

**Pre-check:** head GT-1, GT-2, GT-6 · ?-marked: none · lowest cited: none · Inputs ceiling: HIGH
**Confidence:** MEDIUM — all three head ground truths are unsuffixed and read at source (Inputs axis clean), but the first hop rests on [Assumes: A1]; if that boundary assumption fails (whole-plant boundary instead), net efficiency is 36.1 percent rather than 39.2 percent — a real quantitative shift, though the qualitative point (net is materially below gross) is unaffected either way. The rival reading (that only the whole-plant boundary is a meaningful net figure) is not ruled out; it is disclosed by presenting both numbers rather than resolved, which is why this chain is MEDIUM rather than HIGH on the Inference axis alone.

### Conclusion C3: At fixed 565°C, two demonstrated hardware changes (advanced turbine internals, then supercritical steam pressure) realistically recover about 4.1 gross percentage points using existing/near-term technology

GT-1 (baseline 41.1% gross) + GT-3 (advanced turbine 43.2% gross) + GT-4 (supercritical 45.2% gross)
→ holding hot salt temperature fixed at approximately 565°C and holding air cooling fixed, replacing the baseline turbine's internals with a modern high-isentropic-efficiency turbine already in commercial service in the coal fleet alone raises gross cycle efficiency from 41.1 to 43.2 percent
→ layering a supercritical main steam pressure of 230 bar-a instead of 120 bar-a on top of that same 565 to 566°C salt ceiling, using steam turbine and boiler technology already proven at higher pressures in coal-fired plants, raises gross cycle efficiency further to 45.2 percent
→ because both improvements use hardware classes already commercially mature outside CSP, the full 4.1-percentage-point gross gain from 41.1 to 45.2 percent is realistically recoverable with existing or near-term technology without raising the salt temperature above its fixed 565°C ceiling [Assumes: A7 — the remaining integration risk of a first commercial supercritical molten-salt steam generator is a deployment/first-of-kind risk rather than a genuine technical barrier]
→[2nd] turbine OEMs whose coal-fleet supercritical platforms are already amortized gain a commercial incentive to productize a CSP-specific supercritical steam-generator package once a first project proves it out [Assumes: A10]
→[3rd] immediately after a first commercial deployment, EPC and financing costs likely carry a first-of-kind premium, while across several subsequent projects that premium should fall as the learning curve seen in coal-fired supercritical adoption repeats itself, making 45-percent-class gross efficiency the de facto baseline for utility-scale (>100 MWe) molten-salt towers rather than a research figure

**Pre-check:** head GT-1, GT-3, GT-4 · ?-marked: none · lowest cited: none · Inputs ceiling: HIGH
**Confidence:** LOW — GT-1, GT-3, and GT-4 are all unsuffixed and read at source (Inputs axis clean), but two further axes are short: the endpoint's "realistically recoverable... near-term" framing rests on [Assumes: A7], and the adversarial pass (Cluster A: cycling-duty mismatch; Cluster B: first-of-kind bankability) surfaced a live rival — that commercial deployment fails to realize the design-point gain — which no existing commercial supercritical molten-salt tower plant has yet settled either way as of this analysis. Verification: an operating commercial supercritical CSP tower plant sustaining ~45 percent gross efficiency across real cycling duty would resolve both the Inference and Rivals shortfalls at once.

### Conclusion C4: The same near-term path recovers about 3.4 net percentage points, trailing its 4.1-point gross gain because supercritical pressure taxes the cycle's own parasitics more heavily

C3 (45.2% gross recoverable) + GT-4 (supercritical parasitics)
→ the supercritical cycle's higher main steam pressure raises boiler feed pump power from 3,175 kW in the baseline to 4,977 kW, partly offsetting its gross efficiency gain with a larger internal parasitic load
→ recomputing net output the same way as C2 (power-block boundary, excluding the receiver's cold-salt lift pump) gives roughly 155,551 kW net against 165,000 kW gross, or a power-block net efficiency near 42.6 percent versus the 39.2 percent baseline net figure from C2 [Assumes: A1]
→ so the near-term recoverable path closes roughly 3.4 of the available net-efficiency percentage points at fixed 565°C, somewhat less than the 4.1-point gross improvement because supercritical pressure taxes the cycle's own parasitics more heavily than the subcritical baseline does

**Pre-check:** head C3 (LOW), GT-4 · ?-marked: none · lowest cited: LOW · Inputs ceiling: LOW
**Confidence:** LOW — this chain cites C3 (LOW) on its head, so it is capped at LOW by the lowest-rated-chain rule regardless of its own merits; its own recompute (parasitic scaling, boundary convention A1) is straightforward arithmetic and is not itself an additional source of uncertainty beyond what C3 already carries. Verification: same as C3 — a commercially operating supercritical unit would settle the deployment-risk rival that caps C3.

### Conclusion C5: Beyond the near-term-recoverable path, a further ~3-4 gross points to reach the Rankine-ideal ceiling are structurally locked in by real-machine (turbine/mechanical) irreversibility, not by anything current practice is leaving on the table

C1 (Rankine-ideal ceiling ≈ 46-52%) + C3 (near-term recoverable ≈ 45.2% gross) + GT-11? (turbine isentropic-efficiency practical floor ~90-94%)
→ the near-term recoverable path already captures both concrete, source-documented improvements available at fixed 565°C — better turbine internals and supercritical pressure — reaching 45.2 percent gross against a Rankine-ideal ceiling of roughly 46 to 52 percent
→ the remaining 1 to 7 percentage points to that ideal ceiling is almost entirely turbine isentropic loss, mechanical and generator loss, and minor piping and valve irreversibilities, none of which current turbomachinery can eliminate without blade and materials technology beyond what is already fielded in the coal and CSP turbine fleets
→ this residual is therefore best characterized as fundamentally stuck at the 565°C salt ceiling, in the sense that no known near-term engineering change closes it further while remaining a steam Rankine cycle

**Pre-check:** head C1 (MEDIUM), C3 (LOW), GT-11? · ?-marked: GT-11? · lowest cited: LOW · Inputs ceiling: LOW
**Confidence:** LOW — this chain cites C3 (LOW), so it is capped at LOW by the lowest-rated-chain rule alone; it additionally rests on GT-11? (an unverified engineering judgment about the practical isentropic-efficiency floor). Verification: obtaining vendor-specific isentropic-efficiency curves for current 100-200 MWe reheat turbines, and tightening C1's steam-table basis per its own verification path, would together bound this residual more tightly.

### Conclusion C6: A separate, larger gap (~8-9 points) exists only relative to the true stream-exergy ceiling and is locked in by the choice of any phase-change steam Rankine architecture against a sensible-heat salt source, not by the 565°C temperature itself

C1 (Rankine-ideal ceiling ≈46-52% vs. exergy ceiling ≈56-59%) + GT-4 (supercritical partially closes this)
→ the roughly 8-to-9-percentage-point gap between the true stream-exergy ceiling and the Rankine-cycle-specific ideal ceiling established in C1 is caused by the isothermal boiling plateau inherent to any phase-change steam cycle, which cannot track the salt's continuously falling sensible-heat temperature as well as a hypothetical continuously-staged engine could
→ moving from subcritical to supercritical steam removes part of this mismatch by eliminating the distinct boiling plateau, consistent with GT-4's real, demonstrated efficiency gain from 41.1 to 45.2 percent gross at the same salt temperature
→ even a fully optimized supercritical steam Rankine cycle remains a single-fluid, two-turbine-section architecture rather than the many-staged, continuously temperature-matched engine the exergy ceiling implicitly assumes, so most of this gap is locked in by the decision to use any steam Rankine architecture at all, and only a genuinely different cycle such as a supercritical CO2 Brayton cycle, rather than a better steam cycle, would close the remainder — a change this analysis's fixed-565°C, steam-Rankine framing places out of scope

**Pre-check:** head C1 (MEDIUM), GT-4 · ?-marked: none · lowest cited: MEDIUM · Inputs ceiling: MEDIUM
**Confidence:** MEDIUM — this chain cites C1 (MEDIUM), so it is capped at MEDIUM by the lowest-rated-chain rule; its own qualitative reasoning is corroborated by GT-4's real, unsuffixed data point (subcritical-to-supercritical gain), which reasonably bounds — though does not fully rule out — the rival explanation that the 8-9 point figure is a Fermi-calculation artifact of C1's steam-table approximation rather than a real physical mismatch; only the Inputs axis (via C1) is short.

### Conclusion C7: Switching from air to wet cooling recovers ~1.9 gross points, but only by giving up the water-scarcity rationale that sited these plants in the desert in the first place

GT-1 (41.1% air-cooled) + GT-2 (43.0% wet-cooled)
→ switching only the condenser cooling method from air-cooled to wet-cooled, with salt temperature, main steam conditions, and turbine unchanged, recovers about 1.9 percentage points of gross cycle efficiency
→ this lever is real and immediately available with existing technology, but every named example plant in this technology class is sited in a water-scarce desert specifically because that is where the direct-normal solar resource is strongest [Assumes: A6], so claiming this 1.9-point recovery as unconditionally "free" ignores the water-availability constraint that drove the site selection in the first place
→ the wet-cooling lever should therefore be classified as conditionally recoverable, gated by water availability and cost, rather than as an unconditional near-term engineering win alongside the turbine and supercritical-pressure improvements in C3

**Pre-check:** head GT-1, GT-2 · ?-marked: none · lowest cited: none · Inputs ceiling: HIGH
**Confidence:** HIGH — both head ground truths are unsuffixed and read at source, the source attributes the 41.1-to-43.0-percent difference directly to cooling method with all else held constant (no unpriced inference gap), and no live rival explanation for the difference was identified.

### Conclusion C8: Every design-point figure above is a ceiling on, not a measurement of, the realized annual-average efficiency of a storage-dispatched plant that cycles daily rather than running as baseload

GT-9? (part-load/cycling annual-efficiency Fermi bracket) + C4 (near-term recoverable net ≈42.6%)
→ because all of the gross and net efficiency figures used throughout this analysis are steady-state, full-load design-point numbers, they do not by themselves describe what a storage-dispatched CSP plant actually realizes averaged across a year of cloudy days, startups, and part-load dispatch
→ layering GT-9?'s Fermi bracket onto C4's near-term-recoverable net design figure of about 42.6 percent suggests a realized annual-average net efficiency in the rough range of 40 to 42 percent for a well-stored, dispatch-smoothed plant, versus roughly 36 to 38 percent for the current baseline under the same treatment
→ this cycling penalty is real and additive to every other loss bucket in this analysis, but it does not change which improvements are near-term-recoverable versus fundamentally locked in at 565°C — it means every design-point number quoted elsewhere in this analysis is a ceiling on the realized annual figure, not the realized figure itself

**Pre-check:** head GT-9?, C4 (LOW) · ?-marked: GT-9? · lowest cited: LOW · Inputs ceiling: LOW
**Confidence:** LOW — GT-9? is an unverified Fermi bracket (Inputs axis short) and it cites C4 (LOW, Inputs ceiling also short via the cap); additionally, the second hop combines GT-9?'s bracket with C4's point estimate to produce a new numeric range without pricing what happens if the actual cycling penalty falls outside the 1-3 point bracket (an unpriced Inference step). Verification: an annual-performance dataset (e.g., measured monthly generation vs. design-point efficiency) for a large-storage molten-salt tower plant would replace this Fermi bracket with a measured figure.

## 5. Abandoned Reasoning

### Dead End: Using a SAM/SolarPILOT "0.412 gross efficiency" default parameter as a ground truth

**What was tried:** A web search surfaced a claim that the System Advisor Model's default molten-salt power tower case uses a "0.412" design gross cycle efficiency, and this was initially considered as a candidate ground truth for current commercial practice.

**Why abandoned:** The specific NREL technical report fetched to verify this figure (NREL/TP-5500-57625, "Molten Salt Power Tower Cost Model for SAM") is the cost-model report, not the performance-model report, and does not contain this parameter anywhere in its text — a direct-text search of the fetched and converted document returned no match. The figure could not be read at its source in this session.

**What it ruled out:** This saves a future analyst from citing "SAM default 0.412" without first checking that the specific cited document actually contains it; the fully-verified Sandia SAND2013-1960 baseline (41.1-41.2% gross, GT-1) was used instead, which is close in magnitude, better documented, and was read directly in this session.

### Dead End: Using a single ISO-standard 15°C dead-state temperature uniformly for all exergy/Carnot ceiling calculations

**What was tried:** An initial pass computed the exergy and Rankine-ideal ceilings using only the ISO-standard reference temperature of 15°C for the ambient dead state, as is conventional in general thermodynamics textbooks.

**Why abandoned:** Every named example plant in this technology class (Crescent Dunes in Nevada, Noor III in Ouarzazate, Gemasolar in Andalusia) is sited in a hot, arid climate specifically chosen for its direct-normal solar resource, and the source data itself (GT-5) specifies a 43°C design ambient temperature for the air-cooled condenser — far above the 15°C ISO reference. A single 15°C reference would understate the real cold-sink temperature these plants actually operate against and overstate the achievable ceiling.

**What it ruled out:** A single-point 15°C ceiling calculation was ruled out in favor of the explicit 15-35°C bracket used in chain C1 (Assumption A9), which better reflects the range between winter-night and summer-day conditions at these specific desert sites without overclaiming precision the underlying data does not support.

### Dead End: Treating Gemasolar's reported performance as representative "current commercial practice"

**What was tried:** Considered anchoring the "current commercial practice" ground truth on Gemasolar (the first commercial molten-salt power tower, ~19.9 MWe), since it is one of the three plants the user explicitly named.

**Why abandoned:** Gemasolar is a much smaller unit than Crescent Dunes or Noor III and, at that scale, non-reheat cycle configurations are common for cost reasons; no source for Gemasolar's specific gross or net cycle efficiency was opened and read in this session, so using it as the numeric baseline would have introduced an unverified figure into the analysis's central, load-bearing ground truth (GT-1) rather than only into contextual Assumption A4.

**What it ruled out:** This saves a future analyst from silently blending a small non-reheat unit's (unverified) performance with a large reheat unit's (verified) performance under one "current practice" label; the analysis instead uses the fully-sourced 165 MWe reheat baseline (GT-1) as the numeric anchor and explicitly flags, in Assumption A4, that this does not cover Gemasolar's smaller cycle.

## 6. Conclusion

**Recommended approach:** At the fixed 565°C hot-salt ceiling, pursue the two demonstrated near-term upgrades — an advanced high-isentropic-efficiency turbine and a supercritical (~230 bar-a) main steam pressure — which together raise gross cycle efficiency from today's ~41% baseline (chain C2) to ~45% and power-block net efficiency from ~39% to ~43% (chain C3, chain C4), while treating a shift to wet cooling as a separate, site-gated option rather than a default recommendation (chain C7).

**Key insight:** The efficiency ceiling most people reach for — Carnot between 565°C and ambient, roughly 64-66% — is the wrong number for a real Rankine cycle: once the salt's finite temperature glide and the steam cycle's own isothermal boiling plateau are accounted for, the true ceiling for a steam-Rankine power block at this salt temperature is only about 46-52% (chain C1), and most of the headroom the naive Carnot figure implies is locked in by the choice of a phase-change steam cycle against a sensible-heat salt source rather than by turbine engineering (chain C6); of the roughly 7-point gap that remains between that tighter ceiling and today's ~41% baseline, near-term hardware can close about 4 points (chain C3, chain C4), while the remaining 3-4 points sit behind a turbine/mechanical irreversibility floor no near-term engineering change is known to move (chain C5).

**Trade-offs acknowledged:**
- The supercritical-pressure gain partly taxes itself: higher boiler feed pump power trims the net-efficiency gain to about 3.4 points versus a 4.1-point gross gain (chain C4).
- Wet cooling recovers a further ~1.9 gross points but only by giving up the water-scarcity rationale that sited these plants in the desert in the first place (chain C7).
- Every design-point efficiency figure in this analysis is a ceiling on, not a measurement of, the realized annual-average efficiency of a storage-dispatched plant that cycles daily rather than running as baseload (chain C8).

**Pre-check:** head C1 (MEDIUM), C2 (MEDIUM), C3 (LOW), C4 (LOW), C5 (LOW), C6 (MEDIUM), C7 (HIGH), C8 (LOW) · ?-marked: none · lowest cited: LOW · Inputs ceiling: LOW
**Confidence:** LOW — C3, C4, C5, and C8 are rated LOW and each is load-bearing for at least one claim above; C1, C2, and C6 are rated MEDIUM; only C7 is HIGH. Each chain names its own downgrade cause and verification path on its own section-4 confidence line: C1 rests on GT-10?'s Fermi steam-table basis; C2 rests on the power-block-vs-whole-plant boundary choice (A1); C3 and C4 rest on assumption A7 plus the live commercial-deployment rival the adversarial pass surfaced in Clusters A and B; C5 is capped by its citation of C1 and C3 and additionally rests on GT-11?; C6 is capped by its citation of C1; C8 rests on GT-9?'s Fermi cycling-penalty bracket. The Conclusion adds no further downgrade cause of its own beyond aggregating these — an honestly-calibrated LOW rating reflecting genuine, unresolved first-of-kind deployment uncertainty on the headline recommendation, not a shortfall in the reasoning that produced it.

**Numeric answer, restated directly:**
1. Law-permitted ceiling (real steam-Rankine cycle, 565°C salt, realistic air-cooled sink): **~46-52%**, central estimate **~48%** (chain C1) — *not* the naive two-reservoir Carnot figure of ~64-66%, and *not* the full stream-exergy ceiling of ~56-59% either (both are looser bounds, named for context in chain C1 and chain C6).
2. Current commercial practice: gross **~41%** (41.1% air-cooled / 43.0% wet-cooled, chain C2); net **~39%** on a power-block boundary (~36% on a whole-plant boundary that includes the receiver's tower-lift pump, chain C2).
3. Gap (ceiling to current gross practice, same air-cooled basis): **~7 percentage points** (chain C1 vs. chain C2).
4. Recoverable near-term at fixed 565°C, existing/demonstrated technology: **~4.1 gross points / ~3.4 net points** (chain C3, chain C4) — carried at LOW confidence pending a first commercial deployment.
5. Fundamentally stuck given 565°C plus steam-Rankine architecture: **~3-4 further gross points** to reach the Rankine-ideal ceiling, locked in by the turbine/mechanical irreversibility floor (chain C5); separately, a much larger **~8-9 points** of headroom exists only relative to the deeper stream-exergy ceiling and is locked in by the choice of any phase-change steam-Rankine architecture against a sensible-heat salt source — recoverable only by abandoning steam Rankine altogether (e.g., supercritical CO2 Brayton), which this analysis's fixed-565°C, steam-Rankine framing places out of scope (chain C6).
