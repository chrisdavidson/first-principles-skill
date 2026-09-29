## Techniques not applied (process output)

- fishbone — not applicable — the assumption space for this decision is bounded and directly enumerable (loan mechanics, tax treatment, equity-return uncertainty, liquidity access); it is not so multi-causal that a breadth-first category brainstorm is needed to surface it.
- theoretical-limit (Phase 1 reframe) — not applicable — the essence of this decision is a resource-allocation choice between two well-defined instruments, not a question of whether a stated figure (the 6.25% rate) is a negotiable convention versus a hard bound; the rate is a fixed contractual fact, not a ceiling to derive.
- theoretical-limit (Phase 4 ceiling) — not applicable — there is no governing hard constraint whose law-permitted ceiling needs deriving; the comparison is between a contractual guaranteed rate and a market-driven uncertain return, not a "what is the maximum possible" question.
- inversion (Phase 5 adversarial technique) — not applicable — the headline output is a recommendation/plan (an allocation of $60,000), not a bare claim, so per the inversion-vs-pre-mortem decision rule the adversarial pass uses pre-mortem instead; inversion's Phase 2 invocation (challenging the assumption set) did fire and is recorded in the Assumptions Table.

## Assumption Audit scan (process output)

| Chain | Step | Step Text (brief) | Assumption surfaced? | Added to Table? |
|---|---|---|---|---|
| C1 | head | GT-1+GT-2 loan terms and amortization formula | No new assumption beyond Phase 2 table | — (clean pass) |
| C1 | hop1-4 | Compute payment, shortened term, balance differential, FV equivalence | No new assumption | — (clean pass) |
| C2 | hop1 | Blend Vanguard US/developed-ex-US ranges into a global band | Yes — the blend weights (implicit ~60/30/10 US/dev-ex-US/EM) are an analyst choice, not household-specified | Yes — A-2 |
| C2 | hop2 | Apply 1.5% blended dividend yield + 18% annual tax drag | Yes — the 1.5% blended yield figure is an estimate, not a verified figure for the specific fund the household would actually buy | Yes — A-3 |
| C2 | hop3-4 | Apply same tax model to historical and lost-decade reference returns | No new assumption (uses already-flagged GT-8?/GT-12?) | — (clean pass) |
| C2 | hop5 | State the bracket | No new assumption | — (clean pass) |
| C3 | hop1-2 | Solve breakeven algebraically; compare to forecast range | No new assumption | — (clean pass) |
| C3 | hop3 | Score options on 8 weighted criteria | Yes — the weights reflect an assumed "neutral" household preference, not this household's stated risk/liquidity preferences [Assumes: A-1] | Yes — A-1 |
| C3 | hop4 | Flip-test the weighted score | No new assumption | — (clean pass) |
| C4 | hop1-2 | Actor lens and time lens extension | Yes — assumes no low-cost/no-cost recast is offered on this loan, consistent with the user's stated framing but not independently confirmed | Yes — A-4 |
| C4 | hop3 | Pre-mortem liquidity-shock cluster informs disposition | No new assumption (uses A-4, GT-7) | — (clean pass) |
| C4 | hop4 | Combine breakeven margin with liquidity disposition into a split | Yes — the specific 60-70%/30-40% split is an analyst judgment synthesis, not a numerically optimized allocation | Yes — A-5 |

Scan note: assumptions A-1 through A-5 surfaced by this audit are folded into the Classified Assumptions Table (§2) below, each retaining its inline `[Assumes: X]` mark at the originating chain step in §4.
## Adversarial pass (process output)

**Recompute:** GT-3 payment ($240,000, 6.25%/12 monthly, n=324) recomputed independently via M=Pr(1+r)^n/((1+r)^n−1) → $1,535.40/month, matches. GT-6 differential recomputed two ways (balance-schedule differencing: $192,476−$80,552=$111,924; and direct FV of $60,000 at 6.25% APR monthly-compounded for 120 months: $60,000×(1.00520833)^120=$111,924) — both methods agree exactly, which is the expected mathematical identity, not a coincidence. C2's breakeven algebra (49,200X+10,800=111,924 → X=2.0554 → r=7.74%) recomputed by substituting r=7.74% back through the after-tax formula: g=7.47%, FV=60,000×(1.0747)^10≈$121,700 pretax-equivalent-growth-adjusted, gain≈$61,700, CGT≈$11,110, after-tax≈$111,924 — closes the loop within rounding.

