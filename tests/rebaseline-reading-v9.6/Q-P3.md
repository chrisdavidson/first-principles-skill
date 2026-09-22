**Disclosures (process):** No re-entry edge fired. One Phase 3 source read failed: `energy.gov/energysaver/insulation` returned HTTP 404, and that page was dropped as a citation. The output template, validation rubric and pre-mortem procedure were each opened once. I did not open the trade-off procedure. The options are ranked by one quantity (dollars recovered against dollars spent), and C2 rules the windows out before any weighting is needed, so no multi-criteria choice survives.

**Short answer:** Don't replace the windows for energy savings. Do the attic this year, but first get a blower-door and infrared energy audit (booked now, done in October), and have air sealing and a 1948-specific attic inspection done before the insulation goes in.

---

## Assumption Audit scan (process output)

| Chain | Step | Step Text (brief) | Assumption surfaced? | Added to Table? |
|---|---|---|---|---|
| C1 | 1 | H = $1,640 × heating fraction ÷ coldest-4 share | A1, A2 (already present) | n/a |
| C1 | 2 | H bracket [$1,351, $1,991, $2,733] | none | n/a |
| C1 | 3 | L = 0.35H bracket [$473, $697, $957] | A3 (already present) | n/a |
| C2 | 1 | no window fix can save more than L | none | n/a |
| C2 | 2 | 10-year ceiling $9,570 / $10,970 escalated | A7 (already present) | n/a |
| C2 | 3 | ceiling covers at most 59% of $18,500 | none | n/a |
| C2 | 4 | windows cannot pay back within the stay | A8 (already present) | n/a |
| C3 | 1 | attic loss scales as 1/R | none | n/a |
| C3 | 2 | R-13 → R-49 leaves 26.5% | A5 (already present) | n/a |
| C3 | 3 | removes about 73.5% of attic conduction | none | n/a |
| C4 | 1 | S = a × 0.735 × L | A4 (already present) | n/a |
| C4 | 2 | 10-year break-even needs a ≥ 0.82 / 0.60 | none | n/a |
| C4 | 3 | 30-year break-even needs a ≥ 0.27 | A11 (already present) | n/a |
| C4 | 4 | conduction estimate a ≈ 0.3–0.5 | A15: areas ~1,000 / ~170 sq ft | yes |
| C4 | 5 | clears 30-year, not 10-year | none | n/a |
| C4 | 6 | decision turns on unmeasured a | none | n/a |
| C5 | 1 | only non-energy value remains | A9 (already present) | n/a |
| C5 | 2 | skip replacement unless non-energy need | none | n/a |
| C6 | 1 | audit measures a | A16: audit can measure the split before winter | yes |
| C6 | 2 | air sealing raises delivered saving | A17: air sealing adds saving beyond conduction | yes |
| C6 | 3 | insulate after audit + sealing | none | n/a |
| C6 | 4 [2nd] | colder deck condenses moisture | none (covered by A17) | n/a |
| C6 | 5 [2nd] | K&T wiring / vermiculite hazard | A12: 1948 attic may hold K&T or vermiculite | yes |
| C6 | 6 [3rd] | one pre-job inspection clears both | none | n/a |

## Adversarial pass (process output)

**Recompute.** 1,640×0.85/0.70 = 1,991; 1,640×0.70/0.85 = 1,351; 1,640×1.0/0.60 = 2,733. ×0.35 gives 697 / 473 / 957. 10×957 = 9,570, and 957×11.46 (the sum of 1.03^t for t = 0–9) = 10,967 ≈ 10,970. 10,970/18,500 = 0.593. 1−13/49 = 0.7347. 0.735×697 = 512; 420/512 = 0.820. 0.735×957 = 703; 420/703 = 0.597. 4,200/(30×512) = 0.273. Areas: 1,000/13 = 76.9 and 170×1.1 = 187, so a = 76.9/263.9 = 0.29; with 170×0.5 = 85, a = 76.9/161.9 = 0.48. All figures recompute.

