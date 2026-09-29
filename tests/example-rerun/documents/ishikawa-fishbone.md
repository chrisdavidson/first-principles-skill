## §6→§4 closure ledger (process output)

- "launch a parallel-track diagnostic (cohort/segment decomposition first, ticket-adoption correlation and pricing/competitive pull alongside it, win/loss interviews queued for the residual) together with a cheap, hypothesis-agnostic retention triage, before committing budget to any single named fix" → chain C5 ✓ (also supported by C4)
- "the two CS-flagged signals are better modeled as co-symptoms of a shared upstream driver than as independent causes" → chain C3 ✓
- "the sharp two-quarter inflection pattern systematically under-detects pricing and competitive-displacement causes" → chain C7 ✓
- "a rigorous diagnostic-before-fix posture carries real cost if the true driver is actively compounding while the team waits" → chain C4 ✓
- "the headline urgency figure (churn roughly doubling on a run-rate basis) is a magnitude illustration, not a forecast, and needs methodology verification before external use" → chain C6 ✓ (also supported by C1)
- "leadership's 'find the root cause' framing should be replaced with a multi-hypothesis, segment-aware investigation" → chain C2 ✓
- **Confidence** line → cites C1–C7 per D-07 ✓

## Assumption Audit scan (process output)

| Chain | Step | Step Text (brief) | Assumption surfaced? | Added to Table? |
|-------|------|--------------------|-----------------------|-------------------|
| C1 | 1 | cohort/denominator shift could alone produce the doubling | none (rests on A-1..A-4, already tabled) | n/a |
| C1 | 2 | reported % cannot be read as behavioral without recompute | none | n/a |
| C1 | 3 (concl.) | measurement-integrity check is a Phase-0 gate | none | n/a |
| C2 | 1 | six independently-sufficient conditions remain unruled-out | none (rests on A-7, A-8, already tabled) | n/a |
| C2 | 2 | multiple live causes lower the prior of one uniform cause | A-12 (categories roughly equally likely a priori) | yes |
| C2 | 3 (concl.) | single-cause framing should be replaced | none | n/a |
| C3 | 1 | both signals plausibly share one upstream mechanism | A-18 (shared-cause explanation beats direct one-signal-causes-other) | yes |
| C3 | 2 | a point fix on one signal risks missing the shared cause | none | n/a |
| C3 | 3 (concl.) | signals must be jointly time-correlated before treated as causal | none | n/a |
| C4 | 1 | a leadership-directed single-lever fix has low odds of hitting the true driver | A-12 (already added at C2, step 2) | n/a — already present |
| C4 | 2 [2nd, actor lens] | reallocating capacity to one lever can worsen the real driver | none | n/a |
| C4 | 3 [3rd, time lens] | delay destroys the evidence needed to diagnose correctly | none | n/a |
| C4 | 4 (concl.) | diagnose before committing to a specific fix | none | n/a |
| C5 | 1 | cohort decomposition dominates rival diagnostic options on every criterion | A-10 (Northbrook's systems already capture joinable cohort/rep/channel/ticket data) | yes |
| C5 | 2 | win/loss interviews are a second-wave activity | none | n/a |
| C5 | 3 (concl.) | sequence: cohort decomposition first, then parallel pulls, interviews last | none | n/a |
| C6 | 1 | compounding identity implies ~15.4%→~32.0% annualized run-rate | A-11 (churn events cluster at renewal anniversaries rather than distributing uniformly within a quarter) | yes |
| C6 | 2 | normalized ARR-at-risk brackets both show ~doubling | none | n/a |
| C6 | 3 (concl.) | urgency is real but figure is illustrative, not a forecast | none | n/a |
| C7 | 1 | sharp co-occurring inflection fits a shared discrete trigger better than slow structural drivers | A-13 (pricing/competitive categories are not simply confounded/lagged versions of the categories that do move the signals) | yes |
| C7 | 2 | absent signal is not evidence of absent cause for pricing/competitive | none | n/a |
| C7 | 3 (concl.) | provisional ranking: service-quality > onboarding/product > pricing/competitive (under-observed) | none | n/a |

Scan complete: 22 rows across 7 chains, one per chain step in order, no step skipped. 5 assumptions newly surfaced during Phase 4 (A-10, A-11, A-12, A-13, A-18); all 5 are reflected in the §2 Assumptions Table below (final, post-audit state).

## Self-audit scan (process output)

### Table 1 — chain form (section 4)

| Chain | Chain Head (brief) | Form conforming? | Rule applied | Dependency clean? | Band | Act attempted? | Edges fired |
|-------|---------------------|-------------------|---------------|--------------------|------|-----------------|-------------|
| C1 | GT-2, GT-6, GT-7?, GT-8?, GT-9?, GT-10? | yes | n/a | yes | LOW | yes | none |
| C2 | GT-5, GT-12?, GT-13? | yes | n/a | yes | LOW | yes | none |
| C3 | GT-3, GT-4, GT-12? | yes | n/a | yes | LOW | yes | none |
| C4 | GT-5, GT-2 | yes | n/a | yes | LOW | yes | none |
| C5 | GT-1, GT-2, GT-5, GT-6 | yes | n/a | yes | MEDIUM | yes | none |
| C6 | GT-1, GT-2, GT-14 | yes | n/a | yes | LOW | yes | none |
| C7 | GT-3, GT-4, GT-2, C3 | yes | n/a | yes | LOW | yes | none |

### Table 2 — claim inventory (section 6)

| §6 Span (brief) | Construct | Claim under R11? | R11 clause applied | Chain cited |
|-------------------|-----------|-------------------|----------------------|---------------|
| Recommended approach | bold lead-in | yes | colon closes the bold span | C5, C4 |
| Key insight | bold lead-in | yes | colon closes the bold span | C3, C7 |
| Provisional-ranking table (under Key insight) | prose/table | no | carries neither a bold colon lead-in nor a list marker | n/a |
| Trade-offs acknowledged | bold lead-in | yes | colon closes the bold span | C4, C6, C1, C2 (+ marked caveat: no chain — flagged assumption only, for the organizational-friction risk) |
| Pre-check | bold lead-in | yes | template note: the pre-check line is itself a claim, cited by the chains its own head names | C1, C2, C3, C4, C5, C6, C7 |
| Confidence | bold lead-in | yes | colon closes the bold span; D-07 requires naming every contributing chain below HIGH | C1, C2, C3, C4, C5, C6, C7 |

Scan complete: 7 chain rows, one per section-4 chain block in order; 6 section-6 rows, one per construct in order — 5 claims under R11, 1 excluded. 0 chains malformed, 0 claims untraced.

## Adversarial pass (process output)

**Recompute.** GT-14's compounding identity independently recomputed: (1−0.041)^4 = 0.959^4 = 0.845813 → annualized churn ≈ 15.42% (matches chain C6). (1−0.092)^4 = 0.908^4 = 0.679741 → annualized churn ≈ 32.03% (matches chain C6). ARR-at-risk per 100 accounts recomputed independently: at $18k ACV, base ARR = $1.8M; ×15.42% = $277,560 (Q1) and ×32.03% = $576,540 (Q3). At $40k ACV, base ARR = $4.0M; ×15.42% = $616,800 (Q1) and ×32.03% = $1,281,200 (Q3). All four figures match chain C6 as stated — both bracket ends show a factor of ~2.07–2.08 increase.

**Sensitivity.** The single ground truth whose falsity would most flip the analysis's posture is **GT-7?** (churn-calculation methodology held constant across Q1–Q3). It is `?`-marked. If GT-7? were confirmed true — along with GT-8?, GT-9?, GT-10? — chain C1's LOW rating would move toward HIGH and the "verify measurement before causal work" urgency would soften; the diagnostic-sequencing (C5) and diagnose-before-fix (C4) conclusions would still largely hold, since they do not solely depend on measurement doubt. GT-7? is exactly the first item the recommended cohort/segment decomposition (Option A, chain C5) would resolve.

**Rival.** Strongest rival to the headline conclusion: *leadership's instinct is directionally right — the co-moving signals point at service-quality/support-capacity, and the fastest path to stopping the bleeding is an immediate support-capacity surge run in parallel with a lighter diagnostic, rather than sequencing cohort analysis first.* This rival is not fully ruled out; it is partially absorbed by the pre-mortem's Cluster 2 disposition below, which converts the plan from strictly sequential to parallel-track (diagnose **and** triage), rather than settling the rival outright. This is disclosed on the Conclusion's confidence line rather than claimed as settled. Per-chain rivals are named on each chain's own confidence line in section 4 (C1: "the rise is a clean behavioral signal"; C2: "there is one dominant, uniform cause after all"; C3: "one signal directly causes the other rather than sharing an upstream cause"; C5: "internal data alone can fully resolve all six categories"; C6: "9.2% is already an annualized figure, so no further compounding should be applied"; C7: "competitive displacement is dominant and the ticket/adoption rise is an unrelated coincidence").

**Premise.** It is roughly Q4 2026/early Q1 2027. The diagnostic sprint has already failed badly: leadership still does not know what is driving churn, no effective action has been taken, and churn has kept climbing. What caused it?

**Causes** (unfiltered, from four viewpoints — the RevOps analyst executing the pull, the CS/support leader living with the result, the CFO paying for it, and a competitor who benefits from Northbrook's paralysis):
- Northbrook's CRM/billing/ticketing systems are not actually integrated or query-able the way A-10 assumed; the cohort pull takes six weeks instead of days because rep/channel fields are inconsistently populated.
- The churn-event categorization taxonomy turns out to be inconsistent across sales and finance, so the team cannot agree what counts as "churned" even after pulling the data, and the diagnostic stalls in definitional debate.
- While the diagnostic runs, leadership tells everyone to "wait for the data"; support/CS stays under-resourced the whole time, and if service-quality is the real driver it keeps degrading, unmeasured, in the background.
- CS's own informally-flagged at-risk accounts get no proactive outreach because "the formal study is in progress," and several are lost that a phone call could have saved.
- The board demands an answer before the six-week window closes, and leadership pre-announces a fix (e.g., a price cut) under pressure before the diagnostic finishes, defeating the point of running it at all.
- Findings arrive as an undifferentiated data dump with no clear recommendation, so leadership cannot decide, and another six weeks is spent "aligning" instead of acting.
- A competitor uses the delay window to actively target Northbrook's known at-risk accounts, converting slow diagnosis into accelerated losses in exactly the segment most worth saving.
- The win/loss interview program never reaches a usable sample size, because customers who have already churned do not respond to outreach, and the option silently produces nothing.
- Rep-level and channel-level churn attribution turns out to be organizationally sensitive; the sales organization resists sharing it, and the sales-qualification/ICP-fit hypothesis (A-6) never gets tested because of internal politics.

**Clusters:**
- **Diagnostic execution risk** — systems not actually integrated (A-10), inconsistent categorization taxonomy (A-1/GT-7?), win/loss response-rate collapse. Bears on: chain C5, GT-7?, GT-9?.
- **Cost of waiting** — no interim retention action, at-risk accounts lost during the wait, competitor poaching during the vulnerability window. Bears on: chain C4, the Recommended-approach claim.
- **Governance/political risk** — premature fix announcement under board pressure, sales-org resistance to rep-level data sharing, an undecipherable findings dump causing a second delay cycle. Bears on: chain C5, chain C7, the Recommended-approach claim.

**Disposition:**
- *Diagnostic execution risk* — **mitigation**: a one-day systems-readiness check before committing the six-week timeline; if CRM/billing/ticketing fields are not joinable, add two weeks and disclose that up front rather than discovering it mid-sprint. Owner: RevOps lead.
- *Cost of waiting* — **plan change**: the diagnostic must run in parallel with, not before, a cheap, hypothesis-agnostic retention triage — proactive outreach to CS's existing informally-flagged at-risk accounts, plus a support-backlog/staffing check — that does not presuppose any specific root cause and therefore cannot itself be "the wrong fix." This revision is already folded into chain C5's and the Recommended-approach's final wording above.
- *Governance/political risk* — **mitigation**: secure an executive sponsor (CEO or COO) who commits publicly to a fixed decision date after the diagnostic, has authority to require rep/channel-level data sharing from sales, and pre-briefs the board so a firm recommendation is expected on that date rather than sooner.

**Tripwires:**
- Diagnostic execution risk: if RevOps cannot produce a joined cohort/rep/channel/ticket table by day 3 of week 1, escalate immediately. Owner: RevOps lead, checked daily in week 1.
- Cost of waiting: if the number of informally-flagged at-risk accounts receiving zero proactive outreach in any given week exceeds five, escalate. Owner: CS lead, checked weekly.
- Governance/political risk: any public or board communication naming a specific fix (price change, product-roadmap commitment) before the diagnostic's committed decision date is itself the tripwire. Owner: CEO/executive sponsor, monitored continuously.

**Falsification.** The conclusion is false if a rigorous six-week diagnostic, run in parallel with the cheap universal triage, fails to produce a decision-actionable (≥MEDIUM confidence) hypothesis ranking by the committed date, or if running it causes churn to accelerate faster than a no-diagnostic baseline would have.

## Techniques not applied (process output)

- theoretical-limit — not applicable — no governing hard constraint (physical law, conservation identity, protocol minimum) bounds a SaaS company's churn rate; industry benchmark churn figures are conventions, not physical ceilings, so deriving an "ideal floor" would misrepresent a business/behavioral problem as a physics problem. The compounding identity used in chain C6 is a mathematical definition applied for magnitude-estimation, not a theoretical-limit derivation.
- inversion (Phase 5 adversarial-technique invocation) — not applicable — the headline conclusion is a plan (a sequenced, six-week diagnostic-and-triage investigation with named owners and tripwires), not a bare claim, so pre-mortem is the prescribed tool per the pre-mortem/inversion decision rule stated in both companion documents; inversion was already applied at Phase 2 (see the Inversion analysis feeding chain C2 and the Assumptions Table) and is not re-invoked here.

## Self-Audit Gate (process output)

**Criterion 1: Identify Essence**
Quoted span: "Determine whether Northbrook's quarterly churn rate more than doubling (4.1%→9.2%, Q1→Q3 2026) reflects one identifiable, fixable driver or a superposition of several of six candidate drivers ... and build a falsifiable, sequenced diagnostic plan that distinguishes among them before any fix is funded."
Band: **Rigorous**
Justification: the statement names the underlying decision (single-vs-multi-driver diagnosis, plan-before-fix) rather than restating the leadership prompt or the raw churn figures, and each of the four success criteria is a checkable verb+subject+outcome triplet against section 6 (hypothesis set spanning six categories, ranked falsifiable sequence, provisional ranking with confidence levels, separation of reported figures from their behavioral interpretation).

**Criterion 2: Challenge Assumptions**
Quoted span (from the Assumption Audit scan): "5 assumptions newly surfaced during Phase 4 (A-10, A-11, A-12, A-13, A-18); all 5 are reflected in the §2 Assumptions Table below (final, post-audit state)."
Band: **Rigorous**
Justification: all 18 rows use the four-type scheme, Verdict cells use the token+em-dash form (including a Discard verdict on A-5, not merely Accept everywhere), Verification cells are specific ("unverified — flagged (feeds GT-N?, chain Cn)") rather than generic, and the Assumption Audit scan confirms the audit ran exhaustively over all 22 named chain steps with no step skipped.

**Criterion 3: Establish Ground Truths**
Quoted span: "GT-1, GT-3, GT-4, GT-6 and GT-14 are unsuffixed and reachable (read at source in the prompt or by direct computation), but each feeds only MEDIUM- or LOW-confidence chains rather than anchoring a HIGH chain of its own."
Band: **Sound**
Justification: GT-IDs are stable, provenance labels are present throughout, and the `?`-enumeration ("?-marked: GT-7, GT-8, GT-9, GT-10, GT-11, GT-12, GT-13 — 7 of 14") matches the Ground Truths list on inspection — but several reachable unsuffixed GTs feed only MEDIUM/LOW chains without a Phase 3 unreachable-source record justifying that (they are reachable; the reasoning built on top of them is simply inherently uncertain at this diagnostic stage), which is the specific, named gap the Sound band exists for.

**Criterion 4: Reason Upward**
Quoted span (from the self-audit scan, Table 1): "C1 | ... | yes | n/a | yes | LOW | yes | none" through "C7 | ... | yes | n/a | yes | LOW | yes | none" — all seven rows read `Form conforming? = yes`, `Dependency clean? = yes`.
Band: **Rigorous**
Justification: every conclusion has exactly one chain, every chain has a genuine intermediate (verified by the scan's exhaustive per-chain rows), no chain references an undefined GT-ID, no analogy is used as direct evidence anywhere in the document, every chain step that introduces a new assumption carries an inline `[Assumes: A-N]` mark (confirmed exhaustively by the Assumption Audit scan), and the Abandoned Reasoning section documents three specific dead ends with named structural reasons rather than using the escape valve.

**Criterion 5: Validate**
Quoted span (from the Adversarial pass record): "Falsification. The conclusion is false if a rigorous six-week diagnostic, run in parallel with the cheap universal triage, fails to produce a decision-actionable (≥MEDIUM confidence) hypothesis ranking by the committed date, or if running it causes churn to accelerate faster than a no-diagnostic baseline would have."
Band: **Rigorous**
Justification: every chain's confidence line names its own `?`-inputs with a verification path, or its own unassumed-premise/rival shortfall with what would close it; the ceiling rule is correctly applied (C7 is capped LOW because it cites C3, itself LOW); no chain is rated HIGH while consuming a `?` input; and the full adversarial-pass record (recompute, sensitivity, rival, past-tense premise, an unfiltered nine-item cause list from four viewpoints, three named clusters each bearing chain/GT citations, a named plan change or accepted-risk-with-mitigation per cluster, and a falsification condition) is present and complete — a MEDIUM/LOW-heavy but internally calibrated document is the expected shape of an honest diagnostic-stage analysis, not a shortfall, per this criterion's own governing clause.

**Criterion 6: Conclusion-to-Ground-Truth Traceability**
Quoted span (from the self-audit scan, Table 2): "Trade-offs acknowledged | bold lead-in | yes | colon closes the bold span | C4, C6, C1, C2 (+ marked caveat: no chain — flagged assumption only, for the organizational-friction risk)"
Band: **Sound**
Justification: four of the five Conclusion-section claims trace cleanly to named chains with no new reasoning introduced, and the Key Insight states a non-obvious finding (the CS-flagged signals are more likely co-symptoms than causes, and the absence of a signal is not evidence of an absent cause) rather than restating the Recommended approach — but the Trade-offs-acknowledged claim carries one caveat (organizational-friction risk from discarding the single-owner framing) using the explicit `no chain — flagged assumption only` marker, which the template defines as honestly disclosed but still untraced, placing this criterion at Sound rather than Rigorous.

**Gate result:** 0 criteria Absent; 0 criteria Hand-wavy (2 Sound, 4 Rigorous). Both gate conditions are cleared on the first pass — no re-perception pass is triggered.

---

# Northbrook Analytics — Churn Root-Cause Diagnostic: A First-Principles Analysis

## 1. Problem Essence

**Core problem:** Determine whether Northbrook's quarterly churn rate more than doubling (4.1%→9.2%, Q1→Q3 2026) reflects one identifiable, fixable driver or a superposition of several of six candidate drivers (offer/product gaps, pricing pressure, onboarding failure, service-quality degradation, competitive displacement, or a sales-qualification/ICP mismatch), and build a falsifiable, sequenced diagnostic plan that distinguishes among them before any fix is funded.

**Success criteria:**
1. Names a set of testable hypotheses spanning all six candidate categories, each paired with a discriminating observation that can be checked against the investigation plan in section 6.
2. Produces a ranked, falsifiable diagnostic sequence — which data pull happens first, second, third, with named owners and a timeline — checkable against chain C5 in section 4.
3. States a provisional hypothesis ranking with an explicit confidence level for each entry, checkable against chain C7's ranking table in section 4.
4. Explicitly separates "the reported percentage figures" (given, GT-2) from "what those figures mean behaviorally" (unverified, GT-11?), checkable against chain C1 and the provenance labels in section 3.

A skeptic reading this statement should agree it names the actual decision leadership needs made — not "why did churn rise" taken as a rhetorical given, and not "how do we stop churn" taken as a solved problem — but "do we know enough to act, and if not, what is the fastest falsifiable way to find out."

## 2. Assumptions Table

### Supporting work: Fishbone (breadth-first cause map)

**Effect:** "Quarterly churn rate rose from 4.1% to 9.2% between Q1 and Q3 2026."

Category set chosen by domain signal: rather than the generic six-category default, this uses a set built directly from leadership's five named categories plus one leadership left out (Sales Qualification & ICP Fit) — locked before brainstorming began.

| Category | Candidate causes | Discriminating observation |
|---|---|---|
| **Product/Offer Gaps** | missing feature vs. a named competitor; a product regression/bug in a recent release; an integration/data-source breakage | win/loss notes naming a specific feature gap; ticket-volume spikes aligned to a release date; integration-error ticket category rising specifically |
| **Pricing & Packaging** (A-16) | list-price increase or reduced renewal discounting; packaging change removing a previously-included capability; unfavorable contract-term change | renewal-quote vs. original-quote delta for churned accounts; churned accounts' plan-tier/SKU history; contract-term field on churned vs. retained accounts |
| **Onboarding & Implementation** | lengthened time-to-value for recent cohorts; onboarding-team capacity/turnover; a self-serve onboarding change removing high-touch support recent cohorts needed | adoption-score trend for cohorts <6 months old vs. mature cohorts; onboarding-completion-time trend by cohort; churn-by-cohort-age correlated with onboarding-model flag |
| **Service Quality (Support/CS)** (A-14) | support headcount reduction or turnover; SLA/response-time degradation; a support-tooling or outsourcing change | staffing-to-ticket ratio trend; first-response/resolution-time trend; CSAT/reopen-rate trend around the change date |
| **Competitive Displacement** (A-17) | a well-funded competitor entered/expanded in-segment; a competitor's pricing move undercut Northbrook; a platform/ecosystem shift reduced need for a standalone tool | win/loss notes and rep-reported competitive mentions; exit-interview mentions of a named competitor's price; churned accounts' primary data-warehouse/platform vendor |
| **Sales Qualification & ICP Fit** (A-6) | a prior-period growth push loosened ICP criteria or discounting to hit bookings, producing a wave of poor-fit accounts now reaching first renewal; a newer, lower-quality acquisition channel; expansion into a sub-segment the product doesn't yet serve well | churn rate by signup cohort and by originating sales rep/channel; churn rate by acquisition channel; churn rate by firmographic segment |

No branch here can yet be marked "verified" — every discriminating observation names data this analysis does not have access to. The sixth category is deliberately not one of leadership's original five: it exists specifically to test the assumption (A-6) that churn is a CS/product problem rather than a problem upstream of CS entirely.

### Supporting work: Inversion (failure-guaranteeing conditions)

**Claim:** "There is a single, product/CS-attributable root cause for the churn increase, and fixing it will restore Q1 churn levels."
**Inverted:** "There is no single root cause — the increase is not attributable to one fixable product/CS root cause, and fixing any one candidate will not restore Q1 churn levels."

**Failure-guaranteeing conditions (at least five, unfiltered):**
1. Two or more of the six categories are simultaneously operative (e.g., a support-staffing cut and a competitor launch land in the same window).
2. The rise is a measurement/cohort artifact — a denominator shift or cohort-timing cluster — rather than a behavior change at all.
3. The two CS-flagged signals are downstream co-symptoms of a shared upstream cause rather than themselves causal.
4. The true driver sits upstream of CS entirely (sales-qualification/ICP mismatch in cohorts signed 6–12 months earlier), outside CS's or product's control.
5. A pricing/packaging change, or a competitor's pricing move, is driving cancellations independent of product quality, so product/CS investment would not move the number.
6. Churn is concentrated in one segment/rep/channel rather than uniform, so "the root cause" is heterogeneous across cohorts and a single company-wide fix addresses only part of the base.

**Necessary preconditions for leadership's claim to hold, and load-bearing tags:**

| Precondition | Load-bearing? | Status |
|---|---|---|
| The churn-calculation methodology, denominator, and event-categorization were stable across Q1–Q3 | **load-bearing** | unverified (A-1, A-2, A-3) |
| The active base is large enough that this isn't small-sample noise | **load-bearing** | unverified (A-4) |
| Churn is distributed roughly uniformly across segment/size/rep/channel | **load-bearing** | unverified (A-8) |
| No pricing change or competitive launch coincided with this window | not load-bearing alone (affects only categories b/e) | unverified (A-9) |
| The two CS-flagged signals are causally upstream of churn, not co-symptoms | **load-bearing** for the "CS/product owns the fix" framing specifically | unverified (A-7) |

Three of five preconditions are both load-bearing and currently unverified — per the inversion procedure, this is the analysis's sharpest finding and is reported ahead of the fuller list: **leadership's framing rests on exactly the claims nobody has checked yet.**

### Classified Assumptions Table (post Phase-4 Assumption Audit — final state)

| Assumption | Type | Treatment | Verdict | Verification |
|---|---|---|---|---|
| A-1: The churn-calculation methodology (formula, denominator, categorization taxonomy) was held constant across Q1–Q3 2026 | untested belief | Verify before use in causal reasoning | Challenge — em-dash — central to whether GT-2 reflects behavior or artifact | unverified — flagged (feeds GT-7?, chain C1) |
| A-2: The active-customer denominator's segment/cohort/channel composition was comparable across Q1–Q3 2026 | untested belief | Verify before use | Challenge — an unrelated sales surge or cohort-timing cluster could shift the denominator alone | unverified — flagged (feeds GT-8?, chain C1) |
| A-3: Customers counted as "churned" reflect genuine voluntary non-renewal, not miscategorized events | untested belief | Verify before use | Challenge — categorization drift would inflate GT-2 without any behavior change | unverified — flagged (feeds GT-9?, chain C1) |
| A-4: The active customer base is large enough that the 4.1%→9.2% move is not small-sample noise | untested belief | Verify before use | Challenge — no customer count is given to check this | unverified — flagged (feeds GT-10?, chain C1) |
| A-5: There is a single root cause of the churn increase (leadership's implicit framing) | convention | Explicitly challenge before accepting | Discard — em-dash — the inversion analysis above names six independently-sufficient conditions that remain live and unruled-out, so a single-cause framing is unsupported; replaced with a multi-hypothesis framing | n/a — discarded, feeds chain C2 |
| A-6: Churn is a CS/product problem, not a sales-qualification or pricing/packaging problem | convention | Explicitly challenge before accepting | Challenge — no evidence yet distinguishes an upstream sales/pricing driver from a CS/product driver; added as fishbone category 6 specifically to test this framing | unverified — flagged (feeds fishbone category 6, chain C7) |
| A-7: The two CS-flagged signals (tickets, adoption) are causes of churn, not co-symptoms of a shared upstream driver | untested belief | Verify before use | Challenge — a shared-upstream-cause model fits the co-occurrence at least as well | unverified — flagged (feeds GT-12?, chains C2, C3) |
| A-8: Churn is distributed roughly uniformly across segment, contract size, sales rep, and acquisition channel | untested belief | Verify before use | Challenge — a concentrated pattern would point at a narrower, heterogeneous cause set | unverified — flagged (feeds GT-13?, chains C2, C5) |
| A-9: No pricing change or competitive product/pricing launch coincided with this window | untested belief | Verify before use | Challenge — neither is ruled out by anything in the prompt | unverified — flagged (feeds inversion condition 5, fishbone categories 2 & 5) |
| A-10: Northbrook's CRM/billing/ticketing systems already capture cohort/rep/channel/ticket data in a joinable, query-able form | untested belief | Verify before use | Challenge — surfaced during Phase 4 (chain C5); if false, C5's speed/cost scores are too optimistic | unverified — flagged (feeds chain C5, surfaced by Assumption Audit) |
| A-11: Churn events cluster at annual renewal anniversaries rather than distributing uniformly within each quarter | untested belief | Verify before use | Challenge — surfaced during Phase 4 (chain C6); bears on whether the compounding model is a valid read of the mechanism | unverified — flagged (feeds chain C6, surfaced by Assumption Audit) |
| A-12: The six candidate categories are roughly equally likely a priori | untested belief | Verify before use | Challenge — surfaced during Phase 4 (chains C2, C4); if one category is far more likely a priori, the "blind pick" reasoning weakens | unverified — flagged (feeds chains C2, C4, surfaced by Assumption Audit) |
| A-13: Categories that would not move ticket/adoption metrics (pricing, competitive) are not simply confounded or lagged versions of the categories that do | untested belief | Verify before use | Challenge — surfaced during Phase 4 (chain C7); crux of why an absent signal is treated as inconclusive, not exculpatory | unverified — flagged (feeds chain C7, surfaced by Assumption Audit) |
| A-14: The rise in support-ticket volume reflects genuine product friction, not a change in ticket-logging policy | untested belief | Verify before use | Challenge — a policy/categorization change would inflate counts without any product-experience change | unverified — flagged (fishbone: Product/Offer, Service Quality; feeds chain C3) |
| A-15: The decline in adoption scores reflects genuine reduced usage, not a change in how the score is computed | untested belief | Verify before use | Challenge — a scoring-model or feature-set change could move the metric independent of behavior | unverified — flagged (fishbone: Product/Offer; feeds chain C3) |
| A-16: No mid-2026 pricing/packaging change took effect that would explain a rise in renewal cancellations | untested belief | Verify before use | Challenge — not addressed anywhere in the given context | unverified — flagged (fishbone: Pricing & Packaging) |
| A-17: No named competitor launched a materially cheaper/more capable offering targeting this segment in this window | untested belief | Verify before use | Challenge — not addressed anywhere in the given context | unverified — flagged (fishbone: Competitive Displacement) |
| A-18: The ticket/adoption correlation is better explained by one shared upstream cause than by one signal directly driving the other | untested belief | Verify before use | Challenge — surfaced during Phase 4 (chain C3); an independent "frustration spiral" is a live alternative model | unverified — flagged (feeds chain C3, surfaced by Assumption Audit) |

**Stakes-escalation note:** A-1, A-2, A-3, A-7, and A-8 are the highest-stakes rows — every downstream causal chain in section 4 ultimately rests on at least one of them, and none currently rises above "untested belief." This is why chain C1 (measurement-integrity check) is sequenced first in the recommended investigation, ahead of any hypothesis-specific data pull.

## 3. Ground Truths

### Supporting work: 5-Whys reduce-to-primitives (irreducibility drill on the churn-rate claim)

**Claim:** "Northbrook's churn rate rose from 4.1% to 9.2% between Q1 and Q3 2026, reflecting a real, unified increase in customer-driven cancellation behavior."

**Immediate constituents and irreducibility test:**
1. **Definition stability** — one documented churn formula applied identically each quarter → not statable from the given context → **Assumed — unverified** (A-1).
2. **Denominator comparability** — the active-base composition wasn't diluted/concentrated by an unrelated sales surge or cohort-timing cluster → not statable → **Assumed — unverified** (A-2).
3. **Numerator integrity** — churn events are genuine voluntary cancellations, not M&A/downgrade miscategorization → not statable → **Assumed — unverified** (A-3).
4. **Sample-size adequacy** — the base is large enough that a doubling isn't a handful of accounts → no customer count is given → **Assumed — unverified** (A-4).
5. **Measurement-window definition** — what "quarterly churn" means against an annually-renewing base is itself ambiguous (this is the tension the prompt explicitly flags) → **Assumed — unverified**, and load-bearing for every branch above it.

**Verdict on the parent claim:** all five branches are unverified, so the *interpretation* of the churn rise as "a real, unified, behavior-driven increase" is **not yet verified** — it becomes GT-11? below. The *narrower* claim — "these two percentages were reported to leadership" — requires none of the five branches and is directly stated, so it stands as GT-2 without a `?`.

### Ground Truths list

- **GT-1** Northbrook sells a B2B SaaS data-integration/reporting platform to mid-market operations teams; annual contracts run $18,000–$40,000, renewing yearly. — source: problem statement; read-at-source: opening paragraph of the given context.
- **GT-2** Quarterly churn rate, as reported to leadership, was 4.1% in Q1 2026 and rose to 9.2% by the end of Q3 2026. — source: problem statement; read-at-source: "THE DATA POINT" paragraph.
- **GT-3** Customer Success has flagged rising support-ticket volume as a signal, explicitly not yet causally linked to churn. — source: problem statement; read-at-source: "SIGNALS ALREADY FLAGGED" bullet list.
- **GT-4** Customer Success has flagged declining feature-adoption scores as a signal, explicitly not yet causally linked to churn. — source: problem statement; read-at-source: same bullet list.
- **GT-5** No causal attribution has yet been performed connecting the churn increase to any of the six candidate driver categories. — source: problem statement; read-at-source: "WHAT IS EXPLICITLY UNKNOWN" paragraph.
- **GT-6** Contracts renew annually while churn is reported quarterly, creating a structural ambiguity — explicitly flagged in the prompt as worth surfacing — about what "quarterly churn" is measured against. — source: problem statement; read-at-source: the parenthetical following the contract-value figures.
- **GT-7?** The churn-calculation methodology (formula, denominator definition, categorization taxonomy) was held constant across Q1–Q3 2026. — provenance: unverified. *Phase 3 failure record: source would be "Northbrook's internal RevOps churn-calculation documentation"; unreachable because no such internal system or document is provided in, or accessible from, this diagnostic exercise — this is precisely the first item the recommended data pull (chain C5, Option A) must retrieve.*
- **GT-8?** The active-customer denominator's segment/cohort/channel composition was comparable across Q1–Q3 2026. — provenance: unverified. *Phase 3 failure record: source would be "Northbrook's CRM/billing cohort records"; unreachable, same reason as GT-7?.*
- **GT-9?** Customers counted as "churned" in Q3 reflect genuine voluntary non-renewal rather than miscategorized events. — provenance: unverified. *Phase 3 failure record: source would be "Northbrook's churn-event categorization taxonomy"; unreachable, same reason.*
- **GT-10?** The active customer base is large enough that the reported move is a statistically meaningful behavioral shift, not small-sample noise. — provenance: unverified. *Phase 3 failure record: source would be "Northbrook's active-customer count by quarter"; unreachable, same reason.*
- **GT-11?** The reported churn rise reflects a real, comparable, behavior-driven increase in customer-initiated cancellation (the five-whys parent claim above). — provenance: unverified; contingent on GT-7?–GT-10? all resolving true.
- **GT-12?** The two CS-flagged signals (ticket volume, adoption decline) are causally upstream of churn rather than co-symptoms of a shared third driver. — provenance: unverified (elevates A-7 for use in a chain).
- **GT-13?** Churn is distributed roughly uniformly across customer segment, contract size, sales rep, and acquisition channel. — provenance: unverified (elevates A-8 for use in a chain).
- **GT-14** A quarterly logo-churn rate that is constant within a period compounds geometrically across four quarters under the standard retention identity: annual_churn = 1 − (1 − quarterly_churn)⁴. — source: mathematical definition; read-at-source: definitional, independently recomputed in the Adversarial pass record above.

**Provenance summary:**
```text
?-marked: GT-7, GT-8, GT-9, GT-10, GT-11, GT-12, GT-13 (7 of 14)
Read-at-source: GT-1 — opening paragraph; GT-2 — "THE DATA POINT" paragraph; GT-3, GT-4 — CS-signals bullets; GT-5 — "WHAT IS EXPLICITLY UNKNOWN" paragraph; GT-6 — contract-value parenthetical; GT-14 — retention-compounding identity, recomputed independently
```

No assumption carrying a Discard verdict (A-5) appears in this list. IDs are stable throughout the document.

## 4. Derivation Chains

### Conclusion C1: The churn figures cannot yet be trusted as a pure behavioral signal

GT-2 (reported churn 4.1%→9.2%) + GT-6 (quarterly-report vs. annual-renewal ambiguity) + GT-7? (methodology-stability unverified) + GT-8? (denominator-comparability unverified) + GT-9? (categorization-integrity unverified) + GT-10? (sample-size-adequacy unverified)
→ a cohort-mix or denominator shift alone could produce the doubling shown in GT-2 without any change in customer behavior
→ the reported percentages cannot yet be read as a behavioral signal without a cohort-level recompute that checks methodology, denominator, categorization, and sample size
→ Northbrook must treat measurement-integrity verification as a Phase-0 diagnostic gate that precedes any causal hypothesis test, not an optional side-check

**Pre-check:** head GT-2, GT-6, GT-7?, GT-8?, GT-9?, GT-10? · ?-marked: GT-7?, GT-8?, GT-9?, GT-10? · lowest cited: none · Inputs ceiling: MEDIUM
**Confidence:** LOW — Inputs axis short: GT-7?, GT-8?, GT-9?, GT-10? are all unverified; verification path is the cohort/rep/channel-joined churn table and the churn-event categorization taxonomy (chain C5, Option A). Inference axis also short: the claim that a denominator/cohort shift *could* explain the doubling is a live possibility asserted here, not yet demonstrated against actual cohort data. Rivals axis also short: "the rise is a clean, uncorrupted behavioral signal" remains a live, unruled-out rival. Two axes short → LOW.

### Conclusion C2: A single, uniform root cause is unlikely

GT-5 (no causal attribution done) + GT-12? (signals-as-upstream-cause unverified) + GT-13? (uniform cross-cohort distribution unverified)
→ the inversion analysis names six independently-sufficient conditions that could each alone produce this pattern, and none of them is yet ruled out
→ when multiple independently-sufficient causes remain live and unruled-out, the prior probability that exactly one of them is the uniform root cause across the whole customer base is low [Assumes: A-12]
→ leadership's singular "root cause" framing should be replaced with a multi-hypothesis, segment-aware investigation that expects two or three concurrent drivers affecting different cohorts rather than one uniform defect

**Pre-check:** head GT-5, GT-12?, GT-13? · ?-marked: GT-12?, GT-13? · lowest cited: none · Inputs ceiling: MEDIUM
**Confidence:** LOW — Inputs axis short: GT-12?, GT-13? unverified; verification path is the cohort/segment decomposition and the ticket-adoption correlation study (chain C5, Options A and B). Inference axis also short: hop 2 rests on A-12 (categories roughly equally likely a priori), not yet priced — if one category is known to dominate a priori, the "low probability of one uniform cause" argument weakens. Rivals axis also short: "there is one dominant cause affecting the whole base uniformly" remains live. Two axes short → LOW.

### Conclusion C3: The two CS-flagged signals are likely co-symptoms, not independent causes

GT-3 (rising ticket volume) + GT-4 (declining adoption scores) + GT-12? (signals-as-cause unverified)
→ both signals plausibly share one upstream mechanism — a product change, a support-capacity cut, or an onboarding-quality drop that simultaneously frustrates users into filing tickets and reduces the feature usage adoption scores measure [Assumes: A-18]
→ treating either signal alone as the driver and building a point fix around it risks resolving a symptom while the shared upstream cause keeps operating
→ both signals must be jointly time-correlated against a candidate upstream event before either is treated as causal on its own

**Pre-check:** head GT-3, GT-4, GT-12? · ?-marked: GT-12? · lowest cited: none · Inputs ceiling: MEDIUM
**Confidence:** LOW — Inputs axis short: GT-12? unverified; verification path is chain C5 Option B (the ticket/adoption-to-churn correlation study). Inference axis also short: hop 1 rests on A-18 (shared-upstream-cause model), not yet priced against the live alternative that one signal directly drives the other. Rivals axis also short: "tickets independently cause adoption decline via a frustration spiral, or vice versa" is live and unruled-out. Two axes short → LOW.

### Conclusion C4: Diagnose before committing to a specific fix

GT-5 (no causal attribution done) + GT-2 (churn more than doubled in two quarters)
→ with six live candidate categories and zero causal attribution completed, a leadership-directed fix aimed at the most visible lever has a low chance of targeting the actual dominant driver [Assumes: A-12]
→[2nd, actor lens] committing budget or headcount to one lever reallocates capacity away from the others, and if the real driver sits in a different category that reallocation can worsen the actual driver while leadership believes it has acted
→[3rd, time lens] each additional quarter spent on a misdirected fix is a quarter in which affected cohorts churn out entirely, destroying the evidence needed to diagnose them correctly
→ the cost of a bounded diagnostic sprint is small relative to the compounding cost of misdiagnosis, so Northbrook should authorize the diagnostic before authorizing any specific fix

**Pre-check:** head GT-5, GT-2 · ?-marked: none · lowest cited: none · Inputs ceiling: HIGH
**Confidence:** LOW — Inputs axis clean (both head GTs unsuffixed). Inference axis short: hop 1 rests on A-12 (equal-prior across categories), not yet priced. Rivals axis short: the strongest live rival — act now with an immediate support-capacity surge run alongside a lighter diagnostic, rather than sequencing rigor first (named in full in the Adversarial pass record) — is only partially absorbed by chain C5's parallel-track sequencing, and remains unsettled within this chain's own scope. Two axes short → LOW; a clean Inputs axis does not by itself lift a chain whose Inference and Rivals axes are both short.

### Conclusion C5: Sequence the diagnostic — cohort decomposition first, unconditionally

GT-1 (contract structure: annual, $18k-$40k) + GT-2 (churn 4.1%→9.2%) + GT-5 (no causal attribution done) + GT-6 (quarterly/annual measurement ambiguity)
→ weighted scoring across six decision criteria shows the cohort/segment churn decomposition scoring at or above every rival diagnostic option on every individual criterion, making it a dominant choice rather than merely a highest-weighted total [Assumes: A-10]
→ the win/loss interview program scores highest on diagnostic value alone but lowest on speed, cost, and data reliability, marking it a second-wave activity once the cheaper data pulls have narrowed the hypothesis space
→ Northbrook should launch the cohort/segment decomposition immediately and unconditionally, run the ticket-adoption correlation study and the pricing/competitive-intel pull alongside it, and reserve the win/loss interview program for the competitive and pricing hypotheses the cheaper pulls cannot resolve

**Pre-check:** head GT-1, GT-2, GT-5, GT-6 · ?-marked: none · lowest cited: none · Inputs ceiling: HIGH
**Confidence:** MEDIUM — Inputs axis clean. Inference axis short: hop 1 rests on A-10 (Northbrook's systems already capture joinable cohort/rep/channel/ticket data), not yet verified; verification path is the one-day systems-readiness check named in the Adversarial pass record's Cluster-1 disposition. Rivals axis addressed within this chain's own conclusion: the residual rival ("internal data alone cannot fully resolve competitive/pricing hypotheses") is explicitly priced in by reserving the win/loss interview program for exactly that residual. One axis short → MEDIUM.

### Conclusion C6: The urgency is real in magnitude, but the figure is illustrative, not a forecast

GT-1 (contract value range $18k-$40k) + GT-2 (churn 4.1%→9.2%) + GT-14 (compounding identity)
→ applying the compounding identity to both reported rates yields an implied annualized logo-churn rate near 15.4 percent from the Q1 figure, rising to near 32.0 percent from the Q3 figure, if either quarter's rate persisted for a full year [Assumes: A-11]
→ normalizing to a 100-account cohort across the full contract-value range brackets the implied annual ARR at risk at roughly $277,000-$616,000 on the Q1 run-rate versus $576,000-$1,281,000 on the Q3 run-rate, and both bracket ends show close to a doubling
→ the magnitude of ARR at risk has roughly doubled on a run-rate basis regardless of which contract-value segment is churning, which justifies treating diagnosis as urgent, but the figure is a magnitude illustration built on an unverified persistence assumption and must not be quoted externally as a forecast

**Pre-check:** head GT-1, GT-2, GT-14 · ?-marked: none · lowest cited: none · Inputs ceiling: HIGH
**Confidence:** LOW — Inputs axis clean. Inference axis short: hop 1 rests on A-11 (churn events cluster at renewal anniversaries rather than distributing uniformly within a quarter); if renewals cluster, the compounding model over- or understates true annual attrition; verification path is chain C5 Option A's cohort pull, which will show actual renewal-date distribution. Rivals axis short: GT-6's own ambiguity supports a live reading that 9.2% may already be a rolling annualized rate against staggered cohorts, in which case no further compounding should be applied at all. Two axes short → LOW.

### Conclusion C7: Provisional hypothesis ranking

GT-3 (rising ticket volume) + GT-4 (declining adoption scores) + GT-2 (sharp two-quarter doubling) + C3 (co-symptom hypothesis, LOW)
→ a sharp two-quarter inflection co-occurring with both a support-volume signal and an adoption signal fits a discrete triggering event in a shared upstream system better than it fits slow-moving structural drivers, which would typically not move either metric before a quiet non-renewal [Assumes: A-13]
→ this asymmetry means the current internal signals are systematically better evidence for service-quality and offer/product causes than for pricing and competitive-displacement causes, so an absent ticket or adoption signature is not evidence that those two categories are absent
→ service-quality degradation should be provisionally ranked as the most likely largest contributor, with onboarding failure and offer/product gaps as plausible co-contributors in newer cohorts, and pricing pressure and competitive displacement treated as under-observed rather than ruled out, all at LOW confidence

**Pre-check:** head GT-3, GT-4, GT-2, C3 (LOW) · ?-marked: none directly · lowest cited: LOW · Inputs ceiling: LOW
**Confidence:** LOW — Inputs ceiling is already LOW because C3 (LOW) sits on the head, per the ceiling rule (a chain rates no higher than the lowest-rated chain its head cites). Independent of the ceiling, Inference axis is also short: hop 1 rests on A-13 (pricing/competitive categories are not simply confounded or lagged versions of the categories that do move the signals), not yet verified. Rivals axis is also short: "competitive displacement is actually dominant and the ticket/adoption rise is an unrelated coincidence" is a live, unruled-out rival, named in full in the Adversarial pass record.

## 5. Abandoned Reasoning

### Dead End: Treating the CS-flagged signals as the root-cause categories themselves

**What was tried:** An early framing treated "rising tickets" and "declining adoption" as if they were two of the candidate root-cause categories in their own right — i.e., "the root cause is ticket volume" / "the root cause is low adoption" — which would have pointed the fix directly at ticket-deflection and adoption-nudge campaigns.

**Why abandoned:** This conflates leadership's six candidate *driver* categories with two *operational metrics* CS happens to track. Chain C3 shows a more parsimonious shared-upstream-cause model fits the co-occurrence at least as well, and GT-5 states plainly that no causal attribution connecting these metrics to churn has been done. Treating a metric as a cause without first testing the shared-cause model is exactly the kind of premature convergence the inversion analysis in section 2 warns against.

**What it ruled out:** This dead end saves the team from scoping the "fix" as "reduce ticket volume" or "boost the adoption score" — proxy metrics that could both improve while the underlying driver (e.g., an understaffed support org, chain C1's unresolved measurement question) remains untouched.

### Dead End: Recommending a price cut on the strength of general SaaS retention literature

**What was tried:** An early draft considered recommending a discount or pricing concession as a default retention lever, on the reasoning that discounting broadly correlates with reduced churn in SaaS retention writing.

**Why abandoned:** This is reasoning by analogy — "others have addressed churn this way" — used as direct evidence, which this methodology explicitly bans (section 4's no-analogy rule) absent a Northbrook-specific ground truth connecting pricing to *this* churn rise. GT-5 states no causal attribution has been done; A-16 (no mid-2026 pricing/packaging change identified) is unverified in either direction. Recommending a price cut here would also directly instantiate the second-order risk named in chain C4: compressing margin before knowing whether the real driver is service-quality, which a price cut would not fix and might starve further.

**What it ruled out:** This saves Northbrook from funding a margin-compressing lever before chain C5's pricing/competitive-intel pull (Option D) has even run, and flags pricing analysis specifically as evidence-gathering, not a default action.

### Dead End: Treating the reported 4.1%→9.2% figures as precise, board-ready metrics

**What was tried:** An early pass took GT-2's figures at face value for the magnitude estimate in chain C6 and prepared to state the annualized run-rate (~15.4%→~32.0%) as a forecast-grade number.

**Why abandoned:** The five-whys decomposition in section 3 showed all four constituent branches (methodology stability, denominator comparability, categorization integrity, sample-size adequacy) are unverified, which is why GT-11? carries a `?` and chain C1 rates LOW. Stating the compounded figures as a forecast would overstate confidence the measurement-integrity work has not yet earned.

**What it ruled out:** This reinforces the recommendation (chain C6, chain C1) that RevOps document and audit the churn-rate methodology before any figure derived from GT-2 is used externally or in board communication.

## 6. Conclusion

**Recommended approach:** Launch a parallel-track diagnostic — cohort/segment churn decomposition immediately and unconditionally, the ticket-adoption correlation study and the pricing/competitive-intel pull alongside it, and the win/loss interview program queued for the competitive and pricing residual — together with a cheap, hypothesis-agnostic retention triage (proactive outreach to already-flagged at-risk accounts and a support-capacity check), before committing budget to any single named fix (chain C5; chain C4). Concretely, in week 1: pull churn by signup cohort, segment, contract size, sales rep, and acquisition channel (tests A-8/GT-13?, A-6, and every fishbone category at once); in weeks 1-3 in parallel: join ticket-category data and adoption-score trend by cohort against churn dates (tests A-7/GT-12?, A-18), and pull discount history plus sales/win-loss notes mentioning competitors (tests A-9, A-16, A-17); in weeks 4-6, run structured win-loss/exit interviews on the segment the first two pulls cannot explain (typically the competitive and pricing residual). A one-day systems-readiness check precedes week 1 to test A-10 before the timeline is committed.

**Key insight:** The two CS-flagged signals are better modeled as co-symptoms of a shared upstream driver than as independent causes (chain C3), and the sharp two-quarter inflection pattern systematically under-detects pricing and competitive-displacement causes, because those categories would not be expected to move ticket or adoption metrics before a quiet non-renewal — an absent signal is not evidence of an absent cause (chain C7). This produces the following provisional, evidence-light ranking, useful only for sequencing the investigation, not for justifying a fix:

| Rank | Candidate category | Provisional weight | Confidence | Resolved by |
|---|---|---|---|---|
| 1 | Service-quality degradation (support capacity/quality) | Highest | LOW | Cohort decomposition + ticket/adoption correlation (chain C5, Options A+B) |
| 2 | Onboarding failure (newer cohorts) | Medium-low | LOW | Cohort-age cut within Option A |
| 3 | Offer/product gaps | Medium | LOW | Ticket-category detail within Option B |
| 4 | Sales-qualification/ICP mismatch | Medium (if channel-concentrated) | LOW | Rep/channel cut within Option A |
| 5 | Competitive displacement | Low-medium, likely under-observed | LOW | Win-loss interviews (Option C) + Option D |
| 6 | Pricing pressure | Low-medium, likely under-observed | LOW | Pricing/discount pull (Option D) + Option C |

**Trade-offs acknowledged:** Diagnosing before fixing means the specific driver will not be named for several weeks, which carries real cost if the true driver is actively compounding while the team waits (chain C4); this is mitigated, not eliminated, by running cheap triage in parallel, per the Adversarial pass record's Cluster-2 plan change. The headline urgency figure — churn roughly doubling on a run-rate ARR-at-risk basis — is a magnitude illustration built on an unverified persistence assumption and must not be quoted externally as a forecast until methodology is confirmed (chain C6; chain C1). Leadership's original framing of a single, CS/product-owned root cause is being explicitly discarded in favor of a multi-hypothesis, segment-aware investigation (chain C2), which means no single team can be told "you own the fix" until the diagnostic narrows the field — no chain — flagged assumption only for the organizational-friction risk this creates (see the Adversarial pass record's Cluster-3 disposition).

**Pre-check:** head C1 (LOW), C2 (LOW), C3 (LOW), C4 (LOW), C5 (MEDIUM), C6 (LOW), C7 (LOW) · ?-marked: none directly · lowest cited: LOW · Inputs ceiling: LOW
**Confidence:** LOW — the recommended *posture* (diagnose in parallel with cheap triage before committing to a named fix) rests on C4 and C5; C5 is MEDIUM with a single named, closeable gap (A-10, the systems-readiness assumption), but C4 is LOW because its Inference axis (A-12) and Rivals axis (the act-now rival) are both still open within that chain's own scope. The *specific hypothesis ranking* used to sequence the investigation (chain C7) and the *magnitude framing* used to convey urgency (chain C6) both rest on unverified ground truths (GT-12?, GT-13?, and the persistence assumption A-11) and on live, unruled-out rivals, and C7 additionally inherits C3's LOW rating through the ceiling rule. Per D-07: every chain contributing to this Conclusion is rated below HIGH — C1 (measurement-integrity gate, LOW, verification path: chain C5 Option A), C2 (multi-cause framing, LOW, verification path: chain C5 Options A+B), C3 (co-symptom model, LOW, verification path: chain C5 Option B), C4 (diagnose-before-fix, LOW, verification path: none fully closes the Rivals axis — this is disclosed as an accepted, mitigated risk, not a resolved one), C5 (sequencing, MEDIUM, verification path: the one-day systems-readiness check), C6 (magnitude framing, LOW, verification path: chain C5 Option A's cohort pull), C7 (provisional ranking, LOW, verification path: chain C5 Options A, B, and D plus the win-loss interviews). None of this weakens the recommendation to run the diagnostic — it is precisely why the diagnostic is recommended: the low confidence is in the *causal story*, not in the *decision to gather better evidence before spending against that story*.
