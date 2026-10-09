## Answer

**Recommendation:** Allocate about 85% of the $60,000 ($51,000) to an extra mortgage-principal payment and about 15% ($9,000) to the taxable broad-market index fund (chain C7). This keeps nearly all of the paydown's guaranteed, tax-free advantage (chains C1, C2) and the trade-off's weighted edge (chain C5), while holding a small liquid buffer against payment-shock risk (chain C6).

**Band (from §6):** MEDIUM (chain C7).

**Would change it:** Confirming the historical-average return figure at a primary source, or genuine conviction that forward 10-year equity returns will run at or above roughly 9–10%/yr — above today's 4.2%–6.2% forecast (chain C4) — or a decision-weighting shift toward liquidity/flexibility (chain C5).

## 1. Problem Essence

**Core problem:** Given $60,000 of surplus cash (held above an already-fully-funded six-month emergency reserve) and a $240,000 non-tax-advantaged 6.25% mortgage with 27 years remaining, how should this specific household allocate that $60,000 between guaranteed debt extinguishment and risky taxable equity exposure to maximize risk-adjusted, after-tax household net worth and flexibility — evaluated honestly at a 10-year checkpoint even though the underlying debt obligation runs 27 years — and at what quantified return, risk-weighting, or liquidity-need threshold does the answer reverse?

**Success criteria:**
1. The analysis states the guaranteed after-tax effective-annual return of mortgage paydown as a number, and states the nominal pretax equity total return Option B would need to average over 10 years to match it dollar-for-dollar after taxes — not merely "it depends."
2. The Conclusion section names one specific recommended dollar/percentage allocation of the $60,000, not a range of equally-weighted options.
3. The Conclusion section states at least one quantified condition (a return threshold, a reweighting of decision criteria, or a liquidity-need fact) under which the recommended allocation reverses.
4. The analysis explicitly resolves whether "sell the investment at year 10" and "continue holding it" are different outcomes for comparison purposes, rather than silently picking one.
5. The analysis explicitly addresses what part of Option A's value is realized within the 10-year window versus only after it, given the mortgage's 27-year remaining term.

---

## 2. Assumptions Table

