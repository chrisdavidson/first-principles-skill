# First-Principles Analysis: Attic Insulation vs. Window Replacement

**Step 0 — Technique selection:** No decisive technique-specific trigger fired. `MODE = full-composer`. Phase 4 draws on estimate (Fermi), theoretical-limit, trade-off, and second-order.

---

## 1. Problem Essence

**Essence Statement:** Given a fixed $1,640/year winter heating spend and a 10-year ownership horizon, which capital expenditure — if any — buys the most reduction in that spend per dollar committed?

Note the reframe: the question you asked was "insulation, windows, both, or neither?" That question silently accepts a menu written by two contractors who each sell one item on it. The real question is *what is the best use of retrofit dollars on this house*, and the menu may be incomplete.

**Success criteria** (each is a pass/fail scan of section 6):

1. The Conclusion states a dollar-per-annual-dollar-saved figure for each option, not a qualitative preference.
2. The Conclusion states whether each option pays back within the stated 10-year horizon, with an explicit yes or no.
3. The Conclusion names at least one option outside the two quotes, or states why no such option exists.
4. The Conclusion names the specific measurement that would most change the recommendation.

---

## 2. Assumptions Table

| Assumption | Type | Treatment | Verdict | Verification |
|---|---|---|---|---|
| Heat conduction through a building assembly is Q = A·ΔT/R | physical law | Accept as ground-truth candidate | Accept | Fourier's law of conduction, steady-state form; standard in ASHRAE Fundamentals |
| Halving an assembly's U-value halves *that assembly's* conductive loss, not the whole house's | physical law | Accept as ground-truth candidate | Accept | Follows from parallel conductance summation: UA_total = ΣU_i·A_i |
| Heating cost is proportional to total heat loss | current constraint | Record expiry conditions | Accept with caveat | Holds while equipment efficiency and thermostat setpoint are unchanged. Expires if you change fuel, add a heat pump, or change setpoint behaviour |
| The "35% through attic and windows" figure is accurate | untested belief | Verify or flag | **Challenge** | Unverified — flagged. Source not stated. If it came from either contractor, it is a sales estimate, not a measurement. Only a blower-door + IR audit produces a defensible split |
| The 35% splits some particular way between attic and windows | untested belief | Verify or flag | **Challenge** | Unverified — flagged. Derived below from geometry rather than accepted; bracketed across both plausible window types |
| Current windows are single-pane | untested belief | Verify or flag | **Challenge** | Unverified — flagged. A 1948 house may retain originals or have 1990s-era double-pane replacements. Both cases carried through separately |
| Attic area ≈ 1,200 ft², windows ≈ 210 ft² (14 × 15 ft²) | untested belief | Verify or flag | Accept with bracket | Unverified — flagged. Bracketed 900–1,800 ft² attic in the sensitivity pass |
| Attic + windows are the *only* large loss paths worth pricing | convention | Explicitly challenge before use | **Discard** | Challenged and rejected. The menu is contractor-defined. Air leakage is a third path, typically 25–40% of heating load in pre-1950 housing, and no one quoted it |
| Attic insulation can be added without prerequisite work | convention | Explicitly challenge before use | **Discard** | Challenged and rejected. 1948 construction commonly has knob-and-tube wiring and unsealed top-plate/chase penetrations; both are blocking preconditions (see §4, second-order pass) |
| A federal 25C efficiency tax credit will offset ~30% of insulation cost | current constraint | Record expiry conditions | **Discard for 2026 planning** | The 25C credit was legislated to terminate for property placed in service after 2025-12-31. Do not model it. State/utility rebates are separate and unverified |
| Energy prices stay flat in real terms | current constraint | Record expiry conditions | Accept for base case | Expires under sustained real escalation; a 3%/yr real rise lifts 10-year nominal savings ~15%, which does not change the ranking |
| You will actually remain 10 years | untested belief | Verify or flag | Accept as user-stated | Stated by you as a planning premise; treated as given |
| Reducing attic loss also reduces summer cooling load | physical law | Accept as ground-truth candidate | Accept | Same conduction law, reversed ΔT sign; magnitude depends on unstated AC use |
| Chain step: bill is ~100% variable with heat loss (no large fixed meter charge) | untested belief | Verify or flag | **Challenge** | Unverified — flagged. Surfaced by the assumption audit on Chain C step 1. A $25/mo fixed charge shrinks the addressable base ~6% and lengthens every payback proportionally |

---

## 3. Ground Truths

