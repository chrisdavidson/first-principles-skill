## Step 0 — Technique selection

No technique-specific trigger phrase fires; this is a multi-factor decision with quantitative uncertainty. **MODE = full-composer.** The `estimate` and `trade-off` companion procedures are invoked inline within Phase 4 (magnitude uncertainty + option comparison).

---

## 1. Problem Essence

**Core decision:** Which envelope upgrade(s), if any, to fund *this year* to maximize net financial return (plus comfort) over a ≥10-year hold — attic insulation, window replacement, both, or neither.

Success criteria (checkable against the conclusion):
- Ranks options by cost-effectiveness (savings per dollar spent), not by gross energy saved.
- Tests each option's payback against the 10-year horizon.
- Is robust to the one quantity you did **not** give me: how the 35% loss splits between attic and windows.

The triggering framing ("we lose 35% through attic + windows") is not the question. The question is *marginal return per dollar*, and the 35% is a shared ceiling both options draw from.

---

## 2. Assumptions Table

| Assumption | Type | Treatment | Verdict | Verification |
|---|---|---|---|---|
| Conductive loss ∝ 1/R (U = 1/R) | physical law | accept as GT | HELD | Steady-state Fourier conduction |
| Attic+windows = 35% of total loss | untested belief (your input) | accept as given GT | ACCEPTED-AS-INPUT | Your audit figure |
| Attic/window split of the 35% is unknown | current constraint | bracket both extremes | LOAD-BEARING | Not supplied — drives Phase 4 bracketing |
| 1948 windows are single-pane or failing double (R≈1–2) | convention | challenge; bracket R-1 to R-2 | LIKELY | Typical for era; **verify by inspection** |
| Triple-pane U≈0.20 (R≈5) | convention/measurement | accept with range | HELD | NFRC-typical spec |
| $410×4 mo is heating-dominated, not baseline load | untested belief | flag; conservative use | FLAGGED | Some base electricity may be inside the bill |
| Fuel price flat over 10 yr | untested belief | note; rising prices *help* both paybacks | FLAGGED | If energy inflates, paybacks shorten |
| Both jobs are competently done (attic air-sealed too) | untested belief | assumed | ASSUMED | Standard scope |

Surfaced by inversion ("what would make 'insulation is the better buy' false?"): only if the attic were a trivially small share of the 35% *and* windows were the dominant share — tested and rejected in Chain C2.

---

## 3. Ground Truths

- **GT-1** — Conductive heat loss through an element is proportional to 1/R. *(physical law)*
- **GT-2** — R-13 → R-49 reduces attic conductive loss by 1 − 13/49 = **73.5%**. *(derived from GT-1; arithmetic)*
- **GT-3** — Attic + windows together = **35%** of total heat loss. *(your input)*
- **GT-4** — Winter heating ≈ $410 × 4 = **$1,640** over the four coldest months; full annual heating ≈ $1,640–2,100 (shoulder months add load insulation also captures). *(given + estimate)*
- **GT-5** — Insulation = **$4,200**; windows = **$18,500**. *(quotes)*
- **GT-6?** — 1948 windows R≈1–2 → triple-pane R≈5 cuts window *conductive* loss ~**60–80%**. *(unverified until you confirm existing glazing; range used)*
- **GT-7** — Planned stay **≥10 years**. *(given)*
- **GT-8** — The attic-vs-window split of the 35% is **unknown**. *(explicit uncertainty)*

---

## 4. Derivation Chains

Because GT-8 is unknown, I bracket the split across its full range (attic share from 10% to 25% of total loss; windows take the remainder of the 35%). The key metric is **dollars spent per 1 percentage-point of heating bill eliminated** — this neutralizes the unknown split.

**Estimate procedure — cost-effectiveness ($/1% heating reduced):**

*Insulation:* cuts (attic share × 0.735) of total heating.
- Worst case (attic only 10% of loss): 0.10 × 0.735 = 7.4% cut → $4,200 / 7.4 = **$570 per 1%**
- Central (attic ≈ 22%): 0.22 × 0.735 = 16.2% → $4,200 / 16.2 = **$260 per 1%**
- Best (attic ≈ 25%): 18.4% → **$228 per 1%**

*Windows:* cuts (window share × 0.60–0.80).
- Best case (windows = full 35%, 80% reduction): 28% cut → $18,500 / 28 = **$660 per 1%**
- Central (windows ≈ 13%, 70%): 9.1% → $18,500 / 9.1 = **$2,030 per 1%**

