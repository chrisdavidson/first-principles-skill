## Techniques not applied (process output)

- fishbone — not applicable — the assumption space was adequately enumerated via the inversion procedure's structured failure-precondition analysis (11 preconditions across both paths); no additional category brainstorm was needed to surface further untested beliefs.
- inversion (Phase 5 invocation) — not applicable — the headline conclusion is a plan/recommendation, not a bare claim, so the decision rule routes Phase 5's adversarial technique to pre-mortem instead (inversion was already applied at Phase 2 to challenge both paths' assumptions).
- theoretical-limit (Phase 1 invocation) — not applicable — the essence question (which implementation path minimizes combined schedule and security risk for a small team) was already the real question, not a conventional proxy masking a physical-law question, so no Phase 1 reframe was needed (theoretical-limit was applied at Phase 4 instead, chain C1).

## Assumption Audit scan (process output)

| Chain | Step | Step Text (brief) | Assumption surfaced? | Added to Table? |
|-------|------|--------------------|------------------------|------------------|
| C1 | 1 | continuous maintenance attention required for security-critical subsystems | none | n/a |
| C1 | 2 | ideal floor near zero only if vendor-operated | none | n/a |
| C1 | 3 | conventional figure near zero for a 7-person team | none (rests on GT-6?, already in table) | n/a |
| C1 | 4 | build locks the gap onto the company | none | n/a |
| C1 | 5 | buy transfers most of the gap to the vendor | A-VENDORVIABILITY (vendor remains a going concern) | yes |
| C2 | 1 | decomposition into 8 auth subsystems | none | n/a |
| C2 | 2 | sum to 16wk central, bracket 10-26 | none (rests on rows 6-11, already in table) | n/a |
| C2 | 3 | apply loaded-cost rate to get one-time $ cost | A-RATE ($3,000-4,000/engineer-week loaded cost) | yes |
| C2 | 4 | 16wk central exceeds a plausible urgent-release window | A-HIRING (no additional hire/contractor compresses the timeline) | yes |
| C3 | 1 | decomposition into 7 integration units | none | n/a |
| C3 | 2 | sum to 4.4wk central, bracket 3-7 | none | n/a |
| C3 | 3 | total end-users stay under vendor free-tier ceilings | A-USERCOUNT (end-user count across 120 tenants stays under free-tier caps) | yes |
| C3 | 4 | recurring core-auth cost near $0-50/month today | none (follows from step 3) | n/a |
| C4 | 1 | weighted scoring yields totals 43/91/84/77 | A-WEIGHTS (locked criteria weights reflect the CTO's actual priorities) | yes |
| C4 | 2 | WorkOS weakly dominates Clerk | none | n/a |
| C4 | 3 | no single-criterion reweighting flips build to the winner | none | n/a |
| C4 | 4 | recommend buy (WorkOS) + thin in-house tenant/role layer | none | n/a |
| C5 | 1 | actor lens: engineers redirect saved effort to roadmap | none | n/a |
| C5 | 2 | actor lens: tenant admins gain polished hosted UX sooner | none | n/a |
| C5 | 3 | actor lens: new operational dependency on vendor | none (dependency already implied by C1) | n/a |
| C5 | 4 | time lens: release ships in window, cost stays near-zero for several cycles | none | n/a |
| C5 | 5 | time lens: 12-24mo vendor-pricing dependency | none (A-VENDORVIABILITY already added at C1 step 5) | n/a |
| C5 | 6 | no ground truth contradicted, extension stands | none | n/a |
| C6 | 1 | urgency traces to the feature gating the release | none | n/a |
| C6 | 2 | traces further to auth being deferred during PMF-chasing | none | n/a |
| C6 | 3 | counterfactual test: requirement survives absent the billing deadline | none | n/a |
| C6 | 4 | root cause is a reasoning error, not a resourcing one | none | n/a |
| C6 | 5 | decoupling schedule pressure from method choice resolves the tension | none | n/a |

Surfaced and added to the Classified Assumptions Table (section 2, rows 17-21): A-HIRING, A-USERCOUNT, A-WEIGHTS, A-VENDORVIABILITY, A-RATE.

## Adversarial pass (process output)

**Recompute:** Build Fermi sum recomputed independently: 1.5+1+1.5+2.5+2.5+4+1.5+1.5 = 16.0 engineer-weeks central (matches chain C2). Buy Fermi sum recomputed independently: 0.8+0.8+0.8+0.1+0.3+0.8+0.8 = 4.4 engineer-weeks central (matches chain C3). Trade-off weighted totals recomputed independently: Build = 1(5)+1(5)+5(3)+2(4)+5(2) = 5+5+15+8+10 = 43. WorkOS = 5(5)+5(5)+5(3)+5(4)+3(2) = 25+25+15+20+6 = 91. Clerk = 5(5)+5(5)+4(3)+4(4)+3(2) = 25+25+12+16+6 = 84. Auth0 = 4(5)+5(5)+2(3)+5(4)+3(2) = 20+25+6+20+6 = 77. All four totals recompute exactly as stated in chain C4; no arithmetic error found.

**Sensitivity:** The single ground truth whose falsity would most flip the conclusion is GT-6? (the stipulated 7-person / $40K-MRR / no-enterprise-yet snapshot, prior auth = shared password + Stripe link) — it is `?`-marked. If team size or security-review capacity were materially different (e.g., a 40-person org with a dedicated security function), chain C1's theoretical-limit finding and chain C2's schedule finding would both weaken, which could flip chain C4's ranking. This caveat is already carried on every chain citing GT-6? (C1, C6) and propagates to C4/C5/the Conclusion. Weakest link per chain: C1 — GT-6?'s unverifiable stipulation; C2 — the tenant-isolation-retrofit week estimate (3-5wk, the largest and least certain Fermi line item); C3 — A-USERCOUNT (assumed total end-user count stays under free-tier ceilings); C4 — A-WEIGHTS (whether the locked criteria weights match the CTO's actual priorities).

**Rival:** Headline conclusion — strongest rival is "build now, add SSO later only when an enterprise deal needs it" (deferring the vendor decision rather than the build decision); ruled out jointly by chain C1 and chain C2 (Abandoned Reasoning, Dead End 1) since the continuous-maintenance-tax argument and the schedule bracket both apply regardless of when SSO specifically is added. Chain C1 — rival is "a fractional/part-time security specialist closes the maintenance gap without a full dedicated hire"; this softens C1's magnitude but does not reverse its direction, since a fractional specialist still competes with the same 7-person capacity budget — carried live, bounded, on C1's confidence line rather than fully settled. Chain C2/C3 — rival is "a batteries-included OSS framework compresses build time near the buy path's estimate"; ruled out in Abandoned Reasoning, Dead End 6 (framework scaffolding doesn't touch the tenant-isolation retrofit or C1's maintenance-tax finding). Chain C4 — rival is "Auth0 as default vendor"; ruled out as the default in Abandoned Reasoning, Dead End 4, but named as a live, weaker rival conditional on an imminent (weeks-scale) enterprise pipeline, carried on C4's confidence line.

**Premise:** Six months from now, the WorkOS-adoption plan has already failed — the release either slipped anyway, shipped with a security incident, or is now costing far more than budgeted.

**Causes (unfiltered, from three stakeholder viewpoints):**
Engineer viewpoint: (a) integration trusted client-side tokens or skipped server-side verification, reintroducing a session vulnerability despite using a secure vendor; (b) the homegrown tenant/org-mapping authorization layer shipped a cross-tenant query bug because "we bought an IdP" was treated as license to skip reviewing it; (c) no one owned SDK/dependency version bumps and the integration went stale, breaking silently during a later feature push.
Tenant-admin/customer viewpoint: (d) a customer's IT security policy blocked the vendor's auth domain or redirect flow with no fallback, delaying that customer's onboarding; (e) default MFA enrollment UX confused non-technical tenant admins, generating support burden and early churn.
CFO/business viewpoint: (f) the vendor restructured its pricing (as GT-2/GT-3/GT-4 already show happened industry-wide between 2024 and 2026) and a cost line spiked unbudgeted as tenant count grew; (g) a prospective customer's security/procurement questionnaire flagged the vendor relationship as a compliance gap because nobody had read the DPA/compliance terms before proposing the vendor, blocking a deal despite having "SSO."

**Clusters:**
- Cluster 1, "Authorization-layer complacency" (bears on: GT-1, C1, C4) — cause (b): the belief that buying auth removes the need for careful engineering is false for the app-side tenant/role-mapping layer, exactly where GT-1's documented risk class still lives.
  Disposition: plan change — scope an explicit code review / lightweight security checklist specifically for the tenant/org-scoping authorization code, treated as the single highest remaining risk item; "we bought an IdP" does not substitute for reviewing it.
- Cluster 2, "Unowned vendor dependency" (bears on: C1, C5) — causes (a), (c): no named internal owner for the vendor SDK's integration correctness and version currency.
  Disposition: plan change — assign named, even fractional (~10%), ownership of the vendor relationship and SDK-version currency to one engineer, reviewed quarterly.
- Cluster 3, "Pricing and compliance surprise" (bears on: C3, C4, GT-2, GT-3, GT-4) — causes (f), (g): vendor repricing and unread compliance terms can each convert a "solved" capability gap back into a blocker.
  Disposition: accepted risk with named mitigation — accept that vendor pricing may shift (already disclosed by GT-2/GT-3/GT-4's own sourced note that pricing was restructured industry-wide 2024-2026); mitigate by having chosen WorkOS specifically because its enterprise-connection pricing is tied directly to revenue-generating deals, and by reading the vendor's DPA/compliance documentation before, not after, the first enterprise contract is proposed.
- Cluster 4, "Onboarding friction" (bears on: none of the core chains directly — a narrower product/support-scale finding) — causes (d), (e): IT-policy blocks and confusing MFA UX are real but narrower risks than the security/cost clusters above.
  Disposition: accepted risk with named mitigation — accept as a normal SaaS-onboarding risk; mitigate with a documented fallback contact path for blocked customers and a lightly customized (not default) MFA enrollment flow before the first enterprise-scale customer onboards.

**Falsification:** This conclusion is false if a 7-person team can, in fact, ship a fully correct, security-reviewed, tenant-isolated in-house auth system within the release's actual timeline without a dedicated security reviewer, and do so at materially lower total cost of ownership than the vendor path over a 2-year horizon — i.e., if chain C2's lower bound (10 weeks) is wrong by 2-4x on the low side, or if the team in fact has security-review capacity this analysis was not told about, the recommendation to buy is unsupported.

## §6→§4 closure ledger (process output)

- "Adopt a managed identity provider now — WorkOS AuthKit as the default choice... build only the thin, product-specific tenant/org data model and role-to-feature permission mapping in-house... ship on the buy path's 3-7 week integration bracket rather than the build path's 10-26 week bracket" → chain C4 ✓
- "A 7-person team's binding constraint is not engineering skill but the structural inability to durably service the non-zero continuous security-maintenance tax... buying doesn't just save weeks, it transfers that permanent tax to a vendor" → chain C1 ✓
- "This recommendation accepts a new commercial and operational dependency on WorkOS's pricing and uptime... it defers Auth0's deeper enterprise-compliance tooling... it still requires disciplined engineering on the tenant/role-mapping layer" → chain C5, chain C4 ✓
- "Whether switching vendors or reverting to a self-built system later would be cheap or costly remains untested" → no chain — flagged assumption only (marker present, scored untraced by design)
- "**Confidence:** MEDIUM — every contributing chain is MEDIUM" → chain C1, chain C2, chain C3, chain C4, chain C5, chain C6 ✓
- "If an enterprise pipeline with imminent (weeks-scale) SAML/SSO demand appears, re-run chain C4 with Enterprise-readiness weighted higher" → chain C4 ✓
- "If MRR or tenant count grows enough to approach vendor free-tier ceilings, re-verify actual total end-user count" → chain C3 ✓
- "If engineering headcount grows to include a dedicated security/platform function, chain C1's theoretical-limit finding weakens and the build path becomes reconsiderable" → chain C1 ✓

All surviving §6 claims carry a chain reference (inline) or the honest untraced marker. No claim was cut.

## Self-audit scan (process output)

| Chain | Chain Head (brief) | Form conforming? | Rule applied | Dependency clean? | Band | Act attempted? | Edges fired |
|-------|---------------------|-------------------|---------------|--------------------|------|-----------------|-------------|
| C1 | GT-1 + GT-6? | yes | n/a | yes | MEDIUM | yes | none |
| C2 | GT-1 + C1 | yes | n/a | yes | MEDIUM | yes | none |
| C3 | GT-2 + GT-3 + GT-4 | yes | n/a | yes | MEDIUM | yes | none |
| C4 | C1 + C2 + C3 | yes | n/a | yes | MEDIUM | yes | none |
| C5 | C4 | yes | n/a | yes | MEDIUM | no | none |
| C6 | GT-6? | yes | n/a | yes | MEDIUM | yes | none |

| §6 Span (brief) | Construct | Claim under R11? | R11 clause applied | Chain cited |
|-------------------|-----------|-------------------|----------------------|---------------|
| Recommended approach (WorkOS + thin in-house layer) | bold lead-in | yes | colon closes bold span, same-line assertion | C4 |
| Key insight (continuous-maintenance tax) | bold lead-in | yes | colon closes bold span, same-line assertion | C1 |
| Trade-offs acknowledged (main sentence) | bold lead-in | yes | colon closes bold span, same-line assertion | C5, C4 |
| Trade-offs — switching-cost caveat | prose (caveat) | yes | caveat carrying `no chain — flagged assumption only` marker | none — untraced (marked) |
| Pre-check line | prose | no | pre-check line, not itself an R11 lead-in/list construct | n/a |
| Confidence | bold lead-in | yes | colon closes bold span, same-line assertion | C1, C2, C3, C4, C5, C6 |
| Trigger: enterprise pipeline appears | list item | yes | closes own sentence, >40 chars | C4 |
| Trigger: MRR/tenant growth nears free-tier ceilings | list item | yes | closes own sentence, >40 chars | C3 |
| Trigger: headcount grows to include security function | list item | yes | closes own sentence, >40 chars | C1 |

Scan complete: 6 chain rows, one per section-4 chain block in order; 9 section-6 rows, one per construct in order — 8 claims under R11, 1 excluded. 0 chains malformed, 0 claims untraced (1 claim carries the honest `no chain — flagged assumption only` marker, which is not the same as untraced-and-unmarked).

---

## 1. Problem Essence

**Core problem:** Given a seven-person engineering team with no dedicated security function that must ship its first real per-tenant, multi-user, role-bounded authentication system under a fixed release deadline, which implementation path — building the security-critical subsystems (sessions, credential storage, password reset, MFA, audit log, tenant isolation) in-house versus adopting a managed identity provider — minimizes the combination of security-failure risk and schedule risk to the committed release, without foreclosing near-term enterprise SSO/SAML requirements? Before scoring build-vs-buy as an either/or choice, this analysis also tests whether a split — buying the generic, security-critical primitives while building only the thin, product-specific tenant/role layer — outperforms either pure option, since nothing in the problem requires the same team to either write or not write every layer of the system.

**Success criteria:**
1. A single recommendation (build / buy / phased-hybrid) is stated that is usable directly as decision input.
2. The recommendation is checked against the release-timeline constraint — does it plausibly ship inside the CTO's implied urgent window.
3. The recommendation is checked against the documented auth failure-mode classes (OWASP A07) given the team's stated size and lack of a dedicated security function.
4. The recommendation explicitly states whether it forecloses or preserves a path to enterprise SSO/SAML.
5. The recommendation names concrete trigger conditions (team size, MRR/tenant growth, enterprise pipeline) under which it should be revisited.

---

## 2. Assumptions Table

| Assumption | Type | Treatment | Verdict | Verification |
|------------|------|-----------|---------|---------------|
| 1. Building auth in-house is cheap/fast because it's "just a login form" | convention | Explicitly challenged before use | Discard — refuted by GT-7 (auth decomposes into 8 largely-independent subsystems) and chain C2 (10-26 engineer-week bracket) | GT-7, chain C2 |
| 2. Adopting a managed IdP is automatically safer than building | untested belief | Verify or flag unverified | Challenge — partially upheld: GT-1's failure classes are substantially mitigated in the *outsourced* subsystems, but the app-side tenant/role-mapping layer the buyer still writes carries the same risk class | unverified — flagged; see pre-mortem Cluster 1 |
| 3. Urgency justifies cutting corners on the security-sensitive build/buy decision | convention | Explicitly challenged before use | Discard — refuted by chain C6 (5-whys root cause: urgency is genuine schedule pressure, not license to skip review) | chain C6 |
| 4. They will need enterprise SSO/SAML soon | current constraint | Record expiry conditions | Accept — expires as a driver of the Enterprise-readiness criterion weight if no enterprise pipeline exists 12+ months from now; stated as a requester-supplied planning input | unverified — flagged (requester-stated, not independently confirmed) |
| 5. Switching build method or vendor later is easy/hard (incl. credential/hash portability) | untested belief | Verify or flag unverified | Challenge — moderate friction expected (a one-time password-reset migration flow), not load-bearing for the headline recommendation | unverified — flagged; see §5 |
| 6. No dedicated security engineer/review process exists on the 7-person team | untested belief | Verify or flag unverified | Accept as true per GT-6? stipulation | unverified — flagged |
| 7. [Build] Chosen OSS auth library/pattern accumulates unpatched CVEs post-launch without a named owner | untested belief | Verify or flag unverified | Challenge — unverified, load-bearing on chain C1 | unverified — flagged |
| 8. [Build] Tenant-isolation retrofit onto a codebase with zero existing tenant boundary misses at least one query path (broken object-level authorization) | untested belief | Verify or flag unverified | Challenge — unverified, load-bearing on chains C1 and C2 (largest Fermi line item) | unverified — flagged |
| 9. [Build] MFA/password-reset edge cases go untested under deadline pressure (token replay, timing attack, account enumeration) | untested belief | Verify or flag unverified | Challenge — unverified, load-bearing on chain C1 | unverified — flagged |
| 10. [Build] Audit log added without tamper-evidence, failing its purpose during incident response | untested belief | Verify or flag unverified | Challenge — unverified, load-bearing on chain C1 | unverified — flagged |
| 11. [Build] Team has no prior experience implementing MFA + sessions + tenant isolation together, so unknown-unknowns dominate schedule | untested belief | Verify or flag unverified | Accept as plausible per GT-6? (no per-tenant auth exists in the product today) — load-bearing on chain C2's bracket width | unverified — flagged |
| 12. [Buy] Vendor outage or vendor-side breach with no fallback | untested belief | Verify or flag unverified | Challenge — unverified, not load-bearing for the headline (accepted risk, see pre-mortem Cluster 3/4) | unverified — flagged |
| 13. [Buy] Careless integration (unverified client-side tokens, unchecked webhook signatures, misconfigured redirects) reintroduces vulnerabilities despite a secure vendor | untested belief | Verify or flag unverified | Challenge — unverified, load-bearing (pre-mortem Cluster 1) | unverified — flagged |
| 14. [Buy] Vendor pricing model changes unfavorably as the company grows | untested belief | Verify or flag unverified | Accept as a real, documented risk per GT-2/GT-3/GT-4's own "restructured pricing 2024-2026" finding | GT-2, GT-3, GT-4; flagged |
| 15. [Buy] Vendor's data-residency/compliance posture blocks a future enterprise deal despite technical SSO support | untested belief | Verify or flag unverified | Challenge — unverified, load-bearing (pre-mortem Cluster 3) | unverified — flagged |
| 16. [Buy] Migrating away from a vendor later requires re-hashing/exporting credential data that may not be cleanly portable | untested belief | Verify or flag unverified | Challenge — unverified (cross-references row 5) | unverified — flagged |
| 17. [A-HIRING] No additional engineer/contractor can be brought in to compress the build timeline | untested belief | Verify or flag unverified | Challenge — unverified, load-bearing on chain C2 | unverified — flagged |
| 18. [A-USERCOUNT] Total end-users across 120 tenants stay well under vendor free-tier MAU/MRU ceilings | untested belief | Verify or flag unverified | Challenge — unverified, load-bearing on chain C3 | unverified — flagged |
| 19. [A-WEIGHTS] The trade-off procedure's locked criteria weights (time and security prioritized over pure cost) reflect the CTO's actual priorities | untested belief | Verify or flag unverified | Challenge — unverified, load-bearing on chain C4; CTO should sanity-check before treating C4 as final | unverified — flagged |
| 20. [A-VENDORVIABILITY] Auth0/Clerk/WorkOS remain viable, ongoing businesses over the relevant planning horizon | untested belief | Verify or flag unverified | Accept as low-risk given all three are established, funded companies as of 2026 | unverified — flagged |
| 21. [A-RATE] Loaded engineer cost is approximately $3,000-4,000 per engineer-week | untested belief | Verify or flag unverified | Challenge — unverified, defensible assumed range per the estimate procedure, load-bearing on chain C2's dollar figures | unverified — flagged |
| 22. A self-hosted open-source identity server is a meaningfully different option from both "build" and "buy" | convention | Explicitly challenged before use | Discard — ruled out by chain C1 (self-hosting still carries the continuous-maintenance tax); recorded in §5 as an abandoned rival | chain C1 |

---

## 3. Ground Truths

- **GT-1** OWASP Top 10:2021 A07 "Identification and Authentication Failures" documents, as common implementation weaknesses: session IDs exposed in URLs, session identifiers reused after login instead of regenerated, sessions not properly invalidated at logout or after inactivity, credentials stored in plain text/encrypted-reversibly/weakly-hashed data stores, default admin credentials, and weak or ineffective credential-recovery ("forgot password") processes — source: OWASP Top 10:2021; read-at-source: top10.owasp.org/2021/A07_2021-Identification_and_Authentication_Failures, "Common Weaknesses" section, quoted passages on session management and credential storage/recovery.
- **GT-2** WorkOS pricing: AuthKit (session management, credential storage, password reset, MFA, user management) is free for the first 1,000,000 MAU, each additional 1,000,000 MAU is $2,500/month; SSO (SAML) connections are $125/connection/month for 1-15 connections with volume discounts to $65/connection/month at 51-100; Directory Sync (SCIM) is priced identically to SSO; audit-log streaming is $125/month and event retention $99/month — source: workos.com/pricing; read-at-source: pricing table, direct fetch.
- **GT-3** Auth0 pricing: the Free plan includes 25,000 MAU with no credit card required (both B2C and B2B); B2B Essentials starts at $150/month (500 MAU), B2B Professional at $800/month (500 MAU); one enterprise (SAML/SSO) connection is included even on the Free plan; MFA is included in Professional and available as a $100/month add-on on Essentials — source: auth0.com/pricing; read-at-source: pricing tiers table, direct fetch.
- **GT-4** Clerk pricing: the Hobby (free) tier includes 50,000 MRU; Pro is $25/month ($20/month billed annually) and includes MFA plus one enterprise (SSO) connection; additional enterprise connections are $75/month each in the 2-15 range, with volume discounts above that — source: clerk.com/pricing; read-at-source: pricing tiers table, direct fetch.
- **GT-5?** IBM's 2025 Cost of a Data Breach Report states a global average breach cost of $4.44M (down from $4.88M the prior year), a US average of $10.22M, and a mean time to identify-and-contain of 241 days — cited to: ibm.com/reports/data-breach and related IBM/press coverage; reported-by-delegate: WebSearch summary of IBM's report and secondary press coverage — the ibm.com source page itself was not opened by this analysis. This ground truth feeds no chain head; it is used only as narrative color in the second-order effects discussion (chain C5) and in the Conclusion's framing, so it is not load-bearing and the Phase 3 verification step's read-before-label trigger does not apply to it.
- **GT-6?** Company operating snapshot as stated by the requester: seven-person engineering team, approximately $40K MRR, approximately 120 paying tenants, no enterprise customers yet, and a prior auth model consisting of a single shared password plus a Stripe customer link — unverified: this is private, internal business data supplied directly by the requester about their own company; no external source exists for this analysis to open. Phase 3 failure record: source — none (private/internal data); reason — not externally verifiable, accepted as the stipulated premise of this exercise.
- **GT-7** "Authenticated, per-tenant, multi-user accounts with role boundaries" decomposes into at least eight largely-independent units of work: session management, credential storage/hashing, password reset, multi-factor authentication, invite/role management, tenant-isolation enforcement across data-access paths, audit logging, and a pre-launch security review — session management, credential storage, and password reset are named verbatim as distinct failure-prone subsystems in GT-1; MFA and an audit log are named explicitly in the task's own description of Option A; invite/role management and tenant isolation are logically necessary consequences of "multi-user-per-tenant" and "role/permission boundaries," both named explicitly in the task context — source: GT-1 (for the first three) plus the explicit task-context statement (for the remaining five); this is a definitional decomposition, not an independently-fallible empirical claim, so no further external citation applies.

**Provenance summary:** `?`-marked: GT-5, GT-6 (2 of 7). Read-at-source: GT-1 — top10.owasp.org/2021/A07_2021-Identification_and_Authentication_Failures, "Common Weaknesses" section; GT-2 — workos.com/pricing, pricing table; GT-3 — auth0.com/pricing, B2B/B2C pricing tiers table; GT-4 — clerk.com/pricing, plan comparison table. No chain in section 4 is rated HIGH confidence, so the "every unsuffixed GT feeding a HIGH-confidence chain names its read-at-source location" requirement is satisfied vacuously as well as directly (all four unsuffixed, sourced GTs above name their read-at-source location regardless).

---

## 4. Derivation Chains

### Conclusion C1: A 7-person team cannot durably self-service the continuous security-maintenance requirement that a self-built auth system permanently carries; buying externalizes most of that requirement to a vendor whose business model is built around carrying it (theoretical-limit)

GT-1 (OWASP A07 documents auth as a continuously-evolving vulnerability class) + GT-6? (7-person team, no stated dedicated security function)
→ a security-critical, internet-facing subsystem requires non-zero continuous maintenance attention for its entire operational lifetime, since new attack techniques and dependency CVEs are disclosed on an ongoing basis rather than only at build time
→ the ideal floor for a company's own headcount commitment to that attention approaches zero only when the subsystem is operated by a vendor whose core business is exactly that continuous attention
→ the conventional figure for a seven-person, fully roadmap-committed team is that close to zero of its own headcount is durably allocated to auth-specific security maintenance once a feature ships
→ building in-house locks the resulting gap onto the company itself indefinitely
→ buying transfers most of that gap onto the vendor instead *[Assumes: A-VENDORVIABILITY — the vendor remains a viable, ongoing business over the planning horizon]*

**Pre-check:** head GT-1, GT-6? — ?-marked: GT-6 · lowest cited: none · Inputs ceiling: MEDIUM
**Confidence:** MEDIUM — the qualitative direction of this argument (a small team structurally under-services ongoing security maintenance) is robust and not contingent on any single disputed figure, but it rests on GT-6?, an unverifiable stipulated team-size/stage snapshot this analysis cannot independently confirm; it would be resolved by the requester confirming current and planned security-function headcount. The A-VENDORVIABILITY premise on the final hop is priced: if a chosen vendor ceased operating, the company would fall back toward the build path's C1/C2 risk profile rather than losing service outright, since vendor data remains exportable — so this chain's endpoint is weakened, not reversed, if that premise fails. Rivals: a rival reading — that continuous attention can be handled part-time by an existing engineer without a dedicated title — is addressed in the adversarial pass (Sensitivity/Rival) and softens this chain's magnitude but does not reverse its direction.

### Conclusion C2: The in-house build path brackets to 10-26 engineer-weeks (16 central) of one-time effort plus an ongoing maintenance tax, which exceeds any plausible urgent-release window (estimate)

GT-1 (OWASP A07 failure classes) + C1 (team cannot durably service continuous maintenance)
→ decomposing "authenticated per-tenant accounts" per GT-7 into session management, credential storage, password reset, MFA, invite/role management, tenant-isolation retrofit, audit logging, and a pre-launch security review gives eight roughly independent units of work
→ assigning each unit a defensible engineer-week range (session 1-2, credential storage 1, password reset 1-2, MFA 2-3, invite/roles 2-3, tenant-isolation retrofit 3-5, audit log 1-2, security review 1-2) and summing central values yields 16 engineer-weeks of one-time build effort, bracketed 10 to 26
→ at an assumed $3,000-4,000-per-engineer-week loaded-cost rate this brackets one-time cost near $48,000-$56,000 central, on top of the recurring maintenance tax C1 already names *[Assumes: A-RATE — loaded engineer cost of roughly $3,000-4,000 per engineer-week]*
→ 16 central engineer-weeks exceeds any plausible reading of "the next billed release" as a near-term urgent deadline *[Assumes: A-HIRING — no additional engineer or contractor is added to compress the timeline]*

**Pre-check:** head GT-1, C1 (MEDIUM) — ?-marked: none directly on this head · lowest cited: MEDIUM (C1) · Inputs ceiling: MEDIUM
**Confidence:** MEDIUM — capped by citing C1 (MEDIUM); also rests on this chain's own per-subsystem week assumptions, which are Fermi-estimated with a defensible range rather than measured from this team's actual historical delivery velocity — this would rise if the requester supplied their own estimate-to-actual ratio for comparable infrastructure work. A-RATE and A-HIRING are both priced: if A-RATE were materially lower, the dollar figure would shrink but the schedule conclusion (the actual bottleneck) would be unaffected; if A-HIRING failed (a contractor were added), the wall-clock schedule could compress, which is exactly the caveat carried forward to the Conclusion. Weakest link: the tenant-isolation-retrofit line (3-5 weeks) is the largest and least certain estimate, since the team currently has zero existing tenant boundary to extend from (assumption row 8).

### Conclusion C3: The buy path brackets to 3-7 engineer-weeks (4.4 central) of one-time integration effort with near-$0 recurring cost at current scale (estimate)

GT-2 (WorkOS pricing/free tier) + GT-3 (Auth0 pricing) + GT-4 (Clerk pricing)
→ decomposing the buy path into SDK/session-validation integration, tenant/org model mapping, role/permission mapping, MFA enablement, hosted password-reset adoption, audit-log wiring, and an integration-focused security review gives seven roughly independent units of work
→ assigning each unit a defensible engineer-day range and summing central values yields 4.4 engineer-weeks of one-time integration effort, bracketed 3 to 7
→ at 120 tenants the total end-user count is very likely in the low thousands, well under every vendor's free-tier ceiling (WorkOS 1,000,000 MAU, Auth0 25,000 MAU, Clerk 50,000 MRU) *[Assumes: A-USERCOUNT — total end-users across the 120 tenants stay under those free-tier ceilings]*
→ that positions recurring core-auth cost near $0-50 per month today, rising only when enterprise SSO connections are added

**Pre-check:** head GT-2, GT-3, GT-4 — ?-marked: none · lowest cited: none · Inputs ceiling: HIGH
**Confidence:** MEDIUM — Inputs are clean (all three pricing ground truths were read at source), but the per-unit day-estimates are still Fermi-assumed rather than measured, and A-USERCOUNT is load-bearing on the third hop and not independently confirmed — this would rise to HIGH if the requester confirms actual total end-user count across the 120 tenants. Weakest link: A-USERCOUNT; if average users-per-tenant were unusually high (over roughly 200/tenant), the free tier could be exceeded sooner than assumed, though even the paid tiers here remain cheap relative to the build path.

### Conclusion C4: Scoring build, WorkOS, Clerk, and Auth0 against locked, weighted criteria makes adopting a managed identity provider — WorkOS by default — the dominant option (trade-off)

C1 (team cannot durably self-service continuous maintenance) + C2 (build brackets 10-26 weeks) + C3 (buy brackets 3-7 weeks, near-$0 recurring)
→ scoring build, WorkOS, Clerk, and Auth0 against five locked, weighted criteria (time-to-safe-ship ×5, security-risk-at-this-team-size ×5, cost-at-current-scale ×3, enterprise-readiness ×4, switching-flexibility ×2) using C2's and C3's figures and C1's risk finding yields weighted totals of 43 (build), 91 (WorkOS), 84 (Clerk), 77 (Auth0) *[Assumes: A-WEIGHTS — the locked criteria weights reflect the CTO's actual priorities]*
→ WorkOS scores equal-or-higher than Clerk on every single criterion, so no reweighting within the procedure's 1-to-5 scale can make Clerk the winner over WorkOS
→ closing the 48-point gap between build and WorkOS would require raising the one criterion where build scores higher (switching-flexibility, weight 2) to a weight of roughly 26, far outside the procedure's 1-to-5 bound, so no single-criterion reweighting flips build to the winner either
→ the highest-scoring viable option is adopting a managed identity provider, WorkOS by default, with the thin tenant/role/invite layer that stays product-specific built in-house regardless of vendor

**Pre-check:** head C1 (MEDIUM), C2 (MEDIUM), C3 (MEDIUM) — ?-marked: none directly · lowest cited: MEDIUM · Inputs ceiling: MEDIUM
**Confidence:** MEDIUM — capped by citing three MEDIUM chains. Inference is otherwise clean: the arithmetic recomputes correctly (see Adversarial pass, Recompute) and the flip-test shows the ranking is robust within the procedure's weight bounds, which is unusually strong for the Inference axis but cannot lift the band above the Inputs ceiling C1-C3 set. A-WEIGHTS is priced on the confidence line of the rival discussion below rather than left bare: if the CTO's real priorities differ from the locked weights, the ranking could shift, which is exactly why this line calls out that the CTO should sanity-check A-WEIGHTS before treating this chain as final. Rivals: Auth0-as-default is a live but weaker rival — it wins only if enterprise SSO demand is imminent (weeks, not months) enough that Auth0's deeper enterprise tooling outweighs its higher baseline cost; not settled with certainty here, see §5, Dead End 4.

### Conclusion C5: Second-order effects of adopting WorkOS do not contradict any established ground truth and confirm the recommendation's near-term payoff and longer-horizon commercial risk (second-order)

C4 (adopt WorkOS-style buy, build only the thin tenant/role layer)
→ through the actor lens, the seven engineers redirect the ten-plus weeks of saved effort to product roadmap work instead of auth internals
→ tenant admins gain a more polished hosted MFA and login experience sooner than a homegrown MVP would offer
→ the company takes on a new operational dependency on the vendor's uptime and pricing decisions
→ through the time lens, the release ships inside the urgent window and core-auth cost stays near-zero through the next several growth cycles, until the first enterprise SAML request converts a previously-blocking capability gap into a same-week configuration change
→ over a 12-to-24-month horizon the company accumulates dependence on a vendor whose pricing model has already been restructured industry-wide between 2024 and 2026, a recurring commercial risk to monitor contractually rather than a security risk *[Assumes: A-VENDORVIABILITY — already declared on chain C1]*
→ neither lens surfaces an effect that contradicts a ground truth from Phase 3, so this extension stands without returning to Phase 2

**Pre-check:** head C4 (MEDIUM) — ?-marked: none directly · lowest cited: MEDIUM (C4) · Inputs ceiling: MEDIUM
**Confidence:** MEDIUM — inherits C4's cap. Both lenses were walked and produced concrete, dated effects rather than generic risk language, which keeps Inference clean. Rivals: none live beyond what C4 already names.

### Conclusion C6: The felt urgency is a genuine schedule constraint on when the feature ships, not evidence about which implementation method is safe — treating it as the latter is the reasoning error driving pressure to cut corners (5-whys, causal mode)

GT-6? (stipulated: shared-password-only history, urgent next release)
→ drilling why the release feels urgent traces to the per-tenant auth feature gating the next billed release
→ that in turn traces to auth having been correctly deprioritized while the team chased product-market fit on a shared password, which now lands as a single blocking dependency rather than planned infrastructure work
→ the counterfactual test holds: had the release not been billed, the same per-tenant, multi-user, role-bounded requirement would still exist, so urgency is genuine schedule pressure but not itself evidence about which build method is safe
→ the root cause is a reasoning error rather than a resourcing one: treating "the feature is urgent" as license to also compress the security-sensitive implementation method, when C2 and C3 already show one method is both faster and lower-risk
→ decoupling the two variables resolves the tension: the schedule pressure is real and is answered by choosing the faster path C2 and C3 identify, not by cutting corners on whichever path is chosen

**Pre-check:** head GT-6? — ?-marked: GT-6 · lowest cited: none · Inputs ceiling: MEDIUM
**Confidence:** MEDIUM — the counterfactual test and reasoning-error diagnosis are sound given the stipulated facts, but the whole chain still rests on GT-6?'s unverifiable snapshot of the team's history and priorities; would rise with the requester's confirmation of the deferral narrative.

---

## 5. Abandoned Reasoning

### Dead End: Full in-house build now, on the stated deadline

**What was tried:** Scoped the complete in-house build (sessions, hashing, reset, MFA, invite/roles, tenant isolation, audit log) as the primary path, since the requester's Option A named it as viable.

**Why abandoned:** The Fermi estimate (chain C2) brackets one-time effort at 10-26 engineer-weeks against a stated urgent, near-term release, and the theoretical-limit finding (chain C1) shows the team cannot durably service the resulting continuous maintenance tax regardless of the one-time schedule; both are ground-truth-anchored, not merely inconvenient.

**What it ruled out:** Any variant of "build it right, just move fast" — the schedule and the safety fail together at this team size, so no amount of scoping discipline inside the build path closes the gap chain C4 measures.

### Dead End: Descope MFA and audit-log to a "v2" while still building core auth in-house

**What was tried:** Considered whether trimming the Fermi estimate's smaller line items (MFA 2.5wk central, audit log 1.5wk central) would bring the build path inside a plausible release window.

**Why abandoned:** Those two items total only 4 of the 16 central engineer-weeks; the largest and riskiest line item, the tenant-isolation retrofit (3-5wk, chain C2's named weakest link), is untouched by this descope, so it saves schedule without touching the item chain C1's security-risk finding is actually about.

**What it ruled out:** Schedule-only descoping as a fix — the bottleneck was never the smaller subsystems.

### Dead End: Self-hosted open-source identity server instead of a SaaS vendor

**What was tried:** Considered an open-source, self-operated identity provider as a middle path that avoids per-vendor SaaS pricing and lock-in while still not hand-rolling the crypto.

**Why abandoned:** Chain C1's theoretical-limit argument applies to who operates the continuous patching, not to who wrote the original code; a self-hosted system still requires the 7-person team to patch, monitor, and incident-respond on an ongoing basis, which is the exact capacity gap C1 identifies.

**What it ruled out:** "Self-hosted OSS" as a way to get buy's safety without buy's vendor dependency — it keeps the dependency that actually matters (operational attention) while discarding the one that's cheap to manage (a vendor contract).

### Dead End: Auth0 as the default vendor recommendation

**What was tried:** Scored Auth0 alongside WorkOS and Clerk in the trade-off (chain C4).

**Why abandoned:** Auth0's B2B Essentials tier floors at $150/month even at zero enterprise customers (GT-3), while WorkOS's core auth is free to 1,000,000 MAU (GT-2) with no offsetting capability advantage for a company with no enterprise customers yet. Auth0 remains a live, weaker rival, not fully closed out — see the Conclusion's trigger conditions for the case that flips it.

**What it ruled out:** Treating "most enterprise-hardened" as the deciding tie-breaker before any enterprise deal exists to justify its cost.

### Dead End: Do nothing / ship on the existing shared-password-plus-Stripe-link model

**What was tried:** Considered as the required status-quo option, per the trade-off procedure's own rule to always include doing nothing.

**Why abandoned:** Knocked out by the must-have that the gated feature requires multiple authenticated users per tenant with role boundaries — a single shared password structurally cannot express that, independent of any scoring.

**What it ruled out:** Treating the release deadline as negotiable within this analysis — the analysis takes the feature requirement as fixed and reasons only about implementation method, per the essence statement's success criteria.

### Dead End: A batteries-included OSS auth framework substantially shrinks the build estimate below chain C2's bracket

**What was tried:** Considered whether choosing a framework with built-in session/MFA/password-reset scaffolding would compress chain C2's 16-week central estimate closer to the buy path's 4.4 weeks.

**Why abandoned as the deciding factor:** Even generous scaffolding does not touch the two largest, least-portable line items — the tenant-isolation retrofit onto a codebase with no existing tenant boundary (a data-model and query-path problem the framework's login scaffolding does not solve) and chain C1's continuous-maintenance-tax finding (which is about who operates ongoing patching, not how much boilerplate the team wrote).

**What it ruled out:** Framework choice alone as a way to make "build" schedule-competitive with "buy"; it can narrow the gap but not close the two structural items that drive chains C1 and C2's conclusions.

---

## 6. Conclusion

**Recommended approach:** Adopt a managed identity provider now — WorkOS AuthKit as the default choice — for session management, credential storage, password reset, MFA, and audit logging; build only the thin, product-specific tenant/org data model and role-to-feature permission mapping in-house, since that layer is not meaningfully outsourceable. Ship the gated release on the buy path's 3-7 week integration bracket rather than the build path's 10-26 week bracket (chain C4).

**Key insight:** The real choice was never "build vs. buy the login form." A 7-person team's binding constraint is not engineering skill but the structural inability to durably service the non-zero continuous security-maintenance tax that any self-built, internet-facing credential system carries for its entire operating life; buying doesn't just save weeks, it transfers that permanent tax to a vendor whose business model is built around carrying it (chain C1). This is why cost and speed favor the same option as security — the intuitive framing that "buy is faster but build is more secure once it's reviewed properly" does not hold at this team size (chain C1).

**Trade-offs acknowledged:** This recommendation accepts a new commercial and operational dependency on WorkOS's pricing and uptime, which have already been restructured industry-wide once between 2024 and 2026 (chain C5); it defers Auth0's deeper enterprise-compliance tooling until an actual enterprise pipeline materializes rather than paying for it pre-emptively (chain C4); and it still requires disciplined engineering on the tenant/role-mapping layer the company keeps in-house, since buying narrows where security care is needed rather than eliminating the need for it (chain C4). Whether switching vendors or reverting to a self-built system later would be cheap or costly remains untested — no chain — flagged assumption only.

**Pre-check:** head C1 (MEDIUM), C2 (MEDIUM), C3 (MEDIUM), C4 (MEDIUM), C5 (MEDIUM), C6 (MEDIUM) — ?-marked: none directly (the `?`-marked ground truths sit upstream inside these chains) · lowest cited: MEDIUM · Inputs ceiling: MEDIUM
**Confidence:** MEDIUM — every contributing chain is MEDIUM (chain C1 rests on GT-6?'s unverifiable team-snapshot; chain C2 additionally rests on Fermi-assumed per-subsystem weeks and A-RATE/A-HIRING; chain C3 rests on A-USERCOUNT; chain C4 rests on citing C1-C3 plus A-WEIGHTS; chain C5 inherits C4; chain C6 rests on GT-6?). Nothing here is LOW: Inference and Rivals are each clean at the Conclusion level — the trade-off ranking is robust to reweighting within the procedure's bounds (chain C4), and the two live rivals (Auth0-as-default; a self-hosted OSS identity server) are each explicitly ruled out or bounded in §5. The single fastest way to move this Conclusion toward HIGH is for the CTO to confirm GT-6?'s team-size/stage snapshot and A-USERCOUNT's actual total end-user figure — both are cheap for the requester to confirm and both currently cap the analysis at MEDIUM rather than reflecting genuine uncertainty about the recommendation's direction.

**Revisit triggers (each names the criterion or chain it would change):**
- If an enterprise pipeline with imminent (weeks-scale) SAML/SSO demand appears, re-run chain C4 with Enterprise-readiness weighted higher — Auth0 becomes the live rival worth reconsidering (chain C4).
- If MRR or tenant count grows enough to approach vendor free-tier ceilings, re-verify actual total end-user count before assuming near-zero recurring cost (chain C3).
- If engineering headcount grows to include a dedicated security/platform function, chain C1's theoretical-limit finding weakens and the build path becomes reconsiderable (chain C1).

---

## Self-Audit Gate (process output)

**Criterion 1: Identify Essence**
Quoted span: "Given a seven-person engineering team with no dedicated security function that must ship its first real per-tenant, multi-user, role-bounded authentication system under a fixed release deadline, which implementation path... minimizes the combination of security-failure risk and schedule risk to the committed release, without foreclosing near-term enterprise SSO/SAML requirements?"
Band: **Rigorous**
Justification: The statement names the underlying resourcing/risk trade-off rather than restating "should we build or buy auth," each of the five success criteria is a checkable verb+subject+outcome triplet scoreable against section 6, and the statement is specific to this company's team size, deadline, and no-enterprise-yet stage rather than a generic template.

**Criterion 2: Challenge Assumptions**
Quoted span: "3. Urgency justifies cutting corners on the security-sensitive build/buy decision | convention | Explicitly challenged before use | Discard — refuted by chain C6..." and the Assumption Audit scan's closing line: "Surfaced and added to the Classified Assumptions Table (section 2, rows 17-21): A-HIRING, A-USERCOUNT, A-WEIGHTS, A-VENDORVIABILITY, A-RATE."
Band: **Rigorous**
Justification: All 22 rows use the four-type scheme with em-dash-separated Verdict tokens and specific Verification cells (no bare "unclear"); multiple rows are Discarded (not merely Accepted); every chain-derived assumption the Assumption Audit surfaced was added to this table, confirmed exhaustive against all 29 chain steps in the Assumption Audit scan.

**Criterion 3: Establish Ground Truths**
Quoted span: "Provenance summary: `?`-marked: GT-5, GT-6 (2 of 7). Read-at-source: GT-1 — top10.owasp.org/2021/A07_2021-Identification_and_Authentication_Failures... GT-2 — workos.com/pricing... GT-3 — auth0.com/pricing... GT-4 — clerk.com/pricing..."
Band: **Rigorous**
Justification: Every GT carries a stable ID matching the identifiers used in section 4, a provenance label, and the `?`-marked entries are enumerated by ID and match the two suffixed entries in the list; no criterion-3 chain in this analysis is rated HIGH, so the read-at-source-for-HIGH-chains requirement is vacuously and also directly satisfied (all four unsuffixed GTs name a read-at-source location regardless).

**Criterion 4: Reason Upward**
Quoted span (self-audit scan, chain-form table): "C1 | GT-1 + GT-6? | yes | n/a | yes | MEDIUM | yes | none" through "C6 | GT-6? | yes | n/a | yes | MEDIUM | yes | none" — all six rows read `Form conforming? = yes`, `Dependency clean? = yes`.
Band: **Rigorous**
Justification: All six chains carry a genuine intermediate distinct from any single head input, no hop begins with a `GT-N` identifier, every chain-introduced assumption not already in the table carries an inline `[Assumes: A-N]` tag (verified against the Assumption Audit scan), no analogy is used as direct evidence anywhere in section 4, and Abandoned Reasoning documents six dead ends each with a specific structural abandonment reason (not "ran out of time").

**Criterion 5: Validate**
Quoted span: "no chain in this analysis is rated HIGH confidence while consuming a GT-N? input (C1 and C6 both consume GT-6? and are rated MEDIUM)" and the Adversarial pass record's five labeled parts (Recompute, Sensitivity, Rival, the pre-mortem Premise/Causes/Clusters/Disposition, Falsification), each cluster in the pre-mortem carrying a named plan change or an explicitly accepted risk with a named mitigation.
Band: **Rigorous**
Justification: Every chain's confidence line names its `GT-N?` inputs with a stated verification path, every chain is rated no higher than the lowest-rated chain its head cites (C2/C4/C5 all correctly capped at MEDIUM by citing MEDIUM chains), the Conclusion's MEDIUM rating matches its weakest contributing chains exactly, and the adversarial pass record is complete with all four clusters carrying a disposition.

**Criterion 6: Conclusion-to-Ground-Truth Traceability**
Quoted span (self-audit scan, claim-inventory table): "Scan complete: 6 chain rows... 9 section-6 rows... 8 claims under R11, 1 excluded... 0 claims untraced (1 claim carries the honest `no chain — flagged assumption only` marker...)"
Band: **Rigorous**
Justification: Every section-6 claim either cites a specific section-4 chain inline or carries the honest untraced marker (never both silent), no new reasoning is introduced in section 6 beyond what sections 4 established, and the Key Insight (the continuous-maintenance-tax reframe, chain C1) is a non-obvious finding distinct from the Recommended approach's "adopt WorkOS" restatement.

**Gate result:** No criterion scored Absent; zero criteria scored Hand-wavy (the cap of at most one is not approached). Both pass conditions are met — this analysis clears the Self-Audit Gate on the first pass, with no re-perception pass required.
