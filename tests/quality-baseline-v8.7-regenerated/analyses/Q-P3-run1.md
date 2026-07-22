## 1. Problem Essence

**Core question:** Which of these two capital expenditures, if either, returns more value than it costs over a ≥10-year hold — where "value" is dollars saved on heat *plus* comfort and durability?

The triggering framing ("insulation, windows, both, or neither") is a false binary in two places, and the analysis has to break both open before answering:

1. It treats each project as fixed-scope at a fixed price. The prices are quotes, not costs.
2. It omits the two interventions that dominate this cost class — **attic air sealing** and **interior low-e storm windows** — neither of which is in either quote.

**Success criteria for a correct answer:**
- Attributes the 35% loss between the two paths rather than treating it as one pool.
- Converts each intervention to $/year saved, with an explicit uncertainty bracket.
- Compares against the 10-year horizon, not an unbounded one.
- States which assumption, if wrong, flips the recommendation.

---

## 2. Assumptions Table

| # | Assumption | Type | Treatment | Verdict |
|---|---|---|---|---|
| A1 | Heat loss through an assembly is inversely proportional to its R-value | physical law | Accept | → GT-1 |
| A2 | The "35%" is a measured figure | untested belief | **Challenge** | **Unverified — flagged.** If it came from the window contractor rather than a blower-door/thermal audit, it is a sales figure. Window vendors routinely overstate the window share. |
| A3 | The 35% splits evenly between attic and windows | untested belief | Challenge | **Rejected.** The split is derivable from area × U and is nowhere near even. See GT-8. |
| A4 | $410/month is all heating | untested belief | Challenge | **Rejected as stated.** It includes baseload (lights, hot water, appliances). Heating-attributable share bracketed at 70–100%. |
| A5 | $4,200 is the market price for R-13→R-49 blown-in | convention | **Challenge** | **Failed challenge.** Blown-in cellulose/fiberglass to R-49 typically runs $1.50–$2.50/ft². For a ~1,300 ft² attic that is $2,000–$3,250. **This quote is ~30–100% above range** unless it bundles air sealing, deck baffles, or difficult access. |
| A6 | Triple-pane is the relevant window upgrade | convention | Challenge | **Rejected as the only option.** Interior low-e storm panels capture roughly half the U-value improvement for ~10–20% of the cost. |
| A7 | The 30% federal 25C credit is available | current constraint | Record expiry | **Expired.** 25C was terminated for property placed in service after 2025-12-31. In July 2026 there is no federal credit to model. **Verify against your state/utility programs — those are what remain.** |
| A8 | Existing windows are single-pane | untested belief | Verify | **Unverified — flagged.** A 1948 house may have originals (U≈1.0) or a 1990s double-pane retrofit (U≈0.5). This changes the window share materially; both branches carried below. |
| A9 | House stays occupied by you ≥10 years | given ground truth | Accept | → GT-7 |

---

## 3. Ground Truths

