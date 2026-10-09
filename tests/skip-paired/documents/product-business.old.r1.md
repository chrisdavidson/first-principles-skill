## Assumption Audit scan (process output)

Scan of every named Derivation Chain step in section 4, in order, checking whether the step
relies on an assumption not already present in the Classified Assumptions Table (section 2).

| Chain | Step | Step Text (brief) | Assumption surfaced? | Added to Table? |
|-------|------|--------------------|-----------------------|------------------|
| C1 | 1 | No self-serve signup mechanism exists, so no visitor currently has a path to become a free user | none | n/a |
| C1 | 2 | Funnel identity (GT-8) holds the traffic term at zero independent of conversion rate | none | n/a |
| C1 | 3 (conclusion) | A free tier's pricing/plan structure alone cannot generate inbound funnel growth without the missing signup mechanism | none | n/a |
| C2 | 1 | Breakeven algebra: k* = cost-per-free-account / ACV | A10 — a converted account pays near the current ~$10,000 ACV, not a lower entry price | yes |
| C2 | 2 | External conversion benchmark overlaps upper half of breakeven bracket; both inputs unmeasured internally | none (already covered by `?` on GT-6/GT-7/GT-4) | n/a |
| C2 | 3 (conclusion) | Serving-cost economics are plausible but not provably favorable; breakeven is a testable open question | none | n/a |
| C3 | 1 | Competitor free-tier value splits into funnel-growth vs. deal-parity mechanisms | none (A8 — the "competitors have it" convention — already in table) | n/a |
| C3 | 2 | GT-5? shows competitors have the feature, not which mechanism drives its value; C1 rules out funnel-growth transfer | none | n/a |
| C3 | 3 (conclusion) | Competitive-parity signal is distinct from, and not evidence for, funnel-growth value | none | n/a |
| C4 | 1 | Trade-off weighted totals (75 / 69 / 68 / 51) across four options | A11 — the locked weights, especially ranking cannibalization-protection above revenue upside, reflect actual strategic priorities | yes |
| C4 | 2 | Flip test: ranking is robust to every single bounded weight move except an indefensible one | none | n/a |
| C4 | 3 (conclusion) | Recommend inbound-motion investment plus a narrow, capped, instrumented pilot via existing leads | none | n/a |
| C4 | 4 [2nd] | Near-term actor effects: sales enablement, competitor messaging, renewal-negotiation risk; engineering load smaller than full public launch | A4 — existing outbound pipeline will not quietly substitute down to the pilot offer (already in table) | n/a |
| C4 | 5 [3rd] | Medium-term: pilot data either clears C1/C2's constraints (broader launch justified) or does not (larger investment avoided); inbound motion raises the funnel ceiling regardless | none | n/a |

Two new assumptions surfaced (A10, A11) and were added to the Classified Assumptions Table in
section 2. One previously-tabled assumption (A4) was re-confirmed as the basis for a chain step
and is referenced inline rather than duplicated.
## Adversarial pass (process output)

**Recompute.**
- GT-1? arithmetic: 240 teams × $10,000/team = $2,400,000 = $2.4M ARR. Recomputed independently: 240 × 10,000 = 2,400,000. Matches.
- C2 breakeven algebra: k* = cost-per-free-account ÷ $10,000. At the low end of GT-7?'s bracket ($10/yr): 10 ÷ 10,000 = 0.001 = 0.1%. At the high end ($500/yr): 500 ÷ 10,000 = 0.05 = 5%. Both recompute cleanly.
- C4 trade-off weighted totals, recomputed per option (criteria order: Revenue[4], Cost[4], Cannibalization[5], Learning[3], Roadmap[3], Competitive[2]):
  - O1 (do nothing): 1·4+5·4+5·5+1·3+5·3+1·2 = 4+20+25+3+15+2 = 69
  - O2 (broad public launch now): 2·4+2·4+2·5+4·3+1·3+5·2 = 8+8+10+12+3+10 = 51
  - O3 (narrow gated pilot only): 2·4+4·4+3·5+4·3+3·3+4·2 = 8+16+15+12+9+8 = 68
  - O4 (invest in inbound + narrow pilot): 3·4+4·4+5·5+3·3+3·3+2·2 = 12+16+25+9+9+4 = 75
  All four recompute to the values cited in C4.

**Sensitivity.** The single ground truth whose falsity would most plausibly flip the headline
recommendation is **GT-2?** (no self-serve inbound channel exists today). GT-2? is `?`-marked
(unverified, user-stipulated, no independent source). If GT-2? were false — i.e., the company
already has meaningful self-serve/inbound traffic infrastructure it did not disclose — C1's
funnel-ceiling constraint would not bind, O2's Revenue-upside and Competitive-signal scores in
C4 would rise sharply, and the trade-off would very plausibly flip toward launching broadly now.
Verification path: pull the company's own web analytics / signup-funnel logs before acting on
this analysis's conclusions — this is cheap and should be done first, independent of everything
else here.

Weakest link per chain: **C1** — GT-2?'s unverified status (as above). **C2** — GT-6? and GT-7?
combine unverified status with demonstrably low source-quality (the one primary-source check
attempted, OpenView Partners, did not contain the cited figures). **C3** — whether competitors'
free tier is actually driven by funnel mechanics or deal-parity signaling is untested either way.
**C4** — inherits C2's LOW rating via the head-citation ceiling rule, so the recommendation's
confidence is gated on the same unverified cost/conversion benchmark as C2.

**Rival.**
- Headline (C4) rival: launch the broad public free tier now (O2). Ruled out by the trade-off's
  weighted scoring (51 vs. 75) and the flip test: the maximum single bounded-weight swing in O2's
  favor (raising the Competitive-signal weight to its ceiling of 5) still leaves O4 ahead by the
  equivalent of 15 weighted points, so no single defensible weight correction reverses this
  ranking (see Abandoned Reasoning, Dead End 2, for the closest related reasoning path and why it
  was rejected).
