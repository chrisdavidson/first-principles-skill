**Disclosed:** One re-entry edge fired: the Self-Audit Gate's Fix/Repeat loop. Its trigger was Criterion 3 scoring Hand-wavy on the first pass, because the read-at-source ground truths (GT-6, GT-7, GT-9, GT-10) fed only MEDIUM chains. The fix added chain C6 (HIGH, built only from read-at-source ground truths) and cited it in §6's trade-offs, and the gate cleared on the re-score.

## Answer

**Recommendation:** Apply the full $60,000 to mortgage principal (Option A). First confirm there is no prepayment penalty and that the payment is applied principal-only, and open an undrawn HELOC as a backstop (chain C5).

**Band (from §6):** MEDIUM (chain C5)

**Would change it:** Checking the mortgage statement and tax return would leave the return forecast as the only open input (chain C5). The recommendation itself would reverse if the household starts itemising, refinances at a much lower rate, both prefers risk and expects historical-average returns, or needs liquidity beyond the reserve (chain C1, chain C5).
## 1. Problem Essence

**Core problem:** Which deployment of a surplus $60,000 — prepaying a 6.25% fixed-rate mortgage, investing in a taxable broad-market index fund, or some split or alternative — leaves the household in the best position at year 10, once both uses are put on the same after-tax, nominal, risk-stated basis?

**Success criteria:**

1. Both options' 10-year outcomes are stated in the same units (nominal dollars of net worth at year 10, after all taxes the household would owe), with every figure shown and recomputed independently.
2. The comparison states each return's basis (nominal or real, before or after tax, what scope it covers) before comparing, and puts both on one basis.
3. The break-even market return at which the two options tie is derived, with and without selling at year 10.
4. The difference in *risk* between the two outcomes is stated explicitly, not folded silently into an expected-value figure.
5. A split of the $60,000 and keeping it in cash or Treasuries are tested as options, not only A and B.
6. The answer names what evidence or change in circumstances would reverse it.

Basis note: the mortgage rate is a nominal, after-tax rate (a 0% interest shield means the pre-tax and after-tax costs are the same). Equity returns are quoted nominal and pre-tax, so §4 converts them to nominal after-tax before comparing. Inflation affects both options equally and is therefore left out of the comparison. It enters only as a building block of the equity-return estimate (C3).

## 2. Assumptions Table

