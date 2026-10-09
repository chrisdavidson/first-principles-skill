**Disclosed:** No re-entry edge fired and no reference read failed during this run; the
Self-Audit Gate cleared on its first scoring pass (Criterion 3 scored Sound, all others
Rigorous — see the Appendix for the full verdict blocks).

## Answer

**Recommendation:** Pay down roughly 70–75% of the $60,000 (~$42,000–$45,000) as extra mortgage
principal and explicitly request a loan recast, and invest the remaining 25–30%
(~$15,000–$18,000) in the taxable index fund — after first confirming unused tax-advantaged
retirement space (chain C7).
**Band (from §6):** MEDIUM
**Would change it:** Confirming whether 401(k)/IRA/HSA space is unused this year (chain C7), and
whether the next decade's realized equity return tracks Vanguard's current forecast (4.2–6.2%)
or the long-run historical average instead (chain C3).
## 1. Problem Essence

**Essence Statement:** Given a $240,000 mortgage at 6.25% with no tax shield, and $60,000 in
genuinely surplus cash, should the household eliminate a guaranteed 6.25% obligation or take on
market risk for a potentially higher but uncertain return — and is the honest answer a corner
choice at all, or a specific split between the two?

**Success criteria** (what a correct answer must achieve):
- States, numerically, what each option is worth after 10 years under explicit, stated
  assumptions — not just "investing usually wins long-run."
- Treats the guaranteed-vs-uncertain comparison as a risk-adjusted comparison, not a raw
  expected-value race.
- Tests whether a blend (not just 100% A or 100% B) outperforms either pure option on the
  household's own criteria.
- Names the specific condition(s) under which the recommendation would flip.
- Surfaces the liquidity and behavioral consequences of each path, not just the arithmetic.


## 2. Assumptions Table

| # | Assumption | Type | Treatment | Verdict | Verification |
|---|---|---|---|---|---|
| A-1 | A guaranteed return and an uncertain expected return are directly comparable for decision-making (raw EV race) | convention | Explicitly challenged — replaced with risk-adjusted comparison in Phase 4 | Discard — not valid as sole criterion; replaced by risk-adjusted comparison | Addressed via weighted trade-off (chain C6), which scores certainty as its own criterion |
| A-2 | Paying down principal improves the household's monthly cash-flow flexibility / recession resilience | untested belief | Verify | Challenge — true only conditionally on requesting a recast | GT-7 (read-at-source: Chase.com recast page) — extra principal does not lower the required payment absent a recast request |
| A-3 | Tax-advantaged retirement space (401k/IRA/HSA) is already fully used this year, so it is not a superior destination for this $60k | untested belief | Flag as unverified | Challenge — unverified; carried as an open precondition | Not stated by user; carried into Conclusion as an open precondition (chain C7, Pre-mortem Cluster 4) |
| A-4 | Equities will deliver close to their long-run historical average (~9–10% nominal) over the next decade | convention | Explicitly challenged against current forward estimate | Discard — rejected as the base case; retained only as the named rival in chain C3 | GT-9 (read-at-source: Vanguard, current forecast 4.2–6.2%) vs. GT-11 (historical average, `?`) |
| A-5 | Home equity is effectively as liquid as a brokerage account — "it's still your money" | convention | Explicitly challenged | Discard — contradicted by GT-7 and GT-13 | GT-7 and GT-13 (chain C4) |
| A-6 | The 6.25% mortgage rate is a fixed, non-expiring hurdle rate for the full 10-year horizon | current constraint | Record expiry conditions | Accept — expires on refinance, sale/relocation, or early payoff; contractual, not physical | Expires per the loan contract; see A-10 and Pre-mortem Cluster 6 |
| A-7 | Decisions should maximize raw expected value only, ignoring variance, behavior, and regret | convention | Explicitly challenged | Discard — rejected as sole criterion | Addressed via trade-off's risk/behavioral/tax-efficiency criteria (chain C6) and Pre-mortem Cluster 5 |
| A-8 | A 10-year horizon is "long enough" to make equity returns safe/guaranteed | convention | Explicitly challenged | Discard — rejected; GT-11's "lost decade" is a direct counter-example | GT-11 (`?`) |
| A-9 | Mortgage/debt risk is uncorrelated with the household's other risks (job loss, local economy) | untested belief | Verify | Discard — rejected; combined with GT-7/GT-13, partially inverts the usual framing | GT-14 (`?`), surfaced via inversion |
| A-10 | The household will hold the home for the full 10 years without selling or relocating | untested belief | Flag as unverified | Challenge — unverified; feeds the blend-weighting recommendation | Not stated by user; feeds Pre-mortem Cluster 6, surfaced via inversion |
| A-11 | Approximating Option B's cost basis as a flat $60,000 (ignoring basis growth from reinvested/taxed dividends) is immaterial to the comparison | current constraint | Record as an approximation; check materiality | Accept — checked immaterial; modeling simplification, not physical | Checked in Phase 5 Recompute — effect is on the order of hundreds of dollars, far smaller than the gap between options |
| A-12 | The household's income/employment is meaningfully tied to the same local economy that drives their home's value | untested belief | Flag as unverified | Challenge — unverified; caps chain C5 at MEDIUM | Not stated by user (remote work vs. local employer unknown); surfaced in the Assumption Audit |
## 3. Ground Truths

`?`-marked: GT-8, GT-10, GT-11, GT-12, GT-13, GT-14 (6 of 14).