**Sensitivity:** The single ground truth whose falsity would flip the headline dollar comparison is GT-10 (Vanguard's 10-year forward equity forecast). GT-10 is unsuffixed (read-at-source), but the flip does not require GT-10 to be *wrong* — it only requires realized returns to land above the top of GT-10's stated range, which GT-10 itself does not rule out (forecasts are ranges, not ceilings). This is a Rivals-axis issue, not an Inputs-axis one, and it cannot be closed by re-reading the source again — only by waiting out the horizon or narrowing the range with a probabilistic model, which is outside this analysis's scope. The weakest link on C3/C4 is hop3 of C3 ([Assumes: A-1]): the weighted trade-off's recommendation direction is not robust — the flip-test in C3-hop4 shows a 2-point weight change on a 5-point scale reverses the composite winner.

**Rival:** Headline conclusion ("lean 60-70% toward paydown") — strongest rival is "invest 100% of the $60,000" (Option B in full). This rival is not ruled out by the ground truths; it is only shown to require pretax nominal equity returns above 7.74%/yr, which is above GT-10's entire stated range but below GT-8?'s historical average — the rival stays live and is named on C3/C4's confidence lines rather than claimed settled. For C1 (guaranteed-value calculation): no live rival — this is a closed-form arithmetic result from contractual terms, not a forecast; `rival not applicable — closed-form calculation from stated contractual terms, not a probabilistic estimate`. For C2 (equity bracket): the rival is "the true 10-year return lies outside the stated bracket entirely" — addressed by including both the historical-average and lost-decade reference points as explicit outer bounds, but not eliminated (a rival to a probabilistic bracket cannot be eliminated in advance) — recorded live, pointed at from C2's confidence line. For C3's weighted trade-off (hop3-4): the rival "100% paydown is composite-optimal" is the mirror image of the headline rival, ruled out by the flip-test itself showing neither pole is robust — this is what motivates the hybrid recommendation rather than either extreme; recorded as a §5 Abandoned Reasoning entry (AR-1, AR-2 below) with the flip-test naming what ruled each pole out.

**Premise:** It is three years from now (2029) and the household's decision to commit the bulk of the $60,000 to mortgage paydown has turned out to be a costly mistake.

**Causes** (generated from three stakeholder viewpoints — the household member managing day-to-day cash flow, a future version of the household needing unplanned liquidity, and a rival investment-focused advisor):
1. A major unplanned expense beyond the funded 6-month emergency reserve (job loss extending past six months, uninsured medical cost, major home-system failure, family emergency) hit within the 10-year window, and the household had no accessible liquid capital beyond that reserve, forcing high-interest credit-card debt or a HELOC underwritten on worse terms than if $60,000 had simply stayed liquid (GT-7).
2. Interest rates fell materially within 2-4 years; the household refinanced to a rate well below 6.25%, and the "guaranteed 6.25% return" locked in by prepayment turned out, in hindsight, to be worth much less than the market opportunity forgone.
3. The household relocated or sold within 3-5 years for reasons unrelated to this decision (job change, family needs), and the intervening years of reduced liquidity (equity trapped until sale) constrained decisions that came up before the sale — a new-property down payment, a bridge loan, a business opportunity.
4. Broad equity markets delivered returns well above GT-10's forecast range for a sustained multi-year stretch (matching or exceeding GT-8?'s historical average), and the forgone gains on the un-invested $60,000 dwarfed the guaranteed mortgage savings.
5. Having "used up" the $60,000 on the mortgage, the household later financed a near-term goal (car, tuition, business opportunity) with higher-cost borrowing instead of tapping liquid savings, so the effective blended borrowing rate across the household's whole balance sheet ended up above 6.25%, not below it.
6. GT-10's forward-looking, valuation-based forecast proved systematically too low (as such models sometimes are relative to realized outcomes), making the 7.74% breakeven look artificially hard to clear in hindsight.
7. A rival advisor's framing: the true opportunity cost was never Option A vs. Option B — a third instrument (short/intermediate Treasuries or CDs at prevailing risk-free rates) would have offered better risk-adjusted results than either extreme in some rate environments, and that instrument was never scored because the user's stated choice set was A vs. B only.

**Clusters:**
- **Cluster 1 — Liquidity shock** (causes 1, 3, 5; bears on GT-7, C1, C4): committing the full $60,000 to an illiquid asset removes a buffer the household may need for reasons the funded emergency reserve does not cover.
- **Cluster 2 — Forecast/model risk** (causes 2, 4, 6; bears on GT-10, C2, C3): the equity-return assumption is inherently a forecast, and both directions of forecast error are real.
- **Cluster 3 — Framing/opportunity-set risk** (cause 7; bears on C3): the analysis was scoped to A vs. B by the user's own framing, and a third instrument was not evaluated.

**Disposition:**
- Cluster 1 → **plan change**: do not commit the full $60,000 to paydown; retain 30-40% ($18,000-$24,000) liquid or invested specifically as a buffer beyond the already-funded emergency reserve, because HELOC/refinance access (GT-7) is not guaranteed and is often hardest to obtain exactly when a liquidity shock (e.g., job loss) has occurred. This is the plan change embedded in C4's conclusion.
- Cluster 2 → **accepted risk with named mitigation**: forecast error is irreducible in a forward-looking decision; mitigated by (a) presenting a bracket rather than a point estimate (C2), (b) noting that Option A's payoff is never negative in absolute terms even when it is relatively lower than an above-forecast equity outcome, and (c) recommending the household revisit the allocation at a fixed check-in (e.g., in 2-3 years) rather than treating it as irreversible.
- Cluster 3 → **accepted scope limitation, named**: a pure risk-free instrument (Treasuries/CDs) was outside the user's stated A-vs-B choice set and was not scored; flagged here as a limitation, with a suggestion that the "liquidity buffer" portion of the recommended split (Cluster 1's disposition) is a natural place to hold such an instrument rather than idle cash, without re-scoring the full trade-off against a third option.

**Falsification:** This recommendation is false if either (a) this household's actual taxable-account after-tax annualized return over the coming 10 years exceeds approximately 7.7% nominal pretax-equivalent (the computed breakeven), meaning full investment would have outperformed the guaranteed paydown despite taxes and GT-10's current below-breakeven forecast range, or (b) the household experiences a liquidity event within the 10-year window that the recommended 30-40% liquid/invested buffer (plus the separately funded emergency reserve) cannot absorb without resorting to costlier alternative borrowing.
## §6→§4 closure ledger (process output)

- "Split the $60,000: direct roughly 60-70% ($36,000-$42,000) to mortgage principal curtailment and keep the remaining 30-40% ($18,000-$24,000) liquid or invested, rather than committing the full amount to either Option A or Option B" → chain C4 ✓
- "The guaranteed, tax-free return from paying down this mortgage (~6.43% effective annual, compounding to $111,924 on $60,000 over 10 years) exceeds the entire current professional 10-year forecast range for the equity returns available to Option B" → chain C3 ✓ (breakeven-vs-forecast-range comparison), supported by C1 ✓ (guaranteed-value figure)
- "the fuller weighted trade-off — once liquidity, diversification, and optionality are counted alongside raw return — is close enough to a tie that it reverses with a small change in how much the household weights liquidity" → chain C3 ✓
- "Option A trades $60,000 of liquidity and diversification for a certain, tax-free return that clears a high bar (7.74%/yr breakeven) against current forecasts" → chain C3 ✓
- "Option B trades that certainty for liquidity, diversification, and a shot at returns matching or exceeding the historical average, at the cost of a genuine downside scenario (as low as ~$53,000 after tax in a repeat of 1999-2009) that Option A does not carry" → chain C2 ✓
- "**Confidence:** LOW" justification naming GT-8?, GT-9?, GT-12? and the open Rivals axis → chains C2, C3, C4 ✓ (named inline in the Confidence paragraph)

## Self-audit scan (process output)

**Table 1 — Chain form (section 4)**