**Sensitivity.** The flip ground truth for the attic decision is GT-5? (the 35% figure and its split, carried through A4). It is `?`-marked. It stays unverified here, and the plan's audit is the verification (caveat on C4 and C6). The window conclusion (C2) has no flip ground truth within any plausible range. It would need more than ~$1,850/yr lost through windows alone.

**Rival.** Strongest rival: "insulate the attic now, no audit." It is ruled out by C4 and recorded in §5 ("Dead End: Insulate unconditionally now"). The second rival, "do neither," is also in §5, ruled out by C4 and C6.

**Premise.** It is autumn 2027, and the attic plan has failed: the insulation went in and the bills barely moved, or the job caused damage.

**Causes.**
- *Homeowner:* the 35% was a sales figure, and most loss was through the rim joist and doors.
- *Homeowner:* the $410 bill included water heating and baseload, so heating was smaller than assumed.
- *Installer:* insulation was blown in without sealing top plates or bypasses, and the roof deck grew mold by year two.
- *Installer:* installed depth settled to about R-38, and nobody checked the depth markers.
- *Installer:* live knob-and-tube wiring was buried.
- *Installer:* vermiculite was disturbed, and an abatement bill followed.
- *Payer:* the audit slipped to January and the job missed the winter.
- *Payer:* energy prices fell or the house switched to a heat pump, shrinking savings.
- *Future buyer:* at resale in year 10, the buyer paid nothing for the insulation.
- *Household with children:* skipping the windows left lead-painted friction sashes shedding dust.

**Clusters.**
- K1, unmeasured baseline and split (bills composition, share a; bears on GT-4?, GT-5?, C1, C4): absorbs the sales figure, the bill composition and the price-drop causes.
- K2, hidden 1948 attic conditions (C6, A12): absorbs knob-and-tube, vermiculite and moisture.
- K3, execution quality (C3, A5, A17): absorbs under-delivered depth and missing air sealing.
- K4, window non-energy needs (C5, A9): absorbs lead-paint sashes.
- K5, timing and horizon (C6, GT-6?, A8): absorbs the slipped audit and resale non-capture.

**Disposition.**
- K1, plan change: book the audit now. Also pull 12 months of bills and subtract the summer baseline to isolate heating spend.
- K2, plan change: make a pre-job attic inspection for knob-and-tube and vermiculite a condition of the contract.
- K3, plan change: the contract names settled R-49 depth with depth rulers and an explicit air-sealing line item.
- K4, accepted risk, with mitigation: a lead-safe inspection of the window sashes, followed by targeted sash repair or storm windows if needed.
- K5, plan change: if the audit cannot happen before November, insulate anyway, since C4's 30-year threshold (a ≥ 0.27) is likely met. The accepted residual risk is resale non-capture.

**Falsification.** The window conclusion is false if measured window loss exceeds ~$1,850/yr, about two-thirds of even the high-bracket heating spend. The attic recommendation is false if the audit shows the attic's share a is below ~0.27.

## §6→§4 closure ledger (process output)

```text
- "Recommended approach: skip windows; audit, air-seal, inspect, then insulate attic" → chains C5, C6 ✓
- "Key insight: 35% caps total savings; windows fail on arithmetic; attic turns on share a" → chains C2, C4 ✓
- "Trade-offs acknowledged" → chains C5, C6 ✓
- "Pre-check" → chains C5, C6 ✓
- "Confidence: MEDIUM" → chains C5, C6 ✓
```

---

## 1. Problem Essence

**Core problem:** The question is which, if any, of two envelope upgrades recovers its cost in heating savings over a stay of at least 10 years. That depends on how the 35% loss is split between an R-13 attic and 14 windows of unknown type, and nobody has measured that split.

**Success criteria:**
- The Conclusion states a verdict on the windows that holds across the full bracket of annual heating spend.
- The Conclusion states a verdict on the attic that names the quantity it depends on and the threshold value of that quantity.
- The Conclusion names an action executable this year that resolves any quantity the attic verdict depends on.

## 2. Assumptions Table