- C1 rival: meaningful traffic already exists and could still convert even without a formal
  inbound channel. Addressed in-chain: C1's first hop shows no mechanism exists for *any* volume
  of traffic to convert today, regardless of how much there is, so this rival does not rescue a
  near-term revenue ceiling above roughly zero.
- C2 rival: this company's true cost-per-free-account or conversion rate differs materially from
  the cited external range (in either direction). This rival is **live and unsettled** — nothing
  in the given facts or in this analysis resolves it; the only available observation that would
  settle it is running the measured pilot C4 recommends. Named explicitly on C2's confidence line.
- C3 rival: competitors' free-tier benefit transfers directly to this company by analogy. Ruled
  out by C1, cited on C3's head: the inbound-infrastructure precondition the funnel-growth
  mechanism requires is the exact thing C1 shows is missing.

**Adversarial technique — Pre-mortem** (the conclusion is a recommended plan, so pre-mortem
applies per the decision rule against inversion).

**Premise:** It is twelve months from now. The inbound-motion investment and the narrow gated
pilot have already failed to produce a defensible go/no-go answer on a broader free tier, and
leadership considers the initiative a wasted quarter of roadmap and marketing budget. What
caused this?

**Causes** (unfiltered, from the implementer/engineering, sales-rep, finance/exec, and
competitor viewpoints):
1. (Engineering) The "narrow" pilot's account-provisioning/feature-gating/billing-plan plumbing
   took far longer than estimated, eating the same roadmap capacity the plan claimed to protect.
2. (Engineering) Abuse/security exposure from even a small number of free/trial accounts was
   underestimated, forcing emergency guardrail work.
3. (Sales) Reps used the pilot sandbox as a crutch to avoid pricing conversations, quietly
   extending "free evaluation" access indefinitely — cannibalization that is never labeled as such.
4. (Sales) The free offer's existence leaked into prospect conversations and became a price
   anchor ("why isn't this just free"), hardening the exact price-commoditization risk (A6) the
   plan was meant to avoid.
5. (Finance/exec) Cost-per-free-account came in far above the bracketed estimate (GT-7?) because
   free/trial users were routed to the same high-touch support team built for $10k accounts, with
   no lower-cost support tier ever built — breaking the core cost assumption (GT-3?/A3).
6. (Finance/exec) The inbound-content/SEO investment was cut before its typical 6–12-month payoff
   window, so the "measured, staged" plan collapsed into the same short-termism it was meant to avoid.
7. (Competitor) A competitor used this company's public silence on "free tier" during the pilot
   period as a competitive-displacement talking point and won bake-offs a visible offer might
   have blocked.
8. (Cross-cutting) No single owner ran the pilot end-to-end, so the conversion/cost
   instrumentation that was the entire point of running it (resolving GT-4?) was never cleanly
   built, and twelve months later internal data is no better than it is today.

**Clusters:**
- **Cluster A — Pilot infra creep** (causes 1, 2). Bears on C4's Roadmap-protection score and A5
  — invalidated if the pilot's engineering cost is not actually small.
- **Cluster B — Quiet cannibalization via sales behavior** (causes 3, 4). Bears on A4/A6 and
  C4's Cannibalization-protection score, which already gave the pilot option 3/5 rather than 5/5.
- **Cluster C — Support-cost assumption failure** (cause 5). Bears directly on GT-3?/A3 and C2's
  cost bracket (GT-7?) — the single most damaging cluster, since it invalidates C2's entire
  breakeven calculation, not just a side risk.
- **Cluster D — Under-resourced, impatient measurement** (causes 6, 8). Bears on C4's
  Learning-value score and the entire premise of "measure before committing" — if the
  measurement itself is starved, the plan delivers neither O2's upside nor O1's safety.
- **Cluster E — Competitive silence cost** (cause 7). Bears on C3 and GT-5?.

**Disposition:**
- Cluster C — **Fatal if unresolved** (breaks the economic case outright). Plan change: instrument
  and measure actual support/infra cost per pilot account from day one rather than relying on
  GT-7?'s external bracket; set a cost tripwire — if cost-per-pilot-account exceeds a named
  threshold for two consecutive months, pause expansion and re-route to Finance for re-scoping.
  Owner: Finance, reviewed monthly.
- Cluster D — **Fatal to the plan's value even if not to the company** (wastes the quarter without
  resolving uncertainty, matching the premise exactly). Plan change: name one accountable pilot
  owner (not split across functions) with a Finance-agreed minimum runway of two full quarters,
  fixed before kickoff. Tripwire: no named owner or no agreed runway exists before the pilot
  starts. Owner: the initiative's sponsor, checked before kickoff.
- Cluster A — **Costly but survivable.** Plan change: timebox the pilot's technical build with a
  two-week spike before further commitment, scoped to reuse existing account/tenant
  infrastructure and introduce no new abuse-surface primitives. Tripwire: the spike estimate is
  exceeded without product/eng sign-off. Owner: engineering lead, checked at spike end.
- Cluster B — **Costly but survivable.** Accepted risk, named mitigation: give reps a written
  pilot-usage policy (eligibility, time-boxed access, no silent permanent downgrades) and track
  pilot-account-to-lost-deal correlation monthly. Tripwire: any positive correlation appears.
  Owner: sales ops, monthly.
- Cluster E — **Tolerable.** Accepted risk, named mitigation: equip sales with an immediately
  available answer ("a guided evaluation/sandbox for qualified prospects") rather than treating
  the absence of a public free tier as undefended. Owner: sales/competitive intel, quarterly
  review of CRM loss-reasons for "no free tier" mentions.

**Falsification.** This analysis's conclusion is false if, once the inbound-motion investment and
gated pilot run for the minimum agreed runway, the measured cost-per-free-account and
free-to-paid conversion rate clear C2's breakeven threshold **and** the inbound investment
measurably raises top-of-funnel traffic beyond the near-zero baseline in C1 — in that case a
broader public self-serve free tier is justified sooner than this recommendation stages it, and
continuing to withhold it would be the error.
## Techniques not applied (process output)