- **GT-1** — Conductive loss Q = A·ΔT/R. *(Fourier's law; physical law.)*
- **GT-2** — R-13→R-49, including ~R-2 of air films and framing, cuts conduction through the attic plane by **1 − (15/51) ≈ 71%**. *(Arithmetic on GT-1.)*
- **GT-3** — NFRC U-factors: clear single pane ≈ 1.04; clear double ≈ 0.49; modern triple low-e ≈ 0.18–0.22 Btu/hr·ft²·°F. *(Published measurement.)*
- **GT-4** — Attic quote: $4,200. *(Given.)*
- **GT-5** — Window quote: $18,500 / 14 = $1,321 per window. *(Given.)*
- **GT-6** — Winter bill $410 × 4 = **$1,640 per season, gross**. *(Given.)*
- **GT-7** — Horizon ≥ 10 years. *(Given.)*
- **GT-8?** — 35% of heating loss is via attic + windows combined. *(**Unverified** — provenance unknown, see A2.)*
- **GT-9** — Federal 25C credit unavailable for 2026 placements. *(Current constraint; verify locally.)*
- **GT-10?** — Assumed geometry: ~1,300 ft² attic, 14 windows × ~15 ft² = ~210 ft² glazing. *(**Assumed** — measure yours; the conclusion is not sensitive to ±30% here, but is sensitive to a 2× error.)*

---

## 4. Derivation Chains

### Chain A — Splitting the 35%

GT-1 + GT-3 + GT-10? → compute UA (area ÷ R) for each path →

| Path | Area | U | UA (Btu/hr·°F) |
|---|---|---|---|
| Attic @ R-15 effective | 1,300 | 0.067 | **87** |
| Windows, if single-pane | 210 | 1.04 | **218** |
| Windows, if double-pane | 210 | 0.49 | **103** |

→ **the split is not even, and it inverts depending on A8:**

- **Single-pane branch:** attic 29% / windows 71% of the 35% → attic **10 pts**, windows **25 pts** of total heating energy.
- **Double-pane branch:** attic 46% / windows 54% → attic **16 pts**, windows **19 pts**.

Confidence: MEDIUM (rests on GT-8? and GT-10?).

### Chain B — Attic insulation

Chain A + GT-2 → 71% of a 10–16 point share → **7–11% of total heating energy saved** → applied to GT-6 discounted for baseload (A4: $1,150–$1,640 heating-attributable) →

**Savings: $95–$185/yr, central ≈ $145/yr.**

GT-4 + that → **simple payback 23–44 years, central ≈ 29.** Over GT-7's 10 years, even with 3%/yr fuel escalation, cumulative savings ≈ **$1,650 against $4,200 spent — net −$2,550.**

Now re-run with A5's challenge — a market-rate $2,400 quote: payback ≈ 17 years, 10-year net ≈ **−$750**. Confidence: MEDIUM.

> **This is the load-bearing result.** Attic insulation is conventionally "obvious," and at *this quote and this bill* it does not pay back inside your horizon. What makes it obvious in general is a lower price and a bigger bill.

### Chain C — Triple-pane windows

Chain A + GT-3 → triple-pane cuts window loss by 80% (from single) or 60% (from double) → 20 pts × 0.80 = 16–20 points, or 19 × 0.60 = 11 points → **11–20% of heating energy** → applied to A4's bracket →

**Savings: $145–$310/yr, central ≈ $220/yr.**

GT-5 + that → **simple payback 60–128 years, central ≈ 84 years.** Ten-year net ≈ **−$16,100**. Confidence: **HIGH** — the gap is two full orders of magnitude wider than the uncertainty in GT-8?/GT-10?. Even if the 35% figure is doubled and the bill is entirely heat, windows still do not pay back within 30 years.

### Chain D — The options that were not quoted

GT-1 + A6 + the observation that a 1948 house's infiltration is typically 25–40% of heating load (outside GT-8?'s conduction accounting entirely) →

| Intervention | Cost | Est. savings/yr | Payback |
|---|---|---|---|
| **Attic air sealing** (top plates, chases, can lights) | $800–$1,500 | $80–$200 | **5–14 yrs** |
| **Interior low-e storm panels**, 14 windows | $1,400–$3,500 | $80–$160 | 12–30 yrs |
| Attic insulation @ market rate | $2,400 | $145 | 17 yrs |
| Attic insulation @ quote | $4,200 | $145 | 29 yrs |
| Triple-pane replacement | $18,500 | $220 | 84 yrs |

**Air sealing is the only line that pays back inside your horizon**, and it is in neither quote.

### Second-order pass