| Assumption | Type | Treatment | Verdict | Verification |
|---|---|---|---|---|
| A1: 70–100% of the $410 bill is space heating | untested belief | verify or flag | Challenge — the bill may include water heating and baseload; bracketed at 0.70/0.85/1.0 | unverified — flagged; verify from summer bills |
| A2: the 4 coldest months are 60–85% of annual heating | untested belief | verify or flag | Challenge — depends on climate; bracketed | unverified — flagged |
| A3: 35% of heating energy leaves via attic + windows | untested belief | verify or flag | Challenge — source not named (audit? contractor?) | unverified — flagged; energy audit |
| A4: attic share a of that 35% | untested belief | verify or flag | Challenge — the load-bearing unknown for the attic | unverified — flagged; blower-door/IR audit |
| A5: existing attic performs at nominal R-13 | untested belief | verify or flag | Challenge — 1948 insulation is often settled or gapped; lower effective R raises savings | unverified — flagged |
| A6: conductive heat flow ∝ A·ΔT/R | physical law | accept as ground-truth candidate | Accept — definition of R-value | GT-1, read at source |
| A7: compare in undiscounted real dollars | convention | challenge before use | Challenge — survives: C2 also holds with 3%/yr escalation and no discounting, which is the most favourable case for the windows | arithmetic in C2 |
| A8: 10-year payback is the decision rule | convention | challenge before use | Challenge — insulation outlives the stay; C4 also tests a 30-year horizon | resale capture unverified |
| A9: windows' only value is energy | convention | challenge before use | Discard — lead paint, failed sashes, drafts, noise are real non-energy values (C5) | n/a |
| A10: $4,200 / $18,500 are current, complete quotes | current constraint | record expiry | Accept — expires at the quote validity date; scope (air sealing included?) unconfirmed | user-supplied |
| A11: blown insulation lasts ≥30 years | untested belief | verify or flag | Accept — used only for the lifetime threshold | unverified — flagged |
| A12: 1948 attic may hold knob-and-tube wiring or vermiculite | untested belief | verify or flag | Challenge — surfaced by audit; drives a pre-job inspection | unverified — flagged |
| A15: attic ~1,000 sq ft, windows ~170 sq ft, window U 0.5–1.1 | untested belief | verify or flag | Challenge — used only to bracket a | unverified — flagged |
| A16: an audit can measure the split before winter | untested belief | verify or flag | Accept — priced in C6 (fallback stated) | unverified — flagged |
| A17: attic air sealing adds saving beyond conduction | untested belief | verify or flag | Accept — endpoint does not depend on it | unverified — flagged |
| A18: federal 25C insulation credit still available | untested belief | verify or flag | Discard — not used; I believe it ended for installs after 2025, unverified | unverified — not used in any chain |

## 3. Ground Truths

- **GT-1** Heat flow through a barrier = ΔT × A ÷ R, and U = 1/R. Source: Wikipedia, "R-value (insulation)"; read-at-source (raw wikitext, line 69): "The temperature difference divided by the R-value and then multiplied by the exposed surface area of the barrier gives the total rate of heat flow through the barrier." Line 236: "U is the inverse of R."
- **GT-2?** The attic is currently R-13, and the quote is $4,200 for blown-in R-49. Unverified: user-supplied; quote not seen.
- **GT-3?** The quote is $18,500 for triple-pane replacement of all 14 windows. Unverified: user-supplied.
- **GT-4?** The winter bill averages $410/month over the 4 coldest months ($1,640). Unverified: user-supplied; bills not seen.
- **GT-5?** About 35% of heating energy is lost through the attic and windows combined, split unknown. Unverified: the figure's source is not named.
- **GT-6?** The household plans to stay at least 10 more years. Unverified: stated intent.
- **GT-7?** The existing window type (single-pane, with or without storms, or later double-pane) is unknown. Unverified: not stated.

Phase 3 failure record: `energy.gov/energysaver/insulation`, HTTP 404. It was not used as a citation.

