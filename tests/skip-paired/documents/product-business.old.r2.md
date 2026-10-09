## Techniques not applied (process output)

Mode: `full-composer` (the request names multiple specific techniques — decomposition, assumption
challenge, second-order thinking, inversion, a Fermi/estimate pass, and a pilot-vs-binary
recommendation — so the full composed procedure runs rather than one focused technique).

Invoked and fired: inversion (Phase 2 — enumerating what would make a free tier a bad idea);
second-order thinking (Phase 4 — actor and time lenses on the sales motion, incentives, support
load, and brand perception); estimate/Fermi (Phase 4 — breakeven conversion-rate bracket);
trade-off (Phase 4 — pilot vs. full launch vs. status quo, weighted and locked before scoring);
pre-mortem (Phase 5 — the conclusion is a plan, so pre-mortem is the prescribed adversarial
technique, not inversion a second time).

Not applied:
- fishbone — not applicable — the candidate "jobs" a free tier could do, and the assumption
  space around them, were enumerated directly via decomposition (Phase 1) and inversion's
  failure-condition analysis (Phase 2); a category-brainstorm pass would duplicate that work
  rather than add coverage.
- five-whys (reduce-to-primitives mode) — not applicable — the one claim needing irreducible
  decomposition (the breakeven identity) was reduced to its constituent unit-factors by the
  Estimate procedure's own decomposition step (GT-6, chain C2), which performs the same
  bottoming-out function a separate formal drill would repeat.
- theoretical-limit — not applicable — nothing in this decision turns on a physical or
  mathematical ceiling once convention is stripped away; the one governing identity in play
  (cost per free user vs. margin per conversion) is already a GT-6/C2 accounting identity, not
  a constraint a theoretical-limit pass would sharpen further.

## Assumption Audit scan (process output, end of Phase 4)

One row per chain per step, in order. All surfaced assumptions were pre-added to the
Classified Assumptions Table (section 2) before this scan; the scan's job is to confirm no
chain step introduces one that is still missing. Result: none missing.

| Chain | Step | Step Text (brief) | Assumption surfaced? | Added to Table? |
|-------|------|--------------------|-----------------------|------------------|
| C1 | 1 | signups can only come from already-sourced prospects | A-2 | yes (already present) |
| C1 | 2 | redirecting prospects shifts pipeline, not new volume | none | n/a |
| C1 | 3 [2nd] | sales inherits routing/triage burden | none | n/a |
| C1 | 4 [3rd] | operational drag on the outbound channel | none | n/a |
| C1 | 5 | lead-gen job requires unbudgeted investment | none | n/a |
| C2 | 1 | per-free-user cost brackets to $70-$450/yr | none | n/a |
| C2 | 2 | net margin per conversion brackets to $6,500-$8,500 | A-16 | yes (already present) |
| C2 | 3 | applying brackets to GT-6 yields breakeven ~0.8%-6.9%, central ~2% | A-14 | yes (already present) |
| C2 | 4 | observed benchmarks sit at/above the ~2% central estimate | none | n/a |
| C2 | 5 | headroom shrinks toward the pessimistic end of the bracket | none | n/a |
| C2 | 6 | benchmarks assume a precondition (acquisition motion) this company lacks | none | n/a |
| C2 | 7 | binding constraint is volume, not rate | none | n/a |
| C3 | 1 | buyers cite free-tier existence as negotiation leverage without migrating | A-17 | yes (already present) |
| C3 | 2 | teams within free-tier limits have a direct downgrade incentive absent gating | A-15 | yes (already present) |
| C3 | 3 [2nd] | reps/champions face new pressure | none | n/a |
| C3 | 4 [3rd] | realized ACV may fall across renewals | none | n/a |
| C3 | 5 | real cannibalization risk via two independent channels | none | n/a |
| C4 | 1 | uncapped full launch fails the cost-cap must-have | none | n/a |
| C4 | 2 | weighted comparison: pilot 75 vs. status quo 70, robust to ±1 perturbation | A-13 | yes (already present) |
| C4 | 3 | pilot recommended over full launch and status quo | none | n/a |
| C5 | 1 | the 75-70 margin depends on the pilot clearing a volume+gating bar | A-15 (referenced again) | yes (already present) |
| C5 | 2 | if gating is infeasible, the margin can erode per the flip-test | none | n/a |
| C5 | 3 | the pilot recommendation is conditional on gating and a volume/kill-date gate | none | n/a |

Scan complete: 5 chains, 22 chain-step rows, no step skipped. No assumption surfaced by a chain
step was missing from the Classified Assumptions Table at the time the chain was written.

## Adversarial pass (process output)

**Recompute.** Fermi arithmetic (chain C2): c/m with c ∈ [$70,$450], m ∈ [$6,500,$8,500] →
r* ∈ [70/8500, 450/6500] = [0.82%, 6.92%] — recomputes to the stated "roughly 0.8%-6.9%,
central ~2%" (central using c=$150, m=$7,500 → 150/7500 = 2.0%). Trade-off arithmetic (chain
C4): status quo = 1(5)+5(4)+5(5)+1(3)+1(2)+5(3) = 5+20+25+3+2+15 = 70; pilot =
4(5)+4(4)+4(5)+3(3)+2(2)+2(3) = 20+16+20+9+4+6 = 75 — both recompute as stated.

**Sensitivity.** The single ground truth whose falsity would flip the headline recommendation
is GT-2? (no inbound channel exists today) — it is `?`-marked. If false (an inbound motion
already exists but was simply not mentioned), the volume constraint binding chains C1 and C2
weakens substantially and a fuller launch becomes far more defensible immediately, which would
flip chain C4's framing of the pilot's advantage. Per-chain weakest link: C1's weakest link is
GT-2? itself (unverified channel state); C2's weakest link is the A-14 carry-period assumption
(see its confidence line); C3's weakest link is GT-1? (unverified account/ACV data); C4's
weakest link is the Criterion-1 ("resolves core uncertainty") score of 4/5 for the pilot, which
section C5 shows is not a fixed property of "running a pilot" but a property of a specific
pilot design; C5's weakest link is A-15 (unverified whether the product can technically gate
free-tier signup by account/domain).

