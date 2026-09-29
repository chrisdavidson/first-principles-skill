## Techniques not applied (process output)

- theoretical-limit (Phase 1 essence-reframe invocation) — not applicable — the essence already explicitly separates "law-permitted ceiling" from "current practice" per the question's own framing; no reframe of a convention-vs-hard-bound conflation was needed at Phase 1. (theoretical-limit *does* fire at Phase 4 as the primary technique; only the Phase-1 invocation is not-applicable.)
- inversion (Phase 2 challenge-assumptions invocation) — not applicable — the assumption space was directly enumerable from the governing thermodynamic model and named engineering components without needing a dedicated failure-enumeration brainstorm; inversion is instead applied at Phase 5 to the headline conclusion (a technical claim, not a plan, per the pre-mortem/inversion decision rule).
- fishbone — not applicable — the assumption space was already well-bounded by the governing thermodynamic model and named engineering components; a breadth-first category brainstorm was not needed to surface it.
- estimate (Fermi/unit-factor rebuild) — not applicable — the governing quantities were computed from closed-form thermodynamic relations (Carnot/Lorenz formulas) and named, read-at-source engineering-report figures rather than rebuilt from independent unit-factors.
- trade-off — not applicable — the question is a single quantitative technical determination (a thermodynamic ceiling and a gap decomposition), not a choice among two or more viable options.
- pre-mortem — not applicable — the headline output is a technical claim, not a plan or recommendation of action; Phase 5's decision rule routes claims to inversion instead (which fires; see Adversarial pass record).

## Assumption Audit scan (process output)

| Chain | Step | Step Text (brief) | Assumption surfaced? | Added to Table? |
|-------|------|--------------------|-----------------------|------------------|
| C1 | 1 | naive Carnot vs. isothermal-source framing | none | n/a |
| C1 | 2 | Lorenz formula applied with T_H1/T_H2/T_C | A7 (Lorenz formula), constant-cp caveat | n/a — A7 already in table |
| C1 | 3 | correct ceiling is ~52-53%, not naive ~61% | none | n/a |
| C2 | 1 | net design-point efficiency, power-block scope | A16 (parasitic-scope boundary) | n/a — already in table |
| C2 | 2 | net design-point efficiency, whole-plant scope | none (alternate branch of A16) | n/a |
| C2 | 3 | current-practice design-point range ≈36-42% | none | n/a |
| C3 | 1 | annual-average derate applied to design-point | A13 (annual-average derate) | n/a — already in table |
| C4 | 1 | compute Curzon-Ahlborn efficiency | none | n/a |
| C4 | 2 | CA numerically close to annual-average figure | none | n/a |
| C4 | 3 | CA ruled out as ceiling; Lorenz bound stands | none | n/a |
| C5 | 1 | gap = ceiling − annual average ≈17-18 pts | none | n/a |
| C6 | 1 | ceiling-to-best-near-term-supercritical residual ≈7.0 pts | none | n/a |
| C6 | 2 | ceiling-to-typical-subcritical gap; supercritical closes part | none | n/a |
| C6 | 3 | gross-to-net and design-to-annual account for remainder | none | n/a |
| C7 | 1 | turbine + supercritical levers close 3-6 pts, corroborated by annual-energy/LCOE data | none | n/a |
| C7 | 2 | + parasitic/dispatch levers give combined recoverable ≈4-7 pts | A14-adjacent parasitic-reduction estimate (untabled specific) | yes — added as A19 |
| C7 | 3 | residual ≈11-14 pts has no known near-term fix | none | n/a |
| C7 | 4 | alt-salt chemistry and sCO2 excluded/uncertain, not counted | none (A14, A15 already cited) | n/a |
| C7 | 5 | headline split: ≈25-30% recoverable / ≈70-75% irreducible | none | n/a |
| C7 | 6 [2nd] | supercritical upgrade costs +$61/kWe but LCOE falls 7-10% (actor lens) | none (A17 already in table) | n/a |
| C7 | 7 [3rd] | recoverable margin realized only within towers actually built (time lens) | none (A18 already in table) | n/a |

Scan complete: 21 chain-step rows across 7 chains (C1–C7), in order. One genuinely new item surfaced during the audit and not previously distinguished in the Phase-2 table: **A19 — "near-term parasitic-load reduction and improved part-load/dispatch management recover roughly 1-2 percentage points, beyond the turbine/supercritical levers already captured in A3/A5" (untested belief)** — added to the Classified Assumptions Table below. All other surfaced items were already pre-declared (A7, A13, A14, A15, A16, A17, A18).

## Adversarial pass (process output)

**Recompute.** (1) Lorenz ceiling: T_H1=838.15K, T_H2=569.15K, T_C=330.15K → ln(838.15/569.15)=0.38701; ΔT=269.00; term=330.15×0.38701/269.00=0.47498; η=1−0.47498=0.52502 → **52.5%**, matches the value used throughout. (2) Naive Carnot: 1−330.15/838.15=0.60608 → **60.6%**, matches. (3) Curzon-Ahlborn: 1−√(330.15/838.15)=1−0.62763=0.37237 → **37.2%**, matches. (4) Gap: 52.5%−35%(C3 central)=17.5, rounded **≈17-18 pts**, matches C5. (5) Component cross-check: 9.3 (ceiling→advanced-subcritical gross) + ~3.5 (gross→net, midpoint of scope range) + ~3.5 (design→annual, GT-13? midpoint) ≈16.3, within rounding of the ≈17-18 total — consistent. All computed figures recompute cleanly; no arithmetic error found.