**Chain C1 — Windows fail the horizon under every allocation.**
GT-5 + GT-3 + GT-6? → windows' *best possible* case is 28% of heating = 0.28 × $1,640 ≈ $459/yr → $18,500 / $459 = **40-year payback**; the realistic case is ~$150/yr → **>100 years**. → **Windows do not pay back within 10 years under any split of the 35%.** *Confidence: HIGH* (the conclusion survives even the input value most favorable to windows).

**Chain C2 — Insulation dominates on cost-effectiveness, robustly.**
Insulation's *worst* case ($570/1%) is still better than windows' *best* case ($660/1%). → For **any** allocation of the unknown split (GT-8), the insulation dollar buys more heat-loss reduction than the window dollar. → **Insulation is the strictly more cost-effective buy; the ranking never inverts.** *Confidence: HIGH.*

**Chain C3 — Insulation's absolute case.**
GT-2 + GT-4 central → ~15% heating reduction ≈ $250 (winter-only) to ~$310/yr (annual, capturing shoulder months) → energy-only payback ≈ **10–14 years**; at $4,200 with immediate comfort gain and air-sealing co-benefit, it is roughly break-even-to-positive on energy alone over the 10-year hold and clearly net-positive with comfort. → **Do the insulation this year.** *Confidence: MEDIUM* — hinges on GT-8; a duct-blaster/audit split would tighten it, but C2 already makes the *ranking* robust regardless.

**Second-order pass:** Insulating first *lowers* total loss, which further shrinks the already-tiny dollar return on windows (they'd be reducing a smaller pie) — reinforces, doesn't contradict, C1. Deferring windows preserves the option to replace them later *if a sash physically fails* (rot/seal failure/noise), when the spend is justified by non-energy factors. No extension contradicts a Ground Truth.

**Assumption Audit scan:**

| Chain | Step | Step text (brief) | Assumption surfaced? | Added to table? |
|---|---|---|---|---|
| C1 | 1 | windows best case 28% | window R-value (GT-6?) | already in table |
| C1 | 2 | 40-yr payback | fuel price flat | already flagged |
| C2 | 1 | insul worst > windows best | attic ≥10% of loss | already in table (GT-8) |
| C3 | 1 | 15% cut | attic ≈22% share | already in table (GT-8) |
| C3 | 2 | $/yr → payback | $410 heating-dominated | already flagged |

No new assumptions beyond the table.

---

## 5. Abandoned Reasoning

- **"Windows save the most because glass is the worst insulator."** Rejected: true *per square foot*, but total window area × loss share is small, and the $18,500 cost swamps any per-unit advantage (C1/C2). Reasoning-by-analogy to "glass is cold" is not a ground truth.
- **Whole-house energy-model per-window U-value simulation.** Abandoned — the split (GT-8) is the dominant uncertainty, and the $/1% metric already delivers a split-independent ranking without it. Precision there wouldn't change the decision.

---

## §6 → §4 closure ledger

- "Do the insulation this year" → C3 ✓
- "Do not replace windows this year (energy grounds)" → C1 ✓
- "Insulation is the more cost-effective option regardless of the loss split" → C2 ✓
- "Windows only justified by non-energy factors" → C1 second-order ✓

Ledger clean.

---

## 6. Conclusion

**Do the insulation this year. Do not do the windows. (Insulation only.)**

- **Windows — no** (Chain C1): even under the input values most generous to them, triple-pane replacement pays back in ~40 years, realistically 100+. Over your 10-year stay it recovers maybe $1,500–4,600 of an $18,500 spend on energy. That is a comfort/noise/rot decision, not an energy one — only replace a window when it physically fails.
- **Insulation — yes** (Chains C2, C3): it is the strictly more cost-effective dollar for *any* attic/window split of your 35% (its worst case beats windows' best case), and at $4,200 it lands near break-even-to-positive on energy over 10 years *plus* delivers immediate comfort and warmer ceilings. Ask the insulation contractor to **air-seal the attic plane before blowing** — it's cheap and captures infiltration loss the R-value math above ignores.
- **Both — no**, and **neither — no**: the two options are not a bundle; one clears the bar and one doesn't.

**One thing worth verifying before you sign (the load-bearing unknown, GT-8):** ask for the audit's breakdown of the 35% between attic and windows, and confirm your existing glazing. It won't change the ranking (C2 is robust), but if the attic is on the high end of its range, insulation's payback tightens toward 10 years; if low, it's more of a comfort-justified buy. The windows verdict does not move regardless.

*Confidence: window rejection HIGH; insulation recommendation MEDIUM-HIGH (ranking HIGH, absolute payback MEDIUM pending the split).*