# First-Principles Analysis: $60,000 — Mortgage Paydown vs. Taxable Equity Investment

Prepared 2026-10-08. Decision horizon: 10 years.

## Techniques not applied (process output)

- `theoretical-limit` — not applicable — no governing hard physical/legal ceiling applies beyond the two definitional identities already used as derivation inputs (loan-amortization compounding; capital-gains/dividend tax mechanics). There is no "fundamentals-stripped" ceiling to derive beyond those.
- `fishbone` — not applicable — this is a two-option quantitative comparison with a bounded, already-enumerable cause/consideration set, not a multi-causal diagnostic problem needing breadth-first cause-category brainstorming.
- `five-whys` (reduce-to-primitives mode) — applied in reduced form only — each ground truth below bottoms out directly at a direct measurement (a quoted market yield/rate) or a contractual/statutory definition (loan terms, tax-rate brackets) without requiring further recursive decomposition; no compound claim required a multi-level drill.
- `inversion` at Phase 5 — not applicable — the conclusion is a recommendation/plan (an allocation of $60,000), not a bare claim, so Pre-Mortem is the prescribed Phase-5 adversarial technique, not Inversion. (Inversion is applied at Phase 2 below, challenging the "equities will win" assumption.)

## Assumption Audit scan (process output)

One row per section-4 derivation-chain step, in order. "Added to Table?" of `n/a (pre-existing, Phase 2)` means the assumption was anticipated during Phase 2 (via the Inversion pass on the core "equities will win" belief) and already carries a row in the Assumptions Table below; `yes` means the assumption was first surfaced here at Phase 4 and a new row was added.

