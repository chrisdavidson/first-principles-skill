## Techniques not applied (process output)

- fishbone — not applicable — the Phase 2 assumption space is directly enumerable (~10 starting assumptions plus 3 inversion-derived preconditions) without needing breadth-first category brainstorming; category mapping would not surface anything direct enumeration missed.
- five-whys (causal mode) — not applicable — this is a build-vs-buy decision, not a diagnostic investigation of a recurring symptom; there is no "why does this keep happening" question in scope.
- five-whys (reduce-to-primitives mode) — not applicable — every Phase 3 ground truth is already atomic (a single price point, a headcount, a quoted guidance passage) and passes the irreducibility test directly; none is a compound claim requiring recursive decomposition.
- theoretical-limit — not applicable — no governing physical law bounds a build-vs-buy engineering/business trade-off; there is no "ceiling the fundamentals permit" question here.
- inversion (Phase 5 adversarial-technique slot) — not applicable — the conclusion is a recommendation/plan (adopt and integrate a managed identity provider), and the decision rule routes plan conclusions to pre-mortem rather than inversion; inversion's Phase 2 slot fired instead (applied to "migration off a vendor is cheap").

Techniques that fired: inversion (Phase 2, on the cheap-migration claim), estimate (chains C1, C2), trade-off (chain C3), second-order (in-place extension of chain C3, both actor and time lenses), pre-mortem (Phase 5 adversarial pass).

## Assumption Audit scan (process output)

| Chain | Step | Step Text (brief) | Assumption surfaced? | Added to Table? |
|-------|------|--------------------|-----------------------|------------------|
| C1 | 1 | components sum rather than overlap | component times additive, minimal reuse | yes (A-14) |
| C1 | 2 | sum brackets to 5-9.5 eng-weeks | none | n/a |
| C1 | 3 | add 30-50% review/hardening pass | 30-50% overhead is representative | yes (A-19) |
| C1 | 4 | convert to $20K-$62K labor | none (arithmetic) | n/a |
| C1 | 5 | 1-2 engineers, 1.5-3.5 months of a 7-person org | skill is fungible across the 7 | yes (A-15) |
| C2 | 1 | 120 tenants under every vendor's entry tier | none | n/a |
| C2 | 2 | no bundled enterprise connections at entry tier | none | n/a |
| C2 | 3 | bracket 5-10 SSO/SCIM connections | near-term growth reaches 5-10 logos at $100-150K MRR | yes (A-16) |
| C2 | 4 | 0.3%-2.5% of MRR, grows with revenue | none (arithmetic) | n/a |
| C3 | 1 | weight time-to-ship/security/opp-cost highest | this weighting reflects the company's real constraints | yes (A-17) |
| C3 | 2 | score Build/Buy, totals Buy=106 vs Build=69 | anchor-scale scores are unbiased | yes (A-20) |
| C3 | 3 | gap survives every single-criterion weight change | none (this is the verification step for A-17/A-20) | n/a |
| C3 | 4 | recommend adopting a managed IdP | none (restates prior hop) | n/a |
| C3 | 5 [2nd] | engineers shift to integration; opex line recurs | finance/deal-desk will track and price the opex line | yes (A-21) |
| C3 | 6 [2nd] | sales pulls forward enterprise interest | faster SSO/SCIM availability changes sales conversations | yes (A-18) |
| C3 | 7 [3rd] | per-connection fee compounds into a cost floor | none (follows from A-16/A-21) | n/a |
| C4 | 1 | SSO/SCIM is additive, not a second build | vendor calls sit behind an internal interface | already present (A-11) |
| C4 | 2 | exposure concentrates in 3 integration-time choices | logs continuously exported; no multi-year lock-in signed | already present (A-12, A-13) |
| C4 | 3 | lock-in is a solvable design problem, not a build reason | none (restates prior hop) | n/a |

All 19 named derivation-chain steps across C1-C4 are covered, in order, with no step skipped. A-11/A-12/A-13 were surfaced earlier, at Phase 2 via the inversion procedure applied to "migration off a vendor is cheap," and the audit confirms they are already present in the Assumptions Table rather than re-adding them — a clean pass, not a gap.

## Adversarial pass (process output)

**Recompute.** C1: sessions 1-2wk + reset 0.5-1.5wk + MFA 1.5-3wk + audit log 2-3wk = 5-9.5 eng-weeks; ×1.3-1.5 review overhead = 6.5-14 eng-weeks; ×$3,000-$4,400/eng-week = $19,500-$61,600, rounded to $20,000-$62,000 — recomputes as stated. C2: 5 connections × $100 (Auth0 rate) = $500/mo low; 10 connections × $125×2 (WorkOS SSO+SCIM) = $2,500/mo high — recomputes to $500-$2,500/month, i.e. 0.3% ($500/$150,000) to 2.5% ($2,500/$100,000) of MRR — recomputes as stated. C3: Build weighted = 5(2)+5(2)+4(2)+3(5)+4(1)+2(5)+3(4) = 10+10+8+15+4+10+12 = 69; Buy weighted = 5(5)+5(4)+4(4)+3(4)+4(5)+2(2)+3(3) = 25+20+16+12+20+4+9 = 106; gap = 37 — recomputes as stated.

**Sensitivity.** The single ground truth whose falsity would flip C3 furthest is GT-2? (team size / no dedicated security engineer) — it is `?`-marked. If GT-2? were false in the most generous direction (a dedicated security engineer exists, or headcount is materially larger), Build's Security score could rise from 2 to 4 and its Opportunity-Cost score from 2 to 4, removing 5(2)+4(2)=18 points of Buy's margin, and if Time-to-Ship also improved from 2 to 4 that removes a further 5(3)=15, leaving a gap of 37-18-15=4 — still Buy, but the margin compresses from 37 to 4. Verification: confirm actual headcount and any security-specialist staffing directly with the company (not available to this analysis). Weakest link per chain: C1 — GT-10?/GT-11? are assumed-with-range Fermi primitives, not measurements; C2 — A-16's growth-scenario bracket is a scenario, not a forecast; C3 — A-17/A-20 (weighting and scoring judgment calls); C4 — A-11/A-12/A-13 are currently unimplemented, which is precisely what the Premise below interrogates.

