## Assumption Audit scan (process output)

One row per chain per step (hop), in document order. "Added to Table?" = `n/a` when no assumption is surfaced beyond what Phase 2 already lists; `n/a (already present)` when the step surfaces an assumption that Phase 2 already classified (so no new row is needed); `yes` would mark a genuinely new assumption first surfaced here (none occurred — this run's Phase 2 pass anticipated every assumption later load-bearing chain steps needed).

| Chain | Step | Step Text (brief) | Assumption surfaced? | Added to Table? |
|-------|------|-------------------|----------------------|-----------------|
| C1 | 1 | Lender credits extra principal at contract rate with certainty | none | n/a |
| C1 | 2 | Standard deduction means no interest avoided was ever tax-shielded | none (cites GT-7 directly) | n/a |
| C1 | 3 | Extra principal = riskless, tax-free 6.25% instrument, $110,012 FV | none | n/a |
| C2 | 1 | Breakeven pretax CAGR if sold at yr10 ≈ 7.8% | A-5 (tax-drag approximation) | n/a (already present) |
| C2 | 2 | Breakeven pretax CAGR if held/unsold ≈ 6.75% | A-5 (tax-drag approximation) | n/a (already present) |
| C2 | 3 | Dividend yield covers little of the breakeven; appreciation does the work | none (cites GT-18 directly) | n/a |
| C3 | 1 | Historical base rate maps to ~30% chance of missing the 7.8% breakeven | A-4 (historical distribution as forward proxy) `[Assumes: A-4]` | n/a (already present) |
| C3 | 2 | Expected value ($149k) exceeds median due to right-skew compounding | none | n/a |
| C3 | 3 | Synthesis: better expected value, real non-trivial shortfall risk | none | n/a |
| C4 | 1 | Recovering home equity requires a cost- or delay-bearing mechanism | none (cites GT-6, GT-15 directly) | n/a |
| C4 | 2 | Brokerage balance converts to cash in days at near-zero marginal cost | none | n/a |
| C4 | 3 | $60k is worth strictly more as brokerage optionality than as home equity | none | n/a |
| C5 | 1 | No recast means zero incremental monthly cash-flow protection from A | none (cites GT-6 directly) | n/a |
| C5 | 2 | Recast converts the lump sum to cash flow far slower than holding it liquid | none (cites GT-5 directly) | n/a |
| C5 | 3 | Neither path solves an unmet liquidity need now; B keeps full-value access | none (cites GT-10 directly) | n/a |
| C6 | 1 | A's outcome is capped at exactly 6.25% in every scenario | none | n/a |
| C6 | 2 | B's outcome ranges from a loss to several multiples of principal | none | n/a |
| C6 | 3 | A pure expected-value comparison understates the risk B asks the household to bear | none | n/a |
| C7 | 1 | No prepayment penalty means liquidity can convert into paydown later at zero cost | A-11 (no prepayment penalty) `[Assumes: A-11]` | n/a (already present) |
| C7 | 2 | (actor lens) The household, not a lender, controls when optionality closes | none | n/a |
| C7 | 3 | (time lens) The flexibility gap compounds visibly by year 5-10 | none | n/a |
| C7 | 4 | Preserving the option to choose A later beats committing to A now | none | n/a |
| C8 | 1 | Weighted trade-off totals: Invest=63, Paydown=57, Split=57 (of 85) | A-9, A-10 (liquidity value; behavioral discipline) `[Assumes: A-9, A-10]` | n/a (already present) |
| C8 | 2 | Invest's margin is driven almost entirely by the liquidity criterion | none | n/a |
| C8 | 3 | Flip test: liquidity weight 5→3.5 ties Invest with Paydown; no other single criterion ties it within range | none | n/a |
| C8 | 4 | Recommended approach: invest the $60k, held at LOW confidence | none | n/a |

Scan complete: 26 rows across 8 chains, no step skipped. Every surfaced assumption (A-4, A-5, A-9, A-10, A-11) was already present in the Phase 2 Assumptions Table before this scan ran; no new row was required.

## Techniques not applied (process output)

- fishbone — not applicable — the assumption space in Phase 2 was tractable by direct enumeration (loan mechanics, tax treatment, liquidity, behavior, second-order effects); it did not require category-based brainstorming to surface branches intuition could not reach.
- inversion — not applicable — the analysis's output is a recommended course of action (a plan: invest vs. pay down), which the decision rule in Step 0 routes to Pre-Mortem at Phase 5 instead of Inversion. Inversion's failure-enumeration role at Phase 2 was still exercised informally in spirit — Assumptions A-4, A-9 and A-10 were surfaced precisely by asking what would have to be true for the "invest wins" conclusion to fail — but the structured Inversion procedure itself was not run as a separate pass.

five-whys (reduce-to-primitives), estimate, theoretical-limit, trade-off, second-order, and pre-mortem were all applied: five-whys inline during Phase 3 (GT-1 reduces to the amortization identity, a mathematical definition, not a further-reducible claim); estimate in chains C2-C3 (unit-factor rebuild of the breakeven CAGR and the probability-weighted terminal value, bracketed); theoretical-limit implicitly in chain C6 (Option A's ceiling and floor are identical at 6.25% — there is no convention to strip, which is itself the finding); trade-off in chain C8 (the full weighted matrix); second-order in chain C7 (actor lens + time lens); pre-mortem in the adversarial pass record below.

## Adversarial pass (process output)

**Recompute.** GT-1 payment ($1,535.24), GT-2/GT-3 ten-year balances and interest ($192,615.95 / $136,844.35 baseline vs. $80,702.86 / $84,931.26 under Option A), GT-4 payoff timeline (182 vs. 324 months) and lifetime interest ($98,773.59 vs. $257,416.67), and GT-5 recast payment ($1,151.43) were all recomputed independently via direct amortization simulation (monthly loop, not a closed-form shortcut) rather than taken from the chain text, and matched the figures used in chains C1, C4 and C5. The breakeven pretax CAGRs in C2 (≈7.765% sold, ≈6.750% held) were recomputed by bisection on the after-tax FV equations rather than estimated. The C3 expected value ($149,361 sold-scenario) and shortfall probability (≈29.8% sold, ≈23.3% held) were recomputed from the stated four-bucket discrete distribution by direct summation and linear interpolation; both recomputations reproduced the figures used in the chains.

**Sensitivity.** The single ground truth whose falsity would most plausibly flip the conclusion is GT-12 (the 24%-below-7%/4%-negative historical base rate) — not because GT-12 itself is `?`-marked (it is read-at-source and is not), but because its *forward applicability* is Assumption A-4, which is explicitly flagged. If forward 10-year returns are structurally lower than the 1926-2025 sample (e.g., because current valuations are elevated), the honest direction of the error is that the ≈30% shortfall probability in C3 is an *underestimate*, not an overestimate — which would strengthen, not reverse, the case for caution, while leaving the median-expectation gap untouched in sign. The weakest link in each chain: C2 (two `?`-marked drag/yield inputs, one of which — GT-14 — has an unresolved Phase 3 failure record); C3 (inherits C2's cap and carries a live, unsettled valuation-adjusted rival); C7 (GT-17's unresolved Phase 3 failure record); C8 (the liquidity-weight judgment call, named explicitly in its own flip test).

**Rival.** Headline conclusion ("invest the $60k") — the strongest rival is "pay down the mortgage" (Option A), which the same ground truths support under a different, equally reasonable liquidity weighting; chain C8's own flip test is what settles (bounds, not eliminates) this rival: a 30% reduction in the liquidity weight ties it, and §5's "Dead End 2" entry rules out the 50/50 split as a dominant third option rather than a genuine rival. Chain C3 (expected value vs. shortfall risk) — the rival reading "forward returns will systematically undershoot this historical sample because current valuations are elevated" is live and is **not** settled by this analysis; see §5 "Dead End 1," which discloses rather than resolves this rival, which is why C3 is rated LOW rather than MEDIUM. Chain C6 (risk-adjusted asymmetry) has no live rival beyond the one C3 already carries — rival not applicable beyond C3's, since C6's own two hops are definitional restatements of C1 and C3's already-settled-or-disclosed content. Chain C4/C5 (liquidity and recast mechanics) — no live rival: these are direct readings of GT-6, GT-10, GT-15 with no competing interpretation offered anywhere in this analysis.

**Adversarial technique — Pre-Mortem** (the conclusion is a recommended course of action, a plan; Inversion is not used, per the decision rule in Step 0).

*Premise:* It is ten years from now. The household followed this analysis's recommendation and invested the $60,000 instead of paying down the mortgage. The plan has already failed to deliver what this analysis promised.

*Causes* (generated from the investor's, the future-self's, the lender/risk-manager's, the tax-authority's, and the household's own psychological viewpoints, unfiltered):
1. A genuine bad decade occurred (a repeat of 2000-2009 or worse) and the brokerage balance sits below what the guaranteed mortgage paydown would have delivered.
2. One or both spouses panic-sold near a market bottom, converting a temporary paper loss into a permanent realized one.
3. The liquid balance was gradually spent on discretionary purchases over the decade ("lifestyle creep"), eroding the principal long before any market thesis had a chance to play out.
4. A job-loss shock hit at the same time equities were down (a correlated recession scenario), forcing a sale at the worst possible moment to cover living expenses.
5. The 18%/28% tax-rate assumptions drifted — Congress raised long-term capital-gains rates, or the household's income growth pushed them into a higher bracket or the 3.8% NIIT — eroding more of the gain than modeled.
6. The household found living with a larger, longer-lived mortgage balance psychologically stressful, and impulsively paid it off anyway during a market downturn, crystallizing losses at the worst time and getting the discipline-benefit of Option A without ever having captured its guaranteed-return benefit.
7. The recommendation's own liquidity-weighting judgment call (A-9) was simply wrong for this household — they never actually used the optionality for anything, and paid real variance for a liquidity premium they didn't need.

*Clusters:*
- **Cluster A — Sequencing/correlated-shock risk** (causes 1, 4): bears on chains C3, C6, and GT-12/GT-13.
- **Cluster B — Behavioral execution risk** (causes 2, 3, 6): bears on chain C5, chain C8 (Assumption A-10), and Assumptions A-9/A-10 directly.
- **Cluster C — Tax/assumption drift** (cause 5): bears on GT-8, GT-9, chain C2.
- **Cluster D — Liquidity-value misjudgment** (cause 7): bears on chain C8 (Assumption A-9) directly.

*Disposition:*
- Cluster A — **costly but survivable, risk accepted with a named mitigation**: the household's separate, already-fully-funded six-month reserve (GT-10) is the buffer for a correlated shock, not the $60,000 itself; the $60,000 is explicitly not re-designated as emergency capital. Accepted risk: the ≈24-30% historical shortfall probability quantified in C3 is accepted as the price of the larger expected-value edge.
- Cluster B — **plan change (mandatory)**: before funding the brokerage account, adopt a written investment policy — a single broad low-cost index fund (not individual stocks), held in an account separate from day-to-day spending, with no discretionary withdrawals except for a pre-named purpose, and automatic (not discretionary) rebalancing only. Tripwire: any discretionary withdrawal for non-emergency spending within years 1-3 is the signal this is failing; if it occurs, treat Assumption A-10 (behavioral discipline) as falsified for this household and re-run chain C8 with a lower Behavioral score for Option B, which (per the flip test) combines with a lower liquidity weight to tip the recommendation toward Option A or the split.
- Cluster C — **accepted risk with a named mitigation**: accept that 10-year-old tax-rate assumptions can go stale; mitigate with periodic (e.g., every 2-3 years) re-comparison against then-current law, and use tax-loss harvesting opportunistically rather than assuming it away.
- Cluster D — **plan change**: make the liquidity-weighting judgment call explicit to the household *before* acting on this recommendation (it already is, in chain C8 and the Conclusion's confidence line) rather than burying it as an analyst's silent default; if the household reviews the flip test in C8 and does not recognize the stated liquidity value as their own, the recommendation does not apply to them as stated and Option A or the split should be used instead.

*Falsification.* This recommendation is false if, within the 10-year horizon, the household's realized behavioral discipline is materially worse than Assumption A-10 (any material discretionary withdrawal or panic-sale), or if the household's true liquidity preference is materially lower than Assumption A-9 (they have no plausible use for the optionality and view mortgage-freedom as a terminal goal rather than a financial-return question), or if a recast-enabled cash-flow reduction turns out to be the household's actual near-term priority. Any of these is already shown, by chain C8's own flip test, to be enough to change the recommended option.

## Self-audit: §6→§4 closure ledger (process output)

- "Invest the $60,000 in a broad-market, low-cost taxable index fund (Option B) rather than applying it as extra mortgage principal" → chain C8 ✓
- "The decisive factor is the asymmetric reversibility of the two options, not a raw expected-return comparison" → chain C7 ✓ (chain C5 ✓)
- "This recommendation accepts a quantified ~24-30% historical chance of underperforming the guaranteed paydown-equivalent, ongoing tax complexity, and forgoes the forced-discipline value of a smaller mortgage balance" → chain C3 ✓ (chain C2 ✓, chain C5 ✓)
- "Confidence: LOW" → chain C3 ✓ (chain C8 ✓)

All four Conclusion-section claims (the four prescribed lead-ins) are cited inline to a named section-4 chain; none required a `no chain — flagged assumption only` marker. Ledger clean.

## Self-audit scan (process output)

| Chain | Chain Head (brief) | Form conforming? | Rule applied | Dependency clean? | Band | Act attempted? | Edges fired |
|-------|---------------------|-------------------|---------------|--------------------|------|-----------------|-------------|
| C1 | GT-1, GT-7, GT-9 | yes | n/a | yes | HIGH | yes | none |
| C2 | C1, GT-9, GT-14?, GT-18 | yes | n/a | yes | MEDIUM | yes | none |
| C3 | GT-12, C2 | yes | n/a | yes | LOW | yes | none |
| C4 | GT-6, GT-15 | yes | n/a | yes | MEDIUM | yes | none |
| C5 | GT-6, GT-5, GT-10 | yes | n/a | yes | HIGH | yes | none |
| C6 | C1, C3 | yes | n/a | yes | LOW | yes | none |
| C7 | C4, GT-17? | yes | n/a | yes | MEDIUM | yes | none |
| C8 | C1, C3, C4, C5, C7 | yes | n/a | yes | LOW | yes | none |

| §6 Span (brief) | Construct | Claim under R11? | R11 clause applied | Chain cited |
|-------------------|-----------|-------------------|----------------------|---------------|
| "Recommended approach: Invest the $60,000..." | bold lead-in | yes | colon closes bold span; assertion follows on same line | C8 |
| "Key insight: ...asymmetric reversibility..." | bold lead-in | yes | colon closes bold span; assertion follows on same line | C7 (also C5) |
| "Trade-offs acknowledged: ...accepts a quantified ~24-30% chance..." | bold lead-in | yes | colon closes bold span; assertion follows on same line | C3 (also C2, C5, C8) |
| "Pre-check: head C2 (MEDIUM), C3 (LOW)..." | other (pre-check line) | yes | pre-check line is itself a claim per output-template.md's pre-check note | C2, C3, C5, C7, C8 |
| "Confidence: LOW — primarily because C3..." | bold lead-in | yes | colon closes bold span; assertion follows on same line | C3 (also C8) |

Scan complete: 8 chain rows, one per section-4 chain block in order; 5 section-6 rows, one per construct in order — 5 claims under R11, 0 excluded. 0 chains malformed, 0 claims untraced.

## Self-Audit Gate (process output)

**Criterion 1: Identify Essence**
Quoted span: "Should this household apply $60,000 of surplus cash — already above a fully-funded six-month emergency reserve — as extra principal on a $240,000, 6.25%, 27-years-remaining mortgage that provides no tax shield, or invest it in a taxable broad-market index fund, over a 10-year decision horizon, once the comparison is made after-tax and the realistic variance of 10-year equity returns is priced in rather than assumed away?"
Band: **Rigorous**
Justification: the statement names the household's specific numbers (not a generic template), strips the question down to the after-tax, variance-aware comparison rather than restating the user's prompt verbatim, and each success criterion is a checkable verb+subject+outcome triplet scannable against section 6.

**Criterion 2: Challenge Assumptions**
Quoted span: "A-9 | ... | Challenge — this is a judgment call this analysis makes about the household's revealed preferences, not a fact the household stated; it is the single most sensitive lever in C8's flip test | unverified — flagged"
Band: **Rigorous**
Justification: all 12 rows use the four-type scheme with no freeform labels, every Verdict cell is a leading token plus em-dash justification, every assumption used in a chain despite being unverified (A-4, A-5, A-9, A-10, A-11) carries "unverified — flagged" in Verification, at least six assumptions are Challenged rather than merely Accepted, and the Assumption Audit scan confirms the Phase-4 scan was exhaustive over all 26 named chain steps with no new assumption needing a new row.

**Criterion 3: Establish Ground Truths**
Quoted span: enumerated GT-13, GT-14, GT-17 against the Ground Truths list's `?` suffixes; the list carries `?` on exactly those three of eighteen, matching the provenance summary's "?-marked: GT-13, GT-14, GT-17 (3 of 18)."
Band: **Rigorous**
Justification: every GT carries a stable ID matching section 4's references, a provenance label, and a source more specific than "common knowledge"; the enumeration checks against the list and matches; every unsuffixed GT feeding a HIGH chain (GT-1, GT-3, GT-7 feeding C1; GT-6, GT-5, GT-4, GT-10 feeding C5; GT-6, GT-15 feeding C4) names its read-at-source location; the two unreachable `?` GTs (GT-14, GT-17) each carry a Phase 3 failure record naming the source and why unreachable, and each feeds only MEDIUM/LOW chains (C2/C7), satisfying the EXCEPT clause.

**Criterion 4: Reason Upward**
Quoted span: self-audit scan chain-form table, all eight rows reading `Form conforming? = yes`, `Dependency clean? = yes` (e.g., "C8 | C1, C3, C4, C5, C7 | yes | n/a | yes | LOW | yes | none").
Band: **Rigorous**
Justification: the scan shows every chain's form conforming and dependencies clean with no cycle; every chain has at least one genuine intermediate hop; the trade-off matrix and second-order list are collapsed per the conversion rule (one chain each, C8 and C7); no analogy is used as direct evidence anywhere; every chain step introducing an assumption beyond the Phase 2 table declares it inline via `[Assumes: X]` (C3, C7, C8); Abandoned Reasoning (section 5) documents three specific dead ends with structural, non-generic abandonment reasons.

**Criterion 5: Validate**
Quoted span: "C3 ... Confidence: LOW — two axes are short. Inputs: capped at MEDIUM by the cited chain C2. Rivals: a live, unsettled rival is carried forward... nothing in this analysis settles it."
Band: **Rigorous**
Justification: every chain's confidence line names its specific downgrade cause(s) (a `?`-marked input with its verification path, a cited chain's band, or an unsettled rival) rather than a generic hedge; no chain consuming a `?` input is rated HIGH; every chain is rated no higher than the lowest-rated chain its head cites (C6, C7, C8 all correctly capped); bands are calibrated to their axes in both directions (C4 and C5 are rated HIGH, not defensively lowered, because their axes license it); the adversarial pass record is complete with all five parts (Recompute, Sensitivity, Rival, the Pre-Mortem technique's Premise/Causes/Clusters/Disposition, and Falsification), and every cluster carries a named disposition (a plan change or an explicitly accepted, named-mitigation risk).

**Criterion 6: Conclusion-to-Ground-Truth Traceability**
Quoted span: self-audit scan claim-inventory table, all five section-6 constructs reading `Claim under R11? = yes` with a named chain in `Chain cited` (e.g., "Confidence: LOW — primarily because C3... | bold lead-in | yes | ... | C3 (also C8)").
Band: **Rigorous**
Justification: every Conclusion-section claim cites a specific named chain inline, the §6→§4 closure ledger confirms all four claims plus the pre-check line are discharged with no claim left untraced, no new reasoning is introduced in section 6 that does not already appear in section 4, and the Key Insight (the reversibility asymmetry) is a non-obvious finding distinct from — not a restatement of — the Recommended Approach.

**Gate result:** No criterion scored Absent; zero criteria scored Hand-wavy (the cap of at most one is satisfied with room to spare). The analysis clears the Self-Audit Gate on the first pass — no Fix/Repeat re-score was required.

---

# $60,000: Extra Mortgage Principal vs. Taxable Brokerage Investment — First-Principles Analysis

## 1. Problem Essence

**Core problem:** Should this household apply $60,000 of surplus cash — already above a fully-funded six-month emergency reserve — as extra principal on a $240,000, 6.25%, 27-years-remaining mortgage that provides no tax shield, or invest it in a taxable broad-market index fund, over a 10-year decision horizon, once the comparison is made after-tax and the realistic variance of 10-year equity returns is priced in rather than assumed away?

**Success criteria:**
- The Conclusion section names one recommended option (or an explicit blended option), not an open-ended "it depends."
- The comparison treats the mortgage paydown as an after-tax benchmark and the equity return as an after-tax, taxed-on-realization quantity — not a pretax-note-rate-vs-pretax-equity-return mismatch (the heuristic this analysis was asked not to default to).
- The Conclusion states a quantified historical probability — not a qualitative gesture — that the equity path fails to clear the guaranteed-paydown-equivalent over the stated 10-year horizon.
- The Conclusion names at least one concrete, named condition that would change the recommended option, not only conditions that support the option given.

---

## 2. Assumptions Table

| Assumption | Type | Treatment | Verdict | Verification |
|------------|------|-----------|---------|--------------|
| A-1: Compound-interest arithmetic — (1+r)^n growth and the standard loan-amortization formula — is a fixed mathematical identity | physical law | Accept as a ground-truth candidate; used directly to compute GT-1 through GT-5 | Accept — a mathematical identity is not negotiable by context | Verified — standard amortization formula, computed directly this session |
| A-2: The household's self-reported facts (loan balance, rate, remaining term, tax rates, reserve status, 10-year horizon) are accurate | current constraint | Accept as given; not independently auditable by this analysis | Accept — the household is the primary source for facts about its own finances | user-stated problem facts, quoted directly from the prompt |
| A-3: The loan's contractual terms (6.25% fixed, 27 years remaining) hold unless the household itself changes them | current constraint | Accept as given; expires on a future refinance or loan modification | Accept — contractual, not physical; expiry is a future household action | loan contract terms, as stated |
| A-4: The 1926-2025 historical distribution of rolling 10-year S&P 500 returns is a valid proxy for the next 10 years | untested belief | Verify or flag; used in chain C3 despite being unverified | Challenge — current valuation levels are not evaluated in this analysis, so this proxy's forward accuracy is unknown in either direction | unverified — flagged (`[Assumes: A-4]` on C3's first hop) |
| A-5: A ~0.4-0.6%/year tax-cost ratio approximates this household's annual dividend-tax drag on a passive index fund | untested belief | Verify or flag; used in chain C2 | Challenge — the cited source (GT-14) carries an unresolved Phase 3 failure record | unverified — flagged |
| A-6: The separately-funded six-month emergency reserve remains adequate and untouched throughout the horizon | current constraint | Accept as given; expires if the reserve is depleted or expenses rise materially | Accept — stated precondition of the problem | user-stated problem fact (GT-10) |
| A-7: Whether to request a loan recast after the extra-principal payment is the household's own future choice | convention | Explicitly challenge before use; both branches are modeled rather than one assumed | Accept — both paths modeled (GT-3/GT-4 no-recast; GT-5 recast) | modeled directly, see GT-3 through GT-5 |
| A-8: The stated 28% ordinary / 18% LTCG marginal tax rates remain stable for the full 10-year horizon | current constraint | Accept as given; expires if tax law or the household's bracket changes | Accept — current law and current bracket, with expiry named; sensitivity addressed in the adversarial pass (Cluster C) | user-stated problem facts (GT-8, GT-9) |
| A-9: Liquidity/optionality has real, decision-relevant value to this household despite no current unmet liquidity need | untested belief | Verify or flag; used as a scoring input in chain C8's trade-off | Challenge — a judgment call this analysis makes about revealed preferences, not a household-stated fact; the single most sensitive lever in C8's flip test | unverified — flagged (`[Assumes: A-9]` on C8's first hop) |
| A-10: This household's behavioral discipline around a large liquid balance is high (low temptation/panic-sell risk) | untested belief | Verify or flag; used as a scoring input in chain C8's trade-off | Challenge — inferred only from the sophistication evidenced by the question itself; flagged as Pre-Mortem Cluster B's central risk | unverified — flagged (`[Assumes: A-10]` on C8's first hop) |
| A-11: No contractual prepayment penalty applies to voluntary extra-principal payments on this loan | untested belief | Verify or flag; used in chain C7 | Challenge — two direct-source verification attempts failed (404, 403); carried as strong regulatory convention, not independently confirmed | unverified — flagged (GT-17; `[Assumes: A-11]` on C7's first hop) |
| A-12: Modeling Option B under a "sold at year 10" tax convention, rather than a "held indefinitely, stepped-up basis" convention, is the appropriate base case | convention | Explicitly challenge before use; the more favorable hold-forever convention is disclosed, not used as the base case | Accept — the harder, more conservative convention is adopted deliberately; the easier one is named in §5 "Dead End 3" as a disclosed, even-more-favorable alternative not relied upon | modeled directly; see GT-16 and §5 Dead End 3 |

**Stakes-escalation note:** A-9 and A-10 carry the highest stakes in this analysis — they are the two judgment calls the final recommendation is most sensitive to (chain C8's flip test) — yet neither could be pushed past "untested belief" given the information available; both are therefore flagged explicitly rather than quietly treated as settled.

---

## 3. Ground Truths

- **GT-1** Monthly principal-and-interest payment on the $240,000 balance, fixed at 6.25%/year, amortized over the 324 months (27 years) remaining, is $1,535.24 — source: standard amortization formula M = P·r/(1-(1+r)^-n); read-at-source: computed directly this session and independently re-verified in the adversarial pass's Recompute step.
- **GT-2** Absent any extra payment, the loan balance after 120 months (10 years) is $192,615.95, having paid $136,844.35 in interest over that window — source: direct month-by-month amortization simulation of GT-1's payment; read-at-source: computed directly this session.
- **GT-3** Applying the $60,000 as extra principal today, with the required monthly payment left unchanged (no recast requested), the loan balance after 120 months is $80,702.86, having paid $84,931.26 in interest — a $51,913.09 ten-year interest saving versus GT-2 — source: direct simulation; read-at-source: computed directly this session, re-verified in the Recompute step.
- **GT-4** Under the same no-recast path, the loan is fully paid off at month 182 (about 15.17 years) rather than month 324 (27 years) — about 11.8 years sooner — with total lifetime interest of $98,773.59 versus $257,416.67 baseline, a $158,643.09 lifetime saving — source: direct simulation continued to payoff; read-at-source: computed directly this session.
- **GT-5** If the household instead requests a recast after the $60,000 lump-sum payment, the loan re-amortizes the reduced $180,000 balance over the same 324 remaining months, producing a new required payment of $1,151.43/month — $383.81/month lower than GT-1 — source: amortization formula re-applied to the reduced balance; read-at-source: computed directly this session, re-verified in the Recompute step.
- **GT-6** A lump-sum extra-principal payment does not, by itself, reduce the required monthly payment; it stays at GT-1's level unless the borrower formally requests a recast, which most servicers charge a fee (quoted example: $250) to process — source: mortgagequestions.com, "Recast" article; read-at-source: the page's comparison table — "Extra Principal Payment: Monthly Payment - Stays the same" vs. "Recast: Monthly Payment - Goes down" — and its quoted $250 administrative fee, located via direct fetch of the page.
- **GT-7** This household takes the standard deduction, so mortgage interest provides zero marginal federal or state tax benefit — source: user-stated problem fact; read-at-source: quoted directly from the prompt.
- **GT-8** This household's marginal ordinary income tax rate (federal + state combined) is approximately 28% — source: user-stated problem fact; read-at-source: quoted directly from the prompt.
- **GT-9** This household's marginal long-term capital-gains / qualified-dividend tax rate is approximately 18% — source: user-stated problem fact; read-at-source: quoted directly from the prompt.
- **GT-10** The $60,000 is surplus cash held above an already fully-funded six-month emergency reserve — source: user-stated problem fact; read-at-source: quoted directly from the prompt.
- **GT-11** The decision horizon under analysis is 10 years — source: user-stated problem fact; read-at-source: quoted directly from the prompt.
- **GT-12** Since 1926, approximately 24% of rolling 10-year holding periods in U.S. large-cap equities (S&P 500, total return with dividends reinvested, nominal, pretax) produced annualized returns below 7%/year, and approximately 4% produced negative annualized returns — source: Ben Carlson, "10% Returns in the Stock Market," A Wealth of Common Sense (Apr 2025); read-at-source: the article's stated figure, "24% of the time the U.S. stock market returned less than 7% per year over 10 years," and its companion negative-decade figure, located via direct fetch of the page.
- **GT-13?** The 2000-2009 "lost decade" produced an S&P 500 annualized total return (dividends reinvested) of approximately -0.9%/year — cited to multiple secondary finance-commentary sources converging on this figure; reported-by-delegate: supplied by a web search synthesis; the underlying primary source was not independently opened by this analysis. Not used as a head input in any chain (narrative color only, in C3's second hop); not load-bearing.
- **GT-14?** Morningstar's published "tax-cost ratio" methodology is cited (in secondary commentary) as showing S&P 500 index funds with typical tax-cost ratios of roughly 0.4%-0.6%/year for investors in the highest tax bracket — unverified: this analysis attempted to open the cited Morningstar methodology PDF directly, but the fetch returned non-extractable binary content, so the asserted figures could not be confirmed in the source text itself. **Phase 3 failure record:** source — Morningstar Tax-Cost-Ratio Methodology PDF; reason unreachable — content returned as non-extractable binary/corrupted text.
- **GT-15** As of October 7, 2026, the national average HELOC (home-equity line of credit) interest rate is 7.33% — source: Bankrate national HELOC rate survey; read-at-source: "The national average HELOC interest rate is 7.33% as of October 7, 2026, according to Bankrate's latest survey of the nation's largest home equity lenders," located via direct fetch of the page.
- **GT-16** Securities inherited from a decedent (including a taxable brokerage account) generally take a basis equal to fair market value on the date of transfer rather than the decedent's original cost basis ("stepped-up basis"), eliminating capital-gains tax on appreciation accrued before death if the heir does not sell before inheriting — source: IRS Tax Topic 703; read-at-source: "If you have stocks or bonds that you didn't purchase, your basis is usually determined by the fair market value of the stocks and bonds on the date of transfer...," located via direct fetch of the page.
- **GT-17?** Most fixed-rate mortgages originated under post-2014 "Qualified Mortgage" (Ability-to-Repay) rules carry no prepayment penalty, so a borrower can generally pay extra principal, or pay off the loan early, without a contractual penalty — cited to the CFPB/Dodd-Frank Ability-to-Repay rule (12 CFR 1026.43) convention; unverified: two direct-source verification attempts failed. **Phase 3 failure record:** sources — consumerfinance.gov (returned 404 Not Found) and nolo.com (returned 403 Forbidden); reason unreachable — both cited pages could not be retrieved; carried forward as a widely-reported regulatory convention, not independently confirmed at source this session.
- **GT-18** As of October 7, 2026 (4:00 PM EDT), the S&P 500's current dividend yield is approximately 1.04% — source: multpl.com, S&P 500 Dividend Yield page; read-at-source: "Current Yield: 1.04% +0.26 bps," as of "4:00 PM EDT, Wed Oct 7," located via direct fetch of the page.

**Provenance summary:**
```text
?-marked: GT-13, GT-14, GT-17 (3 of 18)
Read-at-source: GT-1 — direct amortization computation, re-verified in the Recompute step
Read-at-source: GT-3, GT-4, GT-5 — direct amortization computation, re-verified in the Recompute step
Read-at-source: GT-6 — mortgagequestions.com "Recast" comparison table, quoted verbatim
Read-at-source: GT-12 — awealthofcommonsense.com, "24% of the time..." quoted verbatim
Read-at-source: GT-15 — Bankrate HELOC survey, "7.33% as of October 7, 2026," quoted verbatim
Read-at-source: GT-16 — IRS Tax Topic 703, quoted verbatim
Read-at-source: GT-18 — multpl.com, "Current Yield: 1.04%," quoted verbatim
```

---

## 4. Derivation Chains

### Conclusion C1: Extra-principal paydown is financially equivalent to a riskless, already-after-tax 6.25% instrument — the correct benchmark for Option B, not the note rate compared to a pretax equity return

GT-1 (6.25% fixed note rate, fixed payment) + GT-3 (10yr interest saved under no-recast, $51,913) + GT-7 (standard deduction, zero tax shield)
→ GT-3's $51,913 of interest avoided over 10 years is earned with 100% certainty at exactly the note rate, since a lender always credits extra principal against the loan's contract rate with no market or credit risk attached
→ because GT-7 establishes the household captures no deduction from paying that interest in the first place, none of this avoided interest was ever tax-shielded, so there is no tax asymmetry to adjust for on the paydown side, unlike the investment side addressed in chain C2
→ the $60,000 extra-principal payment is therefore economically identical to a riskless, already-after-tax 6.25% instrument, compounding to $110,012 after 10 years, which is the benchmark Option B's uncertain after-tax return must clear rather than a comparison of the note rate against a pretax equity return

**Pre-check:** head GT-1, GT-3, GT-7 · ?-marked: none · lowest cited: none · Inputs ceiling: HIGH
**Confidence:** HIGH — every head input is an unsuffixed, read-at-source (or directly computed and Recompute-verified) ground truth; every hop is a deductive financial-math identity; the one live rival (a future-itemizing household retaining a partial tax shield) is ruled out directly by GT-7, which fixes this household's standard-deduction status for the analysis.

### Conclusion C2: Option B needs an after-tax-equivalent pretax nominal CAGR of about 7.8%/year (if liquidated at year 10) or about 6.75%/year (if never sold) to match C1's guaranteed benchmark — and almost all of that must come from price appreciation, not dividends

C1 (breakeven target, $110,012) + GT-9 (18% LTCG rate) + GT-14? (~0.5%/yr tax-cost drag)
→ compounding $60,000 at a trial pretax CAGR for 10 years, subtracting an annual dividend-tax drag per GT-14? and a one-time 18% capital-gains tax per GT-9 on the gain if liquidated, and solving for the CAGR that reproduces C1's $110,012 target, yields a breakeven of about 7.8%/year pretax
→ solving the same equation without the liquidation tax, representing an investor who never sells and keeps the position unrealized, lowers the breakeven to about 6.75%/year pretax
→ because the fund's current dividend yield per GT-18 is only about 1.0%, roughly 6.7 to 8.8 percentage points of annual price appreciation is required to clear either breakeven, so the comparison hinges almost entirely on uncertain capital appreciation rather than the steadier dividend component of return

**Pre-check:** head C1 (HIGH), GT-9, GT-14? · ?-marked: GT-14? · lowest cited: HIGH · Inputs ceiling: MEDIUM
**Confidence:** MEDIUM — GT-14? is unverified (Phase 3 failure record: the cited Morningstar methodology PDF returned non-extractable content); verification would mean locating a readable primary or secondary source stating Morningstar's actual tax-cost-ratio figures for S&P 500 funds. No other axis is short: the breakeven arithmetic recomputes cleanly by bisection (adversarial pass, Recompute), and no rival reading of the breakeven itself is offered anywhere in this analysis.

### Conclusion C3: Using the historical base rate, there is roughly a 24-30% chance equities fail to clear C1's guaranteed benchmark over this specific 10-year window, even though the probability-weighted expected outcome is meaningfully higher ($149,361 vs. $110,012)

GT-12 (24% of decades <7%, 4% negative) + C2 (breakeven ≈7.8%/6.75%)
→ mapping GT-12's historical frequency data onto C2's ≈7.8% sold-case breakeven, by linear interpolation within the nearest known threshold bucket, implies roughly a 30% historical chance that a random 10-year window's pretax CAGR would have landed below the breakeven needed to match the guaranteed paydown *[Assumes: A-4 — the 1926-2025 historical distribution is a valid forward-looking proxy; if false in the direction of currently-elevated valuations suppressing forward returns, the shortfall probability is likely higher than 30%, strengthening rather than reversing this chain's "non-trivial risk" conclusion, so the endpoint still stands]*
→ the same historical distribution's probability-weighted average outcome is pulled well above its median by compounding on the right-skewed upper tail, producing an expected after-tax terminal value near $149,361 against a $110,012 guaranteed figure, a gap of roughly 35 percent
→ the two facts together mean Option B offers a materially better expected outcome than Option A, but with a real, non-trivial, roughly 1-in-4-to-1-in-3 chance of being the worse choice purely from historical sequencing, independent of any skill or timing on the household's part

**Pre-check:** head GT-12, C2 (MEDIUM) · ?-marked: none directly (cites C2) · lowest cited: MEDIUM · Inputs ceiling: MEDIUM
**Confidence:** LOW — two axes are short. Inputs: capped at MEDIUM by the cited chain C2 (see C2's own confidence line for its cause and verification path). Rivals: a live, unsettled rival — whether current equity valuations make the 1926-2025 base rate an unreliable forward proxy — is disclosed but not resolved (see §5, "Dead End 1"), and nothing in this analysis settles it. The Inference axis is not an additional shortfall: hop 1's `[Assumes: A-4]` annotation states what happens if A-4 fails, and the endpoint still stands either way.

### Conclusion C4: Home equity and a brokerage balance are not equally "available" — recovering paid-down principal costs real money and time, while the same $60k in a brokerage account does not

GT-6 (extra principal doesn't lower the required payment absent a paid recast) + GT-15 (current HELOC rate, 7.33%)
→ recovering paid-down principal requires either a formal recast (a fee, and still no cash back — only a lower required payment going forward), a cash-out refinance (closing costs, requalification, a new note at whatever rate then prevails), a HELOC (a new variable-rate loan currently priced near 7.33% per GT-15, itself close to the 6.25% being avoided), or selling the home outright (large transaction costs and months of delay)
→ a brokerage balance, by contrast, converts to cash in at most a few business days at essentially zero marginal cost beyond the LTCG tax already priced into GT-9 and chain C2 — no new loan, no requalification, no closing costs
→ the $60,000 is therefore worth strictly more as optionality inside a brokerage account than as home equity, independent of which option wins on expected return, because converting it back to cash after choosing Option A costs real money while converting it after choosing Option B costs nothing beyond tax already accounted for

**Pre-check:** head GT-6, GT-15 · ?-marked: none · lowest cited: none · Inputs ceiling: HIGH
**Confidence:** HIGH — both head inputs are unsuffixed and read-at-source; the mechanism is definitional rather than probabilistic and recomputes against the quoted figures; the one candidate rival (brokerage liquidity isn't literally free because LTCG tax applies on sale) is named and settled inline — that cost is already priced into GT-9/chain C2, so it does not compete with this chain's conclusion.

### Conclusion C5: Extra principal provides zero incremental cash-flow cushion against a job-loss shock unless the household separately pays to recast, and even then the cushion arrives far slower than simply holding the $60k liquid

GT-6 (no-recast default) + GT-5 (recast lowers payment by $383.81/mo) + GT-4 (loan paid off 11.8yr sooner under no-recast) + GT-10 (6-month reserve already funded separately)
→ under the default no-recast path, a household that loses income still owes the full required payment regardless of the $60,000 already applied, so Option A supplies zero incremental monthly cash-flow protection unless the household proactively requests and pays for a recast, even though GT-4 shows the loan paid off nearly 12 years sooner at the far end
→ even with a recast requested, the $383.81 monthly reduction from GT-5 would take about 156 months of foregone payment to equal the $60,000 that produced it, so the recast path converts the lump sum into cash flow far slower than simply holding it liquid
→ because the household's 6-month reserve is already separately funded per GT-10, neither path is solving an unmet liquidity need today, but the brokerage path keeps the $60,000 available as a second line of defense at full value, while the paydown path converts it into a thin, slow-to-access monthly trickle at best

**Pre-check:** head GT-6, GT-5, GT-4, GT-10 · ?-marked: none · lowest cited: none · Inputs ceiling: HIGH
**Confidence:** HIGH — all four head inputs are unsuffixed, either read-at-source or directly computed and Recompute-verified; the hops are arithmetic and deductive; the candidate rival (a smaller required payment is valuable insurance regardless of how slowly it arrives) is named and settled inline — it changes the magnitude of the comparison, not its direction.

### Conclusion C6: Option A's payoff is capped at exactly 6.25% with zero variance in either direction; Option B's realized outcome is a wide, right-skewed distribution with real upside and genuine downside, so a pure expected-value comparison understates the risk B asks the household to bear

C1 (6.25% guaranteed, no upside) + C3 (wide/skewed realized-return distribution)
→ C1 establishes that paying down the mortgage caps the household's outcome at exactly 6.25%, with no scenario, however favorable markets become, in which the paydown is worth more than that — there is no convention to strip here, since the loan contract fixes the floor and ceiling at the same number
→ C3 establishes that the brokerage path's realized outcome instead ranges from a loss in roughly 1-in-25 historical decades to several multiples of principal in strong decades, a distribution Option A simply does not have
→ a household that values certainty itself, separately from its probability-weighted average payoff, should discount Option B's higher expected value by some risk premium rather than compare raw expected dollars, which is exactly what the plain "expected equity return beats a guaranteed rate" heuristic skips

**Pre-check:** head C1 (HIGH), C3 (LOW) · ?-marked: none directly (cites C3) · lowest cited: LOW · Inputs ceiling: LOW
**Confidence:** LOW — capped by the cited chain C3; see C3's own confidence line for its cause and verification path. This chain adds no further downgrade cause of its own beyond that cap.

### Conclusion C7: Liquid brokerage capital can convert into mortgage paydown later at essentially zero cost, but mortgage paydown cannot cheaply convert back into liquidity — so deferring the irreversible choice preserves more future option value than committing to it now

C4 (illiquidity/cost asymmetry, HIGH) + GT-17? (no prepayment penalty)
→ because GT-17? establishes that voluntary extra-principal payments carry no contractual penalty, a household holding the $60,000 liquid today retains the standing ability to pay it into the mortgage at any later date it chooses, at zero cost beyond forgone interim interest *[Assumes: A-11 — no prepayment penalty applies; if false, converting liquidity back into paydown later would carry a cost, narrowing but not eliminating the reversibility asymmetry, since recast/refinance/HELOC costs under GT-6/GT-15 already dominate the comparison]*
→[2nd] (actor lens) this means the household itself, not a lender or a market event, controls the timing of ever closing off its own optionality, whereas choosing Option A today hands that same irreversibility decision to the household permanently and immediately, with no symmetric undo
→[2nd] (time lens) immediately after the decision both paths look similar on paper, but by year 5 or 10 the gap in realized flexibility compounds — a household that chose B can respond to a rate drop, a job change, or a strong market by redirecting capital, while a household that chose A has already spent its flexibility and can only regain it by borrowing again at whatever terms then prevail
→[3rd] over a full 10-year horizon this makes Option B the lower-regret choice under genuine uncertainty about the household's own future circumstances, independent of which option wins on expected return alone, because the option to choose A later survives choosing B now, while the option to choose B later does not survive choosing A now without cost

**Pre-check:** head C4 (HIGH), GT-17? · ?-marked: GT-17? · lowest cited: HIGH · Inputs ceiling: MEDIUM
**Confidence:** MEDIUM — GT-17? is unverified (Phase 3 failure record: two direct-source verification attempts failed, 404 and 403); verification would mean locating a live CFPB or regulatory-text page confirming the Qualified-Mortgage no-prepayment-penalty convention. The Inference axis is not an additional shortfall: hop 1's `[Assumes: A-11]` annotation states what happens if A-11 fails, and the endpoint still stands, just by a smaller margin.

### Trade-off matrix supporting Conclusion C8 (technique output — collapses to one chain below per the conversion rule)

Three options were scored: **A** (full $60k paydown), **B** (full $60k invest), **C** (50/50 split, $30k each). No must-have knocks out any option. Weights were locked before scoring, against named anchors, grounded in chains C1-C7:

| Criterion | Weight | Anchor (1 / 3 / 5) | A score | B score | C score |
|---|---|---|---|---|---|
| Expected after-tax 10yr value | 4 | <$90k / $110k (C1's guaranteed figure) / >$140k | 3 ($110,012, C1) | 5 ($149,361 expected, C3) | 4 (~$129,687, blend) |
| Downside/certainty | 4 | high shortfall risk / moderate / zero variance | 5 (riskless, C1) | 2 (~30% shortfall risk, C3) | 3 (half exposure) |
| Liquidity/optionality | 5 | illiquid / partial / fully liquid | 1 (C4, C7) | 5 (C4, C7) | 3 (half liquid) |
| Behavioral/structural fit | 2 | high temptation risk / moderate / forced discipline | 5 (C5) | 3 (A-10, flagged) | 4 |
| Tax efficiency/simplicity | 2 | high complexity / moderate / zero friction | 5 (C1, zero forms) | 2 (C2's drag/complexity) | 3 |
| **Weighted total (of 85)** | | | **57** | **63** | **57** |

**Flip test:** the smallest single-criterion weight change that alters the outcome is on Liquidity (currently 5): dropping it to 3.5 (a 30% reduction) exactly ties Invest with Paydown; below 3.5, Paydown wins outright. No other single criterion's weight, moved anywhere inside its allowed 1-5 range, produces even a tie — Expected-value would need to drop from 4 to 1 (a much larger swing) to tie; Downside/certainty and Behavioral/Tax, even moved to their maximum allowed value of 5, do not overtake Invest's lead. Liquidity-weighting is therefore the one lever that actually controls this recommendation.

### Conclusion C8: Weighing expected value, certainty, liquidity, behavior, and tax simplicity together, investing the $60,000 (Option B) scores highest, but the margin is thin and is controlled almost entirely by how much this household values optionality it does not currently need

C1 (guaranteed value, HIGH) + C3 (expected value & shortfall risk, LOW) + C4 (liquidity asymmetry, HIGH) + C5 (behavioral/structural mechanics, HIGH) + C7 (reversibility asymmetry, MEDIUM)
→ weighting expected after-tax value, downside certainty, liquidity, behavioral fit, and tax simplicity at 4:4:5:2:2 and scoring each option against anchors grounded in C1 through C7 yields weighted totals of Invest=63, Paydown=57, and a 50/50 split=57 out of a possible 85 *[Assumes: A-9, A-10 — liquidity is genuinely valued by this household and its behavioral discipline is high; both are judgment calls this analysis makes rather than facts the household stated, and the flip test below shows exactly how much revising them would change the recommendation]*
→ Invest's six-point margin over both alternatives is driven almost entirely by the liquidity criterion, where it scores a full 5 against Paydown's 1, so the recommendation is sensitive chiefly to how much this household actually values optionality it does not currently need
→ the flip test confirms this directly: lowering the liquidity weight from 5 to 3.5, a 30% reduction, exactly ties Invest with full Paydown, while no other single-criterion weight change inside its allowed range achieves even a tie
→ the recommended approach is therefore to invest the $60,000 in the taxable brokerage account rather than apply it as extra mortgage principal, held at LOW rather than HIGH confidence, because the result is a genuine but not overwhelming win for Invest that a household with a different, equally reasonable liquidity preference could legitimately score the other way

**Pre-check:** head C1 (HIGH), C3 (LOW), C4 (HIGH), C5 (HIGH), C7 (MEDIUM) · ?-marked: none directly (cites C3) · lowest cited: LOW · Inputs ceiling: LOW
**Confidence:** LOW — capped by the cited chain C3 (see C3's own confidence line). Hop 1's `[Assumes: A-9, A-10]` annotation names the liquidity-value and behavioral-discipline judgment calls the trade-off's weights encode; hop 3 prices what happens if either fails — a 30% reduction in the liquidity weight alone ties the two leading options — so a household for which A-9 or A-10 does not hold should not adopt this chain's recommended option as stated. The Inference axis is therefore not counted as an additional independent shortfall beyond the Inputs cap inherited from C3.

---

## 5. Abandoned Reasoning

### Dead End 1: Adjusting the historical base rate for current valuation levels (CAPE-conditioning)

**What was tried:** An attempt to refine GT-12's unconditional 24%-below-7%/4%-negative historical base rate into a valuation-conditioned estimate — i.e., to ask whether currently elevated equity valuations imply a forward 10-year return distribution shifted below the full 1926-2025 historical sample.

**Why abandoned:** No current Shiller CAPE figure or valuation-conditioned forward-return study was verified at source during this session. Applying such an adjustment without a verified figure would have introduced an unverified, undisclosed correction dressed up as precision, which is worse than carrying the unconditional base rate forward with its limitation named directly.

**What it ruled out:** A false-precision point estimate (e.g., "the real shortfall probability is 38%, not 30%") that pretends to account for current valuation when it cannot be grounded in anything read at source this session. The live rival this leaves unsettled is named explicitly on chain C3's confidence line rather than silently resolved.

### Dead End 2: Treating the 50/50 split (Option C) as a "safe" compromise that dominates both pure options

**What was tried:** Initially modeled only pure Option A vs. pure Option B; Option C (50/50 split) was added expecting it might capture "the best of both."

**Why abandoned:** Chain C8's weighted scoring shows Option C ties Option A (57 vs. 57) and trails Option B (63) — blending dilutes the criteria that most favor B (liquidity, expected value) by exactly as much as it gains on the criteria that favor A, with no criterion on which blending is individually optimal. It is retained only as the fallback for a household whose actual risk/liquidity weighting differs from the locked-in weights (named explicitly in C8's flip test), not as a headline recommendation.

**What it ruled out:** The intuitively appealing "just split it 50/50 to be safe" compromise as a way to avoid taking a position. The actual numbers show it only averages the two options; it does not dominate either.

### Dead End 3: Using the "held indefinitely, stepped-up basis" convention as the base case for Option B's tax treatment

**What was tried:** Modeling Option B under the assumption the household never sells within the horizon and benefits from GT-16's stepped-up basis if held until death, which produces a more favorable after-tax figure ($169,095 expected, vs. $149,361 under the sold convention).

**Why abandoned:** A 10-year decision horizon implies the household is at least contemplating the possibility of using the money at year 10, not committing to hold it indefinitely or until death. Adopting the indefinite-hold convention as the base case would have biased the comparison in Option B's favor through a modeling choice rather than a reasoned fact. The more conservative "sold at year 10" convention (Assumption A-12) was used as the base case instead, with the more favorable hold-to-death path disclosed as a real, additional, even stronger argument for B, not relied upon for the headline recommendation.

**What it ruled out:** An inflated case for Option B that would not survive scrutiny if the household's actual plans involve eventually spending the money rather than passing it on at death.

---

## 6. Conclusion

**Recommended approach:** Invest the $60,000 in a broad-market, low-cost taxable index fund (Option B) rather than applying it as extra mortgage principal, treating this decision as separate from the already-funded six-month emergency reserve, and explicitly preserving the no-cost option to redirect brokerage proceeds into the mortgage at any later date if circumstances change (chain C8).

**Key insight:** The decisive factor is not "expected equity returns beat a guaranteed 6.25% rate" — the heuristic this analysis was asked not to default to. It is that home equity and brokerage capital are asymmetrically reversible: liquid money can convert into mortgage paydown later at essentially zero cost, but mortgage paydown cannot cheaply convert back into liquidity, and extra principal does not even reduce the required monthly payment unless the household pays to recast it (chain C7, chain C5). This reversibility asymmetry — not the raw return comparison — is what should carry the most weight when locking in an irreversible decision today, and the trade-off's own flip test shows the recommendation is controlled almost entirely by exactly how much this household values that asymmetry (chain C8).

**Trade-offs acknowledged:** This recommendation accepts a concretely quantified ~24-30% historical chance that the brokerage path actually underperforms the guaranteed paydown-equivalent over this specific 10-year window (chain C3), accepts an ongoing small annual tax drag and cost-basis complexity that the paydown path has none of (chain C2), and forgoes the forced-discipline value of an irreversibly smaller mortgage balance (chain C5, chain C8).

**Pre-check:** head C1 (HIGH), C2 (MEDIUM), C3 (LOW), C4 (HIGH), C5 (HIGH), C7 (MEDIUM), C8 (LOW) · ?-marked: none directly · lowest cited: LOW · Inputs ceiling: LOW
**Confidence:** LOW — primarily because C3 (the historical base-rate shortfall probability, feeding C6 and C8) is LOW, driven by an unsettled rival about whether current valuations make the 1926-2025 historical distribution a reliable forward proxy (chain C3), and because C8's own flip test shows the recommendation reverses to an exact tie with full paydown if the liquidity-weighting judgment call (Assumption A-9) is revised down by just 30%. This is a genuinely close call for a household with a different, equally reasonable liquidity or behavioral-discipline profile (Assumptions A-9, A-10) — not the one-sided result "stocks beat guaranteed debt paydown over long horizons" is sometimes presented as. **What would flip it:** (1) a materially lower household value on liquidity/optionality than Assumption A-9 assumes, (2) demonstrated behavioral discipline weaker than Assumption A-10 assumes (any real discretionary withdrawal or panic-sale in years 1-3 is the named tripwire, adversarial pass Cluster B), (3) a near-term cash-flow need that only a recast-enabled payment reduction would solve, or (4) a horizon materially shorter than 10 years, which would compress chain C3's expected-value edge faster than it would reduce its shortfall risk. Any one of these, per chain C8's flip test, is enough to tip the recommendation to full paydown (Option A) or the 50/50 split (Option C, §5 "Dead End 2").