- fishbone — not applicable — the assumption space for this decision was adequately enumerated
  by inversion's failure-mode brainstorm (A2–A9) without needing a separate breadth-first
  cause-category pass; the decision is a single yes/no/staged choice with one dominant causal
  chain (acquisition-motion → funnel mechanics → economics), not a multi-causal symptom needing
  category-based brainstorming.
## §6→§4 closure ledger (process output)

- "Do not launch a broad public self-serve free tier now; instead invest in building a low-cost inbound/content top-of-funnel motion while running a narrow, capped free or trial pilot limited to existing outbound and referral leads, instrumented from day one to measure real conversion and cost data, with named tripwires before any broader launch decision" → chain C4 ✓
- "A free tier is a conversion multiplier applied to existing top-of-funnel traffic, not a traffic generator in its own right, so its realistic near-term revenue ceiling is bounded near zero without a self-serve inbound channel regardless of how favorable its conversion economics turn out to be — making both 'competitors have it' and 'the breakeven math could work' true and insufficient on their own" → chains C1, C2, C3 ✓
- "This path accepts slower, less visible progress on competitive-parity perception and defers any near-term inbound-driven revenue, in exchange for protecting the existing $2.4M outbound-sourced pipeline from cannibalization and avoiding a large, poorly-bounded engineering commitment before the company has any internal data on its own conversion and cost figures" → chain C4 ✓
- "LOW — capped by chain C2 (LOW), which chain C4 cites on its head; chains C1 and C3 are each MEDIUM" → chains C1, C2, C3, C4 ✓

All four Conclusion-section claims are traced. No claim was cut.
## Self-audit scan (process output)

