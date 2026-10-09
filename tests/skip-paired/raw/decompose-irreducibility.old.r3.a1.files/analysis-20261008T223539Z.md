## Assumption Audit scan (process output)

| Chain | Step | Step Text (brief) | Assumption surfaced? | Added to Table? |
|---|---|---|---|---|
| C1 | 1 | range matches published freeze-margin/stability window | none | n/a |
| C1 | 2 | sub-claim 1 is accurate characterization | none | n/a |
| C2 | 1 | Carnot substitution yields ~63.8% ceiling | none | n/a |
| C2 | 2 | ceiling bounds discharge-side only | A9 (condenser ≈30°C is the correct Tc, not the 290°C tank) | yes — already present (A9), referenced |
| C3 | 1 | real figure (38-42%) consistent with ideal ceiling | none | n/a |
| C3 | 2 | realistic discharge-side efficiency ≈38-42% | none | n/a |
| C4 | 1 | RTE = charge × discharge product | A4 (resistive-charge architecture) | yes — already present (A4), referenced |
| C4 | 2 | achievable RTE ≈37-41% | none | n/a |
| C5 | 1 | tops out near two-thirds RTE [Assumes: A13] | A13 (no near-term breakthrough above ~65-68%) | yes — new, added to table |
| C5 | 2 | no near-term tech reaches >85% | none | n/a |
| C6 | 1 | union of two ranges ≈37-68% | none | n/a |
| C6 | 2 | >85% exceeds optimistic figure by ~20pp | none | n/a |
| C6 | 3 | sub-claim 2 false for current/near-term tech | none | n/a |
| C7 | 1 | >97% belongs to heat-to-heat use case | A3 (electricity- vs heat-to-heat interpretation) | yes — already present (A3), referenced |
| C7 | 2 | commercial practice corroborates claim's combination doesn't exist | none | n/a |
| C8 | 1 | dividing thermal cost by RTE [Assumes: A11] | A11 (thermal→electrical cost conversion is a first-order approximation) | yes — new, added to table |
| C8 | 2 | storage-media cost ≈$32-197/kWh-elec | none | n/a |
| C9 | 1 | interpolated power-block $/kW [Assumes: A12] | A12 (interpolated small-scale power-block cost bracket) | yes — new, added to table |
| C9 | 2 | power rating 1-5MW implied [Assumes: A8] | A8 (duration/power-rating not stated in the claim) | yes — already present (A8), referenced |
| C9 | 3 | power-block adds ≈$160-1,500/kWh | none | n/a |
| C10 | 1 | sum of components ≈$190-1,700/kWh | none | n/a |
| C10 | 2 | range at/above Li-ion range, parity only at best case | A7 (power-conversion cost scaling assumption) | yes — already present (A7), referenced |
| C10 | 3 | sub-claim 3 cost-competitiveness does not hold | none | n/a |
| C11 | 1 | no turnkey 5MWh product exists | A10 (5 MWh representative of commercial deployment) | yes — already present (A10), referenced |
| C11 | 2 | corroborating not primary [Assumes: A14] | A14 (market-absence evidence is corroborating, not primary) | yes — new, added to table |

Scan is exhaustive over all 24 named steps across chains C1-C11, in order, no step skipped.

## Adversarial pass (process output)

**Recompute.**
- C2: 1 − 303/838 = 0.6384 → 63.8% ✓ matches chain text.
- C3: 38/63.8 = 0.596, 42/63.8 = 0.658 — both inside (0,1) and below 1.0, confirming the cited real figure (38-42%) is physically consistent with, and well inside, the derived ideal ceiling (63.8%) ✓.
- C4: 0.98 × 0.38 = 0.3724; 0.98 × 0.42 = 0.4116 → 37.2%-41.2%, rounds to "approximately 37-41%" ✓ matches chain text.
- C6: union of [37,41] and [39,68] = [37,68] → "approximately 37-68%" ✓ matches chain text.
- C8: 22/0.68 = 32.35; 73/0.37 = 197.3 → "$32-$197/kWh-electrical" ✓ matches chain text.
- C9: at 5 MW rating (1 hr duration), 5,000 kW × $800-1,500/kW = $4.0M-$7.5M ÷ 5,000 kWh = $800-1,500/kWh; at 1 MW rating (5 hr duration), 1,000 kW × $800-1,500/kW = $0.8M-$1.5M ÷ 5,000 kWh = $160-300/kWh. Combined duration-sensitive bracket: $160-$1,500/kWh ✓ matches chain text.
- C10: $32-197 (C8) + $160-1,500 (C9) = $192-$1,697, rounds to "approximately $190-$1,700/kWh" ✓ matches chain text.
All computed figures recompute to the values stated in section 4; no correction required.

**Sensitivity.**
- Efficiency verdict (C6): flip candidate is GT-3 (condenser ≈30°C), not `?`-marked. Even at an unusually cold heat sink (5°C/278K), the Carnot ceiling rises only to 1 − 278/838 = 0.668 (66.8%), and real/demonstrated figures would rise correspondingly modestly — nowhere near 85%. C6's conclusion is robust to any plausible real-world value of this input.
- Cost verdict (C10): flip candidate is the power-block $/kW bracket feeding C9 (via GT-8, interpolated under A12), which is this analysis's own estimate, not a direct vendor quote at 1-5 MW scale. If actual small-scale power-block costs fell to large-scale levels (~$200/kW even at 1-5 MW), C9's contribution would shrink toward $40-$200/kWh, pulling C10's low end down to roughly $72-$397/kWh — at that point thermal-ETES could plausibly undercut typical lithium-ion figures. This is the single input most likely to flip the cost verdict and is named explicitly as the least-certain figure in the analysis.