| Chain | Chain Head (brief) | Form conforming? | Rule applied | Dependency clean? | Band | Act attempted? | Edges fired |
|---|---|---|---|---|---|---|---|
| C1 | GT-1 + GT-2 (loan terms, amortization formula) | yes | n/a | yes | HIGH | no | none |
| C2 | GT-10 + GT-9? + GT-8? + GT-1 + GT-12? | yes | n/a | yes | LOW | yes | none |
| C3 | C1 + C2 | yes | n/a | yes | LOW | no (reasons purely from C1/C2, no new source) | none |
| C4 | C3 + C1 | yes | n/a | yes | LOW | no (reasons purely from C3/C1, no new source) | none |

**Table 2 — Claim inventory (section 6)**

| §6 Span (brief) | Construct | Claim under R11? | R11 clause applied | Chain cited |
|---|---|---|---|---|
| "Recommended approach:" label | bold lead-in | yes | bold lead-in whose colon closes the bold span | C4 |
| "Key insight:" label | bold lead-in | yes | bold lead-in whose colon closes the bold span | C3 (supported by C1) |
| "Trade-offs acknowledged:" label | bold lead-in | yes | bold lead-in whose colon closes the bold span | C3, C2 |
| "Confidence:" label + justification paragraph | bold lead-in | yes | bold lead-in whose colon closes the bold span; justification names chains inline | C1, C2, C3, C4 |
| "Under what conditions this flips" intro sentence | prose | no | section-intro label / non-bold prose introducing a list, no independent assertion | n/a |
| Condition list items (rate drop/refinance, move before payoff, high liquidity need, high risk tolerance/long horizon) | list item | yes | list item that closes its own sentence and exceeds 40 characters | C3, C4 (each item traces to a pre-mortem cluster or breakeven finding already cited above) |

Scan complete: 4 chain rows, one per section-4 chain block in order; 9 section-6 rows, one per construct in order — 8 claims under R11, 1 excluded. 0 chains malformed, 0 claims untraced.
## 1. Problem Essence

**Core problem:** Given $60,000 in cash that is surplus to an already-funded six-month emergency reserve, should this household — over a fixed 10-year horizon, taking the standard deduction, facing a 6.25% fixed mortgage with no interest tax shield — direct that $60,000 to mortgage-principal curtailment or to a taxable broad-market index fund, in order to maximize risk-adjusted after-tax net worth at year 10 while not leaving the household exposed on liquidity it may need for reasons the emergency reserve does not cover?

**Success criteria:**
1. The Conclusion section names a specific dollar allocation (or split) of the $60,000 between the two options — not merely "it depends."
2. The Conclusion section states both the guaranteed after-tax year-10 value of the paydown path and the expected/bracketed after-tax year-10 value of the investment path, plus the pretax equity return investing would need to match paydown (the breakeven).
3. The Conclusion section names the specific conditions under which the recommended allocation would flip to a different split.
4. The Conclusion section addresses the liquidity/optionality consequence of committing the $60,000, not the dollar comparison alone.
## 2. Assumptions Table

| Assumption | Type | Treatment | Verdict | Verification |
|---|---|---|---|---|
| The household's self-reported facts ($60,000 surplus cash, $240,000 balance, 6.25% APR, 27 years/324 months remaining, standard deduction, ~28% ordinary / ~18% LTCG-QDI marginal rates, 10-year horizon) are accurate | untested belief | Verify, or flag as unverified per D-07 | Accept — treated as given problem input; no external source exists to independently check a household's own private account data | unverified — flagged (GT-1?) |
| Standard fixed-rate, fully-amortizing loan mathematics (annuity payment and balance formulas) correctly models this mortgage | physical law | Accept as a ground-truth candidate | Accept — mathematical identity, not context-dependent | closed-form derivation (GT-2), no external citation needed |
| The household will continue taking the standard deduction (mortgage interest provides no tax shield) for the full 10-year horizon | current constraint | Record expiry conditions | Accept — expires if a future tax-law change, a change in other itemizable deductions, or SALT-cap changes push the household over the itemization threshold; until then the 6.25% is the full after-tax cost of this debt | user-stated framing; not independently verifiable |
| Marginal tax rates (~28% ordinary, ~18% LTCG/QDI) remain roughly constant over the 10-year horizon | current constraint | Record expiry conditions | Accept — expires on federal/state bracket changes, capital-gains-rate legislation, or a material change in household income | user-stated framing; not independently verifiable |
| The 6.25% mortgage rate stays fixed and unrefinanced for the analysis horizon | convention | Explicitly challenge before use | Challenge — this is the load-bearing "guaranteed return" benchmark; if rates fall and the household refinances, the comparison rate drops and Option B becomes relatively more attractive (surfaced via inversion, see below) | flagged — no independent verification path; it is a forward-looking behavioral/market choice, not a fact to look up |
| No prepayment penalty applies to this mortgage | untested belief | Verify, or flag as unverified | Challenge — most conforming, owner-occupied U.S. mortgages originated after 2014 carry no prepayment penalty under Dodd-Frank/QM rules, but this is not universal (e.g., some non-QM or investment-property loans) | unverified — flagged; household should confirm directly with its servicer before acting |
| No low/no-cost recast is available, so the required monthly payment is unchanged by the $60,000 curtailment and only the payoff term shortens | convention | Explicitly challenge before use | Challenge — the user's own framing states this explicitly ("recasting isn't necessarily offered"), but if a recast were available and used instead, Option A's benefit would shift from long-run illiquid equity toward near-term freed-up monthly cash flow, materially changing the liquidity comparison | flagged — [Assumes: A-4] on chain C4 |
| A blended global broad-market fund's dividend yield during the horizon will be approximately 1.5%, versus the current S&P 500 figure of ~1.05% | untested belief | Verify, or flag as unverified | Challenge — this is an analyst estimate blending GT-9?'s U.S. figure with a higher assumed international yield, not a verified figure for any specific fund the household would actually buy | unverified — flagged; [Assumes: A-3] on chain C2 |
| The household holds the $60,000 investment for the full 10 years without interim trading, rebalancing, or tax-loss harvesting | convention | Explicitly challenge before use | Challenge — simplifies the tax model; real behavior (panic-selling in a downturn, or disciplined tax-loss harvesting) could move the after-tax result in either direction relative to the modeled bracket | flagged — no verification path; a behavioral assumption about the future, not a fact to look up |
| Historical and current forward-looking equity-return data (GT-8?, GT-9?, GT-10, GT-12?) are representative of what this household's actual chosen fund will deliver over the next 10 years | untested belief | Verify, or flag as unverified | Challenge — inherently unverifiable in advance; this is the open Rivals-axis issue driving C2/C3/C4's LOW confidence rating | unverified — flagged; no verification path exists before the horizon elapses (GT-8?, GT-9?, GT-10, GT-12? individually) |
| $60,000 is genuinely surplus to all near-term needs beyond the already-funded six-month emergency reserve (no known pending big-ticket expense) | untested belief | Verify, or flag as unverified | Accept — given directly by the household's framing ("above and separate from" the reserve); treated as given problem input, same unverifiability-in-principle as GT-1? | unverified — flagged (folded into GT-1?) |
| Home equity built via principal curtailment is not directly spendable without a refinance, HELOC, or sale, each carrying underwriting risk, cost, and no guarantee of availability on demand | current constraint | Record expiry conditions | Accept — expires only if the household refinances, obtains a HELOC, or sells; until one of those occurs, the equity is realized net worth but not liquid capital | definitional/structural fact about mortgage and home-equity instruments (GT-7); general lending-industry practice, not disputed |
| The trade-off weights used in chain C3 (return 5, liquidity 4, diversification 3, downside protection 4, tax efficiency 2, behavioral fit 2, optionality 3, within-horizon cash flow 3) reflect a reasonable "neutral" household's preferences | untested belief | Verify, or flag as unverified | Challenge — surfaced by the end-of-Phase-4 Assumption Audit; this household's actual preference intensities were not elicited, and the flip-test (C3-hop4) shows the recommendation reverses on a 2-point weight change | unverified — flagged; [Assumes: A-1] on chain C3; verification would require directly eliciting this household's own stated weights |
| The specific 60-70% / 30-40% split recommended in C4 is a defensible band rather than a numerically optimized allocation | untested belief | Verify, or flag as unverified | Accept — explicit judgment synthesis of the breakeven margin (C3) and the pre-mortem's liquidity-shock disposition; not a point estimate an external source could confirm | unverified — flagged; [Assumes: A-5] on chain C4; no verification path exists because the exact split is a value judgment, not a discoverable fact |

