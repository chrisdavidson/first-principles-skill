**Short answer:** Do the attic insulation this year, and don't replace the windows. Replacing the windows doesn't pay back on energy savings under any assumption I tried. The attic is closer than the contractor's pitch suggests. At exactly 10 years it roughly breaks even, and whether it comes out ahead depends on two facts you can check in an afternoon. The full working follows.

## Trade-off (process output)

Options, in your order: Attic ($4,200), Windows ($18,500), Both ($22,700), Neither.

I set these weights before scoring any option. For every criterion, a higher score is better.

| Criterion | Weight |
|---|---|
| A. Net money over 10 years | 5 |
| B. Net money over the insulation's full life | 3 |
| C. Holds up whether the attic or the windows lose more heat | 3 |
| D. Low upfront cash | 3 |
| E. Comfort and other non-energy benefits | 2 |
| F. Low risk of trouble during the work | 2 |

| Option | A×5 | B×3 | C×3 | D×3 | E×2 | F×2 | Total |
|---|---|---|---|---|---|---|---|
| Attic | 3→15 | 5→15 | 3→9 | 4→12 | 3→6 | 3→6 | **63** |
| Windows | 1→5 | 1→3 | 2→6 | 1→3 | 4→8 | 2→4 | **29** |
| Both | 1→5 | 2→6 | 2→6 | 1→3 | 5→10 | 2→4 | **34** |
| Neither | 3→15 | 2→6 | 5→15 | 5→15 | 1→2 | 5→10 | **63** |

Sensitivity check: Attic and Neither tie exactly. Weight B would decide it, and I can't say B was wrong before seeing the result, so the tie is a real finding. The template's tiebreak (the first-listed option) picks Attic, and C5 and §5 record it.

## Assumption Audit scan (process output)

| Chain | Step | Step Text (brief) | Assumption surfaced? | Added to Table? |
|---|---|---|---|---|
| C1 | 1 | attic U drops from 1/13 to 1/49 | none | n/a |
| C1 | 2 | at most a 73.5% cut | none | n/a |
| C2 | 1 | coldest four months cost $1,640 | none | n/a |
| C2 | 2 | annual heating about $2,600 | A2, A3 (already in table) | n/a |
| C2 | 3 | attic+window pool about $910 | none | n/a |
| C2 | 4 | 65% of loss is outside both quotes | none | n/a |
| C3 | 1 | attic share 35–60% | A5 (already in table) | n/a |
| C3 | 2 | realized cut 55–74% | A6 (already in table) | n/a |
| C3 | 3 | savings $135/$334/$461 | none | n/a |
| C3 | 4 | payback 31/12.6/9.1 yr | none | n/a |
| C3 | 5 | 10-yr savings $3,340–$3,830 at center | A8 (already in table) | n/a |
| C4 | 1 | triple-pane cuts window loss 60–80% | A7 (already in table) | n/a |
| C4 | 2 | savings $168/$319/$543 | none | n/a |
| C4 | 3 | payback 110/58/34 yr | none | n/a |
| C4 | 4 | $58 vs $12.60 per $1/yr saved | none | n/a |
| C4 | 5 | fails at every bracket end | none | n/a |
| C5 | 1 | trade-off totals 63/63/34/29 | A14 (savings add) | yes |
| C5 | 2 | tie goes to attic by tiebreak | none | n/a |
| C5 | 3 | staying past year 10 favors attic | none | n/a |
| C5 | 4 | recommend attic, no windows | none | n/a |
| C5 | 5 | [2nd] colder attic, condensation risk | none | n/a |
| C5 | 6 | [3rd] air sealing and baffles needed | none | n/a |
| C6 | 1 | 1948 is the era of vermiculite and knob-and-tube | A13 (already in table) | n/a |
| C6 | 2 | could stop the job or add cost | A16 (quote excludes remediation) | yes |
| C6 | 3 | test before signing | none | n/a |
| C7 | 1 | two factors drive the attic bracket | none | n/a |
| C7 | 2 | spend measurable from bills | A17 (summer = baseline) | yes |
| C7 | 3 | window type sets the attic's share | A5 (already in table) | n/a |
| C7 | 4 | both checks settle center vs. low corner | none | n/a |

