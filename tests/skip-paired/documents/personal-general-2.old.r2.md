# First-Principles Analysis: Mortgage Paydown vs. Taxable Index-Fund Investment ($60,000, 10-Year Horizon)

*Prepared 2026-10-08. Market/rate figures cited below were fetched live via web search/fetch during this session and are explicitly sourced; where a figure could not be fetched at source this session, it is marked `?` and the gap is named.*

---

## 1. Problem Essence

**Core problem:** Should this household apply its full $60,000 surplus cash to pay down a 6.25% mortgage with no tax shield (a guaranteed, risk-free ~6.43% effective return), invest it in a taxable broad-market index fund (an uncertain, risk-bearing return that must clear roughly a 7.47% pretax nominal hurdle just to tie), or split it between the two over a 10-year horizon — and does today's specific valuation/rate environment, plus the household's liquidity and diversification needs, change the answer from what the raw guaranteed-rate-vs-point-estimate-CAGR arithmetic in the prompt alone would suggest?

**Success criteria:**
1. The Conclusion names a single specific allocation (a percentage or dollar split between paydown and investment) rather than leaving the choice open-ended.
2. The Conclusion's recommended split traces to a derivation chain in section 4 that weighs the guaranteed risk-free return against the risk-*adjusted* expected equity return — not just the point-estimate CAGR comparison already supplied in the prompt.
3. The Conclusion cites at least one current-market data point fetched at source this session (not a training-era average) bearing on whether today's equity starting valuation makes the "historical average" scenario a reasonable central case.
4. The Conclusion states a named, checkable sensitivity condition — a specific fact that, if false, would change the recommended split.
5. The Conclusion addresses liquidity, concentration/diversification, and at least one concrete operational risk (e.g., the "no recast" assumption) as factors distinct from the raw return comparison, per the user's explicit request.

---

## 2. Assumptions Table

*Methodological note on provenance lanes:* household-reported facts about this specific household's own situation (loan terms, cash balance, tax bracket) are treated in section 3 as **stipulated problem inputs** — given premises of the decision, not external research claims — and are not `?`-suffixed on that basis alone. Every assumption *about the world, about third-party behavior (the lender), or about this household's unstated context* is classified and challenged below using the full four-type scheme, exactly as the user requested.

| Assumption | Type | Treatment | Verdict | Verification |
|---|---|---|---|---|
| A-1: No recast — the lender will not recast the loan after the extra-principal payment, so the monthly P&I payment is unchanged | untested belief | Verify directly with the loan servicer, in writing, before remitting payment | Challenge — em-dash: lender-specific operational policy, not verifiable by this analysis; household must confirm | unverified — flagged (used in GT-2, C1, C8) |
| A-2: Household keeps the home for the full 10-year horizon (and, for C8, beyond ~year 15) rather than selling or refinancing sooner | untested belief | Verify against household's actual plans | Challenge — median U.S. homeownership tenure runs well under 10 years with wide variance; if false, the equivalence math still holds pro-rata over whatever shorter window actually occurs | unverified — flagged (used in C1 framing, C8) |
| A-3: Current tax facts (standard deduction; 28% ordinary; 18% LTCG/qualified-dividend) remain stable for 10 years | current constraint | Record expiry: holds only until the next federal/state tax-law change or a household bracket shift | Accept — expires at the next relevant tax-law change; treated as operative until then | stipulated by household; current law as understood |
| A-4: The $60,000 is genuinely surplus beyond the funded emergency reserve, and no other higher-rate debt exists that should be paid first | untested belief | Accept as stipulated; flag for household self-check | Accept — stated as the problem's premise, but a higher-APR debt elsewhere would dominate this entire analysis trivially if present | unverified — flagged |
| A-5: The loan carries no prepayment penalty and permits an unrestricted lump-sum curtailment | current constraint | Record expiry/condition: standard for most conforming post-2014 fixed loans, but confirm against this specific note | Accept — standard for conforming 30-year fixed loans; flagged as a quick confirmation item | unverified — flagged |
| A-6: Current index valuations don't matter; forward 10-year equity returns will resemble the long-run historical average (~9.5% nominal) | convention | Explicitly challenge before using as the default base case | Discard as the default base case — em-dash: contradicted by GT-10/GT-12?/GT-13?; retained only as the optimistic upper scenario, not the central case | challenged; see GT-10, GT-12?, GT-13?, chain C3 |
| A-7: Home values and the broad equity market are independent, uncorrelated risks | untested belief | Flag; note known counter-example | Challenge — em-dash: in a severe recession (2008-09) both fell together, so B's diversification benefit is somewhat overstated in a tail scenario, though the two are far from perfectly correlated in typical conditions | unverified — flagged (used in C6; pre-mortem cause 4) |
| A-8: No other household debt or leverage considerations exist beyond this one mortgage | untested belief | Accept as stipulated; flag for household self-check | Accept — stated as the problem's premise | unverified — flagged |
| A-9: The home already represents a meaningful share of total household net worth | untested belief | Flag as a material unknown; household should disclose approximate balance-sheet composition | Challenge — em-dash: essential context not given; materially affects the weight placed on the concentration-risk finding (C6) | unverified — flagged (used in C6, C9) |
| A-10: Brokerage-account liquidity is frictionless beyond LTCG tax, with no behavioral risk of panic-selling in a drawdown | convention | Explicitly challenge; behavioral-finance literature documents systematic panic-selling | Challenge — em-dash: treating B's liquidity as costlessly available ignores well-documented behavioral risk | unverified — flagged (used in pre-mortem causes 6, 8) |
| A-11: Market-implied long-run inflation expectations are approximately 2.0%-2.5% | untested belief | Verify against a current TIPS-breakeven data source | Challenge — em-dash: training-knowledge estimate, not fetched at source this session | unverified — flagged (GT-17?, used in C7) |
| A-12: Diversification (modern portfolio theory) reduces idiosyncratic risk without necessarily reducing expected return | physical law | Accept as ground-truth candidate | Accept — em-dash: established mathematical/statistical result | source: Markowitz (1952); promoted to GT-16 |
| A-13: The mortgage-balance recursion identity — extra principal paid today under an unchanged payment schedule equals a risk-free deposit compounding at the mortgage's own rate | physical law | Accept as ground-truth candidate | Accept — em-dash: survives direct derivation and independent recomputation | promoted to GT-1; recomputed in chain C1 |
| A-14: Home equity cannot be converted to cash without a new loan origination (sale, cash-out refinance, or HELOC) and the underwriting/approval that entails | untested belief | Surfaced by the end-of-Phase-4 Assumption Audit on chain C5; verify by noting every realistic access path requires some transaction and/or underwriting | Accept — em-dash: definitionally close to true for a retail mortgage; bounded even in the best case by real transaction friction | unverified — flagged (used in C5, C11) |
| A-15: Nominal equity returns partially track inflation over multi-year horizons | untested belief | Surfaced by the end-of-Phase-4 Assumption Audit on chain C7; standard but imperfect empirical regularity | Challenge — em-dash: regularity holds loosely and with lags/exceptions (e.g., 1970s stagflation briefly broke it); not fully priced here | unverified — flagged (used in C7) |