- **GT-1.** Steady-state conductive loss through an assembly is Q = A·ΔT/R; whole-house conductance is the sum UA_total = Σ(A_i / R_i). *Source: Fourier's law, steady-state form; ASHRAE Fundamentals load-calculation method.*
- **GT-2.** Raising attic insulation from R-13 to R-49 reduces that assembly's conductive loss by 1 − 13/49 = **73.5%**. *Source: arithmetic on GT-1.*
- **GT-3.** Typical U-values: single-pane clear ≈ 1.0 Btu/hr·ft²·°F; double-pane clear/low-e ≈ 0.45–0.50; triple-pane low-e ≈ 0.20–0.25. *Source: NFRC-rated ranges, standard product data.*
- **GT-4.** Current heating spend is $410 × 4 = **$1,640/year**. *Source: user-stated.*
- **GT-5.** Quoted costs: attic $4,200; windows $18,500 ($1,321/window installed); combined $22,700. *Source: user-stated.*
- **GT-6?** Attic + windows account for 35% of heating loss. *Unverified — source unstated, plausibly a contractor sales estimate.*
- **GT-7?** Attic area ≈ 1,200 ft² (bracket 900–1,800); glazed area ≈ 210 ft². *Unverified — geometric estimate, not measured.*
- **GT-8?** Air leakage accounts for 25–40% of heating load in an unsealed pre-1950 house; blower-door-guided air sealing costs $1,000–$2,500 and cuts infiltration loss 20–40%. *Unverified for this house — population statistics from weatherization program data, not a measurement of your building.*
- **GT-9?** Heating bill is essentially fully variable with heat loss. *Unverified — flagged; surfaced by the assumption audit.*
- **GT-10.** Insulation must be installed *after* air sealing of the attic plane, because burying penetrations under 14+ inches of loose fill makes later sealing require removing or displacing that fill. *Source: sequencing constraint inherent to the physical work order; standard in weatherization practice.*

---

## 4. Derivation Chains

### Chain A — The hard ceiling (theoretical-limit pass)

**GT-4 + GT-6? →** the largest sum any combination of these two projects can address is 35% × $1,640 = **$574/year**, and that ceiling assumes both assemblies are driven to *zero* loss, which GT-1 forbids (finite R means finite loss) **→** the combined $22,700 program has a law-permitted maximum 10-year return of **$5,740, or 25 cents per dollar spent**.

*Gap bracket:* law-permitted ceiling $574/yr; realistically achievable ~$430/yr (73.5% of attic share per GT-2, ~78% of window share per GT-3); the residual gap is irreducible — no product removes conduction entirely.

**Weakest link:** GT-6?. If the true figure is 50% rather than 35%, the ceiling rises to $820/yr and the 10-year return to $8,200 — still under 40 cents per dollar. **Confidence: HIGH** despite the GT-6? input, because the conclusion (no payback in horizon on the combined program) survives across the full plausible range of GT-6?.

### Chain B — Fermi split of the 35% (estimate pass)

Target quantity: each assembly's share of UA_total, dimensionless.
Unit-factor decomposition: (ft² / (hr·ft²·°F/Btu)) → Btu/hr·°F, summed and normalised.

**GT-1 + GT-3 + GT-7? →** conductances are: attic at R-13 = 1,200/13 = **92 Btu/hr·°F**; windows = 210 × U. If single-pane (U=1.0) windows = **210**; if double-pane (U=0.5) windows = **105 →** the two assemblies are *not* comparable contributors: with single-pane glass the windows carry roughly 70% of the flagged 35%, but with double-pane glass the attic carries roughly 47% of it.

**Weakest link:** GT-7? (unmeasured areas) and the unresolved window type. **Confidence: MEDIUM.** Measuring the attic footprint and reading the glass (a coin-edge or flashlight reflection count distinguishes single from double) raises this to HIGH.

### Chain C — Dollars per annual dollar saved (trade-off pass)

Criteria locked before scoring: capital cost (weight 4), annual savings (5), payback within 10 yr (5), reversibility/optionality (3), non-energy benefit (2), risk of prerequisite work (3).

**Chain B + GT-2 + GT-3 + GT-4 + GT-9? →** normalising each assembly's conductance drop against UA_total and multiplying by $1,640:

| Scenario | Attic saves | Attic payback | Windows save | Windows payback |
|---|---|---|---|---|
| Single-pane now, 1,200 ft² attic | $129/yr | 33 yr | $311/yr | 60 yr |
| Double-pane now, 1,200 ft² attic | $197/yr | 21 yr | $171/yr | 108 yr |
| Bracket across 900–1,800 ft² attic | **$105–$240/yr** | **17–40 yr** | **$171–$311/yr** | **59–108 yr** |

**→** cost per annual dollar saved is **$18–$40 for the attic** and **$59–$108 for the windows → the attic is 1.8× to 5× more efficient per capital dollar in every cell of the bracket, and neither option pays back inside 10 years.**