**Rival.** Headline conclusion (run a scoped pilot): rival = status quo (do nothing), addressed
in C4 via the locked, weighted comparison and its flip-test (section 4); the flip-test shows no
single-criterion ±1 weight change reverses the 75-70 result, with the closest lever being
organizational cost (criterion 6), which would need to move from weight 3 to weight 5 (a +2
move, hitting the scale's ceiling) to flip it. A second rival — full open launch (O2) — is
ruled out structurally, not by scoring, via the cost-cap must-have in C4's first hop; this
rival is recorded in Abandoned Reasoning (Dead End 2). A third, narrower rival to chain C2's
"rate looks achievable" sub-finding — "the rate is irrelevant because volume will be ~0
regardless" — is not a competing conclusion so much as the chain's own next hop; C2 absorbs it
directly (hops 5-6) rather than leaving it live.

**Premise (past tense).** It is now two quarters after the scoped free-tier pilot launched, and
it has already failed — it produced no usable answer on conversion economics and did measurable
damage to the existing paying base.

**Causes (unfiltered, from three stakeholder viewpoints).**
*Sales leadership:* (1) pilot volume was too low to be statistically meaningful because no real
acquisition channel fed it even at pilot scale; (2) reps, uncompensated for free signups,
ignored or routed them nowhere; (3) the pilot was scoped to new-logo-only, but most actual
interest came from existing customers' sub-teams wanting a second free seat — the excluded
population turned out to be the real signal.
*Finance/CFO:* (4) free-user support tickets were as complex and costly as paid-user tickets,
so cost-per-free-user came in above the modeled bracket; (5) the pilot had no enforced kill
date or named decision-owner, so it quietly became a permanent fixture without a stop/continue
re-approval.
*Existing paying customer / champion:* (6) an existing paying account's sub-team accessed the
free tier because nothing gated it by account/domain, triggering a real downgrade; (7) a
customer's procurement team used the free tier's mere existence as renewal leverage even though
no one on their team touched it.
*Competitor:* (8) a competitor expanded its own free tier in response to the announcement,
neutralizing the signaling benefit while this company still carried the cost.

**Clusters (structural weaknesses, with triage and chain/GT bearing).**
- Cluster A — *No real top-of-funnel for the pilot either* (causes 1,2,3). Triage: **costly but
  survivable** (produces an inconclusive pilot, not a disaster, but wastes the test). Bears on:
  A-8, GT-2?, chain C1, chain C2 (hops 5-6), chain C5.
- Cluster B — *No enforced stop/go gate* (causes 4,5). Triage: **costly but survivable** if
  caught, **fatal to the cost-cap rationale** if not (an unbounded-in-practice pilot is exactly
  the O2 failure mode C4's must-have was built to exclude). Bears on: GT-3?, chain C4's cost-cap
  must-have.
- Cluster C — *Leaky eligibility boundary* (causes 6,7). Triage: **fatal to the pilot's
  ACV-protection rationale** specifically — this is the exact mechanism chain C5 identifies as
  capable of erasing the 75-70 margin. Bears on: A-6, A-15, A-17, chain C3, chain C5.
- Cluster D — *Competitive signaling neutralized* (cause 8). Triage: **tolerable** — competitive
  signaling was already the lowest-weighted criterion (weight 2 of 2-5) in C4's trade-off.

**Disposition (per cluster).**
- Cluster A: **plan change** — before launch, name the specific mechanism that will feed the
  pilot (e.g., an in-app upgrade/downgrade path surfaced to existing accounts' adjacent teams,
  or a small, time-boxed content/paid-media test) and set a minimum-viable-signal volume
  threshold below which the pilot is declared inconclusive rather than quietly extended.
- Cluster B: **plan change** — set a hard calendar decision date with a named owner (not "the
  team"), and a cost ceiling with an automatic-pause trigger rather than a dashboard someone has
  to remember to check.
- Cluster C: **plan change** — enforce eligibility at signup (block known paid-account
  domains/emails) and brief the CS/renewal team on a talk track before launch, not after the
  first customer raises it.
- Cluster D: **explicitly accepted risk** — accept that a competitor counter-move may neutralize
  the signaling benefit specifically; no mitigation beyond proceeding on the pilot's other
  merits (bounded-cost uncertainty resolution and ACV protection), which do not depend on the
  signaling value per C4's weighting.

**Falsification.** This recommendation (run a scoped, capped, account-gated, time-boxed pilot
rather than a full launch or no action) is false if no pilot design can simultaneously (a) cap
cost exposure under GT-3? and (b) exclude existing paying accounts from eligibility — i.e., if
the product/billing architecture makes account-level gating technically impossible (A-15 false),
the pilot degrades into an ungated, uncontrolled launch and the status-quo recommendation (O1)
would dominate instead, per the arithmetic in chain C5.

## §6→§4 closure ledger (process output)

- "Do not launch an open, full free tier, and do not simply maintain the status quo either —
  run a scoped, cost-capped, time-boxed, account-gated pilot ... before making any permanent
  packaging decision" → chain C4 ✓, chain C5 ✓
- "The real fork isn't 'free tier yes or no' — it's which job the tier is supposed to do ..."
  → chain C1 ✓, chain C3 ✓
- "Choosing a pilot over an immediate full-parity launch defers ... leaves the breakeven
  conversion rate's real-world achievability genuinely unresolved ..." → chain C2 ✓
- "**Pre-check:**" line (head: C1, C2, C3, C4, C5) → chains C1 ✓, C2 ✓, C3 ✓, C4 ✓, C5 ✓
- "**Confidence:** LOW ..." → chains C1 ✓, C2 ✓, C3 ✓, C4 ✓, C5 ✓

All five Conclusion-section claims cite a named chain inline. No claim cut.

## Self-audit scan (process output)

**Table 1 — chain form (section 4)**

| Chain | Chain Head (brief) | Form conforming? | Rule applied | Dependency clean? | Band | Act attempted? | Edges fired |
|-------|---------------------|-------------------|--------------|--------------------|------|------------------|-------------|
| C1 | GT-2? (no inbound channel) | yes | n/a | yes | MEDIUM | no | none |
| C2 | GT-1? + GT-6 + GT-2? + GT-7 + GT-8? | yes | n/a | yes | LOW | yes | none |
| C3 | GT-1? (outbound-sold base) | yes | n/a | yes | MEDIUM | no | none |
| C4 | GT-3? + C1 + C3 | yes | n/a | yes | MEDIUM | no | none |
| C5 | C4 | yes | n/a | yes | MEDIUM | no | none |

**Table 2 — claim inventory (section 6)**

| §6 Span (brief) | Construct | Claim under R11? | R11 clause applied | Chain cited |
|-------------------|-----------|-------------------|-----------------------|---------------|
| "Recommended approach: ... run a scoped, cost-capped ... pilot ..." | bold lead-in | yes | colon closes bold span, assertion on same line | C4, C5 |
| "Key insight: ... which job the tier is supposed to do ..." | bold lead-in | yes | colon closes bold span, assertion on same line | C1, C3 |
| "Trade-offs acknowledged: ... leaves the breakeven rate's achievability unresolved ..." | bold lead-in | yes | colon closes bold span, assertion on same line | C2 |
| "**Pre-check:** head C1 (MEDIUM), C2 (LOW), C3 (MEDIUM), C4 (MEDIUM), C5 (MEDIUM) ..." | bold lead-in | yes | pre-check line is itself a claim, discharged by its own head | C1, C2, C3, C4, C5 |
| "Confidence: LOW ..." | bold lead-in | yes | colon closes bold span, assertion on same line | C1, C2, C3, C4, C5 |

Scan complete: 5 chain rows, one per section-4 chain block in order; 5 section-6 rows, one per
construct in order — 5 claims under R11, 0 excluded. 0 chains malformed, 0 claims untraced.

## Self-Audit Gate (process output)

**Criterion 1: Identify Essence**
Quoted span: "Should this company add a free tier — and, given that the goal a free tier would
serve is itself unstated and the core economics (conversion rate, true per-user cost) are
unverified, is a bounded pilot a better decision than a binary launch/no-launch call?"
Band: **Rigorous**
Justification: names the real fork (job-ambiguity plus unresolved economics, not "free tier
yes/no" taken at face value) rather than restating the prompt, and each success criterion
below it is a verb+subject+outcome triplet checkable against section 6 without interpretation.

**Criterion 2: Challenge Assumptions**
Quoted span: Assumption Audit scan reconciliation line — "Scan complete: 5 chains, 22
chain-step rows, no step skipped. No assumption surfaced by a chain step was missing from the
Classified Assumptions Table at the time the chain was written."
Band: **Rigorous**
Justification: all 17 rows use the four-type scheme with em-dash Verdict cells and specific
Verification cells (including "unverified — flagged" where used in chains), at least one
assumption (A-4) was Discarded on evidence rather than merely labelled, and the audit scan
confirms exhaustive coverage of every named chain step with nothing missing.

**Criterion 3: Establish Ground Truths**
Quoted span: "?-marked: GT-1, GT-2, GT-3, GT-4, GT-5, GT-8 (6 of 8). Read-at-source: GT-7 —
firstpagesage.com/seo-blog/saas-freemium-conversion-rates/, 'Overall Average' and
industry-comparison sections, fetched 2026-10-08."
Band: **Rigorous**
Justification: all 8 GT-IDs are stable and match the Derivation Chains' usage; the enumeration
matches the suffixed entries when checked against the list; GT-7 names its exact read-at-source
location from a directly fetched source; no GT feeds a HIGH-confidence chain (the analysis's
highest band is MEDIUM), so the HIGH-chain read-at-source requirement is vacuously satisfied;
no Discard-verdict assumption (e.g., A-4) appears in this list.

**Criterion 4: Reason Upward**
Quoted span: self-audit scan Table 1 — "C1 | GT-2? (no inbound channel) | yes | n/a | yes |
MEDIUM | no | none" through "C5 | C4 | yes | n/a | yes | MEDIUM | no | none" (all five rows
read Form conforming = yes, Dependency clean = yes).
Band: **Rigorous**
Justification: every chain in the scan reads form-conforming with clean dependencies, each
carries at least one genuine intermediate hop, each undeclared premise surfaced during
derivation carries an inline `[Assumes: A-N]` mark (A-2, A-14, A-15, A-16, A-17), no analogy is
used as direct evidence anywhere (benchmark figures are cited as GT-7/GT-8? data, not
"others do it this way"), and Abandoned Reasoning (section 5) documents three dead ends with
specific structural reasons rather than vague ones.

**Criterion 5: Validate**
Quoted span: Adversarial pass record — "Falsification. This recommendation ... is false if no
pilot design can simultaneously (a) cap cost exposure under GT-3? and (b) exclude existing
paying accounts from eligibility ..." together with each chain's `**Confidence:**` line naming
its GT-N? inputs, cited Cn bands, and (for C2) the A-14/A-16 downgrade causes with what would
remove them.
Band: **Rigorous**
Justification: every chain's weakest link is named on its own confidence line; no chain is
rated HIGH while consuming a GT-N? input (the ceiling tops out at MEDIUM throughout); every
chain citing another chain is rated no higher than the cited chain's band (C4 ≤ min(C1,C3)=
MEDIUM; C5 ≤ C4 = MEDIUM); the overall Conclusion's LOW rating matches its weakest contributing
chain (C2, LOW) exactly; and the adversarial pass (pre-mortem, since the conclusion is a plan)
ran all five parts — Recompute, Sensitivity, Rival, the pre-mortem technique itself (Premise/
Causes/Clusters/Disposition), and Falsification — with every cluster carrying a named plan
change or an explicitly accepted risk with a named mitigation.

**Criterion 6: Conclusion-to-Ground-Truth Traceability**
Quoted span: self-audit scan Table 2 reconciliation — "5 section-6 rows, one per construct in
order — 5 claims under R11, 0 excluded. 0 chains malformed, 0 claims untraced."
Band: **Rigorous**
Justification: every section-6 claim (including the Pre-check line) cites a named section-4
chain inline, no new reasoning is introduced in section 6 that was not established in section 4,
and the Key Insight (the job-mismatch finding) is a non-obvious result distinct from — not a
restatement of — the Recommended Approach (run a gated pilot).

**Gate result:** No criterion scored Absent; zero criteria scored Hand-wavy (the cap of "at
most one" is not approached). Both clearing conditions are met — the gate is cleared on the
first pass, no Fix/Repeat cycle was required.

---

# First-Principles Analysis: Should This B2B SaaS Company Add a Free Tier?

## 1. Problem Essence

**Core problem:** Should this company add a free tier — and, given that the goal a free tier
would serve is itself unstated and the core economics (free-to-paid conversion rate, true
per-active-free-user cost) are unverified, is a bounded, reversible pilot a better decision
than a binary launch/no-launch call?

**Success criteria:**
1. The Conclusion names which specific job (if any) a free tier would need to perform, and
   states which of three actions it recommends — full launch, no action, or a scoped pilot —
   tied explicitly to that named job. (Checkable: section 6's Recommended Approach names one of
   the three and cites the chain establishing the job.)
2. The Conclusion states a quantified or bracketed breakeven free-to-paid conversion rate and
   compares it against external benchmark data. (Checkable: section 4 contains a numeric
   bracket and a benchmark comparison a reader can recompute.)
3. The Conclusion explicitly addresses cannibalization risk against the existing ~$10,000-ACV,
   outbound-sold base, and states whether that risk is accepted, mitigated, or dismissed.
   (Checkable: section 6 or its cited chains name the risk channel and its disposition.)
4. The Conclusion states a confidence band and names, specifically, what is driving it below
   HIGH and what would raise it. (Checkable: the Confidence line names specific GT-N? inputs
   or chains and a verification path for each.)

## 2. Assumptions Table

Several of these were surfaced via an explicit inversion pass: the claim "adding a free tier is
the right move" was inverted to "adding a free tier is not the right move / actively harms the
company," and at least seven distinct conditions that would guarantee that inverted claim were
enumerated (near-zero top-of-funnel volume feeding the tier; existing teams downgrading into it;
cost outrunning conversion revenue; the outbound motion's pipeline leaking into an unmanaged free
option; no inbound channel to feed it at all; buyers using it as renewal leverage; and the
competitive-parity rationale targeting a segment this company doesn't actually sell to). Each
necessary precondition behind those conditions is recorded below as an `untested belief`.

| Assumption | Type | Treatment | Verdict | Verification |
|---|---|---|---|---|
| A-1: Because all competitors have a free tier, this company needs one too (competitive parity) | convention | challenge explicitly before use | Challenge — no evidence given that deals are actually lost for lack of a free tier, or that the segment seeking parity overlaps the $10K-ACV buyer (see A-10) | unverified — flagged |
| A-2: A free tier functions as a self-serve inbound funnel | convention | challenge explicitly before use | Challenge — a free tier is a packaging decision; a self-serve funnel is a separate GTM capability (signup flow, onboarding without sales, a traffic source) this company does not have per GT-2? | unverified — flagged |
| A-3: B2B freemium conversion dynamics resemble generic/B2C SaaS benchmarks for this product | untested belief | verify or flag | Challenge — GT-7/GT-8? show a 2-3x spread between self-serve and sales-assisted models and a 10x top-to-bottom-quartile spread; this company's product shape (team-based, $10K ACV, sales-assisted today) is not established as matching any specific benchmarked cohort | unverified — flagged |
| A-4: Free users are cost-free / a pure growth lever with no downside cost | current constraint (claimed) | n/a — directly contradicted | Discard — contradicted by GT-3? (Finance: cost scales with active free users, not just paying users) | contradicted by GT-3? |
| A-5: The free tier's job is top-of-funnel lead generation (one candidate among several) | untested belief | verify which job is actually targeted before designing | Challenge — not established as *the* job; competing candidate jobs (PLG expansion within paid accounts, competitive defense, downward segment expansion) are equally plausible and imply different designs | unverified — flagged |
| A-6: Adding a free tier will not cannibalize existing or prospective $10K-ACV paying teams | untested belief | verify | Challenge — outbound-sold mid-market/enterprise accounts have both a negotiation-leverage channel and a seat-migration channel available absent explicit gating (chain C3) | unverified — flagged |
| A-7: The outbound sales team's incentives and workflow are compatible with a parallel free, low-touch motion | untested belief | verify | Challenge — reps are not described as compensated for free signups; routing/ownership is undefined | unverified — flagged |
| A-8: A workable, low-cost acquisition channel exists, or can cheaply be built, to feed a free tier's top of funnel | untested belief | verify | Challenge — directly contradicted as a present-tense claim by GT-2? (100% outbound + referral, no inbound channel today); building one is a separate, unbudgeted investment | unverified — flagged |
| A-9: The free-to-paid conversion rate will be high enough to amortize per-free-user cost | untested belief | verify | Challenge — genuinely unknown; GT-4? confirms no internal pilot has ever produced this number. This is the single most load-bearing unverified input in the analysis | unverified — flagged |
| A-10: The market segment that cares about free-tier parity overlaps with this company's actual $10K-ACV buyer | untested belief | verify | Challenge — no data given on why deals are won or lost; parity argument's relevance is unestablished | unverified — flagged |
| A-11: Cost per active free user is roughly constant across the free-user population (not dominated by a few heavy users) | untested belief | verify; used as a simplifying bracket assumption in the Fermi estimate | Challenge — flagged as a simplification for chain C2's bracket, not a verified distributional claim | unverified — flagged |
| A-12: Today, 100% of revenue depends on outbound sales + referral (restates GT-2? as a constraint on the business, not a permanent fact) | current constraint | record expiry conditions | Accept — expires once/if a deliberate, resourced inbound or self-serve channel is built and proven; not a structural law of this business, just its current state | current state per GT-2? |
| A-13: A scoped, capped pilot can be run at materially lower cost and risk than a full open launch | untested belief (largely design-controllable) | verify via the trade-off's must-have knockout | Challenge, then largely Accept — a pilot's defining feature is a bounded blast radius (capped volume, time-boxed, gated eligibility), which directly answers GT-3?'s cost-scaling constraint; risk is in execution discipline, not the concept (see Adversarial pass, Cluster B) | unverified — flagged, low residual risk |
| A-14: Free users convert to paid or churn out within roughly one year on average | untested belief | verify; simplifying assumption inside the breakeven identity (GT-6) | Challenge — if the real carry period is materially longer, the effective breakeven rate needed is higher than chain C2's bracket states, weakening (not reversing) its conclusion | unverified — flagged |
| A-15: The product/billing architecture can technically gate free-tier signup by account or email domain, excluding existing paying accounts | untested belief | verify before pilot launch | Challenge — unverified; this is the single assumption the Falsification condition in the Adversarial pass hinges on | unverified — flagged |
| A-16: This company's gross margin on SaaS revenue falls in the generic 65%-85% B2B SaaS range | untested belief / convention | challenge; used as a bracket input in chain C2, not a company-specific figure | Challenge — industry convention, not this company's verified margin; a materially lower margin raises the required breakeven rate proportionally | unverified — flagged |
| A-17: Economic buyers/procurement at existing or prospective accounts will cite free-tier availability as renewal/negotiation leverage even without migrating any users | untested belief | verify | Challenge — plausible given standard negotiation dynamics, but not verified for this company's buyers specifically; if false, chain C3's conclusion still stands via its independent seat-migration channel | unverified — flagged |

## 3. Ground Truths

- **GT-1?** Current state: $2.4M ARR, 240 paying teams, average contract value ≈ $10,000/
  team/year (240 × $10,000 = $2.4M, internally consistent) — unverified: user-stipulated
  business metric for this exercise; no financial statement or billing system was opened by
  this analysis to confirm it independently.
- **GT-2?** Go-to-market is 100% outbound sales + referral; no self-serve or inbound
  acquisition channel exists today — unverified: user-stipulated; no CRM, analytics, or
  marketing-channel report was opened by this analysis.
- **GT-3?** Free-tier infrastructure and support costs scale with active (free) user count, not
  only with paying-user count — confirmed internally by Finance per the user — unverified by
  this analysis: the underlying cost model/accounting document was not opened.
- **GT-4?** No internal freemium pilot has ever been run; the free-to-paid conversion rate for
  this specific product and ICP is therefore unknown — unverified: user-stipulated absence of
  data; treated as a safe negative claim but not independently confirmed by this analysis.
- **GT-5?** All named direct competitors currently offer a free tier — unverified:
  user-stipulated; competitor pricing pages were not fetched or checked by this analysis.
- **GT-6** Breakeven identity: for a cohort of free users who each either convert to paid or
  churn out within roughly the same average carrying period, the breakeven free-to-paid
  conversion rate satisfies **r\* = c ÷ m**, where *c* = average annual cost to serve one
  active free user (infrastructure + support) and *m* = net annual margin contributed by one
  newly converted paid customer (ACV × gross margin) — source: derived within this analysis by
  algebraic identity from the definitions of *c*, *m*, and *r* (a mathematical/accounting
  identity, not an empirical claim requiring external citation); applied with bracketed values
  in chain C2.
- **GT-7** Published freemium-to-paid conversion benchmark: average 3.4%-3.7% across freemium
  models (traditional 3.4%, land-and-expand 3.7%), Enterprise-segment figure 3.9%, Enterprise
  visitor-to-freemium rate 12.3%; methodology: 80+ SaaS clients, 2022-2026, published 2026-09-11
  — source: First Page Sage, "SaaS Freemium-to-Paid Conversion Rates"; read-at-source:
  https://firstpagesage.com/seo-blog/saas-freemium-conversion-rates/, "Overall Average" and
  industry-comparison table sections, fetched directly by this analysis on 2026-10-08.
- **GT-8?** Self-serve freemium models reportedly convert at roughly 6%-8% (exceptional
  performers 6-8%+), sales-assisted freemium at roughly 10%-15%, with approximately a 10x gap
  between top- and bottom-quartile performers — cited to: Lenny Rachitsky's research across
  1,000+ products, as synthesized by a web search; reported-by-delegate: the search tool's
  synthesis supplied this figure and the underlying primary source was not opened directly by
  this analysis.

**Provenance summary:** `?`-marked: GT-1, GT-2, GT-3, GT-4, GT-5, GT-8 (6 of 8). Unsuffixed:
GT-6 (derived in-analysis, not a citation), GT-7 (read-at-source as cited above). No GT-item
in this list feeds a HIGH-confidence chain (the highest band reached anywhere in section 4 is
MEDIUM), so the "every unsuffixed GT feeding a HIGH chain names its read-at-source location"
requirement has no instance to satisfy beyond GT-7's location, already named above. No
assumption that received a Discard verdict in section 2 (A-4) appears in this list.

## 4. Derivation Chains

### Second-order thinking: the two lenses walked before chains C1/C3 were extended

**Actor lens.** *Sales reps/SDRs/AEs* — uncompensated for free signups, they are likely to
either ignore free-tier traffic (starving it of follow-up) or lean on it as a no-risk parking
spot for marginal prospects they'd otherwise have to qualify out, concentrating risk exactly
where price sensitivity is highest. *Existing champions inside paying accounts* — once a free
alternative is visible, they face new internal pressure to justify the $10K contract at
renewal, even if no one on their team ever touches the free tier. *Procurement/economic
buyers* — gain a concrete negotiating anchor. *Competitors* — can respond to any public move by
expanding their own free tier, a response that is cheap for them and directly erodes whatever
competitive-signaling benefit motivated the move in the first place.

**Time lens.** *Immediate:* infra/support cost begins accruing the moment any free signup
exists (GT-3?); sales process friction appears immediately (who owns a free signup?).
*A few cycles (2-4 quarters):* real conversion-rate and volume data starts to exist — this is
exactly the data GT-4? says does not exist today, and is the thing a bounded pilot is
positioned to produce. *Long-run, once assumed:* a free tier with no real top-of-funnel channel
behind it tends to calcify into a permanent, low-volume cost center nobody wants to kill because
killing it looks like retreating on competitive parity — an inertia trap distinct from, and in
addition to, the per-user cost math in chain C2.

Both order-marked extensions below (chains C1, C3) carry concrete effects from both lenses;
neither extension contradicts any ground truth in section 3, so neither routes back to Phase 2.

### Conclusion C1: A free tier cannot do the "lead-generation" job by pricing/packaging alone, because this company has no inbound acquisition motion to feed it

GT-2? (100% outbound + referral, no inbound channel today)
→ a free tier with no dedicated acquisition investment can only draw signups from people who
already found the company through outbound or referral *[Assumes: A-2 — a free tier is not
automatically a self-serve acquisition funnel; if A-2 were false and packaging alone created
new inbound demand, this hop and the conclusion below would not follow]*
→ redirecting already-sourced prospects into a free tier shifts existing pipeline rather than
creating new top-of-funnel volume
→[2nd] the sales team inherits a new routing and triage burden for free signups it did not
previously have, without a corresponding increase in new pipeline
→[3rd] left unresolved, this becomes ongoing operational drag on the channel that still
generates all of today's revenue, in exchange for a tier that is not generating new volume
→ the lead-generation job commonly attributed to free tiers requires a separate, unbudgeted
inbound or self-serve GTM investment, not a pricing change alone

**Pre-check:** head GT-2? · ?-marked: GT-2? · lowest cited: none · Inputs ceiling: MEDIUM
**Confidence:** MEDIUM — GT-2? is unverified; pulling current CRM/web-analytics data on
inbound traffic sources would confirm whether any organic/inbound signal already exists and
would remove this input as a cause of the downgrade. The A-14-style assumption on the first hop
(A-2) is priced: if it fails, the conclusion does not follow, but no rival conclusion is left
standing in its place (section 5, Dead End 1), so this is the chain's one short axis (Inputs).

### Conclusion C2: The breakeven conversion rate looks achievable in isolation against published benchmarks, but the binding constraint is top-of-funnel volume, not the rate itself

GT-1? (ARR $2.4M, 240 teams, ACV ~$10,000/team/year) + GT-6 (breakeven identity r\* = c ÷ m) +
GT-2? (no inbound channel today) + GT-7 (First Page Sage: 3.4%-3.9% observed) + GT-8?
(self-serve ~6%-8%, sales-assisted ~10%-15%, 10x top-to-bottom-quartile spread)
→ the per-active-free-user annual cost brackets to roughly $70-$450/year (infrastructure
~$50-$300 plus support ~$20-$150)
→ the net margin per converted paid customer brackets to roughly $6,500-$8,500/year (ACV
$10,000 at an assumed 65%-85% gross margin) *[Assumes: A-16 — a generic B2B SaaS margin
convention, not this company's verified margin; a materially lower margin raises the required
breakeven rate proportionally, weakening but not reversing the next hop]*
→ applying these brackets to the breakeven identity yields a breakeven conversion rate of
roughly 0.8%-6.9%, central estimate ~2% *[Assumes: A-14 — free users convert or churn out
within roughly one year; a materially longer carry period raises the effective breakeven rate
above this bracket, weakening but not reversing the next hop]*
→ the observed benchmark range sits at or above the ~2% central breakeven estimate, so the rate
itself looks achievable in isolation
→ headroom shrinks toward the pessimistic end of the bracket, where the ~6.9% worst-case
breakeven approaches the ~6%-8% low end of the self-serve benchmark range
→ both of those benchmark sources were measured on products that already had a functioning
acquisition motion feeding the free tier, a precondition this company does not yet meet
→ the binding constraint on breakeven here is top-of-funnel volume, not the conversion rate
itself, so this estimate alone cannot justify a launch decision

**Pre-check:** head GT-1?, GT-6, GT-2?, GT-7, GT-8? · ?-marked: GT-1?, GT-2?, GT-8? · lowest
cited: none · Inputs ceiling: MEDIUM
**Confidence:** LOW — three head inputs are `?`-marked (GT-1?, GT-2?, GT-8?); GT-1? would be
removed as a cause of the downgrade by opening the company's own billing/ARR records, GT-2? by
the same CRM/analytics pull named in C1, and GT-8? by opening the Lenny Rachitsky research
directly rather than relying on a search synthesis. Beyond the Inputs axis, the Inference axis
is also short: the A-16 margin hop and the A-14 carry-period hop each only *weaken* the
"achievable in isolation" finding if their premise fails, rather than leaving the endpoint
unaffected, so neither qualifies for the HIGH-band's "still stands" exception. Two axes short at
once is why this chain is rated LOW rather than MEDIUM, per the calibration rule — this is the
estimate the entire analysis is most honest about not yet knowing.

### Conclusion C3: Without explicit account-level eligibility gating, a free tier creates real cannibalization and pricing-pressure risk against the existing outbound-sold base, independent of lead-generation success

GT-1? (240 outbound-sold teams @ ~$10K ACV)
→ outbound-sold mid-market/enterprise buyers can cite a free tier's mere existence as
renewal-negotiation leverage even without any user migrating to it *[Assumes: A-17 — buyers
reference free-tier availability as leverage even without using it; if A-17 is false, this
specific pricing-pressure channel does not occur, but the independent seat-migration channel
in the next hop still establishes the same endpoint]*
→ independently of negotiation leverage, any existing paying team whose usage fits inside the
free tier's limits has a direct incentive to downgrade seats into it unless access is gated by
account
→[2nd] sales reps uncompensated for defending against downgrades, and champions inside paying
accounts who must now justify the contract, both face new pressure that did not exist before a
free alternative was visible
→[3rd] sustained across multiple renewal cycles, this can lower realized average ACV across the
existing base even without any single formal downgrade event
→ a free tier creates real cannibalization and pricing-pressure risk against the existing
outbound-sold base, through at least two independent channels, regardless of whether the tier
succeeds at generating new leads

**Pre-check:** head GT-1? · ?-marked: GT-1? · lowest cited: none · Inputs ceiling: MEDIUM
**Confidence:** MEDIUM — GT-1? is unverified; confirming the actual ACV/account structure
against billing records would remove it as a cause of the downgrade. The A-17 assumption on the
first hop is priced and the endpoint survives its failure via the independent seat-migration
channel, so Inference stays clean; Inputs is this chain's one short axis.

### Trade-off: pilot vs. full launch vs. status quo (full matrix; collapses to chain C4 below)

Options, including the status quo: **O1** status quo (no free tier); **O2** full, open free-
tier launch now; **O3** a scoped, cost-capped, time-boxed, account-gated pilot.

**Must-have knockout:** any option must include a cost-exposure cap and kill-switch, because
GT-3? establishes that free-tier cost scales with active users with no stated ceiling. O2, in
its ordinary open-signup form, has no such cap and is eliminated outright — not scored low, but
disqualified (recorded in section 5, Dead End 2). O1 and O3 remain.

Criteria (locked before scoring), weights 1-5, anchored 1=worst/5=best:
1. Resolves the core uncertainty (conversion rate, cannibalization) within ~2 quarters — **w=5**
2. Downside/cost exposure if it goes badly — **w=4**
3. Preserves outbound revenue / avoids exposing the $10K-ACV base — **w=5**
4. Speed to a decision-useful answer — **w=3**
5. Competitive-signaling value (addresses the parity pressure in A-1) — **w=2**
6. Organizational/process cost (sales comp, support routing changes) — **w=3**

| Criterion | Weight | O1 score | O1 w×s | O3 score | O3 w×s |
|---|---|---|---|---|---|
| 1. Resolves uncertainty | 5 | 1 | 5 | 4 | 20 |
| 2. Downside exposure | 4 | 5 | 20 | 4 | 16 |
| 3. Preserves ACV | 5 | 5 | 25 | 4 | 20 |
| 4. Speed | 3 | 1 | 3 | 3 | 9 |
| 5. Competitive signaling | 2 | 1 | 2 | 2 | 4 |
| 6. Org cost | 3 | 5 | 15 | 2 | 6 |
| **Total** | | | **70** | | **75** |

**Flip test:** the smallest single-criterion weight change that reverses this result is on
criterion 6 (org cost): moving its weight from 3 to ~4.67 would tie it, which on an integer 1-5
scale means moving it to 5 (a +2 move, the scale's ceiling) — not achievable within a ±1 move.
No other single-criterion ±1 move flips the result either (criterion 1 would need to drop from
5 to ~3.3; criteria 2, 3, 4, and 5 each require weight changes exceeding 5 or below 1 to flip
it, i.e., outside the scale entirely). **No single-criterion ±1 weight change flips this
result** — the pilot's win is robust to small weighting disagreement, though the 75-70 margin
is not large in absolute terms.

### Conclusion C4: A scoped, capped pilot is the recommended option over both an open full launch and taking no action

GT-3? (free-tier cost scales with active users) + C1 (lead-gen job needs unbudgeted channel
investment) + C3 (real cannibalization/pricing-pressure risk via two channels)
→ an uncapped, fully-open full-tier launch has unbounded cost exposure under GT-3? with no
containment mechanism, failing the cost-cap must-have and eliminating that option outright
→ across the locked, weighted six-criterion comparison above, a capped and time-boxed pilot
scores 75 against the status quo's 70, a margin that survives every single-criterion ±1 weight
perturbation tested
→ a scoped, reversible pilot is the recommended option over both an open full launch and taking
no action

**Pre-check:** head GT-3?, C1 (MEDIUM), C3 (MEDIUM) · ?-marked: GT-3? · lowest cited: MEDIUM ·
Inputs ceiling: MEDIUM
**Confidence:** MEDIUM — GT-3? is unverified by this analysis (Finance's own cost model was not
opened); opening that cost model would remove it as a cause of the downgrade. This chain also
cites C1 and C3, both MEDIUM, capping it at MEDIUM regardless; both are explained on their own
confidence lines above. The rival (status quo) is addressed by the flip-test above, which is
this chain's Rivals-axis evidence.

### Conclusion C5: The pilot recommendation is conditional on account-level eligibility gating and an enforced volume/kill-date gate, not an unconditional endorsement of any pilot design

C4 (pilot beats status quo 75-70; full launch eliminated by the cost-cap must-have)
→ the 75-70 margin depends on scoring the pilot's "resolves core uncertainty" criterion near
its ceiling (4 of 5), which in turn requires the pilot to generate real signup volume and to
exclude existing paying accounts from eligibility *[Assumes: A-15 — the product/billing
architecture can technically gate free-tier signup by account or domain; unverified]*
→ if account-level gating turns out not to be technically feasible, the cannibalization
channels in C3 reopen inside the "scoped" pilot itself, and if that happens the pilot's
ACV-protection score falls toward the status quo's — which the flip-test arithmetic above shows
is, on its own, enough to erase the 75-70 margin
→ the recommendation to pilot is therefore conditional: it holds for a pilot design that
enforces account-level eligibility gating and sets an explicit minimum-volume/kill-date gate,
not for an unconditionally-designed pilot

**Pre-check:** head C4 (MEDIUM) · ?-marked: none · lowest cited: MEDIUM · Inputs ceiling: MEDIUM
**Confidence:** MEDIUM — this chain cites C4 (MEDIUM), capping it there; its own reasoning is a
conditional ("if gating is infeasible, then...") rather than an assertion that gating fails, so
the A-15 annotation does not itself introduce a new shortfall beyond the cap already inherited
from C4. Verifying A-15 (a short engineering/product-architecture check) would let this chain's
own conditional collapse to a definite "pilot is safe to run as scoped" or "pilot needs
redesign," but would not raise the band above C4's own MEDIUM ceiling.

## 5. Abandoned Reasoning

### Dead End 1: Treat the free tier as a straightforward lead-generation funnel replacement for outbound

**What was tried:** Framing the decision as "will a free tier generate enough new leads to be
worth it," and reasoning from generic freemium funnel-math as if this company already had a
self-serve acquisition motion.

**Why abandoned:** This framing silently assumes A-2 and A-8, both of which are contradicted by
GT-2? as a present-tense fact (100% outbound + referral, no inbound channel today). Pursuing it
conflates a pricing/packaging decision with a GTM-channel-building decision — two different
investments with different costs and risk profiles — and would have produced a funnel-math
answer to a channel-existence question.

**What it ruled out:** Saves a future analyst from re-running freemium-funnel benchmarks
(as in chain C2) as if they applied directly to this company's current GTM motion without first
confirming an acquisition channel exists to feed them — chain C1 establishes why that
precondition matters before chain C2's numbers are used.

### Dead End 2: Full, immediate, open free-tier launch to match competitors (option O2)

**What was tried:** Evaluating an unrestricted, fully self-serve free tier, open to anyone,
launched immediately to achieve full competitive parity with GT-5?'s observation that all named
competitors already have one.

**Why abandoned:** Eliminated by the trade-off's must-have knockout in chain C4: GT-3?
establishes that free-tier cost scales with active users, and an open, uncapped launch has no
containment mechanism against that cost — it fails a must-have rather than merely scoring low.

**What it ruled out:** Saves a future analyst from re-scoring O2 against the weighted criteria
in chain C4's trade-off table — it was never a candidate to be weighed against the pilot in the
first place, because it fails on a threshold condition before weighting applies.

### Dead End 3: Use competitive parity (GT-5?) as the primary justification for any free tier

**What was tried:** Leading the recommendation with "competitors all have one, so we need one"
as the dominant rationale, independent of the channel-mismatch and cannibalization findings.

**Why abandoned:** A-1's Challenge verdict in section 2 found no evidence that deals are
actually lost for lack of a free tier, or that the parity-seeking segment overlaps this
company's $10K-ACV buyer (A-10). The trade-off in chain C4 independently assigned competitive
signaling the lowest weight of all six criteria (weight 2), and the Adversarial pass's Cluster D
showed this specific benefit is the easiest for a competitor to neutralize (by expanding their
own free tier in response). A rationale this weak and this easily countered cannot carry a
decision with real downside (chains C2, C3).

**What it ruled out:** Saves a future analyst from re-litigating "but competitors have one" as
a standalone argument — it is real (GT-5?) but demonstrably the weakest and most fragile reason
available, not a reason to skip the channel and cannibalization analysis in chains C1-C3.

## 6. Conclusion

**Recommended approach:** Do not launch an open, full free tier, and do not simply maintain the
status quo either — run a scoped, cost-capped, time-boxed, account-gated pilot free tier, with
a named decision-owner and a hard go/no-go date, before making any permanent packaging decision
(chains C4, C5).

**Key insight:** The real fork in this decision is not "free tier yes or no" — it is which
specific job the tier is supposed to perform, and the job most often used to justify one
(competitive parity) is both the weakest-grounded rationale available here and the one a
competitor can neutralize fastest, while the two jobs that actually carry risk — building a
channel capable of lead-generation, and protecting the existing $10K-ACV base from
cannibalization — do not go away with a half-measure and are not resolved by matching
competitors' packaging (chains C1, C3).

**Trade-offs acknowledged:** Choosing a pilot over an immediate full-parity launch defers
whatever competitive-signaling benefit a free tier might offer, requires near-term investment
in eligibility gating and instrumentation with a named owner, and leaves the breakeven
conversion rate's real-world achievability genuinely unresolved — the Fermi pass suggests the
needed rate (roughly 0.8%-6.9%, central ~2%) is plausible against published benchmarks (3.4%-
3.9% observed on comparable freemium products, 6%-15% for better-performing self-serve/sales-
assisted models) in isolation, but only once a working acquisition channel exists to generate
volume at all — which this company does not yet have. Resolving exactly that gap is the pilot's
job, not a flaw in the recommendation (chain C2; chains C4, C5 govern the recommendation itself).

**Pre-check:** head C1 (MEDIUM), C2 (LOW), C3 (MEDIUM), C4 (MEDIUM), C5 (MEDIUM) · ?-marked:
none directly · lowest cited: LOW · Inputs ceiling: LOW
**Confidence:** LOW — this overall band is driven entirely by chain C2's unresolved inputs
(GT-1?, GT-2?, GT-8?) and its two priced-but-weakening assumptions (A-14, A-16), not by the
decision logic itself: chains C1, C3, C4, and C5 are each independently MEDIUM, and C4's
pilot-over-status-quo result was shown robust to every single-criterion ±1 weight perturbation
tested. In plain terms — the recommendation ("pilot, not a full launch or no action") rests on
reasoning this analysis is reasonably confident in; the specific number this company would need
to hit to justify scaling the pilot into a permanent tier is exactly what remains unknown, and
resolving that number is the stated purpose of the pilot itself, not a residual gap in this
analysis. GT-4?'s confirmation that no internal pilot has ever been run is the direct cause of
why that number cannot be tightened further without new data.