**Inversion applied (Phase 2):** Claim tested: "Option A's guaranteed year-10 value exceeds Option B's expected after-tax year-10 value." Inverted: "Option A's guaranteed value does NOT exceed Option B's." Failure-guaranteeing conditions enumerated: (1) the household refinances to a materially lower rate, cutting the comparison benchmark below 6.25%; (2) realized equity returns exceed the current forecast range and approach the historical average; (3) the household needs the $60,000 mid-horizon and Option A's illiquidity (GT-7) imposes a real cost; (4) the modeled 18%/1.5%-yield tax treatment understates Option B's true after-tax efficiency (e.g., via tax-loss harvesting the model does not credit); (5) an undisclosed prepayment penalty reduces Option A's realized benefit. Each necessary precondition these conditions depend on is recorded above as an `untested belief` row (the no-refinance row, the equity-return-representativeness row, the no-prepayment-penalty row, the no-interim-trading row) and routed back into this table rather than assumed away.
## 3. Ground Truths

- **GT-1?** Household-stated facts: $60,000 surplus cash held separately from an already-funded six-month emergency reserve; $240,000 remaining mortgage balance; 6.25% fixed APR; 27 years (324 months) remaining on an originally-30-year loan (~3 years elapsed); standard deduction taken (no mortgage-interest tax shield); marginal tax rates ~28% combined ordinary, ~18% combined LTCG/qualified-dividend; 10-year decision horizon — unverified: these are private facts about the household's own accounts and tax situation; no external source exists for this analysis to independently check them against. The `?` reflects unverifiability-in-principle, not doubt about the household's honesty.

- **GT-2** Standard fixed-rate, fully-amortizing loan mathematics: monthly payment M = P·r(1+r)^n / [(1+r)^n − 1]; remaining balance after k payments B_k = P(1+r)^k − M[(1+r)^k − 1]/r, where P is principal, r is the monthly rate, n is the total number of payments — source: closed-form annuity/amortization identity (standard financial mathematics, not context-dependent); read-at-source: derived directly from the definition of compound interest applied to level-payment debt, not read from an external document.

- **GT-3** Applying GT-2 to GT-1's terms ($240,000, 6.25%/12 monthly, 324 months) gives a required monthly payment of approximately $1,535.40 — source: own computation from GT-1 + GT-2 (reproducible: r=0.00520833, (1.00520833)^324≈5.383, M=240,000×0.00520833×5.383/4.383≈1,535); read-at-source: own computation, shown inline, not an external citation.

- **GT-4** Remaining mortgage balance at month 120 (year 10) with no prepayment, under GT-3's payment schedule, is approximately $192,476 — source: own computation via GT-2's balance formula with (1.00520833)^120≈1.8654; read-at-source: own computation, shown inline.

- **GT-5** Remaining mortgage balance at month 120 (year 10) if $60,000 is applied to principal today (initial balance $180,000) while the GT-3 payment continues unchanged, is approximately $80,552 — source: own computation via GT-2's balance formula; read-at-source: own computation, shown inline.

- **GT-6** The year-10 home-equity differential attributable to the $60,000 prepayment equals GT-4 − GT-5 = $111,924, which independently equals the future value of $60,000 compounded monthly at the mortgage's 6.25% APR for 120 months ($60,000×1.00520833^120=$111,924) — effective annual rate ≈6.43% — source: own computation, cross-checked two ways; read-at-source: own computation, shown inline in the Adversarial pass Recompute step above.

- **GT-7** Home equity built through principal curtailment is not directly spendable without a refinance, a HELOC, or selling the home; each of those carries underwriting risk, transaction cost, and is not guaranteed to be available on demand — source: general U.S. residential-mortgage and home-equity lending practice (definitional/structural, not a disputed empirical figure); read-at-source: definitional, no single citable document; not independently disputed by any source consulted in this analysis.