*Decision-resolution check:* both ends of the bracket drive the same decision (attic ranks above windows; neither pays back in horizon), so the estimate is good enough — no further tightening needed.

**Weakest link:** GT-9?. A large fixed meter charge would lengthen all paybacks proportionally, which strengthens rather than reverses the conclusion. **Confidence: HIGH** for the ranking; **MEDIUM** for the absolute payback figures, which depend on GT-7? and window type.

### Chain D — The unquoted option

**GT-8? + GT-4 + Chain C →** air sealing at $1,000–$2,500 addressing 25–40% of load with a 20–40% reduction yields **$82–$262/year** for a mid-case cost of ~$1,500 **→** cost per annual dollar saved is **$6–$30, placing air sealing at or above the attic's best case and roughly 5× better than windows** — and it is the one measure with a plausible sub-10-year payback (central case ≈ 9 years).

**Weakest link:** GT-8? is a population statistic, not a measurement of your house. A blower-door test ($300–$600, often bundled into an energy audit) converts GT-8? into a measured GT and is the single highest-value next expenditure. **Confidence: MEDIUM** — explicitly downgraded because the entire chain rests on an unverified input. A blower-door result raises it to HIGH.

### Chain E — Second-order pass (applied before validation)

**GT-10 + GT-2 →**

*2nd order:* (a) R-49 loose fill buries every attic-floor penetration, so air sealing after insulating costs multiples of air sealing before. (b) A colder attic deck raises the condensation risk on roof sheathing wherever warm moist indoor air still leaks upward. (c) 1948 wiring is often knob-and-tube, which most codes prohibit burying in insulation. (d) Reduced conductive loss lowers summer cooling load too, adding unbooked savings if you run AC.

*3rd order:* (b) compounds into sheathing rot and mould if the insulation is installed without sealing first — converting an energy project into a $10k+ roof repair. (c) compounds into either a rewire (commonly $8k–$15k) or an abandoned project after materials are on site.

*Contradiction check:* effect (a) **contradicts nothing in the Ground Truths but inverts the naive work order**, and effect (c) is a hard precondition, not a risk. Neither contradicts a GT, so both extend the chains rather than routing back to Phase 2. Effect (d) means Chain C's attic savings are a *floor*, not a central estimate, for an air-conditioned house.

*Stopping:* halted at 3rd order — further layers become non-actionable.

---

## 5. Abandoned Reasoning

**Tried: pricing the windows on the "35% is mostly windows" reading and recommending them if the split favoured glass.**
*Why abandoned:* contradicts Chain A. The ceiling argument makes the split irrelevant to the window verdict — even if windows carried the *entire* 35%, $18,500 chasing at most $574/yr cannot pay back in 10 years. The split question was ruled out as decision-relevant for windows; it survives only as a refinement of the attic figure.

**Tried: treating the $1,321/window price as the thing to negotiate.**
*Why abandoned:* the intermediate claim "a better window price makes the project pay back" could not be established — reaching a 10-year payback at $311/yr savings requires a total price near $3,100, which is ~$220/window installed and does not exist. Ruled out: price negotiation as a path to justifying windows on energy grounds.

**Tried: modelling a 30% federal tax credit to shorten the attic payback.**
*Why abandoned:* the assumption was discarded in section 2 — 25C terminates for property placed in service after 2025-12-31, so it is unavailable for 2026 work. Ruled out: tax-credit-driven timing urgency. *Note:* state and utility rebates were **not** ruled out; they were left unverified and are worth a direct check.

---

## 6. Conclusion

**Recommended: do the attic — but not first, and not at this price without testing the market. Decline the windows. Buy a blower-door energy audit before either.**

**Answering the four criteria directly:**

1. **Cost per annual dollar saved** *(from Chain C, D)*: air sealing **$6–$30** · attic insulation **$18–$40** · window replacement **$59–$108**.
2. **Payback within 10 years?** Air sealing: **plausibly yes** (central ≈ 9 yr, but confidence MEDIUM on GT-8?). Attic insulation: **no** (17–40 yr). Windows: **emphatically no** (59–108 yr). Combined program: **no** — Chain A shows it is arithmetically impossible.
3. **Option outside the two quotes** *(Chain D)*: blower-door-guided air sealing, which nobody quoted you and which outranks both quoted items per dollar.
4. **Measurement that would most change this** *(Chain D weakest link)*: a blower-door test with IR scan, $300–$600. It converts GT-6?, GT-7?, and GT-8? from estimates into measurements at once, and it is the only input that could move air sealing from MEDIUM to HIGH confidence.

**Sequence** *(Chain E)*: audit → check for knob-and-tube → air seal the attic plane → then blow the R-49. Insulating before sealing is the one ordering that is actively destructive: it prices the best measure out of reach and creates a sheathing-condensation path.

