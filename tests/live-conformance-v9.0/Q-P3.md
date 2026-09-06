Analysis complete. Three external sources read at source; one Phase 3 read failed and is recorded below. Step 0 classified this as `full-composer` (no focused-technique trigger fired), so all phases ran.

---

# First-Principles Analysis: Attic Insulation vs. Window Replacement

## 1. Problem Essence

**Essence Statement:** Which allocation of this year's improvement budget buys the most avoided heating cost per dollar over a holding period of *at least* ten years — a capital-allocation question about a shared pool of heat loss, not a question about which of two quotes is the better product.

**Success criteria** (each checkable by scanning section 6):

1. The Conclusion names a disposition for each of the four options asked about — insulation, windows, both, neither.
2. The Conclusion states a payback period or ten-year net figure for each option it rejects, rather than a qualitative preference.
3. The Conclusion identifies any higher-return action lying outside the four options, or states that none exists.
4. The Conclusion names which unverified input, if corrected, would change the recommendation.

The triggering event was receiving two quotes. That is not the question. The question is whether either quote clears the household's own cost of capital over its own horizon, and whether the option set the quotes define is the real option set.

---

## 2. Assumptions Table

| # | Assumption | Type | Treatment | Verdict | Verification |
|---|---|---|---|---|---|
| A1 | Conductive loss through a building assembly is inversely proportional to its total thermal resistance | physical law | Accept as ground-truth candidate | **Accept** — laws do not expire | Fourier conduction, one-dimensional composite wall → GT-6 |
| A2 | The stated 35% is an accurate measurement of *this* house | untested belief | Verify, or flag | **Challenge** — origin unstated; if it came from either contractor it is a motivated figure, and both contractors sell against it | unverified — flagged → GT-4? |
| A3 | $410/month is heating fuel cost, not the whole utility bill | untested belief | Verify, or flag | **Challenge** — baseload electric could be $100–150 of it, lowering every saving here | unverified — flagged; bracketed both directions in C5 |
| A4 | Heating occurs only in the four coldest months | convention | Challenge before use | **Discard** — heating load tracks degree days, which run into the shoulder months; annual spend exceeds the four-month sum | corrected via GT-13? |
| A5 | The existing windows are single-pane without storms | untested belief | Verify, or flag | **Challenge** — decisive for the storm-window option, immaterial to the replacement verdict | unverified — flagged; both branches priced in C6 via GT-9 and GT-10 |
| A6 | The attic is dry, adequately ventilated, and free of active knob-and-tube wiring, non-IC-rated recessed fixtures, and attic-terminated bath fans | untested belief | Verify | **Challenge** — surfaced by inversion; 1948 construction makes each likely enough to price before committing | unverified — flagged; any one converts a $4,200 job into a larger one |
| A7 | Nominal R-49 delivers R-49 in service | convention | Challenge before use | **Challenge** — framing bridges, settling and wind-washing reduce effective R | the 71% figure in C2 is an upper bound, discounted to ~70% in C5 |
| A8 | Ten years is the evaluation horizon | convention | Challenge before use | **Discard** — "at least another 10 years" is a floor, not a ceiling; a measure whose service life far exceeds its payback keeps accruing | drives C4 and the C5 framing |
| A9 | The four options offered exhaust the solution space | convention | Challenge before use | **Discard** — air sealing, storm windows, interior inserts and heating-plant upgrades were all excluded by the framing, not by analysis | C6 |
| A10 | $4,200 is a market-rate price for this scope | untested belief | Verify, or flag | **Challenge** — implies roughly $3/sq ft over a mid-size attic, above typical blown-in loose-fill rates for an R-36 add | unverified — flagged; re-bid recommended |
| A11 | Triple-pane outperforms good double-pane by enough to matter here | current constraint | Record expiry conditions | **Challenge** — DOE's whole-window U-factor floor is 0.20 and the ENERGY STAR northern spec is ≤0.30, so the increment is small | Expiry: lifts if triple-pane reaches price parity with double-pane |
| A12 | Comfort and draft reduction have no value beyond the metered bill | convention | Challenge before use | **Challenge** — the bill measures energy, not the radiant asymmetry and infiltration discomfort that motivates most window projects | acknowledged as unpriced upside, deliberately not monetized |
| A13 | No competing claim exists on the $22,700 over the horizon | untested belief | Verify, or flag | **Challenge** — surfaced by the Phase 4 audit from C1; a failing furnace or roof would outrank both quotes | unverified — flagged |
| A14 | Attic floor area is 800–1,600 sq ft and glazing is near 210 sq ft | untested belief | Verify, or flag | **Challenge** — surfaced by the Phase 4 audit from C5; these bounds set the conductance ratio that splits the 35% | unverified — flagged; an audit measures both directly |
| A15 | Heating fuel and appliance efficiency stay constant over the horizon | untested belief | Verify, or flag | **Challenge** — surfaced by the Phase 4 audit from C6; a heat-pump conversion re-prices every saving computed here | unverified — flagged |