**Sensitivity.** The single most flip-relevant ground truth is **GT-13?** (the ≈3-4 point annual-average derate): it is `?`-marked and is the least-grounded figure feeding the headline gap and recoverable-fraction split. If the true annual-average derate is smaller (e.g., 1 point), the gap shrinks to ≈14-15 points and the ≈5-point recoverable estimate becomes a larger *fraction* (≈33-36%) without changing which conclusion (majority-irreducible) holds. Only an implausible derate (near zero, or negative) would meaningfully threaten the "majority irreducible" framing. Secondary sensitivity: **GT-12?** (no plant-specific efficiency figure found; the generic 165 MWe Sandia study is used as the current-practice proxy) — if named plants (Crescent Dunes, Gemasolar, Noor III, Cerro Dominador) perform materially worse than this study due to as-built differences, the gap widens and the recoverable *absolute* points (drawn from the same study's internal subcritical-vs-supercritical comparison) are largely unaffected, but the *baseline* against which they are measured shifts. Verification path for both: open a named plant's audited annual performance report (DOE/SolarPACES) and read the stated annual and design-point power-block efficiency directly.

**Rival.** Headline: the naive-Carnot figure (~61%) as the ceiling — ruled out within C1 itself and in Abandoned Reasoning Dead End 1 (GT-7's Lorenz formula supersedes it). CA (~37%) as the ceiling — ruled out in C4 and Dead End 2 (C2's design-point gross figure of 41.1% already exceeds η_CA, which is impossible for a genuine ceiling). C2 (achieved design-point range): a live, unsettled rival — "the actual named plants perform materially better or worse than this generic Sandia study" — nothing in this analysis fully settles it; GT-11? partially corroborates matching temperatures and cooling mode for Crescent Dunes but not its efficiency. C7 (recoverable/irreducible split): a live, bounded rival — "sCO2 Brayton delivers materially more recoverable efficiency at 565°C than assumed" — GT-14? flags this as uncertain and unestablished by any source located, not confidently ruled out, and is carried as an explicit caveat on the Conclusion's confidence line rather than resolved.

**Premise.** The headline conclusion — that the Lorenz ceiling is ≈52-53%, current annual-average practice is ≈35%, and of the ≈17-18-point gap roughly one-quarter is near/mid-term recoverable while three-quarters is irreducible under the fixed 565°C nitrate-salt constraint — has already turned out to be false.

**Causes** (unfiltered, generated from four viewpoints — thermodynamics engineer, CSP plant operator, technical auditor, competing-technology analyst):
1. (engineer) The Lorenz-cycle model's constant-cp assumption, or its status as *the* applicable bound versus a more refined variable-cp/multi-stream exergy analysis, could shift the ceiling by a point or two.
2. (engineer) The condenser temperature used (43°C+14°C ITD, a *design*-point figure) is compared against an *annual-average* achieved efficiency, mixing two different operating conditions.
3. (operator) GT-12?'s reliance on a generic 165 MWe Sandia study rather than the actual named plants could misrepresent real achieved efficiency if any plant's as-built turbine, cooling system, or parasitics differ materially from the study's assumptions.
4. (operator) GT-13?'s annual-average derate (≈3-4 points) is an engineering-judgment estimate, not confirmed by any plant's audited annual heat balance; real derates could be smaller or larger (Crescent Dunes had documented operability/reliability issues, though those bear on availability more directly than on instantaneous efficiency).
5. (auditor) C6's attribution of the ≈7.0-point ceiling-to-best-supercritical residual entirely to "glide-mismatch plus turbomachinery irreversibility, combined" is a plausibility statement; the Sandia source does not itself decompose this residual into its two causes.
6. (competitor-tech analyst) sCO2 Brayton or advanced recuperator technology might deliver a larger efficiency jump at 565°C than GT-14? assumes, since sCO2's core strength (compact, high-effectiveness recuperation) is not fundamentally tied to very high turbine-inlet temperature.
7. (competitor-tech analyst) The market-deployment observation used in C7's third-order extension (GT-17?) is unverified general industry knowledge and could be wrong in either direction.
8. (generalist) Quoting "≈25-30% recoverable / ≈70-75% irreducible" to this apparent precision, from a chain with several `?`-marked and judgment-call inputs, risks conveying false confidence despite MEDIUM confidence labels throughout.

**Clusters.**
- **Cluster A — Achieved-baseline and annual-average uncertainty** (causes 3, 4) — bears on GT-12?, GT-13?, C2, C3, C5, C7.
- **Cluster B — Ceiling-model precision** (causes 1, 2) — bears on GT-6, GT-7, C1.
- **Cluster C — Residual-decomposition precision** (cause 5) — bears on C6, C7.
- **Cluster D — Near-term-technology headroom uncertainty** (cause 6) — bears on GT-14?, C7.
- **Cluster E — False-precision / market-context caveats** (causes 7, 8) — bears on C7's second-order extension and the Conclusion's presentation.

**Disposition.**
- Cluster A — **costly but survivable**; named plan change: every chain's confidence line touching C2/C3/C5/C7 names GT-12? and GT-13? explicitly as the dominant downgrade cause and states the verification path (a named plant's audited annual performance report).
- Cluster B — **tolerable**; accepted risk, no further plan change — the design-point-vs-annual sink-temperature mismatch was already an explicit, disclosed simplification and shifts the ceiling by at most ~1-2 points.
- Cluster C — **tolerable**; accepted risk — C6 already states the ≈7.0-point residual is "a combined internal-cycle loss this analysis's sources do not further decompose," so no unsupported sub-attribution precision is claimed.
- Cluster D — **tolerable**; accepted risk, small — GT-14? already flags this and C7 already treats it as "a small, uncertain, not-separately-counted addition."
- Cluster E — **costly but survivable**; named plan change: every headline figure in §6 is presented as a range with an explicit MEDIUM confidence label and the specific `?`-marked inputs named, rather than as an unqualified point estimate.

**Falsification.** This conclusion is false if a plant-specific audited annual performance record shows 565°C-class molten-salt-tower annual-average net power-block efficiency outside roughly 30-40%; or if a credible engineering source shows an achievable near-term (≈10-year) 565°C supercritical-steam design-point net efficiency exceeding roughly 46-47% (meaning the irreducible component was overstated); or shows it cannot exceed roughly the ≈39% current-practice central estimate (meaning the ≈5-point recoverable margin does not exist).

## §6→§4 closure ledger (process output)

- "Evaluate the steam Rankine power block ... against the ≈52-53% Lorenz/exergy ceiling, not the naive ≈61% Carnot figure ... prioritize ... near-term levers ..." → chain C1, C7 ✓
- "The naive Carnot number overstates real headroom by roughly 8 points ...; ... roughly three-quarters ... irreducible ..." → chain C1, C7 ✓
- "The recoverable ≈3-6 points are not free ... 7-10% lower whole-plant LCOE ..." → chain C7 ✓ ; trailing caveat ("new nitrate-salt tower construction has slowed ...") → no chain — flagged assumption only
- "**Confidence:** MEDIUM — the Conclusion rests most heavily on C7 ..." → chain C1, C2, C3, C4, C5, C6, C7 ✓

## Self-audit scan (process output)

| Chain | Chain Head (brief) | Form conforming? | Rule applied | Dependency clean? | Band | Act attempted? | Edges fired |
|-------|---------------------|-------------------|---------------|--------------------|------|-----------------|-------------|
| C1 | GT-1+GT-2+GT-6+GT-7 (Carnot, Sandia temps, ACC design point, Lorenz formula) | yes | n/a | yes | HIGH | yes | none |
| C2 | GT-3+GT-4 (Sandia gross efficiencies, itemized parasitics) | yes | n/a | yes | HIGH | yes | none |
| C3 | C2+GT-13? (design-point range, annual derate) | yes | n/a | yes | MEDIUM | yes | none |
| C4 | GT-9+GT-2+GT-6+C1+C3 (CA definition, temps, ceiling, annual avg) | yes | n/a | yes | MEDIUM | yes | none |
| C5 | C1+C3 (ceiling, annual avg) | yes | n/a | yes | MEDIUM | yes | none |
| C6 | C1+C2+C3+GT-8 (ceiling, design range, annual avg, boiling fact) | yes | n/a | yes | MEDIUM | yes | none |
| C7 | C6+C2+GT-5+GT-15?+GT-14? (decomposition, lever magnitude, LCOE data, scope exclusions) | yes | n/a | yes | MEDIUM | yes | none |

