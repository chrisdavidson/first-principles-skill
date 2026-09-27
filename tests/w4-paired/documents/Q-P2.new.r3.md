Below is the complete first-principles workflow for this decision. Per the methodology this instrument runs under, the audit/process artifacts are emitted first (as process output), followed by the six-section signed-off analysis itself.

---

## §6→§4 closure ledger (process output)

- "Fund a capped, gated pilot... contingent on (1) a same-window root-cause read and (2) a randomized holdout cohort" → chain C6 ✓
- "Running a fast, cheap root-cause diagnostic before committing dominates funding the program blind... under every plausible reweighting" → chain C4 ✓
- "This recommendation accepts a short delay... in exchange for a defensible, board-presentable answer next quarter instead of an unmeasurable one now" → chain C5 ✓ / chain C6 ✓
- "the marketing-optics cost of appearing to move slower than the competitor" → no chain — flagged assumption only

## Self-audit scan (process output)

**Table 1 — chain form**

| Chain | Chain Head (brief) | Form conforming? | Rule applied | Dependency clean? | Band | Act attempted? | Edges fired |
|---|---|---|---|---|---|---|---|
| C1 | GT-2 + GT-6? | yes | n/a | yes | LOW | yes | none |
| C2 | GT-2 + GT-8 + GT-11 | yes | n/a | yes | LOW | yes | none |
| C3 | GT-1 + GT-2 + GT-3 + GT-11 | yes | n/a | yes | MEDIUM | yes | none |
| C4 | GT-3 + GT-5 | yes | n/a | yes | HIGH | no | none |
| C5 | GT-3 + GT-5 | yes | n/a | yes | LOW | no | none |
| C6 | C1 + C4 + C5 | yes | n/a | yes | LOW | no | none |

**Table 2 — claim inventory (§6)**

| §6 Span (brief) | Construct | Claim under R11? | R11 clause applied | Chain cited |
|---|---|---|---|---|
| Recommended approach | bold lead-in | yes | same-line assertion after colon | C6 |
| Key insight | bold lead-in | yes | same-line assertion after colon | C4 |
| Trade-offs acknowledged (main sentence) | bold lead-in | yes | same-line assertion after colon | C5, C6 |
| Trade-offs acknowledged (competitor-optics caveat) | bold lead-in (caveat) | yes | caveat with `no chain` marker | none — flagged assumption only |
| Pre-check line | bold lead-in | yes | pre-check line is itself a claim (cited by its own head) | C1, C4, C5, C6 |
| Confidence line | bold lead-in | yes | D-07 discharge via named chains | C1, C5, C6 |

`Scan complete: 6 chain rows, one per section-4 chain block in order; 6 section-6 rows, one per construct in order — 6 claims under R11, 0 excluded. 0 chains malformed, 0 claims untraced.`

## Assumption Audit scan (process output, Phase 4)

| Chain | Step | Step Text (brief) | Assumption surfaced? | Added to Table? |
|---|---|---|---|---|
| C1 | 1 | five-whys enumerates candidate churn drivers | none | n/a |
| C1 | 2 | counterfactual test confirms/rules out none | none | n/a |
| C1 | 3 | program-fit is an untested belief [Assumes: A1] | A1 (already tabled) | n/a |
| C1 | 4 | no causal link established | none | n/a |
| C2 | 1 | apply 19% figure as optimistic ceiling | benchmark transferability | yes (A10) |
| C2 | 2 | 0.5pp gap remains vs. target | none | n/a |
| C2 | 3 | closing the gap needs a stronger effect or another factor | none | n/a |
| C3 | 1 | avoided-loss revenue, holding inflow constant | inflow held constant | yes (A11) |
| C3 | 2 | annualize the near-term saving | none (A11 carries) | n/a |
| C3 | 3 | steady-state base ratio 1.36× | none (A11 carries) | n/a |
| C3 | 4 | $0.5–3M/yr bracket over 15–20 months | none | n/a |
| C3 | 5 | $310K sits below upper, not below lower bound | none | n/a |
| C3 | 6 | value case depends on unresolved share (C1, C2) | none | n/a |
| C4 | 1 | score 4 options against 7 locked-weight criteria | weights reflect priorities | yes (A12) |
| C4 | 2 | diagnose-first beats fund-blind on every criterion | none (A12 carries) | n/a |
| C4 | 3 | flip-test: no single reweight reverses it | none | n/a |
| C4 | 4 | dominance holds regardless of C1/C2 resolution | none | n/a |
| C4 | 5 | recommend gating spend | none | n/a |
| C5 | 1 | redemption liability = deferred discount | A7 (already tabled) | n/a |
| C5 | 2 | CS/marketing incentive shifts to points-engagement | org optimizes to proxy metric | yes (A13) |
| C5 | 3 | competitor rewards arms race | A6 (already tabled) | n/a |
| C5 | 4 | no holdout ⇒ effect unattributable | causal attribution needs a control | yes (A14) |
| C5 | 5 | $310K could recur on an illusory effect | none | n/a |
| C5 | 6 | success criteria require a measurement design | none | n/a |
| C6 | 1 | fatal clusters closed by one fix | none | n/a |
| C6 | 2 | that fix = diagnostic + holdout | none | n/a |
| C6 | 3 | survivable clusters closed by capping exposure | none | n/a |
| C6 | 4 | fund a capped, gated pilot | none | n/a |