| Assumption | Type | Treatment | Verdict | Verification |
|------------|------|-----------|---------|--------------|
| A-1: The stated mortgage figures are accurate — $240,000 balance, 6.25% fixed, 324 months left — and the stated "APR" equals the note rate (APR can include fees and run slightly above the note rate) | untested belief | Verify or flag | Accept — used as the problem's givens, carried as GT-1? | unverified — flagged; check the mortgage statement for note rate, principal balance and maturity date |
| A-2: The marginal mortgage-interest tax shield is 0% for the whole horizon | current constraint | Record expiry | Accept — expires if itemised deductions come to exceed the standard deduction (a change in deduction law, state/local tax caps, or charitable giving); prepaying then gives up a small shield, which lowers A's after-tax return below 6.25% on that margin | unverified — flagged (GT-2?) |
| A-3: The marginal rates of 28% ordinary and 18% on long-term gains and qualified dividends hold for 10 years | current constraint | Record expiry | Accept — expires on a change in tax law or in household income bracket; a higher gains rate raises B's break-even | unverified — flagged (GT-3?) |
| A-4: The loan carries no prepayment penalty, and the servicer applies the $60,000 to principal rather than as advance payments | untested belief | Verify or flag | Challenge — surfaced by inversion; must be verified in the note and with the servicer before acting; made a plan step in §6 | unverified — flagged |
| A-5: After a prepayment the monthly payment stays at $1,535.24 and the term shortens (no recast) | convention | Challenge | Accept — chosen as the comparison basis because it keeps the household's monthly cash flows identical under A and B, so the only difference is the $60,000. A recast would lower the payment, and the freed cash would then need its own investment assumption | Basis choice stated in C1 |
| A-6: The loan is not refinanced or sold within 10 years | untested belief | Verify or flag | Challenge — surfaced by inversion; if rates fall and the household refinances, the prepaid dollars earn the new, lower rate from then on (priced in C1's confidence line: refinancing at 5% in year 3 cuts A to $102,579) | unverified — flagged; sensitivity priced |
| A-7: Expected nominal equity return ≈ dividend yield + net buyback yield + real earnings growth + inflation ± change in valuation | convention | Challenge | Accept — used to bracket the return, not to forecast it; the identity holds by construction, but its forward inputs are uncertain | Building-block decomposition (estimate procedure, C3) |
| A-8: Real earnings growth 1.0–2.5%, inflation 2.0–3.5%, net buyback 0.25–1.25%, valuation change −1.5 to +1.0 pp a year over 10 years | untested belief | Verify or flag | Accept — the only available input for a forward bracket, carried as GT-8? | unverified — flagged; no source can verify a forecast |
| A-9: All index-fund distributions are qualified dividends taxed at 18%, with no capital-gain distributions | untested belief | Verify or flag | Accept — broad-market index funds seldom distribute gains; any that do would raise B's tax drag, which strengthens A | unverified — flagged; minor and one-directional |
| A-10: The right terminal basis for B is sale at year 10 | convention | Challenge | Challenge — a household that never sells defers the gains tax (and may never pay it if the cost basis is stepped up at death), so both the liquidated and the held break-evens are reported (C2) | Both bases computed |
| A-11: The 1928–2025 average S&P 500 return (10.02% geometric) predicts the next 10 years | convention | Challenge | Discard — as direct evidence: this reasons by analogy to a different starting yield and valuation; it is kept only as a rival scenario (§5, C5) | GT-9 |
| A-12: The funded six-month reserve covers liquidity needs, so money locked in home equity is acceptable | untested belief | Verify or flag | Accept — user-stated, carried as GT-4?; it is the premise that makes A's illiquidity tolerable | unverified — flagged |
| A-13: The household values a fixed outcome over an uncertain one with a similar or slightly higher mean (sets the certainty weight in the trade-off) | untested belief | Verify or flag | Challenge — this is a preference, not a fact; the trade-off reports what happens when it is reversed (C5 flip test) | unverified — flagged; only the household can supply it |
| A-14: The house's price risk is the same under both options, so it drops out of the comparison | physical law | Accept as a ground-truth candidate | Accept — an accounting identity: the household owns the same house under A and B, and prepaying changes only the split of its value between lender and owner | Identity, stated in C5 extension |
| A-15: The 10-year Treasury yield is the right riskless nominal benchmark for a 10-year horizon | convention | Challenge | Accept — it is the riskless nominal yield matching the horizon (held to maturity, apart from reinvesting coupons); the comparison does not depend on the tax treatment, because A wins even against an untaxed Treasury | GT-7 |
| A-16: Under B, all dividends are reinvested and nothing is withdrawn for 10 years | untested belief | Verify or flag | Accept — surfaced by the Assumption Audit; it is the like-for-like counterpart of A leaving the prepaid equity untouched | unverified — flagged; a symmetric basis choice |
| A-17: The index fund's running costs are negligible (an expense ratio of 0.05% or less a year) and are left out | untested belief | Verify or flag | Accept — surfaced by the Assumption Audit; any fee adds roughly one-for-one to B's break-even return (C2), so leaving it out favours B, which is the conservative direction for a recommendation of A | unverified — flagged; one-directional |

## 3. Ground Truths

- **GT-1?** The mortgage balance is $240,000 at a 6.25% fixed rate, with 324 monthly payments remaining — unverified: user-stated, no source document cited. **Phase 3 failure record:** no source exists to open (the user's own statement); verify against the mortgage statement.
- **GT-2?** The household's marginal mortgage-interest tax shield is 0%, because the standard deduction exceeds would-be Schedule A deductions — unverified: user-stated. **Phase 3 failure record:** no source to open; verify against the most recent tax return.
- **GT-3?** The household's marginal tax rates on taxable-account returns are 28% on ordinary income and 18% on long-term capital gains and qualified dividends — unverified: user-stated. **Phase 3 failure record:** no source to open; verify against the tax return and state schedule.
- **GT-4?** A six-month emergency reserve is already funded separately; the $60,000 is surplus to it — unverified: user-stated. **Phase 3 failure record:** no source to open.
- **GT-5** Mortgage arithmetic identities. Monthly rate i = note rate / 12. Level payment P = B·i / (1 − (1+i)^−n). Balance recursion b(t+1) = b(t)·(1+i) − P. It follows that two balances under the same payment differ by Δ·(1+i)^t after t months — source: mathematical definition; provenance: derived in this document and recomputed two ways (iterative recursion, and the closed form b(t) = B(1+i)^t − P((1+i)^t − 1)/i), which agree to the cent (C1). This is a definition that bottoms out the irreducibility test, not an empirical claim.
- **GT-6** The S&P 500 dividend yield is 1.06% as of the 30 Sep 2026 close — source: multpl.com, "S&P 500 Dividend Yield"; read-at-source: page header quoted as "Current Yield: 1.06%", dated "4:00 PM EDT, Wed Sep 30".
- **GT-7** The 10-year US Treasury yield is 5.29% as of 30 Sep 2026 — source: multpl.com, "10 Year Treasury Rate"; read-at-source: page header quoted as "5.29%", dated "Wed Sep 30, 2026".
- **GT-8?** Forward building-block ranges for the next 10 years: real earnings growth 1.0–2.5% (central 2.0%), inflation 2.0–3.5% (central 2.75%), net buyback yield 0.25–1.25% (central 0.75%), valuation change −1.5 to +1.0 pp a year (central 0) — unverified: these are forecasts, and no source can verify a future value. **Phase 3 failure record:** no source can verify the claim (it is a forecast); the bracket's width is how this is disclosed.
- **GT-9** $100 invested in the S&P 500 (dividends included) at the start of 1928 grew to $1,157,598.95 by the end of 2025, and $100 in 10-year Treasury bonds grew to $7,752.88 — source: A. Damodaran, NYU Stern, "Historical Returns on Stocks, Bonds and Bills" (histretSP); read-at-source: annual table, cumulative "value of $100" columns, 2025 row. Derived: the geometric annual rate is (11,575.99)^(1/98) − 1 = 10.02% for stocks and (77.5288)^(1/98) − 1 = 4.54% for bonds.
- **GT-10** The S&P 500 cumulative value fell from $156,658.05 (end 1999) to $142,344.87 (end 2009), a 10-year total return of 142,344.87 / 156,658.05 − 1 = −9.14%. Single-year returns were −43.84% in 1931 and −36.55% in 2008 — source: Damodaran histretSP; read-at-source: annual table, 1999, 2009, 1931 and 2008 rows.

Irreducibility (reduce-to-primitives mode), applied to the compound claim "prepaying earns a riskless 6.25% after tax". Its constituents are:

- the interest accrual rule, GT-5 (a definition — verified);
- the 0% shield, GT-2? (assumed);
- the payment staying fixed, A-5 (a basis choice, stated);
- no penalty and no refinance, A-4 and A-6 (assumed).

One branch rests on an assumption, so the parent claim is flagged and its chain C1 carries a `?` input.

**Provenance summary:**

```text
?-marked: GT-1?, GT-2?, GT-3?, GT-4?, GT-8? (5 of 10)
Read-at-source: GT-6 — multpl.com S&P 500 dividend yield page header "Current Yield: 1.06%"; GT-7 — multpl.com 10-year Treasury page header "5.29%"; GT-9 — Damodaran histretSP 2025 row, cumulative $100 columns; GT-10 — Damodaran histretSP 1999/2009/1931/2008 rows
Derived-in-document: GT-5 — mathematical identity, two independent computations agree (C1)
```

Unread remainder: none. The `?` on GT-1? to GT-4? cannot be removed by reading a source, because none was cited. The `?` on GT-8? cannot be removed by any reading, because it is a forecast.

## 4. Derivation Chains

Every figure below was computed twice. First by month-by-month iteration. Then again by closed-form expressions, independently of the chain text. The two agree to the cent, and the recomputed values are listed in the adversarial pass record (appendix).

### Conclusion C1: Option A turns $60,000 into $111,913.09 of extra net worth at year 10, a fixed after-tax nominal 6.25% (6.432% effective annual)

```text
GT-1? (balance $240,000, 6.25% fixed, 324 months) + GT-2? (0% interest shield) + GT-5 (amortization identities)
→ the monthly rate is 0.0625 / 12 = 0.00520833, and the level payment is 240,000 × 0.00520833 / (1 − 1.00520833^−324) = $1,535.24
→ with that payment unchanged under both options, the two balances differ by 60,000 × 1.00520833^t after t months *[Assumes: A-5]*
→ 1.00520833^120 = 1.865218, so the year-10 balance gap is 60,000 × 1.865218 = $111,913.09
→ the balances recompute independently as $192,615.95 without prepayment and $80,702.86 with it, and 192,615.95 − 80,702.86 = $111,913.09
→ the prepaid loan runs −ln(1 − 180,000 × 0.00520833 / 1,535.24) / ln(1.00520833) = 181.58 months, so it pays off in month 182, after the horizon, and no payment is freed within 10 years
→ with a 0% shield, the $60,000 compounds at 6.25% APR monthly after tax, an effective annual rate of 1.00520833^12 − 1 = 6.432% *[Assumes: A-4]* *[Assumes: A-6]*
→ Option A delivers $111,913.09 of extra net worth at year 10, fixed by contract rather than by markets
```

**Pre-check:** head GT-1?, GT-2?, GT-5 · ?-marked: GT-1?, GT-2? · lowest cited: none · Inputs ceiling: MEDIUM
**Confidence:** MEDIUM — the Inputs axis is short. GT-1? and GT-2? are user-stated: checking the note rate, balance and maturity on the mortgage statement, and the standard deduction against Schedule A on the latest return, would remove them as causes of the downgrade. The Inference axis is priced. A-4 (no penalty, payment applied to principal) can be checked with the servicer before acting, and is a §6 plan step. A-6 (no refinance) is priced: refinancing to 5% in year 3 would cut A to 60,000 × 1.00520833^36 × 1.00416667^84 = $102,578.75, and the rest of the analysis is tested against that lower figure (C5). A-5 is a basis choice, not a factual premise. Rivals: rival not applicable — the endpoint is an arithmetic identity on the stated basis; the recast basis is recorded in §5.

### Conclusion C2: Option B ties Option A only if the index fund earns at least 6.62% a year gross (held) or 7.52% (sold at year 10)

```text
C1 (A = $111,913.09 at year 10) + GT-3? (18% on qualified dividends and long-term gains) + GT-6 (S&P 500 yield 1.06%)
→ the annual dividend-tax drag is 0.18 × 1.06% = 0.191 percentage points, so B's pre-sale value is 60,000 × (1 + g − 0.00191)^10 *[Assumes: A-9]* *[Assumes: A-16]* *[Assumes: A-17]*
→ held unsold, B equals C1 when 1 + g − 0.00191 = 1.865218^(1/10) = 1.064322, so g = 6.432% + 0.191% = 6.623%
→ sold at year 10, B pays 18% on the gain above its basis (60,000 plus reinvested after-tax dividends) *[Assumes: A-10]* *[Assumes: A-3]*
→ solving for the sold-at-year-10 break-even gives g = 7.519%, which checks as 7.52% → $111,920.44 against $111,913.09
→ Option B must earn a gross nominal total return of at least 6.62% a year if held, or 7.52% if sold at year 10, just to match A
```

**Pre-check:** head C1 (MEDIUM), GT-3?, GT-6 · ?-marked: GT-3? · lowest cited: MEDIUM · Inputs ceiling: MEDIUM
**Confidence:** MEDIUM — the Inputs axis is short. C1 is MEDIUM, and its own line explains why. GT-3? is user-stated: confirming the 18% combined rate on qualified dividends and long-term gains from the return would remove it. The Inference axis is priced. A-9 and A-17 can only move the break-even up (more tax or fees), which would strengthen A. A-10 is resolved by reporting both bases. A-16 is a symmetric basis choice. Rivals: rival not applicable — the endpoint is a solved equation, and nothing competes with its value.

### Conclusion C3: The forward equity-return bracket [2.81%, 6.56%, 9.31%] straddles the break-even, so B's expected advantage over A is not established

```text
GT-6 (yield 1.06%) + GT-8? (growth, inflation, buyback and valuation ranges) + C2 (break-even 6.62% held, 7.52% sold)
→ the nominal expected return decomposes as dividend yield + net buyback + real earnings growth + inflation + valuation change *[Assumes: A-7]*
→ central 1.06 + 0.75 + 2.00 + 2.75 + 0 = 6.56%, low 1.06 + 0.25 + 1.00 + 2.00 − 1.50 = 2.81%, high 1.06 + 1.25 + 2.50 + 3.50 + 1.00 = 9.31%
→ the after-tax value sold at year 10 is $75,573.89 at the low end, $103,286.13 at the central estimate and $129,988.67 at the high end
→ against A's $111,913.09 that is −$36,339.20, −$8,626.96 and +$18,075.58
→ the central 6.56% lies below both break-evens, while the high end lies above them, so the bracket straddles the decision threshold
→ on the available evidence the expected-value comparison does not establish that B beats A, and the central estimate favours A
```

**Pre-check:** head GT-6, GT-8?, C2 (MEDIUM) · ?-marked: GT-8? · lowest cited: MEDIUM · Inputs ceiling: MEDIUM
**Confidence:** MEDIUM — the Inputs axis is short. GT-8? is a forecast: no reading can verify it, but the bracket bounds it. It would stop being a cause of the downgrade only with ten years of realised returns, so it is disclosed rather than closed. C2 is MEDIUM, explained on its own line. The Inference axis is priced: A-7 is an identity, and only its inputs are uncertain. Rivals: the rival "B wins on the 1928–2025 average" is ruled out as direct evidence in §5 (Dead End: Historical-average forecast). It is carried forward as a scenario in C5.

### Conclusion C4: Option A is the highest-yielding riskless use of the money, so choosing B is purely a bet on an after-tax equity premium above 6.43%

```text
GT-7 (10-year Treasury 5.29%) + C1 (riskless 6.432% effective, untaxed) + GT-10 (2000–2009 S&P 500 total return −9.14%) + GT-3? (28% ordinary rate)
→ the riskless nominal 10-year yield available, 5.29%, is below 6.25% even before any tax *[Assumes: A-15]*
→ after 28% tax a Treasury yields 5.29 × 0.72 = 3.809%, growing $60,000 to 60,000 × 1.03809^10 = $87,195.28
→ A beats that riskless alternative by 111,913.09 − 87,195.28 = $24,717.81 at year 10
→ any advantage B has over A must therefore come from an equity risk premium above a 6.432% after-tax riskless hurdle
→ a full decade of negative equity total return has occurred, so $60,000 in B could be worth 60,000 × 0.908636 = $54,518.06 pre-tax at year 10
→ A is the riskless benchmark B has to beat, and choosing B means accepting a possible loss of principal for a premium C3 cannot show is positive
```

**Pre-check:** head GT-7, C1 (MEDIUM), GT-10, GT-3? · ?-marked: GT-3? · lowest cited: MEDIUM · Inputs ceiling: MEDIUM
**Confidence:** MEDIUM — the Inputs axis is short. C1 is MEDIUM, explained on its own line. GT-3? affects only the Treasury figure of $87,195.28, and the third hop holds even at a 0% tax rate (5.29% < 6.25%), so confirming it would change a magnitude, not the ordering. The Inference axis is priced: A-15 is satisfied by matching the benchmark's maturity to the horizon. Rivals: the rival "a state-tax-exempt Treasury closes the gap" is ruled out by GT-7 in §5.

### Conclusion C5: Recommend Option A (apply the $60,000 to principal), with the second-order effects below

```text
C1 (A fixed at $111,913.09) + C3 (B central $103,286.13, bracket straddles) + C4 (A dominates riskless options) + GT-4? (reserve funded)
→ the weighted totals are A = 47 > keep in Treasuries = 37 > 30/30 split = 36 > B = 30, driven by certainty (×4) and expected value (×4) *[Assumes: A-13]* *[Assumes: A-12]*
→ even scoring B's expected value at 5, on the discarded 10.02% historical rate ($137,905 after tax), leaves B = 38 below A = 47
→ recommend Option A, after confirming no prepayment penalty and principal-only application with the servicer
→[2nd] (actor: household, immediate) the $60,000 becomes home equity reachable only by HELOC, refinance or sale, with the funded reserve covering short-term needs
→[2nd] (actor: household, backstop) an undrawn HELOC opened before prepaying, while income is intact, restores access to that equity in an emergency
→[2nd] (time: years 0–10) the monthly payment stays $1,535.24, so A gives no cash-flow relief inside the horizon
→[3rd] (time: years 15.2–27) payments of $1,535.24 stop after month 182, freeing 324 − 182 = 142 monthly payments
→[3rd] (time: life of loan) total interest falls from $257,416.67 to $98,773.59, a saving of $158,643.09
→[2nd] (actor: servicer) a $60,000 cheque recorded as advance payments rather than principal would defeat the plan, so it is sent marked principal-only and checked on the next statement
→[2nd] (actor: rate market) if rates fall, a refinance would reprice the prepaid dollars at the new rate, which C1 priced at $102,578.75 for 5% in year 3
→[3rd] (time: long run) the share of net worth held in one illiquid asset rises, while house-price risk itself is unchanged because the house is owned under both options *[Assumes: A-14]*
```

**Pre-check:** head C1 (MEDIUM), C3 (MEDIUM), C4 (MEDIUM), GT-4? · ?-marked: GT-4? · lowest cited: MEDIUM · Inputs ceiling: MEDIUM
**Confidence:** MEDIUM — the Inputs axis is short. C1, C3 and C4 are MEDIUM, each explained on its own line. GT-4? is user-stated: confirming that the reserve is held separately and covers six months of spending would remove it. The Inference axis is priced. A-13 (preference for certainty): with the certainty weight reversed from 4 to 1, A scores 32 against B's 27 at the central return, so A still wins. B wins (35 to 32) only if both the preference is reversed *and* returns follow the discarded historical average. A-12 is GT-4? itself. The refinance case ($102,578.75) is roughly level with B's central $103,286.13 rather than clearly above it, so it does not reverse the ranking on certainty-weighted criteria. Rivals: B is ruled out in §5 (Dead End: Historical-average forecast; Dead End: 30/30 split), with the ruling-out input C3 itself suffixed. No second-order effect contradicts a ground truth. Checked against the success criteria: the liquidity effect works against flexibility, and that cost is accepted in §6.

### Conclusion C6: Option B's 10-year outcome has no floor at its $60,000 starting value, whereas both riskless alternatives have contractual returns

```text
GT-10 (2000–2009 S&P 500 total return −9.14%) + GT-9 (1928–2025 geometric 10.02%) + GT-6 (yield 1.06%) + GT-7 (10-year Treasury 5.29%)
→ the S&P 500 lost 9.14% in total over 2000–2009 despite averaging 10.02% a year across 98 years, so 10-year equity outcomes range from below zero to well above the mean
→ a 10-year equity holding therefore has no floor at its starting value
→ today's 1.06% dividend yield supplies only 1.06 points of any forward return, and the rest depends on growth and valuation, which no contract sets
→ by contrast, a 10-year Treasury bought at 5.29% and held to maturity returns that nominal yield by contract, apart from reinvesting its coupons
→ the index fund is the only risky leg of this choice, and the riskless legs set the hurdle it must clear
```

**Pre-check:** head GT-10, GT-9, GT-6, GT-7 · ?-marked: none · lowest cited: none · Inputs ceiling: HIGH
**Confidence:** HIGH — Inputs: every head identifier is read at source (Damodaran histretSP 1999/2009 and 2025 rows; multpl.com page headers). Inference: every hop follows by deduction from those figures or by the definition of yield to maturity. Rivals: the strongest rival, "2000–2009 was an outlier, so equities effectively have a 10-year floor", is ruled out by GT-10 itself. One observed negative decade is enough to show there is no floor, and the endpoint claims nothing about how likely a loss is.

## 5. Abandoned Reasoning

### Dead End: Historical-average forecast (pick B because stocks returned 10% a year)

**What was tried:** Using the 1928–2025 geometric S&P 500 return of 10.02% (GT-9) as B's expected return. That gives $137,905 after tax at year 10, $25,992 above A.

**Why abandoned:** This reasons by analogy (A-11, discarded). The historical figure came from a starting dividend yield and valuation unlike today's 1.06% yield (GT-6). The building-block bracket in C3 puts the central forward return at 6.56%, below both break-evens in C2. Even granting the 10.02% figure, the trade-off at the locked weights still ranks A first (38 < 47, C5).

**What it ruled out:** "Stocks beat mortgages over the long run" as a sufficient argument for B. It is kept only as the upside scenario.

### Dead End: Recast basis (prepay, then lower the monthly payment)

**What was tried:** Valuing A with the payment re-amortised over the remaining 324 months, which frees monthly cash.

**Why abandoned:** A recast creates a stream of freed cash whose use would need a third investment assumption. That breaks the like-for-like comparison A-5 sets up (identical monthly outflows under A and B). It changes how A's benefit is delivered (monthly cash instead of a lower balance), not how large it is at the 6.25% rate.

**What it ruled out:** The idea that the choice between term-shortening and recasting changes which option wins. It changes only how A's benefit arrives.

### Dead End: State-tax-exempt Treasury closes the gap

**What was tried:** A rival to C4: Treasury interest is exempt from state tax, so the riskless alternative might come close to A.

**Why abandoned:** Even fully untaxed, the 10-year Treasury yields 5.29% (GT-7), below the 6.25% A earns after tax. The tax treatment cannot reverse the ordering.

**What it ruled out:** Any riskless security at today's yields as a better use than prepayment.

### Dead End: 30/30 split as the best of both

**What was tried:** The composite option, $30,000 to principal and $30,000 to the index fund. It is worth (111,913.09 + 103,286.13) / 2 = $107,599.61 at the central estimate.

**Why abandoned:** A split's outcome is a straight average of its two halves, so at the central estimate it is beaten by A and only beats A if B does. It halves the downside but also halves the certainty. In the trade-off it scored 36 against A's 47, losing on certainty without gaining enough liquidity to compensate.

**What it ruled out:** Splitting as a default hedge. It would be right only for a household that wants some liquidity outside home equity, a need GT-4? says is already met.

## 6. Conclusion

**Recommended approach:** Apply the full $60,000 to mortgage principal (Option A). Before doing so, confirm in the note and with the servicer that there is no prepayment penalty and that the payment will be applied principal-only, and open an undrawn HELOC as a liquidity backstop. Check the next statement afterwards (chain C5).

**Key insight:** Once both options are on the same after-tax nominal basis, A is a riskless 6.432% effective return (chain C1). That is above every riskless alternative, including an untaxed 5.29% Treasury (chain C4). So B has to beat a 6.62% (held) or 7.52% (sold) gross return just to tie (chain C2), and today's 1.06% dividend yield puts the central forward estimate at 6.56%, below both thresholds (chain C3).

**Trade-offs acknowledged:** A gives up liquidity, since the $60,000 becomes home equity, and gives no monthly cash-flow relief until the loan ends at month 182. It also gives up the upside B would deliver at returns above 7.52%, up to about +$18,076 at the bracket's high end (chain C3, chain C5). In exchange it removes the chance, which B carries, of ending the decade below the $60,000 start (chain C6).

**What would reverse it:** the household starting to itemise (A-2), a refinance at a much lower rate (priced at $102,578.75 for 5% in year 3), a reversed preference combined with returns near the historical average, or a need for liquidity beyond the reserve (chain C1, chain C5).

**Pre-check:** head C1 (MEDIUM), C2 (MEDIUM), C3 (MEDIUM), C4 (MEDIUM), C5 (MEDIUM), C6 (HIGH), GT-4? · ?-marked: GT-4? · lowest cited: MEDIUM · Inputs ceiling: MEDIUM
**Confidence:** MEDIUM — C6 is HIGH and needs no caveat. C1, C2, C3, C4 and C5 are each MEDIUM, explained on their own lines, all because the user-stated figures (GT-1? to GT-4?) and the return forecast (GT-8?) cannot be read at source. GT-4? is also used directly: confirming that the reserve is separate and adequate would remove it. Checking the household's own statement and tax return against GT-1? to GT-3? would leave the forecast as the only cause of the downgrade (chain C5).
## Appendix — process output

## Trade-off analysis (process output)

## Options

- **A**: apply $60,000 to principal.
- **B**: invest $60,000 in a taxable broad-market index fund.
- **S (status quo)**: keep the $60,000 in cash or 10-year Treasuries (GT-7).
- **C (composite)**: $30,000 to principal and $30,000 to the index fund.

Must-haves: none. The emergency reserve is already funded (GT-4?), so liquidity is weighed as a criterion rather than applied as a knock-out. No option is knocked out.

## Criteria & Weights

Weights were locked before any option was scored.

| Criterion | Weight | 1 means | 5 means |
|---|---|---|---|
| Expected after-tax value at year 10 | 4 | ≤ $90,000 | ≥ $120,000 (linear: $97.5k = 2, $105k = 3, $112.5k = 4) |
| Certainty of the year-10 outcome | 4 | could end below $60,000 nominal | fixed by contract |
| Liquidity of the $60,000 | 2 | reachable only by HELOC, refinance or sale | cash within days at no loss |
| Robustness to tax-law change | 1 | outcome moves directly with tax rates | unaffected by tax rates |
| Simplicity | 1 | ongoing decisions and tax reporting | one action, nothing to manage |

## Scoring

| Option | EV (×4) | Certainty (×4) | Liquidity (×2) | Tax robustness (×1) | Simplicity (×1) | Total |
|---|---|---|---|---|---|---|
| A | 4 × 4 = 16 ($111,913; C1) | 5 × 4 = 20 (contractual; C1) | 1 × 2 = 2 | 4 × 1 = 4 (only A-2 can move it) | 5 × 1 = 5 | **47** |
| S | 1 × 4 = 4 ($87,195; C4) | 4 × 4 = 16 (Treasury held to maturity; coupon reinvestment risk) | 4 × 2 = 8 (sellable; price risk) | 4 × 1 = 4 (no state tax) | 5 × 1 = 5 | **37** |
| C | 3 × 4 = 12 ($107,600 central) | 3 × 4 = 12 | 3 × 2 = 6 | 3 × 1 = 3 | 3 × 1 = 3 | **36** |
| B | 3 × 4 = 12 ($103,286 central; C3) | 1 × 4 = 4 (−9.14% decade, GT-10) | 4 × 2 = 8 (sellable at market, with tax) | 2 × 1 = 2 (GT-3?) | 4 × 1 = 4 | **30** |

Each EV score rests on GT-8? through C3, and each certainty score on GT-10 and C1. Liquidity and simplicity scores are preferences anchored to the descriptions above.

## Recommendation

A, with 47 against the runner-up S at 37. **Flip test:** no single weight change flips this result. The closest moves are EV 4 → 1 (A 35, S 34) and liquidity 2 → 5 (A 50, S 49), each leaving a gap of 1. Against B, the closest move is certainty 4 → 1 (A 32, B 27). Changing a score as well as a weight does flip it: with the certainty weight at 1 *and* B's EV scored 5 (the historical 10.02% rate), B scores 35 against A's 32. The flip test varies weights, not inputs, so it does not lift the MEDIUM cap that comes from GT-8?.

## Assumption Audit scan (process output)

| Chain | Step | Step Text (brief) | Assumption surfaced? | Added to Table? |
|---|---|---|---|---|
| C1 | 1 | monthly rate and $1,535.24 payment | no (A-1 via GT-1?) | already present |
| C1 | 2 | balances differ by 60,000 × (1+i)^t | yes — A-5 | already present |
| C1 | 3 | 1.865218 factor, gap $111,913.09 | no | — |
| C1 | 4 | balances recompute independently | no | — |
| C1 | 5 | payoff at 181.58 months | no | — |
| C1 | 6 | 6.432% effective after tax | yes — A-4, A-6 | already present |
| C1 | 7 | A fixed by contract | no | — |
| C2 | 1 | dividend-tax drag 0.191 pp | yes — A-9, A-16, A-17 | A-9 present; A-16 and A-17 added |
| C2 | 2 | held break-even 6.623% | no | — |
| C2 | 3 | 18% on gains when sold | yes — A-10, A-3 | already present |
| C2 | 4 | sold break-even 7.519% | no | — |
| C2 | 5 | B must exceed 6.62% / 7.52% | no | — |
| C3 | 1 | building-block decomposition | yes — A-7 | already present |
| C3 | 2 | 2.81 / 6.56 / 9.31% | no (A-8 via GT-8?) | already present |
| C3 | 3 | after-tax values | no | — |
| C3 | 4 | differences from A | no | — |
| C3 | 5 | bracket straddles threshold | no | — |
| C3 | 6 | EV advantage not established | no | — |
| C4 | 1 | 5.29% < 6.25% | yes — A-15 | already present |
| C4 | 2 | Treasury after tax $87,195.28 | no | — |
| C4 | 3 | A beats it by $24,717.81 | no | — |
| C4 | 4 | B's edge must be an equity premium | no | — |
| C4 | 5 | −9.14% decade → $54,518.06 | no | — |
| C4 | 6 | A is the benchmark | no | — |
| C5 | 1 | weighted totals | yes — A-13, A-12 | already present |
| C5 | 2 | B at EV 5 still 38 | no | — |
| C5 | 3 | recommend A after checks | no (A-4) | already present |
| C5 | 4 | [2nd] money becomes illiquid equity | no | — |
| C5 | 5 | [2nd] HELOC backstop opened first | no (A-12) | already present |
| C5 | 6 | [2nd] no cash-flow relief in horizon | no | — |
| C5 | 7 | [3rd] 142 payments freed | no | — |
| C5 | 8 | [3rd] $158,643.09 less interest | no | — |
| C5 | 9 | [2nd] servicer application | no (A-4) | already present |
| C5 | 10 | [2nd] refinance reprices | no (A-6) | already present |
| C5 | 11 | [3rd] concentration; house risk unchanged | yes — A-14 | already present |
| C6 | 1 | 10-year outcomes span below zero to above the mean | no | — |
| C6 | 2 | no floor at the starting value | no | — |
| C6 | 3 | 1.06% yield is the only contractual part | no | — |
| C6 | 4 | Treasury held to maturity returns its yield | yes — A-15 | already present |
| C6 | 5 | the fund is the only risky leg | no | — |

Techniques not applied:
- theoretical-limit (Phase 1) — not applicable — the question does not turn on whether any figure is a convention or a physical bound; the rates are contractual and market-given
- theoretical-limit (Phase 4) — not applicable — no conclusion needs a law-permitted ceiling
- fishbone — not applicable — the assumption space is a short, enumerable list of financial premises, not a multi-causal effect
- five-whys (causal mode) — not applicable — there is no recurring symptom to trace

## Adversarial pass (process output)

**Recompute.**

- Payment: closed form 240,000 × 0.00520833 × 1.00520833^324 / (1.00520833^324 − 1) = $1,535.2366, which matches the iterative computation.
- 1.00520833^120 = 1.8652182, and 60,000 × 1.8652182 = $111,913.09.
- Closed-form balances: $192,615.95 and $80,702.86, a difference of $111,913.09, which matches the iteration.
- Payoff: 181.58 months closed form; the iteration gives 182.
- EAR: 1.00520833^12 − 1 = 6.4322%.
- Held break-even: 1.8652182^0.1 = 1.0643218, and 6.4322% + 0.1908% = 6.623%.
- Sold break-even: bisection gives 7.519%, and the check at 7.52% gives $111,920.44.
- Bracket: g = 2.81% → pre-sale $77,702.95, basis $65,874.85, after tax $75,573.89; g = 6.56% → $111,252.60, $66,994.40, $103,286.13; g = 9.31% → $143,602.83, $67,968.63, $129,988.67. Each after-tax value lies between the basis and the pre-sale value, as it should.
- Treasury: 60,000 × 1.03809^10 = $87,195.28.
- Decade: 142,344.87 / 156,658.05 = 0.908636, and 60,000 × 0.908636 = $54,518.06.
- Refinance case: 60,000 × 1.2056 × 1.4176 = $102,578.75.
- Interest: $257,416.67 − $98,773.59 = $158,643.09.
- Historical rates: 11,575.9895^(1/98) = 1.10018; 77.5288^(1/98) = 1.04539.
- Split: (111,913.09 + 103,286.13) / 2 = $107,599.61.

Every figure recomputes, and every growth factor above 1 produces a figure above its base.

**Sensitivity.** The single ground truth whose falsity would flip the recommendation is GT-4? (the reserve is funded and separate). If it were false, liquidity would become a must-have, A would be knocked out, and S or C would win. It is `?`-marked, so a confidence caveat is applied (C5 and the §6 Confidence line) and confirming it is a plan step. The weakest link in each chain:

- C1: hop 6 (A-6, refinance), priced at $102,578.75.
- C2: hop 4 (A-10, whether the household sells at year 10), resolved by reporting both bases.
- C3: hop 2 (the GT-8? inputs).
- C4: hop 5, which rests on a single historical decade (GT-10) as evidence that a loss is possible, not as a probability.
- C5: hop 1 (A-13, preference weights).

**Rival.**

- Headline: B is better. This is ruled out in §5 (Dead End: Historical-average forecast; Dead End: 30/30 split).
- C3: the rival "historical average applies" points to the §5 Historical-average entry.
- C4: the rival "a state-exempt Treasury closes the gap" points to the §5 State-tax-exempt Treasury entry.
- C1: rival not applicable — an arithmetic identity on a stated basis; the alternative basis is in §5 (Recast).
- C2: rival not applicable — a solved equation.
- C6: the rival "2000–2009 was an outlier" is ruled out by GT-10 on C6's Confidence line.
- C5: the B rival survives only under a reversed preference *and* the discarded historical return. This is named on C5's Confidence line.

**Premise.** It is 2036, and applying the $60,000 to principal turned out to be a bad decision for this household.

**Causes** (unfiltered; viewpoints: household earner, spouse living with the result, mortgage servicer, a brokerage competitor, the household's heirs):

1. Earner: a job loss in year 3 drained the reserve, and the bank cut the HELOC just as it was needed.
2. Earner: a credit-card balance at 22% built up because the cash was locked in the house.
3. Spouse: a medical bill exceeded six months of reserve.
4. Servicer: the $60,000 was recorded as 39 advance payments, not principal, and the interest saving never happened.
5. Servicer: the note had a prepayment penalty that nobody checked.
6. Brokerage competitor: the S&P 500 returned 12% a year from 2026 to 2036, and B would have been worth about $170,000.
7. Earner: rates fell to 4% in 2028 and the loan was refinanced, so the prepaid dollars earned only 4% from then on.
8. Spouse: the household began itemising after a tax-law change, and the prepayment gave up a deduction.
9. Heirs: the house was sold at a loss in a local downturn, and the equity was gone.
10. Earner: the "6.25%" turned out to be the APR including fees, and the note rate was 6.0%.
11. Spouse: the household needed a down payment for a second property and had no liquid money.

**Clusters.**

- **K1 Liquidity trap** (causes 1, 2, 3, 11) — bears on GT-4? and C5. Costly but survivable. Tripwire: the reserve falls below four months of spending; the household checks it quarterly.
- **K2 Execution error** (causes 4, 5, 10) — bears on A-4, GT-1? and C1. Costly but survivable. Tripwire: the first statement after the payment does not show the principal reduced by $60,000; the household checks the next statement.
- **K3 Opportunity cost** (cause 6) — bears on C2 and C3. Tolerable: A still delivers its fixed $111,913, so this is regret, not loss.
- **K4 Rate and tax regime change** (causes 7, 8) — bears on C1, A-2 and A-6. Tolerable: A falls to about $102.6k, still above the Treasury alternative of $87.2k.
- **K5 House-price loss** (cause 9) — bears on A-14 and C5. Tolerable for the decision, because house-price risk is identical under A and B. Only the illiquidity is A's own, and that sits in K1.

**Disposition.**

- K1 — plan change: open (but do not draw) a HELOC *before* prepaying, while income is intact, and keep the reserve at six months.
- K2 — plan change: get written confirmation from the servicer of no penalty and principal-only application, confirm the note rate on the statement, and check the next statement.
- K3 — accepted risk. Mitigation: future surplus cash beyond the reserve can still go to an index fund, so equity exposure is not given up permanently.
- K4 — accepted risk. Mitigation: any future refinance or itemising decision compares the new rate against investment alternatives at that point.
- K5 — accepted risk. Mitigation: the HELOC from K1 plus the reserve; no change specific to A is warranted.

**Falsification.** The recommendation is false on expected value if the S&P 500's 2026–2036 gross nominal total return averages above 7.52% a year *and* the household turns out to weigh certainty low. It is false as a plan if, within the decade, the household has to borrow at more than 6.25% because the money is tied up in the house.

## §6→§4 closure ledger (process output)

```text
- "Apply the full $60,000 to mortgage principal (Option A) … open an undrawn HELOC … check the next statement" → chain C5 ✓
- "A is a riskless 6.432% effective return … above every riskless alternative … B must beat 6.62%/7.52% … central 6.56%" → chains C1, C4, C2, C3 ✓
- "A gives up liquidity … no monthly relief until month 182 … gives up upside up to about +$18,076 … removes the chance of ending below $60,000" → chains C3, C5, C6 ✓
- "What would reverse it: itemising, refinancing, reversed preference with historical returns, liquidity need" → chains C1, C5 ✓
- "Pre-check: head C1–C5 (MEDIUM), C6 (HIGH), GT-4? · Inputs ceiling MEDIUM" → chains C1, C2, C3, C4, C5, C6 ✓
- "Confidence: MEDIUM …" → chain C5 (and C1–C4 named) ✓
```

## Self-audit scan (process output)

| Chain | Chain Head (brief) | Form conforming? | Rule applied | Dependency clean? | Band | Act attempted? | Edges fired |
|---|---|---|---|---|---|---|---|
| C1 | GT-1? + GT-2? + GT-5 | unreached | hops 3–8 sit beyond the check's two-hop reach for the GT-led-hop and sentence-closing rules; checked by hand, no violation | yes | MEDIUM | no | none |
| C2 | C1 + GT-3? + GT-6 | unreached | hops 3–5 beyond the check's reach for the same two rules; checked by hand, no violation | yes | MEDIUM | yes | none |
| C3 | GT-6 + GT-8? + C2 | unreached | hops 3–6 beyond the check's reach; checked by hand, no violation | yes | MEDIUM | yes | none |
| C4 | GT-7 + C1 + GT-10 + GT-3? | unreached | hops 3–6 beyond the check's reach; checked by hand, no violation | yes | MEDIUM | yes | none |
| C5 | C1 + C3 + C4 + GT-4? | unreached | hops 3–11, including order-marked extensions, beyond the check's reach; checked by hand, no violation | yes | MEDIUM | no | none |
| C6 | GT-10 + GT-9 + GT-6 + GT-7 | unreached | hops 3–5 beyond the check's reach for the GT-led-hop and sentence-closing rules; checked by hand, no violation | yes | HIGH | yes | Fix/Repeat (added in the Criterion 3 fix) |

| §6 Span (brief) | Construct | Claim under R11? | R11 clause applied | Chain cited |
|---|---|---|---|---|
| Recommended approach: apply $60k to principal | bold lead-in | yes | a bold lead-in whose colon closes the bold span | C5 |
| Key insight: riskless 6.432% beats riskless options | bold lead-in | yes | a bold lead-in whose colon closes the bold span | C1, C4, C2, C3 |
| Trade-offs acknowledged: liquidity, upside, no floor under B | bold lead-in | yes | a bold lead-in whose colon closes the bold span | C3, C5, C6 |
| What would reverse it | bold lead-in | yes | a bold lead-in whose colon closes the bold span | C1, C5 |
| Pre-check | bold lead-in | yes | a bold lead-in whose colon closes the bold span | C1, C2, C3, C4, C5, C6 (head) |
| Confidence: MEDIUM | bold lead-in | yes | a bold lead-in whose colon closes the bold span | C5 (C1–C4 named) |

```text
Scan complete: 6 chain rows, one per section-4 chain block in order; 6 section-6 rows, one per construct in order — 6 claims under R11, 0 excluded. 0 chains malformed, 0 claims untraced.
```

## Self-Audit Gate (process output)

**Pass 1 (before re-score):** Criterion 1 Rigorous · Criterion 2 Sound · Criterion 3 Hand-wavy · Criterion 4 Rigorous · Criterion 5 Rigorous · Criterion 6 Rigorous · Gate cleared: yes · Hand-wavy cap cleared: yes

Pass 1 scored Criterion 3 Hand-wavy because several unsuffixed, reachable ground truths (GT-6, GT-7, GT-9, GT-10) fed only MEDIUM chains. The Fix/Repeat loop fired once. The fix was to add chain C6, built only from read-at-source ground truths and rated HIGH, and cite it in §6. The scan, ledger, audit and adversarial rows for C6 were then updated. The verdict blocks below are the final pass.

**Criterion 1: Identify Essence**
Quoted span: "Which deployment of a surplus $60,000 — prepaying a 6.25% fixed-rate mortgage, investing in a taxable broad-market index fund, or some split or alternative — leaves the household in the best position at year 10, once both uses are put on the same after-tax, nominal, risk-stated basis?"
Band: **Rigorous**
Justification: The statement is a single sentence specific to this problem. Each of the six success criteria is checkable against §4 and §6 (shared basis, break-even derived, risk stated, split and status quo tested, reversal conditions named). None requires the answer to be A or B.

**Criterion 2: Challenge Assumptions**
Quoted span: "| A-14: The house's price risk is the same under both options, so it drops out of the comparison | physical law | Accept as a ground-truth candidate | Accept — an accounting identity…"
Band: **Sound**
Justification: Every row uses the four-type scheme with an em-dash verdict, several are challenged (A-4, A-6, A-10, A-13) and one is discarded (A-11), and the Assumption Audit scan covers every step of C1–C6. However, the physical-law row A-14 was never promoted to the Ground Truths list as its treatment requires. That is one entry departing from the prescribed form. *Unresolved gap (caveat): it is not load-bearing for any endpoint.*

**Criterion 3: Establish Ground Truths**
Quoted span: "enumerated GT-1?, GT-2?, GT-3?, GT-4?, GT-8?; the list carries `?` on exactly those five; unsuffixed GT-6, GT-7, GT-9 and GT-10 name read-at-source locations and feed HIGH chain C6; GT-1? to GT-4? and GT-8? carry Phase 3 failure records (no source to open; forecast)"
Band: **Sound**
Justification: The enumeration matches the list, and every reachable unsuffixed ground truth now feeds a HIGH chain. GT-5 is a derived identity with no external source, and it feeds only MEDIUM chains (C1). That is a single isolated shortfall against the "feeds at least one HIGH chain" test, not a pattern.

**Criterion 4: Reason Upward**
Quoted span: "| C6 | GT-10 + GT-9 + GT-6 + GT-7 | unreached | hops 3–5 beyond the check's reach for the GT-led-hop and sentence-closing rules; checked by hand, no violation | yes | HIGH | yes |"
Band: **Rigorous**
Justification: All six chain rows have clean dependencies, and hand inspection finds no form violation at the positions the check cannot reach. Every hop recomputes, as listed in the adversarial Recompute record. §5 has four dead ends in the What-was-tried / Why-abandoned / What-it-ruled-out structure. The historical-average analogy is explicitly discarded as direct evidence (A-11).

**Criterion 5: Validate**
Quoted span: "**Confidence:** MEDIUM — the Inputs axis is short. GT-1? and GT-2? are user-stated: checking the note rate, balance and maturity on the mortgage statement, and the standard deduction against Schedule A on the latest return, would remove them as causes of the downgrade."
Band: **Rigorous**
Justification: Every MEDIUM line names its `?` inputs and cited chains with a verification path, and names which axis is short. C6 is HIGH on three clean axes, so the bands are not uniform. The §6 MEDIUM matches its weakest contributing chain. The adversarial record carries Recompute, Sensitivity, Rival, Premise, Causes, Clusters (each citing GT and Cn ids), Disposition and Falsification.

**Criterion 6: Conclusion-to-Ground-Truth Traceability**
Quoted span: "| Key insight: riskless 6.432% beats riskless options | bold lead-in | yes | a bold lead-in whose colon closes the bold span | C1, C4, C2, C3 |" and §6 Key insight "B has to beat a 6.62% (held) or 7.52% (sold) gross return just to tie (chain C2), and today's 1.06% dividend yield puts the central forward estimate at 6.56%, below both thresholds (chain C3)"
Band: **Rigorous**
Justification: All six §6 claims cite named chains in the scan, with none untraced. The Key Insight is a quantified break-even finding that "stocks beat mortgages" reasoning by analogy does not reach, not a restatement of the recommendation.

**Gate result:** cleared · passes: 2 · Fix/Repeat fired: yes

## Structured summary (process output)

```json
{
  "schema_version": 1,
  "run_mode": "full-composer",
  "assumptions": [
    {
      "id": "A-1",
      "type": "untested belief",
      "verdict": "Accept"
    },
    {
      "id": "A-2",
      "type": "current constraint",
      "verdict": "Accept"
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
      "type": "convention",
      "verdict": "Accept"
    },
    {
      "id": "A-6",
      "type": "untested belief",
      "verdict": "Challenge"
    },
    {
      "id": "A-7",
      "type": "convention",
      "verdict": "Accept"
    },
    {
      "id": "A-8",
      "type": "untested belief",
      "verdict": "Accept"
    },
    {
      "id": "A-9",
      "type": "untested belief",
      "verdict": "Accept"
    },
    {
      "id": "A-10",
      "type": "convention",
      "verdict": "Challenge"
    },
    {
      "id": "A-11",
      "type": "convention",
      "verdict": "Discard"
    },
    {
      "id": "A-12",
      "type": "untested belief",
      "verdict": "Accept"
    },
    {
      "id": "A-13",
      "type": "untested belief",
      "verdict": "Challenge"
    },
    {
      "id": "A-14",
      "type": "physical law",
      "verdict": "Accept"
    },
    {
      "id": "A-15",
      "type": "convention",
      "verdict": "Accept"
    },
    {
      "id": "A-16",
      "type": "untested belief",
      "verdict": "Accept"
    },
    {
      "id": "A-17",
      "type": "untested belief",
      "verdict": "Accept"
    }
  ],
  "ground_truths": [
    {
      "id": "GT-1",
      "read_at_source": false
    },
    {
      "id": "GT-2",
      "read_at_source": false
    },
    {
      "id": "GT-3",
      "read_at_source": false
    },
    {
      "id": "GT-4",
      "read_at_source": false
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
      "read_at_source": true
    }
  ],
  "chains": [
    {
      "id": "C1",
      "confidence": "MEDIUM",
      "rests_on": [
        "GT-1?",
        "GT-2?",
        "GT-5"
      ]
    },
    {
      "id": "C2",
      "confidence": "MEDIUM",
      "rests_on": [
        "C1",
        "GT-3?",
        "GT-6"
      ]
    },
    {
      "id": "C3",
      "confidence": "MEDIUM",
      "rests_on": [
        "GT-6",
        "GT-8?",
        "C2"
      ]
    },
    {
      "id": "C4",
      "confidence": "MEDIUM",
      "rests_on": [
        "GT-7",
        "C1",
        "GT-10",
        "GT-3?"
      ]
    },
    {
      "id": "C5",
      "confidence": "MEDIUM",
      "rests_on": [
        "C1",
        "C3",
        "C4",
        "GT-4?"
      ]
    },
    {
      "id": "C6",
      "confidence": "HIGH",
      "rests_on": [
        "GT-10",
        "GT-9",
        "GT-6",
        "GT-7"
      ]
    }
  ],
  "dead_ends": [
    "Historical-average forecast (pick B because stocks returned 10% a year)",
    "Recast basis (prepay, then lower the monthly payment)",
    "State-tax-exempt Treasury closes the gap",
    "30/30 split as the best of both"
  ],
  "techniques": {
    "applied": [
      "inversion",
      "five-whys",
      "estimate",
      "trade-off",
      "second-order",
      "pre-mortem"
    ],
    "not_applied": [
      {
        "technique": "theoretical-limit",
        "phase": 1,
        "reason": "the question does not turn on whether any figure is a convention or a physical bound; the rates are contractual and market-given"
      },
      {
        "technique": "theoretical-limit",
        "phase": 4,
        "reason": "no conclusion needs a law-permitted ceiling"
      },
      {
        "technique": "fishbone",
        "phase": 2,
        "reason": "the assumption space is a short, enumerable list of financial premises, not a multi-causal effect"
      },
      {
        "technique": "five-whys",
        "phase": 3,
        "reason": "there is no recurring symptom to trace"
      }
    ]
  },
  "gate": {
    "passes": [
      {
        "bands": [
          "Rigorous",
          "Sound",
          "Hand-wavy",
          "Rigorous",
          "Rigorous",
          "Rigorous"
        ],
        "gate_cleared": true,
        "hand_wavy_cap_cleared": true
      },
      {
        "bands": [
          "Rigorous",
          "Sound",
          "Sound",
          "Rigorous",
          "Rigorous",
          "Rigorous"
        ],
        "gate_cleared": true,
        "hand_wavy_cap_cleared": true
      }
    ],
    "fix_repeat_fired": true,
    "cleared": true
  },
  "re_entry": {
    "fired": true,
    "edges": [
      {
        "edge": "the Self-Audit Gate's Fix/Repeat loop",
        "trigger": "Criterion 3 scored Hand-wavy on the first pass because reachable read-at-source ground truths fed only MEDIUM chains."
      }
    ]
  },
  "conclusion": {
    "recommendation": "Apply the full $60,000 to mortgage principal (Option A). Before doing so, confirm in the note and with the servicer that there is no prepayment penalty and that the payment will be applied principal-only, and open an undrawn HELOC as a liquidity backstop. Check the next statement afterwards (chain C5).",
    "confidence": "MEDIUM"
  }
}
```