```text
?-marked: GT-2, GT-3, GT-4, GT-5, GT-6, GT-7 (6 of 7)
Read-at-source: GT-1 — Wikipedia "R-value (insulation)" wikitext lines 69 and 236, quoted above
```

No chain is rated HIGH, so no read location is required for a HIGH chain. GT-1's read location is given anyway.

## 4. Derivation Chains

### Conclusion C1: Attic plus windows cost about $700/yr (bracket $473–$957)

GT-4? ($1,640 over 4 coldest months) + GT-5? (35% via attic and windows)
→ annual heating spend H equals $1,640 × heating fraction ÷ coldest-4-month share [Assumes: A1, A2]
→ H brackets at [$1,351, $1,991, $2,733] per year
→ the combined attic-plus-window loss L = 0.35H brackets at [$473, $697, $957] per year

**Pre-check:** head GT-4?, GT-5? · ?-marked: GT-4?, GT-5? · lowest cited: none · Inputs ceiling: MEDIUM
**Confidence:** MEDIUM — the Inputs axis is short on GT-4? and GT-5?. Twelve months of bills (subtracting the summer baseline) would verify GT-4?, and an energy audit would verify GT-5?. A1 and A2 are priced by the bracket itself, so the Inference axis is clean. This is an estimate, not a contested endpoint, so the Rivals axis does not apply.

### Conclusion C2: No window upgrade can pay back in energy within 10 years

C1 (L ≤ $957/yr) + GT-3? ($18,500 windows)
→ no window upgrade can save more than L, since L is the entire attic-plus-window loss
→ the 10-year recovery ceiling is 10 × $957 = $9,570, or $10,970 with 3%/yr price escalation
→ that ceiling covers at most 59% of the $18,500 cost, even assuming zero attic loss and perfect windows
→ triple-pane replacement cannot repay itself in energy within the 10-year stay

**Pre-check:** head C1 (MEDIUM), GT-3? · ?-marked: GT-3? · lowest cited: MEDIUM · Inputs ceiling: MEDIUM
**Confidence:** MEDIUM — the Inputs axis is short: C1 is rated MEDIUM, and GT-3? is removed by seeing the written quote. Every hop is deduction or recomputed arithmetic taken at the most favourable extreme. The endpoint is a ruling-out, so the Rivals axis is answered.

### Conclusion C3: R-13 to R-49 removes about 73.5% of attic conduction

GT-1 (heat flow = ΔT·A/R) + GT-2? (R-13 now, R-49 quoted)
→ at fixed attic area and indoor-outdoor ΔT, attic conductive loss scales as 1/R
→ moving from R-13 to R-49 leaves 13/49 = 26.5% of that loss [Assumes: A5]
→ the attic upgrade removes about 73.5% of the heat now conducted through the attic

**Pre-check:** head GT-1, GT-2? · ?-marked: GT-2? · lowest cited: none · Inputs ceiling: MEDIUM
**Confidence:** MEDIUM — the Inputs axis is short on GT-2?, which is removed by measuring existing depth and type and reading the quote. A5 is priced: if the existing effective R is below 13, the removed fraction rises above 73.5%, so the endpoint is a conservative estimate and does not collapse. No rival applies.

### Conclusion C4: The attic's payback turns on the unmeasured share a

C1 (L bracket) + C3 (73.5% removal) + GT-7? (window type unknown)
→ the attic saving S equals a × 0.735 × L, where a is the attic's share of L [Assumes: A4]
→ 10-year break-even needs S ≥ $420/yr, so a ≥ 0.82 at central L and a ≥ 0.60 at high L
→ break-even over a 30-year insulation life needs only a ≥ 0.27 at central L [Assumes: A11]
→ a conduction estimate with window U of 0.5–1.1 puts a at roughly 0.3–0.5 [Assumes: A15]
→ at a = 0.3–0.5 the attic job clears the 30-year threshold but not the 10-year one
→ the attic decision turns on the unmeasured share a, which the current data cannot fix