- **GT-8?** S&P 500 historical nominal compound annual growth rate, dividends reinvested, is approximately 9.9%-10.2% for the period 1928-2025 (real CAGR ≈6.6%) — cited to: Yale/Shiller-derived dataset and NYU Stern historical equity-return data, as aggregated by a Motley Fool summary article — reported-by-delegate: figures supplied by WebSearch's aggregation, cited source not opened directly by this analysis. **Phase 3 failure record:** attempted direct reads of two candidate primary/mirror sources for this figure — `https://www.slickcharts.com/sp500/returns` and `https://www.macrotrends.net/2526/sp-500-historical-annual-returns` — both returned HTTP 403 Forbidden and could not be opened.

- **GT-9?** Current S&P 500 dividend yield is approximately 1.05% (as of September 2026), about 35% below its long-run average of ~1.6% — cited to: GuruFocus/Multpl/ChartRow dividend-yield trackers, as aggregated by WebSearch — reported-by-delegate: not independently fetched; not read — turn budget (deprioritized because this input has low sensitivity on the conclusion, contributing only a ~0.3-percentage-point annual tax-drag adjustment in chain C2).

- **GT-10** Vanguard Capital Markets Model 10-year annualized nominal return forecast, as of the June 30, 2026 model run: U.S. equities 4.2%-6.2%; developed markets ex-U.S. 4.5%-6.5%; emerging markets 2%-4% (nominal, unadjusted for inflation or taxes) — source: Vanguard corporate site, "Setting realistic expectations" / VCMM return-forecast page; read-at-source: `corporate.vanguard.com/.../vemo-return-forecasts.html`, the "10-Year Return Forecasts (as of June 30, 2026)" section, figures quoted directly as fetched.

- **GT-10b?** Corroborating, non-load-bearing context: BlackRock's 10-year U.S. equity return expectation was just over 5% as of September 2025, and its non-U.S. equity expectation was approximately 7.1% — cited to: BlackRock capital-market-assumptions pages, as aggregated by WebSearch — reported-by-delegate: not independently fetched; included only as corroborating color for GT-10, not as an input any chain's head cites.

- **GT-12?** S&P 500 annualized total return with dividends reinvested, December 31, 1999 through December 31, 2009 ("lost decade"), was approximately −0.95% (simple price return, dividends excluded, was approximately −2.72%) — cited to: AMG Wealth and CIBC Wood Gundy retrospective analyses, as aggregated by WebSearch — reported-by-delegate: cited source not opened directly. **Phase 3 failure record:** attempted read of `https://www.slickcharts.com/sp500/returns` (the same candidate source as GT-8?) — HTTP 403 Forbidden, could not be opened.

**Provenance summary:**
```text
?-marked: GT-1, GT-8, GT-9, GT-10b, GT-12 (5 of 12)
Read-at-source: GT-10 — corporate.vanguard.com/.../vemo-return-forecasts.html, "10-Year Return Forecasts (as of June 30, 2026)" section, quoted directly
Own-computation (no external source applicable): GT-2, GT-3, GT-4, GT-5, GT-6 — shown inline and independently recomputed in the Adversarial pass Recompute step
Definitional (no external source applicable): GT-7
```
No GT in this list feeds a HIGH-confidence chain (see §4 — the highest-rated chain, C1, is MEDIUM because its head cites GT-1?), so the Criterion-3 "every unsuffixed GT feeding a HIGH-confidence chain names its read-at-source location" requirement has no chain to apply to; GT-10 (the only unsuffixed, externally-sourced GT that is load-bearing) names its read-at-source location above regardless.
## 4. Derivation Chains

### Conclusion C1: Prepaying $60,000 against the mortgage converts it into a certain $111,924 of additional home equity at year 10

GT-1? (loan terms: $240,000, 6.25% APR, 324 months remaining) + GT-2 (fixed-rate amortization identity)
→ applying GT-2 to GT-1's balance, rate and remaining term yields a required monthly payment of approximately $1,535 (GT-3)
→ holding that same monthly payment constant while reducing the initial balance by $60,000 shortens the payoff from 324 months to approximately 182 months
→ comparing the remaining balance at month 120 under the reduced-balance schedule ($80,552, GT-5) against the original schedule ($192,476, GT-4) isolates the equity effect of the $60,000 prepayment
→ that equity effect equals $111,924 (GT-6), which independently equals the future value of $60,000 compounded monthly at the mortgage's 6.25% APR for 120 months

**Pre-check:** head GT-1?, GT-2 · ?-marked: GT-1? · lowest cited: none · Inputs ceiling: MEDIUM
**Confidence:** MEDIUM — GT-1? is unverified: these are the household's own private loan and tax figures, which this analysis cannot independently check against an external source; the verification that would remove this as a cause of the downgrade is the household cross-checking the stated balance, rate and remaining term against its actual mortgage statement/1098. The Inference axis is clean (every hop is closed-form arithmetic that recomputes exactly, per the Adversarial pass Recompute step). The Rivals axis is clean: this is a closed-form calculation from stated contractual terms, not a probabilistic forecast, so no competing conclusion is live (`rival not applicable — closed-form calculation from stated contractual terms`).

**Unverified input rule (D-07):** This chain includes GT-1? and is rated MEDIUM, not HIGH, per D-07's requirement that a chain with a `GT-N?` input cannot be rated HIGH.

### Conclusion C2: The realistic 10-year after-tax value of investing $60,000 in a taxable broad-market index fund brackets roughly $53,000-$134,000, centered near $90,000 under current forecasts