---

## 3. Ground Truths

**Provenance lanes used below:** (i) *stipulated* — a fact about this household's own private situation, given as a premise of the problem, not independently source-checkable by this analysis; (ii) *read-at-source* — this analysis opened the cited source directly and the figure quoted below was read there; (iii) `?` *reported-by-delegate / unverified* — a search-engine synthesis or training-knowledge claim this analysis did not confirm by opening the primary source this session.

- **GT-1** The mortgage-balance recursion `B_{n+1} = B_n(1+r) - Payment`, with an identical payment schedule in both scenarios, makes paying extra principal today exactly equivalent to depositing that amount in a risk-free account compounding monthly at the mortgage's own rate for as long as the loan remains outstanding — source: standard amortization mathematics (definitional identity); read-at-source: derived and independently recomputed directly in this analysis (see chain C1).
- **GT-2** Loan terms as stipulated by the household: $240,000 balance, 30-year fixed, 6.25% APR, 27 years remaining, standard monthly amortization, $60,000 extra principal applied as a lump sum with no recast (payment unchanged) — source: stipulated by the household (not independently source-checkable by this analysis); the "no recast" sub-claim is additionally carried as Assumption A-1 pending written confirmation from the servicer.
- **GT-3** $60,000 in cash is genuinely surplus, held over and above an already-funded 6-month emergency reserve — source: stipulated by the household.
- **GT-4** Household tax facts: standard deduction taken (no mortgage-interest tax shield); 28% federal+state marginal rate on ordinary income; 18% on long-term capital gains and qualified dividends — source: stipulated by the household.
- **GT-5** Decision horizon fixed at 10 years — source: stipulated planning parameter from the household.
- **GT-6** Independently recomputed: $60,000 compounded monthly at 6.25%/12 for 120 months grows to approximately $111,900, closely matching the household's stated $111,913 (the small gap is explained by rounding in intermediate compounding steps); effective annual yield ≈ 6.43%, guaranteed and untaxed (avoided interest, not taxable income) — source: derived from GT-1 + GT-2; read-at-source: recomputed directly in this analysis (chain C1).
- **GT-7** Independently cross-checked: a simplified closed-form approximation (tax the terminal gain once at 18% LTCG at sale, ignoring interim dividend-tax drag) reproduces the household's three stated scenarios within roughly $40-$120 — pretax nominal CAGR 5% → ≈$90,900 (stated $90,833); 7% → ≈$107,600 (stated $107,547); 9.5% → ≈$132,700 (stated $132,862) — and reproduces the stated breakeven pretax nominal CAGR of ≈7.47% almost exactly — source: household's own dividend-reinvestment tax simulation; read-at-source: independently recomputed via an alternate derivation in this analysis (chain C2).
- **GT-8** 10-year U.S. Treasury par yield = 4.02% as of 2026-08-26 — source: U.S. Department of the Treasury, Daily Treasury Par Yield Curve Rates; read-at-source: row for 08/26/2026, fetched directly in this analysis.
- **GT-9?** Secondary commentary indicates the 10-year Treasury yield rose further to approximately 4.6%-4.8% by July-September 2026 — cited to: aggregated financial forecast/news summaries; reported-by-delegate: WebSearch synthesis — the underlying primary sources for the September dates were not opened directly by this analysis.
- **GT-10** S&P 500 Shiller CAPE ratio = 41.80 as of 2026-10-07; historical mean (since the 1880s) = 17.42 — source: multpl.com, Shiller PE page; read-at-source: fetched directly in this analysis, figure/date/mean quoted verbatim from the page.
- **GT-11** Average 30-year fixed-rate mortgage = 7.40% as of 2026-10-08 (up from 7.28% the prior week) — source: Freddie Mac Primary Mortgage Market Survey (PMMS); read-at-source: fetched directly in this analysis, figure and date quoted verbatim.
- **GT-12?** Long-run academic/practitioner research (the Shiller/CAPE literature) finds elevated CAPE readings have historically been associated with below-average subsequent 10-year real equity returns; the relationship is statistical/correlational with wide dispersion, not deterministic, and its predictive power is contested, particularly in the post-2010 low-rate/high-buyback regime — source: general finance literature (training knowledge); unverified: not re-confirmed against a primary dataset this session.
- **GT-13?** The S&P 500's 2000-2009 decade (the "lost decade"), which began at a Shiller CAPE peak near 44 in December 1999, delivered an annualized total return of approximately -0.95% nominal — cited to: Dimensional Fund Advisors commentary and related secondary sources; reported-by-delegate: WebSearch synthesis — the primary return-series data was not opened directly by this analysis.
- **GT-14** Independently computed: applying the $60,000 extra principal payment today while holding the monthly payment constant (≈$1,535/month P&I, independently derived from GT-2's terms) reduces the loan's remaining amortization from 27 years (324 months) to approximately 15.1 years (≈181 months) — roughly 12 years sooner — source: derived from GT-2's amortization parameters; read-at-source: computed directly in this analysis via standard amortization-payment and remaining-term formulas.
- **GT-15?** Under current U.S. tax law (IRC §1014), taxable-brokerage assets receive a step-up in cost basis at the owner's death, eliminating embedded capital-gains tax for heirs; mortgage-paydown "savings" (never-incurred interest) has no equivalent basis-step-up mechanism — source: general tax-law knowledge (training knowledge); unverified: not confirmed against the IRS code this session; relevant only beyond the stated 10-year horizon and therefore not load-bearing for the headline recommendation.
- **GT-16** Diversifying across imperfectly-correlated assets reduces a portfolio's idiosyncratic risk without necessarily reducing its expected return — source: Markowitz (1952) / modern portfolio theory; classified as a physical-law-type mathematical result (Assumption A-12) and promoted directly to ground truth rather than requiring a fresh citation check.
- **GT-17?** Market-implied long-run U.S. inflation expectations (TIPS breakeven) have generally run in approximately the 2.0%-2.5% range through the mid-2020s — source: general market knowledge (training knowledge); unverified: no TIPS-breakeven source was fetched this session.

**Provenance summary:** `?`-marked: GT-9, GT-12, GT-13, GT-15, GT-17 (5 of 17). Read-at-source: GT-1 (self-derived recursion, recomputed in C1), GT-6 (recomputed directly, C1), GT-7 (recomputed via alternate derivation, C2), GT-8 (Treasury.gov daily par yield curve, row 08/26/2026), GT-10 (multpl.com Shiller PE page, figure/date/mean quoted), GT-11 (Freddie Mac PMMS, figure/date quoted), GT-14 (computed directly from GT-2), GT-16 (standard portfolio-theory result). Stipulated (not source-citable; given problem premises): GT-2, GT-3, GT-4, GT-5.

---

## 4. Derivation Chains

*Second-order pass note (actor lens and time lens, applied before the chains below were finalized):* **Actor lens** — the household itself (loses flexibility vs. gains certainty), a future HELOC/mortgage underwriter (who may approve or deny access to the paid-down equity depending on the household's circumstances *at that future time*, not today), a future buyer/market if the home is sold, and the household's own future risk tolerance (which may differ from today's). **Time lens** — immediately (no cash-flow change either way, since the payment is unchanged), within 1-5 years (balances diverge, equity volatility can appear, a liquidity need could surface), at year ~10 (the stated comparison point), and beyond year ~15 (Option A's loan is already retired under the accelerated schedule, while Option B's position is whatever it has become). Both lenses are reflected in chains C5, C6, C7, C8, and C11 below; no extension step was found to contradict a ground truth, so none routes back to Phase 2.

### Conclusion C1: Option A functions as a risk-free asset that dominates every other risk-free alternative open to this household today

GT-1 (paydown = risk-free deposit at mortgage rate) + GT-6 (recomputed FV ≈$111,900, 6.43% effective) + GT-8 (10-yr Treasury 4.02%, Aug 2026)
→ Option A's guaranteed effective yield of about 6.43% is roughly 240 basis points above the risk-free market alternative available to this household today
→ no safe, government-backed instrument currently open to this household pays anywhere close to 6.43% guaranteed and tax-free
→ Option A functions as a risk-free asset that strictly dominates every other risk-free asset this household could buy with the same $60,000

**Pre-check:** head GT-1, GT-6, GT-8 · ?-marked: none · lowest cited: none · Inputs ceiling: HIGH
**Confidence:** HIGH

### Conclusion C2: Choosing Option B is a deliberate bet on capturing close to a full decade of average-or-better equity risk premium

GT-6 (Option A FV $111,900 / 6.43% effective) + GT-7 (Option B breakeven pretax nominal CAGR ≈7.47%) + GT-8 (10-yr Treasury 4.02%)
→ clearing Option A's own outcome requires Option B to earn roughly 3.45 percentage points above today's risk-free rate, year after year, for a full decade
→ a required margin of that size over the risk-free rate is the size of a full, historically-typical equity risk premium, not a trivial gap
→ choosing Option B over Option A is a deliberate bet on capturing close to a full decade of average-or-better equity risk premium, not a near-equivalent, lower-risk alternative

**Pre-check:** head GT-6, GT-7, GT-8 · ?-marked: none · lowest cited: none · Inputs ceiling: HIGH
**Confidence:** HIGH

### Conclusion C3: Today's starting valuation skews Option B's probability-weighted outcome below the historical-average case

GT-10 (CAPE 41.80 vs. historical mean 17.42) + GT-12? (elevated CAPE historically precedes below-average subsequent-decade real returns) + GT-13? (2000-2009 "lost decade" followed a similar CAPE peak near 44)
→ the market's current starting valuation sits in the same historically rare, elevated regime that has twice preceded a multi-year stretch of poor subsequent returns
→ the probability-weighted outcome for a 10-year equity holding started today is skewed below the household's own "historical average" 9.5% CAGR scenario, not centered on it
→ Option B's realistic odds of clearing the 7.47% breakeven from C2 are worse than a simple historical-average framing suggests, though not reduced to zero

**Pre-check:** head GT-10, GT-12?, GT-13? · ?-marked: GT-12?, GT-13? · lowest cited: none · Inputs ceiling: MEDIUM
**Confidence:** LOW — GT-12? (verification: re-run Shiller's own published CAPE/forward-return regression directly against today's reading, not done this session) and GT-13? (verification: open the primary S&P 500 total-return series directly rather than secondary commentary, not done this session) are both unverified at source this session. In addition, a live rival — "CAPE's predictive power is weak this cycle and realized 10-year returns match or exceed history" — is not settled anywhere in this analysis (see Abandoned Reasoning, Dead End 2, and the falsification condition in the adversarial pass record). Both the Inputs axis and the Rivals axis are short, which is why this chain is LOW rather than MEDIUM.

### Conclusion C4: Option A permanently extinguishes a scarce, below-market financing term

GT-2 (household's note: 6.25% fixed) + GT-11 (current market 30-year fixed average: 7.40%)
→ the household's existing loan is already about 115 basis points cheaper than what the same household could obtain by refinancing today
→ once the extra $60,000 is paid down, that cheap, fixed, long-duration borrowing capacity cannot be recreated on the same terms if the household ever wants it back
→ Option A permanently extinguishes a scarce, below-market financing term, which is a real economic cost beyond the loan's own 6.25% rate

**Pre-check:** head GT-2, GT-11 · ?-marked: none · lowest cited: none · Inputs ceiling: HIGH
**Confidence:** HIGH

### Conclusion C5: Option A converts a liquid dollar into one reachable only through a new loan transaction

GT-3 (the $60,000 is surplus beyond the funded emergency reserve) + GT-2 (loan terms, no recast)
→ under Option A, recovering any part of the $60,000 before the home is sold requires originating a new loan (a cash-out refinance or HELOC) at then-prevailing terms and subject to underwriting approval *[Assumes: A-14]*
→ under Option B, the same $60,000 can be sold down to cash in a few business days, with only tax and short-term price risk as friction
→ Option A converts a liquid dollar into a dollar that is reachable only through a transaction with real delay, cost, and approval risk, even though the emergency reserve itself is untouched by either option

**Pre-check:** head GT-2, GT-3 · ?-marked: none · lowest cited: none · Inputs ceiling: HIGH
**Confidence:** MEDIUM — A-14 (home equity cannot be tapped without new loan origination/underwriting) is not quantified: even in the most favorable case for Option A, some minimum transaction friction (30-60+ day closing, or HELOC underwriting) always exists, which is why the qualitative conclusion survives, but this analysis cannot state how much liquidity cost this represents in dollar terms — a household-specific stress-test of actual liquidity needs over the horizon would close this gap.

### Conclusion C6: Option A increases concentration risk in the household's single largest illiquid asset

GT-3 (the $60,000 is surplus cash available to allocate) + GT-16 (diversification reduces idiosyncratic risk without necessarily reducing expected return)
→ every dollar applied to principal adds to the household's existing, single-property, already-leveraged real-estate position *[Assumes: A-9]*
→ every dollar applied to the index fund instead spreads exposure across hundreds of independent businesses and sectors
→ Option A increases concentration risk in the household's single largest illiquid asset while Option B reduces it, independent of which option has the higher expected return

**Pre-check:** head GT-3, GT-16 · ?-marked: none · lowest cited: none · Inputs ceiling: HIGH
**Confidence:** MEDIUM — A-9 (the home already represents a meaningful share of household net worth) is not verified; the household did not disclose total net worth or other holdings. If the home is a small fraction of a much larger portfolio, this chain's conclusion weakens substantially. Verification: the household stating its approximate balance-sheet composition would close this gap.

### Conclusion C7: Option A's advantage is a nominal guarantee, not an inflation hedge

GT-2 (6.25% fixed note, long duration) + GT-17? (market-implied inflation expectations roughly 2.0%-2.5%)
→ in real terms the mortgage's guaranteed paydown return is roughly 4 percentage points above expected inflation, attractive against real yields on inflation-protected Treasuries
→ a fixed-rate loan is a short position on future inflation, so paying it down early forfeits the benefit that higher-than-expected inflation would erode the loan's real burden while nominal equity prices and wages tend to rise alongside that same inflation *[Assumes: A-15]*
→ Option A's advantage is a nominal, locked-in guarantee rather than an inflation hedge, and an inflation surprise to the upside would narrow or reverse its comparative appeal against Option B even though the $111,900 nominal figure itself never changes

**Pre-check:** head GT-2, GT-17? · ?-marked: GT-17? · lowest cited: none · Inputs ceiling: MEDIUM
**Confidence:** LOW — GT-17? (inflation expectations ~2.0%-2.5%) was not fetched from a TIPS-breakeven source this session (verification: pull the current 10-year breakeven from Treasury.gov's TIPS/nominal spread directly). A-15 (nominal equity returns partially track inflation over multi-year horizons) is a standard but imperfect regularity not priced here for its failure mode. Both the Inputs and Inference axes are short, which is why this chain is LOW.

### Conclusion C8: Keeping the home past year 10 would extend Option A's guaranteed-return compounding well beyond the stated 10-year comparison

GT-2 (loan terms: $240,000, 6.25%, 27 years remaining) + GT-14 (extra principal shortens payoff to ≈15.1 years)
→ if the household keeps the home past the 10-year decision horizon, the loan would otherwise still have roughly 17 years left to run, but after the paydown it finishes in about 5 more years
→ for those extra years beyond year 10, Option A keeps generating its guaranteed 6.25% avoided-interest return, a benefit the 10-year snapshot comparison in C1/C2 does not capture
→ extending the analysis horizon beyond 10 years, if the household in fact keeps the home that long, further favors Option A beyond what the headline 10-year numbers already show *[Assumes: A-2]*

**Pre-check:** head GT-2, GT-14 · ?-marked: none · lowest cited: none · Inputs ceiling: HIGH
**Confidence:** HIGH — A-2 (the household keeps the home past year 15) is explicitly conditional in this chain's own wording ("if the household keeps the home... further favors"); if A-2 fails, this chain's extended-horizon benefit simply does not materialize for the unrealized years, but nothing about the headline 10-year comparison in C1-C2 is reversed or weakened by that failure, so the endpoint as stated still stands either way.

### Conclusion C9: A blended allocation beats either pure corner once liquidity, concentration, and the forfeited below-market loan are weighed, under a neutral return assumption

C1 (Option A dominates safe alternatives) + C2 (Option B requires a full risk-premium bet) + C4 (Option A forfeits a below-market loan) + C5 (Option A costs liquidity) + C6 (Option A adds concentration) + C8 (Option A compounds longer if the home is kept)
→ scored on a locked seven-criterion weighted matrix with Option B's return criterion held at its neutral, historical-average footing, the weighted totals come out to Option A 60, Option B 69, and an even 50/50 split 64
→ no single criterion's weight needs to move by more than one point on a 1-21 scale to flip the ranking, so the matrix result is a near-tie rather than a robust lean either way
→ once liquidity, concentration, and the forfeited below-market loan are weighed as the household asked, a pure 100%-either-way allocation is not clearly superior to a blended allocation, which is the one finding this matrix supports with confidence

**Pre-check:** head C1 (HIGH), C2 (HIGH), C4 (HIGH), C5 (MEDIUM), C6 (MEDIUM), C8 (HIGH) · ?-marked: none · lowest cited: MEDIUM · Inputs ceiling: MEDIUM
**Confidence:** MEDIUM — C5 and C6 are each MEDIUM for the reasons stated on their own confidence lines (A-14's unquantified magnitude; A-9's unknown net-worth context), and this chain is capped at their level because it cites them on its head.

### Conclusion C10: The valuation judgment in C3 is what tips the recommendation from a near-even blend toward a paydown-leaning split

C9 (near-tie between A, B, and a blend, under a neutral return assumption) + C3 (today's valuation skews Option B's probability-weighted outcome below the historical-average case)
→ replacing the neutral, historical-average score for Option B's return criterion with a valuation-adjusted score flips the matrix from "Option B 69, Option A 60" to "Option A 65, Option B 64, split 64" — a swing large enough to move the ranking, not just the margin
→ because that swing is driven entirely by the one judgment this analysis is least able to verify at source this session, the honest recommendation is a blend that leans toward paydown rather than a 50/50 split or a full tilt toward Option B
→ a household that rejects the valuation judgment in C3 should read this tilt as unsupported and default to the near-even blend C9 establishes instead

**Pre-check:** head C9 (MEDIUM), C3 (LOW) · ?-marked: none · lowest cited: LOW · Inputs ceiling: LOW
**Confidence:** LOW — this chain is capped at C3's LOW rating because it cites C3 on its head; C3's own confidence line (GT-12?, GT-13?, and the unsettled CAPE-predictive-power rival) carries the full explanation and is not repeated here. This is also this analysis's single most sensitivity-critical chain — see the Sensitivity step of the adversarial pass record below.

### Conclusion C11: Securing a standby HELOC before or alongside the paydown is a required mitigation, not an optional nicety

C5 (Option A reduces liquidity and optionality) + GT-11 (current mortgage-market terms, by extension the market for home-equity lines)
→ a standby home-equity line of credit secured while the household is employed and well-qualified converts illiquid home equity back into an accessible, if costlier and variable-rate, source of cash
→ securing that line before or immediately after the paydown directly offsets the liquidity cost identified in C5, without requiring any change to the paydown-versus-invest allocation itself
→ the household should treat opening a standby HELOC as a required step of this plan, not an optional afterthought, because it is the one mitigation that neutralizes the single scenario (a forced distress sale triggered by an unexpected cash need beyond the emergency reserve) in which Option A's downside is severe rather than merely a smaller gain

**Pre-check:** head C5 (MEDIUM), GT-11 · ?-marked: none · lowest cited: MEDIUM · Inputs ceiling: MEDIUM
**Confidence:** MEDIUM — capped at C5's MEDIUM rating (cited on this chain's head); in addition, a minor live rival — holding a larger standing cash buffer instead of a HELOC — is not fully settled here (a HELOC is typically cheaper to maintain than idle cash is to hold, but carries variable-rate and renewal risk a cash buffer does not).

---

### Assumption Audit scan (process output)

| Chain | Step | Step Text (brief) | Assumption surfaced? | Added to Table? |
|---|---|---|---|---|
| C1 | 1 | guaranteed yield ~240bp above risk-free market alternative | none | n/a |
| C1 | 2 | no safe instrument pays close to 6.43% | none | n/a |
| C1 | 3 | Option A dominates every risk-free alternative | none | n/a |
| C2 | 1 | B must earn ~3.45pp above risk-free | none | n/a |
| C2 | 2 | that margin is a full equity-risk-premium | none | n/a |
| C2 | 3 | choosing B is a risk-premium bet | none | n/a |
| C3 | 1 | current valuation sits in a historically rare regime | none | n/a |
| C3 | 2 | probability-weighted outcome skewed below 9.5% case | none | n/a |
| C3 | 3 | B's odds of clearing breakeven are worse than history suggests | none | n/a |
| C4 | 1 | existing note ~115bp cheaper than today's market | none | n/a |
| C4 | 2 | cheap borrowing capacity cannot be recreated | none | n/a |
| C4 | 3 | Option A extinguishes a below-market financing term | none | n/a |
| C5 | 1 | recovering paid-down equity requires a new loan | A-14 (home equity requires new origination/underwriting) | yes |
| C5 | 2 | B's $60k sellable in days | none | n/a |
| C5 | 3 | A converts liquid dollar to transaction-gated dollar | none | n/a |
| C6 | 1 | principal payments add to single-property concentration | A-9 (home's share of net worth unknown) | yes |
| C6 | 2 | index fund spreads exposure across many businesses | none | n/a |
| C6 | 3 | A raises concentration risk, B lowers it | none | n/a |
| C7 | 1 | real guaranteed return ~4pp above expected inflation | A-11 already tabled (inflation estimate) | n/a (reused, not duplicated) |
| C7 | 2 | fixed-rate debt forfeits inflation-erosion benefit | A-15 (nominal equity returns partially track inflation) | yes |
| C7 | 3 | A's edge is nominal, not an inflation hedge | none | n/a |
| C8 | 1 | loan would otherwise run ~17 more years | none | n/a |
| C8 | 2 | A keeps compounding 6.25% beyond year 10 | A-2 already tabled (home kept past horizon) | n/a (reused, not duplicated) |
| C8 | 3 | longer horizon further favors A, conditional on keeping the home | none | n/a |
| C9 | 1 | weighted matrix: A=60, B=69, split=64 (neutral) | A-9 already tabled (feeds C6, reused here) | n/a (reused, not duplicated) |
| C9 | 2 | flip test: <1-point weight move changes ranking | none | n/a |
| C9 | 3 | blend beats either pure corner | none | n/a |
| C10 | 1 | valuation-adjusted score flips A=65, B=64, split=64 | none | n/a |
| C10 | 2 | recommendation leans paydown because of C3's judgment | none | n/a |
| C10 | 3 | a reader rejecting C3 should default to C9's near-tie | none | n/a |
| C11 | 1 | standby HELOC converts illiquid equity to accessible cash | none | n/a |
| C11 | 2 | securing it offsets C5's liquidity cost | none | n/a |
| C11 | 3 | HELOC is a required step, not optional | none | n/a |

---

## 5. Abandoned Reasoning

### Dead End: Recommend 100% Option A (full mortgage payoff)

**What was tried:** The guaranteed-return math alone (GT-6, chain C1) looks like a clean win — 6.43% risk-free, tax-free, beats any safe alternative and beats the certainty-equivalent of a valuation-stretched equity market. The initial instinct was to recommend putting the entire $60,000 toward principal.

**Why abandoned:** The trade-off matrix (chain C9) shows this corner scores only 60 against a near-even blend's 64 and Option B's neutral-case 69 — it is not decisively superior once liquidity (C5) and concentration (C6) costs are counted, as the user explicitly asked. The pre-mortem (below) also identifies a genuinely fatal-tier tail scenario — a forced distress sale triggered by a liquidity need beyond the emergency reserve, with no standby credit line in place — that a 100%-paydown allocation with no mitigation does not avoid.

**What it ruled out:** Treating the guaranteed-return comparison as sufficient justification on its own, which ignores the liquidity and concentration dimensions the user explicitly asked to be weighed, and ignores the tail-risk case the pre-mortem surfaces.

### Dead End: Recommend 100% Option B (full index-fund investment)

**What was tried:** Using the household's own historical-average 9.5% CAGR scenario, Option B beats Option A ($132,862 vs. $111,913), and broad equities have beaten mortgage rates this low over most historical 10-year windows. The initial instinct, reading the prompt's own optimistic scenario, was to recommend putting the entire $60,000 into the index fund.

**Why abandoned:** Current valuation context (GT-10: CAPE 41.80, near the December-1999 dot-com peak) combined with the empirical 2000-2009 "lost decade" precedent (GT-13?) and the mainstream CAPE-forward-return literature (GT-12?) means the "historical average" scenario is not the right central case to anchor on at this specific valuation starting point (chain C3). The breakeven bar (7.47%, chain C2) is uncomfortably close to or above many valuation-aware forward-return estimates for this starting point.

**What it ruled out:** Treating "stocks beat a 6.25% mortgage rate on average, historically" as sufficient justification without accounting for the starting valuation — exactly the reasoning-by-historical-analogy error this methodology is built to catch.

---

## 6. Conclusion

**Recommended approach:** Split the $60,000 roughly 70/30 toward paydown over investment — about $42,000 applied to mortgage principal and about $18,000 invested in the taxable index fund — rather than sending the full amount to either side (chains C9, C10). Treat two execution steps as required, not optional: get written confirmation from the loan servicer that no recast will occur before remitting the payment, and secure a standby home-equity line of credit while still well-qualified, concurrently with or immediately after the paydown (chain C11).

- Confirm in writing with the servicer that the payment schedule is unchanged — no chain — flagged assumption only
- Confirm no prepayment penalty applies to this specific note — no chain — flagged assumption only
- Open a standby HELOC while employed and well-qualified, sized to roughly replace the $42,000 of liquidity being traded away (chain C11).
- Write a one-paragraph personal investment policy committing to the index-fund tranche's multi-year horizon before investing it, to pre-empt panic-selling in a drawdown (chain C5).

**Key insight:** The decision does not actually turn on whether equities beat a 6.25% mortgage *on average* — over most historical 10-year windows they have (chain C2) — it turns on whether today's historically rare starting valuation (CAPE 41.80 against a 17.42 long-run mean, chain C3) is a good enough reason to discount that average for this specific decade. The trade-off matrix's own flip-test shows the entire headline recommendation pivots on that one judgment: swap in a neutral, historical-average score for Option B's return criterion and the ranking flips from "lean paydown" to "lean invest" (chain C10). That single, currently-unverified-at-source judgment — not the arithmetic in the original prompt, which is correct — is where this recommendation is actually resting its weight.

**Trade-offs acknowledged:** This recommendation accepts a real chance of regret: if equities deliver a strong decade despite today's valuation (a live, unsettled rival — see Dead End: Recommend 100% Option B), the 70% paydown tranche will have underperformed what an all-in equity allocation would have earned, though it will not have *lost* money in any absolute sense (chain C2). It also knowingly forfeits part of the inflation-hedge value and below-market refinancing value embedded in the household's existing 6.25% note (chains C7, C4) in exchange for a guaranteed, de-risked outcome on the larger tranche. It deprioritizes the simplicity of a single clean action (either pure corner, chain C9) in favor of a blend that requires two more moving pieces to execute (the HELOC and the investment policy, chain C11).

**Pre-check:** head C10 (LOW), C11 (MEDIUM), C8 (HIGH), C4 (HIGH), C7 (LOW) · ?-marked: none · lowest cited: LOW · Inputs ceiling: LOW
**Confidence:** LOW overall for the *specific 70/30 tilt*, but MEDIUM for the broader, more load-bearing finding that *some blend beats either pure corner* (chain C9). These are deliberately reported separately: C9's "blend beats either extreme" finding rests only on MEDIUM-rated inputs (C5, C6) and is comparatively robust. The further tilt from a near-even blend toward 70/30-favoring-paydown rests on chain C10, which is capped LOW because it is built on C3 — the valuation judgment resting on GT-12? and GT-13?, neither verified at source this session, plus a live, unsettled rival (chain C7 and the pre-mortem's Falsification condition below). A household that independently verifies GT-12?/GT-13? (e.g., by pulling Shiller's own regression output and the primary S&P 500 return series) or that simply does not find the valuation argument persuasive should treat C10 as unsupported and fall back to C9's near-even blend (roughly 50/55% paydown) instead of 70/30.

---

## §6→§4 closure ledger (process output)

- "Split the $60,000 roughly 70/30 toward paydown over investment..." → chains C9, C10 ✓ (cited inline)
- "...get written confirmation from the loan servicer that no recast will occur..." → chain C11 ✓ (cited inline)
- "Confirm in writing with the servicer that the payment schedule is unchanged" → no chain — flagged assumption only
- "Confirm no prepayment penalty applies to this specific note" → no chain — flagged assumption only
- "Open a standby HELOC while employed and well-qualified..." → chain C11 ✓ (cited inline)
- "Write a one-paragraph personal investment policy..." → chain C5 ✓ (cited inline)
- "The decision does not actually turn on whether equities beat a 6.25% mortgage on average... it turns on whether today's historically rare starting valuation... is a good enough reason..." → chains C2, C3 ✓ (cited inline)
- "...the entire headline recommendation pivots on that one judgment: swap in a neutral, historical-average score... the ranking flips..." → chain C10 ✓ (cited inline)
- "...a real chance of regret: if equities deliver a strong decade despite today's valuation..." → chain C2 ✓ (cited inline)
- "...knowingly forfeits part of the inflation-hedge value and below-market refinancing value..." → chains C7, C4 ✓ (cited inline)
- "...deprioritizes the simplicity of a single clean action..." → chain C9 ✓ (cited inline)
- "...requires two more moving pieces to execute..." → chain C11 ✓ (cited inline)
- "**Confidence:** LOW overall for the specific 70/30 tilt, but MEDIUM for the broader... finding..." → chains C9, C10, C3, C7 ✓ (cited inline)
- "**Pre-check:** head C10 (LOW), C11 (MEDIUM), C8 (HIGH), C4 (HIGH), C7 (LOW)..." → chains C10, C11, C8, C4, C7 ✓ (self-discharging per the Pre-check rule)

---

## Self-audit scan (process output)

| Chain | Chain Head (brief) | Form conforming? | Rule applied | Dependency clean? | Band | Act attempted? | Edges fired |
|---|---|---|---|---|---|---|---|
| C1 | GT-1, GT-6, GT-8 | yes | n/a | yes | HIGH | yes | none |
| C2 | GT-6, GT-7, GT-8 | yes | n/a | yes | HIGH | yes | none |
| C3 | GT-10, GT-12?, GT-13? | yes | n/a | yes | LOW | yes | none |
| C4 | GT-2, GT-11 | yes | n/a | yes | HIGH | yes | none |
| C5 | GT-3, GT-2 | yes | n/a | yes | MEDIUM | no | none |
| C6 | GT-3, GT-16 | yes | n/a | yes | MEDIUM | no | none |
| C7 | GT-2, GT-17? | yes | n/a | yes | LOW | no | none |
| C8 | GT-2, GT-14 | yes | n/a | yes | HIGH | no | none |
| C9 | C1, C2, C4, C5, C6, C8 | yes | n/a | yes | MEDIUM | no | none |
| C10 | C9, C3 | yes | n/a | yes | LOW | no | none |
| C11 | C5, GT-11 | yes | n/a | yes | MEDIUM | yes | none |

| §6 Span (brief) | Construct | Claim under R11? | R11 clause applied | Chain cited |
|---|---|---|---|---|
| "Split the $60,000 roughly 70/30... (chains C9, C10)...secure a standby HELOC...(chain C11)" | bold lead-in | yes | colon closes bold span, text follows on same line | C9, C10, C11 |
| "Confirm in writing with the servicer that the payment schedule is unchanged" | list item | yes | closes its own sentence / over 40 chars | none — flagged assumption only |
| "Confirm no prepayment penalty applies to this specific note" | list item | yes | closes its own sentence / over 40 chars | none — flagged assumption only |
| "Open a standby HELOC while employed and well-qualified..." | list item | yes | closes its own sentence, over 40 chars | C11 |
| "Write a one-paragraph personal investment policy..." | list item | yes | closes its own sentence, over 40 chars | C5 |
| "**Key insight:** The decision does not actually turn on..." | bold lead-in | yes | colon closes bold span, text follows on same line | C2, C3, C10 |
| "**Trade-offs acknowledged:** This recommendation accepts..." | bold lead-in | yes | colon closes bold span, text follows on same line | C2, C7, C4, C9, C11 |
| "**Pre-check:** head C10 (LOW), C11 (MEDIUM), C8 (HIGH), C4 (HIGH), C7 (LOW)" | bold lead-in | yes | colon closes bold span; Pre-check is a claim discharged by its own head per the template rule | C10, C11, C8, C4, C7 |
| "**Confidence:** LOW overall for the specific 70/30 tilt..." | bold lead-in | yes | colon closes bold span, text follows on same line | C9, C10, C3, C7 |

Scan complete: 11 chain rows, one per section-4 chain block in order; 9 section-6 rows, one per construct in order — 9 claims under R11, 0 excluded. 0 chains malformed, 0 claims untraced.

---

## Adversarial pass (process output)

**Recompute.** GT-6: $60,000 × (1 + 0.0625/12)^120, computed independently, ≈ $111,900 — matches the stated $111,913 within rounding of intermediate compounding steps. GT-7: a simplified closed-form check (tax the terminal gain once at 18% LTCG, ignore interim dividend drag) reproduces the stated $90,833 / $107,547 / $132,862 scenarios within roughly $40-$120, and reproduces the stated ≈7.47% breakeven CAGR almost exactly. GT-14: independently derived monthly payment ≈$1,535 on the original $240,000/27-year note, and ≈$1,535 against the new $180,000 balance solves to a remaining term of ≈181 months (≈15.1 years), not supplied by the household and newly computed in this analysis. Trade-off matrix (chain C9): weighted totals A=60, B=69, split=64 under the neutral return assumption, recomputed by hand from the stated weights and scores. Trade-off matrix (chain C10): A=65, B=64, split=64 under the valuation-adjusted return assumption, recomputed the same way.

**Sensitivity.** The single ground truth whose falsity would flip the headline recommendation is **GT-12?** (elevated CAPE historically precedes below-average subsequent-decade equity returns) — it is `?`-marked. If GT-12? does not hold in this cycle (i.e., CAPE carries little genuine predictive power and realized 10-year returns track or exceed the historical average regardless of starting valuation), chain C10 loses its basis, the recommendation collapses back to chain C9's near-even blend, and the honest default shifts from "lean paydown, ~70/30" to "near 50/50, marginal lean to invest." Verification path: pull Shiller's own published CAPE/forward-return regression output directly and check whether the relationship still holds with post-2010 data included, rather than relying on the general, training-knowledge characterization used here.

**Rival.** Headline recommendation (the 70/30 split): the two strongest rivals are "100% Option A" and "100% Option B," both addressed in full in section 5 (Abandoned Reasoning) — each is ruled out by the trade-off matrix (chains C9/C10) and, for 100% Option A specifically, by the liquidity-trap tail risk identified in Cluster 2 below. Chain C3: the live rival "CAPE has no reliable predictive power this specific cycle" is not settled anywhere in this analysis and is carried explicitly on C3's own confidence line and on the Falsification condition below — this is the same rival the Sensitivity step above names. Chains C1, C2, C4, C8: no live rival was identified; these are comparatively uncontroversial, narrow factual claims (rate comparisons, amortization arithmetic). Chains C5, C6, C7: `rival not applicable — these establish a qualitative direction (liquidity cost, concentration cost, inflation-hedge cost) rather than a contested point estimate, and no competing claim about the *direction* of each effect was identified`.

**Adversarial technique — Pre-Mortem** *(the conclusion is a plan/recommendation, so pre-mortem applies rather than inversion)*.

*Premise:* It is 2036. The household executed the 70/30 split — $42,000 to principal, $18,000 to the index fund, with a standby HELOC and a written no-recast confirmation — ten years ago. In hindsight, it was the wrong call. What caused it?

*Causes (unfiltered, from the household's own hindsight view, a fee-only financial planner's review, a tax advisor's review, and an equity-bull devil's-advocate view):*
1. Equities delivered an extraordinary decade (AI-driven productivity boom, sustained multiple expansion) — the household's 18% into equities now looks like a badly undersized bet relative to what an all-in position would have returned (bull viewpoint).
2. A job loss or medical event beyond the 6-month reserve hit in year 3, and credit tightened at the same time, so the HELOC application was denied or priced punitively right when it was needed, forcing a distress sale of the home (planner/household viewpoint).
3. Inflation ran hot (5%+ for several years) — nominal wages and asset prices rose with it, and the fixed 6.25% note turned out to be a bargain worth keeping, not retiring early (tax-advisor/household viewpoint).
4. The household relocated for a job in year 4 and sold into a soft local housing market at the same time a correlated recession hit equities too, so both tranches underperformed together instead of diversifying each other (planner viewpoint).
5. The servicer recast the loan despite the written confirmation (an administrative error or a misunderstanding of the loan's own terms), which didn't match what the household had planned for and caused confusion about whether the guaranteed-return math still held (planner viewpoint).
6. After years of a flat-feeling house with no visible monthly cash-flow change, while financial news repeatedly touted all-time-high markets, the household impulsively tapped the new HELOC to chase the market late in the cycle, compounding risk rather than reducing it (household/bull viewpoint — behavioral).
7. A future tax-law change raised LTCG rates or altered the step-up-in-basis rule, retroactively making the brokerage tranche worse than modeled (tax-advisor viewpoint).
8. The $18,000 equity tranche was invested as a single lump sum immediately before a sharp near-term correction, and the household panic-sold near the bottom rather than holding through it (bull/behavioral viewpoint).

*Clusters:*
- **Cluster 1 — Opportunity-cost regret** (cause 1; bears on chains C2, C3, C10): equities outperform, and the paydown-leaning split captured less upside than an all-in equity bet would have.
- **Cluster 2 — Liquidity trap** (causes 2, 4; bears on chains C5, C11): illiquidity of home equity collides with an unexpected cash need, and the mitigation fails or proves insufficient.
- **Cluster 3 — Inflation-hedge forfeiture** (cause 3; bears on chain C7, GT-17?): a fixed-rate loan's hedge value is given up just as inflation makes that hedge valuable.
- **Cluster 4 — Operational/execution risk** (cause 5; bears on Assumption A-1): the "no recast" premise the entire GT-6 equivalence rests on turns out to be false in practice despite written confirmation.
- **Cluster 5 — Behavioral/sequencing risk** (causes 6, 8; bears on Assumption A-10, chain C5): the investment tranche is mishandled by the household's own future behavior rather than by the market.
- **Cluster 6 — Policy/tax-law risk** (cause 7; bears on GT-15?): legislative change alters the comparison after the fact.

*Triage and disposition:*
- Cluster 1 — **Costly but survivable.** Even in the worst version of this regret, the household is still wealthier in absolute terms than if it had done nothing; it simply isn't as wealthy as the all-in-equity counterfactual. **Accepted risk**, no plan change: the 18% equity tranche deliberately preserves upside participation in exchange for certainty on the larger tranche.
- Cluster 2 — **Fatal-tier if it coincides with a forced distress sale; costly-but-survivable otherwise.** This is the one tail scenario that can turn a "smaller gain" into a genuine loss. **Plan change:** securing the standby HELOC (chain C11) is promoted from a nice-to-have to a required step, executed *before* or immediately alongside the paydown, specifically while the household is still well-qualified — underwriting is far easier to obtain when it is not urgently needed. Tripwire: liquid assets (cash + the brokerage tranche) fall below three months of expenses while a HELOC draw or application is pending — monitor this explicitly.
- Cluster 3 — **Costly but survivable.** A real but bounded economic cost. **Accepted risk**, no further mitigation beyond the diversification the 18% equity tranche already provides (equities tend to do passably, if imperfectly, in moderate inflation). Tripwire: trailing 3-year CPI averages notably above 4% — re-evaluate at that point.
- Cluster 4 — **Costly but survivable, and easily prevented.** **Plan change:** obtain the servicer's no-recast confirmation in writing *before* remitting the extra-principal payment (already listed under Recommended approach), not after.
- Cluster 5 — **Costly but survivable, and largely preventable by discipline.** **Plan change:** write a one-paragraph investment policy statement (already listed under Recommended approach) committing to the equity tranche's multi-year horizon and to not raiding the HELOC to chase the market, before investing any of it.
- Cluster 6 — **Tolerable.** Outside the household's control, low-probability, modest expected impact. **Accepted risk**, no action.

*Falsification:* This recommendation is false — i.e., should not have been followed — if, in hindsight, (a) the household needed liquidity that even the pre-arranged HELOC could not supply because credit markets froze broadly (a systemic, not household-specific, failure), or (b) equities delivered a sustained double-digit nominal CAGR with no serious drawdown over the decade, in which case an all-in-Option-B allocation would have dominated with the benefit of hindsight, or (c) the "no recast" premise underlying GT-2/GT-6 was simply false despite written confirmation, invalidating the guaranteed-FV equivalence the entire paydown side of this analysis rests on.

---

## Self-Audit Gate (process output)

**Criterion 1: Identify Essence**
Quoted span: "Should this household apply its full $60,000 surplus cash to pay down a 6.25% mortgage with no tax shield (a guaranteed, risk-free ~6.43% effective return), invest it in a taxable broad-market index fund... or split it between the two over a 10-year horizon — and does today's specific valuation/rate environment, plus the household's liquidity and diversification needs, change the answer..."
Band: **Rigorous**
Justification: the statement names the actual decision (a three-way allocation choice informed by current valuation context) rather than restating the prompt's arithmetic, and all five success criteria are stated as pass/fail structural tests checkable directly against section 6 (e.g., "names a single specific allocation," "cites at least one current-market data point fetched at source").

**Criterion 2: Challenge Assumptions**
Quoted span (from the Assumption Audit scan): "C5 | 1 | recovering paid-down equity requires a new loan | A-14 (home equity requires new origination/underwriting) | yes" together with the Assumptions Table's A-6 row: "Discard as the default base case — em-dash: contradicted by GT-10/GT-12?/GT-13?..."
Band: **Rigorous**
Justification: every row uses the four-type scheme, every Verdict cell is a leading token plus em-dash justification, at least one assumption (A-6) is Discarded rather than merely Accepted, every row used in a chain while unverified carries "unverified — flagged," and the Assumption Audit scan confirms the audit ran exhaustively over every named chain step and added two previously-unsurfaced assumptions (A-14, A-15) back into the table.

**Criterion 3: Establish Ground Truths**
Quoted span: "?-marked: GT-9, GT-12, GT-13, GT-15, GT-17 (5 of 17)." Cross-checked against the Ground Truths list: GT-9?, GT-12?, GT-13?, GT-15?, GT-17? are exactly the five `?`-suffixed entries — the enumeration matches the list.
Band: **Sound**
Justification: provenance labels, stable IDs, and the enumeration are all correct and checkable, and every unsuffixed GT feeding a HIGH-confidence chain that has an externally-citable source names its read-at-source location (GT-1, GT-6, GT-8, GT-11); the one specific, identifiable shortfall is that GT-2 (stipulated loan terms) feeds HIGH-confidence chains (C4, C8) without a classic read-at-source citation, because this analysis declared a separate "stipulated input" lane for household-reported facts rather than suffixing them — a disclosed, deliberate choice, but one departure from the strict provenance form on an otherwise-correct list, which is the Sound rather than Rigorous descriptor.

**Criterion 4: Reason Upward**
Quoted span (from the Self-audit scan's chain-form table): "C9 | C1, C2, C4, C5, C6, C8 | yes | n/a | yes | MEDIUM | no | none" and "Scan complete: 11 chain rows, one per section-4 chain block in order... 0 chains malformed, 0 claims untraced."
Band: **Rigorous**
Justification: every one of the 11 chains is form-conforming with clean dependencies per the scan, every chain carries exactly one intermediate-to-conclusion structure with no redundant restatement, the Abandoned Reasoning section documents two dead ends in the full What-was-tried/Why-abandoned/What-it-ruled-out structure with specific (non-generic) reasons, no analogy is used as direct evidence (GT-13?'s 2000-2009 precedent is grounded as a cited ground truth, not offered as a bare analogy), and every chain step introducing a new assumption (C5, C6, C7, C8) carries an inline `[Assumes: A-N]` tag per the Assumption Audit scan.

**Criterion 5: Validate**
Quoted span: "C10 is capped at C3's LOW rating because it cites C3 on its head... A chain is also rated no higher than the lowest-rated chain its head cites" and the adversarial pass record's full Recompute/Sensitivity/Rival/Premise/Causes/Clusters/Disposition/Falsification sequence with every cluster carrying either a named plan change (Clusters 2, 4, 5) or an explicitly accepted risk with a named mitigation (Clusters 1, 3, 6).
Band: **Rigorous**
Justification: no chain consuming a `GT-N?` input is rated HIGH (C3, C7 are both LOW), every chain is capped at the lowest-rated chain its head cites (C9, C10, C11 all correctly capped), the overall Conclusion's LOW/MEDIUM split rating is explicitly reconciled against its weakest contributing chains (C10's LOW), and the adversarial pass record is complete with every cluster disposed of rather than merely listed.

**Criterion 6: Conclusion-to-Ground-Truth Traceability**
Quoted span (from the Self-audit scan's claim-inventory table): "Scan complete: 11 chain rows... 9 section-6 rows, one per construct in order — 9 claims under R11, 0 excluded... 0 claims untraced."
Band: **Rigorous**
Justification: every section-6 claim either cites a specific chain inline or carries the `no chain — flagged assumption only` marker (the two servicer/prepayment checklist items), no claim introduces reasoning absent from section 4, and the Key Insight (the recommendation pivots on the unverified CAPE judgment in C3, not on the arithmetic itself) is a non-obvious finding distinct from the Recommended Approach rather than a restatement of it.

**Gate result:** No criterion scored Absent (condition 1 cleared). Zero criteria scored Hand-wavy, well under the one-Hand-wavy cap (condition 2 cleared). **The analysis clears the Self-Audit Gate on the first scoring pass; no Fix/Repeat re-perception pass was required.**