---

## 3. Ground Truths

`?`-marked, enumerated by ID: **GT-4, GT-12, GT-13** (3 of 13).

| ID | Fact | Source | Provenance |
|---|---|---|---|
| GT-1 | The four coldest months average $410/month, totalling $1,640 | Problem statement | read-at-source — the user's message, this conversation |
| GT-2 | $4,200 quoted to blow R-49 over existing R-13 | Problem statement | read-at-source — the user's message |
| GT-3 | $18,500 quoted for 14 triple-pane replacement windows | Problem statement | read-at-source — the user's message |
| GT-4? | Attic and windows together account for ~35% of heating loss | Problem statement; the *measurement's* own origin is unstated | **unverified** — the figure is stated, its derivation is not |
| GT-5 | Intended occupancy is at least ten more years | Problem statement | read-at-source — the user's message |
| GT-6 | Conductive loss through a plane assembly is inversely proportional to its total thermal resistance | Fourier's law, one-dimensional composite wall | physical law — irreducible; no external citation applicable |
| GT-7 | "Upgrading to ENERGY STAR qualified models can save you 7%–15% on annual household energy bills, or roughly $71-$501 annually, depending on your geographic location and the type of window being replaced." | DOE/EE-0352, *Guide to Energy-Efficient Windows*, Oct 2010 | read-at-source — **p.1, left column, "Replacing Old Windows"** |
| GT-8 | "Before replacing your windows, be sure you have already properly insulated and air sealed your home." | DOE/EE-0352, same document | read-at-source — **p.1, left column, closing paragraph** |
| GT-9 | "ENERGY STAR certified (low-e) storm windows can save homeowners $350 on their annual heating and cooling bills (about 10%) when installed over single-pane clear glass windows (without existing storm windows)." | energystar.gov/products/storm_windows_0 | read-at-source — **savings-claims section, first claim** |
| GT-10 | "Consumers who already have clear glass storm windows over their single pane windows and replace the storms with ENERGY STAR certified (low-e) storm windows can save an additional $50 per year on heating and cooling (about 2%) on a national average." | energystar.gov/products/storm_windows_0 | read-at-source — **same section, third claim** |
| GT-11 | "homeowners can save an average of 15% on heating and cooling costs (or an average of 11% on total energy costs) by air sealing their homes and adding insulation in attics, floors over crawl spaces, and accessible basement rim joists." | energystar.gov/saveathome/seal_insulate/methodology | read-at-source — **savings methodology, headline estimate** |
| GT-12? | Insulating glass unit service life before seal or gas-fill degradation is on the order of 20–25 years | **Phase 3 failure record:** osti.gov/biblio/1967951 was opened; its abstract states no service life in years — *citation does not support the claim* | **unverified** — carries `?`; feeds only MEDIUM chain C4 |
| GT-13? | The four coldest months carry roughly 65–75% of annual heating degree days in a typical US heating climate | No source read; the household's climate zone was not supplied | **unverified** — bracketed rather than asserted |

**Phase 3 read attempts that failed, recorded rather than silently dropped:** `energy.gov/energysaver/storm-windows` and `energy.gov/energysaver/insulation` both returned HTTP 404; substitute ENERGY STAR sources were located and read instead. The PNNL low-e storm-window brochure returned an unparseable PDF stream; it was not needed, since GT-9 and GT-10 cover the same ground from a source that did open. `docs.nrel.gov` failed DNS resolution.

---

## 4. Derivation Chains

**C1 — the arithmetic ceiling. Confidence: HIGH.**