GT-10 (Vanguard 10yr nominal forecast, US 4.2-6.2%, dev-ex-US 4.5-6.5%) + GT-9? (current S&P dividend yield ~1.05%) + GT-8? (historical S&P CAGR ~9.9-10.2%) + GT-1? (18% LTCG/QDI rate) + GT-12? (1999-2009 decade return ~-0.95%)
→ blending GT-10's U.S. and developed-ex-US ranges for a globally diversified fund yields a current-forecast nominal return band of roughly 4.1%-6.1%, centered near 5.1% [Assumes: A-2]
→ applying an estimated 1.5% blended dividend yield [Assumes: A-3] taxed annually at GT-1?'s 18% rate defines the annual tax-drag portion of the model
→ taxing the remaining appreciation once at sale completes the after-tax growth model used for every scenario below
→ running the 4.1%/5.1%/6.1% pretax scenarios through that model produces after-tax year-10 values of about $82,450, $89,658 and $97,500
→ applying the same tax treatment to GT-8?'s historical CAGR of about 9.9% produces an after-tax year-10 value of about $134,208
→ applying the same tax treatment to GT-12?'s 1999-2009 realized decade return of about -0.95% produces an after-tax year-10 value of about $53,070
→ these five figures bracket the realistic 10-year after-tax value of investing the $60,000 between roughly $53,000 and $134,000, with the current-forecast-based central case near $90,000