**Rival.** Headline conclusion (adopt managed IdP): rival is "build in-house" — ruled out in Abandoned Reasoning Dead End 1, via C3's 37-point, weight-perturbation-robust gap. C1: rival is "a batteries-included OSS auth starter kit halves the estimate" — not fully settled; GT-9's per-surface hardening requirement (reset/MFA/session each independently documented) partially rules it out, but this is carried as a named, unsettled rival on C1's confidence line rather than claimed as ruled out. C2: rival is "the bracket omits integration engineering time and support-seat add-ons" — not settled; carried as a caveat on C3 (Trade-offs acknowledged) rather than folded silently into C2. C4: rival is the same "build in-house to avoid lock-in" — points to the same Dead End 1 entry as C3.

**Premise.** The plan has already failed: eighteen months after adopting a managed identity provider for per-tenant auth, the decision is understood internally as a mistake.

**Causes (unfiltered, by stakeholder).** *Engineer:* the integration was rushed to hit the gated release and shipped with client-side-only token trust, reintroducing the exact vulnerability class buying was meant to avoid; no internal abstraction layer was built (A-11 skipped under the same time pressure that motivated buying); the free tier's undocumented rate limit was hit during a traffic spike. *On-call/support:* a vendor-side outage took down login for all 120 tenants at once with no fallback path; support cannot self-serve login-UX fixes because dashboard access controls were never set up. *CTO/finance:* 8 enterprise logos closed in 9 months (faster than GT-1?'s "no enterprise customers yet" baseline), each needing SSO+SCIM, and the per-connection bill grew past $1,000/month before finance had priced it into deal margins; the vendor raised per-connection pricing at renewal, and switching now costs more than building would have because A-11/A-12/A-13 were never implemented; the "free" tier vendor discontinued that plan, forcing an unplanned migration under time pressure. *Competitor/adversary:* a competitor cites "you don't own your identity layer" as a procurement objection and wins a deal; an attacker targets the vendor's well-documented, widely-studied integration surface (a misconfigured redirect URI, a leaked API key) rather than a bespoke system.

**Clusters.**
- Cluster 1 — Time pressure defeats the safeguards: the same release urgency (GT-4?) that justifies buying also creates the conditions under which A-11 and A-12 get skipped, because they aren't required to hit the release date, only to make buying safe over the following two years. Bears on: C3, C4, A-11, A-12.
- Cluster 2 — Single vendor dependency, undiversified: outage, price change, and plan discontinuation are three failure modes tracing to one root — no fallback and no contractual protection (A-13). Bears on: C3 (security-risk score), C4, A-13.
- Cluster 3 — Cost surprise at the moment of success: C2's "low single-digit percentage of MRR" holds only if someone actually prices per-connection identity cost into each enterprise deal before it closes; nothing in the plan assigns that owner. Bears on: C2, C3 (2nd-order opex hop), A-21.
- Cluster 4 — Integration bugs relocated, not eliminated: buying moves risk from "build the primitive" to "correctly configure the vendor's primitive"; GT-9's guidance applies to both, and a rushed, unreviewed integration can reproduce the same OWASP-documented failure classes credited to "buy" as avoiding. Bears on: C3 (security-risk score), GT-9.

**Disposition.**
- Cluster 1 — plan change: A-11 (abstraction layer) and A-12 (log export) become named, merge-blocking scope items on the gated release itself, not deferred work.
- Cluster 2 — accepted risk, named mitigation: single-vendor dependency is accepted at this stage (a second identity integration now reproduces the opportunity-cost problem buying was meant to avoid); mitigated by choosing a vendor with a published uptime SLA and by holding A-13 (short contract term) so a bad renewal can be exited.
- Cluster 3 — plan change: per-connection identity cost pricing becomes an explicit deal-desk/finance checklist item before the first SSO-requiring deal closes, not after.
- Cluster 4 — plan change: a second engineer's review against GT-9's OWASP session-management and authentication checklists becomes a merge-blocking step on the auth integration PR.

**Falsification.** This recommendation is false if the managed-IdP integration, built and reviewed under normal (non-rushed) conditions, costs the team more engineer-time and yields a less secure result than a comparably-scoped, well-reviewed DIY build would have — i.e., if C1's cost/time bracket and C3's security-risk scoring are both wrong in the same direction.

## §6→§4 closure ledger (process output)

- "Adopt a managed identity provider for the new authenticated, per-tenant accounts feature rather than building sessions, reset, MFA, and audit log in-house" → chain C3 ✓
- "provided the integration ships with A-11-A-13 designed in from the start" → chain C4 ✓
- "OSS is not free once security-hardening labor is counted" → chain C1 ✓
- "vendor lock-in is a solvable integration-design problem, not an inherent property of buying" → chain C4 ✓
- "the decisive factors are time-to-ship and security-review capacity under release pressure, not the two objections usually argued first" → chain C3 ✓
- "accepting a recurring per-connection opex line and a single-vendor dependency, mitigated by a published SLA and a short contract term" → chain C3 ✓
- "Confidence: MEDIUM, resting on chains C3 and C4" → chains C3, C4 ✓

## Self-audit scan (process output)