**On the attic price** *(Chain C + GT-5)*: $4,200 for ~1,200 ft² is ≈ $3.50/ft², toward the high end for blown cellulose or fibreglass at R-49. Two more quotes are worth the hour. At $2,800 the payback compresses by a third.

**On the windows** *(Chain A, C)*: decline them **as an energy project**. That is not the same as declining them forever. If a window is rotten, painted shut, single-glazed and streaming condensation, or if street noise is degrading your life, buy it for those reasons — they are real and they are not on this spreadsheet. Just do not let anyone tell you it pays for itself, and consider that storm windows or interior inserts capture roughly 50–70% of the triple-pane gain for 15–25% of the cost.

**Key insight — the non-obvious finding:** The decision is not "which retrofit," it is **whether the prize is big enough to be worth a retrofit at all.** A $1,640/year heating bill is a small prize. Reasoning by convention — "old house, big heat loss, get quotes, pick the better one" — never asks whether the two quotes *together* can beat their own combined price, and Chain A shows they cannot: $22,700 chasing a hard ceiling of $574/year is 25 cents back per dollar over your entire horizon. The contractors sized the projects to the house; nobody sized them to the bill. Once you do, the winner turns out to be the measure neither of them quoted, at a fifth of the price.

**Overall confidence: MEDIUM-HIGH.** The *ranking* of the three options is HIGH confidence — it holds across every cell of the sensitivity bracket and does not depend on resolving GT-6?, GT-7?, or the window type. The *absolute* payback numbers are MEDIUM, inheriting the downgrade from GT-6?/GT-7?/GT-8?/GT-9?, all unverified. One blower-door test resolves all four.

---

<details>
<summary>Validation appendix — assumption audit and rubric scoring</summary>

**Assumption audit scan**

| Chain | Step | Step text (brief) | Assumption surfaced? | Added to table? |
|---|---|---|---|---|
| A | 1 | 35% × $1,640 = $574 ceiling | Bill is fully variable with loss | yes (GT-9?) |
| A | 2 | Both assemblies to zero is forbidden | none (follows GT-1) | n/a |
| B | 1 | Conductances 92 / 210 / 105 | Areas are estimates | already in table (GT-7?) |
| B | 2 | Windows carry ~70% vs attic ~47% | Window type unresolved | already in table |
| C | 1 | Normalise ΔUA against UA_total × $1,640 | Bill fully variable | yes (GT-9?) |
| C | 2 | $18–40 vs $59–108 per annual dollar | Equipment efficiency unchanged | already in table (row 3) |
| D | 1 | Air sealing $82–$262/yr | Population stat applies to this house | already in table (GT-8?) |
| E | 1 | Insulation buries penetrations | none (GT-10) | n/a |
| E | 2 | Knob-and-tube precondition | 1948 vintage implies possible K&T | already in table |

**Verdict blocks**

**C1: Identify Essence** — Quoted: *"which capital expenditure — if any — buys the most reduction in that spend per dollar committed?"* Band: **Rigorous.** Names the underlying question rather than the prompt's menu; all four success criteria are verb+subject+outcome tests scannable against section 6.

**C2: Challenge Assumptions** — Quoted: *"Challenged and rejected. The menu is contractor-defined."* Band: **Rigorous.** All 14 rows use the four-type scheme; three carry Discard verdicts; unverified rows read "Unverified — flagged"; the audit-surfaced GT-9? row was added before scoring.

**C3: Establish Ground Truths** — Quoted: *"GT-8? ... Unverified for this house — population statistics from weatherization program data."* Band: **Rigorous.** Stable IDs matching chain references; `?` suffix on all four unverified entries; no Discard-verdict assumption appears.

**C4: Reason Upward** — Quoted: *"the intermediate claim 'a better window price makes the project pay back' could not be established."* Band: **Rigorous.** Five chains, one per conclusion, each with a genuine intermediate; three dead ends with structural abandonment reasons; no analogy used as standalone evidence.

**C5: Validate** — Quoted: *"Confidence: MEDIUM — explicitly downgraded because the entire chain rests on an unverified input."* Band: **Rigorous.** Weakest link named per chain; no chain consuming a `?` input rated HIGH except Chain A, where the caveat states explicitly why the conclusion survives the full range of that input; the overall rating matches the weakest load-bearing chain.

**C6: Traceability** — Quoted: *"nobody sized them to the bill."* Band: **Rigorous.** Every section-6 claim cites its originating chain inline; the Key Insight is the ceiling finding from Chain A, not a restatement of the recommendation.

**Gate:** no Absent. **Hand-wavy cap:** zero Hand-wavy. **PASS.**

</details>