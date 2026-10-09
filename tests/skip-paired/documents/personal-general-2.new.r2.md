## Answer

**Recommendation:** Apply the full $60,000 as extra principal on the mortgage (chain C1, C4). It locks in a guaranteed, tax-free $111,913 of additional home equity by year 10, a rate that beats every legally risk-free alternative and the entire current consensus 10-year equity forecast (chain C1, C4).

**Band (from §6):** MEDIUM

**Would change it:** a re-run of chain C2 using the household's actual fund's trailing dividend yield instead of GT-11?'s blended estimate; realized or revised equity-return forecasts rising above chain C3's ≈7.53%/year breakeven; A-11 revealing unmaxed tax-advantaged retirement space, which would take priority over both options; or the household weighting liquidity/diversification/optionality more heavily than chain C5 does, in which case a 50/50 blend is the named fallback.

## 1. Problem Essence

**Core problem:** Given $60,000 of cash that is genuinely surplus to an already fully-funded six-month emergency reserve, what deployment of that $60,000 maximizes this household's risk-adjusted, after-tax net worth over a fixed 10-year horizon — and is "pay down the mortgage vs. invest in a taxable index fund" actually the complete choice set, or does it omit a superior use of the money?

**Success criteria:**
1. The true, tax-adjusted, risk-adjusted terminal value of both named paths is quantified over exactly 10 years (not an infinite horizon), using a defensible forward-looking equity-return estimate rather than an unconditional historical average.
2. The tax-treatment asymmetry (zero mortgage-interest shield under the standard deduction vs. taxable-brokerage dividend and capital-gains drag) is priced explicitly into both numbers, not asserted qualitatively.
3. The liquidity, behavioral, and amortization-structure nuances the household raised (recast vs. standard amortization; panic-selling risk; illiquidity of home equity given the reserve is already funded) are addressed on their own terms, not folded silently into a single "safe vs. risky" return comparison.
4. Whether the binary framing is complete is explicitly tested, and any superior alternative use of the $60,000, or a legitimate blended allocation, is surfaced if the stated facts support one.
5. The analysis ends in one concrete, decisive recommendation — not a hedge — with the dollar-level reasoning shown, a calibrated confidence rating, and a named condition that would change the recommendation.

---

## 2. Assumptions Table

*Fishbone note: the standard 6M/8P/4S category sets do not fit a personal capital-allocation decision cleanly, so this analysis uses a bespoke six-category set locked before brainstorming: Market/Return, Tax/Policy, Behavioral, Liquidity/Structural, Framing/Scope, Macro/Rate — the "always-valid fallback" clause permits a custom set when none of the presets fit, and this set is locked for the remainder of Phase 2.*

*Inversion note: inverting the claim "paying down the mortgage is the better use of this $60,000" and enumerating what would guarantee that inversion true surfaces six failure-guaranteeing conditions, each mapped to the assumption it already corresponds to below: (1) realized 10-year equity returns exceed the ~7.5%/yr breakeven hurdle derived in chain C3 → A-1; (2) a liquidity emergency beyond the funded reserve arises and home equity cannot be accessed quickly or cheaply → A-10; (3) the household panic-sells Option B near a trough, a mistake structurally impossible under Option A → A-6, A-7; (4) a future tax-law change restores a mortgage-interest deduction while raising capital-gains rates → A-3, A-5; (5) the $60,000 actually had a higher-priority, unstated use (unmaxed tax-advantaged space, higher-rate debt) that dominates both named options → A-11; (6) mortgage rates fall and the household refinances soon, shrinking the window over which the 6.25% rate's benefit accrues → A-13. No new assumption rows were needed — every inversion-derived precondition already maps to a fishbone branch.*

| Assumption | Type | Treatment | Verdict | Verification |
|------------|------|-----------|---------|--------------|
| A-1: Vanguard's VCMM 10-year forward forecast (4.2%–6.2% nominal) is a better predictor of this household's actual 10-year equity return than the unconditional long-run historical average (~10% nominal) | untested belief | Explicitly challenge; favor the valuation-aware forward estimate as the central case, historical average as an upper-bound sensitivity only | Challenge — accepted as central case with explicit bracket to the historical range, not as certainty | GT-9 (read-at-source); forecast accuracy itself is inherently unverifiable in advance — flagged in chain C2/C3 confidence lines |
| A-2: Broad-market dividend yield averages ~1.3% over the next 10 years | untested belief | Verify against the household's actual fund; flag if used | Challenge — sources disagree (1.08%–1.60%) | unverified — flagged GT-11? |
| A-3: Household's 28% ordinary / 18% LTCG+qualified-dividend marginal rates and standard-deduction status hold for the full 10-year horizon | current constraint | Record expiry conditions | Accept — expires on any future tax-law change (bracket shifts, standard-deduction amount, itemization-threshold change) or household income change; until then, treated as given | GT-2 (stipulated by household) |
| A-4: No Net Investment Income Tax (3.8% federal surtax) applies to this household | untested belief | Verify once household MAGI is known; household income level was not stated | Challenge — unverified, would modestly worsen Option B's case if wrong | unverified — flagged GT-15? |
| A-5: No state-level itemization quirk restores a partial mortgage-interest deduction despite the federal standard deduction | untested belief | Verify against the household's specific state's tax code | Challenge — state not specified | unverified — flagged |
| A-6: The household will hold an Option-B investment through at least one full market downturn without panic-selling | untested belief | Verify against the household's own documented risk tolerance/history; absent that, treat as the largest behavioral risk to Option B | Challenge — not verified; central to the adversarial pass in §5/Phase 5 | unverified — flagged; drives the Behavioral criterion in chain C5 |
| A-7: A visible taxable-brokerage balance creates no more temptation for discretionary withdrawal than the same value trapped in home equity | untested belief | Verify against household spending discipline | Challenge — unverified for this household | unverified — flagged; second-order point in chain C1's actor-lens extension |
| A-8: No prepayment penalty applies to this specific mortgage | convention | Challenge before executing Option A; near-universal absence of such penalties on post-2014 qualified mortgages is a convention, not a guarantee for this loan | Challenge — accept provisionally pending confirmation in loan documents/with the servicer | unverified — flagged GT-13? |
| A-9: Paying extra principal without requesting a recast leaves the required monthly payment unchanged and only shortens the payoff term / cuts total interest | current constraint (contract-structure fact) | Confirm directly rather than assume | Accept — independently confirmed by this analysis's own amortization computation | GT-7 (computed directly, Python amortization model) |
| A-10: If a future liquidity need exceeds the funded reserve, the household could access trapped home equity via HELOC, cash-out refinance, or sale, at unknown future rates/terms | current constraint | Record expiry: depends on future rate environment and underwriting conditions | Accept — real but costlier/slower fallback than the already-funded reserve; priced into the Liquidity criterion in chain C5 | GT-3 (stipulated); fallback terms unverifiable in advance |
| A-11: Paying down the mortgage vs. investing in a taxable brokerage account is the complete and correct choice set for this $60,000 — i.e., no unmaxed tax-advantaged space (401(k) match, backdoor Roth, HSA) or higher-rate debt competes for it | untested belief | Explicitly challenge — this is the single largest open framing question and was never ruled out by the stated facts | Challenge — neither confirmed nor denied; carried into §6 as an explicit precondition caveat | unverified — flagged; no chain — flagged assumption only |
| A-12: The $60,000 figure and the "surplus beyond a fully-funded reserve" framing are accurate as of the decision date, with no known pending large expense competing for the cash | current constraint | Accept as a stated fact of the problem | Accept — given | stipulated by household |
| A-13: Current market conditions (10-Year Treasury 5.28%, Vanguard's 4.2%–6.2% equity forecast) are reasonably representative of today's opportunity set, not a transient anomaly about to reverse before the household acts | current constraint | Record expiry: re-check if execution is delayed materially past the analysis date | Accept — as of October 8, 2026; re-verify if the decision is deferred by more than a few months | GT-9, GT-12 (read-at-source as of analysis date) |
| A-14: This is a genuinely fixed-rate loan, so the comparison is a fixed guaranteed rate vs. an uncertain variable return, with no mortgage-side rate-reset risk regardless of which option is chosen | physical law (contractual, for this instrument) | Accept as a ground-truth candidate | Accept — stipulated "30-year fixed-rate" | GT-1 (stipulated by household) |
| A-15: The household remains in the home and keeps this mortgage (does not sell, move, or refinance away) long enough for the modeled amortization schedule to play out as stated | untested belief | Verify against household plans; surfaced during the Phase 4 Assumption Audit from chain C1's third-order time-lens step | Challenge — not verified; if the household expects to sell or refinance well within 10-15 years, the long-horizon freed-cash-flow benefit in chain C1 would not materialize, though the year-10 guaranteed equity gain (chain C1's core claim) is unaffected | unverified — flagged; surfaced post-hoc, added to table per Assumption Audit |
| A-16: This analysis's chosen trade-off weights (return 5, tax 3, liquidity 2, behavioral 4, diversification 3, optionality 2, simplicity 1) reflect a reasonable generic household rather than this specific household's stated priorities | untested belief | Verify against the household's own stated priorities; surfaced during the Phase 4 Assumption Audit from chain C5 | Challenge — not verified; chain C5's confidence line already names this as the chain's own downgrade cause and the exact-tie flip-test as the sensitivity check | unverified — flagged; surfaced post-hoc, added to table per Assumption Audit |