| Chain | Chain Head (brief) | Form conforming? | Rule applied | Dependency clean? | Band | Act attempted? | Edges fired |
|-------|---------------------|-------------------|---------------|--------------------|------|-----------------|-------------|
| C1 | GT-2?, GT-9, GT-10?, GT-11? | yes | n/a | yes | MEDIUM | yes | none |
| C2 | GT-1?, GT-5, GT-6, GT-7 | yes | n/a | yes | MEDIUM | yes | none |
| C3 | GT-1?, GT-2?, GT-4?, GT-9, GT-8?, C1 (MEDIUM), C2 (MEDIUM) | yes | n/a | yes | MEDIUM | yes | none |
| C4 | GT-5, GT-6, GT-7 | yes | n/a | yes | MEDIUM | yes | none |

| §6 Span (brief) | Construct | Claim under R11? | R11 clause applied | Chain cited |
|-------------------|-----------|-------------------|----------------------|---------------|
| Recommended approach: adopt a managed IdP... | bold lead-in | yes | bold lead-in with content on same line | C3, C4 |
| Key insight: OSS isn't free... lock-in is solvable... | bold lead-in | yes | bold lead-in with content on same line | C1, C4, C3 |
| Trade-offs acknowledged: recurring opex, single-vendor dependency... | bold lead-in | yes | bold lead-in with content on same line | C3 |
| Pre-check: head C3 (MEDIUM), C4 (MEDIUM)... | bold lead-in | no | direct entailment of the Confidence line it precedes and mechanically mirrors | n/a |
| Confidence: MEDIUM... | bold lead-in | yes | bold lead-in with content on same line | C3, C4 |

Scan complete: 4 chain rows, one per section-4 chain block in order; 5 section-6 rows, one per construct in order — 4 claims under R11, 1 excluded. 0 chains malformed, 0 claims untraced.

## Self-Audit Gate (process output)

**Criterion 1: Identify Essence**
Quoted span: "Core problem: Given a 7-person, resource-constrained engineering team building its first per-tenant authentication system under a hard release deadline, should the authentication guarantees ... be produced by code the team writes and operates itself, or by a system the team configures and a vendor writes and operates ... and which choice better survives the specific constraints this company actually has"
Band: **Rigorous**
Justification: the statement names the actual decision (not the triggering event "ship the release" or a restatement of the prompt), is specific to this company's team-size/timeline/enterprise-readiness constraints, and each success criterion is a checkable verb+subject+outcome triplet against the Conclusion section.

**Criterion 2: Challenge Assumptions**
Quoted span (Assumption Audit scan, process output): "All 19 named derivation-chain steps across C1-C4 are covered, in order, with no step skipped." Combined with Assumptions Table rows A-4 ("Discard as stated") and A-8 ("Discard as stated") showing challenge was applied, not merely Accept.
Band: **Rigorous**
Justification: all 21 rows use the four-type scheme, Verdict cells use token+em-dash form, multiple rows score Challenge/Discard rather than uniform Accept, unverified assumptions used in chains read "unverified — flagged," and the Assumption Audit scan confirms exhaustive coverage of every named chain step.

**Criterion 3: Establish Ground Truths**
Quoted span: "?-marked: GT-1, GT-2, GT-3, GT-4, GT-8, GT-10, GT-11 (7 of 11)" — checked against the Ground Truths list, which carries `?` on exactly those seven IDs and no others.
Band: **Rigorous**
Justification: stable IDs, provenance labels on every entry, the enumeration matches the list on inspection, GT-5/GT-6/GT-7/GT-9 name their read-at-source location, and GT-8?'s Phase 3 record discloses an ambiguous-citation reason (no single primary source pinned among aggregator results) rather than silently dropping the `?`; no discarded Phase-2 assumption appears in the list.

**Criterion 4: Reason Upward**
Quoted span (self-audit scan, chain-form table): "C1 | ... | yes | n/a | yes | MEDIUM | yes | none" repeated with equivalent yes/yes verdicts for C2, C3, C4 — all four chains form-conforming and dependency-clean.
Band: **Rigorous**
Justification: every conclusion has exactly one chain, each chain names inputs in head form, contains genuine intermediates, every step that surfaced a new assumption carries an inline `[Assumes: X]` mark per the Assumption Audit scan, no analogy is used as direct evidence, and Abandoned Reasoning documents three dead ends with specific structural reasons (a knockout, a robust-margin ruling-out, and a no-defensible-anchor withdrawal).