**Pre-check:** head C1 (MEDIUM), C3 (MEDIUM), GT-7? · ?-marked: GT-7? · lowest cited: MEDIUM · Inputs ceiling: MEDIUM
**Confidence:** MEDIUM — the Inputs axis is short: C1 and C3 are rated MEDIUM, and GT-7? is removed by identifying the window glazing. The weakest link is the A15 area and U estimate. If it is wrong, a shifts, and that is exactly what the endpoint says is undetermined, so the endpoint stands. An A11 failure (shorter insulation life) only raises the lifetime threshold, and the endpoint's dependence on a is unchanged.

### Conclusion C5: Skip window replacement this year unless there is a non-energy need

C2 (no 10-year energy payback)
→ the only remaining case for the windows is non-energy value such as lead-painted sashes, failed frames, drafts or noise [Assumes: A9]
→ skip triple-pane replacement this year unless one of those non-energy needs is present

**Pre-check:** head C2 (MEDIUM) · ?-marked: none · lowest cited: MEDIUM · Inputs ceiling: MEDIUM
**Confidence:** MEDIUM — the Inputs axis is short: C2 is rated MEDIUM. A9 was discarded as a premise, and its negation is what this chain uses, so it is priced. The rival "replace windows because most loss is through them" is ruled out by C2 (§5).

### Conclusion C6: Audit, air-seal and inspect, then insulate the attic this year

C4 (a decides) + GT-6? (at least 10-year stay)
→ a blower-door and infrared audit measures a, the one quantity that flips the attic decision [Assumes: A16]
→ attic air sealing done with the insulation raises the delivered saving above C3's conduction-only figure [Assumes: A17]
→ insulate the attic this year, after the audit confirms a above about 0.3 and after air sealing
→[2nd] a colder attic deck condenses house moisture unless bypasses are sealed and ventilation checked
→[2nd] blown insulation over live knob-and-tube wiring, or disturbed vermiculite, is a fire or asbestos hazard in a 1948 attic [Assumes: A12]
→[3rd] one pre-job attic inspection clears both hazards, so the plan gains a pre-check rather than changing direction

**Pre-check:** head C4 (MEDIUM), GT-6? · ?-marked: GT-6? · lowest cited: MEDIUM · Inputs ceiling: MEDIUM
**Confidence:** MEDIUM — the Inputs axis is short: C4 is rated MEDIUM. GT-6? is confirmed only by the household's own plans, and a shorter stay favours the 30-year threshold less. A16 is priced: if the audit cannot isolate a before November, the fallback is to insulate anyway, because C4's lifetime threshold (a ≥ 0.27) is likely met, so the direction is unchanged. A17 is priced: if air sealing adds nothing, the saving is C3's figure and the endpoint is unchanged. The rivals are ruled out in §5. No second-order effect contradicts a ground truth.

## 5. Abandoned Reasoning

### Dead End: Replace the windows because they probably lose more heat than the attic

**What was tried:** A conduction estimate (A15) suggests single-pane windows could carry 50–70% of L, so the windows seemed to be the bigger target.

**Why abandoned:** C2 shows that even if 100% of the top-bracket L went through the windows and the new windows stopped all of it, 10 years recovers at most $10,970 against $18,500. The window share cannot rescue the economics.

**What it ruled out:** Any window decision justified on energy payback. If window heat loss is the worry, cheaper options such as storm windows or weatherstripping need their own quotes (costs unverified).

### Dead End: Insulate unconditionally now, without an audit

**What was tried:** Commit the $4,200 immediately, because insulation is cheaper per unit of loss removed.

**Why abandoned:** C4 shows 10-year break-even needs a ≥ 0.82 at central L, while the conduction estimate puts a at 0.3–0.5. Committing blind bets $4,200 on the one quantity nobody has measured, when an audit costs a small fraction of that and fits before winter.

**What it ruled out:** Treating the attic as a guaranteed win. It is likely positive only over the insulation's life, not within the stay.

### Dead End: Do neither

**What was tried:** Since neither upgrade clearly pays back within 10 years at central estimates, spend nothing.