## Adversarial pass (process output)

**Premise:** It is September 2027. The attic was insulated, the windows were skipped, and the decision failed.

**Causes** (from four viewpoints: homeowner, contractor, whoever pays, future buyer or inspector):
1. The heating bill barely moved because the attic was a small share of the 35%.
2. Drafty windows still make the rooms uncomfortable.
3. Moisture and ice dams showed up in the colder attic.
4. The house is still cold because walls and air leaks (the other 65%) were never touched.
5. Vermiculite turned up mid-job, the job stopped, and abatement cost extra.
6. Live knob-and-tube wiring was found, so an electrician was needed first.
7. Insulation was blown in without air sealing, and the soffit vents got blocked.
8. The insulation settled below R-49.
9. The $410 included water heating and other loads, so savings were figured on an inflated base.
10. Energy prices fell.
11. A job move forced a sale in year 6.
12. Window sashes rotted anyway, and replacing them in year 3 cost more.
13. Lead paint on the window sashes was flagged at sale.

Causes 1, 9 and 12 contradict the recommendation's own premise, so they carry the most weight.

**Clusters:**
- **K1: the savings base was never measured** (causes 1, 4, 9, 10). Bears on C2, C3, C7, GT-2?, GT-3?.
- **K2: hidden conditions in a 1948 attic** (causes 3, 5, 6, 7, 8). Bears on C5, C6, GT-8?.
- **K3: windows deferred on energy alone, ignoring their condition** (causes 2, 12, 13). Bears on C4, C5.
- **K4: the stay turned out shorter than planned** (cause 11). Bears on C5, GT-5?.

**Disposition:**
- **K1, plan change:** before signing, total 12 months of bills minus the summer baseline, and confirm the window type (C7).
- **K2, plan change:** the quote must include air sealing, soffit baffles and depth markers. Test for vermiculite and inspect the wiring first (C6, C5 [3rd]).
- **K3, accepted risk:** mitigation is to inspect the sashes and repair or replace failing units one at a time, on their condition. Low-e storm windows are a cheaper draft fix to price.
- **K4, accepted risk:** mitigation is to keep the R-49 invoice for a future listing. The loss is capped at $4,200 minus the savings already banked.

## §6→§4 closure ledger (process output)

- "Do the attic insulation this year and skip the window replacement" → chain C5 ✓
- "Windows are the worst buy even if they leak as much heat as the attic" → chains C3, C4, C7 ✓
- "Attic ties with doing nothing at a strict 10-year rule" → chains C3, C5 ✓
- "About 65% of the loss is outside both quotes" → chain C2 ✓
- 5 pre-signing list items → C7, C7, C6, C5, C4 ✓
- "Confidence MEDIUM" → chains C1–C7 ✓

## Self-audit scan (process output)

| Chain | Chain Head (brief) | Form conforming? | Rule applied | Dependency clean? |
|---|---|---|---|---|
| C1 | GT-1? + GT-4? | yes | n/a | yes |
| C2 | GT-2? + GT-7? + GT-3? | yes | n/a | yes |
| C3 | C1 + C2 + GT-6? | yes | n/a | yes |
| C4 | C2 + C3 + GT-6? + GT-4? | yes | n/a | yes |
| C5 | C3 + C4 + GT-5? | yes | n/a | yes |
| C6 | GT-8? + GT-4? | yes | n/a | yes |
| C7 | C3 + C2 | yes | n/a | yes |

| §6 Span (brief) | Construct | Claim under R11? | R11 clause applied | Chain cited |
|---|---|---|---|---|
| Recommended approach | bold lead-in | yes | bold lead-in whose colon closes the bold span | C5 |
| Key insight | bold lead-in | yes | bold lead-in whose colon closes the bold span | C3, C4, C7 |
| Trade-offs acknowledged | bold lead-in | yes | bold lead-in whose colon closes the bold span | C3, C5 |
| What neither quote touches | bold lead-in | yes | bold lead-in whose colon closes the bold span | C2 |
| Before signing | bold lead-in | no | section-intro label: colon span is the whole line, no citation | n/a |
| Total 12 months of bills | list item | yes | list item over forty characters | C7 |
| Check window type | list item | yes | list item over forty characters | C7 |
| Test for vermiculite and wiring | list item | yes | list item over forty characters | C6 |
| Require air sealing and baffles | list item | yes | list item over forty characters | C5 |
| No windows for energy savings | list item | yes | list item over forty characters | C4 |
| Confidence | bold lead-in | yes | bold lead-in whose colon closes the bold span | C1–C7 |