**Criterion 5: Validate**
Quoted span (Adversarial pass record): "Cluster 1 — plan change: A-11 ... and A-12 ... become named, merge-blocking scope items on the gated release itself, not deferred work." (representative of all four clusters carrying a named disposition)
Band: **Rigorous**
Justification: every chain's weakest link is named, every MEDIUM confidence line names its `?` inputs with a verification path and its cited chains without re-explaining them, the Conclusion's MEDIUM rating matches its weakest contributing chains (C3, C4), no chain rated HIGH consumes a `?` input, calibration holds throughout (Inputs-axis `?` presence correctly caps C1-C3 at MEDIUM; C4's clean Inputs axis but short Inference axis is also correctly capped at MEDIUM, not over- or under-rated), and the full five-step adversarial pass ran with every part present, including four clusters each carrying a disposition.

**Criterion 6: Conclusion-to-Ground-Truth Traceability**
Quoted span (self-audit scan, claim-inventory table): "Recommended approach: adopt a managed IdP... | bold lead-in | yes | ... | C3, C4" through "Confidence: MEDIUM... | bold lead-in | yes | ... | C3, C4" — 4 of 5 constructs are claims, all 4 cite chains.
Band: **Rigorous**
Justification: every Conclusion-section claim traces to a named section-4 chain, no new reasoning is introduced in section 6, and the Key Insight ("OSS isn't free, and lock-in is a solvable design problem, not an inherent property of buying — the actually decisive factors are time-to-ship and security-review capacity") is a distinct, non-obvious finding rather than a restatement of "adopt a managed IdP."

**Gate result:** 6 of 6 criteria Rigorous. No criterion Absent; 0 criteria Hand-wavy (well under the 1-criterion cap). Both clearing conditions met — the gate clears on the first pass, with no Fix/Repeat iteration required.

---

## 1. Problem Essence

**Core problem:** Given a 7-person, resource-constrained engineering team building its first per-tenant authentication system under a hard, revenue-gating release deadline, should the authentication guarantees this feature must provide — session integrity, credential recovery, second-factor verification, and an auditable access record — be produced by code the team writes and operates itself (build on an OSS library), or by a system the team configures and a vendor writes and operates (buy a managed identity provider) — and which choice actually survives this specific company's constraints (a whole-org team size of 7, a hard near-term deadline, and no enterprise customers today)?

**Success criteria:**
1. The Conclusion section names exactly one of {Build, Buy} as the recommended approach, not a hedge — verifiable by reading the Recommended-approach line.
2. The recommendation traces to a section-4 chain that explicitly weighs time-to-ship, security risk, and near/future cost against this team's actual size and deadline — verifiable by inspecting chain C3's criteria set and weights.
3. The Conclusion states what happens to the recommendation if the company lands an enterprise customer requiring SSO/SCIM sooner than expected — verifiable by confirming a Conclusion-section line traces to chain C4 or to C3's second/third-order extension.
4. The Conclusion's confidence rating names every `?`-marked or non-HIGH input it depends on directly, per D-07 — verifiable by inspecting the Confidence line's explanation.

---

## 2. Assumptions Table

| Assumption | Type | Treatment | Verdict | Verification |
|------------|------|-----------|---------|--------------|
| Buy is always the safer choice for authentication | convention | explicitly challenge before use | Challenge — true only if the integration itself is built correctly (session validation, token handling); a badly-integrated vendor can be less safe than a minimal, well-scoped DIY system | unverified — flagged |
| Building in-house gives more control | convention | explicitly challenge before use | Challenge — control without maintenance capacity is unmanaged liability, not control, given GT-2?'s absence of a dedicated security engineer | unverified — flagged |
| We can migrate off a managed vendor later cheaply | untested belief | verify via inversion | Challenge — true only conditional on A-11/A-12/A-13 below, per the inversion analysis | unverified — flagged |
| An OSS auth library is free | convention / untested belief | explicitly challenge before use | Discard as stated — license cost is $0, but chain C1 estimates $20,000-$62,000 of engineering labor to build the stated scope; "free" applies to the artifact, not the total cost | unverified — flagged |
| No enterprise customers yet means SSO/SCIM isn't a near-term requirement | current constraint | record expiry conditions | Accept for current release scope only — expires the moment the company enters late-stage negotiation with its first mid-market/enterprise account (GT-8?) | unverified — flagged |
| A 7-person team can absorb the full build scope without slowing the core roadmap | untested belief | verify via estimate | Challenge — chain C1 estimates 15-40% of near-term team capacity concentrated on one release | unverified — flagged |
| Managed-IdP cost stays affordable as the company grows | untested belief | verify via estimate | Challenge — addressed by chain C2 | unverified — flagged |
| Security/compliance liability is lower if we own the code | convention / untested belief | explicitly challenge before use | Discard as stated — liability sits with the company regardless of authorship; a vendor's externally-audited baseline (GT-9) is not reproducible by a 7-person team on this timeline | unverified — flagged |
| Sessions, reset, MFA, and audit log are roughly equal-effort build components | untested belief | verify | Discard as stated — chain C1's bracket shows MFA and audit log are the longer-tail items | unverified — flagged |
| The release deadline can accommodate a full DIY security-review cycle | current constraint | record expiry conditions | Challenge — expires only if the CTO explicitly agrees to slip the gated revenue release; not stated as available (GT-4?) | unverified — flagged |
| A-11: an internal auth/session abstraction layer isolates vendor SDK calls behind an internal interface | untested belief | verify/implement | Challenge — not yet built; load-bearing for chain C4 | unverified — flagged |
| A-12: audit logs are continuously exported to company-owned storage, not only retained in the vendor | untested belief | verify/implement | Challenge — not yet built; load-bearing for chain C4 | unverified — flagged |
| A-13: no multi-year exclusive contract is signed while tenant count is still small | untested belief | verify/decide at contract time | Challenge — not yet decided; load-bearing for chain C4 | unverified — flagged |
| A-14: component build times are additive with minimal cross-component code reuse | untested belief | verify | Accept as a conservative bracket assumption — overestimating build cost is the safer direction for a comparison that already favors buy | unverified — flagged |
| A-15: engineering skill is fungible enough that 1-2 of the 7 could be reassigned to auth work | untested belief | verify | Accept — plausible for a 7-person generalist-stage team, but unconfirmed | unverified — flagged |
| A-16: near-term growth reaches 5-10 enterprise SSO-requiring logos around $100,000-150,000 MRR | untested belief | verify | Accept as an illustrative bracket, not a forecast commitment | unverified — flagged |
| A-17: time-to-ship, security risk, and opportunity cost should dominate the criteria weighting | untested belief (value judgment) | explicitly challenge before use | Accept — directly justified by GT-4? (release urgency) and GT-2? (whole-org team size), the two most load-bearing facts in the analysis | unverified — flagged |
| A-18: faster SSO/SCIM availability changes sales conversations and pulls forward enterprise interest | untested belief | verify | Accept as a plausible, unconfirmed second-order effect | unverified — flagged |
| A-19: a 30-50% security-review/hardening overhead is representative for authentication-adjacent code | untested belief | verify | Accept — a common industry rule-of-thumb range, used as a bracket, not a point estimate | unverified — flagged |
| A-20: the 1-5 anchor-scale scores assigned to Build/Buy per trade-off criterion are unbiased | untested belief | explicitly challenge before use | Accept — mitigated, not eliminated, by the flip-test robustness check on chain C3 | unverified — flagged |
| A-21: finance/deal-desk will actually track and price the new per-connection opex line into enterprise deal margins | untested belief | verify/implement | Challenge — this is exactly the failure mode the adversarial pass's Cluster 3 identifies and assigns a plan-change disposition to | unverified — flagged |

---

## 3. Ground Truths

- **GT-1?** The company has ~120 paying tenants at ~$40,000 MRR and no enterprise customers today — unverified: supplied directly by the requester as context, with no source named; not independently confirmed against company records in this analysis.
- **GT-2?** The entire engineering organization is 7 engineers, with no dedicated platform or security engineer — unverified: supplied directly by the requester as context, with no source named.
- **GT-3?** The product currently runs behind a single shared password plus a Stripe customer link; no per-user or per-tenant authentication exists today — unverified: supplied directly by the requester as context, with no source named.
- **GT-4?** The next billed, revenue-bearing release is gated on shipping authenticated, per-tenant accounts, and the CTO treats this as urgent — unverified: supplied directly by the requester as context, with no source named.
- **GT-5** WorkOS AuthKit (session management, password/social login, MFA, user management) is free up to 1,000,000 MAU; Enterprise SSO and Directory Sync (SCIM) are billed separately per connection, starting at $125/month each for 1-15 connections and declining to $65/month at 51-100 connections; audit-log streaming is $125/month per SIEM connection plus $99/month per 1,000,000 events retained — source: workos.com/pricing; read-at-source: live pricing page, plan-comparison table, per-connection SSO/Directory-Sync add-on table, and audit-log meter rows, fetched 2026-09-29.
- **GT-6** Auth0's B2B Essentials plan costs $150/month at 500 MAU and includes 3 enterprise SSO connections, with additional connections at $100/month each (max 30 total); enterprise MFA is a $100/month add-on; audit-log retention on Essentials is capped at 5 days with 1 log stream. The Professional tier is $800/month, includes 5 SSO connections plus MFA, and extends audit retention to 10 days / 2 streams — source: auth0.com/pricing; read-at-source: live pricing page, B2B Essentials and Professional plan cards, fetched 2026-09-29.
- **GT-7** Clerk's Free plan covers up to 50,000 monthly-retained-users (MRU) per app; the Pro plan is $25/month, includes 50,000 MRU plus 1 enterprise SSO connection, with overage at $0.02/MRU; the B2B Organizations add-on is $100/month for 100 monthly-retained-orgs, then $1/month per additional org; audit/admin logs are available only on the Business plan ($300/month) — source: clerk.com/pricing; read-at-source: live pricing page, plan cards, B2B add-on section, and audit-log row on the Business plan, fetched 2026-09-29.
- **GT-8?** Industry reporting describes an "SSO tax" pattern in which SSO/MFA increasingly function as a binary procurement gate for mid-market and enterprise B2B buyers, with cited (unconfirmed at primary source) figures suggesting a majority of enterprise RFPs require SSO/MFA and most mid-market buyers mandate SSO for vendor selection — reported-by-delegate: multiple secondary/aggregator sources returned by search; no single primary research report was identified among them to open directly within this analysis's turn budget (Phase 3 failure record: ambiguous citation — the aggregator sources do not converge on one identifiable primary survey to read).
- **GT-9** OWASP's Authentication Cheat Sheet states that multi-factor authentication "is by far the best defense against the majority of password-related attacks," citing Microsoft analysis that MFA "would have stopped 99.9% of account compromises"; the same page directs session handling to "invalidate sessions after re-authentication and rotate tokens," and routes password-reset design to a dedicated cheat sheet devoted entirely to that flow's failure modes — i.e., OWASP treats password reset, MFA, and session handling as three separate, nontrivial hardening surfaces, not a subroutine of "login" — source: cheatsheetseries.owasp.org/cheatsheets/Authentication_Cheat_Sheet.html; read-at-source: MFA-effectiveness passage and session-invalidation/token-rotation directive, quoted verbatim, fetched 2026-09-29.
- **GT-10?** Assumed-with-range engineering-effort bracket (Estimate procedure, no measured source available for this specific team): sessions 1-2 engineer-weeks, hardened password reset 0.5-1.5 engineer-weeks, TOTP-based MFA with backup codes 1.5-3 engineer-weeks, a queryable/retained audit-log subsystem 2-3 engineer-weeks — unverified: assumed range per general software-estimation experience, not a direct measurement of this team; verification path: run a timeboxed build spike on one component (e.g., password reset) and compare actual to bracket.
- **GT-11?** Assumed-with-range fully-loaded engineer cost bracket for an early-stage US B2B SaaS company in 2026: roughly $3,000-$4,400 per engineer-week — unverified: assumed range per general market knowledge, not a direct measurement of this company's payroll; verification path: request actual fully-loaded cost-per-engineer from finance.

**Provenance summary:**
```text
?-marked: GT-1, GT-2, GT-3, GT-4, GT-8, GT-10, GT-11 (7 of 11)
Read-at-source: GT-5 — workos.com/pricing, plan-comparison + per-connection add-on tables
Read-at-source: GT-6 — auth0.com/pricing, B2B Essentials/Professional plan cards
Read-at-source: GT-7 — clerk.com/pricing, plan cards + B2B add-on + audit-log row
Read-at-source: GT-9 — OWASP Authentication Cheat Sheet, MFA-effectiveness and session-invalidation passages
```
No unsuffixed ground truth in this analysis feeds a HIGH-confidence chain (all four derivation chains are rated MEDIUM — see section 4), so the "every unsuffixed GT feeding a HIGH chain names its read-at-source location" requirement is vacuously satisfied; read-at-source locations are named above regardless, for GT-5, GT-6, GT-7, and GT-9.

---

## 4. Derivation Chains

### Conclusion C1: Building the full DIY scope costs this team roughly 6.5-14 engineer-weeks (~$20,000-$62,000), concentrated on 1-2 of 7 engineers

**Estimate (Fermi) procedure applied.** Target quantity: engineer-weeks (and fully-loaded $) to bring sessions, password reset, MFA, and audit log to a production-hardened, OWASP-aligned state. Unit-factors: per-component duration (weeks) × review-overhead multiplier × $/engineer-week, dimensionally consistent (weeks × $/week = $).

GT-2? (7-person team, no dedicated security engineer) + GT-9 (OWASP: reset/MFA/session are distinct hardening surfaces) + GT-10? (assumed per-component effort bracket) + GT-11? (assumed $/engineer-week bracket)
→ GT-9 treats password reset, MFA, and session handling as separate hardening surfaces, so the four build components add effort rather than sharing it *[Assumes: A-14 — component times are additive with minimal cross-component reuse]*
→ summing GT-10?'s bracketed per-component durations (sessions 1-2wk, reset 0.5-1.5wk, MFA 1.5-3wk, audit log 2-3wk) yields a 5-9.5 engineer-week core build
→ adding a 30-50% security-review and hardening pass, standard for authentication-adjacent code, brackets total effort at roughly 6.5-14 engineer-weeks *[Assumes: A-19 — a 30-50% review overhead is representative]*
→ at GT-11?'s $3,000-4,400 per engineer-week, that bracket converts to roughly $20,000-$62,000 of fully-loaded labor on a non-differentiating feature
→ against GT-2?'s 7-person total headcount, that is 1-2 engineers' full capacity for 1.5-3.5 months, concentrated on the same release the CTO calls urgent *[Assumes: A-15 — engineering skill is fungible enough to reassign 1-2 of the 7]*

**Pre-check:** head GT-2?, GT-9, GT-10?, GT-11? · ?-marked: GT-2?, GT-10?, GT-11? · lowest cited: none · Inputs ceiling: MEDIUM
**Confidence:** MEDIUM — GT-2? (team size/no dedicated security engineer) is unverified; verification: confirm headcount and staffing directly with the company. GT-10? and GT-11? are assumed-with-range Fermi primitives per the Estimate procedure's explicit allowance for "no first-principles value exists, flag as assumed with a defensible range"; verification: run a timeboxed build spike on one component and request actual fully-loaded engineer cost from finance. A-14, A-15, and A-19 are named premises this chain's endpoint depends on and have not been priced beyond the conservative-direction argument given in the Assumptions Table.

---

### Conclusion C2: Managed-IdP cost is near-zero today and stays a low single-digit percentage of MRR through the first wave of enterprise SSO/SCIM adoption

**Estimate (Fermi) procedure applied.** Target quantity: $/month identity-provider spend at current scale and at a bracketed near-term enterprise-adoption milestone.

GT-1? (120 tenants, $40K MRR, no enterprise customers) + GT-5 (WorkOS pricing) + GT-6 (Auth0 pricing) + GT-7 (Clerk pricing)
→ at 120 tenants, total MAU sits well under every vendor's entry-tier ceiling (WorkOS 1M free, Auth0 500 MAU, Clerk 50,000 MRU free), so core login/MFA costs $0-150/month on any of the three
→ none of the three vendors' scale-appropriate tier bundles more than a few enterprise SSO/SCIM connections, so enterprise-readiness spend stays $0 until an SSO-requiring deal actually closes
→ bracketing 5-10 enterprise SSO/SCIM connections against GT-5/6/7's per-connection rates ($100-125 each, doubled where SCIM is also required) yields roughly $500-2,500/month *[Assumes: A-16 — near-term growth reaches 5-10 enterprise logos around $100-150K MRR]*
→ against a plausible $100,000-150,000 MRR at that stage, $500-2,500/month is 0.3%-2.5% of revenue, a cost that grows with revenue rather than ahead of it

**Pre-check:** head GT-1?, GT-5, GT-6, GT-7 · ?-marked: GT-1? · lowest cited: none · Inputs ceiling: MEDIUM
**Confidence:** MEDIUM — GT-1? (tenant count/MRR/no-enterprise-customers) is unverified user-supplied context; verification: confirm against the company's billing/CRM records. A-16's growth-and-connection-count bracket is a named, unpriced scenario assumption, not a forecast; it is used only to illustrate the cost curve's shape, not as a committed prediction.

---

### Conclusion C3: Adopt a managed identity provider for the initial per-tenant authentication release

**Trade-off procedure applied.**

*Options (must include the status quo):* Build (OSS library, in-house), Buy (managed IdP), Do nothing (keep the shared-password + Stripe-link status quo).

*Must-have knockout:* the feature must support per-tenant, per-user authentication — the status quo provides none (GT-3?) and is eliminated outright, not scored. Build and Buy both remain viable.

*Criteria, weights (1-5), and anchors:*

| Criterion | Weight | 1 means | 5 means |
|---|---|---|---|
| Time-to-ship | 5 | >8 eng-weeks to production-ready | <2 eng-weeks |
| Security risk | 5 | high probability of a critical, unpatched vuln class shipping | inherits a continuously-patched, externally-audited baseline |
| Opportunity cost | 4 | consumes >40% of the team's near-term capacity | consumes <10% |
| Near-term $ cost | 3 | >$1,000/month at current scale | <$200/month at current scale |
| Enterprise-readiness cost (SSO/SCIM/audit-log, when needed) | 4 | a second from-scratch build effort later | additive per-connection pricing on the existing integration |
| Control (UX/data-model customizability) | 2 | fully constrained to a vendor's model | fully custom |
| Lock-in / migration risk | 3 | migration effectively forces a mass credential reset and a rebuild | cleanly abstracted, low switching cost |

*Scores (cited to GT/chain evidence):*

| Criterion | Weight | Build score | Buy score |
|---|---|---|---|
| Time-to-ship | 5 | 2 (C1: 6.5-14 eng-weeks) | 5 (vendor-hosted SDK integration, days-to-weeks) |
| Security risk | 5 | 2 (GT-9: reset/MFA/session are each independently hard) | 4 (inherits vendor baseline; residual risk is integration correctness) |
| Opportunity cost | 4 | 2 (C1: 15-40% of a 7-person org, GT-2?) | 4 (a smaller slice of team time) |
| Near-term $ cost | 3 | 5 (OSS license $0, negligible hosting) | 4 (C2: $0-150/month at current scale) |
| Enterprise-readiness cost | 4 | 1 (SSO/SCIM would be a second full build later) | 5 (C2: additive per-connection pricing) |
| Control | 2 | 5 (fully custom) | 2 (constrained to vendor UX/data model) |
| Lock-in / migration risk | 3 | 4 (no vendor, but see C1's under-review-risk) | 3 (real, conditional on A-11/A-12/A-13 — see chain C4) |

Weighted totals: Build = 5(2)+5(2)+4(2)+3(5)+4(1)+2(5)+3(4) = 69. Buy = 5(5)+5(4)+4(4)+3(4)+4(5)+2(2)+3(3) = 106.

*Flip test:* the smallest single-criterion weight change that flips the winner does not exist within the 1-5 weighting scale — zeroing the single largest Buy-favoring criterion (Enterprise-readiness, weight 4) only removes 16 of the 37-point gap; raising Control (the largest Build-favoring criterion) from weight 2 to the maximum of 5 only removes a further 9 points; even combined, Buy still leads. No single-criterion weight change flips this.

**Collapsed chain:**

GT-1? + GT-2? + GT-4? + GT-9 + GT-8? + C1 (build-cost bracket, MEDIUM) + C2 (buy-cost bracket, MEDIUM)
→ weighting time-to-ship, security risk, and opportunity cost highest reflects what GT-4?'s release urgency and GT-2?'s whole-org team size make least affordable to get wrong right now *[Assumes: A-17 — this weighting reflects the company's real constraints]*
→ scoring Build and Buy on that weighted criteria set, using C1's effort bracket, C2's cost bracket, and GT-9's account of where DIY auth fails, yields Buy=106 versus Build=69 *[Assumes: A-20 — the anchor-scale scores are unbiased]*
→ that 37-point gap survives every single-criterion weight change tested on a 1-5 scale, including zeroing the largest Buy-favoring criterion, so the result is robust rather than a near-tie
→ adopting a managed identity provider for the initial per-tenant authentication release is the recommended approach
→[2nd] engineers shift from writing authentication primitives to correctly integrating and operating a vendor SDK, moving the CTO's budget line from one-time build cost to recurring per-connection opex *[Assumes: A-21 — finance/deal-desk will track and price the new opex line]*
→[2nd] sales gains a truthful SSO/SCIM-available answer sooner than a from-scratch build allows, which can pull enterprise interest forward faster than GT-1?'s no-enterprise-customers baseline assumed *[Assumes: A-18 — faster SSO/SCIM availability changes sales conversations]*
→[3rd] as SSO/SCIM connections accumulate, C2's per-connection fee compounds into a recurring cost floor that must be priced into enterprise deal margins, not absorbed as sunk engineering cost

No extension step contradicts a named ground truth; the chain proceeds without returning to Phase 2. Checked against the decision's own success criteria (ship the gated release without materially delaying it; avoid a security/compliance liability a 7-person team cannot sustain): the recurring-opex and vendor-dependency effects create a new, real tension with "control" already priced into the trade-off at low weight, but do not undermine either success criterion.

**Pre-check:** head GT-1?, GT-2?, GT-4?, GT-9, GT-8?, C1 (MEDIUM), C2 (MEDIUM) · ?-marked: GT-1?, GT-2?, GT-4?, GT-8? · lowest cited: MEDIUM · Inputs ceiling: MEDIUM
**Confidence:** MEDIUM — GT-1?, GT-2?, GT-4? are unverified user-supplied context (verification: confirm against company records). GT-8? is reported-by-delegate with an ambiguous-citation Phase 3 failure record (verification: locate and read a single identifiable primary procurement-gate survey). C1 and C2 are named on this chain's head and are each rated MEDIUM; their own confidence lines carry that explanation and are not repeated here. Rival: "build in-house" is not fully ruled out by score alone but by the flip-test robustness shown above (Abandoned Reasoning, Dead End 1). Caveat — no chain — flagged assumption only: Buy's Time-to-ship score of 5 rests on general vendor-integration experience rather than a formal estimate chain symmetric to C1 (see Abandoned Reasoning, Dead End 3).

---

### Conclusion C4: Vendor lock-in is a solvable integration-design problem, not a reason to build auth in-house instead

**Inversion procedure applied (Phase 2), collapsed here.** Claim: "migrating off the chosen managed IdP later, if needed, will be cheap." Inverted: "migrating away will not be cheap." Failure-guaranteeing conditions included: vendor SDK calls scattered across the codebase with no internal abstraction; per-tenant SSO/SAML metadata living only in the vendor dashboard; audit-log history retained only in the vendor's window; a multi-year exclusive contract signed during an early-stage discount. Necessary preconditions derived and tagged load-bearing: A-11 (internal abstraction layer), A-12 (continuous audit-log export), A-13 (no multi-year lock-in). A fourth candidate precondition — a clean password/credential export path — was not tagged load-bearing because it is true under Build or Buy alike and does not differentiate the two options.

GT-5 (WorkOS per-connection pricing) + GT-6 (Auth0 per-connection pricing) + GT-7 (Clerk per-connection pricing)
→ all three vendors price enterprise SSO/SCIM as additive per-connection fees on an already-integrated core product, not as a second ground-up build *[Assumes: A-11 — vendor calls sit behind an internal interface]*
→ the true migration exposure concentrates in three integration-time choices — abstraction layer, log export, contract term — not in the act of buying itself *[Assumes: A-12 — logs are continuously exported]* *[Assumes: A-13 — no multi-year lock-in is signed]*
→ each of those three choices is a low-cost design decision available now, so vendor lock-in is a solvable integration-design problem, not a reason to build auth in-house instead

**Pre-check:** head GT-5, GT-6, GT-7 · ?-marked: none · lowest cited: none · Inputs ceiling: HIGH
**Confidence:** MEDIUM — the Inputs axis is clean (GT-5/6/7 are all read-at-source, unsuffixed), but the Inference axis is short: the endpoint depends on A-11, A-12, and A-13 all holding, and if any fails the endpoint reverses rather than merely weakens (this is the precise scenario the Phase 5 pre-mortem's Cluster 1 names as fatal), so the HIGH exception ("the endpoint still stands if the assumption fails") does not apply. Verification path: implement A-11/A-12/A-13 as named, merge-blocking scope on the integration itself and verify via architecture review before the first enterprise SSO customer is onboarded. Rival: "build in-house to avoid lock-in entirely" is the same rival ruled out for C3 (Abandoned Reasoning, Dead End 1).

---

## 5. Abandoned Reasoning

### Dead End: Build in-house on an OSS library, as the primary recommendation

**What was tried:** fully scored as the "Build" option in the trade-off matrix (chain C3), using C1's effort/cost bracket and GT-9's security characterization across seven weighted criteria.

**Why abandoned:** the weighted total (69) trails Buy (106) by a 37-point margin that survives every single-criterion weight perturbation tested on a 1-5 scale, including zeroing the largest Buy-favoring criterion outright (chain C3, flip test). The two criteria weighted highest given this company's actual constraints — time-to-ship and security risk — are exactly where Build scores worst.

**What it ruled out:** relitigating a from-scratch build is not worth revisiting unless GT-2? (team size/security staffing) or GT-4? (release urgency) materially change — e.g., the company hires a dedicated security/platform engineer, or the release timeline relaxes substantially.

### Dead End: Do nothing — keep the shared-password-plus-Stripe-link status quo

**What was tried:** considered as the required default "no change" option under the Trade-off procedure's rule to always include the status quo.

**Why abandoned:** fails the must-have knockout outright — it provides no per-user or per-tenant authentication, which is the literal requirement of the gated release (GT-3?, GT-4?). It is not a viable option, not merely a low-scoring one.

**What it ruled out:** no further scoring of the status quo was needed; the decision is genuinely binary between Build and Buy, as posed.

### Dead End: A formal Estimate chain for Buy's own integration effort, symmetric to C1

**What was tried:** began sketching a parallel Fermi estimate for Buy's SDK-integration time (wiring, hosted-UI customization, testing), to match C1's rigor for Build.

**Why abandoned:** the only available inputs were vendor-marketing claims ("integrate in days"), which have no defensible first-principles anchor and would violate the same no-analogy/no-unverified-marketing-as-evidence discipline applied everywhere else in this analysis. Manufacturing a weak ground truth to force symmetry with C1 was rejected in favor of leaving Buy's Time-to-ship score as a named, unsettled rival on chain C3's confidence line.

**What it ruled out:** a false-precision "Buy takes exactly N days" claim. The honest state is that Buy's integration effort is bracketed only qualitatively (days-to-weeks) pending an actual spike — a caveat that stays visible on C3 rather than being resolved with fabricated precision.

---

## 6. Conclusion

**Recommended approach:** Adopt a managed identity provider (e.g. WorkOS AuthKit, Auth0 B2B Essentials, or Clerk Pro + B2B add-on) for the new authenticated, per-tenant accounts feature, rather than building sessions, password reset, MFA, and audit log in-house on an OSS library (chain C3), provided the integration ships with an internal abstraction layer, continuous audit-log export, and a short contract term designed in from the start rather than deferred (chain C4).

**Key insight:** The two objections usually argued first about this decision both dissolve under first-principles costing: an OSS library is not "free" once the security-hardening labor to bring reset, MFA, and session handling to an OWASP-aligned standard is counted (chain C1), and vendor lock-in is not an inherent property of buying but a solvable integration-design problem, contingent on three specific, low-cost choices made at integration time (chain C4). The factor that actually decides this case is neither of those — it is time-to-ship and security-review capacity under a hard release deadline with a whole-org team of 7 and no dedicated security engineer (chain C3).

**Trade-offs acknowledged:** Choosing to buy accepts a recurring, compounding per-connection opex line as the company's tenant base and enterprise-customer count grow, rather than a one-time (if underestimated) engineering cost, and accepts a degree of single-vendor dependency for login availability (chain C3). These are judged acceptable at this stage rather than eliminated: the recurring opex must be explicitly priced into enterprise deal margins going forward (chain C3, second-order extension; adversarial pass, Cluster 3 disposition), and the vendor dependency is mitigated, not removed, by choosing a vendor with a published uptime SLA and by holding to a short contract term (A-13; adversarial pass, Cluster 2 disposition).

**Pre-check:** head C3 (MEDIUM), C4 (MEDIUM) · ?-marked: none · lowest cited: MEDIUM · Inputs ceiling: MEDIUM
**Confidence:** MEDIUM — the recommendation rests on chains C3 and C4, both rated MEDIUM; neither chain's own confidence line is re-explained here. C3's rating traces to unverified company-context ground truths (GT-1?, GT-2?, GT-4?) and a reported-by-delegate procurement-gate statistic (GT-8?); C4's rating traces to three unpriced but named, actionable assumptions (A-11, A-12, A-13) whose failure — per the Phase 5 pre-mortem's Cluster 1 — is precisely what the same release pressure that motivates buying would cause to be skipped. The recommendation is judged robust (chain C3's flip test: no single-criterion weight error flips the winner, and even the single most-levered unverified ground truth, GT-2?, would only compress the margin from 37 points to 4, not reverse it), but it is not HIGH confidence, and it is not unconditional: it depends on A-11-A-13 being implemented as scope on the release itself, not deferred past it.