## Techniques not applied (process output)

- fishbone — not applicable — the five-whys causal-mode pass (chain C1) already performed a lateral, breadth-first scan of candidate churn drivers across six categories before testing depth, filling fishbone's role; running both would duplicate one cause enumeration under two headings.
- inversion — not applicable — the Conclusion is a plan (a funding/gating recommendation), and the pre-mortem/inversion decision rule routes a plan to pre-mortem, which is applied below as the Phase 5 adversarial technique; inversion's claim-focused form is not separately invoked.

## Adversarial pass (process output)

**Recompute.** 48,000 × $19 = $912,000 MRR × 12 = $10,944,000 ARR (matches the stated "~$10.9M"). 48,000 × 1.8pp = 864 members/month; 864 × $19 = $16,416/mo → $196,992/yr. 6.8/5 = 1.36×; 5/6.8 = 0.735 (26.5% gap). (0.958)¹²  ≈ 0.5973 (40.3% annual churn at 4.2% monthly); (0.932)¹² ≈ 0.4296 (57.0% annual churn at 6.8% monthly); (0.95)¹² ≈ 0.5404 (46.0% annual churn at 5% target). 6.8% × (1−0.19) = 5.508%. All figures recompute cleanly; independently verified above.

**Sensitivity.** The single ground truth whose falsity most changes the conclusion is **GT-6?** (whether a churn-cause diagnosis already exists, undisclosed). It is `?`-marked. If a rigorous diagnosis already exists and shows churn is primarily reward/value-driven, chain C1 collapses and the recommendation moves from "gate the spend" toward "fund it now" — this is why the recommended condition is, precisely, surfacing that diagnosis. Per-chain weakest links: C1 → GT-6? itself; C2 → GT-8 (unsourced 19% figure) via [Assumes: A10]; C3 → [Assumes: A11] (inflow held constant); C5 → the four unpriced organizational assumptions (A7, A13, A6, A14).

**Rival.** Headline (C6): rival "fund the full $310K unconditionally now" is ruled out by C4's Pareto-dominance (§5, chain C4). Rival "do nothing" is ruled out the same way (option D scored lowest of the three real contenders in the trade-off; see Dead End 2). C1: rival "the root cause is known internally but undisclosed in this brief" is **not** ruled out — it stays live, which is exactly why the recommended diagnostic is the gating condition rather than an optional nicety. C2: rival "the true effect for this company is larger than the unsourced 19% figure" is also live and unsettled — noted, not contradicted, since C2's claim is framed as a ceiling, not a point estimate.

**Premise.** The loyalty program has already failed to move churn back toward 5%. What caused it?