```text
GT-1 (four coldest months cost $1,640 in total) + GT-2 (attic quote $4,200) + GT-3 (window quote $18,500) + GT-5 (occupancy at least ten more years)
→ the whole four-month heating spend is the hard ceiling on what any measure acting on heating alone can return in a single year
→ dividing the window quote by that ceiling gives 11.3 years, and dividing the combined $22,700 by it gives 13.8 years
→ neither measure touches the heating plant, the water heater or the rest of the envelope, so each returns strictly less than the ceiling and each payback runs strictly longer than those figures [Assumes: no competing claim exists on the $22,700 over the horizon]
→ the window replacement and the both-measures package are each disqualified against a ten-year horizon by division alone, with no energy model, climate data or split of the 35% required
```

*Weakest link:* hop 3's claim that each measure returns less than the ceiling — true by construction, since neither quote touches the heating plant, the water heater, the walls, the floor or the doors.

**C2 — the physical bound on the attic measure. Confidence: HIGH.**

```text
GT-6 (conductive loss is inversely proportional to total thermal resistance) + GT-2 (attic quote raises R-13 to R-49)
→ adding the air films and ceiling finish common to both states puts the assembly near R-14.5 before and R-50.5 after
→ the ratio of those resistances fixes the reduction in conductive loss through the ceiling plane at 71%, independently of area, climate zone and fuel price
→ the residual 29% is a hard floor, so no further depth beyond R-49 can recover more than a small fraction of what this one step already captures
→ the attic measure's physical benefit is bounded and computable from R-values alone, leaving the attic's share of total house loss as the only genuinely open quantity
```

*Weakest link:* the R-1.5 air-film allowance is a standard value, not a measured one. Varying it between R-1.0 and R-2.0 moves the result only between 70.5% and 72.0%, so the conclusion is insensitive to it.

**C3 — the measured window payback. Confidence: HIGH.**

```text
GT-7 (DOE measures $71 to $501 a year for ENERGY STAR window replacement) + GT-3 (window quote $18,500)
→ DOE's measured range is stated against whole-household energy bills and against exactly the kind of old windows a 1948 house carries
→ triple-pane sits at or a little above the top of that range, so $250 to $550 a year is already a generous reading for this house
→ dividing $18,500 by $550 gives 34 years, and dividing it by $250 gives 74 years
→ the quoted window replacement pays back in roughly 34 to 74 years, three to seven times the horizon the household actually stated
```

*Weakest link:* GT-7's range is measured against ENERGY STAR double-pane, not triple-pane. Hop 2 handles this by taking the top of the range and extending above it — a bias deliberately set in the windows' favour.

**C4 — payback against service life. Confidence: MEDIUM.**

```text
C3 (window payback of 34 to 74 years) + GT-12? (insulating glass unit service life of 20 to 25 years)
→ the sealed units would reach the end of their own service life well before the first payback cycle completed
→ lengthening the ownership horizon does not rescue the economics, because a second replacement falls due before the first has been repaid
→ the case against the $18,500 replacement is structural rather than a consequence of the ten-year figure the household happened to name
```

*Confidence caveat:* downgraded from HIGH by **GT-12?**. The OSTI abstract opened but stated no service life in years. What raises this to HIGH: the manufacturer's published seal warranty term for the specific product quoted, or a field-failure study naming a median IGU service life.

**C5 — the attic measure quantified. Confidence: MEDIUM.**

```text
GT-4? (attic and windows together account for 35% of loss) + GT-13? (the four coldest months carry 65% to 75% of annual degree days) + C2 (R-13 to R-49 removes 71% of ceiling-plane loss)
→ the two assemblies' conductances bound the attic's share of that 35% between 23% and 54% of it, or 8% to 19% of total house loss [Assumes: attic floor area between 800 and 1,600 square feet and glazing near 210 square feet]
→ removing 71% of the attic's loss therefore saves 6% to 13% of total heating energy, centrally about 9%
→ annual heating spend is $1,600 to $2,700 once the shoulder season is counted, so the saving is $90 to $356 a year, centrally near $196
→ the $4,200 quote returns roughly $900 to $3,600 over ten years against $4,200 spent, so it does not repay itself inside the stated horizon either
→ the attic case therefore turns entirely on the accuracy of the 35% figure, which a blower-door and infrared audit measures directly for a few hundred dollars
```