## 3. Ground Truths

**Household-stipulated parameters** (the problem's own given facts — not external claims requiring source verification):

- **GT-1** Mortgage: $240,000 remaining balance, 6.25% fixed APR, 27 years (324 months) remaining on the amortization schedule, 30-year fixed-rate loan, no stated rate-reset risk — stipulated by household; read-at-source: user's problem statement
- **GT-2** Household takes the standard deduction (mortgage interest provides $0 marginal tax shield); marginal combined ordinary rate ≈28%; long-term capital gains / qualified dividend rate ≈18% — stipulated by household; read-at-source: user's problem statement
- **GT-3** A six-month emergency reserve is already fully funded, separate from the $60,000 under consideration — stipulated by household; read-at-source: user's problem statement
- **GT-4** Decision horizon = 10 years — stipulated by household; read-at-source: user's problem statement

**Computed directly by this analysis** (Python amortization and tax-drag models; figures independently recomputed, see Adversarial pass record):

- **GT-5** Required monthly principal-and-interest payment on $240,000 at 6.25% APR amortized over 324 months = $1,535.24 — source: standard mortgage amortization formula, computed directly; read-at-source: this analysis's own computation (standard annuity-payment formula applied to GT-1)
- **GT-6** The effective annual rate (EAR) of a 6.25% APR mortgage compounded monthly = 6.4322% ((1+0.0625/12)^12 − 1) — source: standard compounding identity, computed directly; read-at-source: this analysis's own computation
- **GT-7** Without any extra payment, the balance at month 120 (year 10) is $192,615.95. Applying the $60,000 as extra principal at month 0, holding the required payment at $1,535.24 (no recast), the balance at month 120 is $80,702.86, and the loan fully retires at month 182 (≈15.2 years) instead of month 324 (27.0 years) — source: full month-by-month amortization simulation, computed directly; read-at-source: this analysis's own computation
- **GT-8** The balance gap created by the $60,000 paydown at month 120 is $111,913.09, and this equals $60,000 × (1.064322)^10 to the cent — source: derived identity, verified by direct computation against GT-7; read-at-source: this analysis's own computation (confirms "prepaying a fixed-rate loan without recasting is economically a riskless, tax-free, zero-coupon instrument at the loan's EAR")
- **GT-16** The pretax nominal annualized total return a taxable brokerage account would need to earn (net of a ~1.3% dividend yield taxed annually at 18% and an 18% capital-gains tax on the embedded gain at year-10 liquidation) to match Option A's guaranteed $111,913.09 terminal value is ≈7.53%/year — source: binary-search solve against the same tax-drag model used for GT-9/GT-11; read-at-source: this analysis's own computation

**Read at source (external, opened and confirmed by this analysis):**

- **GT-9** Vanguard Capital Markets Model (VCMM), run as of June 30, 2026: 10-year annualized nominal U.S. equity return forecast = 4.2%–6.2% — this is a **published model-based forecast, not a measured fact**; source: Vanguard, "Setting realistic expectations" (corporate.vanguard.com/content/corporatesite/us/en/corp/vemo/vemo-return-forecasts.html); read-at-source: page text quoted verbatim — "our 10-year expected annualized return for U.S. equities declined from a range of 4.9%–6.9% to a range of 4.2%–6.2%"
- **GT-10** Historical rolling 10-year annualized nominal total return for the S&P 500 (dividends reinvested), computed across 1,750 overlapping monthly windows, January 1871–October 2026: best +21.17%/year, worst −4.02%/year — this is a **measured historical range**, not a forecast; source: dqydj.com, "S&P 500 Historical Return Calculator"; read-at-source: table figures quoted directly ("21.17%" best, "-4.02%" worst, 1,750 windows, Jan 1871–Oct 2026)
- **GT-12** 10-Year Treasury par yield = 5.28% as of October 8, 2026 — this is a **measured market rate**; source: U.S. Treasury, Daily Treasury Par Yield Curve Rates (home.treasury.gov); read-at-source: October 2026 table, "10 YR" column, October 8, 2026 row

**Delegate-reported / unverified (flagged):**

- **GT-11?** Current S&P 500 dividend yield is reported variously as 1.08% (dqydj.com, read-at-source, as of September 2026), 1.24%, and 1.60% (other sources, reported via web search, not opened by this analysis). The central estimate of **1.3%** used in GT-16's tax-drag model is this analysis's own blend across these figures, not itself read at a single source — flagged `?` because the modeling input is a judgment blend, not a verified single figure
- **GT-13?** No prepayment penalty is assumed on this mortgage. This is standard for essentially all U.S. residential mortgages originated after the Dodd-Frank "qualified mortgage" rules took effect in 2014, but this analysis did not open the household's specific loan documents or contact the servicer to confirm it for this loan — unverified: no source opened this session for this specific loan; domain knowledge from training, not independently verified here
- **GT-14?** Mortgage "recasting" (re-amortizing the remaining balance at the same rate after a lump-sum principal payment, typically for a small one-time fee) is a commonly — but not universally — offered servicer feature, distinct from refinancing, that lowers the required monthly payment without changing total interest paid for a given lump sum — unverified: not read from a source this session; domain knowledge from training, used only as explanatory texture, not load-bearing for any numeric chain
- **GT-15?** The Net Investment Income Tax (an additional 3.8% federal surtax on net investment income above ~$250,000 MAGI for a married-filing-jointly household, under current law) may or may not apply to this household — unverified: household income level was not stated and no source was opened this session; not load-bearing for the headline chains, named as a sensitivity factor on chain C2

**Provenance summary:**

```text
?-marked: GT-11, GT-13, GT-14, GT-15 (4 of 16)
Read-at-source: GT-9 — corporate.vanguard.com vemo-return-forecasts.html, forecast sentence quoted verbatim
Read-at-source: GT-10 — dqydj.com S&P 500 Historical Return Calculator, best/worst rolling-10yr table figures quoted verbatim
Read-at-source: GT-12 — home.treasury.gov Daily Treasury Par Yield Curve Rates, October 8 2026 "10 YR" row
GT-13, GT-14, GT-15 not read — turn budget / not load-bearing for any chain head (explanatory texture only); each keeps its ? suffix
```

## 4. Derivation Chains

### Conclusion C1: Paying down $60,000 of principal today locks in a guaranteed, tax-free terminal value of $111,913 by year 10, with no change to the required monthly payment

GT-1 (loan: $240,000, 6.25% APR, 324 months remaining) + GT-2 (standard deduction, $0 interest tax shield) + GT-6 (EAR 6.4322%) + GT-7 (balance gap at month 120 = $111,913.09) + GT-8 ($111,913.09 = $60,000×1.064322^10 identity)
→ because GT-7 and GT-8 show the extra-principal balance gap compounds exactly at the loan's effective annual rate, paying down principal today without recasting is economically identical to buying a riskless, zero-coupon instrument yielding 6.4322% for 10 years
→ because GT-2 confirms no mortgage-interest deduction is being given up, that 6.4322% figure is already a full after-tax rate with nothing further to subtract
→ Option A therefore delivers a guaranteed, zero-variance $111,913 of additional home equity by year 10, net of all taxes, while the required monthly payment itself stays at $1,535.24 the entire time (A-9)
→[2nd] (actor lens) because home equity cannot be withdrawn on impulse, Option A structurally removes any possibility of a panic-driven liquidation that a visible brokerage balance would expose the household to in a downturn (A-6, A-7)
→[2nd] (time lens) because the payment is unchanged without a recast, this $111,913 benefit is invisible in month-to-month cash flow for the entire 10-year horizon — it shows up only as a lower running balance and an earlier payoff date, which can feel like "nothing happened" even though $111,913 of guaranteed value was created
→[3rd] (time lens, beyond the 10-year window) if the household keeps paying the unchanged amount, the loan fully retires around month 182 (≈year 15.2) instead of month 324 (≈year 27), freeing roughly $18,423/year of cash flow for the remaining ≈11.8 years of what would have been the original term *[Assumes: A-15 — household stays in the home and keeps this loan long enough for this to play out; if false, only this long-horizon third-order step is affected, not chain C1's core year-10 claim]*
→[3rd] (actor lens) a lower mortgage balance also improves the household's future debt-to-income ratio, which second-order benefits any future loan underwriting (HELOC, auto loan, second mortgage) the household might seek within the horizon

**Pre-check:** head GT-1, GT-2, GT-6, GT-7, GT-8 · ?-marked: none · lowest cited: none · Inputs ceiling: HIGH
**Confidence:** HIGH — every head input is an unsuffixed, stipulated-or-computed ground truth with a named source; every hop is deduction or arithmetic recomputed independently of the chain text (see Adversarial pass record). The only live rival — that a prepayment penalty or recast fee claws back part of the benefit — is addressed in §5 ("Dead End: I-Bonds / munis..." does not apply here; see A-8/GT-13?) and does not survive: typical penalty caps on the rare loans that still carry them (a few hundred dollars, usually ≤2% of the prepaid amount in the first few years) are immaterial against a $111,913 gain, and A-8 is flagged for confirmation before execution without threatening this conclusion's order of magnitude.

### Conclusion C2: Under the current consensus forward-looking equity forecast, Option B's after-tax terminal value falls short of Option A's guaranteed figure

GT-9 (Vanguard VCMM, 4.2%–6.2% nominal) + GT-11? (dividend yield ≈1.3%, mixed sources) + GT-2 (18% LTCG/qualified-dividend rate)
→ modeling the taxable brokerage account with a 1.3% dividend yield taxed annually at 18% and reinvested, plus an 18% capital-gains tax on the embedded gain at year-10 liquidation, converts GT-9's pretax forecast band into an after-tax terminal-value band of $84,770–$100,143
→ every point in that after-tax band sits $11,771 to $27,143 below Option A's guaranteed $111,913 terminal value
→ under the current consensus forward-looking forecast, Option B is expected to underperform Option A over this specific 10-year horizon in after-tax terminal value, not merely "riskier for similar expected return"

**Pre-check:** head GT-9, GT-11?, GT-2 · ?-marked: GT-11? · lowest cited: none · Inputs ceiling: MEDIUM
**Confidence:** MEDIUM — GT-11? (the 1.3% dividend-yield blend) is unverified at a single source; verification: pull the trailing-twelve-month dividend yield of the household's actual target index fund from its official factsheet and re-run the model (the yield would need to move to roughly 1.6%+ before it materially narrows the gap — see sensitivity in the Adversarial pass record). GT-9 itself is a published forecast, not a certainty; that forecast risk is priced forward into chain C3 rather than double-counted here.

### Conclusion C3: Option B only catches Option A if the next decade of equity returns resembles the long-run historical average rather than the valuation-adjusted forecast every major institutional forecaster currently publishes

C2 (MEDIUM) + GT-8 ($111,913.09 target)
→ solving for the single pretax nominal annualized return that would make Option B's after-tax terminal value equal Option A's $111,913.09 guaranteed figure yields a breakeven hurdle of ≈7.53%/year
→ that hurdle sits above the entire current Vanguard forecast band (4.2%–6.2%) and below the commonly cited unconditional long-run historical average for U.S. large-cap equities (≈10% nominal)
→ Option B wins only if the next decade behaves like the unconditional historical average rather than the valuation-adjusted consensus forecast — a real but not-favored possibility, not a coin flip in either direction given GT-9's explicit basis in current elevated valuations

**Pre-check:** head C2 (MEDIUM), GT-8 · ?-marked: none directly on this head (GT-11? inherited via C2) · lowest cited: MEDIUM · Inputs ceiling: MEDIUM
**Confidence:** MEDIUM — capped by C2 (MEDIUM); C2's own confidence line carries the GT-11? verification path and is not re-explained here. This chain's own added uncertainty is the forecast itself: no verification path exists today that would resolve in advance whether the next decade tracks Vanguard's band or the historical average — that is a stated, unresolvable-in-advance uncertainty, not a gap this analysis failed to close.

### Conclusion C4: No legally risk-free instrument available to this household today pays more, after tax, than extinguishing its own mortgage — the theoretical ceiling on riskless after-tax return is set by the household's own loan

GT-6 (EAR 6.4322%, tax-free) + GT-12 (10-Year Treasury 5.28%, Oct 8 2026) + GT-2 (28% ordinary rate)
→ the household's two legally risk-free uses of this cash are prepaying the mortgage (6.4322% guaranteed, no tax ever owed) or holding high-grade fixed income such as Treasuries (5.28% nominal, taxed as ordinary income at 28%, for an after-tax yield of 3.80%)
→ even crediting Treasuries with full state-tax exemption and ignoring the 28% federal bite entirely, the pretax 5.28% Treasury yield still sits 115 basis points below the mortgage's 6.4322% guaranteed, tax-free rate
→ no legally risk-free instrument available to this household today pays more after tax than simply extinguishing its own 6.25% liability, so Option A captures the full theoretical ceiling on riskless after-tax return available to this household

**Pre-check:** head GT-6, GT-12, GT-2 · ?-marked: none · lowest cited: none · Inputs ceiling: HIGH
**Confidence:** HIGH — all head inputs are unsuffixed and read-at-source or computed directly; the arithmetic is simple and recomputed independently (Adversarial pass record). Rival instruments (Series I Savings Bonds, high-grade municipal bonds) were considered and ruled out in §5 ("Dead End: I-Bonds / municipal bonds as a rival to C4") — neither is shown to beat 6.4322% after tax for a $60,000 allocation at this household's profile.

### Conclusion C5: A seven-criterion weighted trade-off recommends full Option A, with a 50/50 mortgage/invest blend as the only allocation close enough to name as a deliberate alternative

GT-6 (guaranteed EAR 6.4322%) + GT-3 (emergency reserve already funded) + C2 (MEDIUM, Option B expected shortfall)
→ scoring four allocations (idle cash, full Option A, full Option B, 50/50 blend) against seven weighted criteria — return (weight 5), tax efficiency (3), liquidity (2), behavioral robustness (4), diversification (3), optionality (2), simplicity (1) — produces weighted totals of 65, 75, 66, and 75, an exact tie between full Option A and the 50/50 blend
→ the tie resolves to Option A under the exact-tie tiebreak rule: Option A's winning criteria (return, tax efficiency, behavioral robustness, simplicity) rest entirely on unflagged ground truths and the HIGH-confidence chain C1, while the blend's winning criteria (liquidity, diversification, optionality) rest on comparatively qualitative judgment
→ the trade-off therefore recommends full Option A as the primary allocation, with the 50/50 blend standing as the only allocation close enough to warrant naming as a deliberate alternative for a household that weights diversification and optionality more heavily than this scoring does *[Assumes: A-16 — the weights used are this analysis's judgment, not the household's own stated priorities]*

**Pre-check:** head GT-6, GT-3, C2 (MEDIUM) · ?-marked: none directly on this head (GT-11? inherited via C2) · lowest cited: MEDIUM · Inputs ceiling: MEDIUM
**Confidence:** MEDIUM — capped by C2 (MEDIUM; its own confidence line carries the GT-11? verification path, not re-explained here). This chain's own added uncertainty is the criterion weighting itself, which is this analysis's judgment call: a reader who weights liquidity, diversification, and optionality (combined weight 7 of 20) more heavily than this analysis did would flip the tie to the blend — see the flip-test result in the Adversarial pass record. No further verification path exists beyond the household stating its own relative priority on these criteria.

## 5. Abandoned Reasoning

### Dead End: Treating Option A's benefit as pure "interest saved" layered on top of the returned $60,000 principal

**What was tried:** An early pass framed Option A's gain as $111,913 interest saved *plus* the $60,000 principal "returned," for a total comparison figure of $171,913 against Option B's after-tax ending value.

**Why abandoned:** This double-counts the principal. GT-8's verified identity ($111,913.09 = $60,000 × 1.064322^10 exactly) shows the $111,913.09 figure already *is* the total terminal-value equivalent — it already nets in the full return of the $60,000 as reduced liability. Adding another $60,000 on top produced an inflated breakeven hurdle (≈12.68%) that contradicted the verified amortization math.

**What it ruled out:** Any comparison methodology that treats mortgage-paydown "gain" as pure profit-over-principal rather than total terminal value. This mistake would have overstated the hurdle rate Option B needs to clear by roughly 5 percentage points — making the recommendation look far more lopsided in favor of Option A than the corrected math (chain C3, 7.53% hurdle) actually supports. Caught during this analysis's own computation (calc3.py → calc4.py) before being used in any chain above.

### Dead End: Using the unconditional long-run historical average (~10% nominal) as the central-case return assumption for Option B

**What was tried:** An early pass modeled Option B at a flat 10% nominal return as the "realistic" central case.

**Why abandoned:** This is reasoning by convention — "stocks have always returned about 10%" — rather than from the current valuation-aware forecasts every major institutional model now publishes. Vanguard's own stated rationale for its lower 4.2%–6.2% band (GT-9) is that current valuations are elevated relative to history, which the unconditional average does not price in.

**What it ruled out:** Anchoring the primary recommendation (chain C2) on a return assumption the most current, credible, published forward-looking model explicitly says is too high for this specific decade. The historical average survives only as an upper-bound sensitivity input in chain C3, not as the central case.

### Dead End: Pairing Option A with an immediately-opened HELOC to "have it both ways" (pay down the mortgage and keep full liquidity)

**What was tried:** Considered recommending Option A plus opening a home-equity line of credit against the resulting lower balance, to preserve access to the paid-down equity.

**Why abandoned:** A HELOC carries its own variable rate, draw and closing costs, and a new underwriting event — none of which are free. GT-3 establishes the household's liquidity need is already structurally solved by the fully-funded six-month reserve. Adding a HELOC pre-emptively would spend real money solving a problem that, per the stated facts, does not currently exist.

**What it ruled out:** A more complex hybrid structure as the primary recommendation. A HELOC remains a reasonable fallback the household could arrange later if an actual liquidity need beyond the emergency reserve emerges — see A-10 — but it is not worth setting up now for this decision.

### Dead End: Series I Savings Bonds or investment-grade municipal bonds as a rival to chain C4's risk-free-ceiling conclusion

**What was tried:** Considered whether I-Bonds or high-grade munis could beat the mortgage's 6.4322% guaranteed, tax-free rate for part of the $60,000.

**Why abandoned:** I-Bonds cap electronic purchases at $10,000 per person per year, structurally unable to absorb more than a small fraction of $60,000 in the relevant timeframe. Investment-grade municipal bond yields for a household in this tax profile generally sit below the mortgage's after-tax-equivalent rate in the current market — though this analysis did not pull a specific sourced muni-yield figure, so that comparison stays qualitative rather than quantified.

**What it ruled out:** Munis/I-Bonds as a dominant rival to C4's conclusion. They remain a legitimate minor diversification idea worth a conversation with a CPA or advisor, but do not change the headline recommendation, and are not cited as a ground truth anywhere above because the comparison was never quantified to this analysis's own sourcing standard.

---

## 6. Conclusion

**Recommended approach:** Apply the full $60,000 as extra principal on the mortgage (Option A) (chain C1, C4). This converts the cash into a guaranteed, tax-free $111,913 of additional home equity by year 10 — a rate (6.43% EAR) that beats the household's only legally risk-free alternative (10-Year Treasuries, 5.28% pretax / 3.80% after-tax) and the entire current consensus 10-year equity forecast (Vanguard VCMM, 4.2%–6.2%) (chain C1, C4).

**Key insight:** The "safe, low-return mortgage paydown vs. risky, high-return stocks" framing is backwards for this specific household. Once the standard-deduction tax asymmetry and the taxable-brokerage drag are both priced in, paying down this 6.25% loan is not a low-return safe choice being traded off against a higher-expected-return risky one — it is a guaranteed 6.43% tax-free return that the current professional consensus forecast for equities (4.2%–6.2%) does not even match, let alone beat (chain C2, C3). Equities only win this comparison if the next decade reverts to the unconditional historical average instead of tracking the valuation-aware forecast every major institutional model is currently publishing (chain C3).

**Trade-offs acknowledged:** Option A sacrifices liquidity, diversification away from a single illiquid asset (the home), and optionality — the emergency reserve (GT-3) already covers the household's stated liquidity need, but the money becomes genuinely harder to redeploy if a priority the household cannot currently foresee arises (chain C5). A seven-criterion weighted trade-off scored full Option A and a 50/50 mortgage/invest blend in an exact tie (75 vs. 75); the tie resolves to Option A on the tiebreak rule, but a household that weights diversification, liquidity, and optionality more heavily than this analysis's weights would reasonably choose the 50/50 blend instead — not a more diluted split, which the scoring does not support (chain C5). Separately, and not resolved by any chain above: confirm all available tax-advantaged retirement space (401(k) match, backdoor Roth, HSA) is already maxed for the year before executing either option — if it is not, that space likely dominates both Option A and Option B and should be funded first — no chain — flagged assumption only (A-11).

**Pre-check:** head C1 (HIGH), C2 (MEDIUM), C3 (MEDIUM), C4 (HIGH), C5 (MEDIUM) · ?-marked: none directly (GT-11? inherited via C2/C3/C5) · lowest cited: MEDIUM · Inputs ceiling: MEDIUM
**Confidence:** MEDIUM — the core "Option A is a guaranteed, excellent, tax-free deal that beats every safe alternative" claim rests on C1 and C4 alone, both HIGH, with no unresolved inputs. The comparative margin over Option B, and the trade-off ranking, rest additionally on C2, C3, and C5, each MEDIUM because they inherit GT-11?'s unverified dividend-yield blend and C9's forecast-based (not certain) central case. What would change the recommendation: (1) if the household's actual target fund's dividend yield and a re-run of chain C2 move the breakeven meaningfully, (2) if realized or revised consensus equity forecasts rise above the ≈7.53% hurdle in chain C3, (3) if A-11 reveals unmaxed tax-advantaged space, which would take priority over both named options, or (4) if the household's own weighting of liquidity/diversification/optionality (chain C5) differs materially from the weights used here, in which case the 50/50 blend — not a more diluted split — is the recommended fallback.

## Appendix — process output

## Techniques not applied (process output)

```text
theoretical-limit — not applicable at Phase 1 — the essence is a capital-allocation decision between two named options, not a question of whether a stated figure is a convention mistaken for a hard bound; the technique is applied instead at Phase 4 (chain C4, risk-free-return ceiling).
inversion — not applicable at Phase 5 — the conclusion is a plan/recommendation (apply $60,000 to the mortgage), which the decision rule routes to pre-mortem rather than inversion; inversion is applied instead at Phase 2 (see the inversion note under §2, mapping six failure-guaranteeing conditions onto A-1, A-3, A-5, A-6, A-7, A-10, A-11, A-13).
five-whys — not applicable at Phase 3 — every ground truth in this analysis bottoms out directly at a stipulated household fact, a direct source reading, or a single computed mathematical identity (e.g. GT-6's EAR formula, GT-8's compounding identity), with no composite claim requiring a multi-level reduce-to-primitives drill.
```

## Assumption Audit scan (process output)

| Chain | Step | Step Text (brief) | Assumption surfaced? | Added to Table? |
|---|---|---|---|---|
| C1 | 1 | Extra principal = zero-coupon bond at loan EAR | no (covered by A-8, A-9 already) | n/a — clean pass |
| C1 | 2 | No deduction subtracted, full rate is after-tax | no | n/a — clean pass |
| C1 | 3 | Guaranteed equity, payment unchanged | no (covered by A-9) | n/a — clean pass |
| C1 | 4 [2nd] | Actor lens: panic-sell immunity | no (covered by A-6, A-7) | n/a — clean pass |
| C1 | 5 [2nd] | Time lens: invisible monthly benefit | no | n/a — clean pass |
| C1 | 6 [3rd] | Time lens: freed cash flow after payoff (~yr 15.2) | yes — household stays in home/keeps loan long enough | yes — A-15 added |
| C1 | 7 [3rd] | Actor lens: improved future DTI | no | n/a — clean pass |
| C2 | 1 | Tax-drag model converts GT-9 band to after-tax band | no (covered by A-1, A-2) | n/a — clean pass |
| C2 | 2 | After-tax band sits below $111,913 | no | n/a — clean pass |
| C2 | 3 | Conclusion: B expected to underperform A | no | n/a — clean pass |
| C3 | 1 | Solve breakeven hurdle ≈7.53% | no | n/a — clean pass |
| C3 | 2 | Compare hurdle to historical average | no (covered by A-1) | n/a — clean pass |
| C3 | 3 | Conclusion: B needs historical-average-like returns | no | n/a — clean pass |
| C4 | 1 | Define two risk-free alternatives | no | n/a — clean pass |
| C4 | 2 | Treasury after-tax yield still below mortgage EAR | no | n/a — clean pass |
| C4 | 3 | Conclusion: mortgage sets the riskless ceiling | no | n/a — clean pass |
| C5 | 1 | Scoring produces exact tie (A vs. blend) | no (weights already disclosed in chain text) | n/a — clean pass |
| C5 | 2 | Tiebreak resolves to Option A | no | n/a — clean pass |
| C5 | 3 | Conclusion: recommend A, name blend as alternative | yes — weights reflect this analysis's judgment, not the household's stated priorities | yes — A-16 added |

Scan complete: 5 chains, 19 steps walked in order; 2 assumptions surfaced (A-15, A-16), both added to the Classified Assumptions Table and marked inline on their originating steps.

## Adversarial pass (process output)

**Recompute.** All computed figures were recomputed independently in this session (Python scripts calc.py → calc4.py, tradeoff.py) and are reproduced here for the record: monthly payment $1,535.24 (GT-5); EAR 6.4322% (GT-6); balance at month 120 without extra payment $192,615.95, with it $80,702.86, full payoff at month 182 vs. month 324 (GT-7); balance gap $111,913.09 = $60,000×1.064322^10 exactly (GT-8); Option B after-tax terminal-value band $84,770–$100,143 across Vanguard's 4.2%–6.2% band (chain C2); breakeven hurdle 7.531% (GT-16, chain C3); Treasury after-tax yield 5.28%×(1−0.28)=3.80% (chain C4); trade-off weighted totals 65 / 75 / 66 / 75 for idle cash / Option A / Option B / 50-50 blend, an exact tie between Option A and the blend (chain C5). No recomputed figure diverged from the chain text.

**Sensitivity.** The single ground truth whose falsity would most flip the conclusion is GT-9 (Vanguard's 4.2%–6.2% forecast), in combination with the `?`-marked GT-11? (dividend yield blend): if realized or revised consensus equity-return expectations rise above the ≈7.53%/year hurdle in chain C3, Option B overtakes Option A in expected terminal value. GT-9 and GT-11? are the chains' named weak points (GT-9 is read-at-source but is a forecast, not a certainty; GT-11? is unverified at a single source). Weakest link per chain: C1 → A-8 (prepayment penalty unconfirmed, but immaterial in magnitude per C1's own confidence line); C2/C3 → GT-9's forecast nature (inherently unverifiable in advance); C4 → none material; C5 → A-16 (judgment-based criterion weights).

**Rival.** C1: rival is "prepayment penalty/recast friction erodes the benefit" — ruled out by magnitude in C1's own confidence line (§4). C2: rival is "realized returns beat Vanguard's forecast" — this is not an unsettled loose end but exactly the subject chain C3 works out quantitatively (breakeven ≈7.53%/yr), so C2's rival is addressed by pointing to C3. C3: the rival (equities beat the breakeven) stays live — nothing in §5 or elsewhere settles it either way; it is named on the §6 Conclusion's confidence line as uncertainty, consistent with C3's MEDIUM rating. C4: rival is "munis/I-Bonds beat the mortgage after tax" — ruled out, see §5 "Dead End: I-Bonds / municipal bonds as a rival to chain C4." C5: rival is the 50/50 blend itself — not ruled out, only tie-broken; it stays live and is named explicitly in §6's Trade-offs-acknowledged as the legitimate alternative.

**Premise.** The plan has already failed: directing the full $60,000 to mortgage principal turned out to be the wrong move for this household.

**Causes** (generated from four viewpoints — the household executing the plan, the household's future self living with a liquidity crunch, a CPA/advisor reviewing the decision in hindsight, and the market as an adversarial force; unfiltered):
1. (household) They never confirmed GT-13? and incurred an unexpected prepayment fee.
2. (household) They felt real regret within 1-2 years because the payment never changed and no benefit was visible (A-9).
3. (household) They later realized they had unmaxed 401(k)/HSA space that should have been funded first (A-11).
4. (future self, crisis) A liquidity need beyond the six-month reserve arose (job loss beyond 6 months, medical event) and a HELOC/refi was slow, expensive, or declined when they needed it (A-10).
5. (future self, crisis) They relocated or sold the home within 2-3 years, before the amortization benefit had time to compound, and transaction costs ate into the realized equity gain (A-15).
6. (CPA/advisor, hindsight) Tax law changed within the 10 years (standard deduction shrank, or the household's itemizable expenses grew) and the "no tax shield" premise (A-3) stopped holding partway through the horizon.
7. (CPA/advisor, hindsight) The household was subject to NIIT or a higher bracket than the stated 28%/18%, invalidating part of the tax-drag model (A-4).
8. (market, adversarial) Equities actually returned well above the 7.53% breakeven for this specific decade, and in hindsight the household gave up a materially larger gain than any forecast suggested was likely (chain C3).
9. (market, adversarial) Inflation ran hotter than assumed, eroding the real value of the "guaranteed" mortgage-paydown benefit faster than a different real asset would have been eroded.

**Clusters:**
- **Liquidity mis-estimation** (causes 2, 4, 5) — bears on chain C1, GT-3, A-10, A-15.
- **Framing gap not resolved before executing** (cause 3) — bears on A-11.
- **Tax-regime drift** (causes 6, 7) — bears on A-3, A-4, A-5, chains C1/C2.
- **Forecast miss / realized returns diverge from consensus** (causes 8, 9) — bears on chain C2, C3, GT-9.
- **Execution-detail oversight** (cause 1) — bears on A-8, GT-13?.

**Disposition:**
- Liquidity mis-estimation → **plan change**: before executing, confirm the six-month reserve reflects a realistic worst-case for this household's actual job/income volatility (not a generic rule of thumb), and if relocation or a job change within 2-3 years is a live possibility, scale back from 100% to roughly 90/10 (mortgage/cash) rather than committing the full $60,000.
- Framing gap → **plan change**: add a concrete pre-execution checklist item — confirm 401(k) match and HSA are fully funded for the year before wiring any of the $60,000 to the mortgage (already carried into §6 as the A-11 caveat).
- Tax-regime drift → **accepted risk**, named mitigation: re-run chains C1/C2 if a tax-law change occurs during the horizon; no action needed today (A-3's expiry condition already names this trigger).
- Forecast miss → **accepted risk**, named mitigation: this is precisely chain C3's named sensitivity; the household is told explicitly the recommendation can look wrong in hindsight if equities beat consensus, and the 50/50 blend (chain C5) is the named hedge for a household that wants to reduce this specific regret risk.
- Execution-detail oversight → **plan change**: confirm GT-13? (no prepayment penalty) directly with the loan servicer before wiring funds — a concrete, cheap, pre-execution action item.

**Falsification.** The conclusion is false if, measured at year 10, the household's actual realized net worth from directing the $60,000 to Option B (after all taxes, and after confirming any prepayment penalty on Option A) exceeds what Option A actually delivered — which, per chain C3, requires realized 10-year pretax nominal equity returns to exceed ≈7.53%/year.

## §6→§4 closure ledger (process output)

- "Apply the full $60,000 as extra principal on the mortgage (Option A)" → chain C1 ✓
- "This converts the cash into a guaranteed, tax-free $111,913 of additional home equity by year 10...beats...Treasuries...and the entire current consensus 10-year equity forecast" → chain C4 ✓
- "Equities only win this comparison if the next decade reverts to the unconditional historical average instead of tracking the valuation-aware forecast" → chain C3 ✓
- "The 'safe...vs. risky...' framing is backwards...it is a guaranteed 6.43% tax-free return that the current professional consensus forecast for equities (4.2%–6.2%) does not even match" → chain C2 ✓
- "A seven-criterion weighted trade-off scored full Option A and a 50/50 mortgage/invest blend in an exact tie (75 vs. 75); the tie resolves to Option A on the tiebreak rule...a household that weights diversification, liquidity, and optionality more heavily...would reasonably choose the 50/50 blend instead" → chain C5 ✓
- "Confirm all available tax-advantaged retirement space...is already maxed...before executing either option" → no chain — flagged assumption only (A-11) ✓ (marker present, claim honestly scored untraced)
- "The core...claim rests on C1 and C4 alone, both HIGH" → chain C1, C4 ✓
- "The comparative margin over Option B, and the trade-off ranking, rest additionally on C2, C3, and C5, each MEDIUM" → chain C2, C3, C5 ✓

Ledger clean: 8 rows, 7 discharged by inline chain citation, 1 discharged by the flagged-assumption marker (honest-untraced, not a citation). 0 claims cut.

## Self-audit scan (process output)

**Table 1 — chain form (section 4):**

| Chain | Chain Head (brief) | Form conforming? | Rule applied | Dependency clean? | Band | Act attempted? | Edges fired |
|---|---|---|---|---|---|---|---|
| C1 | GT-1, GT-2, GT-6, GT-7, GT-8 | yes | n/a | yes | HIGH | no (all head inputs stipulated or computed directly, no external citation on this head) | none |
| C2 | GT-9, GT-11?, GT-2 | yes | n/a | yes | MEDIUM | yes (GT-9 read-at-source attempt; GT-11? attempted via dqydj read + search, left `?` on source disagreement) | none |
| C3 | C2 (MEDIUM), GT-8 | yes | n/a | yes | MEDIUM | no (head's own new input GT-8 is computed directly; external attempt already made for GT-9/GT-11? via cited chain C2) | none |
| C4 | GT-6, GT-12, GT-2 | yes | n/a | yes | HIGH | yes (GT-12 read directly from home.treasury.gov) | none |
| C5 | GT-6, GT-3, C2 (MEDIUM) | yes | n/a | yes | MEDIUM | no (head's own new inputs GT-6/GT-3 stipulated or computed directly) | none |

**Table 2 — claim inventory (section 6):**

| §6 Span (brief) | Construct | Claim under R11? | R11 clause applied | Chain cited |
|---|---|---|---|---|
| Recommended approach: apply $60,000 to mortgage | bold lead-in | yes | bold lead-in whose colon closes the bold span (always a claim) | C1, C4 |
| Key insight: safe-vs-risky framing is backwards | bold lead-in | yes | bold lead-in whose colon closes the bold span (always a claim) | C2, C3 |
| Trade-offs acknowledged: liquidity/diversification/optionality given up, tie with blend, A-11 caveat | bold lead-in | yes | bold lead-in whose colon closes the bold span (always a claim) | C5; final sentence separately carries marker "no chain — flagged assumption only (A-11)" |
| Pre-check: head C1 (HIGH), C2 (MEDIUM), C3 (MEDIUM), C4 (HIGH), C5 (MEDIUM) | bold lead-in | yes | always-claim bold lead-in (Pre-check line), cited by the chains its own head names | C1, C2, C3, C4, C5 |
| Confidence: MEDIUM — rests on C1/C4 (HIGH) plus C2/C3/C5 (MEDIUM) | bold lead-in | yes | bold lead-in whose colon closes the bold span (always a claim); also discharges D-07's naming obligation | C1, C2, C3, C4, C5 |

```text
Scan complete: 5 chain rows, one per section-4 chain block in order; 5 section-6 rows, one per construct in order — 5 claims under R11, 0 excluded. 0 chains malformed, 0 claims untraced.
```

## Self-Audit Gate (process output)

**Criterion 1: Identify Essence**
Quoted span: "Given $60,000 of cash that is genuinely surplus to an already fully-funded six-month emergency reserve, what deployment of that $60,000 maximizes this household's risk-adjusted, after-tax net worth over a fixed 10-year horizon — and is 'pay down the mortgage vs. invest in a taxable index fund' actually the complete choice set, or does it omit a superior use of the money?"
Band: **Rigorous**
Justification: The statement names the core decision (not the triggering request) and is specific to this problem (loan terms, tax status, horizon, reserve status all named); each of the five success criteria is independently checkable against section 6 (e.g., "ends in one concrete, decisive recommendation...with a named condition that would change the recommendation" is checked directly against the Confidence line's "would change it" enumeration).

**Criterion 2: Challenge Assumptions**
Quoted span (Assumption Audit scan, process output): "Scan complete: 5 chains, 19 steps walked in order; 2 assumptions surfaced (A-15, A-16), both added to the Classified Assumptions Table and marked inline on their originating steps."
Band: **Rigorous**
Justification: All 16 rows use the four-type scheme with matching prescribed-treatment vocabulary and token-led Verdict cells (`Challenge — ...`, `Accept — ...`); unverified assumptions used in chains carry "unverified — flagged"; the Assumption Audit scan confirms the Phase-4 scan was exhaustive over every named chain step and that both surfaced assumptions were folded back into the table, not left dangling.

**Criterion 3: Establish Ground Truths**
Quoted span: "?-marked: GT-11, GT-13, GT-14, GT-15 (4 of 16)" — checked against the Ground Truths list, which carries the `?` suffix on exactly GT-11, GT-13, GT-14, GT-15 and no others.
Band: **Rigorous**
Justification: Every GT carries a stable ID matching its use in section 4; every verified GT cites a specific source (user stipulation, this analysis's own computation, or a named external document) with a provenance label; the enumeration matches the list exactly; every unsuffixed GT feeding a HIGH-confidence chain (C1: GT-1,2,6,7,8; C4: GT-6,12,2) names a specific read-at-source location.

**Criterion 4: Reason Upward**
Quoted span (self-audit scan, Table 1): "C1 | ... | yes | n/a | yes | HIGH | ... | none" through "C5 | ... | yes | n/a | yes | MEDIUM | ... | none" — all five rows read `yes` under Form conforming? and Dependency clean?.
Band: **Rigorous**
Justification: All five chains in section 4 are form-conforming and dependency-clean per the self-audit scan; each chain carries a genuine intermediate (verified by the chain text, not merely the scan); the Abandoned Reasoning section documents four dead ends in the full What-was-tried/Why-abandoned/What-it-ruled-out structure; the two assumptions surfaced during the Phase-4 Assumption Audit (A-15, A-16) are declared inline with `[Assumes: X]` on their originating steps; no analogy is used as standalone evidence anywhere in section 4.

**Criterion 5: Validate**
Quoted span: "**Confidence:** MEDIUM — the core...claim rests on C1 and C4 alone, both HIGH, with no unresolved inputs. The comparative margin...rest additionally on C2, C3, and C5, each MEDIUM because they inherit GT-11?'s unverified dividend-yield blend and C9's forecast-based...central case."
Band: **Rigorous**
Justification: The Conclusion's MEDIUM rating equals its weakest contributing chain (C2/C3/C5, MEDIUM), consistent with D-07; no chain with a `?` input is rated HIGH (C2 is the only `?`-consuming chain and is MEDIUM); C3 and C5 are each rated no higher than C2 (MEDIUM), which their heads cite; the adversarial pass record (process output) carries all eight required parts — Recompute, Sensitivity, Rival, Premise, Causes, Clusters, Disposition, Falsification — each with substantive content, and every cluster carries a named disposition (a plan change or an explicitly accepted risk with a named mitigation).

**Criterion 6: Conclusion-to-Ground-Truth Traceability**
Quoted span (self-audit scan, Table 2): "Recommended approach... | bold lead-in | yes | ... | C1, C4" through "Confidence... | bold lead-in | yes | ... | C1, C2, C3, C4, C5" — all five section-6 constructs read `yes` under Claim under R11? with a named chain.
Band: **Rigorous**
Justification: Every Conclusion-section claim cites a specific named chain inline, matching the self-audit scan's claim-inventory table; the sole caveat with no chain (the A-11 tax-advantaged-space precondition) carries the sanctioned `no chain — flagged assumption only` marker rather than being presented as traced, which the output-template explicitly treats as honest disclosure rather than a defect; the Key Insight ("the safe-vs-risky framing is backwards for this household") is a non-obvious finding distinct from the Recommended Approach, not a restatement of it.

**Gate result:** cleared · passes: 1 · Fix/Repeat fired: no

## Structured summary (process output)

```json
{
  "schema_version": 1,
  "run_mode": "full-composer",
  "assumptions": [
    {
      "id": "A-1",
      "type": "untested belief",
      "verdict": "Challenge"
    },
    {
      "id": "A-2",
      "type": "untested belief",
      "verdict": "Challenge"
    },
    {
      "id": "A-3",
      "type": "current constraint",
      "verdict": "Accept"
    },
    {
      "id": "A-4",
      "type": "untested belief",
      "verdict": "Challenge"
    },
    {
      "id": "A-5",
      "type": "untested belief",
      "verdict": "Challenge"
    },
    {
      "id": "A-6",
      "type": "untested belief",
      "verdict": "Challenge"
    },
    {
      "id": "A-7",
      "type": "untested belief",
      "verdict": "Challenge"
    },
    {
      "id": "A-8",
      "type": "convention",
      "verdict": "Challenge"
    },
    {
      "id": "A-9",
      "type": "current constraint",
      "verdict": "Accept"
    },
    {
      "id": "A-10",
      "type": "current constraint",
      "verdict": "Accept"
    },
    {
      "id": "A-11",
      "type": "untested belief",
      "verdict": "Challenge"
    },
    {
      "id": "A-12",
      "type": "current constraint",
      "verdict": "Accept"
    },
    {
      "id": "A-13",
      "type": "current constraint",
      "verdict": "Accept"
    },
    {
      "id": "A-14",
      "type": "physical law",
      "verdict": "Accept"
    },
    {
      "id": "A-15",
      "type": "untested belief",
      "verdict": "Challenge"
    },
    {
      "id": "A-16",
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
      "read_at_source": true
    },
    {
      "id": "GT-9",
      "read_at_source": true
    },
    {
      "id": "GT-10",
      "read_at_source": true
    },
    {
      "id": "GT-11",
      "read_at_source": false
    },
    {
      "id": "GT-12",
      "read_at_source": true
    },
    {
      "id": "GT-13",
      "read_at_source": false
    },
    {
      "id": "GT-14",
      "read_at_source": false
    },
    {
      "id": "GT-15",
      "read_at_source": false
    },
    {
      "id": "GT-16",
      "read_at_source": true
    }
  ],
  "chains": [
    {
      "id": "C1",
      "confidence": "HIGH",
      "rests_on": [
        "GT-1",
        "GT-2",
        "GT-6",
        "GT-7",
        "GT-8"
      ]
    },
    {
      "id": "C2",
      "confidence": "MEDIUM",
      "rests_on": [
        "GT-9",
        "GT-11?",
        "GT-2"
      ]
    },
    {
      "id": "C3",
      "confidence": "MEDIUM",
      "rests_on": [
        "C2",
        "GT-8"
      ]
    },
    {
      "id": "C4",
      "confidence": "HIGH",
      "rests_on": [
        "GT-6",
        "GT-12",
        "GT-2"
      ]
    },
    {
      "id": "C5",
      "confidence": "MEDIUM",
      "rests_on": [
        "GT-6",
        "GT-3",
        "C2"
      ]
    }
  ],
  "dead_ends": [
    "Treating Option A's benefit as pure \"interest saved\" layered on top of the returned $60,000 principal",
    "Using the unconditional long-run historical average (~10% nominal) as the central-case return assumption for Option B",
    "Pairing Option A with an immediately-opened HELOC to \"have it both ways\" (pay down the mortgage and keep full liquidity)",
    "Series I Savings Bonds or investment-grade municipal bonds as a rival to chain C4's risk-free-ceiling conclusion"
  ],
  "techniques": {
    "applied": [
      "fishbone",
      "inversion",
      "second-order",
      "estimate",
      "theoretical-limit",
      "trade-off",
      "pre-mortem"
    ],
    "not_applied": [
      {
        "technique": "theoretical-limit",
        "phase": 1,
        "reason": "the essence is a capital-allocation decision between two named options, not a question of whether a stated figure is a convention mistaken for a hard bound"
      },
      {
        "technique": "inversion",
        "phase": 5,
        "reason": "the conclusion is a plan/recommendation, which the decision rule routes to pre-mortem rather than inversion"
      },
      {
        "technique": "five-whys",
        "phase": 3,
        "reason": "every ground truth bottoms out directly at a stipulated household fact, a direct source reading, or a single computed mathematical identity, with no composite claim requiring a multi-level reduce-to-primitives drill"
      }
    ]
  },
  "gate": {
    "passes": [
      {
        "bands": [
          "Rigorous",
          "Rigorous",
          "Rigorous",
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
    "recommendation": "Apply the full $60,000 as extra principal on the mortgage (Option A) (chain C1, C4). This converts the cash into a guaranteed, tax-free $111,913 of additional home equity by year 10 — a rate (6.43% EAR) that beats the household's only legally risk-free alternative (10-Year Treasuries, 5.28% pretax / 3.80% after-tax) and the entire current consensus 10-year equity forecast (Vanguard VCMM, 4.2%–6.2%) (chain C1, C4).",
    "confidence": "MEDIUM",
    "rests_on": [
      "C1",
      "C2",
      "C3",
      "C4",
      "C5"
    ]
  }
}
```