**Rival.**
- C1: not applicable — GT-1's figures (290°C minimum, 565°C stability ceiling) are specific enough that no competing characterization of what technology this range describes survives.
- C2: rival is using the storage tank's 290°C return temperature as Tc instead of the condenser's ~30°C; ruled out in Abandoned Reasoning Dead End 1 (GT-1 vs GT-3's distinct roles).
- C3: not applicable — GT-4's real-world figure is itself the empirical baseline, not a derived figure open to a competing derivation.
- C4: rival is the heat-pump-charging (Carnot-battery) architecture, carried separately as C5 — not a defeat of C4; both feed C6.
- C5: rival is the ideal 100%-reversible-limit case; acknowledged explicitly on C5's own confidence line as "not demonstrated," so it does not unseat the near-term framing.
- C6: rival is a future breakthrough pushing past ~68% (named via A13); does not rule out C6 because C6's endpoint is explicitly scoped to currently demonstrated/near-term technology.
- C7: not applicable — corroborating chain, not contested by any source reviewed.
- C8: rival is that an itemized bottom-up capex model might find the thermal-to-electrical cost conversion (A11) non-linear; not ruled out, named on C8's own confidence line as the Inference-axis shortfall.
- C9: rival (lower real-world power-block costs) is addressed under Sensitivity above and is the dominant live rival in this analysis.
- C10: rival is "thermal-ETES is competitive at a different scale/duration than the one named in the claim" — not ruled out, plausibly true, and carried explicitly into the Conclusion's Trade-offs rather than falsely claimed settled.
- C11: rival is "absence of a commercial product reflects market immaturity, not fundamental uneconomics" — named live, explicitly not ruled out; this is why C11 is marked `[Speculative]` and non-load-bearing.
- Headline conclusion: the strongest rival is "the claim is approximately true at a different scale/duration/architecture than literally stated" — addressed throughout (C10, C11) and disclosed in the Conclusion's Trade-offs rather than suppressed.

**Premise.** Assume this analysis's headline conclusion — that the claim fails as stated — is itself false: assume the original claim is actually true, i.e., a 5 MWh molten-salt system genuinely round-trips electricity above 85% efficiency and is genuinely cost-competitive with lithium-ion at that scale.

**Causes** (unfiltered, generated from four stakeholder viewpoints before any grouping):
- *Thermodynamicist:* the Carnot ceiling might have been computed with the wrong cold-reservoir temperature, overstating the physical limit's severity; real turbomachinery efficiency might already be closer to the Carnot ceiling than GT-4's cited 38-42% figure.
- *Plant/process engineer:* small-scale power-block costs might have dropped substantially via a proprietary modular design absent from the literature searched; the "5 MWh" claim might implicitly assume a much longer duration (e.g., 20+ hours, 0.25 MW) than this analysis's 1-5 hour bracket, making the power-block cost per kWh negligible.
- *Procurement/finance:* the comparison might have used stale, pre-2025 (higher) lithium-ion prices rather than the falling 2025 prices GT-9 cites, flattering thermal-ETES unfairly in the claim's favor rather than against it; the claim might rest on a subsidized or pre-commercial demonstration cost for thermal-ETES not comparable on a like-for-like basis.
- *Marketing/advocacy (the likely origin of such claims):* the claim's author may have genuinely meant heat-to-heat round-trip efficiency (where >97% is real, GT-11) and mislabeled it as electrical "system efficiency"; the author may have meant bare thermal storage-media cost (GT-7, GT-10) and mislabeled it as full-system cost-competitiveness.

**Clusters:**
- *Cluster A — Wrong physics ceiling* (causes 1-2) — bears on C2, C3, GT-2, GT-3, GT-4. Triage: tolerable/unlikely — GT-3 and GT-4 are each independently corroborated by multiple cited sources and match the textbook Carnot-vs-actual ratio pattern search independently confirmed.
- *Cluster B — Undiscovered cheap power-block technology or longer stated duration* (causes 3-4) — bears on C9, GT-8, A8, A12. Triage: costly-but-plausible at the margin — the single most plausible path to narrowing (not closing) the gap; already named in Sensitivity above.
- *Cluster C — Stale or mismatched cost baseline* (causes 5-6) — bears on C10, GT-9. Triage: tolerable — this analysis used current (2025, falling) lithium-ion pricing, which if anything understates the case against thermal-ETES, so this cluster does not run in the claim's favor.
- *Cluster D — Metric mislabeling (heat-to-heat vs. electricity-to-electricity; thermal-cost vs. electrical-system-cost)* (causes 7-8) — bears on C7, C8, GT-10, GT-11, A3, A6. Triage: fatal-to-the-claim-as-literally-stated but highly informative — explains why the claim is plausible-sounding despite being false.

**Disposition:**
- Cluster A: no conclusion change — causes do not survive scrutiny against multiply-corroborated ground truths; accepted as settled.
- Cluster B: conclusion change — the Conclusion's Trade-offs explicitly names duration-sensitivity and the possibility of rough parity under favorable power-block costs rather than overstating a flat "always fails" verdict; mitigation named: an itemized vendor quote would close this (stated on C9's confidence line).
- Cluster C: no conclusion change — accepted as settled; this analysis's cost baseline does not artificially favor the claim-rejecting verdict.
- Cluster D: conclusion change — the Key Insight was written specifically to surface this mislabeling rather than leaving the rejection unexplained; this is the analysis's primary explanatory contribution.

**Falsification.** This analysis's headline conclusion is false if: (a) a commercially available or peer-reviewed, third-party-measured molten-salt (or equivalent sensible-heat) electricity-storage system in the 290-565°C range demonstrates an AC-to-AC round-trip efficiency above 85% at any scale (overturns chain C6); or (b) an itemized, vendor-quoted installed cost for a 5 MWh molten-salt electricity-round-trip system comes in at or below the equivalent installed cost of a 5 MWh lithium-ion BESS under matched assumptions (overturns chain C10).

Techniques not applied:
- pre-mortem — not applicable — the conclusion under validation is a claim (a truth-value verdict on a stated technical/cost assertion), not a plan with actions and a timeline; per the inversion-vs-pre-mortem decision rule, inversion was applied instead as the Phase 5 adversarial technique.
- trade-off — not applicable — the analysis verifies the truth of a single stated compound claim rather than selecting among multiple viable competing options against weighted criteria; the cost comparison embedded in the claim is quantified directly via the estimate procedure (chains C8-C10) instead.
- fishbone — not applicable — the assumption space here is narrow and directly enumerable (temperature-range framing, charging-architecture ambiguity, cost-basis framing, duration ambiguity); it does not require breadth-first multi-category brainstorming to surface hidden branches.

## §6→§4 closure ledger (process output)

- "accept the temperature-range description (sub-claim 1) as accurate (chain C1), but reject both the '>85% round-trip efficiency' claim ... (chain C6) ... and the unqualified 'cost-competitive at 5 MWh' claim ... (chain C10)" → chains C1, C6, C10 ✓
- "The claim's two sub-parts are not independent — the >85% efficiency figure appears to conflate heat-to-heat round-trip efficiency ... (chain C7) ... with electricity-to-electricity round-trip efficiency ... (chain C6) ... and the cost-competitiveness figure appears to conflate cheap bare storage-media cost ... (chains C8, C9, C10)" → chains C7, C6, C8, C9, C10 ✓
- "This verdict is scoped to currently demonstrated and near-term technology ... it does not rule out ... large scale (100+ MWh) or for direct industrial-heat delivery ... which is in fact where this technology is commercially deployed today (chain C11, speculative/corroborating only)" → chain C11 ✓
- "The cost verdict (chain C10) also carries a wide bracket driven by an unstated discharge duration ... a longer stated duration ... would narrow, but not close, the gap with lithium-ion (chain C9)" → chains C10, C9 ✓
- "**Pre-check:** head C1 (HIGH), C6 (HIGH), C10 (MEDIUM) ..." → chains C1, C6, C10 ✓
- "**Confidence:** MEDIUM — driven down by C10's MEDIUM rating ... C8 (MEDIUM) and C9 (MEDIUM) ..." → chains C10, C8, C9 ✓