```text
Scan complete: 7 chain rows, one per section-4 chain block in order; 11 section-6 rows, one per construct in order — 10 claims under R11, 1 excluded. 0 chains malformed, 0 claims untraced.
```

## Self-Audit Gate (process output)

**Criterion 1: Identify Essence**
Quoted span: "Which of the four spend options returns more in avoided heating cost, over a stay of at least ten years, than it costs up front, when the attic-versus-window split of the 35% loss is unknown?"
Band: **Rigorous**
Justification: the statement names the decision and the unknown that shapes it, and each success criterion can be checked against a property of §6.

**Criterion 2: Challenge Assumptions**
Quoted span: "C6 | 2 | could stop the job or add cost | A16 (quote excludes remediation) | yes"
Band: **Rigorous**
Justification: all 17 rows use one of the four types and have a leading verdict token with a justification, the table has Challenge and Discard verdicts, and the audit covers all 29 steps and added A14, A16 and A17.

**Criterion 3: Establish Ground Truths**
Quoted span: "enumerated GT-1 through GT-8; the list carries `?` on exactly those eight"
Band: **Rigorous**
Justification: the enumeration matches the list, and no GT is unsuffixed, so no read location is owed and no HIGH chain exists.

**Criterion 4: Reason Upward**
Quoted span: "C5 | C3 + C4 + GT-5? | yes | n/a | yes"
Band: **Rigorous**
Justification: all seven chains conform and have clean dependencies, §5 lists four dead ends in full structure, and the audit additions carry `[Assumes:]` marks.

**Criterion 5: Validate**
Quoted span: "Inputs axis short: GT-5? (stay length, user-supplied), and C3 and C4 are MEDIUM"
Band: **Rigorous**
Justification: every chain is MEDIUM because each has user-supplied `?` inputs, each confidence line names its inputs and how to close them, the pre-mortem record is complete with a disposition per cluster, and the overall MEDIUM matches the weakest chain.