**Why abandoned:** C4 shows the attic clears its 30-year threshold across the whole estimated range of a. C6 makes the attic spending conditional on measuring a, which captures "neither" as the outcome if a comes back below ~0.27.

**What it ruled out:** A blanket "neither." It survives only as the audit-negative branch of C6.

### Dead End: Weighted trade-off matrix across the four options

**What was tried:** Scoring {insulation, windows, both, neither} on weighted criteria.

**Why abandoned:** C2 removes "windows" and "both" on arithmetic, and the attic-versus-neither question is decided by one measurable quantity (C4), not by weighting criteria.

**What it ruled out:** Treating a measurement problem as a preference problem.

## 6. Conclusion

**Recommended approach:** Don't replace the windows this year unless lead-painted sashes, failed frames or drafts give a non-energy reason. Book a blower-door and infrared energy audit now. Have the attic air-sealed and inspected for knob-and-tube wiring and vermiculite. Then blow in the R-49 before December, provided the audit shows the attic carries more than roughly 0.3 of the loss (chains C5, C6).

**Key insight:** The 35% figure is a ceiling on what any fix can save, about $700/yr and at most ~$957/yr. That rules out the $18,500 windows on arithmetic alone, before anyone knows the attic/window split. The same arithmetic shows the attic's 10-year payback is not guaranteed and depends entirely on that unmeasured split (chains C2, C4).

**Trade-offs acknowledged:** The plan accepts a few weeks' delay and an audit fee. It gives up any comfort or noise benefit from new windows. It also accepts that the attic probably pays back over its roughly 30-year life rather than within your 10-year stay, so at resale you may not recover the remaining value (chains C5, C6).

**Pre-check:** head C5 (MEDIUM), C6 (MEDIUM) · ?-marked: none · lowest cited: MEDIUM · Inputs ceiling: MEDIUM (chains C5, C6)
**Confidence:** MEDIUM — C5 and C6 are both rated MEDIUM. Their own confidence lines name the verifications: the written quotes, 12 months of bills, and the audit's measurement of the attic share (chains C5, C6).

---

## Self-audit scan (process output)

| Chain | Chain Head (brief) | Form conforming? | Rule applied | Dependency clean? |
|---|---|---|---|---|
| C1 | GT-4? + GT-5? | yes | n/a | yes |
| C2 | C1 + GT-3? | yes | n/a | yes |
| C3 | GT-1 + GT-2? | yes | n/a | yes |
| C4 | C1 + C3 + GT-7? | yes | n/a | yes |
| C5 | C2 | yes | n/a | yes |
| C6 | C4 + GT-6? | yes | n/a | yes |

| §6 Span (brief) | Construct | Claim under R11? | R11 clause applied | Chain cited |
|---|---|---|---|---|
| Recommended approach: skip windows; audit, seal, inspect, insulate | bold lead-in | yes | prescribed lead-in, colon closes bold span | C5, C6 |
| Key insight: 35% ceiling rules out windows; attic turns on split | bold lead-in | yes | prescribed lead-in, colon closes bold span | C2, C4 |
| Trade-offs acknowledged: delay, fee, forgone comfort, resale | bold lead-in | yes | prescribed lead-in, colon closes bold span | C5, C6 |
| Pre-check: head C5, C6 | bold lead-in | yes | bold lead-in whose colon closes the bold span | C5, C6 |
| Confidence: MEDIUM | bold lead-in | yes | bold lead-in whose colon closes the bold span | C5, C6 |

```text
Scan complete: 6 chain rows, one per section-4 chain block in order; 5 section-6 rows, one per construct in order — 5 claims under R11, 0 excluded. 0 chains malformed, 0 claims untraced.
```

## Self-Audit Gate (process output)

The Assumption Audit table covers all 24 chain steps across C1–C6. The self-audit scan is present, and its counts check against §4 (6 blocks) and §6 (5 constructs).