All six Conclusion-section claims are discharged by inline chain citation; no claim required cutting.

## Self-audit scan (process output)

| Chain | Chain Head (brief) | Form conforming? | Rule applied | Dependency clean? | Band | Act attempted? | Edges fired |
|---|---|---|---|---|---|---|---|
| C1 | GT-1 | yes | n/a | yes | HIGH | yes | none |
| C2 | GT-2 + GT-3 | yes | n/a | yes | HIGH | yes | none |
| C3 | GT-4 + C2 | yes | n/a | yes | HIGH | yes | none |
| C4 | GT-5 + C3 | yes | n/a | yes | HIGH | yes | none |
| C5 | GT-6 | yes | n/a | yes | HIGH | yes | none |
| C6 | C4 + C5 | yes | n/a | yes | HIGH | yes | none |
| C7 | GT-11 | yes | n/a | yes | HIGH | yes | none |
| C8 | GT-7 + C6 | yes | n/a | yes | MEDIUM | yes | none |
| C9 | GT-8 | yes | n/a | yes | MEDIUM | yes | none |
| C10 | C8 + C9 + GT-9 + GT-12? | yes | n/a | yes | MEDIUM | yes | none |
| C11 | GT-11 | yes | n/a | yes | MEDIUM [Speculative] | yes | none |

| §6 Span (brief) | Construct | Claim under R11? | R11 clause applied | Chain cited |
|---|---|---|---|---|
| "Recommended approach: Treat the claim as failing as stated..." | bold lead-in | yes | bold lead-in whose colon closes the bold span, carrying its assertion on the same line | C1, C6, C10 |
| "Key insight: The claim's two sub-parts are not independent..." | bold lead-in | yes | bold lead-in whose colon closes the bold span, carrying its assertion on the same line | C7, C6, C8, C9, C10 |
| "Trade-offs acknowledged: This verdict is scoped to..." | bold lead-in | yes | bold lead-in whose colon closes the bold span, carrying its assertion on the same line | C11, C10, C9 |
| "Pre-check: head C1 (HIGH), C6 (HIGH), C10 (MEDIUM)..." | bold lead-in | yes | pre-check line is itself a claim per the citation-form rule, cited by the chains its own head names | C1, C6, C10 |
| "Confidence: MEDIUM — driven down by C10's MEDIUM rating..." | bold lead-in | yes | bold lead-in whose colon closes the bold span, discharged via the chains D-07 requires it to name | C10, C8, C9 |

Scan complete: 11 chain rows, one per section-4 chain block in order; 5 section-6 rows, one per construct in order — 5 claims under R11, 0 excluded. 0 chains malformed, 0 claims untraced.

## Self-Audit Gate (process output)

**Criterion 1: Identify Essence**
Quoted span: "Does a 5 MWh molten-salt (solar-salt, 290-565°C) thermal energy-storage system achieve an electricity-to-heat-to-electricity round-trip efficiency above 85%, and is such a system cost-competitive, at that same 5 MWh nameplate capacity, with a lithium-ion battery system — or does the claim fail on one or both counts?"
Band: **Rigorous**
Justification: The statement names the compound question directly (not the triggering prompt verbatim), and each of the four success criteria in section 1 is a verb+subject+outcome triplet checkable against the Conclusion section without further interpretation.

**Criterion 2: Challenge Assumptions**
Quoted span (Assumption Audit scan): "C5 | 1 | tops out near two-thirds RTE [Assumes: A13] | A13 (no near-term breakthrough above ~65-68%) | yes — new, added to table"
Band: **Rigorous**
Justification: The Assumptions Table uses the four-type scheme throughout with em-dash-separated Accept/Challenge/Discard verdicts (e.g., A2, A6, A7 Discarded with specific justification), and the Assumption Audit scan confirms the end-of-Phase-4 surfacing step ran exhaustively and fed four newly-surfaced assumptions (A11-A14) back into the table.

**Criterion 3: Establish Ground Truths**
Quoted span: "?-marked: GT-12 (1 of 12); read-at-source named for GT-1 through GT-11, each feeding at least one HIGH chain except GT-7, GT-8, GT-9, which feed only MEDIUM chains C8/C9/C10."
Band: **Rigorous**
Justification: All 12 ground truths carry stable IDs, provenance labels, and source citations; the lone unverified entry (GT-12?) is both suffixed and enumerated, and every unsuffixed GT feeding a HIGH-confidence chain (GT-1 through GT-6, GT-11) names its read-at-source location.

**Criterion 4: Reason Upward**
Quoted span (self-audit scan, chain-form table): "C10 | C8 + C9 + GT-9 + GT-12? | yes | n/a | yes | MEDIUM | yes | none"
Band: **Rigorous**
Justification: Every section-4 chain shows `Form conforming? = yes` with `Dependency clean? = yes`; each chain carries a genuine intermediate step; Abandoned Reasoning records four specific, non-generic dead ends each citing GT/C ids; no analogy is used as direct evidence anywhere in section 4.

**Criterion 5: Validate**
Quoted span: "Falsification. This analysis's headline conclusion is false if: (a) a commercially available or peer-reviewed, third-party-measured molten-salt ... system ... demonstrates an AC-to-AC round-trip efficiency above 85% at any scale (overturns chain C6); or (b) an itemized, vendor-quoted installed cost ... comes in at or below the equivalent installed cost of a 5 MWh lithium-ion BESS ... (overturns chain C10)."
Band: **Rigorous**
Justification: The adversarial pass record carries all required parts (Recompute, Sensitivity, Rival, Premise, Causes, Clusters each with a Disposition, Falsification); every MEDIUM/LOW chain (C8, C9, C10, C11) names its own downgrade cause and closure path per D-07; no chain rated HIGH consumes a `GT-N?` input; the Conclusion's MEDIUM rating matches its weakest non-EXCEPT'd contributing chain (C10).

**Criterion 6: Conclusion-to-Ground-Truth Traceability**
Quoted span (self-audit scan, claim-inventory table): "\"Key insight: The claim's two sub-parts are not independent...\" | bold lead-in | yes | bold lead-in whose colon closes the bold span, carrying its assertion on the same line | C7, C6, C8, C9, C10"
Band: **Rigorous**
Justification: All five section-6 claims trace to named section-4 chains with no new reasoning introduced in section 6, and the Key Insight (the heat-vs-electricity and thermal-vs-electrical cost-basis conflation) is a non-obvious finding distinct from the Recommended Approach's restatement of the verdict.

