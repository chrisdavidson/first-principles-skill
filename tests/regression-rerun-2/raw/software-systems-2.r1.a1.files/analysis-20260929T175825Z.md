## §6→§4 closure ledger (process output)

- "Adopt a managed identity provider (WorkOS or Clerk...) now for sessions, password reset, and MFA... build the domain/business-level audit log in-house..." → chain C5 ✓
- "The four capabilities named in the 'build vs buy' framing are not homogeneous... splitting the decision — buying the commodity security surface, building the product-specific one — outperforms treating the four requirements as a single build-or-buy unit" → chain C5 ✓
- "This recommendation accepts an ongoing per-connection vendor cost once enterprise SSO/SCIM requests begin... a vendor migration-effort dependency... and a residual dependency on GT-9?..." → chain C5 ✓ (also cites chain C4 for the contingent-cost point)
- "MEDIUM — the recommendation rests entirely on chain C5, itself capped at MEDIUM by two unverified inputs..." → chain C5 ✓

All four Conclusion-section claims are discharged by inline citation. No claim cut.

## Techniques not applied (process output)

- theoretical-limit (Phase 1 essence-reframe invocation) — not applicable — the core question is a resource-allocation and vendor-selection decision bounded by economic and organizational constraints (team size, timeline, budget, contract terms), not by a convention masking an underlying physical or mathematical ceiling; reframing the essence toward "what do the fundamentals permit once convention is stripped" would not change the question actually being asked.
- theoretical-limit (Phase 4 ceiling-derivation invocation) — not applicable — no conclusion in this analysis turns on a governing hard constraint analogous to a thermodynamic or protocol-minimum bound; the nearest candidate, "the fastest possible time-to-ship," was addressed with the estimate/Fermi technique (chain C2) because engineering time-to-ship has no first-principles physical ceiling comparable to, e.g., Carnot efficiency or the speed of light.
- inversion (Phase 5 adversarial-technique invocation) — not applicable — the headline conclusion is a recommended course of action (a plan: adopt a managed identity provider now, build the domain audit log in-house), not a standalone claim, so per the Phase 5 decision rule the adversarial technique applied is Pre-Mortem, not Inversion; inversion was already applied at Phase 2 to challenge the assumption set (see the Assumptions Table's several Challenge verdicts, notably A-4, A-6, A-7, A-8).
- fishbone (Phase 2 breadth-brainstorm invocation) — not applicable — the assumption space was directly enumerable from the four named requirements (sessions, password reset, MFA, audit log) and the decision axes the prompt itself names (timeline, blast radius, compliance, cost, lock-in, enterprise-readiness) without needing a category brainstorm; a fishbone's marginal value over direct enumeration was low for this bounded a decision.

five-whys (reduce-to-primitives), estimate (Fermi), trade-off, second-order thinking, and pre-mortem all fired and are applied in Sections 3-5 below and in the Adversarial pass record.

## Adversarial pass (process output)

**Recompute.** WorkOS: 120 end users is trivially below the 1,000,000-MAU free threshold → $0/mo, confirmed. Clerk: 120 tenants − 100 free monthly-active-organizations = 20 over threshold × $1/mo = $20/mo, confirmed. Fermi build-path central: 3+4.5+2.5+6.5+4+4 = 24.5 engineer-days ≈ 4.9 weeks, confirmed; low bracket 2+3+2+5+3+3 = 18 days ≈ 3.6 weeks, confirmed; high bracket (4+6+3+8+5+5=31 days) × 1.5 friction multiplier = 46.5 days ≈ 9.3 weeks, confirmed. Buy-specific central: 1.5+0.75+1.5+1.5 = 5.25 days ≈ 1.1 weeks, confirmed. Auth-specific build (24.5 − 8.5 shared) = 16 days ≈ 3.2 weeks, confirmed. Delta: 16 − 5.25 = 10.75 days ≈ 2.15 weeks ("roughly two engineer-weeks"), confirmed. Trade-off weighted totals: Build-only = 5(1)+5(1)+2(5)+4(1)+3(4)+3(4) = 5+5+10+4+12+12 = 48, confirmed. Buy-only = 5(5)+5(5)+2(5)+4(5)+3(2)+3(1) = 25+25+10+20+6+3 = 89, confirmed. Hybrid = 5(4)+5(5)+2(5)+4(5)+3(3)+3(5) = 20+25+10+20+9+15 = 99, confirmed. Flip test: to reverse Hybrid(99) vs Buy-only(89), a 10-point gap, reducing the domain-audit-log-fit weight (currently 3, contributing +4×3=12 to Hybrid's margin) to ≤0.5 is required — the smallest single-criterion move found; no arithmetic error located in any recomputed figure.

**Sensitivity.** The single most load-bearing ground truth is `GT-9?` (whether the release's "audit log" requirement means domain/business events rather than authentication events). It is `?`-marked. If false, the flip test above shows the recommendation reverses to Buy-only (drop the in-house domain-audit-log build entirely). Verification: read the actual feature ticket/spec for this release, or ask the product owner directly what "audit log" is meant to cover. Weakest link per chain: C2's weakest link is `[Assumes: A-9]` (Fermi estimate is informed judgment, not measured team velocity); C4's weakest link is `GT-7?` (SOC2 CC6.1 evidence pattern, reported-by-delegate); C5's weakest link is `GT-9?` (see above) and, secondarily, `GT-8?` (vendor protocol/lock-in characterization, reported-by-delegate).

**Rival.** Headline (chain C5): the strongest rival is Buy-only (adopt the vendor for all four capabilities, including treating its auth-event log as the audit log). It is not fully ruled out — it is bounded by the flip test and by `GT-9?`'s unverified status; Abandoned Reasoning Dead End 3 records it as the named fallback if `GT-9?` is confirmed false. Chain C1: rival is "the Stripe customer link already provides adequate per-tenant identification" — ruled out by GT-1's definition of identification (a billing-portal link carries no session or per-user permission model) and by GT-5's stipulated fact that no per-user separation exists today. Chain C2: rival is "team-specific prior familiarity with a particular OSS library could shrink the build-path estimate below the bracket" — live and unruled-out; it is already the basis of `[Assumes: A-9]` and does not independently lower C2 below its stated MEDIUM band. Chain C3: rival is "un-enumerated per-seat fees (e.g., SMS-based MFA carrier costs) add material cost beyond GT-2/GT-3/GT-4's fee schedule" — checked against the read fee schedules, which name no such fee for TOTP-based MFA; treated as speculative without supporting evidence rather than a live rival. Chain C4: rival is "the company never lands an enterprise customer requiring SSO, making this concern moot" — genuinely live (no enterprise customers exist today) and not ruled out; chain C3 bounds the cost of being wrong about this rival at zero, since SSO/SCIM cost is contingent on an actual connection request rather than paid upfront.

**Premise.** Six months from now, the hybrid authentication rollout has already failed: either a security incident occurred on the new public login surface, or enough of the 120 tenants churned or were locked out during migration that the release is judged a failure, and the team is now doing emergency remediation instead of building product.

**Causes (unfiltered, generated from implementer, support/success, paying customer, CEO/CFO, and adversary viewpoints).**
1. (Implementer) The 120-tenant migration was messier than assumed — duplicate emails across tenants sharing one Stripe billing account, ambiguous admin-vs-member mapping — and blew the 3-6 day migration-component estimate out to three weeks.
2. (Implementer) The vendor's MFA "lost device" recovery flow was accepted as shipped default, unreviewed, and silently reintroduced a weak recovery backdoor.
3. (Support/success) Migration and password-reset emails landed in spam because sending-domain DKIM/SPF was never configured for the new vendor, causing a support spike right after the migration announcement.
4. (Paying tenant/admin) Long-time tenant admins, used to one shared password, mistook the migration email for phishing and ignored it, arriving at go-live locked out.
5. (CEO/CFO) Sales promised SSO to an enterprise prospect before checking per-connection pricing, and the deal's margin did not account for the $65-125/mo line item.
6. (Adversary) Automated credential-stuffing traffic hit the new public login endpoint within days of launch — an attack surface that did not exist under the shared-password scheme — and rate limiting was not confirmed enabled before go-live.
7. (Adversary / supply chain) A CVE in a pinned dependency version (relevant to the domain-audit-log build, which still uses the team's own stack) went unpatched because the release crunch consumed the team's attention.
8. (Implementer) The "straightforward" domain audit log scope-crept into duplicating much of what the vendor's own event log already provides, eating the time savings the hybrid split was supposed to capture.
9. (Support/success) The chosen vendor had an outage during the migration announcement window, tenants could not log in for hours, and support had no prepared message.
10. (Implementer / governance) No one was assigned explicit ownership of the ongoing OSS-dependency patching tax for the domain-audit-log component, so it silently accrued as unowned technical debt.

**Clusters.**
- **Cluster 1 — Migration complexity underestimated** (causes 1, 3, 4). Bears on chain C2 (the Fermi bracket's shared-component estimate) and on the Conclusion's Trade-offs acknowledged claim.
- **Cluster 2 — Security defaults not verified** (causes 2, 6, 7). Bears on chain C1 (the premise that buying strictly reduces GT-1/OWASP-A07 exposure assumes vendor defaults are actually confirmed on, which was never itself established as a ground truth).
- **Cluster 3 — Cost/ownership not budgeted forward** (causes 5, 10). Bears on chain C4 and chain C3's near-zero-cost claim, which is a software list-price fact, not an organizational-process fact.
- **Cluster 4 — Audit-log scope creep erodes the hybrid's time advantage** (cause 8). Bears directly on chain C5's time-to-ship score (4) and the domain-audit-fit rationale (`GT-9?`) that justified the hybrid split; this is the cluster most capable of invalidating the recommendation's own premise.
- **Cluster 5 — Vendor outage with no fallback during the migration window** (cause 9). Bears on chain C5's second-order actor-lens hop about the vendor becoming a shared-uptime dependency.

**Disposition.**
- Cluster 1 — Costly but survivable. Tripwire: a pre-migration tenant-data audit finds more than 15% of tenants with ambiguous or missing email mappings; owner: the migration-script engineer, checked before go-live. Plan change: add an explicit 1-2 day tenant-data audit spike before treating the migration-component estimate as validated.
- Cluster 2 — Fatal if realized (a week-one credential-stuffing breach would be worse than the status quo's already-bad baseline, undermining chain C1's premise). Tripwire: the go-live checklist lacks a signed confirmation, from someone other than the implementer, that rate limiting, anomaly detection, and the MFA-recovery flow were manually tested; owner: engineering lead, checked at the go/no-go review. Plan change: make security-default verification an explicit go/no-go gate, separate from "does login work."
- Cluster 3 — Costly but survivable. Tripwire: a signed enterprise deal includes SSO in scope before the per-connection cost (GT-3/GT-4) has been checked against that deal's margin. Accepted risk with named mitigation: add a one-line cost check to the sales SSO-request handoff, proportionate to the fact that no enterprise deals exist yet.
- Cluster 4 — Fatal to the recommendation's own stated rationale if unaddressed. Tripwire: the domain audit log's spec has not been narrowed to a fixed, small list of named business events before implementation starts. Plan change: scope the domain audit log to a fixed list (e.g., 5-10 named event types) rather than an open-ended "audit everything" ambition, preserving the ~4-day estimate this analysis relied on.
- Cluster 5 — Costly but survivable. Tripwire: no documented fallback or communication plan exists for a vendor outage during the migration window. Accepted risk with named mitigation: subscribe to the vendor's status page and pre-draft a support holding message.

**Falsification.** This recommendation is false if a post-tenant-data-audit re-estimate shows the auth-specific buy-path integration time is not meaningfully less than the build-path time, or if the domain audit log cannot be scoped narrowly enough to preserve its cost advantage over letting the vendor's own event log serve the purpose.

## Assumption Audit scan (process output)

| Chain | Step | Step Text (brief) | Assumption surfaced? | Added to Table? |
|-------|------|-------------------|----------------------|-----------------|
| C1 | 1 | Shared password provides no per-identity boundary, worse than any single OWASP A07 weakness | none | n/a |
| C1 | 2 | Any properly-implemented per-tenant auth is a strict improvement over status quo | none | n/a |
| C1 | 3 (conclusion) | Status quo fails the release baseline; do-nothing knocked out | none | n/a |
| C2 | 1 | Decompose four capabilities into auth-specific vs. shared components | A-9 — Fermi per-component day estimates are informed judgment, not measured team velocity | yes |
| C2 | 2 | Auth-specific build-path central estimate ~3.2 engineer-weeks (bracket 2.1-4.9) | none (covered by A-9 above) | n/a |
| C2 | 3 | Auth-specific buy-path central estimate ~1.1 engineer-weeks (bracket 0.7-1.8) | none (covered by A-9 above) | n/a |
| C2 | 4 (conclusion) | Buying returns ~2 engineer-weeks of capacity; both bracket ends agree | none | n/a |
| C3 | 1 | WorkOS AuthKit costs $0/mo at 120 tenants (MAU-denominated) | none | n/a |
| C3 | 2 | Clerk costs ~$20/mo at 120 tenants (org-denominated) | none | n/a |
| C3 | 3 | SSO/SCIM billed per connection, not per tenant/user | none | n/a |
| C3 | 4 (conclusion) | Buy-path cost decoupled from current revenue, scales with future enterprise events | none | n/a |
| C4 | 1 | SOC2-track buyers typically require SSO/SCIM as baseline evidence | A-5 — enterprise prospects will follow this industry-standard pattern (already in table from Phase 2) | n/a (already present) |
| C4 | 2 | Building SAML/OIDC SSO from scratch later hits the same OWASP A07 failure class, at higher complexity | none | n/a |
| C4 | 3 (conclusion) | Managed IdP converts future SSO into a purchase, provided adapter-layer discipline is maintained | A-6 — adapter-layer discipline maintained at implementation time (already in table from Phase 2) | n/a (already present) |
| C5 | 1 | Weighted trade-off totals: Hybrid 99, Buy-only 89, Build-only 48 | none | n/a |
| C5 | 2 | Flip test: only zeroing domain-audit-log-fit weight reverses the ordering | none | n/a |
| C5 | 3 (conclusion) | Recommend hybrid: buy commodity auth, build domain audit log in-house | none | n/a |
| C5 | 4 (2nd, actor) | Engineers' time shifts from building to integrating, freeing ~2 engineer-weeks | none | n/a |
| C5 | 5 (2nd, actor) | New public login endpoint is a new attack surface; must verify vendor defaults on | none | n/a |
| C5 | 6 (3rd, time) | SSO per-connection pricing becomes a budgetable line item once enterprise deals appear | none | n/a |
| C5 | 7 (3rd, time) | Migration cost rises from moderate to significant if adapter-layer discipline lapses | A-6 — adapter-layer discipline (already in table; referenced again here) | n/a (already present) |

Scan covers all 21 named steps across the 5 section-4 chains, in order, no step skipped.

## Self-audit scan (process output)

**Table 1 — Chain form (section 4)**

| Chain | Chain Head (brief) | Form conforming? | Rule applied | Dependency clean? | Band | Act attempted? | Edges fired |
|-------|---------------------|-------------------|---------------|--------------------|------|-----------------|-------------|
| C1 | GT-5 + GT-1 | yes | n/a | yes | HIGH | yes | none |
| C2 | GT-5 | yes | n/a | yes | MEDIUM | no | none |
| C3 | GT-2 + GT-3 + GT-4 | yes | n/a | yes | HIGH | yes | none |
| C4 | GT-7? + GT-1 | yes | n/a | yes | MEDIUM | yes | none |
| C5 | C1 + C2 + C3 + C4 + GT-1 + GT-8? + GT-9? | yes | n/a | yes | MEDIUM | yes | none |

**Table 2 — Claim inventory (section 6)**

| §6 Span (brief) | Construct | Claim under R11? | R11 clause applied | Chain cited |
|-------------------|-----------|-------------------|----------------------|---------------|
| "Recommended approach:" lead-in + text | bold lead-in | yes | colon closes bold span, prescribed lead-in, always a claim | C5 |
| "Key insight:" lead-in + text | bold lead-in | yes | colon closes bold span, prescribed lead-in, always a claim | C5 |
| "Trade-offs acknowledged:" lead-in + text | bold lead-in | yes | colon closes bold span, prescribed lead-in, always a claim | C5, C4 |
| "Pre-check:" line | prose | no | not one of the four prescribed lead-ins; a structural pre-check field, not an assertion | n/a |
| "Confidence:" lead-in + text | bold lead-in | yes | colon closes bold span, prescribed lead-in, always a claim | C5 |

Scan complete: 5 chain rows, one per section-4 chain block in order; 5 section-6 rows, one per construct in order — 4 claims under R11, 1 excluded. 0 chains malformed, 0 claims untraced.

## Self-Audit Gate (process output)

**Criterion 1: Identify Essence**
Quoted span: "Given an urgent, revenue-gating requirement to ship authenticated per-tenant accounts... which approach... minimizes the risk-adjusted total cost... across both the immediate shipping deadline and the 12-24 month horizon in which enterprise customers requiring SSO/SCIM are expected to arrive?"
Band: **Rigorous**
Justification: The statement names the specific decision (build/buy/hybrid split across four named capabilities) rather than the triggering event ("we need to ship a feature"), and each success criterion is a pass/fail structural test checkable against section 6 (names an approach; states timeline fit; is quantified via Fermi; names flip conditions; addresses SSO/SCIM).

**Criterion 2: Challenge Assumptions**
Quoted span: "A-4 | convention | explicitly challenge | Challenge — the framing implicitly treats 'build' as dependency-free, which does not hold | unverified — flagged" (Assumptions Table) and Assumption Audit scan row "C2 | 1 | ... | A-9 — Fermi per-component day estimates are informed judgment... | yes"
Band: **Rigorous**
Justification: All eight table rows use the four-type scheme with token+em-dash verdicts, at least four rows are Challenge (not merely Accept), unverified-in-chain rows are marked "unverified — flagged," and the Assumption Audit scan is present and exhaustive over all 21 named chain steps with no step skipped.

**Criterion 3: Establish Ground Truths**
Quoted span: "?-marked: GT-6, GT-7, GT-8, GT-9 (4 of 9). Read-at-source: GT-1 (top10.owasp.org/2021/A07..., category description and CWE list quoted verbatim), GT-2 (workos.com/pricing, AuthKit table), GT-3 (workos.com/pricing, Enterprise SSO / Directory Sync tables), GT-4 (clerk.com/pricing, B2B Organizations / Enterprise SSO Add-on sections), GT-5 (this conversation's stipulated Context)."
Band: **Rigorous**
Justification: Every GT carries a stable ID and provenance label, the `?`-marked enumeration matches the four suffixed entries (GT-6, GT-7, GT-8, GT-9) checked against the list, and every unsuffixed GT feeding a HIGH-confidence chain (GT-1, GT-5 → C1; GT-2, GT-3, GT-4 → C3) names its read-at-source location.

**Criterion 4: Reason Upward**
Quoted span (from Self-audit scan Table 1): "C5 | C1 + C2 + C3 + C4 + GT-1 + GT-8? + GT-9? | yes | n/a | yes | MEDIUM | yes | none"
Band: **Rigorous**
Justification: All five chain-form rows read "yes" for Form conforming and "yes" for Dependency clean per the self-audit scan; every conclusion in section 6 traces to exactly one chain (C5); the Abandoned Reasoning section documents four dead ends with the What-was-tried/Why-abandoned/What-it-ruled-out structure, each citing a chain or GT id; no analogy is used as direct evidence; and every chain step introducing a new assumption (C2 step 1, surfacing A-9) carries an inline `[Assumes: A-9]` mark per the Assumption Audit scan.

**Criterion 5: Validate**
Quoted span: "**Confidence:** MEDIUM — the recommendation rests entirely on chain C5, itself capped at MEDIUM by two unverified inputs it cites directly, `GT-8?`... and `GT-9?`..." and the Adversarial pass record's Falsification line: "This recommendation is false if a post-tenant-data-audit re-estimate shows the auth-specific buy-path integration time is not meaningfully less than the build-path time, or if the domain audit log cannot be scoped narrowly enough..."
Band: **Rigorous**
Justification: Every MEDIUM chain (C2, C4, C5) names its specific downgrade cause with a stated verification path (A-9 → track actual hours; GT-7? → open the primary AICPA TSC document; GT-8?/GT-9? → open vendor docs / read the feature ticket); the overall Conclusion confidence (MEDIUM) matches its sole contributing chain C5's band; no chain rated HIGH consumes a `?`-marked input; the adversarial pass record is present in full with Recompute, Sensitivity, Rival, Premise, Causes, Clusters, Disposition, and Falsification, and every cluster in that record carries a named plan change or an explicitly accepted risk with a named mitigation.

**Criterion 6: Conclusion-to-Ground-Truth Traceability**
Quoted span (from Self-audit scan Table 2): "'Recommended approach:' lead-in + text | bold lead-in | yes | colon closes bold span, prescribed lead-in, always a claim | C5" and "'Key insight:' lead-in + text | bold lead-in | yes | ... | C5"
Band: **Rigorous**
Justification: All four Conclusion-section claims trace to chain C5 (with the Trade-offs claim additionally citing C4), no claim introduces new reasoning absent from section 4, and the Key Insight — that the four named capabilities decompose unevenly into commodity-auth versus domain-audit-log work — is a non-obvious finding the literal "build vs buy" framing would not surface, not a restatement of the recommended approach.

**Gate result:** No criterion scored Absent; zero criteria scored Hand-wavy (at most one permitted). The gate is cleared on the first pass; no Fix/Repeat re-score was required.

# Build or Buy Authentication — First-Principles Analysis

## 1. Problem Essence

**Core problem:** Given a 7-person engineering team that must ship authenticated, per-tenant accounts (sessions, password reset, MFA, and an audit log) as the next billed, revenue-gating release, with no per-user authentication in production today, which approach — building on an open-source library, adopting a managed identity provider, or a hybrid split of the four named capabilities across build and buy — minimizes the risk-adjusted total cost (engineering time diverted from the roadmap, security blast radius, compliance/audit readiness, and vendor lock-in) across both the immediate shipping deadline and the 12-24 month horizon in which enterprise customers requiring SSO/SCIM are expected to arrive?

**Success criteria:**
1. The recommendation names a specific approach — build, buy, or a named hybrid split of the four capabilities — rather than restating the binary as posed.
2. The recommendation states whether it can meet the timeline the CTO has framed as urgent, or names the specific alternative timeline it actually requires and why.
3. The recommendation is quantified: it gives an explicit Fermi bracket for build-path engineering time and compares it against a buy-path integration estimate and against vendor cost at the company's current scale (120 tenants) and at a stated future scale.
4. The recommendation states specific, checkable conditions under which it would flip to a different approach.
5. The recommendation explicitly addresses the forward path to SSO/SCIM enterprise-readiness rather than by omission.

A skeptic can verify all five criteria directly against Section 6 without further clarification.

## 2. Assumptions Table

| Assumption | Type | Treatment | Verdict | Verification |
|------------|------|-----------|---------|--------------|
| [A-1] Engineering time is a scarce, non-substitutable resource: a 7-person team can allocate at most 7 person-weeks of capacity per calendar week across all initiatives combined; time spent on auth infrastructure is time not simultaneously available for other roadmap work. | physical law | Accept as ground-truth candidate | Accept — mathematical necessity of exclusive resource allocation, not contingent on this company's choices | Definitional (mutual exclusivity of a bounded resource); no external source needed |
| [A-2] The team currently has no dedicated security engineer or security-focused hire. | untested belief | Verify or flag | Challenge — plausible given a 7-person team running a shared-password scheme in production, but not directly confirmed by the user | unverified — flagged |
| [A-3] "Build in-house on an open-source library/framework" means self-hosting and operationally owning the resulting session store, password-reset flow, MFA secret storage, and audit-log storage — the team, not a vendor, owns patching and incident response. | current constraint | Record expiry conditions | Accept — this is the definitional shape of the "build" option as posed | Definitional, drawn directly from the prompt's option description; expires if the team later hires dedicated security/infra staff |
| [A-4] "Open source = no vendor dependency" — self-hosting an OSS auth library still creates a dependency on that library's maintainers' patch cadence and support quality, typically less accountable than a commercial vendor's contractual SLA. | convention | Explicitly challenge | Challenge — the framing implicitly treats "build" as dependency-free, which does not hold | unverified — flagged (would require researching the specific OSS library's maintenance history before final selection; no specific library was named in the prompt) |
| [A-5] Enterprise prospects for this B2B SaaS product will, once pursued, typically require SSO and SCIM as part of vendor-security due diligence / SOC 2 readiness. | convention | Explicitly challenge | Accept, with caveat — supported by GT-7? | unverified — flagged (GT-7? is reported-by-delegate, not read at the primary AICPA TSC source) |
| [A-6] A well-architected integration (vendor-issued stable user/session identifier held behind an internal adapter layer, rather than coupling application logic directly to vendor-proprietary objects) preserves a moderate-effort migration path to a different OIDC-compliant provider later. | untested belief | Verify or flag | Challenge — plausible and consistent with GT-8?, but not verified against this team's actual future implementation discipline | unverified — flagged; would be confirmed by an architecture review enforcing the adapter-layer pattern at implementation time |
| [A-7] The CTO's "urgent" timeline framing is fixed and non-negotiable, i.e., the release date cannot move even if a faster, safer path is identified. | current constraint | Record expiry conditions | Challenge — the prompt states the CTO "has framed" the timeline as urgent but gives no fixed date; treating it as immovable forecloses a 1-2 day schedule check | unverified — flagged; expires the moment the CTO confirms whether the date is contractual or self-imposed |
| [A-8] "Audit log" in the release requirement refers to a general business/domain event log (who did what to which tenant record), not solely an authentication-event log. | untested belief | Verify or flag | Challenge — this is the crux of the framing challenge in this analysis; not confirmed against the actual product requirement | unverified — flagged; elevated to `GT-9?` for use in chain C5 (see Section 3) |

At least four rows (A-4, A-5, A-6, A-7, A-8) are Challenge, not merely Accept; all four assumption types are represented.

## 3. Ground Truths

**Irreducibility check (5-Whys, reduce-to-primitives mode)**, applied to the compound claim underlying chain C1: "the current shared-password-plus-Stripe-link scheme is the most severe available instance of OWASP A07."
- Constituent (a): "identification" requires distinguishing individual users/tenants from one another — a definitional fact of identity/access-management terminology. Verified — definition, not further reducible.
- Constituent (b): "the current scheme provides zero such distinction" — verified directly from GT-5 below (one shared password across all tenants, plus a billing-portal link). Verified — direct observation of the stipulated scenario.
- Constituent (c): "a scheme with zero identification is the maximal-severity case within OWASP A07's spectrum, since every listed weakness (credential stuffing, weak MFA, session exposure) presupposes some identification already exists to attack" — this is definitional logic about a spectrum's endpoint, not further reducible. Verified.
All three constituents pass the irreducibility test, so the parent claim is verified without an unverified branch; it is not itself listed as a separate GT because it is a derived intermediate (see chain C1), consistent with the rule that a ground truth may not be derived from another item on this list.

- **GT-1** OWASP Top 10 2021, category A07 ("Identification and Authentication Failures"), maps to 22 CWEs and defines vulnerable practices including permitting credential stuffing and brute-force attacks, permitting default/weak/well-known passwords, using weak or ineffective credential-recovery ("forgot password") processes, storing passwords in plain text or weakly hashed form, having missing or ineffective multi-factor authentication, exposing session identifiers in URLs, and failing to correctly invalidate session IDs. — source: OWASP Top 10 2021, A07:2021; read-at-source: top10.owasp.org/2021/A07_2021-Identification_and_Authentication_Failures, category description and CWE-weakness list quoted verbatim.
- **GT-2** WorkOS's AuthKit (session management, password reset, MFA-capable login) is free for the first 1,000,000 monthly active users, with additional usage billed at $2,500/mo per additional 1M MAU. — source: workos.com/pricing; read-at-source: "AuthKit" pricing table ("First 1M MAUs: Free", "Each additional 1M MAUs: $2,500/mo").
- **GT-3** WorkOS prices Enterprise SSO and Directory Sync (SCIM) per connection, separately from AuthKit: $125/connection/month for the first 1-15 connections, declining with volume to $65/connection/month at 51-100 connections (101+ requires a custom quote); Audit Log add-ons (log streaming, event retention) are priced separately at $125/mo and $99/mo respectively. — source: workos.com/pricing; read-at-source: "Enterprise SSO," "Directory Sync," and "Audit Logs" pricing tables.
- **GT-4** Clerk's B2B "Organizations" feature includes 100 monthly-active-organizations free per app, with additional organizations billed at $1/mo each (101-1,000 tier); Clerk's Enterprise SSO add-on includes 1 free connection per app, then $75/mo/connection for connections 2-15 with volume discounts beyond that. — source: clerk.com/pricing; read-at-source: "B2B Organizations" and "Enterprise SSO Add-on" pricing sections.
- **GT-5** The company has a 7-person engineering team, approximately $40,000 monthly recurring revenue, approximately 120 paying tenants, no enterprise customers yet, and its product currently runs behind a single password shared across all tenants plus a Stripe customer portal link, with no per-user or per-tenant authentication in production. — source: this conversation's problem statement; read-at-source: the prompt's stated "Context."
- **GT-6?** IBM's Cost of a Data Breach Report 2025 found the global average cost of a data breach was $4.44 million, and breaches whose initial access vector was compromised credentials averaged approximately $4.67 million and took approximately 292 days to identify and contain. — cited to: IBM Cost of a Data Breach Report 2025; reported-by-delegate: WebSearch aggregation of secondary summaries (bakerdonelson.com, enzoic.com) — cited source not opened by this analysis.
- **GT-7?** AICPA SOC 2 Trust Services Criteria CC6.1 requires logical access controls covering identification, authentication, authorization, and access-impact segmentation; in practice, auditors expect MFA for privileged access and treat centralized identity management, consistent authentication enforcement, and authentication-event logging as standard evidence, with SSO/MFA/SCIM being the typical mechanism B2B SaaS teams use to produce it. — cited to: AICPA Trust Services Criteria, CC6.1; reported-by-delegate: WebSearch aggregation of secondary summaries (ssojet.com, akku.work, sprinto.com) — cited source not opened by this analysis.
- **GT-8?** WorkOS supports SAML and OIDC for Enterprise SSO with more than 60 pre-built IdP integrations; Clerk supports SAML, OIDC, and EASIE with direct integrations for three IdPs; both are independently characterized by a third-party comparison source as "Moderate" migration/exit effort. — cited to: guptadeepak.com CIAM Compass comparison; reported-by-delegate: WebSearch aggregation — cited source not opened by this analysis.
- **GT-9?** The billed release's "audit log" requirement refers to a general business/domain event log (e.g., a tenant admin changing a billing seat, a user exporting customer data), not solely an authentication-event log (logins, MFA challenges, password changes). — unverified: the actual feature ticket/spec for this release was not provided in this analysis; inferred from typical B2B SaaS and SOC2 usage of the term "audit log" as a broader control category than authentication events alone.

**Provenance summary:** `?`-marked: GT-6, GT-7, GT-8, GT-9 (4 of 9). Read-at-source: GT-1 (top10.owasp.org/2021/A07_2021-Identification_and_Authentication_Failures, category description and CWE list quoted verbatim), GT-2 (workos.com/pricing, "AuthKit" table), GT-3 (workos.com/pricing, "Enterprise SSO"/"Directory Sync"/"Audit Logs" tables), GT-4 (clerk.com/pricing, "B2B Organizations"/"Enterprise SSO Add-on" sections), GT-5 (this conversation's stipulated Context).

## 4. Derivation Chains

### Trade-off analysis (supporting Conclusion C5)

**Options named**, including the composite and the status quo: (A) Build-only — OSS library, all four capabilities in-house; (B) Buy-only — managed IdP for all four, including treating its auth-event log as the audit-log requirement; (C) Hybrid (composite) — managed IdP for sessions/password-reset/MFA, domain audit log built in-house; (D) Status quo — shared password + Stripe link.

**Must-have knockout:** MH-1: delivers authenticated, per-tenant accounts (the release's own baseline requirement). Status quo (D) fails MH-1 outright — per chain C1 below, a shared secret with no per-identity boundary is not authentication — and is knocked out before scoring.

**Criteria and locked weights** (1-5, set before any option was scored): time-to-ship ×5; security risk given the team's current maturity ×5; cost at current scale ($40K MRR) ×2; future enterprise-readiness (SSO/SCIM path) ×4; vendor lock-in/reversibility ×3; domain-audit-log fit ×3. Total weight = 22.

**Anchored scale** (1 = worst, 5 = best; higher always better): time-to-ship — 1 = >6 engineer-weeks to a secure v1, 5 = <1.5 engineer-weeks; security risk — 1 = team hand-builds MFA/password-reset under deadline pressure with no external audit, 5 = commodity flows inherited from a SOC2-audited vendor; cost — 1 = >$500/mo at 120 tenants, 5 = <$50/mo; future readiness — 1 = SSO/SCIM requires building a SAML/OIDC IdP from scratch, 5 = SSO/SCIM is a per-connection purchase; lock-in — 1 = fully proprietary, no standard-protocol path, 5 = OIDC-standard, adapter-portable; audit-log fit — 1 = business/domain events not captured, 5 = a purpose-built domain event log.

| Criterion (weight) | Build-only | Buy-only | Hybrid |
|---|---|---|---|
| Time-to-ship (5) | 1 | 5 | 4 |
| Security risk (5) | 1 | 5 | 5 |
| Cost at current scale (2) | 5 | 5 | 5 |
| Future enterprise-readiness (4) | 1 | 5 | 5 |
| Vendor lock-in (3) | 4 | 2 | 3 |
| Domain-audit-log fit (3) | 4 | 1 | 5 |
| **Weighted total** | **48** | **89** | **99** |

**Flip test:** the smallest single-criterion weight change that reverses Hybrid (99) over Buy-only (89) — a 10-point gap — is reducing the domain-audit-log-fit weight from 3 toward 0, since that criterion alone contributes +12 of Hybrid's margin. No other single-criterion move closes the gap with a smaller change (increasing time-to-ship's weight, the only criterion favoring Buy-only, would require moving it from 5 to 15). This analysis judges a weight of ~0 on domain-audit-log fit indefensible, since the release's own stated requirement names an audit log explicitly (see `GT-9?`).

### Estimate (Fermi): build-path vs. buy-path engineering time

Target quantity: engineer-weeks of one-time work to ship a secure v1 covering sessions, password reset, MFA, and audit log, including migrating 120 existing tenants off the shared-password scheme.

| Component | Build-path (days) | Buy-path (days) | Shared across both paths? |
|---|---|---|---|
| Login/session integration | 2-4 | 1-2 | No |
| Tenant-data model + migrate 120 tenants | 3-6 | 3-6 | Yes |
| Password reset (secure, correct) | 2-3 | 0.5-1 | No |
| MFA (enrollment + recovery flow) | 5-8 | 1-2 | No |
| Domain/business audit log | 3-5 | 3-5 | Yes |
| Security hardening (rate limiting, session fixation, CVE review) | 3-5 | 1-2 | No |

Central-value sums: build-path total = 3+4.5+2.5+6.5+4+4 = 24.5 days ≈ 4.9 weeks; buy-path total = 1.5+4.5+0.75+1.5+4+1.5 = 13.75 days ≈ 2.75 weeks. Isolating the auth-specific components (excluding the two shared components, tenant-data migration and domain audit log, which both paths must build regardless): build-path auth-specific ≈ 16 days ≈ 3.2 weeks (bracket 2.1-4.9 weeks); buy-path auth-specific ≈ 5.25 days ≈ 1.1 weeks (bracket 0.7-1.8 weeks). A 1.5× friction multiplier applied to the pessimistic build-path bracket (interrupt-driven team, not one dedicated uninterrupted engineer) gives an upper bound of ≈9.3 weeks. Both the optimistic and pessimistic ends of the bracket agree on direction: buying is faster on the auth-specific, timeline-critical slice of the work, so the estimate is decision-resolving without further tightening (see chain C2).

### Conclusion C1: The status quo cannot be preserved; the do-nothing option is knocked out

GT-5 (current shared-password + Stripe-link scheme, no per-identity separation) + GT-1 (OWASP A07 failure catalog)
→ a single password shared across all tenants provides no mechanism to distinguish one tenant's user from another, which is a more severe gap than any single weakness OWASP A07 catalogs, since those weaknesses all presuppose some per-identity boundary already exists to attack
→ replacing this scheme with any properly-implemented per-tenant authentication system is a strict security improvement over the status quo on the identification dimension alone, independent of which build-or-buy path delivers it
→ the status quo therefore fails the release's own baseline requirement and cannot be preserved, which knocks the do-nothing option out of consideration before any build-vs-buy scoring begins

**Pre-check:** head GT-5, GT-1 · ?-marked: none · lowest cited: none · Inputs ceiling: HIGH
**Confidence:** HIGH — both head inputs are read-at-source, the inference is direct deduction, and the only candidate rival (that the Stripe customer link already provides adequate identification) is ruled out by GT-1's definition of identification and GT-5's stipulated fact that no per-user separation exists today.

### Conclusion C2: Buying the commodity auth capability saves roughly two engineer-weeks over building it

GT-5 (7-person team, urgent timeline)
→ decomposing the four required capabilities into components that differ by build-vs-buy path (login/session, password-reset, MFA, security-hardening) and components required under either path (tenant-data migration, domain audit log) isolates the auth-specific engineering delta from the release's shared baseline cost [Assumes: A-9 — the per-component day estimates are informed engineering judgment, not measured data from this team's own velocity]
→ a first-principles unit-factor buildup of the auth-specific build-path components yields a central estimate of about 3.2 engineer-weeks, bracketed between roughly 2.1 and 4.9 weeks
→ the equivalent auth-specific buy-path components, most of which are inherited configuration rather than implementation, yield a central estimate of about 1.1 engineer-weeks, bracketed between roughly 0.7 and 1.8 weeks
→ buying the commodity auth capability rather than building it returns roughly two engineer-weeks of a seven-person team's capacity back to the timeline-critical release, and both ends of the two brackets agree on this direction, so the estimate is decision-resolving without needing further tightening

**Pre-check:** head GT-5 · ?-marked: none · lowest cited: none · Inputs ceiling: HIGH
**Confidence:** MEDIUM — `[Assumes: A-9]` is unpriced beyond the stated bracket: the per-component day estimates are informed judgment rather than measured data from this team's own historical velocity. Verification that would remove this as a cause of the downgrade: track actual engineering hours against this bracket once work begins, or benchmark against a comparable past sprint if one exists.

### Conclusion C3: The buy path's cost is near-zero at current scale and decoupled from current revenue

GT-2 (WorkOS AuthKit free to 1M MAU) + GT-3 (WorkOS SSO/SCIM per-connection pricing) + GT-4 (Clerk org + SSO pricing)
→ WorkOS's AuthKit costs $0/month at 120 tenants because its free tier is denominated in monthly active users up to 1,000,000 and 120 tenants' total end-user count is far below that threshold
→ Clerk's free tier is denominated in monthly active organizations rather than users, so at 120 tenants Clerk's core auth costs approximately $20/month, 20 organizations above the 100-organization free threshold at $1 each, still under one-twentieth of one percent of the company's $40,000 monthly recurring revenue
→ SSO and Directory Sync (SCIM), the enterprise-specific capabilities, are billed per connection under both vendors rather than per tenant or per user, so their cost only appears once a specific enterprise customer actually requests SSO
→ the buy path's cost is therefore decoupled from the company's current early-stage revenue and instead scales with exactly the future enterprise-revenue event that would justify the expense

**Pre-check:** head GT-2, GT-3, GT-4 · ?-marked: none · lowest cited: none · Inputs ceiling: HIGH
**Confidence:** HIGH — all three head inputs are read-at-source, the arithmetic recomputes independently (see the Adversarial pass record), and the only candidate rival (unenumerated per-seat fees beyond the read fee schedules) is speculative and unsupported by GT-2/GT-3/GT-4's actual terms.

### Conclusion C4: A managed IdP converts the future SSO/SCIM problem into a purchase rather than a project

GT-7? (SOC2 CC6.1 SSO/MFA/SCIM as baseline evidence) + GT-1 (OWASP A07 failure catalog)
→ SOC2-track enterprise buyers typically require SSO and SCIM as baseline vendor-security evidence, so a B2B SaaS company with no enterprise customers today should still expect SSO and SCIM requests once enterprise sales begin [Assumes: A-5 — enterprise prospects will follow this industry-standard pattern; if a given prospect does not require it, this chain's urgency is overstated for that deal, but chain C3 establishes the buy path's per-connection pricing means no cost was incurred on the wrong bet either way]
→ implementing SAML/OIDC SSO correctly from scratch later requires navigating the same class of identification-and-authentication failure modes cataloged in OWASP A07, but for a substantially more complex federated-trust protocol than basic session, password-reset, and MFA flows
→ a managed IdP that already offers per-connection SSO and SCIM as a configurable add-on converts this later, harder problem into a purchasing decision rather than a new engineering project, provided today's integration keeps the vendor's user and session identifiers behind an internal adapter layer rather than coupling application logic directly to vendor-proprietary objects [Assumes: A-6 — adapter-layer discipline is maintained at implementation time; if it is not, the migration path degrades from moderate to significant effort, a risk this analysis prices via A-6 rather than treating as resolved]

**Pre-check:** head GT-7?, GT-1 · ?-marked: GT-7? · lowest cited: none · Inputs ceiling: MEDIUM
**Confidence:** MEDIUM — `GT-7?` is reported-by-delegate (secondary summaries of SOC 2 CC6.1, not the primary AICPA document). Verification that would remove this as a cause of the downgrade: open the primary AICPA Trust Services Criteria document, or obtain a completed SOC 2 audit report from a comparable peer company, to confirm SSO/MFA/SCIM are treated as baseline evidence rather than optional.

### Conclusion C5: Recommend the hybrid split — buy commodity auth now, build the domain audit log in-house

C1 (status quo knocked out, HIGH) + C2 (build-vs-buy time delta, MEDIUM) + C3 (near-zero cost at current scale, HIGH) + C4 (future SSO complexity, MEDIUM) + GT-1 (OWASP A07 failure catalog) + GT-8? (WorkOS/Clerk protocol support, "moderate" lock-in) + GT-9? (audit log means domain events, not just auth events)
→ applying six locked criteria weights (time-to-ship ×5, security-risk-given-team-maturity ×5, current-stage cost ×2, future-enterprise-readiness ×4, vendor-lock-in ×3, domain-audit-log-fit ×3) to the three surviving options yields weighted totals of Hybrid 99, Buy-only 89, and Build-only 48
→ the flip test on these totals shows exactly one single-criterion weight change reverses the ordering: reducing the domain-audit-log-fit weight from 3 to effectively 0, which would mean treating the release's own stated audit-log requirement as worthless, a change this analysis finds indefensible given that requirement's explicit presence in the prompt
→ recommend the hybrid option: adopt a managed identity provider now for sessions, password reset, and MFA, buying back both the OWASP A07 commodity-auth risk and the multi-week build-time delta, while building the domain and business-level audit log in-house on the product's existing stack
→[2nd] engineers' auth-specific work shifts from building and maintaining commodity flows to SDK integration and vendor-API literacy, freeing roughly the two engineer-weeks identified in C2 toward the domain audit log and the rest of the release in the same cycle
→[2nd] the release introduces a public per-user login endpoint that did not exist under the shared-password scheme, a new attack surface that the managed-IdP path defends by default through vendor-side rate limiting and anomaly detection, but which the go-live checklist must still explicitly verify is switched on rather than assumed
→[3rd] once enterprise prospects begin requesting SSO, per-connection pricing becomes a real, budgetable line item that sales must price into deal economics before promising SSO, rather than a surprise discovered after a deal closes
→[3rd] if the adapter-layer discipline named in C4 is not maintained, coupling between application logic and the vendor's session schema accumulates over twelve to twenty-four months, raising future migration cost from moderate to significant, a risk already priced into this recommendation via `[Assumes: A-6]` rather than newly discovered here

**Pre-check:** head C1 (HIGH), C2 (MEDIUM), C3 (HIGH), C4 (MEDIUM), GT-8?, GT-9? · ?-marked: GT-8?, GT-9? · lowest cited: MEDIUM · Inputs ceiling: MEDIUM
**Confidence:** MEDIUM — capped by two unverified inputs cited directly: `GT-8?` (WorkOS/Clerk protocol-support and lock-in characterization, reported-by-delegate; verification: fetch WorkOS's and Clerk's own SSO/OIDC documentation directly) and `GT-9?` (whether "audit log" means domain events, unverified against the actual feature spec; verification: read the release's feature ticket or ask the product owner directly). This chain also cites C2 and C4, both independently MEDIUM (see their own confidence lines above), which does not lower C5 further but is named here per D-07.

Second-order effects were checked against the decision's own success criteria (Phase 4 step 6): the "new attack surface" effect above partially tensions the release's implicit "ship safely" goal unless rate limiting and anomaly detection are explicitly confirmed enabled, which is why that verification is carried forward as a named go/no-go gate in the Adversarial pass record (Cluster 2) rather than left implicit. No second-order effect contradicts a named ground truth, so no return to Phase 2 was triggered.

## 5. Abandoned Reasoning

### Dead End: Auth0 as the buy-path vendor

**What was tried:** Considered Auth0 alongside WorkOS and Clerk as a candidate managed identity provider, based on preliminary secondary-source pricing research (B2B Essentials plan reported around $150/month base, MAU overage reported around $0.07/MAU).

**Why abandoned:** The pricing data available for Auth0 in this analysis was reported-by-delegate (secondary aggregator summaries) rather than read at Auth0's own pricing page, unlike GT-2/GT-3 (WorkOS) and GT-4 (Clerk), which were fetched and read directly. Rather than build a chain on an unverified cost comparison, Auth0 was set aside pending direct verification.

**What it ruled out:** A three-way vendor bake-off inside this analysis, which would have added another `?`-marked ground truth to an already-MEDIUM chain (C5) without changing the structural recommendation. Auth0 remains a legitimate candidate to re-evaluate once its pricing page is read directly.

### Dead End: Self-hosted open-source identity server (e.g., Keycloak) as the "build" option

**What was tried:** Considered whether self-hosting a mature, full-featured open-source identity server, rather than a lighter authentication library, would capture the security maturity of a managed provider while avoiding vendor cost.

**Why abandoned:** This still requires the team to operate, patch, and scale a production identity service — GT-5's team-size constraint applies equally — and does not reduce the auth-specific engineering-time delta computed in C2, since the multi-tenant data-modeling and framework-integration work is the same regardless of the underlying library's scope. It does not capture C3's near-zero current-scale cost or C4's per-connection future-SSO simplicity.

**What it ruled out:** Treating "self-hosted OSS identity server" as a fourth, middle-ground option in chain C5's trade-off matrix; on the scored axes it lands closer to Build-only than to Hybrid or Buy-only and was not carried forward as a separately scored option.

### Dead End: Treating the vendor's authentication-event log as satisfying the "audit log" requirement (pure Buy-only)

**What was tried:** Considered recommending Buy-only outright — adopting a managed IdP for all four named capabilities, including audit log, with no in-house build component.

**Why abandoned:** A managed identity provider's audit trail covers authentication events (logins, MFA challenges, password changes), not domain or business events (e.g., a tenant admin changing a billing seat or exporting customer data). Under `GT-9?`, this is very likely a different thing than what a B2B SaaS release calling for "an audit log" is expected to deliver, so Buy-only risks shipping a release that appears to satisfy the requirement without actually doing so.

**What it ruled out:** Buy-only as the recommended option in chain C5's trade-off matrix (weighted total 89 versus Hybrid's 99). Buy-only remains the analysis's named fallback if `GT-9?` is confirmed false (see chain C5's confidence line and Section 6's Trade-offs acknowledged).

### Dead End: A lightweight, non-authenticated per-tenant identification scheme as a faster substitute for full authentication

**What was tried:** Considered whether a minimal per-tenant token or link, extending the existing Stripe-customer-link pattern, could satisfy the release's need for "per-tenant accounts" without building full login/session/password/MFA machinery, as a faster path than either build or buy.

**Why abandoned:** Chain C1 establishes that the release's own stated requirement is authenticated, per-tenant accounts, and that the current link-based scheme is already the most severe available instance of OWASP A07's identification failure. A lighter-weight token scheme would still fail to distinguish individual users within a tenant and would not resolve the credential-stuffing, session-exposure, and recovery-flow risks GT-1 catalogs.

**What it ruled out:** Any option that treats "per-tenant" identification as sufficient without also addressing per-user authentication; this dead end confirms the must-have knockout applied before chain C5's scoring is doing real work rather than being a formality.

## 6. Conclusion

**Recommended approach:** Adopt a managed identity provider (WorkOS or Clerk — both viable at current scale per chain C3, with Auth0 set aside pending direct pricing verification per Section 5) now for sessions, password reset, and MFA, migrating the 120 existing tenants off the shared-password scheme as part of the same release; build the domain/business-level audit log in-house on the product's existing stack rather than relying on the vendor's authentication-event log to satisfy that requirement (chain C5). This can meet the CTO's urgency framing on the auth-specific critical path (chain C2's ~1.1-week buy-path estimate vs. ~3.2-week build-path estimate), provided the tenant-data migration itself — required under either path — is scoped and audited before the release date is finalized (Adversarial pass, Cluster 1).

**Key insight:** The four capabilities named in the "build vs buy" framing are not homogeneous. Sessions, password reset, and MFA are commodity, security-critical infrastructure that a managed identity provider already builds, operates, and gets independently audited, at a cost that is near-zero at this company's current scale and stays proportional to future enterprise revenue rather than current tenant count (chain C3). "Audit log," by contrast, is very likely a domain/business-event requirement that the vendor's own authentication log does not satisfy (`GT-9?`), so splitting the decision — buying the commodity security surface, building the product-specific one — outperforms treating the four requirements as a single build-or-buy unit (chain C5). A pure build-vs-buy framing, applied uniformly across all four capabilities, would have missed this split entirely.

**Trade-offs acknowledged:** This recommendation accepts an ongoing per-connection vendor cost once enterprise SSO/SCIM requests begin, priced as contingent rather than upfront (chain C4); a vendor migration-effort dependency characterized as "moderate," which holds only if adapter-layer discipline is maintained through implementation (chain C5, `[Assumes: A-6]`); and a residual dependency on `GT-9?`, the unverified assumption that the release's "audit log" requirement means domain business events rather than authentication events — if `GT-9?` is confirmed false, the domain-audit-log build should be dropped in favor of the simpler Buy-only option (chain C5).

**Pre-check:** head C5 (MEDIUM) · ?-marked: none · lowest cited: MEDIUM · Inputs ceiling: MEDIUM
**Confidence:** MEDIUM — the recommendation rests entirely on chain C5, itself capped at MEDIUM by two unverified inputs it cites directly: `GT-8?` (WorkOS/Clerk protocol-support and lock-in characterization, reported-by-delegate from secondary comparison sources rather than the vendors' own documentation — verification: fetch WorkOS's and Clerk's own SSO/OIDC documentation directly) and `GT-9?` (whether "audit log" means domain events, unverified against the actual feature spec — verification: read the release's feature ticket or ask the product owner directly). Chain C5 also cites C2 and C4, both independently MEDIUM (see their own confidence lines in Section 4), which does not lower C5 further but is named here per D-07.

**Conditions under which this recommendation flips:**
1. If `GT-9?` is confirmed false — i.e., the release's "audit log" requirement is satisfied by the vendor's own authentication-event log — flip to Buy-only, dropping the in-house domain-audit-log build (chain C5).
2. If a pre-migration tenant-data audit shows the tenant-migration component is far larger than the 3-6 day bracket used in the Fermi estimate, reconsider the release timeline itself rather than the build-vs-buy choice, since that component is required under either path (chain C2).
3. If the team gains a dedicated security engineer or security-focused hire (making `A-2` false), re-examine the security-risk criterion's weight in the trade-off matrix, currently the largest single driver of Buy-only's and Hybrid's advantage over Build-only (chain C5).
4. If Auth0's own pricing, read directly, is materially cheaper than WorkOS's or Clerk's at the scale this company expects to reach in 12-24 months, reconsider the specific vendor choice without changing the hybrid structure itself (chain C5).