| Chain | Chain Head (brief) | Form conforming? | Rule applied | Dependency clean? | Band | Act attempted? | Edges fired |
|-------|---------------------|-------------------|---------------|--------------------|------|-----------------|-------------|
| C1 | GT-2?, GT-8 | yes | n/a | yes | MEDIUM | no | none |
| C2 | GT-1?, GT-3?, GT-6?, GT-7? | yes | n/a | yes | LOW | yes | none |
| C3 | GT-5?, GT-2?, C1 | yes | n/a | yes | MEDIUM | no | none |
| C4 | C1, C2, C3, GT-1?, GT-3?, GT-4? | yes | n/a | yes | LOW | no (inherits C2's prior attempt via citation) | none |

| §6 Span (brief) | Construct | Claim under R11? | R11 clause applied | Chain cited |
|-------------------|-----------|-------------------|----------------------|---------------|
| Recommended approach: do not launch broadly now; invest + narrow pilot | bold lead-in | yes | bold lead-in whose colon closes the bold span | C4 |
| Key insight: free tier multiplies existing funnel, does not create it | bold lead-in | yes | bold lead-in whose colon closes the bold span | C1, C2, C3 |
| Trade-offs acknowledged: slower visible progress, deferred revenue, for pipeline protection | bold lead-in | yes | bold lead-in whose colon closes the bold span | C4 |
| Confidence: LOW, capped by C2 via C4's head citation | bold lead-in | yes | bold lead-in whose colon closes the bold span | C1, C2, C3, C4 |

Scan complete: 4 chain rows, one per section-4 chain block in order; 4 section-6 rows, one per
construct in order — 4 claims under R11, 0 excluded. 0 chains malformed, 0 claims untraced.
## Self-Audit Gate (process output)

**Criterion 1: Identify Essence**
Quoted span: "Should this company add a free tier now, given it has no self-serve acquisition motion today and free-tier costs scale with usage whether or not free users ever convert — and if not now, what, if anything, should it do instead to address the growth-capacity problem a free tier is being asked to solve?"
Band: **Rigorous**
Justification: the statement names the core decision (not the triggering prompt or a symptom), each of the five success criteria is a verb+subject+outcome triplet checkable directly against section 6 (e.g., "the Conclusion names a concrete next action and tripwire conditions"), and the statement's specific framing (no self-serve motion, usage-scaling cost, growth-capacity reframe) is unique to this problem.

**Criterion 2: Challenge Assumptions**
Quoted span: "A8 | convention | explicitly challenge before use | Challenge — mechanism untested: splits into funnel-growth vs. deal-parity signaling (chain C3); no loss-review data tying lost deals to the absence of a free tier exists in the given facts | unverified — flagged"
Band: **Rigorous**
Justification: all eleven rows use the four-type scheme, every Verdict cell uses a leading token plus em-dash plus specific justification, multiple assumptions are genuinely challenged rather than merely labelled Accept, every chain-used unverified assumption carries "unverified — flagged," and the Assumption Audit scan (process output, Phase 4) confirms the table was checked against every named chain step with two new rows (A10, A11) added from that scan.

**Criterion 3: Establish Ground Truths**
Quoted span: "?-marked: GT-1, GT-2, GT-3, GT-4, GT-5, GT-6, GT-7 (7 of 8); unsuffixed: GT-8 — read-at-source: the funnel-conservation identity itself, verifiable by direct logical inspection"
Band: **Rigorous**
Justification: the enumeration was checked against the Ground Truths list and matches exactly (7 of 8 carry `?`); every unsuffixed GT (only GT-8) feeds only MEDIUM chains (C1, C3), so the HIGH-confidence read-at-source requirement is not triggered; GT-6?'s Phase 3 failure record names the specific source opened (openviewpartners.com/blog/2020-saas-product-benchmarks) and that it did not contain the claimed figures, satisfying the unreachable/does-not-support exception and correctly confining GT-6?/GT-7? to MEDIUM/LOW chains only.

**Criterion 4: Reason Upward**
Quoted span (self-audit scan, chain-form table): "C1 | GT-2?, GT-8 | yes | n/a | yes | MEDIUM | no | none" together with "C2 | ... | yes | n/a | yes | LOW | yes | none", "C3 | ... | yes", "C4 | ... | yes" — all four rows read Form conforming = yes, Dependency clean = yes.
Band: **Rigorous**
Justification: all four chains are form-conforming and dependency-clean per the scan; each chain carries at least one genuine intermediate step; no analogy is used as direct evidence (the "competitors have it" claim is explicitly routed through C3's mechanism-split rather than offered as standalone justification); Abandoned Reasoning documents three dead ends with specific, non-generic abandonment reasons; and the end-of-phase Assumption Audit surfaced and tabled A10 and A11 from chain steps C2-1 and C4-1 respectively, each marked inline with `[Assumes: ...]`.

**Criterion 5: Validate**
Quoted span: "Cluster C — Fatal if unresolved ... Plan change: instrument and measure actual support/infra cost per pilot account from day one ... set a cost tripwire ... Owner: Finance, reviewed monthly" together with "a chain is also rated no higher than the lowest-rated chain its head cites" applied to C4 (LOW, via C2).
Band: **Rigorous**
Justification: every chain names its weakest link and a calibrated band (C1 MEDIUM, C2 LOW, C3 MEDIUM, C4 LOW-via-ceiling-rule); the adversarial pass record carries all parts (Recompute, Sensitivity, Rival, Premise, Causes, Clusters, Disposition, Falsification) with every cluster receiving either a named plan change (Clusters A, C, D) or an explicitly accepted risk with a named mitigation (Clusters B, E); no chain consuming a `?` input is rated HIGH; the Conclusion's LOW rating matches its weakest contributing chain (C2, via C4).

**Criterion 6: Conclusion-to-Ground-Truth Traceability**
Quoted span (self-audit scan, claim-inventory table): all four rows read "Claim under R11? = yes" with "Chain cited" populated (C4; C1, C2, C3; C4; C1, C2, C3, C4) and no row reads "none — untraced."
Band: **Rigorous**
Justification: every Conclusion-section claim cites a specific section-4 chain inline, no claim introduces reasoning absent from section 4, and the Key Insight (the funnel-multiplier-not-generator finding) is a distinct, non-obvious result rather than a restatement of the Recommended approach.

**Gate result:** 0 criteria Absent; 0 criteria Hand-wavy. Both pass conditions are met on the
first scoring pass — no Fix/Repeat loop was required, and no bounded re-entry edge fired.
# First-Principles Analysis: Should the B2B SaaS Product Add a Free Tier?

## 1. Problem Essence

**Core problem:** Should this company add a free tier now, given it has no self-serve
acquisition motion today and free-tier costs scale with usage whether or not free users ever
convert — and if not now, what, if anything, should it do instead to address the growth-capacity
problem a free tier is being asked to solve?

**Success criteria:**
1. The Conclusion section states a definite recommendation (launch broadly / do not launch /
   conditional-staged approach) rather than leaving the question open.
2. The Conclusion's recommendation is traced via a derivation chain to the funnel-mechanics
   constraint arising from having no self-serve channel (i.e., it addresses whether a free tier
   can create inbound demand absent one).
3. The Conclusion explicitly states whether "competitors have it" is sufficient justification on
   its own, and why.
4. The Conclusion names the cost/conversion breakeven condition implied by costs scaling with
   active users, and states whether current evidence clears it.
5. The Conclusion names a concrete next action together with the trigger/tripwire conditions
   that would change the recommendation.

---
## 2. Assumptions Table

**Five-Whys (causal mode) — why do we want this at all?** Applied to surface the real
motivating chain behind "should we add a free tier," rather than taking the question at face
value.

- *Symptom:* The company is asking whether to add a free tier.
- *Why?* → To accelerate growth beyond what the current motion delivers.
- *Why does growth need accelerating?* → Outbound sales + referral is capacity-capped: revenue
  growth is tied to sales headcount and deal velocity, not to any compounding channel.
- *Why is there no compounding channel?* → There is no self-serve/inbound motion for anything —
  free or paid — to run through (GT-2?).
- *Why was none ever built?* → The business has grown to $2.4M ARR successfully without one, so
  building one was never forced onto the roadmap.
- *Counterfactual check:* had the company never asked "should we add a free tier," would the
  underlying growth-capacity constraint still exist? Yes — the constraint is "no compounding,
  low-CAC acquisition channel," not "no free tier" specifically. A free tier is one *candidate
  instrument* toward that root cause, not identical to it, and it only works as an instrument if
  a channel exists for it to compound through.
- *Verdict:* Root cause — outsourcing growth-capacity entirely to outbound headcount, within
  control, correctable by building a compounding acquisition channel (of which a free tier is
  one possible component, not the whole remedy). This finding becomes **A9** below.

**Inversion — what would guarantee this decision fails?** Applied to the claim "we should add a
free tier." Inverted form: "a free tier added now guarantees wasted investment." Failure-
guaranteeing conditions enumerated, with necessary preconditions derived from each (**A2–A8**):

1. No one visits a free-signup page because no inbound traffic source drives anyone there →
   precondition: latent top-of-funnel demand exists and would find the offer (**A2**).
2. Free-tier cost spirals because usage scales unpredictably → precondition: serving cost per
   free account stays low/bounded (**A3**).
3. Existing outbound prospects self-downgrade to the free option instead of signing the $10k
   contract → precondition: no cannibalization of current pipeline (**A4**).
4. Building signup/metering/billing/abuse-prevention infrastructure consumes the same roadmap
   capacity that serves the 240 paying teams → precondition: no material roadmap diversion (**A5**).
5. The free tier anchors buyer expectations and erodes the ability to defend ~$10,000 ACV at
   renewal → precondition: no ACV/price-anchor erosion (**A6**).
6. Signups accumulate but nobody converts them because the org has no lifecycle/PLG nurture
   motion → precondition: the org can build or acquire that motion (**A7**).
7. The decision is made on "competitors have it" alone, without checking whether that mechanism
   even applies to an outbound-only motion → precondition: the competitive-parity argument's
   mechanism actually transfers (**A8**).

All seven preconditions are currently unverified. Per the stakes-escalation rule, several bear
directly on the existing $2.4M revenue base (A4, A6) and are treated as load-bearing throughout
section 4 rather than footnotes.

| Assumption | Type | Treatment | Verdict | Verification |
|---|---|---|---|---|
| A1 — Revenue attributable to a free tier cannot exceed (people who discover/sign up for the offer) × (free-to-paid conversion rate) × (ACV); a free tier multiplies existing top-of-funnel flow, it does not create that flow | physical law | accept as ground-truth candidate | Accept — a conservation-of-flow identity true by construction of any conversion funnel, not negotiable by any decision this company makes | promoted to GT-8, no external citation needed |
| A2 — If a free tier is built, latent top-of-funnel demand exists and will discover and sign up for it | untested belief | verify or flag | Challenge — contradicted in direction by GT-2?'s stated absence of any self-serve channel; no evidence of latent demand is given | unverified — flagged |
| A3 — Free-tier infrastructure and support cost per free account will stay low/bounded | untested belief | verify or flag | Challenge — GT-3? confirms cost scales with active users but not that it stays *low*; magnitude is unmeasured (GT-4?) | unverified — flagged |
| A4 — Existing outbound-sourced prospects will not substitute a free tier for a paid contract | untested belief | verify or flag | Challenge — a real failure mode under inversion precondition 3; outbound reps actively negotiating against a newly visible free option is plausible, not ruled out | unverified — flagged |
| A5 — Building self-serve signup/metering/billing/abuse-prevention infrastructure will not materially divert roadmap capacity from the 240 paying teams | untested belief | verify or flag | Challenge — this is net-new infrastructure per GT-2?, not incremental; opportunity cost is real and unmeasured | unverified — flagged |
| A6 — A free tier will not erode the company's ability to defend ~$10,000 ACV in negotiations and renewals | untested belief | verify or flag | Challenge — price-anchoring risk is a known freemium failure mode and is not addressed by any fact given | unverified — flagged |
| A7 — The organization can build or acquire a lifecycle/PLG conversion motion to actually convert free signups | untested belief | verify or flag | Challenge — the sales/success org is outbound-trained per GT-2?; this is a second capability investment beyond engineering the free tier itself | unverified — flagged |
| A8 — "Competitors have a free tier, therefore we need one" (competitive-parity convention) | convention | explicitly challenge before use | Challenge — mechanism untested: splits into funnel-growth vs. deal-parity signaling (chain C3); no loss-review data tying lost deals to the absence of a free tier exists in the given facts | unverified — flagged |
| A9 — A free tier is the correct and sufficient remedy for the underlying growth-capacity problem (five-whys root cause: no compounding, low-CAC acquisition channel) | untested belief | verify or flag | Challenge — five-whys shows the root cause is the missing channel itself, of which a free tier is one candidate component, not a guaranteed fix on its own | unverified — flagged |
| A10 — A newly converted free-to-paid account would pay near the current ~$10,000 average ACV, not a lower entry-level price point (surfaced in Phase 4 audit, chain C2 step 1) | untested belief | verify or flag | Challenge — if false, the true breakeven conversion rate required is higher than C2 computes, which reinforces rather than undermines the cautious recommendation | unverified — flagged |
| A11 — The locked trade-off weights, especially ranking pipeline-cannibalization protection above near-term revenue upside, reflect this company's actual strategic priorities (surfaced in Phase 4 audit, chain C4 step 1) | convention | explicitly challenge before use | Challenge — defensible given the stakes (losing existing revenue is worse than missing incremental upside) but not independently confirmed with actual finance/exec stakeholders | unverified — flagged |

---
## 3. Ground Truths

**On provenance in this analysis.** Per the Input Contract, a fact the user supplies without
naming an external source enters as `unverified`; naming an internal source (e.g., "Finance")
without this analysis opening that source's own work enters as `reported-by-delegate`. Almost
every fact in this decision is exactly one of those two cases — the company's own business
figures, the competitive claim, and the external benchmarks are all either internal data this
analysis cannot independently audit, or secondary-source figures this analysis could not fully
confirm at their primary source. This is itself a disclosed finding, not an oversight: it is why
the Derivation Chains in section 4 land on MEDIUM/LOW confidence almost throughout, and it is
the direct reason the Conclusion recommends measuring before committing rather than committing
on the data as given.

- **GT-1?** ARR is $2.4M, drawn from 240 paying teams at an average of ~$10,000/team/year —
  unverified: user-stipulated internal business figures, no external source named. Internal
  arithmetic check (not a source, but a self-consistency check this analysis can perform
  directly): 240 × $10,000 = $2,400,000, consistent with the stated $2.4M ARR.
- **GT-2?** 100% of customer acquisition today is via outbound sales and referrals; no
  self-serve inbound channel exists — unverified: user-stipulated, no external source named.
- **GT-3?** Finance confirms free-tier infrastructure and support costs scale with active
  (free) users, not paying users — reported-by-delegate: named source is "Finance" (an internal
  function); Finance's own cost model or analysis was not opened by this analysis.
- **GT-4?** No freemium pilot has ever been run; the company has no internal data on its own
  free-to-paid conversion rate — unverified: user-stipulated statement about organizational
  history, no external source named.
- **GT-5?** All named competitors currently offer a free tier — unverified: user-stipulated, no
  specific competitor list or verification method named.
- **GT-6?** Externally reported B2B SaaS freemium-to-paid conversion rates commonly cluster
  around 1–10%, most frequently cited as 2–5% (with segment variation, e.g., dev tools ~3–7%,
  productivity tools ~1–2%) — unverified, reported-by-delegate. **Phase 3 failure record:**
  this analysis attempted to open a named primary source directly
  (openviewpartners.com/blog/2020-saas-product-benchmarks, via WebFetch) to confirm these
  figures; the page returned was a generic company/portfolio page and did not contain any
  conversion-rate figures — citation does not support the claim at that URL. A secondary source
  (getmonetizely.com) attributes the figures instead to "OpenView Partners' 2022 SaaS
  Benchmarks report," which was not separately located or opened. The remaining secondary
  aggregator sources found (knowledgelib.io, firstpagesage.com) were not read — turn budget;
  several carry anomalous future "last-updated" dates and calculator/marketing-tool framing,
  which this analysis flags as a further reliability caveat rather than treating the figures as
  settled.
- **GT-7?** A commonly cited operational guideline suggests total free-tier serving cost should
  stay under roughly 5% of MRR, and small-scale cloud infrastructure cost for a user base in the
  low thousands of monthly active users commonly runs very roughly $0.05–$0.80/active-user/month
  for infrastructure alone (excluding support labor) — unverified, reported-by-delegate; sourced
  from WebSearch aggregator snippets (getbruin.com, spendark.com, techconcepts.org), not opened
  via WebFetch — not read — turn budget, same reliability caveats as GT-6?.
- **GT-8** A free tier's realized revenue cannot exceed (people who discover and sign up for the
  free offer) × (free-to-paid conversion rate) × (average contract value); a free tier acts as a
  conversion multiplier on existing top-of-funnel flow, it does not by itself create that flow —
  physical-law-type identity (conservation of funnel stages), not an empirical claim; read-at-
  source: the definition itself — directly verifiable by logical inspection, since no conversion
  funnel can output more converted units than it takes in as raw signups.

**Provenance summary:** `?`-marked: GT-1, GT-2, GT-3, GT-4, GT-5, GT-6, GT-7 (7 of 8).
Unsuffixed: GT-8 — read-at-source: the funnel-conservation identity itself (see above); GT-8
feeds only MEDIUM-confidence chains (C1, C3), so no HIGH-confidence read-at-source obligation is
triggered by it.

---
## 4. Derivation Chains

### Conclusion C1: A free tier cannot generate inbound funnel growth without a signup mechanism it currently lacks (theoretical-limit application)

**Governing hard constraint:** GT-8's funnel-conservation identity. **Conventional figure:**
current top-of-funnel self-serve signup volume, which GT-2? establishes is effectively
undefined because no mechanism exists for it at all (not merely low — absent). **Gap:** entirely
a matter of building the missing precondition, not of conversion-rate optimization.

GT-2? (no self-serve inbound channel exists today) + GT-8 (funnel-conservation identity: realized revenue ≤ signups × conversion rate × ACV)
→ the absence of any self-serve signup mechanism stated in GT-2? means no visitor, however many there are, currently has a path to become a free-tier user without the company first building that mechanism
→ under the funnel identity in GT-8, realized revenue from a free tier requires signups to exist before any conversion rate can act on them, so a missing signup mechanism holds the traffic term at zero independent of the conversion-rate term
→ launching a free tier's pricing or plan structure alone, without first building the missing self-serve signup mechanism, cannot by itself generate the inbound funnel growth sometimes assumed to accompany a free tier

**Pre-check:** head GT-2?, GT-8 · ?-marked: GT-2? · lowest cited: none · Inputs ceiling: MEDIUM
**Confidence:** MEDIUM — GT-2? is unverified (user-stipulated, no independent source); the
verification that would remove it as a cause of this downgrade is pulling the company's actual
web analytics / signup-funnel logs to confirm no self-serve mechanism and quantify any existing
site traffic. The rival that "meaningful traffic already exists and could still convert" is
addressed in-chain (hop 1 shows no mechanism exists for any volume of traffic today), so the
Rivals axis is clean; only the Inputs axis is short.

### Conclusion C2: The serving-cost economics of a free tier are plausible but not provably favorable on current evidence

GT-1? (ACV ≈ $10,000/team/year) + GT-3? (free-tier infra/support cost scales with active users, per Finance) + GT-6? (externally reported freemium conversion range, ~1–10%, most commonly 2–5%) + GT-7? (externally reported free-tier serving-cost range, ~$10–$500/free account/year)
→ given a cost-per-free-account-per-year C and GT-1?'s ACV of $10,000, the conversion rate a free cohort needs to clear to pay for its own serving cost is k* = C ÷ $10,000, ranging from about 0.1% at the low end of GT-7?'s bracket to about 5% at its high end *[Assumes: A10 — a converted account pays near the current average ACV rather than a lower entry-level price point]*
→ GT-6?'s externally reported typical range of roughly 1–10% overlaps the upper half of this breakeven bracket but not confidently its low end, so whether a free cohort is self-funding depends sensitively on where this company's actual cost-per-account and actual conversion rate land, and neither figure has been measured internally per GT-4?
→ the serving-cost economics of a free tier are plausible but not provably favorable on external benchmarks alone, making the breakeven condition a testable open question rather than a settled yes or no

**Pre-check:** head GT-1?, GT-3?, GT-6?, GT-7? · ?-marked: GT-1?, GT-3?, GT-6?, GT-7? · lowest cited: none · Inputs ceiling: MEDIUM
**Confidence:** LOW — four `?`-marked inputs on the head (Inputs axis short): GT-1? and GT-3?
would be removed as downgrade causes by pulling actual CRM/billing and Finance cost-model
records; GT-6? and GT-7? would be removed by running the measured pilot this analysis
ultimately recommends (chain C4), since no better external data was reachable (GT-6?'s Phase 3
failure record; GT-7? not read — turn budget). In addition, the rival that this company's true
cost/conversion figures differ materially from the external range is live and unsettled — no
observation currently available except that same pilot settles it (Rivals axis also short, so
two axes are short and the chain is capped at LOW rather than MEDIUM).

### Conclusion C3: "Competitors have it" is a competitive-parity signal, not evidence of funnel-growth value for this company

GT-5? (all named competitors currently offer a free tier) + GT-2? (no self-serve inbound channel exists today) + C1 (a free tier cannot generate inbound funnel growth without a signup mechanism it currently lacks)
→ the mechanism by which a competitor's free tier could matter splits into two distinct channels, organic self-serve funnel growth on one side and deal-level feature-parity signaling inside competitive sales evaluations on the other, and the two require entirely different remedies
→ GT-5? establishes only that competitors have the feature, not which of the two mechanisms produces whatever value they get from it, and C1 already shows this company lacks the inbound infrastructure the funnel-growth mechanism would require regardless of what competitors have built around theirs
→ "competitors have it" is evidence worth testing for a deal-level parity benefit through the existing outbound motion, but it is not evidence that adopting a free tier would generate inbound growth for a company with no self-serve acquisition motion, since that is a different claim requiring a different, currently-missing precondition

**Pre-check:** head GT-5?, GT-2?, C1 (MEDIUM) · ?-marked: GT-5?, GT-2? · lowest cited: MEDIUM · Inputs ceiling: MEDIUM
**Confidence:** MEDIUM — GT-5? is unverified (no competitor list or verification method named;
removed by pulling actual competitive-loss-review data from CRM naming "no free tier" as a
factor) and GT-2? carries the same downgrade cause and removal path as in C1. The rival that
competitors' free-tier benefit transfers directly by analogy is resolved in-chain by citing C1:
the inbound-infrastructure precondition the funnel-growth mechanism requires is exactly what C1
shows is missing, so the Rivals axis is clean.

### Conclusion C4: Invest in a low-cost inbound motion and run a narrow, capped, instrumented pilot through existing leads, deferring a broad public free tier

**Trade-off analysis.** Options: (O1) do nothing — stay outbound/referral-only; (O2) launch a
broad public self-serve free tier now; (O3) launch a narrow free/trial offer gated to existing
outbound and referral leads only, as a sales aid; (O4) invest in building inbound/content
top-of-funnel motion first, running O3's narrow pilot concurrently to generate internal data.
No must-have eliminates an option outright; the one non-negotiable design condition carried into
every free-tier-bearing option is a hard usage/resource cap per account, given GT-3?'s
cost-scaling finding. Criteria, weighted 1–5 and anchored before scoring:

| Criterion (weight) | Anchor 1 | Anchor 5 | O1 | O2 | O3 | O4 |
|---|---|---|---|---|---|---|
| Revenue upside (4) | negligible 12-mo ARR impact | material 12-mo ARR impact given current funnel reach | 1 | 2 | 2 | 3 |
| Cost predictability (4) | open-ended, unbounded risk | fully capped, small in absolute terms | 5 | 2 | 4 | 4 |
| Pipeline/cannibalization protection (5) | high risk of $10k-ACV substitution | no plausible substitution path | 5 | 2 | 3 | 5 |
| Learning value (3) | generates no new internal data | generates clean, decision-useful data | 1 | 4 | 4 | 3 |
| Roadmap protection (3) | large diversion from paying-customer work | minimal diversion | 5 | 1 | 3 | 3 |
| Competitive-parity signal (2) | no improvement | directly closes the gap | 1 | 5 | 4 | 2 |
| **Weighted total** | | | **69** | **51** | **68** | **75** |

C1 (funnel ceiling near zero without a signup mechanism) + C2 (cost/conversion breakeven unresolved) + C3 (competitive-parity signal is distinct from funnel-growth evidence) + GT-1? (ACV/pipeline stakes) + GT-3? (cost scales with active users) + GT-4? (no internal pilot data exists)
→ weighing revenue upside, cost predictability, pipeline-cannibalization protection, internal-learning value, roadmap opportunity cost, and competitive-parity signal across four options with weights locked before scoring yields totals of 75 for investing in inbound motion plus a narrow gated pilot, 69 for doing nothing, 68 for a narrow gated pilot alone, and 51 for a broad public free tier launched now *[Assumes: A11 — the locked weights, especially ranking pipeline-cannibalization protection above near-term revenue upside, reflect this company's actual strategic priorities]*
→ a flip test shows the lead of the top-ranked option over doing nothing survives every single bounded weight change except pushing the revenue-upside weight down to its floor of 1, a correction that would make near-term revenue growth almost irrelevant to the decision and is not defensible, so the ranking is reasonably robust
→ the recommended course is to invest in a low-cost inbound top-of-funnel motion while running a narrow, capped free or trial offer only through existing outbound and referral leads, instrumented to measure real conversion and cost data, deferring a broad public self-serve free tier until that data exists
→[2nd] sales enablement needs, competitor messaging during the pilot period, and renewal-negotiation risk if the pilot becomes visible are the main near-term effects on the people around the decision, while the engineering load stays smaller than a full public launch would require *[Assumes: A4 — existing outbound pipeline will not quietly substitute down to the pilot offer]*
→[3rd] if the medium-term pilot data clears both the funnel-traffic constraint identified in C1 and the breakeven threshold identified in C2, a broader free tier becomes a data-backed next decision, and if it does not, the larger public-launch investment is avoided, so either branch leaves the company better informed while the inbound-motion investment durably raises the funnel ceiling independent of the free-tier decision itself

**Flip-test detail:** the smallest single-criterion weight change that even ties the leading
option with doing-nothing is dropping the Revenue-upside weight from 4 to 1 (a move of 3, to the
floor of the allowed 1–5 range); the next-closest single move (raising Roadmap-protection weight
from 3 to its ceiling of 5) only narrows the lead to an equivalent of 2 weighted points and does
not flip it. No single bounded weight move brings the broad-public-launch option back into
contention (its 24-point gap to the leader cannot be closed by any single criterion's full-range
swing; the largest favorable swing available, maximizing the Competitive-parity weight, closes
only 9 of the 24 points).

**Pre-check:** head C1 (MEDIUM), C2 (LOW), C3 (MEDIUM), GT-1?, GT-3?, GT-4? · ?-marked: GT-1?, GT-3?, GT-4? · lowest cited: LOW · Inputs ceiling: LOW
**Confidence:** LOW — capped by the head-citation ceiling rule: C4 cites C2 (LOW) on its head,
so C4 cannot be rated above LOW regardless of its own axes. GT-1?, GT-3?, and GT-4? would be
removed as downgrade causes by the same internal-data-gathering steps named under C2. The live
rival to this chain's endpoint — launch the broad public free tier now (O2) — is ruled out by
the weighted scoring and flip test above (see also Abandoned Reasoning, Dead End 2), so the
Rivals axis is clean; the LOW rating here is entirely an Inputs-axis consequence inherited from
C2, not a new weakness of this chain's own reasoning.

---
## 5. Abandoned Reasoning

### Dead End: Treating "competitors have it" as sufficient standalone justification

**What was tried:** Accepting GT-5? (all named competitors offer a free tier) as direct
justification for adding one, on the reasoning that matching an established market convention
is itself a safe default.

**Why abandoned:** This is reasoning by analogy without grounding in any verified ground truth
about *why* a free tier works for those competitors — no fact establishes their acquisition
motion, their traffic sources, or whether their free tier is funnel-driven or parity-driven. It
is the direct no-analogies-as-direct-evidence violation the methodology prohibits. Once
decomposed (chain C3), the claim splits into an untested causal mechanism and an untested
transferability assumption, neither supported by GT-5? alone.

**What it ruled out:** Treating competitive parity alone as sufficient grounds for a broad
public launch; narrowed the real decision to the funnel-infrastructure precondition addressed in
chain C1.

### Dead End: Treating the Fermi breakeven estimate (C2) as decisive enough to approve a broad launch

**What was tried:** Computing C2's breakeven bracket, noting it overlaps favorably with the
externally reported conversion range on its upper half, and reading that overlap as "the
economics pencil out, so launch broadly now."

**Why abandoned:** Chain C1 shows the traffic/signup-volume term in the funnel identity is held
near zero regardless of the conversion-rate term. A favorable rate-side breakeven calculation is
necessary but not sufficient — conflating "the rate could plausibly work" with "therefore launch
broadly" ignores the volume constraint and compounds the uncertainty of GT-4?, GT-6?, and GT-7?
all being unverified simultaneously. The intermediate claim could not honestly be pushed to
"therefore launch now" without contradicting C1.

**What it ruled out:** Using cost/conversion economics in isolation, divorced from the
funnel-volume question, as the basis for a go/no-go call. Established that both constraints
(C1's volume ceiling and C2's cost/rate economics) must clear together — which is exactly what
the recommended pilot in C4 is designed to test.

### Dead End: Collapsing the Fermi cost bracket to its most optimistic figure for a cleaner story

**What was tried:** Narrowing GT-7?'s serving-cost bracket to its most optimistic point
(roughly $10/free-account/year) to produce a single clean breakeven number and an unambiguously
favorable narrative.

**Why abandoned:** The estimate procedure's own decision-resolution stop criterion requires
keeping the bracket wide until both ends agree on a decision-relevant outcome. GT-7? is
unverified and its secondary sources showed low editorial reliability (see GT-6?'s Phase 3
failure record and the shared reliability caveat on GT-7?); collapsing to a single optimistic
point before the bracket's ends actually agreed would manufacture false precision rather than
resolve genuine uncertainty.

**What it ruled out:** A "the math is obviously great" framing the actual evidence does not
support; keeps chain C2 honestly rated LOW rather than overclaiming HIGH confidence on an
unverified cost figure.

---
## 6. Conclusion

**Recommended approach:** Do not launch a broad public self-serve free tier now; instead invest
in building a low-cost inbound/content top-of-funnel motion while running a narrow, capped free
or trial pilot limited to existing outbound and referral leads, instrumented from day one to
measure real conversion and cost data, with named tripwires before any broader launch decision
(chain C4).

**Key insight:** A free tier is a conversion multiplier applied to existing top-of-funnel
traffic, not a traffic generator in its own right, so its realistic near-term revenue ceiling is
bounded near zero without a self-serve inbound channel regardless of how favorable its
conversion economics turn out to be — making both "competitors have it" and "the breakeven math
could work" true and insufficient on their own (chains C1, C2, C3).

**Trade-offs acknowledged:** This path accepts slower, less visible progress on
competitive-parity perception and defers any near-term inbound-driven revenue, in exchange for
protecting the existing $2.4M outbound-sourced pipeline from cannibalization and avoiding a
large, poorly-bounded engineering commitment before the company has any internal data on its own
conversion and cost figures (chain C4).

**Pre-check:** head C1 (MEDIUM), C2 (LOW), C3 (MEDIUM), C4 (LOW) · ?-marked: none directly (all `?` inputs route through the cited chains) · lowest cited: LOW · Inputs ceiling: LOW
**Confidence:** LOW — capped by chain C2 (LOW), which chain C4 cites on its head; chains C1 and
C3 are each MEDIUM. The single highest-leverage way to raise this rating is the one named on
chain C1's sensitivity analysis: directly check whether a self-serve inbound channel or
meaningful site traffic already exists (GT-2?) before anything else, since that single fact is
most likely to change the recommendation if it is wrong. The remaining downgrade causes (GT-1?,
GT-3?, GT-4?, GT-6?, GT-7? — all unverified; the live, unsettled rival on C2 regarding this
company's true cost/conversion figures) are each removed by the same instrumented pilot this
recommendation already calls for, which is why the recommendation is to measure first rather
than to commit either way on the evidence as given.