**Gate result:** No criterion scored Absent; zero criteria scored Hand-wavy (at most one permitted). Both gate conditions are met — the analysis clears the Self-Audit Gate on the first pass; no Fix/Repeat cycle was required.

---

## 1. Problem Essence

**Core problem:** Does a 5 MWh molten-salt (solar-salt, 290-565°C) thermal energy-storage system achieve an electricity-to-heat-to-electricity round-trip efficiency above 85%, and is such a system cost-competitive, at that same 5 MWh nameplate capacity, with a lithium-ion battery system — or does the claim fail on one or both counts?

**Success criteria:**
1. The Conclusion states, with a derivation chain, whether the 290-565°C range is an accurate characterization of solar-salt CSP sensible-heat storage (sub-claim 1 verdict).
2. The Conclusion states, with a derivation chain built from the Carnot relation and real-cycle/real-system efficiency data, a quantified achievable range for electricity-to-electricity round-trip efficiency, and compares it against the claimed >85% figure (sub-claim 2 verdict).
3. The Conclusion states, with a derivation chain built from itemized storage-media and power-block cost components, a quantified installed-cost comparison between a 5 MWh molten-salt electricity-round-trip system and a 5 MWh lithium-ion battery system, and states whether cost-competitiveness holds at that scale (sub-claim 3 verdict).
4. The Conclusion renders one overall verdict — holds / partially holds / fails — for the compound claim as stated, tracing that verdict to the three sub-claim verdicts above.

---

## 2. Assumptions Table

| Assumption | Type | Treatment | Verdict | Verification |
|---|---|---|---|---|
| A1: 290-565°C is the standard/characteristic operating window for solar-salt (NaNO3/KNO3) sensible-heat CSP storage | convention | explicitly challenge before accepting | Accept — confirmed by GT-1; multiple independent sources match this exact range | GT-1 |
| A2: A system can round-trip electricity through heat and back to electricity at >85% efficiency in the 290-565°C window | untested belief | verify or flag unverified | Discard — contradicted by GT-2, GT-3, GT-4, GT-5, GT-6 via chains C2-C6; achievable RTE is approximately 37-68%, not above 85% | unverified — flagged, now refuted by chains C2-C6 |
| A3: The claimed round-trip efficiency refers to electricity-in/electricity-out, not heat-in/heat-out | convention / interpretive framing | explicitly challenge | Accept — the only reading consistent with comparing the system to a lithium-ion "battery system" on a nameplate-MWh basis; corroborated by GT-11 | GT-11, internal consistency argument |
| A4: The charging step uses simple resistive (Joule) heating, not a heat-pump (Carnot-battery) cycle | untested belief | flag as unstated; analyze both branches | Challenge — unresolved by the claim's own wording; both architectures carried through chains C4 (resistive) and C5 (heat-pump) and both tested against 85% | unverified — flagged; both cases computed in C4, C5 |
| A5: "Cost-competitive ... at the same nameplate MWh capacity" means comparable $/kWh installed system cost for an electricity-in/electricity-out system at 5 MWh | convention / interpretive framing | adopt explicitly, state alternative readings considered | Accept — the only reading that makes "same nameplate capacity" comparable to a lithium-ion "battery system" | internal consistency argument |
| A6: Cheap molten-salt storage-media cost ($/kWh-thermal) directly translates into a cheap $/kWh-electrical system cost | untested belief | verify or flag unverified | Discard — contradicted by GT-7 vs. GT-9/GT-10 via chains C8, C10: the thermal-cost figure omits power-conversion equipment and the round-trip-efficiency penalty entirely | unverified — flagged, now refuted by chains C8, C10 |
| A7: Power-conversion (turbine/heat-pump) capital cost per kW scales down with system size the way battery-cell and inverter cost per kW does | untested belief | verify or flag unverified | Discard — contradicted by GT-8 via chain C9: rotating thermal machinery shows a severe, documented diseconomy of scale that battery/power-electronics manufacturing does not share to the same degree | unverified — flagged, now refuted by chain C9 |
| A8: 5 MWh implies a specific power rating / discharge duration | current constraint | record expiry/resolution conditions | Challenge — expires (is resolved) the moment a duration or power rating is specified by whoever advances the claim; until then, flagged as unresolved ambiguity and bracketed at 1-5 hours | unverified — flagged; bracketed in chain C9 |
| A9: Ambient / steam-turbine condenser temperature ≈30°C is the correct cold-reservoir value for the Carnot calculation (not the 290°C cold-tank return temperature) | convention | record expiry conditions | Accept — supported by GT-3; expires if climate/cooling-method choice materially changes the actual condenser design temperature | GT-3 |
| A10: The 5 MWh scale at which the claim is evaluated is representative of how this technology would actually be deployed commercially | untested belief | verify or flag unverified | Challenge — GT-11 shows commercial deployments of this technology cluster at far larger scale (100+ MWh) and for direct-heat delivery, not 5 MWh electricity round-trip | unverified — flagged; treated as corroborating evidence only, chain C11 |
| A11: Dividing a $/kWh-thermal figure by round-trip efficiency is an adequate first-order approximation of the true relationship between storage-media cost and delivered-electricity cost | untested belief | flag — modeling simplification, not an itemized cost model | Challenge — reasonable engineering approximation, not verified against an itemized vendor cost breakdown; caps chain C8 at MEDIUM | unverified — flagged; surfaced at C8 during Assumption Audit |
| A12: A 1-5 MW steam-turbine/ORC power-block cost bracket of roughly $800-1,500/kW is representative of what a 5 MWh molten-salt electricity-round-trip power block would actually cost | untested belief | flag — interpolated from adjacent-scale data points, not a direct quote at this exact scale | Challenge — caps chain C9 at MEDIUM; would be resolved by an itemized vendor quote | unverified — flagged; surfaced at C9 during Assumption Audit |
| A13: No major, near-term breakthrough in turbomachinery or heat-pump component efficiency will push demonstrated Carnot-battery round-trip efficiency materially above the ~65-68% ceiling observed in current literature, within the planning horizon relevant to a claim about current/near-term technology | current constraint | record expiry conditions | Accept — expires if a published, verified demonstration exceeds today's ~65-68% ceiling; does not affect the "as currently/near-term demonstrated" framing of chain C5/C6 | unverified — flagged; surfaced at C5 during Assumption Audit |
| A14: Second-order market/vendor-specialization evidence (chain C11) is corroborating, not primary, evidence for the cost verdict | convention / methodological scoping choice | state explicitly to avoid overweighting market evidence relative to the physics/cost chains | Accept — named explicitly so chain C11 is not mistaken for a primary load-bearing chain | surfaced at C11 during Assumption Audit |

---

## 3. Ground Truths

