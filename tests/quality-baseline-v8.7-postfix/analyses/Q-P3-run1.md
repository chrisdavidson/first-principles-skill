# First-Principles Analysis: Insulation vs. Windows

Your question routes to a full first-principles decision analysis (no single focused technique fires — it's a genuine multi-factor investment trade-off). I worked it through the five phases. The math below rests on two quantities you didn't give me — how the 35% splits between attic and windows, and your *annual* (not just coldest-4-month) heating cost — so I've bracketed both rather than pretend precision. Process tables first, then the analysis.

---

## Process output — Phase 4 Assumption Audit scan

| Chain | Step | Step text (brief) | Assumption surfaced? | Added to table? |
|---|---|---|---|---|
| C1 | 1 | Attic = ~0.18 of total loss | Yes — split unknown | Yes (A-4) |
| C1 | 2 | R-13→R-49 saves 73.5% of attic loss | No (from GT-1) | — |
| C1 | 3 | Annual heat cost ≈ $2,000 | Yes — season length | Yes (A-5) |
| C2 | 1 | Window = ~0.17 of total loss | No — same as A-4 | `[Assumes: A-4]` |
| C2 | 2 | Existing windows ≈ R-1–2, new ≈ R-6 | Yes — existing glazing unknown | Yes (A-7) |
| C3 | 1 | Cost-per-$-saved ratio | No | — |
| C4 | 1 | Insulation life 50 yr / windows 25 yr | Yes — asset life | Yes (A-9) |
| C5 | 1 | Partial in-occupancy recovery + resale | Yes — resale capture | Yes (A-10) |

## Process output — §6→§4 closure ledger

- "Do the insulation this year" → chain C1 + C4 + C5 ✓
- "Do not replace windows for energy reasons" → chain C2 + C3 + C4 ✓
- "Windows are ~5× less cost-effective per dollar" → chain C3 ✓
- "Consider low-cost window measures instead" → chain C2 second-order ✓
- "Neither / both are dominated options" → chain C3 + C5 ✓

Ledger clean; rubric gate cleared (weakest link — the attic/window split, A-4 — is flagged, not hidden, and the conclusion is shown to be robust to it via C3).

---

## 1. Problem Essence

**Core decision:** Given a fixed home-improvement budget this year, which envelope upgrade — attic insulation, window replacement, both, or neither — returns the most value over a ≥10-year horizon?

**Success criteria (checkable):**
- Ranks the four options by energy-dollar return per dollar spent.
- Accounts for the ≥10-year occupancy horizon and each asset's useful life.
- Separates energy savings (measurable) from comfort/aesthetic value (real but not an energy return).
- States confidence given the unknowns.

The triggering framing ("35% is lost through attic and windows") is *not* the decision. The decision is about **marginal dollars per marginal saving**, and the two upgrades cost 4.4× different amounts — so the 35% figure alone can't rank them.

## 2. Assumptions Table

| # | Assumption | Type | Treatment | Verdict | Verification |
|---|---|---|---|---|---|
| A-1 | Heat loss through a surface ∝ 1/R | physical law | accept as GT | HOLDS | Steady-state conduction, U = 1/R |
| A-2 | R-13→R-49 removes 73.5% of attic conductive loss | physical law (derived) | accept | HOLDS | 1 − 13/49 = 0.735 |
| A-3 | "35% via attic+windows" is accurate | untested belief | use, flag | UNVERIFIED — contractor assessment, not metered | GT-3? |
| A-4 | **Split of the 35% between attic and windows** | untested belief | **challenge — load-bearing** | UNVERIFIED — bracket f_attic ∈ [0.15, 0.22], f_window ∈ [0.13, 0.20] | Rough area/R estimate; weakest link |
| A-5 | Annual heating cost > the $1,640 coldest-4-month figure | current constraint | bracket | LIKELY — est. $1,800–$2,400/yr | Shoulder-month heating adds to the 4-month core |
| A-6 | Quotes ($4,200 / $18,500) are firm | convention | accept | HOLDS | User-supplied |
| A-7 | Existing windows ≈ R-1 (single) to R-2 (old double); triple-pane ≈ R-5–7 | untested belief | bracket | UNVERIFIED — 1948 house, glazing not stated | GT-7?; window save 60–85% |
| A-8 | Energy prices flat (no escalation) | convention | challenge | CONSERVATIVE — real prices usually rise, so paybacks quoted are *upper* bounds | Favors both upgrades if relaxed |
| A-9 | Blown insulation life ≈ 50+ yr; replacement windows ≈ 20–30 yr | convention | accept | TYPICAL | Industry norm |
| A-10 | Some unrecovered cost transfers to resale value | untested belief | flag | PARTIAL — insulation and windows both add resale, imperfectly | Realtor data varies |

**Load-bearing flag:** A-4 (the split) is the single assumption that most moves the insulation payback. The analysis is built so the *ranking* survives even the worst case of A-4 — see C3.

## 3. Ground Truths

- **GT-1:** Conductive loss ∝ 1/R. (physical law)
- **GT-2:** Attic R-13→R-49 ⇒ 73.5% less attic conductive loss. (derived, GT-1)
- **GT-3?:** Attic+windows ≈ 35% of heating loss. (unverified — A-3)
- **GT-4?:** Split unknown; f_attic ≈ 0.15–0.22, f_window ≈ 0.13–0.20. (unverified — A-4)
- **GT-5:** Coldest-4-month heat cost = $410 × 4 = $1,640; annual est. $1,800–$2,400. (given + A-5)
- **GT-6:** Insulation $4,200; windows $18,500. (given)
- **GT-7?:** Triple-pane cuts window conductive loss 60–85%. (unverified — A-7)
- **GT-8:** Occupancy ≥ 10 years. (given)
- **GT-9:** Insulation lasts ~50 yr; windows ~25 yr. (convention)

## 4. Derivation Chains

**C1 — Insulation annual saving & payback**
GT-1 + GT-2 + GT-4? + GT-5 → attic ≈ 18% of a ~$2,000 annual bill = ~$360/yr of loss, of which 73.5% is removed → **~$265/yr saved** (bracket **$180–$390** across the split and season-length ranges) → payback $4,200 / $265 ≈ **16 yr central (11–23 yr)**. `[Assumes: A-4, A-5]`

**C2 — Window annual saving & payback**
GT-1 + GT-7? + GT-4? + GT-5 → windows ≈ 17% of ~$2,000 = ~$340/yr of loss, ~67% removed → **~$228/yr saved** (bracket **$130–$400**) → payback $18,500 / $228 ≈ **81 yr (46–140 yr)**. `[Assumes: A-4, A-7]`

**C3 — Cost-effectiveness (the decisive chain)**
C1 + C2 → cost per $1/yr saved: insulation **$4,200/$265 ≈ $16**; windows **$18,500/$228 ≈ $81**. → **Insulation is ~5× more cost-effective per dollar.** This ratio is *robust to A-4*: even if the split flips to windows' favor, the 4.4× cost gap keeps insulation ahead unless windows carry essentially *all* the 35% and attic almost none — implausible for an R-13 attic under GT-1.

**C4 — Asset-life reality check**
GT-9 + C1 + C2 → insulation payback (11–23 yr) sits *inside* its ~50-yr life → net-positive lifetime NPV even at the pessimistic end. Window payback (46–140 yr) *exceeds* its ~25-yr life → **windows never recover their cost through energy**, in any bracket. `[Assumes: A-9]`

**C5 — Horizon decision**
GT-8 + C1 + C4 → over 10 years insulation returns **$2,650 (central) of $4,200** in direct savings, plus residual asset value + comfort + resale → favorable. Windows return only **~$2,280 of $18,500** in 10 years → energy-unjustified; their case must rest entirely on comfort/noise/aesthetics/resale. `[Assumes: A-10]`

**Second-order pass (Phase 4 extension, no Ground-Truth contradictions):**
- Insulation → do attic **air-sealing** at the same time (weak point in most 1948 attics); guard against moisture/ice-dams with proper ventilation; **bonus summer AC savings** not counted above (makes C1 conservative).
- Windows → deferring them does *not* mean living with the loss: **exterior storm windows + weatherstripping + cellular shades** capture much of the window loss for roughly **$1,500–$3,000** total — a fraction of $18,500 — and are far more cost-effective than replacement.

## 5. Abandoned Reasoning

- **Metered sub-load split:** I could have tried to nail A-4 exactly. Abandoned — you don't have the data, and C3 shows the ranking doesn't need it.
- **Precise triple-pane R-value:** dropped in favor of the 60–85% bracket; the window verdict (never pays back) holds across the entire range, so precision adds nothing.
- **Financing/opportunity-cost of $18,500:** noted but not modeled; it only *worsens* the window case, so omitting it is conservative and doesn't change the answer.

## 6. Conclusion

**Do the insulation this year. Do not replace the windows for energy reasons.** (→ C1, C3, C4, C5)

1. **Insulation — YES.** ~$265/yr saved (bracket $180–$390), ~16-yr central payback well inside a ~50-yr asset life, and it's the single highest-leverage envelope dollar available (73.5% of attic loss removed for $4,200). Pair it with attic air-sealing. Confidence: **HIGH on the "do it" verdict**, MEDIUM on the exact payback (A-4/A-5 unverified). The one thing that could weaken it: if the attic is a *small* share of the 35% (metering would tell you), payback stretches toward 20+ years — still defensible on asset life and comfort, but no longer a slam dunk. (→ C1, C4)

2. **Windows — NO, not on energy grounds.** ~$228/yr saved against $18,500 = 46–140-yr payback that exceeds the windows' own lifespan in every bracket. They recover only ~$2,280 of their cost in your 10-year stay. Buy them only if you separately value the comfort, quiet, condensation control, and resale at roughly $18,500 — that's a lifestyle purchase, not an energy investment. Confidence: **HIGH** (verdict robust across all unknowns via C3/C4). (→ C2, C3, C4)

3. **Windows are ~5× less cost-effective per dollar than insulation** ($81 vs $16 per $1/yr saved). (→ C3)

4. **Instead of replacement windows,** spend ~$1,500–$3,000 on storm windows, weatherstripping, and cellular shades to capture most of the window loss cheaply. (→ C2 second-order)

5. **"Both" and "neither" are both dominated.** "Both" wastes $18,500 on the poorest-returning option; "neither" leaves the best opportunity (insulation) on the table. (→ C3, C5)

**Bottom line:** Insulation now (+ air-seal the attic), skip the window replacement, and if the windows bother you, use the cheap storm-window/weatherstrip route this year. Revisit full window replacement only when the units fail or when you're buying comfort, not energy savings.

*Sharpen this in an afternoon: (a) ask the contractor for the attic vs. window split behind the 35% (resolves A-4), and (b) total your gas/electric heating charges across the full heating season, not just the 4 coldest months (resolves A-5). Both narrow the insulation payback bracket; neither changes the window verdict.*