**Criterion 6: Conclusion-to-Ground-Truth Traceability**
Quoted span: "Key insight | bold lead-in | yes | … | C3, C4, C7"
Band: **Rigorous**
Justification: all 10 claims cite a chain, and the key insight (cost per dollar saved; the attic's 10-year tie) is not a restatement of the recommendation.

Gate cleared: nothing scored Absent or Hand-wavy.

---

## 1. Problem Essence

**Core problem:** Which of the four spend options returns more in avoided heating cost, over a stay of at least ten years, than it costs up front, when the attic-versus-window split of the 35% loss is unknown?

**Success criteria:**
- The Conclusion names exactly one of the four options as the recommendation.
- The Conclusion gives each quote's payback as a bracketed range, not a single number.
- The Conclusion names the unknown facts that could reverse the recommendation and says how to check them.
- The Conclusion says which hazards or scope gaps in the attic quote must be settled before signing.

## 2. Assumptions Table

| Assumption | Type | Treatment | Verdict | Verification |
|---|---|---|---|---|
| A1: the 35% attic+windows share is accurate | untested belief | verify or flag | Challenge — no source for it was named | unverified — flagged (GT-3?) |
| A2: the $410/month is heating-only | untested belief | verify or flag | Challenge — it may include water heating and other loads; the C2 low bracket assumes a $60/month baseline | unverified — flagged |
| A3: the four coldest months are 55–70% of the heating season | untested belief | verify or flag | Challenge — climate not stated | unverified — flagged (GT-7?) |
| A4: heat conducted through a surface ∝ area / R-value | physical law | accept as a ground-truth candidate | Accept — this is what R-value means | definition; no source opened — unverified — flagged (GT-1?) |
| A5: the attic is 35–60% of the attic+window loss | untested belief | verify or flag | Challenge — depends on whether the windows are single-pane | unverified — flagged |
| A6: the real attic cut is 55–74% (framing and air leaks eat into it) | untested belief | verify or flag | Challenge — heat bridges through joists and leak paths | unverified — flagged |
| A7: current windows are R≈1–2; triple-pane R≈4–5 | untested belief | verify or flag | Challenge — window type unknown | unverified — flagged (GT-6?) |
| A8: energy prices rise about 3%/year | untested belief | verify or flag | Challenge — the flat-price figure is also reported | unverified — flagged |
| A9: the quotes are accurate as stated | current constraint | record expiry | Accept — valid until the quote expires (often 30–90 days) | unverified — flagged (GT-4?) |
| A10: an upgrade must pay back within 10 years | convention | challenge before use | Challenge — your horizon is a minimum and insulation outlasts it (see §5) | your "at least 10 years" (GT-5?) |
| A11: energy upgrades raise sale value | untested belief | verify or flag | Discard — no data; not relied on | not used |
| A12: the federal tax credit applies | current constraint | record expiry | Discard — believed ended for 2026 installs; not relied on | unverified |
| A13: a 1948 attic may hold vermiculite or knob-and-tube; the sashes may have lead paint | untested belief | verify or flag | Challenge — test before any work | unverified — flagged (GT-8?) |
| A14: attic and window savings add up | physical law | accept as a ground-truth candidate | Accept — separate heat paths add; surfaced by the audit at C5 step 1 | parallel paths add (definition); unverified — flagged |
| A15: all decisions must be made this year | convention | challenge before use | Discard — windows can be deferred or done piecemeal | n/a |
| A16: the $4,200 quote excludes hazard cleanup and air sealing | untested belief | verify or flag | Challenge — surfaced at C6 step 2; ask the contractor | unverified — flagged |
| A17: summer bills show the non-heating baseline | untested belief | verify or flag | Challenge — surfaced at C7 step 2; false if AC is on the same bill | unverified — flagged |

## 3. Ground Truths

- **GT-1?** Heat conducted through a surface is proportional to area / R-value — unverified: this is the definition of R-value, but I opened no source for it.
- **GT-2?** Heating bills average $410/month over the four coldest months — unverified: your figure, source not named.
- **GT-3?** About 35% of heating energy is lost through the attic plus the windows — unverified: your figure, no audit named.
- **GT-4?** Quotes: $4,200 for R-13→R-49 attic insulation; $18,500 for 14 triple-pane windows — unverified: your figures.
- **GT-5?** You will stay at least 10 more years — unverified: your stated plan.
- **GT-6?** Old single-pane windows are about R-1 (about R-2 with storms or double-pane); triple-pane units are about R-4 to R-5 — unverified: general figure; your window type is unknown.
- **GT-7?** In a cold US climate the four coldest months carry about 55–70% of the heating season — unverified: your climate is not stated.
- **GT-8?** Houses of this era commonly have vermiculite attic insulation (possibly asbestos) and knob-and-tube wiring, which should not be buried; pre-1978 paint may contain lead — unverified: general regulatory knowledge, no source opened.

```text
?-marked: GT-1, GT-2, GT-3, GT-4, GT-5, GT-6, GT-7, GT-8 (8 of 8)
Read-at-source: none required — no chain is rated HIGH, because every chain has a user-supplied ? input; no Phase 3 read was triggered, so there are no failure records
```

## 4. Derivation Chains

### Conclusion C1: The insulation upgrade removes at most 73.5% of the attic's conducted heat loss

GT-1? (heat loss ∝ area/R) + GT-4? (R-13 → R-49 quote)
→ the attic's U-factor falls from 1/13 to 1/49 per unit of area and temperature difference
→ the insulation removes at most 1 − 13/49 = 73.5% of conducted attic loss

**Confidence:** MEDIUM — Inputs axis short. GT-1? closes by opening any building-physics reference on R-value. GT-4? closes by reading the signed quote. The arithmetic itself is exact.

### Conclusion C2: About $910/year escapes through the attic and windows; about $1,690/year escapes elsewhere

GT-2? ($410 × 4 coldest months) + GT-7? (4 coldest ≈ 55–70% of season) + GT-3? (35% via attic + windows)
→ the four coldest months cost $1,640 in heating
→ annual heating spend is about $2,600, bracketed $2,000–$2,980
→ the attic-plus-window share of the loss is about $910/year, bracketed $700–$1,045
→ the other 65% of the loss, about $1,690/year, is outside both quotes

**Confidence:** MEDIUM — Inputs axis short. GT-2? and GT-7? close with 12 months of bills. GT-3? closes with a blower-door or infrared energy audit. A2 is covered: the $2,000 low end already assumes a $60/month non-heating baseline, and the 65% endpoint is a fraction that doesn't depend on A2.

### Conclusion C3: The attic pays back in 9–31 years, 12.6 years in the central case — roughly break-even at 10 years

C1 (≤73.5% cut) + C2 ($700–$1,045 attic+window loss) + GT-6? (window R sets the split)
→ the attic carries 35–60% of the attic+window loss, 50% in the central case
→ the real cut is 55–74% once framing and air leaks are counted
→ attic savings are $135/year low, $334 central, $461 high
→ simple payback on $4,200 is 31 years low, 12.6 central, 9.1 high
→ 10-year savings in the central case are $3,340 at flat prices to $3,830 with 3%/year price rises, against $4,200

**Confidence:** MEDIUM — Inputs axis short: C1 and C2 are MEDIUM, and GT-6? closes by checking whether your windows are single-pane. A5 and A6 are the ranges the bracket already spans. If either fell outside its range, the payback would move outside 9–31 years, but the central case would stand as stated.

### Conclusion C4: Window replacement fails on energy savings at every bracket end

C2 ($700–$1,045 attic+window loss) + C3 ($12.60 per $1/year saved) + GT-6? (R≈1–2 now, ≈4–5 triple) + GT-4? ($18,500)
→ triple-pane windows cut conducted window loss by 60–80%
→ window savings are $168/year low, $319 central, $543 high
→ simple payback is 110, 58 and 34 years respectively
→ each dollar of annual saving costs about $58 up front, against about $12.60 for the attic in C3
→ even the best case pays back in more than three times your 10-year stay, so energy savings alone do not justify replacement

**Confidence:** MEDIUM — Inputs axis short: C2 and C3 are MEDIUM, GT-6? closes by checking window type, and GT-4? by reading the quote. Robustness: to pay back within 10 years, the savings would have to be 3.4× the high case. The low/high corners of C3 and C4 describe opposite splits and can't both happen.

### Conclusion C5: Do the attic this year, with air sealing and baffles; do not replace the windows

C3 (attic about break-even at 10 years) + C4 (windows fail at every end) + GT-5? (stay ≥ 10 years)
→ with weights fixed before scoring, the totals are Attic 63, Neither 63, Both 34, Windows 29 [Assumes: A14]
→ the tie goes to the attic under the first-listed tiebreak
→ every year you stay past year 10 adds savings on the attic side, because insulation keeps working
→ recommend the attic job this year and no window replacement
→[2nd] less heat reaches the attic, so it runs colder and any warm air leaking up condenses more readily
→[3rd] the attic job must include air sealing of ceiling leaks and soffit baffles, or it trades heat savings for moisture risk

**Confidence:** MEDIUM — Inputs axis short: GT-5? (stay length, user-supplied), and C3 and C4 are MEDIUM. Rivals: "Neither" is ruled out in the central case by §5's first dead end. It stays defensible in C3's low corner, which C7 checks. A14: if savings interact rather than add, "Both" scores even lower, so the endpoint is unaffected. The tie is flagged.

### Conclusion C6: Test for vermiculite and knob-and-tube wiring before signing

GT-8? (1948-era hazards) + GT-4? ($4,200 quote scope)
→ a 1948 attic is in the era when vermiculite and knob-and-tube wiring were common
→ either finding can stop the job or add cost the quote does not cover [Assumes: A16]
→ vermiculite testing and a wiring inspection have to come before signing

**Confidence:** MEDIUM — Inputs axis short: GT-8? closes with an asbestos test of any loose-fill and an electrician's look at the wiring. A16: if the quote already covers remediation, testing before signing is still the right order, so the endpoint holds.

### Conclusion C7: Two afternoon checks decide whether the attic lands at the central case or the low corner

C3 (attic bracket straddles 10 years) + C2 (spend bracket)
→ the two unknowns driving the attic bracket are annual heating spend and the attic's share of the loss
→ annual heating spend can be measured from 12 months of bills minus the summer baseline [Assumes: A17]
→ the attic's share can be estimated from whether the windows are single-pane or double/storm
→ both checks take an afternoon and show whether the attic lands at the central case or the low corner

**Confidence:** MEDIUM — Inputs axis short: C2 and C3 are MEDIUM. A17: if summer bills include AC, use the spring and fall bills with the heat off as the baseline instead. The endpoint holds.

## 5. Abandoned Reasoning

### Dead End: "Neither," judged on a strict 10-year simple payback
**What was tried:** reject the attic because its central payback (12.6 years) is longer than 10.
**Why abandoned:** a 10-year payback rule is a convention (A10), not your goal. Your horizon is "at least" 10 years (GT-5?), and the insulation keeps saving after year 10 (C3).
**What it ruled out:** "Neither" as the central-case answer. It remains defensible only in C3's low corner, which C7 checks.

### Dead End: split the 35% by surface area, which makes the attic dominant
**What was tried:** assume the attic (roughly 1,000 sq ft) dwarfs the windows (roughly 190 sq ft), so the attic carries most of the loss.
**Why abandoned:** it contradicts GT-1?. Loss scales with area divided by R-value, so single-pane windows (190/1 ≈ 190) could lose more than an R-13 attic (1,000/13 ≈ 77). These areas are illustrative.
**What it ruled out:** assuming the attic is automatically the bigger leak. That is why C3 uses a range of 35–60%.

### Dead End: count the federal energy tax credit
**What was tried:** reduce the net cost by 30%.
**Why abandoned:** its availability is unverified (A12; believed ended for 2026 installs), and it is not needed for the recommendation.
**What it ruled out:** relying on a credit. Any credit or utility rebate would only improve the attic case.

### Dead End: justify windows by resale value
**What was tried:** assume the $18,500 comes back at sale.
**Why abandoned:** A11 is an untested belief with no data here, which is too weak to support a $18,500 decision.
**What it ruled out:** the resale argument as a reason for windows.

## 6. Conclusion

**Recommended approach:** Do the attic insulation this year and skip the window replacement, subject to the checks below (chain C5).

**Key insight:** The windows are the worst buy even if they leak as much heat as the attic. Each dollar of annual saving costs about $58 up front, against about $12.60 for the attic. And the attic only breaks even at exactly 10 years, so its case rests on staying longer and on two facts you can check in an afternoon (chains C3, C4, C7).

**Trade-offs acknowledged:** Under a strict 10-year rule, the attic ties with doing nothing (63 vs 63). Choosing it accepts a shortfall of about $370–$860 in the central case in return for savings after year 10 and better comfort (chains C3, C5).

**What neither quote touches:** About 65% of your heat loss, roughly $1,690/year, goes through walls, air leaks and the foundation, which neither quote addresses (chain C2).

**Before signing:**

- Total the last 12 months of heating bills, subtract the summer baseline, and see whether annual heating spend is nearer $2,000 or $3,000 (chain C7).
- Check whether the windows are single-pane or double/storm. Single-pane shifts the loss toward the windows and pushes the attic toward its low corner (chain C7).
- Have any loose-fill attic insulation tested for vermiculite and the wiring checked for knob-and-tube before the job starts (chain C6).
- Require the attic quote to include air sealing of ceiling leaks and soffit baffles (chain C5).
- Do not replace windows for energy savings; even the best case takes more than three times your stay to pay back (chain C4).

**Confidence:** MEDIUM — contributing chains C1–C7 are all MEDIUM because every one rests on figures you supplied that were not checked against a source, plus climate and window-type parameters that are estimates. The Attic–Neither tie was broken by the template's first-listed rule and is flagged (chain C5).