1. **Insulation without air sealing → moisture.** Burying a leaky ceiling plane under R-49 moves the dew point and drives warm indoor air into a now-colder attic. Consequences: condensation on sheathing, ice dams, and delivered R-value well below R-49. *This does not contradict a ground truth — it strengthens Chain D's ranking. Air sealing is a precondition for the insulation, not an alternative to it.*
2. **Whole-house tightening → ventilation.** Sealing plus new windows in a 1948 house can push air changes below ASHRAE 62.2 minimums; radon and humidity rise. At the scale recommended below, this stays below the threshold, but it is a real ceiling on how far to take envelope work without mechanical ventilation.
3. **Windows have a non-energy failure mode.** If sashes are rotted, cords broken, or glazing failed, replacement becomes a *maintenance* decision with an energy side-benefit — and should be judged on maintenance economics, where an $18,500 answer may well be correct. Chain C only rules windows out *as an energy investment*.
4. **Resale.** Attic insulation is largely invisible at sale and recoups poorly; windows recoup roughly 60–70% of cost in typical markets, which shortens the effective 10-year window loss from ~$16,100 to roughly ~$6,000 — still the worst option on this list.

No second-order effect contradicts a ground truth.

---

## 5. Abandoned Reasoning

- **"Windows are 25–30% of home energy use, so replacing them is high-leverage."** Abandoned — this DOE-style statistic is about the *share of loss*, not the *cost of eliminating it*. High share ÷ very high $/unit-of-U-reduction = poor investment. Reasoning from the share alone is the specific error this analysis exists to avoid.
- **Discounted cash flow / NPV.** Abandoned as decoration. When the central paybacks are 29 and 84 years against a 10-year horizon, discounting only makes a negative result more negative; it adds a false precision the inputs cannot support.
- **Degree-day modeling from first principles.** Attempted, then set aside — without your climate zone and fuel price, an HDD model adds an assumption layer without narrowing the bracket. The bill in GT-6 is a *measurement*, and anchoring to it is stronger than anchoring to a modeled load.

---

## 6. Conclusion

**Do neither project as quoted this year. Do this instead:**

1. **Get a blower-door + thermal-imaging audit first** (~$300–600, often free or subsidized by the utility). This converts GT-8? from a sales figure into a measurement and tells you the actual attic/window/infiltration split for *your* house. Every number above has a bracket only because this is missing.
2. **Buy attic air sealing** ($800–$1,500). It is the only intervention here that pays back inside your horizon, and it is a technical prerequisite for the insulation (second-order effect 1).
3. **Re-bid the attic insulation.** Get two more quotes. $4,200 appears 30–100% above market for R-49 blown-in over ~1,300 ft². **At $2,000–$2,500 bundled with the air sealing, do it** — the combined package plausibly pays back in 10–14 years and delivers real comfort gains (warmer ceilings, fewer temperature swings). At $4,200 standalone, it does not pay back in 10 years.
4. **Decline the $18,500 window replacement on energy grounds.** Its payback is 60–128 years. If you want the window loss addressed, buy **interior low-e storm panels** for ~$1,400–$3,500 — roughly half the thermal benefit for under a fifth of the cost — and revisit replacement only when the sashes fail as *maintenance*.

**Total recommended spend this year: roughly $3,000–$4,500** for materially more energy benefit than the $4,200 attic quote alone, and about a quarter of the $22,700 both-quotes package.

### What would change this answer

| If this turns out to be true | The recommendation changes to |
|---|---|
| The audit shows windows are >45% of loss **and** they are single-pane originals | Storms become urgent; replacement still fails on economics |
| Your windows are rotted, stuck, or single-glazed with failed glazing | Replacement becomes a maintenance buy — judge it there, not here |
| Your state/utility offers a large insulation rebate (GT-9 successor) | The $4,200 quote can move back above the bar; re-run Chain B with the net price |
| Your bill is 100% heat and your climate is colder than assumed | All paybacks shorten proportionally; attic clears 10 years at market price, windows still do not |

**Weakest link, stated plainly:** the entire attic/window split rests on **GT-8?** (unverified 35%) and **GT-10?** (assumed geometry). Chain C's verdict survives even large errors in both — it has ~8× of margin. **Chain B's verdict does not.** Whether the attic project is worth $4,200 is genuinely close, and the audit in step 1 is what resolves it. Chain C is HIGH confidence; Chain B is MEDIUM until you measure.