| ID | Ground truth | Provenance |
|---|---|---|
| GT-1 | Mortgage balance $240,000; 30-year fixed at 6.25% APR; 27 years (324 months) remaining | Stipulated by user — household's own account data, not an externally-sourced claim |
| GT-2 | Household takes the standard deduction → $0 of mortgage interest reduces taxable income | Stipulated by user |
| GT-3 | Marginal ordinary tax rate ≈28% (combined federal+state); LTCG/qualified-dividend rate ≈18% | Stipulated by user |
| GT-4 | The $60,000 is surplus cash above an already fully-funded 6-month emergency reserve | Stipulated by user |
| GT-5 | Decision horizon = 10 years | Stipulated by user (framing constraint) |
| GT-6 | Prepaying principal on a fixed-rate amortizing loan is financially equivalent, dollar for dollar, to investing in a risk-free, tax-free instrument yielding the loan's note rate (6.25% nominal, compounded monthly) — a financial-mathematics identity | Definitional/derived (financial algebra), no external citation needed — read-location: self-contained identity, re-derived and checked in Phase 5 Recompute |
| GT-7 | An extra lump-sum principal payment reduces total interest and shortens the amortization term but does **not** reduce the required monthly payment unless the borrower explicitly requests, and the servicer grants, a loan "recast" (re-amortization using the new lower balance); recasts are not automatic, are generally unavailable on FHA/VA/USDA loans, and specific minimums/fees vary by servicer | read-at-source — Chase.com, "Mortgage Recast" page (fetched this session): "When you pay extra toward your principal... you may have the option to lower your payments through a mortgage recast" / "No, there is not a minimum amount required" / "Fees may apply"; general mechanism cross-confirmed across multiple servicer help pages in search results |
| GT-8 | Under current US federal tax law: qualified dividends are taxed annually as received; unrealized capital appreciation in a buy-and-hold position is untaxed until sale; assets held until death receive a stepped-up cost basis | `?` — general tax-law domain knowledge, not read at a specific source this session |
| GT-9 | Vanguard Capital Markets Model's 10-year annualized nominal U.S. equity return forecast, per the June 30, 2026 update, is **4.2%–6.2%**, down from 4.9%–6.9% the prior quarter | read-at-source — corporate.vanguard.com, "Setting realistic expectations" / VEMO return-forecasts page (fetched this session), quoting the model's own stated range and vintage |
| GT-10 | Trailing/forward dividend yield on VTI (proxy for a broad U.S. total-market index fund) is approximately 1.06%–1.13% as of mid-to-late 2026 | `?` — reported-by-delegate (WebSearch aggregation across multiple financial-data sites this session; no single page opened and read directly) |
| GT-11 | Long-run realized historical nominal total return for U.S. broad-market equities (~1926–present) averages roughly 9–10%/yr, but includes extended sub-periods (e.g., the decade beginning ~2000) with near-zero-to-negative nominal CAGR (a "lost decade") | `?` — general, widely-cited financial-history knowledge, not read at a specific source this session |
| GT-12 | The 10-year U.S. Treasury yield was approximately 4.3%–4.8% in September/October 2026 | `?` — reported-by-delegate (WebSearch aggregation this session) |
| GT-13 | Home equity is illiquid relative to brokerage assets: accessing it requires sale, refinance, or a HELOC/home-equity loan, each requiring lender underwriting that can tighten or freeze during economic stress (widely documented during 2008–2009, when many banks suspended or reduced existing HELOC lines); brokerage assets are typically saleable for cash within days regardless of the holder's employment or credit status | `?` — general/historical domain knowledge, not read at a specific source this session |
| GT-14 | A primary residence is a single, undiversified, illiquid asset; increasing equity concentration in it raises concentration risk, which can be correlated with local employment/labor-market risk (a regional downturn can depress both local home values and local employment simultaneously) | `?` — domain/economic-reasoning claim, not a specific sourced statistic |