| §6 Span (brief) | Construct | Claim under R11? | R11 clause applied | Chain cited |
|-------------------|-----------|-------------------|----------------------|---------------|
| "Recommended approach: evaluate against the Lorenz ceiling ... prioritize near-term levers" | bold lead-in | yes | colon closes bold span, text follows on same line | C1, C7 |
| "Key insight: naive Carnot overstates headroom ... most of the gap is irreducible" | bold lead-in | yes | colon closes bold span, text follows on same line | C1, C7 |
| "Trade-offs acknowledged: recoverable points cost capex but LCOE falls; deployment context caveat" | bold lead-in | yes | colon closes bold span; trailing caveat carries `no chain` marker | C7 (+ caveat: no chain — flagged assumption only) |
| "Pre-check: head C1 (HIGH), C2 (HIGH), C3–C7 (MEDIUM) · Inputs ceiling: MEDIUM" | bold lead-in (pre-check line) | yes | pre-check line is itself a claim per the citation rule | C1, C2, C3, C4, C5, C6, C7 |
| "Confidence: MEDIUM — rests most heavily on C7, capped via C6/C3 by GT-12?/GT-13?" | bold lead-in | yes | colon closes bold span, text follows on same line | C1, C2, C3, C4, C5, C6, C7 |

Scan complete: 7 chain rows, one per section-4 chain block in order; 5 section-6 rows, one per construct in order — 5 claims under R11, 0 excluded. 0 chains malformed, 0 claims untraced.

## Self-Audit Gate (process output)

**Criterion 1: Identify Essence**
Quoted span: "What is the law-permitted thermal-to-electric efficiency ceiling for a steam Rankine power block drawing heat from a 565°C molten-salt hot tank, and how much of the gap between that ceiling and current 565°C-class CSP tower practice is closeable by near/mid-term engineering versus irreducible given the fixed nitrate-salt temperature limit?"
Band: **Rigorous**
Justification: the statement names the specific question (an exergy-bound ceiling and a recoverable/irreducible gap split for this exact system) rather than a restatement of the prompt or a symptom, and each of the four success criteria is a verb+subject+outcome triplet checkable against a named chain (C1, C2/C3, C6, C7) without further interpretation.

**Criterion 2: Challenge Assumptions**
Quoted span (Assumption Audit scan): "One genuinely new item surfaced during the audit and not previously distinguished in the Phase-2 table: A19 ... added to the Classified Assumptions Table below. All other surfaced items were already pre-declared."
Band: **Rigorous**
Justification: every row in the Assumptions Table (§2) uses one of the four prescribed types with a matching treatment; Verdict cells use the token+em-dash+justification form; several assumptions are genuinely Challenged (A9's Curzon-Ahlborn misreading, A10's chemistry-margin claim, A12's proxy-study substitution, A16's parasitic-scope boundary); every assumption feeding a chain despite being unverified carries "unverified — flagged" in its Verification cell; and the quoted scan confirms the Phase-4 audit ran exhaustively over all 21 named chain steps and surfaced exactly one previously-undeclared item, which was added.

**Criterion 3: Establish Ground Truths**
Quoted span (Ground Truths §3 provenance summary): "?-marked: GT-10, GT-11, GT-12, GT-13, GT-14, GT-15, GT-17 (7 of 17)."
Band: **Rigorous**
Justification: checking this enumeration against the Ground Truths list confirms it matches exactly the seven `?`-suffixed entries; every unsuffixed GT feeding the two HIGH-confidence chains (C1, C2) names either a read-at-source location in Sandia SAND2013-1960 (GT-2/GT-3/GT-4/GT-6, each citing a specific Table and row) or is explicit that it is a physical-law/definitional derivation with no external source to read (GT-1/GT-7/GT-8/GT-9); IDs are stable throughout; no assumption discarded in Phase 2 appears in this list.

**Criterion 4: Reason Upward**
Quoted span (Self-audit scan, chain-form table): all seven rows read "Form conforming? yes ... Dependency clean? yes", e.g. "C1 | GT-1+GT-2+GT-6+GT-7 ... | yes | n/a | yes | HIGH | yes | none."
Band: **Rigorous**
Justification: the scan confirms all seven chains are form-conforming with clean (acyclic) dependencies; each chain carries at least one genuine intermediate step not restatable from a single head input; §5 documents three dead ends with specific structural abandonment reasons (contradicts GT-7's formula, logically impossible given C2, smuggles in a different ceiling); no analogy is used as direct evidence; and the one hop carrying a declared premise (C1's [Assumes: A7]) is priced in that chain's own confidence line rather than left unaddressed.

**Criterion 5: Validate**
Quoted span (Adversarial pass record): "Cluster A — ... **costly but survivable**; named plan change: every chain's confidence line touching C2/C3/C5/C7 names GT-12? and GT-13? explicitly ... Cluster E — ... named plan change: every headline figure in §6 is presented as a range with an explicit MEDIUM confidence label ..."
Band: **Rigorous**
Justification: every MEDIUM chain's confidence line names its `?`-marked inputs and below-HIGH cited chains with a verification path; no HIGH chain (C1, C2) consumes a `?` input; every chain is rated no higher than the lowest-rated chain its head cites (C3–C7 correctly capped by earlier MEDIUM chains); and the quoted record shows the adversarial pass ran in full (Recompute/Sensitivity/Rival/Premise/Causes/Clusters/Falsification all present) with every one of its five clusters carrying a named disposition — a plan change or an explicitly accepted risk with a named mitigation.

**Criterion 6: Conclusion-to-Ground-Truth Traceability**
Quoted span (Self-audit scan, claim-inventory table): all five rows read "Claim under R11? yes" with a named `Chain cited` column entry, and the reconciliation line reads "5 claims under R11, 0 excluded. 0 chains malformed, 0 claims untraced."
Band: **Rigorous**
Justification: every §6 claim (Recommended approach, Key insight, Trade-offs acknowledged, Pre-check, Confidence) traces to a specific named §4 chain per the quoted scan and the inline citations in §6 itself; no new reasoning is introduced in §6 beyond what §4 established; and the Key Insight ("the naive Carnot figure overstates headroom by ~8 points, and even after correcting for that, most of the remaining gap is irreducible, not an engineering-maturity shortfall") is a non-obvious finding distinct from — not a restatement of — the action-oriented Recommended approach.

**Gate result:** No criterion scored Absent; zero criteria scored Hand-wavy. Both clearance conditions are met on the first scoring pass — no Fix/Repeat re-score was required, and no re-entry edge fired.

# First-Principles Analysis: Thermal-to-Electric Efficiency Ceiling of a 565°C Molten-Salt Power Tower Rankine Power Block

## 1. Problem Essence