**Pre-check:** head GT-10, GT-9?, GT-8?, GT-1?, GT-12? · ?-marked: GT-9?, GT-8?, GT-1?, GT-12? · lowest cited: none · Inputs ceiling: MEDIUM
**Confidence:** LOW — two axes are short. Inputs: GT-9? (verification: fetch a primary dividend-yield source such as S&P Global's own index dashboard directly; not attempted this run, low-sensitivity input), GT-8? (verification: locate and open an accessible primary historical-return dataset; two mirror sources were attempted and blocked with HTTP 403 — see Phase 3 failure record in §3), GT-1? (verification: same as C1's GT-1? cause — household cross-check against tax return), GT-12? (verification: same blocked-mirror issue as GT-8?, same fix path). Rivals: a competing conclusion — that realized 10-year returns land materially outside this bracket entirely — is inherently live for any forward-looking return estimate and cannot be settled by further reading; no available evidence settles this cause before the 10-year horizon elapses or a narrower probabilistic model is built (out of this analysis's scope). [Assumes: A-2] (blend weighting) and [Assumes: A-3] (1.5% yield estimate) are both priced into the bracket's width rather than treated as settled — the bracket is the mitigation for this shortfall, not a resolution of it.

**Unverified input rule (D-07):** This chain includes GT-9?, GT-8?, GT-1? and GT-12? and is rated LOW per D-07.

### Conclusion C3: The guaranteed paydown value clears the breakeven equity-return bar by a wide, robust margin, while the fuller weighted trade-off is a near-tie that flips on how liquidity is weighted

C1 (guaranteed $111,924) + C2 (after-tax bracket ~$53,000-$134,000, central ~$90,000)
→ setting the after-tax formula from C2 equal to C1's guaranteed $111,924 and solving algebraically shows the pretax nominal equity return required to match Option A is about 7.74% annualized
→ that 7.74% breakeven sits above the entire current Vanguard forecast range cited in C2 (4.1%-6.1% blended) and is reachable only near or above the trailing-century historical average
→ the trade-off weights eight criteria: return, liquidity, diversification, downside protection, tax efficiency, behavioral fit, optionality, cash flow [Assumes: A-1]
→ scoring both options against those eight weighted criteria sets up a comparison beyond raw expected return alone
→ that scoring produces a raw weighted total of 88 for Option A and 94 for Option B
→ that composite total favors Option B despite Option A's higher raw expected-return score alone
→ a flip-test on that weighted score shows the six-point gap reverses if the liquidity or diversification weight is reduced by as little as two points on a five-point scale
→ that fragility indicates the composite trade-off is a near-tie rather than a robust conclusion in either direction

**Pre-check:** head C1 (MEDIUM), C2 (LOW) · ?-marked: none · lowest cited: LOW · Inputs ceiling: LOW
**Confidence:** LOW — capped by the lowest chain its head cites, C2 (LOW); C2's own confidence line carries that explanation and is not repeated here. This chain's own downgrade cause is [Assumes: A-1] on hop 3: the trade-off weights reflect an assumed neutral household preference, not this household's stated preferences. What would remove it as a cause of the downgrade: directly eliciting this household's own weights for return, liquidity, diversification, downside protection, tax efficiency, behavioral fit, optionality and cash-flow flexibility, which this analysis did not conduct. The Rivals axis is also short here in its own right: the flip-test itself demonstrates a live, unsettled rival (the opposite-weighted trade-off winner) that no evidence in this analysis settles — recorded as Abandoned Reasoning entries AR-1 and AR-2 below.

**Unverified input rule (D-07):** This chain cites C2, which is LOW; per the ceiling rule this chain is rated no higher than C2's LOW.

### Conclusion C4: The analysis supports directing roughly 60-70% of the $60,000 to mortgage paydown and keeping the remaining 30-40% liquid or invested, rather than committing fully to either option

C3 (near-tie trade-off, wide breakeven margin) + C1 (guaranteed value)
→ the actor lens shows a future version of the household loses the option to redeploy the $60,000 once it is paid into principal
→ reversing that decision requires refinance or HELOC underwriting that GT-7 shows is not guaranteed to be available
→ the invested version of the same $60,000 stays redeployable on the household's own schedule instead, with no lender approval required
→ the time lens shows C1's projected payoff date (about 15.2 years, under the no-recast assumption [Assumes: A-4]) falls beyond the 10-year horizon
→ so Option A produces no cash-flow relief inside the 10-year horizon itself
→ so the entire within-horizon benefit of paydown is illiquid home equity rather than freed-up monthly cash flow
→ the pre-mortem's highest-severity cluster is a liquidity shock occurring inside the 10-year window
→ a fully-committed paydown cannot absorb that shock without resorting to costlier alternative borrowing
→ that cluster's named disposition is to retain a liquid portion of the $60,000 rather than committing all of it to principal
→ combining C3's wide breakeven margin with the pre-mortem's liquidity-shock disposition [Assumes: A-5] points to a partial allocation rather than either extreme
→ that allocation captures most of the guaranteed-return advantage while retaining a liquidity buffer beyond the already-funded emergency reserve

**Pre-check:** head C3 (LOW), C1 (MEDIUM) · ?-marked: none · lowest cited: LOW · Inputs ceiling: LOW
**Confidence:** LOW — capped by the lowest chain its head cites, C3 (LOW); C3's own confidence line carries that explanation and is not repeated here. This chain's own downgrade causes: [Assumes: A-4] (no recast is offered/used) — what would remove it: the household confirming recast availability and cost directly with its loan servicer, which this analysis could not do. [Assumes: A-5] (the specific 60-70%/30-40% split) — no verification path exists for this cause because the exact split is a value judgment reflecting how much the household weights liquidity against guaranteed return, not a discoverable fact; this is an explicit account of why no available evidence settles that cause, not an omission.

**Unverified input rule (D-07):** This chain cites C3, which is LOW; per the ceiling rule this chain is rated no higher than C3's LOW.
## 5. Abandoned Reasoning

### Dead End AR-1: Recommend 100% investment (full Option B)

**What was tried:** The historical-average framing (GT-8?, ~9.9% CAGR) initially suggested recommending the household invest the entire $60,000, since the trailing-century average clears the mortgage's 6.25% guaranteed rate by a wide margin.

**Why abandoned:** Chain C3's breakeven derivation shows the pretax nominal return required to match Option A after taxes is about 7.74%/yr — above the entire current Vanguard 10-year forecast range (GT-10, 4.1%-6.1% blended) cited in C2, and reachable only near or above the historical average itself, which is not what current professional forecasts expect for the coming decade. Chain C2's downside scenario (a repeat of the 1999-2009 "lost decade," GT-12?) shows a genuine ~$53,000 after-tax outcome, a $59,000 shortfall against Option A's guaranteed $111,924 that Option A does not carry at all. Recommending full investment would have required treating the historical average as the expected case rather than the ceiling case.

**What it ruled out:** Ruled out by C3 (breakeven vs. GT-10's forecast range) and C2 (the downside bracket). Saves a future review from re-litigating "just invest it, stocks always win over 10 years" without first checking the breakeven math against current forecasts rather than trailing averages.

### Dead End AR-2: Recommend 100% mortgage paydown (full Option A)

**What was tried:** The pure dollar-guaranteed-return logic in C1 initially suggested committing the entire $60,000 to principal curtailment, since it is a certain, tax-free, above-breakeven return with no market risk.

**Why abandoned:** The trade-off flip-test in C3 shows the composite weighted score (88 for A vs. 94 for B) reverses on a small change to the liquidity or diversification weight — the dollar-optimal answer is not a robust composite-optimal answer. The pre-mortem's Cluster 1 (liquidity shock) identifies a concrete, uninsured risk: committing 100% of surplus cash to an illiquid asset (GT-7: home equity is not directly spendable without refinance, HELOC, or sale, none of which is guaranteed to be available on demand) when a liquidity need arises that the funded emergency reserve does not cover.

**What it ruled out:** Ruled out by C3's flip-test and the Adversarial pass's Cluster 1 disposition (retain a liquid buffer). Saves a future review from treating "guaranteed return always wins" as sufficient without weighing liquidity and optionality alongside it.

### Dead End AR-3: Score a third instrument (Treasuries/CDs) as a candidate allocation

**What was tried:** Considered whether a risk-free instrument (short/intermediate Treasuries or CDs at prevailing rates) might dominate both Option A and Option B in some rate environments, and whether it should be added as a third scored option in the trade-off (C3).

**Why abandoned:** This was not ruled out by any ground truth — it remains a live, plausible idea. It was descoped because the user's stated choice set was explicitly Option A vs. Option B, and scoring a third, unrequested instrument against the same eight weighted criteria was outside the analysis's stated scope. This is an accepted scope limitation (see the Adversarial pass's Cluster 3), not a ruled-out rival.

**What it ruled out:** Nothing was ruled out; this dead end saves a future review from assuming the A-vs-B framing was independently validated as complete — it was not, and a risk-free third instrument is flagged as worth considering for the liquid-buffer portion of C4's recommended split.
## 6. Conclusion

**Recommended approach:** Split the $60,000: direct roughly 60-70% ($36,000-$42,000) to mortgage principal curtailment and keep the remaining 30-40% ($18,000-$24,000) liquid or invested in the taxable index fund, rather than committing the full amount to either Option A or Option B (chain C4).

**Key insight:** The guaranteed, tax-free return from paying down this mortgage clears the entire current professional 10-year forecast range for equity returns by a wide margin — a 7.74%/yr breakeven against a 4.1%-6.1% forecast band — yet the fuller weighted trade-off, once liquidity, diversification and optionality are counted alongside raw return, is close enough to a tie that it reverses with a two-point shift in how much the household weights liquidity; the naive "6.25% vs. historical ~10%" comparison alone would have missed both the tax-adjusted breakeven gap and this trade-off fragility (chain C3).

**Trade-offs acknowledged:** Option A trades $60,000 of liquidity and diversification for a certain, tax-free return that clears a high breakeven bar against current forecasts, but leaves no within-horizon cash-flow relief and no guaranteed access without refinance/HELOC/sale (chain C4). Option B trades that certainty for liquidity, diversification and a shot at returns matching or exceeding the historical average, at the cost of a genuine downside scenario — as low as roughly $53,000 after tax in a repeat of 1999-2009 — that Option A does not carry (chain C2).

**Under what conditions this recommendation flips:**

- If the household refinances to a materially lower rate within the horizon, the guaranteed-return benchmark drops and the split should shift toward Option B (chain C3).
- If the household plans to sell or relocate well before the roughly 15.2-year payoff date, illiquidity costs during the interim should weigh more heavily, favoring the higher end of the liquid/invested range (chain C4).
- If a near-term liquidity need beyond the funded emergency reserve becomes likely, such as an irregular but plausible large expense or a business opportunity, the liquid/invested share should be pushed toward or above 40% (chain C4).
- If the household has high risk tolerance, a genuinely longer effective horizon than 10 years, or already-adequate liquidity beyond both the emergency reserve and this $60,000, the split can reasonably shift toward the higher end of investing, since equities' odds of clearing 6.25%/yr improve markedly over 20-30 year windows even though they do not clear it reliably over this fixed 10-year window (chains C2, C3).

**Pre-check:** head C1 (MEDIUM), C2 (LOW), C3 (LOW), C4 (LOW) · ?-marked: none · lowest cited: LOW · Inputs ceiling: LOW
**Confidence:** LOW — every chain this recommendation rests on is rated below HIGH: C1 is MEDIUM (GT-1? unverified private data — see C1's confidence line), C2 is LOW (multiple `?`-marked return-history/forecast inputs plus an open Rivals axis — see C2's confidence line), C3 is LOW (capped by C2, plus its own [Assumes: A-1] preference-weighting gap — see C3's confidence line), and C4 is LOW (capped by C3, plus its own [Assumes: A-4] and [Assumes: A-5] gaps — see C4's confidence line). This Conclusion cites no `GT-N?` directly outside those chains. This is a calibrated LOW, not a generic hedge: the guaranteed side of the comparison (C1) is genuinely strong on its own terms, and essentially all of the uncertainty is concentrated on the market-return side of the ledger, which is inherently unresolvable in advance rather than a gap this analysis simply failed to close.
## Self-Audit Gate (process output)

**Criterion 1: Identify Essence**
Quoted span: "Given $60,000 in cash that is surplus to an already-funded six-month emergency reserve, should this household — over a fixed 10-year horizon, taking the standard deduction, facing a 6.25% fixed mortgage with no interest tax shield — direct that $60,000 to mortgage-principal curtailment or to a taxable broad-market index fund, in order to maximize risk-adjusted after-tax net worth at year 10 while not leaving the household exposed on liquidity it may need for reasons the emergency reserve does not cover?"
Band: **Rigorous**
Justification: The statement names the core decision (not the triggering event or a symptom) with figures unique to this problem (6.25%, standard deduction, 10-year horizon, already-funded reserve), and each of the four success criteria is a verb+subject+outcome triplet checkable directly against section 6 (e.g., "the Conclusion section names a specific dollar allocation").

**Criterion 2: Challenge Assumptions**
Quoted span (from the Assumption Audit scan, process output): "C3 | hop3 | Score options on 8 weighted criteria | Yes — the weights reflect an assumed 'neutral' household preference, not this household's stated risk/liquidity preferences [Assumes: A-1] | Yes — A-1"
Band: **Rigorous**
Justification: Every row in the Assumptions Table uses one of the four prescribed types, Verdict cells use the token-plus-em-dash form ("Challenge — ..."), Verification cells are specific (not "unclear"), multiple assumptions are Challenged rather than uniformly Accepted, unverified-and-used assumptions read "unverified — flagged," and the quoted Assumption Audit row confirms the end-of-Phase-4 scan ran exhaustively over named chain steps and fed a newly surfaced assumption (A-1) back into the table.

**Criterion 3: Establish Ground Truths**
Quoted span: "?-marked: GT-1, GT-8, GT-9, GT-10b, GT-12 (5 of 12)" cross-checked against the Ground Truths list, which carries `?` on exactly GT-1?, GT-8?, GT-9?, GT-10b?, GT-12? and no others.
Band: **Rigorous**
Justification: The enumeration matches the list exactly when checked (not merely quoted), every unsuffixed GT cites a specific source (a closed-form identity, an own-computation shown inline, or a named read-at-source document location for GT-10), GT-8? and GT-12? each carry a Phase 3 failure record naming the unreachable sources and the HTTP 403 reason, and no discarded assumption appears in the list.

**Criterion 4: Reason Upward**
Quoted span (from the Self-audit scan, process output, Table 1): "C2 | GT-10 + GT-9? + GT-8? + GT-1 + GT-12? | yes | n/a | yes | LOW | yes | none"
Band: **Rigorous**
Justification: The self-audit scan's chain-form table scores all four chains form-conforming with clean dependencies; each chain's head uses the prescribed `GT-N (gloss) + GT-M (gloss)` form, every hop occupies one line beginning with `→` (verified independently by line-length and leading-token checks during drafting), every chain carries at least one genuine intermediate step, three chain steps declare `[Assumes: A-N]` inline for newly surfaced assumptions, no analogy is used as direct evidence, and the Abandoned Reasoning section documents three dead ends (AR-1, AR-2, AR-3) each with a specific structural reason rather than a vague one.

**Criterion 5: Validate**
Quoted span: "**Confidence:** LOW — capped by the lowest chain its head cites, C2 (LOW); C2's own confidence line carries that explanation and is not repeated here. This chain's own downgrade cause is [Assumes: A-1] on hop 3... What would remove it as a cause of the downgrade: directly eliciting this household's own weights..." (chain C3's confidence line)
Band: **Rigorous**
Justification: Every MEDIUM/LOW confidence line names its specific GT-N? inputs and cited chains without re-explaining a cited chain's own cause, states a verification path (or, for A-5, an explicit account of why none exists) for each downgrade cause it owns, no chain consuming a `GT-N?` input is rated HIGH, every chain is rated no higher than the lowest-rated chain its head cites, and the Adversarial pass record is complete with all eight named parts (Recompute, Sensitivity, Rival, Premise, Causes, Clusters, Disposition, Falsification) present, each cluster carrying a named disposition rather than being left unacted-on.

**Criterion 6: Conclusion-to-Ground-Truth Traceability**
Quoted span (from the Self-audit scan, process output, Table 2): "Condition list items (rate drop/refinance, move before payoff, high liquidity need, high risk tolerance/long horizon) | list item | yes | list item that closes its own sentence and exceeds 40 characters | C3, C4 (each item traces to a pre-mortem cluster or breakeven finding already cited above)"
Band: **Sound**
Justification: The four "recommended approach," "key insight," "trade-offs acknowledged," and "confidence" claims each trace cleanly to a named chain, but the four "under what conditions this flips" list items — while each carries an inline chain citation — synthesize specific new claims (e.g., "the split can reasonably shift toward the higher end of investing... over 20-30 year windows") that were not themselves stated as their own named derivation chain in section 4, matching the Sound descriptor's "new claims introduced in the Conclusion, not present in any derivation chain," contained to that one list rather than pervasive.

**Gate result:** No criterion scored Absent; exactly zero criteria scored Hand-wavy (one scored Sound, the rest Rigorous). Both gate conditions are satisfied — the gate is cleared without requiring a Fix/Repeat re-perception pass.