- **GT-1** Solar salt (eutectic NaNO3/KNO3, commonly cited as 60/40 by weight, liquidus ≈221-238°C) is operated commercially in two-tank CSP storage systems across a window whose cold end (≈290°C) is held above the liquidus to prevent freezing, and whose hot end (≈565°C, thermal-stability/decomposition ceiling ≈585°C) is the industry-standard upper bound — source: patent and academic CSP literature retrieved via web search (e.g., US Patent 9,080,788; US Patent 10,254,012; academic CSP thermal-storage reviews); read-at-source: multiple independently retrieved documents directly state "minimum temperature of 290 °C" and "above this temperature [565°C]... the solar salt is not suitable for the service" / "thermal stability at temperatures of up to ~585°C."
- **GT-2** Carnot's theorem (second law of thermodynamics): the maximum possible efficiency of any heat engine operating between a hot reservoir at absolute temperature Th and a cold reservoir at Tc is η_max = 1 − Tc/Th — source: foundational thermodynamic law (physical law, not an empirical citation); read-at-source: numeric application cross-checked against an independently retrieved source (see GT-3) stating "a theoretical Carnot efficiency of about 63%" for the exact Th/Tc pair used in chain C2, confirming correct application of the law.
- **GT-3** Standard steam-turbine design points: turbine inlet temperature ≈565°C (the creep limit of stainless steel) and condenser temperature ≈30°C are cited as typical for steam power cycles — source: mechanical-engineering reference material retrieved via web search; read-at-source: "steam turbine entry temperatures are typically around 565°C and steam condenser temperatures are around 30°C... a theoretical Carnot efficiency of about 63% [is] given compared with an actual efficiency of 42% for a modern coal-fired power station."
- **GT-4** Real steam Rankine cycles at ~565°C live-steam conditions achieve roughly 38-42% actual (gross) thermal efficiency in modern supercritical/ultra-supercritical plants — source: mechanical-engineering reference material retrieved via web search; read-at-source: "most supercritical power plants adopt a steam inlet pressure of 24.1 MPa and inlet temperature between 538°C and 566°C, which results in plant efficiency of 40%... actual efficiency of 42% for a modern coal-fired power station."
- **GT-5** Resistive (Joule) heating converts electrical energy to thermal energy at approximately 98% efficiency, with losses limited to minor resistive/distribution losses — source: foundational electrical-engineering physical law/definition (I²R heating is the only loss mechanism in a well-designed resistive heater); no external citation search required for this definitional fact.
- **GT-6** Demonstrated and near-term "Carnot battery" / pumped-thermal-electricity-storage (PTES) systems — heat-pump charge, heat-engine discharge — report round-trip (electricity-to-electricity) efficiencies of roughly 39-65%, with leading-edge claims up to ~65-68% (e.g., a supercritical-CO2 Brayton-cycle PTES at 38.9%; a 150 kW argon-Brayton system at Newcastle University at 60-65%; a 560°C SPIC demonstration claiming >65%; Malta Inc. targeting up to 60%) — source: academic/industry review literature and press coverage retrieved via web search; read-at-source: "a supercritical CO2 Brayton cycle PTES system achieved a round-trip efficiency of 38.9%... an argon-based Brayton cycle with 150 kW capacity from Newcastle University has a round-trip efficiency of 60% to 65%... a recent SPIC system claims a scaled round-trip efficiency of over 65%."
- **GT-7** Bare molten-salt sensible-heat storage media (tank + salt + insulation only, excluding power-conversion equipment) costs roughly $22-73 per kWh-thermal (NREL/Kolb et al. 2011 cite $22-30/kWh-th; more recent industry estimates cite €15-70/kWh-th; Crescent Dunes storage ≈$80M for 1,100 MWh-thermal ≈$73/kWh-th) — source: NREL technical reports and industry press retrieved via web search; read-at-source: "Molten nitrate salt storage costs 22-30 $/kWhth according to NREL (Kolb et al., 2011)... the molten salt storage component at the 110 MW Crescent Dunes facility for 10 hours of storage was estimated at around $80 million for 1,100 megawatt hours."
- **GT-8** Small-scale (<2 MW) rotating thermal-machinery power-conversion equipment (steam back-pressure turbogenerators, ORC units) shows a strong, documented diseconomy of scale: roughly $700/kW at 50 kW scale down to <$200/kW above 2,000 kW scale for turbogenerators, $2,500-5,775/kW for ORC units in the 2-50 kWe range, and a ~5.5 MW mini power-plant anchor cited at ~$1,500/kW; each 10x scale-up is associated with roughly 20-40% lower unit cost — source: engineering cost-survey and techno-economic literature retrieved via web search; read-at-source: "the capital cost of a back-pressure turbogenerator... varies from about $700/kW for a small system (50 kW) to less than $200/kW for a larger system (>2,000 kW)... one mini power plant produces 5.5 MW of electricity at around $1,500 per kW... each 10x scale-up is generally associated with 20-40% lower unit costs."
- **GT-9** 2025 utility-scale lithium-ion battery-energy-storage-system (BESS) installed costs: cell/pack prices ≈$70-94/kWh; full installed system cost for long-duration (≥4 hr) utility projects ≈$125/kWh (ex-China/US) up to a broader project-cost range of $600-1,400/kWh depending on project scope and region — source: industry price-tracking reports (BloombergNEF-style pack-price reporting, project-cost surveys) retrieved via web search; read-at-source: "Battery pack prices for stationary storage fell to $70/kWh in 2025... the cost of a full battery storage system connected to the grid is $125/kWh as of October 2025 for long-duration... utility-scale battery projects... total costs are significantly higher. Project cost ranges for utility-scale storage typically fall within approximately $600-$1,400 per kWh."
- **GT-10** German Energy Storage Association (BVES) fact-sheet comparison, cited in industry press: molten-salt thermal storage ≈€25-70/kWh-thermal versus lithium-ion full system ≈€833/kWh-electrical (STEAG demonstration project), publicly framed as molten salt being "33 times" cheaper — source: industry press coverage (solarthermalworld.org) retrieved via web search; read-at-source: "Molten salt tanks are around 33 times less expensive than electric batteries when it comes to storing a kilowatt-hour... the figures on the fact sheet range from EUR 25 to 70 EUR/kWhth for molten salt, while the first six demonstration systems which involved large-scale lithium-ion batteries... cost EUR 833/kWhel."
- **GT-11** Commercial thermal-battery vendors (e.g., Rondo Energy) build and deploy this class of storage at large scale (100 MWh-class installations) specifically to deliver heat/steam directly to industrial processes, explicitly not to reconvert the stored heat back to electricity, and cite round-trip (electricity-to-heat-to-heat) efficiency above 97% for that direct-heat use case — source: industry press coverage retrieved via web search; read-at-source: "Rondo's technology is designed specifically for industrial process heat applications rather than round-trip electricity generation... Rondo's heat storage medium... stores heat at over 1000°C with a claimed round-trip efficiency above 97%... a 100 MWh heat battery it installed in California."
- **GT-12?** Small-scale (sub-10 MWh) lithium-ion BESS installed costs trend toward the upper portion of GT-9's range due to lost fixed-cost (BOS/interconnection/EPC) economies of scale relative to multi-hundred-MWh projects — unverified: this specific figure is the search synthesis's own extrapolation ("a mid-range estimate might be about $900 per kWh... This would suggest similar per-kWh costs for smaller 5 MWh projects") rather than a directly cited quote for a 5 MWh project; no itemized small-scale vendor quote was located and opened in this analysis.