**Core problem:** What is the law-permitted thermal-to-electric efficiency ceiling for a steam Rankine power block drawing heat from a 565°C molten-salt hot tank, and how much of the gap between that ceiling and current 565°C-class CSP tower practice is closeable by near/mid-term engineering versus irreducible given the fixed nitrate-salt temperature limit?

**Success criteria:**
1. The ceiling is derived from an exergy/finite-source bound (not naive isothermal Carnot), stated as a numeric range with the governing formula and inputs shown — verifiable by checking chain C1.
2. Current design-point and annual-average practice are each stated as a numeric range grounded in a named, citable source — verifiable by checking chains C2 and C3.
3. The gap is decomposed into named components (internal-cycle irreversibility, parasitics, part-load operation) each tagged hard-limit or addressable — verifiable by checking chain C6.
4. The recoverable and irreducible fractions of the gap are each stated as a percentage/point range with reasoning shown — verifiable by checking chain C7 and the Confidence line in §6.

## 2. Assumptions Table

| Assumption | Type | Treatment | Verdict | Verification |
|------------|------|-----------|---------|--------------|
| A1 — A reversible heat engine's maximum efficiency between reservoirs at T_H and T_C is η=1−T_C/T_H (2nd law / Carnot). | physical law | accept as ground-truth candidate | Accept — foundational, not contestable | GT-1; derived directly, standard thermodynamic definition |
| A2 — Sandia's 165 MWe-class baseline molten-salt tower design point is 565°C hot salt, 296°C cold-salt return, 553°C/120 bar-a main steam. | current constraint | record expiry: a different plant design could return colder/hotter salt or use different steam parameters | Accept — read at source, this study's own baseline definition | GT-2; SAND2013-1960 Table 5, read-at-source |
| A3 — Gross cycle efficiency for baseline/advanced-subcritical/supercritical (566°C) configurations is 41.1% / 43.2% / 45.5%. | current constraint | expires as turbine/cycle technology improves | Accept — read at source | GT-3; SAND2013-1960 Table 5, read-at-source |
| A4 — Itemized power-block and salt-pump parasitic loads (kW) are as tabulated per configuration. | current constraint | expires as pump/fan technology improves | Accept — read at source | GT-4; SAND2013-1960 Tables 5 & 13, read-at-source |
| A5 — Supercritical upgrade at the same ~566°C salt raises annual energy 8.9-13.5% and lowers LCOE 7-10% in this study's SAM simulation. | current constraint | expires with different financing/cost assumptions | Accept — read at source | GT-5; SAND2013-1960 Table 14 & p.31 text, read-at-source |
| A6 — Air-cooled-condenser design point: 43°C ambient + 14°C ITD ≈ 57°C condensing temperature. | current constraint | expires with wet cooling or a different site climate | Accept — read at source; site- and cooling-mode-dependent | GT-6; SAND2013-1960 Table 10, read-at-source |
| A7 — Maximum work extractable from a constant-cp sensible-heat source cooling T1→T2 against sink T_C is η=1−T_C·ln(T1/T2)/(T1−T2) (Lorenz/exergy bound). | physical law | accept as ground-truth candidate | Accept — direct 2nd-law consequence, derived in this analysis | GT-7; standard exergy-analysis derivation |
| A8 — Below its critical point (374°C/221 bar), water boils at constant temperature; above it, no distinct boiling plateau exists. | physical law | accept as ground-truth candidate | Accept — standard property of water | GT-8; derived directly |
| A9 — Curzon-Ahlborn efficiency is a maximum-*power*, not maximum-*efficiency*, bound, and is commonly misread as an efficiency ceiling. | convention | explicitly challenge the misreading before use | Challenge — the misreading is tempting given later numeric proximity to achieved efficiency; corrected via GT-9 | GT-9; derived directly from the model's own definition |
| A10 — Solar salt (60% NaNO3/40% KNO3) is usable to ≈600°C, with 565°C an operating margin below decomposition. | current constraint | expires with reformulated/additized salt chemistry | Challenge — exact decomposition onset not pinned to a single cited figure; accepted with `?` | GT-10?; unverified — flagged (WebSearch summary, source not opened) |
| A11 — Named 565°C-class towers (Crescent Dunes, Noor III, Cerro Dominador) use air-cooled condensers; Crescent Dunes circulates ≈288-566°C salt. | current constraint | expires with a coastal/water-rich site choice | Accept, with `?` — corroborates but does not independently verify GT-2's generic-study figures for these specific plants | GT-11?; unverified — flagged (WebSearch summary) |
| A12 — No plant-specific as-built power-block efficiency percentage was located; the generic Sandia study (GT-2/GT-3/GT-4) is used as the current-practice proxy. | untested belief | verify or flag unverified | Challenge — a real methodological stand-in, not a plant audit | GT-12?; unverified — flagged (search attempted, no figure found) |
| A13 — Annual-average net efficiency sits roughly 3-4 points below design-point due to part-load, cycling, and hot-ambient condenser derating. | untested belief | verify or flag unverified | Challenge — engineering judgment, no plant heat-balance confirms it | GT-13?; unverified — flagged |
| A14 — sCO2 Brayton's efficiency edge over supercritical steam is not established at the 565-600°C class considered here. | untested belief / current constraint | verify or flag unverified; record technology-maturity expiry | Challenge — bounds the recoverable estimate downward rather than resolving it | GT-14?; unverified — flagged |
| A15 — Chloride/carbonate salt chemistries reaching 700-800°C are excluded from this analysis's scope by the question's own nitrate-salt constraint. | convention / scope-boundary | explicitly challenge, then accept the boundary as set by the question | Accept — scope is set by the question, not by this analysis's preference | GT-15?; unverified — flagged, and explicitly out-of-scope for the recoverable-fraction accounting |
| A16 — Power-block net efficiency is computed by excluding salt-tower circulation-pump power (attributed to the receiver/collection loop), with the whole-plant-inclusive alternative reported alongside. | convention | explicitly challenge before use | Challenge — genuinely contestable boundary; both branches carried through explicitly in C2 rather than resolved by fiat | used in C2; not itself a separate GT — both scope branches are stated as results |
| A17 — Supercritical power-block capex premium ≈$61/kWe, yet whole-plant LCOE falls 7-10%. | current constraint | expires with different equipment pricing | Accept — read at source | GT-16; SAND2013-1960 Table 7 & p.27 text, read-at-source |
| A18 — CSP molten-salt-tower deployment has slowed relative to PV-plus-battery-storage in the current cost environment. | untested belief | verify or flag unverified | Challenge — general industry knowledge, no source opened this session; used only in a non-load-bearing second-order hop | GT-17?; unverified — flagged |
| A19 — Near-term parasitic-load reduction and improved part-load/dispatch management recover roughly 1-2 points beyond the turbine/supercritical levers already captured in A3/A5. | untested belief | verify or flag unverified | Challenge — surfaced during the Phase-4 Assumption Audit (chain C7, step 2); no independent source confirms the magnitude | unverified — flagged; used only as a bounding addend in C7, not independently load-bearing |

## 3. Ground Truths