*Confidence caveat:* downgraded from HIGH by **GT-4?** (the 35% figure, origin unstated) and **GT-13?** (degree-day share, climate zone not supplied). What raises this to HIGH: a blower-door-plus-infrared audit reporting the attic plane's own measured share of loss, and the local heating-degree-day distribution from an NOAA climate normals table.

**C6 — the package the question excluded. Confidence: HIGH.**

```text
GT-8 (DOE sequences insulating and air sealing ahead of window replacement) + GT-9 (EPA measures $350 a year from low-e storms over single-pane clear glass) + GT-10 (EPA measures only $50 a year where clear storms already hang) + GT-11 (EPA measures 15% of heating and cooling from air sealing combined with attic insulation)
→ EPA's 15% figure prices a bundle whose cheapest component is air sealing rather than added insulation depth, and the quoted $4,200 scope contains no air sealing at all
→ the storm-window return is conditional rather than universal, worth $350 a year over bare single-pane glass but only $50 a year where clear storms are already fitted
→ DOE's own published sequencing puts insulating and air sealing ahead of window replacement, which is the reverse of the order these two quotes invite
→ the highest-return package available to this house is attic air sealing plus insulation plus storm windows or interior inserts, which is not one of the four options the question offered
→[2nd] burying a 1948 attic under fourteen inches of loose fill conceals knob-and-tube wiring, non-IC-rated recessed fixtures and bath fans terminating in the attic, each of which must be found before the fill goes down
→[2nd] a lower heating load makes an already-oversized furnace more oversized relative to demand, increasing short-cycling
→[3rd] a reduced design heating load lets a future heat pump be specified smaller and cheaper, making the attic work an enabling investment rather than a standalone energy trade [Assumes: heating fuel and appliance efficiency stay constant over the horizon]
→[3rd] $18,500 committed to windows is $18,500 unavailable for a heating-plant upgrade, which acts on all of the heating load rather than the fifth of it the windows touch
```

*Weakest link:* GT-9's $350 is a national average against an average bill. This household's bill is above average, so the figure is conservative for them — but only in the single-pane-without-storms branch. GT-10 bounds the opposite branch at $50, and A5 records which branch applies as unverified.

*Second-order check:* no extension step contradicts a ground truth, so no return to Phase 2 was triggered.

---

## 5. Abandoned Reasoning

**Tried:** recovering the attic-versus-window split directly from the 35% figure.
**Why abandoned:** 35% is a sum; the split is not recoverable from it. No arithmetic on a total yields its parts.
**What it ruled out:** any point estimate of the insulation saving. Replaced with the conductance-ratio bracket in C5 hop 1, which is why C5 reports a range rather than a number.

**Tried:** crediting DOE's measured resale recoup — "On average, homeowners recoup about 78% of the cost when the home is sold" (DOE/EE-0352, p.2, read at source) — against the $18,500 to rescue the window economics.
**Why abandoned:** the figure is measured at resale shortly after the project and decays as the windows age; at a ten-year-plus hold it is materially lower. More decisively, a recoup below 100% is a loss whichever way it is booked.
**What it ruled out:** the "windows pay for themselves at resale" argument, which is the most common counter to C3 and does not survive contact with the 78% figure itself.

**Tried:** applying EPA's 15% figure (GT-11) directly as the insulation saving.
**Why abandoned:** it prices a bundle — air sealing *plus* attic *plus* crawlspace *plus* rim joists — considerably wider than the quoted scope. Using it would have overstated the $4,200 quote's return by roughly 60%.
**What it ruled out:** the shortcut of treating a published programme figure as a project figure. It also produced the analysis's most useful finding, since the gap between the bundle and the quote *is* the missing air sealing.

**Tried:** recommending "neither" on a strict ten-year net-present-value test, which C5 arguably supports.
**Why abandoned:** it treats the ten-year floor as a ceiling, contradicting A8, and it ignores that the insulation's service life is roughly five times its payback while the windows' is shorter than theirs.
**What it ruled out:** a symmetric rejection of both quotes. The two measures fail differently — one on horizon, one on structure — and that asymmetry is the whole answer.

---

## 6. Conclusion

Overall confidence: **MEDIUM**, set by C5, the weakest chain contributing to it.