**Provenance summary:** `?`-marked: GT-12 (1 of 12). Read-at-source: GT-1 (patent/academic CSP documents, "290 °C"/"565° C" quoted directly), GT-2 (cross-checked numeric application against GT-3's independently retrieved source), GT-3 (mechanical-engineering reference, "565°C... 30°C... theoretical Carnot efficiency of about 63%" quoted directly), GT-4 (mechanical-engineering reference, "efficiency of 40%... actual efficiency of 42%" quoted directly), GT-6 (PTES review/press literature, specific percentage figures quoted directly), GT-7 (NREL/Kolb et al. 2011 and Crescent Dunes cost figures quoted directly), GT-8 (engineering cost-survey figures quoted directly), GT-9 (2025 price-tracking figures quoted directly), GT-10 (BVES/solarthermalworld figures quoted directly), GT-11 (Rondo Energy press coverage, ">97%" and "100 MWh" quoted directly). GT-5 is a definitional physical-law fact requiring no external source.

---

## 4. Derivation Chains

### Conclusion C1: The 290-565°C temperature range accurately characterizes solar-salt CSP sensible-heat storage (sub-claim 1)

GT-1 (solar-salt's 290-565°C design window, read at source)
→ this exact range matches the published freeze-margin-to-thermal-stability window for commercial two-tank solar-salt CSP plants
→ sub-claim 1's temperature-range description is an accurate characterization of solar-salt sensible-heat storage, not an invented or unusual figure

**Pre-check:** head GT-1 · ?-marked: none · lowest cited: none · Inputs ceiling: HIGH
**Confidence:** HIGH — rival not applicable (no competing characterization survives GT-1's explicit figures); inputs read-at-source; the inference is a direct factual match.

### Conclusion C2: The ideal (Carnot) ceiling for the discharge-side heat engine in this temperature window is approximately 63.8%

GT-2 (Carnot law, η_max = 1 − Tc/Th) + GT-3 (565°C turbine-inlet / ~30°C condenser are the standard design points)
→ substituting Th = 838 K and Tc = 303 K into the Carnot formula yields an ideal heat-engine ceiling of approximately 63.8%
→ this ceiling bounds only the discharge-side heat-to-electricity conversion step, not the full electricity-to-electricity round trip by itself

**Pre-check:** head GT-2, GT-3 · ?-marked: none · lowest cited: none · Inputs ceiling: HIGH
**Confidence:** HIGH — arithmetic recomputes (1 − 303/838 = 0.638); the rival of using the 290°C cold-tank return temperature as Tc is ruled out, see Abandoned Reasoning Dead End 1.

### Conclusion C3: A realistic discharge-side (heat-to-electricity) efficiency for this window is approximately 38-42%

GT-4 (real steam Rankine cycles at ~565°C achieve roughly 38-42% actual thermal efficiency) + C2 (63.8% ideal Carnot ceiling)
→ the realistic figure sits well inside the ideal ceiling (38-42% versus 63.8%), confirming the real-cycle figure is physically consistent rather than an outlier
→ a realistic discharge-side heat-to-electricity efficiency for this temperature window is approximately 38-42%

**Pre-check:** head GT-4, C2 (HIGH) · ?-marked: none · lowest cited: HIGH · Inputs ceiling: HIGH
**Confidence:** HIGH — GT-4's cited figure is independently consistent with C2's derived ceiling; no rival discharge-efficiency figure survives in the literature reviewed.

### Conclusion C4: A simple resistive-charge / steam-turbine-discharge architecture achieves approximately 37-41% round-trip electricity efficiency

GT-5 (resistive Joule heating converts electricity to heat at roughly 98% efficiency) + C3 (discharge-side efficiency approximately 38-42%)
→ for a simple electric-heater-charge, steam-turbine-discharge architecture, round-trip electricity efficiency is the product of charge efficiency and discharge efficiency [Assumes: A4]
→ this architecture's achievable round-trip electricity-to-electricity efficiency is approximately 37-41%, roughly half the claimed figure

**Pre-check:** head GT-5, C3 (HIGH) · ?-marked: none · lowest cited: HIGH · Inputs ceiling: HIGH
**Confidence:** HIGH — arithmetic recomputes (0.98 × [0.38, 0.42] = [0.372, 0.412]); the rival architecture (heat-pump charging) is carried separately as C5, not treated as unsettled here; A4 is scoped to this architecture only and does not affect the endpoint's validity for that architecture.

### Conclusion C5: Even the most advanced demonstrated "Carnot battery" architecture tops out at roughly two-thirds round-trip efficiency

GT-6 (demonstrated and near-term Carnot-battery / pumped-thermal systems report round-trip efficiencies of roughly 39-68%)
→ even the most advanced heat-pump-charge, heat-engine-discharge architecture, which could in principle approach 100% round trip in a fully reversible idealization, tops out at roughly two-thirds round-trip efficiency once real compressor, turbine, and heat-exchanger irreversibilities are counted [Assumes: A13]
→ no demonstrated or near-term credible architecture for electricity-to-heat-to-electricity round-tripping in this temperature range reaches the claimed above-85% figure

**Pre-check:** head GT-6 · ?-marked: none · lowest cited: none · Inputs ceiling: HIGH
**Confidence:** HIGH — A13 is scoped into the endpoint itself ("no currently demonstrated or near-term credible architecture"); if a future breakthrough occurred, that would not falsify this time-scoped claim about current/near-term technology, so the endpoint stands regardless of A13's outcome. The ideal 100%-reversible-limit rival is acknowledged but is not demonstrated, so it does not unseat the endpoint.

### Conclusion C6: The achievable electricity-to-electricity round-trip efficiency range for this technology is approximately 37-68%, well short of the claimed >85%

C4 (simple architecture, approximately 37-41%) + C5 (advanced architecture, approximately 39-68%)
→ combining the two architecture-specific ranges by union gives an achievable range for electricity-to-electricity round-trip efficiency of approximately 37-68%
→ the claimed above-85% system round-trip efficiency exceeds even the most optimistic best-demonstrated real-world figure by roughly twenty percentage points
→ sub-claim 2 as stated is false for any currently demonstrated or near-term credible technology

**Pre-check:** head C4 (HIGH), C5 (HIGH) · ?-marked: none · lowest cited: HIGH · Inputs ceiling: HIGH
**Confidence:** HIGH — the union of [37,41] and [39,68] is a direct deduction ([37,68]); both contributing chains are HIGH and the rival (ideal reversible 100% limit) is already ruled out as "not demonstrated" on C5's own confidence line.

### Conclusion C7: The genuinely-achievable >97% figure for this storage class belongs to the heat-to-heat use case, not electricity round-trip

GT-11 (commercial thermal-battery vendors deliver heat directly to industrial processes rather than reconverting to electricity, citing above-97% efficiency for that heat-to-heat use case)
→ the above-97% figure genuinely achievable for this class of storage belongs to the heat-to-heat use case, not the electricity-to-electricity use case the claim describes
→ real commercial practice corroborates that the claimed combination of above-85% efficiency and electricity round-tripping does not coexist in any deployed technology

**Pre-check:** head GT-11 · ?-marked: none · lowest cited: none · Inputs ceiling: HIGH
**Confidence:** HIGH — direct reading of GT-11; rival not applicable, this chain corroborates C6 rather than competing with it.

### Conclusion C8: The storage-media cost component alone, expressed per kWh-electrical, is approximately $32-197/kWh

GT-7 (storage-media cost approximately $22-73 per kWh-thermal) + C6 (achievable round-trip efficiency approximately 37-68%)
→ converting a thermal-cost basis to an electricity-delivered-cost basis requires dividing by round-trip efficiency, since each kWh of electricity delivered requires charging roughly one over RTE kWh-thermal worth of energy [Assumes: A11]
→ the storage-media component alone, expressed on an electricity-delivered basis, costs approximately 32 to 197 dollars per kWh-electrical, far above the headline thermal-only figures such as GT-10's cited "33 times cheaper" comparison, which omits round-trip-efficiency and power-conversion costs entirely

**Pre-check:** head GT-7, C6 (HIGH) · ?-marked: none · lowest cited: HIGH · Inputs ceiling: HIGH
**Confidence:** MEDIUM — A11 (dividing thermal cost by RTE is a first-order approximation, not an itemized cost model) is unpriced: closing it requires an itemized bottom-up capex model for an actual thermal-ETES system, which this analysis does not have; until then, this chain's output is an order-of-magnitude bracket, not a precise figure.

### Conclusion C9: The power-block (power-conversion equipment) adds approximately $160-1,500/kWh at 5 MWh scale, depending on assumed duration

GT-8 (small-scale power-block capital cost diseconomy of scale, roughly $200-5,775/kW depending on scale, with a ~5.5 MW/$1,500/kW anchor point)
→ interpolating to the 1-to-5 MW range relevant at this storage capacity gives an estimated power-block cost of roughly 800 to 1,500 dollars per kW [Assumes: A12]
→ a 5 MWh system at a plausible 1-to-5-hour discharge duration implies a power rating of roughly 1 to 5 MW [Assumes: A8]
→ the power-block capital cost alone, spread only over 5 MWh of storage, plausibly adds on the order of 160 to 1,500 dollars per kWh to the installed system cost depending on the assumed duration

**Pre-check:** head GT-8 · ?-marked: none · lowest cited: none · Inputs ceiling: HIGH
**Confidence:** MEDIUM — A8 (duration/power-rating is not stated in the claim) and A12 (the power-block $/kW bracket is interpolated from adjacent-scale data points, not a direct quote at 1-5 MW) are both unpriced beyond the bracket already carried in the hops; closing them requires either a stated duration from whoever advances the claim, or an itemized vendor quote at this exact scale.

### Conclusion C10: Sub-claim 3's unqualified cost-competitiveness claim does not hold at the stated 5 MWh scale

C8 (storage-media electric-equivalent cost approximately $32-197/kWh) + C9 (power-block adds approximately $160-1,500/kWh) + GT-9 (2025 installed lithium-ion system costs approximately $125-1,400/kWh) + GT-12? (small-scale lithium-ion systems trend toward the upper portion of that range)
→ summing the storage-media and power-block components gives a plausible installed cost for a 5 MWh electricity-round-trip molten-salt system of roughly 190 to 1,700 dollars per kWh before balance-of-plant and engineering overhead
→ this range sits at or above the lithium-ion range under typical assumptions, and reaches rough parity with lithium-ion only under the most favorable plausible configuration for the thermal system
→ sub-claim 3's unqualified cost-competitiveness claim does not hold at the stated 5 MWh scale

**Pre-check:** head C8 (MEDIUM), C9 (MEDIUM), GT-9, GT-12? · ?-marked: GT-12? · lowest cited: MEDIUM · Inputs ceiling: MEDIUM
**Confidence:** MEDIUM — GT-12? (small-scale Li-ion cost extrapolation) would be removed as a cause of the downgrade by an itemized vendor-quote library for sub-10 MWh BESS installed costs; C8 (MEDIUM) and C9 (MEDIUM) are named and not re-explained here, as their own confidence lines carry their closure paths; this chain is capped at MEDIUM by the lowest-rated chains it cites.

### Conclusion C11: [Speculative — corroborating only, not load-bearing] Market/vendor evidence corroborates the cost verdict

GT-11 (commercial thermal-battery vendors deploy only at large scale for direct industrial-heat delivery, not small-scale electricity round-trip)
→ no commercial vendor currently offers a turnkey 5 MWh molten-salt electricity-battery product, while multiple vendors offer turnkey 5 MWh or smaller lithium-ion battery-energy-storage containers as a mature, standardized commercial category
→ this absence of a commercial product at this scale and use case is independent market evidence corroborating the capex-based conclusion in C10, though it is weaker, corroborating evidence rather than a primary load-bearing chain [Assumes: A14]

**Pre-check:** head GT-11 · ?-marked: none · lowest cited: none · Inputs ceiling: HIGH
**Confidence:** MEDIUM [Speculative — this chain is not cited on the Conclusion section's head and does not support any claim there beyond the Trade-offs line's explicit framing as corroborating color] — Inference axis: the absence-of-product inference is circumstantial; no available evidence (vendor R&D roadmaps, investor disclosures) was reviewed in this analysis that would settle whether absence reflects fundamental uneconomics or mere market immaturity, and this cause has no verification path within this analysis's scope. Rivals axis: "absence reflects early-stage immaturity, not fundamental uneconomics" is live and not ruled out, named here.

**Unverified input rule (D-07) summary:** Chains C8, C9, C10, and C11 are rated MEDIUM; each names its own `GT-N?`/`[Assumes: A-N]` cause and the verification that would remove it, or an explicit account of why no verification path exists within this analysis's scope (C11). No chain rated HIGH consumes a `GT-N?` input. Every chain is rated no higher than the lowest-rated chain its head cites (C10 ≤ MEDIUM because C8 and C9 are MEDIUM; C10 also carries GT-12? directly).

---

## 5. Abandoned Reasoning

### Dead End 1: Using the 290°C cold-tank temperature as the Carnot cycle's cold reservoir

**What was tried:** Computing the ideal heat-engine ceiling using Th=565°C and Tc=290°C (the storage tank's own "cold" temperature) instead of the turbine's actual condenser temperature.

**Why abandoned:** This conflates the storage medium's engineering return temperature (chosen for freeze margin above the ~221-238°C melting point, per GT-1) with the heat engine's actual thermodynamic cold reservoir, which is the condenser (~30°C, per GT-3). Using Tc=290°C would yield an even lower (~33%) ceiling, which does not change the overall verdict but misapplies GT-2.

**What it ruled out:** Confirms that GT-3's ~30°C condenser figure, not the storage tank's 290°C return temperature, is the correct input to C2's Carnot calculation, and that even this more charitable 290°C misreading would not rescue the claim.

### Dead End 2: Treating "round-trip efficiency" as a heat-to-heat metric to charitably rescue the claim

**What was tried:** Considering whether the >85% figure could be true if "round-trip efficiency" meant heat delivered back as heat/steam (as in GT-11's Rondo Energy example), rather than reconverted to electricity.

**Why abandoned:** The claim explicitly frames the comparison as cost-competitiveness against a lithium-ion "battery system" of the "same nameplate capacity," which only makes sense if both systems deliver electricity in and electricity out; a heat-to-heat reading would make the cost comparison incoherent, since industrial heat batteries are not sold or costed as electricity storage (GT-11). Discarded per assumption A3.

**What it ruled out:** Establishes that the electricity-to-electricity interpretation (A3), not a charitable heat-to-heat reading, is the correct and only coherent interpretation of the claim as stated — closing off a reading that would have made sub-claim 2 trivially true but sub-claim 3 meaningless.

### Dead End 3: Fully modeling lithium-ion cycle-life/degradation economics into the cost comparison

**What was tried:** Extending chain C10 to include a levelized-cost-of-storage (LCOS) model incorporating lithium-ion calendar/cycle degradation versus molten salt's effectively unlimited sensible-heat cycle life.

**Why abandoned:** This refinement would not change the primary verdict — thermal-ETES already loses on capex and round-trip efficiency before cycle life is considered — and no ground truth for lithium-ion cycle-life/degradation figures was verified in this analysis. Abandoned as a non-load-bearing refinement outside the verified-evidence scope of this analysis; not cited on any chain's head.

**What it ruled out:** Confirms that the cost verdict in C10 does not depend on resolving the cycle-life question, so the analysis need not acquire that evidence to reach a confident verdict on the claim as stated.

### Dead End 4: Treating absence of a commercial 5 MWh thermal-ETES product as, by itself, decisive proof of uneconomics

**What was tried:** Initially considering C11 (market/vendor evidence) as a primary, load-bearing chain for the cost verdict, equal in weight to C8-C10.

**Why abandoned:** The inference "no such product exists, therefore it is uneconomic" is circumstantial — it could also reflect market immaturity, lack of demand, or lack of effort, a live rival this analysis did not rule out. Promoting it to primary status would have overstated the analysis's confidence; it was demoted to corroborating, speculative, non-load-bearing status (marked `[Speculative]` on C11).

**What it ruled out:** Prevents the cost verdict from resting on circumstantial market evidence rather than the itemized capex reasoning in C8-C10, keeping the Conclusion's confidence rating honestly tied to its strongest evidence.

---

## 6. Conclusion

**Recommended approach:** Treat the claim as failing as stated: accept the temperature-range description (sub-claim 1) as accurate (chain C1), but reject both the ">85% round-trip efficiency" claim, whose achievable range is approximately 37-68% (chain C6), and the unqualified "cost-competitive at 5 MWh" claim, whose installed cost sits at or above a comparable lithium-ion system under typical assumptions and reaches parity only in the most favorable plausible configuration (chain C10).

**Key insight:** The claim's two sub-parts are not independent — the >85% efficiency figure appears to conflate heat-to-heat round-trip efficiency (genuinely above 97% for this class of storage, chain C7) with electricity-to-electricity round-trip efficiency (capped by an unavoidable heat-engine discharge step at roughly 64% ideally and 37-68% in practice, chain C6); and the cost-competitiveness figure appears to conflate cheap bare storage-media cost ($/kWh-thermal) with the full installed electricity-in/electricity-out system cost, which must also carry a power-conversion "power block" that does not shrink economically at 5 MWh scale the way battery and inverter manufacturing does (chains C8, C9, C10). Reasoning by analogy to large-CSP-scale thermal-storage cost figures, or to heat-battery efficiency figures, is exactly the trap that produces a claim like this one.

**Trade-offs acknowledged:** This verdict is scoped to currently demonstrated and near-term technology at the small (5 MWh), short-duration, electricity-round-trip use case specifically named in the claim; it does not rule out molten-salt or other sensible-heat thermal storage being genuinely cost-effective at much larger scale (100+ MWh) or for direct industrial-heat delivery rather than electricity reconversion — which is in fact where this technology is commercially deployed today (chain C11, speculative/corroborating only). The cost verdict (chain C10) also carries a wide bracket driven by an unstated discharge duration in the original claim; a longer stated duration (lower power rating) would narrow, but not close, the gap with lithium-ion (chain C9).

**Pre-check:** head C1 (HIGH), C6 (HIGH), C10 (MEDIUM) · ?-marked: none directly on the Conclusion, GT-12? carried via C10 · lowest cited: MEDIUM (C10) · Inputs ceiling: MEDIUM
**Confidence:** MEDIUM — driven down by C10's MEDIUM rating; C10 itself names its own GT-12? input and its contributing chains C8 (MEDIUM) and C9 (MEDIUM), each of which names what would close it (an itemized vendor cost model in both cases); the physics verdict alone (chains C1, C6, C7) would support a HIGH-confidence rejection of the efficiency sub-claim, but the compound claim's overall confidence is capped by its weaker, cost-side component.

**Overall verdict:** The claim **fails as stated**. Sub-claim 1 (temperature range) **holds**. Sub-claim 2 (>85% round-trip efficiency) **fails** — no currently demonstrated or near-term credible technology reaches above roughly 68%. Sub-claim 3 (cost-competitiveness at 5 MWh) **fails under typical assumptions and reaches at best rough parity under the most favorable plausible configuration** — it does not hold as an unqualified claim. The compound claim is best read as a conflation of two true-but-different statements (heat-to-heat efficiency above 97%, and large-scale thermal-storage media cost far below battery cost) rather than a correct description of a 5 MWh electricity-round-trip system.