| Assumption | Type | Treatment | Verdict | Verification |
|------------|------|-----------|---------|--------------|
| Mortgage interest provides a 0% marginal tax shield because the household takes the standard deduction | current constraint | Record expiry: this reverses if future itemizable deductions (SALT, charitable giving, a future high-interest year) push Schedule A above the standard deduction, or if tax law changes the standard deduction or SALT cap | Accept — stipulated directly by the household about its own return; no external document exists for this analysis to open, and the figure is internally consistent with the 6.25%-is-the-true-cost framing the household itself supplies | source: household self-report of its own filing status; expiry condition stated above |
| Household marginal rates (28% ordinary, 18% LTCG/QDI) hold for the full 10-year horizon | current constraint | Record expiry: changes if Congress alters bracket thresholds/rates, or if household income moves the household into a different bracket | Accept — stipulated by the household; treated as the planning rate for the full horizon absent a stated reason to expect bracket drift | source: household self-report |
| The extra $60,000 principal payment leaves the monthly payment unchanged and simply shortens amortization (no recast) | current constraint | Record expiry: changes if the household separately elects a recast, which would lower the monthly payment instead of shortening the term — a different cash-flow profile not modeled here | Accept — explicitly stipulated by the household as the operative mechanism | source: household's own stated scenario framing |
| A one-time additional principal payment, with payment held constant, grows the avoided future loan balance by exactly the compounded mortgage rate | physical law | Promote directly to a ground-truth candidate — this is a provable identity of the standard loan-amortization recurrence, not an empirical claim | Accept — verified by direct computation in this analysis (see GT-5) | source: amortization arithmetic, independently recomputed in this analysis |
| The current 10-year Treasury yield (~4.5%) and Vanguard's current 10-year equity forecast are reasonable proxies for "the market's own view of future returns" today | current constraint | Record expiry: both move with market conditions; the specific figures are time-stamped (Aug/Jun 2026) and will drift | Accept — both read directly at the cited primary sources as of their stated dates | source: U.S. Treasury daily yield curve; Vanguard Capital Markets Model, see GT-6/GT-7 |
| The long-run historical ~9.94%/yr nominal U.S. equity average, and the 2000s "lost decade" ~-0.95%/yr figure, are representative anchors for the best- and worst-case empirical brackets | untested belief | Verify at primary source before using as a hard anchor; both were only confirmed through secondary aggregator summaries in this run | Challenge — flagged `GT-8?` and `GT-9?`; used only as illustrative brackets, not as the central planning estimate (Vanguard's forecast, which was read at source, fills that role) | unverified — flagged; see Ground Truths GT-8?, GT-9? |
| The household has no unused tax-advantaged retirement space (401(k)/IRA/HSA) competing for this $60,000 | untested belief | Verify directly with the household before executing either option; if false, it likely dominates both A and B | Challenge — not stated by the household either way; the question as posed scopes the choice to mortgage-vs-taxable-brokerage, so this is carried as a scope caveat on the recommendation rather than resolved | unverified — flagged; named explicitly in the Conclusion as a precondition |
| Selling the investment at year 10 and continuing to hold it (unrealized) are economically equivalent for comparison purposes, given a constant capital-gains tax rate | convention | Explicitly challenge: this equivalence holds only if the tax rate at the eventual realization date is the same 18% assumed throughout, and only if no basis step-up (e.g., at death) or tax-law change intervenes | Challenge — holds under the stated constant-rate assumption; flagged as contingent in Chain C4/C5 and in Abandoned Reasoning | derived in this analysis from the stated 18% LTCG rate; sensitivity named in Chain confidence lines |
| A household that has already fully funded a separate six-month emergency reserve has reduced — but not eliminated — the marginal value of additional liquidity from this $60,000 | current constraint | Quantify rather than assume away: liquidity is scored as a real, nonzero-weight criterion in the trade-off chain (C5) rather than ignored | Accept — directly follows from the household's own stated reserve status | source: household self-report of reserve status |
| The household will not panic-sell the equity position during an interim drawdown, and will not refinance the mortgage mid-horizon in a way that materially changes the realized rate on the already-paid-down principal | untested belief | Flag both as behavioral/future-decision risks; address in the adversarial pass rather than assuming away | Challenge — both are named explicitly as failure clusters in the Phase 5 adversarial pass (Clusters 2 and 3) with a stated disposition | unverified — flagged; addressed via the Phase 5 adversarial pass, not resolved by assumption |
| A broad U.S. total-market index fund's current dividend yield is approximately 1.3%, taxed annually at the 18% qualified rate during the holding period | untested belief | Verify against a live fund fact sheet before relying on the precise drag figure; the figure only moves the final after-tax dollar values by roughly 0.2 percentage points per year, so it is not load-bearing to the headline conclusion | Challenge — used as a reasonable approximation; flagged unverified because no live fund fact sheet was opened in this run | unverified — flagged; sensitivity is small (±0.2 pp/yr) and does not change which option wins any chain in this analysis |
| The household's 28% combined marginal rate is applied to Treasury-note interest in chain C1's risk-free comparison, though Treasury interest is state-tax-exempt (only the federal portion of the 28% actually applies) | convention | Challenge: this is a simplifying approximation surfaced during the Phase 4 Assumption Audit (chain C1, hop 2); it is not load-bearing because it only affects C1's illustrative 320-basis-point comparison, not the headline breakeven in C4, and it biases that one comparison in Option A's favor (overstating, not understating, A's advantage) | Challenge — surfaced during the Phase 4 Assumption Audit; not corrected because it is non-load-bearing and conservative in the direction of not overstating the final recommendation's confidence | unverified — flagged; affects only chain C1's illustrative gap, not chains C4/C5/C7 |
| The seven trade-off criteria and their relative weights (expected value 5, variance/guarantee 4, liquidity 3, long-term cash-flow-timing 3, tax efficiency 2, behavioral fit 2, flexibility 2) reflect this household's actual preferences | untested belief | Verify directly with the household before treating chain C5's ranking as final; surfaced during the Phase 4 Assumption Audit (chain C5, hop 1) | Challenge — chosen by this analysis as a reasonable default, not confirmed against the household's stated preferences; named explicitly as flip condition (b) in chain C7 | unverified — flagged; chain C5's own confidence line and chain C7's flip condition (b) both name this as the recommendation's main lever |

---

## 3. Ground Truths

- **GT-1** The household carries a $240,000 mortgage balance at a 6.25% fixed APR with 324 months (27 years) remaining, and takes the standard deduction, so the marginal tax shield on this mortgage's interest is 0% — the 6.25% APR is therefore already the household's true after-tax cost of this debt. Because a fixed-rate fully-amortizing loan's payment is uniquely determined by its current balance, rate, and remaining term, the existing monthly payment is M = 240,000 × r × (1+r)^324 / [(1+r)^324 − 1] with r = 0.0625/12, which computes to **M ≈ $1,535.36/month** — source: household self-report of loan balance/rate/term (first-hand knowledge of its own mortgage note), combined with the standard amortization-payment formula; read-at-source: the formula was applied and independently recomputed in this analysis (payment verified by back-solving that a $240,000 balance amortizes to $0 in exactly 324 months at this payment and rate).

- **GT-2** The household holds $60,000 in cash that sits above an already-fully-funded six-month emergency reserve, and its marginal rates are 28% on ordinary income and 18% on long-term capital gains/qualified dividends — source: household self-report of its own cash position and filing bracket; read-at-source: stipulated directly by the decision-maker as a first-hand fact about its own finances (no external document applies to a private financial fact of this kind).

- **GT-3** A standard loan-amortization identity: for a fixed-rate, fixed-payment loan, if an extra principal payment of $P is made at time 0 and the monthly payment M is held unchanged, the loan balance at any future month t is lower than it otherwise would have been by exactly P × (1+r)^t, where r is the monthly rate — because the amortization recurrence B(t) = B(0)(1+r)^t − M[(1+r)^t−1]/r is linear (affine) in the starting balance B(0) for fixed M and r, so the only effect of reducing B(0) by $P is to scale that one term by $P(1+r)^t, independent of M. Applied to this household's loan (r = 0.0625/12), a $60,000 extra payment is therefore guaranteed to reduce the year-10 (t=120) loan balance by $60,000 × (1.0625/12)¹²⁰ ≈ **$111,910** — verified in this analysis by computing both balances explicitly: with the extra payment, balance at t=120 ≈ $80,649; without it, balance at t=120 ≈ $192,559; difference ≈ $111,910, matching the closed-form prediction. The equivalent effective annual rate is (1+0.0625/12)¹² − 1 ≈ **6.44% EAR**, and because avoided mortgage interest is never itself a taxable event, this 6.44% is already an after-tax figure — source: standard loan-amortization mathematics; read-at-source: derived and independently recomputed by this analysis using the stated formula, not taken from an external citation.

- **GT-4** The current 10-Year U.S. Treasury Note yield was **4.51%**, dated 08/26/2026 — source: U.S. Department of the Treasury, Daily Treasury Par Yield Curve Rates; read-at-source: the specific table row for that date was fetched and quoted directly from home.treasury.gov. (A separate, lower-quality scrape of a different aggregator site returned an inconsistent 5.22% figure for 10/08/2026; that figure is discarded in favor of the Treasury's own primary data, consistent with a July 2026 secondary reading of ~4.66% reported elsewhere, both of which bracket the 4.51% figure used here and none of which resembles the discarded outlier.)

- **GT-5** Vanguard's Capital Markets Model (VCMM), based on its June 30, 2026 running, forecasts a 10-year annualized nominal return for U.S. equities of **4.2%–6.2%** (midpoint ≈5.2%), down from a 4.9%–6.9% range in the prior (March 2026) running — source: Vanguard Corporate, "Setting realistic expectations" (vemo-return-forecasts); read-at-source: the page was fetched directly and the figures quoted verbatim ("our 10-year expected annualized return for U.S. equities declined...to a range of 4.2%–6.2%...based on a June 30, 2026, running of the Vanguard Capital Markets Model").

- **GT-6?** The S&P 500's compound (geometric) average nominal annual total return from 1928–2024 is commonly cited as approximately **9.94%** — cited to: Aswath Damodaran's (NYU Stern) historical returns dataset; reported-by-delegate: this figure was supplied by a web-search summary citing secondary aggregator pages (walnutinvest.com, moneycrashers.com, dimensional.com), not read directly from Damodaran's own data file. **Phase 3 failure record:** this analysis directly opened Damodaran's primary data page (pages.stern.nyu.edu/~adamodar/.../histretSP.html); the page contains year-by-year raw annual return data for 1928–2025 but does not itself state a pre-computed compound-average summary statistic, so the 9.94% figure could not be confirmed at that primary source in this run — reason: citation does not support the claim (summary statistic absent from the primary data table opened). The figure is used only as an illustrative upper-range anchor, not as the central planning estimate.

- **GT-7?** The S&P 500's annualized total return (dividends reinvested) over the 2000–2009 "lost decade" is commonly cited as approximately **−0.95%/year** — cited to: aggregated market-history commentary (Dimensional, Janus Henderson, and others, as summarized); reported-by-delegate: this analysis did not open a primary total-return database to confirm the figure directly; it is used only as an illustrative worst-case empirical anchor, not as the central planning estimate.

- **GT-8?** A broad U.S. total-market index fund's current dividend yield is approximately **1.3%**, taxed annually as qualified dividend income — unverified: no live fund fact-sheet was opened in this run to confirm the current yield; used only to compute a small (≈0.2 percentage-point/year) tax-drag adjustment that is not load-bearing to any headline conclusion in this analysis.

```text
?-marked: GT-6?, GT-7?, GT-8? (3 of 8)
Read-at-source: GT-1 — standard amortization-payment formula applied to the household-stated balance/rate/term and independently recomputed
Read-at-source: GT-2 — stipulated directly by the household as first-hand knowledge of its own cash position and tax bracket; no external document applies to a private financial fact of this kind
Read-at-source: GT-3 — amortization identity derived and independently recomputed by this analysis (two full balance schedules computed and differenced)
Read-at-source: GT-4 — U.S. Treasury Daily Treasury Par Yield Curve Rates table, row for 08/26/2026, fetched and quoted directly
Read-at-source: GT-5 — Vanguard Corporate "Setting realistic expectations" (VCMM, June 30, 2026 running), fetched and quoted directly
```

---

## 4. Derivation Chains

### Conclusion C1: The mortgage paydown's guaranteed after-tax return exceeds the best comparable riskless market alternative available today

GT-1 (mortgage: $240k, 6.25% APR, 0% tax shield) + GT-2 (tax rates: 28% ordinary / 18% LTCG) + GT-3 (amortization identity) + GT-4 (10-yr UST yield 4.51%)
→ the amortization identity in GT-3 means the $60,000 extra payment guarantees a reduction in the household's future loan balance that compounds at exactly the mortgage's own rate with zero variance, an effective annual rate of 6.44%
→ because avoided mortgage interest is never itself a taxable event, this 6.44% is already an after-tax, risk-free return, whereas the 4.51% Treasury yield is ordinary taxable income that nets to roughly 3.25% after the household's 28% rate *[Assumes: A-12]*
→ the mortgage paydown therefore offers a guaranteed after-tax return roughly 320 basis points above the best comparable after-tax riskless market alternative available to this household today

**Pre-check:** head GT-1, GT-2, GT-3, GT-4 · ?-marked: none · lowest cited: none · Inputs ceiling: HIGH
**Confidence:** HIGH — all four inputs are unsuffixed and read at source; every hop is arithmetic that recomputes independently of the chain text (verified in GT-3 and GT-4's own entries). The only competing framing — comparing the mortgage rate against the pretax Treasury yield rather than the after-tax yield — is addressed and ruled out directly in hop 2, leaving no live rival to this narrow comparison.

---

### Conclusion C2: Because Option A's 10-year outcome is a closed-form identity rather than a market draw, its best case and worst case coincide — a theoretical ceiling and floor that no risky asset can share

GT-3 (amortization identity: $60k extra principal) + C1 (6.44% EAR after-tax riskless return)
→ compounding $60,000 at the mortgage's monthly rate for 120 months produces a guaranteed year-10 reduction in future loan balance of $60,000 × 1.8652 ≈ $111,910, exactly as GT-3 predicts
→ this $111,910 figure is derived from a closed-form amortization formula rather than observed from a market process, so nothing about economic conditions over the next 10 years can move it up or down — the ideal ceiling and the worst-case floor for Option A are mathematically forced to coincide at $111,910
→ Option A therefore has zero dispersion of possible 10-year outcomes, a structural property that is categorically different from — not merely safer than — any return distribution available to Option B

**Pre-check:** head GT-3, C1 (HIGH) · ?-marked: none · lowest cited: HIGH · Inputs ceiling: HIGH
**Confidence:** HIGH — the $111,910 figure recomputes directly from the stated formula (independently checked in GT-3), the ceiling-equals-floor claim follows deductively from the fact that no variable in the formula besides contractually fixed terms exists, and no rival "range" for Option A survives this reasoning — any apparent dispersion in Option A's outcome would require a change to the loan's own fixed terms, a different question addressed as refinance risk in the Phase 5 adversarial pass (Cluster 3, below).

---

### Conclusion C3: Option B's 10-year outcome is a wide empirical range, not a law-derived bound — bracketed from roughly $54,500 (worst modern decade) to roughly $135,000 (long-run historical average), with today's consensus forecast sitting near the bottom of that range

GT-5 (Vanguard 10-yr equity forecast 4.2%–6.2%) + GT-6? (historical average ≈9.94%/yr) + GT-7? (2000s lost decade ≈−0.95%/yr) + GT-8? (dividend yield ≈1.3%) + GT-2 (tax rates: 28% ordinary / 18% LTCG)
→ applying the household's 18% dividend/LTCG rate to each pretax annualized-return scenario converts it into an after-tax 10-year dollar value for a $60,000 lump sum, using after-tax value ≈ 0.82 × [60,000 × (1 + g − 0.0023)¹⁰] + 0.18 × 60,000, where g is the pretax nominal annualized total return and 0.0023 is GT-8?'s small dividend-tax drag *[Assumes: A-11]*
→ at GT-7?'s worst-modern-decade rate (g ≈ −0.95%/yr) this formula gives roughly $54,500; at GT-5's current forecast band (g = 4.2%–6.2%/yr) it gives roughly $83,400–$98,600 (midpoint ≈$90,700); at GT-6?'s long-run historical average (g ≈ 9.94%/yr) it gives roughly $135,000 *[Assumes: A-6]*
→ unlike Option A's single forced value, Option B's year-10 outcome is a genuinely wide empirical distribution spanning roughly $54,500 to $135,000, and the one figure in that range actually read at a primary forward-looking source today (GT-5) sits only about 19% above the bottom of that range, not near its middle or top

**Pre-check:** head GT-5, GT-6?, GT-7?, GT-8?, GT-2 · ?-marked: GT-6?, GT-7?, GT-8? · lowest cited: none · Inputs ceiling: MEDIUM
**Confidence:** MEDIUM — GT-6? and GT-7? are reported-by-delegate anchors used only to bound the illustrative range (verification that would remove them as a cause of this downgrade: opening a primary total-return database directly — e.g., a CRSP or S&P index data file — to confirm both figures at source). GT-8?'s dividend-yield approximation is unverified but moves the final dollar figures by only ≈0.2 percentage points/year and is not itself a cause of this downgrade. GT-5 is unsuffixed and read at source, and the arithmetic recomputes as shown in hop 2.

---

### Conclusion C4: The breakeven nominal pretax equity return required for Option B to match Option A's guaranteed outcome is approximately 7.7%/yr — above today's consensus forecast, below the long-run historical average

C2 ($111,910 guaranteed value) + C3 (after-tax dollar-value formula for Option B) + GT-5 (4.2%–6.2% forecast) + GT-6? (historical average ≈9.94%/yr)
→ setting C3's after-tax formula equal to C2's $111,910 and solving for g gives a required after-dividend-tax annual growth rate of approximately 7.47%/yr
→ adding back GT-8?'s ≈0.23-point dividend-tax drag converts that into a required pretax nominal annualized total return of approximately 7.7%/yr over the full 10 years *[Assumes: A-11]*
→ the forecast band stated in GT-5 (4.2%–6.2%) sits below this 7.7% breakeven, while the long-run historical average stated in GT-6? (≈9.94%) sits above it
→ on the one return estimate actually read at a primary forward-looking source today, Option B is expected to underperform Option A in pure expected-dollar terms, and only a return assumption close to or above the long-run historical average — well above today's consensus forecast — reverses that expectation

**Pre-check:** head C2 (HIGH), C3 (MEDIUM), GT-5, GT-6? · ?-marked: GT-6? · lowest cited: MEDIUM · Inputs ceiling: MEDIUM
**Confidence:** MEDIUM — capped by C3's MEDIUM rating (its own GT-6?/GT-7? dependency) and by GT-6?'s direct unverified status here. Verification that would lift this to HIGH: confirming GT-6? at a primary total-return source, and/or obtaining a second independent forward-return forecast from a provider other than Vanguard that agrees with GT-5's band, removing the "single-forecaster" fragility from this breakeven claim.

---

### Conclusion C5: A locked-weight, multi-criterion comparison favors full mortgage paydown over every alternative allocation — including a 50/50 blend and leaving the cash in a savings account — and does so even under the optimistic historical-average return scenario

C2 (Option A deterministic $111,910) + C3 (Option B range) + C4 (breakeven ≈7.7%/yr) + GT-2 (tax rates/liquidity context)
→ scoring four allocations (A: 100% paydown, B: 100% index, C: 50/50 split, D: status quo cash) on seven weighted criteria — expected after-tax value (weight 5), guaranteed-ness/variance (weight 4), liquidity (weight 3), long-term cash-flow-timing effect (weight 3), tax efficiency (weight 2), behavioral fit (weight 2), flexibility (weight 2) — against anchors set by C3's $54,500–$135,000 range produces weighted totals of A=80, C=72, D=68, B=59 at today's Vanguard-midpoint return assumption *[Assumes: A-13]*
→ re-scoring only the expected-value criterion at GT-6?'s optimistic long-run historical-average return still leaves A=80, C=77, B=69, D=68 — A's lead survives because the maximum possible expected-value-criterion score cannot close the 16-weighted-point structural lead A holds on the other six criteria combined *[Assumes: A-6]*
→ under this locked weighting, full mortgage paydown dominates every alternative at every return assumption considered, including the optimistic one, which means the recommendation's sensitivity lies in the weighting scheme itself, not in the return assumption

**Pre-check:** head C2 (HIGH), C3 (MEDIUM), C4 (MEDIUM), GT-2 · ?-marked: none directly · lowest cited: MEDIUM · Inputs ceiling: MEDIUM
**Confidence:** MEDIUM — capped by C3/C4's MEDIUM rating. The weighting scheme itself is an explicit judgment call this analysis made (criteria and weights stated and locked before scoring, per the trade-off procedure) rather than an empirical fact, so a reader who would weight liquidity or flexibility materially higher than this analysis did could reach a different ranking — named precisely as flip condition (b) in chain C7.

---

### Conclusion C6: Extending the recommendation through both an actor lens and a time lens surfaces effects that change what the 10-year comparison means, without contradicting any ground truth

C5 (recommend A) + GT-1 (27-year remaining term, $1,535/month payment)
→[2nd, time lens] because Option A's extra payment shortens the amortization from 324 months to roughly 182 months (≈15.2 years) rather than 120 months, most of its structural benefit — freeing the full $1,535/month payment roughly 11.8 years earlier than otherwise — arrives after the stated 10-year horizon, not within it, so a year-10-only dollar snapshot understates Option A's full value
→[2nd, actor lens] Option B's path generates recurring tax revenue (dividend tax each year, capital-gains tax at realization) that Option A's path never generates at all, a transfer to the tax authority that is a real, if small, second-order cost unique to Option B
→[2nd/3rd, actor+time lens] a 10-year lump-sum equity holding realistically spans one or two serious drawdowns, so Option B's realized outcome depends not only on the market's draw but on the household's own behavior under stress — a second-order dependency Option A's contractual, non-market mechanism does not share *[Assumes: A-10]*
→ none of these extensions contradicts a ground truth, so they extend chain C5's recommendation rather than reversing it, while also showing that the 10-year framing specifically understates Option A relative to Option B's framing

**Pre-check:** head C5 (MEDIUM), GT-1 · ?-marked: none directly · lowest cited: MEDIUM · Inputs ceiling: MEDIUM
**Confidence:** MEDIUM — inherits C5's cap. The amortization-shortening arithmetic in hop 1 is itself HIGH (recomputed directly from GT-3), but the chain's overall rating is capped by the chain it extends, per the unverified-input/cap rule (D-07).

---

### Conclusion C7: The recommended allocation is approximately 85% ($51,000) to extra mortgage principal and approximately 15% ($9,000) to the taxable index fund, reversing only under three named, quantified conditions

C5 (trade-off recommends A, dominant even at historical-average return) + C6 (second-order: most of A's value arrives after year 10; a liquidity/payment-shock gap is not fully priced into C5's fixed weighting) + C4 (breakeven ≈7.7%/yr)
→ the locked-weight scoring in chain C5 already treats liquidity as a real, nonzero-weight criterion (weight 3 of 21)
→ the second-order extension in chain C6 shows that weight likely understates the household's true exposure to a payment-shock scenario, because Option A's unchanged monthly payment provides zero relief if income is disrupted during the 10-year window *[Assumes: A-9]*
→ mitigating that specific exposure without giving up C5's quantitative edge means tilting slightly short of the trade-off-optimal 100% allocation, retaining a small liquid slice as insurance rather than eliminating it entirely
→ a 85%/15% split — approximately $51,000 to extra mortgage principal and approximately $9,000 to the index fund — keeps essentially all of chains C1/C2's guaranteed after-tax advantage and nearly all of C5's weighted-score edge, while restoring a modest liquid position against the risk C6 surfaced
→ this recommendation reverses toward fuller equity exposure only under at least one of three named, quantified conditions
→ condition (a): conviction that forward 10-year nominal equity returns will run at or above roughly 9–10%/yr, matching or exceeding GT-6?'s historical average and well above GT-5's current 4.2%–6.2% consensus band
→ condition (b): a decision-criteria reweighting toward liquidity/flexibility of the magnitude identified in chain C5's flip test — roughly quadrupling the liquidity weight or zeroing the expected-value weight
→ condition (c): confirmed unused tax-advantaged retirement space (401(k)/IRA/HSA), which this analysis did not resolve and which would dominate both options if present *[Assumes: A-7]*

**Pre-check:** head C5 (MEDIUM), C6 (MEDIUM), C4 (MEDIUM) · ?-marked: none directly · lowest cited: MEDIUM · Inputs ceiling: MEDIUM
**Confidence:** MEDIUM — capped by C4/C5/C6, each of which already names its own downgrade cause (the GT-6?/GT-7? anchors in C3/C4; the locked-weighting judgment call in C5). This chain adds one new judgment of its own — the specific 85/15 split, chosen to address the payment-shock cluster surfaced by the Phase 5 adversarial pass below without materially giving up C5's quantitative edge — which is a reasoned allocation choice, not a figure derived from a ground truth, and is named here explicitly rather than smuggled into the Conclusion section.

---

## 5. Abandoned Reasoning

### Dead End: "Just compare the 6.25% mortgage rate to the ~10% historical stock market average and invest, since 10% > 6.25%"

**What was tried:** Build a one-line chain directly from the nominal mortgage APR and the commonly-cited ~10% long-run nominal historical average equity return, concluding that because 10% exceeds 6.25%, the household should invest the full $60,000 rather than pay down the mortgage.

**Why abandoned:** This chain fails on three specific points, not one. First, it compares a pretax historical average against an after-tax guaranteed rate — it ignores the ~18% capital-gains/dividend tax drag that chain C3 applies, which materially lowers the equity side's realized figure. Second, it uses the long-run historical mean as if it were a forward-looking estimate, when the one return figure this analysis could actually read at a live, forward-looking primary source (GT-5, Vanguard's VCMM) sits at 4.2%–6.2% — well below both the historical average and chain C4's 7.7% breakeven — precisely because current valuations are elevated, a documented reason forward-looking forecasts diverge from trailing averages. Third, it conflates a single point estimate with the wide empirical range chain C3 establishes (roughly $54,500 to $135,000 after tax at year 10), silently assuming the best historical outcome rather than the one return path this analysis has actual, dated evidence for today.

**What it ruled out:** Treating "historical average equity return exceeds the mortgage rate" as a sufficient, stand-alone justification for Option B. It is not — the correct comparison requires the after-tax rate on both sides and a forward-looking, not trailing, estimate of the uncertain side. Chains C3 and C4 replace this one-line comparison with the bracketed, after-tax version.

### Dead End: "Treat 'sell the investment at year 10' and 'continue holding it' as requiring two separate analyses"

**What was tried:** Model Option B's year-10 outcome twice — once assuming the position is liquidated and the capital-gains tax is paid immediately, and once assuming it continues to be held unrealized — on the theory that these are materially different outcomes requiring separate comparison tracks against Option A.

**Why abandoned:** Under the constant-18%-tax-rate assumption this analysis carries throughout (Assumptions Table), the after-tax-if-sold value (0.82 × V10 + 0.18 × basis) and the unrealized value minus its embedded tax liability (V10 − 0.18 × (V10 − basis)) are algebraically identical. The two "separate" analyses collapse into the same number, so building both added no information — the only way they would genuinely diverge is if the realization-date tax rate differs from today's 18% (a step-up in basis at death, a future rate change, or a shift into the 3.8% net investment income surtax), which is already carried as a named, unresolved assumption in the Assumptions Table rather than as a second full analysis track.

**What it ruled out:** A second, parallel set of derivation chains for "sold" versus "held" scenarios. One formula, applied once, covers both under the stated tax-rate assumption; the place this could matter (a future tax-rate change) is a sensitivity note, not a second analysis.

---

## 6. Conclusion

**Recommended approach:** Allocate approximately 85% of the $60,000 ($51,000) to an extra one-time mortgage principal payment, and approximately 15% ($9,000) to the taxable broad-market index fund (chain C7). This captures essentially all of the guaranteed, tax-free, after-tax-return advantage of paying down the mortgage (chains C1, C2) and nearly all of the multi-criterion trade-off's weighted edge (chain C5), while retaining a small liquid position as insurance against the payment-shock risk the second-order analysis surfaced (chain C6).

**Key insight:** The mortgage paydown is not merely "the safe choice" — it is a guaranteed, tax-free 6.44% effective annual return that already beats the best after-tax riskless market alternative available today by roughly 320 basis points (chain C1), and its 10-year outcome is a closed-form identity whose best case and worst case are mathematically forced to be the same number (chain C2). Equities have no such floor: the one return estimate this analysis could verify at a live, forward-looking primary source today (Vanguard's 4.2%–6.2% forecast) sits below the ≈7.7%/yr return equities would need to average, after tax, just to tie the guaranteed outcome (chain C4) — and because that required rate also happens to sit below even the optimistic long-run historical average, the usual "stocks beat mortgage rates over the long run" intuition is quietly comparing the wrong numbers (chain C3, C4).

**Trade-offs acknowledged:** This recommendation gives up some expected dollar value relative to a scenario in which equity returns run at or above the long-run historical average over the next decade (chain C4), and it leaves the chosen $9,000 equity slice fully exposed to the same return uncertainty bracketed in chain C3. It also commits $51,000 to an illiquid form (home equity) that cannot be recovered without a refinance, a HELOC, or a sale (chain C6) — a real cost this analysis accepts explicitly rather than ignores, which is precisely why the allocation is 85/15 rather than 100/0 (chain C7).

**Pre-check:** head C1 (HIGH), C2 (HIGH), C3 (MEDIUM), C4 (MEDIUM), C5 (MEDIUM), C6 (MEDIUM), C7 (MEDIUM) · ?-marked: none directly · lowest cited: MEDIUM · Inputs ceiling: MEDIUM
**Confidence:** MEDIUM — the recommendation rests on chain C7, which is capped at MEDIUM by its own inputs (C4, C5, C6), each of which names its own downgrade cause: C3/C4 rest on the reported-by-delegate GT-6?/GT-7? empirical-range anchors (verification path: open a primary total-return database directly to confirm both), and C5 rests on an explicit, locked trade-off weighting that is a stated judgment call rather than an empirical fact (sensitivity named in C5's flip test and restated as flip condition (b) in C7). The structural finding that does not depend on any of these — that Option A is a deterministic 6.44% after-tax return while Option B is a genuinely wide, currently below-breakeven-forecast empirical range — is HIGH confidence (chains C1, C2) and does not move with any of the open verifications above; what remains open is only how far short of 100% the final split should be, not which side carries the larger share.
## Appendix — process output

## §6→§4 closure ledger (process output)

- "Allocate approximately 85% of the $60,000 ($51,000) to an extra one-time mortgage principal payment, and approximately 15% ($9,000) to the taxable broad-market index fund" → chain C7 ✓
- "This captures essentially all of the guaranteed, tax-free, after-tax-return advantage of paying down the mortgage" → chains C1, C2 ✓
- "nearly all of the multi-criterion trade-off's weighted edge" → chain C5 ✓
- "retaining a small liquid position as insurance against the payment-shock risk the second-order analysis surfaced" → chain C6 ✓
- "The mortgage paydown is...a guaranteed, tax-free 6.44% effective annual return that already beats the best after-tax riskless market alternative available today by roughly 320 basis points" → chain C1 ✓
- "its 10-year outcome is a closed-form identity whose best case and worst case are mathematically forced to be the same number" → chain C2 ✓
- "the one return estimate this analysis could verify at a live, forward-looking primary source today...sits below the ≈7.7%/yr return equities would need to average, after tax, just to tie the guaranteed outcome" → chain C4 ✓
- "that required rate also happens to sit below even the optimistic long-run historical average" → chains C3, C4 ✓
- "This recommendation gives up some expected dollar value relative to a scenario in which equity returns run at or above the long-run historical average" → chain C4 ✓
- "it leaves the chosen $9,000 equity slice fully exposed to the same return uncertainty bracketed in chain C3" → chain C3 ✓
- "It also commits $51,000 to an illiquid form...that cannot be recovered without a refinance, a HELOC, or a sale" → chain C6 ✓
- "which is precisely why the allocation is 85/15 rather than 100/0" → chain C7 ✓
- "**Pre-check:**" line (§6) → chains C1, C2, C3, C4, C5, C6, C7, each with its stated band ✓ (self-citing head)
- "**Confidence:**" line (§6) → chains C3, C4, C5, C1, C2 ✓

Ledger complete: 14 claims identified, 14 traced to a named chain, 0 cut.
## Assumption Audit scan (process output)

| Chain | Step | Step Text (brief) | Assumption surfaced? | Added to Table? |
|-------|------|--------------------|-----------------------|------------------|
| C1 | 1 | compute 6.44% EAR from GT-3's amortization identity | none | n/a |
| C1 | 2 | avoided interest is tax-free; Treasury yield nets to ~3.25% after 28% rate | Treasury interest taxed at full 28% combined rate, though it is state-tax-exempt (new) | yes — added as A-12 |
| C1 | 3 | conclude ~320bp guaranteed after-tax advantage | none | n/a |
| C2 | 1 | compound $60k at monthly mortgage rate to $111,910 at t=120 | none | n/a |
| C2 | 2 | ceiling=floor because formula has no market variable | none | n/a |
| C2 | 3 | conclude zero dispersion for Option A | none | n/a |
| C3 | 1 | state after-tax dollar-value formula using dividend-drag constant | relies on existing dividend-yield assumption | none (already in table: A-11) |
| C3 | 2 | plug worst/forecast/historical rates into formula | relies on existing historical-anchor assumption | none (already in table: A-6) |
| C3 | 3 | conclude Option B is a wide empirical range, forecast near bottom | none | n/a |
| C4 | 1 | solve formula for breakeven after-div-tax rate | none | n/a |
| C4 | 2 | add back dividend-tax drag to get pretax breakeven ≈7.7% | relies on existing dividend-yield assumption | none (already in table: A-11) |
| C4 | 3 | compare 7.7% to GT-5 band and GT-6? average | none | n/a |
| C4 | 4 | conclude Option B underperforms on today's forecast | none | n/a |
| C5 | 1 | score 4 allocations on 7 locked, weighted criteria | the specific criteria/weights reflect this household's true preferences (new) | yes — added as A-13 |
| C5 | 2 | re-score expected-value criterion at historical-average rate | relies on existing historical-anchor assumption | none (already in table: A-6) |
| C5 | 3 | conclude A dominates at every return assumption considered | none | n/a |
| C6 | 1 | amortization shortens 324→~182 months, freeing cash flow after yr 10 | none | n/a |
| C6 | 2 | Option B generates recurring tax revenue Option A does not | none | n/a |
| C6 | 3 | Option B's realized outcome depends on household behavior under stress | relies on existing no-panic-sell assumption | none (already in table: A-10) |
| C6 | 4 | conclude extensions do not contradict any ground truth | none | n/a |
| C7 | 1 | C5's weighting already assigns liquidity a nonzero weight | none | n/a |
| C7 | 2 | that weight likely understates payment-shock exposure | relies on existing reserve/liquidity assumption | none (already in table: A-9) |
| C7 | 3 | mitigating that exposure means tilting short of 100% to Option A | none | n/a |
| C7 | 4 | state the 85%/15% ($51,000/$9,000) split | none — a reasoned allocation choice, not a hidden premise | n/a |
| C7 | 5 | introduce three reversal conditions | none | n/a |
| C7 | 6 | condition (a): equity-return conviction ≥9–10%/yr | relies on existing GT-5/GT-6? facts | none (already in table: A-5, A-6) |
| C7 | 7 | condition (b): reweighting toward liquidity/flexibility | relies on existing weighting assumption | none (already in table: A-13) |
| C7 | 8 | condition (c): confirmed unused tax-advantaged space | relies on existing unused-space assumption | none (already in table: A-7) |

Audit complete: 29 chain steps across 7 chains, visited in order; 2 new assumptions surfaced (A-12, A-13), both added to the Assumptions Table in section 2; all other dependent steps rely on assumptions already present in that table.
## Self-audit scan (process output)

| Chain | Chain Head (brief) | Form conforming? | Rule applied | Dependency clean? | Band | Act attempted? | Edges fired |
|-------|---------------------|-------------------|---------------|--------------------|------|-----------------|-------------|
| C1 | GT-1, GT-2, GT-3, GT-4 | yes | n/a | yes | HIGH | yes | none |
| C2 | GT-3, C1 | yes | n/a | yes | HIGH | yes | none |
| C3 | GT-5, GT-6?, GT-7?, GT-8?, GT-2 | yes | n/a | yes | MEDIUM | yes | none |
| C4 | C2, C3, GT-5, GT-6? | yes | n/a | yes | MEDIUM | yes | none |
| C5 | C2, C3, C4, GT-2 | yes | n/a | yes | MEDIUM | yes | none |
| C6 | C5, GT-1 | yes | n/a | yes | MEDIUM | yes | none |
| C7 | C5, C6, C4 | yes | n/a | yes | MEDIUM | yes | none |

| §6 Span (brief) | Construct | Claim under R11? | R11 clause applied | Chain cited |
|-------------------|-----------|-------------------|----------------------|---------------|
| **Recommended approach:** 85%/15% split... | bold lead-in | yes | colon closes bold span; assertion on same line | C7 |
| **Key insight:** guaranteed 6.44% beats... | bold lead-in | yes | colon closes bold span; assertion on same line | C1, C2, C3, C4 |
| **Trade-offs acknowledged:** gives up expected value... | bold lead-in | yes | colon closes bold span; assertion on same line | C3, C4, C6, C7 |
| **Pre-check:** head C1 (HIGH)... | bold lead-in | yes | §6 pre-check line is itself a claim under R11, discharged by the chains its own head names | C1, C2, C3, C4, C5, C6, C7 |
| **Confidence:** MEDIUM — the recommendation rests on C7... | bold lead-in | yes | colon closes bold span; assertion on same line | C3, C4, C5 (C1, C2 also referenced) |

Scan complete: 7 chain rows, one per section-4 chain block in order; 5 section-6 rows, one per construct in order — 5 claims under R11, 0 excluded. 0 chains malformed, 0 claims untraced.
## Adversarial pass (process output)

**Recompute.** Monthly payment M = 240,000 × (0.0625/12) × (1.0625/12)^324 / [(1.0625/12)^324 − 1] recomputes to ≈$1,535.36/month, matching GT-1. The guaranteed year-10 value of the $60,000 paydown recomputes as 60,000 × (1 + 0.0625/12)^120 ≈ 60,000 × 1.86517 ≈ $111,910, matching GT-3/C2. The effective annual rate (1 + 0.0625/12)^12 − 1 ≈ 6.435% (stated as 6.44%, rounded) matches C1. The breakeven pretax equity rate solved from 0.82 × [60,000 × (1 + g − 0.00234)^10] + 0.18 × 60,000 = 111,910 recomputes to g ≈ 7.70%/yr, matching C4. The trade-off weighted totals recompute from the stated per-criterion scores and weights to A=80, C=72, D=68, B=59 at the Vanguard-midpoint scenario and A=80, C=77, B=69, D=68 at the historical-average scenario, both matching C5 exactly.

**Sensitivity.** The single most sensitive ground truth is **GT-6?** (`?`-marked) — the long-run historical average nominal equity return (≈9.94%/yr). If realized 10-year forward returns track GT-6? rather than GT-5's current forecast band, chains C4, C5, and C7 flip toward favoring more of Option B (condition (a)). Verification that would resolve this: opening a primary total-return database (e.g., a CRSP or S&P index data file) to confirm GT-6? at source, and periodically re-checking Vanguard's (or another provider's) forward forecast against realized returns as the horizon progresses.

**Rival.** Headline conclusion (85/15 toward A): the strongest rival is "100% to Option B," resting on the belief that forward returns will resemble the long-run historical average rather than today's consensus forecast — this rival is not settled by this analysis; it is carried live as flip condition (a) in chain C7. Chain C5 (trade-off ranking): the strongest rival is a reweighting that values liquidity/flexibility far more heavily than this analysis's locked weights — also carried live, as flip condition (b) in C7. Chains C1/C2 (the deterministic-guarantee claims): rival not applicable — these are closed-form arithmetic identities with no plausible competing reading. Chain C3 (Option B's range): a rival reading in which the dividend-tax-drag approximation materially understates true tax drag was considered and ruled out as immaterial — sensitivity is ±0.2 percentage points/year, which does not change which option wins any chain in this analysis (see Assumptions Table, row for A-11).

**Premise.** It is now 10 years later, and allocating 85% of the $60,000 to mortgage paydown and 15% to the index fund has turned out to be the wrong call for this household.

**Causes (unfiltered, from the household's own viewpoint, a skeptical financial advisor's viewpoint, and a future-self facing a liquidity crunch):**
1. Equity markets delivered roughly 10–15%/yr for the decade, making the 85% paydown look like a large opportunity cost in hindsight.
2. The household faced an unexpected large cash need within the 10 years and could not access the $51,000 of home equity without a slow or costly refinance/HELOC, while a fully-invested position could have been partially sold instead.
3. Mortgage rates fell substantially and the household refinanced, so the "locked-in 6.44% EAR" no longer held for the back half of the horizon.
4. The household psychologically regretted "losing" liquidity and felt unable to seize a good opportunity because capital was trapped in home equity.
5. Income disruption made even the unchanged monthly mortgage payment difficult to meet, and the extra principal already paid provided zero monthly cash-flow relief because no recast was elected.
6. The household never confirmed whether 401(k)/IRA/HSA space was unused, and tax-advantaged investing would have dominated both A and B.
7. Inflation ran hotter than assumed, eroding the real value of the "guaranteed" nominal return while nominal equity prices rose with it.
8. The household panic-sold the 15% equity slice near a market bottom during a drawdown, converting a paper loss into a permanent one.

**Clusters.**
- **Cluster 1 — Return-regime risk** (causes 1, 7) — bears on C3, C4, C5, C7. **Disposition:** explicitly accepted risk; chain C7's condition (a) already names the exact return threshold (≥9–10%/yr) that would reverse the call, so this is a bounded, disclosed risk rather than an unknown one.
- **Cluster 2 — Liquidity lock-in / payment-shock risk** (causes 2, 4, 5) — bears on C2, C6, C7. **Disposition:** plan change — this cluster is the reason chain C7 recommends 85/15 rather than 100/0; additionally, the household should confirm HELOC/line-of-credit eligibility now, while income and credit are strong, as a low-cost backstop beyond the $9,000 slice.
- **Cluster 3 — Rate-regime / refinance risk** (cause 3) — bears on C1, C2. **Disposition:** explicitly accepted risk; paying down principal is never harmful in absolute dollar terms, and refinancing a smaller balance after extra paydown is itself a minor secondary benefit — no further plan change beyond noting this trade-off in section 6.
- **Cluster 4 — Suboptimal resource sequencing** (cause 6) — bears on C7's condition (c). **Disposition:** plan change — confirm all available 401(k)/IRA/HSA space is maxed before executing either A or B; already named as a precondition in chain C7.
- **Cluster 5 — Behavioral execution risk on the equity slice** (cause 8) — bears on C6. **Disposition:** plan change — place the $9,000 equity slice under a pre-committed written instruction not to sell during a drawdown, since at this small size the dominant risk to it is behavioral, not market-driven.

**Falsification.** This recommendation is false — i.e., the household should have allocated more to Option B — if realized nominal pretax equity total returns over the next 10 years average at or above approximately 7.7%/yr (chain C4's breakeven), and is more strongly false if they average at or above approximately 9–10%/yr, matching or exceeding the long-run historical average (chain C7's condition (a)).
## Techniques not applied (process output)

five-whys — not applicable — the ground truths needed here (the amortization identity, the household's own loan/tax facts) are already irreducible formulas or first-hand facts; no compound claim required a reduce-to-primitives drill
fishbone — not applicable — the assumption space was directly enumerable from the two options' own structure; no multi-causal breadth-first brainstorm was needed to surface candidate assumptions
inversion — not applicable — the Phase 5 conclusion is a plan/recommendation (an allocation), not a bare claim, so the decision rule routes the adversarial pass to pre-mortem instead of inversion

## Self-Audit Gate (process output)

**Criterion 1: Identify Essence**
Quoted span: "Given $60,000 of surplus cash...how should this specific household allocate that $60,000 between guaranteed debt extinguishment and risky taxable equity exposure to maximize risk-adjusted, after-tax household net worth and flexibility — evaluated honestly at a 10-year checkpoint even though the underlying debt obligation runs 27 years — and at what quantified return, risk-weighting, or liquidity-need threshold does the answer reverse?"
Band: **Rigorous**
Justification: the statement names the specific household facts and the specific tension (10-year checkpoint vs. 27-year obligation) rather than restating the prompt generically, and each of the five success criteria is a verb+subject+outcome triplet checkable directly against section 6 (e.g., "names one specific recommended dollar/percentage allocation" is checked by reading the Recommended-approach line).

**Criterion 2: Challenge Assumptions**
Quoted span (Assumption Audit scan): "Audit complete: 29 chain steps across 7 chains, visited in order; 2 new assumptions surfaced (A-12, A-13), both added to the Assumptions Table in section 2; all other dependent steps rely on assumptions already present in that table."
Band: **Rigorous**
Justification: every row in the Assumptions Table carries a Type from the four-type scheme, a Treatment matching that type's prescribed action, a token-first Verdict with an em-dash justification, and a Verification cell with a specific source or "unverified — flagged"; multiple rows are Challenged rather than merely Accepted; and the Assumption Audit scan confirms the exhaustive per-step sweep required before this criterion is scored, with the two newly-surfaced assumptions (A-12, A-13) added to the table rather than left implicit.

**Criterion 3: Establish Ground Truths**
Quoted span (Ground Truths provenance summary): "?-marked: GT-6?, GT-7?, GT-8? (3 of 8)" — compared against the Ground Truths list, exactly GT-6?, GT-7?, and GT-8? carry the `?` suffix, and no other entry does.
Band: **Rigorous**
Justification: every GT carries a stable ID matching its use in section 4; every unsuffixed GT (GT-1 through GT-5) names a read-at-source location in the provenance summary; the three delegate-reported/unverified GTs are enumerated by ID and that enumeration matches the list exactly; GT-6 additionally carries an explicit Phase 3 failure record (primary source opened, summary statistic not found in it) rather than a bare citation; no criterion-3-scope GT feeds a HIGH chain while unverified — the two HIGH chains (C1, C2) rest only on GT-1 through GT-4, all unsuffixed and read at source.

**Criterion 4: Reason Upward**
Quoted span (self-audit scan, chain-form table): "C1 | GT-1, GT-2, GT-3, GT-4 | yes | n/a | yes | HIGH | yes | none" through "C7 | C5, C6, C4 | yes | n/a | yes | MEDIUM | yes | none" — all seven rows read `Form conforming? = yes`, `Rule applied = n/a`, `Dependency clean? = yes`.
Band: **Rigorous**
Justification: every chain carries a genuine intermediate (verified by the scan's "yes" conformance across all seven rows, meaning no chain was scored against a rule it could not satisfy); each chain has exactly one derivation chain in section 4 with no redundant restatement; the Abandoned Reasoning section documents two dead ends with the specific What-was-tried/Why-abandoned/What-it-ruled-out structure (not a vague reason); no analogy is used as direct evidence (the one place a historical comparison is used — GT-6?/GT-7? — is grounded in named, flagged ground truths, not offered as standalone justification); every chain step that introduced a new assumption (C1 hop 2, C5 hop 1) declares it inline via `[Assumes: A-12]` / `[Assumes: A-13]`, confirmed by the Assumption Audit scan; and every hop recomputes as shown in the Adversarial pass's Recompute section above.

**Criterion 5: Validate**
Quoted span (Adversarial pass record): "Cluster 2 — Liquidity lock-in / payment-shock risk...Disposition: plan change — this cluster is the reason chain C7 recommends 85/15 rather than 100/0..."
Band: **Rigorous**
Justification: every chain's confidence line names its specific downgrade cause (GT-6?/GT-7? for C3/C4; the locked-weighting judgment call for C5; inherited caps for C6/C7), no chain consuming a `?`-marked input is rated HIGH, every chain is rated no higher than the lowest-rated chain its head cites (C4/C5/C6/C7 all correctly capped at MEDIUM by their MEDIUM-or-lower inputs), and the section 6 Confidence rating (MEDIUM) matches its weakest contributing chain (C7, MEDIUM). The adversarial pass (pre-mortem, since the conclusion is a plan) ran in full: Recompute, Sensitivity, Rival, a past-tense Premise, an unfiltered multi-viewpoint Causes list, Clusters each citing the chain IDs they bear on, and a named Disposition per cluster (two plan changes — Clusters 2 and 5 — and three explicitly accepted, bounded risks — Clusters 1, 3, 4), plus a stated Falsification condition.

**Criterion 6: Conclusion-to-Ground-Truth Traceability**
Quoted span (self-audit scan, claim-inventory table): "**Pre-check:** head C1 (HIGH)... | bold lead-in | yes | §6 pre-check line is itself a claim under R11, discharged by the chains its own head names | C1, C2, C3, C4, C5, C6, C7" and all four other section-6 rows, each citing a chain.
Band: **Rigorous**
Justification: all five section-6 constructs (Recommended approach, Key insight, Trade-offs acknowledged, Pre-check, Confidence) trace to specific named chains per the claim-inventory table, with zero rows reading "none — untraced"; section 6 introduces no new claim absent from section 4 (the 85/15 split figure itself is chain C7's own hop 4, not invented in section 6); and the Key Insight states a non-obvious finding (that the usual "stocks beat mortgage rates long-run" intuition compares the wrong after-tax, wrong-horizon numbers) rather than restating the Recommended approach.

**Gate result:** cleared · passes: 1 · Fix/Repeat fired: no
## Structured summary (process output)

```json
{
  "schema_version": 1,
  "run_mode": "full-composer",
  "assumptions": [
    {"id": "A-1", "type": "current constraint", "verdict": "Accept"},
    {"id": "A-2", "type": "current constraint", "verdict": "Accept"},
    {"id": "A-3", "type": "current constraint", "verdict": "Accept"},
    {"id": "A-4", "type": "physical law", "verdict": "Accept"},
    {"id": "A-5", "type": "current constraint", "verdict": "Accept"},
    {"id": "A-6", "type": "untested belief", "verdict": "Challenge"},
    {"id": "A-7", "type": "untested belief", "verdict": "Challenge"},
    {"id": "A-8", "type": "convention", "verdict": "Challenge"},
    {"id": "A-9", "type": "current constraint", "verdict": "Accept"},
    {"id": "A-10", "type": "untested belief", "verdict": "Challenge"},
    {"id": "A-11", "type": "untested belief", "verdict": "Challenge"},
    {"id": "A-12", "type": "convention", "verdict": "Challenge"},
    {"id": "A-13", "type": "untested belief", "verdict": "Challenge"}
  ],
  "ground_truths": [
    {"id": "GT-1", "read_at_source": true},
    {"id": "GT-2", "read_at_source": true},
    {"id": "GT-3", "read_at_source": true},
    {"id": "GT-4", "read_at_source": true},
    {"id": "GT-5", "read_at_source": true},
    {"id": "GT-6", "read_at_source": false},
    {"id": "GT-7", "read_at_source": false},
    {"id": "GT-8", "read_at_source": false}
  ],
  "chains": [
    {"id": "C1", "confidence": "HIGH", "rests_on": ["GT-1", "GT-2", "GT-3", "GT-4"]},
    {"id": "C2", "confidence": "HIGH", "rests_on": ["GT-3", "C1"]},
    {"id": "C3", "confidence": "MEDIUM", "rests_on": ["GT-5", "GT-6?", "GT-7?", "GT-8?", "GT-2"]},
    {"id": "C4", "confidence": "MEDIUM", "rests_on": ["C2", "C3", "GT-5", "GT-6?"]},
    {"id": "C5", "confidence": "MEDIUM", "rests_on": ["C2", "C3", "C4", "GT-2"]},
    {"id": "C6", "confidence": "MEDIUM", "rests_on": ["C5", "GT-1"]},
    {"id": "C7", "confidence": "MEDIUM", "rests_on": ["C5", "C6", "C4"]}
  ],
  "dead_ends": [
    "Just compare the 6.25% mortgage rate to the ~10% historical stock market average and invest, since 10% > 6.25%",
    "Treat \"sell the investment at year 10\" and \"continue holding it\" as requiring two separate analyses"
  ],
  "techniques": {
    "applied": ["theoretical-limit", "estimate", "trade-off", "second-order", "pre-mortem"],
    "not_applied": [
      {"technique": "five-whys", "phase": 3, "reason": "the ground truths needed here (the amortization identity, the household's own loan/tax facts) are already irreducible formulas or first-hand facts; no compound claim required a reduce-to-primitives drill"},
      {"technique": "fishbone", "phase": 2, "reason": "the assumption space was directly enumerable from the two options' own structure; no multi-causal breadth-first brainstorm was needed to surface candidate assumptions"},
      {"technique": "inversion", "phase": 5, "reason": "the Phase 5 conclusion is a plan/recommendation (an allocation), not a bare claim, so the decision rule routes the adversarial pass to pre-mortem instead of inversion"}
    ]
  },
  "gate": {
    "passes": [
      {
        "bands": ["Rigorous", "Rigorous", "Rigorous", "Rigorous", "Rigorous", "Rigorous"],
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
    "recommendation": "Allocate approximately 85% of the $60,000 ($51,000) to an extra one-time mortgage principal payment, and approximately 15% ($9,000) to the taxable broad-market index fund (chain C7). This captures essentially all of the guaranteed, tax-free, after-tax-return advantage of paying down the mortgage (chains C1, C2) and nearly all of the multi-criterion trade-off's weighted edge (chain C5), while retaining a small liquid position as insurance against the payment-shock risk the second-order analysis surfaced (chain C6).",
    "confidence": "MEDIUM",
    "rests_on": ["C1", "C2", "C3", "C4", "C5", "C6", "C7"]
  }
}
```