| Chain | Step | Step Text (brief) | Assumption surfaced? | Added to Table? |
|---|---|---|---|---|
| C1 | 1 | prepaying at 6.25% APR locks in a 6.43% effective annual, tax-free return | none | n/a |
| C1 | 2 | that return is already after-tax (no shield forgone) | none | n/a |
| C1 | 3 | $60,000 compounds to $111,914 of equity in 10 years | A-3 (no recast requested) | n/a (pre-existing, Phase 2) |
| C2 | 1 | split pretax return into dividend leg + price-appreciation leg | none | n/a |
| C2 | 2 | tax dividend leg annually, price leg once at sale | A-10 (28%/18% rates stay stable for 10 years) | yes |
| C2 | 3 | run the model across the four scenario anchors | A-6 (historical anchors are illustrative, not forecasts) | n/a (pre-existing, Phase 2) |
| C3 | 1 | solve for breakeven pretax equity CAGR (~7.53%) | none | n/a |
| C3 | 2 | compare breakeven to Vanguard's 6.2% forecast ceiling | none | n/a |
| C3 | 3 | compare breakeven to the 10-yr Treasury risk premium | A-5 (Vanguard's model is an unbiased base case) | n/a (pre-existing, Phase 2) |
| C4 | 1 | tax the Treasury yield to ~3.76% after-tax | none | n/a |
| C4 | 2 | Option A dominates holding Treasuries | A-2 (no prepayment penalty applies) | n/a (pre-existing, Phase 2) |
| C5 | 1 | concentration / optionality cost of 100% A | none | n/a |
| C5 | 2 | actor lens: household's own future self loses flexibility | none | n/a |
| C5 | 3 | time lens: cash flow is unchanged near-term without recast | A-3 (no recast requested) | n/a (pre-existing, referenced again) |
| C5 | 4 | time lens: fixed-debt inflation hedge is forfeited | A-11 (future inflation path is uncertain) | yes |
| C6 | 1 | trade-off calibration reasoning for the blend split | A-12 (2:1 split is right-sized for an unstated risk tolerance) | yes |
| C6 | 2 | quantify blend ending values across scenarios | none | n/a |

## Adversarial pass (process output)

The headline conclusion is a plan/recommendation (how to split $60,000), so Pre-Mortem is the prescribed Phase-5 adversarial technique (not Inversion, which was already used at Phase 2).

**Recompute.** Monthly payment on GT-1's loan: $240,000 × (0.0625/12) ÷ (1 − (1+0.0625/12)^−324) recomputes to $1,535.25/mo. Effective annual rate from monthly compounding of 6.25% APR: (1+0.0625/12)^12 − 1 recomputes to 6.433%. Ten-year compounding factor: (1+0.0625/12)^120 recomputes to 1.8652, so $60,000 → $111,914 (chain C1) recomputes cleanly. Breakeven pretax equity CAGR: re-solving chain C3's after-tax model independently at a trial 7.5% pretax input gives an ending multiple of ≈1.860, just under C1's 1.8652 target, confirming the true breakeven sits marginally above 7.5% — consistent with the stated ≈7.53%.

**Sensitivity.** The single ground truth whose falsity would most flip the conclusion is **GT-1?** (the loan's actual rate/balance/tax-shield status) — it is self-reported and `?`-marked, and the entire guaranteed-6.43% edge that anchors chains C1, C3, C4, C5, C6 is a direct function of it. Verification: read the loan's amortization statement and the household's actual Schedule A / standard-deduction math (most recent Form 1040) to confirm GT-1 and GT-2 as stated.

**Rival.** Strongest rival to the headline blend: "US equities deliver the ~10%/yr historical average (GT-7?) over 2026–2036, so 100% Option B ($137,740) beats both the blend ($120,523) and 100% Option A ($111,914)." This rival is live and **not settled** by this analysis — no observation available in 2026 can determine 2036's realized return; it resolves only with the passage of time (see chain C3's confidence line). For the intermediate chains: C1's guaranteed-return claim has no live rival (it is a compounding-interest identity, not a forecast) — **rival not applicable — C1 is a definitional/arithmetic claim, not a contested one**. C4's "A dominates holding Treasuries" claim has no live rival at these spreads (6.43% guaranteed vs. 3.76% after-tax, a >250bp gap) — **rival not applicable — the margin is too large for a plausible rival reading of the same ground truths**.

**Premise.** It is 2036. The household followed the recommended $40,000/$20,000 blend, and in hindsight this allocation has already turned out to be a mistake — either because it left too much tied up in an under-performing, illiquid house while equities boomed, or because it left too much exposed to markets right before a prolonged downturn, or because the household's actual 2026 circumstances made the A-vs-B framing itself wrong from the start.

**Causes (unfiltered, from named viewpoints).**
*Household's future (2036) self:* (1) equities delivered the ~10%/yr historical average and the household deeply regrets not going 100% Option B; (2) a 2000-2010-style decade hit and the household regrets not going 100% Option A; (3) the household needed liquidity beyond its 6-month reserve around year 6 (job loss, medical event) and the $40,000 in home equity was slow/expensive to access; (4) the household sold or moved before year 10, and transaction costs/timing ate into the assumed $111,914 equity gain.
*Mortgage servicer / lender:* (5) the servicer offered no low-cost recast, so the household never got the monthly cash-flow relief it expected from paying down principal; (6) an overlooked prepayment penalty clause reduced the realized guaranteed return below 6.43%.
*A financial advisor reviewing the decision in hindsight:* (7) the household had unused 401(k)/IRA/HSA tax-advantaged space in 2026 that neither Option A nor Option B used, and that space would have dominated both; (8) tax law changed mid-decade (standard deduction, SALT cap, etc.), partially restoring the mortgage-interest shield and shrinking Option A's edge versus what was assumed; (9) the household over-anchored on one institution's (Vanguard's) single point-in-time forecast.
*Household's future self under market stress:* (10) during a sharp equity drawdown in year 3-4, the household panic-sold the $20,000 equity position near a bottom, a behavioral failure independent of whether the underlying math was right.

**Clusters.**
- **Forecast-direction risk** (causes 1, 2, 9) — bears on C3, GT-5, GT-7?, GT-8?.
- **Liquidity/access-cost risk** (causes 3, 4) — bears on C5, GT-4?.
- **Mechanical/servicing risk** (causes 5, 6) — bears on C1, A-2, A-3.
- **Opportunity-cost/framing risk** (causes 7, 8) — bears on A-4, GT-1?, GT-2?.
- **Behavioral-execution risk** (cause 10) — bears on C5's behavioral discussion.

**Disposition.**
- Forecast-direction risk — **accepted risk**; mitigation: the blend (chain C6) is itself the mitigation (it avoids betting all $60,000 on forecast direction); revisit the split if a comparable institution's 10-year forecast moves materially, rather than treating the split as permanent.
- Liquidity/access-cost risk — **plan change**: confirm with the servicer, before sending money, whether a low-cost recast is available; if not, shift the split toward $30,000/$30,000 to preserve more liquid buffer.
- Mechanical/servicing risk — **plan change**: verify directly with the servicer that no prepayment penalty applies and what recast fees/options exist before executing Option A.
- Opportunity-cost/framing risk — **plan change**: confirm 401(k)/IRA/HSA space is already maximized for this and future years before finalizing either option; if not, that space likely dominates both A and B and should be resolved first.
- Behavioral-execution risk — **accepted risk**; mitigation: automate the equity portion as a no-touch buy-and-hold position; treat the mortgage-paydown portion as the deliberately un-sellable "sleep at night" anchor.

**Falsification.** This recommendation is false — i.e., a materially different split would clearly have been better — if, with 2036 hindsight, either (a) realized pretax US equity CAGR over 2026-2036 was at or above ≈7.5%/yr nominal, in which case more should have gone to Option B, or (b) the household faced a genuine liquidity need beyond its emergency reserve that the illiquid $40,000 portion could not cheaply meet, in which case less should have gone to Option A.

---

## 1. Problem Essence

**Core problem:** Given $240,000 of 6.25% fixed-rate, tax-shield-less mortgage debt and $60,000 of genuinely surplus cash, how should that $60,000 be split between (a) extinguishing debt that carries a guaranteed, tax-free 6.25%/6.43%-effective cost, and (b) taking on diversified, taxed, uncertain equity risk — so as to maximize risk-adjusted household net worth at a fixed 10-year horizon, net of the fact that one path converts to illiquid home equity and the other stays liquid?

**Success criteria:**
1. The recommendation states a specific dollar split (not just "it depends") and the split traces to a quantified comparison between a guaranteed return and a bracketed range of after-tax equity outcomes.
2. The guaranteed after-tax return of paying down the mortgage is stated as a number, derived from the loan's actual terms, not estimated by analogy.
3. The equity side is modeled after-tax with dividend drag taken annually and capital-gains drag taken once at sale (deferred), not with a single blanket "stocks return X%" assumption.
4. The comparison is explicitly risk-adjusted — a bracket of equity outcomes (including a realistic bad decade) is weighed against the mortgage paydown's certainty, not just a single expected-value number.
5. Liquidity, concentration, inflation-hedge, and behavioral effects are named as real costs/benefits distinct from the raw return numbers, with second-order (actor + time lens) reasoning, not just return math.

---

## 2. Assumptions Table

| Assumption | Type | Treatment | Verdict | Verification |
|---|---|---|---|---|
| A-1: Mortgage interest provides zero marginal tax benefit under the household's standard deduction | current constraint | record expiry — a future year with enough itemizable deductions (large medical bills, charitable gifts, SALT-cap changes) could restore partial shield value | Accept — stated directly by the user as a given fact about current tax position | GT-1?/GT-2? (user-stipulated) |
| A-2: No prepayment penalty applies to extra principal payments on this loan | convention | challenge before use — near-universal for post-2014 conforming US mortgages, but not legally guaranteed for every loan | Challenge — plausible default, not confirmed by the user | unverified — flagged |
| A-3: After a $60,000 lump-sum prepayment, the servicer does not recast the loan (payment stays ≈$1,535.25/mo; term shortens instead) | convention | challenge — this is default servicer behavior unless recast is explicitly requested and paid for | Challenge — load-bearing for chain C1's exact dollar figure and for C5's near-term cash-flow claim | unverified — flagged |
| A-4: The $60,000 has no competing near-term use (no unfunded 401(k)/IRA/HSA headroom, no planned purchase) | untested belief | verify or flag | Challenge — the user confirmed it is surplus to the emergency reserve specifically, not surplus to every other goal | unverified — flagged |
| A-5: Vanguard's VCMM 10-year forecast (4.2%-6.2% nominal, GT-5) is a reasonable, unbiased base case rather than systematically too conservative | convention | challenge explicitly before using as the base case | Challenge — Vanguard's own past vintages have at times underestimated subsequent realized returns; the forecast is valuation-driven and assumes mean reversion that may not occur on this horizon | GT-5 (figure itself read-at-source; its *accuracy* is unverifiable in advance by construction) |
| A-6: The 10%/yr historical-average (GT-7?) and the -0.9%/yr "lost decade" (GT-8?) anchors are useful for *bracketing tail outcomes*, not for predicting 2026-2036 | convention / reasoning-by-analogy | challenge explicitly; used only as illustrative analogy, never as direct evidence of the forecast itself | Challenge — explicitly scoped to the Pre-Mortem/tail-risk discussion, not to the headline breakeven comparison | GT-7?/GT-8? unverified in this session (aggregator-reported, not read at a primary dataset) |
| A-7: A broad, low-cost total-US-market index fund is a reasonable proxy for "the" equity option, with no stock-picking/market-timing edge assumed | convention | accept, lightly challenged — consistent with the user's own framing and well-supported by evidence on active-management underperformance net of fees | Accept | not separately re-sourced this session; treated as well-established background |
| A-8: The household will not be forced to sell the home or urgently extract equity within 10 years in a way that crystallizes Option A's illiquidity cost | untested belief | verify or flag | Challenge — plausible given the horizon and the already-funded emergency reserve, but not confirmed | unverified — flagged |
| A-9: Equities will outperform the guaranteed mortgage-paydown return over this specific 10-year window (the core bet Option B requires) | untested belief | surfaced via Inversion: invert to "equities underperform," enumerate failure-guaranteeing conditions (flat/negative decade, sequence risk near year 10, valuation reversion, behavioral panic-selling) | Challenge — the single most load-bearing untested belief in the comparison; addressed quantitatively in chains C2/C3 and in the Pre-Mortem | unverified — flagged |
| A-10: The 28% ordinary / 18% LTCG+dividend tax rates (GT-2?) remain stable over the full 10-year holding period | untested belief | verify or flag | Challenge — US tax law has changed on shorter cycles than 10 years before | unverified — flagged |
| A-11: The future inflation path is uncertain and could run persistently higher than the ~2-3% implicitly priced into current forecasts, raising fixed-debt's hedge value | current constraint | record expiry — holds only while inflation stays near current/forecast levels; a sustained move materially above or below that changes the hedge's value | Challenge — GT-9? shows 3.4% YoY already running above the Fed's ~2% target | unverified — flagged |
| A-12: A roughly 2:1 (Option A : Option B) split is close to the right calibration point for this household, rather than requiring a different split | untested belief | flag explicitly as risk-tolerance- and goal-dependent; this is the one assumption the Conclusion's clarifying questions ask the user to confirm or correct | Challenge — genuinely contingent on risk tolerance and on A-4/A-8 above, not resolvable from the numbers alone | unverified — flagged |

---

## 3. Ground Truths

- **GT-1?** Mortgage: $240,000 balance, 30-year fixed-rate loan, 6.25% APR, 27 years (324 months) remaining; household takes the standard deduction, so mortgage interest currently provides zero marginal tax-shield value — unverified: self-reported household/account data; no external document exists for this analysis to open and check it against.
- **GT-2?** Marginal tax rates: ≈28% combined federal+state on ordinary income; ≈18% on long-term capital gains and qualified dividends — unverified: self-reported.
- **GT-3** 10-year US Treasury constant-maturity par yield = **5.22%** as of 10/08/2026 — source: U.S. Department of the Treasury, daily treasury par yield curve rates; read-at-source: raw CSV (`daily-treasury-rates.csv`, October 2026, "10 Yr" column, row dated 10/08/2026 = 5.22) downloaded and read directly by this analysis via `curl`, not merely summarized by a delegate.
- **GT-4?** Freddie Mac PMMS 30-year fixed mortgage market average ≈7.03%-7.28% as of October 1, 2026 (new-purchase/refinance context, used only to show the gap between the household's legacy rate and today's market rate) — cited to: Freddie Mac PMMS via Trading Economics; reported-by-delegate: WebSearch summary, source not opened directly by this analysis.
- **GT-5** Vanguard Capital Markets Model (VCMM), Q2-2026 update: 10-year expected annualized nominal return for U.S. equities (MSCI US Broad Market Index) = **4.2%-6.2%**, explicitly stated as nominal — "do not account for inflation, taxes, or investment expenses" — read-at-source: `corporate.vanguard.com/.../vemo-return-forecasts.html`, raw page text fetched and grepped directly by this analysis; quoted passage: *"our 10-year expected annualized return for U.S. equities declined from a range of 4.9%–6.9% to a range of 4.2%–6.2%"* and *"these...are in nominal terms—meaning they do not account for inflation, taxes, or investment expenses."*
- **GT-6?** Broad-market US total-market index fund (VTI, used as the "total US stock market index fund" proxy) trailing/forward dividend yield ≈1.05%-1.13% as of mid/late 2026 — cited to: multiple dividend-data aggregator sites; reported-by-delegate: WebSearch summary, not opened directly; this analysis rounds to **1.2%** as a conservative (slightly-higher-than-observed) working assumption, since a higher assumed yield increases annual dividend-tax drag and is therefore the conservative direction for Option B.
- **GT-7?** Historical long-run US equity nominal total return ≈10%/yr since 1926 (dividends reinvested; price-appreciation-only component ≈6-7%/yr) — cited to: widely-referenced long-run market-history series, reported via general financial-commentary aggregator sites; reported-by-delegate: WebSearch summary, not opened at a primary dataset. Used **only** as an illustrative historical-analogy anchor for the optimistic tail (per A-6), never as direct forecast evidence.
- **GT-8?** "Lost decade" 2000-2010: S&P 500 annualized total return ≈ -0.9% to -0.95% nominal over that specific 10-year window — cited to: financial-commentary/data aggregator sites; reported-by-delegate: WebSearch summary, not opened at a primary dataset. Used **only** as an illustrative sequence-risk/tail-scenario anchor (per A-6), never as direct forecast evidence.
- **GT-9?** Current US CPI inflation ≈3.4% YoY (August 2026, most recent print before October 8, 2026) — cited to: Trading Economics/BLS-sourced reporting; reported-by-delegate: WebSearch summary, not opened directly. Used only as qualitative context for the inflation-hedge discussion (chain C5), not as a load-bearing numeric input to the CAGR math.

**Provenance summary (required):**
`?`-marked: GT-1, GT-2, GT-4, GT-6, GT-7, GT-8, GT-9 (7 of 9).
Read-at-source: GT-3 — Treasury daily-par-yield CSV, October 2026, "10 Yr" column, row 10/08/2026 (value 5.22); GT-5 — `corporate.vanguard.com` VEMO return-forecasts page, raw fetched text, "Key changes since March 31, 2026" / U.S. equities paragraph, quoted verbatim above.
No assumption that was assigned a Discard verdict in Phase 2 appears in this list (none were discarded; all survived with Accept or Challenge).

---

## 4. Derivation Chains

### Conclusion C1: Paying down the mortgage delivers a guaranteed, tax-free 6.43% effective annual return

GT-1? (loan: $240,000 bal., 6.25% APR, 324mo remaining, no tax shield) + GT-2? (28%/18% marginal rates, confirming no shield is being forgone)
→ prepaying principal on a loan whose 6.25% APR compounds monthly locks in a 6.43% effective annual, risk-free return on every dollar prepaid, since (1+0.0625/12)^12 − 1 = 6.433%
→ that return is already after-tax because GT-1 establishes no interest deduction is being sacrificed by paying it off sooner
→ compounding $60,000 at 6.433%/yr for 10 years produces $111,914 of additional home equity with certainty, independent of market outcomes, assuming the loan is not recast to a lower payment *[Assumes: A-3 — no recast; if the household instead recasts after prepaying, principal reduction slows and the realized equity figure would be smaller than $111,914, though the per-dollar guaranteed rate on the amount prepaid is unaffected]*

**Pre-check:** head GT-1?, GT-2? · ?-marked: GT-1?, GT-2? · lowest cited: none · Inputs ceiling: MEDIUM
**Confidence:** MEDIUM — GT-1? and GT-2? are both self-reported and unverified; verification would mean reading the loan's amortization statement and the household's actual Form 1040/Schedule A. The A-3 premise is priced (stated above) and does not change the qualitative endpoint, only the exact dollar figure, so it does not independently lower the band below what GT-1?/GT-2? already cap it at.

### Conclusion C2: After-tax, 10-year ending value of $60,000 invested in a broad-market index fund spans roughly $55,000-$138,000 depending on realized equity returns

GT-2? (28%/18% marginal rates) + GT-5 (Vanguard 10-yr nominal US equity forecast, 4.2%-6.2%) + GT-6? (broad-market dividend yield ≈1.2%, rounded up conservatively)
→ splitting each pretax scenario return into a ≈1.2% annually-taxed dividend yield and a price-appreciation remainder taxed once at sale models how the fund is actually taxed
→ taxing the dividend leg annually at 18% and the price-appreciation leg once, at sale, at 18% on the accumulated gain produces an after-tax 10-year ending-value multiple for any given pretax scenario *[Assumes: A-10 — tax rates stay at 28%/18% for the full decade]*
→ running that model at Vanguard's 4.2% and 6.2% bounds (GT-5), its 5.2% midpoint, the 10%/yr historical-average anchor (GT-7?), and the -1.0%/yr "lost decade" anchor (GT-8?) yields after-tax 10-year ending values on $60,000 of $84,598 (pessimistic, 4.2%), $91,994 (base, Vanguard midpoint 5.2%), $137,740 (optimistic/historical-average, 10%), and $55,234 (severe-downside/lost-decade analogy, -1.0%) *[Assumes: A-6 — the 10% and -1.0% outer anchors are illustrative historical analogies used only to bracket tail risk, not forecasts; the base/pessimistic figures rest on GT-5 alone and do not depend on this assumption]*

**Pre-check:** head GT-2?, GT-5, GT-6? · ?-marked: GT-2?, GT-6? · lowest cited: none · Inputs ceiling: MEDIUM
**Confidence:** MEDIUM — GT-2? (future tax-rate stability) and GT-6? (current fund dividend yield, delegate-reported) are unverified; verification would mean confirming the fund's actual trailing yield from its own prospectus/fact sheet and tracking any tax-law changes over the holding period. A-6 is priced above: the headline base/pessimistic figures this chain feeds into chain C3 do not depend on it, only the illustrative bookends used in the Pre-Mortem do.

### Conclusion C3: Equities must clear roughly a 7.53%/yr pretax return just to tie the guaranteed paydown — above Vanguard's own forecast ceiling

C1 (guaranteed $111,914 / 6.43%) + C2 (after-tax equity scenario ladder) + GT-3 (10-yr Treasury yield, 5.22%, read-at-source)
→ solving chain C2's after-tax model for the pretax equity CAGR that reproduces chain C1's $111,914 endpoint gives a breakeven requirement of about 7.53%/yr pretax nominal
→ Vanguard's own forecast ceiling of 6.2% (GT-5) sits roughly 130 basis points below that breakeven, so equities would need to beat the top of Vanguard's own forecast range just to tie the guaranteed paydown, not to beat it with any margin
→ measured against GT-3's 5.22% risk-free yield, clearing the breakeven requires a pretax equity risk premium of roughly 2.3 percentage points over Treasuries, which sits at the low-to-middle end of commonly cited historical risk-premium ranges and is therefore not a comfortable margin of safety for concentrating a single, undiversified 10-year equity bet *[Assumes: A-5 — Vanguard's model-implied base case is a reasonable, unbiased forecast rather than systematically too conservative; if A-5 is wrong in the optimistic direction, Option B's case strengthens materially and this conclusion weakens accordingly]*

**Pre-check:** head C1 (MEDIUM), C2 (MEDIUM), GT-3 · ?-marked: none · lowest cited: MEDIUM · Inputs ceiling: MEDIUM
**Confidence:** LOW — two axes are short. Inputs: capped at MEDIUM because this chain cites C1 and C2, both MEDIUM (verification path: resolve GT-1?/GT-2?/GT-6? as described on those chains). Rivals: the live rival — "realized 10-year equity CAGR exceeds ~7.53%, so Option B actually wins" — is not settled by this analysis; no observation available in 2026 can settle it, since it resolves only with the passage of time to 2036. A-5 is priced above and does not independently add a third shortfall.

### Conclusion C4: Holding the $60,000 in Treasuries instead of either option is dominated by Option A

GT-3 (10-yr Treasury yield, 5.22%) + GT-2? (28% ordinary rate) + C1 (guaranteed 6.43% from Option A)
→ taxing GT-3's 5.22% Treasury yield at the 28% ordinary rate (Treasury interest is federally taxable though state-exempt, so this slightly understates the true after-tax yield) gives an after-tax yield of about 3.76%/yr
→ 3.76% is more than 250 basis points below chain C1's guaranteed, tax-free 6.43%, so parking the $60,000 in Treasuries instead is dominated by Option A and is not a live third alternative for this surplus *[Assumes: A-2 — no prepayment penalty blocks the paydown; even a meaningful penalty would need to exceed roughly 2.5 percentage points of the prepaid amount to erase this gap]*

**Pre-check:** head GT-3, GT-2?, C1 (MEDIUM) · ?-marked: GT-2? · lowest cited: MEDIUM · Inputs ceiling: MEDIUM
**Confidence:** MEDIUM — GT-2? is unverified (verification: confirm actual marginal rate from a recent return); C1 is MEDIUM for the reasons stated on that chain. A-2 is priced above and the margin is wide enough that no live rival survives at these spreads.

### Conclusion C5: Going 100% into Option A carries liquidity, concentration, and inflation-hedge costs the raw return numbers do not capture

C1 (guaranteed but illiquid equity-building) + C3 (moderate, uncertain risk-adjusted edge to A) + GT-4? (current new-money mortgage/refi rates ≈7.0%-7.3%)
→ fully executing Option A further concentrates net worth in one illiquid, undiversified asset — the home — and forecloses the option to borrow this $60,000 back cheaply later, since GT-4 shows new borrowing today costs roughly 80-180 basis points more than the loan being extinguished
→ because this is a household balance-sheet decision rather than a competitive market, the dominant actor-lens effect is the household's own future self facing a less flexible balance sheet if it needs liquidity before year 10
→ in the near term, cash flow is identical under either option, since a non-recast prepayment does not lower the required payment, so none of Option A's benefit is felt as freed-up monthly cash until the loan is refinanced, recast, or paid off *[Assumes: A-3 — no recast requested]*
→ over the full 10 years, preserving the fixed 6.25% debt instead of extinguishing it also preserves an inflation hedge: if inflation runs persistently above the roughly 2-3% implicit in current forecasts, the real cost of the fixed nominal payments falls further, a benefit Option A forfeits by paying the debt off early *[Assumes: A-11 — future inflation could run persistently higher than currently priced]*

**Pre-check:** head C1 (MEDIUM), C3 (LOW), GT-4? · ?-marked: GT-4? · lowest cited: LOW · Inputs ceiling: LOW
**Confidence:** LOW — capped by citing C3 (LOW); GT-4? is also unverified (verification: confirm current refi/HELOC quotes directly from a lender). A-3 and A-11 are priced above.

### Conclusion C6: A roughly $40,000-to-mortgage / $20,000-to-equities blend is better-calibrated to the uncertainty than either pure option

C1 (guaranteed but moderate, illiquid edge) + C3 (moderate, uncertain-but-real net edge to A) + C5 (real liquidity/diversification/inflation-hedge costs of going 100% A)
→ weighing a guaranteed-but-moderate expected-value edge toward Option A (chain C3) against the real liquidity, diversification, and inflation-hedge costs of going 100% Option A (chain C5) means neither pure allocation is dominant, so a split that locks in most of the guaranteed edge while preserving some liquidity and diversification fits the actual uncertainty better than an all-or-nothing choice
→ sizing that split at roughly two-thirds to Option A and one-third to Option B ($40,000/$20,000) captures about 94% of Option A's base-case extra value ($105,274 of $111,914), cuts the severe-downside shortfall versus 100% A from about $56,680 to about $18,893, and keeps $20,000 fully liquid and diversified *[Assumes: A-12 — a 2:1 split is close to right-sized for this household's unstated risk tolerance and goals; a more risk-averse or more liquidity-constrained household should shift toward $30,000/$30,000, a more risk-tolerant one toward $50,000/$10,000 or further]*

**Pre-check:** head C1 (MEDIUM), C3 (LOW), C5 (LOW) · ?-marked: none · lowest cited: LOW · Inputs ceiling: LOW
**Confidence:** LOW — capped by citing C3 and C5 (both LOW). A-12 is priced above: the direction of the recommendation (a blend tilted toward A, not a pure extreme) is robust to reasonable risk-tolerance variation, but the exact split (40/20 vs. 30/30 vs. 50/10) is not pinned down by the math alone and is named explicitly as a clarifying question in the Conclusion.

---

## 5. Abandoned Reasoning

### Dead End: Weighted trade-off matrix scoring liquidity, diversification, and inflation-hedge as independent criteria

**What was tried:** A formal weighted-criteria trade-off table was built across six criteria (guaranteed/risk-adjusted return, expected value, liquidity, diversification, inflation-hedge/optionality, behavioral simplicity), with weights locked before scoring, comparing 100% A, 100% B, a 70/30 blend, and a 50/50 blend.

**Why abandoned:** Three of the six criteria (liquidity, diversification, inflation-hedge/optionality) were each scored as a simple linear function of "fraction of the $60,000 allocated to equities" — meaning they were not independent considerations but the same underlying axis counted three times. This collinearity mechanically biased the weighted sum toward whichever option maximized equity allocation (Option B), to the point that no feasible weight on the guaranteed-return criterion (bounded 1-5 per the trade-off procedure's own scale) could flip the result back to Option A, even at the maximum weight. That is an artifact of the scoring design, not a genuine finding about the decision.

**What it ruled out:** It ruled out trusting a single weighted-sum number as the basis for the blend's sizing. Chain C6's sizing instead reasons directly from the quantified outcomes in chains C1/C3/C5 (dollar-denominated scenario outcomes and their spreads) rather than from an internally-collinear point score.

### Dead End: Using an unsourced 6.5% "base case" pretax equity return

**What was tried:** Before locating Vanguard's actual current forecast, an initial base-case scenario used 6.5%/yr pretax nominal equity return, recalled from general familiarity with institutional long-term capital-market assumptions rather than from a dated, sourced figure.

**Why abandoned:** Once GT-5 (Vanguard's Q2-2026 VCMM forecast, read at source: 4.2%-6.2%, midpoint ≈5.2%) was located, the unsourced 6.5% figure sat above even the top of a current, dated, directly-read institutional forecast. Using it would have overstated Option B's base-case expected value ($102,616 vs. the correctly-sourced $91,994) and understated Option A's edge, violating the no-reasoning-by-analogy discipline for a number that matters as much as the base case does.

**What it ruled out:** It ruled out relying on recalled/background financial "common knowledge" figures for any number feeding the headline breakeven comparison (chain C3); only read-at-source or explicitly-flagged illustrative-analogy figures (GT-7?/GT-8?, used only for the Pre-Mortem's tail brackets, never for the base case) were used downstream of this point.

### Dead End: Recommending "hold the $60,000 in Treasuries" as a middle-ground option

**What was tried:** Considered recommending that the surplus (or part of it) simply sit in 10-year Treasuries as a "safe" alternative to both paying down the mortgage and taking equity risk.

**Why abandoned:** Chain C4 shows this option is strictly dominated — a 5.22% pretax/≈3.76% after-tax Treasury yield (GT-3) is more than 250 basis points below the guaranteed, tax-free 6.43% available simply by paying down the mortgage (chain C1), with no offsetting benefit (Treasuries are no more liquid than a brokerage account, and the mortgage paydown is already risk-free). This is an absent-fails-style result: the premise that would make Treasuries attractive here (a competitive or superior safe yield) is false.

**What it ruled out:** It ruled out a three-way split across mortgage/equities/Treasuries; the comparison correctly collapses to the two options the user posed, confirming (rather than just assuming) that framing.

---

## 6. Conclusion

**Recommended approach:** Split the $60,000 roughly two-to-one toward debt paydown: apply **$40,000 to mortgage principal** and invest **$20,000 in a broad-market taxable index fund**, rather than committing the full amount to either Option A or Option B (chain C6).

**Key insight:** The common "equities almost always beat a mid-6% mortgage over 10 years" heuristic does not hold under current, directly-sourced numbers: after modeling realistic dividend and deferred-capital-gains tax drag, equities need to clear roughly a **7.53%/yr pretax** nominal return just to tie the guaranteed, tax-free 6.43% paydown return — and that breakeven sits **above** the ceiling of Vanguard's own current 10-year forecast (6.2%, chain C3), not comfortably inside a historical-average assumption. The guaranteed paydown is not "free money certain to lose to stocks" the way generic financial-planning folk wisdom often assumes; it is a genuinely competitive, risk-free alternative at today's rates (chain C1, chain C4).

**Trade-offs acknowledged:** The blend gives up some of Option A's base-case extra value relative to going 100% A — about $6,640 of $111,914, or roughly 6% — in exchange for keeping $20,000 fully liquid, diversified, and positioned to benefit if equities outperform Vanguard's muted forecast (chain C6). It also gives up some of Option B's upside if the historical 10%/yr average reasserts itself, and it does not fully eliminate the illiquidity, concentration, and lost inflation-hedge costs of the $40,000 portion that still goes to the house (chain C5) — no chain — flagged assumption only on the exact degree of residual illiquidity cost, since that depends on A-8 (whether the household is ever forced to access that equity under duress), which this analysis could not verify.

**Pre-check:** head C6 (LOW), C3 (LOW), C1 (MEDIUM) · ?-marked: none · lowest cited: LOW · Inputs ceiling: LOW
**Confidence:** LOW — the recommendation's direction (a blend tilted toward debt paydown, not either pure extreme) is reasonably robust, but its headline chain (C6) and C6's own input C3 are both LOW, driven by: (1) GT-1?/GT-2? being self-reported and unverified — verification means reading the actual loan statement and tax return; (2) the live, currently-unsettled rival that realized 10-year equity returns could exceed the 7.53% breakeven, which no observation available today can resolve (chain C3); and (3) A-12's unresolved dependence on the household's actual risk tolerance and other goals (chain C6), which this analysis could not observe directly.

This analysis could not verify four things that would materially sharpen — and could shift — the recommended split, and the household is the only source that can supply them. First, whether 401(k), IRA, and HSA contribution room is already maximized for this year and the foreseeable future (A-4): if meaningful tax-advantaged headroom exists, redirecting cash flow there very likely dominates both Option A and Option B and should be resolved before finalizing either. Second, whether the loan's servicer permits a low-cost recast after a lump-sum prepayment, and whether any prepayment penalty applies (A-2, A-3): both are cheap to confirm directly with the servicer and both affect the exact dollar figures in chains C1 and C5. Third, whether the household has, or might develop, any other near-term (within-10-year) call on this money — a planned purchase, a career change, a likely move — that would make the $40,000 portion's illiquidity costlier than assumed (A-8). Fourth, and most values-laden: how the household would actually feel watching the $20,000 equity portion — or a larger share, under a more aggressive split — lose 30-40% of its value in a downturn, since the right split genuinely depends on risk tolerance in a way the arithmetic alone cannot settle (A-12), and a household with a strong preference either for certainty or for growth exposure should move the split toward $30,000/$30,000 or toward $50,000/$10,000 accordingly rather than treating $40,000/$20,000 as the only defensible number.

---

## §6→§4 closure ledger (process output)

Every §6 claim below cites its chain inline, so each is discharged without needing a separate ledger row's structural form; the ledger is still enumerated explicitly per the required step.

- "Split the $60,000 roughly two-to-one toward debt paydown: apply $40,000 to mortgage principal and invest $20,000 in a broad-market taxable index fund" → chain C6 ✓
- "equities need to clear roughly a 7.53%/yr pretax nominal return just to tie the guaranteed, tax-free 6.43% paydown return...above the ceiling of Vanguard's own current 10-year forecast" → chain C3 ✓
- "the guaranteed paydown is...a genuinely competitive, risk-free alternative at today's rates" → chain C1, chain C4 ✓
- "The blend gives up some of Option A's base-case extra value...in exchange for keeping $20,000 fully liquid, diversified, and positioned to benefit if equities outperform" → chain C6 ✓
- "does not fully eliminate the illiquidity, concentration, and lost inflation-hedge costs of the $40,000 portion" → chain C5 ✓
- caveat: "no chain — flagged assumption only" marker on the residual-illiquidity-cost-magnitude caveat → marker present, scores untraced by design (honest disclosure, not a citation) ✓ (conformant per the Caveats rule)
- "**Confidence:** LOW...driven by...(1) GT-1?/GT-2?...(2)...chain C3...(3) A-12's unresolved dependence...chain C6" → chain C3, chain C6, plus GT-1?/GT-2? named directly ✓

Scan complete: 7 §6 claim rows, 0 untraced.

---

## Self-audit scan (process output)

| Chain | Chain Head (brief) | Form conforming? | Rule applied | Dependency clean? | Band | Act attempted? | Edges fired |
|---|---|---|---|---|---|---|---|
| C1 | GT-1?, GT-2? | yes | n/a | yes | MEDIUM | no | none |
| C2 | GT-2?, GT-5, GT-6? | yes | n/a | yes | MEDIUM | yes | none |
| C3 | C1, C2, GT-3 | yes | n/a | yes | LOW | yes | none |
| C4 | GT-3, GT-2?, C1 | yes | n/a | yes | MEDIUM | yes | none |
| C5 | C1, C3, GT-4? | yes | n/a | yes | LOW | no | none |
| C6 | C1, C3, C5 | yes | n/a | yes | LOW | yes | none |

| §6 Span (brief) | Construct | Claim under R11? | R11 clause applied | Chain cited |
|---|---|---|---|---|
| "Recommended approach: Split the $60,000...$40,000...$20,000..." | bold lead-in | yes | colon closes bold span; assertion on same line | C6 |
| "Key insight: The common...heuristic does not hold..." | bold lead-in | yes | colon closes bold span; assertion on same line | C3, C1, C4 |
| "Trade-offs acknowledged: The blend gives up..." | bold lead-in | yes | colon closes bold span; assertion on same line | C6, C5 |
| "Pre-check: head C6 (LOW), C3 (LOW), C1 (MEDIUM)..." | bold lead-in | yes | pre-check line is itself a claim, cited by chains its head names | C6, C3, C1 |
| "Confidence: LOW — the recommendation's direction..." | bold lead-in | yes | colon closes bold span; assertion on same line | C3, C6 |
| "This analysis could not verify four things...A-12..." | prose | no | prose carrying neither a bold colon lead-in nor a list marker is not a claim at all | n/a |

Scan complete: 6 chain rows, one per section-4 chain block in order; 6 section-6 rows, one per construct in order — 5 claims under R11, 1 excluded. 0 chains malformed, 0 claims untraced.

---

## Self-Audit Gate (process output)

**Criterion 1: Identify Essence**
Quoted span: "how should that $60,000 be split between (a) extinguishing debt that carries a guaranteed, tax-free 6.25%/6.43%-effective cost, and (b) taking on diversified, taxed, uncertain equity risk — so as to maximize risk-adjusted household net worth at a fixed 10-year horizon"
Band: **Rigorous**
Justification: Names the core trade-off (guaranteed-cost debt vs. taxed uncertain equity, risk-adjusted, fixed horizon) rather than restating "mortgage or invest?"; the five success criteria each name a checkable structural property of the Conclusion (a stated split, a derived guaranteed rate, an after-tax equity model, an explicit risk bracket, named second-order effects).

**Criterion 2: Challenge Assumptions**
Quoted span (Assumption Audit scan): "C2 | 2 | tax dividend leg annually, price leg once at sale | A-10 (28%/18% rates stay stable for 10 years) | yes" — showing the audit surfaced a new assumption (A-10) at a named chain step and recorded it.
Band: **Rigorous**
Justification: All 12 rows use the four-type scheme correctly, Verdict cells use the token+em-dash form (Accept/Challenge, never bare), at least eight rows are Challenged rather than merely Accepted, every chain-used unverified assumption is flagged, and the Assumption Audit scan is present and exhaustive over all 17 named chain steps.

**Criterion 3: Establish Ground Truths**
Quoted span: "?-marked: GT-1, GT-2, GT-4, GT-6, GT-7, GT-8, GT-9 (7 of 9)... Read-at-source: GT-3 — Treasury daily-par-yield CSV...; GT-5 — corporate.vanguard.com VEMO return-forecasts page..."
Band: **Rigorous**
Justification: Checking the enumeration against the list confirms exactly those seven IDs carry `?` and GT-3/GT-5 are the only unsuffixed entries, each with a named read-at-source location; no chain in section 4 is HIGH, so the "every unsuffixed GT feeding a HIGH chain names its read-at-source location" clause is vacuously satisfied; no Phase-2 Discard entries appear in the list (none were discarded).

**Criterion 4: Reason Upward**
Quoted span (Self-audit scan, chain-form table): "C3 | C1, C2, GT-3 | yes | n/a | yes | LOW | yes | none" (and the same "yes/yes" pattern across all six rows)
Band: **Rigorous**
Justification: All six chains score Form-conforming "yes" and Dependency-clean "yes" in the scan; each chain carries at least one genuine intermediate (e.g., C3's breakeven-vs-Vanguard-ceiling hop is not restatable from GT-3 or chain C1/C2 alone); GT-7?/GT-8? are explicitly scoped as illustrative analogy only (A-6), never offered as direct evidence; every surfaced assumption carries an inline `[Assumes: X]` mark; Abandoned Reasoning documents three dead ends with specific, non-generic abandonment reasons (collinear scoring design, an unsourced base-case figure, a dominated third option).

**Criterion 5: Validate**
Quoted span: "Confidence: LOW — two axes are short. Inputs: capped at MEDIUM because this chain cites C1 and C2, both MEDIUM... Rivals: the live rival...is not settled by this analysis..." (chain C3's confidence line)
Band: **Rigorous**
Justification: Every chain with a `GT-N?` input is rated MEDIUM or LOW, never HIGH (D-07 holds across all six chains); each confidence line names its specific `?`-marked inputs, cited chains below HIGH, and priced `[Assumes: X]` premises rather than using vague language; the full five-step adversarial pass (Recompute, Sensitivity, Rival, Pre-Mortem Premise/Causes/Clusters/Disposition, Falsification) is present with every cluster carrying a named disposition (plan change or accepted risk with mitigation); bands are calibrated to what their own axes license (e.g., C1 is MEDIUM on Inputs alone, not pushed lower without cause; C3/C5/C6 are LOW because two axes are genuinely short, not by default).

**Criterion 6: Conclusion-to-Ground-Truth Traceability**
Quoted span (Self-audit scan, claim-inventory table): 5 of 6 constructs scored "yes" under Claim under R11, each with a named Chain cited (C6; C3, C1, C4; C6, C5; C6, C3, C1; C3, C6); the sixth (clarifying-questions prose) correctly scored "no — not a claim."
Band: **Rigorous**
Justification: Every Conclusion-section claim traces inline to a named section-4 chain, no new claim is introduced in §6 that lacks a chain, and the Key Insight (the breakeven sitting above Vanguard's own forecast ceiling) is a non-obvious finding distinct from the Recommended Approach's split, not a restatement of it.

**Gate result:** No criterion scored Absent; zero criteria scored Hand-wavy (the cap of "at most one" is cleared with room to spare). Both pass conditions are met — this analysis clears the Self-Audit Gate on the first scoring pass, with no Fix/Repeat cycle needed.