- **GT-1** A reversible heat engine's maximum efficiency between reservoirs at T_H and T_C is η=1−T_C/T_H (2nd law of thermodynamics). — source: standard thermodynamic definition; derived directly in this analysis — no external source to read; not suffixed.
- **GT-2** Sandia's 165 MWe-gross-class baseline molten-salt power tower design point: hot salt temperature 565°C, cold salt return temperature 296°C, main/reheat steam temperature 553°C, main steam pressure 120 bar-a. — source: J. E. Pacheco, T. Wolf, N. Muley, *Incorporating Supercritical Steam Turbines into Advanced Molten-Salt Power Tower Plants: Feasibility and Performance*, Sandia National Laboratories, SAND2013-1960 (March 2013); read-at-source: Table 5 (p.25), "Baseline Sub-critical" column, rows "Hot Salt Temperature,°C", "Cold Salt Return Temperature,°C", "Main/Reheat Steam Temperature,°C", "Main Steam Pressure, bar-a".
- **GT-3** Gross cycle (turbine-generator) thermal-to-electric efficiency for the same study: 41.1% (Baseline Subcritical), 43.2% (Advanced Subcritical Baseline Cycle 1, Siemens SST-900-class turbine, 565.5°C salt), 45.5% (Supercritical Cycle 5, 566°C salt, 230 bar-a; range 45.2-46.2% across the four supercritical variants studied). — source: same report; read-at-source: Table 5 (p.25), row "Gross Cycle Efficiency, %".
- **GT-4** Itemized parasitic loads (kW) for these three cases: Boiler Feed Pump 3175/2696/5288; Condensate Pump 140/133/126; Cooling Fans 2955/2811/2669; Auxiliaries 700/700/700; Cold (tower-circulation) Salt Pump 12096/13038/13264; Hot Salt Pump 1009/1046/952. — source: same report; read-at-source: Table 5 (p.25) and Table 13 (p.30).
- **GT-5** Adopting supercritical steam (230 bar-a) at essentially the same ~566°C salt temperature raises annual energy production by 8.9-13.5% and lowers levelized cost of energy by 7-10% relative to the subcritical baseline, in this study's System Advisory Model annual simulation (Daggett, CA TMY2 resource); the study's stated conclusion is that it is "economically and technically feasible to incorporate supercritical steam turbines in molten-salt power tower plants." — source: same report; read-at-source: Table 14 (p.31), rows "Annual Energy Delta,%" and "LCOE delta,%", and p.31 body text; abstract, p.3.
- **GT-6** Air-cooled-condenser design point for this plant class: ambient temperature 43°C, initial temperature difference (ITD) 14°C at the design point, giving an approximate design-point condensing temperature of ≈57°C (330 K). — source: same report; read-at-source: Table 10 (p.29), "Cooling System" block, rows "Condenser Type", "Ambient Temperature at Design", "ITD at Design Point".
- **GT-7** Maximum extractable work (exergy) from a constant-specific-heat sensible-heat source cooling from T1 to T2 while rejecting heat to a sink at T_C is Ex=c(T1−T2)−T_C·c·ln(T1/T2); dividing by the heat released, Q=c(T1−T2), gives the ideal (Lorenz-cycle) conversion efficiency η=1−T_C·ln(T1/T2)/(T1−T2) — a direct 2nd-law consequence, equivalent to an infinite cascade of infinitesimal Carnot engines each operating at the local source temperature. — source: standard exergy-analysis derivation; derived directly in this analysis; not suffixed.
- **GT-8** Below the critical point of water (374°C, 221 bar), boiling occurs at constant temperature for a given pressure; above the critical pressure there is no distinct boiling plateau, so a supercritical-pressure heating curve can better match a continuously cooling (glide) heat source than a subcritical (boiling) one. — source: standard property of water; derived directly; not suffixed.
- **GT-9** The Curzon-Ahlborn efficiency η_CA=1−√(T_C/T_H) is the efficiency of an idealized endoreversible heat engine at maximum *power output* (not maximum efficiency) under a specific two-finite-rate-heat-exchanger idealization; it is not a thermodynamic ceiling on efficiency, and real power plants not optimized in the Curzon-Ahlborn sense of "maximum power" routinely exceed it. — source: standard finite-time-thermodynamics result; derived directly; not suffixed.
- **GT-10?** Solar salt (60% NaNO3/40% KNO3) is described in the general CSP literature as usable to approximately 600°C, with the ~565°C standard operating ceiling of current-generation towers reflecting a margin below the salt's practical decomposition/degradation limit. — cited to: general web-search summary (ScienceDirect "Solar Salt" topic and related sources); reported-by-delegate: WebSearch tool summary; cited pages not individually opened and read at source by this analysis.
- **GT-11?** Named 565°C-class molten-salt towers (Crescent Dunes, Noor III, Cerro Dominador) use air-cooled condensers, consistent with desert siting and water scarcity; Crescent Dunes specifically circulates salt between ≈288°C (550°F) and ≈566°C (1050°F) via a Nooter/Eriksen steam generator and an air-cooled condenser. — cited to: web-search summary (PowerMag "TOP PLANT: Crescent Dunes Solar Energy Project" and related sources); reported-by-delegate: WebSearch tool summary; not independently opened and read at source.
- **GT-12?** No plant-specific gross or net thermal-to-electric efficiency percentage for the actual as-built Crescent Dunes, Gemasolar, or Noor III power blocks was located by this analysis's searches; GT-2/GT-3/GT-4 (the generic 165 MWe Sandia study) are used as the best-available grounded proxy for "current 565°C-class subcritical practice," not a plant-specific audited figure. — unverified: two targeted WebSearch queries returned facility overviews and receiver-efficiency figures but no power-block thermal-to-electric percentage; Phase 3 failure record: searches conducted, asserted figure not found in returned sources.
- **GT-13?** CSP power-block annual-average net efficiency is typically several percentage points below design-point net efficiency, due to part-load operation, startup/shutdown cycling, and off-design/hot-ambient condenser performance (an air-cooled condenser's condensing temperature — and hence cycle efficiency — degrades on days hotter than GT-6's 43°C design point). — unverified: engineering-judgment estimate; no plant-specific annual heat-balance or annual power-block-efficiency figure was located by this analysis's searches.
- **GT-14?** sCO2 Brayton cycles are being actively piloted (e.g., DOE STEP program) as a CSP bottoming/replacement technology, with their clearest efficiency advantage over supercritical steam established at turbine-inlet temperatures above roughly 650-700°C; no source located by this analysis establishes a demonstrated sCO2 efficiency advantage over the supercritical-steam figures in GT-3 at the 565-600°C class. — unverified: general literature familiarity; no source opened this session comparing sCO2 vs. supercritical steam at exactly 565-600°C.
- **GT-15?** Chloride-salt and carbonate-salt HTF chemistries under active R&D (e.g., DOE Gen3 CSP program) target hot-side temperatures of roughly 700-800°C, above the ~565-600°C ceiling of nitrate solar salt; adopting them would raise the achievable Lorenz-type ceiling (a different T_H1 in GT-7's formula) rather than close today's gap to the existing ≈52.5% ceiling, and is excluded from this analysis's "recoverable fraction" accounting by the question's own stated nitrate-salt-chemistry scope. — unverified: general literature familiarity; no source opened this session.
- **GT-16** Power-block-specific capital cost for the supercritical configuration is approximately $61/kWe higher than the subcritical baseline ($800/kWe baseline vs. $861/kWe supercritical steam turbine plus once-through steam generator); despite this, the same supercritical plants show 7-10% *lower* overall plant LCOE (GT-5) due to higher annual energy production. — source: SAND2013-1960; read-at-source: Table 7 (p.27) and body text, p.27 ("These add approximately $61/kWe to the power block cost").
- **GT-17?** CSP molten-salt-tower deployment has slowed significantly relative to PV-plus-battery-storage deployment in the current cost environment. — unverified: general industry knowledge; no specific source opened this session; used only in a non-load-bearing second-order (3rd-order) extension hop in C7, not as support for the headline thermodynamic conclusion.

**Provenance summary:**
```
?-marked: GT-10, GT-11, GT-12, GT-13, GT-14, GT-15, GT-17 (7 of 17)
Read-at-source: GT-2, GT-3, GT-4, GT-6, GT-16 — SAND2013-1960 (Sandia, March 2013), Tables 5/7/10/13/14 and body text as cited per-entry above.
GT-1, GT-7, GT-8, GT-9 are physical-law/definitional derivations performed directly in this analysis; no external source citation applies.
```

## 4. Derivation Chains

### Conclusion C1: The correct ceiling is the Lorenz/exergy bound (≈52-53%), not naive Carnot (≈61%)

GT-1 (Carnot/2nd-law bound) + GT-2 (565°C hot salt, 296°C cold-salt return) + GT-6 (≈57°C dry-cooled design sink) + GT-7 (Lorenz/exergy glide-source bound)
→ evaluating naive Carnot with an isothermal source at T_H=838.15K against T_C≈330.15K gives η=1−330.15/838.15≈60.6%, but this treats the entire 565°C-to-296°C sensible-heat release as if delivered at a constant 565°C
→ applying GT-7's Lorenz formula with T_H1=838.15K, T_H2=569.15K, T_C=330.15K gives η=1−330.15·ln(838.15/569.15)/(838.15−569.15)≈52.5%, because most of the salt's heat is released well below 565°C as it cools toward its 296°C return temperature [Assumes: A7 — solar salt specific heat is ~constant over 296-565°C]
→ the physically correct ceiling for this finite-source system is therefore the Lorenz bound, roughly 52-53%, not the naive ≈61% Carnot figure

**Pre-check:** head GT-1, GT-2, GT-6, GT-7 · ?-marked: none · lowest cited: none · Inputs ceiling: HIGH
**Confidence:** HIGH — every head input is an unsuffixed ground truth read at source (GT-2, GT-6) or derived directly as a physical law/definition (GT-1, GT-7); the hop sequence is direct formula application that recomputes cleanly (verified in the Adversarial pass record); the naive-Carnot rival is not merely raised but ruled out within this chain's own hops, satisfying the Rivals axis. The constant-cp premise declared on hop 2 (A7) is priced: solar salt's specific heat varies by only a few percent over 296-565°C, so even a materially wrong cp-profile would shift the ceiling by at most ~1 point, leaving the endpoint ("≈52-53%, well below naive ≈61%") unchanged in direction or materiality.

### Conclusion C2: Current 565°C-class design-point thermal-to-electric efficiency spans ≈36-42% (subcritical) to ≈39-43% (same-temperature supercritical)

GT-3 (gross cycle efficiencies 41.1/43.2/45.5%) + GT-4 (itemized parasitic loads)
→ subtracting GT-4's boiler-feed-pump, condensate-pump, cooling-fan and auxiliary parasitics from gross output (power-block scope, [Assumes: A16]) gives net design-point efficiencies of ≈39.4% (baseline subcritical), ≈41.5% (advanced subcritical, modern turbine), and ≈43.1% (supercritical, 566°C)
→ including the salt-tower circulation-pump power as well (whole-plant-parasitic scope, the more conservative alternative to A16) instead gives ≈36.1%, ≈37.9%, and ≈39.2-40.4% respectively for the same three cases
→ current deployed 565°C-class subcritical towers therefore plausibly sit in a design-point net range of roughly 36-42%, central ≈39%, depending on turbine vintage and the power-block-boundary definition used, while a same-salt-temperature supercritical upgrade would move that range to roughly 39-43%, central ≈41%

**Pre-check:** head GT-3, GT-4 · ?-marked: none · lowest cited: none · Inputs ceiling: HIGH
**Confidence:** HIGH — both head inputs are unsuffixed ground truths read at source (SAND2013-1960, Table 5/13); the [Assumes: A16] scope premise on hop 1 is priced by construction, since hop 3's endpoint explicitly brackets both the A16-true and A16-false results (hop 1 and hop 2) rather than depending on resolving which is "correct" — the range already spans both interpretations, so A16's failure does not narrow or invalidate the endpoint. No live, unsettled rival contests this chain's own arithmetic (a rival about whether *named plants* match this study is addressed in C3, not here).

### Conclusion C3: Estimated current annual-average thermal-to-electric efficiency is ≈35-36%

C2 (design-point range, ≈39% central) + GT-13? (annual-average derate)
→ applying GT-13's qualitative part-load, cycling, and hot-ambient-condenser derate (estimated ≈3-4 percentage points, not confirmed by any plant-specific annual heat-balance located in this analysis) to C2's ≈39% central design-point figure gives an estimated annual-average net thermal-to-electric efficiency of roughly 35-36%, central ≈35%

**Pre-check:** head C2 (HIGH), GT-13? · ?-marked: GT-13? · lowest cited: HIGH · Inputs ceiling: MEDIUM
**Confidence:** MEDIUM — GT-13? is unverified; verification path: open a named plant's (Crescent Dunes, Noor III, Cerro Dominador) audited annual performance report or SAM/TRNSYS annual-simulation output and read the stated annual power-block efficiency, or the annual GWh-electric/GWh-thermal-delivered ratio, directly. C2 itself is HIGH and does not contribute to the downgrade.

### Conclusion C4: Curzon-Ahlborn (≈37%) is not the correct ceiling, despite numerically resembling achieved annual-average efficiency

GT-9 (Curzon-Ahlborn max-power, not max-efficiency, bound) + GT-2 (565°C hot salt) + GT-6 (≈57°C dry-cooled sink) + C1 (Lorenz ceiling ≈52-53%) + C3 (annual-average efficiency ≈35%)
→ computing η_CA=1−√(T_C/T_H) with T_C≈330.15K, T_H=838.15K gives η_CA≈37.2%
→ that figure sits close to C3's estimated annual-average achieved efficiency (≈35%), which could tempt treating Curzon-Ahlborn as the real-world ceiling
→ GT-9 establishes Curzon-Ahlborn is a maximum-power, not maximum-efficiency, bound, and C2's design-point gross figure (41.1% at minimum) already exceeds η_CA, which is impossible for a genuine efficiency ceiling, so the numeric resemblance to annual-average achieved efficiency is coincidental, and C1's Lorenz bound (≈52-53%) remains the correct ceiling

**Pre-check:** head GT-9, GT-2, GT-6, C1 (HIGH), C3 (MEDIUM) · ?-marked: none directly · lowest cited: MEDIUM · Inputs ceiling: MEDIUM
**Confidence:** MEDIUM — capped by C3 (MEDIUM), whose own downgrade cause is GT-13? (see C3's confidence line for the verification path). The logical argument in hop 3 (design-point gross exceeding η_CA) does not itself depend on GT-13?'s precision, only on its rough magnitude relative to C2's HIGH-confidence design-point figures, so this chain's *conclusion* is robust even though its *rating* inherits C3's cap.

### Conclusion C5: The gap between the Lorenz ceiling and current annual-average practice is ≈17-18 percentage points

C1 (Lorenz ceiling ≈52.5%) + C3 (annual-average efficiency ≈35%)
→ subtracting central estimates, 52.5%−35%=17.5, rounded to ≈17-18 percentage points, the quantity the component decomposition in C6 accounts for

**Pre-check:** head C1 (HIGH), C3 (MEDIUM) · ?-marked: none directly · lowest cited: MEDIUM · Inputs ceiling: MEDIUM
**Confidence:** MEDIUM — capped by C3 (MEDIUM); see C3's confidence line for the GT-13? verification path. The subtraction itself recomputes cleanly (Adversarial pass record) and adds no further downgrade cause of its own.

### Conclusion C6: The gap decomposes into internal-cycle irreversibility (dominant), gross-to-net parasitics, and design-to-annual operating losses

C1 (Lorenz ceiling ≈52.5%) + C2 (design-point range, subcritical and supercritical) + C3 (annual-average ≈35%) + GT-8 (water boils near-isothermally below its critical point)
→ from the ceiling (≈52.5%) to today's best-demonstrated near-term design-point gross efficiency at this exact salt temperature (supercritical Cycle 5, 45.5%, C2), the residual loss is ≈7.0 points — a combined internal-cycle loss (GT-8's inherent mismatch between the salt's continuous cooling glide and even a supercritical steam-generator's heating curve, plus residual turbomachinery irreversibility) that this analysis's sources do not further decompose into its two sub-causes
→ from that same ceiling to today's typical deployed subcritical design-point gross efficiency (advanced subcritical, 43.2%, C2), the loss is ≈9.3 points, meaning ≈2.3 of those 9.3 points are closeable near-term simply by adopting the already-studied supercritical configuration at the same salt temperature, while ≈7.0 points remain even after doing so
→ moving from gross to net (C2's scope-dependent parasitic loss, ≈1.7-5.0 points) and from design-point to annual average (C3's GT-13?-based derate, ≈3-4 points) accounts for the remaining portion of C5's total ≈17-18-point gap, closing the decomposition within rounding

**Pre-check:** head C1 (HIGH), C2 (HIGH), C3 (MEDIUM), GT-8 · ?-marked: none directly · lowest cited: MEDIUM · Inputs ceiling: MEDIUM
**Confidence:** MEDIUM — capped by C3 (MEDIUM); see C3's confidence line for the GT-13? verification path. C1 and C2 are individually HIGH and do not themselves add uncertainty; the residual ≈7.0-point internal-cycle figure is an arithmetic difference of two HIGH-confidence numbers (C1, C2) and is itself well-grounded, but its *attribution* to "glide-mismatch plus turbomachinery, combined" rather than a further sub-split is an explicitly disclosed limitation (no source located decomposes it further), not a numeric uncertainty.

### Conclusion C7: Of the ≈17-18-point gap, roughly one-quarter is near/mid-term recoverable and roughly three-quarters is irreducible under the fixed 565°C nitrate-salt constraint

C6 (component decomposition) + C2 (supercritical/turbine lever magnitude) + GT-5 (annual-energy/LCOE corroboration) + GT-14? (sCO2 advantage uncertain at 565°C) + GT-15? (alternative-salt chemistry excluded by scope)
→ within C6's breakdown, adopting an already-commercial modern turbine (≈1.7-2.1 points, C2) plus the same-salt-temperature supercritical steam upgrade (≈1.3-3.7 additional points, C2) together close roughly 3-6 points of design-point net efficiency, corroborated at the whole-plant annual level by GT-5's reported 8.9-13.5% annual-energy gain and 7-10% LCOE reduction for the same supercritical plants
→ adding an estimated ≈1-2 points from parasitic-load reduction and improved part-load/dispatch management [Assumes: A19] gives a combined near/mid-term recoverable estimate of roughly 4-7 points, central ≈5 points, of C5's ≈17-18-point total gap
→ the remaining ≈7.0-point residual identified in C6 — persisting even in the best-demonstrated near-term supercritical configuration — plus the portion of parasitic and part-load losses not addressed by known near-term technology, has no known near-term engineering fix under the fixed 565°C nitrate-salt constraint, constituting an irreducible ≈11-14 points, central ≈13 points, of the total gap
→ per GT-15, raising hot-side temperature via chloride or carbonate salts would raise the ceiling itself (a different T_H1 in GT-7's formula) rather than close today's gap to the existing ≈52.5% ceiling, and is excluded by the question's fixed nitrate-salt-chemistry constraint; GT-14 further flags that sCO2 Brayton's efficiency advantage over supercritical steam is not established at this 565-600°C class, so it is treated as a small, uncertain, not-separately-counted addition to the recoverable estimate
→ therefore, of the total ≈17-18-point gap between the Lorenz ceiling and current annual-average practice, roughly 25-30% (≈5 points) is realistically recoverable with near/mid-term engineering holding the 565°C nitrate-salt ceiling fixed, and roughly 70-75% (≈13 points) is an irreducible consequence of the steam-Rankine glide-mismatch, mature-turbomachinery limits, and residual part-load/parasitic losses with no identified near-term fix
→[2nd] adopting the supercritical/modern-turbine upgrade path raises power-block-specific capital cost by roughly $61/kWe (GT-16), but this study's own annual SAM simulation shows the resulting efficiency and annual-energy gains (GT-5) more than offset that capex increase, yielding 7-10% *lower* overall plant LCOE — so, contrary to a naive expectation that efficiency gains cost money, the recoverable lever identified above is economically favorable within the CSP technology class, not merely thermodynamically available (actor lens: a rational CSP developer or EPC contractor has a cost incentive, not merely a technical option, to adopt it)
→[3rd] this favorable within-technology economics finding does not establish that molten-salt-tower CSP is being built at meaningful scale in the present period relative to PV-plus-battery-storage alternatives (GT-17?, unverified, non-load-bearing); if new nitrate-salt tower construction remains rare regardless of within-technology LCOE improvements, the ≈5-point recoverable margin is realized only inside whichever towers do get built, not across a growing fleet (time lens, long-run-assumed-baseline horizon)

Neither the 2nd- nor 3rd-order extension contradicts any Ground Truth (GT-1 through GT-17); both add market/deployment context consistent with all thermodynamic ground truths, so no return to Phase 2 was triggered.

**Pre-check:** head C6 (MEDIUM), C2 (HIGH), GT-5, GT-14?, GT-15? · ?-marked: GT-14?, GT-15? · lowest cited: MEDIUM · Inputs ceiling: MEDIUM
**Confidence:** MEDIUM — capped by C6 (MEDIUM), which is itself capped by C3's GT-13? (see C3's confidence line for the verification path). GT-14? and GT-15? are unverified but bound the estimate rather than drive its central arithmetic (an excluded lever and a small, uncertain addition, respectively); verification path for GT-14?: open recent DOE Gen3/STEP sCO2 pilot-plant performance literature at ≤600°C turbine-inlet conditions. The dominant downgrade cause is inherited from C3/C6, not introduced fresh here.

## 5. Abandoned Reasoning

### Dead End: Using naive isothermal Carnot (T_H=565°C, T_C≈ambient) as the ceiling

**What was tried:** Computed η=1−T_C/T_H≈60.6% and considered presenting this directly as "the" thermodynamic ceiling for the power block, as a naive reading of the question's own framing (565°C hot side, ambient-linked cold side) invites.

**Why abandoned:** This overstates available exergy because the hot salt is a finite sensible-heat (glide) source cooling from 565°C to 296°C, not an isothermal reservoir held at 565°C. GT-7's Lorenz/exergy formula correctly accounts for the cooling glide and yields ≈52.5% (chain C1) — roughly 8 points lower — because most of the salt's heat is actually released well below 565°C as it cools toward its return temperature.

**What it ruled out:** Any conclusion asserting the power block "ought" to approach ≈61%; that figure is not physically attainable by any real engine, reversible or not, given the actual heat-source profile. It is the loosest true bound available and, left unchecked against a tighter applicable one, would have overstated real headroom in every downstream figure in this analysis.

### Dead End: Using Curzon-Ahlborn as the ceiling because it numerically resembles achieved annual-average efficiency

**What was tried:** Computed η_CA=1−√(T_C/T_H)≈37.2% (chain C4) and noted its striking numeric proximity to the annual-average achieved efficiency estimated in C3 (≈35%), which raised the temptation to treat Curzon-Ahlborn as the realistic ceiling that "explains" current practice.

**Why abandoned:** GT-9 establishes Curzon-Ahlborn is the efficiency of an idealized engine at maximum *power output* under a specific two-resistor idealization, not a maximum-*efficiency* bound. C2's design-point gross efficiency (41.1% at minimum, HIGH confidence, read at source) already exceeds η_CA≈37.2%, which is logically impossible for a genuine ceiling — a real, measured design-point figure cannot exceed a true upper bound. The numeric coincidence with the *annual-average* figure is therefore just that: a coincidence between two unrelated quantities.

**What it ruled out:** Treating the Curzon-Ahlborn/achieved-efficiency numeric proximity as physically meaningful. The correct ceiling remains C1's Lorenz bound (≈52-53%), and the gap to close is ≈17-18 points, not ≈0.

### Dead End: Counting higher-temperature alternative-salt chemistry (chloride/carbonate, ≈700-800°C) as part of the "recoverable" fraction

**What was tried:** Considered including chloride-salt-enabled higher hot-tank temperatures as a lever that could close part of the efficiency gap identified in C5/C6, since it is a real, actively-researched near-to-mid-term CSP technology direction.

**Why abandoned:** Raising T_H1 changes the ceiling itself (a new, higher Lorenz bound via GT-7's formula), not the gap to today's existing ≈52.5% ceiling at 565°C. The question explicitly fixes scope to "nitrate-salt chemistry capping hot-side temperature around 565-600°C" (GT-15?), so this lever is out of bounds for the recoverable-fraction accounting in C7.

**What it ruled out:** Inflating the "recoverable" fraction in C7 by smuggling in a different ceiling under the same label; keeps the ≈25-30%/≈70-75% split in C7 honest to the question's own stated constraint.

## 6. Conclusion

**Recommended approach:** Evaluate the steam Rankine power block of a 565°C-class molten-salt tower against the ≈52-53% Lorenz/exergy ceiling, not the naive ≈61% Carnot figure (chain C1), and prioritize the already-quantified near-term levers — a modern commercial turbine and the same-salt-temperature supercritical steam upgrade — which close roughly 3-6 of the ≈17-18-point gap to that ceiling at a favorable LCOE (chain C7).

**Key insight:** The naive Carnot number overstates real headroom by roughly 8 points because it treats the cooling salt as an isothermal 565°C reservoir rather than a finite sensible-heat source (chain C1); correcting for this still leaves roughly three-quarters of the ≈17-18-point gap as an irreducible consequence of the steam Rankine cycle's own isothermal-boiling/turbomachinery physics, not an engineering-maturity gap that better hardware can close (chain C7).

**Trade-offs acknowledged:** The recoverable ≈3-6 points are not free — a same-salt-temperature supercritical upgrade raises power-block capital cost by roughly $61/kWe, though this study's own annual simulation shows that cost recovered several times over through a 7-10% lower whole-plant LCOE (chain C7); the additional complexity, and the fact that new nitrate-salt tower construction has slowed relative to PV-plus-battery-storage, mean the recoverable margin may be realized in few new plants regardless of its favorable within-technology economics — no chain — flagged assumption only.

**Pre-check:** head C1 (HIGH), C2 (HIGH), C3 (MEDIUM), C4 (MEDIUM), C5 (MEDIUM), C6 (MEDIUM), C7 (MEDIUM) · ?-marked: none directly · lowest cited: MEDIUM · Inputs ceiling: MEDIUM
**Confidence:** MEDIUM — the Conclusion rests most heavily on C7 (MEDIUM), which is capped via C6 and C5 by C3's GT-13? (annual-average derate, unverified) and touches C2's partial reliance on GT-12? (no plant-specific efficiency figure located; the generic 165 MWe Sandia study, SAND2013-1960, is used as proxy). Verification path: open a named plant's (Crescent Dunes, Noor III, Cerro Dominador) audited annual performance report and read its stated design-point and annual-average power-block efficiency directly — this would allow GT-12?/GT-13? to be tightened or dropped and the downstream chains' ratings reconsidered toward HIGH. C1 and C2 are individually HIGH (all-read-at-source or directly-derived inputs), so the Conclusion's design-point-specific claims — the ≈52-53% ceiling itself and the ≈3-6-point supercritical/turbine lever magnitude — carry stronger footing than its annual-average-inclusive headline recoverable/irreducible split.
