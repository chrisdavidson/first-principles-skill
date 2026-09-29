## Techniques not applied (process output)

- fishbone — not applicable — the assumption space here is a linear, well-bounded numeric derivation (load → battery; PSH/derate → array), not a broad multi-causal diagnostic space; a category-based cause brainstorm adds no resolving power over the direct engineering decomposition already performed in Section 4.
- five-whys (causal mode) — not applicable — there is no anomalous symptom to root-cause; this is a forward sizing design, not a failure diagnosis. (Reduce-to-primitives mode was effectively exercised via the estimate procedure's unit-factor decomposition of the derate and load figures.)
- inversion — not applicable — the conclusion is a plan/recommendation, not a bare claim; per the inversion-vs-pre-mortem decision rule, the plan-appropriate adversarial technique (pre-mortem) is applied at Phase 5 instead. A separate Phase 2 inversion pass was not run because the goal did not feel suspiciously under-examined — the derate, DoD, and load uncertainties were already surfaced going into Phase 3.
- theoretical-limit — not applicable — this is a practical engineering sizing exercise, not a question of the physical ceiling on off-grid solar/storage efficiency; no governing hard-constraint ceiling question was posed that convention might be hiding.

## Assumption Audit scan (process output)

| Chain | Step | Step Text (brief) | Assumption surfaced? | Added to Table? |
|-------|------|--------------------|-----------------------|------------------|
| C1 | 1 | December is the binding design month at 50° tilt | A-11 (unobstructed, true-south siting implicit in the PVGIS run) | yes |
| C1 | 2 | worst-month PSH = 170.36÷31 = 5.50 h/day | none | n/a |
| C1 | 3 | break-even array = 1500÷(5.50×0.75) = 364 W | none | n/a |
| C1 | 4 | apply 1.2× recharge margin → 436 W | none | n/a |
| C1 | 5 | round to ≈450 W STC | none | n/a |
| C2 | 1 | usable = 1.5×3 = 4.5 kWh | none | n/a |
| C2 | 2 | nameplate = 4.5÷0.80 = 5.625 kWh | none | n/a |
| C2 | 3 | round to ≈5.6-6.0 kWh nameplate / 4.5 kWh usable | none | n/a |
| C3 | 1 | 450 W ÷ 48 V ≈ 9.4 A charge current | A-10 (48 V nominal bus assumed for this check) | yes |
| C3 | 2 | 9.4 A ÷ 120 Ah ≈ C/12.8 vs LiFePO4 max charge rate | A-13 (LiFePO4 accepts up to ~0.5-1C charge) | yes |
| C3 | 3 | battery charge-acceptance is not the binding constraint | none | n/a |
| C4 | 1 | daily array output = 450×5.50×0.75 = 1,856 Wh | none | n/a |
| C4 | 2 | surplus over 1,500 Wh load = 356 Wh (~24%) | none | n/a |
| C4 | 3 | surplus is what lets the battery recover after a cloudy stretch | A-12 (no backup generator; multi-week excursions beyond this surplus+3-day battery are accepted risk, not covered by sizing) | yes |
| C4 | 4 | autonomy and worst-month array sizing are coupled, not independent | none | n/a |
| C5 | 1 | baseline non-fridge, non-connectivity loads ≈1.0 kWh/day | none | n/a |
| C5 | 2 | an electric fridge typically adds ~0.7-1.2 kWh/day | none | n/a |
| C5 | 3 | 1.5 kWh/day is only consistent with non-electric refrigeration and no connectivity | none | n/a |
| C5 | 4 | a typical electrified year-round load is ~2.5-3.0 kWh/day | none | n/a |
| C6 | 1 | break-even array @2.5 kWh/day = 606 W | none | n/a |
| C6 | 2 | with margin → ≈730-750 W STC | none | n/a |
| C6 | 3 | battery resize @2.5 kWh/day → 7.5 kWh usable / ≈9.6 kWh nameplate | none | n/a |
| C7 | 1 | break-even array @3.0 kWh/day = 727 W | none | n/a |
| C7 | 2 | with margin → ≈875-900 W STC | none | n/a |
| C7 | 3 | battery resize @3.0 kWh/day → 9.0 kWh usable / ≈11.5-12 kWh nameplate | none | n/a |

All four newly surfaced assumptions (A-10, A-11, A-12, A-13) have been added to the Assumptions Table (Section 2) below, each marked inline with `[Assumes: X]` at its originating chain step in Section 4.

## Adversarial pass (process output)

**Recompute.** Independently redone: 170.36÷31=5.4955→5.50 h/day ✓. 1500÷(5.50×0.75)=1500÷4.125=363.6 W ✓. 363.6×1.2=436.4→≈450 W ✓. 1.5×3=4.5 kWh ✓; 4.5÷0.80=5.625 kWh ✓. 450×5.50×0.75=1,856.25 Wh; 1,856.25−1,500=356.25 Wh=23.75%≈24% ✓. 450÷48=9.375 A; 9.375÷120=0.078125C≈C/12.8 ✓. Sensitivity resizes: 2,500÷4.125=606.1 W, ×1.2=727.3 W ✓; 2.5×3=7.5 kWh, ÷0.80=9.375 kWh ✓. 3,000÷4.125=727.3 W, ×1.2=872.7 W ✓; 3.0×3=9.0 kWh, ÷0.80=11.25 kWh ✓. No figure recomputes to a different value than stated in Section 4; no scaled figure lands below its base.

**Sensitivity.** The single ground truth whose falsity would most flip the conclusion is GT-3 (December in-plane irradiation at 50° tilt, 5.50 h/day). It is not `?`-marked — it was read at source from PVGIS — but it is a long-term TMY-type model estimate for a nearby reference coordinate, not a site-specific measurement; a real parcel with worse local microclimate, elevation, or partial shading could run below it. This residual is the weakest link on C1 and every chain that cites it (C4, C6, C7): the mitigation is a site-specific PVGIS/NREL run at the exact parcel coordinates plus a on-site shading assessment before final purchase, not a change to the arithmetic.

**Rival.** Headline rival: sizing the array to the *annual average* PSH (6.35 h/day at 50° tilt) instead of the December worst month, which would yield only ≈315 W — this rival is ruled out in Section 5 ("Dead End: annual-average array sizing") by GT-2/GT-3's seasonal spread and the Essence Statement's year-round-occupancy requirement. Intermediate-chain rival: sizing the battery bank at 100% DoD instead of 80% (nameplate 4.5 kWh instead of 5.625 kWh) — ruled out in Section 5 ("Dead End: 100%-DoD battery sizing") on remote-replacement-logistics and cycle-life grounds, not left live. No other chain in Section 4 has a live, unsettled rival.

**Premise** *(pre-mortem, applied because the conclusion is a plan/recommendation — see inversion-vs-pre-mortem decision rule)*: It is now three winters after installation, mid-January, and the cabin has gone dark — the battery is depleted and the household has no power despite having followed this design.

**Causes** *(generated from three stakeholder viewpoints — the occupant, the installer/designer, and a skeptical off-grid-feasibility critic — unfiltered)*:
1. Occupant added a second refrigerator/freezer, a space heater, or power tools without recalculating the load budget (load creep).
2. Occupant ran through an unusually long cloudy or wildfire-smoke-haze stretch that lasted materially longer than 3 days.
3. Occupant repeatedly let the battery sit at low state-of-charge without periodic full recharge, accelerating LiFePO4 capacity fade beyond the assumed mid-life aging derate.
4. Installer mounted the array at the wrong tilt or an off-south azimuth, silently cutting December output below the 5.50 h/day design basis (GT-3's assumption of true-south, unobstructed siting — A-11 — not actually holding).
5. Installer chose a charge controller undersized for cold-weather open-circuit-voltage rise, causing controller shutdown/fault on cold, clear December mornings.
6. Critic's concern: panels were dust-covered or partly snow-covered for days with no rain/wind to self-clean, invalidating the assumed soiling/snow derate component inside GT-5.
7. Critic's concern: the LiFePO4 BMS enforced a low-temperature charge lockout (most LiFePO4 packs cannot be charged below ~0°C/32°F) on cold winter mornings, blocking charging during exactly the hours the design counted on — an effect not modeled anywhere in GT-5's derate build-up.

**Clusters:**
- **Load creep** (cause 1) — bears on GT-7, C5, C6, C7.
- **Solar-resource shortfall beyond the design basis** (causes 2, 4, 6) — bears on GT-3, GT-11, C1, C4.
- **Cold-weather electrical quirks not modeled in the derate** (cause 5, 7) — bears on GT-5, C1.
- **Battery mismanagement / faster-than-assumed degradation** (cause 3) — bears on GT-4, C2.

**Disposition:**
- Load creep: plan change — specify wiring and the MPPT charge controller to the higher 750-900 W tier (chain C7's sizing) even if fewer panels are installed initially, so the array can be cheaply expanded later; document the load-scaling table (chains C5-C7) prominently for the owner.
- Solar-resource shortfall: accepted risk with named mitigation — this design's basis is "average December plus short cloudy excursions bounded by the 3-day battery," not multi-week smoke/storm events; mitigation is a small propane or gasoline backup generator (1-2 kW) for tail events, and an on-site PVGIS/shading survey before final siting to close the GT-3 residual named under Sensitivity above.
- Cold-weather electrical quirks: plan change — specify a charge controller with low-temperature/cold-start compensation and a battery/BMS combination rated for low-temperature charge cutoff (with internal heating pad if the unit will see sub-freezing mornings), as an explicit component spec rather than only an energy-derate line item.
- Battery mismanagement: accepted risk with named mitigation — install a battery monitor (shunt-based state-of-charge tracking), keep the 80% DoD policy (not push to 100%) specifically to preserve cycle-life margin against real-world abuse, and schedule periodic full-charge cycles.

**Falsification.** This sizing recommendation is false (inadequate) if, under normal non-generator-assisted operation in a representative December, multi-year field data shows the battery state of charge trending toward zero — i.e., the battery is unable to fully recover between ordinary cloudy excursions across a typical winter, rather than only during the extreme tail events this design explicitly accepts as out of scope.

## §6→§4 closure ledger (process output)

- "Build the array to approximately 450 W STC ... battery bank to approximately 5.6-6.0 kWh nameplate ... 4.5 kWh usable at an 80% depth-of-discharge policy" → chain C1, chain C2 ✓
- "Array: approximately 450 W STC at 50° tilt, sized against the December worst-month solar resource with a 20% recharge margin" → chain C1 ✓
- "Battery: approximately 5.6-6.0 kWh nameplate and approximately 4.5 kWh usable, sized as 3 days of the 1.5 kWh/day design load at 80% DoD" → chain C2 ✓
- "The array's charge current into the battery bank works out to roughly C/13 ... confirming the battery is not the constraint on array size" → chain C3 ✓
- "The 3-day battery autonomy is not an independent sizing input — it is a backstop against short excursions below the December average" → chain C4 ✓
- "Tilting the array at 50° instead of true-latitude 35° buys about 9.6% more December output at a cost of only about 3% of annual harvest ... no plausible single-criterion re-weighting reverses the choice" → chain C1 ✓
- "if either is added, the realistic design point is 2.5-3.0 kWh/day and the array and battery scale up by roughly 60-100%" → chain C5, chain C6, chain C7 ✓
- "**Confidence:** MEDIUM — every contributing chain is capped at MEDIUM by unverified inputs ..." → chain C1, chain C2, chain C3, chain C4, chain C5 ✓

All §6 claims are inline-cited to a named §4 chain; no claim requires a cut.

## Self-audit scan (process output)

| Chain | Chain Head (brief) | Form conforming? | Rule applied | Dependency clean? | Band | Act attempted? | Edges fired |
|-------|---------------------|-------------------|---------------|--------------------|------|-----------------|-------------|
| C1 | GT-3, GT-7, GT-5?, GT-11? | yes | n/a | yes | MEDIUM | yes | none |
| C2 | GT-7, GT-8, GT-4? | yes | n/a | yes | MEDIUM | yes | none |
| C3 | C1 (MEDIUM), C2 (MEDIUM) | yes | n/a | yes | MEDIUM | no | none |
| C4 | C1 (MEDIUM), GT-7 | yes | n/a | yes | MEDIUM | no | none |
| C5 | GT-7, GT-10? | yes | n/a | yes | MEDIUM | no | none |
| C6 | GT-5?, GT-11?, C5 (MEDIUM) | yes | n/a | yes | MEDIUM | no | none |
| C7 | GT-5?, GT-11?, C5 (MEDIUM) | yes | n/a | yes | MEDIUM | no | none |

| §6 Span (brief) | Construct | Claim under R11? | R11 clause applied | Chain cited |
|-------------------|-----------|-------------------|----------------------|---------------|
| "Recommended approach: Build the array to approximately 450 W STC ... 80% DoD policy" | bold lead-in | yes | bold lead-in whose colon closes the bold span, content follows on same line | C1, C2 |
| "Array: approximately 450 W STC at 50° tilt ... 20% recharge margin" | list item | yes | closes its own sentence, >40 characters | C1 |
| "Battery: approximately 5.6-6.0 kWh nameplate ... 80% DoD" | list item | yes | closes its own sentence, >40 characters | C2 |
| "The array's charge current ... not the constraint on array size" | list item | yes | closes its own sentence, >40 characters | C3 |
| "Key insight: The 3-day battery autonomy is not an independent sizing input ..." | bold lead-in | yes | bold lead-in whose colon closes the bold span, content follows on same line | C4 |
| "Trade-offs acknowledged: Tilting the array at 50° ... 2.5-3.0 kWh/day and the array and battery scale up ..." | bold lead-in | yes | bold lead-in whose colon closes the bold span, content follows on same line | C1, C5, C6, C7 |
| "Pre-check: head C1 (MEDIUM), C2 (MEDIUM), C3 (MEDIUM), C4 (MEDIUM), C5 (MEDIUM), C6 (MEDIUM), C7 (MEDIUM) ..." | bold lead-in | yes | bold lead-in whose colon closes the bold span, content follows on same line (self-discharging: names its own cited chains) | C1, C2, C3, C4, C5, C6, C7 |
| "Confidence: MEDIUM — every contributing chain is capped at MEDIUM by unverified inputs ..." | bold lead-in | yes | bold lead-in whose colon closes the bold span, content follows on same line | C1, C2, C3, C4, C5 |

Scan complete: 7 chain rows, one per section-4 chain block in order; 8 section-6 rows, one per construct in order — 8 claims under R11, 0 excluded. 0 chains malformed, 0 claims untraced.

## Self-Audit Gate (process output)

**Criterion 1: Identify Essence**
Quoted span: "Core problem: Determine the minimum solar PV array rating (W, STC) and LiFePO4 battery bank capacity (usable and nameplate, kWh) that let a year-round, off-grid, 2-adult cabin at 35°N high-desert New Mexico survive its worst solar month plus a 3-day zero-sun autonomy event, given a load estimate that must itself be sanity-checked rather than taken as fixed."
Band: **Rigorous**
Justification: The statement names a property unique to this exact problem (35°N high-desert NM, LiFePO4, 3-day autonomy, a load figure that must be sanity-checked rather than taken as given) rather than a generic template phrase, and each of its six success criteria is a verb+subject+outcome triplet checkable directly against the Conclusion section without further interpretation.

**Criterion 2: Challenge Assumptions**
Quoted span (Assumption Audit scan): "All four newly surfaced assumptions (A-10, A-11, A-12, A-13) have been added to the Assumptions Table (Section 2) below, each marked inline with `[Assumes: X]` at its originating chain step in Section 4."
Band: **Rigorous**
Justification: The Assumption Audit scan is exhaustive over every named chain step (25 hop-rows across C1-C7), every surfaced assumption was added to the table rather than left implicit, and the Assumptions Table uses exactly the four-type scheme with multiple rows verdicted Challenge rather than a uniform Accept.

**Criterion 3: Establish Ground Truths**
Quoted span (Ground Truths provenance summary): "?-marked: GT-4, GT-5, GT-10, GT-11 (4 of 11)."
Band: **Rigorous**
Justification: Checked against the Ground Truths list, exactly GT-4, GT-5, GT-10 and GT-11 carry the `?` suffix and the enumeration matches; no unsuffixed GT feeds a HIGH-confidence chain (every chain in this analysis is MEDIUM), so the read-at-source-for-HIGH requirement is vacuously satisfied; and GT-4's entry carries a Phase 3 failure record ("source unreachable (404)") rather than a silently unmarked gap.

**Criterion 4: Reason Upward**
Quoted span (self-audit scan chain-form table and reconciliation line): "C1 | GT-3, GT-7, GT-5?, GT-11? | yes | n/a | yes | MEDIUM | yes | none" and "0 chains malformed, 0 claims untraced."
Band: **Rigorous**
Justification: All 7 chain-form rows read Form conforming = yes and Dependency clean = yes with 0 malformed chains per the reconciliation line; every surfaced assumption is declared inline with a literal `[Assumes: A-N]` token (e.g., on C1's first hop and C3's first two hops); and Section 5 documents four specific, non-generic dead ends (annual-average sizing, 100%-DoD sizing, trade-off-matrix scope, DC-native load crediting) rather than invoking the escape valve.

**Criterion 5: Validate**
Quoted span (Conclusion confidence line): "every contributing chain is capped at MEDIUM by unverified inputs: GT-5? ... and GT-11? ... cap C1, C4, C6, C7; GT-4? ... caps C2; GT-10? ... caps C5."
Band: **Rigorous**
Justification: Every chain and the Conclusion carry a Pre-check and Confidence line naming the specific `GT-N?` inputs and the verification that would remove each as a cause of the downgrade; no chain is rated above the lowest-rated chain its head cites (C3, C4, C6, C7 are each correctly capped at MEDIUM by the chains they cite); and the adversarial pass record is complete — Recompute, Sensitivity, Rival, Premise, Causes, Clusters (each naming GT/chain ids), Disposition (a named plan change or accepted risk with mitigation on every cluster), and Falsification are all present.

**Criterion 6: Conclusion-to-Ground-Truth Traceability**
Quoted span (self-audit scan claim-inventory reconciliation line): "8 claims under R11, 0 excluded ... 0 claims untraced."
Band: **Rigorous**
Justification: Every one of the 8 Section 6 claims cites a specific Section 4 chain id per the claim-inventory table; no new reasoning is introduced in Section 6 beyond what chains C1-C7 already established; and the Key Insight (autonomy is a backstop coupled to worst-month array sizing, not an independent requirement) is a distinct, non-obvious finding rather than a restatement of the Recommended approach's array/battery figures.

**Gate result:** No criterion scored Absent; 0 criteria scored Hand-wavy (≤1 required). Both clearing conditions are met — this analysis clears the Self-Audit Gate on the first pass, with no re-perception pass required.

---

## 1. Problem Essence

**Core problem:** Determine the minimum solar PV array rating (W, STC) and LiFePO4 battery bank capacity (usable and nameplate, kWh) that let a year-round, off-grid, 2-adult cabin at 35°N high-desert New Mexico survive its worst solar month plus a 3-day zero-sun autonomy event, given a load estimate that must itself be sanity-checked rather than taken as fixed.

**Success criteria:**
- A specific array rating in W (STC) is stated in the Conclusion, with arithmetic traceable to a named worst-month peak-sun-hour figure and a named total-derate factor.
- A specific battery bank size in kWh is stated in the Conclusion as both usable and nameplate capacity, traceable to load × autonomy ÷ depth-of-discharge.
- The Conclusion labels the 1.5 kWh/day starting load as realistic, low, or high against a component-level decomposition, and names what it implicitly assumes.
- The Conclusion's array sizing is driven by the worst month (December), not the annual average, with the fixed-tilt trade-off resolved by named numbers rather than convention.
- The Conclusion shows the battery autonomy requirement as coupled to, not independent of, the worst-month array sizing.
- The Conclusion states at least one alternate load scenario (2.5-3.0 kWh/day) with resized array/battery numbers, making the sensitivity of both headline figures to the load assumption visible.

---

## 2. Assumptions Table

| Assumption | Type | Treatment | Verdict | Verification |
|---|---|---|---|---|
| A-1: Daily electrical load design point = 1.5 kWh/day | current constraint | record expiry conditions | Challenge — internally consistent only if refrigeration is non-electric and there is no connectivity load; expires once electric refrigeration or internet is added (see chain C5) | unverified — flagged (rests on GT-10?) |
| A-2: Total off-grid system derate = 0.75 | untested belief | verify, or flag as unverified | Challenge — this analysis's own engineering build-up from eight named component factors, not read from one external source; bracketed 0.70-0.80 | unverified — flagged (GT-5?) |
| A-3: Desired autonomy = 3 days, zero solar input | current constraint | record expiry conditions | Accept — explicit user-specified design requirement; would expire only if the owner's risk tolerance or budget changes | source: user brief (GT-8), read-at-source |
| A-4: Battery depth-of-discharge design policy = 80% | convention | explicitly challenge before use | Accept — survives challenge against the live 100%-DoD rival on remote-replacement-logistics and cycle-life grounds (see Section 5) | unverified — flagged (GT-4?; specific manufacturer datasheet fetch attempt returned HTTP 404 this session) |
| A-5: Typical load-component breakdown (lighting, laptop/phone, pump, misc, fridge, connectivity) | untested belief | verify, or flag as unverified | Challenge — rough off-grid design-literature estimate, not tied to a specific appliance datasheet or site survey | unverified — flagged (GT-10?) |
| A-6: Fixed array tilt = 50° (latitude + 15°), true-south facing, no tracking | convention | explicitly challenge before use | Accept — challenged directly against 35° true-latitude tilt using PVGIS-read December/annual figures (GT-2 vs. GT-3) and a weighted trade-off with a robust flip test; 50° wins on the criterion the Essence Statement identifies as binding | source: PVGIS v5.2 API, read-at-source (GT-2, GT-3) |
| A-7: Array oversize margin for post-autonomy battery recovery = 1.2× break-even (bracket 1.1-1.3×) | convention | explicitly challenge before use | Challenge — standard off-grid design-practice convention, not read from one specific source this session | unverified — flagged (GT-11?) |
| A-8: All household loads are served as AC via the inverter (no separate low-voltage DC subsystem credited) | convention | explicitly challenge before use | Accept — conservative simplification; a native-DC lighting/USB subsystem would modestly improve the derate but was not modeled, so this errs toward oversizing rather than undersizing | unverified — flagged (rolled into GT-5?) |
| A-9: Albuquerque-area coordinates (35.08°N, 106.65°W) are representative of "35°N high-desert New Mexico" generally | convention | explicitly challenge before use | Accept — matches the stated 35°N latitude and high-desert climate class; a specific parcel's elevation or microclimate could still shift PSH by some percent | unverified — flagged |
| A-10: 48 V nominal battery bus architecture assumed for the array-to-battery charge-current check | convention | explicitly challenge before use | Accept — reasonable default for a bank in the 5-12 kWh range; the C-rate conclusion (battery not the binding constraint) is insensitive to the specific bus voltage chosen, since current and Ah both scale together | n/a — design-choice, not an empirical fact |
| A-11: Unobstructed, true-south-facing siting with no shading | convention | explicitly challenge before use | Accept — implicit in the PVGIS runs (azimuth = 0°, no shading model); a real parcel with tree or terrain shading needs this re-verified on site | unverified — flagged |
| A-12: No backup generator; occupants accept load-shedding risk for excursions beyond the design basis (average-December surplus plus the 3-day battery) | convention | explicitly challenge before use | Challenge — surfaced by the Phase 5 pre-mortem as a real tail-risk boundary of this design; accepted as a named risk with a stated mitigation (see Conclusion) rather than resolved by sizing alone | n/a — scope decision |
| A-13: LiFePO4 cells typically accept up to roughly 0.5-1C charge rate | untested belief | verify, or flag as unverified | Accept — general lithium-chemistry convention used only to confirm the battery is not the binding constraint; the computed ~C/13 array-to-battery ratio is far enough below even a conservative low-end 0.5C ceiling that the exact figure is not load-bearing | unverified — flagged |

---

## 3. Ground Truths

- **GT-1** Horizontal (0° tilt) solar resource at 35.08°N, 106.65°W (Albuquerque-area high desert, 1,687 m elevation): annual average 5.527 kWh/m²/day; December average 2.832 kWh/m²/day — source: NASA POWER climatology API (power.larc.nasa.gov/api/temporal/climatology/point), parameter `ALLSKY_SFC_SW_DWN`, community RE, 2001-2020 climatology; read-at-source: JSON response fields ANN = 5.5272, DEC = 2.832 kW-hr/m²/day, fetched this session.
- **GT-2** In-plane irradiation at the same coordinates, fixed 35° tilt (true-latitude), azimuth 0° (south): December = 155.56 kWh/m²/month → 5.02 kWh/m²/day (÷31); annual = 2,390.97 kWh/m²/year → 6.55 kWh/m²/day (÷365) — source: PVGIS v5.2 `PVcalc` API (re.jrc.ec.europa.eu), `angle=35, aspect=0`; read-at-source: JSON response `H(i)_m` monthly table, December value 155.56, annual `H(i)_y` 2,390.97, fetched this session.
- **GT-3** In-plane irradiation at the same coordinates, fixed 50° tilt (latitude + 15°), azimuth 0° (south): December = 170.36 kWh/m²/month → 5.50 kWh/m²/day (÷31); annual = 2,317.27 kWh/m²/year → 6.35 kWh/m²/day (÷365) — source: PVGIS v5.2 `PVcalc` API, `angle=50, aspect=0`; read-at-source: JSON response `H(i)_m` monthly table, December value 170.36, annual `H(i)_y` 2,317.27, fetched this session. Load-bearing for chains C1, C4, C6, C7.
- **GT-4?** LiFePO4 depth-of-discharge / cycle-life industry convention: manufacturers commonly rate LiFePO4 packs for roughly 3,000-6,000 cycles to 80% of original capacity at 80% DoD, with somewhat fewer cycles (often cited ~2,000-4,000) when routinely cycled to 100% DoD — unverified: a direct fetch of a specific manufacturer datasheet (Battle Born product page) returned HTTP 404 this session; no specific vendor spec was read. Phase 3 failure record: source unreachable (404, page not found).
- **GT-5?** Off-grid system total derate build-up = 0.75, from eight named loss factors multiplied together: PV nameplate/rating tolerance 0.98 × soiling/dust 0.97 × temperature 0.98 × DC wiring/connections 0.98 × MPPT charge-controller efficiency 0.97 × LiFePO4 round-trip efficiency 0.95 × inverter efficiency 0.94 × mid-life aging derate 0.95 ≈ 0.751 — unverified: this analysis's own engineering build-up from named component conventions, not read from one external source this session; bracketed 0.70 (pessimistic) to 0.80 (optimistic).
- **GT-6** December is the local-minimum-output month at both 35° and 50° tilt: at 35° tilt, December (155.56 kWh/m²) is lower than every other month (next-lowest is November at 179.71); at 50° tilt, December (170.36 kWh/m²) is lower than every other month (next-lowest is February at 182.37) — source: same PVGIS monthly tables as GT-2/GT-3; read-at-source: the full monthly tables already quoted under GT-2 and GT-3.
- **GT-7** Daily electrical load design point = 1.5 kWh/day — source: user-specified design brief; read-at-source: quoted directly from the task ("Rough daily electrical load estimate: ~1.5 kWh/day").
- **GT-8** Desired autonomy = 3 days at full load with zero solar input — source: user-specified design brief; read-at-source: quoted directly ("Desired autonomy: 3 days (i.e., battery bank must carry the load through 3 consecutive days with zero solar input)").
- **GT-9** Battery chemistry = LiFePO4; location = 35°N high-desert New Mexico; year-round occupancy by 2 adults; fully off-grid, no grid connection — source: user-specified design brief; read-at-source: quoted directly from the task's bullet list.
- **GT-10?** Typical year-round 2-adult off-grid cabin load components: baseline non-refrigeration, non-connectivity loads (LED lighting ~0.2 kWh/day, laptop/phone charging ~0.3 kWh/day, small water pump ~0.2 kWh/day, misc. electronics ~0.3 kWh/day) ≈ 1.0 kWh/day; a single efficient DC compressor refrigerator typically adds ~0.7-1.2 kWh/day; satellite internet (e.g., a low-earth-orbit terminal) typically adds ~0.6-1.5 kWh/day — unverified: general off-grid system-design literature figures, not tied to a specific fetched appliance datasheet or site survey this session.
- **GT-11?** Array oversize margin for post-autonomy battery recovery ≈ 1.1-1.3× the break-even array rating, central estimate 1.2× — unverified: standard off-grid design-practice convention, not read from one specific source this session; used so the array can both serve the load and recharge the battery after a below-average stretch, not merely break even on an average day.

**Provenance summary:** `?`-marked: GT-4, GT-5, GT-10, GT-11 (4 of 11). Read-at-source: GT-1 (NASA POWER API JSON, ANN/DEC fields), GT-2 (PVGIS API JSON, 35°-tilt `H(i)_m` table), GT-3 (PVGIS API JSON, 50°-tilt `H(i)_m` table — the chain-load-bearing figure), GT-6 (derived directly from GT-2/GT-3's already-quoted tables), GT-7, GT-8, GT-9 (quoted directly from the user's design brief). No unsuffixed ground truth in this analysis feeds a HIGH-confidence chain (every chain is rated MEDIUM), so the read-at-source-for-HIGH requirement does not additionally apply to any entry.

---

## 4. Derivation Chains

### Tilt-angle trade-off (feeds chain C1)

Two viable fixed-tilt options survive Phase 3: true-latitude tilt (35°) and a winter-biased tilt (50°, latitude + 15°). A third option (a shallow, summer-optimized tilt near 20°) is knocked out by inspection: solar geometry means a fixed surface tilted below latitude moves monotonically toward horizontal, and GT-1's horizontal December figure (2.832 kWh/m²/day) is already only 56% of GT-2's 35°-tilt December figure — a lower tilt only worsens the binding December constraint, so it fails the implicit must-have that December output must not be sacrificed further.

Weighted comparison of the two live options (criteria and weights locked before scoring):

| Criterion (higher score = better) | Weight | 35° tilt | 50° tilt |
|---|---|---|---|
| December (worst-month) output — the binding constraint per the Essence Statement | 5 | 3 (5.02 h/day) | 4 (5.50 h/day) |
| Annual total harvest (affects future load-growth headroom) | 2 | 4 (6.55 h/day) | 3 (6.35 h/day) |
| Installation practicality (standard adjustable racking either way) | 1 | 4 | 4 |
| **Weighted total** | | **27** | **30** |

50° tilt wins, 30 to 27. Flip test: December's weight would have to drop from 5 to below 2 (a cut of more than half) before annual harvest's smaller edge could outweigh it — an implausible re-weighting given the Essence Statement itself identifies worst-month output as the binding design constraint, so this is a robust result, not a near-tie. This resolves assumption A-6 and selects GT-3 (50° tilt) over GT-2 (35° tilt) as the array-sizing input for chain C1.

### Conclusion C1: Recommended array rating, base-case load (1.5 kWh/day)

GT-3 (PVGIS 50°-tilt Dec/annual irradiance) + GT-7 (1.5 kWh/day design load) + GT-5? (0.75 total system derate) + GT-11? (1.2× recharge margin)
→ December is the lowest-output month at 50° tilt per GT-3 and GT-6, so it is the binding design month for a year-round load [Assumes: A-11]
→ the December worst-month peak-sun-hours at 50° tilt is 170.36 kWh/m² ÷ 31 days = 5.50 h/day
→ the break-even array rating is daily load ÷ (worst-month PSH × total derate) = 1,500 Wh ÷ (5.50 h × 0.75) = 364 W
→ applying the 1.2× recharge-margin for post-autonomy battery recovery gives a design array rating of 364 W × 1.2 = 436 W
→ rounding to commercially available module sizes yields a recommended array of approximately 450 W STC

**Pre-check:** head GT-3, GT-7, GT-5?, GT-11? · ?-marked: GT-5, GT-11 · lowest cited: none · Inputs ceiling: MEDIUM
**Confidence:** MEDIUM — GT-5? (the 0.75 derate build-up) is unverified; it would be confirmed by post-install measured system performance against the modeled 0.70-0.80 bracket. GT-11? (the 1.2× margin) is unverified; it would be confirmed against a named off-grid design manual, or by observing whether the battery actually recovers full charge within a normal clear spell after a 3-day autonomy event. GT-3 itself is read-at-source and not `?`-marked, but per the Sensitivity analysis in the adversarial pass it is a nearby-coordinate model estimate rather than a site measurement, which is why this chain still carries a siting-residual caveat even though GT-3's own suffix is clean.

### Conclusion C2: Recommended battery bank size, base-case load (1.5 kWh/day)

GT-7 (1.5 kWh/day design load) + GT-8 (3-day autonomy) + GT-4? (80% DoD design policy)
→ usable capacity required to carry the load through 3 sunless days is daily load × autonomy days = 1.5 kWh × 3 = 4.5 kWh usable
→ at an 80% depth-of-discharge policy chosen for LiFePO4 cycle-life longevity, nameplate capacity = usable ÷ DoD = 4.5 kWh ÷ 0.80 = 5.625 kWh
→ rounding to a practical commercial module size yields a recommended nameplate bank of approximately 5.6-6.0 kWh, delivering about 4.5 kWh usable

**Pre-check:** head GT-7, GT-8, GT-4? · ?-marked: GT-4 · lowest cited: none · Inputs ceiling: MEDIUM
**Confidence:** MEDIUM — GT-4? (the 80% DoD / cycle-life convention) is unverified against a specific manufacturer datasheet; it would be confirmed by pulling the cycle-life spec of the actual battery product purchased. The competing 100%-DoD rival is ruled out in Section 5, not left live.

### Conclusion C3: The battery's charge-acceptance rate is not the binding constraint on array size

C1 (450 W array, MEDIUM) + C2 (5.76 kWh / 120 Ah nameplate bank @48 V, MEDIUM)
→ at a 48 V nominal bus a 450 W array delivers roughly 450 W ÷ 48 V = 9.4 A into the battery under bulk charge [Assumes: A-10]
→ against a 120 Ah (5.76 kWh) nameplate bank this is a charge rate of about 9.4 A ÷ 120 Ah = C/12.8, far below LiFePO4's typical 0.5C-1C maximum charge acceptance [Assumes: A-13]
→ therefore the battery's charge-acceptance rate is not the binding constraint on array size; the December solar resource and the daily load are what size the array

**Pre-check:** head C1 (MEDIUM), C2 (MEDIUM) · ?-marked: none · lowest cited: MEDIUM · Inputs ceiling: MEDIUM
**Confidence:** MEDIUM — capped by citing C1 and C2, both MEDIUM (see their own confidence lines for the underlying GT-5?, GT-11?, GT-4? causes). A-10 (48 V bus) and A-13 (LiFePO4 max charge rate) are accepted design/chemistry conventions rather than load-bearing uncertainties: the computed C/12.8 ratio is far enough below even a conservative low-end 0.5C ceiling that neither assumption's exact value changes the conclusion.

### Conclusion C4: Battery autonomy is a backstop coupled to worst-month array sizing, not an independent requirement

C1 (450 W array, MEDIUM) + GT-7 (1.5 kWh/day load)
→ on an average December day the 450 W array delivers 450 W × 5.50 h × 0.75 = 1,856 Wh
→ this exceeds the 1,500 Wh daily load by 356 Wh, about a 24% surplus
→ that surplus is what lets the battery recover charge after being drawn down during a multi-day cloudy stretch, which is exactly the scenario the 3-day autonomy battery exists to survive [Assumes: A-12]
→ therefore the battery autonomy and the worst-month array sizing are coupled, not independent: the battery is a backstop against short excursions below the December average, not a capacity requirement computed against a separate solar assumption

**Pre-check:** head C1 (MEDIUM), GT-7 · ?-marked: none · lowest cited: MEDIUM · Inputs ceiling: MEDIUM
**Confidence:** MEDIUM — capped by citing C1 (MEDIUM); see C1's confidence line for the underlying GT-5?/GT-11? causes. A-12 (no backup generator; excursions beyond the 356 Wh/day surplus plus 3-day battery are accepted risk) is named and priced in the Section 5 pre-mortem disposition, not left as an unpriced gap.

### Conclusion C5: The 1.5 kWh/day starting load is realistic only under a restrictive, non-default set of implicit assumptions

GT-7 (1.5 kWh/day design load) + GT-10? (typical off-grid load-component estimate)
→ decomposing typical year-round 2-adult cabin loads — LED lighting ~0.2 kWh/day, laptop/phone charging ~0.3 kWh/day, a small water pump ~0.2 kWh/day, miscellaneous electronics ~0.3 kWh/day — totals roughly 1.0 kWh/day before refrigeration or connectivity
→ adding a single efficient DC compressor refrigerator, a near-universal want for year-round occupancy, typically adds another 0.7-1.2 kWh/day on its own
→ therefore the stated 1.5 kWh/day design point is internally consistent only if refrigeration is non-electric (propane or ice-box) and there is no satellite or other internet connectivity load, which is a specific and fairly restrictive implicit assumption for a year-round-occupied cabin
→ a more typical year-round electrified load profile, adding an electric fridge and modest connectivity, lands in the 2.5-3.0 kWh/day range, which chains C6 and C7 resize the system against

**Pre-check:** head GT-7, GT-10? · ?-marked: GT-10 · lowest cited: none · Inputs ceiling: MEDIUM
**Confidence:** MEDIUM — GT-10? (the load-component estimate) is unverified against a specific site survey or appliance datasheet; it would be confirmed by an actual appliance inventory and manufacturer wattage specs for the fridge and any connectivity hardware the owner intends to install.

### Conclusion C6: Recommended array and battery resize at 2.5 kWh/day

GT-5? (0.75 derate) + GT-11? (1.2× margin) + C5 (2.5 kWh/day scenario, MEDIUM)
→ repeating the C1 arithmetic at 2.5 kWh/day gives a break-even array of 2,500 Wh ÷ (5.50 h × 0.75) = 606 W
→ applying the same 1.2× recharge margin gives 606 W × 1.2 = 727 W, rounding to approximately 730-750 W STC
→ repeating the C2 arithmetic gives usable capacity 2.5 kWh × 3 = 7.5 kWh and nameplate 7.5 ÷ 0.80 = 9.375 kWh, rounding to approximately 9.6 kWh nameplate

**Pre-check:** head GT-5?, GT-11?, C5 (MEDIUM) · ?-marked: GT-5, GT-11 · lowest cited: MEDIUM · Inputs ceiling: MEDIUM
**Confidence:** MEDIUM — GT-5? and GT-11? carry the same unverified status and closing verification path named under C1; citing C5 (MEDIUM) caps this chain at MEDIUM regardless.

### Conclusion C7: Recommended array and battery resize at 3.0 kWh/day

GT-5? (0.75 derate) + GT-11? (1.2× margin) + C5 (3.0 kWh/day scenario, MEDIUM)
→ repeating the C1 arithmetic at 3.0 kWh/day gives a break-even array of 3,000 Wh ÷ (5.50 h × 0.75) = 727 W
→ applying the same 1.2× recharge margin gives 727 W × 1.2 = 873 W, rounding to approximately 875-900 W STC
→ repeating the C2 arithmetic gives usable capacity 3.0 kWh × 3 = 9.0 kWh and nameplate 9.0 ÷ 0.80 = 11.25 kWh, rounding to approximately 11.5-12 kWh nameplate

**Pre-check:** head GT-5?, GT-11?, C5 (MEDIUM) · ?-marked: GT-5, GT-11 · lowest cited: MEDIUM · Inputs ceiling: MEDIUM
**Confidence:** MEDIUM — same basis as C6: GT-5? and GT-11? are unverified with the verification path named under C1, and citing C5 (MEDIUM) caps this chain regardless.

### Second-order effects (extends C1/C4; required Phase 4 pass)

**Actor lens.** The occupants will change behavior once the system is in place: they will load-shed (turn off nonessential loads) during real cloudy stretches, and — per the Section 5 pre-mortem — may add appliances (a second fridge, a space heater, a well pump) without recomputing the load budget, silently invalidating GT-7. An installer's siting and component choices (azimuth, charge-controller cold-weather rating) directly determine whether GT-3's modeled December output is actually realized on site. A future owner considering resale will see the load-scaling table (C5-C7) as a limitation unless the wiring and controller headroom recommended in the pre-mortem disposition is already in place.

**Time lens.** Immediately after commissioning, the system meets the 1.5 kWh/day design load with the ~24% December margin computed in C4. After a few years, LiFePO4 capacity fade (commonly cited around 2-3%/year at moderate cycling) and PV module degradation (commonly cited around 0.5%/year) erode that margin — GT-5?'s "mid-life aging" factor (0.95) is a first attempt to price this in, but it is itself unverified. Over a decade or more, a run of unusually smoky or stormy Decembers (a real and possibly increasing risk in the Southwest) could push actual December output below the modeled TMY-type average for a full season, a tail risk the 3-day battery does not cover — this is exactly the "solar-resource shortfall beyond the design basis" cluster the Section 5 pre-mortem names and prices with a generator-backup mitigation.

No extension step contradicts a named ground truth; both effects are carried into the Section 5 pre-mortem clusters and dispositions rather than requiring a return to Phase 2.

---

## 5. Abandoned Reasoning

### Dead End: Annual-average array sizing

**What was tried:** Sizing the array against the annual-average peak-sun-hours (6.35 h/day at 50° tilt) instead of the December worst month, since it would allow a smaller, cheaper array (≈315 W).

**Why abandoned:** Contradicts the Essence Statement's year-round-occupancy requirement. GT-2/GT-3's seasonal spread shows December output at 50° tilt (5.50 h/day) is only about 87% of the annual average, so an annual-average-sized array would run at a deficit for roughly the entire winter half of the year, not just occasional cloudy days — the classic off-grid under-sizing mistake the Essence Statement explicitly rules out.

**What it ruled out:** Any future revision of this design that tries to shrink the array by citing "the annual average PSH is higher" without re-opening the year-round-occupancy requirement.

### Dead End: 100%-DoD battery sizing

**What was tried:** Sizing the LiFePO4 bank at 100% DoD instead of 80%, needing only 4.5 kWh nameplate instead of 5.625 kWh — a smaller, cheaper bank.

**Why abandoned:** 80% DoD was retained instead because the cabin is a remote, primary, year-round residence where battery replacement is logistically costly (no easy resupply), and the cycle-life gain from staying off 100% DoD is a standard longevity trade most LiFePO4 manufacturers document. This reasoning, not a contradicted ground truth, is what settles the choice — the 100% option remains technically workable, just a different, lower-longevity design point.

**What it ruled out:** Treating chain C2's nameplate figure as arbitrary — it is the deliberate result of a stated longevity-vs-cost trade, not an unexamined default.

### Dead End: Full multi-criteria trade-off matrix for the tilt decision

**What was tried:** Considering a full 5-8 criterion weighted trade-off procedure for the 35°-vs-50° tilt choice, matching the general trade-off procedure's usual criterion count.

**Why abandoned:** The decision has only two live options and one criterion (December output) that dominates by an order of magnitude in stakes, per the Essence Statement. Adding more criteria to reach a "standard" count would have manufactured false precision without changing the outcome — the flip test on the lighter two-criterion-plus-practicality table already shows the result is robust to large weight changes.

**What it ruled out:** Any suggestion that the tilt recommendation is under-examined for lacking a full-size matrix; the flip test demonstrates the same robustness a larger matrix would.

### Dead End: Crediting native-DC (non-inverter) loads to reduce the derate

**What was tried:** Exploring whether treating some loads (LED lighting, USB charging) as native 12V/24V DC — bypassing inverter losses — would justify a lower total derate than 0.75.

**Why abandoned:** The load profile provided was not broken into AC-specific and DC-specific circuits, so crediting this without a real circuit plan would be speculative; the 0.75 derate's inverter-loss component (0.94) was kept as a conservative, uniform assumption instead (A-8).

**What it ruled out:** Silently shrinking the array below 450 W on an unexamined DC-native-loads assumption. If the owner commits to a DC-native lighting/USB subsystem at detailed design time, this is a legitimate place to claw back some margin, but it is not assumed here.

---

## 6. Conclusion

**Recommended approach:** Build the array to approximately 450 W STC, fixed-mounted at 50° tilt (latitude + 15°) facing true south, and size the LiFePO4 battery bank to approximately 5.6-6.0 kWh nameplate, delivering about 4.5 kWh usable at an 80% depth-of-discharge policy (chain C1, chain C2).

- Array: approximately 450 W STC at 50° tilt, sized against the December worst-month solar resource with a 20% recharge margin (chain C1).
- Battery: approximately 5.6-6.0 kWh nameplate and approximately 4.5 kWh usable, sized as 3 days of the 1.5 kWh/day design load at 80% DoD (chain C2).
- The array's charge current into the battery bank works out to roughly C/13, far below LiFePO4's typical charge-rate ceiling, confirming the battery is not the constraint on array size (chain C3).

**Key insight:** The 3-day battery autonomy is not an independent sizing input — it is a backstop against short excursions below the December average that the worst-month-sized array is already engineered to recover from, since that array produces about 24% more energy than the daily load on an average December day (chain C4).

**Trade-offs acknowledged:** Tilting the array at 50° instead of true-latitude 35° buys about 9.6% more December output at a cost of only about 3% of annual harvest, a trade this design accepts because an off-grid system cannot export unusable summer surplus and no plausible single-criterion re-weighting reverses the choice (chain C1). The headline numbers also depend on the starting 1.5 kWh/day load holding, which requires giving up electric refrigeration and home connectivity that most year-round occupants ultimately want; if either is added, the realistic design point is 2.5-3.0 kWh/day and the array and battery scale up by roughly 60-100% (chain C5, chain C6, chain C7).

**Pre-check:** head C1 (MEDIUM), C2 (MEDIUM), C3 (MEDIUM), C4 (MEDIUM), C5 (MEDIUM), C6 (MEDIUM), C7 (MEDIUM) · ?-marked: none · lowest cited: MEDIUM · Inputs ceiling: MEDIUM
**Confidence:** MEDIUM — every contributing chain is capped at MEDIUM by unverified inputs: GT-5? (the 0.75 system-derate build-up) and GT-11? (the 1.2× recharge margin) cap C1, C4, C6, C7; GT-4? (the 80% DoD/cycle-life convention) caps C2; GT-10? (the load-component estimate) caps C5. Each would move toward HIGH with a specific follow-up: GT-5? and the GT-3 siting residual close with a site-specific PVGIS/NREL run at the exact parcel coordinates plus an on-site shading and soiling assessment and post-install measured performance; GT-4? closes by pulling the datasheet of the specific battery product purchased; GT-10?/GT-7 close by the owner committing, before purchase, to whether the cabin will run an electric refrigerator and/or satellite internet, which fixes the real daily load design point.