**Recommended approach:** Do the attic this year but not as quoted, decline the windows outright, and reject "neither" as a standing position — the winning package is attic air sealing plus insulation plus storm windows, which was not among the four options offered (chain C6).

1. Decline the $18,500 window replacement: it pays back in roughly 34 to 74 years, and even eliminating 100% of the winter heating bill could not repay it inside 11.3 years (chain C1).
2. Re-bid the attic as an air-sealing-plus-insulation package rather than the insulation-only scope quoted, since air sealing is the cheapest component of the measured 15% bundle and is entirely absent from the $4,200 (chain C6).
3. Establish whether the windows are single-pane without storms before pricing anything: that branch is worth $350 a year in low-e storms at roughly a quarter of replacement cost, while the already-stormed branch is worth about $50 (chain C6).

**Key insight:** The window quote is disqualified by division, before any energy model, climate data or split of the 35% is needed — the entire four-month heating bill is $1,640, so $18,500 cannot clear ten years even under the physically impossible assumption that the windows eliminate all winter heating (chain C1).

**Trade-offs acknowledged:** The attic work does not repay itself inside ten years either on the numbers available — roughly $900 to $3,600 returned against $4,200 spent — which is why a measured audit should precede the contract rather than follow it (chain C5).

*Caveat qualifying the above:* the single input whose correction would most change this recommendation is the 35% figure itself (GT-4?, chain C5); a second, weaker one is insulating-glass service life, which if confirmed at 20–25 years would make the window rejection structural rather than horizon-dependent (chain C4).

---

# Process output

## Assumption Audit (end of Phase 4)

| Chain | Step | Step Text (brief) | Assumption surfaced? | Added to Table? |
|---|---|---|---|---|
| C1 | 1 | four-month spend is the hard ceiling | none — A3 already in table | n/a |
| C1 | 2 | 11.3 years and 13.8 years by division | none | n/a |
| C1 | 3 | neither measure touches plant or envelope | no competing claim on the $22,700 | yes → A13 |
| C1 | 4 | windows and both disqualified by division | none | n/a |
| C2 | 1 | R-14.5 before, R-50.5 after | none — A7 already in table | n/a |
| C2 | 2 | ratio fixes reduction at 71% | none — A1 already in table | n/a |
| C2 | 3 | residual 29% is a hard floor | none | n/a |
| C2 | 4 | benefit bounded by R-values alone | none | n/a |
| C3 | 1 | DOE range against old windows | none — A5 already in table | n/a |
| C3 | 2 | triple-pane at or above range top | none — A11 already in table | n/a |
| C3 | 3 | 34 years and 74 years by division | none | n/a |
| C3 | 4 | payback three to seven times the horizon | none — A8 already in table | n/a |
| C4 | 1 | units reach end of life before payback | none — GT-12? carries the flag | n/a |
| C4 | 2 | longer horizon does not rescue economics | none — A8 already in table | n/a |
| C4 | 3 | case is structural, not horizon-dependent | none | n/a |
| C5 | 1 | conductances bound attic share 23–54% | attic 800–1,600 sq ft, glazing ~210 sq ft | yes → A14 |
| C5 | 2 | saves 6–13% of heating energy | none — A7 already in table | n/a |
| C5 | 3 | annual spend $1,600–$2,700 | none — A3, A4 already in table | n/a |
| C5 | 4 | returns $900–$3,600 over ten years | none | n/a |
| C5 | 5 | case turns on the 35% figure | none — A2 already in table | n/a |
| C6 | 1 | 15% bundle's cheapest part is air sealing | none — A10 already in table | n/a |
| C6 | 2 | storm return conditional, $350 vs $50 | none — A5 already in table | n/a |
| C6 | 3 | DOE sequencing reverses the quotes' order | none | n/a |
| C6 | 4 | winning package not among the four options | none — A9 already in table | n/a |
| C6 | 5 [2nd] | loose fill conceals K&T and fixtures | none — A6 already in table | n/a |
| C6 | 6 [2nd] | oversized furnace short-cycles more | none | n/a |
| C6 | 7 [3rd] | smaller heat pump becomes specifiable | fuel and appliance efficiency stay constant | yes → A15 |
| C6 | 8 [3rd] | $18,500 unavailable for plant upgrade | none — A13 covers it | n/a |