Unsuffixed ground truths feeding load-bearing chains and their read-locations: **GT-7** —
Chase.com "Mortgage Recast" page, the page's own Q&A text on minimums/fees/automaticity (fetched
this session). **GT-9** — corporate.vanguard.com VEMO return-forecasts page, the sentence "our
10-year expected annualized return for U.S. equities declined from a range of 4.9%–6.9% to a
range of 4.2%–6.2%" (fetched this session). GT-1 through GT-5 are user-stipulated problem
parameters (the household's own private account/tax data), not externally-sourced claims, and so
carry no read-location; they are treated as given inputs to the problem, distinct in kind from
the `?`-marked empirical/estimate entries above. GT-6 is a self-contained financial identity,
independently re-derived and checked under Phase 5 Recompute rather than read from a source.


## 4. Derivation Chains

**C1 — Option A's guaranteed value**

```text
GT-1 (balance/rate/term) + GT-6 (prepayment = risk-free-yield identity)
→ paying $60,000 extra principal locks in a guaranteed, tax-free effective annual yield of ~6.43% (6.25% nominal, compounded monthly) on that $60,000, for as long as the loan remains outstanding
→ GT-2 means none of that 6.25% is diluted by a lost tax shield, unlike for a household that itemizes and deducts mortgage interest
→ compounding that guaranteed yield for 10 years gives a certain ending value of 60,000 × (1 + 0.0625/12)^120 ≈ $111,913 (nominal), with zero variance
```
**Pre-check:** head GT-1, GT-6 · ?-marked: none · lowest cited: none · Inputs ceiling: HIGH
**Confidence:** HIGH — Inputs are both unsuffixed (GT-6 is a closed-form identity, re-verified
under Phase 5 Recompute). Inference is direct arithmetic with no modeling choice. Rivals: none —
a rival would only be "the math is wrong," which Recompute checks and confirms.

**C2 — Option B's after-tax 10-year value under the current forward estimate**

```text
GT-9 (Vanguard 10-yr forecast 4.2–6.2%) + GT-10 (dividend yield ~1.1%) + GT-3 (18% LTCG/QDI)
→ modeling qualified dividends as taxed annually at 18% (net ~0.90%) and price appreciation as compounding untaxed until a single sale at year 10 [Assumes: A-11]
→ the forecast's 4.2% / 5.2% / 6.2% points compound to pretax year-10 values of ≈$88,842 / $97,752 / $107,478
→ after paying 18% LTCG tax on the realized gain at sale, the after-tax year-10 values are ≈$83,650 / $90,957 / $98,932
→ every point in that after-tax range, and even the pretax never-sell values, sit below C1's guaranteed $111,913
```
**Pre-check:** head GT-9, GT-10, GT-3 · ?-marked: GT-10 · lowest cited: none · Inputs ceiling: MEDIUM
**Confidence:** MEDIUM — Inputs: GT-9 is read-at-source and unsuffixed, but GT-10 is `?`
(reported-by-delegate); the verification that would remove it as a cause of the downgrade is
reading a single primary source (e.g., the fund issuer's own factsheet) for VTI's exact trailing
yield on one fixed date, rather than an aggregated search snippet — its effect on the result is
in any case small (a 0.1pp dividend-yield swing moves the ending value by well under $500).
Inference rests on the A-11 basis-approximation, checked immaterial in Phase 5. Rivals: a strong,
**live** rival exists — see C3 — so this is not rated HIGH even though the arithmetic itself is
simple.

**C3 — The breakeven threshold and the live rival**

```text
GT-3 (18% LTCG) + C1 (guaranteed value $111,913)
→ solving for the pretax equity return r where 0.82×[60,000×(1+r)^10]+0.18×60,000 = 111,913 gives a sell-at-year-10 breakeven of r ≈ 7.67%/yr
→ solving the same equation assuming zero exit tax (never sell / step-up at death) gives a breakeven of r ≈ 6.45%/yr, essentially the mortgage's own effective yield
→ GT-9's current forecast range (4.2–6.2%) sits below both breakevens, while GT-11's long-run historical average (~9–10%) sits above both
→ which regime the next decade resembles is therefore the single swing factor behind the whole comparison
```
**Pre-check:** head GT-3, C1 (HIGH) · ?-marked: none on this head · lowest cited: HIGH (C1) · Inputs ceiling: MEDIUM
**Confidence:** MEDIUM — Inputs are clean (C1 is HIGH, GT-3 unsuffixed), so the ceiling here is
set by Rivals, not Inputs: GT-11 (`?`) is the named rival, and no verification path exists to
resolve it in advance — whether the next decade's realized return resembles GT-9 or GT-11 is only
observable in hindsight, at the end of the 10-year horizon itself, which is why the recommendation
in C7 is a blend rather than a corner bet on either regime. Inference is a direct algebraic solve,
re-checked in Phase 5 Recompute.

**C4 — Liquidity: the "payoff = safety" assumption only half-holds**

```text
GT-7 (no recast ⇒ no payment relief) + GT-4 (reserve already funded) + GT-13 (home equity illiquid under stress)
→ absent an explicit recast request, Option A's $60,000 produces no monthly cash-flow relief and is not accessible as emergency funds beyond the existing reserve
→ Option B's $60,000 remains sellable for cash within days regardless of the household's employment or credit status
→ the common payoff-equals-safety intuition (A-2, A-5) is therefore only partly true: it removes interest-rate variance but not cash-flow or emergency-access variance, absent a recast
```
**Pre-check:** head GT-7, GT-4, GT-13 · ?-marked: GT-13 · lowest cited: none · Inputs ceiling: MEDIUM
**Confidence:** MEDIUM — Inputs: GT-7 is read-at-source and unsuffixed (the mechanism is well
confirmed); GT-13 is `?` (general/historical domain knowledge about 2008-era HELOC freezes, not
read at a specific source this session) and that is what caps this chain, with the verification
that would remove the cap being a direct citation of HELOC-availability data during 2008–2009.
Inference: direct. Rivals: a qualified borrower could likely get a HELOC quickly in normal times
— named and addressed in §5 Rival of the adversarial pass.

**C5 — Concentration/correlation risk cuts against "more house equity = more safety"**

```text
GT-14 (home-equity concentration/correlation risk) + C4 (illiquidity under stress)
→ directing more capital into home equity increases concentration in a single undiversified, illiquid asset [Assumes: A-12]
→ that asset's value may fall precisely when local employment risk rises, if the household's income is tied to the same local economy
→ keeping capital diversified and liquid can therefore provide better insurance against a correlated job-loss/local-downturn scenario than concentrating further in the home
```
**Pre-check:** head GT-14, C4 (MEDIUM) · ?-marked: GT-14 · lowest cited: MEDIUM (C4) · Inputs ceiling: MEDIUM
**Confidence:** MEDIUM — Inputs: GT-14 is `?`, and the verification that would remove it as a
cause of the downgrade is a direct regional-level study correlating local home-price declines
with local employment/layoff data (rather than the general economic-reasoning basis used here);
C4 is itself MEDIUM, which also caps this chain. The A-12 assumption (income tied to the local
economy) is unverified and, if false (e.g., a fully remote job with employer and income based
elsewhere), would weaken this chain's force considerably — confirming the household's employment
structure is the verification that would lift that part of the cap. Inference: reasoning-based,
not a closed-form calculation. Rivals: none named beyond what C4 already carries.

**C6 — Weighted trade-off across A, B, and a 50/50 blend (C)**

Criteria and locked weights (1–5): Expected after-tax 10-yr value = 5, Risk/certainty = 4,
Liquidity if a need arises = 3, Diversification = 2, Behavioral/simplicity = 2, Tax efficiency
going forward = 2. No must-haves beyond GT-4 (reserve funded), which both options already
satisfy. Anchors: EV scored 1=lowest of the three point-estimates, 5=highest (per C1/C2);
Risk scored 1=full market variance, 5=zero variance; Liquidity scored 1=locked absent lender
approval, 5=sellable in days; Diversification scored 1=adds to an already-large undiversified
asset, 5=adds to a diversified portfolio; Behavioral scored 1=active panic-sell risk, 5=no
ongoing behavioral risk; Tax efficiency scored 1=ongoing dividend/LTCG drag, 5=none going forward.

```text
C1 (A = $111,913 guaranteed) + C2 (B range $83,650–$98,932) + C4 (liquidity) + C5 (diversification)
→ scoring each option on the locked anchors gives A = 5,5,1,1,5,5 for a weighted total of 70
→ B scores 1,1,5,5,2,2 for a weighted total of 42; the blend C (50/50) scores 3,3,3,3,3,4 for a weighted total of 56
→ closing the 14-point A–C gap via Liquidity or Diversification alone would require moving that weight to 10, outside the 1–5 scale
→ even zeroing the EV criterion's weight only closes 10 of the 14 points, leaving A ahead on Risk, Behavioral, and Tax efficiency alone
→ no single-criterion weight change within the 1–5 scale flips the ranking, though it is not robust to the live rival in C3 changing the EV row's numbers
```
**Pre-check:** head C1 (HIGH), C2 (MEDIUM), C4 (MEDIUM), C5 (MEDIUM) · ?-marked: none directly, via cited chains: GT-10, GT-13, GT-14 · lowest cited: MEDIUM · Inputs ceiling: MEDIUM
**Confidence:** MEDIUM — capped by the lowest-rated chains it cites (C2, C4, C5, all MEDIUM).
Inference: the trade-off math itself is straightforward and re-checked in Phase 5 Recompute.
Rivals: C3's historical-average rival is still live and would, if realized, swing the EV row's
scores (though the flip test shows this alone is unlikely to overturn the full-paydown-vs-blend
ranking within this weighting scheme — it would, however, change how much upside the
full-paydown corner solution forgoes).

**C7 — Second-order extension and the decision-ready recommendation**

Actor lens: the household gains monthly slack only if a recast is requested, and that slack can
be saved or lifestyle-inflated; the servicer may misapply an "extra payment" as an advance
future-payment rather than a principal reduction unless explicitly instructed; a lower
loan-to-value balance eases underwriting for a *future* lender (next refinance, HELOC, or other
credit); a financial adviser's rival reading would point out that unused tax-advantaged
retirement space (A-3) could dominate both options and was never priced into this comparison.
Time lens: immediately, Option A removes $60,000 of liquidity with no payment change absent a
recast, while Option B's $60,000 becomes volatile immediately; after a few years, Option A's
benefit is a silent, fully-realized interest saving, while Option B is highly path-dependent and
exposed to early-drawdown panic-selling risk (GT-15, folded into C6's Behavioral criterion); once
in place long enough to be assumed (year 8–10+), Option A's lower balance becomes the invisible
new normal, while year 10 for Option B is only a *decision point* about realizing gains, not a
forced sale — meaning C2's after-tax figures are a conservative, worst-case framing, and the
pretax (never-sell) values are the fairer "wealth at year 10" comparison if no sale is planned;
even on that generous basis, Option A still leads across Vanguard's entire current range (C3). No
extension step here contradicts a Ground Truth.

```text
C6 (trade-off favors full paydown) + GT-7 (recast needed to realize the safety benefit) + C5 (liquidity/diversification insurance value) [Assumes: A-3]
→ the decision-ready recommendation is a blend tilted toward paydown: pay down ~70–75% (~$42,000–$45,000) as extra principal and explicitly request a loan recast
→ invest the remaining 25–30% (~$15,000–$18,000) in the taxable index fund, preserving diversification, same-week liquidity, and upside participation
→ this captures most of C6's robust risk-adjusted advantage while hedging the two live risks a 100% corner solution ignores: forecast error (C3) and concentration/illiquidity (C5)
```
**Pre-check:** head C6 (MEDIUM), GT-7, C5 (MEDIUM) · ?-marked: none directly, via C5: GT-14 · lowest cited: MEDIUM · Inputs ceiling: MEDIUM
**Confidence:** MEDIUM — inherits C6's MEDIUM rating and depends on A-3, which is unverified: if
unused retirement-account space exists, the recommended destination for some or all of the
$60,000 changes outright (see §6 and Pre-mortem Cluster 4 for the explicit precondition this
places on the recommendation).
## 5. Abandoned Reasoning

**Naive "stocks always win over 10 years" reasoning.**
What was tried: defaulting to the common personal-finance heuristic that broad-market equities
beat a ~6% hurdle over any 10-year stretch, based on the long-run historical average.
Why abandoned: GT-9 (read-at-source, Vanguard's current model) puts the forward 10-year forecast
entirely below both the sell-at-year-10 and never-sell breakevens computed in C3; the historical
average (GT-11) is real but is a `?`-marked, unresolved rival, not a settled fact for the *next*
specific decade.
What it ruled out: using the historical average as the base case (A-4) for sizing the
recommendation; it remains live only as the named rival in C3/C6.

**Naive "pay off debt = always safe" reasoning.**
What was tried: treating full mortgage paydown as straightforwardly improving the household's
resilience to job loss or emergencies.
Why abandoned: C4 shows that, absent an explicit recast request, paydown buys zero monthly
cash-flow relief and converts liquid cash into an asset that is specifically harder to access
during the kind of downturn (GT-13) that would also threaten income.
What it ruled out: recommending 100% paydown *without* a recast instruction; the recommendation
in C7 explicitly requires requesting a recast for this reason.

**Annual-18%-on-everything tax model for Option B.**
What was tried: modeling Option B's entire return as taxed at 18% every year, the simplest
reading of "net of 18% LTCG tax drag" in the prompt.
Why abandoned: GT-8 establishes that unrealized price appreciation in a buy-and-hold index
position is not taxed annually — only dividends are — so an annual-18%-on-everything model
overstates the tax drag by roughly 5–6x relative to the bifurcated dividend/capital-gains model
actually used in C2.
What it ruled out: it was replaced before being used in any chain; no conclusion rests on it.

**Pure 100% Option B as the headline recommendation.**
What was tried: recommending full investment of the $60,000, on the standard "mortgage rate is
low, equities win long-run, don't prepay low-interest debt" logic.
Why abandoned: C6's trade-off, run on this household's actual numbers (no tax shield, GT-9's
current forecast), scores 100% investing lowest of the three options (42 vs. 70 for paydown, 56
for the blend), and C3 shows the whole of Vanguard's current forecast range sits below both
breakevens.
What it ruled out: C6, which is what rules it out as the headline, while keeping it alive as the
upside case if the GT-11 rival is realized instead.

**Pure 100% Option A as the headline recommendation (no invested tranche).**
What was tried: taking C6's raw weighted-score winner (70 vs. 56 for the blend) as the final
answer without qualification.
Why abandoned: C5 and the Pre-mortem (§ adversarial pass, Clusters 2 and 6) show that going
100% into home equity forgoes diversification and upside participation that the trade-off's own
locked weights only partially price in, and is also not robust to an early home sale (A-10) or
unused retirement-account space (A-3).
What it ruled out: C7 is what overrides the raw trade-off corner solution with the blend.

## 6. Conclusion

**Recommended approach:** Split the $60,000 roughly 70–75% toward extra mortgage principal
(~$42,000–$45,000) **and explicitly request a loan recast** from the servicer so the paydown
actually lowers the required monthly payment, and invest the remaining 25–30%
(~$15,000–$18,000) as a lump sum in the taxable broad-market index fund (chain C7). Before
executing either leg, confirm whether this year's 401(k)/IRA/HSA space is unused — if so, redirect
that portion of the $60,000 there first, since it was never priced into this A-vs-B comparison
(A-3, chain C7).

**Key insight:** The usual "mortgage rate is low, equities win long-run, don't prepay" advice
does not transfer to this household, because two of its normal supports are missing here: there
is no tax shield reducing the effective mortgage cost below 6.25% (GT-2), and the current (not
historical-average) forward-return forecast for equities sits below the breakeven rate the
mortgage sets (chain C3) — a materially different starting point than the textbook case (chain C1
vs. C2).

**Trade-offs acknowledged:** The recommended blend gives up some of the raw trade-off's top score
(chain C6: 70 for full paydown vs. 56 for a 50/50 blend) in exchange for diversification,
same-week liquidity, and upside participation if the historical-average rival (chain C3) turns
out to be the realized regime instead of Vanguard's current forecast (chain C5). It also assumes,
unverified, that no better-than-both-options use of the money exists in tax-advantaged retirement
space (A-3) and that the household will not sell or relocate within the 10-year horizon (A-10) —
chain C7 names both as open preconditions rather than settled facts.

**Pre-check:** head C1 (HIGH), C3 (MEDIUM), C6 (MEDIUM), C7 (MEDIUM) · ?-marked: none directly on
this head, via cited chains: GT-10, GT-11, GT-13, GT-14 · lowest cited: MEDIUM · Inputs ceiling: MEDIUM
**Confidence:** MEDIUM. The guaranteed-value side of the comparison (chain C1, $111,913) is HIGH
confidence — it is closed-form arithmetic on user-stipulated contract terms. The side that caps
the overall recommendation at MEDIUM is the live, `?`-marked rival in chain C3: whether the next
decade's realized equity return resembles Vanguard's current forecast (GT-9, read-at-source,
4.2–6.2%) or the long-run historical average (GT-11, `?`, ~9–10%) is not something this analysis
can settle, only bracket. What would move this to HIGH: (1) resolving A-3 (confirm retirement-
account space is genuinely exhausted), and (2) the practical impossibility of resolving GT-11's
rival in advance — which is why the recommendation is a blend sized to perform acceptably under
both regimes, rather than a corner bet on one of them.
## Appendix — process output

## Assumption Audit scan (process output)

| Chain | Step | Step Text (brief) | Assumption surfaced? | Added to Table? |
|---|---|---|---|---|
| C1 | 1 | locks in guaranteed tax-free yield ~6.43% | no | — |
| C1 | 2 | GT-2 means no tax-shield dilution | no | — |
| C1 | 3 | compounds to $111,913 | no | — |
| C2 | 1 | model dividends taxed annually, appreciation deferred | yes — flat-basis approximation | A-11 |
| C2 | 2 | forecast points compound to pretax values | no | — |
| C2 | 3 | after-tax values computed | no | — |
| C2 | 4 | all below C1's guaranteed value | no | — |
| C3 | 1 | sell-at-year-10 breakeven ≈7.67% | no | — |
| C3 | 2 | never-sell breakeven ≈6.45% | no | — |
| C3 | 3 | GT-9 range below both breakevens, GT-11 above | no | — |
| C3 | 4 | swing factor is which regime obtains | no | — |
| C4 | 1 | no recast ⇒ no cash-flow relief | no | — |
| C4 | 2 | Option B sellable within days | no | — |
| C4 | 3 | payoff=safety only partly true | no | — |
| C5 | 1 | more home equity = more concentration | yes — income tied to local economy | A-12 |
| C5 | 2 | asset value may fall with local employment risk | no (references A-12 already added) | — |
| C5 | 3 | diversified/liquid capital hedges correlated risk | no | — |
| C6 | 1 | A scores 5,5,1,1,5,5 → 70 | no | — |
| C6 | 2 | B scores 42; blend C scores 56 | no | — |
| C6 | 3 | flip test: liquidity/diversification weight would need to hit 10 | no | — |
| C6 | 4 | zeroing EV weight still leaves A ahead | no | — |
| C6 | 5 | no single-weight change flips ranking | no | — |
| C7 | 1 | blend: ~70-75% paydown + recast | no (A-3 already declared on head) | — |
| C7 | 2 | invest remaining 25-30% | no | — |
| C7 | 3 | captures C6's advantage while hedging C3/C5 risks | no | — |

Scan complete: 7 chains, 24 steps scanned in order; 2 assumptions surfaced (A-11 on C2 step 1,
A-12 on C5 step 1), both already present in the Classified Assumptions Table (§2) before this
scan was written, confirming no gap between the inline `[Assumes: X]` marks and the table.
## Techniques not applied (process output)

fishbone — not applicable — the assumption space here was tractable by direct enumeration plus
inversion; it was not a multi-causal breadth problem needing category brainstorming.
five-whys (reduce-to-primitives mode) — not applicable — the ground truths used either bottom
out directly at a self-contained financial identity (GT-6) or at read-at-source/reported figures
(GT-9, GT-10, etc.); none required recursive decomposition into constituent facts to verify.
theoretical-limit — not applicable — the question is a risk-adjusted guaranteed-vs-uncertain
comparison, not a "what do the fundamentals permit once convention is stripped" ceiling question.
## §6→§4 closure ledger (process output)

- "Split the $60,000 roughly 70–75% toward extra mortgage principal... and invest the remaining 25–30%... redirect that portion... to retirement space first" → chain C7 ✓
- "The usual 'mortgage rate is low... don't prepay' advice does not transfer to this household... a materially different starting point than the textbook case" → chain C1 vs. C2 ✓
- "The recommended blend gives up some of the raw trade-off's top score... in exchange for diversification, same-week liquidity, and upside participation" → chains C6, C5, C3 ✓
- "It also assumes, unverified, that no better-than-both-options use of the money exists... and that the household will not sell or relocate" → chain C7 (A-3, A-10) ✓
- "The guaranteed-value side of the comparison is HIGH confidence" → chain C1 ✓
- "The side that caps the overall recommendation at MEDIUM is the live rival in chain C3" → chain C3 ✓

Ledger complete: 6 claims, 6 traced, 0 cut.
## Self-audit scan (process output)

**Table 1 — Chain form (section 4)**

| Chain | Chain Head (brief) | Form conforming? | Rule applied | Dependency clean? | Band | Act attempted? | Edges fired |
|---|---|---|---|---|---|---|---|
| C1 | GT-1 + GT-6 | yes | n/a | yes | HIGH | no | none |
| C2 | GT-9 + GT-10 + GT-3 | yes | n/a | yes | MEDIUM | yes | none |
| C3 | GT-3 + C1 | yes | n/a | yes | MEDIUM | no | none |
| C4 | GT-7 + GT-4 + GT-13 | yes | n/a | yes | MEDIUM | yes | none |
| C5 | GT-14 + C4 | yes | n/a | yes | MEDIUM | no | none |
| C6 | C1 + C2 + C4 + C5 | yes | n/a | yes | MEDIUM | no | none |
| C7 | C6 + GT-7 + C5 | yes | n/a | yes | MEDIUM | no | none |

**Table 2 — Claim inventory (section 6)**

| §6 Span (brief) | Construct | Claim under R11? | R11 clause applied | Chain cited |
|---|---|---|---|---|
| Recommended approach: split 70–75%/25–30%, recast, check retirement space | bold lead-in | yes | bold lead-in whose colon closes the bold span | C7 |
| Key insight: usual advice doesn't transfer, no tax shield + below-breakeven forecast | bold lead-in | yes | bold lead-in whose colon closes the bold span | C1 vs. C2 |
| Trade-offs acknowledged: gives up top trade-off score for diversification/liquidity/upside | bold lead-in | yes | bold lead-in whose colon closes the bold span | C6, C5, C3, C7 |
| Pre-check: head C1 (HIGH), C3 (MEDIUM), C6 (MEDIUM), C7 (MEDIUM)... | bold lead-in | yes | bold lead-in whose colon closes the bold span | C1, C3, C6, C7 |
| Confidence: MEDIUM, guaranteed side HIGH (C1), capped by live rival (C3) | bold lead-in | yes | bold lead-in whose colon closes the bold span | C1, C3 |

Scan complete: 7 chain rows, one per section-4 chain block in order; 5 section-6 rows, one per
construct in order — 5 claims under R11, 0 excluded. 0 chains malformed, 0 claims untraced.
## Adversarial pass (process output)

**Recompute.** 60,000 × (1+0.0625/12)^120: monthly rate 0.00520833, (1.00520833)^120 = 1.86522
→ $111,913 — matches C1. Option B pretax year-10 values at r=4.2/5.2/6.2%: using g=r−0.00198
(dividend-tax adjustment at 1.1% yield, 18% rate): g=4.002/5.002/6.002% → (1+g)^10 = 1.4807 /
1.6292 / 1.7913 → $88,842 / $97,752 / $107,478 — matches C2. After 18% LTCG on the gain over a
flat $60,000 basis: $83,650 / $90,957 / $98,932 — matches C2. Breakeven solve:
0.82×end+10,800=111,913 → end=$123,308 → (1+g)^10=2.05513 → g=7.468% → r=7.666% ≈7.67% — matches
C3. Never-sell breakeven: 60,000×(1+r)^10=111,913 → r=6.449% ≈6.45% — matches C3. Trade-off
totals: A=5(5)+5(4)+1(3)+1(2)+5(2)+5(2)=25+20+3+2+10+10=70; B=5+4+15+10+4+4=42;
C=15+12+9+6+6+8=56 — matches C6. All recomputed figures agree with the chains; no arithmetic
error found.

**Sensitivity.** The single ground truth whose falsity would flip the conclusion is GT-9 (or,
more precisely, which regime — GT-9's current forecast vs. GT-11's historical average — actually
obtains over the next decade). GT-9 itself is read-at-source and unsuffixed; GT-11, the named
rival, is `?`-marked. No new cap is applied beyond what C3/C6/C7 already carry (MEDIUM), because
this sensitivity is already priced into those chains' confidence lines; the verification that
would remove it is simply the passage of the 10 years themselves — it cannot be resolved in
advance, which is exactly why the recommendation is a blend rather than a corner bet.

**Rival.** Headline conclusion (the 70–75%/25–30% blend): the strongest rival is "invest the
full $60,000," on the view that Vanguard's current forecast is itself overly conservative and
that realized returns will track closer to the historical average (GT-11) — this rival is not
ruled out; it is the live rival named throughout C3/C6/C7's confidence lines. Intermediate chain
C4 (liquidity): the rival "a well-qualified borrower can usually get a HELOC quickly in normal
times, so the illiquidity point is overstated" is not ruled out either — it is true in normal
times, which is precisely why GT-13 specifies *stress* periods as the scenario where it fails;
this rival is named here and is addressed by Pre-mortem Cluster 3's mitigation (not relying on
HELOC access at all for true emergencies). Intermediate chain C1: no live rival — see Recompute.

**Premise.** The recommended plan — pay down ~70–75% with a recast request and invest the
remaining 25–30% — has already failed. What caused it?

**Causes** (generated from the household/executor, a future version of the household 5–10 years
out, a financial-adviser critic, and the mortgage servicer):
1. The extra principal payment was applied by the servicer as an advance future payment rather
   than a principal reduction, because "apply to principal" was never explicitly specified.
2. The household paid down principal but never actually followed through on requesting the
   recast, forfeiting the cash-flow benefit while still taking on the illiquidity downside.
3. The decade turned out to be a strong bull market (realized ~10–12% nominal), and the household
   deeply regrets not investing more, since Vanguard's forecast proved too pessimistic.
4. A real emergency beyond the funded reserve hit during a credit-tightening period; a HELOC
   against the extra home equity was delayed or denied, forcing reliance on high-interest debt.
5. Unused 401(k)/IRA/HSA space was never checked; money that should have gone there first (A-3)
   went into this A-vs-B comparison instead, which was never the best use of the $60,000.
6. Having paid down the mortgage, the household felt "flush" and lifestyle-inflated; conversely,
   having invested, the household panic-sold the index fund during an early drawdown, locking in
   losses (GT-15).
7. The household sold or relocated in year 4 for a job change; the extra principal paid in year 1
   returned as added sale proceeds, but the years 4–10 compounding the "guaranteed 6.25%" framing
   assumed never materialized, so the realized benefit was far smaller than modeled.
8. The servicer sold the loan to a new servicer whose recast policy is stricter or unavailable,
   trapping the household in the no-cash-flow-relief position indefinitely.

**Clusters** (each naming the chain/ground-truth ids it bears on):
- **Execution/process failure** (causes 1, 2) — bears on C4, C7.
- **Forecast error / regret risk** (cause 3) — bears on C2, C3, C6.
- **Correlated tail-risk realized** (cause 4) — bears on C4, C5.
- **Decision scope too narrow** (cause 5) — bears on A-3, C7.
- **Behavioral drift** (cause 6) — bears on C6 (Behavioral criterion), GT-15.
- **Horizon assumption violated — early sale/move** (cause 7) — bears on A-10, C1, C7.
- **Servicer/structural risk to the recast lever** (cause 8) — bears on GT-7, C4, C7.

**Disposition:**
- Execution/process failure → **plan change**: instruct the servicer in writing to "apply to
  principal, not future payments" for every extra payment, and request the recast in the same
  servicing interaction, not "later."
- Forecast error / regret risk → **accepted risk**: explicitly accept that the blend forgoes some
  expected upside if realized returns resemble GT-11 rather than GT-9; the mitigation is the
  25–30% invested tranche, sized specifically to participate in that upside rather than zero.
- Correlated tail-risk realized → **accepted risk with mitigation**: the funded 6-month reserve
  plus the invested tranche are the mitigation for emergencies beyond the reserve; the plan
  explicitly does not rely on HELOC access for emergency liquidity.
- Decision scope too narrow → **plan change**: before executing either leg, confirm whether this
  year's 401(k)/IRA/HSA space is unused, and redirect that portion of the $60,000 there first.
- Behavioral drift → **accepted risk with mitigation**: automate the investment as a single lump
  sum with no active trading, and route any recast-driven payment reduction to an automatic
  savings/investing transfer rather than discretionary spending.
- Horizon assumption violated → **plan change**: if a home sale or relocation within 10 years is
  plausible, shift the split toward investing (lower paydown share), since prepayment's benefit
  is cut short by an early sale while the invested tranche remains fully portable.
- Servicer/structural risk → **accepted risk**: small and worth monitoring as a follow-up item,
  not a reason to abandon the recast request.

**Falsification.** This conclusion is false if, measured over the actual 10-year holding period,
the household's realized diversified after-tax equity return would have exceeded roughly
7.5–7.7%/year compounded, with no offsetting illiquidity, concentration, or behavioral costs
materializing on the paydown side — i.e., if hindsight shows the historical-average regime (GT-11),
not Vanguard's current forecast (GT-9), was the realized path.

Techniques not applied to this step: none — pre-mortem was selected and fully applied because
the headline conclusion is a plan/recommendation, per the decision rule in the pre-mortem
procedure.
## Self-Audit Gate (process output)

**Criterion 1: Identify Essence**
Quoted span: "Given a $240,000 mortgage at 6.25% with no tax shield, and $60,000 in genuinely
surplus cash, should the household eliminate a guaranteed 6.25% obligation or take on market
risk for a potentially higher but uncertain return — and is the honest answer a corner choice
at all, or a specific split between the two?"
Band: **Rigorous**
Justification: The Essence Statement names this specific decision's numbers and tension (not a
generic restatement of the prompt or a symptom), and each of the five success criteria is a
verb+subject+outcome triplet checkable against the Conclusion section (e.g., "names the specific
condition(s) under which the recommendation would flip" is directly checkable against §6's
Confidence line naming GT-9 vs. GT-11).

**Criterion 2: Challenge Assumptions**
Quoted span: "Scan complete: 7 chains, 24 steps scanned in order; 2 assumptions surfaced (A-11
on C2 step 1, A-12 on C5 step 1), both already present in the Classified Assumptions Table (§2)
before this scan was written, confirming no gap between the inline `[Assumes: X]` marks and the
table."
Band: **Rigorous**
Justification: The Assumption Audit scan confirms exhaustive coverage of all 24 named chain
steps with no gap to the table, every row in §2 uses one of the four types with a token-first
em-dash Verdict (Accept/Challenge/Discard) and a specific Verification cell, and multiple
assumptions are Discarded or Challenged rather than uniformly Accepted.

**Criterion 3: Establish Ground Truths**
Quoted span: "`?`-marked: GT-8, GT-10, GT-11, GT-12, GT-13, GT-14 (6 of 14)." / "GT-1 through
GT-5 are user-stipulated problem parameters... and so carry no read-location... GT-6 is a
self-contained financial identity, independently re-derived and checked under Phase 5 Recompute
rather than read from a source."
Band: **Sound**
Justification: IDs are stable, the `?` enumeration matches the list exactly, and GT-7/GT-9
(feeding the HIGH chain C1 via GT-6, and the MEDIUM chains via GT-9) name real read-at-source
locations — but GT-1 and GT-6, which feed the HIGH-confidence chain C1, depart from the
prescribed "read-at-source location" form (one is a user-stipulated input with no external
source, the other a self-derived identity), a specific, disclosed departure rather than an
omission, which is the Sound rather than Rigorous pattern.

**Criterion 4: Reason Upward**
Quoted span: "Scan complete: 7 chain rows, one per section-4 chain block in order; 5 section-6
rows, one per construct in order — 5 claims under R11, 0 excluded. 0 chains malformed, 0 claims
untraced." (self-audit scan, Table 1 reconciliation)
Band: **Rigorous**
Justification: The self-audit scan's chain-form table shows all 7 chains form-conforming with
clean dependencies; every chain carries at least one genuine intermediate; the Abandoned
Reasoning section documents five specific dead ends with precise technical abandonment reasons
(not vague ones); no analogy is used as direct evidence; and the two undeclared assumptions
surfaced by the Assumption Audit (A-11, A-12) are both marked inline with `[Assumes: X]`.

**Criterion 5: Validate**
Quoted span: "GT-11 (`?`) is the named rival, and no verification path exists to resolve it in
advance — whether the next decade's realized return resembles GT-9 or GT-11 is only observable
in hindsight, at the end of the 10-year horizon itself, which is why the recommendation in C7 is
a blend rather than a corner bet on either regime." (chain C3 confidence line)
Band: **Rigorous**
Justification: Every MEDIUM chain names its `?`-marked inputs with either a concrete
verification path (GT-10, GT-13, GT-14) or an explicit, specific account of why no verification
path exists before the horizon elapses (GT-11); no chain consuming a `?` input is rated HIGH;
every chain is rated no higher than the lowest-rated chain its head cites; the §6 Confidence
rating (MEDIUM) matches the weakest contributing chains; and the full adversarial pass record
(Recompute, Sensitivity, Rival, Premise, Causes, Clusters, Disposition, Falsification) is present
with every one of its 7 clusters carrying a named plan change or an explicitly accepted risk with
a named mitigation.

**Criterion 6: Conclusion-to-Ground-Truth Traceability**
Quoted span: "Recommended approach: split 70–75%/25–30%, recast, check retirement space | bold
lead-in | yes | bold lead-in whose colon closes the bold span | C7" (self-audit scan, Table 2,
row 1) — and all 5 rows of Table 2 cite a chain, matching the reconciliation line's "0 claims
untraced."
Band: **Rigorous**
Justification: All 5 Conclusion-section claims trace to named chains (C1, C2, C3, C5, C6, C7
across the four lead-ins plus the Pre-check line), no claim introduces reasoning absent from
section 4, and the Key Insight ("the usual advice does not transfer here because the tax-shield
and forward-return supports are missing") is a non-obvious finding distinct from the Recommended
approach's specific 70/25 split-and-recast instruction.

**Pass 1 (before re-score):** not applicable — this is the analysis's only scoring pass; no
criterion scored Absent and at most one scored Hand-wavy (zero did), so the Fix/Repeat loop did
not fire.

**Gate result:** cleared · passes: 1 · Fix/Repeat fired: no
## Structured summary (process output)

```json
{
  "schema_version": 1,
  "run_mode": "full-composer",
  "assumptions": [
    {
      "id": "A-1",
      "type": "convention",
      "verdict": "Discard"
    },
    {
      "id": "A-2",
      "type": "untested belief",
      "verdict": "Challenge"
    },
    {
      "id": "A-3",
      "type": "untested belief",
      "verdict": "Challenge"
    },
    {
      "id": "A-4",
      "type": "convention",
      "verdict": "Discard"
    },
    {
      "id": "A-5",
      "type": "convention",
      "verdict": "Discard"
    },
    {
      "id": "A-6",
      "type": "current constraint",
      "verdict": "Accept"
    },
    {
      "id": "A-7",
      "type": "convention",
      "verdict": "Discard"
    },
    {
      "id": "A-8",
      "type": "convention",
      "verdict": "Discard"
    },
    {
      "id": "A-9",
      "type": "untested belief",
      "verdict": "Discard"
    },
    {
      "id": "A-10",
      "type": "untested belief",
      "verdict": "Challenge"
    },
    {
      "id": "A-11",
      "type": "current constraint",
      "verdict": "Accept"
    },
    {
      "id": "A-12",
      "type": "untested belief",
      "verdict": "Challenge"
    }
  ],
  "ground_truths": [
    {
      "id": "GT-1",
      "read_at_source": true
    },
    {
      "id": "GT-2",
      "read_at_source": true
    },
    {
      "id": "GT-3",
      "read_at_source": true
    },
    {
      "id": "GT-4",
      "read_at_source": true
    },
    {
      "id": "GT-5",
      "read_at_source": true
    },
    {
      "id": "GT-6",
      "read_at_source": true
    },
    {
      "id": "GT-7",
      "read_at_source": true
    },
    {
      "id": "GT-8",
      "read_at_source": false
    },
    {
      "id": "GT-9",
      "read_at_source": true
    },
    {
      "id": "GT-10",
      "read_at_source": false
    },
    {
      "id": "GT-11",
      "read_at_source": false
    },
    {
      "id": "GT-12",
      "read_at_source": false
    },
    {
      "id": "GT-13",
      "read_at_source": false
    },
    {
      "id": "GT-14",
      "read_at_source": false
    }
  ],
  "chains": [
    {
      "id": "C1",
      "confidence": "HIGH",
      "rests_on": [
        "GT-1",
        "GT-6"
      ]
    },
    {
      "id": "C2",
      "confidence": "MEDIUM",
      "rests_on": [
        "GT-9",
        "GT-10",
        "GT-3"
      ]
    },
    {
      "id": "C3",
      "confidence": "MEDIUM",
      "rests_on": [
        "GT-3",
        "C1"
      ]
    },
    {
      "id": "C4",
      "confidence": "MEDIUM",
      "rests_on": [
        "GT-7",
        "GT-4",
        "GT-13"
      ]
    },
    {
      "id": "C5",
      "confidence": "MEDIUM",
      "rests_on": [
        "GT-14",
        "C4"
      ]
    },
    {
      "id": "C6",
      "confidence": "MEDIUM",
      "rests_on": [
        "C1",
        "C2",
        "C4",
        "C5"
      ]
    },
    {
      "id": "C7",
      "confidence": "MEDIUM",
      "rests_on": [
        "C6",
        "GT-7",
        "C5"
      ]
    }
  ],
  "dead_ends": [
    "Naive \"stocks always win over 10 years\" reasoning",
    "Naive \"pay off debt = always safe\" reasoning",
    "Annual-18%-on-everything tax model for Option B",
    "Pure 100% Option B as the headline recommendation",
    "Pure 100% Option A as the headline recommendation (no invested tranche)"
  ],
  "techniques": {
    "applied": [
      "inversion",
      "estimate",
      "trade-off",
      "second-order",
      "pre-mortem"
    ],
    "not_applied": [
      {
        "technique": "fishbone",
        "phase": 2,
        "reason": "the assumption space here was tractable by direct enumeration plus inversion; it was not a multi-causal breadth problem needing category brainstorming"
      },
      {
        "technique": "five-whys",
        "phase": 3,
        "reason": "the ground truths used either bottom out directly at a self-contained financial identity (GT-6) or at read-at-source/reported figures; none required recursive decomposition into constituent facts to verify"
      },
      {
        "technique": "theoretical-limit",
        "phase": 4,
        "reason": "the question is a risk-adjusted guaranteed-vs-uncertain comparison, not a what-do-the-fundamentals-permit ceiling question"
      }
    ]
  },
  "gate": {
    "passes": [
      {
        "bands": [
          "Rigorous",
          "Rigorous",
          "Sound",
          "Rigorous",
          "Rigorous",
          "Rigorous"
        ],
        "gate_cleared": true,
        "hand_wavy_cap_cleared": true
      }
    ],
    "fix_repeat_fired": false,
    "cleared": true
  },
  "re_entry": {
    "fired": false,
    "edges": []
  },
  "conclusion": {
    "recommendation": "Split the $60,000 roughly 70–75% toward extra mortgage principal (~$42,000–$45,000) and explicitly request a loan recast from the servicer so the paydown actually lowers the required monthly payment, and invest the remaining 25–30% (~$15,000–$18,000) as a lump sum in the taxable broad-market index fund (chain C7). Before executing either leg, confirm whether this year's 401(k)/IRA/HSA space is unused — if so, redirect that portion of the $60,000 there first, since it was never priced into this A-vs-B comparison (A-3, chain C7).",
    "confidence": "MEDIUM",
    "rests_on": [
      "C1",
      "C3",
      "C6",
      "C7"
    ]
  }
}
```