**Criterion 1: Identify Essence**
Quoted span: "which, if any, of two envelope upgrades recovers its cost in heating savings over a stay of at least 10 years. That depends on how the 35% loss is split between an R-13 attic and 14 windows of unknown type"
Band: **Rigorous**
Justification: It names the decision and its governing unknown specific to this house. Each success criterion is a verb–subject–outcome test checkable against §6 (window verdict across the bracket, attic verdict with threshold, action this year).

**Criterion 2: Challenge Assumptions**
Quoted span: "| C4 | 4 | conduction estimate a ≈ 0.3–0.5 | A15: areas ~1,000 / ~170 sq ft | yes |"
Band: **Rigorous**
Justification: Every row is typed from the four-type scheme, with the matching treatment and a token-plus-em-dash verdict. Several rows are challenged and one is discarded. Unverified rows used in chains read "unverified — flagged". The audit covered every step and surfaced A12, A15, A16 and A17 into the table.

**Criterion 3: Establish Ground Truths**
Quoted span: "enumerated GT-2, GT-3, GT-4, GT-5, GT-6, GT-7; the list carries `?` on exactly those six; GT-1 is unsuffixed with read location wikitext lines 69 and 236"
Band: **Rigorous**
Justification: The enumeration matches the list. The single unsuffixed ground truth names its read location. The 404 source has a failure record. GT-1 feeds only a MEDIUM chain, but only because C3's other input is `?`, and a reachable unsuffixed ground truth feeding only MEDIUM chains would band Sound under the strict reading. I note this as the one borderline item.

**Criterion 4: Reason Upward**
Quoted span: "| C4 | C1 + C3 + GT-7? | yes | n/a | yes |" and §5 "Why abandoned: C2 shows that even if 100% of the top-bracket L went through the windows…"
Band: **Rigorous**
Justification: All six chains conform in form and dependency. Assumption-introducing hops carry `[Assumes:]` marks. The arithmetic recomputes (adversarial Recompute). §5 documents four dead ends in the prescribed structure, and no analogy is used as evidence.

**Criterion 5: Validate**
Quoted span: "A16 is priced: if the audit cannot isolate a before November, the fallback is to insulate anyway, because C4's lifetime threshold (a ≥ 0.27) is likely met, so the direction is unchanged."
Band: **Sound**
Justification: Every MEDIUM line names its `?` inputs and cited chains, with verification paths. The adversarial record is complete, with dispositions for all clusters. All chains are MEDIUM for the named Inputs reason. But C3's line is borderline: GT-1 is clean, and the only downgrade cause is GT-2?, which is user-supplied and has no fetchable source. I rate it Sound rather than claim full calibration.

**Criterion 6: Conclusion-to-Ground-Truth Traceability**
Quoted span: "5 claims under R11, 0 excluded. 0 chains malformed, 0 claims untraced." and Key insight "That rules out the $18,500 windows on arithmetic alone, before anyone knows the attic/window split."
Band: **Rigorous**
Justification: Every §6 claim cites its chain. The Key Insight states a non-obvious ceiling result (the split doesn't matter for the windows but decides the attic) rather than restating the recommendation.

The gate is cleared: no criterion scored Absent, and none scored Hand-wavy.

---

**In plain terms:** Your $410 × 4 winter months puts annual heating at about $2,000 (range $1,350–$2,730). If 35% of that leaves through the attic and windows, the most any fix can save is about $700 a year, and at most about $957. Even perfect windows couldn't save more than that, so they can't return $18,500 within 10 years; the best case is under $11,000. The attic upgrade removes about 73% of the heat that currently conducts through the attic ceiling. Whether it pays back within 10 years depends on how much of that 35% is actually the attic: it needs more than about 80% at the central estimate, and a rough conduction estimate suggests 30–50%. Over the insulation's roughly 30-year life, though, it likely comes out ahead. That's why the audit comes first. It costs little next to $4,200, can happen before winter, and should include checks for knob-and-tube wiring and vermiculite, both plausible in a 1948 attic. Every figure except the R-value physics comes from your description and hasn't been checked, so treat these numbers as MEDIUM confidence until the audit and a year of bills confirm them.