## §6→§4 closure ledger

```text
- "Do the attic this year but not as quoted, decline the windows outright, and reject 'neither'…" → chain C6 ✓
- "Decline the $18,500 window replacement: it pays back in roughly 34 to 74 years…" → chain C1 ✓
- "Re-bid the attic as an air-sealing-plus-insulation package…" → chain C6 ✓
- "Establish whether the windows are single-pane without storms before pricing anything…" → chain C6 ✓
- "The window quote is disqualified by division, before any energy model…" → chain C1 ✓
- "The attic work does not repay itself inside ten years either on the numbers available…" → chain C5 ✓
```

Six claims, six chains cited, zero cuts.

## Self-audit scan (process output)

| Chain | Chain Head (brief) | Form conforming? | Rule applied | Dependency clean? |
|---|---|---|---|---|
| C1 | GT-1 + GT-2 + GT-3 + GT-5 | yes | n/a | yes |
| C2 | GT-6 + GT-2 | yes | n/a | yes |
| C3 | GT-7 + GT-3 | yes | n/a | yes |
| C4 | C3 + GT-12? | yes | n/a | yes |
| C5 | GT-4? + GT-13? + C2 | yes | n/a | yes |
| C6 | GT-8 + GT-9 + GT-10 + GT-11 | yes | n/a | yes |

| §6 Span (brief) | Construct | Claim under R11? | R11 clause applied | Chain cited |
|---|---|---|---|---|
| "Overall confidence: MEDIUM, set by C5…" | prose | no | prose carrying neither a bold colon lead-in nor a list marker | n/a |
| "**Recommended approach:** Do the attic this year…" | bold lead-in | yes | prescribed lead-in whose colon closes the bold span; always a claim | C6 |
| "1. Decline the $18,500 window replacement…" | list item | yes | list item closing its own sentence and past forty characters | C1 |
| "2. Re-bid the attic as an air-sealing-plus-insulation package…" | list item | yes | list item closing its own sentence and past forty characters | C6 |
| "3. Establish whether the windows are single-pane…" | list item | yes | list item closing its own sentence and past forty characters | C6 |
| "**Key insight:** The window quote is disqualified by division…" | bold lead-in | yes | prescribed lead-in whose colon closes the bold span | C1 |
| "**Trade-offs acknowledged:** The attic work does not repay itself…" | bold lead-in | yes | prescribed lead-in whose colon closes the bold span | C5 |
| "*Caveat qualifying the above:* the single input whose correction…" | prose | no | prose carrying neither a bold colon lead-in nor a list marker; caveat naming C5 and C4 inline under R12 | n/a |

```text
Scan complete: 6 chain rows, one per section-4 chain block in order; 8 section-6 rows, one per construct in order — 6 claims under R11, 2 excluded. 0 chains malformed, 0 claims untraced.
```

---

# Self-Audit Gate

**Criterion 1: Identify Essence**
Quoted span: "Which allocation of this year's improvement budget buys the most avoided heating cost per dollar over a holding period of *at least* ten years — a capital-allocation question about a shared pool of heat loss, not a question about which of two quotes is the better product."
Band: **Rigorous**
Justification: a single sentence naming the underlying decision rather than the triggering event (receipt of two quotes), followed by four success criteria each carrying a verb-subject-outcome test applied by scanning section 6, and specific enough that it could not appear unmodified in a different analysis.

**Criterion 2: Challenge Assumptions**
Quoted span: from the Assumption Audit scan — "C5 | 1 | conductances bound attic share 23–54% | attic 800–1,600 sq ft, glazing ~210 sq ft | yes → A14"
Band: **Rigorous**
Justification: all fifteen rows draw Type from exactly the four-type scheme, every Verdict cell leads with Accept, Challenge or Discard followed by an em-dash and a specific justification, four assumptions carry Discard verdicts rather than uniform acceptance, every chain-consumed unverified assumption reads "unverified — flagged", and the audit scan covers all 28 chain steps in order with three genuinely new assumptions recorded back into the table.

