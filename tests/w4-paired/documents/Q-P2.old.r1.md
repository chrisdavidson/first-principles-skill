# First-Principles Analysis: Loyalty Program Funding Decision

**Mode:** full-composer (the request asks for the complete methodology — ground truths, challenged assumptions, upward reasoning, validated conclusion — naming individual techniques like pre-mortem and second-order only as components of that whole, not as a request for a single focused technique).

---

## Process output 1: End-of-phase Assumption Audit (Phase 4)

| Chain | Step | Step Text (brief) | Assumption surfaced? | Added to Table? |
|---|---|---|---|---|
| C1 | 1 | 2 quarters ≈ 6 months, so churn began rising before the rival's launch | temporal-precedence identity (Assumption #13) | already in table |
| C1 | 2 | cause cannot precede effect → rival launch isn't primary driver | none beyond #13 | n/a |
| C1 | 3 | rival launch explains at most a recent, final-month layer | none | n/a |
| C2 | 1 | $310k/yr → $25,833/mo cash offset required | GT-7 arithmetic identity | already in table |
| C2 | 2 | $25,833/mo ÷ $19 → ~1,360 members/mo | none beyond GT-7 | n/a |
| C2 | 3 | 1,360/48,000 → 2.83pp required monthly churn cut | none | n/a |
| C2 | 4 | 1.8pp bet is ~64% of the revenue-only bar | GT-5 (bet target is CS's claim, not fact) | already in table |
| C3 | 1 | apply 65–75% margin range → ~1,800–2,100 members/mo | GT-8? margin assumption | already in table |
| C3 | 2 | → ~3.8–4.4pp required | none beyond GT-8? | n/a |
| C3 | 3 | margin bar exceeds full reversion to 4.2% baseline | none | n/a |
| C4 | 1 | root-cause-fit weighting favors diagnostic+pilot over full program | GT-9? adverse-selection pattern | already in table |
| C4 | 2 | weighted totals favor diagnostic+pilot over full-fund and over no-action | none beyond GT-9? | n/a |
| C5 | 1 | committing $310k/yr pre-diagnosis locks in a hard-to-unwind cost | GT-10? benefit-stickiness pattern | already in table |
| C5 | 2 | lock-in compounds with C2's shortfall into a structural drag | none beyond GT-10? | n/a |
| C5 | 3 | spend/attention here is unavailable for the C4-preferred option | none | n/a |
| C6 | 1 | evidence (C1, C3) doesn't justify full funding today | none | n/a |
| C6 | 2 | fit-to-window + trade-off + lock-in risk → conditional decision | none | n/a |

All 17 steps trace to assumptions already seeded in the Phase 2 Assumptions Table below — a clean pass, no new rows required at audit time.

---

## Process output 2: §6→§4 closure ledger

- "Fund conditionally: approve a capped pilot and a parallel 2-week churn-driver diagnostic now, and reserve the full $310,000/year commitment for a defined checkpoint at the board update" → chain C6 ✓
- "Diagnostic: segment the two-quarter churn rise by cohort, plan, and cancellation reason to confirm it predates the rival's launch" → chain C1 ✓
- "Pilot: cap the loyalty program to a bounded cohort and measure whether redeemers are disproportionately low-risk members" → chain C4 ✓
- "Gate: scale to full funding only if the pilot's early redemption pattern is not adverse-selected and the diagnostic points to a price/value-sensitive driver the program can plausibly move" → chain C6 ✓
- "The churn increase began roughly five months before the rival's loyalty program existed, so matching the rival cannot be the primary fix for most of the trend" → chain C1 ✓
- "Losing the fast, visible action signal to the board within this cycle" → chain C6 ✓
- "No guarantee that even a fully successful pilot clears the margin-adjusted breakeven bar of roughly 3.8-4.4 percentage points, well above the 1.8-point bet" → chain C3 ✓
- "Confidence: MEDIUM — chains C3, C4, C5 each carry one unverified input" → chains C3, C4, C5 ✓

Ledger clean: 8/8 claims traced.

---

## Process output 3: Self-audit scan (process output)

**Table 1 — chain form (section 4)**

| Chain | Chain Head (brief) | Form conforming? | Rule applied | Dependency clean? |
|---|---|---|---|---|
| C1 | GT-2 + GT-3 | yes | n/a | yes |
| C2 | GT-1 + GT-4 + GT-7 + GT-5 | yes | n/a | yes |
| C3 | C2 + GT-8? | yes | n/a | yes (depends on C2) |
| C4 | GT-2 + GT-3 + C1 + GT-9? + GT-6 | yes | n/a | yes (depends on C1) |
| C5 | GT-4 + C2 + GT-10? | yes | n/a | yes (depends on C2) |
| C6 | C1 + C3 + C4 + C5 + GT-6 | yes | n/a | yes (depends on C1, C3, C4, C5) |

**Table 2 — claim inventory (section 6)**

| §6 Span (brief) | Construct | Claim under R11? | R11 clause applied | Chain cited |
|---|---|---|---|---|
| "Recommended approach:" lead-in + sentence | bold lead-in | yes | colon closes bold span, content follows on same line | C6 |
| "Diagnostic: segment..." | list item | yes | closes own sentence | C1 |
| "Pilot: cap the loyalty program..." | list item | yes | closes own sentence | C4 |
| "Gate: scale to full funding only if..." | list item | yes | closes own sentence | C6 |
| "Key insight:" lead-in + sentence | bold lead-in | yes | colon closes bold span, content follows | C1 |
| "Trade-offs acknowledged, in exchange for..." | bold lead-in | no | section-intro label: colon-terminated span is the whole line, carries no citation of its own | n/a |
| "Losing the fast, visible action signal..." | list item | yes | closes own sentence | C6 |
| "No guarantee that even a fully successful pilot..." | list item | yes | closes own sentence | C3 |
| "Confidence:" lead-in + sentence | bold lead-in | yes | colon closes bold span, content follows | C3, C4, C5 |

Scan complete: 6 chain rows, one per section-4 chain block in order; 9 section-6 rows, one per construct in order — 8 claims under R11, 1 excluded. 0 chains malformed, 0 claims untraced.

---

## Process output 4: Self-Audit Gate — verdict blocks

**Criterion 1: Identify Essence**
Quoted span: "Whether to commit $310,000/year to a loyalty-program bet that assumes (without diagnosis) that the true driver of the churn increase is addressable by a rewards mechanism, within a 3-week window that precludes full certainty but not a bounded diagnostic."
Band: **Rigorous**
Justification: names the real decision (not "should we copy the rival") with four checkable success criteria tied to specific downstream sections (chains C1, C2/C3, and the Conclusion's decision type), and is specific to this case rather than a generic template sentence.

**Criterion 2: Challenge Assumptions**
Quoted span (from the Assumption Audit scan): "All 17 steps trace to assumptions already seeded in the Phase 2 Assumptions Table below — a clean pass, no new rows required at audit time."
Band: **Rigorous**
Justification: all 13 rows carry one of the four types, at least one is Discarded (row 5) and several Challenged, unverified rows used in chains carry "unverified — flagged," and the audit confirms exhaustiveness over every named chain step.

**Criterion 3: Establish Ground Truths**
Quoted span: "?-marked: GT-8, GT-9, GT-10 (3 of 10)."
Band: **Sound**
Justification: IDs are stable and the `?` enumeration matches the list, but GT-1 through GT-7's "read-at-source" location is the stipulated case text itself (no independent external document exists to open) rather than a third-party citation — an honest but structurally weaker provenance than the Rigorous descriptor envisions for an evidence-based analysis.

**Criterion 4: Reason Upward**
Quoted span (from the self-audit scan, Table 1): "C1 | GT-2 + GT-3 | yes | n/a | yes" (representative row; all six rows read `yes`/`n/a`/`yes`).
Band: **Rigorous**
Justification: every chain has a genuine intermediate, all six chains are form-conforming per the scan, the Abandoned Reasoning section documents two real dead ends with specific abandonment reasons, and no analogy is used as direct evidence anywhere in the chains.

**Criterion 5: Validate**
Quoted span: "Confidence: MEDIUM — chains C3, C4, and C5 each carry one unverified input (GT-8?, GT-9?, and GT-10? respectively), while C1 and C2 are HIGH."
Band: **Sound**
Justification: every GT-N? input is named with what would raise it to HIGH, but three of six chains (C3, C4, C5) rest on no HIGH-confidence chain of their own, which bands this criterion below Rigorous per the "conclusion without a HIGH chain is a banding matter" rule rather than failing the gate.

**Criterion 6: Conclusion-to-Ground-Truth Traceability**
Quoted span (from the self-audit scan, Table 2): "Scan complete: 6 chain rows... 9 section-6 rows... 8 claims under R11, 1 excluded... 0 claims untraced."
Band: **Rigorous**
Justification: every claim traces to a named chain, no new reasoning is introduced in section 6, and the Key Insight (the timing mismatch) is a non-obvious finding distinct from the recommended approach, not a restatement of it.

**Gate result:** No criterion Absent; zero criteria at Hand-wavy (below the one-permitted cap). **Gate cleared.**

---

# 1. Problem Essence

**Core problem:** Whether to commit $310,000/year to a loyalty-program bet that assumes — without diagnosis — that the true driver of the churn increase is addressable by a rewards mechanism, inside a 3-week window that precludes full certainty but not a bounded diagnostic.

**Success criteria:**
1. The recommendation states one of fund / don't fund / fund-conditionally, verifiable directly from the Conclusion section.
2. The recommendation names concrete evidence (a diagnostic and/or pilot design) deliverable inside the 3-week window, verifiable from chain C6 and the Conclusion.
3. The recommendation is backed by an explicit breakeven calculation, not an assertion of net benefit, verifiable from chains C2 and C3.
4. The recommendation explicitly addresses whether the rival's launch is a sufficient causal explanation for the churn rise, verifiable from chain C1.

---

# 2. Assumptions Table

| Assumption | Type | Treatment | Verdict | Verification |
|---|---|---|---|---|
| A points/credit loyalty program will causally reduce this product's churn | untested belief | verify or flag | Challenge — this is the exact bet under test | unverified — flagged (feeds C2–C6) |
| The $310k/year figure includes redeemed-credit liability, not just admin/platform cost | untested belief | verify or flag | Challenge — ambiguous in the premise | unverified — flagged; finance should confirm scope before go/no-go |
| The 48,000-member base is roughly steady-state, so churn-rate arithmetic against a near-constant base is valid for near-term breakeven math | current constraint | record expiry | Accept — expires if signup volume shifts materially (e.g., a marketing push or rival-driven pull) | consistent with "48,000 active members" being a current snapshot |
| Gross margin is high enough that revenue-basis and margin-basis breakeven are similar | untested belief | verify or flag | Challenge — no margin data supplied | unverified — flagged (elevated to GT-8?, feeds C3) |
| The rival's loyalty-program launch is the primary driver of this company's churn increase | untested belief | verify or flag | **Discard** — contradicted by the stated timeline | contradicted by GT-2/GT-3 timing, see chain C1 |
| A 1–2 week churn-driver diagnostic (cohort segmentation, cancellation reasons, support-ticket trends) is feasible inside the 3-week window | current constraint | record expiry | Accept — expires if no cancellation-reason or support-ticket instrumentation exists | unverified — flagged; confirm instrumentation before committing the plan |
| Loyalty-credit redemption is disproportionately by members who would have stayed anyway (adverse selection), not by at-risk members | untested belief | verify or flag | Challenge — plausible from the redemption mechanism, not confirmed for this product | unverified — flagged (elevated to GT-9?, feeds C4); directly testable in a pilot |
| No confounding event (price change, feature removal, outage, support incident) occurred in the same 2-quarter window | untested belief | verify or flag | Challenge — unaddressed in the premise, a live unknown | unverified — flagged; exactly what the diagnostic must rule in/out |
| Seasonality is not a material contributor to the 2-quarter churn rise | untested belief | verify or flag | Challenge — no seasonal baseline given | unverified — flagged; diagnostic should compare against prior-year same quarters |
| Member-facing benefits, once introduced, are hard to withdraw without backlash, making $310k/yr effectively sticky | convention | challenge before use | Accept, with challenge noted — plausible, consistent with common loyalty-design practice, not confirmed for this company | unverified — flagged (elevated to GT-10?, feeds C5); mitigated by framing as a scoped pilot |
| A constant-hazard/geometric churn model (avg. lifetime ≈ 1/monthly churn) is adequate for comparing the 4.2%/5.0%/6.8% scenarios | convention | challenge before use | Accept, with challenge noted — standard SaaS modeling shorthand, ignores cohort heterogeneity and stock-compounding | standard modeling convention, not company-specific data |
| Monthly revenue = active members × price; expected monthly churned members ≈ active base × churn rate | physical law | accept as ground-truth candidate | Accept — formal arithmetic identity | verified by direct calculation (promoted to GT-7) |
| A cause cannot precede its effect (temporal precedence) | physical law | accept as ground-truth candidate | Accept — logical/definitional | used inline in chain C1 |

---

# 3. Ground Truths

*Scoping note: this is a stipulated business case, not a document with external citations to open. "Source" below is the user-supplied Situation text itself; "read-at-source" means the figure was read directly from that stipulated text or computed by direct arithmetic on it — there is no third-party document this analysis could independently open.*

- **GT-1** 48,000 active members at $19/month (~$912,000/month, ~$10.944M ARR run-rate) — source: user's Situation statement; read-at-source: "48,000 active members, $19/month each"
- **GT-2** Monthly churn rose from 4.2% to 6.8% over the last two quarters (~62% relative increase) — source: user's Situation statement; read-at-source: "Monthly churn has risen from 4.2% to 6.8% over the last two quarters"
- **GT-3** A rival service launched a similar loyalty/points program approximately one month ago — source: user's Situation statement; read-at-source: "a rival service launched a similar loyalty/points program last month"
- **GT-4** The proposed loyalty program's stated cost is ~$310,000/year — source: user's Situation statement; read-at-source: "costing ~$310,000/year to run"
- **GT-5** Customer Success's stated target is to pull churn back toward 5% (not to 4.2%) — this records that CS *asserts* this target, not that it will be achieved (achievability is the assumption under test) — source: user's Situation statement; read-at-source: "this program will pull churn back toward 5% (not all the way back to 4.2%)"
- **GT-6** Marketing requires a final go/no-go within 3 weeks, ahead of a board update — source: user's Situation statement; read-at-source: "Marketing wants a final go/no-go decision within 3 weeks"
- **GT-7** Monthly recurring revenue = active members × price; expected monthly churned members ≈ active base × monthly churn rate — source: definitional/arithmetic identity; read-at-source: verified by direct calculation in chain C2
- **GT-8?** Gross margin on this subscription's revenue is assumed at 65–75%, a range typical of consumer subscription platforms — unverified: no company financial data was supplied in the premise; this is an industry-typical placeholder, not the company's actual figure
- **GT-9?** Loyalty/points programs are structurally prone to adverse selection — credits are disproportionately claimed by already-loyal, low-churn-risk members rather than at-risk members — unverified: argued from mechanism (redemption requires ongoing engagement, which disengaging members are least likely to show), not from this company's or this industry's redemption data
- **GT-10?** Member-facing benefits, once introduced, are difficult to withdraw without provoking backlash, making their cost effectively sticky — unverified: general pattern, not confirmed against this company's or close peers' history of benefit removals

**Provenance summary:** `?`-marked: GT-8, GT-9, GT-10 (3 of 10). Read-at-source (unsuffixed, feeding HIGH chains C1/C2): GT-1, GT-2, GT-3, GT-4, GT-5, GT-6, GT-7 — each located verbatim or by direct arithmetic in the user's Situation statement as cited above.

---

# 4. Derivation Chains

### Companion techniques applied
- **Five-Whys (causal mode):** "Why is monthly churn rising?" branches into candidate causes (price, product quality, support quality, competitor pull, cohort effect, seasonality) — the drill correctly halts at "we lack the segmentation data to go deeper," which is itself the finding driving the recommended diagnostic (see Abandoned Reasoning).
- **Fishbone:** breadth-first cause categories for the churn rise — Price, Product/Quality, Competitor, Support, Cohort/Seasonality — none can be ruled in or out from the given premise alone, which is exactly why C1's timing evidence (the one thing derivable without new data) carries the analytical weight here.
- **Inversion:** inverting "the program will pull churn to 5%" yields at least six failure-guaranteeing conditions: adverse selection (GT-9?), the driver being product/support quality that points can't touch, competitive parity netting to zero net effect, the incentive being too small relative to $19/month to be behaviorally significant, redemption-UX friction creating its own dissatisfaction, and the at-risk segment simply not engaging with program communications. Several are already load-bearing (GT-9?); the rest sharpen what the diagnostic/pilot should specifically test.
- **Estimate (Fermi):** the breakeven math in C2/C3 below.
- **Theoretical-limit (structural ceiling):** a rewards/credit mechanism can only move churn among members whose decision is marginal on price/value — it has no channel to affect a decision driven by product dissatisfaction or a genuinely superior competing product, so its achievable ceiling is bounded below "full recovery" regardless of program design quality — this is a structural argument, not a benchmarked figure (no external study was consulted), and it is why GT-9? and the trade-off in C4 both discount the program's root-cause fit.
- **Trade-off analysis:** see C4 below (full matrix shown there).
- **Second-order thinking:** see C5 below.
- **Pre-mortem:** see Section 5 (Validate reasoning is folded into the confidence caveats and Abandoned Reasoning below, consistent with Phase 5).

---

### Conclusion C1: The dominant driver of the churn rise predates the rival's launch

GT-2 (churn 4.2%→6.8% over 2 quarters) + GT-3 (rival launched a similar program ~1 month ago)
→ two fiscal quarters span roughly six months, so the churn increase began approximately five months before the rival's program existed
→ a cause cannot precede its effect, so the rival's launch cannot be the primary driver of the majority of the observed increase
→ at most the rival's launch explains a recent, final-month layer on top of a trend that already had another cause

**Confidence:** HIGH — rests only on GT-2 and GT-3 (both directly stated) plus basic temporal logic; no unverified input is load-bearing.

---

### Conclusion C2: Even a fully realized bet does not clear the program's own cash cost on a revenue basis

GT-1 (48,000 members × $19/mo) + GT-4 ($310k/yr cost) + GT-7 (revenue/churn identities) + GT-5 (bet target: 6.8%→5.0%)
→ converting the $310,000 annual cost to a monthly figure gives about $25,833/month that the program must offset in retained revenue every month it runs
→ dividing that monthly cost by the $19 monthly revenue per member gives roughly 1,360 members that must be prevented from churning each month purely to cover the cash cost, before any margin is considered
→ expressing 1,360 members as a share of the 48,000 base gives a required monthly churn-rate reduction of about 2.83 percentage points, the revenue-only breakeven bar
→ the bet in GT-5 targets only a 1.8-point reduction, from 6.8% to 5.0%, which is about 64% of the revenue-only breakeven bar

**Confidence:** HIGH — pure arithmetic on GT-1, GT-4, GT-7, and GT-5 (the last used only as CS's stated target, not as an assumed-true causal outcome); no unverified input is load-bearing.

---

### Conclusion C3: On a margin-adjusted basis, not even full recovery to the pre-crisis baseline clears the cost

C2 (revenue-only breakeven ≈2.83pp) + GT-8? (65–75% margin range, unverified)
→ applying a 65–75% gross-margin range to the required $25,833 monthly offset raises the required retained-member count to roughly 1,800–2,100 members per month, since only the margin portion of each dollar of retained revenue is available to cover a cash cost
→ expressed in churn-rate terms this is roughly 3.8 to 4.4 percentage points of monthly churn reduction needed to break even, about 4.0 points at the midpoint
→ this margin-adjusted bar exceeds even a full reversion to the pre-crisis 4.2% baseline (a 2.6-point reduction), so breakeven from retention math alone is unlikely under any realistic margin unless the company's true margin is unusually high

**Confidence:** MEDIUM — carries GT-8? (unverified margin assumption). Raising to HIGH requires the company's actual gross margin from finance.

---

### Conclusion C4: A diagnostic-plus-capped-pilot outscores funding the full program outright

Trade-off matrix (weights 1–5; criteria phrased so higher is always better):

| Option | Root-cause fit (w5) | Cost flexibility (w3) | Speed to deploy (w3) | Avoids adverse selection (w4) | Reversibility (w3) | **Weighted total** |
|---|---|---|---|---|---|---|
| Fund full loyalty program now | 2 | 2 | 4 | 2 | 2 | **42** |
| Diagnostic + capped pilot | 5 | 5 | 4 | 4 | 5 | **83** |
| Price/plan adjustment test | 3 | 4 | 2 | 4 | 4 | 61 |
| Support-quality investment | 3 | 3 | 1 | 5 | 3 | 56 |
| Do nothing / wait | 1 | 5 | 5 | 5 | 5 | 70 |

GT-2 (churn timing) + GT-3 (rival timing) + C1 (timing mismatch) + GT-9? (adverse-selection pattern, unverified) + GT-6 (3-week window)
→ weighting root-cause fit heaviest given C1, a full-scale rewards program scores low on root-cause fit and reversibility, while a diagnostic-plus-capped-pilot scores high on both and still fits the 3-week window
→ the weighted totals favor the diagnostic-plus-pilot option (83) over funding the full program outright (42) and over taking no action at all (70), driven by root-cause fit and reversibility

**Confidence:** MEDIUM — carries GT-9? (unverified adverse-selection pattern). Raising to HIGH requires the pilot's own redemption-segment analysis, which the recommendation below builds in as the gating evidence.

---

### Conclusion C5: Full funding now carries lock-in and opportunity-cost risk beyond the $310k headline

GT-4 ($310k/yr cost) + C2 (breakeven shortfall) + GT-10? (benefit stickiness, unverified)
→ committing to a $310,000/year recurring program before the driver is diagnosed locks in a cost that is hard to unwind once members expect redeemable points, independent of whether the program later proves effective
→ that lock-in compounds with the shortfall shown in C2, creating a structural drag on unit economics that persists even after the underlying churn driver is or is not resolved by other means
→ the money and operational attention this program requires are simultaneously unavailable for the diagnostic-plus-pilot option that C4 rated as the better fit for the likely root cause

**Confidence:** MEDIUM — carries GT-10? (unverified stickiness pattern). Raising to HIGH requires reviewing this company's or close peers' history of withdrawing member-facing benefits, or structurally avoiding the question by framing the near-term rollout as an explicitly time-boxed pilot.

---

### Conclusion C6: Fund conditionally — gate full funding behind a diagnostic and a capped pilot

C1 (timing mismatch) + C3 (margin-adjusted shortfall) + C4 (trade-off favors pilot) + C5 (lock-in and opportunity cost) + GT-6 (3-week window)
→ since the dominant driver of the churn rise predates the rival's launch and the program's own retention math likely does not clear its cost even in the best case, funding the program in full today is not justified by the evidence available
→ since a diagnostic-plus-capped-pilot fits the 3-week window, scores highest on the trade-off analysis, and avoids the lock-in and opportunity-cost risk of an unconditional commitment, the decision that matches both the evidence and the timeline is a conditional one: commission the diagnostic and a capped pilot now, and reserve the full-funding go/no-go for the board-update checkpoint

**Confidence:** MEDIUM — aggregates C1 (HIGH), C3/C4/C5 (MEDIUM, each carrying one `GT-N?`). Raising to HIGH requires resolving GT-8?, GT-9?, and GT-10? as described in C3, C4, C5.

---

# 5. Abandoned Reasoning

### Dead End: Attributing the entire churn rise to the rival's competitive launch
**What was tried:** treating the rival's loyalty-program launch as the primary explanation for the two-quarter churn rise, which would make "match the rival with our own program" a directly sufficient response.
**Why abandoned:** contradicted by the stated timeline — GT-2's rise spans roughly six months while GT-3's rival launch is only about one month old, so the rise predates the rival's move by roughly five months (chain C1). A cause cannot precede its effect.
**What it ruled out:** saves the reader from treating "match the rival" as a sufficient rationale for the program without further diagnosis — it explains at most a recent layer on the trend, not the trend's origin.

### Dead End: Using full-base LTV stock revaluation as the primary breakeven metric
**What was tried:** valuing the customer base at $19/churn-rate per member (average-lifetime LTV) at 6.8%, 5.0%, and 4.2% to get aggregate base values of ~$13.41M, ~$18.24M, and ~$21.71M respectively, and using the ~$4.83M delta (6.8%→5.0%) as the "value" of the bet against the $310k/year cost.
**Why abandoned:** this is a stock (multi-year, undiscounted, whole-future-lifetime) quantity being compared against a recurring annual cost without an explicit time horizon or discount rate — a mismatch in kind, not a like-for-like breakeven test. It also assumes the rate change persists indefinitely and is realized instantly across the base, which the case does not support. Chains C2/C3's monthly-flow breakeven compares a recurring cost to a recurring benefit at the same cadence, which is the correct instrument for a 3-week go/no-go.
**What it ruled out:** saves the reader from concluding the program is "obviously cheap" against an $8.3M-scale problem — that framing is directionally informative about the stakes but is not a valid breakeven test on its own, and using it as the primary metric would have overstated the case for funding.

---

# 6. Conclusion

**Recommended approach:** Fund conditionally: approve a capped pilot and a parallel 2-week churn-driver diagnostic now, and reserve the full $310,000/year commitment for a defined checkpoint at the board update (chain C6).
- Diagnostic: segment the two-quarter churn rise by cohort, plan, and cancellation reason to confirm it predates the rival's launch (chain C1).
- Pilot: cap the loyalty program to a bounded cohort and measure whether redeemers are disproportionately low-risk members (chain C4).
- Gate: scale to full funding only if the pilot's early redemption pattern is not adverse-selected and the diagnostic points to a price/value-sensitive driver the program can plausibly move (chain C6).

**Key insight:** The churn increase began roughly five months before the rival's loyalty program existed, so matching the rival cannot be the primary fix for most of the trend, even though the two events look connected by coincidence of timing (chain C1).

**Trade-offs acknowledged, in exchange for gating instead of deciding outright:**
- Losing the "fast, visible action" signal to the board within this cycle (chain C6).
- No guarantee that even a fully successful pilot clears the margin-adjusted breakeven bar of roughly 3.8-4.4 percentage points, well above the 1.8-point bet (chain C3).

**Confidence:** MEDIUM — chains C3, C4, and C5 each carry one unverified input (GT-8?, GT-9?, and GT-10? respectively), while C1 and C2 are HIGH. Raising the overall rating to HIGH requires: the company's actual gross margin (resolves GT-8?), the pilot's redemption-segment read-out (resolves GT-9?), and a review of prior benefit-withdrawal reactions (resolves GT-10?).