**Causes** (unfiltered, generated from CS/implementer, finance/board, competitor, and churning-member viewpoints): (1) low points adoption/redemption because members didn't understand or value the mechanic; (2) program mis-targeted at already-loyal members rather than at-risk ones; (3) redemption friction suppressed usage; (4) the true churn driver (price, product, competitive) was never addressed, so churn kept rising regardless of spend; (5) redemption liability grew larger than budgeted, compounding the margin hit; (6) the competitor's program, better-funded or better-designed, kept pulling switchers regardless; (7) the competitor responded with a richer program, starting an unwinnable rewards arms race; (8) the launch read to the market as reactive/"me-too," costing any goodwill it might have generated; (9) members churned over price or a missing feature that no amount of points touches; (10) broad "subscription fatigue" drove cancellations unrelated to rewards; (11) newer, lower-tenure members — disproportionately likely to be churning — never accrued enough points to feel any stake; (12) churn mean-reverted on its own (a promo cohort's period ending), falsely crediting the program; (13) the opposite confound — the underlying driver kept worsening, falsely blaming the program for a problem it was never sized to fix; (14) no pre-registered holdout existed, so the org can't actually tell which of the above happened.

**Clusters** (structural weaknesses, with bearing):
- **Root-cause mismatch** (causes 4, 9, 10, 11) — bears on GT-6?, chain C1.
- **Measurement/attribution failure** (causes 12, 13, 14) — bears on chain C5, chain C3's statistical-power point.
- **Competitive parity / arms race** (causes 6, 7, 8) — bears on GT-5, chain C5.
- **Liability lock-in / reversibility** (causes 3, 5) — bears on chain C6's pilot-cap logic.

**Disposition:**
- Root-cause mismatch — **Fatal** — plan change: gate full-scale funding on the diagnostic (chain C1); tripwire: <15% of coded exit reasons cite value/rewards, checked at week 3 and quarter-end, owner CS + Data.
- Measurement/attribution failure — **Fatal** (to decision quality) — plan change: mandate a randomized holdout before launch; tripwire: no holdout carved out pre-launch, owner Data/Analytics, checked before go-live.
- Competitive parity / arms race — **Costly but survivable** — accepted risk, mitigation: cap program cost growth behind a re-approval trigger; tripwire: competitor enhances its tier within 2 quarters, owner Marketing/Competitive Intel, checked quarterly.
- Liability lock-in — **Costly but survivable** — accepted risk, mitigation: cap initial commitment to a pilot cohort/budget tranche; tripwire: outstanding point liability exceeds a set % of monthly spend, owner Finance, checked monthly.

**Falsification.** This analysis's recommendation is false if a diagnostic completed within the 3-week window shows a majority of recent churn is attributable to a reward/value-perception gap the loyalty program directly addresses, and no cheaper/faster intervention captures the same value — in that case, funding the full program immediately without further gating would be the correct call.

## Self-Audit Gate (process output)

**Criterion 1: Identify Essence**
Quoted span: "Should the company commit $310,000/year to a points-based loyalty program... given that the churn increase's cause is undiagnosed and the program's causal effectiveness is unverified?"
Band: **Rigorous**
Justification: Names the actual decision (not the triggering event alone), and each of its four success criteria is a verb+subject+outcome test scannable against §6.

**Criterion 2: Challenge Assumptions**
Quoted span: Assumption Audit scan reconciliation — 5 assumptions (A10–A14) surfaced from chain steps and added to the table, none skipped across 28 steps.
Band: **Rigorous**
Justification: Four-type scheme used throughout, em-dash verdict form, unverified-flagged notations present, audit exhaustive over all named chain steps.

**Criterion 3: Establish Ground Truths**
Quoted span: "`?`-marked: GT-6, GT-7, GT-9, GT-10 (4 of 11)" — checked against the list, matches exactly; GT-3 and GT-5 (feeding HIGH chain C4) each carry "read-at-source: stated directly in the decision brief."
Band: **Rigorous**
Justification: Stable IDs, provenance labels throughout, correct enumeration, and the one HIGH chain's unsuffixed inputs name their read-at-source location.

**Criterion 4: Reason Upward**
Quoted span (self-audit scan Table 1): all six rows read "Form conforming? yes... Dependency clean? yes."
Band: **Rigorous**
Justification: Every chain has a genuine intermediate, no analogy used as direct evidence (explicitly barred in Dead End 1), `[Assumes: X]` marks present where surfaced, Abandoned Reasoning carries three specific dead ends.

**Criterion 5: Validate**
Quoted span: Adversarial pass record — Recompute, Sensitivity, Rival, Premise/Causes/Clusters/Disposition, Falsification all present; every cluster carries a named plan change or accepted risk with mitigation.
Band: **Rigorous**
Justification: Bands are calibrated per the three-axis test (C4 legitimately HIGH via a priced flip-test and a ruled-out rival; C1/C2/C5/C6 honestly LOW where two axes are short), the unverified-input and ceiling rules are honored, and the pass is complete.

**Criterion 6: Conclusion-to-Ground-Truth Traceability**
Quoted span (self-audit scan Table 2): all six §6 constructs cite a chain or carry the disclosed caveat marker; the Key Insight ("you don't need to resolve whether the hypothesis is true to see that diagnosing first dominates") is not a restatement of the Recommended approach.
Band: **Rigorous**
Justification: No untraced claims, no new reasoning introduced in §6, Key Insight is genuinely non-obvious.

**Gate cleared** (no Absent) and **hand-wavy cap cleared** (zero Hand-wavy). No re-entry edge fired.

---

# 1. Problem Essence

**Core problem:** Should the company commit $310,000/year to a points-based loyalty program as the mechanism for reversing a monthly churn increase from 4.2% to 6.8%, within a 3-week decision window, given that the churn increase's cause is undiagnosed and the program's causal effectiveness is unverified?

**Success criteria:**
1. The Conclusion states a specific funding decision (fund / don't fund / fund conditionally) with a named dollar commitment or commitment structure.
2. If conditional, the Conclusion names the specific evidence/condition required and confirms it fits inside the 3-week window.
3. The Conclusion explicitly states whether the program targets a diagnosed or an undiagnosed driver of the churn increase.
4. The Conclusion states how the company will know, at the next quarterly board update, whether the spend worked.

---

# 2. Assumptions Table

| Assumption | Type | Treatment | Verdict | Verification |
|---|---|---|---|---|
| A1: The loyalty/credit program addresses the actual root cause of the churn increase | untested belief | verify or flag unverified | Challenge — no root-cause diagnosis exists (GT-6?); load-bearing for the whole bet | unverified — flagged |
| A2: Churn can realistically revert to 5% and that reversion is attributable to this intervention rather than reversion-to-mean, seasonality, or the competitor dynamic | untested belief | verify or flag unverified | Challenge — confounded by GT-5 (competitor's simultaneous launch) and GT-6? (no diagnosis) | unverified — flagged |
| A3: Loyalty/rewards programs generally reduce subscription churn (industry pattern) | untested belief | verify or flag unverified | Challenge — the most commonly cited figure (GT-8) traces to no named study | unverified — flagged |
| A4: $310,000/year is affordable relative to revenue at stake | current constraint | record expiry conditions | Accept — expires once Finance confirms the figure's composition (A7); affordability (2.8% of ARR) is not the binding issue, attributable value is (chain C3) | source: GT-1, GT-3 recompute |
| A5: A legitimate go/no-go decision can be reached within 3 weeks | current constraint | record expiry conditions | Accept — expires at the next board meeting; binding on the design of this recommendation | stated in decision brief |
| A6: Matching the competitor's loyalty launch is the right competitive response (parity convention) | convention | explicitly challenge before use | Challenge — a later-mover, copycat loyalty response typically nets to cost-of-parity rather than differentiation | unverified — flagged |
| A7: The $310K/year figure fully captures the program's cost, including redemption liability growth | untested belief | verify or flag unverified | Challenge — ambiguous whether this is an operating-cost figure only; composition unconfirmed | unverified — flagged |
| A8: 48,000 members / $19-month pricing / ~$10.9M ARR are mutually consistent | physical law (arithmetic) | accept as ground-truth candidate | Accept — recomputes exactly | source: GT-1 |
| A9: (superseded — folded into A8) | — | — | — | — |
| A10: Industry-average loyalty-retention-lift figures (e.g., the 19% claim) are transferable to this member base and price point | untested belief | verify or flag unverified | Challenge — surfaced by Assumption Audit on chain C2; no company-specific data supports transfer | unverified — flagged |
| A11: Gross new-member signups (inflow) will stay roughly constant regardless of the intervention chosen | untested belief | verify or flag unverified | Challenge — surfaced by Assumption Audit on chain C3; not measured in this analysis | unverified — flagged |
| A12: The seven weighted trade-off criteria and their locked weights reflect the company's actual decision priorities | convention | explicitly challenge before use | Challenge — surfaced by Assumption Audit on chain C4; mitigated by the flip-test finding no single reweight changes the winner | unverified — flagged (sensitivity priced) |
| A13: CS/marketing will, absent guardrails, optimize toward loyalty-engagement metrics rather than churn/margin | untested belief | verify or flag unverified | Challenge — surfaced by Assumption Audit on chain C5; organizational-behavior claim, not directly observed here | unverified — flagged |
| A14: Without a randomized holdout, churn changes cannot be attributed to the program versus reversion/seasonality | physical law (statistical/logical) | accept as ground-truth candidate | Accept — a matter of experimental-design logic, not a company-specific claim | accept — formal reasoning |

---

# 3. Ground Truths

- **GT-1** 48,000 active members × $19/month = $912,000 MRR ≈ $10.94M ARR — source: decision brief; read-at-source: recomputed directly (48,000 × 19 × 12 = 10,944,000), consistent with the brief's stated "~$10.9M ARR."
- **GT-2** Monthly churn rose from 4.2% to 6.8% over the last two quarters — source: decision brief; read-at-source: stated directly.
- **GT-3** Proposed loyalty program costs ~$310,000/year to operate — source: decision brief; read-at-source: stated directly. (Composition ambiguity tracked as A7.)
- **GT-4** The stated target is reverting monthly churn toward 5% — source: decision brief; read-at-source: stated directly.
- **GT-5** A named competitor launched a similar loyalty program last month — source: decision brief; read-at-source: stated directly.
- **GT-6?** No churn-cause diagnostic (exit survey, cohort/cause-coding) is disclosed as having been performed — unverified: absence-of-mention in the brief is not proof of absence; Finance/CS may hold undisclosed work.
- **GT-7?** General B2C/consumer-subscription monthly churn benchmarks cluster around 4–8%, varying by vertical, with the citing page itself inconsistent (6.5–8% monthly in one passage vs. 4.04% elsewhere, apparently annual) — cited to: shno.co, in turn crediting "MRRSaver (2026)"; reported-by-delegate — the primary MRRSaver figure was not opened by this analysis.
- **GT-8** The most commonly circulated claim for loyalty-program retention lift (a 19% relative increase) traces, at its point of citation, to no named study, methodology, or sample — source: blog.brandmovers.com; read-at-source: the article's own sentence, opened and confirmed directly, attributing the figure only to unnamed "research published in 2025."
- **GT-9?** Win-back/reactivation campaigns for subscription businesses typically reactivate 5–15% of lapsed customers within 30–90 days (B2C 8–15%, B2B SaaS 5–10%) — reported-by-delegate; sources not independently opened.
- **GT-10?** Retaining an existing subscription customer is commonly estimated at 5–25× cheaper than acquiring a new one (B2B SaaS typically cited at 5–10×) — reported-by-delegate; sources not independently opened.
- **GT-11** Monthly churn compounds geometrically: annual retention = (1 − monthly churn)¹². At 4.2%: ≈59.7% annual retention (≈40.3% annual churn). At 6.8%: ≈43.0% (≈57.0% annual churn). At the 5% target: ≈54.0% (≈46.0% annual churn) — source: mathematical identity; read-at-source: independently recomputed (see Adversarial pass, Recompute).

**Provenance summary:** `?`-marked: GT-6, GT-7, GT-9, GT-10 (4 of 11). Read-at-source: GT-1 — recomputed from the brief's own figures; GT-2/GT-3/GT-4/GT-5 — stated directly in the decision brief; GT-8 — blog.brandmovers.com, sentence quoted verbatim; GT-11 — recomputed. No chain in this analysis is rated HIGH except C4, whose head (GT-3, GT-5) is fully unsuffixed and read-at-source as above.

---

# 4. Derivation Chains

### Conclusion C1: The churn increase's root cause is undiagnosed, so the loyalty program's fit to it cannot be verified

GT-2 (churn rose 4.2%→6.8%) + GT-6? (no churn-cause diagnostic on record)
→ five-whys causal-mode testing enumerated multiple candidate drivers of the churn increase, including competitive switching, price/value mismatch, product or service quality, cohort/promo-expiry timing, cancellation friction, and broader subscription fatigue
→ applying the counterfactual test to each candidate found none could be confirmed or ruled out from the evidence available in this case
→ the assumption that a loyalty/credit program addresses the actual driver of the churn increase is therefore an untested belief carrying full unknown-fit risk [Assumes: A1]
→ no causal link between adding loyalty points and this specific churn increase is established, either internally or via comparable benchmarks

**Pre-check:** head GT-2, GT-6? · ?-marked: GT-6? · lowest cited: none · Inputs ceiling: MEDIUM
**Confidence:** LOW — Inputs axis short (GT-6? unverified; verification: run the internal exit-survey/cohort cause-coding diagnostic named in the recommendation, which would confirm or refute an undiagnosed root cause). Rivals axis also short: "the root cause is known internally but undisclosed" is not ruled out by anything in this analysis — the same diagnostic settles it. Two axes short → LOW.

### Conclusion C2: Even the most optimistic industry figure for loyalty-driven retention lift falls short of the 5% target on its own

GT-2 (6.8% current monthly churn) + GT-8 (unsourced "19%" retention-lift claim) + GT-11 (churn-compounding math)
→ applying the claimed 19% relative retention lift to the current 6.8% monthly churn as an optimistic ceiling yields 6.8% × (1 − 0.19) = 5.51% monthly churn [Assumes: A10]
→ 5.51% remains above the 5% target, leaving roughly a 0.5-percentage-point gap unexplained by the loyalty effect alone
→ closing that gap requires either a materially stronger effect than the unsourced benchmark, or an independent factor such as a root-cause fix or reversion

**Pre-check:** head GT-2, GT-8, GT-11 · ?-marked: none · lowest cited: none · Inputs ceiling: HIGH
**Confidence:** LOW — Inputs ceiling is HIGH (no `?`-marked head input), but Inference axis is short: hop 1 rests on A10 (benchmark transferability), an unpriced premise (verification: a company-specific holdout-cohort measurement, per chain C5/C6). Rivals axis also short: "the true effect for this company could be larger or smaller than 19%" is live and unsettled. Two axes short → LOW.

### Conclusion C3: The revenue at stake plausibly exceeds the program's cost, but only if the program can close a meaningful, currently unverified share of the churn gap

GT-1 (48,000 members, $19/mo, ~$10.94M ARR) + GT-2 (4.2%→6.8% monthly churn) + GT-3 ($310K/yr program cost) + GT-11 (churn-compounding math)
→ holding the active base and new-signup inflow roughly constant, reverting monthly churn from 6.8% to 5% avoids losing about 864 members per month (48,000 × 1.8 percentage points) [Assumes: A11]
→ that avoided loss is worth about $16,400 per month, or roughly $197,000 per year in simple, non-compounding terms
→ over a longer horizon, holding inflow constant, the steady-state member base under 5% versus 6.8% churn differs by a factor of about 1.36×
→ that implies an order-of-magnitude $0.5M–$3M per year steady-state ARR gap, materializing over roughly 15–20 months
→ the $310K/year program cost sits below the upper end of this bracket but not clearly below the near-term lower end
→ the program's value case therefore depends on how much of the churn gap it can actually close, a share chains C1 and C2 show is unverified and at best partial

**Pre-check:** head GT-1, GT-2, GT-3, GT-11 · ?-marked: none · lowest cited: none · Inputs ceiling: HIGH
**Confidence:** MEDIUM — Inputs ceiling is HIGH, but Inference axis is short: the chain rests on A11 (inflow held constant), an unpriced premise (verification: measure actual monthly new-member inflow and rebuild the bracket). No live rival to this specific sizing bracket — Rivals axis clean. One axis short → MEDIUM.

### Conclusion C4: A gated diagnosis-first approach dominates funding the loyalty program blind

GT-3 ($310K/yr proposed cost) + GT-5 (competitor already launched a similar program)
→ scoring four options — fund the loyalty program now, diagnose the root cause first, run a targeted win-back campaign, or do nothing — against seven weighted criteria locked before scoring (root-cause fit, decision speed, cost efficiency, evidence strength, margin impact, competitive positioning, reversibility) [Assumes: A12]
→ the diagnose-first option scores highest of the four on every single criterion when compared against the blind-funding option (107 vs. 42 weighted points; Pareto-dominant, not merely weighted-ahead)
→ the flip-test finds no single-criterion reweighting within a normal 1–5 weight range that reverses this ranking
→ this dominance holds regardless of how chains C1 and C2's unresolved uncertainty ultimately resolves, because diagnosing first is cheap, fits the 3-week decision window, and is fully reversible
→ funding should be gated behind a fast root-cause read and a measurable pilot design, rather than approving the full $310K program uncontrolled

**Pre-check:** head GT-3, GT-5 · ?-marked: none · lowest cited: none · Inputs ceiling: HIGH
**Confidence:** HIGH — Inputs clean; Inference axis satisfied because the assumption most exposed to failure (A12's weighting) was explicitly priced via the flip-test and shown not to change the endpoint; Rivals axis satisfied because the live rival ("fund blind now") is ruled out by Pareto-dominance, not merely out-scored.

### Conclusion C5: Even a nominally successful loyalty program can fail the decision's real purpose if margin and measurement effects are ignored

GT-3 ($310K/yr, credit-based cost) + GT-5 (competitor parity)
→[2nd] redemption liability functions as a deferred discount, so any churn improvement is partly offset by lower realized ARPU among redeeming members [Assumes: A7]
→[2nd] the program also creates an incentive for CS/marketing to report points-engagement metrics rather than the underlying churn and margin goals [Assumes: A13]
→[3rd] if the competitor answers with a richer program, both firms face a rewards arms race that raises the cost of parity without shifting relative competitive position [Assumes: A6]
→[3rd] without a randomized holdout cohort, a genuine program effect cannot be distinguished from reversion-to-mean or seasonal churn decay [Assumes: A14]
→ the $310K/year spend could therefore recur indefinitely on the strength of an unmeasurable, possibly illusory effect
→ the decision's success criteria — restore healthy churn, protect unit economics, and produce a defensible answer for the board — require a measurement design built into the program, not just a launch decision

**Pre-check:** head GT-3, GT-5 · ?-marked: none · lowest cited: none · Inputs ceiling: HIGH
**Confidence:** LOW — Inputs clean, but Inference axis is severely short: four separate hops each rest on an unpriced premise (A7, A13, A6, A14), exceeding the "at most one hop" bound for MEDIUM. Verification paths: A7 — Finance confirms cost/liability composition; A13 — set explicit KPI guardrails (churn/margin, not points-engagement) before launch; A6 — track the competitor's actual response (Cluster 3 tripwire, quarterly); A14 — build the holdout (Cluster 2 tripwire, pre-launch). Two-plus axes effectively short → LOW.

### Conclusion C6: The specific decision structure needed is a capped pilot with a built-in holdout, not a blanket launch or a blanket refusal

C1 (root cause unverified) + C4 (diagnose-first dominates) + C5 (measurement/margin risk)
→ the pre-mortem's two fatal-tier clusters — root-cause mismatch and unmeasurable attribution — are both closed by the same fix
→ that fix is running the diagnostic and building a holdout cohort before scaling spend
→ the pre-mortem's costly-but-survivable clusters — competitive arms race and liability lock-in — are addressed by capping initial exposure to a pilot tranche rather than the full $310K
→ fund a capped pilot gated on a same-window diagnostic read and a holdout design, reserving full-scale funding for the next board cycle once attributable evidence exists

**Pre-check:** head C1 (LOW), C4 (HIGH), C5 (LOW) · ?-marked: none directly · lowest cited: LOW · Inputs ceiling: LOW
**Confidence:** LOW — capped by citing C1 (LOW) and C5 (LOW) on its head; each carries its own verification path stated above (the diagnostic for C1, the guardrails/holdout/tripwires for C5). C4 (HIGH) does not rescue the overall band, since a chain is rated no higher than the lowest-rated chain its head cites — but C4's dominance is exactly why this LOW-confidence chain still yields an actionable recommendation rather than paralysis.

---

# 5. Abandoned Reasoning

### Dead End: Treat the competitor's simultaneous launch as proof that competitive-switching is the primary churn driver

**What was tried:** Inferring, from the timing coincidence alone, that the competitor's loyalty program is pulling members away and that matching it is therefore the right response.
**Why abandoned:** No company-specific evidence (exit survey, win/loss tagging) ties departing members to the competitor; treating temporal coincidence as causal would be reasoning by analogy/coincidence, which this methodology bars as direct evidence.
**What it ruled out:** Saves the analysis from recommending a purely competitive-response strategy (price-matching, rushed feature parity) on the strength of timing alone.

### Dead End: Recommend funding the full $310K program immediately because urgency forces action

**What was tried:** Arguing that doing nothing while churn is 62% above its prior baseline is clearly worse than funding the program now, so the 3-week deadline forces a "fund it" answer.
**Why abandoned:** Chain C4 shows a diagnose-first/pilot option is comparably fast, cheaper, and fully reversible — the premise that speed requires skipping diagnosis is false once a lightweight 2–3 week diagnostic is considered.
**What it ruled out:** Saves the analysis from a false "urgency forces bad process" argument and from framing the decision as "fund vs. do nothing" when a dominant third option exists.

### Dead End: Use "traditional loyalty programs typically retain 40–60% of members" as a direct estimate of this program's expected churn effect

**What was tried:** Anchoring the Fermi/theoretical-limit estimate on program-participant retention benchmarks.
**Why abandoned:** That figure measures how many enrollees keep participating in the loyalty program itself, not the delta in overall subscription churn attributable to the program — a metric mismatch, not a comparable benchmark.
**What it ruled out:** Saves the analysis from anchoring on a benchmark that answers a different question than the one being asked.

---

# 6. Conclusion

**Recommended approach:** Fund a capped, gated pilot — not the full $310,000/year, uncontrolled program — contingent on (1) a same-window (≤3-week) root-cause read using exit-survey and cohort/cause-coding data, and (2) a randomized holdout cohort built into the pilot so effect size is measurable at the next quarterly board update (chain C6).

**Key insight:** The single most robust finding here does not depend on resolving whether the loyalty-program hypothesis is even correct: running a fast, cheap root-cause diagnostic before committing dominates funding the program blind, on every decision criterion, under every plausible reweighting (chain C4). The real decision is not "fund vs. don't fund" — it is "commit money now on faith, or spend three weeks buying the evidence a $310K/year, hard-to-unwind commitment deserves."

**Trade-offs acknowledged:** This recommendation accepts a short delay in fully committing to (or definitively rejecting) the full loyalty program, in exchange for a defensible, board-presentable answer next quarter instead of an unmeasurable one now (chain C5, chain C6). It also accepts that the competitor's head start is not immediately countered at full scale — the marketing-optics cost of appearing to move slower than the competitor was not quantified in this analysis (no chain — flagged assumption only).

**Pre-check:** head C1 (LOW), C4 (HIGH), C5 (LOW), C6 (LOW) · ?-marked: none directly · lowest cited: LOW · Inputs ceiling: LOW
**Confidence:** LOW — driven by C1 (root cause undiagnosed; verification: the recommended exit-survey/cause-coding diagnostic) and C5 (four unpriced organizational/behavioral assumptions; verification: the named KPI guardrails, holdout, and quarterly tripwires), which cap C6. C4 is HIGH and needs no re-explanation. The LOW rating is not a flaw in this analysis — it is the honest reflection that the evidence needed to justify either "fund" or "don't fund" with confidence does not yet exist, which is precisely why the recommendation is to buy that evidence before committing the full spend.

**The specific 3-week deliverable, concretely:**
1. **Cause read:** a fast churn-cause tabulation from cancellation surveys/support-ticket tagging across the last two quarters, cross-cut by tenure cohort, acquisition channel, and self-reported reason (price / product / competitor / other) — doesn't need to be statistically bulletproof, needs to exist before the board date.
2. **Measurement design:** a pre-committed randomized holdout (15–20% of the pilot population excluded from the program) so the next quarterly update can report an attributable effect size, not just a raw churn number.
3. **Capped commitment:** approve a pilot-scale budget (roughly $75–100K, a fraction of the base, for two quarters) instead of the full $310K/year, with a pre-agreed re-approval checkpoint tied to the diagnostic and holdout results.