**Criterion 3: Establish Ground Truths**
Quoted span: "`?`-marked, enumerated by ID: **GT-4, GT-12, GT-13** (3 of 13)" — checked against the list, which carries `?` on exactly GT-4, GT-12 and GT-13 and on no others.
Band: **Rigorous**
Justification: the enumeration matches the suffixed entries when read back against the list; every unsuffixed GT carries a provenance label and a read-location (GT-7 at DOE/EE-0352 p.1 left column, GT-11 at the ENERGY STAR savings methodology headline, and so on); every unsuffixed GT with a reachable source feeds a HIGH chain (GT-1/2/3/5→C1, GT-6→C2, GT-7→C3, GT-8/9/10/11→C6); GT-12? carries a Phase 3 failure record naming the OSTI source and the reason *citation does not support the claim*; and no Phase 2 Discard appears in the list.

**Criterion 4: Reason Upward**
Quoted span: from the self-audit scan chain-form table — "C5 | GT-4? + GT-13? + C2 | yes | n/a | yes", with all six rows conforming and dependency-clean.
Band: **Rigorous**
Justification: every conclusion has exactly one chain in the prescribed head-plus-arrow-led form with one hop per physical line and at least one genuine intermediate; Abandoned Reasoning documents four dead ends in What-was-tried / Why-abandoned / What-it-ruled-out structure; no analogy is offered as direct evidence — the DOE and EPA figures are named ground truths, not appeals to what others did; and the three audit-surfaced assumptions carry inline `[Assumes: X]` marks on C1 hop 3, C5 hop 1 and C6's first third-order hop.

**Criterion 5: Validate**
Quoted span: "**Trade-offs acknowledged:** The attic work does not repay itself inside ten years either on the numbers available — roughly $900 to $3,600 returned against $4,200 spent (chain C5)."
Band: **Sound**
Justification: every chain names its weakest link and every `GT-N?` input in a load-bearing chain carries a caveat naming the input and the verification that would raise it to HIGH, and no chain consuming a `?` input is rated HIGH — but exactly one Conclusion claim rests on a chain that is not HIGH (Trade-offs, on the MEDIUM C5), which the descriptor bands Sound rather than Rigorous. No EXCEPT clause is claimed.

**Criterion 6: Conclusion-to-Ground-Truth Traceability**
Quoted span: from the self-audit scan claim-inventory table — six claim rows, each carrying a chain id, none reading "none — untraced"; and from the analysis text, the Key Insight "The window quote is disqualified by division, before any energy model, climate data or split of the 35% is needed."
Band: **Rigorous**
Justification: all six claims trace to named section-4 chains, no claim introduces reasoning absent from section 4, and the Key Insight names a non-obvious finding — that the arithmetic ceiling settles the window question before any of the disputed inputs matter — rather than restating the recommended approach, which is about which package to buy.

**Gate result:** no criterion Absent; one criterion at Hand-wavy permitted, zero used. **Gate cleared** on the first pass; no re-perception pass was needed or fired.

---

## What I'd tell you in one paragraph

The windows are a clear no, and you don't need to trust any of my modelling to see it: your entire four-month heating bill is $1,640, so $18,500 couldn't repay itself in ten years even if the windows eliminated *all* of your winter heating. Realistically they'd save $250–$550 a year — a 34-to-74-year payback on glass that likely won't last that long. The attic is the right target but the quote is the wrong shape: it's insulation-only, and the cheapest, highest-yield part of attic work is *air sealing* the ceiling plane, which isn't in there. On the numbers available the $4,200 as quoted returns about $900–$3,600 over ten years, so it's marginal too — which is why the $300–600 for a blower-door-and-infrared audit is the actual best first dollar: it replaces that unverified "35%" with a measured number, tells you whether there's knob-and-tube up there (a real risk in a 1948 house that you must know about *before* burying the attic under 14 inches of cellulose), and tells you what your windows actually are. If they turn out to be bare single-pane, low-e storm windows are worth about $350/year at roughly a quarter of replacement cost. DOE's own guidance says it plainly: insulate and air seal *before* you replace windows.

**Sources read:** [DOE Guide to Energy-Efficient Windows (DOE/EE-0352)](https://www.energy.gov/sites/prod/files/guide_to_energy_efficient_windows.pdf) · [ENERGY STAR Storm Windows](https://www.energystar.gov/products/storm_windows_0) · [ENERGY STAR Seal & Insulate methodology](https://www.energystar.gov/saveathome/seal_insulate/methodology)